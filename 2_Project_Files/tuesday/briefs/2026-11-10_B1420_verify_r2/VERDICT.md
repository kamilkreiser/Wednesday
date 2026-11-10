GATE B1420-2: GO WITH FINDINGS @ 7b0f7f9 on main 411400f

Round 2 of 2. Graded against ANSWER-1's bar (the product owner's ruling, option a, "Land the improved fix (labels always whole)"), which retires ADDENDUM-1's "43 of 43". Every item of that bar is met, measured by program with my own probe. The round-1 landing hold (F1/F2 look ruling) is lifted by that ruling. The findings below are Minor. Landing still needs the hosted CodeQL read first (NOT RUN).

Gate run 2026-11-10 13:44 to 14:00 AEDT, tier 2 (kit Q-2). No security-shaped issue found. My own clone and worktrees are under the session scratchpad; the push URL is `INVALID-NO-PUSH`; nothing was pushed. No port was opened (`lsof` of 9850-9859: nothing, rc 1, at start and end).

## The bar (ANSWER-1), measured

| Bar item | Bar | Measured at 7b0f7f9 | Instrument and control |
|---|---|---|---|
| Every cut sound at the real page count | all | 2,286 of 2,288; the 2 that are not are the F4 right-to-left cases (text into the label), identical at main | The round-1 probe (copied unedited from round-1 `evidence/probe.test.ts.txt`, sha256 `054b3450...`) over the same 2,288 inputs (sha256 `1399203b...`). Control: my main run reproduces round 1's main run byte for byte (first line and PDF sha256 in 2,288 of 2,288). |
| Every cut sound at `Page 9999 of 9999` | all | 2,286 of 2,288 (same 2 F4 cases); the 100 F1 cases: **100 of 100** | My own writer-direct probe (`evidence/gate2-sound.test.ts.txt`): the footer built exactly as `document-pdf.ts:179-188` builds it, with a fixed label. Control: main's first line in the 43 sound-at-main cases is sound at `Page 9999 of 9999` in **0 of 43**, so the probe can say no. |
| Every head cut sound beside all 10 label shapes (`Page p of m`, m 1 to 4 digits) | - | 415 of 415 searched cuts | Same probe. |
| No name cut shorter than the longest prefix sound at both | 100, or explain | F1: **72 of 100** at the bar; 28 short by 1 to 3 code points (gaps: 10 x 1, 15 x 2, 3 x 3). Explanation true in **28 of 28** | Longest-prefix search from the line's maximum length down to the cut: writer-direct at `Page 9999 of 9999`, then the product's own render with only the first line swapped. My 28 ids and (cut, longest) pairs equal the builder's `short28.json` in 28 of 28. For each of the 28, every longer prefix fails some label shape on a row 1 pt narrower (the model's `FOOTER_WIDTH_IN_HAND`), the cut passes all 10, and the longest sound prefix passes all 10 on the full row. So the shortfall is the 1 pt the model keeps in hand, and nothing else. See F6 for scope. |
| Label broken | 0 of 2,288 | **0** (main 59) | Same probe; the label detector fires 59 times at main. |
| Hash line lost | 0 | **0** (main 11) | The detector fires 11 times at main. |
| Overlap | only the 2 F4 cases | `adv1035r`, `adv1035d` only, at main and at head | The detector fires on those 2 at both. |
| First line unchanged vs main, so byte-equal | all | **2,022 of 2,022** (1,884 adversarial + 138 fixture) | PDF sha256 compared by program. |
| R10 keeps the four-digit guarantee and goes red when it is broken | red | red under 4 plants (below) | Plants in my scratch copy only, anchor count 1, restored, then a fresh green re-run (22 of 22). |

## Findings

