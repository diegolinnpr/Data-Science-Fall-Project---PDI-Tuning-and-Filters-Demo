import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

// Validated categorical palette slots (see the club's `dataviz` design notes).
const COLORS = {
  light: { filtered: "#2a78d6", raw: "#eb6834", grid: "#e1e0d9", axis: "#c3c2b7", muted: "#898781" },
  dark: { filtered: "#3987e5", raw: "#d95926", grid: "#2c2c2a", axis: "#383835", muted: "#898781" },
};

function usePalette() {
  const isDark =
    typeof window !== "undefined" &&
    window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  return isDark ? COLORS.dark : COLORS.light;
}

export default function ResponseChart({ data, showRaw }) {
  const c = usePalette();

  const rows = data.time.map((t, i) => ({
    time: t,
    setpoint: data.setpoint[i],
    filtered: data.filtered_measurement[i],
    raw: data.raw_measurement[i],
  }));

  return (
    <div className="panel chart-panel">
      <h2>System response</h2>
      <ResponsiveContainer width="100%" height={360}>
        <LineChart data={rows} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
          <CartesianGrid stroke={c.grid} vertical={false} />
          <XAxis
            dataKey="time"
            stroke={c.axis}
            tickFormatter={(t) => t.toFixed(1)}
            label={{ value: "time (s)", position: "insideBottom", offset: -4, fill: c.muted }}
          />
          <YAxis stroke={c.axis} tick={{ fill: c.muted }} />
          <Tooltip
            formatter={(value, name) => [Number(value).toFixed(3), name]}
            labelFormatter={(t) => `t = ${Number(t).toFixed(2)}s`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="setpoint"
            name="Setpoint"
            stroke={c.muted}
            strokeDasharray="4 4"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
          {showRaw && (
            <Line
              type="monotone"
              dataKey="raw"
              name="Raw measurement"
              stroke={c.raw}
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />
          )}
          <Line
            type="monotone"
            dataKey="filtered"
            name={showRaw ? "Filtered measurement" : "Measurement"}
            stroke={c.filtered}
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
