STARTABLE
# B971 drafter report: SEAT-D41, HPSM-POC deploy of main e8ac3f29 to UAT (demo held)

**BLUF.** The kit is written and is startable once Tuesday fills the stamp. One blocker for a START (not for stamping): CI on `S` is still running (push run `41145916659`, `in_progress` at 10:44 AEDT, created 10:41 AEDT), so the kit's Step 0 waits (poll 60 s, up to 60 min). Main head = `S` = `e8ac3f294fa97a340c09dd506abd43f1a248b556`. The range from what the hosts run (`c00e2828`) is 22 merged PRs, web only; the API package should differ only by the commit stamp. The kit deploys UAT only by default; the demo leg (PART B) is written in full but gated on two stamp slots (7 and 11).

## What reaches UAT (MEASURED 10:4x AEDT, read-only `gh api -X GET`)
- `compare c00e2828...S`: status ahead, `ahead_by` 22, `behind_by` 0, 22 commits, every one with one parent, 158 files (86 added, 2 removed, 0 renamed). Each commit is the squash of one merged PR (#239 to #260; table in the kit, with merge sha, merged head and gate line).
- Paths: 148 under `web/src/`, 8 under `web/e2e/`, `infra/README.md`, `infra/tests/test_security_baseline.py`. Zero `api/` paths (control: web/src reads 148), zero `.sql`, migration, schema, `scripts/`, `.github/`, `package*.json`, next/tailwind/postcss config, image or font paths. CSS change is additive (`globals.css` +29, `tokens.css` +12, `contrast.ts` +12).
- New in the web: v1.2 left sidebar and top bar (#240), restyled shared primitives and pages, My readiness and Training pages, `/security` preview pages (#253), customer frame header card (#245), Previous links, browser-held action register (#257), "Delivery phases" (#256). `returnPath.ts` gains the `security` and `training` segments.
- Infra/templates: `infra/main.bicep` `5565c5e9ef65`, `demo.bicepparam` `4ac2dd197945`, `uat.bicepparam` `c5bb59b913bf`, `appservice.bicep` `a762399433e0` all EQUAL at c00e2828 and S. Only `infra/README.md` and one infra test changed. No template deploy is needed or in the kit.
- `scripts/deploy-from-ci.sh` `0024302d1ea3` and `scripts/deploy-package.py` `77dc49939859`: blobs equal at c00e2828 and S.
- Gates: all 22 PRs have a `GO WITH FINDINGS` VERDICT line (B896, B908, B913, B910, B922, B938, B939, B940, B941, B946, B942, B948, B958, B959, B960, B961, B962, B963, B965, B964, B966, B967); every gate head equals the PR's merged head (read from `commits/<sha>/pulls`). No gate in the range is a plain GO and none is a NO GO as the final word (earlier NO GO rounds on #240, #243, #251, #252, #253 were re-gated).
- CI on S: push run `41145916659` (`ci`, main, head_sha S), `in_progress`. Done so far: infra, gitleaks, web build (audit, lint, typecheck, build, deploy package) all success. Still running: api, both `api on SQL Server`, web unit, 5 e2e shards. CodeQL dynamic run `41145916518` also running. Artifacts listed at 10:44: `web-build`, `gitleaks-report-redacted`, `web-deploy-package-unkept` (not a deploy package); `deploy-web-<S>` and `deploy-api-<S>` NOT yet listed. Open code-scanning alerts on main: 0 (state-all control returns 1 row).
- Open PR not in S: #261 (test-only spec row, gate B970 pending). Live seats: G235 (gate) and H78 (builder), neither deploys.

## Measured about the current hosts (RELAYED, not measured)
B874 STATUS last line: `DEPLOYED: UAT + demo @ c00e2828`, web build `ksAkGKt35N5zXMin2YoW8` on both, deployments UAT web `7e4d57b2...` / API `d2f3506e...`, demo web `9467aa26...` / API `c25beeb2...`. No later STATUS ends in a deploy (B810, B836, B874 newest in the `DEPLOYED|ROLLED BACK|PARTIAL` grep). Kept way-back packages exist and I re-hashed them: web `5abfbece273102de03536b5e56519cf0d0934e20f59e4c8a43b95a5ae06fab12` (16,268,213 B), API `86ee28a9f6c8b9dab6f22e5da086977a07363a6230e18653e173654a33270cee` (49,578,939 B), under `.tools/b874/repo/out/deploy-packages/c00e2828.../`. Both sites ran the same commit, so one pair of zips is the way back for both. The kit tells the seat to measure live state itself at Step 0.

## Claims found wrong or changed vs the template and the task
1. Template says "no other HPSM-POC seat is live" and "no PR open": now G235 and H78 are live and PR #261 is open. Kit rewritten (they are named, their trees untouched, neither deploys).
2. Template ways back differ per site (UATNOW vs DEMONOW). Now both sites share one way-back package (c00e2828), so the rollback scripts all point to the same zips; the kit still builds all three scripts (uat, demo, off) and stub-proves them even though the demo is held.
3. The B874 wording proof (W1/W2/W3 refusal literals) and the keyline start-page proof are dropped as new claims: neither the open sign-in, the start page nor the API source is in this range. They are kept as "unchanged-equal" checks (D-12). The API proof is "differs only by commit stamp".
4. The template's CSS check assumed an identical `#1d4f91` count; tokens/globals changed, so the kit records before/after and treats 0 as the way-back class.
5. Task said "CI artifacts": at 10:44 the two deploy artifacts are not yet listed (run in progress). Not a defect, the kit waits.
6. Template port block 9740-9749 reused (B874's, seat closed; no listener on it at 10:4x). My word-boundary kit scan was not clean to run (many kits name ranges such as 9700-9999), so the kit makes the seat re-run it with the control and STOP if a live seat's kit claims the block. Tuesday may prefer to stamp another block.
7. Task text says "the register strings of #257 ... the security preview strings of #253": confirmed by the gate STATUS files (B960 Words table has 7 relabels plus numerals 1, 2, 3; B953 lists the security strings; B963 lists 15 strings). I did not open the B964 Coach list in full.
8. #253's gate B965 raised B965-1 "needs Tuesday's ruling before landing". I did not find the ruling file (only the B965 weekly-limit addendum). It landed, so presumably ruled; the kit asks Tuesday to name it in stamp slot 6.

## Q-questions with defaults
- **Q-1 (the words tension).** The grant excludes new customer-facing words; this deploy carries several lists for the product owner's veto, but UAT is his own review copy ("redo the UAT ... email this to me", 10:10). Default: UAT goes ahead; the demo is held (slot 7 default `UAT ONLY`, slot 11 default `DEMO HELD`); PART B runs only if Tuesday stamps `UAT THEN DEMO` with slot 11 carrying his own clearing words. Under the default the run ends `PARTIAL:` (UAT deployed, demo not started), which is by design.
- **Q-2 (who emails).** The kit forbids any message from the seat; Tuesday sends the product owner the e-mail using the seat's STATUS and `before-*` / `after-*` screenshots (FOR TUESDAY 2). Default: Tuesday sends.
- **Q-3 (hard stop).** The product owner wants it "today, Monday latest". Default: a hard stop that leaves a normal working window today; Tuesday picks the time (no placeholder written).
- **Q-4 (B965-1).** Name the ruling in slot 6 (see claim 8). Default: record "landed under Tuesday's merge GO; ruling file not located by the drafter".
- **Q-5 (port block).** Default 9740-9749 with the seat's re-check; change in the kit if Tuesday knows of a collision.

## Stamp values (suggested)
1. Stamp time: Tuesday's clock at stamping (kit carries no clock).
2. Launch authority: the Tuesday session that read kit and this report; cites the standing 2026-10-16 grant, the 10:07 and 10:10 words, the held-demo default, usage ruling (WED_USAGE_STOP=100 under the Datasec no-90%-line grant).
3. Hard stop: Tuesday's choice (Q-3).
4. `S`: `e8ac3f294fa97a340c09dd506abd43f1a248b556` (re-read `commits/main` just before; squash confirmed, one parent).
5. CI run: `41145916659` with the state Tuesday reads then (drafter saw `in_progress`).
6. Gates: the 22 lines in the kit; open alerts 0; PRs landed after S: none at drafting (open: #261, not in S); B965-1 ruling (Q-4).
7. `UAT ONLY`.
8. `NO TEMPLATE DEPLOY; NO SETTING WRITE`.
9. The drafter default list (roll back at once on: a level that does not sign in, a 200->5xx route, start page differing from before, CSS missing `#1d4f91`, sidebar/top bar absent, new sideways scroll at 390, API accepting a wrong key, required API start line missing).
10. (a) CONFIRMED, (b) CONFIRMED, (c) CONFIRMED, (d) CONFIRMED if Tuesday knows of no HP review or rehearsal.
11. `DEMO HELD`.

## Process notes
Model: Opus, `claude-opus-5-5` (`levels.opus.model_id`), Deploy row at `model-routing.md` line 96 (routing row C6). Launch line carries `BRIEF_SEAT_LEVEL=opus`, pane `Datasec/HPSM-POC-D41`, `.tools/b971` absent (a different directory `.tools/b97` exists). Kit file: 61,866 bytes, 0 non-ASCII by program, no person name, no C-number, 12 four-underscore slots (11 numbered plus the final READ-WHOLE line). The kit is a rewrite of B874's structure, not a byte copy; the template had no `.pre-stamp` copy, so I used its stamped file's structure and left every slot blank. No hosted request, no `az`, no message sent; I ran only `gh api -X GET`, `ls`, `shasum`, `lsof`, `tmux list-panes`, `tail`, `uptime`.
