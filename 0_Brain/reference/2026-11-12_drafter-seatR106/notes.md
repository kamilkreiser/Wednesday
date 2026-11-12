# Drafter notes, Seat R 106th brief (2026-11-12 ~13:0x AEDT)

Output: brief_R106.md (103 lines, 32,114 bytes, under 55 KB). One blank STAMP block (near top), no SELF-CHECK line, no lesson-file names, RULED BY KAM section copied verbatim from R 105th's stamped brief. PROVENANCE: a line for each of the 14 KS keys named (KS-2169, 2005, 2170, 2021, 1931, 1923, 1053, 1081, 966, 2061, 1873, 1868, 663, 1728; each counted exactly once at the start of a line) plus develop/heads, strict-apply base and R105-F1 lines and the ruling mail.

Measured by me this session (read-only):
- ls-remote 13:00 AEDT: develop 1247e1af3c20 (equals gate 327's pins_start.txt); 2203 67baaef2f105, 2206 36c0b86b3dd0 (equal to R 105th's HANDOVER); 2200, 2201, 2099 (8967de8b1755), 2052, 2075, 2194-2198 equal R 105th's pins; 2202 3c2b6ebe2ab8, 2204 25ad80bc8298, 2205 06fbdf990638 new to this brief.
- Worktrees s-r105-ks2169 / s-r105-ks2005 HEAD = the PR heads, status clean; s-r101-ks1053 HEAD 16a5c67e676e.
- READY names and sizes by ls -l equal R 105th's brief (3,450; 4,787; 4,307; 11,075; 15,058; 15,070; 11,838).
- history.md: R 105th guard matches once (control for the R 106th guard).
- Lock holder file read: Seat A 26th, pid 68662, 01:57:36Z, one queue entry (not yours; the brief tells R 106th to re-read).
- Gate 327: verdict.md did NOT exist at my read (folder holds commission.md, ready_r105_mail.txt, scratch/). I did not re-check at the end.
- R105-F1 located: line 26 `EXTRA=run; grep -q ... vitest run && EXTRA=""` in measure_testonly_r105.sh and measure_row_r105.sh; tsc_tests types are passed by caller (line 42 / line 41). originate test script is `jest` (read from s-r105-ks2005 package.json). Whole-suite numbers 221 suites / 2,598 tests (before) and 2,599 (after) read from REC105/evidence/row2005/suite_before_jest.out and suite_after_jest.out; baseline was at 088fa84da10c.

Judgement calls and discrepancies for Wednesday:
1. The commission says R 105th measured strict apply "at develop 1247e1af3c20 with zero offsets". The record (evidence/apply_check_r105.out header, HANDOVER line 16) says develop 697f422f1a39. The brief states the file's version and orders a re-measure at 1247e1af3c20. Develop's two later moves (088fa84da10c; 1247e1af3c20: 13 files, scripts tests and fragments only) touch none of the queued write paths, by R 105th's compare-API json (not re-run by me; no GitHub call).
2. Set-up row 0 is spelled out with a planted control: fixed tool reports the whole-suite count, unfixed form shows fewer, plus unchanged-behaviour controls on a vitest package (transfer) and packages/shared. I added those two (the commission asks only for originate); drop if too much. I did not claim the count at 1247e1af3c20 is 2,598; the brief makes R 106th measure it.
3. Gate 327 was running, so the brief makes the fix round ADDENDUM-only and says never read the gate folder. The STAMP block names gate 327 for Wednesday to fill.
4. The READY carried-list (2194, 2195, 2197, 2198, 2200, 2201) is kept from R 105th's brief; I left to Wednesday whether 2203, 2206, 2204, 2205 join it (brief says so). Several of these may be merged by now; I could not tell from ls-remote.
5. Finding (b) is worded so the brief itself never puts "Refs" directly before KS-2170 (the very slip it warns about).
6. Row 19's two statements are restated from R 105th's brief and pointed at R 103rd's brief; I did not re-read R 103rd's brief QUEUE batch 2 myself (PROVENANCE says so). Rows 16/12/46/KS-2061 text is from R 105th's brief, not re-derived from R 104th's.
7. "R 105th's watcher ran to about 02:10Z": the brief tells R 106th to read REC105/mail/ for anything newer than the wrap mail; I did not check whether such mail exists.
8. Brief contains the literal `cd` in the carried "No `cd`" rule line (line 74), as R 105th's brief did; I wrote no cd myself.

Not measured: machine load/df/panes, Linear states, GitHub PR open/closed state, anything in the Spark.
