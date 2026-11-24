GATE B2061: NO GO @ 4b9814f on main f5882ed

Gate G1 (raised from the kit's G2 at stamp S4: the first app module to take a user's token source, and the "no deprecated
Graph calls" property, C-84), ROUND 1 OF 2 of lane L3, one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2,
lane L3, kit B2056 (seat X66; Stamp S4: Q1 "a" and Q2 "a" in words, Q3 G1, Q4 to Q9 the defaults; every one the
coordinator's, none the product owner's). Head `4b9814f1b18fb269ac88862e99355e267a57eba2` on `b2056/l3-onedrive-browse`,
ONE commit, one parent `89a10a1ba26a16aae7996e059d548bf53531fd44` (no rebase). **Main MOVED during the gate:** PR 48 (lane
L1 round 2) was squashed at 10:23:44Z (21:23:44 AEDT) as `f5882ed74275200ffd37ac998ee650ada0820241` (one parent 89a10a1b;
its tree equals PR 48's head 105b3465; GET 21:32). compare main...4b9814f1: diverged, ahead 1, behind 1, 13 files. The
branch still at 4b9814f1 (GET 21:32); open pull requests 0. Read and measured 2026-11-24 21:21 to 21:40 AEDT in my scratch
`fleet/state/s324/g2061/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity), worktrees `w` (the head;
the mutants ran here and were undone: `status --porcelain` 0 rows, `diff --stat 4b9814f1` empty), `red` (89a10a1b +
`1-red.diff`), `p` (the head + one gate probe file, now `_quarantine/G2061Probe.cs.txt`; `p` equals the head again) and
`m` (the merge of the head with f5882ed7, tree `35287829`). Every dotnet job and test executable through the kit's
`heavy.py` (sha256 `31adedc8...`) and the wave lock, one at a time (42 released lock folders, all mine, in
`g2061/_quarantine/locks/`; lock waits 0 on every job; no other holder seen; the lock absent at the end). Origin by
`gh api -X GET` under the project GH_CONFIG_DIR. Microsoft's public documentation by plain unauthenticated HTTPS GETs of
raw files (named in THE GRAPH CALLS and FOUND 1). No write to the project, GitHub or Jira; no push, no pull request, no
re-run; no tenant, token, Microsoft API, Azure, printer or device; nothing deleted (moved to `_quarantine`).

**BLUF.** The code holds its G1 property: **no input I could build makes the module send a request other than G1, G2 or a
G3 children call on the base host, and no deprecated Graph call is reachable.** MEASURED by a probe of 43 next-link shapes
(Unicode and case-folded hosts, punycode, dot segments, percent-escaped dots, slashes and backslashes, NUL, tab and newline,
`;`, `%3F`, double and trailing slashes, `root:` paths, scheme-relative and relative links, a deeper base path, queries and
fragments) through the landed `GraphClient` and a fake handler that records every `RequestUri`: each is refused
`NextLinkElsewhere` with nothing sent, or sent as a children path of the four forms on `files.kilo.example.test` (the dot
forms are normalised by `Uri` BEFORE the check, and the sent address is the checked object's `AbsoluteUri`). The head is
BASE plus the two frozen patches byte for byte (temporary index: red tree `85982439`, both `29eda104` = `4b9814f1^{tree}`);
ten tools 10 of 10 equal in my copy and in the seat's `.tools/b2056/gate`; red first exactly THE CONTROLS (41 of 41 by
`Assert.`); green 2202 / 0 / 2198 / 4; `MUTANTS: 15 of 15 MATCH, 15 of 15 undone equal` (my run of the frozen tool);
`CHECKS: 10 of 10 PASS`; `RULES: clean (671 files)`; `Ran 111 tests`; hosted `HOSTED 4b9814f1...: PASS` (my read); the
merge with the moved main 2220 / 0 / 2216 / 4, `RULES: clean (671 files)`. **It is NO GO for one reason only (FOUND 1):** the
test literal `D4648F06C91D9D3D!54927` has the exact shape of a real consumer OneDrive item id, the kit's HOLDS forbid a
real or real-looking item id in any file, and I could not show it synthetic or a public example (0 hits in 28 Microsoft
source files; it first appears in the drafter's own `1-red.diff`). A squash would put it in main's history, which can be
neither removed nor rewritten; round 2 replaces it (one `[InlineData]` line). FOUND 2 and 3 are Minor and ride round 2 at
the coordinator's choice. **If the coordinator rules FOUND 1 not blocking, everything else I measured reads GO WITH
FINDINGS.**

## FOUND (graded; whether each blocks landing)

1. **Major, BLOCKS landing of this head (a real-looking OneDrive item id in a committed test; origin not established).**
   `tests/Datasec.Suite.OneDrive.Tests/BrowseTests.cs:36` `[InlineData("D4648F06C91D9D3D!54927")]` (O02's second row): 16
   upper-case hex digits, `!`, 5 digits, the consumer OneDrive id shape. The kit's HOLDS: "no real or real-looking address,
   user, tenant, drive id, item id, token or file name in any file". **Origin, MEASURED:** `git grep -i -F
   D4648F06C91D9D3D` at BASE 89a10a1b: rc 1 (none); at the head 1 file, 1 line. In Microsoft's public sources, by plain
   GETs of raw.githubusercontent.com (each read named in `g2061/logs/ms_fetch1.out`, `ms_fetch2.out`, `ms_fetch3.out` and
   the curl of list-children): 0 lines in each of 28 files (microsoftgraph/microsoft-graph-docs-contrib `main`:
   api-reference/v1.0/api/ driveitem-list-children, drive-recent, drive-sharedwithme, driveitem-get, driveitem-delta,
   driveitem-search, drive-get, driveitem-list-thumbnails, driveitem-createlink, driveitem-copy, driveitem-invite,
   driveitem-move, driveitem-post-children, shares-get, drive-list-following, driveitem-get-content; v1.0/resources/
   remoteitem, driveitem, drive, itemreference; concepts/onedrive-concept-overview; two list-children C# snippets; beta
   driveitem-list-children; OneDrive/onedrive-api-docs `live`: four redirect stubs). Microsoft's own examples use
   obviously invented ids instead (`1312abc!1231`, `1991210caf!192` in drive-recent.md:108-111; `987def!654` in
   drive-sharedwithme.md:159; `0123456789abc!123` in driveitem-search.md:115). In the drafter's files (scoped grep of
   `d2056/scratch`, `evidence`, `seat-tools`): only its own `1-red.diff` and the copies made from it; its report, its
   commission and the kit: 0. gitleaks and `words.py` are clean over it (neither looks for an id shape). It cannot be shown
   synthetic or public-example, so by the commission's rule it is a finding. Harm if real: an item identifier of a
   consumer account (not a credential) in a private repository, permanent once squashed onto main. **Fix (round 2): replace
   it with an obviously synthetic id of the same shape class, for example `SYNTHETIC0002!12345` (letters, digits and `!`,
   so H2 keeps its `!` row), and let `mFolderSelectDropped` stay red on O02's three rows.** Not a code defect: O02 tests
   the same rule with any id.

2. **Minor, does NOT block (README over-claim: "this slice never opens another user's drive").** `README.md:40` "An entry
   that points to another drive is listed and not followed: this slice never opens another user's drive." True of a
   `remoteItem` entry; not of a next link. `IsChildrenPath` (`MyDriveBrowser.cs:269`-`:270`) takes
   `drives/{id}/root/children` and `drives/{id}/items/{id}/children` for ANY drive id that passes the id rule: the module
   cannot know the user's own drive id. MEASURED (probe F4, F5): a first page whose next link names
   `drives/SYNTHETICDRIVE0001/root/children` or `drives/b!SYNTHETIC_drive-0001/items/SYNTHETICX0001/children` (drive ids
   unrelated to the listing) is requested, with the user's token, by the layer. Bounded: it is still Microsoft's documented,
   non-deprecated list-children call on the base origin, Graph enforces access, and only a server's own next link can name
   it (Q2 "a" chose these four forms; the kit's Q2 alternative "b" names exactly this trade). Fix when next touched (round 2
   or later, the coordinator's choice): state it in README Limits ("a next link of a `drives/{id}` form is followed
   whatever drive it names"), or bind the `drives/{id}` forms to a drive id the listing has seen.

3. **Minor, does NOT block (a fragment defeats the loop rule; bounded by the page bound).** `Followable`
   (`MyDriveBrowser.cs:258`) compares `next.AbsoluteUri`, which keeps the fragment; the request sent carries no fragment
   (`PathAndQuery`). MEASURED (probe P2): a server that answers every page with the address just requested plus `#f<n>`
   gets the SAME request (1 distinct `PathAndQuery`) sent 100 times, then `TooManyPages` at page 101; `PagingLoop` never
   fires. The doc comments (`OneDriveBrowseException.cs:17` "names an address the listing already requested; it was never
   requested again"; `MyDriveBrowser.cs:242`-`:243`) over-claim for this shape. The landed layer's `FollowableLink`
   (`GraphClient.cs:734`) has the same comparison (not this lane's). Harm: 99 extra identical children calls inside the
   page bound. Fix when next touched: compare `next.GetLeftPart(UriPartial.Query)`, or refuse a next link with a fragment.
   (A query that differs, `x=0`/`x=1`, is caught on its first repeat: probe P2b, `PagingLoop` at page 3.)

4. **Info (G3 takes any query, as decided; never a path).** MEASURED (probe Q1 to Q4): `children?$x=/../../recent`,
   `?$expand=thumbnails&$select=id`, `?$search=a` and `#/../../recent` are each sent to the children path unchanged
   (`Uri` does not normalise a query or fragment; `AbsolutePath` stays `/v1.0/me/drive/root/children`). The kit's G3 says
   "(any query)"; the README and the class summary do not mention the query. A query option outside the five the page
   documents (`$expand`, `$select`, `$skipToken`, `$top`, `$orderby`, list-children.md:44) can therefore be sent when a
   server names it; what Graph does with `$search` on children is UNMEASURED. No query reaches another path.

5. **Info (the fourth children form is documented by composition, not as a request line).** G1 is list-children.md:64
   (`GET /me/drive/root/children`, its example), G2 list-children.md:37, `drives/{id}/items/{id}/children`
   list-children.md:35 and :106. `drives/{id}/root/children` is no line of the page: it is the drive's `root`
   relationship (drive.md:66 "root | driveItem | The root folder of the drive", drive.md:26 "Get drive root") with
   list-children ("use the `root` relationship on the drive, then access the children relationship", list-children.md:57
   and :99; drive.md:29 "List children ... List children of the root folder of a drive"). As the kit said (DERIVED).
   **None of the four is deprecated:** list-children.md 0 lines holding `deprecat` (re-fetched by me, HTTP 200, 7596
   bytes, `cmp`-equal to the drafter's copy; control `children` 41 lines); the drive resource marks exactly two calls
   deprecated, drive.md:33 "Recent (deprecated)" and :34 "Shared with me (deprecated)" (controls: drive-recent.md and
   drive-sharedwithme.md 3 lines each, their titles at :4 and their notices at :16, "degraded state until November,
   2026").

6. **Info (item rules: the kit's H12, H13 and H17 (d) (e) shapes, now MEASURED; nothing dropped silently).** Probe P4:
   `size` 12.0 and 1e3, and `childCount` 3000000000 end `MalformedItem` (refused, not dropped); `lastModifiedDateTime`
   `01/02/2026` is read as 2026-01-02 (the invariant culture's month/day) and `2026-01-02` as midnight UTC; a name of one
   space is listed (the rule is "non-empty"); a `package` facet is listed as `Other`; `size` and `folder` null read as
   absent; a duplicate `id` property: the LAST one is the one read and checked (`a/b` last: `MalformedItem`; a valid id
   last: listed with it), so the checked id is the listed id; an `id` of `..` ends `MalformedItem`. Pages (P4p): `value`
   not an array, not JSON, a top-level array, a next link that is a number or an unpaired surrogate escape: each
   `MalformedPage`. Every element of `value` becomes an entry or ends the listing (`ReadPage`, `:136`-`:146`).

7. **Info (ids of dots).** `IsItemId` takes `...`, `a..b`, `.a`, `a.`, `!`, `-`, `_` and the module sends them as one
   segment unchanged (probe P5, D7). How Graph's front end treats a segment of three dots or a trailing dot is UNMEASURED;
   DERIVED: every path the module can send ends in the segment `children`, so no normalisation of an id segment can reach
   `recent`, `sharedWithMe` or a search.

8. **Info (no next-link length bound of the module's own).** The layer's `MaxNextLinkLength` (`GraphClient.cs:729`) is
   applied only inside `GetPagesAsync`'s walk; the module's walk has no length check (a long link is bounded only by the
   layer's body bound). Not a property the kit claims.

9. **Info (the seat's OPEN items).** The O02 literal: FOUND 1. The release guard's `GUARD-WARN: development CA deny-list
   holds 0 fingerprints (owed)` predates this lane; no file of this lane touches the guard.

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE", and the commission's WHAT TO DO 1), item by item
- **`89a10a1b..4b9814f1` read whole:** the 12 added files and the slnx diff read whole (the two lock files by program:
  every (id, version, contentHash) of both is in a landed lock file of the head, `scratch/locks.py`, control a planted
  triple missing); `GraphClient.cs` `SendAsync` (52-72), `FollowableLink`, `OnBaseOrigin`, `ResolveAddress` (727-760),
  `GraphOptions.cs` 1-45, `GraphRequest.cs`, `GraphToken.cs` re-read at the head.
- **The tree = BASE + both patches byte for byte:** `29eda104` both ways; the message equals `commit-message.txt` (343
  bytes); author equals committer, `@datasec.com.au`; 13 rows, 1 M and 12 A, numstat 2/0 and 12 added files.
- **Red first:** `Total: 49, Errors: 0, Failed: 41`; per cell O01 1, O02 3, O03 9, O04 1, O05 14, O07 1, O08 11, O09 1
  (equals THE CONTROLS); 41 of 41 `[FAIL]` followed within five lines by `Assert.<X>() Failure`; none outside O01 to O09.
  Restore (`CI=true`, locked) rc 0, build `0 Warning(s)`, `0 Error(s)`. Logs `g2061/logs/r-*.log`.
- **15 mutants, each red on exactly its cells:** every row MATCH and undone equal True, identical to the kit and the seat
  (`g2061/logs/mutants-run.out`): mSelectDropped O01 O04 O09 (3) | mFolderSelectDropped O02 (3) | mIdDotsTaken O03 (2) |
  mIdCharsOpen O03 O05 O08 (8) | mIdLengthOpen O03 (1) | mDuplicateTaken O05 O07 (2) | mBothFacetsTaken O05 (1) |
  mSizeSignTaken O05 (1) | mRemoteShapeTaken O05 (1) | mRemoteIgnored O01 (1) | mPathUnchecked O08 (6) | mPortUnchecked
  O08 (1) | mLoopUnchecked O09 (1) | mPageBoundOffByOne O10 (3) | mNameInText O07 (1).
- **Any request not G1, G2 or G3:** none (BLUF; the probe table below). Another form (`sites/...`): refused (F6). A
  percent-escaped segment: `%2F`, `%5C`, `%00`, `%3F` refused; `%2e%2e` and `%2E` are unescaped AND compressed by `Uri`
  before the check (`AbsolutePath` `/v1.0/me/drive/children`, `/v1.0/me/drive/items/children`), then refused; `%41BC` is
  unescaped to `ABC` and sent as `ABC` (the checked text). A Unicode segment: escaped to `%C4%B0`, refused. A dot segment:
  compressed first; `.../recent/../root/children` is SENT as `/v1.0/me/drive/root/children` (a G3 call), and
  `.../items/x/../../recent` is refused. A link the parser normalises: upper-case scheme, explicit `:443`, upper-case host
  and a Kelvin-sign `K` host are normalised to the base host and sent there (`Host`, `IdnHost`, `DnsSafeHost` all
  `files.kilo.example.test`); a dotless-i host (`IdnHost` `xn--fles-lza...`), a long-s host and a full-width host are
  refused (the host compare is on `Host`, which keeps the Unicode form). A base with a deeper path (`/v1.0/sub/`): only
  links under it are followed (P3). A query that smuggles a path: stays a query (FOUND 4). A relative or scheme-relative
  link parses as `file:` on this OS and is refused.
- **A deprecated call reachable by any input:** no. `ListFolderAsync` takes only ids of `[A-Za-z0-9!._-]{1,256}`, not `.`
  or `..`, as one segment between `items/` and `/children`; next links only as above; `checks_l3.py` check 9: 0 lines of
  the module hold `recent`, `sharedwithme` or `search`, 2 hold `"me/drive/`; check 10: one `_graph.SendAsync(`, no
  `GetPagesAsync(` or `UploadAsync(`.
- **The four children forms documented and not deprecated:** FOUND 5.
- **An item returned that breaks a rule, or dropped silently:** none (FOUND 6).
- **A name or id in a text:** none. Every exception text is fixed or built from the kind and numbers (O07; the probe's
  refusals print `The item id is not one this listing takes. (Parameter 'itemId')`, `My Drive listing failed: <kind>,
  page <n>, item <n>.`, and the layer's `Graph call failed: ..., host <base host>.`); `ToString` of an entry and a
  listing hold counts, kind and size.
- **The token source:** passed to `ListAsync` and on to `_graph.SendAsync` only (`MyDriveBrowser.cs:60`, `:77`, `:106`);
  no field, no log, no call on it. `GraphToken.Value` is `internal` (`GraphToken.cs:33`) and the Graph assembly's only
  `InternalsVisibleTo` is `Datasec.Suite.Graph.Tests` (`Datasec.Suite.Graph.csproj:3`): the module cannot read it.
- **The README sentences against the code:** every sentence holds but `README.md:40`'s second half (FOUND 2). The calls
  table (G1, G2 and their page) holds; "Microsoft marks the first two deprecated" holds (drive.md:33-34); the four forms
  and `NextLinkElsewhere` hold (probe); "page 101 ends the listing (`TooManyPages`)" holds (probe P2: 100 requests, page
  101); the item rules and "nothing is left out silently" hold; "never keeps it and cannot read the token's text" holds.
- **The two new lock files hold only packages already in the repository:** yes (check 4 by id; `locks.py` by id,
  version and content hash; the locked restore rc 0 on the head, the red tree and the merge).

## FRAME (stamp checklist item 11: each every/never/only sentence the change adds, three shapes outside the tested one)
- "makes ONE kind of Graph call ... It makes no other call" (`MyDriveBrowser.cs:10`-`:13`) and README:17-21 "never
  called ... any other link ... is never requested": dot segments (D1 sent as G3, D2 refused), Unicode hosts (H1 to H5:
  refused or the same host), percent escapes (D4 to D6, E1 to E3, E8), a query (Q1 to Q4: sent, children path). Covered;
  the query is FOUND 4 (Info).
- "a next link ... on the base address's origin": `:443`, a trailing-dot host (refused), userinfo (O08), a deeper base
  (P3). Covered.
- "a link already requested is PagingLoop ... never requested" (`MyDriveBrowser.cs:242`-`:243`,
  `OneDriveBrowseException.cs:17`): the exact link (O09), a fragment variant (FOUND 3), a query variant (P2b caught on
  repeat). One finding.
- "An item is read only when ... nothing is left out silently" (`:17`-`:22`, README:29-31): duplicate `id` properties, a
  number written `12.0` or `1e3`, a non-ISO date, a white-space name, a `package` facet (FOUND 6). Covered or stated (the
  non-ISO date and the white-space name are accepted: the rules allow them).
- "the token source is passed into each call and never kept here" / "cannot read the token's text": code read, the
  `internal` property and the single `InternalsVisibleTo`. Covered.
- "never the name or the id" (`DriveEntry.cs:20`, `MyDriveListing.cs:20`, `OneDriveBrowseException.cs:25`-`:26`): O07,
  the probe's refusal texts, the layer's text (host only). Covered.
- "this slice never opens another user's drive" (README:40): a `remoteItem` (listed, not followed: O01), a `drives/{id}`
  next link (FOUND 2), a folder id from another drive passed by a caller (only `me/drive/items/{id}`: the user's drive).
  One finding.
- The kit's H1 to H17: H1 to H11 as the cells say (green; each red cell red under its mutants); H12, H13, H14 MEASURED
  (probe P4, P4p); H15 MEASURED for `sites/...` (F6, refused); H16 the layer's own cells (not re-tested); H17 (a) MEASURED
  (D1, D2: `Uri` compresses before the check), (b) MEASURED in process (`PathAndQuery` holds no fragment; the wire is
  UNMEASURED: no socket opened), (c) as designed (FOUND 4), (d) and (e) MEASURED (FOUND 6), (f) MEASURED (upper-case host
  accepted, normalised).

## THE PROBE (scratch only, never committed: `_quarantine/G2061Probe.cs.txt`; output `scratch/probe-report.txt`)
One test file added to the OneDrive tests in `p` (its own `FakeGraph` per row, the landed `GraphClient`, base
`https://files.kilo.example.test/v1.0/`, synthetic ids and token); the test executable run whole: `Total: 96, Errors: 0,
Failed: 0` (49 + 47 probe cases), build `0 Warning(s)`.

| Rows | Outcome (requests) |
|---|---|
| H4 upper-case host, H7 `:443`, H9 `HTTPS:`, H3 Kelvin-sign host | sent to `files.kilo.example.test`, children path (2) |
| H1 dotless i, H2 long s, H5 full-width f, H6 trailing dot, H8 punycode | `NextLinkElsewhere` (1) |
| D1 `recent/../root/children` | sent as `/v1.0/me/drive/root/children` (2) |
| D2 `items/x/../../recent`, D3 `../beta/...`, D4 `%2e%2e`, D5 `%2E`, D6 `%2e%2e/%2e%2e/recent` | `NextLinkElsewhere` (1) |
| D7 `items/.../children`, E1 `%41BC` (sent `ABC`) | sent, children path (2) |
| E2 `%2F`, E3 `%5C`, E4 backslashes, E5 `%3F`, E6 `;`, E7 `I` with dot, E8 `%00`, E9 tab, E10 newline, E11 `V1.0`, E12 `//`, E13 trailing `/`, E14 `root:/recent:/children`, E15 `me%2Fdrive%2Froot` | `NextLinkElsewhere` (1) |
| Q1 path text in a query, Q2 `$expand`/`$select`, Q3 fragment, Q4 `$search` | sent, children path, query unchanged (2) |
| F1 relative, F2 scheme-relative, F3 no slash, F6 `sites/...`, F7 empty, F8 a 257-character id | `NextLinkElsewhere` (1) |
| F4 `drives/{id}/root/children`, F5 `drives/{id}/items/{id}/children` | sent (2) (FOUND 2) |
| P2 the same address + `#f<n>` | 100 requests, 1 distinct, `TooManyPages` page 101 (FOUND 3) |
| P2b the same call, query `x=0`/`x=1` | `PagingLoop` page 3 (3) |
| P3 base `/v1.0/sub/` | under it: sent; `/v1.0/...` and `../`: refused |
| P4, P4p, P5 | FOUND 6, FOUND 7 |

One probe row is the probe's own artefact, not the module's: an item whose name is an unpaired surrogate escape made
the probe's page builder (`JsonNode` then `ToJsonString`) throw inside the fake handler, read by the layer as
`Transport`. The module's own path for that shape is the `InvalidOperationException` catch (`:226`); the same mechanism is
MEASURED for a next link (P4p row 4: `MalformedPage`), so the item path is DERIVED.

## THE HEAD, MEASURED BY THE GATE (logs `g2061/logs/`)
- Locked restore (`CI=true`) rc 0; build `0 Warning(s)`, `0 Error(s)`; `dotnet test -c Release --no-build`: `total: 2202`,
  `failed: 0`, `succeeded: 2198`, `skipped: 4` (h-test, before the mutants).
- `repo_rules.py` (plain form, `test ! -e w/1_Project_Definition` rc 0): `RULES-NOTE: R5 hash half NOT RUN (no
  supplied-source folder here)`, `RULES: clean (671 files)`; `unittest discover -s build/tests`: `Ran 111 tests`, `OK`;
  `ls-files` 671.
- `checks_l3.py w 89a10a1b`: `CHECKS: 10 of 10 PASS` (13 rows, 1 M 12 A; shared files rc 0; slnx 2 added, 0 removed; lock
  ids 2 and 19, 0 new; ascii 13 files; added 815; public 41; no package or own HTTP; recent/sharedwithme/search 0,
  `"me/drive/` 2; SendAsync 1), every control fired.
- Hosted push run 45372638705 (`hosted3.py 4b9814f1... --total 2202 --rules 671 --skipped-linux 4 --skipped-windows 21
  --unit 111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15`, 21:26): linux `succeeded: 2198`, windows
  `succeeded: 2181`, both `total: 2202` twice, GUARD 14 and 15; rules `RULES: clean (671 files)`, `UNIT-TEST FLOOR: ran
  111, floor 111`; secret-scan every proof line; `check runs beside the four: 0`; last line `HOSTED 4b9814f1...: PASS`.
  `failed Datasec.` lines 0 and 0 (case-insensitive); control: 4 `Datasec.Suite.OneDrive.Tests.dll` lines per leg.
- **The merge with the moved main** (`git merge-tree --write-tree f5882ed7 4b9814f1`: rc 0, tree
  `352878295551b1ad6cb6eca3f4cbb2fb31f5d327`, 671 files; `git diff --name-only 89a10a1b f5882ed7`: PR 48's nine paths,
  none of this change's and no shared file): locked restore rc 0, build `0 Warning(s)`, `0 Error(s)`, `total: 2220`,
  `failed: 0`, `succeeded: 2216`, `skipped: 4`; `RULES: clean (671 files)`.
- Main f5882ed7's push run 45374389206 (`hosted3.py f5882ed7... --total 2171 --rules 659`, the same options, 21:34):
  `HOSTED f5882ed7...: PASS` (linux 2167, windows 2150), Analyze actions, csharp, python success.
- Code scanning: analyses at f5882ed7 and at 89a10a1b, csharp, python and actions `results_count 0`; none on the branch
  ref (the push ran the four jobs only: the pull request's run is the first analysis of this code); open alerts
  repository-wide 0 (21:32).

## SCANS
- gitleaks 8.30.1: control FIRST (a token built by a program from two halves and random characters, never printed, alone
  in a new folder): rc 1, `leaks found: 1` (moved to `_quarantine/gl-control-1`); the 13 head blobs, `added.txt`,
  `commit-message.txt` and both patches under neutral names (17 files): rc 0, `no leaks found`.
- `words.py --control`: `CONTROL FIRED: 13 of 13`; over `added.txt` (815 lines) and `commit-message.txt` (3 lines):
  `WORDS: clean (2 files)`. `B2[0-9]{3}` over both: 0 and 0 (control: the kit 21).
- This folder's texts: SCANS-2 in `landing.txt`.

## NOT RUN
- CodeQL locally (the C# extractor is x86_64; no Rosetta on this Mac, RELAYED from the kit's FACTS 5): the pull
  request's code scanning is the CodeQL read.
- The wire: no socket was opened; what a real `SocketsHttpHandler` puts on the request line is DERIVED from the
  `RequestUri` the fake recorded (`PathAndQuery`, `IdnHost`), not measured.
- Any Microsoft host, tenant or token: how Graph answers G1 to G3 (next-link form, item shapes, `$search` on children, a
  segment of dots) is UNMEASURED (the tenant test, C-76).
- Linux and Windows behaviour of the probe shapes: macOS arm64 only (the cells ran green on both hosted legs).
- A rebuild and whole-solution run of `w` after the mutants (the green run was before; the seat and the drafter each
  measured it after theirs; the merge `m` is a separate fresh build, green).
- Gate mutants beyond the kit's 15.

## LANDING
NO GO on this head for FOUND 1 alone. Round 2 (the last round of lane L3): replace the O02 literal; FOUND 2 (one README
Limits sentence) and FOUND 3 (one comparison) at the coordinator's choice. `landing.txt` is written in full (head-pinned
squash, `--min-checks 8` from PR 47's check names, the merge-ref proof, code scanning, squash scan, MAIN MOVES for main
89a10a1b and for main f5882ed7, which is now main) so that round 2 re-pins the head, the tree and the numbers.
