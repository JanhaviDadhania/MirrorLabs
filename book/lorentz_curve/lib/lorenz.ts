// Lorenz system: x' = σ(y − x), y' = x(ρ − z) − y, z' = xy − βz
export const SIGMA = 10;
export const RHO = 28;
export const BETA = 8 / 3;

export type State = [number, number, number];

export function derivative([x, y, z]: State): State {
  return [SIGMA * (y - x), x * (RHO - z) - y, x * y - BETA * z];
}

// Classical fourth-order Runge–Kutta step.
function rk4(s: State, h: number): State {
  const add = (a: State, b: State, k: number): State => [
    a[0] + k * b[0],
    a[1] + k * b[1],
    a[2] + k * b[2],
  ];
  const k1 = derivative(s);
  const k2 = derivative(add(s, k1, h / 2));
  const k3 = derivative(add(s, k2, h / 2));
  const k4 = derivative(add(s, k3, h));
  return [
    s[0] + (h / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
    s[1] + (h / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]),
    s[2] + (h / 6) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]),
  ];
}

// Returns samples[i] = state at time i * dt, for i = 0..steps.
export function integrate(s0: State, dt: number, steps: number): State[] {
  const out: State[] = [s0];
  let s = s0;
  for (let i = 0; i < steps; i++) {
    s = rk4(s, dt);
    out.push(s);
  }
  return out;
}
