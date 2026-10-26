#!/usr/bin/env python3
"""spark-ab/ab.py — run the Spark A/B task set (tasks.json) against ONE model on the Spark, or a checker control.

Brief: spark-ab/BRIEF.md (Kam 2026-10-26 12:32:27). Ornith 1.5 122B NVFP4 vs DeepSeek V4 Flash, same prompts, same
sampler, same checker.

  ab.py --model control              re-check each task's ORIGINAL Spark out.md with today's checker (no model call):
                                     proves the checker leg reproduces the recorded verdict (PASS and FAIL) before any
                                     model verdict is trusted.
  ab.py --model deepseek|ornith [--url http://127.0.0.1:47788] [--only T01,T02] [--served-name NAME]

Per task:
  1. hosted/replay.build_messages(<spark run dir>) rebuilds the Spark's exact messages and REFUSES unless
     sha256(task+input) and prompt_bytes equal that round's meta (imported, not reimplemented).
  2. POST <url>/v1/chat/completions with lib/spark_call.py's body shape: temperature 0, max_tokens 16384, thinking OFF
     (deepseek: chat_template_kwargs.thinking=false, as spark_call.py; ornith: chat_template_kwargs.enable_thinking=false,
     the field its chat template reads). One request at a time.
  3. out.md / .meta.json / .raw.json written in spark_call.py's shape (same strip, unfenced-diff wrap, unclosed-fence
     close — close_unclosed_fence and DIFF_GRAMMAR imported from lib/spark_call.py).
  4. hosted/check.sh <run> <tier> <tip> <work> [golden]: the SAME checker scripts round.sh ran for that tier, at the
     round's own tip. Clones are kept (nothing is deleted).
Records: runs/<model>/results.jsonl (full checker line; gitignored, may quote Secuura lines) and
results_<model>.tsv beside this file (tracked: ids, verdicts, clause names, tokens, seconds — no code).
Exit 0 always after a full drain (verdicts are data); 2 refusal (byte identity); 4 endpoint/shape failure (stops).
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
LM = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LM, "hosted"))
sys.path.insert(0, os.path.join(LM, "lib"))
import replay  # noqa: E402  — build_messages (the byte-identity proof)
from spark_call import DIFF_GRAMMAR, close_unclosed_fence  # noqa: E402

RUNS_SRC = os.path.join(LM, "runs")
OUT = os.path.join(HERE, "runs")
WORK = os.path.join(HERE, "work")
CHECK = os.path.join(LM, "hosted", "check.sh")
MAX_TOKENS = 16384
MODELS = {
    "deepseek": {"served": "deepseek-v4-flash-0731", "kwargs": {"thinking": False}},
    "ornith": {"served": "Ornith-1.5-122B-NVFP4", "kwargs": {"enable_thinking": False}},
}


def load_tasks(only):
    t = json.load(open(os.path.join(HERE, "tasks.json"), encoding="utf-8"))["tasks"]
    if only:
        want = set(x.strip() for x in only.split(","))
        t = [x for x in t if x["id"] in want]
    return t


def first_fail_clause(checker_out):
    """The first FAIL clause NAME only (e.g. 'A2a', 'B3x') — never the line text, which can quote Secuura code."""
    for line in checker_out.splitlines():
        m = re.match(r"FAIL (A\d+[a-z]*|B\d+[a-z]*)\b", line)
        if m:
            return m.group(1)
    m = re.search(r"stopped at (\w+)", checker_out)
    return m.group(1) if m else "-"


def post(url, body, timeout=1800):
    req = urllib.request.Request(url.rstrip("/") + "/v1/chat/completions", data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def write_outputs(run, raw, wall, body, info, model_key):
    """spark_call.py's artefact shape."""
    out_path = os.path.join(run, "out.md")
    with open(out_path + ".raw.json", "wb") as f:
        f.write(raw)
    j = json.loads(raw)
    choice = j["choices"][0]
    msg = choice.get("message") or {}
    content = msg.get("content") or ""
    reasoning = msg.get("reasoning_content") or msg.get("reasoning") or ""
    finish = choice.get("finish_reason")
    usage = j.get("usage") or {}
    cleaned = content.strip()
    unfenced = False
    if cleaned and "```" not in cleaned and "~~~" not in cleaned and cleaned.startswith("--- "):
        if not [l for l in cleaned.split("\n") if l.strip() and not DIFF_GRAMMAR.match(l)]:
            unfenced = True
            cleaned = "```diff\n" + cleaned + "\n```"
    cleaned, closed = close_unclosed_fence(cleaned, finish)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned + ("\n" if not cleaned.endswith("\n") else ""))
    meta = {
        "backend": "spark-ab", "model": body["model"], "model_key": model_key, "max_tokens": body["max_tokens"],
        "sampler": {"temperature": 0, "max_tokens": body["max_tokens"], "chat_template_kwargs": body["chat_template_kwargs"]},
        "prompt_bytes": info["prompt_bytes"], "sha256_task_plus_input": info["sha256_task_plus_input"],
        "messages_sha256": info["messages_sha256"],
        "prompt_eval_count": usage.get("prompt_tokens"), "eval_count": usage.get("completion_tokens"), "usage": usage,
        "wall_clock_seconds": round(wall, 3),
        "decode_tok_s_end_to_end": round(usage["completion_tokens"] / wall, 2) if usage.get("completion_tokens") and wall else None,
        "thinking_chars": len(reasoning), "think_leak_in_content": ("<think>" in content or "</think>" in content),
        "finish_reason": finish, "done": finish is not None, "done_reason": finish,
        "unfenced_wrapped": unfenced, "unclosed_fence_closed": closed, "content_chars": len(cleaned),
        "task_file": info["task_path"],
    }
    with open(out_path + ".meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta


def check(run, info, model_key, tid):
    work = os.path.join(WORK, f"{model_key}_{tid}_{datetime.datetime.now():%H%M%S}")
    gold = os.path.join(info["brief_dir"], "golden.diff") if info.get("brief_dir") else ""
    t0 = time.time()
    p = subprocess.run(["bash", CHECK, run, info["tier"], info["tip"], work, gold if gold and os.path.isfile(gold) else ""],
                       capture_output=True, text=True)
    if p.stderr:
        with open(os.path.join(run, "check.stderr"), "w", encoding="utf-8") as f:
            f.write(p.stderr)
    last = (p.stdout.strip().splitlines() or ["CHECK HARNESS golden=none result=no output"])[-1]
    m = re.match(r"CHECK (\w+) golden=(\S+) result=(.*)", last)
    v, g, res = (m.group(1), m.group(2), m.group(3)) if m else ("HARNESS", "-", last)
    co = open(os.path.join(run, "checker.out"), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(run, "checker.out")) else ""
    return v, g, res, first_fail_clause(co) if v != "PASS" else "-", round(time.time() - t0, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=["control"] + sorted(MODELS))
    ap.add_argument("--url", default="http://127.0.0.1:47788")
    ap.add_argument("--only", default="")
    ap.add_argument("--served-name", default="")
    ap.add_argument("--label", default="", help="suffix for the results file (e.g. restore)")
    a = ap.parse_args()
    mk = a.model
    tasks = load_tasks(a.only)
    lab = mk + (("_" + a.label) if a.label else "")
    os.makedirs(os.path.join(OUT, lab), exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    tsv = os.path.join(HERE, f"results_{lab}.tsv")
    if not os.path.exists(tsv):
        with open(tsv, "w", encoding="utf-8") as f:
            f.write("when\tid\trung\texpect\tverdict\tfail_clause\tgolden\tprompt_tok\tcompletion_tok\tmodel_s\tcheck_s\tfinish\tthinking_chars\tmessages_sha256\tspark_verdict\tspark_run\n")
    plan = []
    for t in tasks:
        srun = os.path.join(RUNS_SRC, t["run"])
        try:
            msgs, info = replay.build_messages(srun)
        except replay.Refused as e:
            print(f"ab: REFUSED {t['id']} {t['run']}: {e}", flush=True)
            return 2
        plan.append((t, srun, msgs, info))
    print(f"ab: {lab}: {len(plan)} task(s) built; byte identity proven for all (sha256(task+input) + prompt_bytes vs each Spark round's meta)", flush=True)
    for t, srun, msgs, info in plan:
        run = os.path.join(OUT, lab, f"{t['id']}_{t['run'][len('spark_secuura_'):]}")
        n = 2
        base = run
        while os.path.exists(run):
            run, n = f"{base}-r{n}", n + 1
        os.makedirs(run)
        shutil.copyfile(os.path.join(srun, "input.json"), os.path.join(run, "input.json"))
        shutil.copyfile(info["task_path"], os.path.join(run, "task.md"))
        meta = {}
        if mk == "control":
            shutil.copyfile(os.path.join(srun, "out.md"), os.path.join(run, "out.md"))
            shutil.copyfile(os.path.join(srun, "out.md.meta.json"), os.path.join(run, "out.md.meta.json"))
            meta = json.load(open(os.path.join(srun, "out.md.meta.json")))
            wall = meta.get("wall_clock_seconds")
        else:
            m = MODELS[mk]
            body = {"model": a.served_name or m["served"], "messages": msgs, "max_tokens": MAX_TOKENS, "temperature": 0,
                    "chat_template_kwargs": dict(m["kwargs"])}
            with open(os.path.join(run, "request.json"), "w", encoding="utf-8") as f:
                json.dump(body, f, indent=1)
            body_sha = hashlib.sha256(json.dumps(msgs, ensure_ascii=False).encode("utf-8")).hexdigest()
            assert body_sha == info["messages_sha256"], "messages changed between build and send"
            t0 = time.time()
            try:
                raw = post(a.url, body)
            except urllib.error.HTTPError as e:
                print(f"ab: HTTP {e.code} on {t['id']}: {e.read()[:600]!r}", flush=True)
                return 4
            except (urllib.error.URLError, OSError) as e:
                print(f"ab: connection error on {t['id']} after {time.time() - t0:.1f}s: {e}", flush=True)
                return 4
            wall = time.time() - t0
            try:
                meta = write_outputs(run, raw, wall, body, info, mk)
            except (ValueError, KeyError, IndexError) as e:
                print(f"ab: unexpected response shape on {t['id']}: {e}", flush=True)
                return 4
        harness = ""
        if mk != "control" and (meta.get("thinking_chars") or meta.get("think_leak_in_content")):
            harness = "thinking ON or leaked (requested off)"
        if harness:
            v, g, res, fc, cs = "HARNESS", "-", harness, "-", 0
        else:
            v, g, res, fc, cs = check(run, info, mk, t["id"])
        rec = {"when": datetime.datetime.now().isoformat(timespec="seconds"), "id": t["id"], "rung": t["rung"],
               "expect": t["expect"], "verdict": v, "fail_clause": fc, "golden": g, "result": res,
               "prompt_tokens": meta.get("prompt_eval_count"), "completion_tokens": meta.get("eval_count"),
               "model_s": round(wall, 3) if isinstance(wall, (int, float)) else wall, "check_s": cs,
               "finish": meta.get("finish_reason") or meta.get("done_reason"), "thinking_chars": meta.get("thinking_chars"),
               "messages_sha256": info["messages_sha256"], "spark_verdict": info["spark_verdict"],
               "spark_result": info["spark_result"], "spark_run": t["run"], "run": run}
        with open(os.path.join(OUT, lab, "results.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        with open(tsv, "a", encoding="utf-8") as f:
            f.write("\t".join(str(rec[k]) for k in ("when", "id", "rung", "expect", "verdict", "fail_clause", "golden",
                                                       "prompt_tokens", "completion_tokens", "model_s", "check_s", "finish",
                                                       "thinking_chars", "messages_sha256", "spark_verdict", "spark_run")) + "\n")
        print(f"AB {lab} {t['id']} R{t['rung']} expect={t['expect']}: {v} [{fc}] golden={g} · {rec['prompt_tokens']}+"
              f"{rec['completion_tokens']} tok · model {rec['model_s']}s · check {cs}s · Spark was {info['spark_verdict']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
