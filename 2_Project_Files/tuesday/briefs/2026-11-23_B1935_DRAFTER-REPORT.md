STARTABLE: YES

# B1935 DRAFTER REPORT: OXPd 2, lane F1 (seat Datasec/OXPd2-X37), follow-ups of lanes A1 and U in product code

Drafter: in-session Opus, READ-ONLY toward the project, Jira and GitHub. Written 2026-11-23 00:28 AEDT (`date`: 00:28:26). Commission `tuesday/briefs/2026-11-23_B1934-B1937_OXPD-WAVE3-KITS_DRAFTER_COMMISSION.md` (sha256 `4f04ce53...`), lane F1 only. Files written: the kit `tuesday/briefs/2026-11-23_B1935_SEAT-X37_oxpd2-f1.md` (78863 bytes, 231 lines, sha256 `cbb7848b8f83a572f565b26dd04255f6cfddeef2bbab40d281396c6758525922`), its sidecar `.measured` (sha256 `30f82cc8...`), this report, and scratch under `fleet/state/s312/d1935/` only.

## BLUF
- **Startable.** All four follow-ups are built and measured in a prototype at `main` `c480a0c8`: six new test cases (B08, B09 x3, B10, T13), each RED by assertion at BASE and GREEN after the fix; five product mutants, each red on exactly its cases; the whole solution `total: 1668`, `failed: 0` (BASE 1662 + 6); no public line changed in SignIn, Registration or Secrets (`SURFACE: equal (3 folders)`, control 3 of 3).
- (a) `RaiseAudit` calls each `GetInvocationList()` entry in its own try. B08 subscribes a throwing handler FIRST (a new optional `Kit` argument), as gate B1929 asked.
- (b) `Guid.Empty` as a card user's object id is `LookupFailed` at the lookup (no acquire, no audit, the signed-in user stays). The token side needs no line (probe P3: already `BindingRefused`).
- (c) Two README Limits lines (I-4 and Q11's cost), each re-measured by my own probe (P1: 121 s from arrival; P2: `sid-2` ended, the printer keeps the new user).
- (d) A same-object renewal is refused in `Finish` as `Failed`/`TokenAnswerRefused`, the held object kept as it is, so it is served while it lives (T13). This needed a design choice, so it is **STOP-CLASS Q1**. The alternative "take it as a renewal" is mutant `mSameObjectAccepted`, and T13 is red under it.
- **Two STOP-CLASS questions for S4: Q1 (the same-object renewal) and Q2 (the empty identifier: LookupFailed against BindingRefused).** Both defaults are built.
- No rebase in this kit (D6/Q7). The branch stays on BASE and the gate reads the merge. So the hosted numbers are fixed: `--total 1668 --rules 530 --skipped-windows 21`.

## FACTS RE-MEASURED (instrument; control)
- Origin, `gh api -X GET` under the project `GH_CONFIG_DIR`, 00:01:47 and again 00:28:26: `main` `c480a0c81466f88102cb9d15a506b738615ebcbb` (= the commission's), open pull requests 0, `matching-refs/heads/b1935` 0. Pull requests 18 to 25 all closed and merged (list by GET).
- `main`'s push run: `hosted2.py c480a0c8... --total 1662 --rules 530 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan`, rc 0, `HOSTED c480a0c8...: PASS` (00:19:08). This matches the commission's relayed numbers.
- Toolchain: dotnet `10.0.404`, gitleaks `8.30.1`. Repo `.private` `true`, `.permissions.push` `true`, `gh auth status` logged in (count 1).
- At BASE, SignIn `Total: 57`, Universal Print `Total: 346`, both `Failed: 0`. `ls-files` 530.
- **Ruled-subject check, as the commission requires** (`/usr/bin/grep -i -c -F` over `CLARIFICATIONS.md`, sha256 `9c47b0d4...`, C-1 to C-68): `subscriber`, `MaxTapAge`, `StepTimeout`, `same object`, `same token`, `renewal`, `device token`, `all-zero`, `empty identifier` and `binding` all read 0. The positive control `tolerant` reads 5. I checked the five 2026-11-22 board lines the commission quotes by their subjects: card ids `datasec-oxpd-sqlserver-driver-identity-packages-1121`, `-jobs-second-review-nogo-test-1121`, `-tolerant-device-answers-1122`, `-ci-guards-round2-nogo-1122` and `-ci-guards-round3-nogo-1122`. None covers these subjects. Nothing in the kit is called undecided by the product owner. Every choice is labelled the coordinator's.
- `BACKLOG.md`: none of the four items is filed (`GetInvocationList`, `subscriber`, `Guid.Empty`, `same token object`, `MaxTapAge` all 0). The control `tolerant` reads 8.
- Panes: `Datasec/NexusAI-N163` live, no `Datasec/OXPd2-` pane, 0 named X37. `.tools/b1935` absent.

## WHAT I RAN (MEASURED; macOS arm64; every heavy job through `heavy.py` unchanged and the wave lock; lock waits 0 to 4; load1 1.76 to 6.84)
- Three draft clones (`clone`, `clone2`, `clone3`), each at `c480a0c8` with push URL `invalid://no-push`.
- RED: SignIn `Total: 62, Errors: 0, Failed: 5` and Universal Print `Total: 347, Errors: 0, Failed: 1`. The `[FAIL]` counts are 5 and 1, and each red is an assertion message.
- GREEN: both executables `Failed: 0`.
- Mutants: `mAuditOneTry` turned B08 red; `mEmptyTaken` turned B09 x3 and B10 red; `mSameObjectHeld`, `mSameObjectDisposed` and `mSameObjectAccepted` each turned T13 red. Every mutant was undone with `equal True`, and the stat was equal after each undo.
  - The first form of `mSameObjectHeld` (`answer is null && ...`) also reddened T05, T06 x2, T11 and L01, because it rewrote null-answer outcomes. I replaced it with a comparison against the cleared flight, which reddens T13 only. The first kept copy is in `_quarantine/pre-mSameObjectHeld-first`.
- Loops: SignIn 50 of 50 passed, Universal Print 10 of 10 passed.
- Chain, on a fresh clone with the patches applied by `git apply`: locked restore `--force` rc 0 with the 26 lock files equal; build 0/0; whole solution 1668 / 0 failed / 1664 / 4 skipped; publishes plus `GUARD: clean (10 files)` and `(11 files)`; `Ran 111 tests OK`; `RULES: clean (530 files)` (no `--source-documents`).
- Scans: `words.py` reads `WORDS: clean (2 files)` over 147 added lines and the message (control 13 of 13). `gitleaks` rc 0 on the clone and on 10 neutral files (control rc 1, quarantined). ASCII is clean in all seven files (control 1).
- `make_cells.py` and `make_fix.py` reproduce both patches byte for byte on `clone3`.
- Seven probes, run once on the fixed tree (files quarantined): P1 to P4 and Q1 to Q3, quoted in the kit's FACT 4.
- `stamp_check.py <kit>` exits 0: 177 claims, 177 measured.

## D-DECISIONS (all Tuesday's as coordinator; detail in the kit)
- D1 (a): one try per handler, in subscription order, with one shared immutable args object.
- D2 (b): the empty identifier is `LookupFailed` at the lookup. No token-side line is needed.
- D3 (c): the Limits lines are named, not asserted.
- D4 (d): the same object is refused and kept. The choice rests on `ICloudDeviceTokenIssuer.cs:9`, "the holder owns and disposes what it is handed".
- D5: four test methods, six cases, and one optional `Kit` parameter.
- D6: one commit on a new branch, no rebase.
- D7: public lines of three libraries equal to BASE (Secrets above all, per the commission).

## Q-QUESTIONS FOR TUESDAY (each with its default; Q1 and Q2 are STOP-CLASS)
- **Q1 (STOP-CLASS), the same-object renewal.**
  - Default a: refuse it and keep the held object (built).
  - b: accept it as a renewal. That makes an old token look fresh; it is mutant `mSameObjectAccepted`, and T13 is red under it.
  - c: copy every answer into a holder-owned token. Not built. It changes the ownership rule and still leaves an issuer that clears its answer early.
- **Q2 (STOP-CLASS), the empty identifier.**
  - Default a: `LookupFailed` at the lookup, with no audit.
  - b: `BindingRefused` with an audit, after an acquire.
  - c: both. The `:346` line would never be reached (an equivalent mutant).
  - Cost of a: no audit record of a defective identity service's empty answer.
- Q3, the fan-out form: one try per handler.
- Q4, the Limits lines: named only (the alternative is two limit cases).
- Q5, the Universal Print README limit (an issuer that keeps and later clears its token, or answers with a holder copy): named only. The alternative also refuses an answer whose `Origin` is set.
- Q6: Opus by `CLAUDE.md:7`.
- Q7: no rebase; READY at Step 0 + 120 and the push by Step 0 + 90; pane X37; gate G1 round 1.

## CHAIN INPUTS (DRAFTER_RULES measured-literals rule 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | kit, Stamp slots | Tuesday's stamp |
| 1 | `<src>` (10 files), `<repo>` local values, origin `main`, BASE push run | the drafter's scratch (exists); `<repo>`; GitHub |
| 2 | the seven files at BASE | the clone of Step 1 |
| 3 | both patches; the baseline build | Step 1 |
| 4 | the green tree; `mutants_f1.py`; the seat's loop script | Step 3; Step 1; written in Step 4 |
| 5 | the green tree, mutants undone; lock hashes; `surface_f1.py` | Step 4; Step 1 |
| 6 | the staged tree; `commit-message.txt` | Step 5; Step 1 |
| 7 | the staged tree; `run_step.py` | Step 6; Step 1 |
| 8 | the commit; `origin/main` | Step 7; Step 8's fetch |
| 9 to 10 | the commit; the origin | Step 7; GitHub |

## UNMEASURED / NEVER RUN
- Nothing ran on Linux or Windows. The hosted legs of a head of this lane are PREDICTED: linux 1668/1664/4, windows 1668/1647/21.
- `run_step.py`'s neutral scan wording is RELAYED from kit B1932 and was never run by me.
- `clone.py` was run in `draft` mode only, never `seat`. I made no commit, read no identity, pushed nothing and read no hosted run of a head.
- Whether a printer sends a late sign-out, and how a real device-token issuer hands over its answers, are both UNMEASURED; the README lines say so.
- "About 125 seconds" is DERIVED (5 + 4 x 30). P1 measured 121 s at 29 s per step.
- The "PREDICTED merge with a moved main" is not computed. Lanes A2 and F2 may land first; their paths are disjoint by the partition, and Step 8 checks the owned folders.

## OUTSIDE THE FENCES (disclosure)
- I made no write outside my kit, its sidecar, this report and `fleet/state/s312/d1935/`. In the project, Jira and GitHub I used reads only: `gh api -X GET`, git read verbs, and a `clone` into my scratch with push URL `invalid://no-push`. I made no fetch, commit or ref write in a project repo.
- I took the shared heavy lock through `heavy.py` for 35 jobs (`lock taken` lines in `d1935/logs/gate.log`: 35; quarantined lock folders 35; no lock left held), as the commission allows for its four drafters. I never broke another holder's lock.
- I used `sed -i` and in-place Python twice, only on my own files (the kit and `tools/fill.py`), never on a project file.
- Nothing under `Source_Documents/`, a key folder or the NAS library was opened, listed or hashed. No Jira call. No mail. No Artifact or Docs tool was used. I read no ledger, scoreboard, `briefs_staged`, decision card or other project.
- I quarantined rather than deleted: the probe files, the first `2-fix.diff` (before a README re-wrap), the first `clone2`, the first `mSameObjectHeld` copy and the gitleaks control, all under `d1935/_quarantine/`.
- The kit text carries no person's name and no card id (underscore-aware scan: 0; card ids 0; non-ASCII 0). Card ids appear only in this report's ruled-subject check.
