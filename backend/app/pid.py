"""A minimal, from-scratch PID controller.

This is intentionally the simplest correct implementation, not a
production-grade one (see the "Known limitations" in the README's
Week 1 issue list for what's missing and why it matters).
"""

from dataclasses import dataclass


@dataclass
class PIDController:
    kp: float
    ki: float
    kd: float
    setpoint: float
    output_min: float | None = None
    output_max: float | None = None

    def __post_init__(self) -> None:
        self._integral = 0.0
        self._prev_error: float | None = None

    def reset(self) -> None:
        """Clear accumulated state, e.g. before starting a new run."""
        self._integral = 0.0
        self._prev_error = None

    def step(self, measurement: float, dt: float) -> float:
        """Compute one control output from the latest measurement.

        error(t) = setpoint - measurement(t)
        output(t) = Kp*error(t) + Ki*integral(error) + Kd*d(error)/dt
        """
        error = self.setpoint - measurement

        p_term = self.kp * error

        # NOTE: this integral term accumulates without bound. If the
        # output saturates at output_min/output_max, the integral keeps
        # growing anyway ("integral windup"), causing overshoot once the
        # error changes sign. Fixing this is Week 1 Issue #1.
        self._integral += error * dt
        i_term = self.ki * self._integral

        # NOTE: derivative-on-error. A step change in setpoint causes an
        # instantaneous spike in `error`, which spikes the derivative term
        # too ("derivative kick"). Fixing this is Week 1 Issue #2.
        if self._prev_error is None:
            derivative = 0.0
        else:
            derivative = (error - self._prev_error) / dt
        d_term = self.kd * derivative

        output = p_term + i_term + d_term

        if self.output_min is not None:
            output = max(self.output_min, output)
        if self.output_max is not None:
            output = min(self.output_max, output)

        self._prev_error = error
        return output
