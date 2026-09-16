"""Run with `pytest` from the repo root. These should all pass once
Issues #1 and #2 are implemented -- use them to check your work.
"""

import pytest

from pid.pid_controller import PIDController
from pid.plant import FirstOrderPlant


def test_proportional_only_pushes_toward_setpoint():
    pid = PIDController(kp=1.0, ki=0.0, kd=0.0, setpoint=10.0)
    assert pid.step(measurement=0.0, dt=0.1) == pytest.approx(10.0)


def test_zero_error_gives_zero_output():
    pid = PIDController(kp=2.0, ki=1.0, kd=1.0, setpoint=5.0)
    assert pid.step(measurement=5.0, dt=0.1) == pytest.approx(0.0)


def test_reset_clears_state():
    pid = PIDController(kp=0.0, ki=1.0, kd=0.0, setpoint=1.0)
    pid.step(measurement=0.0, dt=1.0)
    pid.reset()
    assert pid.step(measurement=0.0, dt=1.0) == pytest.approx(1.0)


def test_first_order_plant_settles_toward_gain_times_input():
    plant = FirstOrderPlant(gain=2.0, time_constant=1.0)
    for _ in range(2000):
        plant.step(u=1.0, dt=0.01)
    assert plant.value == pytest.approx(2.0, abs=0.05)
