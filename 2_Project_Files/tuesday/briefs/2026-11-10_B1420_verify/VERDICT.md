GATE B1420: GO WITH FINDINGS @ de6e561 on main 411400f

LANDING HOLD (F1): the branch is mechanically sound, but it carries a visible change the tickets do not name. Under the coordinator's Q-answer ("anything more is HELD for the product owner") the landing waits for the product owner's look ruling on F1. Run landing.txt only after that ruling says "land as is".

Gate run 2026-11-10 08:22 to 08:40 AEDT, tier 2 per the kit's Q-2; no security-shaped issue found, so no tier-1 escalation. Own clone under the session scratchpad, push URL set to `INVALID-NO-PUSH`, nothing pushed.

## Findings

| # | Severity | Finding | Instrument and control |
|---|---|---|---|
| F1 | HELD (product owner look) | **A visible change the tickets do not name: names cut shorter than needed.** Of 2,120 adversarial renders, 100 names that were already cut at main are cut **19 to 42 code units shorter** at head. In **43** of them main's render was already sound: the hash line was inside the page, the page label was whole and nothing ran into it. The shorter cut fixes nothing there. In the other 57, main's render had a broken page label; see F2. All 43 are shapes the writer will not break (an opening bracket followed by spaces, a space before a closing mark, tab runs) or seeded random names. Example (`adv0005r`): main shows `W x25 "( " W x55 " Policy Designer \| Synthetic engageme..."` on 2 rows; head shows `W x25 "( " W x51 "..."` on 1 row. Cause: `modelledFooterRows` returns Infinity for a piece wider than `footerColumn()`, the old fixed column (`change-report.ts:661` at head). The row filling now uses the wider `footerTextColumn`, and the writer's line breaker now joins `W( W` into one piece. So a joined piece that the writer would wrap cleanly is clipped instead. In the project's own 168 fixture renders this happens **0** times. The builder disclosed this class (32 cases on its set, case B4 in its PDFs). | My probe renders the change-report PDF at main and at head for the same 2,288 inputs and compares by program: the first line, the PDF sha256, and the rows, hash line and label read back from the text layer. Controls: 1,957 + 149 renders whose first line is unchanged are **byte-equal**. The hash-lost detector fires on 11 fixture renders at main, the label detector on 59 at main, and the overlap detector on 2 at both. |
| F2 | HELD (with F1) | **A second visible change, a beneficial one, that the builder's STATUS does not mention.** In 59 adversarial renders at main the page label is broken: pdfmake squeezes the label column and prints it in fragments (`Pag` / `e 1 o f 1`). Head prints a whole `Page 1 of 1` in all 59, because it cuts those names shorter. This is a fix, but it is not in the tickets' words, so it goes to the same look ruling. | The same probe. Head label broken: **0 of 2,288**. Main: 59. Shown in `pdftotext -layout` of `evidence/before/label-repair_adv0008r.pdf` and `evidence/after/label-repair_adv0008r.pdf`. |
| F3 | Minor | **Scope of what this closes.** The ticket about sizing by the real page count is not done. The builder STOPPED it as an item: the fix needs the page count in the footer callback in `document-pdf.ts`, which is not this lane's file and is listed by held PR #85. That ticket also has no Done-when line, so the Q-1 rule cannot be met. The older footer-budget ticket's policy-PDF half is open too. The PR text must claim only the tab and line-breaking tickets. | `git grep` at head: `FOOTER_WIDEST_LABEL = "Page 9999 of 9999"` is still the sizing label (`change-report.ts:514`, used at `:532` and `:635`). `git diff --name-only` shows `document-pdf.ts` and `pdf-fit.ts` unchanged. |
| F4 | Minor (pre-existing, not this branch) | Two right-to-left (Arabic) names run the footer text into the page label, at main and at head alike. The first line is identical at both and the PDF is byte-equal. Out of scope; listed for the backlog. | Probe ids `adv1035r` and `adv1035d`: `into_label` is true at both. |
| F5 | Minor | `linebreak` is loaded through pdfmake's own resolution (`createRequire` of `pdfmake/package.json`) and is not declared in `@pc/renderers`'s `package.json`. That is deliberate, to get the writer's own copy, and it resolves today. A lockfile bump that moves pdfmake to a different `linebreak` moves the model with it, which is the point. Noted, not a defect. | The lockfile at main has `linebreak 1.1.0`, `pdfmake 0.3.11` and `pdfkit 0.19.1`. Lint is green with it. |

