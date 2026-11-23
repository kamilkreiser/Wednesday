STARTABLE: NO (only because PR 244 has not landed: at drafting `pulls/244` read `merged: false`, open, mergeable_state `unstable`, its `build` check in progress; the kit is complete and becomes startable when PR 244 lands and Tuesday stamps S2 = main after the landing. Nothing else blocks it.)

# B1991 DRAFTER REPORT: NexusAI dev-demo deploy kit (seat D-N168)

Drafter: Opus, in-session, read-only, for Tuesday s316. Commission `2026-11-23_B1991_NEXUSAI-DEMO-DEPLOY-KIT_DRAFTER_COMMISSION.md` (read whole). Clocks by `date`: start 15:56:34, end of reads 16:08:25 AEDT 2026-11-23.
Files written: the kit `2026-11-23_B1991_SEAT-DN168_nexusai-demo-deploy.md` (121 lines), its sidecar `.measured` (99 lines, `stamp_check.py` rc 0), this report; scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/d1991/`.

## BLUF
1. **Identity and tenant RESOLVED by measurement:** NexusAI's own `AZURE_CONFIG_DIR` is signed in as service principal `nexusai-claude-deploy` (user type `servicePrincipal`, id `a71b85e7...`), tenant `d500ebad...`, subscription `0c57ab37...` (`Azure subscription 1`); `az group show nexusai-dev-rg` names subscription `0c57ab37`; role assignments: Contributor on exactly `nexusai-dev-rg`, `nexusai-staging-rg`, `nexusai-marketplace-validate`. So the demo lives in workspace environment #5. `CLAUDE.md:185` is right for this resource; `:19`/`:41` (`fc05dcdd`) are wrong for it (they likely describe the retired VM era).
2. **The route research and the card are wrong about the last deploy.** The demo runs revision `nexusaidev-app--0000100` (2026-10-16, S99O's RD-846 deploy of main `17fc6c5`, image `nexusaidevacrfa39.azurecr.io/nexusai@sha256:c12c43e5...`, tag `2.2.1-s99o-17fc6c5`), not `0000099`/`aae041a` of 2026-09-21. Health 200 OK build `def3ac7e654fdacd` = sha256(`17fc6c5...`)[:16]. Main `85b39c77` is 567 commits ahead of that (not 989 as the card says). The project's CLARIFICATIONS do not record the 0000100 deploy (records gap). The ruling's substance holds: RD-876 part 1 (PR 120, `e553d340`, 10-26) is 149 commits past `17fc6c5`, so the 1,000-row cut is NOT on the demo yet and goes out with this deploy.
3. **The kit:** backup of the share root files (C-19, S99O tool with the path fixed), `az acr build` from a fresh clean clone at S2 with tag `nexusai:<S2>` and `BUILD_COMMIT_SHA=<S2>`, the swap BY DIGEST with `--container-name nexusai-api` only, the guide's six checks in order (RD-302 first), served-CSS checks for the colours, rollback by the recorded digest (Single revision mode), end activity-log audit, gate list.
4. **Two departures from the commission's words, both forced by measurement (D2, D3):** rollback is NOT "re-activate the previous revision and move traffic back" (Single mode); the light-mode colours cannot be screenshotted on the demo (every page is behind sign-in) so the hosted check is the served CSS bytes and the render is UNMEASURED on the demo.

## Facts re-measured (instrument, control)
| fact | instrument | value | control |
|---|---|---|---|
| az identity | `az account show` (first 8 only) + `az ad sp show --query displayName` | SP `a71b85e7` = `nexusai-claude-deploy`, tenant `d500ebad`, sub `0c57ab37`, Enabled | `az group show` id names the same sub |
| SP scope | `az role assignment list --assignee --all` | 3 x Contributor: dev-rg, staging-rg, marketplace-validate | 0 subscription-scope rows |
| app | `az containerapp show` (in memory) | Single mode; latest = latestReady = `0000100`; ingress latestRevision 100; registry by identity; containers `nexusai-api` (c12c43e5 digest, 0.5 CPU, 1Gi) + `redis:7.4-alpine`; env 22 / 5 secretRefs; scale 1/1; volume `nexusai-data` | secret names 6 |
| revisions | `revision list --all` | 101 revisions, 1 active (`0000100`, 100, Healthy, RunningAtMaxScale); `0000099` inactive, Stopped | the 100 inactive read False/0 |
| ACR | `az acr show`, `repository list`, `manifest list-metadata --top 8` | `nexusaidevacrfa39` in `nexusai-dev-rg`, Basic, admin disabled; repos `nexusai`, `nexusai-inspect`; newest manifest `rd848-cand-b2fc9bf` (10-16 19:42Z), then `2.2.1-s99o-17fc6c5` = c12c43e5 | rollback anchor digest present |
| health | one `curl GET /api/health` on the dev demo host | 200 `{"status":"OK",...,"version":"2.2.1","build":"def3ac7e654fdacd"}` | `printf %s 17fc6c5...` hash equals; `echo` form gives `c0f6d84d7051eb09` |
| no deploy since 10-16 | `az monitor activity-log list -g nexusai-dev-rg` from 2026-10-16T05:00Z, all statuses | 37 events; `containerApps/write` 2 (Started + Accepted, 2026-10-16) | that pair is the 0000100 swap itself (instrument not blind) |
| main / PR 244 | `gh api -X GET` | main `85b39c77`; PR 244 open, head `97a07e65` (2 commits on `85b39c77`), 8 files | check runs on main: `deploy` skipped |
| CI switch | `actions/variables` | `total_count` 0 | (org/env variables not readable; as B1978) |
| colours in source | `grep -c -i -F` on `index-styles.css` via contents API | `#0a8793`/`#b44752`/`#b57a13` 1 each at `97a07e65` (lines 272-274), 0 each at `85b39c77` | `#26c6da` 1 in both |
| backup baseline | `ls -A`, `wc -l` on `4_Credentials/demo-share-backup-2026-10-16-s99o-pre-rd846/` | 51 share files, 3 dirs listed, 5 `_*` files | `_sha256.txt` 51 lines |
| env query | the kit's exact `--query ... [name, secretRef] -o tsv` | 22 lines, 5 secretRefs, others `None` | |
| logs flags | `az containerapp logs show --revision 0000100 --container nexusai-api --type console --tail 300 --format text` | rc 0, 302 lines | boot phrases are in `boot-log-0000100.txt` once each (too old for the live tail) |
| --help reads | update, revision activate, ingress traffic set, acr build, logs show (az 2.92.0) | flags used by the kit exist (`--container-name`, `--image`, `--revision`, `--revision-weight`, `--build-arg`, `--file`) | |

