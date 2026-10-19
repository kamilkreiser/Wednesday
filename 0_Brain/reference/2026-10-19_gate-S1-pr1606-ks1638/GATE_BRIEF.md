# Gate brief: GATE S1 = #1606 (KS-1638), Opus, tier 1, round 1 of 2

Commissioned by the Wednesday seat, 2026-10-19 after R 51st's mail of 03:14Z (copied beside this brief: R51_MERGED_0314Z.txt; its KS-1638 section is the author's claim, NOT evidence). Routing v1.0 row G1: tier 1 because it changes the push-time security gate (the pre-push hook's preflight) that every Secuura push runs through. Secuura only.
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project path: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files (READ ONLY there: ls-remote, show, diff, cat-file; clone `--shared` into YOUR scratch and work only there).

**METHOD:** gate O1's method (`0_Brain/reference/2026-10-19_gate-O1-tier1-five/GATE_BRIEF.md` and its verdict.md): read them for method, controls, verdict format and hard limits.

develop = 9512cc70d8c4ad8a1214b17a39d7c48456feb531 (tree 34ea098a022c, verified by Wednesday). #1606 head = 04efb8107ab2f90e815f562ea3b169ea1a70d7eb (Wednesday ls-remote). Files (Wednesday's diff --stat in its own clone): `Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh` (+6/-2), `Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh` (+49/-1), `Blockchain/Dev/scripts/preflight/preflight.sh` (+33).

## The defect it fixes (KS-1638)
With `ALLOW_FORCE=1` (the hook's documented opt-in for a deliberate non-fast-forward push, `.githooks/pre-push:46, :76-82`), the in-hook preflight's leg 14 inherited the variable, so ks998's SC12 ("without ALLOW_FORCE the rewrite is refused") went red and the documented path could never pass its own preflight.

## Named questions (each with its instrument, or "unmeasured")
1. **Is this a weakening?** Half 1 changes SC12's "without" push to `env -u ALLOW_FORCE git push`. Show SC12 still FAILS if the hook stops refusing a non-fast-forward without the flag (plant that regression in the hook, expect SC12 red, restore).
2. **The derived strip list (half 2):** leg 14 strips every ALL-CAPS name the hook reads with an external default (`${NAME:-...}`). (a) Measure the derived set on the real hook (R: ALLOW_FORCE only). (b) Can the derivation ever strip a variable the suites NEED (e.g. a name the hook reads with a default that a suite also sets deliberately)? (c) Plant a NEW `${FOO:-x}` read in a copy of the hook and confirm it appears in the strip list; plant a plain assignment and confirm it does not. (d) On failure the leg "withholds the run": confirm that is a FAIL, not a silent skip.
3. **R's census:** 72 shell suites, 8 push, exactly one (ks998) drives a non-fast-forward push. Re-derive it.
4. **The end-to-end case the ticket is about:** in a scratch repo wired with the real hook, an `ALLOW_FORCE=1` non-fast-forward push now passes the preflight, and the same push without the flag is refused. Both directions.
5. **The fixture change** (leg-14 fixture now writes a hook stub, plus a `nocontrol` variant): does it still test what it tested before? Name any cell whose meaning changed.
6. **Test Evidence:** run the full shell-suite set yourself (R: 91 passed, 0 failed, 0 skipped) and name every suite you did not run.
7. Predicted landing tree onto develop (merge-tree), and overlap with open #1597.

Verdict file: verdict.md in this folder; first line `VERDICT: ... at head 04efb8107ab2...`; last line the sha256 of the file with its first and last lines removed. Scratch: your own s1/ under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c4419525-d2e2-49d0-8b3f-577263d823bb/scratchpad/. Findings only: no fixes, no GitHub or Linear writes, nothing under !CODING, no `cd`, no `rm`, no stderr to /dev/null, no push to any real remote.
