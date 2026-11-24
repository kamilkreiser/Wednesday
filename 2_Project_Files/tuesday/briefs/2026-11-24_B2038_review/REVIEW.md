REVIEW B2038: GO WITH FINDINGS

Fable reviewer, read-only, 2026-11-24. Subject: lane D (B2037) removal of OneDrive "Shared with me" from `02_architecture.md` and `03_plan-of-attack-and-build.md` in `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Design/`, against their `.pre-1124b` before-copies.

Counts: Blocker 0, Major 3, Minor 5, Info 5. Line numbers are the current documents' (no line was added or removed before the appended entries, so they equal the before-copies').

## What holds (checked by program)

- The diff touches exactly the lines the commission lists: 02 lines 3, 98, 212, 216, 226, 231, 371, 543, 743, 1259, 1279 plus an 11-line appended entry at 1368; 03 lines 3, 105, 229, 268, 312, 539, 544 plus a 12-line appended entry at 849. Every edit is inside an existing line; nothing else changed.
- The ruling is stated as ruled. Card title, "Drop it", the option detail and the store time 11:31:08 match `CLARIFICATIONS.md` C-82 byte for byte. C-16 is never written as ruled on by C-82: both documents say "C-82 is his word on this feature, not a ruling of his on C-16" and mark the full-match reading as the coordinator's.
- HP quotes match byte for byte: the release-notes sentence against `MAP.md` line 66; limitation, workaround and resolution "TBA" against `DOCS-MAP.md` line 13 (02 twice each, 03 once each; each found once in its source; a control string absent from both).
- Permissions: nothing removed, correctly. `Files.ReadWrite.All` was in the row before B1773 (A11:412 says "keep `Files.ReadWrite.All` in the registration as `02:703` has it"; 02:1124 "Nothing leaves the scope list").
- Word and PDF carry the new text. Space-blind counts of the feature name: 02 md/docx/pdf 37/37/37 (before-copies 16/16), 03 25/25/25 (before 8/8); "B2037" 15/15/15 and 11/11/11 (before 0). Eleven changed sentences sampled per document: all present in the .docx and in the .pdf, absent from the old .docx; a control sentence absent from all. One 02 sample (F37 row, line 98) did not match in the PDF as one string only because the table's next column is interleaved in the extracted text; its fragments are on PDF text lines 855-857.

## Major

