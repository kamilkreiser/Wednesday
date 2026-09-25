# QA Agent Invocation Brief — Datasec/NexusAI, ONE batched gate "batch #1": RD-447 (TIER 1) + RD-411 (TIER 1) + RD-533 (TIER 2) + RD-627a (TIER 1) + RD-315 (TIER 1) — five targets, five verdicts, one report

**Drafted for Tuesday 2026-09-26 09:05–09:40 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.**
Commissioned on Tuesday's batch #1 commission (2026-09-26) and four READY FOR QA mails on disk, read whole, plus RD-447's facts RELAYED in
the commission (its READY is NOT saved in `briefs/` — `ls briefs | grep -i rd447` → nothing):
- **A — RD-447** @ `911e706859cbbe49ef32d4166ab9b3271bf98d08` (NexusAI-O) — **no READY on disk; facts RELAYED by the commission, cross-read
  against the builder's own logs (§1 Target A)**.
- **B — RD-411** @ `ed01f7eb02430de74ccaaa6d6f265c7638e5aab4` (NexusAI-O) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd411-READY-mail.txt`
- **C — RD-533** @ `95c3c9a9d39429f9093270e283e531f3cda4e88d` (NexusAI-M) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd533-READY-mail.txt`
- **D — RD-627a** @ `057016de2b2929c23f643b7346413199f370d3ce` (NexusAI-N) — the UPDATED READY
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd627a-READY-updated-mail.txt`, and for WHAT
  CHANGED / cells / NOT TESTED the first READY `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd627a-READY-mail.txt`
  (the updated READY :16 says those sections are "Unchanged from the first READY").
- **E — RD-315** @ `1524fca7ec72b23a4f000b77872a4158f8e14f86` (NexusAI-M) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd315-READY-mail.txt`
**Batched under the 2026-09-18 batch-gates rule** (as batch #2, `2026-09-26_nexusai-gate-batch2-rd428-rd444-rd200.md:11`). **Unlike batch #2 the
five deltas are NOT pairwise file-disjoint:** RD-447 and RD-411 both edit `__tests__/helpers/image-manifest.js`; RD-533, RD-315 and main's
RD-579 all edit `backend/server.js` (MEASURED, §1 File overlap). **Main is MOVING tonight: the gate RE-PINS main at its own start (call it
M0) and builds the merged tree M0 + all five in its OWN scratch clone.** Every head is re-read by `git ls-remote` in the launcher, which
refuses on a mismatch.

SELF-CHECK: re-read end-to-end for contradictions | Tuesday 2026-09-26 09:24 AEST
Self-check note: read whole by Tuesday (2026-09-26 09:24 AEST); drafter WRONG list 1-13 read first and carried (RD-447 40/15 vs 40/9/49 left for the gate to resolve); main-is-moving rule accepted; tiers A=1 B=1 C=2 D=1 E=1; authority = Kam 2026-09-25 ~22:0x 'merge once tested' (merges stay Tuesday's GO).

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build these changes and you owe no builder anything. **Every line below that reports what a builder says is a
CLAIM, never evidence.** Explore two scanners that now decode wide text and read machine-shaped labels (A, B — and what they do
TOGETHER, which no builder has run), a server that now dies loudly when it cannot listen (C), an erasure that now reaches a store's
interrupted-write copies (D), and a data route that no longer invents a completion time (E), looking for any state in which **an
identifier in a shipped file goes unseen, a second server lies about running, a copy of erased data survives while the record says
"purged", or a row reports a time that never happened.**

- **RD-447 is TIER 1** (the image-content exposure gates: a missed identifier ships in the customer image). Verdict: **GO / GO WITH
  FINDINGS / NO GO at `911e706`**, plus its merged-tree result.
- **RD-411 is TIER 1** (the same gates; the READY :1 says tier 1). Verdict at **`ed01f7e`**, plus merged-tree result.
- **RD-533 is TIER 2** (operations: boot behaviour; the READY :2 says "Tier 2 per the lane plan … tier 1 if you'd rather"; the commission
  keeps 2). Verdict at **`95c3c9a`**, plus merged-tree result.
- **RD-627a is TIER 1** (erasure; the READY :2 "Tier per the lane plan: 1"). Verdict at **`057016d`**, plus merged-tree result.
- **RD-315 is TIER 1** (data correctness; the READY :2 "I'd call it tier 1"). Verdict at **`1524fca`**, plus merged-tree result.
- **One verdict PER ticket, one report, one mail.** A finding on one ticket never becomes another's verdict. **A finding that exists only
  in the COMPOSITION (A+B on the helper, C+E on the server entry point) is graded on the merged tree and named against BOTH tickets'
  merged-tree lines, never silently against one.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **None of RD-447, RD-411, RD-627, RD-315 appears in `CLARIFICATIONS.md`; RD-533 appears only as a ticket name** (drafter, `grep -n -i -E
  'RD-447|RD-411|RD-533|RD-627|RD-315'` → 2 lines, :520 "RD-533 (a second server on the same PORT logs "running", never listens …" and
  :1108 "an RD-533-shaped foreign server never listens"; positive control, same file and tool: `C-141` found at :1480). The rulings that
  bind these tickets are **Tuesday's, RELAYED by the builders, not read by the drafter in Tuesday's mail**:
  - RD-447 + RD-411 as ONE gate, "your 13:15Z ANSWER" (RD-411 READY :2); the merge ORDER after a GO "RD-447 first, then RD-411 merged
    forward, per your mail" (RD-411 READY :24).
  - RD-411 — the 24-char window is "RD-386's question, Kam's" and is deliberately UNCHANGED (READY :12, :29).
  - RD-627a — "It is NOT stacked, as you ruled" (first READY :2); the merge-forward onto 11666d3 on "Tuesday ANSWER 2026-09-25T15:56:53Z"
    (commit message of `057016d`, MEASURED by `git log`).
  - RD-315 — "Yields: 0 self-applied since your 19:19:22Z ruling" (READY :24).
- **Merging is Tuesday's GO (Kam, 2026-09-25 ~22:0x, "work your way through the tickets and merge once tested", as recorded in the batch #2
  brief :44); this gate merges nothing into anything the fleet can see.**

**The clarifications that bind this gate** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md`,
280,969 bytes, mtime 2026-09-26 08:18:55; line numbers read by `grep -n` at 09:1x AEST — the file grows during the night, re-read them):
- **C-02** (:30) a local run serves every page and API with no sign-in (open mode on a fresh DATA_DIR) — the surface RD-315 and RD-533 drive.
- **C-28** never write, pull, check out or stash NexusAI's `2_Project_Files` (line per the batch #2 brief :50, :153; re-read it).
- **C-40** a check must be able to fail on the thing it claims (batch #2 brief :51). **C-49** the prior-work check. **C-76** an explanation is
  a claim. **C-97/C-98** fixtures change, not policy; cells assert the property after the fix.
- **C-57** (:410) a conflict confined to the counts file is resolved by REGENERATION with the id-superset control ("merged N ⊇ A M ∪ B K;
  missing 0"); any other conflicting file STOPS; suites no fewer than the larger parent's (step 4).
- **C-68** (:657) a verdict holds only at the head it ran on; a semantic overlap git cannot see is re-run by NAME; counts regenerated ONCE on
  the tree after the merge — **"No conflict is not evidence the number is right"** (its 2026-09-18 amendment). **"A clean merge-tree and a
  changed measured surface are not in tension, and the clean result is what makes the change invisible"** (:660) — **this batch's two
  textual auto-merges (the helper, the server entry point) are exactly that case.**
- **C-89** (:827) after a merge commit: `git diff --quiet HEAD` and HEAD's counts equal the regenerated numbers.
- **C-104** (:972) an instrument that enumerates from `git ls-files` TRIPLES its population during an unresolved merge — **never run a census, a
  suite or the id-superset control in a clone with an unresolved merge; resolve (stage) first, then run.** RD-447/RD-411's own helper
  (`shippedFiles`) and several gates enumerate tracked files — C-104 applies to THEM, not just to your instruments.
- **C-110** the floor rule. **C-112** (:1141) a declared limit is where the evidence stops, not a place it is cleared. **C-122** source text does
  not cover behaviour. **C-125** the foreign-server counter.
- **C-133** (:1426) base-aware id accounting, **and its ADDENDUM (:1434, 2026-09-26, from batch #2): "an AUTHORISED RENAME is ACCOUNTED, not a
  STOP, when the old->new id pair is named and the new id is present and green in the merged set."** Cite only if the id-superset control
  misses. **Drafter's prediction: nothing to account** — no branch modifies or deletes an existing test FILE (every `__tests__` change in
  the five deltas is `A`, except the helper `helpers/image-manifest.js` `M`, which carries no test ids; `git diff --name-status`, §1).
- **C-141** (:1480) a builder's proof ticket YIELDS to a `qa-*` ticket; **ADDENDUM** (:1488) a merge hold is gate-class; **ADDENDUM 2** (:1490)
  "yield once" is once PER WAITING GATE TICKET; **ADDENDUM 3** (:1492) the per-gate yield is SELF-APPLIED and a routine yield is LOGGED, not
  mailed — so every one of your holds is a separate `qa-*` ticket the builders yield to without a mail from anyone.
- **C-142** (:1494) what "green" means at a merge (local verify through the lock AND CI's known failing set).
- **Read, not binding here:** **C-163** (:1657, what the customer image ships — context for which files RD-447/RD-411's `shippedFiles` must
  see); **C-165** (:1678, RD-460 package files onto main — a separate item, may move main); **C-166** (:1689, RD-430 form removal — **the
  highest C-number at drafting**; its backend routes are "in lane 1's file", i.e. the server entry point, not yet built).

## PRIOR ROUND
- **RD-447 ← the RD-429 tier-2 gate, finding F1** (the helper's own comment at `911e706`: *"A shipped UTF-16LE .bat with a labelled ID and the
  fleet inbox passed all three gates (RD-429 tier-2 gate F1)"* — READ from `git diff 7c47ec4 911e706`). The drafter did not open that
  report; **find it in `Testing Agent MAIN/projects/nexusai/reports/` by NAME (`ls | grep -i 429`), read F1, and say whether RD-447 closes
  exactly it.**
- **RD-411 ← S59's WIP `c026e94`** ("saved by S60 as found: not re-verified, not gated, 255 behind"; READY :26). **RD-627a ← "gate 5 F-A1,
  F-A2"** (the helper comment in `backend/customerDataFiles.js` at `057016d`); **its T4 re-drive shares RD-639's B-F1** (the previous
  gate's finding, `2026-09-25-gate-rd579-rd639/report.md` §3.5 :232-237 — *"RD-639's false certificate returns one sweep later"*), now
  ticketed RD-684 (updated READY :16, RELAYED). **RD-533 ← "an RD-533-shaped foreign server never listens"** (CLARIFICATIONS :1108) — the
  fleet's own floor counter has had to live with this defect. **RD-315 ← RD-306 half 2** ("removed the same fabrication in the parser; this
  is its sibling", READY :17, RELAYED).
- **The two previous batched gates — their METHOD and their SELF-CORRECTIONS are your inheritance:**
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/report.md`
  (§6 merged tree :291-310; §10 S-1..S-7 :372-379; §11 floor table :381-393) and
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/report.md` (§8 S-1..S-6
  :337-343; §3.5-3.6 the erasure re-drive and inside-DATA_DIR links :232-243; §4 merged tree :259-272). **§3a below keeps H-1..H-6 (from
  rd579-rd639's S-1..S-6) and adds H-7..H-12 (from batch #2's S-1..S-7 and its §6.6 C-57 surprise).** Reuse batch #2's corrected
  instruments BY COPY from `…/2026-09-26-gate-batch2-rd428-rd444-rd200/evidence/`: `qa-floorlib.sh`, `qa-floorcount.py`, `qa-dispatch.sh`,
  `qa-holdlib.sh`, `qa-mutate.py`, `qa-merge.sh`, `qa-mkarm.sh`, `qa-mkarm-clone.sh`, `qa-ssprint.sh`, `qa-h1-selftest.sh`, `qa-h1-scan.py`,
  `qa-c57-id-superset.sh`, `qa-netbelt.sb`, `qa-to.sh` (all present, `ls` at 09:2x AEST).

## 1. Targets — verified at drafting from the object store (09:06–09:30 AEST)
**origin by `git ls-remote` at 2026-09-26 09:06:26 AEST:**
`main` **`12b5edc31ee4ef52415d1cbffbbb0504d7f4715c`** · `rd-447-utf16-scan-s84o` **`911e706859cbbe49ef32d4166ab9b3271bf98d08`** ·
`rd-411-machine-labels-s84o` **`ed01f7eb02430de74ccaaa6d6f265c7638e5aab4`** · `rd-533-listen-eaddrinuse-s84m`
**`95c3c9a9d39429f9093270e283e531f3cda4e88d`** · `rd-627a-erasure-tmp-siblings-s84n` **`057016de2b2929c23f643b7346413199f370d3ce`** ·
`rd-315-no-fabricated-completion-s84m` **`1524fca7ec72b23a4f000b77872a4158f8e14f86`**. (Also read: `rd-200-js-colour-corpus-s84p` = `12b5edc` —
**main was FAST-FORWARDED to RD-200's head; there is no RD-200 merge commit**; `rd-428-provisioning-residue-s84p` `823ef9e`,
`rd-444-gitignore-symlink-s84p` `2f9da1c`, both not yet on main.)
**Re-read all six at your start, mid and end. A moved TICKET head is a finding and a reason to stop, never a typo to fix. A moved MAIN is
expected** (NexusAI-P is merging RD-444 and RD-428 tonight, per the commission) — see "Main is moving" below.

**Main's line at drafting (MEASURED, `git log --format='%H %P' 7c47ec4..12b5edc`):** `cac9cf6` (RD-579, parent `0677388`), `fe53540` (RD-639,
parent `7c47ec4`), `0863711` (merge 1, parents `cac9cf6` `7c47ec4`), **`11666d3c4f615190646914270016419fffa642e2`** (merge 2, parents `fe53540` `0863711`), `4f97260` (RD-200, parent
`7c47ec4`), `c01190d` (forward merge, parents `4f97260` `11666d3`), **`12b5edc`** (RD-200 counts, parent `c01190d`). Counts **4021/238**
(`git show 12b5edc:scripts/verify-expected-counts.json`).

**Main is moving — the rule.** Call main at your start **M0**. (1) M0 must be `12b5edc` or a DESCENDANT of it (`git merge-base
--is-ancestor 12b5edc M0`); (2) `git diff --name-only 12b5edc M0` must share NO path with any of the five deltas below except
`scripts/verify-expected-counts.json` (the launcher refuses otherwise; re-check it yourself). The expected movers — RD-444 (`.gitignore`, its
cell) and RD-428 (9 files, batch #2 brief :107-111) — share none (drafter's `comm -12` of those name lists against the five deltas). (3) Your
merged tree is **M0 + all five**, predicted counts **counts(M0) + 96 tests / + 5 suites** (at M0 = `12b5edc`: **4117/243**; if RD-444 and
RD-428 have both landed and main measures 4037/242 as batch #2's merged tree did: 4133/247 — ARITHMETIC; C-68 says the measurement decides).
(4) If main moves AGAIN during your gate, your verdict names M0 and you say what moved (C-68). **Never re-base your merged tree mid-gate.**

### TARGET A — RD-447 (TIER 1)
- **ONE commit off `7c47ec467f585e9db5daf3a82cdb96deae0b1e7a`** (MEASURED): `911e706` "RD-447: the image-content gates decode UTF-16/UTF-32 text
  instead of spacing its NULs", parent `7c47ec4`, **change and counts in the same commit** (no counts-only tip). `merge-base(911e706, 12b5edc)
  = 7c47ec4`.
- **Delta over `7c47ec4`: 3 files, +287/−8** — `M __tests__/helpers/image-manifest.js` (+99), `A __tests__/rd447-utf16-text-is-decoded.test.js`
  (190), `M scripts/verify-expected-counts.json`. **Test-helper change only: no product file.**
- **Counts: `7c47ec4` 3978/235 → `911e706` 4033/236** (+55/+1; MEASURED).
- **What changed (READ, `git diff 7c47ec4 911e706`):** `BOMS` (UTF-32LE/BE, UTF-8, UTF-16LE/BE, longest first); `sniffWide(buf)` (no sniff under 8
  bytes; UTF-32 by ≥90% NULs in three of four lanes and <10% in the fourth; UTF-16 by ≥40% NULs in one parity and <5% in the other);
  `decodeAs` (TextDecoder for UTF-16; a hand loop for UTF-32, surrogates and >U+10FFFF → U+FFFD, a trailing partial unit → U+FFFD);
  `decodeText(buf)`; `WIDE_RUN` + `unwiden` for a STRING already read as UTF-8 (3+ char+NUL pairs lose their NULs, the run's ends become one
  space); `scannableText(relPath, content)` now takes BYTES or a string (a NUL in bytes + a binary extension → `null`, checked BEFORE
  decoding); **`readTracked` now reads BYTES** (`fs.readFileSync(path.join(ROOT, f))`, no `'utf8'`); `decodeText` and `readTracked` exported.
- **Cells (READ, `git grep -n describe`):** 7 describes at :72 PRECONDITIONS, :84 "three gates find a labelled ID and the inbox in wide text read as
  BYTES", :108 STRING path, :119 "the default reader reads bytes, and that changes nothing for the tree as it is", :136 "does not flag a wide
  file with nothing in it", :144 CONTROLS, :176 decoding details.
- **RELAYED (commission) and CROSS-READ against the builder's logs by the drafter:** 55 cells; red at `7c47ec4` 40 failed / 15 passed
  (`session-tools/s84o/rd447-hold.log:76` "Tests: 40 failed, 15 passed, 55 total" ✔); M1 (string rule removed) exactly 6 red (:193 "6 failed, 49
  passed" ✔); M2 (reader back to utf8) exactly 1 red (:252 "1 failed, 54 passed" ✔); restored 55/55 (:311 ✔); verify 4033/236
  (`rd447-verify.log:17105` "VERDICT: PASS — 4033/4033 tests passed across 236 suites" ✔). **DISCREPANCY:** the separate
  `rd447-red-7c47ec4.log:997` reads **"40 failed, 9 passed, 49 total"** — a 49-cell file, not the committed 55. Find out which cell file that
  log ran (an earlier draft?) and say so; your own red-proof decides.
- **Declared limits** (no READY on disk; the helper's own comment at `911e706`, READ): **L-A1** *"This path is exact for ASCII only: read as
  UTF-8, a non-ASCII UTF-16 character can come out as stray ASCII bytes (U+4E2D is "-N")"* (the STRING path). **L-A2 (drafter-read, not
  declared):** `sniffWide` returns `null` for any buffer under 8 bytes and when the NUL ratios miss the thresholds (e.g. BOM-less UTF-16 whose
  text is mostly non-Latin, where the high bytes are not NUL). **L-A3 (drafter-read):** a NUL-bearing file with a binary extension is `null`
  BEFORE decoding, so UTF-16 text renamed `.png` is not scanned (unchanged from the base — the old code also returned `null` for NUL + binary
  extension — say whether that is still true).

### TARGET B — RD-411 (TIER 1)
- **Chain (MEASURED):** `7be79f041a98e09655d067aedc9d8dcbc0e03ac4` (the change, parent `7c47ec4`, **2 files, no counts**) → **`d81cd973ed175735b509b22f4af5e0b98f067ae8`
  (forward merge of main: parents `7be79f0` `11666d3`)** → `ed01f7e` (**counts only**: `git diff --name-only d81cd97 ed01f7e` = the counts file;
  committed 09:04 AEST, two minutes before the drafter's ls-remote). **`merge-base(ed01f7e, 12b5edc) = 11666d3`** — RD-411 contains main as of
  merge 2, **not RD-200** (READY :6: "Main has since moved to 12b5edc … the branch is NOT re-merged onto it"). `git diff --name-only 11666d3
  d81cd97` = RD-411's two files only.
- **Delta over `11666d3`: 3 files, +147/−7** — `M __tests__/helpers/image-manifest.js` (+33), `A __tests__/rd411-machine-shaped-labels.test.js`
  (115), counts.
- **Counts: `7be79f0` 3978/235 (unregenerated) · `d81cd97` 4012/237 (main's) → `ed01f7e` 4040/238** (+28/+1 over `11666d3`; MEASURED).
- **What changed (READ, `git diff 7c47ec4 7be79f0`):** `LABEL` = `\b(tenant|…|application)(?:\b[^\n]{0,24}\b|)(ids?)\b/i` (the joined form
  `tenantid` added; the 24-char window unchanged); `labelForm(line)` (camelCase humps split; an acronym run before a word split, `AADTenant`
  → `AAD Tenant`; `_` and `-` → space); `hasLabel(line)` = `LABEL.test(labelForm(line))`, used by BOTH `identifierSignals` and `signalLines`;
  the GUID still matched on the ORIGINAL line; `labelForm`, `hasLabel` exported.
- **Cells (READY :16, as sets, 28):** 19 machine shapes (each labelled-identifier 1 AND the signal line); reviewed-file reopen ×3 (env, JSON, snake) on
  `TERMS_OF_SERVICE.md` + PRECONDITION; a new env-var file flagged "not reviewed"; CONTROLS (prose labels; no-label CSV row, `tenantName`,
  `clientIdentity`, `identity`, `requestId` → 0; GUID from the original line; shipped tree has no unreviewed carrier and the detector is live).
- **Builder's claims:** base `7c47ec4` 24 failed / 4 passed; fix 28/28; M1 (`labelForm` = identity) 13 red, M2 (joined alternative removed) 1 red,
  M3 (`signalLines` keeps the prose-only label) 11 red (`session-tools/s84o/rd411-hold.log`); full verify on `d81cd97`'s tree **"PASS — 4040/4040
  … across 238 suites"** (`rd411-verify.log`); "the wider label newly flags NO shipped file, so `__tests__/fixtures/image-carrier-review.json` does
  NOT move" (READY :14, measured at `7c47ec4` with UTF-8 reads — **before RD-447's decoder existed**).
- **The builder's merge-tree vs RD-447 (READY :24):** `git merge-tree --write-tree --name-only` `d81cd97` vs `911e706`, objects in a scratch dir
  (`session-tools/s84o/mt-objects`) → helper AUTO-MERGES, counts the only conflict. **Re-measured by the drafter (§1 File overlap): same result
  against `ed01f7e`.**
- **L-B1..L-B4 — declared limits, verbatim (READY :29-32):** *"The 24-char window (RD-386) is untouched, so a label and a GUID more than 24 chars
  apart on one line, or on adjacent lines, are still not linked."* · *"labelForm splits camelCase and snake only. A label glued to other words with
  no separator (for example "mytenantid") matches via the joined alternative only when "tenant" starts a word."* · *"No re-review of carriers was
  needed (none newly flagged); if a later shipped file trips the wider label, its review fingerprint changes."* · *"The merge-tree is a textual
  check; the combined suite at the merged head is the gate's to run."*

### TARGET C — RD-533 (TIER 2)
- **ONE commit off `7c47ec4`** (MEASURED), change + counts together. `merge-base(95c3c9a, 12b5edc) = 7c47ec4`.
- **Delta over `7c47ec4`: 3 files, +115/−4** — `A __tests__/rd533-listen-error-fails-loudly.test.js` (96), `M backend/server.js` (+16/−1, one hunk
  at `95c3c9a` :22561-22582), counts.
- **Counts: `7c47ec4` 3978/235 → `95c3c9a` 3982/236** (+4/+1).
- **What changed (READ at `95c3c9a`):** `app.listen(PORT, (listenErr) => {` — on `listenErr`: `why` = the EADDRINUSE remedy *"another process is
  already listening on it; stop that process or set PORT to a free port"* else *"check the PORT value and that this process may bind it"*;
  `logger.error(`❌ Could not listen on port ${PORT}: ${listenErr.code || listenErr.message}. ${why}. Exiting.`)`; `setTimeout(() =>
  process.exit(1), 250); return;`. Nothing else in the callback changed (the RD-510 warm-up, F-18 flush interval, SIGTERM/SIGINT handlers,
  F-16 banner all stay inside the success path). **On the merged tree this block sits at :22609-22624** (drafter's merge-tree emulation, §1).
- **Mechanism (READ, `node_modules/express/lib/application.js:598-605`, Express `5.2.1` per its `package.json:4`, read in the NexusAI working
  checkout's `node_modules` — re-read it in YOUR tree's):** `var done = args[args.length - 1] = once(args[args.length - 1]); server.once('error',
  done)`. So the callback is BOTH the listening callback AND the one-shot error handler, wrapped in `once`. **Consequence the READY does not
  state:** after a SUCCESSFUL listen, the `once('error', done)` listener is still attached and `done` is already spent — a later server
  `'error'` event is consumed by a no-op instead of crashing or being logged. Pre-existing (Express, not RD-533); **census it (§6 Q6), do not
  grade it on RD-533.**
- **PORT is a raw string** (`const PORT = process.env.PORT || 3001;` — merged tree :747, READ): a PORT that is a filesystem path reaches
  `listen` as a pipe/socket path. That is the cheap EACCES route (§2a-C).
- **Cells (READY :13-15):** RED at `7c47ec4`: "B exits on its own, non-zero", "B names the failure: EADDRINUSE and the port", "B never claims it is
  running"; GREEN there: "control: server A answers … before and after". GREEN at `95c3c9a`: 4. Mutants M1 `if (listenErr)` → `if (false)`
  reddens all three B cells; M2 `exit(1)` → `exit(0)` reddens ONLY the non-zero cell (`session-tools/s84m/rd533-hold.log`). Full verify **"PASS —
  3982/3982 … across 236 suites"**. Probe at base: *"both logged "running on port 38995", both stayed alive, and lsof showed one listener (A)"*
  (`rd533-probe-7c47ec4.log`).
- **L-C1..L-C5 — declared limits, verbatim (READY :23-27):** *"Linux. SO_REUSEPORT semantics differ, and CI hasn't run on the branch (no PR)."* ·
  *"Container Apps: whether one replica can ever start two processes on one port."* · *"EACCES and other listen errors: same branch, but only
  EADDRINUSE has a cell."* · *"The 250 ms delay is a pragmatic choice. The cell proves the message arrives before exit, on this Mac, over a pipe."* ·
  *"The harness (bootServer) now gets a failed boot instead of a silent second server. That is RD-490/RD-619's intended shape, but no harness
  consumer was re-run beyond the full verify."*

### TARGET D — RD-627a (TIER 1)
- **Chain (MEASURED):** `9fb94311b010c3d4355418eface0e1dc3ecd3795` (the change + counts, parent `7c47ec4`) → **`057016d` (forward merge of main:
  parents `9fb9431` `11666d3`)**, counts regenerated INSIDE the merge commit (**not** a counts-only tip; `git diff --name-only 9fb9431 057016d` =
  main's 5 files incl. the counts). `merge-base(057016d, 12b5edc) = 11666d3`. `git diff --name-only 11666d3 057016d` = RD-627a's 4 files only.
- **Delta over `11666d3`: 4 files, +264/−5** — `A __tests__/rd627a-erasure-tmp-siblings.test.js` (172), `M backend/customerDataFiles.js` (+21),
  `M backend/dataErasure.js` (+70/−1), counts.
- **Counts: `9fb9431` 3983/236 · `11666d3` 4012/237 → `057016d` 4017/238** (+5/+1).
- **What changed (READ, `git diff 11666d3 057016d`):** `isInterruptedWriteOf(name, store)` = `name === store+'.tmp' || name.startsWith(store+'.tmp.')`
  (`customerDataFiles.js`); in `purgeNow`: the data dir listed ONCE before the loop (an existing, unlistable dir → a failure `(data directory)`
  *"could not list it, so interrupted-write copies cannot be proven absent"*; ENOENT → empty list); per store, the siblings are swept **BEFORE**
  P-3's live-store stat (which `continue`s when the store is absent); `_removeInterruptedWrite` decides by `lstat`: directory → `_purgeTree`;
  symlink → `realpathSync` then `unlinkSync` the LINK, a surviving target → failure *"symlink removed but its target still holds the data:
  <target>"*; dangling link → purged; else unlink; ENOENT on lstat → nothing recorded. **Merged-tree blob `09e34f6` = `057016d`'s** (main after
  `11666d3` did not touch `dataErasure.js`).
- **The stores (READ, `customerDataFiles.js` at `057016d`):** 22 customer stores (`settings.json` … `notification_state.json`, incl. the directory
  store `feedback-attachments`, `audit-buffer.json`, `sessions.json`); `.machine-id` and `.persistence-sentinel.json` are infrastructure and NOT
  purged. **No store name contains a path separator** — the one top-level `readdirSync` reaches every store's siblings.
- **Cells (first READY :9):** POPULATION; T1 both forms beside all 22 stores; T2 `audit-buffer.json.tmp` with an IP needle, gone and named in the
  persisted record (`_readRawState`), no file under DATA_DIR still holds the needle; T3 CONTROL (`.machine-id.tmp.*`, `.persistence-sentinel.json.tmp.*`,
  `settings.jsonX.tmp`, `settings.json-old.tmp.1`, `not-a-store.json.tmp` all SURVIVE); T4 a symlinked sibling: target intact, link gone, run fails
  naming it. Builder's re-proof on the new main (updated READY :10-14): A on `11666d3` without the fix — T1, T2, T4 red, POPULATION and T3
  green; B on `057016d` 225/225 over 12 suites (rd627a + rd639's 26 + every `erasure-*` + rd525); C **"PASS — 4017/4017 … across 238 suites"**
  (`session-tools/s84n/rd627a/mf/`).
- **L-D1..L-D4 — declared limits, verbatim (first READY :19-22 and updated READY :16):** *"A writer's tmp that is IN FLIGHT during a purge on a live
  server. Read, not run: the sweep deletes it, and the writer's rename then fails ENOENT, so that write is lost while erasure proceeds, which is the
  intended outcome."* · *"Tmp siblings of RECOVERY copies under backups/."* · *"T4's re-drive shares B-F1, which is now RD-684 … and it closes when
  RD-684 lands."* · *"Half (b) of RD-627 (SIGTERM, lane 1)."*

### TARGET E — RD-315 (TIER 1)
- **ONE commit off `0863711261afc5f3323b8c4fc480d65109b17ba7`** (main's merge 1, RD-579), change + counts together. `merge-base(1524fca, 12b5edc) =
  0863711`. `git diff 0863711 12b5edc -- backend/server.js` = **0 lines** (merges 2 and RD-200 did not touch the server entry point; MEASURED,
  `--shortstat` empty for `0863711..11666d3` and `11666d3..12b5edc`).
- **Delta over `0863711`: 3 files, +99/−5** — `A __tests__/rd315-api-database-no-fabricated-completion.test.js` (94), `M backend/server.js` (2
  lines), counts.
- **Counts: `0863711` 3986/236 → `1524fca` 3990/237** (+4/+1).
- **What changed (READ):** in both `/api/database` transforms (print `:14242`, scan `:14294`, identical at `0863711`, `1524fca` and the merged tree)
  `jobCompletedTime: log.Job_Completed_Time_UTC || log.created_at || new Date().toISOString()` → `… || null`. `jobStartTime` already fell back to
  `null`.
- **Cells (READY :9-13):** seeded through the product's own `SimpleDatabase` into the server's `DB_PATH` BEFORE boot (a dated control, an undated
  print, an undated scan/DigitalSend); RED at `0863711`: "print: an undated row gets jobCompletedTime null" and "scan: …" (both came back with the
  REQUEST TIME); GREEN there: the control and "findability: the undated print row and the undated scan row are both in the response". M1 (old
  fallback at :14242) → ONLY print red; M2 (at :14294) → ONLY scan red. Full verify **"PASS — 3990/3990 … across 237 suites"**
  (`session-tools/s84m/rd315-hold.log`).
- **The census the READY declined (READY :22) — drafter's starting list, READ ONLY on the merged-tree emulation (line numbers equal at `1524fca`;
  RD-533's insertion is below them):** `new Date().toISOString()` appears on **39** lines (41 at `0863711`; the 2 removed are RD-315's). **`||`/`??`
  followed by `new Date().toISOString()`: 0 on the merged tree — positive control, the same grep on `0863711`: 2** (RD-315's two lines). **But the
  class has other spellings** (`grep -i -E`, same file): `:19480` and `:19789` `const date = job.TimeGenerated ? job.TimeGenerated.split('T')[0] :
  new Date().toISOString().split('T')[0];` · `:19926` and `:20031` `new Date(job.Job_Start_Time || Date.now())` · `:10036`, `:10037`, `:10046`
  `… _parsedDate || new Date()`. Each is a CANDIDATE, not a finding: classify every one (§8 Q5).
- **L-E1..L-E3 — declared limits, verbatim (READY :20-22):** *"The Log Analytics path: only the SQLite path is seeded. The LAW parser already yields
  null for missing times since RD-306, but that isn't driven here."* · *"No real browser render of an undated row. The null handling was read, not
  driven."* · *"The other 23 `new Date().toISOString(),` sites in server.js are outside this ticket and were not surveyed for the same class."* (The
  "23" checks: 25 lines contain `new Date().toISOString(),` at `0863711`, 23 on the merged tree — MEASURED.)

### File overlap — NOT disjoint this time (MEASURED, READ ONLY)
Name sets over each head's merge-base with main: A = `7c47ec4..911e706` (3), B = `11666d3..ed01f7e` (3), C = `7c47ec4..95c3c9a` (3), D =
`11666d3..057016d` (4), E = `0863711..1524fca` (3); M = `7c47ec4..12b5edc` (9). Pairwise `comm -12`:
- **A∩B = `__tests__/helpers/image-manifest.js` + counts.** **C∩E = `backend/server.js` + counts.** **C∩M = `backend/server.js` + counts** (RD-579's
  +52/−7 in `7c47ec4..0863711`; RD-533 is off `7c47ec4`, so RD-579 is not in its base). Every other pair = the counts file only. (D∩M and E∩M
  read as `dataErasure.js` / `server.js` only because D and E already CONTAIN those main commits — against main-since-their-own-base they
  share the counts file only.)
- **Drafter's merge prediction, MEASURED with `git merge-tree --write-tree --name-only` (git 2.54.0) with `GIT_OBJECT_DIRECTORY` = a scratch dir in
  the drafter's own scratchpad and the NexusAI store as a read-only alternate; `git count-objects -v` in NexusAI = `count: 1120` before and after:**
  each head vs `12b5edc` → rc 1, counts only (RD-533: "Auto-merging backend/server.js"); `911e706` vs `ed01f7e` → "Auto-merging
  __tests__/helpers/image-manifest.js", counts only; `95c3c9a` vs `1524fca` → "Auto-merging backend/server.js", counts only; **the chain `12b5edc` +
  911e706 + ed01f7e + 95c3c9a + 057016d + 1524fca (trees, bases emulated with `--merge-base`) → counts the ONLY conflict at every step.** Merged
  (pre-regeneration) blobs: `helpers/image-manifest.js` **`07e8711`** (= NEITHER parent: `911e706` has `c6b2fb9`, `ed01f7e` has `b46519b`, base
  `3ca9abc`); `backend/server.js` **`bc099b2`** (= no parent: `12b5edc` `30aeff7`, `95c3c9a` `399615b`, `1524fca` `8261524`); `backend/dataErasure.js`
  `09e34f6` and `backend/customerDataFiles.js` `708c38b` (= `057016d`'s); `helpers/css-colors.js` `78bb004`, `docs/BRAND.md` `5fa08fa` (main's).
  **`node --check` on the two content-merged files as merge-tree wrote them: rc 0 and rc 0.** Merged `__tests__`: **285 files**, `12b5edc` has 280.
- `package-lock.json` is blob `9064763`, `package.json` `cdb1168`, `scripts/verify-suite.sh` `eb9731f` at `7c47ec4`, `12b5edc` and all five heads.
- **Re-prove every line of this yourself in your OWN clone; the drafter's emulation is a prediction.**

### How to build your trees
- **No worktree is created in the NexusAI repo, and you never work in its `2_Project_Files` checkout (C-28).** In that repo use ONLY read verbs:
  `show`, `log`, `diff`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `grep`, `ls-remote`, `archive`, `count-objects`. Never `fetch`, `pull`,
  `push`, `checkout`, `worktree`, `commit`, `stash`, `gc`, `clean`, or `merge-tree --write-tree` without a scratch `GIT_OBJECT_DIRECTORY` of your own.
- **Head trees:** `git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/qa-trees/batch1.XXXXXX/>`, git-indexed where a full verify or a cell needs
  a git tree (suites read `.github` / `node-version`; RD-447/RD-411's helper enumerates tracked files — **an un-indexed tree gives it a different
  population: prove the population equals `git ls-tree -r` at the head, C-104's cousin**).
- **The merged tree:** §9, in **your OWN scratch clone** (`git clone --shared --no-checkout <repo> <your own dir>`).
- **Each tree is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree for a clean arm; `batch1`-prefixed
  directories only. Nothing in another gate's `qa-trees/*`, the builders' `worktrees/` or `session-tools/` is run in — read only.
- `node_modules`: an APFS clone (`cp -c -R`) of the newest gate tree you trust, **after proving** `package-lock.json` is blob `9064763` there too; a
  real directory, never a symlink.

## 2. Why these tiers, and who is waiting
- **RD-447 and RD-411 TIER 1:** these helpers decide which shipped files carry a customer or Datasec identifier into the Marketplace image
  (`shippedFiles`, `identifierSignals`, `unreviewedCarriers`, `carrierFingerprint`). **Any identifier-shaped plant (a labelled GUID, the fleet inbox,
  an email) in a shipped-shape file that the merged helper does not flag is a Major; a shipped file in the REAL tree newly flagged and unreviewed
  on the merged tree is a Blocker for the merge (it means the image ships a carrier nobody reviewed).** A false positive on a benign line is a Minor.
- **RD-533 TIER 2:** a server that cannot listen must never say it is running. **A path on which the process logs "running" or keeps running
  without listening, or exits 0 after a listen failure, is a Major; exiting while the real server A is disturbed is a Blocker.**
- **RD-627a TIER 1:** an erasure is a customer-data-rights statement. **Any byte of a planted needle surviving under DATA_DIR (or behind a
  symlinked sibling) while the persisted record says "purged" is a Blocker; an infrastructure file removed (`.machine-id`) is a Blocker (the
  deployment cannot decrypt, per the comment at `dataErasure.js:45-47`); a sibling removed but not named is a Major.**
- **RD-315 TIER 1:** a report that stamps "now" on an unknown completion is fabricated data. **Any `/api/database` row returning a time that is not
  in the stored row is a Major.** A remaining fabrication site elsewhere is a CENSUS entry (a new-ticket recommendation), not RD-315's verdict,
  unless it sits in the same two transforms.
- **The queue.** Four NexusAI seats (M, N, O, P) share the jest lock; P is merging RD-444/RD-428, M is on RD-413, N queues rd684-proof, rd324-mf,
  rd424-r2, rd314-mf (updated RD-627a READY :18). Expect a live queue; the builders self-yield to each of your `qa-*` tickets (C-141 ADDENDUM 3).

## 2a. LEGITIMATE SHAPES — required measurements, row by row, base and head(s) in the same window
**A+B — the composed scanner (RD-447 × RD-411). Plant each row as BYTES (Node `Buffer`, never a shell `echo`/`printf` or `JSON.stringify` — H-9)
in a scratch copy, verify the first 8 bytes with `xxd`, and run `identifierSignals(scannableText(f, bytes))`, `signalLines`, and
`unreviewedCarriers` over it, at `911e706`, `ed01f7e` and the MERGED tree, same window. `G` = a fresh random GUID per row.**

| row | plant (encoding · text) | `911e706` | `ed01f7e` | merged | predicted-by |
|---|---|---|---|---|---|
| a1 | UTF-8 · `Workspace ID: G` | 1 | 1 | 1 | builder (control) |
| a2 | UTF-8 · `AZURE_TENANT_ID=G` | 0 | 1 | 1 | builder (RD-411) |
| a3 | UTF-16LE+BOM · `Workspace ID: G` | 1 | 0 | 1 | builder (RD-447) |
| **a4** | **UTF-16LE+BOM · `AZURE_TENANT_ID=G`** | **0** | **0** | **1** | **drafter — only the COMPOSITION finds it; no cell of either branch pins it** |
| a5 | UTF-16BE+BOM · `"tenantId": "G"` | 0 | 0 | 1 | drafter |
| a6 | UTF-16LE, NO BOM (NUL stride) · `tenant_id: G` × 10 lines | 0 | 0 | 1 | drafter |
| a7 | UTF-32LE+BOM · `TenantID G` | 0 | 0 | 1 | drafter |
| a8 | UTF-32BE, NO BOM · `AADTenantId=G` | 0 | 0 | 1 | drafter |
| a9 | the a4 file read as a UTF-8 STRING (rd503's path) | 0 | 0 | 1 | drafter (L-A1: exact for ASCII) |
| a10 | UTF-8 file + ONE appended UTF-16LE line `clientId=G` (mixed; no BOM, sniff misses) | 0 | 0 | 1 via `WIDE_RUN` | drafter |
| a11 | UTF-16LE+BOM · `tenantName G`, `clientIdentity G`, `requestId G`, `identity G` | 0 | 0 | **0** | builder controls, widened — **a 1 is a false positive** |
| a12 | UTF-16LE+BOM · `tenantId` and G 30 chars apart; and on adjacent lines | 0 | 0 | 0 (L-B1) | builder (declared) |
| a13 | UTF-16LE text named `x.png` | null | null | null (L-A3) | drafter — say if a `.bat`/`.ps1`/`.reg` wide file is ever `null` |
| a14 | BOM-less UTF-16LE, 80% CJK + one `AZURE_TENANT_ID=G` line (L-A2) | ? | 0 | ? | drafter — **measure the sniff; a miss is a declared-limit finding, not a regression** |
| a15 | UTF-8+BOM · `AZURE_TENANT_ID=G` on line 1 | 0 | 1 | 1 | drafter (U+FEFF before the label) |
| a16 | UTF-32LE with a truncated last unit; 7-byte UTF-16 file | no crash | no crash | no crash | drafter (`decodeAs`, `n < 8`) |
| a17 | the fleet inbox `…@agentmail.to` in UTF-16LE+BOM | signal | 0 | signal | builder (RD-447 PRECONDITIONS) |
| a18 | **reviewed-file reopen:** a COPY of a reviewed carrier (`TERMS_OF_SERVICE.md` per READY :16) + an appended UTF-16LE `AZURE_TENANT_ID=G` line | fingerprint same | same | **CHANGES → "not reviewed"** | drafter |
| a19 | **the REAL shipped tree:** `unreviewedCarriers()` over the merged tree's `shippedFiles`, detector-live control beside it | [] | [] | **[] predicted** | builders measured each alone, never together |

**C — the listen failure (RD-533). Every server on YOUR loopback from YOUR tree, a fresh DATA_DIR each unless the row says shared, open mode
(C-02), at `7c47ec4` and `95c3c9a` (and the merged tree for c1), same window. Record exit code, time from spawn to exit, every stdout/stderr
line, `lsof -nP -iTCP:<p> -sTCP:LISTEN`, and whether `LogFiles/*` holds the line.**

| row | shape | expected at `95c3c9a` | at `7c47ec4` | predicted-by |
|---|---|---|---|---|
| c1 | A on port p; B on the same p, separate DATA_DIRs | B exit **1**; "Could not listen on port p: EADDRINUSE. another process …"; never "running"; A answers `/api/health` before and after | B alive, "running", 1 listener (A) | builder |
| c2 | as c1 but B SHARES A's DATA_DIR | as c1 — **plus: hash A's DATA_DIR before/after B (H-5)**; B's pre-listen init (`initDataSource`, `migrateRetiredSimplexCost`, `validateSettingsIntegrity`, merged :22604-22607) — did it write into A's store? | same writes, then B lives on | drafter — pre-existing writes labelled so |
| c3 | the file log transport | `LogFiles/*` holds the ❌ line before exit (the 250 ms, C-15) | — | builder (L-C4 says pipe only) |
| **c4** | **EACCES-shaped:** PORT = a socket path inside your own `chmod 500` mktemp dir | exit 1; `EACCES`; the NON-EADDRINUSE remedy text | alive? "running"? | drafter (`PORT` raw, :747) — **discharges L-C3** |
| c5 | PORT < 1024 (a free one) as non-root on this Mac | **measure**: binds or EACCES? (macOS ≥ 10.14 is believed to allow unprivileged low ports — a drafter's CLAIM, UNVERIFIED) | same | drafter |
| c6 | PORT = `70000` (out of range) | **measure**: `listen` throws `ERR_SOCKET_BAD_PORT` synchronously → never reaches the callback → `startServer`'s `catch`: what is logged, what exit code? | same | drafter — pre-existing path, label it |
| c7 | the port held by a NON-node listener (`python3 -m http.server p --bind 127.0.0.1` or `nc -l`) | exit 1, EADDRINUSE | alive | drafter |
| c8 | a node listener on `127.0.0.1:p` only; B listens on all addresses | **measure**: does B's wildcard bind succeed beside a loopback-only holder? (relates to rd641 "reserved port binds on every address") | same | drafter |
| c9 | SIGTERM to B inside the 250 ms window | exit code recorded (143 expected: the SIGTERM handlers are registered only on the success path) | — | drafter |

**D — the erasure (RD-627a). A REAL DATA_DIR of your own; plant with unique needles; drive the product path (`requestErasure` → `purgeNow`, as the
rd579-rd639 gate did, §3.4 :194) AND on a real loopback server (its §3.4b :223); read the ledger and `erasure-audit.jsonl` RAW (H-2); at `11666d3`
(base: main without the fix) and `057016d`, and the merged tree for d1, d7, d8.**

| row | plant | expected at `057016d` | at `11666d3` | predicted-by |
|---|---|---|---|---|
| d1 | `audit-buffer.json.tmp` (bare) with an IP needle, store present | gone; named in `purged`; no file under DATA_DIR holds the needle | survives | builder (T2) |
| d2 | `<store>.tmp.<pid>` and `<store>.tmp.<pid>.<suffix>` beside all 22 stores, stores ABSENT | all gone, all named | survive | builder (T1) — **the crash case** |
| d3 | a DIRECTORY sibling `settings.json.tmp.9/` with a needle file inside; `feedback-attachments.tmp/` | tree purged, named | survive | drafter (`_purgeTree` branch) |
| **d4** | **a SYMLINKED sibling → a file OUTSIDE DATA_DIR holding the needle** | link gone; target INTACT; run fails naming the target; record `purged_incomplete` | link survives | builder (T4) |
| d5 | a symlinked sibling → a DIRECTORY outside | link gone; target intact; failure names it | — | drafter |
| d6 | a DANGLING symlinked sibling | removed, recorded purged | survives | drafter (READ: `realpathSync` ENOENT → purged) |
| d7 | a symlinked sibling → ANOTHER STORE inside DATA_DIR, both loop orders (target purged earlier / later) | say what the record says; **stale failure text is the safe direction** (rd579-rd639 report §3.6 R06/R07) | — | drafter |
| d8 | **the RD-639 rule on the merged tree:** the LIVE store is a symlink → outside, AND a `.tmp` sibling is a symlink → the SAME target | both links gone; target intact; BOTH failures named; `purged_incomplete` | — | drafter — **the two rules meet in one loop iteration** (updated READY :7) |
| d9 | **the re-drive** of d4 (sweeper LIVE, `SCHEDULER_LIVE_SEND__ERASURE_SWEEPER=true`, as rd579-rd639 §3.5) | **B-F1 class: predicted `purged` over surviving bytes** (L-D3, declared) | — | builder (declared) — measure, name it, grade it as the known B-F1/RD-684 hole |
| d10 | T3 controls: `.machine-id.tmp.1`, `.persistence-sentinel.json.tmp.1`, `settings.jsonX.tmp`, `settings.json-old.tmp.1`, `not-a-store.json.tmp`, AND `.machine-id` itself | ALL survive, byte-identical | survive | builder (T3) + drafter (`.machine-id`) |
| d11 | DATA_DIR itself unlistable (`chmod 111` on your own dir; restore after — H-5) | failure `(data directory)` named; record not "purged" | — | drafter — **no cell pins P-3 on the listing (§7 M-D4)** |
| d12 | a HARD-LINKED sibling (`ln`, nlink 2, the other name outside DATA_DIR) | **measure**: recorded purged while the bytes survive via the other name? (the code checks no `nlink`) | — | drafter — record; grade by reachability |
| d13 | a sibling created AFTER the one-time listing (L-D1, race) | survives, unrecorded — measure if cheaply reachable (e.g. a preload that writes one between the listing and the loop) | — | builder (declared) |
| d14 | a `.tmp` sibling of a recovery copy under `backups/` (L-D2) | survives (declared) — measure and name | — | builder (declared) |

**E — the undated row (RD-315). Seed through the product's own `SimpleDatabase` into `DB_PATH` BEFORE boot (H-2), boot on loopback, `GET
/api/database`, at `0863711` and `1524fca` (and the merged tree for e1-e3), same window.**

| row | stored row | expected `jobCompletedTime` at `1524fca` | at `0863711` | predicted-by |
|---|---|---|---|---|
| e1 | dated print (`Job_Completed_Time_UTC` set) | that value | same | builder (control) |
| e2 | undated print (completion NULL, `created_at` NULL) | `null` | **request time** | builder |
| e3 | undated scan (DigitalSend) | `null` | request time | builder |
| e4 | completion NULL, `created_at` set | `created_at` (a stored time, not a completion — **say whether that is itself a claim the row does not make**) | same | drafter |
| e5 | completion `''` (empty string) | falls through `||` → `created_at` or `null` | request time | drafter |
| e6 | **reachability:** can the ingestion path (not a hand seed) store a row with both NULL? Which writers set `created_at`? | READ + one ingestion if cheap | — | drafter (READY :10: "insertPrinterLog passes created_at explicitly, so it is stored NULL") |
| e7 | downstream of the transform: does the route (or a caller) sort, filter or date-range over `jobCompletedTime`, so `null` becomes epoch 1970 or drops the row? | READ; probe a sort/filter if the route takes one | — | drafter |
| e8 | the two frontend readers (READY :17: `static/js/index.js` 4903, 6290, 6317, 6376, 6424, 6434, 6584, 6794; `chart-details.js` 595, 939) | re-read at the MERGED tree; "—"/"Unknown" for null (no browser — NOT TESTED line) | — | builder (READ) |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.**

## 3. THE QUESTIONS ALL FIVE TARGETS ANSWER FIRST
0. **SESSION_SECRET UNSET, EVERY RUN** — see §3a H-1 for the ONE permitted printer. Positive control once per target: that target's own cell file
   with a throwaway random 64-hex secret exported (never printed, never written) — identical results, or say what differed.
1. **Re-pin everything yourself:** `git ls-remote` at start, mid and end (three timestamped readings, branch name beside each sha, all six refs);
   M0 = main at your start, and the "Main is moving" rule (§1) re-proved on M0; chains and exact parents (`git log --format='%H %P'`); deltas
   (`git diff --name-status`); counts at `7c47ec4`, `0863711`, `11666d3`, `12b5edc`, M0, `911e706`, `7be79f0`, `d81cd97`, `ed01f7e`, `95c3c9a`,
   `9fb9431`, `057016d`, `1524fca`.
2. **Re-derive every red and every mutant INDEPENDENTLY** — your own script, never the builders' `rd447-hold.sh`, `rd411-hold.sh`, `rd533-hold.sh`,
   `rd533-probe.sh`, `rd315-hold.sh` or `s84n/rd627a/hold.sh` (read them for method; run your own). **Before each mutant arm, prove the mutant still
   parses — `node --check` on every mutated JS file, exit 0, quoted — and assert its anchor matched exactly once and the mutation LANDED (the exact
   mutated text present; batch #2's `qa-mutate.py <arm> <mid> --verify` with its negative control). A red from a mutant that does not parse, or a
   green from a mutation that never landed, is a VOID arm.** Read WHY each red is red: quote the failing assertion.
3. **Name every behaviour guarded by no cell, and every one guarded only by source text (C-122).**
4. **Full verify of each head AND of the merged tree**, `npm run verify -- --maxWorkers=2` (RD-561), through the lock, on a git-indexed tree,
   SESSION_SECRET UNSET. **Predicted: `911e706` 4033/236 · `ed01f7e` 4040/238 · `95c3c9a` 3982/236 · `057016d` 4017/238 · `1524fca` 3990/237 ·
   merged (M0 + all five) counts(M0) + 96 / + 5 = 4117/243 at M0 = `12b5edc`** (arithmetic 4021 + 55 + 28 + 4 + 5 + 4 and 238 + 5 — a PREDICTION;
   C-68 says the measurement decides). Every failure by NAME. **"Re-run until green" is not an acceptance gate (charter §4d).**

## 3a. INSTRUMENT RULES — H-1..H-6 (rd579-rd639 report :337-343) and H-7..H-12 (batch #2 report :372-379 and §6.6)
- **H-1 (from rd579-rd639 S-1: a SET/UNSET idiom printed the secret's VALUE).** The ONLY permitted printer, verbatim:
  `if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi`.
  **FORBIDDEN anywhere in your scripts:** `${SESSION_SECRET-…}`, `${SESSION_SECRET:-…}`, `${SESSION_SECRET+$SESSION_SECRET}`, `echo
  $SESSION_SECRET`, `printenv`, `env | grep`, `set | grep`, and **echoing an env array that could hold it (`${envs[*]}`, batch #2 S-5a)**.
  **Self-test it BEFORE the first hold (a control that can fail):** run the printer once with a throwaway exported and once unset, capture both
  outputs, and assert the throwaway's value is ABSENT from both (compare in-process; never print it). **After every hold, scan that hold's logs
  for the throwaway value** (in-process comparison) and report the count (0); **the scan's own positive control plants a DIFFERENT random marker,
  never the throwaway** (batch #2 S-5b). The same discipline covers every needle and planted GUID: print a GUID only as `<first4>…<last4>`.
- **H-2 (from S-2: an instrument perturbed the measured volume).** Never construct a product storage object (`JsonStorage`, `SimpleDatabase` or any
  module whose constructor writes) on a DATA_DIR you are measuring AFTER its server booted or its erasure ran. Seed BEFORE boot; read ledgers,
  `settings.json`, `erasure-audit.jsonl`, backups and logs RAW.
- **H-3 (from S-3: a live-server hook never installed and the arm silently died).** Every hook you rely on (a preload, a signal handler, a mutated
  rule, a race-writer, the sweeper in LIVE mode — **S-3's own failure was the sweeper never starting because schedulers start only in one boot
  branch**) gets a **LANDING CONTROL** before the measured run: prove it fired once on a known input. An arm whose instrument failed is VOID, is
  re-run, and is reported as a self-correction — never reported as a result.
- **H-4 (from S-4: an edit silently disabled the heartbeat for three holds).** The heartbeat is a SEPARATE child process started by the hold wrapper
  (`while sleep 60; do echo "HB $(date -u +%FT%TZ) <step> <pid> <elapsed>"; done`), killed in the wrapper's `trap … EXIT`; **the wrapper ABORTS the
  hold if no HB line appears within 90 s of the grant**, and after every hold you compute and REPORT the max gap between HB lines (must be ≤ 120 s).
- **H-5 (from S-5: the instrument recorded its own chmod as an "outside change").** Restore your own perturbations (mode bits — d11, c4 — links,
  planted files, held ports) before any before/after hash, and hash the restore.
- **H-6 (from S-6: an extractor matched the wrong anchor; the report's quoting bug on a path with spaces).** Every extractor (function, hunk, census
  grep, date-fallback classifier) gets a POSITIVE CONTROL: extract a known unit and compare with an independently counted expectation (e.g. the
  date-fallback census finds RD-315's two lines at `0863711`). **Every path is quoted** — `!CODING` and `Testing Agent MAIN` contain `!` and spaces.
  **Every server you boot runs under batch #2's network belt (`qa-netbelt.sb`) with its landing control (EPERM for TEST-NET-1, 200 for loopback).**
- **H-7 (from batch #2 S-1: unquoted path word-split, ten VOID arms).** Mutants are built and verified ONLY by a quoted tool with a negative control
  (an unmutated tree → VOID rc ≠ 0). A mutant check that prints an empty count is a VOID arm, never a pass.
- **H-8 (from batch #2 S-2: an insertion's new text contains its anchor).** The landing rule is "the exact mutated text is present AND the
  original text is absent once the new text is removed" — never "the anchor is absent".
- **H-9 (from batch #2 S-3: a harness wrote a literal backslash-n through `JSON.stringify`).** **Byte-level plants (every §2a-A+B row) are written with
  `Buffer` and verified by `xxd -l 16` BEFORE use; a plant whose first bytes are not the intended BOM / NUL stride is VOID.** Never build a wide
  plant with `echo`, `printf`, a heredoc or `JSON.stringify`.
- **H-10 (from batch #2 S-4: Playwright's default argument disabled the thing under test).** Every instrument default that could suppress the
  phenomenon gets a landing control of the PHENOMENON itself: for c1, prove A really holds the port (`lsof`) before B starts; for d9, prove the
  sweeper really re-drove (its ledger `purgedBy`); for a4-a10, prove the plant reaches `scannableText` as bytes (not a UTF-8 string) on the bytes rows
  and as a string on a9/a10.
- **H-11 (from batch #2 S-6: zsh slips — `$s:scripts` eaten as a history modifier, `set -- $p` not word-split).** Every script runs under
  `/bin/bash` explicitly (`#!/bin/bash`, `bash <file>`), and every `<sha>:<path>` is written `"${sha}:${path}"`.
- **H-12 (from batch #2 §6.6: the "missing 0" prediction was wrong because a renamed cell was not accounted).** Before the C-57 control, list every
  `__tests__` file any of the five heads MODIFIES or DELETES (`git diff --name-status <base> <head> -- __tests__`); predicted: only
  `helpers/image-manifest.js` (M, no ids). If a test id is missing, apply C-133 and its rename ADDENDUM (:1434) verbatim, and say which clause.

## 4. TARGET A — RD-447 (TIER 1). Answer each with a measurement.
1. **Scope (READ ONLY, quoted):** `git diff --name-status 7c47ec4 911e706` = the three files; the helper hunks quoted; `readTracked`'s
   one-line change quoted.
2. **RED-PROOF, POSITIVE CONTROL FIRST.** In ONE hold: `rd447-utf16-text-is-decoded.test.js` against `7c47ec4`'s helper — predicted **40 red / 15
   green (RELAYED; the separate `rd447-red-7c47ec4.log` says 40/9/49 — resolve which)** — then at `911e706`, predicted 55/55. Name the 15 base-greens
   and say which are CONTROLS in C-40's sense (can fail).
3. **Mutants (M-A1, M-A2 re-derive the builder's; the rest are new; predictions are the drafter's):** **M-A1** the string rule removed (`WIDE_RUN`
   replace dropped) → predicted exactly 6 red (RELAYED); **M-A2** `readTracked` back to `'utf8'` → exactly 1 red (RELAYED) — **only ONE cell guards
   the reader that the whole fix depends on: say which, and whether it would catch a caller that bypasses `readTracked`**; **M-A3** BOM order
   swapped (UTF-16LE before UTF-32LE) → a UTF-32LE+BOM cell red?; **M-A4** `sniffWide` always `null` → the BOM-less cells red; **M-A5** the UTF-32
   branch of `sniffWide` removed → which?; **M-A6** the binary-extension check moved AFTER decoding → which?; **M-A7** `unwiden` without the end
   spaces (a run glued onto its neighbour) → which?; **M-A8** `decodeText` strips a UTF-8 BOM (behaviour change for UTF-8) → the "changes nothing for
   the tree as it is" cell red? Any arm predicted red that stays green is a **gap in the cells** — name the behaviour it leaves unguarded.
4. **Every row a1-a19 of §2a at `911e706`** (and the merged column in §9).
5. **Who reads text WITHOUT `readTracked`:** census every `scannableText(` caller and every `readFileSync(…, 'utf8')` in the seven helper consumers
   (drafter, `git grep -l -F helpers/image-manifest 12b5edc -- __tests__` → `image-content-exposure`, `rd385-shipped-root-markdown-identifiers`,
   `rd403-first-run-no-publisher-identifiers`, `rd429-nul-byte-does-not-hide-a-file`, `rd442-licence-terms-of-service`,
   `rd503-r2-doc-claims-against-product`, `rd503-shipped-docs-c51-leftovers`; the last has its OWN `readTracked` with `'utf8'` at :45, READ at
   `12b5edc`). **For each, say whether a wide file reaches it as bytes or as a string, and whether its gate would find row a4.**
6. **The real tree:** list every tracked file at `911e706` (and the merged tree) that `decodeText` decodes as UTF-16/32 (BOM or sniff). Drafter:
   **0 tracked blobs at `12b5edc` start with a UTF-16 BOM (`ff fe`/`fe ff`)** — UNCONTROLLED (no positive control was run; the census must plant one).
7. **C-68 re-run set for A and B (one set, named, per-file counts, one hold):** the seven consumers above + `rd447` + `rd411` = **9 suites**
   (re-run the grep; add any file it finds that the drafter missed).
8. **PRIOR WORK (C-49):** the RD-429 gate's F1 (PRIOR ROUND) — does RD-447 close exactly it; did any earlier WIP attempt the decode?

## 5. TARGET B — RD-411 (TIER 1). Answer each with a measurement.
1. **Scope:** `git diff --name-status 11666d3 ed01f7e` = the three files; `d81cd97`'s parents; `11666d3..d81cd97` = RD-411's two files only;
   `d81cd97..ed01f7e` = counts only.
2. **RED-PROOF, POSITIVE CONTROL FIRST:** the cell file against `7c47ec4`'s (and `11666d3`'s — identical helper blob `3ca9abc`) helper — predicted 24 red
   / 4 green — then 28/28 at `ed01f7e`. **Which 4 are green at base, and are they the "CONTROLS (green at base)" of READY :16?** (The READY lists more
   than 4 controls: count them.)
3. **Mutants:** **M-B1** `labelForm` = identity → 13 red; **M-B2** joined alternative removed → 1 red (`tenantid=`); **M-B3** `signalLines` keeps the
   prose-only `LABEL.test` → 11 red (all three RELAYED); new: **M-B4** the acronym rule dropped (`AADTenantId`) → which?; **M-B5** the window
   `{0,24}` → `{0,40}` (RD-386's question is Kam's — **does ANY cell pin the window as unchanged?** predicted: none — a gap to name); **M-B6** GUID
   matched on `labelForm(line)` instead of the original line → "GUID read from the original line" red?; **M-B7** `hasLabel` used in
   `identifierSignals` only (not `signalLines`) → the reopen cells red?
4. **Near-miss census:** run `hasLabel` over every line of every shipped file at `ed01f7e` and at the merged tree; list every line that is TRUE now
   and was FALSE under the old `LABEL` (with or without a GUID). The READY says 0 newly flagged CARRIERS; this asks for newly labelled LINES.
5. **`labelForm` edge shapes:** `TENANTID`, `Tenant-ID`, `tenant.id`, `tenant id` (two spaces), `x-ms-client-request-id`, `subscriptionIds`,
   `principalObjectId`, `resourceGroupName` — the result and whether it matches READY :9-12's description.
6. **PRIOR WORK (C-49):** S59's WIP `c026e94` — confirm its bracket-rule half (RD-418's) is NOT carried and nothing was removed (READY :26).

## 6. TARGET C — RD-533 (TIER 2). Answer each with a measurement.
1. **Scope:** `git diff --name-status 7c47ec4 95c3c9a` = the three files; the one server hunk quoted; nothing else in the callback changed
   (diff the success path byte-for-byte).
2. **RED-PROOF, POSITIVE CONTROL FIRST:** the cell file at `7c47ec4` — 3 red, the A-control green — then 4/4 at `95c3c9a`. **H-10: prove A holds the
   port before B starts.**
3. **Mutants:** **M-C1** `if (false)` → all three B cells red; **M-C2** `exit(0)` → only non-zero red (both RELAYED); new: **M-C3** the `return` after
   scheduling exit removed (B logs "running" then exits 1) → "never claims running" red?; **M-C4** the delay `250` → `0` → does "names the failure"
   redden over a pipe (tests L-C4)?; **M-C5** the two remedy strings swapped → predicted: no cell guards the remedy text — say so; **M-C6** the exit
   moved to `process.exitCode = 1` without exiting → "exits on its own" red?
4. **Every row c1-c9 of §2a.** c4 discharges L-C3 if it runs; c5/c6 are pre-existing paths — label them.
5. **The harness consumers (L-C5):** `helpers/test-server.js` is imported by **54** test files at `12b5edc` (drafter, `git grep -l -F
   helpers/test-server`); the C-68 set for C is the **11 files naming `EADDRINUSE` or `running on port`** (drafter, `git grep -l -i -E
   'EADDRINUSE|running on port' 12b5edc -- __tests__`: `ai-config-aoai-save`, `boot-probe-log-redaction`, `data-source-save-log-redaction`,
   `discover-tables-tenant-mask`, `helpers/test-server.js`, `rd395-ai-enabled-gate`, `rd490-open-access-banner-browser`, `rd510-listen-before-warmup`,
   `rd571-reserved-port-is-bindable`, `rd641-reserved-port-binds-on-every-address`, `setup-rate-limit-allowance` → **10 suites** + rd533). Read how
   `bootServer` treats an early exit, and whether any consumer relied on a silent second server.
6. **The Express residue (READ + census, not graded on RD-533):** after a successful listen, is the `once('error', done)` listener still attached
   (`server.listenerCount('error')` if the server object is reachable from a preload — H-3 landing control), and what happens to a later server
   `'error'`? Label pre-existing.
7. **The floor counter:** CLARIFICATIONS :1108 says an RD-533-shaped foreign server "never listens". Does the fix change what `qa-floorcount.py`
   (C-125) can see? One sentence, READ ONLY.

## 7. TARGET D — RD-627a (TIER 1). Answer each with a measurement.
1. **Scope:** `git diff --name-status 11666d3 057016d` = the four files; `057016d`'s parents; `9fb9431`'s delta over `7c47ec4` (4 files); the
   updated READY's "merged file vs main = exactly RD-627a's +69/−1, and vs 9fb9431 = exactly RD-639's +32/−1" (:5) re-measured.
2. **RED-PROOF, POSITIVE CONTROL FIRST:** the cell file against `11666d3`'s product code (the builder did this in a detached worktree in NexusAI — **you do
   it in YOUR tree**): T1, T2, T4 red; POPULATION and T3 green — then 5/5 at `057016d`. Quote T4's failing assertion at base.
3. **Mutants (all new — the READY lists none):** **M-D1** the sibling sweep call removed → T1, T2, T4 red; **M-D2** `isInterruptedWriteOf` narrowed to
   `startsWith(store+'.tmp.')` only (jsonStorage's form) → ONLY T2 red (the bare `.tmp`); **M-D3** widened to `name.startsWith(store) &&
   name.includes('.tmp')` → T3 red (`settings.jsonX.tmp`, `settings.json-old.tmp.1`); **M-D4** the listing's `catch` swallows every error → predicted:
   **no cell guards the unlistable-dir failure — a gap to name**; **M-D5** the sweep moved AFTER P-3's `continue` → T1 red (the absent-store case);
   **M-D6** `_removeInterruptedWrite` unlinks `realpathSync(full)` (follows the link) → T4 red (target destroyed); **M-D7** the directory branch
   removed (a dir sibling → `unlinkSync` → EISDIR/EPERM) → which?
4. **Every row d1-d14 of §2a** at `11666d3` and `057016d`. d4 and d8 are the TIER-1 core.
5. **The RD-639 live-store symlink rule on the merged tree (C-68):** `rd639-erasure-live-store-symlink.test.js` by name (26 cells RELAYED) and d8; one
   RD-639 mutant (the rd579-rd639 report's M-B1 — "every L1, L2, L3 red", its §4 item 7) on the merged tree.
6. **C-68 re-run set for D (named, per-file counts, one hold):** the **17 files** naming `dataErasure` or `customerDataFiles` at `12b5edc` (drafter,
   `git grep -l -E 'dataErasure|customerDataFiles'`; 2 are helpers — `helpers/purge-and-die.js`, `helpers/rd525-purge-on-signal-preload.js` → **15
   suites**) + `rd627a`.
7. **PRIOR WORK (C-49):** `jsonStorage`'s `collectPriorStateEvidence` and `_existenceEvidence` scan the `.tmp.` prefix (first READY :16) — confirm they are
   unchanged and say whether they now disagree with `isInterruptedWriteOf` in a way that matters (boot evidence vs erasure).

## 8. TARGET E — RD-315 (TIER 1). Answer each with a measurement.
1. **Scope:** `git diff --name-status 0863711 1524fca` = the three files; both server lines quoted; `0863711..12b5edc` touches the server entry point 0
   times.
2. **RED-PROOF, POSITIVE CONTROL FIRST:** the cell file at `0863711` — print and scan red (quote the returned timestamps: they must equal the request
   time, within the request window), control and findability green — then 4/4 at `1524fca`.
3. **Mutants:** **M-E1** old fallback at :14242 → ONLY print red; **M-E2** at :14294 → ONLY scan red (both RELAYED); new: **M-E3** fallback
   `new Date(0).toISOString()` → red?; **M-E4** fallback `''` → red? (does the cell assert `null` or merely "not now"?); **M-E5** `jobStartTime`'s
   fallback changed to now (outside the diff) → predicted: no cell guards it — name the gap.
4. **Every row e1-e8 of §2a.**
5. **THE CENSUS (census only, not a fix; the commission's ask):** every `new Date()`, `Date.now()` and `new Date().toISOString()` site in the server
   entry point on the merged tree, classified: (a) stamps an event happening NOW (legitimate: a log time, a created-at at insert), (b) a FALLBACK
   standing in for a missing stored time (RD-315's class), (c) a default window bound ("today"), (d) other. **Start from the drafter's candidates
   (§1 Target E: :19480, :19789, :19926, :20031, :10036, :10037, :10046) and prove the census complete with H-6's control** (it must find RD-315's two
   lines at `0863711`). For each (b): the route or function, what a caller sees, and whether a cell covers it. Each (b) is a recommendation for a
   new ticket, labelled READ ONLY or PROBED — **not a finding against RD-315** unless it sits in the two `/api/database` transforms.
6. **C-68 re-run set for E:** **no other test file names `/api/database` at `12b5edc`** (drafter, `git grep -l -F '/api/database'` → 0; positive control
   at `1524fca` → 1, the rd315 file) — so the set is rd315 plus the RD-533/RD-579 server-entry-point cells on the merged tree (§9 Q6). Re-run the grep.

## 9. THE MERGED TREE (C-68, C-57, C-89, C-104, C-112, C-133). No verdict is complete without it.
1. **Build it in YOUR OWN scratch clone** under `projects/nexusai/qa-trees/batch1.*/clone-1`: `git clone --shared --no-checkout <repo> <dir>`; in the
   clone only: remove `origin`, set a local `user.name`/`user.email` and `gc.auto 0`; `git checkout -b gate <M0>`; then `git merge --no-ff` in the
   builders' requested order: **`911e706`** (RD-447 first, READY-411 :24), **`ed01f7e`**, **`95c3c9a`**, **`057016d`**, **`1524fca`**. **Predicted: a
   conflict, if any, ONLY in `scripts/verify-expected-counts.json`; `helpers/image-manifest.js` and the server entry point AUTO-MERGE** (drafter's
   emulation, §1); **predict before each merge whether the counts file conflicts** (it depends on which side you took at the previous one — the
   rd579-rd639 report :262 and batch #2 :296-298 measured exactly this) **and explain any clean merge with a side control.** Anything else
   conflicting **STOPS** (C-57). **C-104: resolve and stage before any census or run.**
2. **Resolve the counts file by REGENERATION, never by hand:** take a side to complete each merge commit, then `npm run verify -- --maxWorkers=2
   --update-counts` ONCE on the tree after ALL FIVE merges, through the lock, SESSION_SECRET UNSET, and commit the regenerated file in the clone.
   **Predicted counts(M0) + 96/+5 (4117/243 at M0 = `12b5edc`) — a prediction; the measurement decides.** Then a plain verify of the committed head;
   suites ≥ the largest parent's (C-57 step 4).
3. **Order independence (a control that can fail):** a second clone in reverse order (`1524fca`, `057016d`, `95c3c9a`, `ed01f7e`, `911e706`); **the two
   results' `HEAD^{tree}` must be identical apart from the counts file** — quote both tree ids and the `git diff --name-only`. **This matters more than
   in batch #2: two files are CONTENT-merged, and a textual merge can depend on order.**
4. **Blob identities on the merged tree (drafter's emulation at M0 = `12b5edc`):** `helpers/image-manifest.js` = **`07e8711`** (neither parent),
   `backend/server.js` = **`bc099b2`** (no parent), `backend/dataErasure.js` = `09e34f6` and `backend/customerDataFiles.js` = `708c38b` (`057016d`'s),
   `helpers/css-colors.js` = `78bb004`, `docs/BRAND.md` = `5fa08fa`, `package-lock.json` = `9064763`. **C-112's condition — state it beside the
   conclusion: at M0 = `12b5edc`, 285 `__tests__` files, predicted 284 byte-identical to one parent and ONE identical to NONE
   (`helpers/image-manifest.js`, a textual auto-merge, no test ids).** So the id-superset shortcut does NOT rest on "nothing content-merged" here:
   the composed helper is proven by BEHAVIOUR (Q6), never by the superset alone. 0 files absent.
5. **id-superset control (C-57):** merged test ids ⊇ ids(M0) ∪ ids(`911e706`) ∪ ids(`ed01f7e`) ∪ ids(`95c3c9a`) ∪ ids(`057016d`) ∪ ids(`1524fca`);
   **missing 0 predicted (H-12: no branch modifies or deletes a test file)**. Use batch #2's adapted COPY `qa-c57-id-superset.sh` (reads the jest JSON
   of YOUR own full verifies, keeps the lock-holder refusal, proven first to STOP on a planted missing id), extended to six parents. **Note:
   `911e706` and `95c3c9a` are off `7c47ec4`, `1524fca` off `0863711`, `ed01f7e`/`057016d` off `11666d3`** — ids of later main commits are absent
   from those parents by construction, not by loss. If it misses, apply C-133 and its ADDENDUM verbatim and list every accounted id.
6. **The semantic overlaps git cannot see (C-68), on the merged tree, one hold:**
   - **A×B, the composed helper:** the rd447 and rd411 files (55 + 28), the seven consumers, and **the merged column of rows a1-a19** — especially
     **a4-a10 (only the composition finds them) and a19 (the real shipped tree: `unreviewedCarriers()` = [] with the detector-live control;
     `__tests__/fixtures/image-carrier-review.json` unchanged)**. Neither builder has run a wide plant through the machine-shaped label.
   - **C×E×RD-579, the server entry point:** the rd533, rd315 and rd579 files (`rd579-ai-config-clear-truthful.test.js`, main's) by name, c1 and
     e2/e3 on a merged-tree server; the RD-533 C-68 set (10 suites).
   - **D×RD-639:** rd627a, rd639 and the D C-68 set (15 suites); d1, d7, d8 on the merged tree.
   - then the full verify (Q2).
   Then ONE mutant per ticket on the merged tree (M-A2, M-B1, M-C1, M-D1, M-E1): **each table must still hold through the other four changes**,
   plus **M-AB: `readTracked` back to `'utf8'` AND `labelForm` identity together → a4 must go to 0** (the composition's own mutant).
7. **C-89 on your clone:** `git diff --quiet HEAD` holds and `git show HEAD:scripts/verify-expected-counts.json` equals the regenerated counts.
8. **Nothing leaves your clone.** No push, no remote, no ref written in the NexusAI repo. **Count `<repo>/.git/objects` files before and after your
   whole session and account for any delta by mtime** (four live seats commit into that repo, and P is merging tonight; batch #2's method, its
   report :36, incl. git freshening mtimes of pre-existing objects). Drafter's reading: `git count-objects -v` `count: 1120` at 09:2x AEST.

## 10. CI (C-142) — NOT RUN AT ANY BRANCH HEAD unless a PR exists
- **Unverified by the drafter:** whether any of the five branches has a PR (no `gh` was run; the RD-533 READY :23 says "no PR"). Check with `gh pr
  list --head <branch> --state all` (READ ONLY, NexusAI's own `GH_CONFIG_DIR`); M0's CI Build — `gh run list --commit <M0>` READ ONLY, labelled.
  **`gh` never merges, approves, comments, reviews, labels, re-runs, dispatches or opens a PR.**

## 11. Floor discipline — THE FOUR CLAUSES, plus THE DEADLINE RULE
1. **Every jest run, every server you boot and every erasure drive goes through `session-tools/nexusai-lock.sh`, tagged `qa-b1-…`** (e.g.
   `qa-b1-H1-AB-arms`, `qa-b1-H2-C-servers`, `qa-b1-H3-D-erasure`, `qa-b1-H4-E-route`, `qa-b1-H5-heads-verify`, `qa-b1-H6-merged`) — C-141: gate-class,
   and under ADDENDUM 2/3 every NEW `qa-*` ticket earns a fresh, self-applied yield. **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit
   another seat's process, lock directory, owner file or ticket, even if it looks stuck; if a holder looks stuck, mail a QUESTION (§13) and keep
   waiting. Pure-node rows with no server and no jest (the §2a-A+B helper calls, the date census, the merges themselves) may run outside the lock —
   say which did.
2. **Hold the lock ONCE per multi-run measurement.** Every hold is a TRACKED CHILD of your seat, never detached (`nohup … &`).
3. **Count foreign servers the RD-606 / C-125 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND the server entry point
   anywhere in the remaining argv; "ours" = the ancestor chain CONTAINS your own claude pid. **Your OWN RD-533 rows boot deliberately failing second
   servers — they are "ours" and must be reaped; count them, and prove each B exited (or was killed in a `finally`).** **NEGATIVE controls, all in
   the same run, all must classify FOREIGN — read at drafting 2026-09-26 09:09:53 AEST from `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}
   #{pane_pid}'` + `ps`:** NexusAI-M claude **`88756`** (pane `%11`), NexusAI-N claude **`10246`** (pane `%12`), NexusAI-O claude **`10643`** (pane
   `%13`), NexusAI-P claude **`11987`** (pane `%14`), and Tuesday's claude **`91386`** (pane `%0`, parent bash `89558`). Re-read them at start; if one
   has exited, say so and use the others; **a hold with NO live negative control aborts.** Reuse batch #2's corrected instrument BY COPY with YOUR
   pid as `ROOT` and these as `NEG`:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/evidence/qa-floorlib.sh`
   (its `ROOT` default names that gate's pid 41035 — **correct it to yours before any hold**; its `NEG` default already names these five), `…/qa-floorcount.py`
   and `…/qa-dispatch.sh`. The original is gate 7's
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`.
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, "no needle survives" (d1-d14), "no shipped file
   newly flagged" (a19), "no other fabrication site" (§8 Q5), and "no cell reddens" under any mutant.

**5. THE DEADLINE RULE — every real-server probe has a per-step DEADLINE, a HEARTBEAT, and kills its server in a `finally`.** Every HTTP request
carries a client timeout; each step (boot 60 s, request 30 s, B's expected exit 10 s, erasure drive 120 s, sweeper re-drive 180 s, exit 20 s) has a
written DEADLINE; a step past it is ABORTED and reported, never waited on. **Log a HEARTBEAT line at least every 2 minutes during any hold (H-4: a
separate child, ≤ 120 s max gap, aborted if absent at 90 s); a step with no heartbeat for 5 minutes is aborted and reported,** and a hold that is not
progressing releases the lock. Every server you start (A and every B) is killed in a `finally` (SIGTERM, then SIGKILL after a grace), every port you
hold (c7, c8) is released, and the reap is confirmed by your floor counter.

## 12. HELD
- **LOCAL RUN, NOT THE DEMO:** every request goes to a server YOU booted on 127.0.0.1 from YOUR tree, under the network belt (H-6). No request to any
  live, demo or public host; no Azure, no Entra, no Log Analytics (L-E1 stays NOT TESTED). This is authorised defensive QA of Datasec's own product on
  loopback.
- No merge (outside your own clone), no push, no deploy, no registry, no Partner Center, no production, no money, no external comms, no mail to any
  human. **No `az` at all.** `gh` READ-ONLY and optional (§10). No docker is needed by this gate.
- **Symlinks, hard links, chmod, held ports and scratch git repos live ONLY under your own mktemp dirs.** Never link to, chmod or plant anything in a
  real home directory, the NexusAI tree, or any other seat's directory. Planted GUIDs and needles are random and throwaway.
- **Findings-only:** do not commit (outside your clone), move any branch, file a ticket, or write anything inside the NexusAI project (`2_Project_Files`,
  `session-tools/`, `worktrees/`, `1_Project_Definition/`, `qa-reports/`). **NEVER `rm`** — quarantine, per the template §5.

## 13. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch1/report.md` — ONE report covering all
five tickets; evidence in `./evidence/` beside it.

**Questions:** your routing name is **`QA/NexusAI-batch1`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by) and **PROCEED ON THE SAFEST READING without
waiting**; Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning `[Tuesday -> QA/NexusAI-batch1] ANSWER`. Approval-class
items are NOT RUN and named. Record every question, reading and answer.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-447: <GO|GO WITH FINDINGS|NO GO> @ 911e706 · RD-411: <GO|GO WITH FINDINGS|NO GO> @ ed01f7e · RD-533: <GO|GO WITH FINDINGS|NO GO> @ 95c3c9a · RD-627a: <GO|GO WITH FINDINGS|NO GO> @ 057016d · RD-315: <GO|GO WITH FINDINGS|NO GO> @ 1524fca`
Lead the body with one sentence per ticket, then one line naming M0. Never `wednesday-agent@`. AgentMail key: `AGENTMAIL_API_KEY` in
`/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute: the QA project has none). Never put the key, a planted GUID, a needle or any
secret in a mail or the report.

