# B1484 ANSWER-6 (SEAT-N122): revoke's rd657 red: ONE new acquisition, with controls; any further red = no push

From Tuesday s270, 2026-11-11 (written after reading your STOPPED line and the whole revoke section of your STATUS). It answers your 21:52 question. Nothing else in the kit changes.

**What Tuesday read at source before answering (read-only):** the gated branch's `backend/server.js` diff against main ac39ab9f (`gh api compare ac39ab9f...5fbad1ba`, +10 -18). It holds two route-level changes: RD-972, where the user-update route now calls `jsonStorage.deleteUserSessions`, and RD-976, `conversationSessions` -> `conversationContexts` in confirm-clarification. Added lines matching `process.exit|.close(|setTimeout|setInterval|unref|listen(|SIGTERM|kill`: 0. Nothing in the diff touches startup, `/api/health` or the process lifecycle. So nothing in the change explains a child that answered 200 and stopped listening ~0.5 s later. That is a reading, not a proof, and it is why the rerun below carries controls.

**Decision: yes, ONE new acquisition (it lifts HOLD 11 for this row only, once).** Inside it, in this order, all under the same lock ticket (`b1484-revoke-r2`):
1. **Control on main:** rd657 alone, 3 runs, on MAINP `archive-p13` (main ac39ab9f's tree). Record each result.
2. **rd657 alone, 5 runs, on `revoke-p3` (K 016ed158, tree 460e3ce2).** For these runs only, keep the child's output if the harness offers a way without editing any tracked file (an env var or a jest flag; read `__tests__/helpers/rd395-server-harness.js` first). If it offers none, say so and run without it. Never edit a test or the harness.
3. **The plain full run on `revoke-p3`**, exactly as `p-revoke` ran it.

**Push rule (all four required; otherwise no push):** (a) step 2 reads 5/5 green; (b) step 3 reads `VERDICT: PASS` 5581/337 with rd657 3/3 and `EADDRINUSE` 0; (c) the names compare and C-89 still hold at K (unchanged K, so re-print them, do not re-derive); (d) I1-I8 and the push scans run and pass as the kit says.

**If ANY rd657 run on `revoke-p3` is red (step 2 or step 3):** no push. End `STOPPED: NEEDS TUESDAY` with the counts of steps 1 and 2 and each red's cause line. If step 1 (main) is also red, say so first: then the flake is the harness's and not this branch's, and Tuesday tickets it. Do not run a third acquisition on your own.

**The first FAIL stays on the record:** keep it in STATUS as written (append-only). Your READY line for this row adds `(plain run 1 FAIL rd657 ECONNREFUSED 25122; ANSWER-6 rerun PASS)`, so Tuesday's merge body can state it. A pass on a rerun does not erase a red; it is reported beside it.

Name this file in ADDENDA READ.
