## BLUF

You are **Seat R 53rd** on Secuura Platform K (lane Secuura/Blockchain-R, the RAISE lane; R 52nd wrapped at 05:51Z with nothing open, handover `5_Project_History/2026-10-19_seatR-52nd/HANDOVER.md`, read it first, especially §D and §F). **Raise four held Spark passes as THREE PRs, read every READY at source before applying it, then READY FOR GATE per PR.** All four were read at source by Wednesday and held with hold_ready.py at develop 722e07f19cee. Send a plan confirmation before your first write.

## QUEUE

1. **KS-1645 item 3 only** (Backlog, priority 2, 0 comments): `night/READY_KS-1645-AUDITTYPE-1_spark-dsv4flash_BRIEFED-CODEPATCH-AUDIT-EXPORT-PASS-7of7_2026-10-19.diff.md` (all four in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/`). api-gateway `routes/audit-export.ts`: `type` validated against a runtime list, 400 BAD_REQUEST for unknown or repeated, + a new vitest file. Partial: items 1, 2, 4 of KS-1645 stay open; say so (Refs, never Closes). Tier 1 (an admin route that only refuses more). Note KS-1645 is "repair before this export is deployed": this PR is one of four repairs.
2. **KS-1642, both pieces in ONE PR** (Backlog, priority 4, 0 comments): `READY_KS-1642-READPROBE-1_...` (originate `utils/idNamespaceCollision.ts` one up-front read probe + a reason comment + a new jest file) THEN `READY_KS-1642-H9PIN-2_...` (test-only, RED H9 + CONTROL H9c in the existing `ks1612-409-mapping-survives-the-prisma-error-shape.test.ts`). **Sequencing:** with p1 applied, p2's tamper target moves from `:84` to `:87`; re-read the line and re-prove p2's red against it. Tier 2.
3. **KS-1634 v2 site** (In Progress, priority 2, 5 comments, last 2026-10-19T05:20Z): `READY_KS-1634-V2SIMULATED-1_...` (originate `routes/verificationV2.ts` chainOnlyMatch carries `simulated: chain.simulated`, + a new jest file). **Add Stuart's S-shaped cell by hand** (Wednesday's triage, row 3): a bare `POST /api/anchors` under a connector key with a fresh v4 `documentId` (no documents row), then verified through the gateway, asserting the reply is labelled simulated/off-chain, not on-chain. Test file only: do not edit anchoring `src/index.ts` (Seat J 14th's file). If the cell cannot be built in-process, STOP and mail me what it would need. Tier 1. `Refs KS-1634`.
4. Per PR: READY FOR GATE (cause, the cells, suite counts at the landing parent, files, predicted landing tree on live develop). One BLUF comment per ticket after its PR is raised.

## PARTITION

Yours: api-gateway `src/routes/audit-export.ts`; originate `src/utils/idNamespaceCollision.ts`, `src/routes/verificationV2.ts`; and the tests named above (new files plus the ks1612 jest file). Say so before touching any other file. **NOT yours, live right now:** Seat E 3rd (Secuura/Blockchain-E): api-gateway `routes/platform.ts` (#1613 at its delta gate). Seat C 25th (Secuura/Blockchain-C): originate `routes/documents.ts`, `documentRepo.ts`, `gatewayProvenance.ts`, a new migration 052. Seat J 14th (Secuura/Blockchain-J): anchoring `src/index.ts`, `anchorOverwriteGuard.ts`, originate `routes/anchors.ts`. Seat G 10th (Secuura/Blockchain-G): originate `routes/certifications.ts` and the ks1557 suite. **You share an inbox with all of them: a brief or ANSWER naming another seat is not yours.** Identify yourself by your pane's cockpit name. KS-1622 stays parked until E's #1613 merges (same file); your handover note on its four shapes carries over.

## HOLDS

- **A fresh clone has NO pre-push gate.** Before any push, in your clone: `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`, then `git config --get core.hooksPath` read back in your plan confirmation (Seat E 3rd's catch, KS-1646).
- **Identity:** set `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai` LOCALLY before the first commit; read back `git config --show-origin user.email`.
- **Pushing:** `.githooks/pre-push:352-358` refuses a push whose tip is not the checked-out HEAD; `:76-80` refuses a non-fast-forward push. Never `--no-verify`; never `ALLOW_FORCE` without a mail from me naming it. Transport in full: `-c core.sshCommand='<the repo's ssh command> -o ServerAliveInterval=30'`.
- Merge only on Wednesday's head-pinned GO after a gate verdict. No deploy. Ticket comments are the only client-facing channel.
- No Docker on this Studio. Rotate inside your 80-90 band at a clean boundary; handover first.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- None for these tickets.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- KS-1641 p1 is NOT in this queue (its hold was refused on a checker accommodation; a rebrief is owed by Wednesday).
- KS-1634's S-shaped cell is hand-written by you in the same PR as the v2 site.

PROVENANCE:
- KS-1645, KS-1642, KS-1634 state, priority, comment counts (as quoted inline) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- the four READY files and their product hunks | Wednesday's hold_ready.py output and source read, /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-18_spark-screen/SCREEN_13.md | read 2026-10-19
- develop 722e07f19cee | git ls-remote origin + Wednesday's own fetch | read 2026-10-19
- pre-push refusals | your own .githooks/pre-push at 846ae2788b3b lines 76-80 and 352-358, read by Wednesday | read 2026-10-19
- Stuart's S-shaped cell | Wednesday's triage 0_Brain/reference/2026-10-19_stuart-list-triage/TRIAGE.md row 3 (my project, not yours) | read 2026-10-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-19 17:20
