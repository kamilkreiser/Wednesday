GATE B1538: GO WITH FINDINGS @ 61ce4c3 on main c6b5c8c

Class dependency-override, G2 (Sonnet), round 1 of 2. Clocks: gate resumed 15:10:29 AEDT (predecessor died at the 15:06 rotation), VERDICT 15:20 AEDT 2026-11-12. No security-shaped issue found (see Property checks); no hand-off to a G1 needed.

## Findings
| # | Sev | Where | Finding |
|---|-----|-------|---------|
| 1 | Minor | builder pr-body.txt, first paragraph | Said the commit sits "on top of main c717ba1a" with no mention that main has moved. Main is now c6b5c8c (#314). Corrected copy in this folder states it. |
| 2 | Minor | builder STATUS BLUF / pr-body (RELAYED, not re-run by me) | Local e2e is "equal to base", not eight green: `a11y.spec.ts:39` times out at 30 s at base and head on the builder's macOS box. The read that matters is the hosted `web e2e` result on the PR head (Tuesday's). I did not re-run the e2e shards. |
| 3 | Minor | builder evidence landing.txt | Placeholder form differed from the required form; replaced by the exact `landing.txt` here (`<N>` literal). |
| 4 | Info | unit | Two earlier builder head runs had 1 load-sensitive failure (LoadFailed.states test); my base vs head compare of clean full runs is 4234/4234 with lost 0 added 0 changed 0. Not an effect of the lock (flake also at base under load, per builder; RELAYED). |

No false number found in the squash body or PR body (sentences checked below). One stale statement (finding 1) fixed.

