import { memo } from "react";

/**
 * Renders the campus as a night-time blueprint (SVG) and overlays the live A* search state:
 * the search tree (parent -> child edges the algorithm has expanded), OPEN / CLOSED nodes and the final route.
 */
function CampusMap({ map, nodeIndex, source, destination, onSelect, allowJunctions, step, closedIds, openIds, route, searchTree }) {
  const { width, height, meters_per_unit: mpu = 0.5 } = map.meta;
  const pos = (id) => nodeIndex[id];
  const nodeOf = (ref) => (ref ? nodeIndex[map.locations.find((l) => l.id === ref)?.node ?? ref] : null);
  const src = nodeOf(source);
  const dst = nodeOf(destination);
  const routePoints = route.map((id) => `${pos(id).x},${pos(id).y}`).join(" ");
  const entranceExplored = (b) => closedIds.has(b.entrance);
  const role = (id) => (id && id === source ? "sel-src" : id && id === destination ? "sel-dst" : "");
  const scaleLen = 100;

  const activate = (e, id) => {
    if (e.type === "keydown" && e.key !== "Enter" && e.key !== " ") return;
    e.preventDefault();
    onSelect(id);
  };

  const isPath = (e) => e.kind === "shortcut";

  return (
    <svg className="map" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="Interactive campus map">
      <defs>
        <pattern id="grid-minor" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M25 0H0V25" className="grid-minor" /></pattern>
        <pattern id="grid-major" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" className="grid-major" /></pattern>
        <pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" className="hatch-line" /></pattern>
        <filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width={width} height={height}><feGaussianBlur stdDeviation="6" /></filter>
      </defs>

      <rect width={width} height={height} className="map-bg" />
      <rect width={width} height={height} fill="url(#grid-minor)" />
      <rect width={width} height={height} fill="url(#grid-major)" />

      {map.green_spaces.map((g) => (
        <g key={g.id}>
          <rect x={g.x} y={g.y} width={g.w} height={g.h} rx="14" className="lawn" />
          <rect x={g.x} y={g.y} width={g.w} height={g.h} rx="14" fill="url(#hatch)" />
          <rect x={g.x} y={g.y} width={g.w} height={g.h} rx="14" className="lawn-edge" />
          <text x={g.label_x} y={g.label_y} className="lawn-label" textAnchor="middle">{g.name}</text>
        </g>
      ))}

      {map.edges.map((e) => (
        <line key={`c${e.id}`} x1={pos(e.source).x} y1={pos(e.source).y} x2={pos(e.target).x} y2={pos(e.target).y}
          className={isPath(e) ? "path-under" : "road-casing"} />
      ))}
      {map.edges.map((e) => (
        <line key={`r${e.id}`} x1={pos(e.source).x} y1={pos(e.source).y} x2={pos(e.target).x} y2={pos(e.target).y}
          className={isPath(e) ? "path-line" : "road-fill"} />
      ))}
      {map.edges.filter((e) => !isPath(e)).map((e) => (
        <line key={`m${e.id}`} x1={pos(e.source).x} y1={pos(e.source).y} x2={pos(e.target).x} y2={pos(e.target).y} className="road-mid" />
      ))}

      {map.trees.map((t, i) => (
        <circle key={i} cx={t.x} cy={t.y} r={t.r} className="tree" />
      ))}

      {searchTree.map(([a, b]) =>
        pos(a) && pos(b) ? (
          <line key={`${a}>${b}`} x1={pos(a).x} y1={pos(a).y} x2={pos(b).x} y2={pos(b).y} className="search-edge" />
        ) : null
      )}

      {map.buildings.map((b) => (
        <g key={b.id} className={`building ${b.kind === "ground" ? "ground" : ""} ${entranceExplored(b) ? "explored" : ""} ${role(b.id)}`}
          role="button" tabIndex={0} aria-label={`${b.name}. ${b.description}`}
          onClick={(e) => activate(e, b.id)} onKeyDown={(e) => activate(e, b.id)}>
          <rect x={b.x} y={b.y} width={b.w} height={b.h} rx="5" className="building-shape" />
          {b.label_lines.map((line, i) => (
            <text key={i} x={b.x + b.w / 2} y={b.y + b.h / 2 + (i - (b.label_lines.length - 1) / 2) * 14 + 4}
              textAnchor="middle" className="building-label">{line}</text>
          ))}
        </g>
      ))}

      {map.nodes.filter((n) => n.type === "gate").map((n) => {
        const loc = map.locations.find((l) => l.node === n.id);
        return (
          <g key={n.id} className={`gate ${closedIds.has(n.id) ? "explored" : ""} ${loc ? role(loc.id) : ""}`}
            role="button" tabIndex={0} aria-label={n.name}
            onClick={(e) => activate(e, loc.id)} onKeyDown={(e) => activate(e, loc.id)}>
            <rect x={n.x - 23} y={n.y - 11} width="46" height="22" rx="11" className="gate-shape" />
            <text x={n.x} y={n.y + 4} textAnchor="middle" className="gate-label">{n.name.replace(" Gate", "")}</text>
          </g>
        );
      })}

      {map.nodes.filter((n) => n.type !== "gate").map((n) => {
        const state = n.id === step?.current ? "current" : closedIds.has(n.id) ? "closed" : openIds.has(n.id) ? "open" : "idle";
        const clickable = allowJunctions && n.type === "junction";
        return (
          <g key={n.id} className={`node ${n.type} ${state} ${clickable ? "clickable" : ""}`}
            onClick={clickable ? (e) => activate(e, n.id) : undefined}
            onKeyDown={clickable ? (e) => activate(e, n.id) : undefined}
            role={clickable ? "button" : undefined} tabIndex={clickable ? 0 : undefined}
            aria-label={clickable ? n.name : undefined}>
            {clickable && <circle cx={n.x} cy={n.y} r="14" className="hit" />}
            <circle cx={n.x} cy={n.y} r={n.type === "junction" ? 6 : 4} className="node-dot" />
            {state === "current" && <circle cx={n.x} cy={n.y} r="13" className="current-ring" />}
          </g>
        );
      })}

      {route.length > 1 && (
        <g key={routePoints} pointerEvents="none">
          <polyline points={routePoints} className="route-glow" filter="url(#glow)" />
          <polyline points={routePoints} className="route-casing" />
          <polyline points={routePoints} className="route-line" pathLength="1" />
          <polyline points={routePoints} className="route-flow" />
        </g>
      )}

      {[[src, "A", "marker-src"], [dst, "B", "marker-dst"]].map(([n, letter, cls]) =>
        n ? (
          <g key={cls} className={`marker ${cls}`} pointerEvents="none">
            <circle cx={n.x} cy={n.y} r="21" className="halo" />
            <circle cx={n.x} cy={n.y} r="13" className="pin" />
            <text x={n.x} y={n.y + 4.5} textAnchor="middle">{letter}</text>
          </g>
        ) : null
      )}

      <g className="scale" transform={`translate(24 ${height - 28})`} aria-hidden="true">
        <path d={`M0 0V7H${scaleLen}V0`} />
        <text x={scaleLen + 8} y="8">{Math.round(scaleLen * mpu)} m</text>
      </g>
    </svg>
  );
}

export default memo(CampusMap);
