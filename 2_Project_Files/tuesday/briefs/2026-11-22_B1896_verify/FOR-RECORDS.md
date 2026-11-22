# For the records (MPSCALC-430, 431, 432, 433), gate B1896

## The tickets now
All four read Backlog, 0 comments, 0 links at this gate's own Jira GET (2026-11-22 afternoon; control MPSCALC-361 reads Done); updated stamps unchanged (430 2026-11-20 20:18, 431 20:18, 432 20:19, 433 2026-11-22 10:25). A merge does not move a ticket; the records pass moves all four and comments on each after the pull request lands.

One sentence each for the comments (Tuesday's choices as coordinator, not the product owner's; the tickets say "no product byte and no word of the product owner"):
- MPSCALC-430: a new test class pins the computed settings (6), pinned literals (4), site table (13), setting plants (13) and site plants (7) by expected names; emptying any of them fails a test (shown by planted runs); tests 43 -> 49.
- MPSCALC-431: the mutant tests (compiled mutants, id swap, planted source) compare with the unmutated template and assert exactly one new problem naming the key; a removal of a setting the template lacks fails with "setting <KEY> is not in the unmutated template, so there is nothing to remove", not a bare KeyError; the older guard classes keep their convention, as the ticket allows. SEE THE Q3 GAP BELOW before closing.
- MPSCALC-432: seven site properties are pinned in the site table at the value the template sets and each is shown red by a planted change of the template source (one new test, 7 sub-tests).
- MPSCALC-433: the comment at infra/scripts/validate.sh:4 now says step 2; the text "README.md step 3" reads 0 lines of infra/scripts; one line changed; nothing else.

## The Q3 gap (MPSCALC-431), in the words of Stamp S5
MPSCALC-431's acceptance line "the first failure printed names the key of the defect" is met ONLY by the sub-test label. With one real defect in the template the first failure printed is `FAIL: test_each_planted_source_change_is_one_problem (...) (plant='WEBSITES_ENABLE_APP_SERVICE_STORAGE')`, which names the key in its label; that sub-test's own message is still the bare `unique anchor`. The records pass should read the line so, not as "the message names the key". No ninth edit was made (Tuesday's Q3 answer). The other parts of 431's acceptance line are met by message: exactly-one-new-problem messages name the key, and the removed-setting message names the key (0 KeyError lines at head, 1 at base, in the red runs).

## Findings relayed from the seat: `gitleaks git` over main's history
The seat's whole-history run (710 commits, 709 at base) reported 9449 findings, all rule `generic-api-key`: 9426 in `tests/MpsCalc.Engine.Tests/Fixtures/purchase_bom_scenarios.json`, 17 in `.../purchase_bom_synthetic.json`, 2 in `tests/MpsCalc.Api.Tests/CareKeyPatternApiTests.cs`, 2 in `.../SourceLifecycleTests.GateB41.cs`, 2 in `web/src/api/stub/stubApi.ts`. None is in this branch's commit (the range scan 9c9a7219..HEAD found none). RELAYED.
This gate sampled five of the 9426 at source by location only (random, fixed seed, from the seat's redacted report; no value printed). All five sit on line 1 (the fixture is a single minified line) at different columns, in commits 5dbd2ad2 (three), fdeb7098 and 77238a6e, directly after a `line` or `section` key of a bill-of-materials row. Each match span is 35 characters holding a 28-character token of the shape three lowercase letters, an underscore, then 24 mixed lowercase letters and digits, with entropy 3.6 to 4.0. DERIVED: they look like generated fixture identifiers (a fixed prefix, a fixed length, in BOM line and section rows of a test fixture), not credentials; the rule fired on a generic key-shaped pattern. Not proof that none of the 9426 is real; a records ticket for an allowlist (path-scoped to the fixture files) or a fingerprint baseline is the usual answer, and the rest of the five files above were not sampled.

## The seat's residue incident
The seat moved three pre-existing zero-byte files (`Datasec`, `MPS`, `Commercial`) out of the project folder with a loop that split the path on spaces, and moved them back with `mv -n`. The gate read that nothing TRACKED moved (the branch diff is the two paths only; the three files are untracked zero-byte strays in the project root, not in the repository). The strays themselves are an old unquoted-path artefact of an earlier seat and are still there; a records line, not this change.

## Ticket candidates (not blocking, not this change)
1. A gitleaks allowlist or baseline for the fixture files above (see the section on gitleaks).
2. The `unique anchor` message of the two plant tests could name the plant (the Q3 alternative), which would make 431's first-failure line met by message, not label only.
3. Three untracked zero-byte stray files in the MPS project root (`Commercial`, `MPS`, and `Datasec` one level up).

## Measured in the gate
Head tarball of 48134ee0 and base tarball of 9c9a7219 (Source_Documents never opened): `test_infra.py` Ran 49 OK; `test_validate_script.py` Ran 6 OK; red.py 31 labels DIFF 0; check433 exit 1 at base and 0 at head; scans.py as the kit says; the CI loop 15 files rc 0 with the kit's Ran counts. Nothing deployed.
