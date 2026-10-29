# READY — KS-1666-KS-1666 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1666_p1_certify_reservation_comments/out.md.checker/patch.diff`** (from `ls` at 08:58 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1666_p1_certify_reservation_comments/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1666_p1_certify_reservation_comments/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 08:58 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1666_p1_certify_reservation_comments/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `593cd90c3131f200f4adaf242c1a406a5b66fbb0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	2	Blockchain/Dev/services/originate/src/routes/certifications.ts
34	0	Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (4 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 4 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts 34 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1666 (d): the certify reservation comments match the code RED KS-1666 R1 the reservation comment no longer says the row-first order removes the window', 'KS-1666 (d): the certify reservation comments match the code RED KS-1666 R2 the provisional-row comment no longer calls the window sub-second and names the 10 second bound']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1849 failed=0 | after: total=1854 failed=0` · `NEW reds: []` [baseline_suite.json total=1849 failed=0; after_suite.json total=1854 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+4/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts` (+34/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `593cd90c3131f200f4adaf242c1a406a5b66fbb0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1666_p1_certify_reservation_comments/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1666_p1_certify_reservation_comments/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -517,14 +517,16 @@
       // `anchor_store` row before it answers 202 (anchoring/src/index.ts), so under the old order ANY failure of
       // this write left an anchor naming no document — an orphan anchor, from a legitimate authenticated flow,
       // permanently, and orphan anchors are the rows whose anchored identity another registration can claim (the
-      // KS-1612 round-2 Major). Writing the row first removes the window rather than narrowing it.
+      // KS-1612 round-2 Major). Writing the row first NARROWS that window, it does not remove it: when the reservation
+      // itself fails, the anchor-then-fail path is unchanged (KS-1666 d).
       //
       // RULED (out of the ticket's option 1): every response stays byte-identical to before. That costs two writes
       // on the accepted path — a provisional row, then the real anchor state through the same
       // `ON CONFLICT (id) DO UPDATE` — and a compensating delete on the one refusal that sits between them.
       //
       // The provisional row deliberately carries the anchor state a FAILED anchor would carry: it under-claims for
-      // the sub-second window before the second write, and introduces no new `anchoringStatus` value into the blob
+      // the window before the second write (bounded by the anchoring call's AbortSignal.timeout(10000), so up to 10
+      // seconds, not sub-second), and introduces no new `anchoringStatus` value into the blob
       // KS-1124 F4 ruled on. `confidence` is already 'pending-onchain'. Nothing in this request reads the row in
       // between; a concurrent reader sees "off-chain only", which is true at that instant.
       const tenantId = lifecycleTenantId;
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts
@@ -0,0 +1,34 @@
+// KS-1666 note (d) (gate AK1 on PR #1623, KS-1633): two comments in routes/certifications.ts said what the code does not do. One claimed that writing the documents row before the anchor
+// "removes the window rather than narrowing it" (when the reservation itself fails the anchor-then-fail path is unchanged, and the code's own comment further down says an orphan anchor can still be created).
+// The other called the provisional row's under-claim a "sub-second window" (the window lasts until the second write, after an anchoring call bounded by AbortSignal.timeout(10000)).
+// These cells read certifications.ts as text. R1 and R2 are red until the two comments are corrected; C1 to C3 pin the code the comments describe, which must not move.
+import { describe, it, expect } from '@jest/globals';
+import { readFileSync } from 'fs';
+import { join } from 'path';
+
+const SRC = readFileSync(join(__dirname, '..', 'routes', 'certifications.ts'), 'utf8');
+
+describe('KS-1666 (d): the certify reservation comments match the code', () => {
+  it('RED KS-1666 R1 the reservation comment no longer says the row-first order removes the window', () => {
+    expect(SRC).not.toContain('removes the window rather than narrowing it');
+    expect(SRC).toContain('NARROWS that window, it does not remove it');
+  });
+
+  it('RED KS-1666 R2 the provisional-row comment no longer calls the window sub-second and names the 10 second bound', () => {
+    expect(SRC).not.toContain('the sub-second window before the second write');
+    expect(SRC).toContain('up to 10');
+    expect(SRC).toContain('seconds, not sub-second');
+  });
+
+  it('control KS-1666 C1 the anchoring call is still bounded at 10 seconds', () => {
+    expect(SRC).toContain('signal: AbortSignal.timeout(10000),');
+  });
+
+  it('control KS-1666 C2 the code still says an orphan anchor can be created when the reservation fails', () => {
+    expect(SRC).toContain('when the reservation itself fails the request proceeds and an orphan');
+  });
+
+  it('control KS-1666 C3 the file was read (the instrument is not reading an empty string)', () => {
+    expect(SRC.length).toBeGreaterThan(3000);
+  });
+});
```
