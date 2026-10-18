# B275 DRAFTER REPORT — QuickQuote v2.39 publish RETRY (SEAT-V5)

Drafter: read-only sub-agent for Tuesday (Datasec only). Wrote only this file and `2026-10-19_B275_SEAT-V5_quickquote-v239-retry.md`. No `az`, no HTTP to any hosted or live host, git read verbs with `--no-optional-locks`, `gh` GETs only (Vision `GH_CONFIG_DIR`). No clock typed into a slot.

## Shape
B270 copied section for section (BLUF · AUTHORITY · WHAT TO DO 0–8 · The way back · CHECKS · Records · HOLDS · UNMEASURED · STAMP). Changes, and only these: the merge placeholder and its refusal check are gone (PR #10 is merged); AUTHORITY has three cards; step 2 adds the defective-tag read and closes B270's two pending reads; step 4 becomes 4a (umask 022 export + mode check + planted control), 4b (build, `--file` pitfall named), 4c (boot as runtime user, 3 images × 4 steps, defective image as negative control), 4d (B270's hash checks kept); steps 5–7 add the 10-s poll, docker-log watch, start window, rollback clock and a 10-min tail; final-line formats per Tuesday's prompt; new HOLDs (no Dockerfile change, never point at v0.6.5, no third attempt); STAMP gains R-8/R-9/R-10 and a Pre-launch line. Identity checks, linuxFxVersion before/after, app-settings hashes, PR #8 untouched, signed-in check R-4, every B270 HOLD: kept.

## FACTS (with sources)
| # | Fact | Source |
|---|---|---|
| F1 | B270 outcome: site non-200 10:14:06Z–10:24:02Z; v2.39 served 0 requests; rollback set 10:23:09Z→10:23:21Z; "Site started" 10:24:02Z | `!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/Briefs/2026-10-18_B270_STATUS.md` (BLUF, FOUND 6, ROLLED BACK); evidence `07a-rollback.txt` |
| F2 | Root cause: 69/69 context files not world-readable (umask 077); control on fresh umask-022 archive = 0; Dockerfile COPY as root then `USER node` | `B270_evidence/07e-root-cause.txt`; `git show 5fa1187:stage3/Dockerfile` :23-24, :29, :30 `CMD ["node", "server.js"]` |
| F3 | Failure signature: `Error: EACCES: permission denied, open '/app/stage3/server.js'` 10:13:44Z and 10:22:54Z; "Failed to start site. Revert by stopping site." 10:13:45Z; old container stopped 10:14:06Z | `B270_evidence/07b-2026_10_18_lw0sdlwk000CCZ_default_docker.log`; `07b-…_docker.log` lines 41-57 |
| F4 | B270 switch 10:12:03Z→10:12:09Z; first 503 seen 10:22:50Z; the 503 period began 1m57s after switch end | `05-switch.txt`, `07a-rollback.txt`, F3 |
| F5 | Defective image `v0.6.5-tool2.39-5fa1187` = `sha256:adef6a10e096b9f2a747188768726b929627fad3618a1561267553d13084085d` | B270 STATUS FOUND row 4 (`04b`) |
| F6 | Tags at B270 start: v0.6.4 and v0.6.3 present, no v0.6.5/v0.6.6 | `02b-acr-tags-before.txt` |
| F7 | PR #10 `merged=true`, `merge_commit_sha=5fa1187b1c2fc89bdef50953f85d8aa76be5685d`, `merged_at=2026-10-18T09:57:49Z`, base main; PR #8 `open`, `merged=false`, head `4d6ed6ef403ef8962ded8211b76c3c6809bbb8c3` | drafter `gh api …/pulls/10`, `…/pulls/8`, run at 2026-10-18T19:47:56Z (`date -u`) |
| F8 | Merge commit: tree `ee51fa73…`, parents `437ab4bc…` then `f31720ee…`; `ls-remote origin refs/heads/main` = `5fa1187…` | drafter `git cat-file -p`, `git ls-remote` (same run) |
| F9 | Boot needs `SESSION_SECRET` ≥32, `ADVANCED_UNLOCK_SECRET` or `HPAM_WORD`, and `TABLES_CONNECTION_STRING` (store.js throws at load); "listening" printed only after `store.ensureTables()` resolves | `git show 5fa1187:stage3/server.js` :920-948; `stage3/lib/store.js` :10-11 |
| F10 | `/healthz` has no rate limiter (`/` and `/login` do) | `server.js` :405, :410, :415 at 5fa1187 |
| F11 | QuickQuote CI already runs Azurite `mcr.microsoft.com/azure-storage/azurite` | `.github/workflows/tests.yml:69` at 5fa1187 |
| F12 | `.dockerignore` excludes node_modules, .git, stage3/public, stage3/private, screenshots | `git show 5fa1187:.dockerignore` |
| F13 | Kam's cards (store): `-1017` a, label "Publish 2.39 and approve the three sentences", ruled_ts 18:59:36; `-1018` five-more a, "Approve all five and publish 2.39", ruled_ts 20:56:21; `retry-after-outage-1018` **b, "Retry Monday morning"**, ruled_ts **2026-10-19T06:44:17.295711+11:00**; option b detail "Same fixes, with you around. …" | `0_Brain/dashboard/data/decisions.json` (python read) |
| F14 | Tap minutes 18:58 and 20:55 (live) | B270 stamped STAMP R-1/R-2 lines |
| F15 | DELTA 236's five required changes; ledger row 2026-10-18 "PRODUCTION OUTAGE" rule (boot as runtime user + health poll on app host) | `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:33-36`; `0_Brain/learnings/_ledger_laptop_datasec.md` (second data row; the first row is the Artifact-publish one) |

## UNMEASURED (each with its closing instrument)
| Item | Closing instrument |
|---|---|
| Kam's tap at **06:42:53** for the retry card | Commissioning prompt only; not in local `chat_log.json` reads (seat-scoped read refused by hook) nor in `0_Brain/daily/2026-10-19.md` (`grep -c -i quickquote` = 0). Tuesday: `kam_rulings_today.sh` (source=live) → STAMP R-1 |
| Live linuxFxVersion now | Tuesday's Pre-launch read; seat step 2 |
| ACR: v0.6.6 absent, v0.6.5 still = adef6a10… | seat step 2 (`show-tags`, `manifest list-metadata`) |
| `az acr run` multi-step: detached Azurite reachable by step id; `ignoreErrors`, `timeout`, `disableWorkingDirectoryOverride` semantics | seat dry-run on v0.6.4 (harness PASS arm), STAMP R-9 if not |
| Whether a normal container swap shows any 503 | the 10-s poll in this run (first time measured) |
| B270 `LA_RESULT_PENDING`, `HTTP_TAIL_PENDING` | seat step 2 KQL reads |
| v2.36 reading a `refused` row | carried from B270, no instrument here |
| Vision C-20 quote | read by drafter at `CLARIFICATIONS.md:152-156` (matches B270's quote) — measured, listed for completeness |

## Drafter judgments Tuesday should see
1. **R-8 deviates from DELTA 236's wording on purpose (default).** DELTA 236 says rollback within a minute of a non-200 "after the start window". In B270 the 503s began 1m57s after switch end, i.e. INSIDE any sane window, because App Service stops the old container ~22 s after the new one fails. The default therefore applies the 60-s rule from the switch onward, plus immediate rollback on a docker-log failure line or on W expiring without "listening"+"Site started". The pickup's literal reading is offered as the alternative.
2. **A 200 inside the window proves nothing** (the v2.36 container answers until the swap; `/healthz` carries no version). STARTED therefore requires the new container's listening line in the docker log + linuxFxVersion + a 200 after that.
3. **Third control arm added:** v0.6.4 must PASS the boot harness, so a harness that can never reach "listening" is caught (the defective v0.6.5 FAIL arm alone would be satisfied by a broken harness).
4. **`disableWorkingDirectoryOverride: true`** called out: without it an ACR step runs in its own working dir and `node server.js` fails for a non-image reason.
5. **Mode-check control is planted in a SEPARATE copy**, never in the build context. Check covers dirs (world r+x) as well as files.
6. Kam's "with you around" → R-10: Tuesday posts on the panel at launch; no further tap needed; no launch after Monday morning without re-asking.
7. **One attempt; no third.** Added as a HOLD.

## SLOTS for Tuesday (12 four-underscore slots; B270 convention, refusal-checked)
| Slot | Recommended default |
|---|---|
| Pre-launch | Tuesday reads linuxFxVersion (Vision AZURE_CONFIG_DIR) just before launch, pastes line + `date` clock; expect v0.6.4-tool2.36-437ab4b; PR #8 open, main = 5fa1187 |
| R-1 | paste `kam_rulings_today.sh` (live) lines for 18:58, 20:55 (10-18) and 06:42 (10-19) |
| R-2 | COVERED by five-more-sentences card = a |
| R-3 | `v0.6.6-tool2.39-5fa1187` |
| R-4 | YES as v2.36 did; else UNMEASURED to Kam; mask inbox subjects |
| R-5 | STOP |
| R-6 | Briefs/ (exists); one mail to tuesday-agent@ `[Datasec/Vision_Sales_Portal -> Tuesday] B275 <outcome>` |
| R-7 | ACCEPT floating base; record digest vs B270's `2cf067cfed83…` |
| R-8 | W = 300 s; rollback at once on failure line / W expiry; rollback started ≤60 s after first non-200 at ANY time to end of 10-min tail |
| R-9 | boot cell unmeasurable → STOPPED: NEEDS TUESDAY, nothing switched |
| R-10 | launch Monday morning after a panel post; re-ask Kam if it slips |
| SELF-CHECK stamp time | Tuesday's own `date` at stamping |

Note: the slots are `____` (four underscores) to match B270 and Tuesday's stamp tooling; the brief contains no `@…@` placeholder.

## Summary
1. Brief written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-19_B275_SEAT-V5_quickquote-v239-retry.md`, B270 shape, 12 stamp slots, all with defaults.
2. All five DELTA 236 changes are in: umask-022 export with a mode check and planted control; new tag v0.6.6; a boot as runtime user before the switch, with v0.6.5 as the negative control and v0.6.4 as the harness control; a 10-s app-host poll with the 60-s rollback; three cards verbatim.
3. Verified read-only: PR #10 merged as 5fa1187 (tree ee51fa73, two parents), main = 5fa1187, PR #8 open. Kam's retry card in the store = b "Retry Monday morning", ruled_ts 06:44:17.
4. Kam's 06:42:53 tap minute is UNMEASURED by me. Tuesday pastes it from kam_rulings_today.sh (R-1).
5. Decision for Tuesday: R-8 by default applies the 60-s rule from the switch, not only after the window, because B270's 503s began inside the window.
