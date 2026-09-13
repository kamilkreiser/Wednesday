#!/bin/bash
# controls_check.sh — re-grep every §4 positive-control token of the #903 (KS-991) TIER-2 ROUND-2 brief at the PINNED head
# a4f71cde6, the merge commit 48553f272, develop M18 8861e6216, the reviewed head a70f92d7c and the old base 986c592d5 through the
# GitHub contents API (read-only; GH_TOKEN sourced by NAME from the Secuura .env, never printed). Tokens were derived from #903's
# OWN files at these SHAs — never carried from another gate's brief. PRESENT tokens must grep the stated count; ABSENT tokens
# exactly 0; the blobs / sizes / lines / sha256 must match TARGET; the named lines must read as quoted; the test file at head must
# equal develop's with ONE 122-line insertion after :506 and ONE replaced line (the landed-loop); the hook and preflight.sh must be
# byte-identical at head and at the merge commit; the hook at head vs develop must be exactly ONE changed region (-1/+39); the
# six tamper anchors must occur once in the head's hook; the round-1 record must be on disk; the head commit's message must name
# KS-991 only.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD="${QA903R2_HEAD:-a4f71cde660c1442d98317e26d93845340b20098}"
MERGE="${QA903R2_MERGE:-48553f272ac503d5b13be6bb1a9b6ba1c7f56586}"
DEV="${QA903R2_DEVELOP:-8861e62161466c40f08d2b10a30edeb203123993}"
R1HEAD='a70f92d7cf24672a0d7de1c2e05e64c0bc38985c'
OLDBASE='986c592d5d4e09f600af43e88cc2b69bc4ca7395'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
R1_RECORD='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/peter_903_comment_5585854866.md'
W="$(mktemp -d "${TMPDIR:-/tmp}/qa903ctl.XXXXXX")"
TF='Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh'
HK='.githooks/pre-push'
PF='Blockchain/Dev/scripts/preflight/preflight.sh'
AB='Blockchain/Dev/scripts/audit/audit-baseline.json'
RS='Blockchain/Dev/scripts/run-shell-suites.sh'

fetch() { # path ref outfile -> prints blob sha, or ABSENT, or UNREADABLE
  ( set -a; . "$SECUURA_ENV"; set +a
    P="$1" REF="$2" OUT="$3" python3 - <<'PY'
import base64, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/contents/" + os.environ["P"] + "?ref=" + os.environ["REF"]
try:
    o = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except urllib.error.HTTPError as e:
    print("ABSENT" if e.code == 404 else "UNREADABLE HTTP%d" % e.code); sys.exit(0)
except Exception as e:
    print("UNREADABLE " + type(e).__name__); sys.exit(0)
open(os.environ["OUT"], "wb").write(base64.b64decode(o["content"]))
print(o["sha"])
PY
  )
}
FAILS=0
echo "controls_check.sh — head ${HEAD:0:9}, merge ${MERGE:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
for spec in "tf:$TF:$HEAD" "tf_merge:$TF:$MERGE" "tf_dev:$TF:$DEV" "tf_r1:$TF:$R1HEAD" "tf_base:$TF:$OLDBASE" \
            "hk:$HK:$HEAD" "hk_merge:$HK:$MERGE" "hk_dev:$HK:$DEV" "hk_r1:$HK:$R1HEAD" "hk_base:$HK:$OLDBASE" \
            "pf:$PF:$HEAD" "pf_merge:$PF:$MERGE" "pf_dev:$PF:$DEV" \
            "ab:$AB:$HEAD" "ab_dev:$AB:$DEV" "ab_r1:$AB:$R1HEAD" "rs:$RS:$HEAD" "rs_dev:$RS:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; ABSENT) echo "FAIL $n ABSENT at ${ref:0:9}"; FAILS=$((FAILS+1)); continue ;; esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
