import subprocess, sys, os
# usage: launch.py <cwd> <log> <target_dir> <args...>   (sets cwd without a shell cd; sources scripts/env.sh)
cwd, log, target = sys.argv[1], sys.argv[2], sys.argv[3]
W = "/private/tmp/claude-501/qah2"
env = dict(os.environ, COAGENT_TOOLS=f"{W}/tools", CARGO_TARGET_DIR=target)
for k in list(env):
    if k.startswith("COAGENT_") and k.endswith(("RED", "RED_ROSTER")) or k == "COAGENT_AUDIT_HOST_RED":
        env.pop(k, None)
cmd = ". scripts/env.sh && exec \"$@\""
with open(log, "w") as f:
    rc = subprocess.call(["bash", "-c", cmd, "x"] + sys.argv[4:], cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT)
with open(log, "a") as f:
    f.write(f"\nexit={rc}\n")
sys.exit(rc)
