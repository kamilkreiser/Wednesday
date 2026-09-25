# QA Agent Invocation Brief — Datasec/NexusAI, ONE batched TIER 1 gate: RD-579 + RD-639 (two targets, two verdicts, one report)

**Drafted for Tuesday 2026-09-25 22:50–23:30 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.**
Commissioned on two READY FOR QA mails (copies on disk, read whole):
- **A — RD-579** (NexusAI-M, S84M) @ `cac9cf641c86ff89a48aa42d7447cdcfbbeaa6c1` —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-rd579-READY-mail.txt` (12:50:25Z).
- **B — RD-639** (NexusAI-N, S84N) @ `fe53540fbaf628fa3ca5eb790d023ecf5ae71f0c` —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-rd639-READY-mail.txt` (12:53:38Z).
**Batched under the 2026-09-18 batch-gates rule** (Tuesday's addition, 22:5x AEST): the two branches are file-disjoint except
`scripts/verify-expected-counts.json` (MEASURED, §1). **Both heads and main are pinned here and re-read by `git ls-remote` in the
launcher immediately before launch.**

SELF-CHECK: re-read end-to-end for contradictions | Tuesday 2026-09-25 23:05: read whole; one fix (the merge authority is Kam's 22:0x instruction, not the spent C-127); RD-639's builder was told at 23:0x to FREEZE its branch at fe53540
Self-check note: Tuesday stamped at 2026-09-25 23:05; report path renamed to 2026-09-25-gate-rd579-rd639; the drafter's WRONG list is carried in the brief body.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an
independent tester. You did not build these changes and you owe no builder anything. **Every line below that reports what a
builder says is a CLAIM, never evidence.** Explore the AI-config clear and save routes (A) and the erasure purge of a symlinked
live store (B), with real requests on your own loopback servers and real symlinks on your own temp disks, looking for any state in
which the product **claims something was removed, refused or cleared that is still there**, any caller who can do what they
should not, and any secret that leaves the store.

- **RD-579 is TIER 1** (auth/secret surface: an API key the product says it removed; a route an anonymous caller can reach in the
  open window). Verdict: **GO / GO WITH FINDINGS / NO GO at `cac9cf6`**, plus its merged-tree result.
- **RD-639 is TIER 1** (erasure honesty: a privacy certificate that says `purged` while the bytes survive). Verdict:
  **GO / GO WITH FINDINGS / NO GO at `fe53540`**, plus its merged-tree result.
- **One verdict PER ticket, one report, one mail.** A finding on one ticket never becomes the other's verdict.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- None new for these two tickets. The rulings that bind are in `1_Project_Definition/CLARIFICATIONS.md` (268,324 bytes, mtime
  2026-09-25 21:57), cited below with the line numbers read at drafting. **Merging is Tuesday's GO under Kam's 2026-09-25 ~22:0x instruction "work your way through the tickets and merge once tested" (C-127 is SPENT); this gate merges
  nothing into anything the fleet can see.**

**THE COORDINATOR'S INSTRUCTIONS FOR THIS GATE (Tuesday, 2026-09-25, carried in substance):**
1. Queue on the shared jest lock (`session-tools/nexusai-lock.sh`) with a **`qa-rd579-`** tag (every hold, both tickets:
   e.g. `qa-rd579-A-red`, `qa-rd579-B-arms`, `qa-rd579-merged-verify`). **QUEUE, NEVER TAKE OVER.** Four NexusAI seats (M, N, O,
   P) are working parallel lanes on that one lock right now.
2. The verdict is about **each branch head AND the merged tree**: build your OWN tree of `7c47ec4` + `cac9cf6` + `fe53540` in your
   own project directory (a scratch clone of your own, `git clone --shared`, is fine; §6), regenerate counts there ONCE, run the
   full verify, and report both.
3. RD-579: attack both behaviour claims, red-proof at `0677388` and `7c47ec4` and green at the head, a control that can fail,
   authorization in every state, audit rows, no secret in any response or log, regression on every other ai-config caller, the
   prior-work check, the full verify, and a NOT TESTED section.
4. RD-639: attack with REAL symlinks — store → target outside and inside the data dir, a dangling link, a link to a directory;
   whether the target's data is actually gone or refused; whether the ledger is truthful (**"purged" only when the bytes are gone —
   RD-575's lesson: assert the effect, not the bookkeeping**); and **no deletion outside the data dir**.
5. Prove the two branches file-disjoint except the counts file. Build and verify each head separately, then the merged tree.

**The clarifications that bind this gate** (line numbers read 2026-09-25 ~23:05 AEST):
- **C-28** (:153) never write, pull, check out or stash NexusAI's `2_Project_Files`. **C-40** (:225) a check must be able to fail
  on the thing it claims. **C-49** (:299) the prior-work check. **C-57** (:410) a conflict confined to the counts file is
  resolved by REGENERATION with the id-superset control; any other conflicting file STOPS. **C-63/C-64** (:581/:599) the FIFO lock
  and its usage rule. **C-68** (:657) a verdict holds only at the head it ran on, and merged counts are regenerated once on the
  tree that exists after the merge. **C-75** (:718), **C-92** (:851), **C-93** (:867) RD-549's rule: stored AOAI config is kept
  but used only when confirmed; open-mode confirmation while sign-in is not configured. **C-76** (:729) an explanation is a claim
  — it gets a red proof or is marked UNVERIFIED (RD-579's 500 branch is declared this way). **C-89** (:827) after a merge,
  `git diff --quiet HEAD` and HEAD's counts. **C-97** (:900), **C-98** (:906) cells assert the property after the fix.
  **C-110** (:1101) the floor rule. **C-112** (:1141) a declared limit is where the evidence stops. **C-122** (:1278) source text
  does not cover behaviour. **C-125** (:1320) the foreign-server counter. **C-127** (:1350) merges are Tuesday's GO.
  **C-133** (:1426) base-aware id accounting (cite only if your id-superset control misses; §6 predicts it will not).
  **C-139** (:1472) — its "Not decided here" line (:1476) left a SYMLINKED `feedback-attachments` to "whatever gate 4 or gate 5
  finds"; RD-639 is that finding's fix. **C-141** (:1479) your `qa-*` tickets are gate-class. **C-142** (:1489) what "green"
  means at a merge. **C-162** (:1644) RD-665 was ported onto main as `c5d053b` → `7c47ec4` (the main this gate merges onto).

## PRIOR ROUND
**Neither ticket has a prior QA gate round.** Each is the fix of a finding a previous gate MEASURED; read the finding whole
before you drive anything, and cite it:
- **RD-579 ← RD-464 r3 tier-1 gate, F-1** —
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-20-rd464-r3-60c76d7-tier1/report.md`
  (F-1 at :339, *"`/api/setup/ai-config/clear` answers `"cleared"` while a stored API key is still there"*; its ticket note at
  :617). Its evidence directory is beside it; you may reuse instruments BY COPY.
- **RD-639 ← gate 4, F-A1 (Major, pre-existing class)** —
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/report.md`
  (summary :14, the measurement :152, the finding :290): a top-level store that is itself a symlink is unlinked and recorded
  `purged`, `failed: []`, while its target keeps the data — measured for `feedback-attachments` → outside directory at `6a32426`
  and `feedback.json` → file on main `982a84f`.

## 1. Targets — verified at drafting from the object store (22:52–23:10 AEST)
**origin by `git ls-remote` at 22:52:26 and again at 22:54:43 AEST (identical):**
`main` **`7c47ec467f585e9db5daf3a82cdb96deae0b1e7a`** ·
`rd-579-ai-config-clear-s84m` **`cac9cf641c86ff89a48aa42d7447cdcfbbeaa6c1`** ·
`rd-639-erasure-symlink-s84n` **`fe53540fbaf628fa3ca5eb790d023ecf5ae71f0c`**.
**Re-read them at your start, mid and end. A moved head is a finding and a reason to stop, never a typo to fix.** RD-639's builder
has said it is STACKING RD-627a and RD-324 on `fe53540` — **a new commit on `rd-639-erasure-symlink-s84n` is plausible while you
work. If that branch moves, your RD-639 verdict still names `fe53540`, and you say so.**

### TARGET A — RD-579 (TIER 1)
- **Branch `rd-579-ai-config-clear-s84m` @ `cac9cf6`, ONE commit, single parent `0677388ab031ffaf569a52f6c0301af48f44aece`**
  (MEASURED: `git log --format='%H %P' 0677388..cac9cf6`). `merge-base(cac9cf6, 7c47ec4) = 0677388`. **Main `7c47ec4` is NOT
  its base** — main is two commits past it (`c5d053b542935c0d1ef8e47f0ba3f18fea9917a0` RD-665 port, `7c47ec4` counts; C-162).
- **Delta over `0677388`: three files, +226/−10** — `__tests__/rd579-ai-config-clear-truthful.test.js` (A, 171),
  `backend/server.js` (+59/−10 in two hunks: the clear route `:16379` and the Azure OpenAI save branch `:16617`),
  `scripts/verify-expected-counts.json`. **Not counts-only at the tip: the product change, the cells and the counts are all in
  the one commit.**
- **Counts: `0677388` 3974/234 → `cac9cf6` 3982/235** (+8 tests, +1 suite). `7c47ec4` is 3978/235.
- **Blob facts that carry the red proof (MEASURED):** `backend/server.js` is blob `fa0d262…` at BOTH `0677388` and `7c47ec4` (main
  did not touch it), and `30aeff7…` at `cac9cf6`. **The builder's green/mutation evidence ran on a working tree 18 minutes before
  the commit** (`rd579-green.log` 22:16, `rd579-mutations.log` 22:17, commit 22:34); its "restored to the same sha
  `6eb4c675b5900f3f`" is a `shasum -a 256` prefix, not a git blob. **Drafter checked:**
  `git show cac9cf6:backend/server.js | shasum -a 256` begins `6eb4c675b5900f3f` — the evidence is tied to the committed file.
  Re-prove it.
- **What changed (READ at source):**
  1. **clear** (`POST /api/setup/ai-config/clear`): after the unchanged authority check (`aiConfigActAuthority` →
     `aiProvenance.confirmAuthority`), when `readStatus().state === 'none'` it now reads the four AOAI fields through
     `jsonStorage.getSetting`; if none holds a value and `llmProvider !== 'azure-openai'` it answers 200 `cleared` (the no-op);
     otherwise it nulls the four fields, the confirmation and last-write markers, and `llmProvider` only if it is `azure-openai`,
     **with no fingerprint**. A non-`none` state keeps RD-549's 409 `AI_CONFIRM_STALE` fingerprint path. Then it reads the four
     fields back: any left → **500** *"some are still stored. Nothing is reported as removed."* and **no audit row**; else audit
     `AI_CONFIG_CLEARED` with `{ endpoint: null, orphanedFields: [names] }` (orphan) or `{ endpoint }` (complete).
  2. **save** (`POST /api/setup/ai-config`, Azure OpenAI branch): after the existing validators, if the body carries a key,
     deployment or version, **no endpoint in the body, and `getSetting('azureOpenAIEndpoint')` is falsy** → **400
     `NOTHING_TO_SAVE`** before any write.
- **The cells (READ, 8):** S0 (control: empty store), **S1** (empty endpoint + key on an empty store → 400 `NOTHING_TO_SAVE`, no
  AOAI field or provider written), S2 (control: full save, then key-only rotation → 200 twice), C0 (control: the orphan is on disk),
  **C1** (clear on the orphan → 200 `cleared` and nothing stored), **C2** (orphan beside provider `ollama` → AOAI fields gone,
  `ollama` stays), C3 (clear on an empty store → 200 no-op), C4 (control: a complete pending config still clears through the
  fingerprint). **Every drive in the file is ANONYMOUS in the OPEN window** (`NO_ENV_SIGN_IN`); no enforced, admin or viewer
  state is driven.
- **Builder's claims (`mail-03-ready-rd579.VVzdQV`, evidence in `session-tools/s84m/`):** red at `0677388`: S1, C1, C2; green
  there: S0, S2, C0, C3, C4. Green at head 8/8. Mutations in one hold: **M1** (restore the early return) → C1, C2; **M2** (drop the
  save guard) → S1; **M3** (guard ignores the stored endpoint) → S2; **M4** (clear `llmProvider` unconditionally on an orphan) →
  C2. Full verify `--update-counts`, SESSION_SECRET unset: **PASS 3982/3982, 235 suites**. Predicted merged (main + A only)
  **3986/236 — "a prediction and not a measurement"** (its words).
- **L-A1..L-A4 — the builder's declared limits, verbatim:** *"The 500 read-back branch has no cell. It needs a store whose
  setSetting silently fails. The property holds by construction and is UNGUARDED (C-76)."* · *"No real browser … First-run UI
  rendering of the 400 is not driven."* · *"Enforced / admin / viewer states are not driven. The route's authority check is
  unchanged code, but I did not re-drive it."* · *"Linux and CI: not run on this branch yet (no PR opened)."*

### TARGET B — RD-639 (TIER 1)
- **Branch `rd-639-erasure-symlink-s84n` @ `fe53540`, ONE commit, single parent `7c47ec4`** (MEASURED). **It IS on main's tip.**
- **Delta over `7c47ec4`: three files, +227/−4** — `__tests__/rd639-erasure-live-store-symlink.test.js` (A, 192),
  `backend/dataErasure.js` (+33/−4, `purgeNow`'s live-store branch only, ~`:880`), `scripts/verify-expected-counts.json`.
- **Counts: `7c47ec4` 3978/235 → `fe53540` 4004/236** (+26 tests, +1 suite).
- **Blob facts (MEASURED):** `backend/dataErasure.js` is blob `7992700…` at `0677388`, `7c47ec4` AND `cac9cf6`, and `4835697…` at
  `fe53540`; `git show fe53540:backend/dataErasure.js | shasum -a 256` begins **`e75914eeb26d`**, the value the READY quotes.
- **What changed (READ at source):** in the live-store loop, after P-3's `statSync` (follows the link; ENOENT → skip) and the
  RD-575 `lstatSync` shape check (a real directory → `_purgeTree`): if `lstat` says symlink, `realpathSync` it (non-ENOENT error →
  failure *"could not resolve symlink"*, link left in place); `unlinkSync` the link; if the resolved target still exists → failure
  *"symlink removed but its target still holds the data: <absolute target>"*, else `purged`. The target is never followed or
  deleted. Same rule as P-6 (recovery copies, `:812-839`) and RD-575's `_purgeTree`. **Note one asymmetry, READ:** P-6 records
  `forAudit(copy.path)` (DATA_DIR-relative); the live branch records the store name, and the error text carries the ABSOLUTE
  target path.
- **The cells (READ, 26):** POPULATION (the list is the product declaration, ≥10, contains `settings.json`, `feedback.json`,
  `feedback-attachments`); **L1 × `CUSTOMER_DATA_FILES`** (each store linked to an outside FILE: target intact, link gone,
  `ok:false`, `purged_incomplete`, failure names the realpath, not in `purged`); **L2** (`feedback-attachments` → outside
  DIRECTORY); **L3** (control: `cost_centers.json` ordinary beside a linked `feedback.json` → purged; the link the ONLY failure);
  **L4** (control: dangling link → `ok:true, failed:[]`). **Count check (drafter, READ + arithmetic):** `CUSTOMER_DATA_FILES` at
  `fe53540` has **22** entries, and 1 + 22 + 3 = 26 = the counts delta. **The READY says L1 is "23" — WRONG AT SOURCE by one, or
  the list moved; count it.** The file `jest.mock`s the logger, so no cell reads a log line.
- **Builder's claims (`session-tools/s84n/rd639/`: `hold.sh`, `hold.out`, `A-base.log`, `B-fixed.log`, `C-verify.log`; one lock
  hold, floor 0 with a control that rose):** A (base `7c47ec4` code, new cells): red every L1, L2, L3; green POPULATION, L4. B
  (fixed): rd639 + erasure-reaches-attachments + erasure-verdict-is-derived-from-failures **40/40**. C: full verify
  `--update-counts`, SESSION_SECRET unset: **PASS 4004/4004, 236 suites**. **There is NO per-cell mutant table** — only the
  revert. The gate supplies one (§5 Q3).
- **L-B1..L-B4 — declared limits, verbatim:** *"A live server, or a store on a real second disk: fs only, temp dirs."* ·
  *"A link whose target is ANOTHER listed store inside DATA_DIR. Read, not run: it reports a failure on this run because the
  target still exists then. That is the safe direction (purged_incomplete); the re-drive completes."* · *"Windows junctions, and a
  realpath failure other than ENOENT (the branch exists; no cell forces EACCES)."* · *"The export side of a symlinked store: C-139
  leaves that to 'whatever gate 4 or gate 5 finds'."*
- **Not in this gate:** RD-627a and RD-324, which the builder is stacking on `fe53540` (nothing pushed for them at drafting). They
  get their own READY and their own gate.

### File-disjointness (MEASURED, READ ONLY)
`comm -12` of the name sets: `0677388..cac9cf6` ∩ `7c47ec4..fe53540` = **`scripts/verify-expected-counts.json` only**;
`0677388..cac9cf6` ∩ `0677388..7c47ec4` = **the counts file only**. `package-lock.json` is blob `9064763…` at all four shas.
**Re-prove both yourself** — and prove more than names: the merged tree's `backend/server.js` must equal `cac9cf6`'s blob and its
`backend/dataErasure.js` must equal `fe53540`'s (§6).

### How to build your trees
- **No worktree is created in the NexusAI repo, and you never work in its `2_Project_Files` checkout (C-28).** In that repo use
  ONLY read verbs: `show`, `log`, `diff`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `grep`, `ls-remote`, `archive`. Never
  `fetch`, `pull`, `push`, `checkout`, `worktree`, `commit`, `stash`, `gc`, `clean` or `merge-tree --write-tree` against it.
- **Head trees:** `git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/qa-trees/g579-639.XXXXXX/>`, git-indexed from the object
  store where a full verify needs a git tree (suites read `.github` / `node-version`).
- **The merged tree:** §6. **Your OWN scratch clone** (`git clone --shared --no-checkout <repo> <your own dir>`), merges and commits
  inside that clone only; then `git archive` the merge result into a fresh tree for the runs, or run in the clone's own worktree —
  never both for the same arm.
- **Each tree is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree for a clean
  arm; `g579-639`-prefixed directories only. Nothing in another gate's `qa-trees/*`, the builders' `worktrees/`, or
  `session-tools/s84m|s84n/` is run in — read only.
- `node_modules`: an APFS clone (`cp -c -R`) of the newest gate tree you trust, **after proving** `package-lock.json` is blob
  `9064763` there too.

## 2. Why TIER 1, and who is waiting
- **RD-579:** `/api/setup/` is on `setupOnlyPaths` (`backend/server.js:2183`), so in the first-run window an **anonymous** caller
  reaches both routes. A clear that answers `cleared` while an API key is still stored is a false claim about a secret; a clear that
  a caller can use to wipe someone else's confirmed config is a denial of the AI feature; a save that writes an unusable key is the
  orphan. **Any path that leaves key material stored while a response says cleared, any caller who can clear or save in a state
  where RD-549 says they may not, or any key value in a response, log or audit row, is a Major.**
- **RD-639:** erasure is the customer's privacy right; `purged` is a certificate. **Any path on which the ledger or `ok` says
  `purged` while the customer's bytes are still readable — this run or the NEXT run (§5 Q5) — is a Major. Any deletion outside
  DATA_DIR is a Blocker.**
- **The queue.** Main `7c47ec4` — **CI Build 36133932540 SUCCESS, 3978/3978 across 235 suites, RELAYED from the RD-579 builder's
  READY (`gh run view`, read-only), NOT re-read by the drafter.** Four NexusAI seats share the jest lock. At 22:5x the RD-639
  builder was queued behind RD-579's verify and the RD-533 probe behind S84N's hold — expect a live queue.

## 2a. LEGITIMATE SHAPES — both changes are CHECKERS (template §2a)
**A — the save guard and the clear decision.** Measure every row, base and head, same window.

| shape — ordinary form, as the product really sees it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| wizard save: endpoint + key + deployment + version on an empty store (what `first-run-setup.js:455-463` sends — it refuses to POST without endpoint AND key) | 200, pending (or confirmed for a strict admin) | guard not reached: endpoint in body | builder (S2 first half) |
| key-only rotation over a STORED endpoint | 200, new key stored (prove the stored `ENC:` blob CHANGED, not just "present") | `getSetting('azureOpenAIEndpoint')` truthy | builder (S2) — **S2 only checks presence; a rotation that silently kept the old key passes it** |
| deployment-only or version-only change over a stored endpoint | 200 | same clause | drafter |
| endpoint-only save (no key) on an empty store | 200, endpoint stored — a NEW keyless shape `readStatus` calls `none`; then clear must remove it | guard not reached (endpoint present); clear's `storedAoaiFields` | drafter |
| `{ aiEnabled: true }` alone (the Settings switch, `settings.js:3585`) | unchanged: RD-395 branch, 200 | returns before the AOAI branch | builder ("A body with only aiEnabled is unaffected") |
| `{ skipped: true }` | unchanged, 200 | returns before the AOAI branch | drafter |
| env-configured deployment (`AZURE_OPENAI_ENDPOINT` in env, nothing stored), key-only body | **now 400**; at the base it stored an orphan key. **Prove the base orphan was INERT** (boot hydration `:4336-4344` needs stored endpoint AND key; the loader `:4574-4590` needs `confirmed`/`admin`) — if it was ever USED, the 400 is a regression | guard reads the STORE, not env | drafter — **the row most likely to hide a regression** |
| env provider `ollama`, body with ONLY deployment/version (no endpoint, no key) | the Ollama branch, not the guard (`carriesAoai` is endpoint-or-key) — pre-existing; state what happens | `carriesAoai` | drafter |
| clear: state `none` because provider ≠ `azure-openai` while a FULL AOAI config (endpoint + key, even a confirmation marker) sits stored | **now cleared with NO fingerprint** (at base: a no-op). State who may do it (open window: anyone) and whether this bypasses RD-549 decision 3's stale-page guard | `st.state === 'none'` → orphan branch | drafter — **measure; do not assume it is an orphan** |
| clear: complete pending/confirmed config, correct fingerprint | 200, all cleared, audit `{endpoint}` | unchanged RD-549 path | builder (C4) |
| clear: complete config, stale or missing fingerprint | 409 `AI_CONFIRM_STALE`, nothing removed | unchanged | drafter |
| clear: an `azureOpenAIApiKey` whose `ENC:` blob **cannot be decrypted** (another machine-id: a restore — gate 5 F-B2's territory) with provider ≠ `azure-openai` | `getSetting` returns **null** on decrypt failure (`jsonStorage.js:1390-1415`), so `storedAoaiFields` does NOT see it → **200 `cleared` with the ENC: blob still on disk** | "raw stored fields" are DECRYPTED reads, not raw | drafter — **a "cleared" over a surviving key is F-1's class; measure it** |

**B — the live-store purge.** Every row with real symlinks on your own temp dirs; hash every target byte before and after.

| shape | expected verdict | clause | predicted-by |
|---|---|---|---|
| ordinary file store | removed, `purged` | unchanged | builder (L3) |
| ordinary directory store (`feedback-attachments/`) | tree removed, `purged` | RD-575 `_purgeTree` | builder (C4 in erasure-reaches-attachments) |
| absent store | skip | P-3 ENOENT | drafter |
| store → FILE outside DATA_DIR | link gone, target byte-identical, failure naming target, `purged_incomplete`, `ok:false` | RD-639 | builder (L1) |
| store → DIRECTORY outside DATA_DIR | same; the tree behind it untouched | lstat → link branch, never `_purgeTree` | builder (L2) |
| store → another LISTED store inside DATA_DIR, link iterated BEFORE its target | failure this run; target purged later in the same loop; re-drive → ? | loop order | builder READ-only ("the re-drive completes") — **run it** |
| same, link iterated AFTER its target | P-3's `statSync` follows a now-dangling link → skip; the link survives on disk | P-3 | drafter |
| store → an INFRASTRUCTURE file inside DATA_DIR (`.machine-id`, `.persistence-sentinel.json`) | link gone, **the infrastructure file intact** (deleting it loses the encryption key) | never followed | drafter — **a deleted target is a Blocker** |
| DANGLING link (target already gone) | skip, `ok:true`; **the link itself is left on disk** — say so | P-3 `statSync` follows → ENOENT | builder (L4) |
| a link chain (store → link → file outside), and a RELATIVE link | the resolved final target is what is named; nothing followed or deleted | `realpathSync` | drafter |
| a link to `/`, to `$HOME`, or to DATA_DIR itself | link gone, NOTHING else deleted, failure | never followed | drafter — **Blocker if anything else goes** |
| a self-loop link (ELOOP) and a link whose target's parent is mode 000 (EACCES) | P-3's `statSync` fails first → *"could not stat"* failure; **say whether RD-639's own non-ENOENT realpath branch is reachable at all** | P-3 precedes it | drafter — builder declared the branch unforced (L-B3) |
| a HARD link (`nlink` 2) to a file outside DATA_DIR | `lstat` says regular file → unlinked → **`purged` while the other name keeps the bytes** | not a symlink: RD-639 does not touch it | drafter — **the class sibling; pre-existing; report with its class, do not grade it as RD-639's regression** |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.**

## 3. THE QUESTIONS BOTH TARGETS ANSWER FIRST
0. **SESSION_SECRET UNSET, EVERY RUN.** Every hold under `env -u SESSION_SECRET`, printing **SET or UNSET** (the name only, never a
   value) as its first line. Positive control once per target: the target's own cell file with a throwaway random 64-hex secret
   exported (never printed, never written) — identical results, or say what differed.
1. **Re-pin everything yourself:** `git ls-remote` at start, mid and end (three timestamped readings, branch name beside each sha);
   chains and exact parents (`git log --format='%H %P'`); deltas (`git diff --name-status`); counts at all four shas; the two
   `shasum -a 256` evidence ties above.
2. **Re-derive every red and every mutant INDEPENDENTLY** — your own script, never the builder's `rd579-mutations.sh` or `hold.sh`.
   **Before each mutant arm, prove the mutant still parses — `node --check` on every mutated file, exit 0, quoted — and assert its
   anchor matched exactly once and the mutation LANDED (grep the marker). A red from a mutant that does not parse, or a green from a
   mutation that never landed, is a VOID arm.** Read WHY each red is red: quote the failing assertion.
3. **Name every behaviour guarded by no cell, and every one guarded only by source text (C-122).**
4. **Full verify of each head AND of the merged tree**, `npm run verify -- --maxWorkers=2` (RD-561), through the lock, on a
   git-indexed tree, SESSION_SECRET UNSET. **Predicted: `cac9cf6` 3982/235 · `fe53540` 4004/236 · merged (7c47ec4 + both)
   4012/237** (arithmetic 3978 + 8 + 26 and 235 + 1 + 1 — a PREDICTION). Every failure by NAME. **"Re-run until green" is not an
   acceptance gate (charter §4d).**

## 4. TARGET A — RD-579 (TIER 1). Answer each with a measurement.
1. **Scope (READ ONLY, quoted):** `git diff --name-status 0677388 cac9cf6` = the three files; the two server hunks and nothing else;
   the blob identities in §1.
2. **RED-PROOF, POSITIVE CONTROL FIRST.** In ONE hold: the head's cell file against the server code of **`0677388`** and of
   **`7c47ec4`** (two trees; same blob, run both anyway) — predicted **S1, C1, C2 red; S0, S2, C0, C3, C4 green**; then at
   **`cac9cf6`** — predicted **8/8**. A head green without the base red in the same window is not reportable.
3. **The mutant table, re-derived:** M1 (early return restored) → C1 + C2; M2 (save guard removed) → S1; M3 (guard ignores the
   stored endpoint) → S2; M4 (`llmProvider` cleared unconditionally on an orphan) → C2. **Then the arms the builder did not run:**
   **M5** — clear returns 200 `cleared` WITHOUT the read-back (delete the `left.length` block): predicted **no cell reddens**,
   which proves L-A1 (the 500 branch is unguarded) by measurement rather than by the builder's word. **M6** — the read-back reads
   nothing (`storedAoaiFields` returns `[]`): same prediction. **M7** — clear skips nulling `azureOpenAIApiKey` on the orphan
   branch: predicted C1 red — **if C1 stays green, the cell does not measure the key.**
4. **THE CONTROL THAT CAN FAIL — drive the 500 branch.** L-A1 says it needs *"a store whose setSetting silently fails"*. Build one:
   a preload in YOUR tree (never in NexusAI) that makes `jsonStorage.setSetting('azureOpenAIApiKey', null)` a no-op, then clear an
   orphan. **Predicted: 500, the key still on disk, NO `AI_CONFIG_CLEARED` audit row, and the error log names the FIELD not the
   value.** Then read the honesty of that 500 at source and on disk: by the time it fires, the OTHER fields, both markers and
   possibly `llmProvider` have already been nulled and a runtime override dropped — **say whether *"Nothing is reported as
   removed"* is a true description of a partial removal with no audit row** (charter §4d, "claims something true that isn't").
5. **BEHAVIOUR CLAIM 1 — clear decides from the stored fields and removes an orphan.** On your own loopback server
   (`__tests__/helpers/rd395-server-harness`'s `bootServer`, copied pattern, your own tree, fresh DATA_DIR): seed each orphan shape
   of §2a (key+deployment+version+provider; endpoint only; key only; provider `azure-openai` alone; provider `ollama` + orphan
   fields; full config under provider ≠ `azure-openai`; an undecryptable ENC: key). For each: `settings.json` read RAW from disk
   before and after (never through the product), the response, the audit row. **The oracle is the disk, not the response.**
6. **BEHAVIOUR CLAIM 2 — the save refuses and writes NOTHING.** For the S1 body and each §2a guard row: **compare the WHOLE
   `settings.json` before and after, key set and bytes** — not only the four AOAI fields S1 checks. `aiEnabled` (S1's body carries
   `aiEnabled: true`), `aiConfigLastWrite`, `aiConfigConfirmation`, `aiConfigSkipped` and `llmProvider` must all be unchanged; the
   runtime LLM source (`/api/setup/ai-model` or the product's own status route) must be unchanged; **a 400 that wrote anything is
   a Major.** Also: no `AI_MODEL_CONFIG` audit row for a refused save.
7. **BEHAVIOUR CLAIM 3 — a key-only rotation over a stored endpoint is unchanged.** Drive it at `0677388` and at `cac9cf6`, same
   window: status, response body, which keys changed on disk, the confirmation marker's value after (anonymous rotation must leave
   the config PENDING, C-75), whether the stored `ENC:` key blob actually CHANGED, and the audit row. **Any difference between the
   two shas is a finding.**
8. **AUTHORIZATION — every caller, every state, both routes (charter §4c).** States: (i) OPEN window (sign-in not configured,
   first run not complete); (ii) open window after first run is complete with no users; (iii) sign-in CONFIGURED (env Entra, or a
   stored config) and ENFORCED, with (a) anonymous, (b) signed-in viewer, (c) signed-in admin; (iv) `signInUnproven` (RD-535: a
   restored store that cannot prove sign-in was never configured — it counts as configured). Callers: clear on an orphan, clear on
   a complete pending config with and without fingerprint, save of each §2a shape. **Predicted from source:** clear follows
   `confirmAuthority` — `open` mode for anyone while sign-in is not configured; strict admin → `admin`; otherwise 401
   `AI_CONFIRM_SIGN_IN_REQUIRED` (anonymous) or 403 `AI_CONFIRM_ADMIN_REQUIRED`; save follows `adminGateRefuses` — **a DIFFERENT
   gate; tabulate both side by side** and say where they disagree. For every REFUSED call prove `settings.json` is byte-identical
   before and after and no audit row was written. **Without a CSRF token:** state the answer (pre-existing either way). **A caller
   who can clear or save where the matrix says they may not is a Major.** This discharges L-A3.
9. **AUDIT ROWS.** Read the audit sink the product actually writes (`auditLog`, `backend/server.js:302`) for every accepted clear
   and save: action, detail, actor. `AI_CONFIG_CLEARED` carries `orphanedFields` as NAMES — confirm no value.
10. **NO SECRET ANYWHERE.** Plant a distinctive fake key (never a real one) and search, with a planted-token POSITIVE CONTROL that
    DOES find it first: every response body of every drive, the server's stdout/stderr, the audit file, the log files under
    DATA_DIR, and `settings.json` (where it must appear ONLY as `ENC:`). A search that finds nothing is reportable only beside the
    control that found something in the same window.
11. **REGRESSION ON EVERY OTHER ai-config CALLER — enumerated by the drafter with scoped `git grep` at `cac9cf6` (re-run it):**
    - product callers: `static/js/first-run-setup.js` (:276, :347 confirm, :353 clear, :463 save), `static/js/settings.js` (:3585
      the AI switch, `{aiEnabled}` only), `static/settings.html` (:118, text), `backend/services/aiEnabled.js` (:125, comment);
      readers of the four stored fields in the server entry point: boot hydration (:4336-4344), the loader (:4574-4590 and
      :4825-4832), `GET /api/setup/ai-model` (:16293), confirm (:16339), and `backend/services/aiConfigProvenance.js` (:51, :66).
    - test files naming the route or the provenance module (16): `ai-config-aoai-save`, `auth-gate-fail-closed`,
      `helpers/rd549-dial-oracle-preload.js`, `rd395-ai-enabled-gate`, `rd395-ai-enabled-writer`, `rd395-ai-off-reasons`,
      `rd395-ai-toggle-ui`, `rd395-ai-toggle-write`, `rd486-ai-test-key-forwarding`, `rd516-ai-test-ssrf`,
      `rd545-ai-test-limit-survives-ai-off`, `rd549-ai-config-inert-until-confirmed`, `rd549-ai-config-provenance-unit`,
      `rd549-ai-step-pending-ui`, `rd568-harness-one-machine-identity`, `rd579-ai-config-clear-truthful`.
    Run every one of those suites at the head in one hold, named, with per-file counts (C-68 re-run set). Drive the wizard's
    pending-config panel's **Remove these settings** button path (`_aoaiPendingAct` → clear with the fingerprint) at the HTTP level
    and confirm the answer the page reads is unchanged.
12. **PRIOR WORK (C-49).** Confirm what the READY says was KEPT is byte-for-byte kept: `aiConfigActAuthority`, the 409 fingerprint
    path, the runtime-override drop, the audit action; and that `NOTHING_TO_SAVE`'s shape matches RD-395 round 2 F3's Ollama branch
    (`:16546`). Say whether RD-464 r3 F-1's own repro (its report, :339) now answers correctly, driven exactly as that gate drove it.

## 5. TARGET B — RD-639 (TIER 1). Answer each with a measurement.
1. **Scope (READ ONLY, quoted):** `git diff --name-status 7c47ec4 fe53540` = the three files; the one hunk in `purgeNow`.
2. **RED-PROOF, POSITIVE CONTROL FIRST.** In one hold: the head's cell file against `7c47ec4`'s `dataErasure.js` — predicted **every
   L1, L2, L3 red; POPULATION and L4 green** — then at `fe53540`, predicted **26/26**. Count L1's rows yourself (§1: 22, not 23).
3. **The mutant table (the builder ran none — every arm is new):** **M-B1** drop the `existsSync(liveLinkTarget)` test (a link is
   always `purged`) → predicted every L1, L2, L3; **M-B2** record a failure for EVERY store (the anti-vacuity mutant L3 exists for)
   → predicted L3 red and **POPULATION/L4 behaviour stated**; **M-B3** follow the link and delete the target (`rmSync(realpath)`)
   → predicted L1/L2 red on *"target intact"* — **this is the arm that proves the "never followed" assertion bites**; **M-B4**
   non-ENOENT realpath errors swallowed → predicted **no cell reddens** (L-B3: the branch is unforced) — say so.
4. **DRIVE IT FOR REAL — the effect, not the bookkeeping (RD-575's lesson).** Through the product's own path (`requestErasure` →
   `purgeNow`, as the cells do, **and** once through the admin route `POST /api/admin/erasure-request` on a loopback server you
   booted, then the sweeper's `purgeNow`), for EVERY row of §2a-B: hash every byte of every target (and of DATA_DIR, and of a
   sentinel tree placed BESIDE DATA_DIR) before and after; read the ledger (`erasure state` file) RAW from disk; read `ok`,
   `status`, `filesPurged`, `filesFailed`, `_audit`'s row and the error log. **`purged` for a store is correct only if no byte of
   that store is readable anywhere after the run. Any deletion outside DATA_DIR is a Blocker. Any `purged` over surviving bytes is
   a Major.**
5. **THE RE-DRIVE — the attack the cells do not make (drafter prediction, READ ONLY, MEASURE IT).** After run 1 on a store linked
   to an outside file, the link is GONE and the ledger says `purged_incomplete`. The sweeper re-drives `purged_incomplete`
   (`erasureSweeperScheduler.js:80/:99/:179`). On run 2 P-3's `statSync` finds nothing → skip; `failed` is `[]`; `purgeNow`'s final
   write carries `replacesLedger: true` (`_writeState`, `:309-365`), so the surviving-target entry is REPLACED — **predicted run 2:
   `ok:true`, `status: 'purged'`, `filesFailed: []`, while the outside target still holds every byte.** If measured, that is RD-639's
   false certificate returning one sweep later: **grade it on RD-639, and say whether P-6 (recovery copies) has the same
   re-drive hole at the base** (the class). Note for Tuesday: the builder is stacking **RD-324 (ledger union)** on this branch — say
   whether RD-324 as ticketed would close this, from its ticket text if you can read it without Jira, else say UNKNOWN.
6. **INSIDE-DATA_DIR links (L-B2, discharge it):** a store linked to another LISTED store, both loop orders; a store linked to an
   INFRASTRUCTURE file. Run both runs (first + re-drive). **The infrastructure target must survive both runs.**
7. **AUTHORIZATION:** who may request an erasure (`requireAdminForDataRights`, `backend/server.js:~18891`) — drive anonymous,
   viewer, admin in the enforced state and the open window; nothing RD-639 changed, so this is a pre-existing census, labelled so.
8. **THE ERROR TEXT CARRIES AN ABSOLUTE PATH.** The failure names the target's realpath (outside DATA_DIR). Say where that string
   travels — ledger, `/api/health`'s `filesFailedCount`/detail, logs, any API response — and whether any of those is reachable by a
   non-admin. A path is not a secret; a path in an anonymous response is a finding.
9. **C-68 re-run set for B (named, per-file counts, one hold):** every test file naming `dataErasure`, `purgeNow` or
   `requestErasure` at `fe53540` — **20 files** by the drafter's scoped `git grep -l` (re-run it) — including
   `erasure-reaches-attachments` (RD-575's C4, the in-tree twin), `erasure-verdict-is-derived-from-failures` (P-6),
   `erasure-incomplete-is-not-a-dead-end`, `erasure-ledger-survives-every-writer`, `rd525-export-and-erasure-cover-every-store`,
   `rd631-export-directory-branch-declared-only`.
10. **PRIOR WORK (C-49):** confirm RD-575's comment and `_purgeTree`'s link rule are unchanged, and that the failure text matches
    P-6's byte for byte. Re-run gate 4's F-A1 repro exactly as gate 4 ran it (its evidence: `storelink-classcheck.txt`).

## 6. THE MERGED TREE (C-68, C-57, C-89, C-112). Neither verdict is complete without it.
1. **Build it in YOUR OWN scratch clone** under `projects/nexusai/qa-trees/g579-639.*/clone`:
   `git clone --shared --no-checkout <repo> <dir>`; in the clone only: a local `user.name`/`user.email`; `git checkout -b gate
   7c47ec4`; `git merge --no-ff cac9cf6`; then `git merge --no-ff fe53540`. **Predicted: each merge conflicts ONLY in
   `scripts/verify-expected-counts.json`** (quote git's output). Anything else conflicting **STOPS** (C-57).
2. **Resolve the counts file by REGENERATION, never by hand:** take either side to complete the merge commit, then
   `npm run verify -- --maxWorkers=2 --update-counts` ONCE on the tree that exists after BOTH merges, through the lock, SESSION_SECRET
   UNSET, and commit the regenerated file in the clone. **Predicted 4012/237 — a prediction; the measurement decides.** Also measure
   main + RD-579 alone (the builder predicted **3986/236**) and report whether its prediction held.
3. **Order independence (a control that can fail):** build the other order too (`fe53540` first, then `cac9cf6`) in a second
   clone; **the two merge results' `HEAD^{tree}` minus the counts file must be identical** — quote both tree ids and the
   `git diff --name-only` between them.
4. **Blob identities on the merged tree:** `backend/server.js` = `cac9cf6`'s (`30aeff7…`), `backend/dataErasure.js` = `fe53540`'s
   (`4835697…`), `azure-marketplace/combined/mainTemplate.json` = `7c47ec4`'s, every `__tests__` file byte-identical to one parent
   (**C-112's condition — state it beside the conclusion**), 0 files absent.
5. **id-superset control (C-57):** merged test ids ⊇ ids(`7c47ec4`) ∪ ids(`cac9cf6`) ∪ ids(`fe53540`); **missing 0 predicted**
   (both branches are one merge from main's line, not long-lived). Use a COPY of `session-tools/c57-id-superset.sh` in your own
   project, against your own trees. If it misses, apply C-133 verbatim and list every accounted id.
6. **Run on the merged tree, one hold:** rd579 (8) and rd639 (26), both C-68 re-run sets (§4 Q11, §5 Q9), and the full verify.
   Then ONE mutant per ticket on the merged tree (M1 for A, M-B1 for B): **the tables must still hold through the other change.**
7. **C-89 on your clone:** `git diff --quiet HEAD` holds and `git show HEAD:scripts/verify-expected-counts.json` equals the
   regenerated counts.
8. **Nothing leaves your clone.** No push, no remote added, no ref written in the NexusAI repo. `git clone --shared` reads the
   source's objects through alternates and writes into the clone only — **count `<repo>/.git/objects` files before and after your
   whole session and account for any delta by mtime** (four live seats commit into that repo; their objects are not yours).

## 7. CI (C-142) — RELAYED ON MAIN, NOT RUN AT EITHER BRANCH HEAD
- Main `7c47ec4`: Build **36133932540** success, *"VERDICT: PASS — 3978/3978 tests passed across 235 suites"*; Gitleaks
  36133932459 success; npm-audit success; Deploy demo 36133932539 skipped — **all RELAYED from the RD-579 READY, not read by the
  drafter.** Confirm with `gh run view 36133932540` (READ ONLY, NexusAI's own `GH_CONFIG_DIR`), label it READ ONLY.
- **`gh` never merges, approves, comments, reviews, labels, re-runs, dispatches or opens a PR.** Neither branch has a PR; **report CI
  NOT RUN for `cac9cf6` and `fe53540`.**

## 8. Floor discipline — THE FOUR CLAUSES, plus THE DEADLINE RULE
1. **Every jest run goes through `session-tools/nexusai-lock.sh`, tagged `qa-rd579-…`** (C-141: gate-class; C-110: otherwise no
   queue jumping). **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit another seat's process, lock directory, owner file
   or ticket, even if it looks stuck; if a holder looks stuck, mail a QUESTION (§10) and keep waiting. Live-server probes are floor
   load: run them inside your own hold.
2. **Hold the lock ONCE per multi-run measurement.** Every hold is a TRACKED CHILD of your seat, never detached (`nohup … &`).
3. **Count foreign servers the RD-606 / C-125 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND the server
   entry point anywhere in the remaining argv (kernel argv); "ours" = the ancestor chain CONTAINS your own claude pid. **NEGATIVE
   controls, all in the same run, all must classify FOREIGN — read at drafting 2026-09-25 22:55 AEST from
   `tmux list-panes -a -F '#{pane_id} #{@cockpit_name} #{pane_pid}'` + `ps`:** NexusAI-M claude **`88756`** (pane `%11`),
   NexusAI-N claude **`10246`** (pane `%12`), NexusAI-O claude **`10643`** (pane `%13`), NexusAI-P claude **`11987`** (pane `%14`),
   and Tuesday's claude **`60235`** (pane `%0`). Re-read them at start; if one has exited, say so and use the others; **a hold with
   NO live negative control aborts.** Reuse gate 7's instrument BY COPY with YOUR pid as `ROOT` and these as `NEG`:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`
   and `…/evidence/qa-floorlib.sh` (its first line names gate 7's pid — correct it to yours before any hold).
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, "no secret found" (§4 Q10),
   "no byte outside DATA_DIR deleted" (§5 Q4) and "no cell reddens" under M5/M6/M-B4.

**5. THE DEADLINE RULE — every real-server probe has a per-step DEADLINE, a HEARTBEAT, and kills its server in a `finally`.**
Every HTTP request carries a client timeout; each step (boot 60 s, request 30 s, purge 60 s, exit 20 s) has a written DEADLINE; a
step past it is ABORTED and reported, never waited on. **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every
2 minutes during any hold; a step with no heartbeat for 5 minutes is aborted and reported,** and a hold that is not progressing
releases the lock. Every server you start is killed in a `finally` (SIGTERM, then SIGKILL after a grace) and the reap is confirmed
by your floor counter.

## 9. HELD
- **LOCAL RUN, NOT THE DEMO:** every request goes to a server YOU booted on 127.0.0.1 from YOUR tree. No request to any live, demo or
  public host; **no Azure OpenAI host is ever dialled** — every key and endpoint is fake, and any AI sink is an in-test loopback
  recorder. This is authorised defensive QA of Datasec's own product on loopback.
- No merge (outside your own clone), no push, no deploy, no registry, no Partner Center, no production, no money, no external
  comms, no mail to any human. **No `az` at all.** `gh` READ-ONLY and optional (§7).
- **Symlinks, hard links and chmod live ONLY under your own mktemp dirs.** Never link to, chmod or plant anything in a real home
  directory, the NexusAI tree, or any other seat's directory. A link to `/` or `$HOME` (§2a-B) is created inside your temp dir and
  pointed at — never written through — and a sentinel tree beside DATA_DIR proves nothing else was touched.
- **Findings-only:** do not commit (outside your clone), move any branch, file a ticket, or write anything inside the NexusAI project
  (`2_Project_Files`, `session-tools/`, `worktrees/`, `1_Project_Definition/`). **NEVER `rm`** — quarantine, per the template §5.
- No docker is needed by this gate.

## 10. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/report.md` — ONE
report covering both tickets.

**Questions:** your routing name is **`QA/NexusAI-g579-639`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by) and **PROCEED ON THE SAFEST
READING without waiting**; Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning
`[Tuesday -> QA/NexusAI-g579-639] ANSWER`. Approval-class items are NOT RUN and named. Record every question, reading and answer.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-579: <GO|GO WITH FINDINGS|NO GO> @ cac9cf6 · RD-639: <GO|GO WITH FINDINGS|NO GO> @ fe53540`
Lead the body with one sentence per ticket. Never `wednesday-agent@`. AgentMail key: `AGENTMAIL_API_KEY` in
`/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute: the QA project has none). Never put the key, or any secret, in a
mail or the report.

Verdict format:
- **RD-579: GO / GO WITH FINDINGS / NO GO** naming `cac9cf641c86ff89a48aa42d7447cdcfbbeaa6c1`: the red-proof (`0677388` and
  `7c47ec4` red, head green, same window) first; then M1-M7; the 500 branch driven (§4 Q4); the three behaviour claims on disk; the
  authorization matrix; audit; the secret search with its positive control; the caller regression set; prior work.
- **RD-639: GO / GO WITH FINDINGS / NO GO** naming `fe53540fbaf628fa3ca5eb790d023ecf5ae71f0c`: the red-proof; M-B1..M-B4; every §2a-B
  row with before/after hashes; **the re-drive (§5 Q5) stated plainly**; inside-DATA_DIR links; the hard-link class sibling; nothing
  deleted outside DATA_DIR, with the sentinel control.
- **The merged tree (§6):** both orders, conflicts quoted, counts regenerated once (measured vs 4012/237 and vs the builder's
  3986/236), id-superset with C-112's condition beside it, the merged runs and mutants, C-89.
- Each of **L-A1..L-A4 and L-B1..L-B4** answered: discharged with a measurement, or left standing and named (C-112).
- Report all three refs as **three timestamped readings (start / mid / end)**, each with its branch name.
- Every action recommendation carries its evidence class: **MEASURED AT RUNTIME / PROBED / READ ONLY**. Severity is yours; priority
  is Tuesday's.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Not tested by this gate: a real browser (the wizard's rendering of a 400 or of a 500 from clear), Linux or CI at either branch head (no PR exists), a store on a real second disk or network mount, Windows junctions, and the export side of a symlinked store (C-139).

## WRONG OR UNVERIFIED IN THE COMMISSION AND THE READYS — carried so the gate inherits the corrections
1. **RD-639 READY: "L1: one per CUSTOMER_DATA_FILES name (23)".** The list at `fe53540` has **22** entries, and 26 cells = 1 + 22 + 3.
   Off by one at source (READ + arithmetic; the gate counts it).
2. **RD-579 READY: clear "decides from the raw stored AOAI fields".** It decides from `jsonStorage.getSetting`, which DECRYPTS and
   returns `null` for an `ENC:` value no key candidate opens. Not raw. §2a-A last row.
3. **RD-579 READY: "The property holds by construction" (the 500 read-back).** A claim (C-76), and the 500's text *"Nothing is
   reported as removed"* is written after other fields have been nulled with no audit row. §4 Q4.
4. **RD-639 READY: "the re-drive completes" (L-B2).** True of the files; the drafter predicts the re-drive also turns an OUTSIDE
   target's failure into `purged`. Unmeasured. §5 Q5.
5. **RD-579's cells are all anonymous-in-open-window**, and S2 checks that the key is PRESENT after rotation, not that it CHANGED.
6. **CI on main 7c47ec4 GREEN is RELAYED**, not re-read by the drafter.
7. **Main is not RD-579's base** (`0677388` is); it is RD-639's base. "Red at 0677388/7c47ec4" is one test: `backend/server.js` is the
   same blob at both.
8. **The builder's RD-579 green and mutation logs ran 18 minutes before the commit**; they are tied to it only by the sha256 prefix
   `6eb4c675b5900f3f` (drafter-verified).

## PROVENANCE (drafter, 2026-09-25 22:50–23:30 AEST, read-only)
- origin heads main `7c47ec4…`, `rd-579-ai-config-clear-s84m` `cac9cf6…`, `rd-639-erasure-symlink-s84n` `fe53540…` |
  `git ls-remote origin` | read 22:52:26 and 22:54:43, identical
- chains: `0677388..cac9cf6` = `cac9cf6` (parent `0677388`); `0677388..7c47ec4` = `c5d053b`, `7c47ec4`; `7c47ec4..fe53540` =
  `fe53540` (parent `7c47ec4`); `merge-base(cac9cf6, 7c47ec4) = 0677388`, `merge-base(fe53540, 7c47ec4) = 7c47ec4` |
  `git log --format='%H %P'`, `git merge-base` | 22:52, 22:54
- deltas and disjointness | `git diff --stat`, `git diff --name-only` + `comm -12` | 22:52, 22:54
- counts 0677388 3974/234 · c5d053b 3974/234 · 7c47ec4 3978/235 · cac9cf6 3982/235 · fe53540 4004/236 |
  `git show <sha>:scripts/verify-expected-counts.json` | 22:53, 22:54
- blobs: server.js fa0d262 (0677388, 7c47ec4, fe53540), 30aeff7 (cac9cf6); dataErasure.js 7992700 (0677388, 7c47ec4, cac9cf6),
  4835697 (fe53540); package-lock 9064763 at all four; sha256 prefixes 6eb4c675b5900f3f (cac9cf6 server.js), e75914eeb26d
  (fe53540 dataErasure.js) | `git rev-parse <sha>:<path>`, `git show … | shasum -a 256` | 22:53–22:58
- the RD-579 diff, the save route, `aiConfigActAuthority`, `confirmAuthority`, `readStatus`, `jsonStorage._decryptCandidates`, the
  hydration and loader readers | `git show cac9cf6:<file>`, `git diff 0677388 cac9cf6` | 22:55–23:00
- the RD-639 diff, P-3/P-6/`_purgeTree` context, `_writeState`'s `replacesLedger`, the sweeper re-drive lines, the erasure route
  guard | `git show fe53540:<file>`, `git diff 7c47ec4 fe53540` | 23:00–23:08
- caller sets: `git grep -n "api/setup/ai-config" cac9cf6 -- static backend scripts docs`; `git grep -l` over `__tests__` for the
  route/provenance (16) and for `dataErasure|purgeNow|requestErasure` at fe53540 (20) | 22:58, 23:04
- builder evidence present: `session-tools/s84m/` (green, red-at-0677388, mutations .sh/.log, verify, READY copy) and
  `session-tools/s84n/rd639/` (hold.sh, hold.out, A-base, B-fixed, C-verify) | `ls`, `head`, `grep` | 22:57, 23:02
- negative-control seats %11 → 88756 (M), %12 → 10246 (N), %13 → 10643 (O), %14 → 11987 (P), %0 → 60235 (Tuesday) |
  `tmux list-panes -a -F …`, `ps` | 22:55
- CLARIFICATIONS line numbers (file 268,324 bytes, mtime 21:57; highest C-162 at :1644) | `grep -n` | 23:05
- routing lines `QA/NexusAI-rd579` (:105) and `QA/NexusAI-g579-639` (:106) present in `fleet/inbox_routing.conf` | `grep -n` | 23:08
- CI Build 36133932540 on 7c47ec4 | **RELAYED** from the RD-579 READY, not read
