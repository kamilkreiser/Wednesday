GO WITH FINDINGS
GATE B1534: GO WITH FINDINGS @ 13bf950 on main 5d3bf82. Gate G2, dependency-bump class, round 1 of 2. Clocks from `date`, 2026-11-12 11:37 to 13:17 AEDT. Project Security Composer (datasecau/Datasec-Security-Composer), branch `b1534/composer-bot-updates-repush` = 13bf95065519fc5688b4435aa04a8523bae13eb6. Findings: Blocker 0, Major 0, Minor 3. No security-shaped issue found (three manifest/lock paths, no code added).

## Refs and merge (measured, 13:16)
- `git ls-remote`: branch = 13bf95065519fc5688b4435aa04a8523bae13eb6 (the READY sha); main = 5d3bf82ddca5b07a216ace594be4f47af4119ec6 (the base the builder used; it has not moved). PR heads #91 301991a8, #86 fd24426d, #85 85105729 (draft) all unchanged; #91 and #86 still open, 0 comments, `changed_files` 2 each, not touched. #85 has 0 files with basename package.json / package-lock.json (control: #91 lists both).
- Head is 0 behind, 1 ahead of main (`rev-list --left-right --count` 0 1). `git merge-tree --write-tree main head` rc 0, tree ff517fca = head's own tree, so the merge tree IS the head tree; every "merge" result below is the head result. Control: merge-tree of head against #91 also exits 0 because #91's hunks are byte-identical to ours (see F3).
- Changed paths 3 of 3 in the lane (package.json, apps/web/package.json, package-lock.json); not-in-list count 0 (control with a planted `src/x.ts` prints 1). One commit, author = committer = 88359143+kamilDatasec@users.noreply.github.com (the repo's own identity, equal to main's author). One trailer.
- Open PRs touching a manifest: only #91 and #86 (the two being superseded). No `.github` path at head (0; control `docker/Dockerfile` 1): there is no hosted test workflow; hosted checks on main are only CodeQL `Analyze (csharp)` and `Analyze (javascript-typescript)` (both success on main). Code-scanning analyses: #91 head 0, #86 head 0, #118 head 2, main 30, this branch 0 (no PR yet).
- Org ruleset 24139430 "Security scan rule" active (read).

## The three ANSWER-2 gates, re-run by me (pinned image by digest sha256:83f487e0..., user 501:20, HOME=/tmp, `npx -y npm@11.20.0`, container names pc-g1534-*)
1. No-change install with npm 11.20.0 on a fresh copy of main's 13 files: lock blob stays 53305eb4c7b615b0da35718dfa0830e34bcd9f52; all 12 manifests cmp-identical. PASS. Control: a planted `"lockfileVersion": 4` hashes to 5f38cb3c. (Round-1 ANSWER-1's 27 peer flags: not needed, withdrawn, and absent from the lock: 0 `"peer": true` lines at head.)
2. The update, the builder's exact commands (`--before=2026-10-25T12:00:00Z -D vitest@5.0.5`, then `--before=2026-10-19T00:00:00Z -D -w @pc/web vite@8.3.4`), rc 0 and 0: lock blob 39a36218569c8fc535a5e4eb24b3024de9ac878e, root manifest 7e6304c1, web manifest f59f0e7d: all equal the pushed blobs. PASS. Lock diff entry set by program (`out/lockcmp.txt`): head vs main changes 34 entries; #91 changes 13, #86 changes 21, overlap 0, union 34; head-not-union [], union-not-head []; for every one of the 34 the head entry equals the owning bot's entry (0 differ). Control: a planted chai 9.9.9 is reported. siginfo and stackback removed, nothing added. vite 8.3.0 -> 8.3.4, vitest and @vitest/mocker 5.0.0 -> 5.0.5. The bots' lock blobs re-hashed: #91 7dbad553, #86 32cbf3f7.
3. The image's own npm 10.9.8 `npm ci` accepts the result: CI-stage image built from the head tree, rc 0 (the Dockerfile runs `npm ci --ignore-scripts`). PASS.
- Also confirmed the builder's two side claims: (a) npm 10.9.8 on `-D vitest@5.0.5` fails rc 1 with "Cannot read properties of null (reading 'edgesOut')"; (b) the same npm 11.20.0 commands WITHOUT `--before` give lock blob 5b30f138, not the bots' set (see F1).
- Lock content: `resolved` 336 (325 registry.npmjs.org + 11 workspace links; main 338), changed entries with non-registry host 0, non-sha512 integrity 0, non-ASCII bytes 0 (control 1 for each scan). Every moved transitive sits inside its parent's declared range (printed in `out/lockcmp.txt`, e.g. postcss 8.5.31 under vite `^8.5.29`, rolldown 1.2.14 under vite `~1.2.12`).

