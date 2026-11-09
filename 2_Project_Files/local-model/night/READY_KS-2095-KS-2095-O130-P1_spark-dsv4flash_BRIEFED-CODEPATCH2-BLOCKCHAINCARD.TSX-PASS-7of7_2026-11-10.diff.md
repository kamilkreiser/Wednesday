# READY — KS-2095-KS-2095-O130-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2095_o130_p1_issuer_blockchain_card_leaves_out_the_block_row_when_there_is_no_height/out.md.checker/patch.diff`** (from `ls` at 10:55 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2095_o130_p1_issuer_blockchain_card_leaves_out_the_block_row_when_there_is_no_height/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2095_o130_p1_issuer_blockchain_card_leaves_out_the_block_row_when_there_is_no_height/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 10:55 2026-11-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2095_o130_p1_issuer_blockchain_card_leaves_out_the_block_row_when_there_is_no_height/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `0115269abd111ee6acedb06fb0a0c3f8fd86f35a`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx } + { Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx` (product) and `Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	0	Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx
32	0	Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: BlockchainCard.tsx`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx`; test(s): `Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx 32 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 11 run; controls green; assertion reds)` [red_first.json: failed=3 of total=11; red cell(s): ['BlockchainCard RED ks2095 R1 a proof with blockNumber 0 renders no block-number element', 'BlockchainCard RED ks2095 R2 a proof with blockNumber 0 prints no Block label and no bare 0', 'BlockchainCard RED ks2095 R3 a proof whose blockNumber is absent (undefined at run time) renders no block-number element and does not throw']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (11 passed / 11 run)` [green_after.json: failed=0 of total=11, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=15 failed=0 | after: total=20 failed=0` · `NEW reds: []` [baseline_suite.json total=15 failed=0; after_suite.json total=20 failed=0]
- A6 [verbatim]: `PASS A6 whole frontend/issuer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for frontend/issuer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx` (+3/-0 per numstat.out) and the test file `Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx` (+32/-0); 2 files in all (code_patch2: products Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `0115269abd111ee6acedb06fb0a0c3f8fd86f35a` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2095_o130_p1_issuer_blockchain_card_leaves_out_the_block_row_when_there_is_no_height/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2095_o130_p1_issuer_blockchain_card_leaves_out_the_block_row_when_there_is_no_height/checker.out`.

```diff
diff --git a/Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx b/Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx
--- a/Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx
+++ b/Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx
@@ -192,3 +192,5 @@ export function BlockchainCard({ proof, animate = true }: BlockchainCardProps) {
+            {/* KS-2095: a proof with no known block height (0, or absent) must not print "Block 0"; the row is left out. */}
+            {proof.blockNumber > 0 && (
             <div className="flex items-center justify-between text-xs">
               <span className="text-muted-foreground">Block</span>
               <span className="font-mono text-[11px]" data-testid="block-number">
@@ -199,3 +201,4 @@ export function BlockchainCard({ proof, animate = true }: BlockchainCardProps) {
+            )}
             {proof.slot !== undefined && (
               <div className="flex items-center justify-between text-xs">
                 <span className="text-muted-foreground">Slot</span>
diff --git a/Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx b/Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx
--- a/Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx
+++ b/Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx
@@ -62,4 +62,36 @@ describe('BlockchainCard', () => {
     render(<BlockchainCard proof={mockProof} animate={false} />);
     expect(screen.getByTestId('copy-tx-hash')).toBeTruthy();
   });
+
+  // KS-2095: the issuer's DocumentDetail builds the proof with `blockNumber: ... || 0`, so an anchor with no known height reached this card as 0
+  // and the card printed "Block 0" even for a confirmed anchor. A proof with no height leaves the Block row out and keeps everything else.
+  it('RED ks2095 R1 a proof with blockNumber 0 renders no block-number element', () => {
+    render(<BlockchainCard proof={{ ...mockProof, blockNumber: 0 }} animate={false} />);
+    expect(screen.queryByTestId('block-number')).toBeNull();
+  });
+
+  it('RED ks2095 R2 a proof with blockNumber 0 prints no Block label and no bare 0', () => {
+    render(<BlockchainCard proof={{ ...mockProof, blockNumber: 0 }} animate={false} />);
+    expect(screen.queryByText('Block')).toBeNull();
+    expect(screen.queryByText('0')).toBeNull();
+  });
+
+  it('RED ks2095 R3 a proof whose blockNumber is absent (undefined at run time) renders no block-number element and does not throw', () => {
+    const noHeight = { ...mockProof, blockNumber: undefined } as unknown as BlockchainProof;
+    expect(() => render(<BlockchainCard proof={noHeight} animate={false} />)).not.toThrow();
+    expect(screen.queryByTestId('block-number')).toBeNull();
+  });
+
+  it('control ks2095 C1 a proof with blockNumber 0 still shows the tx details, the truncated hash and the slot', () => {
+    render(<BlockchainCard proof={{ ...mockProof, blockNumber: 0 }} animate={false} />);
+    expect(screen.getByTestId('tx-details')).toBeTruthy();
+    expect(screen.getByText('a1b2c3d4...1234abcd')).toBeTruthy();
+    expect(screen.getByText('Slot')).toBeTruthy();
+  });
+
+  it('control ks2095 C2 a proof with a real height still shows the Block row with that number', () => {
+    render(<BlockchainCard proof={mockProof} animate={false} />);
+    expect(screen.getByText('Block')).toBeTruthy();
+    expect(screen.getByTestId('block-number').textContent).toMatch(/^1\D?234\D?567$/);
+  });
 });
```
