Seat R 93rd

ANSWER: plan confirmation (Seat R 93rd). CONFIRMED. GO for the tree-side set-up and round 1.

1. GO, in this order: fetch develop into worktrees/s-r90-base ONLY (its own configured ssh command; never the shared checkout); take over s-r92-a and s-r92-b on the conditions your brief carries; row 2 by CHERRY-PICK of 05908e3c50de onto d0b4825cc244 (or the develop you read at the cut) inside s-r92-b, saying the new head and re-running the file at the sha you push, as you proposed; gatetest the re-keyed driver on a scratch lock (a control that must refuse, then one that passes); then round 1 rows 1 to 3, one driver at a time, one READY when all three are VERIFIED at origin.
2. Coordination, no action for you beyond care: Seat U 21st (lane U, launched 06:39) was granted a base clone made with git clone --reference worktrees/s-r90-base, which READS s-r90-base's objects and writes nothing there. Your fetch into s-r90-base only ADDS objects, so the two do not conflict. Never run gc, prune, repack or any object-removing verb in s-r90-base: U's clone depends on those objects.
3. Faults: accepted as you listed them (boot cd and lockless git calls came from the launcher's boot recipe; the six variable names and the key prefix printed once at boot). From here on: no cd at all, GIT_OPTIONAL_LOCKS=0 on every shared-checkout git call, nothing from a .env printed, not even a name or prefix. Your REC/tools/__pycache__ is your own record folder: move it into a quarantine folder with a WHY row (never rm), or leave it and name it in the HANDOVER.
4. Your new ready_patch_o121_r93.py (fence equals the canonical patch by sha256 and size): accepted as a declared kit change; name it in the HANDOVER.
5. Note F for round 3: as you plan it (docs-fragments check in your own tree on the applied round-3 diffs before any round-3 push; a refusal = STOP and QUESTION).
6. Unchanged: tier 2 for round 1; row 4 tier 1 in its own READY; rows 5 to 7 tier 1 in one READY; no merge, no deploy, no ticket state change; mail only for READY, QUESTION and the wrap.

Wednesday
