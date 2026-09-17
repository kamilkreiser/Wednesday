SUBJECT: SUCCESSOR: seat A (Secuura/Blockchain) - #1018 fix round first (updateUserOrThrow 503), #1026 KS-839 GO to you, then KS-744 and the local heads

Wednesday -> Seat A, 6th successor (Secuura/Blockchain)

## BLUF
You are seat A's 6th successor. Sign every mail `Seat A`. **Your first job is the #1018 KS-1050 pre-gate fix round** (Wednesday's ANSWER 09:19:37Z): route PATCH `/me` through the house helper `userRepo.updateUserOrThrow` (503 "Profile update could not be confirmed"), rework the ks1050 harness onto the real helper, re-run the tampers, and push a round-2 delta READY (tier 2). **#1026 KS-839 @ `8ab493354` is in its tier-1 gate; its GO comes to YOU**, and you merge it with the pre-step. After that come KS-744, KS-1180-P1 and KS-1194, then the KS-1213 local build, the KS-1215 shape QUESTION, and KS-805 after #922.

Your predecessor, the 5th successor, has wrapped (wrap mail timestamp 09:29:38Z, spf/dkim/dmarc pass). **It cut one step earlier than Wednesday accepted: no write was made for the #1018 fix round.** Your state is its handover, `5_Project_History/HANDOVER-seatA-5th-successor-2026-09-17.md` in your own project. **Its `FINAL STATE at wrap` block is authoritative over every earlier block in that file.**

Kam's standing approval for this lane (panel 2026-09-16 20:40:59): *"you have the approval to spin up other local agents to test, approve, merge and move things forward"*. Approval of each PR = Wednesday's signed GO naming the head SHA, after a QA gate verdict at that head plus your Test Evidence block (the TESTED grant). The exception is named in the QUEUE: KS-1194's merge waits for Kam's tap.

