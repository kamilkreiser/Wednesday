GATE B2208: GO WITH FINDINGS @ b6b5310 on main 7ca5e4c

Gate G1, ROUND 1 OF 2 of the Teams module slice 1 (navigation), one Opus reader (claude-opus-5-5), in-session,
read-only, for Tuesday s338. Kit B2199 (seat X102; S4: Q1 "a" and Q2 "a" IN WORDS, Q3-Q8 the defaults; S8 the counting
runner 89223aca; every choice the coordinator's). Head `b6b531000b61a724ed0ca67631227e1e7292771f` on
`b2199/x102-teams-slice1`, ONE commit, one parent `7ca5e4cefb315f57f4490ce245e1fb762dbf9f6d` (PR 65), tree
`12930aa2d57581855b514b21f169a0aa3d90b351`, 790 files; `diff --name-status 7ca5e4ce b6b53100`: 11 rows, 8 A, 3 M, all
under `src/Datasec.Suite.Teams/` and `tests/Datasec.Suite.Teams.Tests/` (gh api GET 04:42:46 AEDT: compare ahead 1,
behind 0, 11 files; `matching-refs/heads/b2199` one row = the head; main 7ca5e4ce; open pull requests 0). The commit
message equals the kit's `commit-message.txt` byte for byte (279 bytes). Measured 04:42 to 04:59 AEDT in scratch
`fleet/state/s338/g2208/` (`clone`: clone.py draft, push URL `invalid://no-push`, no identity, detached at the head;
worktree `wt-head` at the head; `probe/`, a console program outside the clone that references the head's built
Release assemblies). Every heavy job (restore, builds, test executables, the whole solution, 18 mutant rows, the
probe's build and two runs) through my copy of the kit's `heavy.py` (8 of 8 tool hashes equal THE TOOLS; heavy.py =
S8) under the OXPd wave lock, one holder at a time, queued behind gates B2207, B2209 and B2210 and never breaking an
`owner.txt`; 45 released lock folders of mine in `g2208/_quarantine/locks/`; at the end no process of mine (`ps` 0 rows
naming g2208) and the lock held by gate B2210's own job (05:01:30), not mine; the clone's `status --porcelain` 0 rows at
the end, every mutant undone equal. Nothing to any printer,
device, tenant, Azure, Microsoft host or HP (every request of every cell and probe answered by a handler inside the
process, hosts under example.test); no Jira; no write to the project checkout, the seat's lane or GitHub (the seat's
rows file read by `cat`).

## Grades (round 1 of 2): Blocker 0, Major 0, Minor 1, Info 7. Nothing blocks landing; no fix round.

**The bold question of the gate list, answered first (Tuesday's point a): can any id in its rule add a path segment,
a query or a fragment to a Bearer-carrying request? NO, measured.** FOUND: every id the three rules accept stays one
path segment with an empty query and fragment. TESTED: Tuesday's list (`%2F`, `%2f`, `%2E%2E`, `%3F`, `%23`, a
trailing dot, a trailing space, tab or line feed, U+FF0F, U+FF0E, U+2215, U+2044, U+2024, U+2025, U+FE52, U+2026,
U+00B7, an empty id, ids of 1 to 4 dots) as a bare id and inside a channel-shaped id, through `IsChannelId` and the
REAL request builder (`TeamsBrowser.GetFilesFolderAsync` -> `GraphClient.SendAsync` -> `new Uri(base, relative)` ->
`HttpRequestMessage`), the same and more through `IsTeamId` with `ListChannelsAsync` and `GetFilesFolderAsync`, and
through `IsDriveSegment` with `new Uri(base, "drives/<id>/items")` (this slice sends no drive id; slice 2 will); then a
fuzz of every UTF-16 code unit (0 to 0xFFFF) at the start, middle and end of an id for the channel and drive rules, and
at each of the 36 positions of a team id, plus 182,070 two-position substitutions over a hostile set (`0 x X + - space
tab LF { } ( ) . / g U+FF10 U+0660`). NOT TESTED: Windows (the hosted legs run the cells, not the probe), a real Graph
or any server between. HOW: `evidence-probe-source.cs.txt`, output `evidence-probes.txt` (macOS 27.2.1, .NET
10.0.15); positive control a good channel id sends 1 request and returns the folder; negative control a slash id sends
0 and throws `ArgumentException`. Every refused id sent NO request; every sent request carried `Bearer <redacted>` and
`segments=7`, `q=` empty, `f=` empty. The three findings below are rules WIDER than their stated text, inside one
segment.

**F1 MINOR (P1/P3/P4; R15 beyond the kit): the channel rule and the drive rule end in a regular-expression `$`, which
in .NET also matches before ONE final line feed: an id ending in `\n` passes, is sent, and a listing or folder answer
holding one is returned.** FOUND (probe a): `19:x@thread.tacv2\n` rule=True, SENT
`/v1.0/teams/<team>/channels/19:x@thread.tacv2%0A/filesFolder`; `..\n` and `.\n` pass (the `is not ("." or "..")`
test compares the whole text) and are sent as `..%0A` / `.%0A`, which .NET does not decode or treat as a dot segment
(segments 7, the same path shape); a files-folder answer with `id` `ITEM0001\n` or `driveId` `b!drive_0001\n` is
RETURNED with the line feed in `ItemId` / `DriveId`; a channel listing holding `19:a@thread.tacv2` and
`19:a@thread.tacv2\n` returns BOTH (the duplicate rule is ordinal on the raw text). `\r\n`, a bare `\n`, a space and a
tab are refused. The fuzz finds this the ONLY character outside each stated class that either rule accepts
(`channel abc\n`, `drive abc\n`). Why it matters: the module's own doc comment and README state the channel id "holds no
... space" and a drive id is "1 to 256 characters of ASCII letters, digits and `! . _ -`"; the code is wider; no cell
holds a trailing line feed, so nothing guards it; slice 2 will SEND the drive and item ids this slice returns, and how
Graph or a front end treats `%0A` at the end of a segment (trimmed to `..`?) is UNMEASURED. The Bearer stays on the
Graph origin by the layer's rule, so this is not a token leak. Fix shape (one line each, a follow-up or slice 2's
first lines): `\z` in place of `$` in both `GeneratedRegex` patterns (`^[...]+\z`),
with a T06 row `19:a@thread.tacv2\n` and a T09 row `baddrive` ending in `\n`. The landed OneDrive rule has the same form
(F7).

