STARTABLE: YES

# B1122 drafter report (kit B1122 / SEAT-H101, drafted 12:40 to 12:54 AEDT by `date`)

## BLUF
Kit `2026-11-02_B1122_SEAT-H101_hpsmpoc-focus-ring-fix-round.md` (18,090 bytes, 11 slot lines of four underscores, 0 non-ASCII) is a one-commit fix round on `b1097/hpsmpoc-home-words-focus-ring` @ `dcc5ca039a55dad5ef75a0ca4134efa8a52b1e25`, Sonnet C2, ports 9570-9579, pane `Datasec/HPSM-POC-H101`, gate after it ROUND 2 OF 2 on class R, tier 1 Opus. Startable once stamped; no STOP found at drafting. The kit fixes B1109-1 by a CANDIDATE `scroll-margin-block` (6, 7, 8, 10, 12 px) proved by a full 1460-cell census plus the partner sweep, with the gate's cell list used as data; reshapes R4 (B1109-3); adds the Home-text row (-4) and the 390 and customer-menu rows (-5); reports -2 and leaves -7, -8.

## Facts re-measured (instrument, time)
- Main `4b3cefae71ca43f6f86d23c77dd75ae101a51fd3`, branch `dcc5ca039a55dad5ef75a0ca4134efa8a52b1e25` (gh api ref reads 12:40:11); compare: ahead 2, behind 1, 7 files; open PRs 0. Control: the same compare lists `b1095` and `b1104` with their own paths.
- Partition by `gh api compare` against main: `b1095/...` = 4 `api/` paths (G280's); `b1104/...` @ `f762cc7a` = 23 paths (api, web/contract, web/src/api, security, `shell/CustomerShell.tsx`, `CustomerShell.frame.test.tsx`, `CustomerShell.scoredChip.test.tsx`, server/mock); none is one of the kit's four. `b1113` is NOT on origin (matching-refs 0), so H100's partition rests on its kit's declared property (collateral/customer paths, HOLDS name shell/, globals.css, e2e, partner): relayed, not computed.
- Ports: `lsof` for 9570-9579 = 0; the only listener in 9500-9999 is 9561 (H100). Word-bounded scan `\b9[0-9]{3}\b` over 123 non-`.pre-` SEAT kits of 11-01/11-02: free blocks 9510, 9530, 9540, 9570, 9580; 9570 chosen. Control: the scan names 9561, 9900. Live panes: tuesday, MPS-R134, MPS-G284, MPS-G283, MPS-M76, HPSM-POC-H100, HPSM-POC-G280, fleet-monitor; no H101.
- `df -g` 39 GiB free (stop 25). load1 5.68 at 12:40. Chromium and helpers exist: `.tools/ms-playwright`, `.tools/b198/lock.sh`, `.tools/b1113/waitload7.sh` (`ls -d`); `.tools/b1122` absent.
- File:line at `dcc5ca03` by `grep -n`: `globals.css:82,:89-91,:93`; `Sidebar.tsx:68`; `AppShell.sidebar.test.tsx:273`; `shell-sidebar.spec.ts:77,:114,:219,:243,:258,:447`. Model lines: `model-routing.md:92,:108,:111`; `models_latest.json:23` = claude-sonnet-5-5; `brief_seat.sh:24`.
- B1109 read whole: verdict NO GO round 1 of 2 on class R (NO GO 0 before); class W NO GO 1 of 2 before.

## D-decisions made in the kit
- D-1 New file `PartnerDashboard.text.test.tsx` for the Home-text row, so commit A's four blobs stay byte-equal (checked by `rev-parse`).
- D-2 R4' pins existence, placement and the old rule as a declaration SET; no value in text; values live in browser rows.
- D-3 Candidates 6, 7, 8, 10, 12 px; first one with 0 regression cells and 0 short sweep heights (Menu-toggle cells excepted at both trees) wins; none: STOP with table. Offset stays 2px (-2 reported only).
- D-4 Old-head control census must reproduce 115 regression / 232 failing, or the seat explains before building. Overlay trees on main stand in for the gate's merge `6c1ec54` (the 7 paths are disjoint from PR 274's 8).
- D-5 Mechanics (clone, locks, plant discipline, property checks, push) are by reference to the B1097 kit's steps 3, 9, 11, 12 and standing lines 6-10, because inlining them doubles the kit past the 18 KB cap.

## Q-questions for Tuesday (each with a default)
- Q-1 Home-text row in a new file (path count 4) or appended to `PartnerDashboard.words.test.tsx` (touches commit A's test blob)? Default: new file.
- Q-2 Mechanics by reference to the B1097 kit (the seat must read it at Step 0). Default: reference; inline only if you lift the size cap.
- Q-3 Confirm ports 9570-9579. Default: yes.
- Q-4 Gate wording: does the next gate re-judge class W? Kit says no (blobs byte-equal), class W stays NO GO 1 before. Default: as written.
- Q-5 Is the wide candidate range (up to 12 px) acceptable, since a larger margin shifts where Tab scrolls the rail? Default: yes, smallest wins.

## Contradictions and oddities
- The user brief says partition against `b1113`; no such ref exists yet, so the check is relayed from H100's kit. The kit tells the seat to recompute at the PINS; if H100 pushes first and shares `shell/` or `globals.css`, STOP `NEEDS TUESDAY <path>`.
- B1109 FOR TUESDAY says "Commit A is clean"; its -4 asks for a Home-text row, which the kit places outside commit A's files (D-1).
- B1109 C4 ran a first landing run 3814/3/0 under load; the kit's baseline expects 3817/0/0 and treats a load red as re-run alone 3 of 3.
- Old builder's `.tools/b1097/` and `wt-b1097-*` still exist; the kit marks them read-only, not a REFUSE.

## UNMEASURED
No clone, build, browser or test run. Not measured: whether 6 px (or any candidate) clears the 115 cells; b5, b6, b11 plant details (seat reads `c3-plants.md`); the shard of the new rows (gate read `journey-and-prototype`); the drawer at 390; the Menu-toggle cover under a larger margin; hosted CI.

## Outside the fences
None. Read-only: project files via `gh api -X GET` and the Briefs folder (B1109 STATUS and evidence names); one `ls -d` of `.tools` paths; no decision_queue, Jira, `az`, ssh, docker, Artifact or Docs call; I made scratch copies of raw files under the session scratchpad only.
