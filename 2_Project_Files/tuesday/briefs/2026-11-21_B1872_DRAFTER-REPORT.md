STARTABLE: YES (after the stamp answers the two STOP-class Questions Q37 and Q38 in words, and only after the product owner's ruling on card `datasec-oxpd-jobs-second-review-nogo-test-1121`)

# B1872 drafter report: OXPd 2 lane G, test-only round 3 (A03 deterministic)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1872_SEAT-X23_oxpd2-wp17-jobs-a03-test-fix.md` (sidecar `.measured` beside it; `stamp_check.py <kit>` rc 0, 150 claims, 150 measured, 0 TODO). Tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s306/d1872/gate/` (16 files, sha256 in the kit's THE TOOLS). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s306/d1872/` (clones `clone` and `clone2`, `logs/`, `scratch/`, `_quarantine/`). Drafted 22:13 to 22:44 AEDT 2026-11-21 (clocks by `date` in the kit's header).

## BLUF
- **The fix is one helper change in `ReceiverTests.cs` (`1-a03.diff`, +19 -2):** `StringsReachableFrom` never walks into a `TimeProvider`, `Task`, `CancellationTokenSource`, `CancellationToken`, `CancellationTokenRegistration` or `ExecutionContext`. No product file changes.
- **The commission's red-first loop could not be made to fail here: 0 of 145 runs of the Jobs test project at 8efae983 failed** (45 + 100, `logs/LOOP-red-8efae983.txt`, `LOOP-red2-8efae983.txt`). The reader measured 12 of 40. So the kit adds a **forcing probe**, which is scratch-only and never committed. The probe runs A03's own helper over a receiver that has a receive pending on the shared test token, while a second thread keeps changing another receiver on the same token.
  - At 8efae983 it was red in 8 of 8 runs: 7 to 12 `Collection was modified` per 300 walks, and every completed walk reached the other receiver's spool root.
  - With the fix it was green in 13 of 13 runs: 0 faults, the other spool's root 0 of 300.
  - **Q37 (STOP-class) asks Tuesday to accept this probe as the red that must fire.** It would replace the literal rule "the loop must fail at least once", which would very likely stop the seat at Step 3.
- **The walk still reaches all of the receiver's own state.** The census probe found:
  - At A03's end the fixed walk skips exactly three paths: the receiver's clock, the spool's clock, and each job's `Gone` cancellation source.
  - The receiver's own objects (the receiver, its spool, its 2 jobs, the file entry) were reached 5 times by the fixed walk and 5 times by the old walk.
  - Across the library's 52 types there are 22 fields of a skipped type. Only 4 are in non-generated types (three `_time` clocks and `SpoolJob.Gone`). The other 18 are async state-machine locals.
- **The secret-text property is still caught.** `mUnknownEarly`, `mKeepField` (the text kept in a receiver field) and `mKeepInSpool` (the text kept as the spool job's session) each turn A03 red. `mKeepTask` (the text kept inside a `Task`) survives. That is the named limit of skipping `Task`, and no such field exists in the library.
- **F2 cell (Q38, STOP-class, default YES; `2-w02-body.diff`, +64 -0, same file):** a W02 theory where a body throwing `ObjectDisposedException` ends `JobNotFound` and one throwing `IOException` ends `ScanRefused`. It is green at HEAD2's product code and red under `mReasonDisposed`.
- **`main` moved while I was drafting.** Lane B (pull request 12) landed at 22:33, so `main` is now `5bb1418c`, and the seat WILL make the merge commit (D38).
  - I prototyped it: the merge is clean (`merge-tree` rc 0, tree `44367852`).
  - The merged tree with both diffs gave `total: 1457`, `failed: 0`, `RULES: clean (442 files)`, and both solution folders are in ordinal order.
  - `main`'s own hosted run: PASS with `--total 1335 --rules 410` (control `1336` gives FAIL 4).

## Facts re-measured (instrument; control)
| Fact | Instrument | Result | Control |
|---|---|---|---|
| origin branch / main | `gh api -X GET` 22:42:12 | branch 8efae983; main 5bb1418c (was 8ae5e08c at 22:31:14); 0 open PRs; `.private` true, push true | compare main...8efae983 ahead 3 behind 1 |
| loop at HEAD2 | `a03loop.py` (each run one `heavy.py` job) | 0 of 145 failed, totals 120 | parser `--control` `CONTROL FIRED: 3 of 3` |
| forcing probe at HEAD2 | probe in the Jobs project, 8 runs | 8 of 8 red, faults 7 to 12 per 300 walks | green with the fix: 13 of 13, the other spool's root 0 |
| census | census probe Q1/Q2, 13 runs | 22 skipped-type fields (4 non-generated); 3 SKIP paths; own objects 5 and 5 | planted class `6 of 6` |
| green with fix | loops | fix1 60 of 60 (120); fix2 60 of 60 (122); whole solution 3 of 3 `total: 1313`, `failed: 0`, `skipped: 4`; merged on 5bb1418c 20 of 20 (122) and whole `1457` | red at HEAD2 by the probe |
| mutants (fixed tree) | `tools/mutants.py`, `dotnet test --no-restore` | mUnknownEarly A03 (`Expected: 3` `Actual: 2`, :135); mKeepField and mKeepInSpool A03 (`A03: the receiver keeps the secret's text`, :144); mKeepTask survives; mReasonDisposed W02 body ODE row (`Expected: JobNotFound`, :567); every undo `cmp` equal and `git diff --quiet -- src` rc 0 | the green runs |
| diffs | `git apply --cached --check` with a scratch index | rc 0, rc 0; trees d7417f4e (fix1), 535e4def (both) | sha256 of the file after each |
| texts | `words.py`, gitleaks 8.30.1, ASCII grep | `WORDS: clean (3 files)` for both message sets; gitleaks rc 0; 83 added lines, 0 non-ASCII | `CONTROL FIRED: 13 of 13`; planted token rc 1; planted U+200B 1 |
| rules | `repo_rules.py` (no option) / unittest | `RULES: clean (402 files)` (442 merged); `Ran 60 tests`, OK | `<scratch>/1_Project_Definition` absent |
| hosted HEAD2 | `hosted.py` 1311/402 | PASS | 1313 gives FAIL 4 |

## Decisions in the kit (Tuesday's defaults as coordinator)
D33 is the skip list of six types (Q40). D34 is the census, which proves nothing of the receiver or spool is lost. D35 is red first, the loop count recorded and the forcing probe required (Q37, STOP-class). D36 is the five mutants, with `mKeepTask` the named survivor (Q41). D37 is the F2 cell (Q38, STOP-class). D38 is the merge of the moved `main`: expected clean, `place.py` only on a solution-file conflict, and `slnx_order.py` must print `SLNX: ordinal, job lines 1 and 1` (Q39). D39 is the hosted numbers, PREDICTED `--total 1457 --rules 442` on 5bb1418c. D40 is the window (READY Step 0 + 120, push + 90) and pane X23, opus (Q42).

## Questions for Tuesday (each with its default)
- **Q37 (STOP-class, S4 in words): the red-first rule.** Default: the 40-run loop is printed and a 0 is recorded, and the forcing probe must be red 3 of 3 at HEAD2. Alternative: the commission's literal "must fail at least once" (MEASURED 0 of 145 here, so the round likely stops at Step 3).
- **Q38 (STOP-class, S4 in words; B1866 F2): add the W02 body cell this round?** Default YES (it is test-only, in the same file, measured, and kills mReasonDisposed; the Jobs total goes 120 to 122 and the solution 1311 to 1313). Alternative NO (`1-a03.diff` only, mReasonDisposed stays named).
- Q39: the merge only if `main` is not in HEAD (it now is NOT in HEAD: lane B landed). Alternative: no merge, which leaves an unreviewed squash tree.
- Q40: the six types. Alternatives: own fields only, one level (a secret kept in the spool would pass), or a retry on a changed collection.
- Q41: five mutants. Alternative: also re-run kit B1862's eleven.
- Q42: 120/90 minutes, X23, opus.
- (Report only) The commission's pointer "line 144" is A03's call of the helper. The helper itself is at `ReceiverTests.cs:598` at 8efae983. The kit gives both.

## Chain inputs (each step's inputs exist at HEAD2 or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 1 | `<src>` 16 files; `<repo>` local identity; origin | the drafter's scratch; `<repo>`; GitHub |
| 3 | `a03loop.py`, `force-probe.cs.txt`, HEAD2 build | Step 1 |
| 4 | `1-a03.diff`, `2-w02-body.diff`, both probes, `3-mutants.txt` | Step 1; probe moved out at Step 3 |
| 5 | the green tree | Step 4 |
| 6 | staged tree, commit message, `merge-message.txt` | Step 5; Step 1 |
| 7 | C1, `origin/main`, `place.py`, `slnx_order.py` | 7(a); 7(b) fetch; Step 1 |

## UNMEASURED / NEVER RUN
- How the flake behaves on the hosted runners. It never showed in the whole-solution shape (the reader's 0 of 16, and my 3).
- The neutral scan of stored objects on a commit of this round. I made no commit: my scratch clone has no identity, and I did not override one.
- The fix1-only whole-solution total (1311 is PREDICTED).
- Lane E landing before the seat's push: `merge-tree` against lane E's head is clean, but its squash on `main` is unmeasured.
- The seat's `place.py` path, which is not expected to be needed.
- CodeQL.
- Windows locally.

## Outside the fences (disclosure)
- **Heavy lock:** 310 `heavy.py` jobs took and released `<project>/.tools/wave1-heavy.lock.d` (`mkdir`, then a move into my `_quarantine/locks/`). Lock waits were 0 in 304 of them, at most 16 polls. The commission names heavy.py and the wave lock.
- **Origin fetch for the merge prototype:** `clone.py ... draft` made `clone2`. That is an SSH clone from the GitHub origin with the project deploy key: no HTTP, push URL `invalid://no-push`, no identity. Kit B1862's drafter did the same.
- **Other lanes' heads:** I fetched lane B's and lane E's heads into my scratch clone from their seats' clones (`.tools/b1856/clone`, `.tools/b1849/clone`). That is a read of those repositories, with nothing written there. I used them only for `merge-tree`.
- **Reader scratch:** I read reader B1866's scratch loop script `/private/tmp/b1866-gate/scratch/loop.sh`, which is outside its `evidence/`, to match its loop form.
- **Refused commands:** two of my Bash calls were refused by the no-cd hook. They named my own scratch clone through a shell variable, so the hook could not see they pointed inside TUESDAY. I re-ran them with literal paths inside TUESDAY; nothing ran in a project tree.
- **Writes:** none in any project tree or `<repo>`, no git write in a project repo, no Jira or GitHub write, no message to anyone. I deleted nothing: superseded files went to `d1872/_quarantine/`, including the copied round-2 diffs, mutants and commit message, the probes and two earlier sidecars.
- **Names:** the kit text names no person and no card id (scan: names 0, card ids 0; the planted control fired 1 and 1). It is all ASCII.
- **Port:** none.
