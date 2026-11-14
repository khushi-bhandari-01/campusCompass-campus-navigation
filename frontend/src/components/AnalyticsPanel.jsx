const fmt = (v, d = 0) => (v === null || v === undefined ? "–" : Number(v).toFixed(d));

export default function AnalyticsPanel({ result, loading, hasSelection }) {
  const m = result?.metrics;
  let status = "Waiting for a start and destination";
  let tone = "idle";
  if (hasSelection) { status = "Ready to search"; tone = "ready"; }
  if (loading) { status = "Searching…"; tone = "busy"; }
  if (result) { status = result.success ? "Optimal route found" : "No route exists"; tone = result.success ? "ok" : "bad"; }

  const cells = [
    ["Route distance", result?.success ? `${fmt(result.distance_m)} m` : "–"],
    ["Nodes explored", fmt(m?.nodes_explored)],
    ["Nodes in route", result?.success ? fmt(m?.path_nodes) : "–"],
    ["Execution time", m ? `${fmt(m.execution_time_ms, 3)} ms` : "–"],
    ["Nodes generated", fmt(m?.nodes_generated)],
    ["Heap pushes", fmt(m?.heap_pushes)],
  ];

  return (
    <section className="metrics" aria-label="Analytics">
      <div className={`status-cell ${tone}`} role="status"><i className="led" />{status}</div>
      <dl className="cells">
        {cells.map(([k, v]) => (
          <div key={k}><dt>{k}</dt><dd className="num">{v}</dd></div>
        ))}
      </dl>
      {m && (
        <p className="note">
          Time measures the search alone (no animation trace). Stale heap entries skipped: {m.stale_pops}. Nodes re-opened: {m.reopened}.
        </p>
      )}
    </section>
  );
}
