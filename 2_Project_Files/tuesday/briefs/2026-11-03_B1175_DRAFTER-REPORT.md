STARTABLE: YES

# B1175 DRAFTER REPORT (drafter C8, Sonnet; HPSMPOC-437; written Tue 3 Nov 2026 about 04:28 AEDT, `date` read 04:26:47)

## BLUF
Kit written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1175_SEAT-H107_hpsmpoc-437-remediation-store.md` (branch `b1175/hpsmpoc-437-order-pin-and-titles` from main `2a7709887756b7faab88d6ad483127923c672cfb`, ONE commit, push only, no PR, pane `Datasec/HPSM-POC-H107`, ports 9610-9619 reserved, none needed, Sonnet, C2 `model-routing.md:92`, gate G2 `:109` proposed). Startable once Tuesday fills the 14 Stamp slots (13 slots plus the last line). The partition scan the sweep could not finish is done: no live lane touches the three paths.

## Facts re-measured (instrument and control)
- Ticket: `jira.py HPSMPOC-437` GET: Backlog, 0 comments, labels `b1156-gate`, `b1163-2026-11-03`; done-when quoted in the kit. Word scan for HP-tool terms over the ticket was the sweep's (0); I did not re-run it.
- Main: `git/ref/heads/main` and `commits/main` both `2a770988...` (committed 2026-11-02T10:59:05Z); open PRs 0 (control: `pulls/277` merged, head b1145). Project-folder checkout is stale (its HEAD lacks the sha); every read was from origin.
- Source lines printed by `cat -n`/`awk NR` over raw files at the pin, blobs checked by `git hash-object` equal to `contents` sha: `remediation-store.ts:33, :47, :48-49`; `remediation-store.test.ts:1-2, :29, :80, :135, :184-189`; `RoadmapScreen.register.test.tsx:1-3, :121, :164`. Title lines are exactly the ticket's.
- Partition (the sweep's unmeasured item): `branches --paginate` 293 branches; `compare 2a77098...<b>` read for all 293, 0 error lines, 35 s. Four branches name your paths: b955 @ `9009d8c0`, b984 @ `2eec1997`, b1002 @ `0c3c42da`, b1145 @ `8bc72bb1`. All four are landed or stale: their subjects map to the four main commits on those paths (`edf363427`, `d0eff4ca6`, `e0b939571`, `e30eb1132`); b1145's three blobs equal main's (positive control fired); no PR open; no pane. Negative control: b1097 listed with 8 files and none of the paths.
- Panes at 04:20: %0 tuesday, %1 fleet-monitor, %118 G303, %119 G305, %120 G304. No HPSM-POC pane. (The sweep's %117 R147 pane is gone.)
- Ports: 9610-9619 `lsof` 0 rows; word-boundary scan of 101 non-`.pre-` SEAT kits of 11-02 and 11-03: 0 hits for each of the ten numbers (control 9600: 2 kits). No port is needed.
- Landing rule: `CLARIFICATIONS.md:3617` of `datasecau/HPSM-POC-analysis` main `4f48008c` (read raw by gh; the local copy is stale at 192 lines): "The landing form is a head-pinned squash".
- CI lines from `ci.yml` at the pin (679 lines): 387, 395, 396, 409, 413, 426, 466, 478. Model lines 92, 108, 109, 111 and `models_latest.json:23`, `brief_seat.sh:24` printed by awk/grep.
- Helpers on disk: `.tools/b1145/{lock.sh,waitload7.sh,heavy.sh,hv.sh}` (the kit re-points `heavy.sh:4` and `hv.sh:5`), `.tools/wt-b1113-fix/web/node_modules` 613032 KiB. `.tools/b1175` and `wt-b1175-*` absent.
- Slot count in the kit: 14 (`grep -c`), including the last line.

## D-decisions (mine)
- D1: the pin row is GREEN at main (behaviour unchanged), so "red-first" is replaced by plants that reverse the order for both states, for Verified complete only and for Evidence submitted only (PA, PV, PS), plus PM (date sentence changed) and PX (evidence check removed). A pin that survives PV or PS is a STOP.
- D2: the `describe` renames change the full names of the rows under them, so the kit asks for before/after name lists and a grep of old titles over `web/` (consumers unmeasured here).
- D3: `remediation-store.test.ts:80` (`...blank for Verified complete`) is not stale (its twin at `:135` says "for Evidence submitted too") and is fenced as not yours.
- D4: `partner/action-plan.ts` added to NOT yours and to the main-moved stop, because `isDay` (import at `remediation-store.ts:8`) decides the date row.
- D5: a store-level pin only; no screen row (the ticket's fix shape is a `checkEntry` row).
- D6: no Jira write; the records seat closes the ticket after landing.
- D7: no port needed (jsdom); 9610-9619 reserved only.

## Q-questions for Tuesday (each with a default)
- Q1: SCOPE-437, build or decline. Default `build all` (the sweep named this as Tuesday's call; the fix shapes add no word).
- Q2: gate tier. Default tier 2, G2 (`:109`), round 1 of 2 on class "remediation register tests and titles". Alternative G1 because `remediation-store.ts` is a product file (one whitespace hunk).
- Q3: launch window and authority wording for the Stamp (not mine). Default: launch through the waiter below 7 on two reads; no other live seat shares a path.
- Q4: should a screen-level row also pin the order? Default no.

## UNMEASURED
- Every test outcome and count at main or head (the ticket's "0 of 137 rows red" is relayed); hosted CI; CodeQL.
- Consumers of the old title strings outside the three files (e2e specs, scripts, filters): the kit makes the seat grep for them at its head; I could not, because the local checkout is stale and I did not read the whole tree.
- That b955, b984, b1002 are wholly contained in main (evidence: subjects map to main commits, no PR, no pane; not proved by tree).
- The word scan for HP-tool terms over the ticket: taken from the sweep, not re-run.
- Load average at launch (4.54 at 04:22:54; the waiter decides).

## Outside-the-fences disclosure
Wrote only the kit and this report. Scratch files (branch list, scan output, raw source copies, `scan1.sh`, `ci.yml` copy, the CLARIFICATIONS raw copy) are in the session scratchpad. Reads: Jira GET by the project helper (no token printed); `gh api -X GET` under the project's `GH_CONFIG_DIR` (repos HPSM-POC and HPSM-POC-analysis); `git hash-object`, `tmux list-panes`, `lsof`, `df`, `uptime`, `ls`. One `git cat-file`/`grep` attempt against the stale local checkout at the pin failed with "unable to parse object" and read nothing. No `decision_queue.sh`, no ref write, no HTTP to a host, no `cd`. One tool output (an `ls` of `.tools`, listing worktree names) was larger than intended; nothing was opened from it.
