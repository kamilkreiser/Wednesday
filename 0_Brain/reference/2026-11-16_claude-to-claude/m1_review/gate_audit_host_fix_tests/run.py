#!/usr/bin/env python3
# QA-AUDIT-HOST-FIX launcher: runs argv in the clone root (cwd set by subprocess, no shell cd),
# with the toolchain env of scripts/env.sh pointed at this work dir's own cargo home and target.
import os, subprocess, sys
W = "/private/tmp/claude-501/qahf"
clone = os.environ.get("QA_CLONE", W + "/repo")
env = dict(os.environ)
env["COAGENT_TOOLS"] = W + "/tools"
env["RUSTUP_HOME"] = W + "/tools/rustup"
env["CARGO_HOME"] = W + "/tools/cargo"
env.setdefault("CARGO_TARGET_DIR", W + "/target/main")
env["PATH"] = W + "/tools/cargo/bin:" + env["PATH"]
for k in ("COAGENT_AUDIT_RED", "COAGENT_RED", "COAGENT_RED_ROSTER"):
    env.pop(k, None)
sys.exit(subprocess.run(sys.argv[1:], cwd=clone, env=env).returncode)
