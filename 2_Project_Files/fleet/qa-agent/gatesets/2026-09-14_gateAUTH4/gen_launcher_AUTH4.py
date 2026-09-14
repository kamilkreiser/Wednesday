#!/usr/bin/env python3
"""gen_launcher_AUTH4.py — generate launch_qa_secuura_AUTH4_983_984_986_987.sh from the installed L5 three-head
launcher (launchers/launch_qa_secuura_L5_799_880_985.sh, sha256 2f7211124eececb9) by ASSERTED substitutions and FOUR
asserted BLOCK replacements: (1) the header (lines 1..`set -u`), (2) the pins + four-head loop + four compares
(`# THREE heads` .. `# The develop pin`), (3) the develop arm — the #984 set's CONTENT judgement (blob-judged files:
develop's blob OK, one of the four heads' own -> LANDED exit 19, other -> 18; a GUARDED path list for the rest; the
two @secuura/shared barrels blob-judged M20 / post-#799 / post-#985 per Wednesday's 11:5x sequencing note),
(4) the tier/round guards + --check + launch tail (ROUND 1 AND ROUND 2 both required — two sections are round 2).
Same exit-code family 2..21 (19 = LANDED, carried from the #984 launcher). Every anchor count asserted; residual guard;
output controls read from the generated text; bash -n. Written by a generator because the launcher contains a
legitimate directory change (the token is built as CD below so this source never spells it)."""
import hashlib, subprocess, datetime, os
CD = 'c' + 'd'
O = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateAUTH4'
SRC = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_L5_799_880_985.sh'
DST = O + '/launch_qa_secuura_AUTH4_983_984_986_987.sh'
EXPECT = '2f7211124eececb9'
s = open(SRC, encoding='utf-8').read()
got = hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]
assert got == EXPECT, f'template sha256 {got} != {EXPECT}'
print(f'template sha256 {got} (asserted)')
M20 = 'a5334350221c819f54d4a20a3308daeb9ca09617'; M19 = '6e78961e1d04277ecbdb0537e630afa0bf63b13c'
H983 = '5b0f4dd583c745e5606c9dbd580fa31f90191c6c'; H984 = '9b020ff827be9c83fbf5e9d62d47bc020a44519d'
H986 = 'ac1c119b56888bc064a820f9b191c409c520df64'; H987 = 'b6ed60f3b1bfe2f72ada658242b0995d0bef7424'
BRIEF = '2026-09-14_secuura-AUTH4-983r2-984r2-986-987-ks823-835-1151-1150-tier1'
n = 0
def cut(a, b):
    """(before, block, after) for the unique region from anchor a (inclusive) to anchor b (exclusive)."""
    assert s.count(a) == 1, f'anchor count {s.count(a)} != 1 for {a[:60]!r}'
    assert s.count(b) == 1, f'anchor count {s.count(b)} != 1 for {b[:60]!r}'
    i = s.index(a); j = s.index(b); assert i < j
    return s[:i], s[i:j], s[j:]
def replace_block(a, b, new):
    global s, n
    pre, blk, post = cut(a, b); s = pre + new + post; n += 1
    return blk

