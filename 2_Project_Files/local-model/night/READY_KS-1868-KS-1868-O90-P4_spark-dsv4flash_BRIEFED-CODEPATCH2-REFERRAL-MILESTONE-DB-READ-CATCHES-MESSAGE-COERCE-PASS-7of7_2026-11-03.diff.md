# READY — KS-1868-KS-1868-O90-P4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 05:20 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 05:20 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4307ac876caea7d1835b17d6360760b7ec6e6bbe`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/referral/src/services/milestoneService.ts } + { Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/referral/src/services/milestoneService.ts` (product) and `Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	3	Blockchain/Dev/services/referral/src/services/milestoneService.ts
133	0	Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (24 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: milestoneService.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/referral/src/services/milestoneService.ts`; test(s): `Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/referral/src/services/milestoneService.ts 24 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts 133 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/referral/src/services/milestoneService.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 milestone service: the three DB read catches survive a thrown value they cannot read RED ks1868 R1: a revoked Proxy from the progress read is logged as text and the fresh default progress is answered', 'KS-1868 milestone service: the three DB read catches survive a thrown value they cannot read RED ks1868 R2: an Error whose message getter throws from the progress read is logged as text and the fresh default progress is answered', 'KS-1868 milestone service: the three DB read catches survive a thrown value they cannot read RED ks1868 R3: a revoked Proxy from the pending-rewards read is logged as text and an empty list is answered', 'KS-1868 milestone service: the three DB read catches survive a thrown value they cannot read RED ks1868 R4: an Error whose message getter throws from the pending-rewards read is logged as text and an empty list is answered', 'KS-1868 milestone service: the three DB read catches survive a thrown value they cannot read RED ks1868 R5: a revoked Proxy from the table verification is logged as text and the call resolves', 'KS-1868 milestone service: the three DB read catches survive a thrown value they cannot read RED ks1868 R6: an Error whose message getter throws from the table verification is logged as text and the call resolves']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=36 failed=0 | after: total=45 failed=0` · `NEW reds: []` [baseline_suite.json total=36 failed=0; after_suite.json total=45 failed=0]
- A6 [verbatim]: `PASS A6 whole services/referral suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/referral: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/referral/src/services/milestoneService.ts` (+24/-3 per numstat.out) and the test file `Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts` (+133/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/referral/src/services/milestoneService.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4307ac876caea7d1835b17d6360760b7ec6e6bbe` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/referral/src/services/milestoneService.ts b/Blockchain/Dev/services/referral/src/services/milestoneService.ts
--- a/Blockchain/Dev/services/referral/src/services/milestoneService.ts
+++ b/Blockchain/Dev/services/referral/src/services/milestoneService.ts
@@ -121,7 +121,14 @@
       const r = result.rows[0];
       return this.rowToProgress(r);
     } catch (err: any) {
-      logger.error('DB read user progress failed', { userId, error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB read user progress failed', { userId, error: reason });
       return null;
     }
   }
@@ -156,7 +163,14 @@
       }));
     } catch (err: any) {
       // Table may not exist yet — fall back gracefully
-      logger.error('DB read pending rewards failed', { userId, error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB read pending rewards failed', { userId, error: reason });
       return [];
     }
   }
@@ -235,6 +249,13 @@
       const result = await query('SELECT COUNT(*) AS cnt FROM svc_referral_milestones');
       logger.info('Milestone DB verified', { rows: result.rows[0]?.cnt });
     } catch (err: any) {
-      logger.warn('Milestone table verification failed — table may need migration', { error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.warn('Milestone table verification failed — table may need migration', { error: reason });
     }
   }
diff --git a/Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts
@@ -0,0 +1,133 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868 (operator 90 screen, referral milestone service): three catch blocks of services/referral/src/services/milestoneService.ts
+// pass `err?.message` straight into the logger's meta object, unguarded: dbGetUserProgress (line 124), dbGetPendingRewards (line 159)
+// and verifyDbReady (line 238). `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error
+// whose message getter throws) makes the catch throw, so the public method REJECTS where an ordinary Error gets a logged failure and
+// the fallback (a fresh default progress, an empty reward list, a resolved verification). The cells make the database stand-in
+// reject with such a value and assert the method still resolves with the fallback and the failure is logged as text. The stand-in
+// rejects with a plain function, not vi.fn(): a spy could inspect a revoked Proxy and fail before the code under test saw it.
+// Harness: the real module with ../db and ../utils/logger replaced by plain stand-ins; no database, no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (..._args: unknown[]) => Promise.reject(h.toThrow),
+}));
+
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logs.push({ level, message, meta });
+  };
+  return { createLogger: () => ({ debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') }) };
+});
+
+import { milestoneService } from '../services/milestoneService';
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logs.length = 0;
+});
+
+const LOG = (prefix: string) => h.logs.filter((l) => l.message.startsWith(prefix));
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta?: Record<string, unknown> } | undefined): string => {
+  const e = l?.meta?.error;
+  return typeof e === 'string' ? e : '<' + typeof e + '>';
+};
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+const PROGRESS = 'DB read user progress failed';
+const PENDING = 'DB read pending rewards failed';
+const VERIFY = 'Milestone table verification failed';
+
+async function progressWith(value: unknown): Promise<{ threw: boolean; userId?: string; qualified?: number }> {
+  h.toThrow = value;
+  try {
+    const p = await milestoneService.getUserProgress('user-ks1868');
+    return { threw: false, userId: p.userId, qualified: p.qualifiedReferrals };
+  } catch {
+    return { threw: true };
+  }
+}
+async function pendingWith(value: unknown): Promise<{ threw: boolean; rewards?: unknown[] }> {
+  h.toThrow = value;
+  try {
+    return { threw: false, rewards: await milestoneService.getPendingRewards('user-ks1868') };
+  } catch {
+    return { threw: true };
+  }
+}
+async function verifyWith(value: unknown): Promise<{ threw: boolean }> {
+  h.toThrow = value;
+  try {
+    await milestoneService.verifyDbReady();
+    return { threw: false };
+  } catch {
+    return { threw: true };
+  }
+}
+
+describe('KS-1868 milestone service: the three DB read catches survive a thrown value they cannot read', () => {
+  it('control ks1868 C1: an ordinary Error from the progress read is logged with its message and the fresh default progress is answered', async () => {
+    expect(await progressWith(new Error('db boom'))).toEqual({ threw: false, userId: 'user-ks1868', qualified: 0 });
+    expect(LOG(PROGRESS)).toHaveLength(1);
+    expect(reasonOf(LOG(PROGRESS)[0])).toBe('db boom');
+  });
+  it('control ks1868 C2: an ordinary Error from the pending-rewards read is logged with its message and an empty list is answered', async () => {
+    expect(await pendingWith(new Error('db boom'))).toEqual({ threw: false, rewards: [] });
+    expect(LOG(PENDING)).toHaveLength(1);
+    expect(reasonOf(LOG(PENDING)[0])).toBe('db boom');
+  });
+  it('control ks1868 C3: an ordinary Error from the table verification is logged with its message and the call resolves', async () => {
+    expect(await verifyWith(new Error('db boom'))).toEqual({ threw: false });
+    expect(LOG(VERIFY)).toHaveLength(1);
+    expect(reasonOf(LOG(VERIFY)[0])).toBe('db boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the progress read is logged as text and the fresh default progress is answered', async () => {
+    expect(await progressWith(revokedProxy())).toEqual({ threw: false, userId: 'user-ks1868', qualified: 0 });
+    expect(LOG(PROGRESS)).toHaveLength(1);
+    expect(reasonOf(LOG(PROGRESS)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws from the progress read is logged as text and the fresh default progress is answered', async () => {
+    expect(await progressWith(getterThrows())).toEqual({ threw: false, userId: 'user-ks1868', qualified: 0 });
+    expect(LOG(PROGRESS)).toHaveLength(1);
+    expect(reasonOf(LOG(PROGRESS)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: a revoked Proxy from the pending-rewards read is logged as text and an empty list is answered', async () => {
+    expect(await pendingWith(revokedProxy())).toEqual({ threw: false, rewards: [] });
+    expect(LOG(PENDING)).toHaveLength(1);
+    expect(reasonOf(LOG(PENDING)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: an Error whose message getter throws from the pending-rewards read is logged as text and an empty list is answered', async () => {
+    expect(await pendingWith(getterThrows())).toEqual({ threw: false, rewards: [] });
+    expect(LOG(PENDING)).toHaveLength(1);
+    expect(reasonOf(LOG(PENDING)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: a revoked Proxy from the table verification is logged as text and the call resolves', async () => {
+    expect(await verifyWith(revokedProxy())).toEqual({ threw: false });
+    expect(LOG(VERIFY)).toHaveLength(1);
+    expect(reasonOf(LOG(VERIFY)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R6: an Error whose message getter throws from the table verification is logged as text and the call resolves', async () => {
+    expect(await verifyWith(getterThrows())).toEqual({ threw: false });
+    expect(LOG(VERIFY)).toHaveLength(1);
+    expect(reasonOf(LOG(VERIFY)[0])).toBe('unreadable thrown value');
+  });
+});
```
