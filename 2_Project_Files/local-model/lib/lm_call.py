#!/usr/bin/env python3
"""lm_call.py — the ONE HTTP call the local-model harness makes.

Called by local_model_task.sh (bash 3.2 has no `timeout`, so the wait is a
plain urllib call with a Python-side timeout). Builds the bounded prompt,
POSTs to /api/chat, writes <out>.md and <out>.md.meta.json.

Never called directly by a task author — local_model_task.sh is the contract.
stderr is never redirected to /dev/null by anything that shells out to this.

THINK-FIELD FINDING (probed 2026-09-14, ollama 0.18.2, qwen3:30b-a3b):
the README/ollama docs suggested `think: false` disables reasoning. Probing
showed the OPPOSITE is what actually works cleanly here: `think: false`
does NOT stop the model from reasoning — it just stops ollama from
separating that reasoning out, so it leaks into `message.content` ahead of
the real answer (observed: no opening <think> tag at all, because ollama's
chat template inserts it as part of the PROMPT before generation starts —
only a trailing </think> shows up in the returned text). A Qwen3 `/no_think`
directive in the user turn sometimes suppresses it but was NOT reliable on
a longer, realistic task+input prompt (it still reasoned for ~700 words).
`think: true`, by contrast, makes ollama return a clean, SEPARATE
`message.thinking` field and a `message.content` that is exactly the
model's final answer with no leakage — verified on all three pilot tasks.
So the harness sends `think: true` and reads `content` only; `thinking` is
recorded (length only, not the text) in the sidecar meta for transparency.
"""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request

SYSTEM_PREAMBLE = (
    "You are a bounded task tool, not an agent. You hold no board identity and "
    "must never call Linear, GitHub, or any other service — you only see the "
    "text given to you below.\n"
    "Rules:\n"
    "1. Answer ONLY from facts present in the INPUT JSON below. Never invent an "
    "id, name, date, or value that is not in the input.\n"
    "2. Produce ONLY the output format the TASK section names. No preamble, no "
    "explanation, no markdown code fences unless the task explicitly asks for "
    "them, no closing remarks.\n"
    "3. Where the input lacks a fact the task needs, write UNKNOWN in that "
    "field rather than guessing.\n"
    "4. Do not ask questions back. Produce the output and stop."
)


def main():
    if len(sys.argv) != 8:
        sys.stderr.write(
            "lm_call: usage: lm_call.py <task.md> <input.json> <out.md> "
            "<meta.json> <model> <num_ctx> <base_url>\n"
        )
        return 2
    task_path, input_path, out_path, meta_path, model, num_ctx_s, base_url = sys.argv[1:8]

    task_text = open(task_path, encoding="utf-8").read()
    input_text = open(input_path, encoding="utf-8").read()

    # Validate the input is actually JSON — a bounded tool that cannot trust
    # its own input file is not bounded.
    try:
        json.loads(input_text)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"lm_call: input is not valid JSON: {e}\n")
        return 4

    num_ctx = int(num_ctx_s)
    sha = hashlib.sha256((task_text + input_text).encode("utf-8")).hexdigest()

    user_content = (
        "## TASK\n" + task_text.strip() + "\n\n"
        "## INPUT (JSON)\n" + input_text.strip() + "\n"
    )
    prompt_bytes = len(SYSTEM_PREAMBLE.encode("utf-8")) + len(user_content.encode("utf-8"))

    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PREAMBLE},
            {"role": "user", "content": user_content},
        ],
        "stream": False,
        "think": True,  # see module docstring: True (not False) is what
                         # actually yields a clean content/thinking split.
        "options": {"num_ctx": num_ctx, "temperature": 0},
    }).encode("utf-8")

    load_at_start = ""
    try:
        import subprocess
        load_at_start = subprocess.check_output(
            ["sysctl", "-n", "vm.loadavg"], text=True
        ).strip()
    except Exception:
        load_at_start = "UNKNOWN"

    req = urllib.request.Request(
        base_url.rstrip("/") + "/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"lm_call: HTTP error {e.code}: {e.read()[:2000]!r}\n")
        return 4
    except urllib.error.URLError as e:
        sys.stderr.write(f"lm_call: connection error: {e}\n")
        return 4
    wall_clock = time.time() - t0

    try:
        j = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"lm_call: response was not valid JSON: {e}; body={raw[:2000]!r}\n")
        return 4

    if "message" not in j or "content" not in j.get("message", {}):
        sys.stderr.write(f"lm_call: unexpected response shape: {json.dumps(j)[:2000]}\n")
        return 4

    content = j["message"]["content"]
    thinking = j["message"].get("thinking") or ""
    # Belt-and-suspenders: content should already be clean with think:true,
    # but if a future ollama version regresses and leaks a </think> marker
    # into content anyway, strip everything up to and including it rather
    # than ship raw chain-of-thought to a checker.
    think_leak_in_content = "</think>" in content or "<think>" in content
    if think_leak_in_content:
        import re
        cleaned = re.sub(r"<think>.*?</think>\s*", "", content, flags=re.DOTALL)
        cleaned = re.sub(r"^.*?</think>\s*", "", cleaned, flags=re.DOTALL).strip()
    else:
        cleaned = content.strip()

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned + ("\n" if not cleaned.endswith("\n") else ""))

    meta = {
        "model": model,
        "num_ctx": num_ctx,
        "prompt_bytes": prompt_bytes,
        "prompt_eval_count": j.get("prompt_eval_count"),
        "eval_count": j.get("eval_count"),
        "total_duration_ns": j.get("total_duration"),
        "load_duration_ns": j.get("load_duration"),
        "wall_clock_seconds": round(wall_clock, 3),
        "load_at_start": load_at_start,
        "sha256_task_plus_input": sha,
        "think_field_requested": True,
        "thinking_chars": len(thinking),
        "think_leak_in_content": think_leak_in_content,
        "done_reason": j.get("done_reason"),
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")

    toks_per_s = None
    if meta["eval_count"] and j.get("eval_duration"):
        toks_per_s = round(meta["eval_count"] / (j["eval_duration"] / 1e9), 2)
    sys.stderr.write(
        f"lm_call: ok wall={wall_clock:.2f}s eval_count={meta['eval_count']} "
        f"tok/s={toks_per_s} thinking_chars={len(thinking)} "
        f"think_leak_in_content={think_leak_in_content}\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
