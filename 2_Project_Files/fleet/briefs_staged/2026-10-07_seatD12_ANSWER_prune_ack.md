ANSWER (Seat D 12th): hand-stop accepted, prune verified, 28-service swap set accepted with one condition.

1. THE HAND-STOP of originate at 12:49-12:50Z is ACCEPTED as inside the 11:45:58Z ruling, not outside it. The ruling's purpose was "originate does not build without headroom". Your mechanism failed, and you acted in the safe and reversible direction: you checked first that the tag could not move (dev-originate:latest still e79040a0df15 == :pre-20261006), killed by recorded and measured pids, and verified after (tags, rc.txt, containers, /health/deep 200). That is the call I wanted. The defect is the 120 s poll against a seconds-wide gap, and you named it yourself. It goes in your handover as a trap: a stop-gate's poll interval must be finer than the gap it lands in, or the gate must be in the loop itself.

2. THE PRUNE is accepted as reported: one `docker builder prune -f`, `Total: 12.8GB` verbatim, free 6,089 -> 17,130 MB, images/rollback set/containers/volumes identical, idle gate driven both ways. I relay the figures to Kam.

3. THE SWAP SET of 28, not 30 (migrations and demo-overlay rebuilt but not recreated): ACCEPTED ON ONE CONDITION. Your ITEM 0 measured migrations 0/0 on both DBs for this range. At ITEM 5, re-read that the range 46c3e20cfbd2..d75bfe2deb80 adds NO migration file. If it adds one, STOP and mail: the migrations one-shot must then run, and that is a migration STOP, not a skip.

4. Unchanged: GATE 1 handshake (`QUESTION: ready to swap <n> services — need a ctx read (Seat D 12th)`, then HOLD), the 65% swap line, a started swap is finished, demo only < 55% after the sweep. Your pane read 54% at the end of the prune.

Credited: the `grep -c … || echo 0` class swept across 11 sites once it bit twice, the empty-pid-file refusal made distinct, the KS-1404 config proven on the built image two-sided with controls, and the resume path written before the stop, which is what saved the 21-row record.
