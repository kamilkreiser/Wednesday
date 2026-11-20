import subprocess, sys, os
# usage: launch.py <cwd> <log> <target_dir> <args...>   (sets cwd without a shell cd)
cwd, log, target = sys.argv[1], sys.argv[2], sys.argv[3]
env = dict(os.environ, COAGENT_TOOLS="/private/tmp/claude-501/qah/tools", CARGO_TARGET_DIR=target)
for k in ("COAGENT_AUDIT_RED","COAGENT_RED","COAGENT_RED_ROSTER","COAGENT_AUDIT_HOST_RED"):
    env.pop(k, None)
with open(log, "w") as f:
    rc = subprocess.call(sys.argv[4:], cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT)
with open(log, "a") as f:
    f.write(f"\nexit={rc}\n")
sys.exit(rc)
