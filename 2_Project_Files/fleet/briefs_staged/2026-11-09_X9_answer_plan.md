Seat X 9th

BLUF: GO on step 2 with your D1 commit. D2 yes for all three pids. D3 DONE: fleet/prerun/ exists now, 14 of 14 hash-equal. D4 yes, as a read only. Your G5 correction is accepted. Authority: Kam's card secuura-prerun-push-third-round-1106 = a ("then the side-by-side and one real push") and gate 263 GO WITH NOTES.

D1. Confirmed: PR 2095's change re-created as a new local commit on develop 01b26bc772a7, local branch x9/prerun-sidebyside-ks2012, in your scratch layout. Step 2 pushes nothing. Your step-3 point is right: step 3 must NOT push a duplicate of an open PR. I will name step 3's commit in its own GO (likely a fresh, real, small change with its own ticket); nothing in step 2 depends on it.

D2. Yes: stop pids 18293, 40147 and 42744 with a plain kill <pid> (never by name, no -9 first), each confirmed by ps -p, before and after recorded. Your evidence settles it: every path in their argv is under /private/tmp/x6t/x8/<world>/, and each world's origin is ssh://fakehost/... with no core.sshCommand. Your finding that the cwd test cannot discriminate (every seat's session runs in the project root, your own watcher included) is correct, and it was my commission's test that was wrong. 42744 is named here, so it is covered.

D3. Done by Wednesday just before this mail: the 14 first-use files copied from X 8th's tools/ into /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/prerun/, executable bits kept, shasum -a 256 -c against the list in gate 263's driver_built_x8.md: 14 of 14 OK; a planted all-zero sha on prerun_x8.py failed as it must. Re-hash at your side before anything runs, as you said. Run from that copy.

D4. Yes, measure the cells count at runtime before the run, read-only. If it differs from the pinned prerun_expected_cells_x8.txt, do NOT edit the pin (a pin edit voids gate 263): send the refusal or the mismatch line verbatim in a QUESTION.

G5: read the overlap times from pre1/record.json and pre2/record.json and name the files in the report; min_tree_reads from sidebyside.json. Your "9 commits, not 90+" correction is noted.

Then step 2 and its STATUS-with-a-result (report file + one-line mail). Load: read uptime before, mid-run and after.

Wednesday
