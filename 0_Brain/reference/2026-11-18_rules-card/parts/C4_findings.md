# C4 findings — audit C (rule accuracy + status), listC lines 58-75

| file | audit | what was wrong | evidence |
|---|---|---|---|
| 2026-10-15_storage-policy-for-old-blockchain-files-and-tests-monday.md | C (status + rule) | Marked `dead` as a passed one-off; the rule says later removals follow never-delete "not this grant". Wrong on both. The lesson's frontmatter is `status: live` and its body sets a STANDING narrowing of never-delete plus a regular clean-up. The Monday deliverable was produced and Kam approved it, so the policy is the operative rule for Secuura/Blockchain storage today. Marked dead, it is on no card. Fix: `live`, family `never-delete-quarantine`, rule points at the approved policy. Note: the lesson file itself does not record the approval (it still reads "nothing is removed until the policy exists and Kam has seen it"). | Lesson L5 `status: live`; L17 "this NARROWS [[2026-08-26_never-delete-cleanup-means-quarantine]] for the classes the policy names"; L19 "\"Regularly\" = a scheduled mechanism". Tree: `1_Project_Definition/Policies/2026-10-19_secuura-blockchain-storage-policy.md` L4 "status: APPROVED — Kam ruled card wed-secuura-storage-policy-1019 = a"; `0_Brain/dashboard/data/decisions.json` card `wed-secuura-storage-policy-1019` `ruled_choice: a`, option a: "Weekly removals of the same classes then need no card." |
| 2026-10-12_secuura-done-when-tested-works-deployed-and-never-idle.md | C (rule, missing condition) | The rule reads as if unit tests on develop + fix in the running build always suffice. The lesson's amended form requires the live check wherever one is possible; the unit-test route is only for tickets with no live check possible. The fix drops the tail "needs go on Kam's board" to fit 260 chars (other rows carry that rule). | L21 "Where a live check IS possible, it is made before the close." and L18 "Close when unit tests pass on develop AND the fix is in the running Kintsugi build; the closing comment says 'no live check possible'" |
| 2026-10-09_spark-ornith-sonnet-only-until-monday.md | C (superseded pointer) | Status `superseded` is right, but the `->` names 2026-10-08_sonnet-trials…, a file dated BEFORE this one and itself marked partly superseded. The lesson names model-routing.md v1.0 (Kam 2026-10-18) as what governs now; that lesson exists. | L5 "status: superseded — whole file (… routing now by fleet/specs/model-routing.md v1.0, Kam 2026-10-18)"; `2026-10-18_model-routing-v10-approved-route-by-the-table.md` exists; 2026-10-08_sonnet-trials… L4 "status: live — PARTLY SUPERSEDED 2026-11-16" |
| 2026-10-24_every-boot-works-the-actionable-tickets-unprompted.md | C (cosmetic) | Two sentences run together with no full stop ("launch in waves Signature classes and gates stand"). Content is correct. | Index row text; lesson L20 and L22 are separate points |

CHECKED: 18  WRONG: 4 (1 status, 2 rule content/pointer, 1 cosmetic)

Status rows verified (7 of the 18 are dead/superseded): 6 supported by the lesson or the tree, 1 wrong (10-15).
- 10-08 use-to-100pct: dead, L5 "status: expired".
- 10-10 today-mainly-spark: `dead` kept. The frontmatter literally says "superseded" (L5, by the Spark's return), but the grant ended on its own date (L7 "expires: end of Saturday 2026-10-10"), so dead fits the spec. Either status keeps it off every card.
- 10-26 spark-gate-pilot and 11-12 spark-for-harness: superseded, L5 in each; the `->` target 2026-11-15_the-spark-is-gone… exists.
- 10-28 never-idle-spark: dead, L5 "status: retired".
- 11-16 grant-build-coagent: dead, `0_Brain/tasks/EXPIRING-GRANTS.md` L12 "EXPIRED 2026-11-17 07:26 AEDT — its EVENT happened: Kam reviewed".

Found correct (14):
2026-10-08_use-to-100pct-raise-gate-merge-seats-only.md
2026-10-10_today-mainly-spark-and-sonnet-double-check-everything.md
2026-10-16_tuesday-boot-sweeps-project-feedback-into-tickets.md
2026-10-22_tuesday-sonnet-default-usage-is-a-guide.md
2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice.md
2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md
2026-10-30_kam-and-stuart-meet-monthly-on-long-term-development.md
2026-11-06_clear-the-secuura-board-over-one-to-two-weeks.md
2026-11-11_wednesday-offloads-to-dev-working-nas.md
2026-11-12_spark-for-harness-and-token-heavy-simple-tasks.md
2026-11-15_recent-merge-rules-override-historic-holds.md
2026-11-16_grant-build-coagent-overnight-until-the-morning-review.md
2026-11-16_preflight-failure-must-not-kill-a-rotation.md
2026-11-18_a-gate-keyed-on-tool-names-misses-the-next-tool-that-runs-a-command.md

Minor, not changed:
- 10-16 tuesday-boot-sweeps: the rule omits that the project's own agent files the ticket, never Tuesday's hands (L19); the general manage-don't-do rule covers it.
- 10-22 tuesday-sonnet-default: the 16:52 extension's rule 4 (Tuesday owns the daily workload plan and says when she disagrees, L31) is not in the rule; it is a second rule in the same file.
- 11-06 clear-the-secuura-board: outer date 2026-11-20 is two days away; the row needs a re-check then.

Not checked: seats and enforced_by (other audits); whether weekly storage removals have actually run since 10-19.
