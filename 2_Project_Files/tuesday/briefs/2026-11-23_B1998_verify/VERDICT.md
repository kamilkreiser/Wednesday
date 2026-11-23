GATE B1998: GO WITH FINDINGS @ 81ae47e on main d804de5

Gate G1 (security surface: what passes out of a network client, the strict parser of device answers), round 1 of 2 of
lane FK, one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, lane FK, kit B1993 (seat X54; Q1 = a in
words at stamp S4, Q2 to Q7 the defaults, each the coordinator's, not the product owner's). Head
`81ae47ede965e015d5577a7491b4d6b0bd018805` on `b1993/fk-contract-runtime-follow-ups`, ONE commit, one parent
`d804de5e` (= main at 18:16:38 and 18:33:52). Read and measured 2026-11-23 18:15 to 18:36 AEDT in my own scratch
`fleet/state/s317/g1998/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity) and its worktree `red`
(BASE, then + `1-red.diff`, then + `2-fix.diff`). Every dotnet job and test executable through the kit's `heavy.py`
(sha256 `31adedc8...`) and the wave lock, one at a time (lock waits 0 to 2; no other holder's lock touched; 26 of my
lock folders in `g1998/_quarantine/locks/`). Origin by `gh api -X GET` under the project GH_CONFIG_DIR, and one `git
fetch` of L4's branch into my own clone. No write to the project, GitHub or Jira; no push, no pull request, no re-run;
nothing deleted (probe file and scanner control moved to `g1998/_quarantine/`). No network beyond the origin and the
probe's 127.0.0.1.

**BLUF.** The head is BASE plus the two frozen patches byte for byte (`red` after both: `write-tree` `2d6d5400` = the
head's tree by gh api; patches and the 12 tools equal THE TOOLS' sha256 in my copy and in the seat's `.tools/b1993/gate`).
19 paths (18 M, 1 A), the owned set; 32 changed lines under `src/`, all `///` (C6, and my own count). Red first at BASE
+ `1-red.diff`: 1945 / 1 failed / 1940 / 4, the one red `BodyReadTests.Every_client_names_what_passes_out_of_its_methods`
by its own `Assert.True` message. At BASE alone **all four mutants survive** the landed suite (`Total 149 Failed 0`
each; the kit measured only `mNullAfterFirst` there): the three new cells and the new K8 close four real gaps. At the
head: 4 of 4 MATCH, each red on exactly its cell, 4 undone, rebuilt (adapter dll 18:28:48 later than the last undo
18:28:23), green again 1945 / 0 / 1941 / 4. A regeneration from the head's generator rewrote the 85 files (3780946
bytes) and `git diff --quiet` stayed rc 0: the committed `Generated/` is the program's. K8's 716 and 2117 equal an
independent count, two ways, from the committed generated text. The two summary lines are TRUE on every path of
`Oxpd2ClientCore`: all 201 public methods of the 16 clients call `SendForJsonAsync` (201 calls), `SendRawAsync` has 0
callers, `ReadBoundedAsync` and `SendForJsonAsync` hold no `catch` (the only three in `Generated/` are the parser's
`JsonException` / `InvalidOperationException` over a byte array), and a non-success status returns before any
`ReadAs`. Hosted push run 45128961671 PASS (linux 1941, windows 1924; the LF text cell green on Windows). Merge with
main of the moment = the head itself. One Minor finding (text, not code); nothing blocks the landing.

## FOUND

