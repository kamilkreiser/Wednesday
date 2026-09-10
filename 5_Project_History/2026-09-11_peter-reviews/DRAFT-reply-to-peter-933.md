# DRAFT — reply to Peter on PR #933 (KS-687, Akto slot isolation). **KAM SENDS THIS. Not sent by any agent.**

Review at head `4a5e7b9c6`, 2026-09-11 07:32–08:05 AEST. Nothing approved, commented or touched on the PR.

---

Peter — reviewed #933. **One blocker, and it isn't a flaw in your reasoning — it's a CI topology your guard was never run against.** The rest holds up very well.

**The blocker.** Your new slot-coherence refusal fires on the CI `Akto suite (PR)` job's own configuration. That job runs the platform on slot-4 ports (`SECUURA_API_URL=http://localhost:7182`) beside Akto's default slot-1 side-stack (`:9091`) — exactly the cross-slot shape your gate-run finding #2 says to refuse. So on #933 the job dies at `Boot Akto stack`, the BOLA/BFLA/Broken-Auth scan step is skipped, and the gate is red — on six of the branch's CI'd heads since 10:40Z. After merge it would do the same on every PR, and CI's only Akto scan would stop running. The same job boots and scans green on develop and on three other branches with identical env, and `Stack slot mismatch` exists only in your `slot.ts`. We reproduced the refusal offline from CI's values with two controls that come back coherent.

Port arithmetic can't tell "four stacks on one machine" from "one stack on a CI runner", and you deliberately left no override — which we agree with. So the job has to move, not the guard. Two shapes, your call:

- **A — slot the CI Akto job at 4** (`SECUURA_STACK_SLOT=4` and source `slot-target.sh` before `npm run start`). The config side checks out. Cost: 15 lines in the same job's diagnostics hardcode slot-1 container names (`docker exec akto-testing`, `akto-mongo`, `docker logs akto-dashboard`…) and would address containers that don't exist — outside your 6f2 gate's corpus, so it can't see them.
- **B — put that job's platform on slot-1 ports** (`GATEWAY_PORT 6882` and siblings). Its own header comment already says the target is `:6882`; nothing records why its env chose `7182`.

Either way, one `Akto suite (PR)` CI run proves boot and scan.

**Merge order stays #896 → #933, with one conflict you didn't name.** Both append to the same `for t in …; do` presence list in `Blockchain/Dev/scripts/check-stack-safety.sh` (#896 adds two `$REPO/systemTest/__tests__/…` paths, #933 adds `$ROOT/scripts/__tests__/check_akto_container_names.test.sh`). Mechanical: keep all three, one `; do`, then re-run the shell suites. Everything else between the two merges clean.

**No local platform suite is needed.** Akto needs the one CI run after the fix. Schemathesis, Playwright and k6 don't — and CI's green Schemathesis and k6 smoke are hollow for this PR: both printed that no manifest was published, so neither reached the readers you changed.

**Your tests bite.** We reproduced every baseline exactly (699, 191, 17, 69, 9) and reverted 16 guards — each went red on an assertion, at the count we wrote down first, and restored clean. Where our counts are larger than your table (the coherence call, the scan-target rewrite, the leak check) it's because we ran whole packages rather than the named files; the extra reds are named and none is a defect.

**Three of your premises don't hold as written — none changes the verdict:**
1. **#732 isn't redundant — it's the fix.** It merged on 2026-08-27 as `993246f9b`, an ancestor of your audited base, so F1 was fixed *by* #732 and there is nothing to close. `git blame` names `993246f9b`, not `0077f28b7`.
2. **"The only open PR touching `systemTest/akto/`"** was true when you wrote it, but #900 added `scanOptions.ts` and its test about an hour later, with different blobs from yours.
3. **"Nothing regresses until #896 lands"** isn't quite so. Merged before #896, Schemathesis on slots 2–4 moves from "whatever `actors.json` holds" to the seeded accounts — a change, not a regression. And on slot 1 the k6 overlay fix takes effect the moment #933 merges. Harmless in your intended order.

**A few small ones, take or leave:** six exit-2 cells in the 6f2 gate's suite pass against a gate that can't parse (asserting the refusal text alongside exit 2 fixes it) · the `slot_target` "drops a pinned `SECUURA_ARTIFACT_LABEL`" cell cannot fail under `env -i` (same on #896) · a wiring cell's "after persisting" half is satisfied by a JSDoc example · the CI Akto job's header comment still says `:6882`.

We have not approved, commented on or touched the PR.

---

## Notes for Kam — NOT part of the message

- **Evidence class of the blocker.** **Verified by Wednesday at source:** the #933 head job's `Boot Akto stack` step = failure and its scan step = skipped, while develop's same job has both = success; `Stack slot mismatch` occurs in `slot.ts` at head, and `slot.ts` does not exist on develop. **Relayed from s173, not re-read by Wednesday:** the CI log line itself (the log download 401'd from here), the offline reproduction, the 16-row bite table, and the premise checks.
- **This is why #933 cannot be approved yet** — merging it switches off CI's Akto scan for everyone.
- **Separately, two corrections to Peter's triage document** (ride with this message or go alone): #813's approval was **withdrawn** in his own 14:56Z review, but his triage lists it as approved-at-head; and #900 is listed as merged but is **open**, stacked on #899.
- **Cut the "small ones" paragraph** if you'd rather not hand him work while he waits on us.
