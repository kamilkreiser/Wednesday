# Gate 278, TIER 1 (Opus): PR 2118 (KS-2127), the pre-push hook itself. Built by Seat R 90th. Commissioned 2026-11-09 12:3x by the 11:4x Wednesday seat.

Why tier 1: the change edits .githooks/pre-push, the gate every push in this repo passes through. A defect here can let a failing push through for everyone (the bug it fixes), or block every push.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at FULL tier-1 depth.

Pins (Wednesday's ls-remote 12:3x through the project remote; RE-READ at start and end, and say in the verdict whether each moved):
- develop b9fd80eee85b791dfd0e532d23d8f0da9b4f80ea (PR 2104 squash)
- PR 2118 head 08cf86d0ec5fde3e1d465f9729ce861d270dc534 (branch feature/ks-2127-pre-push-hook-a-failing-git-diff-reads-as-no; one commit cut on 273de443c30c; 4 files +246/-3: .githooks/pre-push +21/-3, new suite Blockchain/Dev/scripts/__tests__/ks2127_pre_push_failing_diff.test.sh (path as the PR files API gives it), two docs fragments)

READY claims (untested by Wednesday; read whole): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatR-90th/mail/ready_ks2127_r90.md . Ticket comment 8d3c3eff on KS-2127.

Questions:
1. Does the diff do ONLY what the READY says? Read every changed hook line. The fix: the three diff sites (lines 129, 143, 252 at develop) now read the diff's exit status instead of `|| true`; the new helper _jr_diff_failed sets a KS-2127 banner, an unconditional changed marker and st_all=1. Is that the right fail-safe direction (a failing diff now forces the preflight rather than skipping it)? Is there any path where the new code REFUSES a legitimate push that develop's hook allows (a clean new-branch push, a fast-forward, a push with no changes, a tag push, a delete push)? Enumerate the legitimate push shapes and put each through the fixed hook (see the 2026-09-11 red-proof-arms lesson: a CLEAN arm for every legitimate shape).
2. Red-proof, independently: run the new suite against develop's hook (expect the 5 fault cells red, 3 controls green) and against the head's hook (8 of 8). Use your own mutant of the fix (not R's tampers) and show it reddens a cell.
3. The 9 existing hook suites R names (pre_push_hook_base, pre_push_hook_base_fixture_guard, pre_push_hook_current_develop, ks998_pre_push_judges_the_push, ks998_pre_push_stale_base_hint, ks884_pre_push_tag_named_develop, pre_push_stack_legs_comment, preflight_deps, preflight_gateway_slot): same tallies on develop's hook and the head's hook. Also leg 12 --check-unreached.
4. POSIX: `sh -n` and `dash -n` (if dash is present) on the head's hook. Note: /bin/sh here is bash 3.2.
5. The fragments: true, and `node Blockchain/Dev/scripts/docs-fragments.mjs check` ends OK.
6. Merge tree of the head on develop b9fd80eee85b (rc and tree); list open PRs sharing any path, with a planted-overlap control.
7. R's NOT COVERED list (other failing-diff shapes; dash parsed only; a tag push whose diff fails now runs the preflight with no cell): say whether any of these is a finding and its severity.

Constraints: clone on the boot volume /private/tmp/g278 (no rm; state its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; never push; load1 under 8; DevMASTER read about 107 GiB free at 12:3x. Do not run the hook against the real remote.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate278-tier1-pr2118-ks2127/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2118: <V>' with V one of GO | GO WITH NOTES | NO GO. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, and findings with ids G278-<n> and a severity. Findings only; post nothing; mail nothing.
