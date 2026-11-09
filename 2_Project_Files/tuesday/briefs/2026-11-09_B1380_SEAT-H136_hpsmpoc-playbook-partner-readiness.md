From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED** = printed by a named instrument; **DERIVED** = source reading, not run; **RELAYED** = read in another file; **UNMEASURED** = nobody has.

# BRIEF B1380 | SEAT-H136: HPSM-POC, BUILDER (OPUS): PLAYBOOK PARTNER READINESS (Kam 2026-11-09 20:19, item 2). NEW BRANCH `b1380/hpsmpoc-playbook-partner-readiness` FROM MAIN `2075486b011057ea496b9ea1b6ae2974e3e2307b`. COMMITS AS NEEDED, PLAIN PUSHES OF THAT REF ONLY, NO PR. NOT MERGED, NOT DEPLOYED.

## KAM'S WORDS (live board 2026-11-09 20:19:58, verbatim)
"the Partner readiness on our site is wrong! we missed the changes in questions from the layout. Please review the layout pages and change the partner readiness questions and change title to Playbook Partner Readiness." He wants it "before tomorrow morning if possible". A parallel lane (B1381, pane `Datasec/HPSM-POC-H137`) builds a Demo Walkthrough at the same time: see PARTITION.

## BINDING HOLD
UAT is on hold (Kam 2026-11-06 10:12) and HPSM-POC deploys nothing. You touch no hosted host: no `az`, no docker push, no ssh, no HTTP to any hosted, demo or UAT host. You open no PR; Tuesday opens, gates and lands it. No Jira write, no message to any human. Never delete (quarantine to `.tools/b1380/_quarantine/`); no force-push, amend, reset, rebase. This phase builds no integration with HP tools.

## THE SPEC (read WHOLE first; it is a DERIVED reading at main 2075486 — re-verify every file:line at your clone)
- `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_docs_1109/hpsmpoc/A_partner_readiness_spec.md` (the analyst's build spec: layout statements verbatim, diff, file map, migration risk, build order, tests).
- Layout source of truth: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1109/f-84472617d43a_HP_Cyber_Security_Services_Playbook_v2_1_Layout_Alignment.html` (`READINESS` ~L732, `readinessGroups` ~L791, `partnerReadiness()` ~L805). Read-only.
- UAT cross-reference (RELAYED): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_docs_1109/hpsmpoc/D_uat_plan_digest.md` — cases UAT-003/004, 070, 086-090.

## TUESDAY'S DECISIONS ON THE SPEC'S OPEN QUESTIONS (defaults; Kam may overrule — build them, record each in STATUS)
1. Q1: the layout's 16 statements REPLACE the deck's for NEW assessments (Kam's instruction is explicit). Old runs keep their own package and still render their own answers.
2. Q2/Q8: the PAGE/MODULE/PDF/document titles and headings become **"Playbook Partner Readiness"** (results page: "Playbook Partner Readiness results"). The short sidebar label stays "My readiness" as the layout has it.
3. Q3: area names = the layout's `readinessGroups` (Strategy and engagement / Assessment and expertise / Implementation and delivery / Managed service and growth), grouping by position as the layout does.
4. Q4/Q5: keep the existing band labels, band summaries and 30-day plans (scoring and bands are unchanged); use the layout's intro text. Add the layout's/UAT-089 wording that the result is **self-assessed and not a verified HP competency or accreditation**.
5. Q6: NO reset or reseed of any hosted data. Change the API demo SEEDER code to the new package as the spec says (code only), with the first 11 ticked as the layout's seed state does; nothing runs against a hosted DB.
6. Q7: icons from the app's existing icon set, nearest meaning.
7. The layout calls its statements "illustrative" / "draft working statements": carry that caveat on the page as the layout does; never present them as official HP criteria.

## THE BUILD (from the spec's section on build order; you own the shape)
A NEW content-package version (the spec proposes 0.7.0) with NEW question IDs; never edit or delete 0.3.0-0.6.1. API seed + web copies + recorded hash + registry; screens show the package a RUN was answered against, not the latest (the hidden bug the spec names); pin the customer Firmware task to its old package so its checklist is unchanged; every title location in the spec's title list; demo seeder code. Tests: new content equals the layout statements byte-for-byte (by program, from the layout file); scoring identical; an old-package run still shows its own answers; Firmware task unchanged; existing report tests pass.

## PARTITION
- **Yours:** content packages (api SeedContent + web content/packages + client copies + registry/hash), readiness assessment/overview/result pages and components, the dashboard readiness tile, title strings for readiness, the API demo seeder's readiness part, tests for these.
- **NOT yours (B1381 owns):** the initial/entry screen, sign-in screen, app shell/layout mount, any new walkthrough panel component, `web/src/components/shell/**` EXCEPT a readiness title string there (if you must change one, name the file:line in STATUS before committing so Tuesday can tell B1381). Never `.github/**`.
- If a file you need is on B1381's side: STATUS line `NEEDS-SHARED <path> <why>` and continue on the rest.

## CHECKS
Every web and api build/test the project's CI runs for the paths you touch (read `.github/workflows/ci.yml` at your clone; print each job's predicate), at main and at your head, counts compared by program; lint + typecheck rc 0; Playwright/e2e for the readiness pages if CI runs them. The SQL Server shard is NOT RUN by you unless the project's own scripts run it locally without docker grants you don't have: say which. A red that is not yours: name it with its cause at main too. Heavy jobs: load1 is noisy tonight (Spotlight indexing the new drive); run heavy jobs serially within your seat.

## HOUSEKEEPING
- Project dir: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC` (the NEW drive; anything naming /Volumes/Laptop-DEV is stale and that drive is not mounted). Own clone `.tools/b1380/repo` by URL with the deploy key `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/3_Access_Keys/github_deploy_rw` as repo-local `core.sshCommand`. Do not use or modify `2_Project_Files/` (it is a stale checkout). Dev servers/listeners only on ports **9640-9649**.
- STATUS: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-09_B1380_STATUS.md`. FIRST line `PROGRESS B1380: b1380/hpsmpoc-playbook-partner-readiness HOLD`; a `WORKING: <part>` last line after every part, at least every 20 min; a PRIOR WORK section (git log on the readiness files, open PRs, any Jira ticket on readiness via the project's reader if it exists). Finish with `READY B1380: <head sha40>` and a section listing every file changed, every decision applied, every check with its predicate and counts, and anything not run. HARD STOP 06:00 AEDT 2026-11-10: push what is green, write what is not.
- Commit messages: plain ASCII, no B-numbers, no person names; end with the attribution line your session reminder gives.
- Shell: no `cd`; absolute single-quoted paths (the `!`); `git -C`; `python3 -I -B`; `/usr/bin/grep -i` with a control for every count.

READ-WHOLE-BY-TUESDAY: DONE 2026-11-09 (drafted and read by Tuesday s259)
