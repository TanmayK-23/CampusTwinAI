from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from backend.database import Base

class CrowdLog(Base):
    __tablename__ = "crowd_logs"
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    density = Column(Float)
    event_flag = Column(Boolean, default=False)
    weather_flag = Column(String, default="clear")

class EquipmentStatus(Base):
    __tablename__ = "equipment_status"
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(String, index=True)
    usage_hours = Column(Float)
    avg_temperature = Column(Float)
    maintenance_history = Column(Integer)
    age_days = Column(Integer)
    failure_probability = Column(Float, nullable=True)
    risk_category = Column(String, nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ShuttleRoute(Base):
    __tablename__ = "shuttle_routes"
    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String)
    stops = Column(JSON)
    active_shuttles = Column(Integer, default=1)
    
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    impact_zone = Column(String)
