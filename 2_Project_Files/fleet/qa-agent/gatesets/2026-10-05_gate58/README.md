# Gateset 2026-10-05_gate58 — README for Wednesday

Drafted 2026-10-05, 03:15Z – 03:40Z UTC (14:15 – 14:40 AEDT; times from `date -u`). Every figure below names the kit file it came from.

## 0. What this gate is, and its status

**gate58 is a T1 gate over ONE Secuura/Blockchain PR: #1379, KS-749, Seat F 1st's advisory bump.** Seat F 1st is both author and merger. The PR changes exactly 7 paths against develop `3ce8cd4026a6e3241413e9c7533d5a84d10c1c79`:
- browserslist 4.28.7 in 6 locks (root, admin, outlook-addin, verifier, governance, referral), plus caniuse-lite / electron-to-chromium / node-releases only where a lock pins them below 4.28.7's floors;
- postcss-selector-parser 6.1.4 in the root lock;
- in all, 23 lock entries;
- 3 rows removed from `scripts/audit/audit-baseline.json` (c83g, 73wf, w9m9, each `expires 2026-10-15`).

Its purpose is to clear the fuse that freezes every Secuura push at 2026-10-15T00:00Z (11:00 AEDT Thu 15 Oct).

Authority:
- Kam's cards `secuura-four-advisories-ruled-after-measurement` = bump and `secuura-five-new-advisories-block-every-push-0929` = a.
- Wednesday's 13:30 ANSWER: ONE PR `Refs KS-749`, both bumps and all three rows. KS 751 is ARCHIVED and is never written hyphenated.

The kit is in `kit.json` and is quoted in the prompt.

**Status: KIT COMPLETE, NOT LAUNCHED. Two things are Wednesday's: the routing line (section 4) and the launch (section 5).** The full dry run on #1379 / dd398f2d14db returned rc 0, with only the routing line reported missing (`repin_dryrun_ex2.out`).

