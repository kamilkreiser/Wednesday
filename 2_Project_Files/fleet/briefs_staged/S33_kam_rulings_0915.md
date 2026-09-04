## TWO KAM RULINGS (panel, 2026-09-05 09:15 AEST) — relayed verbatim, with what each changes in your queue.

**1. RD-245 fix shape — Kam: "proceed — Proceed as ruled."** The (e)+(a) build at 2b3fe32 stands. Nothing changes; the veto is spent. Carry on with F-5 → F-4/F-6/F-7 and the batched gate at the end of the round.

**2. RD-303 + RD-307 — Kam: "untrack-and-quarantine — Untrack the six .azure files (git rm --cached, keep on disk) AND quarantine .machine-id after the agent proves nothing is keyed by it."** This INSERTS into your queue at its priority (both tickets are High) — after F-5 completes, before F-4/F-6/F-7, so both land inside the round the batched gate covers. Two separate commits, on the current branch, no history rewrite:

   **RD-303:** `git rm --cached` the six tracked files under `4_Credentials/.azure/` — they stay on disk; the ignore lines you added at the 09-04 wrap keep them out from then on. Commit message names RD-303 and that it is an untracking, not a deletion. Verify with `git ls-files 4_Credentials/.azure/` → empty, and that the files are still on disk. Comment on RD-303 with the SHA and move it to the state the board uses for done-pending-review.

   **RD-307 — the PROOF comes first, the move second, and the proof is the deliverable if it fails:** establish, from `encryptionService.js` and the data dir, whether anything already encrypted in that repo-folder data dir was keyed from THIS `.machine-id` (the fallback path — versus a key supplied by env/config). State the evidence class. **If nothing is keyed by it:** move `data/.machine-id` into a dated `_quarantine_2026-09-05/` folder beside it (never delete), commit nothing for it (it was never tracked), and record where it went on RD-307. **If something IS keyed by it, or you cannot tell:** do NOT move it; put the finding on RD-307 and mail Wednesday a QUESTION — that is the "after the agent proves" clause of Kam's ruling, and an unproven move would be the RD-294 shape with a key.

Both tickets: one comment each citing "Kam's ruling 2026-09-05 09:15 via Wednesday".

PROVENANCE:
- Kam's two rulings, verbatim | Kam's dashboard panel messages 2026-09-05T09:15:19 and 09:15:23 AEST, `0_Brain/dashboard/data/chat_log.json` — my project, not yours | read 2026-09-05
- The six tracked `4_Credentials/.azure/` files and the ignore lines added at the 09-04 wrap; `data/.machine-id` untracked, ignored, left in place | your READY FOR QA mail 2026-09-04T22:52Z (RD-307 paragraph) and Wednesday's 09-04 sweep (0 suspicious matches, firing control) recorded in NEXT-PICKUP.md 09-04 §5 — the sweep is my project, not yours | read 2026-09-05
- RD-303 To Do/High, RD-307 filed High | Jira REST search, project RD, and your 22:52Z mail | read 2026-09-05
