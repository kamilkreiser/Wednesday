# Gate 258, tier 1 COMPARE: PR 2066 (KS-2032) squashed onto develop cfb6c1573ba9 (PR 2060, KS-1536 3a, merged). Launched 2026-11-08 by the 21:2x Wednesday seat

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. Corrections: develop cfb6c1573ba9c948ebbe898fb2aec283bb9954ab by Wednesday's ls-remote at 22:24 AEDT; QA no-rm (leave your clone at /private/tmp/g258, name its size); one clone; stop under 12 GiB free on DevMASTER; load1 under 8; never cd; if a hook refuses merge-tree, run it in a clone under the session scratchpad and say so.

This is NOT a re-gate of PR 2066 (gate 245 GO WITH NOTES at head baf577c78e7f876551e132e407d0982232622de9: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate245-tier1-y-auth/verdict.md). It answers ONE question B 98th raised in its READY of 11:22Z: two PRs changed the same security files, Blockchain/Dev/services/*/keyRevokePolicy.ts (find its path) and docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md; git merges them clean, and NOBODY has run the two changes together.

Build the union: squash PR 2066's head onto develop cfb6c1573ba9 in your clone (expected tree c2940eebfc6db7c11eb39aac6e32df9d0d2cc00d by B 98th's computation; confirm it).
1. On that tree, run the suites that exercise keyRevokePolicy.ts and isPlatformRole: the KS-2032 cells PR 2066 added, the KS-1536 cells PR 2060 added (guard G1/G2 in packages/shared, auth ks1536, gateway ks1536), and any existing suite that imports keyRevokePolicy (enumerate the importers; do not sample). Each suite with a control that can fail (plant one defect per suite, restore by sha256).
2. Read the union of keyRevokePolicy.ts: does each PR's intent survive the other's? Name any line where 2066's rule and 2060's shared predicate disagree about the same principal or role.
3. tsc for the touched packages on the union.
4. The inventory doc: both PRs' rows present and not contradicting each other.

Verdict line 1: COMBINATION OK, COMBINATION OK WITH NOTES, or COMBINATION BROKEN, with the failing cell. Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_gate258-compare-pr2066-on-2060/verdict.md. Findings only; post nothing.
