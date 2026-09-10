# Checkpoint criteria — written BEFORE the report arrives, so they are not improvised to fit it

**Why written in advance:** a checkpoint judged after reading the report is judged against the
report. These are the conditions I set at 17:15, with kintsugi at 27/33 and nothing yet reported.

## RELEASE the demo half only if ALL of these are true

1. **Kintsugi Phase 2 completed 33/33 with a per-service exit code captured directly** — not through
   a pipe. The seat already found and fixed the `| tee` defect; the evidence must show `$?` per
   service, and any non-zero named.
2. **Behavioural verification PASSED on kintsugi**, not merely "services are up". A container running
   is not a working stack.
3. **KS-535 re-verified AFTER the restart** — wallet/anchoring config intact, from the running
   container's env as well as `.env`. This is the 07-30→08-02 incident's exact shape.
4. **Migrations 044–048 applied and the 046/047 CHECK constraints now present** — the schema baseline
   was captured with controls (constraints 0 of 300 before), so the after-reading must be non-zero
   or the migrations did not do what they claim.
5. **Demo disk re-measured at the moment of release, not quoted from the 14 G reading.** The runbook
   precondition is ≥40 G; demo had 14 G free. ~12 services is the estimate, and an estimate is not a
   measurement. **If it will not fit, STOP — no prune, no image deletion, for any reason.**

## HOLD, and escalate to Kam, if ANY of these

- Any service failed to build and the seat proposes proceeding without it.
- The behavioural verification is partial, or "passed" with caveats it cannot close.
- Demo disk is insufficient. (Kam's grant authorises deploying; it does not authorise making room.)
- Anything asks to merge a PR, bypass a gate, or use `--no-verify`. **Not covered by the grant** —
  "everything possible" = what has MERGED.

## Independent of the report — things I verify MYSELF before releasing

- **The nginx exclusion is real on demo after the rsync**, by the two-sided grep I specified: the
  closure greps 1 and the bypass greps 0 on demo's live file, **and develop's copy comes out the
  opposite way as a control.** A pair that agrees proves nothing.
- **A behavioural 404 on `/originate/` from OUTSIDE the container after the gateway restarts.** The
  file being right on the host is not the claim — a single-file bind mount binds the inode.
- **#938 still unmerged**, so nothing merged behind my back to "fix" it.

## What I will NOT do at this checkpoint

- Release demo because the grant expires Sunday and time feels short. **The grant is permission, not
  pressure.**
- Accept "no errors found" as evidence. A zero from a grep that cannot discriminate is not a pass —
  the seat itself made this argument about `guardian` and it was right.
