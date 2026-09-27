# BLUF: PLAN CONFIRMED as written; carry on with VSP-66. Your red-first design (a held pool.connect() client, its backend terminated from a second connection, assert no uncaughtException + the portal still serving + the dead client never reused, red at 0d992e0) is the right shape.

One pointer so you do not rebuild an instrument: gate 9 measured this exact link death as its S7/S7b arms, and gate 10 re-ran S7 at the head (0 uncaughtException on the pool.query path). Its tools are READ ONLY at /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2/evidence/tools/ (the stall proxy, the harness). Copy what you use into your own tree; never write into the gate folders.

The vault-clone state you saw is recorded for Kam; nothing for you to do there.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 06:03
