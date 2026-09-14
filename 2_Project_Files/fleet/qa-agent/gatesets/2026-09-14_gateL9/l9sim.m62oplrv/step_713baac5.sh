set -uo pipefail
out=$(npm run audit:contract --silent 2>&1); rc=$?
printf '%s\n' "$out"
if [ "$rc" -ne 0 ]; then echo "audit-contract suites are red"; exit 1; fi
cases=$(printf '%s\n' "$out" | grep -oE ' tests [0-9]+' | tail -1 | grep -oE '[0-9]+')
expected=$(tr -d '[:space:]' < scripts/audit/expected-case-count)
if [ -z "$expected" ]; then echo "expected-case-count missing or empty"; exit 1; fi
if [ -z "$cases" ]; then echo "no case count reported — a run of zero cases is not a pass"; exit 1; fi
if [ "$cases" -ne "$expected" ]; then
  echo "ran $cases cases, expected $expected — fewer means cases were lost; more means update scripts/audit/expected-case-count"
  exit 1
fi
echo "OK — $cases audit-contract cases pass (expected $expected)"
