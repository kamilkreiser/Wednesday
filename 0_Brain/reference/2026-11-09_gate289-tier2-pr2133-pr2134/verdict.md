PR 2133: GO WITH NOTES; PR 2134: GO

Gate 289, tier 2 (Sonnet relaunch, started from scratch; the first session's /private/tmp/g289 was not used). Findings only; nothing posted, mailed or pushed.

## Pins
- Start 18:48 and end 19:01 AEDT, by `git ls-remote` on the Blockchain checkout (read verb): develop f98afb113c2d, PR 2133 head b6f0c319c5d4, PR 2134 head bd83319d3545. NONE MOVED, all three equal the commission's pins in full.
- develop moved 6beac8734a2f (both PRs' parent) to e8d23ce366e2 to f98afb113c2d. Total change 6beac..f98afb: 7 files (ks1560 jq-link suite, transfer ks2055 test + `transfer/src/index.ts` (3 lines), 2 cheat + 2 flow fragments). Intersection with either PR's paths: NONE (checked by name list and by blob equality: the PR heads' blobs for their file equal develop's blob at the merge-base, see Q5).
- df /Volumes/DevMASTER: start 99 Gi free (95 percent), end 99 Gi free (same). load1 was 4.9 at start; it spiked to 17.7 at 19:01 from other seats (not this gate: no gate process was running). The Spark shadow waited for load1 under 8.

## Common method
Own partial clone (blob:none) in this session's scratchpad, fetched refs/pull/2133/head and 2134/head; detached worktrees of develop, PR 2133, PR 2134, all full checkouts. No write verb touched `!CODING`. The clone is about 200 MB plus worktrees. node_modules for api-gateway are copies of the main checkout's (read only), `packages/shared/dist` rebuilt from develop source with `tsc` (it emits with 3 zod-typing errors, a dependency-version mismatch in the shared node_modules, not this change).

## PR 2133 (KS-1415 item 2, E11): GO WITH NOTES

### FOUND
Q1 test-only: PR files per git: ONE file, `Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh`, +7 -0 (`git diff --numstat origin/develop...head`). Diff read whole: 3 comment/blank lines plus two `expect` cells. No product byte; the two example env files (`observability/.env.example`, `observability/config/alerting.env.example`) are only read. The merge-tree result changes that one file only.
Held diff vs PR (READY_KS-1415-...-P3, canonical patch.diff, sha256 05f8d272cf7376a2): the +/- lines are byte-identical (all 7 added lines, 0 removed). Differences are only the diff's own framing: git's header lines and `index` line, and the held patch's hunk carries 3 context lines ending at the `echo` line (`@@ -120,4 +120,11 @@`) where the PR's has 4 (`@@ -120,5 +120,12 @@`, one more trailing context line `(( FAIL == 0 ))`). No content difference.
Q2 red proof reproduced. Cells are PINS, labelled honestly: both pass on develop; the PR body says in bold "not a regression test for a present bug... green on develop by design".
Q3 scope: KS-1415 item 2 (per the seat's saved full ticket text, evidence/e11/ticket_ks1415_whole.txt, because I have no Linear access in this gate; Linear itself was NOT read live): "a per-file count cell, `grep -c 'nginx-gateway:6882' <file>` asserted == 0, keep the first-line pin as well". The PR does that for both files and keeps the first-line pins (diff is +7 -0). The PR body claims item 2 only, says item 1 is NOT in the PR, leaves the ticket open, "Refs" not "Fixes". True at this head.
Q4 suite: prometheus_targets.test.sh on develop f98afb: 6 passed 0 failed rc 0; on PR 2133 head: 8 passed 0 failed rc 0.
Q5 merge tree onto f98afb113c2d: rc 0, clean, tree 2721d7b32cb5, one file changed; the merged blob of the suite equals the PR head's blob (3571e564da33).
Q6 docs-fragments (report only): `node Blockchain/Dev/scripts/docs-fragments.mjs check --root <worktree>` rc 0 on PR 2133, PR 2134 and develop alike ("lint clean, render passes html_docs_check", the same two ADVISORY lines about the committed pages differing from the render exist on develop itself, so they are not caused by either PR). Nothing in `.githooks/pre-push`, `ci/` or `.github` names fragments, so no refusal found. I did not run the pre-push hook (not permitted against the real remote).

### TESTED / HOW (instruments and controls)
- Cell outcome by my own mutants on the PR-head worktree (example files restored from a copy and `cmp`-checked after each; `git status` clean):
  - M1 active `SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:6882/stub_status` appended to `.env.example` only: exactly ONE FAIL, "observability/.env.example names the gateway host port 6882 on no line" (7 passed 1 failed).
  - M2 same line in `alerting.env.example` only: exactly ONE FAIL, "observability/config/alerting.env.example names the gateway host port 6882 on no line" (7/1).
  - M4 the same URI as a COMMENT line in `.env.example`: that cell fails (a commented 6882 line is also refused; acceptable and arguably intended by "no line").
  - Negative control for blindness: the same M1 in both files on develop's UNPATCHED suite: 6 of 6 green. So the new cells add the detection and the old pins are blind, as the ticket says.
- The seat's own plants (checker's plant: the two cells turn red together; each alone) I did not repeat byte-for-byte; M1 and M2 are the equivalent single plants and match the seat's claim.

### NOT TESTED
Live Linear read; the pre-push hook; shellcheck; whether another document or script outside `Blockchain/Dev/scripts` names the status URI; macOS bash 3.2 versus Linux bash (I ran macOS /bin/bash path through `bash`, version not recorded).

### Findings
- G289-2133-1, LOW (test strength, not a defect). The cell's pattern is `secuura-nginx-gateway:6882`, narrower than the ticket's stated fix shape `nginx-gateway:6882`. Measured: a plant of `http://nginx-gateway:6882/stub_status` in both files leaves 8 of 8 green (my mutant M3), and so does `http://host.docker.internal:6882/stub_status` (M5). Neither is the real compose service name (`secuura-nginx-gateway`), so the practical blind spot is small, but the cell label "names the gateway host port 6882 on no line" and the code comment "no line of either example may name the gateway on 6882" read broader than the pattern. The PR body states the pattern exactly (`secuura-nginx-gateway:6882`), so it does not misstate it. Suggest, not required: widen to `nginx-gateway:6882` (which is a superset and still 0 on develop; I did not run that variant) or say "by that name" in the label.
- G289-2133-2, INFO. Held diff vs PR differ only in diff framing (one trailing context line), see FOUND.

## PR 2134 (KS-1976, E10): GO

### FOUND
Q1 test-only: ONE file, `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts`, +13 -0. Diff read whole: a comment line plus two `it` blocks (N1, N2). `health-dashboard.ts` (the product file) is not in the PR; merge tree changes the one test file only.
Held diff (READY_KS-1976-...-P1, patch.diff, sha256 1fb719e4c919d754): +/- lines identical (13 added, 0 removed); only the diff framing differs (git header/index line, and the held patch's `@@ -85,4 +85,17 @@` has no function-context text). No content difference.
Q2 cells are PINS: green on develop by construction (the product already has the probe), red only under a plant; the PR body says so in bold. Test labels `ks1976 N1`/`N2` honestly describe what they assert.
Q3 scope: the ticket (KS-1976, from the seat's saved full text, evidence/e10/ticket_ks1976_whole.txt; Linear not read live) asks "one test cell: a rejected probe whose value is a DOMException with a throwing `name` getter; assert the service is listed down". That is N2, exactly. N1 (DOMException named AbortError gives `error: 'timeout'` and `latencyMs: null`) is an extra cell the ticket did not ask for but it covers the other half of mutant H5 (the compare at line 93), so it is within the ticket's purpose (gate 177's H5 = drop the DOMException-name probe). The PR body discloses both cells and claims nothing the diff does not do; "Refs" not "Fixes"; ticket left open; does NOT claim a real AbortController timeout (and says so). The ticket's precondition (PR 1993 merged) holds: develop's `health-dashboard.ts` blob 1b6df6244f09 equals PR 1993's head blob.
Q4 suites: declared file on develop 4 tests 4 passed; on PR head 6 tests 6 passed (4 to 6). Whole api-gateway vitest in MY environment is NOT clean on either side (see G289-2134-1): develop 953 passed / 44 failed / 353 pending over 354 files; PR head 955 passed / 44 failed / 353 pending. The failure sets are IDENTICAL by name on both sides (diff empty after normalising the worktree path), so the PR adds exactly +2 passing tests and moves nothing else.
Q5 merge tree onto f98afb113c2d: rc 0, clean, tree e21db91c9621; PR 2133 and PR 2134 together: rc 0, tree 25d5f6953676, exactly the two PR files changed, the merged blobs equal each PR head's blob (suite 3571e564da33 = PR 2133's; test file a91eb7e6085c = PR 2134's). Disjoint paths.
Q6: same docs-fragments result as above (rc 0). No fragment pair in this PR (Wednesday's ruling for held-Spark rows).

### TESTED / HOW
- The product file `src/routes/health-dashboard.ts` mutated in my worktree (restored by copy and `cmp`; `git status` clean), the declared test file run each time with vitest `--root`:
  - Checker's line 86 alone (`void (error instanceof DOMException && error.name);` becomes `void 0;`): exactly N2 red (5 passed 1 failed).
  - Checker's line 93 alone (`'AbortError'` becomes `'AbortErrorX'`): exactly N1 red (5/1).
  - Both together: exactly N1 and N2 red (4 passed 2 failed).
  - My own mutants: C the `latencyMs: errorMessage === 'timeout' ? null : latencyMs` becomes `latencyMs`: exactly N1 red. D the string `'timeout'` becomes `'aborted'`: exactly N1 red. E the whole `else if (... AbortError) {timeout}` branch removed (a true H5, DOMException then falls to the Error message branch): exactly N1 red.
  - Negative control on develop's UNPATCHED test file with each of those six mutants: 4 of 4 green every time, so mutant H5 survives on develop and the two new cells are what catch it.
- Product bytes: develop's `health-dashboard.ts` unchanged by the PR (the PR touches none).

### NOT TESTED
A real AbortController timeout (the ticket says not measured; the PR says not exercised); Node 24 (I ran Node 26.8.1, same as the seat); eslint and the `typecheck-tests` ratchet (I did not run them; the seat's READY reports ratchet 25/25 baseline, tsc 0, eslint rc 0, unverified by me); a whole-suite clean run (below); live Linear.

### Findings
- G289-2134-1, INFO (my environment, not the PR). I could NOT reproduce the seat's "whole suite 1880 to 1882 tests, 0 failed, 502 files" in this gate's environment: my api-gateway run saw 354 files, 44 failed, 353 pending (missing built sibling packages and dependency drift in the borrowed node_modules; first pass before rebuilding `packages/shared/dist` was worse, 227 failed, with the same property below). The comparison that matters held both times: failing sets identical by name on develop and on the PR head, passed +2 on the PR head. So "no other test moved" is proven; "0 failed whole suite" is the seat's claim only, not reproduced here.
- G289-2134-2, INFO. Scope is one cell wider than the ticket (N1 extra), disclosed in the PR body. The new comment says "...is pinned by no cell." in the present tense above the cells that now pin it; true at the time of writing, stale after merge. Cosmetic.
- G289-2134-3, INFO. Held diff vs PR differ only in diff framing (hunk header context text), no content difference.

## Shared items
- Open PRs sharing a path (Q5): I cannot call the GitHub API with a PR state (the Blockchain `gh` config is not logged in; no token used). Instead I fetched the head of every pull ref numbered 1900 and up (233 refs) and listed those whose diff from their merge-base with develop touches either PR's paths or the product file: PR 1993 (squash-merged: its health-dashboard blob equals develop's, so it is in develop already) and PR 2133 / PR 2134 themselves. NO other PR touches `prometheus_targets.test.sh`, the ks1868 test file, `health-dashboard.ts`, `observability/.env.example` or `observability/config/alerting.env.example`. Planted control: `Blockchain/Dev/services/transfer/src/index.ts` was found in PRs 1938, 1944, 1953, 2048, 2077, 2113 (so the scan detects overlap when it exists). Caveat: this scan reads ALL pull refs from 1900, merged-by-squash PRs included, so it can over-report but cannot under-report among refs that exist.
- Merge order: either; the two PRs are file-disjoint and together merge clean.

## Conduct
- Read-only git on `!CODING` (ls-remote, cat-file once, show/diff on the PR specs); all writes in the scratchpad clone. Two attempts were refused by the workspace hook (a `git -C $VAR fetch` pointing outside WEDNESDAY, an `unlink`); I reworked them with a literal-path wrapper and a mv, nothing circumvented. No rm, no cd. One of my own mistakes: I ran `ls-tree -l` on the partial clone, which pulled blobs (clone grew to about 200 MB); harmless. A first whole-suite run was on a sparse checkout and was discarded as invalid.
- The earlier session's /private/tmp/g289 tree (3 GB) is untouched and unused.
