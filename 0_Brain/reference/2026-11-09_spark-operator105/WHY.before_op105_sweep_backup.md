# Quarantined 2026-11-09 00:1x AEDT by Wednesday (overnight seat). Reversible: move it back.
READY_KS-1868-...-O85-P1 (auth accountLockout.ts catches) does NOT apply at develop 7eda23b34d3b:
develop commit 70ba9ffeb (Refs KS-1967, 2026-11-03, "the login lockout refuses (503) while the session store is down")
changed the file after the READY was cut. Measured by Spark operator 104 (0_Brain/reference/2026-11-09_spark-operator104/ready_check.out: NEITHER(drifted/partial)), not re-run by Wednesday.
A held READY that cannot be raised only blocks the file (it blocked the KS-2022 round-2 rebrief).
The KS-1868 accountLockout piece is NOT done: it goes back to the pool and needs a fresh brief at the tip, AFTER the KS-2022 rebrief has used the file. O85-P2..P6 untouched.

Also moved here: HOLD-NOTE_O85-P1_accountLockout_fail-open_risk.md (Wednesday 2026-11-03, gate 131 G131-F5: an 'ordinary Error' fix at accountLockout.ts can turn the lockout FAIL-CLOSED into FAIL-OPEN). ANY future brief for the KS-1868 accountLockout piece carries that note verbatim and goes to a TIER 1 Opus gate with the fail-closed question as its headline.
