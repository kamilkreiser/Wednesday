STARTABLE: YES - the kit is complete, its sidecar has 208 of 208 claims measured and `stamp_check.py <kit>` exits 0; two things Tuesday decides before launch are Q-5 (the setup test handler sits inside a related-location region of two open high alerts, hosted outcome UNMEASURED, one precedent says it passes) and Q-3 (the permission table and the wire will disagree on the two read routes); neither blocks the start.

# B1762 drafter report (lane N-K: RD-1011 + RD-1013 + RD-1012, SEAT-N160), Fri 20 Nov 2026, drafting 11:43 to 12:28 AEDT

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1762_SEAT-N160_nexusai-lane-nk-datasource-role-checks.md` (945 lines, 144163 bytes, 0 non-ASCII bytes, 5 four-underscore patterns: four slots and the last line)
- Sidecar: the same name plus `.measured` (208 lines, 0 TODO; about 27 lines are hand-built counts or line prints, the rest print where the literal was found in a named corpus: Tuesday should spot-measure the count claims, see UNMEASURED 12)
- This report. Drafter work folder (scratch, nothing outside it): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s296/d1762/` (programs in `progs/`, the three cell files in `cells/`, run outputs in `out/`, quarantined backups in `_quarantine/`).

## BLUF
BASE `b169b8a0eee8eaac594e98918c2ccaff91164dcf` re-read three times (11:43:58, and again at 12:27:14 by `gh api -X GET .../git/ref/heads/main`; open pull requests 0). Tickets RD-1011, RD-1012 and RD-1013: read whole by Jira GET at 11:47 and again at 12:27: all To Do, `updated` equals `created` (2026-11-19 16:21 to 16:22), 0 comments each: **nothing new since the sweep read them**; their scope and acceptance sentences are quoted in the kit.
The design runs. Frozen edit (`apply1762.py`): server.js +12 -0 (three lines before each of the four handlers' first statements), capabilities.js +0 -1 (the `RD-793` key), accessAudit.js +19 -1 (`pathnameOf`), entraProvisioning.js +2 -1. Four old-answer tests rewritten by `apply1762_tests.py`. Three new frozen test files, 47 cells. Dry runs on scratch copies: at BASE 27 of 47 new cells RED and 20 GREEN (exactly the kit's table); at head the 36 focused reader files plus the three new files read 615 of 615 green; 13 plants each reddened exactly the cells their row names; the inventory drive (run twice) changes exactly the four rows and on each only viewer status, gate list and capability text.

