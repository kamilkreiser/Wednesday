STARTABLE
# B981 drafter report (SEAT-G238, HPSM-POC PR #263, tier 2 round 1 of 2, class "test-only pins (four tickets)")
BLUF: kit is startable once stamped. Nothing was run, built or sent; all facts read-only at Sat 31 Oct 2026 13:15 AEDT.

## Measured
- PR #263 open, not draft, mergeable true / blocked; head 53edc92bc59724b8a8981e5de4d539aec0b7786e; base and main both 8ce485275455e07eaa39c46a50e62e7f7f2b3c83; 4 commits; 5 files +120 -11 (matches the builder per file); open PRs: #263 only.
- Checks at head: gitleaks and dependency review success; Analyze x4, api, 2 x SQL Server, infra, web build, web unit tests in progress; no CodeQL row yet.
- Squash settings COMMIT_OR_PR_TITLE / COMMIT_MESSAGES (four commits: kit tells Tuesday to use explicit text files).
- Round count: 120 files with a first line `GATE VERDICT`, 0 naming #263, the four tickets or b978 (round 1).
- Panes: tuesday, HPSM-POC-H81, HPSM-POC-H80, MPS-M52, fleet-monitor; no G238. lsof 9520-9529: 0 listeners. Kits of 30-31 Oct: 952x appears only inside a UUID (B972) and a number (B926): block is free. Builder uses 9510-9519.
- Load1 2.64 (uptime 13:14). Sonnet id claude-sonnet-5-5 (models_latest.json line 23). Routing rows G1/G2/G-cap at model-routing.md lines 108/109/111.
- Kit: 25 lines (long), 0 non-ASCII by program, 8 lines with the four-underscore pattern (S1-S7 plus the bare last line), 0 @X@ slots.
- Builder STATUS and commission read whole; B966/B967/B964 plant tables are referenced by file and approximate line, not re-read by the drafter.

## Q-questions (defaults)
- Q-1 port block 9520-9529: default yes.
- Q-2 landing tree: main is still 8ce48527, so comb tree = head tree; gate re-reads main at Step 0. Default yes.
- Q-3 PackView mock-bypass grading: default Blocker if a lead-changing plant leaves the row green; kit says so.
- Q-4 tier 2 stands (tests only, plants already measured by earlier gates): default yes; any product byte escalates to tier 1.
- Q-5 e2e plants (B966 p6, B967 p1) need a product rebuild and Playwright pointed into 9520-9529; the drafter did not read playwright.config.ts. Default: gate reads it and STOPs if it cannot be pointed there.
- Q-6 PR title and body: title names four keys (fine); body says "builder's local runs" (kit lists as a Minor text fix). Default: Tuesday corrects at landing.
- Q-7 target/hard stop: 90/150 minutes (two npm ci, two suites, 11 plants with rebuilds).

## Stamp values to fill
S1 STAMPED <time> AEDT 2026-10-31 by <seat>; S2 window + load1 (2.64 at 13:14) + live seats H80, H81, M52; S3 Q-1..Q-4 answers; S4 launch authority incl. fetch of two refspecs, npm ci, scratch plants, ports 9520-9529, gitleaks; S5 absolute clocks (target +90, hard stop +150); S6 ls-remote of branch/main/refs/pull/263/merge, check table, open PRs, panes; S7 `model: claude-sonnet-5-5 -- G2 -- gauge <n>%` from usage_tuesday.json and load1; last line `READ-WHOLE-BY-TUESDAY: DONE <time> ...`.
