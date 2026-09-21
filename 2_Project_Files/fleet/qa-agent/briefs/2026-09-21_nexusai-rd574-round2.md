# QA Agent Invocation Brief — Datasec/NexusAI, RD-574 seam-dependent cells — THROUGH-CODE, round 2 of 2

**Written by Tuesday 2026-09-21.** Commissioned on the builder's READY FOR QA (round 2) mail of 04:45Z.

## Charter
Read `fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not
build this and you owe it nothing. **Everything below that reports what the builder says is a CLAIM.**

## 1. Target
- **Branch `rd-574-seam-cells-s74` @ `7728d692f1561fe537960efc5431940e45722cf5`** (short `7728d69`), pushed (verified at commission).
- Base **`6ec3606`** — round 1's head, which round 1's gate returned **NO-GO** on — ancestor confirmed, **exactly ONE commit** in range.
  Round 2 is a new commit on the same branch; nothing was amended or force-pushed.
- Verified at commission from the tree, not the mail: the round-2 delta is FIVE files —
  `__tests__/ai-config-aoai-save.test.js` · `__tests__/rd486-ai-test-key-forwarding.test.js` ·
  `__tests__/rd523-aoai-redirect-refused.test.js` · `__tests__/rd545-ai-test-limit-survives-ai-off.test.js` ·
  **`scripts/verify-expected-counts.json`**. Across the WHOLE branch from main `60c76d7`: **ZERO `backend/` files, and
  nothing outside `__tests__/` except that counts file.** The counts file is expected: the suite grew by the one guard
  cell round 1 asked for, and `verify-suite` says an uncommitted count update protects nobody.
- **NOT on main. Nothing merges on your word or the builder's.** No worktree is pinned — build your own from the
  object store at the sha. The repo is `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files`; its
  working checkout is elsewhere and dirty — pin to the sha, never `HEAD`, never clean or stash it.

## 2. Why THROUGH-CODE, and who is waiting
Round 1 was TIER 1 and spent that weight establishing the subject: composition, inertness, W-1, the hashes, the
seam control — all HELD and all measured. **Do not re-drive them.** Your job is the two Majors, what their repairs
disturbed, and the builder's two new claims below.
🔴 **RD-516 is blocked on this branch.** Round 1 proved RD-516 + RD-574 merge clean with all 31 cells passing, so an
RD-574 that passes here is the last thing between RD-516 and its §5 clause. **Say in your verdict what your result
means for RD-516.** Round 1's report: `…/reports/2026-09-21-rd574-6ec3606-tier1/report.md` — read it first.

## 3. F-2 — the red-proof bar round 1 set, and whether it is really met
Round 1's bar: the repair must kill **V2 (the key-release decision compares HOSTNAME only) on ≥3 cells** and **V3
(ORIGIN only) on ≥1**. Claimed: **V2 → 3 red (dPath, dScheme, dPort); V3 → 1 red (dPath)** — the same cells and
counts as base `60c76d7`, mutating `resolveAiTestCredentials` only, restored byte-identical after each (sha256
`c3b61d0b…8e5f3d73`). **Re-run both mutations yourself.** A kill count you did not reproduce is the builder's.
Then check what the counts do NOT show: that each red cell reddens for the RIGHT reason (the key released to a
different path / scheme / port), not because a fixture changed underneath it.

**dAlias was INCLUDED — judge the reason, it was delegated to the builder.** Claimed: after the stored endpoint became a
NAME, the honest counterpart of "the same machine by another name" is the address that name resolves to, so dAlias is
now `http://192.0.2.20`, the TEST-NET-1 address `RD516_HOSTS` maps the stored name to. Claimed to keep the no-dial
property (no key → the KEY rule refuses before the host policy), and to carry none of the red-proof. **Decide whether
the label is still true, and whether a cell that carries none of the proof earns its place.**

## 4. F-1 — repaired, and the claim that the method caught a second defect
Claimed fix: reserve the port, HOLD it with a throwaway listener while the server makes its own reservation so the two
cannot coincide, release before the call. **Three guards now pin the mechanism instead of a clock:** `refusing !==
first.port`; the port REFUSES before the call; ai-test's error names a CONNECTION REFUSAL, not an HTTP status.
Claimed red-proof: clean 10/10; mutant (holder removed) **10 failed in 1 second**, with the guard's message "the
refusing port 39000 IS the server's own port". **Reproduce the mutant.** Round 1 showed timing could not tell a real
refusal from the self-hit; confirm the new guards can, by the MECHANISM they assert.

