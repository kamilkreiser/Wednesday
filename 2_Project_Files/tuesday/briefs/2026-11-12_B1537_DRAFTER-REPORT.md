STARTABLE: YES (kit `2026-11-12_B1537_SEAT-M131_mps-minimatch-alert-10.md`, 102 lines, 9 Stamp slots plus the last line = 10 runs of four underscores, 0 non-ASCII bytes, 0 person names or card ids in the kit text). Drafted 2026-11-12 11:09 to 11:30 AEDT (`date` printed 11:09:26, 11:12:10, 11:15:52, 11:18:57, 11:23:00). Authority: the product owner's 2026-11-12 10:55 live-board ruling, card `datasec-bot-pr-scan-back-1112` option a ("the MPS and HPSM minimatch alerts each get a small lane"). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1537/` (trial copies, raw files at the pinned shas, the Jira/gh helpers).

## BLUF
- A patched release exists (alert 10: minimatch, medium, development, transitive, range `>= 7.0.0, < 11.0.1`, first patched `11.0.1`), so this is a BUILD kit, not a report kit. Only the `node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch` copy (10.2.6) is in range; 3.1.5 and 5.1.9 are not.
- **No parent release reaches 11.x**: typescript-estree 8.60.0 to 8.72.2 (latest) all declare `minimatch ^10.2.2`, and minimatch 10.x ends at 10.2.6. So the narrowest change is an `overrides` entry scoped to the one parent: `"overrides": {"@typescript-eslint/typescript-estree": {"minimatch": "11.0.1"}}` (an unscoped override is forbidden in the kit: eslint needs minimatch 3).
- **I ran the update on a COPY (TRIAL) with the pinned tool node v24.22.2 / npm 11.19.1:** no-change control kept the lock blob `7c7d4608...`; the update gave manifest blob `b7ceb57f3b04...`, lock blob `610a0767543c...`, lock diff 12 added 4 removed, exactly two entries (new `@isaacs/nonrecursive-glob-match` 1.1.0; estree-nested minimatch 10.2.6 -> 11.0.1), matcher VULN -> clear, `npm audit` 7 moderate -> 0. These are predictions in the kit, never files to copy.
- MPS has **no docker** (the M129/M130 kits forbid it): the regeneration is the host-side pinned node, copied from the M129 conventions (project heavy slots `.tools/.heavy-lock-1/-2`, `.tools/.git-lock`, clone from `2_Project_Files --no-checkout`).
- 0 open PRs, 0 live overlap on `web/package*.json` (4 old branches touch it, none live; the 12 `^b15` branches none).

