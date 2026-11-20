# FOR RECORDS: what a records pass must file after gate B1772 (round 1, NO GO @ a0f9bdc on main 7e1a01c)

The gate wrote nothing outside its verify folder and `/private/tmp/b1772-gate/`. Everything below is for the coordinator to file;
none of it was filed by the gate. `<P>` = the project folder of OXPd 2.

## 1. State to record

- Verdict: NO GO at `a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89`, one Major (the secret scan skips 14 of 24 file names tried, by the
  scanner's built-in list), eleven Minor. No Blocker. Round 1 of 2.
- `main` = `7e1a01cf640f8abac89e7148322651be8e4bf15b`; the lane branch = the head above; pull requests 0; nothing merged, nothing
  deployed, nothing sent. Read 2026-11-20 13:54 AEDT.
- The lane's hosted run `44661506229`: 4 jobs success, attempt 1; every quoted line confirmed in the logs.
- The build, both fixed faults and the lock-file drift were reproduced by the gate.

## 2. Open clauses of WP0.3 and exit point E0.4 (the Jira Task `OXPD2-8` must NOT move to Done on this merge)

| Clause | State | Owner of the next step |
|---|---|---|
| The bundle tool in the pipeline and a test bundle | not built | a decision on how a runner obtains HP's tool: the product owner's |
| Secret scanning with no allow-listed paths | not met as worded until the Major is fixed | the build seat, round 2 |
| CodeQL | no analysis exists; the first pull request will show none | the coordinator reads it; an owner rules if it blocks |
| The development CA in a production bundle | mechanism only; 0 fingerprints; no release mode | a lane, once the certificate can be read |
| HP's beta library in any release artefact | met for today's publish shape only | the lane that changes the publish shape or adds packaging |

## 3. Follow-ups to file (each a backlog line; the first is round 2 of this lane)

1. ROUND 2, same branch, one new commit: finding 1 (refuse tracked paths the scanner skips by name, each with a planted control; or
   scan tracked content under neutral names). Suggested in the same commit because they sit in the same two files: a test that a
   missing deny-list is exit 2 (the one surviving mutant); the development-CA name rule as a substring and ZIP member names split on
   a backslash too; the unit-test floor raised from 16 to the real count; the three line rules for quoted keys, escapes and flow
   mappings in workflows; a NUL-byte rule for tracked files.
2. OWNER DECISION, to the product owner as one question: the four checks are required by nothing. Options: a repository ruleset
   on `main` (pull request required; `linux`, `windows`, `secret-scan`, `rules` required from GitHub Actions); and, because a pull
   request can edit its own checks, a required workflow at organisation level or code-owner review for `.github/**` and `build/**`.
   Also his: GitHub's own secret scanning and push protection read `disabled` on this repository.
3. OWNER DECISION, only if the first pull request reads `blocked`: the one-merge ruling of CODEQL-FIRST-PR.md.
4. COORDINATOR RULE to write into `<P>/CLAUDE.md`: a diff that touches `.github/**`, `build/**`, `global.json`,
   `Directory.Build.props`, `Directory.Packages.props`, `NuGet.config` or a `packages.lock.json` always gets a tier-1 gate; the
   landing wait of landing.txt is the only guard while no check is required.
5. RELEASE MODE of the guard before any job packages, publishes or uploads an artefact: 0 fingerprints is exit 2; `--denylist`
   away from the tracked file is refused; the job calls the guard on the very folder it packages.
6. THE GUARD before the publish shape changes: the library's name searched in every binary file, not only files starting `MZ`
   (a Linux single-file host starts `ELF`); an archive it cannot open (gzip, tar, xz, zstd, 7z) is a finding; key stores and
   certificate containers it cannot read are a finding; UTF-16 PEM text and the two other PEM labels.
7. `RuntimeIdentifiers` into `Directory.Build.props` before the next lane adds a project the host references.
8. THE LAUNCHER (the coordinator's frozen text): export `DOTNET_CLI_HOME`, `HOME` or `NUGET_PACKAGES` beside `DOTNET_ROOT`; say
   in the runbook that it starts with permissions skipped, pulls nothing, and trusts the host key on first use.
9. After the first merge: read `code-scanning/default-setup` (languages), `code-scanning/analyses` on `main`, open alerts; record
   them; any alert is fixed forward, never dismissed.

## 4. `<P>/BACKLOG.md`: lines to add (its 13 lines are each real; none is to be removed)

- The scanner's built-in skip list (finding 1) until round 2 lands; then the scanner's own limits: UTF-16 text, archives, a token
  split over lines.
- No check is required by a repository setting; the checks run from the commit they check (finding 2).
- The guard's release mode (finding 3) and its publish-shape limits (finding 4): extend line 2 and line 11.
- The R5 hash half cannot run on a runner and does not know HP's library; a renamed binary is seen by no check (finding 7).
- Whether hosted minutes on this private repository are billed: UNMEASURED.
- The published folders hold `.pdb` files and, on Windows, a `web.config`: decide before the first package.
- Line 7 can be closed without a registry call: the hosted `linux` log prints the digest the tag resolved to on 2026-11-20,
  `sha256:12b1135f5f8b3c0a214f2a680ff2033dff4f684f445d6c697d9524ceeb303586`.
- `actions/setup-dotnet`: pinned to the commit of `v6.0.0`; the newest release read `v6.1.0` on 2026-11-20.

## 5. `<P>/SETUP_RUNBOOK.md`: two sentences to correct

- "Everything after that commit reaches `main` by pull request only": true as the project's rule; no GitHub setting enforces it
  (the ruleset holds no pull-request rule and the deploy key can write). Say which it is.
- "Owed: a second launch of it by a person": it has never been launched; BACKLOG line 8 says "first". Make them agree.

## 6. Jira `OXPD2` (read by GET on 2026-11-20; the gate wrote nothing)

- 19 issues, all Backlog. `OXPD2-3` to `OXPD2-19`: 17 of 17 equal to the frozen texts (summary, type, parent, labels, every
  paragraph); 5 Epics without parent; each Task under the Epic the kit names; no assignee, no link.
- **`OXPD2-10` ("[WP0.5] HP engagement: draft the questions to HP") describes work that was done today by another agent.** A
  comment on `OXPD2-1` created 2026-11-20T13:28:43 says a draft of the questions to HP exists (2026-11-20), and `OXPD2-10` itself
  now holds 1 comment that the build seat did not write. Its text still lists the draft as the work to do now. Changing the
  ticket (state, text, a link to the draft) is the coordinator's.
- `OXPD2-1` now holds 4 comments (the STATUS read 3) and `OXPD2-2` holds 1.
- **Four Task texts name no requirement row, although `<P>/CLAUDE.md` asks each ticket to cite the F row it serves.** The plan's
  own rows for these four packages hold 0 F ids (counted by program; control: the row of WP0.6 holds 3). What each should cite is
  the gate's reading of the design and is the coordinator's to confirm:

| Ticket | Package | Says today | Should cite |
|---|---|---|---|
| `OXPD2-8` | WP0.3 | "plan E0.4; architecture N1 (no secret in source). No F row is named for this package." | No F row exists for a pipeline. Keep E0.4 and N1; add the packaging decision (both packagings equal, the plan's line 389) and the risk row on HP's beta library (the architecture's R16). Say "F: none (infrastructure)" so the rule is answered, not skipped |
| `OXPD2-9` | WP0.4 | "architecture component C2. No F row is named for this package." | The rows the OXPd 2 adapter carries, first F1 (the sign-in method the device calls, architecture line 64); and the plan's exit point for this package, which the text does not name |
| `OXPD2-10` | WP0.5 | "plan E1.9. No F row is named for this package." | No F row: it is an engagement, not a feature. Keep E1.9; add the four undated HP items (the architecture's D33) and the clarification that HP confirmed. Say "F: none (engagement)" |
| `OXPD2-16` | WP3.8 | "plan E3.3. No F row is named for this package." | The app rows the shared Graph layer serves: F35 (Mailflow, architecture line 95), F37 (OneDrive, line 97), F39 (SharePoint, line 99), F40 (Teams, line 100) |

- The rule itself (`<P>/CLAUDE.md`: "each cites the work package and the requirement row it serves") has no wording for a package
  that serves no F row. Either the rule gains "or says F: none and why", or these four are a standing exception: the coordinator's.

## 7. What the gate leaves on this machine

- `/private/tmp/b1772-gate/` (696M when measured): the clone (push URL invalid), the build output, the gate's package cache and
  home, the probe trees, the CodeQL databases, the logs and the scripts. Nothing in it is a secret; the gate's own throwaway
  certificate and its key are in `probes/ca/`. A reboot clears it. Round 2 can reuse `scripts/` and `logs/` if it is still there.
- No process left running; nothing written under the project folder or its `.tools`; the seat's checkout reads porcelain 0 at the
  head, untouched.

## 8. NOT measured by the gate (carry these as open, not as passed)

A pull request and its checks; whether the ruleset blocks the first merge; CodeQL for C#; Windows and `docker build` locally;
telemetry on the wire; that 10.0.15 is the newest 10.0.x; billing; whether GitHub accepts the two escaped YAML spellings; the
launcher in a real run.
