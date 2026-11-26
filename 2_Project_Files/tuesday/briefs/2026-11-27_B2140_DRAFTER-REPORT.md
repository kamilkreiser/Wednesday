STARTABLE: YES

# B2140 DRAFTER REPORT: the OXPd records pass for the landing of PR 57 (lane OX-C kit 1, the other modules' hygiene), a kit for seat R338

I am the in-session, read-only drafter for Tuesday s332. `date` printed my first clock as `Fri 27 Nov 2026 09:35:43 AEDT` and my last as `Fri 27 Nov 2026 09:53:44 AEDT`. No slot in the kit holds a typed clock. Every MEASURED-BY-DRAFTER clock in the kit is a `date` print or a GitHub timestamp converted to AEDT by `zoneinfo`.

Files written (nothing else outside my scratch):
- **The kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2140_SEAT-R338_oxpd2-records-pr57.md`
  - sha256 `e32536f4...`; 113489 bytes; 345 lines; 0 bytes above 126.
  - 8 lines are over 2000 characters: 1, 14, 17, 155, 156, 195, 280 and 292.
  - 11 slot lines are left unfilled (10 slots plus the last line).
- **Its sidecar `.measured`:** 138 claims, 0 TODO. `stamp_check.py <kit>` returns rc 0.
- **This report.**
- **Scratch:** only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s332/d2140/`. The kit's source with placeholders is `kit.src.md`; `fillkit.py` fills it.

## BLUF
- **Seat id R338 is free.** It is named in 0 of the 25 SEAT kits of 11-26 and 11-27, and in no file name. Controls: R337 is named in 3 kits and R336 in 3.
  - Panes at 09:39:57 and again at 09:53:36: `%0 tuesday`, `%375` and `%376` (both unnamed). None holds `OXPd2`.
  - The next OXPd build kit, B2138 (seat X81), names this records pass as its precondition. Launch only one of the two at a time.
- **The landing.** PR 57 merged at 2026-11-26T22:34:37Z, which is **09:34:37 AEDT on 2026-11-27**, so every text dates the landing 2026-11-27.
  - Squash 0ca8c655 has one parent (38a031e5). Its tree is 7ec27cb9, the same as head 641935b5's tree.
  - 10 files, all modified, +147 and -24. The list equals `landing.txt` lines 22 to 31 compared as a whole list.
- **What the kit writes.** It follows the form of B2132.
  - **C-92**, a Tuesday's note. It records two coordinator choices:
    - The revocation-mode line was dropped, and revocation stays off through the chain policy. It says outright that this does not decide whether a device certificate is ever checked for revocation.
    - The one unfinished whole-solution run was read as a one-off under ANSWER-1's control rule.
  - **Five ticks in place**, each with a `Closed:` line: 77, 119, 120, 122 and 131.
  - **One evidence line under 137**, with no tick. It copies the only precedent, owed item 33's `Evidence added by the records pass` line at BACKLOG line 224.
  - **Two new items:**
    - 159 = FOUND 1 together with H9: a re-issue or a forget done by another process is not seen by a running host.
    - 160 = the landing's other record points, including FOUND 3 to 7 and the PROPOSED 2 tool note.
  - **One history entry, one comment on OXPD2-1, no ticket.** 84 stays open and gets no line.
- **Product owner: no ruling of his bears on this pass.**
  - His board read at 09:40:57 for 2026-11-27 shows two rows, both at 06:44: a tap on the day's plan and a tap on a usage card. Neither is an OXPd ruling. TAPPED-BUT-OPEN is none.
  - His newest OXPd ruling is still 2026-11-25 14:30.
- **Main's push run at 0ca8c655 was re-measured** (run 45905675926). My byte copy of `hosted3.py` (sha256 969fe376), run with `--wait` from 09:38:58 to 09:39:06, printed `HOSTED 0ca8c655...: PASS` at total 2429 and rules 679. The control at `--total 2430` printed `FAIL 4`.
  - At 09:44:41 the check runs read 7 of 7 success, including Analyze (csharp), which was still running at 09:38.
  - Main's analyses at 0ca8c655 read results 0 for each of csharp, actions and python. The next three rows are at 38a031e5 (the control).

