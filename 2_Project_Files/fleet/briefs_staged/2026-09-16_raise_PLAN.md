# STAGED, NOT SENT: plan for raising Ornith's held diffs across THREE Secuura/Blockchain seats (A, B, C)
# Drafted 2026-09-16 ~21:3x AEST by a Wednesday drafting subagent. Supersedes the single-seat staged brief
# `secuura_raise_ornith_ready_diffs.md` (2026-09-15) for the READY bundles. That file stays on disk as history.
# Authority: Kam, panel 2026-09-16 20:40:59, confirmed 20:41:47 ("yes. claude agents"). Wednesday's reading:
# `0_Brain/learnings/2026-09-16_new-account-spin-up-agents-to-test-approve-merge.md`. NOT covered: deploys
# (kintsugi or demo), demo/UAT, external comms beyond the ticket comments the project's rules require,
# `.github/workflows` PRs, other authors' PRs. v1.3 signature classes unchanged.

Seat briefs:
- `2026-09-16_raise_seat_A.md`: api-gateway, demo-service, packages/shared, auth (16 PRs)
- `2026-09-16_raise_seat_B.md`: security, originate, anchoring, vc-issuer, kyc, plus the generated OpenAPI yaml and VOCABULARY.md (20 PRs)
- `2026-09-16_raise_seat_C.md`: scripts, hooks, Start_Up, systemTest tooling, deployment, merge-rule docs, plus 3 record closes (22 PRs, 2 more pending)

---

## 1. Develop tip, measured
- **origin/develop = `0b25f823f6660ac52b665f14055799ff0c3b616d`** (PeterObeden, "Merge pull request #997", 2026-09-15T14:22:41Z). Instrument: GitHub REST `GET /repos/Secuura/Distributed_Secuura/branches/develop`, read twice (~20:5x and ~21:2x). Same SHA both times.
- The READY files were checked at M55 `48e65c435`. Compare API `GET …/compare/48e65c435…0b25f823f`: status `ahead`, 4 commits, 36 files. **All 36 are under `systemTest/schemathesis/**`, `systemTest/CLAUDE.md` or `Projects Documents/QA_Tool_Cheat_Sheet…html`. None of them is among the 111 paths the bundles touch** (a set intersection over the normalised `+++` paths of every READY fence gave an empty result). **No bundle's files moved.** No bundle needs a re-apply because of the tip.
- `0b25f823f` is **not in the local object store** (`git cat-file -t 0b25f823f` → "Not a valid object name"). Each seat has to `git fetch origin` in its own worktree before cutting branches.
- Branch rules on develop (`GET …/rules/branches/develop`, ruleset 18499832): `pull_request.required_approving_review_count = 0`, merge methods merge, squash and rebase are all allowed, `deletion` and `non_fast_forward` are enforced. The kksecura PAT can still squash-merge its own PRs. Kam ruled `raise-to-1` on 2026-09-10 (card `secuura-required-approvals-zero-after-the-untick`, still undelivered) but has **not applied it**. If he applies it mid-run, merges will block because GitHub returns 422 on kksecura approving kksecura. Seats are told to STOP and mail if that happens.

## 2. READY count
- Instrument: `ls night/ | grep '^READY_'`, with (ticket, pin) parsed from each filename by `READY_(KS-\d+)(-<pin>)?_(ornith35b-q\d)_`.
- **84 READY files, 82 distinct (ticket, pin) pairs, 58 distinct tickets** (counted ~21:2x, after KS-910 landed).
- The two duplicates are quantisation twins: `KS-1120-F2` (q4 + q8) and `KS-1171-8j` (q4 + q8). Only one copy of each is raised (q4; see seat B).
- 3 `_superseded_READY_KS-1172-{A,B,D}_*` files are excluded (two-verb versions, replaced by A3/B3/D3).

## 3. Partition: no file in two seats
The split is by directory family. It is balanced by PR effort, not by count: service PRs carry vitest/jest suites and shared guards, while script and doc PRs are small. Every file a bundle touches, including the secondary files a seat edits by hand (the regenerated yaml, openapi prose, comment rewords), sits in exactly one seat.

