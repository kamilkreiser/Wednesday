# B498 drafter report (read-only; two files written)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B498_SEAT-D28_hpsmpoc-hosted-redeploy-486e74e.md` (98 lines). Cloned from B470's brief shape; B470 STATUS (209 lines) read whole for what happened; B443 and B437 STATUS read at their FOR TUESDAY sections only (B470 had already cloned their shape). There are no ADDENDUMs to B470, B443 or B437 (`ls tuesday/briefs | grep -E 'B(437|443|470).*ADDENDUM'` empty).

## Environment naming (asked: is it production?)
Project `infra/README.md` at `486e74e6` (via `gh api`) names three environments: Dev (not deployed), UAT ("the UAT review copy", C-52), Demo (`hpsm-poc-demo-rg`). The project `CLAUDE.md` has 0 hits for "production" (local file, `/usr/bin/grep -n -i`). The brief says so and STOPS before any write if the sha's README or CLAUDE.md calls UAT/Demo production. Target = UAT only, the same two sites as B437/B443/B470.

## Slots for Tuesday (9 runs of four underscores; `grep -o -E '_{4}' | wc -l` = 9)
- Line 86: stamp time, launch authority, hard stop (3).
- Lines 88-92: Stamp rulings 1-5 (5). Ruling 4 = the one image GET allowed or not (default NOT TESTED). Ruling 5 = whether PR #190 counts as "gated" (see disagreement 2).
- Line 98: `READ-WHOLE-BY-TUESDAY: ____` (1).

## MEASURED by me (read-only, ~06:29-06:45 AEDT 23 Oct)
- Main: `gh api .../git/ref/heads/main` and `git ls-remote origin refs/heads/main` (project git, `--no-optional-locks`) = `486e74e6d433662649cb09aee7112f434722feb1`. Parent `2900535a`, tree `8f9a2fae9ea9ea0ca463c329d0801899664e3c17`. The object is not in the project's local store (`cat-file -t` fatal), so the seat's fetch is needed.
- Deployed sha as recorded by B470 STATUS (no live probe): `4695d7f2d50047770f2e8835172d14022d9e9622`, deployed 2026-10-22T07:04:50Z-07:06:48Z, rc 0, live-check web 1883/1883, API 121/121, BUILD_ID `Ho3XBjNivURc1qcj7HCIa`. No later `DEPLOYED:`/`ROLLED BACK:` last line in `Briefs/*STATUS.md` (grep `^(DEPLOYED|ROLLED BACK): `; newest is B470).
- Compare `gh api compare 4695d7f2...486e74e6`: ahead 10, behind 0, 10 commits, 32 files (1 CI + 8 API source + 18 API test + 5 web). The 10 PRs: #182 #183 #185 #187 #186 #184 #188 #190 #191 #189, with shipped/not-shipped column in the brief.
- Open PRs: `gh pr list --state open` = `[]`.
- CI at the sha: `ci` push run 39840292589 (run 456) in_progress, created 2026-10-22T19:27:57Z; "Push on main" 39840293667 in_progress. Artifacts not yet checkable.
- Panes (`tmux list-panes -a -F '#{@cockpit_name}'`): `tuesday`, `Datasec/NexusAI-M1`, `fleet-monitor`. No HPSM-POC pane, no D28.
- Locks/trees: `.tools/.git-lock` absent; no `.tools/b498`, `.tools/wt-b498`. No deploy-from-ci process running.
- Rollback packages for 4695d7f2 in `.tools/wt-b470/out/deploy-packages/4695d7f2.../`: web `103a49fa...` (matches B470 STATUS), api `9111f93f...` (matches), by `shasum -a 256`.
- Ports 8460-8469: `lsof -nP -iTCP:8460-8469 -sTCP:LISTEN` empty. Load 3.98/3.29/2.67.
- Migration/config/infra scan of the 10 commits: no `Migrations/`, `.sql`, `appsettings`, `.bicep`, `infra/`, `scripts/` path; grep of added lines in the 8 API source files and the web mock files for `Environment|Configuration|appsettings|process.env|Options|GetSection|HPSM_|__` = 0 hits. Only CI change is `ci.yml` (not shipped). `/_next/image` is excluded from the web sign-in proxy matcher (`web/src/proxy.ts`, read in `.tools/wt-b470`), and the web has no `public/` (B496 brief).

## Disagreements with your facts
1. "Same target the previous redeploys used": yes, UAT (`hpsm-poc-uat-rg`), not the demo. The grant text says "the Composer demo and the hosted HPSM-POC site"; B470 read it as UAT only and kept the demo out of bounds (C-52). I kept that. The demo group also runs next 16.3.8; the brief tells the seat to say so in FOR TUESDAY and not touch it. Your call whether the demo is a separate brief.
2. "READY = gated + merged through CodeQL": #190 (the security fix) has no separate QA-gate STATUS in `Briefs/` (only the B496 builder STATUS ending `READY FOR QA`). Your 05:41 daily entry has the merge on 21 checks green, CodeQL 0, your own source diff. Other PRs have gates (B488 for #186/#187, B492+B494 for #189, B491 for #184, B495 for #191; #182/#183/#185/#188 test-only). I made #190 a stamp ruling (5); blank or NOT CONFIRMED = the seat stops before any write.
3. "Is anything merged since B470 a migration or config change": no, by path and by grep. But it is not code-stamp-only like B470/B443: three API module assemblies change (customer-name and feedback-comment validation, executive-summary grouping) and the web server's `next` moves 16.3.8 -> 16.4.2.
4. Image optimization probe: the web serves no image besides `favicon.ico`, so a probe proves little (200/400/404 are all answers). I made it one GET, only if stamp ruling 4 says ALLOWED, else NOT TESTED; the patch is proven by the package's `next` version (16.4.2) plus live-check equality, not by that request. Server Actions DoS, never tested. The hidden-character refusals need POSTs outside the fence: NOT TESTED live.
5. Version/commit the site reports: the project has no known version endpoint (UNMEASURED); B470's probe was live-check equality + BUILD_ID + MANIFEST commit; I kept that and ask the seat to record whether health bodies carry a commit field.

## Assumptions
- Rollback target = `4695d7f2` (what B470 left live); second-level `a93b926a` kept in `.tools/b470/rollback`. Artifacts of run 39735946599 expire 2026-10-29.
- The start-page BEFORE read now must PASS the new-look asserts (B470's look is live); the can-fail control is B470's old-build read (24 FAILS) plus a mutated copy.
- sed re-pointing hazard written in: replace `4695d7f2` -> `486e74e6` before `a93b926a` -> `4695d7f2`, or the kit points at the wrong sha.
- Hard stop left as a slot (merge was 06:28 AEDT; I did not invent one). CI is only ~2 min old at my read, so the seat will wait up to 30 minutes.
- Test-only PRs' CI step counts and the shard timeout (now 30 min) are taken from the `ci.yml` patch.

## UNMEASURED
CI result at the sha; whether any live health body carries a commit field; package content diff vs 4695d7f2; the live site's current state; whether `deploy-package.py` can read `next`'s version from `node_modules.tar.zst` (B470 STATUS says live-check compares inside it, so I assumed yes).

## Fenced
No HTTP to any hosted host, no `az`, no ssh, no docker, no fetch/pull/checkout/worktree; git in HPSM-POC only `ls-remote` and `cat-file`; `gh` GET only with the project's `GH_CONFIG_DIR`; no secret file opened; no decision queue, scoreboard, ack, briefs_staged; no Jira; no Artifact/Docs/mail/chat. Two files written.
