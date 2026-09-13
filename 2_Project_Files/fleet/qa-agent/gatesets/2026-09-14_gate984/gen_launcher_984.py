#!/usr/bin/env python3
"""gen_launcher_984.py — derive launch_qa_secuura_ks835_984.sh from the #981 STACKED-PR launcher (the tracked template
carrying the STACK-PARENT pin at exit 10 and the blob-judged develop guard at exit 18/19) by ASSERTED substitutions
(every anchor must occur exactly as often as stated, or the generator refuses), TWO asserted block replacements (the
develop-judgement Python — two judged files here, jwt.ts AND oauth.ts, because #982/#983 landing moves both — and the
--check echo block), THREE asserted insertions (the exit-20 head-SHA-in-both guard from the #980 r2 template; the
exit-21 stdin-is-not-a-TTY guard — the 2026-09-13 ledger's guard candidate, first shipped here; the TIER 1 wording),
then a RESIDUAL GUARD: any token of the source gate (its PR number, tickets, head, stack parent, develop pin, blobs,
env-override prefix, its guarded paths, its M-numbers) left anywhere in the output is a refusal — nothing is written
on refusal. Same method as gen_launcher_981.py / gen_launcher_980r2.py.

Usage: gen_launcher_984.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 an output control failed
"""
import os, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks835_984.sh — cross-project QA agent, TIER 1 (an auth door: what an OAuth-minted bearer CARRIES —
# `scopes`, `authMethod` — and what the api-gateway's scope gate does with it; through code AND live on real in-process
# loopback listeners, no stack) gate ROUND 1 on Secuura PR #984 (KS-835) @ d00a2015c: the consent grant now reaches the
# token. jwt.ts: OAuthMintOptions.scopes REQUIRED, OAuthTokenClaims.authMethod?: 'oauth', the access (:205) and refresh
# (:229) mints carry `{ scopes: [...oauth.scopes], authMethod: 'oauth' }` for an OAuth mint and the role default with no
# label for a login mint; oauth.ts: the code grant passes parseScopeString(result.scope || '') (:848), the refresh grant
# re-mints decoded.scopes ?? [] (:954); api-gateway scopes.ts: the attachScopes docblock only (no behaviour change);
# the lane's ks823 test states a grant in its mint helper; two NEW tests (auth 5 cells raw socket + real jwt.ts;
# gateway 6 cells, all controls, on a 127.0.0.1 listener). Six files +398 -25 over the STACK PARENT. Round 1 on this PR.
#
# THE STACKED SHAPE. #984 is the THIRD commit of a stack on origin develop M18 8861e6216: #982 (KS-790, e62eab87a) ->
# #983 (KS-823, f62c975c1) -> #984 (KS-835, d00a2015c). All three PRs have base develop (GitHub, 07:15 AEST 2026-09-14).
# The gate judges #984's OWN delta against its STACK PARENT f62c975c1 (six files) AND the merged shape: develop is an
# ANCESTOR of the head (0 behind / 3 ahead), so the head tree 39ab0226a IS the stack merged onto live develop — the
# full auth (53/707) and gateway (35/349) suites and the ks860 loopback guard run on it. The "merge-base" pin of the
# template is therefore the STACK-PARENT pin here: the GitHub compare f62c975c1...d00a2015c must read merge_base
# f62c975c1, ahead 1, SIX files (exit 10). The merge seat is queued to squash #982 then #983 onto develop before #984;
# when those land, develop's copies of jwt.ts and oauth.ts CHANGE — EXPECTED, not a hit — so the develop guard judges a
# move by CONTENT, on TWO files (GitHub contents API): jwt.ts blob d0d55c11b (M18's = #982's; #982 does not touch it)
# or 62b6db272 (#983 landed) -> green; 26562a224 (#984's own) -> exit 19, the PR has landed and there is nothing to
# gate; any other blob -> exit 18. oauth.ts blob 4b03f555e (M18) / 80e05458e (#982 landed) / de00ffcea (#983 landed) ->
# green; 0bab1b8bd (#984's own) -> exit 19; any other -> exit 18. Any OTHER file of the move under the GUARDED list —
# routes/proxy.ts (the seven scope-gated mounts), gateway middleware/auth.ts (:370 copies the claims), gateway
# middleware/scopes.ts (#984's own comment-only file), services/enforcement.ts and middleware/rateLimitEnforce.ts (the
# label's other consumers), services/auth/src/routes/auth.ts (POST /api/auth/refresh — the brief's H-launder),
# services/auth/src/services/oauth.ts and types/index.ts, packages/shared/src/security/scopes.ts (the role defaults),
# the ks860 loopback guard file — -> exit 18; the auth/gateway __tests__ moved by #982/#983 landing are NOT guarded;
# otherwise the launcher proceeds and prints the move, which the gate re-states (brief TARGET: develop's own count + 22
# auth / + 6 gateway, 0 failed). If #982/#983 merge before the gate finishes, the PR's GitHub delta shrinks; the verdict
# is on head d00a2015c regardless, and the brief says so.
#
# origin develop at pin time: 8861e6216 (M18, #980's squash, 12:00:26Z 2026-09-13; read 07:09:19 and 07:15:57 AEST
# 2026-09-14) — unmoved since the builder's cut.
#
# Adapted from launch_qa_secuura_ks828_900_981.sh by gen_launcher_984.py (asserted substitutions, TWO asserted block
# replacements — the two-file blob-judged develop guard and the --check block — three asserted insertions: the exit-20
# head-SHA-in-both guard (from the #980 round-2 template), the exit-21 stdin-is-not-a-TTY guard (the 2026-09-13 ledger:
# a QA launcher run inside a Bash tool execs claude HEADLESS, parented to the caller's shell; --check stays headless-
# safe), the TIER 1 wording; residual guard): the same guards and exit codes plus 20 and 21, re-pointed at #984.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks835_984.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
"""

# 1. Replace the header (everything before `set -u`) wholesale.
marker = "set -u\n"
assert s.count(marker) == 1, "header marker"
s = NEW_HEADER + s[s.index(marker):]

# 2. Asserted substitutions: (old, new, expected count in the post-header text).
subs = [
    ("QA981_BRIEF", "QA984_BRIEF", 2),
    ("QA981_PROMPT", "QA984_PROMPT", 2),
    ("QA981_HEAD", "QA984_HEAD", 2),
    ("2026-09-13_secuura-981-ks828-900-tier2", "2026-09-14_secuura-984-ks835-tier1", 3),
    ("refs/heads/feature/ks-828-ks-900-leg-f-guarded-wrappers-and-default-only-factory",
     "refs/heads/feature/ks-835-security-oauth-consent-is-decorative-the-granted-scope-never", 1),
    ("04807ea0eb5e551ab22245d38c499af32724c8fd", "d00a2015c89a4720eaeab64482bbd9b89d878024", 1),
    ("STACK_PARENT='8da20edbd595f97cd3c62baaa4ff7b56ea9eef99'", "STACK_PARENT='f62c975c11ec97cdef04500fd98a43618e702763'", 1),
    ("DEVELOP_SHA='e91eb5bdaf68461e43a6055ed39137bd60a36749'", "DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'", 1),
    ("JUDGED_FILE='Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts'\n"
     "BLOB_PRE975='6beacc935fe84d618a6c51854934a8fbe6306773'\n"
     "BLOB_975='ad0afd7cbb9bfd1b0e44db3913863b5bb95f2d9a'\n"
     "BLOB_HEAD='9bcdb42593925603bdbc617cd13b0f91c863bc9c'\n",
     "JWT_FILE='Blockchain/Dev/services/auth/src/services/jwt.ts'\n"
     "OAUTH_FILE='Blockchain/Dev/services/auth/src/routes/oauth.ts'\n"
     "JWT_BLOBS_OK='d0d55c11beab2bfd8f8140e12de4016cac742134 62b6db272c911557d764ee2f0e77f1df26923426'   # M18 (= #982's) · #983 landed\n"
     "JWT_BLOB_HEAD='26562a22470af688ae733000792a2b0321650145'                                             # #984's own -> landed\n"
     "OAUTH_BLOBS_OK='4b03f555e25bf1221081fdd38f530b983cc763e0 80e05458e9759fbc6c7f33bc8cd90060d30e6149 de00ffceaccd8155349e8de10aaeab3a94c33529'   # M18 · #982 · #983\n"
     "OAUTH_BLOB_HEAD='0bab1b8bdd7c9cb2b085bf94d5487a308eb51dd0'                                           # #984's own -> landed\n", 1),
    ("# The STACK-PARENT pin: the judged delta is STACK_PARENT...HEAD and must be exactly ONE commit on ONE file.",
     "# The STACK-PARENT pin: the judged delta is STACK_PARENT...HEAD and must be exactly ONE commit on SIX files.", 1),
    ('[ "$STACK_READ" = "$STACK_PARENT ahead=1 files=1" ] \\\n'
     '  || { echo "REFUSING: the judged delta is not ONE commit on ONE file over the stack parent: compare reads \'$STACK_READ\', brief pins \'$STACK_PARENT ahead=1 files=1\'" >&2; exit 10; }',
     '[ "$STACK_READ" = "$STACK_PARENT ahead=1 files=6" ] \\\n'
     '  || { echo "REFUSING: the judged delta is not ONE commit on SIX files over the stack parent: compare reads \'$STACK_READ\', brief pins \'$STACK_PARENT ahead=1 files=6\'" >&2; exit 10; }', 1),
    ("# The develop pin, judged by CONTENT (see the header). The one file is judged by its blob SHA on develop;\n# GUARDED = the OTHER files whose movement changes this brief's expectations.",
     "# The develop pin, judged by CONTENT (see the header). jwt.ts and oauth.ts are judged by their blob SHAs on develop\n# (#982/#983 landing moves them — expected); GUARDED = the OTHER files whose movement changes this brief's expectations.", 1),
    ('  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" JUDGED_FILE="$JUDGED_FILE" \\\n  BLOB_PRE975="$BLOB_PRE975" BLOB_975="$BLOB_975" BLOB_HEAD="$BLOB_HEAD" python3 - <<\'PYJ\'',
     '  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" JWT_FILE="$JWT_FILE" OAUTH_FILE="$OAUTH_FILE" \\\n  JWT_BLOBS_OK="$JWT_BLOBS_OK" JWT_BLOB_HEAD="$JWT_BLOB_HEAD" OAUTH_BLOBS_OK="$OAUTH_BLOBS_OK" OAUTH_BLOB_HEAD="$OAUTH_BLOB_HEAD" python3 - <<\'PYJ\'', 1),
    ("  LANDED981*) echo \"REFUSING: ${DEV_JUDGEMENT#LANDED981 } (develop $CUR_DEV)\" >&2; exit 19 ;;",
     "  LANDED984*) echo \"REFUSING: ${DEV_JUDGEMENT#LANDED984 } (develop $CUR_DEV)\" >&2; exit 19 ;;", 1),
    ("re-pin deliberately (launcher DEVELOP_SHA/BLOB_* + brief TARGET + prompt)", "re-pin deliberately (launcher DEVELOP_SHA/*_BLOBS_OK + brief TARGET + prompt)", 1),
    ("grep -q 'TIER 2' \"$BRIEF\" && grep -q 'TIER 2' \"$PROMPT_FILE\"", "grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", 1),
    ("grep -q 'ROUND 1' \"$BRIEF\" && grep -q 'ROUND 1' \"$PROMPT_FILE\"", "grep -q 'ROUND 1' \"$BRIEF\" && grep -q 'ROUND 1' \"$PROMPT_FILE\"", 1),  # identical: asserted present once
    ('echo "  brief and prompt agree on TIER 2 and ROUND 1"', 'echo "  brief and prompt agree on TIER 1 and ROUND 1"', 1),
    ('echo "  stack parent still $STACK_PARENT and the judged delta is ONE commit on ONE file (GitHub compare API)"',
     'echo "  stack parent still $STACK_PARENT and the judged delta is ONE commit on SIX files (GitHub compare API)"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:90]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# 3. Asserted BLOCK replacement 1 — the judgement Python body between `f = os.environ["JUDGED_FILE"]` and the final print.
OLD_BLOCK_START = 'f = os.environ["JUDGED_FILE"]; cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]\n'
OLD_BLOCK_END = 'LEG C-F read the services corpus, so the gate re-runs the full package on the merged tree (brief item 7)" % (pinned, cur, c["ahead_by"], len(files), added, modified, removed)); sys.exit(0)\n'
assert s.count(OLD_BLOCK_START) == 1, "judgement block start"
assert s.count(OLD_BLOCK_END) == 1, "judgement block end"
i0 = s.index(OLD_BLOCK_START); i1 = s.index(OLD_BLOCK_END) + len(OLD_BLOCK_END)
NEW_BLOCK = '''jwt_f = os.environ["JWT_FILE"]; oauth_f = os.environ["OAUTH_FILE"]; cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
jwt_ok = os.environ["JWT_BLOBS_OK"].split(); oauth_ok = os.environ["OAUTH_BLOBS_OK"].split()
try:
    jwt_blob = get("/contents/" + jwt_f + "?ref=" + cur)["sha"]
    oauth_blob = get("/contents/" + oauth_f + "?ref=" + cur)["sha"]
except Exception as e:
    print("UNJUDGEABLE develop blob unreadable: " + type(e).__name__); sys.exit(0)
def name(blob, ok, head, labels):
    if blob == head: return "LANDED"
    if blob in ok: return labels[ok.index(blob)]
    return "OTHER"
jn = name(jwt_blob, jwt_ok, os.environ["JWT_BLOB_HEAD"], ["M18 (= #982's; #982 does not touch it)", "#983 landed"])
on = name(oauth_blob, oauth_ok, os.environ["OAUTH_BLOB_HEAD"], ["M18", "#982 landed", "#983 landed"])
if jn == "LANDED" or on == "LANDED":
    print("LANDED984 develop's jwt.ts blob " + jwt_blob[:9] + " / oauth.ts blob " + oauth_blob[:9] + " = #984's own — the PR has landed; nothing to gate"); sys.exit(0)
if jn == "OTHER" or on == "OTHER":
    print("GUARDED develop's jwt.ts blob " + jwt_blob[:9] + " (" + jn + ") / oauth.ts blob " + oauth_blob[:9] + " (" + on + ") — a version nobody pinned (neither M18's, #982's, #983's nor #984's)"); sys.exit(0)
state = "develop's jwt.ts blob " + jwt_blob[:9] + " = " + jn + "; oauth.ts blob " + oauth_blob[:9] + " = " + on + " (the head tree is unchanged by a stack landing; the verdict stays on the head)"
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (M18; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = ["Blockchain/Dev/services/api-gateway/src/routes/proxy.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/auth.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts",
           "Blockchain/Dev/services/api-gateway/src/services/enforcement.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts",
           "Blockchain/Dev/services/auth/src/routes/auth.ts",
           "Blockchain/Dev/services/auth/src/services/oauth.ts",
           "Blockchain/Dev/services/auth/src/types/index.ts",
           "Blockchain/Dev/packages/shared/src/security/scopes.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts"]
hits = sorted({x["filename"] for x in files if x["filename"] not in (jwt_f, oauth_f) for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
auth_tests = sum(1 for x in files if x["filename"].startswith("Blockchain/Dev/services/auth/src/__tests__/"))
gw_tests = sum(1 for x in files if x["filename"].startswith("Blockchain/Dev/services/api-gateway/src/__tests__/"))
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d (auth __tests__ %d, gateway __tests__ %d) — disjoint from the two judged files (by blob) and the ten GUARDED paths; the gate re-reads develop at start and end and re-derives the full-suite counts on the merged tree (brief TARGET: develop's own + 22 auth / + 6 gateway, 0 failed)" % (pinned, cur, c["ahead_by"], len(files), auth_tests, gw_tests)); sys.exit(0)
'''
s = s[:i0] + NEW_BLOCK + s[i1:]

# 4. Asserted insertion 1 — the exit-20 head-SHA-in-both guard (from the #980 r2 template), after the exit-9 line.
ANCHOR_9 = 'grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }\n'
assert s.count(ANCHOR_9) == 1, "exit-9 anchor"
GUARD_20 = ('grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \\\n'
            '  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }\n')
s = s.replace(ANCHOR_9, ANCHOR_9 + GUARD_20)

# 5. Asserted block replacement 2 — the --check echo block gains the head-SHA line (order: after "names the brief").
OLD_ECHO = ('  echo "  prompt opens with the thinking directive and names the brief"\n'
            '  echo "  prompt tells the agent to MAIL its verdict"\n')
assert s.count(OLD_ECHO) == 1, "check echo block"
s = s.replace(OLD_ECHO, ('  echo "  prompt opens with the thinking directive and names the brief"\n'
                         '  echo "  brief and prompt both name the head SHA $HEAD_SHA"\n'
                         '  echo "  prompt tells the agent to MAIL its verdict"\n'))

# 6. Asserted insertion 2 — the exit-21 TTY guard on the LAUNCH path, BEFORE the override guard (so a headless run with
#    overrides set proves 21, and a pty run with overrides set proves 16 through it).
OLD_LAUNCH = '[ -z "${QA984_BRIEF:-}${QA984_PROMPT:-}${QA984_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }\n'
assert s.count(OLD_LAUNCH) == 1, "override guard anchor"
TTY_GUARD = ('# The launch path execs an INTERACTIVE agent: it needs a pane. A launcher run inside a Bash tool inherits no TTY,\n'
             '# execs claude headless, parented to the caller\'s shell, invisible to Kam, and dies at that seat\'s rotation\n'
             '# (2026-09-13 ledger, the #962 gate). --check above is the headless-safe path; the launch refuses without a TTY.\n'
             '[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent and must run in a pane (cockpit.sh add / a terminal); use --check for a headless guard run" >&2; exit 21; }\n')
s = s.replace(OLD_LAUNCH, TTY_GUARD + OLD_LAUNCH)

# 7. Residual guard — nothing of the source gate may survive (outside the exact header sentence naming the template).
RESIDUAL = ["#981", "KS-828", "KS-900", "981.sh", "04807ea0e", "8da20edbd", "e91eb5bda", "0f69129b3", "QA981", "ks781", "6beacc935", "ad0afd7cb",
            "9bcdb4259", "BLOB_PRE975", "BLOB_975", "$BLOB_HEAD", 'os.environ["BLOB_HEAD"]', "JUDGED_FILE", "LEG F", "LEG C-F", "admin.ts",
            "api-gateway/src/index.ts", "794/794", "KS-1126", "#975", "M10", "corpus", "TIER 2", "ONE file", "LANDED981", "s206", "s209",
            'packages/shared/",']
PERMITTED = ["Adapted from launch_qa_secuura_ks828_900_981.sh"]
body = s
for p in PERMITTED:
    assert body.count(p) == 1, f"permitted phrase count: {p!r}"
    body = body.replace(p, "")
for i, line in enumerate(body.splitlines(), 1):
    for t in RESIDUAL:
        if t in line:
            print(f"REFUSING: residual token {t!r} at line {i}: {line.strip()[:120]}", file=sys.stderr)
            sys.exit(2)

# 8. Output controls — every load-bearing token present the stated number of times.
CONTROLS = [
    ("d00a2015c89a4720eaeab64482bbd9b89d878024", 1), ("f62c975c11ec97cdef04500fd98a43618e702763", 1), ("8861e62161466c40f08d2b10a30edeb203123993", 1),
    ("d0d55c11beab2bfd8f8140e12de4016cac742134", 1), ("62b6db272c911557d764ee2f0e77f1df26923426", 1), ("26562a22470af688ae733000792a2b0321650145", 1),
    ("4b03f555e25bf1221081fdd38f530b983cc763e0", 1), ("80e05458e9759fbc6c7f33bc8cd90060d30e6149", 1), ("de00ffceaccd8155349e8de10aaeab3a94c33529", 1), ("0bab1b8bdd7c9cb2b085bf94d5487a308eb51dd0", 1),
    ("QA984_BRIEF", 2), ("QA984_PROMPT", 2), ("QA984_HEAD", 2),
    ("2026-09-14_secuura-984-ks835-tier1.md", 2), ("2026-09-14_secuura-984-ks835-tier1.prompt.txt", 1),
    ("refs/heads/feature/ks-835-security-oauth-consent-is-decorative-the-granted-scope-never", 1),
    ("exit 21", 1), ("exit 20", 1), ("exit 19", 3), ("exit 18", 5), ("exit 10", 2), ("exit 6", 1), ("exit 13", 1), ("exit 16", 2), ("exit 7", 1), ("exit 15", 1), ("exit 9", 1), ("exit 8", 1), ("exit 12", 1), ("exit 11", 1), ("exit 14", 1), ("exit 17", 1),
    ("'TIER 1'", 2), ("'ROUND 1'", 2), ("ahead=1 files=6", 2), ("LANDED984", 3), ("[ -t 0 ]", 1),
    ("JWT_FILE", 4), ("OAUTH_FILE", 4), ("JWT_BLOBS_OK", 4), ("OAUTH_BLOBS_OK", 4), ("JWT_BLOB_HEAD", 4), ("OAUTH_BLOB_HEAD", 4),
    ("Blockchain/Dev/services/api-gateway/src/routes/proxy.ts", 1), ("ks860-test-listeners-bind-loopback.test.ts", 1), ("Blockchain/Dev/services/auth/src/routes/auth.ts", 1),
    ("GUARDED", 7), ("MAIL YOUR VERDICT", 1), ("no memory maintenance", 1), ("NEVER print a credential value", 1), ("ultrathink", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1), ('cd "$QA_DIR"', 1),
    ("brief and prompt both name the head SHA", 1), ("brief and prompt agree on TIER 1 and ROUND 1", 1), ("ONE commit on SIX files", 3),
    ("M18", 10), ("39ab0226a", 1), ("53/707", 1), ("35/349", 1), ("KS-835", 2), ("KS-823", 1), ("KS-790", 1), ("H-launder", 1),
    ('g.endswith("/") and x["filename"].startswith(g)', 1), ("+ 22 auth", 1), ("stdin is not a TTY", 1),
]
bad = [(tok, s.count(tok), n) for tok, n in CONTROLS if s.count(tok) != n]
if bad:
    for tok, c, n in bad:
        print(f"REFUSING: output control {tok!r} occurs {c} times, expected {n}", file=sys.stderr)
    sys.exit(3)
# no raw control byte
b = s.encode("utf-8")
assert not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], "raw control byte in output"

open(out_path, "w", encoding="utf-8").write(s)
os.chmod(out_path, 0o755)
print(f"written {out_path} ({len(b)} bytes); {len(subs)} substitutions asserted; 2 block replacements; 3 insertions; residual guard clean ({len(RESIDUAL)} tokens); {len(CONTROLS)} output controls")
