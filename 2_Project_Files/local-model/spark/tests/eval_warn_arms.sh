#!/bin/bash
# eval_warn_arms.sh — arms for the 2026-10-26 round.sh fix: a lint WARNING (backticks/apostrophes) must not reach eval.
# Run: /bin/bash <abs>/eval_warn_arms.sh  (SPARK_TEST_TMP optional). No model call; closed local port; no cd.
set -uo pipefail
SPARK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; LM="$(dirname "$SPARK")"
REAL="$LM/night/briefs/ks_1391_p1"
T="${SPARK_TEST_TMP:-$(mktemp -d "${TMPDIR:-/tmp}/ew_arms.XXXXXX")}"; mkdir -p "$T"
export SPARK_URL="http://127.0.0.1:9"
python3 - "$REAL" "$T" <<'PY'
import os, re, sys
real, t = sys.argv[1:3]
b = open(os.path.join(real, "KS-1391.md"), encoding="utf-8").read()
pins = open(os.path.join(real, "spark.pins"), encoding="utf-8").read()
g = open(os.path.join(real, "golden.diff"), encoding="utf-8").read()
def mk(n, text):
    d = os.path.join(t, n); os.makedirs(d, exist_ok=True)
    for f, c in (("KS-1391.md", text), ("spark.pins", pins), ("golden.diff", g)):
        open(os.path.join(d, f), "w", encoding="utf-8").write(c)
# a: drop the File: line inside ## The test -> WARNING TEST PATH (contains backticks and an apostrophe-free quote; add one)
a = re.sub(r"(?m)^(##+\s*The test\b.*\n\n)File: `[^`]+`\n", r"\1", b)
assert a != b
mk("a_warn", a)
# b: names another client -> REFUSED
mk("b_refuse", b.replace("Secuura only.", "Secuura only. Client: Datasec", 1))
PY
a=$(/bin/bash "$SPARK/round.sh" "$T/a_warn" --dry-run 2>&1); arc=$?
echo "$a" | /usr/bin/grep -i 'lint:\|SPARK ROUND\|unbound' | cut -c1-230
[ "$arc" -eq 0 ] && ! echo "$a" | /usr/bin/grep -qi 'unbound variable' && echo "$a" | /usr/bin/grep -q 'lint: WARNING' && echo "ARM PASS (a) warning with backticks does not crash, rc=0" || echo "ARM FAIL (a) rc=$arc"
b=$(/bin/bash "$SPARK/round.sh" "$T/b_refuse" --dry-run 2>&1); brc=$?
echo "$b" | /usr/bin/grep 'SPARK ROUND' | cut -c1-230
[ "$brc" -eq 2 ] && echo "$b" | /usr/bin/grep -q 'REFUSED' && echo "ARM PASS (b) refused rc=2" || echo "ARM FAIL (b) rc=$brc"
c=$(/bin/bash "$SPARK/round.sh" "$REAL" --dry-run 2>&1); crc=$?
echo "$c" | /usr/bin/grep 'SPARK ROUND' | cut -c1-230
[ "$crc" -eq 0 ] && echo "$c" | /usr/bin/grep -q 'DRY-RUN OK' && echo "ARM PASS (c) ks_1391_p1 dry-run OK rc=0" || echo "ARM FAIL (c) rc=$crc"
