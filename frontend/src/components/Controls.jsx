export default function Controls({ anim, speed, onSpeed }) {
  const disabled = anim.total === 0;
  const pct = anim.total ? ((anim.index + 1) / anim.total) * 100 : 0;
  return (
    <div className="controls" role="group" aria-label="Animation controls">
      <div className="btn-row">
        <button onClick={anim.restart} disabled={disabled} aria-label="Restart animation">Restart</button>
        <button onClick={anim.stepBack} disabled={disabled || anim.index < 0} aria-label="Previous step">Back</button>
        {anim.playing
          ? <button className="primary" onClick={anim.pause}>
              <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 1.5h2.5v9H2.5zM7 1.5h2.5v9H7z" fill="currentColor" /></svg>Pause
            </button>
          : <button className="primary" onClick={anim.play} disabled={disabled}>
              <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 1.2l8 4.8-8 4.8z" fill="currentColor" /></svg>{anim.done ? "Replay" : "Play"}
            </button>}
        <button onClick={anim.stepForward} disabled={disabled || anim.done} aria-label="Next step">Next</button>
      </div>
      <input type="range" min="-1" max={Math.max(anim.total - 1, 0)} value={anim.index} disabled={disabled}
        style={{ "--p": `${pct}%` }}
        onChange={(e) => anim.scrub(Number(e.target.value))} aria-label="Search progress" />
      <span className="counter num" aria-hidden="true">{Math.max(anim.index + 1, 0)}/{anim.total}</span>
      <label className="speed">Speed
        <select value={speed} onChange={(e) => onSpeed(Number(e.target.value))}>
          {[0.5, 1, 2, 4].map((s) => <option key={s} value={s}>{s}×</option>)}
        </select>
      </label>
    </div>
  );
}