**F2 INFO (P1, team rule): `Guid.TryParseExact(teamId, "D", ...)` behind the 36-character test accepts `+` at the
start of any of the five groups and `0x` / `0X` at the start of groups 1, 2 and 5 (seen by one substitution; groups 3
and 4 need two and were not listed whole); such an id
is sent as written.** FOUND (fuzz): 719 single-unit substitutions of a 36-character team id accepted, 11 of them holding
a character outside `[0-9A-Fa-f-]` (`+0000000-...`, `0x000000-...`, `00000000-0X00-...`, `00000000-0000-4000-8000-+0000
0000001`, ...); probe a: `0x000000-0000-4000-8000-000000000001` SENT `/v1.0/teams/0x000000-.../channels?$select=
id,displayName` and `.../channels/<channel>/filesFolder`. Fullwidth and Arabic-Indic digits, a dot, `%`, `/`, a
trailing space, tab or line feed: refused (DERIVED: the GUID reader trims white space, which leaves 35 characters). `+`, `x`, `X` cannot
form a separator, so P1 holds; the README's "36 characters in the hyphenated GUID form" is wider in fact. Fix shape (if
wanted): also require `[0-9A-Fa-f-]` only, or compare with `Guid.ToString("D")` ignoring case.

**F3 INFO (the seat's R15 a, the trailing-dot shape, for the gate to decide): a channel id that ends in a dot or is
three or more dots passes and is sent as written; .NET keeps the segment.** FOUND (probe a): `19:x@thread.` ->
`.../channels/19:x@thread./filesFolder`; `...` -> `.../channels/.../filesFolder`; `....` likewise; all
`intended(exact)=True`, segments 7. RFC 3986 section 5.2.4 removes only the complete segments `.` and `..` (general
knowledge), and .NET 10 behaves so on macOS (measured; the seat measured the same). NOT TESTED: Windows (.NET's `Uri`
for the http scheme is managed code shared by both platforms: DERIVED, not run there), and whether Graph or a front end
trims a segment's trailing dots (UNMEASURED; a Windows file-path style trim would turn `19:x@thread.` into another
channel id of the same team). The token never leaves the Graph origin. Decision: acceptable for slice 1 as a named limit
(pr-body 4); recommend slice 2 refuse a channel or drive id that ends in `.` (Microsoft's example channel ids end in
`thread.tacv2` / `thread.skype`, kit FACTS 6), with a T06 row.

