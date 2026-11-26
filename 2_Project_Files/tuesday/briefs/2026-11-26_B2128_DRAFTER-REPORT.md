STARTABLE: YES

# B2128 DRAFTER REPORT: OXPd 2, lane OX-B kit 2 of 2 (the lab tool `oxpd1`: Oxpd1Command.cs, Oxpd1EchoVerb.cs, the Lab README, two test files and the stub), seat X79

Drafter: read-only Opus agent in Tuesday's session (s331). First `date`: `Thu 26 Nov 2026 20:36:59 AEDT`; last `date` before this report: `Thu 26 Nov 2026 21:02:34 AEDT`. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s331/d2128/` (below `<d>`).

## Files written
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2128_SEAT-X79_oxpd2-lane-b-kit2-lab-oxpd1.md` (274 lines, 102152 bytes, sha256 `6f089d82...`; 9 slot lines `____`, S1 to S8 and the last line; printable ASCII, `grep -c -E '[^ -~]'` 0).
- Sidecar: `...-kit2-lab-oxpd1.md.measured` (181 claims, 181 measured; `stamp_check.py <kit>` rc 0, `<d>/logs/stamp-check.out`).
- This report.
- Seat tools in my scratch (the kit's `<src>`): `<d>/seat-tools/` = `clone.py`, `hosted3.py`, `run_step.py`, `words.py`, `mutants_b1.py` (kit B2122's, sha256 equal), `heavy.py` (canonical `31adedc8...`), and this kit's `checks_b2.py` (`f6e874f3...`) and `commit-message.txt` (`bde10a57...`, 383 bytes, subject 325 characters).

## BLUF
1. ONE kit for all six items (Q1 default): **106** (a register writes nothing when the agent read's result or a record holds text, an attribute that is not a namespace declaration, or a second `id`), **107 + 109** (one rule: the three address options take printable ASCII only), **110** (README line plus a pinning cell; no code), **135** (the parser refuses a callback host whose callback address with port 65535 would be over 256 characters), **136** (the parser refuses a delay at least the callback wait or the time-out).
2. Six files changed, none added: `Oxpd1Command.cs`, `Oxpd1EchoVerb.cs`, the Oxpd1 `README.md`, `Oxpd1WriteTests.cs` (V17, V18, V19), `Oxpd1EchoTests.cs` (E09, E10, E11), `Oxpd1Stub.cs` (ONE plan member `ResultContent` and its one use, added lines only). 38 new cases, 26 PREDICTED red on BASE, eleven mutants.
3. PREDICTED totals: Lab executable 314 -> 352; whole solution 2384 -> 2422 (succeeded 2418, skipped 4; Windows 2401 / 21); rules 679 unchanged.
4. **A finding that shapes item 106:** the lab cannot see three of the shapes the owed item lists. The client's parser drops comments and processing instructions (`Oxpd1Soap.cs:105` to `:106`), takes only the result element of the response (`:176`), and hands the lab a masked COPY of the result with no parent (`Oxpd1Client.cs:245`), in which text and CDATA are joined (`Oxpd1Soap.cs:282` to `:283`). So the kit refuses what the lab CAN see and names the rest (comment, processing instruction, anything beside the result, the id as a record's other elements' text) as README Limits, with two LIMIT rows pinned. These are candidates for the adapter lane (H6).
5. **Precondition met:** R334 ended `READY B2124: afb5806b... | C-90 | ticked owed 108 111 127 142 145 150, none in part, new owed 152 to 154 | jira comment 41518`; no pane name holds `OXPd2`; `main` = `504ca043` (PR 55's squash); open PRs 0.

## Facts re-measured (instrument, control)
- Origin (`gh api -X GET`, project `GH_CONFIG_DIR`, account `kamilDatasec`; 20:37:49 and 21:00:07): `main` `504ca043688e...`, one parent `c73cda4c`, tree `7c987de4`; open PRs 0; `matching-refs/heads/b2128` 0 (control `b2122` 1); private true, push true (`<d>/logs/origin.out`).
- BASE tree: tarball by GET into `<d>/src_504c`, 679 files; a scratch repository of it printed tree `7c987de4...` (equal to main's). No `certificates/`, `.key` or `.pem` path in the tarball (count 0).
- BASE push run 45745847562: `hosted3.py ... --total 2384 --rules 679 ...` -> `HOSTED 504ca043...: PASS`; control `--total 2385` -> `FAIL 4` rc 1.
- Lab test counts at BASE (indented patterns over every `.cs` of `tests/Datasec.Suite.Lab.Tests`): Fact 62, Theory 63, InlineData 252, column-1 0, MemberData/ClassData/TheoryData 0 -> 314 (= kit 1's predicted head total).
- The six owned files at BASE: sha256 and line counts in the kit; each printable ASCII, no tab, no CR, final LF (control: planted U+00A0 counted 1). Blob history by GET: `Oxpd1Command.cs` unchanged since PR 53, `Oxpd1EchoVerb.cs` / `Oxpd1EchoTests.cs` since PR 51, `Oxpd1Stub.cs` since PR 53.
- Prior work by GET at each merge and parent: `ReadBeforeRegisterAsync` and `Address` from PR 44, `XmlText` and the own-namespace id rule from PR 45, `--button-target` through `Address` from PR 53, the echo verb from PR 51.
- HP's committed schema (`contracts/oxpd1/hp/`): `name="id"` on 1 line of `authentication.xsd` (14) and 0 of `common.xsd`; `xs:attribute` 0 and 0; `mixed=` 0 and 0; `XMLElementContainer` (the one `xs:any`) not used by `authentication.xsd`. So 106's widened rules refuse no answer in HP's shape.
- The client's own bounds (READ ONLY): `name.Length > 100` and `title.Length > 100` (`Oxpd1Writer.cs:141`, `:285`), callback `AbsoluteUri.Length > 256` (`Oxpd1Echo.cs:122`).
- Live `BACKLOG.md` (sha256 `c816826c...`, 1158 lines): in-process `startswith` counts 1 each for `106/107/109/110/135/136. - [ ] `, `108/111/127/142/145/150. - [x] `, `152/153/154. - [ ] `; control `106. - [x] ` 0.
- Seat id X79 free: a lookbehind scan of every file in `tuesday/briefs/` finds `X79` only in this commission (control `X78` 8 files); no pane `Datasec/OXPd2-X79`.
- Machine (20:43:01): load `3.15 3.11 2.49`; 868 GiB free; wave lock absent; `<project>/.tools/b2128` absent; dotnet `10.0.404`, gitleaks `8.30.1` by path; `<repo>` local `core.sshCommand`, `user.name`, `user.email` set (rc 0, values never printed), deploy key present.
- Tools: `checks_b2.py` on BASE `CHECKS: 1 of 8 PASS` (each check's control fires); on a simulated staged edit (no compile) `CHECKS: 8 of 8 PASS`; `mutants_b1.py --list` good rc 0 (`LIST: 2 mutants, 6 new cells`), bad (adapter path) `LIST REFUSED: rows mBad` rc 1; `apply`/`undo` on a scratch `Oxpd1Command.cs` restored sha256 `3e28c05b...`; the red-label regex maps synthetic `[FAIL]` lines to `Oxpd1WriteTests.V17`, `Oxpd1EchoTests.E10`, `Oxpd1EchoTests.E11`; `words.py --control` 13 of 13; `words.py` over the commit message and over a preview of every cell name, row text and frozen text: `WORDS: clean (1 files)` each; B-number count in the message 0.
- Kit 1's seat pushed 31 minutes after its Step 0 (its STATUS: `12:30:41` boot, `13:01:51` push): the basis of the one-kit default.

## Chain inputs (every step's input exists at BASE or comes from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, Stamp slots (S4 Q1/Q3 answers, S8 runner sha) | Tuesday's stamp |
| 1 | `<src>` 8 files; `<repo>` local values; origin BASE; BASE push run; R334 STATUS + live BACKLOG | my scratch (exists); `<repo>`; GitHub; R334 (READY already) |
| 2 | files at BASE | the clone from Step 1 |
| 3 | THE NEW CELLS and C7; restored, built clone | kit; Step 1 |
| 4 | red tree; C1 to C6; `mutants_b1.py`; `mutants.json` written after green | Step 3; kit; Step 1; Step 4 |
| 5 | green tree, mutants undone and rebuilt | Step 4 |
| 6 | staged tree; `checks_b2.py`, `words.py`, `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit; `origin/main`; `run_step.py`, `hosted3.py` | Step 7a; fetch; Step 1 |

