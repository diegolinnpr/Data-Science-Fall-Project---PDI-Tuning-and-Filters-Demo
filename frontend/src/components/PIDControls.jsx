function Slider({ label, value, min, max, step, onChange, unit = "" }) {
  return (
    <label className="control-row">
      <span className="control-label">
        {label}
        <span className="control-value">
          {value}
          {unit}
        </span>
      </span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </label>
  );
}

export default function PIDControls({ params, onChange }) {
  const set = (key) => (value) => onChange({ ...params, [key]: value });

  return (
    <fieldset className="panel">
      <legend>PID gains</legend>
      <Slider label="Kp (proportional)" value={params.kp} min={0} max={10} step={0.1} onChange={set("kp")} />
      <Slider label="Ki (integral)" value={params.ki} min={0} max={5} step={0.05} onChange={set("ki")} />
      <Slider label="Kd (derivative)" value={params.kd} min={0} max={5} step={0.05} onChange={set("kd")} />
      <Slider label="Setpoint" value={params.setpoint} min={-10} max={10} step={0.5} onChange={set("setpoint")} />

      <label className="control-row">
        <span className="control-label">Plant</span>
        <select value={params.plant_type} onChange={(e) => set("plant_type")(e.target.value)}>
          <option value="first_order">First-order lag (e.g. heater, RC circuit)</option>
          <option value="second_order">Second-order (mass-spring-damper) — Week 1 issue</option>
        </select>
      </label>
    </fieldset>
  );
}
