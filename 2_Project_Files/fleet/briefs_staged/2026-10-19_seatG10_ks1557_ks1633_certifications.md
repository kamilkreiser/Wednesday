## BLUF

You are **Seat G 10th** on Secuura Platform K (lane Secuura/Blockchain-G, this round: originate certifications; history's newest G was 9th). Two tickets, in order: **KS-1557** (In Progress, priority 2, on the board account, 8 comments, last 2026-10-18T13:12Z): a write-role caller can make another organisation's bytes verify CERTIFIED under its own org. The read side merged in #1531 (`3a8713376`); **the write side is unbuilt**. Then **KS-1633** (Backlog, priority 3, unassigned, 0 comments): `POST /api/certifications/issue` anchors BEFORE it writes its documents row. Send a plan confirmation before your first write.

## QUEUE

1. **KS-1557 step 1, settle the multi-tenancy harness (read-only runs, no product change).** Stuart's words: the multi-tenancy harness mode "needs settling first or its evidence cannot be trusted". Read every KS-1557 comment (newest first), especially `28394c95` (2026-10-18, gate F1 note N4: the `:241` cross-tenant cell goes red under `MULTI_TENANCY_ENABLED=true` on untouched develop). Run the ks1557 and ks1119 suites as the `secuura_app` role in BOTH modes (`MULTI_TENANCY_ENABLED` true and false) on a scratch PG, and decide, with evidence, whether the `:241` red is a harness artefact or a real read-side defect. Mail me a STATUS with the matrix (suite x mode x result) and your verdict. **If it is a read-side defect, the fix is in originate `routes/verification.ts`, which is Seat R's file (#1597 at merge): STOP and mail me; do not touch it.**
2. **KS-1557 write side**, to Kam's ruling (b) of 13 Oct, delivered on the ticket as comment `c033e6fb` (read it: the caller may send its own hash). Wednesday's triage read at develop 7e2f8157cec2: `services/originate/src/routes/certifications.ts` checks access only on the legacy path (near `:219`, `documentId && !parentDocumentId`); the lineage branch (near `:413-426`, `:543`) has a cycle check but no parent-access check. Re-locate at the tip. Build the parent-access predicate on the lineage branch: a caller who cannot read the parent document cannot certify from it. Red-first (another org's parent accepted at the tip, refused with the fix), a control (own-org parent still certifies), and Stuart's note that Platform S sends the parent's hash (comment `c1712c38`) must still work. Tier 1 gate. `Refs KS-1557`.
3. **KS-1633**, same file, after KS-1557 is raised, own branch on develop: the ticket's option 1, write the `documents` row first as `POST /api/documents` does, so a failure after anchoring cannot leave an anchor with no row. Red-first. If the reorder changes a response a client sees, STOP and mail me. `Refs KS-1633`.
4. After each PR: READY FOR GATE (cause, cells, suite counts at the landing parent, files, predicted landing tree). Then one BLUF comment per ticket after its PR is raised (what changed, at review, no date). KS-1633 has no comments yet, so yours is the first word Stuart asked for.

## PARTITION

Yours: `services/originate/src/routes/certifications.ts` and its tests, plus the test harness configuration you need for step 1 (say which file before changing any). **NOT yours, live right now:** Seat R 52nd (Secuura/Blockchain-R): api-gateway (`src/index.ts`, `src/services/health.ts`, `src/routes/platform.ts`), originate `routes/verification.ts` (#1597). Seat C 25th (Secuura/Blockchain-C): originate `routes/documents.ts`, `documentRepo.ts`, `gatewayProvenance.ts` (KS-1402). Seat E 3rd (Secuura/Blockchain-E): api-gateway `routes/platform.ts` (KS-1195). Seat J 14th (Secuura/Blockchain-J): anchoring `src/index.ts`, `anchorOverwriteGuard.ts`, originate `routes/anchors.ts`. **You share an inbox with all of them: a brief or ANSWER naming another seat is not yours.** Identify yourself by your pane's cockpit name.

## HOLDS

- **Identity:** before the first commit in ANY clone, set `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai` LOCALLY, then read back `git config --show-origin user.email`. This Studio's global identity belongs to another client.
- **Work in a fresh clone** in your own scratch or the project's deploy-clones/; fetch develop explicitly (the shared checkout's develop is stale).
- **Pushing:** the repo's `.githooks/pre-push:352-358` refuses a push whose tip is not the checked-out HEAD, so check out the branch you push; `:76-80` refuses a non-fast-forward push. Never `--no-verify`; never `ALLOW_FORCE` without a mail from me naming it. Push with the transport in full: `-c core.sshCommand='<the repo's ssh command> -o ServerAliveInterval=30'`.
- Merge only on Wednesday's head-pinned GO after a gate verdict. No deploy.
- Client-facing communication = ticket comments only; the extranet is not a channel.
- No Docker on this Studio; PostgreSQL runs on a scratch PG in your scratch. Rotate inside your 80-90 band at a clean boundary; write the handover first.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- None. Both KS-1557 rulings are delivered: (b) caller may send its own hash, comment `c033e6fb`; (a) the read side hides own-hash certificates, merged in #1531.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- Step 1 is read-only and comes first; a read-side defect is reported, not fixed, in this lane.

PROVENANCE:
- KS-1557, KS-1633 state, priority, assignee, comment counts and last-comment times (as quoted inline) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- Kam's two KS-1557 rulings and their delivery artefacts | Wednesday's decision_queue (ruled cards secuura-ks1557-certify-hash-semantics-1013 and secuura-ks1557-readside-hides-own-hash-certificates-1013) | read 2026-10-19
- file pointers at 7e2f8157cec2, comment ids 28394c95 and c1712c38, Stuart's harness words | Wednesday's triage 0_Brain/reference/2026-10-19_stuart-list-triage/TRIAGE.md rows 7 and 9e (my project, not yours) | read 2026-10-19
- develop 846ae2788b3b | git ls-remote origin, run by Wednesday | read 2026-10-19
- pre-push refusals | your own .githooks/pre-push at 846ae2788b3b lines 76-80 and 352-358, read by Wednesday | read 2026-10-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-19 16:41
