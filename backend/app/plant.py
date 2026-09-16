""""Plants" are the systems being controlled.

Each plant takes a control input `u` and advances its own state by one
timestep. The PID controller never sees the plant's internals -- only
the (possibly noisy, possibly filtered) measurement it reports back.
"""

from dataclasses import dataclass


@dataclass
class FirstOrderPlant:
    """A first-order lag, e.g. a heater warming a room or an RC circuit.

    dy/dt = (gain * u - y) / time_constant
    """

    gain: float = 1.0
    time_constant: float = 1.0
    value: float = 0.0

    def step(self, u: float, dt: float) -> float:
        dydt = (self.gain * u - self.value) / self.time_constant
        self.value += dydt * dt
        return self.value


@dataclass
class SecondOrderPlant:
    """A mass-spring-damper style system (placeholder for Week 1 Issue #5).

    Unlike FirstOrderPlant, this has inertia: it can overshoot and
    oscillate even with a perfect controller, which is what makes PID
    tuning on it more interesting.
    """

    mass: float = 1.0
    damping: float = 1.0
    stiffness: float = 1.0
    value: float = 0.0
    velocity: float = 0.0

    def step(self, u: float, dt: float) -> float:
        raise NotImplementedError(
            "SecondOrderPlant.step is not implemented yet -- see "
            "Week 1 Issue #5 in the README."
        )