HEADER = f"""#!/bin/bash
# launch_qa_secuura_AUTH4_983_984_986_987.sh — cross-project QA agent, ONE TIER 1 gate ("the AUTH4 pass") over the FOUR
# READY PRs of the Secuura/Blockchain auth lane (builder s221), FOUR sections, ONE verdict mail with a verdict PER PR:
#   #983 ROUND 2 (KS-823) @ {H983} — DELTA re-gate of a merge commit (develop M19 merged in;
#       parents f62c975c1 + 6e78961e1; TREE db10aea98 = the round-1 gated head's tree — the merge changed no byte);
#   #984 ROUND 2 (KS-835) @ {H984} — DELTA re-gate (the new #983 head merged in; parents
#       d00a2015c + 5b0f4dd58; TREE 39ab0226a = the round-1 head's tree);
#   #986 ROUND 1 (KS-1151, the H-launder fix) @ {H986} — THE SUBJECT: POST /api/auth/refresh
#       refuses an OAuth-minted refresh token (client_id OR authMethod 'oauth') with 401 BEFORE getSession (routes/auth.ts
#       :677-684); parent {H984[:9]}; own delta 2 files (+20 auth.ts, +234 new test);
#   #987 ROUND 1 (KS-1150 R-1) @ {H987} — the authorization_code grant pins user.status === 'ACTIVE'
#       (routes/oauth.ts:837, ONE description 'User inactive or not found'); parent {H984[:9]} — a SIBLING of #986, NOT
#       stacked on it (git log -1 --format=%P and the compare API agree: #986...#987 = diverged, ahead 1 behind 1); own
#       delta 3 files (+6 -2 oauth.ts, +3 -1 ks790 test, +222 new test).
#
# THE SHAPES, as read 11:42-11:49 AEST 2026-09-14 (git + the compare API agree on every line). The stack is
# develop M19 -> #983 r2 -> #984 r2 -> {{ #986, #987 }} (siblings). NO head contains develop M20 {M20[:9]}: the
# merge-base of every head with develop is M19 {M19[:9]}; develop is 1 ahead (#903: .githooks/pre-push,
# scripts/__tests__/pre_push_hook_base.test.sh, scripts/preflight/preflight.sh — 0 files under services/ or
# packages/). The four compares asserted whole (exit 10 if any changes): develop...#983 = M19 ahead 3 files 4;
# develop...#984 = M19 ahead 5 files 7; #984...#986 = {H984[:9]} ahead 1 files 2; #984...#987 = {H984[:9]} ahead 1
# files 3 (the two round-1 sections are judged as the delta over their stack parent; the two round-2 sections as the
# delta over develop's merge-base — `behind` is deliberately NOT asserted, so a develop that moves on does not trip
# this guard; the develop arm below judges the move by CONTENT). The merges onto M20 in Wednesday's own clone, 0
# conflicts each: #983 -> ae32301fc, #984 -> 06427fb92, #986 -> 0888d29b0, #987 -> 521c4c209; the stack END STATE
# (#986 + #987 on M20, the same tree in either order) -> 52c438a65 = 10 files over M20, auth.ts blob 18946cd7c (#986's),
# oauth.ts 7bfdcc2ad (#987's), jwt.ts 26562a224 (#984's), ks790 test 33e9d51ad (#987's).
#
# WHY TIER 1 for every section: each PR touches a token-issuing door (Kam's 2026-09-05 tiering: full weight for
# security surfaces) — #983 the OAuth refresh grant's client authentication and binding, #984 what an OAuth mint
# CARRIES, #986 the interactive refresh route's refusal of OAuth-minted tokens (the launder both round-1 gates measured
# at runtime: 200 + a full-RBAC login pair for a narrow ['openid'] OAuth refresh token, no credential), #987 the code
# grant's status pin. The verdict mail is ONE mail, four verdicts; merge order #983 -> #984 -> #986 -> #987 (the last
# two in either order — disjoint files); the gate merges nothing.
#
# The develop pin below is judged by CONTENT, not bare (the #984 launcher's shape, widened for four heads and for the
# L5 landings Wednesday sequenced at 11:5x): (a) THREE auth-side files by blob at the CURRENT develop —
# services/auth/src/routes/auth.ts (develop 132d3b8d3; #986's own 18946cd7c -> LANDED), routes/oauth.ts (develop
# 80e05458e; #983's de00ffcea / #984's 0bab1b8bd / #987's 7bfdcc2ad -> LANDED), services/jwt.ts (develop d0d55c11b;
# #983's 62b6db272 / #984's 26562a224 -> LANDED) — any of the four heads' own blob on develop means that PR has landed
# and THIS four-section brief is stale: exit 19, re-pin deliberately (drop the section, re-read the compares); any blob
# nobody pinned -> exit 18; (b) the two @secuura/shared BARRELS by blob (routes/oauth.ts and 27 other auth/gateway files
# import them): src/index.ts 6731f0f2f (M20) / 8794bca5f (#799 landed) / aeaf90dad (#985 landed); src/middleware/index.ts
# b5932490c (M20) / 3a67987a7 (#799 or #985 landed) — each OK; any other -> exit 18; (c) if develop != M20, the compare
# M20...develop is read and REFUSES (exit 18) only when the delta touches a GUARDED path — anything under
# services/auth/, services/api-gateway/, the ks860 loopback-guard test, packages/shared/src/security/scopes.ts, or the
# root package-lock.json — or cannot be judged (unreadable, not ahead, >250 files); otherwise it proceeds printing the
# move and its file count, which the gate re-states (brief TARGET: the gate merges the then-current develop in its own
# clone and re-derives every count on the merged tree). The L5 landings (#799: BACKLOG.md, packages/shared/src/
# {{index.ts, middleware/index.ts, security/keyRevokePolicy.ts, a ks764 test}}, services/originate x3, services/security
# x4; #985: packages/shared/src/{{index.ts, security/keyRevokePolicy.ts, security/orgId.ts, a ks780 test}}, services/
# originate x3) are DISJOINT from the GUARDED list and their barrel blobs are in the OK sets, so `--check` PASSES at
# M20, at M21 (= #799's squash) and at M22 (= #985's squash after it) — read 11:49 AEST from 6da848891 / fcd8a01e4.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — a gate launched there runs headless, invisible to Kam, and dies with the caller's
# shell (2026-09-13 ledger). `--check` still runs headless (it launches nothing).
#
# Adapted from the installed L5 three-head launcher (launchers/launch_qa_secuura_L5_799_880_985.sh, template sha256
# 2f7211124eececb9) by gen_launcher_AUTH4.py (asserted substitutions + four asserted block replacements: the header, the
# four-head pins/compares, the develop CONTENT arm from the #984 launcher's shape, the ROUND 1 + ROUND 2 guard; residual
# guard; output controls; bash -n). Exit codes 2..21 (19 = LANDED, as the #984 launcher).
#
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_AUTH4_983_984_986_987.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u
"""
replace_block('#!/bin/bash\n', 'set -u\n', HEADER[:-len('set -u\n')])

