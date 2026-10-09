LAUNCH BRIEF (Seat K 1st, proposed; Q-LANE-K): a NEW lane, pane `Secuura/Blockchain-K`. **ONE job: KS-1402 under Kam's ruling (a).** `POST /api/documents/:id/transfer-custody` with `newHolderEmail` will resolve the holder INSIDE originate, instead of forwarding the caller's credential to auth's `/api/users/lookup`. Red-first, then ONE PR, ending at `READY FOR QA (Seat K 1st): #<n> (KS-1402) -> gate<NN>` on a **tier-1 QA gate** (auth/credential surface; **never the local models**). No merge, no deploy, no key rotation, no scope change, **no ticket comment** (Wednesday's batch). Secuura NEVER force-pushes. Model: **Opus 5.5**.

> **Supersedes** `fleet/briefs_staged/2026-10-06_seatK1402_build.md` (218 lines, staged, never launched). Kept from it: its analysis, re-measured at today's develop. Changed: develop, floor, lock, tools, flow number, and the ticket comment, which moves from the seat to Wednesday.

## SEND AMENDMENT (Wednesday, at send 03:07:58Z): this block WINS where it differs from the text below
- **The brief was read WHOLE by Wednesday at send** (323 lines, drafted 09:40-10:20 against develop `1e7f90e26137`). Four things moved since: the handlebars push freeze came and went, develop moved, three seats in the partition table wrapped, and Q-MECH is ruled.
- **develop at send = `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6`** (Wednesday's `env -u GIT_SSH_COMMAND git -C <checkout> ls-remote origin`, 03:07:58Z). It is the squash of #1435 (KS-1452, handlebars 4.7.9 → 4.7.10 in five `package-lock.json` files ONLY, per the merge seat's STATUS; not re-derived by Wednesday). Your files are not among those five. **Its objects are PRESENT in the shared store** (Wednesday: `cat-file -t 81d2e5f4…` = `commit`; negative control `deadbeef…` = "could not get object info", same action). `refs/pull/1427/head` = `2b6da5f561b0` and `refs/pull/1436/head` = `90d98754db7b` (same read). The only `feature/ks-1402*` ref is the spent `-b55-1` at `aa16f3256dbf` (same read).
- **develop WILL move again** when Seat R 22nd squashes #1427 (its docs + `Blockchain/Testing/jobs/04-container-trivy.sh` + its tests). If that happens before your RAISE_BASE, the new develop's objects will be ABSENT from the store: Q-OBJ-K applies (mail and WAIT; R 22nd or Wednesday sequences the one transfer). Name the develop you read; a moved develop is not a STOP.
- **Live floor** (`tmux list-panes -a`, 03:07:58Z): `%0 wednesday` · `%1 fleet-monitor` · **`%8 Secuura/Blockchain-R` = Seat R 22nd** (merge seat for #1427, KS-1274; token `ra22`; its lock is the R lineage's `.push-lock-d8`; files = the trivy job + `Blockchain/Dev/scripts/__tests__/container_trivy_*` + both platform docs, flow `35.`). **The partition table's other rows are STALE:** F 6th WRAPPED (its #1436, KS-808, is OPEN at READY, head `90d98754db7b`, worktree `s-f6-ks808` KEPT: never touch); R 21st WRAPPED (R 22nd is its successor); J 1st WRAPPED (board writes done); lane V (#1435) MERGED and wrapped (worktree `s-v1-hbslock` KEPT: never touch). **gate77** (later, not launched) will gate #1429-#1434 + #1436 after #1427 lands; #1436 took flow `41.`. Your code files are in none of those PRs (drafter's 8-head census; #1436 is `run-migrations.sh` + its test + the docs, so it does not touch your files either).
- **Locks:** 0 `.push-lock*` dirs at `worktrees/` by Wednesday's `find -maxdepth 1` at 03:07:58Z (NO control run by Wednesday: re-measure with your private `mktemp -d` control).
- **Sole live Secuura session at launch? NO** (R 22nd is live). So your launcher's boot pull is **READ-ONLY** (KS-907). Record which, per ITEM 0(a).
- **Usage at send: 19%** (`usage_gate.sh --check`, gauge age 3 min). Clause: **cloud: build** (an auth/credential surface fails the Spark predicate; Kam 13:55 today: the Spark as much as possible, so this seat carries 0 Spark tasks and says so).
- **MODEL:** your launcher pins `claude-opus-5`. Wednesday types **`/model claude-opus-5-5`** into your pane at its IDLE prompt (a tap would arrive as a message, not a command) and confirms by mail. Kam's standing word today: every agent on Opus 5.5 for now.
- **RULINGS on the drafter's questions (Wednesday, at send):**
  - **Q-MECH = the DB lookup, sub-choice = the DIRECT `users` SELECT** (the id-path's shape: request db, bound tenant predicate AND the RLS tenant GUC, auth's `toLowerCase().trim()` normalisation). **Why this is inside Kam's ruling and not a reading against it:** the card's option (a) text names it "Stuart's option 2", and Stuart's message offered "users:read + re-mint, **or originate resolves itself**" (`0_Brain/reference/2026-10-09_stuart-list/REPORT.md:34`, Wednesday's drafter quoting Stuart; Wednesday read the card's option text with `decision_queue.sh show` at send). A DB read under originate's own database role IS originate resolving the holder itself with its own credential; the token reading would ADD a credential class Kam did not mention. **Kam is told on his panel as a one-line FYI with his veto; if he vetoes, Wednesday mails you before ITEM 2.** Q-MECH no longer HOLDS ITEM 1: after the plan ANSWER and a ctx read under 45%, proceed.
  - **Every other question at the drafter's recommended default:** Q-SCOPE one path for all callers · Q-NULLT keep `tenant_id IS NULL` tolerance, pinned by C7 · Q-LEGACY declare the gap in NOT COVERED (no stack built for it) · Q-KEY catch and answer 502 `BAD_GATEWAY`, pinned by C9 · Q-739 retire/re-point with a WHY per cell, all 17 listed · Q-HELPER inline (≤ ~25 lines) · Q-LANE-K **K 1st** · Q-LOCK-K **`.push-lock-g1`** (holder seat `Secuura/Blockchain-K k1`) · Q-NUM **`44.`** (re-measure: R 22nd is `35.`, #1436 `41.`; a number collision is a STOP) · Q-OBJ-K mail and wait · Q-BRANCH-K / Q-SUBJ-K as recommended.
- **Tool note from Seat V 1st's WRAP (it used the same G kit today):** `pushg1.sh` pipes through `gatelinesg1.py`, and its absence was swallowed by `|| true`. Before you trust `pushk1.sh`, confirm `gatelinesk1.py` is present in YOUR copy and make the push tool fail LOUDLY if it is missing (planted-absence control). The tool still wins over this brief where they disagree.
- **This seat ends at READY FOR QA, tier 1.** No merge, no ticket comment (Wednesday's batch through a board seat), no message to Peter or Stuart.
- Wednesday's pane is `%0`. Send all mail to `wednesday-agent@agentmail.to`.



## 🔴 THE MECHANISM, STATED PLAINLY
- **Kam's words** (card `secuura-ks1402-s-key-cannot-carry-users-read-1006`, choice `a`, `ruled_ts=2026-10-06T09:58:21.119827+11:00`): *"a: Originate resolves the holder with its own service credential (Stuart's option 2)."* Detail, verbatim: *"No scope change and no re-mint of any live key. Keeps 'on-behalf-of resolution is K-side'. A K build round, then the QA gate, then a merge. The cross-tenant guard must be proved by the gate."*
- **What this brief builds is a DATABASE LOOKUP, not a service token.**
  - Originate computes `lookupHash(<normalised email>)` and reads `users` itself.
  - The read runs on the request's db handle, under originate's OWN database credential: its `DATABASE_URL` role, `secuura_app` by default (`docker-compose.yml:581` at develop).
  - It carries an explicit, bound `tenant_id` predicate AND the request's RLS tenant GUC.
  - **No bearer token is minted, stored or sent. auth's `/api/users/lookup` is no longer called from this route. auth is not changed.**
- **This is a READING of Kam's sentence, not his sentence.** "Its own service credential" can mean originate's own database role (this brief), or a service token that originate presents to auth's `/lookup` (a literal reading). **The brief deviates from the literal reading, so it is Q-MECH, for Wednesday. She decides whether it goes to Kam. Q-MECH HOLDS ITEM 1 onward.**
- Why the drafter recommends the DB reading (each point measured at develop `1e7f90e26137`):
  1. **Originate holds no service bearer of any kind.** A grep for service/internal token patterns over non-test `services/*/src` + `packages/*/src` returned 5 lines: 4 `DEMO_SERVICE_KEY` in demo-service, 1 prose comment in m365-integration. That is 0 in originate and 0 in shared; nonsense-token control rc 1. A token route therefore means a NEW secret and a NEW credential class, which sits closer to Kam's signature class than a read under a credential originate already holds.
  2. **A tenant-less service credential at auth's `/lookup` resolves ACROSS tenants.** `services/auth/src/routes/users.ts:306` (blob `da7341a55f31`) skips the tenant compare when the caller credential carries no `tenantId`. That is exactly the guard Kam said the gate must prove (the KS 1406 class).
  3. **The precedent exists in this same handler.** The id-path holder check `routes/documents.ts:1799-1805` (blob `343eacec7fe8`) does `db.$queryRaw … WHERE id = … AND (tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)` on `(req as any).db`. The hashing precedent is `services/originate/src/services/provenance.ts:110` (blob `483aa9eb331d`): `lookupHash(obo.email.toLowerCase())`.
- **Whichever way Q-MECH goes, the PR body and the READY state the mechanism in one sentence, beside Kam's ruling quoted verbatim, and say it is a reading.**

# LAUNCH BRIEF: Seat K 1st, Secuura/Blockchain, lane K (pane `Secuura/Blockchain-K`). From Wednesday.
Drafted by Wednesday's brief-drafting sub-agent 2026-10-09 ~09:40-10:20 AEDT. Every value carries its instrument. Every value marked "drafter" is the drafter's own measurement: you RE-MEASURE it before you rely on it.

## MODEL
- Kam, 2026-10-09 ~09:4x, verbatim: *"for now, use Opus 5.5 for all sub agnets"* (top block of `0_Brain/learnings/2026-10-09_spark-ornith-sonnet-only-until-monday.md`).
- Your launcher pins an older Opus. Wednesday switches your pane with `/model claude-opus-5-5` right after launch and confirms by mail.
- Add `MODEL: <as your session reports it>` to every STATUS, READY and WRAP mail.
- **Routing:** this is an auth/credential surface, so it fails the Spark predicate. The REPORT's disposition reads "Not Spark/Ornith". No local-model task rides with this seat.

## USAGE AUTHORITY
- The weekly allowance renewed this morning (`usage_gate.sh --check` 0% at 09:15 AEDT, 1% at 09:2x). **The normal 90% stop applies; no `WED_USAGE_STOP`.**
- Authority: Kam's standing week instruction (2026-10-04, renewed to Sun 11 Oct), clause RAISE, plus card `…-1006` = a ("A K build round, then the QA gate, then a merge").
- **Ctx lines:** a build starts only under 45%. A push at 45-64% goes only on Wednesday's per-step word. **The hard ceiling is 65%: WRAP COLD.** Mail `QUESTION: ctx read (Seat K 1st)` before ITEM 1 and before the push.

## BLUF
- **The defect** (drafter, at develop `1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0`):
  - `routes/documents.ts:1664-1750` resolves `newHolderEmail` by `fetch(\`${authBase}/api/users/lookup?email=…\`)`, forwarding the CALLER's `Authorization` (`:1666`, `:1669-1671`).
  - auth's gate needs a role in `ALLOWED_LOOKUP_ROLES` (`users.ts:180`) or the `users:read` scope (`:223`, `:284`).
  - S's connector key is minted WITHOUT `users:read` on purpose (`api-gateway/src/routes/platform.ts:477-478`: "−users:read (Stuart ③ — on-behalf-of resolution is K-side, §6)"; `S_CONNECTOR_SCOPES` `:485-489`, nine scopes).
  - Result: since #1374 (`2d85b84e1012`, an ancestor of develop), every S custody transfer by email gets 403. Stuart measured 7 of 7 refused (KS-1402 comment `d280f168`, 2026-10-05T09:53:44Z) and still 403 on 6 Oct (`7740c258`).
- **The act's authorisation stays on the caller.** `:1599` `isAllowedByRoleOrScope(req, ALLOWED_TRANSFER_CUSTODY_ROLES, 'documents:transfer-custody')` runs BEFORE resolution and stays byte-unchanged. **Only RESOLUTION moves into originate.**
- **Disjoint from the live floor.** No open PR head touches `routes/documents.ts`, `originate.openapi.ts`, `provenance.ts`, the ks739 test or auth `users.ts` (drafter: 0 of 8 heads: #1383, #1427, #1429-#1434). **One shared GENERATED file:** `Blockchain/Dev/docs/openapi/secuura-api.yaml` is in #1429 (KS-1449, gate77), and it is expected in E 12th's unraised KS-591 / KS-1364 work. Regenerate it; never hand-merge it.
- **Flow number `44.` is proposed (Q-NUM).** The highest flow `<h2>` number on develop and on every one of the 130 `refs/pull/*/head` that exist from #1300 to #1434 is `43.` (#1430). `32.` is reserved (KS-1432), and `33.`/`34.` belong to the E lane's unraised KS-591 / KS-1364. Your cheat section `KS-1402` goes LAST.
- **Your lock is `.push-lock-g1`, adopted (Q-LOCK-K).** A new `.push-lock-k1` would be an UNATTRIBUTED lock to both live seats' catch-alls (a STOP). `.push-lock-g1` is a WAIT by path in both: F 6th `raise/lockf3.sh:335`, R lineage `tools/lockra1.sh:303`. 0 locks were present at 22:43:27Z.
- **Expect ONE PR, then WRAP.** Never end a turn on a "next up" line with nothing running (STANDING_LINES `:342`).

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** Where your copy of a tool and this brief disagree about a gate, a knob, a path or a line number, **THE TOOL WINS**: run nothing on the disputed point and mail.

**WAKE:** your re-keyed `inbox_watchk1.sh` (from G 5th's), armed in the background at boot with `timeout: 7200000`.
- It EXITS when it fires: re-arm IN THE SAME ACTION that reads each mail, with `SINCE` = the newest mail READ (STANDING_LINES `:403`).
- After any long action (install, suite, push), LIST the inbox by API before the next ref write.
- Name a watcher pid only from a `ps` FILE.
- Stop every watcher before WRAP, and prove 0 live with a positive control.

## THE PARTITION (one checkout, one inbox `secuura-blockchain@agentmail.to`)
Drafter's reads: `tmux list-panes -a` at 22:4xZ; `ls-remote` at 22:38:26Z; locks by `find -maxdepth 1` at 22:43:27Z (0 found; a private `mktemp -d` control read 1). Paths: `svc/` = `Blockchain/Dev/services/`.

| Seat | Pane | Token / lock | Files | Doc block |
|---|---|---|---|---|
| **K 1st (you)** | `Secuura/Blockchain-K` (NEW; id by mail) | `k1` / `.push-lock-g1` (adopted; holder seat `Secuura/Blockchain-K k1`); worktree `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-k1-ks1402` | `svc/originate/src/routes/documents.ts` (the transfer-custody email block `:1657-1750` and its comments ONLY) · possibly ONE new originate helper (Q-HELPER) · NEW `svc/originate/src/__tests__/ks1402-transfer-custody-resolves-holder-email-in-originate.test.ts` · `svc/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts` (cells this change retires or re-points; Q-739) · `svc/originate/src/originate.openapi.ts` (`:1635`, `:1740-1770` descriptions only) · regenerated `Blockchain/Dev/docs/openapi/secuura-api.yaml` · both platform docs | flow `44.`, cheat `KS-1402` LAST |
| F 6th | `%2` `Secuura/Blockchain-F` | `f6` / `.push-lock-f3` | KS-808: `Blockchain/Dev/scripts/run-migrations.sh` + NEW `Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh` + both docs | `41.` |
| R 21st | `%3` `Secuura/Blockchain-R` | `ra21` / `.push-lock-d8` | the merge of #1427 (KS-1274): `Blockchain/Testing/jobs/04-container-trivy.sh` + `Blockchain/Dev/scripts/__tests__/container_trivy_*` (3) + both docs. It moves develop. | `35.` |
| J 1st (if launched; brief staged beside this) | `Secuura/Blockchain-J` | `j1` / no lock | Linear only: KS-1387, KS-1172, KS-1175 | — |
| gate77 (later) | `QA/…` | the merge seat it names | gates #1429-#1434; #1429 touches `secuura-api.yaml` | — |
| E 12th (expected) | `Secuura/Blockchain-E` | `.push-lock-e4` | KS-591 + KS-1364: `docs/openapi/secuura-api.yaml` + `svc/*/src/*.openapi.ts` + tests | `33.`, `34.` |

- **Measured disjoint** (drafter, `git diff --name-only $(merge-base develop H) H` per head): your code and test files appear in 0 of #1383, #1427, #1429, #1430, #1431, #1432, #1433, #1434. Each head touches exactly 2 doc paths (the positive control). Only #1429 touches `secuura-api.yaml`.
- **SEQUENCING VERDICT:**
  1. `routes/documents.ts`: no open PR touches it, so BUILD IN PARALLEL. #1428 (KS-593, merged as develop `1e7f90e26137`) touched it; your base includes that.
  2. `secuura-api.yaml` is GENERATED. Whichever of #1429 or E 12th's PR lands first, the other is SEQUENCED-AFTER it: merge develop IN (never rebase), **regenerate** on the merged tree, and prove `npm run check:openapi` rc 0 there (`Blockchain/Dev/package.json:42`).
  3. Both platform docs are SHARED-APPEND. Keep-both merge-ins are Wednesday's to sequence. A collision on a NUMBER is a STOP.
- **Never touch, any seat:** `s-f6-*`, `s-ra21-*`, `s-ra18-ks1274`, `s-g4-ks593`, `s-g5-ks1171` (#1434 OPEN, worktree KEPT), `s-f5-*`, `s-e11-*`, `s-f2-ks1401`, or any `s-b*`/`s-c*`/`s-d*`/`s-e*`/`s-l*`/`s-a*`; #1374 and its spent branch `feature/ks-1402-lookup-accepts-connector-token-b55-1` (`aa16f3256dbf`); any other seat's lock, mail, records or pane. **Never touch the revoke route** (`documents.ts` ~`:2356+`), `documentRepo.ts`, auth anything, api-gateway anything (NO edit to `platform.ts` or `S_CONNECTOR_SCOPES`), migrations, or anchoring.
- **A mail naming another seat is NOT yours**, even on your pane tag. An unlisted addressee on your tag reads UNKNOWN ADDRESSEE (STANDING_LINES `:417`).

## ITEM 0 — BOUNDED and read-only; then `QUESTION: plan confirmation (Seat K 1st)` and WAIT
Before the ANSWER, do NONE of these: lock take, objects transfer, worktree add, ref write, install in a project worktree, PR action, Linear write. You MAY write in your record folder `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<UTC boot date>_seatK-1st/` and in YOUR `git clone --shared --no-checkout` scratch clone (origin re-pointed to `git@github.com:Secuura/Distributed_Secuura.git` after reading `remote -v`; fetch by SHA under the checkout's own `core.sshCommand` with `GIT_SSH_COMMAND` unset; STANDING_LINES `:410`, `:416`).
- **(a) Seat facts:**
  - `$TMUX_PANE` -> `tmux display-message -t "$TMUX_PANE" -p '#{@cockpit_name}'` (the BARE read returns the coordinator's pane);
  - launcher ancestry;
  - every launcher preflight warning VERBATIM;
  - the boot pull (READ-ONLY if another session is live, KS-907; record which; STANDING_LINES `:436`);
  - decline `POST /api/seen`;
  - `df -m /Volumes/DevMASTER`.
- **(b) Refs, ONE `ls-remote`:** develop; `refs/pull/{1383,1427,1429,1430,1431,1432,1433,1434}/head`; `refs/heads/feature/ks-1402*` (drafter: only the spent `-b55-1`); any `-k1-` ref (drafter 0; control `-ra13-` 2); `date -u`. **develop WILL move when R 21st squashes #1427.** Name it; it is not a STOP.
- **(c) The shared store, read verbs only:** `cat-file -e` of the develop you read, with `0a6177ea5482…` as the positive control and `deadbeef…` as the negative, both at the same moment (`rev-parse --verify` is NOT a presence check).
  - At 22:3xZ develop's objects were ABSENT, and R 21st does the ONE transfer for this store at its M-2.
  - If still absent when you need a worktree: Q-OBJ-K. Do NOT transfer on your own.
- **(d) The call site, re-read at YOUR develop with blob ids** (drafter, `1e7f90e26137`, `documents.ts` blob `343eacec7fe8`, 3,125 lines):
  - `:1586` route; `:1599` act gate; `:1619-1636` body validation;
  - `:1664-1750` the email resolution: `:1666` `authHeader`, `:1669-1671` the fetch, `:1673` the 404, `:1683-1692` the 400/422 map, `:1693-1734` the KS 739 4xx passthrough, `:1735-1749` the 502 arms;
  - `:1759` `tenantId = getReqTenantId(req)`; `:1799-1805` the id-path holder read.
  - **The ONLY `users/lookup` caller in originate** (census with a must-hit and a nonsense control, read from a FILE).
  - `git log --format='%h %s' 22b268143a63..<develop> -- <documents.ts> <auth users.ts>` (drafter: `1e7f90e26` KS-593, `f42161da3` KS-1278 (the revoke route), `3f9ff4e1e` KS-938 (auth MFA)). State whether any of them moved a line in your block.
- **(e) The mechanism inputs, each measured:**
  - **Hash:** `lookupHash` (`packages/shared/src/crypto/encryptedField.ts:592-598`) THROWS when the key is unregistered; it is not a silent miss (the 10-06 brief said "silent miss", which was wrong). Originate registers the key ONLY inside `if (process.env.PII_ENCRYPTION_KEY)` (`services/originate/src/index.ts:369-376`, via `initFromEnv` at `encryptedField.ts:633`). Measure what auth does, and whether there is any deployment where auth has the key and originate does not (Q-KEY).
  - **Normalisation:** auth hashes `email.toLowerCase().trim()` (`services/auth/src/repositories/userRepo.ts:577`). `provenance.ts:110` lowercases WITHOUT trim. **Copy auth's normalisation, not provenance's.**
  - **Legacy rows:** auth falls back to `auth_find_user_by_email_legacy` (`userRepo.ts:591`; `migrations/039_rls_fail_closed.sql:191`) for rows whose `email` is not yet encrypted. Measure whether originate can or should reproduce it (Q-LEGACY).
  - **Scoping:** copy the id-path's scoping (`:1799-1805`, the request db + bound tenant predicate). Do NOT copy `provenance.ts:112-114`, which uses the DEFAULT prisma with NO tenant predicate. Alternative under Q-MECH: auth's own SECURITY DEFINER `auth_find_user_by_email_hash` (`039:185`, cross-tenant by design) plus an app-layer tenant compare. State which, and why.
  - **RLS:** whether a `users` row with `tenant_id IS NULL` is visible under the tenant GUC (Q-NULLT).
- **(f) Blast radius:** after the change NO caller reaches auth's `/lookup` from this route. So:
  - the KS 739 4xx passthrough (`:1693-1734`) and the 502 arms (`:1735-1749`) can no longer fire there;
  - list each of the 17 `it(`/`test(` cells in `ks739-transfer-custody-lookup-4xx-mapping.test.ts` (blob `85bf4ff3d910`, 383 lines), RETIRED (why) or RE-POINTED (Q-739);
  - **the malformed-email 400 MUST survive:** validate the format in originate before hashing.
- **(g) The partition re-measured:** three-dot file sets of every open head you can read; the lock floor ATTRIBUTED by holder `seat`, two polls a minute apart, control in a private `mktemp -d` (never plant in the shared `worktrees/`, STANDING_LINES `:446`); `s-k1-*` worktree and `-k1-` ref ABSENT.
- **(h) Doc tails at your develop and every open head**, with a newline-tolerant `<h2>` reader (STANDING_LINES `:413`), its planted `<h2>\n 99.` control proven both ways, and a non-zero count asserted (STANDING_LINES `:438`). Confirm `44.` free and `KS-1402`'s existing cheat/flow mentions (drafter: 4 in the cheat, 6 in the flow, from #1374).
- **(i) The project MUSTs quoted from YOUR develop with blob ids** (HOLDS, last block).
- **(j) Linear, read-only, by id:** KS-1402 (state, assignee, parent KS-772, `comments(first:50)` sorted client-side, attachments) and KS-1406, plus KS-99999 in its OWN query as the fabricated-key control.
  - **Board search** for the new behaviour's class by SYMBOL (`users/lookup`, `newHolderEmail`), PATH (`routes/documents.ts`) and ERROR (`may not resolve users by email`), with a must-hit and an inverted control (`searchIssues` is not an absence instrument).
- **(k) Tools:** the copy receipt, the re-keys, the sweep (TOOLS).
- **Your plan confirmation carries:** (a)-(k) one block each; the launcher lines VERBATIM; your restatement of every QUESTION with your measured recommendation; a ctx read request. **Budget: mailed by ~25% ctx.**

## QUEUE (after the ANSWER rules Q-MECH, and a ctx reading under 45%)
1. **ITEM 1: RAISE_BASE + worktree + red-first.**
   - Read develop FRESH and name it in `STATUS: raise base (Seat K 1st)` with its 40-hex and the doc tails AS READ from it. **Wednesday accepts it BY NAME before the worktree.**
   - Under `.push-lock-g1` (your lock tool takes and releases it; hold it short): `git worktree add --detach /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-k1-ks1402 <accepted base>`. Never `-b`.
   - OUTSIDE the lock: `npm ci --ignore-scripts` in `Blockchain/Dev` + `npm run build --workspace=packages/shared`, ASSERTING `packages/shared/dist/index.js` (STANDING_LINES `:381`, `:400`); `npm ci` in EVERY `systemTest/*` dir with a `package.json` (`:432`). Then `git status` must show 0 tracked files modified.
   - **Cells**, in the NEW test file, on the real router with the ks697/ks739 harness (`ks697-transfer-custody-holder-existence.test.ts` blob `56bbd366536c`, 306 lines; both mock `../repositories/documentRepo` and `../db`, `$queryRaw` via `mockQueryRaw`). Originate runs `jest` (`services/originate/package.json:10`); its tsconfig excludes `src/__tests__`, so prove program membership before quoting any tsc green. `fetch` is a spy that must NOT be called for `/api/users/lookup` at head.
     - **C1:** a CONNECTOR token with `documents:transfer-custody` and WITHOUT `users:read` names a same-tenant holder by email. **Base 403** (auth's refusal, mocked as auth answers today). **Head 201**: one custody event, the owner flipped to the resolved id, 0 lookup fetches.
     - **C2:** a tenant-A connector names an email whose only user is in tenant B. **Head 404 `RECIPIENT_NOT_FOUND`**, body byte-equal to C5's, 0 INSERT/UPDATE. The BOUND tenant parameter == tenant A (assert the value, not only the SQL text).
     - **C3:** a caller lacking both the scope and an allowed role. **403 at base and head**, and 0 resolution reads (the gate runs first).
     - **C4:** an interactive ACCESS token (ISSUER_ADMIN): the same holder and 201 at both.
     - **C5:** a true miss: 404 at both.
     - **C6:** a malformed email: 400 at both.
     - **C7:** null-tenant parity per Q-NULLT.
     - **C8:** `' Foo@X.com '` resolves the `foo@x.com` user (lowercased AND trimmed).
     - **C9:** an unregistered HMAC key gives the outcome Q-KEY rules, never an unlabelled 500.
   - **Red at base BY ASSERTION** (C1 must fail on the 403, not on a load error), printed with executed counts (`N of M ran`). Green at head.
   - **Multi-clause guard** (STANDING_LINES `:256`): the resolution's WHERE has two conjuncts (hash AND tenant). One red arm PER conjunct, each flipping one term with the other held.
   - **Tamper matrix**, each tamper alone, with a unique anchor (`grep -c` == 1), restored by content + whole-file sha256 (STANDING_LINES `:193-217`):
     - T1 drop the tenant predicate -> C2 reds;
     - T2 bind `DEFAULT_TENANT_ID` -> C2 reds;
     - T3 skip `:1599` -> C3 reds;
     - T4 restore the caller-header fetch -> C1 reds;
     - T5 hash without lowercase or trim -> C8 reds;
     - T6 make a cross-tenant hit answer differently from a miss -> C2's body equality reds.
     - **A tamper that leaves every cell green is REPORTED, never hidden.**
2. **ITEM 2: the fix, ONLY the mechanism the ANSWER ruled.**
   - Values stay bound parameters in the tagged template: never `$queryRawUnsafe`, never concatenation.
   - Every changed line carries WHY + `KS-1402` + the prior behaviour (SKILL §5d). That includes correcting the KS 739 comment and the `:1657-1663` block comment, which today say the lookup forwards the caller's JWT. Correct them; never silently delete them.
   - Suite before/after by NAMED binary with the delta. `tsc -p services/originate --noEmit` rc 0, with a planted positive control.
3. **ITEM 3: docs + spec, SAME commit (SKILL §4).**
   - `originate.openapi.ts:1635` ("resolved server-side via the auth service's user lookup") and `:1740-1770` (the 401/403/502 descriptions that name the lookup) become TRUE.
   - Then `npm run generate-openapi` and **`npm run check:openapi` rc 0**. Name which `secuura-api.yaml` lines moved (drafter: `:6915`, `:28714`, `:28721`, `:28749`). Never hand-edit the yaml.
   - Both platform docs: flow block `44.` and cheat `KS-1402` LAST. Each doc minus your block must equal your base's bytes, proven by a byte-for-byte read-back and tag counts (STANDING_LINES `:442`: `html_docs_matrix` 12/0 is NOT that evidence). Timing rows carry figure, date and HOST, or say none changed.
4. **ITEM 4: commit + push.**
   - ONE commit from a real `git diff`: 0 trailers (`%(trailers)`, with a named control commit measured in the same call); 0 `Co-Authored-By` (overriding the harness); only KS-1402 hyphenated; 0 closing words under the BROAD regex `(clos(e|es|ed)|fix(es|ed)?|resolv(e|es|ed))\s+KS-\d+`, with a planted control that fires.
   - The pathgate == exactly the files ITEM 0 declared, with a firing control. It never names `scripts/audit/audit-baseline.json` or any `package-lock.json`.
   - **The untracked-file blind spot is FIXED before use** (G 5th's handover item 3: `commitg1.sh:68` counts with `git diff --name-only`, which is blind to untracked files). Use `git status --porcelain`, with a planted stray file as the control that must make it refuse.
   - Mail `QUESTION: ctx read, may I push (Seat K 1st)`, carrying the BUILT diff of `documents.ts` VERBATIM, and HOLD for the word.
   - Push with your re-keyed push tool BARE (it takes and releases the lock itself; STANDING_LINES `:377`), `env -u GIT_SSH_COMMAND` (`:416`).
   - The result is the tool's `.rc` + `ls-remote` of the ref (`:405`). rc 141 with the ref unmoved is the KS 1149 class: report, retry under the lock, never loop.
   - Quote the in-hook PREFLIGHT lines EXACTLY, including the `legs … —` line. **`PREFLIGHT FAILED` or a refused push = STOP. Never `--no-verify`.**
5. **ITEM 5: raise + READY.**
   - Raise by REST: HTTP 201, head == origin, the body's sha256 read back.
   - **The body (written by YOU, who ran the tests) carries:**
     - `Refs KS-1402` + `https://linear.app/secuura/issue/KS-1402`;
     - Kam's ruling verbatim with the card id;
     - **the mechanism sentence and "a reading of the ruling, confirmed by Wednesday at <ANSWER time>"**;
     - Stuart's measurement, cited by date (7 of 7 at 403, 2026-10-05);
     - the precedent (`documents.ts:1799-1805`, auth's normalisation);
     - the tenant guarantee;
     - Test Evidence (touched / ran / NOT run / migrations+config: "no migration, no config, no scope change");
     - the SEQUENCED-AFTER statement for `secuura-api.yaml`;
     - **NOT COVERED:** `live sweep owed` (lowercase, SKILL §5f); no S↔K pair run (Stuart's `PS 992` cell goes green only after a Kintsugi deploy, which is Kam's tap); Q-LEGACY's outcome; the KS 1406 class (a tenant-less connector token) not addressed; auth's `/lookup` unchanged.
   - Foreign keys de-hyphenated (`KS 739`, `KS 1406`, `PS 992`, `KS 593`, `KS 1449`).
   - **ONE READY:** `READY FOR QA (Seat K 1st): #<n> (KS-1402) -> gate<NN>` **(tier 1: auth/credential surface)**. It carries the five READY artefacts (STANDING_LINES `:27-41`). **Item 3, the ticket comment naming the PR, is Wednesday's batch:** say so.
     - Head and develop read by `ls-remote` in the SAME action.
     - Every cell mapped to base/head; every tamper mapped to its cell.
     - NOT COVERED.
     - 🔴 Write a 40-hex value, byte count or ratio ONLY in the tool call that measured it.
   - Then WRAP.

## HOLDS
- **No merge, no merge-in this round, no deploy, no demo or Kintsugi, no live sweep, no `az`, no SSH beyond the push transport, no migration, no Docker** beyond what the pre-push hook runs.
- **No key rotation, no re-mint, no edit to `S_CONNECTOR_SCOPES` or `platform.ts`, no auth-side change, no new secret or env var, no new token** without a fresh ruling. Signature classes pause for Kam: production · money · external communication to any human · anything irreversible.
- **No Linear write of any kind** (no comment, state, assignee, label). **Kam's ruling comment and the PR-naming comment on KS-1402 are Wednesday's batch** (Q-NOTIFY12 carried; project `CLAUDE.md:185-194`). Never the extranet, never `POST /api/seen`, never an @-mention, never a message to Peter or Stuart. A ticket on Peter or Stuart stays theirs (KS-1402 is assigned to the board account; Peter created it). File NOTHING. A finding goes to Wednesday as a QUESTION, after a board search by symbol / path / error string.
- **No force push, ever** (`.githooks/pre-push:46-70`; STANDING_LINES `:399`); no `--no-verify`, `--admin`, `-u`, `ALLOW_FORCE`. Never `git push --dry-run` (it RUNS the hook, `:386`). Never `git fetch --dry-run` (`:406`). Never export `GIT_SSH_COMMAND` (`:416`).
- **After boot: no fetch or pull in the shared checkout, and never write either develop ref.** Read repo files as `git show <sha>:<path>`, never from `2_Project_Files`'s working tree (`:347`). Diffs of YOUR change are three-dot / merge-base (`:162-189`).
- **No spec hand-edit** (regenerate only). No dependency, lock, manifest, baseline or spec-version edit. **Delete nothing** (quarantine). Never write the shared checkout's working tree.
- `cmd > f 2>&1; rc=$?`, never a pipe for a status (zsh has no `PIPESTATUS`). Never `cd`. Absolute paths; `${VAR:?}`. Quote `Projects Documents/` (it has a SPACE). macOS has no `timeout`. Never name a variable `path`.
- **One inbox.** Act only on mail whose subject carries `-K]` AND `(Seat K 1st)`, from `wednesday-agent@agentmail.to`, DKIM/SPF/DMARC pass (provenance tool). A new mail from `kreiser.org@me.com` = STOP and mail Wednesday.
- **The project MUSTs this change type touches.** Drafter: at develop `1e7f90e26137`, SKILL blob `b59b74a592e9` (659 lines) and repo `CLAUDE.md` blob `ff426ce6097d` (498 lines), the same blobs F 6th's drafter cited; project `CLAUDE.md` on disk, sha256/16 `812663207c976c69`.
  1. SKILL §1 (`:13-29`): a written plan before any edit, grounded in the ticket, its parent (KS-772) and the code. **`:30-36`: on platform-k base code, Kamil's comments take precedence.**
  2. SKILL §4 (`:360-421`): BOTH platform-k HTML docs in the SAME commit as any test change; timings measured with host and date.
  3. SKILL §5b (`:444-452`): every fix red on the broken code and green after, numbers quoted.
  4. SKILL §5d (`:507-516`): WHY + ticket + prior behaviour on every changed line; the ticket URL in the PR.
  5. SKILL §5e (`:518-538`): no branches, merges, MD files or Linear tickets unless instructed. This brief instructs ONE branch and ONE PR, and nothing else.
  6. SKILL §5f (`:540-552`): a runtime change is not Done on offline green. Write `live sweep owed` in the body; the ticket does NOT move.
  7. Repo `CLAUDE.md:167-175`: no cross-organisation GitHub references. `:255-256`: the Linear URL in every PR. `:285-286`: the Test Evidence block. `:296`: never push to `develop`.
  8. Project `CLAUDE.md:233-241`: the author merges once TESTED on Wednesday's GO naming the head; **not in this round.**

## TOOLS (copy from the WRAPPED Seat G 5th's raise kit; G 5th's own lock was `.push-lock-g1`)
**Copy** from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-08_seatG-5th/raise/` into your record folder, iterating an ARRAY. Skip `__pycache__`, the `reseat_*` history, `.pre-*` and G 5th's push records. Hash each into `_COPY_HASHES_k1.txt` and `cmp` it. Also copy `provenance_ra20.py` from `…/2026-10-08_seatR-20th/tools/`. **Never run a tool from another seat's folder.** Expected (drafter `shasum -a 256 | cut -c1-16` + `wc -l`, 22:4xZ; a different hash is a STOP and a mail):

| G 5th tool | sha256/16 | lines | yours |
|---|---|---|---|
| `lockg1.sh` | `2a539bce0edd856c` | 581 | `lockk1.sh`; LOCK name gate stays `.push-lock-g1` (Q-LOCK-K); `LOCK_SEAT='Secuura/Blockchain-K k1'` |
| `pushg1.sh` | `825693eb5fbf76c7` | 247 | `pushk1.sh` (re-seat the push tool's co-tenant set too: STANDING_LINES `:418`) |
| `commitg1.sh` | `bd59289cc0f53a6f` | 210 | `commitk1.sh` + the `:68` fix (ITEM 4) |
| `inbox_matchg1.py` | `1361f23c2cd1f034` | 432 | `inbox_matchk1.py`, RE-KEYED |
| `inbox_watchg1.sh` | `b69109d9b223882e` | 162 | `inbox_watchk1.sh`, `WATCHK1_*` |
| `namecheckg1.py` | `f3cbad9a834f2192` | 1199 | `namecheckk1.py`: G 5th handover item 2 (the hard-coded `seat g 5th`/`seatg5` literal; fixtures re-pinned WHOLE) |
| `pathgateg1.py` | `28ad93e128e36dba` | 159 | `pathgatek1.py` |
| `keyscang1.py` | `e85a0c6e624087c9` | 56 | `keyscank1.py` |
| `gatelinesg1.py` | `b5e7923f605af9da` | 73 | `gatelinesk1.py` |
| `bannercheckg1.py` | `1ce35951d965279b` | 244 | `bannercheckk1.py` (`0 checked` is a FAIL, `:339`) |
| `rekey_checkg1.py` | `a1f28f4215db5515` | 932 | `rekey_checkk1.py` (in its own token map, `:333`) |
| `docblockra3.py` | `c4827645b53bce19` | 168 | unchanged |
| `raiseg1.py` / `raise_rest_g5.sh` | `3c9d92463eb92a45` / `d109febb06cd17d1` | 260 / 37 | `raisek1.py` / `raise_rest_k1.sh` |
| R 20th `provenance_ra20.py` | `d215ce0275a6e3f9` | 91 | `provenance_k1.py` |

- **G 5th's handover is your FIRST THREE THINGS** (`HANDOVER-seatG5-2026-10-08.md:8-62`, 174 lines, sha256/16 `0eb5baa656c4cf1b`; read them THERE, whole). It is addressed to G 6th; you are a different lane on the same kit, so apply it with the letter changed:
  1. **The matcher re-key.** Drafter's `ast` read: `MINE` `'g 5th'` `:102`; `OTHER_SEATS` `:212` 141/141 (present `f 6th`, `e 12th`, `g 6th`; ABSENT `r 21st`, `k 1st`, `j 1st`, `g 5th`); `MY_PANE` `'secuura/blockchain-g]'` `:261`.
     - For you: `MY_PANE` -> `secuura/blockchain-k]`.
     - ADD `g 5th`, `r 21st`, `r 22nd`, `f 7th`, `j 1st`, `j 2nd`, and FORWARD-ADD `k 2nd`, each with its `seat …` form. KEEP `g 6th`.
     - `MINE = "k 1st"`, double quotes kept.
     - Keep `(Seat G 9th)` in neither list.
     - Byte-span edit from the AST. Verify by `ast.literal_eval` and `tag()` from source truncated at `end_lineno` (importing RUNS the poll).
     - Drive the 2x2 on FULL-LENGTH real subjects: your brief reads FOR ME; real `(Seat F 6th)`, `(Seat R 21st)` and `(Seat G 5th)` subjects read FOREIGN; `(Seat K 9th)` on your tag reads UNKNOWN ADDRESSEE. Use subjects with no foreign ordinal in their prose.
  2. **`namecheck`'s hard-coded literal** (item 2): re-seat to `seat k 1st`/`seatk1`, and drive a quarantine-style ref before you trust any namespace verdict.
  3. **`commitg1.sh:68`'s untracked-blind count** (item 3): fix it (ITEM 4). Also `mkdir -p "$REC/boot"` before the first take.
- **Re-key: THE GENERIC CLAUSE BINDS AND COMES FIRST.** Re-key EVERY lane-bearing declaration: env names, LOCK_SEAT, ref namespaces, worktree prefixes, log/artefact names, fixtures, banners. Build the token list from EVERY generation the file names (STANDING_LINES `:293`, `:428`), never only `g5`. Sweep live 12+-hex constants outside comments (`:422`); `int(`/`\d\d` generation predicates (`:395`); env-var set-equals-read (`:305`). Print `N checked` per tool.
- **Namespace forms of your token:** `k1`, `-k1-`, `s-k1-`, `seatk1`, `refs/seatk1/`, `Seat K 1st`, `k 1st` (STANDING_LINES `:311`). `k` is not a hex digit, so `k1` cannot occur inside a sha; still state counts raw / bounded (`:368`).
- **Lock arms** run from a COPY of the tool in a scratch dir (STANDING_LINES `:419`). Controls go in a private `mktemp -d`, never in the shared `worktrees/` (`:446`). The unattributed-lock catch-all is CODE: a planted unknown lock is refused, and the tool prints how many dirs it CHECKED (`:402`).

## MAIL FORMATS (to `wednesday-agent@agentmail.to`; prefix `[Secuura/Blockchain-K -> Wednesday] `; every subject names `(Seat K 1st)`)
- `QUESTION: plan confirmation (Seat K 1st)` · `QUESTION: ctx read (Seat K 1st)` · `QUESTION: ctx read, may I push (Seat K 1st)` · `QUESTION: <topic> (Seat K 1st)`. One question per mail; body Context / Question / Meanwhile / Needed-by. Launcher preflight warnings go VERBATIM in the plan mail.
- `STATUS: raise base (Seat K 1st)` · `STATUS: red-first (Seat K 1st)` (cells x base/head, executed counts, tamper matrix) · `STATUS: pushed feature/ks-1402-originate-resolves-holder-email-itself-k1-1, raised #<n> (Seat K 1st)`.
- ONE `READY FOR QA (Seat K 1st): #<n> (KS-1402) -> gate<NN>`.
- `WRAP (Seat K 1st): …`. Include:
  - `MODEL:`, plus an honest note of anything that felt beyond the model;
  - 0 watchers and 0 locks of yours, from a ps file;
  - EVERY REF WRITE (worktree add, push, and its tracking-ref side effect, STANDING_LINES `:434`);
  - RESUME, naming the branch IN FULL with its head;
  - UNMERGED / UNMEASURED / UNFILED;
  - `df -m` before/after;
  - drive hygiene (an open PR keeps its worktree);
  - the tool hashes K 2nd inherits;
  - the handover `5_Project_History/HANDOVER-seatK1-<date>.md`, opening "FOR K 2nd, THE FIRST THREE THINGS";
  - the history entry at the TOP of `history.md`, insert-only proved;
  - "this seat = 1 Claude launch, clause: raise (carrying 0 Spark tasks)".

## QUESTIONS (OPEN; Wednesday rules at the ANSWER; each HOLDS only what it names)
- **Q-MECH (HOLDS ITEM 1 onward). Kam's words: "its own service credential". This brief: a DB lookup under originate's own database role, with no token.**
  - **Recommend:** the DB lookup: request db, bound tenant predicate, auth's normalisation. Reasons in THE MECHANISM above: no service bearer exists; a tenant-less token fails open at `users.ts:306`; the precedent is in the same handler.
  - **For Wednesday on the Kam question:** every constraint Kam wrote is kept (no scope change, no re-mint, resolution K-side, the cross-tenant guard proved by the gate). The deviation is only in HOW. The literal alternative would ADD a credential. The drafter's recommendation: a non-blocking one-line FYI to Kam in the next batch, not a blocking card. Escalate instead if Wednesday reads "service credential" as Kam choosing a token.
  - **Sub-choice:** a direct `users` SELECT (the id-path's shape, two enforcement layers) vs auth's SECURITY DEFINER `auth_find_user_by_email_hash` + an app-layer compare (exact parity with auth, including legacy). **Recommend the direct SELECT.**
  - **Default:** none. HOLD until ruled.
- **Q-SCOPE (binds ITEM 2).**
  - **Recommend:** ONE resolution path for ALL callers. A connector-only branch keeps two resolvers that can drift. Cost: the KS 739 cells change (Q-739).
  - **Default:** as recommended.
- **Q-NULLT (binds C7).**
  - **Recommend:** keep `tenant_id IS NULL` tolerance for parity with today's auth path (`users.ts:306`) and the id path (`:1803`), pinned by C7 either way.
  - **Default:** as recommended.
- **Q-LEGACY (binds ITEM 2 and NOT COVERED).**
  - **Recommend:** measure the count of legacy-plaintext users on a local stack only if one is already up (never build one for this). Otherwise DECLARE the gap in NOT COVERED: a legacy-only user resolves at base via auth and 404s at head.
  - **Default:** declare.
- **Q-KEY (binds C9).** `lookupHash` throws when originate has no registered key (`index.ts:369-376` registers only under `PII_ENCRYPTION_KEY`).
  - **Recommend:** catch it and answer 502 `BAD_GATEWAY`, "could not resolve recipient", in parity with today's unreachable arm (`:1735-1749`). Log it, pin it with C9, and never let it become an unlabelled 500.
  - **Default:** as recommended.
- **Q-739 (binds ITEM 1).**
  - **Recommend:** RETIRE the cells that pin auth's 401/403/5xx passthrough on THIS route, with a WHY comment per cell. RE-POINT the malformed-email 400 cell. Nothing is deleted: a retired cell's file change is shown in the diff. List all 17 with a disposition each.
  - **Default:** as recommended.
- **Q-HELPER (binds ITEM 2).**
  - **Recommend:** a small exported helper in a NEW originate file (e.g. `services/originate/src/services/holderResolution.ts`), so the tenant scoping is unit-testable. Or inline it if under ~25 lines. Declare it in the pathgate either way.
  - **Default:** inline.
- **Q-LANE-K (HOLDS the launch).**
  - **Recommend:** **K 1st**, token `k1`, pane `Secuura/Blockchain-K`: the lane the 10-06 brief named, never launched (0 `s-k*` worktrees, 0 `-k1-` refs). `k` is not a hex digit.
  - **Alternative:** run it as **G 6th** on `Secuura/Blockchain-G`. G 5th's handover applies verbatim, with fewer re-keys. **But the G lane still owns #1434** (KS-1171, OPEN at READY, worktree kept), and any gate77 fix round on it is G 6th's.
  - **Default:** K 1st.
- **Q-LOCK-K (HOLDS the first lock take).**
  - **Recommend:** adopt `.push-lock-g1` (holder seat `Secuura/Blockchain-K k1`). It is already a WAIT by path in both live seats' tools (F 6th `lockf3.sh:335`; R lineage `lockra1.sh:303`, which R 21st copies), and the G lane is not pushing.
  - A new `.push-lock-k1` would be rc 12 UNATTRIBUTED to both catch-alls until Wednesday re-wires them mid-round, a reshaping she declined for F 6th (Q-LOCK56-F6).
  - If a G seat launches, it co-tenants `g1`, attributed by holder `seat` (STANDING_LINES `:412`).
  - **Default:** `.push-lock-g1`.
- **Q-NUM (binds ITEM 3).**
  - **Recommend:** flow `44.` (highest seen `43.`, #1430; `32.`-`43.` allocated). Cheat `KS-1402` LAST.
  - **Default:** `44.`
- **Q-OBJ-K (HOLDS the worktree add).**
  - **Recommend:** if develop's objects are still absent from the shared store when you need them, mail and WAIT. R 21st does the one transfer for this store; one transfer per store, sequenced by Wednesday.
  - **Default:** as recommended.
- **Q-BRANCH-K / Q-SUBJ-K (bind the commit).**
  - **Recommend:** branch `feature/ks-1402-originate-resolves-holder-email-itself-k1-1` (59 characters); commit `fix(KS-1402): originate resolves a transfer-custody holder email itself` (71); PR title `KS 1402: originate resolves a transfer-custody holder email itself` (66), the #1431 shape.
  - **Default:** as recommended.

## UNMEASURED (by the drafter; you measure or say so)
- Every cell, tamper, suite, tsc and `check:openapi` result; the push preflight; Actions.
- Whether develop moves (R 21st's #1427 squash) before your RAISE_BASE, and what the doc tails read then.
- Whether RLS admits a `tenant_id IS NULL` user row under the tenant GUC. The legacy-plaintext row count. Whether any deployment runs originate without `PII_ENCRYPTION_KEY` while auth has the HMAC key.
- GitHub API facts (open-PR list beyond the refs, `mergeable`, Actions): the drafter holds no Secuura GitHub identity. **The "0 of 8 heads" overlap covers the heads named, not every open PR.** Your first API read lists open PRs paginated, then each one's files.
- Your pane id, launcher, sole-session status, ctx. The S↔K live behaviour after a deploy (not this round).

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **Card `secuura-ks1402-s-key-cannot-carry-users-read-1006` = a**, `ruled_ts=2026-10-06T09:58:21.119827+11:00` (verbatim in THE MECHANISM). Option b (add `users:read` + re-mint) was NOT taken; it is the rotate-live-client-keys signature class.
- Earlier: card `secuura-ks1402-lookup-refuses-connector-tokens` = a (2026-10-02T09:59), executed as #1374. That half-fix moved S from 401 to 403.
- **The ruling comment promised to Stuart is NOT on the ticket** (the newest comment is Stuart's `7740c258`, 2026-10-06T06:01Z). **It is Wednesday's to post, not this seat's.**
- Standing: Kam's 2026-10-04 week instruction; drive hygiene 2026-10-05 12:13:55; the 2026-09-11 TESTED merge grant (NOT exercised: this brief ends at READY).

- **The whole ruled-but-undelivered list for `secuura-` at send** (`decision_queue.sh list ruled --undelivered secuura-`, 68 lines, generated by Wednesday at send; pasted by hand because the send gate does not map lane `-K`). Only the two KS-1402 cards above are yours; the rest are context, not work:
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

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE (restate, do not ask)
- `comments(first:50)` sorted client-side; the `$TMUX_PANE` pin; `ast.literal_eval` + truncated-source `tag()` for side-effecting modules; the exec bit checked on disk after any apply, restored per named path only, never `checkout-index -a -f` (F lane rulings 2, 4, 5, 6; 2026-10-08).
- Declining `POST /api/seen` is RIGHT (R 20th's ANSWER_plan). F-02: verify the push identity with an SSH auth probe; never set `SECUURA_ALLOW_ONDISK_KEY` yourself.
- `run-migrations.sh` exits 3 on a failed migration (STANDING_LINES `:109-114` correction). Not yours; never write "exits 0".
- Doc blocks are numbered by ticket and nobody renumbers.

PROVENANCE:
- blast radius: I have not established the blast radius — establish it before acting. ITEM 0(f) is where you do it (every caller of auth's `/api/users/lookup` from originate, read from a FILE census with a must-hit and a nonsense control; the 17 KS 739 cells, each RETIRED or RE-POINTED) | the drafter's census named ONE caller, unverified by Wednesday | read 2026-10-09
- KS-1402 In Progress (started) · assignee board account `kamil.kreiser@secuura.ai` · creator Peter · High · parent KS-772 (Todo) · project "Integrate S with K" · 0 children · 1 attachment #1374 `merged` 2026-10-04T14:30:26Z · 5 comments sorted client-side: `d053e35b` 10-02 Stuart, `d4e7b940` 10-04 board account, `d62d2bd9` 10-05T02:28:48Z Stuart, `d280f168` 10-05T09:53:44Z Stuart, `7740c258` 10-06T06:01:29Z Stuart (newest) · updated 2026-10-08T07:21:19Z | Linear GraphQL by id, `comments(first:50)` sorted client-side; control KS-99999 in its own query = "Entity not found: Issue" | read 2026-10-09 (UTC 2026-10-08T22:40:09Z)
- KS-1406 Backlog · board account · creator board account · Medium · 0 comments · 0 relations | same instrument and control | read 2026-10-09 (UTC 22:40:09Z)
- KS-772 Todo · board account · 17 children (10 unstarted, 4 started, 3 backlog, 0 completed), incl. KS-1402 | Linear GraphQL by id | read 2026-10-09 (UTC 22:4xZ)
- Card `…-1006`: `choice='a' ruled_ts=2026-10-06T09:58:21.119827+11:00`, options a/b as quoted | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-ks1402-s-key-cannot-carry-users-read-1006` rc 0 | read 2026-10-09
- develop `1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0`; heads #1383 `32e8459bc0f5`, #1427 `2b6da5f561b0`, #1429 `1271d9597c43`, #1430 `d9928f4a8a4d`, #1431 `d715e5dfbbf2`, #1432 `c4e6f50654fa`, #1433 `934e20a599b1`, #1434 `d7ba337a8ef6`; `feature/ks-1402-lookup-accepts-connector-token-b55-1` `aa16f3256dbf` (the only ks-1402 ref); `-k1-` 0, `-ra13-` 2; 2,155 lines | `env -u GIT_SSH_COMMAND git -c core.sshCommand=<checkout's> ls-remote git@github.com:Secuura/Distributed_Secuura.git` rc 0 | read 2026-10-09 (UTC 2026-10-08T22:38:26Z)
- Call site: `documents.ts` blob `343eacec7fe85de4a7a9e66b1aef24dbcb77b750` (3,125 lines): `:1586`, `:1599`, `:1657-1663`, `:1664-1750` (`:1666`, `:1669-1671`, `:1693`, `:1738`, `:1744`), `:1759`, `:1799`, `:1803`; diff `22b268143a63..1e7f90e26137` on documents.ts + auth users.ts = +15/-3 across `1e7f90e26` / `f42161da3` / `3f9ff4e1e` | `git show`/`ls-tree`/`grep -n`/`diff --stat`/`log` in the drafter's `clone --shared --no-checkout` (`…/scratchpad/brief_hk1402/clone`, origin = GitHub URL, develop fetched by sha) | read 2026-10-09 (UTC 22:4xZ)
- auth `users.ts` blob `da7341a55f31` (`:180`, `:223`, `:284`, `:297`, `:306`); `platform.ts` blob `037068b67f13` (`:477-489`); `provenance.ts` blob `483aa9eb331d` (`:35`, `:101-114`); `userRepo.ts` `:577`, `:582`, `:591`; `039_rls_fail_closed.sql:185`, `:191`; `encryptedField.ts:592-598`, `:633`; originate `index.ts:369-376`; `docker-compose.yml:581`, `PII_LOOKUP_HMAC_KEY` at `:601` among 10 services | the same clone, `git show … | sed -n` / `grep -n` | read 2026-10-09
- Service-credential census: 5 lines over non-test `services/*/src` + `packages/*/src` (demo-service `DEMO_SERVICE_KEY` x4, m365 prose x1), 0 in originate and shared; `lookupHash` in originate `provenance.ts` = 4 (must-hit); nonsense token rc 1 | `git grep -n -i -E` at develop, output to `grep_svccred.txt` | read 2026-10-09
- Tests: `ks697-…` blob `56bbd366536c` 306 lines; `ks739-…` blob `85bf4ff3d910` 383 lines, 17 `it(`/`test(` cells; originate `jest` (`package.json:10`); root `check:openapi` `:42`, `generate-openapi` `:48` | `ls-tree`, `wc -l`, `grep -c -E` | read 2026-10-09
- Spec: `originate.openapi.ts` `:1635`, `:1746`, `:1753`, `:1764`; `secuura-api.yaml` `:6915`, `:28714`, `:28721`, `:28749` | `git grep -n -i` at develop | read 2026-10-09
- Overlap: K's files in 0 of 8 heads; `secuura-api.yaml` in #1429 only; every head touches 2 doc paths | `git diff --name-only $(merge-base develop H) H` | read 2026-10-09
- Flow numbers (newline-tolerant reader, planted `<h2>\n 99.` HIT by the new reader, MISSED by the same-line one): develop max `39`; across 130 `refs/pull/*/head` #1300-#1434 the max is `43` (#1430); `44` absent everywhere; cheat at develop: 20 `<h2>`, tail `…KS-591, KS-1164, KS-593`; `KS-1402` already in the cheat 4x and the flow 6x (#1374) | `git show <sha>:"Projects Documents/…" | python3 -I h2nums.py` | read 2026-10-09
- Floor `%0 wednesday`, `%1 fleet-monitor`, `%2 Secuura/Blockchain-F`, `%3 Secuura/Blockchain-R`; 0 `.push-lock*` at 22:43:27Z (control 1); WAIT on `.push-lock-g1` in F 6th `raise/lockf3.sh:335` and R 20th `tools/lockra1.sh:303` | `tmux list-panes -a`; `find -maxdepth 1`; `grep -n` | read 2026-10-09
- G 5th kit hashes (TOOLS); handover 174 lines, 14,496 B, `0eb5baa656c4cf1b`; matcher by `ast` as quoted | `shasum -a 256 | cut -c1-16`, `wc -l`, `python3 -I` `ast.literal_eval` | read 2026-10-09
- Project MUSTs: SKILL blob `b59b74a592e9` (659 lines; §1 `:13`, authority `:30`, §4 `:360`, §5b `:444`, §5d `:507`, §5e `:518`, §5f `:540`); repo `CLAUDE.md` blob `ff426ce6097d` (498 lines; `:167`, `:255`, `:285`, `:296`); project `CLAUDE.md` 306 lines `812663207c976c69` (`:185-194`, `:233-241`) | `git ls-tree` + `git show` at develop; `sed -n`; `shasum` | read 2026-10-09
- Superseded brief `2026-10-06_seatK1402_build.md` (218 lines; develop `3f9ff4e1e1b9`; partition B 65th / E 6th; doc `33.`; ITEM 1 = a seat-posted ticket comment) | Read whole | read 2026-10-09
- REPORT `0_Brain/reference/2026-10-09_stuart-list/REPORT.md` (141 lines; KS-1402 disposition A, mechanism flag) | Read whole | read 2026-10-09
- Model line | top block of `0_Brain/learnings/2026-10-09_spark-ornith-sonnet-only-until-monday.md` | read 2026-10-09

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-09 14:09
