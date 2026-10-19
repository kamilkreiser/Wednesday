# Gate brief: GATE T1 = #1607 (KS-1385 (b), the issuer-field freeze), Opus, tier 1, round 1 of 2

Commissioned by the Wednesday seat, 2026-10-19 after J 13th's READY FOR GATE of 03:29Z. Beside this brief: J13_DESIGN_0311Z.txt (the design Wednesday ruled as written) and J13_READY_0329Z.txt (the author's claims): both CLAIMS, not evidence. Routing v1.0 row G1: tier 1, an anchored-identity write path. Secuura only.
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project path: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files (READ ONLY: ls-remote, show, diff, cat-file; `git clone --shared` into YOUR scratch and work only there).

**METHOD:** gate P1's method and format (`0_Brain/reference/2026-10-19_gate-P1-pr1568-r4/GATE_BRIEF.md` and verdict.md): P1 booted anchoring against scratch PostgreSQL for #1568; do the same here.

develop = 9512cc70d8c4ad8a1214b17a39d7c48456feb531; #1607 head = c241bb8624bc5e0f49dfb85ec135997da0864c18 (both Wednesday ls-remote just before this brief).

**Kam's ruling being implemented** (card `secuura-ks1385-cert-holder-can-rewrite-issuer-fields-1018` = b, option text verbatim): *"A follow-up keeps issuerOrgId, orgDid, orgTrust and orgVerified as first anchored, and lets the holder change only the rest."* Option (c), letting the issuing organisation update certification rows, was NOT chosen.

## Named questions (each with its instrument, or "unmeasured")
1. **THE BOOTED SCENARIO (the reason for this gate):** with anchoring BOOTED on your scratch PG: (a) the issuer anchors a document with the four org fields; (b) the holder's organisation re-anchors with different org fields and a new actor; does verify serve the issuer's four fields with the holder's actor, and does the Cardano metadatum the submitter builds (transaction.ts:114 per J) carry the same? Controls: the issuer's own re-anchor still replaces the four (latest wins); a caller the guard refuses changes nothing; a holder event that OMITS the fields does not erase them; a row first anchored without them cannot gain them.
2. **No widening:** confirm who the guard admits is byte-identical to develop (the functions J lists), and that nothing implements option (c).
3. **Completeness of the write-path census:** J says exactly one statement changes metadata_payload after the first anchor (anchoring index.ts:1372, CASE :1426). Re-derive it across every service, scripts/, docker/, migrations/, deployment/. Name any writer J missed.
4. **The SQL merge:** `jsonb_set(EXCLUDED, '{secuura}', (EXCLUDED.secuura - $25) || (the $25 keys of the stored row))`: does it behave for a stored row with no `secuura` object, a JSON null, and a non-object value? Any path where it raises and the upsert fails for a legitimate holder?
5. **The 202 + one info line (no refusal):** is anything a caller relied on changed (status, body)? Does the existing "kept the stored anchor metadata" warning still fire only for real keeps?
6. **Mutants:** re-run J's 8 (or your own equivalents) and add at least one of your own aimed at the booted path.
7. **The beforeAll timeout** J saw twice early: does it appear in your runs? If yes, root-cause it.
8. **NOT tested:** name every suite of anchoring (and any service the PR touches) you did not run.
9. Predicted landing tree (J: a0d111da8b18 while develop is unmoved) and overlap with open #995 (index.ts:-505) and the R lane's PRs.

Verdict file: verdict.md in this folder; first line `VERDICT: ... at head c241bb8624bc...`; last line the sha256 of the file with its first and last lines removed. Scratch: your own t1/ under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c4419525-d2e2-49d0-8b3f-577263d823bb/scratchpad/. Findings only: no fixes, no GitHub or Linear writes, nothing under !CODING, no `cd`, no `rm`, no stderr to /dev/null, no Docker, no real Cardano network.
