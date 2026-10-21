# B418 DRAFTER REPORT (Datasec / HPSM-POC), 2026-10-21 ~19:50 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B418_SEAT-D24_hpsmpoc-uat-template-drift.md` (106 lines, structure copied from B409's). Written by a Sonnet drafter. Nothing was run except read-only git/gh GETs and local file reads; no npm, dotnet, pytest, bicep, az or HTTP.

## Slots for Tuesday to fill at stamping (2; the stamped copy must print 0)
1. `@STAMP_TIME@` in the Stamp paragraph.
2. `@LAUNCH_AUTH@` in the Stamp paragraph. The brief requires it to name the stamping seat, that it READ the brief whole, **a hard-stop time** (I was given none, so I did not invent one) and the ruling cards.

Check before stamping: `/usr/bin/grep -o -E '@[A-Z_]+@' <brief> | sort | uniq -c` reads exactly those two, one each (MEASURED 19:5x).

## What the brief builds (3 commits, one branch `b418/uat-template-drift`, ends READY FOR QA, tier 2 proposed, Sonnet, row C2 `model-routing.md:92`, gate row G2 `:109`)
1. **Infra:** `HPSM_DEMO_NOTICE` off for `uat` (`appservice.bicep:204` today is `contains(['demo','uat'], …)`), and `webOutboundAddresses` committed in `infra/env/uat.bicepparam`. Four existing expectations in `test_security_baseline.py` must change (the `DEMO_AND_UAT` entry, `test_mutation_demo_notice_on_everywhere`, `test_d7_…_notice_…`); the brief names them and forbids renaming tests (the d7 test name will be misleading afterwards; a new row sits beside it).
2. **API:** `UatOpenAuthentication.cs:94` `GetValue<bool>` becomes an exact ordinal `true`. Padded/case-varied `true` refuses to start (message names the setting, never the value); other cells stay as today, with the builder first measuring today's outcome per cell.
3. **Doc:** one line in `infra/README.md` step 7 for "restart a new site once before its first code deploy" (an observation, n=1, not a rule).

