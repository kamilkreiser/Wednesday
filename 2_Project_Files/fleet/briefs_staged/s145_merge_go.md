# MERGE GO — #884 (KS-858/F5). Wednesday's authority, and it always was.

## BLUF
**MERGE #884.** It passed its tier-1 re-gate: F5 closed on BOTH request-target forms, F-QA-2 pinned in
both directions, the KS-953 line-number repair verified with a clean three-way control.
**This is Wednesday's word, not a relay of Kam's** — merges have been Wednesday's to authorise since
protocol v1.3 on 2026-08-07, and Kam reconfirmed it at 09:40 today: *"for this week, you can give the
go ahead to merge as it becomes relevant so that I'm not slowing things down."*

**Do this BEFORE round 3 on #876.** It closes a confirmed unauthenticated bypass that is live on the
demo, and it unblocks a client disclosure.

## THE MERGE
1. **Re-read `ls-remote` first** and merge the SHA the gate actually passed — **`64e457943`**. If the
   head has moved, **STOP and mail**: a verdict is a receipt about a SHA, not about a PR.
2. Merge into `develop`. **Predict the tree oid before the merge and verify it after** — a merge
   receipt saying "no conflicts" is a claim about a process; a tree oid matching an independent
   prediction is a claim about the artefact.
3. **Verify from objects, not from the API's word:** parents held, the gated commit contained, and a
   control that fires.
4. **`develop` has not moved all day** (`306d0db92`). If your merge is the first, say so in the receipt
   with the before and after.
5. **Nothing else merges.** Not #876, not #882, not #885, not #880.

## WHY #880 IS EXPLICITLY EXCLUDED, and this is the line that matters
**A merge is Wednesday's. A merge that makes an EXTERNAL COMMITMENT is Kam's.** #880 (KS-577) silently
picks Option 1 for Platform S — a Stuart-facing contractual choice — so merging it decides something
with a client. **That stays with Kam and this grant does not touch it.** If any other PR turns out to
carry a decision of that shape, stop and say so rather than merging on this GO.

## AFTER THE MERGE
- **Do NOT tell Peter or Stuart anything.** The F5 disclosure is drafted and is **Kam's to send** —
  external communication is his signature class and no merge authority changes that.
- Report the merge: before/after SHAs, tree oid predicted and observed, and the control that fired.
- **Then** start round 3 on #876 as briefed — regression only, six spellings.

PROVENANCE:
- That #884 passed | the QA verdict `[QA -> Wednesday] Secuura KS-858/F5 round 2 (#884, tier 1)`, 2026-09-06T23:08Z | read 2026-09-07
- The SHA the gate passed, 64e4579433c7f93e9025b62b97ed58137225d90c | that verdict's own "SHA gated" line, re-read at its close as unchanged | read 2026-09-07
- Kam's 09:40 reconfirmation and the v1.3 grant it restates | his panel message, and `0_Brain/learnings/2026-08-07_protocol-v1.3-signed-delegation.md` in WEDNESDAY's tree | read 2026-09-07
- That #880 carries an external commitment | s141b's wrap of 2026-09-06T15:21Z: "merging as-is silently picks Option 1 (instant revoke) for Platform S" | read 2026-09-07
- Whether develop has moved since 306d0db92 | re-read it yourself before merging; Wednesday last read it at 09:0x | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 09:41
