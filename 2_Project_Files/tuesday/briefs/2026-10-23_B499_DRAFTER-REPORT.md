# B499 drafter report (read-only; two files written)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B499_SEAT-D29_hpsmpoc-demo-redeploy-486e74e.md` (218 lines). Cloned from B402 (demo, 184 lines, read whole) + its ADDENDUM-1 + B402 STATUS (544 lines; the resumed part 349-544 whole) + B498 (UAT brief 98 lines and STATUS read for packages, deploy, AFTER, FOR TUESDAY). No az, no HTTP to any hosted host, no fetch/pull/push, no docker/ssh. gh GET only with the project's GH_CONFIG_DIR.

## The demo's current deployed sha, and how I know
`ec0a62a1ac107e26d859b5eebd220153a0cf691c`, web build `J4BEdU3NsTbseZT_47jB0`, live since 2026-10-21T02:09:12Z. Source: last line of `Briefs/2026-10-21_B402_STATUS.md` = `DEPLOYED: ec0a62a @ J4BEdU3NsTbseZT_47jB0` (the newest STATUS last line `DEPLOYED:` that names `hpsm-poc-demo-rg` as a deploy target; loop over `Briefs/*STATUS.md` last lines). Every later `DEPLOYED:` (B410, B437, B443, B470, B498) is UAT; B498 FOR TUESDAY item 2 states the demo is still on next 16.3.8 and untouched. B403 is the records step for B400/B402. **Not proven live today** (no HTTP/az): the brief makes the public home-page build id the first read and STOPs on any id other than J4BE.../AuuX.../3cBX...

## Delta ec0a62a..486e74e6 (gh api compare, GET; cross-checked by local `git diff` in 2_Project_Files)
17 commits (ahead_by 17, behind 0, one parent each), 80 files, +5,605 -265, name-list sha256 `3135130775f1...cf569` (the list is embedded in the brief). Both shas are in the local object store. Commits: #171, #176 (product name/spelling), #177-#181 (UAT open sign-in/template/badge/header/login), then B498's ten (#182 #183 #185 #187 #186 #184 #188 #190 #191 #189). Shipped: API (UatOpenAuthentication + Program.cs, Assessment/Feedback/Reporting changes), web (next 16.4.2 + lockfile, uat mode code, product-name edits on every screen). Not shipped: 22 api tests, 12 web unit tests, 6 e2e, ci.yml, infra.

## Migration / config / infra (the thing to look at)
- Migrations: none (no Migrations/.sql/appsettings/.csproj/global.json/scripts path; blobs of deploy-from-ci.sh, deploy-package.py, appsettings.json, global.json equal at both shas; FirstVisitWarmup.cs and Caller.cs byte-equal).
- **Risky pathspec = exactly 7 hits (verified with git diff):** ci.yml, infra/README.md, infra/env/uat.bicepparam, infra/modules/appservice.bicep, infra/tests/test_security_baseline.py, web/package.json, web/package-lock.json. The lineage (B273..B402) never applies Bicep, and B402's rule would STOP on a .bicep/infra path. I did NOT silently waive it: made it **Stamp ruling 5** (blank = STOP before step 6). The package.json/lockfile hits are the intended next bump (proved by version proof, not a ruling).
- appservice.bicep is shared: a later template deploy of the demo would add 5 setting names (API 34 -> 36, web 15 -> 18, values off/empty). Not done here; flagged for FOR TUESDAY.
- New code reads 5 new names (Auth:UatOpen:Enabled/Key, HPSM_UAT_OPEN_SIGNIN, HPSM_ENVIRONMENT, HPSM_UAT_OPEN_KEY), all gated behind the UAT switch (read config.ts, UatOpenAuthentication.Read, routes.ts, Program.cs patches: off/404 when absent; web also needs a site name containing "-uat-"). Brief requires those 5 names ABSENT on the demo (STOP otherwise) and `GET /api/auth/uat` != 200.

## Other measurements
- Main = 486e74e6 (ls-remote in 2_Project_Files and gh ref API); open PRs `[]`; CI run 39840292589 attempt 1 completed/success; artifacts deploy-web id 12453482282 (15,787,957 B, exp 2026-10-29T19:45:49Z), deploy-api id 12453009322 (49,643,602 B, exp 2026-10-29T19:43:40Z), expired=false. Seat's fetch must reproduce B498's sha256: web 7a8f6bec...76b9, api 93ac02eb...59c4.
- Rollback: run 39526511311 artifacts web 12313843314 (exp 2026-10-28T01:24:53Z), api 12313494186 (exp 2026-10-28T01:28:57Z), expired=false; local `.tools/wt-B402` HEAD = ec0a62a1, web.zip `ae63b6e3...f9371` and api.zip `eb8e4cd6...133f` match B402 STATUS (shasum, read-only).
- Ports 8470-8479: lsof rc 1 (no listeners); no brief names them. Pane Datasec/HPSM-POC-D29 absent. Load 4.40/3.27/2.92 at 07:12.

## Lineage differences (disagreements with the instruction / with B402)
1. **Web package census:** B402's six-class path census is infeasible on a next minor bump (B498: 558 differ, 340 old-only, 442 new-only vs 4695d7f2). I replaced it with: sha256 equality with UAT's package, next/@next/* only in node_modules, marker survival (keepAliveMaxTimeout, [warm], logout_hint, RETURN_SEGMENTS...), UAT strings inert. A lineage change, not a copy; Tuesday may prefer otherwise.
2. **Customer-visible words on the demo:** #176 renames the product on every screen (header, title, phase flow), and #186/#187 add refusal messages, a merged-summary sentence and a profile caption. The grant excludes unapproved customer-facing words, so **Stamp ruling 6** needs a C-number/citation (I found B407/B413 "option b" but no C-number; not looked up on records).
3. **Sample-customer PDF may change** (ReportModelBuilder caption, Providers): B402's "difference you cannot trace -> way back" is softened to **ruling 7** (untraceable difference on a healthy site = STOP, no auto-rollback, like B498 ruling 3). Health/boot/required-line misses still roll back.
4. B402's every-table SQLite snapshot dropped (the write is untouched); the warm-up line stays as a regression guard. #173 hosted items dropped (measured by B402).
5. #190 has no separate QA-gate STATUS (as in B498): ruling 4 covers all 17 commits; I listed the gate records I found per PR (B404, B413, B417, B421, B435, B441, B463, B488, B491, B492/B494, B495); #182/#183/#185/#188 marked test/CI only.
6. UAT counts (35/17) are not the demo's: the brief carries B402's 34/15. Demo plan/settings/activity since B402 are UNMEASURED (I found no B408/B433 STATUS); the carried platform-state rule applies.
7. I did not verify whether ci.yml has an automatic demo deploy job (daily note 10-22 mentions "Deploy demo SKIPPED" on an earlier push); the brief makes the seat read it and STOP if one ran.

## Stamp-slot lines (12 runs of four underscores; `grep -o -E '_{4}' | wc -l` = 12, five-underscore control 0)
Stamp time/B-number; launch authority; hard stop (suggest 10:00 AEDT); rulings 1 CI-green, 2 single image GET (default NOT ALLOWED), 3 read-only copy of wt-B402 packages, 4 "gated" for #190 + the rest, 5 infra paths (not shipped, not applied), 6 words (two slots: C-number, citation), 7 visit-difference handling; READ-WHOLE-BY-TUESDAY (last line). Slots 5-7 are beyond your list; delete them if you rule differently in the text.

## Slips
First draft of the risky-pathspec line said "9" then "VOID: 7"; fixed to 7 and re-verified by git diff before finishing.