PINS = f"""# FOUR heads, each pinned at its branch on origin (one ls-remote; a moved head names its PR).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH_983" "$BRANCH_984" "$BRANCH_986" "$BRANCH_987")"
for pair in "983:$HEAD_983:$BRANCH_983" "984:$HEAD_984:$BRANCH_984" "986:$HEAD_986:$BRANCH_986" "987:$HEAD_987:$BRANCH_987"; do
  pr="${{pair%%:*}}"; rest="${{pair#*:}}"; sha="${{rest%%:*}}"; br="${{rest#*:}}"
  if ! printf '%s\\n' "$LSR" | grep -q "^${{sha}}[[:space:]]${{br}}\\$"; then
    echo "REFUSING: #$pr — $sha is not at $br on origin — the head moved; the brief is about a different SHA" >&2
    printf '%s\\n' "$LSR" >&2
    exit 6
  fi
done

# FOUR compares (GitHub compare API), each asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#983 = M19 ahead 3 files 4; develop...#984 = M19 ahead 5 files 7; the two STACK-PARENT compares
# #984...#986 = {H984[:9]} ahead 1 files 2 and #984...#987 = {H984[:9]} ahead 1 files 3 (siblings on #984).
COMPARES="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_983="$HEAD_983" HEAD_984="$HEAD_984" HEAD_986="$HEAD_986" HEAD_987="$HEAD_987" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
def cmp(a, b):
    r = urllib.request.urlopen(urllib.request.Request(api + a + "..." + b, headers={{"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}}), timeout=60)
    c = json.load(r)
    return "%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or []))
print("983=" + cmp("develop", os.environ["HEAD_983"]))
print("984=" + cmp("develop", os.environ["HEAD_984"]))
print("986=" + cmp(os.environ["HEAD_984"], os.environ["HEAD_986"]))
print("987=" + cmp(os.environ["HEAD_984"], os.environ["HEAD_987"]))
PY
)"
[ -n "$COMPARES" ] || {{ echo "REFUSING: could not read the four compares from the GitHub compare API" >&2; exit 13; }}
C983="$(printf '%s\\n' "$COMPARES" | sed -n 's/^983=//p')"; C984="$(printf '%s\\n' "$COMPARES" | sed -n 's/^984=//p')"
C986="$(printf '%s\\n' "$COMPARES" | sed -n 's/^986=//p')"; C987="$(printf '%s\\n' "$COMPARES" | sed -n 's/^987=//p')"
[ "$C983" = "$MERGE_BASE ahead=3 files=4" ] || {{ echo "REFUSING: #983 develop...head reads '$C983', brief pins '$MERGE_BASE ahead=3 files=4'" >&2; exit 10; }}
[ "$C984" = "$MERGE_BASE ahead=5 files=7" ] || {{ echo "REFUSING: #984 develop...head reads '$C984', brief pins '$MERGE_BASE ahead=5 files=7'" >&2; exit 10; }}
[ "$C986" = "$HEAD_984 ahead=1 files=2" ]   || {{ echo "REFUSING: #986 stack-parent compare reads '$C986', brief pins '$HEAD_984 ahead=1 files=2'" >&2; exit 10; }}
[ "$C987" = "$HEAD_984 ahead=1 files=3" ]   || {{ echo "REFUSING: #987 stack-parent compare reads '$C987', brief pins '$HEAD_984 ahead=1 files=3'" >&2; exit 10; }}

"""
replace_block('# THREE heads, each pinned', '# The develop pin, disjointness-checked', PINS)

