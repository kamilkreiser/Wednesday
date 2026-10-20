# B378 DRAFTER REPORT (Sonnet drafter, row C8) for brief `2026-10-21_B378_SEAT-R16_hpsmpoc-records-pr166-pr167.md`

Drafted 2026-10-21 ~07:2x AEDT (`date` printed 07:27:51 AEDT). Marks: MEASURED = I ran it and saw the output; RELAYED = read from a file at path:line; UNMEASURED = nobody ran it. Fences kept: two files written; `gh api` GET only under the project's `GH_CONFIG_DIR`; `git --no-optional-locks ls-remote` only; no Jira call at all (no `.env` read), no az, no HTTP to any app host, no mail/Artifact/Docs. Not opened: `HP Reporting and Docs/`, `HP Docs/`, `.local/`, `Source_Documents/`, `.env`, any `.tools/b*` file (I listed `.tools/` names only).

## 1. What I read (whole)
B370 brief (108 lines) and B370 STATUS (96); B367 (288), B364 (125), B369 (110), B371 (199), B372 (101), B375 (203) STATUS files. Records `CLARIFICATIONS.md` on main by `gh api` (2,009 lines): C-125 `:1920-1923`, C-127 `:1960-1987`, the C-128 numbering `:2005-2009` and its heading list; `history.md:1-14`. The register line `clarifications_register.md:26` via grep (that one line only). Not read whole: C-120, C-122, C-124 (read the shape through C-127's precedent line), the B357 STATUS, the B363 brief/STATUS and the B370 drafter report beyond its first 70 lines.

## 2. Facts (each with where)
- **PR #166:** `merged=true`, merge commit `fa8416de1237f587a77d0cd6f538d1937c1b1de7`, `merged_at` 2026-10-20T20:01:00Z = 07:01:00 AEDT (MEASURED `gh api pulls/166`, `date -j`), tree `fcc1d3bfbd32cdd9ff5da75ab69463422cae77c2`, parent `6818896b…`, subject "HPSMPOC-294 + HPSMPOC-295: feedback utf-7 and Pkcs pin test gaps (gates B367, B371) (#166)", 2 files, +194 −17 (MEASURED `commits/<sha>`; equals B371's +32/-9 and +162/-8 `:32`). PR head `777f29c3…`, 3 commits.
- **PR #167:** merge commit `54fbceac12393f503fae8c5810af9609bac44548`, 07:24:51 AEDT, tree `01b2ca9f17ad4ead8d456af775f00d21a30a1c3d`, parent `fa8416de`, 1 file `ImportFailGuardTests.cs`, +93 −1 (equals B375 `:53`). Head `91cbbcb1…`. Code main = `54fbceac` (MEASURED `ls-remote` and `commits/main`).
- **Records main** `6a368d9e0d7ca92346af9b0876279b00f2d756b1` (MEASURED), 2,009 lines, highest heading C-128 `:1988`; headings C-120..C-128 listed (MEASURED). Records refs `records/b3*`: b315, b346, b363, b370 (b370 merged but its ref remains); no `records/b378`. Mention hits for `C-(129|13[0-2])` on main: exactly 3 lines `:1907`, `:1984`, `:2007` (MEASURED `grep -n`). Next free numbers on main-only: C-129, C-130.
- **Hosted site:** newest `DEPLOYED:`/`ROLLED BACK` STATUS is still B366 (MEASURED `grep -l` + `ls -lt`; B264, B273, B316, B366 listed); nothing newer by mtime. Hosted still `6818896b` per C-128 (RELAYED, no HTTP). CI after merge: on `fa8416de` `Push on main` 39488365467 and `ci` 39488366465 `completed`/`success`; on `54fbceac` `Push on main` 39491761275 and `ci` 39491761682 `in_progress` (MEASURED 07:2x; the seat re-reads).
- **Gate numbers** are quoted from B371 `:1`, `:88`, `:121`, B375 `:1`, `:173-174` and B367 `:1` (RELAYED, not re-measured). The three Jira bodies equal the gates' drafted lines (B371 `:159`, `:160`; B375 `:174`) modulo the edits the brief names (MEASURED by a program: all three equal after removing the edits; -295 has three edits, brief says so).
- **Convention for quoting the owner:** verbatim as a `> ` block, attribution in prose (C-125 `:1913-1915`, `:1920-1921`; MEASURED by reading). The register's line has no first name inside the quote (MEASURED by reading). Base file has the first name 372 lines by `grep -c -i` (B370 STATUS says 437 occurrences; different unit, both are "present in base").
- **Register's own timing:** "~07:2x AEDT"; the brief gives no finer time.

## 3. Choices I made that you may want changed
- **Two C-entries** (C-129 the landings, C-130 the owner's instruction), consecutive; the instruction entry is a separate C-number as you asked.
- **0 transitions**, status unchanged on -294, -295, -305, with a status sentence in each comment (the default you gave). That sentence states "the hosted site runs 6818896", which is why the REFUSE check on a newer deploy is a STOP, not a note.
- **Comment bodies are the gates' drafted lines with "(not merged)" replaced** (ruling R-R14-1 (b) precedent), plus a status sentence; -295 additionally carries the correction to 39845 folded into the one comment (one comment per ticket kept), replacing the gate's pointer clause. The correction's figures "20 -> 25, 1511 -> 1516, 4 rows, 13, 3 of 3" are derived from B364 `:27`, B369 `:8`, B371 `:88`, `:83`, `:160`: the 20 and the 1511 are RELAYED builder/gate baselines.
- **One ticket for B371-1** (summary and description drafted in the brief, plain text), labels `b371-gate b378-2026-10-21 test` modelled on HPSMPOC-305's labels (RELAYED from B375 `:153`); field shape is copied by the seat from a GET of HPSMPOC-305. Notes only in the C-entry.
- **14 catch-up files:** B364, B367, B369, B371, B372, B375 briefs + STATUS, plus this brief and STATUS. B370's brief had left B364/B367/B369 to "PR #166's records seat"; I read that as this seat. Evidence folders excluded (B250).
- **Three history entries** (this seat, #167, #166).
- **create.py:** B370 did not copy it; I told the seat to take it from `.tools/b363/` and STOP if absent (UNMEASURED whether it exists; `.tools/` listing shows b363 only as a dir).
- `@` appears in the bodies only as "@ 777f29c" etc. (a space follows), so the "e-mail 0" check must be an address regex, not "no at-sign". Said nothing in the brief; the seat's usual e-mail regex handles it.

## 4. UNMEASURED, with the instrument that would close each
| Item | Instrument |
|---|---|
| Current Jira status/comments of -294, -295, -305 (pre-reads are the gates' 06:45-06:57 reads) | seat's GETs |
| Whether a ticket for B371-1 already exists | seat's four JQL searches |
| Label spellings and field shape for the create | GET of HPSMPOC-305 and the project's label set |
| Whether `create.py` exists in `.tools/b363/` | seat's `ls` |
| Whether squash commit trees equal the gated heads' trees | seat's `git/commits` GETs (I did not compare) |
| CI result on `54fbceac` | seat re-read to a terminal state |
| Any C-129+ heading on other refs | seat's C-SCAN |
| The register's exact bytes (two spaces after "POC.") | seat's byte-equal assert; I read the line through a `cut -c1-3500` of grep output |
| Whether the 3 comments' text is true at stamp time if another deploy lands | the newer-deploy REFUSE check |

## 5. Questions for Tuesday (recommended answer first)
1. **Do test-only tickets go to Done on merge + gate?** Recommend **no, not on their own**: leave Backlog with the comment, per R-R10-1 (Done = merged + gated + deployed). Alternative: rule a test-only exception to R-R10-1 and a later step moves -294, -295, -305 (each transition id read from `GET …/transitions`).
2. **-295's comment carries the 39845 correction folded in (three edits to the gate line). Approve, or a separate second comment?** Recommend folded (one comment per ticket; the gate's records Note asks for it).
3. **File B371-1 as a ticket, or carry it as a Note?** The gate calls it optional ("your ruling"); you asked to file. Recommend file (done in the brief), since it is a real survivor and cheap.
4. **Quote the owner verbatim in C-130 with two spaces after "POC."?** Recommend yes (the convention in C-125; the quote carries no first name).
5. **Do the six builder and gate files for #166/#167 all go in as catch-up copies (12), including the round-1 NO GO B367?** Recommend yes (the history of the NO GO is the evidence for B371's closure table).
6. **NEXT_C stamp default:** `C-129` (main-only measurement; the seat re-derives; takes C-129 and C-130). **MODEL_LINE default:** `Sonnet (BRIEF_SEAT_LEVEL=sonnet; rows C7/C8); STATUS quotes the brief_seat: model= line or says it was not visible`. **STAMP_TIME, B_NUMBER_CONFIRM (B378 free: no B378 file in `briefs/`, MEASURED), CODE_MAIN_PIN (`54fbceac12393f503fae8c5810af9609bac44548`, ls-remote 07:2x), RECORDS_BASE_PIN (`6a368d9e0d7ca92346af9b0876279b00f2d756b1`)** are yours to re-read at stamp.
7. **If another HPSM-POC records seat (or the PR #127-style land of this branch) races you:** launch B378 first and land its PR before the next records brief, so the next C-SCAN sees `records/b378`.

## 6. Slots and self-check
`/usr/bin/grep -c -E '@SLOT:[A-Z0-9_]+''@'` on the brief prints 1 (one Stamp line holding six tokens; MEASURED by a program: 6 tokens, 1 line). No `.pre-stamp` created (two-file fence): Tuesday copies it before stamping. The last line of the brief is `READ-WHOLE-BY-TUESDAY: PENDING` for Tuesday to replace. The brief names no person in any Jira body or history line (MEASURED on the three bodies: no backtick, no "Kam", no "Tuesday", single line); the one verbatim owner quote is in the C-130 block, as the convention requires.
