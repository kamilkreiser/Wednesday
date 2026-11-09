Spark shadow gate 297: PR 2148 GO, PR 2149 GO WITH NOTES, PR 2151 GO WITH NOTES (Claude: GO WITH NOTES x3; verdict match 2 of 3, 2148 one grade lighter); recall 0 of 7 of the Claude findings (1 touched the same sentence, different point); FP 0 false at source (3 weak/unevidenced Notes, listed)

# Spark shadow calibration, 2026-11-10 ~08:2x: PRs 2148, 2149, 2151 (tier 2), against verdict.md in this folder
Method: Spark run AFTER my verdict was written (not blind to it for me, blind for the Spark). Clone: this session's scratchpad `r` (blobless, sparse). Tunnel: `tunnel.sh check` said DOWN once (http 000, listener present) at 08:20 and `curl` 200 seconds later; no box touched. Model deepseek-v4-flash-0731, SPARK_THINK 0.
- 2149: `spark_gate.sh <clone> 2149 <sha> develop <test> --node-modules <Dev/node_modules>`; facts head 33/33, base-product 33/33 (right: the cells are pins; matches my 28 to 33, red 0).
- 2151: same, .sh suite; head and base both rc 0, `count_unparsed` (the suite prints `passed=27 failed=0`, not `N passed, M failed`).
- 2148: NO test file exists, and `spark_gate.sh` requires one: facts.json was HAND-BUILT by this session (touched file, diff, not_run says so). Diff = merge-base..head.
- `spark_review.py` per PR with `--pr-body-file` = the seat's saved `.final` body; ticket text MISSING for all three (no Linear tool); no `--comment`. Evidence: `.../scratchpad/sp/{o2148,o2149b,o2151,rv2148,rv2149b,rv2151}` (facts, diff, prompt_user.txt, raw_attempt1.txt, review.json).
- Runtime: prompt 5,663 / 8,806 / 11,086 tokens, completion 533 / 503 / 369, 27.2 / 23.1 / 21.3 s, one attempt each, valid JSON, no repetition. Deterministic half 17 to 28 s per PR.

## Verdict match
| PR | Spark | Claude (gate 297) | match |
|---|---|---|---|
| 2148 | GO (4 Notes) | GO WITH NOTES (2 Low) | one grade lighter: it missed both Lows |
| 2149 | GO WITH NOTES (4 Notes) | GO WITH NOTES | match |
| 2151 | GO WITH NOTES (3 Notes) | GO WITH NOTES | match |

## Recall of the Claude findings
| id | sev | Spark | note |
|---|---|---|---|
| G297-2148-1 "0 of 16 super-admin-only" wider than what the 16 counts, no date/version | Low | MISSED | Spark Note 2 actually praised the body for labelling the figure UNMEASURED; it never saw harReplay.ts:333 ("0 of 16 relative endpoints") because the prompt carries the diff, the touched file and cited lines, not that sibling comment. |
| G297-2148-2 "every endpoint" is GET-only; wrong password also gives null | Low | MISSED | needs harTraffic.ts header and secuuraAuth.ts, outside the prompt. |
| G297-2149-1 ADMIN row titled RED but green on develop | Low | MISSED | Spark Note 4 says the cells are PINs (true) and does not see the one row that keeps a RED title; facts show 33/33 on head and base, which is where the inconsistency is visible. |
| G297-2149-2 type cells do not assert the REFUSAL body | Info | MISSED | |
| G297-2149-3 body names KS-1448 hyphenated twice against its own spacing note | Info | MISSED | the PR body WAS in the prompt; the Spark did not read the Notes against the text. |
| G297-2151-1 `bundledDependencies` spelling accepted but pinned by no cell | Low | PARTLY / different point | Spark Note 3: "the bundledDependencies measurement is not in the facts" (true) but it asked for evidence, not for the missing cell; the real gap (mutant m3 leaves 27 of 27) was not found. |
| G297-2151-2 one real-tree cell does all the red | Info | MISSED | |
Recall: 0 of 7 found, 1 partly (G297-2151-1). Nothing above Low in this round, so no Blocker/Major was at stake.

