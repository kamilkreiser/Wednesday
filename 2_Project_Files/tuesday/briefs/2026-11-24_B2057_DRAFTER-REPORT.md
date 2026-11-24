STARTABLE: YES

# B2057 DRAFTER REPORT: OXPd L4, release guard (kit `2026-11-24_B2057_SEAT-X67_oxpd2-l4-release-guard.md`)

Read-only Opus drafter for Tuesday (s324), 2026-11-24 20:01:26 to 20:34:04 AEDT (`date`). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s324/d2057/` (below `<d>`). Kit sha256 `fa64414527d527dd42676f847d0ebee5880e0b6b875644e40f30a6f08baa16eb` (214 lines); sidecar `a8e18467463d9fc63c72ef93691930adcb15d641b4debf16175a9225983454f5` (164 claims, 164 measured, `stamp_check.py` rc 0). Seat tools frozen at `<d>/seat-tools/` (10 files, hashes in the kit).

## BLUF
1. **The lane as the sweep framed it is mostly already built.** Pull request 16 (`185b9eef`, 2026-11-22) landed release mode (owed 14's mode), the substring CA name and backslash split (owed 23's name rule), the library name in any NUL file, unopened archive formats as G3 (owed 11's symptom, fail closed), key stores in release mode, the two other PEM labels and UTF-16 PEM. BACKLOG items 11, 14 and 23 were never ticked (owed 50 says so for 19 to 23; 11 and 14 are not even named there). OXPD2-24 is still Backlog with 0 comments.
2. **What is left in the two files, and what the kit builds:** owed 23's "certificate forms not judged even when the list holds the fingerprint", two of them: **PKCS#7 in PEM** (labels `PKCS7`, `CMS`, `PKCS #7 SIGNED DATA`) and **base64 without PEM markers** (x5c JSON, bare or wrapped base64, `\n`-escaped, glued, in a ZIP member, in UTF-16). Both measured as gaps at BASE (red), both closed in the prototype and in a frozen replay.
3. **It needs ONE line outside the commissioned partition:** `.github/workflows/ci.yml:211` `FLOOR=111` to `FLOOR=115`. The project's own test (`test_pipeline_controls.py:9` and `test_unit_test_floor_equals_the_number_of_planted_controls`) fails `Lists differ: [111] != [115]` without it (MEASURED). No fingerprint moves (they read `FLOOR=N`). Q1, STOP-class.
4. **The coupling the commission asked about:** NO `GUARD:` line changes on either publish folder (MEASURED `GUARD: clean (14 files)` / `(15 files)` with the shipped list and with a list holding the test fingerprint; the new bare rule is dormant while the list is empty). The `rules` job's unit lines DO change: `Ran 111 tests` and `UNIT-TEST FLOOR: ran 111, floor 111` become 115. B2053 (X65, live) expects 111 in Step 5 and passes `--unit 111 --floor 111` to `hosted3.py`. **Landing order: B2053 first, then B2057.** B2056 (L3) is in the same position: whichever of L3/L4 lands second must carry the other's numbers (L3 moves `total:`, L4 moves `Ran`).

