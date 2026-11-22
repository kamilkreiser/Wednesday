PR 2275: GO WITH NOTES (at head 4c361b9cffd737156add09b175c959ad99362a43; tier 2)

# Gate 399, tier 2 (Sonnet), PR 2275 (KS-1536 G2), 2026-11-22 ~22:25-22:50 AEDT

Tier 2 holds: no role spelling's answer changes (Q1), so the tier was right. No HIGH, no MEDIUM finding. Findings only; the merge decision is Wednesday's.

## Pins
- At the start and again at the end (git ls-remote through the Secuura gh credential helper, read-only; gh pr view): develop = c8fd1653a5dc9b79c41f752b29afb296910831a4 (PR 2273's squash: confirmed MERGED with that merge commit), refs/pull/2275/head = 4c361b9cffd737156add09b175c959ad99362a43, PR OPEN, not draft, MERGEABLE, updatedAt 11:21:13Z, ONE commit, parent = develop, tree 11892923134e, 4 files +160 -1.
- Merged state = the head: `git merge-tree --write-tree origin/develop pr/2275` rc 0, tree 11892923134e = the head's own tree.

## How I measured
- Own clone `_work/g` (GitHub, `--reference-if-able` gate 398's clone, `--dissociate`; its default-branch checkout printed a harmless "unable to parse commit" and left no working files, which I did not use). Worktrees: `h` head (suites, static, probe), `d` develop (suites, probe), `x` head (mutants). node_modules and packages/shared/dist APFS-cloned from gate 398's `h`; no package.json, lockfile or packages/ file differs between that tree and develop (diff rc 0) or in this PR. Node v26.8.1. TMPDIR = `_work/tmp`. check:openapi alone used the relative TMPDIR (the unix-socket 104-byte limit, same as gate 398; the first try's EINVAL kept in evidence).
- Scripts in `_work/`: `run_cwd_g399.py`, `suites_g399.sh`, `probes/g399-probe-a.test.ts` + `probe_run_g399.py`, `mutants_g399.py`, `guard_count_g399.cjs`, `static_g399.py`, `openapi_g399.py`, `mt_g399.py`, `lin_read_g399.py` (read-only GraphQL; the key is read into memory, never printed). Evidence in `_work/evidence/`.
- End state: d, h, x each 0 porcelain lines; x's gdpr.ts sha256 = h's (2fb0d3c5c3ec3099). Probe copies and planted files moved to `_work/_quarantine` (no rm). No write in any !CODING path, no GitHub or Linear write, no database, no mail, no launch, no cd. I ran one `docker ps` name listing at the end to confirm no g399 container exists (0); I started none.

## Findings

### LOW
**G399-2275-1: the cells cannot tell whether the shared vocabulary is asked. A local look-alike of isPlatformRole passes every cell AND the guard.**
- My mutants L1 (`const isPlatformRole = r => r === 'SYSTEM_ADMIN'`) and L3 (a local upper-case compare), swapped for the import: 0 of 379 cells fail, guard 0 fail. L4 (the platform list put back as a constant `['SYSTEM_ADMIN']`, the shared predicate unused) also survives all 379 cells; only the guard's G2 sees L4 (`gdpr.ts: 7 > 6`).
- This is inherent: the cells are behaviour pins by design (the commission and the PR say so), and on the file's own list `['SYSTEM_ADMIN','ORG_ADMIN']` any predicate that answers the same on those two strings is equivalent. Not a defect in the change. It bears on Q2.

**G399-2275-2: the at-sign is in the commit message AND in one committed file, not the commit message only.**
- The commit message line 10 names the package with its at-sign (as disclosed). The PR title, PR body and the Linear comment 2b4f7762 carry 0 at-signs (counted).
- The flow fragment `Projects Documents/fragments/flow/KS-1536-...html` also contains it once (`imported from <code>@secuura/shared</code>`), and gdpr.ts line 24 carries it as the import statement itself (unavoidable; every originate route that imports the barrel does). The cheat fragment has none.
- The squash message is written afresh at merge, so the commit message is moot; the fragment line is ordinary file content (GitHub does not mention-notify on file content). Only the "commit message only" part of the seat's disclosure is inexact.

**G399-2275-3 (words, trivial): line numbers in the PR body are develop's.** "The KS-228 list at line 172" and "line 186's list replaced" are develop's lines; on the head the list is at 173 and the constant at 187 (one import line added).

### Info
- **Own-measurement ratchet leg**: standalone `test-types-ratchet.sh` rc 1 on api-gateway `ks815` TS2345 x2, and the leg test is 45 of 48, not the PR's "6 services OK; 48 passed". This is the same clone-install gap gates 395, 397 and 398 recorded (NonSharedBuffer typing; the PR touches no api-gateway file). UNMEASURED here, not red against the PR. The originate ratchet itself (check.cjs) is 337 examined, 0 new, with a planted control rc 1.
- **develop is red on 6 packages/shared cells and this PR removes exactly one** (the standing leg, below).

## The commission's questions

- **Q1 THE SET: identical. 0 differences.**
  - Probe a: the REAL gdprRouter, the REAL `hasAnyRole`, the caller taken from a module variable so the role can be any JS value; stand-ins only for authenticate, the service (recorded) and the users lookup (counted). 56 callers x (GET /consent/check + POST /consent/withdraw for a subject that is not the caller) plus a direct predicate comparison per caller = 168 rows per arm. **The 168 rows are byte-identical on develop and on the head** (0 differing rows).
  - The 56 callers: the seat's 21 spellings (SYSTEM_ADMIN, SUPER_ADMIN, super_admin, system_admin, System_Admin, Super_Admin, sUPER_ADMIN, SYSTEM_admin, platform_admin, PLATFORM_ADMIN, ORG_ADMIN, org_admin, ISSUER_ADMIN, ADMIN, OWNER, VERIFIER, empty, the two KS-1591 spoofs, an array role, no user) plus my own:
    - 10 whitespace-padded or control-character variants (leading and trailing space, newline, tab, CRLF, NBSP, zero-width space, NUL, embedded comma);
    - 12 look-alikes (dotless i, long s, capital I with dot, full-width letters, Cyrillic A and S in SYSTEM_ADMIN, Kelvin sign prefix, hyphen, space and no separator);
    - 11 non-strings (number, boolean, null, undefined, object, an object whose toString says SYSTEM_ADMIN, arrays, a String object x2);
    - two token shapes: ORG_ADMIN with `roles:['SYSTEM_ADMIN']`, VERIFIER with `isPlatformAdmin`/`isAdmin`.
  - **Platform (200, the service called once with the subject, 0 users lookups): exactly SYSTEM_ADMIN, SUPER_ADMIN, super_admin, on both arms.** Every other caller: 403 with 0 service calls (ORG_ADMIN-family callers are decided by the lookup path; the probe's lookup answers no organisation, so refused), on both arms. Positive control: the three platform rows are seen.
  - Predicate level: `hasAnyRole(u, ['SYSTEM_ADMIN'])` (develop's list) vs `hasAnyRole(u, ['SYSTEM_ADMIN','ORG_ADMIN'].filter(isPlatformRole))` (the head's): equal for all 56, no throw. The shared `isPlatformRole` alone says true for 8 spellings (the 3 above plus system_admin, System_Admin, Super_Admin, sUPER_ADMIN, SYSTEM_admin): exactly the 5 the direct swap would have admitted, as the plan's table said. None of the whitespace, look-alike or non-string callers is platform by either predicate.
  - Why it is exact, by the code: `.filter(isPlatformRole)` runs over the file's own `GDPR_ADMIN_ROLES` (`['SYSTEM_ADMIN','ORG_ADMIN']`), where `SYSTEM_ADMIN` is in and `ORG_ADMIN` is out, so the value is `['SYSTEM_ADMIN']`; the caller's role never meets `isPlatformRole`, only `hasAnyRole`'s exact compare after its two-spelling fold. `filter` hands `isPlatformRole` a second (index) argument, which it ignores (one parameter).

- **Q2 THE GUARD: green by the guard's own regex, by a real derivation, within a narrower reach than "one shared list".**
  - Counts with the guard's LIST / SPELLING regexes copied verbatim (`guard_count_g399.cjs`; positive control: a planted `['SYSTEM_ADMIN']` counts 1): gdpr.ts on develop 7, on the head 6 (equal to its baseline 6). The seven on develop are GDPR_ADMIN_ROLES, the platform constant, and five `requireRole` literals; the head loses only the platform constant. The baseline JSON: `git diff origin/develop pr/2275` on it rc 0, and no path with "baseline" in the diff (0). The whole shared vitest on the head: G2 green and G1 green.
  - **Which is it?** It asks the shared vocabulary; it is not merely hiding a list from the regex. The platform constant is now computed by the one shared predicate (its quoted list is gone and nothing quoted replaced it); M5 shows a list quietly appended to it is caught, and widening the file's roles feeds through the shared predicate (A2 `system_admin` added to GDPR_ADMIN_ROLES: becomes platform on the head, killed by P2, so the coupling is real).
  - **But the reach is narrower than "one shared list":** the shared predicate classifies only the two roles in this file's own GDPR_ADMIN_ROLES; it never sees the caller. The decision about a caller is still `hasAnyRole`'s exact compare (originate's own notion of case). Consequently: a change to the shared `PLATFORM_ROLES` alone does not change what gdpr.ts treats as platform unless that role is also added to GDPR_ADMIN_ROLES, and a local look-alike or a restored constant list satisfies the cells (G399-2275-1). The five `requireRole` literals and GDPR_ADMIN_ROLES remain baselined, un-reconciled lists, which the guard's own comment says is the standing allowance ("baselined, not reconciled"). The PR names the two-notions-of-case residual honestly. For Kam's card a ("One shared list without platform_admin, after a check") this meets the guard and the wiring; it does not, and the plan said it would not, unify the two letter-case notions.

- **Q3 THE CELLS: 34 pins green on both arms; M1-M7 reproduce; my own survivors named.**
  - The new file is 34 cells (P1 6, P2 22, P3 2, P4 2, P5 2); 34 names only on the head, 0 only on develop, 0 changed status. Green on develop's gdpr.ts and on the head (inside the originate whole run, both arms 0 failures).
  - Mutants, on x (the 14 test files that import routes/gdpr, 379 cells; the no-mutant control 0 failed; restored and sha256-checked each time), with failures in the new file / in the other files / the shared guard:

    | mutant | new file | other files | guard |
    |---|---|---|---|
    | M1 direct isPlatformRole at both sites | 10 | 45 (ks445 15, ks1029 12, ks444 6, ks1346b 5, ks730b 5, ks431 2) | green |
    | M2 filter also admits ORG_ADMIN | 4 | 86 | green |
    | M3 filter admits every admin role | 4 | 86 | green |
    | M4 filter admits none | 6 | 33 | green |
    | M5 platform_admin appended | 2 | 0 | G1 and G2 red |
    | M6 platform line dropped in mayActForSubject | 6 | 56 | green |
    | M7 isPlatformRole direct in mayActForSubject only | 10 | 23 | green |

    M1-M7 reproduce the PR table's new-file kill counts exactly (10, 4, 4, 6, 2, 6, 10). All 7 compiled. M1's 45 other-file failures also reproduce the PR body's "45 existing cells in 6 GDPR suites".
  - My own mutants:
    - **killed:** L2 local look-alike admitting ORG_ADMIN (4 + 86); A2 GDPR_ADMIN_ROLES gains `system_admin` (2); A3 gains `Super_Admin` (2).
    - **survivors, all 0 of 379 failed:** L1 and L3 (equivalent look-alikes), L4 (constant list; the guard's G2 sees it), A1 (gains SUPER_ADMIN: behaviour-equivalent, since the alias fold already admits it), A4 (gains `platform_admin`: only the guard's G1 sees it, the cells do not), A5 (gains ISSUER_ADMIN: not platform, so no platform-answer change; it widens other GDPR_ADMIN_ROLES users, outside these cells' seam).
  - None of the survivors is a behaviour regression of the head; they are the limits of a pin file plus a count guard (G399-2275-1).

- **Q4 WHOLE: clean, and the standing leg holds exactly.**
  - **originate (jest) whole:** develop 3,171 of 3,171 in 242 files; head 3,205 of 3,205 in 243 files. Failing sets both empty; 34 names only on the head (the new file), 0 only on develop, 0 changed status.
  - **packages/shared (vitest) whole, both arms: 1,730 tests each. Develop 1,724 passed, 6 failed; head 1,725 passed, 5 failed.**
    - Develop's six failing names: (1) ks1536-one-role-vocabulary G2 "no file holds more inline platform-role lists than the frozen baseline"; (2) ks1725-zod3-compat F (114 zod3Issues); (3) ks1725 J (z.record, services/prism/src/index.ts); (4) and (5) ks727-errorhandler-class-guard corpus 2 (the inline-site corpus; the pure-forwarder cell); (6) wallet-signature KS-278 "accepts a valid wallet signature over the message".
    - Head's five: develop's six minus (1). Only on the head: 0. Only on develop: exactly G2. Changed status: only G2. **The PR removes exactly the G2 name and adds none.** (Failing files: 4 on develop, 3 on the head.)
  - **tsc originate:** 0 errors (planted: rc 2, 1 error).
  - **eslint --max-warnings 0** on gdpr.ts and the new cell file: rc 0; develop's gdpr.ts rc 0; planted rc 1.
  - **check.cjs originate:** 337 examined, 276 under `__tests__`, 0 errors, 0 new, 0 stale (planted: 1 new, rc 1).
  - **Fragments:** OK (planted: FAIL, 1 finding).
  - **check:openapi:** CHECK PASS (relative TMPDIR, see above).
  - **Standalone ratchet / leg test:** see Info (clone-install gap, unmeasured, same as gates 395, 397, 398).
  - **Overlap:** 20 open PRs (including this one and 2274); no truncated file list (none at 100 files; control: package-lock.json present in 11). 0 of the other 19 touch gdpr.ts, originate middleware/auth.ts, keyRevokePolicy.ts, the guard, or its baseline JSON. The only gdpr-named path elsewhere is PR 2099's gdprService.ts (not this PR's path).
  - **merge-tree:** vs develop rc 0 (tree 11892923134e = the head's tree). The planted control (a local commit, never pushed, rewriting the constant's line) gives rc 1, CONFLICT in gdpr.ts.

- **Q5 THE PR BODY, Test Evidence, the facts comment 2b4f7762: every sentence I checked holds; one disclosure is inexact.**
  - **Hold (reproduced or code-read):**
    - the Summary: PR 2271's squash 302361a30209 (confirmed MERGED, merge commit 302361a30209334a...); PR 2273 is the develop head's squash (confirmed); the 7-vs-6 guard figures; the baseline untouched; the import precedent (`adminConfig.ts:26`, `certifications.ts:57` import `isPlatformRole`);
    - "45 existing cells in 6 GDPR suites went red" under the direct swap (M1: 45 across the same six files);
    - the role-set table: 0 of 21 differ for the PR, 5 differ for the direct swap, and `platform_admin` is out either way (my 56-caller probe agrees on every row);
    - Test Evidence: 34 pins, P1-P5 counts, 7 mutants with the same kill counts, shared 1,724 -> 1,725 with the one-line G2 diff, originate 3,171 -> 3,205, tsc, eslint, ratchet-originate 0/0, fragments, check:openapi, guard 99 of 99 (the shared whole run shows no ks1536 failure on the head), the Node 26.8.1 caveat, the NOT-run list.
  - **The residual is present and accurate:**
    - two letter-case notions in originate: `hasAnyRole` is an exact compare after a two-spelling fold (`['super_admin','SUPER_ADMIN']`), and `isPlatformRole` ASCII-folds (adminConfig.ts:82/117 and certifications.ts:189 use it); ✓;
    - the lower-case `system_admin` sample user at `services/api-gateway/src/routes/admin.ts:499` (Eve Chen, role `system_admin`) ✓;
    - `documents.ts` (353, 1176, 1537) and `certifications.ts` (135, 1073) already treat `system_admin` as an admin by literal compare ✓.
  - **Inexact:** the at-sign disclosure ("the commit message only"): see G399-2275-2 (also one flow-fragment line; the import line is unavoidable).
  - **Trivial:** the line numbers are develop's (G399-2275-3).
  - The comment 2b4f7762 (created 11:21:22Z, by the Secuura account, 2,886 chars, one of 12 comments on KS-1536, state In Progress) matches the PR body and the figures above; it files no ticket, as stated.

## Verdict
GO WITH NOTES. The change is what it says: one constant, derived from the shared predicate, with no change in who is a platform role (168 probe rows identical, 56 callers, look-alikes and non-strings included), G2 green by a real derivation, the standing shared-suite leg moving by exactly the G2 name, the originate suite 3,171 -> 3,205 with no failure, and merge-tree clean. The notes are the limits above: the cells pin behaviour but cannot see whether the shared predicate is asked (the guard's count only sees a restored constant), the derivation covers only the file's own two admin roles, and the at-sign is in one committed fragment line as well as the commit message. Merge is Wednesday's call; the squash message is written afresh then.
