# B1848 FOR-RECORDS: corrections a records pass should make, document by document

Gate result: GO WITH FINDINGS @ manifest d4c6f78e (see VERDICT.md). Nothing below changes an answer a document gives; each is a citation, a wording or a missing control. This reviewer edited none of it. Cell ids are `L<line> c<cell>` as in `N1_TABLE.md`.

## Deviation register: `Registers/DEVIATION-REGISTER_DRAFT.md`
1. DEV-07, Workpath-behaviour cell (L25 c3): `02:915` lists (a) device-held and (b) cloud/server-held as the options; it does not say Workpath uses (a). Cite a line that says what Workpath does, or reword to "option (a) of D16".
2. DEV-16, Workpath-behaviour cell (L34 c3): `D1:296` gives MFUG p.31-32 and p.33; p.31-34 is on `D1:519`. Cite `D1:519` for the page range.
3. DEV-21, rebuild cell (L39 c4): "not built unless a printer look shows them" is the wording of `03:108`; `03:183` says only "(if F87's condition holds)". Re-cite to `03:108`.
4. DEV-21, status cell (L39 c6): two claims, one citation. The pointer "D3 (PD:Analysis/K1... once placed)" now resolves (K1 is placed); give it a line citation (for example the K1 answer line) and the file name instead of "D3".
5. Line 43: "they come when tests exist" is not on `03:224`; cite or mark it the drafter's.
6. Line 5: "no row carries" APPROVED has no count or control; add "0 of 21 rows by `grep`, control NEEDS APPROVAL 6".
7. Wording to consider (Tuesday's call, not a defect): DEV-09 is RULED as to C-19 while `02:185` says "Not ruled: open question OQ-5"; the register states this as QUESTION 1. A reader scanning the status column sees RULED only.
8. The labels D1, D2, D3 clash between the seat's documents and the analysis reports (`D1:519`, `D1:296`); name documents by file in cross-references.

## WP0.8 map: `Design/WP0.8_reporting-record-map_DRAFT.md`
1. L12: "no source file in `LIB` defines it" shares one citation (an import line) with "imported from the Workpath SDK". Mark the second RELAYED from the kit's measurement (0 files; control 4 Kotlin files) or cite it separately.
2. L25 (extendedUserInfo), L36 (deviceInfo), L46 (supplies deviceInfo): the absences ("no property of this name", "no `deviceInfo` property", "no device block in `suppliesInfo`") are cited to a head line (2001, 1835-1842, 1420). Cite the full property range (1835-2018; the supplies schema range) or point to the L10 set comparison and give its count and a control.
3. L34 and L63 (`resourceId` is an integer): the excerpt of `:1720` is a bare `"type": "integer"`. Cite the schema header line of `sequenceNumber` with it, so the excerpt shows whose type it is.
4. L45: `:2535` is the head of schema `supply`; cite the `$ref` in `suppliesList` (near `:1444`) for "each item of schema supply".
5. L46: `ReportingClient.kt:153` is `jobObj.add("deviceInfo", ...)`; add the line that shows this is the supply payload (the enclosing function head).
6. L61: "lives only in the Workpath SDK binary": cite or soften to "no source of it was found (kit measurement, 0 files)".
7. L37, L38: add the control for "no column" (the 17-column count at the BLUF is the frame; a column that is present, for example `jobId`, found by the same program, is the control).
8. A one-paragraph plain summary above the BLUF (see item 7 of VERDICT.md).

## K1 `Analysis/K1_wp36-mailflow-compose-switch-first-read.md`
1. Row 1 (`SendFragment.kt:349`): "`onViewCreated` calls `initFab()`" cites only the call line; add the enclosing function line.
2. Row 17 (`SendFragment.kt:117`): the "occurs 4 times, no other line sets it" claim has no excerpt; cite lines 604, 606, 608 or say "by `grep`" with the lines.
3. Row for `MainActivity.kt:400-404`: the guard ("only when the switch is true") and the button target (405-410) are two claims; one cell each.
4. BLUF line 4 ("never reached"): give the count/frame or mark DERIVED with the three lines and a control.
5. A plain sentence for the product owner: what INSIDE THE GUARDED BLOCK means for quick messages (the OQ-3 case, DERIVED).

## K2 `Analysis/K2_wp35-teams-gating-first-read.md`
1. F82 answer line: split "the eight references ... only when the switch is true" from the start-up entry claim, with table rows cited for the first.
2. F83 answer line: `FilesFragment.kt:761-762` is an `isPrintSupport` test; cite the switch line (747) as well; give a count and control for "the only way to pin a folder for print" or reword.
3. Row 14 (`FilesFragment.kt:747-774`): "for a folder" is not in the excerpt; cite the line that shows the bottom sheet is for a folder.
4. Lines 40, 43, 44, 48 (always/only): count, frame and a control each, or mark DERIVED with the cited lines.
5. Line 6 names a keystore-like file at the Teams root as not opened; add `*keystore*` to the prune list in the next kit (the seat's own note, STATUS N7).

## K3 `Analysis/K3_wp09-converter-licence-read.md`
No finding in the sample (5 of 25 cells, all SUPPORTS). Optional: state that the frame of "no other candidate" is the seven searched words, so the finding reads "none of the seven".

## K4 `Analysis/K4_wp311-option-values-first-read.md`
1. Line 12 ("removed ... on every device") and lines 23 to 27 ("disabled, never removed"): give the frame and a control, or reword to "at the cited lines".
2. Line 156 ("no TIFF or MTIFF password handling was found"): bring the 7-file list and the control into the document; STATUS is not part of the document set.
3. Line 5: add a control for "0 pruned paths".
4. A plain paragraph above the BLUF for a non-engineer (what the 11 and 7 groups are; what is still UNMEASURED).

## WP0.10 note: `Design/WP0.10_deployment-tool-design-note_DRAFT.md`
1. Line 65: "the other 21 `.xaml` files are controls, dialogs and resources" is not shown by the one dialog file cited; cite the file list by program, or mark DERIVED (29 minus 8).
2. Line 66: "9 modules" is the count of rows `:51` to `:59`, not on `:60`; cite `:51-:60`.
3. Screen rows (lines 56-63): the section-to-screen mapping is by name; mark it DERIVED.
4. Line 65 "no section of their own": rests on heading counts; add a control.

## Process (for the next kit, not for a document)
1. The EXCERPTS writer clips every source line at about 310 characters. 255 of 2158 excerpt lines are clipped, 133 of the register's 221, and `03:108` (the register's most-cited line, 53 of 142 cells) carries its supporting words past the clip. Write the whole line, or a window around the cited words, when the line is over 300 characters; otherwise a G2 reader of the file alone cannot judge long plan-row citations.
2. doccheck does not excerpt citations in `>` scope notes (15) or `###` headings (18); the K4 heading citations are claims (group listed at a line). Excerpt them or move the citation to a cell.
3. Add `*keystore*` to the prune and refusal patterns (a file named `datasec_printer_keystore` sits at the Teams root).
4. The records rows the seat listed (`03:145`, `03:146`, `03:147`, `03:182`, `03:183`, `03:188`, `03:224`; comments on `OXPD2-19` and `OXPD2-11`; the stale OQ-6 pointers) stand; this reviewer filed none of them.
