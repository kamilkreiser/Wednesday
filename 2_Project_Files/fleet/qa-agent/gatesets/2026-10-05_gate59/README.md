# Gateset 2026-10-05_gate59 — README for Wednesday

Drafted 2026-10-05, 05:41Z – 06:09Z UTC (16:41 – 17:09 AEDT; times from `date -u`). Every figure below names the kit file it came from.

## 0. What this gate is, and its status

**gate59 is a T1 gate over ONE Secuura/Blockchain PR: #1382, KS-1005, "change-password reads the hash it verifies".**
- Built by Seat E 1st as `4346bc7fbdf8`. Seat E 2nd merged develop in, pushed and raised it. Seat E 2nd is the merger. Pane `Secuura/Blockchain-E`.
- **The head is a MERGE-IN**, folded before the first push (Wednesday's ITEM 0 ruling 3):
  - head `80bafc849a54a9368810fd0fcd1ee1184fa608bf`
  - parents `4346bc7fbdf8` (built) and `46c3e20cfbd2` (develop = #1380's squash)
  - END_TREE `ada5b278269eb34e6cf3d3bb304f517137562fe4`
  - branch `feature/ks-1005-change-password-reads-the-hash-it-verifies-e2-1`
- **Exactly 4 paths differ from develop:**
  - the new ks1005 test (+203)
  - `services/auth/src/routes/users.ts` (+8/-1: one loader line plus comments)
  - the flow doc (+51)
  - the cheat doc (+35)
- Q-M = gate57's M1-M4 (ruling 4). The gate judges the head itself by M1-M4. It also judges any LATER merge-in with `c4_docs_gate59.py qm`.
- The kit is in `kit.json` and is quoted in the prompt.

**Status: KIT COMPLETE, NOT LAUNCHED.**
- Every checker has a positive control and must-fail tamper arms. All of them were run and all fire (section 3).
- The live dry run returns rc 0. It reports only the routing line as missing (`dry_console_ex2.out`; re-run with this final README as `dry_console_ex3.out`, rc 0 at 06:11Z, develop and head unmoved).
- Two things are Wednesday's: the routing line (section 4) and the launch (section 5).

**What the drafter did:**
- Wrote only into this directory and into `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/b72c1f78-0eff-4438-a1d7-6dcd846422fb/scratchpad/g59/`.
  - That scratch holds a `git clone --shared --no-checkout` of the checkout (`clone/`).
  - ONE fetch went into it (05:41:47Z) of develop, `refs/pull/1382/head` and `refs/pull/1381/head`, using the checkout's own `core.sshCommand`.
  - It also holds one worktree `wt/` at the head, with `npm ci --ignore-scripts` (rc 0) and a built `packages/shared` (`dist/index.js` 17,746 bytes).
  - The scratch is 2.1 GB and was left in place (no `rm`).
- In `/Volumes/DevMASTER/!CODING/`, ran only read verbs: `ls-remote`, `config --get`, `show`, `ls-tree`, `cat-file`, and the `clone --shared` source read.
- Network use was all reads:
  - GitHub REST GETs (pulls, files, compare, the open-PR census). GH_TOKEN was read by name and never printed.
  - ONE Linear GraphQL read of KS-1005 (description sha256 prefix `c505bd0c2b15a072`, 2,835 chars, In Progress, 0 comments, attachment = PR #1382). LINEAR_API_KEY was read by name and never printed.
  - The npm registry, for `npm ci` only.
- Not done: no launch, no routing edit, no mail, no comment, no ticket change, no `rm`.
  - Probe and test overlays were MOVED to `scratchpad/g59/out_*/quarantine/`.
  - Refusal arms used scratch paths only: `G59_FORBIDDEN_ROOT` was pointed at `scratchpad/g59/fakeroot`, a scratch stand-in.
- Python wrote a `__pycache__/` here on import, as gate57's kit did.

## 1. Drafter predictions on #1382 at 80bafc849a54 over develop 46c3e20cfbd2 (the gate re-derives every one)

| check | file | result |
|---|---|---|
| C1 pin | `c1_pr1382_ex1.out` (rc 0, 8/8) | ls-remote pull/head == branch == API == input; open, base develop == ls-remote develop; parents [built, develop]; the built commit is single-parent on `3ce8cd4026a6` with tree `42d9531f0562`; 4 paths with exact +/- by numstat AND API; END_TREE equal (control: develop tree `dab6adb69ea3` differs); trailers empty on head and built (control `bf277eead268` = 53 bytes stripped); declared subject 51 chars, byte-equal to the built subject, `(#` 0 |
| C2 hunk | `c2_pr1382_ex2.out` (rc 0, 5/5) | ONE non-comment change, the loader line; 7 comment lines carry KS-1005 and "was getUserById"; the loader is the ONLY assignment to `user` and nothing writes it before `verifyPassword(data.currentPassword, user.passwordHash)`; the 404 guard is byte-identical and on the next code line; `getUserById(` 8 → 7, survivors byte-identical; userRepo.ts identical (USER_COLS 31 columns, no password_hash; control mfa_secret present); the WithPasswordHash SELECT names password_hash. INFO: `return fromRow(` WITHOUT await (KS-999 sibling), no tenantId param; class census 11 `.passwordHash` readers, with a must-hit control |
| C3 red-first | `c3_redfirst_ex2.out` (rc 0) | at DEVELOP with the head's test written in: A, B, C, D red, each an `AssertionError`. A "expected 404 to be 200"; B "expected 404 to be 400"; C "expected 0 to be greater than 0"; D "expected 404 to be 200". E and F green, 6 ran, 0 load failures. Moved out, status clean. Head 6/6 |
| C3 suite | `c3_suite_ex1.out` (rc 0) | services/auth vitest: develop **840 tests / 78 files / 0 failed**, head **846 / 79 / 0 failed**; 0 new reds. **The ks949 timeout class did NOT recur** (0 NAMED); the 6 KS-1005 cells passed in the full run |
| C3 tsc | `c3_tsc_ex1.out` (rc 0) | tsc 5.9.3: rc 0 at develop and at head. Positive control (planted TS2322 in users.ts, landing asserted) → rc 2, restored by sha256, status clean. tsconfig excludes `src/__tests__` |
| C3b probe | `c3b_probe_ex2.out` (rc 0) | at develop: P1, P2, P4, P5 RED by assertion (404 received) and P3, P6, T1 green. At head 7/7. Timing medians of 7 (ms, mocked db, real argon2id), wrong / right / passwordless: develop 0.61 / 0.41 / 0.40; head **25.9 / 51.2 / 0.53** |
| C4 docs | `c4_docs_ex1.out` (rc 1, 6 FAIL of 18) | PASS: D1 §4, D2 same commit, D3 one pure insert per doc (51 at flow :2067, 35 at cheat :3812, == `  </body>`), D4 numbers [1..12, 19] with h3 19.1 / 19.2, D5 byte-identical to the built commit's inserts, D6a. **FAIL (findings carried as BASELINE, section 2): D6b, D7 ×4, D8** |
| C4 predict | `c4_predict_ex1.out` (rc 0, 5/5) | merge-tree develop × built rc 1 on EXACTLY the two docs; the independent number-order resolution == `ada5b278269e` == head tree (control: 19-above-12 gives `dce903dec85d`); parents; remerge-diff touches only the two docs; 0 trailers. **The READY's "M1 CANNOT be met by a plain merge-tree" is answered: a deterministic resolution reproduces the tree** |
| C5 PR text | `c5_pr1382_ex1.out` (rc 0, 6/6) | Refs + URL; 0 closing keywords; only KS-1005 hyphenated (KS 749 / KS 1333 de-hyphenated); title == declared subject; who-ran-what stated; head / tree / parents / "exactly four paths" / "0 trailers" == kit. Body 6,589 bytes / 6,542 chars, sha256 `f66c4bed2856da49…` |
| C6 NOT COVERED | `c6_pr1382_ex1.out` (rc 0, 3/3) | one `## NOT COVERED` section, carrying session revocation, live sweep §5f, ks949, and the auth suite unmeasured at the head. INFO: the ticket's reset-token flow is NOT named |
| census | `census_ex2.out` (rc 0) | 22 other open PRs; **0 touch routes/users.ts** (control: the classifier FIRES on #1382 itself); 1 EXPECTED OVERLAP: #1381 (both docs, head `82e6bfa9de85`) |
| Q-M later merge-in | `c4_selftest_ex3.out` | if #1381 lands as its merge-in tree `ba3527224ff6` squashed onto `46c3e20c` (SIM develop `57303348831f`), #1382's second merge-in conflicts on exactly the two docs and is predicted at tree **`df1344507d8cc13d23a767914ee85046c019a30c`** (19 after 13). Recompute with `qm` on the REAL develop |

**Drafter's reading:** every artefact claim in the READY reproduces. The open items are rulings, not measurements.

## 2. Doubts for the GATE to rule (the prompt carries all of them), and READY contradictions

- **D1 PREFLIGHT INCOMPLETE 12/15.** The seat cannot name its three skipped legs. gate57 measured legs 3 / 4 / 8 for #1381. For #1382 it is UNMEASURED. The kit has no preflight instrument. The prompt lets the tester run `preflight.sh` in its own worktree.
- **D2 The cheat block is not wrapped** in `<div class="section">` (C4 D6b), unlike its neighbours KS-1404 and KS-1333. The same is true in the built commit, so it is not a merge artefact.
- **D3 The blocks are not self-contained per doc** (C4 D7):
  - the flow block names neither the test file nor how to run it;
  - the cheat block has no §5f / live-sweep line and no NOT-covered note.
  - gate57 required both, per doc.
- **D4 The §4 timing statement** (C4 D8):
  - The docs say "0 hits … must-hit control 3".
  - The PR body says "7 mentions … control 11" and calls a "3" its own false-positive first grep.
  - The kit's duration-proximity instrument (develop): services/auth near a duration = 0 in both file sets. The Akto control = **10** (CLAUDE.md + systemTest/CLAUDE.md + skill) and **11** (both docs + skill).
  - So the body's 11 reproduces on its own set. **The docs' "3", which stays in the repo, does not.**
  - Three inserted rows carry a duration with the date+host only in a sibling row: the ks949 row in each doc, and the "<= 20 min" budget quote.
- **D5 The docs' 19.2 figures are E 1st's at `4346bc7fbdf8`** over `3ce8cd4026a6`: "At head 6 passed", "79 files / 846 tests, 844 passed", the 2 ks949 reds.
  - The gated head is `80bafc849a54`. The drafter measured 846 / 79 / **0** failed there.
  - "At head" in a doc that now sits under a merge-in is ambiguous.
- **D6 The PR's control F does not prove what its comment says.** It sends `'short'` (5 chars), and zod's `newPassword: z.string().min(8)` refuses that before the route body. checkPasswordStrength is never reached. Probe P4 (`'password1'`) proves the strength gate is reached at head and is red at develop.
- **D7 A product comment in users.ts reads "ruled by Wednesday 2026-10-05, not incidental".** That is an internal coordinator's name in client source.
- **D8 `getUserByIdWithPasswordHash`** (userRepo.ts, unchanged by this PR) returns `fromRow(...)` WITHOUT `await`. This is the KS-999 class that #1013 fixed in getUserById.
  - A throw inside fromRow on the now-live change-password path escapes the 503 classifier.
  - It also takes no tenantId, so RLS rests on the ALS tenant GUC. That is UNMEASURED without Postgres.
- **D9 Timing.** Passwordless answers 404 before any hash work (0.5 ms vs 26-51 ms). The route is self-scoped (`req.user.userId`), so no OTHER account is enumerable through it. Information unless the gate finds otherwise.
- **D10 SESSION REVOCATION (the sharpest open question).**
  - Before this PR, no password could change through this route. Other sessions staying live was therefore unreachable.
  - After it, a user who changes a compromised password leaves the attacker's sessions live.
  - The reset flow (`auth.ts:846`) does not revoke either. Only the admin status path (`users.ts:826`) and the erasure subscriber call `revokeAllUserSessions`.
  - Is that a Major a T1 GO cannot carry, or named residue for a ticket? The PR names it in NOT COVERED.
- **D11 Develop race.** #1381 (block 13.) is GO'd for a merge-in head, and Seat B 61st is commissioned to merge it.
  - If it lands before the launch, the launch refuses rc 10.
  - If it lands after the verdict and before #1382 merges, #1382 needs a second merge-in, judged by `c4_docs_gate59.py qm` (predicted `df1344507d8c…`).
  - **Wednesday sequences this** (see W1 below).

**READY contradictions / notes the drafter found (none blocks the artefact):**
1. **"Q-M M1 … CANNOT be met by a plain merge-tree … The resolved tree is mine BY CONSTRUCTION".** An independent, deterministic number-order resolution reproduces `ada5b278269e` exactly (C4 M1), and the wrong-order control differs. M1 IS met.
2. **"tsc … positive control" listed as NOT RUN by the seat.** The kit ran it (rc 2, TS2322).
3. **"the full auth suite at THIS head" listed as NOT RUN.** The kit ran it: 846 / 79 / 0 failed. The ks949 timeouts did not recur.
4. **§4 timing:** the READY / body figure (11) and the docs' figure (3) disagree with each other (D4).
5. Consistent, for the record: head, develop, END_TREE, parents, 4 paths, 70-char merge subject, 0 trailers, 1937 packages, `dist/index.js` 17,746 bytes, the 6-cell pass.

**For Wednesday (not the gate's):**
- **W1 sequencing.** Either hold B 61st's #1381 merge until #1382 has merged on its GO, or accept that #1382 then needs a second merge-in (a new head) before it can merge. The gate's verdict covers that head under Q-M only if `qm` passes on the real develop. A launch after #1381 lands refuses rc 10.
- **W2.** KS-1005 sits In Progress via the integration. It is the gate's to report, Wednesday's to rule.

## 3. The kit's instruments (each exercised; outputs beside it as `<name>_exN.out/.err/.rc`)

| script | what it does | positive control | must-fail tamper arms (all fired) |
|---|---|---|---|
| `lib_gate59.py` | `git()` read verbs only; `wgit()` write verbs only outside `/Volumes/DevMASTER` (lexical + realpath); `guard_out`; GH; `move_out` (shutil.move, gate57's EXDEV fix); `selftest_arm` | — | `refusal_arms_ex1.out`: c3 worktree, c3b `--out`, c4 clone via a SYMLINK into the stand-in root → rc 2 each, 0 entries created |
| `c1_pin_gate59.py` | P1-P8 | `c1_pr1382_ex1` (rc 0); selftest T0 | `c1_selftest_ex1` **10/10**: base-vs-base, 5th path, +/- drift, single parent, trailer, `(#1382)`, 93 chars, develop moved, API head moved. Real control `c1_basehead_ex1` (head = develop) rc 1, failing P1 / P3 / P4 / P5 |
| `c2_hunk_gate59.py` | H1-H5 + INFO H6 | `c2_pr1382_ex2` (rc 0); T0 | `c2_selftest_ex2` **7/7**: 404→400 (H3), a 2nd site switched (H4), loader kept (H1), KS-1005 stripped (H1), passwordHash cleared before verify (H2), USER_COLS widened (H5). `_ex1` = history (H4 bug: all 8 call lines are identical text; fixed to remove ONE occurrence) |
| `c3_redfirst_gate59.py` | redfirst / suite / tsc | the real runs (rc 0); R-0, R-7, S-0, S-1 (a ks949 timeout NAMED, S2 stays green) | `c3_selftest_ex2` **12/12**: loadfail, F red, D red by TIMEOUT, green develop, E red, A red with 500, unknown new red, ks1005 file missing. tsc positive control in the real run. `_ex1` = history (fixture bug) |
| `c3b_probe_gate59.py` + `c3b_probe_ks1005_gate59.test.ts.txt` | the gate's own 7 cells at develop and head | head 7/7; selftest D-0, H-0 | **develop run IS the must-fail arm on real code** (P1 P2 P4 P5 red); `c3b_selftest_ex1` **7/7** (P3 red, P1 no flip, loadfail, P4 timeout, P2 red at head). **`_ex1` = PUBLIC SELF-CORRECTION:** the drafter's P2 asserted "exactly ONE users SELECT" and went red at head with 2. The second SELECT is updateUser's post-write read-back (`getUserById`, userRepo :796-:926). That was a wrong premise, not a finding. P2 now asserts the FIRST SELECT is the only one naming password_hash |
| `c4_docs_gate59.py` | docs D1-D8, predict M0-M4, qm M0-M5 | `c4_predict_ex1` (rc 0); T0 baseline-aware; Q0 | `c4_selftest_ex3` **12/12**: 2nd block edited (D3), 19→20 (D4), one byte (D5), cheat h2 numbered (D6a), live-sweep removed (D7); Q-M on a SIM develop-after: extra users.ts edit (M1 + M3), 19 above 13 (M1), single parent (M2), trailer (M4). Real control `c4_docs_basevsbase_ex1` rc 1 (15 FAIL). The baseline = the 5 real findings (D2 / D3); an arm counts only a NEW failure. `_ex1` = history (T5 plant inert) |
| `c5_prtext_gate59.py` | T1-T6 | `c5_pr1382_ex1` (rc 0); T0 | `c5_selftest_ex1` **7/7**: Refs removed, `Closes KS-1005`, KS-1210 hyphenated, `(#1382)` title, attribution removed, head sha altered |
| `c6_notcovered_gate59.py` | N1-N3, section-bounded | `c6_pr1382_ex1` (rc 0); T0 | `c6_selftest_ex1` **5/5**: revocation removed, live sweep moved above the heading, heading removed, a 2nd heading |
| `gh_census_gate59.py` | API line + census | `census_ex2` (control FIRES on #1382) | `census_selftest_ex1` **5/5**; live arm `G59_REPORTED={}` → rc 15 |
| `fill_gate59.py` | fills prompt + launcher + pins | the dry fills | changed READY → rc 1; moved develop → rc 1 |
| `launcher_gate59.TEMPLATE.sh.txt` | the launcher (gate58's guards; compare ahead 2 / behind 0 / 4 files; 27 keywords) | SIM `--check` rc 0 (`dry_console_ex2.out`) | stale pin 9, develop moved 17, head moved 6, no TTY 21 (never reached `exec claude`); empty README → 8 (`dry_console_060454_README-empty.out`) |
| `repin_and_launch_gate59.sh` | the launch action | `--dry-run` rc 0 | short sha 9, wrong PR 9, wrong head 11, census 15 |

All `*.SIM.*` and `pins_gate59.SIM-*.json` files are exercise output and are never launched. The real `pins_gate59.json` does not exist until the real launch writes it.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1005-1382|coagent@agentmail.to|yes
```
Until that line is present, step 0 of the real launch refuses rc 1. The dry run reports it instead.

## 5. Not adapted / not measured
- No preflight instrument: D1 is the tester's, with an optional run.
- No real Postgres or stack, so RLS, the tenant GUC and the live sweep are all NOT TESTED.
- The `qm` judge has only run on SIM merge-ins. No real second merge-in exists.
- The doc-number mapping for `qm` places the KS-1005 block before the first flow `<h2>` numbered > 19 (else before `</body>`), and in the cheat sheet by the same keys' flow numbers. A future block without a `(KS-n)` flow heading would not be ordered.
- The c6 seed-list matching is a KEYWORD HEURISTIC, labelled as such.

## 6. Re-draft recipe (the head or develop moved)
1. Re-fetch into a scratch clone.
2. Re-measure kit `head`, `end_tree`, `develop`, `develop_tree`, `files` (+/-), `blobs`, `flow_numbers_*`, `block_lines`, `hunk.*`, `pr_body_read`, `reported_overlaps` (re-run `gh_census_gate59.py --json`).
3. Re-run every `--selftest`, then `c1`, `c4 predict`, `c3 redfirst`, and a `--dry-run`.
4. A second merge-in after #1381 changes `parents` (P3: [80bafc849a54, new develop]); C1 P3 then needs the gated head in place of the built commit.

## 7. How Wednesday launches it (after section 4's routing line)
The pane is `QA/Secuura-ks1005-1382`. The report dir is `…/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1005-1382-g59/`. The GO the gate expects is `GO (Seat E 2nd): merge 1382 on gate59`. The verdict subject is kit `verdict_subject_template`.

Exit codes:
- rc 1: routing.
- rc 9: input.
- rc 11: the head moved, or is not the kit head.
- rc 10: develop moved (RE-DRAFT), or the fill refused.
- rc 15: overlap, or #1381's head moved.
- rc 12 / 13 / 14 / 16: usage gate / `--check` / cockpit / override.

Add `WED_USAGE_STOP=…` only with Kam's recorded authority.
```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate59/repin_and_launch_gate59.sh 1382 80bafc849a54a9368810fd0fcd1ee1184fa608bf --dry-run
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate59/repin_and_launch_gate59.sh 1382 80bafc849a54a9368810fd0fcd1ee1184fa608bf
```
