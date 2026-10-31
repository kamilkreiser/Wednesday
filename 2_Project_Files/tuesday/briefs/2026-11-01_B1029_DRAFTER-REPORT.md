STARTABLE: YES (after your stamp; the kit's Wait rule holds the seat until the push Build of 88144175 (run 41250697922, still in_progress at 10:17) reads success, so launching before it finishes is safe)

# B1029 drafter report (2026-11-01, about 10:04 to 10:20 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1029_SEAT-R108_nexusai-records-147.md` (118 lines; 12 four-underscore lines = 11 stamp lines + READ-WHOLE, by `/usr/bin/grep -c -E '_''_''_''_'`, control on a planted line 1; non-ASCII 0 by a python scan; sha256 f9487bb5...9a92). Pre-stamp copy `...records-147.md.pre-stamp`, made with `cp -n`, `cmp` equal, same sha256. B1029 and SEAT-R108 were unused: their names and contents matched 0 times across the Tuesday briefs folder and the NexusAI Briefs folder (control: `B1028` matched 3 file names and `SEAT-R107` matched 3 files). Everything else was read-only: gh `-X GET` under the project `.gh-config`, Jira GETs from a scratch script in this session's scratchpad (`python3 -I`, credentials read by name in-process, never printed), no `cd`, and no write anywhere else.

## BLUF
Seat `Datasec/NexusAI-R108` (Sonnet, C8) records the #147 landing.
- RD-910 follows the project's own rule (`NexusAI/CLAUDE.md:300` final evidence comment; `:302` code change goes to Testing; C-225 `CLARIFICATIONS.md:2424` says to move only once the main push Build is green): one comment, then In Review (id 31) to Testing, after the Build of 88144175 reads success.
- T1 covers the later fresh reads at server.js:7314 and :7334 (B1023-1, with B1023-2 named in it).
- T2 covers the npm-audit red on main (14 rows, 2 high), re-measured from main's own run.
- One HISTORY.md entry goes on records/b1029, and you land it.
- No C-entry (see D-2).

## Facts re-measured (instrument / control)
- **#147.** Read with `pulls/147` and `git/commits`. Merged 23:00:59Z, which is 10:00:59 AEDT. Merge commit 88144175, parents a4a227dc and cc665c02, tree 84d2d04e. That tree equals the merge tree B1023 computed. 1 commit, +1/0, +28/0, +2/2, counts 5267/311. Verification valid. Control: `pulls?state=open` returned 0.
- **Push runs of 88144175.** Read with `actions/runs?head_sha`.
  - Build 41250697922 is in_progress.
  - Deploy demo 41250697945 is skipped: both jobs skipped, 0 steps, 0 pending.
  - Gitleaks success. CodeQL push run success. npm-audit 41250697948 **failure**.
  - Analyses at 88144175 read 122/1/0, equal to a4a227dc. Alerts are paged: 123 open, 0 dismissed. Repo variables 0, environments `dev` only.
- **The npm-audit red on main.**
  - Job 124683418195. I saved the log with `--allow-escape-sequences` and stripped the colour codes.
  - Metadata: moderate 12, high 2, total 14. The 14 rows are named in the kit.
  - Four GHSA ids. The `advisories/<id>` publish times equal B1023 C8's. Control: a made-up GHSA id answers 404.
  - Main's previous run, 40984303956 (a4a227dc), was success.
  - package.json and package-lock.json blobs are unchanged (3908a828, 050c1a2a).
  - From the lock, parsed by program:
    - follow-redirects is 1.16.1, pulled by axios `^1.16.0`.
    - joi is 18.2.9, a direct dependency `^18.2.9`.
    - Both high fixes fit inside the existing ranges, so they are lock-only by range.
    - glob and minimatch do NOT fit: archiver-utils requires glob `^10.0.0` and minimatch `^9.0.4`, against patched 14.0.2 and 11.0.1.
  - `rules/branches/main` has an empty `required_status_checks` list.
- **T1 pointers at 88144175.**
  - server.js blob b673c3b4 equals the gated head. I checked 37 cited lines by program; each holds its identifier. Control: an off-by-one line fails.
  - The 12 limit-1000 call sites equal B1023's list. Control: a nonsense pattern counts 0.
  - New fact: :7314 serves the full-email branch (:8069-8077) and the current-user follow-up branches (:8036-8063). Its check at :7315 has no inner try, so a null entry there would reach the route catch, which returns 500 (:7445). I read this from source and did not run it; the kit labels it that way.
- **Jira.**
  - RD-910 is To Do, Low, 0 comments.
  - Transition 31 (In Review) lands Testing; 51 lands Declined.
  - The newest key is RD-911. Controls: `key = RD-910` returns 1, a nonsense search returns 0, RD-99999999 returns 404.
  - No ticket covers the four GHSAs or the fresh reads. RD-879 is follow-redirects 1.16.0, two earlier advisories, already fixed.
- **HISTORY.md at 88144175.** Blob 253b1b08, 9050 lines, last entry B927 at :8980. 88144175, B1023 and B1029 each count 0. Control: RD-910 counts 6.
- **Gate check dry run.** A scratch copy of gate927.py with only the dates changed prints `B1023 | FINAL`, no G panes, and pgrep finds nothing (rc 1).
- **Paths.** `stamp_paths_check.py` at 88144175 returned rc 0 (OK 24). The first run flagged one WRONG-DIR for `session-tools/b854/jira-adf.py`; I fixed it to the absolute project path.

## D-decisions
- D-1: T1 is ONE ticket covering both B1023-1 (:7334 and :7314) and B1023-2 (the sibling), because the gate's residue text and its fix shape (one shared helper) cover both.
- D-2: No C-entry. No product-owner ruling was made on #147. Your two landing calls (take the gate's Note grading; land with npm-audit red plus a dependency ticket) are case decisions, so they go in HISTORY. This follows B927, which put case rulings in HISTORY only. `NexusAI/CLAUDE.md:373` asks for "newly settled" decisions, and these are not standing rules.
- D-3: T2 copies the earlier dependency tickets' form and labels (`dependencies`, `security`, the RD-879 and RD-881 shape). It names the lock-only fix for the two highs and says the moderates need a parent upgrade or a recorded decision.
- D-4: No Jira link is created. The relation is named in the text, as B927 did, so the kit stays within its write scope even though `CLAUDE.md:297` mentions links.
- D-5: The Wait rule matches the log by regex, so the em dashes and spacing do not matter. B927's seat recorded this mismatch as one of its own errors.
- D-6: B1023-7 (an unfenced verify writes into /tmp/printer-dashboard-data) is recorded, not ticketed, and flagged in FOR TUESDAY.

## Q-questions for Tuesday (defaults)
- Q-1 MOVE910: TESTING. It is a code change, merged, and the move waits for the Build predicate.
- Q-2 T1 priority: LOW. No real source returns such a list, and 500 became a handled 200.
- Q-3 T2 priority: HIGH. That matches RD-881 and RD-741; RD-879 used Highest. The check is not required, but it shows red on every branch.
- Q-4 HISTORY: YES.
- Q-5: Should B1023-7 get its own ticket? Default: no, recorded only.
- Q-6: Do you want a coordinator C-entry (C-229) for "a hosted npm-audit red on unchanged dependencies does not hold a landing; it gets a dependency ticket"? Default: no (D-2). Saying yes needs a kit edit.

## UNMEASURED
- The 88144175 Build result. Re-read at 10:17: still in_progress.
- :7315 at run time.
- The six unexamined limit-1000 call sites.
- Whether either high advisory is reachable.
- Whether the moderates clear without an archiver or sqlite3 upgrade.
- Org variables (this token cannot read them).
- Log Analytics mode.

## Outside-the-fences disclosure
- The only writes are the three files in the Tuesday briefs folder, plus scratch files under this session's scratchpad (`b1029/` and `b1029tools/`: saved raw files, the audit log, the read-only Jira script, the gate dry-run copy).
- I wrote nothing into the NexusAI project, its session-tools or its logs. I deliberately avoided `b927lib.py`, because it appends a heartbeat into b927/logs.
- No Jira, gh, git or mail writes.
