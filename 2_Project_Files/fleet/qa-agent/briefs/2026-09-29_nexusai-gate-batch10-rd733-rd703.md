# QA Agent Invocation Brief — Datasec/NexusAI, ONE batched gate "batch 10": RD-733 (TIER 2, through-code + A REAL-BROWSER LEG) + RD-703 (TIER 2, through-code, test helper only) — two verdicts, one report (+ two OPTIONAL targets, RD-707 and RD-732, only if Tuesday stamps them)

**Drafted for Tuesday 2026-09-29 ~19:08–~19:45 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.**
Commissioned on Tuesday's batch 10 commission (2026-09-29 ~19:0x AEST) and two READY mails on disk, each read WHOLE:
- **A — RD-733** @ `ed4c1bfd5a195f163b8f76e84b467157f8b97813` (branch `rd-733-user-access-stale-entra-check-s86m`, ONE commit on parent `faea66b`) — built by **NexusAI-M (S86M)** —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-29_nexusai-rd733-READY-mail.txt`
- **B — RD-703** @ `bd8e8cdb4c7cd29706467a1e3dfa51591ecead69` (branch `rd-703-wide-run-boundary-s86o`, ONE commit on main `dd15ce1`) — built by **NexusAI-O (S86O)** —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-29_nexusai-rd703-READY-mail.txt`
- **OPTIONAL — RD-707 (NexusAI-O) and RD-732 (NexusAI-M)** — **NOT READY at drafting; NO origin branch names either (MEASURED, ls-remote 19:08:17 and 19:16:19 AEST).** Their sections (§OPT-707, §OPT-732) are **ADD ONLY IF Tuesday stamps it with a head sha**; the launcher leaves each out unless its `P7_*` / `P32_*` stamps are set.

**Batched under the 2026-09-18 batch-gates rule, as batches #1-#9.** A is a PRODUCT change (static first-run page script) plus cells, a comment and a lowered debt fixture; B is TEST-ONLY (a shared test helper, one cell file, a removed parked file). **A and B share NO path but the counts file** (MEASURED, §1). What they share is ONE merge window, one lock queue and one merged tree. **B's semantic cross is with RD-466 `3f7e263`** (queued, batch 9 GO WITH FINDINGS), whose changed cell files CONSUME B's helper (C-68, row x1).
**Every head is re-read by `git ls-remote` in the launcher, which refuses on a mismatch.**

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 19:30
Self-check note: Tuesday read §§0-2a, 4, 5, 12, the WRONG list and FILL AT STAMP line by line; §§3, 3a, 3b, 8-11 are the batch 9 template Tuesday read whole at 12:4x today and are taken as carried. Rulings at stamp: (1) RD-707 and RD-732 are NOT members at this launch (no origin branch, no READY); each may join by an ADDENDUM from tuesday-agent@. (2) WRONG item 8 accepted as the drafter wrote it: name case 4 and case 6 under C-98, do not re-rule. (3) The browser leg uses the installed Google Chrome (channel chrome), never a download; the CDN aborts are classified, not counted as product errors. (4) The MERGE ORDER is the gate's to recommend.

