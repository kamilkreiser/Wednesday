STARTABLE: YES (on Tuesday answering Q1 and Q2 "a" in words at S4; Q2 "b" makes it NO: a re-draft)

# B2109 DRAFTER REPORT: OXPd lane OX-A (the OXPd 1.x client), seat X77

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2109_SEAT-X77_oxpd2-lane-a-oxpd1-client.md` (90592 bytes, sha256 `2b5894833c053f377e7098b32d8415861a08d5e05a58896f79f44cdb34d2b4c3` at 07:54:11 AEDT by `date`); sidecar `.measured` beside it (179 lines: one header, 178 claims); `stamp_check.py <kit>` exit 0 (`178 claims, 178 measured, 0 not measured`). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s329/d2109/` (`<d>`). Drafter's first `date`: `Thu 26 Nov 2026 07:31:49 AEDT`.

## BLUF
1. **All eight owed items fit ONE kit (Q1 default a).** Ten files, all `M`, all under `src/Datasec.Suite.Adapters.Oxpd1/` and `tests/Datasec.Suite.Adapters.Oxpd1.Tests/`; no Lab path, no added file. One helper (`Oxpd1Soap.IsXmlWhiteSpace`: space, tab, CR, LF only) closes 133, 143 and 146 and serves 126 and 134. 126 is FIXED (its first option), 134's client half moves `CallbackMessage` onto `ReadTextAnswer`, 93 refuses any `@` in both records, 85 and 94 are doc-only.
2. **The kit freezes NO patch (Q2 default a, STOP-CLASS).** I could run no dotnet job: `heavy.py` takes the wave lock by `mkdir` of `<project>/.tools/wave1-heavy.lock.d` (its header, read by `sed -n 1,60p`), a write inside the OXPd project folder that the commission forbids. So the seat writes the code and seven NEW cells (29 cases) to a row-by-row spec, red first; the mutants' exact edits go in a rows file the frozen `mutants_a1.py` reads. **Every red, green and mutant number in the kit is PREDICTED, never run; a miss is `STOPPED: NEEDS TUESDAY` by the kit's own wording.**
3. **BASE is `8757daa6c48d1f6764460d378ce3c15863b383df`** (PR 53's squash; open PRs 0; `heads/b2109` 0 rows). BASE hosted run PASS at `--total 2338 --rules 679` (my run of `hosted3.py`; the control at 2339 printed FAIL 4). PREDICTED head: `--total 2367 --rules 679`.
4. **Seat id X77 is free:** no file under `tuesday/briefs/` names `SEAT-X77`, and the word-boundary scan for `X77` over the briefs hits only this commission. The control fires: `X76` is in `2026-11-26_B2104_SEAT-X76_oxpd2-pr53-rescan.md` (and B2104's commission, B2105's kit and B2105's commission). No `Datasec/OXPd2-*` pane is live (`tmux list-panes -a`: `tuesday`, `Datasec/MPS-R329` and unnamed shells).
5. **Model:** `<project>/CLAUDE.md:7` says "every agent on this project runs on the newest Opus" (`awk NR==7`), so the seat runs on `claude-opus-5-5` (`models_latest.json:17`) and the launch line carries `BRIEF_SEAT_LEVEL=opus`. Gate G1 (`model-routing.md:108`).

## FACTS RE-MEASURED (instrument, then what it printed)
- `gh auth status` (project GH_CONFIG_DIR): logged in as `kamilDatasec`. `gh api -X GET repos/datasecau/OXPd_2/branches/main`: `8757daa6...`. `pulls?state=open`: 0. PRs 53 to 36: closed, merge shas listed in `<d>` by the jq line. `.private`/`.permissions.push`: `true true`.
- `gh api -X GET .../commits/8757daa6`: tree `e20eeff6ec7ee5a3b16a9917f6e254135de6271f`, 1 parent `1ccf6d0c...`. My tarball of BASE (`gh api -X GET .../tarball/8757daa6`), indexed in a scratch repo, gave `git write-tree` = `e20eeff6...`. That equality is the control that the tarball is BASE byte for byte (679 files).
- Run 45661759219 (ci, push, success). Its job logs by GET: linux `total: 2338` x2, `succeeded: 2334`, `skipped: 4`, `GUARD: clean (14 files)`; windows `succeeded: 2317`, `skipped: 21`, `GUARD: clean (15 files)`; rules `RULES: clean (679 files)`, `Ran 117 tests`, `UNIT-TEST FLOOR: ran 117, floor 117`. `hosted3.py` PASS (`<d>/logs/hosted-base.out`); control FAIL 4 (`<d>/logs/hosted-base-ctl.out`).
- Adapter test cases at BASE: indented `[Fact` 46, `[Theory` 8, `[InlineData` 58, column-1 0, MemberData/ClassData 0. That gives 104 cases (DERIVED), equal to kit B2100's measured adapter total (RELAYED).
- The eight owed items, each read WHOLE (`awk` over the lines found by `grep -n '^<n>\. - \['`): 85 at line 618, 93 at 678, 94 at 685, 126 at 924, 133 at 973, 134 at 980, 143 at 1044, 146 at 1065. `BACKLOG.md` is 1095 lines, sha `ccacba5f...`.
- Pointers at BASE, each by `grep -n` (`<d>/logs/pointers-src.txt`, `pointers-readme.txt`):
  - `Oxpd1Soap.cs`: class at 15, `ReadAnswer` at 128, the `TextOnly` test at 174, `besides` at 252, `IgnoreProcessingInstructions`/`IgnoreComments` at 98-99.
  - `Oxpd1Writer.cs`: agent `UserInfo` at 188, button target at 290, `Undo` docs at 355 and 535, `OnlyElements` at 756.
  - `Oxpd1Echo.cs`: echo `@` rule at 122, `CallbackMessage` at 212.
  - `Oxpd1ClientOptions.cs:86`; `Oxpd1Command.cs:771` (the lab's `@` rule) and `:1064` (the lab's IsServiceEnabled read).
  - `test.xsd`: `Message` `minLength` 1 at 578; `IsServiceEnabledResponse` at 928-934. `common.xsd:440` holds `LimitedUri`.
- Base sha256 of the ten owned files: `<d>/logs/base-files.txt`. Four of them equal B2100's "After both" column, so row 4 landed byte for byte.
- Prior work, by `gh api` contents at each merge and its parent (`<d>/logs/prior.out`): `OnlyElements` came with PR 52, `ReadTextAnswer` and `CallbackMessage` with 51, `TextOnly` with 48, the agent `UserInfo` with 41, the button target with 53, the `Timeout` summary with 37.
- No landed cell reads the adapter's exception texts: `grep -c -F 'at most 256 characters'` over Lab tests 0 (control `Oxpd1Writer.cs` 3). No test reads the adapter README (grep). The Lab stub's callback body is clean (`Oxpd1Stub.cs:445`).
- Toolchain: `.tools/dotnet/dotnet --version` printed `10.0.404`; `gitleaks version` printed `8.30.1`. The repo's local `core.sshCommand`, `user.name` and `user.email` all return rc 0. Load `2.36 2.30 1.69`; 884 GiB free.

## THE TOOLS (seat-tools in `<d>/seat-tools/`, hashes in `<d>/logs/tools.sha256` and in the kit)
`clone.py`, `heavy.py`, `hosted3.py`, `run_step.py` and `words.py` are byte for byte copies of `s328/d2100/seat-tools` (`cmp` equal, 5 of 5). The new files:
- **`mutants_a1.py`** is B2100's `mutants_b4.py` with three changes: it reads its rows from a JSON file, it MATCHes on "expected red subset of red subset of new cells", and it runs the adapter suite only. `--list` printed `LIST: 1 mutants, 2 new cells` (rc 0) on a good file and `LIST REFUSED` (rc 1) on a bad one. `apply`/`undo` on a copy of BASE's `Oxpd1Writer.cs` left sha `c099aea3...` equal. Its label regex was checked on synthetic `[FAIL]` lines. Its `run` path is NEVER RUN.
- **`checks_a1.py`** runs 8 checks with controls. Over BASE's tree it printed `CHECKS: 1 of 8 PASS` (the controls); over a SIMULATED staged edit that compiles nothing it printed `8 of 8`.
- **`commit-message.txt`** is 374 bytes, 3 lines, with a 316-character subject. `words.py` printed `WORDS: clean (1 files)`; B-numbers 0.

## CHAIN INPUTS (each input exists at BASE or comes from an earlier step)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | kit, Stamp S1-S8 | Tuesday's stamp |
| 1 | `<src>` (8 files, exist); `<repo>` local values (exist, rc 0); origin BASE; BASE push run 45661759219 | drafter scratch; `<repo>`; GitHub |
| 2 | BASE files | Step 1 clone |
| 3 | THE NEW CELLS spec (kit); restored and built BASE clone | kit; Step 1 (restore, build, BASE adapter run) |
| 4 | red tree; C1-C7 spec; `mutants_a1.py`; `mutants.json` | Step 3; kit; Step 1; written in Step 4 after green |
| 5 | green tree, mutants undone, rebuilt | Step 4 |
| 6 | staged tree; `checks_a1.py`, `words.py`, `commit-message.txt` | Step 5; Step 1 |
| 7 | commit; `origin/main`; `run_step.py`, `hosted3.py` | Step 7a; fetch; Step 1 |

## D-DECISIONS (all Tuesday's as coordinator; none the product owner's)
- **D1** One kit for all eight items.
- **D2** The seat writes the code.
- **D3** The helper is the four characters written out, `internal` in `Oxpd1Soap`, used by all four readers.
- **D4** 126 is fixed, not named.
- **D5** `CallbackMessage` goes through `ReadTextAnswer`, so an empty message is null (HP `minLength` 1).
- **D6** Any `@` in `AbsoluteUri` is refused, in both records.
- **D7** 85 is doc-only; the attribute cap stays owed.
- **D8** 94 is doc-only; `W03`'s name is unchanged.
- **D9** New cells only, so no landed line changes.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 (STOP-CLASS)** One kit or two. Default **a**: one kit, all eight. Alternative **b**: the commission's split (133, 143, 146, 126 first).
- **Q2 (STOP-CLASS)** Who writes the code. Default **a**: the seat, to the kit's specification, with PREDICTED numbers. Alternative **b**: a re-draft by a drafter allowed the OXPd wave lock, with frozen patches.
- **Q3** The helper. Default: the four characters written out. Alternative: `XmlConvert.IsWhitespaceChar` (UNMEASURED).
- **Q4** Item 126. Default: fixed. Alternative: name it in the Limits only.
- **Q5** Item 134. Default: through `ReadTextAnswer` (empty message is null). Alternative: three rules inline, with the empty message kept as "".
- **Q6** Item 93. Default: any `@`, both records. Alternative **b**: the authority only (HP's pattern). Alternative **c**: the agent only.
- **Q7** Item 85. Default: doc-only, the cap stays owed.
- **Q8** Item 94. Default: doc-only, `W03` unchanged.
- **Q9** Default: new cells only. Alternative: rows appended to landed theories (the owed list's "one more W07 row").
- **Q10** Defaults:
  - G1 gate, no local CodeQL, Opus.
  - READY at Step 0 + 180 minutes; push by + 150.
  - Pane `Datasec/OXPd2-X77`.

## UNMEASURED / NEVER RUN (a stamp must know)
- **Every dotnet job.** Nobody has run any of these: the PREDICTED red (`Total: 133, Failed: 23`), the green (`total: 2367`, `succeeded: 2363`), the nine mutant expectations ("at least" sets), the release guard, `unittest` and `repo_rules.py` on this lane's tree.
- **Red-on-BASE rows resting on source reading, not a reviewer's run:**
  - A05 rows 5, 6 and 11.
  - T08 row 6.
  - V06 row 2.
  - B07's and W10's path-`@` assertions.
  - The rows marked RELAYED rest on the owed list's probes.
- **Whether .NET's reader keeps white-space-only text nodes** in the stub-fed cells (H10). The control rows are written to hold either way.
- **The `mNoTab` mutant** could redden a landed cell. Most likely ClientTests K15, whose tab sits in text, not beside an element. The tool would print DIFFER, and the kit makes that a `STOPPED: NEEDS TUESDAY`.
- **`mutants_a1.py run` and `checks_a1.py` on real code** are NEVER RUN, as are the commit, push, `run_step.py`, the hosted run on the head, and CodeQL (x86_64 extractor, RELAYED).
- **Cross-lane:** once this lands, two Lab README sentences go stale: `:220` and `:308`-`:311`. They are lane OX-B's (in FOR RECORDS / FOR TUESDAY).

## OUTSIDE-THE-FENCES DISCLOSURE
- **Writes:** only the kit, its `.measured`, this report, and files under `<d>`: the tarball, its extracted tree, seat-tools, logs, a selftest scratch git repo made by `git init`/`add`/`write-tree` (no commit, no identity), and `_quarantine/` (one moved log, nothing deleted). Nothing was written in the OXPd project, GitHub, Jira, the card store or another seat's tree.
- **One refused attempt:** a hook refused a `git -C $R init` because `$R` was unexpanded; the retry used the literal path inside `<d>`.
- **Reads of the project:**
  - `CLAUDE.md`, `BACKLOG.md` and `CLARIFICATIONS.md` (sha only).
  - Read verbs on the stale `<repo>`: `rev-parse`, `cat-file -t`, `config --get` (values not printed).
  - `ls` of `3_Access_Keys`, piped to a filename count only (2 names matching `github_deploy_rw`). No file there was opened or hashed.
  - The Briefs folder listing and the last lines of three STATUS files.
- **Network:** `gh api -X GET` only, under the OXPd GH_CONFIG_DIR: the repo, branches, pulls, refs, contents, the tarball, runs, jobs and job logs.
- **Executed:** `.tools/dotnet/dotnet --version`. No other dotnet. No az, ssh, docker or printer; no message to anyone.
