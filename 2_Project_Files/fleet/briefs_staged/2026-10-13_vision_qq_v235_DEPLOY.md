# BLUF — Datasec/Vision_Sales_Portal: PUBLISH QuickQuote v2.35 to the LIVE site, NOW. Kam authorised it in Tuesday's terminal on 2026-10-13 ~12:1x AEDT, verbatim: "once agents finish up, deploy everything and wrap up". Your round IS finished, so this is the QuickQuote half of "everything". Tuesday ruled card quickquote-v235-publish-1013 = (a) on those words, and receipted the reading on the live board (HTTP 201 bf-7dfdbaafa567). Option a: "The Vision seat builds the image at exactly 3dd15bc, keeps 2.34 for rollback, switches the site, and checks it live; rolls back on any failure." This is a PRODUCTION change and that card is the whole of its scope. Same runbook as yesterday's v2.34 publish. Mail STATUS at each step; stop and mail only on a refusal or a failed check. Then WRAP.

## MEASURED BY TUESDAY (2026-10-13 11:5x AEDT)
- QuickQuote main = 3dd15bcc09862047f6500e1813901edd8a686888 (ls-remote). Its tree equals the gated d030674 (your MERGED's read).
- Code scanning on main: {"fixed":14}, 0 open (gh api, Tuesday's read).
- The live image is v0.6.2-tool2.34-108bbb4 (your az read after the merge). Re-read it in step 1: that tag is the rollback.

## STEPS (the runbook, with the card's guards)
1. **Identity + rollback point.** `az account show` with your project's AZURE_CONFIG_DIR: expect tenant d500ebad / subscription 0c57ab37, and quote the principal. Read the web app's CURRENT container image (linuxFxVersion) and quote it. **That tag is the rollback.** Read live `/healthz` and quote it.
2. **Build** from a clean checkout at EXACTLY 3dd15bc (a worktree or archive of that sha, never a dirty tree): `az acr build --registry hpasqqacr --image hpas-quickquote:<tag> --file stage3/Dockerfile .` from the repo root. Tag in the convention, e.g. v0.6.3-tool2.35-3dd15bc (say why). Quote the final status and digest.
3. **Switch** the web app to the new tag. Quote the command and output. Wait for the restart.
4. **Live check, by you, against the LIVE URL:** `/healthz` OK with its mail block; the page badge reads v2.35; one AUD and one CAD quote price as before; the sign-in page loads normally (the new rate limit must not refuse normal use: a handful of loads, nothing near 300); then the log-capture checklist. Screenshot the live page.
5. **If any live check fails: ROLL BACK** at once to the step-1 tag, confirm it is live, and mail Tuesday with the evidence. Do not debug on production.
6. DEPLOYED mail: old tag, new tag + digest, each live check with its instrument, the screenshot path. **Then WRAP your session** (Kam: "and wrap up"): history entry, handover, move your scratchpad worktree aside, wrap mail.

## HOLDS
- Only this deploy. No other Azure change: no scaling, settings, secrets or new resources. Do NOT deploy the AUD-seed or g17-test-strength backlog branches, or anything not in 3dd15bc. The Dependabot round is NOT started (its card is still with Kam).
- No contact with any customer or John Spears; Kam tells John.
- Never delete the old images or tags (2.34 is the rollback; 2.33 stays too).
- Every factual sentence in a mail names its instrument.

PROVENANCE:
- Kam's authority | his message typed into Tuesday's terminal, 2026-10-13 ~12:1x AEDT (this session) + card quickquote-v235-publish-1013 ruled a in /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/dashboard/data/decisions.json | read 2026-10-13
- main 3dd15bc + alert states | git ls-remote + gh api code-scanning (Vision GH_CONFIG_DIR) | read 2026-10-13
- runbook | /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool/CLAUDE.md (Deploy + log-capture lines) | read 2026-10-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-13 12:15
-- Tuesday
