LAUNCH BRIEF (Seat K 2nd, DRAFT; not sent): pane `Secuura/Blockchain-K`, successor of Seat K 1st. **ONE job: finish KS-1402.** Seat K 1st built, tested and SAVED ITEMS 1-3 in worktree `s-k1-ks1402`. **Nothing is committed.** You (Seat K 2nd): (0) prove the saved state, (R) re-key ONLY the push-path tools, (4) make ONE commit and the push, on Wednesday's per-step word, (5) raise the PR by REST and send ONE `READY FOR QA (Seat K 2nd): #<n> (KS-1402) -> gate<NN>` **(tier 1: auth/credential surface; never the local models)**, then WRAP. No merge, no merge-in, no deploy, no Linear write, no message to Peter or Stuart. Secuura NEVER force-pushes. Model: **Opus 5.5**.

> Drafted by Wednesday's brief-drafting sub-agent, 2026-10-09 04:27-04:4xZ (15:27-15:4x AEDT). Built from K 1st's SEND brief, Wednesday's seven ANSWERs to K 1st, K 1st's five mails and K 1st's handover, all read WHOLE. Every value carries its instrument. A value marked "drafter" is the drafter's own read: RE-MEASURE it before you rely on it. **Wednesday adds the SEND AMENDMENT and rules the four questions at send.**

