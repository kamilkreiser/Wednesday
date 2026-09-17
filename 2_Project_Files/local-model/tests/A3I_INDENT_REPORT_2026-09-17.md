# A3i INDENT SHIFT gate — report (2026-09-17)

Written by Wednesday from the builder agent's final message: the agent's own write of this file was refused by a subagent hook. The verbatim arms outputs are copied beside this file:
- `A3I_INDENT_ARMS_OUTPUT_2026-09-17.txt`: 11 passed, 0 failed, 13:22:04.
- `A3B_ARMS_AFTER_A3I_SWAP_2026-09-17.txt`: 19 passed, 0 failed, 13:26:21.

## BLUF
1. **What was installed.** `checker.sh` has gate A3i, installed 13:15:25 (sha `2f0003a87b31` → `f3ce186cf515`, backup `checker.sh.pre-0917-a3i`), plus the new helper `a3i_indent.py` (`06264a51052a`).
   - On KS-623's real `out.md` it FAILs: `:21 indent 4, brief 2 (shifted +2)`, stopping before A4.
   - The OLD checker PASSes the same output 7/7.
2. **Arms 11/11.**
   - KS-1186 (lenient apply, trailing comments) and KS-1156 (test-only) keep their recorded verdicts line for line.
   - KS-623 at the brief's indent passes 7/7 strict.
   - Legacy input shapes skip with `INFO A3i skipped`.
   - Census: 13 historical runs that PASSed A3c, with exactly 1 flip, KS-623.
3. After the swap, `a3b_line_number_arms.sh` is still 19/19.
4. **Content rule.** A3i uses A3c's rule, so a trailing comment is tolerated. The only thing A3i adds is a byte-exact check of leading whitespace. It can never accept content A3c refused, or refuse content A3c accepted.
5. **RETRY routing is NOT wired.** `night_run.sh` was not edited, so an A3i stop is currently a held FAIL. The three edits needed are below. They are OWED.

## FOUND
- **Where the indent was lost.** `build_input.sh` stores `expected_plus` stripped (`ln[1:].strip()`), and A3c compares stripped text, so no gate knew the brief's indentation. The builder also writes the whole brief into `ticket.description`, which keeps the indentation.
- **KS-623's hunk was not a uniform +2 shift.** ` */` shifted +1, the other lines +2, and there was a trailing blank context line the file lacks, which is why only `-C1` applied. In the applied file only `:21` moved (indent 4); `:20` and `:23` stay at 2. (This corrects the 13:10 IMPROVEMENTS row's "every line".)
- **A shift is not only a fuzzy-apply problem.** With correct context and only the `+` line shifted, strict apply succeeds and the line still lands shifted (arm D2). So A3i runs in every apply mode.

## Design
- **Where A3i gets the exact lines.** It re-reads the `+` lines, with their indent, from `ticket.description` using the builder's own regexes. It uses them only when, stripped, they equal `expected_plus` in order.
- **When it skips.** It prints `INFO A3i skipped` and leaves the verdict unchanged when:
  - there is no `expected_plus`;
  - there is no `## The exact change` section;
  - the description's `+` lines disagree with `expected_plus`.
- **How it measures what was applied.** It copies the tip file to a temp dir, applies the section with A2's recorded options, and runs `git diff --no-index -U0` to get the added lines. It runs before A4, so a shift costs no test run.
- **How it matches.**
  - Lines are consumed as they match, so duplicates count.
  - Exact matches are preferred; a match that differs only in leading whitespace is a SHIFT, with the applied line number.
  - If the tip already has the line, A3i does not fail.
  - Trailing whitespace is not checked.
- **What it prints.**
  - On success it prints `A3i: … OK n`, not a `PASS` line, so recorded PASS/FAIL/RESULT sets stay comparable.
  - The FAIL line avoids the `:NNN \`` shape, which the retry builder parses as missed sites.

## RETRY routing — OWED (night_run.sh edits, check the lock, `.new` + `mv`)
1. **Retry trigger grep:** add `stopped at A3i \(an indentation shift`. Do not add a bare `stopped at A3i`, which also matches the measure-error line.
2. **Verdict regex:** add `FAIL A3i INDENT SHIFT.*`, plus the `FAIL A3c INCOMPLETE.*` still owed from the 11:00 row. The FAIL line already carries "copy the brief's lines byte-for-byte, including leading whitespace" (350 chars on KS-623, under the 600 cap).
3. **Recommended:** add a fixed INDENT SHIFT sentence to `instruction`, because 3 shifted lines can exceed 600 chars.
4. **Arm owed:** `/private/tmp/claude-501/night/a3i_0917/arms/A_new_ks623/checker.out` → `retry_feedback.verdict` starts `FAIL A3i INDENT SHIFT`, with `missed_sites == []`.

The builder checked the trigger by hand: the current trigger gives rc 1 (no retry); the trigger with the A3i clause gives rc 0 and the regex extracts the line.

Optional, not done: `build_input.sh` also writes an unstripped `expected_plus_exact`.

## TESTED / NOT TESTED / HOW
- **Tested:** both arms files (verbatim beside this file). Also the reanchored path with a3b arm J's section: OK when the brief sits at indent 4, and `SHIFT :446 observed=4 expected=6 delta=-2` when it sits at 6, so negative shifts are reported too.
- **Not tested:**
  - retry routing through `night_run.sh`;
  - a test-only brief with `+` lines;
  - tab-indented files;
  - a new-file (`--- /dev/null`) target (code present, no arm);
  - CRLF files;
  - jest inputs.
- **How:**
  - The runner lock was absent at 13:10, 13:15 and 13:22; `pgrep -x` rc 1; 0 checker/vitest processes (positive control: 15 bash processes).
  - Every rc was taken as `> file 2>&1; rc=$?`.
  - Runs used `nice` and `sandbox-exec` with no network; load peaked around 11.
  - Two earlier arm runs failed on arm-side mistakes, with the gate code at the same sha both times: E2 was tripped by the heading appearing in prose, and B2 expected the model's comment where A3i quotes the brief.
- **Independent observation (Wednesday):** SEARCH 17h, a separate agent, saw a KS-1009 wrong variant FAIL at `A3i INDENT SHIFT` on checker `f3ce186c…` during its proof (13:1x–13:2x). That is the gate firing outside its own arms.

## Files
- `tasks/code_patch/checker.sh` (backup `.pre-0917-a3i`)
- `tasks/code_patch/a3i_indent.py` (new)
- `tests/a3i_indent_arms.sh` (new)
- `IMPROVEMENTS.md`: one row stamped 13:27 (backup `.pre-0917-a3i`)

Not touched: `night_run.sh`, `build_input.sh`, `queue.md`, `candidates.md`, the briefs, `a3c_plus.py`, `a3b_line.py`. No mail, commits, pushes, Linear or GitHub writes.
