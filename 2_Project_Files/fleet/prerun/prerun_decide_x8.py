#!/usr/bin/env python3
"""Seat X 8th: which push path does a pre-run record earn? Wednesday's GAP 1 ruling (ANSWER 2026-11-06 06:34:04Z), inside Kam's card secuura-push-queue-prerun-preflight-1106 = a. Derived from Seat X 6th's prerun_decide_x6.py after gate 227 (F2, F4, F10, F15).
usage: prerun_decide_x8.py decide RECORD PUSH_SHA --branch B --worktree W --cells-file F [--max-age 7200] [--now EPOCH] [--out DECISION.json]
       prerun_decide_x8.py live WORKTREE      (X8, gate 237 N4b: exit 0 + `LIVE-CHECK LIVE slot=n pid=p wt=W`, or exit 1 + `LIVE-CHECK NONE wt=W`; anything else is an instrument error)
exit 0   QUALIFIES -> the --no-verify push of the explicit sha
exit 10  FALL BACK -> today's push, the hook under the lock. Record too old, for another sha, count differs from the file, hook differs from the pin, PRERUN_DISABLE set, or ANY other reason that is
                      not a FAILED pre-run. A fallback never removes a guard: the hook runs.
exit 5   REFUSE    -> the record is about THIS push (same sha, branch, worktree) and shows a FAILED pre-run: rc 1 to 127, verdict 'PREFLIGHT FAILED', a shell-suites line or run_shell_suites with failures, or the format gate
                      run and failed. The hook would refuse it too. A pre-run killed by a signal is not a failure (F15): it falls back.
exit 70  the library prerun_x8.py next to this file is not the pinned one (sha256 below): nothing is decided.
any other exit is an INSTRUMENT error; the driver falls back.
F2: an exit code is not a decision. The LAST stdout line is the positive statement `DECISION path=<path> sha=<sha> branch=<branch>`, printed only after the matching decision.json is written; the driver reads both, and pins this file's sha.
The pushed sha is NOT taken from the record's claim alone: this tool reads git itself (HEAD, the checked-out branch, the branch tip, whether the tree is clean, the hook blob at the pushed commit)."""
import argparse, datetime as dt, hashlib, importlib.util, json, os, re, subprocess, sys, time

PIN = "338b5d98afb255ec26da0a5d5db575ba41775412bcbef0bb5bb019f7c16f1cea"        # prerun_x8.py; stamped by rekey_push_x8.py
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "prerun_x8.py")
HOOK_PIN_FILE = os.path.join(HERE, "prerun_expected_hook_x8.txt")     # F10: beside the tool, one line, the sha256 of .githooks/pre-push; Wednesday edits it after a MERGED that changes the hook, having re-read that the refusals are still covered


def load_lib():
    try:
        raw = open(LIB, "rb").read()
    except OSError as e:
        print(f"REFUSED: cannot read {LIB}: {e}")
        sys.exit(70)
    if hashlib.sha256(raw).hexdigest() != PIN:
        print(f"REFUSED: {LIB} is not the pinned prerun_x8.py (sha256 {hashlib.sha256(raw).hexdigest()[:16]}..., pin {PIN[:16]}...); nothing is decided")
        sys.exit(70)
    spec = importlib.util.spec_from_file_location("prerun_x8", LIB)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(wt, *a):
    return subprocess.run(["git", "--no-optional-locks", "-C", wt] + list(a), capture_output=True, text=True)


