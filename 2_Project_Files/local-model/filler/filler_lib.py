#!/usr/bin/env python3
"""filler_lib.py - gates, prompts and the deterministic CHECKERS of the Spark's standing filler queue (routine (c)).

Kam 2026-11-12 11:36 (live board): "please implement this plan as a standard routine going forward"; 16:36: "lets use the
spark for the tasks identified this morning". Rule: 0_Brain/learnings/2026-11-12_spark-for-harness-and-token-heavy-simple-tasks.md
(3. Not for judgement: the Spark proposes, a script checks; its output is never trusted unchecked).

Two task kinds (v1):
  mutants  given a source file + a line range, the Spark proposes ONE single-change mutant per call as a unified diff;
           check_mutant() applies it with `git apply --check` in a scratch git repo and keeps only a diff that
           (1) is one file, one hunk, the named path, (2) applies, (3) changes only lines inside the range,
           (4) changes behaviour-bearing tokens (comment/whitespace-only edits are refused), (5) is not a duplicate.
  numstat  given a seat's READY mail and a PR number, the Spark extracts the +/- claims the mail makes for that PR into
           JSON; check_numstat() (a) refuses any claim that is not grounded in the mail text (number / path absent from
           the mail), then (b) reconciles the grounded claims against the GitHub API numbers and FLAGS every mismatch.
Python 3 stdlib + the git binary. Never writes outside the filler/ folder; never mail, board, push or Linear.
"""
import hashlib
import json
import os
import re
import subprocess
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
LM = os.path.normpath(os.path.join(HERE, ".."))
SPARK_STATE = os.path.join(LM, "spark", "state")
SPARK_URL = os.environ.get("SPARK_URL", "http://127.0.0.1:47788").rstrip("/")
AB_PATTERN = "spark-ab/ab[.]py"          # [.] so pgrep never matches its own command line


# ------------------------------------------------------------------ gates
def live_pid(lock_dir):
    pf = os.path.join(lock_dir, "pid")
    if not os.path.isfile(pf):
        return None
    try:
        pid = int(open(pf).read().strip())
        os.kill(pid, 0)
        return pid
    except (ValueError, ProcessLookupError, PermissionError, OSError):
        return None


def ab_running():
    """pids of a running A/B harness (spark-ab/ab.py), [] when none."""
    r = subprocess.run(["pgrep", "-f", AB_PATTERN], capture_output=True, text=True)
    return [int(x) for x in r.stdout.split()] if r.returncode == 0 else []


def tunnel_up():
    try:
        with urllib.request.urlopen(SPARK_URL + "/v1/models", timeout=3) as r:
            if r.status != 200:
                return False, "HTTP %s" % r.status
            j = json.load(r)
            ids = [m.get("id") for m in j.get("data", [])]
            return True, ",".join(str(i) for i in ids)
    except Exception as e:  # noqa: BLE001 - any failure is DOWN, with its reason
        return False, type(e).__name__


def gate_reasons_local():
    """The gates that need no network: A/B run, round.lock, queue.lock."""
    why = []
    pids = ab_running()
    if pids:
        why.append("A/B run live (pid %s)" % ",".join(map(str, pids)))
    for name in ("round.lock", "queue.lock"):
        p = live_pid(os.path.join(SPARK_STATE, name))
        if p:
            why.append("spark/state/%s held by pid %d" % (name, p))
    return why


def gate_reasons():
    """[] when the Spark is free for ONE filler task, else the list of reasons it is not."""
    why = gate_reasons_local()
    up, detail = tunnel_up()
    if not up:
        why.append("tunnel DOWN (%s)" % detail)
    return why


# ------------------------------------------------------------------ queue file
QCOLS = ["id", "kind", "input", "status", "result"]


