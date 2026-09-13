# S40 switch-on REPORT noted and verified. Card c12 was ruled build-c12 (it crossed your report). Lane R takes S40's proofreading notes

**BLUF.** **For session 40 (seat hpsm-dc13) and session 42 (seat hpsm-3e04).**

**For S40:**
1. **Your 04:08:07Z report is noted, and Tuesday verified it at source (14:09).**
   - The Azure demo returns 401 with no credentials and with wrong credentials, `WWW-Authenticate: Basic`, `/api/health` 401, TLS verify 0.
   - `pc-lane-a` answers 200 on 127.0.0.1:18580; edge, api, worker, idp and web were recreated about 6 minutes earlier, all healthy.
2. **Card `hpsm-composer-demo-release-unreachable-c12` is NOT open any more.** Kam tapped it at 14:04:45 AEST: **`build-c12`**. S42 has a new lane for engine C12 mapping plus fenced synthetic adapter rows, and it may not land by Monday.
   - **Nothing is asked of you now.** Both stacks stay exactly as they are.
   - The next upgrade message from S42 names the new demo `CONTENT_HASH` and its checks.
3. **The verifier re-run on the merged head is S42's call.** Stand by.

**For S42:**
4. **Lane R takes S40's proofreading notes, in the same source-first way as Tuesday's 04:05:32Z list:**
   - **(d) The policy document's Device groups table prints the group's uuid instead of its name.** Show the name; the uuid only where the spec asks for it. If the name is not in `RenderInput`, list the API change for lane Q, and do not reach into `apps/api`.
   - **(e) Check the Preview's Remediation column wording ("Enable"/"Disable") and the two empty firmware-path rows against HP's sample Policy Preview.** Change them only where the sample differs, and cite the sample page.
5. **Both reach the live stacks at the next upgrade, after lane R merges.** The priority order stands: lane R, then lane C12, then Q and W.

## Unchanged
- No push. A combined tier-1 gate is due before any push. Access control stays on the Azure demo.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 14:10

Tuesday
