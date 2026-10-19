# Gate brief: GATE AI1 = PR #1623 (KS-1633: certify writes its documents row before it anchors), Opus, tier 1, round 1 of 2

Commissioned by Wednesday after Seat G 11th's READY FOR GATE (09:50Z). The author's CLAIM is beside this brief: `G11_READY_0950Z.txt` (read it WHOLE). Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY (ls-remote, show, diff, cat-file, log). Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/ai1/`. Build `packages/shared` first; Prisma via `npm run generate --workspace=services/originate`. Scratch PostgreSQL on a port in 55420-55429 (TCP only; never the default unix socket, another session's server sits there), `docker/init/*` + every migration.

**Heads:** #1623 head `b7de864640032c3b118c5aaa9e4e45b777ef67af`; develop `f321e95aa9958153cfd8312223694e5e40b906b3` (Wednesday ls-remote 20:5x). Re-read both at start and before the verdict. Author predicts landing tree `ffb064f00e546835ce11c455ff9609d1e67128fe`.

**The rulings this PR implements (Wednesday's, inside commissioned KS-1633):**
- 19:4x: option (a) row first + a compensating delete of the just-written row on a production anchoring failure; every response byte-identical to today; no contract change.
- 20:3x: shape 1: the provisional row carries the FAILED state; the second write happens only when the state changed; KS-1124 F4-3 reads the LAST save and pins a two-save sequence on the accepted path; F4's failed-path `saves: 1` unchanged. Kam's card `secuura-ks1124-f4-failed-anchor-shows-pending` = b (2026-09-28): a failed anchoring saves a 'failed' status so the record never shows 'pending' forever. That behaviour must still hold.

## Questions (each with its instrument; name what you did NOT run)
1. **Responses byte-identical?** For every path of the certify route (success, production anchoring failure 503, non-production failure, validation refusals, access refusals incl. KS-1557's parent check), compare status + body against develop through the real router on your scratch PG. Any difference is a blocker unless it is a body echo of a new internal id (say which).
2. **The compensating delete:** does it run inside `withTenant` (both GUCs) and is "anything but 1 row" treated as a failed compensation? Reproduce the author's `DELETE 0 outside the transaction` finding as `secuura_app` with a positive control. The `verifiable_credentials.document_id` ON DELETE NO ACTION path: can a freshly-written certification have a credential before the compensation runs? If yes, what happens to the row and the response?
3. **Orphan anchors closed?** With an anchoring stub that persists before answering (verify SETUP asserts it), every failure between the anchor POST and the end of the route: is any anchor_store row left naming no document? Also the reverse: is any documents row left with no anchor where today there would be none?
4. **Kam's (b) still true:** a failed anchoring leaves the STORED row 'failed', never 'pending-onchain', on both routes (certifications.ts around :470 and :1205 at the base; re-locate at the head). The crash window: reason from the code which state the row holds at each point between the two writes; you cannot kill a process mid-request unless you can, so say which.
5. **F4-3 and the save counts:** read the F4-3 diff (old/new) and confirm it fails on a single-write regression (plant one). Confirm F4-2 and the five save-count files (205 cells) pass unchanged.
6. **Ordering pin (N2 of gate AE1):** plant the access-before-cycle reorder mutant (it must compile) and confirm the pin reds it.
7. **Red-first, mutants, landing:** the new suite 6/6 both modes (claim) and red-first 3/6 vs develop's product; one mutant of your own on the compensation; merge-tree on LIVE develop; originate full unit suite on the landing tree (claim 1506); tsc for product AND a check that type-checks the test files (the author flags that `tsc -p services/originate` excludes `src/__tests__`); the three-dot list = the PR's 6 files. List every touched service's integration suites as RUN or NOT tested.

**Verdict file:** `verdict.md` in this folder.
- First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head b7de86464003... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`.
- Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:** findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`, no push. No `cd`, no `rm`, no stderr to /dev/null, no Docker. Every zero gets a positive control. The shell is zsh: no PIPESTATUS.
