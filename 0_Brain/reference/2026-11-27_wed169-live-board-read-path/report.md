---
date: 2026-11-27
type: reference
source: read-only diagnosis by an in-session agent (Opus), commissioned by Wednesday for WED-169; written to this file by Wednesday from the agent's reply, because the agent could not write the report file itself
status: live
---

# WED-169: why the live board's read path fails in bursts

Everything below is the diagnosing agent's finding, from its own commands, unless a line says otherwise. Wednesday has NOT re-run the Azure metrics. Raw data and the timing script: the session scratchpad folder `wed169/` (`timing.py`, `timing.out`, `plan_1m_3d.json`, `app_1m_3d.json`); a scratchpad can be cleared, so the figures that matter are copied here.

## BLUF

PROVEN (1-minute Azure metrics, 3 days): it is not the messages GET that fails. The WHOLE APP goes dark for 2 to 4 minutes: 0 completed requests, 0 MB memory, 0 CPU. Then a backlog drains with response times of 225 to 240 s (the front end's limit is about 230 s), errors, and plan CPU at 97 to 100%.

Dark windows match the poller log to the minute:
- 2026-11-26 03:45 to 03:47 UTC, then 34 errors in the following minutes;
- 2026-11-27 03:19 to 03:22 UTC, then 4 errors;
- 2026-11-27 04:07 to 04:08 and 04:11 UTC, then 27 errors.

Memory: each burst comes as PLAN memory on the B1 instance peaks at 91 to 98%, then drops about 20 points as the app returns. The app's own memory stays flat at 350 to 380 MB, so something else on the instance is growing. Every minute at or above 90% in the 3 days falls in these windows, plus two harmless peaks (11-25 03:34 and 11-27 04:16 UTC).

The empty-body HTTP 500s come from the Azure front end, not the app (the app always sends a body).

LIKELY, NOT PROVEN: the 1.75 GB instance runs out of memory around 14:20 to 15:15 AEDT daily and the app container is killed or restarted. Confirming it needs container logs; application logs, HTTP logs and detailed errors are all OFF.

## Timing (the agent's reads)

12 GETs, one at a time, 12 s apart, 15:16:36 to 15:18:52 AEDT. All 12 returned 200; min 0.07 s, median 0.20 s, max 0.71 s. Poller query: 73 bytes, 0 rows. 3-day Kam read: 89 KB, 23 rows. All rows over 3 days: 320 KB. The query is a cheap partition-plus-range read and the store is small.

## Why posts seemed to survive

They do not. No seat post happened to land in a dark minute (from the local chat mirrors). A card POST got an empty 500 at 10:02 on 11-27 (`2_Project_Files/fleet/state/live_board_post_failures.log`). The poller is simply the densest probe.

## False absence: no

- `get_kam_messages.py` lines 32 to 33 exit 1 on any non-200 or timeout.
- `tools/_kam_live.sh` lines 34 to 36 exit 2 and never print an empty list.
- `tools/kam_msgs.sh` line 59 and `tools/kam_rulings_today.sh` line 58 exit 2 on that failure.
- The poller skips the tick and keeps its watermark: rows are delayed, not lost.
- `tools/chat_reply.sh` lines 197 to 199 print an advisory instead of reporting zero.

## Fix shapes (proposals)

1. Turn on filesystem application and HTTP logging (no charge) so the next burst is caught.
2. Smallest server change: startup `-w 2` to `-w 1`. App CPU is about 5 to 10%, so one worker is enough; this restarts the app.
3. Or scale B1 to B2: twice the memory for about US$14 a month more (the agent's ESTIMATE, not read from Azure).
4. Later, a code change: the board page re-reads every card every 20 s.

No useful client-side mitigation: the poller query is already minimal, and nothing gets through while the app is down.

## Not established

- What else uses the instance's memory, and what happens daily at that hour.
- Who sends the steady 37 or so requests a minute round the clock (it looks like a board page left open; HTTP logs are off).
- Whether the app was killed for memory or restarted by the platform.
- The live card count (that route sits behind Kam's sign-in).

## Corrections this makes to earlier records

- Yesterday's ticket text and today's notes say "the read path" fails while posts work. Per this diagnosis the whole app is dark in those minutes; posts only appeared to work because none was sent then.
