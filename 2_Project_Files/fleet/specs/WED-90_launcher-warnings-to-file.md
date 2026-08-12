# WED-90 spec — launchers write preflight warnings to a session-readable file
(Kam-approved 2026-08-12, ruling 10a. Third live proof of the gap: Secuura's
F-02 printed invisibly again on 2026-08-12.)

## Problem
Launcher preflight output (doctor checks, F-xx warnings, missing keys) prints
to the terminal BEFORE Claude starts, so the agent session can never see its
own warnings. The 08-04 "preflight warnings verbatim in plan-confirmation"
rule is unsatisfiable; Wednesday's pane-capture is the interim workaround.

## Required change (each project's own agent edits its OWN launcher)
1. The launcher tees every preflight warning/error line it prints into
   `4_Credentials/.launch_preflight_last.txt` (gitignored dir already),
   overwriting per launch, with a first line `# launch <ISO-timestamp>`.
2. The launcher's initial prompt gains one line: "Read
   4_Credentials/.launch_preflight_last.txt at boot; include any warnings
   VERBATIM in your plan-confirmation mail; an empty/missing file means a
   clean preflight — say so explicitly."
3. No new files outside the project folder; no secrets ever written to the
   file (warning TEXT only, never key values).
4. Exercise before trusting: run the launcher once, confirm the file carries
   exactly what the terminal showed; confirm a clean launch writes only the
   timestamp line.

## Rollout
Each running session does this as a small end-of-session item (or next boot
if wrapped already). Wednesday verifies by reading the file's presence +
content at each project's next cockpit launch.