**M1. OP-20 is closed on a premise nobody checked: that only Shared with me reaches other users' drives.** 02:231 ("the rebuild makes none of these calls ... OP-20 is closed by C-82 ... nothing to test"), 02:743 (same, in the scope row), 03:268 ("this test is not run"), 03:312 ("the item calls on other users' drives served Shared with me only"; "closed by C-82, not run"), 03:539 ("CLOSED by C-82"), 02:1372, 03:851, 03:853.
The Recent place is kept, and it is not confined to the user's own drive:
- The app's Recent call is `GET /me/drive/recent` with a select that asks for `remoteItem` (A11:210, A11:226).
- Microsoft's page for that call (read today, learn.microsoft.com/en-us/graph/api/drive-recent) says: "This collection includes items that are in the user's drive and items they have access to from other drives", and that such an item is fetched by `GET /drives/{remoteItem-driveId}/items/{remoteItem-id}`.
- Neither reader traced how the app opens a Recent item that lives on another drive (A11 and B1769 hold no line on it; `remoteItem` occurs once in A11, at :210, and 0 times in B1769, 02 and 03).
So the download, convert and permission calls may still land on another user's drive from Recent, and the scope question OP-20 asked may still be live for that path. "Closed by C-82" also puts under his ruling something he did not rule: C-82 drops the feature; the closing of the tenant test is the lane's inference (directed by the commission's own example). Correction: narrow OP-20 to "Recent items on other drives: not traced; test stays until read" instead of closing it, and drop "served Shared with me only" and "nothing to test".

**M2. WP3.10's test column still tests the Shared-with-me calls.** 03:312, tests cell, unchanged: "Graph tests against the 22 live Graph calls of A11 §5 and the thumbnail fetch (23 live calls: `[B1769 §3]`)". The 22 include C10 (`/me/drive/sharedWithMe`), C12 (`POST /search/query`) and C13 (the re-read of each hit), which A11:251 names as the Shared-with-me calls. The same cell's OP-20 clause was edited; this count was not. As written the package is tested against three calls it does not build. (02:231 item 1 and 02:743 use the same 22 and 23, but there they describe the source, which is right.)

**M3. Outside the lane's remit, raised by its own reason: Recent rests on a call Microsoft deprecated in the same notice.** Both documents now say the rebuild builds Recent (02:3, 98, 212, 371, 543; 03:3, 229, 312 `/me/drive/recent`) and give "Microsoft has deprecated the Graph API code" as why Shared with me goes. Microsoft's pages carry the same caution on both calls (read today): "The **recent** API is deprecated and will operate in a degraded state until November, 2026, after which it stops returning data" and the same sentence for **sharedWithMe**. C-82 rules Shared with me only, and "match the shipped 4.4 app" keeps Recent if the shipped app has it, so this is not a lane error. It is a new question for the product owner or the Workpath team (is Recent still working in the shipped app; what replaces the call), and neither document carries it.

## Minor

- **m1. 02:1279** (N-10 row): "HP's 4.4 release notes and OneDrive user guide p26 say it was removed". Only the release notes say removed. The guide's page 26 is a limitation ("Unable to display ...") with resolution "TBA". Overstates the second source.
- **m2. 02:212**: "the shipped app does not" is written as fact. It is HP's documents' statement, not seen on a device (C-82 itself calls it "the card's reading of HP's documents"; the guides map warns "statements, not measurements"), and the source read is 4.4.1, later than the 4.4 notes, with the place live. 02:98 and 02:543 ("HP removed it from the shipped 4.4 app") lean on the same. Say "by HP's documents".
- **m3. 03:233** (E3.1, unchanged): every row F97 to F99 must have a passing test, and class (1) of the deviation register lists rulings by C-number. F99 and F37 are now half-built by C-82; E3.1 neither names C-82 nor says the unbuilt half needs no test (as it does for F89 under C-38).
- **m4. 02:1260, 1261, 1262** (B1817 rows R4-32 to R4-34): still "N-10; default as R4-31" with no closing note; only R4-31 (1259) and the N-10 row (1279) carry one. The chain resolves at 1259, but 02:1372 says N-10's rows were marked, and three were not.
- **m5. 02:212, 02:1368, 03:849**: the article title is quoted as "What's new"; `MAP.md` 66-68 gives no title (only the address ending `what-s-new-`), and `MAP.md`:98 writes "What's New". A quoted title with no source for its spelling.

## Info

- i1. "HP's OneDrive user guide": C-82 calls these "Datasec's own customer guides". The commission asked for "HP's documents", so the lane followed its brief; the ownership word is Tuesday's to settle.
- i2. `05_readiness-to-build.md` lines 22, 185, 261 (and its PDF) still say the rebuild carries all four places and hold OP-20 open. Outside B2037's two documents; now inconsistent with them.
- i3. The pre-B1773 state of the scope row could not be read directly (the project folder is not a git repository and both before-copies postdate B1773); the permissions finding rests on A11:412 and 02:1124.
- i4. Occurrence counts differ from the commission's 11 and 3 because those counted the spaced spelling only; with hyphen and camel-case the before-counts are 16 and 8, as the lane's `verify_installed.txt` prints. No occurrence was missed: every remaining one in the body sits in a not-built sentence, and the unmarked ones (02:1117, 1118, 1124, 1261, 1262; 03:711) are older change-log records.
- i5. Not checked: the kick-off meeting pack's W30 wording; whether the before-copies equal the files as they stood at 12:36 (taken on the lane's `cmp`); every changed line of the .docx and .pdf beyond the eleven samples per document (totals agree).

## Method

Line and word diffs by `difflib` (python3 -I) of each .md against its `.pre-1124b.md`; searches for `shared[ _-]*with[ _-]*me`, `sharedWithMe`, `search/query`, `four places|all four|fourth`, OP-20, N-10, W30, T-14, F37, F99, WP3.10, E3.1, each with `onedrive` as the positive control (135 and 80 occurrences); quotes by exact substring count in document and source; .docx text from `word/document.xml`, .pdf text by `pdftotext -raw` and `-layout`, compared with whitespace and typographic quotes normalised. Two public Microsoft pages were read for M1 and M3; nothing was sent anywhere. Nothing written outside this folder.
