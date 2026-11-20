# FOR RECORDS: what a records pass must file after gate B1778 (round 2 of 2, NO GO @ e0ddd0d on main 7e1a01c)

The gate wrote nothing outside its verify folder and `/private/tmp/b1778-gate/`. Everything below is for the coordinator to file;
none of it was filed by the gate. `<P>` = the project folder of OXPd 2. This list carries round 1's list (gate B1772) forward:
each of its lines is marked CLOSED BY ROUND 2, STILL OPEN or CHANGED, and what round 2 found is added.

## 1. State to record

- Round 1: NO GO at `a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89`, one Major (the secret scan skips files by name), eleven Minor.
- Round 2: NO GO at `e0ddd0dc8518f97ceba09759c5c0b9e987d872e9`, one Major (the second scan exports files only: a token in a
  commit message, a tag message or a file name is seen by no pass), six Minor. No Blocker. **Round 1's Major is closed**
  (24 of 24 names, 59 of 61 rows through the workflow's own function). The new Major is in the kit's frozen text, not in the
  builder's work. A second NO GO on this class goes to the product owner.
- `main` = `7e1a01cf640f8abac89e7148322651be8e4bf15b`; the lane branch = the round-2 head; pull requests 0; tags 0; nothing
  merged, nothing deployed, nothing sent. Read 2026-11-20 15:30 AEDT.
- Hosted runs: `44661506229` (round 1's head) and `44671776263` (round 2's head), each 4 jobs success on attempt 1; every
  quoted line of the second confirmed in the logs by the gate.
- No secret is stored today: all 62 objects of the repository (3 commit messages, 25 tree listings, 34 files) scanned: 0 findings.

## 2. The decision this verdict asks for (ONE question, the product owner's by the round rule)

Either (a) a third commit on the branch that fixes finding 1 (and, cheaply in the same step, findings 2, 3 and 5), then a
short tier-1 re-gate of that diff; or (b) merge the branch as it is and fix forward by a tier-1 lane. What (b) costs: until the
follow-up lands, `main` documents three limits of the scan where the gate measured more, and a token in a commit message is
unseen. What (a) costs: one more commit and one more gate; a candidate is measured (`/private/tmp/b1778-gate/scripts/candidate.py`,
`logs/candidate.txt`: 92 of 108 rows found against 80, 0 lost).

## 3. Open clauses of WP0.3 and exit point E0.4 (the Jira Task `OXPD2-8` must NOT move to Done on a merge of this branch)

| Clause | State | Owner of the next step |
|---|---|---|
| The bundle tool in the pipeline and a test bundle | not built | STILL OPEN: a decision on how a runner obtains HP's tool, the product owner's |
| Secret scanning with no allow-listed paths | CHANGED: met for file names and for first bytes at the start of a file; not met for what a commit stores outside its files | the decision of section 2 |
| CodeQL | no analysis exists; the first pull request will show none | STILL OPEN: the coordinator reads it; an owner rules if it blocks |
| The development CA in a production bundle | mechanism only; 0 fingerprints; no release mode | STILL OPEN |
| HP's beta library in any release artefact | met for today's publish shape only | STILL OPEN |

## 4. Round 1's follow-ups, each marked

1. ROUND 2 of the lane (finding 1 of round 1; the missing-list test; the floor): **CLOSED BY ROUND 2** for the name skipping
   (a second scan under neutral names), the missing deny-list test (it kills the surviving mutant) and the floor (53 equals the
   count, held by a test). NOT taken into round 2, by the kit's own table, and STILL OPEN: the development-CA name rule as a
   substring and ZIP member names split on a backslash; the three line rules for quoted keys, escapes and flow mappings in
   workflows (round 2's finding 4 shows why they matter: an escaped key at workflow level sets the scanner's configuration
   variable past R1); a NUL-byte rule for tracked files.
2. OWNER DECISION, the four checks are required by nothing: **STILL OPEN**, unchanged on GitHub (the required list is empty, no
   pull-request rule, the branch not protected). Round 2 raises the bar inside the two jobs only. Add to the question: the
   fingerprint does not replace a required check (section 5, line 4).
3. OWNER DECISION if the first pull request reads `blocked`: **STILL OPEN**, unchanged (CODEQL-FIRST-PR.md of both rounds).
4. COORDINATOR RULE into `<P>/CLAUDE.md` (a diff touching `.github/**`, `build/**`, `global.json`, `Directory.Build.props`,
   `Directory.Packages.props`, `NuGet.config` or a lock file always gets a tier-1 gate): **STILL OPEN**; not found written
   there by this gate's read of that file.
5. RELEASE MODE of the guard: **STILL OPEN**; now backlog line 14.
6. THE GUARD before the publish shape changes (single-file hosts, other archives, key stores, UTF-16 PEM): **STILL OPEN**; no
   backlog line names the single-file case or the certificate forms (round 1's findings 4 and 5): add them.
7. `RuntimeIdentifiers` into `Directory.Build.props`: **CLOSED BY ROUND 2** (reproduced: a new project with no list of its own
   inherits it; fault 2 does not return).
8. THE LAUNCHER's three dotnet variables and the runbook's launch notes: **STILL OPEN** (the coordinator's frozen text).
9. After the first merge, read the code-scanning setup, the analyses on `main` and the open alerts: **STILL OPEN**.

## 5. New from round 2: follow-ups to file (each a backlog line)

1. THE SECOND SCAN EXPORTS FILES ONLY (finding 1, Major): commit messages, tag messages and file names are read by no pass.
   The fix and the candidate are in the verdict.
2. THE READ CUT (finding 2): a token across byte 125000 of a large file with no blank line, under a skipped name, is seen by
   no pass.
3. THREE BYTE MARKS (finding 3): `DICM` at a stored file's byte 75, `ustar` at 204, `CD001` at 32716 make the second scan skip
   it; the README's sentence on first bytes is too strong.
4. THE FINGERPRINT COVERS TWO JOBS, NOT THE WORKFLOW (finding 4): 10 measured edits that weaken a check stay green, 6 of them
   in one file; a control deleted with the floor lowered in the same commit passes. Later hardening: fingerprint the whole
   file; add `BASH_ENV` and escaped keys to the line rules.
5. `.gitleaksignore` AT THE ROOT is read by the second scan (finding 5): start the scans from outside the checkout.
6. EVERY RUN READS EVERY BRANCH of the origin: a token on one lane's branch reddens every lane's `secret-scan`, and there is no
   ignore mechanism by rule. Write the procedure once: revoke the credential, remove the branch from the origin, never add an
   ignore file.
7. RULES KEYED ON A FILE NAME (for example the clear-text password of `NuGet.config`) do not fire under a neutral name; under
   a skipped folder they are seen by no pass.
8. FALSE REDS of the fingerprint: a job added after `rules`, a top-level block moved below `jobs:`. Say in the README how a
   lane adds a job (set the fingerprint in the same commit, after review).
9. Scale: one `git` process per stored file (10 001 files: 72.5 s on this machine); use one batch process before the
   repository grows.

## 6. `<P>/BACKLOG.md`: lines to change or add (its 18 lines are each real; none is to be removed)

- Line 9 (the design correction pass "is not copied"): untrue since the copy of 14:01 today; tick it or reword it. The
  coordinator's.
- Line 15: replace "two files instead of one, no more" by "an edit inside the `secret-scan` or `rules` job needs a second
  file; an edit outside them, or a commit that changes both, does not".
- Line 16: its three limits are not the whole list: add section 5's lines 1, 2, 3 and 7; "which closes both" is true for
  names and for first bytes at the start of a file only.
- Add: section 5's lines 4, 5, 6, 8 and 9.
- Still missing from round 1's list: the guard's publish-shape limits (extend line 11 by the single-file case); the `.pdb`
  files and the `web.config` in the published folders; `actions/setup-dotnet` pinned to the commit of `v6.0.0` while a newer
  release existed on 2026-11-20.

## 7. `<P>/SETUP_RUNBOOK.md`: sentences to correct

- Round 1's two sentences (the pull-request rule; the first launch): **CLOSED BY ROUND 2**, both now read true.
- Line 14: `4_Credentials/` does not hold "the launcher's preflight log", and `.azure/` was not "made empty by the launcher":
  the launcher has never been run (line 33 says so). Untrue: correct it.
- Line 50: "every package from" the registry was the first restore only; later restores fetched nothing. Say which.
- Line 29 (19 Jira issues): not re-read in round 2.
- Line 87: as backlog line 16.
- Line 60 names a script under the second lane's work folder as the way to run the neutral scan locally; it is not in the
  repository. Either say so or give the three lines a person can type.

## 8. Jira `OXPD2` (NOT read in round 2; round 1's reading carried, unchanged and unverified since)

- `OXPD2-8` stays open (section 3). The five backlog lines 14 to 18 and section 5's nine lines have no ticket.
- `OXPD2-10` describes work another agent did on 2026-11-20: STILL OPEN, the coordinator's.
- Four Task texts name no requirement row (`OXPD2-8`, `-9`, `-10`, `-16`): STILL OPEN; round 1's table says what each should cite.

## 9. What the gate leaves on this machine

- `/private/tmp/b1778-gate/` (916M when measured): the clone (push URL invalid), the probe repositories (they hold the gate's
  random planted tokens: fake values, built by program, never printed, in no project repository), the build trees and output,
  the gate's package cache and home, the CodeQL databases, the logs and the scripts, two `_quarantine_*` folders of first runs.
  A reboot clears it. A third round can reuse `scripts/` (`scan_probes.py`, `step_probes.py`, `pc_probes.py`, `chain.sh`).
- `/private/tmp/b1772-gate/` (round 1's) was read, not written.
- No process left running (0 dotnet, 0 CodeQL); nothing written under the project folder or its `.tools`; the seat's checkout
  reads the round-2 head with an empty porcelain, untouched.

## 10. NOT measured by either gate (carry these as open, not as passed)

A pull request and its checks; whether the ruleset blocks the first merge; CodeQL for C#; Windows and `docker build` locally;
whether GitHub accepts the escaped key and the block-text name of finding 4; a file kept by Git LFS; telemetry on the wire; that
10.0.15 is the newest 10.0.x; billing; the launcher in a real run; which bash the hosted runner has.
