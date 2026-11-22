GATE B1941: GO WITH FINDINGS @ 75fb5fd on main 39f57d6

Gate G1 (security surface: the card-to-user mapping), round 1 of 2 of lane A2, the lane's one reader. OXPd 2, kit
B1934 (seat X36; Q1 to Q14 the defaults, Q4 and Q8 in words, each the coordinator's stamp S4, not the product
owner's): WP1.4 in part, C7 first slice, the card store. Head `75fb5fdf0791ad30ed9b55282a403f5b134355fa` on
`b1934/wp14-identity-card-store`, ONE commit over `c480a0c8`. Read and measured 2026-11-23 01:27 to 01:45 AEDT on Opus
5.5 in my own scratch under `fleet/state/s312/g1941/`: `clone` (by the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity; detached at the head) and worktree `red` (main `39f57d6a`, then `place.py --write`,
`1-red.diff`, the restore, then `2-fix.diff`). Every dotnet job through the kit's `heavy.py` and the wave lock, one at
a time (lock waits 0 to 1, load1 2.2 to 6.1). Origin by `gh api -X GET` under the project GH_CONFIG_DIR at 01:36 to
01:40: main = `39f57d6a` (pull request 26, lane F2); branch = `75fb5fdf`; open pull requests 0 (newest 26, closed);
`compare main...75fb5fdf` diverged, ahead 1, behind 1, merge base `c480a0c8`, 22 files. No write to the project,
GitHub or Jira; no push, no pull request; no `cd`; nothing deleted (my probe file and the scanner control moved to
`g1941/_quarantine/`).

**BLUF.** The lane does what its kit says and the property of THE CONTRACT holds in every shape I could hand it: no
path maps a card to a user who does not hold the whole blob for that user's own mail on a single-page answer, and the
one write keeps every held entry in order, adds one blob, and only under both limits (each probed on both sides). The
head is the two frozen patches plus `place.py` plus the restore, byte for byte. Red first at main `39f57d6a`: 1752 /
87 failed, all Identity, all `NotImplementedException`, L02 green by design; the head 1750 / 0; 39 of 39 mutants MATCH
and undone, rebuilt after the last undo, green again; the merge with main is conflict-free and reads 1752 / 0 and
RULES 551; the head's hosted run PASS; scans clean. **Two Minor findings, neither a path to a wrong user or a wrong
write:** a blob maker that throws a cancellation of its own leaves the store untyped (FOUND 1); a name twice outside
the set is read last-wins while the README says answers are read strictly (FOUND 2). Nothing blocks the landing. They
can go to the records pass (FOR-RECORDS items 1 and 2, with fix sketches) or back as a small fix round (+6 cases);
that choice is the coordinator's. **Q4's two departures: safe, both fail closed and change nothing stored (INFO 1);
they are deviation-register rows for OQ-6, which this gate does not decide.**

## FOUND

1. **Minor (contract, no security effect): a cancellation thrown BY the blob maker leaves the store untyped.**
   `CsaStore.cs:282` and `:299`: `catch (Exception failure) when (failure is not OperationCanceledException)` around
   `_codec.SearchPrefix` and `_codec.Blob`. The maker is not handed the caller's token, so any
   `OperationCanceledException` it throws is its own, yet it passes through. MEASURED (probe P07, scratch, macOS arm64,
   on the head): prefix maker throws `OperationCanceledException`, caller's token not cancelled: `find OTHER
   OperationCanceledException, requests 0`; blob maker throws `TaskCanceledException` inside an enrolment: `OTHER
   TaskCanceledException, patches 0`. Nothing is requested, chosen or written, but the call ends in neither a typed
   result nor the caller's cancellation, against kit D10, THE REQUIRED SECTION's property ("never another exception")
   and the README's "Every call returns its typed result, or throws ... or the caller's cancellation". A caller that
   reads any cancellation as "my user walked away" would mishandle it. Not killed by any cell (F08 throws
   `InvalidOperationException` only). Fix sketch: pass the call's token into `PrefixOf`/`BlobOf`, filter `when
   (failure is not OperationCanceledException || !cancellationToken.IsCancellationRequested)`, two F08 rows.
2. **Minor (README accuracy / strictness): a name twice OUTSIDE the set is read last-wins, not refused.** The strict
   reader refuses a duplicate name inside the set (`CsaReading.cs:67-73`; F07 "a name twice"), but every other read
   goes through `JsonElement.TryGetProperty` (`CsaReading.cs:47`, `:57`, `:132-145`; `CsaStore.cs:196`, `:207`), which
   matches the LAST of duplicate names. MEASURED (P05): `mail` twice with the holder's mail last: `Found user A`; with
   it first: `AssociationInvalid`; `id` twice (B then A): `Found user A`; the set twice and the page's `value` twice:
   the last one read. The README says "Answers are read strictly: a shape the store does not name is
   `MalformedAnswer`". Reaching it needs Graph's own answer to repeat a name (UNMEASURED whether it ever does; the
   answer arrives over the Graph layer's TLS from the tenant), so no caller-controlled path chooses a user this way;
   it is a gap between the README and the code on a security surface. Fix sketch: one duplicate-name check for the
   user object, `customSecurityAttributes` and the page, four F07/R03 rows; or a Limits line naming last-wins.

## INFO

1. **Q4's two departures (DEVIATION-REGISTER items for the product owner's OQ-6 approval, `03:108`, `03:378`): safe.**
   Both fail closed and both are search-side only: neither changes what is stored, so a card enrolled by either app
   still works on both (`02:16` holds). (a) A failed search typed `GraphFailed` (`CsaStore.cs:228-237`, F06): it
   removes the Workpath path where an existing user is sent to enrolment (`A1:208`); it is the target of weakness
   **W10** (`02:691`, "Lookup failure is an error state, never "unknown card""), so by `03:108` it reads as class (3).
   (b) A next page `Ambiguous` / `HeldByAnotherUser` (`:66-69`, `:113`, `:207`; F04, E06; P04a and P05 "nextLink not a
   text": also with an empty first page, or a null link, nobody is chosen): it can cost a sign-in only when Graph pages
   a prefix search (how many holders that needs is UNMEASURED; one card's prefix is held by one user in a sound
   tenant), and then nobody is chosen where Workpath would choose from page one. No W row covers it: a design choice
   neither ruled nor forced, also OQ-6. Not decided here.
2. **D6, a malformed user fails the whole search: right.** MEASURED (P05): a true holder beside a user whose id is not
   an identifier, or whose set holds a `null` value: `MalformedAnswer`. Choosing the readable holder would be wrong
   whenever the unreadable user is a second holder (the answer is then `Ambiguous`), so failing the call is the only
   choice that never picks a user the store could not see whole. The cost is bounded: the answer holds only users
   holding that card's prefix. One shape to measure at the integration run: a `null` attribute inside a set fails the
   user's read and every search that answers that user (P05; null set and null attributes read empty, R02); whether
   Graph sends one is UNMEASURED (FOR-RECORDS item 3).
3. **E06's second row (another user holds the prefix for a DIFFERENT mail refuses the enrolment): right for a mixed
   fleet.** The prefix depends on the card only (`A1:189`, "the same card always gives the same first 62 characters"),
   so any holder of it holds that physical card under some mail. Allowing the enrolment would put one card in two
   users' collections, a state the Find rule turns into `Ambiguous` the moment both tags match and whose handling by
   the Workpath app is UNMEASURED (kit Q5). MEASURED (P02a): A holds the blob made for B's mail: Find
   `AssociationInvalid`, B's enrolment `HeldByAnotherUser`, patches 0; A's own enrolment `Enrolled` (A holds the prefix
   itself: the mail-change rule, E07). Cost: a card reissued from a user with a stale entry needs that entry removed
   first, and removal is not in this slice (owed item 2). Related, P02c: A holds the whole blob and B only the prefix:
   Find `Found user A`, while A's enrolment of the same card reads `HeldByAnotherUser` before `AlreadyEnrolled` (check
   order; nothing written).
4. **The mapping, probed (P01 to P04).** Case of the mail (blob made for the upper-cased mail), `==` padding, a trailing
   space, the bare 62-character prefix: `AssociationInvalid` each; the whole blob upper-cased: `NotFound` in the fake
   (Graph's `startswith` case rule UNMEASURED). A blob held under another user's mail: that user is not chosen; both
   holding the blob made for B's mail: `Found user B` only (P02b). No mail, blob for a mail: `AssociationInvalid`; a
   mail, blob for no mail: `AssociationInvalid`; an empty mail is handed to the maker as an empty text, not null
   (P03c). Two holders, a next page (F04, P04a), an answered user who does not hold the prefix (P04b:
   `AssociationInvalid`, enrolment `HeldByAnotherUser`). The user's own id in braces and upper case in the search
   answer enrols (P04c: normalised by `Guid`). The binding is the two-character mail tag of the Workpath format (12
   bits, `A1:189`); the store never accepts less than the whole 64.
5. **The write, probed (P06).** Held `[x, y, x, old-mail entry, junk]` plus `UPAR` and a number: one PATCH of exactly
   the five held entries in order plus the new blob, names `@odata.type,cardId@odata.type,cardId` only; the other
   values untouched in the tenant. Limits both sides, measured: cards 14 / 15 / 16 (values = cards) `Enrolled` /
   `CardLimitReached` / `CardLimitReached`; values 49 / 50 / 51 with 0 cards `Enrolled` / `ValueLimitReached` x2; 14
   cards + 35 others (49) `Enrolled`, + 36 (50) `ValueLimitReached`; 13 + 36 `Enrolled`, 13 + 37 `ValueLimitReached`;
   15 cards + 35 others (50) `CardLimitReached` (card limit read first). Never more than 15 entries or 50 values after
   a write.
6. **Out-of-form maker answers never reach a request** (F08, 9 rows, and the `IsBase64Url` gate before the filter at
   `CsaStore.cs:287`; the filter is concatenated only from a checked prefix, `:193`). FOUND 1 is the one maker
   behaviour that escapes the typed path, and it too makes no request.
7. **Texts (P10).** Eleven texts over every outcome and failure kind (result, user, attributes, card rule, object id, a
   maker that throws with the card and mail in ITS message, malformed, write refused, search refused, schema missing,
   schema mismatch), each `ToString()` + `Message` + inner: 0 hits for the card, the bad card, the blob, the prefix, the
   id, the sign-in name, the mail, the names, the token, `/v1.0/` and `$filter`; control 2 hits on a planted text. The
   maker's own message never reaches a text (no inner exception attached).
8. **Cancellation and half-written state (P08, P09).** Cancelled while the enrolment's search is in flight:
   `TaskCanceledException`, patches 0. Cancelled after the tenant applied the PATCH: `TaskCanceledException` with the card
   held; enrolling again `AlreadyEnrolled`. Applied then answered 500: `GraphFailed` with the card held; answered 503
   then retried by the Graph layer: `Enrolled`, two PATCHes, no duplicate entry. One PATCH of the whole collection is
   idempotent, so no half-written collection exists; the README's "after which nothing of that call is used or
   written" can be read as "not written" (FOR-RECORDS item 4). Two enrolments at once for one user: both `Enrolled`,
   one card left (the named limit, silent to both callers).
9. **Schema check (P11):** a definition with `status` `Deprecated`, `usePreDefinedValuesOnly` true, or naming another
   set and attribute passes; for owed item 1.
10. **`$select`:** D4's adds `givenName` and `surname` to the Workpath app's (`A1:200`); the README calls it "the
    Workpath app's search, report A1 line 200". Harmless in the fake, UNMEASURED against Graph (the seat's observation,
    confirmed).

## WHAT I MEASURED

- **THE TOOLS:** `cp -Rc` of `fleet/state/s312/d1934/gate/` to `g1941/gate/`; 13 of 13 sha256 equal to kit B1934's
  table (printed in one `shasum` call). `words.py --control` `CONTROL FIRED: 13 of 13`.
- **THE COMMIT against its kit** (read whole: the 9 product files, the README, the 8 test files and both csproj):
  parent `c480a0c8`, `rev-list --count` 1; the stored message byte-equal to `commit-message.txt` (277 bytes); numstat 22
  rows, 1 `M` (`Datasec.Suite.slnx` 2/0), 21 `A`, no D/R. THE CUT: nothing OUT is in (no SignIn/Sessions/Cards/Secrets
  reference, no schema creation, no write of another value, no key, no sign-in or gateway code). D1 to D14 each as
  built (lines cited above and in the seat's FOR TUESDAY, re-read). THE CONTRACT's property: held (INFO 3 to 8).
  README Limits: true as worded, with the reading of INFO 8.
- **THE PATCHES = THE HEAD:** in worktree `red` (main `39f57d6a` + `place.py --write` `PLACED: 2 lines (src at 9, tests
  at 26)` + `1-red.diff` + restore + `2-fix.diff`): `git diff --cached --quiet 75fb5fdf -- Datasec.Suite.slnx
  src/Datasec.Suite.Identity tests/Datasec.Suite.Identity.Tests` rc 0; control over `src/Datasec.Suite.Secrets` rc 1.
- **RED FIRST at main `39f57d6a` (tests and stubs):** restore rc 0; `lockrule.py` `LOCK-RULE: PASS`, `--control`
  `CONTROL FIRED: 2 of 2`; build 0/0; whole solution `total: 1752`, `failed: 87`, `succeeded: 1661`, `skipped: 4`; 87
  failed lines, 87 naming `Datasec.Suite.Identity.Tests.`, 87 naming `NotImplementedException`; per cell exactly the
  seat's (E01:1 ... R06:1); L02 not among them.
- **GREEN, the head (clone):** `CI=true` locked restore `--force` rc 0, status clean after; build `0 Warning(s)` `0
  Error(s)`; whole solution `total: 1750`, `failed: 0`, `succeeded: 1746`, `skipped: 4`. `lockrule.py` PASS on the head.
- **THE MUTANTS:** `mutants_a2.py <clone> <keep> run g1941 'B1941 gate'` as ONE call: 39 rows, every row `Total 88`,
  `MATCH`, `undone equal True`; last line `MUTANTS: 39 of 39 MATCH, 39 of 39 undone equal`. After it: status clean;
  build 0/0 with the library's dll at 01:39:01 after the last restored source at 01:37:41 (a build after every undo
  before the green run); whole solution again 1750 / 0 / 1746 / 4.
- **CHECKS:** `staged.py <clone> c480a0c8` `STAGED: PASS (22 rows)` (22 rows 1 M 21 A; slnx `2 0`; 19 text files
  printable ASCII with LF), `--control` `CONTROL FIRED: 3 of 3`. `boundary.py` `required: _graph.SendAsync( 2,
  HttpMethod.Patch 1, GetElapsedTime( 1, HttpMethod.Get 1`, `BOUNDARY: clean (9 files)`, `--control` `CONTROL FIRED: 33
  of 33`. `repo_rules.py` (never `--source-documents`): `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder
  here)`, `RULES: clean (551 files)` on the head and on the merged tree.
- **MY PROBES:** `G1941Probes.cs` (11 facts) in the clone's Identity test project, built (0/0) and run whole through the
  lock: `Total: 99, Errors: 0, Failed: 0`; outcomes only, in `g1941/scratch/probe-out.txt` (no value printed); the file
  then moved to `g1941/_quarantine/probes/`, the test project rebuilt (0/0) and run whole `Total: 88, Errors: 0,
  Failed: 0`; status clean.
- **THE MERGE:** `git merge-tree --write-tree --name-only 39f57d6a 75fb5fdf` rc 0, tree `c8e302ac...`, no conflict;
  the other side's 7 paths (Secrets, Data, Adapters README, two test files) disjoint from this lane's 22. Worktree `red`
  after both patches: `git write-tree` = `c8e302ac...` (the merge tree); locked restore rc 0; build 0/0; whole
  solution `total: 1752`, `failed: 0`, `succeeded: 1748`, `skipped: 4` (= 1664 + 88); RULES 551 (= 530 + 21). Lane F1's
  round-1 head `c15e13f5`: merge-tree with this head rc 0 (its 7 paths SignIn and UniversalPrint/Registration only).
- **HOSTED:** `hosted2.py 75fb5fdf... --total 1750 --rules 551 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor
  111 --hardened-scan` rc 0: run 45032204534, attempt 1, four jobs success; linux 1750 twice, succeeded 1746, skipped 4,
  GUARD 10 files; windows 1750 twice, succeeded 1729, skipped 21, GUARD 11 files; RULES 551, floor 111; every hardened
  secret-scan row OK; `HOSTED 75fb5fdf0791ad30ed9b55282a403f5b134355fa: PASS`. Main `39f57d6a` with `--total 1664
  --rules 530`: run 45032456562, four jobs and three Analyze rows success, `HOSTED 39f57d6a...: PASS`.

## SCANS

- `words.py` over the 1890 added lines of `c480a0c8..75fb5fdf` (lock files excepted) and the head's message
  (`scratch/words/1.txt`, `2.txt`): every count 0, `WORDS: clean (2 files)`. Over `squash-subject.txt`,
  `squash-body.txt`, `pr-title.txt`: `WORDS: clean (3 files)`.
- gitleaks 8.30.1 `dir --no-banner --redact --ignore-gitleaks-allow --exit-code 1`: control FIRST (a token-shaped value
  built by program from two halves and 36 random characters in a new scratch folder, never printed): rc 1, `leaks
  found: 1`, folder moved to `g1941/_quarantine/gl-control`; the 22 head blobs and the message as `1.txt` to `23.txt`
  in a new folder: rc 0, `no leaks found`; the added lines and message: rc 0, `no leaks found`.
- `build/squash_scan.py squash-subject.txt squash-body.txt --scanner /opt/homebrew/bin/gitleaks` (from main `39f57d6a`'s
  build/): control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.
- gitleaks over this verdict folder (seven files, at 01:45, before this line was written): rc 0, `no leaks found`.

## CODEQL

Not run locally (the gate has no CodeQL step). Read on the pull request (`landing.txt` step 3): two broad catches with a
`when` filter around the handed-in maker (`CsaStore.cs:282`, `:299`), a search filter concatenated from a checked prefix
(`:193`), object ids put into addresses after `Guid.TryParse` (`:136`, `:212`, `:325`); in the tests, SHA-256 of
synthetic cards, an `HttpClient` over an in-memory handler, `WaitAsync` bounds.

## NOT RUN

Any run on Linux or Windows locally (the hosted legs of the head only; the merge with main on the hosted legs is not
measured, windows succeeded 1731 PREDICTED); the 50-run loop (the seat's, 50 of 50, RELAYED; my runs: whole solution 4
times, the Identity executable twice); `run_step.py`'s neutral scan (the hosted secret-scan job ran it on the head:
PASS); `repo_rules.py --source-documents` (never); lane F1's round 2 (not pushed at my read); anything against a tenant;
CodeQL.

## DEVIATIONS

None from the commission. Two notes: the tool display showed no exit code for a silent `git diff --quiet` that returned
1 (my control), so I re-ran both through a small `rc.py` that prints the rc (rc 0 and rc 1); my RED FIRST ran at main
`39f57d6a` (the commission's "at main"), not at `c480a0c8` where the seat ran it (1750 / 87 there, RELAYED).

## TREES LEFT

`g1941/clone` detached at `75fb5fdf`, status clean (mutants undone, probe file quarantined, rebuilt); worktree `g1941/red`
at `39f57d6a` with the lane's 22 paths staged (uncommitted; tree `c8e302ac`); `g1941/logs/**`, `g1941/scratch/**`
(`probe-out.txt`, `words/`, `gl-blobs/`, `mutants/`, helper scripts), `g1941/_quarantine/{locks,gl-control,probes}`. No
process left running; the wave lock not held by this reader.
