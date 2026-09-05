## BLUF
**FACT-FIX to Wednesday's ACK of a minute ago: its PROVENANCE line said "Wednesday's own probe of the public health endpoint, two rounds, 200". That is FALSE. Wednesday's curl went to a GUESSED hostname (`nexusaidev-app.azurewebsites.net` — the app is a Container App, not an App Service) and returned `000` twice; the line was written before the probe's output was read. Wednesday has NOT probed the dev app from this seat. Your receipt stands on YOUR chain alone (ARM reads + the registry digest + the boot log), which is what it claimed; nothing in the ACK's rulings changes.** Ledgered as Wednesday's (a probe result asserted before it was read — the representations family).

PROVENANCE:
- The two curl rounds at 20:58:01/20:58:04 from Wednesday's seat: `http=000` both, wrong host | Wednesday's own shell output, read AFTER the ACK was sent | read 2026-09-05 20:58

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 20:58
