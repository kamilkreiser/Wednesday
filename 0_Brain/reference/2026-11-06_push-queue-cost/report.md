# Secuura/Blockchain push cost, measured read-only (2026-11-06, drafted ~02:10Z for Wednesday)

## BLUF
- One leg owns the push: **leg 14 of 16, the shell-suite run, is 90-92% of every measured push** (948 of 1033 s, 990 of 1096 s, 1102 of 1213 s). It runs 116 suites one after another, always whole, whatever paths changed.
- The **entire hook runs inside the lock**: the driver takes the lock, then calls `git push`, and git runs the hook. The lock protects the seat ref-layer protocol and the develop-overlap judgement, and keeps the machine to one hook. Leg 14 reads only its own worktree. So the expensive legs do not need the lock.
- A test-only push is **not** cheaper. The hook scopes on `^Blockchain/Dev/`, and test files live there. Only a push with nothing under `Blockchain/Dev/` skips the preflight, and no push on this floor today is of that kind.
- Machine load: UNMEASURED during the runs. Start-of-push load1 5.45-6.22 gave 948-1102 s with no ordering by load. One live push started at load1 10.43 projects to about 945 s. That is weak evidence that load 6 versus 10 is not the main driver.
- Recommendation: **option C**, run the full preflight on the tip BEFORE taking the lock, in parallel with a cap, then push under the lock. It is the only option that reaches the 14 branches already built. It needs Kam, because the push step then uses `--no-verify`. Detail and cheaper follow-ups below.

## 1. Per-leg wall clock
The hook prints a time for ONE thing only: `shell suites wall-clock: Ns` (leg 14), `preflight.sh:747-751`. No other leg is timed. Per-leg figures for legs 1-13, 15, 16 are therefore UNMEASURED; only their sum is derivable.

