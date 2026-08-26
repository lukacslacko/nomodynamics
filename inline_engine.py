#!/usr/bin/env python3
"""Re-inline demo/xengine.js into the demo page between its markers.

The demo must be a single self-contained file, but the engine it runs is
differentially tested against the Python reference as a separate module.  This
keeps the two identical; `check_inline.py` enforces it in CI.
"""
import pathlib

here = pathlib.Path(__file__).resolve().parent
html_path = here / "demo" / "nomodynamics.html"
html = html_path.read_text()
eng = (here / "demo" / "xengine.js").read_text()
a = html.index("/* BEGIN xengine.js */") + len("/* BEGIN xengine.js */\n")
b = html.index("/* END xengine.js */")
html_path.write_text(html[:a] + eng + html[b:])
print("re-inlined %d bytes of engine into the demo" % len(eng))
