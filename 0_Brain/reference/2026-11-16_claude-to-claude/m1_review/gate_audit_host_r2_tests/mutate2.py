#!/usr/bin/env python3
"""QA-AUDIT-HOST-R2: mutations of the fix round (head 680d333), plus the first check's M7 (adapted
to the head's text) and M9 (unchanged). Each mutation: its OWN worktree (clean head, no probes) and
its OWN target dir; the crate's tests run without the two long ones; survivors may be re-run with
--long. Usage: mutate2.py [--long] ids..."""
import os, subprocess, sys, re, time
W = "/private/tmp/claude-501/qah2"
CLONE = f"{W}/clone"
HEAD = "680d3333c8713fc12f140068b2a3a985d96c4681"
CR = "crates/coagent-audit-host"
H = f"{CR}/src/host.rs"
D = f"{CR}/src/dir.rs"
MUTS = {
 "Mu1": (H, "                self.pending_held = false;\n                if self.save_current().is_ok() {\n                    let _ = self.anchors.remove(PENDING);\n                }\n                Ok(Outcome::Released(Box::new(b)))",
            "                self.pending_held = false;\n                let _ = self.save_current();\n                let _ = self.anchors.remove(PENDING);\n                Ok(Outcome::Released(Box::new(b)))",
        "release removes pending unconditionally (M-2 fix reverted)"),
 "Mu2": (H, "                } else {\n                    m.free_usage()\n                };",
            "                } else {\n                    m.seat_usage(m.status().own_slot)\n                };",
        "OwnSeatAt measured with seat_usage(own slot) again (M-1 fix reverted, source mutant)"),
 "Mu3": (H, "        if r.is_ok() {\n            self.cfg.limits = limits;\n        }",
            "        self.cfg.limits = limits;",
        "set_limits stores cfg.limits on a refused offer (M-3 (a) reverted)"),
 "Mu4a": (H, "                // several writes: whatever landed, the store is read again (pending anchor first)\n                self.pending_held = false;\n",
             "                // several writes: whatever landed, the store is read again (pending anchor first)\n",
        "pending_held clear dropped on the release's error path"),
 "Mu4b": (H, "                Err(AuditError::SealStale) => {\n                    self.pending_held = false;\n",
             "                Err(AuditError::SealStale) => {\n",
        "pending_held clear dropped on the SealStaleTwice error path"),
 "Mu4c": (H, "                        Err(e) => {\n                            self.pending_held = false;\n                            let _ = self.anchors.remove(PENDING);",
             "                        Err(e) => {\n                            let _ = self.anchors.remove(PENDING);",
        "pending_held clear dropped on the stale-retry plan error path"),
 "Mu4d": (H, "                    self.pending_held = false;\n                    if self.save_current().is_ok() {",
             "                    if self.save_current().is_ok() {",
        "(extra, not an error path) pending_held clear dropped at seal step 4"),
 "Mu5": (D, "            let (ef, eb) = exempt_totals(m);\n",
            "            let (ef, eb) = (0usize, 0usize);\n            let _ = exempt_totals(m);\n",
        "load counts the Segment and anchor slots again (m-2 fix reverted)"),
 "M7": (H, "        if !cfg!(coagent_audit_host_red = \"release_no_pending\") {\n            write_anchor(&self.anchors, PENDING, &post)?;\n            self.pending_held = true;\n        }",
           "        if !cfg!(coagent_audit_host_red = \"release_no_pending\") {\n            self.pending_held = true;\n        }",
        "first check's M7 (adapted to the head): the release writes no pending anchor before deleting"),
 "M9": (H, "    fn ensure_anchor(&mut self) -> Result<(), HostError> {\n        if self.anchor_dirty {\n            self.save_current()?;\n        }\n        Ok(())",
           "    fn ensure_anchor(&mut self) -> Result<(), HostError> {\n        if self.anchor_dirty {\n            let _ = self.save_current();\n        }\n        Ok(())",
        "first check's M9 (unchanged text): a failed anchor save never refuses the next change"),
}

def env_for(mid):
    e = dict(os.environ, COAGENT_TOOLS=f"{W}/tools", CARGO_TARGET_DIR=f"{W}/target-mut-{mid}")
    for k in ("COAGENT_AUDIT_RED", "COAGENT_RED", "COAGENT_RED_ROSTER", "COAGENT_AUDIT_HOST_RED"):
        e.pop(k, None)
    return e

def run(mid, cmd, log):
    with open(log, "w") as f:
        return subprocess.call(["bash", "-c", ". scripts/env.sh && exec \"$@\"", "x"] + cmd,
                               cwd=f"{W}/mut-{mid}", env=env_for(mid), stdout=f, stderr=subprocess.STDOUT)

def failing(log):
    return sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", open(log).read(), re.M)))

def main():
    args = sys.argv[1:]
    long = "--long" in args
    ids = [a for a in args if not a.startswith("--")] or list(MUTS)
    os.makedirs(f"{W}/logs/mut", exist_ok=True)
    for mid in ids:
        path, old, new, what = MUTS[mid]
        wt = f"{W}/mut-{mid}"
        if not os.path.exists(wt):
            subprocess.check_call(["git", "-C", CLONE, "worktree", "add", "-q", "--detach", wt, HEAD])
        full = f"{wt}/{path}"
        src = open(full).read()
        if not long:
            if src.count(old) != 1:
                print(f"{mid} NOT APPLIED (pattern count {src.count(old)}): {what}", flush=True)
                continue
            open(full, "w").write(src.replace(old, new))
        t0 = time.time()
        if long:
            log = f"{W}/logs/mut/{mid}.long.log"
            rc = run(mid, ["cargo", "test", "--locked", "-p", "coagent-audit-host", "--lib", "--", "stop_anywhere", "property"], log)
        else:
            log = f"{W}/logs/mut/{mid}.log"
            rc = run(mid, ["cargo", "test", "--locked", "-p", "coagent-audit-host", "--", "--skip", "stop_anywhere", "--skip", "property"], log)
        fl = failing(log)
        txt = open(log).read()
        compiled = "error[E" not in txt and "could not compile" not in txt
        verdict = "KILLED" if fl else ("NO-COMPILE" if not compiled else ("SURVIVED" if rc == 0 else f"rc={rc}"))
        diff = subprocess.run(["git", "-C", wt, "diff", "--stat"], capture_output=True, text=True).stdout.strip().splitlines()
        print(f"{mid} {'LONG ' if long else ''}{verdict} ({time.time()-t0:.0f}s; diff {diff[-1] if diff else 'none'}): {what} :: {', '.join(fl[:8])}", flush=True)

main()
