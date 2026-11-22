Follow-ups of the identity service's card store (WP1.4, pull request 27). One commit, `a56ed63b`, on `394fa997`.
Seven existing files change, all under `src/Datasec.Suite.Identity/` and `tests/Datasec.Suite.Identity.Tests/`. No
file is added, and no public member, package, project, lock, solution or workflow file changes.

## Why

- A blob maker that threw a cancellation of its own (`OperationCanceledException` or `TaskCanceledException`) left the
  store untyped: the two catches around the maker let every cancellation pass, although the maker is never handed the
  caller's token, so none it throws can be the caller's.
- A name held twice outside the attribute set was read last-wins (`JsonElement.TryGetProperty` answers the last of
  duplicate names): a user object with `mail` or `id` twice, the set twice or the page's `value` twice was read by its
  last copy, while the README said answers are read strictly.

## What changed

- `CsaStore.PrefixOf` and `BlobOf`: `catch (Exception)`, so anything the maker throws, a cancellation included, is
  `CodecFailed` (`CsaStore.cs:288`, `:305`). The class comment says so.
- `CsaStore.GetJsonAsync`: right after the one parse (`CsaStore.cs:242`), `CsaReading.HoldsANameTwice` (`CsaReading.cs:155`)
  walks every object and array of the answer and refuses one in which any object holds a name twice, names compared
  ordinally after their escapes are read: `MalformedAnswer` before anything of it is read (`CsaStore.cs:243`). The
  set's own repeated-name check is removed (the walk holds that rule).
- README: two sentences, each with `file:line`.
- Cells `F12` (6 rows), `F13` (9), `R07` (4), `K06` (3), `E11` (2): 24 cases.

## What proves it

- Red first (macOS arm64): the 24 cases alone at `394fa997`: 1783 total, 24 failed, all Identity, each by its own
  `Assert.IsType` (6 naming the escaped cancellation, 18 because the call answered). Green with the fix: 1783 / 0.
- 44 mutants, each red on exactly its cells (the old filter back on either catch; the walk not run, not entering
  property values, not entering arrays, or comparing names ignoring case; and lane A2's kept rows).
- C# totals 1783 on both legs (1759 + 24), skipped 4 on linux and 21 on windows, RULES 551 files, 111 unit tests with
  floor 111 (push run 45045417543, four jobs success). Merged locally with lane F3's head `6177b525`: 1785 / 0, RULES
  553.

## Still open

- A name written with an invalid escape (a lone UTF-16 surrogate) anywhere in an answer now ends the call in an
  untyped `InvalidOperationException` from the walk; for a name inside the set, or such an escape in a value the store
  reads, that was already so before this change. Nothing is chosen or written. Whether Graph ever sends one is not
  measured. A one-line fix (catch it beside `JsonException`) and a cell are sketched for the records pass.
- A repeated name in a part the store never reads (another set, `@odata.count`) also fails the call; whether Graph
  ever sends a repeated name is not measured (the integration run against a test tenant).
- A caller that cancelled while the maker throws a cancellation of its own gets `CodecFailed`, not its cancellation.

## Who decides

The coordinator chose, as coordinator, this round's cut and every choice inside it: every exception of the blob maker
is `CodecFailed`, a repeated name anywhere refuses the whole answer, the set's own check folded into the walk, and the
named costs above. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
