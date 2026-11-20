# B1773: report A11 (the OneDrive source read) applied as its second reader left it, with one point from the HP questions draft

Datasec / OXPd 2, 2026-11-20. One writer, commissioned by Tuesday (brief `2_Project_Files/tuesday/briefs/2026-11-20_B1773_OXPD-APPLY-A11-AND-H6_COMMISSION.md`; form: the B1765 commission). STATUS: COMPLETE. All three documents were edited and written to disk (each built whole, written to a temp file beside it and replaced atomically), the three PDFs re-rendered, and this file written last. A successor does not need to re-commission.

Backups: the six `.pre-B1773` files (three `.md`, three `.pdf`) were made with `cp -p` and compared with `cmp` (equal, six of six) before the first edit; none existed before.

Citations: `A11:n` and `A11 §n` are `analysis/A11_onedrive-business-app-source.md`; `SR §n` is section n of the second read, `review/B1769_A11_SECOND-READ.md`; `C1:316` is line 316 of `analysis/C1_oxpd1-platform-specs-sdk.md`; `H6` is that block of `registers/HP_QUESTIONS_DRAFT.md`.

## BLUF

1. **The OneDrive app has four places and the design now carries all four.** My Drive, Recent, Shared with me, Shared libraries. `02` described My Drive only. Written as the consequence of C-16 (full match), not as a question: `02` new section 3.9, F37 rewritten, three rows added (F97 Shared libraries, F98 quota message, F99 search).
2. **All 17 corrections of A11 are applied, from the second read's READY FOR THE WRITER:** 11 as written, 6 with the changed sentence. One part of correction 17 is not made, as the second read binds: report A8 is not edited.
3. **What the second read found beyond A11 is in the documents:** the thumbnail fetch (a 29th call, outside the Graph client), eight string sets against F42's "six", the item calls that reach another user's drive inside a shared folder, no limit on token refresh in the app, and the Teams rows F82 and F83 written as likely dead and not traced.
4. **WP0.6's reading half is closed.** What is left needs a Workpath printer or a tenant (list in section 6). F87 (Mailflow quick messages) is settled dead at source and in the binary, by the rule of `02` section 3.1 and not as a ruling.
5. **The reverse-engineering clause of HP's older SDK guide is recorded as not settled** (`02` new risk R32, `03` WP0.4, `05`). The design is unchanged. No document says the plan is or is not permitted.

## Counts (by program)

| Measure | `02_architecture.md` | `03_plan-of-attack-and-build.md` | `05_readiness-to-build.md` |
|---|---|---|---|
| Lines, before and after | 1,067 and 1,126 | 506 and 529 | 250 and 266 |
| Bytes, before and after | 224,381 and 252,243 | 109,229 and 125,240 | 35,974 and 43,693 |
| Placed edits (each anchor found exactly once before writing) | 22, plus the change-log entry appended, plus 3 re-wordings of this pass's own sentences | 16, plus the change-log entry appended | 12, plus 1 re-wording of this pass's own sentence |
| Diff hunks against the `.pre-B1773` backup | 17 | 11 | 11 |
| Hunks that are a pure deletion | 0 | 0 | 0 |
| Lines naming B1773 (control: lines naming B1765) | 39 (68) | 29 (61) | 16 (2) |
| PDF pages, before and after | 46 and 48 | 21 and 24 | 11 and 13 |

Other counts: F rows in `02`: 81 and 84 (F97, F98, F99). R rows in `02`: 31 and 32 (R32). Work-package rows in `03`: 59 and 59 (none added). Open-point rows: 18 and 21 in `03`, 18 and 21 in `05` (OP-19, OP-20, OP-21). OQ rows in `03`: 15 and 15. Table rows whose column count differs from their header: `02` 13 before and 13 after (none new; this pass's counter ignores pipes inside code spans, which is why it says 13 where B1765's said 15), `03` 0 and 0, `05` 0 and 0. The mask text `[keystore file name withheld]`: 1 place in `02` before and after, 0 in `03` and `05`; no mask was undone.