**What the drafter did:**
- Wrote only into this directory and under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/707ca275-d40c-45a7-8ba2-785b7c4e078a/scratchpad/gate58/`. That scratch holds a `git clone --shared --no-checkout` of the checkout and ONE fetch of `develop` + `refs/pull/1379/head` made with the checkout's own `core.sshCommand`. It also holds two worktrees, `wt_head` / `wt_base`, with their `npm ci` installs. The scratch is 4.2 GB and was left in place: the brief says no `rm`.
- In `/Volumes/DevMASTER/!CODING/`, ran only read verbs: `ls-remote`, `show`, `cat-file`, `rev-parse`, `ls-tree`, `log`, `diff`, `config --get`. `lib_gate58.git` refuses any other verb.
- Network use was all reads:
  - GitHub REST GETs: the PR, its files, the open-PR census and the launcher's compare. GH_TOKEN was read by name and never printed.
  - The npm registry: packuments and 10 tarballs hashed in memory, `npm ci` / `npm audit` inside the legs.
- Not done: no launch, no routing-line edit, no mail, no comment, no ticket change, no `rm`.
- Refusal arms ran only with paths inside the scratch. The `G58_FORBIDDEN_ROOT` override points the forbidden root at a scratch dir.

## 1. Drafter predictions on #1379 at dd398f2d14db (the gate re-derives every one, at the head it pins)

| check | file | result |
|---|---|---|
| C1 pin | pred1379_c1.out | **PIN PASS 6/6**: ls-remote pull/head == branch == dd398f2d14db; API open, base develop @ 3ce8cd4026a6 == origin; 1 parent == develop, ahead 1 / behind 0; **END_TREE f550361a829a == the READY's claim** (develop tree 7716438b02ad, the control that differs); API files == numstat == the 7 paths, +92/-103; 0 trailers (control bf277eead268 prints 1) |
| C2 lockdiff | pred1379_c2.out | **LOCKDIFF PASS 48/48**, 23 of 23 ruled entries: 0 unruled, 0 added/removed, 0 flag flips, libc/os/cpu equal (referral libc 10 -> 10). Root key order: 328 of 328 entries carry resolved+integrity after `version` at head (323/323 at base). Maps sorted; every line hunk inside a ruled entry; 0 unsatisfied dep-family edges. **L8: the kit's own surgical edit of each BASE lock == the head, byte for byte, on all 6 locks** |
| C3 integrity | pred1379_c3.out | **INTEGRITY PASS 12/12**: the 5 tarballs recomputed == kit == registry dist.integrity, sha1 == shasum. Negative control: each old tarball matches its own value and not the new one, and a flipped byte changes the hash. Across 45 tracked locks, every entry at a new version carries the recomputed integrity (browserslist 6, psp 4, caniuse 6, e-t-c 6, node-releases 6) |
| C4 baseline | pred1379_c4.out | **BASELINE PASS 5/5**: 25 -> 22, removed exactly {73wf, c83g, w9m9} (each the base's 2026-10-15 row), 0 added, 22 rows byte-equal in order, `$comment` byte-present, 21 deleted lines all inside the three blocks, 0 inserted, 2026-10-15 cohort 3 -> 0, 2026-10-31 4 -> 4 |
| C5 legs, head | pred1379_c5_run.out | **LEGS OK**: leg 2 rc 0 ("All 35 standalone lock(s) pass"); **leg 5 rc 0, tests 59, fail 0** (== expected-case-count 59); legs 6 / 7 rc 0 at today's clock AND frozen at 2026-10-15T00:01Z; 0 of the 3 ids in any output; leg 6 "7 distinct advisories reported, 22 baselined" |
| C5 base control | c5_runbase_ex1.out | **OK**: base today legs 6/7 rc 0/0. **Base FROZEN: leg 6 rc 1, LAPSED c83g, 73wf, w9m9; leg 7 rc 1, LAPSED c83g, 73wf** |
| C5 bite | pred1379_c5_bite.out | **BITE OK**: no-op copy rc 0/0. Root reverted: leg 6 rc 1 naming all three NEW. Governance reverted: leg 7 rc 1 naming c83g + 73wf in `services/governance`. Each lock restored (sha256 back, git status clean) |
| C5 install-root | pred1379_c5_install.out | **OK**: `npm ci --ignore-scripts` rc 0, **added 1937**; root lock sha256 `8a3568d53fb8…` identical before/after; on disk 4.28.7 / 6.1.4 / 1.0.30001814 / 1.5.444 / 2.0.57 |
| C6 scope | pred1379_c6.out | **SCOPE PASS 12/12**: S1 the 7 paths; S2 0 test paths (control hits 1951); S3 0 runtime/manifest; S4 15/15 instrument files blob-equal; S5 mobile lock blob 2f5f8c1f4edf unchanged, KS-769 / 2027-01-01, browserslist 4.28.1 PROD; S6 100644 (control 100755). K1-K4: only KS-749 hyphenated on title/body/commit/branch, `Refs KS-749`, no closing keyword, 0 archived-key hits. K5: the scanner fires 4x on the base baseline. N1: mobile/secuura-app and "CSS build diff" after the NOT run / Not covered headings |

**Drafter's reading:** every claim the READY makes about the artefact reproduces. The open items are the doubts below, which are rulings and not measurements.

## 2. Doubts for the GATE to rule (the prompt carries all of them), and READY contradictions

- **D1, PREFLIGHT INCOMPLETE 12/15.** Legs 3 / 4 / 8 were SKIPPED (no stack on localhost:6882) and are not a pass. The gate starts no stack. The tester rules on them, using C6 S1 / S3 / S4: a lock + baseline-only diff with no instrument moved.
- **D2, METHOD-STATED.** The seat ran no dedicated lock differ (by ruling). C2 here is the gate's own, including a byte-for-byte reconstruction (L8).
- **D3, the frontend CSS build diff is UNMEASURED.** caniuse-lite drives autoprefixer, and admin / verifier / outlook-addin are deployable. The tester measures it if budget allows, or rules NOT COVERED acceptable at T1.
- **D4, mobile/secuura-app.** PROD 4.28.1, dormant to 2027-01-01. Information.
- **D5, 15 pre-existing CLEANUP rows** (KS 470 / KS 559), printed at base AND head. Follow-up owed.
- **D6, root `npm ls` 6 invalid packages**, claimed identical at base and head. Not re-measured by the drafter.
- **D7, co-tenants.** Branches cut from 3ce8cd4026a6 (B 60th, E 1st) red legs 6+7 after 15 Oct until they merge develop in.
- **D8, PR-BODY-CLAIMS.** The contradictions are listed below.
- **D9, KS-749's bot move to In Progress.** Wednesday's.

**READY contradictions the drafter found (none blocks the artefact):**
1. **"body … 8,857 bytes"**: GitHub returns 8,944 BYTES (UTF-8). 8,857 is the CHARACTER count. The sha256 prefix `343abb4938f0d43c` does match, over the bytes.
2. **"of 1,970 root entries, 323 carry resolved+integrity and 323 of 323 …", "measured in the target file"**: 323 is the BASE count. At the head it is **328 of 328**, the 5 new entries included. The PR body repeats the 323 figure. Its "1,647 neither-or-one" is also the base figure (1,615 with neither + 32 with exactly one), which does correct P14's 1,582.
3. **The READY mail itself writes the archived key hyphenated** (≈7 times: the leg-output quotes and the TICKETS section). The PR / commit / branch are clean (C6 K1-K5). Information only: the 13:30 ruling governs the artefacts.
4. Consistent, for the record: +92/-103, 7 files, END_TREE, the 59 cases, 1937 packages, lock sha256 `8a3568d53fb8…`, leg 6 3 LAPSED / leg 7 2 LAPSED under the freeze, "35 standalone locks", and the five on-disk versions all reproduce.

## 3. The kit's instruments (each exercised, outputs beside it as `<name>.out/.err/.rc`)

| script | what it does | exercised runs (rc) |
|---|---|---|
| `lib_gate58.py` | helpers; `git()` read verbs only; `guard_out` / `guard_worktree` (forbidden root, lexical + realpath); semver range reader | `lib_semver_selftest_ex1` (16/16) |
| `c1_pin_gate58.py` | C1 P1-P5 + P3b END_TREE vs the READY | pred1379_c1 (0); **`c1_basehead_ex1` (1: head = develop fails P1/P2/P3/P3b/P4)**; **`c1_filesdrop_ex1` (1: a planted 6-path expectation fails P4 naming verifier)**; `c1_shortsha_ex1` (2) |
| `c2_lockdiff_gate58.py` | C2 L1-L8 + `--selftest` T0-T11 | **`c2_selftest_ex3` (0, SELFTEST OK 12/12)**. Arms: base-vs-base fails L1 on 6 locks; the legit reconstruction PASSes; a dev flip, a libc removal, a **libc MOVE (semantic pass, LINE fail)**, an extra entry, an added entry, the **#1373 key order** (L4 root only), un-sorted maps (L5), **browserslist-only (L7: governance 3 unsatisfied)**, an os change and an old integrity each FAIL on the named check. `c2_basevsbase_ex1` (1, 0 of 23 changed). `ex1`/`ex2` = history (T10 plant bug: every arch array here has ONE element, measured; fixed to alter the element) |
| `c3_integrity_gate58.py` | C3 I1-I4, `--plant <pkg>` | pred1379_c3 (0); **`c3_atbase_ex1` (1: I4 fires, 23 ruled entries old)**; **`c3_plant_ex1` (1: e-t-c with the old integrity fails I3 in 6 locks)** |
| `c4_baseline_gate58.py` | C4 B1-B5 + `--selftest` T0-T7 | **`c4_selftest_ex2` (0, 8/8)**: base-vs-base, two-only, an extra row, a re-escaped arrow (bytes), a re-date instead of removal, a planted row and a json.dump re-serialisation each fail as named. `c4_basevsbase_ex2` (1). `ex1` = history (B1 instrument bug: `$comment` byte-test needed `ensure_ascii=False`; fixed) |
| `c5_legs_gate58.py` + `c5_freeze_clock_gate58.cjs` | C5 `plan` / `parse-selftest` / `freeze-selftest` / `run head|base` / `bite` / `install-root` | `c5_plan_ex1` (0: S0 `<=` at baseline-contract.mjs:141, utcToday :93, AUDIT_BASELINE_PATH :46/:64, 59); `c5_parse_ex1` (0); **`c5_freeze_base_ex1` (0: pins 2026-10-15T00:01:00.000Z; UNSET -> 97; garbage -> 97; no preload -> real day; the tree's own utcToday/isLapsed 2026-10-15 / true / false / false)**; `c5_runbase_ex1` (0, base control); **base-as-head controls: `c5_base_as_head_ex1` (1: frozen legs 6/7 MISMATCH), `c5_bite_atbase_ex1` (1: reverts bite nothing), `c5_install_atbase_ex1` (1: on-disk versions old)**; `c5_refusal_ex1` (2: a devdir under the (scratch-overridden) forbidden root refused, outdir NOT created, `c5_refusal_ls_ex1`) |
| `c6_scope_gate58.py` | C6 S1-S6, K1-K5, N1 + `--selftest` T0-T8 | pred1379_c6 (0); **`c6_selftest_ex1` (0, 9/9)**: base-vs-base S1; the archived key hyphenated in the body / as `ks_751` in the title / hyphenated in the commit, mobile line gone, CSS line gone, `Closes KS-749`, Refs line gone each fail on exactly the named check. `c6_basevsbase_ex1` (1) |
| `gh_census_gate58.py` | API read + open-PR census | `gh_census_ex1` (0: 21 others, 11 overlaps, recorded in kit.json `reported_overlaps`); `gh_census_ex2` (0: 0 unexpected) |
| `fill_gate58.py` | fills prompt + launcher + `pins_gate58.json` | `fill_help_ex1` (0); SIM fills inside the dry runs |
| `launcher_gate58.TEMPLATE.sh.txt` | the launcher (gate54f's guards; files=7; refuses a prompt carrying the archived key hyphenated) | SIM `dry033720.SIM.launcher.sh`: `--check` 0 (inside `repin_dryrun_ex2`); `launcher_stale_ex1` (9); `launcher_wronghead_ex1` (6); `launcher_movedev_ex1` (17); **`launcher_archivedkey_ex1` (8)**; `launcher_notty_ex1` (21: no `--check`, stdin /dev/null, refused at the TTY guard, never reached `exec claude`) |
| `repin_and_launch_gate58.sh` | the launch action | **`repin_dryrun_ex2` (0: full dry run on #1379 / dd398f2d14db; routing reported missing)**; `repin_dryrun_wronghead_ex1` (11); `repin_shortsha_ex1` (9); `repin_dryrun_census15_ex1` (15: `G58_REPORTED=control_reported_empty.json`). `repin_dryrun_ex1` = the first dry run (0), before the launcher's `--check` wording fix |
| `prompt_gate58.TEMPLATE.txt` | the tester's prompt (24 by-name keywords, 0 hyphenated archived key) | filled as `dry03*.SIM.prompt.txt` |

All the `*.SIM.*` and `pins_gate58.SIM-*.json` files are exercise output. They are never launched. The real `pins_gate58.json` does not exist until the real launch writes it.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks749-1379|coagent@agentmail.to|yes
```
Until that line is present, step 0 of the real launch refuses rc 1. The dry run reports it instead.

