## What changes

Tests and one comment. Nothing is deployed and no template, script behaviour, code or contract byte changes. Two files: `infra/tests/test_infra.py` (+106 -9) and `infra/scripts/validate.sh` (+1 -1).

**MPSCALC-430.** A new test class pins each table and each list of plants by its expected names: the computed settings (6), the pinned literals (4), the site table (13), the setting plants (13) and the site plants (7). Emptying any of them now fails a test; before, emptying the plants list read green and emptying a table turned red only the planted-source test.

**MPSCALC-431.** The mutant tests (compiled mutants, module id swap, planted source) take the problems of the unmutated template first and assert that the mutant adds exactly one, whose text names the key. A setting that the unmutated template does not hold, asked to be removed, fails with `setting <KEY> is not in the unmutated template, so there is nothing to remove` instead of a bare `KeyError`. The older guard class keeps its convention (the ticket allows it).

**MPSCALC-432.** Seven site properties (always on, HTTP/2, remote debugging, 32-bit worker, startup command, client affinity, public network access) are added to the site table at the value the template sets, and one new test plants a change of each in a copy of the template source and asserts exactly one new problem naming the property.

**MPSCALC-433.** The comment at `infra/scripts/validate.sh:4` names step 2, the step `infra/README.md` numbers for the what-if (step 3 is the create). A comment only; the script's behaviour is unchanged.

## Who decides

The four tickets say "no product byte and no word of the product owner". The design choices (five key sets for 430, pinning the template's own value for all seven properties, one commit) are the coordinator's, not the product owner's.

## Checked

`infra/tests/test_infra.py` 43 tests before, 49 after, OK; `infra/tests/test_validate_script.py` 6, OK; the 15 Python test files that CI runs pass at the head. Each new check was shown red against a planted defect and green without it (31 planted runs, all as expected). The diff equals the frozen edit list byte for byte.

## Not tested

Hosted CI and CodeQL (they decide on this pull request). `dotnet` and web jobs (neither reads the two files). Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
