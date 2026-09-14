#!/bin/bash
# controls_check.sh — re-grep every positive-control token of the L9 (#940 #941 #942 #887) TIER-2 ROUND-1 brief at the PINNED
# heads 1aa708be9 / d105e07a8 / 53b9c3cc1 / 3aee3deed, their bases (a1e49d151 for #940/#941; c1676269d, cb7a3e3be, de376a9f1)
# and origin develop M18 8861e6216 through the GitHub contents API (read-only; GH_TOKEN sourced by NAME from the Secuura .env,
# never printed). Tokens were derived from the PRs' OWN files at these SHAs — never carried from another gate's brief. PRESENT
# tokens must grep the stated count; ABSENT tokens must grep exactly 0; the blob table must hold; the untouched sibling
# workflow of each PR must be blob-identical to develop's; #941's exceptions.yml must equal its banner + develop's whole
# file; #887's workflow hunk must be byte-for-byte the reviewed one; the fetched bytes must equal the set's model/ copies;
# then guards_sim.py's predictions are re-derived on the fetched bytes (FAILS=0 required).
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
H940="${QAL9_HEAD940:-1aa708be9fcf7a23575398546d84848c967e81c5}"
H941="${QAL9_HEAD941:-d105e07a81c8549b7f47c0542e9594204ce6f599}"
H942="${QAL9_HEAD942:-53b9c3cc1a89f513620516c580a5de5bd60c64de}"
H887="${QAL9_HEAD887:-3aee3deed2e3ac557f0a52c0797c2a4a8df25f69}"
DEV="${QAL9_DEVELOP:-8861e62161466c40f08d2b10a30edeb203123993}"
BASE3='a1e49d15152102acec7c97d96918211227c7fe1e'; C942='c1676269d4b438b9b3f897d80bfeae1161dbec39'; REV887='cb7a3e3be735c2536e8246877fac72ecd4bcd06d'; MRG887='de376a9f10d456a7030b169ba921f88305b70be5'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G="${QAL9_SET:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL9}"
W="$(mktemp -d "${TMPDIR:-/tmp}/qaL9ctl.XXXXXX")"
SCAN='.github/workflows/security-scan.yml'; GATES='.github/workflows/pr-security-gates.yml'; SUITES='.github/workflows/pr-platform-suites.yml'
EXC='Blockchain/Dev/.security/exceptions.yml'; MQ='systemTest/__tests__/manifest_quarantine.test.sh'; BL='BACKLOG.md'; DOC='Blockchain/Dev/docs/DEV-PROCESS.md'; LOCK='Blockchain/Dev/package-lock.json'
PWPKG='systemTest/playwright/package.json'

fetch() { # path ref outfile -> prints blob sha (or UNREADABLE / ABSENT)
  ( set -a; . "$SECUURA_ENV"; set +a
    PTH="$1" REF="$2" OUT="$3" python3 - <<'PY'
import base64, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/contents/" + os.environ["PTH"] + "?ref=" + os.environ["REF"]
try:
    o = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except urllib.error.HTTPError as e:
    print("ABSENT HTTP%d" % e.code); sys.exit(0)
except Exception as e:
    print("UNREADABLE " + type(e).__name__); sys.exit(0)
open(os.environ["OUT"], "wb").write(base64.b64decode(o["content"]))
print(o["sha"])
PY
  )
}
FAILS=0
echo "controls_check.sh — #940 ${H940:0:9}, #941 ${H941:0:9}, #942 ${H942:0:9}, #887 ${H887:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
for spec in "scan940:$SCAN:$H940" "scan941:$SCAN:$H941" "scan942:$SCAN:$H942" "scan_d:$SCAN:$DEV" "scan_b:$SCAN:$BASE3" \
            "gates940:$GATES:$H940" "gates941:$GATES:$H941" "gates942:$GATES:$H942" "gates_c942:$GATES:$C942" "gates_d:$GATES:$DEV" \
            "exc941:$EXC:$H941" "exc942:$EXC:$H942" "exc_d:$EXC:$DEV" "mq942:$MQ:$H942" "mq_c942:$MQ:$C942" "mq_d:$MQ:$DEV" "mq_b:$MQ:$BASE3" \
            "bl942:$BL:$H942" "bl_d:$BL:$DEV" "suites887:$SUITES:$H887" "suites_rev:$SUITES:$REV887" "suites_mrg:$SUITES:$MRG887" "suites_d:$SUITES:$DEV" \
            "doc887:$DOC:$H887" "doc_mrg:$DOC:$MRG887" "doc_rev:$DOC:$REV887" "doc_d:$DOC:$DEV" "lock887:$LOCK:$H887" "lock_d:$LOCK:$DEV" "pw942:$PWPKG:$H942" "pw_b:$PWPKG:$BASE3"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; ABSENT*) echo "FAIL $n: $p ABSENT at ${ref:0:9} ($sha)"; FAILS=$((FAILS+1)); : > "$W/$n"; echo "absent" > "$W/$n.blob"; continue ;; esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis scan940 fac9ef1b8; blobis scan941 3b272c2d9; blobis scan942 47da5cac9; blobis scan_d 47da5cac9; blobis scan_b 47da5cac9
