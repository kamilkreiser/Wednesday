#!/usr/bin/env python3
"""Seat X 8th: the line a seat pastes into its PR, written from the PUSH RESULT and the hook's own output (gate 227 F11; Kam's ruling on card secuura-push-queue-prerun-preflight-1106: each PR states --no-verify and which checks ran).
usage: prerun_prline_x8.py --path noverify|hook --push-rc N --origin-sha S --sha S --branch B --push-out F --decision F --status F [--why TEXT]
It is NOT part of the decide tool, so a broken decide cannot write this line. Every case that is not a verified landing prints a plain `NO PR LINE: ...`: a reader never has to guess which case it holds. Exit 0 whenever it printed a line of either kind."""
import argparse, hashlib, importlib.util, json, os, re, sys

PIN = "338b5d98afb255ec26da0a5d5db575ba41775412bcbef0bb5bb019f7c16f1cea"        # prerun_x8.py; stamped by rekey_push_x8.py
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "prerun_x8.py")
VERDICT = re.compile(r"(?m)^(PREFLIGHT (?:PASSED|FAILED|INCOMPLETE|ABORTED).*)$")


def no_line(why, status):
    print(f"NO PR LINE: {why}. Read {status}.")
    return 0


def load_lib():
    raw = open(LIB, "rb").read()
    if hashlib.sha256(raw).hexdigest() != PIN:
        return None
    spec = importlib.util.spec_from_file_location("prerun_x8", LIB); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    for a in ("path", "push-rc", "origin-sha", "sha", "branch", "push-out", "decision", "status"):
        ap.add_argument("--" + a, required=True)
    ap.add_argument("--why", default="")
    o = ap.parse_args()
    if o.push_rc != "0" or o.origin_sha != o.sha:
        return no_line(f"the push did not land verifiably (path {o.path}, push rc {o.push_rc}, origin holds [{o.origin_sha[:12]}], expected {o.sha[:12]})", o.status)
    if o.path == "noverify":
        try:
            d = json.load(open(o.decision))
            P = load_lib()
            if P is None:
                return no_line(f"pushed with --no-verify, verified, but {LIB} is not the pinned library, so which checks ran cannot be stated from the record", o.status)
            if d.get("path") != "no-verify" or d.get("sha") != o.sha or d.get("branch") != o.branch:
                return no_line(f"pushed with --no-verify, verified, but {o.decision} does not state that decision for this sha and branch", o.status)
            print(P.pr_line(json.load(open(d["record"]))))
            return 0
        except Exception as e:
            return no_line(f"pushed with --no-verify, verified, but the record could not be read ({type(e).__name__})", o.status)
    if o.path != "hook":
        return no_line(f"unknown push path [{o.path}]", o.status)
    try:
        text = open(o.push_out, errors="replace").read()
    except OSError as e:
        return no_line(f"pushed, verified, but {o.push_out} could not be read ({type(e).__name__})", o.status)
    banner = "running preflight gate" in text
    vs = VERDICT.findall(text)
    fmt = [l.replace("remote: ", "")[:200] for l in text.splitlines() if "[format-gate]" in l and re.search(r"SKIP|package\(s\) checked|NOTHING CHECKED", l)]
    fmts = ("; systemTest format gate: " + "; ".join(fmt)) if fmt else "; no format-gate summary line in its output"
    why = f" The pre-run was not used: {o.why[:300]}." if o.why else ""
    if banner and vs:
        s = re.findall(r"(?m)^shell suites: (\d+) passed, (\d+) failed, (\d+) skipped \(of (\d+)\)$", text)
        sl = (f"; shell suites {s[-1][0]} passed, {s[-1][1]} failed, {s[-1][2]} skipped (of {s[-1][3]})") if s else ""
        print(f"Pushed through the pre-push hook under the push lock, without --no-verify. The hook ran the preflight at push time on {o.sha[:12]}: {vs[-1].rstrip('.')}{sl}{fmts}.{why}")
        return 0
    if not banner and not vs:
        # The hook's reason, not a guess at it: every skip it has prints its own note (already on the remote, a tag, not a commit). Only the exit at line 372, nothing under Blockchain/Dev changed, is silent.
        notes = [l.split("[pre-push] note: ", 1)[1][:200] for l in text.splitlines() if "[pre-push] note: " in l]
        said = ("its own note: " + "; ".join(notes)) if notes else f"it found no Blockchain/Dev change in this push on {o.sha[:12]}"
        print(f"Pushed through the pre-push hook under the push lock, without --no-verify. The hook ran no preflight: {said}{fmts}.{why}")
        return 0
    return no_line("pushed, verified, but the hook's output is not a shape this tool can state (a preflight banner without a verdict, or a verdict without a banner)", o.status)


if __name__ == "__main__":
    sys.exit(main())
