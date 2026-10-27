STARTABLE: YES

# B807 drafter report (Sonnet drafter, 2026-10-27 about 10:3x-10:5x AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B807_SEAT-M20_nexusai-measure-890-891-884-893-and-c57-tool.md` (145 lines). Shape copied from the B798 kit (NexusAI-M19, read whole) and its drafter report. Seat `Datasec/NexusAI-M20` (form `Datasec/NexusAI-M<n>` as M19), ports 8930-8939, launch line carries `BRIEF_SEAT_LEVEL=sonnet`.

## BLUF
Startable now. One seat, two lanes, no branch, no commit, no push, no PR. N-MEASURE: four measurements (RD-890 census, RD-891 step 1 race, RD-884 step 1 records read, RD-893 (2) local stand), each posted as ONE Jira comment (the kit's only Jira write, Step 7 after a clean check). N-TOOL: `session-tools/c57-id-superset.sh` line 38 repointed to the lock tool's own default, with a scratch-base red-then-green arm, `.pre-rd886-<UTC>` quarantine copy beside it, atomic `mv`, no gate (your ruling on card candidate 4).

## Facts re-measured (instrument; control)
- Ports 8930-8939: `lsof -nP -iTCP:8930-8939 -sTCP:LISTEN` empty (rc 1; I did not run the bind-and-free control, the kit tells the seat to). Word-boundary scan `893[0-9]` by `python3 -I` over 100 non-`.pre-` SEAT kits of 26-27 Oct: 0 hits (control: `8840` hits 2 kits). Pane list 10:3x: tuesday, HPSM-POC-D37, MPS-R57, NexusAI-G169, HPSM-POC-H44, HPSM-POC-G168, fleet-monitor; no `NexusAI-M20`. load1 3.62 at 10:35. (I did not run a separate `NexusAI-M20\b` kit scan beyond the pane list; the first grep errored on a `{}` quantifier and printed nothing. UNMEASURED.)
- Tickets (Jira GET through `b774lib.py`, in-process): RD-890, -891, -884, -893, -886 all To Do, all 0 comments. Done-when clauses quoted in the kit from the descriptions.
- c57 file: line 38 reads the T9 default, comment lines 36-37 say "stays on the T9 (RD-847), written out"; guard exits 64 unless the lock owner pid is self or an ancestor; real work starts at `A="$1"` (line 51). Four older `.pre-` siblings exist (naming `.pre-<tag>-<UTC compact>`). Control: gate B706 STATUS lines 98/123/124/129 agree (KK_T9 count 1 at line 38).
- Lock tool: line 84 default is `.../session-tools/locks-laptop-1017`, line 61 comment records the move (2026-10-25, RD-847); sha256 `cf01bafb...971f` (equal to B798's). **Finding:** project `CLARIFICATIONS.md` has no entry for the RD-847 base move (`grep laptop-1017` prints nothing; C-63 at :589, C-110 :1109, C-114 :1174 are the lock-rule sources I quote). The records seat owes it (B706 line 129). The live lock directory `locks-laptop-1017/` held a lock at 10:34 (gate G169); the kit forbids touching it and builds the arm on a scratch base.
- Model: `model-routing.md` rows read lines 85-111: no row names a read-only measurement seat. Kit cites C2 (:92) and C8 (:98) as nearest, Sonnet column; id `claude-sonnet-5-5` from `models_latest.json` (grep read it among four ids). Gate after: none (your ruling).
- Kit self-checks: lines with four underscores = 9 (8 slots + last line); `@[A-Z_]+@` = 0; non-ASCII bytes 0; no person's name (I removed one from a quoted routing row); no decision-card id.

## D-decisions (mine, for you to overrule)
- D-1 Read-only detached clone `worktrees/b807-measure` (no branch, no commit) so the seat can read main and boot the stand; the shared checkout is stale.
- D-2 RD-891: `race.js` is READ, not run (it may write `/tmp/printer-dashboard-data`). The seat measures with an `fs` preload that records and refuses any write under that path, with a control, and compares the directory's mtime before and after. The sequential control must read 0 or the run is invalid.
- D-3 RD-893 stand: allowlisted environment (`env -i`), no Azure variable, own temp data dir, own port from the block, loopback only. Measurement (1) (Log Analytics) is explicitly not done.
- D-4 RD-884: records read only; no docker/az/registry. "None found" is a valid verdict.
- D-5 N-TOOL arm in two parts: a string arm (c57 default equals the lock tool's default; exact default once, `KK_T9` zero) and a behavioural arm on a scratch lock base with `NEXUSAI_LOCK_BASE` unset, cutting a scratch copy of the script before `A="$1"` so nothing after the guard can run. If the OLD file does not refuse in the red run, STOP.
- D-6 Fix also replaces the stale comment lines 36-37 (otherwise the comment would contradict the new default); diff limited to lines 36-38.
- D-7 No Jira comment on RD-886 (your "only Jira write" is the four measurement tickets); its record is STATUS.
- D-8 Time guidance relative: READY 90 min, HARD STOP 2.5 h.

## Questions for Tuesday (each with a default)
- Q-1 Model row: no routing row fits a read-only measurement seat. Default: Sonnet, C2/C8 cited as nearest. 
- Q-2 Does the Jira comment on RD-890 carry the whole 9-row table? Default: yes (it is the ticket's Done-when).
- Q-3 The seat runs `npm ci` and a stand without the jest lock (no jest involved). Default: no lock ticket; the kit says STOP if jest turns out to be needed.
- Q-4 Stamp the c57 file's sha256 at launch (I did not record it). Default: you stamp it from `shasum -a 256` before launch.
- Q-5 Launch timing. Default: launch now (load1 3.6; no shared path with G169).

## UNMEASURED
The 37 and 9 counts; the race on this machine; whether the constructor fallback writes under the shared directory; what the stand answers; any earlier registry-build record; the c57 file's sha256; whether `jira-adf.py` `doc()` accepts the comment shape; whether the scratch arm reproduces the false refusal; the Linux runner and node 24; the NexusAI main sha at launch (sweep read `ce8c33a6` at 09:30).

## Outside-the-fences disclosure
- Wrote only the two files above (plus one in-place Python edit of the kit to drop a person's name from a quoted routing row and fix "seven" to "four"). No Artifact, Docs, mail or chat tool. No `cd` (one command was refused by the hook at the start; nothing ran).
- Read: DRAFTER_RULES.md, the 09:30 sweep, the B798 kit and report, NexusAI `CLARIFICATIONS.md` by grep, B706 STATUS by grep, `c57-id-superset.sh` lines 1-80, `nexusai-lock.sh` header and grep of lines 61/84, `model-routing.md` lines 80-112, `models_latest.json` (grep), `b774lib.py` and `jira-adf.py` heads, directory listings of `session-tools/` and `locks-laptop-1017/` (names only).
- Jira: `get` and `adf_texts` of `b774lib.py` only, loaded in-process (it reads the project `.env`; no token printed). No write.
- `lsof`, `tmux list-panes`, `uptime`, one `python3 -I` kit scan (read-only). No gh call, no git verb, no HTTP to any hosted host, no az/ssh/docker, no `decision_queue.sh`, no staged briefs, scoreboard, `_ledger.md`, WEDNESDAY or FRIDAY tree.
