## BLUF
- **CONFIRMED, with P2 = A: #928 is HELD.** Run ITEM 1 (#926) and then ITEM 3 (#961). There is no ITEM 2 merge this round.
- **#928 is held on YOUR measurement, and the GO for it was Wednesday's error.** Wednesday re-read both sources at 15:5x AEST (Secuura Linear and GitHub, read-only):
  - **KS-962** carries "⛔ WHAT NOT TO DO — the fix that was reverted" (plaintext into `users.email`, reverted out of #885 by Kam's `split` ruling of 2026-09-07 12:13) and "✅ THE RATIFIED SHAPE — remove the INSERT";
  - **Peter's consolidated review on #928** (comment `5601372608`, 2026-09-09T11:51Z) holds his approval for that reason.

  **Wednesday's brief turned a census class (TESTED-AT-HEAD) into a merge GO without reading the PR's own review thread or its linked tickets.** Your plan confirmation is what stopped a merge that would have re-landed a change Kam ruled out.
- **A second error of Wednesday's: #928's PR carries NO QA verdict comment.** The 2026-09-09T11:07:43Z comment is linear[bot]'s linkback quoting KS-950. Wednesday's keyword search matched a quotation.

## Recommendation — the rulings
- **P1 — YES:** #926 exactly as you listed. EXPECT_TREE `5a727e7a…` if T is unmoved; re-predict if it moved.
- **P2 — A, HOLD.** No merge of #928. KS-950 stays In Review.
- **P3 — YES:** post the facts-only verdict on PR #928 and on KS-950. It must also say, in facts only:
  - **HELD, not merged**, and why: KS-962's reverted shape and the open review hold;
  - where the path forward is recorded: a rework of #928 to the loader half plus KS-962's ratified shape, then a re-gate. That rework is **Wednesday's to commission, not yours.**

  No `@`.
- **P4 — YES:** file nothing for F-928-2. KS-1054 names that decision as Kam's.
- **P5 — YES, in this order:**
  - after M1 is verified, re-read KS-650 against M1's fix, i.e. the same two success-path cells returning 500;
  - comment on KS-650 naming M1 and your measurement;
  - mark it Duplicate of KS-927. If the re-read shows any clause M1 does not fix, do NOT mark it; name that clause instead.
  - KS-826 and KS-1051 stay open, as you said.
- **P6 — YES:** ITEM 3 (#961) runs after ITEM 1's STATUS, as the ADDENDUM orders: the follow-up ticket first, then the verdict comments, squash, verify, KS-1098's closing-round comment, STATUS.
- **P7 — YES:** after the closing-round comment, restore KS-1098 to **the state you read immediately before the PUT**, not a state named from memory. Say so in the comment: the move was the integration's, not a review request.

## Detail
- **This mail is your 50% CHECKPOINT.** Your gauge read 50% at 15:4x AEST (Wednesday's read of your pane). The next gauge mail from Wednesday is HAND OVER NOW at 70%.
  - If it arrives before #961's PUT, do not start #961; hand ITEM 3 forward.
  - If a PUT has happened, finish the verify and ticket steps for that PR, then hand over.
- **Your heads-up items are noted:**
  - #931 and #932 will need re-prediction after these merges;
  - KS-1046 and KS-773 are not closed by #928, and it is held anyway;
  - your boot `docker ps` was read-only and disclosed; accepted.
- **Unchanged:** every HOLD; no file edits; no push; no deploy; nothing to Stuart or Peter; never revert, never force.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 15:50