| Seat | Owns (write) | Bundles, in queue order | PRs |
|---|---|---|---|
| **A** | `Blockchain/Dev/services/api-gateway/**` · `Blockchain/Dev/services/demo-service/**` · `Blockchain/Dev/packages/shared/**` · `Blockchain/Dev/services/auth/**` | KS-1130 · KS-1123 · KS-960 · KS-1165 · KS-932 · KS-844 · KS-1073 · KS-1087 · KS-1072 · KS-864 · KS-1101 · KS-871 · KS-745 · KS-999 · KS-1018 · KS-1050 | 16 |
| **B** | `Blockchain/Dev/services/{security,originate,anchoring,vc-issuer,kyc}/**` · `Blockchain/Dev/docs/openapi/secuura-api.yaml` (generated) · `Blockchain/Dev/docs/VOCABULARY.md` | KS-1120 · KS-1171(8j) · KS-1118(F2) · KS-887 · KS-975 · KS-747 · KS-908 · KS-888 · KS-974 · KS-976 · KS-1121 · KS-692 · KS-629 · KS-1160 · KS-1028 · KS-1074 · KS-1158(R1) · KS-794 · KS-1133 · KS-1172+KS-1173 | 20 PRs (KS-1172+1173 is one PR) |
| **C** | `Blockchain/Dev/scripts/**` · `.githooks/**` · `Start_Up/**` · `systemTest/{akto,performance}/**` · `systemTest/schemathesis/validate-lint.sh` · `Blockchain/Dev/deployment/**` · `Blockchain/Dev/CONTRIBUTING.md` · `Blockchain/Dev/docs/DEV-PROCESS.md` · repo-root `CLAUDE.md` | KS-1093 · KS-1089 · KS-1127 · KS-884 · KS-1047 · KS-865 · KS-958 · KS-1139 · KS-972 · KS-1011 · KS-1031 · KS-1081 · KS-1033(item 1) · KS-910 · KS-1108 · KS-1117 · KS-1164 · KS-1097 · KS-1037 · KS-1049(A) · KS-1035(D) · KS-1045, then record closes KS-777 · KS-813 · KS-683 (KS-1076 verify-only) | 22 PRs + closes |

**Disjointness, checked mechanically after the briefs were written.** Instrument: parse every `` `READY_…diff.md` `` named in each seat brief, collect the `+++ b/` paths of its per-file sections, and test them against that seat's ownership regexes.
- Seat A: 23 READY files / 32 paths. Seat B: 30 / 40. Seat C: 29 / 39. Total 111 paths.
- **0 paths outside their seat. 0 paths in more than one seat.** Every named READY file exists.
- The only READY files named by no seat are the two quantisation twins `READY_KS-1120-F2_ornith35b-q8_*` and `READY_KS-1171-8j_ornith35b-q8_*`. They are deliberately not raised. 23 + 30 + 29 = 82 = 84 − 2.

**Why openapi goes with B:** the generator (`scripts/generate-openapi.ts`) reads every `services/<svc>/src/<svc>.openapi.ts`. Six bundles change a published contract or require the yaml to be regenerated: KS-747 (security), KS-974 (security, a clause added by hand), KS-629 (kyc), KS-794, KS-1133 and KS-1172 (originate/anchoring). All six are in seat B. No seat-A bundle touches an `*.openapi.ts` (checked against every seat-A path). A single owner for the generated yaml means one regeneration at a time.

