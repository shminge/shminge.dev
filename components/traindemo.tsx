import React, { useState, useEffect, useRef, useCallback } from "react";

export interface TrainProps {
  offset: number;
  nextPage: string;
}

const Train: React.FC<TrainProps> = ({ offset, nextPage }) => {
  const skyString = " ☁️   ☀️    ☁️      ";
  const trainBase = "   🌲    🌳     🌲  ";

  const [t, setT] = useState<number | null>(null);
  const [running, setRunning] = useState(false);
  const [redirectOnStop, setRedirectOnStop] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

const checkAndDelayStart = useCallback(() => {
  const now = Date.now();
  const tick = Math.floor(now / 200);
  const mod = tick % 44;

  const trainLength = trainBase.length + 1;
  const relativeT = mod - offset;

  if (relativeT >= 0 && relativeT < trainLength) {
    // We're in the active run window, so start immediately at t = relativeT
    setT(relativeT);
    setRunning(true);
  } else {
    // Not in window — delay until offset comes around again
    const stepsUntilOffset = (offset - mod + 44) % 44;
    const msUntilOffset = stepsUntilOffset * 200;

    timeoutRef.current = setTimeout(() => {
      setT(0);
      setRunning(true);
    }, msUntilOffset);
  }
}, [offset, trainBase.length]);


  useEffect(() => {
    checkAndDelayStart();
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [checkAndDelayStart]);

  useEffect(() => {
    if (!running) return;

    const interval = setInterval(() => {
      setT((prevT) => {
        if (prevT === null) return null;
        const nextT = prevT + 1;

        if (nextT > trainBase.length + 1) {
          setRunning(false);
          setT(null);
          if (redirectOnStop) {
            window.location.href = nextPage;
          } else {
            checkAndDelayStart(); // Schedule next run
          }
          return null;
        }

        return nextT;
      });
    }, 200);

    return () => clearInterval(interval);
  }, [running, trainBase.length, nextPage, redirectOnStop, checkAndDelayStart]);

  const handleClick = () => {
    if (running) {
      setRedirectOnStop(true);
    }
  };

  const trainStr = t !== null ? placeTrain(t, trainBase) : trainBase;

  return (
    <div onClick={handleClick} className="cursor-pointer select-none">
      <p
        className="whitespace-pre font-mono text-2xl leading-snug"
        style={{
          fontFamily: `"Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji", monospace`,
        }}
      >
        {skyString}
        {"\n"}
        <u>{trainStr}</u>
      </p>
    </div>
  );
};

function placeTrain(t: number, trainBase: string, trainLength: number = 4) {
  let chars = Array.from(trainBase);
  let trainIndex = chars.length - t;

  for (let j = 0; j < trainLength; j++) {
    let i = trainIndex - j + trainLength;
    if (i >= 0 && i < chars.length && !chars[i].trim()) {
      chars[i] = j === trainLength - 1 ? "🚂" : "🚃";
    }
  }

  return chars.join('');
}

export default Train;
