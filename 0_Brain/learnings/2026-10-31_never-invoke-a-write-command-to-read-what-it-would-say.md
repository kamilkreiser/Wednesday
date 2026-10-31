---
date: 2026-10-31
type: correction
source: Kam, live board 2026-10-31 15:40:47 view=tuesday ("this ticket does not make sense"), on a junk card the Tuesday seat posted
status: live
---

# Never invoke a write command to read what it would say

**The rule:** to learn what a tool knows (earlier rulings, a usage line, a refusal list), read it through a READ path: the tool's header (`sed -n 1,40p`), its `show`/`list` verb, or its store file through an inclusion filter. Never run its write verb (`add`, `post`, `create`, `send`) with dummy values on the expectation that it will refuse. And never filter the output of a command that can write: the filter hides the one line that says it wrote.

**What happened (s210, 2026-10-31 14:4x).** To list Kam's earlier rulings on a subject, I ran `decision_queue.sh add --id x --bluf x --option a:x --option b:y` and grepped its output for `CARD` lines. A minute earlier the same probe had been refused by the prior-rulings gate, so I assumed it always would. This time the subject words differed, the gate did not fire, and the card was added and posted to Kam's live board (HTTP 201). My grep hid the "added" line, so I did not know until Kam tapped it at 15:40:47: "this ticket does not make sense". It was withdrawn with the reason and an apology on the board.

**Diagnosis (w=2, mandatory).** This is the third time the same shape has cost something: the 2026-10-18 and 2026-10-24 probe rows (DRAFTER_RULES fence 5: "Read a tool's usage from its header, never by invoking it") were drafter-side; this one is the coordinator's own. The root cause is the same: I treated a refusal I had seen once as a guarantee and used the write path as a cheap read. A gate's refusal depends on its inputs; it is not a read-only mode.

**How to apply.**
- Earlier rulings on a subject: `kam_rulings_today.sh` for today, `decision_queue.sh show <exact id>` for a known card, or read the store file with an inclusion filter. If a real `add` is then refused by the prior-rulings gate, read its CARD list as part of that real attempt; never fake one.
- Before any command I am about to pipe through `grep`, `head` or `tail`, ask: can this write? If yes, run it unfiltered, or do not run it.

Related: [[2026-08-07_a-check-that-cannot-fail]], DRAFTER_RULES fence 5, `_ledger_laptop_datasec.md` row 2026-10-31.
