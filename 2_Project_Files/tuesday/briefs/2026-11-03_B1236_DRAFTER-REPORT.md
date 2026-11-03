STARTABLE: YES (after Tuesday's stamp; 8 four-underscore lines: `grep -o '____' <kit> | wc -l` prints 8, `grep -c -E '_{4}'` prints 8)

# B1236 DRAFTER REPORT (Sonnet drafter, routing row C8) - SEAT-G326, MPS tier-2 gate of b1232

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1236_SEAT-G326_mps-379-template-isolation-gate-tier2.md` (60 lines, 0 non-ASCII bytes by `LC_ALL=C grep -c '[^ -~]'`). Slots: `2026-11-03_B1236_slots.json` (valid JSON, 8 keys, `@NOW@` where Tuesday's clock goes). Pane `Datasec/MPS-G326`, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, tool tree `.tools/b1236`.

## BLUF
Tier-2 gate (G2, `model-routing.md:109`), round 1 of 2 on the new class "MPS Api test: template isolation format guard", NO GO 0 before. The gate squashes the one commit in its own clone, runs the CI dotnet lines at base and merge (counts must be equal: the rows are asserts inside an existing fact), plants the two narrowing mutants (first: `[^""]` to `[^""\n]` in the verbatim text; second: `[^{}""]` to `[^{}""\n]` before the colon) in its own tree, shows each new row red only under its own plant and green alone under the other via a throwaway probe file, probes the two comment sentences on their cells with its own inputs, checks MPSCALC-379 done-when clause by clause and MPSCALC-381 item 3 word by word, and writes landing files (GO) or residue.md and card-input.txt (NO GO). No browser, no web, no mutant search.

## Facts re-measured by me (instrument, then control)
- `date` 20:50 to 20:56 AEDT. `ls-remote`: main `0d656f90...`, branch `0b745183...`; `compare main...head` ahead 1 behind 0, 1 file, +9 -2; `compare main...main` identical, 0 files; open PRs 121, 120; PRs for the branch 0.
- Blobs by `git hash-object` of raw `gh api` bytes: main `be020307...` (473 lines), head `cbe2250b...` (480 lines); 0 non-ASCII bytes in the head file. `diff main head` printed exactly: `98c98`, `315c315`, `378a379,385` (7 lines: 5 comments, 2 asserts).
- Pointers by `grep -n`/`awk NR` over the raw head bytes (all printed): attribute `:67`, `FormatInHole()` `:68`, doc comment `:91-102` (sentence `:98`), real-files fact `[Fact]` `:312` / name `:313` / sentence `:315`, control fact `[Fact]` `:336` / name `:337`, new comment `:379-383`, new asserts `:384-385`, next `[Fact]` `:409`. Plant anchors each count 1 by `grep -c -F` (control: made-up string 0).
- Tickets (Jira GET by a scratch copy of the project reader printing the description; no token printed): MPSCALC-379 and -381 Backlog, comments 0, updated 2026-11-03T09:55; -382 Backlog 0; control -361 Done, 1 comment. Done-when text copied into the kit.
- CI: `ci.yml:42` build, `:43` test (`git show` at main, `awk NR`); `Directory.Build.props:6-7`; SDK `T/dotnet/dotnet --version` 10.0.401; gitleaks 8.30.1. `CLARIFICATIONS.md:758`, `:774`, `:2218` printed. `model-routing.md:98`/`:109`/`:111` printed; `models_latest.json:23` model_id claude-sonnet-5-5; `brief_seat.sh:24` default opus.
- Class recount: 370 STATUS first lines, 95 `GATE VERDICT`, 0 naming the class; controls: `template isolation` 2, ` NO GO @ ` 14.
- Panes 20:51: tuesday, HPSM-POC-D45, NexusAI-R161, HPSM-POC-G325, fleet-monitor. No MPS pane. `G326`/`B1236` in no brief; `T/b1236` absent; `T/b1186` exists, last line `GO WITH FINDINGS (round 2 of 2)`, with all Rule L copy sources present (heavy.sh lines `:8`/`:9` carry the two changes). Load1 3.42, 201 GiB free. Ports: none needed; `lsof` printed only unrelated ports; scan of today's/yesterday's SEAT kits assigns none.

## D-decisions
- D-1 Judged as a squash into main (main equals the pin, head tree = merge tree); MAIN-MOVE reruns on a later main.
- D-2 Rows seen alone via a throwaway untracked probe file (second partial of the test class) instead of editing the test file at an anchor; c0/c1/PL1/PL2 each carry it, 6 runs total with two before-pictures at main's file.
- D-3 Two things beyond the ticket text, graded Note-level: the committed (a) adds "or a quote" (the gate decides it by a double-quote probe) and the new comment block says "any run without a quote" while the pattern also admits doubled quotes in a verbatim string (my reading, UNMEASURED; the gate probes it).
- D-4 The gate predicts by hand BEFORE reading the builder STATUS; the builder's `.tools/b1232` is read-forbidden.
- D-5 Builder's out-of-scope remarks (`:56`, `:62`) reported, not graded.

## Q for Tuesday (each with a default)
- Q-1 Tier G2 Sonnet? Default yes.
- Q-2 Round 1 of 2, NO GO 0 before? Default yes.
- Q-3 Gate writes its own squash subject (head's is 105 characters)? Default yes.
- Q-4 New comment block at `:379-383` probed as a Note-grade extra? Default yes.
- Q-5 READY 120 / hard stop 180 minutes, window until 23:00 (slots file default)? Default yes.
- Q-6 Builder's remarks at `:56`/`:62` reported only? Default yes.

## UNMEASURED
Nothing built, run, planted or probed; plant outcomes and pattern behaviour are readings of `:67`; counts at main and merge; comment probes; the new block's imprecision; standing heavy/light locks (gate lists them with `bash -c`); hosted CI; CodeQL.

## Outside the fences (disclosure)
No fence broken. Reads beyond my files: DRAFTER_RULES, the B1232 kit and STATUS, the B1185/B1186 gate kits, slots and report, `model-routing.md` lines, `models_latest.json:23`, `brief_seat.sh:24`, `CLARIFICATIONS.md` lines, first lines of all `Briefs/*_STATUS.md` into my scratchpad, `ls`/`tail -n 1` of `.tools/b1186` (names only, one STATUS last line), `plant.py` head (25 lines), `jira_read.py` and `heavy.sh` lines, `ci-dotnet.sh`, `env.sh`, `tmux list-panes`, `lsof`, `uptime`, `df`. `gh api -X GET` only (compare, pulls, raw contents of the test file at two refs) under the project's `GH_CONFIG_DIR`; read-only git (`ls-remote`, `show`, `cat-file`, `log`, `ls-tree`) in the project repo. One Jira GET via an in-process scratch script (token not printed). No card store, no mail, no git write, no cd.
