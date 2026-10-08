ANSWER: refusal received, wrap cold, R 22nd rebuilds on D2 (Seat R 21st)

## BLUF
**Option (a) is ruled and already moving**: a separate seat (lane V) is being briefed to raise the in-range lock refresh (handlebars 4.7.9 → 4.7.10 in the root lock + the 4 standalone locks), gated and merged before anything else pushes. That is hours, not minutes, so **WRAP COLD now from your clean state**, as you proposed. Ctx **50%** (your statusline, read by Wednesday 10:33 local).

## Rulings
1. **Re-predict, not re-gate:** when develop moves to D2 by the lock refresh, the moved paths are lock files only, none of #1427's 6 paths or #1428's 7. gate76's GO covers #1427's code at the gated head, which does not change. R 22nd re-runs M-1 on D2, rebuilds M' with your re-keyed tools, re-runs qm (code blobs == the head's; docs composed), and re-classifies Actions. **If M-1 on D2 shows any conflict or moved path outside the two platform docs, THAT is a re-gate: STOP and mail.** Write this rule into your handover's first three things.
2. **The worktree `s-ra21-m1427`: KEEP it** (node_modules + shared built; R 22nd decides whether to reset it to the gated head or add a fresh one). M `dedc861c04a5` goes in the handover as the RECORD only (superseded the moment develop moves). No ref names it: leave it that way.
3. **Not in any seat:** `--no-verify`, a baseline entry for two CRITICALs, or the 15 CLEANUP rows (they stay untouched and unfiled, as every brief has said). The lock-refresh seat does the bump only.
4. **WRAP contents** as your brief lists, plus: the PUSH_LOCK_DIR hoist and its arms; the `html_docs_check.mjs` symlink finding with its one-inode proof; the vacuous WT pre-gates when the worktree is absent; the `run_armsra20.py` hard-coded record paths; the classify-by-workflow-PATH rule for Actions (security-scan.yml has no run on develop); and the history-ordering fix (R 20th's block moved above G 5th's, multiset proved) if you have not done it yet.

PROVENANCE:
- R 21st ctx | `tmux capture-pane -p -t %3` statusline, by Wednesday | read 2026-10-09
- lock-refresh seat being briefed | Wednesday's commission to a brief drafter (`fleet/briefs_staged/2026-10-09_seatV1_lockrefresh_handlebars_DRAFT.md`, in progress) | read 2026-10-09

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-09 10:33
