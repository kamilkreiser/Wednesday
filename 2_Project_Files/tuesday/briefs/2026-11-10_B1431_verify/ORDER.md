ORDER: landing order across every pushed, not-yet-merged NexusAI lane branch of the 2026-11-10 sweep (12 branches), main 849b808c

This file sets the order only. Except for the four B1431 branches (see VERDICT-*.md), these branches are gated by other gates. Measured 2026-11-11 01:2x AEDT in my own scratch clone (push URL invalid, never pushed).

## The branches (ls-remote origin, re-read just before writing)
| key | branch | head | base | files | counts commit on branch | expected counts on main 849b808c (tests/suites) | source of the count |
|---|---|---|---|---|---|---|---|
| T-csp | b1431/nexusai-t-csp-tool-edge-cases | e6addceb | 3929b794 | 4 | no | 5520/328 (+27/+2) | MEASURED here (merge tree) |
| T-ci | b1431/nexusai-t-ci-actions-browser-assert | c79e2e88 | 3929b794 | 7 | no | 5507/328 (+14/+2) | MEASURED here |
| T-smtp | b1431/nexusai-t-smtp-route-cells-standalone | 857843e4 | 849b808c | 2 | no | 5501/327 (+8/+1) | MEASURED here |
| T-archive | b1431/nexusai-t-suites-pass-from-git-archive | 52df6468 | 849b808c | 15 | no | 5497/327 (+4/+1) | MEASURED here |
| F-header | b1432/nexusai-f-shell-layout-header | 5cc88abe | 3929b794 | 2 | no | 5494/327 (+1/+1) | RELAYED, B1432 STATUS:107,135 |
| F-overflow | b1432/nexusai-f-overflow-settings-390-printing-820 | a1d7f46d | 3929b794 | 4 | no | 5493/326 (+0/+0) | RELAYED, B1432 STATUS:106,128 |
| B-cspintake | b1433/nexusai-b-csp-intake-edges-and-typed-fields | 3a5d3444 | 3929b794 | 3 | **YES: 5513/327 (commit 3a5d344 on top of b7bafb8)** | 5513/327 (+20/+1) | RELAYED, B1433 STATUS:135-136 |
| B-learning | b1433/nexusai-b-learning-manager-log-lines | 725dcf0e | 3929b794 | 2 | no | 5501/327 (+8/+1) | RELAYED, B1433 STATUS:120,126 |
| S-l1 | b1480/nexusai-s-l1-design-inventory | 70709c61 | 3929b794 | 7 | no | 5507/329 (+14/+3) | RELAYED, B1480 STATUS:81 |
| S-viewer | b1480/nexusai-s-viewer-write-gates | f913fefb | 3929b794 (on S-l1) | 10 | no | 5513/331 (stack total; +6/+2 over S-l1) | RELAYED, B1480 STATUS:101,147 |
| S-colmap | b1480/nexusai-s-setup-column-mapping | 2a584f7d | 3929b794 (on S-viewer) | 11 | no | 5516/332 (stack total; +3/+1 over S-viewer) | RELAYED, B1480 STATUS:120; its plain run is UNMEASURED there (:148) |
| S-revoke | b1480/nexusai-s-session-revocation-clarification | 5fbad1ba | 3929b794 | 6 | no | 5499/328 (+6/+2; removes 2 names in rd798/rd799, adds 8) | RELAYED, B1480 STATUS:92-93 |

Stack (merge-base --is-ancestor, by program): S-l1 -> S-viewer -> S-colmap. No other ancestry exists among the 12.

## Merge facts (by program: `git merge-tree --write-tree`)
- Pairwise: 0 conflicts in 66 pairs.
- Sequential landing in the order below, each step merging the next head into the previous simulated merge commit: 12 of 12 clean (final simulated tree at local ref `refs/gate/seq-proposed`, 9fc1ebd0). One caveat: this simulation has NO counts commits in it. Read the counts rule below.
- Control: the merge-tree check rebuilt every B1431 tree independently as main plus the head's blobs, and they were equal. A conflicting pair would print rc 1 (none did).

