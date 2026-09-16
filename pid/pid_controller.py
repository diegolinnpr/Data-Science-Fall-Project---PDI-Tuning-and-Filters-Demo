"""Barebones PID controller skeleton -- see GitHub Issue #1.

Implement `PIDController.step()` so that, given the latest measurement
and the time elapsed since the last call, it returns a control output
using the classic PID equation:

    error(t)  = setpoint - measurement(t)
    output(t) = Kp * error(t) + Ki * integral(error) + Kd * d(error)/dt

- Kp (proportional) reacts to the current error.
- Ki (integral) reacts to the accumulated error over time.
- Kd (derivative) reacts to how fast the error is changing.

See the README for the full explanation of each term and links to learn
more. This file intentionally leaves the math unimplemented.
"""

from dataclasses import dataclass


@dataclass
class PIDController:
    kp: float
    ki: float
    kd: float
    setpoint: float

    def __post_init__(self) -> None:
        # TODO(Issue #1): you'll likely need state here to track the
        # accumulated error (for the integral term) and the previous
        # error (for the derivative term). Initialize it in reset().
        self.reset()

    def reset(self) -> None:
        """Clear any accumulated state, e.g. before starting a new run."""
        raise NotImplementedError("TODO(Issue #1): reset controller state")

    def step(self, measurement: float, dt: float) -> float:
        """Compute one control output from the latest measurement.

        Args:
            measurement: the current value of the thing being controlled.
            dt: seconds elapsed since the previous call to step().

        Returns:
            The control output to apply to the plant.
        """
        raise NotImplementedError("TODO(Issue #1): implement the PID equation")
