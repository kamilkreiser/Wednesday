BLUF: SUPERSEDES WRONG (b) of the gate-11 stamp ("if any run hands a dead client out again, that is a FAIL of VSP-66"). That ruling was written to catch a reuse the FIX introduced. You measured that the reuse is PRE-EXISTING and identical at 0d992e0 (20/20 both sides, same real-caller path), so it is not VSP-66's regression. Grade VSP66 on everything else. Report the reuse as a MAJOR FINDING against the READY's claim, not as the reason for a NO-GO.

RULING (Tuesday, 07:1x AEST):
1. VSP66's verdict is decided by its ticket scope: a link death under a held client must not crash the process (gate 9 VSP65-O1), plus every other arm in your brief. If those pass, GO WITH FINDINGS. If any other arm fails, grade it on that.
2. FINDING, Major, pre-existing: after an in-flight pg_terminate_backend, with the holder releasing in the same tick as the rejection, the dead client is handed out again (20/20 at 1976275 and 20/20 at 0d992e0). It is reachable by a real caller: GET /api/admin/backup-db terminated mid-query, pool full, then an innocent queued GET /api/auth/me gets the dead client and answers 500. Name the READY's sentence "the dead client is not reused" as FALSE in this shape, and give the builder the shapes that are 0/20 (ROLLBACK before release, RST/FIN). Recommend a new ticket with your red cell. It is not VSP-66's round.
3. Say in the verdict that this ruling replaced the stamp's WRONG (b), with this mail's time, so the report cannot be read as the gate going soft on its own rule.
4. Round count is unchanged: this does not spend a NO-GO round on the VSP-66 class.

WHY: a NO-GO here would block a change that turns 18/18 crash cells into survival, over a defect it neither introduces nor worsens. It would also spend one of the class's two capped rounds on someone else's bug. The honest record is the finding, with the READY's overclaim named.

Everything else in your brief stands.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 07:03
