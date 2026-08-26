/* Run the demo's script in node with a stubbed DOM: catches infinite loops,
   runaway growth and wiring errors without a browser. */
const fs = require("fs");
const html = fs.readFileSync(__dirname + "/nomodynamics.html", "utf8");
const js = html.slice(html.indexOf("<script>") + 8, html.lastIndexOf("</script>"));

const noop = () => {};
const ctxStub = new Proxy({}, {get: (t, k) => (k === "canvas" ? {} : noop)});
const mkEl = id => ({
  id, width: 880, height: 320, value: "4", textContent: "", innerHTML: "",
  classList: {toggle: noop, add: noop, remove: noop},
  addEventListener(ev, fn){ (this._h = this._h || {})[ev] = fn; },
  appendChild(c){ (this.children = this.children || []).push(c); },
  getContext: () => ctxStub, children: [],
});
const els = {};
const document = {
  getElementById: id => (els[id] = els[id] || mkEl(id)),
  createElement: () => mkEl("new"),
};
const window = {matchMedia: () => ({matches: false})};
let frames = 0, queue = null;
const requestAnimationFrame = fn => { queue = fn; };

const run = new Function("window", "document", "requestAnimationFrame", js + "\nreturn {GLIDERS, gw, hero, selectGlider, dwA, dwB};");
const api = run(window, document, requestAnimationFrame);

const t0 = Date.now();
const FRAMES = Number(process.argv[2] || 4000);
while (queue && frames < FRAMES) { const f = queue; queue = null; frames++; f(); }
const ms = Date.now() - t0;

let worst = 0;
for (const [, m] of api.gw.S) worst += (m.toString(2).match(/1/g) || []).length;
console.log(`ran ${frames} frames in ${ms} ms`);
console.log(`  glider widget: t=${api.gw.t}, laws=${worst}`);
console.log(`  masthead: t=${api.hero.t}`);
if (ms > 20000) { console.log("TOO SLOW"); process.exit(1); }

/* every preset, both resolutions, must stay bounded and finite */
for (let i = 0; i < api.GLIDERS.length; i++) {
  for (const mode of ["parity", "or"]) {
    api.selectGlider(i);
    api.gw.load(api.GLIDERS[i], mode);
    const s = Date.now();
    for (let k = 0; k < 400; k++) { api.gw.tick(); if (api.gw.gone()) api.gw.load(api.GLIDERS[i], mode); }
    let n = 0; for (const [, m] of api.gw.S) n += (m.toString(2).match(/1/g) || []).length;
    const dt = Date.now() - s;
    console.log(`  ${api.GLIDERS[i].name.padEnd(14)} ${mode.padEnd(6)} 400 steps in ${String(dt).padStart(5)} ms, ${n} laws`);
    if (dt > 5000) { console.log("  ^ TOO SLOW"); process.exit(1); }
  }
}
console.log("headless demo test passed");
