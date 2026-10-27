STARTABLE: YES (after CI at `S` is green; the kit makes the seat wait up to 45 minutes and applies a two-run rule)

# B836 DRAFTER REPORT - SEAT-D39: HPSM-POC demo deploy of main `df1dc0fe` (#234 template + #235 chooser logo)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B836_SEAT-D39_hpsmpoc-demo-deploy-df1dc0fe-template-and-chooser.md` (148 lines, 10 four-underscore slots incl. the last line).

## BLUF
- **The smallest deploy that puts `df1dc0fe`'s behaviour live is the two CI packages through `scripts/deploy-from-ci.sh`, with NO template deploy and NO setting write** (D-2). The only runtime change in `bf4a7bdd..df1dc0fe` is #235 (web package). #234 changes nothing live: its four demo settings are the ones B810 set by hand at 12:46-12:55. The switch survives a FUTURE template deploy because #234 is MERGED (the template at main compiles it on with `demo-open-key`); no deploy is needed to achieve that.
- **A template deploy now would remove a live setting:** by name diff, both demo apps hold `WEBSITE_HTTPLOGGING_RETENTION_DAYS`, which the template does not (this is the 36-vs-35 / 18-vs-17 gap B831 named). A template deploy writes `siteConfig.appSettings` whole and re-applies all 31 resources, so it would be a STOP under B831 FOR TUESDAY 5 anyway.
- B831 item 5's five safety steps are carried as **PHASE T, read-only**, before the deploy: an ARM what-if compares live vs template name by name (the four open-sign-in settings must read NO CHANGE, else STOP; every other difference is listed for a later template kit); the suffix `en46o7` (a mismatch is a STOP); `demo-open-key` present (name only; absent is a STOP); the switch ON before and after; the rollback point (the BEFORE wwwroot downloads plus `PREV`'s CI packages, two stub-proven way-back scripts) taken first.
- Live check: the B833 corner probe in a real browser at 1440x900 and 390x844 (keyline file, `naturalWidth` 3000, 0 corner pixels off the page colour; BEFORE must read the tile), with screenshots and logo crops for Tuesday to send; 8 of 8 level sign-ins; API minter; build id / DLL stamp = `df1dc0fe`.

