STARTABLE: YES (after Tuesday stamps: 8 four-underscore lines, S1-S7 at lines 52-58 and the last line 66; Q-1 to Q-6 to answer in S3)

# B1022 drafter report (SEAT-G252, tier-1 gate of branch b1016/hpsmpoc-388-security-workspace-part-b, HPSMPOC-388), drafted Sun 2026-11-01 06:3x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1022_SEAT-G252_hpsmpoc-388-part-b-gate-tier1.md` (66 lines; sha256 `35c3292c894f39257c9e28b4ac033183cb1fcc2ff82886a61e88800966f0b238`) and its exact copy `.md.pre-stamp` (made with `cp -p`, `cmp` equal, same sha256). Seat `Datasec/HPSM-POC-G252`, ports 9270-9279, Opus (`claude-opus-5-5`, `BRIEF_SEAT_LEVEL=opus` inside the launch quotes), launched through `tuesday/tools/launch_when_cool.sh`. Shape: part A's round-1 gate B953 (G224, 70 lines, the tier-1 checks C1-C10, severity table, verdict line, FOR TUESDAY, landing checklist), with the no-PR branch-gate parts of B1005 (G246: hosted CI judged locally, the four landing data files, "NO PR; hosted CI NOT RUN" Condition). B965 (part A round 2) was read as the delta-gate counterpart and for its findings B965-1/-2.

