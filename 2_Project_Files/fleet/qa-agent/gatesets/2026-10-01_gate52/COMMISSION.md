# gate52 COMMISSION — TWO Secuura PRs, merged A then B: #1367 KS-1015 and #1368 KS-1364 (both T2, round 1); author and merger Seat B 53rd, round 52

Filled by fill_gate52.py at 2026-10-01T09:49:42Z from pins_gate52.json (measured 2026-10-01T09:38:04Z). This restates Wednesday's commission to the drafter (2026-10-01), requirement by requirement. The gate prompt carries each requirement by name, and the launcher refuses a prompt that is missing any of the 31 keywords (each matched as a token).

## The PRs
| PR | ticket | role | tier | head | parent | merge-base | ahead / behind | files (+/-) | subject declared -> lands |
|---|---|---|---|---|---|---|---|---|---|
| #1367 | KS-1015 | A (merged FIRST) | T2 | `ac3ceee7f440478431a317d3a31a42ab737f57c7` | `0736d8b7849e` | `0736d8b7849e` | 1 / 0 | 3 (+127/-2) | 75 -> 83 |
| #1368 | KS-1364 | B (merged SECOND, onto A's squash) | T2 | `2a3dcd912a33b1ced6b6769368d87fce82ab64bc` | `0736d8b7849e` | `0736d8b7849e` | 1 / 0 | 5 (+98/-0) | 83 -> 91 |

- develop `0736d8b7849ef6c725c891d7254f2a3e21f42eb6` (tree `da849aa1d5c3d60f62b49b7f625fca01e3d59059`) = #1365's merge. Both 0 behind, siblings.
- END_TREE_A `d1f03c3714541097834e37e2786527c2c1b71573` (`3 files changed, 127 insertions(+), 2 deletions(-)`). END_TREE_B `48f5f8afa6ef1f03f2d64e4afa24fd9f75213ad7` (`7 files changed, 225 insertions(+), 2 deletions(-)`) = the seat's PREDICTED tree. Three instruments agree on each (end_tree_crosscheck_1.out): END_TREE_A by merge-tree + commit-tree, by A's own tree (parent == develop) and by GitHub's `refs/pull/1367/merge`; END_TREE_B by the chained merge-tree, by `merge-tree A B`, and by B's diff applied onto END_TREE_A under a temp index. Controls that differ: develop's own tree da849aa1d5c3 and GitHub's `refs/pull/1368/merge` (B alone).
- EACH ALONE over develop: #1367 merge-tree clean, tree `d1f03c3714541097834e37e2786527c2c1b71573`; #1368 merge-tree clean, tree `bf016acccf532cb008f9175ecc8ef8b86905e875`. THE CHAIN: #1367 squashed (commit-tree -p develop, `c44ae2a0bdf1`) -> END_TREE_A `d1f03c3714541097834e37e2786527c2c1b71573`; #1368 merged onto that squash with no conflict (`9e6fc2697487`) -> END_TREE_B `48f5f8afa6ef1f03f2d64e4afa24fd9f75213ad7` == the seat's PREDICTED tree; `merge-tree --write-tree A B` reads the same tree.
- MODES (git ls-tree): all 7 distinct PR paths 100644 (8 pins: the shared yaml is pinned once per PR) at their head / alone / END_TREE_B; control `Blockchain/Dev/scripts/run-migrations.sh` 100755 at develop / both heads / END_TREE_B.
- IDENTICAL at develop / both heads / END_A / END_B: `pre-push` ffc25ebc37d4, `preflight.sh` 270b8913c009, `generate-openapi.ts` e84acdc9e1be, `check-spec-examples.mjs` e9c14a4dedf1, `package.json` d22c14e6c370.
- Merger: Seat B 53rd (the author of both). Pane: `QA/Secuura-batch1367`. Report dir: `2026-10-01-batch1367-g52`.

## The claim (the ONE READY)
- #1367: 3 files, +127/-2; `referral.openapi.ts` +21/-1 (the GET 200 envelope); 1 new test +76; yaml +30/-1, sha256 `43c71cf6d5f213b6`, 39889 lines.
- #1368: 5 files, +98/-0; two `*.openapi.ts` +1/-0 each; 2 new tests +48 / +46; yaml +2/-0, sha256 `39f027b63d4aa804`, 39862 lines, `required: true` 71 -> 73.
- The A+B union yaml: sha256 `e761a0b3c1eac6a5`, 39891 lines, blob `1ffd687b8a9d…`, `check:openapi` rc 0 on it.
- `generate-openapi --check` rc 0 per PR, control rc 1 with the yaml reverted; `check:openapi` rc 0, 405 example blocks.
- Red-first by assertion: A 3 failed | 3 passed (6); B 1 | 3 (4) per file. Suites: referral 28 -> 34; tenant-provisioning 13 -> 17; originate 1058 -> 1062 (89 -> 90 suites). tsc rc 0.
- Trailers: both commit messages empty, control `bf277eead268` carries Co-Authored-By (53 bytes).

