from fastapi import APIRouter
from backend.ml.benchmark import run_benchmark

router = APIRouter()

@router.get("/inference")
def get_benchmark():
    """Returns the CPU vs GPU benchmark for the model inference."""
    results = run_benchmark()
    return results
