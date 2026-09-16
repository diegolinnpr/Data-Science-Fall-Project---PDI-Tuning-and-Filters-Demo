const API_BASE = "http://127.0.0.1:8000";

export async function simulate(params) {
  const res = await fetch(`${API_BASE}/api/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Simulation request failed (${res.status})`);
  }

  return res.json();
}
