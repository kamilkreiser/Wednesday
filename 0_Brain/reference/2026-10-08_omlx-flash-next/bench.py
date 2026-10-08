#!/usr/bin/env python3
"""Tonight's speed probe for oMLX + Qwen3.8-Flash-Next (2026-10-08, untested until run).

Mirrors the jundot/omlx#4140 method: a nonce-prefixed FRESH request, then a
byte-identical REPLAY, streamed with include_usage, temperature 0, thinking off.
Decode tok/s = (completion_tokens - 1) / (t_last_token - t_first_token)  (prefill excluded, as #3723).
TTFT = t_first_token - t_send.

Usage:
  python3 -I bench.py --url http://127.0.0.1:47780 --model <id from /v1/models> \
      [--prompt-file some_client_neutral_file.txt] [--max-tokens 512] [--reps 3]
Without --prompt-file it uses a short coding prompt (the #4140 shape, ~120 tokens).
With --prompt-file it wraps that file's text in a review request (our task shape).
NO client (Secuura/Datasec) content goes in --prompt-file.
"""
import argparse, json, time, uuid, urllib.request

SHORT = ("Write a Python function parse_duration(s) that converts strings like '1h30m', "
         "'45s', '2h' and '10m' into seconds, with a docstring and three asserts.")


def run(url, model, text, max_tokens):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": text}],
        "max_tokens": max_tokens,
        "temperature": 0, "top_p": 1,
        "stream": True, "stream_options": {"include_usage": True},
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(url.rstrip("/") + "/v1/chat/completions",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time(); t_first = t_last = None; usage = {}; finish = None
    with urllib.request.urlopen(req, timeout=3600) as r:
        for raw in r:
            line = raw.decode().strip()
            if not line.startswith("data:") or line == "data: [DONE]":
                continue
            ev = json.loads(line[5:])
            if ev.get("usage"):
                usage = ev["usage"]
            for ch in ev.get("choices", []):
                d = ch.get("delta", {})
                if d.get("content") or d.get("reasoning_content") or d.get("reasoning"):
                    now = time.time(); t_first = t_first or now; t_last = now
                finish = ch.get("finish_reason") or finish
    ct = usage.get("completion_tokens", 0)
    dec = (ct - 1) / (t_last - t_first) if t_first and t_last and t_last > t_first else 0
    return {"prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": ct,
            "cached": (usage.get("prompt_tokens_details") or {}).get("cached_tokens"),
            "ttft_s": round((t_first or t0) - t0, 2), "decode_tok_s": round(dec, 1),
            "finish": finish, "wall_s": round(time.time() - t0, 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:47780")
    ap.add_argument("--model", required=True)
    ap.add_argument("--prompt-file")
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--reps", type=int, default=3)
    a = ap.parse_args()
    base = SHORT
    if a.prompt_file:
        base = ("Review the following file. List the three most likely bugs with line "
                "references, then propose a fix for the first.\n\n" + open(a.prompt_file).read())
    for i in range(a.reps):
        text = f"[req {uuid.uuid4()}]\n" + base
        print("FRESH ", i, json.dumps(run(a.url, a.model, text, a.max_tokens)), flush=True)
        print("REPLAY", i, json.dumps(run(a.url, a.model, text, a.max_tokens)), flush=True)


if __name__ == "__main__":
    main()
