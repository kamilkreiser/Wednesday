GATE B2064: GO WITH FINDINGS @ 51e91c2 on main 84f088a

Gate G1, ROUND 2 OF 2 of lane L3 (a NO GO here would go to the product owner on a card, never a round 3), one Opus
reader (claude-opus-5-5), in-session, read-only. OXPd 2, lane L3, kit B2062 (seat X69; stamp S4: Q1 "a"
`SYNTHETIC0002!12345`, Q2 "a" a README Limits line, no binding, Q3 "a" compare and send without the fragment, cell O12,
each in words; Q4 to Q10 the defaults; every one the coordinator's, none the product owner's). Head
`51e91c26e838982e272730f0e610ba668ce8b6e6` on `b2056/l3-onedrive-browse` = HEAD1 `4b9814f1` + ONE commit (one parent
HEAD1; HEAD1's one parent BASE `89a10a1b`; no rebase). Main `84f088a224ad62789d026b328e291ad5fde0b527` (PR 49, one parent
f5882ed7, tree 1b633300). compare main...51e91c26: diverged, ahead 2, behind 2, merge base 89a10a1b; open pull requests
0; branch and main re-read unchanged at 22:21 and 22:34 AEDT. Read and measured 2026-11-24 22:21 to 22:40 AEDT in my
scratch `fleet/state/s324/g2064/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity), worktrees `w` (the
head; the mutants ran here and were undone: porcelain 0 rows after), `red` (HEAD1 + `1-red-r2.diff`), `p` (the head + one
probe file, now `_quarantine/G2064Probe.cs.moved`; `p` porcelain 0 rows again), `s` (HEAD1 with the head's three paths
staged, for the kit's check programs) and `m` (main 84f088a2 with the squash tree `0f34cebf` read into index and files).
Every dotnet job and test executable through the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock, one at a time
(49 released lock folders, all mine, in `g2064/_quarantine/locks/`; lock waits 0 on every job; the lock absent at 22:35).
Origin by `gh api -X GET` under the project GH_CONFIG_DIR. Two public pages by plain unauthenticated HTTPS GET of raw
files (named under THE HEAD). No write to the project, GitHub or Jira; no push, no pull request, no re-run; no tenant,
token, Microsoft API, Azure, printer or device; nothing deleted (moved to `_quarantine`).

**BLUF.** Round 2 closes round 1's three findings and breaks nothing I could measure. **FOUND 1 of B2061 (the blocker) is
closed:** O02's row is `SYNTHETIC0002!12345`; the census of every literal of the lane's twelve files at the head finds no
16-hex run, no consumer-shaped id, no GUID, no host outside `example.test`, and the only `!` tokens are the id rule's
class, the new row and `b!synthetic-drive_0001`; **the squash tree `0f34cebf` holds the round-1 literal in no file**
(`git grep -i -F` of its hex part rc 1 there, at the head and at main; control rc 0 at 4b9814f1) and no consumer-shaped id
in any of its 671 files. **FOUND 3 is closed in code:** O12 is red first on HEAD1 exactly as the kit says (`Total: 50,
Errors: 0, Failed: 1`, `Expected: Tuple (PagingLoop, 1)` / `Actual: Tuple (TooManyPages, 100)`) and green at the head;
B2061's probe P2 now ends `PagingLoop` at page 1 with ONE request (round 1: 100); twelve more fragment, host-case,
scheme-case, port and dot-segment repeat variants each end `PagingLoop` with nothing sent again; no request of any probe
carries a fragment. **FOUND 2 is closed as a stated limit**, every README sentence holds against the code. **The G1
property holds:** B2061's 43 next-link shapes, re-run unchanged against the head, give exactly round 1's outcomes (30
refused with nothing sent, 13 sent as G3 children calls on the base host), 0 requests outside G1, G2, G3. Tree = HEAD1 +
both frozen patches byte for byte; 16 of 16 mutants MATCH, 16 undone; 2203 / 0 / 2199 / 4 before and after the mutants;
the squash with main 84f088a2 measured at **2221 / 0 / 2217 / 4, `Ran 117 tests` OK, `RULES: clean (671 files)`, GUARD
14 and 15** (the commission's PREDICTED numbers, now MEASURED); hosted `HOSTED 51e91c26...: PASS` on both legs.
One Minor finding (the round-1 commit stays reachable from the branch and from the pull request's ref) and Info only;
**none blocks landing.**

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (the round-1 commit stays reachable outside main).** The squash lands the final tree only, so
   main and its history never hold the round-1 literal (MEASURED above). But `4b9814f1`, which holds it, stays on the
   origin as the parent of the head on `refs/heads/b2056/l3-onedrive-browse`, and a pull request from this branch makes
   `refs/pull/<N>/head` = `51e91c26`, reaching it too. Pull refs outlive their merge on this repository (MEASURED:
   `matching-refs/pull/4` lists `refs/pull/4/head` to `refs/pull/49/head`, 49 at `0ca131eb`, merged 11:13:27Z); whether
   a pull ref can be removed by the owner is UNMEASURED. Gate B2061's blocking ground was main's history; that ground is
   met. Harm if the id were real: an item identifier of a consumer account (not a credential) in a private repository's
   object store, reachable by ref, not on main. Remedy, the coordinator's choice (landing.txt step 0): land as written
   (the commission's form), or open the pull request from a NEW branch holding one commit of tree `03440d1d` on
   `89a10a1b` (a seat's push; a new head that this gate did not read). Either way, deleting the lane branch after the
   landing is worth considering.
2. **Info (repeat variants that are distinct addresses: bounded, as designed).** Probe P6/P7 at the head: a next link
   that differs from a requested address by the case of an item id (`SYNTHETICFOLDER0001` then `syntheticfolder0001`),
   by the case of a query option name (`$SELECT`), by a percent-escaped `,` (`%2C`, `%2c`) or `$` (`%24select`), by an
   empty `?` or by the query removed is requested ONCE more, and its exact repeat then ends `PagingLoop` (2 requests);
   a server that appends `&` on every page gets 100 distinct requests and `TooManyPages` at page 101 (R14), the shape of
   B2061's P2b (query `x=0`/`x=1`: `PagingLoop` at page 3, unchanged). Under RFC 3986 these are different addresses (the
   query and path are case-sensitive; only unreserved characters' escapes are equivalent, and `%41BC` = `ABC` IS caught:
   P7, 1 request), so no sentence of the change over-claims; whether Graph treats them as one address is UNMEASURED.
   Upper-case host or scheme, `:443`, a dot segment and an upper-case `ME` path are normalised or refused by `Uri` and
   the path rule before the compare (MEASURED: `PagingLoop` or `NextLinkElsewhere` at page 1).
3. **Info (two round-1 doc sentences narrower than the code).** README `:3`-`:4` "the children of the root ... or of one
   folder by its item id, and nothing else" and the class summary `MyDriveBrowser.cs:12` "each next page only when its
   link names a children call of the same forms" read narrower than the four forms the code follows (`drives/{id}`
   included). Round-1 text, untouched by this round; the README's `:19`-`:20` and the new Limits `:41`-`:44` state the
   behaviour exactly. For whoever next touches the module.
4. **Info (the layer's own walk).** `GraphClient.FollowableLink` at the head still reads `requested.Contains(next.AbsoluteUri)`
   (read by `git show`): the same fragment compare round 2 removed from the module. Not this lane's (the kit's H8; FOR
   RECORDS).
5. **Info (the seat's record).** STATUS DEVIATIONS 2 (a stray `cd /` in one read-only command) and 4 (a `dotnet
   --version` outside the runner) are shell-form slips that wrote nothing; check 8's print label `cells 12 (O01..O11)` is
   file order, its rule passed (I re-ran it: PASS). Nothing in the commit or the branch depends on them.
6. **Info (the hosted figures for the landing).** The pull request's merge ref is built on main, so its `rules` job reads
   `Ran 117`, floor 117 and its legs 2221 (linux succeeded 2217 MEASURED locally; windows 2200 DERIVED: 2150 + 50), not
   the push run's 111 / 2203 (Q5 as stamped holds).

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE", and the commission's WHAT TO DO 1), item by item
- **`HEAD1..head` read whole** (3 files; the diff printed whole, 22 added, 4 removed: numstat 5/2, 6/1, 11/1, equal to THE
  CODE) **and `--name-status` against BASE:** 13 rows, 1 M (`Datasec.Suite.slnx`), 12 A under the two OneDrive folders,
  no other row (round 1's thirteen). `MyDriveBrowser.cs` read whole at the head (277 lines); `BrowseTests.cs` whole (213);
  `Fake.cs`, `OneDriveBrowseException.cs`, README whole; `GraphClient.cs` `SendAsync`, `FollowableLink`, `OnBaseOrigin`,
  `ResolveAddress` re-read (the sent address is the returned string re-parsed by `ResolveAddress`; it carries no `#`).
