# FOR RECORDS: what a records pass must file after gate B1783 (round 3, the last: GO WITH FINDINGS @ 6e2629b on main 7e1a01c)

The gate wrote nothing outside its verify folder and `/private/tmp/b1783-gate/`. Everything below is for the coordinator to file;
none of it was filed by the gate. `<P>` = the project folder of OXPd 2. This list carries the lists of rounds 1 and 2 (gates
B1772 and B1778) forward: each of their lines is marked CLOSED BY ROUND 3, CLOSED EARLIER, STILL OPEN or CHANGED, and what round
3 found is added.

## 1. State to record

- Round 1: NO GO at `a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89`, one Major (the secret scan skips files by name), eleven Minor.
- Round 2: NO GO at `e0ddd0dc8518f97ceba09759c5c0b9e987d872e9`, one Major (the second scan exports files only), six Minor.
- Round 3: **GO WITH FINDINGS at `6e2629bca1762006917e5657c30e407034fdfb12`**: no Blocker, no Major, six Minor, each a follow-up.
  Round 2's Major is closed, measured through the workflow's own function; no row of rounds 1 and 2 is lost; the twelve gains
  are confirmed.
- `main` = `7e1a01cf640f8abac89e7148322651be8e4bf15b`; the lane branch = the round-3 head, 3 commits ahead, 0 behind, 25 files;
  pull requests 0; tags 0; nothing merged, nothing deployed, nothing sent. Read 2026-11-20 16:54 AEDT.
