# BRIEF — Secuura/Blockchain, seat s153: the standing queue, unattended since 10:56

## BLUF
**Your board has had no agent on it since 10:56** — over two hours at the time of writing. Work the category-1
standing queue — every ticket that needs nobody outside Kam, Wednesday and you — under the
COO rule and the overnight grant, until it is empty or you wrap for context. **Start at
KS-989 (P1, In Review).** Nothing here asks for a decision from Kam.

## Recommendation
Take the queue in this order and wrap when your context reaches its band:
1. **KS-989 (P1, In Review)** — s149 named it the next highest-value item. *"Wire
   `format:check`, never `quality`"* travels with it.
2. **KS-971 (P0, In Review)** — the only P0 among the 43 In Review. **Wednesday did NOT
   measure priorities across the other 265 open tickets**, so this is not a claim that it is
   the only P0 on the board; if you need that, it is one query.
3. **The other two P1s in In Review** — KS-946 and KS-858 in the listing Wednesday saw, but
   that listing was the truncated 250-row page, so **confirm the P1 set against the board**
   before you sequence on it. Then P2 by identifier.
4. Anything in **In Progress (34)** that is yours and stalled — finish or bounce it back to
   Wednesday with the reason. A stalled ticket nobody names is the failure mode.

PROVENANCE:
- 308 open KS issues; Backlog 190 / In Review 43 / Todo 38 / In Progress 34 / Blocked 3 | Linear GraphQL team KS, states nin completed+canceled, PAGED to exhaustion (4x100, last page short) — run by Wednesday | read 2026-09-08
- assignees kamil.kreiser 247 / UNASSIGNED 32 / peter 23 / stuart.jamieson 6 | same paged query | read 2026-09-08
- origin/develop 986c592d5, demo 400517aaf, #903 #904 #905 #793 open+unmerged, #896/#899/#900 unapproved, KS-968 In Progress, schema trap at c38040bd1 not on develop | s149 handover 2026-09-08 10:56 — RELAYED, Wednesday holds no Secuura identity; re-read before acting | read 2026-09-08
- KS-989 is the next highest-value item and carries "wire format:check, never quality" | s149 handover 2026-09-08 10:56 — RELAYED | read 2026-09-08
- Kam 07:10 "deploy and merge everything that has been tested and done and is ready for deployment" | /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_kam.json + /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh - Wednesday's tree, not yours | read 2026-09-08
- PS-Done 18 held; the count in the ruled card was 15 and the real number is 18 | decision_queue card secuura-platform-s-count-was-wrong-when-you-ruled, open, default HOLD | read 2026-09-08
- assignment rule: new/unassigned to our account, tickets already on Peter or Stuart stay theirs | Kam panel 2026-09-06 10:24, verbatim on the ruled card | read 2026-09-08
- ticket creation aggregates into one larger ticket per logical path | Kam panel 2026-09-06 09:42 | read 2026-09-08
- week-scoped merge + deploy authority sits with Wednesday through Sunday 2026-09-13 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-07_merge-authority-was-already-mine.md + .../2026-09-07_deploy-grant-and-fix-the-visible-data.md - Wednesday's tree, not yours | read 2026-09-08
- users.email is AES-GCM ciphertext; resolve via email_lookup_hash, decisive on a MATCH only | s149 handover 2026-09-08 10:56 + /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md project-trap section - Wednesday's tree, not yours | read 2026-09-08

## WHAT IS MEASURED AND WHAT IS RELAYED — the same facts, in prose
- **BOARD CENSUS: measured by Wednesday today, 2026-09-08 13:1x.** Linear GraphQL, team KS,
  states not completed/canceled, **PAGED to exhaustion** (4 pages of 100, last page short):
  **308 open** — Backlog 190 · In Review 43 · Todo 38 · In Progress 34 · Blocked 3.
  Assignees: kamil.kreiser 247 · UNASSIGNED 32 · peter 23 · stuart.jamieson 6.
  *A first single-shot query returned 250 with `hasNextPage: true`; that number is a CAP and
  is not quoted anywhere. The figures above come from the paged run.*
