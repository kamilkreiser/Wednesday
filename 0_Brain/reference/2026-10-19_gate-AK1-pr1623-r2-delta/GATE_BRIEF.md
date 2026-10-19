# Gate brief: GATE AK1 = PR #1623 (KS-1633) DELTA, Opus, tier 1, round 2 of 2 (THE CAP)

Commissioned by Wednesday after Seat G 11th's READY FOR DELTA GATE (10:50Z). The author's CLAIM is beside this brief: `G11_READY_DELTA_1050Z.txt` (read it WHOLE). Round 1's brief and verdict (gate AI1, NO GO, 1 blocker, 9 notes) are in `../2026-10-19_gate-AI1-pr1623-ks1633/`: read `verdict.md` there WHOLE first. Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/ak1/`. Run every npm/vitest/jest command with `--prefix`/`--root` pointing INTO that clone, never from your cwd (a previous gate's `npm exec` ran in Wednesday's tree). Build `packages/shared` first; Prisma via `npm run generate --workspace=services/originate`. Scratch PostgreSQL on a port in 55440-55449, TCP only, `docker/init/*` + every migration.

**Heads:** #1623 head `ea9d6e697951ef5c78628055429f345486955bcd` (round 1 was `b7de864640032c3b118c5aaa9e4e45b777ef67af`); develop `a0da739b6954d42333640ea190d877f031803c7f`. Re-read at start and before the verdict. Predicted landing tree `e598e00e890284ae6b85a9fe0379eac3c28a72ca`.

**Rulings it implements (Wednesday's, inside KS-1633):** (a-prime) = the pre-anchor write is a NON-DECIDING, event-free reservation (`reserveCertificationRow`); a reservation failure is logged and the request continues to the anchor call, so every response equals develop's; the authoritative `saveCertification` writes the row and exactly ONE ISSUE event; both share one private `insertCertificationRow`. Kam's card `secuura-ks1124-f4-failed-anchor-shows-pending` = b must still hold (a failed anchoring stores 'failed').

**Round 2 of 2:** a NO GO ships nothing and the residue is ticketed. Be exact about what blocks.

## Questions (each with its instrument; name what you did NOT run)
1. **B1 closed?** Re-run AI1's C11 (NUL), C12 (connector principal), C13p (save throws) in production mode with anchoring unavailable, both tenancy modes, through the real router as `secuura_app`: 503 byte-identical to develop. Then sweep EVERY path (success, non-production failure, validation and access refusals incl. KS-1557's parent check, anchoring up + reservation failing) for status + body equal to develop. Any difference is a blocker.
2. **N1:** exactly one ISSUE event per accepted AND per failed certification, equal to develop's count, and its details equal develop's.
3. **The shared insert:** one `INSERT INTO documents` in certificationRepo; `saveCertification`'s SQL and parameters byte-equal to develop's for the same input (diff the statement text and the parameter list); the 210 save-count cells and F4-2 green.
4. **N4 (pool):** read the change to `withTenant`: optional pool, omitted = develop behaviour; the route passes the request's pool on BOTH the reservation and the compensating delete. Plant a mutant (route passes nothing) and confirm the unit cell reds. You cannot run a second tenant database unless you can; say which.
5. **N3, N5, ORPHAN (narrowed), ORDER, DELETE-FAILS:** each red on its named mutant or against develop as claimed; plant one of your own on the reservation's non-deciding wrapper.
6. **Delta discipline:** diff round 1 head -> round 2 head; every changed file and hunk accounted for by a note or the blocker fix.
7. **Landing:** merge-tree on LIVE develop; originate full unit suite on the landing tree; ks1633 (claim 10/10) + ks1557 + ks1538-int in both modes; a type-check that includes test files; the three-dot list = the PR's 8 files. List every touched service's integration suites as RUN or NOT tested.

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head ea9d6e697951... (tier 1 delta, round 2 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:** findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`, nothing in `/Volumes/DevMASTER/WEDNESDAY` except this verdict file, no push. No `cd`, no `rm`, no stderr to /dev/null, no Docker. Every zero gets a positive control. zsh: no PIPESTATUS.
