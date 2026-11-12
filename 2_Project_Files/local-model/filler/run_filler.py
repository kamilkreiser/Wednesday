#!/usr/bin/env python3
"""run_filler.py - take the next `queued` row of filler/queue.tsv, run ONE task on the Spark, check it, mark the row.

usage: run_filler.py [--id ID] [--dry] [--stub-reply FILE] [--no-gate]
  (default)         next queued row; refuses (rc 3, row untouched) unless every gate is open:
                      (i) no A/B run (pgrep spark-ab/ab.py)  (ii) spark/state/round.lock + queue.lock free  (iii) tunnel UP
  --id ID           that row instead of the next queued one
  --dry             print what would run and the gate state; change nothing
  --stub-reply FILE exercise seam: FILE's text is the Spark's reply (no network, no gates); used by tests/ and the red-proofs
rc 0 = a task ran (any checker verdict is data, recorded) / nothing queued; 3 = gated (reasons printed); 2 = usage.

Statuses written to the row: running -> done_accepted | done_flagged | done_rejected | failed
  mutants: done_accepted = >=1 mutant kept; done_rejected = every Spark mutant refused by the checker
  numstat: done_accepted = MATCH; done_flagged = MISMATCH (the seat's claim disagrees with the API) or NO_CLAIMS; done_rejected = ungrounded Spark output
Everything lands in filler/runs/<id>/ (result.json, the Spark's raw replies, accepted mutant diffs) and one line in filler/runs.tsv.
One client's content per task (task.client, Secuura only in v1). Never a board write, mail, push, Linear or GitHub write.
Python 3 stdlib only; the Spark is called through ../lib/spark_call.py (one request at a time).
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import filler_lib as L  # noqa: E402

QUEUE = os.environ.get("FILLER_QUEUE") or os.path.join(HERE, "queue.tsv")
RUNS = os.environ.get("FILLER_RUNS") or os.path.join(HERE, "runs")
LOG = os.environ.get("FILLER_LOG") or os.path.join(HERE, "runs.tsv")
SPARK_CALL = os.path.join(L.LM, "lib", "spark_call.py")
MODEL = os.environ.get("SPARK_MODEL", "nemotron-3.5-super-vl")
ALLOWED_CLIENTS = {"Secuura"}
HEADER = ("# Spark STANDING FILLER QUEUE (routine (c), Kam 2026-11-12). One row per task; columns tab-separated:\n"
          "# id, kind (mutants|numstat), input (task json, relative to filler/), status (queued|running|done_accepted|done_flagged|done_rejected|failed), result (relative to filler/).\n"
          "# Add a row + a tasks/<id>.json to queue work; run_filler.py takes the next `queued` one. Secuura content only in v1.\n")


def save(rows, row, **kw):
    row.update(kw)
    L.write_queue(QUEUE, rows, HEADER)


def call_spark(task_md, inp, out_dir, tag, max_tokens, stub):
    """-> (text, meta). One spark_call.py request (or the stub text). Raises RuntimeError on a failed call."""
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, tag + ".out.md")
    if stub is not None:
        open(out, "w").write(stub)
        return stub, {"wall_clock_seconds": 0.0, "usage": {}, "stub": True}
    tp, ip, mp = (os.path.join(out_dir, tag + s) for s in (".task.md", ".input.json", ".meta.json"))
    open(tp, "w").write(task_md)
    json.dump(inp, open(ip, "w"))
    r = subprocess.run([sys.executable, SPARK_CALL, tp, ip, out, mp, MODEL, str(max_tokens), L.SPARK_URL, "0"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("spark_call rc %d: %s" % (r.returncode, r.stderr.strip()[-300:]))
    return open(out).read(), json.load(open(mp))


def tally(meta, acc):
    acc["spark_seconds"] = round(acc.get("spark_seconds", 0.0) + float(meta.get("wall_clock_seconds") or 0.0), 2)
    u = meta.get("usage") or {}
    acc["prompt_tokens"] = acc.get("prompt_tokens", 0) + int(u.get("prompt_tokens") or 0)
    acc["completion_tokens"] = acc.get("completion_tokens", 0) + int(u.get("completion_tokens") or 0)
    acc["calls"] = acc.get("calls", 0) + 1


def run_mutants(task, rdir, stub):
    src = os.path.join(HERE, task["source"])
    orig = open(src, encoding="utf-8").read()
    lines = orig.split("\n")
    lo, hi = task["lines"]
    stats, seen, used, results = {}, set(), [], []
    accepted = 0
    for k in range(task["n"]):
        md, inp = L.mutant_prompt(task, lines, used)
        try:
            text, meta = call_spark(md, inp, rdir, "m%02d" % (k + 1), 4000, stub[k] if isinstance(stub, list) else stub)
        except RuntimeError as e:
            results.append({"n": k + 1, "accepted": False, "reason": "SPARK CALL FAILED: %s" % e})
            break
        tally(meta, stats)
        v = L.check_mutant(text, orig, task["rel_path"], lo, hi, os.path.join(rdir, "scratch"), seen)
        v["n"] = k + 1
        if v["accepted"]:
            accepted += 1
            seen.add(v["result_hash"])
            open(os.path.join(rdir, "mutant_%02d.diff" % (k + 1)), "w").write(v["patch"])
            changed = [l for l in v["patch"].split("\n") if l[:1] in "+-" and not l.startswith(("+++", "---"))]
            used.append(" | ".join(x.strip() for x in changed)[:160])
        else:
            used.append("(refused, do not repeat the shape of attempt %d)" % (k + 1))
        v.pop("patch", None)
        results.append(v)
    verdict = "ACCEPTED" if accepted else "REJECTED"
    return ("done_accepted" if accepted else "done_rejected"), {
        "verdict": "%s %d/%d mutants kept" % (verdict, accepted, task["n"]), "accepted": accepted, "asked": task["n"],
        "mutants": results, **stats}


def run_numstat(task, rdir, stub):
    mail = open(os.path.join(HERE, task["mail"]), encoding="utf-8", errors="replace").read()
    meta_pr = json.load(open(os.path.join(HERE, task["api_meta"])))
    files = json.load(open(os.path.join(HERE, task["api_files"])))
    md, inp = L.numstat_prompt(task, mail)
    stats = {}
    try:
        text, meta = call_spark(md, inp, rdir, "claims", 1500, stub)
    except RuntimeError as e:
        return "failed", {"verdict": "FAILED", "reason": str(e)}
    tally(meta, stats)
    try:
        claim = L.parse_claim_json(text)
    except Exception as e:  # noqa: BLE001
        return "done_rejected", {"verdict": "REJECTED_UNGROUNDED", "grounding": ["unparseable reply: %s" % e], "raw": text[:400], **stats}
    chk = L.check_numstat(claim, mail, meta_pr, files, task["pr"])
    status = {"MATCH": "done_accepted", "MISMATCH": "done_flagged", "NO_CLAIMS": "done_flagged"}.get(chk["verdict"], "done_rejected")
    return status, {**chk, "claim": claim, "api": {k: meta_pr[k] for k in ("additions", "deletions", "changed_files", "head")}, **stats}


def main(argv):
    args = argv[1:]
    want_id = args[args.index("--id") + 1] if "--id" in args else None
    dry = "--dry" in args
    stub_file = args[args.index("--stub-reply") + 1] if "--stub-reply" in args else None
    stub = open(stub_file).read() if stub_file else None
    rows = L.read_queue(QUEUE)
    row = next((r for r in rows if (r["id"] == want_id if want_id else r["status"] == "queued")), None)
    if row is None:
        print("filler: nothing queued" if not want_id else "filler: no row %s" % want_id)
        return 0
    why = [] if stub is not None or "--no-gate" in args else L.gate_reasons()
    print("filler: next row %s (%s) · gates: %s" % (row["id"], row["kind"], "OPEN" if not why else "CLOSED: " + "; ".join(why)))
    if dry:
        return 0
    if why:
        return 3
    task = json.load(open(os.path.join(HERE, row["input"])))
    if task.get("client") not in ALLOWED_CLIENTS:
        save(rows, row, status="failed")
        print("filler: task client %r not allowed in v1" % task.get("client"))
        return 0
    rdir = os.path.join(RUNS, row["id"])
    os.makedirs(rdir, exist_ok=True)
    save(rows, row, status="running", result="runs/%s/result.json" % row["id"])
    t0 = time.time()
    try:
        status, res = (run_mutants if row["kind"] == "mutants" else run_numstat)(task, rdir, [stub] * task.get("n", 1) if stub is not None and row["kind"] == "mutants" else stub)
    except Exception as e:  # noqa: BLE001 - a crashed run is recorded, never silent
        status, res = "failed", {"verdict": "FAILED", "reason": "%s: %s" % (type(e).__name__, e)}
    res.update(id=row["id"], kind=row["kind"], finished_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
               wall_seconds=round(time.time() - t0, 1), model=MODEL)
    json.dump(res, open(os.path.join(rdir, "result.json"), "w"), indent=1)
    save(rows, row, status=status)
    new = not os.path.isfile(LOG)
    with open(LOG, "a") as f:
        if new:
            f.write("id\tkind\tfinished_utc\tspark_s\tprompt_tok\tcompletion_tok\tcalls\tstatus\tverdict\n")
        f.write("\t".join(str(x) for x in (row["id"], row["kind"], res["finished_utc"], res.get("spark_seconds", ""), res.get("prompt_tokens", ""),
                                           res.get("completion_tokens", ""), res.get("calls", ""), status, res.get("verdict", ""))) + "\n")
    print("filler: %s -> %s · %s · spark %ss" % (row["id"], status, res.get("verdict"), res.get("spark_seconds")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
