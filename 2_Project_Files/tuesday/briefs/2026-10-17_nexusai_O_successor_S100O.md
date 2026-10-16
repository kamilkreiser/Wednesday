# BLUF — SUCCESSOR SEAT Datasec/NexusAI-O (lane 3), next round. FIRST WORK: RD-848 (drop the build stage's duplicate COPY at Dockerfile:74, and add a static guard over EVERY stage), ending at READY FOR GATE (tier 1: the shipped build). Then re-check the gated-but-unmerged RD-801+RD-822 and RD-802 branches against today's main and mail Tuesday one READY FOR GATE per branch. Then RD-828 slice 2, then RD-837 (its hold is cleared, see QUEUE 4). No merge, no deploy, no gate of your own: each needs Tuesday's mail. Send a PLAN CONFIRMATION first.

**Addressed to the cockpit seat `Datasec/NexusAI-O` ONLY.** Establish your seat from your own pane's cockpit name (`tmux display -p '#{@cockpit_name}'`). The highest HANDOVER-S* file in the NexusAI folder is HANDOVER-S99O.md, so you are **S100O** and your handover is `HANDOVER-S100O.md`.

## READ FIRST, in this order (all in the NexusAI folder)
1. `HANDOVER-S99O.md` WHOLE (§0 state at wrap, §2 open items, §4 "Next for lane O").
2. Jira RD-848, RD-828 (all 5 comments), RD-837, RD-821 (comments 39348 and 39361), RD-801, RD-822, RD-802, RD-847.
3. Tuesday's mails on this inbox since 2026-10-16T03:00Z naming O, read WHOLE (the gate 23 TURN 03:40:19Z and the ANSWER 05:21:56Z among them).
4. CLARIFICATIONS: C-40 (line 232), C-57 (line 418), C-63 (line 589), C-186 (line 2009), C-190 (line 2062), C-199 (line 2158).

