# B341 DRAFTER REPORT (QA gate, tier 1, Composer PR #84, SEAT-G24)

Drafted 2026-10-20 19:55 to 20:01 AEDT by Tuesday's drafting sub-agent. Wrote only the brief `2026-10-20_B341_SEAT-G24_composer-gate-pr84-tier1.md` (about 51 KB, over the 40 KB aim: it carries the B331 shape plus the render-measurement rows) and this report. No docker, no tests, no HTTP to any host, no mail, chat or publish tool; git in the project only with read verbs; gh GET only.

## Sources read whole
B331 gate brief (template), B323 builder brief, B323 ANSWER-1, B323 STATUS (120 lines). B320 only skimmed (grep for the load rule and E8 text, not read whole). CLARIFICATIONS C-93 and C-95 read; C-86..C-96 headings confirmed. Build plan L6 headings only (lines 91-102). Not opened: Source_Documents, inbound, .env, keys.

## Slots left for Tuesday
Two, each on its own line: the stamp-time slot (line 13, launch time) and the main-sha slot (line 9, 40 hex from ls-remote at launch). Grep count on the brief 2 (MEASURED 20:00); Tuesday's `.pre-stamp` copy will print 2, the stamped copy must print 0.

## Measurements (instrument, time)
- Clock 19:55:36 AEDT. `uptime` load 6.93 6.35 4.71 (19:55); `ps` showed `docker rm -f -v pc-b335-db-…` running at 19:56, so B335 is live.
- `git ls-remote origin` (project 2_Project_Files, 19:55:36): main `318df1767035e92a55f633824927ce01b9986293`; `refs/heads/b323/policy-pdf-toc` and `refs/pull/84/head` both `0f64aee7f9311486ccd5de2bda381e210d2398e7`; `refs/pull/83/head` `8e062d94549ee027c5ed66924bce45f33904e9e0`; `refs/pull/82/head` `e62889831069135abc25e61b08f2f59f8196e4fd`. `refs/heads/b341*` none; `b301*` control prints the branch.
- `gh api pulls/84`: open, draft, 3 commits, 11 files, +650/-46, mergeable_state blocked. `base.sha` reads `318df176` (current main), while the branch's merge-base is `d8d2a2c7` (`git merge-base`; `rev-list --left-right --count` 1 behind, 3 ahead). `pulls/84/files` listed the 11 paths now in the brief.
- All five commits named in the brief are present as objects in the local clone (`cat-file -t` = commit).
- Commit messages read with `git log d8d2a2c7..0f64aee7` (three; author, trailer as in the brief).
- `git diff --name-only d8d2a2c7 318df176` = the two PR #82 test files only.
- PR #83 now at `8e062d94`: 19 paths changed vs `d8d2a2c7`; `comm -12` against #84's 11 paths = 0 shared (19:58). Legacy `git merge-tree d8d2a2c7 318df176 0f64aee7` printed 0 "changed in both" and 0 conflict markers, no positive control (said so in the brief; not proof).
- Code at head (`git show 0f64aee7:…`): `policy-document.ts:48` DOCX `policy-document/1`, `:55` `policy-document-pdf/3`, `:60` `POLICY_PDF_TOC_TITLE = "Contents"`, `:885` `toc: { title: … }`; `document-pdf.ts:40`, `:147-163`, `:176-178`, `:252-253` the toc marking and node. `git grep -F 'policy-document-pdf/'` at head: src:55, b139 test lines 11, 13, 16, 67, b59 test:242 (comment), plus the new b323 test; at base `/2` at the same places. No hit in apps/api.
- Themes: `git grep -i -E 'theme|dark'` in `packages/renderers/src` at head: one comment in `brand.ts:7`; so the PDF has no themes (the brief says "n/a unless you find one"; head markings are the variants).
- CodeQL (19:57): check-runs Analyze (csharp) and (javascript-typescript) in_progress since 08:54:50Z; combined status pending, 0 contexts; analyses on `refs/pull/84/head` none; open alerts on the PR ref 0, on main 0. The `state=fixed` count command failed (my `paste | bc` pipeline), so there is no control number in the brief; the brief tells the gate to count it.
- Tools: `/opt/homebrew/bin/pdftotext`, `pdfinfo`, `pdftoppm` present; `mutool` and `gs` absent (`which`, 19:57). `docker image ls` shows pc-b323-node:head, pc-b331-node:head/base, pc-b333-*, pc-b335-*, pc-b320-*, pc-b322-*, pc-b301-* exist, none pc-b341-*.
- `apps/api/test` has 74 `db.test` files and `packages/db/test` 23 test files at head (git ls-tree counts); DB route is `scripts/test-db.sh` (internal network, per-run password, `rm -f -v` cleanup) read at lines 1-28 only; `scripts/common.sh` not read. `git diff --stat d8d2a2c7 0f64aee7 -- apps/api` = 1 file, 5 insertions, 4 deletions. `vitest.config.ts` has projects `renderers` and `workspace`; db tests run separately.
- C-86..C-96 are now present in `1_Project_Definition/CLARIFICATIONS.md` (lines 1593-1725), so the brief states K1-K10 as ruled and in the file (the B323 builder brief said local only).

