from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import schema
from backend.ml.shuttle import optimize_route

router = APIRouter()

@router.get("/optimize")
def optimize_shuttle(route_name: str = "Campus Loop", db: Session = Depends(get_db)):
    """ Returns an optimized path. Simulates skipping low demand stops """
    # Get current route
    db_route = db.query(schema.ShuttleRoute).filter(schema.ShuttleRoute.route_name == route_name).first()
    if not db_route:
        # Default fallback
        stops = ["Gate1", "Library", "Hostel", "Cafeteria"]
    else:
        stops = db_route.stops
        
    start_point = stops[0]
    target_stops = stops[1:] # In reality, filter by current demand here
    
    result = optimize_route(start_point, target_stops)
    return {
        "route_name": route_name,
        "suggested_route": result["suggested_route"],
        "expected_delay_reduction_pct": result["expected_delay_reduction_pct"],
        "total_time_mins": result["total_time_mins"]
    }
