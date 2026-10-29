#!/bin/bash
# Arms for tuesday/tools/pr_body_facts.py (GET-only against GitHub; needs the Composer and HPSM-POC gh configs).
# Each arm is a 2026-10-29 PR-body claim a gate caught; the tool's output must CONTRADICT the claim and state the truth.
# ARM 1 Composer #104 (c63c3867...e10fa812): body said "after line 28 / 276" -> output names old lines 30 and 278, not 28/276.
# ARM 2 Composer #103 (c63c3867...2b288a6): body said "lines 218-239"      -> output names new lines 223-244.
# ARM 3 HPSM-POC #241 (c00e2828...59625e5f): body said "eight new test files" -> output counts 9 added test + 1 spec.
# ARM 4 synthetic: a zero-count hunk (-30,0) and a trailing blank line -> "after old line 30", "-1 old lines 41".
set -u
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
P="$DIR/../tools/pr_body_facts.py"
D='/Volumes/Laptop-DEV/!CODING/Datasec'
C="$D/Datasec Security Composer/4_Credentials/.gh-config"
H="$D/HPSM-POC/4_Credentials/.gh-config"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fail=0
out=$(python3 -I "$P" datasecau/Datasec-Security-Composer c63c3867 e10fa812 --gh-config "$C")
printf '%s\n' "$out" | /usr/bin/grep -i -q 'after old line 30)' && printf '%s\n' "$out" | /usr/bin/grep -i -q 'after old line 278)' \
  && ! printf '%s\n' "$out" | /usr/bin/grep -i -q 'old line 28)\|old line 276)' && echo "ARM 1 ok (30 and 278)" || { echo "ARM 1 FAIL"; fail=1; }
out=$(python3 -I "$P" datasecau/Datasec-Security-Composer c63c3867 2b288a6 --gh-config "$C")
printf '%s\n' "$out" | /usr/bin/grep -i -q 'new lines 223-244' && echo "ARM 2 ok (223-244)" || { echo "ARM 2 FAIL"; fail=1; }
out=$(python3 -I "$P" datasecau/HPSM-POC c00e2828 59625e5f --gh-config "$H")
printf '%s\n' "$out" | /usr/bin/grep -i -q '^  added: 12 (2 product, 1 spec, 9 test)$' && echo "ARM 3 ok (9 test + 1 spec)" || { echo "ARM 3 FAIL"; fail=1; }
printf '%s\n' '@@ -30,0 +31,6 @@' '+a' '+b' '@@ -40,2 +46,2 @@' ' x' '-y' '+z' > "$TMP/p.txt"
out=$(python3 -I -c "
import importlib.util,sys
s=importlib.util.spec_from_file_location('f',sys.argv[1]); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
[print(m.describe(r)) for r in m.runs(open(sys.argv[2]).read())]" "$P" "$TMP/p.txt")
printf '%s\n' "$out" | /usr/bin/grep -i -q 'inserted after old line 30)' && printf '%s\n' "$out" | /usr/bin/grep -i -q 'replacing -1 old lines 41$' \
  && echo "ARM 4 ok (zero-count hunk, trailing blank)" || { echo "ARM 4 FAIL: $out"; fail=1; }
exit $fail
