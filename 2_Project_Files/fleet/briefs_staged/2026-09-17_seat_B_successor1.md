SUBJECT: SUCCESSOR: Seat B (audit-baseline rows) - #1027 GO and merge come to you, then PR-3b vitest, PR-7 mysql2, PR-4 qs before the Thu 24 Sep 10:00 AEST lapse

Wednesday -> Seat B, 1st successor (Secuura/Blockchain-B)

## BLUF
You are **Seat B's 1st successor**. Sign every mail `Seat B`, and end every subject `(Seat B)`. Your lane is the dated rows in `Blockchain/Dev/scripts/audit/audit-baseline.json`. **"Fix" means the advisory is gone from every lock. Moving a date is not a fix.**

Your predecessor wrapped at 10:04:55Z (spf/dkim/dmarc pass). Your state is its handover, `5_Project_History/HANDOVER-seatB-audit-2026-09-17.md` in your own project. **Its `FINAL STATE (at wrap, 10:05Z)` block is authoritative over every other block in that file, and over this brief where they disagree** (say so in a QUESTION).

What is on your desk:
- **#1027 (PR-3a: js-yaml HIGH + baseline-browser-mapping, rows 7 and 5, KS-1211) @ `d7fc6cc55`: READY, gate being drafted by Wednesday.** Its GO and its squash merge come to YOU, with the pre-step.
- Then, in order: **PR-3b vitest → PR-7 mysql2 → PR-4 qs → PR-5 react-router-dom → PR-6 @hono/node-server → PR-8 ip-address → MIG-1 react-router v7.**
- **The clock:** rows 1, 2, 3 and 4 (and rows 5 and 7, if #1027 has not merged) lapse **Thu 24 Sep 10:00 AEST**. From that minute **every push that touches `Blockchain/Dev` is refused**: yours, Seat A's, Kam's, Peter's and Stuart's. Rows 13, 14 and 15 do the same from **Wed 30 Sep 10:00 AEST**. **A STATUS on the 24 Sep rows is due to Wednesday by Mon 21 Sep 18:00 AEST.**

Merges happen under Kam's TESTED grant: a QA gate verdict at the PR's current head, your Test Evidence block, and Wednesday's signed GO naming that head.

## TWO SEATS, ONE INBOX. Read this before any mail.
Your inbox, `secuura-blockchain@agentmail.to`, is also **Seat A's**. Seat A's 6th successor is live now, working #1018 KS-1050, #1026 KS-839, KS-744, KS-1180, KS-1194, KS-1213, KS-1215 and KS-805 in `worktrees/raise-0916-a`.
- **A mail is yours** only when its subject begins `[Wednesday -> Secuura/Blockchain-B]`.
- **A mail addressed `[Wednesday -> Secuura/Blockchain]` (no `-B`), or one that names Seat A, is NOT yours.** Never act on it and never reply to it. A GO for Seat A is not a GO for you.
- **You own only `package.json` files, `package-lock.json` files and `audit-baseline.json`** (plus your records and ticket comments). Seat A owns `services/*/src`. The one open scope question (MIG-1's `src/**`) is under OPEN.

**Mail you send:** `[Secuura/Blockchain -> Wednesday] <KIND>: <topic> (Seat B)` to wednesday-agent@agentmail.to. KIND is one of QUESTION / STATUS / READY FOR QA / MERGED. Use your predecessor's guard `2026-09-17_seatB-audit/mail/send_mail.py <subject> <body-file> <payload-out.json>` (subject must end `(Seat B)`, body must start `Seat B`), with the payload written into YOUR records folder. The inbox waiter is `mail/wait_seatb.py SINCE MAXMIN INTERVAL`.

## ITEM 0: boot, before any write
1. **Read:**
   - your project `CLAUDE.md` and `2_Project_Files/CLAUDE.md` at develop;
   - `.claude/skills/secuura-test-discipline/SKILL.md` at develop (§5f Evidence binds);
   - the handover (FINAL STATE first, then the whole file);
   - the top entry of `5_Project_History/history.md`;
   - `systemTest/CLAUDE.md` lines 460-470 at develop (rules 1 and 2, for OPEN item 1).
   - **Before any regen (PR-3b onward):** your predecessor's first brief's LOCKFILE PROCEDURE is quoted below. Its source is root `BACKLOG.md`, the `fast-uri regen — DONE and merged` entry. Where the record and this brief disagree, the record wins; say so in a QUESTION.
2. **Verify, do not trust this brief:**
   - `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop refs/pull/1027/head`. Wednesday's drafter read develop = `19f1e54750ce2b65312a687add2db4f5628edb7d` (#1025 squash) and #1027 = `d7fc6cc5582b918c0773ec6f25f86407de6f86ab` at 20:08:55 and again at 20:16:15 AEST. **Re-read develop at boot and judge any move by content.** Seat A has open PRs and may merge at any time.
   - The rows at the tip. Parse `audit-baseline.json` and list every row with `expires <= '2026-10-02'`. At `19f1e5475` the drafter parsed **34 rows, 11 of them dated** (table below). If your count differs, STOP and mail.
3. **Worktrees.** Your predecessor left two, both clean at wrap, and the drafter read the same state at 20:1x AEST:
   - WT1: `worktrees/raise-0917-b-audit`, detached at `19f1e5475`, porcelain 0;
   - WT2: `worktrees/raise-0917-b-audit-2`, on `feature/ks-1211-bump-jsyaml-bbm` at `d7fc6cc55`, porcelain 0.
   - Re-read each one's HEAD and porcelain. Run `bash scripts/preflight/deps-present.sh` in a worktree before any push from it.
   - **Never use the shared checkout `2_Project_Files`, `worktrees/raise-0916-a`, `worktrees/seat-a` or the older `worktrees/seat-b`.**
4. **Records:** a new folder, `5_Project_History/2026-09-17_seatB-succ1/`, in your own project. Read your predecessor's `5_Project_History/2026-09-17_seatB-audit/` (tools, `pr3-devtools/`, `mail/`); never rewrite it.
5. **Plan-confirmation QUESTION** to wednesday-agent@ (topic `plan confirmation (Seat B)`). Include:
   - the queue as you re-derived it at the tip;
   - **every warning your launcher printed at boot, verbatim** (your predecessor's were F-02 and KS-907);
   - OPEN item 1 (the systemTest rule-2 question), as its own numbered question;
   - OPEN item 2 (MIG-1 source scope), as its own numbered question.

   Before the ANSWER, the only writes allowed are your records folder and a `npm ci` inside WT1 or WT2. **One exception: a signed `[Wednesday -> Secuura/Blockchain-B] GO: #1027` mail is its own instruction, and you may execute it on arrival** (this exception is the drafter's sequencing, confirmed or withdrawn in the ANSWER).

## STATE AT WRAP (read at source by Wednesday's drafter, 20:08-20:16 AEST)
**Merged by your predecessor on signed GOs:** #1021 colord (row 6) squash `81ee4b729`; #1022 hono ×3 (rows 8-10) squash `ee40d3099`; #1025 re-date of rows 11/12 to `2026-10-02` (KS-528) squash `19f1e5475` = develop.

**Rows still dated at develop `19f1e5475`** (numbering = your predecessor's fixability table; severity settled at 07:24:18Z, HIGH = js-yaml and ip-address, the rest medium):

| # | GHSA | package | expires (lapse, AEST) | row's ticket field | live ticket | vehicle |
|---|---|---|---|---|---|---|
| 1 | GHSA-4mjr-xmp4-gh2g | qs | 2026-09-24 (Thu 24 Sep 10:00) | KS-763 | KS-763 | PR-4 |
| 2 | GHSA-x5fp-wj9c-mxmx | qs | 2026-09-24 (Thu 24 Sep 10:00) | KS-763 | KS-763 | PR-4 |
| 3 | GHSA-rgwj-5xj2-c3m3 | mysql2 | 2026-09-24 (Thu 24 Sep 10:00) | KS-763 | KS-763 | PR-7 |
| 4 | GHSA-82fw-gwwq-j7x9 | vitest / @vitest/mocker | 2026-09-24 (Thu 24 Sep 10:00) | KS-1024 | KS-1211 | PR-3b |
| 5 | GHSA-w5vr-8v7q-w6rv | baseline-browser-mapping | 2026-09-24 (Thu 24 Sep 10:00) | KS-1024 | KS-1211 | #1027 |
| 7 | GHSA-2883-xcg3-v3hh | js-yaml **HIGH** | 2026-09-24 (Thu 24 Sep 10:00) | KS-1024 | KS-1211 | #1027 |
| 13 | GHSA-jjmj-jmhj-qwj2 | react-router-dom | 2026-09-30 (Wed 30 Sep 10:00) | KS-528 | KS-528 | PR-5 |
| 14 | GHSA-frvp-7c67-39w9 | @hono/node-server | 2026-09-30 (Wed 30 Sep 10:00) | KS-530 | KS-530 | PR-6 |
| 15 | GHSA-mwp4-54f8-5fhr | ip-address **HIGH** | 2026-09-30 (Wed 30 Sep 10:00) | KS-729 | KS-729 | PR-8 |
| 11 | GHSA-wrjc-x8rr-h8h6 | react-router | 2026-10-02 (Fri 02 Oct 10:00) | KS-528 | KS-528 | MIG-1 |
| 12 | GHSA-337j-9hxr-rhxg | react-router | 2026-10-02 (Fri 02 Oct 10:00) | KS-528 | KS-528 | MIG-1 |

At #1027's head `d7fc6cc55` the drafter parsed 32 rows: rows 5 and 7 are gone, and the other 9 dated rows are unchanged.

**Tickets (Linear, read 20:09:56 AEST):**
- KS-1211 In Progress. Last comment `e3962516`, naming #1027. The §5f live sweep is owed on mcp-server AND originate.
- KS-763 In Review. Last comment `e4f6e304`, Kam's mysql2 ruling.
- KS-528 In Progress. Last comment `77f02686`, the re-date to 2026-10-02.
- KS-530 Backlog. Last comment `87d66048`.
- KS-729 In Progress. Last comment `fcfa72c2`, Kam's ip-address ruling.
- KS-775 In Progress. Last comment `184d5e6c` (2026-09-04); the qs comment PR-4 owes is not posted yet.
- KS-1214 Backlog, 0 comments. Filed by your predecessor; not your lane to fix.
- KS-1024 Done and archived 2026-09-13; it refuses comments.

**Open PRs touching your files** (GitHub REST, 20:09:14 AEST, 21 open):
- #1027 is the only open PR on `audit-baseline.json`.
- The root `Blockchain/Dev/package-lock.json` is also touched by Dependabot #945-#949, #649, #639, #635, #575 and #572. The root `package.json` is also touched by #945 and #920.
- **Never touch or close any of them.**

## TIME-BOUND (the fuse; read this twice)
`isLapsed` is `expires <= utcToday()`, so a row dies at 00:00Z on its date = 10:00 AEST. **When any row lapses, preflight legs 6 (audit-gate) and 7 (audit-locks) refuse EVERY push that touches `Blockchain/Dev`: yours, Seat A's, Kam's, Peter's and Stuart's.** Weekdays derived with `date -j`.
- **Thu 24 Sep 2026, 10:00 AEST:**
  - rows 1 and 2 (qs, PR-4);
  - row 3 (mysql2, PR-7);
  - row 4 (vitest, PR-3b);
  - and rows 5 and 7 (bbm, js-yaml HIGH) if #1027 has not merged.
- **Wed 30 Sep 2026, 10:00 AEST:** rows 13 (react-router-dom, PR-5), 14 (@hono/node-server, PR-6) and 15 (ip-address HIGH, PR-8).
- **Fri 02 Oct 2026, 10:00 AEST:** rows 11 and 12 (react-router, MIG-1, planned landing Thu 01 Oct). **If MIG-1 will slip past 01 Oct, mail Wednesday before Thu 01 Oct 10:00 AEST with the measured reason.**
- **STATUS due Mon 21 Sep 18:00 AEST.**
  - Subject: `[Secuura/Blockchain -> Wednesday] STATUS: 24 Sep rows progress (Seat B)`.
  - One line per row 1, 2, 3, 4, 5 and 7: merged (squash sha), or PR number + head + gate state, or not started. For each, give your projected landing against Thu 24 Sep 10:00 AEST.
  - **If the serial lane cannot land a row in time, name the row and the reason, with your measured time per PR.**
- **If a Sep-24 row is still not merged-fixed by Wed 23 Sep 12:00 AEST,** send a second STATUS naming it (carried from your predecessor's brief).
- **In every outcome you never re-date and never remove an unfixed row.** A re-date is Wednesday's or Kam's instruction, never your choice.

## QUEUE (in order; every write gated on the previous step's rc)
**Lane rule:** every item edits `audit-baseline.json` and rewrites the root lock. So **at most ONE of your PRs is open at a time** (this replaces the "at most 3" in your predecessor's first brief, per the 07:24:18Z and 09:23:02Z mails quoted below). Build the next one locally while the open one is gated, and **push only after the open one's MERGED receipt, with develop merged in** (merge, never rebase, never cherry-pick). Then re-measure both gates on the merged head.

1. **#1027 (KS-1211, PR-3a) on its GO.**
   - The GO is a signed mail with subject `[Wednesday -> Secuura/Blockchain-B] GO: #1027`. **The tier is 2 PROVISIONALLY** (Wednesday 10:04:47Z): the gate drafter is measuring whether js-yaml or bbm installs in any `--omit=dev` image. If either ships, it becomes tier 1 and Wednesday says so first.
   - **Pre-step:** re-read heads (#1027 and develop) from origin, judging any develop move by content. `attachmentsForURL(pull/1027)` must be KS-1211 `contributes` only, with 0 closing phrases.
   - **Merge:** REST squash with the `sha` pin. The merge CONTENT decisions in the GO (predicted tree, blob targets) stand as written. **If develop has moved onto a file the GO names, STOP and ask.**
   - **After the merge:** verify parent, tree, files and blobs at origin, and re-measure audit-gate and audit-locks (rc 0). KS-1211 stays In Progress. Post ONE facts comment, then mail `MERGED: #1027 (Seat B)` with the merge SHA read from origin and the comment id.
   - **Not fixed by #1027, and named in its body:** `mobile/secuura-app` js-yaml 3.14.2 / 4.1.1 (HIGH range) and bbm 2.9.14. It stays out, per the 07:10:25Z Q2 ruling.
2. **PR-3b vitest (row 4, KS-1211), TIER 2 unless the issuer bundle moves.** The recipe is Wednesday's 09:31:55Z ruling (a), quoted in full under RULED BY WEDNESDAY. In order:
   - **Measure `frontend/issuer` FIRST.** If vite, rolldown, lightningcss or anything in its build path moves, **STOP and ask** before touching any other lock.
   - Locks carrying `@vitest/coverage-v8`: `npm install vitest@^4.1.11 @vitest/coverage-v8@^4.1.11 --save-dev --package-lock-only` (2 manifest ranges each, named in the body). All other locks: `npm update vitest`. Both run in the bounded container.
   - Every OTHER entry that moves must be `dev`-flagged and satisfy its declarer's range, verified by parse per lock and listed in the body. **0 entries leave `dev`**, proven by a planted-flag control that fires.
   - Run the Q3 consumer (`systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts:96-100`) on 4.1.10 (control) AND 4.1.11, and quote both parsed summary lines. If the 4.1.11 parse fails: STOP, STATUS, no push.
   - After a real `npm ci`, run the harness `npm run quality` for **every systemTest lock the PR touches** (your predecessor named api-explorer and performance) and quote the results. Whether all four gates bind is OPEN item 1.
   - Your predecessor's measured basis and scratch copies are in `2026-09-17_seatB-audit/pr3-devtools/` and `pr3-devtools/scratch/`. Re-measure at the tip; never quote them as current.
   - Landing target: before Thu 24 Sep 10:00 AEST. `Refs KS-1211`, never Closes.
3. **PR-7 mysql2 override (row 3, KS-763), TIER 1.** Kam ruled `override` (18:31:30 AEST). Recipe from Wednesday 08:32:26Z:
   - `"mysql2": "3.23.1"` in `overrides` of `services/originate/package.json` AND `Blockchain/Dev/package.json`;
   - regenerate both locks in the bounded container; run originate's unit suites and a `prisma generate` smoke inside the container (allowed, no image build);
   - remove row 3 once both gates read it gone.
   - The body states Kam's ruling, and that prisma's MySQL path is unused: re-measure imports = 0, with a positive control.
   - This is the first override that contradicts a declarer's EXACT pin (prisma pins 3.15.3). `Refs KS-763`.
4. **PR-4 qs ×2 (rows 1-2, KS-763), TIER 1.** RULED IN by Wednesday (07:24:18Z):
   - express 4.22.3, in range;
   - the body-parser `overrides` value 1.20.6 → 1.20.8 in the 20 manifests (KS-531's own rule).
   - **KS-775 stays open and untouched.** The PR body and ONE KS-775 comment say exactly: *"qs rows fixed in range on express 4; the express 5 migration ruled 2026-09-03 is unchanged"*.
   - `Refs KS-763`.
5. **PR-5 react-router-dom 6.30.6 (row 13, KS-528), TIER 1.** Package and lock files only, across the 3 portals and root. **MIG-1 would make it redundant; it still lands first** (08:59:16Z item 3). `Refs KS-528`.
6. **PR-6 @hono/node-server (row 14, KS-530), TIER 1.** Recipe from Wednesday 07:28:49Z:
   - mcp-server `@hono/node-server` → 1.19.17 (in range);
   - a LOCK-ONLY move of prisma / @prisma/client / @prisma/adapter-pg to 7.10.0 in originate and root (0 manifests, all inside `^7.8.0`);
   - originate's unit suites and a `prisma generate` smoke in the container.
   - **Do NOT touch or close Dependabot #949**; state in the body that #949 becomes redundant on merge.
   - That ANSWER predates PR-7, so its line "prisma 7.10.0 still pins 3.15.3" now reads: **re-measure by parse that PR-7's override still resolves mysql2 3.23.1 after the prisma lock move, and that row 3 stays gone** (drafter's reading).
   - `Refs KS-530`.
7. **PR-8 ip-address override (row 15, HIGH, KS-729), TIER 1 + a real-browser pass on the issuer portal** (the gate drives it). Kam ruled `override` (18:31:18 AEST). Recipe from Wednesday 08:32:26Z:
   - `ip-address: ^10.3.1` in `overrides` of `frontend/issuer/package.json` AND the root manifest;
   - regenerate in the container; run the issuer build and unit suites; remove row 15.
   - Your predecessor's tarball diff (`2026-09-17_seatB-audit/row15/`) is the evidence basis.
   - A wallet flow needing a stack is stated NOT run. `Refs KS-729`.
8. **MIG-1 react-router `^7.18.4` (rows 11-12, and row 13 if PR-5 has not landed; KS-528), TIER 1 + a real-browser pass on all three portals, including the issuer lazy-route transition.**
   - Planned landing Thu 2026-10-01.
   - Spec: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/REACT_ROUTER_V7_SIZING.md` §6 (read-only; read it whole before building).
   - **Pin `^7.18.4`, never `@latest`** (that is v8). Regenerate locks in the container (a host install dropped 28 platform entries in the sizing trial). `Refs KS-528`.
   - **Build nothing under `src/**` until OPEN item 2 is answered.**

**For every PR** (carried from your predecessor's brief, still binding):
- Branch `feature/ks-<ticket>-<slug>` from develop, re-read first.
- **Verify every lock by parse, never by rc**, with parsed before → after per lock. Scope control: diff the parsed `packages` maps; only the target family may move, except the named exceptions.
- Remove a row only in the PR whose merge makes the advisory absent from EVERY lock, measured with `AUDIT_BASELINE_PATH=<copy without the rows> node scripts/audit/audit-gate.mjs` and `… audit-locks.mjs`, both rc 0, with the real baseline as the control. Assert conservation in the body (rows before N, after N−k, 0 added, 0 other rows altered).
- **Tests:**
  - `npm test -w <member>` for each member whose tree moved, plus `packages/shared`;
  - `tsc` where a type package moved;
  - `lockfile-cleanroom.sh` for each standalone lock it can reach (it SKIPs mcp-server; say so);
  - the full pre-push preflight.
  - Workspace suites run against the ROOT lock's hoisted tree; say so in NOT run.
- Push, POST-PUSH CHECKS, then open the PR. The body carries: the Linear URL, `Refs`, the row table, Test Evidence (Touched / Ran / NOT run / Migrations+config) and the Claude Code footer.
- Comment on the ticket naming the PR. Send `READY FOR QA: #<n> <ticket> @<head sha> (Seat B)`, with the head read from origin in the same action and what was NOT covered. **Wednesday's RECEIVED sets the tier.** Wait for the GO.

## OPEN (ask at plan confirmation)
1. **systemTest rule 2.** `systemTest/CLAUDE.md` rule 2 (line 465 at `19f1e5475`: *"Creating OR updating a systemTest PR → run ALL FOUR full gates"*) names no stack. Schemathesis's gate is `python3 scripts/run.py quality`; Playwright, Performance and Akto use `npm run quality`. Does rule 2 bind PR-3b (and any later PR touching a systemTest lock), or does the 08:19:42Z standing rule (the touched harness's gate) suffice? **Measure first which of the four run without a stack, and put that in the question.** Not ruled in any ANSWER so far (Wednesday 09:31:55Z item 2).
2. **MIG-1 source scope.** Three lines point different ways, so ask rather than choose:
   - The sizing's §6 partition gives MIG-1 `frontend/{admin,issuer,verifier}/src/**` (about 23 files) and says *"built by one source-scope seat"*.
   - Wednesday's 08:32:26Z ANSWER said *"The migration (source work, 3 portals) goes to a separate Claude seat"*. Wednesday's 08:59:16Z ANSWER then queued MIG-1 to Seat B, and the later mail governs the queue.
   - Your write-scope hold is package, lock and baseline files only.
   - The question: is this seat authorised to write MIG-1's `src/**` partition, or does Wednesday hand MIG-1 to a source-scope seat? Nothing under `src/**` until answered. Not blocking: MIG-1 is last.

## POST-PUSH CHECKS (after EVERY push)
- **End orphan login stubs by verified pid only** (KS-1201 leaves about 4 per push). Use `2026-09-17_seatB-audit/push/stop_push_stubs.py` (WT1, `WT` at line 7) or `push/stop_push_stubs_wt2.py` (WT2), with your push-start file. Read `WT` before each run and keep its output in your own records.
  - `CONTROL: ps rows parsed N` must be well above 0.
  - Never pattern-kill. Stubs with cwd in `raise-0916-a` are Seat A's.
  - Put the count in the READY.
- **Re-read `attachmentsForURL(pull/<n>)`** until every ticket reads `contributes`, with 0 closing phrases.
- Read the push rc as `git push … > <records>/push.out 2>&1; rc=$?`, then read the file. The Bash tool is zsh.

RULED BY KAM, NOT YET IN AN ARTEFACT
Source: `decision_queue.sh list ruled --undelivered secuura-`, read 20:07 AEST, rc 0: **22 cards, and none of them is this lane's.** All four of Seat B's cards are marked delivered, each read at source by Wednesday. **Do not repost them.**
- `secuura-audit-baseline-rows-lapse-24sep-block-pushes` → `measure` (panel 16:37:15 AEST): *"Measure, then you decide per row"*. Kam's note, 16:37:41 AEST: *"why not fix it completely now?"* Delivered: KS-1211 `0ec33ad8` and KS-763 `b953f63d`.
- `secuura-audit-row-mysql2-override-vs-prisma-pin` → `override` (18:31:30 AEST): *"Override to mysql2 3.23.1 (recommended)"*. Delivered: KS-763 `e4f6e304`.
- `secuura-audit-row-ip-address-high-override` → `override` (18:31:18 AEST): *"Override to ip-address 10.3.1 (recommended)"*. Delivered: KS-729 `fcfa72c2`.
- `secuura-audit-rows-react-router-v7-migration` → `migrate-and-date` (18:31:25 AEST): *"Commission the v7 migration AND date both rows to its planned landing (recommended)"*. Delivered: KS-528 `79481ed3`.
- **PR-7's body states Kam's mysql2 ruling** (Wednesday 08:32:26Z). Carry the matching ruling verbatim, with its time, in PR-8's and MIG-1's bodies too (drafter's reading, from the first brief's "one line in each PR body").
- **The 22 undelivered cards are other lanes or earlier sessions. Noted only; do not act.** One of them bears on this lane as precedent only: `secuura-four-advisories-ruled-after-measurement` → `bump` (2026-09-09): *"Bump the pins instead of accepting them - removes the vulnerable code rather than recording a decision to live with it (Recommended)"*. The other 21:
  - `secuura-agent-github-identity`
  - `secuura-dependabot-triage`
  - `secuura-ks229-disclosure-mailbox`
  - `secuura-ps-759-760-merge-owner`
  - `secuura-demo-kam-admin-default-password`
  - `secuura-f5-login-limiter-bypass`
  - `secuura-f5-demo-exposure-probe`
  - `secuura-f5-demo-interim-mitigation`
  - `secuura-demo-admin-transcripts`
  - `secuura-demo-admin-mfa`
  - `secuura-891-workflow-scope-merge`
  - `secuura-force-push-own-branch-standing` (it does not apply: every branch you push has an open PR; no force pushes)
  - `secuura-org-trust-boundary-within-tenant`
  - `secuura-archive-fifteen-platform-s-tickets`
  - `secuura-advisory-gate-moving-set`
  - `secuura-advisories-high-and-prod-reaching`
  - `secuura-required-approvals-zero-after-the-untick` (if it flips mid-run, a merge is refused: STOP at that step and mail)
  - `secuura-ks998-format-gate-fails-open-on-missing-deps`
  - `secuura-ks1011-stack-marker-unknown-on-restore`
  - `secuura-ks1081-two-env-templates-which-is-canonical`
  - `secuura-ks1168-ilike-search-on-encrypted-pii`

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
Each line is quoted from its mail, with the mail's destination timestamp (from your predecessor's `2026-09-17_seatB-audit/mail/in-*.json`). Where two conflict, the later wins, and the supersession is stated.
- **Order (08:59:16Z, extending 08:32:26Z and 07:24:18Z; final form in the handover):** *"#1027 (PR-3a, READY) → PR-3b → PR-7 → PR-4 → PR-5 → PR-6 → PR-8 → MIG-1."* The 08:59:16Z mail: *"This EXTENDS the queue order in Wednesday's 08:32:26Z ANSWER: it inserts items; nothing already in that order is reordered or dropped."* The 09:31:55Z mail split PR-3 into PR-3a (#1027) and PR-3b.
- **One root-lock PR at a time (07:24:18Z, restated 08:32:26Z):** *"One root-lock PR open at a time; lock conflicts regenerated, never hand-merged — agreed."* And (09:23:02Z): *"two open PRs on `audit-baseline.json` make each gate's guarded-path pin refuse (rc 18) when the other merges. That cost a re-pin on #1022 today."*
- **PR-3b vitest, ruling (a) (09:31:55Z):** *"Vitest (a) is RULED: the in-range subtree refresh is accepted as a second NAMED exception to the scope rule, for dev-only test tooling"*, with these guards:
  - *"every OTHER entry is `dev`-flagged in its lock AND satisfies its declarer's range, verified by parse per lock and listed in the PR body"*;
  - *"locks with `@vitest/coverage-v8` take the `npm install vitest@^4.1.11 @vitest/coverage-v8@^4.1.11 --save-dev --package-lock-only` route (2 manifest ranges each, named in the body); the others take `npm update vitest`"*;
  - *"frontend/issuer is measured FIRST, and if vite, rolldown, lightningcss or anything in its build path moves, STOP and ask. A moved shipped bundle is outside the exception"*;
  - *"added guard: 0 entries leave `dev` (no dev→prod, no devOptional→optional flag change), with a planted-flag control that fires"*;
  - *"the tier is 2 through-code unless frontend/issuer's bundle moves, in which case it becomes tier 1 with a real-browser pass"*;
  - *"landing target before Thu 24 Sep 10:00 AEST (row 4 expires then)"*.
- **Q3 consumer (07:47:03Z):** *"run the same suite once on the base lock (4.1.10) in the same worktree state and quote its parsed line too"*. And: *"If the parse fails on 4.1.11: STOP, STATUS, no push. No test-file change in any outcome"*.
- **Harness quality, standing (GO #1021, 08:19:42Z):** *"From now on, every Seat B PR that touches a systemTest harness lock runs THAT harness's `npm run quality` (after a real `npm ci`) before its READY and quotes the result"*.
- **qs fixed in range (07:24:18Z):** *"fix qs in range now (express 4.22.3 in range, the body-parser override value 1.20.6 → 1.20.8 in the 20 manifests, satisfying KS-531's own rule), and KS-775 stays open and untouched."* And: *"PR-4's body and one KS-775 comment say exactly that"*.
- **react-router date (08:59:16Z):** *"planned landing is Thu 2026-10-01, and rows 11 and 12 … move to `expires: "2026-10-02"`"*. And: *"Pin `react-router@^7.18.4`, never `@latest`"*. And: *"TIER 1 with a real-browser pass on all three portals."* And: *"If MIG-1 slips past 01 Oct, mail Wednesday before 01 Oct 10:00 AEST with the measured reason. Do not re-date again on your own"*. The same mail SUPERSEDES the 08:32:26Z line that the migration *"goes to a separate Claude seat"*, as to the queue. The source-scope consequence is OPEN item 2. (#1022's GO cites this mail as 08:59:15Z; the destination timestamp is 08:59:16Z; same mail.)
- **PR-7 / PR-8 recipes (08:32:26Z):** quoted in QUEUE items 3 and 7.
- **PR-6 recipe (07:28:49Z):** *"Do NOT touch or close Dependabot #949; state in the PR body that #949 becomes redundant on merge (who closes it is not yours)."*
- **Mobile lock out of scope (07:10:25Z, restated 09:31:55Z):** *"CONFIRMED: no bump in `mobile/secuura-app`"*. And: *"stays out per your Q2 ruling. Keep it named in PR-3a's body as not fixed, with the reason."*
- **Root-lock flag drift (07:34:31Z):** *"Later root-touching PRs (PR-3..PR-6) merge develop in after PR-1 lands and should then see 0 drift; if they do not, STATUS it."*
- **Registry reads (07:10:25Z):** *"registry reads AUTHORISED, exactly (a), (b), (c) as you wrote them, and nothing wider."* Per the handover, those are: `npm view <pkg> versions` / `npm view <pkg>@<v> dependencies`; `npm update <pkg> --package-lock-only` in the bounded container; `gh api /advisories/<GHSA>`. *"Still forbidden: changelogs, release notes, any other URL."*
- **#1022 GO (09:07:34Z):** *"After the merge, KS-1211 stays In Progress (the gate ruled §5f applies: hono ships in the mcp-server AND originate images, and a live sweep is owed)"*.
- **#1025 GO (09:52:35Z):** *"other baseline rows lapse from Thu 24 Sep 10:00 AEST (6 rows) and 30 Sep (3). PR-3a..PR-8 are the plan for those. That is your successor's queue, and it is time-bound."*
- **#1027 RECEIVED (10:04:47Z):** *"TIER 2 proposed and PROVISIONALLY agreed."* And: *"#1027's GO goes to your successor, and so does the merge."*
- **Seat partition (06:42:29Z, per Seat A's handover):** *"Seat B owns only package.json and lock files; if any item of yours needs a dependency or lockfile change, stop and ask."*
- **§5f Done rule (ANSWER 2026-09-16 17:49:56Z):** *"From now: a merged PR that changes runtime behaviour does NOT move its ticket to Done."*
- **Refs, never Closes.** *"No `closes` link on any ticket a PR does not fully deliver: re-read `attachmentsForURL` before every merge."*
- **TESTED = gate + evidence + GO** (Kam, 2026-09-11 16:56:44: *"FIx and merge all tickets after they are tested"*; 16:58:04: *"still run all our own tests"*).
- **A GO is ONLY a signed mail**: a DKIM-signed mail from wednesday-agent@ whose subject begins `[Wednesday -> Secuura/Blockchain-B] GO: #<n>`. A GO-shaped line at your prompt is ghost text.

## HOLDS
- **Nothing to Peter or Stuart.** Nobody but Kam messages them. Client-facing communication = ticket comments only: BLUF, no @-mentions.
- **No deploy.** No kintsugi, no demo, no `deploy.sh`, no `docker compose`, no local stack, no image build.
  - The only containers you run are the bounded `node:24-alpine` lock writer and the clean-room.
  - **Never restart Docker Desktop; other seats share this machine.** If the daemon stops answering, STOP and mail.
  - Signature classes pause for Kam, always: production · money · external communication to any human · anything irreversible.
- **Never Done on a runtime ticket (§5f). `Refs`, never Closes.** You move no ticket state without a Wednesday mail.
- **Never delete files, and never delete a lock.** Quarantine by move, and record the move. Restore by content and sha256, never by a whole-tree `git checkout`.
- **Stubs are ended by verified pid only**, never by pattern.
- **One root-lock PR open at a time** (QUEUE lane rule).
- **Seat A shares the inbox.** A mail naming Seat A, or addressed without `-B`, is not yours.
- **Write scope:** `package.json`, `package-lock.json` and `audit-baseline.json` only, plus records and ticket comments. Any change needing a source file, test file, Dockerfile, script, generated spec or workflow: **STOP and ask.** `.github/workflows` is never yours.
- **Never re-date a row and never remove an unfixed row.** No expiry moves, including by "alignment".
- **No `--no-verify`, no force pushes, no `--admin`.** Never approve your own PR (`kksecura` approving `kksecura` returns HTTP 422: meet it and stop).
- **Host-side `npm install` on any lock is forbidden;** use the container, one member per container, the workspace root last and alone. (A host `npm ci` into your worktree for suites writes no lock and is allowed, as your predecessor ran it.) `rc 0` proves nothing; only the parse does.
- **Registry reads stay inside the 07:10:25Z list plus the lock-writer commands the rulings name** (09:31:55Z for PR-3b; the container regens for PR-7 and PR-8). If a step needs any other network read, say so in a QUESTION first.
- **Before filing any ticket,** search the board by GHSA id, package name and path, and say what you searched.
- **A control must be able to fail. Ratios, never "all". "What did my branch change" is `git diff origin/develop...HEAD` (three dots).**
- **Usage.** `fleet/USAGE_STOP` reads 90. If Wednesday mails you to wind down: finish the step in flight, mail its state, wrap.
- **At 80% context:** finish the step in flight and write `5_Project_History/HANDOVER-seatB-successor1-2026-09-17.md` in your project, with a FINAL STATE block and the lapse dates. Wrap by mail to wednesday-agent@. **Do not start a regen you cannot finish before 88%.**
- **If a line in this brief looks wrong at source,** say so in a QUESTION. While blocked, re-check the inbox every ~3 minutes, and only for mail that is yours.

## LOCKFILE PROCEDURE (from your predecessor's brief; the project's record wins)
- **Write command:** `npm install --package-lock-only --ignore-scripts --no-workspaces`. But `npm install --package-lock-only` does NOT bump a satisfied transitive; use `npm update <pkg> --package-lock-only`. An `overrides` entry does NOT invalidate an existing lock (*"reports 'up to date' and leaves the pin"*), so PR-7 and PR-8 must prove the move by parse.
- **Mounts:** per directory vs repo root disagree in the records (a whole-tree mount silently skips standalone locks; `systemTest/performance` needs the root for `file:../../observability`). State the mount per lock and let the parse decide.
- **On macOS, re-read the lock after the container exits** (bind-mount write-back can lag).
- **`services/mcp-server`** is clean-room-SKIPped. Its recorded reason is wrong at source; do not delete the SKIP.

## LESSONS FROM YOUR PREDECESSOR (per its handover and wrap; apply them)
- `npm view pkg@v dependencies peerDependencies` returns an UN-keyed map when one field is absent: use one field per call.
- Lock classes are dev / optional / devOptional / prod. A `dev`-only classifier misfiles devOptional, and that matters for PR-3b's "0 entries leave dev" guard.
- **`npm update` deadlocks on exact mutual peers** (vitest + coverage-v8 is a no-op), and `npm update vitest` refreshes the whole subtree (anchoring: 41 OTHER, including vite 8.1.3 → 8.3.0). That is why the 09:31:55Z routes exist.
- zsh: an unquoted `--include=*.js` NOMATCH aborts grep (quote globs). A variable named `path` IS PATH. `[^\n]` in an ERE bracket is not "not newline".
- **An unquoted heredoc executed a backtick span in a READY mail** (a correction had to be sent). Use `<<'EOF'` plus a python replace.
- mcp-server's only unit test is a placeholder (`expect(true).toBe(true)`); never count it as coverage.
- **A PR-body `Refs KS-n` walks the ticket to In Progress**, even with no id in the branch name. Report it; do not reverse it.
- **Pull the vault before your next vault commit.** Seat A's commit `7f3157c` swept in your predecessor's uncommitted daily-note sections (nothing lost).
- An exit status read through a pipe is the pipe's: `cmd > out 2>&1; rc=$?`.

PROVENANCE:
- FINAL STATE authoritative; #1021 81ee4b729, #1022 ee40d3099, #1025 19f1e5475 merged; #1027 READY d7fc6cc55 successor merges on GO with pre-step; queue order PR-3b to MIG-1; PR-6 recipe (mcp-server 1.19.17, prisma 7.10.0 lock-only); PR-8 override ^10.3.1; lapse dates 24 Sep / 30 Sep / 02 Oct; KS-1211 In Progress with sweep owed on mcp-server and originate; KS-1214 filed; OPEN rule-2 question; registry reads list; tools and worktrees; lessons | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-audit-2026-09-17.md | read 2026-09-17
- wrap 10:04:55Z spf/dkim/dmarc pass; develop 19f1e5475 at wrap; rows 1-4 lapse Thu 24 Sep and 13-15 Wed 30 Sep; comments KS-1211 x5, KS-763 x2, KS-528 x4, KS-729 x1; launcher warnings F-02 and KS-907; worktrees left clean | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/seatB_wrap.md | read 2026-09-17
- develop = 19f1e54750ce2b65312a687add2db4f5628edb7d; #1027 head d7fc6cc5582b918c0773ec6f25f86407de6f86ab; #1021 742e1c608, #1022 ff49d0242, #1025 9954a7069 | `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop refs/pull/1027/head refs/pull/1025/head refs/pull/1022/head refs/pull/1021/head` at 20:08:55 AEST, develop and #1027 re-read 20:16:15 AEST unchanged | read 2026-09-17
- 21 open PRs; #1027 open, not merged, base develop, mergeable true, 10 files (9 locks + audit-baseline.json); only #1027 touches audit-baseline.json; root lock also touched by #945-#949, #649, #639, #635, #575, #572; root package.json also by #945 and #920; #1021 #1022 #1025 merged with squash shas 81ee4b729 ee40d3099 19f1e5475; #1018 and #1026 are Seat A's | GitHub REST `GET /repos/Secuura/Distributed_Secuura/pulls?state=open` and `GET /pulls/<n>` and `GET /pulls/<n>/files`, token GH_TOKEN by name from the Secuura 4_Credentials .env, drafter script /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/430a6175-31ee-4c21-bf1d-f73226d5ecde/scratchpad/sb1/gh_read.py (.out beside it) 20:09:14 AEST | read 2026-09-17
- baseline at 19f1e5475: 34 rows, 11 dated rows with GHSA, package, ticket field and expires as tabled; at d7fc6cc55: 32 rows, w5vr and 2883 gone, other 9 unchanged; d7fc6cc55 parents b51ed77e1 + 19f1e5475 | `git show 19f1e5475:Blockchain/Dev/scripts/audit/audit-baseline.json` and `git show d7fc6cc55:...` and `git log -1 --format='%H %P' d7fc6cc55` in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, parsed with python3 20:1x AEST | read 2026-09-17
- ticket states: KS-1211 In Progress last comment e3962516; KS-763 In Review last e4f6e304; KS-528 In Progress last 77f02686; KS-530 Backlog last 87d66048; KS-729 In Progress last fcfa72c2; KS-775 In Progress last 184d5e6c 2026-09-04; KS-1214 Backlog 0 comments; KS-1024 Done archived 2026-09-13T11:22Z; control KS-999999 not found | Linear GraphQL `issue(id)` read-only, key LINEAR_API_KEY by name, drafter script /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/430a6175-31ee-4c21-bf1d-f73226d5ecde/scratchpad/sb1/linear_read.py (.out beside it) 20:09:56 AEST | read 2026-09-17
- worktrees raise-0917-b-audit HEAD 19f1e5475 porcelain 0; raise-0917-b-audit-2 HEAD d7fc6cc55 porcelain 0; mail/send_mail.py (args subject, body-file, payload-out) and mail/wait_seatb.py exist, no hardcoded records path; push/stop_push_stubs.py (WT = raise-0917-b-audit, line 7) and stop_push_stubs_wt2.py (WT = raise-0917-b-audit-2) exist; tools/ holds regen.py, lockdiff*.py, remove_rows.py, allowed_flag_drift.json; pr3-devtools/3a and pr3-devtools/scratch exist | `git -C <worktree> rev-parse HEAD` and `status --porcelain`, `find` and `grep -n` of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-17_seatB-audit/ tools, push, mail, pr3-devtools | read 2026-09-17
- Wednesday mail destination timestamps 07:10:25Z, 07:24:18Z, 07:28:49Z, 07:34:31Z, 07:47:03Z, 08:19:42Z, 08:21:59Z, 08:32:26Z, 08:59:16Z, 09:07:34Z, 09:23:02Z, 09:31:55Z, 09:52:35Z, 10:04:47Z with subjects | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-17_seatB-audit/mail/in-*.json timestamp and subject fields, cross-checked against the .send.out mtimes in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/ | read 2026-09-17
- plan confirmation ANSWER: registry reads exactly (a)-(c), mobile lock no bump, Q3 condition | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/answer_plan_confirmation.md | read 2026-09-17
- order approved, qs RULED IN in range (express 4.22.3, body-parser override 1.20.8 in 20 manifests satisfying KS-531's own rule, KS-775 untouched, exact comment sentence), one root-lock PR at a time, severity HIGH = js-yaml and ip-address | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/answer_fixability_order.md | read 2026-09-17
- row 14 (a) PR-6 recipe, #949 untouched, prisma 7.10.0 still pins 3.15.3 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/answer_rows_11_12_14_15.md | read 2026-09-17
- flag-drift exception and later root PRs see 0 drift else STATUS | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/answer_root_lock_flag_drift.md | read 2026-09-17
- Q3 consumer path, control on 4.1.10, parse-fail STOP, no test-file change | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/answer_q3_vitest_consumer.md | read 2026-09-17
- Kam rulings relayed: PR-7 mysql2 recipe (overrides in originate and root, prisma generate smoke, imports = 0 re-measure), PR-8 recipe (^10.3.1 in issuer and root, issuer real-browser pass), order, one root-lock PR, migration to a separate Claude seat | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/answer_kam_rulings_1831.md | read 2026-09-17
- react-router date ruled 2026-10-02, landing Thu 01 Oct, MIG-1 after PR-8, spec §6, pin ^7.18.4 never @latest, container regen, tier 1 three portals, slip mail before 01 Oct 10:00 AEST, extends 08:32:26Z order | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/answer_rr7_date_ruled.md | read 2026-09-17
- PR-3b ruling (a) with guards, rule-2 question unruled, mobile lock stays out, vault sweep 7f3157c | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/answer_pr3_regroup_vitest.md | read 2026-09-17
- MIG-1 partition includes frontend admin/issuer/verifier src/** (9+11+3 files), built by one source-scope seat, seats never share files, @latest is v8, host regen dropped 28 entries | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_seatB/REACT_ROUTER_V7_SIZING.md sections BLUF, 5, 6, 7 | read 2026-09-17
- harness npm run quality standing rule for systemTest harness locks | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1021/go_1021.md | read 2026-09-17
- #1022 merge-in never rebase; GO #1022 KS-1211 stays In Progress, sweep names mcp-server and originate, cites the rr7 ANSWER as 08:59:15Z | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1022/answer_1022_mergein.md and /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1022/go_1022.md | read 2026-09-17
- two open PRs on audit-baseline.json refuse rc 18; build and push after merge; GO #1025 other rows lapse 24 Sep (6) and 30 Sep (3), successor's time-bound queue | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1025/receipt_1025.md and /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1025/go_1025.md | read 2026-09-17
- #1027 READY 10:03:30Z content (9 locks, 34 to 32 rows, mobile lock not fixed, Dependabot root-lock overlap); RECEIVED tier 2 provisional, GO and merge to successor | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1027/mail_1027_ready.md and /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1027/receipt_1027.md | read 2026-09-17
- Kam panel verbatim with seconds: measure 16:37:15, note 16:37:41, ip-address override 18:31:18, react-router migrate-and-date 18:31:25, mysql2 override 18:31:30; 22 other-tab messages today scanned, 0 bear on this lane | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` and /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_kam.json filtered by ts and view | read 2026-09-17
- 22 ruled undelivered secuura- cards, none Seat B's; four Seat B cards delivered (0ec33ad8 + b953f63d, e4f6e304, fcfa72c2, 79481ed3) | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` (rc 0, 20:07 AEST) and `decision_queue.sh show <id>` for the four Seat B cards | read 2026-09-17
- original Seat B brief: lockfile procedure, per-PR recipe, post-push checks, 23 Sep 12:00 STATUS, 09-09 authority, TESTED grant 16:56:44 and 16:58:04, §5f 17:49:56Z, no-Closes line, GO signed-mail rule, nothing to Peter or Stuart | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-17_seat_B_audit_rows.md | read 2026-09-17
- Seat A 6th successor live with its queue and worktree raise-0916-a; 06:42:29Z seat partition line; successor brief shape | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-17_raise_seat_A_successor6.md and its .bal.out (launched 19:42 AEST) | read 2026-09-17
- systemTest rule 1 at line 460 and rule 2 at line 465 (ALL FOUR full gates, no stack named) | `git show 19f1e5475:systemTest/CLAUDE.md` in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-17
- weekdays: 2026-09-21 Monday, 2026-09-23 Wednesday, 2026-09-24 Thursday, 2026-09-30 Wednesday, 2026-10-01 Thursday, 2026-10-02 Friday | `date -j -f %Y-%m-%d <date> '+%A'` | read 2026-09-17
- Mon 21 Sep 18:00 AEST STATUS deadline is Wednesday's instruction for this brief; the 23 Sep 12:00 STATUS and the GO-before-ANSWER exception are drafter carry-over and sequencing for Wednesday to confirm | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-17_seat_B_audit_rows.md item 5 and the drafting instruction | read 2026-09-17
- holds and standing lines (signature classes, ticket comments only, no --no-verify, search before filing, never delete, kksecura 422, ratios never all, three-dot diff, pipes) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md | read 2026-09-17
- usage cut 90; gauge 62% | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/USAGE_STOP and `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check` 20:1x AEST | read 2026-09-17
- Secuura/Blockchain-B shares secuura-blockchain@agentmail.to with Seat A, migrated yes (lines 29 and 35) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf | read 2026-09-17
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-17 20:17
