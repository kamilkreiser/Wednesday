Spark shadow gate 289 (PR 2133 / PR 2134): PR 2133 verdict GO WITH NOTES (Claude: GO WITH NOTES, match); PR 2134 verdict GO WITH NOTES (Claude: GO, same direction, label differs); recall 0/1 substantive findings (G289-2133-1 missed; 2134 has no substantive finding); FP 0 false at source (about 7 padding Notes)

# Calibration row, 2026-11-09 ~19:0x, tier-2 shadow of gate 289 (Claude verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate289-tier2-pr2133-pr2134/verdict.md)
Method: spark_gate.sh then spark_review.py, as in the 2127 shadow. The Claude verdict was written BEFORE the Spark ran (so not blind in the strict sense; the Spark saw none of it). Spark tunnel UP (spark_status.py, queue 0). Repo clone and worktrees under the scratchpad; evidence in <scratchpad>/sp/{o2133,r2133,o2134b,r2134b}/. Inputs fed to the review: the seat's saved full ticket text and final PR body (pre-fetched, labelled; no real .env, no Linear call). Base ref `develop` (not `origin/develop`).

## Deterministic half
- PR 2133: head 8 passed 0 failed; BASE product code (merge-base 6beac873... suite file of the head against the base product) 8 passed 0 failed. Matches my own run (develop 6 passed with the OLD suite, PR head 8 passed). Pin behaviour is correct: new cells are green on base product.
- PR 2134: FIRST RUN INVALID. `--node-modules <api-gateway/node_modules copy>` gave `sh: vitest: command not found`; facts.json recorded files_failed 1, passed 0, failed 0 on HEAD AND BASE, rc 0, and the review ran on it (r2134 discarded). Rerun with `--node-modules <Dev/node_modules>` (the dir that holds .bin/vitest): head 6 passed 0 failed, base product 6 passed 0 failed. Matches mine (4 to 6, pins green on develop). The second run is the one scored.

## Spark review half
- PR 2133: 8224 prompt tokens, 512 completion, 25.5 s, one attempt, valid JSON. GO WITH NOTES, 3 Notes. 
- PR 2134 (valid facts): 7364 prompt, 1401 completion, 46.2 s, one attempt, valid. GO WITH NOTES, 9 Notes.
- Missing inputs: none.

## Scoring against gate 289
| id | sev | Spark | note |
|---|---|---|---|
| G289-2133-1 pattern `secuura-nginx-gateway:6882` narrower than the ticket's `nginx-gateway:6882`; plants `nginx-gateway:6882` / `host.docker.internal:6882` stay green | Low | MISSED | needs the ticket's fix-shape text against the grep literal; the ticket was in the prompt; the Spark read the cells as "grep -c ... 0" and did not compare the pattern with the ticket |
| G289-2133-2 held vs PR differ only in diff framing | Info | n/a | the held patch was not an input |
| G289-2134-1 whole-suite not reproducible by me | Info | n/a | environment fact, needs running; the Spark repeated the seat's 1880 to 1882 as supported (its Note 7) |
| G289-2134-2 scope one cell wider than ticket; stale "pinned by no cell" tense | Info | MISSED | |
| G289-2134-3 held vs PR framing | Info | n/a | |
Verdicts: PR 2133 match. PR 2134: Spark GO WITH NOTES vs Claude GO (both non-blocking; Claude's notes were all Info). Facts: match (8/8, 6/6, base also green).

## Spark's own findings, checked at source
PR 2133: (1) Note, cells green on base as well as head, blindness claim not re-measured: TRUE and by design (PR body says so); my M1-on-develop control re-measured the blindness (6 of 6 green). Low value padding. (2) Note, preflight 13/16 legs and unticked boxes: TRUE, disclosed in PR body. Padding. (3) Note, shipped example files not among inputs (template_siblings included []): TRUE as a statement about the inputs; the files exist and were read by me; Low value.
PR 2134: (1) no product code changed: TRUE, padding. (2) root cause measured by plants: TRUE (self-reported, I reproduced). (3) no real AbortController path: TRUE, same as ticket and PR. (4) green on base: TRUE, by design. (5) stub fetch is faithful but not a real timeout: TRUE restatement. (6) no template relevant: TRUE, padding. (7) "whole api-gateway suite 1880 to 1882, no new failures": taken from the PR body, not in facts.json (facts have only the one file, 6/0); it presents a seat claim as supported; I could not reproduce a clean whole suite either (identical failure sets, passed +2). Mildly over-reaching, not false. (8) pre-merge boxes/preflight: TRUE, padding. (9) byte-equal and sha256 claims are self-reported, not in facts: TRUE and fair as UNMEASURED; my diff against the held patch confirmed the content equal.
Quotes: evidence_quote_found_in_input true throughout on 2133; no overstated comment sentences on either. False positives: 0. Padding: 3 of 3 (2133) and about 6 of 9 (2134) restate that the change is test-only, green on base, or disclosed.

## What the tooling or checklist should change
1. spark_gate.sh / shadow_facts.py: a non-pytest run with `files_failed >= 1` and passed + failed = 0 (here `vitest: command not found`) must exit non-zero or write `facts.run_valid=false`; today it exits 0 with a facts.json that LOOKS like a clean 0/0 and the review proceeds on it. The `--node-modules` help should say "the dir that holds .bin/vitest (the Dev root node_modules)", or the tool should check `<dir>/.bin/vitest` before running.
2. REVIEW_CHECKLIST.md: for a count-style or grep-pattern cell, add "compare the literal in the cell with the ticket's stated fix shape and name any difference (narrower or wider) as a Note". That is the only substantive point this row had and the Spark did not make it.
3. spark_review.py: reject a Note whose evidence is only the PR's own declared limitation ("disclosed, not a defect"); these were 4 of 12 Notes and carry no information. Also tag a finding that restates a PR-body number as "from PR body, not in facts" (PR 2134 Note 7).
4. Verdict rule for test-only pins: when every Note is Info-class or a restatement, the label should be GO rather than GO WITH NOTES; otherwise the label carries no signal (both Spark verdicts here are GO WITH NOTES with zero actionable content).

Running tier-2 record (this row): usable. Direction right on both PRs (no false NO GO, no missed Blocker; neither PR had one). Substantive recall 0 of 1 (a Low).

Conduct: nothing written under /Volumes/DevMASTER/!CODING; no push/post/mail; no .env opened; no rm. Scratchpad total about 2.7 GB (clone .git 190 MB plus several full worktrees and copied node_modules); df DevMASTER start 99 Gi free, end 99 Gi free. Spark answered throughout; load1 was 5.6-9 during the runs (one start at 9.3 was waited out).
