# QA Agent Invocation Brief — Datasec/NexusAI, RD-574 seam-dependent cells — TIER 1, round 1

**Written by Tuesday 2026-09-21.** Commissioned on the builder's READY FOR QA mail of 02:31Z.

## Charter
Read `fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not
build this and you owe it nothing. **Everything below that reports what the builder says is a CLAIM.**

## 1. Target
- **Branch `rd-574-seam-cells-s74` @ `6ec36065eeadb9d445d9c32c3d13826748bab651`** (short `6ec3606`), pushed (verified at commission).
- Base **`60c76d7`** (main), ancestor confirmed, **exactly 6 commits** in range.
- Verified at commission from the tree, not from the mail: **6 files changed, ALL under `__tests__/`,
  ZERO `backend/` files.** Hard stop 1 holds. The six:
  `ai-config-aoai-save` · `helpers/rd516-net-harness-preload.js` · `rd464-aoai-health-routes` ·
  `rd486-ai-test-key-forwarding` · `rd523-aoai-redirect-refused` · `rd545-ai-test-limit-survives-ai-off`.
- **NOT on main. Nothing merges on your word or the builder's.**
- **No worktree is pinned.** Build your own from the object store at the sha. The repo is
  `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files`; ⚠ its working checkout is
  elsewhere and dirty — **pin to the sha, never to `HEAD`, never clean or stash that checkout.**

## 2. Why this is TIER 1, and who is waiting on your verdict
🔴 **This branch is the acceptance clause of ANOTHER ticket.** RD-516's round-2 gate returned GO but
said explicitly that **the GO does not clear its merge**, because RD-516 §5 needs these
seam-dependent cells **on main**. So your verdict is not just about this branch: an unlanded or
wrongly-landed RD-574 is what unblocks or mis-unblocks RD-516. Say in your verdict what your result
means for that dependency.

The change is test-only, which lowers the blast radius but does **not** make it tier 2: the whole
product of this branch is *test confidence*, and a cell that is green for a weaker reason than it
claims is a defect in the thing being delivered.

## 3. THE SET IS 31, NOT 28 — verify the composition, not just the count
The original commission said 28. The builder says 31 = **27 named in the RD-516 gate brief §6 at
`f4264e5`** + **NEW-1** + **A4, E2 and E2-happy**, the last three added by a ruling of
2026-09-20T23:23:24Z (option (b)) that superseded the brief's "the three are NOT in scope".
**Check the composition against those sources.** A count that matches while the membership does not
is the failure mode here. Commit `acbe9f9` is claimed to carry the reason.

## 4. 🔴 THE CORE CLAIM: INERTNESS — and the instrument that must be able to fail
Every cell is claimed **"fixtures only, inert"**: adding them changes no existing suite's result.
The builder's evidence is per-suite before/after with **EMPTY per-cell diffs**, the BEFORE taken in
a **pristine second worktree at `60c76d7`** rather than by reverting files in place (which is the
right shape — say so if it holds).

🔴 **An empty diff is only evidence if a non-empty diff was reachable by the same instrument.**
Establish that your diff method can SEE a difference — perturb one cell deliberately and confirm the
diff goes non-empty — before you accept five EMPTYs. Round 1 of RD-518 failed on exactly this class
(its red-proof was structurally blind to the branch it claimed to test).

`rd545` and `rd523` are claimed measured TWICE — the byte-identical port alone first (`acbe9f9`),
then with the nine on top — so that the second EMPTY is attributable to the new cells and not to the
ported three. Verify that sequencing; it is the part that earns the claim.

## 5. 🔴 THE THREE THINGS THE BUILDER DECLARED AGAINST ITSELF — your first work
As with RD-518 round 2, a self-declared weakness is where the evidence stops, not a place it is
cleared. These are filed, NOT fixed, and they are the most likely place a real finding lives.

**W-1 — the 105/105 baseline was taken UNLOCKED.** The builder corrected its own earlier number:
that five-suite baseline, *which a previous reader accepted*, was measured on a contended floor and
**must not be quoted as a constant**. The suites are claimed re-measured on a quiet floor and all
hold. **Verify the re-measured numbers; do not quote 105/105.** The RD-516 gate independently said
this control "still owes a clean replacement" — two sources now agree it was never sound.

**W-2 — RD-590, and this is the one that can sink the branch.** The builder states that `rd486`'s
four `d-nomatch` cells each isolate ONE variable today, and **will also differ in HOST after this
change, so they pass for a weaker reason while staying GREEN** — and that **"inertness structurally
cannot see it."** Read that plainly: the branch's own headline property is blind to a way the branch
degrades existing cells. **Decide explicitly whether a change that silently weakens four cells may
land on the strength of an inertness argument that cannot detect the weakening.** The builder left
them untouched citing scope and hard stop 1. Scope is a reason not to FIX; it is not a reason for a
gate not to JUDGE.

**W-3 — RD-591 (High), which the builder says OUTRANKS the branch.** Test runs are not isolated
across seats. Contaminated vs quiet evidence is kept side by side in the evidence folder. Confirm
that the measurements this verdict rests on are the quiet ones, and say what RD-591 means for every
number in this report — including your own.

## 6. NEW-1 — a remedy taken on a TIMING trigger, so the timing is the evidence
The result never moved (9/9, EMPTY, every configuration). The **timing** did:
pristine main 21.222 / 21.606 s · `RD516_HOSTS` only 25.213 s (+~4 s) · HOSTS + INTERCEPT 20.602 s.
Mechanism claimed: TEST-NET-1 is unrouted, so HOSTS-only turns a fast `ECONNREFUSED` into a
blackhole costing the request's whole bound (RD-581). The pre-authorisation was conditional on the
result **or the timing** moving. **Re-measure the timing yourself** — wall time returning to baseline
is the only thing separating a remedy from a coincidence, and it is a single-sample claim as stated.
Check the stated boundaries held: only NEW-1, no listener created, `SEAM_OFF` untouched, and the
superseded HOSTS-only line named as superseded in both file and commit.

## 7. The seam was proved to engage — verify the control, not the green
A green suite does not prove the preload engaged, and the builder says so: the preload's `loaded`
line never reaches jest's output because the harness buffers child stdout. The claim rests on a
one-boot control — **intercept ON: preload loaded, stand-in got 9 calls; intercept OFF: the boot
NEVER COMPLETES**, because the name resolves to unrouted TEST-NET-1. That is the right shape
(fails loudly, not quietly reaching a real host). Reproduce it.

Zeros are claimed anchored per the floor rule: `rd545`'s K-live asserts the first test DOES reach the
model host; `rd523`'s A1-happy/A2-happy and the W1 control assert real traffic at the stored origin.
**Confirm those controls fired in the same window as the zeros beside them.**

## 8. Byte-identical ports — check the hashes, not the sentence
Claimed ported byte-identical from `f4264e5`, verified by blob hash: preload
`sha256 06386ede...85d9fc0`; `rd545` `1330be3a4127`; `rd523` `1b484c1b940a`. Re-derive them.
Superseded paragraphs in `rd545` and `rd523` are claimed KEPT and marked superseded rather than
deleted — confirm, because a silently deleted dead end is the defect RD-516 exists to punish.

## 9. Counts
`VERDICT: PASS — 3772/3772 across 214 suites (jest exit 0)`, read not inferred (RD-100),
`--maxWorkers=2` (RD-561). Reproduce the head count yourself.

## 10. Floor discipline — W-3 makes this load-bearing, not boilerplate
Every jest invocation through `session-tools/nexusai-lock.sh`. Hold the lock ONCE across a multi-run
measurement. Assert the foreign `backend/server.js` count **by `ps`, never by `EADDRINUSE`**, before
each run. **A zero is reportable only if a control fired in the same window.** Another gate may still
be finishing on this project — queueing is the mechanism working, not a stall. `bash -n` anything you
write before running it.

## 11. Drivable surface — LOCAL RUN, **NOT THE DEMO**
RD-76 stands. The builder states no demo pass for RD-574 happened and **none must be recorded**.

## 12. HELD
No merge, no deploy, no registry, no Partner Center, no production, no money, no external comms, no
real Azure/credential/vault/tenant/key. **Findings-only: do not commit, do not move any branch.**
Stay off RD-518's cells and off the rd516 suite, as the builder did.

## 13. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd574-6ec3606-tier1/report.md`

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-574 @ 6ec3606 (tier 1)`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`
— absolute path; the QA project has no `4_Credentials` of its own.

**Rule 2: what you did NOT test is first-class output.** And state what your verdict means for
RD-516's blocked merge (§2) — a later reader will come looking for exactly that.