## BLUF
- **G-number: G252** is the next free one. The `SEAT-G<n>` names in `tuesday/briefs` end at G251 (2 files). `/usr/bin/grep -r -l -w 'G252'` over `2_Project_Files/tuesday` returns nothing (rc 1); the control `G251` hits 3 files. No pane carries the name (count 0). B1022 has no file in `tuesday/briefs` (count 0).
- **Tier 1 confirmed.** `model-routing.md:108` is G1 ("security surfaces ... anything handed to a client tester"), `:111` is G-cap, and `:92` is the builder's C2. All three were printed by `/usr/bin/grep -n -i -E '^\| (G1|G2|G-cap|C2) '`. The model id is `claude-opus-5-5` at `models_latest.json:17`.
- **The subject matches the commission.** Measured by `gh api -X GET`:
  - main is `77c3132e`. The branch is `db9c2625`, 3 ahead and 0 behind.
  - 31 paths, +999 -39 (16 added, 15 modified). The commits are `e4019e7a`, `8a7c872e` and `db9c2625`, each with one Sonnet trailer and unsigned.
  - There are 0 PRs for the branch and 0 open PRs. Check-runs and actions runs on the head are both 0; the control (main's commit) shows 19 check-runs.
  - `ci.yml` at the head is blob `0176b491`, 679 lines.
- **The five acceptance criteria** are C3 (reviewed-only, plus the closed release table where a failed or pending read never releases), C5 (no-price, no-write and the register byte-equal) and C4 (Demo aliases, now including the alias path made live, not only the no-run words).
- **Other checks the commission asked for:**
  - The `useSecurityData.ts` removed-line table: 5 removed lines, one of them the `Loaded` interface the kit itself told the builder to extend.
  - The D-8 tail: exactly one line in each of the four files.
  - The words count reconciliation.
  - Tokens, 44 px, widths 390-1440 and axe.
  - The seven-view 404 table, with an HTTP control under a plant.
  - CI predicates from `ci.yml`, with line numbers.
  - Commit sentences graded at the head.
  - The phase line, the verdict line, graded findings with fix-shapes, and the four landing files.
- **Words count reconciled (the kit tells the gate to re-measure).** The kit's item 7 (line 54) quotes 15 strings, and one of them ("Remediation roadmap") is marked as already on main. That leaves **14 new strings**: 3 titles and 11 design strings. A `python3 -I -B` extraction printed all 15. The builder's READY line also says 14. The B1016 drafter report's "13 ... 10 design + 3 titles" is an **arithmetic miscount**: its own Q-1 list underneath names the same 14 (11 + 3).
- **Things the gate is pointed at (predictions, not findings):**
  - The "most severe first" claim. `SecurityFindings.tsx` sorts nothing itself; the gate finds where the order is made (g11).
  - Owner case (iv), a saved entry with an empty owner. Part B shows "Not recorded"; the partner screen is unread.
  - The A2 reading (an older issued run is shown while a newer run is in progress).
  - `HeldReport` reads `session.assessment` for any held route id. The gate checks cross-customer disclosure.
  - The canned harness now puts a newer `report-issued` run above part A's `scored` run.
  - Two stale texts left on purpose under D-8: the `proxy.ts:27` comment and a `proxy.test.ts` row title.
  - The type-scale HOLD ("no 9 to 13 px type"), checked against `text-sm`.

## Facts re-measured (instrument; control)
- **Main and branch:**
  - `gh api -X GET git/ref/heads/main` = `77c3132e213b24616e6f1af9379d2fee66c889b7`.
  - `matching-refs/heads/b1016` = one ref, `db9c2625815b78db19419380c5cb55a41b37f43b` (control: `heads/b101` gives 2).
  - `matching-refs/heads/b1022` = 0.
  - `compare 77c3132e...db9c2625` is `ahead` 3 / `behind` 0, with 31 files, additions sum 999, deletions sum 39, and statuses 16 added / 15 modified (control: `compare 77c3132e...77c3132e` gives 0 files).
  - Each commit's parent is the one before it.
- **PRs and CI:**
  - `pulls?state=open` = 0. `pulls?state=all&head=datasecau:b1016/...` = 0 (control: `pulls?state=closed&per_page=3` gives 268, 267, 266).
  - `commits/db9c2625/check-runs` total 0 and `actions/runs?head_sha=db9c2625` total 0 (control: `commits/77c3132e/check-runs` total 19).
  - Repo merge settings: `allow_squash/merge/rebase` true/true/true. `squash_merge_commit_title` is `COMMIT_OR_PR_TITLE` and `squash_merge_commit_message` is `COMMIT_MESSAGES`. So a squash without explicit text would concatenate the three messages and three Sonnet trailers; the kit's squash-body rule (exactly ONE Opus trailer) covers this.
- **CI** (`contents/.github/workflows/ci.yml?ref=db9c2625`, sha `0176b4915d69...`, 679 lines; lines found by `/usr/bin/grep -n`, and the `web-build` term hits 13 lines as a positive control):
  - `on:` is lines 14-18.
  - `web-build` is 371, with npm ci at 387, audit at 390, audit-dev at 395, lint at 396, typecheck at 409, build at 413 and check-shards at 426. Node 24 is set at 384, 463 and 501.
  - `web-unit` is 450, with npm test at 478.
  - `web-e2e` is 483, with the shard matrix at line 491 and `--shard` at 515.
  - `web` (Next.js) is 526 and needs 528. `secrets` is 629.
  - Lines 1-3 read "Build + test only. No deploy job".
- **Diff content** (read from the `compare` patches): the 5 removed lines of `useSecurityData.ts` are the `Loaded` interface, the two `loadApi` returns and the two hook returns. `proxy.ts` has the one alternation (line 29), and the comment at 27 is unchanged. The `customer-nav.ts` change is the four `built` flags only. Also read: the four views, `roadmap.ts`, `reports.ts`, `views.ts`, the `findings/page.tsx` shape (12 lines, `metadata.title` "Gaps and findings"), the harness/fixtures change, the new `toBe(15)` row in no-price, and the `VIEWS` lists in both proxy tests.
- **Round count:**
  - A `bash` first-lines loop over the project `Briefs/*_STATUS.md` read 537 files and found 129 `GATE VERDICT` lines.
  - The filter `part b|b1016|HPSMPOC-388|security-workspace` gives 0.
  - Positive control: `security preview` gives exactly B953 (NO GO, round 1 of 2, class "customer security preview") and B965 (GO WITH FINDINGS, round 2 of 2 = the cap, same class).
  - So part A's class is closed, and part B is the NEW class ruled at the B1016 stamp (line 135, Q-8). The result is NO GO 0 of 2 on "customer security preview, part B".
- **Landing rule:**
  - The analysis repository `datasecau/HPSM-POC-analysis` main is `06e8d8f9`; `1_Project_Definition/CLARIFICATIONS.md` has 5035 lines.
  - Line 4860 is part A's landing entry, "... a head-pinned squash; customer security preview, part A". Lines 5002 and 5018 are PRs #267 and #268, also head-pinned squashes. The control (an absent string) gives 0.
  - The project's local `1_Project_Definition/CLARIFICATIONS.md` (192 lines) has the older precedent at line 138, "squash-merged head-pinned".
  - Main's recent subjects carry ticket keys (`e0b93957` "HPSMPOC-422 -423: ...", `d0eff4ca` "HPSMPOC-411 -415 -408: ...") and each has at most one trailer.
- **Ports: 9270-9279.**
  - Census: a word-boundary scan of the 54 non-`.pre-` SEAT kits dated 10-31 and 11-01 found 9xxx decades from 930 to 999 in use, with 91x and 92x unused. `/usr/bin/grep -l -w -E '927[0-9]'` over them gives rc 1 (controls: `962[0-9]` hits B1020's kit, `940[0-9]` hits B1016's kit).
  - Listeners: `lsof -nP -iTCP:9270-9279 -sTCP:LISTEN | wc -l` read 0, then 2 with a `python3 -I -B` listener on 9279 (6 s), then 0. The whole machine's TCP listeners are 5000, 7000 and 49xxx-65xxx, none in 9xxx.
  - 9400-9409: still referenced by the B1016 kit, but that builder is finished and its pane is absent from the list. The gate does not use the block anyway: the kit says never bind it.
- **Panes** (`tmux list-panes -a`, 06:3x): `tuesday`, `Datasec/MPS-R105`, `Datasec/MPS-G251`, `Datasec/NexusAI-M60` and `fleet-monitor`. No HPSM-POC seat is live, and there is no H89 or G252 pane. load1 was 7.41 (06:36, `LC_ALL=C uptime`).
- **Paths:**
  - `.tools/b1022` and `.tools/wt-b1022-base` are absent; `.tools/b1016` exists along with 3 `wt-b1016-*` names (the read-forbidden note in the kit).
  - The helpers `b198/lock.sh`, `b267/waitload.sh`, `b649/jira.py`, `node24/bin/node` and `ms-playwright` all exist.
  - The B1016 evidence holds `results.json`, `review-groups.txt`, `storage.json` and 54 PNGs.
  - The builder STATUS has 165 lines, and its last line begins with the expected READY text (count 1).
- **Launch tools:** `launch_when_cool.sh` exists (4547 bytes; header read with `sed -n 1,30p`, not invoked). `brief_seat.sh:24` is `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`. The charter `QA_AGENT_CHARTER.md` and `cockpit.sh` both exist.
- **Kit checks:**
  - 8 four-underscore lines (52-58 and 66).
  - `@X@` markers: 0.
  - Non-ASCII lines: 0 (control: a planted e-acute reads 1).
  - Name forms: 0.
  - `C-<n>` tokens: 0.
  - Card-id shapes: 0 (control: `hpsmpoc-hosted-runtime-1018` is caught).

## D-decisions (drafter's, in the kit)
- **D-1** The landing tree is the head while main is `77c3132e` (0 behind). The gate builds `comb` only if main moves, and judges it then.
- **D-2** Hosted CI and CodeQL are NOT RUN (no PR). The gate runs every `ci.yml` predicate locally, including the five e2e shards on its own ports, and writes "NO PR; hosted CI and CodeQL NOT RUN" as a Condition. If a PR appears mid-gate, the gate reads its runs LAST, after a bounded wait.
- **D-3** The gate re-runs the builder's 14 plants and part A's p18/p18b/p18h, and adds 15 of its own (g1-g14, g18) plus one equivalent (g19). Cap: 34 runs.
- **D-4** Demo: grade by part A's stamped rule (B953 stamp Q-2). The gate must also make the alias path live with a scored-run Demo caller, because the builder's browser evidence is the no-run state only.
- **D-5** The 404 check gets an HTTP control: one plant build (`p14-full`) showing 200 before the tail. Under load it falls back to the unit rows, marked NOT RUN.
- **D-6** The squash body carries exactly one trailer, `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` (per the commission). The builder's three Sonnet trailers are not carried.
- **D-7** Time: target verdict 180 minutes, hard stop 255, under a load of 7.4 at drafting.

## Q-questions for Tuesday (default first; answer in S3)
- **Q-1 The A2 reading** (an older issued run's approved report is shown while a newer run is in progress). **Default: not a finding.** It follows the B1016 kit's item 5 text ("the newest row ... whose status is `report-issued`"). The gate LISTS it for the product owner as a Note, with the one-line alternative (only the newest run counts).
- **Q-2 The free-text owner shown to every role, Demo included** (builder Open (2)). **Default: a Note, listed for the product owner.** It becomes a Blocker only if the customer RECORD's name reaches the owner line by a code path.
- **Q-3 The type scale.** The B1016 HOLD says "no 9 to 13 px type" while also saying "12 px smallest". **Default: any part-B text under 14 px that part A's landed views do not also render is Minor; the same size as part A is a Note.**
- **Q-4 The p14-full HTTP control.** **Default: YES**, one extra `next build` in the mut tree on port 9276. The alternative is unit rows only.
- **Q-5 The PR title and squash subject may carry `HPSMPOC-388`.** **Default: YES**, as main's subjects do.
- **Q-6 What a NO GO means.** **Default:** the branch parks at round 1 of 2 and Tuesday writes a round-2 fix kit for the builder. A second NO GO on this class goes to the product owner on a card.

## UNMEASURED
- **Not run by the drafter:** no worktree, npm, test, build, browser or Jira read.
- **Claims not verified:** the unit count at either tree; e2e; plants.
- **Code questions not traced:**
  - Whether `reviewedItems` sorts by severity.
  - What `RoadmapScreen` shows for a saved entry with an empty owner.
  - What `factsFor` returns for a held customer that is not the session's.
  - Whether `routeId` and `customer.id` ever differ.
  - What `text-sm` computes to in px.
  - Whether the harness change alters which paths part A's rows exercise.
- **Ticket text:** HPSMPOC-388's acceptance criteria are RELAYED from the B1016 kit line 12 (read there by Jira GET); the gate GETs them itself.

## Outside-the-fences disclosure
- **Read-only:**
  - `gh api -X GET` under the project's `GH_CONFIG_DIR`: main ref, matching-refs, pulls, compare (with patches), commits x3, check-runs, actions runs, repo settings, `ci.yml` contents at the head, the analysis repository's main ref, tree and `CLARIFICATIONS.md`, and main's recent commits.
  - Local reads: DRAFTER_RULES, the B1016 kit and drafter report, the B1016 STATUS, B953, B965 (kit start; STATUS lines 125-140), the B1005 kit, `model-routing.md`, `models_latest.json`, the `brief_seat.sh` header, the `launch_when_cool.sh` header, the local `CLARIFICATIONS.md` by grep, and `playwright.config.ts` by grep (the local checkout may be stale; the kit tells the gate to read it at the head).
  - Listings: the B1016 evidence and `.tools` names.
- **Tools used:** `lsof`, `tmux list-panes`, `uptime`, and a 6-second self-exiting loopback listener on 9279.
- **Not done:** no git verb in the project repo, no `cd` (one Bash call was refused by the hook for containing `cd` and was re-issued without it), no Jira call, no hosted HTTP, no `decision_queue.sh`, no card read, no mail, no Artifact or Docs tool.
- **Not opened:** `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, any WEDNESDAY/FRIDAY tree, `HP Reporting and Docs/`, any SOW, `Source_Documents/`, `inbound/`, or the design file.
- **Writes:**
  - The kit, its `.pre-stamp` copy (`cp -p`, then `cmp`), and this report.
  - Scratch under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2aa17213-e9fb-4717-99d9-8efe0dc321ab/scratchpad/b1022/`: `ci.yml`, `clar.md` and `gatelines.txt`.
  - **One stray write:** a first round-count command redirected its loop output to `/tmp/x_unused`, a file outside the scratchpad. It holds the 129 `GATE VERDICT` first lines (the same text as `gatelines.txt`; no secrets). It was not deleted (never-delete rule); Tuesday may quarantine it.
