#!/usr/bin/env python3
"""Provider-agnostic runner: same 10 tasks, same hidden suites, same 2-round
pipeline, against DeepSeek (vLLM), Ornith (Ollama) or Claude (Anthropic API).

  PROVIDER=deepseek  python3 runner.py
  PROVIDER=ollama    python3 runner.py
  PROVIDER=anthropic python3 runner.py     (needs ANTHROPIC_API_KEY)
"""
import json, os, sys, time, urllib.request, urllib.error

sys.path.insert(0, "/home/datasec-rd/spark-eval")
from suite10 import T, strip_fences, score   # tasks + scoring, unchanged


import signal
class _Timeout(Exception): pass
def _alarm(sig, frm): raise _Timeout("exceeded time limit")
class limit:
    """Watchdog: model-generated code can contain infinite loops."""
    def __init__(self, secs): self.secs = secs
    def __enter__(self):
        signal.signal(signal.SIGALRM, _alarm); signal.alarm(self.secs)
    def __exit__(self, *a):
        signal.alarm(0); return False


# Authoritative per-task test counts (from complete runs). A task that errors or
# hangs must score 0 out of its FULL count, not drop out of the denominator --
# otherwise totals across providers are not comparable.
N_TESTS = {"regex-engine":19,"topo-scheduler":12,"interval-set":18,"ttl-lru-cache":13,
           "jsonpath":14,"expr-evaluator":22,"fuzzy-trie":15,"semver-resolver":16,
           "line-diff":13,"state-machine":17}

PROVIDER = os.environ.get("PROVIDER", "deepseek")

CFG = {
    "deepseek": dict(url="http://127.0.0.1:8888/v1/chat/completions",
                     model="deepseek-v4-flash-0731", kind="openai",
                     extra={"chat_template_kwargs": {"thinking": False}}),
    "ollama":   dict(url="http://127.0.0.1:11434/v1/chat/completions",
                     model=os.environ.get("OLLAMA_MODEL", "ornith:35b"),
                     kind="openai", extra={"reasoning_effort": "none"}),
    "anthropic": dict(url="https://api.anthropic.com/v1/messages",
                      model=os.environ.get("ANTHROPIC_MODEL", "claude-opus-5"),
                      kind="anthropic", extra={}),
}[PROVIDER]


