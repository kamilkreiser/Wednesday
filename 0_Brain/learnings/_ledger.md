# Correction ledger — frequency-weighted reinforcement

Design per Kam (2026-08-03, voice): *"similar to when people learn, frequency is
used for reinforcement — if a mistake happens once, that could be isolated; if it
happens more than once, an increased weight is given."*

## The weight scale

Weight = number of occurrences. Each recurrence escalates the response:

| w | Meaning | Required response |
|---|---|---|
| 1 | **Isolated** — could be noise | Log it. Write a lesson file only if it would change future behaviour (importance filter). |
| 2 | **Reinforced** — a pattern, not noise | Lesson file mandatory. If one existed and didn't fire, diagnose *why* (wrong file? too abstract? bad retrieval handle?) and fix the lesson, not just the mistake. |
| ≥3 | **Regression** — the system is failing to learn | Treat like a failing test (no-skip rule). Automatic promotion candidate: move the rule into `identity/` or into *enforcement* (launcher check, hook, CLAUDE.md line). Raise it with Kam at the next briefing. |

Rules:
- Same *underlying* mistake in a new costume still increments the weight — match
  on root cause, not surface form.
- Weights never decay automatically. They are only retired at weekly
  consolidation, with the reasoning written in the audit note.
- Positive reinforcement counts too: when Kam explicitly praises a behaviour,
  log it as `praise` — repetition there tells us what to *keep* doing.

## Ledger (newest at top)