- Hosted runs: `44661506229` (round 1's head), `44671776263` (round 2's head), `44680821033` (round 3's head), each 4 jobs
  success on attempt 1; every quoted line of the third confirmed in the logs by the gate.
- No secret is stored today: all 71 objects of the repository (37 files, 4 commits, 30 folder listings), each in two copies,
  scanned through the workflow's function: 0 findings.
- The pull-request and squash texts beside this file are NEW, written for the whole branch, and each was scanned as a commit
  message through the workflow's function: rc 0. Round 2's texts (`2026-11-20_B1778_verify/`) describe round 2's head and must
  not be used.

## 2. What the coordinator does next (no decision is asked of the product owner by this verdict)

Open the pull request with `pr-title.txt` and `pr-body.md`; follow `landing.txt` (the check wait, the three lines to keep from
the pull-request run's `secret-scan` log, the `mergeable_state` read, the head-pinned squash with BOTH the subject and the
body given, the reads after). The one thing that can still go to the product owner is the case `mergeable_state` = `blocked`
on a green pull request (CodeQL): `CODEQL-FIRST-PR.md` of round 1 holds the steps and who does each.

## 3. Open clauses of WP0.3 and exit point E0.4 (the Jira Task `OXPD2-8` must NOT move to Done on a merge of this branch)

| Clause | State | Owner of the next step |
|---|---|---|
| The bundle tool in the pipeline and a test bundle | not built | STILL OPEN: a decision on how a runner obtains HP's tool, the product owner's |
| Secret scanning with no allow-listed paths | CLOSED BY ROUND 3 as far as a scan of stored objects goes: file names, first bytes, commit and tag messages, header lines, file and folder names. The seven named limits stay | a backlog line per limit that is worth closing (section 5) |
| CodeQL | no analysis exists; the first pull request will show none | STILL OPEN: the coordinator reads it; an owner rules if it blocks |
| The development CA in a production bundle | mechanism only; 0 fingerprints; no release mode | STILL OPEN |
| HP's beta library in any release artefact | met for today's publish shape only | STILL OPEN |

## 4. The follow-ups of rounds 1 and 2, each marked

From round 1:
1. The name skipping, the missing deny-list test, the floor: CLOSED EARLIER (round 2). Not taken, STILL OPEN: the
   development-CA name rule as a substring and ZIP member names split on a backslash; the three line rules for quoted keys,
   escapes and flow mappings in workflows; a NUL-byte rule for tracked files.
2. OWNER DECISION, the four checks are required by nothing: **STILL OPEN**, unchanged on GitHub (re-read: the required list
   is empty, no pull-request rule, the branch not protected).
3. OWNER DECISION if the first pull request reads `blocked`: **STILL OPEN**, unchanged.
4. COORDINATOR RULE into `<P>/CLAUDE.md` (a diff touching `.github/**`, `build/**`, `global.json`, `Directory.Build.props`,
   `Directory.Packages.props`, `NuGet.config` or a lock file always gets a tier-1 gate): **STILL OPEN** (not re-read in round 3).
5. RELEASE MODE of the guard: **STILL OPEN**; backlog line 14.
6. THE GUARD before the publish shape changes (single-file hosts, other archives, key stores, UTF-16 PEM): **STILL OPEN**.
7. `RuntimeIdentifiers` into `Directory.Build.props`: CLOSED EARLIER (round 2).
8. THE LAUNCHER's three dotnet variables and the runbook's launch notes: **STILL OPEN**.
9. After the first merge, read the code-scanning setup, the analyses on `main` and the open alerts: **STILL OPEN**.

From round 2:
1. The second scan exports files only (its Major): **CLOSED BY ROUND 3**, measured.
2. The read cut: **CLOSED BY ROUND 3** for a file with no blank line (0 of 45,000 token lines lost by both copies in four
   files); the file with blank lines is a named limit, and for a token the gate could not produce it (section 5, line 5).
3. Three byte marks: **CLOSED BY ROUND 3 on every measured row** (eight rows, by the second copy). The README claims nothing
   about it; that no mark lies beyond the block is DERIVED, not re-read.
4. The fingerprint covers two jobs, not the workflow: **STILL OPEN**, an owner's setting; backlog line 15 now words it
   truthfully. Later hardening as round 2 said: fingerprint the whole file; `BASH_ENV` and escaped keys into the line rules.
   Re-run once in round 3: the scanner's configuration variable set outside the job still passes the plant (`25 of 25`) and
   hides a real token.
5. A root ignore file read by the second scan: **CLOSED BY ROUND 3** (the step fails on it: a file, a link, a dangling link,
   a folder).
6. Every run reads every branch; no ignore mechanism: **STILL OPEN as a procedure to write**; now in backlog line 16. Round 3
   adds the case of `main` (section 5, line 2).
7. Rules keyed on a file name do not fire under a neutral name: **STILL OPEN**, named in the README and in backlog line 16.
8. False reds of the fingerprint (a job added after `rules`, a top-level block moved below `jobs:`): **STILL OPEN**; say in
   the README how a lane adds a job.
9. Scale, one `git` process per stored object: **STILL OPEN**, and round 3 doubles the copies. The drafter's figure: 3052
   objects, 31.6 s on this machine. The gate's: 71 objects 1.4 s; a 96 MiB file 0.3 s to export and 9.5 s to scan.
Records of round 2: runbook lines 14 and 50, backlog lines 9, 15 and 16: **CLOSED BY ROUND 3** (frozen texts in place, byte
for byte). Runbook line 29 (19 Jira issues): STILL not re-read by any round since the first. Runbook line 60 now says its
runner is a seat's own file and not in the repository: CLOSED.

## 5. New from round 3: follow-ups to file (each a backlog line; none blocks the merge)

1. THE README'S "branches and tags only" (finding 1): on a pull-request run the checkout also fetches that pull request's
   merge commit, and reads it. Reword `README.md:72` and `:73` and `BACKLOG.md:99` in the next lane that touches the README.
   First, MEASURE it: keep the fetch line of the first pull-request run's `secret-scan` log (`landing.txt`, line 1).
2. A FLAGGED MESSAGE ON `main` IS PERMANENT (finding 2): `main` cannot be rewritten and there is no ignore mechanism. Standing
   step: scan the exact squash subject and body through the workflow's function before every merge
   (`/private/tmp/b1783-gate/scripts/texts.py` is the method; it is the gate's file, not in the repository: a lane should put
   a small script of that kind into `build/`). A decision for later: an allow-list by object id inside the fingerprinted job,
   or an owner lifting the ruleset once.
3. THE EXPORT'S OWN CHECKS (finding 3): require each first copy to be 55 bytes longer than its object (`%(objectsize)`);
   count the listing by lines read, not by line ends.
4. THE PLANTED COUNT (finding 4): the sum 25 can be balanced by two faults and does not prove the block's length; the
   fingerprint is the only guard. One planted repository per place (the kit's Question Q4) removes the sum.
5. THE NAMED LIMIT OF A FILE WITH BLANK LINES (finding 5): reword backlog line 16 to "only for a secret longer than about
   2 kB, a private key block for example"; measured: 0 of 1,389,000 token lines lost by both copies; a 3247-byte block across
   both cuts: 0 findings.
6. NOT NAMED AND NOT STORED HERE (finding 6): a file kept by Git LFS (add a rule that refuses `filter=lfs`); the content of
   a submodule; a value joined on one line or encoded another way. And one sentence for the procedure of round 2's line 6:
   removing a branch does not remove its commits from the origin while a pull request's ref reaches them; they are only no
   longer fetched.

## 6. `<P>/BACKLOG.md`: lines to change or add (its 18 lines are each real; none is to be removed)

- Line 9: ticked by round 3. Done.
- Line 15: reworded by round 3. Done.
- Line 16: reworded by round 3; two phrases to correct later (section 5, lines 1 and 5).
- Add: section 5's lines 2, 3, 4 and 6; round 2's lines 4, 8 and 9 if they are not there yet.
- Still missing from round 1's list: the guard's publish-shape limits (extend line 11 by the single-file case); the `.pdb`
  files and the `web.config` in the published folders; `actions/setup-dotnet` pinned to the commit of `v6.0.0` while a newer
  release existed on 2026-11-20 (not re-read in round 3). New observation of round 3: the pinned `actions/checkout` commit is
  the one its tags name `v7` and `v7.0.1`.

## 7. `<P>/SETUP_RUNBOOK.md`

- Lines 14, 21, 50, 60, 66, 80, 86, 87: changed by round 3 and checked true at the head (line 87 does not carry the phrase of
  finding 1; backlog line 99 does).
- Line 29 (19 Jira issues): not re-read.
- After the merge: line 21 (the lane branch) and line 66 (the hosted pipeline) need the pull request, the squash commit and
  the first run on `main`.

## 8. Jira `OXPD2` (NOT read in rounds 2 and 3; round 1's reading carried, unverified since)

- `OXPD2-8` stays open (section 3). The backlog lines 14 to 18 and the follow-ups of sections 4 and 5 have no ticket.
- `OXPD2-10` describes work another agent did on 2026-11-20: STILL OPEN, the coordinator's.
- Four Task texts name no requirement row (`OXPD2-8`, `-9`, `-10`, `-16`): STILL OPEN; round 1's table says what each should cite.

## 9. What the gate leaves on this machine

- `/private/tmp/b1783-gate/` (2.8G when measured): the clone (push URL invalid), the probe repositories (they hold the gate's
  random planted tokens and a few key-shaped blocks of random bytes: fake values, built by program, never printed, in no project
  repository), the CodeQL databases, the four hosted logs, the logs and the scripts, three `_quarantine_*` folders of first runs.
  A reboot clears it. Reusable: `scripts/scan3.py` (every row of the three rounds through both functions), `step3.py`,
  `attack3.py`, `sweep.py`, `keyblock.py`, `texts.py`.
- `/private/tmp/b1778-gate/` (round 2's) was read, not written.
- No process left running; nothing written under the project folder or its `.tools`; the seat's checkout reads the round-3
  head with an empty porcelain, untouched.

## 10. NOT measured by any of the three gates (carry these as open, not as passed)

A pull request, its checks and its fetch line; whether the ruleset blocks the first merge; CodeQL for C#; the step run on Linux
by a gate's own hands (the hosted run proves the plant and the real repository only); Windows and `docker build` locally;
whether GitHub accepts the escaped key and the block-text name of round 2's finding 4; a file kept by Git LFS; telemetry on the
wire; that 10.0.15 is the newest 10.0.x; billing; the launcher in a real run.
