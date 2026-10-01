LAUNCH BRIEF (Seat B 54th): fix GHSA-frvp by an override, remove its baseline row

# LAUNCH BRIEF: Seat B 54th, Secuura/Blockchain. Fix GHSA-frvp-7c67-39w9 (KS-530) with ONE npm override that lifts the single vulnerable `@hono/node-server` copy, regenerate the root lock with no collateral moves, and remove the frvp baseline row. ONE PR, T1, ONE gate, merge on its GO. From Wednesday

## BLUF
You are **Seat B 54th**. Seat B 53rd wrapped cold at 11:28:51Z. It left:
- **#1367 (KS-1015) and #1368 (KS-1364) MERGED on gate52.** develop went `0736d8b7849e` → `ed268a995a88` → **`ea6fcecc3a6f71a4f397ea678da54a06df130cd7`**, tree **`48f5f8afa6ef1f03f2d64e4afa24fd9f75213ad7`**, single parent `ed268a995a88` (drafter's REST `commits/ea6fcecc…`, 11:3xZ).
- **The 2026-10-09 fuse MEASURED ONLY** (B 53rd handover §7 `:201-:223`). For frvp it found that **the row's stated reason is WRONG**: the advisory has a v1 patched range (`<1.19.15` → **1.19.15**), not only the v2 one.
- **That finding is your work.** Kam's card `secuura-fuse-1009-measured-1001` recommends fixing frvp by an override, and its **default** (if he does not answer) is: *"Wednesday has the frvp override built and gated anyway, since it is a real fix inside our merge grant."*

**Develop at origin:** `ea6fcecc3a6f` (drafter's `ls-remote`, 2026-10-01T11:31:57Z). **Re-read it with `ls-remote` at boot.**
- ⚠ **`ea6fcecc3a6f` is NOT in the shared checkout's object store** (`cat-file -t` rc 128). Local `HEAD` and `develop` read `c56dd7c32edf`; `refs/remotes/origin/develop` reads **`ed268a995a88`** (B 53rd's second ruled fetch window, reflog `2026-10-01 21:15:15 +1000`). **Your base needs Q1.** Do NOT branch from `ed268a995a88` as a substitute: #1368 would be missing from your base.

**THE MEASURED FACTS YOU BUILD ON** (drafter, from blobs at `ea6fcecc3a6f` read via the GitHub API; re-measure each at your base):
- **Exactly ONE vulnerable copy exists in all 45 tracked `package-lock.json` files:** `node_modules/@prisma/dev/node_modules/@hono/node-server` **1.19.11** in `Blockchain/Dev/package-lock.json` (`:7641`). Its parent `node_modules/@prisma/dev` **0.24.3** (`:7617`) declares `"@hono/node-server": "1.19.11"` EXACTLY, so no caret admits the patch.
  - The hoisted `node_modules/@hono/node-server` (`:5931`) is already **1.19.17** (patched). `node_modules/hono` is 4.13.8 (`:14878`); `@hono/node-server@1.19.17` peers `hono ^4`.
  - `services/mcp-server/package-lock.json`: `@hono/node-server` 1.19.17 only (via `@modelcontextprotocol/sdk` 1.29.0, which asks `^1.19.9`).
  - `services/originate/package-lock.json`: **NO `@hono/node-server` entry at all.** It resolves `prisma` 7.10.0 → `@prisma/dev` **0.24.17**, and 0.24.17 no longer depends on `@hono/node-server` or `hono`.
  - The other 42 locks: no `@hono/node-server`, no `@prisma/dev`.
- **Who pulls `@prisma/dev` in the root lock:** exactly one parent, `services/originate/node_modules/prisma` **7.8.0** (`devOptional`), the `prisma` CLI that `services/originate/package.json:46` declares in **devDependencies** `^7.8.0`. `@prisma/dev` and its nested `@hono/node-server` are both `devOptional: true` in the root lock (B 53rd wrote "no `dev` flag", which is literally true; the flag is `devOptional`).
- 🔴 **A correction to the record: originate does not DECLARE `@hono/node-server`.** `services/originate/package.json:60` is inside its **`overrides`** block (`:51-:61`), `"@hono/node-server": "^1.19.15"`. npm honours `overrides` only in the ROOT manifest of an install. So that line governs originate's STANDALONE lock and is ignored by the workspace-root install. **That is why the root lock still carries 1.19.11.** No `package.json` anywhere declares `@hono/node-server` as a dependency.
- **Images.** **Only originate uses Prisma** (`services/originate/Dockerfile:38` `RUN npx prisma generate`). Its builder installs from `services/originate/package*.json` (`:28-:30`, `npm ci --ignore-scripts`), i.e. the standalone lock, which has no `@hono/node-server`. **No Dockerfile copies the workspace-root lock** (drafter's grep of all 37 Dockerfiles at `ea6fcecc3a6f`; #1364's body records the same fact). mcp-server's image installs from its own lock (`services/mcp-server/Dockerfile:28-:29`, `:56-:57`). **So the drafter predicts that this PR changes no image's install.** That is a prediction. You re-prove it (ITEM 1 step 8).
- **The row:** `Blockchain/Dev/scripts/audit/audit-baseline.json` (blob `4e5f5daba207`, 161 lines, 25 `accepted` entries, 7 dated). `GHSA-frvp-7c67-39w9` is at **`:88`**, `expires` 2026-10-09, ticket KS-530, and its reason says *"fix is >=2.0.5 only, a semver-MAJOR v1->v2 bump"*. That is the wrong reason.
  - frvp is a **DATED** row. It is **NOT** in `GRANDFATHERED_NO_EXPIRY` (`baseline-contract.mjs:58-:77`, 18 ids). Removing it touches neither the set nor its docstring count.
  - The second `@hono/node-server` row, **`GHSA-92pp-h63x-v22m` (`:76`, KS 470), IS grandfathered** (`baseline-contract.mjs:65`). **It is not yours.** If leg 6's CLEANUP line starts naming it after the override, report that, and remove nothing (#1355's precedent, below).

**Your queue, in this order:**
- **ITEM 0:** plan confirmation. **STOP after sending it.** Fetch, install, edit, regenerate, commit, push and raise nothing before her ANSWER.
- **ITEM 1:** BUILD the override, regenerate the root lock with no collateral, remove the frvp row, prove it all, and RAISE ONE PR (`Refs KS-530`, **T1**).
- **ITEM 2:** ONE READY → gate53 (Wednesday drafts it) → merge on `GO (Seat B 54th): merge <n> on gate53` → verify → handover → WRAP.

**Seat number:** `history.md`'s newest entry is Seat B 53rd (`:24`; next Seat B 52nd `:80`). Bounded census: `b 54th` 0 and `\bb54\b` 0, with control `b 53rd` 1 (`/usr/bin/grep -oiE`). Raw `b54` is **8**, all inside hex runs (among them `b54d762d1a90`, `d3b570ab9b54`, `bf766bb54`, `1be43b54`, `58a90b54`, `b54487216`). No `seatB-54th` folder and no `HANDOVER-seatB54` exist. **You are B 54th.**

**Budget. Hard line: 70% ctx.** Read your ctx off your own pane's statusline. If you cannot read it, ask Wednesday in your STATUS ("Please read my ctx."). **Never estimate it.**
- If ctx passes 70% at any point, finish the step in hand and start nothing else. Write the rest into your handover as UNRAISED / UNMEASURED / UNMERGED.
- **Keep ctx low.** Read by line range. Never `cat` a whole report, handover, lock diff or suite log. Send output to files and read back only the summary lines. The root lock is **674,706 B**: never print it.
- **Never end a turn on a "next up" line with nothing running** (STANDING_LINES `:338-:341`).

**The usage authority.** Weekly usage is **93%** (`usage_gate.sh --check` REFUSED rc 3, "weekly usage 93% >= 90%", gauge 9 min old, 21:39 AEST).
- **This seat runs on Kam's 17:40:22 live-board grant**, the TOP row of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md`. Verbatim: *"thank you.  Keep working with the Spark.  Don't worry about the usage quota as I will rotate Friday to a different account tomorrow morning"*. It ends at his account switch (Fri 2026-10-02 morning).
- **If you launch AFTER that switch, the grant is spent.** The authority is then the new account's gauge, which Wednesday reads before launch. Either way, **your launch and your gate are Wednesday's business, not yours.** Do not run `usage_gate.sh` as a stop for yourself, and do not argue the grant.
- **What the grant does NOT lift:** the QA gate before every merge, deploys, demo, production, money, external comms, and anything irreversible.
- **Necessity clause (cloud):** a local model cannot raise, gate or merge.

🔴 **ARM `inbox_watch49.sh` IN THE BACKGROUND AT BOOT, BEFORE ITEM 0's MAIL.**
- Arm it with **`timeout: 7200000`** (STANDING_LINES `:361-:362`) as a tracked background job. **Never `nohup … &` inside a shell that exits.**
- Note the re-arm deadline and re-arm before it. Re-arm after every match.
- **Before acting on any GO or relayed ruling, list the inbox via the API** and confirm the mail by its subject and timestamp.
- **One "no new mail" poll at the same second as a message's timestamp proves nothing** (STANDING_LINES `:367-:368`).
- A claim about what is RUNNING is a `ps` reading taken in the same action as the sentence.

