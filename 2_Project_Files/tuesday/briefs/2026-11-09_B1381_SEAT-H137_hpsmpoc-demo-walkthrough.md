From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED** = printed by a named instrument; **DERIVED** = source reading, not run; **RELAYED** = read in another file; **UNMEASURED** = nobody has.

# BRIEF B1381 | SEAT-H137: HPSM-POC, BUILDER (OPUS): DEMO WALKTHROUGH RIGHT-HAND PANEL (Kam 2026-11-09 20:19, item 3). NEW BRANCH `b1381/hpsmpoc-demo-walkthrough` FROM MAIN `2075486b011057ea496b9ea1b6ae2974e3e2307b`. COMMITS AS NEEDED, PLAIN PUSHES OF THAT REF ONLY, NO PR. NOT MERGED, NOT DEPLOYED.

## KAM'S WORDS (live board 2026-11-09 20:19:58, verbatim)
"add the demo and links from the other attached HTML. this should be a column that pops up to the right and is launched when you select a new option from the initial screen called Demo Walkthrough. When selected, the user should be logged in as a partner and have all the options from the demo. These are the priority and I would like the changes before tomorrow morning if possible." A parallel lane (B1380, pane `Datasec/HPSM-POC-H136`) rebuilds Partner Readiness at the same time: see PARTITION.

## BINDING HOLD
UAT is on hold (Kam 2026-11-06 10:12) and HPSM-POC deploys nothing. You touch no hosted host: no `az`, no docker push, no ssh, no HTTP to any hosted, demo or UAT host. You open no PR; Tuesday opens, gates and lands it. No Jira write, no message to any human. Never delete (quarantine to `.tools/b1381/_quarantine/`); no force-push, amend, reset, rebase. This phase builds no integration with HP tools.

## THE SPEC (read WHOLE first; DERIVED at main 2075486 — re-verify every file:line at your clone)
- `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_docs_1109/hpsmpoc/B_demo_walkthrough_spec.md` (14 steps verbatim, link/option tables, route map, design, security notes, tests, lane split).
- Demo source of truth: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1109/f-1c6fabb2c95c_HP_Security_Services_Playbook_v2_0_Aligned_Partner_Demo.html` (walkthrough ~L564-577). Read-only.
- UAT cross-reference (RELAYED): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_docs_1109/hpsmpoc/D_uat_plan_digest.md` — UAT-083 (guided steps, each "Open this step" changes no data, no false certification wording).

## SECURITY RULE (non-negotiable)
"Logged in as a partner" REUSES the existing Partner sign-in path the spec names (the same form post / client sign-in), plus a client-side flag that opens the panel. **NO new endpoint, route or identity that mints a session, and nothing on a GET.** A test asserts the set of auth routes is unchanged versus main. Hidden when the Entra sign-in mode is active. If this cannot be done without a new auth path: `STOPPED: NEEDS TUESDAY` — do not build one.

## TUESDAY'S DECISIONS ON THE SPEC'S OPEN QUESTIONS (defaults; Kam may overrule — build them, record each in STATUS)
1. Q1 "all the options from the demo" = the 14 steps with every in-app jump/link, in the partner view. Do NOT re-add the Good/Better/Best sidebar entry or role switcher (removed on purpose; a test guards it). Steps whose target is missing (framework alignment) show the step text with "not in this build yet" and no dead link.
2. Q2 the on-screen message shows; the talk track sits in a collapsed "Presenter notes" section, closed by default.
3. Q3 environments: laptop/dev and UAT builds; hidden in Entra mode.
4. Q4 the title screen is the panel's first step, not a full-screen overlay.
5. Q5 the app's own sample customer (looked up at runtime) stands in for "Rocklea Council"; the text names the app's customer, never a hard-coded id.
6. Q6 "Answer just one" is reworded to VIEW only: no walkthrough step writes data (UAT-083). The panel never submits a form.
7. Q7 "Demo Walkthrough" is a new option on the initial screen beside the existing level choices.
8. Q8 use the app's own PDF/report; do not port the demo's.
9. Q9 remove the person's name from the title step.
10. Q10 Exit closes the panel and leaves the user signed in as partner on the current page.
11. Talk-track claims the spec flags (customer name not sent to the AI; "maps to a named HP Security Manager policy setting"; pricing): check each against the code; keep only what the code proves, otherwise soften to what is true and list each change in STATUS.

## THE BUILD
Content module (the 14 steps as data), the panel component (~380 px right column, pushes content, collapsible, drawer on narrow screens, Back/Next/Exit, jump list, step persisted in sessionStorage), the entry-screen option, the one mount point in the main layout, unit + e2e tests (open from entry -> signed in as partner -> panel visible -> each jump navigates -> no write requests issued -> exit). You may run your own sub-agents in parallel inside YOUR branch per the spec's lane split, as long as one commit history results and every check below passes.

## PARTITION
- **Yours:** the entry/initial screen and sign-in screen option, the app shell/layout mount point, new walkthrough files (content, panel, hooks, styles), e2e/unit tests for these.
- **NOT yours (B1380 owns):** content packages (api SeedContent, web content/packages, client copies, registry), readiness pages/components, the dashboard readiness tile, the API demo seeder. Walkthrough step text that names the readiness page uses the title "Playbook Partner Readiness". Never `.github/**`.
- If a file you need is on B1380's side: STATUS line `NEEDS-SHARED <path> <why>` and continue on the rest.

## CHECKS
Every web (and api, if touched) build/test the project's CI runs for the paths you touch (read `.github/workflows/ci.yml` at your clone; print each job's predicate), at main and at your head, counts compared by program; lint + typecheck rc 0; Playwright e2e for the walkthrough. A red that is not yours: name it with its cause at main too. Run heavy jobs serially within your seat (load is noisy tonight: Spotlight indexing the new drive).

## HOUSEKEEPING
- Project dir: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC` (the NEW drive; anything naming /Volumes/Laptop-DEV is stale and that drive is not mounted). Own clone `.tools/b1381/repo` by URL with the deploy key `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/3_Access_Keys/github_deploy_rw` as repo-local `core.sshCommand`. Do not use or modify `2_Project_Files/` (stale checkout). Dev servers/listeners only on ports **9650-9659**.
- STATUS: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-09_B1381_STATUS.md`. FIRST line `PROGRESS B1381: b1381/hpsmpoc-demo-walkthrough HOLD`; a `WORKING: <part>` last line after every part, at least every 20 min; a PRIOR WORK section. Finish with `READY B1381: <head sha40>` and a section listing every file changed, every decision applied, every check with its predicate and counts, screenshots of the panel (save under `.tools/b1381/shots/`), and anything not run. HARD STOP 06:00 AEDT 2026-11-10: push what is green, write what is not.
- Commit messages: plain ASCII, no B-numbers, no person names; end with the attribution line your session reminder gives.
- Shell: no `cd`; absolute single-quoted paths (the `!`); `git -C`; `python3 -I -B`; `/usr/bin/grep -i` with a control for every count.

READ-WHOLE-BY-TUESDAY: DONE 2026-11-09 (drafted and read by Tuesday s259)
