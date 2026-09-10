---
date: 2026-09-11
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at the 50% checkpoint (~08:0x AEST) by the seat that booted 06:03. The previous version (2026-09-10 19:5x) is fully overtaken: #935 merged, KS-1067 closed, #951 gated NO GO, three new seats running.
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-11 ~08:0x. THREE SECUURA SEATS ARE RUNNING. KAM IS AWAKE AND RULING.

> Full narrative: `0_Brain/daily/2026-09-11.md`. **Measure before acting on any line here** — it is a representation.

## 🔴 WITH KAM — the one that is urgent

**`secuura-ks597-bind-compares-two-id-spaces-now-deployed`** (card, rec B). Kam's 09-07 `bind` compares Platform S's externalRef GUID against K's `organizations.id` raw → every S originate 403s (Stuart measured 144 in 45 min, local). **Both kintsugi and demo-pk serve the post-`48c4d8053` spec (PROBED 07:4x — live `organizationUuid` description matches the wording `48c4d8053` introduced, its parent `718008cef` lacks).** S refusals on the boxes = INFERRED, not observed. **Stuart has NOT been told — Kam's conversation.** ⚠ **ALL DEPLOYS HELD until Kam rules** (s172 Phase 3). ⚠ Instrument trap: a case-sensitive count of `acting Organisation` reads 0 on the live spec — the text is `ACTING`.

**Also his, unchanged:** `raise-to-1` on the `require-pr-gates` ruleset (PAT 403) · the agent GitHub identity invite (ruled 2026-08-26) · four extranet decisions (KS-721, KS-662, KYC image disposal, Actions billing) — **never `POST /api/seen`** · **approvals on Peter's PRs** (#896 draft reply exists; #933/#952/#899/#900 reviews in flight) · **tell Peter #951 is NO GO** so he skips it (his triage ranks it #2) — suggested to Kam 08:0x.

## 🟢 FLOOR — measured at ~08:0x

| pane | seat | lane | next event Wednesday owes |
|---|---|---|---|
| `%4` | **s172** Secuura/Blockchain | MERGE: 12 Peter-approved PRs (squash, API, sha-pinned) → #879 asks + #813 `minLength` → **Phase 3 HELD (KS-597)** → Peter's 16 "Kamil's court" PRs + #942 | its merge receipts; any CHECKPOINT for a suite slot; the orphan-defects ticket; the four-launcher-findings ticket |
| `%6` | **s173** Secuura/Blockchain-B | REVIEW: Peter's #933 → #952 → #899 → #900, #896 shape, approves nothing | **one review mail per PR → Wednesday drafts the reply for Kam** (template: `5_Project_History/2026-09-10_peter-protocol/DRAFT-reply-to-peter-896.md`) |
| `%7` | **s174** Secuura/Blockchain-C | #951 ROUND 2 (last under the cap): F1 mint only to originate + F2 wiring tests that bite + F6 claim fixes; F3+F4 one follow-up ticket | **its READY FOR QA → commission the round-2 tier-1 gate** from `fleet/qa-agent/launchers/launch_qa_secuura_ks1041_951.sh` as template, **naming round 1's report path** (below) and the NEW head |
| `%1` | monitor | — | — |

**Round-1 #951 report:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1041-951-dd0a0c934-tier1/report.md` — NO GO, F1 verified at source by Wednesday (`proxy.ts:254-256`, no originate guard).

**Rulings given to seats today (already in their mail — do not re-rule):** squash per `CONTRIBUTING.md:107` (not merge commits; standing line 47 SUPERSEDED) · non-runtime PRs (#866, #875, #921, #773, #878) → `Done`, **assignee kept** · #813/#879 held · #942 conflict by merging develop in, no force-push · s173's three readings all YES.

## 🟠 NAS — re-running under launchd since 07:27

Kam ruled `narrow-hard` 07:23. `scheduler/nas_sync.sh` now defaults 9 basename ignores for `AGENT=wednesday` (`Datasec TUESDAY node_modules worktrees .venv __pycache__ .next .turbo .pytest_cache`) — **proven on the live unison command line.** Log: `scheduler/logs/nas_sync_wednesday_2026-09-11_072731_86596.log`. ⚠ **DO NOT EDIT `nas_sync.sh` WHILE THIS RUN IS LIVE** — bash reads it by offset; that exact edit killed the previous run's report this morning. Owed when it ends: completion, `Deleting` count, rate — to Kam and Tuesday.

## 🟡 OWED BY WEDNESDAY

1. **Peter corrections, drafted for Kam:** #813's withdrawal is counted "approved" by his triage tool; #900 is reported merged and is OPEN.
2. **Draft replies for Kam** as each s173 review lands.
3. **Family-weight index** (Kam's `measure-first` ruling → `0_Brain/reference/2026-09-10_ledger-fire-measurement/MEASUREMENT.md` recommendation #1) — claimed, not started.
4. **Mechanisms owed from today's ledger:** a pretooluse refusal of `PIPESTATUS` (zsh) · case-insensitive phrase counts · inbox reads filtered on SUBJECT tags, never on From (the QA verdict arrived From: Wednesday) · `send_brief.sh` double-prefixing a subject that already carries a routing tag.
5. **19 → 18 undelivered Secuura rulings** (`decision_queue.sh list ruled --undelivered secuura-`); KS-1077's was delivered today.

## ⚠ TRAPS MEASURED TODAY

- **The Bash tool is zsh — `${PIPESTATUS[0]}` is empty.** Capture to a file and read `$?` on its own line.
- **After Kam's account switch the `%0` statusline has no `7d:` field** — read the allowance from a seat pane (58% at 08:0x, renews ~1d 20h).
- **Two seats booting together overwrite one `.launch_preflight_last.txt`** — ask each seat for its own preflight in its plan confirmation.
- **Peter's triage is a representation:** it counted a withdrawn approval as approved and an open PR as merged. Measure every row before acting on it.
