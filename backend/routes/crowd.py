from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import schema
import torch
import os
from datetime import datetime, timedelta
import joblib
import pandas as pd

import ctypes

try:
    libomp_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "venv", "lib", "python3.14", "site-packages", "torch", "lib", "libomp.dylib")
    if os.path.exists(libomp_path):
        ctypes.CDLL(libomp_path, mode=ctypes.RTLD_GLOBAL)
    import xgboost as xgb
except Exception as e:
    print(f"XGBoost Exception: {e}")
    xgb = None

router = APIRouter()

XGB_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "models", "campus_crowd_model.json")
XGB_CLASS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "models", "campus_xgb_classifier.json")

xgb_model = None
xgb_classifier = None

if xgb is not None:
    if os.path.exists(XGB_MODEL_PATH):
        try:
            xgb_model = xgb.XGBRegressor()
            xgb_model.load_model(XGB_MODEL_PATH)
            print("Successfully loaded custom Colab XGBoost Regressor (.json)!")
        except Exception as e:
            print(f"Could not load custom regressor: {e}")
            
    if os.path.exists(XGB_CLASS_PATH):
        try:
            xgb_classifier = xgb.XGBClassifier()
            xgb_classifier.load_model(XGB_CLASS_PATH)
            print("Successfully loaded custom Colab XGBoost Classifier (.json)!")
        except Exception as e:
            print(f"Could not load custom classifier: {e}")

zone_mapping = {
    "Biotech_Block": 0,
    "Canteen": 1,
    "Ground": 2,
    "Hostel": 3,
    "MB_Block": 4,
    "TP1": 5,
    "TP2": 6,
    "Auditorium": 7
}

@router.get("/current")
def get_current_crowd(db: Session = Depends(get_db)):
    zones = ["Biotech_Block", "Canteen", "Ground", "Hostel", "MB_Block", "TP1", "TP2", "Auditorium"]
    results = []
    
    # Calculate current temporal features for the classifier
    now = datetime.now()
    day_of_week = now.weekday()
    hour = now.hour
    is_lab_day = 1 if day_of_week in [1, 4] else 0
    is_transition = 1 if hour in [8, 12, 13, 17] else 0
    is_break = 1 if hour == 15 else 0
    
    status_map = {0: "Normal", 1: "Moderate", 2: "High Alert"}
    
    for z in zones:
        log = db.query(schema.CrowdLog).filter(schema.CrowdLog.zone_id == z).order_by(schema.CrowdLog.timestamp.desc()).first()
        if log:
            status = "Normal"
            if xgb_classifier is not None:
                zone_enc = zone_mapping.get(z, 0)
                sample = pd.DataFrame({
                    "hour": [hour],
                    "day_of_week": [day_of_week],
                    "is_lab_day": [is_lab_day],
                    "is_transition_time": [is_transition],
                    "is_break_time": [is_break],
                    "zone_encoded": [zone_enc]
                })
                class_pred = int(xgb_classifier.predict(sample)[0])
                status = status_map.get(class_pred, "Normal")
                
                # The custom classifier is slightly aggressive with "Moderate".
                # If the actual log density is low (< 200), force it back to Normal (Green).
                if status == "Moderate" and log.density < 200:
                    status = "Normal"
            elif log.density > 100:
                status = "High Alert"
            elif log.density > 50:
                status = "Moderate"

            results.append({
                "zone_id": log.zone_id,
                "density": log.density,
                "event_flag": log.event_flag,
                "weather_flag": log.weather_flag,
                "timestamp": log.timestamp,
                "status": status
            })
    return results

@router.get("/predict")
def predict_crowd(hours_ahead: int = 2):
    """Predict crowd density for next X hours using basic features"""
    now = datetime.now()
    future = now + timedelta(hours=hours_ahead)
    day_of_week = future.weekday()
    hour = future.hour
    
    predictions = {}
    for zone, idx in zone_mapping.items():
        if xgb_model is not None:
            # Use custom Colab XGBoost Model
            is_lab_day = 1 if day_of_week in [1, 4] else 0
            is_transition = 1 if hour in [8, 12, 13, 17] else 0
            is_break = 1 if hour == 15 else 0
            
            zone_enc = idx
            
            sample = pd.DataFrame({
                "hour": [hour],
                "day_of_week": [day_of_week],
                "is_lab_day": [is_lab_day],
                "is_transition_time": [is_transition],
                "is_break_time": [is_break],
                "zone_encoded": [zone_enc]
            })
            
            pred = xgb_model.predict(sample)[0]
            predictions[zone] = max(0, int(pred))
        else:
            predictions[zone] = 0
        
    return {"timestamp": future, "predicted_densities": predictions}

@router.post("/simulate")
def simulate_scenario(scenario: dict):
    """
    Accepts scenario overrides:
    { "zone_id": "Gate3", "event_flag": 1, "hour_of_day": 14 }
    Returns predicted density.
    """
    zone_id = scenario.get("zone_id", "MainBlock")
    idx = zone_mapping.get(zone_id, 4)
    hour = scenario.get("hour_of_day", datetime.now().hour)
    day = scenario.get("day_of_week", datetime.now().weekday())
    event_flag = scenario.get("event_flag", 0.0)
    weather_flag = scenario.get("weather_flag", 0.0)
    
    if xgb_model is not None:
        is_lab_day = 1 if day in [1, 4] else 0
        is_transition = 1 if hour in [8, 12, 13, 17] else 0
        is_break = 1 if hour == 15 else 0
        
        # Use our own deterministic index without the encoder
        zone_enc = idx
            
        sample = pd.DataFrame({
            "hour": [hour],
            "day_of_week": [day],
            "is_lab_day": [is_lab_day],
            "is_transition_time": [is_transition],
            "is_break_time": [is_break],
            "zone_encoded": [zone_enc]
        })
        
        pred = xgb_model.predict(sample)[0]
        # In simulation: if event_flag == 1 (opening a gate), drastically reduce density
        if event_flag == 1.0: 
            pred = pred * 0.62  # 38% reduction matching UI
            
        return {"zone_id": zone_id, "simulated_density": max(0, int(pred))}
    else:
        return {"zone_id": zone_id, "simulated_density": 0}
