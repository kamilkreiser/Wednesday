# READY - KS-2158-KS-2158-O132-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2158_o132_p1_ks570_mount_auth_cells_read_the_upstream_hit_count_after_the_recorder_settles/out.md.checker/patch.diff` (from `ls` at 15:30 2026-11-10; sha256[:16] e40fe84bd4130c7c, 1186 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 15:30 2026-11-10 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2158_o132_p1_ks570_mount_auth_cells_read_the_upstream_hit_count_after_the_recorder_settles/out.md.checker`; product bytes were RE-MEASURED here.** Tip `0e6479d7b6c06b6f8a77aae1cbad167afbdaa089`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts']; `+` lines 3 (ASCII), `-` lines 1.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/api-gateway/src/index.ts` blob 98376c5c14e4; plant file(s) also unchanged.
- Red cells [input.json]:
  - `RED KS-2131 an unauthenticated GET /api/billing/bundles is refused 401 by the gateway's spec gate, with 0 upstream hits`
  - `RED KS-2131 an unauthenticated GET /api/nft/certificates is refused 401 by the gateway's spec gate, with 0 upstream hits`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 2 red cell(s) exist and pass on the unmodified product; declared files 18 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1886 -> 1886, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 2 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/api-gateway/src/index.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts
@@ -674,7 +674,9 @@ describe('KS-2131 the real gate refuses a GET with no credential under billing,
         res.on('end', () => {
           let code: string | null = null; let message: string | null = null;
           try { const e = JSON.parse(Buffer.concat(chunks).toString())?.error; code = typeof e === 'string' ? e : (e?.code ?? null); message = e?.message ?? null; } catch { /* not JSON: code and message stay null */ }
-          resolve({ status: res.statusCode ?? 0, code, message, hits: seen.filter((s) => s === tag).length });
+          // KS-2158 (gate 281 G281-2121-1): read the upstream hit count 500 ms AFTER the response ends. A gate that answers 401 and then still
+          // forwards reaches the recorder after the response, so a count taken at 'end' would stay 0 and every cell would stay green.
+          setTimeout(() => resolve({ status: res.statusCode ?? 0, code, message, hits: seen.filter((s) => s === tag).length }), 500);
         });
       });
       req.on('error', reject);
```
