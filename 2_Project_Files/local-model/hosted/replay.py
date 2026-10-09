#!/usr/bin/env python3
"""hosted/replay.py — replay the Spark's Secuura tasks on hosted models through OpenRouter (2026-10-09).

Kam, live board 17:26, card wed-hosted-replay-key-and-code-1009 = a: replay our Spark local-model tasks on hosted
models via OpenRouter; Secuura code goes ONLY to zero-retention providers; US$5 cap.

For each row of spark/done.md that has a run dir, it re-sends EXACTLY the messages lib/spark_call.py sent:
  system = lm_call.SYSTEM_PREAMBLE + "\\n\\n" + spark-kit/01_FOR_THE_LOCAL_MODEL.md   (imported / read, never copied)
  user   = "## TASK\\n" + task.strip() + "\\n\\n## INPUT (JSON)\\n" + input.strip() + "\\n"
from the Spark run dir's own input.json (and its task.md for the *2 tiers). Before any request is built it PROVES the
reconstruction against what the Spark recorded: sha256(task + input) == meta.sha256_task_plus_input AND
len(system) + len(user) in UTF-8 bytes == meta.prompt_bytes; a mismatch refuses that task (rc 2 for it).

Every request carries provider routing {"only": [<pinned provider>], "allow_fallbacks": false, "zdr": true,
"data_collection": "deny"} (+ "quantizations": ["fp8"]); send() REFUSES a body without all four (assert_routing).
A budget guard (state/budget.json, all models together) refuses the next request when spent + this request's
WORST-CASE cost would exceed HOSTED_BUDGET_USD (default 5.00).

Usage:
  replay.py --model mimo|glm|deepseek [--dry-run] [--only TAG[,TAG...]] [--limit N] [--keep-clone] [--no-check]
Exit: 0 all done · 1 at least one model FAIL verdict · 2 refused (no key, routing, budget, byte-identity) ·
      4 HTTP/shape failure · 5 HARNESS (checker leg) · 64 usage.
The key is read from 4_Credentials/.env by name (OPENROUTER_API_KEY) and is never printed or written.
Python 3 stdlib only.
"""
import argparse
import datetime
import fcntl
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
WED = os.path.normpath(os.path.join(LM, "..", ".."))
sys.path.insert(0, os.path.join(LM, "lib"))
from lm_call import SYSTEM_PREAMBLE  # noqa: E402  — the Spark's own preamble, imported
from spark_call import DIFF_GRAMMAR, KIT_CONTRACT  # noqa: E402  — the Spark's own contract path + diff grammar

ENV_FILE = os.environ.get("HOSTED_ENV_FILE", os.path.join(WED, "4_Credentials", ".env"))
KEY_NAME = "OPENROUTER_API_KEY"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
SPARK_DONE = os.path.join(LM, "spark", "done.md")
STATE = os.environ.get("HOSTED_STATE", os.path.join(HERE, "state"))
RUNS = os.environ.get("HOSTED_RUNS", os.path.join(HERE, "runs"))
WORK = os.environ.get("HOSTED_WORK", os.path.join(HERE, "work"))
DONE_DIR = os.environ.get("HOSTED_DONE_DIR", HERE)
DEFAULT_CAP = 5.00
PROMPT_TOKEN_MARGIN = 1.30   # a different tokenizer may count the same bytes as more tokens than the Spark's did

