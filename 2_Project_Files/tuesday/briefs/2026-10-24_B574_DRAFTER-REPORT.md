# B574 DRAFTER REPORT (SEAT-M12, fix round for PR #104)

Drafted 2026-10-24, clock read from `date` (about 10:1x to 10:21, local). Read-only in the MPS repo. Brief: `2026-10-24_B574_SEAT-M12_mps-104-fix-round-2.md` (99 lines, sha256 `730fd73d8640bf772cf562d1dd86e0238303ed91a7cf38ba48aef16ae5feba64`), `.pre-stamp` beside it (`cmp` rc 0, 8 lines with the four-underscore pattern, lines 84-90 and 99; 0 non-ASCII bytes by `python3 -I`, control 2; 0 typed clocks of the HH:MM shape).

## What I read
- Gate STATUS `.../Briefs/2026-10-24_B562_STATUS.md`, whole (509 lines): findings at 378-436, round-cap statement 452-465, mutant table 193-232.
- B568 brief (whole, 80 lines) and its `.pre-stamp` lines 62-72 (slot label shape); B560 brief (whole, 114 lines: heavy-slot, port, partition, property-check shapes).
- At `655606a9b7a77bc92b7ef35e3302c4369c7d4029` (git show/grep only): `PanelSectionMapCodeTests.cs` (162 lines), `ReferenceDocumentValidatorSupplyEdgeTests.cs` (65), `SourceLifecycleTests.B560WhitespaceId.cs` (77), `SyntheticBooks.cs` lines 14-40, 104-150, 166-177, 225-245, `PriceBookImporter.cs` 176-206, 415-435, 645-690, `SynnexBook.cs` 61-75, `ReferenceDocumentValidator.cs` 205-215, `docs/IMPORTER.md:127`.
- `stamp_brief.py` header (the real path is `2_Project_Files/tuesday/tools/stamp_brief.py`): fills slots by label, refuses typed clocks. Project `CLAUDE.md` lines 46-60 (branch push only, Tuesday merges).

## Premises, each with file:line
- Head and base: `ls-remote` branch = `refs/pull/104/head` = `655606a9...`, main `a5b4bbb5...`; `pulls/104` open, not draft, `clean`, 7 files; `rev-list --left-right --count` = `0 7`.
- P8/P9/P16 anchor: `PriceBookImporter.cs:660`, `git grep -F` of `group.Any(d => string.Equals(d.Sku, o.DeviceSku, StringComparison.Ordinal))` = one hit. Set built by sheet: `map.Devices.GroupBy(d => d.ModelSheet)` at `:657-660`.
- W5 anchor `SourceDocumentChecks.cs:132` `if (string.IsNullOrEmpty(id))`, one hit. V1e-V1g anchor `ReferenceDocumentValidator.cs:211`, one hit.
- Docs clause: `docs/IMPORTER.md:127` contains the clause once (case-insensitive count 1, control 0).
- Second device already in the sheet: `SyntheticBooks.cs:235` (`J14 SYN-A3B`, "not in the map"); map shape lines 31-35; `PriceRow`/`DevicePrices` are private (`:166`), so the new row writes its own `Price List` row by the tweak hook; a mapped device with no row blocks (`PriceBookImporter.cs:423`); `FindInPriceList` compares ordinally (`SynnexBook.cs:74`), so the case-twin needs its own row; map duplicate and option-device checks are ordinal (`PriceBookImporter.cs:182-204`).
- Existing helper shapes the new rows copy: `PanelSectionMapCodeTests.cs:32-76`, supply fact `...SupplyEdgeTests.cs:53-64`, tab fact base `SourceLifecycleTests.B560WhitespaceId.cs:26-38`.

