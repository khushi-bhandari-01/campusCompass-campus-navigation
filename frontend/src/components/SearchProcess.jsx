import { useEffect, useRef } from "react";

const ACTION_TEXT = {
  added: "added to OPEN",
  improved: "cheaper path found, updated",
  reopened: "re-opened with a cheaper path",
  skipped_closed: "already closed, skipped",
  skipped_worse: "no better than known path, skipped",
};

export default function SearchProcess({ result, trace, index, done, nodeIndex }) {
  const listRef = useRef(null);
  const step = index >= 0 ? trace[index] : null;
  const name = (id) => (nodeIndex[id]?.name ?? id).replace(" entrance", "");

  useEffect(() => {
    const list = listRef.current;
    if (!list) return;
    if (index < 0) {
      list.scrollTop = 0;
      return;
    }
    const active = list.querySelector(".active");
    if (!active) return;

    // Scroll only within the list container, never scrolling the window or outer page
    const listRect = list.getBoundingClientRect();
    const activeRect = active.getBoundingClientRect();

    if (listRect.height === 0) return;

    if (activeRect.top < listRect.top + 4) {
      list.scrollTop -= (listRect.top + 4 - activeRect.top);
    } else if (activeRect.bottom > listRect.bottom - 4) {
      list.scrollTop += (activeRect.bottom - (listRect.bottom - 4));
    }
  }, [index]);

  if (!result) {
    return (
      <aside className="trace" aria-label="Search process">
        <header className="trace-head"><h2>Search process</h2></header>
        <p className="muted">Pick a start and a destination, then press Find route. Each step A* takes, and why, will appear here using f = g + h.</p>
      </aside>
    );
  }

  const shown = Math.max(index + 1, 0);
  const pct = trace.length ? (shown / trace.length) * 100 : 0;

  return (
    <aside className="trace" aria-label="Search process">
      <header className="trace-head">
        <h2>Search process</h2>
        <span className="counter num">Step {shown} of {trace.length}</span>
      </header>
      <div className="progress" aria-hidden="true"><i style={{ width: `${pct}%` }} /></div>

      {!step && <p className="muted">Press play, or step forward to expand the first node.</p>}

      {step && (
        <div className="step-card" aria-live="polite">
          <p className="step-title">
            {step.goal_reached ? "Goal reached" : "Expanding"}
            <strong>{name(step.current)}</strong>
          </p>
          <div className="eq" aria-label={`f equals g plus h: ${step.g.toFixed(1)} plus ${step.h.toFixed(1)} equals ${step.f.toFixed(1)}`}>
            <span className="term"><i>g</i><b className="num">{step.g.toFixed(1)}</b></span>
            <span className="op">+</span>
            <span className="term"><i>h</i><b className="num">{step.h.toFixed(1)}</b></span>
            <span className="op">=</span>
            <span className="term total"><i>f</i><b className="num">{step.f.toFixed(1)}</b></span>
          </div>
          <p className="muted small">
            {step.step === 1
              ? "The start node is the only node in OPEN."
              : step.goal_reached
                ? "The goal now has the lowest f in OPEN, so its path is optimal."
                : "Chosen because it had the lowest f in OPEN."}
            {" "}Parent: {step.parent ? name(step.parent) : "none"}. CLOSED size: {step.closed_count}.
          </p>

          {step.neighbors.length > 0 && (
            <>
              <h3>Neighbours checked</h3>
              <ul className="neigh">
                {step.neighbors.map((n) => (
                  <li key={n.id} className={n.action.startsWith("skipped") ? "skip" : "take"}>
                    <span className="n-name">{name(n.id)}</span>
                    <span className={`tag ${n.action}`}>{ACTION_TEXT[n.action]}</span>
                    <span className="num n-costs">g {n.g.toFixed(1)} · h {n.h.toFixed(1)} · f {n.f.toFixed(1)}</span>
                  </li>
                ))}
              </ul>
            </>
          )}

          <h3>OPEN list <span className="muted small">lowest f first</span></h3>
          {step.open.length === 0 ? <p className="muted small">Empty</p> : (
            <table className="open-table">
              <thead><tr><th>Node</th><th>g</th><th>h</th><th>f</th></tr></thead>
              <tbody>
                {step.open.slice(0, 6).map((o, i) => (
                  <tr key={o.id} className={i === 0 ? "next" : ""}>
                    <td>{name(o.id)}</td><td>{o.g.toFixed(1)}</td><td>{o.h.toFixed(1)}</td><td>{o.f.toFixed(1)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {step.open.length > 6 && <p className="muted small">+ {step.open.length - 6} more in OPEN</p>}
        </div>
      )}

      {done && result.success && (
        <p className="notice ok" role="status">Search finished: route highlighted on the map.</p>
      )}

      <h3>Expansion order</h3>
      <ol className="log" ref={listRef}>
        {trace.map((s, i) => (
          <li key={s.step} className={`${i === index ? "active" : ""} ${i > index ? "future" : ""}`}>
            {name(s.current)} <span className="num">f {s.f.toFixed(1)}</span>
          </li>
        ))}
      </ol>
    </aside>
  );
}
