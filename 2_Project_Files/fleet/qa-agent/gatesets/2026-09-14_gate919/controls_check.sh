#!/bin/bash
# controls_check.sh — re-grep every positive-control token of the #919 (KS-739) TIER-2 ROUND-1 brief at the
# PINNED head 4736e2277 and origin develop M38 0e78c7270, through the GitHub contents API (read-only; GH_TOKEN
# sourced by NAME from the Secuura .env, never printed). Tokens were derived from the PR's OWN files at these
# SHAs — never carried from another gate's brief. PRESENT tokens must grep the stated count; ABSENT tokens must
# grep exactly 0; the blob table must hold; the audit-baseline must be identical both sides; the fetched bytes
# must equal the set's model/ copies.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD_SHA="${QA919_HEAD:-4736e22771c12e56d004f58a67f960ddbc0b0508}"
DEV="${QA919_DEVELOP:-0e78c7270188ac45c1c29f927bdf90728f10215d}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G="${QA919_SET:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate919}"
W="$(mktemp -d "${TMPDIR:-/tmp}/qa919ctl.XXXXXX")"
YAML='Blockchain/Dev/docs/openapi/secuura-api.yaml'
OAI='Blockchain/Dev/services/originate/src/originate.openapi.ts'
DOC='Blockchain/Dev/services/originate/src/routes/documents.ts'
TEST='Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts'
BASELINE='Blockchain/Dev/scripts/audit/audit-baseline.json'

fetch() { # path ref outfile -> prints blob sha (or UNREADABLE / ABSENT). Falls back to the git blobs API for
          # files over the contents API's 1MB inline-content cap (secuura-api.yaml is ~1.3MB) — the contents
          # API still returns a "sha" for those but an empty "content", so absence of content past a valid sha
          # triggers the fallback fetch by blob sha rather than being misread as ABSENT.
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
sha = o["sha"]
content = o.get("content") or ""
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
echo "controls_check.sh — #919 ${HEAD_SHA:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
# test_d is EXPECTED absent — the test file is new in this PR, it does not exist on develop.
EXPECT_ABSENT='test_d'
for spec in "yaml_h:$YAML:$HEAD_SHA" "yaml_d:$YAML:$DEV" "oai_h:$OAI:$HEAD_SHA" "oai_d:$OAI:$DEV" \
            "doc_h:$DOC:$HEAD_SHA" "doc_d:$DOC:$DEV" "test_h:$TEST:$HEAD_SHA" "test_d:$TEST:$DEV" \
            "base_h:$BASELINE:$HEAD_SHA" "base_d:$BASELINE:$DEV"; do
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
blobis yaml_h 8c3df7194; blobis yaml_d 298d95e4a
blobis oai_h 509f13abb; blobis oai_d 12fb03ba6
blobis doc_h a18a8ac57; blobis doc_d b2f4bf351
blobis test_h 1b0eb5dd8
blobis base_h 03d1680e3; blobis base_d 03d1680e3
cmp -s "$W/base_h" "$W/base_d" && echo "ok   audit-baseline.json identical both sides (this PR does not touch it)" || { echo "FAIL audit-baseline.json differs"; FAILS=$((FAILS+1)); }
# fetched bytes == the set's model copies (what the brief was written from)
same() { cmp -s "$W/$1" "$G/model/$2" && echo "ok   $1 == model/$2" || { echo "FAIL $1 != model/$2"; FAILS=$((FAILS+1)); }; }
same yaml_h secuura-api.yaml.4736e2277; same yaml_d secuura-api.yaml.0e78c7270
same oai_h originate.openapi.ts.4736e2277; same oai_d originate.openapi.ts.0e78c7270
same doc_h documents.ts.4736e2277; same doc_d documents.ts.0e78c7270
same test_h ks739-transfer-custody-lookup-4xx-mapping.test.ts.4736e2277
cnt() { /usr/bin/grep -c -F -- "$2" "$W/$1"; }
ck() { local n="$1" tok="$2" want="$3"; local got; got="$(cnt "$n" "$tok")"; [ "$got" = "$want" ] && echo "ok   $n '$tok' = $want" || { echo "FAIL $n '$tok' = $got, want $want"; FAILS=$((FAILS+1)); }; }
# ---- the route change's anchors (documents.ts at head vs develop) ----
ck doc_h 'RECIPIENT_LOOKUP_FAILED' 1; ck doc_h 'if (lookupRes.status >= 400 && lookupRes.status < 500)' 1
ck doc_d 'RECIPIENT_LOOKUP_FAILED' 0; ck doc_d 'if (lookupRes.status >= 400 && lookupRes.status < 500)' 0
# ---- the yaml's KS-739 anchors ----
ck yaml_h 'KS-739' 3; ck yaml_h 'verify-file' 0
ck yaml_d 'KS-739' 0
ck yaml_h 'postDocumentsByIdTransferCustody' 1; ck yaml_d 'postDocumentsByIdTransferCustody' 1
# ---- the PII control: the hunk's hint strings carry no at-sign / secuura.ai; the yaml overall does (control) ----
atsigns="$(/usr/bin/grep -c -F -- '@' "$W/yaml_h")"
[ "$atsigns" -gt 0 ] && echo "ok   yaml_h control: $atsigns at-sign lines elsewhere in the yaml (grep is live)" || { echo "FAIL yaml_h at-sign control did not fire — grep may be broken"; FAILS=$((FAILS+1)); }
ck test_h 'RECIPIENT_LOOKUP_FAILED' 1
# ---- the tamper table's discriminator anchor: 8 it( heads + it.each tables = 16 cells ----
itcount="$(/usr/bin/grep -c -F -- 'it(' "$W/test_h")"
echo "  test_h 'it(' occurrences: $itcount (informational — the 16-cell count also depends on it.each tables)"
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
