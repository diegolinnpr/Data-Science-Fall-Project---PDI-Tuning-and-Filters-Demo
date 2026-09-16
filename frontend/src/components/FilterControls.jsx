export default function FilterControls({ params, onChange }) {
  const setParam = (key) => (value) => onChange({ ...params, [key]: value });
  const setFilterParam = (key) => (value) =>
    onChange({ ...params, filter_params: { ...params.filter_params, [key]: value } });

  return (
    <fieldset className="panel">
      <legend>Sensor noise &amp; filtering</legend>

      <label className="control-row">
        <span className="control-label">
          Sensor noise (std dev)
          <span className="control-value">{params.noise_std}</span>
        </span>
        <input
          type="range"
          min={0}
          max={2}
          step={0.05}
          value={params.noise_std}
          onChange={(e) => setParam("noise_std")(Number(e.target.value))}
        />
      </label>

      <label className="control-row">
        <span className="control-label">Filter</span>
        <select value={params.filter_type} onChange={(e) => setParam("filter_type")(e.target.value)}>
          <option value="none">None (raw signal)</option>
          <option value="moving_average">Moving average</option>
          <option value="low_pass">Low-pass (EMA) — Week 1 issue</option>
        </select>
      </label>

      {params.filter_type === "moving_average" && (
        <label className="control-row">
          <span className="control-label">
            Window size
            <span className="control-value">{params.filter_params.window_size ?? 5}</span>
          </span>
          <input
            type="range"
            min={1}
            max={50}
            step={1}
            value={params.filter_params.window_size ?? 5}
            onChange={(e) => setFilterParam("window_size")(Number(e.target.value))}
          />
        </label>
      )}

      {params.filter_type === "low_pass" && (
        <label className="control-row">
          <span className="control-label">
            Alpha
            <span className="control-value">{params.filter_params.alpha ?? 0.2}</span>
          </span>
          <input
            type="range"
            min={0.01}
            max={1}
            step={0.01}
            value={params.filter_params.alpha ?? 0.2}
            onChange={(e) => setFilterParam("alpha")(Number(e.target.value))}
          />
        </label>
      )}
    </fieldset>
  );
}
