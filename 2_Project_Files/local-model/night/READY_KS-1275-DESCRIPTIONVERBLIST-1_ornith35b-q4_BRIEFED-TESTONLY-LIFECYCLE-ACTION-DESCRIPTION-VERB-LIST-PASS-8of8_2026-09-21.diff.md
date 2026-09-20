# READY — KS-1275-DESCRIPTIONVERBLIST-1 (Ornith, briefed, test_only, modify · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1275-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 09:28 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1275-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1112rows-drafter-precheck/DESCRIPTIONVERBLIST/out.md.checker/patch.diff` rc 0, Wednesday (the 08:4x seat)).

**Held 09:28 2026-09-21 by Wednesday (the 08:4x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1275-ornith35b-night2/out.md.checker`, not typed).** Tip `7be81d5c9b109959b559e03652fb092c12de58e8`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts` (modify). `+` lines 9 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 12/12 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `VERBLISTSTALE` → red exactly ['RED KS-1275 DESCRIPTIONVERBLIST: the registered LifecycleEve']
- `VERBWITHOUTROUTE` → red exactly ['RED KS-1275 DESCRIPTIONVERBLIST: the registered LifecycleEve']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1275-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1275-DESCRIPTIONVERBLIST-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1275-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts
@@ -146,4 +146,13 @@
     const published = (refId: string) => defs.filter((d) => d.type === 'schema' && d.schema?._def?.openapi?._internal?.refId === refId).map((d) => d.schema.shape.action.options);
     expect([published('LifecycleEventRequest'), published('LifecycleEventResponse')]).toEqual([[[...LIFECYCLE_EVENT_ACTIONS]], [[...LIFECYCLE_EVENT_ACTIONS]]]);
   });
+  it('RED KS-1275 DESCRIPTIONVERBLIST: the registered LifecycleEventRequest action description names exactly share, transfer-custody and revoke as the verbs with their own routes - each has a registered POST /api/documents/{id}/<verb> route and none is accepted by LIFECYCLE_EVENT_ACTIONS', async () => {
+    const { LIFECYCLE_EVENT_ACTIONS } = await import('../lifecycleActions');
+    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
+    const request = defs.find((d) => d.type === 'schema' && d.schema?._def?.openapi?._internal?.refId === 'LifecycleEventRequest');
+    const description = String(request?.schema?.shape?.action?._def?.openapi?.metadata?.description ?? '');
+    const verbs = (description.split(' etc.')[0].split(' ').pop() ?? '').split('/');
+    const dedicated = (verb: string) => defs.some((d) => d.type === 'route' && d.route?.method === 'post' && d.route?.path === '/api/documents/{id}/' + verb);
+    expect([verbs, verbs.filter((verb) => !dedicated(verb)), verbs.filter((verb) => (LIFECYCLE_EVENT_ACTIONS as readonly string[]).includes(verb))]).toEqual([['share', 'transfer-custody', 'revoke'], [], []]);
+  });
 });
```
