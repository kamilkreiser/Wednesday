GATE B1846: GO WITH FINDINGS @ 9d49695 on main 5e36d8d

Gate G1 (Opus 5.5, in-session), round 2 of 2, a DELTA check of OXPd 2 lane C's fix round (kit B1834, seat X19): head
`9d49695512ab2f71135e2157c0ff54fe33144528` on `b1834/wp04-oxpd2-fix-f1-f3`, one commit, one parent main
`5e36d8dca42966395ea3dd014c7f788409eb585f`. Measured 2026-11-21 17:52 to 18:03 AEDT (clocks by `date`). Read clone
`/private/tmp/b1846-gate/clone` (made by kit B1834's `clone.py` in mode `draft`: push URL `invalid://no-push`, no
identity). Every git verb that writes objects, every build and the mutant ran in clones of it inside the session
scratchpad (`.../scratchpad/b1846/{head,mut}`, push URL `invalid://no-push`), because the workspace hook refuses
write verbs elsewhere. Every dotnet job went through ONE runner: kit B1834's `heavy.py`, copied unchanged, sha256
`31adedc8...` equal to the kit's table. It reads load first, takes the wave's lock by `mkdir` of exactly
`<project>/.tools/wave1-heavy.lock.d` with `owner.txt`, runs one command under a time bound, and MOVES the lock into
`/private/tmp/b1846-gate/_quarantine/locks/` (22 jobs, 22 moved folders). It uses a closed local proxy
(127.0.0.1:9), and restores carry `-p:NuGetAudit=false`, because the closed proxy refuses the SDK's audit request
(round 1 proved this: `error NU1900` without it). Lock waits were at most 7 (the lock was shared with seat X14 at
17:51), and load1 ran 3.0 to 6.7. Programs are in `/private/tmp/b1846-gate/{scratch,probe,regen}` and logs in
`/private/tmp/b1846-gate/logs/`. `Source_Documents/` was not read, listed or hashed, and `repo_rules.py
--source-documents` was not run.

**BLUF.** GO WITH FINDINGS: no Blocker, no Major, no Minor; four records points. The commit stays inside its scope.
My own regeneration equals the committed `Generated/` byte for byte and as a set. F1, F2 and F3 of round 1 are
CLOSED, each by my own independent run: F1 by a wider walk and 43,962 attempted writes, F2 at the measured
`Array.MaxLength`, F3 by re-running m8. On 536,128 of my own adversarial inputs, the head and the base adapter give
identical outcomes (one digest). The only behaviour change is the stamped D3. The whole suite through the lock is
899 total, 0 failed, and the hosted run of 9d49695 passes. **In plain words: yes, the branch can be landed as it
is. Main has not moved, so its pull request's checks and code scan run on exactly this tree. Land by
`landing.txt`.**

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| R1 | Records | The kit's control row K4 says the client-edge cell is "proved by mutant mBig". No mutant of the bound can redden it, because the edge value `Array.MaxLength - 1` never overflowed (my base run: 0 exceptions on 3618 calls at that limit). Builder's deviation 2. | Future kits: F2's proof is the constructor cell (K3 with mBig); the client cell is a regression guard with no red of its own. |
| R2 | Records | Stamp S1 says "kit 202 lines"; `wc -l` prints 201 and the file ends with a line feed. Builder's deviation 5. | None beyond the record. |
| R3 | Records | The new `internal Oxpd2Schema.PropertyArray`, together with lane C's `InternalsVisibleTo Include="Datasec.Suite.Contracts.Tests"` (simple name, no public key): any assembly in the process that takes that name reaches the arrays without reflection. My probe takes that name to see internals; it did not use this member. This is the same power reflection already gives (named limit H6). | A line for any later lane that loads third-party code into the server process. |
| R4 | Records | N9's new astral rows visit the first two bounded string sites per operation (lane C's `Take(2)`); this limit is carried over and named in STATUS. My 626 astral and non-ASCII length cases cover every site my reading reaches. | None for the merge. |

