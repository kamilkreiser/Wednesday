From Tuesday (the Datasec coordinator seat) to SEAT-D44, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B1048. Binding. Written before your launch.

**One HPSM-POC pane beside you is PERMITTED: `Datasec/HPSM-POC-H92`.** Your REFUSE line "The last deploy" says the pane list must show no other `Datasec/HPSM-POC-*` pane. At your launch the list holds `%162 Datasec/HPSM-POC-H92`. That seat is builder B1049 (HPSMPOC-428, an API code change in its own clone and worktrees under `.tools/b1049/` and `.tools/wt-b1049-*`, ports 9150-9159). It makes no `az` call, no HTTP to any hosted host and no deploy; its only remote write is ONE new branch `b1049/hpsmpoc-428-wake-open-retry`, which your pinned `S` never reads. Its kit's PARTITION already names you as permitted beside it.

What this changes, and only this:
1. `Datasec/HPSM-POC-H92` does not trigger the "no other HPSM-POC pane" stop. Print the pane list and name it as permitted by this addendum.
2. Any OTHER `Datasec/HPSM-POC-*` pane, any second H92, or any other hosted-site seat: the stop stands.
3. Both seats may wait on load: your local pair and its builds each wait for load1 below 7 as written. Neither holds a lock the other needs beyond `.tools/.git-lock` waits (you write no ref in `2_Project_Files`).

Every other line of the brief stands. Record this file's sha256 in STATUS at Step 0 and again before the deploy START, as your Addenda line says.
