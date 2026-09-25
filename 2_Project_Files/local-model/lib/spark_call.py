#!/usr/bin/env python3
"""spark_call.py — the ONE HTTP call the local-model harness makes when LM_BACKEND=spark.

The Spark twin of lib/lm_call.py (2026-09-25, Kam live board 15:28: "Use the spark as much as possible
and push it to its limits ... give it real work but measure progress"). Called ONLY by
local_model_task.sh's LM_BACKEND=spark branch; the Ornith/ollama path (lm_call.py) is untouched.

Target: DeepSeek V4 Flash (vLLM, OpenAI-compatible) on the Spark box, reached through an ssh tunnel
(PORTS.md 47788 -> the box's 127.0.0.1:8888). It writes the SAME artefacts lm_call.py writes, so the
task checkers and hold_ready.py read a Spark run exactly as they read an Ornith run:
  <out.md>            the model's answer (content), stripped, trailing newline
  <out.md>.meta.json  lm_call.py's key set (prompt_eval_count / eval_count / done_reason / wall_clock_seconds ...)
                      plus backend/spark-only keys (finish_reason, usage, thinking, unfenced_wrapped, max_tokens)
  <out.md>.raw.json   the raw response body

THE SETTINGS THAT DECIDE OUTCOMES (each measured on the box, HANDOFF.md 2026-09-22 + Friday's smoke):
  - thinking OFF: `"chat_template_kwargs": {"thinking": false}` — the field Friday's
    ~/spark-eval/friday_smoke_test.py sends (read on the box 2026-09-25, byte-identical to the Studio's copy).
    Thinking ON (the server default, effort=max) spends the whole completion budget and returns EMPTY content.
    SPARK_THINK=1 turns it on (never for coding tasks).
  - temperature 0; one request at a time (MAX_NUM_SEQS=1) — the caller never fans out.
  - finish_reason "length" is written to meta as done_reason "length", so checker.sh's A1 names a TOKEN BUDGET
    CUT instead of "no diff block" (the same key lm_call.py writes from ollama's done_reason).
  - System prompt = lm_call.py's SYSTEM_PREAMBLE (imported, never copied, so the two cannot drift) + the kit's
    01_FOR_THE_LOCAL_MODEL.md task contract (spark-kit README step 1: "put 01 where your runner injects a system prompt").
  - UNFENCED WHOLE-ANSWER DIFF (kit 04 failure mode 8, measured by Friday 2026-09-23): when the answer carries ZERO
    fences, starts with `--- `, and EVERY non-empty line is unified-diff grammar, out.md gets the answer wrapped in a
    ```diff fence and meta records unfenced_wrapped=true + a CONTRACT BREACH (format) line on stderr. Any prose keeps
    the answer verbatim (checker A1 then refuses it). The raw body is always kept.

Usage: spark_call.py <task.md> <input.json> <out.md> <meta.json> <model> <max_tokens> <base_url> [<think 1|0>]
Exit codes: 0 ok (a verdict is the checker's job) · 2 usage · 4 HTTP/JSON/shape failure.
stderr is never redirected to /dev/null by anything that shells out to this. Python 3 stdlib only.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lm_call import SYSTEM_PREAMBLE  # noqa: E402  — one preamble for both backends

KIT_CONTRACT = os.path.normpath(os.path.join(HERE, "..", "spark-kit", "01_FOR_THE_LOCAL_MODEL.md"))
DIFF_GRAMMAR = re.compile(r"^(--- |\+\+\+ |@@ -\d+(,\d+)? \+\d+(,\d+)? @@| |\+|-|\\ No newline|diff --git |index |new file mode )")


def main():
    if len(sys.argv) not in (8, 9):
        sys.stderr.write("spark_call: usage: spark_call.py <task.md> <input.json> <out.md> <meta.json> "
                         "<model> <max_tokens> <base_url> [<think 1|0>]\n")
        return 2
    task_path, input_path, out_path, meta_path, model, max_tokens_s, base_url = sys.argv[1:8]
    think = (sys.argv[8] if len(sys.argv) == 9 else "0").strip().lower() not in ("0", "false", "no", "off", "")

    task_text = open(task_path, encoding="utf-8").read()
    input_text = open(input_path, encoding="utf-8").read()
    try:
        json.loads(input_text)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"spark_call: input is not valid JSON: {e}\n")
        return 4
    if not os.path.isfile(KIT_CONTRACT):
        sys.stderr.write(f"spark_call: the kit's task contract is missing at {KIT_CONTRACT} — refusing to call without it\n")
        return 2
    contract = open(KIT_CONTRACT, encoding="utf-8").read().strip()
    system = SYSTEM_PREAMBLE + "\n\n" + contract
    max_tokens = int(max_tokens_s)
    sha = hashlib.sha256((task_text + input_text).encode("utf-8")).hexdigest()
    user_content = "## TASK\n" + task_text.strip() + "\n\n## INPUT (JSON)\n" + input_text.strip() + "\n"
    prompt_bytes = len(system.encode("utf-8")) + len(user_content.encode("utf-8"))

    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user_content}],
        "max_tokens": max_tokens,
        "temperature": 0,
        "chat_template_kwargs": {"thinking": think},
    }
    try:
        load_at_start = subprocess.check_output(["sysctl", "-n", "vm.loadavg"], text=True).strip()
    except Exception:
        load_at_start = "UNKNOWN"
    req = urllib.request.Request(base_url.rstrip("/") + "/v1/chat/completions",
                                 data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=int(os.environ.get("SPARK_HTTP_TIMEOUT", "1800"))) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"spark_call: HTTP error {e.code}: {e.read()[:2000]!r}\n")
        return 4
    except (urllib.error.URLError, OSError) as e:
        sys.stderr.write(f"spark_call: connection error after {time.time() - t0:.1f}s (a dropped tunnel looks exactly like a dead server — "
                         f"check `pgrep -fl 'L 47788:127.0.0.1:8888'` first): {e}\n")
        return 4
    wall_clock = time.time() - t0
    try:
        with open(out_path + ".raw.json", "wb") as rf:
            rf.write(raw)
    except OSError as e:
        sys.stderr.write(f"spark_call: could not save raw response: {e}\n")
    try:
        j = json.loads(raw)
        choice = j["choices"][0]
        msg = choice.get("message") or {}
    except Exception as e:
        sys.stderr.write(f"spark_call: unexpected response shape ({e!r}): {raw[:2000]!r}\n")
        return 4

    content = msg.get("content") or ""
    reasoning = msg.get("reasoning_content") or msg.get("reasoning") or ""
    finish = choice.get("finish_reason")
    usage = j.get("usage") or {}
    cleaned = content.strip()

    unfenced_wrapped = False
    if cleaned and "```" not in cleaned and "~~~" not in cleaned and cleaned.startswith("--- "):
        bad = [l for l in cleaned.split("\n") if l.strip() and not DIFF_GRAMMAR.match(l)]
        if not bad:
            unfenced_wrapped = True
            sys.stderr.write(f"spark_call: CONTRACT BREACH (format) — the answer is an UNFENCED diff; the WHOLE answer is unified-diff "
                             f"grammar ({cleaned.count(chr(10)) + 1} lines, 0 non-diff lines), so out.md carries it inside a ```diff fence "
                             f"(kit 04 failure mode 8). The raw body is in {out_path}.raw.json.\n")
            cleaned = "```diff\n" + cleaned + "\n```"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned + ("\n" if not cleaned.endswith("\n") else ""))

    meta = {
        "backend": "spark",
        "model": model,
        "base_url": base_url,
        "max_tokens": max_tokens,
        "sampler": {"temperature": 0, "max_tokens": max_tokens, "thinking": think},
        "prompt_bytes": prompt_bytes,
        "prompt_eval_count": usage.get("prompt_tokens"),
        "eval_count": usage.get("completion_tokens"),
        "usage": usage,
        "wall_clock_seconds": round(wall_clock, 3),
        "load_at_start": load_at_start,
        "sha256_task_plus_input": sha,
        "think_field_requested": think,
        "thinking_chars": len(reasoning),
        "think_leak_in_content": ("<think>" in content or "</think>" in content),
        "finish_reason": finish,
        "done": finish is not None,
        "done_reason": finish,  # the key checker.sh A1 reads ("length" = a budget cut)
        "unfenced_wrapped": unfenced_wrapped,
        "content_chars": len(cleaned),
        "system_prompt_files": ["lib/lm_call.py:SYSTEM_PREAMBLE", KIT_CONTRACT],
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    toks = round(usage["completion_tokens"] / wall_clock, 2) if usage.get("completion_tokens") and wall_clock > 0 else None
    sys.stderr.write(
        f"lm_call: ok backend=spark wall={wall_clock:.2f}s prompt_tokens={usage.get('prompt_tokens')} "
        f"eval_count={usage.get('completion_tokens')} tok/s(end-to-end)={toks} think={int(think)} thinking_chars={len(reasoning)} "
        f"done_reason={finish} unfenced_wrapped={unfenced_wrapped} content_chars={len(cleaned)}\n")
    if finish == "length":
        sys.stderr.write(f"spark_call: WARNING finish_reason=length — the answer was CUT at max_tokens={max_tokens}; "
                         f"this is a budget/harness fact, not a model verdict\n")
    if not cleaned:
        sys.stderr.write(f"spark_call: WARNING empty content (finish_reason={finish}, thinking_chars={len(reasoning)}) — "
                         f"not a model verdict; check thinking is off\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
