# B1932 DRAFTER COMMISSION (Opus, in-session, READ-ONLY) -- Datasec / OXPd_2: lane D ROUND 2 (fix round after gate B1930 GO WITH FINDINGS), one build kit for seat Datasec/OXPd2-X35

Re-commission if the kit or report is absent (one Agent call, model opus: "read that commission whole and do it"). Commissioned by Tuesday (s311), written at 2026-11-22 22:53:17 +1100. Return a 10-line summary with `STARTABLE: YES` or `NO` as line 1.

## WHAT IS ESTABLISHED (read each at source)
- Round 1: kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1921_SEAT-X33_oxpd2-d-audit-limit-duplicate-race.md` (Stamp S4: Q1 = b, the in-save refusal), the seat's STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Briefs/2026-11-22_B1921_STATUS.md`, branch `b1921/d-audit-limit-duplicate-race` at `69eeb1dc1e6a24747bcf0708a3cf85f33cfc51f5` (PUSHED: never rebase; ONE fast-forward commit on top).
- The gate: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1930_verify/VERDICT.md` (read WHOLE) and its probes G01 to G07 in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/g1930/_quarantine/` or its evidence folder.
- Main now: re-read by GET (it was 83683af4 at the gate; lane A1's PR 23 and lane S may land before this round: no Data path in either).

## THE KIT (Tuesday's decisions as coordinator)
1. **The Minor (TUESDAY'S CALL: a fix round before landing, because the round-1 README audit sentence is false in the nested-save shape):** `saving` restores its PREVIOUS value at the end of a save (`var outer = saving; ... finally saving = outer;`), sync and async paths; a red-first cell for the gate's G03 (a handler that runs its own SaveChanges first, then changes saved entries: refused) and G04 (an interceptor that does the same and removes entries: refused).
2. **Info 3:** committed cells for the `Tracked` half and the synchronous `SaveChanges` path (the gate's G02 and G01), each red under its mutant (`Tracked` unsubscribed; the sync override's flag removed).
3. **Info 3, README:** the command interceptor named among the limits (Stamp S4 of round 1 said it would be). **Info 2:** a `SavedChanges` handler runs after the commit (the appended row is written, then the save is refused): name it as a limit with its cell, or say why not.
4. No other change; no public member, schema or package (surface.py equal). Totals: round 1's +6 plus the new cells (measured by program).
Gate after: G1 again (round 2 of 2: a NO GO after this goes to the product owner as a card).

## FORM AND RULES
- FORM: round 1's kit (B1921) and the newest fix-round form, `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1915_ANSWER-1_issuer-window-on-library-clock.md` (a fix commit on a pushed branch: never rebase, the merge-base check, hosted2.py with the seat's own total) and `DRAFTER_RULES.md` (red-first, `.measured` sidecar, `stamp_check.py` exits 0, PRIOR-WORK CHECK, read load in bytes, stamp section with `____` slots and the `READ-WHOLE-BY-TUESDAY: ____` last line). The seat works in a NEW clone of the branch (`clone.py`, then checkout of the branch at 69eeb1dc), lane folder `<project>/.tools/b1932/`.
- Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1932_SEAT-X35_oxpd2-d-round2.md`, sidecar, report `2026-11-22_B1932_DRAFTER-REPORT.md`, scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1932/`.
- READ-ONLY toward the project, Jira and GitHub (`gh api -X GET` only under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/.gh-config'`); prototypes only in your own scratch clone (push URL `invalid://no-push`); every heavy job through the round's `heavy.py`, one at a time (gates and seats share the lock); no `cd`; never delete; `python3 -I`; nothing under `Source_Documents/` or the NAS library; nothing to any human.
