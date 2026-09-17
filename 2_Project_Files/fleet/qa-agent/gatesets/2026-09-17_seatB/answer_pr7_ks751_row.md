Wednesday -> Seat B successor (Secuura/Blockchain-B)

## BLUF
**Your DEFAULT stands: remove BOTH rows in PR-7** (GHSA-rgwj / KS-763 and GHSA-3f6p / KS-751). It is the brief's own per-PR rule, "remove a row only in the PR whose merge makes the advisory absent from EVERY lock", and PR-7 is that PR. It is also inside Kam's 18:31 ruling ("Override to mysql2 3.23.1").

## Recommendation
1. Remove both rows; conservation stated for whichever base you merge onto (31 → 29 after #1030, else 32 → 30).
2. **Because the KS-749 reason text says an override was once measured INERT: the proof that matters is RESOLUTION, not the manifest.** Show by parse that mysql2 resolves to 3.23.1 in BOTH locks (root, services/originate), with 3.15.3 absent. Run the negative control on develop (rc 1 naming both advisories). If either lock still resolves below 3.22.0, STOP and ask; do not remove the KS-751 row.
3. KS-751 read by Wednesday (Linear, read-only, 21:0x): state "Tested Not Deployed", **no assignee**, title "Three HIGH advisories published 2026-09-01 … (browserslist x2, mysql2)". It is a three-advisory ticket, so your facts comment says PR-7 closes the MYSQL2 advisory only and the two browserslist ones are not touched. No state change, no reassignment, `Refs KS-751` (never Closes).
4. The READY names this ruling (this mail) under the two-row removal.

## Detail
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done, Refs never Closes, never delete; nothing pushes before #1030's MERGED receipt, develop merged in.
