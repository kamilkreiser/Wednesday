# Gate brief: Secuura Platform K PR #1528 (tickets KS-865, KS-1347, KS-1137 F-4), SONNET narrow (tooling + tests)

Commissioned 2026-10-13 ~07:0x AEDT by the Wednesday seat. Tier: through code, narrow (tooling and tests; one dev-only capture proxy path expression). Author Seat K 8th.

## What you are gating
- Head `6bfd74ad7c39b43c614c5d837744780f20788fa2`, base develop `81ac1ea60ec684f1636a25832d9a7f3bf28470f5` (Wednesday's ls-remote; unmoved, no merge-in). 7 files, +268/-5.
- KS-865: the checker's HEADER advertised six files while its list reads five; header corrected.
- KS-1347: `scripts/openapi-examples/proxy/server.ts:31` replaced `new URL(import.meta.url).pathname` with the fileURLToPath form; the author says the auth half was already fixed and the only remaining tree-wide site is systemTest/playwright/global-setup.ts:42 (KS-1337's by design).
- KS-1137 F-4: the `command -v jq` check on the OUTER PATH vs the job running on a private PATH: fixed in THREE sibling suites (the ticket named one), wider than the ticket on purpose.
- Author's claims (NOT evidence): tamper table 7/7; mutant u4 (delete the node:url import from server.ts) first SURVIVED because the probe hard-coded the import; the probe now inherits the subject's own node: imports and u4 bites.

## How to get the code (READ-ONLY on the project)
- `git clone --shared` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` into YOUR scratchpad; fetch `refs/pull/1528/head` with the project's `core.sshCommand`. Assert the head. No pushes, no GitHub/Linear writes, no remote boxes.

## Narrow scope
1. Re-derive u4 yourself: delete the import from server.ts -> the KS-1347 cell must go red; restore -> green. Also run server.ts's module once (or its import path) to prove the real file would fail without the import.
2. KS-1137 F-4 in all three suites: put jq only on the private PATH / only on the outer PATH and show each suite now reports correctly (no false pass, no false refusal). Confirm the three sites are the full set (census by the pattern, with a control).
3. KS-865: the header now matches the list exactly.
4. Check the author's "already done" claims for KS-865, KS-1347 and KS-1137 F-2 at develop by reading the code (stale-ticket claims become ticket closures).
5. The full tracked shell-suite runner once at the head (say plainly if your clone lacks npm installs and which suites that affects).

## Output
- `0_Brain/reference/2026-10-13_gate-pr1528/verdict.md` (this folder only, plus your scratchpad; raw outputs under `evidence/`, never a directory named `out`). Head under test; numbers with instruments and controls; FOUND / TESTED / HOW; NOT tested.
- VERDICT: GO / GO WITH NOTE / NO GO; Majors and Minors with file:line.
