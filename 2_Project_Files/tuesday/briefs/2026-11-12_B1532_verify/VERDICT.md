GATE B1532: GO WITH FINDINGS @ 6768b41 on main 30b957b

Tier G2, round 1 of 2 (the first gate on this branch; no earlier verdict line). Gate clock 12:04 to 14:25 AEDT 2026-11-12. Nothing pushed, no PR, no Jira, no mail, no az, no hosted HTTP except `gh api -X GET` under the project's own GH_CONFIG_DIR. Own clone `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s272/g1532/clone` (push URL set to an invalid value; never pushed); worktrees there are detached; nothing was written under the project folder except the jest lock tickets that `nexusai-lock.sh` itself files.
Re-read at 14:23: origin main still 30b957b438b2dbf4988de8efd27fd5129509c8de, the branch still one ref at 6768b41dd5238b74651f6c3521687deca51c7bed, open PRs 0.
Landing: head-pinned MERGE COMMIT, never squash (CLARIFICATIONS.md:2067, `Merge path`). All findings are Minor; none blocks.

## Findings
| # | Sev | Finding | Evidence |
|---|---|---|---|
| 1 | Minor | The regenerated inventory carries a meta change that is not in the three routes: `meta.fence.dials.total` 9 to 7 (and the page's fence sentence "of 7 lines"). It is not caused by this change: the tool run on an UNMODIFIED main tree prints `dials total 7` and 205 rows identical to main's committed rows, so it is tool or machine drift. Disclosed by the builder; reproduced here independently. The census test does not pin it. | `docs/role-capabilities.json:56`; `docs/ROLE-CAPABILITIES.md` fence paragraph; my `--generate` at main (raw/inv-main.log) and at head (raw/inv-head.log), `invcmp.py` output |
| 2 | Minor | The Settings page shows "Business hours saved successfully!" for any response status, so a refused save (now a 400 with a reason) looks saved to the user. Pre-existing (a 500 looked saved too), `static/**` is another lane's; the builder reported it. Needs its own ticket. | `static/js/settings.js:2825-2829` (`response.json()` then `showSuccessAlert`, no status read) |
| 3 | Minor | `null`, other JSON primitives and malformed JSON never reach the route: the body parser refuses them and the generic error handler answers 400 `{ error: 'Invalid request', message, code: 'UNKNOWN_ERROR', hint }` with no `success: false` and no `invalid` list. The four empty shapes are all 400 with a reason, but the `null` reason is the parser's text, not the contract shape; cell R3 asserts only status and an unchanged file for `null`. The probe server runs NODE_ENV=development; in production the same handler answers `{ error: 'Invalid request', message: 'Invalid request' }` (`backend/server.js:21988-21991`). Unchanged from main (also 400 there). | `backend/server.js:21967`, `:21982`; `__tests__/rd563-agent-settings-validate-before-write.test.js:72-95`; probe `agent|null` and `business-hours|null` |

No Blocker, no Major.

## Observations (not findings; no action asked)
- Tightening, intended by the kit's DESIGN and said in the PR text: bodies main accepted and stored are now 400 (probe, head vs main): a flag of `1` or `'TRUE'`, `null` flag, a non-string role (array/object), a time of `8:30`, `08:30:00`, `24:00`, `08:30 ` or a null Sunday time with Sunday excluded. Callers read in the repo (`git grep` of the three paths): `static/js/settings.js:2803-2830` (HH:MM from `<input type="time">` with no step, `static/settings.html:539-578`), `__tests__/rd408-r2-misconfigured-explains.test.js:423`, `__tests__/rd436-r4-enforce-stamp-and-status.test.js:86`, `tests/e2e/rd436-r4-login-after-selfheal.browser.js:73`: all send valid bodies.
- No length cap on `agentRole` and the other strings (a 1 MB role was accepted, as on main); the body limit is `express.json` 50 MB. Not part of the ticket.
- Plant P12 (the `Array.isArray` clause of `isPlainRequestObject` removed) stays green: an array has none of the field names, so the result is the same. The clause is redundant but harmless (equivalent mutant, not a test gap).
- `C-15` is cited once in a test header comment (`rd563...test.js:6`); 140 test files on main cite `C-nn` entries the same way. The kit's no-id rule names build, seat, card, queue and person ids; this is an in-repo clarification reference.
- The builder's STATUS says it did not read `roles-foundation-route-census.test.js` or CLARIFICATIONS.md whole and took the jest lock three times (kit said one); it also records the kit's P5 prediction as wrong (it is: P5 also reddens H1 and H2). I re-ran the census and everything else it feeds (below).

## Instruments
- Refs: `git ls-remote` of the branch = `6768b41dd5238b74651f6c3521687deca51c7bed` (one ref; `matching-refs/heads/b1532` length 1, control `heads/main` prints the main sha). origin main `30b957b438b2dbf4988de8efd27fd5129509c8de` by `ls-remote` and by `branches/main` (12:04) = the kit's base. Open PRs 0. `rev-list --left-right --count main...head` = 0 3. Commits A c10f605 (3 paths), I 393bf60 (2 docs files), K 6768b41 (counts file) by `diff-tree`; author and committer both the project's configured noreply address on all three.
- Paths: `git diff --name-status main head` = exactly the six OWNS paths (2 added tests, server.js, the two docs files, the counts file); `.github/` 0 (control: 6 tracked files), `.py` 0 (control: 9 tracked), `static/` 0. Census of the 37 `origin/b1*` and `origin/b9*` branches (merge-base diff against the six paths): exactly two touch them, `b1480/nexusai-s-viewer-write-gates` and `b1480/nexusai-s-setup-column-mapping` (control: head itself touches 6 of 6). Overlap with open PRs 0.
- Merge: `git merge-tree --write-tree origin/main head` in my clone, rc 0, tree `9669e066b921bbae13f213b5ed00daf3d59a2194` = the head's tree (head descends from main: main plus the head blobs, nothing else).
- Jest: every run through `nexusai-lock.sh jest` with `NEXUSAI_LOCK_BASE` set to the project's lock folder, `--maxWorkers=2`, `env -u NODE_OPTIONS`; the lock is taken twice (g1532-gate, then g1532-gate2 after the TMPDIR error below), each released by the script. Load gate: two reads under 24 two minutes apart before each filing (15.01 at 12:35, 23.32 at 12:37; 22.64 at 13:36, 8.78 at 13:38). Jest slots computed with the helper's own formula (`sha256(realpath) % 19`): main tree 16, head tree 6, plant copy 4; `lsof` on 20000-32767 read 0 listeners before every chain step. The project harness picks its own port band from the slot, so my reserved block 9960-9969 was not needed and was not used (lsof 0).
- ERROR OF MINE, disclosed here: the first chain exported `TMPDIR` to a folder named `tmp` inside this repo's checkout. The first full verify at head therefore ended `VERDICT: FAIL` (340 suites passed, 3 failed, 45 tests: rd404, rd441, rd731). Cause read at source: `__tests__/helpers/persistent-temp-root.js:48` refuses a temp root whose path contains `/tmp/`, and rd731's "no repository" cell sits inside this repo's own git checkout. Attribution: the same three suites run at MAIN with that TMPDIR fail the same way (47 tests, 2 passed, 45 failed), and at HEAD with the default TMPDIR they pass 47 of 47. The red-first, new-cell, plant, probe, related and inventory steps ran with that TMPDIR (none of their cells depend on it); the verify below is a rerun with the default TMPDIR.
- Full verify at the head tree (tree `9669e066b921bbae13f213b5ed00daf3d59a2194`, default TMPDIR): `VERDICT: PASS - 5612/5612 tests passed across 343 suites (jest exit 0)`, rc 0, `EADDRINUSE` 0 in the log, 13:38:26 to 14:22:54 (44 min; load1 from 7 to 48 during the run), porcelain empty after, no listener of mine left. Committed counts at the head (`git show 6768b41:scripts/verify-expected-counts.json`) = 5612 tests / 343 suites = the measured pair = the arithmetic 5599+13 / 341+2; `scripts/verify-suite.sh` fails a plain run whose measured pair differs from the committed one in either direction, so the PASS is equality. The head tree is the merge tree (see Merge), so this is also the run on the merge.

## Red first, and the plants
New files copied untracked into a main worktree (blobs `cmp` equal to the head's): 3 of 3 runs, 9 red (R1 R2 R3 R4 M1 H1 H2 H5 E1) and 4 green (R5 H3 H3b H4), EADDRINUSE 0. At the head: 3 of 3 runs 13 of 13 green. Received on main, e.g.: R1 and R2 `500` with `settings.json` changed, R4 `200` (wrong types accepted and written), M1 `500`, H5 `200` and written, E1 viewer and administrator `500`.
Plants on a copy of the head tree (script asserts the match count is exactly 1, `node --check`, one run each of the two new files, reverted by copying the original and `git hash-object` = the head blob `e25b90601d95...`, porcelain empty):
| plant | change | received red |
|---|---|---|
| P0 | none | none (13 of 13) |
| P1 | agent check removed | R1 R2 R3 R4 E1 |
| P2 | agent check moved after the first write | R1 R2 R3 R4 (by the byte-identical assertion) |
| P3 | business-hours check removed | H1 H2 H5 E1 |
| P4 | time literal loosened to `[0-9][0-9]:[0-9][0-9]` | H2 |
| P5 | Sunday pair always required | H1 H2 H3 H3b |
| P6 | `/api/models` mapping restored to `([key, model])` | M1 E1 |
| P7 | blank time refused | H3b |
| P8 | `active` forced false | M1 |
| P9 | Sunday pair never required | H5 |
| P10 | string-type check of the text fields removed | R2 R3 R4 |
| P11 | boolean check always true | R1 R2 R3 R4 H1 H2 |
| P12 | `Array.isArray` clause removed | none (equivalent) |
| P13 | `id: model.name` | M1 |
Every cell except the controls R5 and H4 goes red under at least one plant.

## The four body shapes, a real server, both routes (open-access window; probe `raw/probe-main.json`, `raw/probe-head.json`)
| body | main | head |
|---|---|---|
| no body, no content type | 500 | 400 naming all required fields, file unchanged |
| JSON content type, empty body (`req.body` is `{}`) | 500, file changed | 400 naming all required fields, file unchanged |
| `{}` | 500, file changed | 400, same, file unchanged |
| `null` | 400 (body parser) | 400 (body parser; finding 3) |
| `[]` | 500, file changed | 400, same, file unchanged |
`req.body` for a request with no body is `undefined` (Express 5) and the validator treats it as not a plain object. `GET /api/models`: main 500 on every request; head 200 `{ success: true, activeModel: {...}, availableModels: [ one entry, id equal to activeModel.id, active: true ] }`, shape the same as the sibling `/api/models/active` answer; no valid caller existed on main, so none can change (no page calls the path). Valid bodies (agent five fields; strings `'true'`/`'false'`; the Settings page's five-field body; the full seven-field body): the `agent_*` and `business_*` values stored on main and head are equal (compared by program, control: two different bodies compare unequal).
Boundaries on head: `00:00` and `23:59` accepted; `24:00`, `23:60`, `8:30`, `08:30 `, ` 08:30`, `08:30\n` (JS `$` does not match before a trailing newline), `08:3`, `0830`, `08.30`, Arabic-Indic digits, `08:30:00`, `+8:30`, null, array, 1 MB string all refused; blank accepted; an overnight window accepted.

## Handler-span scan, inventory, docs
- No new role gate: gate tokens (`requireAdminFor`, `requireAdminForDataRights`, `requireRiskConditionAdmin`, `riskConditionAdminPasses`, `adminGateRefuses(`, `role !== 'admin'`, `role === 'admin'`) in added lines 0 (control: a planted line counts 2); the validators are module-level functions outside the handlers and the comments inside the three handler spans carry none of those words. `rd978-handler-span-scan`, `roles-foundation-route-census`, `rd929-capability-design-census`, `rd977-inventory-sentinel-word` all green on head.
- Inventory by the tool, not by hand: `node scripts/role-capability-inventory.js --generate --out-dir` run at the head tree (5 min 20 s under load) reproduces the committed JSON (all 205 rows equal, only `meta.generatedAt` differs) and the committed page (`diff` after dropping the `Generated at` line prints nothing); `--check` rc 0. Committed JSON, main to head, by program: rows changed = exactly `GET /api/models`, `POST /api/settings/agent`, `POST /api/settings/business-hours`, only `statusByMode` and `capability`; statuses 401/500/500/500 to 401/200/200/200 and 401/400/400/400 twice; anonymous stays 401; none added or removed. Meta: `generatedAt`, `originMain` (3929b794 to 30b957b4) and finding 1.
- The inventory tool's backups (`printer_logs_backup_*.db` under each tree's `backups/`) were moved to `g1532/_quarantine/`, not deleted.
- Related suites at head (census, rd929, rd977, rd978, rd408, rd436, rd430, rd798, rd799, rd395 and their prefix matches): 21 suites, 267 tests, 267 passed, EADDRINUSE 0.

## Scans over the 388 added lines and the three commit messages (`scan.py`, controls in the same program)
Names (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, plus the commit login and the org name; `(?<![A-Za-z])name(?![a-z])`, case-insensitive): 0 over lines and 0 over messages; control `x_by_<name>_y` fires 1 for each; `kamera pauline` does not. B-numbers, N125, `Datasec/NexusAI-`: 0 and 0 (control `B1532` fires). Non-ASCII 0 and Cf characters 0 (control U+202E counts 1). GUIDs 0, hosts or URLs 0 in the added lines (the three message hits are the `noreply@anthropic.com` trailer), secret shapes 0 (control AKIA string fires). gitleaks over `git diff main head` no leaks (control AKIA-shaped scratch string: leaks found 1).
CodeQL pre-scan, default setup languages `actions`, `javascript-typescript`, `python`, extended suite (read from `code-scanning/default-setup`): added lines in `.py` 0 and in `.github/` 0 (controls above), so only JS applies. JS rows over all added lines, test files included: `new RegExp(` 0, `eval(`/`new Function` 0, `exec(` 0 (the one hit is generated page prose "spawn attempt(s)"), `innerHTML` 0, `child_process` 0, hand-escape `.replace(/[` 0, `chmod`/`makedirs`/mode literals 0, a request value in a `logger` call 0, a request value in `path.join` 0, banned test tokens (`skip`, `only`, `todo`, `each(`, `setTimeout`, `setInterval`, `xit(`) 0; every row's planted control fires. The one regex literal is `/^([01][0-9]|2[0-3]):[0-5][0-9]$/` (anchored, fixed length, no quantifier). The 400 body reflects field names from fixed lists only. A hit would have been a Major; there are none.

## Claims graded (builder STATUS)
| claim | grade |
|---|---|
| A is three paths, server.js +84 -3, two new tests (5 + 8 cells) | true (`numstat` 84/3, 125, 162) |
| Red-first 9 red / 4 green, 3 runs; new cells 13/13, 3 runs | true (mine, same shape) |
| Inventory diff is exactly the three rows plus `dials.total` 9 to 7, drift present at BASE | true (finding 1) |
| `req.body` undefined with no body, `{}` with empty JSON, parser refuses `null`, `[]` is an array | true (probe) |
| Mutations P0-P7 as listed, P5 prediction in the kit wrong | true (mine: P5 reds H1 H2 H3 H3b) |
| Counts 5612/343 = 5599+13 / 341+2 | true (measured 5612/343, committed K equal; A and I carry no counts path: `diff-tree` per commit) |
| No role gate token, no static/ path, no other backend path | true |
| Deploy demo: branch push starts none; a landing would start one, jobs gated on the variable | true (below) |
| OWED pins on the two b1480 branches | true (below) |
| Gitleaks, name, B-number, CodeQL-row scans 0 | true (re-run above) |
| Three lock acquisitions, one scratch boot outside the lock | not checkable by me; process only, no code effect |

## NOT RUN
- A full verify at the main tree for a by-program comparison with head: not run. The first attempt started at 13:35 and was stopped by me (own processes only, lock released by the script) when the TMPDIR error showed; no time was left after the rerun. Main's committed pair 5599/341 is the reference; the head has no red anywhere, so a "red at head, green at main" case cannot exist. The merge tree equals the head tree, so the head run is also the merge run.
- Hosted Build (`npm run verify -- --maxWorkers=2`, `.github/workflows/build.yml:93` at main), CodeQL on the merge commit, gitleaks, npm-audit, arm-ttk hosted jobs, Linux: hosted CI is the proof. A real browser save of the Settings page. No docker or database suite is involved.
- The b1480 branches were only merge-tested, not run.

## FOR TUESDAY
1. **Landing consequence, plainly.** A merge to main touches `backend/server.js`, `__tests__/` and `scripts/`; `deploy-demo.yml` ignores only `**.md`, `docs/**`, `tests/**` (`.github/workflows/deploy-demo.yml:26-32`; `__tests__/` is not `tests/**`), so **Deploy demo WILL start on the merge push to main**. Its `build` job and `deploy` job are both gated on `vars.CI_DEPLOY_ENABLED == 'true'`. Value read now: repository variables `total_count` 0 (`actions/variables`), the repository's view of organisation variables `total_count` 0 (`actions/organization-variables`, answered 200), `actions/variables/CI_DEPLOY_ENABLED` 404; environments list is `["dev"]` only, there is no `demo` environment (the deploy job names `environment: demo`). The last four Deploy demo runs on main (30b957b4, 740b535c, a15fb98c, ac39ab9f) all read `skipped`. Expected here: both jobs skipped, nothing built, nothing deployed. UNMEASURED: a variable value set at a level this token cannot read (the organisation list itself was 403 for `orgs/datasecau/actions/variables`). Against the demo deploy hold (CLARIFICATIONS C-224, still cited as standing in the 2026-11-12 entries): while the variable is unset the hold is not touched; if anyone sets it to `true` before this lands, the merge would build and push an image and the deploy job would be the only stop. Your landing decision; I touched no variable.
2. Open the PR from branch `b1532/nexusai-lane-s-codeql-set` (head `6768b41dd5238b74651f6c3521687deca51c7bed`), wait for hosted Build and CodeQL, then `landing.txt` (merge commit pinned to that head; never squash). Do not make "the alert reads fixed on the PR head" a condition. The check that can fail is main's CodeQL analysis at the merge commit, after landing. This change names no alert.
3. **OWED, a follow-up and not a finding against this branch.** The two stacked branches pin `POST /api/settings/business-hours` at 500 and must change the pin to 400 once this lands: `b1480/nexusai-s-viewer-write-gates` (ef0ff56e1fb7ab87a55617c0632c05a19e728c53): `__tests__/rd958-viewer-write-gates.test.js:37` and `__tests__/rd958-write-gate-path-variants.test.js:49`; `b1480/nexusai-s-setup-column-mapping` (ccb7aa4a10791c8a8f548a7301d41935648ba5c9) carries the same two lines. Both are 45 behind main. `merge-tree` of each with this head: `backend/server.js` auto-merges; conflicts are in `docs/ROLE-CAPABILITIES.md`, `docs/role-capabilities.json` and `scripts/verify-expected-counts.json` (generated files: regenerate after the merge; main alone already conflicts with each on the counts file). Their seat also owns regenerating the inventory (the business-hours row will read 400 plus the gate status).
4. Follow-up tickets this suggests (not asked of the builder): the Settings page status check (finding 2, `static/js/settings.js:2825`, lane F1); RD-691, RD-974 and RD-975 stay excluded as the kit said.
5. Trailer: the standard prints `Co-Authored-By: Claude Opus 5.5` for the merge body; this gate ran on Sonnet 5.5 so `merge-body.txt` says Sonnet 5.5. Change the one line if you want the template string.
6. Files written: this folder only, plus my work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s272/g1532/` (clone, worktrees, raw prints, logs, `_quarantine/`). Nothing deleted.