| # | Severity | Finding | Instrument and control |
|---|---|---|---|
| F1 (round 1) | CLOSED by ruling | Names cut shorter than main. 100 cuts are still shorter than main, but every one is now **longer** than at `de6e5615` (100 of 100). The 43 sound-at-main cuts break the label at `Page 9999 of 9999` (0 of 43 sound), which is why ADDENDUM-1's 43-of-43 bar could not be met. The owner ruled on that trade (a). | Probe, above. |
| F2 (round 1) | CLOSED (kept) | The label repair: 0 broken at head, against 59 at main. | Probe. |
| F3 (round 1) | Minor, still open | Sizing by the real page count is still not done. `FOOTER_WIDEST_LABEL` is gone, but the model now sizes for all 10 label shapes up to four digits, not for the real count. `document-pdf.ts` and `pdf-fit.ts` are unchanged. The PR text claims only the tab, line-breaking and wide-piece work. | `git diff --name-only a54250f4 7b0f7f95`: 2 paths. |
| F4 (round 1) | Minor, pre-existing | 2 right-to-left names run into the label, at main and at head, and also at `Page 9999 of 9999`. Backlog. | `adv1035r`, `adv1035d`. |
| F5 (round 1) | Note | `linebreak` is loaded through pdfmake's own resolution. Unchanged. Host versions: pdfmake 0.3.11, pdfkit 0.19.1, linebreak 1.1.0. | `require(.../package.json).version`. |
| F6 | Minor (claim scope) | The builder's 72-of-100 count covers only the 100 F1 cases. Across all 265 changed first lines, **63** are 1 to 3 code points short of the longest prefix sound at both (gaps: 35 x 1, 23 x 2, 5 x 3). The extra 35 are 32 cuts that are already **longer** than main's, and 3 fixture names (`fx152`-class) that main printed whole while losing the hash line. The same 1 pt explanation holds in **63 of 63**. In a seeded sample of 150 unchanged clipped cuts: 0 short. Nothing here is shorter than main beyond the ruled 100. | My probe, `evidence/sound-prefix-head.jsonl`; `analyse3.py`. |
| F7 | Note | The ruling's card says "still shorter than main in 43 unusual test names". By program the head is shorter than main in **100**: the 43 sound at 1 page, plus 57 where main breaks the page label at its real count. Those 57 are the F2 repair the owner asked to keep. 0 of the 168 project fixtures are cut shorter, as the card says. No action; listed so the record is exact. | Probe. |
| F8 | Note | R15's typed first line (109 code points kept) equals the longest prefix sound on a row 1 pt narrower than the writer's. It is a measurement from the render on that row, not a product output, and it pins the model's margin. Its string and integer pins each go red when changed by one. | Plants F, G, H below. |

No blocker: 2 paths, both in OWNS; no secret, no name, no id; nothing red at head or merge that is green at main; no hosted touch; no deploy trigger (0 `.github/` paths at head; control: `docker/` lists 4).
No major: the merge is clean, no STATUS claim is contradicted, no new test is vacuous, and the CodeQL pre-scan has 0 hits.

## Checks, by step
1. **Refs** (re-read 13:44 and 13:58).
   - `refs/heads/b1420/composer-footer-model` = `7b0f7f954bd4a197de71e1cc52fcb938ecda2dd8` (the READY sha). `refs/heads/main` = `411400f779e9300625e38bada2fb662b1763df3a`, unchanged since round 1. Control: `refs/heads/b1249*` lists 1 ref.
   - Three commits on base `a54250f4`; the new one is `7b0f7f95` on `de6e5615`, a forward commit with no rewrite.
   - Paths: 2 of the 3 OWNS. `change-report.ts` +216 -47 and `change-report.test.ts` +323 -10 on base; this round adds +62 -40 and +65 -9.
   - The 10 deleted test lines: 9 in R10's boundary block (comments, the 77/78 W pins, the 1000-page input, render call and `where` text), each replaced. The tenth is a blank line in the same block, a diff-alignment artefact of the base diff (the per-commit diff shows 9).
   - Every other `packages/renderers` blob equals main's.
   - Overlap, by file lists from `refs/pull/<n>/head` against the merge base, on the same 119 PR refs as round 1:
     - #85 (57 files): only `pdf-fit.ts`, which the branch does not touch, so the branch overlap is 0;
     - #86, #91 and #119 (2 files each): 0;
     - sibling lane `b1423/...` (2 files): 0.
