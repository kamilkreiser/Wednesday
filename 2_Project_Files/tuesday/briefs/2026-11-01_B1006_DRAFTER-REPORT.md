STARTABLE: YES (after Tuesday stamps the 8 slots; head, main and PR unmoved at the draft)

# B1006 drafter report (SEAT-G247, short tier-1 check, round 3 of PR #266)

## BLUF
Kit written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1006_SEAT-G247_hpsmpoc-266-round3-short-check-tier1.md` (50 lines, 7 checks C1-C7, shaped on the B997 kit and cut down). Target 45 minutes, hard stop 75. Opus, row G1. Ports 9420-9429. The check judges only that `6322d20a` closes B997-1 and changes nothing else; it carries B997's N-4 and N-7 as Notes, not findings.

## Facts re-measured (instrument, control)
- PR #266 / branch / main (`gh api -X GET pulls/266`, `ls-remote`): open, draft false, head `6322d20adf22b18ac3bc3edcd0b0edbeead3eaf7`, base `d0eff4ca637b8959dd205adc0b77e8111b60280a`, `mergeable_state` clean, commits 4, +412 -34, changed_files 9; `refs/pull/266/merge` `cfb8963ba9298a80a1f3172af11198b0348027f1`. Control: the branch and head `ls-remote` lines agree.
- Model: `grep -n` on routing gives G1 row at line 108, G-cap at 111 (the hook's case-sensitivity advisory applies: both counts were positive, so not false zeros). `models_latest.json` line 17 `claude-opus-5-5`. `brief_seat.sh` line 24 defaults to Opus (read).
- Ports: lsof on 9420-9429 = 0 listeners (a `python3 -I -B` bind on 9429 read 2 lines, so the instrument answers; also 9400-9599 = 0 listeners, all-TCP listeners 14). Word-boundary scan `\b942[0-9]\b` over 221 non-`.pre-` briefs dated 10-30 to 11-01: 0 hits. Controls: `\b949[0-9]\b` hits the composer B1001 kit; `\b948[0-9]\b` hits B1000 and B1002; `\b944[0-9]\b` hits B995. 9470-9489 and 9490-9499 are taken (so I did not use the neighbouring decades); 9500+ are other kits'. Panes: tuesday, `Datasec/HPSM-POC-G245`, `Datasec/MPS-M53`, fleet-monitor.
- Collisions: `.tools/b1006` and `.tools/wt-b1006-*` absent (ls: no such file). Present in `.tools`: b997, b998, b1002 (+ its worktrees). B1003 live in G245, no ports.
- CI file at the head (`gh api -X GET contents ...ref=6322d20a`, 679 lines): predicate lines written into C6 (api :33/:86/:88, SQL Server parts :166/:274/:314 floors 100 and 110, aggregate :354, web build :372/:426, unit :451/:478, e2e :484, web :527, infra :576, secrets :630, dependency review :666; line 1 says no deploy job).
- Kit file checks: four-underscore line count 8 (7 slots + last line); non-ASCII lines 0.
- Landing rule: CLARIFICATIONS.md line 138 is the log entry of an earlier head-pinned squash (`grep -n -i 'squash-merged head-pinned'`), not a rule statement; the kit tells the seat to also grep `head-pinned` and quote the rule line.

## D-decisions
- D-1 The seat may READ and COPY the B997 gate's tools (stub, client, c4b, lock) but `.tools/b998` is read-forbidden (builder's work is a claim). The B998 builder itself copied from b997, so I treated b997 as a prior gate's kit.
- D-2 The EF schedule is CARRIED from the round-2 gate (`api/` is main's, proved by C1), not re-measured. This saves a dotnet build and the NuGet dependency; stated as UNMEASURED in the kit.
- D-3 Round-count text: two NO GO hits expected (B994, B997), "third and last round, allowed once by the product owner's 2026-11-01 round-cap ruling"; the cap row (:111) is quoted as the reason the ruling is needed.
- D-4 Added a limits table (C2) against main for all methods: this is the only way to prove "every write limit byte-equal" and "HEAD equals main" beyond the AST hashes; kept to one scratch vitest.
- D-5 Added a dead-upstream GET row (the row that can fail) so the headline 90 s property is re-seen after the HEAD edit, plus C7 squash-file checks with positive controls and a stale-count list (13 files, 623, 3689, 261).
- D-6 No fresh `npm run build` of main: HEAD control on 9422 is optional; the defect number is quoted from B997 S9 (30.08 s, 1 call).

## Q-questions for Tuesday (default in brackets)
- Q-1 Port block 9420-9429 [yes].
- Q-2 Target 45 / hard stop 75 minutes, CodeQL wait capped at the hard stop [yes].
- Q-3 Accept N-4 (`bff.ts:177`) and N-7 (`bff.test.ts:154`) as Notes and that the squash body may say once that a HEAD keeps main's 10 s and one call [yes].
- Q-4 Accept the carried (not re-measured) EF schedule [yes; otherwise add a dotnet step and about 15 minutes].
- Q-5 The kit's C3 lists test paths for the 7 PR files by name for two of them (`EngagementsList.wake.test.tsx`, `formMeter.test.ts`) that I did not locate under `web/src`; the kit tells the seat to take the 7 by program from the diff [accepted by default].

## UNMEASURED
- Whether `git diff --name-only d0eff4ca 6322d20a` lists exactly the 9 paths (read only from the PR counts).
- The B998 builder's claims (all of them), the 20 of 20 check-runs (taken from your note; not re-read), the hosted unit count 3690.
- That `.tools/b997/schedule.json.orig` and the copied scripts exist with the names given (named from the B998 STATUS listing; `ls .tools/b998` showed the copies).
- The launch line was copied from the B997 kit; `launch_when_cool.sh` exists at the path used.

## Outside-the-fences disclosure
Read-only: the briefs directory, B997 and B998 STATUS, model-routing.md, models_latest.json, brief_seat.sh header lines, CLARIFICATIONS.md (grep), `gh api -X GET` of the PR, the contents of `ci.yml` (written to the session scratchpad, not a project file), `ls-remote` of the shared repo, lsof, a 9429 loopback bind for a control (freed on exit). No card read, no Jira, no hosted host, no az. Wrote only the kit and this report.
