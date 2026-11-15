# Deploy kits, 2026-11-16 (Tuesday s281): MPS showcase and Composer demo

Tracked so the commission survives rotation. If a report below is absent at the next boot, RE-COMMISSION it from this file.

**Authority (verbatim, live board, view=tuesday):** 07:04 `hpsmpoc-deploy-round-scope-1116` = "c — All Datasec projects' demos too"; 10:00:13 note on `datasec-demo-deploy-round-apply-1116`: "and deploy hPSM as well". Tuesday posted card `hpsmpoc-review-site-deploy-confirm-1116` (a = Composer, MPS and the HP review site now; b = Composer and MPS now, HP review site later; c = hold). **Options a and b both include Composer and MPS, so these two kits are drafted now and LAUNCHED ONLY after Kam taps a or b on that card.** Tap c = neither launches. Kam's 15 Nov approval of the MPS stop words: card `mpscalc-rollforward-stop-words-1115` = a "Approve the words as written".

**Census (read it whole first):** `tuesday/briefs/2026-11-16_DEPLOY-ROUND_rides-along.md` (sections 2 MPS and 4 Composer, and section 6).

## For every drafter
Read `tuesday/DRAFTER_RULES.md` whole first. Copy the SHAPE of your template kit and its seat's STATUS (Deviations and Corrections first). Write ONLY your kit, its `.measured` sidecar (stamp_check rc 0), your report (last line `DRAFTED B<n>: kit <lines> lines, sidecar rc <rc>, questions <n>`), scratch under `fleet/state/s281/d<B-number>/`. Read-only everywhere: gh GET only (the project's own GH_CONFIG_DIR), az READ verbs only after `az account show` under the project's own AZURE_CONFIG_DIR, public GETs of health/version endpoints only. No deploy, no az write, no push, PR, Jira write, mail, board, Artifact, cd. Clocks from `date`. Every literal a seat must match is measured or reworded. Each deploy seat is Opus (model-routing row C6) and runs its own `az account show` first (tenant ec01829b's environment mapping is UNRESOLVED: the kit says to verify, never to assert).

## B1607 SEAT-D63: MPS hosted showcase deploy of main (template: `tuesday/briefs/2026-11-12_B1542_SEAT-D62_mps-hosted-deploy-0bb3ed12.md`)
Deploy MPS main (5e800095 or later: re-read) to the showcase per B1542's route, with its rollback, the post-deploy checks, the MPSCALC-224 host read (the patched Xml in the package), the roll-forward-only caveat after #196, and the seed-secret question (card `mpscalc-deploy-seed-secret-expired-1112` was ruled a: read what it said and follow it). The showcase is treated as live with real users' data: back up first.

## B1608 SEAT-D64: Composer demo deploy of main (template: `tuesday/briefs/2026-10-31_B986_SEAT-D42_composer-demo-deploy-merged-main.md`)
Deploy Composer main (b4681297 or later: re-read) to the demo VM per B986's route, with its rollback and live checks. **First the words gate on the customer-visible PRs the census names (#95, #113, #119, #120, #122, #124, #125, #130), B986 Step 3 as the template:** any customer-visible string not ruled is a STOP that lists it for Kam. The footer-look row #474 (open, not ruled) is named; if a riding change depends on it, STOP. Composer deploys only on the product owner's card: the card above is that card (say so in the kit).
