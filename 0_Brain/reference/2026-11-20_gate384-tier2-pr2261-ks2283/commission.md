# Commission: QA GATE 384, TIER 2 (Opus), PR 2261 (KS-2283), 2026-11-20 ~04:4x AEDT (written by Wednesday, the 02:5x rotation-successor seat)

SHAPE: as /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-20_gate383-tier1-delta-pr2260-r2-ks1936/commission.md (read it WHOLE: method, hard limits, verdict format, line 1 = `PR 2261: <GO | GO WITH NOTES | NO GO> (at head <40-hex>; tier 2)`). Findings-only: you fix nothing. Write /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-20_gate384-tier2-pr2261-ks2283/verdict.md.

TIER 2, ON OPUS, AND WHY: a test-only follow-up (one file), but the cell it changes pins an AUTH gate (requirePlatformAdmin before the body parser on PATCH /api/admin/identity/users/:id/level), so model-routing 4c's G2 note puts it on an Opus gate.

THE CHANGE: PR 2261 (https://github.com/Secuura/Distributed_Secuura/pull/2261), head 6a71bf74c614686d268a186630a343b7649015f9, one commit on develop 2ad55ceceb7c71020ac0f18c2ba59a7064a5c26c, ONE file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1936-identity-level-route-is-platform-only.test.ts` (+6 -2, lines 108-113): the malformed-body cell's precondition keeps `status 400` for a platform admin and ADDS `expect(() => JSON.parse(platform.text)).toThrow()` (the parser's refusal is an HTML error page; the handler's own refusal is JSON BAD_REQUEST). Ticket KS-2283 (gate 383 F1). The builder's READY is saved beside this file as ready_w43.txt; its record is /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-20_seatW-43rd/ (evidence/matrix_*.json).

QUESTIONS (answer each with your own measurement, in your own clone or worktree under this folder's _work; never in another seat's tree):
Q1 Does the new cell fail under gate 383's G12 (lenient parser + the gate after it), under L1 (lenient parser alone) and under G12R (G12 + the handler's code renamed), and still pass on the PR head under NODE_ENV test AND production? Reproduce at least G12 and one of L1/G12R yourself; do not take the builder's matrix as the result.
Q2 Do M6 and M8 (gate 383's) still die by their own cells, and do the other 13 cells keep their meaning?
Q3 Can the new assertion go vacuous or false-fail in a way the builder did not name (e.g. an empty body, a non-HTML non-JSON reply, Express config, body-parser upgrade)? Measure what you can; say UNMEASURED for the rest.
Q4 The api-gateway suite whole on the merged state (develop + PR) with failure-name sets compared to develop; tsc; the test-type ratchet.
Q5 The PR body and the KS-2283 facts comment (id 5847a0bb): does any factual sentence not hold? The Linear attachment of PR 2261 to KS-1936 (Linear automation; KS-1936's state unchanged): note only.

HARD LIMITS: read-only on GitHub and Linear (no comment, no review, no label, no merge); no write in any !CODING path (your own clone under _work); no database, no container, no box; no mail, no send tool, no launch; no cd; no rm (move to _work/_quarantine); never kill a process by name; /usr/bin/grep -i with a positive control beside every zero.
RETURN: verdict line 1, then a 10-line summary (findings by severity, what you ran, what you did not).
