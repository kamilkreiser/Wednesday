# B827 drafter report (Sonnet 5.5, 2026-10-27 13:46 to 13:56 AEDT, clock from `date`)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B827_SEAT-G174_nexusai-129-probe-race-gate-tier1.md` (102 lines, 8 four-underscore lines: 7 slots + the last line; `.pre-stamp` copy beside it, `cmp` equal, count 8; 0 at-tokens, 0 non-ASCII bytes). Seat `Datasec/NexusAI-G174`, ports 9510-9519, Opus, tier 1 (row G1), round 1 of 2, STATUS path as ordered.

## What I read
- Whole: builder kit B816 (153 lines), ADDENDUM-1, builder STATUS B816 (229 lines), the shape kit B815 (90 lines); B817 read in part (headings, REFUSE, Stamp, Launch line, slot lines, VERDICT lines) rather than whole.
- At source via `gh api -X GET` raw contents at head `92dd28fc`: `backend/jsonStorage.js` (saved to my scratchpad; lines 392-430 helper, 845-885, 950-975, 1272-1300, grep for crypto/probeWritable/FALLBACK/dataDirFallbackActive), `__tests__/rd891-probe-name-race.test.js` (whole, 408 lines), `scripts/verify-expected-counts.json` at head and at main, the compare patch of `jsonStorage.js`, `package.json` (grep), the PR #129 object (title, body, mergeable_state), PR commits, merge-ref commit (parents, tree), head commit tree, check-runs on the head (twice), code-scanning analyses and alerts (PR ref open and all states, main alert #111), ruleset 24139430 name/enforcement, `actions/variables/CI_DEPLOY_ENABLED` (404, nothing learned).
- Project text: NexusAI `CLAUDE.md` (grep of landing/QA-flow sections), `CLARIFICATIONS.md` C-190 (lines 2062-2078), C-68 (line 665), C-209/C-224/C-225 (first lines only), `session-tools/nexusai-lock.sh` header (lines 1-40), `model-routing.md` lines 108 and 111, `models_latest.json` opus id.
- Measurements: `ls-remote` x3 (13:46, 13:47, 13:50), `shasum -a 256` of the lock tool and the four `session-tools/b807` files (match the builder kit's prefixes), `lsof` 9510-9519 (rc 1), `tmux list-panes` (NexusAI-M21 live at 13:49; no G174), `ls` for absent `b827` trees, a loop over the 64 NexusAI STATUS first lines (20 `GATE VERDICT`; 6 loose hits, other classes).
- The shared checkout is stale: `git cat-file -t` of BOTH `92dd28fc` and `97fac53a` failed there. The kit therefore makes the gate clone and fetch (explicit refspecs, in its own clone), as the builder did.

## Design decisions (mine; Tuesday may override)
- D1 Class stated with limbs (a)-(g); P1-P8 restated (P7 tolerance only on own probe, P8 helper defect reads as "unusable" which covers the `crypto` focus).
- D2 Your eight focus items map to: (1) C5(8)+C7+C3's E rows, (2) C13, (3) C3, (4) C4, (5) C5, (6) C6, (7) C8(b), (8) C10. Extras I added: C9 the real two-process race at base and head (the strongest evidence, about 25 minutes), C11 shared-directory fence, C12 messages, C14 claims and PRIOR WORK.
- D3 Two commits is explicitly NOT a finding (ADDENDUM-1), and the landing is a head-pinned merge commit.
- D4 Mutant grading: a stated-property mutant green under all 8 cells is Minor with ticket text (the cell to add named), Major only if a title/body/message/cell title claims it is pinned. This is my judgement call (Q-3).
- D5 Gate writes its own fence-quiet, runner and resolver child; copies only the four hash-pinned b807 files; builder's `session-tools/b816` is read-forbidden as instrument (logs readable as claims).
- D6 Hard stop suggestion 150 / 240 minutes after Step 0.

## Questions for Tuesday
- Q-1 The builder pane `Datasec/NexusAI-M21` was still listed at 13:49. The kit makes the gate wait 10 minutes then proceed (Note). Close it first, or accept?
- Q-2 The hosted `build` check on the head was in_progress at 13:47 and 13:50. Launch now (the gate waits up to 40 minutes beyond its last heavy job), or hold the launch until `build` completes? It is the only node-24/Linux evidence.
- Q-3 Accept the Minor-with-ticket grading for survivors of MU1-MU8 (D4), or should an unpinned "every other code is thrown" half already be a Major because the PR body says "Any other create, write or remove failure is thrown unchanged"? I graded Major only if the claim is read as "pinned by a cell"; the body states behaviour, not a pin.
- Q-4 Round count 0 of 2: rests on my loose scan of first lines (6 other-class hits, not read) and the builder kit's statement. Confirm.
- Q-5 Is C9 (race instrument, 10 sets) wanted in full, or only the constructor sim at base and head (cut the resolver arm to save about 8 minutes)?
- Q-6 Port block 9510-9519: I confirmed no listener; I did NOT scan the SEAT kits for the string (relied on your scan).
- Q-7 The exact `gh pr merge` merge-commit form is left to you (the kit says so).

## UNMEASURED by the drafter
No clone, fetch, install, jest, verify, race, mutant, harness run, `psql`, or node execution of the helper. Not measured: that cells A, B, C, F are red at the base and D, E green (taken from the builder's STATUS; I only read the cell code and reasoned that A and B depend on the rival spy); that the head's 8 cells are green; the verify pair; fence behaviour inside jest; CodeQL on the final `build`; whether a stub `openSync` (MT2) or vanished parent (MT3) is reachable on a real filesystem; load1 (not read). The residues named in C5(5) (unlink fails non-ENOENT after create leaves the probe file) and C6 MT2/MT3 are my source reading of the helper, not runs.

## Facts the kit relies on that I did NOT read at source
- `scripts/verify-suite.sh:85-96` and `build.yml:83-84` (the either-direction CI predicate) and `node-version: '24'`: relayed from the builder kit; the kit tells the gate to read them itself.
- Builder race figures (38/35/37 of 40; measure lane 20/22), 55-file neighbour set, 921 tests, MS1-MS3 results, 15 lister sites, FINDINGS 1-7: relayed from the builder STATUS.
- The stock fence's `FENCE_SUMMARY` stdout line breaking two neighbour files: builder STATUS.
- `DEFAULT_DATA_DIR` comes from `./dataDir` (import line read; `backend/dataDir.js` itself not read); `services/authEnforcement.js` reads the flag (builder STATUS, `git grep -c` list).
- The test names in REFUSE 2's moved-path list (`rd407-*`, `data-dir-selection-bookkeeping`, `rd441-*`) come from the builder STATUS and kit, not a tree listing.
- Instrument usage line for `race-b807.js` and the `B807_SHADOW`-style variable: from the builder kit; I read none of the four b807 files, only their hashes.
- `ruleset 24139430` second threshold `alerts_threshold = errors`: from CLARIFICATIONS C-190 addendum (read), not from the ruleset API (I read only name/enforcement).
- Alert #111 location (line 1252, high, open) read by GET; the builder's claim that the new `openSync` line may draw a new alert is its reasoning, not a measurement.
- Jira RD-891 comment 40204 and B807 STATUS were not read by me; the kit cites them from the builder kit.
- PR title/body quoted from `pulls/129` at 13:47; they may have changed since.
- Stamp dependency: the model receipt and gauge line is the B815 form, copied.