# Prices are USD per token, read from HOSTED_API.md and re-confirmed by GET /api/v1/models/<id>/endpoints 2026-10-09.
MODELS = {
    "mimo": {
        "id": "xiaomi/mimo-v2.6-flash", "provider": "deepinfra", "tag": "deepinfra/fp8",
        "price_in": 0.14e-6, "price_out": 0.28e-6, "max_tokens": 16384,
        # thinking OFF: OpenRouter's unified field, plus the provider-native field HOSTED_API.md cites (litellm blog)
        "extra": {"reasoning": {"enabled": False}, "thinking": {"type": "disabled"}},
        "thinking_expected": False,
    },
    "glm": {
        "id": "z-ai/glm-5.3-flash", "provider": "z-ai", "tag": "z-ai/fp8",
        "price_in": 0.15e-6, "price_out": 0.50e-6, "max_tokens": 32768,
        # thinking CANNOT be disabled on GLM-5.3 (docs.z.ai; OpenRouter mandatory:true) -> the lowest effort, "low".
        # max_tokens doubled vs the Spark's 16384 because reasoning tokens spend the same budget.
        "extra": {"reasoning": {"effort": "low"}},
        "thinking_expected": True,
    },
    "deepseek": {
        "id": "deepseek/deepseek-v4-flash-0731", "provider": "deepinfra", "tag": "deepinfra/fp8",
        "price_in": 0.06e-6, "price_out": 0.18e-6, "max_tokens": 16384,
        "extra": {"reasoning": {"effort": "none"}},
        "thinking_expected": False,
    },
}
REQUIRED_ROUTING = ("only", "allow_fallbacks", "zdr", "data_collection")


def _wtext(path, text, mode="w"):
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        f.write(text)


def _wjson(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)


