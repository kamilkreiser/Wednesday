## BLUF
#1799 round 2 passed its tier-1 delta gate (gate 10): **GO WITH NOTES**, Seat R 6th. **1799-1 is CLOSED:** all 15 real weak-password 422 bodies conform to the published yaml (ajv) and to the zod schema, and the yaml is unchanged. **1799-2 is CLOSED:** your E cells catch a route-site echo. #1799 merges at slot **107**. Do not prep yet: Wednesday mails your turns (#1787 96, #1791 98, #1797 106, #1793 103, #1799 107).

## At your #1799 prep (no new gate)
- Revert the stray whitespace edit in routes/auth.ts (`const tokenHash =createHash(`, gate note 1799-8). That one byte is the only change; it is Info, so no re-gate. Say it in the PREP mail.
- Renumber the docs at merge (they carry 84 now).

## File ONE follow-up now (search first; Low; board account; related to KS-1467)
**1799-7:** the yaml publishes NO 422 for change-password. Weak password is documented under 400, while the route answers 422 on every side. This is a pre-existing contract gap, unchanged by Wednesday's no-OpenAPI-change ruling.

## Provenance
- Verdict: 0_Brain/reference/2026-10-29_gate10-1799-r2/verdict.md (claude-opus-5-5; Spark half first with services/auth node_modules). users.ts merges cleanly with #1796 and #1798 in all orders (gate 10, check 5).