## The Spark's own findings, checked at source
2148
1. Note: ticket text missing, acceptance not assessed. TRUE (input absent). Instructed Note (checklist D.10), not a finding about the PR.
2. Note: PR description present, no overstated sentences. TRUE as far as it goes; it is a statement of no finding.
3. Note: comment-only, blast radius n/a. TRUE (my numstat and non-comment hash).
4. Note: "the comment-only proof is not in facts.json". TRUE but low value: I reproduced the proof myself (sha256 prefix c94297c0ba45f391 both sides, 42 lines). Not a false positive.
2149
1. Note: ticket missing. TRUE, instructed.
2. Note: "SCOPED_ADMIN_ROLES real spelling" has no evidence in facts. The claim is TRUE at source (`packages/shared/src/security/keyRevokePolicy.ts:94`, `new Set(['ADMIN'])`); the Note is a request for evidence, correctly scoped, not a false claim.
3. Note: the other three type cells have no measured mutant. TRUE of the PR body; I ran them (P3 to P5, each exactly one red), so the gap closes. A real, well-aimed Note: best finding of the round.
4. Note: the cells pass on base and head (PINs). TRUE (28 to 33, 33 on base-product run). `evidence_quote_found_in_input` false for this one (the quoted figure is paraphrased), flag raised by the tool.
2151
1. Note: ticket missing. TRUE, instructed.
2. Note: "claimed 25 vs 27 not in facts; base and head both read passed=27". Half right: the tool's "base product code" run executes the PR's suite on the base product tree, so 27 there is expected and 25 is the DEVELOP suite, which the runner does not run; the Note reads that as a gap in the evidence, not a contradiction. Mild misread of the tool's own `targeted_on_base_product_code` meaning; no false claim about the PR.
3. Note: bundledDependencies measurement not in facts. TRUE (the seat's plant is in the body only; I reproduced it as plant C). Touches G297-2151-1's sentence but not its point.
False positives: 0 false at source. Evidence-quote flag was false on 5 of 11 Notes (the tool's own check), all paraphrases, none fabricated facts.

## What the tool or checklist should change (instruction or tooling fix)
1. `spark_gate.sh` `--node-modules` must point at the HOISTED root `Blockchain/Dev/node_modules`, not `services/api-gateway/node_modules` (which has no `.bin`): with the package one the head and base runs print `sh: vitest: command not found`, `files_failed 1`, `passed 0` and the run is still written as facts. The usage line should say so and the tool should refuse (exit 4) when a vitest file ends rc 127 instead of recording 0 of 0.
2. `shadow_facts.py` does not parse the `passed=N failed=M` summary that the portals suite and its siblings print; add it, so shell suites stop reading `count_unparsed` (the 2151 Note 2 came from this).
3. No path for a comment-only or doc-only PR with no test file: `spark_gate.sh` requires at least one. Add `--no-tests` (diff, touched files, merge-base only, `not_run` filled) rather than a hand-built facts.json.
4. Recall gap (2148-1, 2148-2): the review prompt carries the diff, touched files and lines CITED by the PR/comment, not a sibling comment that already quotes the same figure or the code the new comment describes. For a comment-only PR the checklist should say: take each code-fact claim in the new text (file and line) and read it from the cited line; the prompt builder could pull the files named in the added lines (`harTraffic.ts`, `harReplay.ts`) as cited sources. Without that, a documentation PR cannot be checked for over-wide wording.
5. Recall gap (2151-1, 2149-1): the checklist should ask, for a test PR, "is every behaviour added by the product-side line pinned by a cell, and does every cell title match its measured red/green state on base". Both were visible from the diff and facts alone.
6. The Spark's best Note (2149-3) came from reading the body's own admission against the facts: the body-versus-facts comparison is where it works; the code-versus-claim comparison is where it did not.