## Facts re-measured (instrument; control)
- Main `5239020234b416c6c2c07f8a7912d88830de6f7f` (`branches/main`; one parent; the squash of #186; moved at 11:07 from the `793d0a9c` the B1533 kit read). Its `web` job was still `in_progress` at 11:17 (`commits/<sha>/check-runs`, `actions/runs?head_sha=`); other rows success. Hence the kit's base run is the control.
- Blobs: lock `7c7d4608f669a19e4b52c963cdb4debb81d6f879`, manifest `f74032cf4fae0b00ea26d2efc984f4a58f1fa9fb` (contents API `.sha` = `git hash-object` of the raw copy; the lock blob equals the 11-04 #158 head's). Tree 791 paths, `web/` is the only npm project (control: `.github/workflows/ci.yml` listed).
- Alert 10 read whole (`dependabot/alerts`); control `alerts/9` HTTP 410; `state=fixed` 1 to 8. Same GHSA as the withdrawn alert 9 of MPSCALC-384 (Done 2026-11-06, closed "withdrawn"; read whole with its one comment: it says a returning advisory "needs its own ticket"; the range is now narrower).
- CI predicate read from `ci.yml` (139 lines): `web` job `:45-82`, node 24 `:58`, `npm ci`/`lint`/`test` `:61-63`, two Playwright modes `:69-79`, entra build + `check-bundle.mjs` `:82`. Playwright reporter/ports from `web/playwright.config.ts` (`MPSCALC_E2E_MODE`, `MPSCALC_WEB_PORT`) and `vite.config.ts` (`DEFAULT_API_ORIGIN` 5080, so the api-off mode gets a dead origin on 9929).
- Overlap: `compare` for 209 branches (control: 4 historical hits show the loop sees manifest edits); kits of B1527, B1530, B1533 name the manifests 0 times, B1536's kit forbids them (line 70).
- Ports 9920-9929: `lsof` 0 rows (control 12 listeners); word-boundary scan of 51 SEAT kits 0 hits (control `989[0-9]` found B1533, B1536).
- Jira (own GET-only helper, `.env` in-process, `project = MPSCALC AND ( ... )`): no ticket carries alert 10 (control `key = MPSCALC-361`).
- Model: `model-routing.md:92` row C2; `models_latest.json:23`; `brief_seat.sh:24` default opus.

## D-decisions
- D-1 version `11.0.1` (first patched, 16 days old) over 11.0.8 (1 day old, engines narrowed).
- D-2 override scoped to `@typescript-eslint/typescript-estree` only; edit by the Edit tool on the MANIFEST; the lock only ever by npm.
- D-3 a newer 1.x of the new glob-match package at run time is recorded and allowed (only that entry).
- D-4 two paths only (`web/package.json`, `web/package-lock.json`); evidence folder carries six files (the five of the template plus `ticket-text.txt` for records).
- D-5 identity: the project's configured identity by program (the repo's `2_Project_Files` config prints a Datasec address; seat commits on b1526/b1528/b1530 carry it as author and committer); never typed here.

## Q-questions for Tuesday (each with a default)
- Q-1 Pin `11.0.1` or the newest `11.0.8`? Default `11.0.1`.
- Q-2 Seat reads/writes no Jira; should a new MPSCALC ticket be filed from the seat's `ticket-text.txt` after landing (MPSCALC-384's own comment asks for one)? Default yes, Tuesday's records step.
- Q-3 If a typescript-estree release admitting minimatch 11 appears before launch, STOP (default) rather than switch lanes.
- Q-4 If the pinned npm rewrites the lock on the no-change control: STOP with both blobs (default). (The trial did not.)
- Q-5 The hosted `web` job at main was still running at 11:17: if it ends red, does that change the stamp? Default: the seat's own base run decides; Tuesday reads the hosted result before launch.

## UNMEASURED
- Whether the real `npm ci` + lint/test/e2e at head are green (the drafter ran no `npm ci`, no build, no test, no browser); only the lock regeneration and audit were tried, on copies.
- The hosted runner's npm (floats in Node 24) vs the pinned 11.19.1: not compared.
- Hosted CodeQL, and whether the bot-less route needs anything beyond the plain push.
- Whether Dependabot closes alert 10 on landing (it did for #158: RELAYED).
- Wall time of the e2e on this machine under shared heavy slots (slot 1 held at 11:12).

## Outside-the-fences disclosure
- Network beyond `gh -X GET` and Jira GET: **`registry.npmjs.org` GETs** (packuments for minimatch, typescript-estree, typescript-eslint, glob-match) via python `-I` urllib, and the trial's `npm install --package-lock-only` and `npm audit --package-lock-only` (the latter POSTs to the registry's advisory endpoint) run with the tool node under a scratch HOME/cache, on COPIES in `.../d1537/trial_mps/` only. No `npm ci`, no build, no docker, no az, no ssh, no repo write, no ref write, no git fetch/pull/worktree/checkout in any project repo.
- Read other seats' kits (readable claims): B1533, B1536, B1527, B1530, B1535 (grep only for manifests and ports). Did not open `decision_queue.sh`, `fleet/briefs_staged/`, the scoreboard, `_ledger.md`, or WEDNESDAY/FRIDAY trees.
- One `gh` call printed an "admin:repo_hook scope" message beside a 410 (alerts/9/1); no write was attempted. Scratch also holds a few error-JSON files (`main__.nvmrc`, `main__package.json`, `main__package-lock.json`, `main__web_.nvmrc`: 404 bodies from probing absent paths); `cmp_one.sh.bak` came from a scratch-only `sed -i.bak`. Nothing outside `d1537/` plus the two kit files and this report was written.
