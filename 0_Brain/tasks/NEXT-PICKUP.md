---
date: 2026-09-06
type: pickup
source: replaced wholesale by the 20:1x seat at its ROTATION (22:2x)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — BOTH Secuura seats WRAPPED (two successor briefs OWED), two gates running, two merges owed a seat; NexusAI PAUSED; Kam's queue = 1 card; Wednesday boots on OPUS for the week

**Kam tonight, verbatim, both executed:** (1) 20:19 *"change your boot script for the rest of the week to boot in opus 5 rather than fable. we are burning through credits a little too quickly"* — the launcher pins `--model opus`, fable line commented in place, backup `.pre-0906-opus`, **`doctor.sh` holds the date: ok until 2026-09-13, WARN after**, both branches exercised. (2) 20:19 *"keep pushing the secuura agent to polish the platform to a ready state"* — the sort key in every brief.

## 🔴 FIRST ACT: the launcher gate gates every relaunch
**Seat B's KS-911/912 launcher change is LIVE ON DISK and its gate is RUNNING in `%127`.** Until that verdict: **no Secuura seat is relaunched** — or restore both `.pre-` copies first (`Launch_Claude.command.pre-ks911` `9609c845…`, `Launch_Claude.seats.test.sh.pre-ks912` `a5d5d9ef…`, both equal to KS-907's gated hashes) and say so in the brief. Shipped hashes verified live at 22:1x: `932a2cc3…` / `b93b2c83…`. **Both successor briefs wait on this.**

## The floor at 22:2x
- **Secuura develop = `60d1ce97e235528f1f3815f90881a80984e340f0`** (seat B's #869 merge at its wrap). Tonight's chain, every link verified from objects: `b77b20bf6` → `34fc749df` → `e1d840d8e` → `a821bd0aa` → `a8aa723a0` → `ff5218867` → `60d1ce97e`. **SEVEN merges. The live validate-then-fetch SSRF gap is CLOSED.** The local `refs/heads/develop` is STALE — `origin/develop` via `ls-remote` is the only honest ref.
- **NO BUILDERS RUNNING.** Seat A (s141) wrapped 22:07, scored 0.95. Seat B (s140d) wrapped 22:04, scored **1.0** — the best seat this fleet has run.
- **`%127`** tester — the launcher, BY HASH (blocking). **`%128`** tester — **#870 (KS-921) tier-1 re-gate**.
- **NexusAI PAUSED** on Kam's 17:01 word.

## Owed, in order
1. **`%127`'s verdict** → then **both successor briefs** (s141b seat A, s140e seat B) via `brief_and_launch.sh`.
2. **`%128`'s verdict** (#870 re-gate) → GO by SHA or a fix round.
3. **#871 (KS-720) has a PASS and NO SEAT** — its GO goes into seat B's successor brief: merge `6845b1cd382e129845df7ae7affe547bef159e30` by SHA against develop re-read; KS-720 → TND.
4. **FILE THE F-1 FINDING — it is a live security defect, not a PR nit.** From #871's verdict: the `undefined` skip is LIVE on three MFA call sites (`routes/mfa.ts` ~:282 and ~:204; `routes/users.ts` ~:1079 — search `mfaSecret: undefined`). **"MFA disabled" emits a PARTIAL update naming only `mfa_enabled` and `verification_level`, so the flag flips, the call reports success, and the TOTP seed and hashed backup codes SURVIVE in the row.** Measured at the wire with a `null` control. **The mechanism is NOT the one BACKLOG.md records**, which is what the PR's justification pointed at. P2 at least; seat B's successor.
5. **Also from that verdict:** **F-2 — `POST /api/auth/wallet/authenticate` is pinned by NOTHING in 595 tests** (gating it leaves the suite fully green) while the file's own comment claims a cell pins all four public routes. **F-3 retracts the builder's premise, keeps its conclusion:** `null` cannot enter the encryption path for ANY column (`typeof null === 'object'`).
6. **Queued gates after the two running:** #872 (KS-732 @ `235bb1ba3`), #873 (KS-931 @ `7d8a3f0e4`).
7. **Carry into seat B's brief, from Wednesday's own omission:** the two KS-923 re-gate Minors, VERBATIM — **QA-923-1** the harness's subject guard uses `-f` forty lines from a comment saying existence is not readability, so a mode-000 subject prints a SUBJECT line with an **EMPTY hash**; **QA-923-2** CELL 12 counts a SKIP as a PASS, printing "12 passed, 0 failed" while eleven cells ran. Seat B refused to file them from a count and was right.
8. **KS-936** (seat B's third-cell ticket, red-proof must red **at rc 0** against `313f96519`) and **KS-930** (F-3/F-6/F-7 from #870's first gate, its first item being that an nginx final stage has **no route to green at all**).
9. **Kam's card** `secuura-demo-kam-admin-default-password` — open, default HOLD. If ruled: RULING RELAY to a seat + `--delivered`.
10. **KS-926's campaign** opens with **FIVE mechanisms of one family** — nothing runs the guard (KS-926) · running with its positive half dead (KS-927) · the wiring unasserted so deleting the call site leaves every test green (KS-928) · a branch no cell can red (#870's `A_FAIL`) · a type gate excluding the files it is credited with checking (#868's F3).

## Tonight's ledger against Wednesday, one line each
🔴 the pane close that killed #863's push (recovered by re-merge) · 🔴 **a ruling naming a proof path the schema refuses** — a backup code could never reach the handler, agent-caught pre-build (*a ruling is a pointer and Wednesday did not open it*) · 🟡 **an instruction to FILE two findings that carried only a count and a severity** — the agent refused to invent them and was right (*a count is not a finding*) · 🟡 a `%` escaped for printf's FORMAT inside an ARGUMENT, so a tap could not match its own subject · 🟡 three gate refusals on one brief, all pre-cost.

## Standing operational notes
A card add is ALWAYS its own tool call · a wrapped agent's pane is closed only when no tap is queued AND a capture shows no spinner · **never `fetch` / `merge-tree --write-tree` / `worktree add` in an agent's checkout** · the SELF-CHECK line is the canonical sentence + `| $(date)` with NOTHING between them · provenance entries carry three fields even when the middle is "not read", and a path outside Wednesday's tree is absolute or names its owner · **never escape inside an argument**; a `--mail` substring is copied from the subject file AFTER writing it · **a tamper does not count until its subject's hash is shown to have changed** · a merge is verified from objects with a real-object containment control BOTH ways in one batch · **an instruction to file a finding carries its text verbatim or names the mail and section** · QA wrappers red-proofed rc 6 / rc 7 before arming · `git grep -a` / `git diff -a`; `core.fileMode` false; `env bash` 3.2; `/bin/dash` present · the two daily notes are ~600 KB — read the newest seat block, the rotation block and this file, never whole.
