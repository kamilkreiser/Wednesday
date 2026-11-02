# READY — KS-1868-KS-1868-O90-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message-r2/out.md.checker/patch.diff`** (from `ls` at 06:10 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 06:10 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4d1ab2cb6574e2b221353ac3a1de56d515711aaf`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/referral/src/services/milestoneService.ts } + { Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/referral/src/services/milestoneService.ts` (product) and `Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
18	2	Blockchain/Dev/services/referral/src/services/milestoneService.ts
111	0	Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (18 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: milestoneService.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/referral/src/services/milestoneService.ts`; test(s): `Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/referral/src/services/milestoneService.ts 18 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts 111 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/referral/src/services/milestoneService.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 milestone service: the two DB write catches survive a thrown value they cannot read RED ks1868 R1: a revoked Proxy from the reward save is logged as text and the award is still answered', 'KS-1868 milestone service: the two DB write catches survive a thrown value they cannot read RED ks1868 R2: an Error whose message getter throws from the reward save is logged as text and the award is still answered', 'KS-1868 milestone service: the two DB write catches survive a thrown value they cannot read RED ks1868 R3: a revoked Proxy from the progress save is logged as text and the award is still answered', 'KS-1868 milestone service: the two DB write catches survive a thrown value they cannot read RED ks1868 R4: an Error whose message getter throws from the progress save is logged as text and the award is still answered']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=36 failed=0 | after: total=42 failed=0` · `NEW reds: []` [baseline_suite.json total=36 failed=0; after_suite.json total=42 failed=0]
- A6 [verbatim]: `PASS A6 whole services/referral suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/referral: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/referral/src/services/milestoneService.ts` (+18/-2 per numstat.out) and the test file `Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts` (+111/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/referral/src/services/milestoneService.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4d1ab2cb6574e2b221353ac3a1de56d515711aaf` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message-r2/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/referral/src/services/milestoneService.ts b/Blockchain/Dev/services/referral/src/services/milestoneService.ts
--- a/Blockchain/Dev/services/referral/src/services/milestoneService.ts
+++ b/Blockchain/Dev/services/referral/src/services/milestoneService.ts
@@ -177,5 +177,14 @@
         [userId, JSON.stringify(progress.milestonesAchieved || []), progress.qualifiedReferrals || 0,
          progress.totalMilestoneRewards?.toString() || '0', progress.currentTier || null]
       );
-    } catch (err: any) { logger.error('DB save milestone failed', { error: err?.message }); }
+    } catch (err: any) {
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB save milestone failed', { error: reason });
+    }
   }
@@ -191,6 +200,13 @@
          reward.sourceId, reward.sourceType, reward.createdAt, JSON.stringify(reward.metadata || {})]
       );
     } catch (err: any) {
-      logger.error('DB save pending reward failed', { rewardId: reward.id, error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB save pending reward failed', { rewardId: reward.id, error: reason });
     }
   }
diff --git a/Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts
@@ -0,0 +1,111 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868 (operator 90 screen, referral milestone service): the two WRITE catches of services/referral/src/services/milestoneService.ts,
+// dbSavePendingReward (line 194) and dbSaveMilestoneProgress (line 180), pass `err?.message` straight into the logger's meta object,
+// unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter
+// throws) makes the catch throw, so checkAndAwardMilestones REJECTS where an ordinary Error gets a logged failure and the awarded
+// milestones and rewards are still answered (the failed save is swallowed by design). The cells let the read answer "no row yet" and
+// make ONE of the two INSERT statements reject with the value under test, with a first-referral count of 1 (one milestone, one
+// reward) for the reward save and a count of 0 for the progress save. The stand-in rejects with a plain function, not vi.fn(): a spy could inspect a revoked Proxy and fail before the code
+// under test saw it. Harness: the real module with ../db and ../utils/logger replaced by plain stand-ins; no database, no network.
+const h = vi.hoisted(() => ({
+  failOn: '' as string,
+  toThrow: undefined as unknown,
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (text: string, ..._args: unknown[]) => {
+    if (text.includes('INSERT INTO svc_referral_milestones_rewards') && h.failOn === 'reward') return Promise.reject(h.toThrow);
+    if (text.includes('INSERT INTO svc_referral_milestones ') && h.failOn === 'progress') return Promise.reject(h.toThrow);
+    return Promise.resolve({ rows: [] });
+  },
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
+  h.failOn = '';
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
+const SAVE_REWARD = 'DB save pending reward failed';
+const SAVE_PROGRESS = 'DB save milestone failed';
+
+async function awardWith(failOn: string, value: unknown, referrals = 1): Promise<{ threw: boolean; milestones?: number; rewards?: number }> {
+  h.failOn = failOn;
+  h.toThrow = value;
+  try {
+    const r = await milestoneService.checkAndAwardMilestones('user-ks1868', referrals);
+    return { threw: false, milestones: r.newMilestones.length, rewards: r.rewards.length };
+  } catch {
+    return { threw: true };
+  }
+}
+const OK = { threw: false, milestones: 1, rewards: 1 };
+// Progress-save cells use a count of 0: no milestone is achieved, so the progress row serialises (an achieved milestone carries a BigInt
+// reward amount, and JSON.stringify of it throws a TypeError of its own inside the same try, before the statement runs).
+const OK0 = { threw: false, milestones: 0, rewards: 0 };
+
+describe('KS-1868 milestone service: the two DB write catches survive a thrown value they cannot read', () => {
+  it('control ks1868 C1: an ordinary Error from the reward save is logged with its message and the award is still answered', async () => {
+    expect(await awardWith('reward', new Error('db boom'))).toEqual(OK);
+    expect(LOG(SAVE_REWARD)).toHaveLength(1);
+    expect(reasonOf(LOG(SAVE_REWARD)[0])).toBe('db boom');
+  });
+  it('control ks1868 C2: an ordinary Error from the progress save is logged with its message and the award is still answered', async () => {
+    expect(await awardWith('progress', new Error('db boom'), 0)).toEqual(OK0);
+    expect(LOG(SAVE_PROGRESS)).toHaveLength(1);
+    expect(reasonOf(LOG(SAVE_PROGRESS)[0])).toBe('db boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the reward save is logged as text and the award is still answered', async () => {
+    expect(await awardWith('reward', revokedProxy())).toEqual(OK);
+    expect(LOG(SAVE_REWARD)).toHaveLength(1);
+    expect(reasonOf(LOG(SAVE_REWARD)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws from the reward save is logged as text and the award is still answered', async () => {
+    expect(await awardWith('reward', getterThrows())).toEqual(OK);
+    expect(LOG(SAVE_REWARD)).toHaveLength(1);
+    expect(reasonOf(LOG(SAVE_REWARD)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: a revoked Proxy from the progress save is logged as text and the award is still answered', async () => {
+    expect(await awardWith('progress', revokedProxy(), 0)).toEqual(OK0);
+    expect(LOG(SAVE_PROGRESS)).toHaveLength(1);
+    expect(reasonOf(LOG(SAVE_PROGRESS)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: an Error whose message getter throws from the progress save is logged as text and the award is still answered', async () => {
+    expect(await awardWith('progress', getterThrows(), 0)).toEqual(OK0);
+    expect(LOG(SAVE_PROGRESS)).toHaveLength(1);
+    expect(reasonOf(LOG(SAVE_PROGRESS)[0])).toBe('unreadable thrown value');
+  });
+});
```
