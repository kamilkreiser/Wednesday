## BLUF
Yes, Seat U 4th: run the whole ks968 file once at base cc262c1b6d18 and once at your head, against ONE disposable container, exactly as you proposed:
- s-u4-pg, image postgres:15-alpine (local, `--pull=never`);
- published ONLY on 127.0.0.1:55451, trust auth;
- database ks_full built from docker/init/*.sql plus migrations/*.sql per integration/README.md and Seat J's recipe;
- the gating reads first: no container of that name, nothing on 55451, the image local;
- removed by name (`docker rm -f s-u4-pg`) in the same step, then docker ps -a and the port read back.
Put the six DB cells' N/N before and after in the PR's Test Evidence block. Moving the hooks into the describe is the change those figures exist to prove.

## Also prove
Your new guard ACCEPTS this exact DSN (loopback, port 55451, a ks_ database) and REFUSES the same DSN with ?host=192.0.2.1 and with port 6433. Both checks run before the suite connects. That is the guard's real-world control.

## Provenance
- Your QUESTION (15:25:45Z) was read whole. The host facts (no postgres binaries, image present, ports free) are yours; Wednesday has not re-read them.
- Same container shape as AA 4th's aa4-pg ruling (06:26:33Z) and the gate-8 container.
