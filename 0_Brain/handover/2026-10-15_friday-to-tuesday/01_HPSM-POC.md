---
date: 2026-10-15
type: handover
project: Datasec/HPSM-POC (+ HPSM records)
from: Friday → Tuesday
client: Datasec only
status: live
---

# HPSM-POC: handover (Friday → Tuesday, 2026-10-15)

## What it is (one paragraph; the project's CLAUDE.md is the source)
The HP Security Services Playbook **Digital POC**: a US$50,000 not-to-exceed, 12-week PROVE-stage proof of concept HP scaled
down from the original HPSM platform MVP (SOW-01, sibling folder `../HPSM/`), aimed at a **December 2026 event**. Flow:
customer profile → guided assessment → deterministic rules/scoring → findings → HP/HPSM recommendation → remediation roadmap →
AI narrative (from approved structured findings only) → branded executive PDF → next-engagement recommendation → automation
metrics. Principle: **rules decide WHAT; AI explains WHY and HOW** (SOW §3.1). End customer is HP: HP-NDA material never
goes into a code repo, and nothing goes to HP or any human without Kam's explicit send.

## Where everything is
| What | Where |
|---|---|
| Project root | `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/` |
| Code repo | `2_Project_Files/` → `git@github.com:datasecau/HPSM-POC.git` (.NET API + web; ASP.NET Core) |
| Records repo | the project root itself → `git@github.com:datasecau/HPSM-POC-analysis.git` (records seats push here) |
| Boot reads | `CLAUDE.md` → `1_Project_Definition/CLARIFICATIONS.md` (settled rulings, C-nn) → `1_Project_Definition/Questions_and_Answers/00_MASTER_QA.md` (ask nothing already answered) |
| Briefs + STATUS | `1_Project_Definition/Briefs/` (`<date>_B<nnn>_SEAT-<X>_<slug>.md` + `<date>_B<nnn>_STATUS.md`); worktrees at `2_Project_Files/.tools/wt-*` |
| Jira | project **HPSMPOC** (id 10588), kanban board **606**: https://team-1634009483756.atlassian.net/jira/software/c/projects/HPSMPOC/boards/606 |
| Hosted site | `app-hpsmpoc-web-demo-en46o7.azurewebsites.net` (RGs `hpsm-poc-demo-rg` / `hpsm-poc-sm-rg`, Datasec agent-controllable env; the project's SETUP_RUNBOOK names the tenant/SP) |
| Logins | `Launch_Claude.command` (own gh/az config dirs), `3_Access_Keys/` deploy key, `4_Credentials/.env` |
| Backlog | `BACKLOG.md` + the Jira board; Friday's 10-13 board screen: `FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_hpsmpoc_board_screen.md` (in the shared repo) |
| Analysis lesson | `0_Brain/learnings/2026-09-27_hpsmpoc-every-hp-ask-is-its-own-email-plus-a-register.md` (P-tier, Datasec/HPSM-POC) |

## State at handover (measured 2026-10-15 ~10:5x AEDT)
- **main = `d916baf7`** (PR #155, B248: pins `System.Security.Cryptography.Pkcs` 9.0.21 against GHSA-846f-f764-76mx High
  + GHSA-2fmv-rv2c-59x7 Moderate). **main ci on d916baf = run 38470487072 SUCCESS.** No open PRs.
- Before it: **#154** merged 10-14 07:23 → `ce40ce07` (B244 Lane 1 API/tests: -225/-250/-246/-134 + -229 after fix round
  B246 and deltas gate B247 GO WITH NOTES). #153 closed as contained in #154.
- **Hosted = `dc136e68`** (B238, deployed 10-13 18:23, live-checked; ADDENDUM-1 accepted a `.zst` checker gap, records C-104).
  **Kam froze hosted for 14 Oct ("NOTHING to hosted until Kam names a window").** Ask him for the next window before any
  hosted deploy, even with the push-to-demo grant re-confirmed.
- Code Security + CodeQL default setup: **enabled** (Kam turned them on 10-14 06:5x). CodeQL on a PR sometimes does not start on
  reopen. Friday's fix was an **empty commit with the identical tree**, pushed via the API (fast-forward, no force).
  That re-triggers it, and the merge check confirms the merged tree equals the gated tree.

