# Gate 271, tier 2 BATCH, round 1 of 2 each: PR 2103 (KS-2107), PR 2104 (KS-1972), PR 2105 (KS-1974), PR 2106 (KS-2117). Staged 2026-11-09 by the 05:3x Wednesday seat; LAUNCHED 06:0x with these four (KS-2121 not READY; T 17th wrapping). SUPERSEDES the single-PR commission in ../2026-11-09_gate271-tier2-pr2103-ks2107/commission.md (never launched).

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at TIER 2 depth (through code: diff read, words true, cells re-run with a planted defect of your own). Stop line, PER PR: any byte that changes behaviour beyond what the READY states, or any security decision = NEEDS TIER 1 for that PR, stop on it, carry on with the others.

Pins (Wednesday's ls-remote 06:01:10; RE-READ at start and end, and in the verdict say whether each moved):
- develop 6c9a593df4abf746db612946a87839111ec5b7a9 (PR 2068). The three commits were cut from 15dca468b86f; develop has moved by one PR since: each PR's merge tree on 6c9a593df4ab is part of the question.
- PR 2103 head 6de27bab34cdea1a29e6030497675d4e27709537 (Seat T 17th, KS-2107)
- PR 2104 head df9493550372e4292c08b9129001abf340b76304 (Seat G 30th, KS-1972)
- PR 2105 head 5f1685420cc671269999a883ff34c47dc8a0c201 (Seat G 30th, KS-1974, identus-client part only)
- PR 2106 head a8d19bf3918ebe7571bf756fbdeb8cc43e2631de (Seat T 17th, KS-2117; README +4/-1 and transfers.ts docstrings +3/-3 plus the docs pair; the seat says no code byte)

READY claims (untested by Wednesday; read each whole):
- PR 2103: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-17th/evidence/d1/mail/ready_ks2107_body.txt
- PR 2104: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatG-30th/mail/out_06_ready_row1.txt
- PR 2105: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatG-30th/mail/out_08_ready_row2.txt
- PR 2106: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-17th/evidence/d2/mail/ready_ks2117_body.txt
All four originate from held Spark passes (operators 106/107, READY_* files in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/); the cheat + flow fragment pair on each is a Wednesday ruling beyond the READY.

Questions, per PR:
1. Does the diff do only what the READY says? PR 2103: every changed line in documents.ts a comment (prove by strip-and-compare of emitted JS, with a control that fails on a planted code byte). PR 2104: the event-indexer +9 change and its 5 cells. PR 2105: one catch expression in packages/shared/src/prism/identus-client.ts resolveDID; didResolutionMetadata.errorMessage always a string, didDocument null, error notFound unchanged. PR 2106: README and transfers.ts docstrings only (strip-and-compare emitted JS like 2103); is the README's API-key example and the 'accept' action type true against the SDK source?
2. Are the new comments, test names and the fragments TRUE about the code at the head (quote the lines)? An overstatement is a finding.
3. Red-first: re-run each new test file on develop (product reverted) and at the head; plant a mutant of your own (not the seat's) and show a cell fails by assertion; restore by sha.
4. The seats report pre-existing reds (PR 2105: verifyMessageSignature CIP-8/CIP-30 in packages/shared, 1 red on develop and head). Confirm SAME red set before and after; a new red is a finding.
5. Docs-fragments check passes with each pair and fails on a planted defect.
6. PR bodies and ticket comments (2103: 0bb70934 on KS-2107; 2105: 0d041cef on KS-1974; 2106: d90aa502 on KS-2117; 2104: the seat names its own): true at the head. PR 2105 says it NARROWS KS-1974 to its identus-client part: check the body says so plainly.
7. Merge tree of each PR on develop 6c9a593df4ab; the four are file-disjoint by the seats' censuses: verify pairwise with a planted overlap control; and list open PRs sharing any path.

Constraints: clone on the boot volume /private/tmp/g271 (QA no-rm; name its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; load1 under 8; STOP if DevMASTER free space falls under 10 GiB (df at start and end).

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate271-tier2-batch/verdict.md. Line 1 exactly: 'PR 2103: <V>; PR 2104: <V>; PR 2105: <V>; PR 2106: <V>' with V one of GO | GO WITH NOTES | NO GO | NEEDS TIER 1 (append any added PRs in the same form). Then per the common rules: per PR, FOUND / TESTED / HOW (instrument, controls), NOT TESTED, findings with ids G271-<PR>-<n>. Findings only; post nothing; mail nothing.
