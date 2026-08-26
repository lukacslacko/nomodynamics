/* Differential test: demo/xengine.js against the Python reference xnomos.py.
 *
 *   python3 demo/gen_vectors.py > /tmp/xn_vectors.json && node demo/xengine.test.js
 *
 * Each vector is {const, mode, seed, trace}: the Python engine's state after
 * each of N steps, as a sorted list of [cellKey, mask].  Any divergence fails.
 */
const fs = require("fs");
const XN = require("./xengine.js");

const vecs = JSON.parse(fs.readFileSync("/tmp/xn_vectors.json", "utf8"));

function snapshot(S, dim) {
  const out = [];
  S.forEach((m, cell) => out.push([String(cell), m]));
  out.sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0));
  return out;
}

let fails = 0, steps = 0;
for (const v of vecs) {
  const C = v.const;
  let S = XN.seed(v.seed, C), ages = null;
  for (let t = 0; t < v.trace.length; t++) {
    const got = JSON.stringify(snapshot(S, C.dim));
    const want = JSON.stringify(v.trace[t]);
    if (got !== want) {
      fails++;
      if (fails <= 3) {
        console.log("DIVERGENCE", v.name, "mode", v.mode, "at step", t);
        console.log("  js  :", got.slice(0, 200));
        console.log("  py  :", want.slice(0, 200));
      }
      break;
    }
    steps++;
    if (v.sunset) { const r = XN.stepSunset(S, C, v.sunset, ages); S = r.S; ages = r.ages; }
    else S = XN.step(S, C, v.mode);
  }
}
console.log(
  `${vecs.length} vectors, ${steps} verified states, ${fails} divergences`
);
process.exit(fails ? 1 : 0);