- **The two patches against THE TOOLS:** my copy of the eleven tools 11 of 11 equal by sha256 to the kit's list and to the
  seat's `.tools/b2062/gate` copy; the head tree `03440d1d` = HEAD1 + `1-red-r2.diff` + `2-fix-r2.diff` (temporary index,
  red tree `b7926fe5`); the three files' sha256 equal THE CODE's "After both" column (277, 47, 213 lines); the commit
  message equals `commit-message-r2.txt` (329 bytes, subject 271 characters); author equals committer, `@datasec.com.au`.
- **Red first:** HEAD1 + `1-red-r2.diff` (the three files at THE CODE's "After 1-red-r2.diff" column, porcelain exactly
  ` M ...BrowseTests.cs`): locked restore (`CI=true`) rc 0, build `0 Warning(s)`, `0 Error(s)`, the OneDrive executable
  `Total: 50, Errors: 0, Failed: 1`, the one `[FAIL]` O12, next line `Assert.Equal() Failure: Values differ`, then
  `Expected: Tuple (PagingLoop, 1)` / `Actual:   Tuple (TooManyPages, 100)` (`logs/r-exe.log`; runner `xUnit.net v3
  In-Process Runner v4.0.3 (64-bit .NET 10.0.15)`).
- **16 mutants, each red on exactly its cells** (`logs/mutants-run.out`, my run of the frozen tool in `w`): every row
  identical to the kit's and the seat's: mSelectDropped O01 O04 O09 (3) | mFolderSelectDropped O02 (3) | mIdDotsTaken O03
  (2) | mIdCharsOpen O03 O05 O08 (8) | mIdLengthOpen O03 (1) | mDuplicateTaken O05 O07 (2) | mBothFacetsTaken O05 (1) |
  mSizeSignTaken O05 (1) | mRemoteShapeTaken O05 (1) | mRemoteIgnored O01 (1) | mPathUnchecked O08 (6) | mPortUnchecked
  O08 (1) | mLoopUnchecked O09 O12 (2) | mFragmentKept O12 (1) | mPageBoundOffByOne O10 (3) | mNameInText O07 (1);
  `MUTANTS: 16 of 16 MATCH, 16 of 16 undone equal`. After it: porcelain 0; rebuild `0 Warning(s)`, the OneDrive dll
  22:26:47 later than `MyDriveBrowser.cs` 22:26:32 and `DriveEntry.cs` 22:26:34; whole solution 2203 / 0 / 2199 / 4.
