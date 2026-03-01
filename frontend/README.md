# Campus Twin AI Frontend

This is the React frontend for the Campus Twin AI predictive digital twin.

## Tech Stack
- **React (Vite)**
- **Three.js** (`@react-three/fiber`, `@react-three/drei`) for the 3D campus visualization
- **Tailwind CSS** for UI styling
- **Recharts** for live telemetry charts

## Features
- **Live 3D Map**: Visualizes 8 campus zones (including the Auditorium) with real-time crowd density mapped to XGBoost classifications (Normal = Green, Moderate = Yellow, High Alert = Red).
- **WebSockets**: Subscribes to the FastAPI backend for sub-second telemetry updates.
- **AI Route Optimizer**: Displays Dijkstra-computed active shuttle paths dynamically on the UI.
- **What-If Simulations**: Allows clicking intervention buttons (e.g. "Add Extra Shuttle") to recalculate metrics instantly.

## Running Locally

From the root `Campus Twin AI` directory:

```bash
cd frontend
npm install
npm run dev
```

Then visit `http://localhost:5173`.
