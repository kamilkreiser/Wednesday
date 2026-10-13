DEMO DEPLOY to S96O (Datasec/NexusAI-O): deploy NexusAI main @ 3907c57 to the NexusAI DEMO (nexusaidev-app, nexusai-dev-rg). Tuesday's GO. Self-contained.

## BLUF
Deploy main 3907c5789a7d87302c0cdd20f4250e2f391971e4 (RD-839, RD-838, RD-840+841 and everything since the demo's last deploy) to the demo by the MANUAL path, with a recorded rollback, your Entra pre-check FIRST, and a live verification. **STOP and mail before the swap if the Entra pre-check shows a configured security group whose membership the app may not be able to read.** Roll back on any failed live check, then mail.

## Authority (each read by Tuesday)
- Kam, Tuesday's terminal, 2026-10-13T01:14:24Z (typed, human), verbatim: "once agents finish up, deploy everything and wrap up".
- Kam, live board 2026-10-13 18:52:36 AEDT (view=tuesday), verbatim, on the Sustainability screenshots: "these look great.  I like the new look.  please make the change and push them live" (your C-214).
- C-127 (merges and demo redeploys are Tuesday's GO on a QA-gated head). The demo is NOT production; Partner Center / Marketplace, production, money beyond the ACR Tasks build (C-30) and any message to a human are NOT covered.
- Gate status of what deploys: every merge since the demo's last revision went through its gate; the last three = gate 22 GOs.

## Measured by Tuesday
- main = 3907c57 (git ls-remote). Its push Build = 38387979577 completed / success 12:03:45Z, log "VERDICT: PASS — 4506/4506 tests passed across 283 suites (jest exit 0)".
- deploy-demo.yml cannot do this: the repo has NO `demo` environment (environments = dev only), no CI_DEPLOY_ENABLED variable; every push's "Deploy demo" run is `skipped` (seen on b2eecdf and 94cb067).
- Method record: 5_Project_History/2026-09-21_S76D_demo-sync-measurement.md (you read it whole). Last recorded demo deploy: revision nexusaidev-app--0000099 (main aae041a, 2026-09-21). The CURRENT running revision is unmeasured by Tuesday: read it in step 1.

## Steps (one at a time; your launcher-scoped az; re-verify identity before the first az call)
0. Identity: `az account show` = tenant d500ebad…, subscription 0c57ab37…, SP a71b85e7 (nexusai-claude-deploy). Anything else = STOP.
1. ROLLBACK ANCHOR: record the active revision name, its image and its DIGEST (`az containerapp revision list` + `show`), and back up the settings files on nexusai-data (C-19). Put all three in your STATUS before any write.
2. ENTRA PRE-CHECK (your proposal, accepted): read the demo's stored sign-in settings READ-ONLY, names and presence only, never values. If a security group is configured: STOP and mail what you found (C-54 fail-closed could lock sign-in). If none is configured: say so and continue.
3. BUILD: `az acr build -r nexusaidevacrfa39 --image nexusai:<ver>-s96o-3907c57 --build-arg BUILD_COMMIT_SHA=3907c5789a7d87302c0cdd20f4250e2f391971e4 .` from a CLEAN worktree at exactly 3907c57 (no node_modules.* folders inside). A tag that already exists STOPS the build. Record the new digest.
4. SWAP: `az containerapp update -n nexusaidev-app -g nexusai-dev-rg --container-name nexusai-api --image nexusaidevacrfa39.azurecr.io/nexusai@<new digest>`. No env change.
5. VERIFY (RD-302 + C-07 + RD-327): wait until the active-revision list holds ONLY the new revision (name it); /api/health 200 and its "build" = sha256(<40-hex>)[:16]; env NAMES and secretRefs identical before/after (names only); the Sustainability page served by the new revision carries the RD-840/841 assets (fetch the CSS/JS the page references and confirm the new tile/grid rules are present; the pages themselves are behind RD-76 SSO, so say what you could and could not render).
6. ON ANY FAILED CHECK: `az containerapp update … --image <old digest from step 1>`, verify the old revision is again the only active one, then mail.
7. DEPLOYED mail to Tuesday: the old and new revision + digests, the build hash match, every check with its instrument, what was NOT checked. Then Jira (RD-840/841 and RD-838/839: deployed to demo, revision named). Then WAIT for Tuesday's wrap word (it follows at once).

## Not covered
Partner Center, the Marketplace listing, production, any new Azure resource, any secret change, deleting any image or revision, any message to a human.
-- Tuesday
