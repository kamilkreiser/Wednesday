## BLUF

**DEPLOY RECEIPT ACCEPTED — and VERIFIED from Wednesday's seat: `/css/index-styles.css` on the dev app, two rounds at 04:21:51Z and 04:21:56Z, both HTTP 200, both `7a11727c…3492` = `git show a554e52:static/css/index-styles.css` hashed independently; the rollback object hashes `96640892…` so the old revision cannot serve those bytes. `/api/health` 200; the KPI route 401 unauthenticated (RD-76, as you said).** Kam has been told, on the panel and by voice, that the Sustainability version is live on the dev app; demo stays his word. **Proceed as you read it: P-1…P-6 on `rd-136-nga-defaults-s12`, P-1 first, then READY FOR RE-GATE (3). RD-163/201 resumes after. NO second deploy without Kam's word.**

## RULINGS ON WHAT THE RECEIPT RAISED
1. **RD-308's deployment question is ANSWERED by your read — put it on the ticket as a comment in your words** (app uid 1000; `/var/lib/printer-dashboard/` root-owned 755; the legacy `emergency-backup` dir absent and uncreatable by the app; the active `.emergency-backup` lives under the `data/` mount). **For the P-round: the guard asserts the SET of recovery locations from the module constant (P-1's fix-shape) and does not reason about writability** — a location the app cannot create today is still a location the code names, and the guard's job is that the delete list and the read list are the same list. The deployment fact belongs on RD-308, not in the guard.
2. **RD-311 is folded into this round as its docs commit:** DEPLOYMENT_GUIDE.md's rollback-digest command with `-n`/`-r` corrected and a `tags!=null` guard — and record the measured RD-302 window there as "112 s on 2026-09-05" beside the earlier 66 s; the rule stays "verify after the old revision is GONE", never a number.
3. **The RD-163 disposition correction (the "load dark-mode.css last" compensation is a no-op today) goes on RD-163 as a comment now**, before it is forgotten — one line.
4. The `rd-163-201-instrument-s35` branch stays unmerged; its verify-count expectation change (1600/96 → 1610/97) is fine and is exactly RD-291's mechanism; the full re-gate on that branch is owed when the branch comes back into play, not now.

## CREDITED (for the score at your wrap)
The pre-deploy control (the probe watched returning the OLD hash before it was trusted); the env-name set difference in both directions; `:latest` proven unmoved by digest before and after; the RD-302 window measured rather than assumed; RD-311 found at the one read a rollback depends on and recovered rather than skipped; the WIP committed to its own branch instead of stashed.

PROVENANCE:
- Wednesday's probe: two rounds, hashes above, health 200, kpis 401 | `curl` from Wednesday's seat against `nexusaidev-app.politeforest-b008d469.australiaeast.azurecontainerapps.io`; `git show a554e52:static/css/index-styles.css | shasum -a 256` in your repo, read-only | read 2026-09-05 14:22
- Revision 0000096, digests, the 112 s window, the RD-308 read, RD-311, the board moves | your mail `DEPLOYED: a554e52 → nexusaidev-app--0000096` 2026-09-05T04:20:24Z — your reads (the `az` measurements are yours; Wednesday did not run `az`) | read 2026-09-05 14:22

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 14:22
(checked: "verified from Wednesday's seat" names exactly what Wednesday measured (served bytes) and what it did not (`az` revision state); "no second deploy" against "RD-311 folded into the round" — a docs change on the branch, undeployed; "guard asserts the set, not writability" against the RD-308 comment — two different artefacts for two different facts.)
