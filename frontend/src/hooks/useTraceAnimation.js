import { useCallback, useEffect, useState } from "react";

/**
 * Plays back the REAL search trace returned by the backend.
 * index = -1 means "nothing explored yet"; index = steps.length - 1 means the search has finished.
 */
export default function useTraceAnimation(steps, speed) {
  const total = steps.length;
  const [index, setIndex] = useState(-1);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    setIndex(-1);
    setPlaying(total > 0);
  }, [steps, total]);

  useEffect(() => {
    if (!playing) return undefined;
    if (index >= total - 1) {
      setPlaying(false);
      return undefined;
    }
    const timer = setTimeout(() => setIndex((i) => Math.min(i + 1, total - 1)), 750 / speed);
    return () => clearTimeout(timer);
  }, [playing, index, total, speed]);

  const play = useCallback(() => {
    if (total === 0) return;
    if (index >= total - 1) setIndex(-1);
    setPlaying(true);
  }, [index, total]);
  const pause = useCallback(() => setPlaying(false), []);
  const stepForward = useCallback(() => { setPlaying(false); setIndex((i) => Math.min(i + 1, total - 1)); }, [total]);
  const stepBack = useCallback(() => { setPlaying(false); setIndex((i) => Math.max(i - 1, -1)); }, []);
  const scrub = useCallback((i) => { setPlaying(false); setIndex(Math.max(-1, Math.min(i, total - 1))); }, [total]);
  const restart = useCallback(() => { setIndex(-1); setPlaying(total > 0); }, [total]);

  return { index, playing, total, done: total > 0 && index >= total - 1, play, pause, stepForward, stepBack, scrub, restart };
}