def read_queue(path):
    rows = []
    if not os.path.isfile(path):
        return rows
    for line in open(path, encoding="utf-8"):
        s = line.rstrip("\n")
        if not s.strip() or s.startswith("#") or s.startswith("id\t"):
            continue
        parts = s.split("\t")
        parts += [""] * (len(QCOLS) - len(parts))
        rows.append(dict(zip(QCOLS, parts[:len(QCOLS)])))
    return rows


def write_queue(path, rows, header_comment):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(header_comment)
        f.write("\t".join(QCOLS) + "\n")
        for r in rows:
            f.write("\t".join(r.get(c, "") for c in QCOLS) + "\n")
    os.replace(tmp, path)


# ------------------------------------------------------------------ shared helpers
def extract_diff(text):
    """The first ```diff fenced block's body (or the whole text when it is bare diff grammar). None when absent."""
    m = re.search(r"```(?:diff|patch)?[ \t]*\n(.*?)\n?```", text, re.S)
    body = m.group(1) if m else text.strip()
    return body + "\n" if body.startswith("--- ") else None


def strip_code(text):
    """Behaviour-bearing view of source: // and /* */ comments and all whitespace removed."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"(?m)(^|[^:\"'`])//[^\n]*", r"\1", text)
    return re.sub(r"\s+", "", text)


def parse_single_hunk(diff, rel_path):
    """-> (ok, reason, info). One file (path must equal rel_path), exactly one hunk, 1-2 removed lines, <=2 added."""
    lines = diff.rstrip("\n").split("\n")
    if len(lines) < 4 or not lines[0].startswith("--- ") or not lines[1].startswith("+++ "):
        return False, "not a unified diff (no ---/+++ header)", None
    a, b = lines[0][4:].split("\t")[0].strip(), lines[1][4:].split("\t")[0].strip()
    if a != "a/" + rel_path or b != "b/" + rel_path:
        return False, "wrong path: %r / %r (want a/%s)" % (a, b, rel_path), None
    hunks = [i for i, l in enumerate(lines) if l.startswith("@@")]
    if len(hunks) != 1:
        return False, "%d hunks (a single-change mutant has exactly 1)" % len(hunks), None
    if any(l.startswith(("--- ", "+++ ")) for l in lines[2:] if l.startswith(("--- a/", "+++ b/"))):
        return False, "more than one file section", None
    m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", lines[hunks[0]])
    if not m:
        return False, "malformed hunk header", None
    body = lines[hunks[0] + 1:]
    removed = [l[1:] for l in body if l.startswith("-")]
    added = [l[1:] for l in body if l.startswith("+")]
    if not (1 <= len(removed) <= 2) or len(added) > 2:
        return False, "changes %d removed / %d added lines (want 1-2 removed, at most 2 added)" % (len(removed), len(added)), None
    return True, "", {"start": int(m.group(1)), "removed": removed, "added": added}


def git(args, cwd, stdin=None):
    r = subprocess.run(["git", "-C", cwd] + args, capture_output=True, text=True, input=stdin)
    return r.returncode, (r.stdout + r.stderr).strip()


# ------------------------------------------------------------------ mutants checker
def check_mutant(out_text, orig_text, rel_path, lo, hi, scratch, seen_hashes):
    """Verdict for ONE proposed mutant. -> dict {accepted: bool, reason, applied_via, changed, patch, result_hash}.
    scratch: a directory this function owns (made a git repo on first use; the file is re-written each call)."""
    res = {"accepted": False, "reason": "", "applied_via": None, "changed": None, "patch": None, "result_hash": None}
    diff = extract_diff(out_text)
    if diff is None:
        res["reason"] = "no unified diff in the reply"
        return res
    ok, why, info = parse_single_hunk(diff, rel_path)
    if not ok:
        res["reason"] = why
        return res
    os.makedirs(scratch, exist_ok=True)
    if not os.path.isdir(os.path.join(scratch, ".git")):
        git(["init", "-q"], scratch)
    target = os.path.join(scratch, rel_path)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(orig_text)
    pf = os.path.join(scratch, ".mutant.patch")
    with open(pf, "w", encoding="utf-8") as f:
        f.write(diff)
    via = None
    for flags, tag in (([], "strict"), (["--recount"], "recount"), (["--unidiff-zero"], "u0"), (["--unidiff-zero", "--recount"], "u0+recount")):
        rc, msg = git(["apply", "--check"] + flags + [".mutant.patch"], scratch)
        if rc == 0:
            via = tag
            rc2, msg2 = git(["apply"] + flags + [".mutant.patch"], scratch)
            if rc2 != 0:
                res["reason"] = "apply --check passed but apply failed: " + msg2[:200]
                return res
            break
        last = msg
    if via is None:
        res["reason"] = "git apply --check refused: " + last[:200].replace("\n", " ")
        return res
    with open(target, encoding="utf-8") as tf:
        new_text = tf.read()
    # where did the file change? compare original/new line by line (diff of equal-prefix / equal-suffix)
    ol, nl = orig_text.split("\n"), new_text.split("\n")
    i = 0
    while i < min(len(ol), len(nl)) and ol[i] == nl[i]:
        i += 1
    j = 0
    while j < min(len(ol), len(nl)) - i and ol[-1 - j] == nl[-1 - j]:
        j += 1
    first, last_ = i + 1, len(ol) - j          # 1-based original line span that changed
    if last_ < first:                          # pure insertion: not a mutant of existing code
        res["reason"] = "pure insertion, no original line changed"
        return res
    if first < lo or last_ > hi:
        res["reason"] = "changes original lines %d-%d, outside the target range %d-%d" % (first, last_, lo, hi)
        return res
    if strip_code(orig_text) == strip_code(new_text):
        res["reason"] = "comment/whitespace-only change: no behaviour-bearing token changed"
        return res
    h = hashlib.sha256(new_text.encode()).hexdigest()[:16]
    if h in seen_hashes:
        res["reason"] = "duplicate of an earlier accepted mutant (same resulting file)"
        return res
    res.update(accepted=True, applied_via=via, changed=[first, last_], patch=diff, result_hash=h,
               reason="applies (%s), changes original lines %d-%d inside %d-%d, token change real" % (via, first, last_, lo, hi))
    return res


OPERATORS = [
    "change a comparison operator or a comparison constant (for example > to >=, or 0 to 1)",
    "change a logical operator (&& to ||, or negate a condition)",
    "remove a method call or a chained call such as .trim() or .toUpperCase(), keeping the rest of the line",
    "change a numeric or string literal by one step (a bound, a limit, a delimiter)",
    "swap one identifier or argument for another already used on a nearby line",
]


def mutant_prompt(task, source_lines, used):
    lo, hi = task["lines"]
    ex_lo, ex_hi = max(1, lo - 3), min(len(source_lines), hi + 3)
    op = OPERATORS[len(used) % len(OPERATORS)]
    text = (
        "Produce ONE mutant of the source file named in the input: a single behaviour-changing edit, as a unified diff.\n"
        "Rules: the diff touches ONLY the file path %(path)s (use '--- a/%(path)s' and '+++ b/%(path)s'); exactly ONE hunk; "
        "remove 1 line (at most 2) and add 1 line (at most 2); every changed line is an ORIGINAL line numbered between %(lo)d and %(hi)d "
        "inclusive; do not edit comments or whitespace; use NO context lines at all (a zero-context diff: the hunk holds only the '-' and '+' lines, "
        "header '@@ -N,K +N,K @@' where N is the ORIGINAL line number of the first removed line and K the number of removed/added lines); "
        "the '-' lines must be copied exactly from the excerpt; "
        "write the new line so the change is a real change of behaviour (the code should still read as valid TypeScript).\n"
        "Kind of change to make this time: %(op)s.\n"
        "Do NOT repeat any mutant listed under already_used. Emit exactly one fenced diff block and nothing else."
    ) % {"path": task["rel_path"], "lo": lo, "hi": hi, "op": op}
    inp = {
        "path": task["rel_path"],
        "target_line_range": [lo, hi],
        "excerpt_numbered": ["%d: %s" % (n, source_lines[n - 1]) for n in range(ex_lo, ex_hi + 1)],
        "already_used": used,
    }
    return text, inp


# ------------------------------------------------------------------ numstat checker
def _digits_in(text):
    """All whole numbers present in text (commas inside a number removed: 3,131 -> 3131)."""
    t = re.sub(r"(?<=\d),(?=\d{3}\b)", "", text)
    return set(int(x) for x in re.findall(r"(?<![\w.])\d+(?![\w])", t))


def numstat_prompt(task, mail_text):
    text = (
        "A seat's READY mail is given in the input. Extract the line-count claims the MAIL ITSELF makes for pull request %(pr)d: "
        "the PR's total files, total added lines and total removed lines, and the added/removed counts it states per file. "
        "Write them as ONE JSON object and nothing else, no code fence, in exactly this shape: "
        '{"pr": %(pr)d, "files_changed": <int or null>, "additions": <int or null>, "deletions": <int or null>, '
        '"files": [{"path": "<path as written in the mail>", "additions": <int or null>, "deletions": <int or null>}]}. '
        "Use null for anything the mail does not state for this PR; never compute or estimate a number; copy numbers exactly as the "
        "mail writes them (a figure such as +68/-2 means additions 68, deletions 2; 'files 5' means files_changed 5). "
        "Per-file entries only for files the mail names with a count; an empty list when there are none. "
        # 2026-11-13 (F15, F16 REJECTED_UNGROUNDED): the model pinned a GROUP's count ('ten tsconfig.json files (+18 -28
        # together)') on one file and turned a description ('a flow fragment') into a path. Two explicit rules below.
        "A count the mail gives for a GROUP of files ('ten files ... together', 'the two fragments', 'plus a flow and a cheat "
        "fragment (+29 and +21)' without their paths) is NOT a per-file count: leave those files out of the list entirely. "
        "A path is a file path copied character for character from the mail (it contains a '/' or a file extension); "
        "a description such as 'flow fragment' or 'the lock' is never a path. "
        # 2026-11-13 (F17): the model used the count text '+117 -0' as a path for 'one new test file (+117 -0)'.
        "A count given for a file the mail does not name by path (for example 'plus one new test file (+117 -0)') is "
        "left out of the list; a count such as '+117 -0' is never a path. "
        "Ignore every other pull request in the mail."
    ) % {"pr": task["pr"]}
    return text, {"pr": task["pr"], "mail": mail_text}


def parse_claim_json(text):
    s = text.strip()
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    a, b = s.find("{"), s.rfind("}")
    if a < 0 or b <= a:
        raise ValueError("no JSON object in the reply")
    return json.loads(s[a:b + 1])


def _claim_ints(c):
    """Every number the claim asserts, as a list of (label, int)."""
    out = []
    for k in ("files_changed", "additions", "deletions"):
        if c.get(k) is not None:
            out.append((k, c[k]))
    for f in c.get("files") or []:
        for k in ("additions", "deletions"):
            if f.get(k) is not None:
                out.append(("%s.%s" % (f.get("path"), k), f[k]))
    return out


def check_numstat(claim, mail_text, pr_meta, pr_files, pr):
    """-> dict {verdict, grounding:[problems], mismatches:[...], matched:[...]}.
    verdict: REJECTED_UNGROUNDED (a claimed number/path is not in the mail, or the shape is wrong: the Spark is not trusted)
             MISMATCH (grounded in the mail but disagrees with the API: the SEAT's claim is flagged)
             MATCH (every claim equals the API) | NO_CLAIMS (the mail states no counts for this PR)."""
    ground = []
    if not isinstance(claim, dict) or claim.get("pr") != pr:
        return {"verdict": "REJECTED_UNGROUNDED", "grounding": ["claim JSON is not an object for pr %s" % pr], "mismatches": [], "matched": []}
    for k in ("files_changed", "additions", "deletions"):
        v = claim.get(k)
        if v is not None and (not isinstance(v, int) or isinstance(v, bool)):
            ground.append("%s is not an integer or null: %r" % (k, v))
    if not isinstance(claim.get("files", []), list):
        ground.append("files is not a list")
        return {"verdict": "REJECTED_UNGROUNDED", "grounding": ground, "mismatches": [], "matched": []}
    present = _digits_in(mail_text)
    for label, v in _claim_ints(claim):
        if isinstance(v, int) and v not in present:
            ground.append("%s = %s does not occur anywhere in the mail" % (label, v))
    mail_norm = mail_text
    for f in claim.get("files") or []:
        p = f.get("path") or ""
        base = os.path.basename(p)
        if not base or base not in mail_norm:
            ground.append("file path %r (basename %r) does not occur in the mail" % (p, base))
        else:
            # each count claimed for the file must sit within 200 chars after one of the file's mentions
            wins = [_digits_in(mail_norm[m.end():m.end() + 200]) for m in re.finditer(re.escape(base), mail_norm)]
            for k in ("additions", "deletions"):
                if isinstance(f.get(k), int) and not any(f[k] in w for w in wins):
                    ground.append("%s.%s = %s is not stated next to %r in the mail" % (p, k, f[k], base))
        for k in ("additions", "deletions"):
            if f.get(k) is not None and (not isinstance(f[k], int) or isinstance(f[k], bool)):
                ground.append("%s.%s is not an integer or null" % (p, k))
    if ground:
        return {"verdict": "REJECTED_UNGROUNDED", "grounding": ground, "mismatches": [], "matched": []}
    mism, matched = [], []

    def cmp(label, claimed, actual):
        (matched if claimed == actual else mism).append("%s: mail says %s, API says %s" % (label, claimed, actual))

    n_claims = 0
    for k, api in (("files_changed", pr_meta["changed_files"]), ("additions", pr_meta["additions"]), ("deletions", pr_meta["deletions"])):
        if claim.get(k) is not None:
            n_claims += 1
            cmp(k, claim[k], api)
    used = set()
    for f in claim.get("files") or []:
        p = f["path"]
        toks = [t for t in re.split(r"[\s,;]+", p) if t]
        hits = [a for a in pr_files if a["filename"] == p or a["filename"].endswith("/" + p)
                or os.path.basename(a["filename"]) in ([os.path.basename(p)] + toks)]
        if len(hits) == 1:                      # the mail's wording resolves to exactly one API file: compare that file
            used.add(hits[0]["filename"])
            for k in ("additions", "deletions"):
                if f.get(k) is not None:
                    n_claims += 1
                    cmp("%s.%s" % (os.path.basename(hits[0]["filename"]), k), f[k], hits[0][k])
            continue
        # a descriptor such as 'new test' (not a path): the claim must still be true of SOME unused API file
        n_claims += 1
        cand = [a for a in pr_files if a["filename"] not in used
                and all(f.get(k) is None or f[k] == a[k] for k in ("additions", "deletions"))]
        label = "%r +%s -%s" % (p, f.get("additions"), f.get("deletions"))
        if cand:
            used.add(cand[0]["filename"])
            matched.append("%s: no unique path match; an API file has those counts (%s)" % (label, os.path.basename(cand[0]["filename"])))
        else:
            mism.append("%s: no API file has those counts (path matched %d files)" % (label, len(hits)))
    if n_claims == 0:
        return {"verdict": "NO_CLAIMS", "grounding": [], "mismatches": [], "matched": []}
    return {"verdict": "MISMATCH" if mism else "MATCH", "grounding": [], "mismatches": mism, "matched": matched}
