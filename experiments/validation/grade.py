# -*- coding: utf-8 -*-
import os, re, json, glob, sys, statistics as st
LAB = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(LAB, "raw")

def answer_line(out):
    hits = re.findall(r'ANSWER\s*:(.*)', out)
    return hits[-1].strip() if hits else ""

def norm(s): return re.sub(r'[\s`*_-]', '', s).lower()
def pts(s):  return set(re.findall(r'\(\s*-?[\d./√s q]*?\s*,', '')) # unused

def coords(s):
    return set(tuple(x.strip() for x in m.split(',')) for m in re.findall(r'\(([^()]*)\)', s))

def num(s):
    m = re.search(r'-?\d+(?:\.\d+)?', s); return m.group(0) if m else None

def frac_eq(s, a, b):
    s = norm(s)
    if f"{a}/{b}" in s: return True
    try: return abs(float(s) - a/b) < 0.01
    except: return False

def g_math(out):
    a = answer_line(out); c = {}
    mx = re.search(r'max\s*=\s*([^@;]*)@([^;]*)', a, re.I)
    mn = re.search(r'min\s*=\s*([^@;]*)@(.*)', a, re.I)
    c["max=16"] = bool(mx) and num(mx.group(1)) == "16"
    c["max@(4,1,0)"] = bool(mx) and ('4','1','0') in coords(mx.group(2))
    c["min=0"] = bool(mn) and num(mn.group(1)) == "0"
    cs = coords(mn.group(2)) if mn else set()
    c["min@(6,0,0)+(0,3,0)"] = ('6','0','0') in cs and ('0','3','0') in cs
    return c

def g_monty(out):
    a = answer_line(out)
    sw = re.search(r'switch\s*=\s*([^,;]*)', a, re.I); sy = re.search(r'stay\s*=\s*([^,;]*)', a, re.I)
    return {"switch=2/3": bool(sw) and frac_eq(sw.group(1), 2, 3),
            "stay=1/3":  bool(sy) and frac_eq(sy.group(1), 1, 3)}

def g_sub(out):
    return {"count=9": num(answer_line(out)) == "9"}

def g_bulbs(out):
    a = answer_line(out)
    nums = set(re.findall(r'\d+', a.split('count')[0]))
    cnt = re.search(r'count\s*=\s*(\d+)', a, re.I)
    return {"set={1,16,36,64,81,100}": nums == {"1","16","36","64","81","100"},
            "count=6": bool(cnt) and cnt.group(1) == "6"}

def g_floors(out):
    a = answer_line(out); s = norm(a)
    n = re.search(r'solutions\s*=\s*(\d+)', a, re.I)
    A = "blake|dana|evan|casey|alex"; B = "blake|dana|alex|casey|evan"
    return {"solutions=2": bool(n) and n.group(1) == "2",
            "arrangement_A": A in s, "arrangement_B": B in s}

def g_go(out):
    a = norm(answer_line(out)); full = norm(out)
    bug = any(k in a for k in ["check-then-act","checkthenact","stampede","thunderingherd",
                               "중복실행","redundant","duplicate","toctou","race",
                               "double-checked","doublechecked","doublecheck","이중점검","재확인"])
    fix = any(k in a for k in ["double-checked","doublechecked","doublecheck","singleflight","이중점검"])
    code = ("singleflight" in full) or bool(re.search(r'c?\.?lock\(\).{0,400}?(exists|ok)', full))
    return {"bug_identified": bug, "fix_named": fix, "fix_in_code": code}


def g_triples(out): return {"count=306": num(answer_line(out)) == "306"}
def g_josephus(out): return {"survivor=5": num(answer_line(out)) == "5"}
def g_modexp(out):
    a = answer_line(out); m = re.search(r'\d+', a)
    return {"rem=807": bool(m) and int(m.group(0)) == 807}
def g_seating(out):
    a = answer_line(out); m = re.search(r'count\s*=\s*(\d+)', a, re.I) or re.search(r'(\d+)', a)
    return {"count=8": bool(m) and m.group(1) == "8"}
def g_gobugs(out):
    """Graded on the model's own final defect list (ANSWER line): did it name all three?"""
    a = norm(answer_line(out))
    bugs = a.split("fix=")[0]
    fix  = a.split("fix=")[1] if "fix=" in a else a
    return {"map_race":    "map" in bugs or "맵" in bugs,
            "wg_add_race": ("wg.add" in bugs or "waitgroup" in bugs or "add(1)" in bugs),
            "idx_race":    ("idx" in bugs or "index" in bugs or "인덱스" in bugs),
            "fix_sync":    any(k in fix for k in ["mutex","channel","atomic","sync.map","errgroup","waitgroup","락"])}

G = dict(math_opt=g_math, monty=g_monty, subarray=g_sub, bulbs=g_bulbs, floors=g_floors, go_race=g_go,
         h_triples=g_triples, h_josephus=g_josephus, h_seating=g_seating, h_modexp=g_modexp, h_gobugs=g_gobugs)

def grade_all():
    rows = []
    for f in sorted(glob.glob(os.path.join(RAW, "*.json"))):
        r = json.load(open(f))
        checks = G[r["task"]](r["output"])
        r["checks"] = checks
        r["score"] = sum(checks.values()) / len(checks)
        r["pass"] = all(checks.values())
        r["has_answer_line"] = bool(answer_line(r["output"]))
        rows.append(r)
    return rows

if __name__ == "__main__":
    rows = grade_all()
    json.dump([{k: v for k, v in r.items() if k != "output"} for r in rows],
              open(os.path.join(LAB, "graded.json"), "w"), ensure_ascii=False, indent=1)
    for r in rows:
        print(f'{r["task"]:10s} {r["cond"]:5s} {r["model"][-14:]:14s} r{r["rep"]} '
              f'score={r["score"]:.2f} pass={r["pass"]} {r["latency"]:6.1f}s  {answer_line(r["output"])[:70]}')
    print(f"\n{len(rows)} runs graded")

def g_grid(out): return {"paths=911": num(answer_line(out)) == "911"}
def g_sim(out): return {"sum=312": num(answer_line(out)) == "312"}
def g_perm(out): return {"count=15702": num(answer_line(out)) == "15702"}
def g_knap(out): return {"value=140": num(answer_line(out)) == "140"}
def g_premise(out):
    a = answer_line(out)
    m = re.search(r'count\s*=\s*(\d+)', a, re.I)
    rs = set(re.findall(r'-?\d+', a.split('roots')[-1])) if 'roots' in a.lower() else set()
    return {"rejects_uniqueness(count=4)": bool(m) and m.group(1) == "4",
            "all_four_roots": rs == {"-2","-1","1","2"}}
G.update(x_gridpaths=g_grid, x_simgrind=g_sim, x_permcount=g_perm, x_knapsack=g_knap, x_premise=g_premise)