## 🔴 READ FIRST, WHOLE: K 1st's HANDOVER
- `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatK1-2026-10-09.md` (drafter: 154 lines, sha256 `0ffbae86387b455f7c97042be7ef740e58d04441e590784ae55b212dd3544a1b`, re-hashed by the drafter at 04:27Z, equal to Wednesday's `0ffbae86387b455f`).
- **Its "FOR K 2nd, THE FIRST THREE THINGS" (`:1-62`) is AUTHORITATIVE for you.** This brief points at it; it does not replace it. Where this brief and that section disagree, mail before acting.
- Also read whole: K 1st's SEND brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-09_seatK1_build_ks1402_SEND.md` sections THE MECHANISM, ITEM 4, ITEM 5, HOLDS (414 lines; this brief restates what binds you, so read the rest only on need).

## MODEL
- Kam, 2026-10-09 ~09:4x, verbatim: *"for now, use Opus 5.5 for all sub agnets"* (top block of `0_Brain/learnings/2026-10-09_spark-ornith-sonnet-only-until-monday.md`).
- Your launcher pins `claude-opus-5`. Wednesday types `/model claude-opus-5-5` into your pane at its IDLE prompt (a tap would arrive as a message, not a command) and sends you a resume pointer by mail. **Do not wait for it.**
- Put `MODEL: <as your session reports it>` in every STATUS, QUESTION, READY and WRAP mail.

## USAGE AUTHORITY
- Kam's standing week instruction, renewed to **Sun 11 Oct** (`0_Brain/tasks/WEEK-INSTRUCTION.md:5`, `:10`; card `wed-week-instruction-lapses-1004` = a), verbatim: *"do as much work with the spark and claude agents on the secura projects as you can"*. **Clause: raise.** Card `secuura-ks1402-s-key-cannot-carry-users-read-1006` = a: *"A K build round, then the QA gate, then a merge."*
- **Routing:** credential surface, fails the Spark predicate. This seat carries 0 Spark tasks and says so.
- Usage at draft: **23%** (`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check` rc 0, "weekly usage 23% < 90% (gauge age 2 min)", 04:28Z). The normal 90% stop applies; no `WED_USAGE_STOP`.
- **Ctx lines:**
  - The re-key (ITEM R) starts only under **45%**, on Wednesday's read in the plan ANSWER.
  - The commit and the push go only on **Wednesday's per-step word** (`QUESTION: ctx read, may I push`).
  - **65% = WRAP COLD at the next safe boundary** (after a tool is proven, after the push's `.rc` + `ls-remote`, or after the raise's read-back). Never mid-commit, never mid-push.
  - **A seat cannot read its own context %.** K 1st's own estimates ran ~10 points above Wednesday's statusline reads (handover `:125`). Ask; do not estimate.
  - **Budget arithmetic** (Wednesday's 04:16:36Z ANSWER to K 1st): about **2.7 points per tool re-key** (24% at 03:27Z → 32% at 03:40Z over three tools). Seven path tools ≈ 19 points. Mail the plan by ~20%.

## BLUF
- **The change is built.** K 1st's mechanism, a reading of Kam's ruling confirmed by Wednesday: originate validates the email with auth's zod schema, normalises `toLowerCase().trim()` on the value AS SENT, then `lookupHash`. It reads `SELECT id FROM users WHERE email_lookup_hash = $hash AND (tenant_id IS NULL OR tenant_id = $tenant::uuid) LIMIT 1` on the request's db. No token, no new secret, auth unchanged, no scope moved. The act gate at `:1599` is byte-unchanged and runs first (handover `:66-74`).
- **The saved state (drafter, read verbs only, 04:27:42Z):**
  - worktree `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-k1-ks1402`: HEAD `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6`, detached (`branch --show-current` empty);
  - `git status --porcelain` = **7 ` M` + 1 `??`**, exactly the handover's list (`:34-38`);
  - patch `5_Project_History/2026-10-09_seatK-1st/evidence/KS-1402-items1-3-diff.patch`: sha256 `ab8e9e441864e05c35fe1c99adf8feaf0f65a358d8c0070fe2a5c316743bba73`, 88593 B, 8 `diff --git` headers.
  - All three equal the handover. **You re-measure them at ITEM 0(c); the patch is regenerated from the worktree, not only re-hashed from disk.**
- **develop MOVED since K 1st's base.** Drafter's `ls-remote` 04:27:28Z: develop = **`349b35c9163ac59209366adb7a4a89d8779bd6d6`**. That is the squash of #1427 (KS-1274), merged 04:20:00Z per Seat R 22nd's WRAP, and verified at source by Wednesday.
  - #1427 touched the trivy job, its tests and BOTH platform docs (flow `35.`, cheat `KS-1274`). It touched none of your code files (drafter: three-dot file set of #1427 head `ec94946e3be9` = 6 files, 0 of yours).
  - **`349b35c9163a`'s objects are ABSENT from the shared store** (drafter: `cat-file -e` rc 128; `81d2e5f4…` rc 0 as the positive control; `deadbeef…` rc 128 as the negative, same call).
  - **This does not touch your round.** Your commit sits on the ACCEPTED base `81d2e5f4c415` (Wednesday's 03:38:08Z ANSWER, "build on it"). **No merge-in this round.** Never rebase, never force-push (`.githooks/pre-push:46-70`).
  - **Sequencing, plainly:** you raise on base `81d2e5f4c415` → a QA gate measures your head against its own base (Q-DOCSMERGE) → **a merge seat (the R lane) merges develop IN, keep-both on both docs, and REGENERATES `secuura-api.yaml`**, before any merge. That happens after #1427's blocks (already on develop) and after whatever gate77 lands, #1429's yaml included.
- **`secuura-api.yaml` is SEQUENCED-AFTER #1429** (KS-1449, gate77; head `1271d9597c43`, unchanged since K 1st's read). #1429 is the ONLY open head that touches it (drafter: three-dot sets of #1383 #1427 #1429-#1434 #1436; yaml count 1 in #1429, 0 elsewhere; each head's 2 doc paths = the positive control). Whichever lands second merges develop IN and regenerates. Never hand-merge it.
- **Expect ONE commit, ONE push, ONE PR, ONE READY, then WRAP.** Never end a turn on a "next up" line with nothing running (STANDING_LINES `:342`; Wednesday's 03:46Z resume ANSWER to K 1st).

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** Where your copy of a tool and this brief disagree about a gate, a knob, a path or a line number, **THE TOOL WINS**: run nothing on the disputed point, and mail.

**WAKE:** your re-seated `inbox_watchk2.sh`, armed in the background at boot with `run_in_background` and `timeout: 7200000`.
- A `nohup` waiter does NOT wake the pane; a harness-tracked one does (handover `:123`).
- It EXITS when it fires: re-arm IN THE SAME ACTION that reads each mail, with `SINCE` = the newest mail READ (STANDING_LINES `:403`).
- After any long action (push, raise), LIST the inbox by API before the next ref write.
- Name a watcher pid only from a `ps` FILE. Stop every watcher before WRAP and prove 0 live with a positive control.

## THE FLOOR (one checkout, one inbox `secuura-blockchain@agentmail.to`)
Drafter's reads at 04:27:53Z: `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'`; locks by `find -maxdepth 1 -name '.push-lock*'` in `worktrees/`.

| Seat | Pane | Token / lock | Files | Doc block |
|---|---|---|---|---|
| **K 2nd (you)** | `Secuura/Blockchain-K` (id by mail) | `k2` / **`.push-lock-g1`**, holder `Secuura/Blockchain-K k2` | worktree `s-k1-ks1402` (ADOPTED CHECKOUT, not naming rights); the 8 declared files below | flow `44.`, cheat `KS-1402` LAST (built) |
| Wednesday | `%0` `wednesday` | — | — | — |
| gate77 | `%10` `QA/Secuura-gate77` | the gate takes no lock | gating #1429-#1434 + #1436 at develop `349b35c9163a` (`gatesets/2026-10-09_gate77/head_at_launch.txt`: `D 349b35c9…`, `S Seat R 23rd`) | — |
| R 23rd (NOT launched at 04:27:53Z) | `Secuura/Blockchain-R` when launched | `.push-lock-d8` | gate77's merge seat: docs-only keep-both merge-ins of #1429-#1436 + #1429's yaml regen (`RULINGS_wednesday.md:48-51`, `:111`) | — |
| monitor | `%1` `fleet-monitor` | — | — | — |

- **Locks: 0** `.push-lock*` at `worktrees/`; a private `mktemp -d` control with a planted `.push-lock-PLANTED` read **1**. `.push-lock-g1` is a WAIT entry by path in the R lineage's lock tool (`2026-10-09_seatR-22nd/tools/lockra1.sh:303`), which R 23rd copies.
- **`s-k*` worktrees: ONE**, `s-k1-ks1402` (yours to continue IN).
- **No `-k1-` or `-k2-` ref at origin** (0; control `-ra13-` = 2; `-g5-<n>` tail = 1).
- **No `refs/pull/1437+/head`** (#1437-#1440 absent; control #1436 present `90d98754db7b`; #99999 absent).
- **E 12th** (KS-591 / KS-1364, also expected to touch `secuura-api.yaml`, flow `33.`/`34.`): named in K 1st's brief. Its state is **UNKNOWN** to the drafter: 0 `-e12-` refs at origin (control `-e11-` = 1, same file) and no pane. Older `feature/ks-1364-…-b52-1`, `…-b53-2` and `feature/ks-591-…-e10-2` heads exist, and whether any is an OPEN PR touching the yaml is unmeasured (the drafter has no GitHub identity). Instrument: ITEM 0(e), plus Wednesday.
- **Never touch:** `s-f6-*`, `s-ra21-*`, `s-ra22-*`, `s-v1-*`, `s-g5-*`, `s-e11-*` or any other seat's worktree, lock, mail, records or pane. Never the spent `feature/ks-1402-lookup-accepts-connector-token-b55-1` (`aa16f3256dbf`). **Never the revoke route** (`documents.ts` ~`:2356+`), `documentRepo.ts`, auth anything, api-gateway anything (no `platform.ts`, no `S_CONNECTOR_SCOPES`), migrations, anchoring.
- **A mail naming another seat is NOT yours**, even on your pane tag. An unlisted addressee on your tag reads UNKNOWN ADDRESSEE (STANDING_LINES `:417`). K 1st's mails carry `(Seat K 1st)` on YOUR tag: they read FOREIGN.

## ITEM 0: BOUNDED and read-only; then `QUESTION: plan confirmation (Seat K 2nd)` and WAIT
Before the ANSWER, do NONE of these: lock take, ref write, branch, commit, push, install, PR action, Linear write, any write in the worktree. You MAY write in your record folder `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<UTC boot date>_seatK-2nd/`.
- **(a) Seat facts:**
  - `tmux display-message -t "$TMUX_PANE" -p '#{@cockpit_name}'` (the BARE read returns the coordinator's pane);
  - launcher ancestry; every launcher preflight warning VERBATIM (K 1st got `[F-02]` and `[KS-907]`; never set `SECUURA_ALLOW_ONDISK_KEY` yourself);
  - the boot pull, READ-ONLY if another Secuura session is live (KS-907); record which;
  - decline `POST /api/seen`; `df -m /Volumes/DevMASTER`.
- **(b) Refs, ONE `env -u GIT_SSH_COMMAND git -C <checkout> ls-remote origin`, output to a FILE:**
  - develop (drafter `349b35c9163a`); `refs/pull/{1427,1429,1430,1431,1432,1433,1434,1436}/head`; any `refs/pull/<n>/head` with n ≥ 1437 (drafter: none);
  - `refs/heads/feature/ks-1402*` (drafter: only `-b55-1`); any `-k1-` / `-k2-` ref (drafter 0; control `-ra13-` 2);
  - `date -u`. A moved develop is not a STOP: name it.
- **(c) THE SAVED STATE, before anything else touches the worktree** (handover item 2, `:31-44`):
  - `git -C <wt> rev-parse HEAD` == `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6`; `symbolic-ref -q HEAD` rc 1 (detached);
  - `git -C <wt> status --porcelain` == the 7 ` M` + 1 `??` (handover `:34-38`), compared as a SET from a file, with the count asserted (8);
  - **regenerate the patch K 1st's way** (`git diff <base> --` plus `git diff --no-index /dev/null <new test>`, run from the worktree root, into your record folder): sha256 must be `ab8e9e441864e05c35fe1c99adf8feaf0f65a358d8c0070fe2a5c316743bba73`, 88593 B, 8 files. **A different sha256 is a STOP and a mail. Do not repair.**
  - `packages/shared/dist/index.js` present in the worktree (K 1st built it); `Blockchain/Dev/node_modules/.bin/jest` present; the four ROOT `systemTest/*/package.json` dirs each have `node_modules` (STANDING_LINES `:432`: enumerate from `git ls-tree`, REFUSE on 0, assert 4).
- **(d) The floor:** panes as above; locks ATTRIBUTED by holder `seat`, two polls a minute apart, control in a private `mktemp -d` (never plant in the shared `worktrees/`, STANDING_LINES `:446`).
- **(e) Open PRs touching your files, by the GitHub API, paginated**, then each one's `/files`. K 1st measured 30 open, 0 of 21 unnamed ones touching your files or the docs (plan mail, 03:1xZ); the drafter holds no Secuura GitHub identity and measured only the nine named heads.
- **(f) Tools:** the copy receipt (TOOLS). Verify the 3 already-re-keyed tools against `wrap/TOOL_HASHES_k1_for_K2.txt`.
- **(g) Linear, read-only, by id:** KS-1402 (state, assignee, `updatedAt`, `comments(first:50)` sorted client-side). Drafter's expectation, from K 1st: In Progress; 5 comments, newest `7740c258`; `updatedAt` 2026-10-09T02:07:01Z. Add KS-99999 in its OWN query as the fabricated-key control.
- **Your plan confirmation carries:** (a)-(g) one block each; the launcher lines VERBATIM; your answer to each QUESTION below with your measured recommendation; a ctx read request. **Budget: mailed by ~20% ctx.**

## ITEM R: RE-KEY THE PUSH PATH (after the plan ANSWER, under 45%)
**In handover order (`:7-29`), writing NEW `*k2*` files. Never edit the copies, never run a tool from another seat's folder.**
1. **Re-seat K 1st's three PROVEN tools to `k2`:** `inbox_matchk1.py` `caeaa43d0e012d28` (559) → `inbox_matchk2.py`; `inbox_watchk1.sh` `54782d68234bb791` (176) → `inbox_watchk2.sh`; `lockk1.sh` `cc31dd2f56a0bd8c` (602) → `lockk2.sh` (`LOCK_SEAT='Secuura/Blockchain-K k2'`; the LOCK name gate stays `.push-lock-g1`).
   - Matcher: `MINE = "k 2nd"`. **MOVE `k 2nd` OUT of OTHER_SEATS** (K 1st forward-added it). **ADD `k 1st`**, forward-add `k 3rd` and `r 23rd`, each with its `seat …` form. Do this by byte-span edits from the AST. Verify by `ast.literal_eval` + `tag()` run from source truncated at `end_lineno` (importing RUNS the poll).
   - **Do not assume which list wins.** Seat R 22nd measured that its own lineage's `tag()` tests `MINE` BEFORE `OTHER_SEATS` (`HANDOVER-seatR22-2026-10-09.md` item 2). Your matcher is the G-kit lineage. Drive the 2x2 on FULL-LENGTH real subjects: this brief reads FOR ME; a real `(Seat K 1st)` subject on your tag reads FOREIGN; `(Seat K 9th)` on your tag reads UNKNOWN ADDRESSEE; the pre-key copy as the inverting control.
2. **`commitg1.sh` → `commitk2.sh`:**
   - **The `:68` fix:** it counts changed paths with `git diff --name-only`, which is blind to the untracked new test. Count with `git status --porcelain`. Prove it with a planted stray file (in a scratch COPY of the worktree state, never the real worktree) that must make it REFUSE.
   - **`:70-72` hard-codes "exactly 3 changed paths"**: yours is **8**, matched as a SET against the declared list, not only a count.
   - `W`, `BRANCH`, `BASE`, the lock tool name, the trailer and closing-word checks: re-key every lane-bearing literal. `mkdir -p "$REC/boot"` before the first take.
3. **`pushg1.sh` → `pushk2.sh` + the TWO fixes Wednesday approved at 03:27Z** (ANSWER_plan, "Accepted findings"):
   - `:233` `python3 "$R/gatelinesg1.py" … | grep -E 'VERDICT|OK$|MISMATCH' || true` is decorative twice: a missing file is swallowed by `|| true`, and a present file's `VERDICT: MISMATCH` is discarded because the pipeline's status is grep's.
   - The fix: an existence assert on `gatelinesk2.py`, with a planted-absence control; read the gate's rc UNPIPED; decide the push's exit on that rc.
   - Re-seat the co-tenant set (STANDING_LINES `:418`).
4. **`pathgateg1.py` → `pathgatek2.py`**, whose declared set is EXACTLY the 8 files below. It never names `scripts/audit/audit-baseline.json` or any `package-lock.json`. Prove it with a firing control.
5. **`gatelinesg1.py` → `gatelinesk2.py`; `keyscang1.py` → `keyscank2.py`; `raiseg1.py` / `raise_rest_g5.sh` → `raisek2.py` / `raise_rest_k2.sh`; `provenance_ra20.py` → `provenance_k2.py`.** `docblockra3.py` needs NO re-key (K 1st measured 0 live predecessor tokens).
- **The generic clause binds and comes first:** env names, LOCK_SEAT, ref namespaces, worktree paths, log/artefact names, fixtures, banners, live 12+-hex constants outside comments (`:422`), generation predicates (`:395`), env set-equals-read (`:305`). Build the token list from EVERY generation each file names (`g1`, `g5`, `ra20`, `k1`; STANDING_LINES `:293`, `:428`). Print `N checked` per tool.
- **Namespace forms of your token:** `k2`, `-k2-`, `s-k2-`, `seatk2`, `Seat K 2nd`, `k 2nd`. **Your worktree keeps its `s-k1-` name**: it is an ADOPTED CHECKOUT, not naming rights (the E 3rd precedent at `namecheckg1.py` `ADOPTED_WORKTREE`). Your tools take its path as a declared constant, and your branch carries `-k2-` (Q-BRANCH-K2).
- **HELD verifiers** (`namecheckg1.py`, `bannercheckg1.py`, `rekey_checkg1.py`, `trap4_g1.py`, `twolockg1.sh`): per Q-HELD-VERIFIERS. Whatever is held is DECLARED NOT RE-KEYED in your WRAP, with the cost stated.
- **Then mail `STATUS: tools re-keyed (Seat K 2nd)`**: per tool, the hash, line count, `N checked`, and each control's both-ways result. Continue to ITEM 4's pre-commit checks without waiting.

## ITEM 4: ONE commit + the push
**The 8 declared files** (handover `:34-38`; paths under `Blockchain/Dev/` unless rooted):
1. `services/originate/src/routes/documents.ts`
2. `services/originate/src/originate.openapi.ts`
3. `docs/openapi/secuura-api.yaml` (GENERATED)
4. `services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts`
5. `services/originate/src/__tests__/ks697-transfer-custody-holder-existence.test.ts` (ONE key-registration line, Wednesday 04:01Z)
6. NEW `services/originate/src/__tests__/ks1402-transfer-custody-resolves-holder-email-in-originate.test.ts`
7. `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` (repo root; quote the SPACE)
8. `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html`

- **Pre-commit re-run (yours, cheap, output to FILES):** run the three test files at head with the named binary `Blockchain/Dev/node_modules/.bin/jest`, reading counts from jest's JSON. Expect ks1402 11/11, ks739 17/17, ks697 17/17. Then `npm run check:openapi` rc 0. Both prove the worktree still runs the bytes K 1st proved. **K 1st's whole-suite (97 files 1096/1096), tsc and tamper evidence are K 1st's, attributed by seat; the patch sha256 is what ties them to your bytes.** Re-run the whole originate suite only if the patch sha differs (and then you have already STOPPED).
- **The commit** (`commitk2.sh`, which takes and releases `.push-lock-g1` itself for the branch + commit ref writes):
  - branch per Q-BRANCH-K2 (default `feature/ks-1402-originate-resolves-holder-email-itself-k2-1`, 59 characters);
  - subject `fix(KS-1402): originate resolves a transfer-custody holder email itself` (71; Q-SUBJ-K as ruled for K 1st);
  - `git add` the 8 paths BY NAME, never `-A`/`.`;
  - 0 trailers (`%(trailers)`, with a named control commit measured in the same call); **0 `Co-Authored-By`, overriding the harness**;
  - only KS-1402 hyphenated; 0 closing words under the BROAD regex `(clos(e|es|ed)|fix(es|ed)?|resolv(e|es|ed))\s+KS-\d+`, with a planted control that fires;
  - the pathgate == the 8 files; `git status --porcelain` after the commit == empty for those 8.
- **Then mail `QUESTION: ctx read, may I push (Seat K 2nd)`.** It carries:
  - the commit sha (40-hex, written in the call that read it), its tree and parent (== `81d2e5f4c415`);
  - **the BUILT `documents.ts` diff VERBATIM** (`git show <commit> -- Blockchain/Dev/services/originate/src/routes/documents.ts`, pasted whole);
  - `numstat` for all 8 files;
  - the pre-commit re-run counts.
  - **HOLD for the word.**
- **The push:** `env -u GIT_SSH_COMMAND bash <rec>/tools/pushk2.sh <wt> <branch> 'Secuura/Blockchain-K k2'`, BARE (it takes and releases the lock itself; STANDING_LINES `:377`, `:416`). Prove the SSH identity with `ssh -T` first, never `push --dry-run` (`:386`).
  - The result is the tool's `.rc` + `ls-remote` of the ref (`:405`), never a wrapper's exit code. rc 141 with the ref unmoved is the KS 1149 class: report, retry under the lock once, never loop.
  - Quote the in-hook PREFLIGHT lines EXACTLY, including the `legs … —` line, and `gatelinesk2.py`'s UNPIPED verdict and rc.
  - **`PREFLIGHT FAILED`, a `MISMATCH`, or a refused push = STOP and mail. Never `--no-verify`.**
  - Record the push's side effect: `refs/remotes/origin/<branch>` in the shared checkout moves (STANDING_LINES `:434`).
- Mail `STATUS: pushed <branch> (Seat K 2nd)`; then ITEM 5 without waiting, unless the push ANSWER said otherwise.

## ITEM 5: raise + ONE READY
- **Raise by REST** (`raise_rest_k2.sh`), base `develop`, title `KS 1402: originate resolves a transfer-custody holder email itself` (66; the #1431 shape). HTTP 201, `head.sha` == origin's ref, the body's sha256 read back.
- **Read `mergeable` / `mergeable_state` once and REPORT it; do not act on it.** A conflict on the docs or the yaml is expected (develop carries #1427's blocks): it is the merge seat's keep-both, never yours.
- **The body (written by YOU) carries:**
  - `Refs KS-1402` + `https://linear.app/secuura/issue/KS-1402`;
  - Kam's ruling verbatim with the card id (`secuura-ks1402-s-key-cannot-carry-users-read-1006` = a, `2026-10-06T09:58:21+11:00`), the mechanism in one sentence, and "a reading of the ruling, confirmed by Wednesday (2026-10-09 03:07:58Z send amendment)";
  - **the headline (C2):** the tenant guard is NEWLY load-bearing for connectors. At base, auth refused the connector before its tenant compare ran; now the bound tenant predicate is the only thing between a connector and another tenant's user. C2 pins that; C2b pins the interactive case, green at both;
  - **the ruled mechanism is STRICTER than auth's path:** `users.ts:306` skips the tenant compare when either side is falsy (Wednesday ANSWER_plan);
  - **RLS stated honestly:** the bound predicate is the enforcement and the GUC is belt-and-braces. Do not claim two working layers;
  - **the failure-mode change, on its own line:** a DB failure during resolution now lands in the outer catch, `500 INTERNAL_ERROR 'Failed to transfer custody'`, where the id path's `users` read already lands; before, the only failure here was auth unreachable (502). DELIBERATE, accepted by Wednesday 04:01Z;
  - **the deploy requirement:** originate needs `PII_LOOKUP_HMAC_KEY` (docker-compose `:601`). The registration is TWO-condition (`PII_ENCRYPTION_KEY` AND `PII_LOOKUP_HMAC_KEY`; `index.ts:370` + `encryptedField.ts:632-633`), and nothing refuses to start without the second. Without it every email transfer answers a labelled 502 (C9);
  - Stuart's measurement by date (7 of 7 at 403, 2026-10-05); the precedent (`documents.ts:1799-1805`, auth's `toLowerCase().trim()`);
  - Test Evidence: touched / ran (K 1st's runs attributed to K 1st, yours to you) / NOT run / "no migration, no config, no scope change";
  - **SEQUENCED-AFTER:** `secuura-api.yaml` after #1429; both docs keep-both after #1427 (merged) and gate77's rows; "this branch is on `81d2e5f4c415`; the merge seat merges develop IN and regenerates";
  - **NOT COVERED:** `live sweep owed` (lowercase, SKILL §5f); no S↔K pair run (Stuart's `PS 992` cell needs a Kintsugi deploy, Kam's tap); Q-LEGACY (a plaintext-email user without a lookup hash resolved at base via auth's legacy fallback and 404s at head; count unmeasured); the KS 1406 class not addressed, `/lookup` unchanged; the four platform suites not run.
  - Foreign keys de-hyphenated (`KS 739`, `KS 697`, `KS 1406`, `PS 992`, `KS 593`, `KS 1449`, `KS 1274`, `KS 1061`).
- **ONE READY:** `READY FOR QA (Seat K 2nd): #<n> (KS-1402) -> gate<NN>` **(tier 1: auth/credential surface)**.
  - `<NN>` is UNKNOWN at draft: gate77 is live and gate78 is spent on #1435 (`ls fleet/qa-agent/gatesets/`). Wednesday names it in the push ANSWER; if she has not, write `gate<NN>` literally and say so.
  - It carries the five READY artefacts (STANDING_LINES `:27-41`): head and develop read by `ls-remote` in the SAME action; every cell mapped base/head (K 1st's 11 cells; ks739 17 retired (21 executed) + 3 re-pointed (4 executed), BASE 0/17 → HEAD 17/17; ks697 16/17 → 17/17); every tamper (14 rows) mapped to its cell; NOT COVERED; `mergeable_state`.
  - Also: KS-1402's `updatedAt` 2026-10-09T02:07:01Z with its comments unchanged (Wednesday: mention it, do not investigate).
  - **The ticket comment naming the PR is Wednesday's batch:** say so.
  - 🔴 Write a 40-hex value, byte count or ratio ONLY in the tool call that measured it.
- Then WRAP.

## HOLDS
- **No merge, no merge-in, no deploy, no demo or Kintsugi, no live sweep, no `az`, no SSH beyond the push transport and its `ssh -T` probe, no migration, no Docker** beyond what the pre-push hook runs. No objects transfer (develop's new objects are not needed this round).
- **No key rotation, no re-mint, no edit to `S_CONNECTOR_SCOPES` or `platform.ts`, no auth-side change, no new secret or env var, no new token.** Signature classes pause for Kam: production · money · external communication to any human · anything irreversible.
- **No Linear write of any kind.** The ruling comment promised to Stuart and the PR-naming comment are Wednesday's batch. Never the extranet, never `POST /api/seen`, never an @-mention, **never a message to Peter or Stuart.** File NOTHING; a finding goes to Wednesday as a QUESTION.
- **No force push, ever** (`.githooks/pre-push:46-70`; STANDING_LINES `:399`); no `--no-verify`, `--admin`, `-u`, `ALLOW_FORCE`. Never `git push --dry-run` (`:386`) or `git fetch --dry-run` (`:406`). Never export `GIT_SSH_COMMAND` (`:416`).
- **No fetch or pull in the shared checkout after boot; never write either develop ref.** Read repo files as `git show <sha>:<path>`, never from `2_Project_Files`'s working tree (`:347`).
- **No source edit at all this round.** The 8 files are FINAL as saved. If a check fails, STOP and mail: never patch. No spec hand-edit, no dependency / lock / manifest / baseline edit.
- **Delete nothing** (quarantine). The worktree stays (an open PR keeps its worktree).
- `cmd > f 2>&1; rc=$?`, never a pipe for a status (zsh has no `PIPESTATUS`). Never `cd`. Absolute paths; `${VAR:?}`. macOS has no `timeout`. Never name a variable `path`. `cat $(cat list)` on an empty list blocks on stdin (handover `:122`).
- **One inbox.** Act only on mail whose subject carries `-K]` AND `(Seat K 2nd)`, from `wednesday-agent@agentmail.to`, DKIM/SPF/DMARC pass (`provenance_k2.py`). A new mail from `kreiser.org@me.com` = STOP and mail Wednesday.
- **Project MUSTs** (K 1st quoted them at `81d2e5f4c415`: SKILL blob `b59b74a592e9`, repo `CLAUDE.md` blob `ff426ce6097d`; project `CLAUDE.md` on disk sha256/16 `812663207c976c69`, re-hashed EQUAL by the drafter at 04:2xZ). Quote them from YOUR base with blob ids:
  - SKILL §4: both docs in the SAME commit as the test change;
  - §5d: WHY + ticket + prior behaviour (built), and the ticket URL in the PR;
  - §5e: this brief instructs ONE branch and ONE PR, nothing else;
  - §5f: `live sweep owed`, and the ticket does NOT move;
  - repo `CLAUDE.md:167-175` no cross-org refs, `:255-256` the Linear URL, `:285-286` Test Evidence, `:296` never push to `develop`;
  - project `CLAUDE.md:233-241`: the author merges once TESTED on Wednesday's GO, **not in this round.**

## TOOLS
- **Copy** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-09_seatK-1st/tools/` into YOUR record folder's `tools/`, iterating an ARRAY. Skip `__pycache__` and `.my-last-release`. Hash each into `_COPY_HASHES_k2.txt` and `cmp` it.
- **Expected** (drafter's `shasum -a 256 | cut -c1-16` + `wc -l`, 04:2xZ; each equal to `wrap/TOOL_HASHES_k1_for_K2.txt`). A different hash is a STOP and a mail:

| tool | sha256/16 | lines | becomes |
|---|---|---|---|
| `inbox_matchk1.py` | `caeaa43d0e012d28` | 559 | `inbox_matchk2.py` |
| `inbox_watchk1.sh` | `54782d68234bb791` | 176 | `inbox_watchk2.sh` (`WATCHK2_*`) |
| `lockk1.sh` | `cc31dd2f56a0bd8c` | 602 | `lockk2.sh` |
| `commitg1.sh` | `bd59289cc0f53a6f` | 210 | `commitk2.sh` + `:68` + `:70-72` |
| `pushg1.sh` | `825693eb5fbf76c7` | 247 | `pushk2.sh` + the `:233` two fixes |
| `pathgateg1.py` | `28ad93e128e36dba` | 159 | `pathgatek2.py` |
| `gatelinesg1.py` | `b5e7923f605af9da` | 73 | `gatelinesk2.py` |
| `keyscang1.py` | `e85a0c6e624087c9` | 56 | `keyscank2.py` |
| `raiseg1.py` / `raise_rest_g5.sh` | `3c9d92463eb92a45` / `d109febb06cd17d1` | 260 / 37 | `raisek2.py` / `raise_rest_k2.sh` |
| `provenance_ra20.py` | `d215ce0275a6e3f9` | 91 | `provenance_k2.py` |
| `docblockra3.py` | `c4827645b53bce19` | 168 | unchanged |
| `namecheckg1.py` | `f3cbad9a834f2192` | 1199 | HELD unless Q-HELD-VERIFIERS says otherwise |
| `bannercheckg1.py` / `rekey_checkg1.py` / `trap4_g1.py` / `twolockg1.sh` | `1ce35951d965279b` / `a1f28f4215db5515` / `6deaf8d1041ccaef` / `8de9efea404fd88e` | 244 / 932 / 284 / 199 | HELD |

- K 1st's own harness and fix scripts (`fix_ks1402*.py`, `rewrite_ks739.py`, `tamperk1.py`, `suite_before_after_k1.py`, `jestsum.py`) are copied as RECORD only. You make no source edit, so you run none of them.
- Lock arms run from a COPY of the tool in a scratch dir (STANDING_LINES `:419`); controls go in a private `mktemp -d` (`:446`). The unattributed-lock catch-all is CODE, and it prints how many dirs it CHECKED (`:402`).

## MAIL FORMATS (to `wednesday-agent@agentmail.to`; prefix `[Secuura/Blockchain-K -> Wednesday] `; every subject names `(Seat K 2nd)`)
- `QUESTION: plan confirmation (Seat K 2nd)` · `QUESTION: ctx read, may I push (Seat K 2nd)` · `QUESTION: <topic> (Seat K 2nd)`. One question per mail; body Context / Question / Meanwhile / Needed-by. Launcher preflight warnings go VERBATIM in the plan mail.
- `STATUS: tools re-keyed (Seat K 2nd)` · `STATUS: pushed <branch> (Seat K 2nd)`.
- ONE `READY FOR QA (Seat K 2nd): #<n> (KS-1402) -> gate<NN>`.
- `WRAP (Seat K 2nd): …`. Include:
  - `MODEL:`, plus an honest note of anything that felt beyond the model;
  - 0 watchers and 0 locks of yours, from a ps FILE, with a positive control;
  - **EVERY REF WRITE:** the local branch (by the commit tool), the commit, the push and its `refs/remotes/origin/<branch>` side effect;
  - RESUME naming the branch IN FULL with its head;
  - UNMERGED / UNMEASURED / UNFILED;
  - `df -m` before/after; drive hygiene (worktree `s-k1-ks1402` KEPT for the open PR);
  - the tools DECLARED NOT RE-KEYED, with the cost; the tool hashes a K 3rd or the merge seat inherits;
  - the handover `5_Project_History/HANDOVER-seatK2-<date>.md`, opening "FOR THE NEXT K SEAT AND THE MERGE SEAT, THE FIRST THREE THINGS" (the merge-in needs, the yaml regen, the HMAC deploy requirement);
  - the history entry at the TOP of `history.md`, insert-only proved;
  - "this seat = 1 Claude launch, clause: raise (carrying 0 Spark tasks)".

## QUESTIONS (OPEN; Wednesday rules at send or in the plan ANSWER; each HOLDS only what it names)
- **Q-BRANCH-K2 (HOLDS the commit).** K 1st planned `feature/ks-1402-originate-resolves-holder-email-itself-k1-1`; the re-keyed name is `…-k2-1` (both 59 characters).
  - **Measured from the tools, not taste:** namecheck's ownership test is `_MINE_BRANCH = re.compile(r"-" + MINE + r"-[0-9]+$")` (`namecheckg1.py:428`). The lineage's recorded rule is that a branch carrying a predecessor's token "reads as a dead seat's ref to every other seat's namespace sweep, and `_MINE_BRANCH` … would refuse it" (`:498-499`, G 5th re-slugging away from `-g4-`).
  - The one precedent for pushing under a predecessor's token is B 45th's adoption of seven branches that ALREADY EXISTED at origin (`:180-183`, "renaming would create seven new refs that prove nothing new"). Here 0 `-k1-` refs exist (drafter `ls-remote`, control `-ra13-` 2). Nothing is saved by adopting `k1`, and it would have to be an ADOPTIONS entry.
  - The worktree `s-k1-ks1402` is a CHECKOUT, not naming rights (E 3rd's `ADOPTED_WORKTREE` note, same file).
  - **Recommend / default: `feature/ks-1402-originate-resolves-holder-email-itself-k2-1`.**
- **Q-HELD-VERIFIERS (binds ITEM R).** K 1st held 5 verifiers, with Wednesday accepting the trade at 03:40Z.
  - None of the five is on the push path: neither `commitg1.sh` nor `pushg1.sh`, `raiseg1.py` or `raise_rest_g5.sh` invokes any of them (drafter `grep -n -i`; must-hit `gatelinesg1.py` found at `pushg1.sh:233`).
  - **`rekey_check`** (932 lines, 14 live hex constants per K 1st's sweep) verifies other re-keys. Its value is a single verdict instead of per-tool asserted counts. **Recommend HOLD:** ~3-5 points of ctx for evidence the per-tool `N checked` + both-way controls already give.
  - **`namecheck`** (1199 lines, 51 live predecessor-token lines, plus a hard-coded `seat g 5th`/`seatg5` literal at `:446`, G 5th's handover item 2). It is the only instrument that scans branch name, PR title AND commit message for foreign seat tokens and foreign hyphenated keys together. Its re-key is the largest in the kit (~5+ points), with the whole matrix to re-pin.
  - **Recommend HOLD by default, and replace it for THIS round with three asserted one-liners, each with a planted control that fires:**
    1. the branch ends `-k2-1` and carries no other seat segment;
    2. the only hyphenated `KS-\d+` in the branch, subject, body and PR title is `KS-1402`;
    3. the broad closing-word regex.
  - **Re-key `namecheck` only if Wednesday reads your ctx at ≤ 25% in the plan ANSWER.** The arithmetic: K 1st sat at 24% at its plan mail and spent ~2.7 points per tool. The seven path tools plus three re-seats plus ITEM 4-5 land near 55-60% before namecheck; with it, too close to 65%.
  - `bannercheck`, `trap4`, `twolock`: HOLD (not on this round's path).
- **Q-DOCSMERGE (binds ITEM 5's body and the READY).** Does the PR need develop merged in before READY?
  - **Recommend / default: NO.** The established Secuura pattern is that the gate measures the PR's head from its own base, and the merge seat does the keep-both merge-ins:
    - gate77's kit measures a row "from its own base" (`fleet/qa-agent/gatesets/2026-10-09_gate77/RULINGS_wednesday.md:7`, #1436 measured from base `81d2e5f4c415` with a NO-EVIL-MERGE arm);
    - the merge seat performs the docs-only merge-ins with composed docs taken verbatim (`:39`, `:48-51`, Q-MERGEINS77);
    - Wednesday's merge-seat ruling: "the R lane holds the keep-both merge-in tooling" (`:111`);
    - Wednesday's 03:38Z ANSWER to K 1st: "Your PR merges develop IN later if needed; never rebase."
  - A merge-in by you would also need develop's objects, which are ABSENT from the store: Q-OBJ-K, a transfer this round does not carry.
- **Q-LOCK-K2 (binds the first take).** Recommend / default: **`.push-lock-g1`, holder `Secuura/Blockchain-K k2`**: K 1st's Q-LOCK-K ruling, re-seated. It is still a WAIT entry in the R lineage (`lockra1.sh:303`, R 22nd's copy), and 0 locks were present at 04:27:53Z.

## UNKNOWN / UNMEASURED (each with why and its instrument)
- **Your pane id, launcher warnings, sole-session status, ctx**: you are not launched. Instruments: ITEM 0(a); Wednesday's statusline read.
- **E 12th's state** (a second `secuura-api.yaml` writer): 0 `-e12-` refs (control `-e11-` 1), no pane; the older `-b52-`/`-b53-`/`-e10-` KS-1364/KS-591 heads' PR state is unmeasured. Instrument: ITEM 0(e) (the API) + Wednesday.
- **Open PRs beyond the nine named heads**: the drafter holds no Secuura GitHub identity. Instrument: ITEM 0(e), the API paginated.
- **The gate number `<NN>`**: not yet assigned. Instrument: Wednesday's push ANSWER.
- **The in-hook preflight at your push**: it has not run. Instrument: the push's own log.
- **`mergeable_state` after the raise**: no PR yet. Instrument: the API read in ITEM 5.
- **Q-LEGACY count, live sweep, S↔K pair, the four platform suites**: no stack, by HOLD. They go in NOT COVERED.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE (restate, do not ask)
- Q-MECH = the DB lookup, sub-choice the DIRECT `users` SELECT; Kam told as an FYI with his veto (none received) | SEND AMENDMENT 03:07:58Z
- Q-SCOPE one path for all callers · Q-NULLT keep `tenant_id IS NULL` tolerance (C7) · Q-LEGACY declare in NOT COVERED · Q-KEY catch → 502 `BAD_GATEWAY` (C9) · Q-NUM `44.` · Q-SUBJ-K as recommended | SEND AMENDMENT 03:07:58Z
- Q-COMMENTS = YES: the comment sites `:1567-1574` and `:1786-1787` were corrected in place (comments only), and are part of `documents.ts` | ANSWER_plan 03:27Z
- Q-HOIST = (i), a pure move of `tenantId` and `db` above resolution; answer order pinned by C10 | ANSWER_plan 03:27Z
- Q-739: 20 dispositions; **17 RETIRED (21 executed) + 3 RE-POINTED (4 executed)**, superseding "15 (20)" by name | ANSWER_plan 03:27Z + ANSWER_split 04:08Z
- The two-condition Q-KEY requirement and "the ruled mechanism is STRICTER than auth's path" go in the PR body; RLS stated honestly; KS 1406 NOT COVERED and already filed, file nothing | ANSWER_plan 03:27Z
- `pushg1.sh:233` two-way fix (existence assert + unpiped rc) APPROVED | ANSWER_plan 03:27Z
- `searchIssues` is not an absence instrument | ANSWER_plan 03:27Z
- KS-1402 `updatedAt` drift: mention in the READY, do not investigate | ANSWER_plan 03:27Z
- RAISE_BASE ACCEPTED BY NAME `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6`; if develop moves, build on it, merge IN later, never rebase | ANSWER_raisebase 03:38Z
- Build first, re-key ON THE PATH just in time; the 5 verifiers HELD and declared, the cost stated | ANSWER_ctx 03:40Z
- Never end a turn on a "next up" line with nothing running | ANSWER_resume 03:46Z
- ks697 takes ONE key-registration line; both runs (16/17 → 17/17) go in the READY; the cell text byte-identical | ANSWER_ks697 04:01Z
- Q-HELPER inline (~32 lines) accepted; the DB-failure → 500 failure-mode change accepted as DELIBERATE, on its own line in the body; `PII_LOOKUP_HMAC_KEY` deploy requirement in the body | ANSWER_ks697 04:01Z
- "Three per-file runs were green; the whole suite found it" (ks1061) | ANSWER_split 04:08Z
- The K 1st → K 2nd split at the clean boundary; K 2nd does the re-keys, ITEM 4, ITEM 5 | ANSWER_wrap 04:16:36Z
- Carried from K 1st's brief: `comments(first:50)` sorted client-side; the `$TMUX_PANE` pin; `ast.literal_eval` + truncated-source `tag()`; the exec bit checked on disk after any apply (F lane rulings, 2026-10-08) · declining `POST /api/seen` is right; F-02: verify the push identity with an SSH auth probe and never set `SECUURA_ALLOW_ONDISK_KEY` yourself (R 20th) · doc blocks are numbered by ticket and nobody renumbers | K 1st SEND brief `:387-391`

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **Card `secuura-ks1402-s-key-cannot-carry-users-read-1006` = a**, `ruled_ts=2026-10-06T09:58:21.119827+11:00`: *"a: Originate resolves the holder with its own service credential (Stuart's option 2)."* Detail: *"No scope change and no re-mint of any live key. Keeps 'on-behalf-of resolution is K-side'. A K build round, then the QA gate, then a merge. The cross-tenant guard must be proved by the gate."* Option b (add `users:read` + re-mint) was NOT taken.
- Earlier: card `secuura-ks1402-lookup-refuses-connector-tokens` = a (2026-10-02T09:59), executed as #1374, which moved S from 401 to 403.
- **The ruling comment promised to Stuart is NOT on the ticket. It is Wednesday's to post, not this seat's.**
- Standing: Kam's week instruction to Sun 11 Oct; drive hygiene 2026-10-05; the 2026-09-11 TESTED merge grant (NOT exercised: this brief ends at READY).
- **The whole ruled-but-undelivered list for `secuura-`** (`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-`, rc 0, 68 lines, generated by the drafter at 04:28Z; **byte-identical to the list in K 1st's SEND brief** by `diff`). Pasted by hand because **the send gate does not map lane `-K`**. Only the two KS-1402 cards above are yours; the rest are context, not work:
```
[ruled] secuura-agent-github-identity  Secuura/Blockchain — Your Approve was refused: GitHub won't let kksecura approve kksecura's PRs — give the agent its own GitHub identity, or Stuart/Peter approve  => identity @ 2026-08-26T17:12
[ruled] secuura-dependabot-triage  Secuura/Blockchain — Dependabot: close 5 dead workflow-only PRs + rescope the bot?  => close-and-rescope @ 2026-09-01T09:18
[ruled] secuura-ks229-disclosure-mailbox  Secuura/Blockchain — SECURITY.md disclosure mailbox (+ Steve's GitHub handle for CODEOWNERS)  => later @ 2026-09-02T20:15
[ruled] secuura-ps-759-760-merge-owner  Secuura/Platform_S — PS #759 (PS-761) and PS #760 (PS-754) are Peter-approved and unmerged — who merges?  => kam-merges @ 2026-09-05T09:16
[ruled] secuura-demo-kam-admin-default-password  Secuura/Blockchain — Your address kam@secuura.ai is a SYSTEM_ADMIN on the public demo, seeded with the published default password secuura123 (DEMO_SECUURA_PASSWORD unset, ALLOW_DEFAULT_SEED_PASSWORDS=true, MFA off) — set a real password tonight, replace the identity, or both?  => b @ 2026-09-07T06:44
[ruled] secuura-f5-login-limiter-bypass  Secuura/Blockchain — A double slash defeats the LOGIN rate limiter — /api/auth//login skips it and is normalised back to canonical in transit. Measured in a faithful reproduction, NOT yet in the booted gateway. Tell Peter and Stuart now, or when the full-boot confirmation lands?  => wait @ 2026-09-07T06:44
[ruled] secuura-f5-demo-exposure-probe  Secuura/Blockchain — Do we probe the DEMO to find out if F5 is live there?  => probe @ 2026-09-07T06:44
[ruled] secuura-f5-demo-interim-mitigation  Secuura/Blockchain — F5 is CONFIRMED LIVE on the demo — protect it in the interim, or let the fix land?  => letitland @ 2026-09-07T07:08
[ruled] secuura-demo-admin-transcripts  Secuura/Blockchain — Your name is still in 10 dated session transcripts — redact, or leave the record intact?  => redact @ 2026-09-07T07:38
[ruled] secuura-demo-admin-mfa  Secuura/Blockchain — MFA is off on the demo platform admin — turn it on with this change, or leave it?  => later @ 2026-09-07T07:38
[ruled] secuura-891-workflow-scope-merge  Secuura/Blockchain — #891 cannot be merged by the agent — GitHub refuses the token on a .github/workflows file. Your 09-05 'kam-merges' ruling already answers this shape  => kam-merges @ 2026-09-07T18:56
[ruled] secuura-force-push-own-branch-standing  Secuura/Blockchain — RE-CREATED after Wednesday destroyed the record: force-push on an agent's OWN unshared branch — you ruled narrow-allow at 18:03:38  => narrow-allow @ 2026-09-07T18:56
[ruled] secuura-org-trust-boundary-within-tenant  Secuura/Blockchain — RE-CREATED (Wednesday destroyed the record, not the question): inside one tenant, is an ORGANISATION a trust boundary? It is what your #889 hold is waiting on  => bind @ 2026-09-07T19:01
[ruled] secuura-archive-fifteen-platform-s-tickets  Secuura/Blockchain — Archive pass reaches 15 tickets on Stuart's Platform S board — ours to archive, or his?  => archive @ 2026-09-08T10:35
[ruled] secuura-advisory-gate-moving-set  Secuura/Blockchain — A THIRD advisory landed 8 minutes after you ruled, and the agent proved the set is MOVING — this is the pattern you already chose, brought back with its design  => both @ 2026-09-09T08:12
[ruled] secuura-advisories-high-and-prod-reaching  Secuura/Blockchain — Two advisories your own grant refuses to let me clear — one HIGH, one in PRODUCTION auth code — and the gate has turned out to be non-deterministic  => measure-first @ 2026-09-09T10:30
[ruled] secuura-four-advisories-ruled-after-measurement  Secuura/Blockchain — All four measured as you asked — none reachable in our code today, and my recommendation is to BUMP rather than accept them  => bump @ 2026-09-09T10:30
[ruled] secuura-required-approvals-zero-after-the-untick  Secuura/Blockchain — Unticking the status checks removed the LAST technical brake — 44 PRs are one click from develop with zero approvals required. Raise it to 1, or leave it?  => raise-to-1 @ 2026-09-10T10:38
[ruled] secuura-ks1011-stack-marker-unknown-on-restore  Secuura/Blockchain — KS-1011 (P3): the KS-666 stack marker reads unknown for owner/branch/commit/started_at whenever the stack comes up any way but start-secuura.sh — which is every reboot (Docker Desktop restores containers) — a decision on the repair path  => b @ 2026-09-16T09:54
[ruled] secuura-ks1081-two-env-templates-which-is-canonical  Secuura/Blockchain — KS-1081 (P2): Blockchain/Dev carries TWO tracked env templates that disagree by ~39 variables — bootstrap-env.sh reads .env.example, CLAUDE.md documents env.example — which one is canonical?  => a @ 2026-09-16T09:54
[ruled] secuura-ks1168-ilike-search-on-encrypted-pii  Secuura/Blockchain — KS-1168 (P3): userRepo.ts searches encrypted PII columns with ILIKE — a name/email search can never match (ciphertext vs pattern) and looks like no such user; which search design replaces it?  => a @ 2026-09-16T09:54
[ruled] secuura-ks1194-1032-round2-merge-tap  Secuura/Blockchain — Merge #1032 (KS-1194): a failed verification save is never acknowledged — round 2 passed its gate  => merge @ 2026-09-18T09:31
[ruled] secuura-ks1245-smoke-test-degraded-semantics  Secuura/Blockchain — KS-1245: smoke-test.sh fails a 'degraded' /health/deep — pass-with-warning, or keep failing?  => a @ 2026-09-22T18:11
[ruled] secuura-ks1019-blockchain-block-untyped  Secuura/Blockchain — KS-1019: the document's blockchain block is published as z.unknown() — leave it (record why) or type it?  => a @ 2026-09-22T18:11
[ruled] secuura-ks1084-gateway-originate-no-tenant-header-p0  Secuura/Blockchain — KS-1084 (P0): gateway→originate calls send no x-tenant-id — spend a Claude measurement seat on it now, or hold?  => c @ 2026-09-22T18:11
[ruled] secuura-ks1304-withtenant-tenant-pool-and-admin-writes  Secuura/Blockchain — KS-1304: should admin config writes follow a tenant onto its own database?  => c @ 2026-09-26T07:19
[ruled] secuura-pr1245-ks1313-at-the-cap-disposition  Secuura/Blockchain — PR #1245 (KS-1313, the vitest summary reader) failed its second and last allowed gate: authorise a round 3, merge it as is, or close it?  => a @ 2026-09-26T07:18
[ruled] secuura-allowance-89-before-the-0930-freeze  Secuura/Blockchain — Allowance at 89%: the last KS-1341 leak fix and KS-1344 need a new account to land before pushes freeze on 30 Sep  => a @ 2026-09-26T21:04
[ruled] secuura-ks1346-logging-thrown-objects-leaks-secrets  Secuura/Blockchain — KS-1346: logging the full thrown object puts passwords and personal data in the logs; how much should an error log say?  => a @ 2026-09-27T16:32
[ruled] secuura-ks1348-log-files-persist-secrets  Secuura/Blockchain — KS-1348: making originate's log files JSON also writes passwords, tokens and emails into them — redact first, or keep them out?  => a @ 2026-09-27T19:07
[ruled] secuura-ks888-failed-key-save-design  Secuura/Blockchain — KS-888: making a failed API-key save return an error would crash the security service on two other routes. Fix mint only for now?  => b @ 2026-09-28T06:58
[ruled] secuura-ks1348-r2-files-still-leak-allowlist  Secuura/Blockchain — KS-1348: the redaction fix still lets other secrets into the production log files. Allow a third attempt with an allow-list?  => a @ 2026-09-28T06:58
[ruled] secuura-ks888-revoke-validate-on-failed-save  Secuura/Blockchain — KS-888 all three routes: what should a failed revoke and a failed key check answer?  => a @ 2026-09-28T20:24
[ruled] secuura-ks1124-f4-failed-anchor-shows-pending  Secuura/Blockchain — KS-1124 F4: outside production, a certification whose blockchain anchoring failed shows 'pending' forever. How should it say it failed?  => b @ 2026-09-28T20:24
[ruled] secuura-ks1352-revoked-credentials-still-verify  Secuura/Blockchain — KS-1352: a revoked credential still verifies as valid, and says its status check passed. How should verify decide?  => a @ 2026-09-28T20:24
[ruled] secuura-ks888-validate-usage-write-failure  Secuura/Blockchain — KS-888 validate: should a failed usage-counter write lock out a valid API key? The 18:00 default would, and the card never said so  => a @ 2026-09-28T20:24
[ruled] secuura-ks1380-peter-reverting-1358  Secuura/Blockchain — KS-1380: Peter has opened a revert (#1360) of the build fix he merged himself (#1358). Do we leave the direction to him?  => b @ 2026-10-01T08:43
[ruled] secuura-ks1398-typescript-7-move  Secuura/Blockchain — KS-1398: whether and when platform-k moves to TypeScript 7.0.2 (Peter asks you)  => b @ 2026-10-01T07:05
[ruled] secuura-allowance-85-narrow-queue-1001  Secuura/Blockchain — Weekly allowance at 85%: run a narrow queue now, or switch accounts?  => a @ 2026-10-01T12:25
[ruled] secuura-fuse-1009-measured-1001  Secuura/Blockchain — Audit fuse Fri 9 Oct: fix one row now, re-date the two react-router rows by your email  => a @ 2026-10-02T10:02
[ruled] secuura-ks1402-lookup-refuses-connector-tokens  Secuura/Blockchain — KS-1402: your 2 Sep lookup ruling cannot take effect. Tap a to let K's user lookup accept S's connector token  => a @ 2026-10-02T09:59
[ruled] secuura-freeze5-high-no-fix-1004  Secuura/Blockchain — Push freeze 5: two HIGH advisories with no fix anywhere (braces, node-forge) block every push — accept, remove, or wait?  => b @ 2026-10-04T21:06
[ruled] secuura-tsa-accepts-unsigned-tokens-1004  Secuura/Blockchain — Timestamping accepts UNSIGNED timestamp tokens and labels them qualified — file and fix?  => a @ 2026-10-04T21:06
[ruled] secuura-ks1404-tsa-trust-and-library-1004  Secuura/Blockchain — KS-1404 timestamping fix: which timestamp authority do we trust, and may the fix add the pkijs library?  => a @ 2026-10-04T22:07
[ruled] secuura-mobile-dormant-fuse-lapses-1019b  Secuura/Blockchain — Your 17 Sep 'dormant but kept' fuse on the mobile app tree expires Mon 19 Oct — re-date it, or every Secuura push freezes that day  => a @ 2026-10-05T09:59
[ruled] secuura-ks723-whose-to-raise-1005  Secuura/Blockchain — KS-723: the Spark fixed one of Stuart's two endpoints — is this ours to raise, or Peter's ticket?  => a @ 2026-10-05T12:14
[ruled] secuura-tenant-isolation-migration-ks1401-1005  Secuura/Blockchain — KS-1401 / KS-1376: a migration on live data is needed to close two tenant-isolation gaps  => a @ 2026-10-05T16:22
[ruled] secuura-connector-allowlist-missing-setting-ks1256-1005  Secuura/Blockchain — KS-1256: on a fresh install with no settings saved, should connector creation be refused until an admin sets the allow-list?  => b @ 2026-10-05T16:22
[ruled] secuura-internal-tooling-view-filter-1005  Secuura/Blockchain — Hide the 160 Internal tooling tickets from the product board view?  => c @ 2026-10-05T18:14
[ruled] secuura-tooling-32-decision-tickets-1005  Secuura/Blockchain — 32 Internal tooling tickets need a decision: may I decide the 24 engineering ones?  => a @ 2026-10-05T19:52
[ruled] secuura-ks1404-anchors-before-049-merge-order-1005  Secuura/Blockchain — Merge order: hold #1383 (migration 049) until KS-1404's anchor wiring lands, so demo can get both in October?  => a @ 2026-10-05T19:52
[ruled] secuura-pushgate-three-legs-1005  Secuura/Blockchain — Push gate: add any of three proposed checks to what runs before every push?  => a @ 2026-10-05T20:07
[ruled] secuura-ks1188-burnt-backup-code-wording-1005  Secuura/Blockchain — KS-1188: what a user is told when a used backup code's sign-in fails mid-way  => a @ 2026-10-05T20:07
[ruled] secuura-capped-prs-1245-1278-disposal-1005  Secuura/Blockchain — Close two stalled pull requests (#1245, #1278) once their replacements merge?  => a @ 2026-10-05T20:07
[ruled] secuura-ks1402-s-key-cannot-carry-users-read-1006  Secuura/Blockchain — KS-1402: your 2 Sep ruling (S's key carries users:read) cannot happen. Stuart measured it. Pick how K resolves the holder instead  => a @ 2026-10-06T09:58
[ruled] secuura-ks1256-redis-outage-stops-connector-creates-1006  Secuura/Blockchain — KS-1256: closing the fail-open means a Redis outage STOPS Platform-S document creation. Accept, or narrow it?  => a @ 2026-10-06T10:22
[ruled] secuura-uuid-revokes-never-wrote-status-history-1006  Secuura/Blockchain — Did any document get 'revoked' by UUID in the past and silently stay valid? Measure kintsugi and demo read-only?  => c @ 2026-10-06T12:04
[ruled] secuura-five-new-advisories-freeze-every-push-1006  Secuura/Blockchain — Five advisories published overnight freeze every Secuura push (one CRITICAL in 15 services)  => a @ 2026-10-06T13:15
[ruled] secuura-headroom-before-90pct-stop-1006  Secuura/Blockchain — Secuura — how to spend the last ~6% of the weekly allowance before the 90% stop?  => a @ 2026-10-06T19:31
[ruled] secuura-standing-build-cache-prune-1007  Secuura/Blockchain — Secuura — may deploy seats clear Docker BUILD CACHE (only) on kintsugi and demo as a standing rule?  => b @ 2026-10-08T09:19
[ruled] secuura-demo-disk-too-small-to-rebuild-1007  Secuura / Blockchain — Demo box cannot rebuild its own stack: grow its disk, or keep demo where it is  => a @ 2026-10-08T09:19
[ruled] secuura-usage-89pct-raise-backlog-1008  Secuura/Blockchain — Usage is at 89%: the 90% stop will block the raise backlog until Sun 11 Oct unless you lift it  => a @ 2026-10-08T09:19
[ruled] secuura-ks1450-leg14-who-fixes-1008  Secuura/Blockchain — KS-1450 blocks every Blockchain/Dev push: wait for Peter, nudge him, or let us fix his guard  => a @ 2026-10-08T10:46
[ruled] secuura-raise-backlog-at-99pct-1008  Secuura/Blockchain — The raise backlog is unblocked, but weekly usage is at 99%  => a @ 2026-10-08T16:08
[ruled] secuura-ks1195-s-key-ceiling-1009  Secuura/Blockchain — KS-1195: Stuart asks for a higher hourly limit on S's connector keys. What ceiling?  => a @ 2026-10-09T10:06
[ruled] secuura-ks1384-anchor-per-event-1009  Secuura/Blockchain — KS-1384: one blockchain anchor per document, or one per lifecycle event?  => a @ 2026-10-09T10:06
[ruled] secuura-ks695-connector-may-revoke-own-key-1009  Secuura/Blockchain — KS-695 ask 3: to erase its organisation, S's connector must revoke its own key. Allow that one narrow rule?  => a @ 2026-10-09T12:24
67 decision(s) [ruled, undelivered, prefix=secuura-]
```

PROVENANCE:
- develop `349b35c9163ac59209366adb7a4a89d8779bd6d6`; main `54b2a5c26d75`; #1383 `32e8459bc0f5`, #1427 `ec94946e3be9`, #1429 `1271d9597c43`, #1430 `d9928f4a8a4d`, #1431 `d715e5dfbbf2`, #1432 `c4e6f50654fa`, #1433 `934e20a599b1`, #1434 `d7ba337a8ef6`, #1435 `6f4adfe8835e`, #1436 `90d98754db7b`; #1437-#1440 absent, #99999 absent; only `feature/ks-1402*` = `-b55-1` `aa16f3256dbf`; `-k1-`/`-k2-` 0, `-ra13-` 2, `-k2-<n>$` 0 vs `-g5-<n>$` 1; 2,159 lines | `env -u GIT_SSH_COMMAND git -C '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files' ls-remote origin` rc 0, output to a file | read 2026-10-09 (04:27:28Z-04:27:34Z)
- `-e12-` refs 0 (control `-e11-` 1); KS-1364 heads `-b52-1` `bf277eead268`, `-b53-2` `2a3dcd912a33`; KS-591 `-e10-2` `c18de5c9659b` | `grep -c -E` / `grep -E` on the same ls-remote file | read 2026-10-09 (04:34Z)
- #1427 merged as `349b35c9163a` at 04:20:00Z, pinned to M' `ec94946e3be9` | Seat R 22nd's WRAP `fleet/briefs_staged/2026-10-09_seatR22_WRAP.txt:4-18` + `HANDOVER-seatR22-2026-10-09.md:3-6` (Wednesday verified at source, per the commissioning) | read 2026-10-09
- `349b35c9163a` objects ABSENT from the shared store; `81d2e5f4c415` PRESENT; `deadbeef…` absent | `git -C <checkout> cat-file -e <sha>^{commit}`: rc 128 / 0 / 128 in one call | read 2026-10-09 (04:27:42Z)
- worktree HEAD `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6`, detached; porcelain 7 ` M` + 1 `??`, the eight paths as listed | `git -C <wt> rev-parse HEAD`; `branch --show-current` (empty); `status --porcelain` to a file; `grep -c` per class | read 2026-10-09 (04:27:42Z)
- patch sha256 `ab8e9e441864e05c35fe1c99adf8feaf0f65a358d8c0070fe2a5c316743bba73`, 88593 B, 8 `diff --git` | `shasum -a 256`, `wc -c`, `grep -c` on the saved file | read 2026-10-09 (04:27:42Z)
- handover 154 lines, sha256 `0ffbae86387b455f7c97042be7ef740e58d04441e590784ae55b212dd3544a1b` | `wc -l`, `shasum -a 256`; Read whole | read 2026-10-09 (04:27Z)
- open-head file sets: yaml in #1429 only (1), each head 2 doc paths, 0 heads touch the K files; #1427 6 files | `git -C <checkout> diff --name-only $(merge-base 81d2e5f4c415 H) H` per head, all heads PRESENT in the store | read 2026-10-09 (04:28Z)
- floor `%0 wednesday`, `%10 QA/Secuura-gate77`, `%1 fleet-monitor`; no `Secuura/Blockchain-R` or `-K` pane | `tmux list-panes -a -F '#{pane_id} #{@cockpit_name} …'` | read 2026-10-09 (04:27:53Z)
- locks 0 in `worktrees/`, control 1 in a private `mktemp -d`; `s-k*` = `s-k1-ks1402` only | `find -maxdepth 1 -name '.push-lock*'` / `-name 's-k*'` | read 2026-10-09 (04:27:53Z)
- gate77 develop `349b35c9…`, merge seat `Seat R 23rd`, order `1432,1433,1429,1434,1436,1431,1430` | `fleet/qa-agent/gatesets/2026-10-09_gate77/head_at_launch.txt` | read 2026-10-09
- gate measures a row from its own base; merge seat does docs-only keep-both merge-ins; R lane holds the tooling | `gatesets/2026-10-09_gate77/RULINGS_wednesday.md:7`, `:39`, `:48-51`, `:111` (`grep -n -i`) | read 2026-10-09
- gate78 spent on #1435 | `ls fleet/qa-agent/gatesets/` + `0_Brain/daily/2026-10-09.md:47` | read 2026-10-09
- tool hashes and line counts (12 re-hashed, all equal to `wrap/TOOL_HASHES_k1_for_K2.txt`) | `shasum -a 256 | cut -c1-16`, `wc -l` on `2026-10-09_seatK-1st/tools/*` | read 2026-10-09 (04:2xZ)
- `_MINE_BRANCH` `namecheckg1.py:428`; `seat g 5th` literal `:446`; `-g4-` re-slug note `:498-499`; B 45th adoption `:180-183`; E 3rd `ADOPTED_WORKTREE` note | `grep -n -i`, `sed -n` on K 1st's copy | read 2026-10-09
- `commitg1.sh:68` (`diff --name-only`) and `:70-72` ("exactly 3 changed paths"); `pushg1.sh:233` (`|| true`); 0 calls to the held verifiers in commit/push/raise tools, must-hit `gatelinesg1.py` at `pushg1.sh:233` | `sed -n`, `grep -n -i -E` | read 2026-10-09
- `.push-lock-g1` WAIT entry | `2026-10-09_seatR-22nd/tools/lockra1.sh:303` (`grep -n`) | read 2026-10-09
- R lineage `tag()` tests MINE first | `HANDOVER-seatR22-2026-10-09.md` item 2 (`sed -n 1,30p`) | read 2026-10-09
- project `CLAUDE.md` 306 lines, sha256/16 `812663207c976c69` | `wc -l`, `shasum -a 256` | read 2026-10-09
- usage 23% | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check` rc 0 | read 2026-10-09 (04:28Z)
- week instruction LIVE to 2026-10-11, clause verbatim | `0_Brain/tasks/WEEK-INSTRUCTION.md:5`, `:10` (`grep -n -i`) | read 2026-10-09
- model line | top block of `0_Brain/learnings/2026-10-09_spark-ornith-sonnet-only-until-monday.md` (`head -12`) | read 2026-10-09
- undelivered list, 68 lines, identical to K 1st's SEND brief | `decision_queue.sh list ruled --undelivered secuura-` rc 0 + `diff` against the SEND brief's block (empty) | read 2026-10-09 (04:28Z)
- every K 1st figure quoted (cells, tamper rows, suite, tsc, yaml hunks, docs, ks739/ks697 counts, failure-mode change) | K 1st's mails `…_seatK1_plan.txt`, `…_status_redfirst.txt`, `…_Q_split.txt`, `…_Q_item3.txt`, `…_WRAP.txt` and the handover, read WHOLE; K 1st's measurements, NOT re-run by the drafter | read 2026-10-09
- every Wednesday ruling quoted | `…_seatK1_ANSWER_{plan,raisebase,ctx,resume,ks697,split,wrap}.md`, read WHOLE | read 2026-10-09

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-09 15:34
