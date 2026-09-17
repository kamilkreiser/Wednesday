#!/bin/bash
# build_input_open_pr_arms.sh — red-proof for night/build_input.sh refusing only OPEN attached PRs (2026-09-17 15:4x,
# Kam 15:37 "keep the local agent constantly churning through the backlog"). Until this change ANY attached PR refused
# (merged or not), so KS-864-F1009 (03:52) and KS-928 (15:04, merged #874) each needed a hand-copied builder.
#
# Reads only: Linear GraphQL + GitHub REST GET (the Secuura project's keys, sourced inside the builder or in a python
# child here, never printed) and `git show` on the source checkout (the builder's own read verbs). Writes only under
# $SP. No sandbox (the builder needs the network). Never reads an rc through a pipe. No rm: a previous $SP is MOVED.
#
#   C1 control: GitHub reads #874 as closed + merged
#   C2 control: GitHub reads the open-PR ticket's PR as OPEN (default KS-1187 -> #1019; override OPR_TICKET / OPR_PR)
#   A  NEW builder, KS-928 (merged #874) with its 17k pins        -> rc 0, prints `attached PR #874 (...): merged`,
#                                                                    output JSON byte-identical to night/inputs/code_928.json
#   A' NEW stdout vs the 17k-style SCRATCH COPY of the old builder (line 120 refuse -> print), same pins
#                                                                 -> the ONLY differing lines are PR lines
#   B  NEW builder, the OPEN-PR ticket                            -> rc 2, `REFUSED ... OPEN pull request(s) ['#<n>']`,
#                                                                    prints `attached PR #<n> (...): OPEN`, no output file
#   D1 NEW builder, KS-928, NIGHT_GITHUB_API=http://127.0.0.1:9 (connection refused)
#                                                                 -> rc 2, REFUSED `could not be read ... fail closed`, no file
#   D2 NEW builder, KS-928, a localhost stub answering 200 `{"message":"Not Found"}` (no state)
#                                                                 -> rc 2, REFUSED fail closed, no file
#   D3 NEW builder, KS-928, NIGHT_GITHUB_API=file:///            -> rc 2, REFUSED (seam is http/https only), no file
#   N  OLD builder (.pre-0917-widen), KS-928                      -> rc 2 `attached to pull request(s)` (negative control)
#   L  legacy: KS-839 (no attachment) OLD vs NEW                  -> identical rc, stdout and output bytes
#
# Usage: bash build_input_open_pr_arms.sh [new builder] [old builder]   rc 0 only when every arm holds.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
NEW="${1:-$LM/night/build_input.sh}"
OLD="${2:-$LM/night/build_input.sh.pre-0917-widen}"
ENV_FILE=/Volumes/DevMASTER/\!CODING/Secuura/Blockchain/4_Credentials/.env
BRIEFS="$LM/night/briefs"
SP="${OPR_SCRATCH:-/private/tmp/claude-501/night/widen_0917/opr_arms}"
OPR_TICKET="${OPR_TICKET:-KS-1187}"; OPR_PR="${OPR_PR:-1019}"
[ -d "$SP" ] && mv "$SP" "$SP.prev-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SP"
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }
bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
has(){ /usr/bin/grep -q -E "$2" "$1"; }
for f in "$NEW" "$OLD" "$ENV_FILE" "$LM/night/inputs/code_928.json" "$BRIEFS/KS-928.md"; do [ -f "$f" ] || { echo "FATAL: missing $f"; exit 2; }; done
echo "build_input open-PR arms $(date '+%F %H:%M:%S') · new $NEW ($(shasum -a 256 "$NEW" | cut -c1-12)) · old $OLD ($(shasum -a 256 "$OLD" | cut -c1-12))"
PINS928="product=Blockchain/Dev/services/originate/src/routes/adminConfig.ts ref=services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts line=1893 ctx=65536"
PINS839="product=Blockchain/Dev/services/auth/src/services/oauth.ts ref=services/auth/src/__tests__/ks466-oauth-tenant-guc.test.ts line=353 ctx=65536"

