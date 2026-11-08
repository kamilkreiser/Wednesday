# Gate 273, TIER 1 BATCH (Opus): PR 2107 (KS-1971), PR 2108 (KS-1973), PR 2109 (KS-2110), PR 2104 round 2 of 2 (KS-1972). All four by Seat G 30th, all in packages/shared or its tests. Commissioned 2026-11-09 07:3x by the 06:3x Wednesday seat.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at FULL tier-1 depth (security surfaces: an SSRF guard, a credential verifier, a role gate's pins, an indexer's error path). Stop line, PER PR: any byte that changes behaviour beyond what the READY states = a finding (Major or above), carry on with the others.

Pins (Wednesday's ls-remote 07:30:59; RE-READ at start and end, and in the verdict say whether each moved):
- develop 93028c8151ecdd173c341fb7c23a4b89e381cc04 (PR 2078)
- PR 2107 head 987ee2de56e0b9f5e80ad76a6c79d8e909579cc5 (KS-1971, ssrf-guard)
- PR 2108 head 6785129097618efbfc9d74336cd33e53fba4d1c7 (KS-1973, packages/shared/src/vc/verifier.ts)
- PR 2109 head 5350041b426d3e3ee42d5bd812a17b07a2718c3d (KS-2110, test-only pins in packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts)
- PR 2104 head e7faa4f72c4e9a2d1b6e0364fa321acb215b9e6c (KS-1972 round 2: revert of df9493550372 + site-1-only change in event-indexer.ts poll()'s catch)
Each was cut from an OLDER develop (15dca468b86f or 6c9a593df4ab): each PR's merge tree on 93028c8151ec is part of the question.

READY claims (untested by Wednesday; read each whole), in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatG-30th/mail/ :
- PR 2107: out_11_ready_row3.txt
- PR 2108: out_14_ready_row4.txt (carries a verify() caller list; G read neither the handler's catch nor the default resolver)
- PR 2109: out_16_ready_row5.txt
- PR 2104 r2: out_17_ready_ks1972_round2.txt. Round 1 was gate 271: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate271-tier2-batch/verdict.md (its PR 2104 section: NEEDS TIER 1; Wednesday RULED keep only site 1, sites 2/3 byte-equal to develop). This is round 2 of 2 under the cap.
The fixes originate from held Spark passes (operators 107/109, READY_* in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/); the cheat + flow fragment pair on each product PR is a Wednesday ruling beyond the READY.

Questions, per PR:
1. Does the diff do ONLY what the READY says? Read every changed line.
2. PR 2107 (ssrf-guard): enumerate EVERY caller of the changed guard (git grep -w over tracked files, with a control that finds the definition) and say for each whether the change can make it MORE permissive. A guard that now answers 'valid:false' / 'not blocked' where it used to throw is the shape to test.
3. PR 2108 (vc verifier): where a hostile resolver value used to make verify() REJECT it now RETURNS valid:false. Read the two production callers (services/vc-issuer routes/credentials.ts ~374 and routes/presentations.ts ~330) INCLUDING their handlers' catch paths and the verifier's DEFAULT resolver, which G did not read: can valid:false ever be treated as success anywhere a throw used to stop it? The class is exported publicly: say what that means for unknown consumers.
4. PR 2109: are the pins M4 and G5b TRUE pins of develop (green on develop by design) and do they go red under a plant of YOUR OWN (not G's two)? Note G5b reads a route file as text: say what it would miss.
5. PR 2104 r2: event-indexer.ts poll()'s catch only; isRateLimited unchanged; processBlock (~:223) and processTransaction (~:326) byte-equal to develop. Does a thrown value poll() cannot read now reach handleError, and is there any path where a REAL rate limit is now treated as not one? Cell C3 pins site 2; plant your own mutant.
6. Red-first for every new test file: re-run on develop (product reverted) and at the head; plant a mutant of your own per product PR and show a cell fails by assertion; restore by sha. Confirm the SAME pre-existing red set in packages/shared (the seats report 1 red: verifyMessageSignature CIP-8/CIP-30) before and after; a new red is a finding.
7. Comments, test names, fragments, PR bodies and the ticket comments named in the READYs: TRUE at the head (quote lines). An overstatement is a finding.
8. Merge tree of each PR on develop 93028c8151ec; the four are file-disjoint by G's censuses: verify pairwise with a planted overlap control; list open PRs sharing any path.

Constraints: clone on the boot volume /private/tmp/g273 (QA no-rm; name its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; load1 under 8; STOP if DevMASTER free space falls under 8 GiB (df at start and end; it read 9.99 GiB at 07:2x).

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate273-tier1-g30-batch/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2107: <V>; PR 2108: <V>; PR 2109: <V>; PR 2104: <V>' with V one of GO | GO WITH NOTES | NO GO. PR 2104 is round 2 of 2: a NO GO there ships nothing new and its residue is ticketed, so say per finding whether it is closed, residue or new. Then per PR: FOUND / TESTED / HOW (instrument, controls), NOT TESTED, findings with ids G273-<PR>-<n> and a severity. Findings only; post nothing; mail nothing.
