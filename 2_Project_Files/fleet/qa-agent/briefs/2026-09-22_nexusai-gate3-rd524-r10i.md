# QA Agent Invocation Brief — Datasec/NexusAI, BATCHED GATE 3: RD-524 (+RD-404 +RD-441) TIER 1, and RD-516's R10i split + repair THROUGH-CODE

**Written by Tuesday 2026-09-22 (drafted 00:44-00:55 AEST).** Commissioned on NexusAI-F's (S77F) READY FOR QA for RD-524 at
`f422178` (mail 14:42:45Z) and on the RD-516 R10i split `bef8946` + repair `91861ae` (S77F's STATUS 13:55:44Z and
QUESTION 14:27:32Z; Wednesday's ANSWER 14:28:57Z: "step 3 proceeds on 91861ae once step 2 is GREEN; gate 3 reads it after").

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-22 00:53
Self-check note: read whole by Tuesday; the latch question corrected by the drafter to match RD-612 (a restart clears the alarm today, pre-existing); the B range is pinned at 91861ae regardless of the moving head; C-126/C-127 delivered, no Kam ruling open.

## Charter
Read `fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not build this and you
owe it nothing. **Everything below that reports what the builder says is a CLAIM.**

**ONE batched gate, TWO targets, ONE session** — Kam's standing rule of 2026-09-18: batch gates, never pay for the same
floor twice. The targets are disjoint in files (A touches no file B touches), but both will meet the server entry point
through the merge queue (§6). **Give a SEPARATE verdict for each: A GO / NO-GO, B GO / NO-GO.**
- **A is TIER 1 in full**: data-loss detection, a first-boot rule, a NEW authenticated status route, a client banner.
- **B is THROUGH-CODE**: a test-only change (two test files, no product file). RD-516 itself was gated (gate 1) and is
  NOT re-gated; you read the split and the repair and answer §4's questions. Do not re-open RD-516's product.

## RULED BY KAM, NOT YET IN AN ARTEFACT
none open — C-126 and C-127 delivered.

## PRIOR ROUND
PRIOR ROUND: none for RD-524 / RD-404 / RD-441 — round 1. No QA report naming RD-524 exists under
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/` (searched at commission). S59's
unmerged branch `rd-404-441-sentinel-banner-s59` (`ca8d364..feac318`) was never gated.
For B, gate 1's report `…/reports/2026-09-21-rd516-fixround-rd604-batch/report.md` is context (its F-5 is the R7 comment
fix that rides `bef8946`); gate 2's report `…/reports/2026-09-21-gate2-rd495-rd525-rd575/report.md` is context for §6.
Neither is a carry-forward.

