# B272 DRAFTER REPORT: records seat R4, MPS hosted deploy B268 and Kam's ruling on `mpscalc-hosted-deploy-e6f92a5-1017`
Drafted 2026-10-18, 19:42 to 19:51 AEDT. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B272_SEAT-R4_mps-records-b268.md` (134 lines, 28,059 B, sha256 `5894a099…3496`, `wc -lc` + `shasum -a 256` at 19:50:57) and its `.pre-stamp` twin (`cmp` equal, same sha256). Four-underscore count in both: **7** (`/usr/bin/grep -c '_''___'`), meaning six RULED slots plus the stamp time. The kit's Step 0b control line states 7.

**Number.** B272 was free in both places: `ls | grep -c B272` gave 0 in `tuesday/briefs` and 0 in the MPS `1_Project_Definition/Briefs/`, re-checked in the action that wrote the kit.

**Writes.** I wrote nothing under `!CODING/`. Tools used:
- git read verbs with `--no-optional-locks`;
- `gh api` GETs under the MPS `GH_CONFIG_DIR` (account `kamilDatasec`);
- Jira read-only GETs (`/rest/api/3/search/jql`, `/issue/{key}`) through a scratch client that reads `JIRA_*` by name and never prints them;
- `kam_rulings_today.sh` with `KAM_READ_MARKER` pointed at my scratchpad, so Tuesday's read marker did not move;
- `cockpit.sh status`, a read: 7 rows, none of them MPS.

No fetch, no az, no hosted call, no docker, no mail. **Same-action rule:** every sha, count, line and C-number in the kit was re-measured by one bash action at 19:50:36 / 19:50:57, which wrote the kit only if all of them matched. The first run refused to write. The cause was in my instrument, not the data: `cut -c` cut a byte inside the em dash. I fixed the instrument and the second run wrote the kit.

## Read WHOLE
- Brief B171 and `B171_STATUS.md` (the MPS copy).
- Brief B169 (129 lines).
- `B268_STATUS.md` (253 lines, sha256 `163df43f…7dd9e`).
- Brief B268 (73 lines) and its diff against its `.pre-stamp`.
- B171's drafter report.

## Read in part
- `CLARIFICATIONS.md`: headings, plus `:585-609` (C-42 and B171's section).
- `history.md` `:1-38`.
- `BACKLOG.md`: the last 14 lines and the `[B171-` rows.
- `JIRA.md`: the B169 and B171 sections.
- `B172_STATUS.md`: `:1-25` and the tail.
- W2: headings and `:45-54`.
- The daily note: `:111` and `:122`.
- PR #83's body.
- `kam_rulings_today.sh` `:1-40`, to check its marker write.

## Corrections to the commission
1. **Branch + PR path (R1).** The commission says to push a records branch and have Tuesday open the PR after CodeQL. That cannot apply here:
   - The records repo is the PROJECT ROOT, and `git remote -v` is empty.
   - The code repo holds none of the four records files: its tree at `21c2aec` has 547 paths and 0 matches (control: 2).
   - B169 and B171 both committed CLARIFICATIONS path-limited to root `main`, with no push.

   The kit defaults to B171's mechanics and offers a local `records/b272` branch as the alternative.
2. **Jira and B171's way of working.** B171 used Jira for merge comments. There is **no precedent for deploy comments**: no ticket carries a B166 deploy comment, and `text ~ "12f8e566398b…"` returns only the two #73 merge comments. B169 left a deploy-comment pass to Tuesday, so the 8 deploy comments are slot R2 (default YES).
3. **"Catch-up of brief/STATUS files as B171 did."** B171 committed no Briefs files: everything since B99 is untracked (387 untracked entries under `Briefs/`). B171's catch-up was a `history.md` entry for B170. The equivalent today is **B172**, which built #83 and is not in history: slot R6 (default YES). The kit catches up no Briefs files.
4. **#83's merge comment.** No MPSCALC comment carries `21c2aec…` (0). B172's 39599 is from before the merge. B171's rule gives one merge comment per merged PR: slot R4 (default YES).
5. **C-43 heading.** The store's `title` ("Put 9 more merged calculator changes on the hosted site, and approve their new words?") differs from B268's draft heading. The kit follows the file's format, so the store wins.

## Measured (19:43-19:51)
- **Kam:** `18:58 [live] | Decision mpscalc-hosted-deploy-e6f92a5-1017: a — Deploy main e6f92a5 and approve the NEW words in list W2`, exactly once (rc 0, 5 rows shown).
- **Store:** `ruled a 2026-10-18T18:59:30.049266+11:00`, `delivered_ts` None. That 18:59:30 is Tuesday's write; Kam's taps were 18:57:57-18:58:22 (daily note `:111`).
- **Tuesday's 19:41:13 live check:** daily note `:122`.
- **CLARIFICATIONS:** 609 lines; last heading `585:### C-42`; `C-43` appears 0 times. Next free number = **C-43**. Status clean. Root HEAD `5a03994`.
- **Uncommitted records diff:** +151 / +339 / +53.
- **Main:** `21c2aec…` (#83, merged 2026-10-17T20:06:42Z); #84 404.
- **Newest `DEPLOYED:` last line:** B268.
- **Jira:**
  - highest key MPSCALC-231;
  - `eb735fe8` 0, `39009325479` 0, `BkQd8DlC` 0, `21c2aec…` 0, `e6f92a5f…` 1 (214);
  - `mpscalc-b272` 0, `created >= 2026-10-18` 4, `PRE-1` 9.
  - Every DF and W/S search is written into the kit with counts and keys.
  - Tickets 140/142/155/158/194/213/203/214/202/222-225/231 are all Backlog.

## UNMEASURED (and why)
- **Whether each DF ticket's acceptance really covers its candidate**, especially MPSCALC-222 for candidate 2. I read summaries only, not descriptions. The seat reads each acceptance and applies EXISTING/RELATED.
- **The board accountId**: not needed by default, because 0 tickets are created.
- **`scan()` over the drafted texts**: the seat runs it.
- **Whether the uncommitted records diffs belong only to B169 and B171**: I read `--stat` only.
- **Whether `MPS-R4` is free**: `cockpit.sh status` lists no MPS pane, unless status omits panes.
- **The exact verbatim text of B268 R-2…R-7**: it is cited by line (`:67-72`, checked by line prefix) and not copied into the kit.

## Slots and recommended defaults
| Slot | Default |
|---|---|
| R1 commit mechanics | B171's: one path-limited CLARIFICATIONS commit on root `main`; no push, branch or PR |
| R2 deploy comments DC-1…DC-8 | YES, 8 |
| R3 coordinator section for B268 R-2…R-7 | YES (B171 `:596` precedent) |
| R4 #83 merge comment on MPSCALC-231 | YES |
| R5 candidates 1, 5, 6 | BACKLOG rows only, no Jira (0 tickets); candidate 1 can become a ticket if Tuesday wants it |
| R6 B172 history catch-up | YES |
| SELF-CHECK stamp time | Tuesday's time |

With every default taken, the expected last line is `DONE: B272 1 C-entries, 1 coordinator section, 0 tickets, 14 comments` (14 = 8 DC + 1 MC + 5 DF).

## Expected wall-clock
About 25-35 min. B171 took about 15-20 min for 1 section, 4 tickets and 5 comments. This brief has 14 comments, a C-entry plus a section, 3 history entries, 3 BACKLOG rows, and five acceptance reads.
