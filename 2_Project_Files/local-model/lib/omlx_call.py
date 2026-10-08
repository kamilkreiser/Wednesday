#!/usr/bin/env python3
"""omlx_call.py — the ONE HTTP call the local-model harness makes when LM_BACKEND=omlx (2026-10-08).

Kam 2026-10-08 18:12 (verbatim): "go with Ornith 1.5 and deploy it. use this instead of the old model. Keep pushing it
and see how far it can go." Promoted from the A/B's scratch client (runs/ab_ornith15_2026-10-08/omlx_call.py, results
in 0_Brain/reference/2026-10-08_omlx-flash-next/ORNITH15_AB.md) to this tracked path; the request body is unchanged.

Same prompt as lm_call.py byte for byte: SYSTEM_PREAMBLE (imported from lm_call.py, never copied) +
"## TASK\n<task.md>\n\n## INPUT (JSON)\n<input.json>\n". Same sampler as the 1.0 runs where oMLX has the knob:
temperature 0, repetition_penalty 1.15 over the last 512 tokens (LM_REPEAT_PENALTY / LM_REPEAT_LAST_N), max_tokens
(argv, = lm_call num_predict 32768 by default). Thinking OFF via chat_template_kwargs.enable_thinking=false unless
<think> is 1. Streams with include_usage so decode tok/s excludes prefill. The server is local-model/omlx_serve.sh.

Writes <out.md>, <meta.json> (lm_call's key set + backend/omlx keys — "backend":"omlx" and "model" are what lets a later
count tell 1.5 from 1.0), <out.md>.raw.json (the assembled stream: content, reasoning, usage, finish_reason).
Usage: omlx_call.py <task.md> <input.json> <out.md> <meta.json> <model> <max_tokens> <base_url> [<think 1|0>]
Exit: 0 ok · 2 usage · 4 HTTP/shape failure · 5 HTTP 507 (oMLX memory ceiling) — the caller STOPS on 5.
stderr is never redirected to /dev/null by anything that shells out to this.
"""
import hashlib, json, os, re, sys, time, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # self-locating
from lm_call import SYSTEM_PREAMBLE  # noqa: E402

REP_PEN = float(os.environ.get("LM_REPEAT_PENALTY", "1.15"))
REP_N = int(os.environ.get("LM_REPEAT_LAST_N", "512"))


def main():
    if len(sys.argv) not in (8, 9):
        sys.stderr.write(__doc__); return 2
    task_path, input_path, out_path, meta_path, model, max_tok_s, base = sys.argv[1:8]
    think = (sys.argv[8] if len(sys.argv) == 9 else "0").strip().lower() not in ("0", "false", "no", "off", "")
    MAX_TOK = int(max_tok_s)
    try:
        import subprocess
        load_at_start = subprocess.check_output(["sysctl", "-n", "vm.loadavg"], text=True).strip()
    except Exception:
        load_at_start = "UNKNOWN"
    task_text = open(task_path, encoding="utf-8").read()
    input_text = open(input_path, encoding="utf-8").read()
    try:
        json.loads(input_text)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"omlx_call: input is not valid JSON: {e}\n"); return 4
    sha = hashlib.sha256((task_text + input_text).encode("utf-8")).hexdigest()
    user_content = "## TASK\n" + task_text.strip() + "\n\n## INPUT (JSON)\n" + input_text.strip() + "\n"
    body = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PREAMBLE}, {"role": "user", "content": user_content}],
        "temperature": 0, "top_p": 1,
        "repetition_penalty": REP_PEN, "repetition_context_size": REP_N,
        "max_tokens": MAX_TOK,
        "stream": True, "stream_options": {"include_usage": True},
        "chat_template_kwargs": {"enable_thinking": think},
    }
    req = urllib.request.Request(base.rstrip("/") + "/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    t0 = time.time(); t_first = t_last = None; content = []; reasoning = []; usage = {}; finish = None
    try:
        with urllib.request.urlopen(req, timeout=3600) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:") or line == "data: [DONE]":
                    continue
                try:
                    ev = json.loads(line[5:])
                except json.JSONDecodeError:
                    continue
                if ev.get("usage"):
                    usage = ev["usage"]
                for ch in ev.get("choices", []):
                    d = ch.get("delta", {}) or {}
                    c = d.get("content"); rc = d.get("reasoning_content") or d.get("reasoning")
                    if c or rc:
                        now = time.time(); t_first = t_first or now; t_last = now
                    if c: content.append(c)
                    if rc: reasoning.append(rc)
                    finish = ch.get("finish_reason") or finish
    except urllib.error.HTTPError as e:
        b = e.read()[:2000]
        sys.stderr.write(f"omlx_call: HTTP error {e.code}: {b!r}\n")
        return 5 if e.code == 507 else 4
    except (urllib.error.URLError, OSError) as e:
        sys.stderr.write(f"omlx_call: connection error after {time.time()-t0:.1f}s: {e}\n"); return 4
    except Exception as e:  # a mid-stream reset etc. — never a traceback with no line for the run.log
        sys.stderr.write(f"omlx_call: stream error after {time.time()-t0:.1f}s: {type(e).__name__}: {e}\n"); return 4
    wall = time.time() - t0
    content = "".join(content); reasoning = "".join(reasoning)
    json.dump({"content": content, "reasoning": reasoning, "usage": usage, "finish_reason": finish},
              open(out_path + ".raw.json", "w", encoding="utf-8"), indent=1)
    leak = "<think>" in content or "</think>" in content
    cleaned = content
    if leak:
        cleaned = re.sub(r"<think>.*?</think>\s*", "", cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"^.*?</think>\s*", "", cleaned, flags=re.DOTALL)
    cleaned = cleaned.strip()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned + ("\n" if not cleaned.endswith("\n") else ""))
    ct = usage.get("completion_tokens") or 0
    dec = round((ct - 1) / (t_last - t_first), 2) if t_first and t_last and t_last > t_first and ct > 1 else None
    meta = {
        "backend": "omlx", "model": model, "base_url": base,
        "sampler": {"temperature": 0, "top_p": 1, "repetition_penalty": REP_PEN, "repetition_context_size": REP_N,
                    "max_tokens": MAX_TOK, "enable_thinking": think},
        "prompt_eval_count": usage.get("prompt_tokens"), "eval_count": ct, "usage": usage,
        "wall_clock_seconds": round(wall, 3), "ttft_seconds": round(t_first - t0, 3) if t_first else None,
        "decode_tok_s": dec, "end_to_end_tok_s": round(ct / wall, 2) if wall > 0 and ct else None,
        "sha256_task_plus_input": sha, "think_field_requested": think, "load_at_start": load_at_start,
        "prompt_bytes": len(SYSTEM_PREAMBLE.encode("utf-8")) + len(user_content.encode("utf-8")),
        "thinking_chars": len(reasoning), "think_leak_in_content": leak,
        "done": finish is not None, "done_reason": finish, "content_chars": len(cleaned),
    }
    json.dump(meta, open(meta_path, "w", encoding="utf-8"), indent=1)
    sys.stderr.write(f"omlx_call: ok wall={wall:.2f}s prompt={usage.get('prompt_tokens')} completion={ct} "
                     f"ttft={meta['ttft_seconds']} decode_tok/s={dec} model={model} backend=omlx thinking_chars={len(reasoning)} leak={leak} "
                     f"finish={finish} content_chars={len(cleaned)} sha={sha[:10]}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
