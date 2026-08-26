#!/usr/bin/env python3
"""Wrap the artifact-format demo fragment into a standalone page for GitHub Pages.

The demo in demo/ is authored as an artifact body (no <!doctype>/<html>/<head>);
the artifact host supplies the skeleton. This script supplies an equivalent
skeleton so docs/index.html renders identically when served statically.
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "demo" / "nomodynamics.html"
DST = HERE / "docs" / "index.html"

DESC = ("Nomodynamics: the mathematics of self-amending law. Live demo of "
        "nomic chains, ring rotors and the Jubilee Code.")

body = SRC.read_text()
m = re.search(r"<title>(.*?)</title>", body)
title = m.group(1) if m else "Nomodynamics"

DST.parent.mkdir(exist_ok=True)
DST.write_text(
    "<!doctype html>\n<html lang=\"en\">\n<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    f"<meta name=\"description\" content=\"{DESC}\">\n"
    f"<title>{title}</title>\n"
    "<link rel=\"icon\" href=\"data:image/svg+xml,"
    "%3Csvg xmlns='http%3A//www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Ctext y='.9em' font-size='90'%3E%F0%9F%93%9C%3C/text%3E%3C/svg%3E\">\n"
    "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
)
print(f"wrote {DST} ({DST.stat().st_size} bytes)")
