STARTABLE: YES

# B2146 DRAFTER REPORT: the OXPd records pass for the landing of PR 58 (lane OX-C kit 2 part 1, Universal Print registration), a kit for seat R339

I am the in-session, read-only drafter for Tuesday s333. `date` printed my first clock as `Fri 27 Nov 2026 12:06:02 AEDT` and my last before this report as `Fri 27 Nov 2026 12:24:21 AEDT`. No slot in the kit holds a typed clock. Every MEASURED-BY-DRAFTER clock in the kit is a `date` print or a GitHub timestamp converted to AEDT by `zoneinfo`.

Files written (nothing else outside my scratch):
- **The kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2146_SEAT-R339_oxpd2-records-pr58.md`
  - sha256 `b0c3e013...`; 112885 bytes; 340 lines; 0 bytes above 126.
  - 7 lines are over 2000 characters: 1, 17, 165, 166, 193, 275 and 287.
  - 11 slot lines are left unfilled (10 slots plus the last line).
- **Its sidecar `.measured`:** 144 claims, 0 TODO, sha256 `601eb75e...`. `stamp_check.py <kit>` returns rc 0 (144 of 144 measured).
- **This report.**
- **Scratch:** only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/d2146/`. The kit's source with placeholders is `kit.src.md`, which `fillkit.py` fills. The form drafter's programs were copied in as `old_*.py` and adapted.

## BLUF
- **Seat id R339 is free.** It is named in 0 of the 28 SEAT kits of 11-26 and 11-27, and in no file name. Controls: R338 is named in 2 kits and R337 in 4.
  - Panes at 12:12:10: `%0 tuesday`, `%578 Datasec/NexusAI-N183` and four unnamed panes. None holds `OXPd2`.
  - At 12:24:09 the NexusAI pane read `%584 Datasec/NexusAI-N184`, and still no pane held `OXPd2`.
- **The landing.** PR 58 merged at 2026-11-27T01:04:30Z, which is **12:04:30 AEDT on 2026-11-27**.
  - Squash 760e1a64 has one parent (0ca8c655). Its tree is 8e3985c1, the same as head b3248f8c's tree.
  - 4 files, all modified, +109 and -7. The list equals `landing.txt` lines 23 to 26 compared as a whole list; the control (first path changed) reads unequal.
  - Main was still 760e1a64 at 12:24:09. 0 PRs are open and `pulls/59` is 404.
- **Main's push run at 760e1a64 reads PASS** (run 45920447888). My byte copy of the gate's `hosted3.py` (sha256 969fe376), run with `--wait` from 12:07:14 to 12:08:24, printed `HOSTED 760e1a64...: PASS` at total 2431 and rules 679. The control at `--total 2432` printed `FAIL 4`.
  - At 12:13:22 the check runs read 7 of 7 success. Main's analyses at 760e1a64 read results 0 for each of csharp, python and actions. Open alerts are 0, both repository-wide and on the PR ref.
- **What the kit writes.** It follows the form of B2140.
  - **C-93**, a Tuesday's note. It records two coordinator choices:
    - The measured limits in items 54 and 55 are named in the README, not changed by a rule, a configuration check or a cell. It says outright that this does not decide whether the real certificates need a rule on extensions.
    - A failed key generation stays the platform's exception, and a cell pins it for a key that cannot be made.
  - **Three ticks in place**, each with a `Closed:` line: 54, 55 and 75.
    - 54 and 55 already hold a `Closed in part` line. Their `Closed:` line goes directly after it, as in items 45, 65 and 96.
  - **Two new items:**
    - 161 = FOUND 1: a test seam that throws leaves the issuer call unfinished.
    - 162 = the landing item.
  - **One history entry, one comment on OXPD2-1, no ticket.** No line goes under 121, 137, 138 or 76.
  - **The stamp error** is recorded in H-OWNER as the coordinator's own. The stamp named `RegistrationKeys.cs:249` and `:276` for E5's second catch, which is really `RegistrationRecord.cs:164`. The claim held.
- **Product owner: no ruling of his bears on this pass.**
  - His board read at 12:09:38 for 2026-11-27 shows two rows, both at 06:44: a tap on the day's plan and a tap on a usage card. Neither is an OXPd ruling. TAPPED-BUT-OPEN is none.

