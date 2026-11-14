export default function Sidebar({ map, source, destination, onChangeSource, onChangeDestination, onSwap, onFind, onReset,
  loading, canFind, allowJunctions, onToggleJunctions, result, error, nodeIndex }) {
  const junctions = map.nodes.filter((n) => n.type === "junction");
  const options = (selected) => (
    <>
      <option value="">Choose a place</option>
      <optgroup label="Buildings and gates">
        {map.locations.map((l) => <option key={l.id} value={l.id}>{l.name}</option>)}
      </optgroup>
      {(allowJunctions || junctions.some((j) => j.id === selected)) && (
        <optgroup label="Road junctions">
          {junctions.map((j) => <option key={j.id} value={j.id}>{j.name}</option>)}
        </optgroup>
      )}
    </>
  );

  const stops = result?.success ? result.route.map((id) => nodeIndex[id]).filter((n) => n.type !== "junction") : [];
  const hiddenJunctions = result?.success ? result.route.length - stops.length : 0;

  return (
    <aside className="sidebar" aria-label="Navigation">
      <section className="planner">
        <h2>Plan a route</h2>

        <div className="field">
          <label htmlFor="src"><span className="dot dot-src" />From</label>
          <select id="src" value={source ?? ""} onChange={(e) => onChangeSource(e.target.value || null)}>{options(source)}</select>
        </div>

        <button className="swap" onClick={onSwap} disabled={!source && !destination} aria-label="Swap source and destination">
          <svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M4 12V2M4 2L1.5 4.5M4 2l2.5 2.5M10 2v10M10 12l-2.5-2.5M10 12l2.5-2.5" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" /></svg>
          Swap places
        </button>

        <div className="field">
          <label htmlFor="dst"><span className="dot dot-dst" />To</label>
          <select id="dst" value={destination ?? ""} onChange={(e) => onChangeDestination(e.target.value || null)}>{options(destination)}</select>
        </div>

        <div className="actions">
          <button className="primary" onClick={onFind} disabled={!canFind || loading}>
            {loading ? "Searching…" : "Find route"}
          </button>
          <button className="ghost" onClick={onReset}>Reset</button>
        </div>

        <label className="check">
          <input type="checkbox" checked={allowJunctions} onChange={(e) => onToggleJunctions(e.target.checked)} />
          Allow picking road junctions on the map
        </label>

        <p className="hint">
          Click a building or gate on the map to set the start, then another for the destination. A third click starts a new route.
        </p>

        {error && <div className="notice error" role="alert">{error}</div>}
        {result && !result.success && <div className="notice warn" role="status">{result.message}</div>}
      </section>

      {result?.success && (
        <section className="route-info" aria-label="Route information">
          <h2>Route</h2>
          <p className="big num">{result.distance_m.toFixed(0)}<span className="unit"> m</span></p>
          <p className="muted small num">{result.total_cost.toFixed(1)} cost units</p>
          <ol className="stops">
            {stops.map((n, i) => (
              <li key={n.id} className={i === 0 ? "first" : i === stops.length - 1 ? "last" : ""}>
                {n.name.replace(" entrance", "")}
              </li>
            ))}
          </ol>
          <p className="muted small">Passes {hiddenJunctions} road junction{hiddenJunctions === 1 ? "" : "s"}.</p>
        </section>
      )}
    </aside>
  );
}
