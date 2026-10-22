# B487 drafter report (2026-10-22 22:5x AEDT, read-only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B487_SEAT-G46_hpsmpoc-b465-delta-regate-round2.md` (39362 bytes) plus the identical `.pre-stamp` (`cmp` equal; made with `cp` from my Write, not a second Write). Cloned from the B479 shape and the B474 round-1 kit (Standing paragraph and Check 4/6 recipes deferred to it by path). Cockpit `Datasec/HPSM-POC-G46`, Sonnet, row G2, ports 8340-8349.

## Check list in the kit
Check 1 delta and all 56 minus lines (4 commits, 16 of the 19, forbidden prefixes, `followUpFailure` byte-equal, words guard 14 of 14 by the gate's own program, bare-day assertion judged). Check 2 the B474 regression table: B474-1 dates file under unset/UTC/Sydney/LA + whole vitest UTC; B474-2 the 10-cell matrix (+ `process.env.TZ` grep 0); B474-3 W4 and C4 by NEW rows (race row must not click); B474-4 card id 0 over the repo (control 10 at c65a5ab6); B474-5 nine exact Home sites, helpers' other callers unchanged; B474-7 five load rows; -6/-8/-9 deferred and untouched. Check 3 judgments: item-4 `"load"` choice, `reload()` re-read now a read, 412 load sentence partner-addressed, item-2 route (12 callers one argument, none by reference, one-argument output base vs head 0 differences over 40 instants x 5 zones). Check 4 mutants: the 14 round-1 (C3 anchor changed), builder's 7 (L, T, W5, INV, X1, DEF + W4/C4), new L2 L3 L4 Z1-Z4 and per-site E1, each in machine zone and UTC. Check 5 suites (head/base/merge, two zones, names, typecheck, lint, build, shards, 5 repeats). Check 6 browser six specs, old-title and `Home page` builds, per-site teeth, client load 401/412/500 interception if reachable, off-loopback proxy. Check 7 merge-tree, `-merge` status = the 19, overlap per lane, B465-first order, gitleaks over both ranges.

## Measured by me (read verbs)
- ls-remote: main `48521806`, b465 `6182defd` (= READY), b461 `53052201`, b466 `3eded112`, b467 `d6eba5f6`; no `b487*`.
- `rev-list` 4 / 0; numstat 16 files +154 -56 (my sum of per-file deletions = 56); the 19-path set outside-diff 0 (planted control 1); forbidden prefixes 0 bytes (control 7633); skip-family added 0 (control 1); trailers 4; card id 0 files at head, 10 lines at c65a5ab6; `main...head` = 4/10; legacy merge-tree 0 markers; main-only paths 10, 0 among the 19.
- Anchors at the head count 1 (W-title, W4, D, H1, P1, C1, C2 text, `clientFailure(e, "load")`, C4); `{ ...TIME, timeZone }` counts 2.

## Port block check
8340-8349: `lsof` LISTEN empty (rc 1; also empty over 8300-8349); `grep -l -E '834[0-9]|835[0-9]'` over `tuesday/briefs/2026-10-22_B4*.md` = 0 files; control `831[0-9]` = 4 files. `.tools/b487` absent.

## Slot count and hygiene
Four-underscore slots 6 (five stamp slots + last line); control 1. `@[A-Z_]+@` 0. Person-name grep 0. The seven SHAs in the kit each occur and resolve with `cat-file -t` = commit.

## Assumptions and corrections (marked)
1. ASSUMED (arithmetic, unmeasured): merged vitest = main-alone + 25 (head 2081 vs base 2056); the kit tells the gate to measure it.
2. C3's round-1 anchor `clientFailure(e) }` is gone at the head (now `…(e, "load") }`); kit gives the new anchor.
3. The brief said "12 other gate mutants" while the gate table has 14 total (W4, C4 the survivors); the kit says 14 round-1 and the 12 survivors-before are re-run too.
4. I added mutants and probes beyond the request: Z1-Z4 (the test-only zone argument may let day-part mutants live where all instants share a day), L2-L4, per-site E1, a one-argument base-vs-head output diff, a client-load interception on a real screen (marked NOT TESTED-able if the mock cannot be intercepted), gitleaks over the whole branch range too.
5. The bare-day row lost its LA second assertion (builder DESIGN); the kit makes the gate judge it and makes "lost, with no replacement" a Blocker.
6. Not read: Jira; the API source for whether the client GET can answer 412 (kit hands it to the gate). Nothing run: no test, build, browser or HTTP beyond `ls-remote`.
7. The row counts per touched test file (`it(` grep) printed nothing in my run; the kit relies on the builder's "12 added" and the gate's own name multiset.
