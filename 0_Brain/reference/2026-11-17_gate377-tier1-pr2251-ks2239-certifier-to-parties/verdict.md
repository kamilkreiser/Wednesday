PR 2251: GO WITH NOTES (at head 26a85f3ece804fd45d707d061e2ef8f6817b89bc; tier 1)

Gate 377, tier 1, claude-opus-5-5, 2026-11-17 05:35-05:53 AEDT. Findings only: nothing fixed, posted, pushed, merged or written outside this folder.
I checked the pins by gh api twice, at 18:35:17Z and again at 18:52:40Z, and nothing had moved: PR 2251 is open and unmerged, head 26a85f3ece80, base aa4ddb096053. Develop is c480a84e7f53 (PR 2185, gateway redis.ts only, 0 originate files). PR 2160 is open at head b02bd2716cc2.
Environment: my own `--shared` clone in scratch/repo, with worktrees scratch/d (develop c480a84) and scratch/h (head). Package files are identical to gate 376's tree (0 package.json or lock files differ), so I copied node_modules from gate 376's tree as APFS clones (`cp -c`) instead of running `npm ci`. That copied 3 trees (root, originate, shared). I rebuilt shared/dist with tsc in each tree, rc 0. TMPDIR was /private/tmp/g377t, and every jest or tsc run started below load1 8.

## Q1. Who sees the certifier: MEASURED
- **Write side.** `fromDbRow` sets `issuer.id = row.issuer_user_id || certMeta.issuerId || ''`. `issuer_user_id = toActorUuid(cert.issuer.id)`: the certifying user's UUID, or null for a connector, which then falls back to `certMeta.issuerId`, the literal `connector:` principal. `cert.issuer` is `getUserFromRequest(req)` at issue. `issuer.did = certMeta.issuerDid || meta.issuerDid`: the first is `req.user.did`, which no mint sets (the builder's census, not re-run); the second is caller-typed legacy document data.
- **Code diff.** With comments stripped, head against develop differs by 3 lines: one `const mayNameIssuer = principal ? callerMayReadCertification(req, certification) : false;` and two ternaries. The charge line and the read rule's body are untouched.
- **Run on head.** The builder's 34 cells and my own 11 cells in scratch/h `__tests__/g377-gate-cells.test.ts` all pass; this file stays in scratch and is never pushed.
  - These get both values null: a same-tenant user of another organisation, an ORG_ADMIN, an `org_admin`, an `Org_Admin`, an ISSUER_ADMIN, a `platform_admin`, an array role, a userId-less token, and an empty-string userId on the empty-issuer row.
  - Two more get null: a user of the certifier's OWN organisation who is not a party (G4), and a token whose organizationId equals the certifier's id, or which has an `id` claim but no userId (G5).
  - These still get the values: the holder, the certifier, SYSTEM_ADMIN, super_admin, the connector, and `system_admin` (G1).
  - Anonymous callers get null, unchanged.