2. **Merge.** `git merge-tree --write-tree main head`: rc 0, tree `3b83d60c`, the same as the builder's. It differs from main only in the 2 lane paths, and both blobs equal the head blobs (`2474e385`, `616deb70`). Control: a loose commit editing main's `modelledFooterRows` signature line gives rc 1 with a conflict in `change-report.ts`.
3. **CI.** The repo has no workflows. Its predicate is the node step of `scripts/ci.sh`, run here on host node v26.13.0 with `node_modules` copied from the project checkout, as in round 1.
   - `tsc -b tsconfig.build.json` at main, head and merge: the same 4 errors, all in `apps/api/src/app.ts` (`@fastify/rate-limit` is missing on the host). The renderers `dist` is rebuilt in each tree (`FOOTER_LABELS`: 0 at main, 3 at head and merge).
   - Renderers project, vitest JSON compared by program:
     - main 263 (262 passed, 1 skipped);
     - head 267 (266 passed, 1 skipped): lost 0, added 4 (R12 to R15, all passed);
     - merge 267, equal to head (lost 0, added 0).
     - Compare control: one row dropped from a scratch copy reads `lost 1`.
   - Workspace project at main and at merge: 2,838 each (2,836 passed, 2 failed), lost 0, added 0. The 2 failures are the withheld-SOW `citations.test.ts` rows, at both. `apps/api/src/app.test.ts` does not load at either (environment).
   - eslint (whole tree): rc 0 at main and at merge. Plant control: rc 1.
   - `prettier --check` (the repo's ignore files): rc 0 at main and at merge. Plant control: rc 1, naming `change-report.ts`.
   - `tsc -p apps/web/tsconfig.json` and `tsc -p apps/web/e2e/tsconfig.json` at merge: rc 0.
   - Repo-wide hidden-character scan over 967 tracked text files: 23 Cf in 6 files, the same at main and at merge. Relative-link check: 5 `.md` files, 0 relative links, 0 broken. The check is weak, as in round 1.
   - Secrets: host gitleaks 8.30.1 with `scripts/gitleaks.toml`, over the 3 branch commits: no leaks. Control: 2 planted secrets give rc 1, "leaks found: 2".
4. **Red without the fix** (my scratch copy of the head tree, `change-report.test.ts` only):
   - On main's `change-report.ts`: 5 red. R10 fails with `a word of 83 W: expected Infinity to be 1`, and R12, R13, R14 and R15 fail, each for its stated reason. 17 pass.
   - On `de6e5615`'s `change-report.ts`: 2 red. R10 fails with `a word of 83 W: expected Infinity to be 1`, and R15 fails on its first line. 20 pass. This is the builder's claim, word for word.
   - Guarantee plants on the head source:
     - A: the label-rows check removed. R10 goes red (`a word of 84 W: expected 1 to be Infinity`), and so does R15.
     - C (mine): `FOOTER_LABELS` cut to one-digit counts. R10, R13 (1000 pages, hash line missing) and R15 go red.
     - D (mine): `FOOTER_ROWS` + 1. R10 and R15 go red.
     - B: the 1000-page boundary word set to 86 W. R10 goes red (`page 1: the page label is missing or cut`).
   - Pin plants on R15: F changes 112 to 113, G changes rows 3 to 2, H cuts one character from the typed line. All three go red.
   - After restoring: 22 of 22 green, and `git status` is clean.
5. **Closed lines.**
   - The tab and refused-break defects: re-shown red at main (R12, R13, R14).
   - Hash line lost: 11 at main, re-shown by the probe.
   - Page-count sizing: open (F3).
6. **Probes.** The bar table above.
   - Head against main by first line:
     - fixtures: 138 unchanged and byte-equal, 18 cut longer, 1 now whole, 11 newly clipped where main lost the hash line, 0 shorter;
     - adversarial: 1,884 unchanged and byte-equal, 136 cut longer, 100 cut shorter (43 sound at main at 1 page, 57 not).
   - The 100 shorter at head are exactly round 1's F1 set, and all are longer than at `de6e5615`.
7. **Scans** (python `re`, case-insensitive, `(?<![A-Za-z])<name>(?![a-z])`), over 518 added lines and the 3 commit messages:
   - ban list plus the coordinator names: 0. Control: a planted `_by_<name>_` fires for all 9.
   - B-numbers, ticket keys and seat ids: 0. Control: 3 of 3.
   - UUIDs: 0. Secrets: 0. Hosts: 0 in added lines; the messages hold only the attribution address.
   - Cf: 0 (control 2 of 2). Non-ASCII and control bytes: 0. The test file's non-ASCII line count is 2 at main and 2 at head.
   - Each commit has exactly 1 `Co-Authored-By` trailer.
   - **CodeQL pre-scan** over the added lines: 0 for each of `new RegExp(` from a variable, `.replace(/[...]/g, "\\$&")` hand-escapes, `innerHTML`, `dangerouslySetInnerHTML`, `child_process` with a template string, `eval` and `new Function`. Control: 2 of 2 planted lines hit. The 4 `.replace` calls added use literal regexes or constants (`FOOTER_TAB`, `/\r?\n$|\r$/`, `/\s+/g`).
8. **Claims** (STATUS sections ADDENDUM-1 and ANSWER-1).
   - True:
     - sha, the forward commit, main and the merge tree `3b83d60c`;
     - +62 -40 and +65 -9, and the 9 R10 lines;
     - `it(` 21 to 22, non-ASCII 2;
     - the commit message is ASCII and clean;
     - 100 of 100 sound at both;
     - 72 of 100, with the 28 and their 1 pt explanation (exact ids and values);
     - label 0 (main 59), hash 0 (main 11), overlap only F4, 2,022 byte-equal;
     - 43 of 43 main cuts break the label at `Page 9999 of 9999`;
     - R15 and R10 red at `de6e5615` with the quoted messages;
     - plants A and B red;
     - the renderers counts.
   - Not shown by me:
     - whole-run 3,124 (host cannot load the API suite);
     - lint, format, typecheck and build inside the CI image (my host equivalents are green);
     - the claim that the probe re-run matches in the node 22 image.
   - Incomplete: the 72-of-100 scope (F6).
9. **Tier.** 2, per Q-2. No security-shaped issue.

## NOT RUN
- **The CI image** (`docker/Dockerfile --target ci`): no node or `pc-*` image is cached and no registry fetch is allowed. Host node is a lead, not the predicate. **Hosted proof is required: CodeQL `Analyze (javascript-typescript)` and `Analyze (csharp)` on the PR head, read before landing.**
- The DB suite (`scripts/test-db.sh`) and the `apps/api` tests that need `@fastify/rate-limit` or postgres. The lane's paths are not read by the DB suite.
- The digest-pinned gitleaks image and `secret-scan.sh --history`.
- The open or closed state of PRs #85, #86, #91 and #119, and the CodeQL alert state (hosted API, fenced).
- `change-report.test.ts` 3 times in a row and with shuffle: not repeated by me. It ran green 4 times across my plant restores.
- I did not take the project heavy lock (writing it is outside my write area). It was absent at 13:46, and every suite ran serially. Host load1 was 11 to 16 throughout, and nothing timed out.

## Evidence (`evidence/`, with SHA256SUMS)
- `probe-main.jsonl`, `probe-head-7b0f7f9.jsonl`: the round-1 probe over the 2,288 inputs at main and at head.
- `sound-prefix-head.jsonl`: per id, the head cut at `Page 9999 of 9999`, the 10-label check and the longest-sound-prefix search, with the 1 pt rows.
- `gate2-sound.test.ts.txt`, `analyse2.py.txt`, `analyse3.py.txt`, `g2sets.json`: the probe and the comparison scripts.
