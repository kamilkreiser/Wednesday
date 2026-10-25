# B569 drafter report (SEAT-M10, MPS #105 "All device classes", Sonnet builder, row C2/L6, tier-2 delta gate after)

Drafted 2026-10-24 about 08:50-09:05 AEDT, read-only, Sonnet. Brief: `2026-10-24_B569_SEAT-M10_mps-105-all-device-classes.md` (58 long lines, non-ASCII bytes 0 by `python3 -I`, `@[A-Z_]+@` tokens 0). `.pre-stamp` copy written beside it (`cmp` same).

## Stamp-slot count
The `.pre-stamp` copy reads **8** lines with `/usr/bin/grep -c -E '_''_''_''_'` (seven slot lines, 49-55, and the last line 58 `READ-WHOLE-BY-TUESDAY: ____`); the brief's "The unstamped copy reads" says 8. The REFUSE line itself does not match (quotes split the pattern). Tuesday fills 7 slots plus the last line.

## Reads
- Card: `decision_queue.sh show mpscalc-pr105-device-class-cell-words-1024` (the one show): ruling `choice='b'`, ruled_ts 08:53:16 AEDT; option b detail quoted in the brief.
- `git ls-remote origin` in the MPS clone: branch and `refs/pull/105/head` = `4db8661dad27fd2e8d79e0731d998dd1c0f03362`; `refs/pull/105/merge` = `28899d9e...`.
- At the head via `git --no-optional-locks show "${H}:path"` (first try with `$H:web` was mangled by zsh; the brief says braces): `sections.ts:376-392` (constant at :385, doc comment :380-384 says UNAPPROVED), `OnePager.tsx:88-100`, `ProposalDocument.tsx:24-60`, `dealPair.test.tsx` whole (all six uses of the cell read `T.DEAL_WIDE_CLASS_CELL`: :47,48,59,60,72,73). B561 STATUS lines 100-130 (A1-A3).
- `git grep -i "all device classes"` at the head: only the `sections.ts:383` comment.
- Ports: `lsof -nP -iTCP:9180-9189` empty; `grep` of 23/24 Oct briefs for `918x` printed no file. Panes 08:5x: tuesday, Datasec/HPSM-POC-H9, Datasec/MPS-G73 (LIVE), Datasec/MPS-G72, fleet-monitor. Templates: B565 and B566 briefs (REFUSE, HOLDS, Stamp shape), B565 and B560 ADDENDUM-1 for the release-by-MOVE wording.

## Decisions (Tuesday strikes any at the stamp)
1. **A rendered-text row IS needed.** Every existing row reads the constant, so none can go red if the word regresses; the brief adds ONE `it` to `dealPair.test.tsx` with the literal `'All device classes'` typed in the test, covering the one-pager and the usage table, the unchanged summary labels (A2), and a section-rate fixture that must not print it. Red at `4db8661d` (literal vs empty string), green after.
2. **A2 unaffected, by reading:** `rateSummaryLabel` (`ProposalDocument.tsx:39`) tests `deviceClass` null/undefined and returns the bare component label without calling `classLabel`. The brief makes the seat re-prove it.
3. Yours = `sections.ts` plus `dealPair.test.tsx` (the one named test file). The constant's doc comment (UNAPPROVED) must be reworded, same file.
4. Mutants M1 constant `''`, M2 a different word, optional M3 hard-coded empty at `OnePager.tsx:96` (worktree only).
5. Timing is the first REFUSE bullet: no start while pane `Datasec/MPS-G73` is live or until `B566_STATUS.md` ends in a `VERDICT:` line. B566 is live now (MEASURED 08:5x); its STATUS not read.
6. Push is a plain fast-forward of the existing branch, which updates PR #105; counts expected web 134 files / 1,272 -> 1,273 tests (B561 STATUS RELAYED baseline; the seat measures its own).

## Not measured
Whether the 18-character cell fits the printed one-pager and full-proposal column (CSS untouched, outside Yours; listed under NOT TESTED in the brief: a possible layout wrap or page overflow is for Tuesday to weigh at the gate). Whether any doc outside `web/` calls the cell "empty" (one grep, 0 hits). The B566 STATUS contents, `models_latest.json` model id, gh auth, any build, test, lint or tsc run, the branch-moved state after 08:57. No file other than the three named was written.
