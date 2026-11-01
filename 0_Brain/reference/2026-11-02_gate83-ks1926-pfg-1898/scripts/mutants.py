#!/usr/bin/env python3
"""Gate 83 mutants. Copies the head's two test files into /private/tmp/gate83_spark/mut/<name>/, mutates the copy,
runs the NEW suite (which reads the sibling subject file) under a 20 s alarm. Nothing in the repo is touched."""
import os, shutil, subprocess, sys
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate83-ks1926-pfg-1898"
H = W + "/wt_head/systemTest/__tests__/"
SUBJ, SUITE = "package_format_gate.test.sh", "package_format_gate_dead_pid.test.sh"
OLD = 'while ps -p "$dead" >/dev/null 2>&1; do'
NEW = 'while kill -0 "$dead" 2>/dev/null; do'

def sub_nth(s, old, new, n):  # replace the n-th (0-based) occurrence
    idx = -1
    for _ in range(n + 1):
        idx = s.index(old, idx + 1)
    return s[:idx] + new + s[idx + len(old):]

subj0 = open(H + SUBJ).read(); suite0 = open(H + SUITE).read()
assert subj0.count(OLD) == 2, subj0.count(OLD)
M = {
 "M1_pickerA_killzero":       (sub_nth(subj0, OLD, NEW, 0), suite0),
 "M2_pickerB_killzero":       (sub_nth(subj0, OLD, NEW, 1), suite0),
 "M3_both_killzero":          (subj0.replace(OLD, NEW), suite0),
 "M4_pickerA_no_increment":   (subj0.replace('dead=$((dead + 1))', 'dead=$dead', 1), suite0),
 "M5_pickerA_inverted":       (sub_nth(subj0, OLD, 'while ! ps -p "$dead" >/dev/null 2>&1; do', 0), suite0),
 "M6_suite_returns_start":    (subj0, suite0.replace('( eval "$line"; echo "$dead" )', 'echo "$2"')),
 "M7_skip_always":            (subj0, suite0.replace('if [[ -z "$LIVE" ]]; then', 'if true; then')),
 "M8_suite_live_never_found": (subj0, suite0.replace('kill -0 "$p" 2>/dev/null && continue', 'continue')),
 "M9_suite_ps_check_dropped": (subj0, suite0.replace('if [[ "$got" =~ ^[0-9]+$ ]] && ! ps -p "$got" >/dev/null 2>&1; then', 'if [[ "$got" =~ ^[0-9]+$ ]]; then')),
}
out = []
for name, (s, t) in M.items():
    assert (s, t) != (subj0, suite0), name + " no-op"
    d = "/private/tmp/gate83_spark/mut/" + name
    os.makedirs(d, exist_ok=True)
    open(d + "/" + SUBJ, "w").write(s); open(d + "/" + SUITE, "w").write(t)
    p = subprocess.run(["perl", "-e", "alarm 20; exec @ARGV", "/bin/bash", d + "/" + SUITE], capture_output=True, text=True)
    open(W + "/logs/mut_%s.log" % name, "w").write(p.stdout + "\n--- stderr ---\n" + p.stderr + "\nRC=%s\n" % p.returncode)
    last = [l for l in p.stdout.splitlines() if l][-1:] or [""]
    verdict = "SURVIVED" if p.returncode == 0 else ("KILLED (alarm/hang)" if p.returncode in (142, -14) else "KILLED")
    out.append("%-28s rc=%-4s %-9s %s" % (name, p.returncode, verdict, last[0]))
print("\n".join(out))
open(W + "/logs/mutants_summary.log", "w").write("\n".join(out) + "\n")
