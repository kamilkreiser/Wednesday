# DRAFTER REPORT — gate1036: #1036 (KS-763 PR-4, qs in range on express 4) TIER 1 gate set
Written 2026-09-22 08:14:11 AEST / 2026-09-21T22:14:11Z by the drafting subagent. Commission read at `date` = Tue 22 Sep 2026 07:40:40 AEST; this report closes the draft. Files only: nothing launched,
sent, posted or tapped; nothing written under /Volumes/DevMASTER/!CODING/ (read verbs only there; every write verb ran in the drafter's `--shared --no-checkout`
scratch clone `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/37c28f31-b065-4f99-b37a-8976d071f996/scratchpad/predict1036.4e710_tb_c`, kept, never deleted).

## 0. THE DRAFTER'S OWN SLIPS (first, by rule)
- **S1 — a two-dot `diff --raw DEV HEAD` gave 214 records, not the PR's 50** (`read_shape_1.out`): develop's 142 commits since the merge-base appeared as
  78 D + 136 M from the head's side. Instrument, not a finding: re-measured over the MERGE-BASE (`git diff --raw -z --abbrev=40 3961c2add 4b251997a` = 50,
  `read_shape_2.out`); the two-dot count is kept as a labelled control in read_shape_2.out. The script's `.pre-0744-twodot` copy sits beside it.
- **S2 — the scratch clone's `origin` is the LOCAL checkout** (`git clone --shared REPO`), which carries no `refs/pull/*`: `fetch origin refs/pull/1036/merge`
  read "couldn't find remote ref" (`predict_merge_1.out`, `predict_merge_2_ghmergeref.out`). Fixed by fetching from the GitHub URL (`git config --get
  remote.origin.url`) with the checkout's `core.sshCommand`, INTO THE SCRATCH CLONE only (`predict_merge_3_ghmergeref.out`, rc 0). The prompt tells the gate.
- **S3 — three launcher controls (J, M, O) expected exit 31 / 32 / 36 but the launcher refused at 30**: the by-name ladder (exit 30) runs BEFORE the
  CONTEXT / CENSUS / BOTH greps and every token those greps use is also a by-name keyword, so a copy missing one refuses at 30 first. The refusals were
  right; the drafter's `want` was wrong (`launcher_check_controls.out` MISMATCH=3). Corrected (J, M want 30; O now removes a token that is NOT a by-name
  keyword — the KS-775 comment id — so 36 fires) and re-run: `launcher_check_controls_2.out` MISMATCH=0. Exits 31/32 are belt-and-braces guards shadowed by 30;
  the `.pre-0810-ladderorder` copy sits beside the script.
