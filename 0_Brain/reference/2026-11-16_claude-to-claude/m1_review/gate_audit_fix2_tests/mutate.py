#!/usr/bin/env python3
"""Mutation driver for the independent check of M3 AUDIT-FIX2. Usage:
  mutate.py <area> <set> [ids...]
Applies ONE textual mutant at a time to the work tree (from a pristine copy), runs the chosen
tests in release, records pass/fail per test target, restores the file. Writes <area>/logs/mut/."""
import os, subprocess, sys, shutil, re

AREA = sys.argv[1]
SET = sys.argv[2]
ONLY = set(sys.argv[3:])
WORK = os.path.join(AREA, "work")
SRC = os.path.join(WORK, "crates/coagent-audit/src/session.rs")
TST = os.path.join(WORK, "crates/coagent-audit/tests/fix_qam1_seat.rs")
LOG = os.path.join(AREA, "logs/mut")
os.makedirs(LOG, exist_ok=True)

SEAT_COND = '''        if !cfg!(coagent_audit_red = "limits_strand_seat")
            && !self.allowances_owing_a_checkpoint().is_empty()
        {'''
B = "s_b + CLOSING_CHECKPOINT_BYTES > l_b ||"
R = "s_r + CLOSING_CHECKPOINT_RECORDS > l_r {"
SRC_MUTANTS = [
    ("M01", "seat clause removed", SEAT_COND, SEAT_COND.replace('!cfg!(coagent_audit_red = "limits_strand_seat")', "false")),
    ("M02", "seat bytes > to >= (strict by one)", B, "s_b + CLOSING_CHECKPOINT_BYTES >= l_b ||"),
    ("M03", "seat records > to >= (strict by one)", R, "s_r + CLOSING_CHECKPOINT_RECORDS >= l_r {"),
    ("M04", "seat bytes lenient by one", B, "s_b + CLOSING_CHECKPOINT_BYTES - 1 > l_b ||"),
    ("M05", "seat records lenient by one", R, "s_r + CLOSING_CHECKPOINT_RECORDS > l_r + 1 {"),
    ("M06", "seat clause bytes only", "|| s_r + CLOSING_CHECKPOINT_RECORDS > l_r {", "|| (s_r > usize::MAX - 1) {"),
    ("M07", "seat clause records only", "if s_b + CLOSING_CHECKPOINT_BYTES > l_b || s_r", "if (s_b > usize::MAX - 1) || s_r"),
    ("M08", "wrong slot: seat of slot 0", "let (s_b, s_r) = self.seat_usage(self.local_slot());", "let (s_b, s_r) = self.seat_usage(0);"),
    ("M09", "own records only (S-own)", "let (s_b, s_r) = self.seat_usage(self.local_slot());", "let (s_b, s_r) = self.own_usage();"),
    ("M10", "applied when nothing is owed", SEAT_COND, SEAT_COND.replace("&& !self.allowances_owing_a_checkpoint().is_empty()", "&& true")),
    ("M11", "applied to raises only", SEAT_COND, SEAT_COND.replace("&& !self.allowances_owing_a_checkpoint().is_empty()", "&& !self.allowances_owing_a_checkpoint().is_empty()\n            && (new.bytes > self.limits.bytes || new.records > self.limits.records)")),
    ("M12", "applied to lowerings only", SEAT_COND, SEAT_COND.replace("&& !self.allowances_owing_a_checkpoint().is_empty()", "&& !self.allowances_owing_a_checkpoint().is_empty()\n            && (new.bytes < self.limits.bytes || new.records < self.limits.records)")),
    ("M13", "seat checked against the OLD limits", "let (l_b, l_r) = new.per_peer();", "let (l_b, l_r) = self.limits.per_peer();"),
    ("M14", "seat checked against the own seat (own_reserved)", "let (l_b, l_r) = new.per_peer();", "let (l_b, l_r) = new.own_reserved();"),
    ("M15", "clause (A) bytes > to >=", "if u.0 + CLOSING_CHECKPOINT_BYTES > alw.0", "if u.0 + CLOSING_CHECKPOINT_BYTES >= alw.0"),
    ("M16", "clause (A) looks at one owing allowance only (highest slot)", "for s in self.allowances_owing_a_checkpoint() {", "for s in self.allowances_owing_a_checkpoint().into_iter().rev().take(1) {"),
    ("M17", "clause (A) records part dropped", "\n                    || u.1 + CLOSING_CHECKPOINT_RECORDS > alw.1", ""),
]
REC_MUTANTS = [
    ("R1", "recogniser condition (i) dropped",
     "    let prev = match restarted {\n        Some(p) if in_force == d => p,",
     "    let _ = in_force;\n    let prev = match restarted.or(Some(d)) {\n        Some(p) => p,"),
    ("R2", "recogniser condition (ii) dropped", "    if !short || !fits(seat, d.per_peer()) {", "    if false && (!short || !fits(seat, d.per_peer())) {"),
    ("R3", "recogniser condition (iii) dropped", "    if set != Ok(()) || cp != Ok(y.own().seq()) {", "    if false && (set != Ok(()) || cp != Ok(y.own().seq())) {"),
]

