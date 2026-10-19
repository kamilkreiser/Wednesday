## BLUF

You are **Seat E 3rd** on Secuura Platform K (lane Secuura/Blockchain-E). Two jobs from Stuart's list (Kam forwarded it 2026-10-19 15:50 AEDT: "action what you can"): **(1) deliver two of Kam's rulings that never reached their tickets, and build the one that is unbuilt (KS-1195's key limit); (2) a short set of ticket replies Stuart is owed.** Ticket comments are the only client channel. Send a plan confirmation before your first write.

## QUEUE

1. **Deliver Kam's 9 Oct rulings, verbatim, as BLUF comments:**
   - **KS-1195** (In Progress, 9 comments, last 2026-10-18T11:42Z): card `secuura-ks1195-s-key-ceiling-1009`, ruled **(a)** on 2026-10-09 10:06:06 AEDT, option text verbatim: *"Raise the default for S connector keys to 3,000 per hour, tunable by env; new keys only"*, detail *"a Sonnet seat builds it, QA-gated; existing keys keep 1,000 until rotated"*. Say the build is in progress (item 2), no date. Say existing keys keep 1,000 until rotated, and that rotating live client keys is Kam's.
   - **KS-1384** (Backlog, 3 comments, last 2026-10-18T22:42Z): card `secuura-ks1384-anchor-per-event-1009`, ruled **(a)** "One anchor per lifecycle event" on 2026-10-09 10:06:00 AEDT. Say the shape is ruled and WHEN it starts is with Kam (a card is on his panel today), no date.
   - Mail me each comment's id; Wednesday marks the cards delivered.
2. **Build KS-1195's ruling:** register-connector passes a per-key `rateLimit` from an env value, default 3,000 per hour, for NEW Platform S connector keys only; existing keys unchanged. The triage measured (not re-measured by Wednesday): api-gateway `routes/platform.ts` has 0 `rateLimit` at develop 7e2f8157cec2, and the security service's default is `.default(1000)` at `services/security/src/index.ts:666`. Red-first cell, a control that an existing key is unchanged, own PR `Refs KS-1195`, READY FOR GATE (tier 1).
3. **Replies owed (one BLUF comment each, nothing promised, no dates):**
   - **KS-1385** (In Progress, 10 comments, last 2026-10-19T05:03Z) and **KS-1612** (In Progress, 6 comments, last 2026-10-19T02:49Z): both landed on develop today (#1568 as 04a4a33938f0, #1607 as 7e2f8157cec2); not deployed; the deploy waits on the conditions listed in the triage row 6 (Stuart's own dev-ps deploy, the 050/051 censuses, the KS-1402 develop 500 now being fixed by Seat C 25th). Read the existing K comments first; do not repeat what J 13th already posted.
   - **KS-1604** (Backlog, 1 comment, last 2026-10-14T00:42Z): Wednesday's ruling on the fix shape: bind at the ORGANISATION level, as Stuart proposed (the only shape that does not blank the existing S identities). Unscheduled, no date.
   - **KS-1575** (Backlog, 1 comment, last 2026-10-13T00:24Z) and **KS-1596** (Backlog, 0 comments): holding replies: "received, with Kam, not scheduled".
   - **KS-1387** (In Progress, 6 comments, last 2026-10-18T17:04Z): Stuart's document says it is fixed and proven by a clean rebuild of develop on 19 Oct (33 services). Ask on the ticket for the rebuild evidence, or record his document's claim as the evidence and close it if the ticket's own acceptance is met. Say which you did.
4. Read Wednesday's triage for the context of every item: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_stuart-list-triage/TRIAGE.md` (rows 2a, 4b, 5, 9b, 9c, 10).

## PARTITION

Yours: api-gateway `routes/platform.ts` (the register-connector hunk) and the security service's key creation default if the build needs it (say so before touching it). **R 52nd (Secuura/Blockchain-R) has KS-1622 queued on the SAME file `routes/platform.ts` (the audit-log hunk): it now waits until your KS-1195 PR merges.** R also owns api-gateway `src/index.ts`, `src/services/health.ts`, auth `middleware/authenticate.ts`, originate `routes/verification.ts`. **Seat C 25th (Secuura/Blockchain-C)** owns originate `routes/documents.ts` (KS-1402). You share an inbox with both: a brief naming another seat is not yours.

## HOLDS

- **Identity:** before the first commit in ANY clone, set `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai` LOCALLY, then read back `git config --show-origin user.email`. This Studio's global identity belongs to another client.
- **Push from the branch you push** (check it out): the repo's pre-push hook refuses any push whose tip is not the checked-out HEAD. No `--no-verify`, ever. Transport in full (`-c core.sshCommand=...` with `ServerAliveInterval`).
- Merge only on Wednesday's head-pinned GO after a gate verdict. No deploy. No key rotation (Kam's).
- Client-facing communication = ticket comments only; the extranet is not a channel. Never promise a date.
- No Docker on this Studio. Rotate inside your 80-90 band at a clean boundary; write the handover first.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- secuura-ks1195-s-key-ceiling-1009 = **a** (2026-10-09 10:06:06): lands in a KS-1195 comment (item 1) and the build (item 2).
- secuura-ks1384-anchor-per-event-1009 = **a** (2026-10-09 10:06:00): lands in a KS-1384 comment (item 1).

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- KS-1604's fix shape = bind at the organisation level (Stuart's proposal).
- KS-1622 waits for your KS-1195 merge (same file).
- No Docker on the Studio for any seat.

PROVENANCE:
- KS-1402 (In Progress, 12 comments, last 2026-10-15T06:32Z; Seat C 25th's, named here only as a deploy condition) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- KS-1195, KS-1384, KS-1385, KS-1612, KS-1604, KS-1575, KS-1596, KS-1387 states, comment counts and last comments (as quoted inline) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- the two cards, their options and ruling timestamps | Wednesday's tools/decision_queue.sh show - my project, not yours | read 2026-10-19
- platform.ts has 0 rateLimit; security index.ts:666 default 1000 | Wednesday's triage report /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_stuart-list-triage/TRIAGE.md row 2a (a helper's git grep at 7e2f8157), not re-measured by Wednesday | read 2026-10-19
- develop 7e2f8157cec2 and the two merges | git ls-remote origin and Wednesday's own scratch-clone fetch | read 2026-10-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-19 16:18
