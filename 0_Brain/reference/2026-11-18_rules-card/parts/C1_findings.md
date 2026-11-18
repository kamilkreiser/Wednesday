# C1 findings — audit C (rule accuracy + status), listC.txt lines 1-19

| file | audit | what was wrong | evidence |
|---|---|---|---|
| 2026-08-12_hpsm-continuous-readiness-grant.md | C | Row is self-contradictory: status `live` but the rule says "ENDED grant", so Tuesday's card carries a non-rule. The end date it asserts ("architecture round began 2026-09-10") is NOT in the lesson: frontmatter L5 `status: live`, no end marker anywhere in the 43 lines. The operative content (readiness only; stop when the queue is dry) was dropped. Fix keeps `live` and states the grant with its end condition. If the coordinator can show the project started (the later HPSM-POC build/Azure grants of 2026-10-03 and 10-23 suggest so, but no lesson read here says they are the same project), the correct alternative is status `dead`, not live-with-"ENDED". | L10 "until the project starts or Kam lifts it"; L22 "NO build, NO Azure resources, NO billing, nothing HP-facing"; L37-39 "when the queue runs dry, STOP and say so"; 2026-09-15_never-idle...md L16 still cites this grant's duty five days after the claimed end |
| 2026-08-06_ghost-suggestions-in-panes.md | C | "a non-dim submitted line is real" overstates the current form. The 09-05 corrected headline says a submitted line is read on its merits and VERIFIED like any tap, and signature-class prefers DKIM mail; rung 9 shows a submitted turn can be an accepted suggestion. "Real" reads as "authorised". | L246 "not dim = a submitted line ... read on its merits, verify by the same means as any tap, and where the stakes are signature-class prefer the DKIM mail"; L207-209 "a signature-class action on a transcript turn requires `promptSource: typed` AND wording that is not an echo of mine — or DKIM mail" |
| 2026-09-02_coo-actionable-tickets-never-wait-for-kam.md | C | A grant-type rule without what stays Kam's: the signature-class exception is missing, so the row reads as "drive everything". Also missing the same-evening refinement "actionable NOW" (back-burner is not a failure), and "assign only unassigned" dropped "new". The old row's "one ticket per logical unit" was dropped to fit 260 chars (it restates the default after a withdrawn rule, L60). | L20 "Signature classes unchanged: production, money, external comms, irreversible actions still pause; deploys still need a ruling"; L27 "a predicate about WHO, not WHEN"; L56 "the ruling was only to new or unassigned items" |
| 2026-08-14_i-read-representations-they-read-sources.md | C | Not the current form: the latest sharpening (2026-09-08, the acknowledgement is the hop that compresses; quote the scope word) is absent. Rest of the rule is correct. NOTE for audit B (field not changed by me): enforced_by `board_count.sh` covers only counts taken through it; the lesson itself says the other sub-rules are rules, not mechanisms, yet the card truncates this row to 120 chars under "the tool remembers". | L392 "When acknowledging a scoped statement, quote the scope or quote nothing."; for B: L106-107 "it governs counts I take THROUGH it, and cannot stop me hand-writing a query elsewhere"; L109 "The four unmechanised ones will recur" |
| 2026-09-03_a-ratified-design-has-two-halves.md | C | Trigger list includes `deploy` but the rule carried nothing for that moment; the lesson's closing step (screenshots to Kam before deploy, the only instrument that ever caught this class) was missing. | L43 "Any round that changes what a page IS ends with rendered screenshots to Kam, both modes, before the deploy" |

CHECKED: 19  WRONG: 5

Status: all 19 rows are marked `live`; none of the 19 lessons carries a superseded/dead marker in frontmatter or body (only doubt: the HPSM grant above).

Found correct (14):
- 2026-08-03_contemplation-the-cockroach.md
- 2026-08-03_go-slow-earn-autonomy.md (the clause "relaxed by later grants" is not in this file; not verified here)
- 2026-08-04_delegation-v2-observability.md (the "no NEW delegations until redesign approved" constraint at L25 is omitted; treated as lapsed, not verified)
- 2026-08-05_identities-float-verify-always.md
- 2026-08-06_artifact-presence-is-not-execution.md
- 2026-08-07_a-check-that-cannot-fail.md (the 27 moved case sections in the `_cases_` file were not read)
- 2026-08-07_enumerate-every-surface-before-done.md
- 2026-08-09_an-enforcement-you-must-arm-is-not-one.md
- 2026-08-13_headline-must-match-the-operative-case.md
- 2026-08-16_a-recorded-blocker-is-not-a-boundary.md
- 2026-08-17_conversation-needs-a-stable-panel.md
- 2026-08-21_decision-queue-and-rotation-rhythm.md (omits the 70% rotation point, L22; a separate auto-rotate lesson is linked)
- 2026-08-25_travel-drive-stale-pointers.md
- 2026-08-28_contemplation-mistakes-and-the-fixed-will.md