## What the gate must rule (by name)
1. **#1367: the declared GET /api/referrals/{code} envelope == what the handler returns**, on 200 and on every error status the spec lists (file:line). A spec that disagrees with its handler is a Major. (ENVELOPE-MATCHES-HANDLER, ERROR-CODES-MATCH)
2. **#1368: each handler refuses an absent body** — tenants PATCH by the "No fields to update" 400 (`tenant-provisioning/src/index.ts:455-457`), v2 verify by the `:452-456` 400 after the four-alias coalesce (`verificationV2.ts:450-451`); body-parser's `req.body || {}` cited from the installed package. (HANDLER-REJECTS-ABSENT, BODY-PARSER-DEFAULT, ALIASES-COVERED)
3. **#1368's body claim: POST /api/referrals/generate is NOT marked required because its handler accepts `{}`** (`referrals.ts` generateCodeSchema `:16-21`, `.parse` `:61`), verified from source. (GENERATE-NOT-REQUIRED)
4. **Goldens byte for byte; the yaml == generator output** (`--check` rc 0, control rc 1); the three YAML shas. (GOLDENS-BYTE-EQUAL, GENERATOR-REPRODUCES, CHECK-OPENAPI-RC, YAML-SHAS)
5. **Red-first per new test by assertion, then green; referral + tenant-provisioning (vitest) and originate (JEST), 0 new reds.** (RED-FIRST, CONTROLS-GREEN, SUITES-BASE-HEAD, TSC-NO-REGRESSION)
6. **The sequencing: B after A lands exactly on 48f5f8afa6ef1f03f2d64e4afa24fd9f75213ad7; no textual conflict; both stay mergeable.** (SEQUENCE-A-THEN-B, CLEAN-MERGE, END-TREE, BOTH-MERGEABLE, MODES)
7. **The PR-text key scan: only the own hyphenated key, no closing keyword, NO Co-Authored-By trailer** (control `bf277eead268`). (KEYSCAN-OWN-KEY, NO-CLOSING-KEYWORD, NO-TRAILER, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, PR-BODY-CLAIMS, NO-RUNTIME-CHANGE)
8. **The census** of other open PRs touching the 7 paths; Peter's #1360 / #1362 reported only. (COLLISION-CENSUS)
9. **NOT TESTED, explicit.** (NOT-TESTED-LIST) Plus TIERING, DISK-ENOSPC, **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` goes LAST. The pass is proportionate (usage 92%, Kam's 17:40:22 grant).
- NOT in scope: a live server, Schemathesis, any deploy, any DB, any request to a handler.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 53rd): merge 1367 1368 on gate52`. Seat B 53rd merges #1367 then #1368. Verdict mail subject: `[QA -> Wednesday] GATE52 #1367 #1368 (Seat B53 author and merger, round 52; T2 OpenAPI: the referral lookup 200 envelope, two more request bodies required, 3 new spec-rendering tests, the generated yaml)`.

## The drafter's predictions (the gate re-derives each and never adopts one)
- pin_gate52.py -> pin_1.out: END_TREE_A `d1f03c3714541097834e37e2786527c2c1b71573`, END_TREE_B `48f5f8afa6ef1f03f2d64e4afa24fd9f75213ad7`. The measured numstat: #1367 +127/-2 over 3 files (the seat claimed +127/-2); #1368 +98/-0 over 5 files (the seat claimed +98/-0).
- specdiff_gate52.py -> specdiff_1.out: SPECDIFF PASS: 0 FAIL of 17 checks | base 0736d8b7849e | #1367 ac3ceee7f440 | #1368 2a3dcd912a33
- handlers_gate52.py -> handlers_1.out: HANDLERS PASS: 8 checks, 0 FAIL | envelope RL1 at ac3ceee7f440 | absent-body TP1/VV1 at 2a3dcd912a33 | control RG-CTL
- keyscan_gate52.py -> keyscan_1.out: KEYSCAN PASS: 17 checks over 2 PRs, 0 FAIL (trailer control FIRED)
- gh_read_gate52.py -> gh_read_1.out: CENSUS 21 other open PR(s) read | 0 touch a kit path or carry a census key ['KS-1015', 'KS-1364'] | 7 kit paths | client-human PRs named: ['1360', '1362'] (the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)