Verdict format:
- **RD-447: GO / GO WITH FINDINGS / NO GO** naming `911e706859cbbe49ef32d4166ab9b3271bf98d08`: the red-proof (the 40/15 vs 40/9/49 discrepancy resolved);
  M-A1..M-A8; rows a1-a19; the non-`readTracked` readers; the real tree's wide files; the C-68 set.
- **RD-411: GO / GO WITH FINDINGS / NO GO** naming `ed01f7eb02430de74ccaaa6d6f265c7638e5aab4`: the red-proof; M-B1..M-B7; the newly-labelled-lines census;
  the edge shapes; prior work.
- **RD-533: GO / GO WITH FINDINGS / NO GO** naming `95c3c9a9d39429f9093270e283e531f3cda4e88d`: the red-proof with H-10's port control; M-C1..M-C6; rows
  c1-c9 (c4 = the EACCES case); the harness consumers; the Express residue (pre-existing).
- **RD-627a: GO / GO WITH FINDINGS / NO GO** naming `057016de2b2929c23f643b7346413199f370d3ce`: the red-proof at `11666d3` in your own tree; M-D1..M-D7;
  rows d1-d14 on a real DATA_DIR (d4, d8, d9 first); the RD-639 rule on the merged tree; the C-68 set.
- **RD-315: GO / GO WITH FINDINGS / NO GO** naming `1524fca7ec72b23a4f000b77872a4158f8e14f86`: the red-proof; M-E1..M-E5; rows e1-e8; **the census table**.
- **The merged tree (§9):** M0 named; both orders, conflicts quoted, counts regenerated once (measured vs counts(M0) + 96/+5), id-superset with C-112's
  condition beside it (the one content-merged helper named), the composition rows and one mutant per ticket plus M-AB, C-89, the object-count accounting.
