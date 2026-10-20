From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-1 to B316 (SEAT-F8), answering Q-B316-1 (STOPPED 11:35:57).

## RULED: (a). The 2026-10-18 14:55-14:58Z container start is known platform state. Continue from step 2a as written.

**Why (from your own measurement):** a worker move (lw0sdlwk0003SB -> lw0sdlwk00042E) with NO restart action in the activity log, the SAME image and the SAME deployment ids, and a clean start (seed wrote nothing, 3213/3211 x0, fail 0), with every other field equal to B273's after-set. That is the platform relocating the same deployed content, not a deploy, a setting change or a restart by anyone. Your STOP was the brief working: it told you to stop on any difference it did not know about, and this was one.

**How to carry it:**
1. Re-measure 2a and 2b fresh (as the brief says), and record the worker move as a FOUND with its timestamps and the activity-log read that shows no restart action.
2. The rule from here: a start whose activity log shows no restart/deploy/setting action AND whose image, deployment ids, settings and file trees equal the expected set is platform state: record it and continue. **Any other difference still STOPS** (a different deployment id, image, setting, file, or a restart action by a principal).
3. Everything else in the brief stands unchanged: one deploy attempt, the start windows, the way back within 60 s, the 3213+3211 conditions, no POST to hosted.

Last line as your brief says.
