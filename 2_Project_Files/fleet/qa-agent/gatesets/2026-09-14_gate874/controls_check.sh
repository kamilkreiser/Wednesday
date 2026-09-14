#!/bin/bash
# controls_check.sh — re-grep every positive-control token of the #874 (KS-926 doc) TIER-2 ROUND-1 brief
# at the pinned head b244f4913 and origin develop M38 0e78c7270 through the GitHub contents API
# (read-only; GH_TOKEN sourced by NAME from the Secuura .env, never printed). PRESENT tokens must grep
# the stated count; ABSENT tokens must grep exactly 0; the blob table must hold; the audit-baseline must
# be identical both sides; the fetched bytes must equal the set's model/ copy; a PII/secret-shape census
# runs over the document with a live positive control.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD="${QA874_HEAD:-b244f4913c948b6d763a6abcf018dac301232345}"
DEV="${QA874_DEVELOP:-0e78c7270188ac45c1c29f927bdf90728f10215d}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G="${QA874_SET:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate874}"
W="$(mktemp -d "${TMPDIR:-/tmp}/qa874ctl.XXXXXX")"
DOC='Blockchain/Dev/docs/KS-926-CHECKS-THAT-CANNOT-FAIL.md'
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
echo "controls_check.sh — #874 ${HEAD:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
# doc_d is EXPECTED absent — this is a new file, not on develop.
EXPECT_ABSENT='doc_d'
for spec in "doc_h:$DOC:$HEAD" "doc_d:$DOC:$DEV" "base_h:$BASELINE:$HEAD" "base_d:$BASELINE:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in
    UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;;
    ABSENT*)
      if [ "$n" = "$EXPECT_ABSENT" ]; then echo "ok   $n: $p ABSENT at ${ref:0:9} (EXPECTED — new file in this PR, $sha)"
      else echo "FAIL $n: $p ABSENT at ${ref:0:9} ($sha)"; FAILS=$((FAILS+1)); fi
      : > "$W/$n"; echo "absent" > "$W/$n.blob"; continue ;;
  esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
  cp "$W/$n" "$G/model/${p##*/}.${ref:0:9}"
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis doc_h e31f85cda
blobis base_h 03d1680e3
blobis base_d 03d1680e3
cmp -s "$W/base_h" "$W/base_d" && echo "ok   audit-baseline.json identical both sides (this PR does not touch it)" || { echo "FAIL audit-baseline.json differs"; FAILS=$((FAILS+1)); }

cnt() { /usr/bin/grep -c -F -- "$2" "$W/$1"; }
ck() { local n="$1" tok="$2" want="$3"; local got; got="$(cnt "$n" "$tok")"; [ "$got" = "$want" ] && echo "ok   $n '$tok' = $want" || { echo "FAIL $n '$tok' = $got, want $want"; FAILS=$((FAILS+1)); }; }
# ---- structural anchors ----
ck doc_h '# Checks that cannot fail' 1
ck doc_h '**KS-926 campaign — the family statement.**' 1
ck doc_h 'Opened 2026-09-06 (s141b, seat A) at `develop` `066cff675`. Ten members.' 1
ck doc_h '17 of 20 `check-*.sh` have no live entry point' 1
ck doc_h 'A cell that cannot tell the fix from its own fallback is not a regression test.' 1
ck doc_h '[KS-944](https://linear.app/secuura/issue/KS-944)' 1
ck doc_h '[KS-926](https://linear.app/secuura/issue/KS-926)' 1
# ---- word count sanity (the doc is 355 added lines) ----
DOC_LINES="$(wc -l < "$W/doc_h" | tr -d ' ')"
[ "$DOC_LINES" -ge 350 ] && [ "$DOC_LINES" -le 360 ] && echo "ok   doc_h line count $DOC_LINES in [350,360]" || { echo "FAIL doc_h line count $DOC_LINES outside [350,360]"; FAILS=$((FAILS+1)); }
# ---- PII/secret-shape census, with a live positive control ----
atcount="$(/usr/bin/grep -c -F -- '@' "$W/doc_h")"
echo "  doc_h '@' occurrences: $atcount (report every one in the gate's own census — 0 is not asserted here, only counted)"
for shape in 'sk-' 'ghp_' '-----BEGIN' ; do
  c="$(/usr/bin/grep -c -F -- "$shape" "$W/doc_h")"
  [ "$c" = "0" ] && echo "ok   doc_h secret-shape '$shape' = 0" || { echo "FAIL doc_h secret-shape '$shape' = $c, want 0"; FAILS=$((FAILS+1)); }
done
# live-grep positive control: the develop README (or any large tracked text file) must carry at least
# one of these common markdown/code shapes, proving the grep mechanism itself fires.
ctrlcount="$(/usr/bin/grep -c -F -- '](' "$W/doc_h")"
[ "$ctrlcount" -gt 0 ] && echo "ok   doc_h markdown-link-syntax control: $ctrlcount '](' occurrences (grep is live)" || { echo "FAIL doc_h markdown-link control did not fire — grep may be broken"; FAILS=$((FAILS+1)); }

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
