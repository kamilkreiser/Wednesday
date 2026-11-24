STARTABLE: YES

# B2054 DRAFTER REPORT (Datasec / OXPd 2, records kit for pull requests 46 and 47, seat R317)

Drafter: in-session Agent, read-only on every project; wrote only the kit, its sidecar, this report and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s323/d2054/`. Window by `date`: 18:15:05 to about 18:40 AEDT, Tue 24 Nov 2026.

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2054_SEAT-R317_oxpd2-records-pr46-pr47.md` (304 lines, about 84000 bytes). Sidecar: the same name plus `.measured` (110 claims, 110 measured; `stamp_check.py <kit>` exits 0, run last).

## BLUF
- One OXPd records pass for the two landings, in the form of B2045: ONE history entry; `BACKLOG.md` ticks of 79, 83, 87, 116 and (slot TICK95, default TICK) 95, each with a `Closed:` line; a `Closed in part` line on 84 and 96 (both stay open); SEVEN new owed items 119 to 125. NO clarification entry, NO `CLAUDE.md` edit, NO Jira write (GET only). Two record files written (BACKLOG.md, history.md), by HOLD R / R2.
- Texts are frozen (20, sha256 table in the kit); each was scanned by the project's own `scan_record` (copy of `b1785.py`, sha256 `5e766b28...`, the file the seat will use): 0 problems, 0 bytes above 126, no `<<` but the six fill-ins, both slot variants.
- Dry builds on the live files: BACKLOG (TICK) 878 to 934 line feeds, added 56, changed 5, owed 1 to 125 no gap, anchor 863 to 919; (LEAVE) 933, added 55, changed 4. History 321 to 328. The proof by position (added lines removed by position, `[x]` put back by position) equals the old bytes in both variants.