- **The literal census of the whole lane at the head** (`scratch/census.py`, `logs/census.out`): 12 files; hex16 0,
  consumer shape 0, GUID 0, 12+ hex run 0, 9+ digit run 0, JWT-like 0; addresses 6, every host `graph.example.test` or
  `other.example.test` (with `:444`, `user@`, `/beta/`, `http:`); `!` tokens in literals: `A-Za-z0-9!._-`,
  `SYNTHETIC0002!12345`, `b!synthetic-drive_0001` (the rest are C# `!` operators); 141 distinct quoted literals in the
  `.cs` files, every id `SYNTHETIC...`, `REMOTESYNTHETIC0001`, `synthetic-access-0001`, `namesynthetic0001`, names
  `folder-a`, `file-b.pdf`, `shortcut-c`, `a.b_c-d`, one date `2026-01-02T03:04:05Z`, the rest JSON property names, code
  names and fixed texts; the 19 base64 runs are the lock files' package content hashes (public NuGet values). Control:
  the same patterns over HEAD1's `BrowseTests.cs` count hex16 1, consumer 1. **Verdict per class: all synthetic or
  reserved-domain; the old id absent from the head and the squash tree.** The kit's `checks_l3r2.py` check 4 agrees
  (`hits none`).
- **B2061's 43 next-link shapes and P2, P2b against the head** (THE PROBE below): no request other than G1, G2, G3; no
  repeat of a requested address that differs only by its fragment or an empty fragment; case: host and scheme case
  caught, path `ME` refused, an item id's or a query name's case is a new address (Info 2).
- **Every README sentence against the code:** `:3`-`:4` (Info 3); the calls table `:10`-`:11` holds (`:60`, `:77`);
  `:13`-`:15` holds (`:106`; the token source passed through only); `:17`-`:21` holds (43 shapes); `:25`-`:33` hold (O01,
  O05, O07, O10, R14: `TooManyPages` at page 101 after 100 requests); `:37`-`:39` holds; `:40` holds (O01: listed,
  `PointsToOtherDrive` true, not followed); **`:41`-`:44` holds** (F4, F5 sent for unrelated drive ids; a drive id outside
  the id rule refused, F8; the listing's Select holds no `parentReference`, so no drive id is known; only `Followable`
  can produce a `drives/` address: `ListRootAsync` and `ListFolderAsync` build `me/drive/` only); **`:45` holds** (P2,
  R01 to R05, R09, R18, R19; no sent address with a fragment). **The removed over-claim is gone:** "never opens another
  user's drive" 0 lines at the head (check 10; 1 at HEAD1).
- **The hosted run on both legs:** my `hosted3.py` read of push run 45382346368 (22:30): linux `total: 2203` twice,
  `succeeded: 2199`, `skipped: 4`, `GUARD: clean (14 files)`; windows `total: 2203` twice, `succeeded: 2182`, `skipped:
  21`, `GUARD: clean (15 files)`; rules `Ran 111 tests in`, `UNIT-TEST FLOOR: ran 111, floor 111`, `RULES: clean (671
  files)`; secret-scan every proof line, `objects of this commit not among them 0`; check runs beside the four 0; last line
  `HOSTED 51e91c26e838982e272730f0e610ba668ce8b6e6: PASS`. `failed Datasec.` lines 0 and 0, `[FAIL]` 0 and 0 (colour
  codes stripped); control: 5 lines naming `Datasec.Suite.OneDrive.Tests` per leg.

## FRAME (stamp checklist item 11: each every/never/only sentence the change adds, three shapes outside the tested one)
- "a fragment is never sent" (`MyDriveBrowser.cs:244`, README `:45`): tested shape `#synthetic<n>` (O12). Outside it: an
  empty `#` (R01), `#?` with query-like text (R02), `#%00` (R03), `#%23x` (R04), `##` (R05), a tab (R18), 2000 characters
  (R19), with an upper-case host and `:443` (R09), and B2061's Q3 `#/../../recent` (sent as the bare children path).
  Covered: no sent `RequestUri` has a fragment or a `#` in its original string (73 class reads, OTHER 0; R14's class list
  printed for its first 14 of 100 requests, its outcome and distinct count read whole).
- "a link that differs from an address already requested only by its fragment is a loop too" (`:244`-`:245`): R01 to
  R05, R09, R18, R19, each `PagingLoop` at page 1, 1 request, both moving (the address just requested) and constant (the
  first address). Covered.
- "a link that names an address already requested is PagingLoop. Neither is ever requested" (`:243`, restated) and
  `OneDriveBrowseException.cs:17` (unchanged, Q10): the exact address (O09), an upper-case host or scheme, `:443`, a dot
  segment (R06 to R08, R10: caught), `%41BC` for `ABC` (P7: caught), an item id's or query name's case, `%2C`, `%24`, an
  empty `?` (sent once more: different addresses, Info 2). Covered or stated.
- "followed whatever drive id it names, when the id passes the id rule" (README `:41`-`:42`): F4 (`drives/{id}/root`),
  F5 (`drives/{b!...}/items/{id}`), P7 (`drives/SYNTHETICDRIVE0001/items/ABC` after `me/drive/items/ABC`: sent, then its
  repeat `PagingLoop`), F8 (a 257-character id: refused). Covered.
- "Only a server's own next link can name such a call" (`:43`): code read (the two public methods build `me/drive/` only;
  O11: four requests, all `me/drive/`), F4 and F5 (via a next link). Covered.

## THE PROBE (scratch only, never committed: `_quarantine/G2064Probe.cs.moved`; output `scratch/probe-report.txt`)
One test file added to the OneDrive tests in `p` (its own `FakeGraph` per row, the landed `GraphClient`, base
`https://files.kilo.example.test/v1.0/`, synthetic ids and token); B2061's 43 `P1` rows, `P2`/`P2b` and `P3` copied
unchanged in their links, plus `P6` (20 repeat variants, each moving and constant) and `P7` (5 item-id variants); every
request classified G1 / G2 / G3 / OTHER by origin, path pattern and fragment. Build `0 Warning(s)`, `0 Error(s)`; the
test executable run whole: `Total: 116, Errors: 0, Failed: 0` (50 + 66 probe cases).

| Rows | Outcome (requests) at 51e91c26 | Round 1 (B2061) |
|---|---|---|
| H3 Kelvin-sign host, H4 upper-case host, H7 `:443`, H9 `HTTPS:` | sent to `files.kilo.example.test`, children path (2) | same |
| H1, H2, H5, H6, H8 | `NextLinkElsewhere` (1) | same |
| D1 `recent/../root/children` | sent as `/v1.0/me/drive/root/children` (2) | same |
| D2 to D6 | `NextLinkElsewhere` (1) | same |
| D7 `items/.../children`, E1 `%41BC` (sent `ABC`) | sent, children path (2) | same |
| E2 to E15 | `NextLinkElsewhere` (1) | same |
| Q1 to Q4 | sent, children path, query unchanged; Q3 sent WITHOUT its fragment (2) | same |
| F1, F2, F3, F6, F7, F8 | `NextLinkElsewhere` (1) | same |
| F4, F5 `drives/{id}` forms | sent (2) (README Limits `:41`-`:44`) | same (FOUND 2) |
| P2 the same address + `#f<n>` | **`PagingLoop` page 1 (1)** | 100 requests, `TooManyPages` page 101 |
| P2b query `x=0`/`x=1` | `PagingLoop` page 3 (3) | same |
| P3 base `/v1.0/sub/` | under it: sent; `/v1.0/...` and `../`: refused | same |
| P6 R01 to R10, R18, R19 (fragments; host, scheme, port; dot segment) | `PagingLoop` page 1 (1), moving and constant | (not run) |
| P6 R11 to R13, R15, R16, R20 (query case, escapes, removed, empty `?`) | `PagingLoop` page 2 (2) | (not run) |
| P6 R14 (a `&` appended each page) | `TooManyPages` page 101 (100), constant form `PagingLoop` page 2 | (not run) |
| P6 R17 (`/ME/drive/`) | `NextLinkElsewhere` (1) | (not run) |
| P7 id case; `me` then `drives/` form of one id | sent once more, then `PagingLoop` (2) | (not run) |
| P7 `%41BC`, `%41%42C` after `ABC` | `PagingLoop` page 1 (1) | (not run) |
| P7 `A%23BC` | `NextLinkElsewhere` (1) | (not run) |

## THE HEAD AND THE SQUASH, MEASURED BY THE GATE (logs `g2064/logs/`)
- Head `w`: locked restore (`CI=true`) rc 0; build `0 Warning(s)`, `0 Error(s)`; OneDrive executable `Total: 50, Errors: 0,
  Failed: 0`; `dotnet test -c Release --no-build`: `total: 2203`, `failed: 0`, `succeeded: 2199`, `skipped: 4` (before
  and after the mutants); `repo_rules.py` (plain form, `test ! -e w/1_Project_Definition` True): `RULES-NOTE: R5 hash half
  NOT RUN (no supplied-source folder here)`, `RULES: clean (671 files)`; `unittest discover -s build/tests`: `Ran 111
  tests`, `OK`.
- `checks_l3r2.py s 4b9814f1`: `CHECKS-R2: 10 of 10 PASS` (3 M rows; every other path rc 0; round-1 literal staged rc 1;
  ids hits none; ascii; added 22 removed 4; test file exact; Fact 6 Theory 6 InlineData 44; loop line 1/1/0; README 0/1/1;
  every control fired). `checks_l3.py s 89a10a1b`: `CHECKS: 10 of 10 PASS` (13 rows, 1 M 12 A; slnx 2 added; lock ids 2
  and 19, 0 new; added 833; public 42; no package or own HTTP; recent/sharedwithme/search 0, `"me/drive/` 2; SendAsync 1).
- **The squash** (`git merge-tree --write-tree 84f088a2 51e91c26`: rc 0, tree
  `0f34cebf88d2a520c14b6dad3ee3af660062474b`, 671 files; equal to 84f088a2 outside the lane's 13 paths and to the head
  inside them, `diff --quiet` rc 0 each; `git diff --name-status 89a10a1b 84f088a2`: 12 paths, none of this change's):
  locked restore rc 0, build `0 Warning(s)`, `0 Error(s)`, `total: 2221`, `failed: 0`, `succeeded: 2217`, `skipped: 4`;
  the two publishes of `ci.yml:48` and `:78` rc 0; `release_guard.py` `GUARD-WARN: development CA deny-list holds 0
  fingerprints (owed)` then `GUARD: clean (14 files)` and `GUARD: clean (15 files)`, rc 0; no published file name holds
  `Lab`, `Tests` or `OneDrive`; `Ran 117 tests` `OK` (`ci.yml:211` `FLOOR=117`); `RULES: clean (671 files)`.
- Main 84f088a2's push run (`hosted3.py 84f088a2... --total 2171 --rules 659 --unit 117 --floor 117`, the same options,
  22:31): `HOSTED 84f088a2...: PASS` (linux 2167, windows 2150), Analyze actions, csharp, python success.
- Code scanning: analyses at 84f088a2 csharp, actions, python `results_count 0`; none on the branch (the push ran the
  four jobs only); open alerts repository-wide 0 (22:21 and 22:34). PR 49's head carries 8 distinct check names.
- Public pages (plain unauthenticated HTTPS GET, saved in `g2064/ms/`):
  `raw.githubusercontent.com/dotnet/dotnet-api-docs/main/xml/System/UriPartial.xml` (HTTP 200, 8806 bytes): `Query`
  "The scheme, authority, path, and query segments of the URI." (no fragment; the authority's user info is refused
  before); `raw.githubusercontent.com/microsoftgraph/microsoft-graph-docs-contrib/main/api-reference/v1.0/api/driveitem-list-children.md`
  (HTTP 200, 7596 bytes): `deprecat` 0 lines, control `children` 41.

## SCANS
- gitleaks 8.30.1: control FIRST (a token built by `scratch/gl_prep.py control` from two halves and 36 random characters,
  never printed, alone in a new folder): rc 1, `leaks found: 1` (moved to `_quarantine/gl-control-1`); the 13 head blobs,
  the lane's added lines (BASE..head, 1062 lines, lock files included), round 2's added lines (22), both commit messages
  and both patches under neutral names (19 files, `scratch/gl-neutral`): rc 0, `no leaks found`.
- `words.py --control`: `CONTROL FIRED: 13 of 13`; over `checks-base/added.txt` (833 lines, the lane's non-lock added
  lines), `checks-r2/added.txt` (22) and both commit messages: `WORDS: clean (4 files)`. (Over the 1062 lines with the
  lock files: 4 hits, all the runtime identifiers `linux-x64` / `win-x64` of the two new lock files, which the `seat ids`
  class reads as `x64`: false hits, as in every lock file.) `B2[0-9]{3}` over the added lines and both messages: 0, 0, 0
  (control: this commission 6).
- This folder's texts: `squash_scan.py` (the squash tree's `build/`, sha256 equal to main's) with #50 and with #51: each
  `control ... rc 1, found 2`, `message: rc 0, found 0`, `SQUASH-SCAN: clean`. `words.py` over squash-subject (#50),
  squash-body.txt and pr-title.txt: `WORDS: clean (3 files)`. gitleaks over the seven files of this folder: the last
  line of this section, written after the scan.
- gitleaks (about 22:37): the control re-scanned first (`_quarantine/gl-control-1`) rc 1 `leaks found: 1`; this folder's
  seven files under neutral names (`scratch/gl-texts`, before this line was added) rc 0 `no leaks found`. Origin re-read
  at 22:38: the branch at 51e91c26, main at 84f088a2, open pull requests 0, open alerts 0.

## NOT RUN
- CodeQL locally (the C# extractor is x86_64; this Mac runs no x86_64 program, RELAYED from the kit's FACTS 5): the pull
  request's code scanning is the CodeQL read (landing.txt step 3).
- The pull request, its merge-ref run and its code scanning (Tuesday's landing; numbers given in landing.txt).
- The wire: no socket was opened; what a real handler puts on the request line is DERIVED from the `RequestUri` the fake
  recorded.
- Any Microsoft host, tenant or token: how Graph answers G1 to G3, and whether it treats case or escape variants as one
  address, is UNMEASURED (the tenant test, C-76).
- Linux and Windows behaviour of the probe shapes: macOS arm64 only (the cells ran green on both hosted legs).
- The seat's neutral scan of stored objects (`run_step.py`) was not re-run by me; the hosted secret-scan job's proof lines
  stand for it (read above).
- Gate mutants beyond the kit's 16.
- Whether GitHub lets the owner remove a pull ref (FOUND 1).

## LANDING
GO WITH FINDINGS on this head: land by `landing.txt` (head-pinned squash of 51e91c26 onto 84f088a2, `--min-checks 8`,
the merge-ref proof against the main of the moment, the PR's code scanning, squash scan with the real number, main's push
run after at `--total 2221 --rules 671 --unit 117 --floor 117`). FOUND 1's step 0 is the coordinator's choice before the
pull request is opened; nothing else is owed before landing.