## Shared paths (by program, intersections of `git diff --name-only <merge-base> <head>`)
- `backend/server.js`: S-viewer, S-colmap (the stack) and S-revoke. Their merges are textually clean. Semantic coupling: the stack carries a regenerated route inventory (`docs/role-capabilities.json`, `docs/ROLE-CAPABILITIES.md`). `__tests__/roles-foundation-route-census.test.js` compares that inventory with the live server, and S-revoke changes server.js handlers. Whichever of the two lands second must re-run the census and the rd929/rd977/rd978 cells on its merge tree before landing. (A targeted run of those suites on the full 12-branch simulated tree is queued under the jest lock as `qa-b1431-order`. Its result, if it finished, is appended below.)
- Inside the stack: S-l1/S-viewer/S-colmap share capabilities.js, the inventory script, the two docs and the rd929/rd977/rd978 tests. That is expected, since each contains the one before.
- `scripts/verify-expected-counts.json`: changed only by B-cspintake (its counts commit). It is owned by no lane.
- The B1431 branches share no path with any other branch, and none with each other.
- Cross-lane note for the coordinator: S-revoke edits `__tests__/rd798-log-injection-chat-and-learning.test.js` and `__tests__/rd799-log-injection-auth-and-storage.test.js`. Both are in lane T's OWNS block (RD-980's files). No pushed T branch touches them, so nothing conflicts today. The partition, though, says they are T's. Its own gate should rule on it.

## The counts rule (why the order matters)
Every landing changes the suite size except F-overflow. The PR Build's verify predicate requires the counts file to equal the merged tree, so each branch needs a counts commit made on top of the CURRENT main at its turn. B-cspintake already carries one, written for main at 5493/326. Two consequences follow:
1. If B-cspintake lands FIRST, its counts commit is correct as it stands (5513/327), and it needs no new commit. If it lands later, its counts line conflicts with main's newer counts file and must be replaced by a fresh counts commit.
2. F-overflow adds no test, so after any landing its counts already equal main's and it needs no counts commit.

## Proposed order, with the counts each landing must commit (derived = main's value then + the branch's delta; regenerate by running verify, never by arithmetic)
| # | land | counts commit needed | counts after landing (derived) | why here |
|---|---|---|---|---|
| 1 | B-cspintake (3a5d3444, pin as is) | no (already on branch, 5513/327) | 5513/327 | its counts commit is only right on main 5493/326 |
| 2 | F-overflow (a1d7f46d) | no (adds no test) | 5513/327 | no counts change |
| 3 | B-learning | yes | 5521/328 | independent (backend/learningManager.js) |
| 4 | F-header | yes | 5522/329 | independent |
| 5 | T-ci | yes | 5536/331 | changes Build itself (checkout/setup-node v7, browser assert). Landing it before the remaining PRs means their PR Builds run on the new workflow; its own PR Build proves it first |
| 6 | T-csp | yes | 5563/333 | independent |
| 7 | T-smtp | yes | 5571/334 | independent |
| 8 | T-archive | yes | 5575/335 | independent |
| 9 | S-revoke | yes | 5581/337 | server.js; land before the stack so the stack's inventory is re-checked on top of it (census rule above) |
| 10 | S-l1 | yes | 5595/340 | stack base |
| 11 | S-viewer | yes | 5601/342 | on S-l1; server.js and inventory |
| 12 | S-colmap | yes | 5604/343 | on S-viewer; the census must be re-run on its merge tree |

All derived totals assume the per-branch deltas add up (12 branches, no test name shared across branches; the stack deltas are relative to the previous stack member). Each landing's counts commit is measured by `npm run verify -- --maxWorkers=2 --update-counts` on that branch merged with the main of that moment, from a non-dot path, under the jest lock.

## Deploy demo
Every one of the 12 changes at least one path outside `deploy-demo.yml`'s paths-ignore (`**.md`, `docs/**`, `tests/**`). B1431 measured: `scripts/`, `__tests__/`, `.github/`; the others touch `__tests__/`, `static/`, `backend/` or `scripts/`. So each merge starts a Deploy demo run. Both of its jobs are gated on `vars.CI_DEPLOY_ENABLED == 'true'` (`:53`, `:91` at main and at every B1431 head, blob 597b3487 unchanged) and should read skipped. The variable itself is NOT RUN (hosted).

## NOT RUN
Hosted reads (PR states, the CI_DEPLOY_ENABLED value, CodeQL). A full-suite run of the stacked 12-branch tree (only the targeted coupling run is queued). The other lanes' counts are RELAYED from their STATUS files, not re-measured here.

## Appended: coupling run on the simulated 12-branch tree (MEASURED 2026-11-11 01:4x AEDT, jest lock tag qa-b1431-order, --maxWorkers=2, non-dot scratch worktree at 9fc1ebd0)
Ran 13 suites: roles-foundation-route-census, rd929, rd977, rd978, rd958, rd793, rd967, rd972, rd976, rd798-log-injection, rd799-log-injection, rd731, rd720. Result: 133 of 133 passed, 0 failed, rc 0, and the tree was left clean. So, in this order, the stack's route inventory still matches the live server with S-revoke's server.js under it. The census caution above still applies if the order changes. The full suite on the stacked tree is NOT RUN.
