GATE B2107: GO WITH FINDINGS @ b740f54 on main 56f508a

Gate G1 (a changed refusal of a public API answer, a new lock in the quote store, a contract change), ROUND 1 OF 2 of
lane L1, one Opus reader (claude-opus-5-5), in-session, read-only. MPS Commercial Calculator, kit B2106 (seat M176;
stamp S5: Q1 195 out, Q3 the seat pushes and Tuesday lands, Q11 build the descriptions as Tuesday's reading of C-108,
the rest the defaults; every choice the coordinator's). Head `b740f5486e2058c1d899153e41fe492c2500edb8` on
`b2106/m176-mps-l1-233-316-120`, TWO commits (`f8644cce` contract, `b740f548` generated), on main
`56f508a779ea5add1655d1c8a824cde635d6a53c` (PR 228). Main and the branch did NOT move during the gate (gh api -X GET
06:01:24 and 06:20:15 AEDT; open pull requests 0 both times; open code-scanning alerts 0 both times). Read and measured
2026-11-26 06:01 to 06:21 AEDT in my scratch `fleet/state/s328/g2107/`: `clone` (clone_mps.py: the project's deploy key
in that one process, push URL `invalid://no-push`, no identity), local clones `frozen` (main + the frozen script),
`red` (main + E3), `head`, `mut-m2`, `mut-m3`, `sync` (at f8644cce), `probe` (the head + my `GateProbeTests.cs`, never
committed, never pushed). Toolchain: the project's `.tools/dotnet-10.0.404` (`dotnet --version` 10.0.404), node
v24.22.2 and npm 11.19.1 from Tuesday's `tools/node-v24.22.2-darwin-arm64/bin`. Heavy jobs (the whole Api project; the
npm ci + sync) one at a time under the project's `.tools/.heavy-lock-1`, each after two load reads 120 s apart (not
independent: 2.73/1.53 and 3.77/1.85), holder files moved to `g2107/logs/`, the slot dir removed; lock folders absent
at 06:20 (count 0). Filtered runs and the mutants ran outside the lock (light, by the kit's HEAVY list).

**BLUF.** The head is main plus the kit's frozen text byte for byte and the sync's own output byte for byte; the
refusal does what MPSCALC-233's ruling asks for a TYPED reference, and nothing a caller could not already read leaks;
the new lock cannot deadlock. Red first `Failed: 10, Passed: 136, Total: 146` (the kit's ten names); green `V0_`
`Passed: 146`; the whole Api test project `Passed: 3681, Failed: 0`; m2 red exactly N8 and m3 red exactly N6, both
hosts. No Blocker, no Major. Two Minor findings (F1 a pre-existing derived-reference shape that leaves 233's clause 1
NOT MET for long references; F2 the new version-rule section is silent that this very change does not follow it) and
five Info. None blocks landing; F1 blocks reading 233 clause 1 as MET in the records.

## 1. THE DIFF AGAINST THE FROZEN TEXT (MEASURED)
- `apply_edits_l1.py`, `mutate233.py`, `scans2106.py` extracted from the kit by program (3 python blocks; sha256
  6d9b7ef2..., 54f544ec..., cf55e8c9...), each `cmp`-equal to the seat's copy in `.tools/b2106-m176/scratch/`. The
  kit file and the seat's Step-0 copy share sha256 81345a78....
- Replayed on a clone at 56f508a7 (E3, then -E3): every assertion held; blobs after = QuoteStore.cs fb257452,
  QuoteEndpoints.cs 69d61e12, V0Duplicate.cs bfb9506f, openapi.json c41077c0, API.md cd6c5eab; non-ASCII line counts
  unchanged (3, 6, 2, 89, 125). Each EQUAL to the blob at f8644cce AND at b740f548 (`git rev-parse <sha>:<path>`).
- `git diff --name-status`: 56f508a7..f8644cce the five hand-edited paths only; f8644cce..b740f548 the three
  `web/src/api/generated/` paths only. compare API: ahead 2, behind 0, 8 files, the numstat of the kit (4/1, 3/3, 9/1,
  26/0, 110/1, 2/2, 3/3, 5/4). Head tree d63fa0c4 (735 files). Both commits: one parent each, author and committer the
  Datasec address (compare API).
- Commit 1's subject (109 characters) and body equal the kit's text byte for byte, plus one attribution line.
- **The generated files at commit 1 (MEASURED):** in clone `sync` at f8644cce: `npm ci --prefer-offline` rc 0 (273
  packages, 977 ms: served offline), `node scripts/sync-contract.mjs f8644cce...` rc 0, last line `contract f8644cce...
  blob c41077c00cd7c7abe8239f4775915b22743e95ae sha256 ea0768a164ce0fce116421c8e0b1921ee9c6b08329b0de28088a4ee873c70da2`;
  porcelain exactly the three files; blobs SOURCE.txt 2a1a6324, openapi.snapshot.json c41077c0, schema.ts 96be2214,
  each EQUAL to b740f548's; `npx vitest run src/api/contract.sync.test.ts src/api/contract.test.ts`: `Test Files  2
  passed (2)`, `Tests  4 passed (4)`.

## 2. THE RUNS (MEASURED, Debug, logs in `g2107/logs/`)
- Red first (`red` = main + E3 alone), `--filter "FullyQualifiedName~V0_"`: `Failed!  - Failed:    10, Passed:   136,
  Skipped:     0, Total:   146`; failed names exactly N1, N2, N3, N4, N8 on `QuoteApiTests` and `QuoteApiTestsUnderEntra`
  (10 `Failed MpsCalc` lines). How they fail: N8 x2 by `Assert.Equal() Failure`; N1 to N4 x2 (8) by
  `KeyNotFoundException` from `Code()` (`QuoteApiTests.cs:85`, `GetProperty("code")`) called inside
  `AssertRefTakenRefusal` (`QuoteApiTests.V0Duplicate.cs:171`) on the base's 201 body (F5).
- Green (`head`): `V0_` `Passed!  - Failed:     0, Passed:   146, Skipped:     0, Total:   146`; `V0_N` `Passed:    20,
  Total:    20`.
- Whole Api test project (`head`, heavy slot 1, 06:08:51 to 06:14:14): `Passed!  - Failed:     0, Passed:  3681,
  Skipped:     0, Total:  3681, Duration: 5 m 21 s`.
- Mutants (my own clones of the head, `mutate233.py`): m2 (`if (true)` for `lock (_refLock)`) `V0_N`: `Failed!  -
  Failed:     2, Passed:    18, Total:    20`, the two = N8 on both hosts; m3 (`OrdinalIgnoreCase`) the same line, the
  two = N6 on both hosts. m2 is a race: red in the one run I made (the seat: 5 of 5 red).
- NOT RUN by the gate: the Release build, the Engine and Import test projects, the whole `vitest`, `eslint`, `tsc -b`,
  `npm audit`, the production build and `check-bundle.mjs` (the seat's, MEASURED: 0 warnings, 743, 198, 149/1742, rc
  0 each); both Playwright steps, the python job and the package job (run by neither seat nor gate: hosted CI on the
  pull request is their first run; no python test reads any of the eight paths by my grep of tools/, infra/, scripts/;
  the package job publishes and scans the Api and the bundle, so it reads the changed C#); local CodeQL.

## 3. ATTACK
**The lock (no deadlock: DERIVED by reading, and a load probe).** `_refLock` is private (`QuoteStore.cs:130`) and taken
in one place (`:140`, `AddIfRefFree`), which is called from one place (`QuoteEndpoints.cs:563`; `git grep` of src and
tests: 4 lines, these). At that call the handler holds no lock: the source's lock is released at `:540` and the new
quote's lock is taken only after (`:569`). Inside, it holds at most ONE existing quote's lock at a time (`:144`, released
before the next) and then the new quote's lock inside `Add` (`:122`), a quote not yet in `_quotes` (`:126`), so no
other thread can hold it. No path takes a quote's lock and then waits on `_refLock`; the 18 `lock (x.Lock)` sites of
`QuoteEndpoints.cs` and 2 of `QuoteStore.cs` never call into `AddIfRefFree`. A cycle needs a holder of a quote lock to
wait on `_refLock`: there is none. Probe GP6 (per host: 6 sources, 8 rounds of typed clone + derived clone + GET + list
each, 192 requests at once, `WaitAsync(60 s)`): finished, exactly one holder of each typed reference.
**Its cost (F7, Info):** every typed clone takes the one store lock, snapshots `_quotes.Values` and takes each quote's
lock in turn, then writes the new quote through to the file store (`Save`) still under the store lock; typed clones
are serialised and wait on any quote whose lock is held for a write-through. O(n) per typed clone; derived clones,
create and edits do not take it.
**Paths that still store a clashing reference (F4, Info; the ruling covers the clone's typed reference):** create
(`QuoteEndpoints.cs:91`) and PATCH draft (`:212`) store a held reference (probe GP3, both hosts: 201 and 200); a
derived clone after a typed one stores a second holder (GP2: two quotes hold `Q-SYN-1-COPY`); the file-store restore
loads every quote as it is (`QuoteStore.cs:108-111`); no import path creates a quote (`store.Add` callers: `:91` and
`:563` only); new-version copies its own quote's reference. A typed reference held only by a draft that has since
changed it is free (GP7), by the current-version rule (Q7).
**Disclosure:** none beyond what the caller can read. Duplicate requires Seller, a quote reader; every quote reader
reads every quote's `quoteRef` (`Get` `:107`, `ToDto` `:1061`, not redacted). Probe GP4: the refusal body holds neither
the typed reference nor the holder's id, and no Location header. The refusal comes after 404, 403 and the value checks
(N7), so it adds no new existence oracle.
**The derived `-COPY` reference against typed ones (F1, Minor):** a typed one after a derived one is refused (N4); a
derived one after a typed one is not (GP2, by Q5). Not in the kit's cells: `CopyRef` (`:592-609`, unchanged) returns
the SOURCE'S OWN reference when that reference is 100 units and ends `-COPY` (GP1), which every clone of a clone of a
source whose reference is 96 to 100 units reaches (GP1b: 100 `B`, its clone `B`x95+`-COPY`, that clone's clone the
same) through the web Clone button. 233's clause 1 ("a draft whose quoteRef differs from the source") and the kept
docs sentence "A copy never shares its source's reference" (`docs/API.md:444`, `docs/api/openapi.json:369`) are false
for that shape. Pre-existing (not a regression; the lane's refusal is for typed references), so it does not block
landing; it blocks reading clause 1 as MET (the seat read it MET).
**Exactness:** an NFC and an NFD spelling of one word are two references (GP5); case, a trailing and a leading space
are different references (N6); both say "the same UTF-16 code units".
**The docs against the code.** `docs/API.md:444` and `openapi.json:369`: typed, current version, same UTF-16 code
units, no trimming or case folding, 400 `BAD_REQUEST`, nothing stored, derived not refused: each matches
`QuoteEndpoints.cs:543`, `:563-567` and `QuoteStore.cs:142-148` (the 400 is a documented response of the operation:
responses 201, 400, 401, 403, 404). `openapi.json:1036` says "A reference that another quote already holds is refused"
without "current version" or the code-unit rule (F6, Info). `:988` and `:1036` carry the agreed unit sentence;
`maxLength": 100` 8 at base and head. `docs/API.md:8` (120): the nine values MEASURED equal by `git log` of the
contract (36 commits; 18 at `0.9.0-b103`); F2 below. Commit 1's last body line "No word of any document or screen
changes." is loose (it changes two documents' sentences; it means no customer-facing word); the squash body says "No
word a customer reads changes" (F8, Info).

**Three shapes outside each property (each covered or a named limit):**
- Refused when typed and held: a held reference typed with a trailing space (N6: a different reference, 201), a
  reference held only by an older draft value (GP7: free), an NFD spelling of a held NFC one (GP5: free). Covered.
- Never refused when derived: a derived equal to a typed holder (GP2: stored, a second holder), a derived of a
  100-unit `-COPY` source (GP1: equals its source), a blank typed `"   "` (N5: derived, 201). Covered; GP1 is F1.
- One holder under concurrency: eight typed at once (N8: one 201, seven 400), typed beside derived, reads and lists
  (GP6: one per reference), typed beside create or PATCH of the same reference (NOT covered: create and PATCH take no
  store lock and do not refuse; a named limit, F4).
- No disclosure: the body (GP4), the Location header (GP4), the refusal's order against 404 (N7). Covered.
- No lock-order cycle: the only caller holds no lock (reading), nested quote locks (none inside `AddIfRefFree`), a
  mixed load of 192 requests (GP6). Covered.

## 4. SCANS
- SCANS-1 (the change): gitleaks 8.30.1, planted random `ghp_` canary rc 1 first; copies of the eight files at the head
  rc 0 (`no leaks found`, ~957 KB); both commit messages rc 0. `scans2106.py` (the kit's, base = `git archive` of
  56f508a7, head = clone `head`): `added lines: 162`, `non-ASCII lines: 2 | control planted U+200B: 3`, `Cf chars: 0 |
  control: 1`, `GUID lines: 0 | control: 1`, `name scan: names 12 | quiet 12 | control fired 12`, `tab chars in added
  lines: 0 | longest added line: 1524` (equal to the kit). Name scan of the kit (my `namescan.py`, the kit's 12 names,
  underscore-aware, 12 controls fired; plus B-number, seat-id and card-id shapes, 3 controls fired): the 12 names only on
  kit line 406 (the scan's own ban list); `Tuesday` on 41 kit lines (the coordinator's name in kit prose, none in the
  frozen edits, `mutate233.py` or the commit text); the card-id shape only `mps-l1-233-316-120` (the branch name). The
  frozen script, `mutate233.py` and both commit messages: quiet.
- SCANS-2 (the landing texts, with `#229` for `#PRNUM`): gitleaks control rc 1, then rc 0; the same name and id scan
  quiet on squash-subject (116 characters), squash-body, pr-title (197 characters) and pr-body (12 controls fired);
  non-ASCII: 0, 0, 0 and 1 (the attribution line's robot).

## FINDINGS (round 1 of 2; grade; blocks landing?)
- **F1 Minor, does not block landing (blocks reading 233 clause 1 as MET).** The derived `-COPY` cut returns the
  source's own reference for a 100-unit source ending `-COPY`, reached by any clone of a clone of a 96-to-100-unit
  reference (GP1, GP1b); clause 1 and the kept sentence "A copy never shares its source's reference" are false there.
  Pre-existing; a records line and a product choice (FOR-RECORDS (f)).
- **F2 Minor, does not block.** `## Contract version` states the minor-bump rule and is silent that 17 contract
  changes after `0.9.0-b103`, this one included, carry no bump, while `docs/API.md:153` records a bump with "no new
  member"; Q8 is the coordinator's. A records line (which changes the rule covers).
- **F3 Info.** The seat's RESIDUE: one `sed -i` on its own scratch file, one `rm -rf /dev/null` line, one
  `git -c user.name/user.email` commit in a never-pushed control clone; no project file or pushed commit touched.
- **F4 Info (out of the ruling's scope).** Create, PATCH draft, a derived clone after a typed one and a restart still
  store or load a reference another quote holds (GP2, GP3); typed-vs-create/PATCH races are uncovered. FACT 7(b).
- **F5 Info.** Red first of N1 to N4 is by an exception in the helper (`Code()` on a 201 body), not by an assertion
  message; the cause is the right one (201, not 400). A sharper helper would read the status first.
- **F6 Info.** `openapi.json:1036`'s refusal clause omits "current version" and the code-unit rule.
- **F7 Info.** The typed-clone scan is O(n) under one store lock, with the file write-through inside it.
- **F8 Info.** Commit 1's "No word of any document or screen changes." is loose; the squash body replaces it.
No finding is a Blocker or a Major; none needs a fix round before landing.

## LEFT BEHIND
Scratch only: `g2107/{clone,frozen,red,head,mut-m2,mut-m3,sync,probe,basetree,gl,logs,scratch,tmp,dotnet-home}`
(`.local/` folders made by the Api tests inside the clones: never opened; `sync/web/node_modules`). No pull request,
no push, no Jira, no message, no Azure, no hosted call; the project checkout and the seat's `.tools/b2106-m176` read
only. No background process of mine; no lock held. Not mine, reported only: pid 2177, a 4-day-old
`/private/tmp/b1839-gate/.../Datasec.Suite.Sessions.Tests` test host. Nothing deleted.
