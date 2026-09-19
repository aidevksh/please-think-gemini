# -*- coding: utf-8 -*-
import os, json, math, itertools, statistics as st, random
from collections import defaultdict
import grade
LAB = os.path.dirname(os.path.abspath(__file__))
rows = grade.grade_all()
random.seed(7)

def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (round(100*max(0, c-h), 1), round(100*min(1, c+h), 1))

def boot_diff(a, b, n=20000):
    """P(mean(b) > mean(a)) by bootstrap, and 95% CI of the difference."""
    diffs = []
    for _ in range(n):
        ra = [random.choice(a) for _ in a]; rb = [random.choice(b) for _ in b]
        diffs.append(st.mean(rb) - st.mean(ra))
    diffs.sort()
    return dict(mean=round(100*(st.mean(b)-st.mean(a)), 1),
                lo=round(100*diffs[int(.025*n)], 1), hi=round(100*diffs[int(.975*n)], 1),
                p_better=round(sum(d > 0 for d in diffs)/n, 3))

CONDS = ["base", "v1", "v31"]; MODELS = ["gemini-3.8-flash-low", "gemini-3.8-flash-high"]
ORDER = ["math_opt","monty","subarray","bulbs","floors","go_race",
         "h_triples","h_josephus","h_seating","h_modexp","h_gobugs",
         "x_gridpaths","x_simgrind","x_permcount","x_knapsack","x_premise"]
import collections as _c
_cnt = _c.Counter(r["task"] for r in rows)
COMPLETE = {t for t, n in _cnt.items() if n == 30}
INCOMPLETE = {t: n for t, n in _cnt.items() if n != 30}
rows = [r for r in rows if r["task"] in COMPLETE]
present = {r["task"] for r in rows}
TASKS = [t for t in ORDER if t in present] + sorted(present - set(ORDER))
by = defaultdict(list)
for r in rows: by[(r["model"], r["cond"], r["task"])].append(r)

out = dict(n_runs=len(rows), incomplete=INCOMPLETE, conds=CONDS, models=MODELS, tasks=TASKS, cells={}, tasks_detail={}, pairs={})
for m in MODELS:
    for c in CONDS:
        rs = [r for t in TASKS for r in by[(m, c, t)]]
        ps = [1 if r["pass"] else 0 for r in rs]
        out["cells"][f"{m}|{c}"] = dict(
            n=len(rs), passes=sum(ps), pass_rate=round(100*st.mean(ps), 1) if rs else 0,
            ci=wilson(sum(ps), len(rs)),
            partial=round(100*st.mean([r["score"] for r in rs]), 1),
            latency=round(st.mean([r["latency"] for r in rs]), 1),
            chars=int(st.mean([r["chars"] for r in rs])),
            empty=sum(1 for r in rs if r["chars"] == 0))
    for a, b in [("base","v1"), ("base","v31"), ("v1","v31")]:
        A = [1 if r["pass"] else 0 for t in TASKS for r in by[(m,a,t)]]
        B = [1 if r["pass"] else 0 for t in TASKS for r in by[(m,b,t)]]
        out["pairs"][f"{m}|{a}->{b}"] = boot_diff(A, B)

for t in TASKS:
    d = {}
    for m in MODELS:
        for c in CONDS:
            rs = by[(m, c, t)]
            d[f"{m}|{c}"] = dict(n=len(rs), pass_rate=round(100*st.mean([r["pass"] for r in rs]), 1) if rs else None,
                                 partial=round(100*st.mean([r["score"] for r in rs]), 1) if rs else None,
                                 latency=round(st.mean([r["latency"] for r in rs]), 1) if rs else None)
    # which checks fail most, per condition (pooled over models)
    fails = defaultdict(lambda: defaultdict(int))
    for c in CONDS:
        for m in MODELS:
            for r in by[(m, c, t)]:
                for k, v in r["checks"].items():
                    if not v: fails[c][k] += 1
    d["fail_modes"] = {c: dict(fails[c]) for c in CONDS}
    out["tasks_detail"][t] = d

json.dump(out, open(os.path.join(LAB, "summary.json"), "w"), ensure_ascii=False, indent=1)
for k, v in out["cells"].items():
    print(f'{k:34s} pass={v["pass_rate"]:5.1f}% CI{v["ci"]} partial={v["partial"]:5.1f}% lat={v["latency"]:5.1f}s chars={v["chars"]:5d} empty={v["empty"]}')
print()
for k, v in out["pairs"].items(): print(f'{k:40s} Δ={v["mean"]:+5.1f}pp CI[{v["lo"]:+.1f},{v["hi"]:+.1f}] P(better)={v["p_better"]}')
print()
for t in TASKS:
    print(t, {k: v["pass_rate"] for k, v in out["tasks_detail"][t].items() if k != "fail_modes"})
