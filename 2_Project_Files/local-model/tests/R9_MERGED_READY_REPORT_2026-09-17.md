# R9 merged-READY fix — build_comment_input.sh (2026-09-17, tooling agent for Wednesday)

## BLUF
- **Defect confirmed.** At tip `75ad0e55c` the unchanged builder refuses a KS-1179 F-5 docblock brief (range `ssrf-guard.ts:460-461`) with R9 naming `READY_KS-932_ornith35b-q4_PASS-7of7_2026-09-15.diff.md @@ -471,7`. `40fe4db69` (#1004, KS-932) is an ancestor of origin/develop, and all 12 of that READY's `+` lines for ssrf-guard.ts are at the tip, while its 2 `-` lines are gone (a third `-` line, `const timeoutMs = init.timeoutMs ?? 10_000;`, is moved: the READY adds it back).
- **Fixed:** `night/build_comment_input.sh`. Backup: `night/build_comment_input.sh.pre-0917-r9merged`. Written as `.new`, then `mv` over it; `night/log/.night_run.lock` was absent.
- **New arms `tests/r9_merged_ready_arms.sh`: 15/15.** Before the fix: 13/15, with only the two NEW-side ARM1/ARM1b arms failing (the red proof).
- **`tests/comment_patch_arms.sh`: 48/53 with the NEW builder, and exactly 48/53 with the OLD builder** (a scratch copy with only `BUILDER=` pointed at the backup; outcomes are the same arm for arm). The 5 failures come from drift that happened before this change, not from the fix. See below.
- **No other builder has a READY-proximity rule.** `night/build_input.sh`, `tasks/bash_patch/build_bash_input.sh` and `tasks/doc_patch/build_doc_input.sh` have no READY scan (grep `-i` for `ready|proximity|within N lines|glob`). Nothing else was changed.

## The change (R9 only)
If a READY file has a hunk that R9 would match (same file, within 10 lines of a named range), it now checks that READY's content for the product file, across all of its hunks for that file:
1. every `+` line is present at the tip;
2. every `-` line that the READY does not also re-add (a moved line) is absent at the tip;
3. at least one `+` line has alphanumeric text. A READY with no `+` evidence is never counted as merged, which keeps the old `comment_patch_arms` R9 fixture, a header-only hunk, refusing.

If all three hold, it prints `R9 READY skipped: already at tip: <READY> (+N present at the tip, -M absent (K moved); its hunks [...] would otherwise block)` and the READY does not block. Any other READY refuses exactly as before, with the same message. The hunk matching, the 10-line window and the path matching are unchanged; the path test was moved into `_is_prod`, byte-for-byte the same.

**Why moved lines are excluded (a stated improvement on the shape I was given):** without the exclusion, the real KS-932 READY can never qualify. Its `- const timeoutMs = ...` line is re-added verbatim by `+` in its first hunk. This follows the same logic the builder already uses for `must_remove`.

**Conservative on purpose:** a `-` line whose text also appears somewhere else in the tip still counts as "present" and refuses. A READY that merged with seat edits (so its content differs from the tip) keeps blocking. A sweep of all 127 night/READY_* files at `75ad0e55c` (informational, not an arm) judged 13 file-sections "at tip". Every one belongs to a ticket whose number appears in a develop commit message, so there were **no false skips**. 16 more sections belong to tickets in the develop log but differ in content (seat edits, renamed tests), and they still block.

## Arms (`tests/r9_merged_ready_arms.sh`, final run 21:20, scratch `/var/folders/.../T/r9_merged_arms.r5y99sxy`)
| Arm | OLD builder | NEW builder |
|---|---|---|
| ARM1: real KS-932 READY alone + F-5 range :460-461 | rc 2 REFUSED R9, names KS-932 | rc 0; "skipped: already at tip: READY_KS-932 (+12 present, -2 absent (1 moved))" |
| ARM1b: same brief, scratch copy of the whole corpus (127 READYs) | rc 2 REFUSED R9, names KS-932 | rc 0; KS-932 skipped; READY_KS-1179-F4 touches the file but not within 10 lines |
| ARM2: synthetic UNMERGED (KS-932 with `Date.now()` changed to `performance.now()` in one `+` line) | rc 2 R9 | rc 2 R9, names it, nothing skipped |
| ARM2b: hunk header with no `+`/`-` lines | (not run) | rc 2 R9 |
| ARM3: PARTIAL (every `+` present; a context line still at the tip turned into `-`) | rc 2 R9 | rc 2 R9, nothing skipped |
| ARM4 ×7: KS-979, 1118-F3a, 1118-F3b, 1179-F4, 1156-A2, 1156-A3 and 1120-F3 rebuilt from their briefs | rc 0 | rc 0; `comment` block identical to night/inputs/comment_*.json; NEW JSON == OLD JSON in full |
| SOURCE: tracked state of the Secuura checkout | unchanged | unchanged |

Notes on ARM4:
- **Fields that differ from the stored inputs:** only `tip` and `repo` (repo.tip), and only for KS-979, 1118-F3a and 1118-F3b, which were built at `19f1e5475` and are now rebuilt at `75ad0e55c`. `files` and `ticket` are identical. For 1179-F4, 1156-A2/A3 and 1120-F3 there is no difference at all.
- **READY dir:** a scratch copy of the corpus minus each input's own `READY_<id>_*comment-PASS*`. That READY was produced from that input and is not merged, so both builders correctly refuse the rebuild when it is present (checked by probe: KS-979 and KS-1179-F4 refuse R9 against the real night/).
- **R10/R11** go to localhost stubs (Backlog, no open PR), so live ticket and PR state cannot change this regression.

## comment_patch_arms.sh: 48/53, the same with the OLD builder
The 5 failing arms are `ARM10 R10-linear-inprogress`, `R11-open-pr-on-file`, `R11-github-unreachable`, `OK-stub-clean` and `OK-real`. Each gets `REFUSED R9` naming `READY_KS-979_ornith35b-q4_comment-PASS-9of9_2026-09-17.diff.md`:
- **Cause:** these arms run with no `NIGHT_READY_DIR` seam, so they read the real night/. That READY was written at 20:43, after the arms file (20:25). KS-979's comment change is not merged, so R9 is right to refuse.
- **Proof it is not this change:** the OLD builder gives the same 48/53, arm for arm.
- **Fix belongs to the arms file**, which is outside this commission's write set: give those 5 arms `NIGHT_READY_DIR` = a scratch copy of the corpus minus READY_KS-979's comment READY, as ARM4 here does. It has not been changed.

## Files
- `night/build_comment_input.sh` (changed); `night/build_comment_input.sh.pre-0917-r9merged` (backup)
- `tests/r9_merged_ready_arms.sh` (new)
- this report
Nothing was queued; queue.md and done.md were not touched; nothing was committed.
