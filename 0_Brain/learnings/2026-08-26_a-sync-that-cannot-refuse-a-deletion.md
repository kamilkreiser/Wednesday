---
date: 2026-08-26
type: correction
source: "Self-found at the first Studio boot after the travel day: the 2026-08-25 NAS unison leg (launched by my predecessor, cut by the 10:41 shutdown) had deleted six folders from DevMASTER — Datasec/{Marketing_Collateral, RESEARCH, Security Review (796 MB), Task_Dispatcher, Websites} + MultiAgent Coordination. The handover said 'check its log'; the log said 'Deleting … from /Volumes/DevMASTER' 5,316 times. Root cause: the NAS directory is literally '!CODING/datasec' while every other replica has 'Datasec'; the profile runs prefer=newer with confirmbigdel=false."
status: live
supersedes: ""
tier: M
---

# A sync engine that cannot refuse a deletion is a delete command with a delay — read its log for `Deleting`, and check case across replicas before any leg

**The operative case:** I am about to run, or have just run, a bidirectional sync
leg (unison, rsync `--delete`, any two-way engine) between drives Kam depends on.
**Two checks, both cheap, neither of which I did on 2026-08-25:**

1. **Before the leg: prove the replicas agree on the NAMES at the top levels.**
   `ls` on a case-insensitive mount (SMB from macOS, APFS default) will show
   `Datasec` for a directory that is really `datasec`, and unison compares
   case-sensitively. To unison the two trees are *different paths*, so it
   "reconciles" by deleting what each side "lacks" — which is everything under
   both spellings. `python3 -c 'import os; print(os.listdir(root))'` shows the
   real names; `ls -d root/Name root/name` both succeeding on an SMB share is the
   tell, not the all-clear.
2. **After the leg: read the log for `Deleting` before reading it for `finished`.**
   `rc=0` and "finished propagating" are true of a run that deleted 796 MB. The
   only line that carries the cost is `[BGN] Deleting <path> from <replica>`.
   A cut run (shutdown mid-propagation) writes no summary at all, so the absence
   of "Sync finished" is itself the signal to read the body.

## Why the existing lessons did not catch it

- [[2026-08-05_verify-the-chain-not-the-legs]] says verify content at the
  destination. I verified the KK_DEV leg's content and called the NAS leg
  "still running" in the handover — a leg I never verified because it was not
  the leg I needed. **A leg I do not need can still delete from the drive I do.**
- [[2026-08-06_artifact-presence-is-not-execution]] says find the proving line.
  I grepped the log for `Sync finished` and found one — the KK_DEV leg's — and
  read it as the NAS leg's. **The proving line for a deletion is `Deleting`,
  and I never asked the log the question whose answer would have hurt.**
- The engine's own guard was off: `confirmbigdel = false` in the profile
  disables unison's refusal to delete a large fraction of a replica. That is
  Kam's file and his setting; my part is knowing the guard is absent and
  supplying it by hand (the two checks above) until he turns it back on.

## How to apply

1. **Never start a sync leg from a session without the two checks**, and never
   hand a running leg to a successor as "may still be running — check its
   log" without saying WHAT to grep for (`Deleting`, `conflict`, absence of
   `Sync finished`).
2. **Treat a mid-run shutdown as an incident, not a skipped step.** The 10:41
   shutdown was the T9 handover's planned end; the NAS leg's state at that
   moment was unknown and stayed unknown for 24 hours.
3. **Recovery order that worked (2026-08-26):** find every copy (travel drive,
   `~/.unison/backup` via `backup = Name *` + `backuploc = central`, the NAS
   itself) → restore additively (`rsync -a`, no `--delete`) → verify by file
   COUNT and a HASH SAMPLE, not by `du` → run only the legs whose replicas are
   proven case-consistent → card the unsafe leg for Kam with the root cause.
4. **A restore is a write into someone else's folders** (hard rule 1) — it
   happened on Kam's one-click ruling, not on my judgement, and the card carried
   the default HOLD so silence meant nothing moved.
5. **doctor / PORTABILITY:** the case probe belongs in the pre-travel checklist
   (PORTABILITY item 20) — a top-level `os.listdir` diff across every mounted
   replica before "Sync All Drives" runs.

**Related:** [[2026-08-05_verify-the-chain-not-the-legs]],
[[2026-08-06_artifact-presence-is-not-execution]],
[[2026-08-25_one-drive-devmaster-is-master]] (rule 4: sync then launch — now
with the two checks in front of the sync),
[[2026-08-25_travel-drive-stale-pointers]] (day-two lesson of the same move),
[[2026-08-07_a-check-that-cannot-fail]] (a green exit over a deletion), [[_ledger]]

## RECURRENCE 2026-10-04 (w=2) — the lesson fired as DETECTION and never as PREVENTION, so the leg stayed armed
**The case.** Wednesday's own nightly NAS leg (`scheduler/nas_sync.sh`, launchd `com.wednesday.nassync`, 03:30) ran ~14 h, was killed by Kam's 17:50 reboot, and had already propagated false NAS-side deletions of ~200 tracked + ~245k untracked WEDNESDAY files onto DevMASTER. Restored the same evening (git HEAD + an additive rsync from the NAS). Kam did not know the job existed.
**Why the rule did not fire (the w=2 diagnosis).** This file's rules are written for a session STARTING a leg ("never start a sync leg without the two checks"). The 03:30 leg is started by launchd, so no session ever reached the decision point. The wrapper's own header said, honestly, that it could only DETECT a mass deletion after the run, and that honesty read as the risk being handled. Nobody re-asked whether a detect-only mechanism should run unattended at all. Detection after the fact is a post-mortem, not a guard.
**The rule, extended:**
1. **A scheduled mechanism that can destroy data and cannot PREVENT that is held, not armed.** It is carded to Kam with the prevention missing named. "We'd see it in the log" is not a reason to keep it running.
2. **Holds use independent locks:** `launchctl disable` (which survives a login, unlike `bootout`), a hold file the script refuses on, the installer skipping it, and doctor reporting HELD. Any one of them alone gets undone by a well-meaning successor following a "missing job" hint.
3. **The principal hears about every unattended destructive-capable job at least once**, in the morning receipt, with what it can and cannot prevent. A risk he has never heard of is a risk he never accepted.
Locks: commit 4d1ce484. Card: `wed-nassync-rearm-shape-1004`.
