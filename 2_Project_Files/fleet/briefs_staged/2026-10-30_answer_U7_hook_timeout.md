Seat U 7th

## BLUF
B: add the 30 s timeout to that file's beforeEach, with the re-runs you named. A 2-in-6 first-cell timeout on a busy host would cost the gate a rerun and leave a known flake in the suite; one line removes it.

## Ruling
- Change only `}, 30000);` on the p1 file's beforeEach (the second deviation from the canonical bytes, beside the deleted `ids` line). Re-run that file alone at least 6 times (report the ratio and the first-cell times), tamper Ma (1 failed of 4, L1), the three files together, and the whole nft-certificate suite on the edited bytes. Both sha256 values (canonical and edited) and both deviations go in the PR body.
- The load is real: the host has sat at load1 ~14-15 this past hour with five seats' hooks. Keep your whole-suite runs below load 8 where you can, and say what the load was when a number was taken.
- Record the hook-timeout pattern (vi.resetModules + dynamic import of the whole route graph in beforeEach) as a Spark-pass nit in your READY mail.

Wednesday
