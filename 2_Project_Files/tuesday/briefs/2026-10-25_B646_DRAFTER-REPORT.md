# B646 DRAFTER REPORT (Sonnet 5.5 drafter, 2026-10-25 08:39-08:44 AEDT, clock `date`)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B646_SEAT-J13_composer-90-round2-wait-rows.md` (157 lines; 8 stamp slot lines + the last line = 9 lines with four underscores, MEASURED-BY-DRAFTER 08:43:20 by `/usr/bin/grep -c`; non-ASCII lines 0, 08:43:23; name hits 0). Ran nothing in the project: read-only git (`ls-remote`, `show`, `diff`, `log`, `cat-file`), `gh api -X GET pulls/90`, `lsof`, `tmux list-panes`, `ls` of `.tools` names, `/usr/bin/grep`.

## Facts (marks)
- MEASURED-BY-DRAFTER 08:39:09: origin `git@github.com:datasecau/Datasec-Security-Composer.git`; branch = `refs/pull/90/head` = `7b2b238672a7180f1710d085827bbc8fb14b3775`; main `e019ac3abf62` unmoved; #89 head `577e31d7da43`; #88 head `2da99cabb014`. 08:40: `pulls/90` open, draft false, mergeable true, clean, 2 files, +28 -4. `git log e019ac3a..7b2b2386` = 7f736c90, 7b2b2386.
- MEASURED-BY-DRAFTER 08:39: b116 file at the head, lines 72-112 (helper 78-93, `await untilVerdictBanner();` at 111, `VERDICT_DEADLINE_MS` 79, 3 rows at 115/128/139); s47 diff = +3 -0, class-limit comment at lines 15-17 of my read at offset 240.
- MEASURED-BY-DRAFTER 08:40:26: `lsof 9970-9979` rc 1; word-scan of `briefs/2026-10-2[45]_*SEAT*` for `997[0-9]` = 0 files. 08:39: 9930-9939 held by B643's brief (MPS-G105), 9940-9949 by B644 (Tuesday corrected to 9970-9979 mid-draft).
- MEASURED-BY-DRAFTER 08:39: panes `tuesday`, MPS-G105, NexusAI-M8, Security-Composer-J12, MPS-M20, fleet-monitor (G104 not listed; its verdict was written 08:35).
- MEASURED-BY-DRAFTER 08:40: `.tools/b631/scripts` holds common.sh, file.sh, groups.sh, heavy.sh, inter.sh, matrix.sh, mut.py, names.py, props.py, stab.sh, unit.sh (names only, not read).
- RELAYED: all gate measurements, from `B640_STATUS.md` (lines cited in the kit).
- UNMEASURED: see the kit's last section.

## Decisions
- D1 Settle design: keep the state wait; add a wall-clock settle window after the verdict (act turns until now > start + 100 ms, plus one extra turn) rather than "N more turns", since a turn count is the same flaw class as the original loop. Absence of a late rejection cannot be awaited as a state, so a window is stated honestly as such.
- D2 `VERDICT_SETTLE_MS` = 100: covers the sweep (old killed up to ~20 ms; 40 ms missed by both) with margin; ~0.3 s per file.
- D3 Pin (B640-3): pure `deadlineFitsTimeout(deadline, settle, timeout)` with margin 1000 ms, a control row (6000 false, 3000 true, boundary) and a real row reading the configured timeout (`vi.getConfig().testTimeout` as an unverified lead). Mutants W7, W7b, X6, X7 must be red by name.
- D4 No in-file row for B640-1 (a late rejection row would itself trip vitest's unhandled-error net); its proof is the Release.tsx R-after cells in `wt-b646-mut`.
- D5 B640-2: comment reworded to a measured blind window (suggested ~49,000, three pieces of 16,384) or the property; the seat re-probes P-win16k/32k/64k itself, not copied. "passed the old file too" replaced by "the file before B301" per the gate.
- D6 B640-4: recommended not taken (W8 would need a `console` spy, which hygiene forbids; S1 message-only; S4 type-only); the seat must state its choice.
- D7 Extra tree `wt-b646-old` at main for OLD-file comparison runs. Read-only script sources limited to six named files of `.tools/b631/scripts`; mutant drivers (`mut.py`, `matrix.sh`, `props.py`) forbidden, seat writes its own. Fences name J12 (B641), G104 (B640), G98 (B626), J10 (B627), B643, B644 by path and port from both sides.
- D8 Round 2 of 2: replays are the gate's own R-after cells; kit forbids weakening and requires closing every reachable survivor now.

## Open questions for Tuesday
- Q-1 Is `.tools/b631/scripts` (built for the main-based web route) acceptable as the copy source, or should the seat build its own from scratch? (Kit allows a fallback; I did not read the files.)
- Q-2 Is 100 ms settle acceptable, or do you want a larger window (e.g. 250 ms) given load variance? Measurement by the seat will decide margin; a bigger window costs ~0.75 s a file.
- Q-3 Should the b84-web-lows five-turn wait (lines 466-470) get a ticket now, since it carries the same weakness? Kit only reports it in FOR TUESDAY.
- Q-4 Hard stop: I suggested READY 2.5 h / hard stop 4 h, no later than 13:00; adjust at stamp.
- Q-5 Whether `vi.getConfig().testTimeout` exists in vitest 5.0.0 is UNMEASURED; kit lets the seat choose the accessor or STOP with one question.
