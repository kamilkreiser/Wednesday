STARTABLE: YES

# B1696 drafter report (SEAT-D68, HPSM-POC UAT deploy of 36c557ad), 2026-11-18, drafted 08:38 to 08:45 AEDT

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1696_SEAT-D68_hpsmpoc-uat-deploy-36c557ad.md` (118 lines, 21 unfilled slots by `/usr/bin/grep -c '_''___'`, MEASURED 08:43:16). Sidecar `.measured`: `stamp_check.py <kit>` printed `94 claims, 94 measured, 0 not measured`, rc 0.

## BLUF
- The deploy route does NOT re-run CI or the dev-tools audit, so the picomatch advisory does not block it. `deploy-from-ci.sh` (byte-equal at b81793d1 and 36c557ad, sha256 prefix `5688b48e155d1694`) lists the existing green `ci` run for the sha (`:49`), downloads its two artifacts (`:55`) and runs two `az webapp deploy` (`:68`, `:69`). Nothing is dispatched or built. The step that would fail on any NEW run is `node scripts/audit-dev.mjs` at `ci.yml:395` (job at `:372`). The kit forbids any CI trigger, rebuild or `npm install`. If an artifact has expired, the seat STOPs (a rebuild needs a new run, which would fail the audit; that is a decision, not a bypass).
- Main is `36c557ad9255125793bfeb99abdea3b0b4d988e2`: ahead of b81793d1 by 2 first-parent commits (#332 next 16.4.2 to 16.4.5, #333 one test), 3 files (`web/package.json`, `web/package-lock.json`, one `.test.ts`), 0 migration, 0 `.sql`, 0 `infra/`, 0 `scripts/`, 0 non-test `web/src`, 0 `api/`. Open PRs 0, open code-scanning alerts 0.
- CI at 36c557ad: `ci` run 44075419064 push success attempt 1; 21 check-runs success, 1 skipped (PR-only dependency review). Artifacts `deploy-web` 14324573820 (expires 2026-11-24T11:47:37Z) and `deploy-api` 14325822354 (expires 2026-11-24T11:53:20Z), `expired` false.
- The rollback target is b81793d1's packages, already on disk and hash-checked (below), plus live CI artifacts to 2026-11-24T00:59Z.
- Model: row C6, Opus, `model-routing.md:96`, `claude-opus-5-5` at `models_latest.json:17`; launch line carries `BRIEF_SEAT_LEVEL=opus`.

## Facts re-measured (instrument, clock)
- Card text: `decision_queue.sh show <exact id>` into scratch (08:38:07): title "HPSM-POC: deploy the next 16.4.5 security patch to UAT?"; option [a] label `Deploy to UAT now`, detail `Main 36c557ad to UAT by the usual runbook (backup, rollback, live check), reported after`; status ruled, choice a, ruled_ts 2026-11-18T08:36:04+11:00 (the board's 08:35:31 is the commission's clock). Card id is in this report only, not in the kit text.
- main sha, compare, PR merges, head shas: `gh api -X GET` (08:38:19). #332 merge `6c1aa32e2e8082ece9f00a7267c60d6e0473b8b5` head `5e9a3d4066007983b81980e04386ba976fd403f0`; #333 merge `36c557ad9255125793bfeb99abdea3b0b4d988e2` head `c2ed21d684482f5566f13ed7d91363d37cd916ba`. Gates: B1673 `GO WITH FINDINGS @ 5e9a3d4 on main b81793d`, B1676 `GO WITH FINDINGS @ c2ed21d on main 6c1aa32` (first lines read 08:40:07; no Major rows).
- What UAT runs now: UNMEASURED live (fence 4: no HTTP to a hosted host). RELAYED: B1662 STATUS last line `DEPLOYED B1662: b81793d1...`; `tail -n 1` over every `*_STATUS.md` (08:41): newest DEPLOYED/ROLLED/PARTIAL is B1662 (control: 6 rows list). The seat reads the live page at Step 0.
- Packages (gh api artifact zips into scratch, 08:39): web.zip 20034d2f257a345461e8a803231c7597cb59bc769de57051f48f79334b984073, 17,024,660 B, 2115 files; api.zip 7d2ce082364f45502dc1809c5f664e8938bfe60da7b27dab22ce7da5b6876955, 49,760,523 B, 126 files; both MANIFEST commit 36c557ad, run 44075419064; SQL scripts sha256 equal to the ones B1662 recorded.
- Package compare vs PREV's packages on disk (python -I -B): API 126=126, 10 differ (five DLL, five pdb), TARGET sha embedded 5, PREV sha 0. Web 2115=2115, 147 only-old / 147 only-new (chunks), 372 differ: `.next` 615 path-changes, `node_modules` 50, `package.json` 1. The 50 node_modules changes are `next`, `@next/env` and one removed `react/cjs/react.development.js`; react stays 19.2.8; next 16.4.2 to 16.4.5; BUILD_ID `c8yfRyH9dvB3iEk0L1Str` to `d6pnCRzVbiP6IZ5MMle3R`. NOTE: B1662's `pkgcmp1662.py` asserts `node_modules/` 0 differences; that assertion is wrong here and the kit tells the seat to hand-edit it to the measured property (Package checks 4).
- Rollback packages: `.tools/b1662/repo/out/deploy-packages/b81793d15f41d133f5c2657329e31aef3ac00322/` web sha e3b1d575...417e7 (17,073,664 B), API 4f69dcc1...e2e (49,760,533 B), RUN 43990429511; repo HEAD b81793d1, push `DISABLED-no-push` (08:41).
- Tools to copy (sha prefix / lines, 08:41): identity_pass1662.sh d1dd10fc 19; lib1662.sh 496f2966 42; deploy1662.sh f546badc 72; livepred1662.sh 0bedb0f7 55; rollback1662uat.sh 43ef0382 39; live1662.py e8ac942c 55; startlog1662.py 479b8dfa 54; presig1662.py 08f9967d 245; setdiff1662.py 95d26959 20; pkgcmp1662.py 8ac62029 305; closedlist1662.py 934e65ff 30; words1662.py 355e5b61 30; smoke1662.cjs 8548d85c 73; measure1662.mjs 1aa8b4a8 107.
- Ports: kit takes none. `lsof -nP -iTCP:9800-9999 -sTCP:LISTEN` 0 listeners; no `HPSM-POC-D*` pane in the (first 10) `tmux list-panes` lines; no other B1696/D68 file before mine.
- Advisory GHSA-fc5q-39xc-vjpf (gh api -X GET advisories): picomatch `<= 4.0.7`, high, no patched version; the GitHub record shows published 2026-10-19 (not 11-17; the commission's "since 11-17" is when CI began to fail on it, RELAYED, and I did not measure why).
- Dependabot note: `next@16.4.6` exists (gate B1673 finding 2); out of scope, written into the kit as not covered.

## D-decisions (all in the kit)
- D-2 live site is the pass predicate (B1609 ruling), no second attempt. D-7 words check by diff alone (no non-test web/src file). D-8 no page-text walk: widen at stamp if wanted. D-10 the framework patch is the real risk (runtime rendering, caching, headers on the hosted copy), covered by smoke on seven routes, a recorded (not graded) cache-header read, the 16-box page check AFTER = BEFORE, a 5-minute stability hold, a proven way back.
- The BEFORE old-build control of B1662 no longer applies (the unit-box change is deployed); the kit replaces it with "BEFORE must read one width, else STOP".

## Q-questions for Tuesday (defaults)
- Q-1 Both apps deploy (script has no web-only form; API is only re-stamped). Default: both, as B1662. Alternative: hand web-only deploy, a new write class this kit does not carry.
- Q-2 "backup" in the card detail: kit reads it as the platform point-in-time restore plus PREV's kept packages (no schema change, as B1662, accepted then). Default: no database copy. Say if the product owner meant one.
- Q-3 Page-text walk (D-8): default none. Say if you want the 292-page walk because the framework changed.
- Q-4 The picomatch advisory will fail the next PR's CI. Not this seat's work; consider a card for how the audit step treats a no-fix dev-only advisory.

## UNMEASURED
- Live UAT build and health (no hosted HTTP by the drafter); that `audit-dev.mjs` fails today (it reaches the registry, not run); the actual deploy gap (B1662 saw 0 non-200 at 10 s ticks, RELAYED); `az` anything; the stub runs and the verify commands (the seat runs them); whether the activity log holds rows since 2026-11-17T04:22Z.

## Chain inputs (rule 4)
Step 0.4 copy: input = B1662's kept PREV packages, exist at BASE. Build 3 fetch: input = CI run 44075419064 artifacts, exist at BASE. Build 4 pkgcmp: inputs = Step 0.4 copy and Build 3 fetch (both earlier). Build 5 instruments: inputs = `.tools/b1662/*` at BASE. Build 6 stub run: inputs = Build 5 rollback script and Step 0.4 folder (earlier). P1 smoke/page check: inputs = Build 5 tools and live site at BASE. P2 deploy: inputs = Build 3 packages, Build 6 proven way back. P3: inputs = P1 BEFORE tables.

## Outside-the-fences disclosure
- Read: DRAFTER_RULES, the B1662 kit, STATUS, B1664/B1672/B1675/B1673/B1676 first and last lines, model-routing and models_latest lines, `.tools/b1662/` (ls, shasum, wc, rev-parse, remote -v on the project dir; read-only), the card via `show` of the one id. `gh api -X GET` only, under the project GH_CONFIG_DIR, with `-R`/repo path explicit (the default repo of that config printed a different repo, `kamilkreiser/Wednesday`, in a `gh repo view` probe I ran first: no write, but note the default is wrong, always pass the repo).
- Wrote only: the kit, its `.measured` sidecar and this report; scratch files and two downloaded artifact zips in the session scratchpad (`.../scratchpad/art`, `cmp.py`, `cmp2.py`, script copies).
- No az, ssh, docker, no HTTP to any hosted host, no Jira, no `list`, no git ref writes. One slip: `echo =====` was refused by the zsh hook (harmless).