## Refs and merge (measured, `git ls-remote` + bare clone by URL, push URL invalid)
- main read at start and again at 15:20: c6b5c8cf62fc8bc32246589bc7246bae6808f98d. Branch: 61ce4c3d310b786616e238165d634fb0c3533222; parent c717ba1a945191ffa31f13320c19967a6cf7f15a; `rev-list main..branch` = 1; `rev-list c717..main` = 1 (c6b5c8c, #314).
- `git merge-tree --write-tree main branch` = tree 8a67558d00b5ee1d9be98a983f8d528b6dc7ce43, no conflict. `diff --name-only main <tree>` = exactly web/package-lock.json and web/package.json. `diff branch <tree> -- web/package.json web/package-lock.json` = 0 lines (merge = main + the two head blobs).
- Changed-path overlap #314 (c717..c6b5c8c, 24 files) vs head (2 files) = 0 (control: head vs itself = 2).
- Blobs: main lock 81393fd7..., manifest 2e7ed8b3... (equal to the builder's base); head lock add1be79fe97684581d0cd5adce62c4d96730b2f, manifest b549f7f554e19857fd504088a86e81d03d8e819d. `git diff --numstat c717..head`: lock 12/4, manifest 5/0; manifest diff `^[+-][^+-]` count 5.
- Alert 9 (gh GET): open, medium, GHSA-g3hv-75wg-m249, development, transitive, web/package-lock.json, `>= 7.0.0, < 11.0.1`, first patched 11.0.1, created 2026-11-04T23:38:27Z; only open alert (control: alerts/1 = 410). Open PRs 0 now (control: pulls?state=all lists 314, 313, 312).
- Identity: author email and committer email both equal the project's configured email (by program, not echoed). Commit trailer: the one Co-Authored-By line.

## Property checks (measured by me, python over the raw files from `git show`)
- Changed lock keys main vs head = exactly {node_modules/@isaacs/nonrecursive-glob-match (new 1.1.0, dev, no deps), node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch (10.2.6 -> 11.0.1, deps brace-expansion ^5.0.12 + glob-match ^1.0.1)}. Entries 589 -> 590; root "" entry unchanged; 3.1.5 and 5.1.9 entries unchanged.
- Integrity: minimatch 11.0.1 and glob-match 1.1.0 each equal `npm view <pkg>@<ver> dist.integrity`. glob-match 1.1.0 is `latest` and the newest 1.x.
- Manifest: parsed JSON differs from main only by `overrides` = {"@typescript-eslint/typescript-estree": {"minimatch": "11.0.1"}}; the rest equal.
- Security shape: resolved 582 -> 583, off-registry 0; `link` entries 0; install-script packages head = main = {fsevents, unrs-resolver} (none added); non-ASCII/control bytes in head lock 0 (control: planted byte counted 1).
- Matcher: main minimatch copies 5.1.9 clear, 10.2.6 VULN, 3.1.5 clear; head 5.1.9, 11.0.1, 3.1.5 all clear.
- `npm audit --package-lock-only --json`: main {moderate 7, total 7}, minimatch present; head {all 0, total 0}, minimatch absent (high/critical 0 both).
- Q-3 premise: 21 stable estree releases 8.60.0..8.72.2 all declare `^10.2.2`; `latest` = 8.72.2, `canary` = 8.72.3-alpha.8. Of 307 versions in the 8.60 and 8.70 lines (per-version `npm view`), 299 declare `^10.2.2` and 8 declare `^11.0.1` (8.72.3-alpha.1..8, canary). Total stable versions of the package: 415. Canary does not count (ANSWER-1).
- Head tree: `git rev-parse HEAD` = 61ce4c3d..., porcelain empty (0 lines).

## CI predicates, base (c717ba1a) vs head (61ce4c3d); node v24.22.2, npm 11.19.1 (predecessor runner on the same trees; logs relayed, selected ones re-run by me)
| step | base | head |
|---|---|---|
| npm ci | rc 0 | rc 0 |
| lint (0 warnings) | rc 0 | rc 0 |
| typecheck | rc 0 | rc 0 |
| audit-dev.mjs | rc 0, moderate 7 total 7 | rc 0, all 0 (RE-RUN by me) |
| npm audit --omit=dev --audit-level=high | rc 0, 0 vulns | rc 0, 0 vulns (RE-RUN by me) |
| --check-shards | rc 0, plan OK | rc 0, plan OK |
| build (+postbuild, 39 markers none) | rc 0 | rc 0 |
| vitest | 292 files, 4234 tests, 4234 passed, 0 failed | 292 files, 4234 tests, 4234 passed, 0 failed |
| unit name compare (cmpunit.py) | - | lost 0, added 0, changed 0; controls: flip -> sym diff 2, drop -> lost 1, add -> added 1 |
| prod tree (`npm ls --omit=dev --all --parseable`) | 30 lines | 30 lines, identical once clone path normalised (diff 0) |
| infra test_hidden_characters.py (`python3 -B -W error::ResourceWarning`) | - | 14 tests OK, rc 0 (RE-RUN by me; walks every tracked file incl. the new lock) |
| infra test_ci_workflow.py | - | 40 tests OK, rc 0 (RE-RUN by me) |

## Re-measured by me vs RELAYED
- Re-measured: ls-remote main/branch twice; merge-tree and overlap; both blobs; lock key comparison; manifest comparison; integrity vs registry; audit lock-only at main and head; audit-dev and audit-prod at head; hidden-character and ci-workflow tests at head; unit name compare base vs head JSON (head JSON from the predecessor's 15:00 head run at the same trees, base JSON from the 15:17 base run, both finished by the runner I waited for; counts read by me); Q-3 per-version reads; alert 9 and PR reads; identity; the pr-body/squash-body sentences below.
- RELAYED from the builder (not re-run): the eight e2e shards and the base re-runs, the flake analysis, the deploy-package refusal on macOS (identical at base/head), gitleaks, the 14:35 census of 15 historical branches, the no-change npm control (blob unchanged at two toolchains), `npm ci` rc 0 (the predecessor's runner repeated it for both trees, rc 0).

## Sentences checked in pr-body.txt and squash-body.txt (all TRUE at source unless noted)
Alert fields and range; two paths; five added manifest lines; blobs; 12 added / 4 removed; 589 -> 590; the two entries and their dependency strings; "other copies byte-equal"; all added resolved on registry.npmjs.org; 21 stable estree releases, latest 8.72.2, canary alpha.1-8 declaring ^11.0.1, 307 versions / 299 / 8; the 10.x line ends at 10.2.6 (taken from the lock and the drafter; the registry confirmation was not re-read by me, MINOR UNVERIFIED); audit moderate 7 -> 0 and 0 high/critical; production tree unchanged; EMPTY exception list and medium alert (the kit's read of audit-dev.mjs; my audit-dev re-run prints "0 allowed by a dated exception"); unit 4234 / 932 suites / 292 files; shard plan 198/181/182/181/68/67/68/67 (relayed). One stale sentence fixed (finding 1).

## NOT RUN (and why)
api jobs and SQL Server jobs: no api path changes. `secrets` job (gitleaks full history) and rest of infra tests / validate.sh (no Bicep compiler; neither reads the two paths). The eight e2e shards (heavy, builder ran them; RELAYED). Hosted CodeQL, dependency review and checks: Tuesday's read on the PR head. A hidden-character test on the merged tree (not checked out; #314 touches no lock or manifest, and it passed on the head tree).

## Processes
Predecessor runner pid 57843 finished on its own (ALL DONE 15:19:47) and was not killed. heavy.lock absent; ports 9930-9939: 0 listeners (I used none). My work files: s272/g1538/v (bare clone, push URL invalid) and s272/g1538/w.
