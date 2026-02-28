import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_crowd_data():
    zones = ["Library", "Gate3", "Cafeteria", "HostelArea", "MainBlock"]
    start_date = datetime.now() - timedelta(days=30)
    
    records = []
    
    for day in range(30):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.weekday()
        
        # 10% chance of an event today
        has_event_today = np.random.rand() < 0.1
        # Weather: 0=Clear, 1=Rainy
        weather = 1 if np.random.rand() < 0.2 else 0
        
        for hour in range(24):
            for zone in zones:
                # Base density depending on hour (peak around 12-14 and 17-18)
                base = 20
                if 8 <= hour <= 18:
                    base = 60
                if 12 <= hour <= 14 or 17 <= hour <= 18:
                    base = 100
                
                # Modifiers
                if day_of_week >= 5:  # Weekend
                    base *= 0.4
                if has_event_today and hour >= 16:
                    base *= 1.8
                if weather == 1:
                    base *= 0.7
                    
                # Zone specifics
                if zone == "Library" and hour > 21: base *= 2  # late night studying
                if zone == "Gate3" and (hour == 9 or hour == 17): base *= 1.5
                
                # Add noise
                density = max(0, int(np.random.normal(base, base * 0.2)))
                
                records.append({
                    "timestamp": current_date.replace(hour=hour, minute=0, second=0, microsecond=0),
                    "zone_id": zone,
                    "hour_of_day": hour,
                    "day_of_week": day_of_week,
                    "event_flag": int(has_event_today),
                    "weather_flag": weather,
                    "density": density
                })

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, "crowd_data.csv"), index=False)
    print(f"Generated {len(df)} crowd records")


def generate_equipment_data():
    records = []
    for i in range(1, 101):
        age_days = np.random.randint(30, 1000)
        usage_hours = min(age_days * 24, np.random.randint(100, 10000))
        avg_temperature = np.random.normal(45, 10)  # C
        maintenance_history = np.random.randint(0, 10)
        
        # Formula for failure probability
        # Higher age, higher usage, higher temp -> more failure. More maintenance -> less failure
        risk_score = (usage_hours / 10000) * 0.4 + (age_days / 1000) * 0.3 + (max(0, avg_temperature - 40) / 40) * 0.4 - (maintenance_history * 0.05)
        
        failure_prob = np.clip(risk_score, 0, 1)
        
        if failure_prob < 0.3:
            category = "Low"
        elif failure_prob < 0.7:
            category = "Medium"
        else:
            category = "High"
            
        records.append({
            "equipment_id": f"EQ_{i:03d}",
            "usage_hours": usage_hours,
            "avg_temperature": round(avg_temperature, 2),
            "maintenance_history": maintenance_history,
            "age_days": age_days,
            "failure_probability": round(failure_prob, 4),
            "risk_category": category
        })
        
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, "equipment_data.csv"), index=False)
    print(f"Generated {len(df)} equipment records")


def generate_shuttle_data():
    # Shuttle data: 7 days of demand patterns per stop
    stops = ["Gate1", "Library", "Hostel", "Cafeteria", "DeptA"]
    records = []
    start_date = datetime.now() - timedelta(days=7)
    
    for day in range(7):
        current_date = start_date + timedelta(days=day)
        for hour in range(8, 22):  # Shuttles run 8 AM to 10 PM
            for stop in stops:
                base_demand = np.random.randint(5, 30)
                if hour in [9, 17]: base_demand *= 2  # rush hour
                if stop == "Hostel" and hour == 9: base_demand *= 1.5
                if stop == "DeptA" and hour == 17: base_demand *= 1.5
                
                records.append({
                    "timestamp": current_date.replace(hour=hour, minute=0, second=0, microsecond=0),
                    "stop_id": stop,
                    "demand": int(base_demand)
                })

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, "shuttle_demand.csv"), index=False)
    print(f"Generated {len(df)} shuttle demand records")

if __name__ == "__main__":
    generate_crowd_data()
    generate_equipment_data()
    generate_shuttle_data()
    print("Synthetic data generation complete.")
