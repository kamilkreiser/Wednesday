#!/bin/bash
# controls_check.sh — re-grep every positive-control token of the #939 (KS-1068) TIER-2 ROUND-1 brief at the
# PINNED head 284661efe and origin develop M38 0e78c7270, through the GitHub contents API (read-only; GH_TOKEN
# sourced by NAME from the Secuura .env, never printed). Tokens were derived from the PR's OWN files at these
# SHAs — never carried from another gate's brief. PRESENT tokens must grep the stated count; ABSENT tokens must
# grep exactly 0; the blob table must hold; the audit-baseline must be identical both sides; the fetched bytes
# must equal the set's model/ copies.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD_SHA="${QA939_HEAD:-284661efe262b825d83b31b875020ff7765757b8}"
DEV="${QA939_DEVELOP:-0e78c7270188ac45c1c29f927bdf90728f10215d}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G="${QA939_SET:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate939}"
W="$(mktemp -d "${TMPDIR:-/tmp}/qa939ctl.XXXXXX")"
TEST='Blockchain/Dev/services/originate/src/__tests__/ks1068-blockchain-blob-type.test.ts'
REPOFILE='Blockchain/Dev/services/originate/src/repositories/documentRepo.ts'
DOC='Blockchain/Dev/services/originate/src/routes/documents.ts'
BASELINE='Blockchain/Dev/scripts/audit/audit-baseline.json'

fetch() { # path ref outfile -> prints blob sha (or UNREADABLE / ABSENT). Falls back to the git blobs API for
          # files over the contents API's 1MB inline-content cap.
  ( set -a; . "$SECUURA_ENV"; set +a
    PTH="$1" REF="$2" OUT="$3" python3 - <<'PY'
import base64, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
hdrs = {"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/contents/" + os.environ["PTH"] + "?ref=" + os.environ["REF"]
try:
    o = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=hdrs), timeout=60))
except urllib.error.HTTPError as e:
    print("ABSENT HTTP%d" % e.code); sys.exit(0)
except Exception as e:
    print("UNREADABLE " + type(e).__name__); sys.exit(0)
sha = o["sha"]; content = o.get("content") or ""
if content:
    open(os.environ["OUT"], "wb").write(base64.b64decode(content))
else:
    bu = "https://api.github.com/repos/Secuura/Distributed_Secuura/git/blobs/" + sha
    try:
        b = json.load(urllib.request.urlopen(urllib.request.Request(bu, headers=hdrs), timeout=60))
    except Exception as e:
        print("UNREADABLE " + type(e).__name__); sys.exit(0)
    open(os.environ["OUT"], "wb").write(base64.b64decode(b["content"]))
print(sha)
PY
  )
}
FAILS=0
echo "controls_check.sh — #939 ${HEAD_SHA:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
EXPECT_ABSENT='test_d'
for spec in "test_h:$TEST:$HEAD_SHA" "test_d:$TEST:$DEV" "repo_h:$REPOFILE:$HEAD_SHA" "repo_d:$REPOFILE:$DEV" \
            "doc_h:$DOC:$HEAD_SHA" "doc_d:$DOC:$DEV" "base_h:$BASELINE:$HEAD_SHA" "base_d:$BASELINE:$DEV"; do
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
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis test_h f45d3743c
blobis repo_h 6e059d36c; blobis repo_d f715095c1
blobis doc_h f403c37a5; blobis doc_d b2f4bf351
blobis base_h 03d1680e3; blobis base_d 03d1680e3
cmp -s "$W/base_h" "$W/base_d" && echo "ok   audit-baseline.json identical both sides (this PR does not touch it)" || { echo "FAIL audit-baseline.json differs"; FAILS=$((FAILS+1)); }
same() { cmp -s "$W/$1" "$G/model/$2" && echo "ok   $1 == model/$2" || { echo "FAIL $1 != model/$2"; FAILS=$((FAILS+1)); }; }
same test_h ks1068-blockchain-blob-type.test.ts.284661efe
same repo_h documentRepo.ts.284661efe; same repo_d documentRepo.ts.0e78c7270
same doc_h documents.ts.284661efe; same doc_d documents.ts.0e78c7270
cnt() { /usr/bin/grep -c -F -- "$2" "$W/$1"; }
ck() { local n="$1" tok="$2" want="$3"; local got; got="$(cnt "$n" "$tok")"; [ "$got" = "$want" ] && echo "ok   $n '$tok' = $want" || { echo "FAIL $n '$tok' = $got, want $want"; FAILS=$((FAILS+1)); }; }
# ---- the type-widening anchors (documentRepo.ts at head vs develop) ----
ck repo_h '    threadToken?: {' 1; ck repo_d '    threadToken?: {' 0
ck repo_h 'simulatedTxRef?: string | null;' 1; ck repo_d 'simulatedTxRef?: string | null;' 0
ck repo_h 'confidence?: string;' 1
ck repo_h 'txHash?: string | null;' 1; ck repo_d 'txHash: string | null;' 1
# ---- the R2 clause anchor: present at head, absent at develop ----
ck repo_h 'Carried forward on a HASHED anchor_failed write' 1
ck repo_d 'Carried forward on a HASHED anchor_failed write' 0
ck repo_h 'anchorStateSync.ts'"'"'s reconcile carry' 1
# ---- the red-proof cell's anchor and restore-target text (informational: the test file references
# threadToken several times — the load-bearing anchor for the tamper is documentRepo.ts's declaration,
# already checked above as repo_h '    threadToken?: {' = 1) ----
tt="$(cnt test_h 'threadToken')"
echo "  test_h 'threadToken' occurrences: $tt (informational)"
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
