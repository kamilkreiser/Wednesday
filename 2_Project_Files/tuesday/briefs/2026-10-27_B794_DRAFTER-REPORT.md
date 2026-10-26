STARTABLE: YES

# B794 drafter report (MPS PR #128 tier-2 gate kit, seat Datasec/MPS-G167)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B794_SEAT-G167_mps-128-residue-rows-gate-tier2.md` (74 lines). Drafted 07:55-08:02 AEDT, clocks from `date`.

## BLUF
- The kit is startable once stamped: 8 four-underscore lines (S1-S7 plus the last line), `@[A-Z_]+@` count 0, non-ASCII 0, no person name, no card id. Controls: the slot grep fires on a planted `x ____ y` (1).
- Model Sonnet (`claude-sonnet-5-5`, `models_latest.json` line 23), row G2 `model-routing.md:109`, cap row `:111`; launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Ports 8810-8819, pane `Datasec/MPS-G167`, findings `B794-n`, STATUS path as commissioned, last line one of GO / GO WITH FINDINGS / NO GO as the templates.
- The gate MUST run (builder did not): the walk-cap retained kills and the five equivalents (Check 4), controls c1 and c2 and cw-weak for the restart row (Check 3). Added by me beyond the builder's list: K31b (decides whether the `null` priority row is a wish), a 10x timing run of the ticket-retry row (it waits 400 ms on a fake Jira beside a known flaky neighbour), T10-T12/T6/T7 plants (priority-cut), S02b (middle of the hosted-store warning).
- Notable state: CodeQL is ALREADY complete on the head (4 analyses, 0 results, 0 open alerts; all four `Analyze` runs and `dotnet` completed success at 07:56-07:58), so a clean GO is reachable; the gate still re-reads LAST.

## Facts re-measured (instrument, time)
- PR #128: `gh api pulls/128`, 07:56: open, not draft, head `aeb9a336e9a44ac5f79e66e367c54dcb144c0a02`, base `b8ae9011...`, 3 commits, 3 files, +472 -0, `mergeable_state` unstable at 07:56 (the `package` job was in_progress; `actions/runs/40398777816/jobs` at 07:58 shows all four jobs completed success).
- `git ls-remote` (read verbs, `--no-optional-locks`), 07:56: main `b8ae901113a39ce62b280e70f35c1ee50532095e` (unchanged since PR open); branch and `refs/pull/128/head` = head; `refs/pull/128/merge` `9cb97e92...`, whose tree `9ccf0c29` equals the head's tree (`gh api commits/<sha>`).
- `compare b8ae9011...aeb9a336`: ahead 3 behind 0; numstat by `pulls/128/files`: Feedback 162/0, WalkCaps 62/0, Edges 248/0. Commits `68de4ff0`, `c8447faf`, `aeb9a336`, one parent each, unverified.
- Blobs by `gh api contents ?ref=` `.sha`: three test files differ main -> head (88726434->b4736b8c, d9655c54->cfcb440f, 86aa19cc->310b5bf4); the four product blobs equal at both (aac80cbd, dca637f1, e7c6f862, 681c9cc4). Control: ref of 40 zeros answers 404.
- Check-runs on head: 9 (CodeQL, four Analyze, dotnet, web, python success; package completed by 07:58). Analyses 4, results 0; open alerts 0 (control: main analyses read 100 rows). Ruleset: code_scanning (errors / high_or_higher), empty required checks, deletion, non_fast_forward.
- `ci.yml` at main lines 31-43 read raw: `dotnet build MpsCalc.slnx -c Release` then `dotnet test MpsCalc.slnx -c Release --no-build`, 20-minute timeout; predicate written into the kit.
- Landing: `CLARIFICATIONS.md:809` (and `:854`) read: "squash with the head pinned (`--match-head-commit`, the MPS convention ...)"; control `zzz-no-such-7f3a` 0 hits. Repo squash settings `COMMIT_OR_PR_TITLE` / `COMMIT_MESSAGES`; merge and rebase also allowed (the kit forbids anything but the pinned squash). Project `CLAUDE.md:50-52` quoted.
- Added-lines non-ASCII: 0 on the diff (control printf with a non-ASCII byte: 1). One `http` literal (synthetic Jira site address in the ticket-retry row); builder disclosed it.
- Ports: `lsof 8790-8819` empty (rc 1); bind control on 8815 listed then freed (rc 1). Word-boundary scan of 89 non-`.pre-` SEAT kits for `88[01][0-9]`: 0 hits (control match 1, `a8810` 0). Panes at 07:58: `tuesday`, `fleet-monitor` only; `MPS-G167` count 0. No `G167`/`B794` in the briefs folder; `.tools/b794` and `.tools/wt-b794-head` absent (control `.tools/b160` lists); heavy-slot / git-lock dirs: 0 (control `b160` 1). Load 1.45 1.84 3.39 at 07:56.
- Round-class first lines read (head -n 1): B766 "NO GO round 2 of 2 = THE CAP", B763 "NO GO round 2 of 2", B765 "NO GO round 1 of 2 on the branch (... NO GO 4 before ...)", B748 round 1, B752 round 1.

