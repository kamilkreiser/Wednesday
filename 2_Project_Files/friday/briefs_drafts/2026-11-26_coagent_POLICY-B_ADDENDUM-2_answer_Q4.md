This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-26_coagent_POLICY-B_brief.md`. Seat POLICY-B only. Report under "## ADDENDUM 2 (answer Q4)" in your STATUS file.

If your context was compacted while you waited: re-read your brief, addenda 1 and 2 and your STATUS file WHOLE before doing anything.

# POLICY-B ADDENDUM 2: answer to Q4. A two-scan shape to MEASURE FIRST; no engine edit until its figures are in STATUS

Friday read your ADDENDUM 1 section whole (lines 123 to 176). Q3's commit `e11b31a` stands. Your stop was right again: the guard of addendum 1 (point 2) was a figure derived from the base's worst case, and your corpus showed an ordinary text over it. Your figures are quoted below as yours; Friday re-ran none.

## 1. What is withdrawn, by name
- **Addendum 1, point 2's guard as a rule for the base scan with its cut lifted** ("at most 1 024 pieces AND total characters at most the base's measured maximum"): withdrawn. Lifting the 161-piece cut of the existing scan is NOT the shape any more.
- **Addendum 1, point 5 (i)** (each ordinary text under 50 ms per `decide`): withdrawn as written; replaced in section 3 below.
- Everything else of addendum 1 stands (nothing cut silently; a text over a guard is denied as too large; the records of point 6; the differential's added form; P-5; E-2 and E-3 in this lane).

## 2. The shape to measure (the coordinator's proposal: UNMEASURED; your figures decide whether it is built)
Your mechanism (READ by you): in the canonical JSON a line break is `\n`; the scan drops the `\`; the lines glue into one long word; a field whose first character is `-` becomes one option word and yields a piece at every `/` and `~`. So the existing scan reads free text as one shell word, which is the root of both the late-name miss, the names missed after an escape (your six rows), and the piece counts.
- **Scan A = the existing scan, exactly as at the base, with its 161-piece cut.** Nothing of it changes. So for every free text the base's pieces ARE the head's first pieces (the brief's prefix invariant holds by construction), and its cost is the base's.
- **Scan B = a second scan that reads the text as a person sees it:** the same 1 200-character window with every JSON escape sequence turned into a blank (the copy E-3 describes), split at blanks into words FIRST, each word then given to the scan's rules on its own, so that a field's whole value is never one word and never one option word. No 161-piece cut in B. B's pieces are appended after A's. The exact form is yours to choose within that description (your shape (b) is close to it); say in STATUS exactly what B does to quotes, to a leading `-`, to `@`, and to brace groups, and why.
- **The guard is on B alone,** in a measure that follows the time (your shape (c): for example pieces times path components; choose it from your figures and say why), plus the 1 024-piece count. A window over B's guard is denied as too large (`L L L L`), never cut.
- The late-name check (the owner's ruling C-22), the web fetch prompt (C-21, scanned by B alone, since the base does not scan it) and the names after an escape (E-3) are then all delivered by B. E-3 is no longer a separate scan: its red row and its property stay, pinned on B.

## 3. Measure first, in scratch, with no engine edit (as you did for points 2 and 3)
Build B in a scratch tree only. For your whole corpus (every row of your A1.3 table, the four bullet lists and both controls included), your P-0 (4) families, your six escape rows and the `t28` counting rows:
1. B's pieces, B's work in your chosen measure, the time of one `decide` and of the four columns with A + B together, beside the base's.
2. Whether a name placed LATE in the visible part (ending before character 1 000) is found (`X X X X`) in every corpus text and every ordinary family, and whether each of your six escape rows becomes `X X X X`.
3. The largest B work an ordinary corpus text gives, and the smallest B work at which the slowest shape you can build passes your proposed time limit: the guard must sit between the two with room on both sides. Say the room.
4. The worst admitted window, A + B, over the four columns.
**The limits (UNMEASURED proposals of the coordinator; if your figures miss one, do not bend it: `STOP Q<n>` with the figures and the limit you would set):** (i) every ordinary corpus text is under B's guard with at least twice its work to spare; (ii) every ordinary corpus text's one `decide` with A + B is under 60 ms, or under 1.5 times its base time, whichever is larger; (iii) no admitted window takes more than 400 ms over the four columns; (iv) a window B's guard denies is denied in under the same 400 ms.
**If all four hold: build it** (E-1 = A + B with the guard; E-2 through B; E-3 pinned on B), then the brief's sections 6 and 7 with addendum 1's changes. Before the engine edit write the measured figures and the exact guard in STATUS, with `IN PROGRESS` as the last line; no further word from the coordinator is needed to start.
**If any fails, or B misses a name that scan A finds, or you see that B cannot be made sound: `STOP Q<n>`** with the figures and the shape you would recommend. A lane that ends with Part W, the measurements and a design question is a good outcome; an engine change built on a figure nobody measured is not.

## 4. One more record (outside the engine work; in your next BACKLOG commit, one added line)
The owner ruled on the old remote branch `measure-2` (the coordinator's card, answered b: it stays). Add ONE open BACKLOG entry for the sweep that must happen before the repository is ever made public: that sweep must cover every branch and all history, and is told of the remote branch `measure-2` (one saved log file on it holds a folder path of the build machine) and of the 90 files of earlier test pieces on main in which the second check of the host-facts measurement counted the same two folder names as path parts (`gate_MEASURE_2_r2_verdict.md`, its Note N-10, in Friday's `m1_review` folder: READ it and cite the count from it; write no folder name, no path of the real drive and no card id into the entry). Wording: "the owner's ruling", "the coordinator's card", no seat's name.

No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.