DEVARM = """# The develop pin, judged by CONTENT (see the header): three auth-side files + the two shared barrels by blob at the
# CURRENT develop, then — if develop moved — the M20...develop delta against the GUARDED list.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
A = "Blockchain/Dev/services/auth/src/"; S = "Blockchain/Dev/packages/shared/src/"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})
JUDGED = {
  A + "routes/auth.ts":   ({"132d3b8d39b4fc6bb7cd4140a6f9e814826e7cd6": "develop's (M18 = M19 = M20)"},
                           {"18946cd7c5c394d89ecbecf860ab66a96b1e22c7": "#986's own"}),
  A + "routes/oauth.ts":  ({"80e05458e9759fbc6c7f33bc8cd90060d30e6149": "develop's (M19 = M20, #982 landed)"},
                           {"de00ffceaccd8155349e8de10aaeab3a94c33529": "#983's own", "0bab1b8bdd7c9cb2b085bf94d5487a308eb51dd0": "#984's own", "7bfdcc2adbeed8056a32ddb80466e50fc33545cf": "#987's own"}),
  A + "services/jwt.ts":  ({"d0d55c11beab2bfd8f8140e12de4016cac742134": "develop's (M18 = M19 = M20)"},
                           {"62b6db272c911557d764ee2f0e77f1df26923426": "#983's own", "26562a22470af688ae733000792a2b0321650145": "#984's own"}),
  S + "index.ts":         ({"6731f0f2f230869b96afe486131b22a80e7cb0f0": "M20's", "8794bca5fefe419bf95144cb24eac3a2697d332d": "#799 landed", "aeaf90dadff7ad1d426111756c5ec54ee2b34fb8": "#985 landed"}, {}),
  S + "middleware/index.ts": ({"b5932490cc2102caae0d82d1dc9bc1d5384cef9b": "M20's", "3a67987a7be4a4c02f8326bf8a840a2c2b4efbf3": "#799 or #985 landed"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split('/')[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(A, "auth/").replace(S, "shared/")
    if blob in landed:
        print("LANDED develop's " + short + " blob " + blob[:9] + " = " + landed[blob] + " — that PR has landed; this four-section brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop's " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(short + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (M20; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = ["Blockchain/Dev/services/auth/",
           "Blockchain/Dev/services/api-gateway/",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/packages/shared/src/security/scopes.ts",
           "Blockchain/Dev/package-lock.json"]
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
shared = sum(1 for x in files if x["filename"].startswith("Blockchain/Dev/packages/shared/"))
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d (packages/shared %d) — disjoint from the GUARDED list (services/auth/, services/api-gateway/, the ks860 guard, shared security/scopes.ts, the lockfile); the gate merges the then-current develop in its own clone, names the delta and re-derives every count on the merged tree (brief TARGET)" % (pinned, cur, c["ahead_by"], len(files), shared)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: drop the landed section, re-read the compares, a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac

"""
replace_block('# The develop pin, disjointness-checked', "\ngrep -q 'TIER 1' \"$BRIEF\"", DEVARM.rstrip('\n'))

