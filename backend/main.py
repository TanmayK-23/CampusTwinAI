from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import engine, SessionLocal
from backend.models import schema
from backend.routes import crowd, shuttle, benchmark
import asyncio
import random

# Create DB tables
schema.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Twin AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crowd.router, prefix="/crowd")
app.include_router(shuttle.router, prefix="/route")
app.include_router(benchmark.router, prefix="/benchmark")

async def update_live_data():
    """Background task to subtly modify crowd densities every few seconds to simulate live data."""
    while True:
        await asyncio.sleep(5)
        # We need a new session per task to avoid thread issues
        db: Session = SessionLocal()
        try:
            # Get the exact model prediction for the current hour
            current_predictions = crowd.predict_crowd(hours_ahead=0)["predicted_densities"]
            
            zones = ["Biotech_Block", "Canteen", "Ground", "Hostel", "MB_Block", "TP1", "TP2", "Auditorium"]
            for zone in zones:
                latest = db.query(schema.CrowdLog).filter(schema.CrowdLog.zone_id == zone).order_by(schema.CrowdLog.id.desc()).first()
                target_density = current_predictions.get(zone, 50)
                
                if latest:
                    # Move 10% towards the ML model target + 2% random jitter to keep it looking "alive" realtime
                    diff = (target_density - latest.density) * 0.1
                    jitter = random.uniform(-2, 2)
                    new_density = max(0, latest.density + diff + jitter)
                    
                    latest.density = new_density
            db.commit()
        except Exception as e:
            print(f"Error updating live data: {e}")
        finally:
            db.close()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_live_data())


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming signals
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
def read_root():
    return {"status": "Campus Twin AI Backend Running"}
