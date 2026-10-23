# Kam-awaiting cards: verification report, 2026-10-23 (drafted ~11:40 AEDT by a card-drafting agent for Tuesday)

Drafts only. Nothing was posted, added or sent. Cards: `0_Brain/projects_index/2026-10-23_kam-awaiting-cards.json` (13 cards, `decision_queue.sh add --json` shape: id, client_project, title, bluf, options, recommended, default_action).

## Counts (printed by the classifying script, `scratchpad/awaiting/build.py`)

| Project | Candidates | CARD (tickets/rows) | NOT A CARD (ruled) | TUESDAY RULES | STALE | Cards to post |
|---|---|---|---|---|---|---|
| Composer | 11 | 2 | 6 | 0 | 3 | 2 |
| HPSM-POC | 27 | 17 | 4 | 3 | 3 | 9 |
| MPS | 23 | 4 | 5 | 9 | 5 | 2 |
| **All** | 61 | 23 | 15 | 12 | 11 | 13 |

## For the morning card: what is awaiting Kam, per project

- Security Composer: 2 cards (of the 11 rows Tuesday counted: 6 already ruled, 3 stale, 2 genuinely his).
- HPSM-POC: 9 cards covering 17 of the 27 labelled tickets (3 stale labels, 4 already ruled, 3 Tuesday rules).
- MPS Commercial Calculator: 2 cards covering 4 of the 23 needs-ruling tickets (9 Tuesday rules, 5 ruled, 5 stale).
- Total on the board after posting: 13 new cards plus the 1 already open (composer-l05-setup-card-too-1014) = 14.

Correction for the record: Tuesday's "11 items waiting on Kam" for Composer was a count of rows by state wording. At source only 2 are open for him; 9 were ruled (C-71 COMP-1/2/17) or superseded.

## Caveats

- Jira reads were as of ~11:30 today, read-only, label queries `project = HPSMPOC AND labels in (owner-kam, needs-kam, awaiting-hp) AND statusCategory != Done` (27) and `project = MPSCALC AND labels in (needs-ruling) AND statusCategory != Done` (23). Tickets whose last comment is old may have been settled by mail or chat that this agent did not read (chat store not read; mail fenced). Tuesday should skim the HP-POC cards for items Kam already did (PO, M2 signature, showcase notes, deputy name) before posting.
- The HPSM-POC project folder's own CLARIFICATIONS.md is stale (29 Sep); the live record is the analysis repo, not checked out here. Rulings were taken from decisions.json (read, never run) and Jira comments.
- The existing open card composer-l05-setup-card-too-1014 was not duplicated.

## Per candidate

### Composer

| Key | Class | Evidence / reason |
|---|---|---|
| #1 | STALE | Guide v1.2 is final for Paul (C-09); the guide is now v1.5 (BACKLOG #275 row) and edits to it are held under COMP-16 (a) (C-71). Nothing of Kam's remains on this row. |
| #17 | STALE | v1.3 was held (card composer-guide-v13-to-paul => b, 27 Sep); v1.4 card composer-guide-v14-to-paul was withdrawn; the guide moved on to v1.5. Superseded. |
| #21 | STALE | Examples built and live since 27 Sep (C-09, rechecked in later C-entries); no decision hangs on them. They go read-only at #252's deploy, which COMP-1 (b) holds. |
| #35 | NOT A CARD (already ruled) | C-71 COMP-2 (a): Hold them all (Guided mode off). |
| #54 | NOT A CARD (already ruled) | C-71 COMP-17 (a): Keep all six parked (row text itself ends "Ruled 2026-10-12 (C-71, COMP-17)"). |
| #55 | NOT A CARD (already ruled) | C-71 COMP-2 (a): Hold them all. |
| #73 | NOT A CARD (already ruled) | C-71 COMP-17 (a): Keep all six parked. |
| #101 | NOT A CARD (already ruled) | C-71 COMP-17 (a): Keep all six parked. |
| #249 | CARD composer-e8-mapping-review-1023 | Draft mapping sme_check = "not started" on b93/e8-mapping-draft @ b2788db (git show, read-only); C-57 names Kam and Paul as reviewers; approval is Kam's. |
| #252 | NOT A CARD (already ruled) | C-71 COMP-1 (b): After Paul's current review round. A deploy card comes when his round ends. |
| #329 | CARD composer-send-five-questions-1023 | C-96 (K10 a) ruled "Kam sends"; the note exists but the row says not sent. The ruling is made; the send is his act. |

### HPSM-POC

