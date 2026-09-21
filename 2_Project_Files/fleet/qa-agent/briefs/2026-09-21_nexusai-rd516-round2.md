# GATE — RD-516 FIX ROUND (round 2 of 2), branch `rd-516-ai-test-ssrf-s73` @ `aaffbb9` (full: aaffbb91a993e23bf06f27e93ea078c3f7879c30)

**TIER: THROUGH-CODE, NOT A TIER-1 RE-RUN. The scope below is the whole scope and it is deliberately narrow.**

Report to write: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd516-aaffbb9-round2/report.md`
Verdict mail to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-516 round 2 @ aaffbb9 (through-code)`

# WHY THIS IS THROUGH-CODE AND NOT TIER-1 — read before you widen it yourself

**The tier-1 gate on this branch already ran at `f4264e5` and returned: security property CLOSED AND
PROVED, branch NOT CLEARED TO MERGE.** This round fixed that gate's findings. **Its functional delta
is THREE IPv6 AUDIT-REASON STRINGS on a refusal path** — the seat measured refusal, status and body as
unchanged on all eight probed inputs. Everything else it touched is comments, a docs table, and two
deleted fixture files.

**Per C-62's tiering, an already-gated follow-up gets through-code weight.** 🔴 **So you do NOT re-run
the proved batteries.** Naming them so there is no ambiguity:
- **the 26 refusal classes** — proved, anchored by a positive control re-run last as well as first;
- **the absence clause** (adapter diff `60c76d7..HEAD` empty; no `dispatcher`/`ProxyAgent`/`undici`/`axios`);
- **the 105/105-on-main control.**
⚠️ **The 105/105 figure carries a known caveat — it was ONE run on a contended floor. Do not quote it
as a repeatable constant and do not re-run it here; a clean replacement is owed separately.**

**If you believe the delta justifies tier-1 after all, STOP and mail Tuesday with the reason. Do not
silently widen.**

# WHAT YOU ARE VERIFYING — six items, an account, and two instruments

## A. THE SIX COMMISSIONED ITEMS, at source on the branch

1. **F-1's false header is gone.** The module previously claimed ai-config's Azure branch calls it
   *"so (C-54) holds BY CONSTRUCTION"*. Verify the header now states: single definition **for
   ai-test**; `checkEndpointName` exported for ai-config **to adopt and not yet adopted**; C-41's ONE
   PLACE **not** achieved; the mirror clause false in both directions and untested. **Line 177 must
   say `can`, not `does`.** ⚠️ **And verify the claim it replaced is actually false**: `checkEndpointName`
   should have **zero external callers** and ai-config should still run its own inline regex.
2. **RD-588 exists** and covers ai-config wiring + the Gov `cognitiveservices.azure.us` save defect
   (TEST succeeds, SAVE never can) + ONE PLACE unachieved. **It must NOT be written as a security
   regression.** ⚠️ **Check that framing — overstating it is the defect here, not understating it.**
3. **F-2 is fix B: stripped ONCE into a local, used for BOTH the `net.isIP` test and the
   `addressClass` call.** 🔴 **Two independent `.replace()` calls is a FAIL** — the original defect was
   precisely that the second use did not get the fix.
4. **RD-589 exists** for the IPv4-mapped residue, naming the `new URL()` hex-canonicalisation cause.
5. **§4's mutation table is de-trapped**: M-R12 reddens **three** cells (R12, R12-provenance, R10ii);
   **M-R8 is marked INVERTED TODAY** with the reason (R8 already red for RD-541, so deleting a mount
   takes it red→GREEN and applying it as a redden-check yields a confident wrong answer).
6. **§8 classifies NEW-1**: in the set making it 28; `RD516_HOSTS` only; the suite spawns its own
   server so the preload wires as `-r`.

## B. THE F-2 TABLE — REPRODUCE IT, DO NOT READ IT

The seat reports eight inputs, before `f4264e5` and after `aaffbb9`. **Re-drive them yourself.**

    http://[::1]/                  expect ADDRESS_LOOPBACK
    http://[fc00::1]/              expect ADDRESS_RESERVED
    http://[fe80::1]/              expect ADDRESS_LINK_LOCAL_METADATA
    http://[::ffff:192.168.8.37]/  expect HOST_NOT_ON_SOURCED_LIST   <- STILL WRONG, EXPECTED, RD-589
    http://[2001:db8::1]/          expect HOST_NOT_ON_SOURCED_LIST   <- CORRECT, MUST NOT MOVE
    http://127.0.0.1/              expect ADDRESS_LOOPBACK
    http://169.254.169.254/        expect ADDRESS_LINK_LOCAL_METADATA
    https://x.openai.azure.com/    expect ALLOWED

