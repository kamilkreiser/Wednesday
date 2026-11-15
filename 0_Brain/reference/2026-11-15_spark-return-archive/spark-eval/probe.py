#!/usr/bin/env python3
"""Capability + throughput probes for the DeepSeek V4 Flash Spark deployment.

Isolated test of THIS model on THIS device. No external tiers, no ticket set.
Every number here is measured on the box, not quoted from the brief.
"""
import json, time, sys, urllib.request, urllib.error

BASE = "http://127.0.0.1:8888"
MODEL = "deepseek-v4-flash-0731"
RESULTS = []


def post(path, payload, timeout=1800):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = json.loads(r.read().decode())
    return body, time.time() - t0


def get(path, timeout=30):
    with urllib.request.urlopen(BASE + path, timeout=timeout) as r:
        return r.read().decode()


def record(name, ok, detail, **kw):
    RESULTS.append(dict(name=name, ok=ok, detail=detail, **kw))
    flag = "PASS" if ok else "FAIL"
    print(f"[{flag}] {name}: {detail}", flush=True)


def chat(prompt, max_tokens=512, temperature=0.0, **kw):
    p = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
         "max_tokens": max_tokens, "temperature": temperature}
    p.update(kw)
    return post("/v1/chat/completions", p)


def text_of(body):
    """Brief's gotcha #1: output may be in reasoning/reasoning_content, not content."""
    msg = body["choices"][0]["message"]
    return msg.get("content") or "", msg.get("reasoning_content") or msg.get("reasoning") or ""


# ---------------------------------------------------------------- 1. identity
def t_identity():
    try:
        models = json.loads(get("/v1/models"))
        ids = [m["id"] for m in models.get("data", [])]
        record("served model id", bool(ids), f"{ids}", ids=ids)
    except Exception as e:
        record("served model id", False, repr(e))


# ------------------------------------------------- 2. reasoning-field placement
def t_reasoning_field():
    try:
        body, _ = chat("Reply with exactly the word: pong", max_tokens=2048)
        content, reasoning = text_of(body)
        where = ("content" if content.strip() else
                 "reasoning_content ONLY - clients reading .content see EMPTY" if reasoning.strip()
                 else "NEITHER")
        record("reasoning field placement", bool(content.strip() or reasoning.strip()),
               where, content_len=len(content), reasoning_len=len(reasoning),
               content_preview=content[:200], reasoning_preview=reasoning[:200])
    except Exception as e:
        record("reasoning field placement", False, repr(e))


