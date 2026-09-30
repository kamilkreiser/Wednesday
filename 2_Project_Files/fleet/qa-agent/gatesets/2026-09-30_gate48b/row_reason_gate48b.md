# gate48b — #1354's PERMANENT GHSA-r53p row: its `reason`, VERBATIM, split into sentences for ROW-PERMANENT-FIELDS

Read 2026-09-30T02:02:48Z by baseline_gate48b.py: `git show 88802586cebe35855983f7639b5e18069fe11e13:Blockchain/Dev/scripts/audit/audit-baseline.json`, row `GHSA-r53p-7pc4-xj5r`. reason sha256 05a996e94ff7c780ceff0bc83dcb5a0cf241d728ca472714ae45d4ba3542226a, 1794 chars, 10 sentence(s). The split is at `. ` / `; ` before a letter; the gate checks EVERY factual sentence as a row (claim · instrument + tree/image · TRUE / FALSE / UNMEASURED / TRUE-BUT-CONDITIONAL). The drafter checked NONE. It is a PUBLISHED record and it is now PERMANENT: every later triage reads it.

1. Re-measured 2026-09-30 for this advisory (published 2026-09-29;
2. first patched 6.28.1 for the < 6.28.1 range).
3. The pin is undici 5.29.0, a production entry reached only via frontend/issuer -> @meshsdk/core -> @meshsdk/provider -> @utxorpc/sdk -> @connectrpc/connect-node (which declares undici ^5.28.3), in the frontend/issuer lock and in the workspace-root lock through the frontend/issuer workspace member.
4. It is installed in the issuer image's builder stage (npm ci of frontend/issuer's lock) and is not in the served image: measured from the artefact built from this tree, the final nginx stage copies only /app/dist/, has zero node_modules directories anywhere, and undici, connectrpc, connect-node and undici's own error-code literal UND_ERR_ each occur 0 times in the 58 served files, with controls react (27), secuura (8, case-insensitive) and an issuer source string firing in the same grep.
5. undici is pinned in none of the 25 services/* standalone locks (all 45 tracked locks parsed, 14924 package entries);
6. its only other pin is mobile/secuura-app's 6.28.0 via @expo/cli, out of scope under KS 769 and not measured here.
7. No Dockerfile copies the workspace-root lock, so the root lock's entry reaches no image.
8. No patched version exists inside ^5.28.3 (the newest 5.x on the registry is 5.29.0), so a lock bump cannot close this; 7.30.0 lies outside the ranges of this advisory and of all 12 sibling undici rows, and an unscoped overrides entry sized 2026-09-30 in a scratch regen resolved 7.30.0 (723->721 entries), with its build and suites UNMEASURED.
9. Accepted permanently on Kam Kreiser's ruling (card secuura-undici-ghsa-r53p-exception-1354, 2026-09-30);
10. the vulnerable version is removed by the undici override fix, PR #1355 (KS 1378), after which this row is no longer reported.