- Each of **L-A1..L-A3, L-B1..L-B4, L-C1..L-C5, L-D1..L-D4 and L-E1..L-E3** answered: discharged with a measurement, or left standing and named (C-112).
- Report all six refs as **three timestamped readings (start / mid / end)**, each with its branch name.
- **§3a H-1..H-12:** state for each that it was followed, with the self-test outputs (H-1), landing controls (H-3, H-10), max HB gap per hold (H-4) and
  the byte checks of the plants (H-9).
- Every action recommendation carries its evidence class: **MEASURED AT RUNTIME / PROBED / READ ONLY**. Severity is yours; priority is Tuesday's.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, Azure Container Apps, the Log Analytics path of /api/database, a real browser render of an undated row, text encodings other than UTF-8, UTF-16 and UTF-32, and Windows.

## WRONG OR UNVERIFIED IN THE COMMISSION AND THE READYS — carried so the gate inherits the corrections
1. **"NexusAI main is MOVING tonight (P is merging RD-200 -> 12b5edc, then RD-444 and RD-428)"** — at 09:06:26 AEST main ALREADY = `12b5edc`, and it got
   there by FAST-FORWARD (`refs/heads/main` = `refs/heads/rd-200-js-colour-corpus-s84p` = `12b5edc`; no RD-200 merge commit exists). RD-444/RD-428
   had not landed (their branches still at `2f9da1c`/`823ef9e`, not ancestors of main).
