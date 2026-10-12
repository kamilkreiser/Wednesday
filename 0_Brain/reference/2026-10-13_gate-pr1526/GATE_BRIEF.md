# Gate brief: Secuura Platform K PR #1526 (ticket KS-1355 spots 2b, 3, 4), SONNET tier 2

Commissioned 2026-10-13 ~06:4x AEDT by the Wednesday seat.

## What you are gating
- Head `f0278d3b267b7a09374690810a6a578b71e87b57` (Wednesday's ls-remote). Base: K's commit 87b4e0df7 plus develop 69878dc5 merged in; develop is now `81ac1ea60ec684f1636a25832d9a7f3bf28470f5` (KS-1521, governance/staking/transfer tests only). Author Seat K 8th.
- Change (local-dev stack tooling; docker-compose.yml is ALSO the file the Kintsugi/demo boxes run):
  - docker-compose.yml ~:503 (api-gateway CORS_ORIGINS), ~:767 (auth FRONTEND_URL), ~:2185 (demo-service CORS_ORIGINS): slot-1 literals become defaults derived from GATEWAY_PORT / WEBSITE_PORT.
  - env.example:146 CORS_ORIGINS commented out with a pointer.
  - scripts/preflight/preflight.sh:94: derive the gateway when a slot is named; keep :6882 and print one line when unnamed; refuse only a malformed slot; an explicit GATEWAY_URL still wins.
  - scripts/start-local.sh: sources stack_env.sh (after .env), Compose v1 -> v2.
  - scripts/check-stack-safety.sh: rule for scripts that run the PLATFORM compose with up/run/restart/down, named exception list (reason + ticket each, KS-1550), a census cell that reds a new unlisted launcher; plus a NARROW point-1 literal-port guard (scope stated, KS-1381 widens it later).
  - scripts/check-compose-stack-safety.mjs: new render invariants.
  - New tests: preflight_gateway_slot.test.sh, ks1355_slot_blind_launchers.test.sh; ks1417 suite extended.
- Author's numbers (NOT evidence): compose invariants 18 -> 25; check-stack-safety 100 -> 105; new suites 15/0 and 14/0; ks1417 10/0; tamper 16/16; hook "shell suites: 85 passed"; unslotted = slot-1 = base render sha256 2daa06e430f2e651 (four ownership labels held). Artefacts: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-13_seatK-8th/ks1355/RENDER-PROOF.md` and `.../tampers/TAMPER-TABLE-ks1355.md`. Legs 3, 4, 8 (the gateway-dependent ones) did NOT run.

## How to get the code (READ-ONLY on the project)
- `git clone --shared` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` into YOUR scratchpad; fetch `refs/pull/1526/head` and develop with the project's `core.sshCommand`. Assert the head. `docker compose config` renders need no daemon. No pushes, no GitHub/Linear writes, no remote boxes, never start or stop any real stack.

## What to check
1. Render proof yourself: base vs head, unslotted and slot 1 with the four ownership labels held: byte-identical? Slots 2-4: FRONTEND_URL and both CORS_ORIGINS carry that slot's ports and not slot 1's. An explicit .env value still wins; an explicitly EMPTY value falls back to the derived default (is that what the code does, and is it safe).
2. A BOX: with GATEWAY_PORT/WEBSITE_PORT UNSET and FRONTEND_URL/CORS_ORIGINS unset, the head renders exactly the base's values (that is what a box with no such keys in its .env would get). Say plainly what changes for a box whose .env sets GATEWAY_PORT to a non-6882 value but not FRONTEND_URL/CORS_ORIGINS.
3. preflight.sh: run its new unit suite; drive slot unset / 1-4 / malformed / GATEWAY_URL set; confirm the pre-push hook path (.githooks/pre-push ~:282 sourcing systemTest/slot-target.sh) takes the explicit-GATEWAY_URL branch.
4. start-local.sh: sourcing order (.env then stack_env), no remaining `docker-compose ` v1 token, nothing else changed in behaviour for slot 1.
5. The two guards: plant a new literal slot port in a file inside the narrow scope -> red; plant one outside the scope -> green (narrow by design); plant a new launcher running the platform compose without sourcing stack_env -> red; each exception entry has a reason and a ticket.
6. Kill at least three tampers yourself (revert a compose line; revert the preflight derivation; drop the start-local source).
7. The whole tracked shell-suite runner once at the head.

## Output
- `0_Brain/reference/2026-10-13_gate-pr1526/verdict.md` (this folder only, plus your scratchpad; raw outputs under `evidence/`, never a directory named `out`). Head under test; numbers with instruments and controls; FOUND / TESTED / HOW; NOT tested.
- VERDICT: GO / GO WITH NOTE / NO GO; Majors and Minors with file:line and the reproducing shape.
