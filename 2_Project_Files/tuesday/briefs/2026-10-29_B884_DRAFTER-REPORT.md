STARTABLE: YES (after your stamp: twelve slots, four of them decisions: BUILD-SKIPS, G3-SLOT, G7-SLOT, HELD-RULING; each names its default)

# B884 drafter report (kit: `2026-10-29_B884_SEAT-R82_hpsmpoc-records-v12-design-tickets.md`, 387 lines, copy of the unstamped kit at `.md.pre-stamp`)

## BLUF
Kit written for Datasec/HPSM-POC-R82, Sonnet, records, in the shape of B880 and B871. The seat creates 30 Jira Tasks (23 BUILD T01 to T23, then 7 GATHER G1 to G7), writes C-224 (the v1.2 design round, superseding the 2026-10-06 burger-menu instruction), files the two supplied documents locally, adds 6 BACKLOG rows and one history entry, and lands its own records branch `records/b884`. Next C-number: **C-224** (records main `744f82ab`, highest heading C-223; the drafter counted main only, the seat scans every ref). Next Jira key: HPSMPOC-368 (newest now HPSMPOC-367).

## Counts
- Jira: 30 creates (23 build + 7 gather), up to 7 label adds (`gather`), up to 2 optional comments (C165, C21), 0 transitions, 0 edits, 0 links. Dependencies are "Depends" lines carrying keys that already exist at create time (every dependency is an earlier ticket), so no link or edit is needed.
- Records: 1 C-entry, 6 BACKLOG rows (B884-1 to B884-5, B884-C1), 1 history entry, 1 catch-up copy (B880 STATUS, 99 lines, sha256 `a2211cea...f953`, `HP Restricted` on 7 lines, all check names, to be re-read by the seat).
- Kit: 13 four-underscore lines (12 slots + the last line); control on the `.pre-stamp` copy prints 13. 180 Jira text parts, 49 record text parts.

## Duplicates and related tickets (Jira GET, about 45 searches; controls fired)
- **No live ticket covers any BUILD item.** `sidebar` 0, `burger` 0, `hamburger` 0, `left rail` 0, `breadcrumb` 0, `Framework alignment` 0.
- Related, named in the texts: HPSMPOC-183 (Done, empty menu entries hidden; T02 keeps it), HPSMPOC-142 and -93 (Done, print rules; T01), HPSMPOC-190 (Done, feedback pill; T01), HPSMPOC-310 (Backlog, Home versus Dashboard wording; T02, T06), HPSMPOC-24 (Backlog, Entra roles build; G1), HPSMPOC-259 (G1).
- **Partial coverage, so slots:** HPSMPOC-165 (Backlog, `needs-kam`, good/better/best services content, no prices) overlaps G3; HPSMPOC-21 (Backlog, branding source) overlaps the branding part of G7. G3-SLOT and G7-SLOT offer CREATE (default) or COMMENT-ON-HPSMPOC-165 / COMMENT-ON-HPSMPOC-21 (fixed comments C165, C21 are in the kit). HPSMPOC-20 (prototype review and approval) is the milestone this round answers; not touched.

## Spot-check of the delta's file paths (code main `c00e2828`, tree of 1602 entries; control path counts 0)
- 14 of 14 sampled paths exist. Bulk check of every path in the delta's section 4: 101 found, 7 not found; 5 of the 7 are files the delta calls NEW.
- **Two delta errors, corrected in the tickets:** `customer/ApiProfile.tsx` does not exist (the component is exported from `customer/ApiSteps.tsx:38`); `FindingOverride.tsx` does not exist (tree has `useApiOverride.ts`, `lib/override.ts`, `FindingOverride.test.tsx`).
- The delta's "CLARIFICATIONS ends at C-30" is stale (ends at C-223). The B169 burger instruction is verbatim in the records brief `Briefs/2026-10-06_B169_burger-menu-and-feedback-attachments.md` line 3, not in a C-entry; `CLARIFICATIONS.md:749` mentions PR #115 "B169 burger menu". The burger code is live at `AppShell.tsx` lines 132-141 (read).

