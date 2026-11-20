STARTABLE: YES - the kit is drafted, `stamp_check.py` exits 0 (93 of 93 sidecar lines filled), PR 85's head did not move (851057291ffb019baee6c3c51a50d7b8833f5b3a, re-read 19:43:24), every source exists and is sized, and the drafter's own prototype of the kit's rules resolved all 132 rows with no STOP. Three things for Tuesday before the stamp: the seat id C104 is already used by a finished seat (Q-1), the live root tree is not clean (1325 status lines, none under `Content/`), and slot REC-MERGE is the drafter's addition (recommended HOLD).

# B1801 drafter report (Sonnet, Agent-tool drafter), 2026-11-20 19:42 to about 19:56 AEDT

Files: kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1801_SEAT-C104_composer-cw1-sample-crosswalk.md` (50133 bytes), sidecar `...crosswalk.md.measured` (93 lines), this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s301/d1801/` (raw copies of the two PR files, `parse_smmap.py`, `proto.py`, `jget.py`, `mk_measured.py`, saved branch and PR lists, 4 Jira ticket files).

## BLUF
1. One records-only seat builds `Content/<D>_sample-crosswalk/` (two files: `sample-crosswalk.json` and `README.md`) in its own worktree on `records/b1801`, one commit, no push, no merge unless slot REC-MERGE says MERGE. Its STATUS and evidence go under `Briefs/`.
2. The crosswalk is built by six stated rules (R0 key, R1 registry, R2 absent rows, R3 shared controls, R4 policy items, R5 seed cross-check) and checked by 16 programs (CK1 to CK16), each with a planted control that can fail. A row no rule resolves, or a row with two registry controls, is a STOP.
3. The no-copy check is stronger than commissioned: line equality AND a 40-character window test over every long template string and every catalogue string, with three planted positive controls (CK10). The catalogue has NO description fields (see Corrections).
4. Plan facts re-measured: 11 absent rows (by program), 143 items, 376 sub-settings, 13 duplicate names (26 items), 137 map entries, 55 `item_key` items, 123 registry controls: all confirmed. The plan's "17 unmapped" is the map's figure; per the crosswalk's rows it is 18.

## Facts re-measured (instrument, time AEDT, control)
| Fact | Value | Instrument | Control |
|---|---|---|---|
| PR 85 | open, draft, not merged, head 851057291ffb, base 308b7aa60cd8, 57 files, 14 commits | `gh api -X GET .../pulls/85` 19:43:24, project `GH_CONFIG_DIR`, account `kamilDatasec` active (read first 19:43:19) | `pulls/9999` HTTP 404 |
| Code main | b4681297d974 | `branches/main` 19:45:38 | equals the plan's |
| Catalogue | 77372 bytes, 143 items (143 distinct ids; policy 72, display 71), 93 items with sub-settings, 376 sub-settings (distinct, none equals an item id), keys only id/name/category/categoryIds/kind/subSettings, longest string 79 chars, 48 strings of 40 or more | python `-I -B` over the raw file at the pinned head | contents API `size` 77372 equals the raw file size |
| Duplicate names | 13 names on 26 items; 130 distinct names | python with the map's `normaliseName` rule | gap analysis item 9 says "130 distinct names" |
| sm-map.ts | 23279 bytes, 679 lines, 137 entries (parsed equals `grep -c -i 'control_id: "'` 137), how name 65 / hand 55 / catalogue-only 9 / name-other-category 8, 55 `item_key` (55 distinct), controls on several entries UQ-016 (2), UQ-077 (3), UQ-095 (2), UQ-104 (3), 17 catalogue items on no entry, 0 bad ids | python regex over `:30`-`:608` | line count of `control_id:` is 138 (the interface line) |
| Template | 132 rows, M001 to M132 once, T-ids equal, `status` APPROVED x132; strings of 40 or more: target 132, why 132, customisation 132, setting 6 | python over the JSON | `analysis_row` counts 132 by grep |
| Seeds | `map132.txt` 11 `-> None` rows (8, 37, 38, 50, 80, 89, 98, 106, 109, 111, 130), at most one `UQ-` per row; `map132_sm316.txt` UQ column None on the same 11; join key proved 132 of 132 (sm316) and 131 of 132 whole + row 39 prefix (map132) | python | prefix row 39 truncated at 52 chars |
| Registry list | 123 `UQ-` lines (UQ-001..UQ-123) | `grep -c` and python | header line separate |
| PCOMP-29 | Backlog, labels composer-seed-1023 and plan-comp-328, 0 comments, updated 2026-10-23 11:31:42; scope sentence quoted in the kit | Jira GET (`jget.py`, GET only, token in-process) | PCOMP-9999 404; PCOMP-36 shows 2 comments |
| Prior work | 200 branches (2 pages), 0 matching; 130 PRs, titles 0 and bodies 0 matching | `gh api -X GET --paginate` | `^b1569` 1; titles `deploy guide` 12; bodies `hold k6` 1 |
| Root repo | HEAD 53fcad7b on `main`, no remote, config email kamil.kreiser@datasec.com.au (HEAD committer and author equal it), no `index.lock`, 0 staged, `records/b1801` and `.tools/b1801` absent, 1325 status lines (4 modified old STATUS files, rest untracked) | git read verbs | `records/b1688` resolves 3b192407; code clone prints `origin` |
| Seat ids | `SEAT-C104` is B1604's (2026-11-16) and `SEAT-C105` is B1606's; C106 and above 0 | `ls` of the briefs folder | 7 files match `SEAT-C10[45]_` |
| Live panes | 12 panes, 0 named Composer | `tmux list-panes -a` 19:50:24 | pane %0 prints `tuesday` |

