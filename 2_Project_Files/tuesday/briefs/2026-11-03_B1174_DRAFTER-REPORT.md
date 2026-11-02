STARTABLE: YES

# B1174 DRAFTER REPORT - SEAT-G305, tier-2 QA gate of b1169/mps-375-template-isolation-killing-rows (judged as a merge into main 314b53f6)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1174_SEAT-G305_mps-375-template-isolation-gate-tier2.md` (60 lines; 8 four-underscore lines: S1-S7 and the last line, `grep -c` printed 8 and `grep -n` showed lines 51-57 and 60; 0 non-ASCII bytes, `LC_ALL=C tr -d '\000-\177' | wc -c` printed 0; no person's name in it, `grep -c -i` printed 0). Shape copied from the B1166 gate kit and report. No `.pre-stamp` copy was made (the REFUSE control "the `.pre-stamp` copy reads 8" needs Tuesday's stamping copy to exist at launch).

## BLUF
Startable. G2 (`model-routing.md:109`, cap `:111`, model `claude-sonnet-5-5` at `models_latest.json:23`), round 1 of 2, NO GO 0 before on the class. Subject at 03:53-03:58 AEDT by `date`: branch head `82e193cb...` (ls-remote and `gh api compare`: ahead 1 behind 0 on the pin `62fd49c7`, one file +123 -5, `git diff --numstat` `123 5`), main `314b53f6...` (compare pin...main 13 files, none the path, none under `Templates/`). The test file's blob is the same at the pin and at main (`6f7788ec...` by `git rev-parse` and by `gh api contents?ref=314b53f6`), so the merge is textually clean; the kit has the gate fetch main once into its OWN clone (main's object is not in the local checkout: `cat-file` fatal) and cherry-pick the head without committing into `wt-merge`, so every CI line is run on the actual merged tree. The gate writes its own probe, its own plants (GS shape plants in different files and text, GM guard mutants, SC scanner plants in different forms from the scan gate's and the builder's) and its own P7 evidence BEFORE it opens the builder's added lines.