def _rtext(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _rjson(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class Refused(Exception):
    """A refusal: nothing was sent."""


# ------------------------------------------------------------------------------------------------ key
def read_key(env_file=None):
    """Return the key's value from the env file, or None. Never prints it."""
    path = env_file or ENV_FILE
    try:
        lines = _rtext(path).splitlines()
    except OSError:
        return None
    for line in lines:
        s = line.strip()
        if s.startswith("export "):
            s = s[7:].lstrip()
        if s.startswith(KEY_NAME + "="):
            v = s[len(KEY_NAME) + 1:].strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
                v = v[1:-1]
            return v or None
    return None


# ------------------------------------------------------------------------------------------------ tasks
def spark_rows(done_path=SPARK_DONE):
    """Rows of spark/done.md that have a run dir (REFUSED rows have none)."""
    rows = []
    for line in _rtext(done_path).splitlines():
        if not line.startswith("| 20"):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 9 or c[7] in ("-", "") or not os.path.isdir(c[7]):
            continue
        rows.append({"when": c[0], "tag": c[1], "spark_verdict": c[2], "tokens": c[5], "golden": c[6], "run": c[7]})
    return rows


def task_path_for(run, tier, inp):
    """The task.md the Spark round sent (round.sh step 6's choice)."""
    if tier in ("code_patch2", "bash_patch2"):
        return os.path.join(run, "task.md")
    if tier == "bash_patch" and inp.get("self_testing"):
        return os.path.join(LM, "tasks", "bash_patch", "task_selftest.md")
    return os.path.join(LM, "tasks", tier, "task.md")


def system_prompt():
    contract = _rtext(KIT_CONTRACT).strip()
    return SYSTEM_PREAMBLE + "\n\n" + contract


def build_messages(run):
    """Rebuild the Spark's messages for one run dir and PROVE them byte-identical to what it sent.
    Returns (messages, info). Raises Refused on any mismatch."""
    rj = _rjson(os.path.join(run, "round.json"))
    meta = _rjson(os.path.join(run, "out.md.meta.json"))
    input_text = _rtext(os.path.join(run, "input.json"))
    inp = json.loads(input_text)
    tier = rj["tier"]
    tpath = task_path_for(run, tier, inp)
    task_text = _rtext(tpath)
    sha = hashlib.sha256((task_text + input_text).encode("utf-8")).hexdigest()
    if sha != meta.get("sha256_task_plus_input"):
        raise Refused(f"byte-identity: sha256(task+input) {sha[:12]} != the Spark's {str(meta.get('sha256_task_plus_input'))[:12]} "
                      f"({tpath} changed since the round?)")
    system = system_prompt()
    user = "## TASK\n" + task_text.strip() + "\n\n## INPUT (JSON)\n" + input_text.strip() + "\n"
    pb = len(system.encode("utf-8")) + len(user.encode("utf-8"))
    if pb != meta.get("prompt_bytes"):
        raise Refused(f"byte-identity: prompt_bytes {pb} != the Spark's {meta.get('prompt_bytes')} (system prompt changed since the round?)")
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    info = {"tier": tier, "tip": rj["tip"], "brief_dir": rj.get("brief_dir"), "task_path": tpath,
            "sha256_task_plus_input": sha, "prompt_bytes": pb,
            "spark_prompt_tokens": meta.get("prompt_eval_count") or 0, "spark_completion_tokens": meta.get("eval_count") or 0,
            "spark_result": rj.get("spark_result") or rj.get("checker_result"), "spark_verdict": rj.get("verdict"),
            "messages_sha256": hashlib.sha256(json.dumps(msgs, ensure_ascii=False).encode("utf-8")).hexdigest()}
    return msgs, info


def build_body(model_key, messages):
    m = MODELS[model_key]
    body = {
        "model": m["id"],
        "messages": messages,
        "max_tokens": m["max_tokens"],
        "temperature": 0,
        "provider": {"only": [m["provider"]], "allow_fallbacks": False, "zdr": True, "data_collection": "deny",
                     "quantizations": ["fp8"]},
        "usage": {"include": True},
    }
    body.update(json.loads(json.dumps(m["extra"])))
    return body


def assert_routing(body, model_key):
    """Refuse unless the body pins zero-retention routing. Called by send() immediately before the network."""
    p = body.get("provider")
    if not isinstance(p, dict):
        raise Refused("routing: request has no provider object")
    missing = [k for k in REQUIRED_ROUTING if k not in p]
    if missing:
        raise Refused(f"routing: provider is missing {missing} — Secuura code goes only to pinned zero-retention providers")
    want = MODELS[model_key]["provider"]
    if p["only"] != [want]:
        raise Refused(f"routing: only={p['only']!r}, must be exactly [{want!r}]")
    if p["allow_fallbacks"] is not False:
        raise Refused("routing: allow_fallbacks must be false")
    if p["zdr"] is not True:
        raise Refused("routing: zdr must be true")
    if p["data_collection"] != "deny":
        raise Refused("routing: data_collection must be \"deny\"")
    if body.get("model") != MODELS[model_key]["id"]:
        raise Refused(f"routing: model {body.get('model')!r} is not {MODELS[model_key]['id']!r}")


# ------------------------------------------------------------------------------------------------ budget
def worst_case_usd(model_key, spark_prompt_tokens):
    m = MODELS[model_key]
    return spark_prompt_tokens * PROMPT_TOKEN_MARGIN * m["price_in"] + m["max_tokens"] * m["price_out"]


def expected_usd(model_key, spark_prompt_tokens, spark_completion_tokens):
    m = MODELS[model_key]
    return spark_prompt_tokens * m["price_in"] + spark_completion_tokens * m["price_out"]


class Budget:
    """state/budget.json: one running total across ALL models. A request is RESERVED at its worst case before it is
    sent and SETTLED to its real cost after; a crash between the two leaves the worst case counted (conservative)."""

    def __init__(self, path, cap):
        self.path, self.cap = path, cap

    def _locked(self, fn):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path + ".lock", "w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            try:
                d = _rjson(self.path) if os.path.exists(self.path) else {"entries": []}
                r = fn(d)
                d["total_usd"] = round(sum(e["usd"] for e in d["entries"]), 8)
                d["cap_usd_last_seen"] = self.cap
                tmp = self.path + ".tmp"
                _wjson(tmp, d)
                os.replace(tmp, self.path)
                return r
            finally:
                fcntl.flock(lk, fcntl.LOCK_UN)

    def total(self):
        if not os.path.exists(self.path):
            return 0.0
        return sum(e["usd"] for e in _rjson(self.path)["entries"])

    def reserve(self, model_key, tag, worst):
        def fn(d):
            spent = sum(e["usd"] for e in d["entries"])
            if spent + worst > self.cap + 1e-12:
                raise Refused(f"BUDGET: spent ${spent:.4f} + this request's worst case ${worst:.4f} > cap ${self.cap:.2f} "
                              f"(HOSTED_BUDGET_USD) — no request sent")
            rid = f"{model_key}:{tag}:{time.time():.6f}"
            d["entries"].append({"id": rid, "when": datetime.datetime.now().isoformat(timespec="seconds"),
                                 "model": model_key, "tag": tag, "usd": worst, "state": "reserved-worst-case"})
            return rid
        return self._locked(fn)

    def settle(self, rid, usd, source, usage):
        def fn(d):
            for e in d["entries"]:
                if e["id"] == rid:
                    e.update({"usd": usd, "state": "settled", "source": source,
                              "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens")})
                    return
            raise RuntimeError(f"budget entry {rid} vanished")
        self._locked(fn)


def cost_of(model_key, usage):
    """(usd, source): OpenRouter's usage.cost when present, else tokens x HOSTED_API.md prices."""
    c = usage.get("cost")
    if isinstance(c, (int, float)) and not isinstance(c, bool):
        return float(c), "usage.cost"
    m = MODELS[model_key]
    pt, ct = usage.get("prompt_tokens"), usage.get("completion_tokens")
    if not isinstance(pt, int) or not isinstance(ct, int):
        raise ValueError("usage has neither cost nor integer prompt/completion tokens")
    return pt * m["price_in"] + ct * m["price_out"], "computed(tokens x HOSTED_API.md prices)"


# ------------------------------------------------------------------------------------------------ network
def _http_post(url, data, headers, timeout):  # the ONE network call; tests replace it
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def send(body, model_key, key, budget, tag, worst, post=None):
    """Routing assert -> budget reserve -> POST -> settle. Returns (raw bytes, usd, source, wall)."""
    assert_routing(body, model_key)
    if not key:
        raise Refused(f"{KEY_NAME} is not set in {ENV_FILE}")
    rid = budget.reserve(model_key, tag, worst)
    post = post or _http_post
    t0 = time.time()
    raw = post(API_URL, json.dumps(body).encode("utf-8"),
               {"Content-Type": "application/json", "Authorization": "Bearer " + key,
                "X-Title": "Wednesday hosted replay"}, int(os.environ.get("HOSTED_HTTP_TIMEOUT", "1800")))
    wall = time.time() - t0
    try:
        j = json.loads(raw)
        usd, source = cost_of(model_key, j.get("usage") or {})
        budget.settle(rid, usd, source, j.get("usage") or {})
    except (ValueError, KeyError):
        usd, source = worst, "unknown-usage: worst case kept"
    return raw, usd, source, wall


# ------------------------------------------------------------------------------------------------ run dir
def new_run_dir(model_key, tag):
    day = datetime.date.today().isoformat()
    base = os.path.join(RUNS, model_key, f"hosted_{model_key}_{day}_{tag}")
    run, n = base, 2
    while os.path.exists(run):
        run, n = f"{base}-r{n}", n + 1
    os.makedirs(run)
    return run


def write_outputs(run, model_key, body, info, raw, wall, usd, source):
    """out.md / .meta.json / .raw.json in spark_call.py's shape (checker A1 reads meta.done_reason)."""
    out_path = os.path.join(run, "out.md")
    _wtext(out_path + ".raw.json", raw, "wb")
    j = json.loads(raw)
    if j.get("error"):
        raise ValueError(f"API error body: {json.dumps(j['error'])[:400]}")
    choice = j["choices"][0]
    msg = choice.get("message") or {}
    content = msg.get("content") or ""
    reasoning = msg.get("reasoning") or msg.get("reasoning_content") or ""
    finish = choice.get("finish_reason")
    usage = j.get("usage") or {}
    cleaned = content.strip()
    unfenced = False
    if cleaned and "```" not in cleaned and "~~~" not in cleaned and cleaned.startswith("--- "):
        if not [l for l in cleaned.split("\n") if l.strip() and not DIFF_GRAMMAR.match(l)]:
            unfenced = True
            cleaned = "```diff\n" + cleaned + "\n```"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned + ("\n" if not cleaned.endswith("\n") else ""))
    rtok = (usage.get("completion_tokens_details") or {}).get("reasoning_tokens")
    meta = {
        "backend": "openrouter", "model": body["model"], "provider_routing": body["provider"],
        "provider_served": j.get("provider"), "max_tokens": body["max_tokens"],
        "sampler": {"temperature": 0, "max_tokens": body["max_tokens"],
                    **{k: body[k] for k in ("reasoning", "thinking") if k in body}},
        "prompt_bytes": info["prompt_bytes"], "sha256_task_plus_input": info["sha256_task_plus_input"],
        "messages_sha256": info["messages_sha256"],
        "prompt_eval_count": usage.get("prompt_tokens"), "eval_count": usage.get("completion_tokens"),
        "reasoning_tokens": rtok, "usage": usage, "cost_usd": usd, "cost_source": source,
        "wall_clock_seconds": round(wall, 3), "thinking_expected": MODELS[model_key]["thinking_expected"],
        "thinking_chars": len(reasoning), "think_leak_in_content": ("<think>" in content or "</think>" in content),
        "finish_reason": finish, "done": finish is not None, "done_reason": finish,
        "unfenced_wrapped": unfenced, "content_chars": len(cleaned), "generation_id": j.get("id"),
        "system_prompt_files": ["lib/lm_call.py:SYSTEM_PREAMBLE", KIT_CONTRACT], "task_file": info["task_path"],
    }
    _wjson(out_path + ".meta.json", meta)
    return meta