def hook_pin_reason(worktree, push_sha):
    """F10: the hook AT THE PUSHED COMMIT against the pin. Different, missing or unreadable: the pre-run cannot vouch for checks it was never told about."""
    try:
        want = open(HOOK_PIN_FILE).read().strip()
    except OSError as e:
        return f"the hook pin file {HOOK_PIN_FILE} is unreadable ({type(e).__name__})"
    if not re.fullmatch(r"[0-9a-f]{64}", want):
        return f"the hook pin file {HOOK_PIN_FILE} does not hold one sha256"
    p = subprocess.run(["git", "--no-optional-locks", "-C", worktree, "show", f"{push_sha}:.githooks/pre-push"], capture_output=True)
    if p.returncode != 0:
        return f"cannot read .githooks/pre-push at {push_sha[:12]}"
    got = hashlib.sha256(p.stdout).hexdigest()
    return None if got == want else f".githooks/pre-push at {push_sha[:12]} is sha256 {got[:16]}..., the pin in {HOOK_PIN_FILE} is {want[:16]}...; a different hook takes the hook path"


def is_signal_death(rc):
    return isinstance(rc, int) and (rc < 0 or rc >= 128)


def failure_evidence(P, rec):
    """Reasons this record shows a FAILED pre-run. Each read is defensive: an unreadable field is no evidence (the record then falls back). A pre-run killed by a signal shows no failure unless its own verdict says FAILED (F15)."""
    ev = []
    rc = rec.get("rc")
    if isinstance(rc, int) and rc != 0 and not is_signal_death(rc):
        ev.append(f"preflight rc {rc}")
    fg = rec.get("format_gate")
    if isinstance(fg, dict) and fg.get("ran") and isinstance(fg.get("rc"), int) and fg["rc"] != 0 and not is_signal_death(fg["rc"]):
        ev.append(f"systemTest format gate rc {fg['rc']}")
    try:
        pr = P.parse_output(open(rec["output"], errors="replace").read())      # re-read from the output file, like qualify; rec["parsed"] is ignored
    except Exception:
        pr = {}
    if str(pr.get("verdict") or "").startswith("PREFLIGHT FAILED"):
        ev.append("verdict " + pr["verdict"][:60])
    if not is_signal_death(rc):                                                # a killed run's partial output proves nothing about a whole run
        sl = pr.get("suites_line")
        if sl and sl[1] > 0:
            ev.append(f"shell suites: {sl[1]} failed")
        rs = pr.get("run_shell_suites")
        if rs and rs[1] > 0:
            ev.append(f"run_shell_suites: {rs[1]} failed")
    return ev


