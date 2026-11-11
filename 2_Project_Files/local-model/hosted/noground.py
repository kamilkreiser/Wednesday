#!/usr/bin/env python3
"""hosted/noground.py — the NO-GOLDEN test (2026-11-11): real Secuura KS tickets, hosted models, no Claude-written fix.

Commission: 0_Brain/reference/2026-11-11_studio-256-decision/test/commission.md (Kam, live board 21:36:17 + 21:38:45).
It ADDS to replay.py and never changes it: replay.py is imported for the routing pin (assert_routing), the budget
(Budget), the send/retry path (send_with_retry), the key reader (read_key) and the output writer (write_outputs); the
checker leg is the SAME hosted/check.sh with tier code_patch2 and NO golden.

What the model gets (and only this):
  system = lm_call.SYSTEM_PREAMBLE + "\\n\\n" + NOGOLDEN_CONTRACT (below: the kit's mechanics, minus "copy the brief's
           + lines" — there are none)
  user   = "## TASK\\n" + code_patch2 task.md (tasks/code_patch2/make_task.py, generated at build time) +
           "\\n\\n## INPUT (JSON)\\n" + input.json
  input.json = the ticket (Linear title + description + comments, verbatim), the declared product file(s) at the tip
           (whole, or a head+cited-lines excerpt when > 160000 B), ONE existing test in the same service as a read-only
           template, the runner/tsconfig facts, and the harness shape (declared files, the 🔴 red-cell convention).
           No golden, no '+' lines, no red-cell names, no line pins (defect_line is empty).

Judged by check.sh code_patch2 legs that need no golden: A1/A2 applies at the tip, A3 touched set == declared,
A4 red-first, A5 green-after, A6 suite no worse, A7 tsc. A3b/A3c/A3x are brief-derived and skip themselves (no sites,
no expected '+', no brief blocks). The Claude read of each PASS (ACCEPT / WRONG-FIX / PARTIAL) is done by hand after.

Rounds: round 1 = the ticket. --round2 re-sends a FAILed task ONCE with `retry_feedback` = the checker's own FAIL
lines (mechanical, no Claude-written words), so a round-2 PASS costs no Claude minutes.

Usage:
  noground.py build                         fetch the tickets (Linear, read-only) + files at the tip -> state/noground/inputs/
  noground.py run --model mimo|glm|<extra> [--dry-run] [--only KS-1,..] [--round2] [--keep-clone] [--no-check]
Exit: 0 ok · 1 a model FAIL · 2 refused (no key, routing, budget) · 4 HTTP/shape · 5 HARNESS · 64 usage.
Budget: state/noground_budget.json, cap NOGROUND_BUDGET_USD (default 18.00 = the commission's stop line), every
request reserved at its worst case first. Keys are read by name in-process; never printed, never in argv.
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
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import replay as R  # noqa: E402  — the replay harness, imported unchanged

LM = R.LM
SRC = os.environ.get("HOSTED_SPARK_SRC", os.path.join(LM, "spark", "cache", "src"))
TASKS = os.path.join(HERE, "noground_tasks.json")
NG_STATE = os.environ.get("NOGROUND_STATE", os.path.join(HERE, "state", "noground"))
NG_RUNS = os.environ.get("NOGROUND_RUNS", os.path.join(HERE, "runs", "noground"))
NG_DONE = os.environ.get("NOGROUND_DONE", os.path.join(HERE, "done_noground.md"))
SECUURA_ENV = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"   # read-only, by name
SUBDIR = "Blockchain/Dev"
TRIG = 160000
DEFAULT_CAP = 18.00
BYTES_PER_TOKEN = 3.0   # conservative (more tokens than real) for the worst-case reserve

# Extra models (Part A's best hosted ZDR candidate) are added here, never in replay.py. replay.MODELS is extended
# IN-PROCESS so assert_routing / cost_of / write_outputs see them; the file replay.py is not touched.
EXTRA_MODELS = {
    # Part A (2026-11-11): the strongest open model that runs on a 256 GB box (3.0 bpw MLX, ~209 GB) and is hosted ZDR.
    # DeepInfra fp8 base tier, $0.098/$0.294 per M, in OpenRouter's public ZDR list (/api/v1/endpoints/zdr) read
    # 2026-11-11 21:42. Thinking OFF as in the 2026-10-27 V4.1 hosted trial (reasoning.enabled=false, proven 0 tokens).
    "v41": {
        "id": "deepseek/deepseek-v4.1-flash-1017", "provider": "deepinfra", "tag": "deepinfra/fp8",
        "price_in": 0.098e-6, "price_out": 0.294e-6, "max_tokens": 16384,
        "extra": {"reasoning": {"enabled": False}},
        "thinking_expected": False,
    },
}
R.MODELS.update(EXTRA_MODELS)

NOGROUND_CONTRACT = """# Your task contract (no worked brief)