🔴 **The builder says its first F-1 mutant HUNG for 6.5 minutes and exposed a second defect in its own fix:** a throw
out of `beforeAll` skipped the rest of it, `second` was never assigned, and an `afterAll` that stopped only `second`
left that boot running — jest waited on the orphan's handle instead of reporting red. Fixed: the guards stop the server
before throwing and `afterAll` reaps both boots; the mutant now reports in 1 s with 0 orphans. **This is the claim to
test hardest,** because the failure it describes makes a red look like a hang and an orphan look like a foreign seat.
Kill a guard mid-`beforeAll` and confirm: red in about a second, and ZERO surviving server processes afterwards.

## 5. Minors — confirm they are done
- **F-3:** the evidence README now says rd486's pair was flipped in place, tallies only, and cites round 1's P1 pair.
- **F-4:** recorded in both suite headers and filed as **RD-595 (Low)**, with the reason it is not removed this round
  (A4/E2/E2-happy were ported byte-identical by Kam's ruling so their authorship survives).
- **F-5:** recorded in the seam control's own procedure, with the reap commands, and the builder's own sentence that it
  cannot rule out its OFF control leaking into a later measurement of its own.

## 6. The false statements round 1 found
Round 1: the NEW-1 file comment and commit `6ec3606`'s message both said "nothing is bound". Instruction was: correct
the FILE, never amend or force-push, record the correction in the next commit. Claimed done: the file is corrected and
`7728d69`'s message records the correction. **Confirm both — and that no false statement survives in the file.**

## 7. Counts
`VERDICT: PASS — 3773/3773 across 214 suites (jest exit 0)` — one more than round 1's 3772, by the guard cell.
Per-suite: rd486 45→45 EMPTY · ai-config 9→10, diff EXACTLY the new guard cell (declared, not drift) · rd523 23→23
EMPTY · rd545 7→7 EMPTY. Reproduce the head count and the ai-config diff.

## 8. 🔴 FLOOR DISCIPLINE — CORRECTED TODAY, READ THIS VERSION, NOT ANY OLDER BRIEF'S
Every jest run through `session-tools/nexusai-lock.sh`; hold the lock once per multi-run measurement; a zero is
reportable only beside a control that fired in the same window. **The foreign-server count changed today:**
The previous wording — count processes by `ps | grep` on the server path — **OVER-REPORTS.** It matches any process
whose COMMAND LINE mentions the path, and the fleet's own QA agents run with prompts in their argv that contain it.
The builder measured it at one instant: **naive matcher 3, actual server processes 0.** Every earlier "foreign=3" in
its red-proofs was the instrument, not the floor. It is recorded as **RD-591 comment 37901**, with the side-by-side.
**Count only processes whose EXECUTABLE is `node` and whose script argument is the server entry point** — match
the executable, never a substring of the whole command line. The old matcher errs safe but it is wrong, and a seat
that treated foreign==0 as a precondition would never run at all.
Your own prompt deliberately does not contain the server path, so the naive matcher would not count this gate — but
use the corrected one regardless. **Reap every server you start;** an orphan of yours is the next run's foreign seat.

## 9. Drivable surface — LOCAL RUN, **NOT THE DEMO** (RD-76). No demo pass for RD-574 happened; none must be recorded.

## 10. HELD
No merge, no deploy, no registry, no Partner Center, no production, no money, no external comms, no real
Azure/credential/vault/tenant/key. **Findings-only: do not commit, do not move any branch.** Stay off RD-518's cells
and the rd516 suite.

## 11. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd574-7728d69-round2/report.md`

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-574 round 2 @ 7728d69 (through-code)`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`.

This is round 2 of 2. **If you find a Major, C-62 says it is ticketed, not escalated — a third round on this class is
Kam's own call, so say so and stop rather than assuming one.** Rule 2: what you did NOT test is first-class output.
