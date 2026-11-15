# Notes: In Progress screen 2026-11-15

## Instruments
- Linear GraphQL, team KS, state name "In Progress", first:50 paginated: **6 pages, 253 issues, hasNextPage false on page 6**. Comments first:50 per issue, sorted client-side by createdAt. (253 > 250: board_count.sh would refuse; not used.) Key read in-process, never printed.
- GitHub GraphQL via `gh api graphql --paginate`, repo Secuura/Distributed_Secuura, all PRs ordered by updatedAt: **22 pages, 2146 PRs, hasNextPage false**; filtered client-side to updatedAt >= 2026-09-01 = 1480 PRs. (A first try with `gh pr list --limit 1000` hit its cap and was discarded.)
- Ticket-to-PR link = KS-n in PR title, branch, or first 300 chars of body; plus Linear PR attachments; plus open PRs cited as "PR nnnn" in the ticket's newest comment (marked commentCited in the json). Full-body mentions were NOT used for linking (they pulled in dozens of incidental PRs, e.g. KS-1868).
- Gates: 607 verdict.md files under 0_Brain/reference/*gate*/. Match = the PR's 12-hex head appears (case-insensitive) in the file. **Positive control:** 546 merged PRs' heads matched a verdict file, so the matcher works. 71 of 72 open PRs matched; the one miss is PR 2142 head 3ea830e7e221 (KS-2142), reported P-UNGATED.
- Done rule card read: choice a, ruled 2026-10-13.

## Rows that rest on ticket text only
- **Every L row.** Bucket L = all linked PRs merged and the newest comment contains none of my partial-scope phrases (not done, first of, left open, part N, item N of, piece N, remaining, partial, NO GO, reopen, covers ... only). Regex on one comment is a heuristic: a ticket whose scope is incomplete but phrased differently will be in L wrongly, and many tickets I put in B may in fact be complete. 105 L rows deserve a spot-check by the board seat before archiving. Merge was read from GitHub; scope completeness was NOT read against the code.
- Deploy status for the Done rule: only inferred from the newest comment mentioning kintsugi and deployed. No Kintsugi REVISION was read.
- H and D rows come from reading the newest comment (about a dozen tickets read in part); other B rows were not read beyond title, description opening and newest comment keywords.
- P rows: "gated" means a verdict file names the head, NOT that the verdict is GO. Line 1 of each verdict is printed for the reader.
- Lane paths come from regex over title plus first 2500 chars of description. Several tickets gave no path (KS-1468, KS-1175, KS-1036, KS-1033, KS-937, KS-851, KS-920, KS-593, KS-1316, KS-2085, KS-1904) and were placed by theme. Tickets can touch files outside their lane; disjointness is of the globs, not proven against each ticket's real diff.
- Assignees: 233 Kam's account (the board account), 19 none, 1 Stuart (see json). No Peter.

## UNMEASURED
- **Path measurement at develop 48883ba5976b was NOT done:** that commit is not in the local clone of the Blockchain repo (cat-file: not a valid object; local origin/develop is 0e6479d7b6c0, stale) and I did not fetch (read-only commission). No ticket path was verified to exist at any develop.
- No duplicate was proven at source (D = 1 on ticket text only). No Actions-retired premise check beyond a keyword grep.
- Live-lane overlap: tickets in B lanes may touch files of B 176th's queue PRs (2089 2220 2221 2222 2098 2079 2223 2224 2081); I only moved KS-1176 to X after seeing PR 2224's body name it.
- Verdict content (GO / NO GO) of gated PRs not classified.
- 15 tickets have an open PR AND an unmerged-state ambiguity (PR 714/717 for KS-657 older than the 09-01 window show state ?).