ENV = dict(os.environ)
ENV["CARGO_TARGET_DIR"] = os.path.join(AREA, "target_work")
MAN = os.path.join(WORK, "Cargo.toml")

def run_tests(tag, targets, red=None, extra=None):
    env = dict(ENV)
    env.pop("COAGENT_AUDIT_RED", None)
    if red:
        env["COAGENT_AUDIT_RED"] = red
    res = {}
    for t in targets:
        cmd = ["cargo", "test"] + ([] if red else ["--release"]) + ["--locked", "--manifest-path", MAN, "-p", "coagent-audit", "--test", t]
        if extra and t in extra:
            cmd += [extra[t]]
        cmd += ["--", "--nocapture"]
        p = subprocess.run(cmd, env=env, capture_output=True, text=True)
        out = p.stdout + p.stderr
        lf = os.path.join(LOG, f"{tag}.{t}{'.' + red if red else ''}.log")
        open(lf, "w").write(out)
        if "error[E" in out or "could not compile" in out:
            res[t] = "COMPILE-ERROR"
        else:
            res[t] = "pass" if p.returncode == 0 else "FAIL"
            fails = re.findall(r"^    (\S+)$", out.split("failures:")[-1], re.M) if p.returncode else []
            if fails:
                res[t] += "(" + ",".join(sorted(set(fails)))[:400] + ")"
    return res

def apply(path, old, new):
    s = open(path).read()
    if s.count(old) != 1:
        raise SystemExit(f"mutant text found {s.count(old)} times in {path}: {old[:60]!r}")
    open(path, "w").write(s.replace(old, new))

if SET == "src":
    targets = ["fix_qam1_seat", "fix_r5m1_limits", "qa_fix", "gate_r5", "gate_r4", "fix_notes_pinned", "qa_fix2"]
    pristine = open(SRC).read()
    for mid, what, old, new in SRC_MUTANTS:
        if ONLY and mid not in ONLY:
            continue
        try:
            apply(SRC, old, new)
            r = run_tests(mid, targets)
        finally:
            open(SRC, "w").write(pristine)
        line = f"{mid} | {what} | " + " ; ".join(f"{k}={v}" for k, v in r.items())
        print(line, flush=True)
        open(os.path.join(LOG, "summary_src.txt"), "a").write(line + "\n")
elif SET == "rec":
    pristine = open(TST).read()
    for mid, what, old, new in REC_MUTANTS:
        if ONLY and mid not in ONLY:
            continue
        try:
            apply(TST, old, new)
            r = run_tests(mid, ["fix_qam1_seat"])
            r2 = run_tests(mid, ["fix_qam1_seat"], red="limits_strand_seat",
                           extra={"fix_qam1_seat": "qam1_prop"})
            r3 = run_tests(mid, ["fix_qam1_seat"], red="limits_strand_payer",
                           extra={"fix_qam1_seat": "qam1_prop"})
        finally:
            open(TST, "w").write(pristine)
        def ev(red):
            t = open(os.path.join(LOG, f"{mid}.fix_qam1_seat.{red}.log")).read()
            m = re.search(r"Test failed: ([^;]{0,90})", t)
            return m.group(1) if m else "no 'Test failed' text"
        line = (f"{mid} | {what} | normal: {r['fix_qam1_seat']} | under limits_strand_seat: "
                f"{r2['fix_qam1_seat']} [{ev('limits_strand_seat')}] | under limits_strand_payer: "
                f"{r3['fix_qam1_seat']} [{ev('limits_strand_payer')}]")
        print(line, flush=True)
        open(os.path.join(LOG, "summary_rec.txt"), "a").write(line + "\n")
