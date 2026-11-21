GATE B1885: GO WITH FINDINGS @ b514a6b on main f01b907

Gate G1, round 1 of 2, whole-lane reader. OXPd 2, lane T: tolerant reading of printer callbacks (kit B1863 as stamped,
seat X27), head `b514a6b0cc475eb08b2fb80154b0200f51fd3ea0` (one commit, one parent `f01b907e`) on branch
`b1863/oxpd2-tolerant-reading`; main `f01b907e90a72b69386b0184653e6693bd857348`. Read and measured 2026-11-22, 09:35
to 09:50 AEDT (clocks by `date`), on Opus 5.5, in my own clone (session scratchpad `b1885-clone`, made by the kit's
`clone.py ... draft`: push URL `invalid://no-push`, no identity) and two detached worktrees of it (`b1885-red`: the
head with the BASE generator; `b1885-scope`: the head, untouched). Origin by `gh api -X GET` under the project
GH_CONFIG_DIR at 09:35:50 and again at 09:47:45: branch = b514a6b0, main = f01b907e, open pull requests 0, `compare
main...b514a6b0` ahead 1, behind 0, 17 files (Tuesday's figures); open code-scanning alerts on main 0. Tools: the
fourteen files of `fleet/state/s306/d1863/gate/` copied, fourteen of fourteen equal to the kit's THE TOOLS by sha256;
`words.py --control` `CONTROL FIRED: 13 of 13`; my own regen project copies point their one `Compile Include` at my
clone / worktree (a one-line diff each). Every heavy job went through the kit's `heavy.py` (sha256 `31adedc8...`):
load1 first, the wave lock `<project>/.tools/wave1-heavy.lock.d` by `mkdir` with `owner.txt`, released by a move into
`/private/tmp/b1885-gate/_quarantine/locks/` (60 jobs; waits 0 on 58, 1 and 2 polls on two, shared with B1886: waits,
not findings; `evidence/gate.log`); restores `--locked-mode -p:NuGetAudit=false` with `CI=true`. `repo_rules.py` never
got `--source-documents`; nothing under `Source_Documents/` and no key folder was hashed, listed or opened; synthetic
values only, none printed; no socket, no request to a printer or host. No write in the OXPd_2 project but the shared
lock; no git write outside my scratch clone; no GitHub write, no Jira, no mail. Logs: `/private/tmp/b1885-gate/`;
probes, mutant program, outputs and hosted readings in `evidence/`.

**BLUF.** The lane does what the ruling and the kit's D1 to D12 say and nothing more. Scope is the 17 owned paths; the
committed `Generated/` is a fresh generation of the edited generator; every K cell, N3 and P03 is red against the
base's generator by assertion and green at the head (K6b's red is test-only, reproduced by a test mutant); my 10 own
probes over H1 to H16 hold; my 13 generator mutants are all red, but ONE (the optional-null rule applied to the strict
client objects too) is caught only by my probe, not by any cell of the lane: a missing cell, Minor, the code is right.
Whole suite 1404 failed 0; hosted PASS; the merge is the head's own tree. Deviations: accepted or records. Landing
texts written. Can it land? Yes, once B1886 is also GO or GO WITH FINDINGS; main has not moved, so no rebase step.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor (test gap) | **No cell pins "a null in a device answer stays refused" (D3's stays-refused list; D4).** Mutant `mNullStrictToo` (the `schema.Tolerant` condition dropped from the optional-null rule, so client objects read an optional null as absent too) leaves every cell of the lane and every landed test green; only my probe G05 goes red. K8 checks the `Tolerant` flag, N14 checks unlisted enum values only. The code is right today: G05 measures 716 client models refusing an optional root null `WrongType` at its path and 166 refusing an unlisted value `UnknownEnumValue`. | A K8 row: an optional null in a client model's body stays `WrongType` (in this lane's fix round if B1886 calls one; otherwise a follow-up). `FOR-RECORDS.md` item 3. |
| F2 | Records | **H8 (the seat's deviation):** the kit's "`DuplicateKey`, as today" is false of the base, which refuses `{"operationContext":null,"operationContext":...}` `WrongType` at the null (MEASURED: the red run's K4 message). The head refuses it `DuplicateKey`: the null is read as absent by D3 and the unchanged duplicate check (`names.Add` runs before the value is read) fires on the second key. A refusal before and after; no body moves from refused to accepted; the kit's own K4 cell names `DuplicateKey`. My ruling: inside D3's property, not a new behaviour. My mutant `mDupForget` (the name forgotten after a null) is red on K4 and G10. B1886 rules this point for the gate. | Records (`FOR-RECORDS.md` item 4); the pull request body states the changed kind. |
| F3 | Records | **The converter refuses enums without wire names** (the runtime's and the adapter's own enums) on write and read with `Oxpd2Json.Options` (MEASURED, G06: writing `Oxpd2RefusalKind.WrongType` throws; the stock converter wrote the name). Nothing in `src/` does so (`git grep`: the one `Oxpd2Json.Options` use outside `Generated/` serialises a generated answer model). The seat raised it. | Stated in the pull request body; records item 5. |
| F4 | Records | **K6b is a one-line scan**: a split comparison, a `switch`, a local holding the member or an alias is not caught; it does list every line naming a target enum (0 today: my own `git grep -w` of the 28 names over `src/` outside `Generated/`: 0 lines; control inside `Generated/`: 326). | Stated in the pull request body; records item 6. |
| F5 | Records | D8's README line on maps not added (one-sentence limit); the README sentence ends with a full stop inside a semicolon list; tolerance also reaches the targets' answer schemas (no effect: no enum, no null written). | Records items 8 to 10. |

No Blocker, no Major.

## What I re-ran, and the results

**Scope (THE OWNED PATHS).** `owned.py <scope worktree> f01b907e --control`: 17 rows each `OK` (16 `M`, `A
TolerantReadingTests.cs`), `OWNED: PASS (17 rows)`, `CONTROL FIRED: 3 of 3`. `git diff --quiet f01b907e --
contracts/oxpd2/hp contracts/oxpd2/inputs.sha256 .../Device .../Callbacks Datasec.Suite.slnx Directory.Packages.props
.github build README.md '*packages.lock.json'` rc 0 (control over `contracts/oxpd2/generator` rc 1); lock files in the
diff 0. Lane E's product code untouched; existing tests changed: only N3 (`InboundTests.cs`, +11 -3, the method only)
and lane E's `CallbackCellTests.cs` (the `unknown-enum` row moved, `null-optional` kept in P01, P03 added). Each of the
17 files printable ASCII, LF, final newline, no tab (control: a planted U+200B counts 1); README longest line 119.
`words.py` over the 1368 added lines and the commit message: `WORDS: clean (2 files)`; my own case-insensitive count
of owner/ruling/ruled/decid/approv/firmware/printer over the added lines: 4, two inside HP wire names in generated
schema lines, one the README's "A printer callback that carries ...", one the test class summary: no text says anyone
decided anything; no claim about how a printer or firmware behaves. Commit: author and committer the repository's
own identity (domain `datasec.com.au`), attribution `Co-Authored-By: Claude Opus 5.5`.

**The regeneration (D11).** `regen-head` over my clone at the head: `REGEN: 85 files, 3777458 bytes written; stale
files moved to quarantine: 0` (the seat's line), then `git status --porcelain` 0 lines: the committed `Generated/` is a
fresh generation of the edited generator, byte for byte and as a set. The changed set against main is D11's 11 files,
0 added, 0 removed (compare listing). Generator sha256 prefixes at the head `d8850334` / `2ceba872` (the seat's).

**Red first, with the generator as BASE holds it** (worktree `b1885-red`: the head with `Oxpd2RuntimeText.cs` and
`Oxpd2Unit.cs` taken from f01b907e, regenerated: `REGEN: 85 files, 3763086 bytes` = BASE's line, the 11 files back
to BASE): restore rc 0, build 0/0, whole suite `total: 1404`, `failed: 15`, `skipped: 4`, rc 2 by assertion: K1, K2,
K3, K4, K5, K6a, K7, K8, K9, K10, N3 x4 (UsbAccessories operationCallback, UserPolicy applyUserPolicy, JobStatistics,
ScanJob) and P03 (`P03: the parser itself refuses the case unknown-enum`); nothing else red. K6b is green there: its
scanner does not read the generator; its red-first was a stub (kit-prescribed); I reproduced its red with test
mutant `mK6bStub` (the offender line dropped: K6b red by `Assert.Single`, the only red). 15 + K6b = the seat's 16.

**Green at the head, the chain** (my clone): `restore --locked-mode` rc 0, lock files unchanged (rc 0); build `0
Warning(s)`, `0 Error(s)`, 22 assemblies; `dotnet test -c Release --no-build` (the workflow's form, no filter) `total:
1404`, `failed: 0`, `succeeded: 1400`, `skipped: 4` (the four Windows key-ring tests). `repo_rules.py <tree>` (no
option): `RULES-NOTE: R5 hash half NOT RUN`, `RULES: clean (444 files)`; `unittest discover -s build/tests` `Ran 60
tests`, `OK`. (I did not run the two publishes and the release guard locally; the hosted legs read them below.)

**THE REQUIRED SECTION, H1 to H16, by the seat's cells and my own probes** (`evidence/GateProbeTests.cs`, 10 tests in
the Contracts project of my clone only, never committed, moved to quarantine after; `evidence/probe-results.txt`;
with them the suite reads `total: 1414`, `failed: 0`):
- H1/D6: K6a and K6b green; G01: 24 hostile spellings of my own (`utsOk `, `utsOK`, `UTSok`, an escaped U+200B, a
  fullwidth `u`, escaped newline and tab, `utsok\u0000`, `utsStall `, `Unrecognized `, `unrecognized`, `-1`, `00`,
  `utsOk,utsOk`, a JSON-array text, `\u0000`, an emoji suffix, other enums' success words `jdsSucceeded` and
  `dsrSuccessful`, `uts Ok`, ...) each `Unrecognized`, `== UtsOk` false, count 1, the one site path; three fully or
  partly escaped LISTED spellings read their member, count 0.
- H2/D8: K10; G02 over all 46 request enum sites: the report names exactly the site, count 1, the site reads
  `Unrecognized`; EVERY listed value of every site reads its own member, count 0; maps: none (D8).
- H3/D4/D5: K8, K9, N14; G05 (clients: 716 optional nulls `WrongType`, 166 unlisted `UnknownEnumValue`); G06: a
  number, `0`, `null`, `true` for a non-nullable target enum throw `JsonException` (never `Unrecognized`), nullable
  `null` reads null, every one of 4692 listed members of the target and client enums writes exactly its wire name and
  reads back, `Unrecognized` of every target enum refused on write.
- H4/D7: K5; G01 above. H5: D9/D10 rows as the seat moved them (above). H6/H8/H14: K4; G10 (both duplicate values
  null `DuplicateKey`; a required key duplicated with null `DuplicateKey`; a required null inside an array item
  `MissingRequired` at `$.jobDetails[0].jobId`; an escaped spelling of an optional key with null: absent; a key
  differing by case: skipped). H7/H1/NOT DECIDED 2: K7; G03 (three nulls beside one member: a value; two members, or
  two with one unlisted: `OutOfRange`; all four null, `{}`, null beside an unknown member: `OutOfRange`; the
  registration result all null `OutOfRange`, `result` null `MissingRequired`); G04 (every one-of object reached from
  the 10 roots, 4 distinct, with only null members: refused).
- H9/H15: K3; G08 (ten bodies: the four- and six-argument overloads agree on value and refusal, a refusal reports 0
  and empty, the list refuses `Add`). H10/H16: K9, G06. H13: K5 rows. G07: escaped key spellings report the schema
  path only; an unknown key and sibling values holding a marker leave no byte in the report; a refusal after an
  unlisted value is `DuplicateKey`, count 0, no marker in its text. G09: 8 threads x 2000 parses through the shared
  options and converter: wrong reads 0.
- H11: N12 green in every whole-suite run; I did NOT re-measure its diagnostic split. H12 / H16 (iv): named limits,
  true of the code (the handler's catch-all ends a throwing sink `SinkFailed`, `Oxpd2CallbackHandler.cs:195`-`:198`;
  nothing in `src/` calls the six-argument overload: `git grep`, 0).

**NOT DECIDED 1 and 2 stay strict and unbuilt:** device answers strict (K8, N14, G05); a new one-of member skipped and
the object refused (K7, G03 f).

## Mutants of my own on the GENERATOR (`evidence/mutants.py`, `mutants.out`, `mutants2.out`)

Each: exact one-occurrence edit(s) (a `check` pass printed every one standing), regen, build (each 0/0), the whole
suite with my probes (each `total: 1414`), the failing names, then the original bytes restored and proved by sha256
(`undo: sha equal True` every time). After the last: regen `3777458 bytes`, `git status --porcelain` only my probe
file, build 0/0, suite 1414 failed 0; the probe file then moved out and `git diff --quiet b514a6b0` rc 0.

| Mutant | Edit | RED (seat cells; my probes) |
|---|---|---|
| mReportOnRefusal | the count assigned right after the walk, before the refusal check | K3; G07 |
| mPathCap | `<` to `<=` on the 16-path cap | K3 |
| mCountCap | the count raised only inside the cap | K3 |
| **mNullStrictToo** | `schema.Tolerant` dropped from the optional-null rule | **none of the lane's; G05 only (F1)** |
| mEnumAllTolerant | the walker's strict-enum refusal never taken | K8, N14; G05 |
| mWriteNull | `Unrecognized` written as JSON null | K9; G06 |
| mNotZero | `Unrecognized = 1000` | K1, K6a |
| mNoAttr | the attribute not emitted | K1, K2, K3, K5, K9, K10, N3, P03; G01, G02, G06, G07, G09 |
| mDupForget | the key forgotten after an optional null | K4; G10 |
| mClientDefault | the converter returns the default for any unlisted value, client enums too | K9 |
| mObjAll | client objects emitted tolerant | K8; G05 |
| mReadAsListed | an unlisted value read as the first LISTED member | K2, K5, K9, K10, N3, P03; G01, G02, G06, G09 |
| mWalkerCase | the walker's listed-value check ignores case | K5; G01 |
| mK6bStub (test) | K6b's offender line dropped | K6b |

One note on `mNoAttr`'s first run: my probe G09 dereferenced a null on a raw thread and crashed the Contracts test
host (total 1276, rc 1); I fixed my probe (a null counts as a wrong read) and re-ran the mutant: 16 red as above. A
probe bug of mine, not of the lane.

## Suite, hosted, the merge

- **Suite at the head:** `test-head` 1404, failed 0, skipped 4 (before any probe or mutant); after the mutants,
  `test-final` 1414 / 0 with my 10 probes in, and the clone then byte-equal to the head (`git diff --quiet` rc 0).
- **Hosted** (`hosted.py b514a6b0... --total 1404 --rules 444 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor
  60`, 444 = `git ls-tree -r` of the head): push run 44908620198, four jobs success, attempt 1; linux `total: 1404` x2,
  `succeeded: 1400`, `skipped: 4`, `failed: 0`, `0 Warning(s)`, `0 Error(s)`, `GUARD: clean (10 files)`; windows
  `total: 1404` x2, `succeeded: 1385`, `skipped: 19`, `GUARD: clean (11 files)`; secret-scan both PLANTED-CONTROL lines,
  `NEUTRAL-SCAN: stored objects 1036 (...) objects of this commit not among them 0` (the seat's local line), `no leaks
  found` x3; rules `Ran 60 tests`, `UNIT-TEST FLOOR: ran 60, floor 60`, `RULES: clean (444 files)`. `HOSTED
  b514a6b0...: PASS`; control `--skipped-linux 5`: `FAIL 2`. No Analyze rows on the branch push: code scanning is read
  on the pull request (landing step 3).
- **The merge:** `git merge-tree --write-tree f01b907e b514a6b0` rc 0, tree `74963933d4491290d8321a01361a96f8680fb267`
  = `b514a6b0^{tree}`; `merge-base --is-ancestor f01b907e b514a6b0` rc 0. Main has not moved (re-read 09:47:45), so the
  merged tree IS the tree I built and ran (1404 / 0). Lane I is not landed; landing.txt carries MAIN MOVES.

## The seat's deviations

1. N12's counts read from the Contracts assembly run directly: accepted (display only; N12 itself is green in the
   workflow-form whole-suite run, mine included). Records.
2. Display options on some test runs: accepted; none filters; the chain run and all of mine use the workflow's form.
3. H8, `DuplicateKey` asserted where the kit said "as today": inside D3 (F2 above); B1886 rules it for the gate.
4. The README sentence's full stop: text, harmless (F5); each clause of the sentence is true of the code (unlisted
   value read as `Unrecognized`: K2, G02; never written back: K9, G06; optional null absent: K4; required absent or null
   refused: K4, G10; device answers strict: K8, N14, G05).
Also the seat's departure from the prototype (the report assigned only on a value): correct and pinned (mReportOnRefusal
red on K3).

## THE LANDING TEXTS (in this folder)

`pr-title.txt`, `pr-body.md` (ends with the Claude Code line), `squash-subject.txt` (ends `(#PRNUM)`),
`squash-body.txt` (ends `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`), `landing.txt` (the B1877 form:
`pr_retrigger.sh --check`, `pr_checks_wait.sh --min-checks 8`, the csharp analysis at the head's sha first, alerts 0,
head-pinned squash, after-merge reads, MAIN MOVES), `FOR-RECORDS.md`. Each exported through the workflow's own
`neutral_export` (cut by program from the head's `ci.yml`, lines 120 to 128) as a commit message of a scratch
repository and scanned with the workflow's options: nine shapes, every one `no leaks found` rc 0, the planted control
`leaks found: 2` rc 1 (`evidence/texts.out`). Word counts with 16 of 16 controls fired: the four repository texts 0
on names, ids and decision words; pr-body's one non-ASCII character is the required robot line, its one "host" the
claude.com link and one "control number" the test name `P03_`; squash-body's one host is the attribution address.
`words.py` over the four: every class 0 but the 4 bytes of that emoji. landing.txt is Tuesday's working text (paths,
B-numbers), not repository text.

## What I did NOT test

The local publishes and release guard (read on the hosted legs only); CodeQL (none local; the pull request's
analyses are landing step 3); the Windows leg locally; N12's diagnostic split (not re-measured); the kit's nine named
mutants (the seat's own run; mine are beyond them); the drafter's probe program; any printer, device, simulator or
host; the R5 hash half of `repo_rules.py` (never run, by rule). D3, D5, D6 and D4 in depth and the H8 ruling are the
second reader's (B1886).
