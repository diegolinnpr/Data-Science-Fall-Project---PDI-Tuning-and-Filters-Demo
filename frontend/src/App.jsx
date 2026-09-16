import { useEffect, useRef, useState } from "react";
import { simulate } from "./api";
import FilterControls from "./components/FilterControls.jsx";
import PIDControls from "./components/PIDControls.jsx";
import ResponseChart from "./components/ResponseChart.jsx";

const DEFAULT_PARAMS = {
  kp: 2,
  ki: 0.5,
  kd: 0.1,
  setpoint: 5,
  plant_type: "first_order",
  filter_type: "none",
  filter_params: {},
  duration: 10,
  dt: 0.02,
  noise_std: 0,
};

export default function App() {
  const [params, setParams] = useState(DEFAULT_PARAMS);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const debounceRef = useRef(null);

  useEffect(() => {
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(async () => {
      try {
        const result = await simulate(params);
        setData(result);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    }, 150);
    return () => clearTimeout(debounceRef.current);
  }, [params]);

  const showRaw = params.noise_std > 0 || params.filter_type !== "none";

  return (
    <div className="app">
      <header className="app-header">
        <h1>PID Tuning &amp; Filters Demo</h1>
        <p>
          Adjust the gains, add sensor noise, and try different filters to see how a PID
          controller responds. Backend: FastAPI simulation • Frontend: React + Recharts.
        </p>
      </header>

      <div className="app-body">
        <div className="controls">
          <PIDControls params={params} onChange={setParams} />
          <FilterControls params={params} onChange={setParams} />
        </div>

        <div className="results">
          {error && (
            <div className="panel error-banner">
              <strong>Simulation error:</strong> {error}
              <p>
                If this mentions a feature that "isn't implemented yet", that's expected —
                it's one of the Week 1 issues. Pick another option or go fix it!
              </p>
            </div>
          )}
          {data && <ResponseChart data={data} showRaw={showRaw} />}
        </div>
      </div>
    </div>
  );
}
