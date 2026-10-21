# B439 DRAFTER REPORT (Sonnet drafter, row C8) for `2026-10-22_B439_SEAT-R18_hpsmpoc-records-1022.md`

Drafted 2026-10-22 about 09:00-09:20 AEDT (`date` printed 09:17:47). Marks: MEASURED = I ran it or read it at path:line; RELAYED = from your commission; UNMEASURED = not run. Fences kept: two files written; git/`ls`/`grep`/`wc`/`shasum`/`stat` reads only; no `gh`, no Jira call, no `decision_queue.sh`, no `az`, no HTTP; no `.tools/b4*` tree opened (one `ls .tools/` listing only).

## 1. What I read
B422 brief (whole), ADDENDUM-1 and -2 (whole), B422 STATUS (whole); the project `CLAUDE.md` (grep only), root `.gitignore`, `git status`/`ls-files`/`check-ignore`; STATUS files B427 (grep), B429, B431, B432, B434, B435, B436, B437 (grep/last lines/BLUF ranges); B427 and B438 briefs (grep); the deliverables folder listing. Not read: records main, `CLARIFICATIONS.md` on origin (the root copy is stale), Jira, the board, the register (grep for the four ids by name returned 0 lines: the 07:13 rulings are not in the register file).

## 2. Findings that shaped the brief
- **Deliverables conflict (decision for you):** root `.gitignore:12` `*.docx` and `:16` `*.pdf` (MEASURED; `check-ignore` confirms the PDF). The 2026-10-08 HP-walkthrough deliverable (docx, pdf, `screens/`, `SOURCES.md`) is untracked too; `git ls-files -- 1_Project_Definition/Deliverables` printed nothing. So "commit DOCX, both PDFs" cannot be done under the project's rule without `git add -f` or a `.gitignore` edit. **Default written in Part 5:** commit `STYLE.md` and `SOURCES.md` only, binaries and `screens/` stay untracked (named with size and sha256 in the C-entries), no `-f`, no `.gitignore` edit; STOP if that reading breaks. Overrule in the Stamp if you want the binaries in the records repo (then the seat needs your explicit word for `-f`). Sizes MEASURED: docx 3,984,538 B, pdf 7,864,255, email pdf 4,159,989, STYLE.md 6,000, SOURCES.md 18,337, `screens/` 12 MB (61 raw PNGs 8.3 MB): none near a limit.
- **Landing route:** B422's template gave the seat no PR or landing step (STATUS: "Tuesday scans it, opens the PR and lands it through CodeQL"). The brief follows it: seat pushes `records/b439` and stops; the last line says Tuesday opens and lands it by merge commit after CodeQL. You wanted "seat opens the PR only if the template allowed": it did not.
- **Catch-up copies:** B427-B437 briefs, addenda and STATUS files exist in the project `Briefs/` (MEASURED `ls`) but are untracked in the root repo and (RELAYED/assumed) absent from records main; so the brief makes NO new copies and commits only files absent on records main (seat lists `Briefs/` by `gh api`), no `*_evidence` folders. B438's files excluded.
- **Root working copy is stale** (CLARIFICATIONS.md 192 lines; uncommitted edits to `BACKLOG.md` and `history.md` by other seats): the brief forbids reading or committing from it.
- **No helper dir for B439:** `.tools/b422` and `wt-b422` exist; `.tools/b439`, `wt-b439` do not (ls listing).
- Source pins MEASURED: line counts and sha256 first-12 of eight STATUS files; B437 last line verbatim; PR #179 / main `01dd9e4b4d9225999a2830343b1d4bf9f29966ac` at `B437_STATUS.md:20-21`; B436 BLUF `:5`, Majors `:9`; B436-7..-11 at `:184-188`; B435-1 at `:96-101`; B429 `:83` (cap 0.1), `:85` (signin-budget); B431 `:123` (Dependabot), `:213` (CA2254), `:235` (cap); B427 FOUND 5-7 at `:23-25` (item 5 the Demo card name, 6 Home title, 7 Feedback dialog; `:25` read in part).

## 3. Choices you may change
- Four C-entries: one per ruling (C-137 mail line, C-138 badge label, C-139 budget alert) plus C-140 the telemetry STATE; C-numbers are expectations only (C-SCAN decides; B422 landed as #130 per your note, highest C-136 UNMEASURED).
- 13 BACKLOG rows: B435-1, CA2254, signin-budget, Dependabot #1, cap 0.1, B427 5/6/7 (3 rows), B436-7..-11 (5 rows). B427 FOUND 6 relates to word pack item 4 (HPSMPOC-310); no ticket is filed.
- The board strings are quoted as you gave them and cross-checked by the seat with `decision_queue.sh show <exact id>` for the three ids plus `hpsmpoc-telemetry-round3-or-hold-1022` (no `list`). The 07:13 row has no seconds; the brief says so. C-137's outcome is "no outcome in the sources read" because I could not see what the reworded line is.
- Comment body for HPSMPOC-224 is in Part 1 (BLUF form, facts only, no name, "the product owner"). It quotes B431/B436 at BLUF level and says "a test canary string"; the B431 blocker/major counts come from its BLUF line (three Blockers, four Majors), re-asserted by the seat. Proposed to you for approval in the Stamp. No ticket, edit or transition.
- Dependabot #1 recorded read-only (B431/B436 say open; the seat reads the live alert).

## 4. Questions for you (recommended answer first)
1. Deliverables: keep the default (STYLE.md and SOURCES.md only, binaries untracked by rule)? Recommend yes; the DOCX/PDF are drafts for the product owner and HP-facing, which is why the ignore rule exists.
2. Is the HPSMPOC-224 comment wanted given the card is still open (it states the stop as a fact and rules nothing)? Recommend yes.
3. Should the seat also record the other 2026-10-22 rulings (B429 addenda, B432 Q2, B433/B434 cards) that are not in your list? I left them out as not commissioned; say if you want C-entries.

## 5. Slips (mine)
- I printed a very long `ls .tools/` listing by mistake (read-only, no tree opened). One Bash call was refused by a hook for a leading-`=` echo; reissued. Two `cd`-free reads only.
- Line counts: the brief is about 75 lines but many are long; it is under ~90 lines.
- Slots: `/usr/bin/grep -c -E '@[A-Z][A-Z0-9_]+''@'` on the brief should print 2 (the Stamp paragraph line and the final line); the final-line pattern counts per line.
