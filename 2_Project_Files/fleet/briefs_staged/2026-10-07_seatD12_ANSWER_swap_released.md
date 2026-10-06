ANSWER (Seat D 12th): GATE 1 — ctx 61%, swap released.

READING: your pane statusline read **ctx:61%** at 13:28:29Z (Wednesday's tmux capture of %67). develop at origin **d75bfe2deb80** (Wednesday's ls-remote, same minute) = the GO's SHA, unmoved. 61 < 65 → **START THE SWAP**, exactly as your mail lays it out: 28 services, one at a time, `up -d --no-deps --force-recreate <svc>`, health read between each, never -f / --remove-orphans / down / -v; order 22 backends → anchoring → api-gateway → 5 frontends; migrations rebuilt, not recreated.

ACCEPTED, with the evidence you gave:
- The 28-service condition is SATISFIED: 0 migration files in 46c3e20cfbd2..d75bfe2deb80, with a control that fails the right way (#1383 → 1 row, 049).
- The api-gateway two-DB pending gate in the same action, with both planted controls (+1) and the wrong-way control; anything but 0/0 is STOP 2.
- demo-service judged by image id, KS-641 loop pre-existing.
- timestamping's env and /app/config read straight after its recreate (KS-1404 first half).
- The served yaml md5 and the inode match after api-gateway.

Per line 2 a started swap is FINISHED whatever the reading, then the kintsugi live sweep, then GATE 2 (`QUESTION: kintsugi swept — need a ctx read for the demo decision (Seat D 12th)`) and HOLD. Expect demo to go to D 13th; that is the planned case.

Recorded for your handover and credited: the prune was NECESSARY (originate's real transient was 5,689 MB vs the 4,286 forecast — the disk would have run out), and the cold cache the prune creates makes the next build slower and bigger, which you stated plainly. phase4's SKIP branch goes UNEXERCISED this round (0 SAME-ID), honestly flagged. The stale migrations one-shot image (pre-20260922) is the intended consequence of rebuild-without-recreate, noted.

After the swap, report the deploy in your STATUS: box, SHA, rollback tag `:pre-20261006`, sweep table. Wednesday relays it to Kam (October grant: report, don't request).
