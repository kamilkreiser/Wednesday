# HOLD NOTE on O85-P1 (auth accountLockout.ts :89/:119/:130) — written by Wednesday 2026-11-03 01:2x AEDT

DO NOT RAISE O85-P1 AS AN ORDINARY KS-1868 PASS.
Gate 131's finding G131-F5 (verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate131-ks1868-pr1949/verdict.md):
a KS-1868 "unreadable value = ordinary Error" fix at accountLockout.ts (~:92) would turn the lockout check from FAIL-CLOSED into FAIL-OPEN
(an unreadable Redis error today locks/refuses; the ordinary-Error path lets the login through uncounted).
If O85-P1 is raised at all: TIER 1 Opus gate whose headline question is exactly this, and the ordinary-Error outcome must be shown to be
fail-closed too, or the pass is RETIRED (moved to night/_spent_<date>/ with this note). The raise seat decides only after reading this note.