**Same-file ordering, each chain kept inside one seat, in the order the apply check used:**
- A: `routes/verification.ts` KS-1073 → KS-1087 → KS-1072 (the KS-1130/KS-1123 comment rewords also land in this file) · `routes/system-status.ts` KS-864 (A→B) → KS-1101-B · `middleware/audit.ts` KS-871 A → B · `auth/src/routes/users.ts` KS-1018 → KS-1050 · `auth/src/repositories/userRepo.ts` KS-999 (KS-960 is test-only)
- B: `security/src/index.ts` KS-908 → KS-888 → KS-974-A → KS-976 A/B (KS-887's pin reads it) · `security/src/rateLimitScope.ts` KS-975 · `originate/src/services/anchorStateSync.ts` KS-1074 A/B/C → KS-1158-R1 · `originate/src/originate.openapi.ts` KS-794 → KS-1133-A · yaml KS-747 → KS-974 → KS-629 → KS-794 → KS-1133 → KS-1172
- C: `scripts/run-shell-suites.sh` KS-1089 → KS-1127 · `.githooks/pre-push` KS-884 → KS-1047 · `scripts/check-stack-safety.sh` KS-1093 → (pending) KS-1034 · `Start_Up/start-secuura.sh` KS-972 → KS-1011 · `CONTRIBUTING.md` KS-1097 (B,C) → KS-1037 → KS-1049-A → (pending) KS-789 · `docs/DEV-PROCESS.md` KS-1097-A → KS-1035-D · `CLAUDE.md` KS-1097 Da → Db

## 4. Apply check at M55, done by this subagent. The READYs' checker verdicts were NOT re-used.
Instrument: every touched path that exists at M55 (50 files) was exported with `git show 48e65c435:<path>` into a scratch git repo. Each READY fence was split into per-file sections, and each seat's queue was applied in order with `git apply --recount --ignore-whitespace`. On failure, `patch -p1 --fuzz=2` was tried. Output: `scratchpad/raise0916/apply_{A,B,C}.out`. **Since no bundle file moved between M55 and the tip, this result holds at the tip too.**

| Seat | Sections | Clean in order | Need a named accommodation |
|---|---|---|---|
| A | 40 | 37 | KS-1101-C product hunk (the `if (response.ok) {` context line is missing; fuzz 2 also fails; apply by hand from the -/+ lines) · KS-871-PartB product hunk (context does not match `audit.ts:105-111`; apply the one -/+ pair at `:108` by hand) · KS-1050 import hunk (applies ALONE, but conflicts in order with KS-1018's import edit to the same `users.ts` block; merge by hand) |
| B | 52 | 49 | KS-975-item2 product hunk and KS-976-A product hunk (both apply only with `patch --fuzz=2`) · KS-1121 test hunk 2 in `credentialRepo.test.ts` (context mismatch; apply by hand) |
| C | 48 | 46 | KS-1117 product hunk (fuzz, known and named in the READY) · KS-1097-A hunk 2 `DEV-PROCESS.md:259` (a dropped blank context line; apply by hand) |

**⚠ Correction to the staged brief ("exactly TWO are affected" by an indented file header): measured FOUR.** Instrument: `grep -E '^ (---|\+\+\+) '` over the extracted fences of all 84 READYs. Positive control: `^--- ` matched in 84 of 84 extracted patches.
- `READY_KS-1172-A3` :16 and `READY_KS-1172-B3` :15 (` --- a/…`, already known)
- **`READY_KS-1073` :11 (` --- /dev/null`), new**
- **`READY_KS-871-PartB` :10-11 (` --- /dev/null` / ` +++ b/…`), new**

The 09-15 scan matched only `^[ ]--- a/` and missed the ` --- /dev/null` form. Fix: split on the file boundary and de-indent. All four then apply (the KS-871-B product hunk still needs the by-hand line above).

Other format defects seats are told about: `READY_KS-871-PartA` carries fake `diff --git` / `index 1234567..abcdefg` pseudo-headers, which make git create an empty test file first and would defeat `--3way`, so strip them. Several auto-named test files collide by name: KS-1123 F2/F3, KS-864 A/B, KS-974 A/B, KS-976 A/B, KS-1074 A/B/C. Each seat brief gives the renames.

## 5. Collision table: open PRs by `kksecura` against the bundle files
Instrument: `GET …/pulls?state=open&per_page=100` returned 18 open (8 kksecura, 10 dependabot), then `GET …/pulls/<n>/files` for the 8 kksecura PRs. The set was intersected with the READY paths and with the files seats edit by hand (the yaml and the openapi prose).

| Open PR | Head | Colliding file | Bundle (seat) | Hunks overlap? | Handling |
|---|---|---|---|---|---|
| #887 KS-961 | `3aee3deed` | `Blockchain/Dev/docs/DEV-PROCESS.md` | KS-1097-A, KS-1035-D (C) | No. #887 changes :80+ and :117→161; the READYs change :62-65, :187-189, :259-263. Offsets will shift. | Not ours to merge: it also touches `.github/workflows/pr-platform-suites.yml` (card `secuura-891-workflow-scope-merge` → kam-merges). Seat C rebases on develop as normal. |
| #920 KS-734 | `2112a99e3` | `Blockchain/Dev/docs/DEV-PROCESS.md` | KS-1097-A, KS-1035-D (C) | No. #920 changes :139. | Out of this grant's scope. Whichever merges second rebases. |
| #922 KS-679 | `e60a24c50` | `Blockchain/Dev/docs/openapi/secuura-api.yaml` (generated) | KS-747, KS-974, KS-629, KS-794, KS-1133, KS-1172 regenerate it (B) | Generated file | Seat B always regenerates from the sources at its branch tip and never hand-edits the yaml. If #922 merges first, regeneration picks it up. |
| #995, #989, #927, #923, #809 | n/a | none | n/a | n/a | No collision. #995 changes `originate/src/index.ts` and `anchoring/src/index.ts`, which no bundle touches. #989 changes `systemTest/performance/tests/unit/fixtures/*`, which is disjoint from KS-1117/KS-1164 paths. |

## 6. Excluded, and why
- `_superseded_READY_KS-1172-{A,B,D}_*` (3 files): replaced by A3/B3/D3.
- **KS-866**: done.md 20:14 "NOT HELD". The model's text is correct but the brief's content is stale against CONTRIBUTING.md:107/:481 (squash, never push to develop). Reallocated to a Claude seat (Sunday batch). No READY exists.
- **KS-1168, KS-1163, KS-998**: reallocated to Claude as BUILD work (done.md rows 173/185/186; Kam's 07:57Z counter). No READY. Kam's rulings `secuura-ks1168-ilike-search-on-encrypted-pii` = a and `secuura-ks998-format-gate-fails-open-on-missing-deps` = a are **still undelivered**. They belong in the BUILD seat's brief, not these.
- **KS-953 and KS-1102**: Kam-ruled (07:01, KS-953 grammar at 15:04) but Claude-seat BUILD work with no READY. The cards are marked "delivered" to the staged Sunday brief, **which was never sent**. Treat them as undelivered for any BUILD seat.
- **KS-753**: set aside for a Claude seat (needs a mocked harness first).
- **KS-1097's "mirror into the project-root untracked CLAUDE.md by hand"**: excluded. It edits the seat's own instruction file, which is a config change a brief should not order. See open question Q5.
- **Open PRs #887, #920, #922 and the dependabot PRs**: not named by the grant. Untouched.
- **Follow-ups named inside READYs**: they stay on the tickets and are not built in these PRs. KS-1033 items 2–3 · KS-1031 fix 1 (deploy-ordering doc) · KS-1081's 30-variable reconciliation · KS-999's four sibling `return fromRow(` sites · KS-1087 item 2 · KS-1158 R3/R5 · KS-1171's mixed-window design · KS-960's schema reconciliation · KS-1035 items 1–3/5 · KS-1049's hook notice · KS-887's svc_api_keys-anchored tightening (optional) · KS-1139 rule 8 in check-script-portability.sh.

## 7. Pending READYs: add when they exist
- **KS-789 r2**: `Blockchain/Dev/CONTRIBUTING.md` → **seat C**, after KS-1049-A (same file). The local model is running it now.
- **KS-1034**: `Blockchain/Dev/scripts/check-stack-safety.sh` + a new `scripts/__tests__/check_stack_safety_hook_env.test.sh` → **seat C**, after KS-1093 (same file). The local model is running it now.
- (KS-910 was pending when this started. It is now held as `READY_KS-910_…REBRIEF-PASS-7of7` and is in seat C.)

When one lands, Wednesday mails seat C an addendum naming the READY file. It must not be read from the directory listing. The addendum should cite the same PR NOTES header lines.

## 8. Ticket state at plan time
Instrument: Linear GraphQL `issue(id)` with `comments(first:50)`, sorted client-side, for all 58 READY tickets plus KS-1173, KS-777, KS-1076, KS-813 and KS-683. Every READY ticket is **open**: Backlog, except KS-1172/KS-1173 (Todo). KS-777, KS-1076 and KS-683 are Todo; KS-813 is Backlog. None is Done, so no bundle is stale by ticket state. Supporting receipts: PR #795 `merged: true` at 2026-09-03T11:55:42Z, merge commit `7dd304b7c` (for KS-777). KS-813 was fixed by `f09b62945` ("KS-1046 … name the legs that ran (#925)"), found with `git log -S 'legs ran' 48e65c435 -- …/preflight.sh`. KS-1076 item 1 was already recorded as fixed on the ticket (comment 2026-09-13T22:19Z, s215).

## 9. Open questions (each with the default that applies if unanswered)
- **Q1. Platform suites at head while the local model holds memory.** Kam's 08-27 rule is that the four platform suites are the author's final check. Two booted slot stacks (38 services each) alongside ornith:35b is a memory risk; `SKIP_MEMORY` has already fired on this Studio. **Default:** seats A and B run Schemathesis `pr` on their own slot (A=2, B=3, via `SECUURA_STACK_SLOT` + `systemTest/slot-target.sh`) only for bundles that change a route response or a published contract, and only when `memory_pressure` shows ≥30% free. Otherwise the line reads `not run: <measured reason>`, and the READY FOR QA mail says so. Akto, Playwright and k6 are `not run` unless the bundle touches that harness. Seat C needs no stack.
- **Q2. Concurrency inside a seat.** **Default:** at most 3 PRs per seat awaiting GO at once. Same-file bundles are strictly serial: the next branch is cut from develop only AFTER the previous one merged.
- **Q3. KS-692 on merge: Done or leave open?** The ticket's scope is "no tenant ownership check". The PR is Kam's ruled INTERIM narrowing; the ownership model is KS-1116 (Backlog). **Default:** leave open, comment what landed, link KS-1116.
- **Q4. KS-1173 on merge.** Kam's own 09-15 ticket comment says the PR "closes KS-1172 as well". KS-1173's body also asks K two questions (a field for credential references; cross-org anchoring for `verified`, which blocks PS-845), and the deploy ping to S is promised "on DEPLOY". Deploy is outside this grant. **Default:** close KS-1172 as Done. KS-1173 gets a facts comment ("merged at `<sha>`, not deployed; the two questions stay open") and stays open. The two questions go on Wednesday's decision queue.
- **Q5. KS-1097's untracked project-root CLAUDE.md mirror.** **Default:** not done by any seat. Wednesday raises it with Kam.
- **Q6. KS-1045 VM re-measure (`az vm list`, read-only, Secuura Founders Hub tenant).** **Default:** seat C runs `az account show` and, only if it is already on tenant `efc17e5f-7637-4118-b92c-c5236d591cad`, `az vm list -o table`. No `az login`. If it is not signed in, the PR goes up with "facts are the ticket's 2026-09-09 measurements, not re-measured", and Wednesday decides the GO.
- **Q7. Pre-push from a linked worktree.** KS-1034's class means `check-stack-safety.sh`, called under a hook's `GIT_DIR`, can false-red by calling present files "missing". **Default:** if a push fails with `::error::… is missing — … deleted` lines, the seat STOPs and mails a QUESTION. Never `--no-verify`. Wednesday may resequence KS-1093/KS-1034 first.
- **Q8. Record closes (seat C).** **Default:** KS-777 → Done with a #795 receipt. KS-813 → Done with a `f09b62945` receipt after re-reading `preflight.sh` at the tip. KS-683 → Done, no K change, per Kam's 15:04 ruling, with the terminal-state note carried as a comment first. KS-1076 → no write; item 1 is already recorded, item 2 stays open.

## 10. Wednesday's side (not in the seat briefs)
- Usage gate: `fleet/usage_gate.sh` (90% cut) before each seat launch and each QA gate launch.
- One tier-2 through-code QA gate per PR, batchable by tier. GO mails name `#<n>` and the head SHA read from origin.
- The three seats share `coagent@agentmail.to` and the subject prefix `[Secuura/Blockchain -> Wednesday]`. The PR number is the routing key. A GO or ANSWER must name the PR number.
