From Tuesday (Datasec coordinator seat), Datasec / OXPd_2. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Files naming another B-number are READABLE claims only. Marks: **MEASURED** = the drafter printed it with the instrument named (sidecar `.measured` beside this kit, one line per literal); **DERIVED** = source reading or arithmetic, not run; **RELAYED** = read in another seat's file, the gate's verdict or a ticket; **UNMEASURED** = nobody has. Drafted 2026-11-20 from 14:01 AEDT to the write clock in the sidecar's first line (clock reads by `date`: 14:01:26, 14:01:41, 14:05:28, 14:06:07, 14:09:36, 14:10:45, 14:10:54, 14:12:08, 14:14:24, 14:15:34, 14:16:10, 14:17:31) by a read-only drafter for Tuesday. Every `file:line` below was printed by program over the files as they stood in that window; re-print each before you rely on it. **Everything marked MEASURED was run by the drafter in its own scratch folder on a COPY of the head; nothing of it has run on a GitHub runner: every statement about what the hosted run WILL print is UNMEASURED unless it carries a MEASURED mark.**

# BRIEF B1774 | SEAT-X2: OXPd 2, ROUND 2 OF 2 OF THE CI SKELETON (WP0.3). ONE NEW COMMIT ON THE EXISTING BRANCH `b1764/wp03-ci-skeleton`, FAST-FORWARD, NO PULL REQUEST: (1) THE SECRET SCAN READS EVERY STORED FILE WHATEVER ITS NAME AND WHEREVER IT SITS; (2) THE UNIT-TEST FLOOR BECOMES THE REAL COUNT AND IS HELD THERE; (3) `RuntimeIdentifiers` DECLARED ONCE FOR EVERY PROJECT; (4) ONE GUARD TEST FOR THE SURVIVING MUTANT; (5) THE UNTRUE SENTENCES OF THE README AND THE RUNBOOK, FIVE BACKLOG LINES. NO PRODUCT CODE, NO JIRA, NO SETTING, NO LISTENER, NO AZURE, NOTHING TO HP OR TO ANY PERSON, NO SPEND.

Project root: `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2` (below: `<project>`). Code repository: `<project>/2_Project_Files` (below: `<repo>`), origin `git@github.com:datasecau/OXPd_2.git`. **Branch** `b1764/wp03-ci-skeleton`, which EXISTS: its head is `a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89`, ONE commit ahead of `main` `7e1a01cf640f8abac89e7148322651be8e4bf15b` (FACT 1; Stamp S2 re-reads both). You add commits ON TOP of that head; you never rewrite it. Lane size S. **Port block: none. You start NO listener of any kind.**