| Key | Class | Evidence / reason |
|---|---|---|
| HPSMPOC-1 | STALE | Epic container (Commercial & Governance); its own comment says it closes with its last child. Not an ask. |
| HPSMPOC-3 | CARD hpsmpoc-po-confirmation-1023 | Executed only once the PO is approved; no PO recorded since 1 Oct. |
| HPSMPOC-6 | CARD hpsmpoc-deputy-po-name-1023 | Card hpsmpoc-sme-deputy-1019 ruled a ("reply with the name"); the tap has no name and Jira shows none. Verify the name was not typed elsewhere before posting. |
| HPSMPOC-20 | CARD hpsmpoc-m2-signoff-recorded-1023 | Card hpsmpoc-m2-po-signoff-1008 ruled a (email the pack to sign); no signature recorded since. |
| HPSMPOC-51 | CARD hpsmpoc-baseline-hours-metrics-1023 | Baseline null; M1-M7 PROPOSED; last comment 27 Sep. |
| HPSMPOC-82 | CARD hpsmpoc-open-vendor-asks-1023 | Software and NFR licence arrived 2 Oct; live system with devices and integration/API reference still open. |
| HPSMPOC-83 | STALE | Quick Assess dropped from the HP request on 2 Oct (HPSMPOC-181 comment). The ask is gone; close the ticket. |
| HPSMPOC-84 | STALE | Control Hub answered 1 Oct (separate SMB tool) and removed from the HP request 2 Oct (HPSMPOC-166 comment). Close the ticket. |
| HPSMPOC-85 | CARD hpsmpoc-open-vendor-asks-1023 | Firmware vulnerability tool access, still awaiting HP. |
| HPSMPOC-86 | CARD hpsmpoc-open-vendor-asks-1023 | Fleet Threat Assessment access without VPN still awaiting HP. |
| HPSMPOC-90 | NOT A CARD (already ruled) | Card hpsmpoc-c30-feedback-route => a (29 Sep) and hpsmpoc-feedback-button-live-proof-1021 => a (21 Oct): the live proof is already ruled and owned by a seat. |
| HPSMPOC-91 | CARD hpsmpoc-pre-engagement-pack-wording-1023 | Packs built and merged; only the Kam/SME wording is owed (comment 16 Oct). |
| HPSMPOC-94 | CARD hpsmpoc-open-vendor-asks-1023 | Card hpsmpoc-hp-content-gaps-tell-hp-1021 => a (tell HP in the cover note); HP content still not supplied. Rides in the chase card. |
| HPSMPOC-97 | CARD hpsmpoc-open-vendor-asks-1023 | Checklist of HP's 29 Sep follow-ups; overlaps -166 and -181. |
| HPSMPOC-162 | TUESDAY RULES | No draft exists yet (0 comments). Recommended ruling: Tuesday commissions the HPSM-POC seat to draft the three pieces as DRAFT (statement, snapshot question, further-assessment line); Kam reviews when the draft exists, not before. No card until then. |
| HPSMPOC-163 | TUESDAY RULES | No draft exists yet (0 comments). Recommended ruling: Tuesday commissions the band readings (green/amber/red) as DRAFT alongside the weights; Kam reviews with the weights bundle before it goes to HP. |
| HPSMPOC-164 | NOT A CARD (already ruled) | Card hpsmpoc-hp-review-which-build-1021 => b (UAT first) and the 21-22 Oct UAT cards; the invitation card was withdrawn and replaced by Tuesday's checklist. |
| HPSMPOC-165 | CARD hpsmpoc-consulting-offer-package-1023 | Content is Kam, Paul and Peter's; seats may not invent it. |
| HPSMPOC-166 | CARD hpsmpoc-open-vendor-asks-1023 | Checklist of HP's 1 Oct follow-ups; four lines tracked in -181. |
| HPSMPOC-167 | CARD hpsmpoc-open-vendor-asks-1023 | Waits on HP's current generic deck. |
| HPSMPOC-168 | CARD hpsmpoc-industry-choice-list-1023 | Proposal for Kam to accept or decline (ticket says "If Kam declines, close this ticket"). |
| HPSMPOC-181 | CARD hpsmpoc-open-vendor-asks-1023 | Four HP workstreams narrowed 2 Oct; nothing recorded as arrived. |
| HPSMPOC-237 | NOT A CARD (already ruled) | Card hpsmpoc-review-week-larger-plan-1021 => b (21 Oct). |
| HPSMPOC-241 | CARD hpsmpoc-open-vendor-asks-1023 | Sent 8 Oct (card hpsmpoc-hp-questions-send-1008); HP answered 5 of 9 on 16 Oct; the other 4 are a chase, not a send. |
| HPSMPOC-242 | CARD hpsmpoc-showcase-notes-1023 | Card hpsmpoc-showcase-notes-to-tickets-1021 => a ("I'll send them today"); ticket still an empty placeholder. |
| HPSMPOC-257 | TUESDAY RULES | Ticket says "Who decides: Kam" but it is a hardening trade-off with no user-visible cost beyond obscure file names. Recommended ruling: (c) keep the NFKC fold as built and accept the over-refusal (a refusal is the safe side; pin it with the test row). Tuesday may instead post it if she reads it as Kam's. |
| HPSMPOC-268 | NOT A CARD (already ruled) | Card hpsmpoc-runtime-10013-route-1018 => a: wait for Azure, read it at the next deploy (the 20 Oct comment confirms the wait, no action asked). |

