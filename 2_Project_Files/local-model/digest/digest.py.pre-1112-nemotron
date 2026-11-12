#!/usr/bin/env python3
"""digest.py - Spark test-output DIGEST with a deterministic parser and checker (pilot (a), Kam 2026-11-12 11:34).

usage: digest.py RAW_FILE --kind vitest|jest|bash-suite|tsc|generic --out DIR [--delta PREV_digest.json] [--no-spark]

Flow: (1) a deterministic PARSER extracts the ground truth from RAW_FILE (counts; every failure's name, first error
line, first stack frame). (2) The Spark is asked for the digest in a fixed JSON shape. It is NOT shown the parser's
answer, so agreement is evidence. (3) A CHECKER compares every Spark count, the verdict, every failure name (a
bijection with the parser's list), every quoted error/frame line (must occur verbatim in the raw) and every number in an
anomaly (must occur in the raw). Any disagreement -> the Spark digest is REFUSED and the parser's own summary is emitted,
with the mismatches recorded in check.json.

Outputs in DIR: digest.md (BLUF first, one page), digest.json, check.json, spark_response.txt (what the Spark said).
status (first line of stdout, and digest.json "status"):
  CHECKED                 Spark digest accepted: every number re-derived from the raw file
  REFUSED_MISMATCH        Spark digest refused, parser summary emitted           (rc 0)
  PARSER_ONLY_SPARK_DOWN  Spark unreachable / timed out / empty, parser summary  (rc 0)
  PARSER_ONLY             --no-spark                                             (rc 0)
  NO_GROUND_TRUTH         raw file truncated / garbled / empty: the parser cannot establish the counts, the Spark is
                          NOT asked, nothing is claimed                          (rc 3)
rc 2 = usage / unreadable input.  Python 3 stdlib only.

Spark client: same server settings as local-model/gate/spark_review.py (chat/completions, temperature 0,
chat_template_kwargs.thinking=false; thinking eats the token budget, 2026-09-23 lesson). One request at a time: waits
while spark/state/round.lock exists or a live queue.lock holder is running. Test seam: DIGEST_SPARK_STUB=<file> returns
that file's text as the Spark reply (no network).
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.normpath(os.path.join(HERE, "..", "spark", "state"))
URL = os.environ.get("SPARK_URL", "http://127.0.0.1:47788").rstrip("/")
MODEL = os.environ.get("SPARK_MODEL", "deepseek-v4-flash-0731")
MAX_SENT_CHARS = int(os.environ.get("DIGEST_MAX_CHARS", "400000"))
MAX_TOKENS = int(os.environ.get("DIGEST_MAX_TOKENS", "6000"))
REQ_TIMEOUT = int(os.environ.get("DIGEST_TIMEOUT", "900"))
CAP = 200  # parser keeps at most this many failures

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07")
KINDS = ("vitest", "jest", "bash-suite", "tsc", "generic")
COUNT_KEYS = {
    "vitest": ["files_passed", "files_failed", "tests_passed", "tests_failed", "tests_skipped"],
    "jest": ["files_passed", "files_failed", "tests_passed", "tests_failed", "tests_skipped"],
    "bash-suite": ["tests_passed", "tests_failed", "tests_skipped"],
    "tsc": ["errors", "files_with_errors"],
    "generic": ["error_lines", "warning_lines"],
}


def clean(text):
    return ANSI.sub("", text).replace("\r\n", "\n").replace("\r", "\n")


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


# ------------------------------------------------------------------ parser
def _parts(s):
    """'1 failed | 5 passed | 1 skipped' or '1 failed, 3 passed' -> {failed:1, passed:5, skipped:1}."""
    d = {}
    for n, w in re.findall(r"(\d+)\s+(failed|passed|skipped|todo|total)", s):
        d[w] = d.get(w, 0) + int(n)
    return d


def _first_after(lines, i, stop):
    """first non-blank line after index i (before stop(line) is true), or ''."""
    for j in range(i + 1, len(lines)):
        if stop(lines[j]):
            return ""
        if lines[j].strip():
            return lines[j].strip()
    return ""


def parse_vitest(lines):
    t = {"complete": False, "notes": []}
    files = tests = None
    for l in lines:
        m = re.match(r"^\s*Test Files\s+(.*?)\s*\((\d+)\)\s*$", l)
        if m:
            files = _parts(m.group(1))
        m = re.match(r"^\s*Tests\s+(.*?)\s*\((\d+)\)\s*$", l)
        if m:
            tests = _parts(m.group(1))
    if files is None or tests is None:
        t["notes"].append("no vitest 'Test Files' / 'Tests' summary lines (truncated or not vitest output)")
        t["counts"] = {}
        t["failures"] = []
        return t
    t["complete"] = True
    t["counts"] = {"files_passed": files.get("passed", 0), "files_failed": files.get("failed", 0),
                   "tests_passed": tests.get("passed", 0), "tests_failed": tests.get("failed", 0),
                   "tests_skipped": tests.get("skipped", 0)}
    fails, seen, dups, in_sec = [], set(), 0, False
    for i, l in enumerate(lines):
        if re.match(r"^[⎯\s]*Failed (Tests|Suites)\s+\d+", l):
            in_sec = True
            continue
        if not in_sec:
            continue
        m = re.match(r"^\s*FAIL\s{2}(.+?)\s*$", l)
        if not m:
            continue
        name = norm(m.group(1))
        if name in seen:
            dups += 1
            continue
        seen.add(name)
        err = _first_after(lines, i, lambda x: re.match(r"^\s*FAIL\s{2}", x) is not None)
        frame = ""
        for j in range(i + 1, len(lines)):
            if re.match(r"^\s*FAIL\s{2}", lines[j]):
                break
            mm = re.match(r"^\s*❯\s+(\S.*)$", lines[j])
            if mm:
                frame = mm.group(1).strip()
                break
        fails.append({"name": name, "error": err, "frame": frame})
    t["failures"] = fails[:CAP]
    t["capped"] = len(fails) > CAP
    if dups:
        t["notes"].append(f"{dups} repeated FAIL header(s) de-duplicated")
    nf = t["counts"]["tests_failed"] + t["counts"]["files_failed"]
    if t["counts"]["tests_failed"] + t["counts"]["files_failed"] > 0 and not fails:
        t["notes"].append("summary reports failures but no 'Failed Tests' section found")
    if fails and len(fails) > nf:
        t["notes"].append(f"{len(fails)} FAIL entries vs {nf} failed per the summary")
    return t


def parse_jest(lines):
    t = {"complete": False, "notes": []}
    suites = tests = None
    for l in lines:
        m = re.match(r"^\s*Test Suites:\s+(.*)$", l)
        if m:
            suites = _parts(m.group(1))
        m = re.match(r"^\s*Tests:\s+(.*)$", l)
        if m:
            tests = _parts(m.group(1))
    if suites is None or tests is None:
        t["notes"].append("no jest 'Test Suites:' / 'Tests:' summary lines (truncated or not jest output)")
        t["counts"] = {}
        t["failures"] = []
        return t
    t["complete"] = True
    t["counts"] = {"files_passed": suites.get("passed", 0), "files_failed": suites.get("failed", 0),
                   "tests_passed": tests.get("passed", 0), "tests_failed": tests.get("failed", 0),
                   "tests_skipped": tests.get("skipped", 0)}
    start = 0
    for i, l in enumerate(lines):
        if l.strip() == "Summary of all failing tests":
            start = i
    fails, seen, curfile = [], set(), ""
    for i in range(start, len(lines)):
        l = lines[i]
        m = re.match(r"^\s*(?:FAIL)\s+(\S+)", l)
        if m:
            curfile = m.group(1)
            continue
        m = re.match(r"^\s*●\s+(.+?)\s*$", l)
        if not m or m.group(1) == "Console":
            continue
        title = norm(m.group(1))
        name = f"{curfile} :: {title}" if curfile else title
        if name in seen:
            continue
        seen.add(name)
        err = _first_after(lines, i, lambda x: re.match(r"^\s*●\s", x) is not None or re.match(r"^\s*FAIL\s", x) is not None)
        frame = ""
        for j in range(i + 1, len(lines)):
            if re.match(r"^\s*●\s", lines[j]) or re.match(r"^\s*FAIL\s", lines[j]):
                break
            if re.match(r"^\s+at\s+\S", lines[j]):
                frame = lines[j].strip()
                break
        fails.append({"name": name, "title": title, "error": err, "frame": frame})
    t["failures"] = fails[:CAP]
    t["capped"] = len(fails) > CAP
    return t


SUMMARY = re.compile(r"^\s*(?:[\w./-]+:\s*)?(\d+) passed, (\d+) failed(?:, (\d+) skipped)?\s*$")


def parse_bash(lines):
    t = {"complete": False, "notes": []}
    p = f = s = n = 0
    lp = lf = ls = 0
    fails, sums = [], []
    for i, l in enumerate(lines):
        m = SUMMARY.match(l)
        if m:
            n += 1
            p += int(m.group(1)); f += int(m.group(2)); s += int(m.group(3) or 0)
            sums.append([int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)])
            continue
        m = re.match(r"^\s*(ok|FAIL|SKIP)\s+(.*)$", l)
        if m:
            if m.group(1) == "ok":
                lp += 1
            elif m.group(1) == "SKIP":
                ls += 1
            else:
                lf += 1
                err = _first_after(lines, i, lambda x: re.match(r"^\s*(ok|FAIL|SKIP)\s", x) is not None or x.startswith("=="))
                fails.append({"name": norm(m.group(2)), "error": err, "frame": ""})
    if n == 0:
        t["notes"].append("no 'N passed, M failed' summary line (truncated or not a bash-suite log)")
        t["counts"] = {}
        t["failures"] = []
        return t
    t["complete"] = True
    t["counts"] = {"tests_passed": p, "tests_failed": f, "tests_skipped": s}
    t["summaries"] = sums
    t["notes"].append(f"{n} summary line(s) summed")
    if (lp, lf, ls) != (p, f, s):
        t["notes"].append(f"per-line tally ok/FAIL/SKIP = {lp}/{lf}/{ls} differs from summed summaries {p}/{f}/{s} (some suites print no per-test lines)")
    if len(fails) != f:
        t["notes"].append(f"{len(fails)} FAIL line(s) vs {f} failed per the summaries")
    t["failures"] = fails[:CAP]
    t["capped"] = len(fails) > CAP
    return t


def parse_tsc(lines):
    t = {"complete": True, "notes": []}
    errs, files = [], set()
    found = None
    for l in lines:
        m = re.match(r"^(.+?)\((\d+),(\d+)\):\s*error\s+(TS\d+):\s*(.*)$", l) or \
            re.match(r"^(.+?):(\d+):(\d+)\s+-\s+error\s+(TS\d+):\s*(.*)$", l)
        if m:
            errs.append({"name": f"{m.group(1)}({m.group(2)},{m.group(3)}) {m.group(4)}", "error": norm(m.group(5)), "frame": ""})
            files.add(m.group(1))
        m = re.match(r"^\s*Found (\d+) errors?(?: in (\d+) files?)?", l)
        if m:
            found = int(m.group(1))
    t["counts"] = {"errors": len(errs), "files_with_errors": len(files)}
    if found is not None and found != len(errs):
        t["complete"] = False
        t["notes"].append(f"'Found {found} errors' line disagrees with {len(errs)} parsed error lines (truncated or garbled)")
    if found is None and errs:
        t["notes"].append("no 'Found N errors' line to cross-check (tsc --pretty false prints none)")
    if not errs and found is None:
        t["notes"].append("no error lines and no summary: tsc prints nothing on success; treated as zero errors")
    t["failures"] = errs[:CAP]
    t["capped"] = len(errs) > CAP
    return t


def parse_generic(lines):
    t = {"complete": True, "notes": ["generic kind: counts are line tallies, not test counts"]}
    er = re.compile(r"\b(error|err!|fatal|exception|traceback|panic)\b", re.I)
    wr = re.compile(r"\bwarn(ing)?\b", re.I)
    errs, w = [], 0
    for l in lines:
        if er.search(l):
            errs.append({"name": norm(l)[:200], "error": "", "frame": ""})
        elif wr.search(l):
            w += 1
    t["counts"] = {"error_lines": len(errs), "warning_lines": w}
    t["failures"] = errs[:CAP]
    t["capped"] = len(errs) > CAP
    return t


PARSERS = {"vitest": parse_vitest, "jest": parse_jest, "bash-suite": parse_bash, "tsc": parse_tsc, "generic": parse_generic}


def parse(kind, text):
    lines = clean(text).split("\n")
    t = PARSERS[kind](lines)
    c = t["counts"]
    if not t["complete"]:
        t["verdict"] = None
    elif kind in ("vitest", "jest"):
        t["verdict"] = "FAIL" if c["tests_failed"] or c["files_failed"] else "PASS"
    elif kind == "bash-suite":
        t["verdict"] = "FAIL" if c["tests_failed"] else "PASS"
    elif kind == "tsc":
        t["verdict"] = "FAIL" if c["errors"] else "PASS"
    else:
        t["verdict"] = "FAIL" if c["error_lines"] else "PASS"
    t.setdefault("capped", False)
    return t


# ------------------------------------------------------------------ spark client
def _live_pid(lock_dir):
    try:
        pid = int(open(os.path.join(lock_dir, "pid")).read().strip())
        os.kill(pid, 0)
        return pid
    except Exception:  # noqa: BLE001
        return None


def wait_for_box():
    """One request at a time: wait while a round or a queue drainer holds the box."""
    t0 = time.time()
    while os.path.exists(os.path.join(STATE, "round.lock")) or _live_pid(os.path.join(STATE, "queue.lock")):
        if time.time() - t0 > 3600:
            raise RuntimeError("box still locked after 60 min")
        print("digest: Spark box locked (round.lock / live queue.lock), waiting...", file=sys.stderr, flush=True)
        time.sleep(20)


def squeeze(text):
    """clean + collapse runs of identical lines + cap line length; head/tail cut when over MAX_SENT_CHARS."""
    out, prev, rep = [], None, 0
    for l in clean(text).split("\n"):
        l = l.rstrip()
        if len(l) > 400:
            l = l[:400] + " ...[line cut]"
        if l == prev and l.strip():
            rep += 1
            continue
        if rep >= 2:
            out.append(f"[previous line repeated {rep} more times]")
        if rep == 1:
            out.append(prev)
        rep, prev = 0, l
        out.append(l)
    if rep >= 2:
        out.append(f"[previous line repeated {rep} more times]")
    elif rep == 1:
        out.append(prev)
    s = "\n".join(out)
    note = None
    if len(s) > MAX_SENT_CHARS:
        h, tl = MAX_SENT_CHARS // 4, MAX_SENT_CHARS - MAX_SENT_CHARS // 4
        s = s[:h] + f"\n[... {len(s) - MAX_SENT_CHARS} characters cut from the middle: output over {MAX_SENT_CHARS} chars ...]\n" + s[-tl:]
        note = f"input cut to {MAX_SENT_CHARS} chars (head 25% + tail 75%)"
    return s, note


SHAPES = {
    "vitest": '"counts": {"files_passed": int, "files_failed": int, "tests_passed": int, "tests_failed": int, "tests_skipped": int}',
    "jest": '"counts": {"files_passed": int, "files_failed": int, "tests_passed": int, "tests_failed": int, "tests_skipped": int}  (files = Test Suites)',
    "bash-suite": '"summary_lines": [[passed, failed, skipped], ...]  (FIRST: one entry per "N passed, M failed[, K skipped]" line in the file, in order, skipped 0 when not printed)  (do NOT add them up: a program sums the column totals)',
    "tsc": '"counts": {"errors": int, "files_with_errors": int}',
    "generic": '"counts": {"error_lines": int, "warning_lines": int}  (lines containing error/fatal/exception/traceback; lines containing warn/warning that are not error lines)',
}


def build_prompt(kind, raw):
    sysmsg = ("You are a test-output digester. You read raw test output and return ONE JSON object and nothing else: "
              "no prose, no code fences. Never compute or estimate: copy every number and every string verbatim from the output. "
              "A program will re-derive every number and every quoted string from the raw file and discard your answer on any disagreement.")
    user = (f"Raw {kind} output follows between the markers.\n\nReturn exactly this JSON shape:\n"
            '{"verdict": "PASS" or "FAIL",\n ' + SHAPES[kind] + ',\n'
            ' "failures": [{"name": "<full failing test name or file as printed after FAIL/x/●>", "error": "<first error line, verbatim, max 160 chars>", "frame": "<first stack frame / file:line, verbatim, max 160 chars; empty string if none>"}],\n'
            ' "anomalies": ["<one short sentence each: warnings, unhandled rejections/errors, very slow tests, retries, suites that failed to run, anything odd that the counts do not show; quote any number exactly as printed; at most 8>"]}\n'
            "Rules: list EVERY failure, in order, once each. If nothing failed, failures is []. Use null for a count that is not printed. "
            "verdict is FAIL if any test or suite failed or failed to run.\n\n"
            "-----BEGIN RAW OUTPUT-----\n" + raw + "\n-----END RAW OUTPUT-----\n")
    return [{"role": "system", "content": sysmsg}, {"role": "user", "content": user}]


def call_spark(messages):
    """-> (text, usage, seconds). Raises on any failure (caller falls back to the parser summary)."""
    stub = os.environ.get("DIGEST_SPARK_STUB")
    if stub:
        return open(stub).read(), {"stub": True}, 0.0
    wait_for_box()
    body = {"model": MODEL, "messages": messages, "max_tokens": MAX_TOKENS, "temperature": 0, "stream": False,
            "chat_template_kwargs": {"thinking": False}}
    req = urllib.request.Request(URL + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=REQ_TIMEOUT) as r:
        j = json.load(r)
    ch = (j.get("choices") or [{}])[0]
    text = ((ch.get("message") or {}).get("content") or "").strip()
    usage = j.get("usage") or {}
    usage["finish_reason"] = ch.get("finish_reason")
    return text, usage, time.time() - t0


def extract_json(s):
    s = s.strip()
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    a, b = s.find("{"), s.rfind("}")
    if a < 0 or b <= a:
        raise ValueError("no JSON object in the reply")
    return json.loads(s[a:b + 1])


# ------------------------------------------------------------------ checker
def _strip_ell(s):
    return re.sub(r"(\.\.\.|…)\s*$", "", s or "").strip()


def _name_match(sname, p):
    s = norm(sname)
    keys = {norm(p["name"])}
    if p.get("title"):
        keys.add(norm(p["title"]))
    if s in keys:
        return True
    for k in keys:
        a, b = (s, k) if len(s) <= len(k) else (k, s)
        if len(a) >= 15 and a in b:
            return True
    return False


def check(kind, truth, spark, raw_norm, raw_tokens):
    """-> list of mismatch strings (empty = every number re-derived)."""
    mm = []
    if not isinstance(spark, dict):
        return ["reply is not a JSON object"]
    if spark.get("verdict") != truth["verdict"]:
        mm.append(f"verdict: spark {spark.get('verdict')!r} vs parser {truth['verdict']!r}")
    sc = spark.get("counts")
    if kind == "bash-suite" and sc is None:
        sc = {k: truth["counts"][k] for k in COUNT_KEYS[kind]}  # not asked for: derived by code from the verified summary_lines
    if not isinstance(sc, dict):
        mm.append("counts missing or not an object")
        sc = {}
    for k in COUNT_KEYS[kind]:
        a, b = sc.get(k), truth["counts"][k]
        if a is None and b == 0:
            continue  # "null = not printed" (told to the Spark) and the parser's 0 for an unprinted count mean the same
        if isinstance(a, bool) or not isinstance(a, int) or a != b:
            mm.append(f"count {k}: spark {a!r} vs parser {b}")
    extra = set(sc) - set(COUNT_KEYS[kind])
    if extra:
        mm.append(f"unexpected count keys {sorted(extra)}")
    if kind == "bash-suite":
        ss = spark.get("summary_lines")
        def _row(r):  # tolerate {"passed":..,"failed":..,"skipped":..} rows: same three numbers, different container
            if isinstance(r, dict) and {"passed", "failed"} <= set(r) <= {"passed", "failed", "skipped"}:
                return [r["passed"], r["failed"], r.get("skipped", 0)]
            return list(r) if isinstance(r, list) else r
        ss = [_row(r) for r in ss] if isinstance(ss, list) else ss
        norm_ss = ss
        if norm_ss != truth.get("summaries"):
            mm.append(f"summary_lines: spark lists {len(ss) if isinstance(ss, list) else ss!r} entries, parser found {len(truth.get('summaries', []))}; first difference: " + str(next(((i, a, b) for i, (a, b) in enumerate(zip(ss if isinstance(ss, list) else [], truth.get('summaries', []))) if a != b), "length/shape")))
    sf = spark.get("failures")
    if not isinstance(sf, list) or not all(isinstance(x, dict) for x in sf):
        mm.append("failures missing or not a list of objects")
        sf = []
    pf = truth["failures"]
    used = set()
    for x in sf:
        hit = next((i for i, p in enumerate(pf) if i not in used and _name_match(str(x.get("name", "")), p)), None)
        if hit is None:
            mm.append(f"failure not in parser list: {str(x.get('name', ''))[:120]!r}")
            continue
        used.add(hit)
        for fld in ("error", "frame"):
            v = _strip_ell(str(x.get(fld) or ""))
            if v and norm(v) not in raw_norm:
                mm.append(f"failure {fld} not verbatim in raw: {v[:100]!r}")
    if not truth.get("capped"):
        for i, p in enumerate(pf):
            if i not in used:
                mm.append(f"parser failure missing from spark list: {p['name'][:120]!r}")
    an = spark.get("anomalies", [])
    if not isinstance(an, list) or not all(isinstance(a, str) for a in an):
        mm.append("anomalies not a list of strings")
        an = []
    for a in an:
        for num in re.findall(r"\d+", a):
            if len(num) >= 2 and num not in raw_tokens:
                mm.append(f"anomaly number {num} not in raw: {a[:100]!r}")
                break
    return mm


# ------------------------------------------------------------------ delta
def delta(prev, cur):
    if prev.get("kind") != cur["kind"]:
        return {"error": f"kind differs: previous {prev.get('kind')} vs now {cur['kind']}"}
    pc, cc = prev.get("counts", {}), cur["counts"]
    pn = {f["name"] for f in prev.get("failures", [])}
    cn = {f["name"] for f in cur["failures"]}
    return {"newly_failing": sorted(cn - pn), "no_longer_failing": sorted(pn - cn), "still_failing": len(cn & pn),
            "count_changes": {k: [pc.get(k), cc.get(k)] for k in cc if pc.get(k) != cc.get(k)},
            "previous_verdict": prev.get("verdict"), "note": "'no longer failing' = was in the previous failure list, is not in this one (a deleted test looks the same; passing names are not in the raw output)"}


# ------------------------------------------------------------------ render
def render(d):
    c = d["counts"]
    ct = ", ".join(f"{k.replace('_', ' ')} {v}" for k, v in c.items()) if c else "no counts"
    st = d["status"]
    lines = []
    if st == "NO_GROUND_TRUTH":
        lines.append(f"# DIGEST REFUSED: no ground truth ({d['kind']})")
        lines.append("")
        lines.append("**BLUF: the raw output is truncated, garbled or empty. Nothing is claimed. Read the raw file.**")
        for n in d["parser_notes"]:
            lines.append(f"- parser: {n}")
    else:
        lines.append(f"# {d['verdict']}: {ct}")
        lines.append("")
        tag = {"CHECKED": "Spark digest CHECKED: every count, verdict and failure name re-derived from the raw file by the parser.",
               "REFUSED_MISMATCH": "SPARK DIGEST REFUSED (disagreed with the parser): the numbers below are the PARSER's, not the Spark's. Mismatches in check.json.",
               "PARSER_ONLY_SPARK_DOWN": "Spark unreachable or empty: this is the PARSER summary only (" + d.get("spark_error", "") + ").",
               "PARSER_ONLY": "Parser summary only (--no-spark)."}[st]
        lines.append(f"**BLUF:** {tag}")
        lines.append("")
        f = d["failures"]
        lines.append(f"## Failures ({len(f)}{'+, capped' if d.get('capped') else ''})")
        if not f:
            lines.append("none")
        for x in f[:30]:
            lines.append(f"- `{x['name'][:160]}`")
            if x.get("error"):
                lines.append(f"  - error: {x['error'][:120]}")
            if x.get("frame"):
                lines.append(f"  - frame: {x['frame'][:100]}")
        if len(f) > 30:
            lines.append(f"- ... +{len(f) - 30} more in digest.json")
        if st == "CHECKED" and d.get("anomalies"):
            lines.append("")
            lines.append("## Anomalies (Spark, numbers verified present in the raw; wording not verified)")
            for a in d["anomalies"][:8]:
                lines.append(f"- {a}")
        if d.get("delta"):
            dl = d["delta"]
            lines.append("")
            lines.append("## Delta vs previous digest")
            if "error" in dl:
                lines.append(f"- {dl['error']}")
            else:
                lines.append(f"- newly failing ({len(dl['newly_failing'])}): " + ("; ".join(f"`{n[:120]}`" for n in dl["newly_failing"][:15]) or "none"))
                lines.append(f"- no longer failing ({len(dl['no_longer_failing'])}): " + ("; ".join(f"`{n[:120]}`" for n in dl["no_longer_failing"][:15]) or "none"))
                lines.append(f"- still failing: {dl['still_failing']}; count changes: " + (", ".join(f"{k} {a}->{b}" for k, (a, b) in dl["count_changes"].items()) or "none") + f"; previous verdict {dl['previous_verdict']}")
        for n in d["parser_notes"]:
            lines.append(f"- parser note: {n}")
    m = d["meta"]
    lines.append("")
    lines.append(f"_raw {m['raw_bytes']} B -> this digest {{DIGEST_BYTES}} B; sent to Spark {m.get('sent_bytes', 0)} B; Spark {m.get('spark_seconds', 0):.1f}s; status {st}_")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw")
    ap.add_argument("--kind", required=True, choices=KINDS)
    ap.add_argument("--out", required=True)
    ap.add_argument("--delta")
    ap.add_argument("--no-spark", action="store_true")
    a = ap.parse_args()
    try:
        data = open(a.raw, "rb").read()
    except OSError as e:
        print(f"digest: cannot read {a.raw}: {e}", file=sys.stderr)
        return 2
    prev = None
    if a.delta:
        try:
            prev = json.load(open(a.delta))
        except (OSError, ValueError) as e:
            print(f"digest: cannot read --delta file: {e}", file=sys.stderr)
            return 2
    os.makedirs(a.out, exist_ok=True)
    text = data.decode("utf-8", "replace")
    truth = parse(a.kind, text)
    d = {"kind": a.kind, "raw_file": os.path.abspath(a.raw), "counts": truth["counts"], "verdict": truth["verdict"],
         "failures": truth["failures"], "capped": truth["capped"], "parser_notes": truth["notes"], "anomalies": [],
         "spark": None, "meta": {"raw_bytes": len(data), "model": MODEL}}
    chk = {"status": None, "mismatches": [], "spark_called": False}
    rc = 0
    if not truth["complete"] or (b"\x00" in data[:4096]):
        d["status"] = "NO_GROUND_TRUTH"
        if b"\x00" in data[:4096]:
            d["parser_notes"].append("binary content (NUL bytes) in the first 4 KB")
            d["verdict"], d["counts"] = None, {}
        rc = 3
    elif a.no_spark:
        d["status"] = "PARSER_ONLY"
    else:
        sent, note = squeeze(text)
        d["meta"]["sent_bytes"] = len(sent.encode())
        if note:
            d["parser_notes"].append("Spark saw: " + note)
        try:
            chk["spark_called"] = True
            reply, usage, secs = call_spark(build_prompt(a.kind, sent))
            d["meta"].update({"spark_seconds": secs, "usage": usage})
            open(os.path.join(a.out, "spark_response.txt"), "w").write(reply)
            if not reply.strip():
                raise RuntimeError("empty reply (a thinking block or a refusal, not a verdict)")
        except Exception as e:  # noqa: BLE001 - any client failure -> parser summary, said so
            d["status"] = "PARSER_ONLY_SPARK_DOWN"
            d["spark_error"] = f"{type(e).__name__}: {str(e)[:120]}"
        else:
            try:
                sp = extract_json(reply)
                d["spark"] = sp
                raw_norm = norm(clean(text))
                tokens = set(re.findall(r"\d+", clean(text)))
                chk["mismatches"] = check(a.kind, truth, sp, raw_norm, tokens)
            except (ValueError, TypeError) as e:
                chk["mismatches"] = [f"reply not parseable as JSON: {e}"]
            if chk["mismatches"]:
                d["status"] = "REFUSED_MISMATCH"
            else:
                d["status"] = "CHECKED"
                d["anomalies"] = [x for x in (d["spark"].get("anomalies") or [])][:8]
    chk["status"] = d["status"]
    if prev is not None and truth["complete"]:
        d["delta"] = delta(prev, {"kind": a.kind, "counts": d["counts"], "failures": d["failures"]})
    md = render(d)
    n = len(md.replace("{DIGEST_BYTES}", "0").encode())
    for _ in range(3):  # the number's own width changes the length: iterate to a fixed point
        n = len(md.replace("{DIGEST_BYTES}", str(n)).encode())
    md = md.replace("{DIGEST_BYTES}", str(n))
    d["meta"]["digest_bytes"] = len(md.encode())
    open(os.path.join(a.out, "digest.md"), "w").write(md)
    json.dump(d, open(os.path.join(a.out, "digest.json"), "w"), indent=1)
    json.dump(chk, open(os.path.join(a.out, "check.json"), "w"), indent=1)
    print(f"{d['status']} verdict={d['verdict']} raw={len(data)}B digest={d['meta']['digest_bytes']}B spark_s={d['meta'].get('spark_seconds', 0):.1f} out={a.out}")
    for m in chk["mismatches"][:10]:
        print("  mismatch:", m)
    return rc


if __name__ == "__main__":
    sys.exit(main())
