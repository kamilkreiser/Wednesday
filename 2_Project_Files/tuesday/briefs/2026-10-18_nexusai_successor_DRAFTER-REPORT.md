# DRAFTER REPORT: NexusAI lane O successor S101O (2026-10-18, 06:37-06:53 AEDT)

I am a read-only drafter for Tuesday. I launched nothing and sent nothing, and made no Jira, git or gh writes. I ran no git fetch, pull or worktree, no az, and no HTTP to any app host, the demo or production. The only writes are the two files in `tuesday/briefs/`. Some outputs went to my session scratchpad: Jira dumps, mail bodies and merge-tree output.

## 1. Files
- **Body:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_nexusai_successor_S101O.md`.
- **send_brief DRY RUN: rc 0**, "DRY RUN — all gates PASSED, nothing sent". The recipients are datasec-nexusai@ and coagent@.
  - The first dry run gave **rc 1**, verbatim: `BRIEF REFUSED — the QUEUE section names ticket(s) with no provenance line: RD-801 RD-802 RD-820`.
  - I fixed it by reading all three tickets and adding a provenance line: RD-801 and RD-802 are Release Ready, RD-820 is To Do. Then I re-ran it twice, both rc 0.
- **SELF-CHECK** is stamped `2026-10-18 06:52`, which is my own re-read. Re-stamp it after you read the body, because the attestation is the sender's.

## 2. Launch command (one line, same form as S100O)
`bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/brief_and_launch.sh --to "Datasec/NexusAI-O" --subject "SUCCESSOR S101O lane O: RD-478 via RD-761 and RD-794 re-checks, RD-476 prompt build, RD-505/506 via the C-170 head re-check" --body-file /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_nexusai_successor_S101O.md`
- The usage gate runs first.
- `cockpit.sh resolve "Datasec/NexusAI-O"` gives rc 0. DevMASTER is unmounted, so it falls back to `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/Launch_Claude.command`.
- **Lane name: `Datasec/NexusAI-O`.** It is the template's lane. The route exists (inbox_routing.conf:107 and launchers.conf:38), and S100O, the seat this one succeeds, held it. The `-O` suffix keeps the seat letter and the handover name `S101O` in step.

## 3. Corrections to the commission (read these before launch)
1. **The sweep's "next High items with no human dependency" list was mostly wrong at source.**
   - **RD-262** is an umbrella. It closes when its children RD-264..267 leave Testing, and that is a board move for Kam or a teammate (comment 38207).
   - **RD-386** is past the cap. Card `nexusai-rd369-round3-or-ship-at-the-cap` was ruled round3 on 09-09. Round 3 ran at 7cd0907 and came back NO GO at the cap on 09-10 (the card's delivered_artefact). A fourth round is Kam's.
   - **RD-505 and RD-506** have no work of their own on main. Both close only when the C-170 head lands.
   - **RD-476** is genuinely agent work. **RD-478** is agent work, but through its already-gated slice.
   - **Excluded:** RD-262, RD-386, RD-50 (its own scope note says execution is in the Feedback System and Lead Bot folders, and RD-88 was a blocker), and RD-460 itself (Kam's monetisation and ACR decisions).
2. **RD-505/506 are not blocked by Kam's RD-460 decisions.** The C-170 merge that closes them was ruled by Kam (C-170, card `nexusai-package-files-scope` = b), gated (5b, GO WITH FINDINGS), and RELEASED by Tuesday to M on 2026-09-29 (NEXT-PICKUP-TUESDAY.md:1159, nine merges).
   - **Only RD-681 of those nine ever landed.** RD-627b, RD-682, RD-705, RD-695, RD-413, C-170 be0fe37, RD-696 and RD-594 are all off main (`merge-base --is-ancestor`), and all eight are still in Testing.
   - **They are absent from the turn order rebuilt on 10-08 to 10-13** (items 1-25). So they look like a dropped-merge case of the 10-08 ledger family. The brief commissions only the be0fe37 re-check. **You must rule the order**: the 09-29 RELEASE puts C-170 after RD-413.
3. **Twelve more released, gated heads are not on main** (by gh compare, each head has 2-17 commits that main lacks):
   - items 12-17: RD-751, RD-817, RD-747, RD-831, RD-777+776, RD-761;
   - items 20-25: RD-721, RD-794, RD-819, RD-807, RD-131, RD-775.
   - RD-761 and RD-794 carry open CRITICAL CodeQL alerts (#23-#26 and #27). I put RD-761 and RD-794 into item 1, because RD-794 records Tuesday's "RD-761 merges BEFORE RD-794 (13:13:22Z)".
   - Both are **lane R's** branches, and R is not live. Re-checking them in a local worktree touches no ref. Who lands them, and in what order against items 12-16, is yours to rule.
4. **The seat id came from a different source than the commission named.** `5_Project_History/history.md` does not exist; project CLAUDE.md:44 says history lives in `2_Project_Files/HISTORY.md`. Main's HISTORY.md has no S100O entry. It is on the unmerged branch `s100o-history-docs` @ 46bc7b1, at HISTORY.md:8385. With the highest HANDOVER-S100O.md and pending_plan_2026-10-17_S100O.md, that gives **S101O**.
5. **The undelivered-rulings gate does not cover this lane.**
   - send_brief maps only `Datasec/NexusAI` to prefix `nexusai-`, so `Datasec/NexusAI-O` is unmapped. That is the same registry-gap class as the -G/-R note in send_brief.
   - The prefix also misses two ruled, undelivered cards labelled Datasec/NexusAI: `rd104-gh-identity-acceptance-false-premise` (youcheck, 09-07) and `t9-nas-leg-direction` (a, 09-21). Both are carried in the body.
   - The gate greps `^RULED BY KAM…` at line start, so the template's `## RULED BY KAM…` heading would not satisfy it. I wrote the line plain.
   - Mark both cards delivered, or tell me they are live.
