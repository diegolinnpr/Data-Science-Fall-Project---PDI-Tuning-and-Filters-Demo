"""Barebones "plant" skeleton -- see GitHub Issue #2.

A plant is the system being controlled. It takes a control input `u`
and reports back a new measurement after `dt` seconds. This starter
plant models something like a heater warming up a room, or an RC
circuit charging: a first-order lag.

    dy/dt = (gain * u - y) / time_constant

This file intentionally leaves the math unimplemented.
"""

from dataclasses import dataclass


@dataclass
class FirstOrderPlant:
    gain: float = 1.0
    time_constant: float = 1.0
    value: float = 0.0

    def step(self, u: float, dt: float) -> float:
        """Advance the plant by dt seconds given control input u.

        Returns the new value (the measurement a controller would see).
        """
        raise NotImplementedError(
            "TODO(Issue #2): implement the first-order lag equation"
        )
