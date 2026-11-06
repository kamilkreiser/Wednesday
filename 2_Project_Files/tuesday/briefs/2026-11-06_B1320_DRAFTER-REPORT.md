STARTABLE: YES (once H129 has landed on ci.yml and Tuesday writes the later main into S2/S3; the kit refuses on its own if S2 is not after H129's squash)

# Drafter report: B1320 SEAT-H130, retire the demo's repository paths (drafted 10:28-10:40 AEDT 2026-11-06)

## BLUF
- The kit is `2026-11-06_B1320_SEAT-H130_hpsmpoc-retire-demo-repo-paths.md` (+ `2026-11-06_B1320_slots.json`, 12 slot rows; `grep -c '____'` on the kit prints 12). Branch `b1320/hpsmpoc-retire-demo-repo-paths`, pane `Datasec/HPSM-POC-H130`, ports 9310-9319, Opus (C3), gate G1 after.
- **What is really retired (measured demo-site-only):** the demo parameter file; the README environment wording; the validate job's demo loop (`validate.sh:11,18`, `ci.yml:626`); the binding-rule test's demo row; the web and API demo-SITE locks (`config.ts:57-60,82-85`; `UatOpenAuthentication.cs:55-60,115-120`) with their two self-contained test files; and, by default, the `HPSM_DEMO_NOTICE` banner (UAT value is `off`).
- **What is NOT retired and why (the hazard):** the Demo sign-in LEVEL, "Reset demo", the HostedDemo feature, the sample customers and the label `demo` in `IsDemoLike` (UAT runs or passes through them; the label is also the fixture of about 400 API test rows). The word "demo" hits 209 files in `web/src` alone, so a plain grep is not the instrument and the kit says so.
- **UAT's deploy does not use `infra/env/demo.bicepparam`.** Only `validate.sh:18` and `test_security_baseline.py:2276` read parameter files (grep over the whole tree with controls); no workflow but `ci.yml:630` runs them; the code deploys read none.

## Facts re-measured (instrument; control)
1. Main `13ac7d7e86a5675ee20eb987c62818e357599358`, open PRs 0, no `b1320` ref (`gh api -X GET`; control `b1302` ref listed). Analysis main `37715f3b2b73e91e6ea941a1941140013a851aa2`. H129's, H127's (B1311) and the other kits: H127 B1311 is on disk; H128, H129, R178 kits were not on disk at drafting.
2. Tree read from `gh api -X GET tarball/<sha>` (2480 files). Every `file:line` in the kit was printed by `grep -n` or `awk NR==n` from that tree in this session.
3. Parameter-file readers: 2 code readers (`validate.sh:18`, `test_security_baseline.py:2276`), comments elsewhere; other workflows 0 (control `ci.yml` 9). `infra/scripts/env-value.sh` is a dotenv reader, unrelated.
4. Demo-site lock census: `DEMO_WEB_SITE_NAME`/`DemoSiteName`/`DemoLabel`/`DEMO_LABEL`/the two site names appear in `config.ts` 7, `UatOpenAuthentication.cs` 9, `UatOpenDemoTests.cs` 18, `uatOpen.demo.test.ts` 9, `uatOpen.test.ts` 3, `hardening.test.ts` 3, `reviewDoor.test.ts` 1, `UatOpenTests.cs` 1, `test_security_baseline.py` 1, `appservice.bicep` 1 (case-insensitive grep; control: the two demo test files fire). `UatOpenDemoTests.cs` and `uatOpen.demo.test.ts` are self-contained (outside-file grep 0, in-file control 2).
5. UAT values (RELAYED from the records, hashed there): `Assessment__Environment` / `HPSM_ENVIRONMENT` `uat` (`B410_STATUS.md:387-388`; later equality `B1307_STATUS.md:88`, `:157`); `HPSM_DEMO_NOTICE` `off` (`B1307_STATUS.md:30`, `:88`; `B1258_STATUS.md:94`; `B1234_STATUS.md:101`); switch on, `Feedback__Route` off; sites `app-hpsmpoc-{api,web}-uat-25onzn` (`B1290_STATUS.md:30`). The demo's own hash for both labels is `2a97516c354b` (`B1303_evidence/...appsettings.tsv`). No hosted host was read.
6. README: 24 lines match `demo` (printed list in the kit); B1303's list named fewer. The kit makes the seat print and classify each (A environment wording, B Demo level / Reset demo / UAT parameter name).
7. Way-back scripts: not in the repo (find over the tarball 0; control `.tools/b28b` 15 files). They are in the project's untracked `.tools/` (`ls -la`, 3321 bytes each).
8. Landing rule quoted from `CLARIFICATIONS.md:3617` (analysis main `37715f3b`): a head-pinned squash, one parent. `web/package-lock.json` blob `81393fd77c36489b3e8b17a13bde28e225350fb4` (`gh api contents`). e2e matrix at `ci.yml:494`: 8 names; the kit adds or deletes no spec file, so `check-shards` must stay `plan OK` (hosted-entra.spec.ts loses banner assertions only).
9. Ports 9310-9319: 0 listeners (`lsof`; control 11 total listeners), 0 kit hits (word-boundary scan of 11-05/11-06 non-`.pre-` SEAT kits; control `928x` hit 4). Panes: wednesday, Datasec/HPSM-POC-H127, fleet-monitor, three unnamed.
10. Compare controls for the H129 REFUSE: parent...main `ahead`, main...parent `behind`, main...main `identical` (`gh api -X GET compare`).

## D-decisions (made in the kit)
- D-1 Retire by a measured property ("UAT cannot reach it; cell shows UAT equal before/after"), not by name. Each path has a table row: reader, UAT value with source line, what changes at the next deploy.
- D-2 P1 and P2 (the two open-sign-in locks) are retired together with their test files; the UAT twin rows stay and new refusal rows prove label `demo` + switch on is refused everywhere.
- D-3 `uat.bicepparam` stays value-identical; only dangling comments change, proven by byte-equal `build-params` JSON. Compiled `uat` and `dev` settings may differ only by the removed `HPSM_DEMO_NOTICE`.
- D-4 `ci.yml` gets one changed line (the step name at `:626`), because H129 owns the file and lands first.
- D-5 The seat removes `UatOpenDemoTests.cs`; the kit asks it to say which UAT row twins each demo row and to STOP rather than invent a row where none exists.

## Q-questions for Tuesday (each with a default)
- **Q-1 Model.** P1 and P2 are on a sign-in surface. Default **Opus (C3, `model-routing.md:93`)**, launch level `opus`. Alternative: Sonnet C2 (`:92`), which would need the S7 line and the launch level changed together.
- **Q-2 The label `demo` and the template's other demo branches.** `HostedDemoOptions.IsDemoLike` accepts `demo` as well as `uat`; `main.bicep:7`, `appservice.bicep` (`:40-41`, `:128` Feedback route `automation`, `:138`, `:142`), `sql.bicep` and the infra tests' compiled-template cells still name `demo`. Not site-name paths, not reached on UAT, but about 400 API test rows use the label as a fixture. Default **leave all of it** and record as a follow-up; after the lock retires, a template deployed for `demo` would build sites that refuse to start, but no parameter file exists to deploy it. Say retire if the owner wants the template cleaned too (a larger, separate kit).
- **Q-3 `HPSM_DEMO_NOTICE`.** UAT is `off`, so the banner never renders on UAT. Default **retire** the reader, its six render sites, the bicep line, the Playwright env, the `hosted.test.tsx` H4 rows and the hosted-entra banner assertions; U4 proves UAT's rendered pages byte-identical. A hand template deploy of UAT would then stop writing the setting `HPSM_DEMO_NOTICE=off`. Say keep if you would rather leave the banner switch for a future hosted copy.
- **Q-4 Port block.** None was given. Default **9310-9319** (free by lsof and kit scan). H128/H129 kits not on disk, so overlap with their blocks is UNMEASURED: re-run the scan at the stamp.
- **Q-5 Way-back scripts** (`.tools/b1286/rollback1286demo.sh`, `.tools/b1297/rollback1297demo.sh`): outside the repo. Default **the seat does not touch them**; Tuesday quarantines them (never delete) when convenient.

## UNMEASURED
- UAT's live values (no hosted read; the records say `uat` and `off`, hashed). The seat's U-cells run the real functions on UAT-shaped input instead.
- Whether H129 changes the validate job or `:626` (the kit STOPs if it did). H128/H129/R178 paths (kits not on disk).
- Whether `bicep` at the project's pin matches CI's `BICEP_VERSION` (the kit asks the seat to print both).
- `UatOpenDemoTests.cs` rows that have no UAT twin (the seat reports them).
- The remaining demo mentions in `docs/`, `Assessment/README.md` and `web/README.md` beyond `:44`; the NexusAI `deploy-demo.yml`, `scripts/setup-ci-oidc.sh` and `backend/` (another product in this tree; named in the kit as not touched).

## Outside-the-fences disclosure
- Read-only. Wrote only the three B1320 files in the briefs folder. Extracted the repo tarball and the two raw records files into the session scratchpad (not a project folder). `gh` was `-X GET` under the HPSM-POC `GH_CONFIG_DIR`; no hosted, demo or production host, no az, ssh, docker; no decision_queue, no `fleet/briefs_staged/`, no scoreboard, no `_ledger.md`, no Wednesday or Friday tree. Local project reads: the project's `Briefs/` STATUS files and `B1303_evidence/` settings TSVs (hash prefixes only), `ls -la` of the two way-back scripts and `ls` of the project folder. Read other kits in the briefs folder for the slots shape and the port scan (B1311, B1319 head lines). `tmux list-panes` and `lsof` read-only. One early `cd` in a Bash call was refused by the hook and re-issued without it.