**Authority:**
- **ITEM 1:** Kam's card `secuura-fuse-1009-measured-1001` (status **open**, unruled at the drafter's read). Its option (a), recommended: *"A Secuura seat adds the @hono/node-server override (>=1.19.15) and removes the frvp row, with the gate proving Prisma still works."* Its default: *"Nothing is re-dated (that is your signature, never Wednesday's). Wednesday has the frvp override built and gated anyway, since it is a real fix inside our merge grant."* **You act under the default.** It needs no answer from Kam. Plus Kam's 17:40:22 grant (above).
- **ITEM 2's merge:** Kam's tested delegated-merge grant of 2026-09-11 (merges on a gate's GO), plus the EXPIRING-GRANTS row "We approve and merge our own TESTED Platform K work".
- The tiering rule (Kam, 2026-09-05). Kam's week instruction is at `/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md`.
- ⚠ **The card's text says `>=1.19.15`.** A bare `>=` range admits **2.x**, the semver-major move KS-530 was written about. The override's VALUE is Q2, not settled by the card's wording.

**The shared checkout** (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`), drafter's read at 21:39 AEST:

| ref / file | value |
|---|---|
| `HEAD`, `refs/heads/develop` | **`c56dd7c32edf`** (never moved by B 53rd) |
| `refs/remotes/origin/develop` | **`ed268a995a88`** (B 53rd's second ruled window) |
| `ea6fcecc3a6f` in the object store | **absent** (`cat-file -t` rc 128) |
| `.git/FETCH_HEAD` mtime (`TZ=UTC stat`) | **2026-10-01T11:15:15Z** |
| `.git/config` sha256 prefix | **`4f624a213933d54b`** |
| tracked-modified / untracked | 0 / 17 |
| `.git/worktrees` entries | **482** |

- **No `.push-lock-*` directory** exists in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/`.
- B 53rd's worktrees `s-b53-ks1015` and `s-b53-ks1364`, B 52nd's `s-b52-ks1364`, B 51st's four `s-b51-*` and the eight `s-b5-*` are present. **None is yours.** Their removal is Wednesday's to order.

**At origin (`ls-remote`, 11:31:57Z):**
- B 53rd's branches `feature/ks-1015-referral-lookup-spec-declares-envelope-b53-1` (`ac3ceee7f440`) and `feature/ks-1364-two-operation-residue-body-required-b53-2` (`2a3dcd912a33`) are still present (merged).
- **Two older KS-530 branches exist and are NOT yours:** `feature/ks-530-audit-baseline-redate-b44-1` (`9199a2f9f739`) and `feature/ks-530-hononode-server-v1-v2-major-bump-ghsa-frvp-originate-mcp-r21-patchline-1` (`f2751859c015`). Do not touch, rebase or reuse either. They are good namecheck controls (below).
- No `-b54-` ref.
- GitHub has **21** open PRs. **12 touch `Blockchain/Dev/package-lock.json` or `Blockchain/Dev/package.json`**: Peter's **#1360** (KS 1380, the 15-lockfile revert, root lock +2/−6, no `hono` or `prisma` text in its hunk), `kksecura`'s #920 (package.json), and ten Dependabot PRs (#572, #575, #635, #639, #649, #945-#949). **0 touch `audit-baseline.json` or `baseline-contract.mjs`.** Control: the same filter hits #1355's file list twice.
  - **Your merge may leave #1360 or a Dependabot PR needing a rebase. That is NOT yours to fix, mention to anyone, or wait on.** Kam ruled (b) on `secuura-ks1380-peter-reverting-1358`: he talks to Peter himself.

**Seat identity (PROPOSED for ITEM 0 to confirm, Q4):**
- **Pane:** `Secuura/Blockchain`. At the drafter's `tmux list-panes -a` (21:3x AEST) only `%0` and `%1` (`fleet:main`) exist. **You are the only Secuura seat.**
- **Record folder:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<launch date, AEST>_seatB-54th/`. None exists. Put small text files only there.
- **Token `b54`, tool suffix `49`, round 49, lock `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-lock-49`.**
- 🔴 **`lock49.sh` REFUSES without `LOCK_SEAT`** (REQUIRED, no default). Export `LOCK_SEAT='Secuura/Blockchain b54'` before every take that YOU make by hand.
  - Take and release in ONE invocation. Release with the pid the HOLDER FILE records, never `$$`. Put the take's rc on its own line.
  - Expect a rule-B cool-off between takes (B 53rd measured ~90 s; handover `:270`).
- 🔴 **`push49.sh` TAKES `.push-lock-49` ITSELF** (`push48.sh:121` take, `:146` release). **Call it BARE. Never wrap it in your own take** (STANDING_LINES `:373-:374`). B 53rd wrapped it and waited 221 s on its own holder. **Wrap by hand only bare git verbs that do not lock themselves: the ruled fetch, and a merge tool that does not lock.**
- 🔴 **rc ON ITS OWN LINE, NEVER THROUGH A PIPE:** `cmd > "$REC/x.log" 2>&1; rc=$?`. `${PIPESTATUS[0]}` is EMPTY in zsh, and an rc read after a pipe measures the LAST stage (B 53rd §8.3).
- 🔴 **Pass tool arguments LITERALLY, never through a scalar `$ARGS`.** zsh does not word-split a scalar (B 53rd §C.3: `merge48.py` exited 2 on argparse).
- 🔴 **curl to a FILE and parse the file.** Never `echo "$R" | python3` (B 53rd §C.4: control characters in a PR body broke `json.load` and produced a false STOP).
- 🔴 **`TZ=UTC stat`.** Without it, a local time prints under a `Z` label (B 53rd §1).
- 🔴 **ABSOLUTE artefact paths in any command that `cd`s.** **When a whole set goes red at once, suspect the instrument first.**
- 🔴 **Never name a zsh variable `path`.** In zsh, `$path` IS `$PATH`.
- 🔴 **`git rev-parse <rev>:<path>` ECHOES its argument when the path does not resolve.** Resolve with `git cat-file -e` and a control path that does not exist.
- **Worktree:** ONE, made with `git worktree add --detach <abs path> ea6fcecc3a6f` (after Q1), **never `-b`**: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b54-ks530`. Plus ONE short-lived scratch worktree for the red-first control and the pristine regen control (ITEM 1), which you remove yourself and name in the handover.
  - 🔴 **Install at the WORKSPACE ROOT, then BUILD `packages/shared` BEFORE THE FIRST TEST** (STANDING_LINES `:376-:377`): `npm ci --ignore-scripts` in `Blockchain/Dev`, then `npm run build --workspace=packages/shared`. The symlink exists after `npm ci`, so a listing reads "installed", but `main` is `dist/index.js` and nothing resolves until it is built. **Prove resolution BY ACTION** (`require.resolve` plus a real import of `@secuura/shared` from inside originate and mcp-server).
  - **Runners:** originate uses **jest**; mcp-server uses **vitest** (`vitest run`). **vitest prints each failing name TWICE.** Trust the runner's own totals, never a `grep -c`.
  - If any write on DevMASTER returns ENOSPC, STOP and mail. DevMASTER had **474,995 MiB** free at the drafter's `df -m`.

**🔴 NAMESPACE AND MATCHER, this round (no co-tenant is live, but B 53rd's mail sits in this inbox):**
- **`namecheck49`:** `MINE = "b54"`.
  - FOREIGN adds **`"b53"`** and keeps `"b52"`, `"b51"`, `"b50"`, `"d1"` and the older ones.
  - `EXPECTED_ADOPTIONS = 0`. Prove the constant and the set agree with a tamper that reds.
  - **Re-key the PROBE DATA, not just the constants** (`rekey_check48.py:661`/`:663`).
  - Your new branch: `feature/ks-530-<slug>-b54-1`.
  - **Controls, each going the other way on a REAL ref:** `feature/ks-1364-two-operation-residue-body-required-b53-2` (`2a3dcd912a33`) reads FOREIGN. **`feature/ks-530-audit-baseline-redate-b44-1` (`9199a2f9f739`) reads FOREIGN: it shares your ticket prefix, so it is the control that matters this round.** A planted `-b54-9` reads MINE. `feature/ks-530-…-r21-patchline-1` and `kamilkreiser/ks-587-document-blob-simulated-d1` must not read MINE.
- **`inbox_match49`:** `MINE = "b 54th"`. **OTHER_SEATS must include `b 53rd`**, as well as `b 52nd`, `b 51st`, `b 50th`, `d 1st`/`d1`, `seat h` and the older ones.
  - 🔴 **Trap 4, NINETEENTH generation, and B 53rd is the new entry.** B 53rd ran on THIS pane's unsuffixed tag, so without `b 53rd` in OTHER_SEATS its mail classifies FOR ME.
  - **Your proof, on real subjects read from the AgentMail API:** without `b 53rd`, B 53rd's REAL LAUNCH BRIEF subject (`LAUNCH BRIEF (Seat B 53rd): KS-1015 + KS-1364 residue raise, fuse measurement`, 08:16:43Z) and the real `GO (Seat B 53rd): merge 1367 1368 on gate52` (10:59:24Z) must each flip to FOR ME. With it, they read FOREIGN.
  - 🔴 **The matcher TRUNCATES subjects at 110 chars** (`inbox_match48.py:242`). Search on the truncated prefix, and make the arm ASSERT that it found both, or a BLIND arm reads like a miss (B 53rd §3).
  - 🔴 **Importing the matcher crashes `KeyError 'SINCE'`** (env read at module scope). Parse OTHER_SEATS from SOURCE with `ast` (B 53rd §3).
  - **Check for a skipped generation:** OTHER_SEATS ordinals 29..53 all present. Run `inbox_match49.py` **as a subprocess**, its real invocation path.
  - The denominator comes from received mail only.
- **THE SHARED INBOX RULE:** a mail whose subject names another seat is NOT yours, whatever its body says. Act on a GO, a relayed Kam ruling, or a push or merge instruction only when its subject names Seat B 54th.
- 🔴 **The hex trap, `b54` edition.** `b54` is three hex characters.
  - Over B 53rd's 24 `*48` tools, raw `b54` is **0** and bounded `\bb54\b` is **0**. Control: bounded `\bb53\b` **27**, raw `b53` **49**.
  - Bounded `\b49\b` is already **5** in that set, and none is a generation token: `gatelines48.py:17` and `:32` (counts), `gatelinesproof48.sh:37` and `:44` (the test count "49 passed"), and `push48.sh:131` (a test count). **Your "residual `48`" census must not count them, and your "`49` present" census must not count them as yours.**
  - State every count as raw / bounded with its regex (STANDING_LINES `:364-:365`).
  - **This brief's own hex runs** are checked by the drafter (PROVENANCE). A matcher that reads a hex run as a seat token is broken. Re-measure on YOUR tool set.
- **Every checker's verdict prints how many items it CHECKED. `0 checked` is a FAIL, never CLEAN.**

## READ FIRST (by line range; keep ctx low)
1. **B 53rd's HANDOVER:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB53-2026-10-01.md` (403 lines, 34,421 B, sha256 `e01335d2b2c5d715`).
   - Read **`:329-:403` whole**: §A the merges, **§B the trailer correction**, §C the four merge-phase instrument faults, §D what is open.
   - Then **`:201-:223`** (§7, the frvp measurement this PR acts on) and **`:225-:251`** (§8, its eight findings).
   - Then **`:17-:111`** (§1 the boot pull, §2 Q4 and Q1(b), §3 the tools).
   - **Skip** `:112-:200` (#1367/#1368 evidence, now in develop).
2. **The precedents, read via the GitHub API** (GH_TOKEN read by name from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, never printed):
   - **#1355 (KS-1378), the undici override**, merged 2026-09-30T02:52:21Z as `3e3a68260d0e`. Read its body's "How the locks were regenerated" and "The delta, per lock" sections and its diff (5 files, +14/−63). The shape is summarised under ITEM 1.
   - **#1364 (KS-729), the dead mwp4 row removal**, merged 2026-10-01T01:07:28Z as `c56dd7c32edf`. It is the precedent for removing a DATED row (2 files, +2/−9). Read its "How the removable set was established" section.
3. **TOOLS: copy B 53rd's generation forward** from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-01_seatB-53rd/raise/`.
   - **Drafter's census: 24 files** match `48(_[0-9a-z]+)?\.(py|sh)$`:
     - `arms48.py`, `bannercheck48.py`, `build_addendum48_1367.py`, `build_addendum48_1368.py`;
     - `ffproof48.sh`, `gatelines48.py`, `gatelinesproof48.sh`, `inbox_match48.py`, `inbox_watch48.sh`, `keyscan48.py`, `keyscanproof48.sh`;
     - `lock48.sh`, `lockproof48.sh`, `merge48.py`, `namecheck48.py`;
     - `push48_ff.sh`, `push48.sh`, `pushproof48.sh`, `raise48.py`, `raiseproof48.sh`;
     - `refresh48.sh`, `rekey_check48.py`, `rekey48.py`, `watchproof48.sh`.
     - Plus `raise/inert/one_merge46.sh` (INERT) and `raise/templates/` (5: `build_addendum46{,_1356,_1363,_1364}.py`, `build_addendum47_1365.py`).
   - **State your census in ITEM 0**, raw and bounded.
   - **Quarantine B 53rd's `rekey48.py` FIRST.** Move it into `_b53_artefacts_NOT_MINE/` in YOUR record folder.
     - Prove its sha256 equal to the original.
     - Show the equality test FAILING on a 1-byte mutated copy kept OUTSIDE the scanned folder.
     - Quarantine the round's RECORDS with it, not its tools. **Do not copy `_b52_artefacts_NOT_MINE/` forward.**
   - **PARK `build_addendum48_1367.py` and `build_addendum48_1368.py` byte-untouched in `templates/`** (then 7 templates), as B 53rd parked `build_addendum47_1365.py`. They are the GO-parser templates for ITEM 2.
   - Hand-write `rekey49.py` **with itself in its own map, carrying NO bare `"48"` and NO seat token.** Run the pass ONCE, before the hand-fixes.
     - The drafter counted **120 distinct tokens containing "48"** in the 24 files. A bare 48→49 rule destroys, among others: `48th` (seat ordinals in LINEAGE lines), `gate48`, `gate48a`, `gate48b`, `ready48a`, `KS-1348`, `1348r2`, **`ks-1378-undici-override-and-jsyaml-542-b48-1` (#1355's REAL branch, which you will read this round)**, `b48`/`-b48-`/`seatb48`/`s-b48-` (B 48th's seat tokens), `trap4-real-subjects-b48.json`, `inbox_snapshot_b48.json`, the times **`05:48:47Z`**, `05:48:48Z` and `06:14:48`, and hex/UUID runs (`2d2b5ffa-…-b485-…`, `4d68be3a-…-48a0-…`, `5aacd245-…-48d4-…`, `3aeebf2cf09bb481`).
     - **Diff your pass against B 53rd's originals.** Lineage lines survive byte-identical; restore any your pass touched, as B 52nd did.
   - Then:
     - `inbox_match49` / `namecheck49` as above;
     - `bannercheck49` `GEN = "49"`, keeping B 53rd's KEEP-literal mask and its CONTROL C (mask OFF must differ by EXACTLY the KEEP lines);
     - `rekey_check49` `THEIRS_DIR` → `2026-10-01_seatB-53rd`, with its COVERAGE assertion (`MINE == ls`) AND B 53rd's inverted PARKED block over `templates/` + `inert/` (a parked file MUST keep its own generation token);
     - `lock49.sh` → `.push-lock-49`, keeping REQUIRED `LOCK_SEAT`. Its REFUSED message's example must say `b54`;
     - `push49.sh` takes and releases `.push-lock-49` itself (prove it with `lockproof49.sh`);
     - `raise49.py` builds `s-b54-{tag}`, keeping B 53rd's `--existing-worktree` and `--expect-modified` flags. Prove it.
     - 🔴 **`merge49.py`: carry B 53rd's `no_trailer` suppression forward, AND EXTEND IT** (STANDING_LINES `:370-:371`). In `merge48.py` the suppression (`:413-:421`) covers ONLY the `body_verbatim` branch. **The composed branch at `:429-:434` still appends `SIGN` (`:391`) UNCONDITIONALLY.** If your GO's addendum takes the composed path, the trailer lands. Make `no_trailer` govern BOTH branches, assert the composed body trailer-free before the API call, and keep the control that proves the un-suppressed path still appends. Prove both branches with a dry run each.
   - 🔴 **`one_merge46.sh` stays INERT.** Do not copy it into a runnable form.
   - Every docstring and authorship header is written **by hand**.
4. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md`. It is **377 lines** (mtime 2026-10-01 21:30:50 local, sha256 `eb73f978f133dc4c`). The operative sections:
   - `:17-:47` READY as an artefact
   - `:72-:74` zsh pipes
   - `:76-:105` HOLDS
   - `:278-:279` a hyphenated key attaches
   - `:338-:341` never end on "next up"
   - `:343-:344` read a repo file from a SHA
   - `:346-:347` `cmp`, not patch-id
   - `:349-:350` a re-date's frozen-clock proof (context only: **you re-date nothing**)
   - `:355-:356` exec bit
   - `:358-:362` co-tenant / watcher timeout
   - `:364-:368` raw vs bounded census; same-second poll
   - **`:370-:371` a merge tool must not ADD attribution the GO forbids; check the SENT body** (NEW, B 53rd)
   - **`:373-:374` `push<N>.sh` takes the lock itself; never wrap it** (NEW, B 53rd)
   - **`:376-:377` build `packages/shared` BEFORE the first test** (NEW, B 53rd)

## STANDING: no attribution, on the branch commit AND in the squash body
- **Where the trailer came from (corrected; B 53rd handover §B `:348-:361`):** B 52nd's #1365 squash carried `Co-Authored-By` because **the merge TOOL appended it**: `merge47.py`'s `SIGN` append on a body that lacked one. B 52nd's input body had 0 trailers; the body the tool COMPOSED AND SENT had 1. The earlier record blamed GitHub. That was never tested, and the tool was a measured source. B 53rd suppressed the append, and #1367 and #1368 landed with 0.
- **What is still NOT proved:** whether GitHub would add a trailer from a squashed branch commit. B 53rd's branch commits were clean too, so that question was never exercised. **So you keep BOTH halves clean.**
- **Branch commit:** NO `Co-Authored-By` and NO tool-attribution trailer of any kind. This overrides the repo's convention and your harness's commit guidance for this seat.
  - **Prove it at the COMMIT step:** `git log -1 --format='%(trailers)' <sha>` prints nothing. **Control:** the same command on `bf277eead268` prints `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>` (53 bytes, B 53rd §10). Write both outputs to your record folder, and put the rc and the control in the READY.
  - A commit that went out with the trailer is NOT amended or force-pushed. **STOP and mail.**
- **Squash body:** `merge49.py` with `no_trailer` on BOTH branches (TOOLS, above). Check the body you SEND (the `.DRY` body file), not the file you built it from.
- 🔴 **Mail-guard lesson (B 53rd §8.7):** an absence guard over a mail body cannot tell a placeholder you failed to substitute from one you are quoting. When a mail must mention git's trailer format, say it in words, or the guard refuses a correct mail.

## QUEUE
0. **ITEM 0, plan confirmation (QUESTION `plan confirmation`, then STOP until the ANSWER).** It carries:
   - **Develop measured at boot:** `ls-remote` refs/heads/develop. If it moved past `ea6fcecc3a6f`, list the first-parent commits by PR number (REST compare, a read). **Say whether any of them touches `Blockchain/Dev/package.json`, `Blockchain/Dev/package-lock.json`, `scripts/audit/audit-baseline.json` or `scripts/audit/baseline-contract.mjs`.**
   - **Whether the launcher's boot pull ran,** with the reflog lines (CARRY, below). Then **Q1**.
   - Your tool census (raw and bounded), the re-key receipt with its lineage diff, the `merge49.py` both-branch suppression proof, and the trap-4 nineteenth-generation proof.
   - Your watcher pid, READ at the moment you write it.
   - **Read-only re-reads of KS-530 and KS-528:** state, assignee, newest comment. If either has a new comment or state since the drafter's read (PROVENANCE), say so.
   - **Q1-Q4.**
   - **Every launcher preflight warning VERBATIM** (B 53rd saw `[F-02] No SSH identity available for git …`).
   - **Your ctx, read off your pane, or "Please read my ctx."**
1. **ITEM 1, BUILD + RAISE ONE PR, `Refs KS-530`, T1** (section below). STATUS before you start, after the override/lock/row measurement set, and after the push. **No READY yet.**
2. **ITEM 2, ONE READY, HOLD for `GO (Seat B 54th): merge <n> on gate53`, merge, verify** (section below). Then the handover and WRAP.

## OPEN QUESTIONS for ITEM 0
- **Q1: how your base `ea6fcecc3a6f` gets into the object store.**
  - **(a) Moot only if the boot shows `cat-file -t ea6fcecc3a6f` → `commit`** with the reflog lines that brought it, `.git/config` sha256 unchanged and 0 tracked modifications. **Fetch nothing then.**
  - **(b) Otherwise, PROPOSED: ONE bounded fetch, the same shape as B 53rd's.** `git -c core.sshCommand="<the repo's own, with -o ServerAliveInterval=30 -o ServerAliveCountMax=40>" fetch --no-tags origin refs/heads/develop:refs/remotes/origin/develop`.
    - No `--prune` and no other refspec. **Never write the shared `.git/config`.**
    - Under `.push-lock-49`, taken BY HAND (a bare git verb), in ONE invocation.
    - Record before and after: `TZ=UTC` FETCH_HEAD mtime, the all-refs listing diff (expect exactly 1 moved, `refs/remotes/origin/develop` `ed268a995a88` → `ea6fcecc3a6f`, 0 added, 0 removed), `refs/remotes/origin/*` count, and the `.git/config` sha256.
    - Local `develop`/HEAD are NOT moved.
    - **Do not fetch before her ANSWER. One fetch. A second needs a fresh ruling** (B 53rd needed one for its chained merge; your single-PR merge should not, see ITEM 2).
- **Q2: the override's SHAPE, VALUE and REGEN ROUTE. You propose one, with evidence; Wednesday rules.**
  - **Scoped**, the drafter's lean: `"@prisma/dev": { "@hono/node-server": "^1.19.15" }` in the `overrides` of **`Blockchain/Dev/package.json` only** (`:77-:93`). It names exactly the one parent that pins the vulnerable copy, and it mirrors the existing scoped entry `"jsdom": { "undici": "^7.29.1" }` (`:90-:92`). Expected effect (UNMEASURED): the nested `@prisma/dev/node_modules/@hono/node-server` entry dedupes onto the hoisted 1.19.17 and disappears, as `jsdom/node_modules/undici` did in #1355.
  - **Top-level**, the alternative: `"@hono/node-server": "^1.19.15"`, the same value as originate's own override (`services/originate/package.json:60`). It also constrains mcp-server's path through `@modelcontextprotocol/sdk` in the root tree (already 1.19.17, so no move expected). It is a wider net, and it must be REMOVED when KS-530's real v2 migration lands.
  - **The value:** `^1.19.15`, not the card's `>=1.19.15`, unless you show why. A `>=` override admits 2.x on a fresh resolve. Measure the version each produces; do not reason it.
  - **Not proposed, recorded as evidence:** originate's standalone lock already resolves `prisma` 7.10.0 → `@prisma/dev` 0.24.17, which has NO `@hono/node-server` at all. A `prisma` bump in the root tree would remove the copy without any override. It moves the Prisma CLI and many entries (collateral), so it is outside this PR's shape. Name it in the PR body's "alternatives", and do not build it without a ruling.
  - **Comment key:** whether to add a `"// overrides KS 530"` note beside the entry, as `:76` does for KS 493. #1355 added none. Default: none; the PR body carries the reason.
  - **The regen route:** #1355's shape (body, "How the locks were regenerated"): `node:24-alpine` (npm **11.19.0**, node **v24.21.0**, printed in the same run), `Blockchain/Dev` mounted whole (the root lock carries `file:` link entries, so a per-directory mount is the `EMISSINGTARGET` case of KS 1394), and **`npm update <pkg> --package-lock-only --ignore-scripts`** (#1355 found `npm install --package-lock-only` left the root lock unmoved). For you, `<pkg>` is `@hono/node-server`. The host here has npm **11.5.1** / node **v24.7.0** (drafter's `npm -v`/`node -v`). **Say which toolchain you will use and why.** A lockfile written by a different npm can churn unrelated fields; that is exactly a collateral move.
  - ⚠ **npm prints `up to date` even when it rewrote the lock** (#1355). The byte comparison is the instrument, not the banner.
- **Q3: does Prisma still run with `@hono/node-server` 1.19.17? Your PROPOSED proof, BEFORE and AFTER, at your base:**
  - **Find the importer first, by action:** which file in `prisma` 7.8.0 (`services/originate/node_modules/prisma` in a root install) loads `@prisma/dev`, and which file in `@prisma/dev` 0.24.3 loads `@hono/node-server`. `grep` for the module specifier in their `build`/`dist` trees, with a control specifier that must hit.
  - 🔴 **The bundling trap.** `Blockchain/Dev/package.json:76` records that `@prisma/dev` BUNDLES `valibot` 1.2.0, so a valibot override was INERT. **If `@prisma/dev` bundles `@hono/node-server` into its own dist, the override would move the lock and the audit, and leave the executed code at 1.19.11. That is a false fix.** Prove the opposite: the importer `require`s/`import`s `@hono/node-server` as an external specifier, and `require.resolve('@hono/node-server/package.json', { paths: [<@prisma/dev's own dir>] })` returns the nested 1.19.11 before and the hoisted 1.19.17 after (read the `version` from the resolved file). **If it is bundled, STOP and mail.**
  - **Then run Prisma's real entrypoints:** `npx prisma --version` from `services/originate`, and the CLI command that reaches `@prisma/dev` (the drafter believes it is `prisma dev`, the local Prisma Postgres server; you find it from the importer). Start it, read its answer (a listening port or its own ready line), then stop it by YOUR pid only. **Never point it at a real database or any `DATABASE_URL` from `.env`.** Also run `npx prisma generate` from `services/originate` (the command `services/originate/Dockerfile:38` runs). Record rc and the version lines BEFORE and AFTER.
- **Q4: token/suffix/lock.** `b54` / `49` / `.push-lock-49`. Agree, or say why not.
- **Q5: the push identity.** If `[F-02] No SSH identity available for git …` prints again, re-prove the push identity before you build. Use B 53rd's shape (handover §2 `:34-:39`): `git push --dry-run` under the repo's `core.sshCommand` to a probe ref `feature/ks-530-identity-probe-b54-0`. It must write no ref: REST `git/ref` 404, control `develop` 200, and `ls-remote 'refs/heads/*probe*b54*'` 0 refs. **STOP on failure.** The dry run does NOT run the preflight hook.

## ITEM 1 IN DETAIL (ONE PR: the frvp override; T1)
**#1355's shape, which you follow** (its diff and body, read via the API):
- **Where `overrides` lives:** in the ROOT `Blockchain/Dev/package.json` (`"undici": "^7.29.1"` now at `:89`), and ALSO in `frontend/issuer/package.json` (`:68`) because frontend/issuer has its own standalone lock that its Docker image installs. **For frvp, the only lock with the vulnerable copy is the ROOT lock, so only the root manifest is edited**, unless your measurement finds otherwise (then STOP and mail).
- **How the locks were regenerated:** Q2, above. **A pristine control tree at the same SHA, given the identical commands, did not move.** So the override supplies the direction and the `update` verb the re-resolution, and neither alone moves it. **You repeat that control.**
- **The delta was proved per lock, against that control:** the entries that changed, with `integrity` and `resolved` checked against the registry's `dist` for the new version, plus a control comparison that must return false.
- **Baseline: #1355 removed NO row** and touched no `GRANDFATHERED_NO_EXPIRY` entry. It quoted leg 6's CLEANUP line verbatim and left that cleanup to a separate change.
- **#1364 is the precedent for removing a DATED row** (`GHSA-mwp4-54f8-5fhr`): rows 26 → 25, `GRANDFATHERED_NO_EXPIRY` byte-equal, `expected-case-count` and `baseline-contract.test.mjs` untouched, **the contract floor not lowered**, and the removed set proved by parsing both blobs (removed exactly `{id}`, added none, no other row's bytes changed, **no `expires` changed anywhere**).
  - It also found that **leg 7's CLEANUP block cannot see these rows**: it filters on `e?.scope === 'standalone-locks'` (`audit-locks.mjs:299`, unchanged at `ea6fcecc3a6f`), and no row carries a `scope`. Do not read leg 7's CLEANUP as evidence either way.

**THE CONTRACT, measured by the drafter at `ea6fcecc3a6f`:**
- `baseline-contract.test.mjs:217` asserts the REAL baseline has **more than 20** entries. Yours goes 25 → **24**. It still passes; **do not lower the floor.**
- `:220-:231` asserts the no-expiry set EQUALS `GRANDFATHERED_NO_EXPIRY`. frvp has an `expires`, so it is outside that set. Expect no change.
- `baseline-contract.mjs:44` says "The 18 entries"; the set holds 18 and stays 18. **No edit to `baseline-contract.mjs` at all.** If you find you need one, STOP and mail.
- `package.json:46` `audit:contract` runs `baseline-contract.test.mjs`, `lock-discovery.test.mjs` and `gate-exit-codes.test.mjs`.

**BUILD AND PROVE (each rc on its own line, with the SHA and platform):**
1. **Q1 as ruled, then `s-b54-ks530` at `ea6fcecc3a6f`.** Prove the base blobs with `cat-file -e` and a nonexistent-path control: `Blockchain/Dev/package.json` `d22c14e6c370`, `Blockchain/Dev/package-lock.json` `c8cf17aa62a5`, `scripts/audit/audit-baseline.json` `4e5f5daba207`, `scripts/audit/baseline-contract.mjs` `ef82d7c5211d`, `scripts/audit/baseline-contract.test.mjs` `2379c0aeee6e`.
   - `git grep -n frvp ea6fcecc3a6f` and report EVERY hit. Only `audit-baseline.json` is yours to change. Any other file that a gate READS (an exception list, a test fixture that pins the id) is a STOP and a mail. Prose mentions in docs are reported, not edited.
2. **BEFORE, on a PRISTINE tree:** the workspace-root install, the `packages/shared` build and the resolution proof. Then:
   - `npm run audit:contract`, `npm run audit:gate` (leg 6) and `npm run audit:locks` (leg 7). Each rc on its own line. **Control at develop: leg 6 is rc 0 with frvp BASELINED** (in the baselined count, not reported as new). Quote the summary line and the CLEANUP line verbatim.
   - originate suite (**jest**) and mcp-server suite (**vitest**). Totals only.
   - **Q3's BEFORE readings** (importer, resolve path + version, `prisma --version`, the `@prisma/dev` command, `prisma generate`).
3. 🔴 **RED-FIRST (a control, by reading, not by assertion in a new test):** in the SCRATCH worktree at `ea6fcecc3a6f`, remove the frvp row WITHOUT the override, and run leg 6. **It must go rc 1 and name `GHSA-frvp-7c67-39w9`.** That proves the row is load-bearing today and that the override, not the deletion, is what makes your head green. Restore nothing in your real worktree from it; remove the scratch worktree after the regen control below.
4. **The override + the regen** as ruled in Q2, in `s-b54-ks530`. Then the **pristine regen control** in the scratch worktree: the identical regen commands WITHOUT the override must leave the root lock byte-identical (`cmp` rc 0).
5. 🔴 **NO COLLATERAL. The lock diff shows ONLY `@hono/node-server` entries changing.**
   - Parse BOTH lock blobs (base and head) as JSON and diff the `packages` maps key by key. Do not eyeball the text diff.
   - **Allowed:** `node_modules/@prisma/dev/node_modules/@hono/node-server` removed (or re-versioned to ≥1.19.15), and the hoisted `node_modules/@hono/node-server` unchanged at 1.19.17 (or changed only in `version`/`resolved`/`integrity`, if your ruled value moves it).
   - **Expected byte-identical:** the `node_modules/@prisma/dev` entry. Its `dependencies` map records the package's OWN manifest (`"1.19.11"`), not the override. If it changes, report how, and STOP.
   - **List EVERY other moved entry** (added, removed, any field changed, `dev`/`devOptional` flips included) **and STOP and mail.** #1355's root regen carried 12 such flips (eleven `lightningcss-*` binaries and `magicast`, `dev: true` → absent / `devOptional`). Those landed with #1355 and should not recur. If ANY appear, they are a STOP for you, not a precedent: Wednesday rules.
   - The `services/mcp-server` and `services/originate` locks and all 42 others: **byte-identical** (`git diff --numstat` shows none of them).
   - `integrity` and `resolved` of any new or changed `@hono/node-server` entry equal the registry's `dist` values (`npm view @hono/node-server@<v> dist --json`), with a control against another version's integrity that returns false.
6. **Remove the frvp row** from `audit-baseline.json` (`:88`, the whole `GHSA-frvp-7c67-39w9` object). Prove by parsing both blobs: rows 25 → 24; removed exactly `{GHSA-frvp-7c67-39w9}`; added none; every surviving row byte-equal; **no `expires` changed anywhere** (the two react-router rows keep `2026-10-09`); `GRANDFATHERED_NO_EXPIRY` byte-equal; `expected-case-count` and `baseline-contract.test.mjs` untouched by name and by blob. Keep the file's existing formatting (indent and trailing newline); the text diff of this file is ONE removed object, nothing else.
7. **AFTER, at head (fresh `npm ci --ignore-scripts` from the new lock, then the shared build again):**
   - `audit:contract` **rc 0**; leg 6 **rc 0** with frvp **neither reported nor baselined** (it is gone from both); leg 7 **rc 0**. Quote each summary line. **The denominators must move** (#1355's shape): leg 6's baselined count 25 → 24, and frvp's line gone from the reported set.
   - **Quote leg 6's CLEANUP line verbatim.** If it now names `GHSA-92pp-h63x-v22m` (the grandfathered hono row), **report it and remove nothing** (#1355's precedent; that row's removal would edit `GRANDFATHERED_NO_EXPIRY`, which is not this PR).
   - **Q3's AFTER readings**, each against its BEFORE: importer unchanged, resolve path now the hoisted copy at the patched version, `prisma --version` rc 0 and the same version line, the `@prisma/dev` command up and stopped, `prisma generate` rc 0.
   - Suites: originate (jest) and mcp-server (vitest). **0 new reds.** Any red that is not red at develop is a STOP.
   - `tsc --noEmit` for originate and mcp-server, as a no-regression reading ONLY (base rc vs head rc). Service tsconfigs exclude tests (originate's exclude is wider still, B 53rd §5).
8. **Images.** Re-prove the drafter's finding with your own grep over every `Dockerfile` at your base: which `COPY` lines bring a lock into a build, with a control line that must hit (originate's `services/originate/package*.json`, `Dockerfile:28`).
   - **If no image reads a lock this PR changes:** say so with the grep and the control. Build nothing. The PR body states it in one line, as #1364's did.
   - **If one does:** build THAT image only (`docker compose -p b54probe build <service>`), build only. Nothing started, pruned or removed. Record the digest against develop's build.
9. `git diff --numstat ea6fcecc3a6f` touches **exactly 3 paths**: `Blockchain/Dev/package.json`, `Blockchain/Dev/package-lock.json`, `Blockchain/Dev/scripts/audit/audit-baseline.json`. Exec bits unchanged (STANDING_LINES `:355-:356`; all 100644).

**THE PR:**
- Branch `feature/ks-530-<slug>-b54-1`.
- Subject `KS-530: …`, ≤ 84 chars declared, so it lands ≤ 92. Measure it.
- Body: `Refs KS-530` on its own line. **It narrows KS-530 and does not close it.** KS-530 is titled "@hono/node-server v1->v2 major bump (GHSA-frvp) - originate + mcp-server runtime". This PR fixes frvp on v1 and does NOT do the v2 bump. Every other key is de-hyphenated (KS 528, KS 1378, KS 729, KS 493, KS 470). **No closing keyword + reference** anywhere.
- The body states, each with its instrument: the one vulnerable copy and its exact pin; the corrected reading of `services/originate/package.json:60` (an override, ignored by the root install); the override shape and value as ruled; the regen route and toolchain; the per-lock delta table (#1355's shape); the pristine control; the red-first control; the three legs at develop and at head; leg 6's CLEANUP line verbatim; Q3's before/after table; the image finding; the "alternatives" line (the `prisma` 7.10.0 route, not taken).
- **NOT COVERED:** no live run of any service; no Schemathesis, Akto, k6 or Playwright; `mobile/secuura-app` is outside the audit corpus (KS 769) and unmeasured; the 2026-10-09 react-router rows (KS 528) are untouched and still expire then; anything Q3 could not reach.
- **Migrations + config:** none. No schema, no environment variable, no compose file.
- The commit carries **no trailer** (STANDING above). Prove it.
- **Push ONCE with `push49.sh`, called BARE (it takes and releases `.push-lock-49` itself).** Quote the preflight ratio and skipped legs as the hook prints them. B 53rd's: `12/15 legs ran, 3 SKIPPED`, with legs 3, 4 and 8 "local stack not up". Legs 6 and 7 must be among those that RAN; quote their lines. **No `--no-verify`.** A leg that stops you is a question: mail it.
- **KS-530 is already In Progress.** Creating the PR may touch it through the GitHub integration. **Report any movement; do not revert it; issue no state mutation.**
- **No ticket comment on KS-530 or KS-528.**

## ITEM 2 IN DETAIL (ONE READY, HOLD, merge, verify)
- **ONE READY:** `READY FOR QA (Seat B 54th): #<n> (KS-530) …`, per STANDING_LINES `:17-:47`. It includes:
  - the PR number, with its HEAD read from origin in the same action;
  - the evidence of ITEM 1 steps 1-9 and the NOT COVERED;
  - the per-lock delta table and the no-collateral proof;
  - the red-first control and the pristine regen control;
  - Q3's before/after table;
  - the trailer proof and its control;
  - **the PREDICTED END_TREE:** `git merge-tree --write-tree ea6fcecc3a6f <head>` (expect your head's own tree if develop has not moved). Note that `--write-tree` writes objects into the shared store and moves no ref.
  - the fuse recomputed, **and the cohort after the merge: 3 rows → 2** (the react-router pair, KS 528).

  **The PR goes to ONE gate, gate53, T1. Wednesday drafts it.**
- 🔴 **A mailed figure is computed in the SAME tool call that sends the mail.** The tool shell does not persist env between calls.
- 🔴 **Read every send's response. A 400 means nothing was sent; say so.** Use placeholder substitution, never an f-string, for prose with braces. A fuse guard must not be tied to one word order (B 53rd §8.6).
- HOLD with the watcher armed. **Merge only on a signed GO whose subject names Seat B 54th** (`GO (Seat B 54th): merge <n> on gate53`), after listing the inbox by API.
- **Build `build_addendum49_<n>.py` from YOUR GO's measured line**, starting from the parked `templates/build_addendum48_1367.py` (a single-PR GO) and re-keying its pinned values BY HAND. **A GO's clause shape is per-GO.** Never reuse the last GO's parser. Emit `no_trailer` when the GO says NO TRAILER.
- Run `merge49.py` **dry first.** Read the `.DRY` body: 0 `Co-Authored-By`.
  - If the GO's key set differs from the PR body's `Refs` lines, fix it by editing the PR BODY (not a commit), with the head SHA proved identical before and after.
  - 🔴 **OMIT `--prev-tree`.** This is a single-PR merge (B 52nd §C.1: passed on a single PR, it stops rc 3).
  - **`merged_blob_paths` is NOT needed.** That field is for two PRs of one batch touching one file (B 53rd §C.1).
  - If develop moved after the gate read it, **STOP and mail**. If GitHub reports `mergeable: false` or demands an update, **STOP and mail. Rebase nothing without Wednesday.**
- **Merge,** then read develop back by `ls-remote` AND the commits API, and prove the landed tree == the GO's END_TREE.
  - **The squash's objects will not be in the local store** (created at origin; B 53rd §C.2). Read the landed tree via the REST API. **A fetch to read it locally needs a fresh ruling.**
- **The squash subject and body come from the GO**, never pasted from the PR. The declared subject carries NO `(#n)`. The landed length is measured as the string GitHub WROTE.
- **After the merge:** read the landed message's trailers. **0 `Co-Authored-By` is the expectation.** If one landed anyway, report it with its source. Do not try to remedy it (that is history rewriting).
- **Verify after merge:** at the landed tree, `audit-baseline.json` has 24 rows and no frvp; the 2026-10-09 cohort is **2 rows** (wrjc, 337j); the override line is present; the nested `@prisma/dev/node_modules/@hono/node-server` entry is absent (or ≥1.19.15) in the root lock.
- `mergeable_state` may read `unstable`. The PAT 403s on `/status`, `/check-runs` and `/check-suites`; `/rules/branches/develop` shows `deletion`, `non_fast_forward`, `pull_request` and NO `required_status_checks` (B 53rd §10). Report it. It is not a testing claim.
- Then STATUS, handover, and WRAP cold.

## CARRY (list, do not act)
- 🔴 **THE BOOT PULL.** B 53rd was the FIRST seat to REFUSE the launcher's step-1 pull (handover §1 `:17-:30`), after six seats in a row had their checkout fast-forwarded before reading the countermand.
  - The cause is ORDERING. With no other live seat, `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/Launch_Claude.command` (mtime 2026-09-22 18:14, unchanged) tells the seat to "pull latest on the current branch" if safe. The countermand can only sit in a brief the seat reads after that step.
  - **If you read this before pulling, do not pull.** If the launcher already pulled, **disclose it with the reflog lines and do not reset.** The launcher fix is Kam's call, not yours.
  - Also refuse:
    - the SessionStart `POST /api/seen` (`EXTRANET_ME=kam`: it clears **Kam's** flags);
    - "CC Kam on every email";
    - rule 7's extranet to-do.
- **OUT of this seat:**
  - the react-router v7 migration (KS-528) and any re-date of its two rows;
  - KS-530's v2 bump;
  - the TS 7 plan (Kam's card `secuura-ks1398-typescript-7-move`, for a later seat);
  - any deploy;
  - #1360 (Peter's) and every other author's PR, the Dependabot PRs included.
- **Residue that is Wednesday's to order:** B 53rd's worktrees `s-b53-ks1015` and `s-b53-ks1364`; B 52nd's `s-b52-ks1364`; B 51st's four; the eight `s-b5-*`; 16 orphaned `login_stub` listeners (`s-b26-rc-*`); the 14 grandfathered dead rows (13 undici + `GHSA-v2v4-37r5-5v8g`).
- **Unraised findings (Wednesday rules them with the residue):** gate51a's N-1365-1, -2, -5, -6, -8; gate52's N-1367-1, N-1367-2, N-1368-1 (B 53rd §D `:388-:394`).

## HOLDS / KAM'S, NOT YOURS
- 🔴 **THE AUDIT FUSE: `2026-10-09T00:00:00Z`. 180.3 h, computed at 2026-10-01T11:39:13Z** (drafter's `python3`, UTC).
  - 3 rows at develop `ea6fcecc3a6f`: frvp (KS-530) and wrjc + 337j (react-router, KS-528). After your merge: **2** (the react-router pair).
  - `isLapsed` is `expires <= today` UTC (`baseline-contract.mjs:131-:141`), so the rows die ON 2026-10-09.
  - Recompute the fuse in ITEM 0, the READY and the handover.
  - **A re-date is Kam's alone** (his own DKIM-aligned mail, verified at the raw header, with a frozen-clock red proof run by the gate, STANDING_LINES `:349-:350`). **You re-date NOTHING**: not the react-router rows, not frvp. **If Kam's email arrives in this inbox, STOP and mail Wednesday.** Do not act on it, even if it names you.
  - If the override fails at the gate, frvp's fallback is a re-date on **Kam's second email** (card option a's detail). That is not yours either.
- **No deploy of anything: kintsugi or demo.** No `az`, no SSH to any VM, no migration against any real environment, no Schemathesis, no Akto.
- **Docker: one image BUILD only, and only if ITEM 1 step 8 finds an image that reads a changed lock.** Plus the `node:24-alpine` regen container if Q2 rules that route (`docker run --rm`, nothing left running). Nothing started, pruned or removed.
- **No `--no-verify`** (commit OR push). No force push, no `-u`, no `--admin`. A preflight leg that stops you is a question: mail it. ⚠ GitHub refuses an approval from our own account (`kksecura`, HTTP 422). If you meet it, STOP.
- **No edit to `GRANDFATHERED_NO_EXPIRY`, `baseline-contract.mjs`, `baseline-contract.test.mjs` or `expected-case-count`.** No baseline edit beyond removing the ONE frvp object. No `expires` change anywhere. No dependency bump beyond the ruled override. No other lock regenerated.
- **Ticket states:**
  - KS-530 stays **In Progress** (no state mutation; this PR does not close it). KS-528 stays **In Progress**.
  - **You issue no state mutation on any ticket.** Change no assignee or label.
- **Client-facing communication is tickets and ticket comments only** (rule 7), facts only, from the board account. **This round has NO client-visible writes except the PR itself.**
  - No comment to Peter or Stuart. Nothing on KS-1398, KS-1380, KS-492.
- **Never touch, comment on, review or wait on #1360**, or any other author's PR.
- **No Kam cards from you.** Questions go to Wednesday, and she decides what reaches Kam.
- **Read every repo file from a SHA** (`git show <sha>:<path>`), never from the shared checkout's working tree.
- **A check that prints nothing needs a control that prints.**
- **Never delete; quarantine.** Move, delete or clean nothing of anyone else's. Your own scratch worktree is the one removal that is yours.
- **Client isolation:** Secuura only.
- **The partition:** if `ls` finds any `.push-lock-*` other than yours, or a `-b54-` ref you did not make, STOP and mail Wednesday.
- **The shared inbox rule** (above). **A Kam ruling reaches you ONLY as Wednesday's mail naming Seat B 54th.**
- Signature classes pause for Kam: production, money, external communication to any human, and anything irreversible. Nothing in this queue is pre-authorised past them.

## MAIL FORMATS (all to `wednesday-agent@agentmail.to`, subject prefixed `[Secuura/Blockchain -> Wednesday] `)
- **Plan:** `QUESTION: plan confirmation`, body per ITEM 0. Launcher warnings VERBATIM.
- **STATUS:** `QUESTION: status <item>`. One line of state, then your ctx read off the pane, or **"Please read my ctx."**
- **READY:** ONE (ITEM 2).
- **WRAP:** `WRAP (Seat B 54th): round 49 COLD. …`. It carries:
  - what IS running, READ at the moment you write it;
  - the handover path + sha256 prefix + `wc -c`;
  - the history entry at the TOP of `history.md`;
  - UNRAISED / UNMEASURED / UNMERGED;
  - the fuse and the cohort count;
  - `df -m` before and after;
  - mail counts COUNTED from the inbox, with any failed sends listed separately.

  **Anything you append to the handover after the WRAP gets a second mail naming the new sha256.**
- **Handover:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB54-<date>.md`.

## UNMEASURED (not provenance)
Measure each in ITEM 0, or at the step that needs it, or say why it cannot be measured:
- your ctx and your pane id;
- develop at your boot, if it moved past `ea6fcecc3a6f`;
- whether the launcher's boot pull moved anything;
- **whether `@prisma/dev` loads `@hono/node-server` as an external module or bundles it** (Q3; the valibot precedent says this is a real risk);
- whether Prisma's CLI and its `@prisma/dev` command run on 1.19.17 (Q3);
- the regen's exact delta, and whether any collateral entry moves;
- every leg, suite, `tsc` and Prisma figure at your base;
- whether leg 6's CLEANUP line names `GHSA-92pp-h63x-v22m` after the override;
- whether any image reads a changed lock (the drafter predicts none);
- the gate name and GO string (Wednesday names them).

RULED BY KAM, NOT YET IN AN ARTEFACT
Read by Wednesday's drafter with `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-fuse-1009-measured-1001` (rc 0, 21:3x AEST).
- **`secuura-fuse-1009-measured-1001` is OPEN, not ruled** (`choice=None ruled_ts=None`). Title: "Audit fuse Fri 9 Oct: fix one row now, re-date the two react-router rows by your email". Recommended (a): fix frvp now by an override, and re-date ONLY the two react-router rows to Sat 31 Oct by his email. **Default:** *"Nothing is re-dated (that is your signature, never Wednesday's). Wednesday has the frvp override built and gated anyway, since it is a real fix inside our merge grant. Wednesday reminds you on the board on Mon 5 Oct. With no email, the react-router rows freeze pushes on Fri 9 Oct 10:00 AEST."*
- **Your ITEM 1 is the default's "built and gated anyway".** If Kam rules (b) or (c) before your merge, Wednesday relays it by name. Until then, the default stands.
- Context, not yours to deliver: `secuura-ks1380-peter-reverting-1358` => **b** (Kam talks to Peter; leave #1360 alone); `secuura-ks1398-typescript-7-move` => **b**, plan it now (a later seat).

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **This seat's queue (Wednesday, 2026-10-01 evening):** ITEM 0 plan with Q1-Q5; ONE PR, the frvp override, T1, `Refs KS-530`; ONE READY, gate53, merge on its GO. **Hard line 70%.**
- **No attribution, on the branch commit AND in the squash body** (STANDING above). The record's earlier "GitHub harvests trailers" mechanism is WITHDRAWN: the measured source was the merge tool.
- **A gate that trips on the INSTRUMENT is fixed, re-proved and resumed. A gate that trips on a READING is a STOP and a mail.**
- **Measure before the READY. Any red that is not red at develop is a STOP.**
- **A lock diff that moves anything beyond `@hono/node-server` is a STOP and a mail**, whatever npm's banner says.
- **The GO composes squash subjects and bodies.** Never paste a PR body. Declared squash subjects carry NO `(#n)`. The landed length is ≤ 92, measured as the string GitHub WROTE.
- **A hyphenated foreign key in a PR title, body, branch or commit message ATTACHES that ticket: de-hyphenate every key but the PR's own.** In a ticket COMMENT or description, a hyphenated key only cross-references.
- **A ticket that moves itself on PR creation is reported, not reverted.**
- **`ls-remote` at boot is acceptable. The fetch stays refused except as Wednesday rules Q1.**
- Merge only on a signed GO whose subject names Seat B 54th.

VERIFIED BEFORE SENDING (Wednesday's drafter, 2026-10-01)
PROVENANCE:
- seat number: history.md newest entry Seat B 53rd at :24 (next Seat B 52nd :80); bounded "b 54th" 0 and "\bb54\b" 0, control "b 53rd" 1; raw b54 8, all in hex (b54d762d1a90, d3b570ab9b54, bf766bb54, 1be43b54, 58a90b54, b54487216); no seatB-54th folder, no HANDOVER-seatB54 | /usr/bin/grep -n '^## ' and /usr/bin/grep -oiE over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md + ls /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History | read 2026-10-01 21:37
- develop at origin ea6fcecc3a6f71a4f397ea678da54a06df130cd7; b53 branches ac3ceee7f440 and 2a3dcd912a33 present; KS-530 branches feature/ks-530-audit-baseline-redate-b44-1 9199a2f9f739 and feature/ks-530-hononode-server-v1-v2-major-bump-ghsa-frvp-originate-mcp-r21-patchline-1 f2751859c015; no -b54- ref | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop 'refs/heads/*b53*' 'refs/heads/*b54*' 'refs/heads/feature/ks-530*'` rc 0 (a read) | read 2026-10-01 21:31:57 (11:31:57Z)
- ea6fcecc3a6f ABSENT locally (cat-file rc 128); HEAD and develop c56dd7c32edf, origin/develop ed268a995a88 (reflog "2026-10-01 21:15:15 +1000 fetch --no-tags origin refs/heads/develop:refs/remotes/origin/develop: fast-forward"); FETCH_HEAD TZ=UTC 2026-10-01T11:15:15Z; .git/config sha256 4f624a213933d54b; tracked-modified 0, untracked 17; 0 .push-lock-*; .git/worktrees 482; worktrees s-b5-* (8), s-b51-* (4), s-b52-ks1364, s-b53-ks1015, s-b53-ks1364 present | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files rev-parse / cat-file -t / reflog -1 / status --porcelain` + TZ=UTC stat + shasum + ls -a /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees (read verbs only) | read 2026-10-01 21:39
- ea6fcecc3a6f: tree 48f5f8afa6ef1f03f2d64e4afa24fd9f75213ad7, single parent ed268a995a88; tree 4877 entries (not truncated) | `GET https://api.github.com/repos/Secuura/Distributed_Secuura/commits/ea6fcecc3a6f71a4f397ea678da54a06df130cd7` + `/git/trees/ea6fcecc…?recursive=1` (GH_TOKEN read by name from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env, never printed) | read 2026-10-01 21:33
- at ea6fcecc3a6f (blobs via `/git/blobs/<sha>`): Blockchain/Dev/package.json d22c14e6c370, overrides :77-:93 with "undici": "^7.29.1" at :89 and jsdom-scoped undici :90-:92, "// overrides KS-493" note :76 (valibot bundled by @prisma/dev, override inert), scripts audit:locks :45, audit:contract :46, audit:gate :47, workspaces packages/* services/* frontend/*; frontend/issuer/package.json dc17eeef957e "undici" override :68 and jsdom-scoped :70; services/originate/package.json 930fa8afb9ff: prisma ^7.8.0 devDependencies :46, @prisma/client and @prisma/adapter-pg dependencies :18-:19, overrides :51-:61 with "@hono/node-server": "^1.19.15" at :60 | python json + /usr/bin/grep -n over the downloaded blobs in /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/79817561-2a8e-42cd-8745-2ef3ab0b0516/scratchpad/b54/f/ | read 2026-10-01 21:35
- the 45 package-lock.json at ea6fcecc3a6f, all parsed: only Blockchain/Dev/package-lock.json (blob c8cf17aa62a5, 674706 B, 1968 entries) has node_modules/@prisma/dev 0.24.3 devOptional (:7617, declares "@hono/node-server": "1.19.11") and node_modules/@prisma/dev/node_modules/@hono/node-server 1.19.11 devOptional (:7641), hoisted node_modules/@hono/node-server 1.19.17 peer hono ^4 (:5931), node_modules/hono 4.13.8 (:14878), @modelcontextprotocol/sdk 1.29.0 asks ^1.19.9; sole parent of @prisma/dev is services/originate/node_modules/prisma 7.8.0 devOptional; services/mcp-server/package-lock.json (ec20749768f0) @hono/node-server 1.19.17 only; services/originate/package-lock.json (3e088e4e1855) prisma 7.10.0, @prisma/dev 0.24.17 with NO @hono/node-server or hono dependency and no hono entry at all; the other 42 locks: neither package | python json walk over /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/79817561-2a8e-42cd-8745-2ef3ab0b0516/scratchpad/b54/locks/ and /usr/bin/grep -n | read 2026-10-01 21:36
- images: 37 Dockerfiles at ea6fcecc3a6f; none COPYs the workspace-root lock; services/originate/Dockerfile copies services/originate/package*.json (:28) then npm ci --ignore-scripts (:30), npx prisma generate (:38), no other Dockerfile mentions prisma; services/mcp-server/Dockerfile copies its own package.json + package-lock.json (:28, :56) | /usr/bin/grep -niE '^copy .*package|prisma' over the downloaded Dockerfiles | read 2026-10-01 21:35
- audit at ea6fcecc3a6f: audit-baseline.json blob 4e5f5daba207, 161 lines, 25 accepted, 7 dated (10-09: frvp, wrjc, 337j; 10-15: 73wf, c83g, w9m9; 10-31: ggr8); GHSA-frvp-7c67-39w9 at :88, @hono/node-server, KS-530, expires 2026-10-09, reason "fix is >=2.0.5 only, a semver-MAJOR v1->v2 bump…"; GHSA-92pp-h63x-v22m at :76 (@hono/node-server, no expiry); baseline-contract.mjs ef82d7c5211d: "The 18 entries" :44, GRANDFATHERED_NO_EXPIRY :58-:77 (18 ids incl. GHSA-92pp at :65, frvp absent), isLapsed :131-:141 (expires <= today); baseline-contract.test.mjs 2379c0aeee6e: floor "> 20" :217, no-expiry set == GRANDFATHERED :220-:231; audit-locks.mjs :299 filters scope === 'standalone-locks'; audit-gate.mjs CLEANUP line :210 | python json + /usr/bin/grep -n + sed -n over the downloaded blobs | read 2026-10-01 21:36
- #1355 (KS-1378): "KS-1378: undici 7.30.0 in both locks, js-yaml 5.4.2 in systemTest performance", merged 2026-09-30T02:52:21Z, merge 3e3a68260d0e, branch feature/ks-1378-undici-override-and-jsyaml-542-b48-1, base 37205947ddd2; 5 files (+14/-63): Dev/package.json +1 (overrides hunk @@ -86,6 +86,7), Dev/package-lock.json +5/-34, frontend/issuer/package.json +1, frontend/issuer/package-lock.json +4/-26, systemTest/performance/package-lock.json +3/-3; body: node:24-alpine npm 11.19.0 node v24.21.0; issuer lock `npm install --package-lock-only --ignore-scripts`; root lock Blockchain/Dev mounted (32 file: link entries, EMISSINGTARGET KS 1394), `npm update undici --package-lock-only --ignore-scripts` (install left 5.29.0); npm printed "up to date" even when rewriting; pristine control tree did not move; per-lock delta 3 entries (undici 5.29.0->7.30.0, @fastify/busboy removed, jsdom/node_modules/undici removed deduped), issuer 723->721, root 1970->1968; root also 12 dev-flag bookkeeping entries (11 lightningcss-*, magicast) set-equal to the control's; "No baseline row. No GRANDFATHERED_NO_EXPIRY entry touched"; leg 6 CLEANUP quoted, NONE removed; contract/leg 6/leg 7 rc 0 at head; issuer image build rc 0; preflight 12/15, legs 3,4,8 skipped; branch commit 6fab9c0936d4 ends "Co-Authored-By: Claude Opus 5" | `GET /repos/Secuura/Distributed_Secuura/pulls/1355`, `/pulls/1355/files`, `/pulls/1355/commits`, and the v3.diff media type, saved under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/79817561-2a8e-42cd-8745-2ef3ab0b0516/scratchpad/b54/ | read 2026-10-01 21:32
- #1364 (KS-729): "KS-729: remove the dead mwp4 baseline row, correct r53p's reason and the count", merged 2026-10-01T01:07:28Z as c56dd7c32edf; 2 files: audit-baseline.json +1/-8, baseline-contract.mjs +1/-1 ("The 17 entries" -> "The 18 entries"); rows 26 -> 25, cohort 4 -> 3, GRANDFATHERED byte-equal, contract floor not lowered, expected-case-count and baseline-contract.test.mjs untouched; leg 7 CLEANUP blind by construction (audit-locks.mjs:299) | `GET /repos/Secuura/Distributed_Secuura/pulls/1364` + `/pulls/1364/files` | read 2026-10-01 21:37
- open PRs 21; touching Blockchain/Dev/package.json or package-lock.json: #1360 PeterObeden (KS-1380 revert, head d0e99f181a4e, 15 lock files, root lock +2/-6, no "hono"/"prisma" text in its patch), #920 kksecura (package.json), dependabot #949 #948 #947 #946 #945 #649 #639 #635 #575 #572; 0 touch audit-baseline.json or baseline-contract.mjs; control #1355 files hit 2 | `GET /repos/Secuura/Distributed_Secuura/pulls?state=open&per_page=100` + `/pulls/<n>/files` per PR | read 2026-10-01 21:38
- Kam's card: `secuura-fuse-1009-measured-1001` status open (Secuura/Blockchain), choice=None ruled_ts=None, options a (recommended) / b / c, default text as quoted | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-fuse-1009-measured-1001` rc 0 | read 2026-10-01 21:31
- B 53rd handover 403 lines 34421 B sha256 e01335d2b2c5d715, read whole: §1 boot pull refused (:17-:30), §2 Q4 + Q1(b) (:32-:46), §3 tools 22 live + quarantine + trap 4 18th + matcher truncation 110 chars + KeyError SINCE (:48-:110), §7 frvp measured, reason wrong, 1.19.11 pinned exactly by @prisma/dev 0.24.3 (:201-:223), §8 findings incl. push48 self-deadlock (:245-:251), §9 merge steps (:253-:279), §10 trailer proofs 53 B control, rules API (:281-:292), §A merged ed268a995a88 / ea6fcecc3a6f, 0 Co-Authored-By (:331-:346), §B trailer source merge48.py :391/:402 (:348-:361), §C four instrument faults (:363-:386), §D open (:388-:403) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB53-2026-10-01.md | read 2026-10-01 21:30
- B 53rd's tools: 24 files match 48(_[0-9a-z]+)?\.(py|sh)$ in raise/ (as listed), inert/one_merge46.sh, templates/ 5 files; 120 distinct tokens containing "48"; raw b54 0, bounded \bb54\b 0, bounded \bb53\b 27, raw b53 49, bounded \b49\b 5 (gatelines48.py:17, :32; gatelinesproof48.sh:37, :44; push48.sh:131); merge48.py sha256 e29ccb158bb1daf9: SIGN :391, no_trailer verbatim-branch suppression :413-:421, composed branch :429-:434 appends SIGN unconditionally; build_addendum48_1368.py emits "no_trailer": True (:188); push48.sh lock48 take :121 release :146; inbox_match48.py MINE "b 53rd" :93 | ls + shasum + /usr/bin/grep -oE / -noE / sed -n over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-01_seatB-53rd/raise | read 2026-10-01 21:41
- real AgentMail subjects in secuura-blockchain@agentmail.to: "LAUNCH BRIEF (Seat B 53rd): KS-1015 + KS-1364 residue raise, fuse measurement" 08:16:43Z; "GO (Seat B 53rd): merge 1367 1368 on gate52" 10:59:24Z; WRAP (Seat B 53rd) 11:28:51Z | `GET https://api.agentmail.to/v0/inboxes/secuura-blockchain@agentmail.to/messages?limit=100` (AGENTMAIL_API_KEY read by name from /Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env, never printed) | read 2026-10-01 21:40
- STANDING_LINES 377 lines 50667 B sha256 eb73f978f133dc4c mtime 2026-10-01 21:30:50 local; new sections :370-:371 (merge tool must not add attribution; check the SENT body), :373-:374 (push<N>.sh takes the lock itself), :376-:377 (build packages/shared before the first test) | wc + shasum + stat + /usr/bin/grep -n '^## ' + sed -n 368,377p of /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md | read 2026-10-01 21:30
- Linear read-only: KS-530 In Progress, assignee board account, title "@hono/node-server v1->v2 major bump (GHSA-frvp) - originate + mcp-server runtime", updated 2026-09-29T07:02:57Z, newest comment 2026-08-14T01:59:32Z; KS-528 In Progress, board account, "Frontends: react-router v6 → v7 migration…", updated 2026-09-29T07:02:58Z, newest comment 2026-08-14T01:59:31Z | Linear GraphQL `issue(id:)`, no mutation (LINEAR_API_KEY read by name from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env, never printed) | read 2026-10-01 21:38
- usage 93% >= 90%, usage_gate REFUSED rc 3, gauge age 9 min; authority = EXPIRING-GRANTS top row (Kam live board 2026-10-01 17:40:22, verbatim as quoted, EVENT ends at the account switch Fri 2026-10-02) | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check` + /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md :9 | read 2026-10-01 21:39
- registry: @hono/node-server 1.19.17 peerDependencies hono ^4, engines node >=18.14.1; @prisma/dev@0.24.3 dependency @hono/node-server 1.19.11; published 1.19.13, 1.19.14, 1.19.15, 1.19.17 (newest four 1.19.x); host npm 11.5.1, node v24.7.0 | `npm view` (reads) + `npm -v` + `node -v` | read 2026-10-01 21:37
- floor %0 and %1 only (no Secuura seat live); DevMASTER 474995 MiB free | `tmux list-panes -a` + `df -m /Volumes/DevMASTER` | read 2026-10-01 21:37
- fuse 180.3 h computed at 2026-10-01T11:39:13Z | python3 UTC arithmetic against 2026-10-09T00:00Z | read 2026-10-01 21:39
- template: structure, standing sections, matcher/namespace shape, PROVENANCE + SELF-CHECK | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-01_seatB53_raise.md (463 lines, 64698 B) read whole | read 2026-10-01 21:29
- this brief's hex runs: checked for b54 / b53 / d1 inside hex; result recorded in the SELF-CHECK line | /usr/bin/grep -oE '\b[0-9a-f]{7,64}\b' over this file | read 2026-10-01 21:45

Re-read record: the drafter read the brief end to end against the PROVENANCE block. It checked the develop figures (BLUF, Q1, ITEM 1 step 1), the single-PR merge shape (no `--prev-tree`, no `merged_blob_paths`), the 70% line (BLUF, RULED BY WEDNESDAY), the ITEM numbering (QUEUE vs details), that the trailer mechanism is stated as the TOOL's append (the earlier "harvest" wording is withdrawn), that push49.sh is called bare everywhere, that "no state mutation" and "no re-date" hold in every section, and that every QUEUE ticket has a provenance line.
SELF-CHECK: re-read end-to-end for contradictions | 2026-10-01 21:45