## FACTS RE-MEASURED (instrument, control)
- Origin (`gh api -X GET`, project `GH_CONFIG_DIR`, `gh auth status` = the Datasec account; `<d>/logs/origin.log`): main `89a10a1ba26a16aae7996e059d548bf53531fd44`; open PRs 0 (47 in all); `matching-refs/heads/b2057` 0, control `heads/b2048` 1; `.private` true. 48 branches; only `b1861/wp03-ci-guard-follow-ups` names the guard.
- History of the two files (`git log -- build/release_guard.py build/tests/test_release_guard.py` in a draft clone): 2 commits, `7bf3752` (PR 1) and `185b9ee` (PR 16).
- BACKLOG.md (sha256 `287c6663...`, 878 lines): owed 2, 11, 14, 23, 25, 50, 51 read whole; all of 2, 11, 14, 23, 25 still `[ ]`.
- Jira OXPD2-24 (GET only, in-process reader in the form of the project's `.tools/b1832/scratch/jira_get.py`, nothing of `.env` printed; `<d>/logs/jira.out`): Backlog, 0 comments, description read whole; `project = OXPD2 AND ( text ~ "release guard" )` 2 issues (OXPD2-24, OXPD2-8); control `zzqxnonexist` 0.
- Kit B1861 (PR 16's kit): its NOT DECIDED 1 (the packaging-job rule) and 2 (`.pdb`/`web.config`) are the two OXPD2-24 items still open; owed 50 confirms they stay open.
- CLARIFICATIONS.md (1114 lines, sha `f67eceaa...`): `release guard` 0, `release mode` 0, `deny-list` 0, `PKCS` 0, `x5c` 0, `.pdb` 0, `web.config` 0, `FLOOR` 0, `development CA` 0; control `OXPd` 250. No product-owner ruling on this lane.
- BASE hosted run (`hosted3.py ... --unit 111 --floor 111 --guard-linux 14 --guard-windows 15`, 20:25): `HOSTED 89a10a1b...: PASS`.
- Prototype + frozen replay (`<d>/clone`, `<d>/clone2`, and `<d>/clone3` for the red porcelain): red `Ran 115 tests`, `FAILED (failures=3)`, 3 `AssertionError`, 0 `ERROR:`; green `Ran 115 tests`, `OK`; mutants `10 of 10 MATCH, 10 of 10 undone equal`; chain: restore `--force` locks 34 of 34 equal, build 0/0, `total: 2153` `failed: 0`, both publishes, guard 14 and 15 clean, `Ran 115` OK, `RULES: clean (659 files)`; `checks_l4.py` 10 of 10; `WORDS: clean (2 files)`; gitleaks control rc 1, scans rc 0.
- Seat id X67 free: word scan of 214 non-`.pre-`/non-`.measured` SEAT kits of 2026-11-17 to 2026-11-24: `X67` 0 kits, `X66` 0; control `X65` 1 kit (B2053). Live OXPd pane: `Datasec/OXPd2-X65` only.
- Model: `models_latest.json:17` `claude-opus-5-5`; `<project>/CLAUDE.md:7` newest Opus.

## D-DECISIONS (in the kit as Tuesday's defaults)
D1 scope = the two forms; D2 three explicit PEM labels (not any label); D3 bare base64 only while the list is non-empty, runs >= 128 chars, four alignments, padding repaired; D4 one appended class of 4 cases + 3 helpers, no landed case touched; D5 `FLOOR=115`; D6 one commit, push by sha, rebase before first push only, no local CodeQL.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q1 STOP-class, the third path:** default a = add ONE line of `ci.yml` (`FLOOR` 111 to 115) to the partition. Alt b = fold rows into landed cases (no `FLOOR` move, no coupling; landed cases change, re-draft). Alt c = no build lane, records only.
- **Q2 STOP-class, scope:** default a = the two forms only; tar/gzip stay G3 (not opened); OXPD2-24's job rule and `.pdb`/`web.config` stay NOT DECIDED. Alt b = also open tar/gzip members. Alt c = add `--release` to the publish steps (every job red until owed 2's fingerprint exists; product owner's).
- **Q3 STOP-class, landing order:** default = after B2053, and after B2056 if B2056 is ready first; whichever lands after L4 carries `--unit 115 --floor 115`. Alt = L4 first and stamped unit lines in B2053/B2056.
- Q4 root `README.md:67` (G2 form list now incomplete, not false): default untouched. Alt: a fourth path.
- Q5 bare-rule bounds: default as built. Alt: also base64url and an escaped slash.
- Q6 OXPD2-24 NOT DECIDED 1 and 2: default not built, no Jira move.
- Q7 commit subject: default the kit's (231 chars, words clean).
- Q8 local CodeQL: default not run; the PR's CodeQL (Python is in the default setup, owed 3).
- Q9 Opus, READY Step 0 + 100 min, push by + 75, pane `Datasec/OXPd2-X67`, gate G1 round 1 of lane L4.
- **Recommended to Tuesday (not a seat question):** the records pass can tick or narrow owed 11, 14, 23 with PR 16 as the closing source, independently of this lane.

## UNMEASURED
- Hosted Linux and Windows behaviour of the change (PREDICTED only; the unit tests run in the `rules` job on Linux).
- RFC 7468 label names `PKCS7`/`CMS` (from knowledge, no web read this drafting); `PKCS #7 SIGNED DATA` as an older label.
- A compressed .NET single-file host carrying the library (no bundle built; carried from kit B1861 H13).
- The bare rule's cost on a large base64 file beyond the publish folders (0.03 to 0.04 s each, MEASURED).
- Whether the CodeQL Python extractor runs on this Mac (not tried).

## CHAIN INPUTS TABLE (rule 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | kit, Stamp slots (S4: Q1 to Q3) | Tuesday's stamp |
| 1 | `<d>/seat-tools/` (10 files), `<repo>` local values, origin, BASE push run | exists (drafter's scratch); exists; GitHub |
| 2 | files at BASE | Step 1 clone |
| 3 | `1-red.diff`, clone at BASE | Step 1 |
| 4 | `2-fix.diff`, `mutants_l4.py`, red tree | Step 1; Step 3 |
| 5 | green tree, mutants undone | Step 4 |
| 6 | staged tree, `checks_l4.py`, `words.py`, `commit-message.txt` | Step 5; Step 1 |
| 7 | commit, `origin/main`, `run_step.py`, `hosted3.py` | Step 7a; fetch; Step 1 |

## STOP-SEVERITY CHECKS RUN ON MY OWN OUTPUT (each PASS, control FIRED)
Tool hashes; prior-work greps (rc 1 x3; control prints `HEAD:build/release_guard.py:1`); red by assertion 3 of 3; mutants 10 of 10; checks 10 of 10 (each control fires); locks 34 of 34; rules 659; gitleaks rc 0 (control rc 1); words clean (control 13 of 13); guard lines 14 and 15. NEVER RUN: seat-mode clone, commit, neutral scan of a commit, push, read-back, hosted run of a head, rebase, CodeQL.

## WHAT I RAN, WHERE, AT WHAT LOAD (rule: no test run beside a lock without leave)
The commission allowed runs in my scratch clone with heavy jobs through the project's runner. Eight dotnet jobs through `heavy.py` (owner `B2057 drafter`): `d-restore`, `d-publish-linux`, `d-publish-windows` in `<d>/clone`; `c-restore-force`, `c-build`, `c-test`, `c-publish-linux`, `c-publish-windows` in `<d>/clone2`. Lock waits 0 to 7 per job; load1 5.5 to 6.9 at start; one publish pair waited about 3 minutes for load under 7. Seat X65 was live and sharing the lock; I never touched its owner file (the lock folder was absent at 20:34). Python unit runs and mutants (not heavy) ran unlocked in my scratch clones.

## OUTSIDE-THE-FENCES DISCLOSURE
- No write to any project, Jira, GitHub or card store. Project git: READ verbs only. Writes only under `<d>/` and the three deliverables.
- One hook refusal before it ran: `git -C "$K" apply ...` (the hook read the unexpanded variable as outside TUESDAY; re-run with the literal scratch path, inside my scratch).
- One mistyped no-op: `sed -i '' ... /dev/null` failed at once ("in-place editing only works for regular files"); nothing was edited.
- One zsh-refused separator (`echo ======`) before it ran.
- Superseded scratch moved, never deleted: `<d>/_quarantine/1-red.diff.first-proto`, `mutants-proto-9rows/`, `sidecar-v1-circular.measured` (a first sidecar fill that used the claim listing itself as evidence; discarded and redone), `gl-control/`.
- Jira: GET only (one issue, two searches with the required `project = OXPD2 AND ( ... )` form). No credential printed.
- Nothing to any human; no other client read.
