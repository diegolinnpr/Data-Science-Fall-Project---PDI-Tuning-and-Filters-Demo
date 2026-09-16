# PID Tuning & Filters Demo

A UCSB Data Science Club Fall quarter group project. We're using a classic
control-systems problem — **PID controller tuning** — to learn the basics
of control theory through code. Filtering and a custom frontend to
visualize everything will come in later phases; this first phase is just
the core control logic, in plain Python.

## What's here

Three skeleton files with the math left unimplemented on purpose — filling
them in is the group's first three issues:

```
pid/
  pid_controller.py   PIDController skeleton      -> Issue #1
  plant.py             FirstOrderPlant skeleton     -> Issue #2
  demo.py               simulation loop skeleton     -> Issue #3
tests/
  test_pid_controller.py   tests to check your work against
```

## What is a PID controller?

A PID controller is a feedback loop that tries to drive a **measurement**
toward a **setpoint** by continuously computing a **control output** from
the error between them:

```
error(t) = setpoint − measurement(t)

output(t) = Kp·error(t)  +  Ki·∫error dt  +  Kd·(d error/dt)
             \_________/     \___________/     \____________/
             Proportional        Integral          Derivative
```

- **Proportional (Kp):** reacts to the *current* error. Bigger error →
  bigger push. Alone, it always leaves some steady-state error (it stops
  pushing once the error gets small, before it's actually zero).
- **Integral (Ki):** reacts to the *accumulated* error over time. This is
  what eliminates steady-state error, at the risk of overshoot if pushed
  too hard.
- **Derivative (Kd):** reacts to *how fast* the error is changing, damping
  oscillation.

Tuning a PID controller means picking Kp, Ki, Kd so the response is fast,
doesn't overshoot too much, and settles without oscillating.

A "plant" is just the system being controlled — in `plant.py`, a
first-order lag, which behaves like a heater warming a room or an RC
circuit charging: `dy/dt = (gain * u - y) / time_constant`.

## Getting started

You'll need Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest   # everything fails until Issues #1 and #2 are implemented
```

Once `pytest` passes, run the demo (after Issue #3 is done too):

```bash
python -m pid.demo
```

You should see the plant's value climb toward the setpoint over time.

## Issues

1. **Implement `PIDController`** (`pid/pid_controller.py`) — the P, I, D
   terms and the reset logic.
2. **Implement `FirstOrderPlant`** (`pid/plant.py`) — the lag equation
   that advances the plant by one timestep.
3. **Wire up the simulation loop** (`pid/demo.py`) — connect the
   controller and plant and print the response over time.

Claim an issue by assigning yourself, branch off `main`, and open a PR
when `pytest` passes.

## Learning resources

- [PID controller — Wikipedia](https://en.wikipedia.org/wiki/PID_controller) —
  overview of the math and classic failure modes (integral windup,
  derivative kick).
- [Ziegler–Nichols method — Wikipedia](https://en.wikipedia.org/wiki/Ziegler%E2%80%93Nichols_method) —
  a classic recipe for picking starting gains instead of guessing.
- [Brian Douglas's control systems videos (YouTube search)](https://www.youtube.com/results?search_query=brian+douglas+control+systems+pid) —
  widely recommended, very visual explanations of PID control.

## Roadmap

Once the core PID loop works: sensor noise + filters (moving average,
low-pass, maybe Kalman), a custom frontend to visualize tuning live, and
possibly a move to real hardware depending on interest.
