# -*- coding: utf-8 -*-
import os, re, sys, json, time, subprocess, tempfile, hashlib
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tasks import TASKS

LAB = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(LAB, "raw"); os.makedirs(RAW, exist_ok=True)
P31 = open(os.path.join(LAB, "prompt_v31.txt")).read()
P1  = open(os.path.join(LAB, "prompt_v1.txt")).read()
CONDS = {"base": None, "v1": P1, "v31": P31}

NOTOOLS = ("[RULE] 반드시 순수 추론(reasoning)만으로 답하시오. 터미널/셸 명령, 코드 실행, 파일 읽기, "
           "웹 검색 등 어떤 도구도 절대 사용하지 마시오. 계산은 머릿속(텍스트)으로 수행하시오.")

def build(task, cond):
    t = TASKS[task]
    body = NOTOOLS + "\n\n" + t["question"] + "\n\n" + t["fmt"]
    sysp = CONDS[cond]
    return body if sysp is None else sysp + "\n\n---\n\n[USER INQUIRY]\n" + body

def run_one(job):
    task, cond, model, rep = job
    key = f"{task}__{cond}__{model}__r{rep}"
    out_path = os.path.join(RAW, key + ".json")
    if os.path.exists(out_path):
        return json.load(open(out_path))
    prompt = build(task, cond)
    attempts = []
    for attempt in range(3):
        rec = _invoke(prompt, model)
        attempts.append(rec["rc"])
        if rec["chars"] > 0:
            break
    rec.update(task=task, cond=cond, model=model, rep=rep, attempts=len(attempts))
    json.dump(rec, open(out_path, "w"), ensure_ascii=False)
    print(f"done {key} {rec['latency']:.0f}s {rec['chars']}ch tries={len(attempts)}", flush=True)
    return rec

def _invoke(prompt, model):
    workdir = tempfile.mkdtemp(prefix="agyrun_")   # clean dir: no repo files visible to the agent
    t0 = time.time()
    try:
        r = subprocess.run(["agy", "-p", prompt, "--model", model,
                            "--output-format", "text", "--disable-slash-commands"],
                           cwd=workdir, capture_output=True, text=True, timeout=600)
        out, err, rc = r.stdout, r.stderr[-2000:], r.returncode
    except subprocess.TimeoutExpired:
        out, err, rc = "", "TIMEOUT", -9
    dt = time.time() - t0
    return dict(latency=round(dt, 2), chars=len(out), rc=rc, stderr=err, output=out)

if __name__ == "__main__":
    models = sys.argv[1].split(",")
    conds  = sys.argv[2].split(",")
    tasks  = sys.argv[3].split(",") if sys.argv[3] != "all" else list(TASKS)
    reps   = int(sys.argv[4]); par = int(sys.argv[5])
    jobs = [(t, c, m, r) for t in tasks for c in conds for m in models for r in range(1, reps+1)]
    print(f"{len(jobs)} jobs, parallel={par}")
    with ThreadPoolExecutor(max_workers=par) as ex:
        list(ex.map(run_one, jobs))
    print("ALL DONE")
