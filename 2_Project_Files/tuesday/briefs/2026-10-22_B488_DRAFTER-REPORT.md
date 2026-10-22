# B488 drafter report (2026-10-22 about 23:5x AEDT, read-only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B488_SEAT-G47_hpsmpoc-b466-b467-delta-regate-round2.md` (52415 bytes) plus the `.pre-stamp` (`cmp` identical, both sha256 `0e3c9602ff1a…bd198`; made with `cp` from my one Write, NOT a second Write: byte-identity was the goal and a 50 KB re-emit risked a typo). Cockpit `Datasec/HPSM-POC-G47`, Opus `claude-opus-5-5` (row G1), session tier 1, ports 8360-8369. Cloned from the B487 shape; Api-suite rule from the B482 brief and the B478 kit.

## Check list in the kit (7 checks, run per subject)
- **Subject A (b466, tier 1):** (1) delta 6 paths / 2 commits / +246 -8, every minus line, words guard by program (no new literal, counts equal, protected list rc 0, 2 production callers of `Shape.Customer`). (2) B478-1 by the gate's OWN DbContext-planted probe: same name + new facts 200, different hidden 400, clean repair 200 then old hidden 400, clean stored name + hidden 400, create 400; all 212 scalars x 3 positions (held->200, different->400, create->400); exactness probes (case, normalisation, +/- space, edge-space silent trim), length rule untouched (121 chars), industry/ETag/blank ordering; race read at `CustomerEndpoints.cs:191-194`; README clause word-diffed (exactly one clause) and each claim judged; mock parity oracle (scalars, route level, `b.name === held` vs Ordinal); B478-3 note-surface rows + N1; B478-2/4/5/6/7 untouched. (4) mutants H1-H4, M-mock1/2, N1, round-1 M4 M5 M12 M13 (+M6-M8, M14, M15; M1-M3, M9-M11 only if cheap), new A1-A7 (IgnoreCase, trim-before-compare, skip length, trimmed stored, create allowance, mock trim, mock falsy held). (5) Feedback, Api (queued) in a main+A merge tree, web whole, typecheck, lint, repeats. (6) optional real-screen held-name save (NOT TESTED allowed).
- **Subject B (b467, tier 2, test-only):** (1) 2 paths / 2 commits / +109 -0, `git diff api/src web infra .github` 0 bytes, goldens equal. (3) V5 by Row_d/Row_e (caps 5 and 4 read at source), V3 by Row_f (accepted set k 0..60), V6 by Row_g with **who-was-right** on `{0,1,2,26}` vs `{0,2,26}` (rebuild both inputs, read the B477 `probe-V6*` evidence), seed pin judged as sentence-not-hash (what it does not pin; red at the fork; red under M481-S; extra seed mutants; V9 likely not caught by it, Reporting rows carry it), V0/V2 still die. (4) mutant table. (5) Reporting, Api (queued) in a main+B merge tree, repeats.
- **Both:** (7) legacy merge-tree per subject and A-vs-B, `-merge` status = exactly the subject's paths, overlap per live lane plus A/B cross-pair, behind-commits named, gitleaks over delta and whole-branch ranges, merge order recorded (A and B disjoint: either order), per-subject verdict line and a last line carrying four ticket verdicts (204 has 0 delta bytes).

## Measured by me (read verbs)
- `ls-remote`: main `48521806`, b466 `07cd57d2` (READY), b467 `6325a332` (READY), b465 `6182defd`, b461 `53052201`; no `b488*`. All 8 full shas in the kit resolve (`cat-file -t` = commit).
- A: `rev-list --left-right` `0 2`; numstat 6 paths +246 -8 (CustomerEndpoints 1/1, Requests 7/2, README 1/1, Hpsmpoc178 159/0, customer-detail.ts 6/4, customer-name.test.ts 72/0); product diff read in full (ordinal `string.Equals`, update passes `heldName: customer.Name`, create call line 73 unchanged, mock `b.name === held`, put route passes `c.name`); README row diff read (one clause added); `heldName` counts 1 and 5; `Shape.Customer(` callers 2 + 1 test.
- B: `0 2`; numstat 36/0 and 73/0; `git diff api/src` between the heads reports no stat line (0 bytes). Rows read in full (Row_d/e/f/g, the seed row).
- Both: `main...head` `3 4`; merge base `4695d7f2`; legacy merge-tree 0 markers each; main-only paths 8, 0 among either subject's.

## Port block check
8360-8369: `lsof -nP -iTCP:8300-8399 -sTCP:LISTEN` empty (rc 1). Port tokens 83xx/84xx in `tuesday/briefs/2026-10-22_B4*.md` are 8300-8359 only (8360-8399 appear in no brief; control `834[0-9]` hits B469, B483-485 report, B487 files). `.tools/b488` absent. No server is required by any check; the block is reserved for an optional mock probe.

## Hygiene
Four-underscore slots 6 (five stamp slots + last line; control: the instrument counts lines). `@[A-Z_]+@` 0. Person-name grep 0. 8 lines hold non-ASCII (middle dots, same as earlier kits).

## Assumptions and marks
1. ASSUMED: main's #185 may have removed the time-seeded `UatOpenAssertionTests` name drift; the kit says measure, mask only if still present.
2. ASSUMED: HPSMPOC-204's verdict follows Subject B (delta 0 bytes for it); the kit says so on the last line. Say if you want 204 carried separately.
3. Beyond your list I added: A1-A7 mutants, the 212-scalar held-name probe (all three positions), the race read, the edge-space silent-trim Note, the A-vs-B cross-pair merge-tree, optional real-screen Check 6, and whole-branch gitleaks ranges.
4. The round-1 gate's "15 mutants" are re-run only where the code moved (M4 M5 M12 M13 minimum; M1-M3 and M9-M11 live in the untouched Feedback/table code: optional).
5. RELAYED and not re-measured by me: all builder suite figures, the `{0,1,2,26}` vs `{0,2,26}` sets (the contradiction is handed to the gate), the base text of the seeded summary.
6. Not read: Jira, hosted anything, the B477/B478 evidence files (named for the gate), the API behaviour for a >120-character planted name (kit makes the gate show whether the column allows it).
7. Nothing run: no test, build, probe, HTTP beyond `ls-remote`.
