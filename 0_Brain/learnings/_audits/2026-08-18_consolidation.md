# Consolidation audit — 2026-08-18 (Tuesday 06:xx, signing-day morning, fleet floor: one agent working)

Window: **2026-08-16 (Sunday's audit) → 2026-08-18**. Short window — the ritual runs in
the first session after Sunday; Sunday's own audit ran mid-Sunday, so this covers the
16th's evening and the 17th (the densest single day on record: six Secuura legs, HPSM
s26, four Kam architecture inputs, DESIGN_AGENT built, the chat de-dup fix). **Kam skims
this — nothing below took silent effect except the items marked BUILT, which were
exercised before reliance.**

## Boot cost (Kam's standing item — number and trend, deltas still NOT run)

| Component | Bytes | ~Tokens | Share | vs 08-16 |
|---|---|---|---|---|
| **Lessons** (65 files) | 227,555 | ~56,900 | 39% | +2.7K (3 new files) |
| **Ledger** | 128,312 | ~32,100 | 22% | +2.5K |
| **Last 2 daily notes** | 103,231 | ~25,800 | 18% | **−19K** ✅ |
| **INDEX + decision_queue** | 118,281 | ~29,600 | 20% | **+6.5K** ⚠️ |
| identity + people + CLAUDE.md | 11,735 | ~2,900 | 2% | — |
| **TOTAL** | **589,114** | **~147,300** | | **−7.5K** |

**Trend: down for the first time (155K → 147K), and the drop is exactly where the 08-16
audit pointed** — daily notes came back under control (08-17 ran 35KB against 08-14's
117KB). **The new growth driver is INDEX.md's refresh-block stack**: every session
prepends a dated block and none are ever retired; it is now the second-largest artefact
after the lessons. Candidate delta (NOT run — Kam's "let's keep an eye on this" =
monitor): archive refresh blocks older than 7 days into `projects_index/_archive/`,
same pattern as `_audits/`. The 08-16 proposal set (boot digest · ledger row archive ·
decision_queue pruning) remains staged and unrun.

## Promotion EXECUTED: the pre-send self-consistency read is now a gate (three strikes)

Three briefs contradicted themselves while every per-line gate passed (08-13 w=5
"already invoiced" vs its own constraints section · the w=8 mixed provenance block ·
08-17 s26 "exactly once" vs "2 hits"). Per the w≥3 rule, instruction is proven
insufficient → **BUILT into `send_brief.sh`**: every `--kind brief` must carry a
fresh, TODAY-dated `SELF-CHECK: re-read end-to-end for contradictions | date time`
line; missing → refuse, stale-dated → refuse. Same mechanism class as the provenance
gate, honest limit stated in the script: it cannot know the read happened — it converts
omission into a deliberate falsehood, and that shift is the mechanism. Helper
`fleet/self_check_view.sh` extracts the claim-bearing lines (repeated ticket IDs
grouped, number lines, absolutes) so the read is targeted. A mechanical contradiction
DETECTOR was considered and rejected: it would false-positive on legitimate contrasts,
and a gate that blocks legitimate sends gets routed around (w=8 lesson).

**Exercised before reliance, and the exercise caught a real defect:** the first draft
accepted the UTC date as "today" — AEST is UTC+10, so **every morning before 10:00 a
stale attestation carried from last night would have passed**. The stale-path test did
not refuse; fixed to local-date-only; all four paths then proven (no-line refuse rc=1 ·
stale refuse rc=1 · fresh pass rc=0 · `--kind answer` exempt rc=0).
[[2026-08-07_a-check-that-cannot-fail]] applied to the check being built, again.

## DGM validation of recent mechanisms (evidence, not adoption)

- **Queued-ticket freshness gate** (built 08-17): ✅ VALIDATED — refused two real sends
  the same day it was built, and the live read it forced corrected a brief (KS-487 was
  In Progress, not Todo). Also fired correctly this morning (KS-570 named in queue
  context → forced a live read).
- **Scope-claim gate** (built 08-16): ✅ VALIDATED — fired on the one real brief carrying
  the defect; two false positives found and fixed by running it against real briefs
  before arming.
- **`wake_wednesday.sh` fix (WED-111)**: ✅ VALIDATED — first live fire 2026-08-18 06:00
  PASSED: tap into the live pane, no second coordinator, `ps` shows exactly one. The
  four-day daily coordinator leak is closed.
- **Chat de-dup watermark** (built 08-17 on Kam's correction): ✅ VALIDATED — proven live
  on his next message; no double-reads since.
- **Relative-path + provenance gates**: routinely firing (twice on this morning's brief;
  both refusals were correct and fixed by fixing the lines).
- **board_count.sh**: in daily use; every count this morning carried its predicate.

## Ledger review (rows since the 08-16 audit)

New weight movement: w=13 representations family (the ~20-minutes-vs-4 urgency number,
08-17 06:16) · w=7 stale-brief (ENFORCED same hour — see above) · w=4
enforcement-scoped-narrower (chat tap pattern, fixed + case-proven) · w=2
check-the-refusal (lesson file exists, applied all day 08-17 and this morning) · w=2
self-consistency family (ENFORCED today) · four w=1s (test-hook default → guard enforced;
mktemp STATE_DIR self-caught; watermark hand-seed self-caught; rotate tooling note).
**No weights retired** — the window is two days and nothing has earned retirement.
**Health metric honesty, unchanged from 08-16:** corrections are still caught by agents
and gates, not by noticing; the mechanism-caught vs reader-caught instrumentation still
does not exist. The 08-17 signs are good (two of the four w=1s were SELF-caught, and
the wake-fix review caught three defects pre-arming) but two days is not a trend.

## Merges / supersessions

**None.** Kam's 08-10 ruling stands (no lesson cutting without a system that provably
loses nothing). The four-lessons-one-shape cluster (recorded blocker · recorded
exclusion · appended classification · overstated register) remains cross-linked, not
merged.

## For Kam (skim list — nothing needs a decision this morning)

1. Boot cost 155K → 147K, first downward move; INDEX refresh-block stack is the new
   growth driver; all reduction deltas remain staged, none run.
2. The self-consistency gate is live on every future brief (attestation line). If it
   ever annoys you in practice, say so — a gate that gets routed around protects
   nothing.
3. Weekly industry scan NOT run this cycle (signing morning; short window). Owed at the
   next consolidation or a quiet slot this week — recorded as owed, not skipped
   silently.