def ask(prompt, max_tokens=4096):
    if CFG["kind"] == "openai":
        payload = {"model": CFG["model"],
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": max_tokens, "temperature": 0.0}
        payload.update(CFG["extra"])
        headers = {"Content-Type": "application/json"}
    else:
        payload = {"model": CFG["model"], "max_tokens": max_tokens,
                   "temperature": 0.0,
                   "messages": [{"role": "user", "content": prompt}]}
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        headers = {"Content-Type": "application/json",
                   "x-api-key": key, "anthropic-version": "2023-06-01"}

    req = urllib.request.Request(CFG["url"], data=json.dumps(payload).encode(),
                                 headers=headers)
    t0 = time.time()
    try:
        raw = urllib.request.urlopen(req, timeout=3600).read().decode()
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %s: %s" % (e.code, e.read().decode()[:300]))
    dt = time.time() - t0
    b = json.loads(raw)

    if CFG["kind"] == "openai":
        c = b["choices"][0]; m = c["message"]
        text = m.get("content") or m.get("reasoning_content") or m.get("reasoning") or ""
        finish = c["finish_reason"]
        out_tok = b.get("usage", {}).get("completion_tokens", 0)
    else:
        text = "".join(p.get("text", "") for p in b.get("content", [])
                       if p.get("type") == "text")
        finish = "length" if b.get("stop_reason") == "max_tokens" else "stop"
        out_tok = b.get("usage", {}).get("output_tokens", 0)
    return text, finish, out_tok, dt


def attempt(prompt, tests, budget):
    try:
        text, finish, tok, dt = ask(prompt, budget)
    except Exception as e:
        return None, "request failed: %s" % (e,), 0, 0.0, None
    if finish == "length":
        return None, "TRUNCATED at %d tokens" % tok, tok, dt, None
    code = strip_fences(text)
    ns = {}
    try:
        with limit(20):
            exec(compile(code, "<gen>", "exec"), ns)
    except _Timeout:
        return None, "HUNG: module-level code exceeded 20s", tok, dt, code
    except Exception as e:
        return None, "import error: %s: %s" % (type(e).__name__, e), tok, dt, code
    try:
        with limit(60):
            p, n, res = score(ns, tests)
    except _Timeout:
        return None, "HUNG: tests exceeded 60s (infinite loop in generated code)", tok, dt, code
    except Exception as e:
        return None, "suite crashed: %s: %s" % (type(e).__name__, e), tok, dt, code
    return (p, n, res), None, tok, dt, code


def main():
    print("=== PROVIDER=%s  MODEL=%s ===" % (PROVIDER, CFG["model"]), flush=True)
    out = []
    for i, t in enumerate(T, 1):
        print("\n--- %d/%d %s" % (i, len(T), t["name"]), flush=True)
        r1, err1, tok1, dt1, code1 = attempt(t["prompt"], t["tests"], 4096)
        if r1 is None:
            print("   round1 ERROR: %s (%.1fs)" % (err1, dt1), flush=True)
            out.append(dict(task=t["name"], r1=0, r2=0, n=N_TESTS[t["name"]],
                            err=err1, t1=dt1, t2=0.0, tok1=tok1, tok2=0))
            continue
        p1, n, res1 = r1
        print("   round1: %d/%d (%d tok, %.1fs)" % (p1, n, tok1, dt1), flush=True)
        for nm, ok, d in res1:
            if not ok: print("      FAIL %-34s %s" % (nm, d), flush=True)
        if p1 == n:
            out.append(dict(task=t["name"], r1=p1, r2=p1, n=n, err=None,
                            t1=dt1, t2=0.0, tok1=tok1, tok2=0))
            continue
        fails = "\n".join("  - %s: %s" % (nm, d) for nm, ok, d in res1 if not ok)
        fb = ("Your implementation of the following task failed %d of %d hidden tests.\n\n"
              "ORIGINAL TASK\n-------------\n%s\n\nYOUR IMPLEMENTATION\n"
              "-------------------\n%s\n\nFAILING TESTS (actual vs expected)\n"
              "----------------------------------\n%s\n\nRewrite the COMPLETE module "
              "fixing these failures while keeping everything that already passes. "
              "Output ONLY the Python module source, no fences, no commentary.\n"
              % (n - p1, n, t["prompt"], code1, fails))
        r2, err2, tok2, dt2, _ = attempt(fb, t["tests"], 6144)
        if r2 is None:
            print("   round2 ERROR: %s" % err2, flush=True)
            out.append(dict(task=t["name"], r1=p1, r2=p1, n=n, err=err2,
                            t1=dt1, t2=dt2, tok1=tok1, tok2=tok2))
            continue
        p2 = r2[0]
        print("   round2: %d/%d (%d tok, %.1fs)  delta %+d" % (p2, n, tok2, dt2, p2 - p1), flush=True)
        for nm, ok, d in r2[2]:
            if not ok: print("      STILL %-34s %s" % (nm, d), flush=True)
        out.append(dict(task=t["name"], r1=p1, r2=p2, n=n, err=None,
                        t1=dt1, t2=dt2, tok1=tok1, tok2=tok2))

    tot1 = sum(r["r1"] or 0 for r in out)
    tot2 = sum((r["r2"] if r["r2"] is not None else (r["r1"] or 0)) for r in out)
    totn = sum(r["n"] or 0 for r in out)
    secs = sum((r["t1"] or 0) + (r["t2"] or 0) for r in out)
    print("\n=== %s TOTAL: round1 %d/%d (%.1f%%)  round2 %d/%d (%.1f%%)  %.0fs ==="
          % (PROVIDER, tot1, totn, 100.0 * tot1 / totn if totn else 0,
             tot2, totn, 100.0 * tot2 / totn if totn else 0, secs))
    path = "/home/datasec-rd/spark-eval/results_%s.json" % PROVIDER
    json.dump(out, open(path, "w"), indent=2)
    print("raw -> %s" % path)


if __name__ == "__main__":
    main()