# ------------------------------------------------------------- 3. decode speed
def t_decode(n=3):
    """Measured tok/s on code generation. Brief claims 34-39, median 38.12."""
    rates = []
    prompt = ("Write a complete Python implementation of an LRU cache with get/put, "
              "type hints, docstrings, and three unit tests. Output only code.")
    for i in range(n):
        try:
            body, dt = chat(prompt, max_tokens=800, temperature=0.0)
            u = body.get("usage", {})
            out = u.get("completion_tokens") or 0
            if out and dt > 0:
                rates.append(out / dt)
                print(f"    trial {i+1}: {out} tok in {dt:.1f}s = {out/dt:.2f} tok/s", flush=True)
        except Exception as e:
            print(f"    trial {i+1} failed: {e!r}", flush=True)
    if rates:
        rates.sort()
        med = rates[len(rates) // 2]
        record("decode tok/s (code)", True,
               f"median {med:.2f} tok/s over {len(rates)} trials (brief: 38.12)",
               median=med, all=rates)
    else:
        record("decode tok/s (code)", False, "no successful trials")


# ------------------------------------------------------------ 4. prefill speed
def t_prefill(approx_tokens=16000):
    """Prefill rate on a large salted prompt. Brief claims ~1,055-1,239 tok/s."""
    filler = " ".join(f"item{i}" for i in range(approx_tokens))
    prompt = f"Here is a list:\n{filler}\n\nReply with only the word: done"
    try:
        body, dt = chat(prompt, max_tokens=8, temperature=0.0)
        u = body.get("usage", {})
        pt = u.get("prompt_tokens") or 0
        record("prefill tok/s", bool(pt),
               f"{pt} prompt tokens in {dt:.1f}s = {pt/dt:.0f} tok/s" if dt > 0 else "n/a",
               prompt_tokens=pt, seconds=dt, rate=(pt / dt if dt else 0))
    except Exception as e:
        record("prefill tok/s", False, repr(e))


# ------------------------------------------------------------- 5. code quality
def t_code_correctness():
    """Does generated code actually run? Executed, not eyeballed."""
    prompt = ("Write a Python function `solve(nums, target)` returning indices of the two "
              "numbers summing to target. Output ONLY the function, no markdown fences, no tests.")
    try:
        body, _ = chat(prompt, max_tokens=1200, temperature=0.0)
        content, reasoning = text_of(body)
        code = (content or reasoning)
        if "```" in code:
            code = code.split("```")[1]
            if code.startswith("python"):
                code = code[len("python"):]
        ns = {}
        exec(code, ns)
        got = ns["solve"]([2, 7, 11, 15], 9)
        ok = sorted(got) == [0, 1]
        record("generated code executes correctly", ok,
               f"solve([2,7,11,15],9) -> {got} (expect [0,1])", returned=str(got))
    except Exception as e:
        record("generated code executes correctly", False, repr(e))


# -------------------------------------------------------------- 6. tool calls
def t_tool_calls():
    """Must arrive as structured tool_calls, not raw text in content."""
    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {"type": "object",
                           "properties": {"city": {"type": "string"}},
                           "required": ["city"]},
        },
    }]
    try:
        body, _ = post("/v1/chat/completions", {
            "model": MODEL,
            "messages": [{"role": "user", "content": "What's the weather in Sydney? Use the tool."}],
            "tools": tools, "tool_choice": "auto", "max_tokens": 512, "temperature": 0.0,
        })
        msg = body["choices"][0]["message"]
        tc = msg.get("tool_calls")
        if tc:
            record("structured tool_calls", True,
                   f"{tc[0]['function']['name']}({tc[0]['function']['arguments']})", raw=tc)
        else:
            record("structured tool_calls", False,
                   "NO tool_calls field - arrived as text (template/parser problem)",
                   content=(msg.get('content') or '')[:300])
    except Exception as e:
        record("structured tool_calls", False, repr(e))


# ------------------------------------------------------- 7. KV pool / capacity
def t_kv_pool():
    """Settle the KV-pool question from server metrics rather than the brief."""
    try:
        m = get("/metrics", timeout=30)
        keep = [l for l in m.splitlines()
                if any(k in l for k in ("cache_config_info", "kv_cache", "num_gpu_blocks",
                                        "max_model_len", "gpu_cache_usage"))
                and not l.startswith("# HELP")]
        record("KV pool / cache metrics", bool(keep),
               f"{len(keep)} metric lines captured", lines=keep[:25])
        for l in keep[:15]:
            print("     ", l[:200], flush=True)
    except Exception as e:
        record("KV pool / cache metrics", False, repr(e))


def main():
    print(f"=== probing {BASE} at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} ===\n", flush=True)
    for fn in (t_identity, t_reasoning_field, t_kv_pool, t_decode,
               t_prefill, t_code_correctness, t_tool_calls):
        print(f"--- {fn.__name__} ---", flush=True)
        try:
            fn()
        except Exception as e:
            record(fn.__name__, False, f"harness error: {e!r}")
        print(flush=True)
    out = "/home/datasec-rd/spark-eval/results.json"
    with open(out, "w") as f:
        json.dump(RESULTS, f, indent=2)
    n_ok = sum(1 for r in RESULTS if r["ok"])
    print(f"=== {n_ok}/{len(RESULTS)} passed; raw -> {out} ===")


if __name__ == "__main__":
    main()
