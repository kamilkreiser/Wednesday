From Tuesday (the product owner's Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail channel from this project). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`.
# BRIEF B792 - SEAT-D36: HPSM-POC: switch the hosted DEMO site's sign-in to the UAT-style four-level chooser by APP SETTINGS ONLY (option b) - **DRAFTED AS NOT STARTABLE: the drafter found the settings alone cannot do it; this kit REFUSES AT ONCE unless a Tuesday addendum changes the method**

**Why this kit refuses (MEASURED by the drafter 2026-10-27 06:2x AEDT, read-only, `gh api -X GET` at `main` and at `0e631d75`):** the open sign-in is guarded by TWO LOCKS in code, on BOTH apps, and the demo fails both by its name and its label, which settings cannot honestly change:
1. Web, `web/src/server/auth/config.ts` `resolveAuth` (blob sha `88546d64`, identical at `main` and at `0e631d75`): mode `uat` needs `HPSM_UAT_OPEN_SIGNIN` exactly `on` AND `HPSM_ENVIRONMENT` exactly `uat` AND, hosted, the platform's own `WEBSITE_SITE_NAME` containing `-uat-`. The demo web is `app-hpsmpoc-web-demo-en46o7`: no `-uat-`. Switch on with a lock failing = mode `off` (fail closed): every sign-in and API call answers 503. That would BREAK the demo, not give a chooser.
2. API, `api/src/HpsmPoc.Api/Auth/UatOpenAuthentication.cs` `Read` (blob sha `e51abdb1`, identical at `main` and `0e631d75`; `Program.cs` calls `UatOpenAuthentication.Read` and `UseUatOpenRefusals` at `0e631d75`, lines 48 and 141): `Auth:UatOpen:Enabled` exactly `true` needs `Assessment:Environment` = `uat` AND `WEBSITE_SITE_NAME` containing `-uat-`, else the API **refuses to start**. The demo API is `app-hpsmpoc-api-demo-en46o7`: no `-uat-`; and the demo needs `Assessment__Environment` = `demo` for its own locks.
3. `WEBSITE_SITE_NAME` is the platform's own value. Overriding it, or relabelling the demo as `uat`, to get past a lock is a bypass of a safety lock the project wrote on purpose (`infra/modules/appservice.bicep` comments: the switch is `true` in uat ONLY; `infra/tests` rule_uat_only_switches / rule_uat_only_key_references; the key reference `uat-open-key` exists in the UAT vault only). **Nobody in this kit does that.**

So option b by settings only is **not available**. The old demo API `0e631d75` DOES contain the open sign-in and the `uat.action-off` guard (same blobs as `main`), so the API build is not the obstacle; the locks are. What would be needed is a CODE change (a new, gated lock for a `demo` level chooser: label and site mark `-demo-`, its own key secret in the demo vault, role grants, tests), then a build, a gate, and a deploy of the web AND the API to the demo. That is hours, not the 06:50-07:30 window, and it is the product owner's decision, not this seat's.

**Model route (for the future kit).** `fleet/specs/model-routing.md` row C6 "Deploy", line 96: `| C6 | **Deploy** (dev, staging, test or demo, ...) | no | no | no (unmeasured) | **1st** | — | **2 Opus 5.5 deploy-seat rows, 0.96 each, 0 rollbacks** ... Opus: RULED caution (as C3). **Production is P1** ... | A failed deploy is fixed at the root and re-verified (workspace hard rule 7). Any rollback: Kam is told. |`. Launch with `BRIEF_SEAT_LEVEL=opus`.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`, no other step, BEFORE any read, any `az`, any HTTP)
1. **Always, as drafted:** write STATUS with one line `B792 is NOT STARTABLE as drafted: the open sign-in is locked to label uat + site name containing -uat- on both apps (config.ts resolveAuth; UatOpenAuthentication.Read); a settings-only change breaks the demo (web 503 / API refuses to start) or bypasses the lock` and end `STOPPED: NEEDS TUESDAY <one question: which of Q-1 a/b/c in the drafter report>`. No `az` call, no HTTP, no write anywhere but the STATUS file.
2. **Unless the Stamp holds a Tuesday addendum** (a file `B792_ADDENDUM-*.md` in `tuesday/briefs/`, read whole) that names a NEW method and its gate (for example: a merged, gated PR that adds a demo-label chooser lock, with the web AND API package shas). Without that addendum slot 6 reads `NONE` and rule 1 applies.
3. Stamp slots: count runs of four consecutive underscores in your copy with `/usr/bin/grep -o -E '_{4}' <copy> | wc -l`: must read 0 (control: a scratch file holding five underscores reads >= 1). The last line must begin `READ-WHOLE-BY-TUESDAY: DONE`.
4. Clock: `date` after 07:30 AEDT Tue 27 Oct 2026, or any day other than 27 Oct 2026: STOPPED.
5. Authority: the product owner's tap of option b on card hpsmpoc-demo-site-level-chooser-1027 must be named in slot 2, plus the 2026-10-16 push-to-demo grant. Missing = STOPPED. (Even with the tap, rule 1 holds: a tap chooses the goal, it does not unlock a code lock.)

## WHAT THE SETTINGS WOULD BE IF THE LOCKS WERE RELAXED BY CODE (reference only; DO NOT RUN; names MEASURED from `infra/modules/appservice.bicep` at `main` = `0e631d75`, blob `2734479b`)
- Web: `HPSM_UAT_OPEN_SIGNIN`=`on`; `HPSM_ENVIRONMENT`=(label the new lock accepts); `HPSM_UAT_OPEN_KEY` (>= 32 bytes; UAT: Key Vault reference to secret `uat-open-key`); `AUTH_SECRET` (>= 32 chars; already a vault reference to `bff-session-key`); `HPSM_DEMO_NOTICE` stays `on`; `HPSM_API_DEV_AUTH_HEADER/VALUE` must be absent.
- API: `Auth__UatOpen__Enabled`=`true`; `Auth__UatOpen__Key` (same secret as the web's key); `Assessment__Environment`; `HostedDemo__Seed__OwnerObjectId/OwnerTenantId` (already set on the demo).
- Entra: in mode `uat` the web has NO Entra sign-in (sign-in and callback answer 404; `routes.ts`): the chooser REPLACES Entra, it does not sit beside it.
- A settings change restarts the app (about 1-2 min on B1; UNMEASURED here).

## STANDING LINES
PRIOR-WORK CHECK (a READY without a PRIOR WORK section is returned); no message to any human; no Jira write; never delete (quarantine); this phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only. No production exists for HPSM-POC. Ports if ever needed: 9660-9669 only (see report), never 9540-9549, 9640-9649, 8760-8769, 9390-9399.

## PARTITION
B783 (web `68ebdbf7` on both sites, done 05:58) and B782 (the circle-only logon variant, `Datasec/HPSM-POC-H41`) are other seats'. This seat touches neither and writes nothing hosted.

## HOLDS (never, in this brief)
Any `az` write; any app-setting change on the demo; setting `WEBSITE_SITE_NAME` or relabelling the demo as `uat`; copying any UAT secret; any deploy; any HTTP to a hosted host.

## Stamp
- 1. Stamp time (AEDT, date): ____
- 2. Launch authority (the product owner's tap of option b on card hpsmpoc-demo-site-level-chooser-1027, named, plus the 2026-10-16 push-to-demo grant): ____
- 3. Hard stop (no change START after 07:30, DONE by 07:45): ____
- 4. Pins as Tuesday read them (main head; demo web/API builds live): ____
- 5. Ruling: Tuesday accepts that this kit refuses as drafted (CONFIRMED / NOT CONFIRMED): ____
- 6. Addendum naming a new method and its gate (or `NONE`): ____

**Last line of STATUS, exactly one of:** `DEPLOYED: <only after an addendum>`, `ROLLED BACK: <reason>`, or `STOPPED: NEEDS TUESDAY <one question>`.

READ-WHOLE-BY-TUESDAY: ____
