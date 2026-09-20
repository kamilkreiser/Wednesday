# READY — KS-1203-UNTYPED-1 (Ornith, briefed, test_only, vitest) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1203-ornith35b-night/out.md.checker/patch.diff`** (read from `ls` of that dir at 17:04, not copied from a previous READY).

> ⚠ **APPLIES WITH `--recount`, NOT STRICT.** The model's hunk header is miscounted: `@@ -64,1 +64,8 @@` declares new=8, actual new=9. The checker applied it with `--recount` and graded it PASS on that basis. **The raise seat must apply the canonical patch the same way and say so in the PR** — do not claim a strict apply.

**Held 17:04 2026-09-20 by the 16:0x Wednesday seat after a source read.** Tip `e470198783bcb1ef0eac94780f87579974051423`. ONE file, test-only, **zero product bytes**: adds one cell to `Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts`.

**What it pins.** KS-1203's load-bearing premise is that a connector restricted by `allowedDocumentTypes` can still create the default DOCUMENT type by sending no type at all — and the suite is blind to it today. The cell drives untyped body shapes through `enforceDocumentTypeRules` and asserts the catalogue is never consulted. **It pins the CURRENT behaviour; it does not fix the ticket**, so it is raised as **`Refs KS-1203`, never a closing word.**

**Source read (Wednesday, same action as this file):** the model's 8 `+` lines are **byte-identical** to the brief's; exactly one file touched; no product file.

**Checked by Wednesday at source BEFORE the brief was queued:** fence context `:64` == `});` byte-exact **with a shifted control** (`:63` is `  });`, which does not match); both control titles exact and unique at `:53` and `:58`; both tamper `From` lines byte-exact at `:100` and `:116`. **One discrepancy found and NOT waved through: `:116`'s text is not unique — it also sits at `:136`.** The brief named it; the BUILDER accepted it (a single-line tamper plants by line index after a byte check at that number), and the builder is the authority on its own contract. Recorded so the next reader does not re-derive it as ambiguity.

**Adjacency, ruled:** `allowedDocumentTypes` is thematically adjacent to the live seat's `ks1230-settings-write-validates-allowed-document-types.test.ts` on #1100/#1101. **No file overlap and no product-file overlap** — the partition here is by PATH, which is the checkable one.

**HELD. Not raised.** Raise only after #1100/#1101 land, so develop is not moving under it.

---
## Checker verdict (verbatim tail)
tamper SPELLINGSHONOURED: planted SPELLINGSHONOURED at Blockchain/Dev/services/api-gateway/src/services/enforcement.ts:100 (10708 -> 10764 bytes; sha256 ee05d9c6c99f)
PASS T8[SPELLINGSHONOURED] Blockchain/Dev/services/api-gateway/src/services/enforcement.ts restored by bytes: sha256 69709f07956e == tip blob, git diff --quiet rc 0
PASS T6[SPELLINGSHONOURED] red set == declared exactly: {RED KS-1203: a body carrying no resolvable documentType admi}, every red an assertion failure
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

## Diff
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
