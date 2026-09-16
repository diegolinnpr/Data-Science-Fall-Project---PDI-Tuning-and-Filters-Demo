# PID Tuning & Filters Demo

A UCSB Data Science Club Fall quarter group project. We're using a classic
control-systems problem — **PID controller tuning** and **signal
filtering** — to learn the basics of control theory through code, before
optionally moving on to real hardware.

## Quarter roadmap

- **Week 0 (done):** this repo — a working simulator + interactive frontend
  so everyone can *see* what P, I, and D each do, and what noise/filtering
  does to a control loop, before writing any code of their own.
- **Week 1:** members pick up one of the [issues](#week-1-issues) below —
  each one is a real gap in the simulator (a missing filter, a classic PID
  bug, a missing chart) that you'll implement and open a PR for.
- **Later weeks:** depending on interest, we'll extend this to more plants
  (Week 1 Issue #4 is the first step), better tuning tools, and potentially
  move the same PID code onto real hardware (e.g. a motor or a
  temperature-controlled system on an Arduino/Raspberry Pi).

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
  what eliminates steady-state error — but push it too hard (or let it
  accumulate while the output is saturated) and you get overshoot and
  oscillation. That failure mode is called **integral windup**, and it's
  [Week 1 Issue #1](#week-1-issues).
- **Derivative (Kd):** reacts to *how fast* the error is changing, damping
  oscillation. It's also the most noise-sensitive term — an instant setpoint
  change or a single noisy sample can spike it. That's the **derivative
  kick** problem, [Week 1 Issue #2](#week-1-issues).

Tuning a PID controller means picking Kp, Ki, Kd so the response is fast,
doesn't overshoot too much, and settles without oscillating. Try it
yourself in the demo — that intuition is the whole point of Week 0.

## Why filters?

Real sensors are noisy. If you feed raw noisy measurements straight into a
PID controller, the derivative term amplifies that noise into a jittery,
erratic control output. Filters smooth the measurement *before* it reaches
the controller, at the cost of adding some lag (a filtered signal always
reacts a little slower than the raw one — that trade-off is the whole game
in filter design).

This demo ships with:

- **Moving average** — averages the last *N* samples. Simple and effective,
  but every sample in the window counts equally, so it's slow to react to
  real changes.
- **Low-pass filter (EMA)** — an exponentially-weighted average that reacts
  faster to recent samples. It's stubbed out as
  [Week 1 Issue #3](#week-1-issues) for you to implement.
- **Kalman filter** — the "proper" answer for combining a noisy sensor with
  a model of how the system should behave. It's out of scope for Week 0/1,
  but it's the natural next step if the group wants to go further — see
  [Learning resources](#learning-resources).

## Architecture

```
backend/   FastAPI + numpy — runs the PID/plant/filter simulation loop,
           exposes POST /api/simulate
frontend/  React + Vite + Recharts — sliders for Kp/Ki/Kd/noise/filter,
           calls the backend and plots setpoint vs. measurement live
```

The frontend re-runs the simulation (a fresh backend request) every time
you move a slider, so the chart always reflects the current parameters.

## Getting started

You'll need Python 3.11+ and Node 18+.

**Backend**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload   # http://127.0.0.1:8000
```

Run the tests with `pytest` from the `backend/` directory.

**Frontend** (in a second terminal)

```bash
cd frontend
npm install
npm run dev   # http://127.0.0.1:5173
```

Open the frontend URL, both servers need to be running at once.

## Week 1 issues

These are tracked as [GitHub Issues](../../issues) — comment on one to
claim it, then open a PR against `main` when it's ready. Good-first-issue
labels mark the ones that need the least control-theory background to
start with.

1. **Fix integral windup** in `backend/app/pid.py` (clamp/back-calculate
   the integral term when the output saturates).
2. **Fix derivative kick** in `backend/app/pid.py` (switch to
   derivative-on-measurement, or add setpoint weighting).
3. **Implement the low-pass (EMA) filter** in `backend/app/filters.py` —
   good first issue.
4. **Implement `SecondOrderPlant`** in `backend/app/plant.py` — a
   mass-spring-damper system with real inertia and overshoot.
5. **Add a control-effort chart** to the frontend showing `control_output`
   over time (already returned by the API, just not plotted yet) — good
   first issue, no control theory required.

Each issue on GitHub has more detail and acceptance criteria.

## Learning resources

- [PID controller — Wikipedia](https://en.wikipedia.org/wiki/PID_controller) —
  solid overview of the math and the classic failure modes.
- [Low-pass filter — Wikipedia](https://en.wikipedia.org/wiki/Low-pass_filter)
- [Moving average — Wikipedia](https://en.wikipedia.org/wiki/Moving_average)
- [Kalman filter — Wikipedia](https://en.wikipedia.org/wiki/Kalman_filter) —
  for when you want to go beyond simple filters.
- [Brian Douglas's control systems videos (YouTube search)](https://www.youtube.com/results?search_query=brian+douglas+control+systems+pid) —
  widely recommended, very visual explanations of PID and filtering.
- [Ziegler–Nichols method — Wikipedia](https://en.wikipedia.org/wiki/Ziegler%E2%80%93Nichols_method) —
  a classic recipe for picking starting gains instead of guessing.

## Contributing

1. Comment on the issue you want to work on so nobody doubles up.
2. Create a branch off `main`, make your change, and add/update tests in
   `backend/tests/` where relevant.
3. Open a PR — link the issue it closes and briefly describe what you
   changed and why.
4. Ask in the club channel if you get stuck — the point of Week 1 is to
   learn by doing this together, not to struggle alone.
