# A2 findings — audit A (seat scope), listA.txt lines 29-56

| file | audit | what was wrong | evidence |
|---|---|---|---|
| 2026-09-23_build-seats-run-in-cockpit-panes.md | A | seats `friday`; rule is general conduct (build work goes to a visible pane seat, subagents only for short passes) using fleet-wide tools (wed_claim.sh, send_brief.sh, usage_gate.sh) that every coordinator runs; it merely arose on Friday. Should be `all`; rule reworded from 'When Friday starts' to 'When I start'. | L9 headline: "Build seats run in VISIBLE cockpit panes; in-session subagents are for short reading and drafting only"; L4 Kam: "yes, use cockpit panes for build seats going forward"; L16 names wed_claim.sh / send_brief.sh; nothing in the file is laptop-only. |
| 2026-09-24_decisions-go-on-the-fleet-activity-panel.md | A | seats `friday`; decision_queue.sh and the live board are fleet-wide, and the 2026-11-10 extension (201 = storage only; ask for the footer line) is a general diagnostic rule. Only items 5-6 (the Friday TAB, friday-seat hide) are seat-specific and the row's rule does not carry them. Should be `all`; rule reworded to 'When I need'. | L15 "`2_Project_Files/tools/decision_queue.sh add --json`"; L43-44 "When Kam says he cannot see something on the board, ask for the footer line... A post's HTTP 201 is never evidence that a card 'is on the board'"; L34 family: "the queue was already his preferred surface". |
| 2026-09-27_hpsmpoc-every-hp-ask-is-its-own-email-plus-a-register.md | A | seats `friday`; this is a Datasec project rule ("as a rule for the project"), not a laptop-owned thing. Datasec -> `tuesday,friday`. (Lower severity: the lesson is written with Friday as actor, and Tuesday's feedback sweep currently excludes HPSM-POC.) | L6 "tier: P-Datasec/HPSM-POC"; L10 Kam: "Do this as a rule for the project"; L18 "Scope: HPSM-POC". |
| 2026-09-30_qa-gates-may-switch-to-opus48-when-flagged.md | A | seats `tuesday`; the grant covers Datasec QA gates, which Friday also launches; the dialog and the shared-config hazard exist on any seat. Should be `tuesday,friday`; rule now says 'Datasec QA gate' (the scope word the row dropped) and 'the coordinator' instead of implying Tuesday. | L11 "a QA gate session (any Datasec gate this seat launches)"; L16-17 Kam: "Let QA gates switch to Opus 4.8 when flagged"; L35 "Scope: QA gates only." |
| 2026-10-04_as-much-secuura-work-as-possible-spark-and-claude.md | A | seats `wednesday`; a standing Secuura-client throughput rule, not about a Studio-owned thing (its only Studio-specific part, the Spark, is dead). Secuura -> `wednesday,friday`; 'plus local-model work' qualified because Friday has none. | L10 Kam: "do as much work with the spark and claude agents on the secura projects as you can"; L13 "Wednesday is choosing the next Secuura work"; L16 "Expiry: none stated". |
| 2026-10-05_board-taps-suffice-for-audit-redates.md | A | seats `wednesday`; the grant names a channel Kam accepts for a class of ruling on Secuura repos (audit-baseline.json, lock-discovery.mjs); nothing Studio-owned. Secuura -> `wednesday,friday` (Kam's words carry no client scope at all, so `all` is arguable; kept to the client the lesson evidences). Rule text unchanged. | L12 Kam: "board taps are enough for audit re-dates"; L19 "Secuura seats treated a re-date as approval-class". |
| 2026-10-08_fix-our-own-problems-involve-peter-sporadically.md | A | seats `wednesday`; a Secuura client-conduct rule (Peter, Platform K), nothing Studio-owned. Secuura -> `wednesday,friday`. Rule text unchanged. | L11 "a Secuura problem has turned up ... and Wednesday is about to route it to Peter"; L13 Kam: "We are working on a new approach where we fix our own problems and tickets and only involve Peter sporadically." |
| 2026-10-10_merge-and-archive-when-done-and-ready.md | A | seats `wednesday`; a Secuura grant that by its own text restates the 2026-09-11 TESTED grant, whose index row is already `wednesday,friday`; the two rows disagree. Should be `wednesday,friday`; 'Wednesday's completion check' -> 'the coordinator's'. (Judgment call: it is a grant given on view=wednesday; reject this fix if Kam's grants are held to the seat they were spoken to.) | L17 "This restates the open-ended 2026-09-11 TESTED grant; nothing new is authorised for merges."; L11 "a Secuura PR has passed its QA gate". |

CHECKED: 28  WRONG: 8

## Left narrow on purpose (judgment, not counted wrong)
- 2026-10-03_hp-security-manager-azure-deploy-grant.md (`friday`) and 2026-10-06_push-to-demo-when-ready-no-card.md (`friday`): Datasec projects, so the client rule would give `tuesday,friday`; but both are money/deploy GRANTS addressed to Friday by name (10-03 L11 "Friday is about to create Azure resources"; 10-06 L9 "Friday deploys it"). Widening would hand Tuesday a deploy/spend authority Kam did not speak to it. Kept `friday`.
- 2026-10-12_boot-sweeps-all-feedback-repositories.md (`tuesday`): a Tuesday boot ritual; its exclusions are the projects another seat covers (L14). Kept.
- 2026-10-07_archive-bulky-leftovers-to-g-drive-clear-after-a-month.md (`wednesday`): G-DRIVE is mounted on the Studio only (L16). Kept; note item 5 ("any disk-freeing brief names the G-DRIVE option") is only usable from that seat.
- 2026-09-25_three-tier-routing…, 2026-10-08_ornith-15…, 2026-10-09_spark-first-model-choice… (`wednesday`): Ornith / night queue, Studio-owned. Correct. 2026-10-01_friday-cloud-threshold-90.md (`friday`): L15 "this seat (the Friday tab)". Correct (its enforced_by is audit B's).
- 12 dead/superseded rows in this slice: seats has no effect on any card; status checked against frontmatter and found off-card either way. One vocabulary mismatch, not fixed: 2026-10-10_today-mainly-spark-and-sonnet… is `dead` in the index while its frontmatter says `superseded` (L5); 2026-10-05_october-deploy… and 2026-10-08_new-account… are `dead` in the index while frontmatter still says `status: live` with a passed `expires` (the index is right, the lesson frontmatter is stale).

## Found correct (seats)

- 2026-09-23_spark-kit-running-a-local-coding-model.md
- 2026-09-23_use-the-local-model-as-much-as-possible.md
- 2026-09-25_spark-calibrate-like-ornith-start-high-oversight.md
- 2026-09-25_three-tier-routing-ornith-spark-cloud-always-on.md
- 2026-09-29_datasec-github-commits-go-through-codeql.md
- 2026-10-01_friday-cloud-threshold-90.md
- 2026-10-03_hp-security-manager-azure-deploy-grant.md
- 2026-10-05_october-deploy-both-boxes-when-ready.md
- 2026-10-05_spark-target-50-tasks-a-day.md
- 2026-10-06_past-70pct-spark-takes-80pct-of-tasks.md
- 2026-10-06_push-to-demo-when-ready-no-card.md
- 2026-10-06_use-to-100pct-spark-all-tickets-one-or-two-deployers.md
- 2026-10-07_archive-bulky-leftovers-to-g-drive-clear-after-a-month.md
- 2026-10-08_new-account-push-merge-test-as-much-as-possible.md
- 2026-10-08_ornith-15-replaces-10-push-it-harder.md
- 2026-10-08_use-to-100pct-raise-gate-merge-seats-only.md
- 2026-10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis.md
- 2026-10-09_spark-ornith-sonnet-only-until-monday.md
- 2026-10-10_today-mainly-spark-and-sonnet-double-check-everything.md
- 2026-10-12_boot-sweeps-all-feedback-repositories.md
