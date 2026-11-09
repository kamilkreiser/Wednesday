PR 2114: GO WITH NOTES; PR 2115: GO WITH NOTES

# Gate 277, tier 2 batch, Secuura / Blockchain, 2026-11-09 (11:33-11:37 local)

| PR | head | verdict |
|---|---|---|
| 2114 (KS-2141) | 39be43e5cc63d9d486652fd4cbe2d1fb598e1b05 | GO WITH NOTES |
| 2115 (KS-2132) | e9a127267f97dc7bea7cbd0a7ce849d0389ecdf8 | GO WITH NOTES |

Pins: develop 2a031f51403f, PR 2114 head and PR 2115 head were each read with ls-remote at the start and again at the end. None moved. Neither verdict is voided.
Both PRs are tier 2 (test-only / docs-only). The product-byte stop line was not crossed by either, so neither is NEEDS TIER 1.

## Q1 and Q4: surface and merge trees (both PRs)
FOUND:
- PR 2114 touches exactly 3 paths: the ks1560 suite and its two KS-2141 fragments (cheat/ and flow/). Diff is +70/-4. No product byte.
- PR 2115 touches exactly 1 path: the ks1534 api-gateway test file, +3/-0. No product byte. `connectorAllowList.ts` is identical to develop's.
- Merge trees (`git merge-tree --write-tree origin/develop origin/prN`): PR 2114 rc 0 (tree aa700c9e), PR 2115 rc 0 (tree 980482cd).
- The two PRs share no path (comm of the sorted path lists is empty).
- Both heads' merge-base is 273de443c30c, not the current develop 2a031f51403f. The three-dot diffs above are against that base. The merge trees were taken on current develop.
- Open PRs sharing paths: I fetched PR refs numbered 2080 and above (36 refs). Exact-path match on the 4 paths plus a stem grep for ks1560, ks-2141, ks1534, ks-2132 and connectorAllowList. The only hit is PR 2082 on the ks1534 test file. Its blob is 82d20a34, identical to develop's blob, so it is already merged by content (its head is not an ancestor of develop, but the file matches). Planted control: PR 2114's own diff against the same path list returns 3 hits, so the instrument finds a shared path.

## PR 2114 (KS-2141): BLUF
The new `links_jq` predicate does what the READY says. The suite is green at the head and every mutant I planted turned a named cell red. The only things that need a word are one weak spot (the comment strip is not pinned by a new cell) and one under-description in the fragment.

TESTED / HOW:
- Suite run on macOS /bin/bash 3.2.57 at the head. Result is 14 passed, 0 failed, rc 0. This covers F-2078-1 (7 spellings, and the continued line), F-2078-2 (3 spellings), and census CELL 2 with offenders empty. CELL 0 is the positive control that the census finds the 3 trivy suites. CELL 1 finds tenant_isolation.
- Census instrument planted defect: I turned the `ln -sf` in tenant_isolation_stderr_own_file.test.sh into `true -sf`. CELL 2 went red with `got "tenant_isolation_stderr_own_file.test.sh"`. Restored by sha (81b1a8b6 before and after).
- My own mutants of the predicate, with the suite restored by sha (da2781e2 before and after). Each was a no-op-checked sed:
  - Comment strip dropped: the existing "CONTROL every harmless respelling ... (5 spellings)" cell goes red, and only that one. The new F-2078-2 cell stays green. This matches what the seat disclosed.
  - Continuation join dropped: only "F-2078-1 a backslash-continued ln -sf" goes red.
  - `command` alternative dropped: "F-2078-1 every legitimate respelling (7)" goes red.
  - `--symbolic` dropped: same cell goes red.
  - `(` dropped from the prefix class: same cell goes red.
  - `)` dropped from the end class: same cell goes red.
- Predicate probes on one-line fixtures (own set): 
  - `ln -sf "$JQ_BIN" "$root/bin/"` gives no. `.../bin` gives no. `.../bin/jq.bak` gives no. `echo ln -sf x "$root/bin/jq"` gives no. `ln -f` (no symlink flag) gives no. A quoted `"ln"` gives no.
  - `... 2>&1`, `&>/dev/null`, `echo hi; ln ...`, `|| { echo x; }`, a trailing bare `#` all give yes.
  - `ln -sf "$JQ_BIN" "$root/mybin/jq"` gives YES (false accept).
  - `true || ln -sf "$JQ_BIN" "$root/bin/jq"` gives YES (the statement is present but may not run).
- Words: the paragraph above `links_jq` (lines 37-44), read against the code under it. Every clause is true of the code. The `ln`-as-command positions (line start, after `; & | ( !`, after then/do/else, after `command`), the symlink flag forms, "last word before end of statement or a redirection" and the comment/echo/`[ -x ]` rejections are all as stated. The destination-directory spelling `"$root/bin/"` is judged "no link" as the fragment says, and no cell pins it.
- Fragment figures: "cells 11 -> 14" is true (14 passed, 3 new cells). Hand change count "three of its five lines": the diff removes 4 lines (3 comment lines plus the old one-line regex) and fits.

