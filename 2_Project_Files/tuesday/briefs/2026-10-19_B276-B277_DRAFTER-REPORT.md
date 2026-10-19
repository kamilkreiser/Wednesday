# B276 / B277 DRAFTER REPORT (wave 1 of the 2026-10-19 ticket sweep)

Drafter: read-only sub-agent for Tuesday (Datasec only). Wrote only the three files in `briefs/` named B276, B277 and this report. No Artifact/Docs/mail/chat tools, no git write verbs, no Jira/gh writes, no HTTP, no az, no docker. Did not open `fleet/briefs_staged`. Read `.env` files only by `grep -c` of two variable names (counts).

## What I read
- The sweep `0_Brain/projects_index/2026-10-19_ticket-sweep-hpsmpoc-composer.md` whole.
- B274 brief whole (shape: REFUSE, BLUF, READ FIRST, BASE/IDENTITY, Parts, HOLDS, STATUS, last line, STAMP); B273 brief lines 1-60 and 100-141 (identity, HOLDS, stamp, SELF-CHECK); B155 brief whole (the Composer seat shape); `brief_seat.sh` head (lines 1-50); B275 drafter report head.
- Not read: B152/B154 STATUS (used the B155 STATUS top only), B265 STATUS, any Jira ticket, any code at origin.
- Composer newest seat brief in Tuesday's folder is B155 (and B154); no B15x Composer brief newer than that.

## What I measured (commands)
- Brief numbers free: `ls` of Tuesday `briefs/` and both projects' `Briefs/` grepped for B276/B277 -> 0 hits (B275 is the newest, QuickQuote).
- Composer: root `.git` exists, branch `main`, `git remote` -> 0 remotes; code repo origin `datasecau/Datasec-Security-Composer`; local code HEAD `0b2fca43` (2026-09-27), stale; no `.github/` locally; `scripts/` holds `up.sh`, `health-check.sh`, `ci.sh`; `PC_CI_EDGE_PORT` default 18180 in `ci.sh`; `BACKLOG.md` 314 lines, 308 numeric ids; CLARIFICATIONS 1,398 lines, 74 headings, last C-74; `history.md` 1,754 lines, newest B147; rows 84 and 140 text; rows 66 and 70 already end with the Friday C5 sentence; `b47-check-off-guide.cjs` exists in `Briefs/2026-10-03_B47_evidence/`; `3_Access_Keys` has `composer_github_deploy_rw`; no lock helper in `.tools`.
- HPSM-POC: code origin `datasecau/HPSM-POC`; local code HEAD `8869b1a9` (2026-09-23), stale (`web/e2e` only `smoke.spec.ts`, api tests only `HealthEndpointTests.cs`); local CLARIFICATIONS 192 lines, 30 headings; `.tools/b198/lock.sh`, `.tools/b265/`, `.tools/b274/` exist; keys `github_deploy_rw`, `analysis_deploy_rw` present.
- `.env` name counts: AGENTMAIL_API_KEY 0 in both projects; JIRA_API_TOKEN 1 in HPSM-POC, 0 in Composer.
- Slot check: both files' slot grep prints 0 for the self-match-safe pattern; positive control with a scratch line prints 1.

## Slots left for Tuesday
B276: `CODE_MAIN_SHA` (sweep says `befd45e7`), `RECORDS_MAIN_SHA` (sweep says `47a9896e`), `MODEL`, `STAMP_TIME`, `PANE`, `PANE_SUFFIX`, `PORT_BLOCK`, `LOCAL_START_SECONDS`, `NEXT_C`, `B_NUMBER_CONFIRM`; rulings R-W1-1 to R-W1-4.
B277: `COMPOSER_MAIN_SHA` (sweep says `230f9fab`), `MODEL`, `STAMP_TIME`, `PANE`, `PANE_SUFFIX`, `PORT_BLOCK`, `RETRY_SECONDS`, `B_NUMBER_CONFIRM`; rulings R-W1-5 to R-W1-8.
I used a new slot grep (`@SLOT:[A-Z0-9_]+@`) because the older `@[A-Z][A-Z0-9_]*@` pattern does not match a colon. Tuesday's stamping step must use the new pattern, and keep `.pre-stamp` copies.

## Doubts
1. **-246 N-4 conflict (top for B276):** the sweep says the next HPSM deploy seat (B273) satisfied N-4; B274's FOR TUESDAY still lists it as owed, and B273's brief forbade records. The brief makes the seat resolve it at source and defaults to comment only.
2. **Key mapping:** I treated -288..-292 as B274's T01..T05 (T04 = -291 Pkcs comment) from B274's creation order and the sweep's file lists; unverified against Jira. -227's Done-when is unread by anyone; if it needs CI, the brief leaves the ticket open.
3. **Composer records are local-only** (no remote), so CL0 is a local branch commit, and Tuesday must accept that (R-W1-5). The CL0 row lists are the sweep's, not mine; I read only rows 66, 70, 84, 140. The ruling text for Friday C5/C9 may not exist as C-entries; the brief tells the seat to leave those rows and list them.
4. Composer `gh` identity is unmeasured (I assumed `kamilDatasec` from the HPSM sister project, hedged in the brief). Local code checkouts of both projects are stale, which the briefs say.
5. #84 may already be fixed upstream, or may not reproduce; the brief requires the seat to try three fresh runs before changing anything. The #140 fix is a new v2 file, leaving B47's evidence untouched.
6. Both briefs run past a plain ~250 lines only in line width, not count (116 and 90 physical lines, long lines); a very long line may be harder to review than the B274 style.