## Facts re-measured (instrument, time AEDT 27 Oct; control)
1. Main = `df1dc0fe25e87dda4a9748c14870f942371a58a5` (`git --no-optional-locks ls-remote origin refs/heads/main`, 16:58:06).
2. `compare bf4a7bdd...df1dc0fe`: ahead 4, behind 0, 11 files (`gh api -X GET`, 16:58; control reversed: behind 4). Commits, each one parent, chained: `5c36e377` #222 (`api/tests/.../RequestTimingLogTests.cs`), `271f6932` #233 (`infra/tests/test_ci_workflow.py`), `197d7544` #234 (appservice.bicep, infra README, test_security_baseline.py), `df1dc0fe` #235 (6 web files incl. added `hp-mark-keyline.png`). `pulls/222,233,234,235`: all merged, merge commits as listed; #234 head `7ed38bc8` = B831's gated head; #235 head `8804deb8` = B833's gated head.
3. Blob ids equal at `bf4a7bdd` and `df1dc0fe`: `scripts/deploy-from-ci.sh` `0024302d`, `scripts/deploy-package.py` `77dc4993`, `infra/main.bicep` `5565c5e9`, `infra/env/demo.bicepparam` `4ac2dd19`; `appservice.bicep` differs (`2734479b` -> `a7623994`), README differs (`gh api contents?ref=`, 16:58).
4. CI at `S`: `ci` push run `40458012503` `in_progress` (web build, infra, secrets success; api, SQL Server x2, unit, 5 e2e in progress; kept `deploy-*` artifacts not yet uploaded: `ci.yml:138-143`, `:567-572`); a SECOND `ci` push run `40458199925` `pending` (created 05:56:48Z, triggering actor a user, attempt 1; cause UNMEASURED); `Push on main dynamic` CodeQL run `40458012152` `completed/success` (16:58-17:0x).
5. Rollback packages: run `40420821396` `deploy-web-bf4a7bdd...` 16,119,754 B and `deploy-api-bf4a7bdd...` 49,644,733 B `expired=false`, expire 2026-11-02 23:44/23:51Z.
6. Code-scanning alerts on `refs/heads/main`: open 0; all states 1 (control: the call returns rows).
7. Repo merge settings: squash/merge/rebase all allowed; `COMMIT_OR_PR_TITLE` / `COMMIT_MESSAGES`.
8. Production: `infra/main.bicep:6` `@allowed([ 'dev', 'uat', 'demo' ])`; `infra/env/` = demo, dev, showcase-ai, uat; project `CLAUDE.md` `production` 0 hits (control `demo` 1). The seat re-checks `az group list`.
9. Name diff (live names RELAYED from B810's `.tools/b810/final/names-{api,web}.txt`, 36 / 18 lines, names only, checked for value-shaped content first; template names by grep of `appservice.bicep` at `S`): live-only = `WEBSITE_HTTPLOGGING_RETENTION_DAYS` on both apps; template-only on the sites = none. Value drift: UNMEASURED.
10. Template params: every required `main.bicep` param (no default) is set in `demo.bicepparam` (so a what-if needs no prompt).
11. Ports 9650-9659: `lsof ... -sTCP:LISTEN` 0 lines (control: unranged 13), 16:59. Word-boundary scan of 131 non-`.pre-` SEAT kits of 26-27 Oct: `965x` hits 4 = B747, B783, B784, B789 (all closed; matches Tuesday's assignment); control `961x` hits 4.
12. Live panes (`tmux list-panes -a`, 16:59): `tuesday`, `Datasec/NexusAI-M24`, `Datasec/NexusAI-M23`, `fleet-monitor`; no HPSM-POC seat.
13. `.tools/b836` absent; no `B836` file in the project Briefs or in `tuesday/briefs` before this draft.
14. Model: `model-routing.md` line 96 row C6 Deploy, O55 `1st`; `models_latest.json` line 17 `claude-opus-5-5`.

## D-decisions (summary; the kit holds them in full)
- D-1 pin `S`. D-2 no template deploy, smallest deploy = the two packages (why: the four settings already live; a template deploy removes `WEBSITE_HTTPLOGGING_RETENTION_DAYS` and re-applies 31 resources; the ruling says "not deployed by itself"; the merge already keeps the switch on for the next template deploy). D-3 both packages via the script (README step 7, same-commit rule). D-4 PHASE T is read-only incl. an ARM what-if; its JSON stays in `.tools/b836/whatif/`. D-5 no setting write; switch stays ON. D-6 settings equal before/after by program. D-7 minter as B810. D-8 ways back: build rollback to `bf4a7bdd` (switch stays on), switch-off only as last resort. D-9 database wake. D-10 UAT skew.
- Tools are copied from `.tools/b810/` (the most recent proven demo kit) instead of `.tools/b783/`: B783's files use ports 965x already, but B810's are the ones re-proven against today's switch-on demo; the re-point is 897x -> 965x with a `grep` that must read 0 afterwards.

## Q-questions for Tuesday (each with a default)
- **Q-1 Ruling 2 (slot 8):** accept no template deploy + a read-only what-if? Default: YES (`NO TEMPLATE DEPLOY; PHASE T read-only incl. what-if`). If you want the template deployed too, that is a separate kit after PHASE T's list is read; this kit does not do it.
- **Q-2 A T.2 difference other than the four** (expected: `WEBSITE_HTTPLOGGING_RETENTION_DAYS`, plus any value drift): stop the package deploy? Default: NO, record it for the later template kit (slot 9(b) CONFIRMED). The four open-sign-in settings reading anything but NO CHANGE remains a STOP.
- **Q-3 What-if refused or unavailable** (role, flag): Default: continue on the second instrument (git history of the suffix line + live names) and the drafter's name diff; value compare UNMEASURED.
- **Q-4 Two `ci` push runs at `S`:** Default: whichever green run the script picks is accepted if it is a `ci` push run of `S` with both kept artifacts; a red or cancelled run at `S` beside a green one is a STOP. Tuesday may want to look at why `40458199925` exists before stamping slot 5.
- **Q-5 UAT** still shows the old tiled chooser logo (UAT runs `d415a3fe`; B810's runbook was demo-only, so no STOP-shaped Q here). Default: out of scope; a UAT deploy is its own kit if the product owner wants the review copy to match.
- **Q-6 Slot 6 for #222 and #233:** their gate verdict lines were not read by me (test-only, earlier lanes; B810 recorded #222 as test-only). Default: Tuesday names them at the stamp; the seat only checks they hold no runtime path.

## UNMEASURED
- The live demo state now (settings, values, build, switch) - no `az`, no HTTP; relayed from B810 (DONE 13:06).
- Value drift between live settings and the template; whether `WEBSITE_HTTPLOGGING_RETENTION_DAYS` matters to anyone.
- The suffix by ARM (B831-7); the drafter relies on B810's live names and B831's compiled form.
- Why a second `ci` push run of `S` exists; the final CI conclusion.
- Whether Next emits the keyline PNG byte-identical into `.next/static/media` (the kit expects equal and STOPs otherwise).
- #222 / #233 gate verdict lines.

## Outside-the-fences disclosure
- I read names-only files in a closed seat's tree (`.tools/b810/final/names-api.txt`, `names-web.txt`) after checking them for value-shaped content (`value|secret|password|key=`: api 0, web 1 = the name `HPSM_UAT_OPEN_KEY`), and listed `.tools/b810/`, `.tools/b810/kit/`, `final/`, `presig3/` by `ls`. No value was read. DRAFTER_RULES does not forbid this; the kit tells the seat to copy those files by name.
- I fetched six files at `S` (ci.yml, deploy-from-ci.sh, infra README, appservice.bicep, main.bicep, demo.bicepparam) plus README at `bf4a7bdd` by `gh api -X GET` raw into my session scratchpad (not the project).
- Two hook refusals on my own commands (a `cd`, an unquoted `====`); both re-issued without them. No `az`, no ssh, no HTTP to any hosted host, no git write, no decision-queue call, no Jira, no mail.
- Read the heads of the B825 and B826 builder kits for the ruling quotes, and `EXPIRING-GRANTS.md` row 12. Did not read the B804 kit: B810 deployed by the same script (`deploy-from-ci.sh deploy`, its STATUS PART 1), so B804's mechanics add nothing.