## Facts re-measured (instrument, control)
- Seat id R317 free: word scan (`-w`, case-blind) over 221 non-`.pre-` SEAT kits of the last 8 days: 0 hits; control R316: 4 lines in 2 kits (B2045, B2049). No `R317` file name in the briefs folder; `tmux list-panes -a`: `%0 tuesday` and two unnamed.
- Project state equals B2045's `READY.manifest` (sha256 of CLAUDE.md, BACKLOG.md, history.md, CLARIFICATIONS.md and the register, all 5 equal) at 18:15; last line of B2045 STATUS is its READY line.
- Landings by `gh api -X GET` under the project's `.gh-config` (account read by `gh auth status`): main `89a10a1b` (tree `4933b988`, parent `c6f5d36a`, 18:08:17 AEDT); PR 46 merged 05:56:16Z = 16:56:16 AEDT as `c6f5d36a` (head `77641b0e`, 7 files, +109 -20); PR 47 merged 07:08:18Z = 18:08:18 AEDT as `89a10a1b` (head `a7f74ff3`, 15 files, +982 -94). Both single-parent squashes; trees equal the gates' (`41cad605`, `4933b988`). PRs: 47 in all, 0 open, merged numbered 44 or more exactly 44 to 47 (control `pulls/44` = `b0b26b60`).
- Hosted at each merge commit: 7 of 7 check runs success; job logs read: c6f5d36a linux 2110/4 skipped of 2114, windows 2093/21 of 2114, rules 657 files; 89a10a1b linux 2149/4 of 2153, windows 2132/21 of 2153, rules 659 files, `failed: 0` on all four (control: the first log read printed 0 bytes without `--allow-escape-sequences`, 51502 with it). Code scanning analyses results_count 0 for 3 languages at both (control: 12 rows listed); open alerts 0 has no control of its own (closed alerts also 0), so the kit says only the analyses rows prove anything.
- Source at main by TARBALL (`gh api -X GET .../tarball/89a10a1b...`, 1709518 bytes, 659 files, extracted into its own new folder; read by `python3 -I -B`): `facts.py` 66 PASS 0 FAIL with four controls False (print in `facts.out`): every file:line pointer of the texts, `new DeviceTokenClient(` 0 lines in `src/` and 12 in one test file, `CertificateChainPolicy` 0 lines in the three other handlers (control 1+ in DeviceTokenClient.cs), `ReadOnlyViolations(` only at `Oxpd1Read.cs:124` and `:128`, and the owed-116 counts: `sharedWithMe`, `drive/recent`, `/recent`, `recent` each 0 lines; controls `GraphClient` 16 lines in 8 files, `drive` 93 in 15, `zzqxnonexist` 0.
- Owed 95 re-proved: Lab Oxpd1 README names the pipe shape at `:174` ("as for `oxpd1 read`"), and at `b0b26b60` (PR 44) at line 123 of 124 (read by `contents?ref=` raw); `LabFiles.cs:34` still `File.ReadLines` (code unchanged), README `:35` to `:37` (exit 7) does not name a pipe. The text says all three; a code fix is not filed (Q2).
- PR 46's diff of `IppTransportException.cs` (compare API): 3 added and 1 removed lines, all `///` (comment only). PR 46 and 47 file lists equal the owed-item Where lists (7 and 15).
- Jira (GET only, the project reader, a read-only fence in my script): census 62 (OXPD2-1 to 62, from R316's create), Done exactly 33, 39, 41, 47, control `no-hardware` 23, `OXPD2-99999` 404; 17 phrase searches for the new items' "Jira:" lines each 200 with 0 issues; controls `named pipe` and the MASTER title find OXPD2-1. `sharedWithMe` finds OXPD2-55 (design documents; named in no text).
- BACKLOG probes for each new/ticked item and Jira-line term (P-3): counts as the kit prints (all 0 except the controls and `CertificateRevocationCheckMode` 1). `Tuesday's reading` in CLARIFICATIONS is now 42 (R316's C-84), not 41; the kit says 42.

## MEASURED LITERALS table (rule 4: every chain step's inputs, each from an EARLIER step or present at BASE)
| Step | Inputs | Where each comes from |
|---|---|---|
| 0 | kit, sidecar, five project files, df, python, tmux | exist at BASE (Tuesday's briefs folder; project) |
| 1 helper | `b2045.py`, `b1785.py`, the scanner copy | BASE files; the scanner copy is made in Step 0 |
| 2 | SOURCES rows, `READY.manifest`, GitHub, Jira reader and `.env`, the tarball | BASE; the tarball and its extract are made inside Step 2 (P-F) before use |
| 3 dry run | frozen texts, before-copies, helper, facts | kit; Step 0; Step 1; Step 2. `<<BL-NEW8>>` from the dry BACKLOG built earlier in Step 3 |
| 4a | the Step-3 build, live BACKLOG bytes | Step 3; BASE (re-read) |
| 4b | live history bytes, `<<BL-NEW8>>` | BASE (re-read); 4a's print |
| 5 | all prints, the manifest | Steps 0 to 4 |

## D-decisions (mine, for Tuesday to overrule)
- D1: model. The commission says "Sonnet" for B2054 but the OXPd `CLAUDE.md` line 7 (the product owner's C-56 word) says Opus for every agent on the project, and B2045 (the form) ran Opus; model-routing C8 (line 98) is about drafting and has no records-seat row. The kit is written for Opus (launch line `BRIEF_SEAT_LEVEL=opus`), Q1.
- D2: no C-entry. CLARIFICATIONS counts 0 on every lane subject (P-3); the coordinators' choices are not his words. Precedent: B2041's history line. Q3.
- D3: no Jira write (the form's Jira verbs answered a product-owner note). Q8.
- D4: the fix-lane item (124) is ONE item for B2052 FOUND 1 to 3, as commissioned, and names kit B2053 as the coordinator's plan and its ordering before first-run row 2 as the coordinator's reading (relayed from the commission); P-L stops the seat if main moved or a PR numbered 48 exists.
- D5: seven new items rather than fewer: 119 (server sentence), 120 (two platform words), 121 (other handlers without a chain policy), 122 (dead revocation-mode line), 123 (PR 46's other points), 124 (PR 47's three Minor points), 125 (PR 47's other points); the form of items 104 to 111. Q5.
- D6: item 95 ticked by the item's own second route (README names the shape) with the honest note that the code still hangs on a pipe; slot TICK95, default TICK. Q2.
- D7: the seat reads main by tarball and `gh api -X GET` (no git verb in the project), the gate's clone was used only by me for pointers and is not a source in the kit.
- D8: launch line in today's form (`launch_when_cool.sh ... CLAUDE_CONFIG_DIR=... BRIEF_SEAT_LEVEL=opus bash brief_seat.sh`), copied from B2049 line 249, not the older `cockpit.sh add` of B2045.

## Questions for Tuesday (each with a default; the kit's Q1 to Q8)
1. Model: Opus (default) or Sonnet as the commission says.
2. Slot TICK95: TICK (default) or LEAVE (item 95 stays open for the code fix).
3. Clarification entry: none (default).
4. Tick 83 beside its finding (item 120): tick (default).
5. Seven new items as frozen (default) or 119 and 120 merged.
6. Item 124 and its kit B2053 wording: as frozen; re-hash 124 and H-OWNER if the lane has landed or been renamed by the stamp.
7. No owed item for the lab's WS-Addressing default (default).
8. No Jira write (default).
Slots for Tuesday to fill at the stamp: RECORDS (default HOLD), TICK95 (default TICK).

## UNMEASURED
- The seat's helper, selftest, HOLD R and HOLD R2 on the live files, and the stop after a partial write: never run on a real output (marked in the kit). The kit's frozen-text fills (date, clock, sha8) are prototype-only here.
- Every review measurement relayed in the texts (macOS arm64 probes, mutants, the 40 root spellings, probe P04 and so on) is the reviewers', not re-run; Linux and Windows fetch behaviour; the M577; anything on a device.
- Whether another OXPd records pane exists when the kit is launched (REFUSE 5 is the seat's check). Whether the regenerated tarball has the same sha256 (the kit says a difference is named, not a stop).
- `date` values inside the sidecar that say "18:3x" were replaced by a run at 18:32:32; the Jira census is a moment read.

## Outside-the-fences disclosure
- I read git objects of another seat's scratch clone `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s323/g2052/clone` (read verbs only: show, grep, ls-tree, diff, log, rev-parse, cat-file, status --porcelain; with `--no-optional-locks`) for pointers; not the project repo; no fetch, no write. The kit does not cite it as a source.
- I read `fleet/specs/model-routing.md` (lines 94 to 102), `models_latest.json` (grep), `tools/launch_when_cool.sh` and `brief_seat.sh` headers, three other kits' stamp sections and launch lines (B2043 pre-stamp, B2048 pre-stamp, B2049 line 249), all in Tuesday's briefs or tools. I did not read `briefs_staged/`, the scoreboard, any ledger, any card store or board, WEDNESDAY, FRIDAY or any other client.
- Three small stamp_check output files were written to `/tmp` (`x_unused.txt`, `sc_unused.txt`, `sc_out.txt`), not the scratch folder, before I switched to `d2054/init.out` and `check.out`; they hold only the tool's printed claim list. One `sed -i.bak` on my own scratch `sidecar.py` (a `.bak` stays in scratch), one `cp` of `pr46.json` to `pr46.json.keep` in scratch. Nothing deleted.
- Jira: the project's `.env` was loaded by the project's own reader (a copy of `b1785.py` in my scratch) in-process; nothing printed from it; a GET-only wrapper refused any other method. GitHub: GET only under the project's `.gh-config`. No HTTP to any printer or hosted host; no az, ssh, docker, mail; no write to any project, Jira, GitHub or card store; one cd was refused by the hook at the start (before it ran) and one `==` echo separator was refused by the zsh hook; both re-issued without.
- Nothing of another client read or written; no human messaged.
