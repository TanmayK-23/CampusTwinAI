# Campus Twin AI – Predictive Digital Twin for Smart Campuses

## Overview
Campus Twin AI is a full-stack, predictive digital twin system built for smart campuses. It provides real-time crowd density tracking and AI-driven shuttle routing, displayed seamlessly on a 3D campus map. 

## Features
- **3D Campus Map**: Built with Three.js (`@react-three/fiber`), rendering live heatmaps for crowd density.
- **Predictive ML Models**: PyTorch-based MLPs for crowd forecasting (with SHAP feature importance).
- **GPU Benchmarking**: Real-time evaluation of model inference speed (CPU vs GPU).
- **Simulation Mode**: Test "what-if" scenarios (e.g., Opening Gates, Adding Shuttles) and instantly see the calculated impact on congestion, downtime, and energy on a glowing overlay dashboard.
- **Demo Reliability Mode**: A dedicated script to preload a consistent database state for flawless presentations.

## Tech Stack
- **Frontend**: React (Vite), TailwindCSS, Three.js, Recharts, Lucide Icons
- **Backend**: FastAPI, Uvicorn, SQLite (Zero-Config MVP for smooth Demo), WebSockets via FastAPI
- **ML/AI**: PyTorch, Scikit-Learn, SHAP, NetworkX

## Setup Instructions

### 1. Backend Setup
Navigate to the project root and create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Generate Data and Train Models
Our data generation and ML pipelines are ready natively:
```bash
# Generate synthetic datasets (Crowd, Equipment, Shuttle usage)
export PYTHONPATH=. 
python3 data/generate_data.py

# Train PyTorch MLPs and save models
python3 models/train.py

# Preload the database for Demo Reliability Mode
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

## How to run GPU Benchmark
The dashboard automatically fetches inference metrics from the `/benchmark/inference` endpoint. The PyTorch script in `backend/ml/benchmark.py` automatically detects `mps` on your Mac M2 or `cuda` on an RTX 3050 and calculates the inference speedup compared to standard CPU execution. The results are permanently displayed on the top Navigation Bar.
