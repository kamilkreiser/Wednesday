# Deploy round 2026-11-16: the rides-along census (Tuesday s281)

Tracked so the commission survives rotation. If `2026-11-16_DEPLOY-ROUND_rides-along.md` is absent at the next boot, RE-COMMISSION it from this file.

## Kam's words (verbatim, live board)
- 2026-11-15 19:15:40, note on hpsmpoc-narrative-reedit-migration-1115: "a — Allow the one migration (gated, not deployed) | note: deploy as well"
- 2026-11-15 19:16:20, note on hpsmpoc-q1-partly-answer-1115: "once all changes are made, deploy to all systems so everything is synced and has all recent changes"
- 2026-11-16 07:04, card hpsmpoc-deploy-round-scope-1116: "c — All Datasec projects' demos too"
  (options were: a hosted demo now, UAT after HP's review, HPSM only / b hosted demo and UAT now, HPSM only / **c All Datasec projects' demos too** / d hold everything)

**Tuesday's reading (to be stated to Kam with the list):** the DEMO environments of HPSM-POC, MPS Commercial Calculator, NexusAI and Security Composer. **UAT stays on hold** (the 11-06 hold while HP reviews; c does not name UAT). Nothing deploys before the list is on the board. Never production. Never a migration Down on a hosted database.

## The census drafter (Sonnet, C8): output `tuesday/briefs/2026-11-16_DEPLOY-ROUND_rides-along.md`
Rules: read `tuesday/DRAFTER_RULES.md` whole first. READ-ONLY everywhere: `gh` GET/`gh api -X GET` only (each project's own `4_Credentials/.gh-config` as GH_CONFIG_DIR), `az` READ verbs only and ONLY after `az account show` under that project's own `4_Credentials/.azure` (never a login, never a write, never a restart). `curl` GETs of public health/version endpoints are fine. No push, PR, workflow dispatch, deploy, Jira write, mail, board, Artifact, cd. Print no token. Scratch under `2_Project_Files/fleet/state/s281/deploy-census/`.

For EACH of the four projects, measured at source, each fact with its command:
1. **Which demo environment exists today** (name, URL, how it is deployed: workflow file + trigger, script, or manual). HPSM-POC: its demo was DECOMMISSIONED 2026-11-05 (kit `2026-11-05_B1303_SEAT-D54_hpsmpoc-demo-decommission.md`) — say what "hosted demo" means for HPSM now (read the project's DEPLOY/runbook docs and the last deploy records, `2026-11-12_B1540_SEAT-D61_...` and its records `B1543`). If an environment does not exist, say so; do not invent one.
2. **What is deployed there now** (commit sha, how measured: a version endpoint, a deploy run, an image tag, an app setting) and **main's head**.
3. **What rides along**: every PR merged to main between the deployed sha and main head (number, title, one plain line of user-visible effect). Flag anything with a deploy-time step (migrations, SQL grant scripts, app settings that must ship with the API, data resets).
4. **Holds and conflicts** that touch a demo deploy, grepped in the pickup `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md`, `0_Brain/tasks/EXPIRING-GRANTS.md`, and the project's own CLAUDE.md / CLARIFICATIONS: at least NexusAI's C-224 demo hold; Composer's "deploys only on Kam's card" and the three-dots footer look; MPSCALC-224's host read; HPSM's UAT hold. Quote each with file:line. Say plainly whether Kam's 07:04 'c' lifts it or whether it needs his word.
5. **The deploy route and its checks** for each (the last successful deploy kit for that project is the template: HPSM `2026-11-12_B1540_SEAT-D61`, MPS `2026-11-12_B1542_SEAT-D62`, Composer `2026-10-31_B986_SEAT-D42`, NexusAI: find it), the rollback path, and the live checks a deploy seat would run.

End with: a BLUF table (project | environment | deployed sha -> main sha | PRs riding | deploy-time steps | holds needing Kam) and a short plain-language list for Kam (no shas, no ticket numbers in his version). Last line: `DRAFTED DEPLOY-CENSUS: <projects measured>/4, questions <n>`.