Sources (all under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/`): G = `2026-11-06_seatG-28th/evidence/push_ks1377/`, E1 = `2026-11-06_seatE-38th/evidence/push_ks1128/`, E2 = `.../push_ks864/`, E3 = `.../push_ks1841/` (in flight). Each holds `status.txt` (driver stamps) and `push.out` (hook output).

| Push | Total (`PUSH end ... elapsed=`, status.txt) | Leg 14 (`push.out`) | Leg 14 share | Rest (total - leg 14) | load1 at gate (status.txt) |
|---|---|---|---|---|---|
| G ks1377 | 1033 s | 948 s (push.out:3600) | 91.8% | 85 s | 5.85 |
| E1 ks1128 | 1096 s | 990 s (push.out:3601) | 90.3% | 106 s | 5.45 |
| E2 ks864 | 1213 s | 1102 s (push.out:3601) | 90.9% | 111 s | 6.22 |
| T ks1622 | 1144 s (`seatT-13th/HANDOVER.md:20`) | not read | n/a | n/a | n/a |
| E3 ks1841 | in flight | 89 of 116 suite headers at 02:09:02Z, 725 s after `PUSH start` 01:56:57Z | n/a | n/a | 10.43 |

- Seat T's 1165 s figure comes from the brief only. No file I read carries it; T's 1144 s is in HANDOVER.md. So 4 completed pushes (3 with per-leg data) plus 1 in flight. That is 5 real pushes, 3 with legs.
- "Rest" (85-111 s, mean 101 s) holds: the hook's pre-steps (ref judgement, format gate), legs 1-13, 15, 16, and the git upload. Not separable. Leg 2 (35 `npm ci --dry-run`), legs 6 and 7 (npm audit, registry) and leg 16 (tsc over 5 services) are the plausible weights. UNMEASURED; closing it needs a timestamp per `step()` in `preflight.sh`.
- Leg 14 in detail: `run-shell-suites.sh` loops `for rel in "${reached[@]}"` with `bash suite & wait`, so strictly **sequential**. Suite output is buffered and printed after. 116 suites (92 under `Blockchain/Dev/scripts/__tests__` + 24 under `systemTest/__tests__`, counted by ls; G's `push.out:3599` says 116 passed of 116). Mean 8.2 s per suite. Only two self-time: KS-1401 at 16/19/18 s and the hook-behaviour suite at 10/12/17 s (push.out:1085, 1266 in G/E1/E2). Together about 3% of leg 14; no single suite dominates, the cost is spread. Per-suite times are UNMEASURED; closing it needs a `date` stamp around each suite in the loop.
- Context: `preflight.sh:625` records 10 suites at 38-39 s on 2026-09-04. Now 116 suites at 948-1102 s.
- **Waiting on machine load vs the leg's own work: UNMEASURED.** What exists: load1 sampled once, at the gate, before the push (status.txt). Spread 154 s in leg 14 across loads 5.45-6.22 is not explained by that load. E3 at load1 10.43 is on pace for about 945 s (725 s / 89 suites x 116, assuming equal suite weight, which is not true, so treat as a hint). Closing: sample load1 every 30 s during a push, and time one leg-14 run on an idle box.
- Zero control: the driver's "waited 0 polls" for the pgrep gate is a real recorded zero in all four status files (`gate ok: no pre-push hook running (waited 0 polls)`); the grep for it matched, so the zero is a reading, not a miss.

Dead time under the lock that is not the hook: G, E1, E2, E3 spent 12, 11, 11, 10 s between `ACQUIRED` and `PUSH start` (status.txt: a fetch of develop, ls-remote, the develop gate, the overlap gate against 26 open PRs, load check). Post-push ls-remote about 3 s. Lock handoff G to E2: 00:38:33 release, 00:38:36 turn, 3 s. The queue itself wastes almost nothing.

Throughput check: G acquired 00:21:05, E3 acquired 01:56:47 = 5742 s for 5 pushes (G, E2, T, E1, T) = about 1148 s each. 14 queued x 1148 s = 4.5 h, against the 3.5 h in the brief (that figure matches about 900 s a push). The live queue file listing at 02:04:39Z (last status line of R's ks1136) showed 17 live tickets including the holder.

## 2. What the lock protects
Read: `pushlock_t13_newbranch_v3.sh` (in `seatT-13th/tools/`), `launch_driver_t13.py`, `.githooks/pre-push`, STANDING_LINES lines 519 and 540, learning 2026-09-09 lines 82-87.
- Sequence in the driver: precheck, join queue (`push_queue.sh`), wait for turn, `mkdir` the lock, check no `pre-push` hook running (anchored pgrep), load1 < 16, precheck again, **`git push`** (hook runs inside it), ls-remote, release. The hook is invoked by git from within the push, so **the whole hook is inside the lock**.
- Named shared resources (from the sources, not from a test I ran):
  1. **The ref layer of the shared checkout.** Learning 2026-09-09 line 82: each seat's push protocol snapshots every ref and worktree HEAD, and another seat's ref write reads as a foreign diff; line 87 is the standing block, "the other seat makes NO ref write while it is held". The v3 driver itself does not snapshot refs; the snapshot is in the seat's own protocol around it.
  2. **The develop-overlap judgement.** `overlap_gate.sh` and `develop_gate.sh` re-run immediately before the push; the result is only valid while no sibling push or merge lands in between.
  3. **CPU.** STANDING_LINES 519: load1 < 16 and no other hook running. Hook fixtures run the hook again against throwaway repos, which is why the pgrep pattern names the GitHub remote.
  4. **Fairness.** `push_queue.sh` (STANDING_LINES 540) exists because a bare mkdir lock lost handoffs; it orders, it does not protect.
- Do the expensive legs need item 1 or 2? Leg 14 and the other legs read the pushing worktree (its tracked scripts, its `node_modules`) and run fixtures in TMPDIR with `GIT_*` cleared (`run-shell-suites.sh`). I found no ref or lock read in legs 1-16. UNMEASURED: fixed ports, shared postgres sockets or shared `/tmp` names across concurrent runs. Closing: run two preflights at once in two scratch worktrees and compare to the sequential result.
- The hook's own pre-steps (ref judgement, KS-856 non-fast-forward refusal, format gate) read refs and belong inside the lock, but are cheap.

## 3. Which legs depend on changed paths; are test-only and docs-only cheaper?
- Scope switch is `changed=$(... | grep '^Blockchain/Dev/')` then `[ -z "$changed" ] && exit 0` (`pre-push:130, 372`). Everything under `Blockchain/Dev/` triggers **all 16 legs**, including leg 14's fixed 116 suites. No leg selects by path inside the run: leg 14 `ROOTS` are two fixed dirs, so it is "always whole".
- Outside `Blockchain/Dev/` (docs, `Projects Documents/`, vault): only the KS-989 systemTest format gate (0-2 s per touched package, per the hook header) and the ref refusal run. This is by code reading plus the hook's own suite (G `push.out:1218,1471,1490`, "the docs-only push skips the preflight"). No docs-only push was timed today: UNMEASURED. Closing: read the status.txt of any push of only `Projects Documents/` paths.
- Real test-only comparison: Seat K's ks1507 (`seatK-17th/evidence/push_ks1507/paths.txt`) is auth `__tests__` files plus docs fragments, all or mostly under `Blockchain/Dev/`, so it takes the full preflight. It is still queued (no push.out), so its elapsed is UNMEASURED. Every completed push.out (G, E1, E2, E3) prints `Blockchain/Dev changes detected` (4 of 4 hits, so the pattern works), and all four show the same 13/16 legs, 3 skipped (legs 3, 4, 8: stack down), and the same 116 suites.
- Consequence: leg 14 cost is **independent of the diff**. A one-line test edit costs the same as a service change. About 90% of the queue is identical work repeated per push.

## 4. Options
Kinds: **REMOVES** (check no longer runs), **MOVES** (same check, outside the lock), **FASTER** (same check, same place, less wall time). No option below removes a security or secrets leg; legs 6, 7 (advisories), 9 (tracked credentials) and `check_slot_credentials` inside leg 14 stay in every option.

**A. Do nothing.** Cost: about 1148 s a push, 14 pushes about 4.5 h. Weakens nothing. Decider: none. Baseline for the others.

**B. Run leg 14's suites in parallel inside the hook (FASTER).** Change: `run-shell-suites.sh` runs N suites at once, output still buffered per suite. Keeps every check. Saving UNMEASURED: 12 cores, load1 7-11, so free cores are few; per-suite single-core use is UNMEASURED. Risks: suites sharing ports, sockets or fixed `/tmp` names. **Does not reach the current queue:** the hook and `run-shell-suites.sh` run from each pushing worktree's own tracked copy, so only branches cut after the change merges get it, and the change itself must pass the queue. Decider: Secuura repo owner via a PR; Wednesday schedules.

**C. Pre-run the preflight on the tip before taking the lock (MOVES). RECOMMENDED.** Change: in the driver, run `bash preflight.sh` (via the same `slot-target.sh` source the hook uses) plus the format gate on the clean worktree BEFORE `join`, record the tip sha it judged, and under the lock push with `--no-verify` only if the tip still equals that sha. Saving: arithmetic upper bound, not a measurement: the lock then holds about 25 s of work per push, so the queue serialises about 14 x 25 s = 6 min; the real limit is CPU. With a cap of 3-4 concurrent preflights, 14 pushes cost about ceil(14/4) x 1100 s = about 66 min wall. CPU headroom at 4 concurrent is UNMEASURED. Reaches already-built branches, because the pre-run uses each branch's own unmodified hook code. Weakens: (1) the hook no longer fires at push time, so nothing machine-enforces "these legs passed for this sha", only the driver's own comparison; (2) `--no-verify` also skips the KS-856 non-fast-forward refusal (the driver already requires a NEW branch, so that case is closed by precheck) and the format gate (run it in the pre-run); (3) `--no-verify` rule of 2026-09-22 requires the PR to say so and name which legs ran, so the PR text must carry that. Decider: **Kam** (his bypass rule), Wednesday to brief the seats. Pre-conditions to test first, by a read-only dry design: two preflights concurrently in scratch worktrees give the same verdict as sequential; the driver's pgrep gate still matches only the real hook.

**D. Scope leg 14 to suites related to the changed paths (REMOVES, for unrelated suites).** Saving UNMEASURED without per-suite times and without a map from path to suite. Weakens: GitHub Actions is retired, so the hook is the only backstop (hook header lines 8-11); a suite not run on a push is a regression nobody sees until a later full run. Acceptable only with a full run on develop after merge and an always-run set holding the guard suites. Decider: Kam. Not recommended now.

**E. Fewer pushes: stack a seat's tickets into one branch and one PR (FASTER by count).** Seat J has 5 branches queued, R 4, V 4, K 2, E 1 in flight, F 1 (counts from the 02:04:39Z queue listing in R's status.txt and the status files read). A single push of several refs does not work today: `pre-push:351-359` REFUSES a pushed commit that is not HEAD and changes `Blockchain/Dev`. One branch per seat would save about (tickets - 1) x 1148 s per seat, for example J at 5 tickets saves about 77 min. Weakens no check; it weakens review granularity and PR blast radius, and branches already built would need re-cutting. Decider: Wednesday with Kam (PR policy). Good for tickets not yet built.

**F. Add timing (no effect on wall time, no check touched).** A `date` stamp per `step()` and per suite. Prerequisite for sizing B, D and the load question. Decider: Secuura repo owner; low risk. Worth doing alongside whichever option is chosen.

## Recommendation
Choose **C**, bounded to 3-4 concurrent pre-runs and the existing load1 < 16 gate, with the PR disclosure required by the 2026-09-22 rule, and ask Kam first because it uses `--no-verify` as the push step. Do **E** for tickets not yet built and **F** now. Hold **B** for the next develop merge window: it helps every later push, but cannot help the 14 already waiting.

## Not done / UNMEASURED, with what closes each
- Per-leg times for legs 1-13, 15, 16: timestamp per `step()`.
- Per-suite times and which suites are heavy: stamp around each suite in `run-shell-suites.sh`.
- Load share of the 948-1102 s: sample load1 every 30 s during a push; time one run on an idle box.
- Concurrency safety of the suites (ports, sockets, /tmp): two concurrent preflights in scratch worktrees.
- Docs-only and test-only elapsed from a real push: none completed today; read the first one that lands (K ks1507 for test-only).
- Seat T's 1165 s: brief only; 1144 s is from HANDOVER.md.
- Nothing was run, written, fetched or checked out beyond this report file. No credential was read or printed.
