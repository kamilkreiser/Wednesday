# NOT A CARD: composer-guided-hold-1119 (Datasec/Security Composer) - the Guided hold is already ruled
Drafter A, read at source 2026-11-19 17:00 to 17:10 AEDT (read-only). No card is drafted because the product owner has already decided this.

## The ruling, quoted
- Composer CLARIFICATIONS.md line 1298, C-71 row COMP-2 (card composer-decisions-pack-1012, option a "All defaults for this project", ruled 2026-10-12T20:12:54+11:00):
  "Guided mode is switched off on the demo. Eight open items only matter in Guided mode. Build any of them while it is off? (a) Hold them all until you switch Guided back on . (b) build some now (name them)" - recommended and ruled default: "(a) Hold them all." - "If you pick the default: No Guided work until you turn it back on."
  The trigger for lifting it is his own act ("until you turn it back on"). It names no date, and he has not asked to turn it on.
- Card composer-guided-view-1006 (ruled c, 2026-10-06T19:29:30+11:00), option c: "Hide Guided now AND bring the 66 questions into the Expert flow: (a) the same day; then a separate, larger brief puts the questionnaire's 66 questions and their 'how to ask' help into the one view". Option a's detail on that card: "one switch brings it back". Recorded as C-52 (line 885). The 66 questions in the Expert flow went on the demo under card composer-expert-66-demo-deploy-1007 (a).
- Line 1262 (before C-71): "Guided stays OFF: ... /site.json = { "environment": "demo", "guided_view": false }" - relayed, not probed by me today.
- Applied since: PCOMP-75 comment 41225, 2026-11-15 18:19: "HELD. This ticket's open work is parked on purpose and is not to be built while the Guided hold stands: No Guided work until you turn it back on."
- Searched CLARIFICATIONS.md from line 1299 onward for Guided hold, switch, turn back on and the switch name (positive control: the same search finds line 1768, and the same pattern finds line 1262 before C-71): no later entry changes, lifts or ends the hold. decision_queue.sh prior returned the 2026-10 Guided cards above and no later one.

## What was verified about the ten keys (Jira GET, 2026-11-19)
All ten are Backlog and unchanged since 2026-10-23, except PCOMP-75 (comment 2026-11-15). Nine carry label held; PCOMP-75 does not carry the label but its comment says held.
| key | what | hold row |
|---|---|---|
| PCOMP-68 | session end loses one screen of typing (GuidedWizard) | C-71 COMP-2 (a) |
| PCOMP-69 | Seat C wording shown in Guided awaits the product owner | COMP-2 (a) |
| PCOMP-72 | emptied box plus Next deletes a saved answer (GuidedWizard) | COMP-2 (a) |
| PCOMP-75 | End page heading touches section tiles (Guided End page); items a and c already fixed | COMP-2 (a) (#108 (c)) |
| PCOMP-84 | Dashboard 'How an engagement works' cards at 390 px (Dashboard.tsx ExpertGuide) | COMP-2 (a) row #223 |
| PCOMP-85 | Guided home 4-step guide not clickable | COMP-2 (a) |
| PCOMP-86 | Guided persona's demo data is mostly finished examples | C-71 COMP-16 (a) "Hold both" (his by ownership; demo data) |
| PCOMP-87 | Guided home reads each row one at a time | COMP-2 (a) |
| PCOMP-88 | read-only role sees editable wizard words (GuidedWizard) | COMP-2 (a) |
| PCOMP-90 | Guided wizard: draft pinned to older release reads as answerable | COMP-2 (a) |

## What this changes for the backlog (what it makes buildable)
- Nothing becomes buildable. The ten are correctly held and wait on nothing from the product owner today: they wait on his own switch, which he has not thrown. The sweep's line "10 wait on Kam" is not a call for a card; they should count as held on purpose, not as waiting on a decision.
- Two oddities for Tuesday, for the Jira record, not for him: (1) PCOMP-84 is about the Expert Dashboard, not Guided; its own State line says a phone fold of that strip is "the project owner's to ask for", and it sits under COMP-2 only because row #223 was listed there. (2) PCOMP-86 is held under COMP-16, not COMP-2 (demo data, "until you raise them").
- Optional, Tuesday's call: the only question never put to him is "off for good" (then the ten close as not wanted). It frees no builder and costs him a tap; I recommend not raising it unless he says Guided is dead. If wanted, the card would be: BLUF "Guided mode stays hidden. Do you want to drop it for good, so ten parked tickets close?" options a keep it hidden (default), b drop it for good, c turn it back on.
