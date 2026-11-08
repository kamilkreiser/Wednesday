# READY - KS-2134-KS-2134-O110-P1 (spark-dsv4flash, briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2134_o110_p1_social_token_pins_mixed_case_and_github_second_send/out.md.checker/patch.diff` (from `ls` at 08:13 2026-11-09; sha256[:16] 8c9db585a12674ec, 2283 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 08:13 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2134_o110_p1_social_token_pins_mixed_case_and_github_second_send/out.md.checker`; product bytes were RE-MEASURED here.** Tip `425ea1d3df0fec9186f994d54b9da62beaf8f4e9`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/auth/src/__tests__/ks1858-a-usable-token-is-sent-exactly-as-the-provider-answered-it.test.ts']; `+` lines 29 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/auth/src/providers/social/github.ts` blob 4546ac7eca39; plant file(s) also unchanged.
- Red cells [input.json]:
  - `PIN KS-2134 case: a mixed-case answered token`
  - `PIN KS-2134 github second send`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/auth/src/__tests__/ks1858-a-usable-token-is-sent-exactly-as-the-provider-answered-it.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 2 red cell(s) exist and pass on the unmodified product; declared files 8 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1837 -> 1839, red 1 -> 0`
  - `PASS A5 RED WITH PLANT: 2 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/auth/src/providers/social/github.ts, Blockchain/Dev/services/auth/src/providers/social/google.ts), pass without it`
  - `PASS A7 RESTORE: 3 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks1858-a-usable-token-is-sent-exactly-as-the-provider-answered-it.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1858-a-usable-token-is-sent-exactly-as-the-provider-answered-it.test.ts
@@ -23,6 +23,8 @@
 /** A usable (visible) token with a leading and a trailing space: trim() would change it, the emptiness test must not. */
 const ANSWERED = ' tok-ks1858-f1 ';
 const PLAIN = 'tok-ks1858-plain';
+/** KS-2134: a token with upper-case letters, so a case-folding mutant on any adapter is visible (every other fixture is lower case). */
+const MIXED = 'Tok-KS1858-MiXeD';
 
 type Call = { url: string; init?: { headers?: Record<string, string> } };
 let calls: Call[];
@@ -90,4 +92,31 @@
     }
     expect(got).toEqual(ADAPTERS.map((a) => [a.name, expectedCarried(a, PLAIN)]));
   });
+
+  it('PIN KS-2134 case: a mixed-case answered token reaches the profile call with its case unchanged on all five', async () => {
+    const got: Array<[string, string | undefined]> = [];
+    for (const a of ADAPTERS) {
+      stubFetch(a, MIXED);
+      await a.make().exchangeCode('good');
+      got.push([a.name, carried(a)]);
+    }
+    expect(got).toEqual(ADAPTERS.map((a) => [a.name, expectedCarried(a, MIXED)]));
+  });
+
+  it('PIN KS-2134 github second send: the /user/emails call carries the answered token unchanged when the profile has no email', async () => {
+    const gh = ADAPTERS.find((a) => a.name === 'github')!;
+    calls = [];
+    vi.stubGlobal('fetch', vi.fn(async (url: string, init?: Call['init']) => {
+      const u = String(url);
+      calls.push({ url: u, init });
+      const body = gh.isToken(u) ? { access_token: ANSWERED }
+        : u.endsWith('/user/emails') ? [{ email: 'a@secuura.test', primary: true, verified: true }]
+        : gh.isProfile(u) ? { id: 7, name: 'Ada Lovelace', login: 'ada' }
+        : {};
+      return new Response(JSON.stringify(body), { status: 200, headers: { 'content-type': 'application/json' } });
+    }));
+    const profile = await gh.make().exchangeCode('good');
+    expect(profile.providerId).toBe('7');
+    expect(calls.filter((c) => c.url.endsWith('/user/emails')).map((c) => c.init?.headers?.Authorization)).toEqual([`Bearer ${ANSWERED}`]);
+  });
 });
```