You are a coding model fixing ONE real ticket. There is NO worked brief: nobody has written the fix for you. The
ticket text (description and comments, verbatim) says what is wrong; the files at the pinned tip are the code. You
decide the minimal change that makes the code behave as the ticket asks, and you write a test that proves it.

## Output

Emit exactly ONE fenced ```diff block and nothing outside it. If the ticket asks for something you cannot do inside
the declared files, or the files do not match the ticket, STOP and say so in one line instead of a diff.

## The rules that decide pass or fail

1. Touch EXACTLY the declared files (`product_files` + `test_files`), no other. Never touch the reference test.
2. Context lines keep their leading space and are copied byte for byte from the file you were given.
3. Count every hunk header honestly: `@@ -a,b +c,d @@`, b = context + '-' lines, d = context + '+' lines. Write the
   content first, count, then write the header. A miscounted header rejects the whole patch.
4. Your new test must be RED at the tip and GREEN after your product change. Every cell that should fail before the
   fix carries the red circle character U+1F534 in its title (`it('🔴 <ticket id>: ...')`); a failing cell without it
   is read as a broken control. At least one CONTROL cell (no red circle) passes before and after.
5. Minimal, deterministic product change: imports the file already has, no new dependencies, no refactors, no
   changed behaviour outside what the ticket asks. Keep the existing tests of the service green.
6. Where a fact you need is not in the input, write UNKNOWN in a comment rather than inventing it.
"""


def _sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def git(*a):
    p = subprocess.run(["git", "-C", SRC, *a], capture_output=True, text=True)
    return p.returncode, p.stdout


def show(tip, path):
    rc, out = git("show", f"{tip}:{path}")
    return out if rc == 0 else None


def env_value(path, name):
    """One value from an env file, by name. Never printed."""
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return None
    for line in lines:
        m = re.match(r"\s*(?:export\s+)?([A-Za-z0-9_]+)\s*=\s*(.*)$", line)
        if m and m.group(1) == name:
            return m.group(2).strip().strip("'\"") or None
    return None


def linear_issue(ident):
    key = env_value(SECUURA_ENV, "LINEAR_API_KEY")
    if not key:
        raise R.Refused("LINEAR_API_KEY is not in the Secuura .env")
    num = int(ident.split("-")[1])
    q = ("query($n:Float){issues(filter:{number:{eq:$n},team:{key:{eq:\"KS\"}}}){nodes{identifier title priority "
         "state{name} assignee{name} description comments(first:50){nodes{body createdAt user{name}}}}}}")
    req = urllib.request.Request("https://api.linear.app/graphql", data=json.dumps({"query": q, "variables": {"n": num}}).encode(),
                                 headers={"Authorization": key, "Content-Type": "application/json", "User-Agent": "noground"})
    nodes = json.load(urllib.request.urlopen(req, timeout=60))["data"]["issues"]["nodes"]
    nodes = [n for n in nodes if n["identifier"] == ident]
    if not nodes:
        raise R.Refused(f"{ident} not found on Linear")
    return nodes[0]


def ticket_text(issue):
    """The ticket as the model sees it: description + comments (oldest first), verbatim."""
    cs = sorted((issue.get("comments") or {}).get("nodes") or [], key=lambda c: c.get("createdAt") or "")
    t = issue.get("description") or ""
    if cs:
        t += "\n\n## Comments on the ticket (oldest first)\n"
        for c in cs:
            t += f"\n### comment {c.get('createdAt', '')[:16]}\n{c.get('body') or ''}\n"
    return t


def excerpt_rule():
    bi = open(os.path.join(LM, "night", "build_input.sh"), encoding="utf-8").read()
    m = re.search(r'_EXCERPT_RULE = \(\n(.*?)\n\)\n', bi, re.S)
    rule = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))) if m else ""
    if not rule:
        raise R.Refused("could not read _EXCERPT_RULE from night/build_input.sh")
    return rule


def excerpt(body, text, path, margin=40, head=60):
    """Head + every line the ticket cites for this file (`<basename>:NNN`) or quotes uniquely, +- margin."""
    fl = body.split("\n"); n = len(fl); base = os.path.basename(path)
    want = [(1, min(head, n))]
    for m in re.finditer(re.escape(base) + r"[`]?\s*:?\s*(\d{1,5})(?:\s*-\s*(\d{1,5}))?", text):
        a = int(m.group(1)); b = int(m.group(2) or a)
        if 1 <= a <= n:
            want.append((max(1, a - margin), min(n, b + margin)))
    for sn in set(re.findall(r"`([^`\n]{12,160})`", text)):
        hits = [i + 1 for i, ln in enumerate(fl) if sn in ln]
        if len(hits) == 1:
            want.append((max(1, hits[0] - margin), min(n, hits[0] + margin)))
    want.sort(); merged = []
    for a, b in want:
        if merged and a <= merged[-1][1] + 10:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    regions = [{"first_line": a, "last_line": b, "text": "\n".join(fl[a - 1:b])} for a, b in merged]
    return {"excerpt": True, "total_lines": n, "total_bytes": len(body), "carried_bytes": sum(len(r["text"]) for r in regions),
            "regions": regions, "rule": excerpt_rule(),
            "why": f"noground: {path} is {len(body)} B; the head and every line the ticket cites or quotes (+-{margin}) are carried"}


