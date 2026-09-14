---
date: 2026-09-15
type: correction
source: the 2026-09-14 18:55 seat, at the 05:30 shift change — Ornith's first night lost to an open pane
status: live
tier: W
---

# A wrapped seat's pane is closed in the SAME ACTION its wrap is read — and a floor-clearing deadline is met by LISTING the panes, never by trusting that every wrap woke the coordinator

**The operative case, so the headline matches it:** a mechanism with a pane census is due to fire (the Ornith night runner's G2 at 23:30; any "no other agents run" gate), or a seat's wrap has just been read. **Two rules, both mechanical:** (1) score + `pane_close.sh` happen in the same action as reading the wrap mail — a wrapped seat with an open pane is a LIVE agent to every census; (2) at least ten minutes before any floor-clearing deadline, `tmux list-panes -t fleet:0` is read and every non-coordinator pane is closed or the deadline is reported as missed — the listing is the instrument; the inbox is not.

**The case.** s234 (the board archive pass) wrapped at 22:20 on 2026-09-14. Its STATUS (12:18Z) and wrap (12:20Z) reached the inbox; **no wake reached the coordinator for either** — the second such gap that evening (s232's wrap had sat 30 minutes, noted and not diagnosed). The seat's pane `%50` stayed open. At 23:30 the launchd night runner passed G1 and refused at G2: *"foreign live pane(s): Secuura/Blockchain-B"*. Kam's first Ornith night — the standing rule he had set five hours earlier — produced nothing. Found at the 05:30 shift-change tap; the pane closed; the runner re-run by hand inside the window, where every ticket then BUILD_REFUSED on a stale object store (a second, independent gap: the runner depends on the shared checkout having fetched develop).

**Why the existing rules did not fire.** The 09-14 coordinator lesson says every wake ends in an output — but a wake that never arrives ends in nothing, and the seat had written "all gate panes closed before 23:30" into its own pickup as a deadline it would meet *on the wrap mail*. The deadline was real; the trigger was a mail; the mail's wake did not come. **A deadline met "on an event" is a promise (2026-08-07); a deadline met by a read taken at the deadline is a mechanism.**

**How to apply:**
1. **Wrap read → score → `pane_close.sh` in ONE action.** Never "score now, close later".
2. **Before any census-gated mechanism fires, list the panes yourself** — `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'` — ten minutes before, and again at the minute; close what is wrapped; report what is not.
3. **A missing wake is a w-row the moment it is noticed, with the runner log as the instrument** — not "noted, not diagnosed". Two in one evening is a mechanism failure, and the second one cost a night.
4. **The night runner (and any unattended mechanism) states its INPUT dependencies as gates:** G2 checks panes; nothing checked that the object store carried the develop tip. Add a G6: `git cat-file -t <origin develop tip>` in the source checkout, REFUSE with the reason if absent — and the daily Claude seat's brief carries "fetch develop before 23:00" as a standing line until the runner has its own mirror (Kam's identity call).
5. **Enforcement candidate (w=3 promotes it):** `wednesday_rotate.sh --self` and the 23:00 close bell both list the fleet panes and refuse/alarm on any non-coordinator pane whose seat has a wrap mail in the inbox — the census in the path, not in memory.

**Family:** [[2026-08-07_a-promise-is-not-a-mechanism]] · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (a wake you must receive is not an enforcement) · [[2026-09-14_the-coordinator-adds-value-or-it-is-waste-three-duties-not-watching]] (duty 1: the instruction was Ornith at night — it was not carried out) · [[2026-09-03_a-pane-close-is-a-session-kill]] (the close's own discipline) · [[2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule]] (the mechanism this protects).
