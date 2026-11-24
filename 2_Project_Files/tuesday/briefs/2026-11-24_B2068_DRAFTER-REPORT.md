STARTABLE: YES

# B2068 DRAFTER REPORT: OXPd M577 first-run row 2 (the Test service on, one panel screenshot, off again), seat X72

Drafter: in-session, read-only, Opus (claude-opus-5-5), for Tuesday s325. Drafted 2026-11-24 23:20 to 23:32 AEDT (`date` at 23:25:46 and 23:32:27). Commission: `tuesday/briefs/2026-11-24_B2067-B2068_OXPD-ECHO-AND-ROW2_DRAFTER_COMMISSION.md`, lane B2068 only.

**Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2068_SEAT-X72_oxpd2-m577-row2-test-service.md` (50344 bytes at 23:32; 8 slot lines, S1 to S7 and the last line `READ-WHOLE-BY-TUESDAY: ____`). Sidecar: `...row2-test-service.md.measured`. `stamp_check.py <kit>`: rc 0, `137 claims, 137 measured, 0 not measured`.

## BLUF
- Startable: PR 48 (gate B2052 FOUND 1 to 3) has landed; main `217286f3` builds clean; the lab has all four Test service operations; the printer's discovery tree lists `OXPd:Test` at the path the lab sends to.
- The run makes at most 6 requests that carry the password, over 5 lab runs, plus one first contact that sends nothing. It writes only the Test service switch: the enable is sent only when the read says off, and the disable only when this run turned the service on. It finishes with `undo-owed`.
- **Guest or admin, measured from HP's text (`contracts/oxpd1/.../test.wsdl` at main):**

| Operation | Credentials HP accepts | Source |
|---|---|---|
| `IsServiceEnabled` | guest or admin | `:503` |
| `EnableService` | admin only | `:525`; guest refused `:535` |
| `GetScreenCapture` | admin only | `:369`; guest refused `:379` |
| `DisableService` | guest or admin | `:548` |

  The lab sends admin to all four.
- Two branches, chosen by what R02 reads:
  - **OFF:** enable, screenshot, disable. `undo-owed` should print `nothing is owed` (exit 0).
  - **ON:** write nothing, take the screenshot, leave the service on. `undo-owed` should exit 11 with `no undo list was read`, which is the correct result in this branch (Q3).
- **Gate: none, in my reading (Q1).** HP says the service "must be explicitly enabled after every reboot" (`test.wsdl:123`), and the run turns it off again before it ends. Nothing lasting is written to the device, and the local files are not committed.

## FACTS RE-MEASURED (instrument, control)
1. **Origin**, by `gh api -X GET` under the project's `GH_CONFIG_DIR` at 23:22:26:
   - main is `217286f321b1b5240856ffb15540f069775e9065`; open pull requests: 0.
   - PR 48 is `closed`, merged, with merge commit `f5882ed74275200ffd37ac998ee650ada0820241`.
   - `git merge-base --is-ancestor f5882ed 217286f` returns rc 0.
2. **Draft clone** (`clone.py draft`, in `fleet/state/s325/d2068/clone`): `HEAD 217286f3...`, `push URL: invalid://no-push`.
3. **Build** (through `heavy.py`):
   - Jobs: `d-restore: rc 0`, `d-build: rc 0`, lock waits 0, load1 2.07.
   - Build log: `0 Warning(s)`, `0 Error(s)`.
   - Working tree: 0 porcelain lines.
   - Lock: both folders were moved to my `_quarantine/locks/`, and `wave1-heavy.lock.d` was absent afterwards (checked with `ls`).
