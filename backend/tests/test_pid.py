import pytest

from app.filters import LowPassFilter, MovingAverageFilter, NoFilter
from app.pid import PIDController
from app.plant import FirstOrderPlant, SecondOrderPlant


def test_proportional_only_pushes_toward_setpoint():
    pid = PIDController(kp=1.0, ki=0.0, kd=0.0, setpoint=10.0)
    output = pid.step(measurement=0.0, dt=0.1)
    assert output == pytest.approx(10.0)


def test_zero_error_gives_zero_output():
    pid = PIDController(kp=2.0, ki=1.0, kd=1.0, setpoint=5.0)
    output = pid.step(measurement=5.0, dt=0.1)
    assert output == pytest.approx(0.0)


def test_output_is_clamped_to_limits():
    pid = PIDController(kp=100.0, ki=0.0, kd=0.0, setpoint=10.0, output_max=1.0)
    output = pid.step(measurement=0.0, dt=0.1)
    assert output == 1.0


def test_reset_clears_integral_and_derivative_state():
    pid = PIDController(kp=0.0, ki=1.0, kd=0.0, setpoint=1.0)
    pid.step(measurement=0.0, dt=1.0)
    pid.reset()
    assert pid._integral == 0.0
    assert pid._prev_error is None


def test_first_order_plant_settles_toward_gain_times_input():
    plant = FirstOrderPlant(gain=2.0, time_constant=1.0)
    for _ in range(2000):
        plant.step(u=1.0, dt=0.01)
    assert plant.value == pytest.approx(2.0, abs=0.05)


def test_second_order_plant_is_not_implemented_yet():
    plant = SecondOrderPlant()
    with pytest.raises(NotImplementedError):
        plant.step(u=1.0, dt=0.01)


def test_no_filter_passes_signal_through():
    f = NoFilter()
    assert f.apply(3.14) == 3.14


def test_moving_average_smooths_a_constant_signal():
    f = MovingAverageFilter(window_size=3)
    f.apply(1.0)
    f.apply(1.0)
    assert f.apply(1.0) == pytest.approx(1.0)


def test_low_pass_filter_is_not_implemented_yet():
    f = LowPassFilter(alpha=0.5)
    with pytest.raises(NotImplementedError):
        f.apply(1.0)
