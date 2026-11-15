# Notes: board screen 2026-11-15

## Instruments used
- `board_count.sh linear` for Todo (37). It refused Backlog and In Progress (more than 250 rows; its linear path pages only once and caps first at 250; BOARD_COUNT_PAGE=1000 is rejected by Linear). The Backlog 480 and In Progress 252 figures come from my own paginated GraphQL read (`scratch/fetch.py`, 100 per page until hasNextPage=false, 778 rows total across 5 states) and are labelled as such.
- Linear GraphQL (key sourced inside python from the Blockchain .env, header without Bearer, never printed): description, assignee, labels, comments first:50 sorted newest first client-side, per ticket.
- `gh pr list --state open --limit 500 --json number,title,headRefName,files,body` with the Blockchain GH_CONFIG_DIR: 85 PRs. Ticket-to-PR mapping from KS-nnn in title, branch or body.
- GitHub contents API and git tree API at `48883ba5976b` (tree 6783 entries, not truncated) for path existence and line greps (`scratch/g.sh`). GitHub code search (default branch only) for callers of createBruteForceProtection.
- Python prefix test for lane disjointness and for lane-vs-open-PR file overlap.
- model-routing.md v1.0 for rows; the retirement lesson (Spark gone) for the Spark column.
- Scratch in this folder: `scratch/` (fetch.py, g.sh, ks.json, prs.json, prs_body.json, tree.json).

## Slip to record
One Bash call contained a stray `cd` (it was refused by the hook, nothing ran). No other violation.

## UNMEASURED
- The local clone is stale (0e6479d7b, 2026-11-10) and does not hold the target sha; I did not fetch (would write into a !CODING checkout). All "at develop 48883ba5976b" facts come from the API for the specific files named, not a whole-repo grep.
- I did NOT read all 732 Backlog and In Progress tickets. Todo (37) was screened by title with descriptions and newest comments read for about 25. Backlog/In Progress was screened by service keywords (billing, staking, governance, kyc, vc-issuer, systemTest, Akto and similar) plus a "ruled / build seat" comment grep. Other areas (anchoring, frontend, docs, tokenisation, timestamping, nft, analytics, referral, wallet-connector) are unscreened or excluded by ownership.
- Ticket text of Backlog items KS-1910, 1900, 1899, 1993, 1994, 2188, 2189, 2185, 1914, 2003, 2044, 1749 was read for BLUFs only, not full bodies; whether each is still live at the ref was grepped only for 1934, 1935, 1897, 1372, 2036, 2030, 1914, 2003, 1684 (partially), 2189 (partially), 1749 (partially). Others: not re-read in code.
- Whether the "doc line" KS-1372 names exists and where (path not found); whether KS-1897 needs gateway changes; whether KS-1694's fix touches only package files.
- Whether PR 2089 (Seat B queue) is merged or closed, and whether ticket mentions in PRs exist only in comments (a PR body that does not name the KS key would hide an overlap; file-level overlap check covers the lanes' globs regardless).
- Weekly usage gauge (P2/P3): not run. Sizes S/M are my estimate from ticket text, not measured effort. Whether the Opus gate and Sonnet seat cost fit today's quota: unknown.
- Peter/Stuart-assigned tickets (8 + 7) and tickets assigned to nobody (127): not individually read.
- Whether production data or UAT is involved in KS-2189/2188 tests (needs real Postgres?): unmeasured.
