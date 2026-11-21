STARTABLE: YES - the kit is complete and stamp_check reads 175 of 175 claims measured, rc 0. One answer at the stamp is stop-class: Q7, whether `DeleteUnreadable` is built. The default is YES, guarded by a re-read under the store's lock. S4 must answer Q7 in words. The kit's other choices are Tuesday's defaults, each with a cell.

# B1835 drafter report | Datasec / OXPd_2 | push wave, lane SL (WP1.1 follow-up: a secret store listing that goes past unreadable records) | drafter Opus, 2026-11-21 17:00 to 17:19 AEDT

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1835_SEAT-X20_oxpd2-wp11-secrets-list-unreadable.md` (83178 bytes, 268 lines). Its sidecar `.measured` holds 175 claim lines plus the `KIT` line. Tools for the seat: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1835/gate/` (6 files; sha256 listed in the kit). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1835/` (main's tarball, lane D's three files, programs, logs).

## BLUF
1. **The precondition holds.**
   - `main` is `5e36d8dca42966395ea3dd014c7f788409eb585f`, read at 17:00:40 and again at 17:18:22.
   - Its hosted run is green: `total: 894` on both legs, skipped 4 on linux and 19 on windows, `RULES: clean (291 files)`, `HOSTED ...: PASS`.
   - There is no `b1835` ref and no open pull request.
   - Lane D's branch `b1831/wp15-token-broker` is PUSHED at `70c1fad5`, READY per its STATUS. The commission says "not yet pushed"; that is out of date. It touches no path of this lane: 35 files, none under the store's two directories.
2. **The design** (the D-decisions, all Tuesday's defaults):
   - A NEW public interface `ISecretStoreInventory`, implemented by `LocalSecretStore`, with two members:
     - `ListAll()` returns `Readable` (judged exactly as `ListNames()` judges a record, decryption included) and `Unreadable`: each record that does not read, by its record id and a `StatedName`. The name is given only when it parses, follows the name rule and hashes to the id; it is labelled unauthenticated.
     - `DeleteUnreadable(recordId)` removes a record only while, under the lock, it does not read.
   - `ISecretStore`, `ISecretStoreMaintenance` and seven other source files stay byte-equal.
   - The 20-line `ListNames()` block is frozen by sha256 and counted once in the head.
   - Every existing test file is untouched; the cells (U01 to U14) go in a new file.
3. **What the two verdicts force, and the kit carries:**
   - Round 1, finding 5: this lane IS the "one more call" that names what `Rewrap` failed on. Cell U03 ties `Rewrap().Failed` to `Unreadable.Count`.
   - Finding 3: a stated name is never trusted.
   - Finding 11: a second process's records look unreadable to the first. Cell U14 and a named limit.
   - Finding 4 with round 2's guard: `DeleteUnreadable` ends the way back after `RevokeOlderKeys(true)`. Cell U13 and a named limit.
   - Finding 6: what stands at a record path but is not a plain file is unreadable, with no hang.
   - Round 2, N2: "none throws after its write succeeded" must stay true.
   - Round 2, N7: twelve mutants, each red on its own cell.
4. **Two tool findings, both handled in the kit:**
   - (a) `words.py` counts the store's existing lock field `_gate`. Measured: `lock (_gate)` printed `WORDS: 1 hits`, and with `_lockfield` in its place it printed `clean`. Every new locked member adds such a line. Step 6(d) checks the hits equal the `_gate` token count, then checks a copy with the field renamed. The field itself must not be renamed, because that would break the frozen `ListNames()` block.
   - (b) B1831's `hosted.py` hard-codes `Ran 53 tests`. Lane R5 of this wave changes `build/tests/**`, so a landed R5 would make every later read FAIL. My copy adds `--unit` and `--floor`, default 53. Measured: PASS on main with and without them; `FAIL 2` with `--unit 54` (the control).
5. **The repository rules now run WITHOUT `--source-documents`.** This follows the newest DRAFTER_RULES line and review B1830 F4.
   - For a clone under `.tools/b1835/`, the default supplied-source path is absent, so the hash half does not run.
   - Measured on a scratch git copy of main: `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)` and `RULES: clean (291 files)`.
   - Lane D's seat had passed the option. It hashed 35223 files, the key folder included, and printed 37 R5 rows (RELAYED, `B1831_STATUS.md:297`, `:328`).

## FACTS RE-MEASURED (instrument in brackets)
- **Origin** [gh api -X GET, project GH_CONFIG_DIR, 17:00:40 and 17:18:22]:
  - private true, push true.
  - 8 branches: main, six landed lane branches, and b1831 at `70c1fad5`.
  - Pull requests 1 to 6 merged; 0 open.
  - `compare main...70c1fad5`: ahead 1, behind 0, 35 files, none under `src/Datasec.Suite.Secrets` or its tests.
- **Main's tree** [tarball by GET]:
  - 291 files.
  - The solution file is 19 lines (sha256 `765755d6...`) and already holds the store's two projects (lines 7 and 16).
  - `ci.yml` is 199 lines (sha256 `c3894bbc...`), unchanged since lane D's drafting. Lines 40/42/45/46/48, 70/72/75/76/78, 117, 192 and 199 were re-printed.
- **The store** [cat -n and grep at main]:
  - 21 source files and 17 test files.
  - 68 test methods by the indented pattern; the column-1 count is 0.
  - The `ListNames()` block is lines 199 to 218: 715 bytes, sha256 `5f03bc97...`. A program counted it once in main's file; the control, with one character changed, counted 0.
  - `_gate` appears on 9 lines.
  - Free cell prefix: `U`. The existing prefixes are F, G, K, L, M, R and W.
  - sha256 of the seven files that stay frozen are listed in the kit, FACT 3.
- **Hosted run of main** [gate/hosted.py, 17:03:28]:
  - PASS, rc 0. With `--skipped-linux 5` (the B1831 copy) the result is FAIL 2, rc 1; with `--unit 54` (my copy) it is FAIL 2, rc 1.
  - linux: succeeded 890, skipped 4. windows: succeeded 875, skipped 19.
  - NEUTRAL-SCAN: 598 objects.
- **Build rules on a scratch git copy of main** [repo_rules.py, unittest, session scratchpad]: `RULES: clean (291 files)`, `Ran 53 tests`, `OK`.
- **Commit message** [wc, words.py, gitleaks]:
  - Subject 143 bytes; the file is 201 bytes and 3 lines.
  - `WORDS: clean (1 files)`; gitleaks rc 0.
  - Scanner control: a token built from two halves gave rc 1.
  - `words.py --control` printed `CONTROL FIRED: 13 of 13`.
- **Machine** [17:04:13]:
  - Load averages 4.77, 3.17, 2.51; 1003 GiB free.
  - `.tools/` has no `b1835` and no lock folder.
  - 0 OXPd2 panes out of 3.
  - dotnet is 10.0.404 and gitleaks is 8.30.1.
- **Quotes and pointers** [own checker]:
  - 34 fragments checked, each a substring of its cited lines. On the first run 2 missed; I reworded both in the kit (one `///` line break; one design line that moved from 559 to 926).
  - Every `file:line` was re-printed by awk.

## D-DECISIONS (all Tuesday's defaults; each has a Question, an alternative, a cost and a cell)
| D | Default |
|---|---|
| D1 | A new interface `ISecretStoreInventory`; the existing interfaces are untouched. |
| D2 | "Reads" means exactly what `ListNames()` accepts, open included. |
| D3 | `StatedName` only when the name parses, follows the rule and hashes to the id; it is unauthenticated. |
| D4 | No version for an unreadable entry. |
| D5 | A fault that is not a record's throws the whole call. |
| D6 | `Readable` in name order; `Unreadable` in the record store's order. |
| D7 | `DeleteUnreadable` re-reads under the lock and removes only what does not read. |
| D8 | `ReadOnlyCollection` over a fresh array per call. |
| D9 | `AddLocalSecretStore` registers the interface. |
| D10 | `ListNames()`, the other source files and the existing tests are frozen. |
| D11 | README text. |
| D12 | Only the typed error leaves. |
| D13 | Both legs, no skip; Unix-only rows run inside the cells. |

## Q-QUESTIONS FOR TUESDAY (defaults already assumed in the kit)
| Q | Default |
|---|---|
| Q1 | New interface. |
| Q2 | Reads as `ListNames()` does. |
| Q3 | Consistent stated name only. |
| Q4 | No version. |
| Q5 | Non-record faults throw. |
| Q6 | The order of D6. |
| **Q7 (STOP-CLASS, answer in words)** | `DeleteUnreadable` BUILT. Its cost: it destroys records another process or a reversed revocation could read (H14, H15). The alternative: removal only by `Delete(StatedName)`, and nameless records are left to an operator. |
| Q8 | `ReadOnlyCollection`. |
| Q9 | Registered. |
| Q10 | `ListNames()` frozen. |
| Q11 | README text. |
| Q12 | Typed error. |
| Q13 | Both legs. |
| Q14 | The names. |
| Q15 | 210 and 150 minutes, X20, G1 with a second reader on D3, D7, H14 and H15. |

## UNMEASURED
- Every build and test outcome, including the hosted Windows leg under U13 and U14 (DPAPI-NG `LOCAL=user` with rotation).
- The 10 s guard of the pipe row on a slow runner.
- Whether a cast of `ReadOnlyCollection` behaves exactly as U09 expects. This is documented .NET behaviour, but not run here.
- The predicted totals: the base plus the seat's cells, with skipped 4/19 unchanged.

## CHAIN INPUTS (each produced earlier or present at BASE)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 1 | the gate folder; `<repo>`'s local identity; the BASE file for the frozen block | the drafter's scratch; at BASE |
| 2 | the clone on its branch | Step 1 |
| 3 | the stubs; `TestRoot`, `RingKit`, `SwitchableRecordStore`, `SecretRecord` | Step 2; at BASE |
| 4 | the red cells | Step 3 |
| 5 | the green tree | Step 4 |
| 6 | the staged tree; `listnames-block.txt`; `words.py`; `commit-message.txt` | Step 5; Step 1; the gate folder |
| 7 | the commit; the base's totals, skipped and `Ran` counts | Step 6; Step 1's `hosted.py` on BASE |

## THE CHECKS I RAN, AND THE CHECKS THAT ARE NEVER RUN
Each check I ran had a control that fired:
- `hosted.py`: PASS, and FAIL on the control;
- `words.py --control`;
- `words.py` on the `_gate` line, and on the same line with the field renamed;
- gitleaks, with its control;
- the frozen-block count: 1, and the control 0;
- `repo_rules.py` with the hash half not run;
- the ASCII scan of the kit: 0;
- the refuse slot count: 8 on the unstamped kit;
- `stamp_check`: rc 0.

Marked NEVER RUN in the kit: the owned-paths property, every heavy job, `hosted.py` on a head of this lane, the push.

## READING LOAD
The seat reads the kit (83178 bytes) plus 170731 bytes:
- `CLAUDE.md`, `CLARIFICATIONS.md` and `SETUP_RUNBOOK.md`: 66579 bytes;
- the store's 14 source files, 5 test files, `Directory.Build.props` and `ci.yml`: 99239 bytes;
- five tool headers: 4913 bytes.

The lines read in part add 8204 bytes. **The total, about 262 kB, is well over the wave-1 limit of "about 100 kB".** Most of the excess is `LocalSecretStore.cs` (33565 bytes). The seat must read that file whole: it edits it and must not disturb `ListNames()`.

## WHAT I DID NOT READ
- The design documents whole: only 03:153, 02:375, 02:926 and the C15 lines found by grep.
- The verdicts' `FOR-RECORDS.md` and the landing texts.
- The B1829 kit beyond what B1831 carries. The commission names it as a form, and B1831 is the newer kit of the same form.
- Lane D's code, apart from `SecretStoreSessionRecordStore.cs`, `ISessionRecordStore.cs` and `Fakes.cs` (to check whether anything implements `ISecretStore`: nothing does).
- Lane D's STATUS beyond the grep hits and its DEVIATIONS; lane C's STATUS beyond its DEVIATIONS.
- Jira: no call (the kit needs none).
- Nothing of HPSM-POC, the NAS library or `Source_Documents/`: one `test -d` on that folder's path, with nothing listed or opened.

## CORRECTIONS TO THE COMMISSION
- Lane D's branch IS pushed: `70c1fad5`, READY.
- "Read N verdicts whole" was done. The seat's kit restates every binding line, so the seat does not have to read the verdicts.
- The commission gives SL's output as `.measured` and report only; there is no slnx line for this lane.

## OUTSIDE-THE-FENCES DISCLOSURE
I wrote only the kit, its sidecar, this report and files under `fleet/state/s304/d1835/`:
- `main.tar.gz` and its extract;
- `laneD/`: three files fetched by `gh api -X GET`;
- `gate/` with 6 files: 4 copied unchanged, `hosted.py` changed, and a new `commit-message.txt`;
- `scratch/`, `logs/`.

Other actions to disclose:
- In the session scratchpad: one scratch git repository made from the tarball (`git init` and `add`), where I ran `repo_rules.py` and the build rules' Python unit tests. That is not a project tree. My first `git init` aimed at the d1835 folder was refused by a hook, then issued in the scratchpad.
- `gh api -X GET` only.
- No git verb in any project tree, no .NET build or test, no Jira, no message.