## Filing of the documents (the project's convention)
Customer-supplied documents go to `1_Project_Definition/Source_Documents/<date>_<topic>/` with a `SHA256SUMS` file (e.g. `2026-10-11_hp-feedback-steve-inch/`). That folder is in `.gitignore` (line 11, `git check-ignore -v` rc 0, control rc 1), so it is **not versioned and nothing is committed**; the C-entry records names, sizes and sha256. `HP Reporting and Docs/` (Datasec's own reports) and `2_Project_Files/HP Docs/` (tax and contract PDFs) are not the review-feedback folder. sha256 of both files re-measured: equal to your figures. The reference folder holds exactly the two files; the video is never touched.

## Banned-term scan (program over every fixed part)
Classes: day words, banned words (with `\bphase` as a prefix), backtick, non-ASCII, e-mail, B-number (also case-insensitive), seat/`Datasec/`/R82, lower-case card-id shape, person names (including Pete, Peter, Steve, Paul, Terry), `\bHP\b`, FOR-heading quote. Jira parts: **0 hits in all 11 classes**, every class's plant fires. Two fixes made on the way: the word "next-phase" (G1) and a file name carrying a brief number (`playbook-b17-clicks.spec.ts`, T23; the text now says "its file name carries a brief number"). Longest summary 176 characters (limit 255). Record parts (C-entry, rows, history): backtick, B-number, seat and `Datasec/` strings occur by design (records form); person names 2 and `HP` 1, all inside the product owner's verbatim quotation (CE-2); non-ASCII: 2 lines, the em dash in the C-entry and history headings (the form of C-223).

## Q-questions for Tuesday at the stamp (each with a default)
- **Q-1: the word "phase" is banned, but the design's menu label is "Delivery phases".** I kept the ban (strict prefix) and wrote "the Service offers entry, relabelled as the design shows", so the exact label is in no Jira text. Default: keep. If the ban is only about the project-scope sentence, say so and the label can be written in T02/T17.
- **Q-2: G3-SLOT and G7-SLOT** (create the wider gather ticket, default, or comment on HPSMPOC-165 / -21 instead).
- **Q-3: BUILD-SKIPS.** Default NONE (no live duplicate of any build item).
- **Q-4: HELD-RULING.** The commission's card names "three held pieces" but I do not know them. The entry guesses the delta's three hold-outs (the packages page, the Framework alignment table, the Training principles list) and says the coordinator confirms; fill the slot with the ruling text or NOT YET RULED.
- **Q-5: the C-entry quotes the commission verbatim, which contains two first names (Peter, Pete) and "HP".** Default: keep, as commissioned. The Jira texts contain none.
- **Q-6: filing is local only** (folder ignored) although the commission said commit if versioned. Default: as written, no commit.
- **Q-7: transcript.** The commission mentions "a video and transcript"; the reference folder holds the HTML and one AI-generated DOCX summary only. The kit says the transcript is not among the two files supplied. Confirm no third file is coming.
- Minor: launch window and hard stop longer than B880 (target 150 minutes, hard stop 240) because of 30 read-back creates; labels `design-v12` (all) and `gather` (G only), no B-number in any label.

## UNMEASURED
Every "restyle only" verdict and CSS/contrast figure of the delta (not re-run; no browser opened); whether the API refuses Service offers for Consultant and Demo (T02 requires the check); whether a merge to code main triggers a deploy; every records ref for a taken C-224 (only main counted); the DOCX contents (not opened; only its file name and sha256); the project's total issue count; drift of records, code or Jira after about 10:35; whether the repository allows the seat's own records PR (B871 and B880 did).

## Outside-the-fences disclosure
Read-only throughout (Jira GET, `gh api` GET, file reads). I wrote only the kit, its `.pre-stamp` copy and this report. Scratch files are in the session scratchpad. No git command was run inside `!CODING` beyond `git check-ignore` and `rev-parse` reads (no fetch). Three hook events: a `cd` refusal and an unquoted `=====` refusal (both re-issued), and case-sensitive-grep advisories on index greps that did not decide any count.
