---
date: 2026-10-12
type: feedback
source: Kam, live board 2026-10-12 17:12:10 view=wednesday, verbatim "please clear fleet activity board once questions have been answered (as a rule)"; first ruled 2026-09-08 10:19 ("clear fleet activity items once answered")
status: live
---

# Clear the fleet activity flag as soon as a question is answered

**Rule:** every QUESTION mail from a seat gets its flag cleared in the SAME step as its ANSWER is verified delivered: `bash 2_Project_Files/tools/fleet_ack.sh answered "<subject substring>" "<label>"` (rc 3 = no match yet: re-run after the collector ticks). Check `fleet_ack.sh list` at every checkpoint; it must read FLAGGED 0 unless a question is genuinely open. Only Wednesday's session writes "answered", only after delivery is verified (WED-73).

**Why:** the tool and the 2026-09-08 ruling existed, but lived only in the tool's header and the archived ledger, never in a boot-read lesson, so this seat never saw it and Kam had to repeat it on 2026-10-12. A rule that is not in the boot digest is not a rule that fires.

**Sequence per answer (the hook forbids chaining the note with the send):** (1) send_brief ... --kind answer; (2) cockpit.sh say ... --mail; (3) fleet_ack.sh answered; (4) note_entry.sh quoting the actual output lines.

**Same family, same day (18:02):** Kam's card taps arrive as chat messages ("Decision <id>: a — ..."); they do not change the store. Rule the card in the same step as acting on it (`decision_queue.sh rule <id> <key>`), mark it `--delivered <id> "<artefact>"` when the ruling is in its artefact, and compare `decision_queue.sh list open` with what he can see at every checkpoint. On 2026-10-12 three cards stayed open for 1.5 hours after I had acted on his taps, and he re-tapped them.

## EXTENSION 2026-11-16 (w=3 REGRESSION, Tuesday seat): the check now runs itself
Kam, live board 2026-11-16 10:22:53 view=tuesday, verbatim: *"please clear the fleet activity cards once they are decided. do this as a standing rule please"*. Six tapped cards had stayed open up to 3 h 20 min; he re-tapped them at 10:01. **Mechanism:** `2_Project_Files/tuesday/tools/tapped_but_open.sh`, called at the end of `kam_rulings_today.sh`, prints every card he tapped today that is still `open` in the store, with the exact `decision_queue.sh rule <id> <key>` line. When it prints anything, rule those cards before any other step. Proven live the same minute: it caught his three 10:25 taps.
