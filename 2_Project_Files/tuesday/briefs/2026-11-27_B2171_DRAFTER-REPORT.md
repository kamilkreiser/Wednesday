STARTABLE: YES (X85's STOPPED line with `nothing is owed` is in place; no device seat live at 19:04:31; the kit refuses at Step 0 otherwise)

# B2171 drafter report: kit `2026-11-27_B2171_SEAT-X88_oxpd2-echo-and-forwarder-r2.md` (in-session read-only drafter, Opus, for Tuesday s334)

Clocks by `date`: first `Fri 27 Nov 2026 19:00:38 AEDT`; origin read 19:02:20; harness 19:04:10 to 19:04:22; tools sha 19:05:42; local facts 19:05:47; prior-work counts 19:09:43; stamp_check rc 0 at 19:10:52. Kit 196 lines, all ASCII; sidecar `.measured` 104 claims, 104 measured. Scratch `<d>` = `fleet/state/s334/d2171/` (`seat-tools/`, `orig/`, `test/`, `gen/`, `_quarantine/`).

## BLUF
1. **The fix is a seat-tool change, no lab change, and it is proven on a fake lab only.** New `lab_run_env2.py` (sha `460b8ac7...d79d`) is X85's `lab_run_env.py` (sha `7d97985b...f1ab`) with ONE change: `@GUEST@` becomes a regular file `<lane>/guest/<label>.cred`. The file is made with O_EXCL and O_NOFOLLOW, mode 600, and holds one line `OXPD_TEST_PRINTER_GUEST_PASSWORD=<16 hex>`. It is moved to `<lane>/_quarantine/guest/` after every end, a kill included. The admin `@CRED@` pipe is unchanged. Diff: `<d>/gen/lab_run_env2.diff`.
2. **Hang reproduced, then fixed** (`<d>/test/harness-run1.out`, 9 cases). The fake lab opens the file twice, as `Oxpd1EchoVerb.cs:288` -> `LabFiles.cs:57` and then `:296` -> `LabFiles.cs:34` do. The second open is bounded at 10 s. With X85's tool unchanged it printed `pipe: read` and then `HANG ... blocked 10 s`, which is X85's E01. With the new tool: exit 0, both opens read the same 16-hex value, and the file was quarantined as `-rw------- 50`. The admin pipe still read once. `@CRED@` given to the echo got exit 12. Both words got exit 2. A leak got exit 30 (file still quarantined). A kill path quarantined the file. An existing quarantine target left the file in place.
3. **Kit shape, per the commission.** Part A runs first, all direct to `192.168.8.157`: R01D, R02D, the Test service on only if off (W21A/W22A), E01 sync guest, E02 async guest with the listener on `<mac>:18627`, then W23A (the printed undo) and R04A. Part B is B2169's forwarder test: F01, R01F, R02F (with R04A as its direct control), W21B/W22B on `<via>`, E01F, E02D (`:18631`), E02F (`:18632` through `fwd.py`), W23B, R04B, F02, then U01. Part A's outcome sets Part B's legs. The first line says the kit SUPERSEDES B2169.
4. **The precondition is changed as commissioned.** X85's last line must start `STOPPED: NEEDS TUESDAY E01 hung` and hold `undo-owed nothing is owed`. The B2169 X88 lane or STATUS being present is a REFUSE.
5. **At most 10 admin requests** (12 with the D5 fallback); X85 used 10. The grant does not widen the kit. Every write is undone inside its own Part.

## Facts re-measured (instrument, clock)
- Origin `main` `760e1a644ce9a419cf1b9132d0776e9e5eac1cac`, open PRs 0 (`gh api -X GET`, project GH_CONFIG_DIR, 19:02:20). This is the sha X85 built. BASE tree: `fleet/state/s334/d2159-L9/src_760e`.
- X85 STATUS: 182 lines. In-process checks on its last line: startswith `STOPPED: NEEDS TUESDAY E01 hung` -> True; `undo-owed nothing is owed` count 1; control `row 3 is TAKEN` count 1. Its LAB lines ending `pipe: read`: 7 (6 admin runs plus e01).
- Absent (`ls -d`, 19:04:52): `.tools/b2169-x88` and `.tools/b2171-x88`. Briefs files matching `B2169_SEAT-X88|B2171`: 0 (control: `B2159_SEAT-X85` gives 2). The wave lock folder is absent.
- Ports (`lsof -sTCP:LISTEN`, 19:04:31 and 19:05:47): 18627, 18631, 18632, 7627 and 10443 each 0 lines (control: all listeners 15, then 25). Kit scan over the 40 non-`.pre-` SEAT kits of 11-26/11-27 in Tuesday's briefs (`grep -l -w`): 18627 appears in X85 and B2169; 18631, 18632 and 10443 appear in B2169 only; X88 appears in X85 (its stamp text) and B2169. Control `7627` gives 2. Live panes: `%0 tuesday`, `%375`, `%376`; no `Datasec/OXPd2-*` pane.
- This Mac (19:05:47): en0 `192.168.20.220`; route gateway `192.168.20.1` on en0; firewall disabled; dotnet `10.0.404`; load `2.16 2.53 4.52`; project root has no `.git`.
- Prior work over 120 OXPd Briefs `*STATUS.md` (`grep -l -F`, 19:09:43): `SyncEchoString: Answered` 0; `fwd.py` 0; control `EnableTestService --execute` 3; `e01-echo-sync` 1 (X85).
- Pointers by `awk NR==n` at BASE (`<d>/gen/facts.out`): Oxpd1EchoVerb.cs:20, 23, 253, 288, 296, 304, 320, 339, 351, 367, 372, 378, 388, 393, 402; LabFiles.cs:34, 57; README.md:35, 37, 144, 149, 208, 209, 319, 326, 331, 337; DeviceChannel.cs:54; Oxpd1Client.cs:69, 78, 86; Oxpd1Command.cs:20, 309, 358, 399.
- Model: `models_latest.json` line 17 `claude-opus-5-5`; `<project>/CLAUDE.md:7` is the Opus rule.

## Prototype checks (STOP-severity, run on my own output)
- REFUSE check on X85's last line: PASS (control fired: `row 3 is TAKEN` = 1).
- Guest file `stat -f '%Sp %z'` gave `-rw------- 50` on the synthetic quarantined file: PASS.
- Exit 12 when `@CRED@` reaches an echo: FIRED (h4). Exit 7 and exit -9 on a real echo: never run (fake only).
- Underscore-aware name scan of the kit for the product owner's names: 0 (control `_by_<name>_` fired 1 each).

## Chain inputs
| Step | Inputs | From |
|---|---|---|
| 0 | stamp; X85 STATUS (present) | Tuesday; X85 |
| 1 | five tools (exist); origin; credentials by name; B2068 kit; X85 `logs/r02-test-before.out` (exists, `ls`) | `<d>/seat-tools`; GitHub; `.env` (never read); Briefs; X85 lane (read only) |
| 2 | lane | 1 |
| 3 | dll, lab_run_env2, session, enabled.py | 1, 1, 2, 1 |
| 4 | branch, pins | 3 |
| 5 | E01/E02 outcomes, fwd.py, fwdlog, `<mac>`, free ports | 4, 1, 1, 2, 2 |
| 6 | forwarder, R01D pins, R04A text | 5, 3, 4 |
| 7 | `<via>`, leg, branch | 6, 5, 3 |
| 8 | pid, session | 5, 3 to 7 |

## D-decisions (Tuesday's defaults in the kit)
- **D1 precondition:** X85's STOPPED line with `nothing is owed`.
- **D2 direct controls:** R04A doubles as R02F's control, which saves one admin read.
- **D3 host:** the IP everywhere (X85 used the name).
- **D4 `<via>`:** E01F runs only through the forwarder, because on the direct host it would repeat E01.
- **D5:** the W23B direct fallback.
- **D6:** findings are not STOPs, but an echo exit -9 or 7 is.
- **D7:** no retry.
- **D8 guest file location:** `<lane>/guest/`, not the run folder. The commission said "in the run folder", but the lab refuses a run folder that already exists (`Oxpd1EchoVerb.cs:304` RunRecorder.Create, exit 5), so the file cannot be there before the run.
- **D9:** the Test service is cycled once per Part, so the printer is clean at the Part boundary.

## Q-questions for Tuesday (each with a default)
- Q1 (STOP-class) order: **a** Part A then Part B, legs set by Part A.
- Q2 (STOP-class) credentials: **a** admin pipe by name; guest as a mode-600 file through lab_run_env2.
- Q3 Test service: cycled twice (alternative: once around both Parts).
- Q4 keep E02D on 18631 beside E02F (alternative: drop it and use E02 as the control).
- Q5 REFUSED at R02F is a finding.
- Q6 the IP.
- Q7 the ports as assigned.
- Q8 names: lane `b2171-x88`, READY at +150 min.
- Q9 forwarder 5400 s.
- Q10 a hang again is a STOP.
- **Also for Tuesday (not in the kit):** the guest file sits in `<lane>/guest/`, not in "the run folder" as the commission worded it (D8). Default: accept.

## UNMEASURED
- Whether the real lab reads a regular mode-600 file twice without trouble. DERIVED: `File.Exists` plus two `File.ReadLines` on a regular file is ordinary, and the fake proves the tool side only.
- Whether the M577 answers either guest echo; the callback across subnets (owed 118); everything in Part B through the forwarder (B2169's UNMEASURED list stands).
- Whether the lab's `oxpd1-client.log` or summary holds the guest value. README:41-42 says the client scrubs the password. The value is random and harmless either way.
- The Test service by IP rather than by name: never run (X85 used the name). DERIVED to be the same device.

## Outside-the-fences disclosure
- **Writes:** the kit, its `.measured` and this report under `tuesday/briefs/`. Scratch under `fleet/state/s334/d2171/`: copies of 4 tools plus new `lab_run_env2.py`, `orig/lab_run_env.py`, the fake lab, the harness, synthetic `synth.env` (fake values), the harness lane, `gen/`. I moved one seat-tools copy of `lab_run_env.py` into `d2171/_quarantine/` and deleted nothing.
- **Reads:** X85 STATUS and X85 kit; B2169 kit, report and sidecar; B2068 files through fill.py counts; BASE source; the OXPd Briefs STATUS files (counts only); `ls` of X85's lane logs folder (names only).
- **Commands:** `gh api -X GET` twice; local `lsof`, `ipconfig`, `route`, `socketfilterfw`, `uptime`, `dotnet --version`; `tmux list-panes`.
- **Not done:** no device contact, no listener of any kind, no build, no lock, no `.env` read, no Source_Documents or key folder, no project write, no Jira, no GitHub write, no card, no mail.