## CI by program (pinned image ci stage; `--network none`; same commands as `ci:node`; the host is not used)
| Check | main 5d3bf82 | head 13bf950 (= merge tree) |
|---|---|---|
| image build with `npm ci` | rc 0, npm 10.9.8, node v22.23.2 | rc 0 |
| `npm run lint` | rc 0 | rc 0 |
| `npm run format:check` | rc 0 | rc 0 |
| `npm run typecheck` | rc 0 | rc 0 |
| `npm run build` (then vitest in the same container) | rc 0 | rc 0 |
| whole vitest suite (JSON) | 315 files, 3177 tests: 3174 passed, 1 skipped, 2 failed | identical counts |
| name/status compare of the whole suite | - | lost 0, added 0, changed 0 |
| `packages/db` suite (throwaway postgres:16 by digest, internal network) | 39 files, 674 passed | 674 passed, lost 0 changed 0 added 0 |
| `apps/api` db suite | 83 files, 1563 passed | 1563 passed, lost 0 changed 0 added 0 |
| `--target web` image build | not run | rc 0 |
| versions under test | vitest 5.0.0, vite 8.3.0, @vitest/mocker 5.0.0 | vitest 5.0.5, vite 8.3.4, @vitest/mocker 5.0.5 |
- The 2 red rows are the same two at both: `packages/content/src/citations.test.ts` (E8 SOW citation rows) fail with "SOW text not readable" (present in both JSONs, control: the same files hold "passed"). They need the withheld source text the repository does not carry; green-at-main status is unchanged (red at base too). Compare controls on scratch copies of the head JSON: flipped row `changed 1`, dropped row `lost 1`, added row `added 1`.
- Note: my first `format:check` run died on an invalid container name (rc 125, my own typo); re-run alone later on the same two images: rc 0 at both ("All matched files use Prettier code style!").
- `npm audit` (image npm 10.9.8, lockfile-only, from each tree's manifests): main 17 findings (14 moderate, 2 high, 1 low), head 14 (12 moderate, 1 high, 1 low). Closed by head: vite (the high), vitest, @vitest/mocker. New at head: none; severity changed: none. No new high or critical.
- Dependabot alerts (my own matcher `scripts/alerts.py`, matcher control asserted): 23 open, 4 high. At the head lock alerts 5 to 12 clear (vite 8.3.0 -> 8.3.4 for 5-10, one high; @vitest/mocker 5.0.0 -> 5.0.5 for 11 and 12). 15 stay VULN, 3 of them high: undici 6.28.1 (18, 20, 25, 26, 27), fast-uri 3.1.8 and 4.2.2 (14-17, 19, 22-24), ip-address 10.7.2 (21), fastify 5.12.5 (13).

## Scans
Underscore-aware `(?<![A-Za-z])<name>(?![a-z])`, names Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite: 0 in the commit message and 0 in the 149 added lines, each control `x_by_<name>_y` fires. Ticket/seat words in the message 0 (control 2). Secrets / UUIDs / tenant ids in added lines 0 (control 1), Cf characters 0 (control 1), hosts in added lines: only `https://registry.npmjs.org`. CodeQL pre-scan (JavaScript and C# are the analysed languages; added lines are JSON only): `new RegExp(`, hand-escape replace, innerHTML, child_process, chmod: 0 (control 1). No code is added, so no CodeQL query has new input; hosted CodeQL on the PR head is still Tuesday's read. Repo-wide scans that walk tracked files: the project has none in a hosted workflow (no `.github`); no file other than the three manifests changed, so hidden-character state of the tree is main's.

## Findings
| # | Class | Where | Finding |
|---|---|---|---|
| F1 | Minor | package-lock.json (whole), commit body | The lock is only reproducible with the dated installs (`--before=2026-10-25T12:00:00Z` for vitest, `--before=2026-10-19T00:00:00Z` for vite). The same npm 11.20.0 commands without `--before` give blob 5b30f138 (40 changed entries, newer rolldown and others). The commit body says so ("resolution was dated (--before)"), and PR text states it. Not a defect of this change; a future plain `npm install` will move those packages. |
| F2 | Minor | project tooling, not this diff | The pinned npm 10.9.8 cannot resolve vitest 5.0.5 (arborist crash, reproduced) and adds `"peer": true` to 27 entries on any rewrite; main's lock is maintained with a newer npm (11.20.0 reproduces it byte-for-byte) but Dockerfile and `.nvmrc` do not say so. Any future in-image `npm install` will hit this. Follow-up item for the 15 remaining alerts. |
| F3 | Minor | builder STATUS "Supersede rule" | STATUS and the kit say #86/#91 "would conflict" if landed; measured: `git merge-tree` of this head with #91 exits 0 (the hunks are identical). They are redundant, not conflicting; closing them unmerged is still correct. |

## Claims graded (builder STATUS rounds 1-3)
True (re-measured): npm 10.9.8 crash; 11.20.0 byte-for-byte on no-change; update blob 39a36218 with the dated installs; 34 entries, bots' versions; manifests one line each; lock `resolved` 336 = 325 + 11; image `npm ci` rc 0; whole suite 315/3177 (3174/2/1) at both; db 674 and 1563; web image rc 0; 8 alerts clear, 15 stay (3 high); identity and one trailer; branch ref and PRs untouched. Not shown here: the builder's gitleaks runs and the `scripts/secret-scan.sh --tree` result (I ran my own regex scan instead, 0 hits).

## NOT RUN
- Hosted CodeQL on the PR head (does not exist yet; Tuesday's read after the PR opens).
- The compose-stack, .NET bridge and egress sections of `scripts/ci.sh`; `scripts/ci.sh` as a whole (reads the withheld SOW text). The update changes no file those read.
- gitleaks / `scripts/secret-scan.sh` (replaced by my regex scan above).
- Playwright / browser tests of the web app (none are in the project's node CI predicate).
- A separate "merge tree" test run: skipped as redundant, merge tree = head tree (0 behind main).

## FOR TUESDAY
- Open the PR from `pr-title.txt` and `pr-body.txt`; land with `landing.txt` (N left as `<N>`; run it from this folder or with absolute paths for the two files). Then close #86 and #91 unmerged with a pointer; then read `dependabot/alerts?state=open` at main: 5 to 12 should be gone (a still-open one is a new round).
- squash-body trailer is `Co-Authored-By: Claude Sonnet 5.5` (the model that wrote this gate), where the standard text names Opus 5.5; swap if you prefer the standard.
- Resources: images `pc-g1534-node:base`, `pc-g1534-node:head`, `pc-g1534-web:head` removed by exact name; `pc-g1534` containers 0, networks 0, images 0 (control: other node images remain, 3). I pulled the pinned digest image `node:22-bookworm-slim@sha256:83f487e0...`, which was not cached; I left it. Heavy lock `.tools/composer-heavy.lock` absent now (I took and released it per job into `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s272/g1534/quarantine/`); I wrote nothing in the project folder except the lock directory itself. Work folder with scripts, logs, JSON and my clone: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s272/g1534/` (clone push URL set invalid; nothing pushed). Ports used: none.
- Outside-the-fences: network = git fetch/ls-remote of the repo by the deploy key (no push), `gh api -X GET` only, registry.npmjs.org from the containers, Docker Hub pull of the pinned digest. No az, Jira, mail, PR action.
