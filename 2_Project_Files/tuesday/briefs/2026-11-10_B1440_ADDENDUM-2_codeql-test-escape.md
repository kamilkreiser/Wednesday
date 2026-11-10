From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-2 to your kit B1440 (SEAT-H150). Every rule of your kit still binds you. HARD STOP stays 15:30 AEDT. This is NOT a gate round: gate B1440-2 read GO WITH FINDINGS @ fc90f07; hosted CodeQL on pull request 304 then raised 2 new HIGH alerts in your test code. CodeQL is never bypassed or dismissed, so they are fixed.

## The alerts (read by Tuesday from GitHub code scanning on refs/pull/304/head)
- #16 and #17, rule `js/incomplete-sanitization` (high), both at `web/src/components/partner/PartnerDashboard.alias.test.tsx:50`: "This does not escape backslash characters in the input."
- Line 50 builds `new RegExp(\`${NAME_A.replace(/[()]/g, "\\$&")}|${NAME_B.replace(/[()]/g, "\\$&")}\`)`: only `(` and `)` are escaped.

## The fix (ONE forward commit, test file only)
- In that test file only: stop hand-escaping. Either (preferred) match by text without a regular expression, e.g. a matcher function over `textContent` that checks `includes(NAME_A) || includes(NAME_B)`, or escape every RegExp metacharacter including the backslash with one helper (`s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")`). Re-scan the WHOLE branch diff for the same pattern (`/usr/bin/grep -rn -E 'replace\(/\[' ` over your added test lines, with a positive control on line 50 before the fix) and fix every other instance the same way.
- No product file changes. No new words.

## Prove it (under `## ADDENDUM-2` in STATUS)
- `git diff fc90f07 HEAD --stat`: test file(s) only.
- The changed test file(s) pass at your head; the row it pins still fails when the alias fix is reverted in a copy (the row's purpose is unchanged).
- Full `npm test` count equal to the gate's (4216) or the difference explained; lint and typecheck rc 0.
- Plain-ASCII commit message, attribution line; plain push of `b1440/hpsmpoc-web-ui-rulings`.

**Last line:** `READY B1440-3: <head sha40>`, or `STOPPED: NEEDS TUESDAY <one question>`.