**F4 INFO (the seat's DEVIATION 1, guard counts): the seat was RIGHT to follow the source.** FOUND: main 7ca5e4ce's own
push run reads `GUARD: clean (28 files)` / `(29 files)`: `hosted3.py 7ca5e4ce --total 2564 --rules 782 --guard-linux 28
--guard-windows 29` PASS; the same with 14 / 15 FAIL 2 (`GUARD: clean (14 files)` count 0, `(15 files)` count 0). The
counts moved with lane L3a (PR 64, the server wiring Graph and OneDrive; gate B2196 measured 14 -> 28 / 15 -> 29). This
lane changes no published file (the server project does not reference Teams; the head's hosted legs read 28 / 29).
The kit's "The guard counts do not move" was true at its BASE d9f89115 and stale after the move; no STOP was owed.

**F5 INFO (mutants): the kit's eight re-run on the head, 8 of 8 MATCH, the same red cells as the seat's; the gate's own
ten, 8 MATCH, 2 SURVIVE (no cell row).** HOW: `mutants_c3.py` (sha256 08e43be7, the kit's) through the runner; the
kit's rows file read from the seat's lane by `cat`, sha256 `e278c8ed...` = the seat's STATUS; my rows
`evidence-gate-mutant-rows.json` (sha256 `59700072...`), written before the run, `--list` `LIST: 10 mutants, 1 suites,
13 cells`. Kit rows: mTeamIdUnchecked T04 T07 (Failed 4); mChannelDotsTaken T06 (2); mChannelSlashTaken T06 T08 (2; T08
inside the suite); mFolderFacetUnchecked T09; mDriveIdUnchecked T09; mDuplicateKept T07 T08; mNameEmptyTaken T07 T08;
mPageBoundDropped T11 (1); `MUTANTS: 8 of 8 MATCH, 8 of 8 undone equal`. Gate rows: MATCH gChannelLengthDropped (T06,
the 257-character row), gChannelCheckDropped (T06, 8 rows), gEntryIdUnchecked (T07 T08), gFolderIdUnchecked (T09),
gSelectWidened (T03, both rows: the select is pinned), gTeamEntryLeaks, gChannelEntryLeaks, gFolderLeaks (T12 each: a
name or id in a ToString is caught); SURVIVE gTeamLengthDropped (no cell offers a space-padded GUID longer than 36: the
GUID reader trims, so without the length test such an id would pass; the test is present) and gDriveDotsDropped (no
cell offers a folder answer whose id or drive id is `.` or `..`; probe a measured `IsDriveSegment` refusing both).
`MUTANTS: 8 of 10 MATCH, 10 of 10 undone equal`. After both runs: clone porcelain 0 rows, `TeamsBrowser.cs` sha256
`67cd8e9b...` again, rebuild 0 / 0, the Teams executable `Total: 48, Failed: 0`.

**F6 INFO (cells): T05 asserts the request path against `TeamsSynthetic.PathOf(...)`, the same `new Uri(base, ...)`
rule the layer uses, so it cannot see an escaping change of `:` or `@`; T03 pins the team path as exact text.** The
unescaped form `/channels/19:synthetic0001@thread.tacv2/filesFolder` is measured by the probe (macOS) and by the seat's
probe, not by a cell on either hosted leg. By design (kit T05: "printed, not asserted"); named for the tenant run (R12).

**F7 INFO (outside this lane, pre-existing): the landed OneDrive rule `MyDriveBrowser.IsItemId`
(`src/Datasec.Suite.OneDrive/MyDriveBrowser.cs:84`, `[GeneratedRegex("^[A-Za-z0-9!._-]+$", ...)]` at :87) has F1's form**
(read; this lane copied it as the kit's D3 says). OneDrive sends item ids in `me/drive/items/<id>/children`; a follow-up
for the OneDrive lane, not a reason to hold this one.

**F8 INFO (process, my own):** four of my shell calls were REFUSED by the session's hooks before anything ran (a `cd`,
an unquoted `======` separator, a git write verb on a variable path the hook could not resolve, a `cp` whose SOURCE was
in the seat's lane; each redone without the pattern: `cat >` for the rows file); one `grep -c` of the gate's own rows
counted 0 because the kit's mutant run had applied `mTeamIdUnchecked` at that moment (re-checked by `--list` after the
undo). No probe or mutant ran in the project checkout.

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE (G1 ...)", line 217), whole
- **`<BASE>..<head>` read whole:** 11 files read in full (TeamsBrowser.cs 240 lines, the three result types, the
  exception, the csproj, the README, TeamsFake.cs 153, TeamsTests.cs 291, both lock diffs). `checks_teams.py <clone>
  7ca5e4ce g2208/scratch/checks`: `CHECKS: 10 of 10 PASS`, each control FIRED (1 rows 11 A 8 M 3; 3 the frozen csproj
  True; 4 BASE lock files 56, known packages 68, project entries 2 / 3; 6 T01-T13 once each; 7 staged Fact 6 Theory 8
  InlineData 42; 8 every banned text 0, `me/joinedTeams` 2, `/channels` 4, `/filesFolder` 2, `GetPagesAsync` 2; 9 landed
  files changed 0; 10 README counts); `added.txt` 857 lines, lock lines 62. Lane L0's three kept files have the same
  blob ids at main and head (AssemblyMarker `1fdcc993`, SkeletonTests `ef000031`, test csproj `31d8b088`).
- **The pin run and each mutant's reds:** the gate's runs of the head: locked restore rc 0 (porcelain 0 after), build
  `0 Warning(s)` `0 Error(s)`, Teams executable `Total: 48, Errors: 0, Failed: 0` (three times: before, between and
  after the mutants); whole solution `total: 2611`, `failed: 0`, `succeeded: 2607`, `skipped: 4` (74 s, no bound
  reached); mutants F5.
- **Any id in its rule adding a path segment, a query or a fragment to a Bearer-carrying request:** NO (the bold
  answer above); rules wider than stated: F1, F2, F3.
- **Any request sent before an id check:** NO. By reading: `ListChannelsAsync` checks the team id before `ListAsync`;
  `GetFilesFolderAsync` checks null, team, then channel before `SendAsync`; `ListJoinedTeamsAsync` takes no id. MEASURED:
  T04 (7 rows x both calls) and T06 (8 rows) assert 0 requests; every refused probe shape sent 0; gChannelCheckDropped
  turns T06 red (the check is guarded).
- **A listing returning an item that breaks a rule, an id twice, or leaving an item out silently:** no item is left
  out silently (every item that fails ends the listing with `MalformedItem`, page and item; the walk yields a page
  before the next is requested, so a refusal on page 1 sends 1 request: T07/T08 assert it). Duplicates: refused
  ordinally (T07/T08, mDuplicateKept); an id differing only by a trailing line feed is a second id (F1).
- **A files folder without both ids in the drive rule:** no, but for the trailing line feed (F1). The facet must be an
  object (mFolderFacetUnchecked), the id and drive id each pass `IsDriveSegment` (gFolderIdUnchecked, mDriveIdUnchecked).
- **A Graph-layer failure wrapped or swallowed:** no. The module catches only `JsonException` and
  `InvalidOperationException` inside its two readers (parsing an answer the layer already returned); `GraphCallException`
  passes untouched (T10: HttpStatus, PagingForeignAddress, MalformedResponse; T11 PagingTooManyPages; by reading no
  other try in the file).
- **A fake answer asserting a Microsoft behaviour as fact:** none found. `FakeTeamsGraph`'s summary: "Every Graph
  answer it gives is an ASSUMPTION of the test that scripts it"; every comment about Graph cites Microsoft's page by
  title or says UNMEASURED; README `## Limits` names R10, R11, R12 and "Built and tested against a FAKE Graph only".
- **Any message or `ToString` carrying a value:** no. `TeamsBrowseException` is built only from kind, page and item
  (the constructor takes nothing else); the two `ArgumentException`s carry fixed text and the parameter name; the three
  `ToString` overrides print lengths (T12, and gTeamEntryLeaks / gChannelEntryLeaks / gFolderLeaks each turn T12 red).
- **The lock files against BASE's (check 4; Tuesday's point b):** only what the one `ProjectReference` needs. Source
  lock: `net10.0` gains `datasec.suite.graph` and `datasec.suite.logging` (Project) and `Serilog` 4.4.0 /
  `Serilog.Sinks.File` 7.0.0 (CentralTransitive, the hashes BASE's other lock files carry); its sha256 `6466b1a2...` equals
  the landed OneDrive source lock byte for byte (both reference Graph alone). Test lock: the same four entries plus
  `datasec.suite.teams` gaining its dependency on Graph; sha256 `59f8b44c...`. No package added, no version changed,
  the rid sections untouched; the locked restore passed locally and on both hosted legs (`NU1004` 0 lines each).
- **The hosted run on both legs:** the gate's `hosted3.py b6b53100 ... --total 2611 --rules 790 --skipped-linux 4
  --skipped-windows 21 --unit 117 --floor 117 --hardened-scan --guard-linux 28 --guard-windows 29`: `HOSTED
  b6b531000b61a724ed0ca67631227e1e7292771f: PASS` (run 46042311709: linux succeeded 2607, windows 2590, skipped 4 / 21;
  rules 790, floor 117; secret-scan every control); control `--total 2612` FAIL 4. The Teams test dll `passed` on linux
  (515 ms) and windows (898 ms); `failed Datasec.` / `NU1004` 0 lines on either leg (case-blind; control `Datasec.`
  223 and 257 lines).
- **`words.py` and gitleaks over the added lines and the message:** `words.py --control` `CONTROL FIRED: 13 of 13`;
  over `added.txt` and `commit-message.txt` `WORDS: clean (2 files)`; B-numbers 0 and 0 (control: the kit 25). gitleaks
  8.30.1: control FIRST (a token-shaped text built from two halves and random characters, never printed) rc 1, moved to
  `g2208/_quarantine/`; the 11 head blobs, the message, `added.txt` and `added-locks.txt` under neutral names (14 files)
  rc 0; `gitleaks git` over `7ca5e4ce..b6b53100` rc 0; `src/Datasec.Suite.Teams` rc 0.
- **CodeQL:** the pull request's own run (kit FACTS 7); main 7ca5e4ce: csharp, python, actions results 0; open alerts 0
  (04:55:12).
- Also: `repo_rules.py` on the head worktree `RULES: clean (790 files)` (no --source-documents; `test ! -e
  1_Project_Definition` rc 0); `build/tests` `Ran 117 tests` OK.

## TUESDAY'S POINTS
(a) The id rules through `Uri` and the request builder: the bold answer and F1-F3 (every shape's printed URI or "NOT
SENT" in `evidence-probes.txt`). (b) The lock files: the gate list item above.

## ADVERSARIAL: three shapes outside each property (each covered, measured or a named limit)
- P1 (no request for a refused id; one resource): a trailing line feed (F1, measured); `+` / `0x` in a team id (F2,
  measured); trailing dots and only-dots (F3, measured; server side a named limit).
- P2 (the three forms): an upper-case team id is sent as written (T03 row 2); the select is pinned (gSelectWidened);
  a next link on the origin with another path is followed (R11, named limit, by reading `OnBaseOrigin`).
- P3 (listing): an id differing only by a line feed counts as new (F1); a non-object item on the channel listing is
  refused by the same reader as the teams' (T07 `notobject`; no channel row: by reading the shared `ReadEntry`); an
  invalid string the JSON reader will not decode is refused (by reading: `InvalidOperationException` -> null).
- P4 (folder): a line feed in either id is returned (F1); an id `...` is returned (`IsDriveSegment` takes it; probe);
  a folder facet `{}` with a `file` facet beside it is accepted (by reading: only the folder facet is checked).
- P5 (layer failures): unwrapped by reading (no catch of `GraphCallException`, no `catch (Exception)`); T10/T11.
- P6 (texts): the exception constructor takes no value; `ArgumentException` texts fixed; T12 plus three gate mutants.
- P7 (landed cells): whole solution 2611 / failed 0 locally and on both legs; lane L0's three files unchanged.
- State and concurrency: `TeamsBrowser` holds two readonly fields (the Graph client and the page bound); no static
  state but the two generated regexes; no cache (D6).

## NOT RUN
Local CodeQL (kit FACTS 7). Any probe on Windows (F3: DERIVED only). Any tenant, Graph host or server between (R10,
R12, and the server-side treatment of `%0A` and trailing dots: UNMEASURED). The seat's lock-folder moves and
predictions file (not this gate's points).

## MAIN AT THE END
`7ca5e4cefb315f57f4490ce245e1fb762dbf9f6d` (PR 65), one parent, tree `e8085394`; open pull requests 0; code scanning
open alerts 0; branch `b2199/x102-teams-slice1` = `b6b531000b61a724ed0ca67631227e1e7292771f` (gh api GET 04:59:32
AEDT). Main did NOT move during this gate: the squash tree is the head's tree `12930aa2`, 790 files, whole solution
`total: 2611`, `failed: 0`, `succeeded: 2607`, `skipped: 4`, `RULES: clean (790 files)` (all measured above). Push run
of main: `HOSTED 7ca5e4ce...: PASS` at 2564 / 782 / 28 / 29. If B2207 or B2209 lands first, landing.txt MAIN MOVES (B)
applies (expected file overlap with either: none; X100's two files and X101's 16 are outside both Teams folders).

## LANDING
`landing.txt` (steps, totals 2611 / 2607 / 2590 / 790 / 28 / 29 on 7ca5e4ce, MAIN MOVES), `pr-title.txt` (188
characters), `pr-body.md`, `squash-subject.txt` (230 characters with the placeholder; `SQUASH-SCAN: clean` with #66:
control rc 1 found 2, message rc 0; words clean over subject, body and title, `WORDS: clean (3 files)`; pr-body.md
counts only the required "coordinator", "reviewed head" and the attribution line's emoji: it is not committed),
`squash-body.txt`, `FOR-RECORDS.md`. Evidence: `evidence-probes.txt`, `evidence-probe-source.cs.txt`,
`evidence-mutants.txt`, `evidence-gate-mutant-rows.json`, `evidence-hosted.txt`. Recommendation: land as GO WITH
FINDINGS; F1 (and F3's trailing-dot refusal) are two regex lines and two cell rows, best taken as the first lines of
Teams slice 2, which is the first slice to SEND the drive and item ids; F7 to the OneDrive lane.