Still owed from round 1, and untouched here: F4 (process), F5, F6, F7 (records). See `FOR-RECORDS.md`.

## Item 1: scope

- Refs by GET at 17:52 and 18:00:00: branch `9d496955...`; main `5e36d8dc...` (unmoved); open pull requests 0; the
  head's parents `5e36d8dc` only; `rev-list` ahead 1, behind 0. The commit message is the kit's 123-byte subject
  plus the one attribution line, and the author and committer are the project's identity.
- `git diff --name-status 5e36d8dc 9d496955`: 11 rows, 9 `M` and 2 `A`, 0 `D`. 2 under
  `contracts/oxpd2/generator/` (`Oxpd2Generator.cs`, `Oxpd2RuntimeText.cs`); 5 under `Generated/` (`Runtime/`
  `Oxpd2InboundOperation.cs`, `Oxpd2Json.cs`, `Oxpd2ParseLimits.cs`, `Oxpd2Schema.cs`; `Targets/`
  `Oxpd2InboundCatalogue.cs`), which is FACT 3's prediction; 4 under `tests/Datasec.Suite.Contracts.Tests/` (`M`
  `ClientTests.cs`, `InboundTests.cs`; `A` `LimitTests.cs`, `ReadOnlyListTests.cs`). Every path is `.cs`.
- `git diff --quiet 5e36d8dc 9d496955 -- Datasec.Suite.slnx Directory.Packages.props .github build README.md
  '*.csproj' '*packages.lock.json' global.json Directory.Build.props NuGet.config` rc 0. The same over
  `contracts/oxpd2/hp contracts/oxpd2/inputs.sha256` and both `.gitattributes` rc 0. Controls: the same verb over
  `Generated` rc 1 and over `contracts/oxpd2/generator` rc 1. Tree 293 files.
- Added lines (389): 0 outside printable ASCII (control: a planted U+200B counts 1). `words.py` (control `CONTROL
  FIRED: 13 of 13`) over the added lines and the commit message: `WORDS: clean (2 files)`.
- **Regeneration (mine).** Round 1's console, compiled from the head's three generator files by absolute include
  (`regen-build`, `regen-run`): `REGEN: files 85, bytes 3763086`. It is set-equal and byte-equal, 85 of 85, to the
  committed `Generated/` (86 files with `.gitattributes`, 3,763,086 bytes of `.cs`). A one-byte change is detected
  (control). The output holds 0 CR, 0 tab and 0 non-ASCII bytes.
- After my locked restore, `git status --porcelain` printed 0 lines: no lock file changed.
- Code read whole: the generator diff (2 files, 33 insertions, 14 deletions) and the four test diffs. The emitted
  runtime is the generator text verbatim (the regeneration equality proves it).

## Item 2: F1 closed? YES

