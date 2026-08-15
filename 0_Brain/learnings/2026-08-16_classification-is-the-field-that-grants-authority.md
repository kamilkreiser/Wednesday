---
date: 2026-08-16
type: correction
source: "Caught by the Datasec/NexusAI agent within 15 minutes of my brief. I wrote 'RD-93 — duplicate transition id 51 on the RD board, landing on Declined. Board config, reversible.' Neither half is true: transition 51 lives in a workflow shared by 25 workflow schemes across a 35-project company Jira. I verified the 25 myself afterwards — the agent was exact."
status: live
supersedes: ""
---

# A scope/reversibility CLASSIFICATION is a fact needing provenance — and it is the one that decides my own authority

**The operative case, so the headline matches it:** I am about to write words like
**reversible · local · board config · demo-only · contained · inside scope · low-risk** into a
brief, a score, a ticket or a report. **Stop.** That is not a description of the work. **It is
the field that decides whether the work is inside my delegated authority** — and I have never
once checked one the way I check a count.

## What happened

My brief queued RD-93 as: *"duplicate transition id 51 on the RD board, landing on Declined.
**Board config, reversible.**"*

**The predecessor's wrap never said those last three words.** It said *"duplicate transition
id 51 on the RD board, lands on Declined. Both real, both inert."* **The classification was
mine, appended on top of a sourced fact** — and my `PROVENANCE:` line cited the wrap mail, so
the whole sentence travelled looking sourced.

**The reality, measured by the agent and then independently by me:** RD (project 10320) runs
on workflow scheme 10035 — *named* `CUP: Software Simplified Workflow Scheme`, which is
itself part of why it reads as local — whose default workflow
`Copy 3 of Software Simplified Workflow for Project HPONE` is **shared by 25 of the site's 57
schemes** (HPAM, KEYC, PE, TEA, MMP, WDM, CVL, LDR, HDU, AS, CAP and more). **Editing
transition 51 changes other teams' boards.** Not local. Not reversible in the sense v1.3 uses.

## Why this is a distinct lesson and not another provenance row

🔴 **`send_brief.sh` cannot catch this class, and that is the finding.** The gate refuses a
brief whose **facts** lack a source. **A characterisation appended to a properly-sourced fact
rides through free.** The fact was real, the citation was real, the read-date was real — and
the word that mattered had no source at all.

**And the word that mattered is the one that grants permission.** *Reversible* is the exact
term separating what I may authorise under v1.3 from what needs Kam's signature. So the error
is not that I misinformed an agent. **I manufactured my own permission to delegate it** — the
same shape as a prompt line that supplies a missing approval
([[2026-08-06_ghost-suggestions-in-panes]] escalation), except that I generated it myself, in
good faith, inside the mechanism built to prevent exactly this.

**The asymmetry that makes it invisible:** a wrong count gets checked because counts look like
claims. **A classification looks like framing** — like the helpful context an experienced
coordinator adds. It reads as service, not as assertion.

## How to apply

1. **Treat every scope word as a measurement, and give it its own PROVENANCE line.**
   `reversible | <the command or file that establishes the blast radius> | read YYYY-MM-DD`.
   If I cannot write that line, the honest brief says *"I have not established the blast
   radius — establish it before acting."*
2. **The question is always "what else does this touch, and how did I find out?"** For a
   config object: what else references it. For a workflow, scheme, template, shared library,
   CI file or DNS record: **enumerate the consumers before calling anything local.** A thing's
   NAME is not its scope — RD's scheme is named after another project entirely.
3. **Never let a classification inherit a neighbouring fact's citation.** If the source did
   not say "reversible", I do not get to say it under the source's name.
4. **Suspect myself hardest when the classification is convenient.** "Reversible" was the word
   that let me hand the item to an agent rather than to Kam's queue. **That is what makes it
   the same family as accepting a result that already agrees with the story**
   ([[2026-08-14_i-read-representations-they-read-sources]]): *did I want this to be true, or
   did it save me work?*
5. **Reversibility is a property of the effect, not of the action.** A one-line edit is not
   reversible because it is one line; it is reversible if undoing it restores the world for
   everyone it reached.

**The honest note on credit:** not self-caught. The agent said plainly *"where your brief does
not survive contact"* and gave the measurement, having been told in that same brief that this
was the most valuable thing it could send me. **That instruction paid for itself inside
fifteen minutes**, which is the argument for keeping it in every brief.

**Related:** [[2026-08-06_brief-provenance-enforcement]] (the gate this slips past),
[[2026-08-14_i-read-representations-they-read-sources]],
[[2026-08-15_a-cap-is-never-neutral]] (its sibling: I quoted a number without its predicate
the same morning — both are unstated qualifiers riding inside a sourced sentence),
[[2026-08-07_protocol-v1.3-signed-delegation]] (the authority this misclassification would
have widened), [[2026-08-16_a-recorded-blocker-is-not-a-boundary]], [[_ledger]]
