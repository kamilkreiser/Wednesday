LAUNCH BRIEF (Seat D 1st): KS-1379 + KS-1380 one-direction design, measure both, recommend

# LAUNCH BRIEF: Seat D 1st, Secuura/Blockchain, DESIGN LANE. Measure both lock directions for KS-1379 and KS-1380, recommend one, build and push nothing. From Wednesday

## BLUF
You are **Seat D 1st**, a **DESIGN-ONLY** seat. **Kam delegated the local-build question to Wednesday at 14:18:29 AEST** (verbatim below: Stuart's KS-1395 message, plus "KS-1379 and KS-1380 are probably one fix ... ask Kam to pick one direction"). **Wednesday will pick the direction from YOUR measurement** and tell Kam. Your job is to **measure BOTH directions, then recommend ONE**, with the one-PR shape it implies.
- **Direction A (KS-1379's fix-shape):** regenerate each standalone lock that #1339 re-resolved **from its committed pre-#1339 lock**, carrying only the targeted bumps. Hypothesis (UNMEASURED): this puts `packages/shared` back on `@types/express-serve-static-core` 4.19.8 / `@types/pg` 8.20.0 and fixes KS-1380 as a side effect.
- **Direction B (KS-1380's suggestion):** move the lagging locks' `@types` forward to agree with `packages/shared` (4.19.9 / 8.23.1). This leaves KS-1379's drift in place.
- **Also resolve:** are KS-1395's two advisories (undici `GHSA-r53p-7pc4-xj5r`, js-yaml `GHSA-r3ph-w7gj-g6xm`) still REPORTED at develop? State the leg output. **You draft NO comment.**

**This round you create no branch, no push, no PR, no ticket comment or state change, and no deploy.** Building a fix is a later round, on Wednesday's ruling.
**Budget:** Wednesday reads `ctx:NN%` off your pane on every STATUS. **Your hard line is 75% by her reading.** Send a STATUS at each measurement set. At 75%, finish the step you are on and hand over the rest as UNMEASURED. **You cannot read your own statusline, and the `<total_tokens>` counter is not your context window.**
**Necessity clause (cloud):** a local model cannot run docker image builds, regenerate locks in containers or measure a two-direction design across 28 locks.

**Bases (both read with `ls-remote`, 2026-09-30 14:20:41 AEST):**
- develop `3e3a68260d0ef541b2410d323849d2639ddd6941`.
- **PRIMARY base: #1356's head `52dadb07f70d20da8f201b518eba4ebff05c8455`.** #1356 is open, Seat B 49th's in-range refresh of six advisories across 18 locks, in gate49a. It merges first, and your fix lands on top of it.
- Both objects are already in the shared checkout (`cat-file -t` = commit). **You need NO fetch.**
- #1339's squash is `2cb858335472fafcce535ca4ad328c897ed87bfb`. **Its parent `8af6ab8216007462e596daed6b0adcd1e87e34ee` holds the committed pre-#1339 locks.**

**The drafter's lock census, from `git show <sha>:<lock>` + JSON parse at 14:21. It is your expectation, NOT your input: re-measure it.**
| SHA | `packages/shared` esc / pg | locks carrying either `@types` at top level | locks that disagree with shared | `@types/pg` versions in play |
|---|---|---|---|---|
| `8af6ab821600` (pre-#1339) | 4.19.8 / 8.20.0 | 28 | **2** (`services/mcp-server` esc 4.19.9; `services/vc-issuer` esc 4.19.9, pg 8.21.0) | 8.20.0 ×22, 8.21.0 ×1 |
| `d9ce1403d158` (KS-1380's "last good build") | 4.19.8 / 8.20.0 | 28 | **2** (the same two) | same |
| `3e3a68260d0e` (develop) | 4.19.9 / 8.23.1 | 28 | **15** | 8.20.0 ×12, 8.23.1 ×10, 8.21.0 ×1 |
| `52dadb07f70d` (#1356 head) | 4.19.9 / 8.23.1 | 28 | **15**, set-identical to develop's | same as develop |

The 15 at develop and #1356's head:
- the workspace root;
- `connectors/whatsapp-bot`;
- `services/`: analytics, billing, governance, kyc, nft-certificate, referral, shared, staking, tenant-provisioning, tokenisation, transfer, vc-issuer, wallet-connector.

**Two things follow, and both are for the design:**
1. **KS-1380 says "every lock agreed" at `d9ce1403d`. That is not true of the top-level entries:** mcp-server and vc-issuer disagreed there and still built. **A disagreement alone does not fail a build.** What fails is an exported type that is inferred across the `/shared` boundary (TS2742), or a type passed across it (TS2345). The failing set is therefore a measurement, not something the census can tell you.
2. 🔴 **Direction A can reintroduce #1356's advisories.** The drafter compared the pre-#1339 locks with #1356's head:
   - vulnerable versions: `frontend/issuer` brace-expansion 5.0.9, `services/anchoring` brace-expansion 2.1.4 + fast-uri 3.1.7, `services/api-gateway` brace-expansion 5.0.9, `services/originate` brace-expansion 1.1.18 / 5.0.9 + fast-uri 3.1.7;
   - #1356's head has the patched 5.0.12 / 2.1.7 / 1.1.21 / 3.1.8;
   - **#1356 touches NONE of #1339's 13 standalone locks.** These four are clean today only because #1339's fresh re-resolution happened to pull patched versions.

   A lock regenerated from its pre-#1339 lock must re-carry **#1339's targets, #1355's undici override (issuer) and #1356's refresh targets**. Otherwise legs 6/7 go red. Across the 13 locks, **1,288 entries differ in version** between `8af6ab821600` and `52dadb07f70d`. KS-1379 says "~1,000", measured on #1339 alone.

**Seat identity**
- **Pane:** the cockpit row **`Secuura/Blockchain-B`**. Wednesday reads your ctx off it. Your tmux pane id is UNMEASURED: say it in ITEM 0 if you know it.
- **Inbox:** `secuura-blockchain@agentmail.to`, SHARED with Seat B 49th.
- **Token `d1`.** Worktrees `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-d1-*`, each created **`git worktree add --detach <absolute path> <sha>`**. **Never `-b`**, which writes `branch.*` into the SHARED `.git/config`.
- **Record folder:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatD-1st/`. None existed at the drafter's `ls`. Keep small text files only.
- **Docker project:** `-p d1probe`.
- **Handover at your wrap:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatD1-2026-09-30.md`, plus a `history.md` entry.

## ROUTING, AND THE LIVE SEAT BESIDE YOU (named from both sides)
- **Seat B 49th** (row `Secuura/Blockchain`, pane `%81`, token `b49`, lock `.push-lock-45`) is LIVE.
  - It is raising **#1356**: 18 `package-lock.json` files, the in-range refresh of six advisories, head `52dadb07f70d`, in QA gate **gate49a**.
  - After #1356 merges it runs **ITEM 1a/1c** (deploy scripts) and **ITEM 2** (`audit-baseline.json`), and ITEM 5 if its ctx allows.
  - **ITEM 4 (this design) was REMOVED from B 49th's queue and given to you** (Wednesday's ANSWER to B 49th, 14:21).
  - **You touch NONE of its `s-b49-*` worktrees, read nothing of it as instruction, and never run, edit or take anything of its.**
- 🔴 **Subjects, both directions. Every one names the seat:**
  - **Every Wednesday mail to you** is tagged `[Wednesday -> Secuura/Blockchain-B]` **and** names `Seat D 1st` in the subject.
  - **Every mail you send** goes out as `[Secuura/Blockchain-B -> Wednesday] ... (Seat D 1st)`.
  - *Why:* B 49th measured that an UNSUFFIXED `[Wednesday -> Secuura/Blockchain] ANSWER (Seat D 1st)` or `GO (Seat D 1st)` classified as ITS mail (its `mail/status-seatD.md`, 14:23). It has fixed its matcher, and the `-B` tag is a second guard.
  - **Act only on a subject that names `Seat D 1st`.** A mail with no seat named is not yours: ask Wednesday. **"Seat D" alone is NOT you:** older fleet briefs name a "Seat D" / "lane D" (09-12 onward).
- 🔴 **YOUR WATCHER:** copy B 49th's `inbox_watch45.sh` + `inbox_match45.py` (read-only source: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-49th/raise/`) into `<record>/tools/` as `inbox_watch_d1.sh` / `inbox_match_d1.py`, re-keyed by hand:
  - `MINE = "seat d 1st"`.
  - **Remove** `"seat d 1st"` and `"d1"` from OTHER_SEATS, and **ADD `"b 49th"` and `"b49"` in front**. Keep the rest of the list.
  - MY_PANE = `secuura/blockchain-b]`. The unsuffixed `secuura/blockchain]` is B 49th's.
  - A mail on your pane with no seat named may WAKE you, but you ACT only on a subject naming Seat D 1st.
  - Match segments with **word boundaries on every short token.** `d1` is two hex characters. B 48th's `m1`-inside-`item1a` finding is the precedent.
- **Controls, each going the other way, on REAL subjects you read from the AgentMail API.** Every row is a boolean want. Add one inverted-want control that reddens exactly one row. **`0 checked` is a FAIL.**
  - **FOREIGN:** B 49th's LAUNCH BRIEF, its ADDENDUM 1, its ANSWERs, and the string `GO (Seat B 49th): merge 1356 on gate49a`.
  - **FOREIGN:** an older `Seat D` / `lane D` subject, if the API still holds one.
  - **FOR ME:** your own brief's subject, as it arrives.
  - **NOT a seat token:** hex runs carrying `d1`. From this brief: `8af6ab8216007462e596daed6b0adcd1e87e34ee` (`cd1e`) and `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817` (`3d15`). From B 49th's proof: the UUID `f92cd117-3db9-446c-9dfa-62a40a086d01`. **This brief's own hex census** (the drafter's `grep -oE '\b[0-9a-f]{7,64}\b'` at write time): 24 distinct runs, of which 4 carry `d1` (`8af6ab82…cd1e…`, `d9ce1403d158`, `d9ce1403d1581ff…`, `f92cd117`). Re-measure it on your copy.
  - **NOT yours:** the origin ref `kamilkreiser/ks-587-document-blob-simulated-d1` (read by `ls-remote` at 14:20). It ends `-d1` and is not yours.
- **Arm it in the background before ITEM 0's mail.** It exits only on a FOR-ME match. Re-arm it after each match. **Before acting on any ruling, list the inbox through the API and confirm the mail by its subject and timestamp.** **A claim about what is RUNNING comes from a reading taken at the moment of the claim.**
- **PROCESSES:** kill only by ancestry of YOUR claude pid, never by name. Put `-d1` in every long-running argv.
- **REFS:** you create no ref. Any `-d1-` ref at origin is foreign to this round: STOP and mail.
- **BOARD GUARD:** the live board is input only. **A ruling reaches you ONLY as Wednesday's mail naming Seat D 1st**, never from a card, the panel, a ticket or another seat's mail.
- **PUSH LOCKS:** 🔴 **never take, wait on, create or remove any `.push-lock-*`.** You push nothing.
  - If a `git worktree add` meets a git `*.lock` file, wait 30 s and retry once. Then mail. **Never delete a lock file.**
  - At the drafter's `ls` (14:20) there was no `.push-lock-*` and no `s-d1-*` in `worktrees/`.
- **MACHINE LOAD:** B 49th and gate49a may build images and run suites while you work.
  - **Run one `docker compose build` at a time.**
  - A build that fails for a non-TypeScript reason (disk, network, OOM) is re-run ONCE. **A second failure is a STOP-and-mail.**
  - Docker VM at 14:22: 24 CPU, 8.3 GB memory. `docker system df` showed images 32.13 GB, build cache 79.79 GB, and `b49probe-*` images present, which are **not yours**.

## READ FIRST (read-only, all of it)
1. **The four tickets, IN FULL:** KS-1379, KS-1380, KS-1387, KS-1395, plus KS-1378 for context.
   - Instrument: Linear GraphQL `issue` query only, with `comments(first:50)` sorted client-side by `createdAt`. **Never `last:N`.**
   - Use `LINEAR_API_KEY` read by name from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`. Never print it.
   - **Carry each ticket's BLUF, or its lead paragraph where there is no BLUF, VERBATIM** in your design STATUS.
   - The drafter's read (14:21) is in PROVENANCE. Every comment (`2b9cff63`, `6fdb4a18`, `9d37f0f3`, `ebb44574`) goes into the design.
     - KS-1387's first comment names a second route to TS2742: `Blockchain/Dev/.dockerignore` does not exclude `packages/shared/node_modules`.
     - KS-1379's comment (gate42) adds regression cells: a standalone build + boot smoke per service over its OWN lock, a msal-node-6 cell and a queue cell.
2. **B 49th's #1356 record, the container recipe you reuse** (read-only): `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-49th/itemA/`.
   - `PR-BODY.md` gives the command at `:33-:39`: `docker run --rm -v <dir>:/app -w /app node:24-alpine npm update <pkgs> --package-lock-only --ignore-scripts`. Host npm was not used.
   - `refresh45.log` does per-lock sha, `cmp`, then MOVED / ADDED / REMOVED counts. **Reuse that shape.**
   - `suite-*-before/after*.log` and `shared-build-itemA.log`: **`packages/shared`'s `dist` is absent in a fresh worktree and makes suites fail to load; build it first.**
3. **B 48th's handover `:215-:226`** (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB48-2026-09-30.md`): the carried KS-1380 design and finding 3. Its findings that bind you:
   - 🔴 **`up to date` is not evidence nothing moved.** Use `cmp` rc and sha256.
   - 🔴 **A root-manifest `overrides` entry is inert under `npm install --package-lock-only`.** `npm update <pkg> --package-lock-only --ignore-scripts` re-resolves it.
   - 🔴 **A root-lock regen with a MANIFEST change moved 12 unrelated entries** (eleven `lightningcss-<platform>` + `magicast`). B 49th scoped this at 13:57: **with no manifest change the pristine control moved nothing.**
   - 🔴 **A substring matcher read a passing test's name as a verdict.** The rc on its own line is the instrument. **Never grep leg logs for `FAIL`.**
4. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` (356 lines, mtime 2026-09-30 07:01:49). The lines that apply to you:
   - `:217-:219`: rc through a pipe. In the Bash tool's zsh `${PIPESTATUS[0]}` is EMPTY. Write `cmd > log 2>&1; rc=$?`.
   - `:249`: duplicates between tickets are Wednesday's word. KS-1380 and KS-1387 are client humans' tickets.
   - `:338-:341`: never end a turn on a "next up" line with nothing running.
   - `:343-:344`: read repo files from a SHA.
   - `:346-:347`: `cmp`, not patch-id.
   - `:352-:353`: the client-comment hold.

## QUEUE
0. **ITEM 0, the plan confirmation to Wednesday.** Push, build and regenerate nothing before her ANSWER. Include:
   - the boot-pull refusal proof (HOLDS);
   - every launcher preflight warning, VERBATIM;
   - the watcher's pid, READ at the moment you write it, and its controls' result;
   - your worktree plan;
   - `docker info` / `docker system df` / `df -m /Volumes/DevMASTER`;
   - the four tickets' comment counts as you read them;
   - your re-measure of the census table;
   - OPEN QUESTIONS, if any.

   **Ask Wednesday to read your ctx.**
1. **KS-1380 reproduced, at BOTH bases.** Worktree `s-d1-base` at `52dadb07f70d` (primary) and `s-d1-dev` at `3e3a68260d0e`.
   - **Run no `npm install` on the host in either worktree.** An untracked `packages/shared/node_modules` enters the build context, because `.dockerignore` does not exclude it (KS-1387). Prove none exists before building (`ls` rc).
   - `docker compose -p d1probe -f <wt>/Blockchain/Dev/docker-compose.yml build <svc>`, **one service at a time**, over every service with a `build:` (33 `build:` entries at develop by the drafter's count; re-count). **Minimum:** analytics, billing, governance, the eight latent ones KS-1380 names, mcp-server and vc-issuer.
   - Per service: rc, and the **first error line** verbatim.
   - **Build only:** never `up`, `down`, `run` of a service, `--rmi`, `prune` or `rm`.
   - `docker system df` before and after each set. **If Docker's disk fills, STOP and mail. Prune nothing.**
   - **STATUS `status d1 repro (Seat D 1st)`.**
2. **Direction A: KS-1379's fix-shape, measured.** Worktree `s-d1-a` at `52dadb07f70d`, with pristine control `s-d1-actl` at the same SHA.
   - Take the **13 standalone locks #1339 re-resolved**: `frontend/issuer`, `packages/shared`, and `services/` anchoring, api-gateway, auth, demo-service, guardian, m365-integration, originate, prism, queue, security, timestamping (drafter's `git diff --numstat 2cb858335^ 2cb858335`; re-derive it). For each lock:
     1. **Restore its bytes from `8af6ab821600`**, `cmp` against `git show`.
     2. Leave its **manifest** as at the base.
     3. **Derive the targets from the diffs, never from memory:** #1339's manifest diff for that path; #1355's for issuer; #1356's refreshed packages from its per-lock diff.
     4. Run `npm install <pkg>@<ver> --package-lock-only --ignore-scripts` of **only** those targets. Use `npm update <pkg>` where the target is a transitive refresh.
   - **Container:** `node:24-alpine`, npm 11.19.0, printed in the same run. **Never host npm 11.5.1.** Mount the repo ROOT for any lock that links `file:../../observability`. **Never mount at `/dev`.**
   - **Per lock:** pre/post sha256, `cmp` rc, entries MOVED / ADDED / REMOVED against the base lock (parsed), and the `@types` pair. **Never the `up to date` banner or the rc.**
   - **Then:**
     - which images build (item 1's set);
     - legs 6 / 7 / `audit:contract` rc, each on its own line. 🔴 **List every advisory id #1339, #1355 and #1356 cleared, each shown NOT reported.** A regression here makes A inadmissible as run: say so, with the id;
     - the runtime movers KS-1379 names (`services/queue` bullmq / msgpackr; `services/m365-integration` + `packages/shared` `@azure/identity` / `@azure/msal-node`): base version → A's;
     - the control's moves, set-compared, before you attribute anything.
   - **The root lock is not in A's set** (KS-1379: it moved 0 non-target versions). It disagrees with shared at both bases. Say what A leaves it at, and whether that matters for the suites, which run from the root lock.
   - **STATUS `status d1 directionA (Seat D 1st)`.**
3. **Direction B: KS-1380's suggestion, measured.** Worktree `s-d1-b` at `52dadb07f70d`, control `s-d1-bctl`.
   - Move the **15** disagreeing locks forward to `packages/shared`'s `@types/express-serve-static-core` 4.19.9 / `@types/pg` 8.23.1, with the same container, the same per-lock numbers and the same control.
   - Say which command did it (`npm update`, or `npm install <pkg>@<ver>` as a direct dev dependency; **the latter is a MANIFEST change: name it**). Say what else each move dragged: `@types/pg` 8.23.1's own dependencies, counted.
   - Then the images, the legs and contract, and the advisory list, as in A.
   - **State plainly what B leaves undone: KS-1379's ~1,000-entry drift and its runtime majors stay.**
   - **STATUS `status d1 directionB (Seat D 1st)`.**
4. **Controls:** a pristine control worktree **beside every lock regen**: same SHA, same container, same commands, no target. Report the moved-entry sets of the change and of the control, and their difference. **Attribute nothing the control also moves.**
5. **Suites, before and after each direction,** for every service whose image failed at the base, plus `packages/shared`.
   - Build `packages/shared` first in each suite tree.
   - Run each suite the way B 49th's itemA logs did, and name the runner.
   - Give counts (files / tests / failed) at base, A and B. **Any red that is not red at base is a finding, named.**
   - **Keep suite trees separate from image-build trees** (the `.dockerignore` route above), or prove `packages/shared/node_modules` is absent before every build.
6. **KS-1395's two advisories, the fact for Stuart.** In `s-d1-dev` (develop `3e3a68260d0e`) and `s-d1-base` (#1356 head): `npm run audit:gate` and `npm run audit:locks` from `Blockchain/Dev`, rc on its own line, with the NEW / CLEANUP blocks VERBATIM.
   - **Are `GHSA-r53p-7pc4-xj5r` and `GHSA-r3ph-w7gj-g6xm` REPORTED as new?**
   - Expected NO, from the drafter's reads of both SHAs at 14:21:
     - r53p is a baseline row (#1354, Kam's (c));
     - r3ph is in no row, because the lock no longer pins the vulnerable version: `systemTest/performance` js-yaml 5.4.2;
     - issuer and root undici 7.30.0.
   - ⚠ **B 49th measured legs 6/7 rc 1 at develop on SIX NEWER advisories** (the ones #1356 fixes; its plan mail 03:45Z, per Wednesday's ANSWER). So "KS-1395's two are cleared" and "pushes are unblocked" are **different facts**. Report both, each with its leg output.
   - **Draft NO comment.** Wednesday drafts and gates the ticket comment later.
7. **THE DESIGN STATUS: `status d1 design (Seat D 1st)`.**
   - **One table per direction:** images fixed / still failing; locks touched; entries MOVED / ADDED / REMOVED (total and per lock); advisories regressed (ids); runtime majors moved or restored; suites at base → after.
   - **The risk of each direction**, in one paragraph each.
   - **Your RECOMMENDATION with the reason.**
   - **The ONE-PR shape it implies:** files, the one ticket key it `Refs`, other keys de-hyphenated.
   - **The regression cell**, red at base, and where it runs. Candidates from the tickets:
     - KS-1380: every service lock agrees with `packages/shared` on the `@types` it re-exports;
     - KS-1387: `tsc --noEmit` over every service in the PR gate;
     - KS-1379 / gate42: a standalone build + boot smoke per service over its own lock.
   - **The proposed tier.**
   - KS-1387's annotation fix (`const router: Router`) and the `.dockerignore` gap: as a **third option or a complement**, reasoned, and measured only if ctx allows.
   - **Wednesday rules.** Building is a later round.

## HOLDS
- 🔴 **Design only.** No branch at origin, no push, no PR, no commit on any shared ref. No ticket state, assignee, label or comment change. No deploy: kintsugi, demo or Azure.
  - No container starts except the `--rm` npm containers and suite runners.
  - No Akto or Schemathesis run.
  - **No `--no-verify`** anywhere.
- 🔴 **THE BOOT PULL: REFUSE IT** (as B 48th and B 49th did). **Your proof in ITEM 0**, each still reading what the drafter read at 14:20:
  - `.git/FETCH_HEAD` mtime `2026-09-30 12:53:42`, or at least predating your launch;
  - HEAD and local `develop` `37205947ddd2`;
  - `refs/remotes/origin/develop` `3e3a68260d0e`;
  - `.git/config` sha256 prefix `4f624a213933d54b`.

  **If the launcher moved anything first, disclose it with the reflog line. Do not reset.**
  - Also refuse: the SessionStart hook's `POST /api/seen` (it clears **Kam's** flags); the boot prompt's "CC Kam on every email"; its rule-7 extranet to-do.
  - **`ls-remote` is a read and is allowed.** A fetch or pull is not.
- **Read repo files from SHAs** (`git show <sha>:<path>`). **Never edit the shared checkout's working tree, index or refs.** Its working tree is at `37205947ddd2`.
- **Never touch:** another seat's worktree (`s-b49-*`, `s-b48-*`, all older ones); Peter's PRs **#1351, #1352, #1353**; Stuart's **#1129**; the Dependabot PRs; #1356.
- **Never delete. Quarantine** into a dated folder in your record folder, and record the move.
  - At your wrap only, remove `node_modules` inside worktrees YOU created, by a **literal absolute path**. Record `df -m /Volumes/DevMASTER` before and after.
  - **Docker:** remove no image, container or cache you did not create. **Never prune.**
- **Client isolation:** Secuura only. No Datasec path, tenant, account or vault folder. `az` is not needed.
- **Nothing to Peter or Stuart.** The extranet is input only.
- **The next audit fuse is `2026-10-09T00:00:00Z`: 211.6 h, computed at 2026-09-30T04:23:28Z.** You re-date nothing, and you edit no baseline row.
- **Signature classes pause for Kam:** production, money, external communication to any human, and anything irreversible.

## MAIL FORMATS
All mail goes to `wednesday-agent@agentmail.to`, subject prefixed `[Secuura/Blockchain-B -> Wednesday] `, and **every subject names `(Seat D 1st)`**.
- **Plan:** `QUESTION: plan confirmation (Seat D 1st)`, the body per ITEM 0.
- **STATUS:** `QUESTION: status d1 <set> (Seat D 1st)`. One line of state, then the measurement, then **"Please read my ctx."** Wednesday answers `continue` or `hand over`, with the ctx she read.
- **Design:** `QUESTION: status d1 design (Seat D 1st)`, as in QUEUE item 7.
- **WRAP:** `WRAP (Seat D 1st): design lane COLD. ...`, which carries:
  - "Cold. Nothing is running.", or what IS running, READ at the moment you write it;
  - the handover path with its sha256 prefix and `wc -c`;
  - the history entry;
  - the UNMEASURED list;
  - `df -m` and `docker system df` before and after;
  - mail counts COUNTED from the record.

## UNMEASURED (not provenance)
- your ctx and your pane id;
- whether the launcher's boot pull moved the shared checkout;
- **the failing image set at either base** (the tickets report analytics, billing and governance at `0aa9b52c6` / `8c810023f`; nobody has built at `3e3a68260d0e` or `52dadb07f70d`);
- whether #1356's refresh of the analytics / billing / governance locks (3/3 lines each) changes their build;
- **everything about Direction A and Direction B:** the moves, images, legs, suites and runtime movers;
- whether `npm update` of a transitive `@types` package moves it under npm 11.19.0;
- legs 6/7 output at either base as YOU run them, including KS-1395's two ids;
- whether the root lock's `@types` disagreement affects any suite;
- whether gate49a's GO or #1356's merge happens during your session. If develop moves, **re-pin nothing on your own: say so in a STATUS**;
- Docker's free space at your boot.

RULED BY KAM, NOT YET IN AN ARTEFACT
**Kam's instruction on the live board, 2026-09-30 14:18:29 AEST, view=wednesday.** Instrument: `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh`, rc 0, read 14:24:36, 2 messages today, 0 withheld. Quoted VERBATIM:
> please have a look at the following message from stuart. Do everything you can to resolve and once tested and deployed let me know - Good morning @⁨Kam⁩ I have/has some issues with the local build. Could you have a look at KS-1395, its related to KS-1378 as it blocks every push (its related to two new advisories). It's in the Dependency and Version Currency project, where KS-763 lives. It records both advisories, what pulls each one in, how to reproduce, and what "done" means. It's linked to KS-1378, KS-729 and KS-1379. Note: KS-559 and KS-470 are archived. Something to consider, said Claude, is that KS-1379 and KS-1380 are probably one fix. The @types version change that breaks the three services is one of the ~1,000 unrelated version changes KS-1379 describes. PR Secuura/Distributed_Secuura#1339 wasn't trying to change those packages. KS-1379's proposed fix regenerates each lockfile from its committed version. That would likely put packages/shared back on the older @types, which fixes KS-1380 as a side effect. The alternative is to move the 11 lagging services forward, which is KS-1380's suggestion. If both tickets are worked separately, they could pull in opposite directions. So ask Kam to pick one direction and have them done together. Heading back to Taiwan today so will be in a more reasonable timezone to have a catchup 🙂

→ **Must land in:** Wednesday's direction ruling (made on your design), then ONE PR in a later round, then Wednesday's report to Kam once it is "tested and deployed". **"Deployed" is NOT this seat's**: it is a signature class and a later round's.

**Context rulings, delivered, not yours to act on:**
- `secuura-five-new-advisories-block-every-push-0929` ⇒ **a** (bump), delivered as #1339. This is the direction #1339 and #1356 follow.
- `secuura-undici-ghsa-r53p-exception-1354` ⇒ **c** ("Accept permanently, like the twelve siblings | note: And fix now"), delivered as #1354 + #1355 (12:55:28).

**Undelivered secuura- cards.** Read with `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-`, rc 0, **37 cards**, 14:21:46; the same 37 ids as B 49th's brief. **None of them touches this design, so do not act on them:**
- secuura-agent-github-identity, secuura-dependabot-triage, secuura-ks229-disclosure-mailbox, secuura-ps-759-760-merge-owner;
- secuura-demo-kam-admin-default-password, secuura-f5-login-limiter-bypass, secuura-f5-demo-exposure-probe, secuura-f5-demo-interim-mitigation, secuura-demo-admin-transcripts, secuura-demo-admin-mfa;
- secuura-891-workflow-scope-merge, secuura-force-push-own-branch-standing, secuura-org-trust-boundary-within-tenant, secuura-archive-fifteen-platform-s-tickets;
- secuura-advisory-gate-moving-set, secuura-advisories-high-and-prod-reaching, secuura-four-advisories-ruled-after-measurement, secuura-required-approvals-zero-after-the-untick;
- secuura-ks1011-stack-marker-unknown-on-restore, secuura-ks1081-two-env-templates-which-is-canonical, secuura-ks1168-ilike-search-on-encrypted-pii, secuura-ks1194-1032-round2-merge-tap, secuura-ks1245-smoke-test-degraded-semantics, secuura-ks1019-blockchain-block-untyped;
- secuura-ks1084-gateway-originate-no-tenant-header-p0, secuura-ks1304-withtenant-tenant-pool-and-admin-writes, secuura-pr1245-ks1313-at-the-cap-disposition, secuura-allowance-89-before-the-0930-freeze;
- secuura-ks1346-logging-thrown-objects-leaks-secrets, secuura-ks1348-log-files-persist-secrets, secuura-ks888-failed-key-save-design, secuura-ks1348-r2-files-still-leak-allowlist, secuura-ks888-revoke-validate-on-failed-save;
- secuura-ks1054-f9282-migration-failure-visibility, secuura-ks1124-f4-failed-anchor-shows-pending, secuura-ks1352-revoked-credentials-still-verify, secuura-ks888-validate-usage-write-failure.

**Of these, context only:**
- `secuura-four-advisories-ruled-after-measurement` ⇒ bump;
- `secuura-advisory-gate-moving-set` ⇒ both: the 2026-09-09 grant is Wednesday's, and it covers adding a baseline entry only.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **This round is DESIGN ONLY. Wednesday approves the design before any build** (B 49th's brief, ITEM 4; carried to you by the ANSWER of 14:21).
- **The budget instrument:** Wednesday reads `ctx:NN%` off the pane on each STATUS. **Hard line 75%.** Do not start a step that does not fit under 75%: hand it over.
- **`ls-remote` at boot is acceptable. What stays refused is the pull and the fetch** (ANSWER plan to B 48th, 10:03).
- **Parallel measurement image builds are approved exactly as bounded:** detached worktree, `-p <yours>probe`, build only; never up/down/--rmi/prune; stop and mail if Docker's disk fills (ANSWER plan to B 47th, 06:26).
- **Finding-3 scoping, accepted as B 49th's measurement at `3e3a68260d0e`:** a lock refresh with no manifest change moved nothing in the pristine control; B 48th's 12-entry drift came from a changed manifest (ANSWER to B 49th, 13:57).
- **The container route is the instrument:** `node:24-alpine`, npm 11.19.0; host npm not used (ANSWER to B 49th, 13:57; KS-1379's "blocked on" section).
- **An acceptance of a production-reaching advisory is Kam's**, never a seat's or a design's (ANSWER plan to B 49th, 13:46). A direction that clears only by a baseline row is a card, not a recommendation.
- **KS-1395: do NOT comment. Wednesday will have the answer drafted and gated in a later round** (ANSWER to B 49th, 14:21).
- **Post NO ticket comments without a drafted, gated text** (GO gate48b, 12:41; STANDING_LINES `:352-:353`).
- **Duplicate handling between KS-1380 and KS-1387 is Wednesday's word on your evidence.** Both are client humans' tickets.
- **A hyphenated foreign key in a PR title, body, branch or commit ATTACHES that ticket.** Your proposed PR shape de-hyphenates every key but its own.
- **The 2026-09-09 grant is WEDNESDAY'S: the seat MEASURES and reports; Wednesday decides** (ANSWER leg7 to B 47th, 07:18).
- **PR #1351, #1352, #1353 are Peter's: do not touch them, comment on them or wait on them** (gate47 GO).
- **Merged is not deployed.** KS-1379's condition stands: no deploy carries #1339's runtime moves until KS-1379 is done or Kam says otherwise.

VERIFIED BEFORE SENDING (Wednesday's drafter, 2026-09-30)
PROVENANCE:
- develop 3e3a68260d0ef541b2410d323849d2639ddd6941; refs/pull/1356/head and feature/ks-1378-in-range-lock-refresh-six-advisories-b49-a both 52dadb07f70d20da8f201b518eba4ebff05c8455; refs/pull/1339/head fa93ff88f47e; origin ref kamilkreiser/ks-587-document-blob-simulated-d1 exists; no -d1- ref | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop refs/pull/1356/head refs/pull/1339/head refs/pull/1355/head 'refs/heads/*b49*' 'refs/heads/*d1*'` rc 0 (a read, nothing written) | read 2026-09-30 14:20
- both SHAs present locally (cat-file -t commit); shared checkout HEAD and develop 37205947ddd2, origin/develop 3e3a68260d0e; FETCH_HEAD mtime 2026-09-30 12:53:42; .git/config sha256 prefix 4f624a213933d54b; no .push-lock-* and no s-d1-* under worktrees/; s-b49-cleanup s-b49-ctrl s-b49-itemA s-b49-ks1054 s-b49-ks1054c present; DevMASTER 505255 MiB free | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files cat-file / rev-parse` + stat + shasum + `ls -a /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/` + df -m | read 2026-09-30 14:20
- #1339 squash 2cb858335472, parent 8af6ab821600; its file list (13 standalone locks + root + manifests + two email.ts); #1356 is one commit on 3e3a68260d0e touching 18 locks (root, frontend admin/verifier/website, services analytics billing governance mcp-server nft-certificate referral shared staking vc-issuer, observability, systemTest akto api-explorer performance playwright), none of #1339's 13 standalone | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files rev-parse / log / diff --numstat` (read verbs) | read 2026-09-30 14:21
- the @types census table (28 locks carrying either; disagree 2 / 2 / 15 / 15; pg versions) at 8af6ab821600, d9ce1403d158, 3e3a68260d0e, 52dadb07f70d | `git show <sha>:<lock>` for every Blockchain/Dev package-lock.json (40 per SHA) + /opt/homebrew/bin/python3 JSON parse (scratchpad census.py) | read 2026-09-30 14:21
- pre-#1339 vs #1356 head over the 13: brace-expansion 5.0.9/2.1.4/1.1.18 and fast-uri 3.1.7 in issuer, anchoring, api-gateway, originate vs 5.0.12/2.1.7/1.1.21/3.1.8; 1,288 entries version-differ in total | `git show 8af6ab821600:<lock>` and `52dadb07f70d:<lock>` + python3 parse | read 2026-09-30 14:22
- KS-1395 packages: systemTest/performance js-yaml 5.4.2, issuer and root undici 7.30.0 at both SHAs; baseline carries GHSA-r53p-7pc4-xj5r and not GHSA-r3ph-w7gj-g6xm at both | `git show <sha>:<path>` + python3 parse | read 2026-09-30 14:21
- compose: Blockchain/Dev/docker-compose.yml, 33 build: entries; governance Dockerfile builds /shared in a shared-builder stage with npm ci then COPY --from into the service builder | `git show 3e3a68260d0e:Blockchain/Dev/docker-compose.yml` and `:Blockchain/Dev/services/governance/Dockerfile` | read 2026-09-30 14:22
- KS-1379 Backlog, board account, creator board account, 1 comment 2b9cff63 (gate42 checklist); KS-1380 Todo, board account, creator Peter, 1 comment 6fdb4a18; KS-1387 Backlog, board account, creator Stuart, 2 comments 9d37f0f3 and ebb44574; KS-1395 Backlog, board account, creator Stuart, created 2026-09-30T02:52Z, 0 comments, measured at 37205947d; KS-1378 In Progress, 3 comments | Linear GraphQL issue query with comments(first:50) sorted client-side, no mutation (LINEAR_API_KEY read by name from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env, never printed), rc 0 | read 2026-09-30 14:21
- #1356 open, not merged, head 52dadb07f70d, author kksecura; #1339 closed merged; 24 open PRs; #1351 #1352 #1353 PeterObeden | GitHub REST GET /repos/Secuura/Distributed_Secuura/pulls/1356, /pulls/1339, /pulls?state=open (GH_TOKEN read by name from the same .env, never printed) | read 2026-09-30 14:22
- B 49th state: plan confirmed with ITEM A first; itemA measured and finding-3 scoping accepted; READY #1356 to gate49a; ITEM 4 removed and given to Seat D 1st; KS-1395 not to be commented | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-30_answer_seatB49_plan.md, _itemAmeasured.md, _ready1356.md, _1a1c.md | read 2026-09-30 14:20
- B 49th's routing finding (unsuffixed Seat D 1st mail read FOR ME, fixed; d1 hex controls) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-49th/mail/status-seatD.md and raise/seatD-cotenant-proof.txt + Wednesday's routing requirement to this drafter | read 2026-09-30 14:23
- the container recipe and suite/shared-dist findings | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-49th/itemA/PR-BODY.md :33-:39 and refresh45.log (read-only) | read 2026-09-30 14:23
- the -B row: launchers.conf maps Secuura/Blockchain-B to /Volumes/DevMASTER/!CODING/Secuura/Blockchain/Launch_Claude.command; inbox_routing.conf maps Secuura/Blockchain-B to secuura-blockchain@agentmail.to (yes); B 34th ran on it 2026-09-27 (pane %45) | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/cockpit.sh resolve Secuura/Blockchain-B` rc 0 + /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/launchers.conf + /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf + /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-27.md :56 | read 2026-09-30 14:20
- floor: cockpit panes wednesday %0, Secuura/Blockchain %81, fleet-monitor %1; no -B pane live | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/cockpit.sh status` + `tmux list-panes -a` | read 2026-09-30 14:23
- Docker 29.8.0, 24 CPU, 8.3 GB; images 32.13 GB, build cache 79.79 GB; b49probe-nft-certificate and b49probe-mcp-server present | `docker info` + `docker system df` + `docker images` | read 2026-09-30 14:22
- Kam's 14:18:29 instruction verbatim; 2 messages today, 0 withheld | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` rc 0 (live board, seat=wednesday) | read 2026-09-30 14:24
- 37 undelivered secuura- cards; secuura-five-new-advisories-block-every-push-0929 ruled a, delivered #1339 | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` rc 0 + `show secuura-five-new-advisories-block-every-push-0929` rc 0 | read 2026-09-30 14:21
- B 48th's KS-1380 carry and finding 3 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB48-2026-09-30.md :215-:226 | read 2026-09-30 14:23
- STANDING_LINES 356 lines, mtime 2026-09-30 07:01:49 | wc -l + stat of /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md | read 2026-09-30 14:23
- next fuse 211.6 h at 2026-09-30T04:23:28Z | /opt/homebrew/bin/python3 UTC arithmetic against 2026-10-09T00:00Z | read 2026-09-30 14:23

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-30 14:27
