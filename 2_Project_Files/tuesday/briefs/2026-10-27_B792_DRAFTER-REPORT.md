STARTABLE: NO

# B792 drafter report (Datasec / HPSM-POC, demo site level chooser by app settings), drafted 2026-10-27 06:2x-06:3x AEDT

## BLUF
Option b cannot be done by app settings alone. The chooser (mode `uat`) is behind two code locks on both apps: a label of exactly `uat` AND the platform's `WEBSITE_SITE_NAME` containing `-uat-`. The demo is `...-demo-en46o7` with label `demo`. Turning the switch on there makes the web answer 503 on every sign-in and API call (mode `off`, fail closed) and makes the API refuse to start. Getting round it means faking the site name or label, which is a bypass of a lock the project wrote on purpose (switches true in uat ONLY, tested by `infra/tests`). The kit B792 is written as a REFUSE-AT-ONCE stub. The old demo API `0e631d75` does support the open sign-in and `uat.action-off`, so that is not the blocker. The real fix is a code change plus a web AND API deploy to the demo: not possible in the demo window.

Setting names that WOULD change if a code change relaxed the locks (not to be run now): web `HPSM_UAT_OPEN_SIGNIN`=on, `HPSM_ENVIRONMENT`, `HPSM_UAT_OPEN_KEY` (+ vault secret), `AUTH_SECRET` (already set); API `Auth__UatOpen__Enabled`=true, `Auth__UatOpen__Key`, `Assessment__Environment`. Entra is REPLACED in that mode (sign-in and callback 404), not kept beside it.

## Facts (instrument; control)
- F1 config.ts `resolveAuth` locks (MEASURED, `gh api -X GET contents/web/src/server/auth/config.ts?ref=main` raw, read whole): switch on needs `HPSM_ENVIRONMENT === "uat"`, hosted needs `WEBSITE_SITE_NAME` including `-uat-`, no dev-auth header, key >= 32 bytes, `AUTH_SECRET` >= 32. Control: blob sha `88546d64` read at `main` and at `0e631d75` equal, so the same file.
- F2 API `UatOpenAuthentication.Read` (MEASURED, same method, lines 98-131 and 172-186): needs `Auth:UatOpen:Enabled` exactly `true`, `Assessment:Environment` = `uat`, site name containing `-uat-`, key >= 32 bytes, else throws "refusing to start". `UseUatOpenRefusals` answers 403 code `uat.action-off` for any route marked `DestructiveAction` before sign-in. Control: blob `e51abdb1` equal at `main` and `0e631d75`; `Program.cs` blob `4128e681` equal and its text at `0e631d75` holds `UatOpenAuthentication.Read` (line 48) and `UseUatOpenRefusals` (line 141); `DestructiveAction.cs` blob `fed52ee4` equal. So the OLD demo API has the feature. Whether the demo API's reset/erase routes are the marked ones: from the README line "Reset demo, personal-data export/erase, showcase reset and customer delete answer 403 uat.action-off" (RELAYED, `infra/README.md` ~line 233).
- F3 bicep (`infra/modules/appservice.bicep`, blob `2734479b` equal at both refs, MEASURED): `Auth__UatOpen__Enabled`, `HPSM_UAT_OPEN_SIGNIN` are `uat`-only expressions; key references `uat-open-key` only in uat; demo holds empty values. `HPSM_DEMO_NOTICE` is `on` in demo only. Project rule on hand-set settings: not stated as a ban in what I read; the rule that matters is the uat-only switch tests (`infra/tests/test_security_baseline.py` named in the code search for the switch names; I did not read its rule bodies; it differs between `0e631d75` and `main`, blobs `ecfedeeb` vs `e8cb32ff`).
- F4 Demo state: B783 STATUS (RELAYED, read via grep, not whole): demo web `68ebdbf7`, API `0e631d75`, settings API 34 / web 15, the five UAT names absent, `HPSM_DEMO_NOTICE` on, demo login `<title>Sign in</title>`. UAT: API 35 / web 17, `Auth__UatOpen__Enabled` true.
- F5 Ports 9660-9669: `lsof -nP -iTCP:9660-9669 -sTCP:LISTEN | wc -l` = 0. Word-boundary scan of non-`.pre-` SEAT kits of 26/27 Oct hit B744, B749, B750, B751 (I did not open them; likely probe ranges; control: none), so the block is unclean by the rule; the kit uses no port. Live pane list not read.
- F6 Model row C6 line 96 quoted in the kit (MEASURED, `sed -n 96p`).

## D-decisions
- D-1 Kit written as a refuse-at-once stub (STARTABLE NO), not a settings kit, because no honest settings-only path exists.
- D-2 I did not propose setting `WEBSITE_SITE_NAME` or `Assessment__Environment=uat` on the demo: that is a lock bypass.

## Q-questions for Tuesday (each with a default)
- Q-1 What does the product owner get instead for the 07:51 demo? (a) keep the demo as it is, with the Entra sign-in (default; nothing breaks, and he already sees the morning logo); (b) demo from the UAT site, which already shows the chooser with the morning logo, with the downsides that its synthetic-data banner is off and its identity is the review copy (UAT web `...-uat-25onzn`); (c) commission a code change for a demo-label chooser, to land after the demo (default for after).
- Q-2 If (b): does he accept the banner being off on UAT (a banner ruling of his, B418)? Default: no change, ask him.

## UNMEASURED
Whether a code change could be built, gated and deployed by 07:30 (assumed no). How the demo API treats `Assessment__Environment=uat` (not tested, not needed). The `test_security_baseline.py` rule bodies. B783 STATUS read by grep, not whole. The live state of either site (no HTTP, per fence). `infra/README.md` read by grep for key words only.

## Outside-the-fences disclosure
None known. Reads only: `date`, DRAFTER_RULES.md, B783 kit (first 140 lines via a tool-result file), B783 STATUS (grep and a tail), `gh api -X GET` under the HPSM-POC `GH_CONFIG_DIR` (contents and search/code), `lsof`, `/usr/bin/grep`, `ls`, `sed -n 96p` on model-routing.md. No az, no HTTP to a hosted host, no card read, no Jira. Only two files written. I did not read `.tools` content. B783 STATUS read does not equal "whole".