## Facts re-measured (instrument)
- Round count: first `GATE VERDICT` lines of `Briefs/*_STATUS.md` 87; lines matching `template isolation|isolation scan|TemplateIsolation|scan-and-docs|b1142` 1 (B1150, GO WITH FINDINGS); ` NO GO @ ` among them 0; control: ` NO GO @ ` over all 87 prints 10. B1105 and B1118 are the template-store class and are not matched.
- Scanner anchors at the head (`grep -n` over the head blob saved in the scratchpad; each printed one line): `depth++;` `:141`, `depth--;` `:145`, `else if (c == '\'')` `:128`, `verbatim && next ==` `:190`, `c == '\\' && !verbatim` `:197`, `{{` branch `:201`, `}}` branch `:205`; new facts at `:306 :329 :353 :363 :372 :379`; file 415 lines; third comment `:286-287` (`awk NR`).
- CI: `ci.yml` at main by `gh api contents | base64 -d | awk NR`: `:1`, `:30` `dotnet:`, `:42`, `:43`; `global.json` 10.0.100 rollForward latestFeature; `Directory.Build.props:6-7`; local SDK `T/dotnet/dotnet --version` 10.0.401.
- Jira (`T/b1125/jira_read.py`, no `full` argument so it writes nothing; header read first): MPSCALC-375 Backlog, 0 comments; control MPSCALC-363 Done with 1 comment; `text ~ "TemplateIsolation"` lists 375 only.
- Builder STATUS: 93 lines, last line `READY FOR QA: B1169 ... @ 82e193cb...`, has `## PRIOR WORK`; read in full for the claims (8 of 8 plants, P7 0 of 9 red, Api 3259 on the pin).
- Head commit: unsigned (`%G?` N), subject 119 characters (`wc -c` 120), trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`; the kit forbids reusing that subject for the squash (limit 100).
- Origin: `matching-refs/heads/b1174` 0 (control `b1093` 1); local `refs/heads/b1174*` 0; `.tools/b1174` absent; `.tools/b1146` present with `heavy.sh hb.sh env.sh ci-dotnet.sh trxsum.py nuget-home` (315 MB); `.tools/b1125/jira_read.py` present; `.tools/b1166` and `.tools/b1128` exist (not used).
- Locks: bash `ls -d .tools/*/heavy.lock .tools/*/light.lock` 0 hits (control `.tools/b1146` printed). Panes 03:57: `%0 tuesday`, `%117 Datasec/MPS-R147`, `%1 fleet-monitor`; no `Datasec/MPS-G305`. SEAT kits of today naming `TemplateIsolationTests` (`grep -l -w`, non-`.pre-`): B1162, B1164, B1165, B1169 (the builder), B1171 (R147, a PARTITION sentence about the closed builder; records only).
- Ports: none assigned, none needed; `lsof` listed `*:49152 *:5000 *:59869 *:7000 127.0.0.1:49166 :49168 :49171`. Load 2.01 4.63 6.07 at 03:53; `df -g` 251.

## D-decisions (mine; Tuesday may override)
- D-1 Subject is the MERGED tree (main plus the head's one commit, applied with `cherry-pick --no-commit` in the gate's own clone), not the builder's branch tree.
- D-2 Independence: the gate copies from `.tools/b1146` (not `b1169`) and never opens `.tools/b1169`, its `plants.py` or predictions; plants GS/GM/SC and the P7 corpus are the gate's own, in different forms from the scan gate's M3-M8 and the builder's PS/P plants.
- D-3 P7 is re-measured three ways: reasoning from source, an exhaustive enumeration (length 0-6 over `$ @ " { } \ ' / a`) with count and SHA-256 compared with and without the branch, and the file's filter under the plant.
- D-4 Extras beyond the brief: GM4 (drop one entry of `GuardShapes()`, predicted survivor), SC6 (the backslash block of `SkipCharLiteral`, a branch the builder did not name), GS6 (a conditional with a colon in a hole: guard strictness), sentence-by-sentence comment table with an IMPRECISE grade.
- D-5 Comment sentence FALSE is a Major (the ticket's clause C); a FALSE sentence in the head commit's message is a Note because Tuesday lands with the gate's own subject and body.
- D-6 Rule L gap between load reads 120 s (as B1166), plus waiting on any other seat's heavy/light lock; up to 20 plant runs, so expect about 40 minutes of read gaps. Target READY 150 min, hard stop 240 min (the builder took 39 min).
- D-7 TMPDIR `/private/tmp/b1174-seat-tmp`, proved outside any work tree, because the builder found `A_path_outside_any_git_work_tree_is_refused` goes red otherwise.
- D-8 Whole suite: base 1 run, merge 2 runs, new facts alone 10 runs.

## Q-questions for Tuesday (each with a default)
- Q-1 G2 right? Default YES (test only, no product byte, mechanism measured by the scan's gate).
- Q-2 Read gap 120 s versus the original 4 s? Default 120 s (B1166 precedent); with 4 s the gate is about 40 minutes quicker.
- Q-3 Is the `}}` branch residual (neither pinned nor removed) acceptable for clause B? Default yes: recorded as PARTLY-DONE, not a NO GO.
- Q-4 S5 hard-stop clock: left for Tuesday (suggest not later than 07:30 AEDT).
- Q-5 Launch window and the `.pre-stamp` copy: left for Tuesday.

## UNMEASURED
Nothing built, tested, planted or probed. The six new facts at main; the merge counts; whether each plant compiles; the guard behaviour on a conditional in a hole; survivors GM4 and SC6 (reading only); the hosted runner's SDK; open PRs' file lists (builder claim; I read only the PR numbers `[121, 120]`).

## Outside-the-fences disclosure
Wrote only the two files. Read-only elsewhere: the DRAFTER_RULES file, the B1166 and B1169 kits and the B1166 report, the briefs folder, the MPS project's `Briefs/` STATUS files, `CLARIFICATIONS.md` lines, `.tools` (ls and the headers/sources of `heavy.sh`, `hb.sh`, `env.sh`, `ci-dotnet.sh`, `jira_read.py`; `ls` of `.tools/b1169` names, no file opened). Ran `jira_read.py` (GET only) twice; `gh api -X GET` under the project config; `git` read verbs in the project repo, plus one `git worktree list` that the hook REFUSED (nothing ran). Wrote two scratch files in the session scratchpad (`head.cs`, a copy of the head blob made by `git show`, and `gv.txt`, the verdict lines). `tmux list-panes` and `lsof` read. The hook also advised case-sensitive greps on pointer lookups; each printed its own hit, so none is a zero.
