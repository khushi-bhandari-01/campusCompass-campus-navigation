// All backend communication lives here. The route and the search trace ALWAYS come from the Python API.
const BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

async function request(path, options = {}) {
  let res;
  try {
    res = await fetch(`${BASE}${path}`, { headers: { "Content-Type": "application/json" }, ...options });
  } catch {
    throw new Error(
      BASE
        ? "Cannot reach the PATHFINDER backend. If it is hosted on a free plan it may be waking up; wait a minute and retry."
        : "Cannot reach the PATHFINDER backend. Start it with 'uvicorn main:app --reload' in the backend folder."
    );
  }
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (body.detail) detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    } catch { /* ignore non-JSON error bodies */ }
    throw new Error(detail);
  }
  return res.json();
}

export const fetchMap = () => request("/api/map");
export const findRoute = (source, destination) =>
  request("/api/find-route", { method: "POST", body: JSON.stringify({ source, destination }) });
export const resetSearch = () => request("/api/reset", { method: "POST" });
