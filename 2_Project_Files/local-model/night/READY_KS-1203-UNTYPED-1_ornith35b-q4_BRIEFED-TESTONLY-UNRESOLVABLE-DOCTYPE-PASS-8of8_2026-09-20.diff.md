# READY — KS-1203-UNTYPED-1 (Ornith, briefed, test_only, vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1203-ornith35b-night/out.md.checker/patch.diff`** (from `ls` of that dir at 17:05). **Use it, not the quoted diff below** — see the --recount note.

**Held 17:05 2026-09-20 by the 16:0x Wednesday seat after a source read.** Tip `e470198783bcb1ef0eac94780f87579974051423`. ONE file, test-only, **zero product bytes**: adds one cell to `Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts`.

**Source read (Wednesday, same action as this file):** the model's 8 `+` lines are **byte-identical** to the brief's; exactly one file touched; no product file.

**Checker result:** PASS 8/8. Both tampers red **exactly their declared cell** and every control stayed green under both; both tamper files restored byte-for-byte to the tip blob (`sha256 69709f07956e == tip blob, git diff --quiet rc 0`).

⚠ **APPLY WITH THE CANONICAL PATCH, NOT THE QUOTED DIFF.** The checker recorded `apply=--recount (miscounted header: hunk @@ -64,1 +64,8 @@ declared old=1 new=8 actual old=1 new=9)`. The model's hunk header undercounts its own added lines by one — a known Ornith weakness, named in the 2026-09-14 head-to-head. The harness accepted it under `--recount`; **a human or a seat applying the quoted text with plain `git apply` will fail.** The raise seat applies `patch.diff` from the run dir and states the deviation in the PR.

⚠ **WEDNESDAY'S RULING FOR THE RAISE: `Refs KS-1203`, never a closing word.** This cell pins today's behaviour; it does not complete the ticket.

**Provenance note on the brief:** its second tamper's `from` line text is **NOT unique** in the file — it recurs about twenty lines further down. The brief flagged it and the builder accepted it, because a single-line tamper plants by line index after a byte check at that index. **Stated rather than buried:** the plant is correct here, and the general rule stands that a tamper `from` should be unique or explicitly pinned by line.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[SPELLINGSHONOURED] every control green under the tamper
tamper UNTYPEDGETSADEFAULT: planted UNTYPEDGETSADEFAULT at Blockchain/Dev/services/api-gateway/src/services/enforcement.ts:116 (10708 -> 10743 bytes; sha256 bc70ed4eef2f)
PASS T8[UNTYPEDGETSADEFAULT] Blockchain/Dev/services/api-gateway/src/services/enforcement.ts restored by bytes: sha256 69709f07956e == tip blob, git diff --quiet rc 0
PASS T6[UNTYPEDGETSADEFAULT] red set == declared exactly: {RED KS-1203: a body carrying no resolvable documentType admi}, every red an assertion failure
PASS T7[UNTYPEDGETSADEFAULT] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts mode=modify runner=vitest cells=7 tampers=2 apply=--recount (miscounted header: hunk @@ -64,1 +64,8 @@ declared old=1 new=8 actual old=1 new=9 )
RESULT: PASS (8/8)

## Diff (reference only — apply the canonical patch)
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts
@@ -64,1 +64,8 @@
+  it('RED KS-1203: a body carrying no resolvable documentType admits with an EMPTY docType and never consults the catalogue', async () => {
+    const untypedShapes = [{}, { documentType: '' }, { type: '' }, { DocumentType: 'SSD_DOCUMENT' }, { document_type: 'SSD_DOCUMENT' }, { Type: 'SSD_DOCUMENT' }, { data: { title: 'no type here' } }];
+    for (const body of untypedShapes) {
+      const result = await enforceDocumentTypeRules(body, undefined);
+      expect([result.ok, (result as { docType?: unknown }).docType]).toEqual([true, {}]);
+    }
+    expect(redisService.getAllDocumentTypes).not.toHaveBeenCalled();
+  });
 });
```
