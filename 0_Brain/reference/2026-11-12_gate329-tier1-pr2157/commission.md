# Gate 329, TIER 1 (Opus; routing v1.0 tier-1 row: a live behaviour change at the document-create door of the api-gateway). PR 2157 (KS-1952), round 2 after gate 301's GO WITH NOTES (2026-11-10): Seat R 106th's fix round for gate 325's finding G325-2204-1. Commissioned 2026-11-12 ~14:3x AEDT by the 12:3x Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate325-tier1-pr2204/commission.md` (read it whole: its Constraints, output shape and controls all apply) and calibration from gate 325's verdict.md (its G325-2204-1 finding, lines 256 to 263, is what this round answers) and gate 301's verdict `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-10_gate301/verdict.md` (PR 2157's round 1; its G301-2157-1..-3 notes).

Pins (Wednesday's `git ls-remote origin` 14:34:30 AEDT; RE-READ at start and end, and say if either moved): develop b7137aa97c79221730804ad208a8d080743ace5a; refs/pull/2157/head 2c0692100527329a6c1d262b58fc2fd51740e4ac. THE HEAD IS A MERGE COMMIT (parents 424bcfb752c8 = the fix commit, and develop b7137aa97c79), granted by Wednesday so the pushed tree passes the audit gate on today's baseline; it claims to change nothing beyond develop + the fix. Compute the PR's diff against develop yourself (expect 3 files: routes/verification.ts and the ks1952 + ks466 tests, +143 -1 by the seat).

READY (read whole; reproduce, do not trust): `ready_r106_ks1952_mail.txt` in THIS folder.

THE RULING this round executes (Wednesday's G325-2204-1, inside Kam's two rulings KS-1952 and KS-1466): "whichever of 2157 / 2204 merges SECOND carries a follow-up that applies 2157's 503 to EVERY create, typed or untyped." PR 2204 merged FIRST (b7137aa97c79).

Questions:
1. **The merge commit is honest:** the tree of `2c0692100527` equals (develop b7137aa97c79 + the fix commit's changes) exactly; the merge commit's own diff against its first parent contains only develop's changes; nothing else rode in. Show the instruments.
2. **The guard:** `routes/verification.ts` now refuses EVERY POST /api/documents with 503 SERVICE_UNAVAILABLE while `redisService.isRedisAvailable()` is false: typed, untyped, empty-string type, falsy non-string type, truthy non-string type. Is anything that should NOT be refused now refused (other routes, a non-create on the same router, a health path)? Where exactly does the guard sit relative to auth, body parsing and enforcement: can an unauthenticated caller now learn Redis state from a 503 where it got a 401 before? (Answer from the code; if it is a change, grade it.)
3. **Cells:** C2 inverted and the two new cells RED against 2157's previous guard (reproduce the seat's 3 failed of 7), GREEN at the head; C1 and C3 (Redis up) unchanged; one mutant of your own (e.g. the guard reading only `body.documentType`) killed.
4. **With 2204 merged:** on the PR's merge tree with develop, run ks1952, ks466, enforcement, ks501, ks1466, ks1203 and the whole api-gateway vitest suite (prove it whole); does the G325-2204-1 hole close (an untyped create during an outage no longer reaches enforcement unchecked)? Write the cell that would have caught it if none does.
5. **Gate 301's notes:** do G301-2157-1..-3 and its body's '## Gate 301 notes' section still read true at the new head? Does the PR body now carry a 'Fix round (G325-2204-1)' section that is accurate?
6. **Census + typecheck:** open PRs on the 3 paths (with a control); `tsc --noEmit` on api-gateway; the test-type-check ratchet for api-gateway (the seat: 25 errors, 25 baselined, 0 new).
7. **Live-behaviour statement for the GO:** state in one paragraph exactly what changes for a caller during a Redis outage after this merges, so Wednesday's GO can name it. Nothing deploys from a merge.

Spark: the test-digest STANDARD on your whole-suite log (raw kept), then the Spark shadow review with `--pr-body-file`, one request at a time; record recall/false positives.

OUTPUT: `verdict.md` in THIS folder. First line: 'PR 2157: GO / GO WITH NOTES / NO GO (at head 2c0692100527; tier 1; round 2)'. Findings G329-2157-N, graded. NOT TESTED. The Spark result. If your Write is refused, return the text in full.

Constraints: exactly gate 325's. Read-only on the project checkout (clone into `scratch/` in THIS folder for any write verb; installs only there, `--ignore-scripts`). Every npm/npx/vitest/tsc call names its directory explicitly and never runs from the WEDNESDAY working directory. No push, no comment, no ticket write, no merge, no mail. If DevMASTER drops, wait, re-read what you wrote, then resume.
