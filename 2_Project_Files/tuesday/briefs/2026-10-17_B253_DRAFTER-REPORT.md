# B253 DRAFTER REPORT: HPSM-POC hosted deploy of main 72073da (SEAT-F3)

**Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B253_SEAT-F_hpsmpoc-hosted-deploy-72073da.md` (sha256 `6b71fbf86697d7603a8dd3ba74c387b077fead0ee166e56e49f84f8813082d69`, 09:37 AEDT 2026-10-17).
**Drafter scope:** read-only. No write under `!CODING/`, no `az`, no HTTP to any hosted site, no fetch/checkout/worktree. Reads: `git --no-optional-locks` (ls-remote, rev-parse, cat-file, diff, grep, ls-tree) and `gh api` GETs with the project `GH_CONFIG_DIR`.

## Measured (this session, 09:31–09:37 AEDT = 2026-10-16T22:31–22:37Z)
- **Main:** `ls-remote origin refs/heads/main` = `72073dace1635899e1262548e561781073b4c7b4` (09:32:42). `refs/heads/b251/imports-bff-hardening` = `9195408f…`.
- **Merge commit (GitHub commits API):** tree `e161c831fb692056b54b91cdcc1e2603315c414d`, one parent `d916baf7…`, committed 2026-10-16T22:14:13Z, 14 files +663/−27. **Tree = B252's gated head tree** (`B252_STATUS.md:14` "tree e161c831fb69 = head tree", `:84`; and `rev-parse 9195408^{tree}` in `.tools/b252/repo` = `e161c831…`). DELTA 202's "merge tree == gated tree" is confirmed.
- **Range (compare API):** `d916baf...72073da` ahead 1, behind 0, 1 commit. Files: AssessmentModule.cs +1/−1, ImportEndpoints.cs +40/−6, ImportPendingSweep.cs +9/−2, JiraRestMailSink.cs +1/−1, FeedbackEndpoints.cs +1/−1, ShapeAnchorTests.cs, ImportPendingSweepLoopTests.cs, 2 infra tests, scripts/deploy-package.py +24/−5, bff.ts +22/−3, formGate.ts +67/−4, 2 web tests.
- **Risky paths / config** (local diff on `9195408` in `.tools/b252/repo`, same tree): only `infra/tests/*` ×2 + `scripts/deploy-package.py`. 0 migrations (84 = 84 migration paths), 0 `.sql`, 0 appsettings, 0 bicep, 0 `.github`, 0 csproj, 0 package*.json. Config-pattern added lines in `api/src` 0 (control 1). `process.env` added 0. `appsettings.json:17` `ImportsEnabled: false`. Contract `0.17.1-draft` ×2.
- **Store writers changed:** `SaveIfStillPendingAsync` (`ImportEndpoints.cs:216`, `:223`) on the upload path only (`:160/:164/:187`); every import route has `ImportsSwitch` (`AssessmentModule.cs:263-268`, `ImportEndpoints.cs:411-419`); sweep registration `AssessmentModule.cs:123` gated on `ImportsEnabled`. No new hosted service, no startup writer.
- **CI on 72073da:** `ci` 38974522883 push attempt 1 success (jobs 14 success + 1 skipped); CodeQL "Push on main" 38974522543 success; 19 check-runs = 18 success + dependency review skipped (4 Analyze success). Open code-scanning alerts on main 0. Open PRs 0. PR #156 merged 22:14:14Z, head `9195408`.
- **Artifacts:** target run 38974522883 web 15,358,881 B (exp 2026-10-23T22:21:13Z), api 49,387,048 B (exp 22:27:53Z). Way back run 38470487072 web 15,358,552 B (exp 2026-10-20T21:33:27Z), api 49,385,788 B (exp 21:39:15Z), all expired=false.
- **Live today (records):** B249 last line `DEPLOYED: d916baf @ _8fw76mEajOsf7FyCTWP2` (`B249_STATUS.md:212`); its After (`.tools/b249/after/summary.txt`): deployments web `a3b65135…`, API `c4ada9cc…`, DLLs d916baf ×1, 34/15 EQUAL, access 5. No hosted-deploy brief after B249 in the project's Briefs (B250 records, B251 build, B252 gate).
- **Way-back kit on disk:** `.tools/wt-B249` HEAD `d916baf…`, clean; `out/deploy-packages/d916baf…/` holds web.zip `c143593c15a7346a…`, api.zip `2142017f915f113b…`, assessment.sql `8a4084b696aad699…`, feedback.sql `d3d667176aaeb797…`, RUN `38470487072`.
- **Live `.zst` start bytes:** B249's post-deploy download `web-wwwroot-20261016T013810Z.zip` → `node_modules.tar.zst` (11,033,281 B) starts `28 b5 2f fd`, so the new -255 magic check should pass.
- **Records repo:** `datasecau/HPSM-POC-analysis` main `6f5f0dc` (2026-10-16T01:52Z), highest C-106; C-105 = Kam's grant (`CLARIFICATIONS.md:1235`). The B249 deploy record is still owed (C-106's numbering note).
- **Ports:** `lsof` 6900–7099 → only `*:7000` (ControlCe). **Locks:** `.tools/.git-lock` absent.
- **Panes (`@cockpit_name`):** tuesday, Datasec/MPS-V2, QA/NexusAI-gate24, **Datasec/HPSM-POC-G2 (%36, B252, still open)**, Datasec/NexusAI-O, Datasec/MPS-LE, Datasec/MPS-LD, Datasec/Vision_Sales_Portal, fleet-monitor. **`Datasec/HPSM-POC-F3` is free** (as is `-F`). Pane titles (`#{pane_title}`) are the Claude session titles, so the free name was checked on `@cockpit_name`.

## UNMEASURED (for the seat)
- Hosted state since 2026-10-16T01:47:40Z; `az account show`; hosted runtimes today; the new `deploy-package.py` reader against a full live `.zst` (only 4 bytes read: trailing bytes or a skippable frame (B252-9) could still make it refuse); Tuesday's completion-check record; Jira.

## Traps
1. **72073da is not in any local object store.** The seat must `git fetch origin main` under `.tools/b198/lock.sh` before making `wt-B253`. Brief says so.
2. **Check-run count:** DELTA 202 says "20/20 checks incl. CodeQL"; on `72073da` I count **19** (18 success + 1 skipped). Probably the PR head carried one more (dependency review runs on PRs). Not a blocker, but do not quote 20 for main.
3. **The deploy script's own reader changed (-255).** B252 could not run `deploy-package.py web` in CI's form on the Mac. If `live-check` REFUSES the site's `.zst`, the brief has the seat compare with `wt-B249`'s reader + `nmcmp.py` before treating it as a failure.
4. **Favicon route cache** (B249 Open 2) gives site-only 2 / rc 1 on any `live-check` after a visit, including the pre-deploy read. The brief marks it as known.
5. **B252-1 (Minor regression) ships to hosted:** a file named with a trailing backslash escapes the BFF's 20 MiB count; the API still enforces it (422). Tuesday merged with it under GO WITH NOTES. Not a deploy blocker, but it should be on Tuesday's ticket list.
6. **Runtime 10.0.12 (HPSMPOC-254):** B252/B251 name no deploy check. I carried B249's FOUND-1 re-measure as READ-ONLY, pre and post; it does not block.
7. B252's worktrees and stopped containers are still on disk and its pane is open; the brief tells the seat not to touch them.

## Stop-Tuesday-launching?
Nothing I measured blocks the launch. READY holds on every read: gate GO WITH NOTES at the gated tree = merge tree, ci + CodeQL green, 0 alerts, 0 migrations, 0 settings, 0 new customer-facing words per B252. Tuesday's completion check is Tuesday's own record to confirm.

## Launch (same form as B249, new pane name)
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-F3 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B253_SEAT-F_hpsmpoc-hosted-deploy-72073da.md'"
```
Watch for: `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-17_B253_STATUS.md`, last line `DEPLOYED: 72073da @ <build id>` or `STOPPED: NEEDS TUESDAY`.
