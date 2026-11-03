STARTABLE: YES (after your stamp; Q-1 to Q-4 carry defaults; nothing blocks the launch)

# DRAFTER-REPORT B1233 (kit `2026-11-03_B1233_SEAT-C87_composer-pcomp124-126-b778-rows.md`, 109 lines; model Sonnet via the Agent call, routing row C8 `model-routing.md:98`)

## BLUF
One builder kit, seat C87, Datasec Security Composer, for PCOMP-124, -125, -126 (the "four shapes" residue of the PR #114 review). Test-only, ONE file `packages/db/test/b778-route-b-script-complete.db.test.ts`, on a NEW branch `b1233/composer-pcomp124-126-b778-rows` cut from main `d424af7f503f1abe8ae24fe3acbc54aa963e6c25`, one commit, one plain push, no PR. No script change, no DEPLOY.md byte (line 255 untouched, unread), no new word. Seven fixtures and seven rows (3 indented/letter-before-dashes refusals, 3 VT/FF/NBSP refusals, 1 `--`+CR accept); the ten-name `accepts` list and completeness row grow to sixteen; the shape control gets seven entries. b778 54 to 61 (UNMEASURED), b616 109 to 109 (file not edited). Tier 2 (G2 `:109`), builder C2 (`:92`), `claude-sonnet-5-5` (`models_latest.json:23`), `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## Facts re-measured (instrument; `date` 20:00:57 first read, 20:04:15 last)
- Main: `git ls-remote origin refs/heads/main` = `d424af7f...`. Raw `T` at that sha (`gh api -X GET contents?ref=`): 1786 lines, git blob `2348719a`, sha256 `1a2e549c`, 54 `it(` rows (`grep -c -E '^\s*it\('`; control b616 file: 92), 0 non-ASCII bytes (python `-I`), `PCOMP` 0 (`grep -c -i`). `DEPLOY.md`: 652 lines, blob `89c35502`, sha256 `64fd6ada`; line 203 is the awk line (extracted by regex in python, not retyped). All kit `file:line` pointers printed by `grep -n` over those raw copies.
- Tickets PCOMP-124/-125/-126 read whole from the 19:53 Jira dump (127 rows, max PCOMP-127, same session scratch); all Backlog, 0 comments, "Not ruled", "a review of its own". Residue (PCOMP review `residue.md`, 19 lines) and B1197 STATUS read.
- **Host-engine probe** (`/usr/bin/awk` 20200816, `env -i PATH=/usr/bin:/bin`, my miniature COMPLETE, real line taken by program, mutants N33/N15/N16/N17/N11/N12 built by replacing the review's anchors, anchor-changed asserted): complete A on all; the three PCOMP-124 fixtures R on real and A only under N33; VT/FF/NBSP R on real and A only under N15/N16/N17 respectively; `--`+CR (before restrict and as first line) A on real and R only under N11/N12. Control: `existing-indented` (`  -- x`) R on all seven sides (so N33 is not killed by the existing row; the miniature is ONE engine only).
- CI predicates read: `scripts/ci.sh:117` (`ci:node` = lint, `prettier --check .`, typecheck, build, test) and `:118` -> `scripts/test-db.sh:58` (`npx vitest run --config packages/db/vitest.config.ts && ...`); the b778 file is judged by the `packages/db` run. The CI typecheck does not read `packages/db/test` (PCOMP-115, queued after).
- Open PRs #91, #86, #85 (draft): `pulls/<n>/files` hits for `DEPLOY.md` or the b778 path 0, 0, 0; control #85 prints `document-pdf.ts` 1. Refs: `git ls-remote origin` shows `b1170/...` (ce523783), `b778/composer-route-b-dump-complete`; none named `b1233`.
- Panes (`tmux list-panes -a`): `%0 tuesday`, `%1 fleet-monitor`, `%172 Datasec/HPSM-POC-G325`; no Composer pane. Heavy lock and `.tools/b1233` absent (`ls -d` rc 2). Seat C87/B1233 scan of non-pre kits: one word-hit, an old MPS candidate id in `2026-10-17_B164_...` (not a seat). Ports: none assigned, none needed (not scanned).
- Plumbing dirs exist: `.tools/b1197/scripts/` (gate's: mutants1197.py, plants-inner1197.sh, unit.sh ...), `.tools/b1193/scripts/` (fmt.sh, fmtcheck.sh, tsc.sh). I did not verify `imgbuild.sh` in b1197's listing (my `ls` was cut at 40); the kit says "verify each exists, else take from b1193".
- Four-underscore runs in the kit: 9 (`grep -o -E '_{4}' | wc -l`), as the template.

## D-decisions
- D1 Test-only, no script change: the PR #114 review says the line is right on 1,032 cells x 3 engines and all three tickets say "only the test file changes". The kit orders STOP if a row cannot go red without a product byte.
- D2 New branch off main, not b1170 (that branch was squashed into main by #114).
- D3 Three PCOMP-124 fixtures (the review's three cells) rather than the ticket's one, so each of three narrower mutants (X1 tab, X2 one space, X3 letter) has its own row. Q-2.
- D4 One PCOMP-126 fixture (ticket's text); the `--CR` first-line cell is not added. Q-3.
- D5 Completeness row (`:1758`) title says "ten"; extending the list to sixteen makes the title false, so the kit permits exactly that one retitle (`names.py` lost 1, added 8). Q-4.
- D6 Hard stop 180, target 120 (83 mutant plants + 3 engines, as B1193).
- D7 In-row shape pins because the shape control's `trim()` and `startsWith("--")` skip VT/FF/NBSP/accept lines.

## Q-questions for Tuesday (each with a default)
- Q-1 The cap row (`model-routing.md:111`) fired on the class "Route B completeness check (0021) header-key rule" (NO GO 1 of 2, 2 of 2, granted third). Does a new builder lane on the ticketed residue need a card, or does the product owner's "land it and ticket the four shapes" plus each ticket's "a review of its own" cover it? Default: proceed; the next gate counts as round 1 of 2 on a new class "Route B test rows for the four shapes". Tuesday's call.
- Q-2 Three PCOMP-124 fixtures (default) or the ticket's one.
- Q-3 One PCOMP-126 fixture (default) or also the first-line `--CR` cell.
- Q-4 Retitle the completeness row from ten to sixteen (default YES).

## UNMEASURED
- Colour of every new row, b778 61 of 61, b616 109 of 109 (RELAYED by the PR #115 kit), prettier layout, lint, the other two engines, each X-mutant's per-row result, whether the six refusal names are accepted by the `&&s==0`-dropped edit (expected yes by the logic of `s`), gawk, the demo VM, hosted CI and CodeQL. Whether the `plants-inner1197.sh` list cut works unchanged.

## Outside-the-fences disclosure
Wrote only the kit, this report and the slots file. Scratch (raw copies, `probe.py`, fixture files under `scratchpad/b1233/`) is in this session's scratchpad. Reads: `gh api -X GET` under the Composer `GH_CONFIG_DIR`, `git ls-remote`, the Jira dump already in the scratchpad (no new Jira call), plain reads of the B1193/B1224/B1230 kits, the B1197 STATUS/`residue.md`/`d6-survivors.txt`, `tmux list-panes`. No decision_queue, no briefs_staged, no ledger, no docker/az/ssh, no hosted HTTP. One slip: my first Bash call contained a `cd` and the hook refused it; no effect. Advisory hook notes on case-sensitive greps were acknowledged; counts used here were paired with controls where stated.

READ-WHOLE-BY-TUESDAY (report): ____
