from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import schema
import torch
import os
from datetime import datetime, timedelta
from backend.ml.torch_models import CrowdMLP

router = APIRouter()

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "models", "crowd_mlp.pt")
model = CrowdMLP(5)
if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

zone_mapping = {"Library": 0, "Gate3": 1, "Cafeteria": 2, "HostelArea": 3, "MainBlock": 4}

@router.get("/current")
def get_current_crowd(db: Session = Depends(get_db)):
    """Returns the latest crowd logs (our current 'live' state)"""
    zones = ["Library", "Gate3", "Cafeteria", "HostelArea", "MainBlock"]
    results = []
    for z in zones:
        log = db.query(schema.CrowdLog).filter(schema.CrowdLog.zone_id == z).order_by(schema.CrowdLog.timestamp.desc()).first()
        if log:
            results.append({
                "zone_id": log.zone_id,
                "density": log.density,
                "event_flag": log.event_flag,
                "weather_flag": log.weather_flag,
                "timestamp": log.timestamp
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
        # Feature vector: [zone_idx, hour_of_day, day_of_week, event_flag, weather_flag]
        # Assume no events or weather for generic prediction
        x = torch.tensor([[idx, hour, day_of_week, 0.0, 0.0]], dtype=torch.float32)
        with torch.no_grad():
            pred = model(x).item()
        predictions[zone] = max(0, round(pred, 2))
        
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
    
    x = torch.tensor([[idx, hour, day, float(event_flag), float(weather_flag)]], dtype=torch.float32)
    with torch.no_grad():
        pred = model(x).item()
        
    return {"zone_id": zone_id, "simulated_density": max(0, round(pred, 2))}