No blocker: every changed path is inside the lane, there is no secret and no name, nothing is red at head or at merge that is green at main, nothing touches a hosted service, and the merge triggers no deploy (the repo has no `.github/` tree: 0 paths; control: `docker/` lists 4).
No major: the merge is clean, no claim is contradicted, and no new test is vacuous.

## Checks, by step

1. **Refs.**
   - `git ls-remote`: `refs/heads/b1420/composer-footer-model` = `de6e5615957cd4a48967f7f8a2f24cdb826ea1ad` (the READY sha). `refs/heads/main` = `411400f779e9300625e38bada2fb662b1763df3a`. Re-read at 08:37: same. Control: an older lane ref pattern lists 1 ref.
   - Changed paths: 2 of the 3 the lane OWNS (`packages/renderers/src/change-report.ts` +175 -28, `packages/renderers/test/change-report.test.ts` +257 -0). `pdf-fit.ts` is not touched.
   - Merge base: `a54250f4`. Two commits, one per ticket, each with exactly one `Co-Authored-By` trailer.
   - Overlap with the sibling that landed this morning (`a54250f4..411400f7`: `apps/web/src/screens/Discovery.tsx` and `LaneC4-discovery-typed-subanswer.test.tsx`): **0**.
   - Overlap with open PRs, from file lists computed from `refs/pull/<n>/head` against the merge base:
     - #85: 57 files, 0 overlap. It lists `packages/renderers/src/document-pdf.ts` (line 44) and `packages/renderers/src/pdf-fit.ts` (line 46); this branch touches neither, as Q-3 requires.
     - #86: 2 files, 0 overlap.
     - #91: 2 files, 0 overlap.
     - Control: the same filter finds lines 44 and 46 on #85.
   - `refs/pull/119/head` holds the same two paths as the landed sibling, and its content equals main. It is the sibling's PR; its open or closed state was not read (that needs the hosted API).
2. **Merge.**
   - `git merge-tree --write-tree origin/main head`: rc 0, tree `011b34fa42f98e999be8a4dffc0c8c3b28298093`. This is the same tree id the builder recorded.
   - It differs from main only in the two lane paths, and both blobs equal the head blobs (`069f6013`, `cefeb3b3`).
   - Control: a loose commit on main that edits the `FOOTER_HARD_BREAK` line (main `:521`) gives rc 1 with a conflict in `change-report.ts`.