6. **RD-476 is "new customer-facing words"** under grant row 1's NOT list. The ticket already routes it through Kam before any merge, and the brief says so. Its eval is narrowed to the test mock, because the project .env holds no Azure OpenAI variable and a live run would spend money.
7. **Subject prefix:** it still reads `[Wednesday -> …]`, the same known OWED item as on 10-17.

## 4. Verified facts (each with its instrument, 06:37-06:51 AEDT)
- **main:** c7ca0ed7113750b2 (`git ls-remote`). There is no rd-476/478/505/506 branch, and no commit on any ref names RD-476.
- **T9 unmounted:** `ls /Volumes`.
- **Lock base:** `locks-laptop-1017` has an empty `queue-jest/`, 29 entries in `released/`, and no holder (`find`).
- **No NexusAI pane** (`cockpit.sh status`). Load 2.15 (`uptime`).
- **CodeQL** (gh api):
  - 239 open on main;
  - #27 critical at ollamaAdapter.js:126, and #19/#20 at server.js:16606/:16815, all open;
  - ruleset 24139430 active;
  - code_security enabled.
- **Deploy-demo SKIP mechanism** (deploy-demo.yml:53/:91 need `vars.CI_DEPLOY_ENABLED=='true'`):
  - repo variables 0;
  - org variables 0;
  - environments: `dev` only;
  - the last 3 runs were skipped.
  - The brief gives the seat the before and after checks.
- **gh token:** scopes `gist, read:org, repo`, no `workflow`. be0fe37 adds `.github/workflows/arm-ttk.yml`.
- **Legacy read-only `git merge-tree`:**
  - RD-794 on c7ca0ed: only the counts file conflicts, and server.js auto-merges.
  - be0fe37 on c7ca0ed: counts-only.
- **Tickets:** all candidate tickets were read WHOLE, with every comment, paged and sorted (RD-262, 386, 476, 505, 506, 478, 50, 460, 794, 761). Linked tickets were read by status.
- **Mail:** Tuesday's fifteen ANSWERs to NexusAI-O (2026-10-16T20:42Z to 2026-10-17T10:02Z) and the TURN were read whole, through the AgentMail GET with Tuesday's key.

## 5. Chosen tickets (priority, then key)
1. **RD-478** (Highest). **Narrowed** to its gated slice RD-794 @ cd171f9, re-checked after RD-761 @ 7f1881e. Each ends at READY FOR GATE. No new removal is built.
2. **RD-476** (High). **Whole except item (4)**, which is mock-only. It ends at READY FOR QA, tier 2, and does not merge until Kam sees it.
3. **RD-505 + RD-506** (High). **Re-check only** of the C-170 head be0fe37. It ends at READY FOR GATE, tier 1, and a re-gate is likely: the head is 304 behind.

## 6. What I could not verify
- RD-761's merge-tree. Its head is not in the local clone, and I may not fetch.
- Gate reports 19, 20 and 5b. They are on the T9 only; Laptop-DEV's `Testing Agent MAIN/…/reports` has no folder for them. The verdicts come from your RELEASE files and NEXT-PICKUP.
- Why the batch 5a/5b merges stopped after RD-681. I found no record. It may be C-189/C-190 on 09-28/29.
- Whether a push carrying a workflow file is accepted by the seat's SSH deploy key.
- The usage gauge (`usage_gate.sh` not run).
- Tuesday's 2026-10-06T13:13:22Z "RD-761 before RD-794" mail itself. It is quoted from RD-794 comment 39135 and was not read at source.
