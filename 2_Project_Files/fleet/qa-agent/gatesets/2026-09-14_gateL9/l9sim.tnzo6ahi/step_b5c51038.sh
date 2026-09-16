set -u
FIXTURES="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL9/l9sim.tnzo6ahi/fixtures"
TMP="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL9/l9sim.tnzo6ahi"
if ! probe="$(cd "$FIXTURES" && env -u SECUURA_STACK_SLOT -u STACK_SLOT -u SECUURA_ARTIFACT_SUFFIX npx tsx "$TMP/drive.ts" '2026-01-01T00:00:00.000Z' "$TMP/does-not-exist.json" 2>"$TMP/probe.err")"; then
  printf '  FAIL harness: the tsx driver did not run\n'
  printf '     stdout: %s\n' "$(printf '%s' "$probe" | head -3)"
  printf '     stderr: %s\n' "$(head -3 "$TMP/probe.err" 2>/dev/null)"
  exit 1
fi
echo GUARD-PASSED
