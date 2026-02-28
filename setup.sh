#!/bin/bash

echo "============================================="
echo " Campus Twin AI - automated Setup Script"
echo "============================================="

# 1. Backend Setup
echo -e "\n[1/3] Setting up Python Backend..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment & installing pip packages..."
source venv/bin/activate
pip install -r backend/requirements.txt

# 2. Frontend Setup
echo -e "\n[2/3] Setting up React + Vite Frontend..."
cd frontend
npm install
cd ..

echo -e "\n[3/3] Setup complete!"
echo "---------------------------------------------"
echo "To run the backend:"
echo "  source venv/bin/activate"
echo "  export PYTHONPATH=."
echo "  uvicorn backend.main:app --reload --port 8000"
echo "---------------------------------------------"
echo "To run the frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo "============================================="
