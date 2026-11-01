STARTABLE: YES (once Tuesday stamps the seven slots and the last line; nothing blocks at source)

# B1036 DRAFTER REPORT - SEAT-G256, HPSM-POC tier-2 (Opus) QA gate of B1034, round 1 of 2 on class "roadmap actions from the reviewed run"

## BLUF
Kit `2026-11-01_B1036_SEAT-G256_hpsmpoc-388-roadmap-two-runs-gate-tier2.md` (70 lines, 8 four-underscore lines = 7 slots + last line, 0 non-ASCII bytes) and its byte-exact `.pre-stamp` (cmp equal, sha256 `6b8730d7f5cf...` both). It gates branch `b1034/hpsmpoc-388-roadmap-two-scored-runs` @ `1353d337` (1 commit on main `1f4bf7bc`, 2 test paths +27 -0). The shape follows B1027 (round-2 tier-1 gate, same component), at tier 2 on Opus. It adds to the builder's five plants (c0, g18b, g18, g18c, h1) five new ones: g18d (second-newest run), g18e (actions merged across runs), g18f (top chosen oldest-first), h2 (a harness map hit returns the default result), g14 (meaning kept). There are two controls: c1 and the equivalent g20. It also adds red-first against a planted product line and against the base harness, and a byte-level differential of harness answers with every map at its default. Pane G256, ports 9290-9299.

## FACTS (instrument + control)
- Pins, 11:05 AEDT, `gh api -X GET`: main `1f4bf7bc4f73c9696523bfd59f95355ab37b76a8`; the branch is `1353d337fdd27ad8ea705c99296410217ca19f70`; `matching-refs/heads/b1036` returns 0 (control `b1034` 1); open PRs 0; PRs for the head 0 (control: closed PRs list 269, 268).
- `compare 1f4bf7bc...1353d337` gives ahead 1, behind 0, 2 files: `SecurityRoadmap.test.tsx` +19 -0 and `testing/harness.ts` +8 -0. The commit has one parent `1f4bf7bc` and tree `3d46254d...`. It is unverified, with a 113-character subject (`wc -c`) and 1 Co-Authored-By line (Sonnet).
- Check-runs on the head: 0 (control: main 19). Code-scanning alerts on the branch: 0.
- `ci.yml` has the same blob at head and main: `0176b491`, 679 lines. Lines 1-3 say "Build + test only. No deploy job". Repo squash settings: COMMIT_OR_PR_TITLE / COMMIT_MESSAGES.
- The shared `2_Project_Files` holds neither `1353d337` nor `1f4bf7bc` (`cat-file -t` fails). It does hold `7f0d832d` (commit). So the gate's clone has to fetch both.
- The 27 added lines (`+` lines of the patch) show 0 hits for each of: non-ASCII (control `\x80` 1), `B###`/key/URL/localdomain (control `+B123` 1), and timers/skip/only. The auth-shaped census `role|session|cookie|auth|token|signIn` also reads 0, but no control was run for it, so the kit has the gate run one.
- Plant anchors were counted at the head by `grep -c -F` over the raw contents. Each one reads 1 in its own file and 0 in the other. The zero control `NOSUCH-zz-b1036` reads 0 in both. In `useSecurityData.ts:77-78`, line 78 holds both the reviewed and the actions anchors.
- Round count over 543 `Briefs/*_STATUS.md`: 131 GATE VERDICT first lines. The filter for this class reads 0; control `part b` reads 3 (B691, B1022, B1027).
- Seat suffix: G256 has 0 kits and 0 STATUS hits (control G255: 11 and 9).
- B-number: B1036 has 0 names, 0 text hits and 0 project briefs (control B1035: 3). `.tools/b1036` is absent (control `.tools/b1034` present).
- Ports 9290-9299 were scanned word-bounded over 150 kits and 133 Datasec `.md` files dated 10-31 and 11-01: 0 and 0 (controls: 928x 2/2, 927x 3/3). Across all dates the block shows 4 old kits. `lsof` shows 0 listeners. No free 10-port block exists in 9000-9999 across ALL dates, so the frame is the recent kits, the same frame B1027 used.
- Panes at 11:1x: tuesday, Datasec/HPSM-POC-R109, Datasec/HPSM-POC-D43, fleet-monitor. load1 was 2.61.
- Landing rule: the analysis repo's CLARIFICATIONS at `dd44bce8` has 5053 lines, and 95 of them match `head-pinned` (an absent string reads 0). Line 5036 is the PR #269 landing ("a head-pinned squash; customer security preview, part B") and line 4860 is part A's. The project-local CLARIFICATIONS line 138 that the B1034 kit cited carries a decision-card id, so it is not cited in the kit.

## D-decisions
- D-1: Tier 2 on Opus, per the builder stamp's GATE-ROUND. An auth-shaped finding or one that discloses something is a STOP to tier 1 (the last column of the G2 row).
- D-2: The new plants are g18d, g18e, g18f and h2, plus g14 for meaning, and c1 and g20 as controls. A plant that branches on the COUNT of runs is NOT RUN by design, because no finite set of rows can pin it. That is said in the kit.
- D-3: Severity. g18b, g18c or h1 surviving is Major. Any new rule plant surviving with a behaviour proof is Major (as B1027-1). g18 with R3 green is Major. Red-first against the base harness coming out green is Major.
- D-4: A `base` worktree at `1f4bf7bc` serves the base suite (3782), the names, the red-first overlay and the differential.
- D-5: The gate makes its own clone and fetches by URL with the per-command key, as B1027 and B1034 did. The inherited `core.sshCommand` is stale.
- D-6: Landing data files are pr-title, pr-body, squash-subject and squash-body. The squash body carries exactly one Opus trailer.

## Q-questions (defaults)
- Q-1: Are the new plants as listed? Default yes.
- Q-2: May the differential scratch file go in `wt-b1036-base`? Default yes.
- Q-3: May the PR title and squash subject carry HPSMPOC-388, as PR #269 did? Default yes.
- Q-4: Include the two audits? Default yes.
- Q-5: Ports 9290-9299 and pane G256? Default yes.
- Q-6: Round statement "0 of 2 before, round 1 of 2"? Default yes.

## UNMEASURED
- Whether any plant prediction holds, especially g18e's side reds and h2.
- Whether `recorded` is reset between tests. R3's exact-list assertion implies it is; the drafter did not read where.
- The new row's runtime.
- The builder's `.tools/b1034/logs/` contents.
- B1033 and B1031 progress (each STATUS tail is a working line).

## Outside the fences
- The builder's evidence folder is empty; its logs are under `.tools/b1034/logs`. This is a Note in the kit.
- The builder committed with `core.hooksPath=/dev/null`, per its own Corrections. This is a Note.
- The B1034 kit's landing citation (`CLARIFICATIONS.md:138`) holds a decision-card id. The kit cites the analysis repo instead.
