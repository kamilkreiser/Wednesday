---
date: 2026-11-18
type: principle
source: Kam, Friday's terminal 2026-11-18, while the lesson digest was being synthesised into a short rules card
status: live
tier: W
---

# A lesson is weighted guidance, not an absolute law: its weight is how often it has been reinforced, and repeats are kept as a count, not as more text

**The operative case.** I am about to write a lesson, a rule line on the rules card, a family file, or a ledger row; or I am about to apply a lesson to a situation. **Ask how often this has actually happened, and write and apply it with that weight.**

**Kam, verbatim:** *"with lessons, these should never be absolute. I like the reinforcement method, if something happens once, its worth taking note, twice - start of a pattern or reinforcement. multiple times and this becomes more important to pay attention to. Also, pmultiple entries do not need to be kept just their reinforcement"*

**Context.** He had asked what could be done about a boot digest too large to read (281 lessons, 8,030 lines), and the first card listed every lesson as an equal one-line rule. Earlier the same day an independent review found the one-line rules often overstated their lessons.

**How to apply:**
1. **Once = a note.** A single occurrence is recorded and worth knowing; it is not written as "never" or "always" unless the lesson itself is about a hard boundary.
2. **Twice = the start of a pattern.** It gets attention and a diagnosis (this is the ledger's w=2).
3. **Many times = pay the most attention.** High counts come first on the card and are the ones a seat reads before anything else.
4. **Repeats are stored as reinforcement, not as more entries.** A second write-up of the same rule is folded into the first line and adds to its count; the extra text does not have to be read, carried in the card, or kept in what a seat loads. (Friday's reading, offered to Kam for correction: the folded lesson files stay on disk as the record; they are not deleted.)
5. **The hard rules are not lessons.** Client separation, secrets, production, money, messages to people outside the team and irreversible actions are rules of the project rules file and stay hard at any count. (Friday's reading, same offer.)
6. **When applying a lesson, weigh it against the case in hand.** A low-count lesson that does not fit the situation is not obeyed mechanically; say what was weighed.

**Mechanism:** `2_Project_Files/tools/rules_card.py` computes each rule's count from the ledgers at every generation and orders the card by it; a superseded row passes its count to the line it was folded into.

**Related:** [[2026-08-03_frequency-weighted-reinforcement]] (the same principle, stated for the ledger; this file extends it to how lessons are written, stored and read) · [[2026-08-03_context-loading-split]] (his 2026-08-10 ruling: no cutting without evidence that nothing is lost).
