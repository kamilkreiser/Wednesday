## QA GATE - TIER 2, round 1: GO WITH NOTES

**PR:** Secuura/Distributed_Secuura #1821, "KS-1840" (Seat R 65th)
**Head:** `345f5111f6f6dde17e2de538fbb61cd20e5535d3`. ls-remote of refs/pull/1821/head showed this SHA at the start and again at the end (2026-10-29T22:14Z). It matches the claim.
**Develop:** `e3d8456ec81d0b02172dd5a3060404815e797bde`, the same at both reads. Merge-base with the head: `593cd90c3131`.
**Gate:** QA gate 25. Findings only. I fixed nothing, commented nowhere (no GitHub, no Linear), pushed nothing, merged nothing, deployed nothing.

### Counts
- **Diff:** 6 files, +82 / -4, exactly the 6 declared (three-dot against develop e3d8456e and against 593cd90c both give the same set). Per file: BACKLOG.md 7/0, DEVELOPMENT.md 1/1, index.ts 3/3, the new test 32/0, flow doc 20/0, cheat sheet 19/0. No other anchoring source file changed.
- **index.ts is comment-only. Proof:** I printed the TypeScript AST of the base file and the head file with `removeComments: true` and compared. Equal (68792 = 68792 chars). **Control:** a head copy with `res.status(404)` changed to `405` printed UNEQUAL against the base, and develop's index.ts printed equal to the base's. Also, every changed line in the `-U0` diff starts with ` *` (0 non-comment changed lines). Scripts: `ast.js` (the proof) and `strip.js` (a scanner version; it mis-scans this file and reports false, see I2).
- **DEVELOPMENT.md:** one hunk, line 121, one line out, one in. **BACKLOG.md:** one hunk, 7 lines added, 0 removed.
- **Red-first, spark_gate:** BASE product code 3 passed / 2 failed (R1, R2 red; C1 to C3 green); HEAD 5 / 0.
- **Red-first, my own swap:** at head 5/5. With the base's index.ts (old comment) restored: 2 failed / 3 passed (R1, R2 red, C1 to C3 green). Restored file sha256 `71b089cd...` equal before and after.
- **Whole anchoring suite, same tree, same symlinked install:**
  - Head: 37 files, 526 passed / 3 failed / 21 skipped of 550 (34 files green, 3 red).
  - Develop e3d8456e: 36 files, 521 passed / 3 failed / 21 skipped of 545 (33 green, 3 red).
  - Delta +5 cells, all pass, 0 new reds. The same 3 red on both sides: `threadTokenMint ... per-seed policyId` and ks1717 R10 and R11. The ks1822 file (12 cells) is skipped on both sides.
  - **threadTokenMint is red on both** (pre-existing, as known). The other red files are my install (I1).
- **Merge-tree of the head onto e3d8456e:** CONFLICT, in exactly two files, both under `Projects Documents/` (the flow doc and the QA cheat sheet). Tree `1d270f05...`. BACKLOG.md, DEVELOPMENT.md, index.ts and the new test merge clean. The merged tree differs from the head only by develop's 4 nft-certificate files and the two conflicted docs.

### Findings

**N1 (Note, claim check; the claim is TRUE).** The retired function is no longer cited in `index.ts`: `git grep makeFetchDocFromAnchorStore` in `Blockchain/` at head gives DEVELOPMENT.md (1) and the test's R1 line (1), nothing in index.ts; at 593cd90c the same grep gave index.ts:984 and DEVELOPMENT.md:121 (positive control). The retirement is real: `78cb3c393` "KS-1628 (2 of 2): retire the public POST /api/documents/:id/verify (#1589)" deletes `makeFetchDocFromAnchorStore` from api-gateway `routes/verification.ts` (the deleted diff contains `-function makeFetchDocFromAnchorStore(`), and it is in develop's history. The function is absent from `api-gateway/src` at head.
- **New index.ts comment:** "The gateway function once cited here as the caller that handles a non-200 was retired in KS-1628. Whether a current caller treats a 404 from this route as no anchor is not measured (KS-1840)." Accurate. A grep of non-test, non-doc source in `Blockchain/Dev` for `anchors/document` finds no caller inside the services other than the route itself, the spec/OpenAPI metadata and the specRouteMap pattern (so "not measured" is honest; I did not search the frontends or external callers).
- **DEVELOPMENT.md:121 new sentence:** same statement, same truth, and it names the retired function on purpose.

**N2 (Low, pre-existing, same row, not in the diff).** DEVELOPMENT.md:121 still says "Verified: nonexistent id -> `404 {"error":"No anchors found"}`". The handler at head returns `{ success: false, error: { code: 'NOT_FOUND', message: 'No anchors found' } }` (index.ts:991, and `ABSENT_DOCUMENT_ANCHORS_BODY` in anchorReadGate.ts:147). So the same row still carries a second stale sentence. The PR is scoped to the one citation; flag only, not a fix-before-merge. The body shape changed after the row was written.

**N3 (Low, docs literal accuracy).** Both new Projects Documents blocks say `git grep makeFetchDocFromAnchorStore` "finds 2 hits" (flow doc 119.1) / "2 after the change" (cheat sheet). Run with no pathspec at head it finds 4 files / 6 lines (DEVELOPMENT.md 1, the test 1, flow doc 2, cheat sheet 2), because the two new doc blocks themselves name the symbol. It is 2 only in `Blockchain/` (I ran both, both ways). Suggest "in `Blockchain/`" at prep. Not a code claim.

