---
date: 2026-11-18
type: correction
source: "Consolidation of the Tuesday seat's ledger rows 2026-11-12..11-18 at the kit stamp (14 of 28 rows), found by the s290 Fable audit of the rules card (0_Brain/reference/2026-11-18_rules-card-tuesday/REPORT.md, gap G1), on Kam's 11:28:59 instruction to adopt Friday's card and improve it"
status: live
tier: M
seats: tuesday
supersedes: ""
---

# The kit stamp is where this seat makes half its mistakes. Run the checklist; the stamp tools' OK is not the check.

**The lesson:** a STAMP freezes a kit that a seat will obey literally, so every sentence I stamp is a claim I make. In the 2026-11-12..11-18 window, 14 of this seat's 28 ledger rows were made at the stamp. Each time the drafter's text was trusted, or the stamp tool's OK was taken as proof. `stamp_check.py` measures that a literal is present, not what it means. `stamp_brief.py` checks that slots are filled, not their shape. Before every stamp, run the checklist below; each item is a past miss.

**Context:** the rules card had one stamp line, and its text existed in no lesson file. The stopping rules lived only in ledger rows, which are archived after about three days and then never fire. This file is where they live from now on.

**How to apply: the STAMP CHECKLIST (each item names its ledger row):**
1. **Read whole, really whole.** Read the kit with the Read tool (offset/limit pages), or print the tail of every line a display cut (`awk 'length>N'`). Never read it through `cut -c`. If a page was persisted to a file, read the file. *(s279 11-15)*
2. **Who decided.** Run `/usr/bin/grep -i -n 'product owner\|ruling\|ruled\|Kam\|decided\|agreed'` over the kit. For each hit, run `decision_queue.sh show <id>`: the card's `client_project` must equal the lane's project, and its option detail must name the lane's scope. A decision Tuesday made is written as "the ticket's proposed default, approved by Tuesday". A store write (amend/add) is read back with `show` before any note says it happened. *(B1675 11-17; B1695 11-18 w=2)*
3. **Sentences about behaviour.** Every frozen sentence that says what code, a test or a gate finding DOES gets its source lines printed beside it in the stamp action (one `sed -n` per sentence). Paraphrases of a finding are read against the finding's own row. *(B1552, B1553 w=2, 11-15)*
4. **Commands in the consuming tool's syntax.** jest/vitest `-t` is a JS regex (`a|b`), grep BRE is `a\|b`. Run the literal, or at least check it against the tool's syntax. *(B1687 11-18)*
5. **Predicted numbers are measured or removed.** A diff shape, count or "exactly once" is measured by applying the change to a scratch copy (`git diff --stat`) or counting by program, or the claim is reworded to the byte-equality check. A drafter's arithmetic is never a measured sidecar line. *(B1569 11-15; 11-12 count row)*
6. **Expected outputs come from a real run.** If a kit tells a seat to MATCH a tool's output, quote it from a real run. List each step's inputs against the step that makes them. If the kit changes an answer the code gives, carry a by-program census of the tests and generated fields that pin the OLD answer. *(11-12 w=3 REGRESSION; B1555 11-15)*
7. **Clocks are printed, never typed.** STAMP, BASE and READ-WHOLE clocks come from `date` in the same command that fills them, or from the source's own printed time. Never write an `xx:Nx` estimate. *(s281 11-16; s286 11-17; s288 11-18)*
8. **After the stamp, before the launch:** check `wc -c` (never 0) and `tail -n 1` against the kit's own Step-0 rule for its last line. A rewrite is built and ENCODED first, written to a temp file, then `os.replace`d. Never `open(path,'w')` on the live kit. *(s283 11-16; s286 11-17)*
9. **Lane still live?** Before commissioning or stamping a lane taken from a sweep, grep the pickup and today's note for the lane id and its keys, and read every DROPPED or HELD line. *(s278 11-15)*
10. **Queue, don't fire.** A stamped kit joins the queue. The next launch waiter starts only after the previous waiter's exit and its rung-5 read. *(s282 11-16)*

11. **What lies outside the frame.** For every kit whose property says "every", "all", "no value" or "none", write one line at the stamp naming three things the property's subject is handed that are NOT the tested shape (for a repository scan: commit and tag messages, names, refs; for a logging filter: a dictionary of another type, a list of pairs, a name that holds no listed stem), and check that the kit covers each or names it a limit. For a security surface (a filter, a deny-list, a scanner, a parser) the drafter's commission carries the same question as a required section from round 1. **The stamp's line NAMES what lies outside the frame and may tell the seat to stop and ask or to refuse closed; it never invents a new behaviour: a new rule for a parser or a state machine goes back to a drafter as a Question with a default, a state table and a model run.** *(B1774 11-20 s297; B1787 11-20, w=2: the rule sat in a ledger row and the next stamp of the same kind did not meet it; B1786 11-20 s301: a time rule Tuesday wrote into a stamp slot was built as written and was the review's Blocker)*

12. **A STOP-severity check nobody has run.** When a drafter's report says a kit's checks were not run, each STOP-severity check is run once on the drafter's own prototype output (PASS, control FIRED), or the Stamp marks it "never run on a real output: a failure traceable to the kit's own wording is a STOPPED: NEEDS TUESDAY question, not the seat's to amend". *(B1801 11-20 s301: a no-copy check failed on the commissioned output's own ids; the seat amended it and went on past the STOP)*

**At the merge, the stamp's sibling:** read the printed check table, not the ALL GREEN line. It must name every job the repo expects (`pr_checks_wait.sh --min-checks N`). *(s287 11-18)*

**Related:** [[2026-08-07_a-check-that-cannot-fail]], [[2026-08-14_i-read-representations-they-read-sources]], [[2026-09-07_read-the-clock-at-boot]], [[2026-11-18_lessons-are-weighted-by-reinforcement-never-absolute]], [[_ledger_laptop_datasec]]
