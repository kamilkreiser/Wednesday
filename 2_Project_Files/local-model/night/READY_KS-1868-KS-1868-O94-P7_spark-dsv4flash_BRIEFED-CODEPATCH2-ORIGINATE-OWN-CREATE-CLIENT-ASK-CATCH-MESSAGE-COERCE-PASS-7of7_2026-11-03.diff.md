# READY — KS-1868-KS-1868-O94-P7 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p7_originate_own_create_client_ask_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 12:32 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p7_originate_own_create_client_ask_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p7_originate_own_create_client_ask_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p7_originate_own_create_client_ask_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p7_originate_own_create_client_ask_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:32 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p7_originate_own_create_client_ask_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7f24c8124ec4985642db29c109f47a45708fbaba`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/ownCreateClient.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/ownCreateClient.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/originate/src/services/ownCreateClient.ts
56	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: ownCreateClient.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/ownCreateClient.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/ownCreateClient.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts 56 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/ownCreateClient.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (1 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=1 of total=3; red cell(s): ['KS-1868 askOwnCreate reads the thrown value safely RED ks1868 R1 an Error whose message getter throws is not-answered with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2385 failed=11 | after: total=2393 failed=11` · `NEW reds: []` [baseline_suite.json total=2385 failed=11; after_suite.json total=2393 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/ownCreateClient.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts` (+56/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/ownCreateClient.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7f24c8124ec4985642db29c109f47a45708fbaba` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p7_originate_own_create_client_ask_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p7_originate_own_create_client_ask_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p7_originate_own_create_client_ask_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/ownCreateClient.ts b/Blockchain/Dev/services/originate/src/services/ownCreateClient.ts
--- a/Blockchain/Dev/services/originate/src/services/ownCreateClient.ts
+++ b/Blockchain/Dev/services/originate/src/services/ownCreateClient.ts
@@ -85,6 +85,12 @@
     return readOwnCreateBody(body);
   } catch (err: unknown) {
     if (isTimeoutError(err)) return notAnswered('deadline', `own-create did not answer within ${OWN_CREATE_CALL_TIMEOUT_MS} ms`);
-    return notAnswered('unanswered', `own-create could not be reached: ${err instanceof Error ? err.message : String(err)}`);
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    return notAnswered('unanswered', `own-create could not be reached: ${reason}`);
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts
@@ -0,0 +1,56 @@
+// KS-1868: askOwnCreate (src/services/ownCreateClient.ts) is documented "Never throws": every way the call can fail is a `not-answered` answer,
+// which the resolver turns into "write nothing" and the retry route into a 503 with no POST. Its catch reads
+// `err instanceof Error ? err.message : String(err)` inside a template literal, unguarded. An Error whose `message` getter throws makes the catch
+// throw, so askOwnCreate REJECTS where an ordinary Error gives `not-answered` with the reason. (A revoked Proxy is not a cell here: it already throws
+// one call earlier, in `isTimeoutError`, which another pass guards.)
+// The fetch stand-in is a plain function, not jest.fn(): a spy inspects what it rejects with and could itself fail on a throwing value first.
+import { askOwnCreate } from '../services/ownCreateClient';
+
+const question = { documentId: 'doc-1', contentHash: 'sha256:' + 'a'.repeat(64), timestamps: ['2026-01-01T00:00:00.000Z'] };
+
+const rejecting = (value: unknown): typeof fetch => ((..._args: unknown[]) => Promise.reject(value)) as unknown as typeof fetch;
+
+/** The answer, or the string 'rejected' when askOwnCreate rejects (an assertion can then fail on it). */
+async function ask(value: unknown): Promise<unknown> {
+  try {
+    return await askOwnCreate(rejecting(value), 'http://anchoring.test', 'Bearer t', question);
+  } catch {
+    return 'rejected';
+  }
+}
+
+describe('KS-1868 askOwnCreate reads the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error is not-answered with its message', async () => {
+    expect(await ask(new Error('connection reset'))).toEqual({
+      outcome: 'not-answered',
+      kind: 'unanswered',
+      reason: 'own-create could not be reached: connection reset',
+      loose: [],
+    });
+  });
+
+  it('control ks1868 C2 a thrown plain string is not-answered with the text', async () => {
+    expect(await ask('plain text failure')).toEqual({
+      outcome: 'not-answered',
+      kind: 'unanswered',
+      reason: 'own-create could not be reached: plain text failure',
+      loose: [],
+    });
+  });
+
+  it('RED ks1868 R1 an Error whose message getter throws is not-answered with a constant reason', async () => {
+    const hostile = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    expect(await ask(hostile)).toEqual({
+      outcome: 'not-answered',
+      kind: 'unanswered',
+      reason: 'own-create could not be reached: unreadable thrown value',
+      loose: [],
+    });
+  });
+});
```
