# Drafter notes: Seat S 78th, hono 4.13.13 -> 4.13.18 lock refresh (re-commission, 12:0x AEDT 13 Nov)

Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatS78_hono_core_lock_refresh.md` (29,501 bytes by `wc -c`). All new scratch uses `s78_*` names in this folder; no old partial file was deleted or overwritten.

## Pins read
- develop `9105cfdee484a6342d4980d8fc9ea6da3bc87851`; refs/pull/2226/head `15914b780cb605df02895eb173aeaa2a70c35262`; refs/pull/2099/head `8967de8b17558890dc4ace2732cb8350768df601`. Read by `git ls-remote` at 2026-11-13 00:59:41Z = 11:59:41 AEDT (`s78_lsremote.out`, `s78_time_read.out`), identity kksecura confirmed by `gh auth status`.
- **PR 2226 is NOT merged**: `gh api pulls/2226` -> `merged=false`, state open, head 15914b780cb6, merge_commit_sha (the API's test merge) a5075b8dedfa. The brief's BASE rule makes the seat STOP and STATUS until it merges.

## Re-derived vs reused (old partial files from the killed run)
- RE-DERIVED (not trusted): develop and 2226 pins; the fetch into `clone2` (the old `clone2` was a blobless clone with refs only); census on develop and on the 2226 merge-tree (`s78_census_develop.out`, `s78_census_merged2226.out`; they equal the old `census_*.out`); the merge-tree tree `630e31d69ee2` (equals old `mt_develop_2226.out` AND Seat B 172nd's mail).
- REUSED as inputs only: `batch_20261113T005316Z.txt` (the copied mail; I read it, its numbers were then matched by my own legs run); the census script `census_hono.py` in the previous seat's scratchpad (read whole, four planted controls, rc 0 controls OK; it is the old run's script). `clone/` is a failed clone (Repository not found, no credentials) and was not used. `numstat_2226.out`/`diff_root_2226.out`: not relied on (I measured the diff myself, see s78_diff_*).

## What I measured (instrument in the brief; files in this folder)
- Census (47 locks, controls OK): exactly 2 carriers of hono, each one `node_modules/hono` 4.13.13, no other `@hono/*` key: root lock and `services/mcp-server`. **No package.json in all 47 declares `hono`** (`s78_pkgjson_hono.out`); bounds come from the locked packages: SDK `^4.11.4`, `@prisma/dev` `^4.12.8`, node-server peer `^4 || ^5.0.0-0`; all admit 4.13.18.
- Scoped `npm update hono --package-lock-only --ignore-scripts` (host Node v26.8.1, npm 11.19.0): root and isolated mcp-server both rc 0, **3 3 diff, 4.13.13 -> 4.13.18**, integrity `sha512-H9q/E1X...` (`s78_update_*.out`, `s78_diff_*.out`). So the verb lands 4.13.18 (4.13.16 is the minimum clearing; whether a 4.13.16 pin is a no-op is UNMEASURED).
- Legs (scratch `git init` of 47 locks + `scripts/audit`, `semver` via `npm ci` in `scripts/audit`): merged-2226 tree gate rc 1 (8 distinct, 5 baselined, the 3 hono ids NEW) and locks rc 1 (7 match, 4 baselined, 3 NEW in mcp-server); AFTER both refreshed: gate rc 0 (5/5) and locks rc 0 (4 match, 4 baselined). Outputs `s78_gate_*.out`, `s78_locks_*.out`. My first locks-AFTER run was rc 1 because I had not copied the isolated mcp lock back into the `after` tree (drafter slip, corrected and re-run).
- Rehearsal: develop + a python string edit of ONLY the hono entry (scratch, not the route), `git merge-tree` against PR 2226's head -> rc 0; merged blobs of both locks IDENTICAL by `git hash-object` to the npm results; planted control (edit node-server entry 2.1.5 -> 2.1.9) rc 1 with conflict. Against PR 2099 rc 0 (`s78_mt*.out`).
- Reachability of `hono` (import walk, `s78_walk.out`): mcp-server `dist/http-server.js` 86 modules, 0 hono, 0 node-server; `dist/index.js` 434 modules, 0 and 0; control SDK `streamableHttp.js` 240 modules, hono 1, node-server 2. Static grep of mcp-server dist+src: 0 imports (control express found). This was run on the GATE 349 built tree (PR 2226 head, hono 4.13.13 installed), which I did not build.
- Board (`s78_board.out`): no ticket carries any of the five hono ids; controls present. Plan: file ONE new ticket, priority 1, board account; KS-2194 is the sibling and is not touched.

## RULINGS Wednesday must make before stamping
1. **Two extra hono advisories.** GitHub lists GHSA-46wx-v44x-9hh2 (medium, `< 4.13.16`) and GHSA-4h7h-rv7c-7m2v (medium, `>= 4.5.1, <= 4.13.15`), published 23:30-23:31Z, first patched 4.13.16. The npm bulk API (leg 7's feed) does not list them yet; Seat B's run showed only three. Your commission said "ALL five ids absent": I read that as the 3 hono + 2 node-server ids. Rule: do you want the two extras in the ticket title and PROOF 1 (I put them in as a re-read-at-cut line, and the ticket title names all five), or only the audit-visible three? 4.13.18 clears all five either way.
2. **Target 4.13.18 vs 4.13.16.** The clean verb lands 4.13.18 (published 11-07 and 11-11 respectively for .17/.18; .18 is 2 days old). I read no package-age policy this session (carried S 77th's finding that STANDING_LINES has none; I did not re-grep). Accept 4.13.18? (The brief says STOP if the verb lands anything else.)
3. **Ticket: who files.** The brief has the seat file it (as S 77th did). Your read-only board grant means you cannot; option: Kam/the board account files before launch and the STAMP carries the key.
4. **Tier.** The brief says TIER 1 per your commission. Note for the ruling: hono is NOT loaded by mcp-server's two entries (measured), so the suite proves no-regression only; the tier rests on "a wrong lock re-freezes the floor", as with gate 349.
5. **The merge-tree vs 2226 requirement.** Once 2226 is merged (base = develop after merge), the merge-tree against its head is trivially clean; the brief keeps it as a PROOF line (and says it still holds under squash). Say if you want it dropped.
6. **Stamp slots left blank:** develop sha at the stamp, 2226 state, pane, floor, and Seat B's queue position for this row (who merges it: the brief says "a Seat B on your head-pinned GO", no ordinal).
7. **Launch precondition.** Do not launch until PR 2226 has merged, or accept that the seat STOPs at its base check.

## Faults and cautions
- First extract run failed because the shell had no credentials for the blobless clone (promisor); fixed by exporting the same extraheader; a stray empty `s78_work/` dir and `s78_work2/` hold scratch (nothing deleted).
- A `sed -i` on a script that had never been written (the heredoc was refused by the no-rm hook for `rm -f`): re-created without rm; no state changed.
- Scratch trees (`s78_work2/merged`, `after`, `mcpiso`, `clone2`, `s78_idx_*`, `s78_tmp_lock_*`) are regenerable; `.git` inside `s78_work2/merged` and `after` are scratch `git init`s. Nothing was written under `/Volumes/DevMASTER/!CODING/`, nothing pushed, mailed, posted, or written to Linear or GitHub.

## UNMEASURED
- The hook as a whole; leg 7 on a full checkout (I ran a faithful 47-lock corpus, not the hook).
- Root `npm ci` before/after; mcp-server's suite and tsc (carried from S 77th at the pin: 15/15 files, 137/137, tsc 0); the Docker route.
- CommonJS `require` paths in the import walk (resolve hook sees the ESM graph only); every other shipped entry of every other service (only two locks carry hono, so none other installs it; that is an inference from the census, not a walk).
- `@prisma/dev` reachability (gate 349's numbers, not re-derived).
- The hono 4.13.13 -> 4.13.18 code diff (not read).
- Whether a 4.13.16 pin is a no-op.
- The open-PR scan at the seat's cut (gate 349's 89-PR scan carried; I only re-ran 2226/2099 merge-trees).
- SKILL.md lines 483-484 at the seat's base (read at develop 9105cfdee484: "If a change genuinely does not affect either doc, say so explicitly and why").
- Linear priority/assignee of a newly filed ticket; any package-age policy beyond S 77th's grep.