## 5. How Wednesday launches it
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate58/repin_and_launch_gate58.sh 1379 dd398f2d14db554c47550925fd80761ca9298dfa --dry-run
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate58/repin_and_launch_gate58.sh 1379 dd398f2d14db554c47550925fd80761ca9298dfa
```
Add `WED_USAGE_STOP=…` only with Kam's recorded authority. In one action it:
1. Reads the PULLS API and runs the census (rc 15 on an unexpected overlap).
2. Runs ONE `ls-remote`.
3. Refuses rc 11 unless HEAD == API == pull/head == branch, open, unmerged, on develop, and the branch matches `^feature/ks-749-[a-z0-9-]+-f1-1$`. Refuses rc 10 if develop moved.
4. Fills the prompt, the launcher and `pins_gate58.json`.
5. Re-reads develop and the head.
6. Runs the override check (16), `usage_gate.sh --check` (12), the launcher's `--check` (13; a pin older than 30 min is exit 9), then `cockpit.sh add` (14).

The pane is `QA/Secuura-ks749-1379`. The GO the gate expects is `GO (Seat F 1st): merge 1379 on gate58`. The report dir is `…/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks749-1379-g58/`.

## 6. What I could not adapt, or did not measure
- **D3 (the CSS build diff) and D6 (`npm ls` invalid set) are not measured by the kit.** The prompt hands both to the tester as budget items.
- **A develop move is a RE-DRAFT (rc 10), not a re-pin.** C2's expectations and L8 reconstruction, C4's 25/22 rows, C5's base control and C6's 15 instrument blobs are base-blob-specific. No automatic re-measure exists.
- The advisory database is live. Every leg 6 / 7 reading above holds for 2026-10-05 ~03:30Z.
- Leg 5 runs real gates. A freeze is never applied to it: it runs at today's clock, as the preflight does.
- No Linear read. KS-749's state is the READY's report.
- The scratch worktrees (4.2 GB, with `node_modules`) remain. Moving or deleting them is Wednesday's call at drive hygiene; the drafter may not `rm`.

## 7. Re-draft recipe (develop moved, or the change is not this one)
1. Re-measure the base: kit.json `base`, `base_tree`, `base_blobs`, `locks.*.{expected_changes.from, libc_base, os_base, cpu_base, base_blob}`, `baseline_rows_base`, `mobile_lock_blob`. Re-run `gh_census_gate58.py --json` and refresh `reported_overlaps`.
2. Re-run the C2 / C4 / C6 `--selftest`, the C3 at-base run, C5 `plan` + `run … base`, and a `--dry-run`.
