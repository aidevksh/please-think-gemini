# -*- coding: utf-8 -*-
"""Builds the validation report HTML from summary.json + graded.json."""
import os, json, io
LAB = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(LAB, "summary.json")))
G = json.load(open(os.path.join(LAB, "graded.json")))
NARR = json.load(open(os.path.join(LAB, "narrative.json")))
OUT = NARR["out_path"]

payload = json.dumps(dict(summary=S, runs=[{k: r[k] for k in
        ("task","cond","model","rep","latency","chars","score","pass")} for r in G],
        narr=NARR), ensure_ascii=False)

html = io.open(os.path.join(LAB, "report_template.html"), encoding="utf-8").read()
html = html.replace("/*__DATA__*/null", payload)
for k, v in NARR.items():
    if isinstance(v, str):
        html = html.replace("{{" + k + "}}", v)
io.open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, len(html), "bytes")
