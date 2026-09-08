# BRIEF SKELETON — copy this file as the starting point of every brief

**WHY THIS EXISTS (ledger w=4, 2026-09-09 — a REGRESSION with no mechanism until now).**
`send_brief.sh` matches three literals with `grep '^…'` — **at line start, exact text**.
Four briefs have been refused because a markdown heading prefix was put in front of one
of them (`## 5. PROVENANCE` on 2026-09-07, cost four rounds; `## RULED BY KAM…` twice on
2026-09-08; `## 5. RULED BY KAM…` on 2026-09-09). Every instance was gate-caught and free,
and every instance recurred anyway.

**The diagnosis the fourth instance earned, and it is why more care was never going to
work:** the rule is about a LITERAL STRING and the failure is a FORMATTING REFLEX. A writer
numbering `## 1.`, `## 2.`, `## 3.` across a document will number the gated section too —
the hand is being *consistent*, which is the opposite of careless. A rule held in prose
cannot beat that. A file you copy can.

**How to use it:** copy this file to the scratchpad, fill it in, delete what does not apply.
Never retype the three literal lines below — they are the strings the gate greps, and they
were read out of `send_brief.sh` (lines 142, 359, 425) in the action that wrote this file,
not composed from memory.

**Do NOT put a `#`, a `##`, a number, a bullet or any leading whitespace in front of the
three literal lines.** A heading ABOVE them is fine and is how this skeleton does it.

---

## BLUF

<What is true now, what changed, what it means. A reader who stops here must be correctly
informed and not misled. Name the actors — Kam, Wednesday, the seat, Peter, Stuart — never
"you"/"I"/"we" outside a mail addressed to one agent.>

<Seat number, if this is a successor brief: DERIVE it from THAT PROJECT'S OWN
`5_Project_History/history.md`, never from Wednesday's counter and never from a scratch
filename. State the derivation.>

## 1. ITEM 0 — <ticket id> (<priority>, <state>, <assignee or UNASSIGNED>)

<The commission. Quote the ticket's own SCOPE sentence verbatim: a brief narrower than its
ticket produces a ticket that closes on a fraction. If this brief commissions LESS than the
ticket, say so as narrowing and say what tracks the rest.>

<What "done" means for this round, and where the round ENDS (READY FOR QA / merged / filed).>

## 2. THE QUEUE AFTER ITEM 0

<Give the RULE and the REASON; stop reaching for the ANSWER. Handing a seat an answer
removes exception-handling from the only party that can see the exceptions. Every hint
carries its bound: a title-only read says so.>

<Name what is NOT actionable and why, so it is not silently re-proposed.>

## 3. HOLDS

<Signature classes (production, money, external comms, irreversible). Never delete —
quarantine. Client-facing comms are ticket comments only. Any project-specific standing
lines. Any Wednesday ruling still operative — see the section below.>

## 4. IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO

<Keep this line in every brief. It is the highest-value sentence in the template: four
refusals in ninety minutes on 2026-09-07, three confirmed correct. A brief item that is
wrong is Wednesday's error and will be named as Wednesday's.>

<Name the WAKE: any instruction whose execution outlasts a turn says what will prompt the
seat when it ends — a foreground wait, a background job that EXITS so the harness
re-invokes, or an explicit "I will tap you". "Monitor it" is not a wake.>

## 5. Rulings that carry no delivery mark

<!-- The line below is a GATE LITERAL. It is required whenever
     `decision_queue.sh list ruled --undelivered <prefix>` is non-empty for this project.
     An EMPTY section under it is valid; an ABSENT heading is not.
     Each card: `- <card-id>: "<ruling verbatim>" -> must land in <ticket/PR/row>`
     A card's mark records what a SEAT WROTE DOWN — never a fact about the world. Do not
     assert a card as still-undone OR as still-binding without opening its artefact;
     UNKNOWN is the honest word, and the over-cautious direction is the one that hides. -->
RULED BY KAM, NOT YET IN AN ARTEFACT
- <card-id>: "<ruling verbatim>" -> must land in <artefact>

## 6. Rulings Wednesday gave this project that still bind

<!-- NOT a gate literal — this is a RULE (lesson 2026-09-05, EXTENSION 2026-09-06 02:2x,
     ledger w=4) and its enforcement is still only a CANDIDATE. Built from the staged
     ANSWERs to this project since the previous brief, READ, never from memory. An empty
     section is valid; an absent one means a scope ruling given to seat N lives in a mail
     that seat N+1 never reads. -->
RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- "<ruling verbatim>" (<mail timestamp>)

<!-- ── THE REMAINING TWO GATE LITERALS. Nothing may precede them on their line. ──
     PROVENANCE  (send_brief.sh:142) — every fact carries: <fact> | <source> | read YYYY-MM-DD
       · a RELATIVE path is refused unless the line says whose tree it is in
       · a SCOPE WORD is refused unless a provenance line establishes it. The list
         is NOT reproduced here on purpose: this file was refused by that very gate
         on its first run, because spelling the words out made the template trip the
         guard it documents. Read them from the gate itself — `send_brief.sh:59`,
         the `SCOPE_HIT` regex — which also cannot go stale. Such a word decides
         whether the work is inside Wednesday's delegated authority, so it is a
         measurement, not framing.
       · name the INSTRUMENT inline for every count, SHA, base, head or line number;
         a truncated query states its bound
     SELF-CHECK  (send_brief.sh:359) — the phrase and the stamp with NOTHING between them,
       detail on the following indented lines. RUN `self_check_view.sh <body-file>`;
       do not tick the box. Re-run it after ANY amendment: an attestation carried past
       an edit is a check that was never run. -->
PROVENANCE:
<fact> | <the command or file that establishes it, and whose tree it is in> | read YYYY-MM-DD
SELF-CHECK: re-read end-to-end for contradictions | YYYY-MM-DD HH:MM
    <what the self-check surfaced, or "no contradictions">
