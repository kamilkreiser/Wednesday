Wednesday -> Seat A third successor (Secuura/Blockchain)

## BLUF
RULED: Kam ruled card `secuura-ks1194-failed-save-answers-200` -> **fail-closed** (panel card tap 2026-09-17 07:50:34 AEST, view=wednesday; reconciled 07:51:12). The chosen option, verbatim: *"Seat A builds it"*, detail *"failed save answers 503; approve raises the level only after the row persists; tier-1 gate; merge held for your tap"*.
**This SUPERSEDES your successor brief's QUEUE item 7** (KS-1194 "on its card default ... mail a one-line QUESTION to confirm the card is still on its default"). The card is RULED, so no confirming QUESTION is needed. **Everything else in item 7 stands.** KS-1194 is the same file as A16 (auth `routes/users.ts`), so it runs strictly serial after A16 merges and needs a free slot. **Even after a gate GO, the merge WAITS for Kam's tap, relayed by Wednesday.**

## Recommendation
1. Post a KS-1194 comment quoting the ruling verbatim (the choice, the detail, the tap time). This is the same first-turn exception as the other two ruling comments (ITEM 0 step 3), gated on the previous comment's rc. Name the comment id in your plan confirmation.
2. When KS-1194 comes up in the queue, propose the fail-closed shape and its file census in a QUESTION before building. It should cover: which call sites save (`saveVerificationRequest` at `users.ts:1147` and the review approve path), what a caller sees on 503, and the ordering of the level raise after the row persists.
3. No reply needed to this mail beyond the comment id in your plan confirmation.

## Detail
- Queue order after this mail is unchanged: GO #1016 merge → #1014 waits for its delta gate → KS-1195 build → KS-1187 severity reads → A16 KS-1050 → A11 KS-1101 → KS-1194 (ruled) → the gdpr x-user-email ticket candidate.
- Holds unchanged: nothing to Peter or Stuart; no deploy; no local stack; Kam's 40% cap.
