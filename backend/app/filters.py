"""Signal filters applied to the (noisy) plant measurement before the
PID controller sees it.

Every filter implements `.apply(x) -> float`, called once per timestep
with the latest raw sample.
"""

from collections import deque
from dataclasses import dataclass, field


class NoFilter:
    """Passes the raw signal through unchanged -- the baseline to compare against."""

    def apply(self, x: float) -> float:
        return x


@dataclass
class MovingAverageFilter:
    """A simple windowed average (FIR filter).

    Smooths noise well but adds lag proportional to `window_size`, and
    every sample in the window is weighted equally -- a stale sample
    from `window_size` steps ago counts as much as the newest one.
    """

    window_size: int = 5
    _buffer: deque = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        self._buffer = deque(maxlen=self.window_size)

    def apply(self, x: float) -> float:
        self._buffer.append(x)
        return sum(self._buffer) / len(self._buffer)


@dataclass
class LowPassFilter:
    """Exponential moving average / RC low-pass filter (placeholder).

    y[n] = alpha * x[n] + (1 - alpha) * y[n-1]

    Unlike MovingAverageFilter, this weights recent samples more
    heavily and needs no buffer -- but it isn't implemented yet.
    See Week 1 Issue #3 in the README.
    """

    alpha: float = 0.2

    def apply(self, x: float) -> float:
        raise NotImplementedError(
            "LowPassFilter.apply is not implemented yet -- see "
            "Week 1 Issue #3 in the README."
        )


FILTERS = {
    "none": NoFilter,
    "moving_average": MovingAverageFilter,
    "low_pass": LowPassFilter,
}
