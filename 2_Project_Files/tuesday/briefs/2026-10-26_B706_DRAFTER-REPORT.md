STARTABLE: YES (after your stamp; one stamp decision: Q-1). Pane `Datasec/NexusAI-G132`, ports 9730-9739 (none bound), Sonnet.

# B706 drafter report - tier-2 gate of the installed lock tool (RD-847, builder B702)

## BLUF
Kit `2026-10-26_B706_SEAT-G132_nexusai-847-lock-tool-gate-tier2.md` (74 lines, shape of B697, adapted: no PR/CI/CodeQL/clone; instrument = sha256 pair, `diff` against the kept pre-copy, own arms on fresh scratch bases, own mutants G-M1..G-M6, `/bin/bash` 3.2, caller census, ONE probe ticket). Round 1 of 2 on class "the NexusAI lock tool's default base". Gate never edits, moves, replaces or rolls back; rollback recipe is quoted as text for you. Re-read at 07:06 AEDT after the account switch: nothing in the subject moved.

## Facts re-measured (instrument, control)
- Live tool sha256 `cf01bafb...971f` at 00:41 and again 07:06 (`shasum -a 256`); pre-copy `3c33f5ae...a792`; builder candidate = live; `current-lock.sh` = pre-copy; inode 186218638, 18894 bytes, 391 lines, `-rwxr-xr-x` 501:20. `bash -n` rc 0. `diff pre live` rc 1: `60a61` (1 comment) and `79c80,84` (new BASE line + 4 comments). Default is now at LINE 84 (kit says so; the builder kit's "line 79" is stale). `grep -c -F KK_T9` live 0 (pre-copy 1 = control).
- No `.new-847`, one `.pre-847-*`. `ls /Volumes` = Laptop-DEV, Macintosh HD, Recovery.
- Base: `queue-jest/` empty both times, no lock dir; `released/` 699 (00:41) then 701 (07:06; B703 live, one `b703` record seen).
- Panes 07:06: tuesday, Datasec/NexusAI-M13, Security-Composer-J18, MPS-G131, fleet-monitor. `NexusAI-G132` free (word-boundary scan over 155 non-pre SEAT kits of 10-24..26 hits only B703's mention of the gate and this kit; control `NexusAI-G128` hit 1).
- Ports 9730-9739: `lsof` rc 1 twice; scan hits B623, B624, B649, B677, B678 as prose only (B623/B649/B677 text read: "reserve"/"next kit takes"); control `x 9730 y` matched.
- Callers: 22 kits (at 00:4x) pinned `3c33f5ae`; by 07:06 B703 carries 1 `cf01bafb` line and 3 `3c33f5ae` lines (restamped; the kit tells the gate to read which). Load1 4.91.
- Model: `model-routing.md:109` row G2; `claude-sonnet-5-5` (`models_latest.json`).
- Round count: no earlier gate on this class. Checked: briefs-folder filter on `lock` (B702 listed = control, no gate kit); `CLARIFICATIONS.md` 0 lines with `RD-847`; STATUS files with `RD-847` = B702 only.
- Kit hygiene: stamp-slot lines 8 (7 slots + last line; control: expected by design), at-sign placeholders 0, non-ASCII 0, person names 0.

## D-decisions
- D1 Arms run COPIES of the live file, never the live path; the only live touch is one probe ticket tagged `b706-probe`.
- D2 Because B703 files real tickets, "base unchanged" is replaced by "no new `released/` entry with a b706 tag from the arms" (a listing equality would false-fail).
- D3 Builder's `props.py`/arms are readable but not run; gate writes its own (independence).
- D4 Added mutants G-M5 (`:-` to `-`) and G-M6 (derived default) beyond the builder's M1-M4.
- D5 Probe waits FIFO behind B703; at hard stop it is TERMed by its own pid and Check 5 becomes NOT TESTED (verdict capped).

## Q-questions for Tuesday
- Q-1 The probe ticket on the live base while B703 is live may wait through a long jest ticket (minutes to an hour). Default: allowed (S4 slot), gate hard stop 3 h, cap at GO WITH FINDINGS if unreached. Alternative: launch the gate when `queue-jest/` is empty.
- Q-2 The kit pins `cf01bafb` in launch checks and voids the gate if the hash moves. Default: yes.
- Q-3 B703's remaining 3 `3c33f5ae` lines: default is the gate lists them, not grades them.

## UNMEASURED
No arm, probe or copy of the tool was run by me; whether B703 holds a ticket at your launch; wall time of the arms; whether any process calls the tool without the variable (census is text plus the live process list at the probe).

## Outside-the-fences disclosure
None. Read-only commands only (`shasum`, `stat`, `ls`, `diff`, `bash -n`, `grep`, `lsof`, `tmux list-panes`, `uptime`); scratch lists in my session scratchpad; wrote only the two output files. Did not read the ledger, scoreboard, staged briefs, other trees, nor run `decision_queue.sh`.
