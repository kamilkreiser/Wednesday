#!/bin/bash
# controls_check.sh — re-grep every positive-control token of the #879 (KS-945) TIER-2 ROUND-2 brief at
# the pinned head 0374bec00 and origin develop M38 0e78c7270 through the GitHub contents API (read-only;
# GH_TOKEN sourced by NAME from the Secuura .env, never printed). Tokens were derived from the PR's OWN
# files at these SHAs. PRESENT tokens must grep the stated count; ABSENT tokens must grep exactly 0; the
# blob table must hold; the audit-baseline must be identical both sides; the fetched bytes must equal the
# set's model/ copies.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD="${QA879_HEAD:-0374bec007d09d62afd8596d3d15abeead0526b9}"
DEV="${QA879_DEVELOP:-0e78c7270188ac45c1c29f927bdf90728f10215d}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G="${QA879_SET:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate879}"
W="$(mktemp -d "${TMPDIR:-/tmp}/qa879ctl.XXXXXX")"
GUARD='Blockchain/Dev/scripts/check-shared-relink.sh'
SUITE='Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh'
BASELINE='Blockchain/Dev/scripts/audit/audit-baseline.json'

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
mkdir -p "$G/model"
echo "controls_check.sh — #879 ${HEAD:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
for spec in "guard_h:$GUARD:$HEAD" "guard_d:$GUARD:$DEV" "suite_h:$SUITE:$HEAD" "suite_d:$SUITE:$DEV" \
            "base_h:$BASELINE:$HEAD" "base_d:$BASELINE:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; ABSENT*) echo "FAIL $n: $p ABSENT at ${ref:0:9} ($sha)"; FAILS=$((FAILS+1)); : > "$W/$n"; echo "absent" > "$W/$n.blob"; continue ;; esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
  cp "$W/$n" "$G/model/${p##*/}.${ref:0:9}"
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis guard_h d41c79538
blobis guard_d 7426b1874
blobis suite_h 867ce728a
blobis suite_d 239ea9637
blobis base_h 03d1680e3
blobis base_d 03d1680e3
cmp -s "$W/base_h" "$W/base_d" && echo "ok   audit-baseline.json identical both sides (this PR does not touch it)" || { echo "FAIL audit-baseline.json differs"; FAILS=$((FAILS+1)); }

cnt() { /usr/bin/grep -c -F -- "$2" "$W/$1"; }
ck() { local n="$1" tok="$2" want="$3"; local got; got="$(cnt "$n" "$tok")"; [ "$got" = "$want" ] && echo "ok   $n '$tok' = $want" || { echo "FAIL $n '$tok' = $got, want $want"; FAILS=$((FAILS+1)); }; }
# ---- the pm_writes function and its clauses (head only — new in this PR) ----
ck guard_h 'function pm_writes(L,   t, n, a, i, verb, segs, sg, k)' 1
ck guard_d 'function pm_writes(L,   t, n, a, i, verb, segs, sg, k)' 0
ck guard_h 'if (verb ~ /^(-v|--version|-h|--help)$/) continue' 1
ck guard_d 'if (verb ~ /^(-v|--version|-h|--help)$/) continue' 0
ck guard_h 'if (verb ~ /^(ls|list|view|info|show|config|ping|whoami|outdated|pack|version|help|search|docs|why|explain|team|owner|dist-tag|root|prefix|bin)$/) continue' 1
ck guard_h 'if (pm_writes(L)) {' 1
# ---- the OLD enumerating rule is GONE at head, present at develop ----
ck guard_d 'if (L ~ /npm[ \t]+(ci|install|i)([ \t]|$)/ || L ~ /(yarn|pnpm)[ \t]+install([ \t]|$)/) {' 1
ck guard_h 'if (L ~ /npm[ \t]+(ci|install|i)([ \t]|$)/ || L ~ /(yarn|pnpm)[ \t]+install([ \t]|$)/) {' 0
# ---- the suite's key cells (head only; the source text escapes every backtick as \` inside the
# double-quoted case-name literal) ----
ck suite_h 'expect "KS-945: \`npm run build\` after the re-link is a write' 1
ck suite_h 'expect "KS-945: \`npm --version\` is a probe, not an install"' 1
ck suite_h 'expect "KS-945: \`node -v && npm -v\` is a probe' 1
ck suite_h 'expect "KS-945: \`npm --help && pnpm -h\` is a probe"' 1
ck suite_h 'expect "KS-945: \`yarn --frozen-lockfile\` still blocks' 1
ck suite_d 'KS-945' 0
# raw-control-byte census over every fetched file + a synthetic positive control
python3 - "$W" <<'PY' || FAILS=$((FAILS+1))
import sys, os
W = sys.argv[1]; bad = 0; n = 0
for f in sorted(os.listdir(W)):
    p = os.path.join(W, f)
    if os.path.isfile(p) and not f.endswith('.blob'):
        b = open(p, 'rb').read(); n += 1; bad += sum(1 for x in b if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)
ctrl = b"const bad = 'doc\x00bad';\n"; c = [i for i, x in enumerate(ctrl) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f]
print(("ok   " if bad == 0 and c == [16] else "FAIL ") + f"raw control bytes across the {n} fetched files: {bad} (synthetic NUL control at offset {c})")
sys.exit(0 if bad == 0 and c == [16] else 1)
PY
echo "work dir (kept): $W"
echo "controls_check: FAILS=$FAILS"
[ "$FAILS" -eq 0 ] && exit 0 || exit 1
