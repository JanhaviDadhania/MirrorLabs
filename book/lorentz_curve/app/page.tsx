"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { integrate, type State } from "@/lib/lorenz";

const DT = 0.005;
const T_MAX = 50;
const START: State = [1, 1, 1];
const TRAIL = 4; // time units of trail shown behind the point
const SCALE = 11; // pixels per unit
const SIZE = 560;

export default function Page() {
  const samples = useMemo(
    () => integrate(START, DT, Math.round(T_MAX / DT)),
    [],
  );

  const [t, setT] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Advance t while playing; loop back to 0 at the end.
  useEffect(() => {
    if (!playing) return;
    let frame = 0;
    let last = performance.now();
    const tick = (now: number) => {
      const elapsed = (now - last) / 1000;
      last = now;
      setT((prev) => (prev + elapsed * speed >= T_MAX ? 0 : prev + elapsed * speed));
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [playing, speed]);

  // Draw the trail and head at the current t.
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx) return;

    const index = Math.min(Math.round(t / DT), samples.length - 1);
    const from = Math.max(0, index - Math.round(TRAIL / DT));
    const angle = t * 0.25; // slow rotation so the 3D shape is visible

    // Project (x, y, z) to the screen: rotate about the z-axis, centre z at 25.
    const project = ([x, y, z]: State): [number, number] => {
      const cx = x * Math.cos(angle) - y * Math.sin(angle);
      const cy = z - 25;
      return [SIZE / 2 + SCALE * cx, SIZE / 2 - SCALE * cy];
    };

    ctx.fillStyle = "#0b0f1a";
    ctx.fillRect(0, 0, SIZE, SIZE);

    ctx.lineWidth = 1.5;
    for (let i = from; i < index; i++) {
      const alpha = (i - from) / Math.max(1, index - from);
      ctx.strokeStyle = `rgba(255, 170, 80, ${alpha})`;
      const [x1, y1] = project(samples[i]);
      const [x2, y2] = project(samples[i + 1]);
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    }

    const [hx, hy] = project(samples[index]);
    ctx.fillStyle = "#ffd27a";
    ctx.beginPath();
    ctx.arc(hx, hy, 4, 0, Math.PI * 2);
    ctx.fill();
  }, [t, samples]);

  const state = samples[Math.min(Math.round(t / DT), samples.length - 1)];

  return (
    <main className="min-h-screen bg-[#070a12] text-slate-200 flex flex-col items-center gap-5 p-6 font-sans">
      <h1 className="text-xl font-semibold">Lorenz system</h1>
      <p className="text-sm text-slate-400 font-mono">
        x′ = σ(y − x) &nbsp; y′ = x(ρ − z) − y &nbsp; z′ = xy − βz &nbsp; (σ=10, ρ=28, β=8/3)
      </p>

      <canvas
        ref={canvasRef}
        width={SIZE}
        height={SIZE}
        className="rounded-lg border border-slate-800 max-w-full"
      />

      <div className="w-full max-w-[560px] flex flex-col gap-3">
        <label className="flex items-center gap-3 font-mono text-sm">
          <span className="w-10">t</span>
          <input
            type="range"
            min={0}
            max={T_MAX}
            step={DT}
            value={t}
            onChange={(e) => {
              setPlaying(false);
              setT(Number(e.target.value));
            }}
            className="flex-1"
          />
          <span className="w-16 text-right">{t.toFixed(2)}</span>
        </label>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setPlaying((p) => !p)}
            className="px-4 py-1.5 rounded bg-slate-800 hover:bg-slate-700"
          >
            {playing ? "Pause" : "Play"}
          </button>
          <label className="flex items-center gap-2 text-sm">
            speed
            <select
              value={speed}
              onChange={(e) => setSpeed(Number(e.target.value))}
              className="bg-slate-800 rounded px-2 py-1"
            >
              {[0.25, 0.5, 1, 2, 4].map((s) => (
                <option key={s} value={s}>
                  {s}×
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="font-mono text-sm text-slate-400">
          x = {state[0].toFixed(3)} &nbsp; y = {state[1].toFixed(3)} &nbsp; z ={" "}
          {state[2].toFixed(3)}
        </div>
      </div>
    </main>
  );
}