- **REPO STATE: RELAYED from s149's handover of 2026-09-08 10:56, NOT re-derived by
  Wednesday** — Wednesday holds no Secuura identity, so every topology claim here is
  second-hand and you re-read it before acting on it:
  `origin/develop 986c592d5` · `demo 400517aaf` · unarchived 370 ·
  `#903 #904 #905 #793` open and unmerged · `#896/#899/#900` UNAPPROVED deliberately ·
  KS-968 In Progress · **the schema trap is at `c38040bd1`, NOT on develop.**
- **Kam's 07:10 instruction today, verbatim:** *"I'm going to drop off the kit if we please
  deploy and merge everything that has been tested and done and is ready for deployment."*
  **Wednesday is NOT converting that into a deploy instruction for you** — see HOLDS.

## 🔴 PROJECT TRAP — third occurrence across two seats, so it leads
**Any probe of `users.email` by literal comparison is VOID BY CONSTRUCTION** — the column is
AES-GCM ciphertext. Resolve via `email_lookup_hash`; a hash comparison is decisive **on a
MATCH only**. If a finding rests on an email equality check, the finding is unproven.

## HOLDS — unchanged, and two of them are Kam's own
1. **Platform S: the FIFTEEN Kam ruled on are archivable; the DELTA is HELD.** He ruled
   `archive` at 10:35 on a set stated as fifteen. **The real number is 18 — and the wrong
   figure came from us**, so the correction sits on his desk as
   `secuura-platform-s-count-was-wrong-when-you-ruled`, default HOLD.
   **Archive nothing further in that class**: the three beyond his fifteen wait for his word.
   *(An earlier draft of this brief said "archive none of them", which contradicted his own
   ruling — caught by the ruling gate, not by Wednesday, and corrected here.)*
2. **Tested-Not-Deployed: HELD** on Kam's earlier `hold`. His 07:10 sentence above reads like
   it lifts this, and Wednesday is deliberately NOT reading it that way — a deploy
   instruction inferred from a sentence about dropping off a kit is not an instruction.
   **If your queue reaches something that needs it, stop and ask Wednesday.**
3. **Signature classes unchanged:** production, money, **external communication to any
   human**, irreversible actions. Wednesday holds week-scoped merge and deploy authority
   (through Sunday 2026-09-13) — so a merge is Wednesday's GO to give, not yours to take,
   and **a merge that itself makes a commitment to Stuart or Peter is Kam's alone.**
4. **Client-facing communication goes ON THE TICKET.** The extranet is INPUT ONLY. Nobody
   messages Peter or Stuart except Kam; anything urgent comes to Wednesday as an escalation
   candidate with the text ready.
5. **Handovers to Peter or Stuart are TEST BLOCKS**, never a list of PRs: the stream parent,
   the PRs inside it, the ONE pass that proves it, and the single thing the human must do.
6. **Ticket CREATION aggregates** (Kam, 2026-09-06 09:42): one larger ticket per logical
   path with its items as sub-issues or a checklist — never three or five for one line of
   work. *"Within a logical path"* is the limit.
7. **Assignment** (Kam, 2026-09-06 10:24, correcting himself): new and UNASSIGNED tickets go
   to our account. **A ticket already on Peter or Stuart stays theirs** — moved only on Kam's
   word, per ticket, never by a predicate.

RULED BY KAM, NOT YET IN AN ARTEFACT
====================================
Every one of these is Kam's word from 2026-09-08. They live on his panel and in mail to a
seat that has since wrapped — which is nowhere you would land. **Put each into the artefact
named beside it and say so in your receipt**, or the next seat asks him again.

- `secuura-ci-dead-19-days-blocks-your-own-ruling`: *"fix — Kam fixes the billing / spending
  limit himself — the only unblock, and it releases KS-961 plus every future PR gate"*
  -> must land in: a comment on **KS-961** naming Kam as the owner of the unblock, so nobody
  re-diagnoses dead CI as a code problem.