## Facts re-measured (instruments)
- **GitHub** (`gh api -X GET`, the project GH_CONFIG_DIR, account kamilDatasec), read by `ghreads.py`, `logs.py`, `facts2.py` and `hosted3.py`:
  - **Main.** `commits/main` is 0ca8c655, subject ending `(#57)`. It was re-read at 09:53:36 and is unchanged.
  - **Pull requests.** `pulls/58` and `issues/58` are 404, 0 PRs are open, and the newest are 57 to 53.
  - **Events.** merged and closed, both at 22:34:38Z.
  - **The landed message.** The subject equals `squash-subject.txt` with `#57` (True; the `#56` control is False). The body equals `squash-body.txt` without its final LF (True; with the LF it is False).
  - **The PR run** 45905000610 holds `HEAD is now at 5e24c9c Merge 641935b5… into 38a031e5…` once in each of its 4 logs. Control: `Merge 38a031e5` on 0 lines.
    - linux: `total: 2429` ×2, `succeeded: 2425`, skipped 4, GUARD 14.
    - windows: `succeeded: 2408`, skipped 21, GUARD 15.
    - RULES 679, `Ran 117 tests`, floor 117/117, `no leaks found` ×3.
    - `Datasec.Suite.{Graph,Server,Adapters.Oxpd2}.Tests.dll (net10.0|x64) passed` on 2 lines each, on each leg. `failed Datasec.` is 0.
  - **The push run at 38a031e5** (45823255997), linux log: `total: 2422` on 2 lines. Control: `total: 2429` on 0. 2422 + 7 = 2429.
  - **Blobs.** All ten paths changed between 38a031e5 and 0ca8c655, and each new blob equals the tarball's git blob.
    - Unchanged: CallbackCredentials.cs, CsaStore.cs, DeviceAuthCellTests.cs and HttpIppTransport.cs.
    - The line `CertificateRevocationCheckMode = X509RevocationMode.NoCheck` goes from 1 line to 0. `LoopKey(` goes from 0 lines to 3.
- **Tarball of 0ca8c655** (1777315 bytes, 679 files): `facts.py` read POINTERS 45 of 45, and the one-line-off control FIRED.
- **Project:**
  - All nine files equal `.tools/b2132/READY.manifest`: CLARIFICATIONS dca1f3ad, BACKLOG ba8ab83e, history 9a1edb62, CLAUDE 0f1fccc0, QUESTIONS_BY_OWNER 06b484a2, HP_QUESTIONS_DRAFT 845ec7c8, deviation register e2621f1b, 02_architecture 7ca385fe, 03_plan 389c4c53.
  - B2132 READY is 1665ca86 and B2134 READY is 641935b5.
  - Owed items run 1 to 158: 92 open, 66 ticked. Blocks 77, 119, 120, 122, 131, 137 and 158 are each 7 lines ending in `Discovered:` (`blocks.py`).
  - Item 86 (line 628) already names the re-issue half as DERIVED.
- **Jira** (GET-only fence; POST, PUT, DELETE and PATCH were refused in-process):
  - The census is 63. Done: 33, 39, 41, 47.
  - OXPD2-1 has 18 comments; the newest is 41525, which starts `Records pass after pull request 56`.
  - All 10 phrases return 0 issues. The 5 controls fire.
- **Dry build** (`dry.py`; the frozen table re-parsed from the written kit is byte-equal to the one from the source):
  - CLARIFICATIONS: 1228 to 1236, C-92 at line 1230.
  - BACKLOG: 1192 to 1212. Added 20, changed 5. Removing by position and un-ticking gives back the old bytes.
    - Open 89, ticked 71.
    - `Closed: ticked in place` goes from 63 to 68; `Evidence added` goes from 1 to 2.
    - The anchor moves from 1177 to 1197.
  - History: 402 to 410.
  - `scan_record` finds 0 problems on 31 lines. J-1 has no `scan_jira` codes, and its ADF read-back is EQUAL.
  - 0 doubled words, 0 doubled groups and 0 repeated runs of 12 or more characters. All three controls fired.

## D-decisions (drafter's)
- **D1 (form).** B2132 is the form. The evidence-line shape comes from owed item 33's line 224, the only precedent.
- **D2 (each frozen claim checked against its source line).** Every sentence was checked. Corrections made before freezing:
  - **BL-160, "HTTP/1.1".** The doubled-group check tokenised it as `1 1` and fired, so the text now reads "the request on the wire".
  - **BL-160, the second orphan.** It said "another seat's clone"; it now says "an earlier review's clone", because FOR-RECORDS names a gate's clone.
  - **P-4 and P-8 prefixes.** Those holding inner backticks were shortened to prefixes without backticks.
  - **The final-LF clause.** A claim about B2132's seat that I had not read at source was removed.
