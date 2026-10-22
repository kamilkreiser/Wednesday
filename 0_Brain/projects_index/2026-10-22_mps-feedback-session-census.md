BLUF: Of the 53 MPSCALC tickets raised from the 16 Oct calculator review (26 from the meeting, 27 from the feedback sweep), 31 are fully merged AND in the newest hosted deploy (main e6f92a5f, 18 Oct); 8 are part-done (merged half deployed, other half open), 8 are not started, 6 are ruled deferred or decided with no build; nothing is "merged, not deployed" except one half of MPSCALC-151; hosted is 11 commits behind main f5b6f5a7. So: NO, not all complete.

# MPS Calculator feedback session census (read-only, 2026-10-22 ~11:20)

Asked by the product owner 2026-10-22 11:01 (TUESDAY daily_tuesday/2026-10-22.md:88).

## 1. Session identified

Most likely meant: **the review of the calculator held by the product owner with the reviewer on 2026-10-16** (recording "MPS Calculator Walkthrough", 51m36s).
- Source: brief `Briefs/2026-10-16_B99_SEAT-B_mps-paul-review-tickets.md` ("Kam's words, verbatim"), `Briefs/2026-10-16_B99_STATUS.md` (BLUF: 50 meeting items PR-01..PR-50, 53 tickets MPSCALC-136..188, lanes A-J), `CLARIFICATIONS.md:466` (C-32), Tuesday daily 2026-10-16.md:68 ("MPS Paul review: 6 grouped cards ... 8 lane briefs B100-B107"). Lanes B100-B109 (+ rulings in `Briefs/2026-10-16_MPS-LANES_ADDENDUM-1_kam-rulings-1303-1306.md`).
- Why this one: it is the only session that produced a numbered item list, a written "feedback" sweep ("all feedback items in this project"), ticket range and lane split; the owner's instruction was "create tickets from everything mentioned ... then get agents to action these as well as all feedback items".
- Item list used: the 53 tickets (T01-T26 = MPSCALC-136..161 from the meeting; BL-01..BL-27 = MPSCALC-162..188 from the feedback sweep). The meeting's 50 PR items: 39 became tickets, 11 needed none (built/context/answered) per B99_STATUS BLUF.

Other candidate (less likely): the owner's own hosted-feedback items of 2026-10-13 (brief `Briefs/2026-10-13_B81_SEAT-R_read-kam-feedback-items-hosted.md`, owner quote at :Why). Its two asks (7th tile, file upload) are DONE and DEPLOYED (B99_STATUS table FB-01/FB-02: C-27 #38 / C-28 #39, deployed b9a3d769; both ancestors of the newest deploy since #38/#39 precede #43). Also the reviewer's 3 hosted-feedback items (FB-03..05) are inside the 53: FB-03 -> MPSCALC-161 (not started), FB-04/05 -> MPSCALC-138 (done+deployed).

## 2. Deploy state (from the project's records only, no HTTP)

