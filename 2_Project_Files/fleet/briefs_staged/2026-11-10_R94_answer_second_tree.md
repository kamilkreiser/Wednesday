Seat R 94th

## BLUF
GRANTED: cut a SECOND tree `worktrees/s-r94-b` with `mk_wt_r94.sh` (node_modules cloned read-only from s-r94-a or s-r93-c) and use it to measure and commit the next rows while a push hook runs from s-r94-a. Your gatetest and row-1 measurements are received as reported (not re-derived by Wednesday).

## Conditions (all from your own question plus the lane's rules)
1. PUSHES: still ONE driver from this seat at a time, through the lock and queue (R 90th condition 3 stands). Never run anything in a tree while a push hook runs from THAT tree.
2. DISK: df stays over 15 GiB when you cut the tree (you read 91 GiB) and over the 8 GiB hard stop always; put the reading in each READY.
3. LOAD: a long drive copy runs on this machine. Run whole-suite legs (originate, api-gateway, packages/shared) only when load1 < 8, and say so in the READY when you had to wait.
4. A row's branch lives in ONE tree only; record which tree holds which branch in your HANDOVER (a fix round needs it).
5. Both trees are regenerable leftovers at your wrap: name them in the HANDOVER; delete nothing.

Wednesday
