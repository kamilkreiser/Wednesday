From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-1 to your kit B1396 (SEAT-H146). Your kit's holds, partition, draft rules and housekeeping all still bind you.

# A FIX ROUND ON YOUR OWN BRANCH `b1396/hpsmpoc-documents` (head 6b185f3f), FORWARD COMMITS ONLY

An independent read-only verifier returned **NO GO** on 6b185f3. Read its record whole first:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1396_verify/VERDICT.md` (findings table, section 3; spot-check table).

## Fix these, each in a plain forward commit (no amend, rebase or force-push), then push
1. **BLOCKER:** `Deliverables/2026-11-10_testing-evidence/testing-evidence.md:143` quotes a test method name containing a ban-list name joined by underscores. Shorten the quoted name before the name with "...", as the table already does for other long names. **Fix your rule-4 checker too:** a name joined by underscores must be found. Use `(?<![A-Za-z])<name>(?![a-z])` or treat `_` as a separator, and add a control that plants `_by_<name>_` and must fire. Re-run it over all 22 changed paths and print the result.
2. **MAJOR:** privacy draft, line 124. "31 Mar 2027 = 90 days after the Week 10 end" is wrong (Week 10 ends 3 Dec 2026). State what 31 Mar 2027 actually is relative to (the verifier: 90 days after the signed SOW's End Date, 31 Dec 2026). Re-derive it yourself with `date` arithmetic and print it. Keep the date a PROPOSAL.
3. **MAJOR:** re-base record, line 53. The three phrase counts are wrong (verifier: "twenty-one calendar days" 0 exact, because the SOW has "(21)" between the words; "Effective Date" 3; "End Date" 3). Re-count with your own program and print it with a control. Write what you measure, and say that the exact phrase is split.
4. **MINOR, do it:** the 24 provenance pointers into the coordinator's folders, your `.tools` folder or "branch b1396" carry brief numbers and seat ids into client deliverables. Replace each with a source a reader of the analysis repository can resolve (a repository path:line, a Jira key, a code path at a named sha), or with `[src: internal QA record, not in this repository | RELAYED]`. No `B<digits>`, seat id or coordinator name may remain in the 22 paths. Check by program, with a control.
5. **MINOR, do it:** AI tools record, line 63. Decision C-22 names the project's dev subscription, not "the product owner's own tenant". Correct the attribution.
6. **MINOR, do it:** admin guide, line 54. The content version range omits 0.2.0, 0.6.1 and an unversioned file. List them as measured.
7. **MINOR, do it:** admin guide, line 196. The UAT walk-through checklist includes tearing down the environment, which would delete the only site the customer has. Remove that step from the walk-through, or mark it `NOT FOR UAT: the customer's review site; teardown only on the product owner's explicit word`.
8. Cosmetic: the escaped `\|` inside prose may stay unless it breaks a table.

## Do NOT touch
The pre-existing lines on analysis main that the verifier noted (3 old M2 lines with an SOW run, and 100 old stage-gate lines with names). They need their own ruling. List them under HELD in STATUS, unchanged.

## Last line
Re-run ALL your draft-rule programs with their controls after the fixes, print them in STATUS under `## FIX ROUND 1`, and finish with exactly `READY B1396: <new head sha40>`, or `STOPPED: NEEDS TUESDAY <one question>`. HARD STOP 10:30 AEDT 2026-11-10 as stamped.