Findings:
- G277-2114-1 (low): the comment-strip step is only pinned by a pre-existing control (the 5-spellings cell), not by a new KS-2141 cell. F-2078-2 stays green when the strip is dropped, because the regex's `[^;&|#]` class already refuses `#`. The seat disclosed this. A future edit that weakens the strip is still caught, by an older cell whose label does not mention it.
- G277-2114-2 (low): the predicate has false accepts. `$root/mybin/jq` matches because `bin/jq` is a substring of `mybin/jq`, and `true || ln -sf ... bin/jq` or a dead branch counts as "carries the link". The census asks whether the statement is present, not whether it runs, so this is within the suite's stated purpose. It is a limit the fragments do not state. They list only the destination-directory spelling as unmeasured.
- G277-2114-3 (info): the fragments describe the hand change as three of five existing comment lines. The file also has 3 added comment lines (42-44), a new KS-2141 paragraph. Neither fragment says so. This is not false, because "hand change" is about the old paragraph.

## PR 2115 (KS-2132): BLUF
The +3 lines add two new INPUT rows to the shared `NON_STRING_LISTS` table plus one comment line. There are no new cells and no new assertions. The two rows feed R1 to R5, so the cell count stays the same (11 in the file). They catch loops that skip the last element of a list of 4 or more, or of exactly 4, or that cap the walk at 4.

TESTED / HOW:
- File run at the head with vitest: 11 passed (11).
- Mutants of `allowListHoldsANonString` in connectorAllowList.ts. Each was run against the PR 2115 file (NEW) and against develop's version of the file saved beside it (OLD). Product file restored by sha (33a5cdf6 before and after).
  - M1 skip last element when length >= 3: NEW R1-R5 red; OLD 11 of 11 green.
  - M2 skip last when length >= 5: NEW R1-R5 red; OLD 11 of 11 green.
  - M3 (mine) walk capped at the first 4 indices: NEW R1-R5 red; OLD 11 of 11 green.
  - M4 (mine) skip last only for a list of exactly 4: NEW R1-R5 red; OLD 11 of 11 green. This is the one only the "number LAST of four" row can catch.
  - All four survive the pre-PR file, so the two rows do add detection.
- R5 goes red under every mutant. It compares the predicate's verdict array to an all-true array, so no row is named in its failure. This matches the seat's note that the cause was unread. I read the cell and this is the cause.
- Words: PR body and Linear comment NOT readable (no API access in this gate), so NOT TESTED. The READY's claims I could check hold: 11 -> 11 cells in the file, the five red cells (the READY's PR text may list three; I measured five), and "the four-string row is named only by the 3-or-more mutant" as a statement about the row. The M4 result bears out that the four-element row is the distinct one.

Findings:
- G277-2115-1 (low): the new cell label `a number LAST of four strings` is inexact. The list is `['SSD_DOCUMENT','X','Y',1]`: three strings and a number, four elements. The label would read true as "LAST of four elements". The other new label, `a null at index 4, the last, of five`, is correct. It only shows in a failure message.
- G277-2115-2 (info): the READY says R1, R2 and R5 turn red where five do. That is a count in the seat's own words, not the code's. The PR body may repeat it, which I could not read.

## NOT TESTED
- PR bodies and Linear ticket comments for both PRs: no read access in this gate. Not read, so NOT TESTED.
- The whole api-gateway suite ("1880 -> 1880", 168 files). I ran only the touched file (11 cells), because load was 9-10 throughout.
- `node scripts/docs-fragments.mjs check` for PR 2114: it REFUSED on my shallow clone ("fetch the full history"), rc 2. NOT TESTED.
- That the golden diff applies unchanged on 425ea1d3df0f: that commit is not in my clone.
- PR 2114's suite on Linux bash. Only /bin/bash 3.2.57 on macOS was run.
- Open PRs numbered below 2080, and open-versus-merged state of the PRs I fetched: I had no API, so "open" was approximated by content (a path sharing with develop-identical blobs counted as merged). The PRs numbered 2080+ are 36 refs, including both of mine.
- tsc and eslint of the PR 2115 test file; the pre-push hook legs; any runtime outside the in-process test server.

## My conduct
- Clone: /private/tmp/g277/r, blobless, depth 200, size 533M (du -sh /private/tmp/g277 at 11:36), NOT removed (QA no-rm). It holds two symlinks to the read-only checkout's node_modules, a scratch copy of develop's ks1534 test (ks1534old.test.ts), and sed-mutated files that I restored by sha. Nothing was done in /Volumes/DevMASTER/!CODING except read, the ssh key read, and the node_modules read through the symlinks. No git write verb ran there. Nothing was pushed, posted or mailed.
- One slip: the first vitest run used `/bin/sh -c "cd ... && ..."`, a cd inside a compound command. It ran in a subshell and changed nothing. All later calls used absolute paths only.
- stderr was never discarded. df DevMASTER at start and end: 108Gi free both times. Load1 was 9.1 at the start and about 10.3 at the end, which is OVER the load-1-under-8 limit. The load was not mine alone (an unrelated machine load), but the limit was exceeded during the run.
- Pins re-read at the end: develop 2a031f51403f, PR 2114 39be43e5cc63, PR 2115 e9a127267f97. None moved.