### MPS

| Key | Class | Evidence / reason |
|---|---|---|
| MPSCALC-95 | STALE | Ruled by Friday and built (13 Oct comment); only the ticket label is stale. |
| MPSCALC-109 | STALE | Merged in PR #49 (17 Oct); "Open after merge: nothing from the review". |
| MPSCALC-112 | TUESDAY RULES | Recommended ruling: singular "and 1 more rate (see full proposal)", folded into the next words pack (same precedent as MPS-11 in the 12 Oct pack, which Kam accepted); not its own card. |
| MPSCALC-113 | TUESDAY RULES | Recommended ruling: leave the 5+1 wrap; Kam ruled "fill the row" (mpscalc-dashboard-seventh-tile-1013 => c) and the three-across step was marked optional/unruled. Cosmetic. |
| MPSCALC-128 | TUESDAY RULES | Recommended ruling: keep both figures and make the card show the breakdown's cents-rounded sum so they agree (consistent with mpscalc-rental-parts-cents-rounding-1013 => a); wording change, if any, goes in the next words pack. |
| MPSCALC-129 | NOT A CARD (already ruled) | Card mpscalc-rental-book-words-1014 => a (its Fixes 1-3 are these three sentences). |
| MPSCALC-137 | NOT A CARD (already ruled) | C-45 (20 Oct) and K-01 (mps-paul-review-roles-k01-k18-1016 => a): owner self-approval, audited; planned as T-V7-6. |
| MPSCALC-144 | NOT A CARD (already ruled) | Card mpscalc-large-format-manual-items-1017 => b (C-35): add the items after MPSCALC-202 and 203 are live. |
| MPSCALC-153 | STALE | Merged in PR #68 (17 Oct); nothing open. |
| MPSCALC-157 | STALE | Merged in PR #50 (17 Oct); nothing open. |
| MPSCALC-159 | NOT A CARD (already ruled) | K-12 deferred: mps-paul-review-pricing-k09-k11-k12-1016 => a (build K-09 then K-11; defer K-12). Waits on HP data; nothing to rule now. |
| MPSCALC-177 | STALE | Built on Kam's K-19 = a ruling (16 Oct); ready pending CI. |
| MPSCALC-188 | NOT A CARD (already ruled) | Ruled (a) accept for release 1: roles card K-01/K-18 => a, 16 Oct (comment cites it verbatim). |
| MPSCALC-202 | TUESDAY RULES | Recommended ruling: yes, widen PRE-1 to count everything the app refuses at boot and wrap pre1_count so a bad shape prints one STOP line (technical deploy-safety scope; C-24 as amended). |
| MPSCALC-204 | TUESDAY RULES | Recommended ruling: ownership and state checks answer before the range check (WHO before WHAT), and skip the maximum check when the floor already failed. API behaviour only. |
| MPSCALC-222 | TUESDAY RULES | Recommended ruling: the runbook states "roll forward only" once a Care pack or Staging row exists, and the deploy card carries the hand count (B268 already measured it as 0). |
| MPSCALC-224 | TUESDAY RULES | Recommended ruling: record the residual until the host image moves, read the platform log patch line at each deploy (same posture Kam ruled for HPSM-POC: hpsmpoc-runtime-10013-route-1018 => a). |
| MPSCALC-226 | TUESDAY RULES | Recommended ruling: no code change; the next deploy card states that after the class and care-pack branches a rollback hides calculated care-pack quotes, so roll forward. |
| MPSCALC-228 | CARD mpscalc-deal-usage-edge-rules-1023 | Not covered by mpscalc-deal-usage-proposal-rates-1017 (which ruled printing rates at all) or the 20-22 Oct cards (searched). |
| MPSCALC-229 | CARD mpscalc-deal-usage-edge-rules-1023 | Same: gate B170's question to the owner. |
| MPSCALC-230 | CARD mpscalc-deal-usage-edge-rules-1023 | Same: gate B170's question to the owner. |
| MPSCALC-261 | CARD mpscalc-rental-credit-authorisation-1023 | Ticket says the authorisation rule has no D card and "waits for a ruling"; D-01..D-15 were accepted without it. |
| MPSCALC-316 | TUESDAY RULES | Recommended ruling: state the unit once ("at most 100 UTF-16 code units; an emoji counts as two") in docs/API.md and openapi.json; a docs line, no behaviour change. |