1. **Minor (repository text a caller reads as a list: true, incomplete).** The new summary names two types that pass
   out; a caller who catches exactly those meets others, and "never reads" is the client's code, not the platform's.
   MEASURED by a gate probe (`G1998Probe.cs`, 7 facts, a real `SocketsHttpHandler` against a raw answer on 127.0.0.1,
   in `red`, never committed, moved to `_quarantine/G1998Probe-red.cs`; the Contracts executable whole `Total: 159,
   Errors: 0, Failed: 0`; output `scratch/probe-out.txt`): (a) P01, P02: a body that ends early (content length and
   chunked) leaves the method as `System.Net.Http.HttpIOException`, an `IOException`, as the sentence says (H4 now
   MEASURED on macOS); (b) P04: with a caller's handler that decompresses, a corrupt gzip body leaves as
   `System.IO.InvalidDataException`, neither named type; (c) P05: `HttpClient.Timeout` during the send leaves as
   `TaskCanceledException` (inner `TimeoutException`), not an `HttpRequestException`; (d) P06: `HttpClient.Timeout`
   (300 ms) does NOT bound the body read: headers then silence ended only at the caller's 3 s token (2916 ms,
   `TaskCanceledException`, inner `IOException`); (e) P03: two 404 answers with 1000-byte bodies on one HttpClient =
   2 requests on 1 connection: the platform handler drained the unread error body to reuse the connection. No probe
   result is parsed, handed back or made a refusal; the sentence holds as worded ("the client never reads"; "X and Y
   pass out", not "only X and Y"). No product code constructs any of the 16 clients today (the 16 class names occur
   nowhere under `src/` outside `Generated/`), so no caller is misled yet. Fix (the coordinator's order, a later round
   or the README pass): one more sentence ("also a cancellation, and whatever the caller's handlers throw; the platform
   may drain a non-success body it does not hand to the client") and a records line that the body read is bounded by
   the caller's token only (FOR-RECORDS.md item 1).

## INFO (each the gate's own reading; DERIVED marks source reading, not run)

1. **Every path of `Oxpd2ClientCore` (head, `:41` to `:109`).** `SendRawAsync` (`:41`): the raw answer, no body read,
   0 callers in the 16 clients (seat's DEVIATIONS 3 confirmed: 201 / 201 / 0). `SendForJsonAsync` (`:48`): `using`
   the response; status outside 200 to 299 returns `(status, null, null)` at `:57` before any read; a declared length
   above the limit returns TooLarge unopened (`:74`); else `ReadBoundedAsync`. `ReadBoundedAsync` (`:72`): `using` the
   stream; no `catch`, no wrap; the limit stops the read at limit + 1 bytes. Whatever `HttpClient.SendAsync` throws
   passes out (`:53`, no `catch`); `ReadAsStreamAsync` (`:79`) and `ReadAsync` (`:94`) the same. The parse (`:66`)
   reads a byte array only. No `LoadIntoBuffer` anywhere under `src/`.
2. **The cells.** `FailingContent` overrides `CreateContentReadStreamAsync`, so `ReadAsStreamAsync` hands its stream
   (or its fault) through unbuffered, as the real `SocketsHttpHandler` content does (P01, P02 agree); the identity
   check is `ReferenceEquals` and the type check exact (`Assert.ThrowsAsync<IOException>`), so D1 alternative (b)
   (a wrap into `HttpRequestException`) would turn the cell red (DERIVED). H19 (the `using` removed) is equivalent as the
   kit says: disposing the answer disposes the content and the stream it handed out (DERIVED). The text cell needs
   `\n` after each line: green on the hosted Windows leg (no CR LF there).
3. **K8.** The loop sends `Payloads.Minimal(strict)` plus one null per optional root property and asserts `WrongType`
   at `"$." + Name` with `value is null`; `mNullAfterFirst` (tolerate every optional null but the first) is red on K8
   alone at the head and green at BASE. Independent count (`scratch/k8count.py`, no reflection, no test code): (A) the
   1131 `Fill` blocks of the 16 client `Oxpd2Schemas.cs` mapped from the 1131 public models, `false` entries; (B) the
   `Wire name ...` summaries of the 16 `Models.cs` without `(required)`: both 716 models and 2117 properties, at the
   head and at `d804de5e` (the generated models do not change in this lane).
4. **The regeneration.** My `regen/` is the kit's two files with ONE line changed in my copy only: the `Compile
   Include` names my worktree's generator, not the seat's clone (the frozen file names `.tools/b1993/clone`). It wrote
   3780946 bytes (the head generator; BASE's writes 3777458), file times 18:25:35, then `diff --quiet` rc 0 and 19
   staged-only rows.
5. **Q1 a holds.** F1 to F3 are on main by pull request 7 (`0804860b`, ancestor of `d804de5e`, rc 0; its subject names
   all three); the cells and members item 36 names are present at BASE (FOR-RECORDS.md). Nothing owed is dropped:
   F4, F5, F7 and D11 stay in item 36 / 38 as the kit carries them; F6 is this lane.
6. **The commit message** equals `commit-message.txt` plus git's final line feed (342 = 341 + 1); its subject runs two
   clauses into one ("cells pin it and that a non-success body is never read"); the squash subject in this folder
   replaces it.

## WHAT I RAN (MEASURED; logs in `g1998/logs/`)
- Tools: 12 of 12 sha256 equal to THE TOOLS in my copy `g1998/gate` and in `<project>/.tools/b1993/gate`.
- Origin at 18:16 and 18:33: main `d804de5e`; `b1993` one ref = `81ae47ed`; compare ahead 1, behind 0, 19 files
  (+3 -1, 16 x +2, +213, +19 -12); head parents [`d804de5e`], tree `2d6d5400`; open pull requests 0 (newest 37); open
  alerts on main 0; main's Analyze rows at `d804de5e` csharp / python / actions results 0; the head's check runs four,
  all success, no Analyze row (a branch push).
- `red` at BASE: `red-restore` (CI=true, locked) rc 0. `mutants_fk.py ... run` at BASE (all four): every row `Total
  149 Failed 0 | red NONE | ... DIFFER | undone equal True`, `MUTANTS: 0 of 4 MATCH, 4 of 4 undone equal` (the
  expected survivors; `mNullAfterFirst`'s row equals the kit's required row exactly).
- RED (`1-red.diff`; the two test files' sha256 equal THE CODE's "After both"): `red-build` 0 Warning(s) 0 Error(s);
  `red-test` (no filter) `total: 1945`, `failed: 1`, `succeeded: 1940`, `skipped: 4`, `Test run summary: Failed!`,
  the one `failed ` line the text cell, message `ApplicationClient: its summary does not say what passes out of its
  methods`.
- GREEN (`2-fix.diff`, `add -A`, `write-tree` = `2d6d5400`): `regen-head` (above); `head-build` 0 / 0 (adapter dll
  18:25:54); `head-test` `total: 1945`, `failed: 0`, `succeeded: 1941`, `skipped: 4`, `Passed!`, `failed Datasec.`
  lines 0. `mutants_fk.py ... run` (one call, 8 heavy jobs): every row `Total 152 Failed 1`, each red on exactly its
  cell, `MUTANTS: 4 of 4 MATCH, 4 of 4 undone equal`. After: `diff --quiet` rc 0, `write-tree` `2d6d5400`, 19 rows;
  `post-mutants-build` 0 / 0; `post-mutants-test` 1945 / 0 / 1941 / 4.
- `checks_fk.py` on my staged tree: `CHECKS: 6 of 6 PASS` (C1 19 rows M 18 A 1; C2 32 shared paths rc 0, control rc 1;
  C3 0, control 1; C4 267 added lines; C5 0, control True; C6 32 lines, 0 not `///`, control True).
- `repo_rules.py` (no `--source-documents`; `test ! -e red/1_Project_Definition` rc 0): `RULES-NOTE: R5 hash half NOT
  RUN`, `RULES: clean (629 files)`; `unittest discover build/tests`: `Ran 111 tests`, `OK`.
- Merge with main of the moment: `merge-tree --write-tree d804de5e 81ae47ed` rc 0 = `2d6d5400` (the head: main is its
  parent). L4 (`26f4b57a`, fetched 18:34): `merge-tree 26f4b57a 81ae47ed` rc 0 = `9611a597`, shared paths 0.
- Hosted (head): `hosted3.py 81ae47ed... --total 1945 --rules 629 --skipped-linux 4 --skipped-windows 21 --unit 111
  --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15` (no --wait; the run had ended) rc 0: run
  45128961671 attempt 1 every job; linux `succeeded: 1941`, windows `succeeded: 1924`, `GUARD: clean (14 files)` /
  `(15 files)`, `RULES: clean (629 files)`, `NEUTRAL-SCAN: stored objects 1641 ... objects of this commit not among
  them 0`, `104 commits scanned`; last line `HOSTED 81ae47ede965e015d5577a7491b4d6b0bd018805: PASS`. `failed Datasec.`
  lines 0 and 0 (control: `Datasec.Suite.Contracts.Tests` 5 lines in each log).
- Probe (FOUND 1): 7 facts, all green as facts, output above.

## SCANS
- gitleaks 8.30.1: control FIRST (a token built by program from two halves and 36 random characters, never printed,
  outside any clone, scanned alone): rc 1, `leaks found: 1`, moved to `_quarantine/gl-control-*`. Then the head's
  message, the 267 added lines, both patches and the 19 blobs at the head as `1.txt` to `23.txt`: rc 0, `no leaks
  found`; `gitleaks git` over `d804de5e..81ae47ed`: 1 commit, rc 0, `no leaks found`.
- `words.py --control` `CONTROL FIRED: 13 of 13`; over `added.txt` (267 lines, 13325 bytes) and the head's message:
  `WORDS: clean (2 files)`. My landing texts `squash-subject.txt` (with #38), `squash-body.txt`, `pr-title.txt`:
  `WORDS: clean (3 files)`. `build/squash_scan.py` from main d804de5e's build/ (TMPDIR in my scratch), subject with
  #38: control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`. `pr-body.md` names the coordinator and the
  product owner on purpose (who decides) and is not a repository text.

## FRAME QUESTION (stamp item 11): for each every/never/all sentence the lane adds, three shapes NOT the tested one
| Sentence | Shape 1 | Shape 2 | Shape 3 |
|---|---|---|---|
| summary: an HttpRequestException from the send and an IOException while a success body is read "pass out of a method as they are" (every method) | the 185 methods that are not the first JSON method of their client: the same `SendForJsonAsync` (201 of 201 calls, MEASURED count; no cell) | a real socket's early end: P01, P02 `HttpIOException` MEASURED (H4) | a third type: P04 `InvalidDataException`, P05 `TaskCanceledException` MEASURED (FOUND 1b, 1c); cancellation H7 (N14 helper) |
| summary: "The client never reads the body of a non-success answer" | 404 / 500 / 302: cell; a 1xx or other 3xx: one branch `:55` (H9, DERIVED); with the platform's default redirect handling a 302 is followed before the client sees it (DERIVED, the caller's handler) | a 2xx with a failing body: read by design (H10); a 2xx with a declared length above the limit: not opened, TooLarge (N14 cell) | the platform drains it on dispose: P03 MEASURED, 2 requests on 1 connection (FOUND 1e) |
| K8 comment: "Every optional root property of every client model refuses a null" | every one of 2117 in 716: the loop; counts equal an independent count (INFO 3) | an optional property below the root: named limit H12 (`mNullAfterFirst` changes nested objects too and is caught at the root only, DERIVED) | the target models: K4 reads a null as absent by design (H13); a model with no optional root property: counted out (1131 - 716 = 415, MEASURED) |
| cell summary: "Covered: the first JSON-answer method of each of the 16 clients" | the other methods: same runtime call (above) | `SendRawAsync`: 0 callers (H5 has no member) | a client with no JSON method: none (16 of 16 have one; the cells assert 16) |
| kit: "no code line of the adapter changes" | C6 32 of 32 `///` | my own `diff -U0` count over `src/`: 32, 0 not `///` | compare file list 19 = the owned paths; `Oxpd2RuntimeText.cs`, `Oxpd2ClientCore.cs`, `Oxpd2Json.cs` unchanged (C2) |
| kit: the regeneration "writes exactly the committed files" | `regen-head` then `diff --quiet` rc 0, 19 staged-only rows | file times new (18:25:35), so the files were written, not skipped | byte count 3780946 (head generator) vs 3777458 at BASE (the patched generator compiled) |

## NOT RUN
CodeQL (read on the pull request: landing.txt step 3); any printer, device or host but 127.0.0.1 and the origin; the
probe on Linux or Windows; the build and test of the merge with L4 (`9611a597`, landing.txt MAIN MOVES (B)); the merge
with any main after d804de5e; `repo_rules.py --source-documents`; the H19 mutant (the kit's equivalent row);
the seat's `run_step.py` neutral scan (the hosted secret-scan job's lines read instead).

## WHO DECIDED
Every choice of this lane and of the landing order is the coordinator's (Tuesday's), as coordinator; none is the
product owner's. FOUND 1 is for the coordinator to order into round 2 of this lane or the adapter README pass; it does
not block this landing.