2. **RD-447's READY is not on disk** (`briefs/` has no rd447 file). Its facts are RELAYED by the commission; four of five check against the builder's logs
   (§1 Target A); **`rd447-red-7c47ec4.log:997` contradicts "red 40/15" with "40 failed, 9 passed, 49 total"** — unresolved at drafting.
3. **"RD-447 … off main 7c47ec4"** — `7c47ec4` WAS main when the branch was cut; main is now four merges and three RD-200 commits past it
   (`merge-base(911e706, 12b5edc) = 7c47ec4`). Same for RD-533. Not wrong, but "main" is stale.
4. **"RD-627a @ 057016d (… = 9fb9431 + main 11666d3 merged forward, auto-merge)"** — true, and **`057016d` is NOT a counts-only tip**: the counts were
   regenerated inside the merge commit (`git diff --name-only 9fb9431 057016d` = 5 files incl. the counts). RD-447, RD-533 and RD-315 have NO
   counts-only tip either (change + counts in one commit); only RD-411 (`d81cd97..ed01f7e`) does.
5. **RD-627a's first READY :2 "whichever lands second takes a real content merge in dataErasure.js"** — SUPERSEDED by its updated READY :4 ("there was NO
   hand resolution") and by the drafter's merge-tree (the merged `dataErasure.js` = `057016d`'s blob).
