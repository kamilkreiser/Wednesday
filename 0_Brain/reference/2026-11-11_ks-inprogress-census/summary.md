# KS started-type census, 2026-11-11 (read-only)
Source: Linear GraphQL, team KS, state.type = started, paginated (first:50 pages, hasNextPage to end).
Paginated total: 238 (matches board_count.sh 238). census.tsv has 238 data rows + header.

## Counts per class (mechanical, from data only)
- A (>=1 OPEN PR): 73
- B (PRs present, ALL merged/closed; candidate Done): 159 (157 non-D + 2 D)
- C (no PR attached): 4
- D (assigned to Peter or Stuart): 2, both Stuart Jamieson, both also class B (shown "B+D" in tsv). No Peter-assigned tickets in this set.
- Check: A 73 + B 161 (incl. 2 B+D) + C 4 = 238.

## Counts per state
- In Progress: 229
- In Review: 6
- Blocked: 3 (started-type)

## Assignee
- kamil.kreiser@secuura.ai: 216; unassigned: 20; stuart.jamieson@secuura.ai: 2.

## PRs
- 472 GitHub PR URLs found in attachments; all 472 measured via gh api (state + head sha 12). "merged" = merged flag true; otherwise GitHub state open/closed.
- gh auth: authenticated with the Blockchain .gh-config (read-only calls only).

## UNMEASURED / caveats
- PR state UNMEASURED: none (0 of 472).
- Only attachment URLs matching github.com/<owner>/<repo>/pull/<n> count as PRs. PRs referenced only in descriptions or comments are NOT seen, so some C tickets may have PRs elsewhere, and B tickets may have unattached open PRs.
- Attachments fetched first:50 per ticket; any ticket with more than 50 attachments would be truncated (not checked individually).
- Class B is only "all attached PRs merged/closed". Closed-unmerged PRs count the same as merged here; the board seat must verify scope at source.
- Head sha for merged PRs is the PR head at last measure, not the merge commit.
- Peter's identity matched by name regex "peter|stuart" on assignee name; no Peter-named assignee exists in the set.

## Files
- /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_ks-inprogress-census/census.tsv (columns: id, title, state, priority, assignee, updatedAt, parent, children, labels, prs as url|state|sha12 joined by ;, class)