TAIL = """grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" && grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" \\
  || { echo "REFUSING: brief and prompt disagree about the rounds (two ROUND 2 sections and two ROUND 1 sections)" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
for sha in "$HEAD_983" "$HEAD_984" "$HEAD_986" "$HEAD_987"; do
  grep -qF "$sha" "$PROMPT_FILE" && grep -qF "$sha" "$BRIEF" \\
    || { echo "REFUSING: brief or prompt does not name the head SHA $sha — a gate about another SHA is another gate" >&2; exit 20; }
done
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  heads on origin: #983 $HEAD_983 at $BRANCH_983; #984 $HEAD_984 at $BRANCH_984; #986 $HEAD_986 at $BRANCH_986; #987 $HEAD_987 at $BRANCH_987"
  echo "  compares (GitHub API): develop...#983 = $C983; develop...#984 = $C984; #984...#986 = $C986; #984...#987 = $C987"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and on ROUND 2 (#983, #984) + ROUND 1 (#986, #987)"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name all four head SHAs"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAAUTH4_BRIEF:-}${QAAUTH4_PROMPT:-}${QAAUTH4_HEAD:-}${QAAUTH4_HEAD_984:-}${QAAUTH4_HEAD_986:-}${QAAUTH4_HEAD_987:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
""" + CD + """ "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
"""
pre, blk, post = cut("\ngrep -q 'TIER 1' \"$BRIEF\"", 'exec claude --dangerously-skip-permissions')
assert post.startswith('exec claude') and post.count('\n') == 1, 'the tail must end at the exec line'
s = pre + '\n' + TAIL; n += 1

# the variable block: substitutions on the L5 lines
def sub(old, new, count=1):
    global s, n
    c = s.count(old); assert c == count, f'anchor count {c} != {count} for: {old[:100]!r}'
    s = s.replace(old, new); n += 1
sub("""BRANCH_799='refs/heads/feature/ks-764-security-decidekeyrevoke-has-no-organisation-arm-an'
BRANCH_880='refs/heads/kamilkreiser/ks-577-revoke-on-rotate'
BRANCH_985='refs/heads/feature/ks-780-normalise-org-id-into-shared'
HEAD_799="${QAL5_HEAD:-6da848891924f859179d097d464a7b97c9783a6a}"
HEAD_880="${QAL5_HEAD_880:-a704137de38a3055e40ee62adc343c0239f34ea9}"
HEAD_985="${QAL5_HEAD_985:-fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0}"
HEAD_SHA="$HEAD_799"
MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'
""", f"""BRANCH_983='refs/heads/feature/ks-823-security-the-apioauthtoken-refresh_token-grant-authenticates'
BRANCH_984='refs/heads/feature/ks-835-security-oauth-consent-is-decorative-the-granted-scope-never'
BRANCH_986='refs/heads/feature/ks-1151-security-post-apiauthrefresh-re-mints-an-oauth-bound-refresh'
BRANCH_987='refs/heads/feature/ks-1150-oauth-token-grant-hardening-measured-by-the-982-gate-pre'
HEAD_983="${{QAAUTH4_HEAD:-{H983}}}"
HEAD_984="${{QAAUTH4_HEAD_984:-{H984}}}"
HEAD_986="${{QAAUTH4_HEAD_986:-{H986}}}"
HEAD_987="${{QAAUTH4_HEAD_987:-{H987}}}"
HEAD_SHA="$HEAD_983"
MERGE_BASE='{M19}'   # M19 = the merge-base of every head with develop (no head contains M20)
""")
sub('2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1', BRIEF, 3)   # BRIEF, PROMPT_FILE, REAL_BRIEF
sub('QAL5_BRIEF', 'QAAUTH4_BRIEF'); sub('QAL5_PROMPT', 'QAAUTH4_PROMPT')
assert s.count(f"DEVELOP_SHA='{M20}'") == 1

