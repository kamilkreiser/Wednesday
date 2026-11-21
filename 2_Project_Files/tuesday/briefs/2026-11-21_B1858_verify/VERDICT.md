GATE B1858: GO WITH FINDINGS @ cfa3185 on main 762e774

Gate G2 (Opus 5.5, in-session), round 2 of 2, a DELTA review. OXPd 2 lane A, WP3.8, the shared Graph HTTP layer: the
fix round (kit B1851, seat X14) at head `cfa31851274f44d90696b3554a0e27901920008b` on `b1832/wp38-graph-layer`, one
parent `f2b237d08565fbb07ad5a285c37b6b93d3cecc39` (the round-1 head). Main is now
`762e774eeac2eb324704c7e5ebf0ace86e018f04` (pull request 9, lane D's token broker, one parent 61b17ec0). Measured
2026-11-21 from 19:50:33 to 20:02:11 AEDT (clocks by `date`).

**BLUF.** GO WITH FINDINGS: no Blocker, no Major, no Minor. The findings are records only (round 1's R1 to R6, still
open by design; the named limit N13; two process records of the seat; one text note on the PR body). The tier stays
**G2**: no kept token, no persistence, no forbidden reach (my own reflection walk at cfa31851).
- **F1 of round 1 is fixed.** The 7 round-1 inputs and the 4 name sites (D3's own rows) each end
  `GraphCallException` of kind `MalformedResponse`, no inner exception, no `[XX]` byte form in any text: 28 of 28 of my
  inputs (with 17 more forms of my own). At round-1 head f2b237d0 the same probe gives 28 of 28 `InvalidOperationException`.
- **The fuzz, seed 20261847, 60,000 conversations:** other exceptions **0** (752 at f2b237d0 in the same run of the
  same probe: the control), 0 hangs, 0 over a request bound, 0 Authorization off the base origin or on an upload, 0
  waits past `MaxTotalWait`. My own upload fuzz (seed 20261858, 6,000 conversations, 9,127 spoiled range strings): 0
  other exceptions, 0 `[XX]` texts (2,756 escapes and 2,025 `[XX]` texts at f2b237d0).
- **The census holds:** exactly the seven sites (`GetString()` 3, `TryGetProperty(` 4), every other JSON text call 0;
  exactly 2 `catch (InvalidOperationException)`, no wider catch added (`catch (Exception)` 4 = round 1).
- **Suite 1091, 0 failed. Merge with 762e774e: clean, 1170, 0 failed** (= 973 + 176 + 21), RULES clean (368 files),
  build/tests Ran 60. Hosted run of cfa31851: PASS (both legs 1091).
- **Mutants:** mPage and mRange in my own form, plus one of mine: 3 of 3 red by assertion, each undone and proved.

**In plain words: the branch can be landed. Main moved (the token broker landed), but the branch merges with it
cleanly; the pull request's checks must be proved to have built the merge with 762e774e and must read 1170 tests on
both legs, Ran 60 and floor 60, then CodeQL's csharp analysis on the pull request (landing.txt).**

## How I worked

- **Read clone** `/private/tmp/b1858-gate/clone`, made by the kit's `clone.py` in mode `draft` (push URL
  `invalid://no-push`, no identity). The seven tools of the fix kit copied to `/private/tmp/b1858-gate/gate`: 7 of 7
  sha256 equal to its THE TOOLS; `words.py --control` `CONTROL FIRED: 13 of 13`.
- **Write verbs** (checkout, the scratch merge commit, the mutants) ran only in clones under the session scratchpad
  (`.../scratchpad/b1858/{head,merge,probe,probe1,mut,red}`, push URL `invalid://no-push`); the workspace hook refuses
  them elsewhere. The scratch merge commit `f35b8daa` (throwaway identity) is never pushed.
- **One runner for every dotnet job:** the kit's `heavy.py`, unchanged (`31adedc8...`). 23 jobs; each read load first,
  took the lock by `mkdir` of exactly `<project>/.tools/wave1-heavy.lock.d` with `owner.txt` after 0 waits, and MOVED
  it to `/private/tmp/b1858-gate/_quarantine/locks/` (23 folders). No lock folder is left in `.tools`.
- **Closed proxy** (the runner's), locked restores with `-p:NuGetAudit=false` (the closed proxy refuses the audit).
  Nothing was fetched: 0 log lines naming `http(s)://` or an `NU1xxx` code in each restore log, `git status
  --porcelain` 0 lines after.
- **Never** `repo_rules.py --source-documents`; no key folder opened; nothing under `Source_Documents/` read, listed
  or hashed. Logs in `/private/tmp/b1858-gate/logs/`; my probe `/private/tmp/b1858-gate/probe/GateProbe.cs`
  (sha256 `41acf76f...`, round 1's probe plus my sections F and Y); its reports `/private/tmp/b1858-gate/probe-out/report-probe-head2.txt`
  (cfa31851) and `report-probe-head1.txt` (f2b237d0).

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| R1 to R6 | Records | Round 1's records, unchanged by design (the fix kit's D7: records only): `MaxThrottleRetries` and `MaxNextLinkLength` unbounded; no time bound on the token source; redirects and default headers are the host's; the token as a string; one guarding test for the total-wait cap; the round-1 builder's `sed -i`. | FOR-RECORDS.md items 1 to 6. |
| N13 | Records | A `value` item holding text the reader cannot decode is returned unvalidated (a cloned `JsonElement`); a module that turns it into text meets .NET's refusal. Measured: round 1's shape `value item invalid UTF-8` is a value at cfa31851. NOT DECIDED (the fix kit's item 1). | For whoever writes the first module that reads page items. |
| P1 | Records (process) | Seat deviation 1, a stray `cd /dev/null` (failed, changed nothing); deviation 2, the boundary-scan control printed `tail`'s rc. | None beyond the record. My own C8 walk passed. |
| T1 | Text note | `pr-body.md` names `OXPD2-16` because this commission asks for it; `words.py` counts it as its one hit (ticket keys 1). The PR body is not stored in the repository; the squash texts are clean. | Keep (the commission's word) or drop the key; Tuesday's choice. |

## Item 1: the kit's FOR TUESDAY section

**The delta read whole.** `git diff f2b237d0 cfa31851`: 7 rows, all `M`: `GraphClient.cs` 33/17, `GraphCloud.cs` 1/1,
`Answers.cs` 6/0, `PagingTests.cs` 75/1, `RandomConversationTests.cs` 175/45, `Synthetic.cs` 26/0, `UploadTests.cs`
41/1; ls-tree 330 files (unchanged).
- The two clauses: `GraphClient.cs:368` in `FirstExpectedStart`, after `catch (JsonException)`, `return null` (the
  caller at `:239` turns null into `MalformedResponse`); `:717` in `ReadPage`, around the element reads inside
  `using (document)`, `throw Fail(GraphFailure.MalformedResponse, 0, 0)`. `Fail` (`:431-432`) builds the exception from
  the kind, status, attempts, wait and base host only: no inner exception. The `throw Fail(...)` lines inside the
  region throw `GraphCallException`, which the clause does not catch. Exactly `InvalidOperationException` both times.
- The two comments: `GraphClient.cs:133-135` now cites report A11 line 238 and "not measured against Graph";
  `GraphCloud.cs:9` cites report A1 line 363 and "not measured here". F2 of round 1 is closed.
- The rows: 9 page rows and 2 pinning rows, 10 upload rows (5 bodies x 2 paths), each built from `0xFF`-style byte
  literals and ASCII escapes through `Synthetic.JoinBytes` and `Answers.Bytes` (a `ByteArrayContent`); each asserts the
  exact type, the kind, `InnerException` null, no `\[[0-9A-F]{2}\]` in `Message` or `ToString()`, and the send count.
- The widened generator: bodies built as bytes; one JSON string in three spoiled by one of nine inserts (raw byte
  0x80-0xFF, `FF FE`, `C0 AF`, `E0 80 AF`, `ED A0 80`, `\ud800`, `\udfff`, and the valid `C3 A9` and `😀`);
  one body in ten gains an escaped name; reach counters asserted at least 1 BEFORE the problem check (so a pass proves
  the reach, which answers the seat's deviation 3); the seed in every problem line and in the assertion message; a
  `[XX]` text check per conversation.

**The census at cfa31851** (`/usr/bin/grep -c -F` over the 15 `.cs` files of `src/Datasec.Suite.Graph`, extracted by
`git archive`): `GetString()` 3, `TryGetProperty(` 4, standalone `GetProperty(` 0; `GetInt16/32/64`, `GetUInt`,
`GetDouble`, `GetSingle`, `GetDecimal`, `GetBoolean`, `GetGuid`, `GetDateTime`, `GetBytesFromBase64`, `GetRawText`,
`EnumerateObject`, `.Name`, `ValueEquals`, `JsonSerializer`, `JsonNode`, `Utf8JsonReader`, `JsonMarshal` 0 each.
Controls: `JsonDocument.Parse` 3, `namespace` 15. The six lines: S1 `:344`, S2 `:353`, S3 `:697`, S4 `:703`, S5 `:705`,
S6 and S7 `:708` (as the seat's FOR TUESDAY 1). The third `JsonDocument.Parse` is `IsJsonObject` (`:321-332`): it reads
`ValueKind` only, no text. **No site was added.** `catch (InvalidOperationException)` 2, `catch (Exception)` 4 (round
1: 4), `catch (JsonException)` 3, bare `catch {` 0.

**The F1 probe cases and the four name sites at cfa31851** (my probe, section F; the same probe at f2b237d0 is the
control):

| Input | cfa31851 | f2b237d0 |
|---|---|---|
| Round 1's 5 page shapes (nextLink invalid UTF-8, overlong, lone surrogate; deltaLink invalid UTF-8, lone surrogate) | 5 x `MalformedResponse`, 1 request, no `[XX]` | 5 x `InvalidOperationException` |
| Round 1's 2 upload range answers (invalid UTF-8, lone surrogate), each on the 202 path and the status-read path | 4 x `MalformedResponse`, 1 / 2 requests | 4 x `InvalidOperationException` |
| D3's 4 name rows (`value-name-lone-surrogate`, `next-name-lone-surrogate`, `delta-name-lone-surrogate`; `ranges-name-lone-surrogate` on both paths) | 5 x `MalformedResponse` | 5 x `InvalidOperationException` |
| My own name forms (`valu\udbff` with no value, `@odata.nextL\udc00 x3`, `@odata.deltaL\udfff x3`, delta name after a good nextLink, `nextExpectedR\udbff x4` on both paths) | 6 x `MalformedResponse` | 6 x `InvalidOperationException` |
| My own value forms (encoded surrogate `ED A0 80`, above U+10FFFF `F4 90 80 80`, truncated `E2 82`, low-then-high escapes; upload overlong and a third range `ED A0 80`, both paths) | 8 x `MalformedResponse` | 8 x `InvalidOperationException` |
| Valid: escaped pair, `C3 A9`, raw `FF` in a name, an escaped name BEFORE the real `value` | 4 x value | 4 x value |

Summary line at cfa31851: `F summary: inputs 28, MalformedResponse 28, other exceptions 0, [XX] in a text 0`; at
f2b237d0: `MalformedResponse 0, other exceptions 28, [XX] in a text 12`. Authorization on an upload in section F: 0.
(An escaped name placed before the real property is never decoded, because the reader matches the real one first: a
value at both heads, not a site.)

**The fuzz, seed 20261847** (round 1's section Z, unchanged): `Z seed 20261847: conversations 60000 (20000 per entry
point), requests 69028, other exceptions 0, hangs 0, over a request bound 0, Authorization off the base origin or on an
upload 0, waits past MaxTotalWait 0`. Control at f2b237d0 in the same probe: `other exceptions 752`, the round-1
figure exactly. Outcomes at cfa31851, paging: `MalformedResponse` 3486 (round 1's 381 + 371 escapes now land here).
**My upload fuzz** (section Y, seed 20261858; random 202 / 503-then-status-read / 200 answers, half the range strings
spoiled by one of 10 forms, one body in eight with an escaped `nextExpected...` name, `MaxPieceRetries` 0 to 3):
`spoiled range strings 9127, other exceptions or hangs 0, [XX] in a text 0, over a request bound 0, Authorization on
an upload 0`; at f2b237d0: 2756 escapes, 2025 `[XX]` texts.
**No-deny-list log and text scan** (round 1's, unchanged): a Serilog file logger at Verbose with no deny-list wrote
42,097,924 bytes; 124,935 exception and result texts kept. The planted access token, renewed token, path word, body
word, upload credential, source message word and `Bearer`: **0** each in the log and in the texts. `[XX]` byte form in
the texts: **0** (control: the pattern matches `bytes [FF] at`; at f2b237d0 it counts 2412). Control: the base host
162,746 times in the log. Every other round-1 section re-ran green at cfa31851 (`PROBE: PASS (0 failures)`): the
reflection walk (C8: no token-typed field outside generated async frames, every static readonly), 12 off-origin sends
refused, 34 next links with 0 tokens to another host, 58 of 58 Retry-After values equal my oracle, body reads stopped
at 1001 bytes, 0 bytes read on a 429.

**The suite at cfa31851** (head clone, through the lock): locked restore rc 0, build `0 Warning(s)` `0 Error(s)`,
`dotnet test -c Release --no-build`: **total 1091, failed 0, succeeded 1087, skipped 4** (the secret store's 4).
**Red first, re-run by me:** the head's tests over f2b237d0's product code (`git checkout f2b237d0 --
src/Datasec.Suite.Graph` in a scratch clone): total 1091, **failed 21**: the 9 page rows, the 10 upload rows, and the
paging and upload random facts; the seed lines equal the seat's (`seed 20261122: conversations 1621, ... 210, ...
111`; `seed 20261123: conversations 5000, ... 774, ... 484`). The pinning rows and the `SendAsync` fact green.

**Mutants (mine, in the mut clone at cfa31851; exact one-place replacements by `/private/tmp/b1858-gate/mutate.py`,
one heavy `dotnet test -c Release --no-restore` each, undone by the reverse replacement, proved by `git diff --quiet`):**

| Mutant | Edit (my form, not the seat's `when` filters) | RED by assertion | Undo |
|---|---|---|---|
| mPage | the `ReadPage` clause catches `FormatException` (never thrown there) | 10: the 9 page rows (`Assert.IsType() Failure`) and `GetPagesAsyncEndsInAResultOrAGraphFailure` | rc 0 |
| mRange | the `FirstExpectedStart` clause does `throw;` instead of `return null;` | 11: the 10 upload rows (`Assert.Throws() Failure: Exception type was not an exact match`) and `UploadAsyncEndsInAResultOrAGraphFailure` | rc 0 |
| mValueOutside (mine) | the `value` lookup (S3) moved in front of the guarded region | 2: `value-name-lone-surrogate` and `GetPagesAsyncEndsInAResultOrAGraphFailure` (`seed 20261122 conversation 136: escaped InvalidOperationException`) | rc 0 |

After the last undo: total 1091, failed 0, skipped 4.

**Words and gitleaks.** `words.py` over the 357 added lines and the commit message: `WORDS: clean (2 files)`; 0 lines
outside printable ASCII (control with a planted U+200B: 1); `owner|decid|approv|ruled|ruling|instruct|coordinator`
and the ban-list names 0 (control: `token` 12); 0 64-hex values. gitleaks 8.30.1 with the workflow's four options:
control (a provider-shaped value built from two halves) rc 1 `leaks found: 1`; the 7 changed files at cfa31851 under
neutral names, the added lines and the commit message: rc 0 `no leaks found`.

**Scope.** 7 `M` rows, all under `src/Datasec.Suite.Graph/` (2) and `tests/Datasec.Suite.Graph.Tests/` (5); no `A`,
`D` or `R`. `git diff --quiet f2b237d0 cfa31851 -- Datasec.Suite.slnx Directory.Packages.props .github build contracts
README.md global.json Directory.Build.props NuGet.config src/Datasec.Suite.Logging '*.csproj' '*packages.lock.json'`
rc 0 (control over `src/Datasec.Suite.Graph` rc 1). One commit, one parent f2b237d0; no package, project, lock or
workflow change.

**The hosted run of cfa31851** (`hosted.py`, unchanged, `--total 1091 --rules 330 --skipped-linux 4 --skipped-windows
19 --unit 53 --floor 53`): run 44886249190, attempt 1, four jobs success, every step success; linux `total: 1091` x2,
`succeeded: 1087`, `skipped: 4`; windows `total: 1091` x2, `succeeded: 1072`, `skipped: 19`; both `0 Warning(s)`,
`0 Error(s)`, `GUARD: clean (10 files)` / `(11 files)`; secret-scan both PLANTED-CONTROL lines, `no leaks found` x3,
`objects of this commit not among them 0`; rules `Ran 53 tests`, `UNIT-TEST FLOOR: ran 53, floor 53`, `RULES: clean
(330 files)`. Last line `HOSTED cfa31851...: PASS`. Control `--total 1092`: `FAIL 4`. The 19 skipped lines on windows
all name `Datasec.Suite.Secrets.Tests`, 0 name `Datasec.Suite.Graph`.

## Item 2: the merge with main 762e774e (holds)

- Refs by GET (19:50:33): branch `cfa31851`, one parent f2b237d0; main `762e774e`, one parent 61b17ec0, tree
  `e1489d23`; `compare 762e774e...cfa31851`: diverged, ahead 2, behind 3, merge base 5e36d8dc; 0 open pull requests
  (1 to 9 closed, none with this head).
- `git merge-tree --write-tree 762e774e cfa31851`: **rc 0, CLEAN**, tree `84b6bc8135f8f1f1b5f635fea9f4c4d4fb6919a8`
  (368 files). Against main: 40 paths, 39 added under the two lane folders and `Datasec.Suite.slnx` M with numstat
  2 / 0. The merged solution file holds lane D's two Sessions lines and this lane's two Graph lines, each folder in
  ordinal order (Graph after Core, Sessions after Server; Graph.Tests after Core.Tests, Sessions.Tests after
  Secrets.Tests). The lane folders of the merged tree equal cfa31851's (`git diff --quiet` rc 0; control against main
  rc 1).
- The merged tree in a scratch commit, through the lock: locked restore rc 0 (nothing fetched), build `0 Warning(s)`
  `0 Error(s)`, **total 1170, failed 0, succeeded 1166, skipped 4** = 973 (main's push run, linux and windows `total:
  973`, read by `hosted.py`: PASS) + 176 + 21, as expected.
- `python3 -I build/repo_rules.py <merged tree>` (no `--source-documents`; the folder beside the root holds no
  `1_Project_Definition`, `test ! -e` rc 0): `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)`,
  **`RULES: clean (368 files)`**, rc 0. `python3 -I -B -m unittest discover -s build/tests`: **`Ran 60 tests`**, `OK`;
  the merged `ci.yml` holds `FLOOR=60`. (The head alone: `RULES: clean (330 files)`, `Ran 53 tests`.)

## Item 3: the seat's deviations

| # | Ruling | The line that proves it |
|---|---|---|
| 1 | ACCEPTED, process record (P1) | STATUS DEVIATIONS 1: a `cd /dev/null` that failed; every path absolute; the tree is unaffected (scope above) |
| 2 | ACCEPTED, process record (P1) | the 4 HIT lines are the control's proof; my own C8 reflection walk at cfa31851 passed (probe section G, `PROBE: PASS`) |
| 3 | ACCEPTED | `Judge` asserts both reach counts at least 1 before the problem check, so a green fact proves its reach; the red run shows the counts (my red-first re-run: 210/111 and 774/484) |
| 4 | ACCEPTED, true | `git diff --name-only 5e36d8dc 61b17ec0 | wc -l` prints 14 |
| 5 | ACCEPTED, true | my red-first re-run: `UploadAsyncEndsInAResultOrAGraphFailure` red at f2b237d0 with no share raised; mRange turns it red at cfa31851 |

## STATUS claims, graded

| Claim | Grade |
|---|---|
| local total 1091 (1070 + 21), skipped 4 | true (mine) |
| red first: 21 failed, exactly the 19 rows and two facts; seed lines | true (mine, same seed lines) |
| `GraphClient.cs` and `GraphCloud.cs` equal FACT 7 | true (mine: `13b0eded...` and `6a693631...` at cfa31851) |
| seven sites at `:344 :353 :697 :703 :705 :708`; clauses at `:368 :717` | true (mine) |
| mPage red 10, mRange red 11 | true in kind (mine: 10 and 11, different forms) |
| hosted PASS, both legs 1091, Ran 53, RULES clean (330) | true (mine) |
| restore fetched nothing; no lock file changed | true (mine, same form) |
| main did not move during the round (61b17ec0 at the push) | true at the push (19:43:59); main moved to 762e774e at 19:44:55 |
| merged expected 1096 with 61b17ec0 | superseded: main is 762e774e, merged total 1170 (mine) |

## Item 4: the landing texts

Written: `pr-title.txt`, `pr-body.md`, `squash-subject.txt` (ends `(#PRNUM)`), `squash-body.txt` (ends the one
attribution line), `landing.txt` (main moved: `pr_retrigger.sh --check` against 762e774e; `pr_checks_wait.sh
--min-checks 8`; CodeQL analyses on `refs/pull/N/head` at the head's sha first, then alerts 0; the merge's legs 1170,
rules `RULES: clean (368 files)`, `Ran 60`, `floor 60`; head-pinned squash; after-merge reads with tree 84b6bc81),
`FOR-RECORDS.md` (R1 to R6, N13, the runbook and README lines). Each exported through the workflow's own
`neutral_export` (cut by program from the merged `ci.yml` from line 120; identical at cfa31851) as the message of a
commit object in a scratch repository and scanned with `--no-banner --redact --ignore-gitleaks-allow --exit-code 1`:
title, title + body, body, the squash message with a number, squash body, squash subject, landing.txt, FOR-RECORDS.md:
export rc 0, message stored whole, scan rc 0, `no leaks found`, 8 of 8; control (the squash message plus a planted
token built at run time) rc 1, `leaks found: 2`. `words.py` over the title, the squash subject and the squash body
without its attribution line: `WORDS: clean (3 files)`; the squash body whole: `WORDS: clean (1 files)`; the body
without its footer: `ticket keys 1` (`OXPD2-16`, asked for by this commission; T1), every other class 0. All ASCII
except the body's footer line. Every number in the texts is this reader's measurement or a RELAYED line marked so.

## NOT RUN / NOT TESTED

- Anything on Windows locally (the hosted windows leg ran 1091 at the head; the merge on Windows waits for the pull
  request's run).
- C# CodeQL: it cannot extract on this arm64 machine, and no analysis exists on the branch (0 on the ref by GET); the
  pull request's csharp analysis is the only C# proof (landing step 3).
- `dotnet publish` and the release guard locally (the hosted GUARD lines were read).
- A real `HttpClientHandler`, sockets, redirects, proxies, decompression; no listener was started. Any real Graph
  answer or tenant.
- Round 1's nine mutants (Q10) and the seat's exact mPage / mRange forms (mine are different forms of the same two).
- `repo_rules.py --source-documents`, `nocopy.py`, anything reading `Source_Documents/`.
- Concurrency beyond the builder's 50-call test; my fuzz runs its conversations one after another.
