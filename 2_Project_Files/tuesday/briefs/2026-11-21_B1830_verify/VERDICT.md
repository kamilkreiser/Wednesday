GATE B1830: GO WITH FINDINGS @ 48120e5 on main ddbdf80

Gate G1 Tier 1 (Opus 5.5, in-session), round 1 of 2, of OXPd 2 WP0.4 (cut): HP's 37 specification inputs with a
fingerprint list, the generated OXPd 2 clients and callback models with a bounded parser, and a gateway test stub. Head
`48120e5889599baccce88bc2a782df720c1f2e8c` on `b1829/wp04-oxpd2-clients`, one commit, parent main
`ddbdf8009d0df77d084ef4834bb78d7c4a80b5b0`; main has since moved to `bb91433481718652bf808884fb56a7ffa2754386`.
Measured 2026-11-21 15:53 to 16:20 AEDT (clocks by `date`). Read clone `/private/tmp/b1830-gate/clone` (push URL
`invalid://no-push`, no identity); every git verb that writes objects, every build and every mutant ran in clones of it
inside the session scratchpad (`.../scratchpad/b1830/{head,merged,mut}`), because the workspace hook refuses write verbs
elsewhere. Every dotnet job went through ONE runner (the kit's `heavy.py`, copied unchanged, sha256 equal): load read
first, the wave's lock taken by `mkdir` of exactly `<project>/.tools/wave1-heavy.lock.d` with `owner.txt`, one command
under a time bound, the lock MOVED into `/private/tmp/b1830-gate/_quarantine/locks/`; closed local proxy (127.0.0.1:9);
restores with `-p:NuGetAudit=false` because the closed proxy refuses the SDK's audit request (proved: the same locked
restore without it printed `error NU1900` 11 times, rc 1). Lock waits 0 on every job; load1 0.4 to 3.8. Programs under
`/private/tmp/b1830-gate/scratch/` and `/private/tmp/b1830-gate/probe/`, logs under `/private/tmp/b1830-gate/logs/`.

