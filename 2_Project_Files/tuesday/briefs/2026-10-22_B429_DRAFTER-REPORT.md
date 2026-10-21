# B429 drafter report (HPSMPOC-224 telemetry)

Drafted 2026-10-22 about 01:50-02:05 AEDT, read-only. Brief: `2026-10-22_B429_SEAT-T1_hpsmpoc-telemetry-224.md` (78 long lines, 2 `@STAMP@` slots: the Stamp line and the last line).

## BLUF for Tuesday
HPSMPOC-224 is a CODE change, not a hosted setting. The card BLUF ("It is a hosted setting") is wrong on this point. App Insights and Log Analytics already exist and are wired by connection string; the API and web contain no telemetry SDK. So the seat ends at READY FOR QA (code), and the deploy is a separate Phase B after a QA gate and your GO. No new paid resource is needed; the cost is ingestion only.

## What I read
- Templates: B418 and B427 whole (structure, refuse lines, STATUS convention, last-line format). Project `CLAUDE.md` whole. `1_Project_Definition/CLARIFICATIONS.md` only by grep (192 lines; the local copy is old, it holds C-07 and nothing on UAT or telemetry, so UAT facts came from B410/B422 instead).
- Card `hpsmpoc-demo-telemetry-review-week-1021` via `decision_queue.sh show` (ruled `a` 2026-10-21T14:43:26+11:00).
- Jira HPSMPOC-224, one GET at 2026-10-22 01:53:10 AEDT (HTTP 200): Backlog, labels `b170-found`/`hosted-demo`, updated 2026-10-06, no comments. Description has BLUF, Recommendation, Detail, Where, Severity, Related; **no "Done-when" line**, so the brief writes one.
- Code at `origin/main` (local ref `ae7a2c86`): `monitoring.bicep` whole, `appservice.bicep:80-100,185-215`, `instrumentation.ts` whole, API csproj PackageReferences, `Program.cs` grep, `infra/README.md:128-182` (step 7) and `:219-227` (UAT), telemetry grep over the whole tree.
- Records: B170 STATUS lines 22-23/82-83/136/152/158, B175 STATUS 138/159, B410 STATUS 36/62/76/171-190, B422 lines 56-101 (grep hits), B102 grep hits, model-routing rows C2/C6/G1/G2, `models_latest.json` (opus = `claude-opus-5-5`), the 2026-10-16 grant file.

## What I measured and how
- main: `git ls-remote origin refs/heads/main` = `35b2b73ebf570878be3aea999e0af08a3fcbbfbf`. The local `origin/main` ref is stale at `ae7a2c86`; all code lines cited are at `ae7a2c86` and the brief tells the seat to re-measure.
- Telemetry grep (`applicationinsights|opentelemetry|instrumentation|APPLICATIONINSIGHTS_CONNECTION_STRING|appinsights|logAnalytics`): hits only in infra (monitoring, appservice, rbac), tests, the web's unrelated `instrumentation.ts` warm-up, and `@opentelemetry/api` as a peer in `package-lock.json`. No SDK anywhere.
- `git log -S` on the connection-string symbol: `19fba6e` (B02), `2664422` (B40), `8217061` (B60) only. Prior work named in the brief: B170 (found it), B175 R8 (left it to 224), B102 (resources), B410 TELEMETRY (rejected the code-free auto-instrumentation route for UAT).
- Web has no `APPLICATIONINSIGHTS_AUTHENTICATION_STRING` in the template (only the API, `appservice.bicep:94`); both identities hold Monitoring Metrics Publisher (`rbac.bicep:94-105`).

## Cost
Relayed from B410 `:76`: A$4.7582/GB beyond 5 GB free, shared per billing account; the 1 GB/day cap gives a worst case near A$145/month. I derived A$10 is about 2.1 GB/month (10/4.7582). The brief makes the seat estimate in Phase A and measure the `Usage` table before and 24 h after in Phase B, and roll back and STOP above about A$10. I did not measure any current ingestion (needs az).

## Open questions for Tuesday (with my recommendation)
1. **Correct the card's wording to the product owner:** it is code plus a deploy, not a setting. Recommend: tell him in the next report.
2. **Which hosted copy?** The card title says "the demo HP uses"; the records say UAT is the copy HP reviewers open (C-52, `infra/README.md:221`). The brief deploys UAT only. Recommend: UAT only now; the demo gets it at its next deploy under your push-to-demo grant, after UAT proves it.
3. **A$10 stop line:** my reading of "small but not zero"; he gave no figure. Recommend: keep, but rule it.
4. **The workspace `dailyQuotaGb: 1`** allows about A$145/month worst case, far above A$10. I put `monitoring.bicep` out of the seat's lane. Recommend: ask for a lower UAT cap (about 0.1 GB/day) as a separate small infra card; the seat only proposes a number.
5. **Gate tier:** I proposed tier 1 (G1: anything deploying, and it touches what a site records about people). Recommend: tier 1, Opus gate.
6. **Collision with B418:** it edits `appservice.bicep:204`, `uat.bicepparam`, the baseline test file. The brief keeps B429 out of those and says rebase if a web setting is ever needed. Check B418's PR state at launch.
7. **Pane/model:** `Datasec/HPSM-POC-T1`, `BRIEF_SEAT_LEVEL=opus`; I did not check the pane is free or load1.
8. **Phase B continuity:** a brief seat exits at its last line. Phase B text is the spec for ADDENDUM-1 to the same seat, or for a successor deploy brief. Recommend: a new deploy brief citing this one, if the pane is gone.

## Could not establish (UNMEASURED, with the instrument)
- Whether the Azure Monitor OpenTelemetry package supports net10.0 and the Entra string (the seat's restore and test run at the pinned dotnet).
- Whether the Next.js 16 standalone build keeps a new telemetry dependency in the traced `node_modules` (`package-standalone.mjs` + `deploy-package.py verify` locally).
- Whether a harmless existing fault exists for the positive control (D5 tells the seat to find one or STOP).
- Current UAT ingestion volume and the free-allowance use (az `Usage` read, Phase B).
- Whether B418 has landed; whether the live UAT still runs `ae7a2c86` (B410/B427 say so; not re-read).
- Resource group names: UAT `hpsm-poc-uat-rg` is from B410 `:30`; the demo's group is not needed.
- The Datasec identity facts (sub, tenant, user domain) are RELAYED from B410 `:18`, not re-run; the user said "datasec-rd subscription", which matches that record.

## Fences
No Artifact, mail, chat or card write; no `decision_queue.sh list`; no scoreboard; no az, gh or hosted HTTP; no `Notes (MASTER)`. I read the `.env` only for the variable NAMES (grep of `JIRA_*`) and sourced it transiently in a subshell for the one Jira GET; no value was printed. Jira response saved to the session scratchpad only (`.../scratchpad/j224.json`). Two commands were refused by hooks (a `cd`, a leading `=` word) and reissued correctly.

## Files
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B429_SEAT-T1_hpsmpoc-telemetry-224.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B429_DRAFTER-REPORT.md`