6. **The commission's "both RD-533 and RD-315 edit backend/server.js in different regions"** — true (`:22561-22582` vs `:14242`/`:14294`), and **RD-579 on
   main ALSO edits it** (`7c47ec4..0863711`, +52/−7). RD-533 is off `7c47ec4`, so the merged server entry point is a THREE-way composition (RD-579 +
   RD-533 + RD-315); merge-tree auto-merges it to `bc099b2` (= no parent), which parses (`node --check` rc 0).
7. **RD-533's listen callback "~:22564"** — correct at `95c3c9a` (the `app.listen` line); on the merged tree it is **:22609** (RD-579 adds 45 net lines
   above it).
8. **RD-533 READY's EACCES limit (L-C3)** — a low port is probably NOT an EACCES recipe on macOS (drafter's CLAIM, UNVERIFIED, §2a c5); a PORT that is a
   socket path in an unwritable dir is (READ: `PORT` is a raw string, merged :747). Measure both.
9. **RD-315 READY :22's "other 23 sites"** — matches the drafter's count of lines containing `new Date().toISOString(),` (25 at `0863711`, 23 after RD-315),
   but that spelling is NOT the class: 0 `||`/`??` fallbacks remain, while ternary and `Date.now()` fallbacks do (§1 Target E). The census must use the
   CLASS, not the spelling.
