#!/usr/bin/env python3
"""Assert that the engine inlined in the demo is demo/xengine.js verbatim."""
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
html = (here / "demo" / "nomodynamics.html").read_text()
eng = (here / "demo" / "xengine.js").read_text()
a = html.index("/* BEGIN xengine.js */") + len("/* BEGIN xengine.js */\n")
b = html.index("/* END xengine.js */")
ok = html[a:b] == eng
print("inlined engine matches demo/xengine.js:", ok)
sys.exit(0 if ok else 1)
