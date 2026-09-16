# DRAFTER REPORT — #1011 (KS-871) TIER 1 ROUND 2 gate set @ 6dc8256448b50de6a15519001a4f7032ace1ae19

Drafted 2026-09-17 05:13–05:42 AEST (clocks from `date`) by a Wednesday drafting subagent. Nothing was launched and no pane was opened. The launcher ran with `--check` only. Nothing was merged, pushed, commented, filed or mailed. No git write verb touched the Secuura checkout.

## BLUF

- **The set is ready.**
  - Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1011r2-ks871-tier1.md`
  - Prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1011r2-ks871-tier1.prompt.txt`
  - Launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks871_1011r2.sh` (mode 755, sha256 `e11ca9c4bcb93fd3`).
- **`--check` rc 0** four times:
  - 05:33:21 (develop `79432c797`);
  - 05:37:07 (develop had moved to `e0f41a8fa`, cleared by content as disjoint);
  - 05:38:21 on the final brief and prompt, before the negative controls;
  - 05:43:44 after a header-clock-only edit to the brief (`check.out`; the earlier runs are kept as `check.*-run-*.out`).
- **11/11 negative fixtures refused**, each with its expected distinct exit code, on the final text (`controls_check.out`, 05:38:49–05:42:37).
- **Develop moved twice.** Round 1 ended on `1125607e9`. Wednesday read `79432c797` (#1012) at 05:13. At 05:36:48 it was `e0f41a8fa` (#1013 KS-999, `services/auth` only).
  - Merged-tree OIDs: `1429bc93fad4f5892b816e991ec4373b85046053` for `79432c797`; **`839294c16de1ec6392964daddd5d967132465abc` for `e0f41a8fa`**.
  - The api-gateway subtree is `0e7c4b535` in both, so the api-gateway predictions carry over.

## Top predictions (drafter-labelled; the gate falsifies)

1. **The census on `6dc825644` reproduces round 1's D3 counterfactual, with REGRESSION 0 in both envs.**
   - Rows DIFF from base: 256 in test, 574 in production. All of them move from a non-canonical path on base to the canonical path on head. **F-1011-1, F-1011-2 and F-1011-3 CLOSED for their round-1 instances.**
   - Instruments: `predict_from_r1_d3.out` (from round 1's JSONs, 4/4 oracle controls). `drafter_probe.out`: the 29-request probe gives head == round-1 D3 on 29/29 rows plus the nested fixture, and head == merged on 29/29.
2. **F-1011-5 CLOSED for its three rows, with a NEW Minor test-quality residue: the production cell does not pin its own premise.** MEASURED (`drafter_sample.out`):
   - As committed, index.ts really re-evaluates under production. The witness is `X-CSRF-Token`, mounted only at module-load NODE_ENV ≠ test; it is present on both production responses.
   - With `vi.resetModules()` removed, the header is absent and the file is still 3/3 green.
   - The cell's only production witness is the 307, and `versioning.ts:47` reads NODE_ENV per request.
3. **A pre-existing door bypass exists by two spellings KS-1187 does not name (base == head, not this PR).** Scope-less connector, ENFORCED:
   - `POST /api/gdpr/%65rasures` → 200, and the upstream received it. That holds in test and in production (after the 307).
   - `POST /api/gdpr/x/../erasures` → 200 with an upstream hit in test; in production the 307 is followed by a 400.
   - Whether originate routes such a path is UNMEASURED. By READ inference (express 4 matches the raw pathname) originate likely answers 404.
   - Disposition: an escalation candidate for Wednesday / Kam, recorded by the gate only.

## What the drafter measured (all in this folder)

| # | what | instrument → output | result |
|---|---|---|---|
| P0 | head, commits, develop, compare | `git_read.sh` → `.out` 05:15:30; `gh_read.py` → `.out` 05:16:42 | head `6dc825644` = refs/pull/1011/head = branch. 3 commits (`0a1f8900c` → merge `22c0a51a8` [parents `0a1f8900c` + `1125607e9`] → `6dc825644`). merge-base `1125607e9`. develop `79432c797` (#1012). compare diverged, ahead 3, behind 1, files 4. PR delta: audit.ts `a7be8626f → 052131de0`; Part A `8d66dfaf7`; Part B `f6bf4f9d4`; real-app `ef19446f2` |
| P1 | develop move #2 | `devmove_read.py` → `.out` 05:37:33; `merged_oid_e0f41.sh` → `.out` 05:37:52 | `e0f41a8fa` = #1013 KS-999, 3 `services/auth` files. Merged tree `839294c16`, api-gateway subtree `0e7c4b535` (the same as for `79432c797`) |
| P2 | substrate | `drafter_setup.py` → `.out` 05:20:34 | Clone --shared with worktrees base `1125607e9` / head / merged (local no-ff `79432c797` = `2a38b4a7c`, tree `1429bc93f` = `merge-tree --write-tree`). Shared dist built per tree, IN TREE |
| P3 | suites | `drafter_sample.out`, `drafter_targets.out` | head **50/417**, base **47/408**, merged **51/419**; all pass, 0 pending. `tsc -p .` rc 0 on all three |
| P4 | including tsc | `drafter_tsc.py` → `.out` 05:23:41 | Round 1's program. `--listFilesOnly` includes all 4 PR files (head, merged). **30 lines / 10 files on base, head and merged; 0 in PR files; NEW 0.** No plant (the gate's) |
| P5 | 29-request real-app probe | `drafter_probe.py` → `.out` 05:22:54 | base vs head SAME 22 DIFF 7 (5 gdpr refusals, batch.verify, v1 login → auth.login). head vs merged 29/29. head vs round-1 D3 29/29 |
| P6 | census prediction | `predict_from_r1_d3.py` → `.out` 05:19:22 | See Top prediction 1. Spelling invariance: head 118/119 test, 119/119 production (base 65 / 109). D3 test vs production differ only on 7 `POST /api/documents` rows: 307 then a 5 s client timeout, the same on base (curio) |
| P7 | request-target forms | `drafter_targets.py` → `.out` 05:24:37, `targets_*.json` | Base == head: `/api/LOGS` 204 → `LOGS.create`; `/API/logs` 204 **unaudited**; unrouted 404s carry caller text. Head fixes the absolute-form and v1 spellings. Door bypass rows in Top prediction 3 |
| P8 | real-app cell tampers + witness | `drafter_sample.py` → `.out` 05:21:47 | F0 3/3. R1 **2 red** (= READY). NORESET **0 red**. NOPRODENV **1 red** (`expected 403 to be 307`). CSRF witness: present with reset, absent without. tsc rc 0 every row. Restore sha-identical |
| P9 | gate control tamper | `drafter_gctrl.py` → `.out` 05:26:38 | G-CTRL **3 red** of 50/417 (Part A CONTROL + both real-app admitted rows). tsc 0. Restore sha-identical |
| P10 | Linear | `linear_read.py` → `.out` 05:17:50 | pull/1011 → KS-871 `contributes` only. KS-843, KS-858 and KS-1187 carry no #1011. KS-1187 is Backlog, Urgent, 0 attachments |
| P11 | checkout bounds | `git_read.out` 05:15:30, `bounds_mid.out` 05:26:47, `bounds_end.out` 05:36:48 | Porcelain 0 ×3. config sha `d7e7298b…` ×3. refs 899 ×3. worktrees 110 / list 111 ×3. Branch `feature/ks-597-b-caller-scoped-externalref` ×3. refs/pull/1011/head unmoved. develop `79432c797` → `e0f41a8fa` between mid and end. 0 checkout `.vite` / `.vitest` / `.cache` entries newer than the setup (control: 30) |

## Disagreements with the READY (and with the commission)

1. **Commission item 1, read literally, calls the recommended fix a regression.** "Any row that differs from base outside the gdpr refusal classes is a regression." D3, which Wednesday's NO GO mail told the seat to implement, changes about 230 (test) and 536 (production) non-gdpr rows, all toward canonical. In production that includes R-5's `v1.login` → `auth.login` rows.
   - The brief keeps the rule as the FAIL criterion (nothing dropped). It adds an independent target-only oracle and requires both counts.
   - This is flagged for Wednesday to overrule if she means the literal rule.
2. **"recorder 0 hits (so the door)"** does not discriminate the door from CSRF: under production, CSRF is mounted (`index.ts:387`). The 403 body is `INSUFFICIENT_SCOPE` and a with-scope control gives 200 (P7), so the door explanation is right. The cell does not prove it.
3. **"stubs env in beforeAll" (C4):** true as committed, but unpinned (P8).
4. **The NO GO mail asked for TE, G-V1 and G-D3 re-runs.** The READY table omits them. On this head TE and G-D3 are identity edits, and R1D covers G-V1. Not a defect.
5. **"tree = prediction e073733d1":** not read by the drafter. Left to the gate (item 6).
6. **"develop 1125607e9: 47 / 408":** develop is now `e0f41a8fa`. Merged api-gateway is 51/419, so the denominators need re-stating (R-9 style).
7. **Round-1 R-7 (KS-858 not in body)** still holds. The body now also names KS-1187 once; KS-1187 has no attachment.

## Every deviation from round 1's set

- **Base tree:** `1125607e9` (the merge-base), not `d067725ff`. Round 1 proved the two audit-identical on 1115 × 2 envs. Four named trees: base, head, merged, dev.
- **Census oracle:** round 1 classed rows against D3; the head now IS D3. The brief requires a target-only oracle plus spelling invariance, with planted controls, and keeps D3 JSONs as a reproducibility reference (method lesson 6).
- **New method lessons:** 7 (an env witness keyed to module load) and 8 (re-run the prior instrument).
- **New gate items and rows:**
  - item 4: the module-load witness and NORESET / NOPRODENV rows;
  - item 9: D6 added beside KS-1187, record-only;
  - items 11–13: suites and disjointness, seat claims plus R-1..R-9, NOT TESTED.
- **Tamper table:** the READY's rows plus ONE control tamper, G-CTRL. Round 1's G-NONGDPR / G-ADMITTED-ONLY / G-D3 / G-V1 / TE are dropped as gate rows: identities, or covered by the seat's R-rows.
- **The PRIOR ROUND block (BRIEF_TEMPLATE round-N rule)** names the round-1 report path. The prompt carries it too.
- **Launcher:** generated by `gen_launcher_1011r2.py` from the round-1 launcher itself (the same PR, the same guards). 18 asserted substitutions, 74 output controls, a residual guard (round-1 tokens, minus the permitted template mention and the round-1 report path), `#1011` enumerated first (9), `bash -n` rc 0.
  - JUDGED: 14 files (round 1's 12 + `routes/audit-export.ts` + `routes/verification.ts`).
  - GUARDED: those 14 + the 3 ks871 tests + the Dev lockfile.
  - LANDED: audit.ts `052131de0`.
  - The compare is pinned at `1125607e9` ahead 3, files 4. The OK message no longer claims "merged tree = head tree".
  - **New exits:** 24 (brief AND prompt must name the round-1 report path) and 25 (brief AND prompt must require CLOSED / STILL OPEN / NEW). Overrides were renamed `QA1011R2_*`.
- **Negative fixtures:** 11 versus round 1's 8.
  - The five commissioned: missing subject → 23, missing tier → 7, missing SHA → 20, missing mail step → 12, missing per-entry farm → 22.
  - Round 1's others: head override → 6, LANDED → 19, unpinned blob → 18.
  - New: no round-1 report → 24, no per-finding disposition → 25, no ROUND 2 → 15.
- **Report dir:** `Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks871-1011-6dc825644-tier1-r2/`. Subject `[QA -> Wednesday] TIER 1 GATE #1011 ROUND 2 (KS-871) 6dc825644 — <verdict>`, from coagent@.

## Outside the rules, stated

- `merged_oid_e0f41.sh` guarded its `merge-tree` call with `git cat-file -e … 2>/dev/null`, which **discarded stderr** on that one existence test. The line above it printed `cat-file -t` with stderr kept, and the object existed, so nothing was hidden. It is still a rule slip.
- The drafter substrate farmed node_modules per entry only for Dev, api-gateway and shared. The other 24 package `node_modules` were linked wholesale, a shortcut inherited from round 1's `drafter_setup.py`, and vitest never ran in them. Afterwards the checkout had 0 `.vite` / `.vitest` / `.cache` entries newer than the setup. The brief tells the gate to farm every package per entry, as round 1's gate did.
- Renames, not deletions:
  - `bounds_end.out` → `bounds_mid.out`, when a later reading was taken.
  - `check.out` → `check.first-run-develop-79432c797.out`, then `check.second-run-before-e0f41-edit.out`.
  - `controls_check.out` → `controls_check.first-run-before-e0f41-edit.out`.
  - All were re-run on the final brief and prompt. Probe test files and the including-tsc configs were quarantined by rename in the clone's `_quarantine/`. Nothing was `rm`'d.
- Tamper edits and probes ran only in the drafter clone. `audit.ts` and the real-app test were restored sha-identical: `f0b0b1984ecf` and `ae45e5d600da`.
- Drafter clone: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/76d545ac-4e62-4400-be44-c9ce11c3c344/scratchpad/gate1011r2_draft_cjm5soog` (`drafter_paths.json`).
