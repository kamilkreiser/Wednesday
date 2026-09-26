# QA Agent Invocation Brief — Datasec/NexusAI, ONE batched gate "batch #6" (lane 4: settings UI + brand, tests and docs): RD-693 (TIER 1) + RD-286 (TIER 2) + RD-204 (TIER 2) + RD-197 (TIER 2) + RD-686 (TIER 2) + RD-692 (TIER 2), plus two OPTIONAL members Tuesday may add at stamp (RD-430, RD-694 item 4) — six targets, six verdicts, one report

**Drafted for Tuesday 2026-09-27 09:25–10:30 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.**
Commissioned by Tuesday's batch #6 commission (2026-09-27, heads read at origin 09:3x AEST) on six READY FOR QA mails on disk, each read WHOLE, all from NexusAI-P (lane 4, seats S84P/S85P):
- **A — RD-693** (lane-4 half: the shown-once SCIM token cleared on leave) @ `ddf1b75f7c3c4aead2da2ce9b3c0b724fb4b3969` —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-rd693-READY-mail.txt`
- **B — RD-286** (ground and geometry guards; ruling (a), two deletions) @ `1645c69eeb9a28a267b44b5ffe7fd5fdb51149b2` —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-rd286-READY-mail.txt`
- **C — RD-204** (vendor stand-in coverage, test-only) @ `fe47bb49124805a67ca79274104309e4c902041c` —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd204-READY-mail.txt`
- **D — RD-197** option (b) (emphasis-on-notice-ground guard, test-only) @ `43e729cbf056cd7ff064535372e7b2b2f23fcc5f` —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd197-READY-mail.txt`
  **and its one-line correction** `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd197-correction-READY-mail.txt`
  (the accepted-limit ruling is dated 2026-09-25T18:21:26Z, not 2025).
- **E — RD-686** (+ RD-694 items 1-3 wording; docs and a helper header) @ `8962a149798531b61eddd22361dec1261a372f4e` —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd686-694-READY-mail.txt`
- **F — RD-692** (provisioning-token guards, test-only) @ `4580829aa7ad1c1cfee969d89885b6d87e1205ca` —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd692-READY-mail.txt`