def reference_test(tip, test_dir, products):
    """An EXISTING test in the service that imports a declared product (smallest such file > 1 KB), else the smallest
    test in test_dir that imports anything from ../ ."""
    rc, out = git("ls-tree", "-r", "--name-only", tip, test_dir + "/")
    tests = [t for t in out.split("\n") if re.search(r"\.test\.ts$", t) and ".integration." not in t]
    stems = [os.path.splitext(os.path.basename(p))[0] for p in products]
    best = []
    for t in tests:
        body = show(tip, t) or ""
        if len(body) < 1000:
            continue
        if any(re.search(r"from\s+['\"][./]+(?:[\w\-/]*/)?" + re.escape(s) + r"['\"]", body) or
               re.search(r"(?:import|require|mock)\(\s*['\"][./]+(?:[\w\-/]*/)?" + re.escape(s) + r"['\"]", body) for s in stems):
            best.append((len(body), t))
    if best:
        return sorted(best)[0][1], "imports a declared product"
    sized = sorted((len(show(tip, t) or ""), t) for t in tests[:200])
    sized = [x for x in sized if x[0] > 1000]
    return (sized[0][1], "no test imports a declared product; the smallest test in the directory") if sized else (None, "none")


def build_one(task, tip, issue, rule_cache=None):
    prods = [f"{SUBDIR}/{p}" for p in task["products"]]
    m = re.match(rf"^{re.escape(SUBDIR)}/(services/[^/]+|packages/[^/]+)/", prods[0])
    service = m.group(1)
    if any(not p.startswith(f"{SUBDIR}/{service}/") for p in prods):
        raise R.Refused(f"{task['id']}: products span services (A6/A7 measure one service)")
    test_dir = f"{SUBDIR}/{service}/src/__tests__"
    pkg = json.loads(show(tip, f"{SUBDIR}/{service}/package.json"))
    script = pkg.get("scripts", {}).get("test", "")
    kind = "jest" if "jest" in script and "vitest" not in script else "vitest"
    svc = f"{SUBDIR}/{service}"
    if kind == "vitest":
        setup = "; setupFiles ./vitest.setup.ts" if show(tip, f"{svc}/vitest.setup.ts") is not None else ""
        runner = f"vitest (run one file with `npx vitest run <file>` from {svc}{setup})"
    else:
        runner = f"jest (ts-jest; run one file with `npx jest <file>` from {svc}; jest.config.js)"
    try:
        co = json.loads(re.sub(r"//[^\n]*", "", show(tip, f"{svc}/tsconfig.json") or "{}")).get("compilerOptions", {})
    except ValueError:
        co = {}
    ts = ", ".join(k for k in ("strict", "noUnusedLocals", "noUnusedParameters", "esModuleInterop") if co.get(k))
    ts += f", module {co.get('module', '?')}, target {co.get('target', '?')}"
    text = ticket_text(issue)
    files, excerpted = {}, []
    for p in prods:
        body = show(tip, p)
        if body is None:
            raise R.Refused(f"{task['id']}: {p} is not at the tip")
        if len(body) <= TRIG:
            files[p] = body
        else:
            files[p] = excerpt(body, text, p); excerpted.append(p)
    ref, why = reference_test(tip, test_dir, prods)
    if ref:
        files[ref] = show(tip, ref)
    slug = re.sub(r"[^a-z0-9]+", "-", issue["title"].lower()).strip("-")[:60].rstrip("-")
    newtest = f"{test_dir}/{task['id'].lower().replace('-', '')}-noground-{slug}.test.ts"
    if show(tip, newtest) is not None:
        raise R.Refused(f"{newtest} already exists at the tip")
    imports = " | ".join(l for l in (files[prods[0]] if isinstance(files[prods[0]], str) else "").split("\n") if l.startswith("import "))[:1500]
    note = ("CODE_PATCH2 (multi-file): your diff touches EXACTLY these files and no other - products: " + ", ".join(prods)
            + f"; tests: {newtest} (new). NO WORKED BRIEF: the ticket text is all there is; decide the fix from it and from "
            + "the files. " + (f"READ-ONLY template: `{ref}` is an EXISTING test in the same service ({why}); copy its import / "
            + "mock / app-building shape, do NOT modify it. " if ref else "No template test was found; write UNKNOWN where a mock shape is needed. ")
            + "Red-first cells carry the red circle U+1F534 in their it() title; at least one control cell does not. "
            + "Where a dependency your cell needs is not mocked by the template, mock it in YOUR test with the same factory shape.")
    d = {
        "ticket": {"identifier": issue["identifier"], "title": issue["title"], "state": (issue.get("state") or {}).get("name"),
                   "priority": issue.get("priority"), "description": text},
        "repo": {"source_checkout": SRC, "tip": tip, "branch": "develop", "repo_subdir": SUBDIR, "service_dir": service,
                 "shared_pkg_dir": "packages/shared", "shared_pkg_name": "@secuura/shared", "test_runner": runner,
                 "typescript": ts + ("; the first product's imports at the tip are: " + imports if imports else "")},
        "product_file": prods[0],
        "defect_line": {"line": 0, "text": "", "sites": [], "expected_plus": [], "red_cells": []},
        "test_dir": test_dir, "suggested_test_file": newtest, "reference_test_file": ref or "",
        "reference_test_note": note, "files": files,
        "source_checkout": SRC, "tip": tip, "repo_subdir": SUBDIR, "service_dir": service,
        "shared_pkg_dir": "packages/shared", "shared_pkg_name": "@secuura/shared",
        "task_type": "code_patch2", "product_files": prods, "test_files": [{"path": newtest, "status": "new"}],
        "noground": {"tier": task["tier"], "rung": task.get("rung"), "golden": "NONE", "ticket_sha256": _sha(text)},
    }
    if excerpted:
        d["excerpt_rule"] = excerpt_rule(); d["excerpted_files"] = excerpted
    return d


