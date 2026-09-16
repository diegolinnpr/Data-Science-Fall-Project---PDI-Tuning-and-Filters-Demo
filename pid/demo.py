"""Wires a PIDController up to a FirstOrderPlant and runs it -- see
GitHub Issue #3.

Once Issues #1 and #2 are done, this is where it comes together: run
this script and you should see the plant's value climb toward the
setpoint over time.

This file intentionally leaves the simulation loop unimplemented.
"""

from pid.pid_controller import PIDController
from pid.plant import FirstOrderPlant


def run(steps: int = 200, dt: float = 0.05) -> None:
    pid = PIDController(kp=1.0, ki=0.0, kd=0.0, setpoint=5.0)
    plant = FirstOrderPlant()

    # TODO(Issue #3): loop `steps` times. On each iteration:
    #   1. Read plant.value as the current measurement.
    #   2. Call pid.step(measurement, dt) to get a control output.
    #   3. Call plant.step(output, dt) to advance the plant.
    #   4. Print the elapsed time and plant.value so you can watch the
    #      system respond, e.g.: print(f"t={i * dt:.2f}  y={plant.value:.3f}")
    raise NotImplementedError("TODO(Issue #3): implement the simulation loop")


if __name__ == "__main__":
    run()
