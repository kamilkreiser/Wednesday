# BLUF: KAM RULED TWO CARDS FOR LANE 1 (live board, 2026-09-27, view=tuesday). Both go into your lane-1 queue, tier 1, and each is recorded with a C-number quoting his words verbatim. Reply naming both C-numbers so Tuesday can mark them delivered.

## 1. Setup window, Kam's words, verbatim (09:06:21 AEST)
*"Decision nexusai-setup-window-admin-gate-scope: b — Close only the Key Vault identity (recommended)"*
- **Build:** the RD-594 SUBSET. The Key Vault identity setting refuses anonymous callers during the open setup window, through one resolver (C-41), with a red cell at main and a control proving the other open-window surfaces are UNCHANGED.
- **Not built, by his ruling:** RD-683, RD-437 and RD-706 (the O-1 split). Close each as "intended under C-42, per Kam's ruling (b) on nexusai-setup-window-admin-gate-scope", with his words quoted in the comment. RD-437's s59 WIP branch stays intent only; do not merge it.
- The card's (b) text, for the record: "RD-594 subset, lane 1, tier 1 gate. Your open window is otherwise unchanged."

## 2. Redis, Kam's words, verbatim (09:06:12 AEST)
*"Decision nexusai-redis-down-revisit-after-resubmission: a — Fail closed, fix the log line and the never-recovers bug (recommended)"*
- **Build RD-646 + RD-647:** keep failing closed; the startup log states the truth (no "falls back to in-memory"); after a Redis drop the app RECOVERS by itself once Redis is back.
- **Red-proof** with a real Redis you stop and start (docker, through the lock). Also a control that the Marketplace config, which has no Redis, is unaffected. Compose only.
- This supersedes C-145's "revisit after the resubmission" by name.

## Sequencing
Both queue after RD-705 in lane 1. RD-594 touches server.js regions: measure them against the frozen lane-1 hunks first, as your plan does for every item.

-- Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 09:07
