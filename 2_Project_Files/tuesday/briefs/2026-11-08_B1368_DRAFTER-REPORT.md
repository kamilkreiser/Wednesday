STARTABLE: YES (after Tuesday's stamp; two independent branches from main, nothing deploys)

# B1368 DRAFTER REPORT (SEAT-M100, MPSCALC-385 then MPSCALC-386)

Files: kit `2026-11-08_B1368_SEAT-M100_mpscalc-385-386.md` (87 lines by `wc -l`, ASCII by `grep -c -v -x -E '[ -~]*'` 0, 12 four-underscore lines: 11 Stamp slots plus the last line, control: the template reads 12 the same way), `2026-11-08_B1368_slots.json` (12 keys incl. READ-WHOLE, valid JSON by `json.load`, no `@SEAT@`, no angle bracket), this report. Shape from B1352 (M99); Stamp keys `(S0)`..`(S10)` as B1362's slots.

## BLUF
- M100 is free: `/usr/bin/grep -l -w M100` over `tuesday/briefs/*.md` printed 0 files (control: `-w M99` printed 3). One hit in the MPS folder is a test-name token (`N500-one-number-M100-manual-reversed` in `Briefs/2026-10-23_B533_evidence/c5-a6-policy-timing.txt:3`), not a seat. B-number 1368 is unused (no `.tools/b1368`, `matching-refs/heads/b1368` 0).
- **385 premise is true at `bb9bac9b`:** `printPending` set `:223`, `flushSync` `:234`, flag cleared only inside `printNow`'s finally; no row names `flushSync` (test file count 0, control on the source 3). Fix shape from the ticket (try/catch clear-and-rethrow, or set after flushSync); the kit states a PROPERTY and leaves the shape to the seat.
- **386:** 18 shapes copied from the ticket text; the exact strings live in the B1356 STATUS/evidence (kit tells the seat to read them as claims). The ticket gives a fix shape for F1-F4/H shapes but NONE for M1-M3; the kit says so and gives M3 a property route (formatter exempt only in `format/decimal.ts`, resting on the existing row `:246`). STOP surface: any fix that reds real code (H6/H7/H8 likeliest) or the FleetGrid per-element sites (`FleetGrid.tsx:378`, `:444` re-printed at `bb9bac9b`).
- Kit length 87 lines; the commission asked under ~110.

## Facts re-measured (instrument; control)
- `date` 21:20:17 AEDT (code reads), 21:21:14 (last). `uptime` load 5.05 3.40 2.99. `df -g` 105 GiB free.
- Main `bb9bac9bf604af7c30826403889f8ecb995f940f`, open PRs 0 (`gh api -X GET`, project `GH_CONFIG_DIR`); lockfile blob `7c7d4608...` equals `.tools/b1352/wt-b1352-a/web/package-lock.json` (`git hash-object`).
- Line counts at that sha by `wc -l`: 349, 487, 687, 441. `it(` rows: 29 (ProposalPage.test.tsx), 41 in 7 describes (guard test). Pointers by `grep -n`/`awk NR`: see kit FACTS 2 and 3; two corrections made after a re-print (helpers `:78-:79`, `purchase :93`; `flushSync` 3 not 2 in the source).
- CI `ci.yml` at main: `:45 :58 :61 :62 :63 :66` (grep -n).
- Ports: `lsof -nP -iTCP:9480-9489 -sTCP:LISTEN` empty rc 1 (control: unfiltered listing 11 lines); `-w -E '948[0-9]'` over the 6 non-`.pre-` SEAT kits of 7-8 Nov 0 hits; one hit in the 6 Nov B1353 kit (NexusAI records seat, not live, outside the 7-8 Nov window the rule names). Panes by `tmux list-panes`: tuesday, fleet-monitor, Datasec/NexusAI-G366, unnamed; no MPS pane.
- Model: `model-routing.md` `awk NR==92` is C2 (Sonnet 1st), `NR==109` is G2; `models_latest.json:23` `claude-sonnet-5-5`.
- Tickets read by own Jira GET (project `.env` read in-process, never printed): 385 Backlog, comments 0; 386 Backlog, comments 0; control 361 Done. JQL `project = MPSCALC AND ( key in (...) )`. C-98 found at `CLARIFICATIONS.md:2605`; landing lines `:774`, `:2218` printed.
- Branches matching 385/386/proposal/print/guard at origin: only old ones (b09, b16, b79, b94, b100, b103, b107); none touches the four paths by name (compare not run: UNMEASURED, the seat does it at Step 1).

## D-decisions
- D1: both branches from main, not stacked (paths disjoint), so each PR lands alone.
- D2: no merge of main in (no written rule; main is quiet; kit stops only if main moved onto a read path).
- D3: A and B each get properties not shapes; A's one row is described with a route (`vi.mock('react-dom')` delegating) the seat may change.
- D4: 18 rows plus at most one allowed-form control (`join('+')`) if the file has none; kit asks for exact add count and `comm` lost 0.
- D5: READY 150 / HARD STOP 240 (two tickets); copy sources from `.tools/b1352` (heavy.sh, hb.sh, r.sh, node24, node_modules), all present by `ls`.
- D6: mutant check on B in a copy tree, not a plant table (shapes are the 18 rows themselves).

## Q-questions for Tuesday (default in brackets)
- Q-1 stacked or independent branches? [independent]
- Q-2 does A's fix shape stay the seat's choice? [yes, try/catch preferred]
- Q-3 M1-M3 left to the seat's design, STOP if it reds real code? [yes]
- Q-4 merge main in? [no]
- Q-5 READY 150 / HARD STOP 240? [yes]
- Q-6 port block 9480-9489? [yes]

## UNMEASURED
No test, lint, build or vitest run; whether `vi.mock('react-dom')` works in this file with its other rows (the seat proves it); whether the 18 shape strings in the B1356 evidence match the ticket's descriptions exactly (evidence files listed by `ls`, not read); whether any fix for H6/H7/H8 trips real source (the seat's STOP); `.tools/b1352/node24` and node_modules copy sources exist by `ls` but were not executed; compare of old branches against the four paths; CodeQL state of main.

## Outside-the-fences disclosure
Wrote only the three B1368 files, plus raw copies of four source files, two Jira dumps and `ci.yml` in the session scratchpad (`/private/tmp/claude-501/.../scratchpad`), and `/tmp/x` once by a stray redirect in a port-scan command (an empty or tiny listing; not in any repo). Read a Jira body in-process via an inline python (the project helper's logic, output to scratchpad). No decision-queue access, no card read, no `fleet/briefs_staged`, no scoreboard, no ledger. `gh` was `-X GET` only. A `cd`-containing and a bare-equals command were each refused by hooks and re-issued without them.
