import os
import pandas as pd
from datetime import datetime, timedelta
from backend.database import SessionLocal, engine
from backend.models import schema

def preload_database():
    print("Preloading demo state into PostgreSQL...")
    schema.Base.metadata.drop_all(bind=engine)
    schema.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 1. Load Equipment
    equip_df = pd.read_csv("data/equipment_data.csv")
    for _, row in equip_df.iterrows():
        eq = schema.EquipmentStatus(
            equipment_id=row['equipment_id'],
            usage_hours=row['usage_hours'],
            avg_temperature=row['avg_temperature'],
            maintenance_history=row['maintenance_history'],
            age_days=row['age_days'],
            failure_probability=row['failure_probability'],
            risk_category=row['risk_category']
        )
        db.add(eq)
        
    # 2. Add explicit Demo predictable failure for demo reliability
    # Let's override EQ_001 to be failing definitively
    demo_eq = db.query(schema.EquipmentStatus).filter(schema.EquipmentStatus.equipment_id == "EQ_001").first()
    if demo_eq:
        demo_eq.usage_hours = 9500
        demo_eq.avg_temperature = 85.5
        demo_eq.age_days = 2000
        demo_eq.maintenance_history = 0
        demo_eq.failure_probability = 0.98
        demo_eq.risk_category = "High"
        
    # 3. Load basic events
    demo_event = schema.Event(
        name="Tech Symposium 2026",
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=4),
        impact_zone="MainBlock"
    )
    db.add(demo_event)
    
    # 4. Load partial crowd logs (just the demo state)
    # We will insert a known crowd spike at MainBlock
    zones = ["Library", "Gate3", "Cafeteria", "HostelArea", "MainBlock"]
    now = datetime.now()
    
    for zone in zones:
        density = 50.0
        if zone == "MainBlock": density = 180.0 # Force crowd spike for demo
        log = schema.CrowdLog(
            zone_id=zone,
            timestamp=now,
            density=density,
            event_flag=True if zone == "MainBlock" else False,
            weather_flag="clear"
        )
        db.add(log)
        
    # 5. Default shuttle routes
    route1 = schema.ShuttleRoute(route_name="Campus Loop", stops=["Gate1", "Library", "Hostel", "Cafeteria"])
    route2 = schema.ShuttleRoute(route_name="Express Dept", stops=["Gate1", "DeptA"])
    db.add(route1)
    db.add(route2)

    db.commit()
    db.close()
    print("Demo state successfully preloaded.")

if __name__ == "__main__":
    preload_database()
