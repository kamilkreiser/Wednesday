From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED** = printed by a named instrument; **DERIVED** = source reading, not run; **RELAYED** = read in another file; **UNMEASURED** = nobody has.

# BRIEF B1387 | SEAT-H140: HPSM-POC, BUILDER (OPUS), FIX ROUND for the gate's NO GO (round 1 of 2) on branch `b1380/hpsmpoc-playbook-partner-readiness` @ `e4bcb9ba70e08e9acb0748f6e650f39002ff0224`. FORWARD COMMITS ON THAT BRANCH, PLAIN PUSHES OF THAT REF ONLY, NO PR. NOT MERGED, NOT DEPLOYED. Written 2026-11-09 22:41 AEDT.

## READ WHOLE FIRST (read-only)
1. The original builder brief: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-09_B1380_SEAT-H136_hpsmpoc-playbook-partner-readiness.md`. Every hold, decision, partition, check and housekeeping line binds you (UAT hold, nothing hosted, no PR, no Jira, no message to any human, never delete, no force-push/amend/reset/rebase, ports 9640-9649, no `cd`).
2. The gate's verdict: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-09_B1384_STATUS.md` (first line and findings B1384-1 to -4 at about lines 136-139) and `.../2026-11-09_B1384_evidence/residue.md` (read whole).
3. The previous builder's STATUS: `.../2026-11-09_B1380_STATUS.md` (its decisions and checks table).

## THE FIX (closes the residue; nothing else)
1. **B1384-2 (Major):** the results page of a run on the NEW statements (content 0.7.0, the provisional set) shows the layout's caveat that these are draft working statements, not official HP accreditation criteria, beside the existing self-assessed note; a run on the deck's 0.3.0 statements does NOT show it. Copy the caveat's wording from where it already renders (the runner / My readiness hub / module page / 0.7.0 PDF) so every surface says the same thing: name the source line in STATUS. Unit tests for both cases (new run shows it, old run does not) and an e2e assertion on the results page. Prove each new test goes RED with your fix removed in a copy, then GREEN.
2. **B1384-4 (Minor):** the partner card titled "Readiness self-assessment" (`web/src/content/partner/partner-showcase.v0.1.0.json:31`, client copy `:75`, per the gate). The product owner asked for the title "Playbook Partner Readiness". First read how the project versions and hashes content packages (registry, hash, PROVENANCE, the rule the original brief applied to readiness packages). If that package may be edited in place under the project's own rule, retitle it and regenerate the client copy with `node web/scripts/client-content.mjs`; if the rule says a changed package needs a new version, follow the rule exactly as the 0.7.0 work did; if neither is safe tonight, leave it and write the reason in STATUS. Say which you did.
3. **B1384-1 (Minor):** your STATUS carries a proper `## PRIOR WORK` section (git log on the files you touch, open PRs; Jira: say "no project Jira reader; not searched").
4. **B1384-3:** nothing to build; where you re-run a figure the gate could not show, record it in STATUS.

## CHECKS
At your final head: every web and api check the original brief lists, by the same predicates, compared by program with the previous head e4bcb9b's numbers (in its STATUS) and with main: lint + typecheck rc 0, vitest, build, the readiness e2e set, dotnet build 0 warnings, the API tests you can run (SQL Server NOT RUN). A red not yours: name it with its cause at main.

## HOUSEKEEPING
- Clone: reuse `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1380/repo` (its branch is the one to fix; confirm `git status` clean and HEAD = e4bcb9b first; if not, STOP). Do not use `2_Project_Files/`.
- The gate seat G370 has finished and its servers are stopped; check `lsof` on 9640-9649 is 0 before you start one.
- The other HPSM gate (G371, walkthrough) runs in parallel on ports 9670-9679 in `.tools/b1385/`: not yours, do not touch.
- STATUS: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-09_B1387_STATUS.md`. First line `PROGRESS B1387: fix round on b1380 HOLD`; a `WORKING: <part>` last line after every part, at least every 20 min. **The LAST line of the file, when you finish, is exactly `READY B1387: <head sha40>` and nothing after it.** Finish with a section listing every file changed, each finding closed and how, every check with its predicate and counts, and anything not run.
- Commit messages: plain ASCII, no B-numbers, no person names; end with the attribution line your session reminder gives. Commit and push as soon as the fix is green (the drive dropped twice today: push early).
- HARD STOP 01:30 AEDT 2026-11-10: push what is green, write what is not.
- Shell: absolute single-quoted paths (the `!`); `git -C`; `python3 -I -B`; `/usr/bin/grep -i` with a control for every count.

READ-WHOLE-BY-TUESDAY: DONE (written by Tuesday s260; read back whole before launch)