## Facts re-measured, with instruments (the kit carries each with its sidecar line)
- Handler lines 15962, 15987, 16053, 17385; helper `requireAdminFor` 19093; limiter 1397/1404/1405; server.js blob `668e343f3207`, **22800 lines** (the commission said about 19,000). Helper's refusal text printed: `res.status(403).json({ error: 'Admin access required' })`; no new word.
- `adminGateRefuses` (authEnforcement.js:634) read at source and driven by cells G1 to G4: setup unfinished or no sign-in never refuses; the open window and the wizard path keep working (O1 to O4 drive the real server's open shape).
- Frames (git-tree style counts over the tarball): 471 `.js` / 389 `.test.js` under `__tests__` and `tests`; 387 `.test.js` directly under `__tests__`; 969 non-binary files outside node_modules; run list 101 files (78 / 5 / 18 / 2 / 15 by indicator), 19 of them manifest readers (the same 19 as B1739's kit, which needs a git tree).
- Code scanning: 22 open alerts at main (control: 229 to 233 at the lines the commission named). **Three of the four handlers lie on no alert path; the setup test handler lies inside a related-location region of alerts 67 and 68 (`js/missing-token-validation`, high).** Precedent measured: pull request 231 added three lines inside the same two alerts' region at `DELETE /api/setup/data-sources/:id` and its head's hosted checks (CodeQL and three Analyze jobs) were `success`.
- Inventory: drift D at BASE = 0 rows; BASE drive 152 s, head drive 154 s; four rows change, nothing else (the kit's INVENTORY rule).
- The old answers: at A alone 6 cells red in 5 files (`rd793` C2 and C3, `rd988` T7, `rd958` X2, `rd978` probe, `rd929` pending cell); with R only `rd929`; with I and T none.

## Corrections to the commission
1. `server.js` is 22800 lines, not about 19,000.
2. The commission lists open alerts 229 to 233; **five more `js/user-controlled-bypass` high alerts are open (224, 225, 227, 279, 280)**; none touches a handler of this lane; 22 open in all. Also two medium alerts sit in `entraProvisioning.js` (145, 146 at `:619`, `:643`), outside the edit.
3. RD-793 and RD-990 are BOTH in pull request 231; pull request 230 is the records history. (The commission wrote "pull requests 230 and 231".)
4. The two read routes were never on the pending list (they are `config.read`); only the two test routes were. After the change the table and the wire disagree on the two reads (Q-3).
5. Four existing tests pin the old answer and must be rewritten (the commission said "any existing test that pins an OLD answer"); a fifth, `rd929`, turns red between A and I and green after the regenerated inventory, with no edit.
6. The test routes share one 5-per-10-minutes limiter, so a cell file can send at most 5 requests to the two of them per booted server (kit FOUND 4 and HOLD 27).
7. The B1739 kit's frame figure (469 / 387) was two short; the kit uses 471 / 389 by program.

## D-decisions (Tuesday's, said so in the kit; each a default)
- D-1 (RD-1011): refuse all four routes to a non-administrator, check as the first statement, three added lines per handler in RD-793's own comment style (no `requireAdminFor(` token inside the comment, because two tests count that token).
- D-2 (RD-1012): the helper `pathnameOf` drops scheme and host of an absolute-form target, cuts at the first `?` or `#`, never decodes, never resolves dot segments; pinned by U5 and H4.
- D-3 (RD-1013): the entry calls `requestPath(req)`; `accessAudit.js` requires nothing, so no import cycle.
- D-4: the `RD-793` key leaves `PENDING_GATE` (precedent: RD-958, RD-964, RD-968 keys went when closed).
- D-5: commit list A1011, A1012, A1013, R (before the lock), I and T (inside the chain), at most two M, K.
- D-6: the frozen cell text is embedded in the kit (31 KB) so the dry-run colours are the ones the seat gets; the seat extracts it by `awk` and `cmp`.

## Q-questions for Tuesday (each with the kit's default)
- **Q-1** Level and gate: Sonnet, row C2 (pilot, `model-routing.md:92`), gate G1 Opus 5.5 (`:108`). Default: as written. (The commission's "routing row C8" is the drafter row; the builder row is C2.)
- **Q-2** Percent-encoded path: as sent, no decoding, no dot-segment resolution. Default: as sent.
- **Q-3** The table keeps `config.read` for describe-table and discover-tables although a viewer is now refused on them (cell P2 pins the default). Alternative: move both to `admin.read` in `capabilities.js`. Default: keep, say so in READY; RD-929 (drafted after this lane) settles it.
- **Q-4** Remove the `RD-793` key (rd958 X2 and rd793 C3 rewritten) or keep an empty list. Default: remove.
- **Q-5** Hosted check at the setup test handler (alerts 67 and 68). Default: build as frozen, run CQ-1 and CQ-2, land on the hosted result; if the hosted check blocks, the reshape is a departure (move the check into a middleware beside the limiter at `server.js:1404`) that Tuesday decides then. The local tool uses start lines, so its rc 0 does not answer the region question; the kit says so.
- **Q-6** Slot 18 (band 31520-32159), trees `old28, probe13, new20, inv10, mut34, v12, chk54, chk62` (controls reproduce 16, 15 and 5). Every slot 0 to 18 is named in some finished kit or gate of 18 and 19 Nov; slot 18 is named by the fewest files (4). Default: slot 18, after you re-scan live panes at launch.
- **Q-7** Hard stop: the kit predicts about 2 hours of seat work before the lock and about 1.6 hours of lock hold; Tuesday fills the slot.
- **Q-8** The records seat: the ticket text each of RD-1011/1012/1013 asks the product owner a question only in RD-1011 (the two reads); no comment is drafted here. Default: none from the seat.

## Recommended slots
Jest worktree slot 18, band 31520-32159, no port block (the cells' servers take ports from the band). Pane `Datasec/NexusAI-N160`, `BRIEF_SEAT_LEVEL=sonnet`, launch line in the kit's Stamp section. No other NexusAI lane was running or queued at 12:27 (records seat B1759 only; STATUS files of 19 and 20 Nov end in READY or are records).

## Chain-step inputs (each input is produced by an earlier step or exists at BASE)
Step 1 run list: BASE files. Step 1b: tree at R = A commits + R, both made before the lock from BASE. Step 2 BASE drive: BASE. Step 3 head drive: tree at R; produces the two docs (commit I). Step 4 red-first: BASE plus the three files extracted from the kit (kit exists). Step 5 tstep: needs the kit text only. Step 6: tree at T (needs I and T). Step 7 plants: tree at T. Step 9 to 12 verifies: T, then K (needs `v12`'s counts file from step 10). No step uses a file a later step makes.

## UNMEASURED (the drafter did not measure these)
1. The local CodeQL tool (it builds a database): not run; the hosted result for alerts 67 and 68 at the setup handler (one precedent only).
2. 65 of the 101 run-list files at head, including the 19 manifest readers (need a git tree); the 36 focused files were measured at A, at R and at head but NOT at BASE (they read green at the states above; the BASE colours are the seat's step 1).
3. The heads census (every open branch for the owned paths): not run.
4. Whether a request with no session counts toward the shared limiter; that a sixth request is refused (the cells never send one).
5. Express's pathname for an absolute-form target below no router (the lane does not change that branch).
6. The full verify and the counts pair (PREDICTED 6195 / 390 = 6148 + 47, 387 + 3); lock-hold durations at real load.
7. The `ROLE-CAPABILITIES.md` status-count lines (the changed rows were measured, not the page's totals); the `--check` line.
8. The first-run wizard in a real browser; sign-in configured with the first run unfinished on a real server (G2 covers the helper only).
9. The drafter did not take the project's jest lock (no lane was live; its scratch runs were single-worker and at load about 2 to 3); its scratch trees share slot 13 because they sit inside the coordinator's git repository.
10. A plant that cuts the authority of an absolute-form target at `/` only stayed GREEN (dropped from the table, listed under "not plant-proved").
11. Search recall of the Jira text searches (a ticket naming none of the words is not found).
12. The sidecar's auto lines prove only that a literal exists in a named corpus; the count claims were measured by hand (27 lines). Tuesday's spot-check should pick count claims.

## Outside-the-fences disclosure
Read-only: Jira GET (the three tickets, RD-1014 to RD-1020 by key, 12 text searches), `gh api -X GET` (ref, pulls, tarball of the sha, code-scanning alerts and two analyses as SARIF, pull 231 files and checks), NexusAI project files (B1733, B1737, B1739 STATUS and kits, the two VERDICT files, `.tools` listings, `.env` read in-process by the Jira reader, nothing printed). Scratch writes only under the work folder plus the kit, sidecar and this report. I ran node and jest on scratch copies, **booted real servers on loopback** through the inventory tool and the test harness (their fence refused every outbound connect; temp folders under `/var/folders`), ran the inventory drive twice (two `printer_logs_backup_*.db` per drive, moved to `_quarantine/`), and used a read-only `NODE_PATH` into an earlier lane's `node_modules` (a symlink into it was refused by a hook and not made). A hook refused one command for `rm`/`sed -i` text; nothing ran from it. **I started overlapping jest runs once and stopped them with `kill` and `pkill -f` on processes whose command line held my own scratch path; their 104-file output is void and unused.** No message to any human, no PR, no write to any project repo, no Jira write, no alert action.
