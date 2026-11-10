# Spark shadow of gate 305 (PRs 2163, 2164, 2165), 2026-11-10 ~16:4x
Method: blind (Spark run after my verdict.md was written; I did not read the Spark output first). Tunnel UP by spark_status.py (queue 0). Tool: spark_gate.sh (deterministic half) then spark_review.py, base ref `develop`, inputs pre-fetched read-only (ticket text from Linear, PR body from the GitHub API, passed as --ticket-file / --pr-body-file; no .env passed to the tool). Clone: scratchpad g305 (2.2G with node_modules), outputs in scratchpad spark/{o,r}<pr>/ (facts.json, diff.patch, review.json). Spark: deepseek-v4-flash-0731, one attempt each, valid JSON, no repetition.

## Spark shadow PR 2163: verdict GO WITH NOTES (mine GO WITH NOTES, match); recall 0/2 of G305-2163 findings; FP 2 of 5
Deterministic half: rc 0 but the facts are WRONG for this suite: head `0 passed, 1 failed (aborted)` and base the same, because the ks949 suite dies with `FAIL packages/shared is not built (...dist/index.js missing)`: the tool's fresh worktree has no gitignored build output and `--node-modules` is only linked into vitest package dirs, not Dev root. My own run (shared built, Homebrew Postgres): develop 27/27, head 28/28. The Spark saw the FAIL tail in its prompt (3 occurrences) and did not mention it; its verdict is right by luck of the shape, not because it read the facts.
| id | Spark | note |
|---|---|---|
| G305-2163-1 (Note: id-arm-only guard still green) | MISSED | |
| G305-2163-2 (process, merge base one behind) | MISSED | needs the READY |
Spark findings checked at source: (1) Note "seat's red proof not in facts.json": TRUE and fair (facts carry no plant). (2) Note "item 1 unaddressed, as the PR states": TRUE, restates the body. (3) Note "does not verify the WHERE is the two-arm guard, only the observable effect": TRUE but that is the point of a behaviour cell; low value. (4) Note "does not assert tenant_id untouched": FALSE/misses the construction (the plant UPDATE writes only tenant_slug, so tenant_id is untouched by construction). FP. (5) duplicate of (3): FP (padding).
## Spark shadow PR 2164: verdict GO WITH NOTES (mine GO WITH NOTES, match); recall 2/3 partly (G305-2164-1 partly, -3 partly, -2 missed); FP 1 of 4
Deterministic half: head 13/13 (matches mine), base 13/13 (the tool runs the PR's own test file on base PRODUCT code, and a test-only PR has no product change, so base == head by design; mine: develop 11/11, head 13/13).
| id | Spark | note |
|---|---|---|
| G305-2164-1 (cells are SETUP assertions, not product pins) | PARTLY (Spark 2: red proof is a planted `true`, not a real load failure) | |
| G305-2164-2 (rev-parse true if TMP is inside a work tree) | MISSED | |
| G305-2164-3 (suite continues, hook still refuses, clearer message) | PARTLY (Spark 3: exit code unchanged, hook still refuses) | |
Spark findings at source: (1) restates the body, TRUE. (2) TRUE (the body says so). (3) TRUE (existing FAIL accounting still returns rc 1). (4) "facts show base 13 passed, contradicting the PR's 11": FALSE, a tool-artefact misread (see above); FP, tool-induced.
## Spark shadow PR 2165: verdict GO WITH NOTES (mine GO WITH NOTES, match); recall 1/6 (G305-2165-4 found; -1,-2,-3,-5,-6 missed); FP 3 of 6
Deterministic half: head 11/11, BASE product code with the PR's test 8 passed 3 failed: matches mine exactly (R1-R3 red). The one product-PR case where the tool's base-vs-head design does give the red proof.
| id | Spark | note |
|---|---|---|
| G305-2165-1 (second caller, CredentialDetailModal) | MISSED | context outside the diff, not in the prompt |
| G305-2165-2 (RED in permanent cell names) | MISSED | |
| G305-2165-3 (develop THREW on undefined/null) | MISSED | needs a run, the Spark cannot run code |
| G305-2165-4 (negative/NaN unpinned, body discloses) | FOUND (Spark 5) | |
| G305-2165-5 (prettier flag) | MISSED | |
| G305-2165-6 (symlink environment) | MISSED | outside the diff |
Spark findings at source: (1) scope only the issuer half: TRUE, the body says so. (2) root cause in DocumentDetail unfixed: TRUE, the body says so. (3) cells test the card, not the data flow from DocumentDetail: TRUE, low value. (4) "red-first base failure is due to new tests expecting new behaviour, not a regression": a misreading of what red-first means; FP. (5) found. (6) "claim that it 'fixes' the ticket is overstated": FALSE, the body says Refs and leaves the ticket open; FP.
## What the tool or checklist should change
1. spark_gate.sh / shadow_facts.py: a bash suite that dies on a missing gitignored build (`packages/shared is not built`) writes facts head 0/1 and base 0/1 as if measured. It should detect `is not built` / `not installed` setup aborts and put a REFUSAL line (not a fail count) into facts, and link the Dev-root node_modules and run `npm run build -w packages/shared` for Blockchain/Dev bash suites. A model asked to review facts that say head FAILED must be told by the tool, not left to notice.
2. spark_review.py: when facts head failed, the prompt should carry a mandatory first line "HEAD FAILED IN THE TOOL'S RUN" so the verdict cannot be GO without addressing it (2163 prompt held it three times and the Spark ignored it).
3. Test-only PRs: base == head in the tool by design, so "base 13/13" invites a misread (Spark 2164 finding 4). The facts should state `test_only: base run is the PR's test on unchanged product, expected equal`.
4. Context builder: for a product PR add the callers of a changed component (grep of the import) as prompt context; the second caller in PR 2165 was the only product-behaviour finding and the Spark could not see it.
5. Padding: duplicate findings (2163 #3 and #5) should be merged by the post-process, as in calibration 6 item 7.
Conduct: nothing written under !CODING; no push, post, comment, mail; no real .env value printed (the Secuura .env was read by an in-process script for the Linear and GitHub reads only). Spark answered throughout (35 to 54 s per review, 10k to 16k prompt tokens). Scratchpad: g305 2.2G, spark 745M.