def decide(P, rec_path, push_sha, branch, worktree, cells_file, max_age, now):
    """-> (path, [(rule, why)], rec). path is 'no-verify', 'hook' or 'refuse'."""
    reasons, rec = [], None
    if "PRERUN_DISABLE" in os.environ:                                         # F4: set at all, even empty: nothing is trusted
        reasons.append(("env", "PRERUN_DISABLE is set in this environment; it is a test knob and earns no fast path"))
    # git first, independent of the record: is the worktree really at the sha that will be pushed?
    hp, cp, tp, sp = (git(worktree, "rev-parse", "HEAD"), git(worktree, "symbolic-ref", "--short", "-q", "HEAD"),
                      git(worktree, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"), git(worktree, "status", "--porcelain"))
    head, cur, tip, dirty = hp.stdout.strip(), cp.stdout.strip(), tp.stdout.strip(), sp.stdout.strip()
    # X8 (gate 237 N1): an exit code is read for every one of these. A read that fails cannot vouch for the tree: the record does not qualify (hook path), and it is never failure evidence.
    failed = [f"git {n} rc {p.returncode}" for n, p, ok in (("rev-parse HEAD", hp, (0,)), ("symbolic-ref HEAD", cp, (0, 1)), (f"rev-parse refs/heads/{branch}", tp, (0,)), ("status", sp, (0,))) if p.returncode not in ok]
    if failed:
        reasons.append(("git", "a read of the worktree failed, so it cannot be shown clean and at the pushed sha: " + "; ".join(failed) + f" [{(sp.stderr or hp.stderr).strip()[:120]}]"))
    elif head != push_sha or tip != push_sha or cur != branch or dirty:
        reasons.append(("git", f"worktree HEAD {head[:12]} / branch tip {tip[:12]} / checked out [{cur}] / dirty={bool(dirty)}, asked to push {push_sha[:12]} on {branch}"))
    hook = hook_pin_reason(worktree, push_sha)
    if hook:
        reasons.append(("hook_pin", hook))
    try:
        rec = json.load(open(rec_path))
    except Exception as e:
        reasons.append(("wellformed", f"record {rec_path!r} unreadable ({type(e).__name__})"))
    cells = None
    try:
        cells = P.read_cells(cells_file)[0]                             # X8 (gate 237 N5): line 1 is the count; the blob line after it is `run`'s
    except Exception as e:
        reasons.append(("cells", f"expected cell count file {cells_file!r} is missing, unreadable or not one integer ({type(e).__name__})"))
    if rec is not None:
        try:
            for x in P.qualify(rec, push_sha, now, max_age, cells, branch, worktree):
                reasons.append((x.split(":")[0], x.split(":", 1)[1].strip()))
        except Exception as e:
            reasons.append(("wellformed", f"record could not be judged ({type(e).__name__}: {e})"))
    if any(r == "cells" for r, _ in reasons):
        reasons.append(("cells-file", f"the expected count is read from {cells_file}; Wednesday edits it after a MERGED that changes the cell count"))
    if not reasons:
        return "no-verify", reasons, rec
    about_this = (isinstance(rec, dict) and rec.get("sha") == push_sha and rec.get("sha_end") == push_sha and rec.get("branch") == branch
                  and os.path.realpath(str(rec.get("worktree", ""))) == os.path.realpath(worktree))
    if about_this:
        ev = failure_evidence(P, rec)
        if ev:
            return "refuse", [("failed", e) for e in ev] + reasons, rec
    return "hook", reasons, rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("decide")
    a.add_argument("record"); a.add_argument("push_sha"); a.add_argument("--branch", required=True); a.add_argument("--worktree", required=True)
    a.add_argument("--cells-file", required=True); a.add_argument("--max-age", type=int, default=7200); a.add_argument("--now", type=float); a.add_argument("--out")
    lv = sp.add_parser("live"); lv.add_argument("worktree")          # X8 (gate 237 N4b): is a pre-run live in this worktree? Read by the push driver, which pins this file
    o = ap.parse_args()
    P = load_lib()
    if o.cmd == "live":
        # The answer is a STATEMENT on the last stdout line AND an exit code (F2's rule): exit 0 + `LIVE-CHECK LIVE slot=<n> pid=<p> wt=<wt>`, or exit 1 + `LIVE-CHECK NONE wt=<wt>`.
        # Anything else (a crash also exits 1, but prints no statement) is an instrument error to the driver.
        wt = os.path.realpath(o.worktree); hits = P.live_in_tree(wt)
        if hits:
            print(f"LIVE-CHECK LIVE slot={hits[0][0]} pid={hits[0][1]} wt={wt}"); sys.exit(0)
        print(f"LIVE-CHECK NONE wt={wt}"); sys.exit(1)
    path, reasons, rec = decide(P, o.record, o.push_sha, o.branch, o.worktree, o.cells_file, o.max_age, o.now or time.time())
    word = {"no-verify": "QUALIFIES", "hook": "FALL BACK", "refuse": "REFUSE"}[path]
    print(word)
    for r, w in reasons:
        print(f"  {r}: {w}")
    print(f"DECISION-DETAIL rules={','.join(sorted({r for r, _ in reasons})) or '-'} cells_file={o.cells_file}")
    if o.out:
        json.dump(dict(path=path, sha=o.push_sha, branch=o.branch, reasons=reasons, record=o.record, cells_file=o.cells_file, at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")), open(o.out, "w"), indent=1)
    print(f"DECISION path={path} sha={o.push_sha} branch={o.branch}")          # LAST, after the file: this line is the decision the driver reads
    sys.exit({"no-verify": 0, "hook": 10, "refuse": 5}[path])
