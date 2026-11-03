STARTABLE: YES

# B1237 drafter report (Tuesday's kit drafter, claude-sonnet-5-5), 2026-11-03 21:49 to 21:58 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1237_SEAT-G327_composer-pcomp124-126-gate-tier2.md` (48 physical lines; 7 four-underscore runs = 6 slots + last line by `grep -o | wc -l`; 0 non-ASCII by python `-I`). Slots: `2026-11-03_B1237_slots.json` (same key style as B1217's). Nothing else written except scratch under the session scratchpad.

## BLUF
Startable. Tier-2 Sonnet gate of b1233 @ 5a774e1d (one commit on main d424af7f, test file only, +144 -1), round 1 of 2 on a NEW class. The kit makes the gate re-run the builder's properties R-a..R-g, the three engines, the review's M01-M50 / N01-N33 plus X1-X3, and the three tickets' Done-when. Lightened vs the B1197 round-3 kit: no 899-cut frame, no browser, no new mutant search, no builder-STATUS embargo beyond hashing predictions first.

## Facts re-measured (instrument, control)
- `git ls-remote`: head 5a774e1d, main d424af7f; `b1237*` none (control `b1170*` prints 1). `gh api -X GET compare`: ahead 1, behind 0, one file T +144 -1; commit parent d424af7f, tree 432155d2; open PRs 91, 86, 85(draft). `git cat-file -t` of the head and main shas: `commit` locally (control: invalid name errors), so no fetch needed.
- Raw `T` at both shas via `gh api contents?ref=`: main 1786 lines blob 2348719a (matches the builder kit's pin); head 1929 lines blob d725e8ac, sha256 95eb87d1 (matches the builder's plant sha). `diff` main vs head: 1 removed line = the completeness-row retitle (ten to sixteen). Head: 61 `it(` rows, `PCOMP` 0, non-ASCII 0, control bytes 0, CR 0 (python `-I`; no control built, the kit gives the gate one).
- Every `T:line` pointer in the kit printed by `grep -n` over the head copy (VT :169, FF :170, seven members :1288-:1300, accepts tail :1352-:1357, rows :1548..:1598, :1630, :1640, :1895, etc.).
- Commit message (gh api): 0 hits of `B[0-9]{3,4}|PCOMP|Kam|Kreiser|Tuesday|Wednesday` over the message text, exactly 1 `Co-Authored-By`; subject over 100 characters (kit tells the gate to write a shorter squash subject); author e-mail is the local-host `.localdomain` one.
- Panes: tuesday, MPS-G326, HPSM-POC-D45, HPSM-POC-G325, fleet-monitor; 0 Composer panes. `P/.tools/composer-heavy.lock` and `P/.tools/b1237` absent (`ls -d` rc 2; controls: `.tools/b1233` lists). `G327`/`B1237` in non-`.pre-` SEAT kits: 0 (control G326: 1). load1 3.96 at 21:51.
- Round count: no `*_STATUS.md` with `GATE VERDICT` in its first 3 lines names pcomp-124/125/126, four shapes, b778-rows, B1233 or B1237 (loop output empty; control: the B1197 file matches 'route b'). The earlier class has 3 NO GOs (B1173, B1181, B1197 granted final), a different class per the product owner's new ruling, so this gate is round 1 of 2.
- Plumbing: b1197/scripts holds mutants1197.py, names.py, plants-inner1197.sh, unit.sh, c2host.sh, extract.py etc.; it has NO imgbuild.sh, so the kit takes `imgbuild.sh` from b1217 (finished G319 gate). `d6-survivors.txt` exists (91 lines; 6 SURVIVOR, 20 EQUIV by grep).
- Model: G2 `model-routing.md:109`, G-cap `:111`; `claude-sonnet-5-5` at `models_latest.json:23`. Landing rule `CLARIFICATIONS.md:1799` and `:1885` found by grep -n -i.
- Ports: none assigned or needed (`--network none`); `lsof` 9400-9409 rc 1 at drafting but not reserved. No word-boundary scan of other kits was run for a block because none is claimed.

## D-decisions
- D1. Instruments: the previous gates' scripts (b1197, b1217), never the builder's `.tools/b1233` (claims only). The builder's R-f table is the prediction the gate must hash its own before reading.
- D2. Squash subject at most 100 characters, no PR number, no ticket key in any landing file (consistent with the builder kit; Jira is a records seat's).
- D3. PCOMP-126's second cell (`--CR` as first header line) is a Note (stamped Q-3), upgraded to Minor only if a ticket's Done-when requires it.
- D4. typecheck, build, root vitest not required (test-only; CI typecheck does not read packages/db/test); lint and `format:check` whole repo are required.
- D5. READY 90 / HARD STOP 150 suggested; the heavy budget is one image per tree, about 6 db runs, 16 accepts-deletion plants in one container, three engines.

## Q-questions for Tuesday (each with a default)
- Q-1. Window and hard stop: kit suggests READY 90 / HARD STOP 150 (builder used 120/180). Default: 90/150, slots file ends 01:00 window, never after 01:30.
- Q-2. Landing files carry no ticket key (the builder's commit has none either). Default: yes, none.
- Q-3. PCOMP-126's un-added first-line `--CR` cell graded Note, not Minor. Default: Note, stated in the PR body as not covered.
- Q-4. The sixteen `accepts`-deletion plants and the shape-control checks are kept (light, one container) although tier 2. Default: keep.
- Q-5. I did not read the three tickets (Jira not touched by me); their Done-when is RELAYED from the builder kit and the gate reads them. Default: gate reads, grades G-4.

## UNMEASURED
- Everything dynamic: no test, container, prettier, awk or plant by me. The R-f verdict grid is the builder-kit's host-engine measurement, not mine. The builder's 311/3,116/2/1 chain counts, the 96-cell engine grids and its plants table are RELAYED. Open PR file lists are RELAYED (builder, 21:44); the kit makes the gate re-read them. Whether `imgbuild.sh` from b1217 still builds the current tree (it was built for b1217's `node` image) is not checked.

## Outside-the-fences disclosure
- Read only: `git ls-remote`, `git cat-file`, `rev-parse`, `ls-tree` in `2_Project_Files` with `--no-optional-locks`; `gh api -X GET` under the project `GH_CONFIG_DIR` (compare, commits, pulls, contents raw); `tmux list-panes`, `lsof`, `ls`, `uptime`, `date`; reads of the builder kit/STATUS, B1217/B1197 kits, model-routing, models_latest, project Briefs and `.tools` listings; python `-I` scans on scratch copies in the session scratchpad `x/`.
- One Bash call began with a typed `cd` in a compound command and was refused by the hook (nothing ran); reissued without it. A Bash grep with a one-line advisory about case-sensitivity ran with `-E` patterns over my own copies; the counts that matter carry controls above.
- I did not run `decision_queue.sh`, read `briefs_staged/`, the scoreboard, `_ledger.md`, or any WEDNESDAY/FRIDAY tree. No Jira call, no mail.
