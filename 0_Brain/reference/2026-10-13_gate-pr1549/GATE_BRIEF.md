# Gate brief: pull request 1549 (KS-1385, anchors carry the latest event's identity), Opus tier 1 (identity and attribution on anchored records)

Commissioned by the Wednesday seat. 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

## The rulings this implements
- Kam, card secuura-ks1385-anchor-identity-needs-ps895-ruling-1013, ruled b at 18:52:53 AEDT, verbatim: "Latest event's identity wins".
- Wednesday's site ruling to the author (08:48:09Z): forward Platform S's identity block at SIX of the seven anchor-emitting sites; site 5 (POST /api/anchoring/submit, anchors.ts) stays OUT. anchor_store upsert gains metadata_payload = EXCLUDED.metadata_payload; content_hash stays out (unruled).

## What you are gating
- Head aca6efb0864b11360eca90d1217d72ccd24e10ac (Wednesday's own ls-remote of refs/pull/1549/head = the author's). Branch cut from 026c2d16; develop is now d53d80cbb2d50a5525c3d881a2da7a31eba67fb5 (Wednesday's ls-remote). 12 files.
- Author's claims (NOT evidence): one helper, utils/anchorIdentity.ts, forwards S's top-level `identity` block verbatim (not re-validated: identitySchema is the authority) at sites 1, 2, 3 (emitLifecycleAnchor and its four call sites), 4, 6, 7. Site 5 is excluded with the reason in place. The upsert goes from 12 to 13 columns. The PR body and the ticket say documentType and signatureHash are overwritten by the latest event too. Reused cells C1-C7, C9, C10; C8 inverted to a behavioural cell with C8b as its control. New anchoring integration lane plus an exclude on the default lane, proven with a planted always-red control. 14/14 mutants killed by name. Predicted merge tree on d53d80cb: 55252322; originate 109 suites / 1361 tests; anchoring integration 4/4; tsc clean. One pre-existing anchoring red: threadTokenMint.test.ts:71.
- THE AUTHOR'S OWN POINTERS, to attack first: (1) the certifications cells mock six modules: does the mock set hide an early return so site 6/7 cells pass vacuously? (2) the upsert cell runs SQL EXTRACTED from index.ts rather than dbPersistAnchor, so it pins the statement, not the call site; (3) the include/exclude globs of the new anchoring lane; (4) UNSURVEYED consumers of metadata_payload that might assume write-once. Survey them yourself: every reader in every service, and what an overwritten documentType/signatureHash does to each.

## Gate
1. Diff develop..head by file; classify every hunk; nothing outside the 12 files.
2. Enumerate EVERY site in originate (and anywhere else) that POSTs to anchoring's /api/anchors (do not sample). Confirm exactly six forward through the helper, site 5 does not, and no seventh exists unaccounted for.
3. The identity block: what if S sends no identity, null, a non-object, an oversized or extra-field block, or a block for a DIFFERENT actor than the authenticated caller? Is anything trusted that should be checked (whose identity is it, and who may assert it)? Report what the code does; judge against Kam's ruling.
4. The upsert: run it against real Postgres yourself (your own port): first event, then a second event with a different identity, then the same tx again. State exactly what is overwritten and what is kept, including content_hash, and whether "the identity stored beside a transaction hash is the identity of the event that produced that hash" holds.
5. Consumers of metadata_payload (item 4 above): list them with file:line and the effect of an overwrite on each.
6. Mutants: re-run the author's 14 (reject kills with empty messages or a collapsed cell count), plus at least four of your own (e.g. the helper forwards the CALLER's identity instead of S's; site 5 forwards; the upsert overwrites content_hash; the helper drops identity when another field is present). Include a comment-only control.
7. Merge prediction on the LIVE develop tip (re-read it yourself): overlap scan with a planted control, merge-tree with a conflicting negative control; tests on the predicted tree.

## Rules
Read-only on the project: clone --shared into YOUR scratchpad and fetch there. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; never delete; never rm inside bash -c. Your own Postgres on a free port (lsof first); avoid 55413, 55414, 55418, 55419, 55436, 55440, 55463, 55471. Write only here and in your scratchpad (raw outputs under evidence/, never a directory named out); npm/tar outputs to explicit absolute paths in your scratchpad.

## Output
0_Brain/reference/2026-10-13_gate-pr1549/verdict.md: VERDICT on line 1, sha256/16 of the report on LINE 2 (delete line 2, sha256 the rest, first 16 hex), FOUND / TESTED / HOW, NOT tested, severities with file:line. Merge only on Wednesday's head-bound GO; nothing deploys from this verdict.
