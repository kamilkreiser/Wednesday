STARTABLE: YES (after your stamp; all 9 slots are four-underscore slots, none filled)

# B1195 drafter report - SEAT-N94, NexusAI RD-917, round 2 of 2 fix round

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1195_SEAT-N94_nexusai-rd917-round2-read-key.md`. Drafted by a Sonnet sub-agent under routing row C8 (`model-routing.md:98`). Drafted at the clock of the first read (a `date` printed 09:23:27 AEDT) through the last write; the kit carries no typed clock.

## BLUF
- One new forward commit on the EXISTING branch `b1183/nexusai-rd917-streamexport-destroyed-and-vanished` (head `559e4269c311627455fdd1ce77c33f60020e9833`, read by `gh api -X GET git/ref/heads/...`), plain fast-forward push, no PR, no rebase/amend.
- Fix shape as you decided: key the `reads` Map by a normalised key (strip trailing `/` and `\`, non-strings pass through) at the queue wrapper (`:240`) and in `judged` (`:231`); push into `vanished` only when the Map holds the key (`:244`). The ZIP and manifest for a directory at the two by-name sites stay as at main; the kit forbids refusing, skipping or warning about it.
- Cells: TWO new `test(` declarations in the EXISTING test file (X: directory at each by-name site; Y: duplicate and unknown-path ENOENT warning). Tests +2, suites +0: the branch's 5297/315 becomes 5299/315 (arithmetic asserted, not literals). Counts diff is TWO lines (`_updated`, `tests`), not three, because `suites` does not move.
- Model: Sonnet, row C2 (`model-routing.md:92`, counter "as C1", C1 at `:91` "one fix round on the same seat model"). Not C3 (`:93`, design surface, "the decision, not a spelled-out edit": the edit is spelled out) and not C4 (`:94`, nothing destroyed). Model id `claude-sonnet-5-5` (`models_latest.json:23`). Launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- The gate after it: tier 1 (G1, `:108`), round 2 of 2 (G-cap `:111`), separate kit.

## Facts re-measured (instrument; control)
- Branch head 559e4269 and main f282dec3: `gh api -X GET git/ref/heads/...`. `matching-refs/heads/b1195` length 0; control `matching-refs/heads/b1183` length 1. Open PRs length 0; control `pulls/99999` answers 404.
- `compare 559e4269...main`: one file, `HISTORY.md` +32 -0. Main's `backend/dataExport.js` blob `2a4ba545` (404 lines) and counts 5294/314 (raw files fetched with `Accept: application/vnd.github.raw`, `git hash-object`). Branch blobs: dataExport.js `8573bdc8` (447), test `f17a4236` (300), counts `9efc0fe6` (5297/315 at `:4`, `:5`), verify-suite.sh `eb9731f5`, build.yml `e4e5c095`, deploy-demo.yml `597b3487`, package.json `c29998f4`: all agree with the gate's C1 (`B1191_STATUS.md:28`, checked by `awk NR==28`).
- Every `streamExport` pointer in the kit was printed by `awk NR==n` / `/usr/bin/grep -n` over the raw head file (`:212 :217 :218 :221 :227-:231 :233 :239 :240 :242-:248 :256 :327 :374 :385 :394 :383 :393 :401 :406 :409 :411 :416 :425 :431 :438`). Control for the site count: `archive.file(` occurs 4 times at head AND 4 at main. Test file: `^test(` count 3, `.each` count 0, D/V/W at `:132/:236/:276`.
- Archiver (read in the gate's installed tree `worktrees/b1191-head/node_modules/archiver`, a READ only): `package.json:3` 8.0.0; `core.js:95` sourcePath = filepath; `:107` statQueue push; `:460` directory branch; `:461` name slash; **`:463` `trailingSlashIt(task.filepath)`**; `:189` emit entry; `:405` emit warning; `:488` ENTRYNOTSUPPORTED. Control: grep for `emit(.(warning|entry)` printed the three emit lines. The drafter did not run archiver.
- Gate STATUS pointers cited in the kit (`:1 :28 :48 :69 :76 :95 :96 :102 :121 :129 :130 :139 :141 :146 :148 :149`) each printed by `awk NR==n` and matched to the content cited.
- CI predicate lines at the head: `build.yml:29` (node 24), `:84` (verify), `verify-suite.sh:258 :343 :354 :366`. Deploy lines `deploy-demo.yml:26 :27 :28 :29 :33 :53 :91 :95`. Repo variables 0 (control `zzqxnonexist` 404), environments `["dev"]`. Org variables UNMEASURED by me (token 403); the gate read 0 at the repo-scoped endpoint.
- Clarifications: C-68 `:665`, C-190 `:2062` (item 2 `:2067`, ADDENDUM `:2076-:2081`), C-224 `:2412`, C-231 `:2467` (file is 2480 lines now).
- Ports: `lsof -nP -iTCP:8500-8599 -sTCP:LISTEN` empty, rc 1. Word-bounded scan of SEAT kits of 2-3 Nov for `N94`, `b1195`, `NexusAI-N94`: 0 files each; control `NexusAI-N93`: 8 files. Live panes: tuesday, Datasec/MPS-M88, Datasec/Security-Composer-C83, Datasec/MPS-M87, Datasec/HPSM-POC-H108, fleet-monitor; no NexusAI seat.
- `worktrees/b1195-n94` and `session-tools/b1195` absent (`ls` rc non-zero). `worktrees/b1183-n93` EXISTS (round-1 builder's clone): the kit tells N94 to make its own clone and not open it.
- Slots: 9 (`grep -c -E '_''_''_''_'` over the kit prints 9; the kit's REFUSE line says 9).

## D-decisions (mine, for you to veto)
- D1. Two new cells in the existing file (X, Y) instead of extra cases in V: V is green at the head today; folding cases into it would blur which fault is red. Five `test(` declarations, existing three untouched.
- D2. Cell X pins only "settles, manifest.json present, settings.json present" and does NOT pin what the ZIP/manifest hold for the directory (the product owner's call). The unchanged-output proof (property (c)) is a Step-5 PROOF in STATUS, MAIN blob vs FIX, per entry sha256 plus parsed manifest minus `requestedAt`, with a one-byte-plant control.
- D3. Cell Y's fixture must include a file under `feedback-attachments/`, because `:406` is reached only when `manifest.files` has a directory-store row (gate `:130`); a fixture without it cannot show the defect.
- D4. Three-state table per cell (head / main's dataExport blob / fix). Predicted head: D V W green, X Y red. Main: D V red, W X Y green. Fix: 5 of 5.
- D5. Re-run K1-K8 and K11 by anchor text (line numbers shifted), plus new MX (judge side un-normalised -> X red only) and MY (drop the push guard -> Y red only). K9/K10 are not required (gate Notes).
- D6. Size bound 15 added lines on `backend/dataExport.js`, hunks only in the region `:227`-`:248`. Round 1 was 52 added; the estimate for this fix is under 10.
- D7. Time: target 120 min, hard stop 180 min after Step 0 (round 1 was 150/210; this round is smaller, the verify alone is about 24 min per the gate `:95`).
- D8. REFUSE inverted from round 1: the branch MUST exist at 559e4269; any other head is a STOP.

## Q-questions for Tuesday (each with a default)
- Q-1. May the builder READ two of the gate's scripts as models, `session-tools/b1191/instrument/replicate-dir-hang.js` (45 lines) and `probe.js` (450 lines), though standing line 3 forbids opening another seat's tree? Default: YES for those two named files, read-only; the builder writes its own under `session-tools/b1195/`. (The kit says this; stamp Q-1 to confirm.)
- Q-2. If no plant can reach the product's real `archive.on('warning')` handler without editing product code (e.g. the ESM class prototype cannot be spied under the repo's jest transform), the builder STOPs. Default: let it STOP and ask; fallback you may ratify: run the plant through a spy on `ZipArchive.prototype.emit`, which I judged plausible but did not execute.
- Q-3. Bound of 15 added lines in `backend/dataExport.js`. Default: 15.
- Q-4. "Byte-equal" for the directory case is defined as: same entry-name set, same sha256 per entry except `manifest.json`, same parsed manifest minus `requestedAt`, same `filesIncluded` set, same `totalBytes`. Literal whole-ZIP byte equality is not reachable (the manifest entry is now last and carries its own timestamp; the gate's own p2 comparison used this definition, `B1191_STATUS.md:48`). Default: the definition above.
- Q-5. Launch line follows the B1183 template (`launch_when_cool.sh ... "WED_USAGE_STOP=100 BRIEF_SEAT_LEVEL=sonnet bash brief_seat.sh ..."`), not the `cockpit.sh add` form quoted in DRAFTER_RULES.md. Default: the template form; change it at stamping if you want `cockpit.sh`.

## UNMEASURED
- Whether the key normalisation fixes the hang: I read the archiver lines and the gate's probes but ran nothing (fences: read-only). The kit makes the builder prove it (cells X, Step 5 replication).
- Whether jest can spy `ZipArchive.prototype.emit` under the repo's transform (Q-2).
- Whether CodeQL flags `js/file-system-race` on the test's existing stat-then-unlink (`exportWithVanish`, `:220-:224` at the head); the gate could not judge it either (no PR). The kit tells the builder not to add a second such pair.
- Organisation-level variables (token 403). Hosted Build/CodeQL on this head. Node 24 on hosted runners.
- Jira: I did not call Jira; the kit's RD-917 facts are RELAYED from the gate's PRIOR WORK (`B1191_STATUS.md:121`).

## Outside-the-fences disclosure
- Read-only outside my two files: raw files of the NexusAI repo at the pinned sha and main via `gh api -X GET` under the project's `GH_CONFIG_DIR`; the gate's STATUS file, `CLARIFICATIONS.md`, `replicate-dir-hang.js` (first 60 lines), and the archiver `core.js` in `worktrees/b1191-head/node_modules` (another seat's tree, read-only, greps only); `model-routing.md`, `models_latest.json`, `DRAFTER_RULES.md`, the B1183 kit, `tmux list-panes`, `lsof`. Scratch copies of the fetched files sit in my session scratchpad (outside the project).
- No `decision_queue.sh`, no `fleet/briefs_staged/`, no scoreboard, no `_ledger.md`, no WEDNESDAY/FRIDAY tree, no Jira, no HTTP to any hosted host, no git write verb in any project repo, no `cd`.
- A case-sensitive grep advisory fired on several of my greps; none returned a zero I relied on without a positive control (each count above is paired with a control).