## Port block and its grep
**7640-7649.** `lsof -nP -iTCP:7630-7699 -sTCP:LISTEN` rc 1 (19:57). `grep -E '\b764[0-9]\b'` over `briefs/2026-10-20_*`: 0 files; also 765x to 770x 0. The `NNNN-NNNN` ranges named by today's briefs run from 7230 up to a highest end of 7629 (7550-7619 is a B333/B335 range, 7620-7629 and 7630-7639 named by 11 briefs, 7570-7579 B335's). The brief says it is a reserve only, nothing publishes a port.

## Design choices (where I went beyond the B331 template)
- Added "WHAT THIS GATE MUST ESTABLISH (a-j)" mirroring the commission and a severity floor tuned to a customer-facing PDF (a false page number is a Blocker).
- The page-number proof (r1) uses poppler only, with bbox-layout to tell the 13 pt heading line from the contents line, plus an independent oracle: heading page in the BASE render of the same fixture plus the pages the contents take must equal the printed number (works when the contents flow is the only change; the gate must say where it does not hold).
- Extra fixtures beyond the commission's two: a contents list that spills onto page 3 (the builder's STATUS lists this NOT TESTED), zero-heading spec, repeated/nested titles, boundary headings, long token and non-ASCII title.
- DB test rows A-D: pre-edit file over the head image (valid because `e783cc3..0f64aee7` touches only that file, which the gate proves), head file over head, base file over base image (route control), head file over base image (edit not vacuous); row E: find other PDF-page readers in the db suites by program (the builder named eight and did not run the rest).
- Mutants M1 to M8; the page-number arithmetic lives in pdfmake not the repo, so M1 has two variants (an extra blank page; a patched read-only pdfmake copy mounted for one run, kept under the `-mut` tree). This stretches "in a -mut tree only"; see Q3.
- Non-policy bytes (r4b) are measured on the gate's own scenarios from the repo's s41 generate path, base vs head, each twice; the `package_manifest` diff must be exactly the PDF's sha256 and template_version.

## Disagreements (source wins)
1. Your task said base `d8d2a2c7`; the GitHub API says `base.sha` is `318df176`. Both are right in their sense (merge-base is `d8d2a2c7`); the brief uses `d8d2a2c7` for the PR's own diff and `318df176` for the merge row.
2. Task said head has 3 commits, 11 files: confirmed. Task said main is `318df176` "only two test files outside #84's paths": confirmed.
3. The builder's STATUS says renderers base 238 tests vs "252" final, 14 new: consistent; no mismatch to grade. (The B331 count mismatch had no analogue here.)
4. Builder's STATUS line 4 says "I could not run the DB suite" then ANSWER-1 later ran it; the end of the file is authoritative, the brief quotes the later state.
5. The commit time zone: commits print +1100 (git), while my clock is AEDT; both are the same local time, no issue.

## Open questions with recommended answers
1. **PC_E8_SOW_TEXT for the unit step of ci:node.** Recommend: confirmed as at B320/B331 (Composer is Datasec's own product), passed by docker cp or read-only mount, never opened.
2. **Launch while B335 is mid-run?** Recommend: launch when load1 is below 7 (as you did for B331); the gate's own LOAD rule makes it wait for any pc-b335 job. If B335 runs for hours, expect the heavy rows to sit idle; consider launching after B335's verdict.
3. **M1's patched-pdfmake variant overlays one library file read-only for a single run (kept under the -mut tree, image untouched).** Recommend: allow; without it the off-by-one in the number the commission names cannot be a repo mutant.
4. **Brief size (51 KB vs 40 KB aim).** Recommend: accept; the cuts that would reach 40 KB are the r4 scenarios and the r6 split, which are the gate's value. If you prefer, drop mutants M7 and M8 and the PR #83 reader grep.
5. **Model:** the builder was Sonnet; the gate is Opus per G1. No question.
6. **Round framing:** a NO GO on the false-page-number class goes back to a builder; recommend Sonnet again with the failing PDF named, since the code is one block.
7. **"Contents" word card:** Tuesday's to open (K9); the gate approves nothing.