## D-decisions (override at the stamp)
- D1. Class label: "a pinned row that does not turn red under the defect it names, or turns red for another reason, or can fail only by timing". Round 1 of 2 on this new PR per Tuesday's builder-kit stamp; a same-class Major in the new rows is reported for a card, not a build round (written into the kit as commissioned).
- D2. Cap overshoot (26 source rows, 33 listed names vs the builder kit's 30) is graded a Note, not a finding, with the three cheapest drops left as a candidate decision for Tuesday.
- D3. The `http` literal is a Note if the in-process `FakeJira` answers it (the gate must show it and show the literal already exists in base tests).
- D4. Landing restated as head-pinned squash (`gh pr merge 128 ... --squash --match-head-commit aeb9a336...`), done by Tuesday only.
- D5. Merge check uses the PR's own merge ref tree (equal to head tree) plus the legacy 3-argument `merge-tree` inside the gate's own clone only; `merge-tree --write-tree` forbidden everywhere.
- D6. Jira read is optional (Check 7f) with the gate's own in-process `urllib` call because `CLAUDE.md` names no read helper and the builder helpers are read-forbidden; "Jira NOT READ" is acceptable.
- D7. Time suggestion: target verdict 2.5 h, hard stop 4 h after Step 0 (about 70 short runs plus the CI line of 10-15 minutes); the absolute latest bound is Tuesday's to stamp.

## Q-questions for Tuesday (each with a default)
- Q-1. Is the class label above the right one to print on the verdict line? Default: yes, round 1 of 2.
- Q-2. Cap counting rule (source rows 26 vs listed names 33). Default: Note only.
- Q-3. Allow the gate's Jira GET (Check 7f)? Default: yes, GET only, optional.
- Q-4. Should the gate also run the MPSCALC-342 strip-one-character survivors (information only)? Default: priority-cut, run only if time remains.

## UNMEASURED by the drafter
Nothing was cloned, built or run. Every mutant outcome, the builder's red sets, 435/193/3158, the 7 m 16 s Api run, the claim that K19 needs the NBSP case, and the claim that the `null` priority row is equivalent are the builder's (RELAYED) or my hypotheses. The hosted `dotnet` job's content beyond its conclusion; whether `Analyze (csharp)` covers this head's C# (the analyses list carries 4 rows; the kit makes the gate show `commit_sha` and languages); the mutant line numbers (`:181-190`, `:126-141`, `:302-320`, `:60-61`, `:200`, `:210`, `:219`, `:381`) are the builder kit's, not re-read by me. The kit's pointers to earlier gate STATUS line ranges (B766 and B765 and B763) are the builder kit's and may have drifted; the kit tells the gate to find them itself.

## Outside-the-fences disclosure
- Wrote only the kit and this report (plus one scratch diff file `pr128.diff` in the session scratchpad, not a project path). Both written with Write; one Edit and one python byte replacement on the kit (a raw NBSP in my own text, turned into the ` ` escape).
- Read (Datasec only, all read verbs): DRAFTER_RULES.md, the B793 kit, the B775 kit, B789 kit and STATUS, first lines of five gate STATUS files, project `CLAUDE.md` (lines 48-53 and a Jira grep), `CLARIFICATIONS.md` (grep and lines 807-811), `JIRA.md` path attempt (not at `1_Project_Definition/`; unread), `model-routing.md` lines 109-111, `models_latest.json` lines 20-40, `brief_seat.sh` line 24, `.tools` directory listings (names only, `ls -d`/`ls -a`, no tree opened).
- `gh api -X GET` only; no fetch, clone, worktree, checkout, merge-tree, commit. A short-lived `python3 -I` listener on 127.0.0.1:8815 as the lsof positive control, freed. No Jira, mail, chat, Artifact, Docs or decision_queue use. No HTTP to any hosted site. `tmux list-panes` read-only.
