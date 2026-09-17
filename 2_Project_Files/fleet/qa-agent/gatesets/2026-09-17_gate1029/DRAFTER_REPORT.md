# DRAFTER REPORT — #1029 (KS-1180 part 1) TIER 2 gate set @ cd3580e1f

Drafted 2026-09-17 21:03–21:30 AEST (clocks from `date`). Work ran in the drafter's own clone `GS/scratch/gate1029_draft_2jl843cs/` (worktrees `wt_head`, `wt_curdev`, `wt_merged`). The Secuura checkout got read verbs only. Nothing was pushed, filed, commented, mailed or launched. `GS/` = this directory.

## BLUF
- **Head `cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc`** = `refs/pull/1029/head` = the branch (ls-remote 21:03:16, 21:09:56, 21:29:47; PR API 21:13:04). Develop **`75ad0e55c`** (#1026, auth only) throughout; compare develop...head = merge_base `20ab16f9a`, ahead 3, behind 1, files 1.
- **Launcher `--check` rc 0** (`out/check.out`, 21:26:06–21:26:17), sha256 `c0f036756bcccc64`, 212 lines. **17 / 17 guard controls fire** (21:26–21:29:39): test-file fixture develop 0 / LANDED 19 / unpinned 18; develop override = merge-base 0, behind the merge-base 0, pre-#1016 18; head override 6; brief/prompt mutations 7, 15, 20, 12, 22, 23 ×2, 24, 25, 26.
- **Guarded by PATH BLOBS at the current develop, not develop's SHA:** the ks1072 test (`4ad1cdcd1` OK / `d9c98320e` LANDED), its import closure `routes/verification.ts` `28fb58343`, `services/redis.ts` `47659ee9c`, `utils/logger.ts` `77200ea9c`; api-gateway `package.json`, `vitest.config.ts`, `vitest.setup.ts`, `tsconfig.json`; the `packages/shared/src` tree `960758bcb`. Any other develop move passes and is listed (api-gateway files touched, compare status).
- **Every seat claim the drafter re-ran holds.** Merge trees = predictions; 5 / 5 tamper rows exact; head 56 / 551; tsc rc 0; KS-1180 `contributes` only; KS-1073 not linked.
- **The new witness discriminates (MEASURED):** tier 1 answering the hash each cell expects (the #1016 gate's GT2) reds 5 at the WITNESS on head and **0 on the pre-PR blob**; GREREAD 0 on the pre-PR blob; the new control reds on a deaf listener (1) and on a double read (1 + 5).
- **One defect in the builder's evidence (D1):** the seat's GT2 is NOT the #1016 gate's GT2. Its originate answers without `blockchain`, so the OLD guard reds it too (5 at `expected 'none' to be 'persisted'` on the pre-PR blob). It proves nothing the old guard didn't.
- **One limit the PR's wording overstates (D2):** tier 1 answering + one discarded anchor-store read stays **56 / 551 green**. The witness proves "asked once", not "answered". KS-1180's open tier-1 half (a 0-read cell) closes it.
- **Predicted verdict: GO** (Records), **or GO WITH FINDINGS** if the gate grades D2 against the assertion message.

## Outputs
- Brief `briefs/2026-09-17_secuura-1029-ks1180p1-tier2.md` (sha256 `3ce5ca7986fe48e7`); prompt `.prompt.txt` (`7598e896fac34db6`, opens `ultrathink`). Subject `[QA -> Wednesday] TIER 2 GATE #1029 (KS-1180) cd3580e1f — <GO | GO WITH FINDINGS | NO GO>`, coagent@ → wednesday-agent@. Report dir `…/reports/2026-09-17-ks1180-1029-cd3580e1f-tier2-r1/`, NOT-TESTED.written-first.md, MERGE ADDENDUM, probe rule (probe files OUTSIDE services/*).
- Launcher `launchers/launch_qa_secuura_ks1180p1_1029.sh` from `gen_launcher_1029.py` (template: the #1018 round-2 launcher). 24 asserted anchors (22 substitutions + 2 whole-block replacements: header, develop judgement). Pins re-read from the repo at head / merge-base / develop, residual guard, output controls, heredoc parity (0 apostrophes, 8/8 and 75/75 parens), no git write verb, `bash -n` rc 0. New exit 26 = the probe-location rule in brief and prompt.
- Kept generator slips (nothing written on the first two):
  - `out/gen_launcher.run1-…` (residual guard hit the exit-26 message naming #1018 F-3);
  - `out/gen_launcher.run2-…` (my control counts ignored header occurrences);
  - `out/gen_launcher.run3-…` + `out/check.run1-…` + `out/launch_qa_secuura_ks1180p1_1029.sh.pre-212602-superseded` (rc 0, 17/17, superseded by a cosmetic regen: "MOVED past" printed for a develop BEHIND the merge-base; the exit-23 text said "prompt" when the brief lacked the subject).
- Scripts: `import_closure_1029.py`, `drafter_setup_1029.py` (+ `drafter_setup_farm.py`, a byte copy of gate1028's), `api_read_1029.py`, `drafter_run_1029.py`, `drafter_followup_1029.py`, `gen_launcher_1029.py`, `make_fixtures_1029.py`, `check_launcher_1029.sh`. Fixtures under `controls/`.

## Measured (own clone; `out/`)
**Trees** (`drafter_setup.out`):
- `merge-tree a4dc0d8ee × 81ee4b729` = `02f3ab417` = tree(`7553821fc`).
- `merge-tree 7553821fc × 20ab16f9a` = `5138ce742` = tree(`cd3580e1f`).
- Each merge's first-parent diff = develop's delta: name sets (7 and 17 files) and `patch-id --stable` (`32ecd72a7f07a0c8`, `6b11d554c180397c`) are equal, and every brought blob equals develop's. Each second-parent side is the test file only. Control: the two develop deltas differ.
- patch-id(`d7e95cd9f..a4dc0d8ee`) = patch-id(`20ab16f9a..cd3580e1f`) = `d99b1ba3c8e1e5f3`.
- Merged over `75ad0e55c` = `1227ecc82`; its api-gateway and shared subtrees equal the head's.

**Suites** (`drafter_run.out`, `drafter_followup.out`):

| tree | files / tests | failed | tsc -p . rc |
|---|---|---|---|
| develop `75ad0e55c` | 56 / 550 | run 1: 2 (ks864b, ks864c; ~5.6 s timeouts). Run 2: 0 | 0 |
| head | 56 / 551 | 0 | 0 |
| merged | 56 / 551 | 0 | 0 |

- **Test-including program:** develop 31 errors, 1 in ks1072 (TS18046 at `(124,10)`); head 30, 0 in ks1072. The plant added 2 errors.
- **eslint:** the ks1072 test reads 0 / 0 at head and at develop. The control fires `no-unused-vars` (severity 1).

**Tampers:** 13 rows (`tamper_rows.json`; the table is in the brief §2). tsc 0 and restored on every row, 0 load failures. Twelve rows matched the prediction on run 1. D-DOUBLE-ALWAYS matched on its re-run: run 1 had +1 db.retry timeout at 6.36 s.

**Links** (`api_read.out`):
- pull/1029 → KS-1180 `contributes` (In Progress, set by the GitHub bot at 11:00:14Z). Controls: pull/1028 → KS-744; pull/99999 → 0.
- KS-1073's attachments: pull/1005 `closes` only.
- 0 closing phrases; 0 at-signs.

**Bounds:**
- **Checkout at 21:09:56, 21:11:24 and 21:29:47:** porcelain 0, worktrees 112, refs 937, `.git/config` `09959c342094001c`, api-gateway `.vite/vitest` 2026-08-17 20:54:28.
- **LISTEN rows:** 17 → 18, with 0 node listeners at both readings. The extra row is not node.

## Where the READY / PR body is wrong or incomplete
- **D1 (MEASURED):** `tamper.py` labels GT2 "the #1016 gate's GT2", but it is a weaker form that the OLD guard also catches. The PR table's GT2 row therefore does not show discrimination. Target: seat evidence, RECORD/Polish.
- **D2 (MEASURED):** the assertion message "KS-1180: tier 2 answered, one anchor-store read of this document" and the READY's "witness tier 2" claim more than an exact-request-list check proves (D-T1-ALSO-READ is green suite-wide). The code comment's "only if" is accurate.
- **D3 (MEASURED):** the listener counts every stub request. If the live-scan URL pointed at the stub, the cells would red although tier 2 answered. This is unreachable today and fails closed. RECORD.
- **READY "P-1016-2 not re-measured":** now measured as closed.
- **READY "no file overlap":** true.

## NOT measured by the drafter
- The gate's own-direction rows, and D4 (listener leak after a status red): READ only.
- Any real anchoring or originate service.
- The ks1073 file (KS-1180's other half).
- Schemathesis/Akto: predicted NOT REQUIRED (test-only).
- Whether develop moves again before launch. `--check` judges that.

## For Wednesday
- **Nothing blocks the launch.** Re-run `--check` in the cockpit right before launching. It refuses only if a guarded path moves or #1029 lands.
- **`.git/config` changed:** the checkout's sha256 moved from `d7e7298b…` (the #1018 gate, 20:32) to `09959c34…` (21:09). It did not change during drafting, and it is not a #1029 matter. Worth one look (a launcher's `core.sshCommand` refresh is the likely writer).
- **Usage cap:** confirm under the 40% cap before launch; launch only from a cockpit pane.