**BLUF.** GO WITH FINDINGS: no Blocker, no Major; three Minor code or test findings, one Minor process finding, and
records. Scope is exactly the lane's property; the 37 inputs are byte-equal to HP's files and are the only copies of
supplied bytes; my own adversarial inputs (535,843 parser inputs plus 3,316 client calls) produced only values and typed
refusals, never another exception, never a stack fault, never a read past the limit, never a refusal text holding a byte
of the input; my independent reading of HP's five target specifications agreed with the generated parser on all 4,274
targeted cases; my own regeneration equals the committed `Generated/` byte for byte and as a set; the merge with the
moved main is CLEAN and the merged tree builds and passes 894 of 894 run (890 passed, 4 skipped). **In plain words: yes,
the branch can be landed, but because main moved after it was built, its pull request's checks must first run against
the current main (and be proved to have built that merge) and the code scan, which has never run on this code, must be
green; then squash by `landing.txt`, as long as main is still bb914334.**

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor | Public `IReadOnlyList` members hand out their backing arrays: `Oxpd2Schema.Properties` (`Oxpd2Property[]`), `Oxpd2Schema.EnumValues` (`string[]`), `Oxpd2InboundCatalogue.Operations` (`Oxpd2InboundOperation[]`), `Oxpd2InboundOperation.RequestContentTypes` (`string[]`); each reads `is <array>: True`. Any code in the process can cast and write, and every later parse changes: on `UsbAccessories POST /operationCallback`, body `{}` read `MissingRequired` before, `Malformed` after a write that cleared `Required`, also through the catalogue (`logs/probe-run4.log`, section F). The serializer pass still refused, so no weaker ACCEPT was shown; C8's letter holds (0 static fields that are not readonly, by reflection; the options are read-only: `Converters.Clear` and the resolver's `Modifiers.Add` both refused). Not reachable from network bytes. | Emit `System.Array.AsReadOnly(...)` (or a `ReadOnlyCollection`) for the four members; add a reflection cell that no public member's value is an array. Follow-up, not a reason to hold the merge. |
| F2 | Minor | `Oxpd2ClientCore.ReadBoundedAsync` computes `limit + 1` in `int`: a client built with `new Oxpd2ParseLimits(int.MaxValue, 32)` (the constructor accepts it) throws `OverflowException: Arithmetic operation resulted in an overflow.` out of the client method on a 200 answer of `{}` (`int.MaxValue - 1` works). The kit's N14 says no exception but `ArgumentException`/`OperationCanceledException` leaves a client method. Caller configuration only, not network input. | Compute the first buffer size and the growth in `long`, or bound `maxBodyBytes` in the limits constructor (for example at most `Array.MaxLength - 1`); add the edge to N14. Follow-up. |
| F3 | Minor | A stated behaviour has no cell: `MinLength`/`MaxLength` are documented as counted in Unicode scalar values (the runtime's `LengthCheck` skips low surrogates). My mutant m8 (count every UTF-16 unit) SURVIVES the builder's suite (826 of 826 pass) and is killed by my own cases (40 differences: `maxLength` astral characters refused as `OutOfRange`). | Add to N9 a string of exactly `maxLength` astral characters (value) and one more (refused). Follow-up. |
| F4 | Minor (process) | The kit's Step 3(e)(i) R5 run (`repo_rules.py --source-documents <project>/1_Project_Definition/Source_Documents`) walks and hashes the whole supplied folder, including the SDK's `tools/certificates/` that holds HP's development root CA private key: the builder's run hashed 35223 files; mine, with every `tools/certificates` folder pruned before descent (2 folders, contents never listed), hashed 35215, so 8 files there were opened and hashed by the builder's run (DERIVED by subtraction). Nothing was printed or copied; the kit ordered the run; it contradicts the kit's own line "never open, list, copy or hash anything under the SDK's `tools/certificates/`". | Future kits that run the R5 hash half over `Source_Documents/` prune `tools/certificates` (the gate's wrapper `scratch/item1.py` does it with the repository's code unchanged), or the R5 follow-up excludes it. For the records. |
| F5 | Records (design point) | Q6 refuses an enum value the inputs do not list, and D9 refuses a JSON null for an optional property. Code is right as stated, but on the inbound callbacks a firmware that adds one enum value (42 enum sites in `jobStatistics` alone by the builder's site table; my own reading reached 36 enum sites across the 10 operations) or sends a null makes the WHOLE callback refused. What the printer then does (retry, drop) is UNMEASURED. | For WP1.2 before callbacks are wired: per-site tolerant reading (an unknown marker) or a regeneration discipline on each beta; put it on the master list. |
| F6 | Records | N11 (strict `anyOf [ $ref, {} ]`) has no effect on any parsed path today: the 1014 sites are 4xx/5xx bodies, which the clients do not parse (status only), and the inbound surface has 0. A body stream that throws `IOException` mid-read leaves a client method as `IOException` (the STATUS names only `HttpRequestException` as passing through). | Say both in the records; N15 gains the `IOException` line. |
| F7 | Records | The device-answer models carry HP's credential-shaped fields (for example `BearerAuthorizationTokenValue`, 72 occurrences of the family in `Generated/`; a `GetFunctionsSolutionTokenAsync` client method for HP's own operation). No client sends a credential (0 requests with `Authorization` over 3,316 calls; 0 header uses in `Generated/`), but when a later lane logs or stores these models the logging deny-list must cover them. | A records line for the lanes that consume the clients (WP1.2, logging). |

No finding blocks the merge. Graded against the commission's GRADE: items 1 to 5 hold, no text is false; the only
findings are Minor, records or text.

## Item 1: scope (`scratch/item1.py`, `logs/item1.log`: ITEM1 PASS, every control fired)

| Check | Read | Control |
|---|---|---|
| refs (GET 15:53:54 and 16:14:54) | branch `48120e58`; main `bb914334` (pull request 5 merged 04:51:30Z, parent ddbdf800); open pull requests 0; `.private` true, `.permissions.push` true | |
| commit | one commit beyond ddbdf800, parents `48120e58 ddbdf800`; message = the kit's subject plus the one attribution line | |
| paths by property | 141 changed: 140 `A` all under `contracts/oxpd2/`, `src/Datasec.Suite.Adapters.Oxpd2/` (project file, lock file, `Generated/`) and `tests/Datasec.Suite.Contracts.Tests/`; 1 `M` = `Datasec.Suite.slnx`; no forbidden file (`Directory.Packages.props`, `ci.yml`, `build/**`, `.github/**`, `README.md`, `global.json`, `Directory.Build.props`); no existing lock file changed; `Generated/` holds only `.cs` and `.gitattributes` | the property refuses `src/Datasec.Suite.Adapters.Oxpd2/Adapter.cs` and `build/x`: FIRED |
| solution file | numstat 2 0; the two added lines are exactly the `place.py` lines; both Folder blocks in ordinal order | |
| frozen blocks | cut by program from the stamped kit: S 3587 B, T2 141 B, T3 569 B, T4 8 B, each sha256 = FACT 7; T2, T3 and both T4 files byte-equal | T2 file against T3 block: unequal, FIRED |
| the 37 | `inputs.sha256` 37 lines, sha256 `6760314d9fd8c56bf7ce6b815deb5c26adc78f1098878b06616c4315b5013d7e`; set-equal to the files under `contracts/oxpd2/hp/`; 37 of 37 committed files byte-equal to their source under `<spec>` (my read, paths from the list only); 37 of 37 list hashes equal; Block S bytes and hash prefixes equal | |
| R5 (the repository's code, run unchanged through a wrapper that prunes `tools/certificates`) | supplied folder: `RULES-NOTE: R5 hashed 35215 files`, exactly 37 lines `RULES: R5 contracts/oxpd2/hp/<path>:0`, set-equal to the list, nothing else, rc 1; empty folder: `RULES: clean (253 files)` rc 0; no folder (the hosted form): `RULES: clean (253 files)` rc 0 | a folder holding one copy of `Datasec.Suite.slnx`: `RULES: R5 Datasec.Suite.slnx:0`, FIRED |
| bytes | no key, certificate or binary path; no NUL byte; no PEM block; outside `hp/` every added file ASCII with no tab or CR; no 64-hex value outside `inputs.sha256` | the 64-hex and PEM patterns fire on planted text |

## Item 2: the parser of network input (the G1 core)

**Read.** The runtime is emitted verbatim from `contracts/oxpd2/generator/Oxpd2RuntimeText.cs` (my regeneration
equals the committed files, item 3); I read its parser, limits, refusal, schema, client core and query builder text
whole. `Oxpd2Json.TryParse` (runtime text lines 372 to 407): after the three null checks the FIRST statement is
`if (body.Length > limits.MaxBodyBytes)` returning `TooLarge "$"`; then a BOM check, `Utf8.IsValid`, ONE
`Utf8JsonReader` pass with `MaxDepth = limits.MaxDepth + 1` driven by a schema walker (recursion only along the
schema, whose depth is at most 9; unknown values skipped by an explicit stack, duplicate keys refused at every level),
trailing data refused, then `JsonSerializer.Deserialize` with read-only options (duplicates, comments and trailing
commas off, strict numbers, unmapped members skipped); `JsonException` and `InvalidOperationException` become
`Malformed "$"`. A refusal's text is `"Oxpd2Refusal " + Kind + " at " + Path` and the path is built from the schema's
property names and indexes only.

**Is `MaxBodyBytes` checked on the span length before any JSON read: YES**, by the code above and by three measurements:
a body of `MaxBodyBytes + 1` that is ALSO a BOM followed by invalid UTF-8 is refused `TooLarge`, not `Malformed`, on
all 10 operations (so neither check ran first); 64 MiB of `[` and of spaces return `TooLarge` (slowest input of the
whole run 14.9 ms); my mutant mSize (check removed) turns the builder's N1 red by assertion.

**My own inputs** (`scratch/specgen.py` reads HP's five target files with my own resolver, NOT the builder's
generator; `probe/Program.cs` runs them against the built adapter; seed 8302026; `logs/probe-run2.log`):

| Set | Inputs | Result |
|---|---|---|
| A. targeted rows from my reading of the spec, every N1 to N11 row at every site my full payload reaches, on all 10 inbound JSON operations | 4,274 | 0 differing from the kit's Q6 rules; outcomes value 493, WrongType 1981, DuplicateKey 510, MissingRequired 430, OutOfRange 430, Malformed 358, UnknownEnumValue 72; every refusal path equal to the predicted one. My full payloads reach a SUBSET of the sites (for example 36 enum sites against the builder's 46: optional branches my resolver does not enter), so this set complements the builder's site-by-site rows rather than replacing them |
| B. size and depth (N1, N2) per operation | 170 | exactly `MaxBodyBytes` value; +1 `TooLarge`; 64 MiB spaces and `[` `TooLarge`; depth 32 value, 33 `TooDeep`; 100000 nested arrays and 100000 nested objects in an unknown property `TooDeep`; 100000 unclosed `[` `TooDeep`; with limits (1 MiB, 4096): depth 4096 value through the serializer pass too, 4097 `TooDeep`; with (int.MaxValue, 4096): 64 MiB of `[` after a valid prefix `TooDeep`; no stack fault |
| C. my fuzz, all 10 operations in parallel (also a concurrency check of the shared schemas) | 360,000 (36,000 per operation: random bytes 0 to 4096, JSON-alphabet noise, 1 to 8 byte edits of my minimal and full payloads, structural mutations: type swaps, Int64 edges, `1e3`, `-0`, `1E400`, 3000-character strings, astral text, 20 to 70 deep arrays, removed and duplicated keys, sentinel keys, arrays grown by up to 400 items) | 0 exceptions; outcomes value 78622, Malformed 134698, MissingRequired 54300, WrongType 49003, DuplicateKey 30485, OutOfRange 10460, UnknownEnumValue 1758, TooDeep 669, TooLarge 5; every refusal text of the exact form, path grammar held, every path name a property name of my reading, no sentinel in any text |
| D. outbound sample: 57 of the 1,131 device-answer models (every 20th) through the same parser | 171,399 | 0 exceptions; the seven fixed rows as expected on all 57 |
| E. clients: hostile path values (`../x`, `a/b`, `%2F`, space, `?x=1`, `#`, `..%2F`, `%2e%2e`, backslash, CR LF header text, NUL, `e` acute, an absolute URL, `//host`, `~`, 10000 characters) on every path parameter of all 201 methods; empty, `.`, `..`, null; hostile required query values; N14 answers (an endless body, a lying `Content-Length` of 10, a declared 5 GiB, 204, a duplicate key) | 3,172 + 144 | path: same host, same segment count, query and fragment unchanged, the value one escaped segment; empty, `.` and `..`: `ArgumentException` naming the parameter only; null: `ArgumentNullException`; 32 query values escaped into the query with the same pair count; endless and lying bodies refused `TooLarge` with at most limit + 1 bytes read; 0 requests with `Authorization`; one host requested, `device.example.test` (my fake handler). F2 and the `IOException` line of F6 are the only exceptions seen, both outside network bytes or named |

Per row, what the parser gives: `-0` reads as 0 then the bounds apply (value where 0 is in range); `1e3`, `1.5`,
`1.0`, `1E0`, `9223372036854775808`, `-9223372036854775809` and a 401-digit number are `WrongType`; Int64.MinValue and
MaxValue are values where unbounded; the BOM is `Malformed` by an explicit check; a lone surrogate escape is
`Malformed` in a known string, an unknown string and an unknown KEY; overlong UTF-8 and UTF-8-encoded surrogates are
`Malformed`; keys differing only by case are not duplicates; `"qqk"` and `"qqk"` are duplicates.

**Limits settable from outside:** only by constructing `Oxpd2ParseLimits(maxBodyBytes >= 1, 1 <= maxDepth <= 4096)` and
passing it per call or per client; the default is a get-only static of an immutable class; no writable static (C8);
F1 is the one shared state a cast can change. **D3 (the leak check as rebuilt): ACCEPTED.** My independent check over
364,274 inbound inputs is stricter than the literal one (exact text form, every path name from the schema) and found 0.
**D9: ACCEPTED as a choice** (the schemas hold no `nullable`); compatibility in F5. **N11: ACCEPTED**, moot today (F6).
**Q6 (unknown enum values refused) on the inbound callbacks:** safe as code (no value of an unlisted member is
built); a product risk on firmware drift (F5), for FOR TUESDAY, not a blocker.

## Item 3: the generator and the generated code

- My own regeneration (`/private/tmp/b1830-gate/regen`, the three generator files compiled by an absolute include,
  no package): 85 files, 3,761,642 bytes; equal to the committed `Generated/` (minus its `.gitattributes`) as a set and
  byte for byte (`scratch/item3.py`, `logs/item3a.log`); control: one byte changed is detected.
- Determinism: a second run from ANOTHER path (the merged clone), under `LANG`/`LC_ALL` `tr_TR.UTF-8` and
  `TZ=Pacific/Kiritimati`, equal to the first; the output holds 0 CR, 0 tab, 0 non-ASCII bytes, 0 `/Users/`,
  `/Volumes/`, `/private/`, drive paths, dates, `Environment.`, `AppContext`; the generator sorts with
  `string.CompareOrdinal` everywhere and upper-cases with `ToUpperInvariant`.
- Counts by reflection over the built assembly: 16 clients, 201 public async methods (Application 30, Authentication
  8, Copy 13, Device 10, DeviceUsage 4, JobStatistics 6, PrintJob 3, ScanJob 15, SdkSupport 20, Security 4,
  SolutionDiagnostics 5, SolutionManager 36, Supplies 6, UsbAccessories 23, UserPolicy 15, WebHook 3); 12 inbound
  operations, 10 with a JSON body; the catalogue's 10 keys equal my reading's 10.
- No `description`, `summary` or `title` text of HP's (3,611 strings; 3,576 of 25 or more characters) appears verbatim;
  the 22 that share a 40-character window with `Generated/` share it through operation paths, wire values and type
  names only (all 22 printed in `logs/desc.log`); control fires.
- C6: 0 public parameters named token, accessToken, authorization, bearer, credential, password, secret or apikey;
  header use in `Generated/`: `Headers.Authorization` 0, `"Authorization"` 0, `AuthenticationHeaderValue` 0,
  `DefaultRequestHeaders` 0; the words `Retry`, `Refresh` and `Bearer` (628, 20, 296) are HP's names only
  (`BasicServerRetryBehavior...`, `ApplicationAgentRefresh`, `BearerAuthorization...`); loops exist only in the runtime.
  D4's explanation holds.
- N13 and D10: escaping proved in item 2 E; dot segments: `.` and `..` are left unescaped by `Uri.EscapeDataString`
  and would be removed by URI normalisation, so refusing them is right.
- C8: the adapter references System.Collections, System.Memory, System.Net.Http, System.Net.Primitives,
  System.Runtime, System.Text.Json only (0 ASP.NET Core, Identity, logging or Serilog); its project file is T2 (no
  package, no project reference).
- **Size as a review risk:** `Generated/` is 86 files, 3,761,650 bytes, 60,557 lines (1,234 models, 186 enums, 16
  clients). I read the runtime text whole, the catalogue and one schema file; I did NOT read the models, enums and
  clients line by line, nor the generator's `Oxpd2Unit.cs` and `Oxpd2Generator.cs` line by line. The trust in them
  rests on the regeneration equality, the reflection counts, the scans above and above all on 4,274 rows of my
  independent spec reading that the generated inbound models judged exactly as predicted. A hand review of 60k
  generated lines is not possible; a later change to the generator is reviewable, a change to `Generated/` alone is
  caught by the regeneration test.

## Item 4: the gateway stub (read; not probed by a program of mine)

`tests/Datasec.Suite.Contracts.Tests/GatewayStub.cs` (test project only): Kestrel `Listen(IPAddress.Loopback, 0)`;
`GET /api/healthcheck` text `Healthy!`; `POST /api/negotiate` JSON `url` (the stub's own `/printerhub`) and
`accessToken` `synthetic-access-0001`; `POST /api/send` sends ONE hub message to `Clients.All` with method = the body's
`realm` and the one argument = the whole body, 200 with no body; not JSON, or no non-empty `realm`: 500 with `error`;
hub mapped at `/printerhub`; the `Authorization` header recorded, never checked (named limit, A9 line 51, RELAYED). Every
test `HttpClient` of the stub tests uses `SocketsHttpHandler { UseProxy = false }`, the hub client sets
`Options.Proxy = null`. URL literals in the test project: `http://device.example.test/service/` (the client tests' base
address over a fake `HttpMessageHandler`, never a socket) and `ws://` built from the stub's own loopback address; no
other host. Values synthetic (`synthetic-secret-0001`, `user0001@example.test`, `printer-0001`).

## Item 5: build, suite, merge, hosted

- Head, through the runner: locked restore with `CI=true` rc 0 (the restore fetched nothing: the proxy is closed, so a
  fetch would fail; the project cache holds 64 entries before and after; `git status --porcelain` 0 lines); build
  `0 Warning(s)`, `0 Error(s)`; test `Test run summary: Passed!`, `total: 826`, `failed: 0`, `succeeded: 826`,
  `skipped: 0` (`logs/head-test.log`).
- **The merge with the moved main:** `git merge-tree --write-tree bb914334 48120e58` rc 0, CLEAN, tree
  `da108e115460495ae1db5e5800a51864ed080c02`; the only path both sides changed is `Datasec.Suite.slnx`, whose lines sit
  in different places (the store's `Secrets` lines and this lane's `Adapters.Oxpd2` / `Contracts.Tests` lines); merged
  file 19 lines, 13 project lines in ordinal order, sha256 `765755d67948466e594c545afcb69950d6d980581711c2f732967826de7c8f2a`;
  merged tree 291 entries = prediction (main's 151 with the head's 140 added paths and that file), 0 differing. The
  merged tree in its own clone: locked restore rc 0; build 0 warnings, 0 errors; test total **894**, failed 0, succeeded
  890, skipped 4 (`logs/merged-test.log`); 894 = 762 (main bb914334, read in its hosted logs: total 762 on both legs) +
  132. The commission's 826 + 69 - 1 is the same number.
- Hosted run `44867697605` of the head, by GET (`hosted.py`, unchanged; `logs/hosted.out`): four check runs, `linux`,
  `windows`, `secret-scan`, `rules`, completed success, attempt 1, every step success; linux and windows each
  `total: 826` twice, `succeeded: 826`, `failed: 0`, `skipped: 0`, `0 Warning(s)`, `0 Error(s)`, `GUARD: clean (10
  files)` / `(11 files)`; secret-scan `PLANTED-CONTROL secret-scan: rc 1`, `PLANTED-CONTROL neutral-scan: planted in 11
  places, found by name 1, found under a neutral name 25 of 25, rc 1`, `NEUTRAL-SCAN: stored objects 592 (356 blob, 20
  commit, 216 tree), copies written 1184, objects of this commit not among them 0`, `no leaks found` 3 times; rules
  `Ran 53 tests`, `UNIT-TEST FLOOR: ran 53, floor 53`, `RULES: clean (253 files)`; the control line counts 0 in every
  log. **These runs built the head on the OLD main; the pull request's code scan has NOT run (0 analyses for the
  branch's ref).**

## Item 6: mutants (mine, in my own clone; `scratch/mutant.sh`, `logs/m*-test.log`)

Each made with the Edit tool on a generator source, regenerated by my regen console into the mutant clone, restored,
built (0 warnings, 0 errors every time), the whole suite run, then undone with the Edit tool (`git diff --quiet --
contracts/oxpd2/generator` rc 0 after each); after the last, regenerated once more and the suite run: total 826,
failed 0, and `git diff --quiet` of the whole tree rc 0.

| Mutant | Edit | Suite | Red by |
|---|---|---|---|
| mDup | options `AllowDuplicateProperties = true` (the walker reads it) | failed 11 (N5 10, N14 1) | assertion: "unknown key twice at the top: expected DuplicateKey, got a value" |
| mSize | the span-length check made dead | failed 10 (N1) | assertion: "MaxBodyBytes + 1: expected TooLarge, got a value" |
| mDepth | `DefaultMaxDepth = 4096` | failed 10 (N2) | assertion: "depth MaxDepth + 1: expected TooDeep, got a value" |
| mEnum | `HasEnumValue` always true | failed 5 (N3 4, N14 1) | assertion: "expected UnknownEnumValue, got Malformed" (the serializer still refuses; the kind tells) |
| mEsc | `Segment` returns the value unescaped | failed 1 (N13) | assertion: "the path holds more than one escaped segment for a hostile value" |
| mAuth | a Bearer header set in the shared JSON send path | failed 1 (C6) | assertion: `Assert.DoesNotContain() Failure` |
| m7 (mine) | the skip walk refuses duplicates only at its first level | failed 10 (N5 "three levels down") | assertion: "key twice three levels down: expected DuplicateKey, got a value"; also proves the serializer pass does NOT catch duplicates inside skipped values: the walker is the only guard there |
| m8 (mine) | string length counted in UTF-16 units | **0 failed: SURVIVES** | killed by my cases (40 differences): F3 |

## Item 7: the deviations

| # | Ruling | The line that proves it |
|---|---|---|
| D1 | ACCEPTED | the same locked restore without the switch: `error NU1900` 11 times, rc 1 (`logs/head-audit-control.log`); `ci.yml` lines 40 and 70 run `dotnet restore --locked-mode` without it, so the hosted audit is unchanged; known-vulnerability status NOT TESTED here |
| D2 | ACCEPTED (records) | the red run's stubs were restored by sha256; the head's suite and my regeneration are green and equal |
| D3 | ACCEPTED | item 2: 364,274 inbound inputs, every refusal text of the exact form with schema names only, 0 leaks |
| D4 | ACCEPTED | item 3: 0 header uses; `Authorization`, `Retry`, `Refresh`, `Bearer`, `File.` occur only in HP's names |
| D5 | ACCEPTED | the lock files' `linux-x64`/`win-x64` come from `RuntimeIdentifiers`; the project's word scan over every other added line: `WORDS: clean` |
| D6 | ACCEPTED | my count over the 37: `additionalProperties` false 206 of 206; query parameters: 201 of 201 one `parameters` object, form, explode |
| D7 | ACCEPTED | my probe classified path and query values by where a marker lands (independently): 32 query values, every path parameter of 201 methods escaped |
| D8 | ACCEPTED | the 5 s read window keeps C7 red by assertion (STATUS RED FIRST); the stub tests pass at the head |
| D9 | ACCEPTED as a choice; F5 | my cases: optional null `WrongType` at the property path on every site |
| D10 | ACCEPTED | `.` and `..` refused with `ArgumentException` naming the parameter (item 2 E) |
| D11 | ACCEPTED; records | empty classes and object-only `JsonElement` behave as stated in my cases; `TestSupport.cs:32` makes `oxpd2-contracts-*` folders under the system temp folder and nothing removes them (hygiene, records) |

## Item 8: texts (exported and scanned: `scratch/texts.py`, `logs/texts.log`)

`pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`, `landing.txt` in this folder. Each exported
through the workflow's own `neutral_export` (cut by program from the head's `ci.yml`, lines 120 to 128) as the commit
message of a scratch repository and scanned with the workflow's options (`--no-banner --redact --ignore-gitleaks-allow
--exit-code 1`): title, title and body, body, the squash message with a number, as written, the squash body, the
default squash shape and `landing.txt`: export rc 0, message stored whole, scan rc 0, `no leaks found`, 8 of 8; the
control (the squash message with a planted token built from parts) scan rc 1, `leaks found: 2`. The project's word
scan (`words.py`, control `CONTROL FIRED: 13 of 13`) over the title, the squash subject, the squash body without its
attribution line and the pull-request body without its footer: `WORDS: clean (4 files)`; the squash body whole:
`WORDS: clean (1 files)`. The texts say HP's files are kept on the owner's agreement and that every choice about the
code was made inside the build; none says he decided anything about the clients, the parser or the stub. `landing.txt`
is for Tuesday and is not committed (it names the branch and paths). `FOR-RECORDS.md` lists what a records pass files.

The lane's own words: the commit message and every added line outside `hp/` and the lock files (65,148 lines):
`words.py` `WORDS: clean (2 files)`; 0 bytes outside printable ASCII; "decided", "ruled", "ruling", "approved",
"instructed" 0; no sentence says a printer sends anything without the schema-and-synthetic wording (the one such
comment, `TestSupport.cs:61`, says "Every payload is SYNTHETIC: shaped by HP's schema ... none was seen on a printer").

## The builder's claims (STATUS), graded

True as measured: one commit, 141 files; the 37 copies and the list sha256; the references 3819 / 365 / 146 / 0
(asserted by its test, green in my run); `Generated/` 85 `.cs` 3,761,642 bytes, with `.gitattributes` 86 files
3,761,650 bytes, 60,557 lines; 16 clients, 201 methods, 12 inbound operations; total 826 = 694 + 132; build 0/0; R5
three ways (my supplied-folder count differs, 35215 against 35223, by the pruned certificates folders only: F4); the
hosted run and its lines; 0 Authorization; no package. Not shown by me: the red-first runs (the stubs are gone; my
mutants stand in for six of the controls).

## NOT RUN / NOT TESTED

Anything on Windows (the hosted `windows` leg is the only proof); `dotnet publish` and the release guard locally (the
hosted GUARD lines were read instead); `docker build`; CodeQL for C# (the extractor does not run on this arm64 machine;
the hosted code scan on the pull request is the only C# proof, and it has not run); known-vulnerability status of the
packages (audit off under the closed proxy); a program of mine against the gateway stub (read only; the builder's three
stub tests pass in my run); the 1,074 device-answer models outside my sample of 57 except through the builder's tests
and the regeneration; `pattern` and `format` (not checked by design); any real printer, simulator or gateway payload;
the R5 hash over `tools/certificates/` (pruned by me on purpose); the pull_request runs of the merge with bb914334 (they
do not exist yet).
