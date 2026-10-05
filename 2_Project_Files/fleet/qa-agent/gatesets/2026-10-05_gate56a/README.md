# Gateset 2026-10-05_gate56a — README for Wednesday

Drafted 2026-10-05 AEDT; work 2026-10-04 23:53Z – 2026-10-05 00:2xZ UTC. Each figure names the kit file it came from.

## 0. What this is, and its status
**gate56a is a T2 gate over TWO Secuura/Blockchain PRs, both raised and merged by Seat B 59th on ONE READY and TWO GOs:**
- **PR 3 — KS-528:** `Blockchain/Dev/scripts/audit/audit-baseline.json`, the two react-router rows (GHSA-wrjc-x8rr-h8h6, GHSA-337j-9hxr-rhxg) `expires` 2026-10-09 -> **2026-10-31**. Subject `KS-528: the two react-router baseline rows are re-dated to 2026-10-31` (69).
- **PR 4 — KS-769:** `Blockchain/Dev/scripts/audit/lock-discovery.mjs` `:209`, the mobile-tree 'dormant but kept' exclusion `expires: '2026-10-19'` -> **`'2027-01-01'`** (comment `:202-:208`). Subject `KS-769: the mobile-tree dormant exclusion is re-dated to 2027-01-01` (67).
- **Base:** develop `14d40d4455c7da3c31c71d614fc7c4d1d4ffc2fb` (#1376's squash; tree `6d96b6e81275` == `57fa9e31d7ce`'s, the stale shared checkout's readable stand-in). Origin develop re-read by `ls-remote` at 2026-10-04T23:53:57Z and 2026-10-05T00:05:02Z: unmoved (`c1_basestate_live_ex1.out`).

**Status: KIT COMPLETE, NOT LAUNCHED, NOT LAUNCHABLE until the READY.** PR numbers / heads / branches are inputs: `repin_and_launch_gate56a.sh <n3> <head3> <n4> <head4> [--dry-run]`. Two things are Wednesday's: the routing line (section 4) and the launch (section 5). The SIM dry run (section 1) returns rc 0 with only the routing line reported.

**What the drafter did:** wrote only in this folder and under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/b2564a3d-…/scratchpad/g56a/`. In the shared Secuura checkout ran only `ls-remote`, `show`, `cat-file`, `rev-parse`, `log`, `ls-tree`, `grep` (lib `git()` refuses other verbs). Base-side content was read from the scratch clone `…/8e88f5e9-…/scratchpad/vclone` (holds 14d40d44). Head-side runs used SYNTHETIC edits: scratch files (`g56a/syn/`) and four SIM commits made with plumbing in a scratch `clone --shared` (`g56a/simrepo`, `sim/make_sim_gate56a.py`). Network: two unauthenticated GETs of `api.github.com/advisories/<GHSA>` (captured in `advisories/`). **Not done:** no fetch into any project repo, no clone or worktree of the Secuura repo beyond the scratch `--shared` clone of the scratch vclone, no `.env` read, no mail, no launch, no `inbox_routing.conf` edit, no `rm`, no read of the gateD2 report (the SIM fill used a scratch stand-in via `G56A_PREV_REPORT`).
**Refusal arms:** C3's OUT guard was driven with a scratch stand-in root (`c3_refusal_ex1.out`, `c3_refusal_ls_ex1.out`: nothing created). **One lapse to report:** `make_sim_gate56a.py`'s own refusal arm was driven ONCE with the literal path `/Volumes/DevMASTER/!CODING/zz_should_not_exist`; it refused before any write and `ls` confirmed the path absent — against the commission's "scratch paths only" rule; not repeated.

## 1. Drafter predictions (base = REAL; head = SYNTHETIC, never evidence)
| check | file(s) | result |
|---|---|---|
| C1 base state | `c1_basestate_live_ex1.out` (rc 4) | develop == kit base by live ls-remote; both base blobs == kit; trailer + mode controls fire. **"NO PR YET", never a PASS.** Control `c1_basestate_stalelocal_control_ex1.out` (rc 1): ls-remote from the scratch clone reads the shared checkout's STALE local develop `c56dd7c32edf` — FAILS B1/B2 (why c1 runs ls-remote in the checkout by default, `--remote-repo`). `c1_basestate_vclone_ex1.out` is that same fault before the fix. |
| C1 SIM | `c1_sim_good3_ex1` / `c1_sim_good4_ex1` (rc 0, 13/13), `c1_sim_sibling_ex1` (rc 0: SIBLING-ADVANCE, develop = PR 3's squash, PR 4 ahead 1 / behind 1), `c1_sim_bad4_ex1` (rc 1: P5 trailer, P6 `(#9905)` suffix, P7 a second hyphenated key), `c1_sim_wrongwhich_ex1` (rc 1, 8 FAIL: PR 4 judged as PR 3), `c1_shortsha_ex1` (rc 2) | PASS on the right shape, FAIL on each planted fault |
| C2 selftest | `c2_selftest_pr3_ex1` 10/10, `c2_selftest_pr4_ex1` 7/7 | intended edit (and edit + appended reason note / rewritten comment) PASS; wrong date, one row only, third row, row added/removed, reason rewritten, reordered, re-indented; 2026-12-31, code line, second literal, ticket, field added — each FAILS its own row |
| C2 base / synthetic | `c2_basestate_pr{3,4}_ex1` (rc 4), `c2_basestate_standin_pr3_ex1` (rc 4, read at 57fa9e31d7ce in the shared checkout), `c2_basevsbase_pr{3,4}_ex1` (rc 1), `c2_syn_good_pr{3,4}_ex1` (rc 0), `c2_syn_extrarow_pr3_ex1` (rc 1: J3 + J6, base line 137), `c2_syn_wrongdate_pr3_ex1` (rc 1: J4), `c2_syn_wrong1231_pr4_ex1` (rc 1: L3), `c2_simcommit_*` (good rc 0, bad4 rc 1 L3) | as designed |
| C3 | `c3_syn_good_pr3_ex2` (rc 0, 14/14), `c3_syn_good_pr4_ex2` (rc 0, 10/10), `c3_simcommit_good{3,4}_ex1` (rc 0), `c3_basestate_pr{3,4}_ex1` (rc 4) | see the table below |
| C3 FAIL arms | `c3_syn_wrongdate_pr3_ex1` (2026-11-01: A5 + G3 FAIL — the fuse no longer blows on 31 Oct), `c3_syn_extrarow_pr3_ex1` (a third row re-dated: A6 FAIL), `c3_syn_wrong1231_pr4_ex2` / `c3_simcommit_bad4_ex1` (2026-12-31: A4 FAIL — dead on 31 Dec, ~24 h early), `c3_basevsbase_pr{3,4}_ex2` (A2/A3/A4 + G2 FAIL) | each wrong edit caught |
| C4 | `c4_syn_good_pr{3,4}_ex1`, `c4_syn_good_pr3_live_ex1` (live advisory GET), `c4_simcommit_good{3,4}_ex1` (rc 0); `c4_syn_rowadded_pr3_ex1` (S1), `c4_syn_pkgchanged_pr3_ex1` (S2), `c4_syn_keyadded_pr4_ex1` (S1), `c4_syn_reasonchanged_pr4_ex1` (S2) rc 1; base state rc 4 | react-router 6.30.6 in 4 locks (root, admin, issuer, verifier), inside `>= 6.0.0, < 7.18.0` and `>= 6.4.0, < 7.18.0`; controls 7.18.0 / 5.3.4 OUTSIDE; mobile lock `2f5f8c1f4edf` |
| C5 | `c5_selftest_pr{3,4}_ex1` 6/6, `c5_simbody_pr{3,4}_ex1` rc 0 (8/8), `c5_crossbody_control_ex1` rc 1 (PR 4's body judged as PR 3's) | cards ruled a with the kit timestamps and labels; grant verbatim present; ANSWER carries ``write `2027-01-01` `` and names 2026-12-31 WRONG |
| census | `census_clean_ex1` (SAME-KEY reported), `census_overlap_ex1` (OVERLAP on the baseline) | SIM only |
| dry run | `repin_dryrun_ok_ex1.out` (= `dry_001252.*`, rc 0; routing line REPORTED absent; SIM launcher `--check` rc 0) | SIM. Earlier `dry_001111.*` rc 13 (README not yet written) and `dry_001241.*` rc 13 (launcher bug: the per-PR loops' `set --` clobbered `$1`, so `--check` fell through to the TTY refusal; fixed with `MODE` captured first) are kept as history. |
| launch refusals | `repin_dryrun_overlap_ex1` rc 15, `repin_dryrun_movedhead_ex1` rc 11, `repin_dryrun_staledev_ex1` rc 10, `repin_shortsha_ex1` rc 9; SIM launcher `launcher_stalepin_ex1` exit 9, `launcher_badcompare_ex1` exit 10, `launcher_notty_ex1` exit 21 | each arm fires |

**C3 measured lapse semantics (both files, at base 14d40d4455c7):**
- `isLapsed`: `Blockchain/Dev/scripts/audit/baseline-contract.mjs:141` **`return expires <= today;`** (:131 signature `isLapsed(entry, today = utcToday())`; malformed -> lapsed :140; absent -> never :133). `utcToday`: `:93` `new Date().toISOString().slice(0, 10)` (UTC). **No env/arg clock knob exists** (`git grep process.env` in scripts/audit: only `AUDIT_BASELINE_PATH`, `AUDIT_ADVISORY_STUB`, timeouts) — hence the Date-stub preload.
- PR 3 readers: leg 6 `audit-gate.mjs:191` `const today = utcToday();` + `:197` `isLapsed(entry, today)` (preflight.sh:419-420); leg 7 `audit-locks.mjs:283/:289` (same pair; the frontend locks carry react-router too). CI `.github/workflows/security-scan.yml` runs audit-gate.mjs.
- PR 4 reader: `lock-discovery.mjs:258` `isLapsed(entry)` (default today) inside `validateOutOfScope` (:239), called by `findStandaloneLockDirs` (:312) <- `audit-locks.mjs:148` (leg 7), and by the leg-5 contract case `lock-discovery.test.mjs` "the real OUT_OF_SCOPE_LOCKS validates against the real repository".
- So a written day D is **dead from D 00:00:00Z, valid THROUGH D-1 (UTC)**: 2026-10-09 -> through 10-08; **2026-10-31 -> through 2026-10-30**; 2026-10-19 -> through 10-18; **2027-01-01 -> through 2026-12-31**. Measured at the day edges (23:59:59.999Z alive / 00:00:00.000Z dead) in `c3_syn_good_pr{3,4}_ex2.out` A1-A5; the real audit-gate.mjs agrees (G1 base rc 1 both ids LAPSED @10-10; G2 head rc 0 @10-10; G3 head rc 1 @10-31; G4 control rc 1 NEW; G5 control rc 0 @10-08T23:59:59.999Z).

## 2. Doubts for the GATE (the drafter rules none)
- **D1** Other fuses: GHSA-c83g-rgw3-j3cx, GHSA-73wf-gq98-2v4g (browserslist), GHSA-w9m9-85wc-3x92 (postcss-selector-parser) lapse **2026-10-15 00:00Z** (seen in A6 at 10-30); GHSA-ggr8-5vv4-36mx and GHSA-vfj7-8cjw-p6xm on 2026-10-31. After PR 3 lands, the next push freeze is **15 Oct**, not 31 Oct. Not this gate's to fix — Wednesday's to card.
- **D2** PR 3's literal 2026-10-31 is valid only through **30 Oct** under `<=` (the card said "to Sat 31 Oct"). The ANSWER ruled "write the literal anyway, say valid through 30 Oct": c5 B3 checks the body says so.
- **D3** PR 4's comment `:205-:208` at base describes the OLD date ("end of Sunday 2026-10-18", "lapses 00:00Z Mon 19 Oct"). If kept unedited it is false of 2027-01-01: c2 WARN L6 prints it (it fired on the drafter's minimal synthetic, which left the comment alone).
- **D4** The `branch_rx` (own key lower-case, sibling's absent) is the drafter's convention, not a measured seat plan: a branch named otherwise makes the launch refuse rc 11 and c1 P2 FAIL — Wednesday may loosen `prs.*.branch_rx` in kit.json before launch.
- **D5** c3 runs the extracted modules, not a full install: leg 5 (the audit:contract suites, incl. the real-repo OUT_OF_SCOPE case), leg 7's registry half, the pre-push hook and CI are not run. G1-G5 use a CANNED `npm audit` report naming only the two advisories (so G2's "OK" says nothing about other advisories).
- **D6** SIBLING-ADVANCE: if one PR merges first, the other is behind 1. c1 P3 accepts exactly that (sibling subject + sibling path only); the prompt asks for the combined tree. The launch itself requires develop == kit base (both open).
- **D7** PR 3's numstat with appended reason notes would be +4/-4 (the reason strings are one line each, ~900 chars); c2 J5 prints the note for the tester to read — the allowance is "append only", not "any text".
- **D8** The 81 mobile-tree advisories (2 critical, 45 high) are the code comment's figure, not re-measured; C4 proves only that the lock blob is unchanged.

## 3. Instruments (each exercised; outputs `*_exN.*` beside it)
`lib_gate56a.py` (read verbs only, `guard_out` lexical+realpath before mkdir, `pr_cfg`, `side_text`); `c1_pin_gate56a.py` (help 0, short-sha 2, base-state 4, SIM pass/fail/sibling); `c2_diffshape_gate56a.py` (selftest 10/10 + 7/7; base-state 4; base-vs-base FAIL); `c3_clock_gate56a.py` + `c3_freeze_clock_gate56a.mjs` + `c3_probe_gate56a.mjs` (K0 self-test, A1-A6, G1-G5 / D1; base-state 4; base-vs-base FAIL; OUT refusal); `c4_security_gate56a.py` (live + fixture advisories, 4 fail arms); `c5_notcovered_gate56a.py` (selftest 6/6 x2, cross-body control); `gh_census_gate56a.py` (clean / overlap SIM); `fill_gate56a.py`; `prompt_gate56a.TEMPLATE.txt` (21 keywords); `launcher_gate56a.TEMPLATE.sh.txt`; `repin_and_launch_gate56a.sh`; `sim/make_sim_gate56a.py` + `sim/` fixtures; `advisories/` (drafting-time captures). gateD2's lock-diff / integrity / legs / PKI / docs scripts and gate55's regen / cells / handler scripts were NOT copied: they do not apply to a date-only edit.

## 4. Routing line — NOT added
Back up `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`, then add, with PR 3's real number:
```
QA/Secuura-ks528-769-<n3>|coagent@agentmail.to|yes
```

## 5. Launch
From Seat B 59th's READY take both PR numbers and FULL heads, then `repin_and_launch_gate56a.sh <n3> <head3> <n4> <head4> --dry-run`, then without `--dry-run`. rc 10 on develop != kit base (section 7); rc 11 on a head / branch-rule mismatch; rc 15 on an OVERLAP. The launcher's compare wants, per PR, `develop ahead=1 behind=0 files=1 paths=<its path>`.
SIM dry run: `dry_<HHMMSS>.*` with `G56A_ROUTING` (empty scratch file), `G56A_CENSUS_OFFLINE=sim/census_clean`, `G56A_LSREMOTE_FILE=sim/lsremote_ok.txt`, `G56A_PREV_REPORT` (scratch stand-in), `G56A_COMPARE_FILE=sim/compare_ok.txt`, PRs 9903 / 9904 at the SIM heads.

## 6. Not adapted / not measured
- No PR exists: every head-side figure is SYNTHETIC. The real bodies, branches, numstat and reason notes are unseen.
- No live GitHub API call (no `.env` read): c1's API half, the census and the launcher's compare ran only as SIM replays. The real launch path (steps 4-7) is unexercised.
- gateD2's report was not read or hashed (the fill records its sha256 at launch; no pinned value was found in the brain).
- The leg-6 run is end-to-end on the real script but with a canned `npm audit`; legs 5 and 7 and the pre-push hook were not run.

## 7. Develop moved before launch, or a new head
1. If develop moved by something OTHER than these PRs: re-read both paths' blobs at the new develop; if unchanged, update kit.json `base`, `base_tree`, `base_parent` (and re-run c1 `--base-state`, c2/c3 `--selftest` / base-state); if either path changed, RE-DRAFT C2/C3 expectations. 2. `repin_and_launch_gate56a.sh … --dry-run`.
