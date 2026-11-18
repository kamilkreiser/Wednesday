---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Brief provenance and pointers: what a brief or handover must carry so the reader can act on it

**The one idea.** A brief, a handover and a pickup line are the only world the next reader has. Every fact in one needs a source that was actually read; every pointer must lead to something that exists, is durable and is fit to answer the question; and everything owed (Kam's rulings, the coordinator's own rulings, a release, a ratified design, the limits of a fix) must be written where the successor is guaranteed to land. What is not written as an item does not exist for the reader.

## The rules

1. **When sending any brief:** send it through `send_brief.sh` with a PROVENANCE block, one line per fact: fact | source (path, URL, ticket, command) | read date. Take each fact from the authoritative record of the event, not from a summary of it; a summary written by another project, and my own ticket titles, are exactly where direction, ownership and causality get flattened. `2026-08-06_brief-provenance-enforcement.md`

2. **Before asking Kam or any human to run anything:** verify the preconditions myself, read-only (does the path exist, is the command needed, does the problem actually block us). If I cannot verify, say so in the ask ("I believe X; I could not check Y"). Prove the problem is real before spending someone's hands on it. `2026-08-06_brief-provenance-enforcement.md`

3. **For every "verify X from Y" in a brief:** open Y first and confirm it answers X correctly today; if I cannot, say so and name a cross-check. A file the brief asks the agent to repair is never ground truth for that repair: name an independent source. Withholding an unverified fact obliges me to make sure the verification path I name instead is sound. `2026-08-04_validate-brief-pointers.md`

4. **When a brief queues work on a ticket:** the provenance line carries the ticket's scope sentence (quoted), not only its state. If the brief commissions less than the ticket, say so as narrowing ("part 1 of 3 this round; the rest tracked before part 1 merges"). The item also carries the receiving seat's authority over it, read from the client's own rules file before the item is written; "author to merge" on a board says who is expected to merge, not which seat may. `2026-08-04_validate-brief-pointers.md`

5. **Before sending a mail that sequences, holds or releases something already sequenced (a pull request, ticket, deploy):** re-read the previous outbound to that agent for the same id. If the new mail changes it, name the earlier mail and item and say SUPERSEDES. The self-check covers Kam's rulings, the mail against itself, and the previous mail to this agent on every id named. `2026-08-04_validate-brief-pointers.md`

