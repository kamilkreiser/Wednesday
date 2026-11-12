GATE B1537: GO WITH FINDINGS @ 41880f6 on main 1515a71
Gate G2 (model-routing.md:109), class dependency-override, round 1 of 2. Project MPS Calculator. Branch b1537/mps-minimatch-alert-10 @ 41880f644f8aeeac566c80ed2f79bfafd79123e0, main 1515a71dc5a5f28eaf6c13ac129cc600f8d10b02. Gate clocks 12:54 to 14:46 AEDT 2026-11-12 (`date`). No security-shaped issue found. Findings: 0 Blocker, 0 Major, 2 Minor.

## Findings
| # | Class | Finding | Where |
|---|---|---|---|
| F1 | Minor | The head's FIRST whole Vitest run was red: 4 of 1541 failed (3 x "Test timed out in 5000ms", 1 x "Unable to find an element": InventoryPickerMany, PartnerRebate.b456, PriceReason, PurchaseBomEditor.addSectionWait). Load1 rose from 6.7 to 26 during that run (other seats' jobs; logs/jobs.log "head-vitest ... load_end=26.45"). Re-run at calm load (load 2.5 to 6): head 1541 of 1541, the 4 files alone 18 of 18, names lost 0 changed 0 added 0 vs main; main also green twice (1541). The builder reported the same load flake on UNCHANGED main. Not caused by this change (no code, minimatch is not in vitest's tree), but hosted CI can show it. A red hosted `web` job on these four files is a re-run, not a rejection. | out/head-whole.json (red), out/head-whole2.json, out/head-4files.json |
| F2 | Minor | Builder read the kit's Q-3 as stable releases only. Confirmed: 21 stable typescript-estree releases 8.60.0 to 8.72.2 all declare ^10.2.2 (read by me at 14:0x, control: the count printed 21 identical values); the canary 8.72.3-alpha.8 declares ^11.0.1. Override remains the narrowest stable-only change; the removal condition is likely near. | npm view output, logs |

All builder claims in the STATUS that I re-measured are TRUE: refs, two paths, blobs 610a0767/b7ceb57f, 12/4, 297/298, the two keys, audit 7 to 0, matcher, no-change control, 1541/192+10/51/8 files 1109118 bytes 0/57. The builder's `ci.yml` line pointers (:60, :125) are true.

## Refs and merge (measured)
- `git ls-remote origin` at 12:55: branch = 41880f644f8aeeac566c80ed2f79bfafd79123e0, main = 1515a71dc5a5f28eaf6c13ac129cc600f8d10b02 (control: refs/heads/b1530* printed one line). Head is 1 ahead, 0 behind (`rev-list --left-right --count` 0 1).
- Changed paths: exactly `web/package-lock.json` and `web/package.json` (2 of 2). #187's files (11: docs, 2 src/MpsCalc.Api/Quotes, 3 tests/MpsCalc.Api.Tests, 3 web/src/api/generated) overlap with the head: 0. Open PRs 0 (control: `pulls?state=all&per_page=2` printed 187, 186).
- Lock and manifest blobs at main (1515a71) = 7c7d4608f669a19e4b52c963cdb4debb81d6f879 / f74032cf4fae0b00ea26d2efc984f4a58f1fa9fb = the same two blobs at the builder's base 5239020 (unchanged). Head blobs: lock 610a0767543c5cf51862d10013939cd7caaacff3, manifest b7ceb57f3b04a5794f1ac9401f3a0ab206ad0ee0.
- `git merge-tree --write-tree origin/main origin/b1537/...` (in my own clone, push URL invalid) rc 0, tree 2a65dd79 = the head's tree (head descends from main), so merge = main plus the two head blobs; `npm ci` etc. at head therefore also cover the merge tree.
- Commit identity `41880f6 kamil.kreiser@datasec.com.au | kamil.kreiser@datasec.com.au` (author = committer, the repo's own address).

## Property checks by program (lockcmp.py in the work folder, controls inside)
- Changed lock entry keys = exactly {node_modules/@isaacs/nonrecursive-glob-match (new, 1.1.0, dev, BlueOak-1.0.0, integrity sha512-GPm/..., no dependencies), node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch (10.2.6 -> 11.0.1, integrity sha512-t+Vn6DX4...RZoLQ== = `npm view minimatch@11.0.1 dist.integrity`)}. Root "" entry equal. Entries 297 -> 298. Non-registry `resolved`: 0. Non-ASCII bytes in both locks: 0.
- Manifest: parsed JSON equals main's plus `overrides` = {"@typescript-eslint/typescript-estree": {"minimatch": "11.0.1"}}, key order kept; `git diff -U0` shows the 5 added lines (`+  },` `+  "overrides": {` ...), numstat 5 0.
- Alert matcher (range >= 7.0.0, < 11.0.1; controls 10.2.6 vuln, 11.0.1 clear, 5.1.9 clear, 3.1.5 clear, 11.0.1-rc.1 vuln, 7.0.0 vuln, 6.9.9 clear): main 3.1.5 clear, 5.1.9 clear, 10.2.6 VULN; head 3.1.5, 5.1.9, 11.0.1 all clear. Alert 10 open at 12:55 (GHSA-g3hv-75wg-m249, range and first-patched 11.0.1 as stated; control: alert 9 answers 410).
- `npm audit --package-lock-only --json` (registry): main 7 moderate, 0 high, 0 critical, total 7, minimatch present; head total 0, minimatch absent.
- No-change npm control at the pinned Node v24.22.2 / npm 11.19.1 (drive-local `tools/node-v24.22.2-darwin-arm64`): main's two files -> `install --package-lock-only` "up to date", lock blob stays 7c7d4608 (control: a one-character plant, lockfileVersion 3 -> 4, hashes a98049d0). Main manifest + override over main's lock reproduces head's lock blob 610a0767 and manifest b7ceb57f exactly.

## CI steps as ci.yml:45-82 runs them (Node v24.22.2, npm 11.19.1, Vitest 5.0.3, Playwright 1.63.0 with the installed Chrome; ports 9971, 9972, dead API origin 9979, all free afterwards; `MPSCALC_E2E_BASE_URL` set to my port, as the web server needs it)
| Step | main 1515a71 | head 41880f6 |
|---|---|---|
| `npm ci` | rc 0 | rc 0 (lock and manifest agree) |
| `npm run lint` (parses TS through the changed copy) | rc 0 | rc 0 |
| `npm test` (vitest run, sorted full names) | 1541 passed, 145 files (two runs) | run 1 red under load (F1: 1537 passed, 4 failed); run 2 1541 passed; 4 files alone 18 passed. Names vs main: lost 0, changed 0, added 0 (run 2) |
| Playwright stub (CI step 1) | 192 passed, 10 skipped | 192 passed, 10 skipped; lost 0 changed 0 added 0 |
| Playwright api-off (CI step 2) | 51 passed | 51 passed; lost 0 changed 0 added 0 |
| `VITE_MPSCALC_AUTH=entra npm run build` + `check-bundle.mjs dist` | rc 0; 8 files, 1109118 bytes, markers 0/57 | same, 1109118 bytes |
Compare controls (cmp.py): flip a passed row to failed names it as changed, drop a row shows lost 1, add a row shows added 1. `npm ls minimatch --all`: head estree copy `minimatch@11.0.1 overridden`, eslint 3.1.5, redocly 5.1.9; the only diff against main is that one line (so the diff program can fail). Direct exercise from the estree package directory: main resolves 10.2.6, head resolves 11.0.1; both `minimatch('a/b.ts','**/*.ts')` true, `('a/b.js', ...)` false; `require('@typescript-eslint/typescript-estree')` loads and parses `const x: number = 1;` (body length 1) at both.
- Production tree: `npm ls --omit=dev --all` at main and head, path-normalised: identical (11 lines each; `diff` empty). Lock-level: the 6 non-dev entries equal at both.

## Scans
- Name scan over the commit message and every added line, `(?<![A-Za-z])<name>(?![a-z])` for Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite: 0 each (control `x_by_<name>_y` fired for each). Banned-word scan (B-numbers, ticket keys, Tuesday/Wednesday/Friday, SEAT, M131) of the message: 0 (control fired). One trailer. Subject 80 characters.
- Secrets: gitleaks 8.30.1 over origin/main..head rc 0, after a planted `ghp_` + 36 random characters canary was refused (rc 1). Cf characters in added lines 0; UUID or host strings in added lines 0; non-registry URLs 0.
- CodeQL pre-scan: added lines are 17 (5 in the manifest, 12 in the lock) and all JSON; `new RegExp|innerHTML|child_process|os.chmod` over the diff: 0. No code is added or changed.
- Repo-wide scan that walks tracked files: Cf characters across the 708 tracked files at head: 7 files, all pre-existing (scripts/tests/test_deploy_pre1.py, 5 C# test files, 1 csproj), none in the diff and the same at main by construction (diff touches only the two JSON files). No MPS workflow runs a repo-wide hidden-character test (grep over .github).
- Tests that read the changed files: ci.yml:60 and :125 (setup-node cache key), tools/demo/test/test_run_demo.py:38 (a fake lock), tools/leakscan (an exemption and a string path). None reads the real file. Read at head by `git grep -n`.
- Deploy: ci.yml runs on push to main; no deploy workflow is triggered by this change; nothing is deployed.

## NOT RUN
- dotnet, python and `package` jobs (the change reads no file they read; hosted CI is the proof), hosted CodeQL, the hosted `web` job, check-runs on the head (my token cannot read them; `actions/runs` is Tuesday's read).
- The 8 specs the Playwright config leaves out of CI's two modes.
- Red-without-fix: not applicable to a dependency change (no test added); the proof is the names compare and the matcher/audit, above.
- Load gate: two reads 120 s apart were taken before every heavy job (waits up to 16 min, see logs/jobs.log, logs/wait.log); the reads are not independent. The job run lengths were short because the machine was quiet at run time; my wrapper took a slot (heavy-lock-1 or -2) per job and released each (holders moved to logs/).

## FOR TUESDAY
- Landing: head-pinned squash (`landing.txt`; `<PR-NUMBER>` is a literal place). Open the PR from branch b1537/mps-minimatch-alert-10 into main. If main moves, re-check the two blobs at main (7c7d4608..., f74032cf...) before landing.
- After landing: `dependabot/alerts?state=open` should no longer list alert 10 (still open = new round). Hosted `web` may flake on the four UI tests of F1 under load: re-run it, do not reject.
- Override removal condition: remove the `overrides` block (and regenerate the lock with npm at Node 24) once the first STABLE `@typescript-eslint/typescript-estree` release declares minimatch ^11 (the 8.72.3 alpha line already does; latest stable is 8.72.2, ^10.2.2). Because the sibling `@typescript-eslint/*` packages and `typescript-eslint` are exact pins at 8.71.1, that means bumping them together.
- Squash trailer: squash-body.txt ends `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` (this session's attribution line; the standard names Opus 5.5).
- Outside the fences: I ran `git worktree add` (two worktrees) and `merge-tree` in my own clone only; `gh api` GETs under the project config; `npm ci`/`view`/`audit` against registry.npmjs.org; nothing in the project folder was written. Work folder: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s272/g1537/ (clone, main-tree, head-tree, out/, logs/ kept, nothing deleted).
