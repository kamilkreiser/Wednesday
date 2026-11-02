# QA Gate 116 verdict (TIER 2): Secuura/Distributed_Secuura PR 1934 (KS-1413, start-up banners no longer echo the demo password)

## BLUF
**GATE 116 (TIER 2) on PR 1934 at 7e0918b74977: GO WITH NOTES. Nothing has to be fixed before merge.**
Both banner lines that echoed `demo123` are gone; the new line names the account and points at CLAUDE.md. The product change is two comment+echo pairs (+2/-1 each) and nothing else in either script. The "secret" is a hard-coded published demo default (also written in the repo's CLAUDE.md line 107), not an env var or .env value, so the "every way it can be set" question does not apply: there is exactly one literal per banner. The remainder of KS-1413 is still open and the author's NOT-in-diff list is correct but not complete (G116-F2). Tier 2 stands (G116-F5).

Not measured on Node 24 (no Node involved; bash only). Run on macOS bash/zsh host.

## 1. Heads + diffstat (logs/head_start.log, final.log)
- PR head `7e0918b74977bfdb6e22427b798215f9804a3115` at START and END: identical. Merge-base `8f313815f415`. 1 commit. Three-dot numstat: 6 files, **+96/-6** as claimed (new suite 49/0, banner test 5/4, start-local 2/1, start-secuura 2/1, flow fragment 18/0, cheat fragment 20/0). Nothing outside the declared paths.
- **Develop moved again**: the brief said `bc8558db6b66`; at START and END it is `66a36e3f777d`. 0 of the PR's 6 paths are touched by develop since the base (overlap grep rc 1).
- PR body not read (no Secuura gh auth here); the author's READY mail copied into evidence/.

## 2. The hunks
- start-secuura.sh :711 `echo -e "    Issuer:  demo@secuura.io / demo123"` becomes a comment line plus `echo -e "    Issuer:  demo@secuura.io (password: the published demo default - see CLAUDE.md)"`.
- start-local.sh :284 `echo "    Issuer:  demo@secuura.io  / demo123"` becomes a comment plus `echo "    Issuer:  demo@secuura.io  (password: the published demo default - see CLAUDE.md)"`.
- Test side: banner suite cell 3 loosened from the full `demo@secuura.io / demo123` string to `demo@secuura.io`; new suite with 4 cells (planted-matcher control, both banners still name the account, one value cell per script).
- CLAUDE.md line 107 does carry the demo login, so the pointer resolves (checked in the clone).

## 3. (a) What the head still prints (logs/inspect.log, inspect2.log, final.log)
- Banner lines touched: no secret value at head. There is no env var, default expansion, .env read or empty case in these lines; the old text was a single string literal, now a constant sentence. So all four "ways" print the same constant.
- Still printed by the two scripts (KS-1413 remainder): start-local.sh :280 `Grafana ... (admin/secuura_grafana)` and :285 `Admin: admin@secuura.com / admin123` (both on the author's list).
- Still present but NOT printed: start-secuura.sh :603 and :614 curl login literals `demo123` and `admin123` (author lists :603 only; :614, the admin literal, is a sibling and is not named in the author's mail). curl output goes to a variable, stderr to /dev/null, no `set -x` in either script; the literals are visible only in `ps` for the life of the call. Redis password: `-a "$REDIS_PW"` into docker exec, never echoed.
- No `set -x` / xtrace in either script (positive control: 51 and 83 echo lines counted in the same files).
- Elsewhere in the repo (not these scripts): `Blockchain/Dev/systemTest/cross-tenant-isolation/repro.sh:143` prints `admin@secuura.com / admin123` on a failure path; `deploy.sh:872`, `smoke-test.sh:157,171`, `auth-matrix-smoke.sh:38` hold the literal without printing it; `check-no-default-passwords.sh` is the gate the "KS 951 extension" refers to.

## 4. (b) Byte identity to held O76-P1 (logs/identity2.log; run dir out.md.checker section_1..4.diff only)
Applied the four section diffs with `patch -p1` to a `git archive` of base `8f313815f415` (scratch outside git): all four dry-runs rc 0, then **4 of 4 files EQUAL by sha256 to the PR head blobs**: start-secuura.sh `1641b8db...`, start-local.sh `db5f4fb9...`, banner test `4474f528...`, new suite `2778796a...`. No hand edit. (My first attempt used `git apply` from a scratch dir inside the WEDNESDAY repo and silently left start-secuura.sh unpatched; discarded, redone with patch(1). The reapply control was not clean with patch --dry-run, so the "second apply is refused" control is NOT demonstrated; the sha256 equality is the evidence.) Fragments are the author's own, read not compared.

## 5. (c) Behaviour otherwise unchanged
`git diff -U0` of the two scripts shows exactly the two hunks above and no other line. Both scripts `bash -n` clean at head. Nothing was started (no docker, no stack); the change is inside a final display block (`show_urls` / the closing Credentials block), after all start logic.

## 6. (e) Re-measure
- **Red-first**: new suite at base scripts: 2 failed, 2 passed, both failures the value cells `want "0", got "1"` (assertion). Head: 4 of 4, rc 0. Matches the author.
- **Siblings**: all 10 suites that name either script (bootstrap_env_slot_ports 51, check_slot_credentials 32, ks1355 36, stack_env 25, stack_guard 27, start_secuura_banner 4, expected_services 5, marker_unknown_warning 5, slot_names 23, plus the new one): identical results base vs head, 0 failed (logs/suites_base.log vs suites_head.log; only diff is the new suite missing at base). That is the author's nine plus the new one.
- **merge-tree** onto develop `66a36e3f777d`: rc 0, clean; result changes exactly the PR's 6 paths (SAME_PATHS).

## 7. Mutants (scripts/mutants.sh, logs/mutants.log; separate worktree copy of head, product only, tests untouched, sha256 restored each time: RESTORE_OK x7)
| mutant | result |
|---|---|
| M1 start-secuura value restored | killed by its own cell only |
| M2 start-local value restored | killed by its own cell only |
| M3 value printed by `printf` instead of echo | value cell SURVIVES (the matcher only sees `echo`); only the account-named control fired because my mutant also dropped the echo |
| M4 second `echo` with the value on the same line | killed |
| M5 value assembled by expansion (`${P}123`) | value cell SURVIVES (matcher looks for literal `demo123`); control fired only because the line shape changed |
| M6 Issuer line deleted | killed by control (and banner suite) |
| M7 admin123 line altered | survives: out of the suite's scope by design |
So the two hunks are each pinned by their own cell (the author's claim holds), but the matcher is narrow (G116-F3).

## 8. Kam's ks1346 logging rule
Not a thrown-object log. The diff adds no value to any output; it removes one.

## 9. FINDINGS
- **G116-F1 (INFO, measured).** Develop at gate time is `66a36e3f777d`, not `bc8558db6b66`; still 0 overlap, merge-tree clean.
- **G116-F2 (RECOMMENDED, note for the PR body).** The author's NOT-in-diff list is correct but incomplete. Add: start-secuura.sh :614 admin curl literal `admin123` (sibling of :603); `cross-tenant-isolation/repro.sh:143` echoes `admin123` on failure; literals in deploy.sh, smoke-test.sh, auth-matrix-smoke.sh (not printed). Also state plainly that after this PR a banner still prints `admin123` and `secuura_grafana` in start-local.sh, so KS-1413 must stay open.
- **G116-F3 (INFO/RECOMMENDED follow-up, measured).** The new suite's matcher is `^\s*echo[^|]*demo123`: a re-introduction through `printf`, a multi-line echo, a variable, or a different value is not caught (M3, M5 survive the value cell). It also names only demo123, not admin123/secuura_grafana. Cheap hardening for the KS 951 extension; not a blocker for a two-line banner fix.
- **G116-F4 (INFO).** The new banner text depends on CLAUDE.md still publishing the demo login (line 107 today). If that line is removed or the file is absent from a copied tree, a developer has no on-screen way to log in. Wording is fine for the repo.
- **G116-F5 (INFO, tier).** TIER 2 stands. The value is a published, seeded demo default already written in CLAUDE.md and in several scripts, nothing deployment-specific; no behaviour, config or persisted state changes; the change only removes characters from a closing banner. Not raised to tier 1. Caveat: this is a disclosure-in-terminal class change, but there is no real secret to disclose in these two lines.
- **G116-F6 (INFO).** CONTROL cell 3 of start_secuura_banner.test.sh was weakened from the full credential string to the account name; intended and pinned by the new suite.
- **No FIX-BEFORE-MERGE item.**

## 10. NOT TESTED
- The live PR body, Linear, CI, the author's pre-push hook (13 of 16 legs, 3 skipped), Node 24.
- Actually running either script (no stack, no docker); the banner text is read with grep/diff, never printed by a run.
- The other 79 shell suites in the directory (the hook ran them per the author; I ran only the 10 that name the scripts).
- The docs-fragment check on the two fragments (read as part of numstat only, not linted) and the fragment bytes against the author's.
- Other repos/docs/README or tooling that parse the old banner text `/ demo123`; GNU/Linux bash behaviour.
- Whether CLAUDE.md pointer matters to devs without CLAUDE.md in their checkout.
