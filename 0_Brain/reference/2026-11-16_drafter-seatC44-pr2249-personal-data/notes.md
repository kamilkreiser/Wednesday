# Drafter notes: Seat C 44th, PR 2249 fix round (2026-11-16, 11:15 to 11:41 AEDT)

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatC44_pr2249_personal_data.md (about 40.8 KB). STAMP block blank. SELF-CHECK 11:41.

## What I did (read-only on !CODING; all scratch under _work/)
- Read the commission, gate 374 verdict, W 32nd's brief + four mails + HANDOVER, C 43rd HANDOVER, the R 121st / A 31st existing-branch driver set.
- Own `--shared` clone `_work/c44` (objects borrowed from gate 374's scratch repo; PR head, 2161, 2138, develop 553c0f8 fetched from that local repo). Built a compile-checked PROTOTYPE of the fix (`proto_patch.py`, `proto_patch2.py`, `proto.diff`), a 32-cell realistic cell file (`ks590p-realistic-personal-data.test.ts.draft`), a 19-answer leak dump (`dump_*.json`), 8 mutants (`mutants.py`), a forced-cell census (`census_proto.json`), merge-tree both orders (`mt.out`).
- Every jest/tsc run was load-gated (load1 <= 8; logged in the runner outputs).

## Findings that change the commission's default (for Wednesday)
1. Same-tenant cannot stay unchanged: index.ts:265 gives every request the default tenant; v1 verify has no authenticate. A live anonymous caller is "same-tenant" for default-tenant rows and today sees the email local part AND the user id on all four paths (develop and head). Brief recommends one public view for all callers (X); alternative Y costed. Needs Wednesday's confirmation at the stamp.
2. The "three paths that show the user id today" are the chain-first answers: the anchor's issuerOrgId (a user id) reaches `issuer`, `certification.certifierOrganizationId` and `onChainMetadata.issuerOrgId` on v1 verify-file, v1 by hash and v2 chainOnlyMatch. PR 2249 left those lines untouched; the fix round changes them.
3. Company vs person: reliably separable on the write side (the person lives only in certification_metadata.issuerName); the residual is a TYPED person's name in issuedBy. Rule R (organization_name, metadata.issuerName, issuedBy fields, "@" filtered) recommended; Rule S (organization_name else null) is the strict default, mostly null for K-minted documents.
4. docs/VERIFICATION.md line 59 shows an email as the issuer example: PR 2249 left it untouched; it needs an edit.

## Instruments and controls
- tsc: first run rc 2 with 6 TS6133/TS2614 errors (check bites), rc 0 after counted fixes.
- Red-first: head 31 red / 1 pass; develop 27 / 5; prototype 0 / 32; all reds AssertionError (0 other).
- Mutants gB, gC, m1 to m6 all killed by assertion; product sha256 equal before/after.
- Census: 20 forced existing cells in 6 files (ks590n 13, ks1986 2, ks1557-trusted 2, ks584-p3 1, ks1561-verify-original-registrant-certifier 1, ks563 1). One further red in that run was my own dump file with no output path (scratch, not product).
- Develop-moved ks1634 tests: 22/22 green on the prototype.
- Intersection develop-move x branch paths: 0, control 1.
- merge-tree: prototype x 2161 clean both orders (tree a5a28366aaf7); head x 2161 tree 0aca64bc3e2c (same as gate 374); PR 2138 x prototype rc 1 (control).

## Slips and honest corrections
- First P5 cell draft had no documentId in the chain metadata (answer had none), so two P5 cells were red on the prototype for a harness reason; fixed and re-run before any number went into the brief.
- First tsc run refused at load1 > 8 (gate worked); waited.
- A grep census of test files is wider than the after-suite census (9 candidate files vs 6 red); the brief says the whole-suite census is the instrument.
- Not run: the whole originate suite on the prototype (67 related suites only), eslint, docs-fragment check, any push.
- No write under /Volumes/DevMASTER/!CODING (the shared clone c44 lives in _work). 358 MB in _work/c44 (a worktree); I did not delete it (no rm).