## OWED, in priority order
1. **Records seat (HPSM-POC-analysis):** Jira transitions + comments for **-225 / -250 / -246 / -134 / -229 → done**;
   comment lines for B244/B245/B246/B247/B248; **file tickets:** T-0 / B246-1 *reverse race* (ImportEndpoints.cs:176-186),
   T-1 *silent row loss*, T-2 *false Critical log*, B246-2 *stale comment*; **B243 notes N-1..N-10**; -225's **Lane-2
   remainder** (FeedbackEndpoints.cs:57 + JiraRestMailSink.cs:131).
2. **B248 FOUND-1 (needs Kam's window):** the running Pkcs DLL is the ASP.NET Core *shared framework's*, not the package.
   Real exposure is the .NET runtime. Runtime 10.0.13 fixes both CVEs; CI runs 10.0.13; the laptop's `.tools/dotnet` is 10.0.12;
   **the hosted App Service runtime is UNMEASURED.** Measure it when the freeze lifts and ticket it via the records seat. Tell Kam.
3. **Lane 3 (CI):** -227, -155, -224 (and -218's 30 Nov braces exception is already merged as #151; -218 itself had a HARD DATE of 1 Nov).
4. **Kam's 58 board items as GROUPED cards**, plus a lane-2 words card (9 sentences) **before any hosted deploy** that ships new words.
5. Close the ~10 done-but-open Jira tickets (the 10-13 board screen lists them).

## How Friday ran it (keep what works)
- **Tier-1 changes:** build seat → independent QA gate seat (fresh, never the builder) → coordinator's completion check →
  PR → `merge_when_green.sh <repo> <PR> <head-sha>` (pinned head; it refuses if the head moves) → read main ci to the end.
- **Tier-2 (small, e.g. a package pin):** build seat → the coordinator reviews the diff AT SOURCE (GitHub compare API) and re-runs the
  red-proof → PR → merge_when_green.
- After every merge: confirm via the commits API that the parent and tree match the gated tree. Then main ci. A red main ci is
  never dismissed; it is fixed in code (B248 was exactly that: an advisory published the night before turned main red).
- Every brief ends with a fixed final-line token (`READY FOR GATE: <branch> @ <sha>`, `READY FOR REVIEW: …`, `DONE: …`,
  `STOPPED: NEEDS <seat>`). The watcher matches it. **Check the token shape BEFORE launch** (ledger w=3, 10-13).
- Every HP ask is its own email plus a register row (the P-tier lesson above).
- Ports: each seat gets its own 10-port block (e.g. 6930-39). Never share.

## HPSM (the parent project): Friday's records claim moves to you too
Friday held a claim on `Datasec/HPSM` for records work: the 09-23 "added" archive filing and the 09-29 HP meeting
transcript → HPSM records. **Measured today:** the HPSM project root (records repo, `datasecau/HPSM-analysis`) on the laptop
drive is checked out on **`records/b08`** (last commit 2026-10-02) with **54 uncommitted paths**. The T9's copy is on `main`
(2026-09-17) with 31. **They have diverged. Do not "fix" either by copying files.** Both sides' uncommitted work is backed up in
`/Volumes/KK_T9_External_HDD/_SYNC_2026-10-15/step1_uncommitted/<drive>/!CODING/Datasec/HPSM/` (`tracked.patch` +
`modified_and_untracked.tgz` + `meta.txt`). Both repos now hold each other's commits under `refs/remotes/t9-drive-2026-10-15/*`
(laptop) and `refs/remotes/laptop-drive-2026-10-15/*` (T9). Reconciling them is a records-seat job, and a Kam question if a
choice is needed.

**RULED by Kam, 2026-10-16 (terminal to Friday), verbatim: *"HPSM on laptop drive is the master, not the t9."*** The laptop
drive's HPSM (on `records/b08`, with its uncommitted work) is authoritative. Never copy or sync the T9's HPSM over it. The T9 copy
is a stale backup: its `main`-only commits are already present on the laptop as `refs/remotes/t9-drive-2026-10-15/*`, for
reference only. The 2026-10-15 sync added only files the laptop lacked and overwrote nothing. It deliberately left out the T9's
pre-separation `6_Policy_Composer`, which the laptop quarantined twice (09-25, 10-02).
