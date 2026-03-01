# Campus Twin AI – Predictive Digital Twin for Smart Campuses

## Overview
Campus Twin AI is a full-stack, predictive digital twin system built for smart campuses. It provides real-time crowd density tracking and AI-driven shuttle routing, displayed seamlessly on a 3D campus map. 

## Features
- **3D Campus Map**: Built with Three.js (`@react-three/fiber`), rendering 8 custom building zones (including the Auditorium) based on real-time crowd density.
- **Predictive ML Models**: Employs an external pre-trained XGBoost Regressor and Classifier pipeline (`campus_xgb_classifier.json`) for live intelligence mapping.
- **GPU Benchmarking**: Real-time evaluation of backend inference speed (CPU vs GPU speeds).
- **Simulation Mode**: Test "what-if" scenarios (e.g., Opening Gates, Adding Shuttles) and instantly see the calculated impact on congestion on a glowing overlay dashboard.
- **Demo Reliability Mode**: A dedicated script to preload a consistent database state for flawless presentations.

## Tech Stack
- **Frontend**: React (Vite), TailwindCSS, Three.js, Recharts, Lucide Icons
- **Backend**: FastAPI, Uvicorn, SQLite (Zero-Config MVP for smooth Demo), WebSockets via FastAPI
- **ML/AI**: XGBoost, Scikit-Learn, NetworkX

## Setup Instructions

### 1. Backend Setup
Navigate to the project root and create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Generate Data and Preload State
Run these two scripts to initialize the background CSV data and preload the SQLite database for a guaranteed flawless UI demo:
```bash
# Generate synthetic temporal arrays and datasets
export PYTHONPATH=. 
python3 data/generate_data.py

# Inject the XGBoost pre-trained models into the DB for Demo Reliability Mode
python3 preload_demo_state.py
```

### 3. Run Backend Server
```bash
uvicorn backend.main:app --reload --port 8000
```
*API docs available at `http://localhost:8000/docs`*

### 4. Run Frontend Server
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173` in your browser.

## How to run Hardware Benchmark
The dashboard automatically fetches inference metrics from the `/benchmark/inference` endpoint. The PyTorch script in `backend/ml/benchmark.py` automatically detects `mps` on your Mac M2 or `cuda` on an RTX GPU, spinning up generic execution loops to calculate parallel hardware speedups compared to standard CPU execution. The results are permanently displayed on the top Navigation Bar.
