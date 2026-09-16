# DRAFTER REPORT: #1009 (KS-864 F-1007-1 follow-up) tier-2 gate set, 2026-09-17 01:27–03:09 AEST (network outage about 01:42–03:03)

**BLUF**
- **Files:**
  - brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1009-ks864-tier2.md`
  - prompt: `…/briefs/2026-09-17_secuura-1009-ks864-tier2.prompt.txt`
  - launcher: `…/launchers/launch_qa_secuura_ks864_1009.sh`, from `gatesets/2026-09-17_gate1009/gen_launcher_1009.py` (template: the #1007 tier-2 launcher; 21 substitutions, 57 output controls, residual guard clean, bash -n rc 0)
- **Launcher `--check` (03:08:22, `check.out`):**
rc 0
- **Negative controls, `--check` only (`controls_check.out`):** head override exits 6; prompt without MAIL exits 12; brief without the SHA exits 20; brief without TIER 2 exits 7.
- **Tier:** TIER 2 holds. It is test only: `system-status.ts` is blob `956083916` at base, head and develop (`git_read.out`). **Origin did not move:** ls-remote at 03:03:43 still shows #1009 `6ec0cb198` and develop `73d3fcb90`.
- **Questions:** Wednesday's 8 are all in the brief. The drafter added a setup-vacuity tamper (resetModules), red-before-green against the pre-#1007 blob, a re-run of #1007's S-A and S-B, residual tampers (`??`, production-only), and an env probe with a control.

**Where the READY disagrees with what I measured**
1. **Including tsc.** The seat reports 53 → 47 overall and 6 → 0 in the KS-864 files, including TS2741 ×2 "pre-existing on develop". My program (`drafter_static.out`; inclusion shown by `--listFilesOnly`; planted TS2322 + TS6133 control) gives **34 → 30 raw lines, KS-864 files 4 → 0, and 0 TS2741 in any tree**. The #1007 gate also had 4, not 6. Both agree on the direction: the KS-864 files reach 0 and ks864c adds 0. PREDICTION: RECORD, or Polish on the seat's evidence.
2. **"vi.resetModules gives a fresh module per block" is true but unpinned.** Removing it reds 0. Removing it while a development-only regression is present also reds 0, although that regression alone reds 1 (`drafter_run.resetModules-rows.out`). PREDICTION: Polish at most.
- **Agree (measured):**
  - Suites: base 45/391, head 46/397, merged 46/397; 0 pending.
  - G-2 issuer, verifier and admin: tsc rc 0; exactly that portal's 2 ks864c cells red, AssertionErrors only.
  - ks864c on the pre-#1007 blob: 3 staging reds, 3 development passes.
  - P-1007-1 is neutral by parser: `it`/`expect` identical; the type edit leaves the transpile identical (control differs); JS delta is 2 lines per file. #1007's S-A still reds 2 ks864a cells at head.
  - Env restore works: the probe passes, and with the restore removed it reds `NODE_ENV='development'`.
  - eslint 0/0.
  - linkKind: `contributes` on KS-864 only; 0 closing phrases (controls hit).
  - 0 files shared with #1008 or any open PR.
  - Merged api-gateway tree equals head's (`2f3b012cc`).

**Predictions (instrument)**
- S-B at head reds 3 (ks864b ×2 + ks864c issuer staging): `drafter_run.first-run-…out`.
- Setting env after import reds 6. A production-only regression reds 0. `||` → `??` reds 0. These are residuals for item 2.
- Merged tree with develop still at 73d3fcb90: 46/397 (measured). Any later develop: unmeasured.

**HOLDs I came near**
- A combined Bash call included `git -C <checkout> worktree list`. The no_cd hook refused it as a write verb, and nothing in that call ran. I re-ran without it and counted `.git/worktrees` (110 entries, plus main = 111).
- The first reset rows ABORTED on a marker that matched the docblock. I renamed their output rather than deleting it and re-ran with `vi.resetModules();`.
- The launcher ran only with `--check`. Every write verb and edit happened inside `scratchpad/gate1009_draft_bvv184t0` via script files.
- Checkout readings: porcelain 0 and config sha `e0fa706f…` at 01:28 and at 03:08. Refs 891 at both.
- No rm, no credential echoed, #1008's clone and gateset untouched.

**NOT measured**
- The seat's own scratch tsconfig and worktree type resolution (not visible to me).
- A `--no-isolate` cross-file run (I only read that the vitest config uses defaults).
- The packages/shared suite.
- Any develop newer than 73d3fcb90.
- The parity grid and real-app probe (done by the #1007 gate; no product byte changed).