- Newest deploy record: **B268, hosted showcase on main `e6f92a5f7568b2f2d72f454524b8e09406357957` (PR #82), 2026-10-18 (~19:33-19:41 AEDT)**. Sources: `Briefs/2026-10-18_B268_STATUS.md:8` and last line `DEPLOYED: e6f92a5f... live-check 0`; `5_Project_History/history.md:94-96`; CLARIFICATIONS C-43 (:611-624).
- Earlier deploy: B166 `12f8e566` (PRs #43-#73) 2026-10-17 ~10:00 (`history.md:139`). Both lie in the ancestry of e6f92a5f.
- No later deploy record: `DEPLOYED:` last lines over Briefs: newest is B268; CLARIFICATIONS 2026-10-21 entries say "not deployed (MPS hosted is one card per deploy)" (e.g. :821); B406 history line 11.
- Main now: `f5b6f5a710258a4a36ffbcab92787a2434962500` (PR #93, 2026-10-20T23:20Z), by `git ls-remote origin main` in 2_Project_Files and `gh api .../commits/main`. `gh api compare e6f92a5f...f5b6f5a7`: ahead_by=11, behind_by=0 (= PRs #83-#93, none deployed).
- Contained test: for every merge sha below, `gh api repos/datasecau/MPS-Commercial-Calculator/compare/<merge sha>...e6f92a5f` status "ahead" (deployed sha contains it).
- Jira is NOT a state instrument here: all 229 MPSCALC tickets from -86 up are Backlog (only -86, -89 Done); the project rule is "no project rule moves a ticket on merge or deploy" (JIRA.md:185). Status below comes from merge commits + records.

## 3. Per-item table

Statuses: DONE+DEPLOYED / PARTIAL (a part merged+deployed, another part open) / NOT STARTED / DEFERRED-or-RULED (with source). "contained" = compare result "ahead" vs e6f92a5f.

### 3a. From the meeting (T01-T26)

| Item | Ticket | Merged (PR, sha) | Deployed | Status |
|---|---|---|---|---|
| Roles: all users hold all roles, hide role choice (T01) | MPSCALC-136 | #67 a6813d70 (web half) | yes, contained; first in 12f8e566 | PARTIAL: web half deployed; the Entra all-roles group assignment is Kam-approval-class and its state is not recorded (NOT MEASURED); B164 K8 notes act-as switch disappears for 4-role sign-ins |
| Owner self-approval, audited (T02) | MPSCALC-137 | none | no | NOT STARTED (ruled K-01=a 16 Oct; folded into v13 T-V7-6, `B308_STATUS.md:178`; `B166_STATUS.md:190`: "self-approval is not built") |
| Dashboard Deals won/lost + switch + order (T03) | MPSCALC-138 | #51 0738fb0a | yes, contained | DONE+DEPLOYED (title fix #75 725b4ef5 also in e6f92a5f) |
| (i) info hints site-wide (T04) | MPSCALC-139 | #68 ec29d51a | yes | DONE+DEPLOYED |
| Import care packs (T05) | MPSCALC-140 | #74 ed726068, #78 f1d5641a | yes | DONE+DEPLOYED |
| Price-book coverage audit (T06) | MPSCALC-141 | #65 a5cbbf81 (docs only) | yes | DONE+DEPLOYED |
| Class "Care pack" (T07) | MPSCALC-142 | #76 0217044e (+#78) | yes | DONE+DEPLOYED |
| "Supply" -> "Supplies" (T08) | MPSCALC-143 | #52 e59fa18f | yes | DONE+DEPLOYED |
| Large-format items source (T09) | MPSCALC-144 | none | no | NOT STARTED (waits reviewer's file K-08 open default "LFP manual"; C-35 ruling waits MPSCALC-202/-203, `CLARIFICATIONS.md:514,623`) |
| Blank section label, max 100 (T10) | MPSCALC-145 | #68 ec29d51a | yes | DONE+DEPLOYED |
| Add section/Save/Calculate top+bottom (T11) | MPSCALC-146 | #68 | yes | DONE+DEPLOYED |
| Class "Customisation" (T12) | MPSCALC-147 | #69 3478ff43 | yes | DONE+DEPLOYED |
| Picker adds several items (T13) | MPSCALC-148 | #68 | yes | DONE+DEPLOYED |
| Fleet/quote import wizard, phase 2 (T14) | MPSCALC-149 | none | no | DEFERRED (K-17 phase 2, lane I not launched; ADDENDUM-1 item 5) |
| Usage redesign: deal-level charges, per-device pages, one calculation (T15) | MPSCALC-150 | #73 12f8e566 (engine/API); #82 e6f92a5f prints deal rates (214) | yes | PARTIAL: engine+API+proposal rates deployed; UI half open (`B169_STATUS.md:167` "UI half open"; no branch for it) |
| Purchase software term = contract term (T16) | MPSCALC-151 | #61 7f3ea7dd (warning half); #86 67bf2004 (V5 software section, 10-20) | #61 yes; #86 NO (after e6f92a5f; compare "behind") | PARTIAL: warning half deployed; "offer only the matching term SKU" half: whether #86 satisfies it is not read -> UNKNOWN; #86 MERGED NOT DEPLOYED |
| Later: meter billing -> invoices (T17) | MPSCALC-152 | none | no | DEFERRED ("Later" bucket, B99_STATUS lanes table) |
| Typical values in usage hints (T18) | MPSCALC-153 | #68 | yes | PARTIAL: merged+deployed; governed-setting half moved to MPSCALC-212 (open; `B164_STATUS.md:130`) and K-04 data ask still open |
| Client fleet template, phase 2 (T19) | MPSCALC-154 | none | no | DEFERRED (K-17 phase 2) |
| Class "Staging" (T20) | MPSCALC-155 | #76 0217044e | yes | DONE+DEPLOYED |
| Credit callout on proposals (T21) | MPSCALC-156 | #50 4eb57742 | yes | DONE+DEPLOYED |
| Align proposals with the reviewer's two documents (T22) | MPSCALC-157 | #50 4eb57742 | yes | DONE+DEPLOYED |
| Target click -> margin needed (T23) | MPSCALC-158 | #73 12f8e566, #77 422b87b2 | yes | DONE+DEPLOYED |
| HP promotional pricing / MFP rebates (T24) | MPSCALC-159 | none | no | DEFERRED (K-12 "defer", ruled a, ADDENDUM-1:7 and :"Build K-09 then K-11; defer K-12") |
| Partner referral rebate starts at 7% (T25) | MPSCALC-160 | none | no | NOT STARTED (`B103_STATUS.md:226` waits lane A; no commit/branch; code search "referral" = 0) |
| Archive (delete) a quote (T26) | MPSCALC-161 | none | no | NOT STARTED (`B102_STATUS.md:195` waits lane D contract; no branch) |

### 3b. From the feedback sweep (BL-01..BL-27)

| Item | Ticket | Merged (PR, sha) | Deployed | Status |
|---|---|---|---|---|
| Overlay store hardening | MPSCALC-162 | #59 169e5a88 | yes | DONE+DEPLOYED |
| Overlay concurrency/timing | MPSCALC-163 | #58 f3ab6fc6 | yes | PARTIAL: timing tests merged; "under-load half stays open" (PR title; B164:342) |
| Source version store integrity | MPSCALC-164 | #59 | yes | DONE+DEPLOYED |
| Start refusals in words | MPSCALC-165 | #59 | yes | PARTIAL by records: merged but listed "stay open" (`B164_STATUS.md:342`); the open remainder not read |
| Validation content checks | MPSCALC-166 | #56 7dd1afeb | yes | DONE+DEPLOYED |
| Stage route fault logging tests | MPSCALC-167 | #57 db4a8f68 | yes | DONE+DEPLOYED |
| Duplicate rule on checked versions | MPSCALC-168 | #55 c06141b6 | yes | DONE+DEPLOYED |
| Quote API: name the source set | MPSCALC-169 | none | no | NOT STARTED (waits lane C2 after contract; no branch) |
| Fleet line identity / price audit | MPSCALC-170 | #64 6cf4e453 | yes | PARTIAL: merged ("pairing within one number"); records keep it open (`B164_STATUS.md:342`) |
| Empty quote cannot calculate | MPSCALC-171 | #54 86e6c297 | yes | DONE+DEPLOYED |
| Approver corrects Won/Lost outcome | MPSCALC-172 | none | no | NOT STARTED (ruled MPS-7; no commit/branch) |
| Demo loader posts S4 hosted | MPSCALC-173 | #47 84580b5f | yes | DONE+DEPLOYED (code); a hosted run of the loader not measured |
| Feedback hardening (401, rate limit) | MPSCALC-174 | #60 fa23e5b9 (401), #62 d0562848 (429 contract docs) | yes | PARTIAL: rate-limit half unbuilt (B106 local branch only, `B106_STATUS.md:111`; code search FEEDBACK_RATE_LIMITED = docs/API.md only) |
| SOURCES_UNAVAILABLE words | MPSCALC-175 | #43 5d7e4813, #53 07e3c933 | yes | DONE+DEPLOYED |
| Feedback triage + My feedback | MPSCALC-176 | none | no | NOT STARTED (`B106_STATUS.md:144` waits lane D, then words) |
| Feedback pill on phone | MPSCALC-177 | #44 621e3300 | yes | DONE+DEPLOYED |
| Docs drift | MPSCALC-178 | #47 84580b5f | yes | DONE+DEPLOYED |
| Leak tests: generic types | MPSCALC-179 | #63 894f538a | yes | DONE+DEPLOYED |
| Dev server HMR host | MPSCALC-180 | #46 ea851c67 | yes | DONE+DEPLOYED |
| Quote/snapshot stores on a database | MPSCALC-181 | none | no | DEFERRED ("Later" bucket, B99_STATUS) |
| Importer date: Sydney | MPSCALC-182 | #66 de808f51 | yes | DONE+DEPLOYED |
| PRE-1 inside deploy script | MPSCALC-183 | #72 798fe984 | yes | DONE+DEPLOYED |
| Test gap failed inventory read | MPSCALC-184 | #45 71bce520 | yes | DONE+DEPLOYED |
| 390 px quote screen and dashboard | MPSCALC-185 | #68 ec29d51a | yes | DONE+DEPLOYED |
| Dashboard: one failed read fails all tiles | MPSCALC-186 | #51 0738fb0a | yes | DONE+DEPLOYED |
| Hosted proof: catalogue edit survives restart (C-19) | MPSCALC-187 | none | no | NOT STARTED (own hosted brief; no STATUS names it after 10-16) |
| Decision: cost inferable from applied prices (K-18) | MPSCALC-188 | none | n/a | RULED: K-18 = a "accept cost-plus visibility" (`MPS-LANES_ADDENDUM-1:6`); no build |

## 4. Totals

- Items: **53** (26 meeting tickets + 27 sweep tickets).
- DONE+DEPLOYED: **31** (meeting 14, sweep 17).
- PARTIAL (a half merged+deployed, other half open): **8** (MPSCALC-136, 150, 151, 153, 163, 165, 170, 174).
- NOT STARTED: **8** (137, 144, 160, 161, 169, 172, 176, 187).
- DEFERRED/RULED-OUT (no build by ruling): **6** (149, 152, 154, 159, 181 deferred; 188 decided).
- MERGED NOT DEPLOYED: 0 whole tickets; one half: MPSCALC-151 matching-SKU half via #86 (and v13 work #83-#93 outside this list).
- Open for the owner's question: 8 + 8 = 16 tickets still with an open part (plus 6 deliberately deferred/decided).
- Newest deployed sha: `e6f92a5f` (B268, 2026-10-18 ~19:33-19:41 AEDT). Main `f5b6f5a7`, ahead by 11 commits (PRs #83-#93), none deployed.

## 5. Controls

- Contained test can fire: compare of post-deploy commits (acfcf5de #84, 21c2aec7 #83, 67bf2004 #86) against e6f92a5f returned "behind" (behind_by 2/1/6); in-scope commits returned "ahead" (ahead_by 3-39).
- "No commit names the ticket" zeros (137, 144, 149, 152, 154, 159, 160, 161, 169, 172, 176, 181, 187, 188): the same regex over the 59 main commits since 2026-10-13 finds hits for 138 (#51) and 150 (#73); branch search (gh branches) for 150/174/rate-limit finds b103/b106 branches, and finds none for 137/160/161/169/172/176; code search "referral" = 0 while "rebate" = 60 (the search works); FEEDBACK_RATE_LIMITED hits only docs/API.md.
- "No later deploy": `DEPLOYED:` grep over Briefs finds B268 as newest; the same grep finds earlier B166, B92 (so it can fire).
- Jira read: 231 issues returned from MPSCALC-86 to -316 incl. the two Done (-86, -89), so a non-Backlog status is visible when present.
- gh identity: `gh auth status` = kamilDatasec with the project's GH_CONFIG_DIR; a git@github.com URL ls-remote without the deploy key returned "Repository not found" (wrong-credential control), the repo-local origin returned f5b6f5a7, equal to gh API.

## 6. NOT MEASURED

- Anything on the live hosted site (no HTTP by fence): the deployed behaviour was not seen; "deployed" is by record + ancestry only.
- Whether the Entra "all roles" group (MPSCALC-136) was assigned in the tenant; the hosted S4 loader run (173); the C-19 restart proof (187).
- Whether #86 (V5 software section) fulfils the matching-SKU half of MPSCALC-151; the open remainders of 163, 165, 170 beyond the records' "stay open".
- The 11 meeting items that needed no ticket were not re-verified.
- Words approval for the new sentences (done at the B166/B268 deploy cards per records; not re-read).
- Anything after 2026-10-21 14:36 (last record read: B406 / history top).
