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
            zones = ["Library", "Gate3", "Cafeteria", "HostelArea", "MainBlock"]
            for zone in zones:
                latest = db.query(schema.CrowdLog).filter(schema.CrowdLog.zone_id == zone).order_by(schema.CrowdLog.id.desc()).first()
                if latest:
                    # Random walk by -5 to +5 people
                    diff = random.uniform(-5, 5)
                    new_density = max(0, latest.density + diff)
                    
                    # Create a new log instead of mutating so we have historical graph (if needed) or just update latest
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
