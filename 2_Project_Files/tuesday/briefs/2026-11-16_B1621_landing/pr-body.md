Wording only. No code line, test row, package version, target or property changes.

**What changes**
- `scripts/tests/test_sdk_pin.py` docstring: a new SDK raises "the Pkcs or Xml pin" (it said the Pkcs pin only).
- `src/MpsCalc.Api/MpsCalc.Api.csproj` comment: the target `KeepPinnedXmlOutOfPackagePruning` exists only for the Xml pin, so the two are removed or changed together.
- The docstring now names two choices as accepted, with no change in strictness: the MSBuild reader flags a plain `dotnet msbuild` command in CI (wider than the routes it guards, and safe), and keys of `global.json` other than `sdk` are not read.

**Proof**
- The guard file's code, with the docstring dropped, is equal to main (AST compare); the project file's text outside XML comments is equal to main and the file still parses.
- `test_sdk_pin.py` 13 tests and `test_sdk_pin_routes.py` 51 tests pass, as on main.
- The two "accepted" sentences were checked by planting each case: a `dotnet msbuild` line in `ci.yml` gives exactly one problem naming msbuild; an extra `msbuild-sdks` key in `global.json` gives none.
- Not run locally: the restore, build, tests and package of the Api project (the machine cache lacks the pinned package). The hosted `dotnet` and `package` jobs are the proof for the project file.

Nothing is deployed by this change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
