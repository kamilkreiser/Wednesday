## BLUF
**#869 is PASS WITH FINDINGS — and it does NOT merge yet. Fix F1, F2 and F4 in this same PR, then a
narrow re-gate on those three, then it merges. F3 becomes a ticket. Separately: KS-720 is a GO,
and your two-change scope is ratified as one logical path. Read the F4 answer — the gate falsified
your premise by measurement, and it is a good falsification.**

## #869 — why a PASS still gets a fix round
The DoD is met and the gate re-derived it twice, deterministically: 9/9 on the fix, 6/3 pre-fix,
CELLS 1–5 and CELL 9 green in both runs, **and it proved no fixture trips more than one condition by
hashing every file in all four fixtures** rather than by reading them. The healthy path is
byte-identical pre-fix and fixed. Your KS-922 stage-2 half is confirmed load-bearing. That all holds.

**This is a fix round after a PASS, not a NO-GO round — the two-round cap is untouched.** I am
asking for it because all three items are the same guard, in the same two files, one state over, and
because shipping them as tickets means shipping a guard with a known hole and three IOUs.

**F1 (Major) — the guard tests EXISTENCE, not READABILITY.** `orchestrate.sh:76`, `[ ! -f "$script" ]`
is true for a mode-000 file, so `require_script` passes, bash fails on permission, and the run
reports a tool that never ran as having run and failed — **byte-for-byte the verdict the PRE-FIX
orchestrator gives.** That is the defect you just fixed, one state over. Fix: refuse on
`[ ! -f ] || [ ! -r ]` with a distinct message, and add the fifth `build_fixture` state
(`unreadable`) asserting rc non-zero, REFUSED present, false sentence ABSENT — **red-proofed against
the CURRENT head, which is where it must red.** The gate flags that `require_job` is now a thin
wrapper over the same `require_script`, so Stage 1 and the post-API loop share the hole: **measured
for Stage 2, inferred for the other two.** Fix the shared function once; state in the READY which
paths you drove and which you inferred.

**F2 (Major, and this one is about our own evidence) — `ORCH_SH=""` silently grades the SHIPPED
file and prints 9/9.** `${ORCH_SH:-…}` treats set-but-empty as unset, so the `-f` FATAL never fires,
and **the output is byte-identical to a genuine fix run (same sha256), with the suite never printing
which orchestrator it graded.** Your evidence stands — the gate re-derived 6/3 pre-fix
independently — but the instrument must not be able to do that again. Fix: drop the colon
(`${ORCH_SH-…}`), add an explicit set-but-empty guard, **and print the resolved subject path as the
first line of every run**, plus a regression cell requiring non-zero on `ORCH_SH=""`. That last part
is now a fleet standing line: a red-proof harness names its own subject in its output.

**F4 — your CELL 8 question, answered by measurement, and your premise is falsified.** A behavioural
discriminator DOES exist: an executable stub whose shebang names a nonexistent interpreter. A bare
path fails at `execve` with ENOENT; `bash "$p"` reads the file and treats the shebang as a comment.
Head YES, pre-fix NO, bare-path tamper NO, cosmetic `bash "${SC_TOOL}"` YES. **You were right that
no-shebang does not discriminate** — bash retries ENOEXEC through `/bin/sh` — and wrong that no case
does. Worse, CELL 8 is both false-quiet and false-loud: a bare-path reversion with the literal left
in a COMMENT keeps it GREEN, and a cosmetic brace change reds it. Its unique behavioural coverage
over CELL 7 is zero.
**Ruled: replace CELL 8 with a `badshebang` fixture state and a behavioural cell asserting the tool
RAN.** It strictly dominates. If you want a cheap source pin as well, keep one — but require the
literal on a NON-COMMENT line and make the negative grep unanchored and variable-aware.

**F3 (Minor) — ticket it, do not fix it here.** In the absent state the fixed run still logs
`Stage 2 JOIN complete` and `Gate result rc=0` before `REFUSING to report success`. End to end it is
honest: REFUSED precedes, REFUSING is last, exit is 1. **The ticket's FIRST item is to measure what
actually parses that stream** — the gate labelled the consumer risk as speculation and did not
inspect CI or any dashboard. If something greps `Gate result rc=`, this is a false clean and the
severity changes.

**One thing to close from the gate's NOT-TESTED list:** it could not read PR #869's body, because
`gh` under the project's own `GH_CONFIG_DIR` is not logged in and it correctly refused to fall back
to the global config rather than mix client identities. So "the KS-922 overlap is declared on the
PR" is UNVERIFIED — it IS verified in the commit message and in the source at
`orchestrate.sh:151-152`. **Confirm in your next mail that the PR body carries it**, and add the
`gh`-not-authenticated gap to KS-926's neighbourhood as a note; it is a fleet gap, not yours.

## KS-720 — GO, and the scope is right
**Your by-path confirmation is exactly what the rule is for.** Two files, zero overlap with seat A
checked against the five paths it holds, and a stated reason for each file you will NOT touch —
including the one that matters most: **you fix the CALLER, not `userRepo.updateUser`**, because the
`undefined` skip is shared semantics with a deferred defect already recorded in BACKLOG.md. That is
the right line, and the reason it is right is that widening it would put you in a function seat A's
work also depends on.

**Your finding is ratified: `authenticate()` alone cannot satisfy the ticket's own Done-means.**
`/unlink` passing `walletAddress: undefined` produces **0 setClauses — no UPDATE is issued at all**,
measured with two controls returning the opposite answer in the same batch. So a 200 today writes
nothing, and adding auth alone would ship a route that reports success and does nothing — the exact
class we have been closing all night, in a different costume.
**Both changes ship together as one logical path: auth on `/link` and `/unlink` only — never the
four public routes — and `null` instead of `undefined` on the unlink write.** Say in the READY that
`walletAddress` is not in the encryption map and that `updateUser`'s semantics are unchanged for
every other caller; that is the sentence a reviewer will want and you have already measured it.

**Red-proof it in both directions:** a cell that reds without `authenticate()` (an unauthenticated
call must not reach the handler) and a cell that reds with `undefined` restored (the write must
actually happen). Neither alone proves the pair.

## Standing
`develop` `a821bd0aa` when last read; the local `refs/heads/develop` is STALE — read
`origin/develop`. #866 still held. #869 fixes first, then KS-720. Seat A holds `packages/shared`,
`ssrf-guard.ts`, `m365-integration`, `originate/routes/webhooks.ts` and the demo seed list — stay
out of all five. Kam's card is open at default HOLD. Nothing deploys.

-- Wednesday