10. **RD-411 READY :14's "newly flags NO shipped file"** was measured at `7c47ec4` with UTF-8 reads; on the merged tree the reader decodes wide text, so the
   claim must be re-measured there (a19).
11. **Ruling timestamps (13:15Z ANSWER, 15:56:53Z ANSWER, 19:19:22Z ruling), "RD-684", "RD-386 is Kam's", Jira states "-> Testing"** — RELAYED from the
   READYs and commit messages; not read in Tuesday's mail or Jira by the drafter.
12. **CI and PR state on all five heads: UNVERIFIED** (no `gh` run at drafting).
13. **The Express `once('error', done)` residue (§1 Target C)** — READ in the NexusAI working checkout's `node_modules` (a single named file, not a tree
    search); the gate re-reads it in its own tree.

## PROVENANCE (drafter, 2026-09-26 09:05–09:40 AEST, read-only)
- origin heads (six branches + main + RD-200/428/444) | `git ls-remote origin <refs>` | 09:06:26
- chains, parents, merge-bases with `12b5edc`, main's line `7c47ec4..12b5edc` | `git log --format='%H %P %ad %s'`, `git merge-base` | 09:07
- counts at twelve shas | `git show "${S}:scripts/verify-expected-counts.json"` (bash; a zsh `$S:s` slip in the first attempt, re-read) | 09:08
- deltas, name-status, stats, pairwise overlaps, `server.js`/`dataErasure.js` shortstats per segment | `git diff --name-status|--stat|--shortstat`,
  `comm -12` | 09:08–09:10
