---
date: 2026-09-30
type: grant
source: Kam, live board 2026-09-30 09:07:30 view=tuesday, ruling card nexusai-gate11-opus55-safeguard-model-switch
status: live
tier: W
---

# A QA gate flagged by Opus 5.5's safeguards may switch to Opus 4.8 — per gate session, never as a setting for every seat

**The operative case, so the headline matches it:** a QA gate session (any Datasec gate this seat launches)
has been stopped by Opus 5.5's safeguards and is parked at Claude Code's "Switch to Opus 4.8?" dialog.
**Kam's ruling (b) says: switch THAT session to Opus 4.8 and let it carry on.** It does not say: change the
model for every seat, and it does not say: answer the dialog with "Switch automatically".

**His words, verbatim:** *"Decision nexusai-gate11-opus55-safeguard-model-switch: b — Let QA gates switch to
Opus 4.8 when flagged"*. Option (b) on the card read: *"Answer that dialog per session (not 'switch
automatically' for every seat), so the attack-style rows can run. A model choice only you can make."*

**Why it came up:** gate 11 (RD-591 + RD-735, 2026-09-30) was stopped five times by the classifier on
security-test wording (forged headers, outside dialers, userinfo leaks), then sat at the switch dialog
holding the jest lock. Tuesday did not answer the dialog (a model/config choice, and the gate shares this
seat's `CLAUDE_CONFIG_DIR`), closed the gate to free the lock for merges, and carded it.

## How to apply
1. **Never choose "1. Switch automatically"** in that dialog: it is "switch without asking from now on", a
   persistent config change, and the gate runs on `TUESDAY/4_Credentials/.claude` — the same config as this
   coordinator seat. That would switch seats Kam did not name.
2. **Switch the one session:** dismiss the dialog, then switch that pane's model to Opus 4.8 with the
   session's own `/model` command, and tell the gate by mail (a pointer tap behind it) that it now runs on
   Opus 4.8 by Kam's ruling of 2026-09-30 09:07, naming this file. Record the switch time in the gate brief's
   report requirements (the report must say which rows ran on which model).
3. **The full gate runs, attack rows included** — the ruling exists so they can run. The earlier "narrowed
   brief" default is superseded for gates, not for any other seat.
4. **Scope: QA gates only.** Builder seats and this coordinator stay on Opus 5.5 unless Kam says otherwise.
   No expiry stated; re-read if he changes models or accounts.

**Family:** [[2026-08-07_protocol-v1.3-signed-delegation]] (a model choice was his, not mine) ·
[[2026-09-06_a-scoped-override-carries-its-own-expiry]] (none stated — said so) ·
[[2026-08-16_classification-is-the-field-that-grants-authority]] ("per session" is the scope word that decides
which dialog option is inside the grant).
