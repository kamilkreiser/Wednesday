---
date: 2026-11-13
type: correction
source: Wednesday's own boot, 14:1x seat (no Kam words; found when the hook refused her own inbox)
status: live
tier: W
---

# A seat-scoped hook in the shared settings template binds EVERY seat

**The lesson:** `.claude/settings.template.json` is shared by every coordinator tree
(WEDNESDAY, TUESDAY, FRIDAY), so a hook written "for this seat only" with the seat's
name hardcoded runs on all of them. Tuesday's s274 inbox-scope hook allowed only
`tuesday-agent@` + `coagent@`, and at Wednesday's 14:1x boot it refused Wednesday her
OWN inbox: the inbox her merge seat reports READY and MERGED to.

**How to apply:**
1. Any hook or guard that names a seat resolves the seat from the tree (the folder-name
   rule in `fleet/cockpit/seat_resolve.sh`), never a literal. Fixed for
   `tuesday/hooks/pretooluse_inbox_scope.sh` 2026-11-13 and tested 12 cases: each tree
   reads its own inbox and coagent (rc 0); every other inbox is refused (rc 2).
2. When a hook refuses Wednesday's own core loop (her inbox, her repo, her note), it is a
   defect to fix at once, not a rule to route around: read the hook, find the hardcoded
   seat, make it resolve, test every tree.
3. A hook's directory name (`tuesday/hooks/`) is not where it runs; the template is.

**Family:** [[2026-09-09_the-seat-resolver-is-the-layer-above-every-agent-aware-fix]]