## 1. Targets — verified at commission from the object store
### TARGET A — RD-524 + RD-404 + RD-441
- **Branch `rd-524-404-441-s77f` @ `f42217844bde4fd07952a3d1ec7f165d0957790d`** (short `f422178`), at origin.
- **Base main `bdca588eced9c6a7ee6085b19e48765be3c8c07b`** (the RD-604 merge). `merge-base(bdca588, f422178) = bdca588`.
- **Chain `bdca588..f422178`, exactly THREE commits:**
  - `faa9cbe445d0cf932c48b784550a4c5383bd4ceb` — WIP carry: 7 files (the two new test files, the two new helpers, the
    store module `backend/jsonStorage.js`, the server entry point, `static/js/index.js`);
  - `07b9ce6854d036d541d05ba4a3ba97c17e8159c4` — fixture W fix in the rd441 test + `BACKLOG.md` (5 entries);
  - `f42217844bde4fd07952a3d1ec7f165d0957790d` — `scripts/verify-expected-counts.json` → **tests 3838 / suites 218** (main: 3797 / 216).
  - (The READY mail's §1 says "Four commits" and then lists these three; the object store has three. Minor record error.)
- **Files, exactly NINE:** `BACKLOG.md` (M), `__tests__/helpers/persistent-temp-root.js` (A),
  `__tests__/helpers/rd441-banner-render.js` (A), `__tests__/rd404-sentinel-first-boot-vs-wipe.test.js` (A),
  `__tests__/rd441-persistence-alarm-reaches-dashboard.test.js` (A), `backend/jsonStorage.js` (M), the server entry point (M),
  `scripts/verify-expected-counts.json` (M), `static/js/index.js` (M). 1360 insertions, 59 deletions.
- `backend/services/authEnforcement.js` is **byte-unchanged** (blob `ca764a4` at main and at A).
- **Prior-work claim (C-49), measured at commission:** vs S59's `feac318`, both helpers are **byte-identical**; the rd404
  test is feac318's **plus 30 inserted lines, 0 deleted** (B7, F4); the rd441 test is feac318's **plus 8 inserted lines,
  0 deleted** (fixture W's two Entra IDs). Confirm no S59 assertion was weakened.

### TARGET B — RD-516 R10i split + repair (through-code)
- **Branch `rd-516-ai-test-ssrf-s73`. Range `b9666342f50646fbe44aefcdeeaa732dea10dccb..91861aef2302ef8c8800a28a8977e490c021679a`**,
  exactly TWO single-parent commits:
  - `bef8946d621a41b1a70ee28bb0a12e942be4abda` — the split: the built half stays in `__tests__/rd516-ai-test-ssrf.test.js`
    as a normal cell; the scheme/port half parked verbatim in `__tests__/helpers/rd583-parked-NOT-RUN/rd516-r10i-scheme-port.test.js`;
    plus the F-5 comment correction on R7 (RD-585 comment) in the same test file;
  - `91861aef2302ef8c8800a28a8977e490c021679a` — the repair: R10i reads `checkEndpointName` (network-free name layer,
    `aiEndpointPolicy.js:212`) instead of the async `assertAllowedAiEndpoint` (`:276`), whose `.ok` was undefined on the
    Promise and whose DNS branch refused all nine names.
- **Files, exactly TWO** (both test files); no `backend/`, `static/` or `scripts/` change; counts file unchanged at
  3797 / 216 across the range (the step-2 merge adds RD-423's suite and regenerates it — not your range).
- 🔴 **THE RANGE END IS PINNED AT `91861ae`, NOT AT THE BRANCH HEAD.** At commission origin's `rd-516-ai-test-ssrf-s73` read
  `91861ae` (00:44 and 00:48 AEST), but NexusAI-F is mid step 2 (forward merge of main + verify) and step 3 (merge to main).
  By launch the head may be a forward-merge commit above `91861ae`, or RD-516 may already be MERGED into main. **Either way
  you read `bef8946` and `91861ae` only.** State which of the three you found at each head reading.

### All targets
- **No worktree is pinned. Build your own INSIDE YOUR OWN PROJECT (Testing Agent MAIN), from the object store at each
  sha:** `git -C <repo> archive <sha> | tar -x -C <a fresh mktemp -d under your project>`. Archive is read-only on the
  repo. **Never run `git worktree add`, `checkout`, `fetch`, `stash`, `clean` or a commit against the NexusAI repo.**
  Its working checkout is elsewhere and dirty (34 porcelain lines at commission): pin to the sha, never `HEAD`.
- **`git merge-tree --write-tree` writes objects.** Keep the NexusAI repo untouched by pointing it at your own object
  directory: `GIT_OBJECT_DIRECTORY=<your mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree <x> <y>`.
  The same two variables let you `git archive <tree-id>` a merge-tree RESULT into your own directory, if you want to run
  cells on a merged tree (§3 Q6).
- The repo is `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files`.
- **NOT on main. Nothing merges on your word or the builder's.**

## 2. Why this tier, and who is waiting
- **TIER 1 for A.** It decides when the product raises (and does not raise) its data-loss alarm, adds a route every
  signed-in user can read, and changes what the dashboard renders.
- **THROUGH-CODE for B.** Test-only; the question is whether the cell now proves what it names.
- 🔴 **The merge queue.** Main is `bdca588`. Queued, in order: **RD-516 → RD-495 → RD-525** (all GO'd; being merged by
  NexusAI-F, S77F, pane `%34`, claude pid `94093` — re-read at launch) **→ RD-575** (gate 4, after its forward merge)
  **→ RD-524** (this gate), forward-merged onto whatever main is then. Each is forward-merged and verified GREEN before it
  lands (C-68 / C-89); each merge is Tuesday's GO under C-127. **A GO on A is a GO at `f422178` only (C-68)**: the
  forward merge over RD-516, RD-495, RD-525 and RD-575 changes the server entry point and the customer-data list that A's
  evidence rule reads, so it can expire cells. **Say which, in §6's terms.**

## 3. TARGET A — the wipe alarm is raised exactly when it should be, and every signed-in user sees it (TIER 1)
Claimed (READY mail; `session-tools/s77f/mail-07-ready-rd524.txt`):
- **KEPT from S59 `b587646`:** `collectPriorStateEvidence` (store module `:1042`), taken on the constructor's FIRST line
  (`:1081`); seven sentinel states — `intact`, `intact-legacy`, `first-boot`, `ephemeral`, `unverified` (wiped false),
  `missing-with-evidence`, `sentinel-invalid` (wiped TRUE, latched for the process lifetime); read-back-verified sentinel
  write; `recheckPersistenceSentinel` (only `unverified` re-checks, 30 s throttle); `persistenceStatus()` /
  `persistenceHealth()`.
- **Server entry point:** persistence subsystem verdict; `sentinelState` on the two admin surfaces (`:1688`, `:18055`);
  **`GET /api/status/persistence` at `:18506`, below `app.use(requireAuth)` at `:2627`**, returning
  `{volumeWiped, isPersistent}` only, `Cache-Control: no-store`; 503 `PERSISTENCE_STATUS_UNAVAILABLE` before storage
  exists, 500 on a throw. `isAlwaysPublicPath` (`:2129`) matches `path === p || path.startsWith(p)`; the builder says no
  public entry is a prefix of the route.
- **`static/js/index.js`:** `SERVICE_BANNER_SOURCES` (`:1144`, `persistence: '/api/status/persistence'`),
  `fetchPersistenceStatus` (`:1183`), `showPersistenceAlarm` (`:1197`), `testAPIConnection()` called again from
  `loadFromDatabase()` (`:1276`).
- **IMPROVED:** `PRIOR_STATE_MARKER_NAMES` (`:1000`) = `.auth-enforcement-stamp.json` (RD-554) and
  `.entra-group-unproven.json` (RD-452/RD-535) — cells **B7** (either alone raises the alarm and is named) and **F4** (the
  list equals the basenames `enforcementStampPath()` and `groupRestoreMarkerPath()` build).
- **DROPPED:** `a2cf7f2`'s control-character regex hunk (main fixed it under RD-429).

**Answer each of these with a measurement:**
1. **The first-boot rule, both directions, every evidence source ALONE.**
   - **A genuine fresh volume raises NO alarm**: empty persistent directory (NOT under `/tmp/` — that path is `ephemeral`
     by design, `:1489`), boot, read the state (`first-boot`), `volumeWiped: false` on the route, no banner. Also an
     ABSENT directory (`ENOENT` returns no evidence, `:1049`).
   - **A volume wiped of everything except ONE piece of prior evidence raises it** (`missing-with-evidence`, wiped true,
     the evidence named in the log). **Enumerate every source from the code, not from this list**, and plant each ALONE on
     an otherwise empty volume with no sentinel. From `:1042-1074` at commission:
     (a) each name in `PRIOR_STATE_STORE_NAMES` (`:976`: nine explicit names + `...CUSTOMER_DATA_FILES`, deduplicated) —
     one representative is not enough: **every name**; (b) a recovery copy of each (backup, previous backup, emergency,
     legacy emergency — from `recoveryLocations.js`; say where each lives and whether a copy OUTSIDE the data directory
     counts); (c) each use marker; (d) a `.machine-id` this process did not write; (e) an interrupted write for a store,
     for `.machine-id` and for the sentinel (`<name>.tmp.*`); (f) an unlistable data directory (say whether you could
     produce one honestly as a non-root user, and what state results).
   - **Controls:** a file NOT on any list (for example `notes.txt`) alone must NOT raise it — if it does, say why; and a
     present, valid sentinel beside any evidence must read `intact`.
   - **The legitimate-erasure path:** run a customer data erasure (the product's own route), then restart. The sentinel is
     INFRASTRUCTURE (`customerDataFiles.js:71`, never purged), so the expected state is `intact`, not a wipe. **A false
     wipe alarm after a legitimate erasure is a finding.** Note RD-610 (S77F's READ, not measured): erasure leaves the
     RD-554 stamp behind — say whether that changes anything here.
2. **The route leaks nothing beyond the two booleans, and is unreachable anonymously.**
   - Body keys EXACTLY `volumeWiped`, `isPersistent`, both booleans, in each sentinel state you can produce; headers
     (`Cache-Control: no-store`); the 503 and 500 bodies (what they carry — any path, state name or evidence text is a finding).
   - **Enforced + configured state:** anonymous → the refusal code and body; viewer → 200; admin → 200 (the RD-523 SIGNED
     pattern the cells use).
   - **Path-variant probes against the gate**: trailing slash, upper case (`/API/Status/Persistence` — Express routing is
     case-insensitive, `isAlwaysPublicPath` is not), `//api/status/persistence`, percent-encoded segments, a query string.
     Any variant that reaches the handler anonymously in the enforced state is a Major.
   - **Setup-open states — SAY WHAT IT ANSWERS THERE:** first-run (setup not complete), and enforced-but-sign-in-UNCONFIGURED
     (the fixture-W situation: `adminGateRefuses` answers "still in setup" while tenant/client are unset,
     `authEnforcement.js:592/:646`). The route comment says "open in first-run mode". State whether an anonymous caller
     gets the two booleans there, and judge whether that is acceptable (two booleans, C-01 open window) — **report, do
     not decide policy.** Also: the auth state unreadable → 503 as the comment says?
3. **The banner renders for signed-in users on a wiped volume.** Drive a REAL browser if you can on a local run (a
   headless Chromium via Playwright or similar inside your own project): sign in as a viewer on a volume booted into
   `missing-with-evidence`, screenshot the dashboard, and name the banner text. Then the negative: a fresh volume shows no
   storage banner. If you cannot drive a browser, PROBE the served `index.js` (the three functions and the source URL as
   served) and the API answer, and **label it PROBED, not measured** — the builder's U1-U3/B1-B6 render the page in jsdom
   only and the builder says a pixel check is owed to this gate. Note RD-613 (banner only on the dashboard) and the
   loading-overlay blur the BACKLOG entry describes: report what you see, do not score RD-613.
4. **The latch.** Within one process: once `missing-with-evidence` or `sentinel-invalid` is set, show that NOTHING in the
   running process clears it — the wipe path's own sentinel re-creation, a health read, `recheckPersistenceSentinel`
   (called directly and via both routes), a settings write, an erasure. **Then restart on the same volume.**
   🔴 **Tuesday's question as first put was "the latched alarm cannot be cleared by a restart alone". The code and the
   builder's own BACKLOG say the opposite, and it is tracked:** RD-612 — *"The wipe alarm lasts one process lifetime; a
   restart clears it with nobody having acknowledged it"* (the wipe path re-creates the sentinel, so boot 3 reads
   `intact`), stated as pre-existing on the base. **Measure it** (boot 1 fresh → wipe → boot 2 alarm → boot 3), report the
   state and the banner at boot 3, and say whether RD-524 changes the pre-existing behaviour in either direction. A
   restart clearing the alarm is RD-612's, not a new defect of this change, **unless** you find it is new — then it is
   one. Give the fix-shape RD-612 would need in one line; findings-only.
5. **`sentinel-invalid`**: an HMAC-mismatched sentinel and a non-sentinel JSON (C3's unparseable case) both raise it.
   RD-611 (HMAC keyed by `resolveDataDir()`'s machine id): boot the server the product's way (DATA_DIR set) so you do not
   manufacture RD-611's mismatch; say which way you booted.
6. **RD-525's and RD-575's stores after their merge (neither is on main; READ ONLY acceptable, label it).**
   `PRIOR_STATE_STORE_NAMES` spreads `CUSTOMER_DATA_FILES` at module load. RD-525 (`792fda0`) grows that list 11 → 21 (four
   of the ten are already explicit names here); RD-575 (`bcb438d`, stacked on `792fda0`) adds `feedback-attachments`, a
   DIRECTORY. Say whether the evidence rule will see each new store after the merge — including whether
   `present.has('feedback-attachments')` counts a directory, what `recoveryCopiesFor` does for a directory name, and
   whether an empty `feedback-attachments/` left by a first boot's own writes could ever be seen by the constructor-first
   scan. Better than READ ONLY: archive the merge-tree RESULT of `f422178 × bcb438d` (your own object dir, §1 — it
   conflicts only in the counts file, which the rd404 cells do not read) and run the rd404 file on it; label that PROBED.
   The builder's claim: "F2 derives from CUSTOMER_DATA_FILES, so F2 covers them without edits" — check F2 does.
7. **The server-entry-point diff is only the persistence work.** Hunk-level read of `git diff bdca588 f422178 --` the
   server entry point (+36 −2 at commission, `--numstat`): name any hunk that is not the persistence subsystem, the two
   `sentinelState` lines, the new route, or a comment.

**Builder's red-proofs — RE-RUN THEM YOURSELF.** A kill you did not reproduce is the builder's.
- **R0** clean at `07b9ce6`: 41/41 (rd404 22 incl. B7 + F4, rd441 19). Re-run at `f422178` (test-identical to `07b9ce6`).
- **M1** — product reverted (the store module, the server entry point, `static/js/index.js` at `bdca588`; tests kept):
  **24 red, 17 green**, every red behavioural (A1-A4, S1, R2-R4, G1, U1, B4, B5, G2, C3, D1, D2, F1-F4). Confirm the count
  AND that no red is a harness error.
- **M2** — ONLY the use-marker loop removed from `collectPriorStateEvidence`: **exactly 1 red, B7**; F4 stays green.
- **Add your own mutants:** (i) drop ONE store name from the evidence set (not from `CUSTOMER_DATA_FILES`) — which cell
  reddens? if none, name the unguarded source; (ii) drop the `.machine-id` clause; (iii) drop the tmp-prefix clause;
  (iv) make the route return `persistenceHealth()` or the whole store state — which cell catches the leak?; (v) make the
  banner read `/api/health` again (G2 should); (vi) clear `persistenceWiped` in the wipe path's re-creation (the latch
  cell should redden). A source no cell guards is a finding, not a blocker by itself — say which.
- Evidence: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s77f/` — `expect-rd524.txt` (written
  first), `rd524-proof-hold.sh`, `rd524-proof-hold.log`, `rd524-R0.log`, `rd524-M1.log`, `rd524-M2.log`,
  `rd524-full-verify.log`, `mail-07-ready-rd524.txt`.
- **Builder's full verify:** 3838 / 3838, 218 suites, PASS; counts committed as `f422178`. **Run your own.**

## 4. TARGET B — the split is honest, the parked file is inert, and R10i now discriminates (THROUGH-CODE)
Claimed (`session-tools/s77f/mail-05-status.txt`, `mail-06-question.txt`; C-130 + addendum):
- In-suite R10i asserts: the four sourced suffixes allowed; `openai.azure.us`, `services.ai.azure.cn`, the two-label host
  `foo.bar.openai.azure.com` and userinfo refused. Only `'http not https': false` left it, verbatim, for the parked file.
- R10i reads `checkEndpointName(u).ok` (layers 0 and 1, no network). Every assertion VALUE unchanged; only the function.

**Answer each of these with a measurement:**
1. **The parked file is inert.** `jest --listTests` on a tree at `91861ae` (with the repo's own config, `package.json`
   `testPathIgnorePatterns` includes `/__tests__/helpers/`): the control `__tests__/rd516-ai-test-ssrf.test.js` IS listed
   and the parked file is NOT. Also run `npm run verify`'s jest invocation form (read `scripts/verify-suite.sh` for the
   arguments it passes) to show it does not re-include helpers.
2. **No skip remains in the COLLECTED suite.** Measured at commission: an anchored
   `^\s*(test|it|describe)\.skip\(` / `^\s*x(it|test|describe)\(` search over `__tests__/` excluding `__tests__/helpers/`
   finds **0 at `91861ae`**, with the control firing (**1 at `b966634`**, R10i; and 1 in the parked file, which carries its
   `test.skip` verbatim and is not collected). Reproduce it, and then run the whole rd516 file (no `-t`) and report
   skipped = 0. (A `-t R10i` run reports the other cells as "skipped" by filter — that is not a `test.skip`; say so if you
   use it.)
3. **R10i discriminates.** Through the lock, one hold:
   - **CLEAN**: green.
   - **M-a** — add `'openai.azure.us'` to `SOURCED_SUFFIXES`: red on key `'openai.azure.us NOT sourced'` ONLY.
   - **M-b** — the one-label rule removed (`!label.includes('.')` → `true` in `hostIsSourced`): red on `'two-label host'` ONLY.
   - **Your own:** M-c remove the userinfo refusal in `checkEndpointName` (red on `'userinfo'` only?); M-d remove one
     sourced suffix (red on that suffix's key only?). Report the full received-vs-expected object for each red.
   - The builder's own run 2 at `91861ae` (`rd516-split-hold.log`, 14:43Z) shows M-a and M-b red on the right keys — a
     kill you did not reproduce is the builder's. Its run 1 at `bef8946` reddened on the CLEAN run too (every key
     undefined) — that is why the repair exists; **confirm by running R10i at `bef8946` CLEAN: it must be red**, which
     proves the repair was needed and that the cell at `91861ae` is not the same dead cell.
4. **The built half asserts nothing the product does not do.** For each of the eight keys, name the line in
   `aiEndpointPolicy.js` (at `91861ae`) that produces the value, and note which LAYER refuses each refused key
   (userinfo is refused by layer 0 as `URL_UNPARSEABLE`, not by the host list). Say whether the cell's name ("… a
   two-label host and userinfo are refused") matches. `'http not https'` must be ABSENT from the in-suite cell and the name
   must not claim §3.3 whole.
5. **C-130 and its addendum match the commits.** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md`
   `:1385` (C-130) and `:1394` (addendum) at commission: check every factual claim there against `bef8946` / `91861ae`
   (file paths, what moved, "every assertion value unchanged", the parked header warning, the listTests shape). A claim
   that does not match the commits is a finding against the record.
6. **The F-5 comment edit changed no assertion.** `git diff b966634 91861ae --` the rd516 test file: the hunk at R7
   (`:769`) must be comment lines only. Prove it mechanically (for example, strip comments from both versions of that
   describe and compare), not by eye alone.
7. **Parked-file fidelity.** The parked describe is "verbatim apart from the require path" plus a header: diff it against
   the R10(i) describe at `b966634` and name every non-header difference.

## 5. (no third target)

## 6. Across targets — merges, counts, full verify
- **Quote `git merge-tree --write-tree` (with your own object directory, §1) and report conflicts for A `f422178` against:**
  - **RD-516 `91861aef2302ef8c8800a28a8977e490c021679a`** (and, if its head has moved, the new head too);
  - **RD-495 `179bf603cf563013ac9f89dbc7b1e216e8a9d385`**;
  - **RD-525 `792fda0b3dc1884b32f3e04877f18959fbaaae77`**;
  - **RD-575 `bcb438d1cabb9ef855a024ff93c59048034e6ce8`** (context; gate 4).
  All four touch the server entry point.
- 🔴 **Measured at commission (00:45 AEST), not claimed by anyone:** `f422178 × 91861ae` **clean (rc 0)**;
  `f422178 × 179bf60`, `× 792fda0`, `× bcb438d` **rc 1, CONFLICT in `scripts/verify-expected-counts.json` ONLY** — the
  server entry point auto-merges in all three. A counts-file conflict is expected (each branch regenerated it) and is
  resolved by regeneration, not by hand. **Re-measure at your heads.** If main has moved (RD-516/495/525 landed), ALSO
  merge-tree `f422178` against the new main and quote it.
- **Say what the auto-merged server entry point means for A under C-68:** the route and the persistence subsystem must
  survive the forward merge unchanged; name the cells that must be re-run on the forward-merged tree (at minimum every
  rd441 route cell and every rd404 cell that reads `CUSTOMER_DATA_FILES`).
- **Full verify of A** (`npm run verify -- --maxWorkers=2`, RD-561, through the lock): predicted **3838 / 218** green.
  **Account for every failure. A red, or a count that disagrees with the committed counts file, is a finding.**
- **B needs no full verify of its own** (test-only, one cell; the builder's step 2 verifies the merged tree). Run the whole
  rd516 file at `91861ae` and report its counts. If you choose to run a full verify of B anyway, say why.

## 7. Floor discipline — THE FOUR CLAUSES (current wording; supersedes gate 1's §7)
1. **Every jest run goes through `session-tools/nexusai-lock.sh`.** The lock is SHARED and contended: NexusAI-F
   (S77F, pane `%34`) is live on the floor and holds or queues for it for RD-516 step 2/3 and the queued merges.
2. **Hold the lock ONCE per multi-run measurement.**
3. **Record the foreign `backend/server.js` count beside every result.** Count it this way:
   - **`basename(argv[0]) == node` AND `backend/server.js` appears ANYWHERE in the remaining argv** — not only as the
     first argument, because the preload form is `node -r <helper> …`;
   - tell yours from foreign by **ANCESTRY**, and **"ours" means the server's ancestor chain CONTAINS YOUR OWN seat pid**
     (your claude pid, your jest pid, or your lock-holder pid). **A SHARED ancestor proves nothing:** the tmux server,
     launchd (pid 1) and any login shell sit above EVERY seat, so a test of "the chains intersect" classifies every fleet
     server as ours and reads foreign=0 while another seat's server is live (fourth correction, 2026-09-21, RD-606);
   - carry a **NEGATIVE control**: a pid you KNOW is foreign must classify foreign in the same run. NexusAI-F's claude is
     pid `94093` (its pane shell `94091`), read at commission — re-read it; a chain through it and not through yours must
     come out foreign, or the ours/foreign split is unproven. (NexusAI-D `%30` and NexusAI-E `%32` were NOT on the floor
     at commission; if either is back, carry it too.)
   - **NEVER** by `EADDRINUSE`, **never** by a grep of whole command lines (that over-reports, RD-591 c.37901), and
     **never** by raw `comm` (blind on macOS, RD-574 r2 R2-1).
4. **A zero is reportable only beside a control that fired in the same window.** Spawn one server the way the harness
   does, require the count to RISE, then reap it.

**Reap every server you start.** An orphan of yours is the next run's foreign seat. The browser drive in §3 Q3 starts a
server outside jest: it counts, it is yours by ancestry, and it is reaped before you release the lock.

## 8. Drivable surface — LOCAL RUN, **NOT THE DEMO** (RD-76). No demo pass happened for either target, and none must be recorded.

## 9. HELD
- No merge, no deploy, no registry, no Partner Center, no production, no money, no external comms.
- No real Azure, credential, vault, tenant or key. Entra IDs in fixtures are the all-zero test values.
- **Findings-only: do not commit, do not move any branch, do not file a ticket, do not write inside the NexusAI project.**

## 10. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate3-rd524-r10i/report.md`

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 3: RD-524 @ f422178 + RD-516 R10i split/repair (tier 1 / through-code)`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` — an absolute path, because the QA project has none.

Verdict format:
- **A: GO / NO-GO**, **B: GO / NO-GO**, stated separately.
- Then one paragraph on what the verdicts mean for the merge queue (RD-516 → RD-495 → RD-525 → RD-575 → RD-524), with the
  merge-tree results of §6 quoted: in particular whether A's GO survives its forward merge over the four, and which cells
  must be re-run on the merged tree.
- **Rule 2: what you did NOT test is first-class output** (a NOT TESTED section, not a footnote). Every action
  recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.
- Report the head of each target as three timestamped readings (start / mid / end), each with its branch name, and main's
  head the same way. For B, say at each reading whether the branch head is `91861ae`, a commit above it, or merged.

PROVENANCE:
- origin heads: main bdca588eced9…, rd-524-404-441-s77f f42217844bde…, rd-516-ai-test-ssrf-s73 91861aef2302…, rd-495 179bf603cf56…, rd-525 792fda0b3dc1…, rd-575 bcb438d1cabb…, rd-404-441-sentinel-banner-s59 feac3187b83f… | `git ls-remote origin main rd-524-404-441-s77f rd-516-ai-test-ssrf-s73 rd-495-csp-violations-hard-gate-s71 rd-525-export-erasure-coverage-s76e rd-404-441-sentinel-banner-s59 rd-575-purge-reaches-attachments-s76e` | read 2026-09-22 00:44:45 AEST; main/rd-524/rd-516 re-read unchanged 00:48:31
- A chain bdca588..f422178 = faa9cbe (parent bdca588) → 07b9ce6 → f422178; merge-base(bdca588, f422178) = bdca588 | `git log --format='%H %P | %s' bdca588..f422178`; `git merge-base` | read 2026-09-22 00:44
- A files (9) and per-commit files; 1360+/59− | `git diff --name-status bdca588 f422178`; `git diff-tree -r --name-status` per commit; `git diff --stat` | read 2026-09-22 00:44
- counts: bdca588 3797/216; f422178 3838/218; b966634 and 91861ae 3797/216 | `git show <c>:scripts/verify-expected-counts.json` | read 2026-09-22 00:45
- authEnforcement.js blob ca764a4 at bdca588 and f422178 | `git rev-parse <c>:backend/services/authEnforcement.js` | read 2026-09-22 00:44
- carried tests vs feac318: two helpers identical; rd404 +30/−0; rd441 +8/−0 (fixture W Entra IDs) | `git rev-parse` blobs; `git diff --shortstat feac318 f422178 -- <file>` | read 2026-09-22 00:47
- S59 range ca8d364..feac318 = b587646, 1639a1d, 4b96580, a2cf7f2, acfd8da, feac318; ca8d364 ancestor of feac318 | `git log ca8d364^..feac318`; `git merge-base --is-ancestor` | read 2026-09-22
- A code positions at f422178: requireAuth mount :2627; route :18506 (503/500 bodies, no-store); alwaysPublicPaths :2048, prefix match :2129; sentinelState :1688/:18055; persistenceHealth use :1672; store module PRIOR_STATE_STORE_NAMES :976, PRIOR_STATE_MARKER_NAMES :1000, collectPriorStateEvidence :1042 (ENOENT → none :1049; unlistable → evidence), constructor-first scan :1081, states :1466-1484 + setState lines 1559/1577/1580/1601/1614/1631/1635, latch comment, recheck :1658, persistenceStatus :1678; index.js :1144/:1183/:1197/:1276 | `git grep -n` / `git show f422178:<file> | sed -n` | read 2026-09-22 00:46-00:50
- sentinel and .machine-id are INFRASTRUCTURE (never purged) | `git show f422178:backend/customerDataFiles.js` (:71); dataErasure.js :45 | read 2026-09-22
- RD-611..RD-614 and RD-497 BACKLOG entries (RD-612: restart clears the alarm, pre-existing) | `git diff bdca588 f422178 -- BACKLOG.md` | read 2026-09-22 00:49
- customerDataFiles.js blobs: f422178 f16dfe2, 792fda0 1279a19, bcb438d a2e4caf | `git rev-parse <c>:backend/customerDataFiles.js` | read 2026-09-22
- B range b966634..91861ae = bef8946 (parent b966634) → 91861ae (parent bef8946); files: the rd516 test (M) + the parked file (A in bef8946, M in 91861ae); no backend/static/scripts change | `git rev-list --parents`; `git diff-tree`; `git diff --stat b966634 91861ae -- backend static scripts` (empty) | read 2026-09-22 00:45
- B diff content: R7 comment hunk at :769; R10i skip → test, 'http not https' removed from both objects, assertAllowedAiEndpoint → checkEndpointName | `git diff b966634 91861ae -- __tests__/rd516-ai-test-ssrf.test.js` | read 2026-09-22 00:46
- aiEndpointPolicy.js at 91861ae: SOURCED_SUFFIXES :129 (4), hostIsSourced :156 (one-label rule), checkEndpointName :212 (userinfo → URL_UNPARSEABLE), async assertAllowedAiEndpoint :276, exports :304 | `git show 91861ae:backend/services/aiEndpointPolicy.js` | read 2026-09-22 00:46
- skip search: anchored skip forms in collected __tests__ = 0 at 91861ae, 1 at b966634 (control), 1 in the parked file (control) | `git grep -nE '^[[:space:]]*(test|it|describe)\.skip\(|^[[:space:]]*x(it|test|describe)\(' <c> -- __tests__ ':(exclude)__tests__/helpers'` | read 2026-09-22 00:50 (an earlier `\b` form returned a FALSE ZERO under git grep -E — do not reuse it)
- testPathIgnorePatterns includes /__tests__/helpers/ | `git show 91861ae:package.json` | read 2026-09-22
- C-130 :1385, addendum :1394 (file mtime 2026-09-22 00:27) | `grep -n C-130 CLARIFICATIONS.md`; `sed -n 1383,1398p` | read 2026-09-22 00:46
- builder claims A (KEPT/IMPROVED/DROPPED, 24 red / B7, 3838/218, not-tested list) | AgentMail tuesday-agent@ READY 14:42:45Z; session-tools/s77f/mail-07-ready-rd524.txt; expect-rd524.txt | read 2026-09-22 00:45
- builder claims B (split, repair, run-1 dead-cell finding, run-2 M-a/M-b reds at 14:43Z, CLEAN run started 14:45:12Z) | AgentMail STATUS 13:55:44Z, QUESTION 14:27:32Z; Wednesday ANSWER 14:28:57Z; session-tools/s77f/expect-rd516-split.txt, rd516-split-hold.log (tail) | read 2026-09-22 00:46
- merge-tree at 00:45: f422178×91861ae rc0; f422178×179bf60, ×792fda0, ×bcb438d rc1, CONFLICT scripts/verify-expected-counts.json only, server.js auto-merged | `GIT_OBJECT_DIRECTORY=<scratch mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git merge-tree --write-tree --name-only <x> <y>` | read 2026-09-22 00:45
- floor: pane %34 shell 94091 → claude 94093 (NexusAI-F, etime 03:08); panes %30/%32 absent | `tmux list-panes -a`; `ps -o pid,ppid,etime -p 94093` | read 2026-09-22 00:46
- no prior QA report naming RD-524 | `grep -ril 'RD-524' Testing Agent MAIN/projects/nexusai/reports/` (0) | read 2026-09-22 00:47
- fourth ancestry correction | TUESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md §7 | read 2026-09-22
