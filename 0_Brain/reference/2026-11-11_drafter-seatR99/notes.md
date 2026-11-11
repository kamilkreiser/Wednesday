# Drafter notes, Seat R 99th brief (2026-11-11 ~23:5x AEDT)

## Departures from R 98th's brief, and why
1. Stamp item 1 is now the first round rows 18, 20, 21 + 22, 36 (four tier-2 PRs, "up to four per READY"); item 2 holds rows 37, 38, 40 and the tier-1 block behind Wednesday's ANSWER to that READY. R 98th's rule "later pushes wait for the ANSWER" is carried; the split into two rounds is the drafter's choice from the HANDOVER's order. Wednesday may re-split.
2. The R 98th stale-lock item is dropped (spent; lock absent, queue empty at the drafter's read).
3. Rows 41 and 42 and 17 are removed: all gone to the merge lane (Wednesday's facts).
4. Added two warnings the commission did not name: origin already holds `feature/ks-2055-...-history-entry-as` and `feature/ks-2141-...-legitimate` branches (a prior seat's), so rows 36 and 37 need different branch names and a PR-state read.
5. Rows 23 + 26, 24, 25, 27, 28, 29 + 31, 35 are named "not yours until the tier-1 block is done or an ADDENDUM", because the HANDOVER's queue omits them. This is the drafter's reading of the HANDOVER; it is not a Wednesday ruling.
6. RULED BY KAM quotes two cards printed by `decision_queue.sh show` (ks2055, go-counts) in the card's own words; R 98th's brief only named them.
7. PACE 60 percent, model claude-sonnet-5-5 and push protocol carried unchanged.
8. No SELF-CHECK stamp (Wednesday stamps). The STAMP BLOCK text says it is the drafter's carry of R 98th's stamp and that Wednesday re-stamps.

## Could not measure
- Strict apply of any held patch at `bff81a0d768d`, open-PR overlap, suites, tsc, hooks: no GitHub call, no build.
- The develop sha is not an object in the shared checkout (`log` said bad object); read from `ls-remote` only.
- R 96th's brief past line 119 (provenance only), `REC98/mail/` and R 98th's wrap mail, history.md, gauge, live panes.
- Test runners of analytics, vc-issuer, demo-service (relevant to R 98th's TOOL TRAP 1).
- Whether the two origin branches in departure 4 have open PRs.
- Whether the vault's 1529177 is the `ahead 1` commit (the count agrees, the sha was not read), and whose the two modified daily notes are.

## Method notes
- Linear read via R 98th's `linear_rows_r98.py 72` plus one inline read-only assignee query (key read in-process, never printed). `kam_rulings_today.sh` not run. One refused call (a `cd` in my first bash line) was reissued without it; no files other than these two were written.
- Brief length is about 130 lines (long lines).