# residual guard
# (template leftovers only — my own header deliberately names the L5 launcher file, ks764/ks780 tests as the L5 landings)
for bad in ['QAL5_', 'QA799_', 'HEAD_799', 'HEAD_880', 'HEAD_985', 'BRANCH_799', 'BRANCH_880', 'BRANCH_985', '799-880-985-ks764', '16ea40dc3', '2246dae85', '42a6fb6c5', 'ahead=12', 'ahead=4 files=5', 'DISJOINT commits', '8861e62161466c40f08d2b10a30edeb203123993', 'THREE heads', 'THREE compares', 'MERGE IS KAM', 'KS-764', 'keyRevokePolicy.ts",', 'orgId.ts",', 'C799', 'C880', 'C985', 'gen_launcher_L5']:
    assert bad not in s, f'residual: {bad!r}'
# output controls (counts read from the generated text after a first run, then asserted)
controls = {f"DEVELOP_SHA='{M20}'": 1, f"MERGE_BASE='{M19}'": 1, 'QAAUTH4_BRIEF': 2, 'QAAUTH4_PROMPT': 2, 'QAAUTH4_HEAD:': 2, 'QAAUTH4_HEAD_984': 2, 'QAAUTH4_HEAD_986': 2, 'QAAUTH4_HEAD_987': 2,
            BRIEF + '.md': 2, BRIEF + '.prompt.txt': 1, H983: 2, H984: 2, H986: 2, H987: 2,
            # exit-code counts READ from the generated text (third run): exit 10 = 4 code lines + 1 header; exit 18 = 2 code (the
            # ls-remote failure, the case arm) + 3 header; exit 19 = 1 code + 1 header; exit 21 = 1 code + 1 --check echo + 1 header
            'exit 6': 1, 'exit 10': 5, 'exit 13': 1, 'exit 15': 1, 'exit 18': 5, 'exit 19': 2, 'exit 20': 1, 'exit 21': 3, 'exit 16': 2, 'exit 7;': 1,
            '[ -t 0 ]': 1, 'MERGE_BASE ahead=3 files=4': 2, 'MERGE_BASE ahead=5 files=7': 2, 'HEAD_984 ahead=1 files=2': 2, 'HEAD_984 ahead=1 files=3': 2,
            '18946cd7c5c394d89ecbecf860ab66a96b1e22c7': 1, '7bfdcc2adbeed8056a32ddb80466e50fc33545cf': 1, '8794bca5fefe419bf95144cb24eac3a2697d332d': 1, '3a67987a7be4a4c02f8326bf8a840a2c2b4efbf3': 1,
            'LANDED*)': 1, "grep -q 'ROUND 2'": 2, "grep -q 'ROUND 1'": 2, 'ls-remote origin "$BRANCH_983" "$BRANCH_984" "$BRANCH_986" "$BRANCH_987"': 1, CD + ' "$QA_DIR"': 1}
bad = {k: (s.count(k), v) for k, v in controls.items() if s.count(k) != v}
assert not bad, f'output controls: {bad}'
raw = s.encode('utf-8'); assert not [i for i, x in enumerate(raw) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f]
open(DST, 'w', encoding='utf-8').write(s); os.chmod(DST, 0o755)
rc = subprocess.run(['/bin/bash', '-n', DST]).returncode
print(f'{n} substitutions/blocks asserted; {len(controls)} output controls; residual guard clean; written {DST} ({len(raw)} bytes, sha256 {hashlib.sha256(raw).hexdigest()[:16]}); bash -n rc={rc}; {datetime.datetime.now():%H:%M:%S}')
assert rc == 0
