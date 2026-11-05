# Gate 203 commission — Secuura / Blockchain, KS-1666 (b, c, e + (a) A-prime), LOCAL SHA (no PR yet), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 19:2x AEDT. Model: Opus (tier 1: it changes what is STORED on a failure path — a compensating delete). QA GATE: findings only; fix nothing; write nothing outside this folder; no box; post nothing to Linear or GitHub.
Write `verdict.md` here EARLY as a stub (line 1 `NO GO (INCOMPLETE: killed before the verdict)`), overwrite at the end. Final line 1 is exactly `GO`, `GO WITH NOTES` or `NO GO (<reason>)`.
Read first, whole: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md; then `status_ks1666.txt` here (Seat V 21st's mail, verbatim). Never `cd`; never a recursive grep/find over 0_Brain/reference, local-model/ or 5_Project_History.

## Subject — a LOCAL SHA (read it by SHA)
`4d1c96b495bd46936eed010ca1c72c0b69d79553`, ONE commit whose parent is develop-at-build `5fc5569ed96ac61f64823cc9e1fa841899aa1f62` (Wednesday: cat-file commit; rev-parse ^ = 5fc5569ed96a; diff stat 7 files +452/-14; 19:24). Get it read-only: `git clone --shared /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files <your subfolder>` then `git -C <subfolder> checkout --detach 4d1c96b495bd...`. Develop NOW = `8c5da776eccf3a4361d64ca3d44f83420ef7dd60`.

## Wednesday's rulings you check against (binding)
- (a) = A-PRIME: when the reservation landed (provisionalWritten) and the authoritative save throws: delete the reserved row ONLY if NO anchor was created (anchoringStatus 'failed', upstreamAnchorId null), with exactly the 503 path's delete (same pool, count check, error line); the ORIGINAL failure is answered unchanged; if the delete itself throws, its error line is logged and the original failure is still answered (never masked). When anchoring was ACCEPTED, the row is KEPT (RED ORPHAN invariant, ks1633 integration test :246-260, must hold). Inherited 10 s client-timeout window: accepted, must not be widened.
- (f) = not built (KS-2008 filed for the class). (b) two pool-mutant cells, (c) provisionalWritten cell, (e) header/title wording only.
- One extra line in ks1293-originate-suite-is-hermetic.test.ts's manifest: accepted (the suite requires it).

## Questions
1. Scope: exactly 7 files; certifications.ts changes only the move of the 503 delete into a shared local function + the new call on the failed-save path. The 503 path's behaviour is byte-for-byte unchanged (status, body, delete, logs) — base vs head cells.
2. A-prime decision table, base vs head, on the real route with only db/anchoring doubled: {reservation landed?} x {anchor accepted / failed / anchoring not called} x {save ok / throws ordinary Error / throws unreadable value} x {delete ok / delete throws / delete counts 0}. For each: rows left, response status/body, logs. Head deletes ONLY when no anchor exists; never deletes when an anchor was accepted; the original failure answer is identical to base in every cell. "N of M".
3. Tenant/pool: the delete runs in the same request pool and tenant scope as the reservation (b's mutants: no pool passed; withTenant ignores the pool) — reproduce both and one tamper of your own.
4. RED ORPHAN: you cannot run Postgres-backed integration cells unless you can stand one up in your folder; if you cannot, read the cell and the code path and state the invariant holds by reading, as UNMEASURED-at-runtime.
5. Suites: originate jest suite (classify failures vs base; note the seat's ks1868/ks1943 TS2451 `mockH` worker-order flake), tsc, eslint, docs-fragments with a planted defect.
6. Merge tree onto develop 8c5da776eccf: rc and tree; shared paths with everything merged since 5fc5569ed96a (PR 2007, 2010, 2011) = 0, planted control.
7. (e) is comment/title only: comment-stripped transpile diff = only the title line.

## Output
`verdict.md` (verdict line, BLUF, findings with severity, file:line, evidence path). Final message: verdict line + one line per finding.