## TUESDAY'S RULINGS (the commission; carried in substance — the gate applies them, it does not re-rule them)
- **Tiers.** **RD-733 is TIER 2 (through-code) PLUS A REAL-BROWSER LEG** (Tuesday's ruling: the READY's own surface is a rendered page, and its claim is a console error in a real browser). **RD-703 is TIER 2 (through-code)** (Tuesday ruled its shape **(a)**, a boundary-character rule; the gate verifies (a) as built, it does not re-open (a) vs (b)).
- **(a) ONE gate session for both; a browser leg for RD-733 ONLY**, against a LOCAL server on `127.0.0.1` booted from YOUR OWN tree (open mode, a fresh data dir), driving a real Chromium-family browser (Playwright or your browser tool). **Never the demo, never any non-loopback host** (§11).
- **(b) Main is `f9cb440` at drafting** (Tuesday's ls-remote 19:0x AEST; the drafter's 19:08:17 and 19:16:19 AEST readings agree; RD-204 via PR #33 on top of `faea66b`). **MAIN MAY MOVE BEFORE AND DURING THE GATE:** merges are QUEUED — RD-723 (`19fc17c`), RD-618 (`874c4f5`), RD-466 (`3f7e263`), batch 3 (RD-685 `9d7076b`, RD-314 `ce148d5`), batch 8 (RD-700 `006b056`, RD-609 `8f9d921`, RD-648 `b12a475`), P's RD-197 (`43e729c`) onward. **Take M0 = origin main AT YOUR OWN START by `git ls-remote`, say so, and RE-BASE EVERY PREDICTION in this brief on it** (counts, `__tests__` census, the helper's consumer set, C-185's known set, which partners are already in). Re-read main at start, mid and end. Never re-base mid-gate.
- **(c) C-190: every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes (test code included). The gate itself NEVER opens, comments on, approves or merges a PR.** You READ (gh, READ ONLY) whether each branch has a PR and its CodeQL result; if none exists, **CodeQL is NOT RUN at that head** — say so.
- **(d) C-57 on the merged tree:** predict the id set; like with like (all history-bearing checkouts). **Neither member is cut from `1904765`, so C-187 does NOT apply to either** (MEASURED: `image-content-exposure` blob `9ede5fd` at `f9cb440`, `ed4c1bf`, `bd8e8cd`). **Predicted missing 0; any missing id is a STOP.**
- **(e) The gate NEVER merges and never pushes. Findings only.** Merges exist ONLY inside your own scratch clones, as the merged-tree measurement (§8).
- **(f) STANDING (batch 7 ruling f): every jest run inside a hold gets `--forceExit` AND a hard deadline; every mutated file is restored in a `trap … EXIT`.** H-20 and H-21 (§3a).
- **(g) C-185 + its ADDENDUM:** main's CI known-failing set is **{rd638-export-always-ends E2, rd465-first-run-open-window O-1 "Turn on Authentication Control: success removes the banner"}**, O-1 ONLY while its failure is the `checkEntraStatus` TypeError; **O-1 leaves the set when RD-733 merges** — the gate shows (row k1-k4) that it can.
- **Launch order:** as gate slots free; the launcher re-pins heads at launch and reads main as it finds it.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not build
these changes and you owe no builder anything. **Every line below that reports what a builder says is a CLAIM, never evidence.** Explore two changes — a removed
dead auto-check on the first-run User Access tab plus a lowered brand-debt fixture (A), and a boundary-character rule in the wide-run reader every image-content
gate uses (B) — looking for any state in which **the User Access tab still throws, renders less, or loses a function a user ever reached; the debt guard stops
reddening on re-added debt; a lowered count is not the measured count; a function the removal deleted still has a caller; a wide-run reading that was right
before changes; a gate that reads the helper goes red or silently blind; a cell is green while its named behaviour is broken; or the id set loses a test silently.**

- **RD-733 is TIER 2 (through-code) + a REAL-BROWSER LEG.** Verdict: **GO / GO WITH FINDINGS / NO GO at `ed4c1bf`**, plus its merged-tree result.
- **RD-703 is TIER 2 (through-code).** Verdict at **`bd8e8cd`**, plus its merged-tree result.
- **One verdict PER ticket, one report, one mail.** A finding on one ticket never becomes another's verdict.
- **TIER 2 AT THROUGH-CODE WEIGHT, FINDINGS-ONLY:** no fixes, no pushes, no PRs, no deploys, nothing to Partner Center, the demo or production (§11).

## THE CLARIFICATIONS THAT BIND THIS GATE (opened by the drafter at source, ~19:15 AEST)
File: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md` (341,777 bytes, 1985 lines, mtime 2026-09-29 13:03;
the last numbered entry is C-191 at :1977 — re-read line numbers, the file grows). **The drafter opened ONLY these (line numbers MEASURED):**
- **C-18** (:109) — *"Dead UI is removed, not hidden."* (Kam, 2026-09-14). RD-733's removal rests on it.
- **C-40** (:231) — a check must be able to fail on the thing it claims to be about.
- **C-49** (:305) / **C-50** (:314) — the PRIOR-WORK check; keep what works.
- **C-57** (:416) — *"A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control."*
- **C-68** (:663) — a verdict holds only at its head; *"a clean merge-tree and a changed measured surface are not in tension"*; re-run the affected cells BY NAME.
- **C-98** (:912) — *"A cell asserts the PROPERTY THAT MUST HOLD AFTER THE FIX, never the defect that exists before it"* (row r6: RD-703's case 6 and case 4 pins).
- **C-102** (:951), **C-104** (:978), **C-112** (:1147), **C-125** (:1326), **C-133** (:1432), **C-141** (:1486) + ADDENDA, **C-174** (:1794) — as carried in the batch 9 brief.
- **C-130** (:1392) — *"A cell that fails for a known, ticketed reason is PARKED outside the suite, never `test.skip`ped inside it."* RD-703 RE-ARMS such a cell.
- **C-184** (:1897), **C-185** (:1906) + its **ADDENDUM** (:1912) — *"O-1 counts as known ONLY while its failure is `TypeError: Cannot set properties of null (setting 'disabled') at checkEntraStatus`"* and *"O-1 leaves the set when **RD-733** merges"*; **C-186** (:1919).
- **C-187** (:1927) + its ADDENDUM — not applicable to either member (ruling d); read it only for the cross tree MT2 (RD-466 carries `7e3262b`).
- **C-190** (:1962) — *"Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included."*
- **Not opened by the drafter, so not cited:** every other C-number (C-176, the rd200 fixture's `_about` ruling, is NAMED by its title only — read it if you rely on it).

## PRIOR ROUND
PRIOR ROUND (RD-733): **no prior gate.** RD-733 is linked as a Duplicate of **RD-189** (Low, pass-9 P9-07c, "guard the lookup") and Relates to **RD-469** (F-11,
the `1470e18` gate, "C-18 dead UI") — RELAYED from the READY :33-38; the rd465 O-5 note (`08c6128`) named the throw "pre-existing on main".
PRIOR ROUND (RD-703): **no prior gate.** The parked cell is **RD-699**'s (S84O, `02fe76a`), parked under C-130 for this ticket; WIDE_RUN / unwiden are **RD-447**'s (`911e706`).

PRIOR ROUND (method, and the lessons this brief carries): the **batch 9 gate** is the most recent NexusAI gate.
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch9/report.md`
(verdicts §0; merged tree §8, main-moved §8.9; WRONG §14; self-corrections §15; recommendations §17). **Carried from it, each deliberately:**
1. **A membership can change mid-gate** (batch 9 took RD-466 by a Tuesday ADDENDUM). An ADDENDUM mailed from `tuesday-agent@` supersedes the launcher's closing
   member line — whatever its subject's arrow says (batch 9 §14.9: an ADDENDUM from `tuesday-agent@` arrived titled "[Wednesday -> …]"). Apply it; record it.
2. **Main moved DURING batch 9** (`dd15ce1` → `faea66b`), and after it (→ `f9cb440`). **Measure every member onto the main you find at the END as a merge-tree
   (counts-only?) and name the combined blobs** (§8.9's form) — the verdict still names M0.
3. **S-2 (a VOID arm):** a driver called a function that did not exist on an older tree — **guard every driver against the oldest tree it runs on** (here: the
   `faea66b`/M0 browser arm and the `dd15ce1` helper arm).
4. **S-4 (a wrong prediction):** a clone-2 merge predicted to conflict was clean — **write predictions before, and report the wrong ones as predictions, not measurements.**
5. **S-5 (a VOID control):** the C-112 census's "M0 left out" control read 0 because a member CONTAINED M0 — **a zero stands only beside a control that fires
   for THIS parent set.** B contains `dd15ce1`, A contains `faea66b`; M0 contains both.
6. **§14.1 (a message prediction was wrong):** predictions about a THROWN or LOGGED message are measured and quoted, never assumed from the code path.
7. **E-1 (batch 9, READ ONLY):** npm-audit fails on EVERY ref since 02:17Z on `ip-address` GHSA-2vr4-cq9g-pvrc until RD-732 lands — **any PR's CI will show that
   red; it is not a member's finding** (name it, do not count it).
8. **The batch 8 lessons still stand** (K2 full verify cannot pass today — every run here is K1; status-check every tree; run every control inside the clone
   that owns the objects; every instrument writes its own distinct path; zsh eats `:s` and a leading `=` — `/bin/bash`, braces).
**Reuse instruments BY COPY** from batch 9's `evidence/` (`qa-srvlib`-family server boot via batch 7's `qa-srvlib.js`; `qa-netbelt.sb`, `qa-netbelt-ctl.js`,
`qa-floorlib.sh`, `qa-floorcount.py`, `qa-to.sh`, `qa-holdlib.sh`, `qa-jestwrap.sh`, `qa-runj9.sh`, `qa-mut9.py`, `qa-mutlib9.sh`, `qa-merge9.sh`,
`qa-c57-id-superset.sh`, `qa-c112-census.py`, `qa-h1-selftest.sh`, `qa-h1-scan.py`, `qa-jsum.js`, `qa-mail.py`, `qa-ssprint.sh`) at
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch9/evidence/`, and batch 7's `qa-srvlib.js` at
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch7/evidence/`. **Batch 9's `qa-floorlib.sh` defaults are
STALE (`ROOT=68684`, batch 9's seats) — correct BOTH.** **macOS has no `timeout` binary** (`qa-to.sh`: `perl alarm`, rc 142 = fired).

## 1. Targets — verified at drafting from the object store (19:08–~19:40 AEST)
**origin by `git ls-remote` at 2026-09-29 19:08:17 AEST (call ended 19:08:20):** `main` **`f9cb44059401f560a9e72532b95705103354a7aa`** (= `refs/pull/33/head`) ·
`rd-733-user-access-stale-entra-check-s86m` **`ed4c1bfd5a195f163b8f76e84b467157f8b97813`** · `rd-703-wide-run-boundary-s86o` **`bd8e8cdb4c7cd29706467a1e3dfa51591ecead69`** ·
`rd-466-image-case-names-s86o` `3f7e263bf69f571d79aeae6ecc7b48ce6730d4c2` (the cross partner) · `rd-723-rd638-e2-budget-s86n` `19fc17ca5aa41e3be3a6b9d174a5d627f4a33145` ·
`rd-618-csp-intake-residue-s86m` `874c4f503d0f37a032014e562972b17e903e1072` · `rd-646-647-redis-fail-closed-recovers-s86m` `608a1cd99adcc69f6d2cdc552f170e89710adb02` ·
`rd-685-hardlinked-store-s84n` `9d7076b0368f02ca030a904a2ce45de93739238e` · `rd-314-law-window-after-source-s84n` `ce148d5d8332606654c189cd14f3aadee227a407` ·
`rd-700-rd411-control-comment-s86n` `006b05609708bddeeea572ab5a1c7d404cbbe1dc` · `rd-609-gate-table-archive-name-s86n` `8f9d92197e0acf642b4fe2938673861e2a12c5aa` ·
`rd-648-harness-boot-residuals-s86n` `b12a475fa73b439eea49cc9f692ef915af478253` · `rd-197-emphasis-ground-guard-s84p` `43e729cbf056cd7ff064535372e7b2b2f23fcc5f`.
**NO origin branch for RD-707 or RD-732; no `refs/pull/*/head` equals either member head** (re-read 19:16:19 AEST: main, RD-733, RD-703, RD-466 unchanged). None of
the queued heads is an ancestor of `f9cb440`; `faea66b` and `dd15ce1` are. Every sha here is a commit in the local object store (`cat-file -t`).
**Re-read at your start, mid and end. A moved TICKET head is a finding and a reason to stop, never a typo to fix.**

**Chains (MEASURED, `git log --format='%H %P'`):**
- **A:** `ed4c1bf` (parent `faea66b1bce5c17a2fef282c808821b3bf0825c6`, 2026-09-29 19:05:23 AEST, "RD-733: remove the dead User Access auto-check (checkEntraStatus), which threw
  on every visit (C-18)"). **merge-base(A, main) = `faea66b`** — A is NOT forward-merged onto `f9cb440`.
- **B:** `bd8e8cd` (parent `dd15ce1ae8277cc9450e62b11b584a40d2226bf3`, 13:46:39 AEST). **merge-base(B, main) = merge-base(A, B) = `dd15ce1`.**
- **Main since the members' bases:** `faea66b..f9cb440` = RD-204 (`b86799d` merge of `faea66b` into `rd-204-vendor-coverage-s84p`, then `f9cb440` counts
  4210/254). Files: `__tests__/helpers/dom.js` (M, `04f182f` → `3f913ff`), `__tests__/helpers/vendor-surface.css` (M), `__tests__/rd204-bootstrap-5.3.0-painting.json`
  (A), `__tests__/rd204-vendor-coverage.test.js` (A), counts. `dd15ce1..f9cb440` adds RD-681 (the server entry point `bc099b2` → `0d7e387`, `rd681-…test.js`).
  **`__tests__/helpers/dom.js` is `require`d by rd733 AND rd465** (and 30 other files) — **C-68: rd733/rd465 run on MT1 under a dom.js neither head carried.**

**Deltas (MEASURED, `git diff --numstat`):**
- **A over `faea66b`:** `static/js/first-run-setup.js` **+5/−118** (`bec7ae8` → `9d62976`) · `__tests__/rd733-user-access-no-stale-check.test.js` **+97** (added, `ce8963a`) ·
  `__tests__/rd465-first-run-open-window.test.js` **+4/−3** (`720e6b1` → `f16b811`, comment text only — READ) · `__tests__/fixtures/rd200-js-brand-debt.json` **+3/−3**
  (`48965a5` → `18afe43`) · counts **+3/−3**. **Counts 4195/253 → 4199/254** (+4 tests: U1, CTRL-REC, CTRL-TAB, CTRL-VAL; +1 suite).
- **B over `dd15ce1`:** `__tests__/helpers/image-manifest.js` **+38/−1** (`ceacc7f` → `23bfa4f`) · `__tests__/rd699-decode-branches-behaviour.test.js` **+59/−4**
  (`df3ae5a` → `2047c79`) · `__tests__/helpers/rd703-parked-NOT-RUN/rd699-be-run-glue.test.js` **−28 (deleted, `cd66df5`)** · counts **+2/−2**. **Counts 4191/252 →
  4202/252** (+11 = 10 new + 1 re-armed; the parked file lived under `__tests__/helpers/`, which `testPathIgnorePatterns` excludes).
- **Blobs elsewhere:** `static/first-run-setup.html` `50be509` at `faea66b`, `ed4c1bf`, `dd15ce1`, `bd8e8cd`, `f9cb440` · the server entry point `0d7e387` at `f9cb440` and `ed4c1bf`,
  `bc099b2` at `bd8e8cd`/`dd15ce1` · `image-content-exposure` `9ede5fd` at `f9cb440`, `ed4c1bf`, `bd8e8cd` (`7e3262b` at RD-466 `3f7e263`) · `image-manifest.js`
  `ceacc7f` at `f9cb440`, `ed4c1bf`, `3f7e263` · `package-lock.json` `9064763` at every member/main sha (`f74a4e8` at RD-732's `7e63afe`/`daf2210`) · the harness `2453a3f`
  everywhere · `scripts/verify-suite.sh` `eb9731f` everywhere · `rd200-js-colour-corpus.test.js` `5219fd5` at `ed4c1bf` and `f9cb440`.
- **Counts:** `faea66b` 4195/253 · **`ed4c1bf` 4199/254** · `dd15ce1` 4191/252 · **`bd8e8cd` 4202/252** · **`f9cb440` 4210/254** · `3f7e263` 4191/252 · `7e63afe` 4191/252 · `daf2210` 4210/254.
- **`__tests__` files (NUL-safe `ls-tree -r -z`):** 295 (`dd15ce1`) · 296 (`faea66b`) · 297 (`ed4c1bf`) · 294 (`bd8e8cd`) · **298 (`f9cb440`)**.
- **Harness require-population:** 23 at `f9cb440` and `ed4c1bf`, 22 at `bd8e8cd` (no rd681) — neither member touches the harness.

**Main may move (ruling b).** Call main at your start **M0**. (1) M0 must be `f9cb440` or a DESCENDANT (the launcher refuses otherwise); (2) main's movement
since `f9cb440` must not touch a member path (the launcher refuses otherwise); **it MAY touch `__tests__/helpers/dom.js`, `static/first-run-setup.html`, or any
file that `require`s `image-manifest.js` — a NOTE, and then C-68 on that member's cells**; (3) your merged trees are **MT1 = M0 + A + B** and **MT2 = MT1 + `3f7e263`**
(unless RD-466 is already on M0 — then MT1 IS the cross tree; say so); **predicted at M0 = `f9cb440`: MT1 4225/255 (4210 + 4 + 11 / 254 + 1 + 0), MT2 4225/255
(RD-466 adds 0/0 — its counts equal its base's)**; re-base both on YOUR M0 (each queued merge adds its own delta — ARITHMETIC ONLY); (4) if main moves AGAIN during your
gate, your verdict names M0 and says what moved (C-68), and you measure each member onto the END main by merge-tree (lesson 2).

### TARGET A — RD-733 (TIER 2 + browser leg) @ `ed4c1bf`
- **What changed (READ, the whole diff over `faea66b`):** in `switchSection`, the block `if (section === 'users') { setTimeout(() => checkEntraStatus(), 500); }`
  is replaced by a 5-line comment; **`async function checkEntraStatus()` (≈100 lines) and `function updateEntraComponent(…)` are deleted.** At `faea66b`
  `checkEntraStatus` reads `#check-entra-btn`, `#entra-status-loading`, `#entra-status-list`, `#entra-overall-status`, then does `btn.disabled = true` FIRST — so it
  throws before any fetch. The Analytics timer `setTimeout(() => loadDataSources(), 300)` is unchanged (CTRL-REC's premise). `revalidateEntraConfig` is kept.
- **Cells (READ, `ce8963a`):** jsdom; the page body without scripts; `identifier-mask.js` then `first-run-setup.js` (the page's order). **U1** switches to `users`
  with `window.setTimeout` replaced by a recorder, runs and AWAITS every recorded callback, expects none to reject. **CTRL-REC** (Analytics records `[300]`),
  **CTRL-TAB** (section/tab active, `#entra-status-list` present), **CTRL-VAL** (`revalidateEntraConfig` marks `#entra-tenant-badge` "Valid" for synthetic ids).
- **The fixture (READ):** three first-run-setup entries lowered — `#28a745` 16 → 15, `#dc3545` 2 → 1, `#ffc107` 5 → 4; 66 entries both sides; debt total 147 → 144.
  A raw literal count of the three values in `first-run-setup.js` reads 16/2/5 at `faea66b` and 15/1/4 at `ed4c1bf` (drafter, `grep -o`, NOT the guard's extractor).
  The guard (`rd200-js-colour-corpus.test.js`, unchanged `5219fd5`): **RESOLVES** fails when a value is unrecorded or found > recorded; **NO ROT** fails when found <
  recorded; **REPORTS** asserts the unresolved total = the manifest sum. The removed code also held `#d4edda`, `#fff3cd`, `#f8d7da` — **not lowered: verify they are
  tokens or otherwise unrecorded** (the guard would have gone red otherwise).
- **Builder's claims (RELAYED, READY :14-31):** browser before (main `faea66b`): 1 console error `TypeError: Cannot set properties of null (setting 'disabled') at
  checkEntraStatus (first-run-setup.js:3706:26) at first-run-setup.js:236:34`; after (`faea66b` + the fixed file): 0 errors, 0 warnings; viewport pixels identical;
  RED on `faea66b`'s file: U1 fails with the TypeError, the three controls pass; GREEN 4/4; M1 (only the users timer put back) → U1 only; rd465 10/10 on the fix;
  full verify **4199/4199 across 254**. Two failed runs disclosed (run 1: CTRL-VAL without identifier-mask.js; run 2: rd200 NO ROT before the fixture was lowered).
  **The drafter checked (MEASURED):** `rd733-fixed-first-run-setup.js.keep` hashes (`git hash-object`, no write) to **`9d62976`** = `ed4c1bf`'s blob; `rd733-hold.log`'s
  last VERDICT is the disclosed run-2 FAIL; `rd733-verify.log` carries `VERDICT: PASS — 4199/4199 tests passed across 254 suites` (mtime 19:04, BEFORE the commit at 19:05:23).
- **PRIOR WORK (RELAYED, READY :33-41):** "None of those ids is in any committed static/*.html at any commit (`git log --all -S'id="check-entra-btn"'` is empty)";
  arrived with the root import `8eb94ce`; `9b58261` only MOVED the script; REMOVE by C-18 rather than RD-189's guard; the function would mark steps 1-3 complete from
  `azureAdConfigured` alone and assumes a security group, contradicting RD-454 / C-47 (**C-47 not opened by the drafter**). KEPT: `revalidateEntraConfig`.
- **The drafter's READ of the prior-work surface (MEASURE it, row p1-p4):** the three missing ids are absent from `static/first-run-setup.html` at `faea66b`, but the
  removed function ALSO wrote `entra-{auth,group,users}-{icon,status,badge}` through a template literal, showed `#users-continue`, and marked `#tab-users` completed —
  **most of those DO exist in the HTML** (`entra-auth-icon`, `entra-group-badge`, `users-continue`, …). They were never reached (the throw is at the function's first
  statement). **At the head every `entra-*-{icon,status,badge}` id in the HTML still has a literal JS writer, and `#users-continue` is shown by `showUsersContinue()`
  (READ census)** — so the drafter READS nothing user-facing lost; row p2 measures it.
- **NOT TESTED — VERBATIM (READY :45-49):**
  *"- The demo (RD-76)."* ·
  *"- A real Entra round trip on the tab: open mode, no tenant configured. The saved-config path (revalidateEntraConfig on load) is driven only in jsdom, by CTRL-VAL."* ·
  *"- Browsers other than Chromium."* ·
  *"- Whether any operator relied on the tab marking steps complete by itself: it never did, because the function threw before reaching that code."*
  → **L-A1** (the demo) · **L-A2** (a real Entra round trip; the saved-config path in a real browser — row w5 discharges the Re-validate path in the browser) ·
  **L-A3** (browsers other than Chromium) · **L-A4** (operator reliance — row p3 MEASURES "it never did": the throw precedes every write) · **L-A5** (CI/CodeQL at the head — NOT RUN unless a PR exists).

### TARGET B — RD-703 (TIER 2, through-code) @ `bd8e8cd`
- **What changed (READ, the whole diff):** `scannableText`'s last line `text.replace(WIDE_RUN, unwiden)` → `unwidenRuns(text)`. `unwidenRuns` walks WIDE_RUN matches;
  **the ambiguous shape** = a match whose first char is not NUL, followed by a char that is neither end-of-text nor NUL; **if the first char is NOT `\p{L}\p{N}` and
  the next IS, the first char stays outside and the run is read BE (`run.slice(1) + next`, `end += 1`)**; otherwise the LE reading is kept. **A BE run (`run[0] ===
  NUL`) gets a trailing space when the next char is not whitespace and the piece does not already end in a space.** `WIDE_RUN.lastIndex = end` after each match.
  WIDE_RUN and `unwiden` are unchanged (READ). `ALNUM = /[\p{L}\p{N}]/u`.
- **Cells (READ):** the parked cell RE-ARMED — its 4-line test body **byte-identical** to the parked file's (MEASURED, awk extract + compare), now inside the M-A7
  describe (so its jest id is new; `NUL` resolves to the describe's own `String.fromCharCode(0)`, `GUID` to the file's `…000699` — the same values); a NEW describe
  "RD-703 — an ambiguous wide run is split at its non-alphanumeric boundary" with **10 cells**: case 1, case 2 (+ `labelledIdentifiers` 1), case 3, case 4 (control),
  case 5 (control; both ends letters), "both ends letters or digits" (`LE('Abc')+'d'` → `'Abc d'`), "neither end" (`LE('(ab')+')'` → `'(ab )'`), case 7, case 8,
  **case 6 STATED LIMIT pinned to `'abcxy z'`**.
- **Builder's claims (RELAYED, READY :11-17):** RED with `dd15ce1`'s helper = {re-armed, 1, 2, 3}; green at main: 4, 5, 7, 8, both, neither, case 6's pin; GREEN 21/21;
  **M1 no boundary rule → {re-armed, 1, 2}; M2 no BE trailing space → {3}; M3 rule inverted → {re-armed, 1, 2, case 4}**; C-68 "every consumer of the helper … 15
  suites, 388/388"; full verify **4202/4202 across 252**. The builder's plain-node tables (READ, `rd703-measure-dd15ce1.txt` / `-fixed.txt`): at `dd15ce1` cases 1, 2,
  3, 4, 6 read "DIFF", 5, 7, 8 "OK"; fixed: 1, 2, 3 "OK", **4 and 6 still "DIFF"** (case 4 = `"Tenant ID:  <GUID>"`, a double space, pinned as "today"). Identity:
  `"A"+BE("bcd") === LE("Abc")+"d"` true.
- **The drafter's READ (MEASURE, rows r4-r6):** (i) the consumer census by `require` finds **12** files at the head (13 at `dd15ce1`/`f9cb440`, the extra being the parked
  file); the READY's 15 adds `.dockerignore`/Dockerfile/rd385/rd327 readers — **re-derive and name the difference.** (ii) Latin/digit boundaries only were driven (READY
  NOT TESTED); `\p{L}` makes a Cyrillic/CJK boundary count as a letter — measure one. (iii) "every case that was right before is byte-identical" is a universal claim
  over all inputs — a DIFFERENTIAL (row r5), not 8 cases, is what can refute it.
- **NOT TESTED — VERBATIM (READY :25-28):**
  *"- Case 6 (endianness switching inside one run with no separator) is a stated limit, pinned, not solved."* ·
  *"- Non-Latin scripts at the boundary: ALNUM is \p{L}\p{N}, so a CJK or Cyrillic boundary char counts as a letter; only Latin and digit boundaries were driven."* ·
  *"- UTF-32-in-a-string runs (up to three NULs per char) at an ambiguous boundary: not driven."* ·
  *"- CI Build and CodeQL at this head: not run (no PR). The diff adds no fs calls; the new regex is a single-class \p test, and WIDE_RUN is unchanged."*
  → **L-B1** (case 6) · **L-B2** (non-Latin boundary — row r4 M-latin + r5 corpus) · **L-B3** (UTF-32-in-a-string at the boundary — row r5 drives it) · **L-B4** (CI/CodeQL — NOT RUN unless a PR exists).

### File overlap and MERGE-TREES — the drafter RAN merge-tree in a SCRATCH object dir of its own (NexusAI's store as a read-only alternate)
**MEASURED (`GIT_OBJECT_DIRECTORY` = the drafter's scratchpad, `GIT_ALTERNATE_OBJECT_DIRECTORIES` = NexusAI's `.git/objects`; nothing written in NexusAI), ~19:25:**
M0(`f9cb440`) × A, M0 × B, A × B, and A and B each × RD-723 `19fc17c`, RD-618 `874c4f5`, `608a1cd`, RD-314, RD-700, RD-609, RD-648 `b12a475`, RD-197 `43e729c`,
RD-732-local `daf2210` → **each rc 1, conflicted = `scripts/verify-expected-counts.json` ONLY**. A × RD-466 `3f7e263` and B × `3f7e263` → **rc 0 (clean)**;
M0 × `3f7e263` rc 0; M0 × `daf2210` rc 0. **Context, not ours:** A × RD-685 and B × RD-685 also conflict on `backend/dataErasure.js` — RD-685's own forward merge
(batch 9 named the same). **Re-measure by `git merge-tree --write-tree --name-only` in YOUR OWN scratch object dir (§8.1) on YOUR M0: A × M0, B × M0, A × B, A × `3f7e263`,
B × `3f7e263`, M0 × `3f7e263` (skip what M0 already contains).**

### MERGE ORDER — the drafter's proposal, with its predicted end state and the C-68 re-run set per merge
**Proposed order: 1. RD-733 (A) → 2. RD-703 (B).** Why: A removes `rd465 O-1` from C-185's known set, so every later CI Build is judged against a smaller set;
B is test-only with no CI effect. **The order is file-independent (every pair = counts), so order independence is the control (§8.3), not an assumption. Challenge it.**

| step | merge | predicted conflicts | predicted counts after (M0 = `f9cb440`) | C-68 re-run set BY NAME (on the tree after that step) |
|---|---|---|---|---|
| 1 | M0 + A | counts only | **4214/255** | rd733 (4) + rd465 (10) + rd200 (all) + every cell file that reads `first-run-setup` (45 at `ed4c1bf` by `git grep -l`, 46 at `f9cb440` with rd204 — re-derive; + the `dom.js` requirers that load the page) — positive control rd733, negative control a file that only names it in a fixture JSON |
| 2 | + B | counts only | **4225/255** | the `image-manifest` consumer set (12 requirers at the head + whatever reads the helper's output indirectly — re-derive; positive control rd699, negative control `.dockerignore`) |
| x | + `3f7e263` (MT2, the cross tree) | none (clean) | **4225/255** | the helper consumer set again, **with RD-466's `image-content-exposure` (`7e3262b`) and rd418** — they consume B's helper and neither head carried both |

**End state predicted: MT1 4225/255 · MT2 4225/255 at M0 = `f9cb440` — ARITHMETIC; re-base on YOUR M0; the measurement decides.** Re-derive every set in YOUR clone at
M0 with a positive control (the ticket's own cell file must be found) and a negative control (a file that only MENTIONS the name must NOT be counted as a reader).

### How to build your trees
- **No worktree is created in the NexusAI repo, and you never work in its `2_Project_Files` checkout.** In that repo use ONLY read verbs: `show`, `log`,
  `diff`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `grep`, `ls-remote`, `archive`, `count-objects`. Never `fetch`, `pull`, `push`, `checkout`,
  `worktree`, `commit`, `stash`, `gc`, `clean`, or `merge-tree --write-tree` without a scratch `GIT_OBJECT_DIRECTORY` of your own.
- **Every tree is K1** — `git clone --shared --no-checkout <repo> <dir>` then `checkout` in YOUR clone (origin removed; local identity; `gc.auto 0`;
  `core.fsmonitor false`; hooks off), under a fresh `mktemp -d` in
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/qa-trees/batch10.XXXXXX/`. Status-check before use.
- **Each tree is EXCLUSIVE to this gate and to ONE purpose.** A fresh arm per mutant; never reuse a mutant tree for a clean arm; `batch10`-prefixed directories only.
- **The red-at-parent trees:** A — YOUR clone at `ed4c1bf` with `static/js/first-run-setup.js` restored to `faea66b`'s blob `bec7ae8`; B — YOUR clone at `bd8e8cd` with
  `__tests__/helpers/image-manifest.js` restored to `dd15ce1`'s `ceacc7f` — hashed after the restore, committed IN YOUR CLONE ONLY so each tree is a clean K1.
- `node_modules`: an APFS clone (`cp -c -R`) of the newest gate tree you trust, **after proving** `package-lock.json` is blob `9064763` there too; a real directory, never a
  symlink. (§OPT-732 is the one exception: its tree gets its OWN `npm ci`.)

## OPTIONAL TARGET — RD-707 (NexusAI-O) — ADD ONLY IF Tuesday stamps it with a head sha
**Status at drafting: NOT READY; no READY mail; NO origin branch (MEASURED 19:08 and 19:16). A LOCAL branch `rd-707-key-backup-copies-s86o` sits at `3f7e263` =
RD-466's head (no RD-707 commit yet); the builder's `rd707-verify.log` (19:11) shows it still queued for proof.** If the launcher's `P7_HEAD`/`P7_BRANCH`/`P7_READY` are
NOT stamped, **this section is not part of your gate — do not measure it, and say "RD-707: not a member" in §0.** If they ARE stamped, RD-707 is **TIER 1**, gets its
own verdict, and **these checks are REQUIRED:**
- **v1 — scope and stack:** RD-707 is STACKED on RD-466 (`3f7e263` must be an ancestor of its head unless RD-466 is on M0); its own delta (over `3f7e263`) names
  `.dockerignore` and rd418's cell file (+ counts). C-187's ADDENDUM applies to any tree carrying RD-466 — measure (a1)-(a4)/(b) if a `1904765`-cut branch is merged with it.
- **v2 — THE NARROWING (the builder's own correction, RELAYED from its 13:29 mail to Tuesday):** a first rule `**/*.[eE][nN][vV].*` reddened 4 C-68 cells (rd411's
  `settings.env.example` probe, rd699 M-AB's `machine.env.txt`, S51 ARM 1/ARM 2's nested `.env.local`); it was narrowed to env BACKUPS only (`.bak`, `.old`, `.orig`, `~`,
  case-insensitive). **Prove at the head, by a real `.dockerignore` evaluation of a planted context (the image-content gates' own manifest function, not a regex of yours):
  `.env.example`, `settings.env.example`, `machine.env.txt`, a nested `.env.example`, `docs/…/.env.example` (if RD-391's re-include covers it) SHIP; `prod.env.bak`,
  `prod.ENV.old`, `x.env.orig`, `x.env~`, `x.pem.bak`, `x.key.old`, `x.PEM.orig`, `x.pfx.bak`, `x.p12~`, `x.crt.old`, `x.jks.bak` are EXCLUDED; `.env.save`, `id_rsa.bak`,
  `.env.bak` stay excluded (base behaviour); control: the same plants at `3f7e263` (base) — the backups SHIP there.** Name every plant whose fate differs from this list.
- **v3 — the tracked set is unchanged:** the shipped tracked-file list at base and head identical (builder: 180 → 180) — measured with the gates' manifest function.
- **v4 — mutants:** the builder's (M1 pem backup removed, M2 env backup removed, M3 the broad `*.env.*` rule restored → the new "env-shaped carrier files still ship" cell
  must redden) re-derived INDEPENDENTLY; your own: drop ONE suffix (`~`) → which cell reddens? (C-40: if none, name it).
- **v5 — C-68:** rd418, `image-content-exposure`, rd411, rd699 and every `image-manifest`/`.dockerignore` reader by name on the head, on MT1 (+ RD-707) and against B's
  NEW helper (B changes how those readers read text — the combination is new).

## OPTIONAL TARGET — RD-732 (NexusAI-M) — ADD ONLY IF Tuesday stamps it with a head sha
**Status at drafting: NOT READY; no READY mail; NO origin branch (MEASURED). A LOCAL branch `rd-732-ip-address-10-7-2-s86m` is at `daf221037d20966c64739d0e71e034ff516904b6`
= a merge of `7e63afe` (the lockfile commit, on `dd15ce1`, 13:01:39) with main `f9cb440` (19:06:14; its message says "Merge main faea66b" but its second parent is
`f9cb440`).** If `P32_HEAD`/`P32_BRANCH`/`P32_READY` are NOT stamped, say "RD-732: not a member". If stamped, RD-732 is **TIER 2** and **these are REQUIRED:**
- **y1 — the lockfile diff is ONLY that package** (at `7e63afe` over `dd15ce1`: `package-lock.json` +3/−3, exactly `node_modules/ip-address`'s `version` 10.5.0 → 10.7.2,
  `resolved` and `integrity` `sha512-7H/2gFSIitxc0hG3nOI1glS8QLo/EHBFFLk8vEUjXY/xu0AdL8jZ9U1IzO2PUm0d2D/ofQcAifb0g6OBkt8U7w==` — READ). At the stamped head: the delta
  over its merge-base with M0 is `package-lock.json` only; `package.json` unchanged; no other `packages` key changes (a JSON-level diff of the `packages` map, not a line count).
- **y2 — `npm ci` succeeds** in YOUR OWN fresh K1 tree of the head (its OWN `node_modules`, never the APFS clone): `npm ci --offline --ignore-scripts --no-audit --no-fund`
  under a deadline. **No registry access is permitted (§11): if the tarball is not in the npm cache (`ENOTCACHED`), y2 is NOT RUN — name it and mail a QUESTION; do not go online.**
- **y3 — the resolved version:** `node -p "require('<tree>/node_modules/ip-address/package.json').version"` = `10.7.2`, and `npm ls ip-address` (offline) shows its path
  (lock READ: `ip-address` is `"optional": true`, reached from `socks` ← `socks-proxy-agent` (optional)). **"Ships in the production image" is the builder's claim:** the
  Dockerfile runs `npm ci --omit=dev` (READ :31) — optional deps are NOT omitted by that flag; say whether the chain is installed under `--omit=dev` (an offline `npm ls
  --omit=dev ip-address` in your tree). **No docker.**
- **y4 — the full verify passes** on the head's own tree (through the lock), predicted **4210/254** at `daf2210` (the counts file is main's; a lockfile-only change adds no test).
- **y5 — the advisories:** `npm audit --omit=dev --audit-level=moderate` is NETWORK — NOT RUN; READ ONLY: name what GHSA-rpw4-54j3-4h4q / GHSA-2vr4-cq9g-pvrc affect only
  from what is on disk (the lock's version bump), and say that batch 9's E-1 (npm-audit red on every ref) is expected to clear on the PR's own npm-audit run.

## 2. Why these tiers, and who is waiting
- **RD-733 TIER 2 + browser — severity rules:** **any product error in the real browser at the head (pageerror, or a same-origin console error) is a Major (it is the
  ticket's property); a function or element a user ever reached that the removal took away is a Major; a lowered fixture count that is not the guard's measured count,
  or a debt guard that no longer reddens on re-added debt, is a Major (C-40); a cell green while its named behaviour is broken is a Major (C-40); a READY/comment claim
  that is false is a Minor.** The tab rendering less at the head than at main is a Major.
- **RD-703 TIER 2 — severity rules:** **a reading that was right at `dd15ce1` and changes at the head (outside the ambiguous shape and the BE trailing-space rule, each
  named) is a Major (the READY's own "byte-identical" claim); a helper consumer red at the head or on MT1/MT2 is a Major; a branch of the rule that no cell can see
  (its mutant leaves the suite green) is a Minor (C-40); a pinned known-wrong output (case 6, case 4) is Tuesday's accepted limit — name it under C-98, do not re-rule.**
- **Who is waiting:** RD-733's merge author is **NexusAI-M (S86M)**; RD-703's is **NexusAI-O (S86O)** — under C-184/C-186's turn order and C-190's PR route.

## 2a. LEGITIMATE SHAPES — required measurements, row by row
**Columns: the head, the base it is measured against (P = `faea66b`'s product for A; `dd15ce1`'s helper for B), and the MERGED tree. Every server row: your own K1
tree, under the network belt, a fresh DATA_DIR, killed in a `finally` by pid.**

**A-cells — RD-733's jsdom cells (every arm names the tree; foreign count beside every result).**

| row | shape | expected at `ed4c1bf` | at P | predicted-by |
|---|---|---|---|---|
| u1 | **RED-AT-PARENT (POSITIVE CONTROL FIRST):** `ce8963a`'s 4 cells against P's `first-run-setup.js` (`bec7ae8`) | — | **U1 RED with `TypeError: Cannot set properties of null (setting 'disabled')` (quote it); CTRL-REC, CTRL-TAB, CTRL-VAL green** | builder |
| u2 | the 4 cells, clean; + the H-1 SS control | 4/4 | — | builder |
| u3 | **the builder's M1, re-derived INDEPENDENTLY:** only the users timer put back, calling the removed function | **U1 only** red (`ReferenceError`? or `TypeError`? — MEASURE and quote; the function no longer exists at the head) | — | builder |
| u4 | **the gate's own mutants:** M-other (the users branch schedules `() => { document.getElementById('qa-b10-none').disabled = true; }`); M-guard (the timer put back AND a null-guarded `checkEntraStatus` restored); M-val (`revalidateEntraConfig`'s tenant-badge write removed); M-rec (the Analytics timer removed) | M-other → **U1 red** (U1 is about ANY throw, not one name); M-guard → **U1 GREEN** (name it: U1 does not forbid scheduling, only throwing); M-val → **CTRL-VAL red**; M-rec → **CTRL-REC red** (the recorder's control can fail) | — | drafter |

**W — THE BROWSER LEG (Tuesday's ruling; row by row, main M0 and the head in the SAME window, same browser binary, same steps).** Server: YOUR K1 tree, booted with
batch 7's `qa-srvlib.js` shape (development mode, OPEN mode = no auth configured, a FRESH DATA_DIR, no Redis), on `127.0.0.1:<free port>`, under the network belt,
killed in a `finally` by pid. Browser: Playwright (`@playwright/test` 1.62.1 is in NexusAI's `node_modules`) or your browser tool. **Playwright's bundled Chromium is NOT
installed on this machine at its default path (MEASURED: `chromium.executablePath()` → `…/chromium-1234/…`, exists = false); `/Applications/Google Chrome.app` IS (use
`channel: 'chrome'`). NEVER download a browser (no network).** Every browser run: a route handler that ABORTS every request whose host is not `127.0.0.1:<port>` and
COUNTS it by URL (the page links Bootstrap CSS/icons from `cdn.jsdelivr.net` — they WILL be aborted); launch args `--disable-background-networking --no-first-run`.

| row | shape | expected at `ed4c1bf` | at M0 (the parent's JS blob `bec7ae8` — prove M0 serves the same page files as `faea66b`, else run both) | predicted-by |
|---|---|---|---|---|
| w0 | **LANDING CONTROLS (before any measured arm):** the browser's version string; a page `fetch('http://192.0.2.1/')` is ABORTED by your route (count 1); a same-origin `/api/health` → 200; a `setTimeout(() => { throw new TypeError('qa-b10-ctl'); }, 10)` evaluated in the page is CAUGHT by your `pageerror` listener (count 1) | all four fire | same | drafter |
| w1 | **RED AT MAIN (POSITIVE CONTROL FIRST):** open `/first-run-setup.html`, listeners attached BEFORE navigation (`pageerror`, `console` all types, `requestfailed`), click `#tab-users`, wait 1,500 ms, then 3,000 ms more | — | **exactly ONE pageerror `TypeError: Cannot set properties of null (setting 'disabled')` whose stack names `checkEntraStatus`**, ≈500 ms after the click (quote the timestamps); quote file:line:col | builder |
| w2 | the head, the same steps | **0 pageerrors, 0 same-origin console errors/warnings within 4.5 s** | — | builder |
| w3 | **console classification:** every console error at both trees split into (i) same-origin (product) and (ii) the aborted CDN URLs (`net::ERR_FAILED` on `cdn.jsdelivr.net`) — **the READY's "0 errors" was measured with the CDN reachable; yours will carry (ii)** | (ii) IDENTICAL by URL at main and head; (i) = {} at head | (i) = {the TypeError} | drafter |
| w4 | **"the tab renders fully" (DOM, not pixels):** after the click — `#section-users` has `active` and a non-zero bounding box; `#tab-users` active; `#user-step1..3` visible; `#entra-status-list` present with the SAME number of visible `li` as the HTML carries; `#users-continue` present; screenshots (viewport AND full page) of the User Access tab | as stated, **identical element set and boxes to main** | as stated | commission |
| w5 | **the kept path in a real browser (L-A2, partly):** enter CTRL-VAL's synthetic tenant/client ids, drive the tab's Re-validate control (or call `revalidateEntraConfig()` if no control is on the tab — say which) | `#entra-tenant-badge` reads "Valid"; **0 aborted non-CDN requests** (no tenant contacted); 0 pageerrors | same | drafter |
| w6 | **pixels:** the viewport screenshots at main and head compared byte-/pixel-wise (READY: "identical") | identical, or the differing region named | — | builder |
| w7 | **C-68 by blob identity:** every same-origin file the page loaded (from YOUR network log: html, `js/*.js`, css) — its blob at the head vs on MT1 | identical (A's page files are M0's except `first-run-setup.js`) — **if ANY differs, run w1-w4 on MT1 too** | — | drafter |

**P — PRIOR WORK (C-49), READ + MEASURED.**

| row | shape | expected | predicted-by |
|---|---|---|---|
| p1 | **the history:** `git log --format='%h %ad %s' -S'check-entra-btn' -- static`, the same for `checkEntraStatus` and `entra-overall-status`; `git log --all -S'id="check-entra-btn"' -- static` (and WITHOUT `-- static`) with a positive control (`id="entra-auth-icon"` → ≥ 1 commit) | `8eb94ce` (root import) and `9b58261` (the CSP refactor that MOVED the script) only; **scoped to `static/` the `id=` pickaxe is EMPTY; unscoped it returns `ed4c1bf` itself** (the cell file's own comment quotes the literal — MEASURED by the drafter); quote `9b58261`'s diff hunk to show it removed no element | READY + drafter |
| p2 | **what the removed code WROTE, and who writes it now:** every id the removed function touched (literal and `entra-${component}-…` expanded for auth/group/users), each: present in the HTML at `faea66b`? at the head? written by any remaining JS at the head (literal writer)? | the three missing ids absent everywhere; every HTML-present id still has a writer at the head; `#users-continue` via `showUsersContinue()`; `#tab-users` 'completed' — **name who sets it now, or say nothing does (and whether anything ever did, given the throw)** | drafter |
| p3 | **L-A4 — "it never did" (operator reliance):** at P in jsdom AND in the browser, instrument the removed function's first write (`btn.disabled`) and its first fetch (`/api/health`, `/api/setup/status`) — did any fetch or DOM write after line 1 ever execute? | **0 fetches from `checkEntraStatus`, 0 writes past `btn.disabled`** — the throw precedes all (quote the network log at P: no `/api/setup/status` request attributable to the users switch) | READY |
| p4 | **the READY's two stated reasons** (steps 1-3 marked complete from `azureAdConfigured` alone; "groups are likely set up") — READ at `faea66b`, quoted; say whether C-47 / RD-454 say what the READY says (C-47 NOT opened by the drafter — open it and quote, or say you did not) | quoted | READY |

**F — THE LOWERED DEBT FIXTURE (a guard change; C-40).**

| row | shape | expected | predicted-by |
|---|---|---|---|
| f1 | **each lowered count = the guard's own measured count at the head:** run rd200's own extractor (its `jsCorpus()`/`actual` map, in-process, not a grep) at `ed4c1bf` and at P for the three keys | `first-run-setup.js #28a745` 15 (P 16), `#dc3545` 1 (P 2), `#ffc107` 4 (P 5); every OTHER entry's measured count unchanged between P and head | builder |
| f2 | **the three not-lowered colours the removed code held** (`#d4edda`, `#fff3cd`, `#f8d7da`): tokens? recorded? | say which, by the guard's own `TOKENS` set; if recorded and not lowered, NO ROT would have reddened — prove it did not by the head's rd200 run | drafter |
| f3 | **PLANT (debt added back):** at the head, add ONE `#28a745` literal in live code of `first-run-setup.js` (a fresh arm) | **RESOLVES red naming `first-run-setup.js #28a745 (manifest records 15, found 16)`**; REPORTS red too (total 145 ≠ 144) — quote both | commission |
| f4 | **PLANT (rot):** at the head, remove ONE more `#ffc107` from live code | **NO ROT red naming `manifest 4, found 3`** | drafter |
| f5 | **the head's code with P's fixture** (`48965a5`) | **NO ROT red on exactly the three keys** (the builder's run-2 red, re-derived) | builder |
| f6 | the fixture's other bytes: `_about`, entry order, tickets — **only the three `count` values differ** (a JSON-level diff) | as stated | drafter |

**K — rd465 O-1 and C-185's known set.**

| row | shape | expected at `ed4c1bf` | at P | predicted-by |
|---|---|---|---|---|
| k1 | rd465 by name, 3 runs each at P, head and MT1 (durations from `--json`) | 10/10 ×3 | 10/10 ×3 (the CI race does not fire locally — say so) | builder |
| k2 | **DETERMINISTIC RED for the race (POSITIVE CONTROL):** a COPY of rd465 (your mutate tool, a fresh arm) with `await new Promise((r) => setTimeout(r, 600));` inserted as O-1's first statement, so the 500 ms users timer scheduled by the O-9 cells fires INSIDE O-1 | **O-1 GREEN** | **O-1 RED with the `checkEntraStatus` TypeError** (quote) — C-185 ADDENDUM's mechanism reproduced | drafter |
| k3 | **the timer mechanism gone:** `switchSection('users')` schedules nothing at the head (U1's recorder shows `[]`); the users-branch `setTimeout` line absent; `git grep -n "checkEntraStatus"` over `static/` returns ONE line, a comment | as stated | P: one scheduled callback at 500 ms | commission |
| k4 | **rd465's diff is comment text only:** strip `//` and `/* */` comments at P and head, collapse whitespace — equal; control (one literal changed in a copy) CAUGHT | equal; control caught | — | drafter |

**C — CENSUS: the removed functions have no other caller (with a positive control).**

| row | shape | expected | predicted-by |
|---|---|---|---|
| c1 | `git grep -n -E "checkEntraStatus\|updateEntraComponent"` at the head over `static/` and `backend/` (and `templates/`/`views/`/`public/` if they exist — list the top-level dirs first) | **one hit: the RD-733 comment in `first-run-setup.js`**; 0 in `backend/`, 0 in any HTML `data-csp-fn`/`onclick` | commission |
| c2 | **positive control:** the same grep at P | ≥ 1 definition + the timer call + 3 `updateEntraComponent` calls, all in `first-run-setup.js` | drafter |
| c3 | **indirect callers:** the CSP dispatcher calls functions BY NAME from `data-csp-fn` (READ: `#tab-users` has `data-csp-fn="switchSection"`) — census every `data-csp-fn="…"` value in `static/**/*.html` at the head, and every `window[…]`/string-keyed dispatch in `static/js/csp-helpers.js`; **no `data-csp-fn` names a removed function** (positive control: `switchSection` found) | as stated | drafter |

**B — RD-703's helper (every arm quotes the received value).**

| row | shape | expected at `bd8e8cd` | at `dd15ce1`'s helper | predicted-by |
|---|---|---|---|---|
| r1 | **RED-AT-BASE (POSITIVE CONTROL FIRST):** `2047c79`'s rd699 against `ceacc7f` | — | **exactly {re-armed, case 1, case 2, case 3} red; case 4, 5, 7, 8, both-ends, neither, case 6 green** — quote each received value vs the builder's `rd703-measure-dd15ce1.txt` | builder |
| r2 | the head clean; rd699's whole file | **21/21** (count it; name every title) | — | builder |
| r3 | **the builder's mutants re-derived INDEPENDENTLY:** M1 (the boundary branch removed), M2 (the BE trailing-space branch removed), M3 (the rule inverted: `ALNUM.test(run[0]) && !ALNUM.test(next)`) | M1 → **{re-armed, 1, 2}**; M2 → **{3}**; M3 → **{re-armed, 1, 2, case 4}** | — | builder |
| r4 | **the gate's own mutants:** M-both (drop `!ALNUM.test(run[0])` — the "both ends alphanumeric" branch); M-next (drop `next !== NUL`); M-li (drop `WIDE_RUN.lastIndex = end;`); M-latin (`ALNUM = /[A-Za-z0-9]/`); M-ws (`!/\s/.test(text[end])` → `true`) | M-both → **"both ends letters or digits" red** (the commission's branch is GUARDED iff this reddens); M-next, M-li, M-latin, M-ws → **MEASURE; any that stays 21/21 is a branch no cell sees — name it (C-40)**; M-latin is L-B2's guard question | — | drafter + commission |
| r5 | **THE DIFFERENTIAL (the READY's "every case that was right before is byte-identical"):** `scannableText` at `ceacc7f` vs `23bfa4f` over (i) every tracked text file the image-content gates scan (their own manifest function, K1 tree), (ii) a SEEDED generated corpus (≥ 10,000 strings: LE/BE/UTF-32-in-string runs of 1-6 chars, ASCII/Latin-1/Cyrillic/CJK/digit/punctuation boundaries, runs at string start/end, adjacent runs, NUL-only runs) — print the seed | (i) **0 differing files** (predict; any difference is named with its path); (ii) every differing input is the AMBIGUOUS shape (first char non-alnum, next alnum) or a BE-run trailing space — **any other class is a Major**; POSITIVE CONTROL: case 1's input IS in the diff list; a UTF-32-in-a-string boundary sample is present (L-B3) | — | drafter |
| r6 | **case 6 and case 4 (C-98):** case 6 pins `'abcxy z'` (a known-wrong reading, the READY's stated limit); case 4 pins `'Tenant ID:  <GUID>'` (a double space the builder's own table marks DIFF) | quote both; **say, without re-ruling, that each cell asserts today's output rather than the property (C-98), and that Tuesday's commission accepted case 6 as a stated limit**; say whether the double space can change any gate's verdict (a `labelledIdentifiers` read of case 4's text) | — | drafter |
| r7 | **C-130 re-arm:** the parked file absent at the head, present at `dd15ce1` (`cd66df5`) and INERT there (`jest --listTests` omits it while listing rd699 — a control); the re-armed test's 4 lines byte-identical to the parked file's; its full jest id at the head quoted; `NUL`/`GUID` bindings resolved (READ) | as stated | — | commission |
| r8 | **C-68 — every consumer of the helper, BY NAME:** re-derive the population by `require` (positive control rd699; negative control `.dockerignore`, which only names it; the helper file itself not counted) AND by behaviour (any file that calls `scannableText`/`scanReadings`/`identifierSignals` through another helper); run the set at `dd15ce1`, the head and MT1/MT2 | all green at the head and MT1/MT2; **name the difference from the READY's "15 suites, 388/388"** | commission |

**X — the cross-change cell with RD-466 `3f7e263` (C-68). On MT2 (or on M0 + B if RD-466 is on M0).**

| row | shape | expected | predicted-by |
|---|---|---|---|
| x1 | the helper consumer set (r8) by name on MT2 — RD-466's `image-content-exposure` (`7e3262b`) and rd418 read text through B's NEW helper | **all green**; name per-file counts | drafter |
| x2 | r5's differential (i) repeated on MT2's tracked text files | 0 differing files | drafter |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.**

## 3. THE QUESTIONS ALL TARGETS ANSWER FIRST
0. **SESSION_SECRET UNSET, EVERY RUN** — §3a H-1's ONE permitted printer. Positive control once per target: its own cell file with a throwaway random
   64-hex secret exported (never printed, never written) — identical results, or say what differed.
1. **Re-pin everything yourself:** `git ls-remote` at start, mid and end (three timestamped readings, branch name beside each sha): main, both member branches,
   RD-466's branch, the queued merges, and whether RD-707/RD-732 branches now exist. M0 and the "Main may move" rule re-proved; chains and exact parents; deltas;
   counts at `faea66b`, `ed4c1bf`, `dd15ce1`, `bd8e8cd`, M0.
2. **POSITIVE CONTROL FIRST — re-derive every red and every mutant INDEPENDENTLY** — your own scripts, never the builders' `rd733-hold.sh`, `rd703-hold.sh`,
   `rd733-serve.sh` or `rd703-measure.js` (read them for method). **Before each mutant arm, prove it still parses — `node --check` on every mutated JS file, exit 0,
   quoted — and that it LANDED (the exact mutated text present, the original absent once the new text is removed; your mutate tool's `--verify` with its negative
   control). A red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.** Quote the failing assertion of every red.
3. **Name every behaviour guarded by no cell, and every one guarded only by source text** (u4 M-guard, r4's survivors at least).
4. **Full verify of each head and of MT1**, `npm run verify -- --maxWorkers=2 --forceExit`, through the lock, SESSION_SECRET UNSET, a fresh SHORT TMPDIR each,
   **K1 only**. Prove `--forceExit` reached jest or say it did not and rely on the deadline. **Predicted: `ed4c1bf` 4199/254 · `bd8e8cd` 4202/252 · M0 = `f9cb440`
   4210/254 · MT1 4225/255 (regenerated once)**; MT2's full verify only if the queue allows (else NOT RUN and named — its C-68 set x1 is required).
   Every failure by NAME; **C-185's known set is CI's, not local: a LOCAL failure of rd638 E2 or rd465 O-1 is named, never waved through.** Re-run until green is not an acceptance gate.

## 3a. INSTRUMENT RULES — H-1..H-21 (carried from the batch 9 brief, which carried batches #1-#8)
- **H-1.** The ONLY permitted SESSION_SECRET printer, verbatim:
  `if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi`.
  **FORBIDDEN anywhere in your scripts:** `${SESSION_SECRET-…}`, `${SESSION_SECRET:-…}`, `${SESSION_SECRET+$SESSION_SECRET}`, `echo
  $SESSION_SECRET`, `printenv`, `env | grep`, `set | grep`, and **echoing an env array that could hold it (`${envs[*]}`)**.
  **Self-test it BEFORE the first hold (a control that can fail):** run the printer once with a throwaway exported and once unset, capture both, assert
  the throwaway's value is ABSENT from both (compare in-process; never print it). **After every hold, scan that hold's logs for the throwaway value** and
  report the count (0); **the scan's own positive control plants a DIFFERENT random marker, never the throwaway.** Print any needle only as
  `<first4>…<last4>`, and **mask GUIDs with or without hyphens**. Export the throwaway INSIDE the run's subshell, never in argv.
- **H-2.** Never construct a product storage object on a DATA_DIR you are measuring AFTER its server booted. Seed BEFORE; read logs RAW.
- **H-3.** Every hook you rely on (a route handler, a pageerror listener, a planted literal, a mutated line) gets a **LANDING CONTROL** before the measured run: prove it
  fired once on a known input. An arm whose instrument failed is VOID, is re-run, and is reported as a self-correction.
- **H-4.** The heartbeat is a **separate child** process started by the hold wrapper (`while sleep 60; do echo "HB $(date -u +%FT%TZ) <step> <pid>
  <elapsed>"; done`), killed in the wrapper's `trap … EXIT`; **the wrapper ABORTS the hold if no HB line appears within 90 s of the grant**, and after
  every hold you compute and REPORT the **max gap** between HB lines (must be ≤ 120 s). Keep the HB child's output unfiltered.
- **H-5.** Restore your own perturbations (mutated files, planted literals, held ports, browser profiles, env files) before any hash, and hash the restore.
- **H-6.** Every extractor and census gets a POSITIVE CONTROL. **Every path is quoted** — `!CODING` and `Testing Agent MAIN` contain `!` and spaces.
  **Every server you boot runs under the network belt (`qa-netbelt.sb`) with its landing control (EPERM for TEST-NET-1, 200 for loopback).** **The browser is the one
  process that may run outside the belt (Chrome's own sandbox): its belt is your route handler, proven by w0.** Try it under the belt first; say which applied.
- **H-7.** Mutants are built and verified ONLY by a quoted tool with a negative control (an unmutated tree → VOID rc ≠ 0). A mutant check that prints an
  empty count is a VOID arm, never a pass.
- **H-8.** The landing rule is "the exact mutated text is present AND the original text is absent once the new text is removed" — never "the anchor is absent".
- **H-9.** Byte-level plants (NUL-bearing wide strings, UTF-32-in-a-string runs, a planted colour literal) are written with `Buffer` and verified by
  `xxd -l 16` (at the plant's offset) and `wc -c` BEFORE use; never with `echo`, `printf`, a heredoc or `JSON.stringify` where the bytes matter.
- **H-10.** Prove every phenomenon reachable before measuring its absence: "0 errors at the head" → w0's thrown-error control caught and w1's TypeError caught at
  main in the SAME browser; "the race" → k2's red at P; "no other caller" → c2's positive control.
- **H-11.** Every script runs under `/bin/bash` explicitly, and every `<sha>:<path>` is written `"${sha}:${path}"`. **Never `set -- $x` or `declare -A`
  in the default shell** (macOS bash 3.2 has no associative arrays).
- **H-12.** Before the C-57 control, list every `__tests__` file any head MODIFIES or DELETES. **Predicted: A MODIFIES `rd465-first-run-open-window.test.js`
  (titles UNCHANGED — READ) and ADDS `rd733-…` (4 ids new to main); B MODIFIES `rd699-decode-branches-behaviour.test.js` (existing titles UNCHANGED; +11 ids)
  and DELETES `helpers/rd703-parked-NOT-RUN/rd699-be-run-glue.test.js` (never collected — prove it at `dd15ce1`).** Name the stale-parent files: every `__tests__`
  file main changed since each member's base that the member carries at its OLD blob (`helpers/dom.js` `04f182f` and `helpers/vendor-surface.css` for both; for B also
  everything RD-681 changed).
- **H-13.** Every tree census is NUL-safe (`ls-tree -z`), with a positive control on a path containing a space.
- **H-14.** Every driver ends with an explicit END record; a run with no END record is VOID, whatever its exit code.
- **H-15.** Pass preloads as `-r "<path>"` in argv, never through `NODE_OPTIONS`. **No exception is declared in this batch.**
- **H-16.** A plant is checked to be what the product will treat it as before it is used (the colour literal sits in LIVE code the rd200 extractor reads, not a comment;
  the generated wide strings match WIDE_RUN — count the matches before using them as the ambiguous shape).
- **H-17.** Absolute tool paths only; every arm asserts the thing actually STARTED (jest's first suite line, the server's listen line, the browser's version and the
  page's `load` event) before its rc is read.
- **H-18.** zsh consumes `:s`/`:a` in `$var:path` AND `=` at word start — `/bin/bash`, braces, and **reject any sha256 equal to `e3b0c442…` as a VOID read**.
- **H-19.** gitleaks canaries (if you run gitleaks over the deltas) are planted as real keys, not JSON-escaped inside strings.
- **H-20 (ruling f).** **EVERY jest invocation inside a hold carries `--forceExit` AND runs under a per-step hard DEADLINE** (`qa-to.sh <seconds> …`,
  rc 142 = fired): targeted cell runs 600 s, the C-68 union 2,400 s, a full verify 2,700 s; **each browser run 180 s**. A deadline that fires ABORTS that step
  (reported by name, never retried silently), the wrapper's EXIT trap runs, and the lock releases through the wrapper's own exit. **`--forceExit` hides open
  handles, so a leak census (children by pid — the browser's too —, ports, temp dirs, browser profiles) runs after every jest and every browser run.**
- **H-21 (ruling f).** **Every file you mutate is restored in a `trap … EXIT` installed BEFORE the first mutation** (restore by `git show
  "${sha}:${path}" > file` or from a pre-mutation copy, then hash-compare to the pinned blob); the trap also covers INT and TERM; after every hold, assert
  every mutated path's hash equals its pinned blob and report it. **A mutant tree left mutated after a deadline is a self-correction to report, and that
  tree is quarantined, never reused.**

## 3b. THE NEGATIVE-ASSERTION SWEEP (C-102) — REQUIRED, scoped to what these members change
**A REMOVES a scheduled callback** (a later throw no longer happens) — a negative cell that was green only because the page threw (e.g. a cell asserting an element
was NOT updated, or a banner still present) may now reach a different line. **B adds an EARLY branch** to how a wide run is read — a negative image-content cell
("an identifier in X is flagged", "no plant ships") may now be refused/flagged by a different reading.
1. **Enumerate the changes (READ, quote each):** `git diff faea66b ed4c1bf -- static/js/first-run-setup.js`; `git diff dd15ce1 bd8e8cd -- __tests__/helpers/image-manifest.js`.
2. **Enumerate the callers' cells** on MT1: every cell that switches to `users` or loads `first-run-setup.js` and asserts an ABSENCE (positive control: rd465's
   O-9 cells must be found; rd454's group-optional cells); every cell that asserts a flag/absence through `scannableText` (positive control: rd699 M-AB, rd411's
   env-var probe). Classify each NEGATIVE or POSITIVE.
3. **For each NEGATIVE cell: does it still reach the check it is NAMED for?** Proven by coverage (batch 9's `qa-cov9.js` form) at P/`dd15ce1` and at the head.
   **A negative cell whose green now comes from a different line is DISARMED** — name it.
4. **Self-test first or ABORT:** a positive control (a cell you know reaches its named check), a negative control (a POSITIVE cell), and a non-empty population.
5. **Report per ticket:** population, negative cells, still reaching, disarmed.

## 4. TARGET A — RD-733 (TIER 2 + browser leg). Answer each with a measurement.
1. **Scope:** `git diff --name-status faea66b ed4c1bf` = the five files; the only product path is `static/js/first-run-setup.js`; nothing in `backend/`.
2. **POSITIVE CONTROL FIRST (u1, w1, k2):** the jsdom red at P, the browser red at main, the race red at P. Then u2-u4, w2-w7.
3. **(a) the browser leg (w0-w7)** — screenshots of the User Access tab at main and head in `./evidence/`, named `b10-w-<tree>-<sha7>-{viewport,full}.png`.
4. **(b) PRIOR WORK (p1-p4)** — name anything user-facing lost, or say "nothing", with p2/p3's measurements.
5. **(c) the fixture (f1-f6)** — each lowered count equal to the guard's measured count; the guard reddens on re-added debt (f3) and on rot (f4).
6. **(d) rd465 O-1 (k1-k4)** — green at the head, the race reproduced red at P and green at the head, the timer mechanism gone.
7. **(e) the census (c1-c3)** — no other caller, direct or by name.
8. **C-190 (READ ONLY):** does `rd-733-user-access-stale-entra-check-s86m` have a PR, and a CodeQL result? The added lines are a comment and cells; say whether any
   changed line matches a pattern CodeQL flags (READ ONLY, a note for the merge author).

## 5. TARGET B — RD-703 (TIER 2, through-code). Answer each with a measurement.
1. **Scope:** the helper, rd699, the parked file's deletion, counts; nothing under `backend/`, `static/`, `docs/`, no Dockerfile/.dockerignore.
2. **POSITIVE CONTROL FIRST (r1):** red at `dd15ce1`'s helper; then r2-r8.
3. **The both-ends-alphanumeric branch** (r4 M-both), **the three mutants** (r3), **the re-armed cell verbatim** (r7), **the 8 measured cases** (r1/r2 against the
   builder's tables), **the C-68 set by name** (r8, x1).
4. **PRIOR WORK (C-49):** WIDE_RUN and `unwiden` KEPT byte-identical (READ: `git diff` shows no `-` line in either); the RD-447 comment still true (its "one character
   per step" claim — say whether `unwidenRuns` keeps it); the superseded "prefer BE" direction (RD-703 comment 38619, RELAYED — not opened by the drafter).
5. **C-190 (READ ONLY):** the branch's PR (if any), its CodeQL; the new regex `/[\p{L}\p{N}]/u` is a single class tested per char — say whether any super-linear shape
   exists in `unwidenRuns` (a PROBE: time `scannableText` on a 1 MB alternating-NUL string at base and head, READ ONLY acceptable).

## 8. THE MERGED TREE (C-68, C-57, C-89, C-104, C-112, C-133). No verdict is complete without it.
1. **Build it in YOUR OWN scratch clone** under `projects/nexusai/qa-trees/batch10.*/clone-1`: `git clone --shared --no-checkout <repo> <dir>`; in the clone
   only: remove `origin`, set a local `user.name`/`user.email`, `gc.auto 0`, `core.fsmonitor false`, hooks off; `git checkout -b gate <M0>`; then `git merge
   --no-ff` in the PROPOSED ORDER: **`ed4c1bf`**, **`bd8e8cd`** (= MT1); then, in a SEPARATE clone (`clone-x`) built from MT1's commit, `git merge --no-ff
   3f7e263` (= MT2; skip if M0 already holds it). **Write your prediction for each merge BEFORE it; anything other than the counts file conflicting STOPS
   (C-57).** Re-measure every pair by `merge-tree` in a SCRATCH object dir first. **C-104: resolve and stage before any census or run.**
2. **Resolve the counts file by REGENERATION, never by hand:** take a side (a placeholder) to complete each merge commit, then `npm run verify --
   --maxWorkers=2 --forceExit --update-counts` ONCE on MT1 after both merges, through the lock, SESSION_SECRET UNSET, under its deadline; commit the
   regenerated file in the clone. **Predicted 4225/255 at M0 = `f9cb440`.** Then a plain verify of the committed head.
3. **Order independence (a control that can fail):** clone-2 in REVERSE (`bd8e8cd`, `ed4c1bf`). **The two `HEAD^{tree}` must be identical apart from the
   counts file** — quote both tree ids and the `git diff --name-only`; the side control run INSIDE the clone that owns both.
4. **Blob identities (C-133's C-112 control):** member paths at MT1 == their head's blob (`9d62976`, `ce8963a`, `f16b811`, `18afe43`, `23bfa4f`, `2047c79`); the
   parked file ABSENT; **`__tests__/helpers/dom.js` = M0's `3f913ff`** (neither member changed it — the C-68 point); every other `__tests__` file == M0's or a head's;
   `package-lock.json` `9064763`. **`__tests__`: 298 at MT1 predicted (298 + 1 − 1), 298 at MT2**; 0 identical to no parent, 0 absent. **The census's "M0 left out"
   control must FIRE for this parent set (lesson 5)** — redo it with A only / B only if it reads 0.
5. **id-superset control (C-57) — ruling (d): PREDICT, then measure, all K1.** merged ids ⊇ ids(M0) ∪ ids(`ed4c1bf`) ∪ ids(`bd8e8cd`)? **Predicted: missing 0;
   new ids 15 (rd733's 4 + rd703's 11) = the counts delta.** Use a COPY of batch 9's `qa-c57-id-superset.sh` (keeps the lock-holder refusal; proven first to STOP on a
   planted missing id). **Any missing id: name it, its file, the file's blob at M0, at each head and on the merged tree, and its history — it is a STOP.**
6. **The semantic overlaps git cannot see (C-68), one hold:** on MT1 — every C-68 set of the MERGE ORDER table BY NAME (per-file counts), rows u2, f1, f3, k1, k2,
   r2, r8; the full verify. On MT2 — x1, x2. Then ONE mutant per ticket on MT1: **u3's M1** (U1 red) and **r3's M1** (re-armed, 1, 2 red).
7. **C-89 on your clone:** `git diff --quiet HEAD` holds; `git show HEAD:scripts/verify-expected-counts.json` equals the regenerated counts.
8. **Main at your END:** `git merge-tree` of each member onto the END main in your scratch objects — counts-only? any combined blob named (batch 9 §8.9's form).
9. **Nothing leaves your clone.** No push, no remote, no PR, no ref written in NexusAI. **Count `<repo>/.git/objects` files before and after your whole
   session and account for any delta by FULL-DATE mtime** (live seats commit there; `--shared` clones and merge-tree freshen mtimes — say so).

## 9. CI (C-185, C-190) — NOT RUN AT ANY BRANCH HEAD unless a PR exists
- **Unverified by the drafter** (no `gh` run; `ls-remote` shows no `refs/pull/*/head` equal to either member head at 19:16 AEST). Check with `gh pr list --head <branch>
  --state all` (READ ONLY, NexusAI's own `GH_CONFIG_DIR`) for both branches (control: without `--head` it returns PRs, e.g. #33); for any PR, its CodeQL `Analyze
  (<language>)` runs (C-190: the `CodeQL` summary run can read completed/neutral before the analyses exist) and any NEW high-or-higher alert in changed code; M0's CI
  Build with `gh run list --commit <M0>` READ ONLY and its failing set against C-185's `{rd638 E2, rd465 O-1 (TypeError only)}`; the npm-audit workflow's red (E-1).
  **`gh` never merges, approves, comments, reviews, labels, re-runs, dispatches, sets a variable, dismisses an alert or opens a PR.**

## 10. Floor discipline — THE FOUR CLAUSES, plus THE DEADLINE RULE (carried from the batch 9 brief)
1. **Every jest run, every server you boot goes through `session-tools/nexusai-lock.sh`, tagged `qa-b10-…`** (e.g. `qa-b10-H1-reds`, `qa-b10-H2-mutants`,
   `qa-b10-H3-browser`, `qa-b10-H4-heads-verify`, `qa-b10-H5-merged`) — C-141: gate-class; under ADDENDUM 2/3 every NEW `qa-*` ticket earns a fresh, self-applied
   yield from the builders. **When a MERGE ticket (gate-class, C-141 ADDENDUM) is already queued when you file, file yours with `--after <that merge ticket's
   tag>` (ADDENDUM 4's tool) so you sit directly behind it; never ahead of it.** **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit another seat's
   process, lock directory, owner file or ticket, even if it looks stuck; if a holder looks stuck, mail a QUESTION (§12) and keep waiting. **Expect a busy
   queue: RD-723, RD-618, RD-466, batch 3 and batch 8 are merging ahead of you, and RD-707/RD-732/RD-591 proofs are queued (MEASURED at drafting in the builders' logs).**
   Pure reads, the r5 differential, the k4/f6 compares and merge-trees may run outside the lock — say which did.
2. **Hold the lock ONCE per multi-run measurement.** Every hold is a TRACKED CHILD of your seat, never detached (`nohup … &`).
3. **Count foreign servers the C-125 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND the server entry point anywhere in the
   remaining argv; "ours" = the ancestor chain CONTAINS your own claude pid. **Record the foreign count BESIDE EVERY RESULT.**
   **NEGATIVE controls, all in the same run, all must classify FOREIGN:** `62649` (NexusAI-M), `9959` (NexusAI-N), `38362` (NexusAI-O), `20317` (NexusAI-P), `64933` (Tuesday) —
   Tuesday names the live seat pids (NexusAI-M, -N, -O, -P and her own) at stamp, each in backticks. Re-read them at start; if one has exited, say so and use the
   others; **a hold with NO live negative control aborts.** Reuse batch 9's instrument BY COPY with YOUR pid as `ROOT` and these as `NEG`:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch9/evidence/qa-floorlib.sh`
   (**its defaults are STALE — `ROOT=68684`, batch 9's seats — correct `ROOT` and `NEG` before any hold**) and `…/qa-floorcount.py`; the original counter is gate 7's
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`.
   **Also count browser processes you start (by pid from your ancestry) and prove 0 left after each browser run.**
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, "0 errors at the head" (w0/w1), "no other caller" (c2), "missing
   0" (the planted-missing-id control), "0 differing files" (r5's case-1 control), "guarded by no cell" (the mutant LANDED and parsed).

**5. THE DEADLINE RULE — every real-server probe, every browser run and every request has a per-step DEADLINE, a HEARTBEAT, and kills its server in a `finally`.**
Every HTTP request carries a client timeout; each step (boot 120 s, request 30 s, browser run 180 s, targeted jest 600 s, C-68 union 2,400 s, full verify
2,700 s, exit 25 s) has a written DEADLINE (`qa-to.sh`); a step past it is ABORTED and reported, never waited on. **Log a HEARTBEAT line at least every 2 minutes
during any hold (H-4: a separate child, ≤ 120 s max gap, aborted if absent at 90 s); a step with no heartbeat for 5 minutes is aborted and reported,** and a
hold that is not progressing releases the lock. Every server, socket, browser and child you start is killed in a `finally` (SIGTERM, then SIGKILL after a grace)
**by pid from your own ancestry, never by pattern (C-174)**, and the reap is confirmed by your floor counter. **H-20 and H-21 apply to every jest.**

## 11. HELD
- **LOCAL RUN, NOT THE DEMO:** every server request goes to a server YOU (or a cell) booted on 127.0.0.1 from YOUR tree, under the network belt (H-6). **The browser
  loads ONLY `http://127.0.0.1:<port>/…`; every other request is aborted by your route handler and counted (w0, w3).**
- **External hosts you MAY contact, and nothing else:** `git ls-remote origin` (pins); `api.github.com` via `gh` READ ONLY (§9); `api.agentmail.to` (your
  verdict mail and any QUESTION). **No Azure, no npm registry, no CDN, no demo, no customer-test tenant, no Entra tenant, no Partner Center, no docker, no browser download.**
- **FINDINGS-ONLY (ruling e):** no fix, **no merge outside your own clones, no push, never push — not to main, not to ANY author's branch**, **no PR opened,
  commented, approved or merged (C-190 is the merge authors' route, not yours)**, no deploy, **nothing to Partner Center, the demo or production**, no money,
  no external comms, no mail to any human. **No `az` at all.**
- **Never write into** the builders' `session-tools/` (copy, then hash at start and end) or any `worktrees/` directory; **never run the builders' hold or serve scripts.**
- **Symlinks, chmod, sockets, held ports, browser profiles, env files and scratch git repos live ONLY under your own mktemp dirs.**
- **Findings-only:** do not commit (outside your clones), move any branch, file a ticket, or write anything inside the NexusAI project (`2_Project_Files`,
  `session-tools/`, `worktrees/`, `1_Project_Definition/`, `qa-reports/`). **NEVER `rm`** — quarantine, per the template §5.

## 12. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch10/report.md` — ONE report covering every
member; evidence in `./evidence/` beside it (screenshots included).

**Questions:** your routing name is **`QA/NexusAI-batch10`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by) and **PROCEED ON THE SAFEST READING without waiting**;
Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning `[Tuesday -> QA/NexusAI-batch10] ANSWER`. Approval-class items (anything
touching the demo, Azure, Partner Center, money, or a human) are NOT RUN and named. Record every question, reading and answer.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 10: RD-733 · RD-703`
Lead the body with ONE line per ticket in this form — `RD-733: <GO|GO WITH FINDINGS|NO GO> @ ed4c1bf (browser leg: main TypeError <n>, head errors <n>)` · `RD-703: … @
bd8e8cd` (· `RD-707: … @ <stamped>` or `RD-707: not a member` · `RD-732: … @ <stamped>` or `RD-732: not a member`) — then one line naming M0, the merge order you
recommend, the merged counts you measured, rd465 O-1 (k2 red at P / green at head?), the r5 differential's result, and the C-57 result. Never
`wednesday-agent@`. AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute: the QA project has none).
Never put the key, a token or any secret in a mail or the report.

Verdict format:
- **RD-733** naming `ed4c1bfd5a195f163b8f76e84b467157f8b97813`: u1-u4; w0-w7 with the screenshots; p1-p4 (anything lost, named); f1-f6; k1-k4; c1-c3.
- **RD-703** naming `bd8e8cdb4c7cd29706467a1e3dfa51591ecead69`: r1-r8 (the differential's classes and its seed); x1-x2.
- **The merged tree (§8):** M0; both orders; counts regenerated once (measured vs 4225/255 re-based on M0); the id-superset result; the C-68 sets by name; one mutant
  per ticket; C-89; the END-main merge-trees; the object-count accounting; **your recommended merge order.**
- **The §3b sweep:** per ticket, population / negative cells / still reaching / disarmed.
- Each of **L-A1..L-A5 and L-B1..L-B4** answered: discharged with a measurement, or left standing and named (C-112).
- All refs as **three timestamped readings (start / mid / end)**, each with its branch name.
- **§3a H-1..H-21:** for each, that it was followed, with the self-test outputs (H-1), landing controls (H-3, H-10), max HB gap per hold (H-4), byte checks
  (H-9), every deadline that fired (H-20) and every restore hash (H-21).
- Every action recommendation carries its evidence class: **MEASURED AT RUNTIME / PROBED / READ ONLY**. Severity is yours; priority is Tuesday's.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, CodeQL at any head without a PR, any browser other than the one local Chromium-family run against a 127.0.0.1 server, the page as styled by its CDN stylesheets (blocked), a real Entra tenant, the npm registry, any deploy, docker, real Azure, Partner Center, the demo, and Windows.

## WRONG OR UNVERIFIED IN THE COMMISSION AND THE READYS — carried so the gate inherits the corrections
1. **RD-733 READY :3 "(parent faea66b = main)"** — main is **`f9cb440`** at drafting (RD-204 via PR #33, merged after the READY's parent was cut). RD-733 is NOT
   forward-merged; main's movement since `faea66b` changes `__tests__/helpers/dom.js` (`04f182f` → `3f913ff`), which rd733 AND rd465 `require` — **C-68: re-run them on MT1.**
2. **RD-733 READY :39 and the cell's own header "`git log --all -S'id="check-entra-btn"'` is empty"** — MEASURED: it now returns **`ed4c1bf` itself** (the cell file's
   comment quotes the literal); scoped to `-- static` it is EMPTY (positive control `id="entra-auth-icon"` → `4e4a630 3a539b1 8eb94ce`). Cosmetic; the claim holds for `static/`.
3. **RD-733 READY :14 "Playwright Chromium"** — Playwright's bundled Chromium is ABSENT at its default path on this machine (MEASURED); which binary the builder drove is
   UNVERIFIED (its `browser-check.txt` names none). `/Applications/Google Chrome.app` exists.
4. **RD-733 READY :39 "None of those ids is in any committed static/*.html"** — TRUE for the three it names (button, spinner, overall card); **but the removed function
   ALSO wrote `entra-{auth,group,users}-*`, `#users-continue` and `#tab-users` 'completed', most of which DO exist in the HTML** (READ). They were unreachable (the throw
   is its first statement) and each HTML-present `entra-*` id still has a writer at the head (READ census). Not false — incomplete; p2 measures it.
5. **RD-733 READY :26 "Full verify on ed4c1bf's tree: 4199/4199"** — `rd733-verify.log`'s mtime (19:04) PRECEDES the commit (19:05:23 AEST); the verified tree is presumably
   the same content, UNVERIFIED. The browser check (~13:08 AEST) ran on an extract of `faea66b` + the fixed file; that file's hash = `ed4c1bf`'s blob `9d62976` (MEASURED).
6. **RD-703 READY :15 "C-68: every consumer of the helper … 15 suites, 388/388"** — the `require` census at the head finds **12** requirers (13 at `dd15ce1`, incl. the parked
   file); the READY's 15 includes `.dockerignore`/Dockerfile/rd385/rd327 readers — UNVERIFIED which; r8 re-derives.
7. **RD-703 READY :8 "(its describe is back in the suite)"** — the TEST moved back byte-identical (MEASURED, 4 lines); its DESCRIBE did not: it now sits under
   "RD-699 — a wide run never glues onto the word after it (M-A7)", so its jest id is new. Cosmetic; no C-57 loss (the parked file was never collected).
8. **Commission "4/5/7/8 green both"** — TRUE of the CELLS; but case 4's cell pins `"Tenant ID:  <GUID>"` (a double space) that the builder's own table marks DIFF at base
   AND fixed, and case 6 pins a known-wrong `'abcxy z'`. Both assert today's output — a C-98 tension the gate names (r6), not re-rules.
9. **Commission "RD-707 (NexusAI-O, .dockerignore key-backup rules stacked on RD-466 …)"** — NO origin branch (MEASURED 19:08, 19:16); the LOCAL branch
   `rd-707-key-backup-copies-s86o` = `3f7e263` (RD-466's head, no RD-707 commit); the builder's proof 2 and verify were still queued (logs 19:11). Not stampable at drafting.
10. **Commission "RD-732 (NexusAI-M, ip-address 10.5.0 -> 10.7.2 lockfile-only bump)"** — NO origin branch (MEASURED); LOCAL `rd-732-ip-address-10-7-2-s86m` = `daf2210`,
    a merge of `7e63afe` with main **`f9cb440`** whose message says **"Merge main faea66b"** (stale message). The lockfile change at `7e63afe` is exactly ip-address's
    version/resolved/integrity (READ). `ip-address` is `"optional": true` in the lock, reached from `socks` ← `socks-proxy-agent` (optional); "ships in the production image"
    is UNVERIFIED (the Dockerfile's `npm ci --omit=dev` does not omit optional deps — READ; y3 measures).
11. **Commission "NexusAI main = f9cb440 (RD-204 via PR #33 on top of faea66b)"** — VERIFIED at 19:08:17 and 19:16:19 AEST (`refs/pull/33/head` = `f9cb440`; chain
    `b86799d` (merge of `faea66b`) → `f9cb440` "RD-204: counts regenerated once on the merged tree (4210/254; batch-6 merge 2)").
12. **Commission "Known-failing CI set: {rd638-export-always-ends E2, rd465 O-1 with that TypeError only} (C-185 + its addendum)"** — VERIFIED at source (:1906, :1913).
13. **Drafter's own slips, disclosed:** (H-18) two reads in zsh lost `:s` (`$s:scripts/…`, `$s:static/…`) and printed errors — re-run under `/bin/bash` with braces; the
    project's hook refused two `cd`s (re-issued without); one `git hash-object` (no `-w`, nothing written) on the builder's `.keep` file. The drafter's merge-trees wrote
    objects ONLY into its own scratchpad object dir. No recursive search of any project tree (single-directory `ls` of `session-tools/s86m`, `s86o`, `session-tools/` only).

## PROVENANCE (drafter, 2026-09-29 ~19:08–~19:45 AEST, read-only; EXACT times only where a `date` call stamped them, the rest "~")
- origin refs | `git ls-remote origin` (named refs, `refs/heads/*`, `refs/pull/*/head`) | **19:08:17–19:08:20** and **19:16:19–19:16:25** (date-stamped)
- every pinned sha a commit; chains, parents, dates, messages; merge-bases; ancestry of the queued heads | `cat-file -t`, `log --format='%H %P %ci | %s'`, `merge-base [--is-ancestor]` | ~19:09
- local refs for RD-707/RD-732 | `for-each-ref` | ~19:10
- deltas and numstats; main's movement `faea66b..f9cb440`, `dd15ce1..f9cb440` | `diff --numstat|--name-status` | ~19:10
- counts at 9 shas; blobs (first-run-setup js/html, fixture, rd465, rd733, helper, rd699, parked, dom.js, ICE, server, lock, verify-suite, rd200 cell) | `git show`, `git rev-parse` | ~19:11–~19:30
- RD-733's product/fixture/rd465 diff whole; rd733 cell file whole; rd465 :20-72 and :141-165; rd200 cell :40-115; census of removed functions/ids at P and head; entra-* writers | `git diff`, `git show`, `git grep -c/-n` | ~19:12–~19:28
- pickaxe `-S'id="check-entra-btn"'` (--all, and scoped to static/) + positive control | `git log -S` | ~19:20
- RD-703's diff whole; rd699 :1-30, :95-130; the re-armed cell vs the parked file (awk extract, byte compare) | `git diff`, `git show` | ~19:13–~19:22
- `image-manifest` consumer census at `dd15ce1`/`bd8e8cd`/`f9cb440`; `first-run-setup` readers; `dom.js` requirers; harness population | `git grep -l` over `__tests__` | ~19:14–~19:18
- merge-trees (27 pairs) | `git merge-tree --write-tree --name-only`, scratch `GIT_OBJECT_DIRECTORY`, NexusAI's objects as alternate | ~19:25
- RD-732 lock diff; ip-address dependents; Dockerfile npm flags | `git diff`, `git show` + python | ~19:30
- CLARIFICATIONS: size/mtime/lines; C-numbers' line numbers; C-18, C-130, C-185 + ADDENDUM, C-187 + ADDENDUM, C-190, C-191 read | `ls -l`, `wc -l`, `grep -n`, `sed -n` | ~19:15
- the batch 9 report §0, §8, §14, §15, §16, §17 | `sed -n` | ~19:07
- builder evidence: `s86m/rd733-evidence/browser-check.txt`, `rd733-hold.log` (whole), `rd733-verify.log` VERDICT, `.keep` hash; `s86o/rd703-hold.log` VERDICT + tail,
  `rd703-measure-dd15ce1.txt`, `rd703-measure-fixed.txt`, `mail-25-rd707.abEHgY`, `rd707-measure-*.txt`, `rd707-verify.log` tail | `ls -la`, `cat`, `grep`, `tail` | ~19:18–~19:32
- Playwright: `@playwright/test` 1.62.1 in NexusAI `node_modules`; `chromium.executablePath()` exists=false; `/Applications/Google Chrome.app` present | `node -e`, `ls -d` | ~19:28
- routing: **no `QA/NexusAI-batch10` line in `fleet/inbox_routing.conf`** (batch9 :146 exists) — Tuesday adds it; the launcher's guard 40 refuses until then | `grep -n` | ~19:30
- report dir `2026-09-29-gate-batch10` absent | `ls -d` | ~19:30
- the batch 9 brief (646 lines) and launcher (571 lines) whole | `Read` | ~19:05

## FILL AT STAMP — Tuesday, before launch (the launcher refuses until the starred items are done)
- ★ both STAMP placeholders at the top (the SELF-CHECK line and the Self-check note) — LAST, by hand, no placeholder token in the note.
- ★ the routing line `QA/NexusAI-batch10|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf`.
- ★ the negative-control seats in §10 (replace the stamp placeholder there with the pids, each in backticks) AND the launcher's `NEG_SEATS` — Tuesday's own pid included.
- OPTIONAL: RD-707 — set the launcher's `P7_BRANCH`, `P7_HEAD` (full 40-hex, re-read by ls-remote) and `P7_READY` ONLY when its READY is on disk; copy the READY to
  `briefs/` and name it in §OPT-707. RD-732 — the same with `P32_*` and §OPT-732. Left empty, the launcher tells the gate each is not a member.
- If a member head MOVES before launch: the launcher's guard 18 refuses — re-pin that head in the launcher and every occurrence in this brief, re-read its
  READY, never `sed` a sha blindly.