My own walk (`probe/Program.cs` section F1; not the builder's walk) starts from every public static property AND
field of every public type of the built adapter (1445 types, 1238 members), goes through every public instance
property and field of every adapter object reached (8496 objects, including 4362 schemas and 12 operations), and
into every element of every collection reached (1510). A collection counts as an offender when it is an array, an
`IList` that is not read-only, an `ICollection<T>` that is not read-only, or an `IDictionary` that is not read-only.
Every collection also gets an identity write through `IList` and `IList<T>`.

| Read | Head 9d49695 | Base adapter (control) |
|---|---|---|
| collection-valued members found | 4: `Operations`, `RequestContentTypes`, `EnumValues`, `Properties`, each `ReadOnlyCollection<T>` | the same 4, each an array |
| offenders | 0 | 8 lines: the 4 members, each "array" and "identity write accepted" |
| identity writes accepted | 0 of 3016 | 1508 of 3016 |
| public members whose declared type is an array (properties, fields, method returns) | 0 | 0 |
| the round-1 case: then NON-identity writes on every schema reached (clear `Required` on every property, replace every enum value, `Add`, `Clear`, `RemoveAt`, swap every catalogue operation, replace every content type) through `IList<T>`, `IList` and a cast to the array type | 0 of 43,962 accepted | 41,286 of 43,962 accepted |
| body `{}` on `UsbAccessories POST /operationCallback`, before and after those writes, and through the catalogue | `MissingRequired at $.usbCallback` all three | `MissingRequired at $.usbCallback`, then `Malformed at $` both ways |
| digest of my 5128 targeted cases, before and after the writes | `CAD36262C6BF06AB` both | `CAD36262C6BF06AB`, then `21C842F79E113971` |

**Does any public member still hand out an array or a writable collection? No.** The per-value lists inside a parsed
model are built per parse (named limit D1); reflection into private fields is named limit H6; and R3.

## Item 3: F2 closed? YES

Probe section G on the head: `System.Array.MaxLength 2147483591`, `Oxpd2ParseLimits.HighestMaxBodyBytes 2147483590`,
on .NET 10.0.15 Arm64.

- `new Oxpd2ParseLimits(n, 32)`: `int.MinValue`, -1 and 0 each throw `ArgumentOutOfRangeException ParamName=maxBodyBytes`;
  1, 2147483589 and 2147483590 are made; 2147483591, `int.MaxValue - 1` and `int.MaxValue` each throw
  `ArgumentOutOfRangeException ParamName=maxBodyBytes`. On the base adapter all of the upper values are made: this
  is the stamped behaviour change D3, and nothing else.
- **Every one of the 201 methods of the 16 clients** (not only the first JSON method of each), built with
  `(HighestMaxBodyBytes, 32)` and `(HighestMaxBodyBytes, 4096)`, against nine small answers: `{}` with a declared
  length, `{}` with no length, an empty 200, one byte with no length, `[]`, 4 KiB of spaces then `{}`, a 100 KiB string
  value, 204, and 500 HTML. That is 3618 calls with **0 exceptions of any kind**. Outcomes: Malformed 1206,
  MissingRequired 1000, WrongType 402, status-only 402, value 608.
- Section E (round 1's N14 set) at `(Array.MaxLength - 1, 32)` with answer `{}`: value. The `IOException` line of
  round 1's F6 is unchanged (records, not this lane).

## Item 4: F3 closed? YES

- **m8 re-run by me.** In the mut clone, `LengthCheck`'s condition `!char.IsLowSurrogate(text[i])` was replaced by
  `i >= 0`, with my own edit (a different form from the builder's), so every UTF-16 unit is counted. I regenerated
  (`REGEN: files 85, bytes 3763063`; changed: the generator and `Generated/Runtime/Oxpd2Json.cs`), restored with a
  locked restore, and built (0 warnings, 0 errors). The whole suite: total 899, **failed 5**, succeeded 890, skipped 4.
  The 5 failures are `InboundShapeTests.N9_...` for `Authentication POST /prePromptResult` and `/postPromptResult`,
  `UserPolicy POST /applyUserPolicy` and `/configurationChange`, and `UsbAccessories POST /operationCallback`.
  Each is RED BY ASSERTION (`Assert.True` in `TestSupport.cs:306`): `... maxLength astral characters: expected a
  value, got Oxpd2Refusal OutOfRange at <site>`, at the sites `$.languageCode` (x2), `$.userInfo.displayName`,
  `$.userPolicyConfiguration.guestAttributes.displayName` and `$.usbCallback.hidRead.data` (maxLength 90110, raw
  body under the limit). I undid it with the Edit tool, regenerated (`REGEN: files 85, bytes 3763086`), and ran the
  whole suite (899, failed 0): `git diff --quiet` of the mut clone rc 0.
- **My own astral cases** (`scratch/specgen.py`, my independent reader of HP's five target files, extended): 626
  cases at every bounded string site my full payloads reach. They cover maxLength astral characters (value) and
  maxLength + 1 (OutOfRange); maxLength - 1 letters plus one astral (value); maxLength astral plus one letter
  (OutOfRange); maxLength and maxLength + 1 as escaped surrogate pairs (value, OutOfRange); e-acute, euro sign and
  U+10FFFF at maxLength (value) and past it (OutOfRange); minLength astral (value) and minLength - 1 (OutOfRange);
  and a single astral character where minLength is 2 or more (OutOfRange). Two escaped-pair cases at the 90110 site
  are over 1 MiB and left out by construction. **Head: 0 of 5128 targeted cases differ from the rule. m8 adapter:
  311 differ** (the first 40 printed: maxLength rows of every kind, plus minLength - 1 and single-astral rows).

## Item 5: nothing else changed in behaviour

- **Differential, base against head, on the same inputs** (my probe built twice, against the head's adapter and
  against the base adapter; the base adapter is round 1's build of 48120e58, whose generator and `Generated/`
  equal main 5e36d8dc's, `git diff --stat` empty). Section A covers my 5128 targeted cases; section C my fuzz, seed
  **21112026**, 360,000 inputs over the 10 operations in parallel (random bytes, JSON-alphabet noise, 1 to 8 byte
  edits, structural mutations: type swaps, Int64 edges, `1e3`, `-0`, `1E400`, 3000-character strings, astral text,
  20 to 70 deep arrays, removed and duplicated keys, sentinel keys, arrays grown by up to 400); section D 171,399
  inputs over 57 device-answer models. That gives **536,128 outcome lines, sorted; digest
  `C01CF2581B3C94FC37E646FD714D70E264E3B7217C76F0D7C112B87FBECD447A` for BOTH**. With round 1's seed 8302026 the
  head's fuzz counts equal round 1's line exactly (DuplicateKey 30485, Malformed 134698, MissingRequired 54300,
  OutOfRange 10460, TooDeep 669, TooLarge 5, UnknownEnumValue 1758, value 78622, WrongType 49003).
- Head, round 1's properties again (sections B and E): 170 size and depth rows as required. These are exactly
  `MaxBodyBytes` (value) and +1 (TooLarge); +1 that is also a BOM followed by invalid UTF-8 (TooLarge: the size check
  runs first); 64 MiB of spaces and of `[`; depth 32 and 33; 100000 deep; 4096 and 4097 at limits (1 MiB, 4096); and
  64 MiB of `[` at `(Array.MaxLength - 1, 4096)`. 3172 hostile path and query calls, 0 differing; 128 N14 calls; 0
  requests with `Authorization`; one host. 0 static fields that are not readonly. The options are read-only. The
  references are unchanged (System.* only). Every refusal text has the exact form, with schema names only and no
  sentinel. `PROBE: PASS (0 failures, 0 case differences)`. Slowest single parse 14.4 ms.
- **Whole suite through the lock** (head clone, `CI=true` locked restore rc 0, build `0 Warning(s)` `0 Error(s)`,
  `dotnet test -c Release --no-build`): `Test run summary: Passed!`, **total 899, failed 0, succeeded 895, skipped 4**.
  The 4 skipped are the secret store's `KeyRingProtectionTests` Windows cases (K06, K07, W01, W02). This equals the
  builder's total.
- **Hosted run of 9d49695 by GET** (kit B1834's `hosted.py`, unchanged, `--total 899 --rules 293 --skipped-linux 4
  --skipped-windows 19`; `logs/hosted.out`): run 44877267745, attempt 1. Four check runs (`linux`, `windows`,
  `rules`, `secret-scan`), each completed success, every step success. linux `total: 899` x2, `succeeded: 895`,
  `skipped: 4`, `failed: 0`, `GUARD: clean (10 files)`. windows `total: 899` x2, `succeeded: 880`, `skipped: 19`,
  `failed: 0`, `GUARD: clean (11 files)`. secret-scan `PLANTED-CONTROL secret-scan: rc 1`, `PLANTED-CONTROL
  neutral-scan: ... 25 of 25, rc 1`, `NEUTRAL-SCAN: stored objects 670 ... objects of this commit not among them 0`,
  `no leaks found` x3. rules `Ran 53 tests`, `UNIT-TEST FLOOR: ran 53, floor 53`, `RULES: clean (293 files)`. Last
  line `HOSTED 9d496955...: PASS`. Control: `--skipped-linux 5` prints `FAIL 2`. The code scan has NOT run on this
  branch (push runs carry the four ci jobs only); it runs on the pull request.
- **Lanes in flight.** `git merge-tree --write-tree` of this head with `b1831/wp15-token-broker` (70c1fad5) and with
  `b1836/r5-hp-inputs-exemption` (28d2852d) is clean both times (rc 0). The sides are path-disjoint; `landing.txt`
  says what to do if either lands first.

## Item 6: the builder's deviations

| # | Ruling | The line that proves it |
|---|---|---|
| 1 | ACCEPTED | `LimitTests.cs`: `ArrayBound = Array.MaxLength - 1`, and `Published()` reads `HighestMaxBodyBytes` by reflection and asserts it equals `ArrayBound`; my probe: 2147483590 = 2147483591 - 1. Writing the tests first against main needed it. |
| 2 | ACCEPTED; records R1 | my base adapter: 0 exceptions at `Array.MaxLength - 1` on 3618 calls, so K4 has no red; the kit's wording is wrong, not the build |
| 3 | ACCEPTED | wider is safer; my own wider walk on the base names exactly the same four members (and nothing else), and 0 on the head |
| 4 | ACCEPTED | my run: the forbidden-path verb rc 0, controls over `Generated` rc 1 and over `contracts/oxpd2/generator` rc 1; both forms fire |
| 5 | ACCEPTED; records R2 | `wc -l` of the stamped kit prints 201, last byte `0a` |

## Item 7: texts (`scratch/texts.py`; round 1's program with paths changed)

`pr-title.txt` (the commit subject), `pr-body.md` (what the round closes; the behaviour change in its own bold
section: a `maxBodyBytes` above `HighestMaxBodyBytes` = `System.Array.MaxLength - 1`, including `int.MaxValue - 1`,
is now refused when the limits are made), `squash-subject.txt` (ends `(#PRNUM)`), `squash-body.txt` (ends with the
one attribution line), `landing.txt` (the round-1 form: `pr_retrigger.sh --check` on the pull_request run,
`pr_checks_wait.sh --min-checks 8` = 8 distinct names read on pull request 6's head, the totals, CodeQL 0 open
alerts, head-pinned squash, after-merge reads, and MAIN MOVED), and `FOR-RECORDS.md`.

Each text was exported through the workflow's own `neutral_export` (cut by program from the head's `ci.yml`, lines
120 to 128) as the commit message of a scratch repository, and scanned with `--no-banner --redact
--ignore-gitleaks-allow --exit-code 1`. That covers title, title and body, body, the squash message with a number,
the squash message as written, the squash body, the default squash shape, and `landing.txt` (after its last edit):
export rc 0, message stored whole, scan rc 0, `no leaks found`, 8 of 8. Control (a planted token built from parts):
scan rc 1, `leaks found: 2`. `words.py` over the title, squash subject, squash body without its attribution line and
PR body without its footer: `WORDS: clean (4 files)`; the squash body whole: `WORDS: clean (1 files)`. The decision
words "decided" and "approved" count 0 in every committed text, and the only host and non-ASCII hits are the footer
and attribution lines. No text says the owner decided anything; each says every choice was made inside the build.

## NOT RUN / NOT TESTED

- Anything on Windows: the hosted `windows` leg is the only proof.
- The builder's mArr and mBig mutants: I re-ran only m8. My F1 base run stands in for mArr (it shows the same four
  members and that later parses change), and the constructor edges on the base stand in for mBig.
- Lane C's six earlier mutants.
- `dotnet publish` and the release guard locally (I read the hosted GUARD lines).
- CodeQL for C#: the extractor does not run on this arm64 machine, and the pull request's scan has not run yet.
- A client at the highest limit handed a body near 2 GiB (memory; named limit H9).
- Concurrency of the read-only views (named limit H5; my fuzz ran 10 operations in parallel without a difference).
- Any real printer, simulator or gateway payload.
- `repo_rules.py --source-documents` over the supplied folder (by the kit's design, Q8).
- The pull_request runs and the merge with any later main: they do not exist yet.