3. **CI** (the repo has no workflows; its predicate is the node step of `scripts/ci.sh`).
   - The CI image could not be built offline: neither `node:22-bookworm-slim@sha256:83f4...` nor any `pc-*` image is cached, and the builder's `pc-b1420-node:base` had been removed by its own Step 6. Fallback: host node v26.13.0, with `node_modules` copied from the project's local checkout into my scratch trees. That copy differs from main's lockfile in 44 entries: optional platform binaries plus `@fastify/rate-limit`, `fastify-plugin` and `ip-address`, which the API needs. Every renderer dependency is identical: pdfmake 0.3.11, pdfkit 0.19.1, linebreak 1.1.0, fontkit 2.0.4, vitest 5.0.0, typescript 5.9.3, eslint 10.10.0, prettier 3.9.6.
   - `tsc -b tsconfig.build.json` built `engine`, `renderers` and every package at main, head and merge. The only errors are 4, all in `apps/api/src/app.ts` (`@fastify/rate-limit` is missing), identical at all three.
   - Renderers project, vitest JSON compared by program:
     - main 263 (262 passed, 1 skipped);
     - head 266 (265 passed, 1 skipped): lost 0, added 3 (R12, R13, R14, all passed);
     - merge 266, equal to head (lost 0, added 0).
     - Compare control: one row dropped from a scratch JSON reads `lost 1`.
   - Workspace project at main and at merge: 2,838 each (2,836 passed, 2 failed), lost 0, added 0. The 2 failures are the E8 SOW citation rows, whose withheld text is not mounted, at both. `apps/api/src/app.test.ts` fails to load at both (missing `@fastify/rate-limit`, an environment fault).
   - `eslint` (whole repo): rc 0 at main and at merge. Plant control: rc 1 with 5 error lines.
   - `prettier --check` (whole repo, with the repo's ignore files): rc 0 at main and at merge. Plant control: rc 1.
   - `tsc -p apps/web/tsconfig.json` and `tsc -p apps/web/e2e/tsconfig.json` at merge: rc 0.
   - Repo-wide hidden-character scan over every tracked text file (967): 23 Cf characters in 6 files, the same file list at main and at merge. Relative-link check over tracked `.md`: 5 files, 0 relative links, 0 broken, at both. The check is weak, as there is nothing to break.
   - Secret scan: host gitleaks 8.30.1 with the repo's `scripts/gitleaks.toml`, over the branch commits and over the head `change-report.ts`: no leaks. Control: 2 planted keys give rc 1 and "leaks found: 2". This is not the digest-pinned image `secret-scan.sh` uses.
4. **Red without the fix**, in scratch copies:
   - Head tests on main's `change-report.ts`: R12, R13 and R14 are red, and the 18 existing rows pass. R12 says "the footer model says 1 rows for the first line, the render takes 2". R13 says "...says 2 rows ... the render takes 3". R14 says "...says 3 rows ... the render takes 2".
   - Head tests on commit 1's `change-report.ts`: R13 and R14 are red and R12 is green. Each commit's rows are red without that commit's fix.
   - Every expected integer is a typed literal, compared against the render read back through `readPdfTextLayer`. None is a product output.
5. **Closed lines.**
   - The tab defect at main: re-shown by R12 red at main.
   - The refused-break defect at main: re-shown by R13 red at main, and by 11 project-fixture renders that lose the hash line at main and keep it at head.
   - Page-count sizing: open (F3).
   - The policy-PDF half of the older footer ticket: open (F3).
6. **Probes.**
   - The writer port was read against pdfmake 0.3.11 source and matches it: `DocPreprocessor.js:6` (tab to four spaces), `TextBreaker.splitWords` (the `lineEnd` rule), `Line.hasEnoughSpaceForInline` and `addInline` (the leading and trailing cuts, `newLineForced`), and `LayoutBuilder.buildNextLine` with `findMaxFitLength` (the hard wrap; `cloneInline` keeps `lineEnd` on both halves, as the model does).
   - Main against head render probe: 2,288 inputs. 168 are every change-report input the project's own renderer tests build, logged from a scratch copy. 2,120 are adversarial company names:
     - brackets and curly quotes with 1 to 3 spaces;
     - closing marks after spaces;
     - tab runs of 1 to 80 (lead, mid and trail);
     - hyphen, slash, soft hyphen, ZWSP, NBSP, ideographic space, em dash;
     - CJK, emoji, combining marks, Arabic, U+2028, CR LF, VT;
     - 500 seeded random names.
   - Results:
     - Head loses the hash line **0 of 2,288** times (main: 11, all fixture names that the new rows pin).
     - A page label is broken **0** times at head (main: 59).
     - A name that was whole at main is clipped at head only in the 11 renders where main lost the hash line.
     - Changed first lines: fixtures 19 (11 newly clipped where main lost the hash line, 7 cut longer, 1 now whole); adversarial 163 (63 cut longer, 100 cut shorter: F1 and F2).
     - Every unchanged first line gives a byte-equal PDF.
   - Writer-direct at 1,000 pages, on 8 head first lines that take 2 rows (the widest W and @ lines, a hyphen case, tab-after-line-feed cases, bracket cases): the hash line is lost on 0 pages, the label is broken on 0, and text overlaps the label on 0.
   - The builder's look evidence: `SHA256SUMS` verifies 18 of 18; controls C1 to C4 are byte-equal, and A1 and B1 to B4 differ, as its table says.
7. **Scans** (python `re`, case-insensitive, `(?<![A-Za-z])<name>(?![a-z])`), over the 432 added lines and both commit messages:
   - Ban-list names: 0. Control: a planted `_by_<name>_` fires for every name.
   - Ticket or brief ids and coordinator names: 0.
   - UUIDs or tenant ids: 0. Secrets: 0. Hosts or URLs: 0. Private keys and GitHub tokens: 0.
   - Cf characters: 0 (control: 2 of 2). Non-ASCII: 0. Raw control bytes: 0 (the test uses `\t` and `\n` escapes).
8. **Claims in the builder's STATUS.**
   - True: branch sha and base; 2 commits, 2 paths, +175 -28 and +257 -0; `pdf-fit.ts` and `document-pdf.ts` untouched; test rows 18 to 21; renderers 263 to 266, lost 0, added 3; the red-first messages, word for word; the tab cause (`DocPreprocessor.js:6`); the library versions; merge tree `011b34fa` and a clean merge on `411400f7`; evidence sha256 and byte-equal controls; no name, key or secret.
   - True in kind on my own set: 0 hash lines lost at head; 0 names whole at main and clipped at head except where main lost the hash line; the shorter-cut class (my count 100 on my set, against its 32 on its set).
   - Not shown by me: whole-run 3,120 to 3,123 (the API suite cannot load without the CI image); its 757-case and 1,237-case counts (its inputs are not in the kit); the lint, format, typecheck and build rcs inside the CI image (my host equivalents are green).
   - Incomplete: the STATUS gives the 32 shorter cuts as kept-the-hash-line-at-main, without saying that many such cuts also repair a broken page label (F2).
9. **Tier.** Tier 2 per Q-2. No security-shaped issue found.

## NOT RUN
- **The CI image** (`docker/Dockerfile --target ci`): its base image is not cached and no registry fetch is allowed. Every check above ran on host node with a copied `node_modules`. It is a lead, not the CI predicate. **Hosted proof is required: CodeQL `Analyze (javascript-typescript)` and `Analyze (csharp)` on the PR head**, read by the coordinator before landing.
- **The database suite** (`scripts/test-db.sh`) and `apps/api` tests that need `@fastify/rate-limit` or postgres. The lane's paths are not read by the DB suite. The API renders change reports through `render.ts` and the built `dist`; covered only by the renderer tests.
- **The digest-pinned gitleaks image** and `secret-scan.sh --history`. Host gitleaks was used on the branch range only.
- **The open or closed state of PRs** (#85, #86, #91, #119) and any CodeQL alert state: these need the hosted API, which is fenced. File lists were taken from `refs/pull/<n>/head`.
- The Word footer (unchanged code path; R3 passes).

## Evidence (this folder)
- `evidence/probe-main-vs-head.jsonl`: 2,288 rows (id, company name, and the main and head first line, sha256, pages, rows, hash line, label). ASCII-escaped.
- `evidence/before/` (main) and `evidence/after/` (head): 7 cases (3 over-clip F1, 2 label repair F2, 2 controls), with `SHA256SUMS`. The controls are byte-equal.
- `evidence/probe.test.ts.txt` and `evidence/analyse.py.txt`: the probe and the comparison script.