def task_md():
    path = os.path.join(NG_STATE, "task_code_patch2.md")
    os.makedirs(NG_STATE, exist_ok=True)
    p = subprocess.run([sys.executable, os.path.join(LM, "tasks", "code_patch2", "make_task.py"), path], capture_output=True, text=True)
    if p.returncode != 0:
        raise R.Refused(f"make_task.py rc {p.returncode}: {p.stderr.strip()[:300]}")
    return path


def build_messages(input_text, task_text):
    system = R.SYSTEM_PREAMBLE + "\n\n" + NOGROUND_CONTRACT.strip()
    user = "## TASK\n" + task_text.strip() + "\n\n## INPUT (JSON)\n" + input_text.strip() + "\n"
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    info = {"prompt_bytes": len(system.encode()) + len(user.encode()), "sha256_task_plus_input": _sha(task_text + input_text),
            "messages_sha256": _sha(json.dumps(msgs, ensure_ascii=False)), "est_prompt_tokens": int((len(system.encode()) + len(user.encode())) / BYTES_PER_TOKEN)}
    return msgs, info


def no_golden_proof(d):
    """Refuse an input that carries anything golden-shaped."""
    dl = d.get("defect_line") or {}
    bad = [k for k in ("expected_plus", "red_cells", "sites") if dl.get(k)]
    if re.search(r"(?m)^##+\s*(The exact change|Red cells|The test)\b", d["ticket"]["description"]):
        bad.append("a brief section heading in the ticket text")
    if bad:
        raise R.Refused(f"{d['ticket']['identifier']}: input carries golden-shaped content: {bad}")


