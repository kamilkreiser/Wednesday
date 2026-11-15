#!/usr/bin/env python3
"""Run the HARD suite. PROVIDER=deepseek (local HTTP) or opus (claude CLI)."""
import json, os, signal, subprocess, sys, time, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hard import T

PROVIDER = os.environ.get("PROVIDER", "deepseek")
OPUS_MODEL = os.environ.get("OPUS_MODEL", "claude-opus-5")

class _TO(Exception): pass
def _alarm(s, f): raise _TO()
class limit:
    def __init__(self, s): self.s = s
    def __enter__(self): signal.signal(signal.SIGALRM, _alarm); signal.alarm(self.s)
    def __exit__(self, *a): signal.alarm(0); return False


class _Stub:
    def __init__(self, *a, **k): raise RuntimeError("stub")
    def __getattr__(self, n): raise RuntimeError("stub")
class _StubNS(dict):
    def __missing__(self, k): return _Stub

def n_tests(t):
    """Count assertions by running the suite against a stub namespace."""
    try:
        with limit(30):
            return len(t["tests"](_StubNS(), ""))
    except Exception:
        return 0


def strip_fences(code):
    if "```" in code:
        parts = code.split("```")
        cand = max((p for i, p in enumerate(parts) if i % 2 == 1), key=len, default=code)
        code = cand
        if code.lstrip().lower().startswith("python"): code = code.lstrip()[6:]
    return code


def ask(prompt, max_tokens):
    t0 = time.time()
    if PROVIDER == "opus":
        p = subprocess.run(["claude", "-p", "--model", OPUS_MODEL, "--allowed-tools", ""],
                           input=prompt, capture_output=True, text=True, timeout=2400)
        if p.returncode != 0:
            raise RuntimeError("claude rc=%s %s" % (p.returncode, (p.stderr or "")[:200]))
        return p.stdout, "stop", 0, time.time() - t0
    payload = {"model": "deepseek-v4-flash-0731",
               "messages": [{"role": "user", "content": prompt}],
               "max_tokens": max_tokens, "temperature": 0.0,
               "chat_template_kwargs": {"thinking": False}}
    req = urllib.request.Request("http://127.0.0.1:8888/v1/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        raw = urllib.request.urlopen(req, timeout=3600).read().decode()
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %s: %s" % (e.code, e.read().decode()[:200]))
    b = json.loads(raw); c = b["choices"][0]; m = c["message"]
    text = m.get("content") or m.get("reasoning_content") or m.get("reasoning") or ""
    return text, c["finish_reason"], b["usage"]["completion_tokens"], time.time() - t0


def attempt(prompt, t, budget):
    try:
        text, finish, tok, dt = ask(prompt, budget)
    except Exception as e:
        return None, "request failed: %s" % (e,), 0, 0.0, None
    if finish == "length":
        return None, "TRUNCATED at %d tokens" % tok, tok, dt, None
    code = strip_fences(text)
    ns = {}
    try:
        with limit(30):
            exec(compile(code, "<gen>", "exec"), ns)
    except _TO:
        return None, "HUNG: module import >30s", tok, dt, code
    except Exception as e:
        return None, "import error: %s: %s" % (type(e).__name__, e), tok, dt, code
    try:
        with limit(180):
            res = t["tests"](ns, code)
    except _TO:
        return None, "HUNG: tests >180s (likely O(n) instead of O(log n), or infinite loop)", tok, dt, code
    except Exception as e:
        return None, "suite crashed: %s: %s" % (type(e).__name__, e), tok, dt, code
    p = sum(1 for _, ok, _ in res if ok)
    return (p, len(res), res), None, tok, dt, code


def main():
    label = OPUS_MODEL if PROVIDER == "opus" else "deepseek-v4-flash-0731"
    print("=== HARD SUITE  provider=%s  model=%s ===" % (PROVIDER, label), flush=True)
    NT = {t["name"]: n_tests(t) for t in T}
    print("   test counts: %s  (total %d)" % (NT, sum(NT.values())), flush=True)
    out = []
    for i, t in enumerate(T, 1):
        print("\n--- %d/%d %s" % (i, len(T), t["name"]), flush=True)
        r1, err1, tok1, dt1, code1 = attempt(t["prompt"], t, 8192)
        if r1 is None:
            print("   round1 ERROR: %s (%.1fs)" % (err1, dt1), flush=True)
            out.append(dict(task=t["name"], r1=0, r2=0, n=NT[t["name"]], err=err1, t1=dt1, t2=0.0))
            continue
        p1, n, res1 = r1
        print("   round1: %d/%d (%d tok, %.1fs)" % (p1, n, tok1, dt1), flush=True)
        for nm, ok, d in res1:
            if not ok: print("      FAIL %-46s %s" % (nm, d[:90]), flush=True)
        if p1 == n:
            out.append(dict(task=t["name"], r1=p1, r2=p1, n=n, err=None, t1=dt1, t2=0.0)); continue
        fails = "\n".join("  - %s: %s" % (nm, d) for nm, ok, d in res1 if not ok)
        fb = ("Your implementation of the following task failed %d of %d hidden tests.\n\n"
              "ORIGINAL TASK\n-------------\n%s\n\nYOUR IMPLEMENTATION\n-------------------\n%s\n\n"
              "FAILING TESTS\n-------------\n%s\n\nRewrite the COMPLETE module fixing these "
              "while keeping what passes. Output ONLY the Python module source, no fences.\n"
              % (n - p1, n, t["prompt"], code1, fails))
        r2, err2, tok2, dt2, _ = attempt(fb, t, 12288)
        if r2 is None:
            print("   round2 ERROR: %s" % err2, flush=True)
            out.append(dict(task=t["name"], r1=p1, r2=p1, n=n, err=err2, t1=dt1, t2=dt2)); continue
        p2 = r2[0]
        print("   round2: %d/%d (%.1fs)  delta %+d" % (p2, n, dt2, p2 - p1), flush=True)
        for nm, ok, d in r2[2]:
            if not ok: print("      STILL %-45s %s" % (nm, d[:90]), flush=True)
        out.append(dict(task=t["name"], r1=p1, r2=p2, n=n, err=None, t1=dt1, t2=dt2))

    t1 = sum(r["r1"] for r in out); t2 = sum(r["r2"] for r in out); tn = sum(r["n"] for r in out)
    secs = sum(r["t1"] + r["t2"] for r in out)
    print("\n=== %s HARD TOTAL: round1 %d/%d (%.1f%%)  round2 %d/%d (%.1f%%)  %.0fs ==="
          % (label, t1, tn, 100.0*t1/tn if tn else 0, t2, tn, 100.0*t2/tn if tn else 0, secs), flush=True)
    slug = "opus5" if PROVIDER == "opus" else "deepseek"
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "hard_results_%s.json" % slug), "w"), indent=2)


if __name__ == "__main__":
    main()
