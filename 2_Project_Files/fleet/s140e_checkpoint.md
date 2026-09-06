# CHECKPOINT at your 51 percent — size the full boot BEFORE you start it, and stop rather than half-do it

## BLUF
**Your watcher reports 51 percent. Before you begin the F5 full-boot confirmation, decide whether it
FITS — the experiment and its controls and the write-up — and if it does not, STOP BEFORE STARTING IT
and say so in your wrap.** A half-run boot experiment is worse than none: it produces a result nobody
can rely on and a successor cannot tell an incomplete run from a negative one.

## HOW TO DECIDE
The experiment is not just the drive. It is: stand the real assembled gateway plus auth in your own
copy · burn the limit · drive `/api/auth//login` · the canonical control in the same batch · a
route the gateway does not serve at all, so a 200 cannot be an artefact · then the write-up with each
rc named. **If any of those would land on the wrong side of your window, that is a no.**

## IF IT FITS
Run it, and remember the standard you set yourself tonight: **if something else in the real chain
intervenes, that is the finding** and it is just as valuable as a confirmation. Do not treat an
intervention as a failed experiment.

## IF IT DOES NOT FIT
Then your remaining round is:
1. **Wrap with a handover that makes the experiment startable cold** — the exact probe shape, the
   controls, what "final" would mean, and the fact that six of eight mounts are inferred. KS-946
   should be readable by a seat that has none of tonight's context.
2. **Do NOT start the KS-486 sweep either** — it is 11 tickets and it will not fit beside a wrap.
3. Nothing else. No new PR, no new ticket unless something falls out of the wrap itself.

## UNCHANGED
Nothing goes to Peter or Stuart; Kam is carded and the default is HOLD. Your #875 and #878 are queued
for gates and need nothing from you. **Nothing deployed, demo box untouched.**
**Say which way you went in the wrap** — "it fitted and here is the result" or "it did not fit and I
stopped before starting". Either is a good answer; only a half-run is not.

PROVENANCE:
- your context at 51 percent | the fleet watcher's checkpoint wake on your pane, read by Wednesday | read 2026-09-06
- the experiment's shape and its controls | Wednesday's ruling `RULED: the F5 FULL-BOOT confirmation goes first` 2026-09-06T13:46Z and your own F5 mail 13:44Z | read 2026-09-06
- Kam is carded with default HOLD | `decision_queue.sh add` receipt for `secuura-f5-login-limiter-bypass`, read before this line was written | read 2026-09-06
