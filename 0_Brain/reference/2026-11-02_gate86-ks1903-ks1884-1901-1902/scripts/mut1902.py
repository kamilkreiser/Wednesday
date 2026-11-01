#!/usr/bin/env python3
"""Gate 86 mutants for PR 1902. Mutates COPIES of the subject under /private/tmp/gate86_spark/mut1902/<name>/ and runs the
PR's new suite (and, with --extra, the strengthened suite) against each via MANIFEST_READERS_AGREE_SH. Repo untouched."""
import os, subprocess, sys
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate86-ks1903-ks1884-1901-1902"
H = W + "/wt_1902/systemTest/__tests__/"
SUBJ = open(H + "manifest_readers_agree.test.sh").read()
def rep(old, new, count=-1):
    assert old in SUBJ, old
    return SUBJ.replace(old, new, count)
def nth(old, new, n):
    idx = -1
    for _ in range(n + 1): idx = SUBJ.index(old, idx + 1)
    return SUBJ[:idx] + new + SUBJ[idx + len(old):]
D = '2>"$ERR_DIR/'
M = {
 "A_writer_devnull":      rep('2>"$ERR_DIR/writer"', '2>/dev/null'),
 "B_playwright_devnull":  rep('2>"$ERR_DIR/playwright"', '2>/dev/null'),
 "C_performance_devnull": rep('2>"$ERR_DIR/performance"', '2>/dev/null'),
 "D_schemathesis_devnull":rep('2>"$ERR_DIR/schemathesis"', '2>/dev/null'),
 "E_all_devnull":         rep('2>"$ERR_DIR/writer"', '2>/dev/null').replace('2>"$ERR_DIR/playwright"', '2>/dev/null').replace('2>"$ERR_DIR/performance"', '2>/dev/null').replace('2>"$ERR_DIR/schemathesis"', '2>/dev/null'),
 "F_print_on_pass":       rep('PASS=$((PASS+1)); echo "ok   $label -> $want"', 'PASS=$((PASS+1)); echo "ok   $label -> $want"; echo "     writer stderr: $(head -c 400 "$ERR_DIR/writer" | tr "\\n" " ")"'),
 "G_loop_only_writer":    rep('for _k in writer playwright performance schemathesis; do\n      [[', 'for _k in writer; do\n      [['),
 "H_nonempty_test_inverted": rep('[[ -s "$ERR_DIR/$_k" ]] &&', '[[ ! -s "$ERR_DIR/$_k" ]] &&'),
 "I_stderr_into_stdout":  rep('2>"$ERR_DIR/writer"', '2>&1'),
 "J_shared_file":         rep('2>"$ERR_DIR/playwright"', '2>"$ERR_DIR/writer"'),
 "K_no_trap":             rep("trap 'rm -rf \"$ERR_DIR\"' EXIT\n", ""),
 "L_no_truncation":       rep('head -c 400 "$ERR_DIR/$_k"', 'cat "$ERR_DIR/$_k"'),
 "M_label_dropped":       rep('echo "     $_k stderr: $(', 'echo "     stderr: $('),
}
suites = {"pr_suite": H + "manifest_readers_agree_stderr.test.sh"}
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]): suites["strengthened"] = sys.argv[1]
out = []
for name, s in M.items():
    assert s != SUBJ, name + " no-op"
    d = "/private/tmp/gate86_spark/mut1902/" + name
    os.makedirs(d, exist_ok=True)
    mp = d + "/manifest_readers_agree.test.sh"
    open(mp, "w").write(s)
    row = []
    for sn, sp in suites.items():
        env = dict(os.environ, MANIFEST_READERS_AGREE_SH=mp)
        if sn == "strengthened":   # strengthened suite lives next to support/, copy path is in H via HERE; subject comes from env
            pass
        p = subprocess.run(["perl", "-e", "alarm 120; exec @ARGV", "/bin/bash", sp], capture_output=True, text=True, env=env)
        open(W + "/logs/mut1902_%s_%s.log" % (sn, name), "w").write(p.stdout + "\n--- stderr ---\n" + p.stderr + "\nRC=%s\n" % p.returncode)
        last = [l for l in p.stdout.splitlines() if l.startswith("Results")][-1:] or ["?"]
        row.append("%s: %s rc=%s %s" % (sn, "SURVIVED" if p.returncode == 0 else "KILLED", p.returncode, last[0]))
    out.append("%-26s %s" % (name, " | ".join(row)))
print("\n".join(out))
open(W + "/logs/mut1902_summary%s.log" % ("_strengthened" if len(suites) > 1 else ""), "w").write("\n".join(out) + "\n")
