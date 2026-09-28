# BLUF: `Datasec/Vision_Sales_Portal`: Kam ruled VSP-74 at the cap as (a): "Merge both now; ticket the six layouts" (live board 2026-09-28 20:21:02). You are the MERGE AUTHOR for ONE fast-forward: portal main e59232e to 110bb03. 110bb03 is VSP-75's gated head, and it contains VSP-74 round 2 (4813e5f). Then file ONE ticket for the six failing layouts, record Kam's ruling on VSP-74, and wrap. No deploy, no production, nothing in Azure.

Gate 13 report (read it whole before merging; Tuesday has): `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate13-vsp74r2-vsp75/report.md`. Verdicts: VSP-74 round 2 of 2 NO-GO (six class-hunt shapes), VSP-75 GO on its own scope, merge line FAST-FORWARD (main is an ancestor of 110bb03; the result tree equals 110bb03's own, 6d57e4cb).

## THE MERGE (one step)
1. Re-read origin immediately before: main must be e59232e and `fix/vsp-75-backup-all-tables-2026-09-28` must be 110bb03 (both read by Tuesday via ls-remote at 20:23 AEST). If either moved: STOP and mail. Do not merge a different head.
2. Fast-forward only (`merge --ff-only` to 110bb03, then push that sha to main). No merge commit, never a rebase. 4813e5f is never merged alone (merge coupling).
3. Before the push, on 110bb03: `npm test` and `test:db` as SETS against the gate's numbers (unit 131, db 126, 0 names lost against e59232e's 114/98, 0 failing). Any lost name or failure is a STOP.
4. After the push: ls-remote main == 110bb03. Push-to-main workflows are test.yml and gitleaks.yml only (Tuesday read `.github/workflows` at 110bb03; there is no deploy workflow). **CI is UNMEASURED** because this project's gh is not logged in (Kam's login is still owed). Say so in the MERGED mail, and do not claim green.
5. One MERGED mail to tuesday-agent@: new main (ls-remote), the two suite sets, and CI UNMEASURED with the reason.

## THE TICKET (Kam: "ticket the six layouts"), ONE ticket, BLUF-first, linked to VSP-74 and VSP-81
- **Contents, from the report's FINDINGS INDEX, with repro, fix shape and regression cell for each:** VSP74-G13-F1 (FK on a single partition invisible), F2 and F5 (one label shared by two tables), F3 (a search_path shadow named kept then overwritten), F4 (an inheritance child emptied by `DELETE FROM "leads"` without ONLY), and F6 (another schema's partition-level FK, which loses rows even on the default path).
- **Add G13-M1 and G13-M2** (the bare-name DELETE/INSERT follows the search_path; an other-schema inheritance child). They share F3/F4's fix (qualify every statement: `ONLY "public"."<t>"`), so one test pass proves them together. Add **G13-P1** (ambiguous duplicate labels in the refusal) as Polish inside it.
- State the likelihood as the gate measured it: the portal's own schema has none of these shapes (READ); production's catalog is NOT TESTED. Also state that in 5 of the 6 shapes the default (no flag) refuses and changes nothing.
- **The runbook line, in the ticket and in BACKLOG.md:** "Before any restore, list production's non-public schemas, partitions, inheritance children and dotted table names, and the connecting role's name against its schemas."
- **BACKLOG.md (gate G13-O3):** record VSP-74 round 2, this ruling, the new ticket and VSP-81. Record them in the merge's follow-up commit, or next time BACKLOG.md is touched. Say which in your mail.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- vision-vsp74-cap-reached-ship-or-round3: "a — Merge both now; ticket the six layouts (recommended)" (live board 2026-09-28 20:21:02) -> write it on VSP-74 (a comment quoting it, with the new ticket id) and on VSP-75.
- vision-vsp65-production-deploy (a, 06:57:40): NOT deployed in this session. His gh login and his typed word come first. VSP-65 comment 38520 already carries it.
- vision-prod-postgres-idle-transaction-timeout (b, 06:57:51) with card vision-vsp67-second-consumer-attio-bridge: production is unchanged. At 20:21:55 Kam offered to authorise VSP-67 by EMAIL (he is travelling), and Tuesday sent him the text. **VSP-67 is NOT yours this session.** If his signed email arrives, Tuesday briefs it separately.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-28 (gate 12/13 stamps): any loss of a row of a table the plan names as kept is a FAIL; merge coupling means 74 and 75 merge together via 110bb03 or not at all.

## HOLDS
- No deploy, no production, no `az` write, no Partner Center. Portal main only, for the one fast-forward.
- PRIOR-WORK CHECK before rebuilding anything. Nothing is being rebuilt this session; the ticket is a filing.
- Local Postgres on 127.0.0.1:5433, your own databases only. Never delete; quarantine.
- The vault clone's divergence (ahead 14 / behind 550) is Kam's: do not touch it.

PROVENANCE:
- verdicts, merge line, findings F1-F6/M1/M2/P1, runbook line, O3 | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate13-vsp74r2-vsp75/report.md | read 2026-09-28 20:23
- main e59232e, VSP-75 head 110bb03, workflows test.yml + gitleaks.yml only | git ls-remote + ls-tree/show at 110bb03 in /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files | read 2026-09-28 20:23
- Kam's (a) ruling and the VSP-67 email offer | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_msgs.sh 2 (source=live) rows 20:21:02 and 20:21:55 | read 2026-09-28 20:23
Self-check note: one fast-forward on Kam's (a); no deploy; VSP-67 and VSP-65 explicitly excluded; the ticket is one ticket, per his words.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 20:23
