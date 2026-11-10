# READY — KS-1954-KS-1954-O131-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1954_o131_p1_transfer_escalation_sweep_leaves_a_step_pending_when_its_workflow_cannot_be_read/out.md.checker/patch.diff`** (from `ls` at 13:41 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1954_o131_p1_transfer_escalation_sweep_leaves_a_step_pending_when_its_workflow_cannot_be_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1954_o131_p1_transfer_escalation_sweep_leaves_a_step_pending_when_its_workflow_cannot_be_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1954_o131_p1_transfer_escalation_sweep_leaves_a_step_pending_when_its_workflow_cannot_be_read/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1954_o131_p1_transfer_escalation_sweep_leaves_a_step_pending_when_its_workflow_cannot_be_read-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:41 2026-11-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1954_o131_p1_transfer_escalation_sweep_leaves_a_step_pending_when_its_workflow_cannot_be_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d3e663692a8f414f16610236259cab14b27ff0f7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts } + { Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts` (product) and `Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts
127	0	Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (2 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: approvalWorkflowService.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts`; test(s): `Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts 127 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1954 the escalation sweep leaves a step pending when its workflow cannot be read RED ks1954 R1 with the workflow reads failing, an overdue escalating step is not counted as timed out', 'KS-1954 the escalation sweep leaves a step pending when its workflow cannot be read RED ks1954 R2 with the workflow reads failing, the step is not written as timed_out and stays pending', 'KS-1954 the escalation sweep leaves a step pending when its workflow cannot be read RED ks1954 R3 a sweep that could not read the workflows can be repaired by the next sweep, which then escalates']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=466 failed=0 | after: total=471 failed=0` · `NEW reds: []` [baseline_suite.json total=466 failed=0; after_suite.json total=471 failed=0]
- A6 [verbatim]: `PASS A6 whole services/transfer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/transfer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts` (+127/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d3e663692a8f414f16610236259cab14b27ff0f7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1954_o131_p1_transfer_escalation_sweep_leaves_a_step_pending_when_its_workflow_cannot_be_read/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1954_o131_p1_transfer_escalation_sweep_leaves_a_step_pending_when_its_workflow_cannot_be_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts b/Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts
--- a/Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts
+++ b/Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts
@@ -621,3 +621,5 @@
         const instance = rowToStepInstance(row);
         const workflow = await this.findWorkflowByStepId(instance.stepId);
+        // KS-1954: a step whose workflow cannot be found (the workflow reads failed) is left pending, never marked timed_out (terminal).
+        if (!workflow) continue;
         const stepDef = workflow?.steps.find(s => s.id === instance.stepId);
diff --git a/Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts b/Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/transfer/src/__tests__/ks1954-the-escalation-sweep-leaves-a-step-pending-when-its-workflow-cannot-be-read.test.ts
@@ -0,0 +1,127 @@
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+
+// KS-1954: the escalation sweep (processEscalations) looks up each overdue step's workflow. When the workflow reads fail, the workflow
+// is undefined, so the step is treated as "no escalation configured" and marked timed_out. timed_out is terminal (a later sweep selects
+// only pending steps), so an escalation the step was configured for is lost and running the sweep again cannot repair it. A step whose
+// workflow cannot be found must be left pending. Harness: the real module with ../db replaced by an in-memory model of the two tables
+// (a SELECT of pending step instances, the workflow reads, and the INSERT ... ON CONFLICT upsert that applies a step's new state) and
+// ./delegationService replaced by a plain stand-in. No database.
+const h = vi.hoisted(() => ({
+  workflowReads: 'ok' as 'ok' | 'fail',
+  rows: [] as any[],
+  inserts: [] as unknown[][],
+}));
+
+const WORKFLOW_ROW = {
+  id: 'wf-ks1954',
+  name: 'KS-1954 workflow',
+  workflow_type: 'single',
+  steps: [
+    { id: 'ks1954-esc', order: 0, name: 'Escalating step', approverType: 'user', approverId: 'u-first', requireSignature: false, requireComment: false, requireWalletVerification: false, isParallel: false, timeoutHours: 1, autoEscalate: true, escalateTo: 'boss-user' },
+    { id: 'ks1954-plain', order: 1, name: 'Plain step', approverType: 'user', approverId: 'u-second', requireSignature: false, requireComment: false, requireWalletVerification: false, isParallel: false, autoEscalate: false },
+  ],
+  created_by: 'tester',
+  created_at: new Date('2026-01-01T00:00:00Z'),
+  updated_at: new Date('2026-01-01T00:00:00Z'),
+  is_active: true,
+};
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: async (sql: string, params?: unknown[]) => {
+    const text = String(sql);
+    if (/FROM svc_approval_step_instances/.test(text)) {
+      const pending = h.rows.filter((r) => r.status === 'pending');
+      return { rows: pending, rowCount: pending.length };
+    }
+    if (/FROM svc_approval_workflows/.test(text)) {
+      if (h.workflowReads === 'fail') throw new Error('workflow read failed');
+      return { rows: [WORKFLOW_ROW], rowCount: 1 };
+    }
+    if (/INSERT INTO svc_approval_step_instances/.test(text)) {
+      const p = params || [];
+      h.inserts.push(p);
+      const row = h.rows.find((r) => r.id === p[0]);
+      if (row) {
+        row.status = p[3];
+        row.assigned_to = p[4];
+        row.escalated_to = p[15];
+      }
+      return { rows: [], rowCount: 1 };
+    }
+    return { rows: [], rowCount: 0 };
+  },
+}));
+vi.mock('../services/delegationService', () => ({ delegationService: {} }));
+
+type Mod = typeof import('../services/approvalWorkflowService');
+let mod: Mod;
+const realError = console.error;
+
+function overdue(id: string, stepId: string) {
+  return {
+    id,
+    step_id: stepId,
+    transfer_id: 'transfer-' + id,
+    status: 'pending',
+    assigned_to: 'u-first',
+    assigned_at: new Date('2026-01-01T00:00:00Z'),
+    due_at: new Date('2026-01-01T01:00:00Z'),
+  };
+}
+
+beforeEach(async () => {
+  mod = await import('../services/approvalWorkflowService');
+  h.workflowReads = 'ok';
+  h.rows = [];
+  h.inserts.length = 0;
+  console.error = () => undefined;
+});
+
+describe('KS-1954 the escalation sweep leaves a step pending when its workflow cannot be read', () => {
+  it('RED ks1954 R1 with the workflow reads failing, an overdue escalating step is not counted as timed out', async () => {
+    h.workflowReads = 'fail';
+    h.rows = [overdue('i1', 'ks1954-esc')];
+    const out = await mod.approvalWorkflowService.processEscalations();
+    console.error = realError;
+    expect(out).toEqual({ escalatedCount: 0, timedOutCount: 0 });
+  });
+
+  it('RED ks1954 R2 with the workflow reads failing, the step is not written as timed_out and stays pending', async () => {
+    h.workflowReads = 'fail';
+    h.rows = [overdue('i1', 'ks1954-esc'), overdue('i2', 'ks1954-plain')];
+    await mod.approvalWorkflowService.processEscalations();
+    console.error = realError;
+    expect(h.inserts.filter((p) => p[3] === 'timed_out')).toHaveLength(0);
+    expect(h.rows.map((r) => r.status)).toEqual(['pending', 'pending']);
+  });
+
+  it('RED ks1954 R3 a sweep that could not read the workflows can be repaired by the next sweep, which then escalates', async () => {
+    h.rows = [overdue('i1', 'ks1954-esc')];
+    h.workflowReads = 'fail';
+    await mod.approvalWorkflowService.processEscalations();
+    h.workflowReads = 'ok';
+    const second = await mod.approvalWorkflowService.processEscalations();
+    console.error = realError;
+    expect(second).toEqual({ escalatedCount: 1, timedOutCount: 0 });
+    expect(h.rows[0].assigned_to).toBe('boss-user');
+  });
+
+  it('control ks1954 C1 with the workflow readable, an overdue step set to escalate is escalated to the named user', async () => {
+    h.rows = [overdue('i1', 'ks1954-esc')];
+    const out = await mod.approvalWorkflowService.processEscalations();
+    console.error = realError;
+    expect(out).toEqual({ escalatedCount: 1, timedOutCount: 0 });
+    expect(h.rows[0].status).toBe('pending');
+    expect(h.rows[0].assigned_to).toBe('boss-user');
+    expect(h.rows[0].escalated_to).toBe('boss-user');
+  });
+
+  it('control ks1954 C2 with the workflow readable, an overdue step not set to escalate is marked timed_out', async () => {
+    h.rows = [overdue('i2', 'ks1954-plain')];
+    const out = await mod.approvalWorkflowService.processEscalations();
+    console.error = realError;
+    expect(out).toEqual({ escalatedCount: 0, timedOutCount: 1 });
+    expect(h.rows[0].status).toBe('timed_out');
+  });
+});
```