## Answers to the commission's own questions
- **Does the demo's pattern keep the address list out of git? No, it keeps it IN git** (`infra/env/demo.bicepparam:19-24`, 25 addresses with a C-59 comment "Not secrets: Azure-owned outbound addresses… Kept here so an infra redeploy keeps the product owner's ruling instead of emptying the list"). The brief therefore commits the UAT list the same way.
- **The UAT list is NOT the demo's.** B410's applied list (25 IPv4, read by me from its untracked `.tools/b410/build-b/uat-b3.parameters.json`, mtime 18:47) shares 0 addresses with the demo's (different stamp). I quoted the 25 in the brief with a sha256 (`e1d68385…49b5`) because the builder may not open B410's tree and has no `az`. I read that one file once, one key only. It is the only thing I opened outside the code repo objects and Tuesday's tree.
- **Is the list still current?** UNMEASURED (needs `az`). The brief makes FOR TUESDAY ask the deploy seat to compare against a fresh `possibleOutboundIpAddresses` read before the next UAT template deploy.
- **Routing:** C2, Sonnet, tier-2 gate. Reason recorded: decisions are made (banner ruling, C-59 pattern, B417's fix-shape); item 2 is a stricter parse of an existing switch with an exact outcome table. If you read item 2 as "auth design" and want C3/Opus or a tier-1 gate, say so at stamping; the Stamp paragraph has room.

## Questions for Tuesday (decisions NOT built; my recommendation each)
1. **Application logging on the UAT API** (B410: the start scan had no instrument; the demo has it on by hand, the template has none: `git grep` of `httpLogging|applicationLogs|logsConfig|detailedErrorLogging` over `infra` at `ae7a2c86` printed 0, positive control not run).
   Recommendation: **yes, but as a separate follow-up brief, UAT-only (`environmentName == 'uat'`), not in B418.** Reasons: it is a new `Microsoft.Web/sites/config` resource or siteConfig change, so a different surface from this lane's tables; a template-wide setting would touch the demo's API (never-touch-prod class); and the start scan is the only consumer I found. Before writing that brief, someone should read what the demo has set (the portal state, via the deploy seat with `az`), so the template mirrors a measured setting rather than a guess.
2. **`deploy-from-ci.sh fetch --run <id>`** (B410: `fetch` takes only `<sha>` and filters `--status success`, `deploy-from-ci.sh:49`; ADDENDUM-3 needed the fetch steps by hand, verify unchanged).
   Recommendation: **do not build now.** The strictness (green-only) is a safety feature; the exception was a one-off ruling and the manual path worked with the verifier intact. If you want it later, make it a tier-1 brief (it is a deploy tool) where `--run` requires an explicit reason string and still runs `deploy-package.py verify --expect-run`; `scripts/**` is outside B418's partition on purpose.
3. **Runbook line "restart a new site before its first code deploy":** built inside B418 (doc-only, `infra/README.md` step 7, the file is in the PARTITION). Recommendation: keep it in, worded as one observation (UAT, 21 Oct, n=1, the stale `LastError` reading fits but is unproven). The B410 platform story has a competing explanation I could not rule out (the status tracker counted the earlier code-less container failure). Not step 4: that step is about secrets, where a restart is the documented wrong move.
4. **Hard-stop time for the seat** (not in my instructions). Recommendation: a modest one (the work is small), stated in `@LAUNCH_AUTH@`.

## Suspect or worth your eye
- **B417-1 outcome choice is mine:** padded/case-varied `true` is made to **refuse to start**, not to silently read as off. Reason in the brief (same direction as the label's padded cells; a template meaning "on" that quietly runs closed is a harder mistake to see). It changes `True`/`TRUE` from "opens" to "refuses", which is stricter than B417's own fix-shape allows ("off or refuses to start"); both fit its wording. Override at stamping if you prefer plain-off.
- **Gate B417's own text says "exact `true` (ordinal)"**; the commission says the same. I kept `False`/`FALSE`, `""` and the like at **today's measured behaviour** (the builder measures first), to avoid breaking existing config and rows. If the builder's probe disagrees with B417's matrix, it reports under Corrections.
- **Line numbers** in the brief marked `~` (`rule_env_switches`, the two test lines near 879-887 and 957-960) are from a `sed` window, not exact `grep -n`; the brief tells the builder to re-measure all of them.
- **Open-PR and port checks are point-in-time:** 0 open PRs (control 177/176) and nothing listening on 8000-8009 at 19:39; the port check had no positive control. Both are re-run by the builder as REFUSE checks.
- **B410's note that main's CI run at `ae7a2c86` had a cancelled `api-other-and-feedback` shard** (20-minute timeout): the builder's whole-API baseline may be slow or red for reasons that are not its edits; the brief makes "red in a file you touch" a STOP and says a slow shard is not a red test. The red-main ticket (ADDENDUM-3) is Tuesday's.
- **The sibling list is empty.** I found no live sibling for these files; live panes are UNMEASURED.
- **Web is deliberately untouched.** The banner is read by `web/src/app/layout.tsx:23`; B418 asserts 0 web paths in the diff and leaves the e2e mention list for the QA lane. The brief states "No new customer-visible words".
- **Expected effect on the live UAT:** none (it already runs banner off and the 25 addresses by hand); the next UAT template deploy becomes a no-op on those two settings. That should be proven with a what-if by the deploy seat, not by this lane.

## Files written (only these two)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B418_SEAT-D24_hpsmpoc-uat-template-drift.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B418_DRAFTER-REPORT.md`

SELF-CHECK: read B409's brief whole, B410's STATUS whole (both pages), B410 ADDENDUM-2 whole, B417 finding B417-1 and d3, `model-routing.md` rows C2 and G2; measured main by `ls-remote` = `ae7a2c86` (expected), `b418*` refs absent (control `b386*` present), 0 open PRs; no forbidden git verb, no `gh` write, no Artifact/Docs/mail/chat tool, no `rm`; no other client's name and no person's name written in either file; no HP Restricted path opened.
