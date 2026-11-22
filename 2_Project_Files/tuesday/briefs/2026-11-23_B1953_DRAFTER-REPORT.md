STARTABLE: YES

# DRAFTER REPORT B1953 (OXPd 2, lane A2-F2, seat Datasec/OXPd2-X43), read-only drafter (Opus 5.5), 2026-11-23 04:20 to 04:43 AEDT

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1953_SEAT-X43_oxpd2-a2-f2.md` (75750 bytes) + `.measured` (163 claims, 163 measured; `stamp_check.py <kit>` rc 0, printed `163 claims, 163 measured, 0 not measured`). Tools for the seat: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s313/d1953/seat-tools/` (ten files, sha256 in the kit). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s313/d1953/` (below `<d>`).

## BLUF
- **The fix is ONE boundary, and it closes all three exits** (the lane's and both pre-existing ones). The whole-answer walk `CsaReading.HoldsANameTwice` already reads every name. It now also reads every string value once (`case JsonValueKind.String: _ = element.GetString();`, `CsaReading.cs:184-186` after the patch). The one parse also catches `InvalidOperationException` beside `JsonException` and ends the call `MalformedAnswer` (`CsaStore.cs:254`). The walk runs before `Clone()` and before any read, so no later read can meet a text the reader cannot read. That holds for the 25 JSON read lines of the library, censused by program and listed in the kit's THE READ SITES, and on the paths the cells cover.
- **Red first at main `49f686a8`, MEASURED:** whole solution `total: 1806`, `failed: 23`, `succeeded: 1779`, `skipped: 4`. All 23 failures are Identity cells, and all are `Assert.IsType() Failure`: 22 name `typeof(System.InvalidOperationException)` and 1 is `Value is null`. By cell: F14 11, R08 5, K07 4, E12 3. Green after the fix: 1806 / 0 / 1802 / 4.
- **Mutants:** 47 of 47 MATCH and 47 undone. These are the 44 rows of lane A2-F, each still applying byte for byte (three of them with larger expected cell sets, as measured), plus three new rows. A build after the last undo, then green again. The loop: 50 of 50. The chain: forced restore with 28 of 28 lock files equal, build 0/0, test 1806/0, both publishes, guard 10 and 11 files, unittest 111, `RULES: clean (551 files)`. Checks: boundary clean (control 33 of 33), words clean (control 13 of 13), gitleaks rc 0 (control rc 1), neutral scan 25 of 25 / 0 / no leaks.
- **Named cost (Q1):** a bad escape in a value the store NEVER reads now fails the call (F14 row 11, `jobTitle`; at BASE `Found`). This is the same fail-closed rule as lane A2-F's repeated-name check.
- **Beyond the lane, found by my probe (not a cell):** bytes that are not UTF-8 inside a string were a further untyped exit at BASE. `JsonDocument.Parse` does NOT reject them. Raw `FF` in an unread name, in a card entry, or the UTF-8 form of a lone surrogate in the display name or in a name inside the set gave `OTHER System.InvalidOperationException` at BASE. At the head every one is `TYPED MalformedAnswer`. There is no cell because `Fakes.Raw` answers with text (`Fakes.cs:121`), and `Fakes.cs` is not owned (Q3).

## FACTS RE-MEASURED (instrument and control each)
1. Origin (`gh api -X GET` under the project GH_CONFIG_DIR, 04:29:17): main `49f686a88fdb5c810c124dfe55ca1e68d2c29819`. `b1953` refs: 0 (control: `b1944` 1 row, `a56ed63b`). Open pull requests: 0. Newest pull request: 29, closed and merged. Open code-scanning alerts: 0. `.private` true, `.permissions.push` true. Lane F3's branch `b1945/f3-readme-limits` is at `6177b525` (ahead 1 / behind 1 against main), touching four paths, none of them ours.
2. BASE's hosted run (`hosted2.py ... --total 1783 --rules 551 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan`, 04:28:59): run 45048341660, linux 1779, windows 1762, rules 551, floor 111/111, both GUARD lines, `HOSTED 49f686a8...: PASS`.
3. THE CODE: the BASE and after sha256 of the nine files (facts.py over `<d>/clone2` and `git show BASE:`). The three source files at BASE are equal to kit B1944's "after" column (compared table to table). Numstat: 8/1, 6/0, 7/2, 26/0, 44/0, 28/0, 28/0, seven `M` rows. `ls-files` 551. The second `apply --check` of `2-fix.diff` is refused.
4. Six reused tools, each sha256-equal to kit B1944's table: clone, heavy, hosted2, words, run_step, boundary.
5. Toolchain: dotnet `10.0.404`, gitleaks `8.30.1`. `df` shows 973 GiB available. Panes: `tuesday` and `Datasec/OXPd2-X42`. There is no X43 pane, no `.tools/b1953`, and no `B1953` file in Briefs/ (control: `B1944` 2).
6. CLARIFICATIONS subject-word counts are all 0 (surrogate, escape, UTF-16, untyped, InvalidOperationException, MalformedAnswer, card store, HPAuthenticationSuite, whole character); control `tolerant` 5. Nothing about this subject is ruled by the product owner.
7. BACKLOG: the finding is not filed. `InvalidOperationException` 0. `surrogate` 1, at line 288: the Data library's snapshot, unrelated. Control `tolerant` 8.
8. Ports: none assigned, none used. The kit carries "Port block: none".

## D-DECISIONS (each Tuesday's as coordinator, each a Question with a default)
- D1: one boundary (the walk reads every text, and the parse's catch types what fails). D2: its cost, an unread bad value fails the call. D3: four new Theories with 23 rows, no existing line changed. D4: the comment and the README name escapes only; non-UTF-8 bytes are measured by probe only. D5: one commit, with the rebase rule before the first push.

## Q-QUESTIONS FOR TUESDAY (defaults assumed in the kit)
- **Q1 (STOP-CLASS, S4 in words): default a, one boundary that closes all three exits.**
  - b: the catch alone. This closes the name cases only and leaves 11 value rows untyped as a NAMED LIMIT; DERIVED from `mValuesUnread`, which reddens exactly those 11 rows.
  - c: move the callers' reads inside `GetJsonAsync`'s try. This is a second mechanism, and unread values would stay harmless.
- Q2: the README wording as patched (escapes named, bytes not named). Alternative: also name non-UTF-8 bytes.
- Q3: no cell for non-UTF-8 bytes (it would need a new byte-level handler class in a test file). Alternative: add one Theory with its own handler.
- Q4: not a deviation-register row; it is named in FOR RECORDS.
- Q5: Opus.
- Q6: READY at +110 minutes, push at +80, pane X43, gate G1 round 1 of 2 of lane A2-F2.
- **Commission item 2 answered:** the same change does cover both pre-existing exits. Each has its own red-first rows: the name inside the set is F14 row 4 and R08 row 2; values the store reads are F14 rows 7-10, R08 rows 3-5, K07 rows 3-4 and E12 row 3. No NAMED LIMIT was needed.

## UNMEASURED
- Whether Graph ever sends a lone-surrogate escape or bytes that are not UTF-8.
- Every run on Linux or Windows, so the hosted legs of a head of this lane are PREDICTED: linux 1802, windows 1785.
- The merge with lane F3's head; its fix round may still change its paths, though none is shared (DERIVED).
- CodeQL on the coming pull request.
- Whether `catch (InvalidOperationException)` raises a CodeQL note. There are 0 alerts on main, and the catch is filtered by type, not `catch (Exception)`; DERIVED.

## NOT RUN / NEVER RUN (said in the kit's FACT 6)
- `clone.py` seat mode, the branch, the commit and its identity read.
- The neutral scan on a commit of this lane, the push and its read-back.
- `hosted2.py` on a head of this lane, and the rebase.
- `repo_rules.py --source-documents`: never.

## OUTSIDE-THE-FENCES DISCLOSURE
- **Writes:**
  - Inside the commission's three outputs: the kit, its `.measured`, and this report.
  - Inside my scratch `<d>/`: three clones made by `clone.py ... draft` (push URL `invalid://no-push`, no identity); edits, a `git add`, mutant edits and builds inside `<d>/clone`; my probe file `ProbeB1953.cs` in the working trees of `<d>/clone2` and `<d>/clone3`, never committed; logs; helper scripts; one `sed -i` on my own `scratch/probe_run.py`.
  - Moved to `<d>/_quarantine/` (nothing deleted): the gitleaks control folder and a first sidecar version (`sidecar-v1.measured`).
  - The heavy lock (`.tools/wave1-heavy.lock.d`): taken and released by `heavy.py` only, at about 200 lock takes with 0 to 2 waits. At 04:34:45 it was held by another holder and was not touched.
- **Reads:**
  - Of the project, read-only: `CLAUDE.md`, `CLARIFICATIONS.md`, `BACKLOG.md`, SETUP_RUNBOOK by size and hash only.
  - Of GitHub, by `gh api -X GET` only.
  - Locally: tmux pane names.
  - No read of `Source_Documents/`, a key folder, the NAS, a sibling project, `fleet/briefs_staged/`, `scoreboard.md` or `_ledger.md`.
- **Network:** `git clone` from the origin three times, plus GETs. No Jira call, no push, no pull request, no mail, no az.
- **Tool slip:** the Write tool turned one JSON surrogate-pair escape I typed in the kit into the emoji character. Found by a non-ASCII scan (1 byte), replaced by program with the ASCII escape text. The kit now holds 0 bytes over 126.

## FOR THE GATE (G1 round 1 of 2)
- Read THE READ SITES against the head.
- Check whether the new `InvalidOperationException` catch can take an exception that is not a text read. The only code inside that try is the Parse, the walk and `Clone()`; DERIVED.
- Re-probe raw non-UTF-8 bytes on the head; my probe outcomes are in `<d>/scratch/probe-head.txt` and `probe-base.txt`.