blobis gates940 571817703; blobis gates941 571817703; blobis gates942 eac30f09b; blobis gates_c942 eac30f09b; blobis gates_d 571817703
blobis exc941 d6401126e; blobis exc942 d238e899a; blobis exc_d d238e899a
blobis mq942 2ae67f244; blobis mq_c942 e58518966; blobis mq_d 57a0f3582; blobis mq_b dbf52276b
blobis bl942 a8dadd27e; blobis bl_d 9d99b3bec
blobis suites887 fd5e8343c; blobis suites_rev 8607f9bf2; blobis suites_mrg fd5e8343c; blobis suites_d a509ad793
blobis doc887 efe300e69; blobis doc_mrg 1eba87408; blobis doc_rev f496bcd74; blobis doc_d c9cd41d58
blobis lock887 17d2061b3; blobis lock_d 17d2061b3
# fetched bytes == the set's model copies (what the brief and the sim were written from)
same() { cmp -s "$W/$1" "$G/model/$2" && echo "ok   $1 == model/$2" || { echo "FAIL $1 != model/$2"; FAILS=$((FAILS+1)); }; }
same scan940 security-scan.yml.1aa708be9; same scan941 security-scan.yml.d105e07a8; same scan_d security-scan.yml.8861e6216
same gates942 pr-security-gates.yml.53b9c3cc1; same gates_d pr-security-gates.yml.8861e6216
same exc941 exceptions.yml.d105e07a8; same exc_d exceptions.yml.8861e6216
same mq942 manifest_quarantine.test.sh.53b9c3cc1; same mq_d manifest_quarantine.test.sh.8861e6216; same mq_c942 manifest_quarantine.test.sh.c1676269d
same bl942 BACKLOG.md.53b9c3cc1; same bl_d BACKLOG.md.8861e6216
same suites887 pr-platform-suites.yml.3aee3deed; same suites_rev pr-platform-suites.yml.cb7a3e3be; same suites_d pr-platform-suites.yml.8861e6216
same doc887 DEV-PROCESS.md.3aee3deed; same doc_mrg DEV-PROCESS.md.de376a9f1
# the sibling files untouched per PR
cmp -s "$W/gates940" "$W/gates_d" && cmp -s "$W/gates941" "$W/gates_d" && echo "ok   #940/#941 leave pr-security-gates.yml byte-identical to develop" || { echo "FAIL #940/#941 pr-security-gates.yml differs from develop"; FAILS=$((FAILS+1)); }
cmp -s "$W/scan942" "$W/scan_d" && cmp -s "$W/exc942" "$W/exc_d" && echo "ok   #942 leaves security-scan.yml + exceptions.yml byte-identical to develop" || { echo "FAIL #942 security-scan.yml/exceptions.yml differ from develop"; FAILS=$((FAILS+1)); }
cmp -s "$W/lock887" "$W/lock_d" && echo "ok   #887 leaves package-lock.json byte-identical to develop (the live red's mechanism is not this PR's)" || { echo "FAIL #887 lockfile differs"; FAILS=$((FAILS+1)); }
diff -q <(tail -26 "$W/exc941") "$W/exc_d" >/dev/null && echo "ok   #941 exceptions.yml = 22-line banner + develop's 26 lines unchanged" || { echo "FAIL #941 exceptions.yml tail != develop's file"; FAILS=$((FAILS+1)); }
cmp -s "$W/suites887" "$W/suites_mrg" && echo "ok   #887 the doc commit does not touch the workflow (head blob = the merge's)" || { echo "FAIL #887 workflow moved in the doc commit"; FAILS=$((FAILS+1)); }
cnt() { /usr/bin/grep -c -F -- "$2" "$W/$1"; }
ck() { local n="$1" tok="$2" want="$3"; local got; got="$(cnt "$n" "$tok")"; [ "$got" = "$want" ] && echo "ok   $n '$tok' = $want" || { echo "FAIL $n '$tok' = $got, want $want"; FAILS=$((FAILS+1)); }; }
# ---- #940 anchors (security-scan.yml at head vs develop / #941)
ck scan940 '        shell: bash {0}' 1; ck scan940 'shell: bash {0}' 2; ck scan940 'do NOT delete it' 1; ck scan940 'That is FALSE and was measured so' 1; ck scan940 'is currently inert' 0
ck scan940 'out=$(npm run audit:contract --silent 2>&1); rc=$?' 1; ck scan940 'audit-contract suites are red' 1; ck scan940 'set -uo pipefail' 2
ck scan_d '        shell: bash {0}' 0; ck scan_d 'is currently inert' 1; ck scan_d 'out=$(npm run audit:contract --silent 2>&1); rc=$?' 1; ck scan_d 'run: |' 8
ck scan941 '        shell: bash {0}' 1; ck scan941 'do NOT delete it' 0; ck scan941 'is currently inert' 1
# ---- #941 anchors
ck scan941 'node scripts/audit/audit-gate.mjs' 1; ck scan941 'check-npm-audit.mjs npm-audit.json .security/exceptions.yml' 0; ck scan941 'SCA gate — npm audit vs the triaged baseline (warn-first)' 1; ck scan941 'SCA gate — npm audit vs allow-list (warn-first)' 0
ck scan941 "continue-on-error: \${{ github.event_name == 'pull_request' }}" 4; ck scan941 'one-list-triage-two' 1; ck scan941 '0) echo "OK — no advisories outside the triaged baseline" ;;' 1; ck scan941 '2) echo "SKIP (advisory) — npm audit could not run (offline / registry unreachable)" ;;' 1; ck scan941 '3) echo "FAIL — the audit gate REFUSED to report a verdict (see its line above)"; exit 1 ;;' 1
ck scan_d 'node scripts/audit/audit-gate.mjs' 0; ck scan_d 'check-npm-audit.mjs npm-audit.json .security/exceptions.yml' 1; ck scan_d "continue-on-error: \${{ github.event_name == 'pull_request' }}" 4
ck exc941 'SUPERSEDED 2026-09-10 (KS-1077)' 1; ck exc941 'THIS FILE IS NO LONGER READ BY ANY GATE' 1; ck exc_d 'SUPERSEDED 2026-09-10 (KS-1077)' 0; ck exc_d 'exceptions: []' 1
# ---- #942 anchors
ck gates942 'npm install --global --no-audit --no-fund tsx@4.23.12' 1; ck gates942 'tsx@4.23.12' 1; ck gates942 'tsx@4.23.13' 1; ck gates942 'Pin tsx for the shell suites (KS-1078 — no registry fetch mid-test)' 1; ck gates942 '^4.23.12 in akto) so the suites run what those packages expect' 1; ck gates942 'bash scripts/run-shell-suites.sh' 1
ck gates_d 'tsx@4.23.12' 0; ck gates_d 'Pin tsx' 0; ck gates_d 'bash scripts/run-shell-suites.sh' 1
ck mq942 '2>"$TMP/probe.err")" \' 1; ck mq942 '2>"$TMP/probe.err"' 2; ck mq942 'probe.err' 3; ck mq942 '2>&1' 2; ck mq942 '   || [ "$probe" != "NULL" ]; then' 1; ck mq942 "printf '     stdout: %s\\n'" 1; ck mq942 "printf '     stderr: %s\\n'" 1; ck mq942 'env -u SECUURA_STACK_SLOT -u STACK_SLOT -u SECUURA_ARTIFACT_SUFFIX npx tsx "$TMP/drive.ts"' 5
ck mq_d '2>"$TMP/probe.err"' 0; ck mq_d '2>&1' 1; ck mq_d 'env -u SECUURA_STACK_SLOT -u STACK_SLOT -u SECUURA_ARTIFACT_SUFFIX npx tsx "$TMP/drive.ts"' 5; ck mq_c942 'env -u SECUURA_STACK_SLOT' 0; ck mq_c942 '2>"$TMP/probe.err"' 2
ck bl942 'quarantine_call_sites.test.sh` uses the same' 1; ck bl942 'smoke-test.sh section 6 calls' 1; ck bl942 '- [ ]' 33; ck bl_d 'quarantine_call_sites.test.sh` uses the same' 0; ck bl_d '- [ ]' 32
ck pw942 '"tsx": "^4.23.13"' 1; ck pw_b '"tsx": "^4.23.1"' 1; ck pw_b '"tsx": "^4.23.13"' 0
# ---- #887 anchors
ck suites887 'workspace-suites:' 1; ck suites887 'Workspace unit suites (advisory, non-blocking)' 1; ck suites887 'IT CANNOT RUN TODAY' 1; ck suites887 'npm run build --workspaces --if-present' 2; ck suites887 'npm run test --workspaces --if-present' 2
ck suites_rev 'workspace-suites:' 1; ck suites_d 'workspace-suites:' 0; ck suites_d 'IT CANNOT RUN TODAY' 0
ck doc887 '2026-09-14, head `de376a9f1`' 1; ck doc887 'It could not run when it was written' 1; ck doc887 'Actions resumed on 2026-09-09' 1; ck doc887 'OpenSSL 3.6.3' 1; ck doc887 '1 of 208' 1; ck doc887 '0 of 588' 1; ck doc887 'it cannot run today' 0; ck doc887 'Measured baseline, 2026-09-07 on develop' 0
ck doc_mrg 'it cannot run today' 1; ck doc_mrg 'Measured baseline, 2026-09-07 on develop' 1; ck doc_mrg 'OpenSSL 3.6.3' 0
# the reviewed hunk == the head hunk (diff-of-diffs on the fetched bytes: +/- lines of (rev - base) vs (head - dev) — the base copy of the workflow is develop's at b6884888d; fetch it)
sha="$(fetch "$SUITES" b6884888da5ee326d7fbc224797bbc9dbb9e7179 "$W/suites_b887")"; echo "read suites_b887 = pr-platform-suites.yml @ b6884888d: blob ${sha:0:9}"
diff "$W/suites_b887" "$W/suites_rev" | /usr/bin/grep '^[<>]' > "$W/hunk_rev.txt"; diff "$W/suites_d" "$W/suites887" | /usr/bin/grep '^[<>]' > "$W/hunk_head.txt"
cmp -s "$W/hunk_rev.txt" "$W/hunk_head.txt" && echo "ok   #887 the reviewed workflow hunk (b6884888d->cb7a3e3be) == the head hunk (develop->3aee3deed), $(wc -l < "$W/hunk_rev.txt" | tr -d ' ') changed lines" || { echo "FAIL #887 workflow hunk differs between the reviewed head and the head"; FAILS=$((FAILS+1)); }
diff "$W/suites_b887" "$W/suites_d" | /usr/bin/grep '^[<>]' > "$W/dev_own.txt"; diff "$W/suites_rev" "$W/suites887" | /usr/bin/grep '^[<>]' > "$W/rev_to_head.txt"
cmp -s "$W/dev_own.txt" "$W/rev_to_head.txt" && echo "ok   #887 head-vs-reviewed workflow delta == develop's own delta ($(wc -l < "$W/dev_own.txt" | tr -d ' ') changed lines; no seat line)" || { echo "FAIL #887 head-vs-reviewed delta is not develop's own"; FAILS=$((FAILS+1)); }
# ---- the sim on the FETCHED bytes: point guards_sim.py's model dir at a scratch model/ built from the fetched files
mkdir -p "$W/sim/model"; cp "$W/scan_d" "$W/sim/model/security-scan.yml.8861e6216"; cp "$W/scan940" "$W/sim/model/security-scan.yml.1aa708be9"; cp "$W/scan941" "$W/sim/model/security-scan.yml.d105e07a8"; cp "$G/model/security-scan.yml.940+941" "$W/sim/model/security-scan.yml.940+941"
cp "$W/gates_d" "$W/sim/model/pr-security-gates.yml.8861e6216"; cp "$W/gates942" "$W/sim/model/pr-security-gates.yml.53b9c3cc1"; cp "$W/mq942" "$W/sim/model/manifest_quarantine.test.sh.53b9c3cc1"
python3 "$G/guards_sim.py" "$W/sim" > "$W/sim.out" 2>&1; rc=$?; echo "guards_sim.py on the fetched bytes: rc=$rc, $(/usr/bin/grep -c '^ok ' "$W/sim.out") ok / $(/usr/bin/grep -c '^FAIL ' "$W/sim.out") FAIL"; [ "$rc" -eq 0 ] || FAILS=$((FAILS+1))
# raw-control-byte census over every fetched file + a synthetic positive control
python3 - "$W" <<'PY' || FAILS=$((FAILS+1))
import sys, os
W = sys.argv[1]; bad = 0; n = 0
for f in sorted(os.listdir(W)):
    p = os.path.join(W, f)
    if os.path.isfile(p) and not f.endswith('.blob') and not f.endswith('.txt') and f != 'sim.out':
        b = open(p, 'rb').read(); n += 1; bad += sum(1 for x in b if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)
ctrl = b"const bad = 'doc\x00bad';\n"; c = [i for i, x in enumerate(ctrl) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f]
print(("ok   " if bad == 0 and c == [16] else "FAIL ") + f"raw control bytes across the {n} fetched files: {bad} (synthetic NUL control at offset {c})")
sys.exit(0 if bad == 0 and c == [16] else 1)
PY
echo "work dir (kept): $W"
echo "controls_check: FAILS=$FAILS"
[ "$FAILS" -eq 0 ] && exit 0 || exit 1
