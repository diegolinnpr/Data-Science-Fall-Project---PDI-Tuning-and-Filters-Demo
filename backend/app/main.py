from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .simulate import run_simulation

app = FastAPI(title="PID Tuning & Filters Demo")

app.add_middleware(
    CORSMiddleware,
    # Vite's default dev server ports.
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    kp: float = 1.0
    ki: float = 0.0
    kd: float = 0.0
    setpoint: float = 1.0
    plant_type: str = "first_order"
    filter_type: str = "none"
    filter_params: dict = {}
    duration: float = 10.0
    dt: float = 0.02
    noise_std: float = 0.0
    seed: int = 42


@app.post("/api/simulate")
def simulate(request: SimulationRequest) -> dict:
    try:
        return run_simulation(**request.model_dump())
    except (ValueError, NotImplementedError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}