- **Other fields of the answer.** A non-party's answer has exactly the keys blockchain, certificationId, chargeEventId, checks, issuer, status, verified and verifiedAt (G6).
  - The `blockchain` blob holds anchor state only. Its writers are issue (anchorId, txHash, confidence, status), the document anchor writes (txHash, blockHeight, anchorId, status, simulated, createAttempts, threadToken policy and script fields, and `error`, which is up to 500 characters of anchoring's error text) and anchorStateSync. I counted 0 identity, issuerOrgId, userId or email keys in anchorStateSync; the control was 14 `blockchain` lines.
  - Measured: **no person-derived value reaches a non-party.** This PR does not change the blob. Residual, read but not run: the `error` string is anchoring's own validation text, which echoes paths, not values, for the DID regex.
  - Nothing for Kam on personal data.

## Q2. Billing untouched: MEASURED
- The charge statement is byte-identical: it is not in the code diff.
- X-C5 pins the whole argument list for 7 kinds of caller. My G2 checks that 5 more non-party role spellings are each charged exactly once, and G3 pins `'anonymous'` as the initiator for an empty-string userId.
- The builder's m-X6 reran with the same 7 reds, plus 6 of my G cells.
- My own charge mutants:
  - g-M3 (a non-party is billed as 'anonymous'): 3 red (X-C5 for the non-party and the ORG_ADMIN, and ks1699v V-C1).
  - g-M4 (the party bit added to the charge metadata): 10 red (X-C5 x7, V-C1, V-A6 and G3).
- Anonymous calls: 0 charges (X-C6 x5).
- **No billing change. Nothing for Kam.**

## Q3. The party rule is reused, not widened: MEASURED
- `callerMayReadCertification`'s body is unedited; only its JSDoc changed.
- `''` never matches `''`: X-A5 x2 and G3 pass on head. My g-M6 (guard removed) reds X-A5, G3 and ks1695 R13.
- **Case variants.** `isPlatformRole` ASCII-folds the role, so a lower-case `system_admin` IS a platform role. It gets the certifier on verify (G1), as it already does on GET /:id (G7: 200).
  - A lower-case `org_admin` or `Org_Admin` is NOT a party: it gets null, and GET /:id answers it 404.
  - My g-M5 (a literal upper-case set in place of isPlatformRole) reds X-C3 (super_admin), G1 and G7, plus the ks1695 C3, C10 x2, C11 and R13 cells. So the fold is pinned.
  - This PR narrows, never widens: before it, every signed-in caller saw the certifier.
  - **Context for Kam's open demo-accounts card:** if the 2 lower-case `system_admin` demo accounts are not really platform admins, they still see the certifier on verify, as on GET /:id. This is not a defect of this PR.

## Q4. Nothing else changed: MEASURED
- The code diff is confined to the verify handler (3 lines).
- Census of the whole originate suite, cell by cell, A2 (develop c480a84) against B2 (head):
  - only develop's old V-C7 title is gone, and only the new V-C7 title plus the 34 ks2239 cells are new;
  - 0 status changes;
  - V-C3 (8 other routes still 401 for an anonymous caller) and X-C8 are green.
- V-C7 is the only changed existing cell. The ks1699v header sentence also changed (a comment).
- Merge-tree of develop c480a84 and the head: clean both orders, same tree d7a8fc221140. The merged certifications.ts is the head's and redis.ts is develop's.
- Merge-tree of the head and PR 2160 b02bd2716cc2: clean both orders, tree 78c9141c5d95, and the merged file carries both edits.
- Planted controls:
  - the head plus an edit of 2160's `const msg = ...` gives 1 CONFLICT in each order;
  - the head plus an edit of develop's redis.ts line gives 1 CONFLICT in each order.

## Q5. Tests are honest: MEASURED
- **Red first.** The ks2239 file on develop's product bytes gives 10 failed / 24 passed of 34, all by AssertionError, and 34/34 at head.
- **The builder's 12 mutants, rerun in my tree.** Counts below are reds in the builder's own files. The extra G cells are mine, and the leaks they catch are consistent:

  | mutant | reds |
  |---|---|
  | m0 | 11 |
  | m-noop | 0 |
  | m-X1 | 11 |
  | m-X2 | 11 |
  | m-X3 | 4 |
  | m-X4 | 3 |
  | m-X5 | 1 |
  | m-X6 | 7 |
  | m-X7 | 9 |
  | m-X8 | 1 |
  | m-X9 | 6 |
  | m-X10 | 21 |

  All are the same as the builder's, with 0 predicted-but-not-red and every red an AssertionError. Each mutant was restored by content, and the sha256 was equal afterwards (918af18d076e).
- **m-X10's extra cells.** There are 19, not the 17 in the commission (the builder corrected this in the READY): R14 and R15 in ks1695, plus 17 S, R and P3 cells in ks1699-share. All exercise `callerMayReadCertification`, directly (GET /:id) or through `callerMayShareOrRecertify`, which calls it first. Confirmed: they are the shared read rule's own cells.
- **My mutants:**

  | mutant | change | reds |
  |---|---|---|
  | g-M1 | the did leaks to an org-admin-role non-party only | 3: X-A3 and G2 x2 |
  | g-M2 | party-ship by organizationId | 9: X-C1, C2 x3, C4, C7 x2, C9 and G5 |
  | g-M3, g-M4 | the charge mutants | see Q2 |
  | g-M5 | literal upper-case platform set | see Q3 |
  | g-M6 | empty-principal guard removed | see Q3 |

  Its first run load-failed (TS6133, an unused import) and I fixed it. Then 8 red, all AssertionError.
- **Whole originate jest, interleaved, `--maxWorkers=50%`:**

  | run | tree | suites / tests | failed | load1 at start |
  |---|---|---|---|---|
  | A1 | develop | 230 / 2,817 | 0 | 7.93 |
  | B1 | head | 231 / 2,851 | 0 | 7.47 |
  | A2 | develop | 230 / 2,817 | 0 | 7.76 |
  | B2 | head | 231 / 2,851 | 0 | 6.75 |

  These equal the builder's numbers.
- **tsc:**
  - src: rc 0 on both trees;
  - test tree: the same 4 pre-existing errors on both (ks1937 and ks488, TS2300 and TS2451), 0 in the PR's files;
  - a planted TS2322 is reported.
- **eslint `--max-warnings 0`:** 0 errors and 0 warnings on all 3 changed .ts files. The plant gives 2 (no-var, no-unused-expressions).
- **Docs:** `docs-fragments.mjs check` is green. The planted unclosed div gives rc 1 (FAIL, 1 finding), and after the restore (sha256 equal) it is green again.

## Q6. The PR body: READ
- Present:
  - Kam's four rulings, stated as facts;
  - the W34-R4 `OVL_IGNORE_PRS="2160"` line (count 1);
  - the W-1 and W-2 tables;
  - an honest NOT-run list (Schemathesis, Akto, Playwright, k6, no stack, production UNMEASURED);
  - the hook's final line, verbatim (count 1).
- Absent, as required:
  - closing keywords: 0 hits for `close[sd]|fix(e[sd])|resolve[sd]`; a planted "Fixes KS-1" gives 1;
  - a self-hold sentence: the only "hold" hits are "holder".
- `KS-2239` is the only hyphenated key.

## Notes (GO WITH NOTES; none blocks)
- N1 (low, PR body): the body never names **tier 1** ("tier" occurs 0 times; control "Kam" 1). The commission asks for it.
- N2 (low, PR body wording): "Ran (all local, on develop eb27110fc6e4)" heads a list that also holds the A2/B2 runs on aa4ddb096053. The table itself is correct.
- N3 (info, environment): my `check:test-types` gives rc 1 with 2 "new" auth errors. Develop gives exactly the same 2 in my tree, and the cause is that my tree lacks the nested service node_modules (I cloned 3 trees). The PR touches 0 files in the five services on that list, and originate is not on it. This is not the PR's.
- N4 (info, flake): my first, unintended whole-suite run on head ran at default workers, and load1 climbed to 16.79. In it, ks1385 C7 was red and ks488 load-failed (TS2300 against ks1937). Neither file is touched by the PR. Both pass in isolation (4 suites, 94/94), and all 4 controlled whole runs are green. These are pre-existing, load or order dependent; ks488 is the builder's candidate (5).
- N5 (info, client-visible): a non-party now gets a NEW `did: null` key where the key was absent, and the verifier ResultPage shows "Unknown". Both are declared in the PR body.
- N6 (context for Kam's demo-accounts card): a lower-case `system_admin` is a platform role, so it is named the certifier (Q3).
- Out of scope by Kam's 17:08:43 ruling: issuerOrgId anchored on chain. Not reported as a defect.

## For Kam by name
None from this PR. No personal data reaches a non-party, and no billing changes. For his open demo-accounts card only: lower-case `system_admin` tokens are treated as platform admins here, as on GET /:id.

Evidence: scratch/o/ (whole_A1/B1/A2/B2.json, mut/summary.json, mut_m5/, tsc_*.out, docs_*.out, check_test_types.out), scratch/mt.sh, scratch/mutants.py, scratch/static.sh, scratch/docs.py, scratch/pr_body.md, and scratch/h/.../g377-gate-cells.test.ts.
