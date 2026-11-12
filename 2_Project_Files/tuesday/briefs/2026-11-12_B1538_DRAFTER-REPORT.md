STARTABLE: YES (kit `2026-11-12_B1538_SEAT-H161_hpsmpoc-minimatch-alert-9.md`, 104 lines, 9 Stamp slots plus the last line = 10 runs of four underscores, 0 non-ASCII bytes, 0 person names or card ids in the kit text). Drafted 2026-11-12 11:09 to 11:30 AEDT (`date` printed 11:12:34, 11:15:52, 11:18:57, 11:23:00). Authority: the product owner's 2026-11-12 10:55 live-board ruling, card `datasec-bot-pr-scan-back-1112` option a ("the MPS and HPSM minimatch alerts each get a small lane"). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1537/`.

## BLUF
- Patched release exists (alert 9: minimatch, medium, development, transitive, `>= 7.0.0, < 11.0.1`, first patched `11.0.1`): a BUILD kit. Same shape as the MPS lane: only the estree-nested minimatch 10.2.6 is in range; no parent release reaches 11 (typescript-estree 8.60.0 to 8.72.2 all `^10.2.2`; `eslint-config-next` 16.3.6 asks `typescript-eslint ^8.46.0`, which floats to the same estree); so a scoped `overrides` entry, `11.0.1`.
- **PREMISE CORRECTION (the braces question):** there is NO live braces exception at main `c717ba1a`. `web/scripts/audit-dev.mjs:2-3` says the list is EMPTY and the ruling lapsed (advisory withdrawn 2026-10-23), `:11` `EXCEPTIONS = Object.freeze([])`, `:12` blocking = high/critical; `ci.yml:391-393` says "no exception is in force. (... braces ... lapsed ...)". `2026-11-30` exists only as a SYNTHETIC fixture in `web/src/audit-dev.test.ts` (:15, :37-38, :68, :74, :88; :51 asserts the list is `[]`). Minimatch is not in any allow-list (there is none), and it is `moderate`, so it never blocked CI. The bump takes the audit counts line from moderate 7 to 0 (TRIAL); nothing is widened and the kit forbids touching `audit-dev.mjs`, its test and `ci.yml`.
- **TRIAL on a COPY**, both toolchains (tool node v24.22.2 / npm 11.19.1, and the project's `.tools/node24` v24.21.0 / npm 11.19.0): the no-change control kept lock blob `81393fd7...` under both; the update gave manifest blob `b549f7f554e1...`, lock blob `add1be79fe97...`, 12 added 4 removed, the same two entries as MPS, 589 -> 590 entries, matcher VULN -> clear, `npm audit` 7 moderate -> 0.
- Parallel lane: B1535 (messaging) owns `web/src/**` product files and two e2e specs; names neither manifest (count 0). No HPSM pane is live yet. 15 old branches touch the web manifest or lock, all at least 108 commits behind.
- E2E: the kit runs all eight CI shards at HEAD (the base only for a red shard, Q-4) because the change is a lint-time dev dependency; the unit suite, lint, typecheck, build, the production tree (`npm ls --omit=dev` byte-equal) and the repo-wide hidden-character scan (DRAFTER_RULES item 8) run at both.

## Facts re-measured (instrument; control)
- Main `c717ba1a945191ffa31f13320c19967a6cf7f15a` (one parent; the SDK-pin squash). 22 check-runs, all success except the PR-only `dependency review` (skipped). Open PRs 0 (control: `state=all` printed #313..#311 closed).
- Blobs: lock `81393fd77c36489b3e8b17a13bde28e225350fb4`, manifest `2e7ed8b306e8a9a8d8a9ce507c4129dc6444d2c8` (contents API `.sha` = `git hash-object`). Tree 1807 paths: `web/package.json`, `web/package-lock.json`, `web/.nvmrc` (24) only.
- Alert 9 read whole; controls: `alerts/1` 410, `state=fixed` 2 to 8, 7 rows. Lock: 589 entries, estree 8.70.1 at `:2787`, nested minimatch `:2838`; 8 minimatch dependents (control: brace-expansion copies listed).
- CI read from `ci.yml` (682 lines): `web-build :371`, `web-unit :450`, `web-e2e :483` (8 shards, `:494`), `web :529`, `infra :578`, `dependency-review :668`; node 24 at `:384,:463,:504`.
- Infra tests: none reads `web/package*.json` (58 scripts/infra files at depth <= 3 fetched and grepped; hits are synthetic fixtures; control: `ci.yml` named by 3 files).
- Ports 9930-9939: `lsof` 0 rows (control 12); scan of 51 SEAT kits 0 hits (control `968[0-9]` found B1504, B1506). e2e env ports read at `web/playwright.config.ts:4,21,22,25`.
- Playwright cache holds chromium-1208/1234/1243 (no download needed); `/Applications/Google Chrome.app` exists.
- Jira (own GET-only helper, `project = HPSMPOC AND ( ... )`): no ticket carries minimatch or the GHSA; precedent HPSMPOC-346 (fast-uri) read whole; HPSMPOC-218 (braces) listed.
- Model rows as in the MPS report; HPSM kit says READY target Step 0 + 240 min (eight shards).

## D-decisions
- D-1 `11.0.1`, scoped override; D-2 manifest edit with the Edit tool, lock only by npm; D-3 a newer 1.x of the new glob-match entry is recorded and allowed.
- D-4 the override block is the LAST manifest key (after `engines`), five added lines, 0 removed (TRIAL).
- D-5 two clones by URL (`repo` = base, `head` = work), the HPSM convention of the B1503/B1519 kits; seat-local heavy lock plus the load gate (HPSM has no shared project slots; B1535 holds its own, so the gate bounds the machine).
- D-6 second no-change control with the project's own `.tools/node24` (both reproduced the lock in the trial).
- D-7 never edit `audit-dev.mjs`, `audit-dev.test.ts`, `ci.yml`; any new high/critical row at head: STOP.

## Q-questions for Tuesday (each with a default)
- Q-1 Pin `11.0.1` or `11.0.8`? Default `11.0.1`.
- Q-2 No Jira reads/writes by the seat; `ticket-text.txt` (including the braces-premise correction) for Tuesday's records step. Default yes.
- Q-3 If an estree release admitting minimatch 11 appears before launch: STOP (default).
- Q-4 E2E base re-run only for shards red at head (default), or all eight at base as well (about doubles the time; raise READY to 420 min)?
- Q-5 If either pinned npm rewrites the lock on the no-change control: STOP with both blobs (default).
- Q-6 Is the "braces exception lapsing 2026-11-30" premise from the stamp text a memory of an earlier state (the 2026-10 `b571`/`b242` branches carried it)? Default: yes, stale; Tuesday corrects the note.

## UNMEASURED
- Real `npm ci`, lint, typecheck, build, unit and the eight shards at head and base (the drafter ran none; only lock regeneration and `npm audit` on copies).
- Whether the machine's Playwright/Next versions equal hosted; the e2e wall time; whether B1535's seat contends for the heavy load.
- Hosted CodeQL and `dependency review` on the PR; the `postbuild`/deploy-package step's behaviour with the new nested copy (the prod tree should be unchanged).

## Outside-the-fences disclosure
- Network beyond `gh -X GET` and Jira GET: `registry.npmjs.org` GETs (packuments via python `-I` urllib) and, in `.../d1537/trial_hpsm/` COPIES only, `npm install --package-lock-only` (twice per toolchain) and `npm audit --package-lock-only` (POST to the registry's advisory endpoint). No `npm ci`, build, docker, az, ssh, repo write, ref write, fetch/pull/worktree/checkout in a project repo.
- Read the HPSM `.tools/node24` binaries by running `node -v`/`npm -v`/`npm install --package-lock-only` in the scratch copy (a project tool, read-only use). Read other kits as readable claims: B1519, B1503 (grep), B1535, B1536. Did not open `decision_queue.sh`, `fleet/briefs_staged/`, the scoreboard, `_ledger.md`, or WEDNESDAY/FRIDAY trees.
- Scratch also holds `hpsm_scan/` (58 fetched script files) and `hpsm_infra/` (infra tests and web scripts at the pinned sha) for the greps; nothing outside `d1537/` plus the two kit files and this report was written.