## D-decisions (the drafter's, for Tuesday to accept or change)
- **D1 Form:** no NexusAI deploy kit exists under `tuesday/briefs/`; form = DRAFTER_RULES + B1792's shape; procedure = `DEPLOYMENT_GUIDE.md` section 2 at main (lines 122-251) + S99O's real 2026-10-16 run (its swap tool, logs, backup tool). B1978's pointer "`DEPLOYMENT_GUIDE.md:96-130` ... `az acr build`" does not match main's guide (now the customer-facing guide; no `az acr build` in it). The `az acr build` line comes from S99O's actual command and `scripts/deploy-dev.sh:107`. **`scripts/deploy-dev.sh` is NOT used and is forbidden** (it redeploys the ARM template, reads keys and flips secrets).
- **D2 Rollback = image swap back to the recorded digest** (guide lines 237-251), because `activeRevisionsMode` is `Single`; "re-activate and move traffic" would need a mode switch (a setting change). The activate/traffic commands are documented from `--help` only and never run.
- **D3 Colours:** hosted pages are behind sign-in (RD-76; S99O read `/index.html` 302), so no screenshot of the demo; the seat GETs `/css/index-styles.css`, `/css/dark-mode.css`, `/css/tokens.css` and compares bytes with S2 plus the three hex. Whether `index-styles.css` is served without sign-in is UNMEASURED (a 302 is recorded, not a failure).
- **D4 Tag = the 40-hex S2** as the commission says (`nexusai:<S2>`), one tag only, no `latest`; the swap is BY DIGEST (the guide: tags can move).
- **D5 Build from a fresh `git clone --no-hardlinks` at `.tools/b1991/clone`**, fetched with the Datasec_DEV deploy key, detached at S2, porcelain empty. The project checkout's `core.sshCommand` names the missing `/Volumes/Laptop-DEV` mount and its local origin/main is stale (`50b7c40c`); it is not touched.
- **D6 Backup first (W0)** although the commission's list of writes does not name it: C-19 requires "back up settings before the swap" and every earlier demo deploy (S76D, S96O, S99O) did it. It uses `az storage account keys list` (an action) and file downloads; key in a variable only.
- **D7 Additional HOLD:** the Q of an env change. 567 commits ride along; the kit changes no env. If the new image needs a new setting, boot fails or degrades and the kit rolls back (a fix-forward is a new card).

