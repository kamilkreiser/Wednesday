STARTABLE: YES

# B1239 drafter report (SEAT-R162, NexusAI RD-911, the comment half only)

Drafted 2026-11-03, `date` prints 22:01:43 to 22:07:24 AEDT. Model row: seat C2 (`model-routing.md:92`), no gate (G3 `:110`), drafter C8 (`:98`) on Sonnet; seat level `BRIEF_SEAT_LEVEL=sonnet` inside the launch-line quotes (`models_latest.json:23` = `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus).

## BLUF
- The kit is startable. It posts ONE comment on RD-911, makes NO transition, writes NO repo file. It is narrower than the ticket and says so in its own words: the comment half only; the replacement-by-a-count half stays open on the ticket.
- Re-measured at main `f3ab00bd`: ten rows. Nine wall-clock bounds are LEFT with a reason; ONE is a count candidate (the injected missing-file window: `PAST_BUDGET_MS` `:45`, clock check `:138`, used at `:245`, `:319`, `:344`), marked "inference from the source, not a measurement", not done here.
- The sweep's three pointers (`:44`, `:45` of the first file, `:68` of the second) all re-derive. The two test files are byte-identical at `8a812415` (the ticket's commit) and at `f3ab00bd`. A third file, `__tests__/helpers/rd407-setting-writer.js`, holds waits and a duration, so the frame includes it (the ticket says "exactly two test files named rd407"; the tree shows three rd407 paths).
- The comment text (BLUF / Recommendation / Detail) is written into the kit as three fixed parts. All three scan clean (0 on every class, scanlib controls True, "Tuesday" 0 times), so the seat needs no waiver.

## Facts re-measured, with instrument and control
| Fact | Instrument | Control |
|---|---|---|
| main = `f3ab00bd473d053a0f925616aebfe550aca3ba64`, 2026-11-03T09:28:33Z | `gh api -X GET repos/datasecau/Reporting_Dashboard_Au/commits/main` (22:02) | `pulls/99999` 404. `git ls-remote` over ssh answered "Repository not found" (no deploy key in this shell), so origin was read through `gh api` instead |
| repo identity `datasecau/Reporting_Dashboard_Au` | `git --no-optional-locks -C .../NexusAI/2_Project_Files remote get-url origin` | `datasecau/NexusAI` is the wrong name, per the B1235 kit |
| open PRs: 1 (#164, records for RD-922) | `pulls?state=open` | #164 is irrelevant to a comment seat; the kit says so |
| 3 rd407 paths in the tree, `truncated=false` | `git/trees/<main>?recursive=1` filtered by `rd407` | the same tree contains the listed blob shas |
| blobs: first file `faa6db5c...` 540 lines, second `45a2a890...` 702 lines, helper `2e0f5208...` 102 lines | raw GET then `git hash-object`, equal to the tree shas; the first two also equal at `8a812415` | wrong line (`awk NR==99999`) prints 0 bytes |
| RD-911 To Do, 0 comments, changelog 0, links 0, 3 labels | Jira GET through the project helper `b1210lib.py` (`get`, `search`, `comments`, in-process credentials) | `RD-99999999` 404; `key = RD-911` 1; `text ~ "zzqxnonexist"` 0; `text ~ "RD-911"` 0; `text ~ "rd407"` 6 |
| RD-899 and RD-900 (Testing, 1 comment each) and RD-407 (Release Ready, 10 comments) mention no bound, deadline or window | regex over `adf_texts`, 0 hits each | the regex alternation includes `60000` and `deadline`, which occur in the ticket text itself |
| the census: 17 lines / 9 / 5 across the three files | one `grep -E` pattern (sha256 prefix `92ac32cc6f08b194`), re-extracted FROM THE KIT FILE by program and run again: 17, 9, 5 | a planted file with a `Date.now` difference under `toBeLessThan`, a `}, 90000);` and a `setTimeout` matched 3 of 3 |
| zero counts: `toBeLessThan`/`toBeGreaterThan`/fake timers 0, per-test timeout argument 0, `setInterval` 0 | `grep -c` per file | the planted file gives 1 for the first two patterns |
| every `file:line` of the ten rows | `grep -n` and `awk NR==n` over the raw files at the pin, printed just before writing | wrong-line control 0 bytes |
| census lines that are not bounds: prose `A:17,43,124,290,380`; `B:209`, `B:655` (byte counts); `W:73`, `W:81` (`waitForGo`) | `awk NR==n` | listed in the kit |
| arithmetic `8 * 60000 = 480000`, `2 * 8 * 15000 + 120000 = 360000` | shell `$(( ))` | n/a |
| ports: `lsof -nP -iTCP:9800-9999 -sTCP:LISTEN` 0; SEAT kits of 11-02 and 11-03 (non-`.pre-`) for `R162` 0 and `B1239` 0 | `lsof`, `ls | grep -v '\.pre-' | xargs grep -l -w` | `R156` found 2 files; no port is needed by this seat anyway |
| live panes: `tuesday`, `Datasec/Security-Composer-G327`, `Datasec/HPSM-POC-G325`, `fleet-monitor`; NexusAI pattern 0 | `tmux list-panes -a -F '#{@cockpit_name}'` | planted `Datasec/NexusAI-R999` counts 1 |
| REFUSE wording for same-project panes (the seat refuses only on a SECOND pane named exactly `Datasec/NexusAI-R162`): `grep -c -x 'Datasec/NexusAI-R162'` | tested on four lists | `[R162, N96, tuesday]` gives 1 (own pane, not a stop); `[N96]` gives 0; `[R162, R162]` gives 2 (fires); `[R1620, xDatasec/NexusAI-R162]` gives 0 (no substring hit). It does NOT fire on `Datasec/NexusAI-N96` |
| kit shape: 73 lines, 9 stamp slots (`STAMP`, `LAUNCH WINDOW`, `Stamped by`, `Launch authority`, `Heads at launch`, `Model receipt line`, `AUTH-RULINGS`, `SLOT JIRA`, the last line), all four underscores | `/usr/bin/grep -c -E '_''_''_''_'` on a copy = 9 | the seat's own REFUSE uses the same split-quote form |

## The ten rows (summary; the kit has the pointers and reasons)
LEFT: (1) `A:41` jest.setTimeout 60000; (2) `A:44` BUDGET; (3) `A:246/253/255` M2 lower bound; (4) `B:68` STORM_DEADLINE_MS 60000 (`:241-242`, `:253-254`), with the CONTROL cell at `:294-:300` turning loud on a kill; (5) `B:69` jest.setTimeout 360000 (note: 8 x 60000 = 480000 > 360000); (6) `B:90/242` 20 ms poll; (7) `B:504/525` now + 1 h session expiry; (8) `W:75` 2 ms poll; (9) `W:83/97` duration reported, never asserted. CANDIDATE: (10) `A:45` + `A:128/138/139`, used at `A:245` (M2), `:319` (R1), `:344` (R3).

## D-decisions (mine, for Tuesday to veto)
- D-1. The frame includes the helper file (3 files, not the ticket's 2), because it holds a wait and a reported duration. If Tuesday wants the strict two-file frame, delete rows 8 and 9 and the "9" in the BLUF becomes "seven" (the BLUF, Detail and the kit's row count all change together).
- D-2. Comment shape is BLUF / Recommendation / Detail only. The B1235 AUTH paragraph is dropped (nothing is moved, nothing needs the "records step" statement), so the waiver for the word "Tuesday" is not used and the scan forbids the word everywhere.
- D-3. The Recommendation names a product-owner decision (leave the window and close, or replace by a count). The ticket's own "Done when" offers exactly that choice. It states a default ("the ticket stays open for that half"), so nothing is asked of a human by the seat.
- D-4. Row 4 (`STORM_DEADLINE_MS`) is LEFT, not a candidate: a stall of 60 s with the failure loud in the CONTROL cell. What S1/S2 do after a kill, and real storm durations, are stated in the comment as not measured.
- D-5. The seat posts after writing the full assembled text into STATUS, STOP only on a figure failing its source (per the commission). It does not wait for another read by Tuesday.
- D-6. A census count other than 17, 9, 5 holds the comment rather than letting the seat reclassify silently.
- D-7. The kit asks the seat to copy the b1210 helpers (read-only source) into `session-tools/b1239/`, as the B1235 kit does, with `transitions`, `do_testing`, `pick_done`, `do_done`, `create` forbidden.

## Q-questions for Tuesday (each with a default)
- Q-1. Keep the helper in the frame (D-1)? Default: yes.
- Q-2. Should the Recommendation carry the product-owner choice (D-3), or only "no action needed" with the candidate stated in the Detail? Default: as drafted.
- Q-3. The kit refers to `launch_when_cool.sh` and the template's launch line; `launch_when_cool.sh` and the `_slots.json` stamping file were not touched here (the slots JSON for B1239 is not produced: outside my two files). Tuesday's stamp helper needs a `B1239_slots.json` with the nine keys above. Default: Tuesday makes it from `B1235_slots.json`.
- Q-4. The seat's Step 0 copy: the kit's `.pre-stamp` sibling is not produced (outside my two files). The pre-stamp slot count the seat's control expects is **9**; Tuesday should copy the unstamped kit to `.pre-stamp` before stamping. Default: copy.

## UNMEASURED
- Per-cell and per-storm run times on a hosted runner (no figure printed by a green cell; I did not read any CI log).
- What S1 and S2 do after a SIGKILL (not examined; the kit and comment say so).
- Whether any stall has ever ended the injected window (the ticket says no figure exists).
- How many observations the product's retry loop makes over its budget (needed to choose a count for row 10).
- Whether the product-owner choice in the Recommendation is welcome; Tuesday's stamp decides.
- Job B scripts (`assemble1210.py`, `figures1210.py`, `d1210.py`) were read by header and by head only (first 12 to 83 lines); the kit tells the seat to read them whole and gives sha256 prefixes copied from the B1235 kit, not recomputed by me.

## Outside-the-fences disclosure
- Created and removed an empty file `/tmp/nope` by accident (one `tee` in a pane-list command; 0 bytes, removed in the same command). It is the only write outside the session scratchpad, my two files and nothing in the repo.
- All other scratch (a Jira read script, census program, planted file, raw copies, a heartbeat line) is under the session scratchpad. I imported the project helper `b1210lib.py` read-only (`sys.dont_write_bytecode`, heartbeat path redirected to the scratchpad so no line was written to the `b1210` folder); it reads `.env` in-process and prints no token. It also imports `session-tools/b854/jira-adf.py`.
- Importing `scanlib1114.py` ran one `gh api -X GET user` (read; login not printed).
- `git ls-remote` against the ssh URL was attempted once and failed ("Repository not found"): a read attempt only.
- Read-only reads of project files: `CLAUDE.md:286-310`, `Briefs/*_STATUS.md` greps for `RD-911` (B927, B1018, B1023, B1029, B1054, B1141, B1153), the b1210 scripts' heads, the sweep file lines 60-90, the B1235 kit, `DRAFTER_RULES.md`, `model-routing.md` lines 90-112.
- No `decision_queue.sh`, no Artifact/Docs/mail, no HTTP to any hosted host, no `cd`, no git write, no `gh` write, no Jira write. Two hook advisories (case-sensitive multi-word grep) fired; each count had a positive control and was nonzero or control-checked.
- Not read: `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, any WEDNESDAY/FRIDAY tree.