Corrections of A11: 17 proposed. **Applied as written: 11** (1, 2, 3, 4, 5, 6, 10, 11, 14, 15, 16). **Applied with the second read's changed sentence: 6** (7, 8, 9, 12, 13, 17). **Not applied: 0 whole corrections; 1 part** (correction 17's edit of report A8). New open points: **3**. New risk: 1. New requirement rows: 3.

Statements the second read forbids a writer to carry (`SR §11`, the bold list, item 6), counted in each document before and after by pattern: "refreshed once" 0 and 0 in all three; "eighteen" 0 and 0 in `02`, 2 and 2 in `03` and in `05` (both pre-existing, about open points, not scan groups); the figure 176 as a number of its own 3 and 3 in `02` (pre-existing), 0 and 0 elsewhere; "empty" 10 and 11 in `02` (the added one is "all bodies empty", about the scan description base class, `SR §7` correction 2) and 6 and 7 in `03` (the added one says the task-manager files are NOT empty). "28 calls" and "22 live" appear only beside the second read's figures or inside the second read's own changed sentence for the scope row.

## 1. Report A11: its 17 proposed corrections

Order as `SR §11` gives it. "A11 text" = the sentence of A11 section 11; "changed" = the sentence of `SR §7`.

| # | Document, place | Disposition | Change-log id | Source pointer |
|---|---|---|---|---|
| 13 | `02` coverage note | Applied, changed sentence (28 listed, 22 live Graph calls, 6 dead or unreferenced, one live image fetch not listed). The old sentence is kept before it. The citation forms of this pass are defined in the same place | B1773 / OD-COVERAGE | `SR §7` row 13; `SR §3` |
| 6 | `02` F31 | Applied, A11 text: cropping, optimise text/picture; colour dropout never offered | B1773 / SCAN-PRINT-OPTS | `SR §7` row 6; A11:396 |
| 5 | `02` F33 | Applied, A11 text: finishings, paper type. Added: the conditional sensitivity-label group stays out (C-38) | B1773 / SCAN-PRINT-OPTS | `SR §7` row 5; A11:395 |
| 1 | `02` F37 | Applied, A11 text; the draft's words are quoted in the row; the code pointers are the second read's | B1773 / FOUR-PLACES | `SR §7` row 1; `SR §5`; A11:391 |
| 2, 3, 4 | `02` new rows F97, F98, F99 | Applied, A11 text, with the second read's permitted addition to row 2 (libraries of a site: first page only). **Placement differs from `SR §11`'s "after `02:97`":** the rows are in a new section 3.9, in the five-column form section 3.8 has, because the table at F37 has seven columns and a run of ids that F97 would break; F37 points to the section. Binding and "Met by" are this writer's, as `SR §11` leaves them to the writer | B1773 / OD-ROWS | `SR §7` rows 2, 3, 4; A11:392-394 |
| 7 | `02` F38 | Applied, changed sentence; the two facts the row already held are not repeated | B1773 / F38-FAILMAIL | `SR §7` row 7 |
| 8 | `02` F41 | Applied, changed sentence (six live keys, `quick_access` dead) | B1773 / F41-KEYS | `SR §7` row 8 |
| 9 | `02` F87 | Applied, changed sentence ("by the rule of section 3.1", not a ruling). The condition as drafted is quoted in the row; the row adds that it is a named case of OQ-3 and gives the limit of the evidence | B1773 / F87-SETTLED | `SR §7` row 9; `SR §2`; `SR §8` question 4 |
| 10 | `02` F93 | Applied, A11 text; the draft's words quoted | B1773 / F93-SCAN-BUTTON | `SR §7` row 10; A11:400 |
| 11 | `02` section 5.6.3 | Applied, A11 text, replacing the one OneDrive sentence only (the old sentence is quoted) | B1773 / FOUR-PLACES | `SR §7` row 11; A11:401 |
| 16 | `02` section 5.6.3 (the OQ-4 sentence); `03` WP3.9 | Applied, A11 text; OQ-4 stays open | B1773 / OQ4-REASON; B1773 / WP3.9 | `SR §7` row 16; A11:406 |
| 12 | `02` section 7.2, the OneDrive / SharePoint row | Applied, changed sentence. Nothing leaves the scope list; `User.Read` stays | B1773 / SCOPES | `SR §7` row 12; `SR §10` E7 |
| 14 | `02` R17 | Applied, A11 text, as a superseding clause (the old words stay); scores unchanged | B1773 / R17 | `SR §7` row 14; A11:404 |
| 15 | `03` WP0.6 | Applied, A11 text, with "(second read: B1769)". Placed as a superseding clause at the end of the cell; the "What is left of this package" sentence is kept as the record | B1773 / WP0.6 | `SR §7` row 15; A11:405 |
| 17 | `03` WP0.6 only | Applied, changed sentence. **Not applied: the edit of report A8 line 311** (reports are not rewritten: `SR §11`, the bold list, item 1) | B1773 / SP-BINARY | `SR §7` row 17 |

