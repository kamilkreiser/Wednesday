# BLUF — Datasec/Vision_Sales_Portal: PUBLISH QuickQuote v2.34 to the LIVE site, NOW. Kam authorised it on the live board on 2026-10-12, verbatim: 19:12:13 "these look great.  Please deploy", and 19:12:23 "Decision quickquote-v234-publish-1012: a — Publish v2.34 now" (card option a: "A Vision agent builds the image from main 108bbb4, keeps the current live tag for rollback, switches the live web app, and checks the live page (CAD offered, a CAD quote prices). It reports the old and new tag."). This is a PRODUCTION change, Kam-signed, and that card is the whole of its scope. Follow QuickQuote's own runbook exactly. Mail STATUS at each step below. No plan confirmation is needed (the card IS the plan); stop and mail only on a refusal or a failed check.

**Addressed to the cockpit seat `Datasec/Vision_Sales_Portal`.** Read first: QuickQuote CLAUDE.md, "Deploy" and the "Deploy checklist — log capture" lines (around :185-196), plus your predecessors' MERGED mail (07:19Z) and wrap on this inbox.

## MEASURED BY TUESDAY (2026-10-12 19:1x AEDT)
- QuickQuote main = 108bbb443647e0f1c8ec2f426e9f33c15585eaa2 (ls-remote). Its parents are e408904 + 1270b71 (gh api). Its tree equals the gated 1270b71's tree (your predecessor's rev-parse).
- The last publish (2026-09-27) was image v0.6.1-tool2.33-986f7b8 (Vision history.md, as relayed by the previous seat). The CURRENT live tag is UNMEASURED. Read it yourself in step 1.
- The Dockerfile runs strip.js (stage3/Dockerfile:25), so the image builds the hosted page itself. That is why the CI stage3 red on a fresh checkout does not apply to the image.

## STEPS (the runbook, with the card's guards)
1. **Identity + rollback point.** `az account show` with your project's AZURE_CONFIG_DIR: quote the tenant, subscription and principal, and expect d500ebad / 0c57ab37. Read the web app's CURRENT container image: `az webapp config container show -n hpas-quickquote -g hpas-quickquote-rg` (or the site's linuxFxVersion). Quote it. **That tag is the rollback.** Also read `/healthz` on the live site and quote it.
2. **Build** from a clean checkout at EXACTLY 108bbb4 (a git worktree or archive of that sha, never a dirty tree): `az acr build --registry hpasqqacr --image hpas-quickquote:<tag> --file stage3/Dockerfile .` from the repo root. Tag in the existing convention, e.g. v0.6.2-tool2.34-108bbb4 (say which you chose and why). Quote the build's final status and digest.
3. **Switch** the web app to the new tag (the runbook's "point the webapp at the new tag"). Quote the command and its output. Wait for the app to restart.
4. **Live check, by you, against the LIVE URL:**
   - `/healthz` OK, with its mail block as the runbook says;
   - the page badge reads v2.34;
   - CAD is in the currency list;
   - one CAD quote prices (CA$ shown);
   - one AUD quote prices as before.
   Use the site's normal sign-in only as far as it is open (no new accounts, no test emails to customers). Then run the log-capture checklist (az webapp log show; the diagnostic setting qq-console-to-la). Screenshot the live CAD quote.
5. **If any live check fails: ROLL BACK** at once to the step-1 tag, confirm the old version is live, and mail Tuesday with the evidence. Do not debug on production.
6. MERGED/DEPLOYED mail: the old tag, the new tag + digest, the live check results (each with its instrument), and the screenshot path. Then wrap.

## HOLDS
- Only this deploy. No other Azure change: no scaling, no settings, no secrets, no new resources (money is Kam's). Do NOT deploy the AUD-seed branch or anything not in 108bbb4.
- No contact with any customer or John Spears. Kam tells John.
- Never delete the old image or tag (it is the rollback).
- Every factual sentence in a mail names its instrument.

PROVENANCE:
- Kam's authority | live board via /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_msgs.sh (19:12:13, 19:12:23 rows) + card quickquote-v234-publish-1012 in /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/dashboard/data/decisions.json | read 2026-10-12
- main 108bbb4 + parents | git ls-remote and gh api (Vision GH_CONFIG_DIR) in /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool | read 2026-10-12
- runbook | /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool/CLAUDE.md lines 185-196 | read 2026-10-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-12 19:14
-- Tuesday
