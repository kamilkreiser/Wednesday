# READY — KS-1364-TEAMSWEBHOOKNOTIFY-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-teams-webhook-notify/out.md.checker/patch.diff`** (from `ls` at 03:25 2026-10-08; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-teams-webhook-notify/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-teams-webhook-notify/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 03:25 2026-10-08 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-teams-webhook-notify/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `46c3e20cfbd21acee0c67d544180c33deaa4c8ef`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts , Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-teams-webhook-config-notify-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-teams-webhook-config-notify-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
58	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-teams-webhook-config-notify-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-teams-webhook-config-notify-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1364-teams-webhook-config-notify-body-required.test.ts fails at the untouched tip (2 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=2 of total=6; red cell(s): ['KS-1364: the two Teams POSTs publish a REQUIRED request body RED KS-1364 TW1: POST /api/teams/webhook-config marks its request body required', 'KS-1364: the two Teams POSTs publish a REQUIRED request body RED KS-1364 TW2: POST /api/teams/notify marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1364-teams-webhook-config-notify-body-required.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=57 failed=0 | after: total=63 failed=0` · `NEW reds: []` [baseline_suite.json total=57 failed=0; after_suite.json total=63 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +60/-2 test=src/__tests__/ks1364-teams-webhook-config-notify-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-teams-webhook-config-notify-body-required.test.ts` (+58/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `46c3e20cfbd21acee0c67d544180c33deaa4c8ef` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-teams-webhook-notify/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-teams-webhook-notify/checker.out`.

```diff
--- a/Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
+++ b/Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
@@ -861,7 +861,7 @@
   summary: 'Register a Teams incoming webhook for notifications',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: M365TeamsWebhookConfigRequestSchema } } },
+    body: { content: { 'application/json': { schema: M365TeamsWebhookConfigRequestSchema } }, required: true },
   },
   responses: {
     201: {
@@ -958,7 +958,7 @@
     'lifecycle events (certified / revoked / verified).',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: M365TeamsNotifyRequestSchema } } },
+    body: { content: { 'application/json': { schema: M365TeamsNotifyRequestSchema } }, required: true },
   },
   responses: {
     200: {
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-teams-webhook-config-notify-body-required.test.ts
@@ -0,0 +1,58 @@
+// KS-1364 (85 request bodies not marked required): the published contracts for POST /api/teams/webhook-config and
+// POST /api/teams/notify did not mark the request body required, so a spec-driven caller (Schemathesis) may send no
+// body at all. Both handlers (index.ts) refuse an absent body with 400: webhook-config parses it with
+// teamsWebhookSchema (channelName and webhookUrl required), notify with teamsNotifyRequestSchema (event required,
+// non-empty). So the spec now says each body is required - the one-line shape the KS-1364 m365 carves landed. This
+// file renders the document the generator publishes, from the shared registry the m365-integration module populates
+// on import, and runs the notify validator itself. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../m365-integration.openapi';
+import { teamsNotifyRequestSchema } from '../teamsNotifyRequest';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'm365-integration (ks1364 teams pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string): string | undefined {
+  return operation(path, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-1364: the two Teams POSTs publish a REQUIRED request body', () => {
+  it('RED KS-1364 TW1: POST /api/teams/webhook-config marks its request body required', () => {
+    expect(operation('/api/teams/webhook-config', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 TW2: POST /api/teams/notify marks its request body required', () => {
+    expect(operation('/api/teams/notify', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 TWC1: both bodies keep their request schemas and their bearerAuth', () => {
+    expect({ config: bodyRef('/api/teams/webhook-config'), notify: bodyRef('/api/teams/notify') }).toEqual({
+      config: '#/components/schemas/M365TeamsWebhookConfigRequest',
+      notify: '#/components/schemas/M365TeamsNotifyRequest',
+    });
+    expect(operation('/api/teams/webhook-config', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/teams/notify', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+  });
+
+  it('control KS-1364 TWC2: the notify validator the handler runs refuses an absent body (it arrives as {})', () => {
+    expect(teamsNotifyRequestSchema.safeParse({}).success).toBe(false);
+    expect(teamsNotifyRequestSchema.safeParse({ event: 'certified' }).success).toBe(true);
+  });
+
+  it('control KS-1364 TWC3: the request components still list their required fields', () => {
+    const s: AnyObj = doc.components?.schemas ?? {};
+    expect(s.M365TeamsWebhookConfigRequest?.required).toEqual(expect.arrayContaining(['channelName', 'webhookUrl']));
+    expect(s.M365TeamsNotifyRequest?.required).toEqual(expect.arrayContaining(['event']));
+  });
+
+  it('control KS-1364 TWC4: the GET /api/teams/webhook-config list stays bodiless and the landed m365 carve keeps its required body', () => {
+    expect(operation('/api/teams/webhook-config', 'get')?.requestBody).toBeUndefined();
+    expect(operation('/api/m365/sites', 'post')?.requestBody?.required).toBe(true);
+  });
+});
```

**Appended by Wednesday 03:25 2026-10-08 (not written by hold_ready):** REVIEWED HOLD on 2026-10-05 (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-teams-webhook-notify/REVIEW.md`) but never held until now; classed UNRAISED by `0_Brain/reference/2026-10-08_spark-hold-census/CENSUS.md` (forward strict apply at develop eae08a3f441c, reverse refuses, no open PR). Read the REVIEW body for any raise caveat (the census read only its verdict line). Any YAML companion is in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-teams-webhook-notify/`. Raise is blocked until develop is green on pre-push leg 14 (pickup 03:1x).