## D-decisions (each Tuesday's default as coordinator; each a Question)
D1 one kit; D2 152 and 153 out (shared file only the README); D3 the seat writes the code, five refusal texts frozen; D4 106 = the reviewer's proposal widened to the record (result attribute, result text, any-depth second `id`, record attribute/text), invisible shapes named limits; D5 107+109 by one printable-ASCII rule on all three address options (stricter than HP's anyURI; `xn--` hosts); D6 110 README + pin (the client throws on more than 100 UTF-16 units, so the lab cannot count characters); D7 135 in the parser, port 65535 assumed, up to 4 characters early; D8 136 as a usage error, defaults counted, async ignores the time-out; D9 no Windows early return, one stub member; D10 the `IsServiceEnabled` README sentence untouched.

## Questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS, S4 in words): one kit or two.** Default a: one kit for all six (38 cases, 11 mutants). Alt b: split by file, `Oxpd1Command.cs` first.
- **Q2: do 152 and 153 join?** Default: NO (later round). They live in `LabFiles.cs` (not touched here); the README is the one shared file.
- **Q3 (STOP-CLASS, S4 in words): who writes the code.** Default a: the seat, to the kit's spec. Alt b: re-draft by a drafter allowed the wave lock.
- Q4 (106 width). Default: widened to the record. Alt: the proposal exactly (V17 rows 7 to 9 become LIMIT rows, one mutant fewer).
- Q5 (107/109). Default: printable ASCII only. Alt: `XmlText` on `AbsoluteUri` plus a README line (V18 rows 3, 6, 7, 10 flip).
- Q6 (110). Default: README + pin; no safe code alternative in this lane.
- Q7 (135). Default: parser, exit 2, port 65535. Alt: build the call before the folder.
- Q8 (136). Default: usage error. Alt: words in the exit-13/8 lines only.
- Q9 (Windows, stub). Default: no early return; one stub member.
- Q10 (gate, level, timing, pane). Default: G1 (`model-routing.md:108`), no local CodeQL, Opus (`<project>/CLAUDE.md:7`, `BRIEF_SEAT_LEVEL=opus`), READY at Step 0 + 180, push by + 150, pane `Datasec/OXPd2-X79`, gate round 1 of 2 of lane OX-B kit 2.

