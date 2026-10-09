LAUNCH BRIEF (Seat R 22nd): successor of Seat R 21st on pane `Secuura/Blockchain-R`. **A MERGE SEAT for ONE PR: #1427 (KS-1274, the trivy bare-object guard). It finishes gate76 STEP 2, which R 21st built and could not push.** You re-predict and rebuild the docs-only keep-both MERGE-IN M' of the NEW develop into #1427's branch. You push M' BARE through the hook, then do ONE API squash on GO 2. Nothing deploys. Secuura NEVER force-pushes. **This seat pushes exactly ONE thing: M', on `feature/ks-1274-trivy-bare-object-guard-ra18-1`.** cloud: merge (carrying 0 Spark tasks). **No raise work.**


## SEND AMENDMENT (Wednesday, at send __:__:__Z): this block WINS where it differs from the text below
- develop at send = `________________________________________` (Wednesday's `env -u GIT_SSH_COMMAND git -C <checkout> ls-remote origin`, __:__Z). Drafter's read: `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6` (ls-remote 2026-10-09T02:47:17Z). **If it moved, the M-1 prediction below is VOID.** Re-run it before send, or say so here.
- `refs/pull/1427/head` at send = `________________________________________` (drafter: `2b6da5f561b05a820bbe1ab5e891bff9f4f531c8`, the same read; the branch ref is the same SHA).
- Live floor (`tmux list-panes`, __:__ local): `%0 wednesday` · `%1 fleet-monitor` · ____ . YOU are a new pane on `Secuura/Blockchain-R`. Read your own id with `$TMUX_PANE`, never with a bare `tmux display`.
- Sole live Secuura session at launch? ____ . This decides whether your launcher's boot pull runs (ITEM 0).
- Usage at send: ____% (`usage_gate.sh --check`). The drafter did NOT read it.
- **MODEL:** the launcher pins **`claude-opus-5`** (`Launch_Claude.command:664`, `exec claude --dangerously-skip-permissions --model claude-opus-5`; drafter `grep -n`). Wednesday types **`/model claude-opus-5-5`** into your pane **at its IDLE prompt** and confirms by mail. R 21st measured that a tap sent while you are mid-turn arrives as a message and does NOT switch (handover :8-9; plan mail :8-9). Put one line `MODEL: <as your session reports it>` in every STATUS / WRAP mail.
- Rulings on the drafter's questions (Q-START22, Q-WT22, Q-DEVPATHS22, Q-MSUBJ22, Q-PRED22, Q-OBJ22, Q-LEGS67, Q-MATCH22, Q-ORDER1436): ____ .
- Wednesday's pane is `%0`. Send all mail to `wednesday-agent@agentmail.to`.

# LAUNCH BRIEF: Seat R 22nd, Secuura/Blockchain, lane R (pane `Secuura/Blockchain-R`). From Wednesday.
DRAFT: staged by Wednesday's brief-drafting sub-agent on 2026-10-09, ~13:30-13:55 AEDT (02:30Z-02:55Z). NOT sent, NOT launched. Every value carries its instrument. Every value marked **(drafter)** is a reading the drafter made in its own scratchpad or with read verbs, and **you RE-MEASURE it**.

## BLUF
- **Seat number, derived and not counted:** R 21st's handover opens with "FOR R 22nd, THE FIRST THREE THINGS" (`5_Project_History/HANDOVER-seatR21-2026-10-09.md`, **130 lines, sha256/16 `216792ecad1622ef`**). Drafter used `shasum -a 256` and `wc -l`; both equal R 21st's WRAP mail :54. Read it WHOLE at source, before anything else.
- **Why you exist:** R 21st built M = `dedc861c04a548cffb708ac88e7cd3c17208cdb7` on develop D1 `1e7f90e26137`. Its own gates read `52 gates CHECKED, 52 passed, 0 failed`, qm was 8/8, and P2 was green. **Its push was REFUSED at preflight legs 6 and 7** by three handlebars advisories, two of them CRITICAL (handover :3-7, :117-125). **M is a RECORD ONLY.** No ref names it, and nothing you do names it either.
- **What moved:** lane V landed the in-range lock refresh. develop is now **D2 = `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6`**, the squash of #1435 (KS-1452, "in-range lock refresh clears three handlebars advisories", by kksecura 2026-10-09T13:13:52+11:00). It has ONE parent, `1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0` (D1), and tree `ccbb76460ad6…`. Ancestry D1 -> D2 is rc 0; the reverse control is rc 1 (drafter `merge-base --is-ancestor` both ways; `%P` word count 1).
- **D1..D2 = 5 paths, all `package-lock.json`, +18/-18** (drafter `git diff --raw --numstat 1e7f90e2… 81d2e5f4…`, read verbs on the shared checkout): `Blockchain/Dev/package-lock.json` 2/2, and `Blockchain/Dev/services/{governance,originate,referral,vc-issuer}/package-lock.json` 4/4 each. **The overlap with #1427's 6 paths (base..head) is 0** (drafter `comm -12` of the two `diff --name-only` lists; the control, head paths vs base..D1, returns exactly the two docs). The two docs' blobs are UNCHANGED from D1 to D2: flow `6c2038c3778f…` and cheat `c3de14c08d56…` at both (drafter `ls-tree`). **Wednesday's ruling therefore applies: a lockfile-only move is a RE-PREDICT, not a RE-GATE** (R 21st's `ANSWER_refused` ruling 1; handover :13-22). The STOP condition stands in full: **if YOUR M-1 shows any conflict outside the two `Projects Documents/` docs, or a moved path of #1427 or #1428, STOP and mail. That is a RE-GATE.**
- **THE MERGE-IN, RE-PREDICTED ON D2 BY THE DRAFTER WITH TWO INSTRUMENTS** (in a private bare repo in the drafter's scratchpad whose `objects/info/alternates` points at the shared store, so no verb touched `!CODING`):
  - **Instrument 1:** `c4_docs_gate76.py chain --repo <drafter bare repo> --order 1427 --develop 81d2e5f4c415… --heads 1427=2b6da5f561b0…,1428=64eafead891e…` returned **rc 0, ALL OK**. Tree **`e948c77b8b464f347a6af5abc515490de782ead6`**. Flow blob **`b2bd07dbae400c0ad15b89046a65967a117e1a15`** and cheat blob **`f4503e99d43e8a90ffe881291295695e7cd61ae1`**, which are **the SAME composed blobs as the kit**: `cmp` against `gatesets/2026-10-08_gate76/composed_2026-10-08/2_1427_composed_{flow,cheat}_doc.html` gives rc 0 for both, and the control (flow vs the kit's cheat) gives rc 1. Guard rc 0 at 12/0, which is NOT tag-balance evidence. Read-backs OK on both docs, with tag balance `()` == develop. FINAL-flow / FINAL-cheat / FINAL-CODE all True. The merge-tree cross-check returned rc 1 with "outside the docs differing: []" and was never picked. `--union` DIFFERS on FLOW: 3862 vs 3863 lines, with table, td and tr each one open tag unbalanced. That reproduces the hazard. chain.json sha256/16 `0a9b940800d1fc38`.
  - **Instrument 2:** `git merge-tree --write-tree --name-only D2 head` returned **rc 1, with conflicts on EXACTLY the two docs** and tree `d232875f8bf6…`. Substituting the two composed blobs with `update-index --cacheinfo` in a private `GIT_INDEX_FILE`, then running `write-tree`, gives **`e948c77b8b464f347a6af5abc515490de782ead6`**, the same tree. **CONTROL, the same construction on D1:** merge-tree `49dd3048cdfd…` gives `57c9b5eaec95…`, which is R 21st's T' exactly, so the instrument reproduces the known answer.
  - **So T'' (the M' tree AND the squash tree) = `e948c77b8b464f347a6af5abc515490de782ead6` (drafter).** Expect it to differ from R 21st's T' `57c9b5eaec95…` in exactly the 5 lock files (drafter `diff --name-only 57c9b5ea e948c77b` = those 5).
  - **D2..T'' = 6 paths, +94/-8**, modes {100644: 5, 100755: 1}. `Blockchain/Testing/jobs/04-container-trivy.sh` stays 100755, with blob `77ad59c5e…`. This is the same set as D1..T'.
  - **head..T'' (the push delta OURS..M') = 14 paths, +439/-22, 12 of them under `Blockchain/Dev/`**, so the FULL preflight runs in-hook. That compares with R 21st's 9 paths and 7 under `Blockchain/Dev/`; the +5 are the locks (drafter `diff --shortstat`).
- **D2's objects are PRESENT in the shared store.** `cat-file -t 81d2e5f4…` returned `commit`, and the NEGATIVE control `deadbeef…` returned "could not get object info" (drafter, same command). The commission records that F 6th made the transfer at 02:28Z; the drafter did not read F 6th's record of it. **No M-2(i) transfer is expected (Q-OBJ22).**
- **Neither ticket moves to Done** (§5f; RULINGS Q-LIVE76: a live trivy scan is OWED). No ticket comment. Wednesday sends the notifications in a batch (Q-NOTIFY12).
- **Budget by MAIL HANDSHAKE:** send `QUESTION: ctx read (Seat R 22nd)` before M-3 and again before the squash. HARD CEILING 65% ctx: WRAP COLD at the next safe boundary and name what you hold. **A merge-in that is started and not pushed is the one state that must not be left for a successor.**
- **Never end a turn on a "next up" line with nothing running** (STANDING_LINES :342-345).

**THE SEQUENCE, in order. Nothing writes before step 4.**
1. **Re-key the R tools** (TOOLS below). 🔴 **The generic clause comes FIRST and binds: re-key every lane-bearing declaration, including LOCK_SEAT defaults, env prefixes and fixtures. Where the tool and this brief disagree, the tool wins.** Every list after that clause is an EXPECTATION.
2. **M-1, the re-prediction on develop `81d2e5f4c415`, with TWO instruments, in YOUR clone.**
3. **The plan mail** (`QUESTION: plan confirmation (Seat R 22nd)`) together with `STATUS: re-prediction on <12-hex> (Seat R 22nd)`. **Then HOLD.**
4. **On Wednesday's word (the literal `START STEP 2 (Seat R 22nd)`, Q-START22):** add the worktree, build M' (`mergeinra22_gate76.sh`), run qm, run P2 on the real M', then push M' BARE (`pushra1_ff.sh`, which takes and releases `.push-lock-d8` itself).
5. **`STATUS: merge-in 1427 pushed (Seat R 22nd)`**, with the push's gate lines VERBATIM and the Actions classified by workflow PATH.
6. **GO 2, plus the SEPARATE ADDENDUM**, both from Wednesday. The subjects must match EXACTLY (THE GO below).
7. **The squash, pinned to M'.**
8. **Verify at source** (X-6).
9. **WRAP.**

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** 🔴 **Where your copy of a tool and this brief disagree about a gate, a knob, a path or a line number, THE TOOL WINS.** Run nothing on the disputed point; tell Wednesday what the tool says.

**WAKE:** your re-keyed `inbox_watchra1.sh` (`WATCHRA22_*`), armed in the background at boot with `timeout: 7200000`. It EXITS when it fires, so re-arm it IN THE SAME ACTION that reads each mail, with `SINCE` = the newest mail you have READ (STANDING_LINES :403). After the push and after the squash, LIST the inbox by API before the next ref write. Name a watcher pid only from a `ps` FILE read immediately before. Stop every watcher before WRAP and prove 0 are live, with a positive control.

## FOR R 22nd, THE FIRST THREE THINGS (from R 21st's handover :11-76; it is AUTHORITATIVE, so read them THERE, whole)
1. 🔴 **REBUILD ON D2: re-predict, not re-gate, with ONE stop condition** (handover :13-23). The drafter's M-1 above is an EXPECTATION that you re-measure. Expect the tree to CHANGE because the locks differ, and the two composed doc blobs NOT to change. That is what the drafter measured; you assume neither. gate77's merges follow (#1429 KS-1449 and #1430 KS 1328 per RULINGS Q-RACE76; Wednesday names the rows), and every predicted tree is re-run on develop AFTER your squash.
2. 🔴 **R 21st's FORWARD-ADD IS YOUR TRAP** (handover :25-33). In `tools/inbox_matchra1.py` (**`b801d4caafd66110`**, 598 lines; drafter `shasum` and `wc -l`, EQUAL to the handover :106), `OTHER_SEATS` (`:222`) carries `"r 22nd"` and `"seat r 22nd"`.
   - Drafter's raw quoted-token census (`grep -o -F | wc -l`): `"r 22nd"` 2 and `"seat r 22nd"` 2. These include comment mentions; the tool wins.
   - **REMOVE them FIRST**, or your own brief and every ANSWER read FOREIGN and your watcher never fires.
   - ADD `"r 21st"` / `"seat r 21st"`.
   - FORWARD-ADD **`"r 23rd"` / `"seat r 23rd"`** (spelled `23rd`; drafter census of `"r 23rd"` = 0 today).
   - Change `MINE` at `:102` (`MINE = "r 21st"`, drafter `grep -n`) to `"r 22nd"`. Keep DOUBLE quotes, and edit by the byte span the AST gives you.
   - Prove the edit BY IMPORT on FULL-LENGTH real subjects from the API. Feed `{"messages":[]}`, catch `SystemExit`, and include an inverted-want control.
   - **Include R 21st's real GO-shaped subjects reading FOREIGN, and a `(Seat R 23rd)` addressee on your pane tag reading NOT mine** (STANDING_LINES :404, :411, :415, :417).
   - **Sweep class:** R 21st's is `(?:[1-9]|1[0-9]|20)` (1-20; drafter `grep -o -E | wc -l` = 9 sites in `sweepra21.py`). **Yours must match 1-21 and NOT 22**, for example `(?:[1-9]|1[0-9]|2[01])`. Prove it on the PARSED pattern: `ra21` MATCH, `ra22` no, `ra210` no.
   - **Re-key the sweep's CONTROL 1b fixture COMPLETELY, tokens AND its record-folder PATH** (handover :56-61).
3. 🔴 **WHAT LIED TO R 21st** (handover :34-76). Read all eight there. The ones that bind your queue:
   - (a) The `html_docs_check.mjs:120` entry guard exits 0 having checked nothing when it is invoked through a symlinked path. The kit's `--selftest` reads **13/15** under `TMPDIR` (`/var` -> `/private/var`). Name the failing arms by their printed text ("guard POSITIVE CONTROL", "TAG BALANCE"), and re-drive the guard pair by hand on a CANONICAL path: T'' rc 0 (12, 0); one bare `<p>` planted rc 1 (11, 1).
   - (b) The mergein's `PUSH_LOCK_DIR` check is HOISTED (`:111-112`). Keep it that way.
   - (c) Re-key an inherited probe's DATA as well as its tokens. `run_armsra21.py` hard-codes R 21st's record folder and R 21st's scratchpad (drafter census: `2026-10-09_seatR-21st` 1, `028f980d` 1, `scratchpad/r21` 1). **Re-point `REC` and `SCR`, and rebuild the synthetic arm commits on D2.**
   - (d) zsh `"$M:Projects…"` applies the `:P` modifier. Write it as `"${M}:${PATH_VAR}"` and self-check that the instrument reads 40-hex.
   - (e) Two pre-gates pass VACUOUSLY when the worktree is absent.
   - (f) Classify Actions by workflow PATH against TWO references.
   - (g) Assert RAW counts before writing a byte.
   - (h) Read your cockpit name with `-t "$TMUX_PANE"`. The bare read returned `wednesday` eight times.

## THE PARTITION
| Seat | Pane | Token / lock | Writes | Never |
|---|---|---|---|---|
| **R 22nd (you)** | `Secuura/Blockchain-R` | `ra22` / **`.push-lock-d8`** (`LOCK_SEAT='Secuura/Blockchain-R ra22'`, ref-ns `seatra22`) | ONE fresh DETACHED worktree `s-ra22-m1427` at the gated head (Q-WT22); ONE merge-in commit M' in it; ONE push of M' to `feature/ks-1274-trivy-bare-object-guard-ra18-1` (its NAME adopted for that one push, gate73 Q-ADOPT10 (a) / RULINGS Q-MERGEIN76); ONE API squash of #1427 on GO 2; your record folder `5_Project_History/2026-10-09_seatR-22nd/`; your handover; your history entry | any other push, branch or raise; any ticket write or comment; any objects transfer unless Wednesday rules it (Q-OBJ22) |
| R 21st (WRAPPED 23:37Z) | your pane | `ra21` | nothing | `worktrees/s-ra21-m1427` (detached at M `dedc861c04a5`, porcelain 0, KEPT on ruling 2; drafter `rev-parse` + `status --porcelain`); M itself; `2026-10-09_seatR-21st/` (COPY its tools, never run or edit them there) |
| R 20th to R 3rd (WRAPPED) | your pane | `ra20` to `ra3` | nothing | their worktrees and records |
| R 18th (AUTHOR of #1427, wrapped) | — | `ra18` | nothing | `worktrees/s-ra18-ks1274` |
| G 4th (author of #1428, merged) | — | `g4` | nothing | `worktrees/s-g4-ks593` |
| **F 6th** (WRAPPED 02:46Z; #1436 open at READY FOR QA) | `Secuura/Blockchain-F` | `f6` / **`.push-lock-f3`** | nothing now | **PR #1436 (KS-808)**, branch `feature/ks-808-run-migrations-counts-skips-apart-f6-1` at **`90d98754db7b`** (== `refs/pull/1436/head`, drafter ls-remote 02:47:17Z), `worktrees/s-f6-ks808` (KEPT for its gate), its record folder, `.push-lock-f3`. **#1436 also appends a block to BOTH platform docs** (F 6th READY :17-19), so it is your docs neighbour (Q-ORDER1436). Never merged by you. |
| **V 1st / V 2nd** (WRAPPED; #1435 MERGED as D2) | `Secuura/Blockchain-V` | `v1`/`v2` | nothing | **every KS-1452 asset**: `worktrees/s-v1-hbslock` (LEFT, V 2nd WRAP :76), the origin branch `feature/ks-1452-handlebars-lock-refresh-v1-1` (still exists, V 2nd WRAP :66), `refs/pull/1435/head` `6f4adfe8835e…`, their records, the KS-1452 comment |
| J 1st (WRAPPED; board-only) | `Secuura/Blockchain-J` | `j1` | nothing | its board writes |
| any other live seat (floor in the SEND AMENDMENT) | its own | its lock (WAIT) | — | every other PR: never merged by you |

**Seats share ONE inbox (`secuura-blockchain@agentmail.to`). A mail naming another seat is NOT R 22nd's,** even on your pane tag (STANDING_LINES :336-337, :362-363). Matcher precedence: an unlisted addressee reads UNKNOWN ADDRESSEE, never FOR ME (:417).

## ITEM 0: BOUNDED and read-only. Then `QUESTION: plan confirmation (Seat R 22nd)`, and WAIT
Before the ANSWER, do NONE of these: take a lock; add a worktree; write a ref; transfer objects; install; edit a PR; write a ticket; comment.

**The boot pull (STANDING_LINES :436).** Your launcher pulls `2_Project_Files` at boot BY DESIGN when you are the SOLE live session; KS-907 makes it read-only only when another session is live (`Launch_Claude.command:244-380`, the `[KS-907] … READ-ONLY` line at `:350-351`). That is the project's rule, not a breach.
- If it pulls, it fast-forwards the shared `develop` / `origin/develop`, which both read **`ddea005553bf…`** (drafter `for-each-ref`), to D2. **RECORD it**: from/to, the `.git/FETCH_HEAD` mtime (drafter read `8 Oct 13:41`), and the new `rev-parse --all` count + sha256/16. Then carry on.
- **After boot: no `git fetch` or `pull` in the shared checkout, and no write to either develop ref.**

Measure:
- **(a) Refs, in ONE `ls-remote` saved to a file:**
  - develop; `refs/pull/{1427,1383,1429-1436}/head`; #1427's branch.
  - Any `-ra22-` ref. The drafter read **0**, with `-ra13-` = **2** and `-ra18-` = **1** as controls: 2,160 refs, highest `refs/pull` 1436, at 02:47:17Z.
  - `date -u`.
  - A moved #1427 head is a STOP: mail. A moved develop is NOT a STOP: name it and re-predict (b).
- **(b) M-1, the re-prediction, in YOUR clone.**
  - Build the clone with `clone --shared --no-checkout`, reset origin to `git@github.com:Secuura/Distributed_Secuura.git`, and fetch D2 BY SHA if it is absent, under the checkout's own `core.sshCommand` with `GIT_SSH_COMMAND` unset (STANDING_LINES :410).
  - **Instrument 1:** `python3 <kit>/c4_docs_gate76.py chain --repo <clone> --order 1427 --develop <develop read now> --heads 1427=2b6da5f561b05a820bbe1ab5e891bff9f4f531c8,1428=64eafead891e81f5adb4e46aaa94ff6a6ace1998 --out <fresh dir on a CANONICAL path>`. Then `cmp` its `1_1427_composed_*` against the kit's `2_1427_composed_*`, with a discriminating control, and `git hash-object` each.
  - **Instrument 2:** `merge-tree --write-tree` (D2, head), a private-index substitution of the two composed blobs, then `write-tree`. Include the D1 control: it must give `57c9b5eaec95…`.
  - Want: tree `e948c77b8b46…`, blobs `b2bd07dbae40…` / `f4503e99d43e…`, guard 12/0, ALL OK, conflicts on the two docs ONLY.
  - **A conflict or a moved #1427/#1428 path outside the two docs means RE-GATE: STOP and mail.** The chain tool's own refusal for this is `develop … moved a CODE path of #… — RE-GATE` (`c4_docs_gate76.py:221-223`).
  - Re-hash `KIT_REPORT.md` (`af3a9c3b7954598e`), `RULINGS_wednesday.md` (`6013997a79a714ed`), `kit.json` (`f14645aa2dc5a993`) and kit.json's 12 `script_sha256` pins (drafter `shasum`; the three file hashes EQUAL the handover :88).
  - The kit's lib refuses a write verb under `!CODING`, so `--repo` is always YOUR clone.
- **(c) Tools:** the copy receipt; THE SWEEP; the re-key; membership BY IMPORT; your line-by-line read of the re-keyed builder; the 11 refusal arms + P1 at their own asserts (STANDING_LINES :444). **All of this is in your record folder only, and nothing writes a ref.** R 21st's precedent is ANSWER_plan step 2: the re-key happened before the START word.
- **(d) The shared store, read verbs only:**
  - `rev-parse --all`, count + sha256/16. The drafter read **1,654 / `f97ee53e189fd53b`** at ~02:48Z. R 21st's wrap read 1,651 / `25dad918f55979ee`; the +3 since then comes from lane V's and F 6th's ref writes and is NOT attributed by the drafter.
  - `cat-file -e` of D2, the gated head and `bf277eead26897bb648c801f92308681dbdaffdc`, with `deadbeef…` as the NEGATIVE control at the same moment. `rev-parse --verify` is NOT a presence check.
  - Local `refs/heads/feature/ks-1274-trivy-bare-object-guard-ra18-1`: the drafter's `for-each-ref` read **`2b6da5f561b0…`**, and `refs/remotes/origin/…` is the same value. It becomes your `--m-retain`.
  - Locks, identified by the holder's `seat` field: two polls, with the control in a private `mktemp -d`. The drafter's `ls -la worktrees | grep push-lock` read 0, with NO control driven, because the drafter plants nothing there.
  - `s-ra22-*` worktrees: drafter **0**, with `s-ra21-m1427` = 1 as the control. `worktrees/` has 518 entries (drafter `ls -A | wc -l`).
- **(e) Seat facts:**
  - `$TMUX_PANE`, then `tmux display-message -t "$TMUX_PANE" -p '#{@cockpit_name}'` with a nonexistent-option control.
  - Launcher ancestry from `ps` (the `--model` argument).
  - Watcher pid, read from a ps FILE.
  - `df -m /Volumes/DevMASTER`: drafter 393,072 MB available, 80%.
  - Every launcher preflight warning VERBATIM, from `4_Credentials/.launch_preflight_last.txt`. R 21st's were `[F-02] No SSH identity available for git…` and the KS-907 pair.
  - The merge-note artefact, re-hashed: **`HANDOVER-seatR18-2026-10-08.md` sha256/16 `1081ef422c811c0d`** (drafter `shasum`, equal to R 21st's plan (e)).
- **(f) Linear, read-only:** KS-1274's state, assignee, newest comment, and the #1427 attachment's `linkKind`/`status`. Run the fabricated-key control (KS-99999) in ITS OWN query. The baseline is R 21st's WRAP at 23:37Z: `In Progress`, updatedAt `2026-10-08T06:52:05.291Z`, 0 comments, #1427 `contributes`/`open`. **UNKNOWN to the drafter today, because the drafter has no Linear read; your (f) closes it.**

**Your plan confirmation carries:** blocks (a)-(f), one each; the re-key receipts; the launcher lines VERBATIM; the boot-pull record; a ctx read request. **Budget: mailed by ~25% ctx.**

## TOOLS
**Copy** from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-09_seatR-21st/` into `…/2026-10-09_seatR-22nd/`, keeping the SAME subfolder layout (`tools/`, `merge/`, `boot/`). Hash each file into `_COPY_HASHES_ra22.txt` and `cmp` it. **Never run a tool from R 21st's folder**: `$R` is the script's own dir, so it would write YOUR artefacts into THEIR records. **Expected values** are below (drafter `shasum -a 256 | cut -c1-16` + `wc -l`, ~02:45Z; **all 14 EQUAL the handover table :98-111**):

| tool (R 21st path) | sha256/16 | lines | your copy |
|---|---|---|---|
| `merge/build_addendumra21_gate76.py` | `9ca495b426ba21f0` | 523 | `build_addendumra22_gate76.py` |
| `boot/m7_squashra21.sh` | `ad8bb745dbcf1598` | 104 | `m7_squashra22.sh` (`$M7_TOOLS` = `merge/`) |
| `tools/mergeinra21_gate76.sh` | `c40fb7c90939b81b` | 323 | `tools/mergeinra22_gate76.sh`, beside the ONE `lockra1.sh`; HOISTED (`:111-112`) |
| `tools/m3_args_ra21.sh` | `bdc2f340e5b020de` | 33 | `tools/m3_args_ra22.sh`: EVERY value re-derived (M-3 below) |
| `merge/run_armsra21.py` | `dedd3e9fb1d77813` | 157 | `run_armsra22.py`, with `REC`/`SCR` re-pointed |
| `tools/inbox_matchra1.py` | `b801d4caafd66110` | 598 | same name, RE-KEYED (first-three item 2) |
| `tools/sweepra21.py` | `cfbaaf75339b37a2` | 273 | `sweepra22.py`: class 1-21, CONTROL 1b fully re-keyed |
| `tools/inbox_watchra1.sh` | `73e696201184ce0a` | 159 | same name, `WATCHRA22_*`, banner |
| `tools/provenance_ra21.py` | `d215ce0275a6e3f9` | 91 | `provenance_ra22.py` (it carries no lane token) |
| `tools/poll_actionsra21.py` | `11afd225bf61bb6f` | 49 | `poll_actionsra22.py` |
| `merge/mergera1.py` | `aaf230e7d1975213` | 604 | UNCHANGED |
| `tools/pushra1_ff.sh` | `dd8b1083a37fb82d` | 128 | UNCHANGED (LOCK_SEAT required, no default) |
| `tools/lockra1.sh` | `b7aa55e5574362e9` | 559 | UNCHANGED (`:217` DEFAULTS `PUSH_LOCK_DIR` to `.push-lock-d8`: the mergein's hoisted check guards it) |
| `merge/merge_squash_v3.sh` | `460c4e7841d77505` | 390 | UNCHANGED, unused |

- A different hash is a STOP and a mail. Re-hash the originals at your wrap.
- 🔴 **Re-key: THE GENERIC CLAUSE BINDS, AND IT COMES FIRST. Re-key every lane-bearing declaration, including LOCK_SEAT defaults, env prefixes and fixtures. The tool wins.** EXPECTATION only: the drafter's raw case-insensitive census (`grep -o -i -E … | sort | uniq -c`; an alternation-order-dependent count, so assert YOUR raw counts before writing a byte, per handover :72-74) is listed here.

  | tool | expected hits (raw) |
  |---|---|
  | builder | `ra21_` 114, `r 21st` 4, `r 20th` 14, `ra20` 2, `ra21` 1 |
  | m7 | `ra21_` 23, `ra21` 5, `r 20th` 2 |
  | mergein | `ra21_` 5, `r 21st` 2, `r 20th` 2, `push-lock-d8` 3 (KEEP) |
  | m3_args | `1e7f90e26137` 2, `57c9b5eaec95` 1, `ra21` 2, `seatra21` 1, R 21st's scratch path 1, R 21st's record folder 1 |
  | run_arms | `ra21_` 62, `r 21st` 5, `ra20` 3, and R 21st's record folder + scratchpad 1 each |
  | sweep | `ra20` 10, `ra21` 7, `r 20th` 4, `push-lock-d8` 1 |
  | watcher | `watchra21` 4 |
  | poll_actions | `ra21` 3 |

  Also re-key: the GO fixture `merge/go_fixture_1427_SYNTHETIC.txt`, which names D1 `1e7f90e26137` and T' `57c9b5eaec95` once each, so re-key it to D2, T'' and the REAL M'. Also re-key log/artefact names (`mergeinra21_gate76.log`, `mergera21_gate76_merge.out`), GO-clause ordinals, and banners. Build the token list from EVERY generation each file names (STANDING_LINES :294, :428). Sweep every live 12+-hex constant outside comments before the first run (:422), and print `N checked` per tool; `0 checked` is a FAIL (:339-340). A seat token quoted in a comment counts toward a raw assert (:448), so name other seats in comments WITHOUT quote marks.
- **Predecessor-claim tuple (builder `:438-446`):** ADD `"Seat R 21st"` (a wrapped predecessor on your pane). **ADD `"Seat V 2nd"` and `"Seat V 1st"`**: D2's own message carries `Merged by Seat V 2nd …` at body line 43 and names `HANDOVER-seatV1-…` at :46 (drafter `git log -1 --format=%B 81d2e5f4… | grep -n -i`; control: D1's message carries `Merged by Seat R 20th` at :57). Assert `"Seat R 22nd"` ABSENT, and keep every inherited name (Q-PRED22).
- **Builder GO-clause regex** (`:186`) becomes `GO \(Seat R 22nd\): merge \d{3,5} on [a-z0-9]+`.

## THE BUILDER (R 21st's, re-keyed)
Row #1427: `RA22_LANDING=merge-in`, `RA22_NO_MERGE_IN=0`, `RA22_MERGE_IN_HEAD=<M'>`, `RA22_DOCS=merged`, `RA22_QM=require`, `RA22_OWN_KEYS=KS-1274`, `RA22_EXPECT_PATHS=6`, `RA22_MODE_CENSUS={"100644": 5, "100755": 1}`, `RA22_HEAD_TRAILER=refuse`.
- With `RA22_DOCS=merged` on a merge-in, `merged_blob_paths=[]`. The builder asserts that M's doc blob == the GO's composed blob AND that the GO's composed blob != the GATED head's blob.
- These values are unchanged from R 21st except the prefix. `EXPECT_PATHS` = 6 is D2..T'' (drafter).

**Arms:** re-run `run_armsra22.py` before the first real use.
- Each arm must REFUSE at ITS OWN assert, with 11 distinct reasons, and POSITIVE controls P1 and P2 must pass.
- Rebuild the synthetic arm commits (`M_OK` with tree T'' and parents [gated head, D2]; `M_SWAP`; `M_BADTREE`) on D2, in YOUR clone.
- **P2 is re-run on the REAL M' after `qm`**, against the GO fixture re-keyed to D2 / T'' / M'.
- If P1 (the row #1428 fixture) reads as the tool built it, report it with the asserting line (R 21st's ANSWER_ctx_hoist ruling 3).

**Then:** builder -> `mergera1.py --dry`, then READ the `.DRY` body yourself. Check each of these:
- ONE `Merged by Seat R 22nd`.
- Last line byte-equal to the GO's `merge_note`.
- 0 trailers, 0 Co-Authored-By, 0 `Generated with`.
- ONE `^Refs `.
- Subject byte-equal to the GO's (80).
- Hyphenated key set == `{KS-1274}`.
- 0 closing adjacency under the builder's broad `CLOSING` (`:458`).

## M1: THE GO PARSER for GO 2
Each line must give exactly ONE match against the regexes extracted from YOUR builder by `ast` (`build_addendumra21_gate76.py:158-172`, read by the drafter; there are **13** `one()` patterns incl. flow and cheat). Wednesday builds GO 2 from THIS table and runs it against your extracted regexes before sending: 13/13 exactly once, clause fullmatch, ABSENT strings 0.
| builder line | GO 2 value | instrument |
|---|---|---|
| `- develop D:` | `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6` (or develop at GO time, if it moved and M' was rebuilt) | ls-remote 02:47:17Z (drafter) |
| `- PR head:` | `2b6da5f561b05a820bbe1ab5e891bff9f4f531c8` = the GATED head. M' rides in `RA22_MERGE_IN_HEAD` (ruled, R 20th ANSWER_builder ruling 2) | ls-remote |
| `- PR base B:` | `0a6177ea5482227e83d5045b68b8577a56326ffc` (the head's one parent; Q-PRBASE21 carried) | `git log -1 --format=%P` (drafter) |
| `- END_TREE:` | `9b6c3dfef865dfc35b05d4da8fcad7e24249fbb1` | `git log -1 --format=%T` (drafter) |
| `- Target tree T':` | `e948c77b8b464f347a6af5abc515490de782ead6` (== tree(M'), re-read on the REAL M') | predicted by the drafter, two instruments |
| `flow \`Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html\` = ` | `b2bd07dbae400c0ad15b89046a65967a117e1a15` (COMPOSED, unchanged from D1) | chain + hash-object + cmp vs kit |
| `cheat \`Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html\` = ` | `f4503e99d43e8a90ffe881291295695e7cd61ae1` (COMPOSED, unchanged from D1) | chain + hash-object + cmp vs kit |
| `Declared squash subject: \`…\`` | `KS-1274: job 04 fails a scan when trivy reports neither Results nor ArtifactName` | gate76 verdict, RULINGS Q-SUBJ76 |
| `N chars, LANDS N` | `80 chars, LANDS 80` | drafter `printf %s | wc -c` = 80 |
| `N bytes, sha256 …` | `4998 bytes, sha256 91e3ee3adae71f8099808e5b269e449df62e600c9a88bb4b86524039a4f7f252`: **digits only, with NO thousands comma** | drafter `wc -c` + `shasum -a 256` on `…/Testing Agent MAIN/projects/secuura/reports/2026-10-08-gate76/evidence/1427.squash_body.GATE76.txt` |
| `merge_note: \`…\`` | `Merged by Seat R 22nd on the authority of HANDOVER-seatR18-2026-10-08.md sha256 1081ef422c811c0d` | R 21st's M1 :110, re-keyed; drafter `shasum` |

**PRESENT in GO 2:** the clause `GO (Seat R 22nd): merge 1427 on gate76`, plus **`qm Q2 STRICT`** and **`qm green`** (`RA22_QM=require`). **ABSENT:** `NEW-FAILING`, `PENDING NONE`. Exactly ONE `flow \`` line and ONE `cheat \`` line.

**The ADDENDUM** (a separate mail, provenance-checked) carries `ACTIONS VERDICT (Wednesday):` and `0 new failures`. 🔴 **ADDENDUM rule (handover :67-71):** Actions on M' are classified by workflow PATH against TWO references:
- D2's own `push` runs. Expect about 2 workflows; UNMEASURED by the drafter.
- The gated head's `pull_request` runs, 6 workflows per R 21st.

**`security-scan.yml` has NO run on develop**, so a develop-only classifier would call its failure on M' NEW. Use the class `no D run, fails on the gated head too (named)`. Three workflows are named `pr`. Query by FULL 40-hex `head_sha`, with a fabricated-sha control (total_count 0).

## QUEUE: STEP 2, IN ORDER
- **M-1** = ITEM 0 (b). Mail `STATUS: re-prediction on <D 12-hex> (Seat R 22nd)`, carrying: the tree; both blobs; the `cmp` results; the D1 control; and the line "kit selftest 13/15 (`html_docs_check.mjs:120` symlink guard; arms 'guard POSITIVE CONTROL' and 'TAG BALANCE' re-driven by hand on a canonical path)". **Then WAIT for `START STEP 2 (Seat R 22nd)`** (Q-START22).
- **X-0 ctx QUESTION** before M-3. Proceed under 50%, or at 50-64% on Wednesday's explicit word. At 65%+, WRAP COLD. Usage 90%+: WRAP COLD.
- **M-2 the worktree, by hand under ONE lock take** (`lockra1.sh take`, released with the HOLDER FILE's pid, never `$$`). Run `worktree add --detach /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-ra22-m1427 2b6da5f561b05a820bbe1ab5e891bff9f4f531c8`, never `-b` (Q-WT22). `rev-parse --all` must be byte-identical across it. RELEASE.
  - **No objects transfer:** D2 should read PRESENT. If it reads ABSENT, STOP and mail (Q-OBJ22).
- **M-3 merge-in.** `mergeinra22_gate76.sh` **TAKES AND RELEASES THE LOCK ITSELF**, so never wrap it in your own take (STANDING_LINES :377). Drive it through `m3_args_ra22.sh` (a bash ARRAY). Every argument is REQUIRED (`:69-78`); the values below are re-derived by the drafter, and you re-derive them by the TOOL's own meaning:
  - `--wt /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-ra22-m1427`
  - `--br feature/ks-1274-trivy-bare-object-guard-ra18-1`
  - `--ours 2b6da5f561b05a820bbe1ab5e891bff9f4f531c8`
  - `--dev 81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6`
  - `--dev-parent 1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0` (D2's FIRST parent, i.e. D1, NOT the merge-base)
  - `--dev-parent-count 1` (drafter: `%P` word count 1)
  - `--base 0a6177ea5482227e83d5045b68b8577a56326ffc` (COMPUTE it: drafter `merge-base 2b6da5f5… 81d2e5f4…` = `0a6177ea5482…`)
  - `--predicted-tree e948c77b8b464f347a6af5abc515490de782ead6`
  - `--flow-blob b2bd07dbae400c0ad15b89046a65967a117e1a15`
  - `--cheat-blob f4503e99d43e8a90ffe881291295695e7cd61ae1`
  - `--vclone <YOUR clone, holding both blobs AND tree T''>` (pre-gate `:174-175` reads `ls-tree $PREDICTED_TREE` there). **NOT R 21st's clone.**
  - `--control-commit bf277eead26897bb648c801f92308681dbdaffdc` (55 B of trailers, drafter `%(trailers) | wc -c`)
  - `--expect-conflicts 2`
  - `--m-retain 2b6da5f561b05a820bbe1ab5e891bff9f4f531c8` (the LOCAL branch ref's real value, read now)
  - `--lock-seat 'Secuura/Blockchain-R ra22'` and `--my-ref-ns seatra22` (`:82-85` asserts they match)
  - `--own-key KS-1274`
  - `--head-paths`: #1427's 4 code paths, `Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh,Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh,Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh,Blockchain/Testing/jobs/04-container-trivy.sh` (drafter `diff --name-only base head` minus docs)
  - `--dev-paths`: **12 paths** = base..D2 minus `Projects Documents/` (drafter count 12): #1428's 7 originate paths PLUS the 5 lockfiles (`Blockchain/Dev/package-lock.json`, `Blockchain/Dev/services/{governance,originate,referral,vc-issuer}/package-lock.json`). See Q-DEVPATHS22. The `:285-316` NONDOC sweep covers them either way; predicted `12 checked`.
  - `--expect-ours-paths 14` (drafter: head..T'' = 14; was 9)
  - `--expect-dev-paths 6`
  - `--subj 'Merge develop 81d2e5f4c415 into the KS-1274 branch (docs keep-both, gate76 step 2)'` (82 chars, drafter `wc -c`; Q-MSUBJ22)
  - env `PUSH_LOCK_DIR=/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-lock-d8` (REQUIRED; the basename is asserted at `:112`), with `GIT_SSH_COMMAND` UNSET.

  Want:
  - Conflicts on EXACTLY the two docs, resolved BY CONTENT to the composed bytes VERBATIM. **Never `git merge-file --union`, never a hand edit.**
  - tree(M') == `e948c77b8b46…`.
  - Parents EXACTLY `[2b6da5f561b0…, 81d2e5f4c415…]`, each read separately.
  - 0 trailers vs the 55-byte control; subject byte-equal.
  - The tool's own `MERGEINRA22_GATE76: N gates CHECKED, N passed, 0 failed` / `VERDICT: PASS` and its `.rc`.
  - Then read M' AT SOURCE with a wrong-value arm per fact, as R 21st did (M_built mail :40-47). Brace every `"${M}:${P}"`.
- **M-4 qm, in YOUR clone:** `c4_docs_gate76.py qm --repo <clone> --pr 1427 --head 2b6da5f561b05a820bbe1ab5e891bff9f4f531c8 --merge-in-head <M'> --develop-after 81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6 --predicted-tree e948c77b8b464f347a6af5abc515490de782ead6 --out <fresh canonical dir>`. Q1-Q6 must PASS (R 21st: CHECKED 8, 0 FAIL). Then run P2 on the REAL M'.
- **M-5 push M' BARE.**
  - **S-1 first, in `s-ra22-m1427` AT M', outside the lock:**
    - `npm ci --ignore-scripts`, then `npm run build --workspace=packages/shared`, then ASSERT `dist/index.js` exists.
    - `npm ci --ignore-scripts` in EVERY `systemTest/*` with a `package.json` (STANDING_LINES :400, :432).
    - The install must follow M', because M' carries D2's locks. F 6th's lesson: "a locks-only develop move still needs `npm ci`" (F 6th WRAP :33-34).
  - **Q-LEGS67:** run legs 6 and 7 standalone in the worktree (`npm run audit:gate` and `npm run audit:locks` from `Blockchain/Dev`) BEFORE the real push. A NEW advisory = STOP and mail (another freeze; F 6th's lesson 3, an EXPECTATION). Never baseline, never `--no-verify`.
  - **F-02:** prove the push identity with an SSH auth probe (`ssh -T` under the repo's own key, plus a refused-key control). Never `push --dry-run` (it RUNS the hook, :386-387). Never set `SECUURA_ALLOW_ONDISK_KEY` yourself.
  - **KS-1086:** snapshot the five indicators and `.git/config` before the push, and compare after.
  - **The push:** first `env -u GIT_SSH_COMMAND LOCK_SEAT='Secuura/Blockchain-R ra22' FF_DRYPROOF=1 bash <REC>/tools/pushra1_ff.sh <abs worktree> feature/ks-1274-trivy-bare-object-guard-ra18-1 2b6da5f561b05a820bbe1ab5e891bff9f4f531c8`, then the same command without `FF_DRYPROOF`. The tool takes and releases the lock itself.
  - The hook runs the FULL preflight. **Expected, not measured, on M': legs 6 and 7 PASS now that the locks pin handlebars 4.7.10, and legs 3/4/8 SKIP** (no stack: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED`).
  - Result = the tool's `.rc` + `ls-remote` (:405). rc 141 with the ref unmoved is the KS-1149 class: report it, retry under the lock, never loop. **`PREFLIGHT FAILED` or a refused push = STOP. Never `--no-verify`.**
  - Quote the gate lines EXACTLY. Record that the push moves the shared `refs/remotes/origin/feature/…-ra18-1` and leaves local `refs/heads/…` at the gated head (:434).
- **M-6 Actions on M'**, by FULL 40-hex `head_sha`, classified by PATH against D2 AND the gated head (the ADDENDUM rule above), SUBSET, with two agreeing terminal polls and a fabricated-sha control. Mail `STATUS: merge-in 1427 pushed (Seat R 22nd)` with M', its qm, the push's gate lines, and the Actions. WAIT for GO 2 and its ADDENDUM.
- **X-1 GO 2 COMPLETE** (M1, by `ast`). Run `provenance_ra22.py check` on the GO and the ADDENDUM with their exact subject prefixes. Its arms must each refuse: no record; dmarc flipped; body sha zeroed; **genuine record + TAMPERED body**; wrong prefix. A real signed mail must pass.
- **X-2 refs in ONE action:** develop == GO 2's D, and #1427 head == M'. A moved develop = STOP: mail `STATUS: re-prediction on <12-hex> (Seat R 22nd)` and WAIT for a superseding GO.
- **X-3 KS-1274 BEFORE** (Linear: state + the #1427 attachment).
- **X-4** builder -> `m7_squashra22.sh dry` (35+ required knobs; `M7_LANDING=merge-in`, `M7_MERGE_IN_HEAD=<M'>`, `M7_QM=require`) -> READ the `.DRY` body.
- **X-5 squash, PINNED to M'** (`sha: <M'>`) via `m7_squashra22.sh go`: provenance -> clause -> develop AND the PR head re-read by `ls-remote` in the same action -> builder -> real.
- **X-6 verify at source** (`ls-remote` AND the API):
  - squash tree == `e948c77b8b46…`;
  - "is a commit", "exactly 1 parent" and "parent == 81d2e5f4c415…", each with a wrong-value arm (:424);
  - 0 trailers, with the reader non-blind on `bf277eead268`;
  - 0 `Generated with`;
  - landed subject == declared (80, no ` (#n)`);
  - exactly 6 paths vs D2;
  - landed doc blobs == the composed blobs;
  - `04-container-trivy.sh` still `100755`;
  - ONE `Merged by Seat R 22nd`;
  - "did it land" = the PR's `merged` field.
- **X-9 KS-1274 AFTER:** it must NOT walk to Done. If it did: STOP, mail `STATUS: KS-1274 walked (Seat R 22nd)` with both reads, and never move it back. A bot attachment change is reported, never reverted. Mail `STATUS: merged 1427 (Seat R 22nd)`. Then WRAP.

## STANDING FINDINGS CARRIED (STANDING_LINES, by current line; file 448 lines, sha256/16 `6d8166bac3139428`, drafter)
| line | finding |
|---|---|
| `:398` | pane id from `$TMUX_PANE` |
| `:399` | no force push, ever; MERGE develop in |
| `:400` | a fresh worktree builds `packages/shared` before its first push |
| `:403` | watcher SINCE = newest mail READ |
| `:405` | a result is the tool's `.rc` + `ls-remote` |
| `:408` | a merge-in needs develop's objects in the WORKTREE's store |
| `:409` | inherited tools fail closed on unset knobs |
| `:410` | a `clone --shared` origin is the LOCAL checkout |
| `:411` / `:415` | trap 4's FORWARD half and the untagged-arm tension |
| `:416` | never export `GIT_SSH_COMMAND` around a push tool |
| `:417` | unlisted addressee = UNKNOWN ADDRESSEE |
| `:420` | `for-each-ref` globs do not cross `/` |
| `:422` | develop parent is an argument; sweep 12+-hex constants |
| `:423` | `rev-parse <sha>:<path>` echoes on absence |
| `:424` | "ONE parent" is three reads |
| `:428` | re-key EVERY lane-bearing declaration |
| `:432` | `npm ci` in every systemTest package |
| `:434` | a worktree push moves the shared tracking ref, not the local branch |
| `:436` | the boot pull is the project's rule |
| `:440` | authenticity gates bind the record to the BODY |
| `:442` | html_docs_matrix 12/0 is NOT tag-balance evidence |
| `:444` | a refusal arm counts only at its own assert |
| `:446` | never plant a control in the shared `worktrees/` |
| `:448` | quoted seat tokens in comments count to raw asserts |
| `:374` | a merge tool must not ADD attribution; check the SENT body |
| `:377` | a tool that takes the lock itself is never wrapped |
| `:386-387` | `push --dry-run` runs the hook |
| `:348` | read repo files from a SHA, never from the main checkout's working tree |

## HOLDS
- **No squash without GO 2, in its SUBJECT, naming THIS seat's number. No merge-in write before `START STEP 2 (Seat R 22nd)`.**
  - #1436 (KS-808, F 6th's), #1435 (merged), #1383, #1429-#1434 and every other PR: never merged, pushed to, commented on or edited by you.
  - No `--admin`. HTTP 422 on an own-account approval: meet it and STOP.
- **ONE push only (M-5).**
  - No `--no-verify`, no force push, no `-u`, no `push --dry-run`.
  - No baseline edit, no lock edit, no audit-baseline entry, ever.
  - After boot, never `git fetch`/`pull` in the shared checkout. `GIT_SSH_COMMAND` stays UNSET for every network verb. Never write either develop ref.
- **No deploy, no `az`, no SSH (beyond the auth probe), no migration, no Docker, no stack.**
- **No client-facing communication.**
  - No ticket comment or state change.
  - Never the extranet: **decline the launcher's `POST /api/seen`**, as R 20th and R 21st did and Wednesday confirmed.
  - **No mail or comment to Peter or Stuart.**
- **No guard, doc, lock, manifest or spec edit** beyond M''s two composed doc blobs, which are the kit's bytes VERBATIM. The `html_docs_check.mjs:120` defect is Wednesday's to file, not yours to fix.
- **Never delete: quarantine.** Never touch any of these:
  - any gate kit or report;
  - `s-ra21-m1427` and M `dedc861c04a5`, and R 21st's records;
  - `s-ra18-ks1274` and `s-g4-ks593`;
  - **the KS-1452 / #1435 assets (`s-v1-hbslock`, `feature/ks-1452-…-v1-1`, V's records)**;
  - **#1436 / F 6th's assets (`s-f6-ks808`, `feature/ks-808-…-f6-1`, `.push-lock-f3`, F 6th's records)**;
  - another lane's lock, mail or records.
- No secret in argv, in a kept ps capture, in a mail or in a record file.
- Signature classes pause for Kam. A squash onto develop is irreversible: it moves ONLY on GO 2.
- **One inbox.** Act only on mail whose subject carries `-R` AND `(Seat R 22nd)`, with DKIM/SPF/DMARC checked by `provenance_ra22.py`. A mail naming another seat is not yours. A new mail from `kreiser.org@me.com` = STOP and mail Wednesday.
- Never `cd`. Use absolute paths and `${VAR:?}` on every path built from a variable. Use `-z` for paths (`Projects Documents/` has a SPACE). macOS has no `timeout`. zsh has no `PIPESTATUS`; never name a variable `path`; brace `"${M}:…"`.

## THE GO (verbatim subjects; nothing else authorises the squash)
From `wednesday-agent@agentmail.to`, with DKIM pass, the SUBJECTS EXACTLY (R 21st's brief :148 shape, re-keyed):
- **`[Wednesday -> Secuura/Blockchain-R] GO (Seat R 22nd): merge 1427 on gate76`**
- **`[Wednesday -> Secuura/Blockchain-R] ADDENDUM (Seat R 22nd): Actions verdict for GO 1427 on gate76`**

Both are sent only after M' is pushed and qm-green.

gate76's verdict reads GO for #1427 at `2b6da5f561b0…` (`[QA -> Wednesday] GATE76 (T2 x2): …`; report.md sha256 `58c3b8d1e5b720c232d45908908bfb6e136f574c752b4c211c06ef2f7b6e9599`, drafter `shasum`, equal to R 21st's brief :149). Its GO string 2 "covers ONE docs-only keep-both merge-in commit M, then its squash", with doc blobs = the kit's composed files "or a `chain` re-run on the real develop". The verdict NAMES Seat R 20th; GO 2 is Wednesday's and names YOU. A GO naming any other seat, PR or gate is not yours.

## MAIL FORMATS
Subjects:
- `[Secuura/Blockchain-R -> Wednesday] QUESTION: <topic> (Seat R 22nd)`
- `STATUS: re-prediction on <12-hex> (Seat R 22nd)`
- `STATUS: merge-in 1427 pushed (Seat R 22nd)`
- `STATUS: merged 1427 (Seat R 22nd)`
- `STATUS: KS-1274 walked (Seat R 22nd)`
- `WRAP (Seat R 22nd): …`

**The WRAP mail carries:**
- BLUF.
- 0 watchers live, proved.
- EVERY REF WRITE: the worktree add, the push of M' plus its tracking-ref side effect, and the API squash.
- KS-1274 before and after.
- UNMERGED / UNMEASURED.
- Drive hygiene: `s-ra22-m1427` and your scratch clone once #1427 is merged (your own only). Name `s-ra21-m1427` as R 21st's, left for Wednesday's ruling.
- The tool hashes R 23rd inherits, RE-MEASURED.
- Your handover.

**WRAP:** verify the squash at source (X-6) BEFORE wrapping. Your handover is **`5_Project_History/HANDOVER-seatR22-2026-10-09.md`**, opening **"FOR R 23rd, THE FIRST THREE THINGS"**:
1. gate77's merges follow, and every predicted tree must be re-run on develop AFTER your squash. **#1436 (KS-808) now needs a keep-both against #1427's blocks in both docs.**
2. Your `r 23rd` forward-add trap, the sweep class R 23rd needs (1-22, not 23), and your tools by MEASURED hash.
3. What lied to you this round.

Insert the history entry at the TOP and prove the insert is insert-only.

## RULED BY KAM, NOT YET IN AN ARTEFACT
R 21st's brief carried the 64 `[ruled] secuura-*` cards (`decision_queue.sh list ruled --undelivered`, 22:2xZ yesterday). None was in R 21st's queue. **The drafter did NOT regenerate the list; Wednesday regenerates it at send.** Act on NONE; if one bears on your work, mail Wednesday.

## QUESTIONS FOR WEDNESDAY (each with the drafter's recommended default)
- **Q-START22:** the literal `START STEP 2 (Seat R 22nd)` in your ANSWER to the re-prediction/plan mails releases M-2 onward. The re-key, sweep, arms and builder read happen BEFORE it (record folder only, no ref), as ruled for R 21st. **Default: yes.**
- **Q-WT22:** a FRESH detached `s-ra22-m1427` at the gated head, or reset R 21st's `s-ra21-m1427` (detached at M, 2,727 MB, node_modules built against D1's locks, which are stale for M' anyway)? **Default: FRESH.** `s-ra21-m1427` is left untouched for your drive-hygiene ruling. Resetting it would mean writing in another seat's worktree and orphaning M's only name.
- **Q-DEVPATHS22:** `--dev-paths` = the 12 non-doc paths of base..D2 (#1428's 7 + the 5 lockfiles), or R 21st's 7? **Default: 12**, by the tool's meaning ("the named develop paths must be EXACTLY develop's", `mergeinra21_gate76.sh:270-274`). The NONDOC sweep at `:299-316` covers all 12 regardless.
- **Q-MSUBJ22:** M' subject `Merge develop 81d2e5f4c415 into the KS-1274 branch (docs keep-both, gate76 step 2)` (82). **Default: yes.**
- **Q-PRED22:** add `"Seat R 21st"`, `"Seat V 1st"` and `"Seat V 2nd"` to the builder's PREDECESSOR_CLAIMS; `"Seat R 22nd"` stays absent. **Default: yes** (V 2nd's claim is in D2's message :43).
- **Q-OBJ22:** D2 reads PRESENT in the shared store (drafter). If R 22nd reads it ABSENT: STOP and mail rather than transfer? **Default: STOP and mail** (a transfer is a store write you have not ruled for this seat).
- **Q-LEGS67:** run legs 6/7 standalone in the worktree after S-1, before the real push, with a new advisory = STOP? **Default: yes** (F 6th's lesson 3; R 21st lost its push to exactly this).
- **Q-MATCH22:** beyond the R tokens, add `v 1st`, `v 2nd`, forward `v 3rd`, `f 6th`, forward `f 7th` to `OTHER_SEATS`? Drafter raw census: `"v 1st"`/`"v 2nd"`/`"f 6th"` = 0 quoted hits today; V 1st's WRAP :49 found the same gap in namecheck. **Default: yes, with a real-subject arm each.**
- **Q-ORDER1436:** #1436 (KS-808) appends to BOTH platform docs and is at READY FOR QA, not gated. **Default: #1427 lands first.** #1436 is re-predicted at its own gate. If #1436 somehow lands first, R 22nd's blobs are VOID: STOP, re-predict, mail.

## UNKNOWN / UNMEASURED (by the drafter; you measure or say so)
| item | why unknown | instrument that closes it |
|---|---|---|
| The REAL M', the in-hook preflight on M', Actions on M', qm on a real M' | nothing built or pushed | M-3 to M-6 |
| GitHub API facts about #1427 today (state, `mergeable`, `base.sha`, labels) | the drafter holds no Secuura GitHub identity | the PR API |
| D2's own Actions runs, and which workflows they cover | the drafter has no GitHub identity | `poll_actionsra22.py` by full `head_sha` |
| KS-1274's Linear state today (last read R 21st WRAP 23:37Z) | no Linear read | ITEM 0 (f) |
| Usage % | not read | Wednesday at send |
| Your pane, the floor, whether the boot pull runs | not known before launch | ITEM 0 (e), the SEND AMENDMENT |
| The lock floor | the drafter's `ls` read 0 with NO control | ITEM 0 (d), with a `mktemp -d` control |
| Who moved `rev-parse --all` from 1,651 to 1,654 | not attributed | not needed; record your own baseline |
| Whether legs 6/7 pass on M' | an EXPECTATION only (D2's locks pin 4.7.10; a new advisory may have landed since) | Q-LEGS67 |
| Reachability of the handlebars advisories in our code | never measured, and not needed | — |
| `run_armsra22.py`, the re-keyed matcher, the sweep | unbuilt | ITEM 0 (c) |
| The kit `--selftest` | not re-run by the drafter | known 13/15, with the symlink cause |
| The four platform suites; preflight legs 3/4/8; KS-1274's owed live trivy scan | no stack | — (Q-NULLRESULTS rides with the live scan) |

PROVENANCE:
- develop `81d2e5f4c415…`; #1427 branch == `refs/pull/1427/head` == `2b6da5f561b0…`; #1436 head == F 6th's branch `90d98754db7b…`; #1435 head `6f4adfe8835e…`; 2,160 refs, highest pull 1436; `-ra22-` 0 / `-ra21-` 0 / `-ra18-` 1 / `-ra13-` 2 | `env -u GIT_SSH_COMMAND git -C <Blockchain checkout> ls-remote origin` saved to a drafter scratch file + `grep -c` | read 2026-10-09 (UTC 02:47:17Z)
- D2 message, tree, ONE parent D1, author date; ancestry D1->D2 rc 0, reverse rc 1; D1..D2 = 5 lockfiles +18/-18; 0 overlap with #1427's paths (control returns the 2 docs); doc blobs unchanged | `git log -1 --format`, `merge-base --is-ancestor`, `diff --raw --numstat`, `comm -12`, `ls-tree` on the shared checkout (read verbs) | read 2026-10-09 (UTC ~02:44Z)
- D2 PRESENT in the shared store (negative control `deadbeef` absent); 64eafead and bf277eead present | `cat-file -t` on the shared checkout | read 2026-10-09 (UTC ~02:44Z)
- merge-base(head, D2) = `0a6177ea5482…`; head tree `9b6c3dfef865…`, one parent `0a6177ea5482…`; `04-container-trivy.sh` 100755 at D2; control commit trailers 55 B | `merge-base`, `log -1 --format`, `ls-tree`, `%(trailers) | wc -c` | read 2026-10-09 (UTC ~02:45-02:50Z)
- T'' `e948c77b8b46…`, blobs `b2bd07dbae40…` / `f4503e99d43e…`, guard 12/0, union hazard, cmp IDENTICAL to the kit (control rc 1); chain.json `0a9b940800d1fc38` | `c4_docs_gate76.py chain` rc 0 in a drafter bare repo with alternates to the shared store (out `…/scratchpad/r22/chain_1427_on_81d2/`) + `cmp` + `hash-object` | read 2026-10-09 (UTC ~02:46Z)
- T'' again, via merge-tree `d232875f8bf6…` (rc 1, two docs only) + private-index substitution; D1 control -> `57c9b5eaec95…` | `merge-tree --write-tree`, `GIT_INDEX_FILE` + `read-tree`/`update-index --cacheinfo`/`write-tree` in the same scratch repo | read 2026-10-09 (UTC ~02:45Z)
- D2..T'' 6 paths +94/-8, modes; head..T'' 14 paths +439/-22, 12 under `Blockchain/Dev/`; T'..T'' = the 5 locks; base..D2 non-doc = 12 | `diff --raw --numstat`, `--shortstat`, `--name-only | grep -c` in the scratch repo / shared checkout | read 2026-10-09 (UTC ~02:46-02:50Z)
- shared store `rev-parse --all` 1,654 / `f97ee53e189fd53b`; local + origin develop `ddea005553bf…`; local + tracking #1427 branch `2b6da5f561b0…`; `s-ra21-m1427` HEAD `dedc861c04a5…`, detached, porcelain 0; worktrees present (`s-f6-ks808`, `s-v1-hbslock`, `s-ra18-ks1274`, `s-g4-ks593`, `s-ra21-m1427`); 0 `.push-lock*` (no control); 518 entries; FETCH_HEAD mtime 8 Oct 13:41 | read verbs + `ls` on the shared checkout | read 2026-10-09 (UTC ~02:48Z)
- R 21st handover 130 lines `216792ecad1622ef`; R 18th handover `1081ef422c811c0d`; 14 R 21st tool hashes/lines == handover :98-111 | `shasum -a 256`, `wc -l` | read 2026-10-09 (UTC ~02:30-02:45Z)
- re-key census figures; matcher token counts; sweep class 9 sites; `MINE` at :102; fixture constants | `grep -o -i -E | sort | uniq -c`, `grep -o -F | wc -l`, `grep -n` on R 21st's copies (raw) | read 2026-10-09 (UTC ~02:45-02:52Z)
- GATE76 body 4,998 B / `91e3ee3a…`; report.md `58c3b8d1…`; kit hashes `af3a9c3b…` / `6013997a…` / `f14645aa…`; composed kit blobs == `b2bd07db…` / `f4503e99…` | `wc -c`, `shasum -a 256`, `git hash-object` | read 2026-10-09 (UTC ~02:47Z)
- subject lengths 82 / 80 | `printf %s | wc -c` | read 2026-10-09 (UTC ~02:50Z)
- launcher pins `claude-opus-5` (:664); KS-907 lines :244-380 | `grep -n` on `Launch_Claude.command` | read 2026-10-09 (UTC ~02:51Z)
- F 6th WRAP (0 locks, `s-f6-ks808` KEPT, #1436 READY FOR QA, lesson 3); V 1st/V 2nd WRAP (`s-v1-hbslock` left, v1-1 branch still at origin); gate78 VERDICT (GO #1435 at `6f4adfe8835e`) | read of `fleet/briefs_staged/2026-10-09_seat{F6,V1,V2}_*.txt`, `2026-10-09_gate78_VERDICT.txt` | read 2026-10-09
- R 21st rulings (re-predict not re-gate; KEEP worktree; hoist approved; START-word shape; Opus 5.5 by idle `/model`) | `briefs_staged/2026-10-09_seatR21_ANSWER_{plan,ctx_hoist,refused}.md` | read 2026-10-09
- STANDING_LINES 448 lines, sha256/16 `6d8166bac3139428` | `wc -l`, `shasum` | read 2026-10-09 (UTC ~02:52Z)

SELF-CHECK: re-read end-to-end for contradictions | drafter 2026-10-09 ~13:55 AEDT
