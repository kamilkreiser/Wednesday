#!/bin/bash
# controls_check.sh — re-grep every positive-control token of the #988 (KS-704) TIER-2 ROUND-1 brief at
# the pinned head 8cb99a002 and origin develop M38 0e78c7270 through the GitHub contents API (read-only;
# GH_TOKEN sourced by NAME from the Secuura .env, never printed). Tokens were derived from the PR's OWN
# files at these SHAs. PRESENT tokens must grep the stated count; ABSENT tokens must grep exactly 0; the
# blob table must hold; the fetched bytes must equal the set's model/ copies.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD="${QA988_HEAD:-8cb99a002c5177bb1418ee1fab7cd2974076989a}"
DEV="${QA988_DEVELOP:-0e78c7270188ac45c1c29f927bdf90728f10215d}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G="${QA988_SET:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate988}"
W="$(mktemp -d "${TMPDIR:-/tmp}/qa988ctl.XXXXXX")"
REPORT='systemTest/performance/gate/report.ts'; CLI='systemTest/performance/gate/cli.ts'
TESTF='systemTest/performance/tests/unit/gate/reportFailedGateBreakdown.test.ts'
DOC='systemTest/performance/docs/quick-start.md'

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
echo "controls_check.sh — #988 ${HEAD:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
# report_d/cli_d/doc_d are EXPECTED present (develop already has these files, this PR edits them);
# test_h is the only new file (absent at develop).
EXPECT_ABSENT='test_d'
for spec in "report_h:$REPORT:$HEAD" "report_d:$REPORT:$DEV" "cli_h:$CLI:$HEAD" "cli_d:$CLI:$DEV" \
            "test_h:$TESTF:$HEAD" "test_d:$TESTF:$DEV" "doc_h:$DOC:$HEAD" "doc_d:$DOC:$DEV"; do
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
blobis report_h 21d2dbe7d
blobis report_d b76b87a91
blobis cli_h c679e091b
blobis cli_d 4502e327c
blobis test_h 87171abf4
blobis doc_h dcdf76ad5
blobis doc_d 390b99722

cnt() { /usr/bin/grep -c -F -- "$2" "$W/$1"; }
ck() { local n="$1" tok="$2" want="$3"; local got; got="$(cnt "$n" "$tok")"; [ "$got" = "$want" ] && echo "ok   $n '$tok' = $want" || { echo "FAIL $n '$tok' = $got, want $want"; FAILS=$((FAILS+1)); }; }
# ---- report.ts anchors ----
ck report_h 'const STATUS_CODE_COUNTERS' 1; ck report_d 'const STATUS_CODE_COUNTERS' 0
ck report_h 'function isHttpRateGate' 1; ck report_d 'function isHttpRateGate' 0
ck report_h 'function formatStatusCodeBreakdown' 1; ck report_d 'function formatStatusCodeBreakdown' 0
ck report_h 'function printGateLines' 1; ck report_d 'function printGateLines' 0
ck report_h "if (name === 'http_req_failed')" 1; ck report_d "if (name === 'http_req_failed')" 0
ck report_h "metrics: K6Summary['metrics'] = {}" 1
ck report_h "['http_server_error', '[5xx]']" 1
ck report_h "['http_rate_limited', '[429/503]']" 1
ck report_h "['http_503', '[503]']" 1
# ---- the ONE cli.ts line ----
ck cli_h 'printReport(results, scenarioArg, scenarioCfg.blocking, summary.metrics);' 1
ck cli_d 'printReport(results, scenarioArg, scenarioCfg.blocking, summary.metrics);' 0
ck cli_d 'printReport(results, scenarioArg, scenarioCfg.blocking);' 1
ck cli_h 'printReport(results, scenarioArg, scenarioCfg.blocking);' 0
# ---- the new test file: 4 cells (anchor requires the 4-space test-body indent, since "split('"
# contains the bare substring "it('" once as a false hit) ----
ck test_h "    it('" 4
ck test_h 'http_server_error [5xx] passes=' 1
ck test_h "toContain('http_503 [503] absent')" 1
ck test_h "toContain('failed=0')" 1
ck test_h "toContain('ok=37')" 1
# ---- the doc sample block ----
ck doc_h 'status codes: http_server_error \[5xx\] passes=0 fails=8,453' 0
ck doc_h 'status codes: http_server_error [5xx] passes=0 fails=8,453' 1
ck doc_d 'status codes: http_server_error [5xx] passes=0 fails=8,453' 0
ck doc_h '**A failed HTTP rate gate carries a third line (KS-704)**' 1
ck doc_d '**A failed HTTP rate gate carries a third line (KS-704)**' 0

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
