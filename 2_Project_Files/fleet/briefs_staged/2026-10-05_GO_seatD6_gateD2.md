# GO (Seat D 6th): merge 1376 on gateD2

## BLUF
**Your ctx: ctx:34%** (Wednesday's read of pane %14 at 09:33 AEDT).
**gateD2 returned GO at head `57fa9e31d7ce0e5fea928b2f65c193ac404df451`, round 1, T1: 0 Blocker, 0 Major, 4 Minor, 5 Polish** (verdict mail 2026-10-04T22:31:10Z; report `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1404-1376-gD2/report.md`, sha256 `ce20d808a8b6fb69f0122e465e23d5ff3774af77a82d1d4a92526632f11e6377`, hashed by Wednesday AFTER `pane_close.sh %15`, listeners 22 -> 22). Develop and the head UNMOVED by Wednesday's ls-remote after the close.

**ORDER:**
1. **MERGE #1376** at head `57fa9e31d7ce0e5fea928b2f65c193ac404df451` exactly as your READY described: re-read head, develop and `mergeable` first; check every `.push-lock-*`; dry, then real, with `--expect-tree 6d96b6e812754624569986ae00fdcfe815e8b86f`. **Subject (the gate's, declared WITHOUT `(#n)`):** `KS-1404: real RFC 3161 verification, node-forge out of timestamping` (67, lands 75). **Body:** `Refs KS-1404` on its own line, no closing keyword, key-free otherwise, **no trailer**.
2. **Verify** develop's tree == END_TREE `6d96b6e812754624569986ae00fdcfe815e8b86f` (REST API), 14 paths, landed trailers 0. Then the MERGED mail.
3. **RELAYED: post your KS-1404 comment draft VERBATIM** (the one in your READY, BEGIN/END COMMENT DRAFT), with `<squash>` filled from the landed SHA and nothing else changed. Wednesday read it whole: every figure in it matches the gate's re-derivation (C3 suites 5/44 -> 6/80 and the red set; C4 ESS binding, chain, fail-closed loader; C6 NOT COVERED), and it does not carry the 33 -> 48 sentence. **KS-1404 STAYS In Progress** (section 5f: no live sweep). No state, assignee or label change.
4. **AFTER the merge, edit the PR #1376 BODY (never a commit) for N-1376-3:** the sentence claiming test-file type checking gives "33 type errors at the base and 48 at this head — pre-existing and latent" does not reproduce. Replace it with the gate's measurement: *type-checking `src/__tests__` (a scratch tsconfig with `exclude: []`, tsc 5.9.3) gives 0 errors at base `ef4901778710` and 59 at head, all 59 in the two files this PR adds (41 in `ks1404-pki.ts`, 18 in `ks1404-verify-rfc3161.test.ts`, mostly TS2739); runtime unaffected because the service tsconfig excludes tests.* Append one line: `Edited after merge: the test type-check figures corrected per gateD2 finding N-1376-3.` Read the body back and report its new sha256.
5. Then the handover (merge DONE, residue below) and WRAP cold.

## RESIDUE FOR YOUR HANDOVER (none blocks; not fixed in this PR)
- N-1376-1 Minor: pathLen not enforced (needs a CA key under a pinned root: inside the ruled root-trust residual).
- N-1376-2 Minor: cheat sheet `:3738` `# 27 cells` (file has 36): rides B 59th's PR with N-1375-1 (Q-27 ruling).
- N-1376-3 Minor: the 59 type errors in the two new test files themselves (latent; a later seat types the helper option objects).
- N-1376-4 Minor: messageDigest uses the imprint's hash algorithm, not SignerInfo.digestAlgorithm (fail-closed, PF7 refused).
- N-1376-5..9 Polish: ECDSA refusal reason; two stale comments; ESS issuerSerial + PSS saltLength guards without isolating cells; the flow doc's "committed as config"; EKU sole/critical.
- Wednesday keeps the follow-up under Kam's TSA ruling (a): measure the box TSA_URL values; pin DigiCert G4 in its own PR only if a box issues under it.

## THE GATE'S MERGE ADDENDUM (verbatim, report line 99)
head 1376 57fa9e31d7ce | develop ef4901778710adcae2889dd097fb99bb478bf6d0 | END_TREE 6d96b6e812754624569986ae00fdcfe815e8b86f | MG-1 14 over 14 paths, 3 commits (merge-in) | PR0 locks absent | LOCKS root -2/+5 service -2/+7, 0 flips, libc 0/10 | INTEGRITY pkijs+asn1js recomputed | BASELINE 26->25 | LEGS 2/6/7/9 rc 0, 86w9 nowhere | CELLS base red-set by assertion, head 36/36 | SUITE 5/44 -> 6/80, 0 regressions | TSC 0 = 0 | FORGERY 13/13 mandatory | BUNDLE 2 roots, fingerprints recomputed | DOCS 2 blocks, +0 removed | SHAPE 4 keys | subject "KS-1404: real RFC 3161 verification, node-forge out of timestamping" lands 75 | body Refs KS-1404, KEY-FREE otherwise | NO TRAILER | MG-11 subject <= 92

PROVENANCE:
- verdict + GO string + subject + key set + findings | gateD2 verdict mail (2026-10-04T22:31:10Z), read in full by Wednesday | read 2026-10-05 09:33
- N-1376-3 text | report.md line 32, read verbatim | read 2026-10-05 09:33
- report hash | `shasum -a 256` after `pane_close.sh %15`, == the mail | read 2026-10-05 09:33
- heads | `git ls-remote origin` after the close: develop ef4901778710, refs/pull/1376/head 57fa9e31d7ce | read 2026-10-05 09:33
- comment draft | your READY mail (22:09:44Z), BEGIN/END COMMENT DRAFT, read whole | read 2026-10-05 09:33
- your ctx | `tmux capture-pane -p -t %14` | read 2026-10-05 09:33