The drafter's prototype (`proto.py`, a claim, not code) of rules R0 to R5, all 132 rows resolved: 112 on a one-entry control, 4 by R3a (rows 81, 83, 103, 104), 3 by R3b (116, 117, 118), 1 by R3c elimination (row 82), 1 spanning (row 16), 11 absent. 125 of 143 catalogue items on rows, 18 on none (13 Cloud twins plus `ILCloudInfoTab`, `PLCloudAutoFWUpdate`, `ILEntraIDSetup`, `PLFirewallConfig`, `PLFtpServer`); 7 of 376 sub-settings named by the map's entries (8 with the hand row H-1); 7 map entries on no row; rows with no vendor item: 80, 106. The seed's SM id differs from the map on rows 36 (a Cloud twin) and 114 and on the 8 absent rows that the seed names and the map holds only as `SM-` catalogue-only entries.

## Answer to item 4 (the required question: three things that are not a clean one-to-one row)
1. **Duplicate vendor names (13 names, 26 items).** COVERED by flag, not a limit. The seed's own name match picked the Cloud twin on row 36; rows take the map's hand-resolved on-device item; `DUP_NAME_ITEM` and `SEED_DIFFERS` mark them; each Cloud twin is listed once in `catalogue_items` with `NO_SAMPLE_ROW`, `DUPLICATE_NAME_TWIN` and its peer.
2. **Catalogue items no sample row maps to (18 of 143).** STATED AS A LIMIT. The crosswalk is sample-row first, so "every catalogue item" means every item is listed once with its rows or `NO_SAMPLE_ROW`, in `catalogue_items`, the README and `_meta.counts`.
3. **Sub-settings (376; only 6 sample rows are sub-settings: 8, 114, 115, 116, 117, 118).** COVERED by listing, stated as a limit: all 376 ids sit under their parent item; the named ones in `sub_settings_named` with their rows; the rest are "not named by the sample". Also stated as limits: 7 registry controls on no row, 6 shared-item sub-controls whose map entries are on no row, rows 80 and 106 with no vendor item, and M008's sub-setting (a hand row, H-1).

