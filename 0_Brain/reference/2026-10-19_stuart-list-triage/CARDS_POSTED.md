# Cards posted from the Stuart-list triage (2026-10-19, ~16:15 AEDT)

Prior-ruling research for the five B-cards in TRIAGE.md. For each card a plain `decision_queue.sh add --json` was re-run (refused, logged 05:10:59Z to 05:11:21Z in `fleet/state/dq_prior_refusals.jsonl`). Then every match it named was read:
- leg-1 panel messages, read in full from `kam_msgs.sh 2000 --source both`;
- leg-2 ruled cards, opened with `show` where they share the ticket;
- the card store, searched for KS-1384/1402/1570/1580/1575/1596/1454, rowHash, stub and timestamp verb;
- DEPLOY-BLOCKERS.md:7 and EXPIRING-GRANTS.md:24.

None of the five ids was in the store before posting. The JSON-path `_override_prior` is stored only as a flag, so each card's measurement is also the closing "Prior-ruling check:" sentence of its BLUF. The final JSONs are in the session scratchpad `final/`.

## 1. secuura-ks1402-who-creates-the-holder-1019: POSTED (override, case ii)
- Decisive priors (a different question):
  - card `secuura-ks1402-lookup-refuses-connector-tokens`, ruled `a` 2026-10-02T09:59:22: "Widen /lookup to accept a connector token, as /stub already does (KS-564)".
  - card `secuura-ks1402-s-key-cannot-carry-users-read-1006`, ruled `a` 2026-10-06T09:58:21: "Originate resolves the holder with its own service credential (Stuart's option 2)".
  - Neither one rules who creates a holder who is not yet a K user.
- The other 13 matches: 5 panel messages from 08-21, 09-06 and 09-10 (an anchor-store forward, ticket categorising, PR triage), none on this ticket, plus 8 cards matching on holder/creates/1019.
- Tool: `added: secuura-ks1402-who-creates-the-holder-1019 (Secuura/Blockchain) ... [rec: a]`, `live-board: ... posted to Secuura (HTTP 201)`.
- Advisory printed: count_list_check flagged "13 share only generic words" against a 3-word list. This is a false positive: 13 counts matches, and the 3 items are the shared words.

## 2. secuura-ks1384-schedule-per-event-anchors-1019: POSTED (override, case iii: the card already says what was ruled and asks only the rest)
- Decisive prior: card `secuura-ks1384-anchor-per-event-1009`, ruled `a` 2026-10-09T10:06:00: "One anchor per lifecycle event". It ruled the shape, not the schedule. It has no delivery mark.
- `secuura-ks1612-third-round-after-cap-1018` (a, 2026-10-19T06:43:54) and `secuura-ks1612-round3-nogo-1019` (a, 2026-10-19T11:08:33) ruled #1568's gate rounds and only name KS-1384 as an alternative.
- The other 19 matches share only event, anchors or 1019:
  - panel messages from 08-17 to 09-15 (Purview, ATTIO, backlog, agents);
  - two event-date cards from another project;
  - the KS-1404 merge-order card;
  - the storage and author cards.
- Tool: `added: secuura-ks1384-schedule-per-event-anchors-1019 ... [rec: b]`, `live-board: ... (HTTP 201)`.

## 3. secuura-ks1580-erasure-revoked-key-code-1019: POSTED (override, case ii)
- No card and no panel message is on KS-1580. The store search found 0 cards citing it.
- Nearest priors, all on other tickets:
  - `secuura-ks1187-erasure-door-reads-back`, ruled 2026-09-17 10:40: "fix-now — Seat A builds the gateway door fix".
  - `secuura-ks1207-revoked-session-plus-junk-key-bypass`, ruled 2026-09-17 15:10: "build-after-1019".
  - `secuura-ks1352-revoked-credentials-still-verify` (a), `secuura-erasure-scope-gate` (A) and `secuura-ks695-erasure-merge-timing-1013` (b).
- The rest match on code, erasure or 1019 only, including 2 erasure cards from another project.
- Tool: `added: secuura-ks1580-erasure-revoked-key-code-1019 ... [rec: a]`, `live-board: ... (HTTP 201)`.

## 4. secuura-ks1570-round-may-deploy-1019: AMENDED, then POSTED (override, case iii)
- Already ruled, so the card no longer asks it:
  - The October grant, live board 2026-10-05 16:21:39 (EXPIRING-GRANTS.md:24): "for the month of October, keep pushing, keep publishing, deploy all that works and is ready but only when its ready.  Deploy to both servers, demo and kintsugi". It ends Sat 31 Oct.
  - The ADMIN shape: card `secuura-ks1570-admin-role-bound-shape-1013`, ruled `b` 2026-10-13T11:47:50. Its default text: "The deploy blocker stays on the list until KS-1570 is merged and Kam has seen it."
  - DEPLOY-BLOCKERS.md:7 (OPEN): "no deploy of develop to kintsugi or demo until KS-1570 is merged and Kam has seen it."
- What is left, and what the card now asks: has he seen it? Seeing it closes the row.
- Amendments:
  - New title.
  - The BLUF opens with the two rulings and quotes the grant.
  - Options: (a) "I have seen it: close the blocker row", deploying under the grant once Stuart's deploy lands and the 500 fix merges; (b) one-page summary first; (c) hold all deploys.
  - Recommended (a); default unchanged.
- The other 64 matches: deploy cards from other projects, earlier one-off kintsugi deploy rulings (each spent), and the 09-18 10:27 panel note "deploy to kintsugi. this is the dev server so it should be the first to update...", which sets the order, not this round.
- Tool: `added: secuura-ks1570-round-may-deploy-1019 ... — KS-1570 round: the ADMIN bound you ruled on 13 Oct is merged. Have you seen it? (Your October grant already covers the Kintsugi deploy.) [rec: a]`, `live-board: ... (HTTP 201)`.

## 5. secuura-s-signing-contract-additions-1019: POSTED (override, case ii)
- No card and no panel message is on KS-1575, KS-1596 or rowHash. The store search found 0 cards citing them.
- Nearest priors:
  - `secuura-ks719-contract` (require): a different contract.
  - panel 2026-09-03 13:36: "Decision secuura-ps-signing-key-provision-2026-09-03: leave — Leave — Stuart drives; mint at the next S prod deploy prep". A different subject.
  - `secuura-ks1385-anchor-identity-needs-ps895-ruling-1013` (b, 2026-10-13T18:54): it names KS-1454's column but does not rule these verbs.
- The BLUF check line adds that KS-1384's mapping is already ruled (9 Oct, a). Only its schedule is open, on card 2.
- Tool: `added: secuura-s-signing-contract-additions-1019 ... [rec: a]`, `live-board: ... (HTTP 201)`.

All five are confirmed `[open ]` in `decision_queue.sh list open` after posting.
