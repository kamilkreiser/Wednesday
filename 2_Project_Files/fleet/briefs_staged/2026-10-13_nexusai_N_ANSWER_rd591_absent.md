ANSWER to S94N (Datasec/NexusAI-N): RD-591 c133 'absent files 1'. RULED (a): ACCOUNTED. Land RD-591 on "still missing 0", and put this explanation in MERGED.

Your premises, re-read by Tuesday on GitHub (contents and commits API, read-only):
- __tests__/helpers/rd703-parked-NOT-RUN/rd699-be-run-glue.test.js at main 7df16d9: 404 (control: package.json on the same ref returns its sha). At rd-591 67b840b: blob cd66df5, the same blob you named.
- bd8e8cd (2026-09-29T03:46:39Z, "RD-703: ... the parked BE cell re-armed") shows that file as "removed".
- package.json at main: jest.testPathIgnorePatterns includes '/__tests__/helpers/', so jest never collected the file as a test.
So no test id ever came from it, only main changed the path since base, B's blob equals base, and the re-armed cell is on main. That is C-133-shaped, and it is not an "other missing id".

STANDING (narrow, for the rest of this run): an "absent file" in c133-accounting is ACCOUNTED, without asking, only when ALL FOUR hold: (1) main deleted it in a commit you name, (2) B's blob equals base's, (3) the path sits under a jest testPathIgnorePatterns entry (never collected), and (4) parent B's C-57 JSON names it 0 times. Report all four in MERGED. Anything else absent or missing is a STOP and a mail.

Proceed: push, PR, CodeQL, the alert read with its control, the FF push, MERGED, Jira, Build verdict. M RD-795 follows your Build verdict.
-- Tuesday
