# ATTIO hands-on UX test — full report (Kam's 2026-08-22 19:55 commission)

**Tester:** Wednesday, at her own browser seat on Kam's signed-in Chrome
(fingerprint verified: 28 cores match this Mac Studio; workspace = `datasec`
confirmed from the URL and page on every sitting).
**Sittings:** Part 1 by the predecessor session (~20:00, board/kanban + NFR +
settings), Part 2 this session (~20:10–20:35: salesperson deep-dive, manager
pass, template audit).
**Writes made:** ONE test note on the synthetic [SYN] Ashgrove deal, created
and permanently deleted in the same sitting (restore verified by read-back:
Notes 3 → 2). Nothing else touched. Companies-by-Country untouched (HOLD).
NFR drag not re-attempted (proven human-drag-only yesterday, four ways).

## BLUF

The system is genuinely usable and the data discipline shows — but **three
things would bite a real salesperson on day one**: (1) the daily-job tasks are
**unassigned**, so the Home screen says "Tasks 0" while follow-ups sit in the
global list; (2) the daily job **doesn't dedupe** — the same Ashgrove follow-up
now exists twice (yesterday's manual run + today's first scheduled fire); and
(3) **email is fully walled off** until a mailbox is configured (M365 consent,
ATTIO-8) — Compose opens to a "no mailboxes configured" dead end, so the 13
templates, though all verified clean, cannot be used at all yet. The manager
pass is healthy: all three reports render and their numbers reproduce.

## Salesperson pass — findings

1. 🔴 **Follow-up tasks are invisible where a salesperson looks.** The bridge
   writes tasks with **no assignee**; Attio's Home shows only *your* tasks, so
   Home reads "Tasks 0" while the follow-up sits in the global Tasks list.
   Fix: the daily job assigns the task to the deal owner (owner is populated —
   Kamil on every deal).
2. 🔴 **Duplicate follow-up tasks.** Two identical "[Follow-up 2026-08-21]
   [SYN] Ashgrove…" tasks (due today / due tomorrow), both linked to the same
   deal — the manual real-write run and the first scheduled fire each created
   one. The job needs an idempotency check: skip if an OPEN task for the same
   flag+deal exists. (Same ack-discipline class as the bridge's watermark —
   the task write is currently at-least-once with no dedupe.)
3. 🔴 **Email composing is a dead end until ATTIO-8.** Compose email → "You do
   not have any mailboxes configured." This gates: sending, template use,
   sequences, and the not-contacted signal. ATTIO-8 (M365 consent) is now the
   single biggest rollout unlock.
4. **The [SYN] rehearsal set has no people** — Compose from the Ashgrove deal
   offers "Associated people: 0 recipients"; the company's Team is 0 too. The
   [DEMO] showcase people (14, e.g. Grace Ihaka) ARE linked to companies — so
   this is specifically the **migration path producing deals without
   contacts**. Since [SYN] is the rehearsal for the real 153-lead migration,
   the real migration must create/link People or reps can't email anyone from
   a deal. → migration ruling set.
   **[CORRECTED 2026-08-23, agent-measured — this finding was a SAMPLE OF
   ONE. Live measurement: 14 of 18 deals ARE linked to People; exactly four
   are not (Blank Holdings, Ashgrove Partners, Larkspur Freight, Copperfield
   Council), and Ashgrove — the one deal the test opened — is one of the
   four. The migration's People path is BUILT and running (peopleFrom parses
   Vision contact fields, upserted by email); the four have no person because
   their synthetic leads carry no contact data. The requirement changes
   shape: not "build People creation" but "MEASURE contact coverage across
   the 153 real leads before migrating, and report it as a first-class
   number" — unparseable-contact leads are the deals that arrive unemailable.
   Original text kept above for churn-visibility; the same correction applies
   to line ~109's REQUIRED-step wording.]**
5. **Deal record quality reads well** (stage, owner, Vision lead id, "Open in
   Vision" link, backdated notes) but several curated attributes render as
   empty "Set X…" prompts (Deal value, Sales motion, Opportunity size, Budget,
   Timeline) — the 10/18 value-coverage gap is salesperson-visible on every
   record.
6. **Note flow is clean** — create/type/autosave/link happens in seconds.
   Two quirks: opening the composer **creates the note instantly** (an
   abandoned open leaves an "Untitled note" behind), and deletion is
   permanent with a confirm.
7. **Cosmetic but everywhere:** the API actor renders as **"Attio-atent"** —
   misspelled workspace-member name on every activity row. Rename to
   "Attio Agent" (or "Vision Bridge") in workspace settings.

## Manager pass — the three reports (Sales Pack)

- **Deals per stage:** renders all stages in pipeline order incl. the new NFR
  (0). Bar values sum to **18** — matches the workspace total exactly.
- **Total deals in pipeline:** **18 records** — reproduces. ⚠️ One
  headline-vs-body issue: the title says "pipeline" but the count includes
  Won (2), Cancelled (1), On hold (3). A manager would read 18 as active
  pipeline; the active number is 12. Rename or filter (next ATTIO brief).
- **Deals older than 90 days:** **4 records** — matches the design doc's
  built figure (built on Vision dates; Attio created_at trap documented).
- Dashboard description is honest about synthetic data and its as-at date.

## Template audit (all 13, full bodies read)

- **Zero raw «BLOCKED» / «CONTENT» / «SENDER» / «SIGNATURE» markers** — every
  gap is a proper `[[ FILL: … ]]` with a pointer to where the rep finds the
  content. The one suspected template (Introduction & Pre-qualification,
  entered before the FILL rule) is clean. Scan validity: the same extraction
  shows 30+ `[[ FILL:` markers, so a raw « would have been visible.
- Variable chips render with full paths in the UI (`{ Company › Name }`,
  `{ Name › First }`) — Deal→Company traversal confirmed working.
- **Minor:** bodies carry a typed "Best regards, Kamil Kreiser" signature;
  when the mailbox syncs and supplies its own signature, sends may
  double-sign. Decide at ATTIO-8 time: strip from templates or send without
  a mailbox signature.

## Carried from Part 1 (predecessor's sitting, unchanged)

NFR stage confirmed at the end of the pipeline (human drag pending, Kam's
10 seconds) · status reorder is human-drag-only (four mechanisms tried) ·
kanban lazy-loads column headers away during fast scroll; empty columns are
bare slabs; card fields skeleton-load · `datasec@attio.email` forwarding
address shows "In Sync" — a BCC ingestion path needing NO M365 consent that
could partially un-blind not-contacted before ATTIO-8 (next session assesses)
· Objects 3/12 = at the Free cap · guessed settings URLs redirect to
/settings/account; navigate by search.

## Items for the next ATTIO session's brief

1. Daily job: assign follow-up tasks to the deal owner + idempotency
   (skip when an open task for the same flag+deal exists). Both are bridge
   code — ungated.
2. Rename the "Total deals in pipeline" report or filter to active stages
   (title currently overstates).
3. Rename the "Attio-atent" workspace member.
4. Migration plan: contacts/People creation + company-team linking is a
   REQUIRED migration step (evidence: [SYN] deals have zero addressable
   recipients).
5. datasec@attio.email BCC-ingestion assessment (carried).
6. At ATTIO-8 time: template signature strategy (avoid double signatures).

## For Kam (no rush, queued)

- The 10-second NFR drag (unchanged).
- Companies-by-Country: HOLD stands — untouched this sitting.
- ATTIO-8 (M365 consent) is now the biggest single unlock: it opens email,
  templates, sequences-on-Pro, and the not-contacted signal.