# ---- controls: GitHub PR state, read here independently of the builder
cat > "$SP/controls.py" <<'PYC'
import json, os, sys, urllib.request
for n in sys.argv[1:]:
    r = urllib.request.Request(f"https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/{n}", headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json", "User-Agent": "wednesday-opr-arms"})
    with urllib.request.urlopen(r, timeout=30) as f: j = json.loads(f.read())
    print("PR %s state=%s merged=%s" % (n, j["state"], j["merged"]))
PYC
bash -c 'set -a; source "$1"; set +a; python3 "$2" 874 "$3"' _ "$ENV_FILE" "$SP/controls.py" "$OPR_PR" > "$SP/controls.out" 2>&1
echo "  .. controls: $(tr '\n' '|' < "$SP/controls.out")"
if has "$SP/controls.out" '^PR 874 state=closed merged=True$'; then ok "C1 GitHub reads #874 closed + merged"; else bad "C1" "$(tr '\n' '|' < "$SP/controls.out")"; fi
if has "$SP/controls.out" "^PR $OPR_PR state=open merged=False\$"; then ok "C2 GitHub reads #$OPR_PR ($OPR_TICKET's attached PR) as OPEN"; else bad "C2" "$(tr '\n' '|' < "$SP/controls.out")"; fi

runb(){ # runb <label> <builder> <ticket> <pins> [env assignments...] — sets RC, BO (stdout+stderr), BJ (output path)
  local lbl="$1" d="$SP/$1" b="$2" t="$3" p="$4"; shift 4; mkdir -p "$d"
  BO="$d/build.out"; BJ="$d/input.json"
  # shellcheck disable=SC2086
  env NIGHT_BRIEFS_DIR="$BRIEFS" "$@" bash "$b" "$t" "$BJ" $p > "$BO" 2>&1
  RC=$?
  echo "  .. $lbl rc=$RC :: $(/usr/bin/grep -E '^(attached PR|build_input: REFUSED|wrote )' "$BO" | cut -c1-200 | tr '\n' '|')"
}

echo "--- A: KS-928 (merged #874) now builds"
runb A_new_928 "$NEW" KS-928 "$PINS928"
if [ "$RC" -eq 0 ] && has "$BO" '^attached PR #874 \(Secuura/Distributed_Secuura\): merged$' && cmp -s "$BJ" "$LM/night/inputs/code_928.json"; then
  ok "A  NEW builder KS-928 → rc 0, prints the merged state of #874, output byte-identical to night/inputs/code_928.json ($(shasum -a 256 "$BJ" | cut -c1-12))"
else bad "A" "rc=$RC cmp=$(cmp "$BJ" "$LM/night/inputs/code_928.json" 2>&1 | head -1) $(tail -2 "$BO" | tr '\n' '|')"; fi
# the 17k-style scratch copy: the OLD builder with the refuse at the PR gate turned into a print (as KS-928's input was built)
sed 's/^    refuse(f"attached to pull request(s): {prs}")$/    print(f"attached to pull request(s): {prs}")/' "$OLD" > "$SP/scratch_copy_builder.sh"
diff "$OLD" "$SP/scratch_copy_builder.sh" > "$SP/scratch_copy.diff"
if [ "$(/usr/bin/grep -c '^[<>]' "$SP/scratch_copy.diff")" = 2 ]; then
  runb A2_scratchcopy_928 "$SP/scratch_copy_builder.sh" KS-928 "$PINS928"
  # the `wrote <out path>` line names each arm's own scratch path; normalise it (the output bytes are compared by cmp)
  sed "s#$SP/[^/]*/input.json#<OUT>#" "$SP/A2_scratchcopy_928/build.out" > "$SP/A2_scratchcopy_928/build.norm"
  sed "s#$SP/[^/]*/input.json#<OUT>#" "$SP/A_new_928/build.out" > "$SP/A_new_928/build.norm"
  diff "$SP/A2_scratchcopy_928/build.norm" "$SP/A_new_928/build.norm" > "$SP/A2_stdout.diff"
  NONPR="$(/usr/bin/grep '^[<>]' "$SP/A2_stdout.diff" | /usr/bin/grep -v -E '^[<>] attached (PR #|to pull request)' | /usr/bin/grep -c .)"
  NPR="$(/usr/bin/grep -c -E '^[<>] attached (PR #|to pull request)' "$SP/A2_stdout.diff")"
  if [ "$RC" -eq 0 ] && cmp -s "$SP/A2_scratchcopy_928/input.json" "$SP/A_new_928/input.json" && [ "$NONPR" = 0 ] && [ "$NPR" -ge 2 ]; then
    ok "A' NEW vs the scratch-copy builder on KS-928: output JSON identical; stdout differs ONLY in $NPR PR line(s): $(/usr/bin/grep '^[<>]' "$SP/A2_stdout.diff" | cut -c1-120 | tr '\n' '|')"
  else bad "A'" "rc=$RC nonpr=$NONPR npr=$NPR $(head -8 "$SP/A2_stdout.diff" | tr '\n' '|')"; fi
else bad "A'" "the scratch copy did not differ from OLD in exactly one line: $(tr '\n' '|' < "$SP/scratch_copy.diff")"; fi

echo "--- B: a ticket with an OPEN attached PR still refuses"
runb B_new_open "$NEW" "$OPR_TICKET" ""
if [ "$RC" -eq 2 ] && has "$BO" "^attached PR #$OPR_PR \\(Secuura/Distributed_Secuura\\): OPEN\$" && has "$BO" "^build_input: REFUSED $OPR_TICKET — attached to OPEN pull request\\(s\\) \\[.*'#$OPR_PR'.*\\]" && [ ! -f "$BJ" ]; then
  ok "B  NEW builder $OPR_TICKET (open #$OPR_PR) → rc 2 REFUSED naming OPEN #$OPR_PR, no output written"
else bad "B" "rc=$RC file=$([ -f "$BJ" ] && echo yes || echo no) $(tail -3 "$BO" | tr '\n' '|')"; fi

echo "--- D: the PR state cannot be read -> refuse (fail closed)"
runb D1_new_connrefused "$NEW" KS-928 "$PINS928" NIGHT_GITHUB_API=http://127.0.0.1:9
if [ "$RC" -eq 2 ] && has "$BO" '^build_input: REFUSED KS-928 — attached PR #874 \(Secuura/Distributed_Secuura\): its state could not be read \(URLError: .*fail closed$' && ! has "$BO" '^attached PR #874 .*: merged' && [ ! -f "$BJ" ]; then
  ok "D1 NEW builder, API unreachable (127.0.0.1:9) → rc 2 REFUSED 'could not be read … fail closed', no state printed, no file"
else bad "D1" "rc=$RC $(tail -2 "$BO" | tr '\n' '|')"; fi
# D2: a localhost stub that answers 200 with a body that carries no PR state
cat > "$SP/stub_server.py" <<'PYS'
import http.server, sys
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        b = b'{"message":"Not Found","documentation_url":"stub"}'
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        open(sys.argv[2], "a").write(self.path + " auth=" + ("present" if self.headers.get("Authorization") else "absent") + "\n")
    def log_message(self, *a): pass
s = http.server.HTTPServer(("127.0.0.1", 0), H)
open(sys.argv[1], "w").write(str(s.server_address[1]))
s.handle_request()
PYS
python3 "$SP/stub_server.py" "$SP/stub.port" "$SP/stub.requests" > "$SP/stub_server.out" 2>&1 &
STUB_PID=$!
for _ in 1 2 3 4 5 6 7 8 9 10; do [ -s "$SP/stub.port" ] && break; python3 -c 'import time; time.sleep(0.3)'; done
if [ -s "$SP/stub.port" ]; then
  runb D2_new_nostate "$NEW" KS-928 "$PINS928" NIGHT_GITHUB_API="http://127.0.0.1:$(cat "$SP/stub.port")"
  if [ "$RC" -eq 2 ] && has "$BO" "^build_input: REFUSED KS-928 — attached PR #874 \\(Secuura/Distributed_Secuura\\): its state could not be read \\(KeyError: 'state'\\).*fail closed\$" && [ ! -f "$BJ" ] && has "$SP/stub.requests" '^/repos/Secuura/Distributed_Secuura/pulls/874 auth=present$'; then
    ok "D2 NEW builder, stub answers 200 with no state → rc 2 REFUSED (KeyError 'state'), the stub saw GET /repos/Secuura/Distributed_Secuura/pulls/874, no file"
  else bad "D2" "rc=$RC req=$(tr '\n' '|' < "$SP/stub.requests" 2>/dev/null) $(tail -2 "$BO" | tr '\n' '|')"; fi
else bad "D2" "the stub server did not start: $(tr '\n' '|' < "$SP/stub_server.out")"; fi
kill "$STUB_PID" 2>/dev/null; wait "$STUB_PID" 2>/dev/null
runb D3_new_fileseam "$NEW" KS-928 "$PINS928" NIGHT_GITHUB_API=file:///
if [ "$RC" -eq 2 ] && has "$BO" '^build_input: REFUSED KS-928 — attached to pull request\(s\) .* NIGHT_GITHUB_API is not an http\(s\) URL' && [ ! -f "$BJ" ]; then
  ok "D3 NEW builder, NIGHT_GITHUB_API=file:/// → rc 2 REFUSED (the stub seam is http/https only; a file cannot fake a merged state)"
else bad "D3" "rc=$RC $(tail -2 "$BO" | tr '\n' '|')"; fi

echo "--- N: negative control"
runb N_old_928 "$OLD" KS-928 "$PINS928"
if [ "$RC" -eq 2 ] && has "$BO" "^build_input: REFUSED KS-928 — attached to pull request\\(s\\): \\['https://github.com/Secuura/Distributed_Secuura/pull/874'\\]\$" && [ ! -f "$BJ" ]; then
  ok "N  OLD builder KS-928 → rc 2 REFUSED 'attached to pull request(s)' (the merged PR refused, as before)"
else bad "N" "rc=$RC $(tail -2 "$BO" | tr '\n' '|')"; fi

echo "--- L: a ticket with NO attached PR is untouched"
runb L_old_839 "$OLD" KS-839 "$PINS839"; RC_O=$RC
runb L_new_839 "$NEW" KS-839 "$PINS839"; RC_N=$RC
for x in L_old_839 L_new_839; do sed "s#$SP/[^/]*/input.json#<OUT>#" "$SP/$x/build.out" > "$SP/$x/build.norm"; done
if [ "$RC_O" = "$RC_N" ] && cmp -s "$SP/L_old_839/build.norm" "$SP/L_new_839/build.norm" && { { [ ! -f "$SP/L_old_839/input.json" ] && [ ! -f "$SP/L_new_839/input.json" ]; } || cmp -s "$SP/L_old_839/input.json" "$SP/L_new_839/input.json"; } && ! has "$SP/L_new_839/build.out" '^attached PR'; then
  ok "L  KS-839 (no attachment): OLD and NEW identical — rc $RC_N, stdout identical ($(/usr/bin/grep -c . "$SP/L_new_839/build.out") lines), output $( [ -f "$SP/L_new_839/input.json" ] && echo "identical ($(shasum -a 256 "$SP/L_new_839/input.json" | cut -c1-12))" || echo "absent in both"), no GitHub read"
else bad "L" "rc old=$RC_O new=$RC_N $(diff "$SP/L_old_839/build.norm" "$SP/L_new_839/build.norm" | head -4 | tr '\n' '|')"; fi

echo "build_input open-PR arms: $pass passed, $fail failed ($(date +%H:%M:%S))"
[ "$fail" -eq 0 ]
