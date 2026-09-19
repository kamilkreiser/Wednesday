# READY — KS-1260 (Ornith, briefed, bash_patch) — PASS 7/7 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1260-ornith35b-night/out.md.checker/section_N.diff`, each applied with its `section_N.diff.opts`** (section_1 = preflight.sh; section_2 = the NEW suite `Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh`).

**Held 10:01 2026-09-19 by the 06:0x Wednesday seat after a source read.** Tip `3c447abc7` (#1050 KS-1261 merged). Product `Blockchain/Dev/scripts/preflight/preflight.sh` (~:702-704): the early KS-1209 failure verdict keeps the `($n_ran/$TOTAL_LEGS legs ran)` ratio. **Scope = RATIO ONLY** (Wednesday's ruling: the ticket's own second option; the skipped-legs lines are NOT restored). **Refs KS-1260, linkKind contributes, never Closes.** Runtime (the pre-push gate every author runs: say so in the PR body) → stays In Progress on merge (§5f); tier 1 at the gate is reasonable for the pre-push gate.

## Source read (Wednesday)
- section_1 (product): 4/4 +/- lines IDENTICAL to the brief's; crossed control (KS-1261 brief) 0/4.
- section_2 (new suite): 77/77 line bodies present in the brief's fence; the control brief shares 51 (generic suite helpers), so for THIS section the compare discriminates only weakly. The checker's red-first (2 🔴 red at the tip by assertion) and green-after carry that section.
- Checker B1-B7: strict apply; 6 sibling preflight suites unchanged; shellcheck not installed (informational).
- #1057's T7 tamper (:699) sits OUTSIDE this hunk (the subagent's read, not re-derived by Wednesday).

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0
PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))
PASS B5a the script parses after the hunk (bash -n)
B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0
PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))
PASS B6 sibling suite(s) that drive preflight.sh: no NEW failure after (6 suite(s))
INFO B7 shellcheck not installed (informational)
clone restored (the new test quarantined to /private/tmp/claude-501/night/clone_ks1260/../quarantine/20260919-100017_bash, never deleted)
SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh red_first=yes apply_mode=strict
RESULT: PASS (7/7)
