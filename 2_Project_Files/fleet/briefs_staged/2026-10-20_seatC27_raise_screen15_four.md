## You are Seat C 27th (lane Secuura/Blockchain-C, a RAISE seat): raise four held Spark passes as four PRs

**Why you exist:** the Spark (local model) produced four PASSes overnight (screen 15). Wednesday read every one at source and held them. Seat R 55th is busy on other files (below), so these get their own lane under Kam's standing rule (as many agents as the code partition allows). The C lane's last seat, C 26th, wrapped cleanly; its handover is `5_Project_History/2026-10-19_seatC-26th/HANDOVER.md` (read its LATEST STATE for the clone and push setup that worked). Develop is `4a065fb7535080190c407237f948d0af3538f2dd` (#1626, KS-1460; Wednesday's ls-remote at 00:1x AEDT 2026-10-20). Send a short plan confirmation (preflight warnings verbatim) before your first write.

---
## BLUF

Raise four PRs, one per held Spark pass, each `Refs` or `Closes` exactly as below. Every patch is the Spark's output byte-for-byte (the canonical `patch.diff` named in each READY file). Re-take each pre-image at live develop before applying. Send a READY FOR GATE per batch. Merge only on Wednesday's head-pinned GO.

## QUEUE (in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/`)

1. **KS-1653**: `READY_KS-1653-STUBTRANSFERSCOPE-1_spark-dsv4flash_BRIEFED-CODEPATCH-USERS-PASS-7of7_2026-10-20.diff.md`. `hasUsersStubScope` in `services/auth/src/routes/users.ts` (~:256) also admits `documents:transfer-custody`; `certifications:write` stays. New vitest file. **This is the change the ticket's own Recommendation names**, so it closes the ticket (`Closes KS-1653` is acceptable; say if you disagree). Its one comment (11:00:57Z, from gate AJ1 N3) says the ADMISSION half had no red cell: the new test's control C1 (certifications:write still admitted) is that red, so say so in the PR. Tier 1: a security gate is widened by one scope.
2. **KS-1639**: `READY_KS-1639-TEXTFALSEINACTIVE-1_spark-dsv4flash_BRIEFED-CODEPATCH-CONVERTERS-PASS-7of7_2026-10-20.diff.md`. `rowToApiKey` in `services/security/src/converters.ts` (~:171) reads a string `is_active` as active only for `t`/`true` (any case, trimmed); everything else, including `''` and unknown strings, reads inactive. **It deliberately differs from the ticket's snippet** (that regex read `''` as active); the PR body says so and says the ticket's "accept text at all?" question is NOT settled. `Refs KS-1639`. Tier 1 (a revoked key must not read active).
3. **KS-1661**: `READY_KS-1661-SIMULATEDHEAL-1_spark-dsv4flash_BRIEFED-CODEPATCH2-VERIFICATION-PASS-7of7_2026-10-20.diff.md`. Both heal paths refuse a truthy INCOMING `chain.simulated`: `services/originate/src/routes/verification.ts` (~:454, v1) and `services/originate/src/routes/verificationV2.ts` (~:129, v2), plus a new jest file through both real routers. This was a rung-3 Spark task (two product files). Latent today. `Closes KS-1661` per the ticket's scope sentence ("both heal paths"). Tier 1 (anchor integrity). PR #1597 (KS-1634) touched the v1 verify route and MERGED on 2026-10-19 (Seat R 52nd's wrap, as recorded in Wednesday's note, not re-read by Wednesday on GitHub). So it is on develop already, and re-taking the pre-image at live develop covers it. KS-1634 itself is still In Progress with #1621 also merged, so do not touch its other open work.
4. **KS-1658**: `READY_KS-1658-NAMESPACECAUSE-1_spark-dsv4flash_BRIEFED-CODEPATCH-IDNAMESPACECOLLISION-PASS-7of7_2026-10-20.diff.md`. In `services/originate/src/utils/idNamespaceCollision.ts` (~:69), when a node cannot be read the walk now still visits its `cause` before returning. New jest file. `Closes KS-1658` (the ticket names only `cause`). Tier 2.
5. **Per PR:**
   - Show patch == sections, the pre-image blob at live develop, and the suite counts of that service at the landing parent, with a red-first run on develop.
   - Predict the landing tree on live develop.
   - Run an open-PR overlap census on each touched file (Wednesday holds no GitHub identity and did not check this).
   - One READY FOR GATE mail for KS-1653 + KS-1639 + KS-1661 together (one tier-1 batch) and one for KS-1658 (tier 2). They are file-disjoint, so Wednesday gates them as batches.
   - One BLUF ticket comment per PR.

## PARTITION

**Yours:** `services/auth/src/routes/users.ts` (the `hasUsersStubScope` hunk only), `services/security/src/converters.ts`, `services/originate/src/routes/verification.ts` and `verificationV2.ts` (the heal hunks only), `services/originate/src/utils/idNamespaceCollision.ts`, and the four new test files.

**NOT yours: Seat R 55th (Secuura/Blockchain-R) is live in these files right now.**
- `services/m365-integration/src/index.ts` (KS-1671)
- `services/auth/src/routes/auth.ts`
- `services/security/src/index.ts` (KS-1568)
- `services/api-gateway/src/routes/platform.ts` (KS-1622)

`routes/users.ts` is also named by KS-1194 part 2 (~:1293), a different hunk: check that PR's state before you push.

You share one inbox with every Secuura seat. A mail naming another seat (R 55th) is not yours. Establish your own seat from your pane and process, never from which thread looks like yours.

## HOLDS

- **A fresh clone has NO pre-push gate.** Before any push: `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`, then `git config --get core.hooksPath` read back in your plan confirmation (KS-1646).
- **Identity:** `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai` LOCALLY before the first commit; read back `git config --show-origin user.email`.
- **Pushing:** your repo's `.githooks/pre-push` refuses a push whose tip is not the checked-out HEAD (lines 352-358 at 846ae2788b3b, as read by Wednesday on 10-19; re-read at your clone) and a non-fast-forward push (:76-80). Never `--no-verify`; never `ALLOW_FORCE` without a mail from Wednesday naming it. Transport: `-c core.sshCommand='<the repo's ssh command> -o ServerAliveInterval=30'`.
- `tsc -p` in originate excludes test files (KS-1090): type-check the tests another way, and treat `Tests: 0 total` as a load failure. Build `packages/shared` first in a fresh clone (KS-846).
- Merge only on Wednesday's head-pinned GO after a gate verdict. No deploy. Ticket comments are the only client-facing channel. No Docker on this Studio.
- Rotate inside your 80-90 band at a clean boundary, handover first. Mail every state change; a turn never ends on an unmailed report.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- None for these tickets.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- None for these four tickets; each was held by Wednesday on 2026-10-20 at 00:18 (hold_ready output) after a source read of the diff.

PROVENANCE:
- KS-1653 Backlog, priority 4, 1 comment, last 2026-10-19T11:00:57Z, scope: "Add `documents:transfer-custody` to `hasUsersStubScope`. Keep `certifications:write`" | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- KS-1639 Backlog, priority 3, 0 comments, scope: "`rowToApiKey` reads the Postgres text forms of false as ACTIVE" | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- KS-1661 Backlog, priority 3, 0 comments, scope: "Both heal paths guard on the STORED blob's `simulated` flag and never look at the INCOMING anchoring reply's" | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- KS-1658 Backlog, priority 4, 0 comments, scope: "The KS-1642 read probe skips an unreadable node WITH ITS SUBTREE" | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- KS-1634 In Progress, priority 2, 9 comments, last 2026-10-19T12:40:03Z, attachments #1621 and #1597 (named only for overlap) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- develop 4a065fb75350 | git ls-remote origin via Wednesday's cache clone | read 2026-10-20
- the four diffs and the in-scope `visit`/`depth` for KS-1658 | Wednesday's source read of each run's section diffs and of idNamespaceCollision.ts at 4a065fb75350 | read 2026-10-20

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-20 00:19
