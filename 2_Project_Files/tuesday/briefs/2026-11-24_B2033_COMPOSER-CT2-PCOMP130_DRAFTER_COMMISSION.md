# B2033 COMMISSION (in-session, READ-ONLY): Security Composer PCOMP-130 build kit, lane C-T2 (q-gate test plants for every alternative), seat `Datasec/Composer-C109`

Commissioned by Tuesday (s321) on 2026-11-24, after the sweep below. One drafter (Sonnet; an XS test-only lane, routing table `fleet/specs/model-routing.md`: name the row). Return a 10-line summary whose line 1 is `STARTABLE: YES` or `NO`.

## WHY THIS LANE, AND WHOSE CALL
Sweep `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_SWEEP-1110_datasec-actionable-lanes.md` ranks C-T2 second (line 26; ticket detail line 50; question line 204). PCOMP-130's own text says "Not ruled: whether and when to do it": building it now is Tuesday's call under the product owner's standing words (Tuesday terminal 2026-10-24, verbatim: "check tickets that can be actioned and if there are any, always start the process of working through it.  You dont need to wait on me to request"), the same call Tuesday made for PCOMP-67. Not his ruling.

## BINDING
The Composer block at the top of `/Volumes/Datasec_DEV/TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md` (no deploy of a changed content release without his own card) binds: this lane is branch-only, PR by Tuesday, NO deploy of any kind; the kit carries the `CONTENT_HASH` refusal line `tuesday/DRAFTER_RULES.md` requires for Composer kits.

## STATE (RE-MEASURE every one you freeze)
Composer main `8b9ab200` per the sweep, 0 open PRs. PCOMP-130: re-read whole by Jira GET (credentials by name in-process from the project's own `4_Credentials/.env`, never printed; list the Datasec projects folder to find the Composer project, never a `%20` duplicate). The owned file: `packages/content/test/b330-sm316-qgate.test.ts` ONLY (sweep: patterns at line 88 and 97, `morePlants` at 25/31/37 and 208-214). Any other path is a STOP naming the line. PRIOR WORK: the PCOMP-67 kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1959_SEAT-C108_composer-ct-qgate-plants.md` (its form; PR 132) and C-158/C-159 in the project's CLARIFICATIONS.

## THE KIT
Form: B1959 above. Branch `b2033/pcomp130-plant-every-alternative`. Regression per the ticket: each of the three mutants (drop True, drop svg, drop jpg) turns the plant check red; the unmutated file stays at the same test count with the same names; prove it in your own prototype in a scratch clone (the runner's summary lines quoted, the test command run as the kit freezes it). `tuesday/DRAFTER_RULES.md` binds whole (sidecar, `stamp_check.py` rc 0, hashed sources, PRIOR-WORK CHECK, stamp slots, last line `READ-WHOLE-BY-TUESDAY: ____`). Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2033_SEAT-C109_composer-ct2-plants.md`, report `..._B2033_DRAFTER-REPORT.md`, scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s321/d2033/`.

## RULES
READ-ONLY toward the Composer project, Jira and GitHub (`gh api -X GET` only under that project's `4_Credentials/.gh-config`). Prototype in a scratch clone only. No `az`, ssh, or hosted site. No `cd` (absolute single-quoted paths); never delete; `python3 -I`. Nothing to any human. Nothing of HPSM-POC or any other client.