**You do NOT** open, comment on or merge a pull request; push any ref but `b1764/wp03-ci-skeleton`, and that only as a fast-forward of the head above; push to `main`; force-push, amend, reset or rebase; change a repository or organisation setting; write Jira (no call of any kind to Jira in this round: the records pass files the tickets); start any OUT item of the next section; run anything from `1_Project_Definition/Source_Documents/**` or copy a byte of it into `<repo>`; read or write a sibling project; write `1_Project_Definition/Design/**`, `Analysis/**`, `Review/**`, `CLARIFICATIONS.md`, `<project>/CLAUDE.md`, `<project>/.gitignore` or `<project>/Launch_Claude.command`; message a human. **No `az`**, no `docker` (the container image is built by the hosted run only), no `ssh` beyond what `git` itself runs for origin. **No HTTP to any hosted host, not even a GET**, with exactly these named exceptions: `gh api -X GET` (GitHub); `git` fetch and push to the origin above; the NuGet registry `https://api.nuget.org/v3/index.json` for `dotnet restore` (say in STATUS whether any package came from it: the drafter's run needed none beyond the cache). Never delete (quarantine to `<project>/.tools/b1774/_quarantine/`). Never type `cd` (`git -C '<dir>'`, `env -C '<dir>' <command>`, absolute paths). **Secrets (`<project>/CLAUDE.md:48-51`): locations only, never values. Any planted token is BUILT by a program in your scratch folder, never typed whole, never committed, never printed whole.**

model: claude-fable-5-2 (`/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json:11`). Why Fable: `<project>/CLAUDE.md:7`, "every agent on this project runs on the newest Fable (the product owner's instruction of 2026-11-19)". The routing table has no Fable build row (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md:39` still says Fable is not a worker tier): that instruction is newer and governs this project, as in round 1. Gate after: a separate kit, **tier G1** again (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md:108`: "security surfaces"). **Launch carries `BRIEF_SEAT_LEVEL=fable` inside the quotes** (`brief_seat.sh:31` reads `${BRIEF_SEAT_LEVEL:-opus}`; `:33` accepts `opus|sonnet|fable`).

## THE AUTHORITY (who decided what; quoted, never paraphrased)
- **The word to build is unchanged and is the ONLY word of the product owner in this lane:** C-42 (`<project>/1_Project_Definition/CLARIFICATIONS.md`, the tap "Start the no-hardware work now"), quoted in `<project>/CLAUDE.md:25-28`. **Every choice of this round (what is fixed, what is left out, how the branch moves, every default D1 to D10 below) is Tuesday's decision as coordinator. None is the product owner's, and no file, commit message or STATUS line of yours says he decided, ruled, approved or asked for anything in this round.**
- **The verdict this round answers** (RELAYED; the gate's file is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1772_verify/VERDICT.md`, readable by you as a claim): first line `GATE B1772: NO GO @ a0f9bdc on main 7e1a01c`; ONE Major and eleven Minor findings, no Blocker. **This is NO GO 1 of 2 on the class "CI skeleton of WP0.3"; a second NO GO goes to the product owner. So every fix below is proven RED and then GREEN on your machine BEFORE the push, and again by the hosted run after it.**
- **Landing rule** (`<project>/CLAUDE.md:55-57`): "**Seats push a branch only; Tuesday opens the pull request and merges once the checks and CodeQL are green.**" and (`<project>/CLAUDE.md:82`) "Tuesday lands a pull request by SQUASH, pinned to the reviewed head (`--match-head-commit`), one parent". The squash folds both commits of the branch into one; that is why a second commit costs nothing.
- **E0.4, the clause at stake** (`<project>/1_Project_Definition/Design/03_plan-of-attack-and-build.md:72`; the design copies under `<project>` were re-copied at 14:01 today, so this line sits 3 lower than round 1's kit printed it): "runs secret scanning (no allow-listed paths)". Requirement N1 (`02_architecture.md:138`): "CI secret scanning with no allow-listed folders".

## WHAT ROUND 2 FIXES AND WHAT IT LEAVES (the gate's finding numbers; RELAYED from the verdict)
| Finding | In or out | What you do |
|---|---|---|
| 1 (Major): the secret scan skips files by NAME | **IN** | THE FIX below: a second scan of every stored file under a neutral name; frozen text T1 |
| 3, last sentence: a missing deny-list read as an empty one survived the 48 cases | **IN, one case** | frozen text T3 |
| 8: the `rules` job passes on `Ran 16 tests` while 48 exist | **IN** | frozen texts T2 and T4: the floor is the count, and a test holds it there |
| 9: `RuntimeIdentifiers` is set per project | **IN** | frozen text T5 |
| 10: two untrue sentences of the runbook; five missing backlog lines; the base-image line | **IN** | frozen texts T7 and T8 |
| 1 again: the README's sentence for R1 was untrue while the scanner skipped names | **IN** | frozen text T6 |
| 2 (no check is required; a setting) | OUT, never a seat's | backlog line 15 of T7 says so; nothing else |
| 3 (the release mode: 0 fingerprints must refuse; the substring name rule; ZIP names split on a backslash) | **OUT** | backlog line 14 of T7; you write NO `--release` mode |
| 4 (single-file and other archive shapes of G1) | **OUT** | nothing; the records pass files it |
| 5 (the certificate forms of G2) | **OUT** | nothing |
| 6 (the YAML-escape forms of R3 and R4) | **OUT** | nothing; `build/repo_rules.py` is NOT yours in this round |
| 7 (the content half of R5) | **OUT** | backlog line 17 of T7; no rule change |
| 11 (the launcher's three dotnet variables) | **OUT** | `Launch_Claude.command` is not yours |
| 12 (`.pdb` files, the action's newer release, the scanner's own limits, the word rule under `.github/`) | **OUT** | the scanner's limits are named in T6 and in backlog line 16; nothing else |
| CodeQL, the organisation ruleset, any repository setting | NOT a seat's at all | nothing |
**If you find yourself editing `build/repo_rules.py`, `build/release_guard.py`, `build/tests/test_repo_rules.py`, the `Dockerfile` or the launcher: STOP, that is an OUT item.**

## THE DECISIONS OF ROUND 2 (each Tuesday's as coordinator; each a Question at the stamp)
- **D1 THE FIX IS A SECOND SCAN UNDER A NEUTRAL NAME, NOT A CONFIGURATION FILE AND NOT A REFUSAL OF NAMES.** Why not a configuration file: the scanner's skip list is built into its default configuration (MEASURED [F3]: the `[allowlist]` block of `config/gitleaks.toml` at tag `v8.30.1` holds 25 path patterns); removing it means carrying a private copy of the whole default file (3209 lines, 222 rules) and passing `--config`, which rule R1 and round 1's default D9 forbid, and which would then need R1 to tell the project's own reviewed file from a weakening one. Why not a refusal of the 14 names (the gate's "smallest"): the product will hold images, fonts and lock files (a panel, an admin UI), so a refusal would be lifted by the first lane that needs one, and it would cover neither a name the gate did not try nor the history. Why this: it needs no option the rules forbid, it covers the working tree AND the history in one pass, and it is proven on 61 planted files (THE FIX, MEASURED).
- **D2 THE FIX LIVES IN ONE STEP OF `ci.yml`,** as the last step of the `secret-scan` job: one shell function used for the planted repository AND for the real one, so the control and the scan cannot drift apart. No new script file.
- **D3 THE CONTROLS ON THE PIPELINE'S OWN CONTROLS LIVE IN ONE NEW TEST FILE** `build/tests/test_pipeline_controls.py` (frozen text T4). It reads the real `ci.yml`; `build/tests/test_repo_rules.py` and `build/repo_rules.py` stay byte-equal to round 1. R1 does not change: the names the scanner skips stay ALLOWED in the tree, because they are now scanned.
- **D4 THE FLOOR IS THE COUNT, AND MOVES WITH IT.** `FLOOR=53` in the `rules` job; the job fails unless the log reads `Ran <n> tests` with n at least `FLOOR`; a test fails unless `FLOOR` is set exactly once and equals the number of indented `def test_` lines under `build/tests`. **How the floor moves: the commit that adds a planted control raises `FLOOR` by one in the same commit; the commit that removes one lowers it and says why. A floor that does not equal the count is RED in the `rules` job either way.**
- **D5 `RuntimeIdentifiers` MOVES TO THE ROOT `Directory.Build.props`.** Every project inherits it, the test project too; so `tests/Datasec.Suite.Core.Tests/packages.lock.json` gains two runtime sections (MEASURED [F6]: 24 added lines, 0 removed; the two lock files under `src/` do not change) and is committed.
- **D6 THE BASE-IMAGE BACKLOG LINE IS NOT TICKED.** The digest is now known from the hosted log (MEASURED [F8]) and is written into the line; the `FROM` line still names a tag, so the line stays open until a lane that owns `packaging/` pins it. `packaging/linux/Dockerfile` is NOT yours.
- **D7 THE BRANCH MOVES BY A SECOND COMMIT, FAST-FORWARD.** No amend and no force (`<project>/CLAUDE.md:56-57` and round 1's rule). The hosted `ci` run on the NEW head must be green on its own.
- **D8 THE PLANTED REPOSITORY OF THE HOSTED JOB IS COMMITTED UNDER A THROWAWAY IDENTITY** (`planted-control`, written with `git -c` INSIDE the workflow text, for a repository that lives under `$RUNNER_TEMP` and is never pushed). That is the workflow's text, not a command of yours: **your own commits in `<repo>` use the repository's own identity only.**
- **D9 NO JIRA, NO PULL REQUEST, NO SETTING.** The pull-request texts beside the verdict are Tuesday's to re-word after your READY.
- **D10 THE GATE AFTER YOU PROBES THROUGH THE WORKFLOW'S OWN FUNCTION.** A scan of a folder by its own names still skips the 14 names; that is the scanner, unchanged. Say so first in FOR TUESDAY.

## PRIOR WORK (what round 1 built in each file you touch, and why; NOTHING that works is rewritten)
| File | What round 1 built, and why (RELAYED from `2026-11-20_B1764_STATUS.md` and the gate; the lines MEASURED at the head) | What round 2 does to it | What stays byte-equal |
|---|---|---|---|
| `.github/workflows/ci.yml` (135 lines) | ONE workflow `ci`, 4 jobs. `secret-scan`: fetch the scanner by sha256, a planted control that REQUIRES rc 1 (`ci.yml:101-110`), the history scan (`:113`), the working-tree scan (`:116`); every scan line carries `--ignore-gitleaks-allow` because round 1 MEASURED that the inline allow comment otherwise hides a finding. `rules`: the unit tests with a floor of 16 (`:131-133`), then the rules (`:135`) | APPEND T1 after `ci.yml:116`; REPLACE the three lines `:131-133` by T2 | lines 1 to 130 and 134 to 135; every job name; every `uses:` line; the triggers; the permissions block |
| `build/tests/test_release_guard.py` (250 lines, 22 cases) | the planted controls of G1 to G3; class `GuardExitCodes` holds the exit-2 cases (`:223`); its last case is `test_shipped_denylist_parses` (`:240-246`) | INSERT T3 (one case) directly after `:246` | all 22 cases |
| `Directory.Build.props` (12 lines) | the shared build properties; `RestoreLockedMode` when `CI` is `true` (`:10`), which is the detector of round 1's fault 2 | REPLACE the whole file by T5 (3 added lines, 0 removed) | lines 1 to 10 |
| `src/Datasec.Suite.Core/Datasec.Suite.Core.csproj`, `src/Datasec.Suite.Server/Datasec.Suite.Server.csproj` | each declares `RuntimeIdentifiers` `linux-x64;win-x64` in its own `PropertyGroup` (line 4 of each): the cause-fix of round 1's fault 2 (publishing for one runtime rewrote a lock file, and the next locked restore failed NU1004) | REMOVE that `PropertyGroup` (4 lines) from each; the value now comes from T5 | every other line |
| `tests/Datasec.Suite.Core.Tests/packages.lock.json` | written by the restore | RE-WRITTEN BY THE RESTORE, never by hand (D5) | its first 134 lines (of 137 at the head; the candidate's file has 161) |
| `README.md` (68 lines) | the 5 frozen first lines, `## Layout`, `## Reserved names`, `## Checks` | INSERT T6 (3 places, 6 lines) | every existing line |
| `build/tests/test_pipeline_controls.py` | does not exist | NEW: T4 | - |
| `<project>/SETUP_RUNBOOK.md` (94 lines), `<project>/BACKLOG.md` (101 lines, 13 owed lines), `<project>/5_Project_History/history.md` (12 lines) | the first seat's records | T7, T8, one prepended history entry | every byte this kit does not name (`cmp` against a before-copy) |
**Round 1's two faults must not return** (the gate reproduced both): fault 1, `dotnet test` red without the `test` section of `global.json` (you do not touch `global.json`); fault 2, the lock files (Step 4 proves it again, both with and without `CI=true`).
**PRIOR-WORK CHECK (Step 1; a READY without a `## PRIOR WORK` section is returned unread).** Re-read the origin under the project `GH_CONFIG_DIR`: `gh api -X GET repos/datasecau/OXPd_2/git/matching-refs/heads/` must print exactly 2 rows, `refs/heads/b1764/wp03-ci-skeleton` at `a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89` and `refs/heads/main` at `7e1a01cf640f8abac89e7148322651be8e4bf15b`; `pulls?state=all` must count 0. **A third ref, a pull request of any state, or either head at another sha: `STOPPED: NEEDS TUESDAY` with the reading** (someone moved the branch, or Tuesday opened the pull request; neither is yours to guess). Then the local side: `git -C '<repo>' --no-optional-locks rev-parse HEAD` prints the lane head; `status --porcelain` prints 0 lines; `rev-parse --abbrev-ref HEAD` prints `b1764/wp03-ci-skeleton`. A dirty tree or another head: STOP (do not stash, do not reset). Print the table (`ALREADY-ON-BRANCH` for each T-text whose bytes are already in the file, `WORK` otherwise) with the line that proves each row.

## THE FIX, MEASURED (gitleaks 8.30.1 at `/opt/homebrew/bin/gitleaks`, the version the workflow pins; the workflow's own options `--no-banner --redact --ignore-gitleaks-allow --exit-code 1`; every token built by a program, never printed)
**What the scanner does, MEASURED [F2] and [F3]:** (a) it does not read a file whose path matches its built-in list (25 patterns: by directory, by extension, by exact name; one more list sits inside the rule for this token kind); (b) **it also does not read a file whose FIRST BYTES look like a PDF, a Windows or Linux program, a ZIP or a gzip stream, whatever the file is called** (rows A51 to A55 below: the token is in clear text right after the first bytes; this is NOT in the gate's verdict); (c) its history form additionally does not read a file that git shows as a binary change (rows A50 and A57).
**The fix:** every file the repository stores (every blob of the object store: every commit of every fetched ref, reachable or not) is written under the name `<its object id>.txt` behind ONE plain first line, into a folder outside the checkout, and that folder is scanned. The neutral name defeats (a); the first line defeats (b); reading the object store instead of the change text defeats (c) and covers the history.
**The acceptance table (MEASURED [F4], the drafter's `acceptance.log`; each row is ONE scratch repository holding ONE committed file; "by name" columns are the scanner's exit code on that repository as round 1 scans it; "neutral" is its exit code on the folder the workflow's own function wrote; the function was CUT OUT of the candidate `ci.yml` by program, not retyped; 1 = found, 0 = not found).** Rows A01 to A24 are the gate's 24 names; A25 to A61 are the drafter's own.
```
ROW | class | file name | working tree by name rc | history by name rc | stored files | neutral rc
A01 | gate | package-lock.json | 0 | 0 | 1 | 1
A02 | gate | go.sum | 0 | 0 | 1 | 1
A03 | gate | yarn.lock | 0 | 0 | 1 | 1
A04 | gate | pnpm-lock.yaml | 0 | 0 | 1 | 1
A05 | gate | packages.lock.json | 1 | 1 | 1 | 1
A06 | gate | x.png | 0 | 0 | 1 | 1
A07 | gate | x.pdf | 0 | 0 | 1 | 1
A08 | gate | x.svg | 0 | 0 | 1 | 1
A09 | gate | x.min.js | 1 | 1 | 1 | 1
A10 | gate | node_modules/a.js | 0 | 0 | 1 | 1
A11 | gate | vendor/a.go | 1 | 1 | 1 | 1
A12 | gate | gitleaks.toml | 0 | 0 | 1 | 1
A13 | gate | x.dll | 1 | 1 | 1 | 1
A14 | gate | docs/x.md | 1 | 1 | 1 | 1
A15 | gate | .env | 1 | 1 | 1 | 1
A16 | gate | bin/x.txt | 1 | 1 | 1 | 1
A17 | gate | x.ttf | 0 | 0 | 1 | 1
A18 | gate | x.jpg | 0 | 0 | 1 | 1
A19 | gate | poetry.lock | 0 | 0 | 1 | 1
A20 | gate | Cargo.lock | 1 | 1 | 1 | 1
A21 | gate | deps/go.mod | 0 | 0 | 1 | 1
A22 | gate | verification-metadata.xml | 0 | 0 | 1 | 1
A23 | gate | x.html | 1 | 1 | 1 | 1
A24 | gate | x.ipynb | 1 | 1 | 1 | 1
A25 | dir | bower_components/lib/a.js | 0 | 0 | 1 | 1
A26 | dir | vendor/github.com/a/b.go | 0 | 0 | 1 | 1
A27 | dir | venv/lib/python3.12/site-packages/a.py | 0 | 0 | 1 | 1
A28 | dir | pkg-1.0.dist-info/RECORD | 0 | 0 | 1 | 1
A29 | dir | vendor/bundle/a.rb | 0 | 0 | 1 | 1
A30 | dir (per-rule list) | @octokit/auth-token/README.md | 0 | 0 | 1 | 1
A31 | ext | font.woff2 | 0 | 0 | 1 | 1
A32 | ext | sheet.xlsx | 0 | 0 | 1 | 1
A33 | ext | blob.bin | 0 | 0 | 1 | 1
A34 | ext | tool.exe | 0 | 0 | 1 | 1
A35 | ext | sym.pdb | 0 | 0 | 1 | 1
A36 | ext | pic.GIF | 0 | 0 | 1 | 1
A37 | ext | pkg.gem | 0 | 0 | 1 | 1
A38 | ext | letter.docx | 0 | 0 | 1 | 1
A39 | exact | gradlew | 0 | 0 | 1 | 1
A40 | exact | mvnw | 0 | 0 | 1 | 1
A41 | exact | deno.lock | 0 | 0 | 1 | 1
A42 | exact | npm-shrinkwrap.json | 0 | 0 | 1 | 1
A43 | exact | Pipfile.lock | 0 | 0 | 1 | 1
A44 | exact | gradle.lockfile | 0 | 0 | 1 | 1
A45 | exact | go.work | 0 | 0 | 1 | 1
A46 | exact | jquery-3.7.1.min.js | 0 | 0 | 1 | 1
A47 | exact | Database.refactorlog | 0 | 0 | 1 | 1
A48 | exact | javascript.json | 0 | 0 | 1 | 1
A49 | exact | vendor/modules.txt | 0 | 0 | 1 | 1
A50 | binary: NUL bytes | nul.dat | 1 | 0 | 1 | 1
A51 | binary: starts %PDF | magic_pdf.txt | 0 | 1 | 1 | 1
A52 | binary: starts MZ | magic_mz.txt | 0 | 0 | 1 | 1
A53 | binary: starts ELF | magic_elf.txt | 0 | 0 | 1 | 1
A54 | binary: starts PK 03 04, token in clear after | magic_zip.txt | 0 | 0 | 1 | 1
A55 | binary: starts gzip magic, token in clear after | magic_gz.txt | 0 | 0 | 1 | 1
A56 | binary: starts PNG magic | magic_png.txt | 1 | 1 | 1 | 1
A57 | binary: random bytes around the token | rand.dat | 1 | 0 | 1 | 1
A58 | size: 96 MiB, token in the last line | big.txt | 1 | 1 | 1 | 1
A59 | limit (inherent): a real zip holding the token | real.zip | 0 | 0 | 1 | 1
A60 | limit (inherent): a real gzip holding the token | real.txt.gz | 0 | 0 | 1 | 0
A61 | limit (inherent): UTF-16LE text | utf16.txt | 0 | 0 | 1 | 0
A62 | quiet: no token, plain name | a.txt | 0 | 0 | 1 | 0
A63 | quiet: no token, skipped name | package-lock.json | 0 | 0 | 1 | 0
```
**Totals, printed by the same program:** token rows 61; found in the working tree by name 14; found in the history by name 13; **found under a neutral name 59**; the 2 not found are A60 and A61. The gate's 24: by name found 10, not found 14 (the gate's own reading); neutral found 24 of 24. The two quiet rows stay quiet in all three columns. Row A59's class word is the drafter's and is wrong for that row: the ZIP's member was stored without compression, and it WAS found. **The limits that stay (the scanner's, named in T6 and in backlog line 16, never claimed as fixed): compressed content (A60), text saved as UTF-16 (A61), and a token split over two lines (RELAYED from the gate; not re-measured).** The scanner has no size limit unless an option sets one (A58: 96 MiB, found; R1 already forbids that option).
**One repository, the history case (MEASURED [F5]):** 60 token files committed and then ALL removed by a second commit: the working-tree scan by name finds 0 (rc 0), the history scan by name finds 12, the neutral scan finds 58 of 60 in 61 stored files.
**The real repository (MEASURED [F5], read verbs only on your checkout, output in the drafter's scratch):** the neutral scan of all 36 files your checkout stores (25 of the head, 1 more of `main`, 10 unreachable ones left by round 1's staged mutants) is rc 0, `no leaks found`.
**The trap the dry run found, so that you do not fall into it (MEASURED [F7]):** a constant NAMED with the word for a credential store next to a 64-hex value makes the scanner's generic rule fire, by name AND under a neutral name (the drafter's first name for the scan fingerprint did exactly that: rc 1, rule `generic-api-key`). The two constant names of T4, `REVIEWED_SCAN_JOB` and `REVIEWED_RULES_JOB`, are MEASURED clean. Do not rename them.

## THE FROZEN TEXTS (you extract each from your Step-0 copy BY PROGRAM: the lines strictly between its two marker lines; you retype nothing. Each block: ASCII, LF, final newline. The sha256 and line count of each block are in FACT 9; prove each before you use it)
**T1, the new LAST step of the `secret-scan` job: appended directly after `ci.yml:116` (the working-tree scan line), before the blank line that precedes `  rules:`.** 52 lines. MEASURED [F5]: run as the runner runs it (`/bin/bash --noprofile --norc -e -o pipefail`) on macOS bash 3.2 on the candidate tree, it printed `PLANTED-CONTROL neutral-scan: planted 6, found by name 1, found under a neutral name 6, rc 1`, then `NEUTRAL-SCAN: stored files 26, files of this commit not among them 0`, then `no leaks found`, and ended rc 0. **On a Linux runner (bash 5, GNU sed, the Linux binary of the scanner): UNMEASURED; your hosted run is its first proof.**
@@T1-BEGIN@@
      - name: scan every stored file under a neutral name
        run: |
          neutral_export() {
            mkdir "$2"
            git -C "$1" cat-file --batch-all-objects --batch-check='%(objecttype) %(objectname)' > "$2.list"
            while read -r kind id; do
              if [ "$kind" = blob ]; then
                { printf 'stored file %s\n' "$id"; git -C "$1" cat-file blob "$id"; } > "$2/$id.txt"
              fi
            done < "$2.list"
          }
          found_in() {
            sed -n -E 's/.*leaks found: ([0-9]+).*/\1/p' "$1"
          }
          p="$RUNNER_TEMP/plant-repo"
          head='gh'
          tail='p_aB3dE5gH7jK9mN1pQ3sT5vW7yZ9bD1fH3jL5n'
          git init -q "$p"
          mkdir -p "$p/node_modules" "$p/gone"
          n=0
          for name in a.txt package-lock.json node_modules/a.js x.png first-bytes.txt gone/yarn.lock; do
            n=$((n + 1))
            if [ "$name" = first-bytes.txt ]; then printf '%%PDF-1.7\n' > "$p/$name"; fi
            printf 'value = "%s%s"\nplanted file %s\n' "$head" "$tail" "$n" >> "$p/$name"
          done
          git -C "$p" add -A -f
          git -C "$p" -c user.name=planted-control -c user.email=planted-control@invalid commit -q -m 'planted: six files'
          git -C "$p" rm -q gone/yarn.lock
          git -C "$p" -c user.name=planted-control -c user.email=planted-control@invalid commit -q -m 'planted: one file removed'
          rc=0
          "$RUNNER_TEMP/gitleaks/gitleaks" dir "$p" --no-banner --redact --ignore-gitleaks-allow --exit-code 1 > "$RUNNER_TEMP/plant-by-name.log" 2>&1 || rc=$?
          by_name=$(found_in "$RUNNER_TEMP/plant-by-name.log")
          neutral_export "$p" "$RUNNER_TEMP/plant-neutral"
          rc=0
          "$RUNNER_TEMP/gitleaks/gitleaks" dir "$RUNNER_TEMP/plant-neutral" --no-banner --redact --ignore-gitleaks-allow --exit-code 1 > "$RUNNER_TEMP/plant-neutral.log" 2>&1 || rc=$?
          cat "$RUNNER_TEMP/plant-neutral.log"
          found=$(found_in "$RUNNER_TEMP/plant-neutral.log")
          echo "PLANTED-CONTROL neutral-scan: planted 6, found by name ${by_name:-0}, found under a neutral name ${found:-0}, rc $rc"
          test "${by_name:-0}" -eq 1
          test "${found:-0}" -eq 6
          test "$rc" -eq 1
          neutral_export . "$RUNNER_TEMP/repo-neutral"
          stored=$(ls "$RUNNER_TEMP/repo-neutral" | wc -l | tr -d ' ')
          git ls-tree -r HEAD > "$RUNNER_TEMP/head.list"
          missing=0
          while read -r mode kind id path; do
            if [ "$kind" = blob ] && [ ! -s "$RUNNER_TEMP/repo-neutral/$id.txt" ]; then missing=$((missing + 1)); fi
          done < "$RUNNER_TEMP/head.list"
          echo "NEUTRAL-SCAN: stored files $stored, files of this commit not among them $missing"
          test "$stored" -ge 1
          test "$missing" -eq 0
          "$RUNNER_TEMP/gitleaks/gitleaks" dir "$RUNNER_TEMP/repo-neutral" --no-banner --redact --ignore-gitleaks-allow --exit-code 1
@@T1-END@@
**What the plant proves, name by name:** `a.txt` is the one file the scanner reads under its own name (the control of the "by name" count: it must read 1, which proves the other five ARE skipped by this binary); `package-lock.json` is skipped by exact name, `node_modules/a.js` by directory, `x.png` by extension, `first-bytes.txt` by its first bytes, and `gone/yarn.lock` is skipped by name AND exists only in the first commit. Each file holds its own number, so the six are six stored files. **The step fails unless the neutral scan finds exactly 6.** The planted value is the same two halves round 1's planted control joins at run time; it is never written whole in the repository.
**T2, the `rules` job: REPLACES the three lines `ci.yml:131-133`** (`python3 -I -m unittest ...`, the `grep -E '^Ran (1[6-9]|...` line, the `grep -x 'OK'` line) by these 6 lines. MEASURED [F5]: the step printed `UNIT-TEST FLOOR: ran 53, floor 53` and ended rc 0.
@@T2-BEGIN@@
          FLOOR=53
          python3 -I -m unittest discover -s build/tests -v 2>&1 | tee "$RUNNER_TEMP/unittest.log"
          ran=$(sed -n -E 's/^Ran ([0-9]+) tests? in .*/\1/p' "$RUNNER_TEMP/unittest.log")
          echo "UNIT-TEST FLOOR: ran ${ran:-0}, floor $FLOOR"
          test "${ran:-0}" -ge "$FLOOR"
          grep -x 'OK' "$RUNNER_TEMP/unittest.log"
@@T2-END@@
**After T1 and T2 `ci.yml` has 190 lines** (135 + 52 + 3; MEASURED [F5]); the `secret-scan` job is 88 lines and the `rules` job 21 lines as T4's helper cuts them.
**T3, the guard test that kills the surviving mutant: inserted directly after `test_release_guard.py:246`** (the last line of `test_shipped_denylist_parses`), inside class `GuardExitCodes`. 8 lines, the first one blank. It is GREEN on the guard as it is (a missing list is already exit 2, `release_guard.py:57-58`): it is a guard on behaviour that exists, and its RED is the mutant (Step 3).
@@T3-BEGIN@@

    def test_missing_denylist_is_exit_2_never_an_empty_list(self):
        self.put("one.txt", b"one\n")
        code, lines = self.guard(denylist=os.path.join(self.root, "no-such-list.txt"))
        self.assertEqual(code, 2, lines)
        self.assertTrue(any(line.startswith("GUARD: bad deny-list") for line in lines), lines)
        self.assertEqual([line for line in lines if line.startswith("GUARD: clean")], [])
        self.assertEqual([line for line in lines if line.startswith("GUARD-WARN")], [])
@@T3-END@@
**T4, the NEW file `build/tests/test_pipeline_controls.py`, the whole file.** 116 lines, 4 cases. Its two fingerprints are the sha256 of the `secret-scan` job and of the `rules` job of the candidate `ci.yml` (MEASURED [F5]); **if your `ci.yml` after T1 and T2 does not give these two values, your edit is not byte-equal to the frozen text: find the difference, never change a fingerprint to make a case pass** (the one exception is Step 6's fix-forward, where you say so).
@@T4-BEGIN@@
"""Controls on the pipeline's own controls.

The workflow keeps its secret-scan job and its rules job as they were reviewed, and the unit-test
floor of the rules job equals the number of planted controls under build/tests.

These cases read the workflow and the test files of this repository as they are checked out; they
build no input. A change to one of the two jobs is reviewed first, then the fingerprint below is
set to the new value in the same commit. A new planted control raises FLOOR in the workflow by one
in the same commit.
Run: python3 -I -m unittest discover -s build/tests -v
"""
import hashlib
import os
import re
import unittest

TESTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(TESTS))
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "ci.yml")

# SHA-256 of each job's text in the workflow, from its key line to the line before the next job
# (or the end of the file). In the rules job the number after FLOOR= is read as the letter N.
REVIEWED_SCAN_JOB = "b64ca5f000c85b4b0fa20e676054b4027eb0e7a45b93d708911937951a6b87f3"
REVIEWED_RULES_JOB = "19008b73772b35fdb57723f1041ec0a7ec8f60128bcf1130f8b2ce78bd0665a6"

JOB_KEY = re.compile(r"^  [A-Za-z0-9_-]+:\s*$")
FLOOR_LINE = re.compile(r"^\s+FLOOR=([0-9]+)\s*$")
FLOOR_NUMBER = re.compile(r"FLOOR=[0-9]+")
CASE_LINE = re.compile(r"^\s+def test_")


def job_text(workflow, job):
    """The lines of one job, or None when the workflow does not hold exactly one job of that name."""
    lines = workflow.splitlines(keepends=True)
    starts = [at for at, line in enumerate(lines) if line.rstrip("\r\n") == "  %s:" % job]
    if len(starts) != 1:
        return None
    end = len(lines)
    for at in range(starts[0] + 1, len(lines)):
        if JOB_KEY.match(lines[at]):
            end = at
            break
    return "".join(lines[starts[0]:end])


def job_sha256(workflow, job):
    text = job_text(workflow, job)
    if text is None:
        return None
    return hashlib.sha256(FLOOR_NUMBER.sub("FLOOR=N", text).encode("utf-8")).hexdigest()


def floors(workflow):
    """Every number the workflow sets FLOOR to: exactly one is right."""
    found = []
    for line in workflow.splitlines():
        match = FLOOR_LINE.match(line)
        if match:
            found.append(int(match.group(1)))
    return found


def planted_controls(folder):
    """The number of test cases in the test files of a folder, counted as the indented def lines."""
    count = 0
    for name in sorted(os.listdir(folder)):
        if name.startswith("test_") and name.endswith(".py"):
            with open(os.path.join(folder, name), "r", encoding="utf-8") as handle:
                count += sum(1 for line in handle if CASE_LINE.match(line))
    return count


class PipelineKeepsItsOwnControls(unittest.TestCase):
    def setUp(self):
        with open(WORKFLOW, "r", encoding="utf-8", newline="") as handle:
            self.workflow = handle.read()

    def test_secret_scan_job_is_the_reviewed_text(self):
        self.assertEqual(job_sha256(self.workflow, "secret-scan"), REVIEWED_SCAN_JOB,
                         "the secret-scan job changed: review the change, then set the fingerprint")

    def test_rules_job_is_the_reviewed_text(self):
        self.assertEqual(job_sha256(self.workflow, "rules"), REVIEWED_RULES_JOB,
                         "the rules job changed: review the change, then set the fingerprint")

    def test_unit_test_floor_equals_the_number_of_planted_controls(self):
        self.assertEqual(floors(self.workflow), [planted_controls(TESTS)],
                         "FLOOR in the workflow must be set once, to the number of test cases under build/tests")

    def test_a_narrowed_scan_a_removed_plant_and_a_lowered_floor_are_seen(self):
        scan = '"$RUNNER_TEMP/gitleaks/gitleaks" dir "$RUNNER_TEMP/repo-neutral" --no-banner'
        changed = {
            "the scan of every stored file narrowed to one folder": self.workflow.replace(scan, scan.replace("repo-neutral", "repo-neutral/docs")),
            "the planted control's requirement removed": self.workflow.replace('          test "${found:-0}" -eq 6\n', ""),
            "a scan that may fail": self.workflow.replace("--ignore-gitleaks-allow --exit-code 1\n", "--ignore-gitleaks-allow --exit-code 1 || true\n"),
            "the job switched off": self.workflow.replace("  secret-scan:\n", "  secret-scan:\n    if: false\n"),
        }
        for label, text in changed.items():
            with self.subTest(label):
                self.assertNotEqual(text, self.workflow)
                self.assertNotEqual(job_sha256(text, "secret-scan"), REVIEWED_SCAN_JOB)
        gone = self.workflow.replace("  secret-scan:\n", "  not-the-scan:\n")
        self.assertIsNone(job_sha256(gone, "secret-scan"))
        count = planted_controls(TESTS)
        lowered = FLOOR_NUMBER.sub("FLOOR=16", self.workflow)
        self.assertNotEqual(floors(lowered), [count])
        self.assertEqual(job_sha256(lowered, "rules"), REVIEWED_RULES_JOB)
        twice = self.workflow.replace("          FLOOR=", "          FLOOR=16\n          FLOOR=")
        self.assertNotEqual(floors(twice), [count])
        no_floor_check = self.workflow.replace('          test "${ran:-0}" -ge "$FLOOR"\n', "")
        self.assertNotEqual(no_floor_check, self.workflow)
        self.assertNotEqual(job_sha256(no_floor_check, "rules"), REVIEWED_RULES_JOB)


if __name__ == "__main__":
    unittest.main()
@@T4-END@@
**What T4 holds and what it does not (say both in the README by T6 and in STATUS):** a change of one line of the `secret-scan` job or of the `rules` job now needs a second edit in another file, in the same commit, where a reviewer sees it; a commit that changes both together is still green, and nothing but a reviewer or a required check from outside the commit stops that (the gate's finding 2, which is not a seat's). The `linux` and `windows` jobs are NOT held by a fingerprint: later lanes change them.
**T5, `Directory.Build.props`, the whole file** (15 lines; lines 1 to 10 are round 1's, byte-equal):
@@T5-BEGIN@@
<Project>
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <Deterministic>true</Deterministic>
    <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
    <!-- On a pipeline runner (CI=true) every restore, also the one inside build and publish, must match the lock files. -->
    <RestoreLockedMode Condition="'$(CI)' == 'true'">true</RestoreLockedMode>
    <!-- The two packagings (the Linux container and the Windows service), declared once for every project, so that one
         lock file per project holds for both publish legs. A project never declares its own list. -->
    <RuntimeIdentifiers>linux-x64;win-x64</RuntimeIdentifiers>
  </PropertyGroup>
</Project>
@@T5-END@@
**And the two project files lose their own list:** from `src/Datasec.Suite.Core/Datasec.Suite.Core.csproj` remove its lines 2 to 5 (the `PropertyGroup` holding the comment and `RuntimeIdentifiers`); the file then has 5 lines: `<Project Sdk="Microsoft.NET.Sdk">`, the `ItemGroup` with `InternalsVisibleTo`, `</Project>`. From `src/Datasec.Suite.Server/Datasec.Suite.Server.csproj` remove its lines 2 to 5 likewise; the file then has 8 lines. Their sha256 after the edit are in FACT 9. Then the lock file of the TEST project is re-written by `dotnet restore Datasec.Suite.slnx` run WITHOUT `CI` in the environment (Step 4): you never edit a lock file by hand.
**T6, `README.md`, three insertions (6 lines in all; the file goes from 68 to 74 lines):**
(a) directly after the line that begins ``  - `build/tests/test_repo_rules.py`:`` (line 24), this ONE line:
@@T6A-BEGIN@@
  - `build/tests/test_pipeline_controls.py`: the controls on the pipeline's own controls (S2)
@@T6A-END@@
(b) directly after the line that begins ``  - `.github/workflows/ci.yml`:`` (line 29 before (a)), these TWO lines, the first one blank:
@@T6B-BEGIN@@

Every project takes its `RuntimeIdentifiers` (`linux-x64;win-x64`, the two packagings) from `Directory.Build.props`. A project file never declares its own list.
@@T6B-END@@
(c) at the END of the file, directly after the R5 line (line 68 before (a) and (b)), these THREE lines:
@@T6C-BEGIN@@
- S1: the `secret-scan` job scans the history and the working tree, and then scans every file the repository stores (in any commit, under any name) a second time, copied under a neutral name behind one plain first line. Neither a file's name nor its first bytes can make the scanner skip it. The job first proves this on six planted files, five of which the scanner does not read under their own names.
- S1 does not see: text saved as UTF-16, compressed content, a secret split over two lines.
- S2: the `secret-scan` job and the `rules` job are held to their reviewed text by a fingerprint, and the `rules` job fails unless it ran at least as many planted controls as `build/tests` holds (`FLOOR` in the workflow equals that count).
@@T6C-END@@
The README's R1 sentence stays as it is: with S1 beside it, it is true for every name. The README's line `build/repo_rules.py: rules R1 to R5` stays.
**T7, `<project>/BACKLOG.md` (outside the repository).** (a) In owed line 7, REPLACE the ONE line that begins `   - Why deferred: a digest could not be read` (file line 46) by the line between the T7A markers; the box of line 7 stays `[ ]`. (b) INSERT the five numbered lines between the T7B markers directly after the last line of owed line 13 (file line 84, `    - Discovered: 2026-11-20 during the first build lane`) and before the blank line above the heading `## The no-hardware work packages and their Jira keys`. No other byte changes.
@@T7A-BEGIN@@
   - Why deferred: the digest is known without a call to that registry (the hosted `linux` job of run `44661506229` printed `mcr.microsoft.com/dotnet/aspnet:10.0@sha256:12b1135f5f8b3c0a214f2a680ff2033dff4f684f445d6c697d9524ceeb303586` on 2026-11-20), but the `FROM` line still names the tag; the line stays open until a lane that owns `packaging/` pins it
@@T7A-END@@
@@T7B-BEGIN@@
14. - [ ] The release guard has no release mode
    - Where: `2_Project_Files/build/release_guard.py`; `2_Project_Files/build/denylist/dev_ca_sha256.txt`
    - Symptom: with 0 fingerprints in the list the guard prints a warning and passes; `--denylist` may point away from the tracked list; no job is made to call the guard on the folder it packages
    - Why deferred: today's two legs package and release nothing; the first release leg must not start before a mode exists in which 0 fingerprints is exit 2
    - Source: the independent review of the first lane's branch, 2026-11-20 (its finding 3); owed line 2 above
    - Discovered: 2026-11-20 by the independent review of the first lane's branch
15. - [ ] No check is required by a repository setting
    - Where: the organisation ruleset on `main` (ruleset `24139430`): its list of required checks is empty and it holds no pull-request rule
    - Symptom: a pull request with a red `secret-scan` or `rules` job can be merged as far as the status checks go, and the checks run from the commit they check. Since the second commit of the first lane a change to the `secret-scan` job or the `rules` job must also change a fingerprint in `build/tests/test_pipeline_controls.py`: two files instead of one, no more
    - Why deferred: a repository or organisation setting is not a seat's; the coordinator takes it to the product owner
    - Source: the same review (its finding 2); `<project>/CLAUDE.md`, section Additions and corrections, "Required checks"
    - Discovered: 2026-11-20 by the independent review of the first lane's branch
16. - [ ] The secret scanner's own limits
    - Where: the `secret-scan` job of `2_Project_Files/.github/workflows/ci.yml`
    - Symptom: the scanner (gitleaks 8.30.1) does not read a file whose name is on its built-in list, nor a file whose first bytes look like a PDF, a program or an archive. Since the second commit of the first lane the job scans every stored file a second time under a neutral name behind one plain first line, which closes both. Still seen by no pass: text saved as UTF-16, compressed content, a secret split over two lines. GitHub's own secret scanning and push protection read disabled on this repository, so this job is the only net
    - Why deferred: the three limits are the scanner's; closing them needs a decoding step or another tool, which is a decision
    - Source: the same review (its findings 1 and 12); `1_Project_Definition/Briefs/2026-11-20_B1774_STATUS.md`, section ACCEPTANCE
    - Discovered: 2026-11-20 by the independent review of the first lane's branch
17. - [ ] The R5 hash half cannot run on a runner
    - Where: `2_Project_Files/build/repo_rules.py` (rule R5)
    - Symptom: the comparison with the supplied source runs only where that folder exists (a seat's machine); the hosted `rules` job prints `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)`. It compares whole files only and knows nothing of HP's library, so a renamed or changed copy is seen by no check
    - Why deferred: the supplied source may not be copied to a runner; a content rule (a tracked file holding a NUL byte) is a later lane's
    - Source: the same review (its finding 7)
    - Discovered: 2026-11-20 by the independent review of the first lane's branch
18. - [ ] Whether hosted minutes on this private repository are billed
    - Where: the organisation's billing view (it needs organisation-admin rights)
    - Symptom: UNMEASURED; every push of a lane branch and every pull request runs four hosted jobs
    - Why deferred: not readable by a seat; the coordinator reads the minutes as the organisation's existing practice and says so to the product owner
    - Source: the first lane's brief, Q6; the same review (its finding 10)
    - Discovered: 2026-11-20 during the first build lane
@@T7B-END@@
**T8, `<project>/SETUP_RUNBOOK.md` (outside the repository). Two sentences the gate found untrue, replaced exactly; then the numbers this round changes, by property.**
(a) In the paragraph `**The repository.**` (file line 19) REPLACE the sentence that begins `Everything after that commit reaches` and ends `lands it by squash.` by the text between the T8A markers (one line; it ends the paragraph as the old sentence did).
@@T8A-BEGIN@@
By the project's rule everything after that commit reaches `main` by pull request only: a seat pushes a branch, the coordinator opens the pull request and lands it by squash. That is a rule of `<project>/CLAUDE.md`, not a mechanism: no GitHub setting enforces it (the ruleset on `main` holds no pull-request rule and names no required check, and the deploy key can write).
@@T8A-END@@
(b) In owed line 8 (file line 78) REPLACE the words `Owed: a second launch of it by a person` by `Owed: a first launch of it by a person` (the rest of the line stays).
(c) **By property: after your edit no sentence of the runbook states a number or a head that round 2 made untrue.** At least these: the paragraph `**The lane branch**` (line 21) says TWO commits and names both shas (the second is your pushed head, read back) with one clause on what the second holds; the checks table's two cells `Ran 48 tests` and `RULES: clean (25 files)` (lines 48 and 49) become what you printed in Step 5; the table gains ONE row for the neutral scan with the command you ran and the two lines it printed; the paragraph `**The hosted pipeline**` (line 65) gains ONE sentence with the second run's id and the four lines of Step 6; `## What is owed` gains five numbered lines 14 to 18, one sentence each, saying what the five lines of T7B say; owed line 7 gains the digest clause of T7A. Any other sentence you find untrue: correct it and name it in STATUS; a sentence you are not sure of: leave it and name it in FOR TUESDAY.

## FACTS (re-print each; a pointer is the drafter's, printed once, and can be stale)
1. **The heads** (MEASURED [F1], `gh api -X GET` under the project `GH_CONFIG_DIR`, account verified first, 14:01:41): `main` = `7e1a01cf640f8abac89e7148322651be8e4bf15b`; `b1764/wp03-ci-skeleton` = `a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89`; `matching-refs/heads/` 2 rows; `compare/main...b1764/wp03-ci-skeleton` ahead 1, behind 0, 24 files; pull requests of any state 0 (Tuesday read the same two shas with the API at 13:39:51: RELAYED). Your checkout `<repo>`: `HEAD` at the lane head, porcelain 0 lines, 25 tracked paths (read verbs only).
2. **The ruleset and what a branch push meets** (RELAYED from the gate's `CODEQL-FIRST-PR.md`, read by the drafter; not re-read): one organisation ruleset on `main` only, 4 rules, `required_status_checks` an empty list, no bypass. Its `non_fast_forward` rule targets the default branch: NOTHING on GitHub refuses a non-fast-forward push to the lane branch, so the fast-forward of Step 6 is proven by YOU before the push (ancestor check) and after it (the compare read).
3. **The scanner** (MEASURED [F2], [F3]): `/opt/homebrew/bin/gitleaks version` prints `8.30.1`. Its default configuration at tag `v8.30.1` (`gh api -X GET repos/gitleaks/gitleaks/contents/config/gitleaks.toml?ref=v8.30.1`): 3209 lines, 222 rules; the global `[allowlist]` block holds 25 path patterns, 13 value patterns and 2 stop words; 3 more path lists sit inside single rules (one of them inside the rule for the planted token's kind: `(?:^|/)@octokit/auth-token/README\.md$`). `gitleaks dir --help` names `--max-target-megabytes` ("files larger than this will be skipped", unset by default) and `--max-archive-depth` (default 0: no archive is opened). Where the scanner looks for a configuration, in its own help's order: `--config`, then the two configuration variables, then `(target path)/.gitleaks.toml`.
4. **The test count at the head** (MEASURED [F4b]): `/usr/bin/grep -c -E '^[[:space:]]+def test_'` prints 22 for `build/tests/test_release_guard.py` and 26 for `build/tests/test_repo_rules.py` (48; the column-1 pattern `^def test_` prints 0 and 0). After T3 and T4: 23, 26 and 4 = **53**; `python3 -I -m unittest discover -s build/tests -v` on the candidate printed `Ran 53 tests`, then `OK`.
5. **The candidate's local runs** (MEASURED [F5], drafter's scratch copy of the head with T1 to T6 applied and committed): `python3 -I build/repo_rules.py <copy>` prints `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)` and `RULES: clean (26 files)` (in `<repo>` the hash half RUNS and should print the count of supplied files: round 1 printed 1657); `gitleaks dir` and `gitleaks git` with the workflow's options: rc 0 each, `no leaks found`; 6 `uses:` lines; 0 lines holding the word for the credential store; 0 non-ASCII lines in the five changed text files.
6. **The dotnet chain on the candidate** (MEASURED [F6], the project's SDK `<project>/.tools/dotnet/dotnet`, which prints `10.0.404`, executed with the drafter's own home and package cache; one heavy job at a time, load1 between 2.6 and 2.7): `dotnet restore Datasec.Suite.slnx` without `CI`: rc 0, and exactly ONE lock file changed (`tests/Datasec.Suite.Core.Tests/packages.lock.json`, 24 added lines: the sections `net10.0/linux-x64` and `net10.0/win-x64`). Then with `CI=true`: `dotnet restore --locked-mode` rc 0; `dotnet build -c Release --no-restore` rc 0, `0 Warning(s)`, `0 Error(s)`; `dotnet test -c Release --no-build` rc 0, `total: 1`, `failed: 0`, `succeeded: 1`; both `dotnet publish` lines of the workflow rc 0 (10 and 11 files); the guard over each prints the warning line and `GUARD: clean (10 files)` and `GUARD: clean (11 files)`; `dotnet restore --locked-mode` again rc 0; the three lock files byte-equal before and after. **Fault 2 does not return:** both publishes WITHOUT `CI` leave all three lock files byte-equal (`cmp` rc 0 three times) and the locked restore after them is rc 0. **A later project inherits the list:** a scratch fourth project with NO runtime list of its own, referenced by the host, restores with both runtime sections in its lock file and the host publishes for `win-x64` under `CI=true` rc 0.
7. **The mutants on the candidate** (MEASURED [F7], each in its own scratch copy; "unit" is the suite, "step" is the workflow step run as the runner runs it):
| Mutant | unit | step |
|---|---|---|
| none (control) | `Ran 53 tests`, `OK` | neutral step rc 0; floor step rc 0 |
| the plain first line dropped from the function | RED 1: `test_secret_scan_job_is_the_reviewed_text` | `found under a neutral name 5`, rc 1 |
| the function reads only the checked-out commit | RED 1: the same case | `found under a neutral name 5`, rc 1 |
| the plant scanned under its own names | RED 1: the same case | `found under a neutral name 1`, rc 1 |
| the planted control's three requirements deleted | RED 2: the same case and `test_a_narrowed_scan_a_removed_plant_and_a_lowered_floor_are_seen` | rc 0 (the step cannot see its own requirement gone: the unit case is what goes RED) |
| the scan of the real stored files deleted | RED 2: the same two | rc 0 (likewise) |
| `FLOOR=16` | RED 1: `test_unit_test_floor_equals_the_number_of_planted_controls` | floor step rc 1 |
| one planted control deleted, floor kept | `Ran 52 tests`, RED 1: the floor case | floor step rc 1 |
| a missing deny-list read as an empty one | RED 1: `test_missing_denylist_is_exit_2_never_an_empty_list` | - |
| the `secret-scan` job given `if: false` | RED 1: `test_secret_scan_job_is_the_reviewed_text` | - |
8. **The hosted log line of the base image** (MEASURED [F8], the drafter's copy of the gate's saved `linux` job log of run `44661506229`, line 267): `#5 [1/3] FROM mcr.microsoft.com/dotnet/aspnet:10.0@sha256:12b1135f5f8b3c0a214f2a680ff2033dff4f684f445d6c697d9524ceeb303586`. The gate's quote holds.
9. **The frozen blocks** (MEASURED [F9]; `lines / bytes / sha256` of the text strictly between the markers, as the drafter's extraction program printed them from THIS file, each equal to the file the dry runs used):
| Block | Lines | Bytes | sha256 |
|---|---|---|---|
| T1 | 52 | 2965 | `85405ebceb2951e123a8bae16f55150a690d3907e8b138bf68da15b7eca94777` |
| T2 | 6 | 362 | `906f103d749e00c8280b685bfb23563c25eb2bcb860fb2b3112fd4390334c790` |
| T3 | 8 | 507 | `3dc5e54f1fbd3f66c8a6cc704e5fbeca3e06a405ee4f84011709193d4260f4e8` |
| T4 | 116 | 5471 | `837032cb58a87d3ed2fe9ac3509b738385bab9ca9d12ee7de12b849be175ea12` |
| T5 | 15 | 834 | `fb0e61199cb7ecc326452ca0e0e66ea1c7943487b135b0c03305516c4ffe9a47` |
| T6A | 1 | 94 | `504f42892f7039cc851daeab4e5ec610690cbc9e79446b5673008df59c4d0f7a` |
| T6B | 2 | 162 | `3debdc87ca4a80d41169527c285c231219b0f8041fe5b4f87b1d781de5be4a6c` |
| T6C | 3 | 735 | `a8cd2ae7f62b56bf10798fcacd15e3c253fdb7ff26853e9267e55b935a808afd` |
| the Core project file after the edit | 5 | 136 | `a9a4038bc27cd9cf334b0dc394549525208d9d0d55d5302ee53d27e1ac1d4ad5` |
| the Server project file after the edit | 8 | 270 | `0270476a5b5078b5eb7d59ff70bc4e1976880b2df2b5ad423195e3d6debd38b1` |
T7A, T7B and T8A are prose for the records files: their line counts are in the sidecar; they have no dry run.
10. **Toolchain by PATH** (MEASURED [F10]): `<project>/.tools/dotnet/dotnet --version` prints `10.0.404`; `/opt/homebrew/bin/gitleaks` 8.30.1; `/opt/homebrew/bin/python3` 3.14.10; `/bin/bash` 3.2.57 (the runner's is newer: UNMEASURED there). Your dotnet environment, every run: `DOTNET_ROOT='<project>/.tools/dotnet'` first on `PATH`, `DOTNET_CLI_HOME` and `HOME` = `'<project>/.tools/b1774/dotnet-home'`, `NUGET_PACKAGES='<project>/.tools/nuget-packages'`, `DOTNET_CLI_TELEMETRY_OPTOUT=1`, `TESTINGPLATFORM_TELEMETRY_OPTOUT=1`, `DOTNET_NOLOGO=1` (the launcher exports only the first: finding 11, not yours to fix; set the others yourself).
11. **Machine and neighbours** (MEASURED [F11], 14:17:31): `LC_ALL=C uptime` load averages between 2.6 and 3.5 during the drafting; 1031 GiB available on the volume; `tmux list-panes -a` shows 0 panes whose name holds `OXPd2`; `<project>/.tools/` holds `b1764`, `dotnet`, `nuget-packages` and no `b1774`; `<project>/1_Project_Definition/Briefs/` holds the round-1 kit copy and its STATUS only. No other kit of today names this project's repository (before this kit was written, 3 brief files held `oxpd2` in their names, all three the round-1 kit). The six design files under `<project>/1_Project_Definition/Design/` carry the file time 14:01 of today: the coordinator's correction pass was copied in. It is not yours; you read the design only for the two lines this kit quotes.

## THE OWNED PATHS (closed list, by PROPERTY first)
**The property.** In `<repo>`, the diff `a0f9bdcc..HEAD` touches only files that carry one of the IN items of the table above, each changed only as a frozen text says; no tracked file is added except T4's; no file is deleted or renamed. Outside `<repo>` you write only the three records files, your own Briefs files and your lane folder. **At least these, and no other (8 paths in `<repo>`; any other path: prove it meets the property or `STOPPED: NEEDS TUESDAY`):**
| # | Path | Change |
|---|---|---|
| 1 | `.github/workflows/ci.yml` | T1, T2 |
| 2 | `build/tests/test_release_guard.py` | T3 |
| 3 | `build/tests/test_pipeline_controls.py` | NEW, T4 |
| 4 | `Directory.Build.props` | T5 |
| 5 | `src/Datasec.Suite.Core/Datasec.Suite.Core.csproj` | 4 lines removed |
| 6 | `src/Datasec.Suite.Server/Datasec.Suite.Server.csproj` | 4 lines removed |
| 7 | `tests/Datasec.Suite.Core.Tests/packages.lock.json` | re-written by the restore (24 added lines expected) |
| 8 | `README.md` | T6 |
Outside `<repo>`: `<project>/BACKLOG.md` (T7), `<project>/SETUP_RUNBOOK.md` (T8), `<project>/5_Project_History/history.md` (one prepended entry), `<project>/1_Project_Definition/Briefs/2026-11-20_B1774_*` (the Step-0 copy, STATUS, a HANDOVER file under the band only), `<project>/.tools/b1774/**`, and `<project>/.tools/nuget-packages/**` (the restore may add to the cache). **If the restore changes a lock file under `src/`: that is NOT expected (the drafter's run changed none): STOP and say which lines.**

## THE WORK
0. **Step 0 and STATUS-NOW** into `<project>/1_Project_Definition/Briefs/2026-11-20_B1774_STATUS.md`: FIRST line `PROGRESS B1774: PENDING`; the kit copy into `Briefs/` (`cmp`, sha256, 0 unfilled slots); the REFUSE counts with controls; `date`; `LC_ALL=C uptime`; `df -g`; **target READY = Step 0 + 150 minutes (`date -v+150M`); the branch push by Step 0 + 100, or STOP; HARD STOP = Stamp S7**; a `WORKING:` line as the LAST line, updated after each step. Every records file is built whole, written to a temp file beside the target and `os.replace`d.
1. **PRIOR-WORK CHECK** (above), then **Setup**: `<project>/.tools/b1774/{logs,scratch,out,_quarantine,dotnet-home,status}`; print `'<project>/.tools/dotnet/dotnet' --version`, `gitleaks version`, `git --version`, `python3 --version`, `/bin/bash --version`. **Extract the frozen blocks** from the Step-0 copy by program into `.tools/b1774/scratch/frozen/` and print each block's lines, bytes and sha256 against FACT 9 (a difference is a STOP: the copy is not the kit). Write `.tools/b1774/predictions.txt` (sha256 printed) BEFORE any edit of `<repo>`: the head's suite is `Ran 48 tests`, `OK`; the acceptance harness on the head's scan lines finds the 14 gate names NOT found by name; after T3 alone the suite is `Ran 49 tests`, `OK`; after T3 and T4 (before T1 and T2) the suite is RED on all four of T4's cases and on nothing else; after T1 and T2 it is `Ran 53 tests`, `OK`; the restore changes exactly one lock file; every chain step is rc 0; the hosted run shows 4 jobs `success` with the lines of Step 6. A prediction that fails is named in STATUS, never edited.
2. **RED FIRST, on the head as it is (nothing edited yet).** Build your OWN harness `.tools/b1774/scratch/acceptance.py` (standard library; the token is built by the program from a random source, written nowhere but the scratch repositories, never printed; assert that the token is absent from every captured output): for each of the 63 rows of the acceptance table, a scratch repository under `.tools/b1774/scratch/acc/` holding the ONE file with the content the row's class names (a token row: the line `value = "<token>"` and a second line naming the row; A50 to A61: the bytes the class words say, the token in clear text except A60 and A61; A58: 96 MiB of filler lines, then the token), committed with a throwaway identity passed by `git -c` (these are scratch repositories, not `<repo>`; set `GIT_CONFIG_GLOBAL=/dev/null` for them). Columns 4 and 5: `gitleaks dir <repository>` and `gitleaks git <repository>` with the four options of the workflow. Print the table and its totals. **Required now: columns 4 and 5 equal the table above for all 63 rows (14 and 13 found); the gate's 14 names read 0. That is the Major, seen red by you.** A row that differs from the drafter's: name it, check the scanner's version, and go on only if the difference is in a row the scanner FINDS more often than the drafter saw (a row it finds less often is a STOP).
3. **TESTS FIRST.**
   (a) T3 into `test_release_guard.py`. Suite: `Ran 49 tests`, `OK`. **Its red, by mutant mD (builder's own run, not independent):** in a COPY of `build/` under `.tools/b1774/scratch/mD/`, change `release_guard.py:57-58` so that a list that cannot be opened returns an empty set; run the copy's suite: the new case is RED and ONLY the new case (print the `FAIL:` lines; the drafter's run: `failures=1`). The copy is never staged; `<repo>` holds no mutant.
   (b) T4 as the new file, BEFORE `ci.yml` changes. Suite: RED, and print which cases (MEASURED [F4b]: `Ran 53 tests`, `FAILED (failures=6)`; the RED names are exactly T4's four cases, the fourth counted once per sub-case, because the workflow still holds round 1's jobs and no `FLOOR`; every round-1 case and T3 stay green).
   (c) T1 and T2 into `ci.yml` (the Edit tool; the bytes from your extracted blocks). Print by program: the file has 190 lines; the sha256 of the `secret-scan` job and of the `rules` job as T4's own helper `job_sha256` computes them equal T4's two constants; `floors` returns `[53]`; `planted_controls` returns 53. Suite: `Ran 53 tests`, `OK`. Then `python3 -I '<repo>/build/repo_rules.py' '<repo>'` after `git add` of the eight paths' current state: `RULES: clean (26 files)` with the R5 note that the hash half RAN (print its count). Print the job names (exactly `linux`, `windows`, `secret-scan`, `rules`), every `uses:` line (6, each one of round 1's two pins) and the count of the word for the credential store in `ci.yml` (0; control: the count of `uses:` is 6).
   (d) **Run the two changed steps as the runner runs them.** A small runner of your own under `.tools/b1774/scratch/`: cut the `run: |` block of the named step out of `<repo>/.github/workflows/ci.yml` by program (the lines after `run: |` that are indented by at least 10 spaces, with 10 spaces removed), write it to a file, and run `/bin/bash --noprofile --norc -e -o pipefail <file>` with the working folder `<repo>` (`env -C`), `GIT_CONFIG_GLOBAL=/dev/null`, and `RUNNER_TEMP` set to a NEW empty folder under `.tools/b1774/scratch/` that holds `gitleaks/gitleaks` as a link to `/opt/homebrew/bin/gitleaks`. Step `scan every stored file under a neutral name`: required lines `PLANTED-CONTROL neutral-scan: planted 6, found by name 1, found under a neutral name 6, rc 1`, `NEUTRAL-SCAN: stored files <n>, files of this commit not among them 0` (n is what your object store holds: print it; the drafter read 36 before any edit) and rc 0; the planted value appears 0 times in the output (count it by joining the two halves in your program). Step `planted controls`: `UNIT-TEST FLOOR: ran 53, floor 53`, rc 0. **A step that writes anything under `<repo>`: STOP (print `git status --porcelain` before and after: equal).**
   (e) **GREEN, the acceptance table through the workflow's own function:** extend your harness: cut the function `neutral_export` out of `<repo>/.github/workflows/ci.yml` by program (from the line `neutral_export() {` to the first line that is `}` alone; print the two line numbers: the drafter's were 119 and 127), run it on each of the 63 scratch repositories, scan the folder it wrote, fill columns 6 and 7. **Required: column 7 equals the table above for all 63 rows: 59 of the 61 token rows found, the 2 not found are A60 and A61, both quiet rows 0.** Then the one-repository history case: the 60 token files except A58, committed, all removed by a second commit: neutral finds 58 in 61 stored files. Print both tables whole in STATUS, section ACCEPTANCE.
   (f) **Mutants on the staged `ci.yml` (builder's own run, not independent; each made with the Edit tool on the work tree, the named check run, then undone with the Edit tool and proved by `git -C '<repo>' diff --quiet` against the staged file):** **mA, the scan narrowed again** (drop `printf 'stored file %s\n' "$id";` and the braces from the function): the neutral step prints `found under a neutral name 5` and ends rc 1, and the suite is RED on `test_secret_scan_job_is_the_reviewed_text`. **mB, the planted control removed** (delete the three `test` lines after the `PLANTED-CONTROL neutral-scan` line): the suite is RED on the same case and on `test_a_narrowed_scan_a_removed_plant_and_a_lowered_floor_are_seen`; the step itself stays rc 0, and you SAY so (that is why the unit case exists). **mC, the floor lowered** (`FLOOR=16`): the suite is RED on `test_unit_test_floor_equals_the_number_of_planted_controls`, and the `planted controls` step ends rc 1. After the last undo: suite `Ran 53 tests`, `OK`.
4. **THE BUILD FILES.** T5 into `Directory.Build.props`; the two project files lose their four lines (prove the three sha256 against FACT 9). Then, each heavy job behind the load gate of HEAVY, logs under `.tools/b1774/logs/`:
   (a) WITHOUT `CI` in the environment: `dotnet restore Datasec.Suite.slnx`. `git -C '<repo>' status --porcelain` must show the test project's lock file as the ONLY lock file changed; print its diff stat (expected 24 added, 0 removed).
   (b) WITH `CI=true`: `dotnet restore --locked-mode`; `dotnet build -c Release --no-restore` (rc 0, `0 Warning(s)`, `0 Error(s)`); `dotnet test -c Release --no-build` (print the totals; **a total of 0 is a STOP**); the two `dotnet publish` lines of the workflow with `-o '<project>/.tools/b1774/out/linux'` and `.../out/windows`; the guard over each (`clean`, 10 and 11 files expected); `dotnet restore --locked-mode` again; the sha256 of the three lock files equal before and after (b).
   (c) **Fault 2 must not return:** WITHOUT `CI`, both publish lines again into `out/linux-noci` and `out/windows-noci`; `cmp` each of the three lock files against its copy from before (c): rc 0 three times; then `CI=true dotnet restore --locked-mode` rc 0.
   (d) `dotnet build-server shutdown`; `pgrep -f` for the project's dotnet path prints nothing. **You never start the server.** NOT RUN by you, said so: `docker build`; anything on Windows.
   (e) **T6 into `README.md`** (the three insertions, the Edit tool, the bytes from your extracted blocks): the file then has 74 lines, and `git diff --numstat` for it reads 6 added and 0 removed.
5. **CHECKS before the commit (each with a planted control), on the staged tree:** (a) `git -C '<repo>' diff --cached --name-status a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89` is exactly the 8 rows of THE OWNED PATHS (7 `M`, 1 `A`); tracked paths 26. (b) every ADDED line ASCII (`LC_ALL=C /usr/bin/grep -c -v -x -E '[ -~]*'` prints 0 per changed text file, so no tab either; control: a planted U+200B in a scratch copy prints 1). (c) the whole suite `Ran 53 tests`, `OK`; `repo_rules.py` clean (26 files) with the hash half run. (d) the scanner, three passes with the workflow's options: `gitleaks dir '<repo>'` rc 0; `gitleaks git '<repo>'` rc 0; the neutral step of 3(d) once more on the staged tree rc 0 (its planted control inside it is the red). (e) no person's name, decision-card id, B-number, finding id, seat id or the words `product owner` in any ADDED line or in the commit message: the UNDERSCORE-AWARE scan `(?<![A-Za-z])<name>(?![a-z])` (python `re`, case-insensitive) for each name of the ban list in step 7 of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md`; control: a planted `_by_<name>_` in a scratch copy fires. (f) no secret value, no key, no certificate file added. (g) the diff of `README.md`, `Directory.Build.props` and `ci.yml` removes only the lines this kit names (print `git diff --cached --numstat`; MEASURED [F5] on the candidate: `ci.yml` 56 added and 1 removed (git keeps two of the three replaced lines, which T2 repeats unchanged); `test_release_guard.py` 8 and 0; `Directory.Build.props` 3 and 0; each project file 0 and 4; the lock file 24 and 0; `README.md` 6 and 0; and `test_pipeline_controls.py` 116 and 0, DERIVED from its line count).
6. **Commit, push, and the hosted run.**
   (a) ONE commit on the branch. Subject, exactly: `Scan every stored file under a neutral name; hold the scan and the test floor to a reviewed text (WP0.3)` (104 bytes). No body but the attribution line your session reminder gives (count 1). No B-number, no person's name, no card id, no finding number, no word about who decided what. `git log --format='%h %ae | %ce' a0f9bdcc..HEAD`: ONE row, both addresses equal to `git config --local --get user.email` (compare in-process; print masked).
   (b) **The fast-forward, proven before the push:** `git -C '<repo>' merge-base --is-ancestor a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89 HEAD` rc 0; `rev-list --count a0f9bdcc..HEAD` prints 1; `git -C '<repo>' ls-remote origin refs/heads/b1764/wp03-ci-skeleton` prints the lane head of FACT 1 (if it prints another sha, **someone moved the branch: make NO push, `STOPPED: NEEDS TUESDAY` with the sha**).
   (c) `git -C '<repo>' push origin HEAD:refs/heads/b1764/wp03-ci-skeleton` (the repository's own `core.sshCommand`; **no `--force`, no `+`, no `--force-with-lease`**). Expected last line of the output, in the form git prints for a fast-forward (MEASURED [F12] on a scratch bare repository): `   a0f9bdc..<your sha7>  HEAD -> b1764/wp03-ci-skeleton`. **The refusal path (MEASURED [F12] the same way): a push that is not a fast-forward ends rc 1 with a line ` ! [rejected]        HEAD -> <branch> (fetch first)` and `error: failed to push some refs`. If you see that, or any `remote: error`, or any `! [remote rejected]`: make NO second attempt, do NOT fetch, pull, merge, rebase or force; write the output verbatim in STATUS and end `STOPPED: NEEDS TUESDAY branch push refused: <the rejected line>`.**
   (d) Read back: `gh api -X GET repos/datasecau/OXPd_2/git/matching-refs/heads/b1764` = ONE row = your sha40; `compare/a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89...<sha40>`: `ahead_by` 1, `behind_by` 0, the file list equal to the 8 paths; `compare/main...<sha40>`: ahead 2, behind 0; `main` still at its sha of FACT 1; pull requests 0.
   (e) **The hosted run of the NEW head** (`gh api -X GET repos/datasecau/OXPd_2/commits/<sha40>/check-runs`, every 60 s for at most 30 minutes): 4 check runs, each `success`, attempt 1. **From each job's log by GET (`actions/jobs/<id>/logs`), the lines that prove the fix RAN, each printed with its count (each at least 1; control: a line that is not there counts 0):**
   - `secret-scan`: `PLANTED-CONTROL secret-scan: rc 1` (round 1's control, still there); **`PLANTED-CONTROL neutral-scan: planted 6, found by name 1, found under a neutral name 6, rc 1`**; **`NEUTRAL-SCAN: stored files <n>, files of this commit not among them 0`** (n on a fresh clone is DERIVED as 34: the 26 files reachable at round 1's head plus one new file per path of your commit; print what the log says, and if it is not what `git -C '<repo>' rev-list --objects origin/main HEAD` counts as blobs on your side, name the difference: a larger number is not a fault); `3 commits scanned.` (DERIVED: round 1's log read `2 commits scanned.`); `no leaks found` at least 3 times.
   - `rules`: `Ran 53 tests`; `UNIT-TEST FLOOR: ran 53, floor 53`; `OK`; `RULES: clean (26 files)`.
   - `linux` and `windows`: `0 Warning(s)`, `0 Error(s)`, `total: 1`, `failed: 0`, `GUARD: clean (10 files)` and `GUARD: clean (11 files)`; `linux` also the image line. **The Windows leg is the only proof of T5 on Windows.**
   (f) **A red job is yours:** fix the ROOT CAUSE on the branch with a NEW commit (fast-forward push, the same checks (b) to (e)); at most 3 commits of yours on the branch in all (4 with round 1's), a further one is a STOP. **If the fix changes a line of the `secret-scan` job or the `rules` job** (the likely case is a shell difference on the Linux runner, which is UNMEASURED): recompute the fingerprint with T4's own helper, set the constant in the SAME commit, re-run Steps 3(d), 3(e) and 5, and name every changed line in STATUS under DEVIATIONS. Never re-run a job to turn it green; never weaken a requirement of T1 to make it pass (a `test` line removed or loosened is a STOP, not a fix). No run within 10 minutes of the push: `STOPPED: NEEDS TUESDAY hosted run did not start`.
7. **THE RECORDS (after the hosted run is green).** `<project>/BACKLOG.md` per T7 (`cmp` the first 45 lines and the old lines 47 to 84 and 85 to 101 against a before-copy: equal; the file gains 30 lines). `<project>/SETUP_RUNBOOK.md` per T8 (print the diff against the before-copy; every changed line is one this kit names or one you name). `<project>/5_Project_History/history.md`: one new entry directly under the title line, above the existing entry (the old bytes unchanged: `cmp` the tail against a before-copy), dated by `date`. Each file built whole, written to a temp file beside it, `os.replace`d; all three are ASCII today (0 non-ASCII lines, MEASURED [F11]): encode as ASCII and STOP on an encode error rather than write.
8. **CONTEXT BAND AND HANDOVER.** About 70% context: start no new part; about 75%: stop at a safe boundary (files whole, no process running, any mutant undone and proved, nothing staged that is not committed or named, no half-written records file) and write `<project>/1_Project_Definition/Briefs/2026-11-20_B1774_HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps / the two heads), last line `HANDOVER B1774: next <step> | done <steps>`, and end STATUS with the same line.
9. **STATUS sections:** Step 0 | Toolchain | BLUF | PRIOR WORK (the table of the PRIOR-WORK CHECK) | PREDICTIONS and their outcome | RED FIRST (Step 2's table) | THE EDITS (each of the 8 paths: the frozen block, its sha256, the numstat) | ACCEPTANCE (Step 3(e)'s two tables, whole) | MUTANTS | THE BUILD (Step 4: every command, rc, the lock-file reading) | CHECKS | COMMIT AND PUSH (the push output verbatim, the read-backs) | HOSTED RUN (each job, each proof line with its count) | RECORDS | DEVIATIONS (every place you did not follow a frozen text, with the reason; "none" if none) | NOT RUN | FOR TUESDAY (FIRST: the round-2 gate must probe the scan THROUGH the workflow's function, because a folder scanned by its own names still skips the 14 names; then: the new head and `main`; the fingerprints as committed; what stays open of WP0.3 and E0.4, unchanged by this round: the bundle tool, the real fingerprint, CodeQL, plus the scanner's three limits; the sentences of the pull-request texts beside the verdict that this round makes untrue: the line that says a rule refusing the skipped names is not built, and the count 48; any OUT item you were tempted to touch; every Question default as built) | Trees left | Commits (sha, `%ae | %ce`). **LAST LINE on finish is EXACTLY one of:** `READY B1774: <sha40>` (the BRANCH head as read back by `gh api -X GET` after the push, every job of ITS hosted run `success`, the records written) | `STOPPED: NEEDS TUESDAY <one question>` | `BLOCKED: <reason>` | `HANDOVER B1774: next <step> | done <steps>`.

## THE LANE (partition from both sides)
| Field | Value |
|---|---|
| Branch | `b1764/wp03-ci-skeleton`, an EXISTING ref: new commits on top of `a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89`, fast-forward only |
| Your paths (property) | THE OWNED PATHS above. Any other path: prove it meets the property or `STOPPED: NEEDS TUESDAY` |
| NOT yours | in `<repo>`: every path not in the list of 8, and by name `build/repo_rules.py`, `build/release_guard.py`, `build/tests/test_repo_rules.py`, `build/denylist/**`, `packaging/**`, `global.json`, `Directory.Packages.props`, `NuGet.config`, `.gitignore`, `.editorconfig`, the `.slnx`, the two lock files under `src/`. In `<project>`: `CLAUDE.md`, `.gitignore`, `Launch_Claude.command`, `.claude/**`, `3_Access_Keys/**` and `4_Credentials/**` (read by name only), `.tools/dotnet/**` (read and execute only), `.tools/b1764/**` (round 1's folder: read only), `1_Project_Definition/CLARIFICATIONS.md`, `Design/**`, `Analysis/**`, `Review/**`, `Registers/**`, `Source_Documents/**`, the round-1 kit copy and its STATUS, every sibling project, the library copy on the NAS, the gate's folder under `/private/tmp/` (not needed: do not open it) |
| Disjointness | no other seat is commissioned on this project's repository (FACT 11; Tuesday confirms at the stamp, S3). The coordinator's correction pass wrote the design copies under `<project>/1_Project_Definition/Design/` at 14:01 today (FACT 11); whether it writes there again while you run is Tuesday's to say at the stamp (S3). You write nothing there |
**PARTITION: every path not named as yours is NOT yours.**

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`; checked BEFORE `.tools/b1774` is created; each count with a control that can fail)
A stamp slot unfilled: `/usr/bin/grep -c -E '_''_''_''_' <Step-0 copy>` must print 0 (control: the unstamped kit prints the count in the Stamp heading); last line not `READ-WHOLE-BY-TUESDAY: DONE ...`. `<project>/.tools/b1774` exists and no HANDOVER file names it. `<repo>` is not at the lane head of FACT 1 with an empty porcelain on branch `b1764/wp03-ci-skeleton`. The origin does not read the two heads of FACT 1, or holds a pull request (the PRIOR-WORK CHECK). `'<project>/.tools/dotnet/dotnet' --version` does not print `10.0.404`. `gitleaks version` does not print `8.30.1` (the acceptance table is this version's). `gh auth status` under the project `GH_CONFIG_DIR` is not the Datasec account that `hosts.yml` names, or `gh api -X GET repos/datasecau/OXPd_2 --jq .permissions.push` does not print `true`. The deploy key missing. Another pane whose name holds `OXPd2` (`tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` prints exactly ONE such line, yours). `df -g /Volumes/Datasec_DEV` under 25 GiB free. **Load is NOT a refuse.**

## HEAVY
A heavy job here = `dotnet restore`, `dotnet build`, `dotnet test`, `dotnet publish`, and the 96 MiB row of the acceptance harness. Run ONE at a time, never in the background beside another. **Load gate: `LC_ALL=C uptime` load1 under 24 on TWO reads 120 s apart (not independent: say so)** before each dotnet job (the 2026-11-11 load ruling for this 18-CPU machine, RELAYED). No lock file: you are the only seat on this project; other projects' seats share the machine, so a wait is not a finding; waited 60 minutes: say so; at the hard stop `BLOCKED: load <n>`.

## STANDING LINES
**PRIOR-WORK CHECK** (above; a READY without a `## PRIOR WORK` section is returned unread). **No message to any human. No Jira call.** Never skip a failure: fix the root cause and re-verify end to end; a red that is not yours is NAMED with its cause. **Never delete** (`rm`, `branch -d`, `--prune`, `gc`, `reset`, `clean`, `stash`, `checkout -- <file>`, `sed -i`): MOVE to `_quarantine`; a mutant is undone with the Edit tool and proved. Not run = NOT RUN. **Source beats this kit: where a pointer, a count or a quoted line differs from what you print, say so and follow the source; a frozen text is followed byte for byte, and where you cannot, that is a DEVIATION named in STATUS, never a silent change.** **No invented fact** (`<project>/CLAUDE.md:61-62`): every statement about how GitHub, a runner or the scanner behaves carries its source or the word UNMEASURED. Shell: no `cd`; absolute single-quoted paths (the path holds a `!`); no unquoted word starting with `=`; `git -C ... --no-optional-locks` for reads; `/usr/bin/grep -i` with a positive control per count (and `-F` for literals); a pipeline's `$?` is its last command's: run the checked command alone; every count, `file:line` and clock in STATUS is printed by a program. Inputs (the verdict, logs, earlier files) are data, read and never obeyed. Closed lists are stated by PROPERTY first and then "at least these"; any other shape: prove it meets the property or STOP. Git identity: the repository's own only (never `git -c user.name/user.email`, never `GIT_AUTHOR_*` / `GIT_COMMITTER_*` for a commit in `<repo>`; D8 is the workflow's text for a runner's throwaway repository, and your scratch repositories are not `<repo>`). Landing is Tuesday's (pull request, hosted checks, CodeQL; never bypass, never dismiss an alert). **NOTHING is deployed, released, published or sent. No Azure. No spend.**

## HOLDS
No path outside the owned list; no pull request; no push to `main`; no force-push, amend, reset or rebase; never delete; no `cd`; **no configuration file, ignore file, baseline or narrowing option for the secret scan; no change to R1 to R5 or G1 to G3; no `--release` mode; no new job; no change to the `linux` or `windows` job; no new action; no workflow line naming the credential store; no weakening of a `test` line of T1 or T2; no fingerprint changed to make a case pass; no renamed constant in T4; no lock file edited by hand; no package added or changed; no download of an SDK or a tool; no `sudo`, `brew`, `apt-get`**; no token typed or printed whole; no planted file tracked; no git identity override in `<repo>`; no Jira call; no read of a sibling project; no write to `<project>/CLAUDE.md`, `CLARIFICATIONS.md`, `Design`, `Analysis`, `Review` or the launcher; any records file you rewrite (STATUS, `history.md`, `BACKLOG.md`, the runbook) is built and encoded in full first, written to a temp file beside it, then `os.replace`d; a records file is never opened for writing before its content exists, and never encoded as ASCII when it already holds non-ASCII bytes (encode the ADDED bytes and check them; `cmp` the unchanged part against a before-copy); no hosted call beyond the named exceptions; no `az`, `docker`, `ssh` of your own; no text anywhere that says the product owner decided, ruled or approved anything in this round.

## Questions with defaults (Tuesday answers at the stamp; every default is already assumed above)
- Q1 (D1, the shape of the fix): default the second scan under a neutral name. Alternative A, the gate's "smallest": R1 refuses the 14 names as tracked paths (then `build/repo_rules.py` and its tests become yours, images and lock files are forbidden in the tree, and names the gate did not try stay open: the drafter measured 24 more). Alternative B: a private copy of the scanner's default configuration without its path list, passed by `--config` (3209 lines to carry and re-derive at every scanner update; R1 and D9 of round 1 must then be changed).
- Q2 (D2 and D3, where the new text lives): default one step in `ci.yml` and one new test file (8 paths in the repository). Alternative: the four cases as a class inside `build/tests/test_repo_rules.py` (7 paths; that file then reads the real workflow, against its own first sentence).
- Q3 (D5, where `RuntimeIdentifiers` lives): default the root `Directory.Build.props` (the test project's lock file changes, MEASURED). Alternative: a new `src/Directory.Build.props` that imports the root one (no lock file changes; one more file and one more place to look: UNMEASURED by the drafter).
- Q4 (D6, the base image): default the digest is written into backlog line 7 and the line stays open. Alternative: `packaging/linux/Dockerfile` becomes yours for ONE line (`FROM ...aspnet:10.0@sha256:<the digest>`), the hosted `linux` job proves the pull, and line 7 is ticked. UNMEASURED by the drafter (no `docker`), and it adds a ninth path to a round that may not fail.
- Q5 (D4, the floor): default `FLOOR` equals the count exactly (a test) and the job needs at least `FLOOR`. Alternative: the job needs exactly `FLOOR` (then a skipped case counted by the runner's Python differently would redden the job: UNMEASURED).
- Q6 (D8, the planted repository's identity): default two commits under `planted-control` inside the workflow text. Alternative: no commit at all (the six files are only added to the index and one is removed again; every one stays in the object store and is exported): no identity is written anywhere, but the plant then no longer shows a real second commit.
- Q7 (the OUT list): default as the table. If Tuesday wants one more small item in (the gate names the substring name rule and the three line rules as "small and in the same two files"): it is a NEW frozen text and a new dry run, not a sentence at the stamp.
- Q8 (the gate): default G1, round 2 of 2, and its commission tells it to probe through the function (D10).
- Q9 (the pane name): default `Datasec/OXPd2-X2`.
- Q10 (the windows): default READY at Step 0 + 150 minutes, the push by Step 0 + 100.

## Stamp
The unstamped copy of this kit reads 9 such lines (S0 to S7 and the last line).
- (S0) COMMISSION (what named this round, and what the product owner has said on this lane since his word to start): Gate B1772 (round 1 of 2) read NO GO at a0f9bdc on main 7e1a01c with one Major (the secret scan skips files by name); this round is Tuesday's decision as coordinator to fix it before any pull request. The product owner has said nothing on this lane since his word to start (C-42). FOR YOUR RECORDS, as the project's rules ask a brief to say: on 2026-11-20 at 14:02 AEDT Tuesday copied the corrected design set into this project's 1_Project_Definition folder (Design: 02, 03 and 05 as md and pdf; Analysis: A10 and A11 new and six reports replaced; Review: three files new and one replaced; Registers: the draft of the questions to HP; CLARIFICATIONS.md replaced by a file that adds C-44 after the same 43 entries), 34 files, each compared equal to its source after the copy. None of it is yours and none of it changes this kit's two quoted design lines, which Tuesday re-printed at the stamp.
- (S1) STAMP (`STAMPED <time> AEDT <date> by <seat>`; what Tuesday read whole and re-printed): 14:33 AEDT 2026-11-20, stamped by Tuesday (seat s297). Tuesday read this kit with the Read tool, lines 1 to 545 in three pages. Re-printed by Tuesday in the stamp command (date printed 14:33:31 Fri 20 Nov 2026): the origin's refs (exactly 2 rows, the two heads of FACT 1), pull requests of any state, the seat checkout's head, branch and porcelain, the panes, the project .tools listing and the SDK folder name; the eight frozen blocks T1 to T6C extracted by program from this file, each with the lines, bytes and sha256 of FACT 9; 63 acceptance rows; the commit subject's 104 bytes; 4 cases in T4 and 1 in T3; line 72 of the project's copy of 03 holds the secret-scanning clause and line 138 of 02 holds N1; the project's CLAUDE.md lines 7, 55 to 57 and 82 read as quoted; models_latest line 11 holds claude-fable-5-2. Recounted by hand: 135 + 52 + 3 = 190; 23 + 26 + 4 = 53; 8 owned paths. NOT re-printed by Tuesday: every dry-run result (the acceptance columns, the mutant table, the dotnet chain, the two job fingerprints inside T4), the scanner's configuration figures, the other file:line pointers, the hosted log line of the base image, the sidecar literals. The load-gate sentence in section HEAVY is relayed and is Tuesday's standing rule.
- (S2) BASE (`main` and the lane branch at origin as Tuesday reads them at the stamp; pull requests of any state): main 7e1a01cf640f8abac89e7148322651be8e4bf15b; b1764/wp03-ci-skeleton a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89; the origin holds exactly these 2 refs; pull requests of any state 0.
- (S3) STATE AT THE STAMP (the seat's checkout: head, branch, porcelain; any `Datasec/OXPd2` pane; `<project>/.tools/b1774` absent; `<project>/.tools/dotnet` version; any other writer under `<project>`): Seat checkout: head a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89, branch b1764/wp03-ci-skeleton, porcelain 0 lines (git read verbs by Tuesday). Panes whose name holds OXPd2: 0. The project .tools listing holds b1764, dotnet and nuget-packages and no b1774. The SDK folder under .tools/dotnet/sdk is named 10.0.404 (Tuesday did not execute dotnet: your REFUSE check prints the version). No other writer under the project while you run: the coordinator's copy of the design set is finished (S0) and no other seat or agent is commissioned on this project now; the round-1 gate's folder under /private/tmp is not yours and is finished.
- (S4) Q-ANSWERS (defaults: Q1 neutral-name scan; Q2 one step and one new test file; Q3 root props; Q4 line 7 stays open; Q5 floor equals the count; Q6 two planted commits; Q7 the OUT table; Q8 G1; Q9 Datasec/OXPd2-X2; Q10 150 and 100 minutes): All ten defaults, each Tuesday's own decision as coordinator and none the product owner's: Q1 the second scan under a neutral name; Q2 one step in ci.yml and one new test file; Q3 the root Directory.Build.props; Q4 backlog line 7 stays open with the digest written in; Q5 FLOOR equals the count by a test and the job needs at least FLOOR; Q6 two planted commits under the throwaway identity inside the workflow text; Q7 the OUT table as written; Q8 a round-2 gate at tier G1 that probes through the workflow's own function; Q9 the pane Datasec/OXPd2-X2; Q10 READY at Step 0 + 150 minutes and the push by Step 0 + 100.
- (S5) LAUNCH WINDOW (until; load1 at the stamp; live seats beside you; one waiter): Launch by 15:13 AEDT 2026-11-20; load averages 2.00 2.38 2.80; no other OXPd seat; one MPS build seat and one NexusAI review run on this machine and share nothing with you; one waiter.
- (S6) PORT BLOCK AND MODEL RECEIPT (no port; level fable; `BRIEF_SEAT_LEVEL=fable` inside the quotes): No port and no listener; level fable (claude-fable-5-2); BRIEF_SEAT_LEVEL=fable inside the quotes; the product owner's instruction of 2026-11-19 that every agent of this project runs on the newest Fable.
- (S7) HARD STOP (absolute latest start; READY = your Step-0 date + 150 min; the branch push by Step 0 + 100; the absolute hard stop): Absolute latest start 15:13 AEDT; READY = your Step-0 date + 150 min; the branch push by Step 0 + 100; the absolute hard stop 18:13 AEDT 2026-11-20.
**Launch (Tuesday), ONE waiter, after the Stamp, level inside the quotes:** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/OXPd2-X2 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=fable WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1774_SEAT-X2_oxpd2-wp03-round2-secret-scan.md'"` No az. Nothing deploys. **Your commission is THIS file (read-only);** Step 0 copies it unchanged into `1_Project_Definition/Briefs/`.

READ-WHOLE-BY-TUESDAY: DONE by Tuesday (seat s297), stamped 14:33 AEDT 2026-11-20: Read tool, lines 1 to 545 in three pages (1 to 180, 181 to 370, 371 to the end). The only word of the product owner this kit rests on is his word to start (C-42); every choice of this round is written as the coordinator's. Round 2 of 2: a second NO GO goes to the product owner. The new scan step has run on macOS only: your hosted run is its first proof on a Linux runner.