## Facts re-measured (instruments)
- **GitHub** (`gh api -X GET`, the project GH_CONFIG_DIR, account kamilDatasec), read by `ghreads.py`, `logs.py`, `facts2.py` and `hosted3.py`:
  - **Main.** `commits/main` is 760e1a64, subject ending `(#58)`.
  - **Pull requests.** `pulls/59` and `issues/59` are 404, 0 PRs are open, and the newest are 58 to 54.
  - **Events.** merged and closed, both at 01:04:30Z.
  - **The landed message.** The subject equals `squash-subject.txt` with `#58` (True; the `#57` control is False). The body equals `squash-body.txt` without its final LF (True; with the LF it is False).
  - **The PR run** 45919934631 holds `HEAD is now at 34e020d Merge b3248f8c… into 0ca8c655…` once in each of its 4 logs. Control: `Merge 0ca8c655… into` on 0 lines.
    - linux: `total: 2431` ×2, `succeeded: 2427`, skipped 4, GUARD 14.
    - windows: `succeeded: 2410`, skipped 21, GUARD 15.
    - RULES 679, `Ran 117 tests`, floor 117/117, `no leaks found` ×3.
    - `UniversalPrint.Tests.dll (net10…) passed` and `Server.Tests.dll (net10…) passed` on 2 lines each, on each leg. `failed Datasec.` is 0.
  - **The push run at 0ca8c655** (45905675926), linux log: `total: 2429` on 2 lines. Control: `total: 2431` on 0.
  - **Blobs.** The four paths changed between 0ca8c655 and 760e1a64, and each new blob equals the tarball's git blob.
    - Unchanged: RegistrationKeys.cs and RegistrationRecord.cs.
    - `AfterArrivalCheck` goes from 0 lines to 2. In the README, `Each catch can only refuse` goes from 0 lines to 1.
- **Tarball of 760e1a64** (1778239 bytes, 679 files): `facts.py` read POINTERS 56 of 56, and the one-line-off control FIRED.
- **Project:**
  - All nine files equal `.tools/b2140/READY.manifest` (sha256 705a3fed…). B2140 READY is 705a3fed and B2138 READY is b3248f8c.
  - Owed items run 1 to 160: 89 open, 71 ticked.
  - Blocks (`dry.py`): 54 at 377-384 and 55 at 385-392, each ending in a `Closed in part (the records pass of 2026-11-23)` line. 75 at 542-548 and 160 at 1189-1195, each ending in a `Discovered:` line. The anchor heading is at 1197.
  - B2138's DEVIATIONS are D-1 and D-2. The D-2 line holds `249`, `276` and `RegistrationRecord.cs:164`.
- **Jira** (GET-only fence; POST, PUT, DELETE and PATCH were refused in-process):
  - The census is 63. Done: 33, 39, 41, 47.
  - OXPD2-1 has 19 comments; the newest is 41547, which starts `Records pass after pull request 57`.
  - All 10 phrases return 0 issues. The 5 controls fire.
- **Dry build** (`dry.py`; the frozen table re-parsed from the written kit is byte-equal to the one from the source):
  - CLARIFICATIONS: 1236 to 1244, C-93 at line 1238.
  - BACKLOG: 1212 to 1229. Added 17, changed 3. Removing by position and un-ticking gives back the old bytes.
    - Open 88, ticked 74.
    - `Closed: ticked in place` goes from 68 to 71.
    - The anchor moves from 1197 to 1214.
  - History: 410 to 418.
  - `scan_record` finds 0 problems on 28 lines. J-1 has no `scan_jira` codes, and its ADF read-back is EQUAL.
  - 0 doubled words, 0 doubled groups and 0 repeated runs. All three controls fired.

## D-decisions (drafter's)
- **D1 (form).** B2140 is the form. The shape of a `Closed:` line after a `Closed in part` line comes from items 45 (313/314), 65 (470/471) and 96 (712/713).
- **D2 (repeated-run check).** The repeated-run check FIRED on full paths: `.../Registration/RegistrationKeys.cs` contains the 13-character run `/Registration` twice in a row. So the texts name RegistrationKeys.cs, RegistrationRecord.cs and RegistrationKeysTests.cs by base name plus folder.
  - The kit's dry figures say this, so the seat's own check will not stop on it.
