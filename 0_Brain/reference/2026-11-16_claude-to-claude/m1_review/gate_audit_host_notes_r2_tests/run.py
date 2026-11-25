#!/usr/bin/env python3
# QA-AUDIT-HOST-NOTES-R2 launcher (the first check's run.py, W changed): runs argv in a given tree (QA_CLONE; cwd set by subprocess, no shell cd),
# with the toolchain env of scripts/env.sh pointed at this work dir's own cargo home and an own target.
import os, subprocess, sys
W = "/private/tmp/claude-501/qahn2"
clone = os.environ.get("QA_CLONE", W + "/clean")
env = dict(os.environ)
env["COAGENT_TOOLS"] = W + "/tools"
env["RUSTUP_HOME"] = W + "/tools/rustup"
env["CARGO_HOME"] = W + "/tools/cargo"
if "CARGO_TARGET_DIR" not in env:
    sys.exit("run.py: set CARGO_TARGET_DIR (one per tree)")
env["PATH"] = W + "/tools/cargo/bin:" + env["PATH"]
for k in ("COAGENT_AUDIT_RED", "COAGENT_RED", "COAGENT_RED_ROSTER", "COAGENT_AUDIT_HOST_RED"):
    if k not in os.environ.get("QA_KEEP", "").split(","):
        env.pop(k, None)
sys.exit(subprocess.run(sys.argv[1:], cwd=clone, env=env).returncode)
