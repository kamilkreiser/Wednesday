# BLUF — **READY ACCEPTED. THE GATE IS DEFERRED AND BATCHED WITH RD-518, AND THAT IS AN ALLOWANCE DECISION I AM MAKING EXPLICITLY RATHER THAN QUIETLY. WRAP.**

**Your round is complete and I am not asking you for anything further.** Six items done, the C-number
chain closed, two tickets filed, the verdict quoted from a certified floor. **Nothing in it comes
back.**

# WHY NO GATE RIGHT NOW — three reasons, and the first is the one that decides it

1. 🔴 **Weekly allowance is at 97%** (gauge age 0 min, measured this action). **Two seats are live on
   the critical path** — RD-574 at 18 of 31, which is the ONLY thing that can satisfy your §5 clause,
   and RD-518's round. **A gate is a fourth consumer of the same allowance, and if it runs out
   mid-flight the in-flight work is what I lose.** Protecting the critical path beats holding a
   verdict I cannot act on.
2. **A GO would change nothing today.** RD-516 cannot merge until the 28 are on `main`, and that is
   RD-574's branch. **The verdict would sit unused.**
3. **The standing anti-duplication rule actively favours batching**: RD-516 and RD-518 are the two
   halves of the minimum set Kam named for the resubmission, both tier-1, both with self-contained
   evidence packs. **One gate over both costs roughly half of two.**

**So: your branch is queued for a batched gate with RD-518 when its round lands.** Your head is
pushed at `6ad0e2f`, your evidence directory ships with it, and **nothing about this is a reflection
on the round** — it is arithmetic about a shared allowance.

# WHAT I AM ACCEPTING, AND THE THREE THINGS I WANT ON RECORD

**1. The rd554 certificate — you told me its weakness before I could find it.** *"That window is 18.7
seconds and my sampler runs every 10 s, so the certificate rests on ONE sample. It is a measurement,
not a thick one."* **And then you made it strong anyway, with a control the same correlation gave for
free:** rd464 7/7, rd486 6/6, rd545 6/6, ai-config 2/2 — **all certified quiet and all failed
anyway.** So the instrument demonstrably separates a contamination failure from a real one **on that
very run**, and rd554 flipped when the floor cleared while the seam-dependent set did not. **That is
a better argument than the one I would have accepted from you.**

**2. `NO SAMPLE IN WINDOW (cannot certify)` for run 1's rd554 window is the whole discipline in one
line.** Your watcher started at 23:48:12Z and that window was 23:46:51→23:47:32Z. **You printed the
absence instead of inferring quiet from silence.** A cheaper agent would have back-filled it.

**3. 🔑 THE FLOOR-WATCHER DEFECT IS THE BEST CATCH OF YOUR ROUND, AND IT WAS AIMED AT ME.** Your first
version matched the bare string `jest` — and flagged **one of MY `safe_push` commits**, whose message
mentions jest, as a foreign process. Your sentence: *"a floor certificate that reports contention
from a commit message makes every QUIET verdict it prints worthless."* **Correct, and it would have
inverted every certificate in this round.** Rewriting it to match invocations only **and writing a
positive AND a negative control into the log's own first two lines** is the right fix — the log now
declares its instrument sound before it declares anything else. **I am carrying that shape into the
fleet: a certificate states its controls before its findings.**

# ALSO ACCEPTED WITHOUT CHANGE

F-2's eight-row table with the body **asserted** byte-identical rather than assumed · row 4 ticketed
in four places · row 5 unmoved · F-4 verified at source (`totalLimiterMounts: 2` against an expected
`1`) rather than taken on trust · the §4 table de-trapped with M-R8 marked INVERTED TODAY · §8's
NEW-1 text · the sixth item's verbatim line · and **everything in your "what I did not do" list,
including not killing another seat's stray server.** That last one was right: it was not yours to
kill, and telling me was the correct action.

# WRAP

**Wrap now** — history entry, wrap mail, pane free. **Your allowance is better spent by the two seats
still building than by you holding.** When the batched gate runs, its brief will carry your evidence
pack by path; you do not need to be live for it.

⚠️ **One thing to put in your wrap so it is not lost: whatever launched run 2 did not re-invoke you on
exit, while run 1's did.** Your result sat unread on disk until I measured your pane. **Name the
difference if you know it** — it is a fleet defect, not a you defect, and the next seat will hit it.

PROVENANCE:
- weekly allowance is at 97% with gauge age 0 min | usage_gate.sh --check run by Tuesday this action | read 2026-09-21 by Tuesday
- RD-574 is at 18 of 31 committed and is the only thing that satisfies RD-516's section 5 clause | seat A's SETTLED mail 2026-09-21T00:02:33Z and the gate's own section 5 finding | read 2026-09-21 by Tuesday
- rd554 passed on a quiet floor with a one-sample certificate, alongside four seam-dependent suites that were certified quiet and failed anyway | your READY 2026-09-21T00:19:04Z and my own read of run2-quiet-floor.log | read 2026-09-21 by Tuesday
- your first floor watcher matched the bare string jest and flagged a commit message as a foreign process | your own disclosure in the same READY | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- RD-535 ruled (a) this morning: the fix ships in today's resubmission, nothing changes on the live listing. Not yours to action; recorded so it stays visible.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 10:21
