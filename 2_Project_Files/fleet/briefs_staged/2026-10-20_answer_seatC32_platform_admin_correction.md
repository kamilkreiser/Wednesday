## BLUF
Your correction is accepted and thanked: all three of your steps go ahead, and the code-comment fix for develop rides in the gap-2 PR as its own comment-only hunk. Two things are Wednesday's to own here, below.

## Your three steps and the develop comment
1. Correct the #1667 PR body, and comment on KS-1695 and KS 1536 with the untruncated census. Name the `head -20` cause as you proposed. Yes.
2. File the `documents.ts:1076` ticket with the census in it. Yes. Add the other three same-shape sites you found (`certifications.ts:123` and `:959`, `documents.ts:299`), and `adminConfig.ts:60` as the one list that DOES include `platform_admin`. Say KS 1536's "seven lists" is an undercount, with your count and its frame (non-test lines, `git grep` at develop 88933d5c7ebb).
3. The merged R18 comment on develop: fold the correction into the gap-2 PR, as a SEPARATE comment-only hunk in `certifications.ts`, listed in your READY as its own item with the same non-comment-multiset proof you used today (control included), so the gate can check it in one read. No separate PR.

## What Wednesday owns
- My ruling (a) on your round 2 and my CK1 gate brief repeated "platform_admin is a gateway-only spelling" from your plan and the gate's N2 note; I did not read `adminConfig.ts` or grep originate for the spelling myself. The rationale was a relayed fact I passed on as my own premise. The outcome (refuse) is unchanged; the basis is corrected.
- Kam has been told: card `secuura-platform-admin-spelling-certification-reads-1020` is on his board with the corrected facts. Recommended and default is (a), keep it refused and settle the spelling in the KS-1536 clean-up. If he rules (b) or (c) I will mail you; until then (a) stands.

## Provenance
- Your CORRECTION mail read whole; the `adminConfig.ts:60/:78` lines and the 41/4 counts are YOUR reads, not re-run by Wednesday (unread by me: `adminConfig.ts`).
- The card text read back from `decision_queue.sh add` output (id secuura-platform-admin-spelling-certification-reads-1020, HTTP 201).

## Unchanged
Idle on gap 2 until my "1654 merged" mail (gate CN1 is running).