6. **When writing a successor brief, a morning sweep, or a card for Kam:** first list the cards Kam has ruled for that project since the last brief and ask, per card, where the ruling now lives. A ruling is delivered only when it sits in the artefact the next reader lands on (the row, ticket, pull request or comment); "relayed to a seat" is a step, not the receipt. Every successor brief carries a section "RULED BY KAM, NOT YET IN AN ARTEFACT" (each ruling verbatim with the artefact it must land in) and a second section "RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE" (each binding scope, hold or "do not" ruling from the coordinator's answers, quoted with its timestamp, built from the staged answers, not memory). Empty is valid; absent is not. A ruling meant to outlive its round is also written on the ticket by the agent in the same turn. `2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact.md`

7. **Before any sentence that treats a card's state as reality (undone, still binding, still open, still held, already done, closed):** open the artefact the card names. A card's mark records what a seat wrote down, never a fact about the world; an unmarked card means unknown, not undone. The over-cautious misreading is the dangerous one: a hold that looks like diligence can ride in every successor brief untested. A card carried into a brief's holds names the artefact checked and the date read, or is listed as unknown. `2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact.md`

8. **When a brief contains an unknown:** give it two clauses: why it is unknown and which instrument closes it ("unmeasured: no identity for that system here; read the comments endpoint in your first turn"). Never append a disposition ("not done", "still open") to an uncertainty. `2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact.md`

9. **When sending a GO, release or merge instruction:** it is owed work. In the same action as the mail, write it into the project's handover document and my own pickup; the mail is the content, the handover is the claim. Address the routing name, not a session letter, which expires at rotation. At the next checkpoint measure the thing itself (has the branch moved?), not the mail. A seat wrapping with an unexecuted GO names it in its handover, and the coordinator who sent it owns re-arming it. `2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact.md`

10. **When Kam ratifies a mock and I write the build brief:** a mock has two halves, what the page says and what the page is. Open the file and measure the layout into numbered, checkable properties (grid, chrome, tiles, chips, popover, table rules); "build it like the mock" is not a brief. Every later round cites the mock by reference and names which half it closes. The completion check asks both "does it match the brief?" and "does it match the artefact Kam approved?"; where they differ the ratified artefact wins. The QA brief gets the mock as an expected artefact. Any round that changes what a page is ends with rendered screenshots to Kam, both modes, before deploy. `2026-09-03_a-ratified-design-has-two-halves.md`

11. **When a handover, note or brief names a mechanism I used (a gate, watcher, probe, launch):** write the path of the file that runs it. Never a pane id, pid, port or "the wrapper" in its place; runtime ids may sit beside the path. Before writing a tool anywhere, run `git check-ignore -v <path>`: tooling a successor must find belongs in a tracked path; state drawers hold state. Misplaced tooling is moved, not un-ignored, and not while something is live on it. When a mechanism cannot be found, never compose a plausible launch command (it may work and bypass the guard): keep reading the source or say it is unrecorded. Test: could a seat on another machine, from a fresh clone, run it from the handover alone? `2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id.md`

12. **When a handover, wrap or pickup says prepared, staged, ready, queued, built or waiting:** name the durable path inside the project tree, or do not use the word. Never a temp directory, a session scratchpad, or "my worktree" without saying which and whether it is pushed. If it is not durable, say so: "drafted in this session's scratchpad, will not survive it, re-derivable from X". This binds the coordinator's own handovers too. `2026-09-20_prepared-in-a-scratchpad-is-lost.md`

13. **When partitioning work across seats that share one inbox:** each row carries what a seat can measure about itself (pane id, cockpit name, launcher pid, launch time) before it carries the work, and tells the seat to establish its identity from the process table, never from which conversation looks like its own. State that a suffixed seat name is not the bare project name. Never write "you (seat N)" in mail that lands in a shared inbox. `2026-09-21_a-partition-table-must-identify-seats-by-what-they-can-measure.md`

14. **When a ruling names the places to fix:** say the list is closed: "these and no others; if you find the same shape elsewhere, list it with the lines and STOP on it". In a seat's report, every "also", "in addition" or "while I was there" is a change nobody ruled on: name each in the check's brief as an item to attack first. When a fix moves an operation earlier (store before apply, write before check), ask what the later step was protecting, and have the seat state that reason for each path before reordering. `2026-11-18_a-fix-extended-beyond-the-named-paths-is-a-stop-question.md`

15. **Secuura work. When handing anything to Peter or Stuart (a review request, text for Kam to send, a ticket comment, a "waiting on the team" line):** group it first into test blocks: the stream parent, the pull requests in the block, the one test pass that proves it, and the one thing the human has to do, each block as large as one pass can prove. Never a flat list of pull requests; one that fits no block is stated as the exception with its reason. The receiving agent builds the blocks; the coordinator ratifies them and writes Kam's short text; Kam sends, nobody else messages them. Test: it must read as "run this, and these are done", not "here are N things". `2026-09-05_handovers-to-peter-and-stuart-are-test-blocks.md`

## What a tool already enforces

- `2_Project_Files/fleet/send_brief.sh` refuses a brief whose body lacks a PROVENANCE block, or any line lacking a source or read date. It does not know whether the source was really opened (it turns an omission into a deliberate false line), and it does not cover instructions to humans.
- `send_brief.sh` (with the decision queue's delivered mark and undelivered view) refuses a brief to a project that has ruled-but-undelivered cards when the body lacks the "RULED BY KAM" section. Not covered, named as candidates only: the coordinator's-own-rulings section, the scope clause on queued tickets, the SUPERSEDES check, and the artefact-and-date requirement on holds.

## The mistakes this family keeps catching

- A fact taken from a convenient summary (often my own ticket title) instead of the record of the event.
- A pointer to something stale, under repair, runtime-only or already wiped, offered as ground truth.
- A ruling relayed by mail to a seat that then rotated, found "unanswered" by the next reader and asked again.
- A hold or "not done" asserted from a queue mark without opening the artefact.
- A brief faithfully built and checked against itself while the half it left out (layout, sibling paths, the rest of the ticket) ships wrong.
- A flat list handed to a reviewer who needed one pass to run.

## Members

- `2026-08-04_validate-brief-pointers.md` — In a brief, for every 'verify X from Y': open Y and confirm it answers X today; a file the agent must repair is never ground truth. Queued tickets carry scope sentence and seat authority; a mail changing an earlier one names it and says SUPERSEDES.
- `2026-08-06_brief-provenance-enforcement.md` — When sending a brief: use send_brief.sh with a PROVENANCE block (fact | source | read date) from the authoritative record, not a summary or my ticket title. Before asking Kam to run anything, verify its preconditions read-only or say what I could not check.
- `2026-09-03_a-ratified-design-has-two-halves.md` — When Kam ratifies a mock and I write the build brief: measure the mock's layout (grid, chrome, tiles, chips) into numbered checkable properties, cite the mock by ref, and check delivery against the ratified artefact, not only the brief.
- `2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact.md` — When writing a successor brief or sweep: list Kam's ruled cards and my binding scope rulings, each with the artefact it must land in. A card mark records what a seat wrote, not the world. An UNKNOWN names why and what closes it. Put a RELEASE in the handover.
- `2026-09-05_handovers-to-peter-and-stuart-are-test-blocks.md` — When handing work to Peter or Stuart (review request, text for Kam, ticket comment): group into TEST BLOCKS (stream parent, PRs, the one pass that proves it, what the human does), never a flat PR list; a PR fitting no block is stated as the exception.
- `2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id.md` — When a handover or brief names a mechanism: give the file PATH that launches or runs it, never a pane id, pid, port or 'the wrapper'. Tooling must live in a tracked path (check git check-ignore); never invent a launch command when the real one cannot be found.
- `2026-09-20_prepared-in-a-scratchpad-is-lost.md` — When a handover or wrap says prepared, staged, ready or queued: name the durable in-project path or do not use the word. Scratchpad or unpushed worktree work is lost: say it is re-derivable, not prepared.
- `2026-09-21_a-partition-table-must-identify-seats-by-what-they-can-measure.md` — When I partition work across seats sharing an inbox: rows carry self-measurable identity (pane id, cockpit name, pid) before the work, tell seats to establish identity from the process table, and never write 'you (S74)' in shared mail.
- `2026-11-18_a-fix-extended-beyond-the-named-paths-is-a-stop-question.md` — When a ruling names places to fix: say the list is closed, and have the seat list-and-STOP on siblings. Read every "also did X" in a report as an unruled change to attack first; when a fix reorders an operation, ask what the later step protected.
