# Commission: QA GATE 351, TIER 1, on PR 2228 (KS-1699: originate POST /:id/verify gets the KS-1695 reader check), Secuura/Blockchain, 2026-11-13 13:57:24 AEDT

Commissioned by Wednesday (the 11:5x seat). Model: OPUS (routing v1.0: tier-1 gates = Opus; an authorisation decision on a route that bills). Usage 98%, a guide per Kam 2026-10-22: a gate needs a clone and runs; no local tier can run one. Findings only: nothing fixed, posted, mailed, pushed, merged or written to Linear or GitHub. Work only in `scratch/` of THIS folder; write `verdict.md` here. Never write inside `/Volumes/DevMASTER/!CODING/` (read verbs only there); GitHub reads with GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config" (confirm `gh auth status` = kksecura); repo Secuura/Distributed_Secuura. No `cd`; zsh has no PIPESTATUS; never delete; bound every listing with `| head -N`. Linear comments: `first:50`, sorted client-side (never `last:N`).

## Copy-and-change
Template: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_gate348-tier1-pr2224-2225/commission.md` and its `verdict.md` (read WHOLE: method, scratch-clone rules, red-proof requirements, verdict format; gate 348 gated the sibling R 117th rows on the same originate surface).

## The subject (pins by Wednesday's ls-remote at 13:57:24, in `pins.out` here; re-pin before the first measurement and before the verdict)
- develop 49e4d6a4d0074883dd76372abc54bf0bfb09e6d5.
- PR 2228, KS-1699, head 4383051cafcf7c4535ab74eaa82a850be8efd780, ONE commit on develop: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+13 -0: a reader guard after the not-found block and before the charge write; a refused caller gets the route's own 404 with the SAME bytes as not-found and NO charge event), a new jest file `.../originate/src/__tests__/ks1699-certification-verify-needs-issuer-holder-or-admin.test.ts` (23 cells), and a flow + cheat docs fragment pair.
- The builder's READY (Seat R 118th) is the claim under test: `r118_ready.txt` in THIS folder (read whole). Its record: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/` (the seat R 118th folder, HANDOVER first).
- Open PR 2160 (head b02bd2716cc2) also edits certifications.ts: the builder pushed under a named grant ignoring that overlap.

## The questions (tier 1)
1. **The guard, at source:** read the whole verify route at the head. Who may verify after this change (the builder says: platform admin, issuer, holder, issuing connector)? Does it reuse the KS-1695 reader-check helper exactly (the guard's definition and its other call sites), or a copy? Is the refused response byte-identical to not-found (cloaked), and does NO charge event or other write happen before the refusal (order of operations, read the lines)?
2. **CONSUMERS, THE QUESTION THAT DECIDES THE TIER-1 VERDICT:** enumerate every caller of POST /:id/verify in the repo (gateway routes and proxy, frontend apps (the builder named frontend/issuer api.ts:481, not measured), e2e specs (it named verifier-exhaustive.prelaunch.spec.ts:298, which passes no token), other services, SDK/clients). For each: does it send a principal the new guard admits? Name any legitimate caller this change would now refuse (a verifier who is none of the four, an unauthenticated public verify flow). Read, with a positive control for the search.
3. **Red-proof, reproduced YOURSELF:** the 23 cells green at the head; the guard removed -> the expected reds; your OWN independent mutants (guard after the charge write; a wrong principal field; the cloak bytes changed) each caught. A cell that cannot go red is a finding.
4. **Whole originate suite** at develop and at the merge (the builder measured A/B only at the OLD base 49781230da49): same ratio plus the new cells; `tsc` as the repo runs it.
5. **The 2160 overlap:** merge-tree of the head against PR 2160's head b02bd2716cc2, both orders, with a planted-conflict control; does the combined file keep BOTH changes' semantics (read the merged region)?
6. **Scope:** KS-1699's scope sentence vs this PR (it selects /:id/verify ONLY; share and recertify are named open questions for Kam): say whether the body and ticket comment state the narrowing honestly. The PR is ALSO attached to KS-1695 (the builder's finding: the branch name carries 'ks-1695'): confirm and say whether it changes anything on KS-1695.
7. Body: Test Evidence present; PREFLIGHT line quoted ('13/16 legs ran, 3 SKIPPED'); no self-hold sentence; the title starts `Refs KS-1699:`; docs fragments present and accurate.

Verdict format: line 1 `PR 2228: <GO | GO WITH NOTES | NO GO> (at head <full sha>; tier 1)`, then FOUND / TESTED / HOW / NOT TESTED; findings numbered G351-2228-N. A NO GO names the exact fix.

Return a 10-line summary.
