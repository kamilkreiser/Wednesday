"""Start the red script exactly as `bash scripts/red-controls-scanner.sh` with cwd = the pristine clone's root."""
import os, subprocess, sys
W = "/private/tmp/claude-501/qsn"
env = dict(os.environ)
for k in ["COAGENT_RED", "COAGENT_RED_ROSTER", "COAGENT_AUDIT_RED", "COAGENT_AUDIT_HOST_RED", "COAGENT_SCANNER_RED", "COAGENT_SCANNER_SRC_DIR", "CARGO_TARGET_DIR"]:
    env.pop(k, None)
env.update(COAGENT_TOOLS=W + "/tools", RUSTUP_TOOLCHAIN="1.100.0", COAGENT_SCANNER_RED_TARGET=W + "/target_red",
           COAGENT_SCANNER_RED_LOGS=W + "/logs/red", COAGENT_SCANNER_RED_SCRATCH=W + "/scratch_red")
with open(W + "/logs/red_controls.log", "w") as out:
    rc = subprocess.call(["bash", "scripts/red-controls-scanner.sh"], cwd=W + "/clone_red", env=env, stdout=out, stderr=subprocess.STDOUT)
with open(W + "/logs/red_controls.log", "a") as out:
    out.write("exit %d\n" % rc)
sys.exit(rc)
