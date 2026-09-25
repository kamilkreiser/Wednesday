# COMMISSION — DRAFT the round-21 THIRD tier-1 batch QA gate kit "gate21T1c" over #1234 and #1239. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-25 (~17:4x AEST). A previous drafter died partway through
(`fa11cd0d-…/scratchpad/gate21T1c/`). Its mail captures were copied here, and every TEXT_SHA256 was re-verified against the live
message (40/40, `_meas/capture_verify_1.out`). Recorded here as the gate's commission; the QA agent reads it.

## The batch: TIER 1 (full gate: security/data surfaces; red proof RED at base / GREEN at head in the tester's own clone), FROZEN at two
- **#1234** KS-1127 + KS-1089 + KS-1135, head `6320a61d86b5d3fb9b693ea5fefb42050e1d2a43` (Seat L4, wrapped). Its READY FOR QA 4 (06:17:31Z) says tier 1.
- **#1239** KS-1263 "G", head `42c20e998a1a69887b8378968a8ff4f19106c24b` (Seat L1, wrapped). Kam ruled (c) with a req.db measurement condition.
  **The gate MUST run behavioural ROLLBACK cells in BOTH MULTI_TENANCY modes (on and off).**
- Wednesday read both heads with ls-remote at 16:2x AEST. The drafter re-read them: identical (`_meas/lsremote_2.out`, `predict_1.out`,
  `repin_dryrun_1.out`, and the GitHub pulls API).
- Develop at commissioning: `aa600af94d69ad59db279d32cbbd7596931a739b`. It **MOVED during drafting** to
  `d9515f4a06e0db0396a059ccd8c76b610f22a22b` (#1240 KS-789, CONTRIBUTING.md only). The kit is pinned to d9515f4a0.
- Routing: `QA/Secuura-batch1234`. The drafter PROPOSES the line `QA/Secuura-batch1234|coagent@agentmail.to|yes` and did NOT write
  inbox_routing.conf.

## Gate rules the prompt carries (from the round's precedent, gate21T1b)
1. Per-PR verdict GO / NO GO / GO WITH FINDINGS. Findings only. Round 1 of 2.
2. Worktrees from refs/pull/<n>/head. Never write the shared checkout.
3. Anchoring wording "N passed / 1 failed; threadTokenMint pre-existing (KS-562)", only where anchoring runs. Neither PR touches anchoring.
4. KS-1155 load false-red: re-run once. An assertion failure is real.
5. Reap only the gate's own login_stub.mjs (by cwd + ppid, never by name, never pid 1).
6. NO standalone run of pre_push_hook_base.test.sh or run-shell-suites.sh. #1218 is not merged: measured, 0 on develop.
7. Docker/stack: a FREE slot only, never another gate's stack; tear down what you start.
8. HOLDS: no merge, push, ticket/PR write or deploy.
9. GO string: `GO: merge #1234, #1239 batch`.
10. Record merge-bases and path-disjointness: the two PRs vs each other, and vs develop's commits since their bases.

## Deliver (drafter: no launch, mail, tap, commit, push; writes only in its work dir)
COMMISSION.md, the prompt, the launcher (`bash -n` clean), a repin-and-launch script (re-reads heads / develop / mergeable at launch, refuses on
mismatch), a controls script run both ways, a `--dry-run` of the repin script (rc 0), and README.md with the ONE launch command.
