# Gate brief: Secuura Platform K PR #1521 (KS-1533 arm 1), FIX ROUND 1 of 2 — OPUS DELTA gate

Commissioned 2026-10-13 ~05:5x AEDT by the Wednesday seat. Under the cap this is round 1 of 2 for this class.

## What you are gating
- Head `e4d7a13e8e20e57dbe92a9563266de2df495276b`; develop `b08ee6299e864bea2aff18f31bdd22281161c1db` (both Wednesday's ls-remote). Previous gated head `c02c0b5dcc22d3a59c7faa787b08a2871bfdafda`.
- Previous verdict (NO GO, M1 + m1..m3): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-13_gate-pr1521/verdict.md` and its `evidence/`. READ IT FIRST and re-use its harness (the role x target x connectorId x rotate matrix over real HTTP, the 16 smuggling shapes, register-connector's shapes).
- Delta per author V 5th: 113d2a91 (the fix + cells), a merge of develop b08ee629 (never rebased), e4d7a13e (comment only). index.ts +21/-2; the test file +65/-9.
- Claimed fix: M1: inside the connectorId block, `if (isProvisioner && data.rotate === true)` -> 403; a provisioner may still NAME a connectorId (no rotate -> 201). m1: the row stores normaliseOrgId(data.organizationId). The :248 cell replaced by three red-first cells plus a platform-role rotate control; tokens now carry exactly generateConnectorToken's claims.
- Author's numbers (NOT evidence): unfixed 4 red / 16 green, fixed 20/20; 16 of 17 mutants killed (survivor C4, the masked one); services/security 30 files / 331 tests; tsc, eslint clean.

## How to get the code (READ-ONLY on the project)
- `git clone --shared` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` into YOUR scratchpad (the project checkout is READ-ONLY); fetch `refs/pull/1521/head` and develop with the project's `core.sshCommand`, or use `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-12_seatV-5th/bundles/ks1533a-delta-c02c0b5d-to-e4d7a13e.bundle` (sha256/16 1f6983fe27ef502e, verified; needs c02c0b5d and 25059609). Assert the head first. No pushes, no GitHub/Linear writes, no remote boxes.

## Scope (delta)
1. Re-run the previous matrix at the new head, in-memory and Postgres storage: no non-platform caller retires another organisation's key, by any rotate shape (rotate true, "true", 1, nested, smuggled per the 16 shapes); platform roles still rotate; register-connector unchanged end to end.
2. m1: mixed-case/padded/blank organisation ids stored and listed consistently; the :1181 list filter agrees with what is stored; no existing row becomes unlisted (read the writers).
3. Kill R1 and S1 yourself on a green baseline; confirm C4 is still the only survivor and still masked.
4. The develop merge: the PR's files keep their blobs; nothing in develop's delta interacts.
5. The author's noted pre-existing item (index.ts:981-989 resolves the tenant from the RAW organisation id when none is sent): confirm it fails safe as stated, or report otherwise. Do not count it against this PR unless the PR made it worse.
6. Suites at the head: services/security, shared 949, tsc, eslint.

## Output
- `0_Brain/reference/2026-10-13_gate-pr1521-r1/verdict.md` (this folder only, plus your scratchpad). Head under test; numbers with instruments and controls; FOUND / TESTED / HOW; NOT tested.
- VERDICT: GO / GO WITH NOTE / NO GO; Majors and Minors with file:line and the reproducing shape.