**N4 (Info). The test is a text pin.** R1 (`not.toContain('makeFetchDocFromAnchorStore')`) would also pass if the comment were deleted outright; R2 requires `was retired in KS-1628` and `is not measured (KS-1840)`, which closes that. Nothing reads DEVELOPMENT.md (the author said so and suggested a twin cell; not added, so the doc row can regress unseen). C2 pins the handler line text, C3 is a non-empty read. Header and describe title now say what the cells read; I checked the text.

**N5 (Scope, item C; flag, do not decide).** BACKLOG.md item C is a pure 7-line addition about the `threadTokenMint` cell, a different subject from the ticket (a stale route-comment citation). It is out of the ticket's apparent scope; the author discloses it, gives a reason (no open PR touches BACKLOG.md) and says it is easy to drop. I could not read the Linear ticket (no access in this gate), so I cannot say whether KS-1840 lists it. The call is Kam's / the coordinator's: keep it, or move it to its own PR.

**N6 (Accuracy of the item C sentences, against gates 20 and 21):**
- "describe at :16, its one it at :17": TRUE (`threadTokenMint.test.ts` line 16 `describe(`, line 17 `it(`).
- "Red in gate 20": TRUE (gate 20 verdict: 536/537 pass, 1 fail = this cell; also at the PR head 524/525 and "at base per KS-1827").
- "green (509 of 509 and 517 of 517) in gate 21": TRUE (gate 21 verdict, 1817-1).
- "Both gate verdicts record the host Node as v26.8.1": TRUE (gate 20 line 127, gate 21 line 58).
- "which host or install tree differs is not recorded": MOSTLY. Gate 21 did record one install-tree fact (its first run lacked `packages/shared`; it copied the built one beside node_modules, verdict line 68), though it did not link that to this cell. Wording stands as "not recorded" for the cause; the sentence could name that.
- "Red ... on Seat R 64th's host and on Seat R 65th's host": NOT CHECKABLE from the gate files; those come from the seats' own runs. I cannot verify them.
- "measured 2026-10-29 UTC": the gate folders are dated 2026-10-30 locally; I cannot reconcile the UTC date from the verdicts alone. Cosmetic.
- **A new data point, mine:** red on both head and develop on this host (Node per the host, vitest 4.1.x, symlinked checkout install). The item says "Cause not measured", which stays true.

**N7 (Info, merge-prep).** Both Projects Documents files conflict textually (the new blocks append at the same point as develop's section 118 blocks). Section numbers: develop's highest flow-doc section is 118 (the NFT list block); the head has 116, 117, 119 (no 118). The author's stated renumber at prep (B to 120, A to 119) is consistent. Keep both sides in each file.

### TESTED / NOT TESTED / HOW

**TESTED**
- **Head:** ls-remote at the start and the end.
- **Diff:** scope, numstat and `-U0` hunks.
- **index.ts:** comment-only proof, by the AST print, with two controls (a code-mutated copy; develop's copy).
- **The claim:** against KS-1628 (`78cb3c393`) and a grep at base and head.
- **The route's current handler:** read.
- **Red-first:** spark_gate and my own swap.
- **The whole anchoring suite:** head and develop.
- **Merge-tree.**
- **Gate 20 and 21 verdicts** checked against item C.

**NOT TESTED**
- html_docs_check on the two docs (the author's rc 0 and the planted controls are not reproduced); a browser render.
- tsc, eslint, audit:gate and audit:locks on the new files.
- The `threadTokenMint` cause.
- The Linear ticket text and the PR body (no gh login in this shell).
- The anchoring integration files, the four platform suites, Node 24, any running stack.
- Any caller outside `Blockchain/Dev/services` (frontends, other repos) of the 404 route.
- The "Seat R 64th" run.

**HOW**
- **Clone:** `git clone --shared` of the checkout into the then-non-existent `.../scratchpad/gate25/clone`. `rev-parse --show-toplevel` was asserted equal to it before the fetch. Origin was set to `git@github.com:Secuura/Distributed_Secuura.git` and the checkout's `core.sshCommand` was read and copied. It fetched `refs/pull/1821/head` and `develop` only.
- **node_modules:** the root `Blockchain/Dev/node_modules` and `services/anchoring/node_modules` were symlinked from the checkout (untracked, never added). TMPDIR=/tmp/g25.
- **spark_gate:** `spark_gate.sh <clone> 1821 <head> develop <test> --node-modules <checkout>/Blockchain/Dev/node_modules --work ... --out .../spark`, rc 0. It asserted the head as the tip with merge-base 593cd90c and base tip e3d8456e, and reported 6 files +82/-4. Artefacts in `spark/`.

### Instrument errors / caveats of my own
- **I1.** The suite has 3 red at develop AND head, not the author's 1: ks1717 R10 and R11 fail with `TypeError: isUsableEmitterSecret is not a function`, and the 12 ks1822 cells are skipped. That is the checkout's prebuilt `@secuura/shared` lacking that export (the same cause as gate 24's I1), so it is my resolution, not the PR. Identical on both sides. I did not rebuild shared. The 21 skipped cells are those same two files.
- **I2.** My first comment-strip, with the TypeScript scanner, returned "not equal" for the base-vs-head control pair as well as the real one: the scanner, run without parser context, does not take this file's JSDoc block as a comment in one spot. I discarded it and used the parser's `removeComments` printer. `strip.js` is kept for the record, not as evidence.
- **I3.** The `pretooluse_no_cd.sh` hook refused `git -C $VAR <write verb>` (fetch, checkout, merge-tree) three times; each was re-issued with the literal scratchpad path, against my clone only. Nothing ran against the Secuura checkout.
- **I4.** threadTokenMint took 50 s at head and 1.2 s at develop, both red. The head run was under load (spark_gate had just run); I do not claim timing as a finding.

### FIX-BEFORE-MERGE
(none)

Optional at prep: N3 ("in `Blockchain/`"); decide N5; both docs conflict (N7).