## UNMEASURED / PREDICTED (the riskiest predictions, for the stamp)
- Every dotnet number: red 26 of 352, green 352 / 2422, all eleven mutants MATCH. None run.
- RED rows resting on DERIVED, not RELAYED, behaviour: V17 rows 8 and 9 (text or attribute on another agent's record passes BASE); V17 row 2 (CDATA reaches the lab as text, from the mask's docstring); V18 row 7 (button target, same `Address`); V18 row 10 (BASE's `Uri.TryCreate` takes a space and escapes it as `%20`: UNMEASURED, the least certain row); E09 row 200 (BASE's parser takes a 200-character name of 63-character labels); E11 rows 3, 4, 7, 8 (equal and default bounds). A miss stops the seat with a question to Tuesday.
- V17 row 11 (a comment is dropped by the client) and row 12 (id as a name) are LIMIT rows, DERIVED green on both.
- E10 (232-character host, a whole run): RED RELAYED from owed 135's probe (macOS); Windows DERIVED.

## Outside-the-fences disclosure
- No write to the OXPd project, Jira, GitHub or the card store; no `cd`; nothing deleted (moved into `<d>/_quarantine/`: kit 1's `checks_b1.py` copied by mistake into my seat-tools, two superseded checks output folders, the first sidecar). No recursive read of the project folder: files read by path only (`CLAUDE.md`, `BACKLOG.md`, `CLARIFICATIONS.md` C-85 to C-90 by `sed`, the B2122 and B2124 STATUS files' heads, tails and grep lines, `.tools/` listed at depth 1); `Source_Documents/` not touched. `gh` only as `gh api -X GET` under the project `GH_CONFIG_DIR`. No Jira call. Nothing to any person, HP or device. No dotnet job, no lock taken.
- **One write outside my scratch:** a `find ... > /tmp/x` file list (not needed, a slip) at about 20:41; moved into `<d>/_quarantine/tmp-x-find-list` at once; `/tmp/x` no longer exists. The same command sent its stderr to `/dev/null`, as did one `gh api` loop reading blob shas (both read-only).
- Git write verbs ran ONLY in my own scratch repository `<d>/selftest/clone` (BASE's tarball, no remote): `init`, `add`, one `commit` with `-c user.name/user.email` set to a placeholder (scratch only, never a project repository), `add` of the simulated edit, and one `git stash` to clear it before the BASE-side rerun.
- Two hook refusals, each re-issued in an allowed form: an `echo` separator starting with `=` and an unquoted `$G` command variable (re-run inside `bash`).
- The kit carries the GitHub login name `kamilDatasec` in FACTS 1 (as kits B2109 and B2122 did); it is not text the seat copies into a commit.
- Card ids: none read, none cited.
