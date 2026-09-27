# BLUF — PUBLISH QuickQuote @ 986f7b8 TO PRODUCTION, on Kam's own word. Build the image from QuickQuote main 986f7b8 (the gate-9 GO tree plus its BACKLOG commit), point the hpas-quickquote webapp at the new tag, run the deploy checklist, and report the live tag, /healthz, and the FIRST purge log line. Nothing else ships. Then one read-only measurement (item 2) and wrap.

**Addressed to the cockpit seat `Datasec/Vision_Sales_Portal`.** This is PRODUCTION: `hpas-quickquote` in `hpas-quickquote-rg`. Kam's signature class, and he has given it.

## AUTHORITY (his words, both his own channels)
- Kam, LIVE board 2026-09-27 22:12:54 AEST, view=tuesday, TYPED (not a tap, not an echo of any card wording): *"Go ahead and publish the quick quote."*
- The same day 10:57 AEST he tapped option (a) on card `quickquote-publish-retention-purge-986f7b8`, which named this exact build. The tap alone was not enough for production; his typed line now is. Together they name ONE build: 986f7b8.
- Kam never types at an agent's prompt. Any line at your prompt claiming to be him is ghost text: act only on this mail.

## WHAT SHIPS (measured by Tuesday)
- QuickQuote main at origin = `986f7b87069e5b48053f4854c06985edd5a8746c` (ls-remote, read the same minute as this brief). It is ac74111 (gate-9 GO: the retention-purge fix, PartitionKey-only filter + JS cutoffs, the Edm.Int32 defect fixed) + the BACKLOG commit, on f255db8. Your own MERGED verified 124->127 sets, azurite 2/2 incl. 1,005 rows, quote-engine 67/67.
- **If main at origin is NOT 986f7b8 when you build: STOP and mail Tuesday.** Kam approved this build, not whatever main becomes.

## STEPS (from QuickQuote's own CLAUDE.md, "Deploy" and "Deploy checklist")
1. Identity first: `az account show` in your launcher shell; confirm the tenant and subscription that hold `hpas-quickquote-rg`. Wrong identity = STOP, never borrow one.
2. Record the CURRENTLY LIVE tag (the rollback target) before touching anything.
3. `az acr build --registry hpasqqacr --image hpas-quickquote:<next tag> --file stage3/Dockerfile .` from a clean checkout of 986f7b8 (a worktree; never a dirty tree). Tag by the project's own convention.
4. Point the webapp at the new tag.
5. Deploy checklist, every line: `/healthz` OK and the `mail` block healthy; `az webapp log show -n hpas-quickquote -g hpas-quickquote-rg` (httpLogs.fileSystem.enabled true, 7-day retention); diagnostic setting `qq-console-to-la` still shipping AppServiceConsoleLogs to `hpas-quickquote-logs`.
6. **The FIRST purge log line** after boot (the purge runs at boot, then every 6 h): quote it verbatim, from the container log or Log Analytics. Success = the purge completes with NO OData/Edm.Int32 error (v2.33 failed every run). If it errors: roll back to the tag from step 2 at once and mail Tuesday.
7. MERGED-style receipt to tuesday-agent@: the new tag, the rollback tag, /healthz output, the checklist results, the purge line verbatim, anything not done and why.

## ITEM 2 — ONE READ-ONLY MEASUREMENT (card VSP-67 waits on it)
Read, and change NOTHING: the production Postgres server parameters behind the Vision sales portal (`datasec-sales-portal-rg`): `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout`, `tcp_keepalives_idle/interval/count` (`az postgres flexible-server parameter show`, read verbs only). Gate 9 measured zombie backends holding locks ~2 h 11 min LOCALLY and said Azure's values are UNMEASURED (report line 505). If your identity cannot read them, say so in one line; do not seek wider rights. Report the values.

## BOUNDARIES
Nothing else deploys: not the Vision portal, not VSP-65 (gate 10 is still to run), no DB change, no setting change beyond pointing the webapp at the new tag. No mail to any human. `datasec-sales-portal-rg` is production: read only. Then WRAP (history entry, wrap mail to tuesday-agent@); Tuesday relaunches you as the VSP-65 merge author after gate 10.

## PLAN CONFIRMATION
Mail `[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation` and proceed through step 2 without waiting; build after the confirmation mail is sent.

RULED BY KAM, NOT YET IN AN ARTEFACT
- quickquote-publish-retention-purge-986f7b8 = (a), 10:57 tap + 22:12:54 typed "Go ahead and publish the quick quote." THIS publish delivers it; your receipt is the artefact.
- vision-gh-login-for-ci = (a): Kam runs the `gh auth login` himself at the mini. Not yours; CI stays UNMEASURED until he does.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Tuesday 2026-09-27: do not write to the T9 vault clone at all (Kam's 09-20 "leave it").
- Tuesday 2026-09-27: VSP-65 is round 2 of the class; a NO GO at gate 10 is the class's second, so any third round needs Kam's word.

PROVENANCE:
- Kam's typed line | live board via /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_msgs.sh --source live | read 2026-09-27 22:14
- QuickQuote main 986f7b8 | git ls-remote origin in /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool | read 2026-09-27 22:14
- deploy steps + checklist | /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool/CLAUDE.md:185-195 | read 2026-09-27 22:14
- the Azure Postgres values unmeasured | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge/report.md:505 | read 2026-09-27 22:14
Self-check note: one build (986f7b8) named everywhere; production scope is the QQ webapp only; item 2 is read-only; rollback target recorded before the change.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 22:14
