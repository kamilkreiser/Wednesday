STARTABLE: YES (after Tuesday's stamp; two STOP-class Questions, Q16 and Q23, must be answered in words at S4)

# B1857 DRAFTER REPORT: lane SL fix round (round 2 of 2), kit `2026-11-21_B1857_SEAT-X20_oxpd2-wp11-secrets-fix-round.md`

Drafter: Opus, read-only, in session, 2026-11-21 19:43 to about 20:00 AEDT (clocks by `date` listed in the kit's first line). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s305/d1857/` (below `<scratch>`).

## BLUF
- **The fix needs no freeze lifted.** The record store's READ is the one step at which no byte of the record has been judged. Every later step (parse, id, name rule, open) works on bytes `ReadPlainFile` read in full. So `Judge` gets a fourth state, `NotHandedOver`: the record store's read itself was `UnreadableRecord`. `DeleteUnreadable` removes only on `DoesNotRead` and throws `StorageFailed` on `NotHandedOver`. `ListAll()` lists both kinds exactly as round 1 does, so parity with `ListNames()` holds. That is Tuesday's ruling-1 property, exactly. `FileSecretRecordStore.cs`, `ISecretStore`, `ISecretStoreMaintenance`, `ListNames()` and every test file of `main` stay frozen.
- **Ruling 2 (the ring check first)** is one line: `CheckRingUnchanged();` after the disposed check, under the lock.
- **The code is ready as `1-code.diff`:** +62 -17 over three files. I compiled it with the project's SDK in a scratch harness, together with the store's own 19 product files. The harness drove 16 shapes from both verdicts through HEAD1, the fix and three mutants:
  - Every F1 shape was removed at HEAD1 and is kept with the fix: descriptors, `FileShare.None`, mode 000, empty, link, pipe, folder, link to a folder.
  - P08 and P09 were removed at HEAD1 and are refused with the fix.
  - The legitimate removals are unchanged: a changed payload, and a record under a key this store revoked.
  - The planted hand-off cell (U21) is green at HEAD1 and with the fix, and goes red under mR1 (20 of 20).
- **Cells:** U04 and U14 changed, U15 to U21 new. Expected total 920 (DERIVED). Seven cells are red against HEAD1 (MEASURED in kind). U20 and U21 are pinning cells with their mutants.
- **`main` moved during drafting** to `762e774e` (pull request 9, lane D). It touches 0 files under the store's two directories, so D21 lets the push go ahead.

## Facts measured (instrument, clock)
- **Origin, by `gh api -X GET` under the project `GH_CONFIG_DIR` (19:52:38):**
  - private true, push true.
  - branch = `a5ba020bc58e5239242504621a3fb2cfc20020f4`, one parent `61b17ec0`.
  - `main` = `762e774eeac2eb324704c7e5ebf0ace86e018f04`.
  - Pull requests 1 to 9 all closed, 0 open, none on the lane branch.
  - No ref `b1857`.
  - Compare `61b17ec0...762e774e`: 37 files. 0 are under `src/Datasec.Suite.Secrets/` or `tests/Datasec.Suite.Secrets.Tests/`, by `grep -c`. Control: 23 are under Sessions.
- **My scratch clone** (`clone.py draft`, push URL `invalid://no-push`):
  - `merge-tree --write-tree --name-only origin/main a5ba020b`: rc 0, 1 line.
  - `git grep` of `DeleteUnreadable|ListAll\(|ISecretStoreInventory` on `origin/main` src and tests: 0 lines. Control: `ListNames(` gives 1 line in Sessions.
  - `ls-tree` counts: HEAD1 295, main 329.
- **Hosted runs, by `hosted.py` (GET only):**
  - HEAD1 PASS with `--total 913 --rules 295 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60` (19:50:51). Control `--unit 53`: FAIL 2.
  - `main` `762e774e` PASS with `--total 973 --rules 329`, rest the same. Control `--total 1`: FAIL 4.
- **The harness** (19:49:53 to 19:50:29; logs `<scratch>/proto/run-*.log`, builds `build-*.log`):
  - Five builds, each rc 0 with `0 Error(s)`. 16 shapes per build.
  - The per-shape table is in the kit's FACT 6.
  - Variants: `mhanded` and `mnoring` confirm in kind which cells each mutant reds. `mr1` reds the hand-off.
- **The diff:**
  - `git apply --check -R` in my clone: rc 0. Numstat: 21/4, 8/3, 33/10.
  - The 62 added lines: 0 non-ASCII. `words.py` over them plus the commit message: `WORDS: clean (2 files)`. Control: `CONTROL FIRED: 13 of 13`.
  - `_gate` added: 0.
  - Boundary words in the 29 added `.cs` lines: 0 each. Control: `File.` fires.
  - `NotHandedOver`: 4 in the fixed file, 0 at HEAD1.
  - Frozen block: count 1 in both the head and fixed files. Control: 0.
- **Scanning and repository rules:**
  - gitleaks 8.30.1 over the commit message and the diff: rc 0. Control: rc 1. My first control, a repeated-pattern token, did NOT fire (rc 0). I replaced it with a random 36-character body, which fired.
  - `repo_rules.py` (no option) over my fixed clone: `RULES-NOTE: R5 hash half NOT RUN ...`, `RULES: clean (295 files)`. `unittest discover`: `Ran 60 tests`, OK.
- **Toolchain:** `dotnet --version` 10.0.404; `gitleaks version` 8.30.1.
- **Machine:** load1 between 2.00 and 3.37. The wave lock folder was absent at 19:47:06 and 19:49:53. Panes: X14 and X23 live, no X20. `.tools/b1857` absent.
- **`stamp_check.py <kit>`:** rc 0, 219 claims, 219 measured. 80 were measured against the source. 139 are names, commands or placeholders the kit defines; each is marked "no literal to match".

## D-decisions (all Tuesday's defaults as coordinator; detail in the kit)
- **D14:** the two-state `Judge` mechanism, no freeze lifted (Q16, STOP).
- **D15:** `StorageFailed` when the bytes are not handed over (Q17). A folder's answer changes from false to `StorageFailed`.
- **D16:** such a record is still listed, with `StatedName` null (Q18).
- **D17:** the ring check comes first and supersedes D7's "never checks or uses the key ring" (Q19).
- **D18:** a folder or a link to a folder gets `StorageFailed` and is kept (Q20).
- **D19:** cells U04 and U14 changed, U15 to U21 new, all in `InventoryTests.cs` (Q21). This reads "every existing test file stays frozen" as the test files of `main` `61b17ec0`; ruling 2 itself changes U14.
- **D20:** the drafter's diff is applied after the red run (Q22).
- **D21:** no rebase. STOP only if the moved `main` touches the store's two directories (Q23, STOP).
- **D22:** named limits: a decryption failure that is not the record's own, the race with a second process that writes without changing the ring, and EIO/ENFILE (Q24).

## Questions for Tuesday (each with its default)
- **Q16 (STOP-CLASS):** mechanism. Default A: the two-state `Judge` in `LocalSecretStore.cs` only.
  - Alt B: lift the freeze of `FileSecretRecordStore.cs:42-45` and map an open or read failure to `StorageFailed`. Its cost: `ListNames()` and `TryGet` change reason for a locked or mode-000 file, and A's split is still needed for the look-before-open rows.
  - Alt C: name the destruction instead. Ruled out by ruling 1.
- **Q17:** `StorageFailed` (default) vs false.
- **Q18:** still listed (default) vs `ListAll` throwing vs a third contract property.
- **Q19:** ring check first (Tuesday's default) vs none vs the full check.
- **Q20:** folder and link to a folder both get `StorageFailed` (default) vs false.
- **Q21:** the cells in `InventoryTests.cs`, no new file, total 920 (default) vs a new file (rules 296).
- **Q22:** the drafter's diff (default) vs the seat writes the product change.
- **Q23 (STOP-CLASS):** never rebase; fetch and print `main`'s changes since `61b17ec0`; STOP only on the two store directories (default). Alt: rebase with force-with-lease on Tuesday's word.
- **Q24:** named limits (default) vs refusing on any open failure that is not an authentication failure.
- **Q25:** seven mutants, round 1's twelve not re-run (default) vs also re-running mOpen and mStorage.
- **Q26:** READY at Step 0 + 180, push by Step 0 + 140, new pane X20, opus (default; the commission's numbers).

## UNMEASURED / NEVER RUN
- **No suite run.** All of these are DERIVED: the totals (920 local, 994 merged with `762e774e`), the red-first list in the suite, and the mutant reds in the suite (mFalse, mBoth, mListDrop and mSwallow were not run even in the harness).
- **Linux and Windows not run.** The harness ran on macOS arm64 only:
  - U16 on the hosted Linux runner is the likeliest red: the process-wide limit inside the test host.
  - U15 on Windows (sharing violation) and U18 on Windows (DPAPI-NG) are DERIVED.
- **U16 does nothing on Windows.** That is a named hole.
- **Not covered:** the H29 decryption limit, EIO and ENFILE.
- **`git apply --check` forward on a clean HEAD1 tree:** I ran only the reverse check, on HEAD1 with the diff applied. That is equivalent, but not the same command the seat runs.

## Chain inputs (MEASURED LITERALS rule 4)
| Step | Inputs | Produced by / present at |
|---|---|---|
| 0 | kit, Stamp | Tuesday |
| 1 | `<src>` seven files (exist, sha256 in THE TOOLS); `<repo>` local config; origin | drafter scratch; `<repo>`; GitHub |
| 2 | test helpers | the clone from Step 1 (exist at HEAD1: `Fresh`, `Print`, `Snapshot`, `Bounded`, `Expect`, `ReadFailingRecordStore`, `TestRoot.Refused`, `RingKit.MakeNamedPipe`, `SwitchableRecordStore`) |
| 3 | the reading; the lock files at HEAD1 | Step 2; HEAD1 |
| 4 | the red tests; `1-code.diff` | Step 3; Step 1 copy |
| 5 | the green tree | Step 4 |
| 6 | the staged tree; `listnames-block.txt`; `commit-message.txt` | Step 5; Step 1; Step 1 |
| 7 | the commit; HEAD1's hosted numbers | 7(a); Step 1 |

## Reading load (mine)
- **Read whole, 324610 bytes** (MEASURED by `wc -c`): the commission, `DRAFTER_RULES.md`, both verdicts, B1854's `probes.txt`, the round-1 kit, kit B1851, and at HEAD1 `LocalSecretStore.cs`, `FileSecretRecordStore.cs`, `ISecretRecordStore.cs`, `ISecretStoreInventory.cs`, `SecretStoreError.cs`, `InventoryTests.cs` and `TestRoot.cs`.
- **Read in part, about 60 kB** (estimated, not measured): the round-1 STATUS sections, the README diff and the Limits lines, the probe sections of G11/G12 and P04/P08/P09/P11, the tool headers, kit B1845's headings, and the `stamp_check.py` header.
- **The kit:** 91293 bytes at its first write. The sidecar's `KIT` line holds the final size.

## Outside the fences: disclosure
1. **I ran `dotnet` outside the wave lock.** Taking it would mean writing into the project's `.tools`, which is forbidden.
   - What ran: five harness builds and five harness runs, in `<scratch>/proto`.
   - Setup: own HOME, NuGet and CLI folders, and a closed proxy (127.0.0.1:9). No package was restored.
   - Conditions: load1 2.00 at the start; the lock folder was absent at both reads.
   - Same pattern and disclosure as drafter B1851.
2. **The harness compiled a COPY of the store's product source** in my scratch. Nothing was copied into any project. In its own process it ran `setrlimit`, `mkfifo` and `chmod 000` on its own temporary files.
3. **Temporary folders left behind.** The harness left 80 temporary folders `d1857-*` under the session's `$TMPDIR` (`/var/folders/.../T/`). They hold synthetic records and random 32-byte key files and nothing else. I did not delete them (never-delete rule). They can be quarantined or left.
4. **Git write verbs, in my own scratch clone only:** `switch -c`, `fetch origin main`, `merge-tree --write-tree` and `apply --check -R`. The working-tree edits that made `1-code.diff` were done with the Edit tool. The clone has push URL `invalid://no-push`. No git write in any project tree.
5. **Other scratch-only actions:**
   - `sed -i` once over my own three harness `.csproj` files.
   - `repo_rules.py` (no option) and `unittest discover`, run in my clone. `<scratch>/1_Project_Definition` is absent, so nothing was hashed.
6. **External reads:** `hosted.py` four times and `gh api -X GET` reads, all GET under the project's `GH_CONFIG_DIR`.
7. **What I did not do:** no Jira or GitHub write, no message, no key folder opened, nothing under `Source_Documents/` read.
8. **Card ids:** I read no decision card and name none.