def append_done(model_key, row):
    path = os.path.join(DONE_DIR, f"done_{model_key}.md")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# hosted/done_{model_key}.md — one row per hosted replay of a Spark task ({MODELS[model_key]['id']} via "
                    f"OpenRouter, pinned {MODELS[model_key]['tag']}, zdr) — newest at the bottom\n"
                    "| when | tag | verdict | model s | tokens (prompt+completion) | reasoning tok | cost USD | spark verdict | golden | run dir | spark run dir |\n"
                    "|---|---|---|---|---|---|---|---|---|---|---|\n")
    with open(path, "a", encoding="utf-8") as f:
        f.write("| " + " | ".join(str(x).replace("|", "/") for x in row) + " |\n")


# ------------------------------------------------------------------------------------------------ main
def main(argv=None, post=None):
    ap = argparse.ArgumentParser(prog="replay.py")
    ap.add_argument("--model", required=True, choices=sorted(MODELS))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="", help="comma-separated Spark run-dir basenames or tags")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--keep-clone", action="store_true")
    ap.add_argument("--no-check", action="store_true", help="skip the checker leg (debug only)")
    ap.add_argument("--done", default=SPARK_DONE)
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 64 if e.code else 0
    mk = a.model
    m = MODELS[mk]
    cap = float(os.environ.get("HOSTED_BUDGET_USD", DEFAULT_CAP))
    budget = Budget(os.path.join(STATE, "budget.json"), cap)

    rows = spark_rows(a.done)
    if a.only:
        want = set(x.strip() for x in a.only.split(",") if x.strip())
        rows = [r for r in rows if r["tag"] in want or os.path.basename(r["run"]) in want]
    if a.limit:
        rows = rows[:a.limit]

    key = read_key()
    if not a.dry_run and not key:
        print(f"replay: {KEY_NAME} is not in {ENV_FILE} — add it there (never on the command line); nothing sent")
        return 2

    # build + prove every request first; nothing is sent until all are built
    plan, refused = [], []
    for r in rows:
        try:
            msgs, info = build_messages(r["run"])
            body = build_body(mk, msgs)
            assert_routing(body, mk)
            plan.append((r, body, info))
        except Refused as e:
            refused.append((r, str(e)))
    exp = sum(expected_usd(mk, i["spark_prompt_tokens"], i["spark_completion_tokens"]) for _, _, i in plan)
    worst = sum(worst_case_usd(mk, i["spark_prompt_tokens"]) for _, _, i in plan)
    spent = budget.total()
    print(f"replay: model {mk} = {m['id']} pinned {m['tag']} · {len(plan)} request(s) built, {len(refused)} refused · "
          f"byte-identity proven for all {len(plan)} (sha256(task+input) + prompt_bytes vs the Spark's meta)")
    print(f"replay: PRE-FLIGHT estimate ${exp:.4f} (Spark's own token counts x {m['price_in']*1e6:.3f}/{m['price_out']*1e6:.3f} "
          f"per M) · worst case ${worst:.4f} (prompt x{PROMPT_TOKEN_MARGIN} + max_tokens {m['max_tokens']} every task) · "
          f"spent so far ${spent:.4f} of cap ${cap:.2f} (all models)")
    if mk == "glm":
        print("replay: NOTE glm thinks at effort=low (cannot be disabled); its output tokens are unmeasured — the estimate "
              "uses the Spark's thinking-OFF completion counts and is a FLOOR")
    for r, why in refused:
        print(f"replay: REFUSED {r['tag']}: {why}")

    if a.dry_run:
        dd = os.path.join(STATE, "dry", f"{mk}_{datetime.datetime.now():%Y%m%d-%H%M%S}")
        os.makedirs(dd, exist_ok=True)
        for r, body, info in plan:
            print(f"DRY {os.path.basename(r['run'])}: POST {API_URL} model={body['model']} provider={json.dumps(body['provider'])} "
                  f"{'reasoning=' + json.dumps(body.get('reasoning')) if 'reasoning' in body else ''}"
                  f"{' thinking=' + json.dumps(body['thinking']) if 'thinking' in body else ''} "
                  f"prompt_bytes={info['prompt_bytes']} est=${expected_usd(mk, info['spark_prompt_tokens'], info['spark_completion_tokens']):.5f}")
            _wjson(os.path.join(dd, os.path.basename(r["run"]) + ".request.json"), body)
        print(f"replay: DRY-RUN — {len(plan)} request bodies written to {dd}; key {'present' if key else 'ABSENT'}; "
              f"zero network calls")
        return 2 if refused else 0

    worst_rc = 2 if refused else 0
    for r, body, info in plan:
        tag = os.path.basename(r["run"])
        wc = worst_case_usd(mk, info["spark_prompt_tokens"])
        run = new_run_dir(mk, tag)
        shutil.copyfile(os.path.join(r["run"], "input.json"), os.path.join(run, "input.json"))  # byte copy
        shutil.copyfile(info["task_path"], os.path.join(run, "task.md"))
        req_record = dict(body)
        _wjson(os.path.join(run, "request.json"), req_record)  # no key in body
        try:
            raw, usd, source, wall = send(body, mk, key, budget, tag, wc, post=post)
        except Refused as e:
            print(f"replay: REFUSED {tag}: {e}")
            _wtext(os.path.join(run, "run.log"), f"REFUSED: {e}\n")
            return 2  # budget/routing refusal stops the drain
        except urllib.error.HTTPError as e:
            body_txt = e.read()[:1500]
            _wtext(os.path.join(run, "run.log"), f"HTTP {e.code}: {body_txt!r}\n")
            print(f"replay: HTTP {e.code} on {tag} (routing pinned; a 404/no-endpoints here means the zdr+only pin found "
                  f"no endpoint — NOT a model verdict): {body_txt[:300]!r}")
            return 4
        except (urllib.error.URLError, OSError) as e:
            _wtext(os.path.join(run, "run.log"), f"connection error: {e}\n")
            print(f"replay: connection error on {tag}: {e} (worst case stays charged in the budget)")
            return 4
        try:
            meta = write_outputs(run, mk, body, info, raw, wall, usd, source)
        except (ValueError, KeyError, IndexError) as e:
            _wtext(os.path.join(run, "run.log"), f"shape: {e}\n")
            print(f"replay: unexpected response on {tag}: {e}")
            return 4
        log = (f"hosted: ok model={body['model']} served_by={meta['provider_served']} wall={wall:.2f}s "
               f"prompt_tokens={meta['prompt_eval_count']} eval_count={meta['eval_count']} reasoning_tokens={meta['reasoning_tokens']} "
               f"cost=${usd:.5f} ({source}) done_reason={meta['finish_reason']} content_chars={meta['content_chars']}")
        _wtext(os.path.join(run, "run.log"), log + "\n")
        print(f"replay: {tag}: {log}")
        harness = None
        if not m["thinking_expected"] and (meta["thinking_chars"] or meta["think_leak_in_content"]):
            harness = "thinking was ON or leaked (requested off)"
        if meta["provider_served"] and m["provider"].replace("-", "").lower() not in str(meta["provider_served"]).replace(".", "").replace("-", "").lower():
            harness = f"served by {meta['provider_served']!r}, not the pinned {m['provider']}"
        verdict, golden, cres = "UNCHECKED", "-", ""
        if harness:
            verdict = "HARNESS"
            cres = harness
        elif not a.no_check:
            work = os.path.join(WORK, f"{os.path.basename(run)}_{datetime.datetime.now():%H%M%S}")
            gold = os.path.join(info["brief_dir"], "golden.diff") if info.get("brief_dir") else ""
            p = subprocess.run(["bash", os.path.join(HERE, "check.sh"), run, info["tier"], info["tip"], work,
                                gold if gold and os.path.isfile(gold) else ""],
                               capture_output=True, text=True)
            last = (p.stdout.strip().splitlines() or ["CHECK HARNESS golden=none result=no output"])[-1]
            if p.stderr:
                _wtext(os.path.join(run, "check.stderr"), p.stderr)
            mm = re.match(r"CHECK (\w+) golden=(\S+) result=(.*)", last)
            verdict, golden, cres = (mm.group(1), mm.group(2), mm.group(3)) if mm else ("HARNESS", "-", last)
            if not a.keep_clone and os.path.isfile(os.path.join(work, ".hosted_check_work")):
                shutil.rmtree(os.path.join(work, "clone"), ignore_errors=False)  # our own --shared clone; symlinks unlinked, not followed
        _wjson(os.path.join(run, "round.json"),
               {"verdict": verdict, "tier": info["tier"], "tip": info["tip"], "golden": golden, "checker_result": cres,
                "spark_run": r["run"], "spark_verdict": info["spark_verdict"], "spark_result": info["spark_result"],
                "model": body["model"], "provider_routing": body["provider"], "cost_usd": usd})
        append_done(mk, [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tag, f"{verdict} ({cres})",
                         round(wall, 3), f"{meta['prompt_eval_count']}+{meta['eval_count']}", meta["reasoning_tokens"],
                         f"{usd:.5f}", info["spark_verdict"], golden, run, r["run"]])
        print(f"HOSTED {mk} {tag}: {verdict} — {cres} · golden {golden} · Spark was {info['spark_verdict']} · ${usd:.5f} · "
              f"spent ${budget.total():.4f}/{cap:.2f}")
        rc = {"PASS": 0, "FAIL": 1, "HARNESS": 5}.get(verdict, 0)
        worst_rc = max(worst_rc, rc) if rc != 0 else worst_rc
    return worst_rc


if __name__ == "__main__":
    sys.exit(main())