- **D3 (119 ticked whole).** 119's own symptom is single-process, and the review found it true on every single-process path. FOUND 1 is multi-process, a new reach of the same cache, so it goes to item 159.
- **D4 (FOUND 2, the hang).** It goes to 137's evidence line, not to item 160.
- **D5 (no names or card ids in the kit).** None appear. His board rows are described in words only.
- **D6 (the date).** The landing, Discovered and Source dates are all 2026-11-27, by `zoneinfo`.

## Chain inputs
| Step | Inputs | Source |
|---|---|---|
| 0 | kit, sidecar, project files, df, python3 | BASE |
| 1 | the `b1785.py` copy, scratch copies | Step 0 |
| 2 | SOURCES, GitHub, tarball, job logs, Jira GETs, B2132/B2134 STATUS | BASE (origin) |
| 3 | frozen texts, C-number (P-7), BL-OLD8 (before-copy), BL-NEW8 (dry BACKLOG) | Steps 0, 2 |
| 4a | live CLARIFICATIONS, filled C-92 | Step 3 |
| 4b | live BACKLOG, 5 ticks, 5 Closed lines, BL-EV-137, BL-159/160 | Step 3 |
| 4c | filled J-1 (C-92 from Step 2) | Step 3 |
| 4d | live history, BL-OLD8/NEW8 (4b), CMT-1 (4c), C-92 | 4b, 4c |

## Q-questions for Tuesday (defaults as written in the kit)
- **Q1: C-92 as a Tuesday's note with both choices.** Default: yes.
  - (a) No C-entry.
  - (b) Keep only the revocation choice.
- **Q2: tick 119 whole, with FOUND 1 filed as 159.** Default: yes. Alternative: a `Closed in part` line under 119, which forces a re-draft.
- **Q3: 137 gets one evidence line in item 33's form, and its first line ("seen once") is not edited.** Default: yes. Alternative: a clause of 160 only.
- **Q4: FOUND 1 and H9 become one item 159, which names item 86's derived clause.** Default: yes. Alternative: an evidence line under 86.
- **Q5: FOUND 7 / PROPOSED 2 (the mutant tool leaves the last mutant's build) becomes a clause of 160.** Default: yes. Alternative: its own item, which makes the landing item 161.
- **Q6: all other notes go to 160.** Default: yes.
- **Q7: one comment and no ticket.** Default: yes.
- **Q8: no line under 84, 86, 121 or 138, and CLAUDE.md is not edited.** Default: yes.

## UNMEASURED / NEVER RUN
- **Never run:** the seat's helper and selftest, HOLD R and R2 on the live files, the live ticks and the evidence insertion by position, and the POST.
- **RELAYED, not measured by me:** every probe, mutant and red/green count of the review and the seat (macOS arm64). I did not open the four `.tools/b2134/logs/` files named in BL-EV-137; I only confirmed their names with `ls`, with `red-graph.log` as the control.

## Outside the fences (disclosure)
- **Board read.** `kam_rulings_today.sh 2026-11-27` ran once, with `KAM_READ_MARKER` pointed at `d2140/kam_read_marker`. Only the first 40 characters of each row went to my session, and nothing was saved.
  - Two card-id prefixes showed in my session. Neither is written to any file.
  - `kam_msgs.sh` was not run, and no card was read.
- **hosted3.py.** I ran a byte copy (sha 969fe376) twice, GET only. It wrote job logs into `d2140/hosted-main*`.
- **How the kit and sidecar were written.** The kit was put in place with `cp -n` from `kit.out.md` (`cmp` equal). The sidecar was made by `stamp_check.py --init`, then `cat` of `side.out` (`cmp` equal). I did not use the Write tool for these two files, because the kit is 113 KB. Only this report was written with the Write tool.
- **Commands I ran.** I ran `find -maxdepth 4` over Tuesday's own `2_Project_Files` to locate the board reader. I ran `ls` (no recursion) on `.tools/b2134/logs/`.
  - One Bash call held a stray harmless `cd_dummy=1` assignment. No `cd` was run.
- **No write anywhere else.** Nothing was written to the project, Jira, GitHub or the card store. Nothing was deleted. Nothing went to any human or device.
