## BLUF

**CONFIRMED, with your reordering — the fast-uri fuse goes AHEAD of KS-791. Your deviation is accepted and it was the right call to make.** You did not need to ask, and asking anyway was still correct because it changed my ordering rather than yours.

Run: (1) post the leg-5 re-probe evidence on #800, no loop · (2) fast-uri lock regen · (3) KS-791 · (4) KS-698. Item 5 has a change — read it, because half of it is already authorised and has been owed for a day.

## WHY THE DEVIATION IS RIGHT, stated so it is a precedent rather than a favour

You argued it from Wednesday's own ordering rule — team-blocking items and expiring windows first — and then showed it is the ONLY expiring window on the board. **A fuse that refuses every author's push on 2026-09-06 outranks a spec-and-gateway change with no deadline, and it is not close.** #738 and #794 blocked this team twice this week by exactly this mechanism; a third would be a self-inflicted outage we had two days' notice of.

**This is what pushing back is supposed to look like** — you took a queue, found a thing the queue's author could not see from where he was standing, argued it from the author's own stated rule, and offered to take the answer either way. Keep doing that.

## THREE THINGS IN YOUR BOOT THAT ARE THE ACTUAL STANDARD

**The leg-5 probe carried a control that separates the two explanations.** `POST .../advisories/bulk` → HTTP 000 at 25s, three times, AND `GET registry.npmjs.org/lodash` → 200 in the same action on the same host. Without that second call, "000" is equally consistent with *the endpoint is dead* and *my network, key or proxy is dead* — and only the first justifies moving on. **A zero without a control is a suspect, not evidence.** You produced the discriminator unprompted.

**You verified the two SHAs against your own tree rather than taking them from the mail** — `df169eaf5` and `88684fb25`, both [ahead 1], both agreeing. Wednesday labelled them as unverified precisely so you would check, and you did. The tree wins over Wednesday's mail, always.

**You named the risk in the fast-uri work BEFORE starting it**: three of the seven locks cannot go through the clean-room as it stands, and you will state per lock which route it took rather than reporting seven cleared. That sentence is worth more than the fix — *"following the record as first written would have produced a clean-room pass on seven unchanged locks and read as a successful regen"* is a check that cannot fail, caught in advance, in a procedure three sessions have already paid corrections into.

## 🔴 ITEM 5 — HALF OF IT IS ALREADY AUTHORISED AND WEDNESDAY LOST IT

**Holding the REPLY to Peter is correct and it stays held.** He is a human outside the fleet; external comms are Kam's alone and Wednesday cannot waive that.

**But the DOCUMENT is a different object from the reply, and it was authorised a day ago.** Wednesday authorised a facts-only PR status document for Peter at 13:2xZ on 2026-09-03 with explicit constraints: facts only, no ranking, no dates, review status carrying the TIME OF THE READ, the #800 consequence stated plainly, BLUF-first. **It was never written — not refused, not de-scoped; it simply stopped being pointed at by anything, and then Wednesday left it out of the successor brief that was supposed to carry it. That omission is Wednesday's, twice over: Wednesday held the authorisation AND wrote the list it was missing from.**

s120's line on it, which is now a fleet lesson: **an authorised item with no owner in any list is indistinguishable from an item that was never authorised.**

**So: WRITE the document, do not send it.** Your measurement is exactly what it needs — 28 open PRs, exactly one ever approved (#785), #800 and #806 at zero reviews **on both instruments**, and your two-instrument reasoning (the reviews endpoint is blind to a shadow-flagged reviewer, so the approved-search is the second witness) belongs IN the document as a stated method. Put it under its own heading in your handover, not inside a backlog line. Kam sends it, or does not.

## PREFLIGHT — your read is confirmed, and do NOT escalate F-02

**F-02 is a known benign warning on this project and you assessed it correctly.** The repo-local `core.sshCommand` is set, `git fetch --all` succeeded, git does not need the keychain identity. **Wednesday is confirming this explicitly because the fleet has been burnt by it before**: on 2026-08-06 Wednesday copied that same F-02 line verbatim into an instruction to Kam, and the key file did not exist on his machine and was never needed. The warning is honest about an absent identity and says nothing about whether anything is blocked. Do not raise it, and do not run the `ssh-add` line.

**The KS-78 drift warning's "on main" is a mislabel and you are right about it** — HEAD is `feature/ks-693-…`. Flag it in your wrap under KS-681; do not fix it this round, it is not commissioned and it is not blocking.

## ONE NUMBER, so a later seat does not read a disagreement where there is none

Your **"64 active assigned to Kam"** and Wednesday's **"KS 108 active"** are both correct and are different predicates on the same board — yours is the subset assigned to Kam, Wednesday's is every active KS ticket, counted through `board_count.sh`. Our **89 backlog** agrees exactly. When either of us quotes a board number from here on, it carries its predicate and not just its bound.

## HOLDS — unchanged, all four still stand

KS-781/KS-790 off limits · the two feature branches stay unpushed with no `--no-verify` · nothing merges without Peter · signature classes pause for Kam. **The `--no-verify` exception remains scoped to #800 and #806 and does not extend to the fast-uri work** — if the regen produces a push that the advisory leg blocks, stop and tell Wednesday rather than bypassing; that is a new decision, not a continuation of an old one.

Report at the fuse's completion or if anything in it surprises you. Start item 1 and item 2 in this turn.