## Partition program output (gh `pulls/<n>/files --paginate`, `grep -x -F` against the Yours list, plus the glob form)
```
lane #102 paths 21 shared-exact 0 shared-by-glob 0
lane #105 paths 17 shared-exact 0 shared-by-glob 0
lane #106 paths 8  shared-exact 0 shared-by-glob 0
control planted (docs/IMPORTER.md appended to #106 list): 1
control self #104 list vs Yours: 4 (the 4 existing Yours paths; the 5th is the optional new file name)
```
Open PRs: #102, #104, #105, #106 only. Live MPS panes: `Datasec/MPS-M9` (%367, round 3 on #102), `Datasec/MPS-G73` (%364, gate on #105); other-project panes `HPSM-POC-H10/H11/G75`, `tuesday`, `fleet-monitor`. B573 (SEAT-M11, #106 round, `tests/MpsCalc.Engine.Tests/Reconciliation*.cs`) is named NOT yours in the brief; no B573 file existed at drafting.

## Ports and stray checks
- `lsof -nP -iTCP:9240-9249 -sTCP:LISTEN` empty (rc 1). `/usr/bin/grep -o -w -E '924[0-9]'` over `briefs/2026-10-2[34]_*.md`: no hit (rc 1); positive control `916[0-9]` over the B568 files printed 9160 and 9169. Today's briefs name up to 9213 (ranges 9100-9219); nothing at or above 9220.
- `.tools/b574` and `.tools/wt-b574-mut`: absent. `.tools/heavy-slot-1` and `-3` exist (other seats), `-2` free; `.tools/.git-lock` not present at the listing.
- load1 at drafting: 24.15 / 13.86 / 10.57 (brief tells the builder to wait, with a heartbeat).

## Rulings I made inside the commission
- Append the Import rows to `PanelSectionMapCodeTests.cs` (its helpers are private); a new file beside it is the fallback and is in Yours.
- Supply row: price `new decimal(1,0,0,true,28)` (the smallest step), fallback to the largest step giving one issue if the issue count differs; extra mutants V1h, V1i added to show the step.
- Docs: delete exactly `: a SKU listed on several sheets is a row on each, so they are not distinct SKUs`, leaving the 371 parenthetical; proved by a subsequence program. Amended WORDS-DRAFT string 5 reported as deletion only.
- Expected rows: 3 panel rows (second-device-only, first-device-only, case-twin) + 1 supply + 1 tab = 5 added; Import 179 -> 183, Api 2,210 -> 2,211, Engine 394.
- Expected kills: P8 by second-device row; P9 by second-device and first-device rows; P16 by the case-twin row; W5 and W1 by the tab row; V1e-V1i by the one-step row.

## UNMEASURED
No build, test, mutant or probe. Not measured: that `SYN-A3B` and the lower-case twin can be mapped and imported (`Succeeded`) through the `Action<XlsxWriter>` hook alone; that minus 1E-28 gives exactly one issue (the brief carries a fallback); that each row is green at the head and dies under its mutants; mergeability at launch; Jira after the gate's read (no Jira call made by me); whether a #106 round brief B573 later names a path in Yours (the lane files make it unlikely).

## Deviations from B568's shape
- Tests-only round: "red first" restated as green-at-head then red-under-named-mutants (B568 had a real defect). Added a small differential against `a5b4bbb5` (rows exercise the Warning only).
- Added REFUSE lines for the heartbeat file, the shared `.git-lock`, the stray `=`/`MPS`/`Commercial` project-root files, and the zsh `$H:t` hazard I hit myself while drafting.
- Replaced the round-1 brief's `grep -P` non-ASCII check (macOS `/usr/bin/grep` has no `-P`, I confirmed the failure) with `grep -E '[^[:print:][:space:]]'`, with controls.
- Slot labels cloned from B568 (7 slots plus READ-WHOLE, 8 lines); slot lines end in the four-underscore token. No gauge figure in the model-receipt label (the routing line given in the commission is used verbatim).
- The `.pre-stamp` was made with `cp` (byte-identical, `cmp` rc 0) rather than a second Write, to guarantee byte identity.