- merge prediction and merged blobs | `git merge-tree --write-tree --name-only` with `GIT_OBJECT_DIRECTORY` in the drafter's scratchpad, NexusAI objects as
  alternate; `git count-objects -v` 1120 before/after; `node --check` on the two content-merged files | 09:10–09:12
- package-lock / package.json / verify-suite blobs at seven shas | `git rev-parse` | 09:09
- RD-447 and RD-411 helper diffs; RD-533 and RD-315 server diffs; RD-627a product diff; store list | `git diff`, `git show` | 09:12–09:16
- merged-tree line numbers (:747, :14242, :14294, :22604-22624) and the date-fallback census (with the `0863711` control) | `grep -n -i -E` over
  `git show` output | 09:15–09:18
- Express listen source | `sed -n 585,610p node_modules/express/lib/application.js`, `package.json:4` 5.2.1 | 09:19
- cell names, consumers (7), `test-server` readers (54), EADDRINUSE set (11), erasure set (17), `/api/database` readers (0; control 1), BOM census (0,
  uncontrolled) | `git grep -n|-l`, `git ls-tree -r` + `cat-file` | 09:13–09:22
- CLARIFICATIONS ids (C-02 :30, C-57 :410, C-68 :657, C-89 :827, C-104 :972, C-112 :1141, C-133 :1426 + ADDENDUM :1434, C-141 :1480 + ADDENDUM :1488 +
  2 :1490 + 3 :1492, C-142 :1494, C-163 :1657, C-164 :1667, C-165 :1678, C-166 :1689 (highest); 280,969 bytes, mtime 08:18:55; ticket grep 2 lines) |
  `grep -n` | 09:20
- builder evidence present in `session-tools/s84o/` (rd447-{hold.sh,hold.log,red-7c47ec4.log,verify.log}, rd411-{hold.sh,hold.log,verify.log},
  mt-objects, yield-log.txt), `s84m/` (rd533-{hold.sh,hold.log,probe.sh,probe-7c47ec4.log,red-at-7c47ec4.log}, rd315-{hold.sh,hold.log,red-at-0863711.log}),
  `s84n/rd627a/` (A-base.log, B-fixed.log, C-verify.log, hold.sh, `mf/` A-newmain, B-merged, C1-update, C2-plain) | `ls`, `grep -n` | 09:21
- batch #2 and rd579-rd639 reports: verdicts, merged tree, self-corrections, floor tables | `sed -n`, `grep -n` | 09:22–09:25
- negative-control seats %11 → 88756 (M), %12 → 10246 (N), %13 → 10643 (O), %14 → 11987 (P), %0 → 91386 (Tuesday; parent 89558) | `tmux list-panes -a
  -F …`, `pgrep -P`, `ps` | 09:09:53
- routing: `QA/NexusAI-batch1|tuesday-agent@agentmail.to|no` appended to `fleet/inbox_routing.conf` by the drafter | `tail` | 09:3x
