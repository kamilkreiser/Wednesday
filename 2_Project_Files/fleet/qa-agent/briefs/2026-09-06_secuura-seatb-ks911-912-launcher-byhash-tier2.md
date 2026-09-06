# QA Agent Invocation Brief — Secuura / Blockchain, SEAT B: KS-911 + KS-912, BY HASH

**Charter first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
Findings only. You never fix, never file a ticket, never touch a builder's tree.

**TARGET — two files OUTSIDE git, identified BY HASH. TIER 2.**
```
SHIPPED  Launch_Claude.command         sha256 932a2cc3aebe6cf838bf885ac92eec08e259f0572c0e08910088ac58e269f55c
SHIPPED  Launch_Claude.seats.test.sh   sha256 b93b2c838e8766a8dc2b72e24d2f6fab21f9b912772e52328d43996414f18888
PRE      Launch_Claude.command.pre-ks911       9609c8453da8d7743a4b3ed2a94db6b09bef588c29f83e57b16255963a0929f1
PRE      Launch_Claude.seats.test.sh.pre-ks912 a5d5d9ef8bd3e1039e3ee89b6334356644939f91b76c5002fef41e0dca554901
TAMPER   Launch_Claude.command.KS912-TAMPER-noprune.parked
                                       21a1ec04f7bc2e89f96475df42c4cb22c0292e0cb92539150e3f734656ec6ced
```
All at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/`. 23 changed lines in the launcher, 75 in the
suite; modes unchanged.

**WHY THIS GATE IS URGENT rather than routine: this change is LIVE ON DISK.** The launcher is not in
git; the next boot of either Secuura seat reads whatever is on disk now. **I am holding all Secuura
relaunches until this verdict**, so a seat is idle while you work. Restore, if it comes to that, is
one `cp` from each `.pre-` copy — **but you do not do that: you are findings-only, and that file is
the project's, not ours.**

## 2. Spec / DoD
Five findings from the KS-907 gate, fixed as one by-hash change, **F-04 first as ruled**: the cell
KS-912 says *"never asserts the pruning it is named for"*. The builder's own red-proof is the claim
to re-derive: with a parked tamper making the prune write-back a no-op (2 changed lines), the OLD
cell **passes on a launcher that does not prune** while the new one fails.

## 3. Scope — claims to measure
1. **The `.pre-` hashes equal KS-907's gated figures exactly.** That is the chain that makes "no
   in-place edit" checkable rather than promised: the baseline edited IS the file that passed that
   gate, with no drift between. **Verify both, and verify the shipped hashes match the files on disk
   right now** — this target is a hash, not a ref, so a file that changed under us invalidates the
   whole gate.
2. **F-04's red-proof:** against the parked tamper (`21a1ec04…`), the run is claimed as
   `17 passed / 1 failed` with the OLD cell green and the NEW one red —
   *"…and the DEAD pid is GONE from the registry"*. **Re-derive it.** The pairing to check is that
   CASE 1 asserts a LIVE pid is still IN the registry while CASE 2 asserts a DEAD pid has LEFT it —
   presence and absence in the same batch, so neither passes because the launcher always clears or
   always keeps.
3. **F2's fixture correction, which is the subtle one.** The unwritable-DIRECTORY fixture reaches
   only ONE of the two sites the ticket names, because the truncate sits inside `if [ -f "$SEAT_FILE" ]`
   and the file cannot exist when its directory does not. The regression cell therefore uses a
   read-only FILE, which reaches both. **Verify both sites are reached**, and that in every fixture
   the launcher still exits 0 and still emits its `DRY_RUN` markers — that is the control that makes
   an empty stderr mean something.
4. **HUNT — CASE 6 changes `TMPDIR` for the launcher process**, which is how it makes the registry
   unwritable without permissions games. The builder judged the blast radius nil (the launcher uses
   `TMPDIR` only for the seat registry) and **said plainly it did not prove that exhaustively.**
   **This is the assumption to press.** Name the assertion first: is there any other `TMPDIR`
   consumer in the launcher's path, and does the cell therefore exercise a launcher no real boot
   would produce?
5. **F3's counter:** `LAUNCH_RUNS` is incremented inside `run_launcher` so it cannot drift from the
   call sites; the suite prints 8. **The builder's own grep returned 9 and one of the nine is a
   COMMENT** — it caught that before publishing. Re-derive the 8 with an instrument that excludes
   comments, and say which you used.
6. **F6 and F1:** `grep -qc … ; echo $?` printed an exit status where a count was implied, now
   `grep -q … && echo YES || echo NO`, A/B'd with an absent string as the control. And F1 is a
   JUDGEMENT, not a measurement — the builder deleted a sentinel's CLAIM and kept the `END` marker
   as a plain lowercase comment, reasoning that a marker saying where something ends is navigation
   while a marker claiming a property is a contract. **I agreed. If you read the survivor as still
   sentinel-shaped, say so** — that is a judgement call you are entitled to differ on.
7. **Side effects, which matter more here than usual because this file boots real seats.** The
   builder reports `2_Project_Files/.git/config` byte-identical (`75c96972…`) after all 8 launcher
   runs, and `.launch_preflight_last.txt` restored byte-identical from its own backup rather than
   trusting the suite's EXIT trap. **Re-derive both.** It also verified the launcher issues no
   `pull`, `fetch`, `checkout` or `reset` against the project repo — only `git config` writes.
   **Check that enumeration yourself; it is the sentence that makes this file safe to run at all.**
8. **The registry side effect it disclosed:** the suite's runs overwrite the seat registry, so a live
   entry is replaced by the last dry-run's dead pid. Self-healing at the next launch (that is CASE 2)
   and the process scan finds the session regardless. **Confirm it is self-healing rather than
   merely claimed to be.**
9. **HUNT — what does a BOOT on this file do that the suite does not exercise?** The suite is
   dry-run. Name the assertion first, then say what a real boot reaches that no cell covers. **You
   are not to perform a real boot** — the seats are live and one is mid-session.

## 4. Credentials
Pointer only. You need none. **Never launch a real seat.**

## 5. State-mutation & cleanup
Your own copies in `mktemp`. **Never modify the launcher, the suite, or either `.pre-` copy in
place** — copy them out and work on the copies. Never touch seat A's tree (`2_Project_Files`, live)
or seat B's worktree. No demo VM, no shared stack, no Docker, no prune. Quarantine by rename, never
delete; the parked tamper stays parked. **A tamper does not count until its subject's hash is shown
to have changed.** Report the LISTEN set before and after.

## 6. Output boundary
Findings only, one verdict, evidence class on every finding, NOT-TESTED at the same prominence.
**Say explicitly whether the shipped hashes still match the files on disk at the END of your pass** —
if they moved, the verdict is void and I need to know that first.

## 7. Known-fragile / known-changed
- **An instrument is not evidence until it has produced the other answer in the same batch.**
- **A cell that cannot tell the fix from its own fallback is not a regression test** — assert WHICH
  mechanism judged the case, not that some mechanism did.
- **A count taken from the wrong population, reported with confidence**, is this ticket's own class:
  the builder's 9-vs-8 near-miss was exactly that.
- `env bash` 3.2; `/bin/dash` present; `core.fileMode` false; darwin only.

## 8. Logistics
Report to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Secuura SEAT B KS-911 + KS-912 (launcher, by hash)`, verdict in the first line.
Budget ~25 minutes — a seat is idle behind this.

PROVENANCE:
- the five hashes, the 23/75 changed lines, the F-04 red-proof, the F2 fixture correction, the 9-vs-8 near-miss and the CASE 6 / F1 caveats | the builder's READY mail 2026-09-06T11:16:20Z, read whole | read 2026-09-06 21:2x
- the ruling that F-04 goes first and the change ships BY HASH with a new `.pre-` copy and three hashes in the READY | Wednesday's mails to the builder 2026-09-06 21:07 and 21:47, sent through the gate | read 2026-09-06 21:4x
- that the change is live on disk and ungated, and that Wednesday is holding relaunches on it | Wednesday's own handover block, /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md - my project, not yours | read 2026-09-06 22:1x
- NOT READ by me: the launcher diff itself — I have read only the builder's description of it | not read | read 2026-09-06
