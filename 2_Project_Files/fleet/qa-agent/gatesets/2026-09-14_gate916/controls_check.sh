#!/bin/bash
# controls_check.sh — re-grep every positive-control token of the #916 (KS-993+KS-1026) TIER-2 ROUND-1
# brief at the pinned head 12507d200 and origin develop M38 0e78c7270 through the GitHub contents API
# (read-only; GH_TOKEN sourced by NAME from the Secuura .env, never printed). Tokens were derived from
# the PR's OWN files at these SHAs. PRESENT tokens must grep the stated count; ABSENT tokens must grep
# exactly 0; the blob table must hold; actor_manifest.ts at head must be byte-identical to develop's copy
# (the measured proof the merge-in resolved fully to develop's text); the fetched bytes must equal the
# set's model/ copies.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD="${QA916_HEAD:-12507d200375a5ebcab1579920cb75e74a6391f1}"
DEV="${QA916_DEVELOP:-0e78c7270188ac45c1c29f927bdf90728f10215d}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G="${QA916_SET:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate916}"
W="$(mktemp -d "${TMPDIR:-/tmp}/qa916ctl.XXXXXX")"
PKG='systemTest/package.json'; TESTF='systemTest/performance/tests/unit/runner/actor_manifest.test.ts'
README='systemTest/README.md'; AM='systemTest/performance/runner/actor_manifest.ts'
PEETF='systemTest/performance/tests/unit/runner/actorManifest.test.ts'

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
echo "controls_check.sh — #916 ${HEAD:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
for spec in "pkg_h:$PKG:$HEAD" "test_h:$TESTF:$HEAD" "readme_h:$README:$HEAD" "readme_d:$README:$DEV" \
            "am_h:$AM:$HEAD" "am_d:$AM:$DEV" "peet_d:$PEETF:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; ABSENT*) echo "FAIL $n: $p ABSENT at ${ref:0:9} ($sha)"; FAILS=$((FAILS+1)); : > "$W/$n"; echo "absent" > "$W/$n.blob"; continue ;; esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
  cp "$W/$n" "$G/model/${p##*/}.${ref:0:9}"
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis pkg_h b757d4c0d
blobis test_h 4955bc92f
blobis readme_h 2862e0bdb
blobis readme_d b9d4f9407
blobis am_h 22feeb397
blobis am_d 22feeb397
blobis peet_d 6380bc33e

# the measured proof: actor_manifest.ts at head is BYTE-IDENTICAL to develop's copy (not path/name-equal — content-equal)
cmp -s "$W/am_h" "$W/am_d" && echo "ok   actor_manifest.ts at head == develop byte-for-byte (the merge-in resolved fully to develop's text)" || { echo "FAIL actor_manifest.ts at head differs from develop"; FAILS=$((FAILS+1)); }

cnt() { /usr/bin/grep -c -F -- "$2" "$W/$1"; }
ck() { local n="$1" tok="$2" want="$3"; local got; got="$(cnt "$n" "$tok")"; [ "$got" = "$want" ] && echo "ok   $n '$tok' = $want" || { echo "FAIL $n '$tok' = $got, want $want"; FAILS=$((FAILS+1)); }; }
# ---- package.json anchors
ck pkg_h 'fixtures/tsconfig.json playwright/tsconfig.json performance/tsconfig.json performance/tsconfig.node.json akto/tsconfig.json api-explorer/tsconfig.json api-explorer/tsconfig.test.json' 1
ck pkg_h '"typecheck":' 1; ck pkg_h '"pretypecheck":' 1
ck pkg_h 'Carries NO dependencies on purpose (KS-993)' 1
ck pkg_h 'declares no dependencies of its own on purpose (KS-993)' 1
# ---- the trimmed test file anchors
ck test_h 'survives a corrupt manifest by falling back rather than throwing' 1
ck test_h "it(" 1
# ---- develop's Peter file: the cell-6 counterpart must be ABSENT (0), confirming the trim's premise
ck peet_d 'corrupt' 0
ck peet_d "it(" 8
ck peet_d 'it.each' 2
# ---- the catch-block anchor T1 tampers (present once, on develop's copy = the head's copy, byte-identical)
ck am_d '} catch {' 1
ck am_h '} catch {' 1
# ---- README anchors
ck readme_h 'Root entry point: `npm run typecheck` runs all seven tsconfigs (KS-993)' 1
ck readme_d 'Root entry point: `npm run typecheck` runs all seven tsconfigs (KS-993)' 0
ck readme_h 'there is no systemTest-root package.json' 0
ck readme_d 'there is no systemTest-root package.json' 1

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