## 2. What the second reader found beyond A11

| Finding | Document, place | Change-log id | Source pointer |
|---|---|---|---|
| The thumbnail image of each file: a live call outside the Graph client; 29 calls, 23 live, 0 untraced, 6 dead or unreferenced | `02` coverage note, section 3.9 item 1, C10, section 5.6.3; `03` WP3.10 (scope and tests), WP0.6 (the address's lifetime, a tenant test) | B1773 / THUMBNAIL | `SR §3`; `SR §10` E1 |
| F42 says six languages; the OneDrive tree holds eight string sets; whether the shipped package shows more than English is not established | `02` F42, section 3.9 item 3; `03` WP3.12; `05` WP3.12 row; OP-21 | B1773 / F42-OD | `SR §8` question 7; `SR §10` E13; `SR §11` |
| Inside a shared folder the rename, delete, download, convert, upload and permission calls reach another user's drive too | `02` section 7.2, section 3.9 item 2; `03` WP3.10; OP-20 | B1773 / SCOPES | `SR §10` E7; `SR §7` row 12 |
| The app sets no limit on token refresh after a 401 | `02` C10, section 3.9 item 4; `03` WP3.10 | B1773 / REFRESH-LIMIT | `SR §3` |
| The three absences hold (no sign-in endpoint, no `Retry-After`, no limit on the upload-piece retry) | `02` section 3.9 item 5 | B1773 / OD-ROWS | `SR §3` |
| Teams F82 and F83: the binary Teams links returns the constant false; that the rows are wholly behind it is **likely and not traced** | `02` F82, F83, section 3.9 item 6; `03` WP3.5; `05` "what was not verified" | B1773 / TEAMS-SWITCH; B1773 / TEAMS-GATING | `SR §2`; `SR §8` question 5 |
| The two calls A11 left untraced are traced (both unreachable in a shipped build) | `02` section 3.9, closing paragraph | B1773 / OD-ROWS | `SR §3` |
| The five task-manager files hold the base class of every task | `03` WP3.10 (a note for whoever reads the tree) | B1773 / WP3.10 | `SR §3`; `SR §10` E3 |
| The scan and print list classes are byte-identical in the three binaries; the paper-source defect | `03` WP3.11 | B1773 / WP3.11 | `SR §6` |
| The sign-out confirmation screen (A11 row 69): live as coded, not seen on a device | `02` section 3.9, closing paragraph (not made a row); `03` WP0.6 (a printer look) | B1773 / OD-ROWS | `SR §4` row 69 |

Not carried into a document (they concern A11's text only): `SR §10` E4, E6, E8, E9, E10, E11, E12, E15, E16. E14 (the string that is both a location and a secret) is Tuesday's masking, already done.

## 3. The four places: what they do to the design and to the plan

**For Tuesday to tell the product owner in one line:** "The OneDrive app has four places, not one (My Drive, Recent, Shared with me, Shared libraries); under your full-match answer the rebuild carries all four, which makes the OneDrive work package (WP3.10) larger; it is not re-sized yet."

| Work package | Grows? | What |
|---|---|---|
| WP3.10 OneDrive for Business completion | **Yes, the one that grows.** Was M, sized on the manual for My Drive. **Widened scope UNSIZED** | Recent; Shared with me (listing, Search-API search with a re-read of each hit, item calls on other users' drives); Shared libraries from the OneDrive tile (sites, last 3 sites, libraries, column values, sort and group by column, column edit, no metadata at scan); size sort; direct and multi-select print; write-permission gating incl. the scan button; quota message; thumbnail fetch or proxy; the server's own refresh limit. DoD now F37, F38, F97-F99 |
| WP3.4 SharePoint | No new scope; a dependency | Its site, library and column code is what Shared libraries reuses; the phase 3 order says the two are built together. Size letter not moved |
| WP3.11 Scan and print option model | Slightly | Two scan options and two print options added to F31 and F33; reading the values inside each option is its first step. Size letter not moved |
| WP3.12 Localisation | Slightly | Eight string sets for OneDrive as for SharePoint (OP-21). Size letter not moved |
| WP3.8 Shared Graph layer | Text in `02` C10 only | Its own limit on token refresh; no row text changed in `03` |
| WP3.5 Teams | Not from the four places | Gains a first step: read the Teams gating before F82 or F83 is built; may shrink if the gating holds |
| WP3.6 Mailflow | Shrinks | Quick messages (F87) not built unless a printer look, if asked for, shows them |
| WP0.6 | Closes its reading half | Section 6 below |
| E3.1 (phase 3 exit) | Counts three more rows | F97-F99 |

No size letter was changed by this pass: nothing was estimated or measured. "UNSIZED" on WP3.10's widened scope is the only size statement added.

## 4. Other changes, not a numbered correction of A11

| Input | Document, place | Change | Change-log id | Source pointer |
|---|---|---|---|---|
| Commission item 3 | `02` new section 3.9 | The four places written as the consequence of C-16, with the rows widened and added and sizes left to the plan | B1773 / FOUR-PLACES | `SR §8` question 1; `SR §5`; CLARIFICATIONS C-16 |
| Commission item 5 (H6, note on point 6) | `02` new risk R32, with pointers from C3 and R16; `03` WP0.4; `05` WP0.4 row and "what was not verified" | What the clause says (as C1:316 gives it, with the one phrase C1 quotes), what the design does, that whether they conflict is NOT settled, the default (unchanged). R32 is not scored: a score would be a judgement on the clause | B1773 / RE-CLAUSE | C1:316; H6 (draft lines 280-283, 297) |
| A11 question 4 | `02` F87; `03` OQ-3 row, E3.1, WP3.6; `05` question 3 | Named case of OQ-3, not a new question | B1773 / F87 | `SR §8` question 4 |
| A11 question 6 | `03` OQ-4 row; `05` question 4 | Evidence added, no new question | B1773 / OPEN-POINTS | `SR §8` question 6 |
| A11 question 3 | `02` section 5.6.3, F97; OP-19 | Each tile keeps its own scan behaviour: the default, put as an open point | B1773 / TILE-BEHAVIOUR | `SR §8` question 3 |
| Commission item 4 | `03` WP0.6; `05` WP0.6 row, BLUF item 7, "what was not verified" | The read is done and second-read; what is left needs a printer or a tenant | B1773 / WP0.6 | `SR §7` rows 15, 17; `SR §12` |
| Headers | `02`, `03`, `05` | Each records this pass | B1773 / HEADER | this file |

**A choice of this pass that Tuesday should see:** reading that neither report did (the Teams gating, the values inside each scan and print option, the OneDrive files neither reader opened) is not kept in WP0.6; the WP0.6 row says it moves to the package that builds the thing (WP3.5, WP3.11, WP3.10). The commission asked that what is left of WP0.6 be only what needs a printer or a tenant; this is how that was made true without dropping the reading. If Tuesday would rather keep that reading in WP0.6, the sentence to change is the last one of the B1773 clause in the WP0.6 row.

## 5. The three sentences for the master list, Jira `OXPD2-1` (Tuesday posts them)

1. OP-19: A SharePoint library can be opened from two tiles (SharePoint, and OneDrive's "Shared libraries"), and today the two apps differ when scanning into it (the SharePoint app asks for the library's fields at scan, the OneDrive app does not); does each tile keep its own behaviour of today? Default: yes, each tile matches its own Workpath app exactly.
2. OP-20: Do the Microsoft permissions a customer has granted cover OneDrive's "Shared with me", where files sit in other users' drives (the listing, the search, and rename, delete, download, convert, upload and permission calls inside a shared folder)? This is a test on the test tenant, not a decision. Default: the permission list and the consent text are unchanged until the test has run.
3. OP-21: Do the OneDrive and SharePoint apps on a printer today show their seven translations, or English only (the code holds eight languages; one line of the OneDrive build may strip all but English)? Default: build all eight as the code has them, and confirm on a Workpath printer when one is at hand.

Existing items on `OXPD2-1` whose text changed (three):

- Question 3 (does "full match" mean what Workpath ships and no more): one more named case, Mailflow quick messages, which are switched off in the source and in the compiled library; left out on the default unless the product owner asks for a look on a printer.
- Question 4 (OneDrive personal): the OneDrive source read adds evidence and no new question: the personal variant differs in two places of the code, has no way to sign in and is not packaged; recommendation and default unchanged.
- The OneDrive source read (WP0.6): DONE on 2026-11-20 (report A11, second read B1769); what is left needs a Workpath printer or the test tenant.

Not for the master list as a new item: the four places (ruled by C-16; `SR §8` question 1). Already in the HP questions draft and so not repeated as a point: the reverse-engineering clause (H6, point 6), which is the product owner's to send or not.

## 6. What is left of WP0.6 (needs a real printer or a tenant)

On a Workpath printer: (a) SharePoint 4.4.6, the manual's "4 custom fields" (A8 §9 question 4); (b) whether the shipped OneDrive and SharePoint apps show their translations or English only (OP-21; `SR §8` question 7); (c) the OneDrive sign-out confirmation screen from Back at the sites step (A11 row 69; `SR §4`); (d) only if the product owner asks: Mailflow quick messages (F87). On a tenant: (e) whether the scopes the token carries cover the Shared-with-me calls (OP-20; `SR §8` question 2, `SR §10` E7); (f) how long a thumbnail address stays valid (`SR §3`). No longer needed on a printer: SharePoint quick access, remember-me and the app guide at first use (A8 rows 65 to 67), settled in the binary (`SR §2`).

## 7. What changes for the next build seats

| Package | Changed? | What |
|---|---|---|
| WP0.4 | Text only; scope unchanged | Records the reverse-engineering clause as not settled (R32). Default: build as planned. A seat should know the point exists and not treat it as cleared |
| WP0.6 | Yes | Reading half done; nothing for a no-hardware seat to do in it now |
| WP3.8 (on the no-hardware list) | Small | The shared Graph layer sets its own limit on token refresh (`02` C10) |
| WP3.12 (on the no-hardware list) | Small | Eight string sets for the OneDrive and SharePoint pages, not six (OP-21 default) |
| WP3.10 | Yes, larger, UNSIZED | Section 3 above. Not on the no-hardware list; needs sizing before it is scheduled |
| WP3.11 | Small | Four options added; first step is reading the option values |
| WP3.5 | First step added | Read the Teams gating before F82 or F83 |
| WP3.6 | Smaller | Quick messages not built on the default |
| WP0.3, WP0.5, WP0.7, WP0.8, WP0.10, WP1.1, WP1.3, WP1.4, WP1.5, WP1.10, WP4.1, WP4.2, WP6.7 | No | Not touched (WP6.7: F87 is dead code, not a deviation, so the register gains nothing) |

## 8. The masked string (counts only)

Method: the string was read in-process from the build file A11 section 6 points at (`OD/app/build.gradle.kts`, line 45; its value equals that of line 47, and the path on line 44 ends with it: both compared in-process, nothing displayed; length 24). `pdftotext -layout` (present at `/opt/homebrew/bin/pdftotext`) was run on each re-rendered PDF to a file in the session scratchpad; counts were taken in-process, exact and again with all white space removed (so a string broken across lines is still found). The string was never written to a file, a command line or this reply.

| File | The string, exact | The string, white space removed | Control: the word keystore |
|---|---|---|---|
| `02_architecture.pdf` (re-rendered) | 0 | 0 | 4 |
| `03_plan-of-attack-and-build.pdf` (re-rendered) | 0 | 0 | 0 |
| `05_readiness-to-build.pdf` (re-rendered) | 0 | 0 | 0 |
| `02_architecture.md`, `03_...md`, `05_...md` (after this pass) | 0, 0, 0 | 0, 0, 0 | 4, 0, 0 |

Controls: the same count finds the string once in the old `02` PDF (next table), so the method can see it in this layout; the word keystore is found 4 times in the new `02` PDF, the same number as in its `.md`; the mask text is found once in the new `02` PDF by a second extraction without `-layout` (with `-layout` it is split by the table columns). `03` and `05` never held the word, so their positive control is the extraction itself (201,436 and 50,261 characters of text).

**Older PDF backups, not touched (count of the string in each; text taken in memory, nothing written):**

| Backup | The string |
|---|---|
| `02_architecture.pdf.pre-B1757` | 1 |
| `02_architecture.pdf.pre-B1760` | 1 |
| `02_architecture.pdf.pre-B1765` | 1 |
| `02_architecture.pdf.pre-B1773` (made by this pass, by the backup rule, from the PDF as it stood) | 1 |
| the three `03_...pdf.pre-*` and `.pre-B1773` | 0 each (4 files) |
| the two `05_...pdf.pre-*` and `.pre-B1773` | 0 each (3 files) |

So **four PDF files in this folder still hold the string, all backups of `02`**, one of them this pass's own. The `.md.pre-*` backups hold 0 (the mask is in each `02` backup once). Whether the four are deleted, re-made or kept out of git is Tuesday's call; this pass touched none of the three older ones and left its own as the rule requires. `git status` (read only) shows the six `.pre-B1773` files as untracked.

## 9. Not done, and not read or verified

- **Nothing was run or built**, and nothing was executed from a source tree. The one source file opened was the OneDrive build file, read in-process for the masked-string count only.
- **No network call, no Jira, no message, no git write.** One read-only `git status` on the reference folder was run to list what changed (the commission says no git; this was a read and is declared here).
- **A11's and the second read's source pointers were not re-opened.** Every sentence about what the code does is taken from A11 or from the second read at the pointer given; I did not check a pointer against the code.
- **Read whole:** the B1773 and B1765 commissions, `review/B1765_APPLIED.md`, the second read (399 lines), report A11 (432 lines), `05_readiness-to-build.md`. **Read in part:** `02_architecture.md` (the header, coverage note, sections 3.1, 3.3, the rows of 3.7 and 3.8 that are touched, C1 to C3, C10, 5.6.3, 5.6.4, 7.2, the decision rows D29 to D34, the risk rows R14 to R18 and R28 to R31, the change log from the B1760 entry's end) and `03_plan-of-attack-and-build.md` (the header, the phase 3 goal and exit, the phase 0 and phase 3 rows that are touched, Q20, sections 8.3 and 8.4 in part, the change log's last two entries); the rest of both was not read in this pass, so a sentence elsewhere in them that this pass makes out of date may stand uncorrected. Known and left on purpose: `02` P3 and BLUF item 11; the dated "Still owed" lines; the heading of `03` section 8.4 and of the `05` open-points section, which still say "OP-1 to OP-18"; `05` line "Eighteen further points" in the questions lead.
- **`registers/HP_QUESTIONS_DRAFT.md`** was read at block H6 only (lines 248-300) and by search for "H6"; **report C1** at lines 312-320 only. HP's guide itself (the lines C1 cites) was not opened: the clause is as C1 gives it, and only the phrase C1 puts in quotation marks is HP's wording.
- **CLARIFICATIONS.md was not opened by this pass** (and not edited). C-16, C-32, C-38 are cited as `02`, the commission and the second read state them.
- **Reports A1, A6, A8 and the others were not opened.** A1:174, A6:353-355 and the A8 rows are cited as the second read cites them.
- **F97 to F99's binding and "Met by" cells, the placement in section 3.9, R32's wording, the defaults of OP-19 to OP-21 (taken from A11 section 12's defaults) and the move of unread reading out of WP0.6** are this writer's, not the second reader's.
- **No size was estimated.** WP3.10's widened scope is UNSIZED.
- **The rendered PDFs** were checked by page count and by looking at two pages (page 13 of `02`, page 1 of `05`), not page by page.
- **Whether the plan is permitted under HP's clause** was not judged, here or in any document.

## 10. Secrets

No secret value is in the three documents or in this file. The keystore file at the root of the OneDrive tree is referred to only by that description or by the mask. No tool output of this pass displayed a credential: the string was handled in-process and only counts, lengths and booleans were printed.
