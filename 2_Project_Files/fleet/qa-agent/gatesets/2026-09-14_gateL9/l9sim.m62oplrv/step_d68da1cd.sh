set -uo pipefail
node scripts/audit/audit-gate.mjs
rc=$?
case "$rc" in
  0) echo "OK — no advisories outside the triaged baseline" ;;
  2) echo "SKIP (advisory) — npm audit could not run (offline / registry unreachable)" ;;
  3) echo "FAIL — the audit gate REFUSED to report a verdict (see its line above)"; exit 1 ;;
  *) echo "FAIL — new or lapsed advisories; triage them (fix, or a reasoned baseline entry with a ticket)"; exit 1 ;;
esac
