---
date: 2026-09-06
type: pickup
source: replaced wholesale by the 20:1x seat at its 65% handover refresh (22:1x)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Secuura: 4 merges tonight, seat B WRAPPING (successor OWED), 3 PRs under/awaiting gates; NexusAI PAUSED; Kam's queue = 1 card; Wednesday boots on OPUS for the week

**Kam tonight, verbatim, both executed:** (1) 20:19 *"change your boot script for the rest of the week to boot in opus 5 rather than fable. we are burning through credits a little too quickly"* — `Launch_Wednesday.command` pins `--model opus`, fable line commented in place, backup `.pre-0906-opus`, **`doctor.sh` holds the date: ok until 2026-09-13, WARN after**, both branches exercised. (2) 20:19 *"keep pushing the secuura agent to polish the platform to a ready state"* — the sort key for both seats' free-choice items, delivered into every brief.

## 🔴 CONSTRAINT WEDNESDAY TOOK — it binds the successor
**Seat B's item-4 launcher change (KS-911/912) is LIVE ON DISK and UNGATED** — `Launch_Claude.command` sha256 `932a2cc3…`, suite `b93b2c83…`; `.pre-ks911` `9609c845…` and `.pre-ks912` `a5d5d9ef…` equal KS-907's gated hashes exactly. **Do NOT relaunch or rotate a Secuura seat until it is gated — or restore both `.pre-` copies first (one `cp` each) and say so in the brief.** Its gate is unqueued and unstarted.

## The floor at 22:1x — every head from `ls-remote`, READ verbs only in agents' checkouts
- **Secuura develop = `ff5218867d3fabd1913fc43fdea442ef2afd81fc`**, verified from objects. Tonight's chain: `b77b20bf6` (#851) → `34fc749df` (#864) → `e1d840d8e` (#863) → `a821bd0aa` (#865) → `a8aa723a0` (#867/KS-913) → `ff5218867` (#868/KS-914). **The local `refs/heads/develop` is STALE — read `origin/develop`, never the branch name.**
- **`%121` seat A (s141)** — merged #867 and #868. Now on **F2** (the one regression #868 introduced: `deliverWebhook` lost its try/catch while `safeOutboundRequest` can throw despite documenting it does not — latent, reachability looked for and not found). Then F1/F3/F4/F5 tickets, the PR-body DoD via the REST API, then **KS-920**, then KS-926's campaign. Holds **#870** (KS-921 fix round @ `2f6b30fde`) awaiting a re-gate.
- **`%119` seat B (s140d) — WRAPPING at ~50%.** Has a **GO to merge #869 (`8b7d57cc6`) as part of the wrap**. Then KS-923 → TND, two harness Minors + the third-cell ticket filed, handover. **A SUCCESSOR BRIEF IS OWED** — its queue: #866 (KS-909, ungated), the third-cell ticket, KS-733, and the seat-B table under Kam's direction.
- **`%126` tester — #871 (KS-720, tier 1)**, running. **Gate queue after it: #870's fix round, then #872 (KS-732).** Two testers is tonight's ceiling on Kam's credit word; the queue is announced rather than re-shuffled.
- **NexusAI PAUSED** on Kam's 17:01 word. No pane. Resume only on his word at `!CODING/Datasec/NexusAI/HANDOVER-S42.md` §2.

## Owed by the successor, in order
1. **Seat B's wrap mail** → score the session → **write and launch the s140e successor brief** (respect the launcher constraint above).
2. **#871's verdict** (tier 1, running) → read whole → score → GO by SHA or a fix round.
3. **#870's fix round gate**, then **#872's** — in that order.
4. **Verify #869's merge from objects** if seat B lands it during the wrap; if it did not, the successor merges it with the GO quoted.
5. **Seat A's F2 READY** → gate (small round).
6. **Kam's card** `secuura-demo-kam-admin-default-password` (open, default HOLD) → if ruled, RULING RELAY to seat A + `--delivered`.
7. **KS-926's campaign** when it starts: it opens with **FIVE mechanisms of one family** — KS-926 (nothing runs the guard) · KS-927 (running with its positive half dead) · KS-928 (the wiring unasserted, so deleting the call site leaves every test green) · #870's `A_FAIL` branch (no cell can red it) · #868's F3 (a type gate excluding the files it is credited with checking).

## Tonight's ledger, in one line each
🔴 the pane close that killed #863's push (recovered by re-merge) · 🔴 **Wednesday's KS-732 ruling named a proof path the schema refuses** — a backup code could never reach the handler; agent-caught pre-build (w=139/23: *a ruling is a pointer and Wednesday did not open it*) · 🟡 a `%%` escaped for printf's FORMAT inside an ARGUMENT, so a tap could not match its own subject and an agent idled two minutes (quoting family w=4) · 🟡 three gate refusals on one brief (provenance block, provenance line shape, self-check line shape) — all pre-cost.

## Standing operational notes (carried + new tonight)
A card add is ALWAYS its own tool call · a wrapped agent's pane is closed only when no tap is queued AND a capture shows no spinner · **never `fetch` / `merge-tree --write-tree` / `worktree add` in an agent's checkout** · the SELF-CHECK line is the canonical sentence + `| $(date)` with NOTHING between them · every provenance entry carries three fields even when the middle is "not read", and a path outside Wednesday's tree is absolute or names its owner · **never escape inside an argument — `printf '%s' "$text"` passes text verbatim** · a `--mail` substring is copied from the subject file AFTER it is written · **a tamper does not count until its subject's hash is shown to have changed** · a merge is verified from objects (`cat-file -p` parents + tree) with a real-object containment control BOTH ways in one batch · a two-dot `diff` renders merged work as deletions — a PR's content is `merge-base..head` · `git grep -a` / `git diff -a` in this repo · `core.fileMode` false, so modes are index facts · `/bin/dash` present, `env bash` 3.2, Docker linux/arm64 · the two daily notes are ~500–600 KB — read the newest seat block, the rotation block and this file, never whole.
