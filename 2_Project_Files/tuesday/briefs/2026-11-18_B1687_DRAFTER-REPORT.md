STARTABLE: YES. Nothing blocks a launch: there is no required predecessor (REFUSE 4(b) only needs the measured main `2de5e84c` as an ancestor), the branch `b1687/nexusai-lane-nx-l-log-sink-tests` is absent at origin (GET 404, control below), no NexusAI pane was live at drafting, and stamp_check exits 0 (119 claims, 119 measured, 0 not measured). Merges are held by the picomatch advisory, so the seat builds and pushes only (the kit says so and forbids any `gh pr` verb).

Drafter: Sonnet 5.5 Agent-tool drafter for Tuesday. Clock: started Wed 18 Nov 2026 06:21 AEDT, kit and sidecar finished 06:36 AEDT (`date` readings in the session: 06:21:37, 06:21:49, 06:28:55, 06:33:43, 06:35:15, 06:36:33).

## BLUF
- Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1687_SEAT-N149_nexusai-lane-nx-l-log-sink-tests.md` (354 lines) and sidecar beside it (`.measured`, 119 lines). Brief B1687, seat SEAT-N149, pane `Datasec/NexusAI-N149`, branch `b1687/nexusai-lane-nx-l-log-sink-tests`, Sonnet (`claude-sonnet-5-5`, `models_latest.json:23`), launch line carries `BRIEF_SEAT_LEVEL=sonnet`. Model row **C2** (`model-routing.md:92`), gate **G2** (`:109`), P4 `:50`, all re-printed with `awk NR==n`. Stamp slots (four) and the last line are four underscores (grep count 5).
- Scope: lane NX-L, RD-980 only, both items of the sweep (section 4), four ticket items, two owned test files: `__tests__/rd798-log-injection-chat-and-learning.test.js` and `__tests__/rd799-log-injection-auth-and-storage.test.js`. No counts file (no cell added or removed), no helper, no product byte committed.
- Item 1 (Major): the job-line mask becomes the ticket's date-time shape; `MASK-JOB-TIME` gains five rows (three plants must compare different, plus `deDE` and `narrowSpace` must stay equal). Item 2: **first-listed option taken and said so in the kit** (freeze one value per pinned state, the two route-190 masks removed); the four `p190`/`h190` hashes cannot be frozen by the drafter (no jest), so a chain step measures them three times, writes them with a frozen `set190.py`, and makes commit A inside the same lock acquisition. Item 3: first-listed option (a `LOCALE_ENV` of `C.UTF-8`, in all five rd798 boots, never the shared harness). Item 4: the stale cell is found by text (now rd799 `:287`, the ticket's `:272` is stale), retitled with the ticket's own suggested sentence.
- Red-first is by plants (eight server plants J1-J3, K1-K5 into a scratch `backend/server.js`; each must read GREEN at BASE and RED in named cells at head), three test plants (T1 old mask back, T2 the two masks back, T3 locale pin off under de_DE), and a locale run of the three log-injection files at BASE versus head. The cell count is held by rewriting `MASK-COUNT` and `MASK-PARAGRAPH` in place as negative controls (Q-1).
- Base: whatever origin main is at stamp time (REFUSE 4(b) needs `2de5e84c` as an ancestor). **Disjointness verified, not assumed:** open #219 files = `HISTORY.md`; open #220 files = `__tests__/rd385-shipped-root-markdown-identifiers.test.js`, `backend/server.js`, `backend/services/schedulers/healthSweeperScheduler.js` (paginated GETs); neither holds a path of OWNS-B1687. The kit does not wait for either, and says what to do if either lands first (HOLD 13: plants re-anchor by string, never by line).
- Slot **6** (band 23840-24479), trees `b1687-nodot/{old1,pre2,new9,mut1,chk11}` (program-printed, all slot 6; control `b1680-nodot/old34` = 2). Slots 0-5, 13, 15-17 are named by the 8 SEAT-N kits of 17 and 18 Nov; B1683 holds slot 4.

## Facts re-measured with instruments (origin main `2de5e84c799e32232d65cd759085d728d7141583`, tree `e09d1fe2c9b486e5a2b06a0af1ec9360f02339c0`, committed 2026-11-17T16:12:53Z; gh GET `branches/main` at 06:21:49 and `git/ref/heads/main`)
| fact | instrument | value |
|---|---|---|
| ticket RD-980 | GET-only whole reader (project `.env` in-process) | To Do, label `b1375-2026-11-09`, updated 2026-11-09T08:44, 0 comments, 0 links; four items; "a proposal, not decided" |
| counts file at main | contents API, decoded `sed -n 1,8p` | 5870 / 377, `_updated` 2026-11-17T14:25:10.296Z |
| blobs | contents API `sha` = `git hash-object` of the fetched file | rd798 `775d1e0b61be` (721 lines), rd799 `48157cbab1b2` (361 lines), rd800 `594a279fd214`, `backend/server.js` `bf648e298429` (22645 newlines) |
| last commits | commits API `sha=2de5e84c&path=` | rd798 `5fbad1ba`, `2ec2a32e`, `71f7787c`; rd799 `5fbad1ba`, `f624eb33`, `2ec2a32e` |
| open PRs | GET `pulls`, GET `pulls/<n>/files --paginate` | #220 (head `41907572`) three files above; #219 (head `9f998e9d`) `HISTORY.md`; disjoint from OWNS-B1687 |
| b1687 branch at origin | GET `git/ref/heads/b1687/...` | 404; control: `refs/heads/main` -> `2de5e84c...`, `b1683/...` -> `41907572...` (ssh `ls-remote` is not available to the drafter) |
| pointers in rd798 | `awk NR==n`, `grep -n -F` | `clockMasked` :434, job mask :436, route-190 masks :437 :438, `hoursCanon` :439, `EXPECT_HOURS` :442, cells :467 :484 :489 :494 :499, `MASK-ISO` :521, `MASK-JOB-TIME` :529, `MASK-COUNT` :540, `MASK-PARAGRAPH` :548, `bootServer` :138 :199 :215 :233 :274 |
| rd799 stale cell | `grep -n -F`, `awk NR==287` | :287, the old title occurs once; repo-wide over the tarball of main only the rd799 file holds it |
| plant anchors in server.js | python `count` over the file | each of the seven anchor strings occurs exactly once (timeStr :13743, template :13744, count :10661, description/impact/action :20234 :20235 :20236, threshold :20225); control: an absent string counts 0 |
| ASCII | python count of code points over 127 | 0 in both files and in the patch (control: a planted U+2014 counts 1) |
| mask logic | `maskcheck980.js` (kit text, node only) | BASE: before, after, invalid, critical all `true` (the weakness); head: all `false`; deDE, narrowSpace stay `true` |
| mask vs locales | node loop over `toLocaleString` for en-AU, en-US, de-DE, en-GB, fr-FR, ja-JP, hi-IN, C | 8 of 8 masked, 0 not; `/\s/.test(' ')` true |
| locale effect | `LC_ALL=de_DE.UTF-8 LANG=de_DE.UTF-8 node -e ...` vs `C.UTF-8` | `6.11.2026, 18:44:28` and `1.234,5` vs `11/6/2026, 6:44:28 PM` and `1,234.5` |
| patch | `apply_patch.py --plan`, then real, then a second real | ten hunks each once, `applied`, `node --check` ok both, second run `old text occurs 0 time(s)` and STOP; result `cmp` equal to the drafter's own edit; sha256 `1c1373dbaa46ea4e6d23f897816ad3f753f15d1fba4851d7c6cf07b13c94abf2` |
| `set190.py` | run on a scratch copy | `lines changed: 4`, `written`, `node --check` ok; second `--plan` `lines changed: 0` |
| kit blocks | extracted by program from the kit and compared | patch, `maskcheck980.js`, `set190.py`: all three byte-equal to the scratch files (the first write turned the escapes `•`, `…`, ` ` into literal characters; fixed, see disclosure) |
| code scanning | paginated GET `state=open&ref=refs/heads/main` | 22 open, 13 in `backend/server.js`, 0 in rd798 or rd799 |
| CI predicate | `awk NR==64`, `NR==93`, `NR==29` of build.yml | `node scripts/assert-browser.js`; `npm run verify -- --maxWorkers=2`; `node-version: '24'`; no LC_ALL, LANG or TZ in the file (`grep -c -i` 0, control `node-version` 1) |
| deploy trigger | `grep -n -A2 -F 'push:'` of deploy-demo.yml | `push:` `branches: [main]` `paths-ignore:` (a branch push starts nothing) |
| landing rule | `awk NR==2067` of CLARIFICATIONS.md | "Merge path: open a PR from the gated branch, wait for CodeQL ..., then land the SAME commit. Never squash, never rebase" |
| slot / listeners | `names1687.py` (copy of the B1683 drafter's, retagged), `lsof` | 11 listeners machine-wide, 0 in slot 6; `lsof -iTCP:23840-24479` 0 rows; panes `tuesday`, `fleet-monitor` only |
| tools by path | `ls .tools/b1683/` | newest set present (`lib.sh`, `lib2.sh`, `commit.sh`, `static.py`, `plant.py`, `rs.py`, `slot.py`, `census.sh`, `s_mstep.sh`, ...); B1683 clone's identity lengths 12 and 46 (value not printed); project has no `.tools/node*` |

## Chain table: each step's inputs and where each comes from (rule 4)
| step | inputs | produced by |
|---|---|---|
| 0 browser | `old1` at BASE, `scripts/assert-browser.js` | Step 1 (clone, detach, `npm ci`); the file exists at main (ls of the tarball) |
| 1 base | `old1`, rd798, rd799, rd800 at BASE, `maskcheck980.js` | Step 1; the program is written from the kit's block before the lock |
| 2 loc-base | `old1`, the same three files | Step 1; locale env is on the command line only (HOLD 15) |
| 3 plants-base | `mut1` at BASE, plant specs (JSON for `plant.py`), saved originals | Step 1 tree; specs written before the lock from the kit's table; originals saved inside the step |
| 4 measure | `pre2` (BASE + patch uncommitted), `rd980.patch`, `set190.py`, `wt` | Step 1; patch and script written from the kit; `pre2` made by the patch before the lock (no jest) |
| 5 commitA | `wt` (patch + hashes), `commit.sh`, identity | step 4 writes the hashes; the patch is applied in `wt` before the lock; the step also creates `new9`, `chk11`, re-detaches `mut1` at A |
| 6 head | `new9` at A | step 5 |
| 7 loc-head | `new9` | step 5 |
| 8 plants-head | `mut1` at A, plant specs | step 5; specs from the kit (T-plants anchor on the head text: counts 1 measured on a patched scratch copy) |
| 9 readers | `new9`, the Step 1b(iii) list | step 5; list is the rd798 file alone at drafting |
| 10-12 mainmove, p-plain, mainmove-last | clone, `chk11` at A | step 5 |
The one cross-step dependency that is new: step 4 produces four values that step 5 commits. Both are in ONE lock acquisition (step 4 appends the list); the kit says so and tells the seat to prove the append with `--plan` before the lock.

## D-decisions (the drafter's)
- D-1 One commit A (two files), made inside the chain because the four 190 hashes are only measurable by a jest run. Alternative would have been a second chain (violates one acquisition).
- D-2 Option choices: item 2 first-listed (freeze per state, masks removed); item 3 first-listed (env, in the test file's boots, not the harness). Item 3's value `C.UTF-8` is the ticket's own "hosted shape" it measured green.
- D-3 Cell count held constant: `MASK-COUNT` and `MASK-PARAGRAPH` rewritten in place into negative controls (their masks no longer exist). Exactly six titles change, all by the patch; a seventh or a count change is a STOP.
- D-4 rd799 and rd800 under `de_DE.UTF-8` are measured (steps 2 and 7) and any red there at BASE is reported, never edited (the ticket's four items name only rd798's cell; rd800 is not an owned file; the shared harness is out of scope).
- D-5 Plants are scratch-only in `backend/server.js` of `mut1` and the kit forbids ever staging it; the kit forbids printing any range of that file (two comment lines carry the retired address until #220 lands).
- D-6 Tools are taken from `.tools/b1683/` (newest), step scripts written fresh (B1683's Correction 5).
- D-7 No wait on #219 or #220: disjoint files. If #220 lands first, plants anchor by string; HOLD 13 covers a main move.
- D-8 Time of lock hold PREDICTED about 55 minutes (verify 23 min 18 s RELAYED from B1683, plus about thirty short `-t` runs); HARD STOP slot left for Tuesday.

## Q-questions for Tuesday (each with a default)
- Q-1 Rewrite `MASK-COUNT` and `MASK-PARAGRAPH` in place as negative controls (count unchanged, titles changed), or delete both (count 5870 down by two, a counts regenerate, contrary to this kit's "no counts" rule)? Default: rewrite in place, as the kit does.
- Q-2 Pin the child's locale to `C.UTF-8` (the ticket's hosted shape) or to `en_US.UTF-8`/`en_AU.UTF-8`? Default: `C.UTF-8`. Node 26 prints the same en-US form for it (measured); the hosted runner's real locale is unmeasured, which is the reason for pinning.
- Q-3 Gate G2 (the kit's choice) or G1? Default: G2: tests only, the product file is planted in scratch only.
- Q-4 If rd799 or rd800 read red under `de_DE.UTF-8` at BASE (unmeasured; the ticket names only the rd798 cell), is a follow-up ticket wanted? Default: the seat reports it in READY and does not edit; Tuesday opens the follow-up.
- Q-5 The ticket's done-when (5), the independent review, is Tuesday's G2 gate; agreed? Default: yes.
- Q-6 Sequence against NX-M (RD-717, RD-749): both would touch the counts file only if a cell is added; NX-L adds none. Default: one NexusAI seat at a time, NX-L first (the sweep's order).

## UNMEASURED
- No jest was run by the drafter. Every red set, the eight-plant matrix, the `de_DE` red set at BASE, the cell counts N798, N799, N800 (PREDICTED only as line counts 28 and 16), the four 190 hashes and the final pair are PREDICTED or to be measured by the seat. The mask logic was proved by node on the extracted `clockMasked` text only; `maskcheck980.js` does not boot a server.
- Whether route 190's day and night answers really differ in count and paragraph (RELAYED from the ticket); whether any 190 answer carries run-varying text beyond the ISO mask (the kit's three-run agreement rule and STOP cover it).
- Whether the 190 and 198/201 answers are unchanged by removing the paragraph and count masks for the 198/201 cells (the 198/201 `EXPECT_HOURS` values stay; if one reads red at A, step 6 is a STOP).
- Hosted runner locale and Node 24 behaviour; whether the other tests that scan test files (hidden characters, shape bans) accept the patch (the full verify is the last word).
- Ssh `git ls-remote` (not available to the drafter; the absence of the branch was read with gh GET).
- Whether any NexusAI pane is live (seat's REFUSE 4(a)); whether #219 or #220 lands before launch.

## Outside-the-fences disclosure
- Writes: the kit, its sidecar and this report in the briefs folder. Scratch only under the session scratchpad `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/0f6ab911-939a-403c-8cca-13683e6f84b8/scratchpad/` (main's two test files, the harness, `backend/server.js` and a tarball of main extracted into its own directory, the patch, `set190.py`, `maskcheck980.js`, `names1687.py`, node logic scripts, the ticket read). Nothing written in the NexusAI project folder and nothing under `fleet/state`.
- **Instrument deviation to say plainly:** the Write and Edit tools turned a backslash-u escape typed in the kit text into the literal character (U+2022, U+2026, U+202F, 27 characters in all). I fixed this once with a small python replace on my own kit file (the escapes restored; non-ASCII count 0 afterwards) and then proved the three embedded blocks byte-equal to the scratch files by program. I also used python for several small text edits to the kit (sha, wording) and for writing the sidecar from the `--init` skeleton. All of it is inside my two files plus the stamp_check sidecar.
- Reads: RD-980 by a GET-only reader (token never printed); gh GET under the project's `GH_CONFIG_DIR` (branches, ref, commits, contents, tarball, pulls, pulls files, compare, code-scanning, `user` login counted only); project files read: B1683 kit, drafter report and STATUS (`## Corrections` and the chain table), `.tools/b1683/` file names and `apply_patch.py`, `plant.py`, `namescan.py` and `slot.py` (headers), CLARIFICATIONS.md line 2067, `scanlib1114.py:20` (a code line, no names read from it), `session-tools` listing, the sweep note, model-routing and models_latest lines. One `git ls-remote` was attempted against the project's local checkout (a read verb) and failed with a publickey refusal; no effect.
- One hook refusal (an unquoted `=====` in a command, before any effect); several advisories (grep and cut) heeded by counting with controls. No `cd`, no git write in any project repo, no az, no ssh, no docker, no HTTP to any host except GitHub and Jira GETs, no jest, no `decision_queue.sh`.
- No address, host or revision name was written into the kit, sidecar or this report; the kit names `azurecontainerapps`, `azurewebsites` and `azurecr` only as words in a scan instruction, and the retired address is named only as "the retired VM address". The kit has 0 dotted quads (control: a planted one counts 1), 0 person-name hits by the underscore-aware pattern (nine names, controls fire), and the words "card" and "decision-queue" appear only inside the scan-pattern instructions and as "no card id".
