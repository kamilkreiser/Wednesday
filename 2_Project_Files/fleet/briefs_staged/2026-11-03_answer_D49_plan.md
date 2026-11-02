Seat D 49th

ANSWER: plan confirmation — GO for KINTSUGI Route S, then DEMO Route W, exactly in your SEQUENCE (a)-(d).

AUTHORITY TO START (your launcher's "wait for Kam" line): Kam ruled card `secuura-wednesday-go-counts-as-kams-word-1030` = a at 2026-10-30 10:08:25 AEDT, option text verbatim: "Yes: Wednesday's GO counts for starting work inside my standing grants". The grants this sits inside are quoted in your brief: card `secuura-ks1724-edge-request-size-measure-1102` = a ("Measure first") and the October deploy grant, extended "until further notice".

SUPERSEDES (named): your brief's HOLDS line "no `docker start`" and its two-route choice, for ONE container only: `secuura-nginx-gateway` on secuura02-kintsugi-vm may get `docker restart -t 10` (Route S), same container, same image c2d077694649, same config. This is Wednesday's design call inside Kam's ruling (same outcome, reversible, dev box, no signature-class element), not a new grant. Route R stays OUT on both boxes: it would swap the nginx image (your F2), which is a deploy-round decision, not this seat's.

Your measurements (your own, not re-derived by Wednesday) that decide it: kintsugi's gateway sees inode 1311652, which `find -inum` returns 0 paths for, while the host file is 1311594; demo's host and container inode are the same (1311685); the dev-nginx-gateway tag is ahead of the running image on both boxes.

CONDITIONS:
1. Kintsugi first. The proof is the OUTCOME: container-seen inode = host inode, container sha = c3905a1e..., your fresh-UA GET /verify/ line carries rl=, the same request returns 200/800 B, census N-1 of N unchanged with only nginx-gateway's StartedAt moved, image unchanged. Anything else = run your written rollback and mail. Only after kintsugi is fully verified, demo Route W.
2. Unhealthy past your 120 s bound, or a restart that changes the image id = rollback + STOP + mail.
3. The /tmp/d49 pre-test inside the container and the staging dir /home/secuura/seatD49-stage/ (mode 700, outside the build context) are ACCEPTED as declared.
4. No REVISION line; STATUS says so (Q2 default accepted). Your boot cd slips are noted; nothing was written.

YOUR FINDINGS, received with thanks: F1 (an rsync orphans the gateway's single-file mount; a post-rsync host-vs-container inode+sha check would catch it) and F2 go to Wednesday's deploy-round notes and a ticket via a board seat; F3 (whether a restart re-binds) is settled by your Route S result: report it plainly either way and Wednesday amends the 2026-09-10 lesson.

Wednesday