## Corrections to the commission and to the plan
1. **Commission: "the catalogue's description fields" do not exist.** The catalogue has no description or help field. CK10 covers every string of the catalogue and every long template string, by line AND by 40-character window.
2. **Commission: seat id C104 is already used** (B1604, finished 2026-11-16) and C105 (B1606). The commission's "highest seat id" scan window (19th and 20th) could not see it. Next free is C106. The kit follows the commission; Tuesday may rename (Q-1).
3. **Commission and DRAFTER_RULES.md disagree on the drive:** the rules file names `/Volumes/Laptop-DEV/...` paths (its fence 4 and launch line); the commission and the existing paths are `/Volumes/Datasec_DEV/...`. The kit uses the commission's.
4. **Plan: "the first 100 of 199 branches"**: now 200, read in full, 0 matching. The plan's "17 of 143 unmapped" is the map's figure; per rows it is 18.
5. **Plan lane CW-1 "Reads: map132.txt and map132_sm316.txt existence checked, not read":** read now; the seeds disagree with the map on 2 rows by id (36, 114) and carry vendor ids on 8 rows the registry lacks. The kit makes the map the authority and the seed a cross-check.
6. **Ticket PCOMP-29:** its folder name `Content/2026-10-20_<sample>-template/` and "SM catalogue lives on the sibling project's branches" are superseded by the plan (the Composer's own PR 85); the ticket's K4 allows vendor ids AND names, the commission is stricter (ids only): the kit follows the commission (Q-2).
7. **C-90 leaves the Q-04 "HP-internal identifiers" question open** (its own text: "not decided here"): the kit keeps this folder internal and lists it under FOR TUESDAY.

## D-decisions (the drafter's, for Tuesday to confirm or change at the stamp)
- D-1 ADDED source `registry_list.txt` (ids only, 123 controls): lets CK5 prove every registry id exists and gives `registry_controls_no_row`. Not on the commission's list.
- D-2 Output shape: one JSON (`_meta`, `rows` 132, `catalogue_items` 143, `map_entries_unattached`, `registry_controls_no_row`) plus a README of at most 70 lines; the sample's `setting` text and vendor names are NOT carried; the sample's `section` (8 enumerated names) is.
- D-3 The map (`sm-map.ts`) is the authority for registry-to-vendor; the seeds are cross-checks (flagged, never overridden by guess).
- D-4 One hand row, H-1 (M008 to `ILUnifiedPassword` / `PLAutoEWSAdminPasswordReset`), from two records (gap analysis item 9; the map's reason on UQ-008), proved by program against the catalogue.
- D-5 Commit on `records/b1801` in a worktree; slot REC-MERGE (HOLD or MERGE) added; no push (the root has no remote). Under slot RECORDS `DRY` the files are built under `.tools/b1801/dry/` only.
- D-6 Review tier G2, agreed with the plan, plus: the gate re-runs CK10 and CK12 itself.
- D-7 Model row C2 (as the plan), Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes; no heavy lock, no docker, no ports.

## Q-questions for Tuesday (each with a default; none blocks the draft)
- Q-1 Rename the seat id to C106 (B1604 and B1606 used C104 and C105)? Default: keep C104 as commissioned (no live pane, the earlier seat finished 2026-11-16).
- Q-2 Carry vendor item names (C-90 permits them)? Default: NO (the commission's rule); a later kit change if wanted.
- Q-3 REC-MERGE HOLD or MERGE? Default: HOLD (commit only; the G2 review reads the worktree; the records pass folds it).
- Q-4 Accept `registry_list.txt` as an added id-only source? Default: yes.
- Q-5 Hard stop: recommend READY target 150 minutes after Step 0, HARD STOP 210 minutes after (a clock is Tuesday's to type at the stamp).

## Recommended slots
BASE: PR head 851057291ffb019baee6c3c51a50d7b8833f5b3a plus the seven sources' sizes and sha256 prefixes of FACT 2 (printed from `sources_sha.txt` in scratch: template JSON 137914 `a43f5c5102a96a2f`, template README 3984 `7fff32884771111e`, map132 18106 `df4de694e68640a1`, map132_sm316 16129 `348cf49795cb59a6`, registry_list 11075 `2a960c83484fa09f`, catalogue 77372 `5dc1192d9a3a73bc`, sm-map.ts 23279 `3c48b72a9374a455`). ROOT: root main 53fcad7b11231ea8db6551b377a84734c6c28346; code main b4681297d974ac3d8e74a4a12baeb9ea41962c52. RECORDS: WRITE. REC-MERGE: HOLD. HARD STOP: Tuesday's clock.

## Load (by program)
Kit 50133 bytes; READ list (7 whole sources 287859, three record slices 9769, the PCOMP-29 text 1940) 299568; total 349701 bytes, under the 400 kB limit. The template JSON (137914) is read by program only and never printed, so the seat's context cost is far smaller.

## Chain inputs (each step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | Made by |
|---|---|---|
| 0 | this kit, root repo, `date +%F`, template files | BASE (exist) |
| 1 | `pulls/85`, the two PR files, five local sources, PCOMP-29, plan lines 94-102, C-90, gap analysis 369-392 | BASE; the raw PR files are fetched in Step 1 |
| 2 | branch and PR lists, Jira, records greps | BASE |
| 3 | sources of Step 1, `crosswalk_build.py` (seat writes it) | Steps 0 and 1 |
| 4 | in-memory JSON and README text | Step 3 |
| 5 | the two written files, the sources, scratch mutants | Steps 1 and 4 |
| 6 | the written files, the checks logs | Steps 4 and 5 |
| 7 | all logs, STATUS | Steps 0 to 6 |
The worktree is created in Step 4 and nothing earlier needs it.

## UNMEASURED
- The seat's own program, every check CK1 to CK16 and its controls: designed, not run (the prototype ran the resolution only, not the checks, not the write).
- Whether the map's `item_key` entries are policy items that exist at code main (RELAYED from the map's own comment `sm-map.ts:3`-`:6`); the drafter did not read main's content release.
- Whether `git worktree add -b records/b1801` succeeds against this root's dirty tree: precedent B1688 did it; the drafter ran no ref write.
- The name list of CK12 (built by the seat from the template's `_meta` and the build-plan file name): not run; the drafter never printed any name.
- `status_watch.sh`, `launch_when_cool.sh` and the cockpit: not run. No lsof (no port block needed).
- Whether anyone else holds a live Composer pane beyond the 19:50:24 read.

## Outside-the-fences disclosure
Read-only everywhere except this report, the kit, its sidecar and scratch `fleet/state/s301/d1801/`. Reads outside the kit's own list: PCOMP-30 and PCOMP-36 (Jira GET, to learn what CW-2 expects), B314, B330, B532, B321 and B328 STATUS head, tail and grep lines, BACKLOG row #328, C-89, C-90, C-100 headings, the gap analysis section 5, the stale `.pre-` and measured files of the two form kits only by name. No write to Jira, GitHub or any record; no request to any hosted site beyond `gh api -X GET` and Jira GET; nothing of HPSM-POC opened (the catalogue's own `source` string names it as provenance; not followed); no cd; nothing deleted (my first sidecar skeleton was moved aside to scratch, my own file). One instrument slip: a first `echo` separator beginning with `=` was refused by the shell hook and re-run without it; one control I first chose for the root git log (`PCOMP-74` in a commit message) printed nothing because those commits do not carry the key, so it was not used as a control.
