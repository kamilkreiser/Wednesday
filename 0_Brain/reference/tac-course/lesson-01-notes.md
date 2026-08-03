---
course: Tactical Agentic Coding (agenticengineer.com)
lesson: 01 — Hello Agentic Coding
runtime: 21:52
captured: 2026-08-03
transcript: transcripts/lesson-01-hello-agentic-coding.txt (verbatim, 881 cues)
codebase: /Volumes/DevMASTER/!CODING/Agentic Coding/Resources and Lesson Material/tac-1
---

# Lesson 01 — Hello Agentic Coding

## Summary

Framing lesson: no new mechanics, sets the course's thesis. The instructor
splits the generative-AI era into **phase one = AI coding** (prompt → code;
"the big three": context, model, prompt) and **phase two = agentic coding**
(prompts that reliably execute long chains of *tools*). Adding tools to the big
three gives **the core four: context, model, prompt, tools**.

The stated mission: become an "irreplaceable engineer" by moving up the stack —
not writing code, but *building systems that build systems*. The course is 8
lessons, each delivering exactly one **tactic**.

**Tactic 1: "Stop coding."** Deliberately provocative. The claim: your hands and
mind are no longer the best tool for *writing* code; engineering cycles should
be reallocated to **planning, reviewing, and creating closed-loop structures**.
Code understanding stays critical; hand-typing does not. (He is explicit that
this is uncomfortable and that he'll be "sharp" about it.)

**The demo** (codebase `tac-1`, ~35 lines of README): run an *AI coding prompt*
(`CREATE main_aic.py: print goodbye ai coding`) — one file appears. Then an
*agentic coding prompt* — checkout a branch, create a file, run both files, git
add, git commit, report. Same tool, categorically different work: the second is
**engineering work**, not code generation.

**Second demo — the one that actually matters: Claude Code is *programmable*.**
`programmable/` holds three scripts (shell, Bun/TypeScript, Python-uv) that each
do the same thing: read `prompt.md` and shell out to `claude -p "<prompt>"`,
capturing stdout. Because Claude Code is a terminal binary, any language can
invoke it — so agentic prompts can be **embedded anywhere in the software
development lifecycle**, running "with and without your oversight." That is the
foundation the remaining seven lessons build on (he name-drops "agentic
triggers" and "long-running end-to-end AI developer workflows" as what's coming).

## Key learnings (what's actually here)

1. **The core four (context, model, prompt, tools)** — a clean vocabulary for
   why tool-calling changed the category, not just the speed.
2. **Agentic prompt = a prompt containing a sequence of tool calls**, judged by
   the *scale and reliability* of the chain, not by novelty of tool-calling.
3. **Programmability is the real unlock** — `claude -p` from any script means
   agentic work can be triggered by code, CI, hooks, schedulers; the human is
   optional at run time.
4. **Reallocate human cycles to planning / reviewing / closed loops** — the most
   useful line in the lesson, and the one that matches our own doctrine.
5. **Tools change, tactics transfer** — his own caveat: don't get stuck on one
   tool.

## Verdict against Kam's filter ("use what's good, not what takes us backwards")

**GOOD — adopt or already ours:**
- *Programmable agentic prompts* (`claude -p` from scripts). We already do this:
  Wednesday's coordination harness invokes `claude -p` and `codex exec` as
  scored seats. Validated, not new to us — but the lesson's framing of
  *embedding across the SDLC* (triggers, hooks, CI) is a genuine expansion we
  have not yet exploited.
- *Human cycles → planning, reviewing, closed loops.* This is exactly our
  delegation protocol (verifier first, review gates, escalate at 3 rounds).
- *One tactic per lesson, compressed.* Good pedagogy; worth copying in how I
  write briefs and skills.

**CAUTION — where it would take us BACKWARDS if adopted literally:**
- **"Stop coding" as an absolute.** Fine as a provocation about *typing*
  boilerplate; dangerous as doctrine. Our hard rules (verify before claiming
  done, no-skip-on-failure) require reading and understanding code closely, and
  the Secuura/CypherKey work is exactly the kind where hand-verification of a
  diff catches what an agent's confidence hides. Adopt as "don't hand-type what
  an agent can generate"; reject as "don't engage with code."
- **"Millions and millions of tokens… pay to play."** Volume is not a strategy.
  Our day-3 experiments showed one strong pass + a grounded verifier beat
  search/repetition on well-specified work. Spend where verification says it pays.
- **Running "without your oversight" this early.** Directly against Kam's
  go-slow directive (2026-08-03). Autonomy is the destination; supervised
  pilots are the path. Keep the oversight until the ledger earns its removal.
- **Marketing frame ("irreplaceable engineer", "10x leverage", "loot box").**
  Motivational packaging; no operational content. Ignore.

**NEW to us, worth watching in later lessons:** agentic *triggers* (what fires a
workflow), and the closed-loop/self-validating structures he previews — that is
the part most likely to upgrade our delegation protocol. Lessons 6–8 codebases
(`adws/` directory in tac-6, multi-agent apps in tac-8-2) suggest the substance
lands there.

## How to deploy (concrete, for us)

1. **Nothing to change today from lesson 1** — its one mechanic (programmable
   `claude -p`) is already in production in `2_Project_Files/coordination/`.
2. **Watch item:** when lessons 5–8 introduce triggers/closed loops, evaluate
   against our delegation protocol R1–R8 rather than adopting wholesale.
3. **Reusable idea now:** the *AI-coding-prompt vs agentic-prompt* contrast is a
   good teaching device for briefs — state the tool chain expected, not just the
   outcome.