def worst_usd(mk, est_tokens):
    m = R.MODELS[mk]
    return est_tokens * R.PROMPT_TOKEN_MARGIN * m["price_in"] + m["max_tokens"] * m["price_out"]


def append_done(row):
    if not os.path.exists(NG_DONE):
        with open(NG_DONE, "w", encoding="utf-8") as f:
            f.write("# hosted/done_noground.md — one row per NO-GOLDEN round (noground.py; tickets, verdicts, cost; no code). Newest at the bottom.\n"
                    "| when | model | ticket | tier | rung | round | verdict | checker | model s | tokens (p+c) | reasoning tok | cost USD | served by | run dir |\n"
                    "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    with open(NG_DONE, "a", encoding="utf-8") as f:
        f.write("| " + " | ".join(str(x).replace("|", "/").replace("\n", " ") for x in row) + " |\n")


def done_rows():
    out = []
    if not os.path.exists(NG_DONE):
        return out
    for line in open(NG_DONE, encoding="utf-8"):
        if line.startswith("| 20"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 14:
                out.append({"model": c[1], "ticket": c[2], "round": c[5], "verdict": c[6], "checker": c[7]})
    return out


def cmd_build(a):
    spec = json.load(open(TASKS, encoding="utf-8"))
    tip = spec["tip"]
    os.makedirs(os.path.join(NG_STATE, "inputs"), exist_ok=True)
    rc = 0
    for t in spec["tasks"]:
        if a.only and t["id"] not in a.only:
            continue
        try:
            issue = linear_issue(t["id"])
            if re.search(r"peter|stuart", ((issue.get("assignee") or {}).get("name") or ""), re.I):
                raise R.Refused(f"{t['id']} is assigned to {issue['assignee']['name']}")
            d = build_one(t, tip, issue)
            no_golden_proof(d)
            p = os.path.join(NG_STATE, "inputs", f"{t['id']}.json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=1, ensure_ascii=False)
            print(f"BUILT {t['id']} tier={t['tier']} rung={t.get('rung')} products={len(d['product_files'])} "
                  f"excerpted={len(d.get('excerpted_files') or [])} ref={os.path.basename(d['reference_test_file']) or '-'} "
                  f"ticket={len(d['ticket']['description'])} chars input={os.path.getsize(p)} B")
        except (R.Refused, urllib.error.URLError, KeyError, ValueError) as e:
            print(f"REFUSED {t['id']}: {e}"); rc = 2
    return rc


def feedback_for(prev_run):
    """Round 2: the checker's own FAIL lines from round 1, verbatim — no Claude-written words."""
    co = os.path.join(prev_run, "checker.out")
    lines = [l for l in open(co, encoding="utf-8", errors="replace").read().split("\n") if l.startswith(("FAIL", "RESULT"))] if os.path.exists(co) else []
    return {"verdict": "FAIL", "checker_fail_lines": lines[:8],
            "instruction": "Your first diff for this exact task was refused by the checker for the reasons above. Emit the COMPLETE diff again (every product hunk and the test), fixing them."}


def cmd_run(a, post=None):
    mk = a.model
    if mk not in R.MODELS:
        print(f"noground: unknown model {mk}"); return 64
    m = R.MODELS[mk]
    cap = float(os.environ.get("NOGROUND_BUDGET_USD", DEFAULT_CAP))
    budget = R.Budget(os.path.join(NG_STATE, "noground_budget.json"), cap)
    spec = json.load(open(TASKS, encoding="utf-8"))
    tpath = task_md(); task_text = open(tpath, encoding="utf-8").read()
    rows = done_rows()
    plan = []
    for t in spec["tasks"]:
        if a.only and t["id"] not in a.only:
            continue
        ip = os.path.join(NG_STATE, "inputs", f"{t['id']}.json")
        if not os.path.exists(ip):
            print(f"noground: {t['id']} has no built input (run `noground.py build`)"); continue
        mine = [r for r in rows if r["model"] == mk and r["ticket"] == t["id"]]
        real = [r for r in mine if r["verdict"].startswith(("PASS", "FAIL"))]
        if a.round2:
            if any(r["round"] == "2" for r in real) or not real or not real[-1]["verdict"].startswith("FAIL") or real[-1]["round"] != "1":
                continue
            rnd = 2
        else:
            if real:
                continue
            rnd = 1
        input_text = open(ip, encoding="utf-8").read()
        d = json.loads(input_text)
        no_golden_proof(d)
        if rnd == 2:
            prev = sorted(x for x in os.listdir(os.path.join(NG_RUNS, mk)) if x.startswith(t["id"] + "_r1_"))
            d["retry_feedback"] = feedback_for(os.path.join(NG_RUNS, mk, prev[-1])) if prev else {"verdict": "FAIL"}
            input_text = json.dumps(d, indent=1, ensure_ascii=False)
        msgs, info = build_messages(input_text, task_text)
        info.update({"task_path": tpath, "tip": d["tip"], "tier": "code_patch2"})
        body = R.build_body(mk, msgs)
        R.assert_routing(body, mk)
        plan.append((t, rnd, d, input_text, body, info))
    est = sum(worst_usd(mk, i["est_prompt_tokens"]) for *_, i in plan)
    typ = sum(i["est_prompt_tokens"] * m["price_in"] + 4000 * m["price_out"] for *_, i in plan)
    print(f"noground: model {mk} = {m['id']} pinned {m['tag']} zdr · {len(plan)} request(s) · typical ~${typ:.4f} "
          f"(prompt bytes/{BYTES_PER_TOKEN} + 4000 out) · worst ${est:.4f} · spent ${budget.total():.4f} of cap ${cap:.2f}")
    key = R.read_key()
    if a.dry_run:
        dd = os.path.join(NG_STATE, "dry", f"{mk}_{datetime.datetime.now():%Y%m%d-%H%M%S}")
        os.makedirs(dd, exist_ok=True)
        for t, rnd, d, _, body, info in plan:
            print(f"DRY {t['id']} r{rnd} tier={t['tier']}: POST {R.API_URL} model={body['model']} provider={json.dumps(body['provider'])} "
                  f"prompt_bytes={info['prompt_bytes']} est_tokens={info['est_prompt_tokens']} worst=${worst_usd(mk, info['est_prompt_tokens']):.4f}")
            with open(os.path.join(dd, f"{t['id']}_r{rnd}.request.json"), "w", encoding="utf-8") as f:
                json.dump(body, f, ensure_ascii=False)
        print(f"noground: DRY-RUN — {len(plan)} bodies in {dd}; key {'present' if key else 'ABSENT'}; zero network calls")
        return 0
    if not key:
        print(f"noground: {R.KEY_NAME} is not in {R.ENV_FILE} — add it there (never on the command line); nothing sent")
        return 2
    worst_rc = 0
    for t, rnd, d, input_text, body, info in plan:
        tag = f"{t['id']}_r{rnd}"
        run = os.path.join(NG_RUNS, mk, f"{tag}_{datetime.datetime.now():%Y%m%d-%H%M%S}")
        os.makedirs(run)
        with open(os.path.join(run, "input.json"), "w", encoding="utf-8") as f:
            f.write(input_text)
        shutil.copyfile(info["task_path"], os.path.join(run, "task.md"))
        with open(os.path.join(run, "request.json"), "w", encoding="utf-8") as f:
            json.dump(body, f, indent=1, ensure_ascii=False)   # no key in the body
        try:
            raw, usd, source, wall = R.send_with_retry(body, mk, key, budget, tag, worst_usd(mk, info["est_prompt_tokens"]), post=post)
        except R.Refused as e:
            print(f"noground: REFUSED {tag}: {e}"); return 2
        except R.RateLimited as e:
            append_done([f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}", mk, t["id"], t["tier"], t.get("rung"), rnd,
                         "SKIPPED-RATE-LIMIT", f"HTTP {e.code} x{e.attempts}", "-", "-", "-", "0.00000", "-", run])
            worst_rc = max(worst_rc, 4); continue
        except urllib.error.HTTPError as e:
            print(f"noground: HTTP {e.code} on {tag}: {getattr(e, 'hosted_body', b'')[:300]!r}"); return 4
        except (urllib.error.URLError, OSError) as e:
            print(f"noground: connection error on {tag}: {e}"); return 4
        try:
            meta = R.write_outputs(run, mk, body, info, raw, wall, usd, source)
        except (ValueError, KeyError, IndexError) as e:
            print(f"noground: unexpected response on {tag}: {e}"); return 4
        harness = None
        if not m["thinking_expected"] and (meta["thinking_chars"] or meta["think_leak_in_content"]):
            harness = "thinking was ON or leaked (requested off)"
        served = str(meta["provider_served"] or "")
        if not served:
            harness = "the response names no provider: zero-retention routing NOT proven for this call"
        elif m["provider"].replace("-", "").lower() not in served.replace(".", "").replace("-", "").replace(" ", "").lower():
            harness = f"served by {served!r}, not the pinned {m['provider']}"
        verdict, cres = "UNCHECKED", ""
        if harness:
            verdict, cres = "HARNESS", harness
        elif not a.no_check:
            work = os.path.join(R.WORK, f"noground_{os.path.basename(run)}")
            p = subprocess.run(["bash", os.path.join(HERE, "check.sh"), run, "code_patch2", d["tip"], work, ""], capture_output=True, text=True)
            last = (p.stdout.strip().splitlines() or ["CHECK HARNESS golden=none result=no output"])[-1]
            if p.stderr:
                with open(os.path.join(run, "check.stderr"), "w", encoding="utf-8") as f:
                    f.write(p.stderr)
            mm = re.match(r"CHECK (\w+) golden=(\S+) result=(.*)", last)
            verdict, cres = (mm.group(1), mm.group(3)) if mm else ("HARNESS", last)
            if not a.keep_clone and os.path.isfile(os.path.join(work, ".hosted_check_work")):
                shutil.rmtree(os.path.join(work, "clone"), ignore_errors=False)
        with open(os.path.join(run, "round.json"), "w", encoding="utf-8") as f:
            json.dump({"verdict": verdict, "checker_result": cres, "ticket": t["id"], "tier": t["tier"], "rung": t.get("rung"),
                       "round": rnd, "model": body["model"], "provider_routing": body["provider"], "provider_served": served,
                       "cost_usd": usd, "golden": "NONE"}, f, indent=1)
        append_done([f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}", mk, t["id"], t["tier"], t.get("rung"), rnd, verdict, cres,
                     round(wall, 1), f"{meta['prompt_eval_count']}+{meta['eval_count']}", meta["reasoning_tokens"], f"{usd:.5f}", served, run])
        print(f"NOGROUND {mk} {tag} [{t['tier']}]: {verdict} — {cres} · ${usd:.5f} · served {served} · spent ${budget.total():.4f}/{cap:.2f}", flush=True)
        rc = {"PASS": 0, "FAIL": 1, "HARNESS": 5}.get(verdict, 0)
        worst_rc = max(worst_rc, rc)
    return worst_rc


def main(argv=None, post=None):
    ap = argparse.ArgumentParser(prog="noground.py")
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build"); b.add_argument("--only", default="")
    r = sub.add_parser("run"); r.add_argument("--model", required=True); r.add_argument("--dry-run", action="store_true")
    r.add_argument("--only", default=""); r.add_argument("--round2", action="store_true")
    r.add_argument("--keep-clone", action="store_true"); r.add_argument("--no-check", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 64 if e.code else 0
    if not a.cmd:
        ap.print_usage(); return 64
    a.only = set(x.strip() for x in a.only.split(",") if x.strip())
    return cmd_build(a) if a.cmd == "build" else cmd_run(a, post=post)


if __name__ == "__main__":
    sys.exit(main())
