---
date: 2026-09-07
type: correction
source: this seat's own 00:16 quiet-hours voice violation + "morning/overnight" framing errors
status: live
tier: W
---

# Establish the LOCAL clock and day-phase from `date` at boot — before any time-framed ritual (greeting, voice, morning-vs-overnight)

**The operative case, so the headline matches it:** Wednesday is booting and about to
greet Kam, speak aloud, call it "morning," or describe how long an agent has been idle.
**Stop. Run `date '+%H:%M %Z'` first and read the day-phase from it — never infer the
time from fleet mail timestamps (they are UTC ≈ AEST−10) or from the fact that the boot's
date just rolled over.** A greeting ritual, the voice channel, and the morning-vs-overnight
framing all depend on knowing what o'clock it actually is locally.

**What happened (2026-09-07):** a fresh seat booted just after midnight (00:1x AEST),
saw the date roll 09-06→09-07 and fleet mail stamped "13:56"/"14:xx" (UTC), and concluded
it was *morning* with an agent idle *overnight*. It then (1) spoke a spoken greeting at
00:16 — a quiet-hours violation (no voice 23:00–06:00 unless on fire), and (2) wrote
"morning" and "sat idle overnight" into the chat mirror, the daily note and two briefs.
Seat A had actually been idle ~30 minutes. The gate that should have stopped the voice did
not exist (rule-only); it does now (`speak.sh` quiet-hours guard).

**How to apply:**
1. **First tool action after the brain load that touches time: `date`.** The statusline
   `ctx:NN%` is the context instrument; `date` is the clock instrument. Read both; infer
   neither from the harness counters, the mail, or the date-rollover.
2. **Fleet mail timestamps are UTC.** Local AEST ≈ UTC + 10. A mail "13:56" is 23:56 local.
   Convert before reasoning about "how long ago" or "overnight vs today".
3. **Day-phase gates rituals:** 06:00–23:00 = speech allowed + a greeting is appropriate;
   23:00–06:00 = quiet hours (no voice; `speak.sh` now enforces it — override only
   `WEDNESDAY_SPEAK_URGENT=1` for a genuine fire). A post-rotation boot inside quiet hours
   is an *overnight coordinator* seat, not a morning one — no greeting, no voice, chat
   mirror only for the record.
4. **A duration claim ("idle overnight", "waiting 3 min") is a measurement** — compute it
   from two clock reads, don't eyeball it from a pane's "done HH:MM" against a misread now.

**Family:** [[2026-08-03_mental-model-not-source-of-truth]] (read the source — here the
source is the system clock) · [[2026-08-14_i-read-representations-they-read-sources]]
(a mail timestamp is a representation of an instant, in another zone) ·
[[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (the voice rule was lesson-only until
the `speak.sh` guard) · [[2026-08-03_daily-rhythm-6-to-23]] · voice-protocol.md.
