"""Ties a PIDController, a plant, and a filter together into a time series."""

import numpy as np

from .filters import FILTERS
from .pid import PIDController
from .plant import FirstOrderPlant, SecondOrderPlant

PLANTS = {
    "first_order": FirstOrderPlant,
    "second_order": SecondOrderPlant,
}


def run_simulation(
    kp: float,
    ki: float,
    kd: float,
    setpoint: float,
    plant_type: str = "first_order",
    filter_type: str = "none",
    filter_params: dict | None = None,
    duration: float = 10.0,
    dt: float = 0.02,
    noise_std: float = 0.0,
    seed: int = 42,
) -> dict:
    """Run a fixed-timestep simulation and return time series arrays.

    The control loop each step is: measure plant -> add sensor noise ->
    filter -> feed to PID -> apply PID output back to the plant.
    """
    if plant_type not in PLANTS:
        raise ValueError(f"Unknown plant_type: {plant_type!r}")
    if filter_type not in FILTERS:
        raise ValueError(f"Unknown filter_type: {filter_type!r}")

    plant = PLANTS[plant_type]()
    pid = PIDController(kp=kp, ki=ki, kd=kd, setpoint=setpoint)
    signal_filter = FILTERS[filter_type](**(filter_params or {}))

    rng = np.random.default_rng(seed)
    steps = int(duration / dt)

    time = np.zeros(steps)
    setpoint_series = np.full(steps, setpoint)
    raw_measurement = np.zeros(steps)
    filtered_measurement = np.zeros(steps)
    control_output = np.zeros(steps)

    control = 0.0
    for i in range(steps):
        measurement = plant.value + rng.normal(0.0, noise_std)
        filtered = signal_filter.apply(measurement)
        control = pid.step(filtered, dt)
        plant.step(control, dt)

        time[i] = i * dt
        raw_measurement[i] = measurement
        filtered_measurement[i] = filtered
        control_output[i] = control

    return {
        "time": time.tolist(),
        "setpoint": setpoint_series.tolist(),
        "raw_measurement": raw_measurement.tolist(),
        "filtered_measurement": filtered_measurement.tolist(),
        "control_output": control_output.tolist(),
    }