**Batched under the 2026-09-18 batch-gates rule** (as batches #1-#4). **The six deltas ARE pairwise file-disjoint except
`scripts/verify-expected-counts.json`, which FOUR of them change (RD-693, RD-204, RD-197, RD-692 — MEASURED, §1 File overlap), so the counts
file conflicts in six pairs, not one.** RD-286 and RD-686 do not change the counts. **Two of the six change what a user sees or what ships in
`static/`** (RD-693 `static/js/entra-provisioning-ui.js`, RD-286 `static/css/dark-mode.css`); the other four are tests, a test helper and
docs. **Two members carry a REAL-BROWSER leg (§11a): RD-693 (the batch-2 gate's R11, bfcache Back) and RD-286 (its e2e spec plus an
independent pixel compare).** Every member's colour story goes through ONE BRAND leg (§11b).

**RD-693's lane-1 half is RD-705** (`rd-705-no-store-authenticated-pages-s86m` @ `e164d1a99cb33166d37c98d6f9069d51a7c18ad7`, `Cache-Control:
no-store` on every HTML page from the server entry point). **It is NOT gated here** — Tuesday's commission says it is gated in batch 5a. You
never grade it. You DO measure how it changes RD-693's browser leg if it is on M0 (§11a, row b9).

**OTHER GATES MAY RUN CONCURRENTLY.** At drafting (09:31:51 AEST) the batch-3 gate (`QA/NexusAI-batch3`, claude `36118`, pane `%23`) and the
batch-4 gate (`QA/NexusAI-batch4`, claude `40285`, pane `%24`) were both LIVE and share the NexusAI jest lock (and batch-4 the docker lock).
A batch-5a gate may start. **None is yours: you never touch their worktrees, trees, clones, processes, lock tickets or reports**, and you
queue behind their tickets exactly as behind any other (§13). Their servers will show in your foreign-server counter as FOREIGN — record them,
never "fix" them.

SELF-CHECK: re-read end-to-end for contradictions | @STAMP@
Self-check note: @STAMP@

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester.
You did not build these changes and you owe no builder anything. **Every line below that reports what a builder says is a CLAIM, never
evidence.** Explore a shown-once credential that must now vanish when the admin leaves the page and come back as an explanation, not a
token (A); two deleted dark grounds that must move no pixel, and a browser spec that claims to guard every "stated" ground (B); a coverage
report of what the jsdom vendor stand-in does not paint (C); a placement guard for the dark `-emphasis` colours (D); a brand guide and a
helper header that now claim to say exactly what the brand gates read (E); and two guards for RD-428's token clears (F) — **looking for any
state in which a secret stays on screen or in memory after the admin leaves, a user-visible pixel or colour moves without a ruling, a colour
leaves the style guide, or a guard or a document reports green or "true" over something it never saw.**

- **RD-693 is TIER 1** (credential handling: a shown-once SCIM bearer token; Tuesday's commission raises it from the READY's "Proposed tier 2
  WITH a browser leg", READY :6, exactly as batch 2 raised RD-428). **REAL-BROWSER leg required (R11).** Verdict: **GO / GO WITH FINDINGS /
  NO GO at `ddf1b75`**, plus its merged-tree result.
- **RD-286 is TIER 2 + a browser leg** (C-168 Q1; READY :6). Verdict at **`1645c69`**, plus merged-tree result.
- **RD-204 is TIER 2** (tests only; READY :6). Verdict at **`fe47bb4`**, plus merged-tree result.
- **RD-197 is TIER 2** (tests only, option (b) only; READY :6). Verdict at **`43e729c`**, plus merged-tree result.
- **RD-686 is TIER 2** (docs + a helper header, words only; READY :6). Verdict at **`8962a14`**, plus merged-tree result.
- **RD-692 is TIER 2** (tests only; READY :6). Verdict at **`4580829`**, plus merged-tree result.
- **One verdict PER ticket, one report, one mail.** A finding on one ticket never becomes another's verdict. **A finding that exists only in a
  COMPOSITION (693×692 on the provisioning module, 286×197/204 on the dark sheet, 686×every brand reader, and the optional 430×204/197 on
  `settings.html`) is graded on the merged tree and named against BOTH tickets' merged-tree lines, never silently against one.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **Merge authority (Kam, standing):** *"Please work your way through the tickets and merge once tested."* (2026-09-25 ~22:0x, re-affirmed
  2026-09-27 ~08:2x per Tuesday's commission; RELAYED — the drafter did not read Kam's board). **Merges happen on Tuesday's GO after a gate
  verdict AT HEAD; the merge author is the live lane-4 seat `Datasec/NexusAI-P` (S86P)** — C-175 (:1801): *"lane 4 is the merge author for its
  six READYs (RD-204, RD-197, RD-686, RD-692, RD-693, RD-286) once their gate (batch 6) returns, and nothing merges without a gate verdict plus
  Tuesday's RELEASE."* **No deploy, no production, no Partner Center** — see §12 for what a merge push to main triggers. **This gate merges
  nothing into anything the fleet can see.**
- **Brand (Tuesday's commission):** any colour a change introduces must resolve to NexusAI's style-guide token (`docs/BRAND.md` §3, values in
  `static/css/tokens.css`); **an OFF-GUIDE colour is a Major**; **palette choices are Kam's** (RD-197 option (a) stays his — C-166 :1705 names
  RD-197's order only; the (a)/(b) split is RELAYED by RD-197 READY :6 and the cell's own header).
- **Rulings that ARE in CLARIFICATIONS (read them there):** RD-693 ruled (c) → **C-171** (:1749); RD-286 scope (a)(a)(a), RD-288 measure-first
  and closed, the dark classification ruling (a) → **C-168** (:1719); the two deletions → **C-172** (:1756); **RD-286's deviation ACCEPTED** and
  RD-430's re-pin grant → **C-175** (:1794); RD-694 item 4 ruled (a) → **C-176** (:1805); RD-430 ruled (a) remove the form → **C-166** (:1700).
  Positive control, same file and tool: `grep -n '^\*\*C-141\.'` finds :1480.
- **NOT in any artefact (drafter: `grep -n -i -E 'RD-204|RD-197|RD-692|RD-686'` over CLARIFICATIONS → RD-204/RD-197 only inside C-166 :1705 and
  C-175 :1801, RD-686 only in C-175 :1801 and C-176, RD-692 only in C-175 :1801):**
  - **RD-204:** "Your ruling (S84P thread): fetched ONCE, sha384 verified, list COMMITTED" (READY :41) and "no test fetches anything (Tuesday,
    2026-09-25T12:59:36Z)" (the painting list's own `_about`) — RELAYED.
  - **RD-197:** option (b) ONLY; option (a) (palette values) is Kam's (READY :6, :28); the M2 ACCEPTED LIMIT (READY :17, ruling
    2026-09-25T18:21:26Z per the correction mail) — RELAYED.
  - **RD-692:** the file question — "(a) a NEW disjoint file" vs "(b)" — was **unanswered at READY time** (READY :6; RD-686 READY :25 "proceeding on
    its safest reading"). **Whether Tuesday has since ruled (a) is UNVERIFIED by the drafter** (WRONG list item 7). The gate grades the file as built.
  - **RD-693 tier 1** (the commission; READY :6 proposed tier 2).
- **RD-705 is not in scope** (batch 5a). **RD-701** (guard 3), **RD-289** (empty-state members), **RD-704** (light-corpus resolve-or-record gate),
  **RD-687** (no reachable danger action) are filed follow-ups named by the READYs — **not in scope; never grade them.**

**The clarifications that bind this gate** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md`, 313,569
bytes, 1,847 lines, mtime 2026-09-27 09:09; line numbers by `grep -n -i '^\*\*C-<n>\.'` at 09:3x AEST — the file grows, re-read them):
- **C-02** (:30) a local run serves every page and API with no sign-in (open mode on a fresh DATA_DIR) — the surface your browser drives.
- **C-15** (:94) broken configuration fails with an explanation. **C-18** (:109) dead UI is removed, not hidden (C-171's reason for the meta).
- **C-28** (:153) never write, pull, restore, reset, check out or stash NexusAI's `2_Project_Files`.
- **C-40** (:225) a check must be able to fail on the thing it claims. **C-49** (:299) the prior-work check.
- **C-57** (:410) a counts-only conflict is resolved by REGENERATION with the id-superset control; any other conflicting file STOPS; suites no
  fewer than the larger parent's.
- **C-61** (:489) one browser-backed guard lives in `npm run verify` (RD-490), so **verify needs Google Chrome**; the rest of `tests/e2e/` stays outside.
- **C-68** (:657) a verdict holds only at the head it ran on; a semantic overlap git cannot see is re-run BY NAME; counts regenerated ONCE on the tree
  after the merge — "No conflict is not evidence the number is right."
- **C-89** (:827) after a merge commit: `git diff --quiet HEAD` and HEAD's counts equal the regenerated numbers.
- **C-96** (:893) two cells asserting different properties must fail independently. **C-97** (:900) a fix reddening an older test changes the FIXTURE,
  never the policy. **C-98** (:906) a cell asserts the property after the fix. **C-103** (:955) a canary the ruleset does not target is not a control —
  **exactly RD-204's T2 (a `transparent` tamper that did not tamper).**
- **C-104** (:972) `git ls-files` TRIPLES its population during an unresolved merge — resolve and stage before any census or run.
- **C-110** (:1101) THE FLOOR RULE — every jest invocation through the lock (`jest --listTests` included), the lock held once per multi-run measurement,
  the foreign-server count beside every result, **a ZERO only beside a control that fired in the same window.**
- **C-112** (:1141) a declared limit is where the evidence stops; the id-superset shortcut by byte identity holds ONLY when no test file was content-merged.
- **C-122** (:1278) source text does not cover behaviour. **C-125** (:1320) the foreign-server counter.
- **C-130** (:1386) a known-reason failing cell is PARKED, never skipped. **C-131** (:1407) a check pinning a removed feature is re-anchored.
- **C-133** (:1426) base-aware id accounting and its ADDENDUM (:1434) authorised renames; **C-150** (:1570) C-133's conditions are decided on FILE
  CONTENT (blobs). (Cite only if the id-superset control misses — none is predicted here.)
- **C-141** (:1480) a builder's proof ticket YIELDS to a `qa-*` ticket; ADDENDUM (:1488) a merge hold is gate-class; ADDENDUM 2 (:1490) once PER waiting gate
  ticket; ADDENDUM 3 (:1492) self-applied; **ADDENDUM 4 (:1494) `--after <ticket-tag>`**; **:1484 "Not covered: … gate tickets among themselves"** (§13.6).
- **C-142** (:1503) what "green" means at a merge.
- **C-166** (:1700) RD-430 (a). **C-168** (:1719) RD-286 scope, RD-288, dark classification. **C-171** (:1749) RD-693 (c). **C-172** (:1756) RD-286 two
  deletions. **C-174** (:1784) NEVER KILL BY PATTERN — every browser, server and child you stop is stopped by a pid from YOUR OWN ancestry.
  **C-175** (:1794) RD-286 deviation accepted; RD-430 re-pin grant (three pins, `dom-harness.test.js` + `jsdom-instrument-limits.test.js`, "Not covered:
  any other pin"); lane 4 merge author. **C-176** (:1805) RD-694 item 4 (a).
- **Read, not binding here:** C-173 (:1765), C-177 (:1814), C-178 (:1830); **C-179 (:1839) is the highest C-number at drafting.**

## PRIOR ROUND
PRIOR ROUND: the batch-2 gate (QA/NexusAI-batch2) gated RD-428 @ `823ef9e`, RD-444 @ `2f9da1c`, RD-200 @ `12b5edc`; verdicts GO WITH FINDINGS (RD-428),
GO WITH FINDINGS (RD-200). THREE of this batch's tickets are its findings.
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/report.md`
(§3.3 the mutant table incl. M-A6 :68 and M-A10 :72; §3.4 the real browser :74; **R8 :105, R11 :110**; §3.6 the CDN allow-list :122-128; §3.9 BRAND :144-150;
§7 findings :311-322; A-F1 :329-333; C-F1 :337; **§10 S-4 :376, the bfcache instrument lesson**; §11 floor :381-392).
Findings carried forward and their disposition:
- **A-F1 (Minor)** — two RD-428 F2 properties had no cell: the 409/428 conflict clear (M-A6 → 145/145 green) and "a real switch is distinguished from a
  same-mode press" (M-A10 → 145/145 green) → **filed as RD-692, built at `4580829` (Target F).** Its regression test was specified at :333 and
  recommendation 1 :403 ("rd388 TOKEN also asserts the token is cleared and absent after a 409; rd409-410 SAME MODE asserts a same-mode press is
  SILENT"). **The builder put them in a NEW file instead (READY :6). Say whether the new cells are exactly that specification, or less, and re-run
  the batch-2 gate's own M-A6 and M-A10 against them.**
- **A-N5 (note, pre-existing at both shas)** — Chrome 153 restored Settings from bfcache after Back with the token on screen and in memory
  (`pageshow` `[false,true]`, `Cache-Control: public, max-age=0`) (:110, :321) → **ruled C-171 (c): RD-693 (lane 4, Target A) + RD-705 (lane 1, batch 5a).**
  **Re-run R11 exactly, with the batch-2 gate's corrected method (§10 S-4 :376): Playwright's default `--disable-back-forward-cache` REMOVED, `goBack`
  waiting for `commit`, a landing control that a plain loopback page restores.**
- **C-F1 (Polish)** — the RD-200 gate is described as doing less than it does: hex alpha is KEPT, runtime-built `hsl(${h}…)`/`rgb(${r}…)` ARE read, a
  private field `this.#add` reads as a colour (:264-267, :317, :337) → **RD-694 items 1-3, carried by RD-686 at `8962a14` (Target E); item 4 (the
  fixture `_about`) is OPTIONAL member H.**
- **A-N4 (note)** — `brand-token-conformance` pins no count for `--nx-brand-chrome` and none for any dark value (:322) — context for RD-686's rule-3 text.
- **RD-286, RD-204, RD-197: no prior QA round of their own.** RD-286's lineage: QA pass 19 (F5 and "F5's second instance", 60 device px at `7e5faa9`) →
  RD-288 measured NOT a defect at `c2d84ec` (C-168 :1727). RD-204's: RD-333 delivered the navbar half (READY :40). RD-197's: HISTORY S29 corrected
  "7 of 10" to three accents (READY :28).
- **Instruments — reuse BY COPY, never run in place.** Floor/lock/merge set: the batch-1 gate's corrected copies in
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch1/evidence/`: `qa-floorlib.sh`, `qa-floorcount.py`,
  `qa-dispatch.sh`, `qa-holdlib.sh`, `qa-jestwrap.sh`, `qa-mutate.py`, `qa-merge.sh`, `qa-ssprint.sh`, `qa-h1-selftest.sh`, `qa-h1-scan.py`,
  `qa-c57-id-superset.sh`, `qa-netbelt.sb` (all present, `ls` at 09:3x AEST). **`qa-floorlib.sh` :3-4 names that gate's `ROOT=33673` and
  `NEG=88756,10246,10643,11987,51143` — correct BOTH to this gate's values (§13.3) before any hold.** Browser set: the batch-2 gate's
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/evidence/`: `qa-a-browser.js`
  (its :32 `QA_BFCACHE=1` → `ignoreDefaultArgs: ['--disable-back-forward-cache']`; its :306 `goBack({ waitUntil: 'commit' })`), `qa-a-lib.js`, `qa-a-probe.js`,
  `qa-png.js`, `qa-netbelt.sb`, `qa-netbelt-ctl.js`. The original counter is gate 7's
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`.

## 1. Targets — verified at drafting from the object store (09:28–09:40 AEST)
**origin by `git ls-remote` at 2026-09-27 09:28:31 AEST:** `main` **`1904765007e9447ac6c980f9840c0689a02abe6c`** · `rd-693-token-clear-on-leave-s85p`
**`ddf1b75f7c3c4aead2da2ce9b3c0b724fb4b3969`** · `rd-286-ground-geometry-guards-s85p` **`1645c69eeb9a28a267b44b5ffe7fd5fdb51149b2`** · `rd-204-vendor-coverage-s84p`
**`fe47bb49124805a67ca79274104309e4c902041c`** · `rd-197-emphasis-ground-guard-s84p` **`43e729cbf056cd7ff064535372e7b2b2f23fcc5f`** · `rd-686-694-brand-wording-s85p`
**`8962a149798531b61eddd22361dec1261a372f4e`** · `rd-692-provisioning-token-guards-s85p` **`4580829aa7ad1c1cfee969d89885b6d87e1205ca`**. Also read: `rd-430-remove-response-form-s84p`
`9ba6f1d8976a57130c2c887c6c68509b5efadab4` (being re-pinned, §10) and `rd-705-no-store-authenticated-pages-s86m` `e164d1a99cb33166d37c98d6f9069d51a7c18ad7` (batch 5a).
**`rd-694-fixture-about-s86p` (RD-694 item 4, `1d457cef2a1b1a66454a3ce77d751be56fa8bbbc`) is NOT on origin** — a local branch only (§10). All shas above
are commits in the local object store (`git cat-file -t`). **Re-read all refs at your start, mid and end. A moved TICKET head is a finding and a reason to
stop, never a typo to fix.**

**All six contain main:** `merge-base(<head>, 1904765) = 1904765` for every one (MEASURED). **Counts at `1904765`: 4133/247.**

**Main is moving — the rule.** Call main at your start **M0**. (1) M0 must be `1904765` or a DESCENDANT (`git merge-base --is-ancestor 1904765 M0`); (2)
`git diff --name-only 1904765 M0` must share NO path with the six deltas below except the counts file (the launcher refuses otherwise; re-check it
yourself). **Expected movers: the batch-3 (lane 2, erasure), batch-4 (lane 3, image content) and batch-5a (lane 1, incl. RD-705's server entry point)
merges — none in this batch's delta set, BUT (a) RD-705 on M0 changes RD-693's browser leg (§11a b9), and (b) any `static/` or `__tests__/helpers/`
change on M0 moves what RD-204's pins, RD-197's sweep and the brand readers measure: re-run their named sets on M0 and say what moved.** (3) Your
merged tree is **M0 + all six**; predicted counts **counts(M0) + 33 / + 4** (4166/251 at M0 = `1904765`, ARITHMETIC; C-68 says the measurement
decides). (4) If main moves AGAIN during your gate, your verdict names M0 and says what moved. **Never re-base mid-gate.**

### TARGET A — RD-693 (TIER 1) — the shown-once token cleared on leave, with a REAL-BROWSER leg
- **Chain (MEASURED):** `4a86c4a5d6beb55135bc372bfe9ef6fdc915c0a6` (red-first cells only, parent `1904765`, counts = main's 4133/247) → **`ddf1b75`** (the fix + counts,
  parent `4a86c4a`). No forward merge (cut from `1904765`).
- **Delta over `1904765`: 3 files, +163/−3** — `A __tests__/rd693-token-cleared-on-leave.test.js` (128), `M static/js/entra-provisioning-ui.js` (**+32/−0, a single
  added block at :1430-1461**, before `window.NexusProvisioningUI = {`), counts. **Counts: `1904765` 4133/247 → `ddf1b75` 4137/248** (+4/+1).
- **What changed (READ, `git diff 1904765 ddf1b75`):** `dropTokenOnLeave()` — if a token is held, null it, set `state.tokenDroppedOnLeave = true`, and
  `render()` when the container exists; `pagehide` → `dropTokenOnLeave()`; `pageshow` with `e.persisted === true` → `dropTokenOnLeave()`, then, if the flag
  is set, clear it and `setStatus('The SCIM token generated on this page was cleared when you left this page. It was never saved: generate a new one to
  continue.', 'error')`; **one listener pair per window** via `window.__nxProvisioningLeave` (a re-evaluation removes the previous pair). The module is
  loaded by `static/settings.html:863` and `static/first-run-setup.html:2307` (READ at `1904765`). The header comment cites "Tuesday's ruling (c)
  2026-09-26 (CLARIFICATIONS C-171)" ✔ (C-171 :1749-1754).
- **Drafter-READ, not in the READY:** (1) **`static/js/identifier-mask.js:115` already registers a `pageshow` handler** on the same window
  (`first-run-setup.html:14` loads it) — prior art (C-49) and a composition on first-run (row a11). (2) **The status is set with kind `'error'`**: the
  rendered colour of that line in both themes is a BRAND row (§11b). (3) A `pagehide` fires on EVERY unload — a same-tab navigation, a Reload, a tab close,
  and a bfcache entry — but **not** on a tab switch (`visibilitychange`). **The admin's real journey is "Generate → switch to the Entra portal tab → paste
  → come back → Save"; a clear on tab switch would break provisioning. Row a6 proves it does not.**
- **Builder's claims (READY :13-17):** 4 ids (LEAVE / RESTORE / RESTORE WITHOUT A PAGEHIDE / CONTROL), each with findability before the act; RED at `4a86c4a`
  (LEAVE, RESTORE, RESTORE WITHOUT A PAGEHIDE red; CONTROL green), GREEN 4/4 "with the fix (byte-identical to the committed file)", one hold
  `s85p-rd693-hold` 19:39Z, floor 0. **Full verify "PASS — 4137/4137 … across 248 suites" — drafter cross-read: `session-tools/s85p/rd693-hold.log` says
  `=== rd693 verify at 4a86c4a` ✔ with that VERDICT line ✔, i.e. on `4a86c4a` + an UNCOMMITTED fix the READY calls byte-identical to `ddf1b75`'s
  file. No full verify exists on the committed `ddf1b75` tree. (UNVERIFIED; §3 Q4 runs it.)**
- **C-68 note (READY :17):** "whichever of RD-692 and RD-693 merges SECOND re-runs `__tests__/rd692-provisioning-token-guards.test.js` by name." **This
  gate runs it on the merged tree regardless.**
- **Merge-tree claims (READY :18, RELAYED):** vs rd204, rd197, rd692 counts only; vs rd430, rd286 **`c219890`** (an OLDER RD-286 head), rd686 clean.
- **L-A1..L-A3 — NOT TESTED, VERBATIM (READY :22):**
  - **L-A1** *"a real back-forward cache (Chrome; the gate's R11)"*
  - **L-A2** *"first-run-setup.html's instance in a browser"*
  - **L-A3** *"other browsers' pagehide timing."*
- USER-VISIBLE (READY :11): after leaving and pressing Back, the panel shows no token and a new sentence of shipped copy. **Quote it from the page, both
  themes, both pages.**

### TARGET B — RD-286 (TIER 2 + browser leg) — ground and geometry guards; ruling (a): two deletions
- **Chain (MEASURED, `git log --format='%H %P' 1904765..1645c69`, 10 commits):** `e5f03b6dc46602b814a03fa53e4248d829235caa` (WIP spec, parent **`5f2683cd198067016d56a32ec4e1f46f4e45dcc6`**) →
  **`a09dd834e87e116e2fd37b07c2f0be7c40aa55aa`** (forward merge, parents `e5f03b6` `1904765`) → `58b20d3` (installed Chrome) → `30332b1` (two instrument fixes) → `c2d84ec`
  (RD-288 positive control) → **`fc0278d`** (RD-288 comment correction, comment only) → `1d58881` (ruling (a): four LOAD-BEARING markers) → `fa72606` (base th a
  restatement: 3 overrides) → **`c21989085772a08128b7dfe9d55d0ced388a1f8b`** (one-at-a-time inverse: one override) → **`1645c69`** (ruling (a) of C-172: the two deletions + the base th marker).
  Full shas in the launcher. **No counts change anywhere: `1645c69` 4133/247 = main** (the spec is outside verify, C-168 Q1).
- **Delta over `1904765`: 2 files** — `M static/css/dark-mode.css` (**+16/−25**), `A tests/e2e/rd286-ground-and-geometry.spec.js` (635).
- **dark-mode.css, READ in full (`git diff 1904765 1645c69 -- static/css/dark-mode.css`), three hunks:**
  1. **:1850-1870 → :1850-1863** — the 21-line "F5's SECOND INSTANCE — KNOWN, MEASURED, AND DELIBERATELY NOT FIXED" comment on `body.dark-mode .nx-sus-cls` is
     REPLACED by a 15-line "RD-288 — MEASURED, AND NOT A DEFECT AT THIS HEAD" comment (commit `fc0278d`; authorised by C-168 :1727 "the shipped dark-mode.css comment
     that asserted the defect is corrected on the RD-286 branch (`fc0278d`, comment only; the rule is byte-identical)").
  2. **:1913 and :1920** — the base `body.dark-mode .nx-sus-rank th` and `… td` `background-color` lines keep their VALUES (`#262626`, `#1c1c1c`); their comments become
     "LOAD-BEARING OVERRIDE (RD-286): without it the last header paints the light #f8f9fa in dark" / "… the cell paints the light #ffffff in dark". **The td marker
     is C-168's dark-classification ruling (a) (:1728, "4 dark rank-table rules … get an explicit load-bearing-override marker"); the th marker is the deviation
     ACCEPTED in C-175 (:1795).**
  3. **:1928, :1933 (at main)** — the two `background-color` declarations in `td:last-child` (`#1c1c1c`) and `th:last-child` (`#262626`) DELETED (C-172).
  **Drafter's comment-stripped declaration diff (python, `/\*[\s\S]*?\*/` removed, non-empty stripped lines, `difflib`): exactly `- background-color: #1c1c1c;` and
  `- background-color: #262626;`, nothing added** — the "two deletions only" of C-172 holds for DECLARATIONS; the remaining +16/−25 is comment text. The launcher
  re-proves this (guard 84). **The READY's "PLUS one comment change" (READY :17) is relative to `c219890`, not to main — the other two comment changes came in
  earlier commits under C-168; all three are accounted.**
- **Colour text the delta adds (READ):** `#262626`, `#1c1c1c` (unchanged values on changed lines), and **`#f8f9fa`, `#ffffff` inside the two new marker COMMENTS** in
  `dark-mode.css`. The brand-token-conformance test "resolves EVERY colour in dark-mode.css" (RD-686's own words) — **so whether its extractor strips comments
  decides whether two LIGHT values now sit in the dark corpus.** The builder's verify at `1645c69` is green (`rd286-verify.log` ✔ 4133/4133, 247) — **explain the
  green (C-40): comments stripped, or the values resolve? Row k3.**
- **Builder's claims (READY :8-22):** population 29 "stated, not inherited" claims bound rule by rule to the live CSSOM; guard 2 light and dark 0 mismatches; guard
  1: 78 opaque members per theme, 0 findings, F5 control → 4 findings, restored → 0; inverse per rule: base th 6 members 2 changed, base td 18/18, control (a td copy
  in another sheet) → exactly `body.dark-mode .nx-sus-rank td` reported dead; RD-288: 0 px, control 4784/4783 inside, 0 outside; **RD-286 (a) pixel-neutral: BEFORE
  rebuilt IN-PAGE by re-inserting the two declarations verbatim at the END of dark-mode.css; before==after TRUE both themes; positive control (base td ground → red)
  seen TRUE; restored rule text identical TRUE.** Spec 18/18 in Chrome 153 (`session-tools/s85p/rd286-hold.log` ✔ "18 passed (50.5s)"); screenshots BEFORE
  `session-tools/s85p/rd286-evidence/c219890/…` AFTER `…/1645c69/sustainability-{light,dark}.png` (present ✔). Full verify 4133/4133, 247 ✔.
- **Drafter-READ, the method gap in the pixel-neutral arm:** the BEFORE state is a RECONSTRUCTION (two declarations appended at the END of the sheet, not at their
  original position, in a new rule object). Same specificity and value, so it is probably equivalent — **but no arm compares against the REAL base (main's
  `dark-mode.css` blob `49e63a6`) rendered in its own tree. Row p2 does.**
- **Instrument fixes disclosed (READY :24-28):** `30332b1` (viewport coordinates; mis-credited selectors), `c2d84ec` (positive control before a zero), the one-at-a-time
  inverse, the override count "4 → 3 → 1 → 2". Carry them.
- **The builder's surface:** `scripts/qa-surface-up.sh <sha> <port>` — **READ at `1645c69` :159-211: it runs `git -C "$REPO" worktree add --detach
  "$PROJECT/qa-worktrees/$SHA"` in the NexusAI repo.** You may NOT run it as-is (C-28, §14). Stand an equivalent surface from YOUR archive tree: read its seed
  steps (:162-) and reproduce them against your own DATA_DIR; say what you reproduced and prove the seed landed (the Sustainability tab renders members — the
  spec's own "tab renders members" cell).
- **L-B1..L-B5 — NOT TESTED, VERBATIM (READY :32):**
  - **L-B1** *"guard 3 (RD-701)"*
  - **L-B2** *"the empty-state members (RD-289; reported UNVERIFIED per run)"*
  - **L-B3** *"browsers other than Chrome"*
  - **L-B4** *"viewports other than 1280x900."*
  - **L-B5** *"Playwright's bundled Chromium is absent here, so the spec uses installed Chrome, as RD-490 does."*
- **Not covered (C-168 :1724):** a defect either guard finds in `static/css/sustainability.css` (outside lane 4) — STOP that part and name it to Tuesday.

### TARGET C — RD-204 (TIER 2) — what the vendor stand-in does not paint
- **Chain (MEASURED, 8 commits):** `72cd3db` (off **`7c47ec467f585e9db5daf3a82cdb96deae0b1e7a`**) → `dfc92b4` (merge `11666d3`) → `cbe0243` (pins) → `a19559f` (merge `5f2683c`) → `82798e3` (counts
  4052/243) → `8bb4e73` (merge `748cece`) → **`83e5a1b274a37c0a8e19d02ffa01e2ad1941ee4b`** (merge `1904765`; its counts file is a PLACEHOLDER `{tests: 1, suites: 1}`, MEASURED) → **`fe47bb4`**
  (**counts only**: `git diff --name-only 83e5a1b fe47bb4` = the counts file).
- **Delta over `1904765`: 5 files, +1405/−3** — `M __tests__/helpers/dom.js` (+88/−0, appended after :684), `M __tests__/helpers/vendor-surface.css` (+39/−0, all
  comments per the READY), `A __tests__/rd204-bootstrap-5.3.0-painting.json` (1133), `A __tests__/rd204-vendor-coverage.test.js` (142), counts.
  **Counts: `1904765` 4133/247 → `fe47bb4` 4148/248** (+15/+1).
- **What changed (READ at `fe47bb4`):** `paintingRulesOf(cssText)` (comment-stripped; `fg` = a `color` declaration, `bg` = `background`/`background-color`; values
  matching `PAINT_NONE = /^\s*(transparent|none|0 0|0|inherit|initial|unset|currentcolor)\s*(!important)?\s*$/i` do not count); `uncoveredVendorNodes()` walks each visible
  text node up to the first opaque computed ground and reports every Bootstrap painting selector that matches an element whose same KIND no excerpt rule covers.
  The painting list (224 selectors; `paintingRules: 285`, `skippedSelectors: 122`) was derived ONCE by **`session-tools/s84p/rd204/derive-families.js`** (on disk,
  2,416 bytes, OUTSIDE the repo) from `session-tools/s84p/rd204/bootstrap-5.3.0.min.css` — **drafter: its sha384 (base64) = `9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM`
  = the list's `sha384` field = the pages' integrity attribute ✔ (openssl, READ).**
- **Drafter-READ: TWO DIFFERENT readings of "paints".** The committed list counts `--bs-*color*` custom properties as fg and `--bs-*-bg*` / `--bs-bg` as bg
  (derive-families.js :4-6), **but `paintingRulesOf` — which judges the EXCERPT's coverage — counts only literal `color` / `background` / `background-color`.** An
  excerpt rule that paints through a `--bs-*` custom property would NOT count as covering. **That errs toward reporting (over-count), and it is the reading the
  READY's gate ask points at:** "check the transparent-vs-opaque reading of paintingRulesOf matches Bootstrap's own semantics." **Measured in the list (READ):**
  `.btn` `{fg:true, bg:true}` although Bootstrap 5.3's `.btn` ground is `var(--bs-btn-bg)` = `transparent` by default; `.btn-close` `{fg:true, bg:true}` although its
  "ground" is an SVG icon (`--bs-btn-close-bg: url(…)`; the derivation excludes only properties NAMED `*icon*`); `.navbar-dark` `{fg:true, bg:false}`; `.badge`
  `{fg:true, bg:false}`; `.bg-primary` `{fg:false, bg:true}`. **And `currentcolor` is treated as painting NOTHING — for `background-color: currentcolor` that is
  wrong (it paints the text colour).** Rows c5-c9.
- **Builder's claims (READY :20-37):** 15 ids green at `fe47bb4`; pins feedback-admin 24, first-run-setup 49/49, index 76/76, login 2, settings 155/155; **T1** (@covers
  `.btn-danger` removed) → BOTH WAYS red, 14 green; **T3** (login.html gains `navbar.bg-dark`) → login pin red 2 → 3; **T2** (excerpt gains `.btn { background-color:
  transparent }`) stayed 15/15 — "Resolved, not reported (C-103) … The tamper did not tamper"; **T2b** (the same tamper OPAQUE, anchor asserted, parsed rule
  printed `{"selector":".btn","fg":true,"bg":true}`) → ALL 8 pins red: feedback-admin 24→16, first-run-setup 49→13 both, index 76→47 both, login 2→1, settings 155→131
  light / 140 dark. Proof holds `s85p-rd204-proof-verify` at `a19559f` (15/15; T1; T3) and `s85p-rd204-t2b` at `83e5a1b` — **drafter: `session-tools/s85p/rd204-hold.log`
  ✔ (verify at `a19559f` 4052/4052, 243) and `rd204-t2b.log` ✔ present; the 4148/248 verify on `83e5a1b`'s tree is RELAYED (not found in those two logs).**
- **Forward-merge claim (READY :37):** "C-112: every `__tests__` file byte-identical to a parent, 0 absent." RELAYED.
- **L-C1..L-C4 — NOT TESTED / LIMITS, VERBATIM (READY :44-48):**
  - **L-C1** *"jsdom only: this counts text nodes on Bootstrap-painted elements the excerpt does not cover; it does not measure contrast, and nothing here drives a real browser."*
  - **L-C2** *"Only pages that CDN-link Bootstrap 5.3.0; dark only for pages that link the dark sheet."*
  - **L-C3** *"The list is Bootstrap 5.3.0's. A version bump needs a re-derivation, and the PROVENANCE cell fails until it is done."*
  - **L-C4** *"The pins are a ratchet, not a target: 155 unmeasured nodes on settings is the measured state, not an acceptable one."*
- Gate asks (READY :50): **re-run T1/T2b/T3 against the pins, and check the transparent-vs-opaque reading of `paintingRulesOf` against Bootstrap's own semantics** — §6.

### TARGET D — RD-197 option (b) (TIER 2) — emphasis colours only on their notice ground
- **Chain (MEASURED, 7 commits):** `7d87d74` (off `7c47ec4`) → `3f91242` (merge `11666d3`) → `a08ca38` (per-family reach) → `9c742fa` (merge `5f2683c`) → `f4dd74d` (counts
  4046/243) → **`cd589e098cbccf6351fb19b7159d61fe171aa63a`** (merge `1904765`; counts PLACEHOLDER `{1,1}`, MEASURED) → **`43e729c`** (**counts only**).
- **Delta over `1904765`: 2 files, +155/−3** — `A __tests__/rd197-emphasis-on-notice-ground.test.js` (152), counts. **Counts: 4133/247 → `43e729c` 4142/248** (+9/+1).
- **What it is (READ at `43e729c`):** E = the dark `-emphasis` tokens below AA (`gen.AA_TEXT`) on `surface-raised`, COMPUTED from `scripts/derive-brand-tokens.js`
  (blob `d94423a`, identical at main and every head, MEASURED); every page that links the dark sheet (`helpers/dark-corpus.js derivePagesLinkingDarkSheet`) is rendered
  dark and every visible text node painted in an E value must sit on its own family's `-subtle` ground. Limits in its header: default render state only; unresolved
  nodes counted, not scored; RD-204's stand-in gap applies.
- **Builder's claims (READY :9-20):** E = info-emphasis 4.32, success-emphasis 4.46, danger-emphasis 4.17; CLEAN 9/9 (38 E-coloured nodes across 4 dark pages —
  chart-details, first-run-setup, index, settings; 19 unresolved counted); **M1** (info notice ground → `#262626`) RED on first-run-setup, 30 sites; **M2** (every
  danger notice ground `#2b1c1d` → `#262626`) stayed GREEN — **ACCEPTED LIMIT**; proof `session-tools/s84p/rd197-proof.log` ✔ (present, 39,601 bytes) at `3f91242` =
  RD-197 + main `11666d3`; "STILL VALID AT THE MERGED HEAD (C-68)" by a READ of the files it reads between `11666d3` and `1904765` (only RD-428's focus rules);
  full verify 4142/248 at `cd589e0` (`session-tools/s85p/rd197-mverify.log` present).
- **L-D1..L-D3 — NOT TESTED / LIMITS, VERBATIM (READY :31-32, :17):**
  - **L-D1** *"success and danger emphasis on RENDERED pages: no reachable danger action exists (RD-687, first-run's danger branches have no caller). The success action is loading first-run with a saved data source (loadDataSources, first-run-setup.js:2322 at S84P's read), which this jsdom run does not drive. A browser leg that drives an error and a success state is where those belong."*
  - **L-D2** *"jsdom only; nodes jsdom cannot resolve are counted, not scored."*
  - **L-D3** *"M2 (every danger notice ground #2b1c1d -> #262626): stayed GREEN. ACCEPTED LIMIT (your ruling 2025-09-25T18:21:26Z, option (a)): no danger-emphasis text renders by default, so the pages never reach that family; the probe cells cover the shape."* (ruling date corrected to **2026**-09-25 by the correction mail).

### TARGET E — RD-686 (+ RD-694 items 1-3) (TIER 2) — words only
- **Chain (MEASURED):** ONE commit `8962a14`, parent `1904765`. **Delta: 2 files, +54/−25** — `M docs/BRAND.md` (+35/−19, §8 rule 3 only, :558-600 at head),
  `M __tests__/helpers/css-colors.js` (+19/−6, the JS-corpus header comment at :246-275 only). **Counts unchanged 4133/247** (`rd686-verify.log` ✔ 4133/4133, 247).
- **The claims the words now make (READ, `git diff 1904765 8962a14`), each a measurement you re-derive with YOUR OWN probe — §8:**
  - **E1** dark-mode.css: `brand-token-conformance.test.js` resolves every hex, every `rgba()` triple (alpha ignored), every `--*-rgb` triple; `hsl()` recorded UNCONVERTED
    and fails by name; "3 functional sites" (READY :13).
  - **E2** light stylesheets: only token values' OCCURRENCE COUNTS are pinned; **125 distinct hex values that are not token values (of 147 distinct) and 96
    `rgba()`/`hsl()` sites** are read by no assertion (BRAND.md; READY :14).
  - **E3** the e2e brand-pairing ratchet "sees off-guide colours only in rendered pairs, outside `npm run verify`" (`tests/e2e/brand-pairing.spec.js`,
    `brand-pairing-ratchet.json`, `brand-offguide-ratchet.json` exist at `1904765`, READ by name).
  - **E4** JS gate: hex KEEPS alpha — `#ba5ebaff` stays, `#b5bf` → `#bb55bbff`, `#0096d680` fails; `rgb()`/`rgba()` alpha ignored.
  - **E5** runtime-built `` `hsl(${h}, …)` ``, `` `rgb(${r}, …)` `` and a CONCATENATED `'rgb(' + r + …` ARE read, as unresolved (fail); `'#' + hex` and
    `['#','00','96','d6'].join('')` are NOT read.
  - **E6** a private class field/method `this.#add` reads as `#aadddd`; an ID selector `'#face'` reads as a colour; "no current site is such an identifier".
  - **E7** named colours (`'white'`) are not read; only `static/js/*.js`.
  - **E8** the closing sentence: "a green brand gate means 'every colour in dark-mode.css is a token, the light sheets' token counts are unchanged, and no
    off-guide colour literal in static/js beyond the recorded debt', not 'on brand'."
- **Drafter-READ, WRONG in the READY:** READY :23 says "re-run the probe (**the snippets are in the commit message**)". **They are not** — `git log -1
  --format=%B 8962a14` carries the CLAIMS (the values above) and no code. **You write your own probes over `extractJs`/the CSS extractor; the claims are
  your oracle.** (WRONG list item 5.)
- **L-E1..L-E2 — NOT TESTED / NOT IN THIS BRANCH, VERBATIM (READY :21, :23):**
  - **L-E1** *"NOT TESTED: this is prose. The reviewer's check is to re-run the probe (the snippets are in the commit message) and compare it to the words."*
  - **L-E2** *"NOT IN THIS BRANCH: RD-694 item 4 (the READY's per-ticket split vs the manifest's joint ownership) and the fixture `_about` text."* (→ optional H.)
- **New ticket named:** RD-704 (Medium) — the light-corpus gate is a brand call; **not in scope.**

### TARGET F — RD-692 (TIER 2) — the two RD-428 F2 guards
- **Chain (MEASURED):** `078c8c0` (WIP, parent `1904765`, the first hold RED on clean code for SAME MODE — disclosed) → **`3dcd1c0ff8b0505f47b5288917b4732089b5c63a`** (SAME MODE
  corrected) → **`4580829`** (**counts only**). **Delta: 2 files, +151/−3** — `A __tests__/rd692-provisioning-token-guards.test.js` (148), counts. **Counts: 4133/247 →
  `4580829` 4138/248** (+5/+1). It reads `static/js/entra-provisioning-ui.js` from disk (`UI_SRC`, :31) — **the file RD-693 changes.**
- **Builder's claims (READY :8-21):** 5 ids (the 409 and 428 titles are built in a loop — your id list comes from jest's JSON, never a grep); findability before
  each act; one hold `s85p-rd692-hold` at `3dcd1c0`: CLEAN 5/5; **M-A6** (the 409/428 clear deleted) → 409, 428, CONTROL red; **M-A10** (`var changed = true`) →
  SAME MODE red; anchors matched once; restored, hash equal. Full verify 4138/4138, 248 ✔ (`rd692-hold.log`, at `3dcd1c0` = counts-only-different from `4580829`).
- **DISCLOSED (READY :21):** the first hold (`078c8c0`) was red on CLEAN code; one jest-spawned server (pid 79522, orphaned to pid 1) was "stopped by pid, and the
  floor was back to 0 before the re-run." **Carry it** (it predates C-174 and names a pid, not a pattern ✔).
- **L-F1..L-F2 — NOT TESTED, VERBATIM (READY :27):**
  - **L-F1** *"jsdom only (the gate's R8 already drove the conflict clear in a browser)"*
  - **L-F2** *"a real server's 409/428 bodies are stubbed with the shapes the component branches on (status + errorCode)."*

### File overlap — disjoint except the counts file (MEASURED, READ ONLY)
Name sets over `1904765` (every head's merge base): A `ddf1b75` (3), B `1645c69` (2), C `fe47bb4` (5), D `43e729c` (2), E `8962a14` (2), F `4580829` (2).
Pairwise `comm -12`: **A∩C, A∩D, A∩F, C∩D, C∩F, D∩F = `scripts/verify-expected-counts.json` only; every pair involving B or E = NOTHING.** (Optional G
`9ba6f1d`: `rd430-response-form-removed.test.js`, `static/js/settings.js`, `static/settings.html` — disjoint from all six, and **its counts file is main's
4133/247 although it adds a test file** (§10); optional H `1d457ce`: the fixture only — disjoint.)
- **Merge-tree: NOT run by the drafter** (the commission forbids the drafter a `merge-tree --write-tree`, even with a scratch object dir). **The builders' claims,
  RELAYED:** RD-693 READY :18; RD-286 READY :30 (all clean vs rd204 `fe47bb4`, rd197 `43e729c`, rd430 `9ba6f1d`, rd686 `8962a14`, rd692 `4580829`, rd693 `ddf1b75`);
  RD-204 READY :32-35 (vs RD-197 **`cd589e0`**, an older RD-197 head; vs rd286 **`a09dd83`**, an older RD-286 head); RD-197 READY :22-26 (same older heads); RD-692
  READY :23 (vs rd286 **`fc0278d`**); **RD-686 READY :17 "not run yet"**. **Only RD-286's claim is against the current heads. §11 Q1 measures every pair.**
- **C-112's condition (predicted):** no file other than the counts file is touched by two members, so **every `__tests__` file of the merged tree should be
  byte-identical to a parent** → the byte-identity shortcut MAY apply — **only once you have measured it (§11 Q4)**; it never replaces the C-68 semantic
  re-runs below.
- `package-lock.json` blob `9064763` (full `906476350431e2ecb3c21070a25c64b1702c1aa8`), `package.json` `cdb1168`, `playwright.config.js` `fb3017b`, `static/css/tokens.css`
  `de6e0fe`, `scripts/derive-brand-tokens.js` `d94423a` at `1904765` and all six heads (and G, H) — MEASURED. **No member touches a token value.**
- `__tests__` at `1904765`: **289 files**; merged predicted **294** (+ rd693, rd204 test, rd204 json, rd197, rd692).

### THE UNMEASURED INTERACTIONS — git sees none of them as a conflict; each is a required measurement (§11 Q6, §11a, §11b)
- **U1 — 693 × 692 on the provisioning module.** RD-692's cells evaluate `entra-provisioning-ui.js` per test in jsdom and fire no page events; RD-693 adds a
  window-level listener pair and a `window.__nxProvisioningLeave` global. **Does any jsdom teardown or `window.close()` dispatch `pagehide` and clear a token
  mid-cell? Does the "one pair per window" replacement hold across rd692's per-test re-evaluations?** Re-run rd692 BY NAME on the merged tree (READY-693 :17).
- **U2 — 693 × the existing RD-428/RD-409-410/RD-388 cells on the same module** (`entra-provisioning-ui`, `entra-provisioning-revoke-ui`, `rd372`, `rd388`,
  `rd409-410`, `rd428-scim-token-mode-change`, `dark-ground-luminance`, + rd692, rd693 — census `git grep -l entra-provisioning-ui ddf1b75 -- __tests__` = 8 cell
  files + the rd200 fixture). Every one on the merged tree, per-file counts.
- **U3 — 693 × RD-705 (batch 5a, lane 1).** With `Cache-Control: no-store` on the HTML, Chrome 153 may refuse bfcache entirely — then RD-693's `pageshow
  persisted` branch is unreachable in the product, and the admin who presses Back sees a fresh page with **no** explanation line. Not a defect of either
  ticket; a composition to DESCRIBE (§11a b9).
- **U4 — 693 × identifier-mask on first-run-setup** (`static/js/identifier-mask.js:115` `pageshow` handler; `first-run-setup.html:14` and `:2307` load both): two
  `pageshow` listeners on one window — order and effect in a real bfcache restore (§11a a11).
- **U5 — 286 × 197 and 286 × 204 on the dark sheet.** RD-197 renders index (the Sustainability tab lives in `index.html:1003`) dark; RD-204's index pins are 76/76.
  RD-286 removes two grounds whose VALUES equal the base rule's, so the computed ground of every `.nx-sus-rank` `:last-child` cell should be unchanged — **predicted
  no change to either; measure (rd197 and rd204 by name on the merged tree, index dark).**
- **U6 — 286 × the brand readers.** `dark-mode.css` is read by 29 `__tests__` files (census at `1645c69`); the new marker COMMENTS carry `#f8f9fa`/`#ffffff` (k3).
- **U7 — 686 × every brand reader.** `docs/BRAND.md` is read by NINE cell files (`brand-chrome-contrast`, `brand-chrome-gradient-stops`, `brand-md-accent-count`,
  `brand-token-conformance`, `costs-header-solid`, `light-active-tab-chrome`, `muted-4-16-attribution`, `primary-button-chrome`, `rd200-js-colour-corpus`; census
  `git grep -l BRAND.md 8962a14 -- __tests__`) and `css-colors.js` by FOUR (`brand-chrome-gradient-stops`, `brand-token-conformance`, `css-colors-stripper`,
  `rd200-js-colour-corpus`) — **a doc edit can move a cell that counts or quotes the doc.** The builder's full verify is green; name the 10 by file on the merged tree.
- **U8 — 204 × 197 on `helpers/dom.js`** (204 appends exports only; 197 imports `renderPage`, `visibleTextNodes`, … from it): the 33 importers (census at
  `fe47bb4`) via the merged full verify, and rd197 by name.
- **U9 — OPTIONAL G (RD-430) × 204 / 197 / 693 on `settings.html`.** Removing the Response Guidelines form removes Bootstrap-painted nodes from settings: **RD-204's
  settings pins (155/155) are PREDICTED to move — and C-175's re-pin grant covers ONLY the three pins in `dom-harness.test.js` and `jsdom-instrument-limits.test.js`
  ("Not covered: any other pin").** If G is included and an rd204 settings pin reddens on the merged tree, that is a **C-57/C-97 STOP to NAME and a QUESTION to
  Tuesday**, never a re-pin by you. RD-197 renders settings dark (its E sweep's corpus shrinks); RD-693's panel lives on the same page.

### The proposed MERGE ORDER, the predicted counts, and each merge's C-68 re-run set (census at `1904765` / heads, `git grep -l`, scoped to `__tests__`)
The order (a proposal — Tuesday decides; the gate proves order independence in §11 Q3): **(1) RD-686 → (2) RD-286 → (3) RD-204 → (4) RD-197 → (5) RD-692 → (6) RD-693**
(optional: **G RD-430 after RD-204 and RD-197** — C-166 :1705 "Built … after RD-204 and RD-197 (Tuesday's order)"; **H RD-694 item 4 after RD-686**).
Why: the two members that do not touch the counts first (clean); RD-204 before RD-197 (both jsdom brand sweeps; 204 extends `dom.js` that 197 imports); RD-692 before
RD-693 so that RD-693, the one PRODUCT change to the module, merges SECOND and carries rd692's by-name re-run (READY-693 :17), and so RD-693 (tier 1) lands onto a
tree that already guards the clears it must not break.

| step | merge | predicted conflict | predicted counts after (arithmetic, M0 = `1904765`) | C-68 re-run set — by NAME, per-file counts |
|---|---|---|---|---|
| 1 | RD-686 → M0 | none (no counts change) | 4133/247 | the 10 BRAND.md / css-colors.js readers (U7) |
| 2 | RD-286 | none | 4133/247 | the 29 `dark-mode.css` readers (re-census; helpers excluded from the suite count) + **the rd286 spec in the browser (§11a)** + `muted-4-16-attribution` (reads `.nx-sus-rank`) |
| 3 | RD-204 | none if you take the counts side at step 1-2 (4133); **predict it** | 4148/248 | the `vendor-surface.css` readers (`badge-bg-info-contrast`, `chart-details-dark`, `dark-ground-luminance`, `dom-harness`, `sustainability-dark-mode`, `rd204`) + the 33 `dom.js` importers via the full verify |
| 4 | RD-197 | counts | 4157/249 | rd197 + rd204 + the step-2 dark readers that render dark pages |
| 5 | RD-692 | counts | 4162/250 | the 8 `entra-provisioning-ui` cell files (U2) |
| 6 | RD-693 | counts | **4166/251** | step 5's set + rd692 BY NAME + rd693 + `identifier-mask` (U4) |
Arithmetic: 4133 + 0 + 0 + 15 + 9 + 5 + 4 = 4166; 247 + 1 + 1 + 1 + 1 = 251. **Re-run every census yourself; add any file it finds that the drafter missed.**
Optional: G adds its own delta (`rd430-response-form-removed` + the C-175 re-pins; its re-pinned counts unknown at drafting) → re-run `dom-harness`,
`jsdom-instrument-limits` (C-175 condition 3), rd204, rd197, and every `settings.html` reader (26 files at `1904765`); H adds 0/0 → re-run `rd200-js-colour-corpus`.

### How to build your trees
- **No worktree is created in the NexusAI repo, and you never work in its `2_Project_Files` checkout (C-28).** In that repo use ONLY read verbs: `show`, `log`,
  `diff`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `grep`, `ls-remote`, `archive`, `count-objects`. Never `fetch`, `pull`, `push`, `checkout`, `worktree`,
  `commit`, `stash`, `gc`, `clean`, or `merge-tree --write-tree` without a scratch `GIT_OBJECT_DIRECTORY` of your own. **Never run `scripts/qa-surface-up.sh`
  (it adds a worktree to the NexusAI repo).** **If a sha is missing from the local object store, it is UNMEASURED — never fetch.**
- **Head trees:** `git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/qa-trees/batch6.XXXXXX/>`, git-indexed where a suite needs it (**prove the population equals
  `git ls-tree -r` at the head**).
- **The merged tree:** in **your OWN scratch clone** (`git clone --shared --no-checkout <repo> <your own dir>`), §11.
- **Each tree is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree for a clean arm; `batch6`-prefixed
  directories only. **Nothing in another gate's `qa-trees/*` (batch-3's, batch-4's, batch-5a's), the builders' `worktrees/`, `qa-worktrees/` or `session-tools/` is run
  in — read only.**
- `node_modules`: an APFS clone (`cp -c -R`) of the newest gate tree you trust, **after proving** `package-lock.json` is blob `9064763` there too; a real directory,
  never a symlink. `@playwright/test` comes from it; the browser is the installed Google Chrome (`channel: 'chrome'`; L-B5).

## 2. Why these tiers, and who is waiting
- **RD-693 TIER 1:** a SCIM bearer token is the whole perimeter of `/scim/v2`. **Any state in which, after the admin leaves the page (navigation, Back,
  Forward, Reload, tab close), the shown-once token is on screen, in page memory, in any browser storage or cache, in the console, or on the wire, is a Major;
  a bfcache restore showing it is a Major; the token lost on a TAB SWITCH (the paste-into-Entra journey) is a Major (a product regression); a silent loss with
  no explanation where the design promises one is a Minor; a cell that cannot fail on the thing it claims is a Major (C-40).**
- **RD-286 TIER 2 + browser:** **any pixel of the Sustainability tab that moves between main and `1645c69` in either theme (outside a declared dither
  band you measure) is a Major (C-172 says "moved no pixel"); a guard that goes green over an empty or shrunken population is a Major; a declaration change
  beyond the two deletions is a Major; a false comment (a "LOAD-BEARING" override whose removal changes nothing) is a Minor.**
- **RD-204 / RD-197 / RD-692 TIER 2 (tests only):** a cell that cannot fail on the thing it claims (C-40) is a Major; a pin that moves under a change it claims
  to guard and stays green is a Major; a flake is a Minor; a mis-reading of Bootstrap semantics that UNDER-reports is a Major, one that over-reports is a Minor.
- **RD-686 TIER 2 (words):** **a sentence the measurement contradicts in the UNSAFE direction (the doc says the gate reads something it does not) is a Major; in
  the safe direction (the gate reads more than the doc says) a Minor; a number off by any amount is a Minor.**
- **Brand (all):** a colour a change introduces that does not resolve to a style-guide token = **OFF-GUIDE = Major**; a palette change = STOP (Kam's).
- **The queue.** NexusAI builder seats live at drafting (re-read 09:31:51 AEST): **M** (claude `62649`, pane `%19`), **N** (claude `9959`, pane `%21`), **P** (claude `20317`,
  pane `%22`, the lane-4 seat that built all six and is the merge author); the batch-3 and batch-4 gates live (`36118` %23, `40285` %24). **The jest lock was held by
  `s86m-rd594-hold` since 23:17:43Z with ~11 tickets queued** (read-only `cat` of the owner file and `ls queue-jest/`). Expect waits; never jump.

## 2a. LEGITIMATE SHAPES — required measurements, row by row, base and head(s) in the same window
Every row is either a CHECKER row (a guard/pin/doc claim) or a real-browser product row. **Expected verdict per the clause; a row whose expected verdict and
clause disagree is a finding against this brief — say so.**

**A — RD-693: the token and the admin's real journeys. REAL BROWSER (§11a), loopback server from YOUR tree, fresh DATA_DIR, open mode (C-02), keyboard
and page actions only. Trees: base `1904765`, head `ddf1b75`, MERGED; plus M0 if it carries RD-705 (b9). Every row records: status-line text, token in
`outerHTML` (in-process equality, never printed), token in page memory (`NexusProvisioningUI` state via an evaluate that returns a BOOLEAN), `pageshow.persisted`
and `notRestoredReasons`, every request (URL, headers, body), every storage kind.**

| row | shape — ordinary form | at `1904765` | at `ddf1b75` / merged | clause | predicted-by |
|---|---|---|---|---|---|
| a1 | Settings > Provisioning > SCIM > Generate > navigate to another NexusAI page > **Back** (the batch-2 R11) | **restored, token on screen + in memory** (A-N5) | restored (`persisted:true`), **token absent from DOM and memory; status = the RD-693 sentence verbatim** | pageshow persisted | builder; batch-2 :110 |
| a2 | … > **Forward** after a1 (return to the other page, then Forward again to Settings is not the shape — do: Generate, Back to the PREVIOUS page, Forward to Settings) | restored with token? | token absent; sentence shown | same | drafter |
| a3 | Generate > **Reload** (F5) | cleared (a fresh page) | cleared; **no** sentence (a fresh load has no flag) | pagehide + fresh state | drafter |
| a4 | Generate > navigate away > Back **with bfcache BLOCKED** (e.g. an `unload` listener planted in-page, or DevTools disable) | fresh page, no token | fresh page, no token, no sentence | persisted false | drafter |
| a5 | Generate > **Save (SCIM)** > navigate away > Back | Save already cleared the token | same, and **no** sentence (the flag is set only when a token was held) | `if (!state.generatedToken) return` | drafter |
| a6 | **Generate > switch to ANOTHER TAB (a second page in the same context) for 10 s > switch back** — the paste-into-Entra journey | token still shown | **token STILL SHOWN, in memory, no sentence** — a clear here is a Major | no pagehide on visibilitychange | drafter — **the regression row** |
| a7 | Generate > open another NexusAI page in a NEW tab from a link (Cmd/Ctrl+click) | kept | kept | no pagehide | drafter |
| a8 | Generate > ArrowLeft to Graph (token kept, not shown — RD-428) > navigate away > Back | restored with the token in memory (batch-2 R11 head column) | **memory null**; sentence shown; arrow back to SCIM shows NO token | pagehide clears regardless of mode | drafter |
| a9 | Generate > close the TAB, reopen Settings in a new tab | fresh | fresh | — | drafter |
| a10 | **first-run-setup.html's instance** (L-A2): the same a1 shape if the page mounts the panel; if it does not mount it, say so with the evidence (no `#rd135-provisioning-mount` / no container) | measure | measure | :2307 | builder (declared) |
| a11 | first-run-setup a1 with `identifier-mask.js`'s own `pageshow` handler live (U4): a masked identifier restored AND the token cleared, both | measure | measure | two listeners | drafter |
| a12 | **a1 with the wire/storage audit:** every request during Generate → leave → Back; `localStorage`/`sessionStorage`/IndexedDB/Cache Storage/cookies after each step; console lines | token only in the `/scim-token` response | same; **token in no request after Generate; in no storage; in no console line** | batch-2 Q5b | drafter (positive control: the audit FINDS it in the mint response) |
| a13 | the sentence's rendered colour and ground, light and dark, settings and first-run (the `'error'` kind) | — | resolves to a style-guide token; AA on its ground | BRAND.md §8 | drafter (→ §11b) |
| a14 | two consecutive restores: a1, then navigate away and Back again | — | second restore: no token (none to clear); **sentence absent or present — say which and whether that is honest** | flag cleared on first restore | drafter |

**B — RD-286: the Sustainability tab and the spec. REAL BROWSER, both themes, 1280×900 (L-B4) AND one extra viewport (e.g. 1024×768).**

| row | shape | at `1904765` | at `1645c69` / merged | predicted-by |
|---|---|---|---|---|
| p1 | the spec `tests/e2e/rd286-ground-and-geometry.spec.js` on YOUR surface from each tree | (spec absent at main — run the head's spec against main's CSS in a SCRATCH tree = the head tree with `dark-mode.css` replaced by blob `49e63a6`) | **18/18** | builder |
| p2 | **independent pixel compare:** screenshot clips of both `.nx-sus-rank` tables (and the whole tab) at main vs head, same seed, same viewport, both themes, determinism precondition (the same clip twice byte-identical) first | — | **0 differing pixels**, beside a positive control (a planted 1-px ground change IS seen) | drafter — **the REAL base, not the in-page reconstruction** |
| p3 | the in-page reconstruction's BEFORE (two declarations appended at the sheet's END) vs the REAL base render (p2) | — | identical? | drafter |
| p4 | per-rule inverse re-derived: remove base th alone / base td alone / each `:last-child` alone | — | th, td change their grounds; the two `:last-child` rules are gone | builder (C-172) |
| p5 | guard 2 with the two `:last-child` declarations RE-INSERTED at their original position (a scratch copy of `dark-mode.css`) | — | the claimant population returns to its `c219890` shape — say what guard 2 and the inverse report | drafter |
| p6 | guard 1 control (F5 re-declared) and guard 2 control (one stated ground mutated) | — | red, then green on restore | builder |
| p7 | the RD-288 arm: chips transparent → 0 px; control red → ~4,780 inside, 0 outside | — | same | builder (C-168) |
| p8 | a stated-ground CLAIM comment renamed to a selector that matches nothing (scratch copy) | — | "an unbound claim fails" — red | builder (READY :8) |
| p9 | the population count (29) and the "tab renders members" precondition on YOUR seed | — | 29; members > 0 | builder |
| p10 | light theme screenshots main vs head | — | identical (the change is dark-only) | C-168 Q3 conditions |

**C — RD-204: the reading of "paints" (pure node over the committed list and the fetched copy; jsdom for the pins).**

| row | shape | expected | predicted-by |
|---|---|---|---|
| c1 | T1 — `@covers .btn-danger` removed from `vendor-surface.css` | BOTH WAYS red; 14 green | builder |
| c2 | T2b — excerpt gains `.btn { background-color: #ffffff }` (OPAQUE) | ALL 8 pins red, with the builder's numbers | builder |
| c3 | T3 — `login.html` gains a `navbar.bg-dark` element (scratch copy) | login pin red 2 → 3 | builder |
| c4 | T2 — `.btn { background-color: transparent }` | 15/15 green — **and say whether that is RIGHT by Bootstrap's semantics** (a transparent ground paints nothing) | builder (C-103) |
| c5 | `.btn` in the committed list: `{fg:true, bg:true}` while Bootstrap 5.3's `.btn` ground is `var(--bs-btn-bg)` = transparent | **over-report** — how many reported nodes on the 5 pages are `.btn` bg-only? | drafter |
| c6 | `.btn-close` `{bg:true}` — its `--bs-btn-close-bg` is an SVG `url()` (an icon), not a colour | over-report — census | drafter |
| c7 | an excerpt rule painting through a custom property (`.x { --bs-btn-bg: #fff }`, scratch) | **NOT counted as covering** by `paintingRulesOf` — the asymmetry; say which direction it errs | drafter |
| c8 | `background-color: currentcolor` in an excerpt rule (scratch) | `PAINT_NONE` says "nothing" — Bootstrap/CSS says it PAINTS (the text colour) — **under-report?** | drafter |
| c9 | a painting selector with a pseudo-class (`.btn:hover`) or attribute (`[data-bs-theme=dark] .x`) | skipped (declared; LOWER bound) — count the 122 skipped and name the families | builder (declared) |
| c10 | PROVENANCE: the list's `sha384` = every page's integrity attribute; re-derive the list with a COPY of `derive-families.js` over the fetched copy (`session-tools/s84p/rd204/bootstrap-5.3.0.min.css`, READ only, copied) and compare byte-for-byte to the committed JSON's selectors | identical | drafter — **the derivation lives OUTSIDE the repo; say so** |
| c11 | NO STALE PINS with a pin for a page that no longer links Bootstrap (scratch) | red | builder |

**D — RD-197 (jsdom over YOUR trees).**

| row | shape | expected | predicted-by |
|---|---|---|---|
| d1 | M1 — info notice grounds → `#262626` | RED on first-run-setup, ~30 sites named | builder |
| d2 | M2 — every danger notice ground `#2b1c1d` → `#262626` | GREEN (ACCEPTED LIMIT L-D3) — **the per-family reach line prints "NOT REACHED"** for danger | builder |
| d3 | success family: the same move for success notice grounds | measure: reached or not? | drafter |
| d4 | E derived: perturb `surface-raised` in a SCRATCH copy of `derive-brand-tokens.js` so info-emphasis clears AA | E shrinks by one; the E cell stays green (derived, not hard-coded) | builder (claim "derived") |
| d5 | an E colour placed on the CARD ground (`#1c1c1c`), not raised | named? (the rule is "only on its own notice ground") | drafter |
| d6 | FINDABILITY: the 38 E nodes and 19 unresolved — per page | re-measured | builder |
| d7 | **L-D1 in a real browser (optional, if cheap):** drive first-run with a saved data source (success) — any success-emphasis text off its ground? | measure or NOT RUN | builder (declared) |

**E — RD-686 (plain node over the helpers at `1904765` AND at `8962a14`; the doc text is the oracle).** Rows e1-e8 = claims E1-E8 of §1 Target E: each
re-derived with your own probe, with a positive control per probe (a planted value the probe MUST report). **e9:** the css-colors.js change is COMMENT-ONLY —
strip comments from both blobs (`78bb004`, `bdb5ca3`) with the repo's own stripper and prove the code identical; `node --check` both.

**F — RD-692 (jsdom).** f1 M-A6 → 409, 428, CONTROL red; f2 M-A10 → SAME MODE red; **f3 the batch-2 gate's own M-A6 and M-A10 wording re-run against the NEW
file AND the old files** (rd388 TOKEN, rd409-410 SAME MODE); **f4** M-F3: the 428 branch's clear only deleted (the 409 kept) → does exactly the 428 cell redden?;
**f5** M-F4: the POSITIVE CONTROL's status sentence changed → red?; **f6** on the MERGED tree (with RD-693's listeners) all five green, rd692 BY NAME (U1).

## 3. THE QUESTIONS ALL SIX TARGETS ANSWER FIRST
0. **SESSION_SECRET UNSET, EVERY jest RUN AND EVERY SERVER YOU BOOT** — see §3a H-1 for the ONE permitted printer. Open mode (C-02) needs no secret.
1. **Re-pin everything yourself:** `git ls-remote` at start, mid and end (three timestamped readings, branch name beside each sha, all six refs + main + the two
   optional ones); M0 and the "Main is moving" rule re-proved on M0; chains and exact parents (`git log --format='%H %P'`); deltas (`git diff --name-status`);
   counts at `1904765`, M0, `4a86c4a`, `ddf1b75`, `a09dd83`, `c219890`, `1645c69`, `a19559f`, `83e5a1b`, `fe47bb4`, `3f91242`, `9c742fa`, `cd589e0`, `43e729c`, `8962a14`,
   `3dcd1c0`, `4580829` (and G, H if included).
2. **Re-derive every red and every mutant INDEPENDENTLY** — your own scripts, never the builders' `rd693-hold.sh`, `rd692-hold.sh`, `rd286-hold.sh`,
   `rd286-shots.js`, `rd204-hold.sh`, `rd204-t2b.sh`, `rd197-proof.sh`, `rd686-verify.sh` (read them for method; run your own). **Before each mutant arm, prove
   the mutant still parses (`node --check` on every mutated JS file, exit 0, quoted; for a CSS mutant, a parse by the same parser the cells use — jsdom's CSSOM
   or the spec's CSSOM binding) and that it LANDED (H-7/H-8). A red from a mutant that does not parse, or a green from a mutation that never landed, is a VOID
   arm.** Read WHY each red is red: quote the failing assertion.
3. **Name every behaviour guarded by no cell, and every one guarded only by source text (C-122).**
4. **Full verify of each head AND of the merged tree**, `npm run verify -- --maxWorkers=2` (RD-561), through the lock, on a git-indexed tree, SESSION_SECRET
   UNSET (verify needs Chrome, C-61). **Predicted: `ddf1b75` 4137/248 · `1645c69` 4133/247 · `fe47bb4` 4148/248 · `43e729c` 4142/248 · `8962a14` 4133/247 ·
   `4580829` 4138/248 · merged (M0 + all six) counts(M0) + 33 / + 4 = 4166/251 at M0 = `1904765`** — ARITHMETIC; C-68 says the measurement decides. **`ddf1b75`
   has never been verified as a committed tree (§1 A) — this is its first.** Every failure by NAME. **"Re-run until green" is not an acceptance gate (charter §4d).**

## 3a. INSTRUMENT RULES — H-1..H-17 (inherited from the batch-4 brief §3a, unchanged where they apply) and H-18..H-20 (browser and token, from the batch-2 report)
- **H-1 (a SET/UNSET idiom once printed the secret's VALUE).** The ONLY permitted printer, verbatim:
  `if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi`.
  **FORBIDDEN anywhere in your scripts:** `${SESSION_SECRET-…}`, `${SESSION_SECRET:-…}`, `${SESSION_SECRET+$SESSION_SECRET}`, `echo $SESSION_SECRET`,
  `printenv`, `env | grep`, `set | grep`, **echoing an env array that could hold it (`${envs[*]}`)**, and **`docker inspect` output** of anything that received it
  (no docker is needed here; the rule stands). **Self-test it BEFORE the first hold (a control that can fail):** run the printer once with a throwaway exported and
  once unset, capture both outputs, assert the throwaway's value is ABSENT from both (compare in-process; never print it). **After every hold, scan its logs for
  the throwaway value** (in-process) and report the count (0); **the scan's own positive control plants a DIFFERENT random marker, never the throwaway.**
- **H-2** Never construct a product storage object on a DATA_DIR you are measuring after its server booted. Read `settings.json`, backups and logs RAW.
- **H-3** Every hook you rely on (a Playwright route interceptor, a pageshow recorder, a mutated rule, a planted CSS rule, a seed) gets a **LANDING CONTROL** before the
  measured run. An arm whose instrument failed is VOID, is re-run, and is reported as a self-correction — never as a result.
- **H-4** The heartbeat is a SEPARATE child process started by the hold wrapper (`while sleep 60; do echo "HB $(date -u +%FT%TZ) <step> <pid> <elapsed>";
  done`), killed in the wrapper's `trap … EXIT`; **the wrapper ABORTS the hold if no HB line appears within 90 s of the grant**, and you report the max gap
  between HB lines per hold (must be ≤ 120 s).
- **H-5** Restore your own perturbations (scratch CSS/JS/HTML edits, planted rules) before any before/after hash, and hash the restore.
- **H-6** Every extractor (hunk, census grep, colour extractor, CSS rule extractor, screenshot clip, pixel differ) gets a POSITIVE CONTROL. **Every path is quoted** —
  `!CODING` and `Testing Agent MAIN` contain `!` and spaces. **The browser harness ABORTS every request to a non-127.0.0.1 host** (Playwright `route('**/*')`, logged),
  except Tuesday's batch-2 CDN allow-list if you need Bootstrap to render (batch-2 report §3.6 :122-128: exact URLs, SRI held) — **run BOTH renders and label them.**
- **H-7** Mutants are built and verified ONLY by a quoted tool with a negative control (an unmutated tree → VOID rc ≠ 0).
- **H-8** The landing rule is "the exact mutated text is present AND the original text is absent once the new text is removed" — never "the anchor is absent".
- **H-9** Byte-level plants are not needed by this batch; if you write one, `Buffer` + `xxd -l 16` before use (never `echo`/`printf`/heredoc/`JSON.stringify`).
- **H-10** Prove the phenomenon is reachable before measuring its absence: **bfcache restores a plain loopback page (`persisted:true`) before a1 is read; the pixel
  differ SEES a planted 1-px change before p2's zero is read; the colour resolver FAILS a planted `#123456` before §11b's "all resolve" is read.**
- **H-11** Every script runs under `/bin/bash` explicitly, and every `<sha>:<path>` is written `"${sha}:${path}"` (zsh eats `$s:t`, `$s:s`, `$s:h` — the drafter
  slipped on exactly this twice today).
- **H-12** Before the C-57 control, list every `__tests__` file any head MODIFIES or DELETES (`git diff --name-status 1904765 <head> -- __tests__`); **MEASURED at
  drafting: RD-204 `M helpers/dom.js`, `M helpers/vendor-surface.css`; RD-686 `M helpers/css-colors.js`; no cell file is modified or deleted by any member.**
- **H-13** Every path census is NUL-safe (`git ls-tree -z`, `ls-files -z`) with a positive control that a space-bearing path is found.
- **H-14** Your GUID/token redactor matches hyphen OR space separators; scan every evidence file with it before the report is written.
- **H-15** No inline loops under zsh; every arm builder is a `#!/bin/bash` file.
- **H-16** No docker image is built by this gate. If you find you need one, it is NOT RUN with the reason named.
- **H-17** A plant or mutant whose shape lands in a different class than intended is VOID for its row — re-plant; an interesting surprise gets its own row.
- **H-18 (batch-2 S-4 :376: two VOID holds' worth of bfcache arms).** Playwright's default launch argument `--disable-back-forward-cache` makes Chrome report
  `BackForwardCacheDisabledByCommandLine`: **launch with `ignoreDefaultArgs: ['--disable-back-forward-cache']`**; a bfcache restore fires `pageshow`, not `load`,
  so **`page.goBack({ waitUntil: 'commit' })`** then settle; record `pageshow` `persisted` via an init script AND `performance.getEntriesByType('navigation')[0]
  .notRestoredReasons` where available; **LANDING CONTROL first: a plain loopback page restores with `persisted:true`.** An a-row whose Back was not a restore
  is not a1 — label it a4.
- **H-19 (the token).** Print a token only as `<first4>…<last4> (len N)`; compare by equality or hash in-process; **mask it in every screenshot** (the RD-409/410 and
  batch-2 gates did); scan every evidence file for the full token after each browser hold and report the count (0) beside a positive control that plants a
  different random marker.
- **H-20 (C-174).** Every server, browser and child you stop is stopped by a pid YOU spawned (`$!`, your own child list) or proven to descend from YOUR claude pid.
  **Never `pkill -f`, never `kill $(pgrep -f …)`.** Every browser is closed in a `finally`; count Chrome processes whose ancestry contains your pid before and
  after each browser hold (0 after).

## 4. TARGET A — RD-693 (TIER 1). Answer each with a measurement.
1. **Scope (READ ONLY, quoted):** `git diff --name-status 1904765 ddf1b75` = the three files; `4a86c4a` cells only; the product hunk is ADDITIONS ONLY (numstat
   `32 0`) — so every existing clear (Save, Revoke, Reload, a refused save; READY PRIOR WORK :20) is byte-unchanged: prove it by extracting those functions at both shas.
2. **RED-PROOF, POSITIVE CONTROL FIRST, in ONE hold:** rd693 against `1904765`'s module → predicted LEAVE, RESTORE, RESTORE WITHOUT A PAGEHIDE red, CONTROL green; then
   **4/4** at `ddf1b75` (the COMMITTED file, not a working-tree copy). **Is CONTROL a control that can fail (C-40)?**
3. **Mutants (all new; predictions the drafter's):** **M-A1** drop the `pagehide` listener → LEAVE red, RESTORE red?; **M-A2** drop the `persisted === true` test
   (clear on every pageshow) → CONTROL red (a first load must change nothing)?; **M-A3** `setStatus(…)` removed → RESTORE red?; **M-A4** `render()` removed from
   `dropTokenOnLeave` (memory cleared, DOM stale) → LEAVE red on the panel half?; **M-A5** the `__nxProvisioningLeave` replacement removed (listeners stack) → any
   cell red? (predicted NONE — a gap to name, or prove harmless); **M-A6** `tokenDroppedOnLeave` never reset → a14's second restore shows the sentence again — any
   cell?; **M-A7** listen on `visibilitychange` instead of `pagehide` → which cell? (the a6 regression — **predicted: none; name the gap**); **M-A8** `document`
   instead of `window` as the event target → LEAVE/RESTORE red?
4. **Every row a1-a14 of §2a** (§11a) — base, head, merged; a10/a11 on first-run-setup.
5. **THE SAFETY LEG (batch-2 Q5b's shape):** with the positive control beside it, the token after leave+Back reaches **no** request, storage, console line,
   server stdout/stderr, `LogFiles/*` or `settings.json`.
6. **C-68 re-run set for A (§1 table step 6)** in one hold, per-file counts, **rd692 by name.**
7. **PRIOR WORK (C-49):** the four existing clears kept; `identifier-mask.js:115`'s `pageshow` handler (the only other page-lifecycle listener in `static/js`,
   census `git grep -l -E 'pagehide|pageshow' ddf1b75 -- static` = 2 files) — was its pattern known and reused, or a second idiom? The meta `no-store` at
   `settings.html:6` untouched (READY :20; RD-705's). READ.

## 5. TARGET B — RD-286 (TIER 2 + browser). Answer each with a measurement.
1. **Scope (READ ONLY, quoted):** the three `dark-mode.css` hunks of §1 Target B, and **the comment-stripped declaration diff = exactly the two `- background-color`
   lines** (your own stripper, with a positive control: a planted declaration change IS reported). Each comment change mapped to its authority (C-168 :1727 / :1728;
   C-175 :1795).
2. **The spec, POSITIVE CONTROL FIRST, in ONE browser hold (§11a):** its own CAN-FAIL cells (guard 1 F5, guard 2 mutation, inverse dead-override, RD-288 red control,
   the (a) arm's red control) seen RED-then-GREEN; then 18/18 at `1645c69` and on the merged tree.
3. **Mutants (new):** **M-B1** re-insert ONE of the two deleted declarations at its original place → which cell? (predicted: the inverse reports that pair dead
   again — C-172's reason); **M-B2** change the base td marker back to "stated, not inherited" → guard 2's population grows, guard 2 red (the light `#ffffff` returns)?;
   **M-B3** delete the base `th` declaration (the load-bearing one) → the inverse / guard 2 red, and the last header paints `#f8f9fa` in dark (screenshot);
   **M-B4** the spec's claim marker regex narrowed → "an unbound claim fails" or the population shrinks unseen?
4. **Every row p1-p10 of §2a**, both themes, 1280×900 and one more viewport.
5. **k3 (U6):** does any jest brand reader read the `#f8f9fa`/`#ffffff` inside the new `dark-mode.css` comments? Prove the extractor strips comments (plant an
   off-token hex inside a comment in a scratch copy: green) and reads declarations (plant it in a declaration: red).
6. **C-68 re-run set for B (§1 table step 2).**
7. **PRIOR WORK (C-49):** the F5 comment's history (QA pass 19, `7e5faa9`; Wednesday's 2026-09-04 ruling) replaced — C-168 authorises it; `tests/e2e/ground.js
   groundCandidates` reused, not forked (READY :31). READ.

## 6. TARGET C — RD-204 (TIER 2). Answer each with a measurement.
1. **Scope:** `git diff --name-status 1904765 fe47bb4` = the five files; `dom.js` +88/−0 (additions only, appended); `vendor-surface.css` +39/−0 **all comments** —
   prove with the repo's own CSS parse that the rule set is identical at both blobs (`2bdc133` → `658b4d6`).
2. **RED-PROOF, POSITIVE CONTROL FIRST, in ONE hold:** c1 (T1), c2 (T2b), c3 (T3) re-derived by YOUR mutator — the builder's numbers are the prediction; c4 (T2) green.
3. **The semantics question (the READY's gate ask) — rows c4-c9:** for each, say whether `paintingRulesOf` and the committed list agree with what Bootstrap 5.3.0
   ACTUALLY paints on that element in a REAL browser (optional but decisive: render the five pages with the CDN allow-list, §3a H-6, and read the computed
   `background-color`/`color` of every node the report names as bg-uncovered on settings — how many are transparent in reality?). **Name the direction of every
   mismatch: over-report (safe) or under-report (a Major for the claim).**
4. **c10 PROVENANCE re-derivation** (a COPY of `derive-families.js`, run by you over a COPY of the fetched file) — identical or not; state that the derivation
   lives outside the repo (L-C3: a version bump needs it).
5. **C-68 re-run set for C (§1 table step 3).**
6. **PRIOR WORK (C-49):** "deliberately NOT wired into `unmeasurableNodes` or `scripts/jsdom-unmeasured-ceiling.json`" (READY :42) — confirm both byte-unchanged.

## 7. TARGET D — RD-197 option (b) (TIER 2). Answer each with a measurement.
1. **Scope:** `git diff --name-status 1904765 43e729c` = the two files; no palette value touched (`tokens.css` `de6e0fe`, `derive-brand-tokens.js` `d94423a` identical
   — the launcher proves it; re-prove).
2. **RED-PROOF, POSITIVE CONTROL FIRST, in ONE hold:** d1 (M1) red, d2 (M2) green with its NOT REACHED line, PROBE RED/GREEN cells, then 9/9.
3. **Every row d1-d7.** **Is FINDABILITY a control that can fail (C-40)** — plant a page state with zero E nodes (scratch) and see it red.
4. **"STILL VALID AT THE MERGED HEAD" (READY :19) was a READ; re-measure it:** the clean 9/9 and M1 at `43e729c` itself (not `3f91242`).
5. **C-68 re-run set for D (§1 table step 4).**
6. **Option (a) stays Kam's:** state that nothing in RD-197 changes a colour value, and record — without ruling — the three E ratios you measure.

## 8. TARGET E — RD-686 (+ RD-694 items 1-3) (TIER 2). Answer each with a measurement.
1. **Scope:** the two files; `css-colors.js` COMMENT-ONLY (e9).
2. **Rows e1-e8** — each claim re-derived by your own probe at `1904765` (the doc says "measured at main 1904765") AND at the merged tree, each probe with a positive
   control. **Quote the doc sentence beside the number you measured.** E2's "125 of 147 distinct hex / 96 functional sites" and E1's "3 functional sites" are counts
   — reproduce them or name the difference and its cause.
3. **Is the new text TRUE in the unsafe direction?** (Does it claim the gate reads something it does not?) — the Major class of §2.
4. **C-68 re-run set for E (§1 table step 1)**, per-file counts.
5. **PRIOR WORK (C-49):** rule 3's two bullets (RD-199, RD-200) — "Both histories are kept in the new text" (READY :19): quote where. §6 of BRAND.md untouched
   (READY :19) — prove by diff.

## 9. TARGET F — RD-692 (TIER 2). Answer each with a measurement.
1. **Scope:** the two files; no other file touched (the READY's (a) — a NEW file; the rd409-410 file untouched, READY :25 — prove by blob).
2. **RED-PROOF, POSITIVE CONTROL FIRST, in ONE hold:** f1, f2 re-derived; CLEAN 5/5; **then f3 — the batch-2 gate's own M-A6/M-A10 against the new AND the old files.**
3. **f4, f5 (new mutants), f6 on the merged tree (U1).**
4. **A-F1's specification vs the cells (batch-2 report :333, :403):** say whether the new file asserts exactly "cleared and absent after a 409" and "a same-mode
   press is SILENT", or less; the READY changed SAME MODE's assertion after a red-on-clean first hold (READY :21) — **is the corrected assertion still the property
   M-A10 breaks (C-98), or a weakening to fit?**
5. **C-68 re-run set for F (§1 table step 5).**

## 10. OPTIONAL MEMBERS — Tuesday fills or leaves EXCLUDED at stamp (the launcher refuses a mismatch)
**If a member below reads `STATUS: EXCLUDED`, it is NOT in this gate: do not gate it, do not merge it into your clone, do not measure it beyond U9's READ.**

### OPTIONAL G — RD-430 STATUS: EXCLUDED
- *(Tuesday: to include, replace the line above with `### OPTIONAL G — RD-430 STATUS: INCLUDED @ <40-hex head>`, name its READY mail path here, and set the
  launcher's `OPT_G_HEAD`.)*
- **Branch** `rd-430-remove-response-form-s84p`, at drafting `9ba6f1d8976a57130c2c887c6c68509b5efadab4` = `8ca8f22` (red-first cells, off `11666d3`) → `17b465c` (merge
  `5f2683c`) → `0f93446` (merge `1904765`) → `9ba6f1d` (the removal). **Being RE-PINNED by the lane-4 seat under C-175** (three pins: `dom-harness.test.js` and two
  cells of `jsdom-instrument-limits.test.js`, settings visible nodes 172 → 157; conditions: a red-proof per re-pinned cell, the READY names each pin old → new, both
  files on the C-68 list). `session-tools/s86p/rd430-repin-hold.log` exists (READ, not relied on).
- **Delta at `9ba6f1d` over main:** `A __tests__/rd430-response-form-removed.test.js` (133), `M static/js/settings.js` (−17), `M static/settings.html` (+3/−54). **Its
  counts file is main's 4133/247 although it ADDS a test file (MEASURED) — the re-pinned head must regenerate it (C-89).**
- **If INCLUDED — TIER 2 (a user-visible REMOVAL; C-166, C-18) + a browser look** at Settings > the AI section, both themes, before/after (the AI features switch card
  STAYS, C-166 :1702). Its READY's NOT TESTED list is carried VERBATIM here by Tuesday at stamp. **U9 is a required measurement, and a red rd204 settings pin is a STOP
  to name (C-175 "Not covered: any other pin").** The launcher's expected delta for G: the three files above + `__tests__/dom-harness.test.js` +
  `__tests__/jsdom-instrument-limits.test.js` + the counts file.
- Verdict line, if included: **RD-430: GO / GO WITH FINDINGS / NO GO** at its stamped head.

### OPTIONAL H — RD-694 STATUS: EXCLUDED
- *(Tuesday: to include, replace the line above with `### OPTIONAL H — RD-694 STATUS: INCLUDED @ <40-hex head>`, name its READY mail path here, and set the
  launcher's `OPT_H_HEAD`.)*
- **RD-694 item 4 (C-176):** `1d457cef2a1b1a66454a3ce77d751be56fa8bbbc` "RD-694 item 4: correct the RD-200 debt manifest's _about text (entries unchanged)", ONE commit on
  `1904765`, branch `rd-694-fixture-about-s86p` — **NOT on origin at 09:28 (ls-remote: no such ref); a local branch only; its verify was QUEUED at ~23:33Z**
  (`session-tools/s86p/rd694-verify.log`, READ). Delta: `M __tests__/fixtures/rd200-js-brand-debt.json` (+1/−1); counts 4133/247 (no test change).
- **If INCLUDED — TIER 2:** a per-key diff proving every entry byte-identical (only `_about` moves); the fixture's only reader is `rd200-js-colour-corpus.test.js`
  (census `git grep -l rd200-js-brand-debt 1904765 -- __tests__` = 1 ✔) and no `.js` reads `_about` (C-176 :1807 — re-prove with a positive control); **the new
  `_about` text vs RD-686's words (E4) — consistent?**
- Verdict line, if included: **RD-694: GO / GO WITH FINDINGS / NO GO** at its stamped head.

## 11. THE MERGED TREE (C-68, C-57, C-89, C-104, C-112). No verdict is complete without it.
1. **Build it in YOUR OWN scratch clone** under `projects/nexusai/qa-trees/batch6.*/clone-1`: `git clone --shared --no-checkout <repo> <dir>`; in the clone only:
   remove `origin`, set a local `user.name`/`user.email` and `gc.auto 0`; `git checkout -b gate <M0>`; then `git merge --no-ff` in the PROPOSED order:
   **`8962a14`** (RD-686), **`1645c69`** (RD-286), **`fe47bb4`** (RD-204), **`43e729c`** (RD-197), **`4580829`** (RD-692), **`ddf1b75`** (RD-693) (+ G after RD-197, H after
   RD-686, only if INCLUDED). **Predict before each merge whether the counts file conflicts** (it depends on the side you took at the previous one) **and explain any
   clean merge with a side control**; **predicted: steps 1-3 clean, steps 4-6 conflict in the counts file ONLY.** Anything else conflicting **STOPS** (C-57).
   **C-104: resolve and stage before any census or run.** **Also run every PAIRWISE `git merge-tree --write-tree --name-only --messages` of the six heads (15 pairs)
   in the clone's own object store and report rc + conflicted paths per pair — the builders' merge-trees were mostly against OLDER heads (§1).**
2. **Resolve the counts file by REGENERATION, never by hand:** take a side to complete each merge commit, then `npm run verify -- --maxWorkers=2 --update-counts`
   ONCE on the tree after ALL merges, through the lock, SESSION_SECRET UNSET, and commit the regenerated file in the clone. **Predicted counts(M0) + 33/+4 (4166/251
   at M0 = `1904765`).** Then a plain verify of the committed head; suites ≥ the largest parent's (C-57 step 4). **Also measure the counts at EACH step's tree (`jest
   --listTests | wc -l` inside the lock is enough for suites) against the §1 table.**
3. **Order independence (a control that can fail):** a second clone in a DIFFERENT valid order — **O2: `ddf1b75`, `4580829`, `43e729c`, `fe47bb4`, `1645c69`, `8962a14`**. **The
   two `HEAD^{tree}` must be identical apart from the counts file** — quote both tree ids and the `git diff --name-only`.
4. **Blob identities on the merged tree (predicted at M0 = `1904765`):** `static/js/entra-provisioning-ui.js` = `38500ec` (RD-693's), `static/css/dark-mode.css` = `e90297e`
   (RD-286's), `__tests__/helpers/dom.js` = `3f913ff`, `__tests__/helpers/vendor-surface.css` = `658b4d6`, `__tests__/helpers/css-colors.js` = `bdb5ca3`, `docs/BRAND.md`
   = `a3f4413`, `static/css/tokens.css` = `de6e0fe`, `package-lock.json` = `9064763`. **C-112's condition — state it beside the conclusion: at M0 = `1904765`, 294
   `__tests__` files predicted, EVERY one byte-identical to a parent (no test file content-merged) — MEASURE it; only then may the id-superset rely on byte identity,
   and the C-68 by-name runs are owed regardless.**
5. **id-superset control (C-57):** merged test ids ⊇ ids(M0) ∪ ids(`ddf1b75`) ∪ ids(`1645c69`) ∪ ids(`fe47bb4`) ∪ ids(`43e729c`) ∪ ids(`8962a14`) ∪ ids(`4580829`), with a COPY
   of the batch-1 gate's `qa-c57-id-superset.sh` (keeps the lock-holder refusal; prove it first to STOP on a planted missing id). **PREDICTED: exact pass, missing 0**
   (no member modifies or retitles a cell — H-12). Ids come from jest's JSON (rd692's 409/428 titles are built in a loop). Any miss → C-133 + ADDENDUM + C-150
   verbatim, or a STOP to name.
6. **The semantic overlaps git cannot see (C-68), on the merged tree:** U1-U8 (and U9 if G is INCLUDED), the per-step sets of §1, the merged columns of §2a A-F; the
   full verify (Q2); then ONE mutant per ticket on the merged tree (**M-A1, M-B3, T2b, M1, e9's comment-only proof, M-A6 of RD-692**): each must still hold through the
   other five changes.
7. **C-89 on your clone:** `git diff --quiet HEAD` holds and `git show HEAD:scripts/verify-expected-counts.json` equals the regenerated counts.
8. **Nothing leaves your clone.** No push, no remote, no ref written in the NexusAI repo. **Record `git count-objects -v` of the NexusAI repo before and after your
   whole session and account for any delta by mtime** (live seats commit into that repo; other gates' merges land).

## 11a. THE BROWSER LEGS — RD-693 (R11) and RD-286 (the spec + an independent pixel compare)
1. **Browser:** installed Google Chrome via Playwright from YOUR tree's `node_modules/@playwright/test`, `channel: 'chrome'` (L-B5; the batch-2 gate measured Chrome
   153.0.8010.53, Playwright 1.62.1). **If no browser launches, the leg is NOT RUN, RD-693 cannot be GO, and you mail a QUESTION (§15) and proceed with the rest.**
2. **Server:** YOUR loopback server from YOUR archive tree, fresh DATA_DIR per flow, open mode (C-02), a port of your own; for RD-286 the surface is seeded as
   `qa-surface-up.sh`'s seed says (reproduced, never run — §1 B). **Every browser run and every server you boot goes through `session-tools/nexusai-lock.sh jest
   qa-b6-…`** (the jest kind is the lock that guards servers on this Mac; C-110).
3. **bfcache (H-18):** `ignoreDefaultArgs: ['--disable-back-forward-cache']`, `goBack({ waitUntil: 'commit' })`, a `pageshow` recorder init script, `notRestoredReasons`
   where available; landing control first. **Rows a1-a14** at `1904765`, `ddf1b75`, merged — same hold, same window.
4. **b9 — RD-705 on M0 (U3):** if M0 contains RD-705 (the server sets `Cache-Control: no-store` on HTML — check `git log M0 -- <the server entry point>` for its
   commit, and the response header on `/settings.html`), run a1 on the MERGED tree built on that M0: record `persisted`, `notRestoredReasons`, the token (absent
   either way) and whether the RD-693 sentence appears (predicted: a fresh load, NO sentence). **And run a1 on `ddf1b75` itself (which does not carry RD-705) so the
   `persisted:true` branch is measured in a real browser at least once.** If M0 does not contain RD-705, say so and skip b9. **Never grade RD-705.**
5. **RD-286:** the spec (p1) through YOUR surface per tree; your own screenshot clips (p2, p3, p10) with the determinism precondition and a positive control; the
   inverse re-derived (p4, p5). Masked PNGs saved under `evidence/`. **1280×900 + one more viewport.**
6. **Network:** the harness ABORTS every non-loopback request (H-6), logged; if Bootstrap must render, run the CDN allow-list render too (batch-2 §3.6), both labelled.
7. **Every browser closed and every server stopped in a `finally`, by pid (H-20); Chrome count 0 after every run.**

## 11b. THE BRAND LEG — every colour any member introduces, one table
1. **The guide:** `docs/BRAND.md` §3 "The tokens" (`:117` at `1904765`) and `static/css/tokens.css` (`de6e0fe`, identical everywhere — MEASURED). `tokens.css` is linked
   by NO page; resolution is VALUE-EQUALITY in the theme block the rule applies to (batch-2 report §3.9 (c) :147). **A colour that resolves to no token in its
   theme = OFF-GUIDE = Major.** Palette choices are Kam's: **record, never rule.**
2. **k1 — static census:** extract every colour literal from the ADDED lines of every `static/` file in any delta (RD-693's JS hunk, RD-286's CSS hunks; G's if
   INCLUDED) **after comment stripping** — predicted: **none added** (RD-693 adds no colour literal; RD-286 adds only comment text and removes two declarations).
   Positive control: the same extractor FINDS a planted `#123456` and the resolver FAILS it.
3. **k2 — rendered:** the RD-693 sentence (`'error'` kind) — computed `color` and effective ground, light and dark, settings and first-run; each resolves to a token
   in its theme; contrast ≥ 4.5:1 (a13). The Sustainability rank tables at head vs main — every computed ground identical (p2).
4. **k3 — comments carrying hex:** `#f8f9fa`/`#ffffff` in RD-286's new `dark-mode.css` comments (U6, §5 Q5) — read or not by any gate.
5. **k4 — tests and docs:** RD-204's JSON and RD-197's cell carry colour VALUES as test data (derived, not introduced into the product) — state that none reaches
   `static/`; RD-686's BRAND.md adds no token and changes no value (diff §3 untouched).
6. **k5 — the brand gates themselves on the merged tree:** `brand-token-conformance`, `rd200-js-colour-corpus`, `brand-md-accent-count`, and (outside verify)
   `tests/e2e/brand-pairing.spec.js` against its ratchet on the merged tree's surface — **optional; if run, run it at M0 too and report only the delta.**

## 12. CI and DEPLOY (C-142) — READ ONLY
- **Unverified by the drafter:** whether any of the six branches has a PR (no `gh` was run). Check with `gh pr list --head <branch> --state all` (READ ONLY,
  NexusAI's own `GH_CONFIG_DIR`); M0's CI Build — `gh run list --commit <M0>` READ ONLY, labelled. **`gh` never merges, approves, comments, reviews, labels,
  re-runs, dispatches or opens a PR.** CI NOT RUN at a head with no PR.
- **What a merge push to main triggers (READ at `1904765`, `.github/workflows/deploy-demo.yml`):** `on: push: branches: [main]` with `paths-ignore: '**.md',
  'docs/**', 'tests/**'`. **Every member's delta has at least one non-ignored path** (RD-686's `__tests__/helpers/css-colors.js`; RD-286's `static/css/dark-mode.css`;
  the others' `__tests__/…` and the counts file) — so **each merge push would START the workflow.** Its `build` job runs `az acr build` only if
  `vars.CI_DEPLOY_ENABLED == 'true'` (:53); its `deploy` job needs the same and the `demo` environment's required reviewer (:91, :95). **Read (never set)
  whether `CI_DEPLOY_ENABLED` is set and what the batch-1 merges' push runs did (`gh run list --workflow deploy-demo.yml --branch main --limit 5`, READ ONLY) and
  state it in the report for Tuesday**, because "no deploy" at merge time rests on that switch and that reviewer. `deploy.yml` is `workflow_dispatch` only (READ).

## 13. Floor discipline — THE FOUR CLAUSES, plus THE DEADLINE RULE, plus THE OTHER GATES
1. **Every jest run — full verifies, cell runs, mutants, `jest --listTests` — AND every browser run and every server you boot goes through
   `session-tools/nexusai-lock.sh jest <tag> …`, tagged `qa-b6-…`** (e.g. `qa-b6-H1-arms`, `qa-b6-H2-browser-693`, `qa-b6-H3-browser-286`, `qa-b6-H4-heads-verify`,
   `qa-b6-H5-merged`). **`--after <ticket-tag>`** files a ticket directly behind a named live ticket (C-141 ADDENDUM 4): use it ONLY to sit directly behind a
   NexusAI MERGE ticket already queued (gate-class — never jump it) or behind your own preceding `qa-b6-*` ticket; **never use it to jump anyone.** C-141: every
   NEW `qa-*` ticket earns the builders' self-applied yield. **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit another seat's process, lock directory,
   owner file or ticket, even if it looks stuck; if a holder looks stuck, mail a QUESTION (§15) and keep waiting. Pure-node rows with no server, no browser and no
   jest (§2a-C c5-c10, §2a-E e1-e9, censuses, the merges themselves) may run outside the lock — say which did. **No docker is needed; never take the docker lock.**
2. **Hold the lock ONCE per multi-run measurement.** Every hold is a TRACKED CHILD of your seat, never detached (`nohup … &`).
3. **Count foreign servers the C-125 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND the server entry point anywhere in the remaining argv;
   "ours" = the ancestor chain CONTAINS your own claude pid. **NEGATIVE controls, all in the same run, all must classify FOREIGN — read at drafting 2026-09-27
   09:31:51 AEST from `tmux list-panes -a -F '#{pane_id} #{@cockpit_name} #{pane_pid}'` + `pgrep -P` + `ps`:** NexusAI-M claude **`62649`** (pane `%19`), NexusAI-N claude
   **`9959`** (pane `%21`), NexusAI-P claude **`20317`** (pane `%22`), and Tuesday's claude **`23230`** (pane `%0`, parent bash `22288`); plus the live gates
   QA/NexusAI-batch3 claude `36118` (`%23`) and QA/NexusAI-batch4 claude `40285` (`%24`). Seats restart; re-read them at start; if one has exited, say so and use the
   others; **a hold with NO live negative control aborts.** Reuse the batch-1 gate's instrument BY COPY with YOUR pid as `ROOT` and these as `NEG`:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch1/evidence/qa-floorlib.sh` (**its `ROOT=33673` and `NEG` default
   name the batch-1 gate's seats — correct both before any hold**), `…/qa-floorcount.py` (`--chrome` counts your Chrome) and `…/qa-dispatch.sh`. The original is gate 7's
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`. **A headless Chrome is a floor
   process too** (batch-2 §9.3).
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, "the token reached nothing" (a12), "0 pixels moved" (p2),
   "no colour added" (k1), "no id missing" (§11 Q5), "no cell reddens" under any mutant, and "no token/throwaway in any log".

**5. THE DEADLINE RULE.** Every probe, browser and server step has a written DEADLINE (server boot 60 s, request 30 s, page load 30 s, key press 10 s, browser close
20 s, a jest cell run 600 s, the rd286 spec 1200 s, a full verify 2700 s); a step past it is ABORTED and reported, never waited on. **HEARTBEAT at least every
2 minutes during any hold (H-4: a separate child, ≤ 120 s max gap, aborted if absent at 90 s); a step with no heartbeat for 5 minutes is aborted and reported,** and a
hold that is not progressing releases the lock. Every server and browser you start is killed in a `finally`, by pid (H-20).

**6. THE OTHER GATES (batch-3, batch-4, and any batch-5a).** They may be live now, with `qa-*` tickets in the same jest queue. **You treat their tickets exactly as a
builder treats yours under C-141: never jump them, never interrupt a running one, never move, signal or edit one.** C-141 says "Not covered: … gate tickets among
themselves" (:1484), so **between gates the order is plain FIFO: you do NOT self-re-queue behind their tickets and you do NOT ask them to move; if their hold is
running, you wait.** Never read their trees as inputs, never run in their clones, never count their servers as ours. **If main moves because their merges land,
apply §1's "Main is moving" rule.** If you and one deadlock or its hold looks stuck past its own heartbeat, mail a QUESTION (§15) and keep waiting.

## 14. HELD
- **LOCAL RUN, NOT THE DEMO:** every request goes to a server YOU booted on 127.0.0.1 from YOUR tree; the browser aborts every non-loopback request except the
  labelled CDN render. No request to any live, demo or public host; no Entra, no Azure, no real SCIM client — every token is minted by your own local server and is
  throwaway. This is authorised defensive QA of Datasec's own product on loopback.
- **Findings only:** no fixes, no pushes, no deploys; no merge outside your own clone; nothing to Partner Center, the demo or production; no money; no external
  comms; no mail to any human. **No `az` at all.** `gh` READ-ONLY and optional (§12). **Never set, change or read-and-print any GitHub variable or secret value.**
- **Scratch CSS/JS/HTML edits and scratch git repos live ONLY under your own mktemp dirs.** Never plant anything in the NexusAI tree or any other seat's directory.
- **Do not commit (outside your clone), move any branch, file a ticket, or write anything inside the NexusAI project** (`2_Project_Files`, `session-tools/`,
  `worktrees/`, `qa-worktrees/`, `1_Project_Definition/`, `qa-reports/`). **Never run `scripts/qa-surface-up.sh`.** **NEVER `rm`** — quarantine, per the template §5.

## 15. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch6/report.md` — ONE report covering all six tickets (and
any INCLUDED optional member); evidence in `./evidence/` beside it.

**Questions:** your routing name is **`QA/NexusAI-batch6`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by) and **PROCEED ON THE SAFEST READING without waiting**;
Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning `[Tuesday -> QA/NexusAI-batch6] ANSWER`. Approval-class items are NOT RUN
and named. Record every question, reading and answer.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-693 · RD-286 · RD-204 · RD-197 · RD-686 · RD-692`
(if Tuesday INCLUDES an optional member at stamp, the launcher appends ` · RD-430` and/or ` · RD-694`, and this line carries the same suffix).
Lead the body with ONE line per ticket in the form `RD-<n>: <GO|GO WITH FINDINGS|NO GO> @ <short sha> — <one sentence>`, then one line naming M0, the merged
counts, and the R11 result. Never `wednesday-agent@`. AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute:
the QA project has none). Never put the key, a token, the throwaway secret, a canary or any secret in a mail or the report.

Verdict format:
- **RD-693: GO / GO WITH FINDINGS / NO GO** naming `ddf1b75f7c3c4aead2da2ce9b3c0b724fb4b3969`: the red-proof; M-A1..M-A8; rows a1-a14 with the REAL bfcache (H-18) at base,
  head and merged; b9; the safety leg; rd692 by name; L-A1..L-A3.
- **RD-286: GO / GO WITH FINDINGS / NO GO** naming `1645c69eeb9a28a267b44b5ffe7fd5fdb51149b2`: the declaration diff; the spec's controls and 18/18; M-B1..M-B4; rows p1-p10
  incl. the REAL-base pixel compare; k3.
- **RD-204: GO / GO WITH FINDINGS / NO GO** naming `fe47bb49124805a67ca79274104309e4c902041c`: T1/T2b/T3 re-run; rows c4-c11 and the direction of every semantic mismatch.
- **RD-197: GO / GO WITH FINDINGS / NO GO** naming `43e729cbf056cd7ff064535372e7b2b2f23fcc5f`: M1/M2; rows d1-d7; FINDABILITY as a control.
- **RD-686: GO / GO WITH FINDINGS / NO GO** naming `8962a149798531b61eddd22361dec1261a372f4e`: e1-e9, each sentence beside its measurement.
- **RD-692: GO / GO WITH FINDINGS / NO GO** naming `4580829aa7ad1c1cfee969d89885b6d87e1205ca`: f1-f6 and A-F1's specification vs the cells.
- (G / H only if INCLUDED.)
- **The merged tree (§11), the browser legs (§11a) and the brand leg (§11b):** M0 named; 15 pairwise merge-trees; both orders; conflicts quoted; counts regenerated
  once (measured vs counts(M0) + 33/+4); per-step counts; id-superset; C-112's condition stated (measured, not assumed); U1-U8 (U9) each answered; one mutant per
  ticket; C-89; the object-count accounting; the deploy-trigger reading (§12).
- Each of **L-A1..L-A3, L-B1..L-B5, L-C1..L-C4, L-D1..L-D3, L-E1..L-E2 and L-F1..L-F2** answered: discharged with a measurement, or left standing and named (C-112).
- Report all refs as **three timestamped readings (start / mid / end)**, each with its branch name.
- **§3a H-1..H-20:** state for each that it was followed (or N/A with the reason), with the self-test outputs (H-1), landing controls (H-3, H-10, H-18), max HB gap per hold
  (H-4), and the token scans (H-19).
- **The floor (§13):** every hold with its tag, queue wait, controls fired, foreign max / ours max, Chrome max, and which other gates were live.
- Every action recommendation carries its evidence class: **MEASURED AT RUNTIME / PROBED / READ ONLY**. Severity is yours; priority is Tuesday's.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, browsers other than the installed Google Chrome, viewports other than those the gate names, Azure Container Apps and the demo, a real Entra SCIM client, the release pipeline's own image build and any registry, and Windows.

## WRONG OR UNVERIFIED IN THE COMMISSION AND THE READYS — carried so the gate inherits the corrections
1. **"RD-204 and RD-197 both conflict ONLY in scripts/verify-expected-counts.json"** — incomplete. **FOUR members change the counts file (RD-693, RD-204, RD-197,
   RD-692), so it conflicts in SIX pairs** (MEASURED name sets, §1). Still counts-only (C-57 regenerate) — every other pair is file-disjoint.
2. **RD-693 tier:** the READY proposes "tier 2 WITH a browser leg" (READY :6); the commission sets TIER 1. The brief follows the commission (as batch 2 raised RD-428).
3. **RD-693's full verify "4137/4137 … 248" ran on `4a86c4a` + an uncommitted fix** (`rd693-hold.log` "rd693 verify at 4a86c4a"), not on the committed `ddf1b75`.
4. **RD-286 "exactly two deletions … PLUS one comment change":** relative to `c219890` only. Over main the delta also carries the base-td LOAD-BEARING marker (C-168's
   ruling (a), `1d58881`) and the 21-line RD-288 comment rewrite (`fc0278d`, C-168 :1727). All three comment changes are authorised; **the DECLARATION delta is exactly
   the two deletions (MEASURED).** The new marker comments put `#f8f9fa`/`#ffffff` into `dark-mode.css` comments (k3).
5. **RD-686 READY :23 "the snippets are in the commit message"** — FALSE: the commit message carries the claimed VALUES, no probe code (READ, `git log -1 --format=%B
   8962a14`). The gate writes its own probes.
6. **Builders' merge-trees were mostly against OLDER heads:** RD-204/RD-197 vs RD-286 `a09dd83` and each other's older heads (`cd589e0`); RD-692 vs RD-286 `fc0278d`;
   RD-693 vs RD-286 `c219890`; RD-686 "not run". Only RD-286's READY ran against the current six. The drafter ran none (forbidden to it); §11 Q1 runs all 15 pairs.
7. **RD-692's file question ((a) new file vs (b)) — whether Tuesday ruled is UNVERIFIED** (not in CLARIFICATIONS; READY :6 "still pending"). The gate grades the file as built.
8. **"RD-705 is gated in batch 5a"** — CONFIRMED only as a DRAFT: a batch-5a brief appeared during drafting
   (`briefs/2026-09-27_nexusai-gate-batch5a-rd681-rd682-rd627b-rd695-rd705-rd413.md`, 09:47, names `e164d1a`, routing name `QA/NexusAI-batch5a`), not yet
   launched at 09:47. Whether batch 5a merges before this gate's M0 decides row b9. RD-705 is on origin at `e164d1a`.
9. **OPTIONAL H — RD-694 item 4 "built @ 1d457ce, READY pending":** `1d457ce` is a LOCAL branch `rd-694-fixture-about-s86p`, **NOT pushed to origin** (ls-remote 09:28: no
   ref). Including H needs a push (lane 4's) and a READY; the launcher refuses an unpushed head.
10. **OPTIONAL G — RD-430 at `9ba6f1d` carries main's counts (4133/247) while adding a test file** (C-89 at that head). The re-pin under C-175 must regenerate them.
    **And U9: removing the form is predicted to move RD-204's settings pins (155/155), which C-175's grant does NOT cover ("Not covered: any other pin") — if G
    is to ride with RD-204, Tuesday needs a ruling first (see the report-back).**
11. **"No deploy":** `deploy-demo.yml` STARTS on every push to main whose paths are not all `**.md`/`docs/**`/`tests/**` — every member qualifies. Whether its build
    (`az acr build`) and deploy jobs run depends on `vars.CI_DEPLOY_ENABLED` and the `demo` reviewer — UNVERIFIED by the drafter (§12 reads it).
12. **RD-204's painting list is derived by a script OUTSIDE the repo** (`session-tools/s84p/rd204/derive-families.js`) with a DIFFERENT "paints" reading from the
    in-repo `paintingRulesOf` (custom properties vs literal properties) — READ; the gate measures the consequences (c5-c10).
13. **CI and PR state on all six heads: UNVERIFIED** (no `gh` run at drafting).
14. **The routing line `QA/NexusAI-batch6|tuesday-agent@agentmail.to|no` is NOT yet in `fleet/inbox_routing.conf`** (the drafter may write only the two output files);
    the launcher refuses (exit 40) until Tuesday adds it.
15. **Kam's grant re-affirmation "2026-09-27 ~08:2x"** — RELAYED from the commission; the drafter did not read Kam's board. C-175 (:1801) carries the merge-author rule.

## PROVENANCE (drafter, 2026-09-27 09:25–10:30 AEST, read-only)
- origin heads (six branches + main + rd-430 + rd-705; rd-694-fixture-about absent) | `git ls-remote origin <refs>` | 09:28:31
- chains, parents, merge-bases with `1904765`, counts at every chain sha | `git log --format='%H %P %s'`, `git merge-base`, `git show "${S}:scripts/verify-expected-counts.json"` | 09:29–09:45
- deltas, numstat, name-status, pairwise overlaps (28 pairs incl. G and H) | `git diff --name-only|--numstat|--name-status`, `comm -12` | 09:33
- tips counts-only (`83e5a1b..fe47bb4`, `cd589e0..43e729c`, `3dcd1c0..4580829`), forward-merge contents, placeholder counts at `83e5a1b`/`cd589e0` | `git diff --name-only`, `git show` | 10:0x
- RD-693 product diff and cell titles; RD-286 dark-mode.css diff + comment-stripped declaration diff (python difflib); RD-686 full diff + commit message; RD-204 dom.js
  diff, painting-list entries, derive-families.js, fetched copy's sha384 (openssl); RD-197 cell header; RD-692 cell titles | `git diff`, `git show`, `python3`, `openssl dgst -sha384` | 09:35–10:05
- blob identities (tokens.css, derive-brand-tokens.js, package-lock, package.json, dark-mode.css, entra-provisioning-ui.js, dom.js, css-colors.js, BRAND.md, settings.html,
  settings.js, rd200 fixture, vendor-surface.css, playwright.config.js) at nine shas; `__tests__` file count 289 at main | `git rev-parse "${S}:${P}"`, `git ls-tree` | 10:0x
- consumer censuses (entra-provisioning-ui 8 cells + fixture; dark-mode.css 29; dom.js 33; css-colors 4; BRAND.md 9; vendor-surface 7 + fixture; settings.html 26; nx-sus-rank;
  rd200 fixture 1; pagehide/pageshow 2 in static) | `git grep -l`, scoped to `__tests__`, `tests`, `static` | 09:5x–10:0x
- page wiring (settings.html :863, first-run-setup.html :14/:2307, index.html :1003, meta no-store :6) | `git grep -n` over `static/*.html` | 10:1x
- deploy-demo.yml triggers and job gates (:27-32, :53, :91, :95); deploy.yml dispatch-only | `git show 1904765:.github/workflows/…` | 10:1x
- builder evidence (s85p: rd693-hold.log, rd692-hold.log, rd686-verify.log, rd286-hold.log/-verify.log/-hold.sh/-evidence/, rd204-hold.log, rd204-t2b.log, rd197-verify.log,
  rd197-mverify.log, rd430-hold.log, yield-log.md; s84p: rd197-proof.log, rd204/; s86p: rd430-repin-hold.log, rd694-verify.log) — VERDICT lines and presence | `ls`, `grep -a`, `tail` | 10:0x–10:1x
- `scripts/qa-surface-up.sh` worktree use (:159-211); `playwright.config.js` header; the rd286 spec header and cell titles | `git show 1645c69:…` | 10:1x
- the batch-2 gate report (R8 :105, R11 :110, S-4 :376, A-F1 :315/:329-333, C-F1 :317/:337, A-N5 :321, A-N4 :322, §3.6 :122-128, §3.9 :144-150) and its evidence
  listing (qa-a-browser.js :32, :306) | `grep -n`, `sed -n`, `ls` | 09:4x
- CLARIFICATIONS ids (C-02 :30, C-15 :94, C-18 :109, C-28 :153, C-40 :225, C-49 :299, C-57 :410, C-61 :489, C-68 :657, C-89 :827, C-96 :893, C-97 :900, C-98 :906, C-103 :955,
  C-104 :972, C-110 :1101, C-112 :1141, C-122 :1278, C-125 :1320, C-130 :1386, C-131 :1407, C-133 :1426 + ADDENDUM :1434, C-141 :1480 + :1484 + :1488/:1490/:1492/:1494, C-142
  :1503, C-150 :1570, C-166 :1700, C-168 :1719, C-171 :1749, C-172 :1756, C-173 :1765, C-174 :1784, C-175 :1794, C-176 :1805, C-177 :1814, C-178 :1830, C-179 :1839 highest);
  313,569 bytes, 1,847 lines, mtime 09:09 | `grep -n -i '^\*\*C-<n>\.'`, `sed -n` | 09:4x
- negative-control seats %19 → 62649 (M), %21 → 9959 (N), %22 → 20317 (P), %0 → 23230 (Tuesday; parent bash 22288), %23 → 36118 (batch-3 gate), %24 → 40285 (batch-4
  gate), %25 → 16516 (QA/Vision-gate9, another project) | `tmux list-panes -a -F …`, `pgrep -P`, `ps` | 09:31:51
- jest lock owner `s86m-rd594-hold` since 23:17:43Z, ~11 queued tickets | `cat session-tools/locks/nexusai-jest.lock/owner`, `ls queue-jest/` (read only) | 09:3x
- routing: NOT written by the drafter; `QA/NexusAI-batch1` :114, `-batch2` :109, `-batch3` :122, `-batch4` :123 present; `-batch6` absent | `grep -n -i batch` | 09:3x
