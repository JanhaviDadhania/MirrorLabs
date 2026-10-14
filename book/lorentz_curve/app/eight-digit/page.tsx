"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { integrate, type State } from "@/lib/lorenz";

const DT = 0.005;
const T_MAX = 50;
const CELL = 1e-8; // width of one 8-decimal cell
const COLORS = ["#dc2626", "#7dd3fc", "#16a34a", "#000000", "#7c3aed"]; // red, light blue, green, black, purple
const LIVE = "#94a3b8";
const BG = "#ffffff";
const VALID = /^-?\d+(\.\d{1,8})?$/;
const BOX = { w: 1040, h: 840, scale: 17 };
const GAP = { w: 520, h: 200, logMin: -9, logMax: 1 };

type Run = {
  x: string; // the value typed when Run was pressed
  samples: State[];
};

type Commit = {
  id: number;
  color: string;
  x: string;
  t: number; // time at which this run was committed
  run: Run;
};

export default function EightDigitPage() {
  const [input, setInput] = useState("6.78954323");
  const [t, setT] = useState(0);
  const [run, setRun] = useState<Run | null>(null);
  const [commits, setCommits] = useState<Commit[]>([]);
  const [error, setError] = useState<string | null>(null);
  const nextId = useRef(1);
  const boxRef = useRef<HTMLCanvasElement>(null);
  const gapRef = useRef<HTMLCanvasElement>(null);

  // Commit is only allowed while the box shows a run made from the current x.
  const canCommit = run !== null && run.x === input.trim();

  function indexAt(time: number, samples: State[]) {
    return Math.min(Math.round(time / DT), samples.length - 1);
  }

  // Box: every committed trajectory up to its commit time, plus the live run.
  useEffect(() => {
    const canvas = boxRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx) return;
    const { w, h, scale } = BOX;
    const px = (x: number) => w / 2 + x * scale;
    const py = (z: number) => h - 20 - z * scale;

    ctx.fillStyle = BG;
    ctx.fillRect(0, 0, w, h);

    const drawTrail = (samples: State[], upTo: number, color: string) => {
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i <= upTo; i++) {
        const [x, , z] = samples[i];
        if (i === 0) ctx.moveTo(px(x), py(z));
        else ctx.lineTo(px(x), py(z));
      }
      ctx.stroke();
      const [hx, , hz] = samples[upTo];
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(px(hx), py(hz), 5, 0, Math.PI * 2);
      ctx.fill();
    };

    for (const c of commits) {
      drawTrail(c.run.samples, indexAt(c.t, c.run.samples), c.color);
    }
    if (run) drawTrail(run.samples, indexAt(t, run.samples), LIVE);
  }, [t, run, commits]);

  // Gap: log10 |x(t) − x_first(t)| for each commit, against the first commit.
  useEffect(() => {
    const canvas = gapRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx) return;
    const { w, h, logMin, logMax } = GAP;
    const padL = 36;
    const padB = 22;
    const plotW = w - padL - 8;
    const plotH = h - padB - 8;
    const px = (time: number) => padL + (time / T_MAX) * plotW;
    const py = (lg: number) => 8 + ((logMax - lg) / (logMax - logMin)) * plotH;

    ctx.fillStyle = BG;
    ctx.fillRect(0, 0, w, h);

    ctx.strokeStyle = "#00000018";
    ctx.fillStyle = "#475569";
    ctx.font = "11px monospace";
    for (let lg = logMin; lg <= logMax; lg += 2) {
      ctx.beginPath();
      ctx.moveTo(padL, py(lg));
      ctx.lineTo(w - 8, py(lg));
      ctx.stroke();
      ctx.fillText(`1e${lg}`, 2, py(lg) + 4);
    }
    for (let time = 0; time <= T_MAX; time += 10) {
      ctx.fillText(`${time}`, px(time) - 6, h - 6);
    }

    const ref = commits[0];
    if (!ref) return;
    for (const c of commits) {
      if (c.id === ref.id) continue;
      const last = indexAt(c.t, c.run.samples);
      ctx.strokeStyle = c.color;
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      let started = false;
      for (let i = 0; i <= last; i++) {
        const gap = Math.abs(c.run.samples[i][0] - ref.run.samples[i][0]);
        const lg = Math.max(logMin, Math.log10(Math.max(gap, 1e-300)));
        if (!started) {
          ctx.moveTo(px(i * DT), py(lg));
          started = true;
        } else {
          ctx.lineTo(px(i * DT), py(lg));
        }
      }
      ctx.stroke();
    }
  }, [commits]);

  function doRun() {
    const typed = input.trim();
    if (!VALID.test(typed)) {
      setError("Enter a number with at most 8 decimal places, for example 6.78954323.");
      return;
    }
    setError(null);
    // The machine keeps only 8 decimals. The true start is somewhere in the
    // cell [x, x + 10⁻⁸). A new point in that cell is drawn on every run.
    const hidden = Math.random() * CELL;
    const samples = integrate([Number(typed) + hidden, 1, 1], DT, Math.round(T_MAX / DT));
    setRun({ x: typed, samples });
    setT(0);
  }

  function commit() {
    if (!run) return;
    const id = nextId.current++;
    setCommits((prev) => [
      ...prev,
      {
        id,
        color: COLORS[(id - 1) % COLORS.length],
        x: run.x,
        t: Math.round(t / DT) * DT,
        run,
      },
    ]);
  }

  return (
    <main className="min-h-screen bg-[#070a12] text-slate-200 p-6 font-sans">
      <div className="max-w-[1100px] mx-auto flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold">The 8-digit machine</h1>
          <Link href="/" className="text-sm text-slate-400 hover:text-slate-200">
            Lorenz viewer →
          </Link>
        </div>

        <p className="text-sm text-slate-400 max-w-[560px]">
          This machine stores 8 decimal places. The x you type stands for a true value
          somewhere in a cell 0.00000001 wide, and the machine cannot tell where. Each run
          picks a point in that cell that you cannot see or set. Type the same x, choose
          the same t, and commit. Each commit is drawn in its own color on the same box.
        </p>

        <div className="flex flex-col gap-8">
          {/* Top: controls and the box */}
          <div className="flex flex-col gap-4 w-full">
            <label className="flex items-center gap-3 font-mono text-sm">
              <span className="w-12">x</span>
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                inputMode="decimal"
                className="flex-1 bg-slate-800 rounded px-3 py-1.5"
              />
              <button
                onClick={doRun}
                className="px-4 py-1.5 rounded bg-slate-800 hover:bg-slate-700"
              >
                Run
              </button>
            </label>
            {error && <p className="text-sm text-rose-400">{error}</p>}

            <canvas
              ref={boxRef}
              width={BOX.w}
              height={BOX.h}
              className="rounded-lg border border-slate-800 w-full"
            />

            <label className="flex items-center gap-3 font-mono text-sm">
              <span className="w-12">t</span>
              <input
                type="range"
                min={0}
                max={T_MAX}
                step={DT}
                value={t}
                disabled={!run}
                onChange={(e) => setT(Number(e.target.value))}
                className="flex-1"
              />
              <span className="w-16 text-right">{t.toFixed(2)}</span>
            </label>

            <div className="flex items-center gap-3">
              <button
                onClick={commit}
                disabled={!canCommit}
                className="px-4 py-1.5 rounded bg-amber-700 hover:bg-amber-600 disabled:opacity-40"
              >
                Commit
              </button>
              {run && !canCommit && (
                <span className="text-xs text-slate-500">
                  x changed since the last run. Press Run again.
                </span>
              )}
            </div>
          </div>

          {/* Bottom: legend of commits and the gap plot */}
          <div className="flex-1 w-full flex flex-col gap-4">
            <h2 className="text-sm font-mono text-slate-400">
              committed runs ({commits.length})
            </h2>
            {commits.length === 0 ? (
              <p className="text-sm text-slate-500">
                Nothing committed yet. Run, choose t, and commit.
              </p>
            ) : (
              <ul className="flex flex-col gap-1 font-mono text-sm">
                {commits.map((c, k) => (
                  <li key={c.id} className="flex items-center gap-3">
                    <span
                      className="inline-block w-3 h-3 rounded-full"
                      style={{ background: c.color }}
                    />
                    <span className="w-16">#{k + 1}</span>
                    <span className="w-36">x = {c.x}</span>
                    <span>t = {c.t.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            )}

            <div className="flex flex-col gap-2">
              <span className="text-sm font-mono text-slate-400">
                gap in x from commit #1, log scale
              </span>
              <canvas
                ref={gapRef}
                width={GAP.w}
                height={GAP.h}
                className="rounded-lg border border-slate-800 w-full"
              />
              <span className="text-xs text-slate-500">
                Each line is |x − x₁| for one commit. It starts near 10⁻⁸ and rises
                roughly as a straight line on this scale, which is exponential growth.
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