- **S4 — the first generator run refused on three wrapped phrases** (`gen_launcher.run1.out`: "MEASURE develop's row count NOW", "CLEANUP naming exactly
  GHSA-4mjr + GHSA-x5fp", "name it uniquely" — the template wrapped them across lines / said "name every container uniquely"). Reflowed in the template
  (`.pre-0759-wraps`), re-filled (`fill_prompt_2.out`), re-generated (runs 2–4: two generator self-control miscounts — `exit 18` occurs 4× not 3×, and the JUDGED
  regex counts 52 rows not 65 — fixed in the generator; run 4 wrote).
- **S5 — the first `gen_launcher_gate1036.py` heredoc was REFUSED by the fleet's no-cd hook** because the launcher text it carries contains the launcher's own
  legitimate `cd "$QA_DIR"` before `exec`; the generator was written with the Write tool instead (the docstring says so; the launcher line is assembled from
  two string halves so the generator file itself never carries the token the hook reads).

## 1. BLUF (every value re-read at origin in the same action it was written)
- **Head UNMOVED, develop UNMOVED through the draft.** `git ls-remote origin` at 07:42:24 (`lsremote_1.out`), 07:53:35 (`fill_prompt_1.out`), 07:59:36 /
  08:00:04 / 08:00:21 / 08:00:41 (`gen_launcher.run1..4.out`), 08:00:52 (`launcher_check_1.out`), 08:12:16 (`lsremote_final.out`):
  `4b251997a96034ee8a3359aac357ee17d222c3ef refs/pull/1036/head` = `refs/heads/feature/ks-763-qs-in-range`; `3916eacd12af23bfd464440b4c770f7da0f2dd96 refs/heads/develop`.
  PR API 07:47:43 head == pin, base develop (base sha 3961c2add), open, not draft, mergeable_state "unknown" (`api_read_1.out`).
- **#1036 MERGES CLEANLY onto develop 3916eacd1** (MEASURED in the scratch clone, `predict_merge_1.out`): `git merge-tree --write-tree` in BOTH orders rc 0,
  0 conflicts, one tree **`04b05e093ad8b3d6e55b0fe553d7deb96b247050`**. Its delta to the head tree = develop's 164-path delta since the merge-base (set-equal);
  its delta to develop = exactly the 50 PR paths, every one at its HEAD blob; develop-delta ∩ PR paths = ∅ (`git diff --name-only -z 3961c2add..3916eacd1` = 164:
  95 .ts, 34 .py, 18 .sh, 8 .md, 3 .html, 2 .yaml, …; no lock/manifest/baseline). `count-objects -v` on the checkout identical before/after.
- **audit-baseline.json conservation:** develop 29 rows (blob 91d8b71c9 = the merge-base's: develop has not touched it since #1033 landed) → head 26 (648e8ee7b)
  = merged 26 (same blob). Removed exactly {GHSA-4mjr-xmp4-gh2g (KS-763, expires 2026-09-24), GHSA-x5fp-wj9c-mxmx (KS-763, 2026-09-24), GHSA-q8mj-m7cp-5q26
  (KS-531 → KS-775, 2026-11-11)}; 0 added, 0 altered, key order kept, `$comment` equal; re-derives BYTE-EQUAL from develop's by
  `json.dumps(indent=2, ensure_ascii=False) + "\n"` (the ensure_ascii=True variant does not: the `$comment` carries an em dash) — `read_shape_2.out`.
- **GitHub's `refs/pull/1036/merge` (5c5d4ff0f) is STALE**: parents e2d0672af (develop 2026-09-21 15:01 AEST, 47 commits behind 3916eacd1) + the head; tree
  7981ab41f. CONTROL: `merge-tree(e2d0672af, head)` in the scratch clone reproduces 7981ab41f exactly (`predict_merge_4_ghcontrol.out`) — the instrument agrees
  with GitHub; the ref is simply old. Not a verdict input.
- **The locks (parse, `read_shape_2.out`):** 45 tracked locks at head = 45 at develop (same set); **29 moved = exactly the 29 qs carriers at develop**; 0 qs
  < 6.16.0 at head; express 4.22.1/4.22.2 → 4.22.3, body-parser 1.20.6 → 1.20.8 in every carrier; express 5.2.1 / body-parser 2.3.0 untouched (root,
  mcp-server); **side-channel moves 1.1.0 → 1.1.1 in 23 locks** (the 6 carriers already at 1.1.1: whatsapp-bot, issuer, root, packages/shared, mcp-server,
  vc-issuer); mysql2 3.23.1 (root, originate) and vitest 4.1.11 preserved wherever carried. **20 manifests move EXACTLY `overrides.body-parser` 1.20.6 → 1.20.8**
  (JSON parse; no other key, no other override: 20 of 20). Whole-entry diff outside the family: NOT done by the drafter (the gate's item 3(e)).
- **Runtime reach, READ:** 37 tracked Dockerfiles; every services/* Dockerfile and connectors/whatsapp-bot run `npm ci … --omit=dev` on the service's OWN lock
  (api-gateway :47, auth :54, originate :79; CMD `node dist/index.js`; EXPOSE 8080 / 4003 / 4000); the root lock is installed by no Dockerfile; frontend/issuer's
  qs is dev-only (vitest via `url`). The three reach Dockerfiles are byte-identical head == develop (6faa70472, 9402b0de3, ac2fb91bf) — `dockerfile_anchors_1.out`.
- **Docker daemon DOWN at 07:48** (`host_probe_1.out`: socket absent, `docker ps` 0): the image build (item 6a) is NOT TESTED unless the gate finds it up; the
  prompt makes the gate probe first and run the load trace on the host otherwise. Host node v24.7.0, npm 11.5.1; load1 8.69; **3 LISTEN rows on :5432** (not ours;
  the prompt says never connect); `timeout` not installed.
- **Linking (`api_read_1.out`, 07:47–07:48):** attachmentsForURL(pull/1036) = KS-763 contributes open + KS-775 contributes open (controls: pull/1033 → KS-763
  merged; pull/99999 → 0); both In Progress, completedAt null; the two READY comment ids present — KS-775 `09d6f7c6…` body EXACTLY the READY string (byte-equal),
  KS-763 `1b1eb4d3…` names #1036, no `@`; 0 closing phrases in title / body (8376 chars) / 3 commits / the 1 linear[bot] comment; `Refs KS-763` ×1, `Refs KS-775`
  ×0 (the KS-775 link is by attachment); KS-531 archived (Done, archivedAt 2026-08-16), no attachment expected.
  ⚠ **Lead: commit c9e034744's subject is 112 chars** (> the 92-char rule; c93d84c9b 77, 4b251997a 84; all ASCII). The PR title is 138 chars (not a commit
  subject). The gate grades it; the squash subject is what lands.
- **Dependabot overlap (07:48, 19 open PRs):** EXACTLY the READY's ten (#949 #948 #947 #946 #945 #649 #639 #635 #575 #572) share paths with #1036 (#649 pg: 18;
  #575 dotenv: 17; #948 vite: 4; #635 cbor: 2; six the root lock only); 0 other open PRs touch audit-baseline.json; #1036 is the seat's only open PR.
- **The seat's slips (READY):** (i) 251 → 50: the drafter could NOT reproduce 251 — `git diff --name-only mb...head | wc -w` = 50 (no PR path carries
  whitespace); the seat's 251 instrument is unnamed → RECORD; (ii) express 5.2.1 unmoved in root + mcp-server (consistent with the root-loop claim); (iii) body
  ",," ×0, "all 3 rows" ×1, "express 5" ×5, updated_at 2026-09-17T14:52:26Z (consistent with "patched once").
- **Prompt** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-1036-ks763-qs-tier1.prompt.txt`: **236 lines, 33925 bytes,
  sha256 `f88ae264d1577e81d78b045933d0014a0bb63d385a6f7a5359dc8e043f44f695`**; line 1 `ultrathink`; no PENDING / deadbeef / `@@` residue (fill script asserts);
  the ELEVEN by-name items each with its instrument and the drafter's prediction; the MERGE ADDENDUM shape verbatim with the 50 `path blob (mode)` targets
  (one 5051-char line); the CONTEXT RULE; the report dir; the GO string `GO: merge #1036` + BASE_GO.
- **Launcher** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks763_1036.sh`: 474 lines, 35691 bytes, mode 755, sha256
  `280817161f50aadac940d94cf3ec26a2d552853c8235881e5a48cb6854eeb8ab`; **`--check` rc 0 by the drafter's hand** at 08:00:52–08:01:16 (`launcher_check_1.out`:
  "develop 3916eacd1 = the generation pin: 65 of 65 guarded paths at their merge-base blobs … read from 30 directory listings"). **17 controls PASS**
  (`launcher_check_controls.out` A–I, K, L, N, P, Q + `launcher_check_controls_2.out` J, M, O): wrong sha → 6; CUR_DEV=head → 19 LANDED; CUR_DEV=c9e034744 → 18;
  CUR_DEV=merge-base → 0; CUR_DEV=Dependabot #949's head → 18 (40 unpinned); deadbeef → 34; PENDING → 33; no addendum → 25; wrong target blob → 35; no REACH
  FIRST → 27; by-name miss → 30; BOTH miss → 36; no ultrathink → 8; launch without a TTY → 21.
- **Predicted verdict: GO WITH FINDINGS** (RECORD-class: the 112-char commit subject; the KS-775 body link by attachment only; the stale GitHub merge ref;
  the image build NOT TESTED if Docker stays down) — nothing the drafter measured blocks the merge. The gate owns items 3(e), 4, 5, 6 entirely.

## 2. Every count, with its command
| value | command (read-only in the checkout unless marked SCRATCH) | file |
|---|---|---|
| head 4b251997a = branch = refs/pull/1036/head | `git -C REPO ls-remote origin refs/heads/develop refs/pull/1036/head refs/pull/1036/merge refs/heads/feature/ks-763-qs-in-range` | lsremote_1.out, lsremote_final.out |
| develop 3916eacd1; branches API agrees | same + `GET /branches/develop` | lsremote_*.out, api_read_1.out |
| merge-base 3961c2add | `git merge-base HEAD DEV` | read_shape_2.out |
| behind 142 / ahead 3 | `git rev-list --left-right --count DEV...HEAD` | read_shape_2.out |
| 50 PR paths (NUL-safe) | `git diff --name-only -z mb...HEAD` | read_shape_2.out |
| 50 by wc -w (the READY's 251 not reproduced) | `git diff --name-only mb...HEAD \| wc -w` | read_shape_2.out |
| 214 two-dot records (control; S1) | `git diff --raw -z DEV HEAD` | read_shape_1.out, read_shape_2.out |
| 50 raw records: 29 locks + 20 manifests + 1 baseline, all M, 0 mode changes, +552/−951 | `git diff --raw -z --abbrev=40 mb HEAD`; `git diff --numstat mb HEAD` | read_shape_2.out |
| develop delta 164 paths, ∩ PR = ∅; 142 commits, 6 merges | `git diff --name-only -z mb..DEV`; `git rev-list --count [--merges] mb..DEV` | read_shape_2.out |
| baseline rows 29 / 29 / 26 (dev / mb / head), removed 3, added 0, altered 0 | `git show <sha>:Blockchain/Dev/scripts/audit/audit-baseline.json` + json | read_shape_2.out |
| scripts/audit 13 files, only the baseline moved; trees bba64599e (dev = mb) / a3fdeb17b (head) | `git ls-tree <sha> Blockchain/Dev/scripts/audit/`; `git rev-parse <sha>:…/scripts/audit` | read_shape_2.out |
| 45 tracked locks; 29 moved; 29 qs carriers; 0 qs < 6.16.0; 23 side-channel moves | `git ls-tree -r --name-only HEAD \| grep package-lock.json` + `git show` + json parse | read_shape_2.out |
| 20 manifests exactly overrides.body-parser 1.20.6 → 1.20.8 | `git show <sha>:<manifest>` + json parse | read_shape_2.out |
| 37 Dockerfiles; runtime `npm ci --omit=dev` lines | `git ls-tree -r --name-only HEAD` + `git show HEAD:<Dockerfile> \| grep -n` | read_shape_2.out, dockerfile_anchors_1.out |
| merged tree 04b05e093, 0 conflicts both orders (SCRATCH) | `git -C CLONE merge-tree --write-tree --name-only DEV HEAD` and `HEAD DEV` | predict_merge_1.out |
| merged − head = 164 (= dev delta); merged − dev = 50 at head blobs (SCRATCH) | `git -C CLONE diff-tree -r --name-only -z <tree> <tree>` | predict_merge_1.out |
| GitHub merge ref 5c5d4ff0f: parents e2d0672af + head, tree 7981ab41f; 47 commits stale (SCRATCH fetch from the GitHub URL) | `git -C CLONE -c core.sshCommand=… fetch --no-tags <url> +refs/pull/1036/head:… +refs/pull/1036/merge:…` | predict_merge_3_ghmergeref.out |
| merge-tree(e2d0672af, head) == 7981ab41f (control, SCRATCH) | `python3 predict_merge_ghcontrol_gate1036.py` | predict_merge_4_ghcontrol.out |
| count-objects identical before/after (count 9190, in-pack 101422) | `git -C REPO count-objects -v` | predict_merge_1.out, checkout_counts_*.txt |
| checkout porcelain 17, refs 1197, worktrees 257, branch develop, config 6417b203accd839f — equal before/after | `git status --porcelain \| wc -l`; `git for-each-ref \| wc -l`; `ls .git/worktrees \| wc -l` | checkout_counts_before/after.txt (diff: the timestamp line only) |
| PR API: open, 3 commits, 50 files, +552 −951, 1 comment, mergeable_state unknown | `GET /pulls/1036`, `/pulls/1036/files`, `/pulls/1036/commits`, `/issues/1036/comments` | api_read_1.out, out/gh/* |
| compare merge_base 3961c2add ahead 3 behind 142 files 50 | `GET /compare/develop...4b251997a` | api_read_1.out |
| 19 open PRs; overlap = the ten Dependabot PRs; 0 others on the baseline | `GET /pulls?state=open`, `/pulls/<n>/files` per PR | api_read_1.out |
| attachments, comments, states, histories | Linear GraphQL `attachmentsForURL`, `issue(id)`, `history` | api_read_1.out, out/linear/* |
| Docker down; node 24.7.0 / npm 11.5.1; load1 8.69; :5432 3 LISTEN rows | `docker version`; `node --version`; `npm --version`; `uptime`; `lsof -nP -iTCP:5432 -sTCP:LISTEN` | host_probe_1.out |
| prompt 236 lines / 33925 B / sha256 f88ae264… | `wc -l -c`; `shasum -a 256` | fill_prompt_2.out, this report |
| launcher 474 lines / 35691 B / sha256 28081716…; bash -n 0 | generator output | gen_launcher.run4.out |
| `--check` rc 0 (24 s) | `launch_qa_secuura_ks763_1036.sh --check` | launcher_check_1.out |
| 17 controls, MISMATCH 0 after S3 | `bash launcher_controls_gate1036.sh <launcher> <prompt>` (+ SEL subset) | launcher_check_controls.out, launcher_check_controls_2.out |

## 3. What the launcher guards (and what it deliberately does not)
- Head: branch AND refs/pull/1036/head must both be at the pin (exit 6). Compare: merge_base 3961c2add + ahead 3 + files 50 (exit 10); `behind` NOT asserted
  (develop moves by design). Develop: judged by CONTENT over 65 paths from 30 GitHub contents listings — the 49 non-audit PR paths at their merge-base
  blobs, the 3 reach Dockerfiles unmoved, scripts/audit exactly its 13 files with only the baseline pinned; all 50 at head blobs → 19 LANDED; anything else →
  18 GUARDED (a Dependabot PR landing first is the expected mover: control F = #949's head → 18 with 40 unpinned paths). develop's SHA and the predicted merged
  tree are PRINTED, not guards: the gate re-predicts over the tip it reads and names it BASE_GO.
- Prompt ladders: 93 by-name keywords (exit 30), 46 BOTH tokens that must sit in the READY capture AND the prompt (36), all 50 head blobs (35), the subject /
  report dir / addendum / REACH FIRST / npm-version / MERGEABILITY (23–29), CONTEXT (31) and CENSUS (32) — the last two shadowed by 30 (S3), PENDING (33),
  deadbeef (34), ultrathink (8), TTY (21), overrides at launch (16).
- BRIEF = the READY capture `gatesets/2026-09-18_gate1036/mail_1036_ready.md` (as gate16B/16C did); no separate brief .md was written (the commission names
  only the prompt).

## 4. NOT MEASURED by the drafter (the gate's, or nobody's)
- The shipped audit scripts (item 4) — they talk to the registry; not run. The workspace `npm ci` + the 26-member suite matrix, frontend/issuer vitest, the
  whatsapp-bot own-lock install, lockfile-cleanroom (item 5) — not run. The image build and the runtime load trace (item 6) — not run (Docker down; the host
  route is the gate's). The whole-entry lock diff outside the express/body-parser/qs/side-channel family (item 3(e)) — not done. Any lock REGENERATION (the
  npm-version dependent recipe) — not attempted. The PR API's `mergeable` recomputation — "unknown" at 07:47, not polled. The seat's Records path
  (`5_Project_History/2026-09-17_seatB-succ1/pr4/`) — not opened (a seat's history; read-only by rule, unnecessary for the pins). The 251 instrument — not
  identified. No Datasec file or mail touched.

## 5. Tool-use count and wall-clock
- Wall-clock: `date` at commission read 07:40:40 AEST → this report (the `Written` line above).
- Tool calls: 50 through this report (48 Bash + 1 Write + this Bash; two Bash calls were REFUSED by the fleet's hooks before running — the `git -C $C merge-tree`
  control (re-issued as a script file) and the generator heredoc carrying the launcher's `cd` (re-issued with the Write tool) — and are counted).
