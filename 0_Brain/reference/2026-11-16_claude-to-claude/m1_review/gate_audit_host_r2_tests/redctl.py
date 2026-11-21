import subprocess, os, sys
W="/private/tmp/claude-501/qah2"
env=dict(os.environ, COAGENT_TOOLS=f"{W}/tools", CARGO_TARGET_DIR=f"{W}/target-redctl", COAGENT_AUDIT_HOST_RED="own_seat_counts_requests")
for k in ("COAGENT_AUDIT_RED","COAGENT_RED","COAGENT_RED_ROSTER"): env.pop(k,None)
log=open(f"{W}/logs/red_ctl/qa2_triggers_red.log","w")
rc=subprocess.call(["bash","-c",". scripts/env.sh && exec cargo test --locked -p coagent-audit-host --test qa2_triggers -- --nocapture --test-threads=1"],cwd=f"{W}/probe",env=env,stdout=log,stderr=subprocess.STDOUT)
log.write(f"\nexit={rc}\n")