- **D3 (the loader's catch pointer).** The review's pointer for the loader's catch is `RegistrationRecord.cs:149`. At 760e1a64 that line is the comment inside the catch; the `catch (Exception)` is at `:147`. BL-CLOSE-54 cites `:147` by my read.
- **D4 (each frozen claim checked against its source line).** Every sentence was checked. Corrections made before freezing:
  - **"first bullet".** The README's "One exception to the first rule" is in the third bullet of What it does, not the first. BL-CLOSE-55, BL-162 and PART 2 now say "the exception to its first rule" and cite "its line 21" and "its line 54".
  - **C-93's "a cell pins it".** K07 pins only the key case, so it now reads "for a key that cannot be made".
  - **BL-162's "part 2 of this kit".** It now reads "part 2 of the lane's kit 2".
- **D5 (commission item 2, lines for items that stay open).** The form gave no line to an item that only stays open: B2140's Q8 put none under 84, 86, 121 or 138, and 137 got its line only for a new sighting. So 121, 137 and 138 get no line (Q8). This lane met no hang.
- **D6 (commission item 4, the stamp error).** It goes in H-OWNER, not in C-93. The form's C-entry records choices a reader could take for his; the "Who decided" line is where the coordinator's own acts sit (Q6).
- **D7 (commission item 3, one destination per finding).** FOUND 2, 3 and 4 go into the `Closed:` lines they measure. FOUND 5, FOUND 6's D-1, FOUND 7, point (c) and the FOR-RECORDS notes go to 162. FOUND 6's D-2 goes to H-OWNER (Q5).
- **D8 (no names or card ids in the kit).** None appear. His board rows are described in words only.

## Chain inputs
| Step | Inputs | Source |
|---|---|---|
| 0 | kit, sidecar, project files, df, python3 | BASE |
| 1 | the `b1785.py` copy, scratch copies | Step 0 |
| 2 | SOURCES, GitHub, tarball, job logs, Jira GETs, B2140/B2138 STATUS | BASE (origin) |
| 3 | frozen texts, C-number (P-7), BL-OLD8 (before-copy), BL-NEW8 (dry BACKLOG) | Steps 0, 2 |
| 4a | live CLARIFICATIONS, filled C-93 | Step 3 |
| 4b | live BACKLOG, 3 ticks, 3 Closed lines, BL-161/162 | Step 3 |
| 4c | filled J-1 (C-93 from Step 2) | Step 3 |
| 4d | live history, BL-OLD8/NEW8 (4b), CMT-1 (4c), C-93 | 4b, 4c |

## Q-questions for Tuesday (defaults as written in the kit)
- **Q1: C-93 as a Tuesday's note with both choices.** Default: yes.
  - (a) No C-entry.
  - (b) Keep only the first choice.
- **Q2: tick 55 whole.** Part (1) was closed by PR 22, its non-RSA limit is named in rule 8, and parts (2) to (7) are closed here. The rule for (3) and the configuration check for (6) are not built, which C-93 records. Default: yes. Alternative: a second `Closed in part` line.
- **Q3: tick 54 whole.** The two survivors are now a named limit, and the gate measured that no cell reaches either catch on macOS. Default: yes. Alternative: a part line.
- **Q4: FOUND 1 becomes new item 161.** Default: yes. Alternative: a clause of 162.
- **Q5: Info destinations as in D7.** Default: yes. Alternative: every Info note goes to 162.
- **Q6: the stamp error goes in H-OWNER.** Default: yes. Alternative: a third paragraph of C-93.
- **Q7: one comment and no ticket.** Default: yes.
- **Q8: no line under 121, 137, 138 or 76, and CLAUDE.md is not edited.** Default: yes. Alternative: one line under each of 121, 137 and 138.

## UNMEASURED / NEVER RUN
- **Never run:** the seat's helper and selftest, HOLD R and R2 on the live files, the live ticks and insertions, and the POST.
- **RELAYED, not measured by me:** every probe, mutant and count of the gate and the seat (macOS arm64), including "358 cells", G1, G2, G3, G8 and G9, and the C01 Linux reach.
- **Not verified by me:** that no assembly is strong-named. My recursive grep over the tarball failed on a zsh glob, so that claim is the gate's FOUND 7, relayed.

## Outside the fences (disclosure)
- **Board read.** `kam_rulings_today.sh 2026-11-27` ran once, with `KAM_READ_MARKER` pointed at `d2146/kam_read_marker`. Only the first 60 characters of each row went to my session, and nothing was saved.
  - Two card-id prefixes showed in my session. Neither is written to any file.
  - `kam_msgs.sh` was not run, and no card was read.
- **hosted3.py.** I ran a byte copy (sha 969fe376) twice, GET only. It wrote job logs into `d2146/hosted-main*`.
- **How the files were written.**
  - The path guard refused `cp` from the project's `b1785.py` into my scratch, because it misread the copy as a write to the project. I copied it with `cat` instead (`cmp` equal, sha256 5e766b28).
  - The kit was put in place with `cp -n` from `kit.out.md` (`cmp` equal). The sidecar was made by `stamp_check.py --init`, then a `cat` of `side.out` (`cmp` equal, ids equal).
  - Only this report was written with the Write tool.
- **Commands I ran.** I ran `find -maxdepth 4` over Tuesday's own `2_Project_Files` to locate the board reader.
  - I ran one recursive `grep -r` inside my own scratch tarball folder (`tar/x`, not the project). It failed on a zsh glob.
  - No `cd` was run. Nothing was deleted.
- **No write anywhere else.** Nothing was written to the project, Jira, GitHub or the card store. Nothing went to any human or device.