🔴 **THE ACCEPTANCE IS NOT THE REASON STRING — IT IS THAT REFUSAL DID NOT MOVE.** For every refused
row, assert the response **body is byte-identical to `REFUSAL_BODY`** and zero dials occur. **A
changed audit reason with an unchanged refusal is the fix; a changed refusal is a FAIL even if the
reason looks better.**
⚠️ **Row 5 moving is a REGRESSION, not an improvement.** A public literal that is genuinely not on the
sourced list must keep refusing for that reason.

## C. THE 33-FAILURE ACCOUNT — verify it is complete, with no residue

`npm run verify -- --maxWorkers=2` (RD-561: the worker argument is mandatory). **Expect
`VERDICT: FAIL`** — that is the CORRECT state of this branch.

    10  rd464-aoai-health-routes        seam-dependent
     8  rd486-ai-test-key-forwarding    seam-dependent
     7  rd523-aoai-redirect-refused     seam-dependent (fixtures dropped)
     5  rd545-ai-test-limit-survives    seam-dependent (fixtures dropped)
     1  ai-config-aoai-save             NEW-1, seam-dependent
     2  rd516-ai-test-ssrf              R7 + R8, DELIBERATE
    ---
    33

🔴 **A 34th failure, or any failure outside these six suites, is a FINDING.** In particular
**`rd554-restore-r3-conjunction` must PASS** — it failed on a contended floor in round 1 and passed on
a quiet one, and if it fails for you that changes its classification entirely. **Stop and mail
Tuesday rather than recording it.**

⚠️ **`rd516-ai-test-ssrf.test.js` must read 28 passed / 2 failed / 1 skipped** — identical to the
pre-change baseline. That suite holds the security property and the seat did not touch it. **A
different number there is the most serious thing you could find.**

## D. 🔴 THE TWO INSTRUMENTS THE VERDICT RESTS ON — AUDIT THESE, THEY ARE NOT DECORATION

**D1. THE FLOOR CERTIFICATE.** This branch's verdict was taken on a shared machine where **two seats
each reached a confident wrong conclusion this morning from cross-seat test contamination.** The seat
built `evidence-s75b-rd516-fix/floor-watch.sh` to certify its runs.

🔴 **Its FIRST version matched the bare string `jest` and flagged a COMMIT MESSAGE as a foreign
process.** The seat found and reported this itself. **Verify the shipped version is the fixed one:**
- **the log's first two lines must carry a PASSING positive AND negative control** — a commit message
  containing "jest" NOT flagged, a real foreign jest invocation flagged;
- **it must detect by process, NEVER by `EADDRINUSE`** (RD-533: a second server that never listens
  raises no bind error);
- **if either control is absent or failing, every QUIET verdict in this round is unsupported** and
  that is your finding.

**D2. THE HEAD EQUIVALENCE.** The READY named `6ad0e2f`; the head is `aaffbb9`. **Verify
`git diff --name-only 6ad0e2f..aaffbb9` is `HISTORY.md` ONLY**, and run a control diff
(`f4264e5..6ad0e2f`) proving the command would show code if there were any. **Tuesday verified this;
verify it independently, do not inherit it.**

## E. THE CLARIFICATIONS CHAIN

**C-54 must be UNTOUCHED — it is the RESUBMISSION CHECKLIST.** C-74's mis-citation must be **recorded,
not rewritten**. **C-107** (mirror clause, with the mis-citation chain and the standing line *cite
this clause by content, never as "C-54"*) and **C-108** (the IPv6 rule) must exist.
⚠️ `1_Project_Definition/CLARIFICATIONS.md` is outside git — read it on disk.

# WHAT A GO DOES AND DOES NOT MEAN

🔴 **A GO HERE DOES NOT CLEAR THE MERGE. Say so explicitly in your verdict, in those words.**
RD-516's §5 acceptance clause requires the 28 seam-dependent cells to be **on `main`**, and they are
on a different seat's branch (RD-574), still building. **No reader may record this verdict as
clearing the merge.**

**No merge, no deploy, no real Azure. Local run at this commit only (RD-76, C-02).**

# THE FLOOR RULE APPLIES TO YOU

1. **Every jest invocation through `session-tools/nexusai-lock.sh`** — including yours.
2. **Hold the lock ONCE across a multi-run measurement.**
3. **Record the foreign `backend/server.js` count beside every result, by `ps`, never by a bind error.**
4. 🔑 **A ZERO IS ONLY REPORTABLE IF A CONTROL FIRED IN THE SAME WINDOW.** A measurement that finds
   nothing and one that never happened produce the identical output.

⚠️ **Two other seats are live on this project right now** — one on `__tests__/` for the five
seam-dependent suites, one on `backend/server.js` and `backend/encryptionService.js`. **Queue behind
them; a wait is the mechanism working, not a stall.**
