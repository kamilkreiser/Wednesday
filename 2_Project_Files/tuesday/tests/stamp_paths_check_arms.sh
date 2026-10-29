#!/bin/bash
# Arms for tuesday/tools/stamp_paths_check.py (GET-only against GitHub; needs the HPSM-POC gh config).
# RED  1: the B884 pre-stamp kit at HPSM-POC c00e2828 -> rc 1 and exactly one WRONG-DIR, AppShellFeedback.test.tsx
#         (the 2026-10-29 10:26 T04 stamp: the tree has it under components/feedback/, the kit said components/shell/).
# GREEN 1: the same kit with that one path corrected -> rc 0.
# RED  2: a synthetic line pointer past EOF (web/src/components/shell/NextStep.tsx:9999) -> rc 1, LINE-PAST-EOF.
set -u
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
C="$DIR/../tools/stamp_paths_check.py"
K="$DIR/../briefs/2026-10-29_B884_SEAT-R82_hpsmpoc-records-v12-design-tickets.md.pre-stamp"
H='/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config'
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fail=0
out=$(python3 -I "$C" "$K" datasecau/HPSM-POC c00e2828 --gh-config "$H"); rc=$?
n=$(printf '%s\n' "$out" | /usr/bin/grep -i -c '^WRONG-DIR.*AppShellFeedback.test.tsx')
all=$(printf '%s\n' "$out" | /usr/bin/grep -i -c '^WRONG-DIR\|^LINE-PAST\|^AMBIG\|^MISSING-LOCAL')
[ "$rc" = 1 ] && [ "$n" = 1 ] && [ "$all" = 1 ] && echo "RED 1 ok (rc 1, the T04 path, 1 failure)" || { echo "RED 1 FAIL rc=$rc n=$n all=$all"; fail=1; }
sed 's#AppShellFeedback.test.tsx; hosted#feedback/AppShellFeedback.test.tsx; hosted#' "$K" > "$TMP/fixed.md"
python3 -I "$C" "$TMP/fixed.md" datasecau/HPSM-POC c00e2828 --gh-config "$H" >/dev/null; rc=$?
[ "$rc" = 0 ] && echo "GREEN 1 ok (rc 0)" || { echo "GREEN 1 FAIL rc=$rc"; fail=1; }
printf -- '- see `web/src/components/shell/NextStep.tsx:9999`\n' > "$TMP/eof.md"
out=$(python3 -I "$C" "$TMP/eof.md" datasecau/HPSM-POC c00e2828 --gh-config "$H"); rc=$?
[ "$rc" = 1 ] && printf '%s\n' "$out" | /usr/bin/grep -i -q '^LINE-PAST-EOF' && echo "RED 2 ok (LINE-PAST-EOF)" || { echo "RED 2 FAIL rc=$rc"; fail=1; }
exit $fail
