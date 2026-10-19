# Gate brief: GATE U1 = #1607 round 2 DELTA (KS-1385 (b)), Opus, tier 1, round 2 of 2 (the last under the cap)

Commissioned by the Wednesday seat after J 13th's READY FOR DELTA GATE of 04:15Z (beside this brief: J13_READY_R2_0415Z.txt, a CLAIM). Secuura only.
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project path: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files (READ ONLY: ls-remote, show, diff, cat-file; `git clone --shared` into YOUR scratch and work only there).

**Round 1 context:** gate T1's brief and verdict: `0_Brain/reference/2026-10-19_gate-T1-pr1607-ks1385b/` (GO WITH NOTE at c241bb8624bc; MIN-1 odd stored shapes raise 22023, refused callers 500 via RETURNING; MIN-2 log split pinned by source only). Re-use T1's probes and its booted harness where they are in the scratchpad (`.../scratchpad/t1/`), read-only, or rebuild them in yours.

develop = ce98606212e4 (moved: R's #1606 / KS-1638, pre-push hook + leg-14 cells, 3 files); #1607 head = 243d324d4dd7e9ac5e277b2ac0b8566f54d32a30 (Wednesday ls-remote just before this brief; re-read both, full shas).

## Questions (each with its instrument, or "unmeasured")
1. **Delta scope:** `git diff --stat c241bb8624bc 243d324d4dd7`: exactly T1's two Minors (J: 3 files, +130/-12)? Anything else changed?
2. **MIN-1 closed?** Re-run T1's own MIN-1 probe on the new head for every stored shape (secuura JSON null / string / array / number / absent; payload SQL NULL / JSON null / string / number / array), for an ADMITTED holder and a REFUSED caller, booted. Expect: no error; refused caller = develop's behaviour byte for byte; admitted holder = rest applied, issuer fields absent.
3. **MIN-2 closed?** Re-run T1's mutant (`heldIssuerFields` forced false) on the new head: does a COMMITTED cell now red? Is `classifyPersistOutcome` exercised on real rows from the real statement?
4. **Round 1's booted scenario still YES** on the new head (one pass of T1's booted holder re-anchor + its four controls).
5. `allow` still byte-identical to develop; nothing implements option (c).
6. **Landing on the moved develop:** merge-tree onto ce98606212e4 (J: 5adb4e513696). Because develop's delta touches `.githooks` and `scripts/`, run the shell-suite set on that predicted tree (91 expected) as well as anchoring's suites.
7. NOT tested, by name.

Verdict file: verdict.md in this folder; first line `VERDICT: ... at head 243d324d4dd7...`; last line the sha256 of the file with its first and last lines removed. Scratch: your own u1/ under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c4419525-d2e2-49d0-8b3f-577263d823bb/scratchpad/. Findings only: no fixes, no GitHub or Linear writes, nothing under !CODING, no `cd`, no `rm`, no stderr to /dev/null, no Docker, no real network beyond ls-remote/fetch into your own clone.
