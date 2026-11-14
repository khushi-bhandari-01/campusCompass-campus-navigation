import { useCallback, useEffect, useMemo, useState } from "react";
import { fetchMap, findRoute, resetSearch } from "../services/api.js";
import useTraceAnimation from "../hooks/useTraceAnimation.js";
import Sidebar from "../components/Sidebar.jsx";
import CampusMap from "../components/CampusMap.jsx";
import Controls from "../components/Controls.jsx";
import AnalyticsPanel from "../components/AnalyticsPanel.jsx";
import SearchProcess from "../components/SearchProcess.jsx";

const NO_TRACE = [];

export default function NavigatorPage() {
  const [map, setMap] = useState(null);
  const [loadError, setLoadError] = useState("");
  const [sel, setSel] = useState({ source: null, destination: null });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [speed, setSpeed] = useState(1);
  const [allowJunctions, setAllowJunctions] = useState(false);

  const loadMap = useCallback(() => {
    setLoadError("");
    fetchMap().then(setMap).catch((e) => setLoadError(e.message));
  }, []);
  useEffect(loadMap, [loadMap]);

  const nodeIndex = useMemo(() => (map ? Object.fromEntries(map.nodes.map((n) => [n.id, n])) : {}), [map]);
  const trace = result?.trace ?? NO_TRACE;
  const anim = useTraceAnimation(trace, speed);

  const clearResult = () => { setResult(null); setError(""); };

  const handleSelect = (id) => {
    clearResult();
    setSel((s) => {
      if (!s.source || (s.source && s.destination)) return { source: id, destination: null };
      return { ...s, destination: id };
    });
  };
  const setSource = (v) => { clearResult(); setSel((s) => ({ ...s, source: v })); };
  const setDestination = (v) => { clearResult(); setSel((s) => ({ ...s, destination: v })); };
  const swap = () => { clearResult(); setSel((s) => ({ source: s.destination, destination: s.source })); };

  const handleFind = async () => {
    setLoading(true); setError(""); setResult(null);
    try {
      setResult(await findRoute(sel.source, sel.destination));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSel({ source: null, destination: null });
    clearResult();
    resetSearch().catch(() => {}); // best effort: the API is stateless
  };

  const upto = anim.index;
  const closedIds = useMemo(() => new Set(trace.slice(0, upto + 1).map((s) => s.current)), [trace, upto]);
  const step = upto >= 0 ? trace[upto] : null;
  const openIds = useMemo(() => new Set(step ? step.open.map((o) => o.id) : []), [step]);
  const searchTree = useMemo(
    () => trace.slice(0, upto + 1).filter((s) => s.parent).map((s) => [s.parent, s.current]),
    [trace, upto]
  );
  const route = result?.success && anim.done ? result.route : [];

  if (loadError) {
    return (
      <main className="splash" role="alert">
        <h1>campusCompass</h1>
        <p>{loadError}</p>
        <button className="primary" onClick={loadMap}>Try again</button>
      </main>
    );
  }
  if (!map) return <main className="splash" role="status"><h1>campusCompass</h1><p>Loading campus map…</p></main>;

  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <svg className="logo" width="28" height="28" viewBox="0 0 32 32" aria-hidden="true">
            <rect x="1" y="1" width="30" height="30" rx="8" fill="#0c0c0d" stroke="#3a3a40" strokeWidth="1.5" />
            <path d="M8 23 L14 14 L19 18 L25 9" fill="none" stroke="#2f80ff" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
            <circle cx="8" cy="23" r="3.2" fill="#ffffff" stroke="#0c0c0d" strokeWidth="1.5" />
            <circle cx="25" cy="9" r="3.2" fill="#2f80ff" stroke="#ffffff" strokeWidth="1.5" />
          </svg>
          <h1>campusCompass</h1>
          <span className="tagline">Campus navigation</span>
        </div>
        <span className="badge" title="f(n) = g(n) + h(n)"><b>A*</b> search, f = g + h</span>
      </header>

      <div className="workspace">
        <Sidebar map={map} nodeIndex={nodeIndex} source={sel.source} destination={sel.destination}
          onChangeSource={setSource} onChangeDestination={setDestination} onSwap={swap}
          onFind={handleFind} onReset={handleReset} loading={loading} canFind={!!sel.source && !!sel.destination}
          allowJunctions={allowJunctions} onToggleJunctions={setAllowJunctions} result={result} error={error} />

        <main className="stage">
          <div className="map-wrap">
            <CampusMap map={map} nodeIndex={nodeIndex} source={sel.source} destination={sel.destination}
              onSelect={handleSelect} allowJunctions={allowJunctions} step={step} closedIds={closedIds}
              openIds={openIds} route={route} searchTree={searchTree} />
            {loading && <div className="map-loading" role="status">Running A* on the server…</div>}
          </div>
          <Controls anim={anim} speed={speed} onSpeed={setSpeed} />
          <ul className="legend" aria-label="Map legend">
            <li><i className="sw sw-src" />Start</li><li><i className="sw sw-dst" />Destination</li>
            <li><i className="sw sw-cur" />Current node</li><li><i className="sw sw-open" />In OPEN</li>
            <li><i className="sw sw-closed" />Explored (CLOSED)</li><li><i className="sw sw-tree" />Search tree</li>
            <li><i className="sw sw-route" />Final route</li>
          </ul>
          <AnalyticsPanel result={result} loading={loading} hasSelection={!!sel.source && !!sel.destination} />
        </main>

        <SearchProcess result={result} trace={trace} index={anim.index} done={anim.done} nodeIndex={nodeIndex} />
      </div>
    </div>
  );
}