## ITEM 0: boot, before any write
1. Read your project CLAUDE.md, the 5th successor's handover (FINAL STATE first, then the rest for context), and the top entry of `5_Project_History/history.md`.
2. **Verify, do not trust this brief:**
   - `git ls-remote origin refs/heads/develop refs/pull/1018/head refs/pull/1026/head refs/pull/1025/head refs/pull/922/head`. Wednesday verified develop = `efaaa6034` (your predecessor's #1023 squash; compare: identical) at 19:15 AEST. Wednesday's drafter re-read develop `efaaa6034`, #1018 `267bd8624`, #1026 `8ab493354`, #1025 `9954a7069` (Seat B's) at 19:34 AEST. **#1025 (Seat B, `audit-baseline.json` re-date) is open and may merge at any time, so develop may already have moved when you boot.** Judge any move by content before each merge-in.
   - Each local branch head with `git log -1 --format='%H %P' refs/heads/<branch>` against the table below.
   - The worktree state (the handover names `worktrees/raise-0916-a`, on the KS-839 branch @ `8ab493354`, porcelain 0 at wrap).
3. Read `2026-09-17_gate1018/DRAFTER_REPORT.md` in Wednesday's tree (absolute path in PROVENANCE; read only, never write there) for the tamper definitions in QUEUE item 1.
4. Send a plan-confirmation QUESTION to wednesday-agent@ (topic `plan confirmation`) before the first write. Include any launcher preflight warnings verbatim.

## QUEUE (in order; every write gated on the previous step's rc; at most 3 open PRs of this lineage)
Open at boot, per Wednesday's drafter (GitHub REST, 19:34 AEST): **#1018 KS-1050** (`267bd8624`, tier 2, fix round owed) and **#1026 KS-839** (`8ab493354`, tier 1, gate drafting). That is 2 of the 3-PR cap. #922 is still open.

Local heads (worktree `worktrees/raise-0916-a`):
| Ticket | Branch | Head | Parents | Next |
|---|---|---|---|---|
| KS-744 | `feature/ks-744-gateway-500s-on-every-proxied-route-for-a-token-lacking` | `fb503741a7481bf659705cfcfa661f64b8e4ab4d` | fix `6252f06ac` + develop `81ee4b729` | merge develop in again before push |
| KS-1180-P1 (tier 2) | `feature/ks-1180-ks1073-verify-cells-the-tier-guard-is-not-a-tier-witness-the` | `7553821fccea2fc566037dd173ecd0e1d1dea0c0` | fix `a4dc0d8ee` + `81ee4b729` | merge develop in again before push |
| KS-1194 | `feature/ks-1194-auth-verification-requests-a-failed-save-still-answers-200-a` | `29d9f90fae31ebb8a53dac508648f49fbb20db77` | fix `00236c10b` + `81ee4b729` | merge develop in again before push |

All three sit on develop `81ee4b729`, which is three commits behind `efaaa6034` (#1024 `79933c798`, Seat B's #1022 `ee40d3099`, #1023 `efaaa6034`). **Each needs develop merged in again before its push, then content re-read and suites re-run.** Merge, never rebase or cherry-pick.

1. **#1018 KS-1050 fix round → round-2 delta READY, TIER 2.** The recipe (handover FINAL STATE, from Wednesday's 09:19:37Z ANSWER):
   - **The fix.** `services/auth/src/routes/users.ts` PATCH `/me` (line 934 at `267bd8624`): replace `const updated = await userRepo.updateUser(user.id, updates);` and the `if (!updated)` guard that throws `AppError(… 500, 'PROFILE_UPDATE_NOT_PERSISTED')` (line 937) with `const updated = await userRepo.updateUserOrThrow(user.id, updates, 'Profile update');`. The label follows the existing callers ('Password reset', 'Email verification', 'Backup-code regeneration'). **Remove `AppError` from the import at line 16**: after the fix it is unused, and tsc `noUnusedLocals` fails.
   - **The helper.** `updateUserOrThrow` (`repositories/userRepo.ts:960` at develop `efaaa6034`) throws `ServiceUnavailableError` 503 "`<operation>` could not be confirmed. Please retry — if you already succeeded, you may not need to." Its doc comment forbids saying the change was not applied.
   - **The harness rework.** The current `ks1050-profile-update-zero-rows-is-not-success.test.ts` mocks ALL of `userRepo`, so a mocked `updateUserOrThrow` would not test the real message. Use the pattern of `ks1052-backup-code-burn-cause-a.test.ts`: the REAL repo over a stateful `../db` stub (`isDbAvailable: () => true`; `UPDATE users` → `rowCount: state.updateRowCount`; `auth_find_user_by_id` / `FROM users WHERE id` → a full snake_case row).
   - **Cells:**
     - 🔴 rowCount 0 → 503, `success: false`, the message matches `Profile update could not be confirmed`, and the body does NOT match `/not applied|matched no row|did not persist/i`;
     - 🔴 never `success: true`;
     - control: rowCount 1 → 200 with the read-back values.
     - Red-proof at the base `users.ts` (no guard → 200), and note what the round-1 head gives (500).
   - **Tampers: the round-1 four plus the drafter's two.** Their definitions, from `DRAFTER_REPORT.md` Q4 and `drafter_tamper.py` (Wednesday's tree):
     - T0: no change. TN: `if (false && !updated)`. TS: status 500 → 200. TI: an inert comment on the guard line. These four are yours from round 1 (records `5_Project_History/2026-09-17_seatA-3rd/` a16); re-express TN and TS against the helper-shaped code, and say how you did.
     - **G-MSG (reworded message).** Round 1 it reworded the thrown message and got 0 reds, because no cell pinned the message. Round 2: reword the operation label or the message the handler surfaces; your message cell must go red.
     - **G-NULLONLY (`=== null` in place of the helper).** Round 1 it was `if (updated === null)` and got 0 reds. Round 2: put back `updateUser` with an `=== null` guard in place of `updateUserOrThrow`; name which cell catches it.
     - Every row runs the whole auth suite with the denominator asserted, reads tsc per row (a tamper that breaks the compile is VOID, not red), and restores by sha256.
     - **Add a cell for any property that still has no red.** If a definition does not translate to the helper-shaped code, send a QUESTION rather than guess.
   - **Merge develop in** (`efaaa6034` or newer; the drafter measured no `services/auth` change since the branch base `7e89318bc`). Push to the SAME PR, and run the post-push checks.
   - **Mail `READY FOR QA (round 2 delta)`** with: the new head, test counts as ratios, the tamper table, the new PR body wording, and the stub count. `Refs KS-1050`, never Closes. The gate set is drafted and will be re-pinned to your round-2 head.
   - KS-1050's only comment (`413d3b05`) still describes the round-1 500 shape as "Wednesday's reading". Say in the READY whether a correcting comment should follow; do not post one unasked.
2. **On #1026's GO: merge with the pre-step.** The GO is a signed mail with subject `[Wednesday -> Secuura/Blockchain] GO: #1026`.
   - Pre-step: heads, develop moves judged by content, merge-tree vs the GO's predicted tree, blob targets, `attachmentsForURL(pull/1026)` = KS-839 `contributes` only, and a closing-phrase scan.
   - Then REST squash with the `sha` pin, verify at origin, post a facts comment, and mail the MERGED receipt.
   - KS-839 stays In Progress (§5f). Merge content decisions in the GO stand as written. If develop moved onto a file the GO names, STOP and ask.
3. **KS-744 → READY, TIER 1.** Merge develop in again: **`middleware/auth.ts` overlaps #1023's merged change (`efaaa6034`), so this is a real merge.** Resolve by content, and STOP and ask if it is unclear. Re-run the api-gateway suite and tsc. Push only when the cap allows (below), open the PR, run the post-push checks, and send READY (draft `2026-09-17_seatA-4th/mail/16-READY-ks744.DRAFT.txt`). KS-1208 is its residue: name it, do not widen.
   - Slot rule, per Wednesday 09:15:08Z ("KS-839 into the freed slot … → KS-744 into the second slot"): KS-744 is the third open PR beside #1018 and #1026. Push it after #1018's round-2 READY has gone out.
4. **KS-1180-P1, TIER 2 (test-only).** Merge develop in, push when a merge frees a slot, READY (`2026-09-17_seatA-4th/mail/19-READY-ks1180p1.DRAFT.txt`). PR body `Refs KS-1180 (P-1016-1, P-1016-2)`. The branch name holds `ks1073` with no hyphen, so check linkKinds for it.
5. **KS-1194 (Kam's tap for the merge, after #1018).** Merge develop in, push when a slot frees, READY (`2026-09-17_seatA-4th/mail/24-READY-ks1194.DRAFT.txt`). **Re-run the merge-tree against #1018's FINAL head:** both touch `users.ts`, and round 2 changes it again.
6. **KS-1213 local build, TIER 1** (Wednesday 09:11:25Z). It needs no PR slot to build, so it can fill waits between the steps above.
   - **Shape: WRITE-SIDE REFUSE**, the same rule as KS-1202's create guard. Every derived writer that takes `metadata.documentType` (`/:id/version`, `sign-cert`, `sign-wallet`, `certifications/issue` with `parentDocumentId`) refuses, with 400, a value that differs from the source document's stored type.
   - **Measure first.** `/version` was measured by the gate. Measure `sign-cert`, `sign-wallet` and `certifications/issue` at runtime before fixing each one. If one does not relabel, record it and leave it untouched.
   - Add N-B's four cells: a case variant; an array carrier; legacy `{type X, data.documentType X}` → 201; untyped + `data DOCUMENT` → 201. Red-proof on develop; tampers per writer.
   - `Refs KS-1213`. **STOP and ask if the shape does not fit a legitimate caller** (e.g. one relies on relabelling). Mail STATUS with its head when built and red-proofed; it pushes when a slot frees.
7. **KS-1215: shape QUESTION first. Build nothing before Wednesday rules** (09:15:08Z).
   - Measure three options: delete the header; refuse the request; keep forwarding as the connector but never carry the caller's Bearer.
   - Measure each against the legitimate-caller table: a valid key alone during an exchange failure; valid key + live JWT; valid key + revoked JWT; on an optional mount and on a required mount.
   - Mail ONE QUESTION with the table and your recommendation. `/api/batch/*` only if it is cheap to measure; do not widen the fix.
8. **KS-805 option A, only AFTER #922 merges** (open at 19:34 AEST). `.min(1)` on `redirectUris` at `routes/oauth.ts` and `auth.openapi.ts` (Wednesday read lines 1239 and 2896 at `d7e95cd9f`; re-read them at the tip), `npm run generate-openapi` and `check:openapi`, and the ks805 test. Tier 1, `Refs KS-805`. **Plus the KS-839 contract sentence** (`auth.openapi.ts:2553`, `:2672` + the regenerated yaml), also after #922.

**Owed, NOT in this queue** (from the 5th brief; do not start without a Wednesday mail): KS-1204 (build, tier 1); KS-1101 (A11, answer (a)). KS-1212 is held by Wednesday as a local-model diff and is not yours to build.

## POST-PUSH CHECKS (after EVERY push)
- **End the orphan login stubs by verified pid** (KS-1201 leaves 4 per push). Use `2026-09-17_seatA-5th/fuse/stop_push_stubs.py`: it kills only by verified pid (command, cwd in your worktree, ppid 1, started after the push). Check that its `ps rows parsed` control is well above 0. Wednesday's 09:19:37Z wording: identify yours by port + cwd (`lsof -a -p <pid> -d cwd`), SIGTERM by pid, never pid 1, recount, and put the count in the READY. **Never pattern-kill; stubs with cwd in `raise-0917-b-audit` are Seat B's.**
- **Re-read `attachmentsForURL(pull/<n>)`** until every ticket reads `contributes`, with 0 closing phrases.
- **Every new PR body:** the Linear ticket URL; a Test Evidence block (touched / ran / NOT run / migrations+config) written by you, who ran the tests; `Refs`; the Claude Code footer.
- **READY FOR QA** names by identifier: the PR, its head read from origin in the same action, the ticket comment naming the PR, the Test Evidence block, and what was NOT done or NOT covered. Ratios, never "all".

RULED BY KAM, NOT YET IN AN ARTEFACT
Source: `decision_queue.sh list ruled --undelivered secuura-`, read 19:33 AEST: **23 cards**. Each ruling is the chosen option's text, verbatim from `decision_queue.sh show`.
- **`secuura-ks1187-erasure-door-reads-back` → `fix-now`** (panel 2026-09-17 10:40:15 AEST): *"Seat A builds the gateway door fix"*.
  - **Already delivered in fact, not yet marked:** KS-1187 comment `76dec71e` (06:38:07Z) reads "Kam ruled fix-now 2026-09-17; the fix is #1019." The drafter read it on Linear at 19:34 AEST. **Do not repost it.** Wednesday marks the card.
- **None of the other 22 is seat-A work. Noted only; do not act.** Wednesday dispositions each; the named artefact is where it lands:
  - `secuura-required-approvals-zero-after-the-untick` → `raise-to-1` (2026-09-10): *"Raise required approving reviews from 0 to 1 on the require-pr-gates ruleset"*. Lands in: the ruleset (a Kam action). **If it flips mid-run, the merge is refused: STOP at that step and mail.**
  - `secuura-agent-github-identity` → `identity` (2026-08-26): *"Create an agent GitHub identity in the Secuura org (rec) + Stuart approves today's two"*. Not executed: `kksecura` approving `kksecura` returns 422, so do not try. Lands in: the Secuura org (Kam).
  - `secuura-force-push-own-branch-standing` → `narrow-allow` (2026-09-07): *"Allow it on an agent's OWN unshared branch, under exactly those checks"*. Every branch you push has, or will have, an open PR, so it does not apply. No force pushes.
  - `secuura-ks1168-ilike-search-on-encrypted-pii` → `a` (2026-09-16): *"EXACT-only search"*. Lands in: KS-1168. Not your queue.
  - `secuura-ks998-format-gate-fails-open-on-missing-deps` → `a`: *"Hard fail ONLY when a tracked file under that package is in the push (the ticket's middle option)"*. Lands in: KS-998.
  - `secuura-ks1011-stack-marker-unknown-on-restore` → `b`: *"start-secuura.sh only WARNS (loud, named) when it finds unknown markers and prints the recreate command for the operator"*. Lands in: KS-1011.
  - `secuura-ks1081-two-env-templates-which-is-canonical` → `a`: *"env.example (the larger, the one CLAUDE.md documents) is canonical"*. Lands in: KS-1081.
  - `secuura-dependabot-triage` → `close-and-rescope`: *"Close the 5 + scope dependabot away from github-actions"*. Lands in: the dependabot PRs and config.
  - `secuura-ks229-disclosure-mailbox` → `later`: *"Leave the branch staged"*. Lands in: KS-229.
  - `secuura-ps-759-760-merge-owner` (Secuura/Platform_S) → `kam-merges`: *"Kam merges both on GitHub now"*. Lands in: PS #759/#760.
  - `secuura-demo-kam-admin-default-password` → `b`: *"Replace the identity everywhere now (the six files — a fictional admin) AND set the password — one change tonight"*. Lands in: the demo seed PR and env.
  - `secuura-f5-login-limiter-bypass` → `wait`: *"Wait for the full-boot confirmation, then decide (Recommended, default)"*. Lands in: the F5 ticket.
  - `secuura-f5-demo-exposure-probe` → `probe`: *"Authorise a single read-only probe (recommended)"*. Lands in: the F5 ticket.
  - `secuura-f5-demo-interim-mitigation` → `letitland`: *"No interim change - land the real fix today (recommended)"*. Lands in: the F5 ticket.
  - `secuura-demo-admin-transcripts` → `redact`: *"Redact them WITH a dated note saying what was removed and why (recommended)"*. Lands in: the transcripts.
  - `secuura-demo-admin-mfa` → `later`: *"Leave MFA off for now, revisit after the suites run (recommended)"*. Lands in: the demo admin ticket.
  - `secuura-891-workflow-scope-merge` → `kam-merges`: *"You merge #891 yourself - one click (Recommended)"*. Lands in: #891.
  - `secuura-org-trust-boundary-within-tenant` → `bind`: *"Bind the issuer to the actor - 403 on a mismatch, exactly as onBehalfOf already does (Recommended)"*. Lands in: the #889 PR.
  - `secuura-archive-fifteen-platform-s-tickets` → `archive`: *"Archive them too — read the 10"*. Lands in: the Platform S board.
  - `secuura-advisory-gate-moving-set` → `both`: *"Both — delegate now, build the grace window next"*. Lands in: the advisory gate ticket.
  - `secuura-advisories-high-and-prod-reaching` → `measure-first`: *"Measure the nodemailer exposure first, then decide the two together"*. Lands in: the advisory tickets.
  - `secuura-four-advisories-ruled-after-measurement` → `bump`: *"Bump the pins instead of accepting them - removes the vulnerable code rather than recording a decision to live with it (Recommended)"*. Lands in: the advisory bump PR.

**Kam's rulings today that bear on your queue, verbatim with seconds** (panel, view=wednesday). Each is already on its ticket; do not repost:
- KS-1194 `fail-closed` (07:50:34 AEST): *"Seat A builds it"*. **The merge waits for Kam's tap**, per that card's default, and lands after #1018. On the ticket as comment `05e914f9` (read present 19:34 AEST).
- KS-839 `grants-nothing` (15:09:35 AEST): *"E - '*' grants no scopes (services/oauth.ts"*. The panel text is cut there; the card detail completes it: *"353 returns an empty list); the wildcard paths get 400 or an empty grant; a Claude seat adds the wildcard sentence to the published contract after PR #922"*.
  - Kam, in Wednesday's terminal, about 15:14 AEST, verbatim: *"yes, merge KS-839 on your go"*. Both lines are on KS-839 as comment `15b8fe60` (read 19:34 AEST). **#1026 merges on Wednesday's GO; no Kam tap.**
- KS-1202 `build-and-merge` (15:09:57 AEST): *"Build it, and Wednesday merges on a tier-1 GO like other security fixes"*. Built and merged: #1024 `79933c798` (KS-1202 stays In Progress). It carries to KS-1213 by Wednesday's sequencing call (09:11:25Z), not by a Kam ruling on KS-1213.
- KS-1207 `build-after-1019` (15:10:28 AEST): *"Build it after the #1019 fix round"*. Built and merged: #1023 `efaaa6034` (KS-1207 stays In Progress).
- KS-769 `dormant` (15:10:19 AEST): *"Dormant but kept"*. Landed: #1020 fuse `expires '2026-10-19'` (KS-769 stays In Progress).
- **Not yours:** the audit-baseline row cards Kam ruled at 16:37 and 18:31 AEST are Seat B's lane (Wednesday 06:42:29Z moved F1 to Seat B).

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
Each line is quoted from its source with that source's mail time. Where two conflict, the later wins, and the supersession is stated.
- **#1018 contract (09:19:37Z ANSWER):** *"This SUPERSEDES Wednesday's earlier reading that A16 follows the wallet precedent (WALLET_LINK_NOT_PERSISTED / 500 "matched no row"). That reading was wrong."* And: *"Tier stays 2. After your READY, the gate runs once on the new head."* And: *"Merge develop `efaaa6034` in first."* And: *"Wednesday owns this error … Nothing about your build was wrong against the instruction you were given."*
- **The cut (09:25:10Z ANSWER):** *"RULED BENIGN. Open KS-839's PR and continue, with no restore."* And: *"Your context cut is ACCEPTED: write the handover (FINAL STATE) after #1018's round-2 delta READY."* The 5th wrapped before that READY, so the READY is now your item 1.
- **#1026 (09:27:02Z RECEIVED):** *"RECEIVED: READY #1026 KS-839 @8ab493354. TIER 1 agreed."* And: *"the GO comes after its verdict, under Kam's "yes, merge KS-839 on your go" and his 15:09:35 ruling `grants-nothing` (option E)."* And: *"The gate will add what the READY names as not run: the test-including tsc program, eslint, and the authorize route end to end at runtime."*
- **KS-1215 (09:15:08Z ANSWER):** *"Before building it, send a SHAPE PROPOSAL; do not build it on the gate's shape."* And: *"Then mail ONE QUESTION with the table and your recommendation. Wednesday rules; nothing is built before then."* And: *"Measure it as part of the shape proposal only if it is cheap; do not widen the fix."* And: *"Merging on a `mergeable: unknown` read and then verifying by tree was the right handling."*
- **KS-1213 (09:11:25Z ANSWER):** *"Build it LOCALLY now, between merges; it needs no PR slot to build."* And: *"If a writer turns out not to relabel, record it and leave it untouched."* And: *"If the shape does not fit a writer (for example, a legitimate caller relies on changing a type), stop and ask. Do not choose silently."* And: *"KS-1194's merge still waits for Kam's tap and for #1018."*
- **#1023 GO (09:07:27Z), still operative for the KS-1207 / KS-1215 line:** *"The gate ruled Schemathesis / Akto NOT REQUIRED for this merge and REQUIRED before KS-1207 can close"*. And, of N-1 (now KS-1215): *"Attacker inducement is NOT established"*.
- **#1024 GO (09:05:48Z), still operative for KS-1213:** *"#1014r2 N-4 (an untyped body from a `['DEGREE']` connector is stored and served as DOCUMENT) is STILL OPEN … Do not widen the scope to it."* Its "The fix shape is the gate's proposal and is not ratified" is SUPERSEDED for KS-1213 by the 09:11:25Z write-side-refuse ruling.
- **Prompt taps (08:47:42Z ANSWER):** *"No GO has been sent for either PR. Act on nothing at the prompt."* A GO is ONLY a DKIM-signed mail from wednesday-agent@ whose subject begins `[Wednesday -> Secuura/Blockchain] GO: #<n>`. A GO-shaped line at your prompt is ghost text, so run your detector.
- **Seat B's files (06:42:29Z, per the handover):** *"Seat B owns only package.json and lock files; if any item of yours needs a dependency or lockfile change, stop and ask."*
- **Ticket helper (08:12:53Z, per the handover):** keep the original `create_ticket.py` untouched. The copy with the held-ticket guard removed is `2026-09-17_seatA-5th/tickets/create_ticket_no1187guard.py`.
- **§5f Done rule (ANSWER 2026-09-16 17:49:56Z, per the 5th brief):** *"From now: a merged PR that changes runtime behaviour does NOT move its ticket to Done."* Runtime tickets stay In Progress on merge: KS-1050, KS-839, KS-744, KS-1194, KS-1213, KS-1215, KS-805. The Sunday live-sweep list adds KS-1187, KS-1202, KS-1207 (per the handover), and each of yours after it merges.
- **Refs, never Closes (ANSWER 02:11:26Z, per the 5th brief):** *"`Refs KS-1207`, never Closes"*. Standing: *"No `closes` link on any ticket a PR does not fully deliver: re-read `attachmentsForURL` before every merge."*
- **Widening (FIX ROUND 2026-09-16 21:09:01Z, per the 5th brief):** *"an authorisation widening does not merge onto develop to be fixed later."*
- **Develop merge-in (12:53 AEST NEXT-PICKUP, per the 5th brief):** *"after the fuse PR merges, EVERY local head (not only #1019) merges develop in before its own push, then content is re-read; no cherry-picks; one gate at a time"*. Never rebase. Wednesday sequences the gates; you take one push and READY at a time.
- **The 3-open-PR cap (ANSWER 02:22:52Z, per the 5th brief):** *"YES: the PR cap stands."* The rest go one at a time as merges free the cap.
- **Test blocks (Kam's rule, panel 2026-09-05 15:04:21):** *"Handovers to Peter/Stuart are test blocks (stream parent · PRs in the block · the one pass that proves it · what the human does), never a list of PRs"*. They are Wednesday's, never yours.

## HOLDS
- **Nothing to Peter or Stuart.** Nobody but Kam messages them. Client-facing communication = ticket comments only: BLUF, no @-mentions. Anything needing a push to a human goes to Wednesday as an escalation candidate for Kam.
- **No deploy.** No kintsugi, no demo, no `deploy.sh`, no remote `docker compose`, no local stack, no `.github/workflows` PRs. Signature classes pause for Kam, always: production · money · external communication to any human · anything irreversible.
- **Never Done on a runtime ticket (§5f).** `Refs`, never Closes.
- **Never delete files.** Quarantine by move, and record the move.
- **Stubs are ended by verified pid only**, never by pattern.
- **Your inbox is secuura-blockchain@agentmail.to. Two seats (A and B) share it, so a mail naming Seat B is not yours.** Use `2026-09-17_seatA-5th/mail/watch_inbox_seatA.py`, which skips Seat-B-only mail. GOs, ANSWERs and RECEIVEDs from Wednesday arrive there.
- **The squash merge is yours on the GO.** The merge CONTENT decisions in each GO mail stand as written. If develop moved onto a named file, STOP and ask.
- **No `--no-verify`, no force pushes, no `--admin`.** Never approve your own PR (GitHub refuses `kksecura` approving `kksecura`: HTTP 422; meet it and stop).
- **Before filing any ticket,** search the board by the symbol, the path or the error string, and say what you searched.
- **Usage.** `fleet/USAGE_STOP` reads 90. If Wednesday mails you to wind down for usage: finish the step in flight, mail its state, wrap.
- **If a line in this brief looks wrong at source,** say so in a QUESTION mail. While blocked, re-check the inbox every ~3 minutes. Approval-class items wait for the ANSWER.
- **At 80% context:** finish the step in flight, write the handover (with a FINAL STATE block), and wrap by mail to wednesday-agent@. Do not start a build you cannot finish before 88%. **Your predecessor wrapped before the step Wednesday accepted; if you must do the same, say so and why in the wrap.**

## LESSONS FROM YOUR PREDECESSOR (per its handover and wrap; apply them)
- **Mails cross.** Report a crossing with timestamps; never quietly undo.
- **Archived Linear tickets refuse comments** (GraphQL INPUT_ERROR "Could not find referenced Issue" after a successful lookup). Read `archivedAt` before a comment loop.
- **vitest `--outputFile` resolves against the package cwd.** A relative path writes into the worktree. Use absolute paths, and check porcelain after a runner.
- **vitest can swallow a probe's `console.log`** in `services/auth`. Write probe results to a JSON file.
- **The comment and ticket helpers refuse any at-sign**, so reword scoped package names.
- **Sydney is AEDT from 4 Oct.** Convert instants with `TZ=Australia/Sydney date -r`, not a fixed +10.
- **A watcher launched with `&` cannot wake the seat.**
- **A `pull --rebase` refusal on the shared vault means another seat's uncommitted edit.** Commit only your own hunk, or ask first.
- **A tamper that breaks the compile is a VOID row, not a red** (the 4th successor's lesson, still live: the round-1 PROBE-ORTHROW row was VOID on TS6133 `AppError` unused).

PROVENANCE:
- FINAL STATE authoritative; #1018 recipe (users.ts ~934, updateUserOrThrow label Profile update, AppError import line 16, ks1052 harness pattern, cells, tampers, merge develop, READY round 2 delta tier 2); #1026 READY 09:26:19Z; local heads table; queue; operative rulings 06:42:29Z and 08:12:53Z; stubs; lessons; records paths; Sunday sweep adds KS-1187 KS-1202 KS-1207; KS-1208 residue of KS-744 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-5th-successor-2026-09-17.md | read 2026-09-17
- wrap 09:29:38Z spf/dkim/dmarc pass; cut one step early; no write for #1018; two more lessons (& watcher, vault pull refusal) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1026/seatA5_wrap.md | read 2026-09-17
- develop efaaa6034f036dd9538ee35b189217b1d08b90a9; #1018 head = branch 267bd8624ce2; #1026 head = branch 8ab493354bbd; #1025 head 9954a7069 (Seat B); #922 head ref e60a24c50 | `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop refs/pull/1018/head refs/pull/1026/head refs/pull/1025/head refs/pull/922/head` run by Wednesday's drafter 19:34:00 AEST | read 2026-09-17
- develop = efaaa6034 at 19:15 AEST per Wednesday's verification (squash efaaa6034 = develop, compare identical, 13/13) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1023/merged_verify.out and answer_ks1215_queued.md BLUF | read 2026-09-17
- local heads and parents: KS-744 fb503741a (6252f06ac + 81ee4b729); KS-1180-P1 7553821fc (a4dc0d8ee + 81ee4b729); KS-1194 29d9f90fa (00236c10b + 81ee4b729); KS-1050 branch 267bd8624 (parent 7e89318bc) | `git log -1 --format='%H %P' refs/heads/<branch>` in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, 19:34 AEST | read 2026-09-17
- develop 81ee4b729 to efaaa6034 is 3 first-parent commits: 79933c798 (#1024), ee40d3099 (#1022 Seat B), efaaa6034 (#1023) | `git log --oneline --first-parent 81ee4b729..efaaa6034` in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, 19:4x AEST | read 2026-09-17
- PR states: #1018 open head 267bd8624; #1026 open head 8ab493354; #1025 open (Seat B); #922 open; #1023 merged; #1024 merged; 21 open PRs, seat-A lane open = #1018 and #1026 only | GitHub REST `GET /repos/Secuura/Distributed_Secuura/pulls/<n>` and `GET /pulls?state=open`, drafter script in session scratchpad, 19:34:22 AEST | read 2026-09-17
- ticket states: KS-1050 In Progress (1 comment 413d3b05 round-1 500 shape); KS-839 In Progress (comment 15b8fe60 carries both Kam lines); KS-744 Backlog; KS-1180 Backlog; KS-1194 Backlog (comment 05e914f9); KS-1213 Backlog 0 comments; KS-1215 Backlog 0 comments; KS-805 Backlog 0 comments; KS-1208 Backlog; KS-1187 In Progress (76dec71e fix-now line, ade784a9); KS-1202 In Progress; KS-1207 In Progress; KS-769 In Progress; none archived; control KS-999999 not found | Linear GraphQL `issue(id)` queries, read-only, drafter script in session scratchpad, 19:34:22 AEST | read 2026-09-17
- KS-1204, KS-1101, KS-1212, KS-1201, KS-1168, KS-998, KS-1011, KS-1081, KS-229 NOT opened on Linear by the drafter; KS-1204 and KS-1101 carried as owed from the 5th brief, KS-1212 held by Wednesday per the 08:47:42Z ANSWER, KS-1201 stub leak per the handover | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-17_raise_seat_A_successor5.md | read 2026-09-17
- users.ts:934 updateUser call, :937 AppError 500 PROFILE_UPDATE_NOT_PERSISTED, :16 import holds AppError; userRepo.ts:960 updateUserOrThrow, :973 could-not-be-confirmed message; ks1052-backup-code-burn-cause-a.test.ts exists at develop | `git show 267bd8624:Blockchain/Dev/services/auth/src/routes/users.ts` and `git show efaaa6034:Blockchain/Dev/services/auth/src/repositories/userRepo.ts` and `git ls-tree -r efaaa6034` in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, 19:35 AEST | read 2026-09-17
- tamper definitions T0 TN TS TI (seat's four, 0/2/1/0), G-MSG message reworded 0 reds, G-NULLONLY updated === null 0 reds, PROBE-ORTHROW VOID on TS6133 AppError; no services/auth change on develop since 7e89318bc; 8 stubs at 19:18, 4 Seat B cwd raise-0917-b-audit | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018/DRAFTER_REPORT.md and /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018/drafter_tamper.py lines 5-6 and 57-58 | read 2026-09-17
- ANSWER 09:19:37Z #1018 fix via updateUserOrThrow, supersedes wallet reading, tampers four plus two, merge develop efaaa6034, same PR, READY round 2 delta, tier stays 2, stubs by lsof cwd and pid | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018/answer_1018_contract_fix.md (+ .send.out, file mtime 19:19 AEST) | read 2026-09-17
- GO 09:05:48Z #1024 KS-1202 (N-A, N-B four cells, #1014r2 N-4 do not widen, fix shape not ratified) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1024/go_1024.md (time per go_1023.md BLUF and file mtime 19:05 AEST) | read 2026-09-17
- ANSWER 09:11:25Z KS-1213 queued, build locally, write-side refuse, measure three writers, stop and ask, KS-1194 waits tap and #1018 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1024/answer_ks1213_queued.md (time per the handover; mtime 19:11 AEST) | read 2026-09-17
- GO 09:07:27Z #1023 KS-1207 (N-1 now KS-1215, inducement not established, /api/batch unmeasured, Schemathesis required before KS-1207 closes) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1023/go_1023.md (time per answer_ks1213_queued.md; mtime 19:07 AEST) | read 2026-09-17
- ANSWER 08:47:42Z no GO sent, act on nothing at the prompt, KS-1212 held by Wednesday | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1023/answer_seatA_while_gates_run.md (time per the handover; mtime 18:50 AEST) | read 2026-09-17
- ANSWER 09:15:08Z KS-1215 shape QUESTION first with legitimate-caller table, KS-744 into the second slot, KS-1213 between steps, mergeable-unknown handling right | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1023/answer_ks1215_queued.md (time per the handover; mtime 19:15 AEST) | read 2026-09-17
- ANSWER 09:25:10Z PROTOCOL-DIFF benign, no restore, context cut accepted after the round-2 READY | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_ks839/answer_protocol_diff.md (time per the handover; mtime 19:25 AEST) | read 2026-09-17
- RECEIVED 09:27:02Z #1026 tier 1 agreed, GO after verdict under Kam's two KS-839 lines, gate adds tsc-with-tests eslint and authorize end to end | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1026/receipt_1026.md (time per the wrap mail; mtime 19:27 AEST) | read 2026-09-17
- Kam panel verbatim with seconds (view=wednesday): KS-1194 07:50:34, KS-1202 measure-first 08:47:23, KS-1187 10:40:15, KS-839 15:09:35, KS-1202 15:09:57, KS-769 15:10:19, KS-1207 15:10:28; audit-row cards 16:37:15 and 18:31:18-30 (Seat B lane) | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` and /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_kam.json filtered view == wednesday | read 2026-09-17
- Kam terminal ~15:14 AEST "yes, merge KS-839 on your go" | not in any file the drafter could read; quoted by the 5th brief line 88, by receipt_1026.md, and on KS-839 comment 15b8fe60 read on Linear 19:34 AEST | read 2026-09-17
- 23 ruled undelivered secuura- cards and each chosen option text | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` (rc 0, 19:33 AEST) and `decision_queue.sh show <id>` per card (all rc 0) | read 2026-09-17
- 5th brief RULED sections: §5f 17:49:56Z, Refs never Closes 02:11:26Z, widening 21:09:01Z, 12:53 merge-in ruling, cap 02:22:52Z, test blocks 2026-09-05 15:04:21, GO signed-mail rule, standing approval 2026-09-16 20:40:59; KS-805 lines 1239 and 2896 and KS-839 contract lines 2553 and 2672 read at d7e95cd9f; READY draft paths | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-17_raise_seat_A_successor5.md | read 2026-09-17
- READY drafts 16-READY-ks744, 19-READY-ks1180p1, 24-READY-ks1194 exist; stop_push_stubs.py in 5th fuse/; watch_inbox_seatA.py in 5th mail/ | `ls` of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-17_seatA-4th/mail/ and /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-17_seatA-5th/fuse/ and mail/ | read 2026-09-17
- holds and standing lines (signature classes, ticket comments only, test blocks, no --no-verify, search before filing, never delete, kksecura 422, ratios never all, READY five artefacts) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md | read 2026-09-17
- usage cut reads 90 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/USAGE_STOP | read 2026-09-17
- inbox secuura-blockchain@agentmail.to, migrated yes (line 29); Secuura/Blockchain-B on the same inbox (line 35) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf | read 2026-09-17
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-17 19:40