## Inputs table (every step's inputs exist at BASE or come from an earlier step)
| step | inputs | from |
|---|---|---|
| 0 | kit, card id (S0), S2, PR 244 state, CI checks, variables | Stamp; GitHub |
| 1 | `AZURE_CONFIG_DIR` folder, the SP login | BASE (exists) |
| 2 | app, revisions, ACR, anchor tag `2.2.1-s99o-17fc6c5`, activity log | BASE (Azure) |
| 3 | `session-tools/s99o/share-backup.sh`, the 2026-10-16 backup | BASE (files) |
| 4 | clone of `2_Project_Files`, deploy key, S2 | BASE + Step 0 |
| 5 | BUILT_DIGEST, `ev/env-before.tsv` | Step 4, Step 2 |
| 6 | NEW, EXPECTED_BUILD, env-before, `index-styles.S2.css`, package.json at S2 | Steps 5, 4, 2, 0 |
| Rollback | anchor digest | Step 2.4 |
| 7 | first-write time | Step 3 |

## Q-questions for Tuesday (each with its default)
- **Q1 The card's BLUF named the wrong last deploy** (21 Sept, 989 commits). The real demo is the 2026-10-16 build; 567 commits (plus PR 244) ride along. Does the ruling still cover it without a word to the product owner? *Default: yes: option a's detail ("deploy main to the dev demo after the colours land, the 1,000-row cut going out without its notice") is unchanged by the count; Tuesday notes the correction in the stamp and in the wrap to him.*
- **Q2 Rollback without asking (S7)?** *Default: yes, once, on any failed Step 6 check, by the recorded digest (the guide's rule "If any of 1-6 fails, roll back"); Tuesday tells the product owner after.*
- **Q3 Backup W0 (D6) allowed under this deploy's authority?** *Default: yes (C-19).*
- **Q4 Colours rendered on the demo UNMEASURED (D3) acceptable for DEPLOYED?** *Default: yes; the gate takes the served CSS bytes (or the image's source plus B1977's render) as the colour proof.*
- **Q5 Records:** the 2026-10-16 deploy (`0000100`) is missing from CLARIFICATIONS; the kit asks the seat to draft a C-entry covering both deploys for the records seat. *Default: yes, records seat after the gate.*

## UNMEASURED
S2 itself, its check runs, its `package.json` version, the merge shape of PR 244; whether `/css/index-styles.css` answers without sign-in; the new image's boot on 567 newer commits (any new required env); the RD-302 window for this rollover; the Entra group read on a new revision (no sign-in, as on 2026-10-16); org- and environment-level GitHub variables (not readable, 403 as B1978); who else may hold an `az` write on `nexusai-dev-rg` at launch (the seat checks panes).

## Outside the fences (disclosure)
- **DRAFTER_RULES fence 4 says "No HTTP to any hosted, demo or production host" and "No az".** The commission overrides both for this run: Azure READ verbs and one health GET on the dev demo host. I sent exactly one HTTP request (`GET /api/health`, 15:59:02 AEDT). Azure: only the read verbs named in the kit's header, plus `az ad sp show` and `az role assignment list` (reads), `az monitor activity-log list`, `az containerapp logs show` (read, to prove the flags), `az storage account show`, and five `--help` reads. No `build`, `update`, `set`, `create`, `delete`, `activate`, `deactivate`, `login`.
- **A raw `az containerapp show -o json` was written to scratch with the 22 plain env values in it** (secrets are not returned by `show`, but values such as a connection string are). I masked all 22 values in place with `os.replace` within the same minute and set the file to 0600. `az_account.json` in scratch holds the full ids (not secrets; never printed). `logs-0000100.txt` (302 lines of live app logs) sits in scratch; scanned for `AccountKey=`/`InstrumentationKey=`: 0. Tuesday may quarantine both.
- `--help` invocations: the commission asked for them; DRAFTER_RULES fence 5 prefers reading a header; for `az` there is no header to read.
- No `cd`, no delete, no git write, no mail, no Jira, no card list (one `decision_queue.sh show` of the exact id, filtered by id: 1 line).
- The card's `ruled_ts` is `2026-11-23T11:37:45.785740+11:00`; the commission quotes the board line at 11:37:14 (a 31-second difference between the board's printed clock and the store's ruled_ts: not a conflict, but S0 should quote the store's value).
