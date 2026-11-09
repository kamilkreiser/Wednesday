From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-1 to your kit B1392 (SEAT-H142). Every hold, partition and housekeeping rule of the kit still binds you; HARD STOP 10:30 AEDT 2026-11-10 as stamped.

# ONE FIX ON YOUR BRANCH `b1392/hpsmpoc-web-ui` (head 121ee236): WRITE THE TWO LITERAL U+202E CHARACTERS AS ESCAPES

**Why.** PR #300's hosted CI (run 42673925319, attempt 2) went red in `infra (Bicep validate)`:
`FAIL: test_no_tracked_file_holds_a_raw_direction_control_or_hidden_character (test_hidden_characters.NoRawHidd...)`
`AssertionError: Lists differ: ['web/src/server/mock/customer-shape.test.[213 chars]pe)'] != []`
That is the same item your gate (B1451, finding B1451-1) graded Minor. Its kit said "Major if a CI step refuses it", and a CI step does. Read the gate's line in `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-10_B1451_STATUS.md` (`## FINDINGS`, B1451-1).

**The change.**
- In `web/src/server/mock/customer-shape.test.ts`, at the two lines B1451-1 names (:17 and :58 at your head; re-print them with `grep -n`), replace each literal U+202E with the escape text `‮` inside the same string literal. The string's runtime value must stay byte-identical.
- Do nothing else: no other file, no other line.
- This is ONE plain forward commit. No amend, no rebase, no force-push. Then do a plain `git push origin b1392/hpsmpoc-web-ui`.

**Prove it, each with output in STATUS under `## ADDENDUM-1`:**
1. `git diff 121ee236 HEAD --stat` shows exactly 1 file and 2 changed lines.
2. A python `unicodedata` scan over every tracked file at your new head finds 0 literal U+202E/U+200B or other Cf characters in that file. Control: the scan finds 2 at 121ee236.
3. Run the project's own infra test that failed, `python3 -m unittest` for `infra/tests/test_hidden_characters.py` (find how CI runs it in `.github/workflows/ci.yml`). It is RED at 121ee236 and GREEN at the new head.
4. `customer-shape.test.ts` vitest is green at the new head, and its 8 rows are still 8; the full `npm test` counts match the gate's numbers.
5. The commit message is plain ASCII, with no B-number or name, and ends with your session's attribution line.

**Last line** of your STATUS file when done: `READY B1392: <new head sha40>` (`git ls-remote` of the branch equals it), or `STOPPED: NEEDS TUESDAY <one question>`.
