STARTABLE: YES, after Tuesday fills the slots (S2 = the head sha40, S3 = MAIN plus the base sha40). The builder has READY (its STATUS last line, read at 11:19 as the REFUSE check only; no other line of that file was read) and the branch is at origin.

# Drafter report: B1322 SEAT-G350, tier-2 gate of b1313/hpsmpoc-runner-rows-ci-comment (drafted 11:17-11:25 AEDT 2026-11-06)

## BLUF
Kit `2026-11-06_B1322_SEAT-G350_hpsmpoc-runner-rows-gate.md` (ASCII; 8 lines carry a four-underscore run: seven slots and the last line) plus `2026-11-06_B1322_slots.json` (8 keys, parsed by python). Sonnet, G2 (`model-routing.md:109`, cap `:111`), round 1 of 2 on a new class. The gate's weight is the loosened-test risk: 31 patterns compared old-against-new by program, the 8 NOT patterns re-run fail-open at base and red at head on real source copies, its own census against the builder's 21, the readers of ci.yml, `--list` for the 14, the whole battery, then 10 plants (5 of its own).

## Facts re-measured (instrument; control)
1. Refs 11:17 (`gh api -X GET`): main 13ac7d7e86a5675ee20eb987c62818e357599358; `matching-refs/heads/b1313` one row ecc45f66ebfce3effdfdde5312f2a596ad5f9ee8 (control `heads/b1295` length 1); open PRs 0; commit: one parent 13ac7d7e, e2e-runner.test.ts +125 -32, ci.yml +2 -2; message 1679 chars, subject 98 (`wc -c`).
2. ci.yml: `diff` of raw base and head prints only :415-416; `grep -v` comment-lines diff rc 0. The test file: `it(` 86 -> 87, `PIN` :93-130 31 keys (awk), 8 `// NOT` (awk), REFLOW 31 entries (awk), 32 `PIN.` uses (grep -o, webEnvCall twice), removed 32 / added 121 lines (patch), non-ASCII added 0 (`LC_ALL=C grep`). Textual `expect(` 356 -> 368, but the patch holds 42 added / 30 removed strings and the added side includes `expect(` inside fixture strings: the kit tells the gate to count calls, not text (this is a trap for a naive gate).
3. Round count: loop over 709 STATUS first lines, 163 `GATE VERDICT`, 8 match runner/source-text/reflow/e2e-runner/ci comment; all 8 read GO or GO WITH FINDINGS (printed first 170 chars). Control hits B622, B693. NO GO 0 of 2 before.
4. My crude census (python over base `it(` blocks that read a file and match; `/tmp`-free, in the session scratchpad): 20 rows `112 264 424 430 436 442 449 458 530 544 550 560 643 777 849 864 870 984 1001 1013`; control: a planted row counts 1. It misses :161 and :900 and over-counts; the builder says 21, the kit before it said 16. The gate must beat it with its own instrument and name differences.
5. Ports: `lsof -nP -iTCP:8560-8563 -sTCP:LISTEN | wc -l` 0 (control: all listeners 11). Word-boundary scan of non-.pre SEAT kits of 5 and 6 Nov for 8560-8563: one hit, the builder's own kit (4 lines). The gate needs no block; the file's CLI rows expect these ports closed and bind nothing.
6. Panes (`tmux list-panes -a`): wednesday, G349 (%31, the review-door gate, live), D56, H128, H129 (the builder, still live). Load 8.5 at 11:18, disk 93 percent used, 142 GB free.
7. Model/landing: `model-routing.md:109` G2, `:111` cap; `models_latest.json:23` `claude-sonnet-5-5`; landing source `CLARIFICATIONS.md:5636` (C-299) head-pinned squashes; closed PR titles read as style (3 printed).
8. Builder trees `.tools/b1313`, `wt-b1313-{base,mut,w}` exist and are named READ-FORBIDDEN; `.tools/b1322` and `wt-b1322-*` do not exist (listing).

## D-decisions
- D-1 The class is treated as new although B693's class name contains "runner source-text rows": both neighbours were GO, so NO GO count is 0 either way.
- D-2 Pattern loosening is judged by program (normalise and compare residue, then the gate's OWN wrong-shape strings, then empty and whitespace-only strings), because the builder's refused strings only test what the builder thought of.
- D-3 NOT claim: at least 3 of the 8, three kinds of source, base and head, with a one-line control for each.
- D-4 The builder's own `refused` lists and `REFLOW` table are attacked by Y3 and Y4 (drift of the table against PIN).
- D-5 `(gate B124 N-1)` dropped from ci.yml:415 is a Note; the gate must still run the five readers.
- D-6 A moved main on other paths is not a stop; on the two paths or on files the rows read it is.

## Q-questions for Tuesday (each with a default)
- Q-1 Port block? Default: none.
- Q-2 Gate tier: G2 Sonnet (tests plus a comment, no product byte)? Default: yes.
- Q-3 Class name "runner source-text rows and the CI comment", round 1 of 2, NO GO 0 before? Default: yes.
- Q-4 Run e2e shards, dotnet, SQL Server, validate.sh? Default: no (nothing in the diff reaches them).
- Q-5 Hard stop Step 0 + 100, target Step 0 + 70 (longer than G349's 90/60: about 10 plants on a loaded machine)? Default: yes.
- Q-6 Run G349 and G350 concurrently (load 8.5)? Default: yes, each through the heavy slots; neither shares a path.

## UNMEASURED
Every old/new pattern comparison (the gate's step 2); the 8 fail-open claims; the builder's 23/24/8 plant counts; the whole suite (4070 base, 4102 head); the `--list` output (14 in 2 files is the builder's kit's own run, not mine); the five readers; the builder's 21-row census table and its "needing neither" reasons (the STATUS was not read beyond its last line).

## Outside the fences
None. Read-only: DRAFTER_RULES, the B1313 kit, the B1321 kit and report (template), the B1313 STATUS last line and line count, `model-routing.md` (awk), `models_latest.json` (grep), STATUS first lines, `gh api -X GET` (ref, matching-refs, commit and patch, raw contents, pulls, records CLARIFICATIONS), `lsof`, `tmux list-panes`, `ls`. Wrote only the three B1322 files and scratch files in the session scratchpad. No decision_queue, no ledger, no briefs_staged, no Artifact.