done
blobis() { [ -f "$W/$1.blob" ] || { echo "FAIL $1 not read"; FAILS=$((FAILS+1)); return; }; [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis tf affdf027b; blobis tf_merge d95af6514; blobis tf_dev d95af6514; blobis tf_r1 650215b8a; blobis tf_base 650215b8a
blobis hk 1b22d4e14; blobis hk_merge 1b22d4e14; blobis hk_dev f0748ed56; blobis hk_r1 31d27018a; blobis hk_base aae2743ac
blobis pf 0727300f7; blobis pf_merge 0727300f7; blobis pf_dev acfb7fa3e
blobis ab 03d1680e3; blobis ab_dev 03d1680e3; blobis ab_r1 33bc6f29a; blobis rs bf766bb54; blobis rs_dev bf766bb54
same() { cmp -s "$W/$1" "$W/$2" && echo "ok   $1 byte-identical to $2" || { echo "FAIL $1 DIFFERS from $2"; FAILS=$((FAILS+1)); }; }
diffs() { cmp -s "$W/$1" "$W/$2" && { echo "FAIL $1 byte-identical to $2 (must differ)"; FAILS=$((FAILS+1)); } || echo "ok   $1 DIFFERS from $2 (as it must)"; }
same hk hk_merge; same pf pf_merge; same tf_merge tf_dev; same ab ab_dev; same rs rs_dev; same tf_r1 tf_base
diffs tf tf_merge; diffs hk hk_dev; diffs pf pf_dev; diffs hk_r1 hk_base; diffs ab_r1 ab
for pair in "tf:6dabbb516e92e5cf" "tf_dev:48ada0c361efcc3c" "tf_r1:1b01dc0c581994a5" "hk:92abd8e9b30e8d19" "hk_dev:cc940299b2aec733" "hk_r1:d397524ddbde5938" "hk_base:57b046fed04ca492" "pf:b8bb4c873c9fb61d" "pf_dev:7f4083d915708a15"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(shasum -a 256 "$W/$f" | cut -c1-16)" = "$want" ] && echo "ok   $f sha256 $want" || { echo "FAIL $f sha256 is not $want"; FAILS=$((FAILS+1)); }
done
for pair in "tf:646" "tf_dev:524" "tf_r1:374" "hk:282" "hk_dev:244" "hk_r1:219" "hk_base:181" "pf:545" "pf_dev:521"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -l < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want lines" || { echo "FAIL $f is not $want lines"; FAILS=$((FAILS+1)); }
done
for pair in "tf:34232" "tf_dev:26945" "tf_r1:18384" "hk:16472" "hk_dev:14027" "hk_r1:13017" "hk_base:10572" "pf:31527" "pf_dev:29971"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -c < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want bytes" || { echo "FAIL $f is not $want bytes"; FAILS=$((FAILS+1)); }
done
lineis() { # file line expected-text
  local got; got="$(sed -n "${2}p" "$W/$1")"
  [ "$got" = "$3" ] && echo "ok   $1:$2 = $3" || { echo "FAIL $1:$2 is: $got"; FAILS=$((FAILS+1)); }
}
# --- the hook at head: the guard block the brief cites
lineis hk 128 "if [ -z \"\$changed\" ] && ! git rev-parse '@{upstream}' >/dev/null 2>&1; then"
lineis hk 133 "    # KS-991 — A STALE LOCAL \`develop\` CAN ONLY INFLATE THE DIFF, SO SKIP IT."
lineis hk 146 "    #   KS-991  a ref BEHIND the remote   -> inflated diff -> INVENTS a change"
lineis hk 160 "    _refs='develop origin/develop refs/remotes/origin/develop'"
lineis hk 161 "    if git rev-parse --verify --quiet develop >/dev/null 2>&1 &&"
lineis hk 162 "       git rev-parse --verify --quiet origin/develop >/dev/null 2>&1 &&"
lineis hk 163 "       [ \"\$(git rev-parse develop)\" != \"\$(git rev-parse origin/develop)\" ] &&"
lineis hk 164 "       git merge-base --is-ancestor develop origin/develop 2>/dev/null; then"
lineis hk 165 "        echo \"[pre-push] KS-991: local 'develop' is BEHIND origin/develop — ignoring the\" >&2"
lineis hk 166 "        echo \"[pre-push]   stale ref for base selection. (git fetch origin develop:develop\" >&2"
lineis hk 167 "        echo \"[pre-push]   to refresh it.) origin/develop is still consulted below.\" >&2"
lineis hk 168 "        _refs='origin/develop refs/remotes/origin/develop'"
lineis hk 170 "    for _ref in \$_refs; do"
lineis hk 192 "    if [ -n \"\$base\" ] && [ \"\$_informative\" -eq 0 ]; then"
lineis hk 193 "        echo \"[pre-push] KS-882: every ref that resolves already CONTAINS this commit,\" >&2"
lineis hk 200 "    if [ -z \"\$base\" ]; then"
lineis hk 201 "        echo \"[pre-push] KS-854: no base to diff against — 'develop' does not resolve,\" >&2"
lineis hk 254 "[ -z \"\$changed\" ] && exit 0"
lineis hk 256 "echo \"[pre-push] Blockchain/Dev changes detected → running preflight gate (bypass: --no-verify)\""
# --- the hook at develop: the single loop line
lineis hk_dev 132 "    for _ref in develop origin/develop refs/remotes/origin/develop; do"
# --- the test file at head: the cited lines
lineis tf 29 "#        HOOK_SH=/path/to/other/pre-push bash …   (to test a different copy)"
lineis tf 56 "HOOK=\"\${HOOK_SH:-\$REPO_ROOT/.githooks/pre-push}\""
lineis tf 63 "WORK=\"\$(mktemp -d \"\${TMPDIR:-/tmp}/ks854.XXXXXX\")\""
lineis tf 64 "trap 'rm -rf \"\$WORK\"' EXIT"
lineis tf 508 "# CASE 10 — KS-991. A STALE local \`develop\` must not INVENT a change."
lineis tf 530 "build_fixture \"\$WORK/c10\" with-develop"
lineis tf 535 "  git branch develop origin/develop"
lineis tf 546 "  git checkout -q -b docs/stale --no-track origin/develop"
lineis tf 555 "  git merge-base --is-ancestor develop origin/develop 2>/dev/null \\"
lineis tf 572 "if printf '%s' \"\$out10\" | grep -q 'KS-991'; then"
lineis tf 573 "  ok \"CASE 10 — a stale local develop is IGNORED for base selection, and the hook says so (KS-991)\""
lineis tf 578 "if printf '%s' \"\$out10\" | grep -q '\\[preflight\\] ran'; then"
lineis tf 582 "  ok \"CASE 10 — a docs-only push on a CURRENT base SKIPS the preflight, despite the stale local develop\""
lineis tf 586 "# CASE 11 — the KS-991 fix must not become \"always skip\". The SAME stale local"
lineis tf 592 "build_fixture \"\$WORK/c11\" with-develop"
lineis tf 605 "  echo change > Blockchain/Dev/file.txt"
lineis tf 622 "if printf '%s' \"\$out11\" | grep -q '\\[preflight\\] ran'; then"
lineis tf 623 "  ok \"CASE 11 — a real Blockchain/Dev change on the branch still RUNS the preflight with a stale local develop (the fix did not become 'always skip')\""
lineis tf 633 "for out_name in out1 out2 out3 out4 out5 out6 out7 out8 out9 out10 out11; do"
lineis tf 641 "[ \"\$landed\" -eq 0 ] && ok \"every case's commit LANDED before its push, so each assertion is on a real change\""
lineis tf 644 "printf '\\n  %d passed, %d failed\\n' \"\$pass\" \"\$fail\""
lineis tf_dev 511 "for out_name in out1 out2 out3 out4 out5 out6 out7 out8 out9; do"
# --- CASE 5 / CASE 6 assertions the tampers hinge on (unchanged lines, also at develop)
lineis tf 326 "if printf '%s' \"\$out5\" | grep -q 'KS-882'; then"
lineis tf 364 "if printf '%s' \"\$out6\" | grep -q '\\[pre-push\\]'; then"
lineis tf_dev 326 "if printf '%s' \"\$out5\" | grep -q 'KS-882'; then"
lineis tf_dev 364 "if printf '%s' \"\$out6\" | grep -q '\\[pre-push\\]'; then"
# --- preflight.sh at head: the env_fail arm
lineis pf 96 "env_fail=0   # KS-991: leg 1 could not RUN (no workspace install) vs a real finding"
lineis pf 118 "    env_fail=1"
lineis pf 531 "    if [ \"\${env_fail:-0}\" -ne 0 ]; then"
lineis pf 532 "        echo \"PREFLIGHT FAILED — but leg 1 could not RUN: this working tree has no\""
chk() { # file token mode(present|absent|N)
  local f="$1" tok="$2" mode="$3" c
  c="$(/usr/bin/grep -c -F -- "$tok" "$W/$f")"
  if [ "$mode" = present ] && [ "$c" -ge 1 ]; then echo "ok   $f  present x$c  $tok"
  elif [ "$mode" = absent ] && [ "$c" -eq 0 ]; then echo "ok   $f  absent      $tok"
  elif [ "$mode" != present ] && [ "$mode" != absent ] && [ "$c" -eq "$mode" ]; then echo "ok   $f  exactly x$c $tok"
  else echo "FAIL $f  $mode expected, count $c: $tok"; FAILS=$((FAILS+1)); fi
}
# --- the test file at head vs develop
chk tf "KS-991" 8; chk tf "CASE 10" 8; chk tf "CASE 11" 6; chk tf "out10" 6; chk tf "out11" 5; chk tf "PRECONDITION-LOST" 33; chk tf "build_fixture \"\$WORK/c" 12
chk tf "  ok \"" 27; chk tf "  bad \"" 28; chk tf "[ \"\$landed\" -eq 0 ] && ok \"" 1
chk tf "merge-base --is-ancestor develop origin/develop" 2; chk tf "docs/stale" 4; chk tf "feature/stale" 4; chk tf "trunk-moved" 2
chk tf "COMMIT-DID-NOT-LAND" 13; chk tf "GIT_CONFIG_GLOBAL=/dev/null" 3; chk tf "\[preflight\] ran" 8; chk tf "[preflight] ran" 1
chk tf_dev "KS-991" absent; chk tf_dev "CASE 10" absent; chk tf_dev "CASE 11" absent; chk tf_dev "out10" absent; chk tf_dev "  ok \"" 22; chk tf_dev "build_fixture \"\$WORK/c" 10
chk tf_r1 "CASE 7" absent; chk tf_r1 "CASE 9" absent; chk tf_r1 "  ok \"" 15
# --- the hook at head vs develop (the tamper anchors)
chk hk "_refs=" 2; chk hk "KS-991" 3; chk hk "merge-base --is-ancestor develop origin/develop" 1
chk hk "[ \"\$(git rev-parse develop)\" != \"\$(git rev-parse origin/develop)\" ] &&" 1
chk hk "[pre-push] KS-991: local 'develop' is BEHIND origin/develop" 1; chk hk "for _ref in \$_refs; do" 1
chk hk "for _ref in develop origin/develop refs/remotes/origin/develop; do" absent
chk hk "KS-882: every ref that resolves already CONTAINS this commit" 1; chk hk "KS-854: no base to diff against" 1; chk hk "check-package-format.sh" 1
chk hk_dev "_refs=" absent; chk hk_dev "KS-991" absent; chk hk_dev "for _ref in develop origin/develop refs/remotes/origin/develop; do" 1; chk hk_dev "check-package-format.sh" 1
chk hk_base "check-package-format.sh" absent; chk hk_base "KS-991" absent; chk hk_r1 "KS-991" 3; chk hk_r1 "check-package-format.sh" absent
# --- preflight.sh
chk pf "env_fail" 3; chk pf "KS-991" 3; chk pf "PREFLIGHT FAILED — but leg 1 could not RUN" 1; chk pf "Do NOT reach for --no-verify" 1; chk pf "PREFLIGHT FAILED — fix the above before pushing." 1
chk pf_dev "env_fail" absent; chk pf_dev "KS-991" absent; chk pf_dev "PREFLIGHT FAILED — fix the above before pushing." 1
# --- the shapes re-derived in Python: the insertion, the hook delta, the six anchors, 0 control bytes
cat > "$W/sim.py" <<'PY'
import re, sys, difflib
W = sys.argv[1]
th = open(f"{W}/tf", encoding="utf-8").read().split('\n'); td = open(f"{W}/tf_dev", encoding="utf-8").read().split('\n')
hh = open(f"{W}/hk", encoding="utf-8").read(); hd = open(f"{W}/hk_dev", encoding="utf-8").read()
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
sm = difflib.SequenceMatcher(None, td, th, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
ck(len(ops) == 2, f"test file develop -> head: {len(ops)} changed regions (expected 2): {[(o[0], o[1]+1, o[2], o[3]+1, o[4]) for o in ops]}")
ck(ops and ops[0][0] == 'insert' and ops[0][1] == 506 and ops[0][4] - ops[0][3] == 122, "region 1 = an INSERT of 122 lines after develop's :506")
ck(len(ops) == 2 and ops[1][0] == 'replace' and (ops[1][2] - ops[1][1], ops[1][4] - ops[1][3]) == (1, 1) and td[ops[1][1]].endswith('out9; do') and th[ops[1][3]].endswith('out9 out10 out11; do'), "region 2 = the landed-loop line, out9 -> out9 out10 out11")
ck(len(th) == len(td) + 122, f"head lines = develop lines + 122 ({len(th)} vs {len(td)})")
titles_h = re.findall(r'^\s*ok\s+"([^"]+)"', '\n'.join(th), re.M) + re.findall(r'^\[ "\$landed" -eq 0 \] && ok "([^"]+)"', '\n'.join(th), re.M)
titles_d = re.findall(r'^\s*ok\s+"([^"]+)"', '\n'.join(td), re.M) + re.findall(r'^\[ "\$landed" -eq 0 \] && ok "([^"]+)"', '\n'.join(td), re.M)
new = [t for t in titles_h if t not in titles_d]
ck(len(titles_h) == 28 and len(titles_d) == 23, f"ok titles: head {len(titles_h)} (28), develop {len(titles_d)} (23)")
ck(len(new) == 5 and all(('CASE 10' in t or 'CASE 11' in t) for t in new) and [t for t in titles_h if t not in new] == titles_d, "the 5 new titles are CASE 10/11's; the other 23 are develop's in order")
sm2 = difflib.SequenceMatcher(None, hd.split('\n'), hh.split('\n'), autojunk=False)
ops2 = [o for o in sm2.get_opcodes() if o[0] != 'equal']
ck(len(ops2) == 1 and ops2[0][0] == 'replace' and (ops2[0][2] - ops2[0][1], ops2[0][4] - ops2[0][3]) == (1, 39), f"hook develop -> head: {len(ops2)} changed region(s) (expected 1: -1/+39): {[(o[0], o[1]+1, o[2], o[3]+1, o[4]) for o in ops2]}")
GUARD = """    _refs='develop origin/develop refs/remotes/origin/develop'
    if git rev-parse --verify --quiet develop >/dev/null 2>&1 &&
       git rev-parse --verify --quiet origin/develop >/dev/null 2>&1 &&
       [ "$(git rev-parse develop)" != "$(git rev-parse origin/develop)" ] &&
       git merge-base --is-ancestor develop origin/develop 2>/dev/null; then
        echo "[pre-push] KS-991: local 'develop' is BEHIND origin/develop — ignoring the" >&2
        echo "[pre-push]   stale ref for base selection. (git fetch origin develop:develop" >&2
        echo "[pre-push]   to refresh it.) origin/develop is still consulted below." >&2
        _refs='origin/develop refs/remotes/origin/develop'
    fi
    for _ref in $_refs; do
"""
ck(hh.count(GUARD) == 1, "the T1/T2 anchor (the 11-line guard block) occurs once in the head's hook")
ck(hh.count("       git merge-base --is-ancestor develop origin/develop 2>/dev/null; then\n") == 1, "the Tg-A/Tg-E anchor line occurs once")
ck(hh.count('       [ "$(git rev-parse develop)" != "$(git rev-parse origin/develop)" ] &&\n') == 1, "the Tg-B anchor line occurs once")
ck(hh.count("""        echo "[pre-push] KS-991: local 'develop' is BEHIND origin/develop — ignoring the" >&2\n""") == 1, "the T3 anchor line occurs once")
ck(hd.count("    for _ref in develop origin/develop refs/remotes/origin/develop; do\n") == 1, "develop's hook: the single loop line (T1's target) occurs once")
for name in ["tf", "tf_dev", "hk", "hk_dev", "pf", "pf_dev"]:
    b = open(f"{W}/{name}", 'rb').read(); n = sum(1 for x in b if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)
    ck(n == 0, f"{name}: 0 raw control bytes (got {n})")
sys.exit(1 if fails else 0)
PY
python3 "$W/sim.py" "$W" || FAILS=$((FAILS+1))
# --- the round-1 record on disk, and the head commit's message ids (API)
[ -s "$R1_RECORD" ] && [ "$(wc -c < "$R1_RECORD" | tr -d ' ')" = "6230" ] && echo "ok   round-1 record on disk, 6230 bytes: $R1_RECORD" || { echo "FAIL round-1 record missing or not 6230 bytes: $R1_RECORD"; FAILS=$((FAILS+1)); }
[ "$(/usr/bin/grep -c -F 'The one ask' "$R1_RECORD")" = "1" ] && [ "$(/usr/bin/grep -c -F 'CASE 7' "$R1_RECORD")" = "2" ] && [ "$(/usr/bin/grep -c -F 'CASE 8' "$R1_RECORD")" = "2" ] && [ "$(/usr/bin/grep -c -F 'Not approving yet' "$R1_RECORD")" = "1" ] && echo "ok   round-1 record names 'The one ask' once, CASE 7 and CASE 8 twice each, 'Not approving yet' once" || { echo "FAIL round-1 record content"; FAILS=$((FAILS+1)); }
MSG="$( set -a; . "$SECUURA_ENV"; set +a
  HEAD="$HEAD" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/commits/" + os.environ["HEAD"]
try:
    o = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
    print(o["commit"]["message"])
except Exception as e:
    print("UNREADABLE " + type(e).__name__)
PY
)"
printf '%s\n' "$MSG" > "$W/commit_msg.txt"
if [ "$(/usr/bin/grep -c -F 'UNREADABLE' "$W/commit_msg.txt")" = "0" ]; then
  ids="$(/usr/bin/grep -o -E 'KS-[0-9]+' "$W/commit_msg.txt" | sort -u | tr '\n' ' ')"
  [ "$ids" = "KS-991 " ] && echo "ok   head commit message names KS-991 only" || { echo "FAIL head commit message ids: $ids"; FAILS=$((FAILS+1)); }
  [ "$(/usr/bin/grep -c -F '@' "$W/commit_msg.txt")" = "0" ] && echo "ok   head commit message 0 at-signs" || { echo "FAIL head commit message carries an at-sign"; FAILS=$((FAILS+1)); }
  [ "$(/usr/bin/grep -c -E '#[0-9]{3,4}' "$W/commit_msg.txt")" = "0" ] && echo "ok   head commit message 0 PR refs" || { echo "FAIL head commit message carries a PR ref"; FAILS=$((FAILS+1)); }
  [ "$(/usr/bin/grep -c -F '26 passed, 2 failed' "$W/commit_msg.txt")" = "1" ] && [ "$(/usr/bin/grep -c -F '28 passed, 0 failed' "$W/commit_msg.txt")" = "1" ] && echo "ok   head commit message carries the red-first tallies" || { echo "FAIL head commit message tallies"; FAILS=$((FAILS+1)); }
else
  echo "CANNOT READ the head commit message from the API"; exit 2
fi
echo "work dir (kept): $W"
echo "controls_check: FAILS=$FAILS"
[ "$FAILS" -eq 0 ] && exit 0 || exit 1