## MEASURED BY TUESDAY'S DRAFTER (2026-10-17 06:0x-06:2x AEDT)
- origin main = **17fc6c5157d5446cc015e97555fdc1ffcdc986ee** (`git ls-remote origin refs/heads/main`). It is PR #86 (RD-846) per HANDOVER-S99O §0.
- **GitHub Code Security on datasecau/Reporting_Dashboard_Au = ENABLED** (`gh api repos/datasecau/Reporting_Dashboard_Au --jq .security_and_analysis`: `code_security.status` "enabled"; dependabot_security_updates enabled; secret_scanning, push protection, non-provider patterns and validity checks all "disabled"). CodeQL can run on your PRs. It was OFF on 10-14 (the S99O brief); re-read it before you rely on it.
- Open CodeQL alerts #154-#160 (js/log-injection) are all still open on main: #155-#158 `backend/routes/feedback.js` :277/:315/:363/:474; #154 `backend/routes/entraProvisioning.js:432`; #159/#160 `backend/services/scimProvisioning.js` :259/:354 (`gh api .../code-scanning/alerts?state=open`).
- Dockerfile at main 17fc6c5 (`git show 17fc6c5:Dockerfile`): stages `base` (:2), `deps` (:28, FROM base), `build` (:40, FROM deps), `production` (:82, FROM base). `:23` (base) and `:74` (build) are both `COPY package.json package-lock.json ./`. The RD-846 comment at `:109` still says "(line 22)" (F-846-2; the base pair is :23).
- Origin refs (`git ls-remote origin 'refs/heads/rd-8*'`): NO `rd-848*` and NO `rd-837*` branch. `rd-828-gate14-cells-s93o` = `b2eecdf0d94b46df4200c8d986d4f27649aa25e2` (slice 1, merged). `rd-801-feedback-log-injection-s87o` = `661311351166ea80006e088356c179f125a3ebec`. `rd-802-provisioning-log-injection-s87o` = `a103c8e8c8a97fdd4ccd563d9555f0abb3db94a0`.
- Load at 06:17: 7.62 / 6.07 / 5.03 (`uptime`). This machine is shared with the MPS lanes: heavy runs (docker builds, full jest) only while the 1-minute load is below 40.
- The T9 volume is mounted (`ls /Volumes`: KK_T9_External_HDD present, 06:1x). RD-847 says the lock tool's BASE is hard-coded to the T9 path (`session-tools/nexusai-lock.sh:79`), so the lock works only while it stays mounted. Check before every locked run; if the T9 is gone, STOP and mail Tuesday.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- nexusai-rd846-build-broken-demo-deploy-1013: Kam's choice "b" ("Keep going tonight"), ruled 2026-10-16T12:15:29+11:00. It has been acted on: RD-846 merged as PR #86 and main 17fc6c5 is on the demo as revision nexusaidev-app--0000100 (HANDOVER-S99O §0-§1). -> must land in an RD-846 comment. Tuesday records the delivery (decision_queue.sh --delivered); **nothing for you to do**, and it is not a reason to deploy anything.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- C-186: merge turns open only on Tuesday's TURN/RELEASE mail.
- C-190: every merge to main goes through a PR; no new high-or-higher CodeQL alert; no alert is ever dismissed (dismissal is Kam's).
- RD-802 never merges before RD-801 and never rides in the same push (gate 19 RELEASE, turns 18 and 19).

## AUTHORITY
- **Merges:** Kam's grant to Tuesday, EXPIRING-GRANTS row 1, scope quoted exactly: *"READY = QA gate at the deployed head + Tuesday's completion check + merged via CodeQL; runbook unchanged (backup, rollback, live check); report each deploy after it lands. Merges: Tuesday's GO on a gated head, one at a time, CodeQL never bypassed. NOT: MPS hosted (still card-per-deploy), production (QuickQuote live), money, any human, new customer-facing words, read-only content releases."* Given by Kam, typed into the Tuesday terminal 2026-10-16 ~11:4x AEDT: *"yes, the push to demo when ready applies to you now.  3)HPSM-POC not frozen.  we need to keep working on it now.  4)nexus and all datasec projects now controlled by this account.  doing github next"*. For you this means: build, push your branch, mail READY. **A merge happens only on Tuesday's TURN mail for a gated head.**
- **The demo deploy is NOT in this brief.** It comes as its own brief from Tuesday, after a merge.

## QUEUE
1. **RD-848** (Low; tier 1, because the Dockerfile is the shipped build). Branch off main 17fc6c5, for example `rd-848-dockerfile-build-stage-s100o`.
   - Drop `Dockerfile:74` (the build stage inherits the pair from `base` :23 via `deps`).
   - Add a static guard over **every stage**: no COPY in a stage may copy only files the stage already holds byte-identical. It must **resolve globs** (the gate's N-846-1: a literal-path guard misses the first bad commit 8de8e5c, where the base stage used `package*.json`). Red-first: the guard is red at 17fc6c5 (it names :74) and at 8de8e5c, and green at your head. C-40: a planted duplicate COPY in another stage turns it red.
   - F-846-2: the comment at `:109` cites the stage by name, not a line number.
   - Prove the image: your own ACR build (S99O's tools are in `session-tools/s99o/`: `dind-build.sh`, `vfs-matrix.sh`) on the vfs path that reproduced RD-846, plus the gate's re-arm probe (one inserted `COPY LICENSE ./` after the old :74 must now stay green on vfs), the shipped `/app` manifest diff against 17fc6c5's image (expect EMPTY), and a full verify with counts regenerated once (C-57). Docker builds run **under the docker lock** (S99O's disclosed slip).
   - End: mail `READY FOR GATE: <branch> @ <sha>` (tier 1) with PRIOR WORK and NOT TESTED. Tuesday commissions the gate.
2. **RD-801 + RD-822 @ 6613113, then RD-802 @ a103c8e: re-check against today's main. Do not gate them yourself, and do not merge.** History (read it, do not redo it): gate 19 gave RD-801 GO WITH FINDINGS (N-801-1 Polish: C1 controls NEL U+0085 and CSI U+009B pass `logSafe` raw) and RD-822 GO; gate 20 gave RD-802 GO. The gate 19 RELEASE (2026-10-12) put them at merge turns 18 (RD-801+822) and 19 (RD-802). They never merged.
   - Both heads are **134 commits behind main**; merge-base `d97039fe33b2f3b63899b27d591f3317e7eaa8a0` (`gh api .../compare/main...<branch>`: rd-801 ahead 3, rd-802 ahead 5, rd-802 is rd-801 + 2). Of the 75 files main changed since the merge-base, the only one the branches also touch is `scripts/verify-expected-counts.json`. That predicts a counts-only conflict (C-57). **Measure it yourself** with `git merge-tree --write-tree origin/main <head>` for each head.
   - In a fresh LOCAL worktree (never push it, and never move either gated branch ref), forward-merge main into 6613113, regenerate counts once with the id-superset control (C-57), run the full verify, and confirm the new `__tests__/rd801-*`, `rd822-*` cells still pass by name. Then the same for a103c8e on top of that merged RD-801 tree (stacked, C-199).
   - Search Jira for a ticket holding N-801-1. If none, list it as a ticket candidate for Tuesday (do not file it).
   - Mail Tuesday ONE mail per branch: subject `[Datasec/NexusAI-O -> Tuesday] READY FOR GATE: <branch> @ <head sha>`. Body: the merge-tree result (conflicting files by name), the merged tree id, the verify line, the counts, which gate verdict the head already carries, and whether anything except the counts file changed under it. Tuesday then decides between a re-gate kit and a merge TURN.
3. **RD-828 slice 2** (Low; tier 2, test-only, red-first per cell against its named mutant). Branch off the then-main. Cells (RD-828 description and comment 39408):
   - B-F1 (RD-737): pin the census to the 16 literal rule strings (or derive KEY_EXTS from `.dockerignore` and pin its length). Red under M-census.
   - C-F1 (RD-708): an ARM that strips only server.js's IP lines; expect `|finding gone` for that kind only. Red under M-fileOnly.
   - C-P1 (RD-708, Polish): a count going DOWN is labelled `|finding gone`. **Propose the label in your plan; Tuesday rules it.**
   - E-F1 (RD-675): an upper-case extension plant (`X.CMD`) and a cell that drives the tracked cell's own filter with a planted path list. Red under M-case and M-inline.
   - **D-F1 needs no cell** (RD-828 description: "Corrected in RD-690's MERGED mail; no code"). The morning sweep's row listed it as a cell; the ticket wins.
   - End: `READY FOR QA` (tier 2) to Tuesday.
4. **RD-837** (Medium; tier 2, tooling outside git). The ticket's hold reads "Do NOT build yet: lane O's tooling queue, after F-821-1". **F-821-1 is cleared:** RD-821 round 3 was installed 2026-10-12T10:53:52Z after gate 21's GO (comment 39361). Fix `session-tools/c57-id-superset.sh:77` so each runner tree uses its own install (or prints the resolved proxy-addr path and version beside the failed count). Install per C-63 (a new file, arms on a scratch base, atomic mv, old file kept). Re-read `:77` first; the line number is from 10-12.

## NOTE ONLY (no action)
- The demo's Entra group check on revision `nexusaidev-app--0000100` is still UNEXERCISED: 0 failures over 0 sign-ins (HANDOVER-S99O §0). Do not sign in, and send no HTTP to the demo. Tuesday tracks it.
- The three stale open PRs (#58, #67, #70, last updated 10-07/08) are not yours this round.

## STANDING LINES
- PRIOR-WORK CHECK before rebuilding, replacing or removing anything. Every READY carries PRIOR WORK + NOT TESTED.
- Never delete (move aside). Never edit a running script. Never kill by pattern.
- Every factual sentence in a mail names its instrument, or says "unmeasured".
- zsh does not word-split unquoted lists; build file lists in bash and check for a real "Tests:" line.
- `uptime` before every docker build or full jest; start only below load 40. Gates outrank you on the lock.
- Write the handover when your pane first shows less than 10% before auto-compact.

PROVENANCE:
- origin main 17fc6c5157d5 and the rd-801 / rd-802 / rd-828 refs; no rd-848 or rd-837 ref | `git --no-optional-locks -C /Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/2_Project_Files ls-remote origin refs/heads/main 'refs/heads/rd-8*'` | read 2026-10-17
- code_security enabled, secret scanning disabled | `gh api repos/datasecau/Reporting_Dashboard_Au --jq .security_and_analysis` with GH_CONFIG_DIR=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config | read 2026-10-17
- alerts #154-#160 open, paths and lines | `gh api 'repos/datasecau/Reporting_Dashboard_Au/code-scanning/alerts?state=open&per_page=100'` | read 2026-10-17
- rd-801/rd-802 ahead 3/5, behind 134, merge-base d97039f, only overlap scripts/verify-expected-counts.json (75 files on main's side) | `gh api repos/datasecau/Reporting_Dashboard_Au/compare/main...<branch>` and `compare/d97039f...main` | read 2026-10-17
- Dockerfile stages and :23 / :74 / :109 at 17fc6c5 | `git show 17fc6c5:Dockerfile` in /Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-10-17
- RD-848 fix shape, glob-resolving guard, F-846-2 | Jira RD-848 description (GET /rest/api/3/issue/RD-848) | read 2026-10-17
- RD-828 slice 2 cells; D-F1 is no code; slice 1 merged as b2eecdf | Jira RD-828 description and comments 39199-39411 | read 2026-10-17
- RD-837 hold text and :77 | Jira RD-837 description | read 2026-10-17
- F-821-1 cleared: round 3 installed 10-12 after gate 21 GO | Jira RD-821 comments 39348 and 39361 | read 2026-10-17
- RD-801 / RD-822 / RD-802 ticket text, alerts named | Jira RD-801, RD-822, RD-802 (GET issue + comments) | read 2026-10-17
- gate 19 verdicts RD-801 GO WITH FINDINGS (N-801-1), RD-822 GO; turns 18 and 19 | /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-10-12_nexusai_gate19_RELEASE.md lines 8 and 14 - Tuesday's tree, not yours | read 2026-10-17
- N-801-1 text | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-07-gate-batch19/body-0.md lines 9 and 29 | read 2026-10-17
- gate 20 RD-802 GO | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-08-gate-batch20/report.md line 18 | read 2026-10-17
- RD-847 lock base on the T9; T9 mounted | Jira RD-847 + HANDOVER-S99O.md §2; `ls /Volumes` | read 2026-10-17
- RD-737, RD-708, RD-675, RD-690 (slice 2's source tickets) all Release Ready | Jira RD-828 issuelinks (GET /rest/api/3/issue/RD-828) | read 2026-10-17
- RD-846 merged as PR #86; demo revision 0000100; group check unexercised; next work for lane O | /Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/HANDOVER-S99O.md §0, §4 | read 2026-10-17
- grant scope, quoted | /Volumes/Laptop-DEV/TUESDAY/0_Brain/tasks/EXPIRING-GRANTS.md table row 1 - Tuesday's tree, not yours | read 2026-10-17
- undelivered card nexusai-rd846-build-broken-demo-deploy-1013, choice b | `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh show nexusai-rd846-build-broken-demo-deploy-1013` - Tuesday's tree, not yours | read 2026-10-17
- C-40 :232, C-57 :418, C-63 :589, C-186 :2009, C-190 :2062, C-199 :2158 | /Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md | read 2026-10-17
- load 7.62 | `uptime` | read 2026-10-17

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-17 06:26

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-O -> Tuesday] QUESTION: plan confirmation` with: your seat identity facts (pane id, cockpit name, claude pid); what you read; your first `git ls-remote origin refs/heads/main`; whether Docker is up (`docker info`); your launcher preflight warnings VERBATIM; your RD-848 guard design (where it lives, how it resolves globs); your C-P1 label proposal. Then start QUEUE 1 unless Tuesday says otherwise within 15 minutes. Your wake is Tuesday's mail plus a tap.
-- Tuesday
