# Gate 281, TIER 1 BATCH (Opus): PR 2121 (KS-2131, round 1) and PR 2118 (KS-2127, ROUND 2 OF 2, a narrow compare on the delta). Both by Seat R 90th. Commissioned 2026-11-09 13:4x by the 11:4x Wednesday seat. One session for both, under the 09-18 minimise-gate-duplication rule.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at FULL tier-1 depth for PR 2121; for PR 2118, the delta only (round 1 is settled by gate 278).

Pins (Wednesday's ls-remote at 13:49:23 AEDT; RE-READ at start and end, and say whether each moved):
- develop 4d6b7bb17fd3be7b3fde8a3babc5d59c91c959b8 (PR 2110 squash)
- PR 2121 head 5ea632ca569c40af9685b85845273b3a13b470a9 (KS-2131: ks570-proxy-mount-auth.test.ts +96/-1 and two fragments; test-only; READY /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatR-90th/mail/ready_ks2131_r90.md)
- PR 2118 head cd8b80e38a4bfedbfb04cd3bdcddf93b10ffa074 (KS-2127 round 2: one new commit on round 1's 08cf86d0ec5f; delta: .githooks/pre-push +5, suite +56/-1, both fragments rewritten; READY .../mail/ready_ks2127_r2_r90.md). Round 1 verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate278-tier1-pr2118-ks2127/verdict.md. The ruling for this round: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_R90_answer_gate278_fixround.md.

PR 2121, questions:
1. Is it test-only (no product byte)? Does each new cell boot the REAL app in-process and refuse a credential-less GET on /api/billing/bundles, /api/nft/certificates and /api/certifications with 401 and 0 upstream hits? Is the sk_ key control admitted and forwarded?
2. The seat's stated DEVIATION: with the gate `if (!hasBearer && !hasApiKey)` turned off, the certifications cell stays green because that mount's requireScope also refuses with an identical 401. Verify by your own mutants: gate off alone; gate off plus requireScope off that mount; requireScope off alone. Is the cell title for certifications true?
3. The seat's whole-suite measurement (9 red, none on billing, nft or certifications, with the gate off at 2a031f51403f) is the case FOR the PR: reproduce it at develop 4d6b7bb17fd3.
4. The fragments: true, and the docs-fragments check ends OK.

PR 2118 round 2, questions (the DELTA only):
5. G278-1: does a non-HEAD push under a failing diff now show the KS-2127 cause in its refusal (banner or git's error)? Does the new cell assert rc != 0 and KS-2127 in the output? Is the refusal still FAIL-CLOSED (not loosened)?
6. G278-2: are both fragments now true about tag pushes (they used to pass silently; they now run the preflight if HEAD, and are refused otherwise)? Check the PR body and comment 8d3c3eff too if they repeated the old sentence.
7. G278-3: does a new cell fail when st_all is not 1 (gate 278's mutant M3)?
8. No regression: the 9 hook suites and the push-shape probe (gate 278's /private/tmp/g278/probe/shapes.sh may be reused, read it first) give the same verdicts as round 1 in a healthy repo.

Both:
9. Merge tree of each head on develop 4d6b7bb17fd3 (rc and tree), and of the two together. Do they share any path? Open PRs sharing their paths, with a planted control.

Constraints: clone on the boot volume /private/tmp/g281 (no rm; state its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; never push; never run the hook against the real remote; keep load1 under 8 (do NOT stress the machine on purpose); df DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate281-tier1-pr2121-pr2118r2/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2121: <V>; PR 2118: <V>' with V one of GO | GO WITH NOTES | NO GO. PR 2118 is at the two-NO-GO cap: a NO GO there means the closed instances ship and the residue is ticketed, so give each finding a severity and say which round-1 note it closes. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, and findings with ids G281-<PR>-<n>. Findings only; post nothing; mail nothing.