- `secuura-892-round4-passed-but-introduced-two-majors`: *"round5 — ONE more narrow round —
  F-1 and F-2 only, F-2 first"*
  -> must land in: the **#892 PR thread** (round-5 scope, F-2 first), and the round count
  stated in the fix-round mail under the two-NO-GO cap.
- `secuura-ks968-rotation-three-worlds`: *"separate — Authorise the one two-boolean statement
  — it settles which of the three worlds this is"*
  -> must land in: a comment on **KS-968** carrying the statement and its result.
- `secuura-ks968-my-decision-table-was-void`: *"hashcmp — Authorise ONE read-only comparison"*
  -> must land in: the same **KS-968** comment. **READ-ONLY, one comparison, and remember the
  project trap: a hash comparison is decisive on a MATCH only.**
- `secuura-793-security-expiry-two-triages-disagree`: *"earlier — Take the EARLIER expiry
  (2026-09-10) for the three, plus develop's corrected q8mj row and #793's 4 new advisories"*
  -> must land in: the **#793** audit-baseline rows themselves.
- `secuura-793-the-four-rows-you-authorised-are-already-expired`: *"add-dead — Add the four
  as-is, expired, and file ONE ticket to re-triage them"* — **one ticket, not four**
  (his aggregation rule).
  -> must land in: the **#793** baseline + **one** new re-triage ticket.
- `secuura-archive-fifteen-platform-s-tickets`: *"archive — Archive them too — read the 10"*
  -> must land in: the archived state of that fifteen. **s149 relayed this at 10:36 and its
  claims row says 33 archived + 2 cascade-restored — RELAYED, not verified by Wednesday.
  Check the board before re-doing it; and see HOLD 1 for the three beyond his fifteen.**

## THE GATE — every change, before any score or ship
agent → Wednesday → **testing agent** → Wednesday. You hand over a READY/wrap mail stating
sets not counts, the branch and SHA, the surfaces changed, how it authenticates, and what
you did NOT do. **A READY is a QA trigger, not a score trigger.** The pass is TIERED by what
the change touches (full weight for security surfaces, data destruction, deploys and human
handovers; through-code only for tests, docs, config and already-gated follow-ups) and
CAPPED at two NO GO rounds on one class.

## WHAT WEDNESDAY OWES YOU
- Wednesday is the wake path: mail `wednesday-agent@agentmail.to` with
  `[Secuura/Blockchain -> Wednesday] QUESTION: <topic>` and keep working on the next item
  rather than blocking, unless the question is approval-class.
- **Say what you expect will WAKE you** if you ever have to wait on something outside your
  session. *"I will check back"* is not a mechanism; a job that exits, a scheduled tick, or
  a tap from Wednesday is.
- Record analysis in three fields: **FOUND** (the claim), **TESTED** (what was and was not
  exercised), **HOW** (the instrument, the command, the controls — including the negative
  one, so a zero is a zero somebody can vouch for).

## HOUSEKEEPING YOU SHOULD KNOW
- The fleet chat is now one writer per file; nothing you do touches it.
- Kam has a second agent, **TUESDAY**, on all Datasec projects. She is not on this board and
  never will be. If a Datasec name appears in your work, that is a finding, not a detail.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 13:18
Found and fixed FOUR, all mine. Three on the first pass: an absolute ("the only P0 on the
board") resting on a measurement taken only WITHIN In Review; two P1 ids asserted from the
truncated 250-row page, now marked as needing confirmation; and a duration rounded up past
its own stated fact. The fourth was caught by the ruling gate rather than by me, and it was
the worst: HOLD 1 said "archive none of them" while the rulings section carries Kam's own
`archive` on fifteen of exactly those tickets. The hold now says what is actually true —
his fifteen stand, the three beyond them wait for him.
