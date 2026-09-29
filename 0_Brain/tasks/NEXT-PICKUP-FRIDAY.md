---
date: 2026-09-27
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, WRAP 2026-09-27 21:5x (Kam: continue Tuesday after his HP meeting)
supersede: replace wholesale; previous = NEXT-PICKUP-FRIDAY.md.pre-0925-rotate-successor2
---

# NEXT PICKUP — FRIDAY

**The tree is at `/Users/kamilkreiser/1FILES TO SYNC/FRIDAY`.** Quote every path (spaces).

## 🔴🔴 HANDOVER 2026-09-29 20:5x (successor seat, ctx 65%) — READ FIRST; supersedes the blocks below where they differ
**MERGED tonight (head-pinned, trees/blobs verified):** HPSM-POC #53 (B55) · #55 (B58) · #54 (B56 content 0.5.0) · #56 (B60 part 1: H2/H5/H7) · #57 (B56 F-1 API) → main **f403251**. Records: analysis #7 (B55), #8 (B56) → analysis main 4495c62. Composer #12 (B22 wizard) → HPSM-light main **a60fc22**.
**LIVE SEATS:**
- **Datasec/Composer-D (%36) = B24 DEPLOY of a60fc22 to the demo VM** (Kam 16:28 "publish … make them live"). Brief `Datasec Security Composer/1_Project_Definition/Briefs/2026-09-29_B24_deploy-a60fc22-to-demo-vm.md`. On READY: verify live yourself (Basic auth; a string only this build has), that the temp NSG rule is gone, then tell Kam with the check; `decision_queue.sh --delivered composer-two-logins-deploy-for-paul-friday <C-number>`. Wake: watch_status `seen_b24`.
- **Composer-C (%18) = B22 ADDENDUM-3:** R2-1 end-page fix on `b22/end-page-r2-1` (tier 2) + BACKLOG R2-2/R2-3. **Its deploy needs Kam's word** (separate).
- **HPSM-POC-E (%32) = B60 round 2 of 2 on PR #58** (ADDENDUM-5: F-1 reset door scores draft ungated; F-2 partial seed; F-3 gitleaks false positive; N-5 approver name on hosted PDF; N-4 pin RequireApprovedRuleset; N-2). Then **HPSM-POC-QA (%34, B62)** re-gates (write a B62 ADDENDUM-1 pinning the new head; cap: a 2nd NO GO ships nothing without Kam).
- **HPSM-POC-QA2 (%35) = B63 tier-1 gate on PR #59** (B59 web: Entra sign-in, standalone, notice, DRAFT labels). Verdict wait `wait_verdict.sh` on B63_STATUS. HPSM-POC-D (%31, B59) kept for its fix round.
- **HPSM-POC-A (%23) = B58 records/b58** (ADDENDUM-1): open + merge its records PR when the branch appears.
**Open Kam card:** `hpsmpoc-hosted-seed-owner` (rec b presenter account; default nothing until D-3). Tickets filed tonight: HPSMPOC-105..112.
**Tooling shipped this seat:** chat_reply unread-rows advisory (1ac298ace) · cockpit ensure_caffeinate (a66e49c6d) · watch_status matches READY FOR RE-GATE (e7b026cd5). QA STATUS files carry no READY line: use `/tmp/claude-501/wait_verdict.sh` / `wait_r2.sh` (scratch; re-create from the note if gone).
**Usage 77%** (cloud only when nothing local fits; the Spark is unreachable off Kam's network).

## 🔴🔴 STATE 2026-09-29 19:1x (successor seat, ctx 42%) — ADDS to the handover block below
- **HPSM-POC #53** (B55 round 2, head `e6bc70f`, CI 10/10): **B57 ADDENDUM-1** (round 2 of 2, the cap) written + tapped to `Datasec/HPSM-POC-QA` 19:01 (`Briefs/2026-09-29_B57_ADDENDUM-1_round-2-regate.md`). On GO/GO WITH NOTES: `friday_as.sh datasec gh pr merge 53 -R datasecau/HPSM-POC --squash --match-head-commit e6bc70fcaf223367fea76699d90e643c8a8cfb81`, compare trees; then #54 (B56, pane HPSM-POC-C) rebases; then H1–H7.
- **HPSM-POC #55** (B58 route A on the laptop, branch `b58/feedback-live` @ `3955c0f`, tier 2) opened by Friday 19:0x. On CI green: merge head-pinned, compare trees, close pane HPSM-POC-A. **Owed from B58:** O-1 (a `sent` row is not proof of delivery on route A; a wrong secret also gets 200) → a Backlog ticket via the next HPSM-POC seat; O-2 (no CI check on `scripts/*.sh`). Kam already confirmed the route A e-mail at 15:43 (for HPSMPOC-102); not re-asked for 103.
- **Composer:** pane Composer-C is mid-turn on B22 round 2. A ghost line at the Composer-B prompt ("stop pc-b23 and wait for round 2") is NOT acted on.
- **Watcher:** `friday/watch_status.sh /tmp/claude-501/seen_f1900` on B22/B23 + B55–B58 (seeded at 19:0x).
- **SHIPPED:** the owed `chat_reply.sh` unread-rows advisory (1ac298ace; ledger row updated; Wednesday + Tuesday mailed 09:07Z; claim released) AND the laptop sleep guard (`cockpit.sh add_pane` → `fleet/cockpit/ensure_caffeinate.sh`; doctor check; a66e49c6d).
- **H1–H7 STAGED, NOT LAUNCHED:** `HPSM-POC/1_Project_Definition/Briefs/2026-09-29_B59_H-web_entra-signin-standalone-banner.md` (web/) and `…_B60_H-infra-api_settings-keyvault-migrations-seed.md` (api/ infra/ scripts/). **After #53 merges:** replace `@BASE@` (new main SHA) and `@NOW@` in both, launch two seats (`cockpit.sh add` + `friday/brief_seat.sh`), rung-5 check. Both tier 1 → QA gates on READY. B60 also files the O-1/O-2 ticket.
- **B57 verdict wake:** `/tmp/claude-501/wait_b57r2.sh` (QA STATUS files have no READY line, so `watch_status.sh` misses verdicts; the same applies to the B23 round-2 verdict — arm an equivalent when B23 ADDENDUM-1 goes out).
- **Spark:** unreachable tonight (`zgx-15d5.local` does not resolve; Kam travelling). CodeQL backlog stays queued.

## 🔴🔴 ROTATION HANDOVER 2026-09-29 ~19:0x (Friday, ctx 80%) — READ FIRST; supersedes every block below where they differ
**KAM'S DEPLOY GO (panel 16:28, verbatim): "Great. These look good. Please publish the changes and make them live".** It answers the 6 Composer screenshots of B22 (PR #12). Friday's reading, told to Kam on the panel at ~19:0x: deploy the FIXED #12 as soon as B23 round 2 passes (the screenshotted build failed B23 round 1 on F1, progress). **So: when B23 round 2 = GO / GO WITH NOTES → merge #12 head-pinned → deploy HPSM-light main to the demo VM per `DEPLOY.md`** (backup before migrate; `remote-update.sh`; temporary access removed and proven; PREFLIGHT; `/site.json`; check the running build live; the C-06/C-08/C-09 pattern). Migrations 0019 + any new ones; the content release is unchanged. Then tell Kam, with the live check, on the panel. If round 2 is NO GO: ship what closed per the cap, ticket the rest, and ask Kam whether to deploy anyway.
**LIVE SEATS (panes):**
- **Composer-C** (B22 round-2 fix, `Briefs/2026-09-29_B22_ADDENDUM-2_gate-findings-round-2.md`) → then **Composer-B** re-gates it (B23 pane, acked; write a B23 ADDENDUM-1 pinning the new head).
- **HPSM-POC-B** (B55 round-2 fix for #53) → then **HPSM-POC-QA** re-gates it (B57 pane, acked; a B57 ADDENDUM-1 pinning the new head). This is the last round. After #53 merges: tell B56 (pane HPSM-POC-C) to rebase #54 and regenerate the contract, B57's seat gates #54, merge; then brief the H1–H7 hosted build (Kam approved at 15:07).
- **HPSM-POC-A** (B58: Route A live on the laptop, R-1/R-3; closes HPSMPOC-102).
**WATCHERS DIE WITH THIS SEAT. Re-arm at boot:** `friday/watch_status.sh <seen> "<glob>"` on:
- `!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-09-29_B2[23]*STATUS*.md`
- `!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-09-29_B5[5678]*STATUS*.md`
Use fresh seen files: counts start from the current READY lines.
**caffeinate** re-armed 18:55 for 6 h (pid 7260). It expired at 14:44 earlier and the laptop likely slept.
**Usage 71%:** cloud seats only when nothing local can do the work and it matters now.
**OWED MECHANISM (ledger 09-29, w=2):** `chat_reply.sh` must show Kam's live rows newer than the last read, before posting.

## 🔴 STATE 2026-09-29 16:3x (Friday, ctx ~78%) — Kam: "thats great. thank you! keep going with the work". SUPERSEDES the 15:3x/15:4x blocks where they differ
- **Usage 71% (> 70%):** cloud seats only when nothing local can do the work AND it matters now (the 09-25 three-tier rule). Queued, low urgency: CodeQL backlog (HPSM-POC #1 `js/bad-tag-filter` in `web/e2e/security.spec.ts:23`; HPSM-POC-analysis #1 in a seat-notes script; HPSM-analysis 115 = 93 http-to-file-access + 22 file-access-to-http in its scripts: a triage report first). These are good Spark tasks when it is up.
- **Composer:** PR **#12** (B22 wizard→E8, head 5e91f84) is at QA gate **B23** (pane Composer-B, seen `seen_composer_b23`). The screenshots are on Kam's Friday tab (6 desktop). **Deploy only after the gate passes AND Kam says "deploy"** (card ruled a at 10:43: "after gate + seen screenshots"; he was asked to say "deploy"). Follow `DEPLOY.md` (backup first). The B22 pane (Composer-C) is kept for fixes.
- **HPSM-POC:**
  - **#53** (B55 follow-up): B57 = NO GO (F-1 return dead-ends after "I'm done"; F-2 the BFF-IP rate-limit bucket). The ROUND 2 fix runs on pane HPSM-POC-B (`B55_ADDENDUM-1`; seen `seen_b55r2`). Then B57 re-gates (pane HPSM-POC-QA, acked): the last round.
  - **#54** (B56 content, DRAFT): after #53, rebase and gate.
  - **B58** (pane HPSM-POC-A): Route A on the laptop (R-1/R-3), closes HPSMPOC-102 (seen `seen_hpsmpoc_w6`).
  - **H1–H7 hosted build:** brief right after #53 merges (Kam approved the plan 15:07).
- **Route A: PROVEN** (HPSMPOC-102 created; the wrong secret created nothing; Kam got the email). Later: advise Kam to Regenerate the secret.

## 🔴 STATE 2026-09-29 15:4x (Friday, ctx ~76%) — ADDS to the 15:3x block
- **Kam APPROVED the hosted plan** (15:07, hpsmpoc-hosted-plan-approve a, "Approve with the seat's recommendations"): build H1–H7 FIRST (B54 plan §6: `Architecture/2026-09-29_hosted-demo-plan-and-cost_FOR-KAM.md`, merged in analysis 4b86480).
  - Then a new RG `hpsm-poc-demo-rg` australiaeast, sub `a6b8fe11-…`, tenant `ec01829b-…`, B1, SQL S2 (~A$49/mo), a A$150 budget, B2B guests, DRAFT scoring on hosted.
  - **Brief H1–H7 right AFTER #53 merges** (H1 Entra sign-in touches `bff.ts` and web auth, which #53 also changes).
  - Tell Kam before creating ANY Azure resource. The deploy happens only when H1–H7 are merged.
- **Route A:** the URL + secret are in HPSM-POC `4_Credentials/.env` (FEEDBACK_AUTOMATION_WEBHOOK_URL/_TOKEN, mode 600).
  - Test: POST 200, but no Jira issue appeared, and a WRONG token also got 200.
  - Waiting on Kam: the flow's on/off state + audit log (asked 15:40, 3 steps on the tab).
  - After it works: a seat does R-1..R-3 (B54 doc §6); then advise Kam to Regenerate the secret (it passed through chat/terminal).

## 🔴 STATE 2026-09-29 15:3x (Friday, ctx 74%) — supersedes the 14:2x blocks where they differ
- **Composer:** main **5b5252c** (#9, #10, #11 merged; 0 open CodeQL alerts, verified at source). **B22** (pane Composer-C) = the wizard follows E8 + the four choices; it rebases onto 5b5252c (ADDENDUM-1). On READY: open the PR (CodeQL) → QA gate (a new seat) → merge → SCREENSHOTS TO KAM on the Friday tab (`chat_reply --file`) → only after Kam has seen them, deploy per `DEPLOY.md` (backup first; the demo VM `remote-update.sh`, as C-06/C-08/C-09 did). Kam's word = card composer-two-logins-deploy-for-paul-friday (a) at 10:43.
- **HPSM-POC:** main **1bcbeb1**.
  - **#53** (B55 client follow-up, head 179cb37, CI 10/10) is at QA gate **B57** (pane HPSM-POC-QA). On GO: merge.
  - **#54** (B56 content 0.5.0 + DRAFT weights + tiers, head f400eb4) is a DRAFT PR. After #53 merges: tell B56 (pane HPSM-POC-C) to rebase and regenerate the contract, then have B57's seat gate it as round 1 (a new addendum), then merge.
  - The records for B55/B56/B57 go by one records branch afterwards.
  - The weights doc (`Architecture/2026-09-29_proposed-weights_DRAFT-FOR-HP-VETTING.md`) goes to Kam as a copy-ready text **in the CHAT** (his rule: steps and formatted text in chat, not email), minus its internal section.
- **Kam's hands:** the Route A Jira rule (19 steps on the Friday tab, 15:05). Then he says "done", and a seat runs R-1..R-3 from the B54 doc.
- **Open cards:** hpsmpoc-hosted-plan-approve (new, 14:3x). Everything else was ruled.
- **Watchers:** `seen_hpsmpoc_w4` (B57 + B22). Idle wakes of held seats are wake_ack'd.

## 🔴 STATE 2026-09-29 14:2x-b (Friday) — Kam's 12 rulings ACTIONED; supersedes the cards list above
- **Ruled today (all reconciled 14:18):** composer deploy (a: deploy after the gate AND Kam has seen the screenshots) · wizard four choices (a) · follow Paul's E8 questionnaire (a: step 1 now, wording later) · 110 (a: "later - keep going") · HPSM-POC follow-up (b: the partner accepts each answer) · principles and sections (a) · feedback route (A: a Jira Automation rule Kam owns) · hosted link (a: plan + cost FIRST, nothing created until he approves) · tiers (a: groupings, no prices) · weights (a: Datasec proposes, HP vets) · transcript gaps (b) · intro video (b: next phase).
- **LIVE:**
  - Composer-A: B20, idle.
  - Composer-B: B21, the QA gate on #11.
  - Composer-C: B22, the wizard follows E8 + the four choices + screenshots; then its PR, a QA gate, SCREENSHOTS TO KAM, and the deploy per DEPLOY.md (backup first).
  - HPSM-POC-A: B54 (C-32, Jira, Route A steps, hosted plan).
  - HPSM-POC-B: B55 (L3 follow-up).
  - HPSM-POC-C: B56 (0.5.0 content + weights + tiers).
  - Contract merge order: B55 then B56.
- **Watcher:** `seen_hpsmpoc_w2` on the B54–B56 and B22 STATUS files; `seen_composer_b21` on the B21 STATUS.
- **RULE (ledger 09-29):** run `kam_rulings_today.sh` in the same action as every card add and every chat_reply.

## 🔴 STATE 2026-09-29 14:2x (Friday, ctx 70% checkpoint) — supersedes the 13:1x block where they differ
- **Composer:**
  - MERGED today: #9 (B16 Guided/Expert) and #10 (B18 gate notes + the CodeQL test fix) → HPSM-light main **cb6f78d**. NOT deployed; DEPLOY.md holds the backup + rollback recipe.
  - **PR #11** (B20: all 20 pre-existing CodeQL alerts fixed; in-app rate limit, 1,200/min, contract 0.19.0; head f23fabf) is at its **QA gate B21** (pane Composer-B, `Briefs/2026-09-29_B21_SEAT-B_QA-gate-PR11.md`; watcher seen file `seen_composer_b21`). On GO / GO WITH NOTES: merge head-pinned and compare trees. On NO GO: the fix round goes to pane Composer-A (the B20 seat, kept open), then round 2 re-gates, and that is the cap.
  - B19's E8 mapping is merged locally (root repo cccbe1b; no remote). It raised card composer-wizard-follow-paul-e8-questionnaire.
- **CodeQL backlog still queued:** HPSM-POC (1 high, a test file), HPSM-POC-analysis (1 high), HPSM-analysis (115 medium, scripts). Brief them after #11 (one HPSM-POC seat for the two small repos; an HPSM seat for a TRIAGE report first on the 115).
- **Ruled today:** composer-paul-110 (a). Kam's CodeQL policy is recorded (lesson + memory, narrowed per Tuesday).
- **Open Kam cards (11):** the 8 HPSM-POC cards, plus composer-two-logins-deploy-for-paul-friday, composer-guided-wizard-four-choices and composer-wizard-follow-paul-e8-questionnaire.

## 🔴 STATE 2026-09-29 13:1x (Friday, ctx 65%) — supersedes the 11:0x block where they differ
- **HPSM-POC:** wave 1 fully MERGED on main **1bcbeb1**: #50 B51 collateral, #52 B50 feedback (delivery OFF), #51 B49 sections. Records: analysis PRs #1–#5, analysis main 4a93311. Floor EMPTY. Next work waits on Kam's cards: L3 client follow-up (HPSMPOC-89), L4 pack 2, the 0.5.0 questions, HPSMPOC-94 remediation (needs Jason O'Keefe content), 95 tiers.
- **HPSM:** B05 merged (analysis #1). Readiness only.
- **Composer:** #9 (B16 Guided/Expert) MERGED → main **6968b7f**, NOT deployed.
  - #10 (B18 gate notes, head ccb3470) is at the RE-GATE: the B17 seat (pane Composer-B) is running round 2 of 2 per `Briefs/2026-09-29_B17_ADDENDUM-1_round-2-regate.md`. On GO or GO WITH NOTES: merge head-pinned, compare trees, and tell Kam it is deploy-ready for Paul (card composer-two-logins-deploy-for-paul-friday; a deploy follows DEPLOY.md: backup before migrate).
  - The B18 seat (Composer-A) is idle, kept for a possible fix.
  - **B19 (Composer-C)** is mapping Kam's E8 questionnaire (HP-branded, git-ignored in Source_Documents) against the 26/123/55. Analysis only; records by branch.
- **Kam emailed today:** HP-4..8 (08:58); Steve's follow-up bullet list (~10:55).
- **Open Kam cards (10):** hpsmpoc-c30-policy-principles-and-sections · -c30-feedback-route · -hosted-link-for-hp · -client-followup-model · -section-intro-video-scope · -weighting-matrix-owner · -transcript-gaps · -good-better-best-tiers-scope · composer-two-logins-deploy-for-paul-friday · composer-guided-wizard-four-choices. (composer-paul-110 was ruled 13:1x.)
- **Watchers:** friday/watch_status.sh on the B17 STATUS (seen file `seen_composer_r2`) and on B19. Re-arm after every wake. The idle wakes of held seats are wake_ack'd.
- Leftover stacks: pc-b16, pc-b17, pc-b18. Quarantine only, never delete.

## 🔴 STATE 2026-09-29 11:0x (Friday) — supersedes the 09:2x block where they differ
- **LIVE SEATS:**
  - HPSM-POC-A (%7): B49 sections, idle by design. Once #52 merges: rebase, add the contract commit, un-draft PR #51, merge.
  - HPSM-POC-B (%8): B50 feedback, FIX ROUND 2 from `Briefs/2026-09-29_B50_ADDENDUM-1_gate-findings-fix-round.md`.
  - HPSM-POC-QA (%10): re-gates #52 at round 2 (the cap: a second NO GO ships what closed and tickets the rest).
  - Composer-A (%11): B16 done; PR datasecau/HPSM-light #9 @ 4bffb38.
  - Composer-B (%13): the B17 QA gate on #9.
- **MERGED today:** HPSM-analysis #1 · HPSM-POC-analysis #1, #2, #3 (records) · HPSM-POC #50 (B51 collateral; main 70eb4f0). The org CodeQL ruleset → every records change goes by PR (a branch + `friday_as.sh datasec gh pr create/merge --match-head-commit`).
- **Kam emailed today:**
  - 5 HP asks (HP-4..8) at 08:58;
  - the consolidated follow-up for Steve at 11:0x (copy block = B53's `Registers/2026-09-29_HP-follow-up-bullet-list_DRAFT-FOR-KAM.md`).
- **Kam cards OPEN (10):**
  - hpsmpoc-c30-policy-principles-and-sections
  - hpsmpoc-c30-feedback-route
  - hpsmpoc-hosted-link-for-hp
  - hpsmpoc-client-followup-model
  - hpsmpoc-section-intro-video-scope
  - hpsmpoc-weighting-matrix-owner
  - hpsmpoc-transcript-gaps
  - hpsmpoc-good-better-best-tiers-scope
  - composer-two-logins-deploy-for-paul-friday (Kam told Paul "end of the week" = Fri 2 Oct)
  - composer-paul-110-questions-source
  - composer-guided-wizard-four-choices
- **Next when rulings land:** L3 client follow-up (HPSMPOC-89) · L4 pack 2 · HPSMPOC-94 guided expert remediation (needs HP's Jason O'Keefe content) · a Composer deploy only on Kam's tap.
- Leftovers: pc-b16 stack (the B16 builder's) · the B52 QA worktrees · `.tools/wt-B53-records`. Quarantine, never delete.

## 🔴 STATE 2026-09-29 09:2x (Friday, drive seat) — supersedes every block below where they differ
**Kam met HP at 07:05 (the meeting was about HPSM-POC, NOT HPSM; Friday's first brief got that wrong and corrected it). Kam is travelling; his words: "continue with the project".**
- **Tree:** /Volumes/Laptop-DEV/FRIDAY (the drive). The 09-28 wrap branch has been picked (f7d9561cc). main is level with origin at each commit.
- **NEW GitHub org ruleset (since ~06:14 today):** main on the datasecau analysis repos requires CodeQL results, so direct pushes are refused (GH013). Records land by PR: the seat pushes a branch; Friday runs `friday_as.sh datasec gh pr create` then `gh pr merge --squash --match-head-commit`, and compares trees. Precedents today: HPSM-analysis #1, HPSM-POC-analysis #1.
- **HPSM:** B05 done and merged (C-79 pointer; SOW-01 HP items list; OneDrive catalogue). Readiness only. Seat's local main diverges from origin after the squash (the next seat fetches and resets its branch; it must not push local main). Brief files B05 and ADDENDUM-1/2 stay UNTRACKED on purpose (they quote the meeting).
- **HPSM-POC:** B48 done and merged (C-30; Jira HPSMPOC-82..92; `Architecture/content/2026-09-29_question-set-aligned-to-policy-principles_DRAFT-FOR-KAM.md`; `Architecture/2026-09-29_meeting-features-design_FOR-KAM.md` with K1..K10 and the lane plan).
  - **WAVE 1 LIVE** (base main b1d3ec9): B49 L1 sections (pane HPSM-POC-A) · B50 L2 feedback, delivery OFF (-B) · B51 L4 collateral packs 1+3 (-C). Contract merge order: B50 then B49. Watcher: `friday/watch_status.sh <seen> ".../Briefs/2026-09-29_B49*STATUS*.md" (B50, B51)`. On READY: review at source, QA gate (B50 is tier 1: new outbound integration), merge head-pinned on green.
  - **L3 client follow-up (HPSMPOC-89)** starts on the ruling or default of card hpsmpoc-client-followup-model. **L4 pack 2** follows L3.
  - **Kam cards open (4):** hpsmpoc-c30-policy-principles-and-sections · hpsmpoc-c30-feedback-route · hpsmpoc-hosted-link-for-hp · hpsmpoc-client-followup-model. Reconcile at every checkpoint.
  - **HP asks HP-4..HP-8** emailed to Kam 08:58 (5 mails; register updated; HP-3 reversed: we propose the questions).
  - **Open question to Kam:** "Feedback board on chat" = the Friday tab or the Teams chat? Default: the Friday tab.
  - **OWED from Kam:** the full meeting transcript (download requested). When it arrives, a seat records the rest in HPSM-POC C-30's successor.
- caffeinate pid 46889 (6 h from 08:44).

## 🔴 FIRST, EVERY BOOT AND EVERY CHECKPOINT
- `kam_rulings_today.sh`, then `python3 2_Project_Files/tools/reconcile_rulings.py` (then `--apply`).
- The live-board wake is `fleet/cockpit/live_chat_poll.sh --seat friday` (armed by the shared launcher). Kam's posts arrive as "[Wednesday tap] [live-board] …".
- **Before ANY `git pull` of this tree: commit Friday's own data files first** (decisions.json, chat_friday.json, usage_friday.json, .spoken.log, the note). When committing, use `git commit -- <paths>`: other tools stage chat_tuesday/chat_wednesday.json, and those are not Friday's.
- STATUS wake: `2_Project_Files/friday/watch_status.sh <seen-file> "<glob>"`. It keys on the COUNT of READY lines, so a seat that re-saves a finished STATUS will NOT re-fire it; check idle panes.
- Unregistered project folder (HPSM: its launcher needs DevMASTER) → `cockpit.sh add <Name> "bash '…/2_Project_Files/friday/brief_seat.sh' <client> '<dir>' '<brief>'"`. Register the pane name in `fleet/inbox_routing.conf` BEFORE a `say --mail` tap: without a line, say --mail exits 1 SILENTLY (the fix is owed).

- **The LAPTOP SLEEPS.** Arm `caffeinate -dims -t 21600` (background) in the same action as launching any seat, and check `pgrep -fl caffeinate` at boot. On 09-25 it slept at ~17:0x and cut two seats' turns. One was armed at 17:4x until ~23:4x.

## 🔴 DRIVE MOVE 2026-09-28 (Kam, travelling this week) — read before anything else
- Kam: "move all your files and all project files to this drive". DONE and checksum-verified 20:5x: `/Volumes/Laptop-DEV/FRIDAY` (this tree), `/Volumes/Laptop-DEV/!CODING/Datasec/{HPSM, HPSM-POC, Datasec Security Composer}`. Laptop copies under `~/1FILES TO SYNC/` are UNTOUCHED (never delete; Kam decides).
- **The drive is the new home**: launch Friday from `/Volumes/Laptop-DEV/FRIDAY/Launch_Friday.command`. The laptop tree is now stale the moment the drive seat writes; do not run both. Friday's cockpit rows for HPSM-POC/Composer already point at the drive (launchers.conf, commit 27a0750f0).
- NOT copied: `HPSM-POC/.tools/` (68 GB of scratch worktrees, work all merged; a partial 15 GB copy sits on the drive). Their `.git` files point at laptop paths (absolute gitdir); if they matter, a seat runs `git worktree repair` there. Copy the rest on a quiet night if Kam wants.
- The drive's OLD HPSM (pre-SOW-rewrite repos) is quarantined at `!CODING/Datasec/_quarantine_2026-09-28_HPSM-drive-sync-copy/HPSM` (old HPSM-light push URL disabled). Drive-only files brought INTO the new HPSM: `1_Project_Definition/Source_Documents/OneDrive_1_12-08-2026/` (6,244 HP files + zip, git-ignored), `3_Access_Keys/` (8 keys, 0600), `4_Credentials/` policy-composer-*.env + `.azure`; the one conflicting log kept as a second copy. Categorise/read the OneDrive dump for HPSM use in the next HPSM seat's brief.
- **WRAP 2026-09-28 ~21:3x:** the drive was EJECTED before the wrap commit, so the drive copy lacks tonight's last note lines and this line. They are pushed to origin branch `friday-wrap-2026-09-28`; at the first drive boot, after committing own files and pulling main, merge that branch (it only touches Friday's note, pickup, history and chat/usage data). Resume plan unchanged: Tuesday after Kam's 07:05 HP meeting. Kam is TRAVELLING this week. Attachment mails to Kam land in his junk folder: say so on the panel and put a drawer copy too.
- Local main was 136 behind origin at 20:0x; pull (own files committed first) at the first drive boot.

## 🔴🔴 DAY INSTRUCTION, live until end of SATURDAY 2026-09-26 — `tasks/WEEK-INSTRUCTION-FRIDAY.md`
Kam (terminal ~08:0x, verbatim): "Yes, please keep going for the day. I'll be out all day, so just keep working on getting the product ready and refined." = Datasec/HPSM-POC. Still his: deploys, anything to HP/humans, money, template text + validator/rule changes, irreversible. Usage 71% at 09:50: cloud seats only when nothing local can do it AND it matters now; Spark first.

## 🔴🔴 RESUME TUESDAY 2026-09-29, AFTER KAM'S HP MEETING (07:05) — Kam 21:5x Sunday, verbatim: "If you have done everything that can for now, please wrap up. and we will continue the work on tuesday after I have met with HP"
**Wrapped clean on Sunday night. The floor is empty, and caffeinate has been stopped on purpose.** Nothing runs Monday unless Kam says so (this is his instruction, not a gap).
**Tuesday, first work:** read Kam's panel messages for what HP said, then turn his answers into briefs. What his answers unblock:
1. **HPSM (readiness-only until he says the build starts):** the clinic pack `HPSM/1_Project_Definition/Architecture/2026-09-29_HP-meeting-clinic-pack_FOR-KAM.{md,pdf}` covers HPSM-15/28/31/38. **HPSM-37 is Kam's to rule after Tuesday's review** (card hpsm37-scoring-model-accept, ruled b: he rules it). SOW-01 = a verbal start, terms in negotiation (C-78). Record whatever HP said as HPSM's next C-number, via a seat.
2. **HPSM-POC:** 32 open tasks + 9 epics (board_count 21:4x); all wait on Kam's decisions, HP/SME content (HP-1 corrected deck slides, HP-2 IDC s91 permission: register `0_Brain/reference/2026-09-27_hpsmpoc-hp-requests/HP_REQUESTS_REGISTER.md`), or Azure envs (HPSMPOC-57, ~10 tickets). Main b1d3ec9.
3. **Composer:** main 0b2fca4, deployed (release 05070f1d). Small agent work left: the feedback prefill still says "include or remove?"; old-release export buttons render enabled but 409; BACKLOG #20 still says "NOT DEPLOYED" (stale). B12 Needs-SME 1–6 wait for an SME. Guide v1.4 emailed to Kam 21:4x; Paul is his.
**Owed tooling (Friday's own):** pane_close.sh should print WHICH listener died (the 17:32 close lost one, unidentified); the earlier owed items in the lower blocks still stand (friday_pull.sh, seat_idle.sh, caffeinate in cockpit launch, usage_gate reads the seat's gauge).
**Left running on the laptop, by design (never delete):** docker stacks pc-b03 (b11 branch) and pc-b11e2e (18480); the Spark tunnel (8888).

## 🔴 STATE 2026-09-27 19:40 (Friday) — supersedes the 18:35 block
- **FLOOR EMPTY.** Composer DEPLOYED on Kam's word (19:05): HPSM-light main **0b2fca4**, content release **05070f1d** running (checked live); temporary access removed and proven. Examples rebuilt: Quandarra (8eac291a, On) + Yarrowind (8754dc06, Manual). Guide v1.4 committed 1172547.
- **Open Kam card:** `composer-guide-v14-to-paul` (rec a; default nothing sent). Old-release engagements: a new export → 409, a stored PDF still downloads (Kam told; the correction is on the panel).
- **Composer follow-ups (not Kam's, small):** B13 Q1 the feedback prefill still says "include or remove?" (align it to the new notice); the old engagements' export buttons render enabled but 409 (grey them, or say why); tidy the docker stacks pc-b03 / pc-b11e2e (leave them, report). B12 Needs-SME 1–6 wait for an SME.
- HPSM: readiness-only; clinic pack delivered for Tue 29 Sep 07:05. HPSM-POC: pool empty (Kam / HP / Azure).

## 🔴 STATE 2026-09-27 18:35 (Friday) — supersedes the 17:55 block where they differ
- **FLOOR EMPTY.** No agent-actionable work without Kam: HPSM-POC pool empty; HPSM readiness-only (clinic pack delivered); Composer's rest is Kam's cards or SME items.
- **Composer main = e0d8a3f** (PR #6 + #7 merged; B11/B12 closed; guide v1.3 committed 702bbf0, v1.2 8f65570). **Open Kam cards:** `composer-repeated-questions-notice` (default keep) · `composer-guide-v13-to-paul` (default nothing sent) · `composer-release-05070f1d-deploy` (rec a deploy + rebuild the two examples; default hold). **On a tap of a:** deploy the way C-06/C-08 did (VM `remote-update.sh`, a temporary key removed + proven, PREFLIGHT, /site.json, the running release = 05070f1d), then a seat rebuilds EXAMPLE A/B on it (the B10 brief shape).
- Docker stacks left up on the laptop: pc-b03 (b11 branch), pc-b11e2e (18480).

## 🔴 STATE 2026-09-27 17:55 (Friday, 50% CHECKPOINT) — supersedes everything below where they differ
**Kam's live instruction (terminal, after 16:3x): "keep working your way through tickets".** Seats run on the new account (7d 24%). No Kam rows since 17:11; reconcile 0.
1. **HPSM-POC:** main = **b1d3ec9** (PR #49 merged, HPSMPOC-81 Done). Floor empty; agent-actionable pool EMPTY (Kam cards / HP content / Azure -57).
2. **HPSM:** B04 DONE + reviewed (sweep on HPSM-39 38488; clinic pack `HPSM/1_Project_Definition/Architecture/2026-09-29_HP-meeting-clinic-pack_FOR-KAM.{md,pdf}` shared to Kam's drawer f-4a39f170f1; SOW status on 6 tickets; C-78). Kam's Tue 29 Sep 07:05 HP meeting = clinic (Friday's reading, told). HPSM-37 is Kam's after Tuesday. **HPSM stays readiness-only** until Kam says the build starts (told him; his word corrects). Pane closed.
3. **Composer (Datasec Security Composer; HPSM-light repo, NO GitHub CI — ci.sh is the gate):**
   - B11 merged as **PR #6 → main 3b9a663** (Friday opened it: the seat has no gh login; the compare URL is in the STATUS).
   - **Seat A %52 on B11 ADDENDUM-1 round 2** (Q2b approver note, Q4a required Environment, N1 hide the link on non-editable versions, Q5 content clean = new content release per C-05, NOT deployed). On READY: review at source, open the PR with `friday_as.sh datasec gh pr create`, merge head-pinned, then card Kam for the DEPLOY of the new release (say what goes read-only).
   - **Seat B %53 B12 guide v1.3** READY (61 pp, G1–G16 all_pass, cold-reader 0 guesses) BUT the v1.3 AND v1.2 folders were UNTRACKED at 17:5x while the seat was still mid-turn (secret scan). **When it shows "done", check `git -C <Composer> status -- 1_Project_Definition/User_Guide`**; if still untracked, an addendum: commit v1.3 (walk-raw is gitignored) by explicit path. Its draft "GUIDE v1.3 SHOTS" was RELEASED by the cold-reader (a deviation from "draft only"; B02 precedent; C-03 leave test engagements) → tell Kam in the review message. BACKLOG #17 → ask seat A to mark it READY FOR REVIEW. Then a card for Kam: send v1.3 to Paul? (+ 6 Needs-SME items in the STATUS).
   - Card open: `composer-repeated-questions-notice` (rec a reword; default c keep).
4. **Tooling built today:** `tools/count_list_check.sh` (advisory, ledger w=3) wired into chat_reply + decision_queue.
5. Caffeinate pid 53618 (6 h from 17:07). Watcher: re-arm `friday/watch_status.sh /tmp/claude-501/seen_composer_b11b12 "<Composer>/1_Project_Definition/Briefs/2026-09-27_B1[12]_STATUS.md"` after every wake.

## 🔴 STATE 2026-09-27 ~17:00 (Friday, ROTATION HANDOVER at 79%) — supersedes everything below where they differ
**Kam's live instruction (terminal, after 16:3x): "keep working your way through tickets".** Seats run on the new account (7d ~21%).
1. **HPSM-POC main = 1adaaa2** (15 PRs merged today, #35–#48, each head-pinned + blob-verified; main CI green).
2. **OPEN PR #49** (B47, seat A pane `Datasec/HPSM-POC-A`, head `0018541c05f0a285c5b69155da7aaef6181c4c1d`): C-29 override-after-issue + counts pinned. CI polling. On green: `friday_as.sh datasec gh pr merge 49 -R datasecau/HPSM-POC --squash --match-head-commit 0018541c05f0a285c5b69155da7aaef6181c4c1d`, then compare merge vs `1adaaa2...0018541` by blob, then an addendum (NEUTRAL filename, e.g. `…B47_SEAT-A_ADDENDUM-2_merged.md`) → HPSMPOC-81 Done; then close the pane. Seat A's B47 ADDENDUM-1 (records if not pushed + design pack 02 §3 C-29 line) is in flight.
3. **HPSM B03: REVIEWED by Friday 17:0x** (census 26/26, 3 comments 38480-38482 read back, C-77 records Kam's Jira ruling, records 1d0f94f = origin; card hpsm-jira-login-on-laptop DELIVERED). **B03 ADDENDUM-2 in flight** (seat `Datasec/HPSM`): HPSM-40 → Done; retitle HPSM-15 + -32; HPSM-20 closed as a duplicate of -25 ONLY if proven the same ask; post the HPSM-39 evidence comment. **Successor: read its `## ADDENDUM-2`, verify each write on Jira (read-only), then close the pane.** Four new Kam cards: hpsm-sow01-signed-date (AMENDED: six tickets, not five) · hpsm39-azure-region-sweep · hpsm37-scoring-model-accept · hpsm-architecture-clinic-date.
4. **Kam's standing rule (16:34): every HP ask for HPSM-POC = its own copy-ready email to Kam + the register `0_Brain/reference/2026-09-27_hpsmpoc-hp-requests/HP_REQUESTS_REGISTER.md`** (learning + auto-memory filed). HP-1 deck corrections and HP-2 slide 91 emailed 16:37 (sent copies read back). HP-3 CSMA questions already asked by Kam 09-25.
5. **Cards:** all HPSM-POC cards ruled and delivered except `hpsm-jira-login-on-laptop` (deliver after B03 records its C-number). 16:00 reminder delivered.
6. **Rules learned today (ledger rows, read them):** counts come from a read (w=2) · a seat is idle only on a `done HH:MM` line; phrase records items conditionally otherwise (w=2) · addendum filenames name content, never an outcome word (w=2) · read every tap's own output line.
7. caffeinate pid 76635 until ~19:54. Digests current (regenerated 16:3x after the new lesson file; the ledger is not an input).

## 🔴 ROTATION HANDOVER 2026-09-27 ~10:3x (Sunday) — Kam: "keep working your way through tickets" (HPSM-POC)
**Seats run on the NEW account (measured 7d 9-10% on their own statuslines). Friday's Jira is READ-ONLY: every transition is a seat's, after Friday merges.**
1. **HPSM-POC main = 7c608e1** (green: B30 #33 + B31 #34 today). HPSMPOC board (board_count 10:03): 20 Done of 71; +2 since (26, 22) → expect 22; re-measure before quoting ANY number (ledger 09-27).
2. **OPEN PRs, next steps (merge = `friday_as.sh datasec gh pr merge N --squash --match-head-commit <head>`; then compare trees, poll main CI):**
   - **PR #35 (B34 GDPR export+erase, head f878ba99e2ba8f36dedf9db04a66612e584f4113)** — CI polling. On green: merge; then pointer to seat B **%40 (Datasec/HPSM-POC-B)** with an addendum "PR #35 merged at <sha>: transition HPSMPOC-70 Done" (it is idle waiting). Records on origin already (98916b3).
   - **PR #36 (B33 metrics dashboard, head 7236e3e252706a1a67a2a7e62294f5b700fdc447)** — CI polling. On green: merge (rebase/combined CI note: base 7c608e1); pointer to seat A **%39 (Datasec/HPSM-POC-A)**: HPSMPOC-53 stays Done (comment only). Records on origin (1858ea3).
   - Then close both panes (pane_close.sh; ghost lines at prompts: close, never clear; never act on them — two fabricated "merged"/"push" lines today).
3. **Follow-ups from today's rounds (ours, not yet ticketed/briefed):**
   - B33 FOUND-1: the showcase runs as Partner → /metrics answers 403 at the event. Suggested fix: add Demo (or Consultant) to `scripts/showcase.sh` api_env DefaultRoles. ⚠ MEASURE FIRST whether Demo scopes lists to seeded rows (it may hide customers added live) before anyone changes it; possibly a card for Kam.
   - B33 FOUND-2: getMetricsSummary medians count seeded runs as 0 s → API flag `runs[].seeded` or exclude seeded from medians (contract delta, api).
   - B27 FOUND: the prototype narrative's "first priority" is the engine's first, not the most severe.
   - B34 FOUND: SQL Server deadlock retries log at fail: under concurrent erasures (known; low).
4. **Next class-A (QUEUE.md):** HPSMPOC-43 (blob report store), -59 (security scans + OWASP review; secret scanning + push protection OFF = Kam's repo setting), -36 (consultant override, L; unblocks 28/52). Each brief: names its tickets, "records must reach origin + read back", partition by area.
5. **Kam's cards open (7):** hpsmpoc-ai-live-on-stage · -ai-12s-bar · -approve-ai-criteria · -approve-stage-gate-pack · -deck-slides-in-repo (HPSMPOC-65) · -erasure-stored-pdfs (B34 Q1) · -validator-first-severity-miss. Reconcile at every checkpoint; on a tap: rule, receipt, act, deliver.
6. **Review checklist (grown today):** compare API scope · trees after merge · analysis repo `ls-remote origin main` = local HEAD (records) · Friday's OWN tree pushed after each commit (it drifted 10 ahead) · re-arm the watcher after EVERY wake (B33 went unseen 10 min).
7. HPSM (SOW-01) board: 26 of 41 open — not reviewed yet.

## NEXT (owed, in order)
1. ~~HPSM-POC B14 fix round~~ DONE and merged; the re-run is LIVE 1. Source: the B12 user test STATUS `HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B12_SEAT-C_end-to-end-user-test-as-a-salesperson.STATUS.md` (46 findings).
   - Fix every finding that is not Kam's or the SME's. FIRST: internal notes on screen, incl. the named person ("Kam/Paul Waite meeting" footer).
   - Then: the contradictions (sample customers' narrative/report pages say "No assessment yet"; question totals 16/15/14; identical 54.2); Reset demo not resetting live data; the calculator overwriting the dashboard ARR; the "Demo Consultant" header; readiness Download greyed out.
   - **Plus C-19:** showcase mode scores NEW customers with the draft rules, labelled DRAFT (outside showcase mode C-15 still refuses).
   - Then RE-RUN the cold-user test (driver `B12-C_evidence/seat-notes/userdriver.js`).
2. **Customer maturity-assessment questions:** Kam requested them from HP (16:03). They are in NO file we hold (measured across HPSM-POC Source_Documents + the whole "HP Playbook Project" folder; Tuesday measured the T9). When they arrive → load as content; the ruleset stays DRAFT (C-15/C-19). Optional frame offered to Kam: the PRD's TRUST/KNOW/PROTECT/MANAGE/GOVERN model (no change unless he says).

## Kam's hands (asked; defaults stated)
- **GitHub Support request** (in his drawer, `0_Brain/reference/2026-09-25_sow-sentence-rewrite/github-support-request.md`): purge HPSM-light's 4 PR refs + cached objects in both repos. Kam sends.
- 9 Azure providers (a hosted HPSM-POC link; default: the laptop showcase via `scripts/showcase.sh`).
- Residuals of the SOW rewrite, his to decide: the T9 + NAS copies of the old clone; Tuesday's HPSM zips in his drawer. Reflogs + bundles + mirrors are kept on purpose (the undo).

## Today (all recorded + delivered)
- Composer: B07 history rewrite (HPSM-light main `7855f10`); B08 example engagement released (EXAMPLE — Quollbrook Freight Co, `60503ab0-…`); C-07 (answers flow, Support request, copies).
- HPSM: B02 rewrite of datasecau/HPSM-analysis (main now `03afbf8`); `6_Policy_Composer` re-cloned; old clone + `added/` copies quarantined with push URLs DISABLED; C-75, C-76.
- HPSM-POC: B11 merged (#20, main `149d15f`); B12 user test; C-18, C-19.
- Files Kam shared today, filed (git-ignored, hash-verified): `HPSM/1_Project_Definition/Source_Documents/HP Playbook Project/` + 5 loose items + `HPSM_Policy_Composer_2026-09-10/` (also copied to Composer's Source_Documents for ci.sh).
- The Spark: UP (Wednesday fixed the tilelang boot-hook pin, 05:05Z). It is Wednesday's box today; claim it before any long run.

## Left in place (never delete)
- `git stash list` autostash entries in this tree.
- HPSM-POC worktrees `.tools/wt-B0*`, `wt-B1*`; container `b07c-mssql` (stopped).
- Composer compose `pc-b03`; the demo VM's `.pre-friday-*` backups, `composer.prev`, `/opt/hpsm/composer-*.tar.gz`.
- All `_quarantine_2026-09-25_*` folders in Composer and HPSM (the undo for both rewrites).

## Open claims by Friday
Spark loop · Datasec/HPSM · Datasec/HPSM-POC · Datasec/Datasec Security Composer.