| 2026-11-20 | 🟡 **THE 04:5x ROTATION SUCCESSOR's FIVE MECHANISM-CAUGHT SLIPS IN ONE SHORT SEAT: a `cd` in its first call (pretooluse_no_cd refused), an unquoted `====` separator (zsh word-split hook refused), a cockpit tap addressed by pane id `%108` instead of its name (cockpit.sh rc 8), a note carrying a receipt verb with no receipt file (note_entry rc 3), and two UNBOUNDED recursive greps (over 2_Project_Files and fleet/state/*.log) that ran past the 120 s timeout and had to be stopped by hand.** [W] All zero cost: every one refused before acting or was a read. 🔑 [[2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour]] (read a tool's usage line before its first call: the tap's name rule is in cockpit.sh) + [[2026-08-15_a-cap-is-never-neutral]] (an unbounded search over a tree with node_modules is a cost, not a read). Rule (re-applied): absolute paths, never cd; `echo ----` separators; read a fleet tool's usage before calling it; a recursive search names its directory narrowly (or uses a known file) before it runs. | correction (mechanism-caught, zero cost) | +1 (use-the-fleet's-tool family) | [[2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour]] | noted 05:3x |

| 2026-11-20 | 🟡 **AT 03:40 THE 02:5x ROTATION SUCCESSOR PUT `fleet_ack.sh answered` AND THE NOTE LINE SAYING 'fleet_ack flag cleared' IN ONE CALL; fleet_ack REFUSED (the collector had not yet ingested B 207th's QUESTION), SO THE NOTE RECORDED AN ACT THAT DID NOT HAPPEN.** [W] Self-caught on reading the same call's output; corrected in the note at once (03:40 CORRECTION line); zero cost (no seat or Kam relied on it). 🔑 [[2026-11-01_a-note-is-its-own-message]] + [[2026-08-26_mirror-reports-state-not-intent]] (a note line is a receipt; written before the step's output it is a forecast). Rule (re-applied): the note is its own call, composed only after the step's output is on screen; a refusable step (fleet_ack, send, launch) is never bundled with the line that reports it. | correction (self-caught, zero cost) | +1 (note-alone family) | [[2026-11-01_a-note-is-its-own-message]] | corrected 03:40 |

| 2026-11-20 | 🟡 **THE HOOK EXTENSION THE 23:4x SUCCESSOR ARMED AT 23:55 REFUSED A LEGITIMATE READ FIVE MINUTES LATER: a `grep` over cockpit.sh's OWN SOURCE was matched as 'cockpit.sh with NO verb', because the checker matched the tool's PATH anywhere in a segment, not in COMMAND POSITION. Its 7-quiet selftest held no case where the path is an argument (grep, sed, cat, ls).** [W] Self-caught on the refusal, zero cost (a read was blocked, nothing ran); fixed 2026-11-19 23:59: the checker matches only in command position (optional ( {, VAR=x, nohup/time/exec/command, bash/sh/zsh, then the path), and the selftest gained the read cases (10 fire / 11 quiet; the old any-position match ablated reads 3 failures). The first version's own live test (`true <path> --help`) was itself a path-as-argument case, so the proof that armed it was the false positive. 🔑 [[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]] + [[2026-09-11_red-proof-arms-cover-every-legitimate-shape-of-the-real-event]] (every legitimate shape gets a CLEAN arm: here, reading the tool). Rule (re-applied): before arming a refusing hook, list the legitimate shapes that MENTION its subject without doing the act (reading, grepping, documenting it) and give each a quiet arm. | correction (self-caught, zero cost) | +1 (new-rule-just-after-adoption family) | [[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]] | fixed 23:59 |

| 2026-11-19 | 🔴 **AT 22:10 THE 21:2x SUCCESSOR PUT A BARE `cockpit.sh 2>/dev/null >/dev/null` IN FRONT OF D 74th's pane_close CALL: NO VERB, BOTH STREAMS DISCARDED, NO PURPOSE. THEN, INVESTIGATING IT, RAN `cockpit.sh --help` TO SEE WHAT A BARE CALL DOES.** [W] Self-caught on re-reading the call; both fell through to the `*)` branch (`die "usage: ..."`), so nothing was written; pane list unchanged (read by tmux list-panes). Zero cost. The hook did NOT catch it: pretooluse_cockpit_verb.sh refuses an INVENTED verb, not an ABSENT one. THIS IS THE THIRD DAY of the 11-17 rows' exact costume (07:20 wake_ack, 10:5x and 13:03 cockpit list), read at THIS seat's boot: the boot read the rows as facts about other seats, not as a rule about my next call. 🔑 [[2026-10-31_never-invoke-a-write-command-to-read-what-it-would-say]] + [[2026-08-06_never-discard-stderr]]. Rule (re-applied): a fleet tool appears in a call only as the act it exists for, with its output kept; to learn what a tool does, READ its header or dispatch (`sed -n`), never run it. MECHANISM OWED (w>=3 regression, failing-test treatment): extend the hook to refuse (a) a fleet tool call with no verb and (b) any fleet tool call whose stdout AND stderr both go to /dev/null; claim it as WED work first; raise with Kam at the next briefing. | correction (self-caught, zero cost) | +2 (invoke-to-read family; REGRESSION, w>=5 across 11-17..11-19) | [[2026-10-31_never-invoke-a-write-command-to-read-what-it-would-say]] | noted 22:11; mechanism BUILT + armed 2026-11-19 23:55 by the 23:4x successor: fleet/hooks/pretooluse_cockpit_verb.sh now refuses (a) cockpit.sh with no verb or a --flag in the verb slot and (b) any fleet/tools *.sh call with stdout AND stderr both to /dev/null; checker fleet/hooks/pretooluse_cockpit_verb_check.py --selftest 7 fire / 7 quiet, 3 ablations red, live fire refused; quoted heredoc bodies stripped (the old hook refused a heredoc that wrote the new one) |

| 2026-11-19 | 🟡 **THE 21:2x SUCCESSOR TYPED TWO CLOCKS IN ITS FIRST TEN MINUTES: '21:28' IN A NOTE LINE STAMPED 21:27 (K 54th's pane read), THEN A SELF-CHECK OF '21:3x' ON S 94th's BRIEF (the send gate REFUSED it) AND, ON RE-ATTEST, '21:30' WHILE `date` IN THE SAME CALL PRINTED 21:29.** [W] Caught by the note tool's advisory and the send gate's self-check refusal; zero cost (no act rested on either time). The second re-attest passed the gate though it was a minute AHEAD: the gate checks shape and freshness, not that the minute was read. 🔑 [[2026-08-14_i-read-representations-they-read-sources]] (#2: a timestamp is generated in the writing command or pasted from tool output, never retyped). Rule (re-applied): a SELF-CHECK or note clock comes from `date '+%H:%M'` run in the SAME call that writes it (sed the line from the tool's output), never typed after looking at a clock. | correction (tool-caught, zero cost) | +1 (typed-clock family) | [[2026-08-14_i-read-representations-they-read-sources]] | noted 21:29 |

| 2026-11-19 | 🟡 **AT 18:40 THE 19 NOV AFTERNOON SEAT CHAINED `send_brief.sh ... ; cockpit.sh say --mail ...` IN ONE CALL FOR S 92nd's ADDENDUM 1; THE SEND WAS REFUSED (card_id_gate read a quoted option detail as a card title) AND THE TAP WENT OUT ANYWAY, POINTING S 92nd AT A MAIL THAT DID NOT EXIST.** [W] Self-caught on reading the output; resent rc 0 within a minute, and the tap was queued behind the seat's running turn, so it landed after the mail existed; zero cost. 🔑 [[2026-08-17_check-the-refusal-before-the-kill]] (a tap is a destructive-class step for this purpose: it acts on the seat) + [[2026-09-01_a-tap-is-a-pointer-not-a-message]]. Rule (re-applied): the tap is its own call, made only after the send's rc 0 is on screen; never `;` or `&&` it behind a refusable send. | correction (self-caught, zero cost) | +1 (check-the-refusal family) | [[2026-08-17_check-the-refusal-before-the-kill]] | resent 18:40 |

| 2026-11-19 | 🟡 **AT 06:04 THE 19 NOV MORNING SEAT's BOOT NOTE SAID EXPIRING-GRANTS AND WEEK-INSTRUCTION WERE READ 'in the pickup read'; THAT CALL's OUTPUT (298 KB) WENT TO A PERSISTED FILE AND ONLY THE PICKUP's TOP WAS OPENED.** [W] Self-caught at 06:06 while writing the pickup block; read then, correction line in the note. Zero cost (no action rested on it), but the read surfaced a live item: the 11-06 board-clearing grant's outer read is Friday 20 Nov (re-ask line added). 🔑 [[2026-09-10_i-endorse-things-i-have-not-read]] + [[2026-08-06_artifact-presence-is-not-execution]] (a command that cat'ed a file is not a read of it when its output was persisted unopened). Rule: when a tool result is persisted ('Output too large'), every file in that call stays UNREAD until opened; the boot note lists only what reached the screen. | correction (self-caught, zero cost) | +1 (endorsed-unread family) | [[2026-09-10_i-endorse-things-i-have-not-read]] | corrected 06:06 |





































**Rows dated 2026-11-17 and earlier live in [[_ledger_archive]]** (11-17 moved 2026-11-20 05:3x by the 04:5x rotation-successor seat at the 05:30 shift-change wrap, 14 row(s), conservation asserted; 11-15 moved 2026-11-18 05:31 by the 14:52 (11-17) successor seat at the 05:30 shift-change wrap, 12 row(s), conservation asserted; 11-13 moved 2026-11-16 03:4x by the 00:5x seat before its rotation, 12 row(s), conservation asserted; 11-10 moved 2026-11-13 05:3x by the 03:1x rotation-successor seat at the 05:30 shift-change wrap, 10 row(s), conservation asserted; 11-07..11-09 moved 2026-11-12 06:0x by the 04:1x (11-12) seat at the shift-change wrap, 35 row(s), conservation asserted (1800 == 1800); 11-06 moved 2026-11-10 05:3x by the 22:20 (11-09) seat at the 05:30 shift-change wrap, 19 row(s), conservation asserted; 11-05 moved 2026-11-09 05:3x by the 03:5x seat at the 05:30 shift-change wrap, 22 row(s), conservation asserted; 11-04 moved 2026-11-07 05:3x by the 04:0x seat at the 05:30 shift-change wrap, 17 row(s), conservation asserted; 11-03 moved 2026-11-06 05:3x by the 20:00 (11-05) seat at the 05:30 shift-change wrap, 19 row(s), conservation asserted; 11-01..11-02 moved 2026-11-05 05:3x by the 22:0x (11-04) seat at the 05:30 shift-change wrap, 38 row(s), conservation asserted (1697 == 1697); 10-29..10-31 moved 2026-11-03 05:3x by the 03:2x successor seat at the 05:30 shift-change wrap, 34 row(s), conservation asserted (1662 == 1662); 10-27..10-28 moved 2026-11-01 05:3x by the 00:0x rotation seat at the 05:30 shift-change wrap, 27 row(s), conservation asserted (1625 == 1625); 10-24..10-26 moved 2026-10-30 05:3x by the 03:2x successor seat at the 05:30 shift-change wrap, 14 row(s), conservation asserted (1601 == 1600 + 1 new); 10-21..10-23 moved 2026-10-27 05:3x by the 22:2x seat at the 05:30 shift-change wrap, 14 row(s), conservation asserted (1561 == 1561); 10-20 moved 2026-10-23 05:3x by the 22 Oct morning seat at the 05:30 shift-change wrap, 18 row(s), conservation asserted (1538 == 1538); 10-19 moved 2026-10-22 05:3x by the overnight Sonnet seat at the 05:30 shift-change wrap, 27 row(s), conservation asserted; 10-18 moved 2026-10-21 05:3x by the 15:01 seat at the 05:30 shift-change wrap, 9 row(s), conservation asserted; 10-16 moved 2026-10-20 05:1x by the overnight seat at the 05:30 shift-change wrap, 3 row(s), conservation asserted; 2026-10-12..2026-10-15 moved 2026-10-19 05:3x by the overnight seat at the 05:30 shift-change wrap, 50 row(s), conservation asserted; 10-10 moved 2026-10-14 05:3x by the overnight seat at the 05:30 shift-change wrap, 15 row(s), conservation asserted; 10-05..10-09 moved 2026-10-13 05:3x by the overnight seat at the 05:30 shift-change wrap, 87 row(s), conservation asserted; 10-04 moved 2026-10-08 05:3x by the overnight seat at the 05:30 shift-change wrap, 12 row(s), conservation asserted; 10-03 moved 2026-10-07 05:3x by the night seat c1dbe0b9 at the 05:30 shift-change wrap, 1 row(s), conservation asserted; 10-02 moved 2026-10-05 05:3x by seat 8e88f5e9 at the shift-change wrap, 1 row(s), conservation asserted; 10-01 moved 2026-10-04 05:30 by seat 73252fd5 at its 05:30 wrap, 8 rows, conservation asserted; 09-30 moved 2026-10-03 05:30 by the morning seat 73252fd5 at its 05:30 wrap, 9 rows, conservation asserted; 09-29 moved 2026-10-02 05:30 by seat 79817561 at its 05:30 wrap, 11 rows, conservation asserted; 09-28 moved 2026-10-01 05:30 by the evening seat cb6b682a at its 05:30 wrap, 6 rows, conservation asserted; 09-27 moved 2026-09-30 19:14 by the day seat cab52cfa at its rotation, 6 rows, conservation asserted; 09-26 moved 2026-09-30 00:05 by the overnight seat at boot, 10 rows, conservation asserted; 09-25 moved 2026-09-29 05:3x by the overnight seat at its wrap, 15 rows, conservation asserted; 09-24 moved 2026-09-28 05:3x by the overnight seat at its wrap, 2 rows, conservation asserted; 09-23 moved 2026-09-27 05:3x by the 09-26 evening seat at its wrap, 19 rows, conservation asserted; 09-22 moved 2026-09-26 at the 05:30 shift-change wrap, 28 rows, conservation asserted; 09-21 moved 2026-09-24 05:3x by the 00:00 seat at its wrap, 22 rows, conservation asserted; 09-19 moved 2026-09-22 07:22 by the 03:45 seat at its rotation handover, 15 rows, conservation asserted; 09-18 moved 2026-09-22 03:3x by the 00:05 seat at its rotation handover, 20 rows, conservation asserted (1192 == 1192); 09-17 moved 2026-09-21 00:50 by the 23:4x seat at its 70% checkpoint, 37 rows, conservation asserted; 09-16 moved 2026-09-20 03:5x by the 03:3x Sunday seat at its 50% checkpoint, 55 rows, conservation asserted (1104 = 1104); 09-15 moved 2026-09-18 10:0x; 09-14 moved 2026-09-17 05:10 by the 05:03 seat at boot, 28 rows, conservation asserted; 09-13 moved 2026-09-16 00:49 by the 00:1x seat at its checkpoint, 24 rows, conservation asserted; 09-12 moved 2026-09-15 11:08 by the 05:3x seat at its wrap, 12 rows, conservation asserted; (09-10 moved 2026-09-13 22:1x by the 17:48 seat, 76 rows, conservation asserted; 09-09 moved 2026-09-12 10:4x at the 09:15-rotation seat's 70% checkpoint under rule 3c, 112 rows, conservation asserted; 09-08 moved 2026-09-11 05:3x; 09-07 moved 2026-09-10 05:3x at the overnight wrap under CLAUDE.md rule 3c, 71 rows, conservation asserted; 09-06 moved 2026-09-09 12:5x; 09-04 moved 09-06 08:0x; 09-03 moved 09-06 00:06; 09-02 moved 09-05 08:1x; 09-01+08-31 moved 09-04; ≤08-29 moved 08-31 and 09-02.)

**Fleet-insight and agent-credit rows dated ≤ 2026-09-05 live in [[_ledger_fleet_insights]]** (moved 2026-09-05 under WED-145 Phase 0; conserved, never deleted).

| Date | What happened (root cause) | Type | w | Lesson | Status |
|---|---|---|---|---|---|