4. **Dry runs** of `oxpd1 write --write EnableTestService` and `DisableTestService` (built dll, `--addressing 2004`, B2044's pins), both rc 0:
   - Target: `POST https://npi5a4e46.local:7627/hp/device/webservices/OXPd/TestService`, with action `.../ITestService/EnableService` (or `DisableService`) and WS-Addressing 2004/08.
   - The enable's dry run printed its undo line: `... --write DisableTestService --execute`.
   - The disable's dry run printed `its undo: none (the device turns the Test service off at every boot)`.
5. **Local reads against 127.0.0.1 port 9** with a missing synthetic credentials file:
   - `--read IsServiceEnabled` and `--read GetScreenCapture` both exited 7 before any connection, so the lab accepts both names.
   - Control: `--read IsServiceEnabledX` exited 2 and printed the list of seven names.
   - `undo-owed` over a session of dry runs only printed `no undo list was read` and `not confirmed ...`, rc 11. This is the form the ON branch should show.
6. **The device's Test service**, read from B2044's saved page (`<project>/.tools/b2044/ews/m1/m07__DevMgmt_DiscoveryTree.xml.html`, 6119 bytes, read-only; I made no request):
   - `OXPd:Test` appears once (control `OXPd:DeviceInfo` also once).
   - Path `/hp/device/webservices/OXPd/TestService`, revision `test/2010/04/14`, MinorRevision `1.1`.
7. **Run-folder rule:** no folder from `<project>/.tools` up to `/` holds a `.git`, and none is a symbolic link (checked with `[ -e ]` and `[ -L ]`). Control: `<project>/2_Project_Files/.git` exists.
8. **R02 one-liner** (written into the kit), run on five synthetic files:
   - false and true files: `answer lines 1 | tags 2 | enabled: false` and `enabled: true`.
   - Controls, which all failed as intended: a child element gave `tags 4 | UNREADABLE`, the value `maybe` gave `UNREADABLE`, and a file with no answer line gave `answer lines 0`.
   - I extracted the one-liner from the kit text with `shlex` and re-ran it, so the kit's bytes are what was tested.
9. **Doc and toolchain:**
   - `docsecret.py --shape` printed `value length 9 | upper 1 | lower 7 | digit 1 | other 0`, `SHAPE OK`.
   - `test -f` on the doc: rc 0. I never opened the doc.
   - `.tools/dotnet/dotnet --version`: `10.0.404`.
10. **Tools:** the four copied files match by sha256 (`shasum -a 256`): clone.py `6dc83945`, heavy.py `31adedc8`, docsecret.py `1e2acce2`, lab_run.py `a295dfa3`. These equal kit B2044's THE TOOLS.
11. **Seat id X72 is free.**
    - In tuesday/briefs from 2026-11-17 to 11-24 (`.pre-` files excluded), whole-word search: X72 appears in 1 file (this commission) and X71 in 1 file (the same commission).
    - Control: X70 appears in 6 files.
    - In OXPd `Briefs/`, X71 or X72 appears 0 times; control X70 appears 2 times.
    - `tmux list-panes` shows no OXPd pane.
12. **No earlier row-2 run on the device:**
    - Exactly 1 STATUS file in `Briefs/` names the host (B2044).
    - `EnableTestService --execute` appears 0 times in it; control: the host string appears 8 times.
13. **Model:**
    - `models_latest.json` `levels.opus.model_id` is `claude-opus-5-5`.
    - `<project>/CLAUDE.md:7` says Opus; `model-routing.md:18` also says Opus (an override).
14. **Grant:** `EXPIRING-GRANTS.md:10` reads "OXPd agents may set the M577's local administrator password ... and set the printer up for the OXPd project", and covers "the printer needs list's section 2a, B1968". Row 2 is at `B1968:66`.

## D-DECISIONS (all are Tuesday's as coordinator; each is restated in the kit)
- **D1:** run a separate R02 read before any write (Q2).
- **D2:** in the ON branch, write nothing (Q3).
- **D3:** take one screenshot and never retry it. A C01 fault still runs the undo path, then the run ends STOPPED.
- **D4:** W03 is W02's printed undo, compared by program with W01's dry-run undo line.
- **D5:** pass the password through a named pipe.
- **D6:** use one fresh session folder.
- **D7:** the seat views `panel.png` once and writes one line. It stops if the panel shows a firmware, reset or wipe prompt, or a prompt for another password (Q6).

## QUESTIONS FOR TUESDAY (each has a default; Q2 and Q3 are STOP-CLASS and must be answered in words at S4)
1. **Q1, gate.** Default: no gate (a device run with nothing lasting on the device). Alternative: a read-only verifier over STATUS and the session folder.
2. **Q2, a separate R02 before the enable.** Default a: yes (6 password requests at most). Alternative b: let W02's own read decide (5 at most).
3. **Q3, the service found ON.** Default a: record it, write nothing, take the screenshot, leave it on, and accept U01 exit 11 as the correct end. Alternative b: stop at R02 and ask.
4. **Q4, addressing.** Default: `--addressing 2004` only, and an HTTP 400 is a STOP. Alternative: one 2005 try.
5. **Q5, pins.** Default: R01 first contact re-reads the pins (nothing is sent), and a change is a STOP. Alternative: skip R01.
6. **Q6, viewing the panel.** Default: the seat views it once. Alternative: only Tuesday views it.
7. **Q7, records.** Default: the next OXPd records pass writes the history entry. Alternative: a records step inside this kit.
8. **Q8, level, windows and pane.** Default: Opus, READY at Step 0 + 60 minutes, pane `Datasec/OXPd2-X72`, hard stop at S7.
9. **Q9, timing (report only; not in the kit).** Default: launch when stamped, even at night. A sleeping panel may give a dark capture; the kit does not count that as a fault. Alternative: hold the launch until daytime so the screenshot shows a lit panel.

## CHAIN INPUTS (every input exists at BASE or comes from an earlier step)
| Step | Inputs | Where they come from |
|---|---|---|
| 0 | the kit, the Stamp slots | Tuesday's stamp |
| 1 | the four tools; the origin; the checkout's three local git values; the doc's shape | `fleet/state/s322/d2044/seat-tools/` (exists, hashes measured); GitHub; `2_Project_Files`; the doc (`test -f` rc 0) |
| 2 | `<lane>` | Step 1 |
| 3 | dll, `lab_run.py`, session, printer | Steps 1, 1, 2; the printer |
| 4 | pins | Step 3 |
| 5 / 6 | branch, pins | Step 4 (W02's already-on line moves to Step 6), Step 3 |
| 7 | lane | Steps 1 to 6 |

## UNMEASURED (named in the kit as limits or NEVER RUN)
- Whether firmware `2510156_069175` answers `IsServiceEnabled` and the other Test operations at all. HP marks them as OXPd 1.7, and gate B2052 FOUND 10 leaves this open.
- Whether the Test service accepts WS-Addressing 2004. B2044 measured 2004 on DeviceInfo, Authentication and Authorization only.
- The executed-run output lines. I derived them from source (`Oxpd1Command.cs:791`, `:794`, `:898`, `:902`, `LabFiles.cs:187`, `Oxpd1Writer.cs:254`) and the lab's cells pin them against a stub, but I could not run them, because the only stub lives in the test project and I sent nothing to the device.
- The real capture's size against the bound. Gate B2052 measured the bound at about 780,000 bytes saved and 790,000 refused.
- How a capture looks when the panel is asleep.
- What the device does with a disable sent to a service that is already off. The kit never sends one.
- Whether R03's HTTP 400 at the first run counted toward the device's lockout. It was not a refused password.

## STOP-SEVERITY CHECKS RUN ON A PROTOTYPE
- **R02/R04 `enabled` one-liner:** PASS on synthetic false and true. Its controls failed as intended (child element, bad value, no answer line).
- **The B2052 rule ("a shape outside HP's schema writes nothing")** is the lab's own and was not re-run by me. It is relayed from gate B2052 and covered by PR 48's cells.
- **Never run on a real output:** the comparison of W02's undo line with W01's, and the `file`/`stat`/`shasum` check of `panel.png`. If either fails, the kit routes it to `STOPPED: NEEDS TUESDAY`.

## OUTSIDE THE FENCES (disclosure)
1. **The two heavy jobs wrote briefly into the project tree.** `heavy.py` took the shared lock by `mkdir` of `<project>/.tools/wave1-heavy.lock.d` for each job and moved the folder into my scratch (`fleet/state/s325/d2068/_quarantine/locks/`). This is B2044's drafter form; no other holder was present. Nothing else was written in the project.
2. **I wrote lab run folders outside my commissioned scratch path.** The lab refuses a run folder inside a git work tree (exit 9), and the TUESDAY tree is one. So the dry and local run folders went to the session scratchpad: `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/344b75d7-2239-4c38-b831-23dec3b1795c/scratchpad/d2068-session` and `.../d2068-session2`. They hold only `summary.txt` files from dry and local runs. No secret was involved: the credentials file named was a missing synthetic path.
3. **I read the doc's shape once.** `docsecret.py --shape` reads Kam's doc in-process and prints lengths only. I did not print, copy or write the value.
4. **I read inside another lane's folder, read-only.** I read B2044's saved discovery-tree page in `<project>/.tools/b2044/ews/m1/`, and listed the folder names of `.tools/b2044/` and its `session/` folder.
5. **Nothing reached the printer, GitHub (GET only), Jira or the card store from me.** No `cd`, no deletion.

READ-ONLY toward the project, GitHub and the printer, except item 1 above.
