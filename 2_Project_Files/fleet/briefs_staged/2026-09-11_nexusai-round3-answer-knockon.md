# Fix it in this round

**Ruled: FIX `backend/server.js:3961` in this round**, as you describe: mask `workspaceId` with the existing `maskId()` (first 8, last 4), and pass the probe's message under a different key so the "FAILED at boot" banner and the TENANT MISMATCH hint survive winston. Add a jest cell (red at `e51d302`, green after), then **re-run the image proof** and count full workspace, tenant and client IDs and the secret across the whole run. All must be 0.

## Why this is inside the round, not scope creep
- **Your MAJ-3 fix is what makes the leak reachable from the package.** Shipping MAJ-3 without it would ship a regression created by the commissioned fix. Making the commissioned fix safe is part of the fix.
- **It is the same class Kam already ruled on:** `fix-first` on M1 (*"Fix it before the zip is built"*, 08:18) was an identifier-class secret in the container log.
- **The banner defect sits on the same line** and costs nothing extra to fix. A boot alarm that has never printed its own text is exactly what the tenant-transfer outage built it for.

## In READY FOR QA
Put it at the head, as its own item with FOUND / TESTED / HOW, marked **"introduced-reachable by MAJ-3, fixed in the same round"**. Name the pre-existing banner defect separately, with your winston control. Carry on with the `20a723b` control run, item 5 and the forensics as planned.

Tuesday
