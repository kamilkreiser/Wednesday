REVIEW B2038-R2: GO WITH FINDINGS

Fable reviewer, read-only, 2026-11-24, delta review after lane D's rounds 1 to 4. Subject: the current `02_architecture.md`, `03_plan-of-attack-and-build.md` and `05_readiness-to-build.md` in `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Design/` (stamped 13:01, 13:01, 12:58), against their `.pre-1124b` before-copies and against `REVIEW.md` beside this file.

Counts: Blocker 0, Major 1, Minor 3, Info 5. All eleven findings of round 1 that asked for a change are closed.

## 1. The round-1 findings

| Finding | State | Where |
|---|---|---|
| M1, OP-20 closed on an unchecked premise | CLOSED: narrowed, not closed; what is left (items that point to another drive from My Drive or a library, `remoteItem`, not traced) is said and marked as general knowledge | 02:231, 02:743; 03:268, 03:312, 03:539; 05:185, 05:261 |
| M2, WP3.10 tests the dropped calls | CLOSED: "18 live calls, 19 with the thumbnail fetch", C9, C10, C12 and C13 removed (22 less 4 is 18; agrees with A11 §5) | 03:312 |
| M3, Recent rests on a deprecated call | CLOSED by the product owner's ruling of 12:54 (round 2) | 02:3, 98, 212, 371, 543; 03:3, 229, 312; 05:22 |
| m1, the guide "say it was removed" | CLOSED | 02:1279 |
| m2, "the shipped app does not" as fact | CLOSED ("say it does not (no device seen)"; "by HP's documents") | 02:212, 98, 543 |
| m3, E3.1 does not name C-82 | CLOSED | 03:233 |
| m4, R4-32 to R4-34 without a closing note | CLOSED | 02:1260 to 1262 |
| m5, article title quoted with no source | CLOSED (unquoted, "What's New" as `MAP.md`:98) | 02:212, 02:1368; 03:849 |
| i2, 05 still said four places and OP-20 open | CLOSED | 05:22, 185, 261, 306, 308 |

The diff still touches only named lines. 02: 3, 98, 170, 171, 212, 216, 226, 231, 371, 543, 743, 1259 to 1262, 1279 and one appended entry (1368 to 1386). 03: 3, 105, 229, 233, 268, 307, 312, 539, 544 and one appended entry (849 to 868). 05: 22, 185, 261 and two appended paragraphs (306 to 309). No line was added or removed before the appended entries.

## 2. Major

**R2-M1. 03:544 still says three places are built.** "the four places are ruled by C-16 (`[ARCH §3.9]`; B2037: Shared with me since dropped by C-82, three are built)". Round 2 did not reach this line: it is the one place in the three documents that still has the rebuild building Recent with no round-2 note beside it. Every other "three" carries "(round 2: two)" or is followed by the ruling (02:3, 02:1370; 03:3, 03:851, 03:852). Correction: "two are built since the Recent ruling".

## 3. Minor

- **R2-m1. 02:170 and 03:307 (F81 in line): "this follows from the product owner's ruling ... as the coordinator applied it".** The change logs say it plainly and correctly ("the coordinator's decision, not the product owner's", 02:1379, 03:863), and "the product owner may reverse it" is there. But the in-line sentence opens with "follows from" his ruling, whose card names OneDrive's Recent view only. A reader of the row alone takes it as nearer his word than it is. Use the change log's wording in the row.
- **R2-m2. 03:233 (E3.1): F81 and F82's Recent entry point have no place in the deviation rule.** F37's two places are put in class (1), ruled. F81 is named with no class, and F82's entry point (round 4) is not named at all. By E3.1's own sentence, a design choice "neither ruled nor forced" needs the product owner's approval before phase 3 exits (OQ-6) and has a list ("today: F18 and F43/D19 ..."); neither item was added to it.
- **R2-m3. "C-entry to follow" has no entry yet.** The 12:54 ruling is cited that way at every round-2 place in the three documents, and `CLARIFICATIONS.md` holds no record of it ("Drop Recent too": 0 occurrences; control "Drop it": 2). The option, its detail and his note match the coordinator's message to me word for word; the card's title I could not check against any record. Until the entry exists and its number replaces the placeholder, the documents quote a ruling the project has not recorded.

## 4. Overstatement in rounds 2 to 4

None beyond R2-m1.
- His note "rebuild without graph" is quoted verbatim, marked as being clarified with both readings named, the default marked as the coordinator's, and followed by "nothing else in this document is changed on account of it, and every other Graph call stays as designed" (02:1377, 03:861, 05:308). It is not used to remove anything by itself.
- Round 3 uses the note once, as "both readings of his note ... remove that call" (02:1379, 03:863). That is true of both readings, and the decision is still marked the coordinator's.
- Round 2 itself says F81 was not changed by the ruling because "the ruling names OneDrive's Recent view".
- Round 4 is marked "on the coordinator's instruction".

## 5. Remaining build, test or estimate of Recent, Shared with me, Teams Recent

Only R2-M1. Checked on every unchanged line of 02 and 03 that holds "recent" (control: 109 and 79 occurrences): what is left is the roaming-store keys (02:102), recent search terms (02:173), recent sites (02:198; 03:306) and older change-log records (02:1075, 02:1117; 03:705, 03:711). None is the recent call. WP3.5's tests cell says "(none for F81, not built)"; WP3.10 stays UNSIZED with one place added.

## 6. Word and PDF

Same text. Occurrences of "recent" (case-blind, whitespace-blind): 02 md/docx/pdf 109/109/109, 03 79/79/79, 05 md/pdf 21/21 (05 has no .docx). "B2037 round": 6/6/6, 4/4/4, 3/3. Nine round 2 to 4 sentences sampled in each of 02 and 03, five in 05: each present the same number of times in every format; a control sentence absent from all.

## 7. Other features on the two calls

None found beyond what the lane lists. Over `Analysis/*.md`: `drive/recent` in A11 (2) and A2 (1) only; `/recent` also in K2 (3, file paths of `RecentFragment.kt`); `sharedWithMe` in A11 (3) and D1 (1); `insights` in A5, A6, A9, A12 is Application Insights every time (9 hits read), not Graph insights. A8 (SharePoint) has no recent-files call; its "recent limit" is the last 3 sites, kept in the store.

## Info

- i1. K2 Table 1 row 16 (`RecentFragment.kt:289`) is one of the 16 reads of the `isSIOEnabled` switch, and F82's row already says the whole row is likely dead behind that switch. Round 4's removal is consistent with it and may be moot.
- i2. "told to him on the board" (02:1379, 03:863) was not checked by me.
- i3. 05 carries rounds 1 and 2 only. It has no line on Teams' Recent files, so rounds 3 and 4 had nothing to change there.
- i4. The full card text of the Recent ruling is repeated four times in 02 (3, 98, 212, 543), twice in 03 (229, 312) and once in 05 (22), beside the change-log copy. Correct, but when the C-number arrives there are many places to update.
- i5. My round-1 search of the briefs folder for the kick-off pack's W30 wording ran in the background for some minutes and returned nothing usable; I stopped it. The pack's W30 wording is still not checked.

## Method

As round 1: line and word diffs by `difflib` (python3 -I) of each current .md against its `.pre-1124b.md`; case-blind searches with a positive control from the same file; .docx text from `word/document.xml`, .pdf text by `pdftotext -raw`, compared with whitespace and typographic quotes normalised. Nothing written outside this folder; nothing sent anywhere.
