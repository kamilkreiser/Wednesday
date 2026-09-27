# QA Agent Invocation Brief — Datasec/NexusAI, ONE batched gate "batch 5b" (lane 1): the C-170 PACKAGE INTO MAIN (RD-460, TIER 1) + RD-696 (TIER 2, tests only) + RD-594 (TIER 2, guard cells only) — three verdicts, one report

**Drafted for Tuesday 2026-09-27 09:25–10:05 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.** (RD-594 was a placeholder
until Tuesday's mid-draft message at ~09:40 AEST made it a full member.)
Commissioned on Tuesday's batch 5b commission (2026-09-27, heads read by Tuesday at origin 09:3x AEST) and four READY mails on disk, each read WHOLE
(all three members are NexusAI lane 1: A and B by **NexusAI-M (S84M)**, C by **NexusAI-M (S86M)**; the live lane-1 seat that merges after the verdict is
**NexusAI-M (S86M)**):
- **A — C-170 / RD-460, the package into main** @ `be0fe3704023d8f092da0be27f79b82fbc029085` (branch `rd-460-pkg-into-main-s84m`) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-c170-package-READY-mail.txt`
- **B — RD-696** @ `2c221fa2ed01a837b5390502619689e5527fc951` (branch `rd-696-listen-remedy-cells-s84m`) — the original READY
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd696-READY-original-mail.txt` (cells, mutants, NOT closed)
  and the re-tag `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd696-READY-mail.txt` ("The body stands unchanged").
- **C — RD-594 subset (C-178), guard cells only** @ `c7fbf338e9ffeb64790208b2391c6c1b81b419fa` (branch `rd-594-kv-identity-open-window-s86m`) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-rd594-READY-mail.txt`

**Batched under the 2026-09-18 batch-gates rule, as batches #1-#4.** Every pair of A, B and C shares ONLY the counts file (MEASURED, `comm -12`); all
three are single commits directly on main `1904765` (MEASURED: `git log --format='%H %P' 1904765..<head>` = one line each, parent `1904765`). B and C are
tests only (no product file). **This gate has TWO legs:** the
ordinary code-gate leg (red-proofs, mutants, full verify, merged tree), and for A a **PACKAGE leg** that reuses the 2.2.1 package gate's checks
(MANIFEST, per-entry byte identity with the SHIPPED 2.2.1 zips, anonymous pull, arm-ttk locally with both controls, no Partner Center). **Every head is
re-read by `git ls-remote` in the launcher, which refuses on a mismatch.**

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 09:53
Self-check note: 2026-09-27 09:53

## TUESDAY'S RULINGS AT STAMP (they answer WRONG items 1, 2, 4, 13, 14 and 17)
- **`.github/workflows/arm-ttk.yml` (WRONG 1): COVERED — by C-138 + C-170, not C-165.** Tuesday's commission named the wrong C-number; the drafter's correction is ADOPTED (ledger 2026-09-27). C-138 is Kam's approval of this exact workflow's content and its Actions spend; C-170 (b) brings "every path whose 2.2.1 content a main build or main test needs", and `rd630-armttk-ci-workflow` reads the file. Measure §0 (a)-(d) as written; if the file at `be0fe37` is NOT blob-identical to the RD-630 file C-138 approved, or ANY other workflow changes, coverage FALLS and that is a STOP to name. **C-142's "Kam owns .github" is honoured by Tuesday flagging the copy to Kam on the live board before the merge push** (a flag, not an ask).
- **Renamed test ids (WRONG 4): AUTHORISED RENAMES under C-133's ADDENDUM, on these conditions only.** C-170 (b) brings "the tests that pin the package shape" and says "Re-anchored tests carry C-131/C-151-shape proofs", so the re-anchor is Kam's scope. Each missing id is accounted ONLY if: (1) its file at `be0fe37` is blob-equal to `3f79e9c`'s (a copy, not an edit); (2) the old->new pair is named in your table and the new id is present and GREEN; (3) the re-anchored cell carries its C-151 proof (Q-P7). **An id with no new counterpart and no C-131 removal naming it is a Major and a STOP for the merge.** Carry this ruling verbatim into the merge author's RELEASE.
- **RD-594's tier (WRONG 14): TIER 1.** Kam's own card (C-178 :1831) says "tier 1 gate", and his card outranks the builder's suggestion and Tuesday's commission. The k-rows were already at full depth; the verdict line reads TIER 1.
- **K2 re-runs on the merged population (WRONG 17): RULED binding.** At every lane-1 merge that touches the server source (rd-413, rd-681, rd-682, rd-627b, rd-695, rd-705 and any later one), the merge author re-runs rd594 by name on the merged tree and states K2's population in its MERGED mail. S86M records it as a C-number when RD-594 merges.
- **The merge grant's re-affirmation (WRONG 2): its source is Tuesday's TERMINAL, not the chat file.** Kam typed after /login, 2026-09-27 ~08:2x AEST: *"New account logged in. Please keep going with the work."* It is recorded in Tuesday's EXPIRING-GRANTS row (read by Tuesday at boot). The grant itself (2026-09-25 22:04) is unchanged.
- **Seats (WRONG 13): re-read at stamp** — 62649, 9959, 20317, 23230, 36118, 40285 and 16516 are all live (`ps` at stamp time).
- **Launch order:** after 5a and 6, as gate slots free. The launcher re-pins heads at launch.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did
not build these changes and you owe no builder anything. **Every line below that reports what a builder says is a CLAIM, never evidence.** Explore a
branch that COPIES 32 released package paths onto main plus one deletion (A), a tests-only file that guards a server's listen-failure branch (B), and
a tests-only file that guards "the Key Vault identity reaches no anonymous caller in the open setup window" by ENUMERATING routes from source (C),
looking for any state in which **main, once A is merged, builds a Marketplace package that differs from the one customers are served; a merge pushes
something that deploys, publishes, or touches Azure or Partner Center; a test id vanishes without an authorised rename; a copied file silently
reverts something main changed itself; a route hands the Key Vault identity to an anonymous caller while C stays green; or a "guarding" cell stays
green while the thing it is named for is broken.**

- **C-170 PACKAGE (RD-460) is TIER 1** (the package door; READY :6 "Tier 1 (package door)"; C-170 :1745 "Tier 1"). Verdict: **GO / GO WITH FINDINGS /
  NO GO at `be0fe37`**, plus its merged-tree result. A NO GO here means "do not merge into main", never "withdraw the live listing" — the live
  2.2.1 package is not this gate's target and nothing here touches it.
- **RD-696 is TIER 2** (tests only, no product change; READY :6 "Tests only"). Verdict at **`2c221fa`**, plus its merged-tree result.
- **RD-594 is TIER 1 (Tuesday ruled at stamp, per Kam's C-178 card; was TIER 2)** (Tuesday's commission: "tests only; guards a tier-1 security property"; READY :6 "Suggested tier 2"). **Kam's card text in C-178
  (:1831) says "tier 1 gate" — WRONG item 14; Tuesday rules the tier at stamp.** Whatever the tier label, the property it guards is a customer-security
  property: **rows k1-k12 are required at full depth.** Verdict at **`c7fbf33`**, plus merged-tree result.
- **One verdict PER ticket, one report, one mail.** A finding on one ticket never becomes another's verdict. A finding that exists only in a
  COMPOSITION is graded on the merged tree and named against both tickets' merged-tree lines.
- **TIER 1 AT FULL WEIGHT, FINDINGS-ONLY:** no fixes, no pushes, no deploys, nothing to Partner Center, the demo or production (§12).

## 0. THE `.github/workflows/arm-ttk.yml` QUESTION — the author asked it; the drafter read both rulings at source
The author's READY :10: *".github/workflows/arm-ttk.yml (the RD-630 arm-ttk workflow from the release line; it's copied, not new. Kam approved it in
C-138, but .github is Kam-owned, so please confirm this counts as covered)."* **This gate does not RULE on coverage (that is Tuesday's); it MEASURES
the facts the ruling rests on and reports them.** The texts, verbatim from
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md` (313,569 bytes, mtime 2026-09-27 09:09; line numbers by
`grep -n` at 09:2x AEST — re-read them, the file grows during the day):
- **C-138 (:1458)** — *"Kam ruled arm-ttk INTO CI: the Marketplace template toolkit runs on every change to `azure-marketplace/**`, from ONE new
  workflow file (RD-630). This supersedes Tuesday's 2026-09-21T21:32:49Z "no .github edits in lane C" line for RD-630 only (S78G)."* Kam's words
  (:1459): *"Yes, please put the check into CI. We've waited this long. Let's make the next submission as good as we can."* … *"The Actions spend is his
  decision, and this is it."* Tuesday's conditions (:1460): *"one NEW workflow under `.github/workflows/`; NO existing workflow edited (above all
  `deploy-demo.yml` and its `CI_DEPLOY_ENABLED` gate); arm-ttk and pwsh pinned explicitly …; it joins the one package gate and does not merge without
  that gate and a Tuesday GO"*. As built (:1461): pwsh 7.6.6 and arm-ttk 20260213, each by version AND sha256. Not covered (:1462): *"any other CI
  change; making the job a required status check …; moving the pins"*.
- **C-165 (:1688)** — Kam, live board **2026-09-26 07:18:54 AEST**:
  *"Decision nexusai-release-package-files-into-main: a — Yes, bring only the package files into main"*; scope then read by Tuesday as *"NOT the image, NOT release-policy or test re-anchors"*; SUPERSEDED IN PART (:1691).
- **C-170 (:1740)** — Kam, card `nexusai-package-files-scope`, live board **2026-09-26 21:05:47 AEST**:
  *"Decision nexusai-package-files-scope: b — Package plus what main needs to build and check it (recommended)"*. Scope now (:1744): *"a COPY onto a branch off current main (never a merge of
  the release branch; C-58/C-72 stand) of every path whose 2.2.1 content a main build or main test needs, each with its source sha and a PRIOR WORK
  line. Re-anchored tests carry C-131/C-151-shape proofs. The main build must reproduce the 2.2.1 MANIFEST sha256s. Tier 1. No deploy, no Partner
  Center (C-23)."*
- **C-142 (:1503, last sentence of its RD-641 bullet)** — the only CLARIFICATIONS source the drafter found for "Kam owns .github": *"A fix touching
  `.github/workflows` is mailed before pushing (Kam owns .github changes)."*

**Measure and report, each labelled:** (a) `.github/workflows/arm-ttk.yml` at `be0fe37` is blob-identical to `3f79e9c`'s (RD-630's file as released) and
to the file RD-630's own commit introduced (`git log -- .github/workflows/arm-ttk.yml` on the release line: `1e217fc` "WIP RD-630 …", READ by the
drafter); (b) **no OTHER workflow changes**: every other `.github/workflows/*` blob at `be0fe37` equals `1904765`'s (drafter: `deploy-demo.yml` blob
`953b2a2` at both); (c) **a main test needs it** — `__tests__/rd630-armttk-ci-workflow.test.js` (copied in A) reads `.github/workflows/arm-ttk.yml`
(`:14`, READ) — so it falls inside C-170's "every path whose 2.2.1 content a … main test needs"; (d) what the workflow does on a push to main (§7:
`on.push.branches` includes `main`, `paths` `azure-marketplace/**` — **merging A WILL start an arm-ttk run on main**, which C-138 names as Kam's
Actions-spend decision). **The drafter's reading, for Tuesday to confirm or correct: C-138 approved the workflow's content and its CI spend; C-170
brings "what main needs to build and check" the package, and a copied test reads the file; C-142's "mailed before pushing" is satisfied by the READY
itself having asked. Coverage is Tuesday's ruling at stamp.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **Merging on Tuesday's GO after a gate verdict at the head** — Kam, terminal, 2026-09-25 ~22:04 AEST: *"Please work your way through the tickets and
  merge once tested."* (Tuesday's daily note 2026-09-25 :84, READ by the drafter; as recorded in the batch #1-#4 briefs). Tuesday's commission says it
  was re-affirmed 2026-09-27 ~08:2x; **the drafter did not find the re-affirmation in `0_Brain/daily_tuesday/2026-09-27.md` or `chat_tuesday.json`
  (grep "merge once tested" / "work your way") — UNVERIFIED, RELAYED.** The grant covers merges only: **no deploy, no production, no Partner Center,
  no az writes.** This gate merges nothing into anything the fleet can see.
- **RD-696's origin — the batch #1 gate's C-F1 (RD-533, Minor)** is in that gate's report, not in CLARIFICATIONS (drafter `grep -n -i 'RD-696'` on
  CLARIFICATIONS → 0 lines; positive control, same file and tool: `C-141` found 10 times). Tuesday's commissioning of RD-696 is RELAYED by the READY.
- **RD-594's shape — guard cells, not a product change — is Tuesday's acceptance, recorded in C-178's own note (:1838, READ by the drafter at 09:4x;
  the READY :19 claim VERIFIED):** *"DELIVERED AS GUARD CELLS 2026-09-27; the property PRE-EXISTED via RD-518 round 3 (`4230d23`, G-01/RD-592:
  `healthDetailsForCaller` serves `keyVaultEncryption.detail` to admins only). MEASURED, not read: at main `1904765` the new cells … are GREEN 5/5 in
  the fresh open window, and the mutation that bypasses the projection reddens K1 and K2. No product code changed. Tuesday accepted that shape (ANSWER
  2026-09-26T23:12:25Z), superseding this entry's "with a red cell at main", and told Kam his card's premise was stale."* **Kam's own words (C-178 :1831)
  are "Close only the Key Vault identity (recommended)"; the card's (b) text says "tier 1 gate".** Whether "the property already holds" satisfies his
  "close" is Tuesday's relay to Kam (done, per the note); this gate MEASURES whether the property holds and whether the cells can see it break.
- **C-173 (:1765, Tuesday's rulings, 2026-09-26T22:52:14Z):** RD-660, RD-661, RD-642, RD-672 *"queue behind be0fe37's merge. Any package REBUILD or
  publish stays Kam's (C-23, C-27)."* and *"The lane-1 gate (batch 5) is drafted after batches 3 and 4 launch"*. So **A's merge unblocks four tickets**;
  your Q-P rebuild is evidence in your own directory, never a publishable package.

**The clarifications that bind this gate** (the file above; line numbers at 09:2x AEST, re-read them):
- **C-02** (:30) open mode. **C-20** (:117) real-Azure behaviour is tested through the Marketplace. **C-23** (:132) Kam alone uploads to Partner Center.
  **C-27** (:148) the customer image push is Kam's. **C-28** (:153) never write, pull, check out or stash NexusAI's `2_Project_Files`. **C-38** (:210) /
  **C-45** (:266) the self-contained package (the control build at main FAILS because of them — READY :20). **C-40** (:225) a check must be able to fail
  on the thing it claims. **C-49** (:299) prior-work check.
- **C-57** (:410) a conflict confined to the counts file is resolved by REGENERATION with the id-superset control; *"Any other conflicting file still
  stops."* **C-58** (:433) the four package decisions (digest-only image; the anonymous-pull probe KEPT, item 4). **C-72** (:695) the customer image is
  built from MAIN at the merged head — **after A merges, the next image is built from a main that carries the copied docs and scripts; §4 Q-P10 asks
  what, if anything, of A enters the image.**
- **C-68** (:657) a verdict holds only at its head; semantic overlaps re-run by NAME; *"a clean merge-tree and a changed measured surface are not in
  tension"*. **C-76** (:729) an explanation is a claim. **C-89** (:827) after a merge commit: `git diff --quiet HEAD`, HEAD's counts = the regenerated
  numbers. **C-102** (:945) early returns disarm negative cells (§3b). **C-104** (:972) never census an unresolved merge.
- **C-110** (:1101) THE FLOOR RULE. **C-112** (:1141) a declared limit is where the evidence stops. **C-122** (:1278) source text does not cover
  behaviour. **C-125** (:1320) the foreign-server counter.
- **C-131** (:1407) a check pinning a REMOVED feature is re-anchored, not kept by restoring it. **C-133** (:1426) base-aware id accounting, and its
  **ADDENDUM** (the authorised-rename case, same entry). **C-151** (:1577) a pinned "not yet set" value is RE-ANCHORED, the old refusal kept on a COPY.
  **C-170 says A's re-anchored tests carry C-131/C-151-shape proofs — verify that claim per re-anchored cell (§4 Q-P7).**
- **C-138** (:1458), **C-142** (:1503) what "green" means at a merge (local verify green AND CI Build failing set = the known set; *"Kam owns .github
  changes"*), **C-149** (:1561) the release image, **C-150** (:1570) C-133's conditions are decided on blobs, **C-158** (:1634), **C-161** (:1652) 2.2.1
  is LIVE, **C-162** (:1659) the RD-665 port on main (the only main change to the template since `0677388`), **C-165** (:1688), **C-170** (:1740),
  **C-173** (:1765), **C-174** (:1784) NEVER KILL BY PATTERN, **C-178** (:1830; build bullet :1832; its DELIVERED note :1838) RD-594's Key Vault
  subset — *"your open window is otherwise unchanged"* is the bar (:1834); **C-124** (:1307) the Key Vault success path (RD-594's NOT TESTED names it).
- **C-141** (:1480) a builder's proof ticket YIELDS to a `qa-*` ticket; ADDENDUM (:1488) a MERGE hold is gate-class; ADDENDUM 2 (:1490); ADDENDUM 3
  (:1492) self-applied; **ADDENDUM 4** (:1494) a yield re-queues behind with `nexusai-lock.sh <kind> <tag> --after <ticket-tag> <cmd…>`.
- **Highest C-number at drafting: C-179** (:1840 at the 09:4x re-read; the file grew from 313,569 to 314,204 bytes, mtime 09:37, while the drafter
  worked — S86M appended C-178's DELIVERED note).

## PRIOR ROUND
PRIOR ROUND (package leg): the **2.2.1 package gate** gated `e3d9301b5101d8310c19f9e100c5001e1122fa22` (package commit `3f79e9c`), verdict **GO WITH
FINDINGS** (2026-09-25 18:52–19:40 AEST).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-pkg-gate-221/report.md`
(verdict :3; findings F-1..F-4 :13-; Q0 :42; Q1 :58; Q2 :78; Q3 :123; Q4 :156; Q5 :174; Q6 :187; Q7 :203; Q11 :259; floor :272; self-corrections :291;
NOT TESTED :299). Its brief: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-package-gate-221.md`.
Findings carried forward and their disposition:
- **F-1..F-3** (handover doc wording, evidence hygiene) — about the 2.2.1 DOC Kam received; not in A (A does not copy `docs/resubmission/`, READY :13).
  Not re-opened.
- **F-4** (the RD-665 rule reads only top-level resources and accepts any `/api/health` host) — **the RD-665 cell file is ALREADY on main** (C-162)
  and A does not touch it (not in A's delta). Carried as KNOWN.
- **2.2.0 gate F-3 (a CONSISTENT wrong digest), partly closed by c2b** — A copies c2b (`__tests__/marketplace-package-build.test.js` at `3f79e9c`)
  onto main: re-run the BW arm (template AND both exceptions → one wrong well-formed digest) on `be0fe37` — predicted exactly c2b-green red (Q-P6).
- **Reuse its instruments BY COPY** (all present, `ls` at 09:3x AEST):
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-pkg-gate-221/evidence/qa-q2q5.py` (per-entry zip
  compare), `…/qa-struct.py` (template structural diff), `…/qa-mutate221.py` (package mutants), `…/qa-q2ctl.py`, `…/qa-ids.py`, `…/qa-mkarm.sh`,
  `…/qa-runlib.sh`, `…/qa-jestwrap.sh`, `…/qa-jsum.js`, `…/qa-to.sh`. **Its self-corrections are rules here:** H-17 (Q3 attempt 1 VOID from a relative
  tool path — absolute paths only), H-18 (zsh `$s:<letter>` history modifiers ate `sha:path` — the drafter hit it AGAIN today; `/bin/bash` and
  braces, H-11), H-19 (a gitleaks canary JSON-escaped inside a string does not fire `arm-template-secret-parameter` — plant it as a real key).

PRIOR ROUND (RD-696): the **batch #1 gate** gated RD-533 at `95c3c9a` (TIER 2), **GO WITH FINDINGS**; RD-533 merged (`748cece`, an ancestor of
`1904765`).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch1/report.md`
(§6 RD-533 :220-; §6.3 mutants M-C4 :240, M-C5 :241; §6.4 rows c1-c9 :244-; §6.5 harness consumers :261; findings C-F1 :428; limits L-C3/L-C4 :481-482).
- **C-F1** (Minor): *"the remedy text (M-C5: 173/173 green), the 250 ms delay (M-C4: 4/4) and the non-EADDRINUSE (EACCES) branch are guarded by no
  cell; the behaviour is right (c4)"* → **RD-696 claims to close the remedy text (M-C5), the EACCES branch (c4) and the file transport (c3), and states
  M-C4 stays OPEN.** Re-derive every one of those claims (§5).
- Reuse its instruments BY COPY: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch1/evidence/qa-floorlib.sh`
  (**its defaults are STALE: `ROOT=33673`, `NEG=88756,10246,10643,11987,51143` — correct BOTH**), `…/qa-floorcount.py`, `…/qa-dispatch.sh`,
  `…/qa-holdlib.sh`, `…/qa-mutate.py`, `…/qa-merge.sh`, `…/qa-mkarm-clone.sh`, `…/qa-ssprint.sh`, `…/qa-h1-selftest.sh`, `…/qa-h1-scan.py`,
  `…/qa-c57-id-superset.sh`, `…/qa-netbelt.sb`, `…/qa-netbelt-ctl.js`, `…/qa-srvlib.js`, `…/qa-c-probe-v2.js` (the RD-533 c-row probe),
  `…/qa-lockcheck.js`, `…/q-merged-identity.py`, `…/q-c68-sets.sh`. The original counter is gate 7's
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`.
PRIOR ROUND (RD-594): the property RD-594's cells guard was built and gated as **RD-518 round 3** at `4230d237321a2f252730aeca37c73a950eca0f25`,
verdict **GO** on G-01 (RD-592) and G-02 (RD-593), 2026-09-21.
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd518-4230d23-round3/report.md`
- It drove the health-detail projection (`healthDetailsForCaller`, `publicKeyVaultState`) with `NODE_ENV=production`, one fresh DATA_DIR per state; the
  RD-518 r3 cells (`__tests__/rd518-r3-health-detail-decision.test.js`) drive S5 (no Entra, users present) and S6 (first run incomplete, users present).
  **RD-594 claims the gap is the FRESH store (no users) and every route other than `/api/admin/health`** (READY :24, the cell file's header). Read
  that report's state table and say whether the fresh-store state was really undriven (C-49), and whether RD-594's K1 is then new coverage or a
  duplicate.
- Carried-forward findings: read its Minor/Polish list and say whether any bears on K1/K2 (e.g. a field it named as residual).

- **Concurrent gates today, read for context, NOT re-run:** batch #3 (`2026-09-27-gate-batch3`, lane 2 erasure) and batch #4
  (`2026-09-27-gate-batch4`, lane 3 image content) were LIVE at drafting (panes `%23` claude `36118`, `%24` claude `40285`). Either may MERGE into
  main during your gate — see "Main may move".

## 1. Targets — verified at drafting from the object store (09:27–09:40 AEST)
**origin by `git ls-remote` at 2026-09-27 09:27:41 AEST:** `main` **`1904765007e9447ac6c980f9840c0689a02abe6c`** · `rd-460-pkg-into-main-s84m`
**`be0fe3704023d8f092da0be27f79b82fbc029085`** · `rd-696-listen-remedy-cells-s84m` **`2c221fa2ed01a837b5390502619689e5527fc951`** (= Tuesday's commission).
No `rd-594*` branch at origin at 09:27:41; **re-read at 09:41:43 AEST (all four identical to the above for main/A/B):**
`rd-594-kv-identity-open-window-s86m` **`c7fbf338e9ffeb64790208b2391c6c1b81b419fa`** (= Tuesday's message). Lane 1's other branch at origin:
`rd-705-no-store-authenticated-pages-s86m` `e164d1a` (not a member). Every sha is a commit in the local object store (`cat-file -t`).
**Other pinned shas, in full:** the 2.2.1 PACKAGE COMMIT `3f79e9cb8ed8834e08a1744af8bbbd5823d4303a` (3f79e9c) · the 2.2.1 gated head
`e3d9301b5101d8310c19f9e100c5001e1122fa22` (e3d9301) · the RD-665 fix `d14a975e6a325b0b246fbb85287b7831f22e5f33` (d14a975) · the image commit
`0677388ab031ffaf569a52f6c0301af48f44aece` (0677388) = `merge-base(3f79e9c, 1904765)`.
**Re-read at your start, mid and end. A moved TICKET head is a finding and a reason to stop, never a typo to fix.**

**Main may move during your gate.** Call main at your start **M0**. (1) M0 must be `1904765` or a DESCENDANT of it; (2) `git diff --name-only 1904765 M0`
must share NO path with A's 34-path delta, B's or C's 2-path delta except `scripts/verify-expected-counts.json` (the launcher refuses on a hit; re-check
it yourself) — **and a movement that touches `backend/server.js` changes C's K2 POPULATION (row k9): say so and run K2 on M0's population**; (3) your
merged tree is **M0 + A + B + C**, predicted counts **counts(M0) + 157 tests / + 9 suites (4290/256 at M0 = `1904765`)**; (4) **batch #3
and batch #4 may merge first.** Neither shares a path with A or B (drafter: batch #3's deltas are the erasure/LAW/storage modules + their cells; batch
#4's are `.dockerignore`, `Dockerfile`, `__tests__/helpers/image-manifest.js`, `image-content-exposure`, `rd385-shipped-root-markdown-identifiers`,
`rd418/rd698/rd699/rd327` cells — from their launchers' expected-file lists, READ). **If batch #4 is in M0, its image-content guards join A's C-68 set
(row X2).** (5) if main moves AGAIN during your gate, your verdict names M0 and says what moved (C-68). **Never re-base mid-gate.**

### TARGET A — C-170 / RD-460, the package into main (TIER 1)
- **Chain (MEASURED):** ONE commit, `be0fe37`, parent **`1904765`** only; committed 2026-09-27 01:26:58 +1000; message "RD-460 / C-170: bring the released
  2.2.1 package files, and what main needs to build and check them, onto main". `merge-base(be0fe37, 1904765) = 1904765` (fast-forwardable).
- **Delta over `1904765`: 34 files, +2112/−602** (MEASURED `--shortstat`): **32 copied paths + 1 deletion + the counts file** —
  - `A` `.github/workflows/arm-ttk.yml`, `__tests__/dev-scripts-template-parameters.test.js`, `__tests__/helpers/shipped-plan-build.js`,
    `__tests__/listing-folds-rd465-rd454.test.js`, `__tests__/marketplace-setup-checks.test.js`, `__tests__/marketplace-single-build-path.test.js`,
    `__tests__/rd471-wizard-image-element-types.test.js`, `__tests__/rd472-image-bearing-resources.test.js`, `__tests__/rd630-armttk-ci-workflow.test.js`,
    `azure-marketplace/listing-assets.txt`, `scripts/arm-ttk-check.sh`;
  - `M` `DEPLOYMENT_GUIDE.md`, `README.md`, `__tests__/marketplace-keyvault-durability.test.js`, `__tests__/marketplace-package-build.test.js`,
    `__tests__/marketplace-template-log-analytics-enabled.test.js`, `__tests__/rd461-self-contained-and-template-toolkit.test.js`,
    `__tests__/rd503-r2-doc-claims-against-product.test.js`, `azure-marketplace/combined/README.md`, `azure-marketplace/combined/mainTemplate.json`,
    `azure-marketplace/plans/README.md`, `azure-marketplace/plans/managed-ai/createUiDefinition.json`, `azure-marketplace/release-policy.json`,
    `azure-marketplace/submission-readiness-checklist.md`, `docs/HOSTING_AND_COST_ANALYSIS.md`, `docs/MARKETPLACE_TEST_PROCEDURE.md`,
    `docs/REFERENCE_ARCHITECTURE.md`, `docs/marketing/MARKETPLACE_LISTING_CONTENT.md`, `scripts/deploy-dev.sh`, `scripts/marketplace-package-build.sh`,
    `scripts/provision-customer.sh`, `scripts/validate-marketplace-template.sh`, `scripts/verify-expected-counts.json`;
  - `D` `scripts/build-plan-packages.sh` (absent at `3f79e9c` too — "retired by RD-506").
  **No `backend/`, `static/` or other runtime path is in the delta** (MEASURED from the list).
- **Copy identity (MEASURED, the drafter's own loop):** for every A path except the counts file and the deletion, `rev-parse be0fe37:<p>` ==
  `rev-parse 3f79e9c:<p>` — **32/32 equal, 0 not equal**; the deletion path is absent at `3f79e9c`. **`git diff 3f79e9c be0fe37 -- azure-marketplace`
  is EMPTY.** `be0fe37` vs `3f79e9c` differs in **29** paths (= the 25 "main-only" paths + the 3 "NOT copied" + the counts file, READY :13-14 —
  arithmetic, verify it); `1904765` vs `3f79e9c` differs in **62** (= READY :8's inventory count).
- **Package blobs (MEASURED `rev-parse`):** `mainTemplate.json` `3a8a35c` at `0677388` → **`eed2dac` at `1904765`** (the RD-665 port, C-162) →
  **`93ecbca` at `d14a975`, `3f79e9c`, `be0fe37`**; `createUiDefinition.json` `7deabd8` (main) → `6d87b9d`; `viewDefinition.json` `c8d5fd5` everywhere;
  `release-policy.json` `32e432b` (main) → `c3db2d5` (`d14a975`) → `241f983` (`3f79e9c`, `be0fe37`); `marketplace-package-build.sh` `803f05b` (main) →
  `40ec7de`. **So main's ONLY own template change since `0677388` (RD-665, C-162) is superseded by a template that ALSO carries it — prove that
  structurally, not by the READY's sentence (Q-P3).**
- **Counts (MEASURED):** `1904765` **4133/247** → `be0fe37` **4280/254** (+147/+7); `3f79e9c` 4125/242; `e3d9301` 4127/242.
- **The builder's evidence (outside the repo, READ ONLY):** `session-tools/s84m/pkg-copy-set.txt` (33 entries = 32 copies + the deletion; READ),
  `pkg-diff-inventory.txt`, `pkg-prior-work.txt`, `pkg-verify.log` (the FAILED first verify), `pkg-verify2.log`, `pkg-build-final-be0fe37/`
  (`MANIFEST-2.2.1_be0fe37.txt` ending `MANIFEST COMPLETE: 32 checks, 0 failed`, first line `… version 2.2.1, commit be0fe37…`; plan zip sha256
  `621b94b5…94c0`, listing `0c6f40f0…3ad9`), `pkg-build-control-main-1904765/FAILED-MANIFEST-2.2.1_1904765.txt`.
- **Drafter's READ-ONLY pre-reading of the zips (python `zipfile` in memory, nothing written):** the builder's be0fe37 plan zip entries
  `mainTemplate.json` `f91ee8f1006e76e1…`, `createUiDefinition.json` `51cb0b8d8b1dcc23…`, `viewDefinition.json` `3f3fc3b292ba83a3…` — **equal to the
  SHIPPED 2.2.1 plan zip's three entries**; listing 7/7 entries equal. **Whole-file shas differ** (plan 18 022 bytes both; listing 626 778 bytes both):
  entry timestamps — the plan entries carry build time, the listing entries the COMMIT time via `git archive` (pkg221 Q6). **You measure it.**
- **The SHIPPED 2.2.1 zips (the live listing's package, C-160/C-161) — hashed by the drafter at 09:3x, equal to C-160 and the pkg221 report:** in
  `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.1/`: plan `NexusAI_plan-managed-ai_2.2.1_3f79e9c.zip`
  `5fb547893535ecd891b8147cf117c83f83b2f05dfc68f28f7732383aaf1172dd`, listing `NexusAI_listing-assets_2.2.1_3f79e9c.zip`
  `ba29c1890df2bb1b9c1edcd884eecdf2151db9a71211badf807156b355b9a7e7`, manifest `MANIFEST-2.2.1_3f79e9c.txt`
  `75ae0aa7283652b6d69696414fb864c4f13a28b2ac7364de184abce53ab58100`. **Never write into that directory; copy before unzipping; hash at start and end.**
- **Builder's claims (RELAYED):** non-draft build at `be0fe37` rc 0, "MANIFEST COMPLETE: 32 checks, 0 failed", the live anonymous-pull check passed;
  MANIFEST identical to the shipped one after normalising commit sha, zip sha/bytes and build time; the three JSON entries byte-identical; CONTROL build
  from `1904765` exits 1, FAILED-MANIFEST only, no zip; verify **4280/4280 across 254** (`--update-counts`, lock, SESSION_SECRET unset), floor 0/0,
  C-89 clean, pre-commit gitleaks clean; first verify FAILED 3 RD-506/RD-526 guard cells (`marketplace-single-build-path.test.js`) until three
  "excluded" files were copied (READY :24, "DISCLOSED"). Branch amended before first push (ls-remote showed no branch).
- **NOT TESTED — VERBATIM (READY :28-32):**
  *"- arm-ttk: not run locally in this item; the copied arm-ttk.yml workflow runs it in CI once a PR exists."* ·
  *"- No deploy (C-23: nothing to Partner Center)."* ·
  *"- The dev scripts (deploy-dev.sh, provision-customer.sh) were not executed, only their test cells."* ·
  *"- Linux/CI: not run yet (no PR)."*
  → **L-P1** (arm-ttk not run locally by the author — you run it, Q-P8) · **L-P2** (no deploy, Partner Center) · **L-P3** (dev scripts not executed) ·
  **L-P4** (Linux/CI — arm-ttk in CI is UNMEASURED unless a PR exists).

### TARGET B — RD-696 (TIER 2, tests only)
- **Chain (MEASURED):** ONE commit, `2c221fa`, parent **`1904765`** only; 2026-09-27 04:04:39 +1000, "RD-696: cells for RD-533's unguarded listen-failure
  parts (tests only)". `merge-base(2c221fa, 1904765) = 1904765`.
- **Delta over `1904765`: 2 files, +111/−3** — `A __tests__/rd696-listen-failure-remedies.test.js` (108 lines), `M scripts/verify-expected-counts.json`.
  **No product file.** Counts **4133/247 → 4138/248** (+5/+1; MEASURED).
- **What the cells do (READ at `2c221fa`):** ONE `beforeAll` boots server A through `helpers/rd395-server-harness` (`bootServer`), then spawns a SECOND
  server with `spawn(process.execPath, [<the server entry point>])` on A's port (EADDRINUSE) and again with `PORT` = a socket path inside a `chmod 0o500`
  directory (EACCES, the batch #1 gate's c4 shape); each spawn gets a fresh DATA_DIR/HOME, sign-in env blanked, a 60 s race, SIGKILL on timeout; reads
  `<HOME>/LogFiles/error.log`. Cells: (1) EADDRINUSE → `REMEDY_IN_USE`, not `REMEDY_OTHER`; (2) the failure line in `error.log`; (3) exit < 5 s from spawn;
  (4) fixture CONTROL: the locked dir refuses writes; (5) EACCES → exit 1, names EACCES, `REMEDY_OTHER`, never "running on port". `afterAll`
  restores 0o700 and `fs.rmSync`s its own temp dirs. `jest.setTimeout(300000)`.
- **Builder's claims (RELAYED):** all 5 green at base (tests only); reds by mutation in one hold (`session-tools/s84m/rd696-hold.log`, `rd696-hold.sh`):
  **M-C5** (remedy swap) → cells 1 and 5 red; **delay 250 → 8000 ms** → cell 3 red; **`logger.error` → `console.error`** → cell 2 red; every anchor
  count 1, every mutant restored by sha. Verify **4138/4138, 248 suites**, counts committed, C-89 re-stage done; a header comment changed AFTER the
  verify and the file was re-run alone 5/5. "Jest did not exit one second after…" is pre-existing (also on rd533's file alone).
- **NOT closed — VERBATIM (original READY :22):** *"NOT closed: M-C4 itself. With the delay at 0, and with a bare process.exit(1), all 5 cells stay
  green, because the line still lands in error.log on this Mac. No cell here can tell the delay is gone. The test header says so, and the Jira comment
  records it."* (The READY has no section titled "NOT TESTED"; this paragraph is its declared limit.) → **L-B1** (M-C4, the 250 ms delay, UNGUARDED) ·
  **L-B2** (Linux/CI and a non-Mac file transport — not declared by the author; the drafter's addition, C-112).
- **A drafter's READ you must MEASURE (row t5):** the "header comment changed after verify" means the COMMITTED file's blob is NOT the blob the full
  verify ran; say which blob your verify ran and that it is `2c221fa`'s.

### TARGET C — RD-594 subset (C-178), guard cells only (TIER 2; see WRONG item 14)
- **Chain (MEASURED):** ONE commit, `c7fbf33`, parent **`1904765`** only; 2026-09-27 09:37:33 +1000, "RD-594 subset (C-178): guard cells: the Key Vault
  identity reaches no anonymous caller in the open window". `merge-base(c7fbf33, 1904765) = 1904765`.
- **Delta over `1904765`: 2 files, +147/−3** — `A __tests__/rd594-kv-identity-open-window.test.js` (144 lines), `M scripts/verify-expected-counts.json`.
  **No product file.** Counts **4133/247 → 4138/248** (+5/+1; MEASURED — the same numbers as B's head, by coincidence). `backend/server.js` is blob
  `bc099b2` at `1904765` and `c7fbf33` (and unchanged by A and B).
- **What the cells do (READ at `c7fbf33`):** ONE `beforeAll` boots a server through `helpers/rd395-server-harness` (`bootServer`, tag `rd594`, 150 s boot
  timeout) on a FRESH store (no seed: no users, first run incomplete, no sign-in — Entra env blanked), with `KEYVAULT_NAME`
  `nexusai-rd594-nonexistent-vault`, a wrap-key name, `KEYVAULT_IDENTITY_CLIENT_ID` a synthetic GUID, `RATE_LIMIT_MAX` 20000; sleeps 3 s.
  `getRoutes()` = every `^app\.get\('(\/api\/[^':*]+)'` literal (multiline) in the server entry point's SOURCE — **78** (drafter reproduced the regex
  with python at `1904765`, `c7fbf33` and `be0fe37`: 78 each, `/api/admin/health`, `/api/setup/status`, `/api/health` all in it). `scan(text)` = the
  client id, the vault name, or `/vault\.azure\.net/i`. `get(p)` = one anonymous `fetch`, `redirect: 'manual'`, 20 s abort; a thrown error becomes
  `status: null`. Cells: **PRE** (the server log says `KV path FAILED` and names the client id — detail IS populated); **POP** (≥ 50 routes and the three
  known members); **K1** (anonymous `/api/admin/health`: 200, `keyVaultEncryption` an object with NO `detail`, no id/name/host anywhere); **K2**
  (control (a): `scan(h.output)` fires on identity AND vault name; drive all 78 anonymously; control (b): `/api/admin/health` answered 200; ≥
  `floor(78 × 0.9)` = 70 answered with a non-null status; `leaks` empty); **CTRL-OPEN** (anonymous `/api/admin/health` and `/api/setup/status` both 200).
  `jest.setTimeout(420000)`; `afterAll` stops the server and `fs.rmSync`s its dirs.
- **The population, measured by the drafter on the same file (python, READ):** 86 `app.get('/api/…')` literals in all (any column, any quote), 78
  parameter-free + **8 with `:param`/`*`**; 0 indented, 0 double-quoted or backtick; **12 `app.use('/api…')` router mounts** and 8 other `<x>.get('/…')`
  calls — the declared "routers" limit is real and sizeable (row k7).
- **Builder's claims (RELAYED, READY :9-19):** GREEN at `1904765` 5/5; **M1** (`healthDetailsForCaller`'s admin check replaced by `return full;`, anchor
  count 1) reddens K1 and K2, and K2 names exactly `/api/admin/health 200 {identity:true, vaultName:true, vaultHost:true}`; the server source restored by
  sha (`session-tools/s86m/rd594-hold.log`); verify **4138/4138 across 248**; merge-tree "against rd-413, rd-695, rd-460, rd-681, rd-682, rd-627b,
  rd-696 and rd-705, the only conflict each time is scripts/verify-expected-counts.json (C-57)" (scratch object dir `session-tools/s86m/mt-objects-rd594`).
  C-68 note (READY :32): *"K2 enumerates routes from server.js at run time. After any frozen lane-1 branch merges (rd-413 adds a health field; rd-681/682
  change a route), K2 re-runs on the merged population."*
- **NOT TESTED — VERBATIM (READY :34-37):**
  *"- /api/setup/managed-identity's principalId on a real Azure host (VM IMDS, or App Service WEBSITE_OWNER_NAME).
  That is not the Key Vault identity and cannot be produced locally. Unmeasured."* ·
  *"- Routes with :params, non-GET routes, and routes outside server.js (routers). K2's population is the literal GET set only."* ·
  *"- The demo, and a real Key Vault success path (C-124)."*
  → **L-C1** (managed-identity principalId on a real host) · **L-C2** (param, non-GET and router routes — 8 + every non-GET + 12 mounts) · **L-C3** (the
  demo; the Key Vault SUCCESS path — when the vault resolves, is the identity in any other field?).

### File overlap and MERGE-TREES
Name sets over each head's merge-base with main (all `1904765`): A (34), B (2), C (2). **`comm -12` A∩B = A∩C = B∩C = `scripts/verify-expected-counts.json`
only** (MEASURED). **Merge-tree NOT run by the drafter** (its hard rules forbid `merge-tree --write-tree` against the project repo, even with a scratch
object dir). **Predicted:** M × A, M × B, M × C fast-forward (each head contains M); **every pair = counts-only conflict** (each regenerated the one file
from `1904765`); C's author RELAYS the same for A×C and B×C. **The launcher's guard 80 measures A×B, A×C and B×C in a FRESH scratch object dir
(NexusAI's store as a read-only alternate) and refuses on anything but counts-only; re-measure them yourself (§9 Q1).**

### MERGE ORDER — the drafter's proposal, with its predicted end state and the C-68 re-run set per merge
**Proposed order: 1. C-170 package (A) → 2. RD-696 (B) → 3. RD-594 (C).**
Why: A is the tier-1 item four tickets wait behind (C-173); it is a fast-forward on M0 = `1904765` (no counts merge at all), so its merge is the cheapest
and its CI run (Build + arm-ttk, §7) happens on a main that holds nothing else new; B then merges counts-only; **C LAST, because its K2 population is
enumerated from the server source at run time — it is measured on the tree that holds everything else (C-68; READY :32).** Neither A nor B changes the
server source (blob `bc099b2` throughout), so the population is predicted unchanged at every step — **measure it (78) on the merged tree anyway.** The
order is file-independent (every pair = counts), so **order independence is the control (§9 Q4), not an assumption. Challenge it if any row says
otherwise.**

| step | merge | predicted conflicts | predicted counts after | C-68 re-run set BY NAME (on the tree after that step) |
|---|---|---|---|---|
| 1 | M0 + A | none at M0 = `1904765` (fast-forward); counts only if M0 moved | **4280/254** at `1904765` | every file in A's delta under `__tests__/` (the 8 new + 5 modified + the helper's consumers) + every `marketplace-*`, `rd461-*`, `rd471-*`, `rd472-*`, `rd503-*`, `rd630-*`, `rd665-*`, `dev-scripts-template-parameters*`, `listing-folds-*` suite + `rd385-shipped-root-markdown-identifiers` + `image-content-exposure` (C-72: does A change what ships? row X2) |
| 2 | + B | **counts only** | **4285/255** | rd696 + rd533-listen-error-fails-loudly + rd510-listen-before-warmup + every suite importing `helpers/rd395-server-harness` or `helpers/test-server` that asserts on listen failure (batch #1 §6.5: `git grep -l -i -E 'EADDRINUSE|running on port'` = 10 suites + the helper at M) |
| 3 | + C | **counts only** | **4290/256** | rd594 (K2 on the MERGED population, 78 predicted) + rd518-r3-health-detail-decision + every suite that drives `/api/admin/health`, `healthDetailsForCaller`, `publicKeyVaultState` or `adminGateRefuses` + every suite importing `helpers/rd395-server-harness` (B's and C's shared harness) |

**End state predicted: 4290/256 = 4133 + 147 + 5 + 5 / 247 + 7 + 1 + 1 — ARITHMETIC; C-68 says the measurement decides.** **Re-derive every set in YOUR
clone with a positive control** (the ticket's own cell file must be found): `git grep -l -E 'marketplace-package-build|release-policy|mainTemplate|
createUiDefinition|listing-assets|arm-ttk|shipped-plan-build'`, `git grep -l -i -E 'EADDRINUSE|EACCES|running on port|Could not listen'` and
`git grep -l -E 'admin/health|healthDetailsForCaller|publicKeyVaultState|adminGateRefuses|KEYVAULT_IDENTITY_CLIENT_ID'` over `__tests__` at M0 (the
drafter ran no content search over the tree — hard rule); add what the table misses and say which.

### How to build your trees
- **No worktree is created in the NexusAI repo, and you never work in its `2_Project_Files` checkout (C-28).** In that repo use ONLY read verbs:
  `show`, `log`, `diff`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `grep`, `ls-remote`, `archive`, `count-objects`. Never `fetch`, `pull`,
  `push`, `checkout`, `worktree`, `commit`, `stash`, `gc`, `clean`, or `merge-tree --write-tree` without a scratch `GIT_OBJECT_DIRECTORY` of your own.
- **Head trees:** `git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/qa-trees/batch5b.XXXXXX/>`, git-indexed where a full verify or a cell needs a
  git tree. **The package build reads the repo through `git archive`/`rev-parse` only; run it with the cwd INSIDE your own archive extract** (2.2.0 gate
  F-6: the listing-list argument is a FILESYSTEM path relative to the cwd).
- **The merged tree:** §9, in **your OWN scratch clone** (`git clone --shared --no-checkout <repo> <your own dir>`).
- **Each tree is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree for a clean arm; `batch5b`-prefixed
  directories only. Earlier gates' trees are their evidence — copy from, never run in.
- `node_modules`: an APFS clone (`cp -c -R`) of the newest gate tree you trust, **after proving** `package-lock.json` is blob `9064763` there too (it is
  `906476350431e2ecb3c21070a25c64b1702c1aa8` at `1904765`, `be0fe37`, `2c221fa`, `c7fbf33` — MEASURED); a real directory, never a symlink.

## 2. Why these tiers, and who is waiting
- **C-170 PACKAGE TIER 1:** after this merges, every future package build and every package test runs from main. **A main that builds a package whose
  zipped `mainTemplate.json`, `createUiDefinition.json` or `viewDefinition.json` differs from the SHIPPED 2.2.1 zip's by one byte is a Blocker; a copy
  that silently reverts a change main made itself (a "Class C" path) is a Blocker; a merge that triggers a deploy, an image build or any Azure write is a
  Blocker (§7); a test id lost without an authorised rename is a Major (C-57/C-133); a re-anchored cell with no red proof (C-151 shape missing) is a
  Major; a copied doc that states something false about the product is a Minor.**
- **RD-696 TIER 2:** tests only. **A cell that stays green when the property it is NAMED for is broken is a Major (C-40); a cell that is flaky or leaks
  a server/port/chmod'd dir is a Minor; an unguarded property the READY declares (M-C4) is NOT a finding — it is L-B1, carried.**
- **RD-594 TIER 2 (guarding a tier-1 security property):** **any parameter-free GET /api route that returns the Key Vault identity clientId, vault name
  or vault host to an anonymous caller in the fresh open window is a Blocker — against the PRODUCT, found by this gate, whatever C's cells say; a K1/K2
  that stays green when a route leaks (a blind population, a scanner that sees nothing, a threshold that passes on errors) is a Major (C-40); a CTRL-OPEN
  that cannot fail is a Minor; a route that leaks the identity through a `:param`, non-GET or router path is L-C2 — MEASURE it if cheap (k7), grade it
  on the product.**
- **Who is waiting:** the merge author is the live lane-1 seat **NexusAI-M (S86M)** (pane `%19`, claude `62649` at 09:29:23 AEST) — also C's author.
  RD-660, RD-661, RD-642 and RD-672 queue behind A's merge (C-173); S86M's next item is RD-646+RD-647, its red run `s86m-rd646-red` queued in the lock
  (RD-594 READY :39) — expect a live queue.

## 2a. LEGITIMATE SHAPES — required measurements, row by row (the checkers here are `scripts/marketplace-package-build.sh`, the re-anchored package suites, and RD-696's cells)
**Columns: the head, the base it is measured against (M = `1904765`), and the MERGED tree. Every build row: the REAL build script, non-draft unless the row
says draft, a NEW empty out-dir, cwd inside your own extract, `TMPDIR` in your project.**

**P — the package build (A).**

| row | shape | expected at `be0fe37` | at M | predicted-by |
|---|---|---|---|---|
| p1 | non-draft build, version `2.2.1`, the shipped files as copied | rc 0; `MANIFEST COMPLETE: 32 checks, 0 failed`; 2 zips + manifest | rc 1; `FAILED-MANIFEST` only; no zip | builder (proof + CONTROL) |
| p2 | p1's three plan entries and seven listing entries vs the SHIPPED 2.2.1 zips' | **all 10 byte-identical**; entry-name sets identical | — | builder + drafter's READ ONLY pre-reading |
| p3 | p1's MANIFEST vs the shipped `MANIFEST-2.2.1_3f79e9c.txt` | identical after normalising commit sha, zip sha/bytes, build time — **list every differing line and classify it** | — | builder |
| p4 | the same build at `3f79e9c` (the package commit), your own extract | rc 0, the same 10 entries — the "same package" baseline measured in YOUR window | — | drafter (pkg221 Q6) |
| p5 | version `2.2.0` at `be0fe37` | rc 0 (the `"2.2.0"` exception is still present) | — | drafter (pkg221 V3: the version is not bound to content) |
| p6 | the `"2.2.1"` exception REMOVED (a copy), version 2.2.1 | rc 1, "no exception for exactly this image" | — | drafter (pkg221 V1) |
| p7 | the `"2.2.1"` image one hex off (a copy) | rc 1; **and through the package suites: c2b-green red, by name** | — | pkg221 V2/V2J |
| p8 | BW: template AND both exceptions → one wrong well-formed digest (a copy) | the real build: rc 1 at the anonymous-pull probe; the suites: exactly c2b-green red | — | pkg221 BW (2.2.0 gate F-3 residual) |
| p9 | a leftover zip in the out-dir | rc 2, nothing written (RD-527) | — | S78G |
| p10 | the anonymous-pull probe answering 401 (stubbed) | rc 1 non-draft; WARN with `--draft` | — | drafter (C-58 item 4) |
| p11 | `--draft` at M | rc 0 or 1? — **say what main's build does in draft mode**; a DRAFT- zip at M must NOT equal the shipped entries | — | drafter |

**T — RD-696's cells (B). At `2c221fa` and on the merged tree; every server under the network belt.**

| row | shape | expected at `2c221fa` | at M | predicted-by |
|---|---|---|---|---|
| t1 | the 5 cells, clean | 5/5 green | the file is absent at M; run it against M's product code — 5/5 green (tests only) | builder |
| t2 | M-C5: the two remedy strings swapped in the product | cells 1 and 5 red | — | builder |
| t3 | the delay 250 → 8000 ms | cell 3 red | — | builder |
| t4 | `logger.error` → `console.error` on the failure line | cell 2 red | — | builder |
| t5 | **M-C4: the delay → 0, and a bare `process.exit(1)`** | **5/5 GREEN (L-B1, declared)** — measure; then say what WOULD pin it (e.g. a file transport that flushes asynchronously — a stub that delays its write by > 0 ms — does the line still land?) | — | builder (declared) + drafter |
| t6 | the `chmod 0o500` fixture as ROOT or on a filesystem that ignores mode bits | cell 4 (the fixture control) must go RED, not skip — prove the control can fail (C-40) | — | drafter |
| t7 | EADDRINUSE via an IPv4-only holder (batch #1's C-N1 shape) | what do cells 1-3 see? (the second server may bind `::`) | — | drafter (batch #1 C-N1) |
| t8 | the `afterAll` cleanup: after a run, no locked dir, no socket file, no live child under your tree | none left | — | drafter (H-5, C-174) |
| t9 | the spawn timeout path: a second server that never exits (a mutant that swallows the listen error) | the cell fails within its 60 s race and the child is SIGKILLed — **no orphan** (count it) | — | drafter |
| t10 | the header comment changed after verify | the committed blob is what your verify runs | — | drafter (§1 Target B) |

**K — RD-594's cells and the property they guard (C). At `c7fbf33`, at M (the cell file against M's product — identical server source), and on the
merged tree; every server under the network belt (K2 drives 78 GET routes anonymously — some may try egress: list every route the belt refused).**

| row | shape | expected at `c7fbf33` | at M | predicted-by |
|---|---|---|---|---|
| k1 | the 5 cells, clean, fresh store | 5/5 green | 5/5 green (the property pre-existed, C-178 :1838) | builder |
| k2 | **M1: `healthDetailsForCaller`'s admin check → `return full;`** (anchor count 1) | **K1 AND K2 red**; K2's leak list names exactly `/api/admin/health 200 {identity:true, vaultName:true, vaultHost:true}` | — | builder (Tuesday's ask) |
| k3 | **M-K3: a NEW parameter-free GET route planted in the server source that returns the identity clientId** (a copy; e.g. `app.get('/api/zz-qa-leak', (q, r) => r.json({ id: process.env.KEYVAULT_IDENTITY_CLIENT_ID }))` at column 0) | **K2 red naming `/api/zz-qa-leak`; POP's count 79; K1 green** — the population rule catches a route nobody listed | — | drafter — **the enumeration's own positive control** |
| k4 | M-K3's route written INDENTED, or with double quotes, or split across lines (`app.get(\n'…'`) | **K2 GREEN — the regex `^app\.get\('` misses it** (predicted, READ) — a population blind spot; name each shape | — | drafter (READ the regex) |
| k5 | **K2 control (a) broken**: the server log no longer names the identity (a mutant removes the id from the KV-failure log line) | K2 fails at control (a) — BEFORE the absence check — never a pass | — | builder (control) + drafter |
| k6 | **K2 threshold**: 9 or more of the 78 routes made to hang past 20 s or refuse (a preload that delays them; landing control) | K2 red at `answered >= 70`; **with 8 hung, K2 passes while 8 routes were never read — say what the 10% tolerance can hide, by NAME of the routes that did not answer in the clean run** | — | drafter |
| k7 | the 8 `:param` GET routes and the 12 `app.use('/api…')` router mounts, driven anonymously ONCE by you (params filled with a harmless literal), fresh store | none carries the id/name/host — **L-C2 discharged if clean; a leak is a Blocker against the product** | — | drafter (L-C2) |
| k8 | the Key Vault SUCCESS shape is not reachable locally (C-124): instead, `KEYVAULT_*` UNSET entirely | PRE fails (no KV path attempted) — **show PRE is what stops K1/K2 passing vacuously** | — | drafter (C-40) |
| k9 | K2's population on the MERGED tree and on M0 | 78 (neither A nor B changes the server source); **if M0 moved and touched the server source, the new count and the new routes by name** | — | builder (C-68 note) + drafter |
| k10 | **CTRL-OPEN's mutant**: `adminGateRefuses` made to refuse anonymous callers in the fresh window (a copy) | CTRL-OPEN red (both 401/403); K1 then? (a refused K1 has no body to leak — does K1 go red on `status: 200`?) | — | drafter (C-178 "otherwise unchanged" bar) |
| k11 | `vaultHost` — `/vault\.azure\.net/i` — on a vault name the product would render as a host: does any route return the vault URI in a DIFFERENT form (e.g. `https://…vault.azure.net/keys/…`, url-encoded)? | scan still fires, or name the form it misses | — | drafter |
| k12 | the state: fresh store, `NODE_ENV` as the harness sets it, Entra env blanked | say which `NODE_ENV` the cells ran under; RD-518 r3's gate used `NODE_ENV=production` — **run K1 once under production mode by hand** (a fresh DATA_DIR, the belt) | — | drafter (PRIOR ROUND) |

**D — the deploy/CI trigger (A, B and C — B's and C's `__tests__/` paths are not ignored either). READ ONLY on the workflow files + `gh` READ ONLY. No
workflow is ever dispatched.**

| row | shape | expected | predicted-by |
|---|---|---|---|
| d1 | which workflows a push of the merged tip to `main` starts (on-push filters of every `.github/workflows/*.yml` at the merged tree vs the paths the merge changes) | `build.yml` (push main), **`deploy-demo.yml` (push main, `paths-ignore` `**.md`, `docs/**`, `tests/**` — `__tests__/`, `scripts/`, `*.json`, `.github/` are NOT ignored, so it STARTS)**, **`arm-ttk.yml` (push main, `azure-marketplace/**`)**; `deploy.yml` workflow_dispatch only | drafter (READ `1904765`/`be0fe37`) |
| d2 | what `deploy-demo.yml`'s jobs do when started | `build` runs `az acr build` **only if `vars.CI_DEPLOY_ENABLED == 'true'`**; `deploy` needs `build`, `environment: demo` (required reviewer) and the same variable — **measure whether the variable is set** (`gh variable list` READ ONLY, NexusAI's own `GH_CONFIG_DIR`) **and what the last `deploy-demo` runs on main pushes did** (`gh run list --workflow deploy-demo.yml --branch main --limit 5`, `gh run view <id>` READ ONLY: skipped / success / which jobs ran) | drafter |
| d3 | `deploy-demo.yml` byte-unchanged by A (C-138's condition) | blob `953b2a2` at M and `be0fe37` | drafter (MEASURED) |
| d4 | arm-ttk on the push to main | starts (Kam's Actions-spend decision, C-138); **what it would see — run the SAME check locally (Q-P8) so the CI run is predicted, not discovered** | drafter |

**X — compositions git cannot see (C-68).**

| row | shape | expected | predicted-by |
|---|---|---|---|
| x1 | every copied `__tests__` file that main ALSO has (the 5 `M` files): did main change any of them since `0677388` (the release line's base)? | **none changed on main since `0677388`** (else the copy reverted main's change — a Blocker) — measure with `git log 0677388..1904765 -- <file>` per file and blob compare | READY :14/:26 ("Class C untouched") — builder's claim |
| x2 | if M0 includes batch #4 (RD-418/RD-425/RD-443/RD-698/RD-699): `rd385-shipped-root-markdown-identifiers`, `image-content-exposure`, `rd418-*`, `rd698-*` on M0 + A | green — the rd385 file :4 says README.md, CHANGELOG.md and DEPLOYMENT_GUIDE.md are PULLED from the customer image, and A's other paths are under `scripts/`, `docs/` (opt-in, not re-included), `azure-marketplace/`, `__tests__/`, `.github/` | drafter (READ the rd385 file at `1904765`, `8823458`, `8e27dc2`; `.dockerignore` at `1904765`) |
| x3 | if batch #4 is NOT yet in M0: the same suites on YOUR emulation M0 + A + RD-425 (`8823458b963360ffd212f9b19a0efddea5ba9e66`) + RD-418 (`5a782c10698a6e678ca89957ec661f48daf9c8f8`) in a separate clone (their gate is theirs; this is only the forward composition) | green | drafter — **optional; do it only if cheap, and say which** |
| x4 | if M0 includes batch #3: nothing in A or B touches the erasure/storage/LAW modules; C-68 set = none beyond step 1/2 | — | drafter |
| x5 | RD-696 × A: does A change any file RD-696's cells read or drive (`helpers/rd395-server-harness.js`, the server entry point, the logger)? | no (A has no runtime path) | drafter |
| x6 | RD-594 × RD-696: both boot servers through `helpers/rd395-server-harness`; run both files in ONE jest process on the merged tree (`--runInBand`) | both green; no port collision, no leaked server between them | drafter |
| x7 | RD-594 × the frozen lane-1 heads it names (rd-413 adds a health field; rd-681/682 change a route): NOT members — **say only what K2 would need at their merge** (C-68), no run | — | builder (C-68 note) |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.**

## 3. THE QUESTIONS ALL TARGETS ANSWER FIRST
0. **SESSION_SECRET UNSET, EVERY RUN** — §3a H-1's ONE permitted printer. Positive control once per target: its own cell file with a throwaway random
   64-hex secret exported (never printed, never written) — identical results, or say what differed.
1. **Re-pin everything yourself:** `git ls-remote` at start, mid and end (three timestamped readings, branch name beside each sha, all refs: main, A, B,
   `mkt-release-2.2.0-s81j`, `rd-665-standard-webtest-s83l`, and C's `rd-594-kv-identity-open-window-s86m`); M0 and the "Main may move" rule re-proved;
   chains and exact parents (`git log --format='%H %P'`); deltas (`git diff --name-status`); counts at `1904765`, M0, `be0fe37`, `2c221fa`, `c7fbf33`,
   `3f79e9c`, `e3d9301`.
2. **POSITIVE CONTROL FIRST — re-derive every red and every mutant INDEPENDENTLY** — your own scripts, never the builders' `hold.sh` files (read them for
   method). **Before each mutant arm, prove it still parses — `node --check` on every mutated JS file (and `JSON.parse` on every mutated JSON, `bash -n`
   on every mutated shell script), exit 0, quoted — and that it LANDED (the exact mutated text present, the original absent once the new text is
   removed; `qa-mutate.py <arm> <mid> --verify` with its negative control). A red from a mutant that does not parse, or a green from one that never
   landed, is a VOID arm.** Quote the failing assertion of every red.
3. **Name every behaviour guarded by no cell, and every one guarded only by source text (C-122).**
4. **Full verify of each head and of the merged tree**, `npm run verify -- --maxWorkers=2` (RD-561), through the lock, on a git-indexed tree,
   SESSION_SECRET UNSET. **Predicted: `be0fe37` 4280/254 · `2c221fa` 4138/248 · `c7fbf33` 4138/248 · merged (M0 + A + B + C) counts(M0) + 157 / + 9 =
   4290/256 at M0 = `1904765`**
   (predictions; C-68 says the measurement decides). Every failure by NAME. **"Re-run until green" is not an acceptance gate (charter §4d).**

## 3a. INSTRUMENT RULES — H-1..H-16 (carried from the batch #3 brief, which carried batches #1/#2 and rd579-rd639) and H-17..H-19 (the pkg221 gate's self-corrections)
- **H-1 (rd579-rd639 S-1: a SET/UNSET idiom printed the secret's VALUE).** The ONLY permitted printer, verbatim:
  `if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi`.
  **FORBIDDEN anywhere in your scripts:** `${SESSION_SECRET-…}`, `${SESSION_SECRET:-…}`, `${SESSION_SECRET+$SESSION_SECRET}`, `echo
  $SESSION_SECRET`, `printenv`, `env | grep`, `set | grep`, and **echoing an env array that could hold it (`${envs[*]}`, batch #2 S-5a)**.
  **Self-test it BEFORE the first hold (a control that can fail):** run the printer once with a throwaway exported and once unset, capture both, assert
  the throwaway's value is ABSENT from both (compare in-process; never print it). **After every hold, scan that hold's logs for the throwaway value** and
  report the count (0); **the scan's own positive control plants a DIFFERENT random marker, never the throwaway** (batch #2 S-5b). Print any needle only
  as `<first4>…<last4>`, and **mask GUIDs with or without hyphens** (batch #1 S-2).
- **H-2 (rd579-rd639 S-2).** Never construct a product storage object on a DATA_DIR you are measuring AFTER its server booted. Seed BEFORE; read logs RAW.
- **H-3 (rd579-rd639 S-3).** Every hook you rely on (a preload, a stubbed anonymous-pull probe, a stubbed file transport for t5, a mutated rule) gets a
  **LANDING CONTROL** before the measured run: prove it fired once on a known input. An arm whose instrument failed is VOID, is re-run, and is reported
  as a self-correction.
- **H-4 (rd579-rd639 S-4).** The heartbeat is a SEPARATE child process started by the hold wrapper (`while sleep 60; do echo "HB $(date -u +%FT%TZ) <step>
  <pid> <elapsed>"; done`), killed in the wrapper's `trap … EXIT`; **the wrapper ABORTS the hold if no HB line appears within 90 s of the grant**, and after
  every hold you compute and REPORT the max gap between HB lines (must be ≤ 120 s). (pkg221: a `grep -v` filter BUFFERED the in-script heartbeat — keep
  the HB child's output unfiltered.)
- **H-5 (rd579-rd639 S-5).** Restore your own perturbations (mode bits — t6, the chmod'd dirs — sockets, planted files, held ports) before any hash, and
  hash the restore.
- **H-6 (rd579-rd639 S-6).** Every extractor and census gets a POSITIVE CONTROL. **Every path is quoted** — `!CODING` and `Testing Agent MAIN` contain `!`
  and spaces. **Every server you boot runs under the network belt (`qa-netbelt.sb`) with its landing control (EPERM for TEST-NET-1, 200 for loopback).**
  **The package build is the ONE exception: its anonymous-pull probe must reach `nexusaireleaseacr.azurecr.io` (§12) — run it OUTSIDE the belt, and
  run nothing else in that process.**
- **H-7 (batch #2 S-1).** Mutants are built and verified ONLY by a quoted tool with a negative control (an unmutated tree → VOID rc ≠ 0). A mutant check
  that prints an empty count is a VOID arm, never a pass.
- **H-8 (batch #2 S-2).** The landing rule is "the exact mutated text is present AND the original text is absent once the new text is removed" — never
  "the anchor is absent".
- **H-9 (batch #2 S-3).** Byte-level plants (a policy copy with one hex off, a MANIFEST line, a template digest) are written with `Buffer` and verified by
  `xxd -l 16` BEFORE use; never with `echo`, `printf`, a heredoc or `JSON.stringify` where the bytes matter (re-serialising the template changes every
  byte — edit the ONE value in the raw bytes).
- **H-10 (batch #2 S-4).** Prove every phenomenon reachable before measuring its absence: for t-rows prove the port is really held (a connect succeeds)
  and the directory really refuses a write; for p-rows prove the probe stub really answered (H-3).
- **H-11 (batch #2 S-6).** Every script runs under `/bin/bash` explicitly, and every `<sha>:<path>` is written `"${sha}:${path}"`. **Never `set -- $x` or
  `declare -A` in the default shell.**
- **H-12 (batch #2 §6.6).** Before the C-57 control, list every `__tests__` file any head MODIFIES or DELETES (`git diff --name-status <its base> <head> --
  __tests__`). **Predicted this time: A MODIFIES FIVE (`marketplace-keyvault-durability`, `marketplace-package-build`,
  `marketplace-template-log-analytics-enabled`, `rd461-self-contained-and-template-toolkit`, `rd503-r2-doc-claims-against-product`), and RENAMES ids in at
  least four of them (§9.6) — missing 0 is NOT predicted.**
- **H-13 (batch #1 S-1).** Every tree census is NUL-safe (`ls-tree -z`), with a positive control on a path containing a space.
- **H-14 (batch #1 S-6).** Every driver ends with an explicit END record; a run with no END record is VOID, whatever its exit code.
- **H-15 (batch #1 S-7).** Pass preloads as `-r "<path>"` in argv, never through `NODE_OPTIONS`.
- **H-16 (batch #1 S-5).** A plant is checked to be what the product will treat it as before it is used (here: the socket path is inside the locked dir;
  the held port is the one the second server is given).
- **H-17 (pkg221 self-correction 1: a relative tool path made every arm exit 127 and the build never ran).** Absolute tool paths only; every arm asserts
  the build script actually STARTED (its first MANIFEST/FAILED-MANIFEST line exists) before its rc is read.
- **H-18 (pkg221 self-correction 2; the drafter hit it again today).** zsh consumed `:s`/`:a` in `$var:path` as history modifiers and git read a wrong
  revision; one printed the empty-input hash `e3b0c442…`. `/bin/bash`, braces, and **reject any sha256 equal to `e3b0c442…` as a VOID read**.
- **H-19 (pkg221 self-correction 3).** A gitleaks canary JSON-escaped inside a string does not fire `arm-template-secret-parameter`; plant canaries as
  real keys and read the rule before believing either result.

## 3b. THE NEGATIVE-ASSERTION SWEEP (C-102) — REQUIRED, scoped to what these members change
**Neither member adds an early return to product code (A has no runtime path; B is tests only). The C-102 risk here is in the CHECKS:** A replaces
`scripts/marketplace-package-build.sh` (`803f05b` → `40ec7de`) and re-anchors five existing package cell files (C-151). A negative-asserting package cell
that stays GREEN because the new build script refuses EARLIER (a new precondition, a missing registry field) is invisible to every verify.
1. **Enumerate the build script's new early exits (READ, quote each):** `git diff 1904765 be0fe37 -- scripts/marketplace-package-build.sh`, every new
   `exit`, `return` or `fail` before the manifest's last check.
2. **Enumerate the callers' cells** at `be0fe37`: every cell that spawns the build script or requires `helpers/shipped-plan-build.js` (`git grep -l -E
   'marketplace-package-build|shipped-plan-build'` over `__tests__`, positive control: `marketplace-package-build.test.js` must be found), and classify each
   NEGATIVE (asserts a refusal, an absent zip, a FAIL line, a non-zero exit) or POSITIVE.
3. **For each NEGATIVE cell ask the one question: does it still reach the check it is NAMED for?** Measure it: run it with `bash -x` tracing of the build
   script (or the MANIFEST lines it writes) and show the FAIL line it asserts is written BY the named check, not by an earlier refusal. **A negative cell
   whose red now comes from a different, earlier line is DISARMED** — name it with the line.
4. **Self-test first or ABORT (C-102):** a positive control (a cell you know reaches its named check — e.g. c2b RED on the one-hex-off image: its FAIL
   line is the tag-exception check), a negative control (a cell you know is POSITIVE), and a non-empty population.
5. **Report per ticket:** population, negative cells, still reaching, disarmed. B: population = RD-696's own 5 cells (cell 4 is the negative control's
   control; cell 5's "never running on port" is negative — prove it is reached by the EACCES branch, not by an earlier crash). **C: K1 and K2 are
   NEGATIVE cells ("carries no identity") — the C-102 question is exactly "does each still reach the projection it is named for?": prove with coverage of
   the server source (`--coverage --collectCoverageFrom=<the server entry point>`) that K1's request executes `healthDetailsForCaller`'s non-admin branch
   and `publicKeyVaultState`, and that K2's 78 requests reach their handlers (count the non-null statuses per route; a 401/403/429 from a gate BEFORE the
   handler is a route whose body was never produced — list those by name: they are "answered" for the 90% rule but are not evidence of no leak).**

## 4. TARGET A — C-170 / RD-460 PACKAGE INTO MAIN (TIER 1). Answer each with a measurement.
**Q-P0 — the frame.** The re-pins (§3 Q1); `be0fe37`'s only parent is `1904765`; `3f79e9c` is NOT an ancestor of main (MEASURED: `merge-base(3f79e9c,
1904765) = 0677388`) — **A is a COPY, not a merge (C-58/C-72, C-165/C-170)**: prove no commit of the release line is reachable from `be0fe37` that is
not reachable from `1904765` (`git log 1904765..be0fe37` = one commit).
**Q-P1 — the copy, exactly.** Re-measure §1's copy identity: 32/32 blob-equal to `3f79e9c`, the one deletion, `azure-marketplace/` empty diff
`3f79e9c..be0fe37`, the 29-path residual `be0fe37..3f79e9c` classified into (25 main-only | 3 NOT copied | counts). Compare with the builder's
`pkg-copy-set.txt` (33 entries) and `pkg-diff-inventory.txt` (62 paths).
**Q-P2 — the NOT-copied three (READY :13, "Your call whether any should come anyway").** `bicep/nexusai-customer.bicep`,
`docs/resubmission/2026-09-22_resubmission-handover-for-kam.md`, `docs/SECURITY-AND-COMMERCIAL-READINESS-AUDIT.md`: for each, show `git grep` at
`be0fe37` (positive control on a copied path) that no build step and no test reads it — **the builder's first scoping error was exactly a name-grep that
missed a repo-WALKING guard (READY :24); so also run every repo-walking guard at `be0fe37` with each file swapped for its `3f79e9c` blob and show nothing
changes.** Recommend, with an evidence class; the decision is Tuesday's.
**Q-P3 — no Class-C revert.** For each of the 32 copied paths, `git log --format=%h 0677388..1904765 -- <p>`: every path main touched since the base must
be one whose `3f79e9c` blob ALREADY carries main's change. **Predicted: only `azure-marketplace/combined/mainTemplate.json` (the RD-665 port, C-162)** —
prove structurally (parse both; `1904765`'s webtest resource == `3f79e9c`'s webtest resource) that `93ecbca` carries RD-665 exactly as `eed2dac` does, and
that every other difference `eed2dac` → `93ecbca` is a release-line change named in `pkg-prior-work.txt`. Any other path main touched = Blocker (x1).
**Q-P4 — the build reproduces the shipped package (p1-p4).** POSITIVE CONTROL FIRST: the build at `3f79e9c` in your own extract (p4). Then at `be0fe37`
(p1). **Binding comparison PER ENTRY:** every entry of your be0fe37 zips, of the builder's be0fe37 zips, and of the SHIPPED 2.2.1 zips — the three
plan JSON files and the seven listing PNGs — byte-identical, entry-name sets identical (reuse `qa-q2q5.py` by copy). Both manifests end `MANIFEST
COMPLETE: 32 checks, 0 failed`; `diff` yours vs the shipped one and explain every differing line (p3). **C-165's acceptance line, measured:** every
MANIFEST sha256 entry equals the shipped MANIFEST's; the zipped webtest `Kind` is `standard`; **no ACR credential field** (`acrUsername`,
`acrPassword`, `acrLoginServer`) anywhere in the zipped createUiDefinition or template (a scoped JSON walk, with a control: the same walk on
`1904765`'s files FINDS them — C-165 :1692 cites `mainTemplate.json:31,35,540-543`).
**Q-P5 — the CONTROL build from main fails, and for the stated reason (p1 at M).** Your own build at `1904765`: rc 1, `FAILED-MANIFEST-2.2.1_1904765.txt`,
no zip. Quote the FAIL lines and show they are the registry/wizard-output checks the READY names (C-38/C-45), not an unrelated failure — **a control that
fails for the wrong reason is not a control (C-40).**
**Q-P6 — the version exception and digest arms (p5-p10).** POSITIVE CONTROL FIRST: the package suites clean at `be0fe37` (by name: `marketplace-*`,
`rd461-*`, `rd471-*`, `rd472-*`, `rd503-*`, `rd630-*`, `dev-scripts-template-parameters*`, `listing-folds-*`, `rd665-*`). Then V1/V2/V3/BW on COPIES, through
the REAL build script with a stub anonymous-pull probe answering 200 where the registry must not decide (H-3 landing control), and V2J/BW through the named
suites: **c2b-green must redden by name** (pkg221 V2J 235/236, BW exactly c2b-green).
**Q-P7 — the re-anchored cells carry C-151-shape proofs (C-170 :1744).** For each of the five MODIFIED cell files, list every cell whose assertion changed
`1904765` → `be0fe37` (`git diff`), and for each: (a) the old refusal is kept by putting the OLD value back into a COPY of the real files (C-151) — show
the cell that does it; (b) run that copy arm: it must redden the old-value cell by name. **Predicted re-anchors (READ, `git diff` on the five files):**
`marketplace-package-build` +337/−108 (renamed POSITIVE CONTROL, renamed `--draft` cell, c1/c2/c2b, RD-527 block), `rd461` +22/−12 (the "registry step
held for RD-460" exemption removed — C-131: the removal wins), `rd503-r2` +25/−6 (the existing-vault PRECONDITION re-anchored — C-131's own case),
`marketplace-keyvault-durability` +125/−0 (a NEW RD-505 block, additions only), `marketplace-template-log-analytics-enabled` +3/−2. Each re-anchor names
its release-line commit in `pkg-prior-work.txt` — check it.
**Q-P8 — arm-ttk LOCALLY (discharges L-P1; predicts d4).** `bash /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s78g/armttk.sh
/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files <be0fe37> b5b` (`TMPDIR` inside your project first); quote `TOTAL N/M PASS`
(pkg221: 49/49 at `3f79e9c`). Both controls, `hideconf` and `hardloc`, must fire — **a 49/49 without a control that fired is not reportable.** ALSO run
the COPIED `scripts/arm-ttk-check.sh` (the file CI runs) on your extract, IF it can run with the locally pinned pwsh/arm-ttk under
`session-tools/pwsh-v7.6.6.*` and `arm-ttk-20260213.*` WITHOUT downloading anything — else NOT RUN, named. **arm-ttk IN CI is UNMEASURED unless a PR
exists (§10).**
**Q-P9 — no secrets in what A adds to main.** gitleaks (`dir` mode, `--redact`) over copies of A's 34 delta files at `be0fe37`, once with the repo's
`.gitleaks.toml` and once with the default rules. **POSITIVE CONTROL FIRST:** a canary each ruleset TARGETS (H-19) planted in a copy must fire in the same
run. Report the version.
**Q-P10 — what reaches the IMAGE (C-72).** With `.dockerignore` and `Dockerfile` at M0 (and at M0 + A), list which of A's 34 paths the image build
context would carry and which the Dockerfile COPYs (READ + the image-manifest helper `__tests__/helpers/image-manifest.js` if present at M0, run
pure-node, no docker). **Predicted: none of A's paths ships** (README.md/DEPLOYMENT_GUIDE.md are pulled — rd385 :4; `docs/*` is opt-in and none of A's
docs is re-included; `scripts/` — say). If any ships, it is a C-72 finding for the NEXT image, not a defect of the package.
**Q-P11 — prior work (C-49).** `pkg-prior-work.txt` names a release-line commit for every copied path — check 32/32; the 2.2.0 and 2.2.1 gate reports
cover the release-line content (cite, do not re-run); C-131's RD-625 case is exactly the rd503-r2 re-anchor.

## 5. TARGET B — RD-696 (TIER 2). Answer each with a measurement.
1. **Scope:** `git diff --name-status 1904765 2c221fa` = the two files; no product file (`git diff --quiet 1904765 2c221fa -- backend static` rc 0).
2. **POSITIVE CONTROL FIRST:** the cell file against `1904765`'s product code — 5/5 green (tests only), then against `2c221fa` — 5/5; **H-10: prove the
   port is held and the dir refuses a write before reading any cell's green.**
3. **Mutants — re-derive the READY's three independently, then the drafter's:** **M-C5** (remedy strings swapped) → cells 1, 5 red; **M-D8000** (delay
   250 → 8000) → cell 3 red; **M-LOG** (`logger.error` → `console.error` on the failure line) → cell 2 red; **M-C4** (delay → 0; and a bare
   `process.exit(1)`) → **5/5 green, L-B1 — carried, not a finding**; **M-B1** (the EACCES branch given the in-use remedy) → cell 5 only?; **M-B2**
   (the failure line logged AFTER `process.exit` is scheduled with a 0 ms delay AND the file transport made async — a stub that writes after 5 ms; H-3
   landing control) → does cell 2 go red? **If yes, say what that means for M-C4 (a cell design that COULD pin the delay — describe it as a
   fix-shape, do not write it)**; **M-B3** ("running on port" logged before listen succeeds) → cell 5 red?; **M-B4** (the chmod fixture made
   0o700) → cell 4 red (the fixture control can fail, C-40), and cell 5 then sees what?
4. **Every row t1-t10 of §2a.** t5, t6 and t9 first.
5. **Leak census after every RD-696 run (C-174: never kill by pattern):** no child of your jest left, no port held, no `nexusai-rd696-*` temp dir left
   with mode 0o500, measured by YOUR floor counter anchored on your claude pid (a leaked server is a Minor; a leak you cleaned by pattern is a rule
   break).
6. **C-68 set for B** (the §1 table, step 2) on `2c221fa` and the merged tree.
7. **PRIOR WORK (C-49):** the batch #1 gate's c1-c9 rows and M-C4/M-C5 (report §6.3-§6.4): is RD-696 exactly C-F1's recommended cell set (report §16
   item 4)? Say what of C-F1 is now closed, by measurement, and what is still open.

## 6. TARGET C — RD-594 subset (C-178), guard cells only (TIER 2). Answer each with a measurement.
1. **Scope:** `git diff --name-status 1904765 c7fbf33` = the two files; no product file (`git diff --quiet 1904765 c7fbf33 -- backend static` rc 0).
   **C-178's DELIVERED note (:1838) says what the READY :19 claims** (drafter VERIFIED the text; re-read it) — quote it in the report.
2. **POSITIVE CONTROL FIRST — the property pre-exists, so the red proof is by MUTATION:** the cell file against `1904765`'s product — 5/5 green; at
   `c7fbf33` — 5/5 green. **Then M1 (Tuesday's ask; row k2): `healthDetailsForCaller`'s admin check replaced by `return full;` — anchor count 1, `node
   --check` rc 0, landed (H-8) — K1 AND K2 must redden, and K2's leak list must name exactly `/api/admin/health 200 {identity:true, vaultName:true,
   vaultHost:true}` (quote it).** Restore by sha and hash the restore (H-5).
3. **K2's population and its two positive controls (Tuesday's ask):** reproduce the enumeration independently (your own script over the server source at
   the head AND on the merged tree — **78** predicted, the drafter's python reproduction); show control (a) FIRES (`scan(h.output)` true for identity and
   vault name — and break it, row k5, to show K2 then fails at (a) rather than passing); show control (b) (`/api/admin/health` found and 200); count the
   routes that answered (≥ 70 of 78 required) and list by name every route that did NOT, and every route whose status came from a gate before its handler
   (§3b item 5). **Then M-K3 (row k3): a planted leaking route must redden K2 by name — the proof that "enumerate, don't list" works.** Then k4's shapes.
4. **The population rule and C-68 (Tuesday's ask):** K2 enumerates at run time, so its verdict holds only for the server source it enumerated. **Run K2 on
   the MERGED tree (step 3 of the MERGE ORDER) and state the population there;** name, for the merge author, the rule the READY :32 states (K2 re-runs on
   the merged population after rd-413, rd-681, rd-682 and any other lane-1 merge that touches the server source), and say whether a MERGED mail that
   omits that re-run would be a C-68 gap.
5. **Mutants beyond M1 (drafter's):** **M-K3** (row k3); **M-K5** (control (a) broken, row k5); **M-K6** (8 vs 9 routes hung, row k6); **M-K10**
   (`adminGateRefuses` closes the fresh window, row k10 — CTRL-OPEN red); **M-K11** (`publicKeyVaultState`'s allow-list admits `detail`) → K1 red, K2 red?
6. **Every row k1-k12 of §2a** — k2, k3, k6 and k7 first.
7. **C-68 set for C** (the MERGE ORDER table, step 3) on `c7fbf33` and the merged tree.
8. **PRIOR WORK (C-49):** the RD-518 round-3 gate report (PRIOR ROUND): was the fresh-store state undriven there (READY :24's claim)? Is K1 new coverage
   or a duplicate of an rd518-r3 cell? `healthDetailsForCaller`, `publicKeyVaultState`, `rd518-r3-health-detail-decision.test.js` and
   `adminGateRefuses`'s two permissive branches byte-unchanged (READY :28-29) — blob-compare them `1904765` vs `c7fbf33` vs the merged tree.
9. **Merge-trees vs the other lane-1 heads (READY :31, RELAYED):** re-measure C × A and C × B (members) in your scratch object dir; for the NON-members
   it names (rd-413, rd-695, rd-681, rd-682, rd-627b, rd-705) re-measure ONLY if their heads are at origin and in the object store (`ls-remote`,
   `cat-file -t`; never fetch) — report each as counts-only / other / not measurable. **Never gate a non-member head.**

## 7. THE DEPLOY / CI TRIGGER CHECK (rows d1-d4) — REQUIRED because A changes `.github/`
1. **READ** every `.github/workflows/*.yml` at the merged tree: its `on:` filters, and which of them a push of the merged tip to `main` would start given
   the paths the merge changes. Tabulate: workflow, starts (yes/no), which jobs could run, and under what condition.
2. **`deploy-demo.yml` (the one that can deploy):** quote its `on.push` (`branches: [main]`, `paths-ignore: '**.md', 'docs/**', 'tests/**'`) and its two
   job `if:` conditions (`vars.CI_DEPLOY_ENABLED == 'true'` on `build`, which runs `az acr build`; the same plus `needs.build` and `environment: demo` on
   `deploy`, which runs `az containerapp update`). **Predicted: the merge push STARTS the workflow; whether anything builds or deploys depends ONLY on the
   variable and the reviewer gate.** Measure with `gh` READ ONLY (NexusAI's own `GH_CONFIG_DIR`): `gh variable list`; `gh run list --workflow
   deploy-demo.yml --branch main --limit 5` and `gh run view` of the run for the `1904765` push — were `build` and `deploy` SKIPPED? **If
   `CI_DEPLOY_ENABLED` is `true`, that is a finding for Tuesday before ANY merge (every merge to main would `az acr build`), not a defect of A.** If `gh`
   cannot read it, say so: **UNMEASURED**, and the merge author must read it before pushing.
3. **`arm-ttk.yml`** starts on the merge push (`azure-marketplace/**` changes). Its result is predicted by Q-P8; **C-138 is Kam's Actions-spend decision.**
4. **`build.yml`** starts (push main): C-142's merge-green includes its failing set equalling the known set — the merge author's check after the push;
   **your job is to predict it: run the verify on the merged tree (§9) and name any cell that is known to behave differently on Linux.**
5. **Nothing is dispatched, re-run or approved by you.** `gh` never merges, approves, comments, reviews, labels, re-runs, dispatches, sets a variable or
   opens a PR.

## 9. THE MERGED TREE (C-68, C-57, C-89, C-104, C-112, C-133). No verdict is complete without it.
1. **Build it in YOUR OWN scratch clone** under `projects/nexusai/qa-trees/batch5b.*/clone-1`: `git clone --shared --no-checkout <repo> <dir>`; in the clone
   only: remove `origin`, set a local `user.name`/`user.email`, `gc.auto 0`, `core.fsmonitor false`; `git checkout -b gate <M0>`; then `git merge --no-ff`
   in the PROPOSED ORDER: **`be0fe37`**, **`2c221fa`**, **`c7fbf33`**. **Write your prediction for each merge BEFORE it** (the MERGE ORDER table);
   **anything other than the counts file conflicting STOPS (C-57).** Re-measure A × B, A × C and B × C by `merge-tree` in a scratch object dir first (Q1).
   **C-104: resolve and stage before any census or run.**
2. **Resolve the counts file by REGENERATION, never by hand:** take a side (a placeholder) to complete each merge commit, then `npm run verify --
   --maxWorkers=2 --update-counts` ONCE on the tree after ALL merges, through the lock, SESSION_SECRET UNSET; commit the regenerated file in the clone.
   **Predicted 4290/256 at M0 = `1904765`.** Then a plain verify of the committed head; suites ≥ the largest parent's (C-57 step 4).
3. **The fleet's merge of A is a FAST-FORWARD-able one at M0 = `1904765`.** Say whether a `--no-ff` merge and a fast-forward give the same TREE (they must),
   and whether the merge author's C-89 then has anything to regenerate (predicted: nothing, if A merges first at `1904765`).
4. **Order independence (a control that can fail):** clone-2 in REVERSE (`c7fbf33`, `2c221fa`, then `be0fe37`). **The two `HEAD^{tree}` must be
   identical apart from the counts file** — quote both tree ids and the `git diff --name-only`.
5. **Blob identities and C-112's condition, stated beside the conclusion:** every A path at the merged tree == its `be0fe37` blob == its `3f79e9c` blob;
   `__tests__/rd696-listen-failure-remedies.test.js` == `2c221fa`'s; `__tests__/rd594-kv-identity-open-window.test.js` == `c7fbf33`'s; the server source
   `bc099b2` (every parent); `package-lock.json` `9064763`. **`__tests__`: 299 files predicted (M 289 + A 8 + B 1 + C 1; the drafter's `ls-tree -r`
   counts: 289 at `1904765`, 297 at `be0fe37`), every one byte-identical to at least one parent, 0 identical to none, 0 absent (NUL-safe, H-13).**
6. **id-superset control (C-57) — MISSING IDS ARE PREDICTED, NOT 0.** merged test ids ⊇ ids(M0) ∪ ids(`be0fe37`) ∪ ids(`2c221fa`) ∪ ids(`c7fbf33`)?
   **Predicted: NO** — A
   RENAMES cells main has (drafter READ, `git diff` on the five modified files: `marketplace-package-build` "POSITIVE CONTROL: the manifest records WHERE
   the image and login server were resolved from…" → "…WHERE the image came from…"; the `--draft` cell "registry and pull problems…" → "release-registry and
   pull problems…"; `rd461`'s `describe` "RD-461: wizard text needs nobody at Datasec (outside the registry step held for RD-460)" → "RD-461 / RD-460:
   wizard text needs nobody at Datasec, with no step exempt" — **a describe rename changes the id of EVERY cell inside it** — plus its two cells;
   `rd503-r2` "PRECONDITION — … skips the role assignments on the existing-vault path" → "PRECONDITION — … offers no existing-vault path, and always
   assigns both Key Vault roles"). Use batch #1's adapted COPY `qa-c57-id-superset.sh` (reads the jest JSON of YOUR OWN verifies; keeps the lock-holder
   refusal; proven first to STOP on a planted missing id), four parents (B and C add ids only — predicted to contribute 0 missing). **List every missing
   id, and for each: its file, the new id that replaces it, and
   whether C-133's mechanical test holds on blobs (C-150): merged blob == `be0fe37`'s AND only `be0fe37` changed the file since the merge base
   `1904765`.** C-133 says it does NOT cover "short-lived branches (plain C-57 applies unchanged)"; its ADDENDUM accounts an AUTHORISED RENAME "when the
   old->new id pair is named and the new id is present and green". **Whether C-170's "Re-anchored tests carry C-131/C-151-shape proofs" is the
   authorisation is Tuesday's ruling (TUESDAY'S RULINGS AT STAMP); you REPORT the full old->new table, the C-133 blob test per file, and any id that
   has NO new counterpart (a pure loss — a Major, unless a C-131 removal names it).**
7. **The semantic overlaps git cannot see (C-68), on the merged tree, one hold:** every C-68 set of the MERGE ORDER table BY NAME (per-file counts); rows
   p1/p2 re-run FROM THE MERGED TREE (the package built from the merged tip must still reproduce the shipped 10 entries — this is the claim main
   inherits); rows t1-t5 on the merged tree; rows k1-k3 and k9 on the merged tree (K2's population THERE); x1-x7; then the full verify (Q2). Then ONE
   mutant per ticket on the merged tree: **M-PKG** (the `"2.2.1"` image one hex off — c2b-green red), **M-C5** (rd696 cells 1, 5 red) and **M1** (rd594
   K1 and K2 red) — each must still hold through the other changes.
8. **C-89 on your clone:** `git diff --quiet HEAD` holds; `git show HEAD:scripts/verify-expected-counts.json` equals the regenerated counts.
9. **Nothing leaves your clone.** No push, no remote, no ref written in NexusAI. **Count `<repo>/.git/objects` files before and after your whole session
   and account for any delta by mtime** (live seats commit there). Drafter's reading: `count-objects -v` `count: 436` at 09:3x AEST.

## 10. CI (C-142) — NOT RUN AT ANY BRANCH HEAD unless a PR exists
- **Unverified by the drafter** (no `gh` run). Check with `gh pr list --head <branch> --state all` (READ ONLY, NexusAI's own `GH_CONFIG_DIR`) for all
  three branches; M0's CI Build with `gh run list --commit <M0>` READ ONLY, labelled. **arm-ttk in CI: UNMEASURED unless a PR exists** — say so in the verdict.
  **`gh` never merges, approves, comments, reviews, labels, re-runs, dispatches or opens a PR.**

## 11. Floor discipline — THE FOUR CLAUSES, plus THE DEADLINE RULE
1. **Every jest run, every server you boot (RD-696's cells boot servers) goes through `session-tools/nexusai-lock.sh`, tagged `qa-b5b-…`** (e.g.
   `qa-b5b-H1-arms`, `qa-b5b-H2-pkg-suites`, `qa-b5b-H3-heads-verify`, `qa-b5b-H4-merged`) — C-141: gate-class; under ADDENDUM 2/3 every NEW `qa-*` ticket
   earns a fresh, self-applied yield from the builders. **When a MERGE ticket (gate-class, C-141 ADDENDUM) is already queued when you file, file yours with
   `--after <that merge ticket's tag>` (ADDENDUM 4's tool) so you sit directly behind it; never ahead of it.** **QUEUE, NEVER TAKE OVER:** never kill,
   signal, move or edit another seat's process, lock directory, owner file or ticket, even if it looks stuck; if a holder looks stuck, mail a QUESTION
   (§13) and keep waiting. **The package BUILDS (no jest, no server), the zip compares, arm-ttk and gitleaks may run outside the lock — say which did.**
2. **Hold the lock ONCE per multi-run measurement.** Every hold is a TRACKED CHILD of your seat, never detached (`nohup … &`).
3. **Count foreign servers the RD-606 / C-125 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND the server entry point anywhere in the
   remaining argv; "ours" = the ancestor chain CONTAINS your own claude pid. **Record the foreign count BESIDE EVERY RESULT (C-110 clause 3).**
   **NEGATIVE controls, all in the same run, all must classify FOREIGN — read at drafting 2026-09-27 09:29:23 AEST from `tmux list-panes -a -F
   '#{pane_id} #{@cockpit_name} #{pane_pid}'` + `pgrep -P` + `ps`:** NexusAI-M claude **`62649`** (pane `%19`), NexusAI-N claude **`9959`** (pane `%21`),
   NexusAI-P claude **`20317`** (pane `%22`), NexusAI-O claude **`38362`** (pane `%29`, re-read 2026-09-28 07:51), and Tuesday's claude **`59108`** (pane `%0`, parent bash `56603`, re-read 2026-09-28 07:51 after the s90 rotation; **Tuesday rotated since batch #3's
   `47349`**). Also live then: QA/NexusAI-batch3 `36118` (`%23`), QA/NexusAI-batch4 `40285` (`%24`), QA/Vision-gate9 `16516` (`%25`) — usable as extra
   negatives while they live. **Datasec/Vision_Sales_Portal (`67576`, `%20`) is GONE (Vision retired).** Re-read them at start; if one has exited, say so
   and use the others; **a hold with NO live negative control aborts.** Reuse batch #1's instrument BY COPY with YOUR pid as `ROOT` and these as `NEG`:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch1/evidence/qa-floorlib.sh`
   (**its defaults are STALE — correct `ROOT` and `NEG` before any hold**) and `…/qa-floorcount.py`; the original counter is gate 7's
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`.
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, "no entry differs" (p2: the one-hex-off copy is its
   control), gitleaks' zero (the canary), "no disarmed cell" (§3b), "no ACR field" (Q-P4: the same walk on main's files finds them), "no leak" (t8/t9).

**5. THE DEADLINE RULE — every real-server probe and every network request has a per-step DEADLINE, a HEARTBEAT, and kills its server in a `finally`.**
Every HTTP request carries a client timeout; each step (boot 60 s, request 30 s, registry call 30 s, package build 300 s, arm-ttk 600 s, exit 20 s) has a
written DEADLINE; a step past it is ABORTED and reported, never waited on. **Log a HEARTBEAT line at least every 2 minutes during any hold (H-4: a
separate child, ≤ 120 s max gap, aborted if absent at 90 s); a step with no heartbeat for 5 minutes is aborted and reported,** and a hold that is not
progressing releases the lock. Every server you start is killed in a `finally` (SIGTERM, then SIGKILL after a grace) **by pid from your own ancestry,
never by pattern (C-174)**, and the reap is confirmed by your floor counter.

## 12. HELD
- **LOCAL RUN, NOT THE DEMO:** every server request goes to a server YOU booted on 127.0.0.1 from YOUR tree, under the network belt (H-6).
- **External hosts you MAY contact, and nothing else:** `nexusaireleaseacr.azurecr.io` (the build script's own anonymous-pull probe, and your own
  anonymous token + manifest GET by digest — the sha256 of the manifest bytes must equal
  `fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66`; negative control in the same window: the manifest GET with no token = 401);
  `git ls-remote origin` (pins); `api.github.com` via `gh` READ ONLY (§7, §10). **No demo request, no customer-test tenant, no Partner Center, no Microsoft
  docs fetch.**
- **TIER 1 AT FULL WEIGHT — FINDINGS-ONLY:** no fix, no merge (outside your own clone), **no push, never push — not to main, not to ANY author's branch**, no deploy, no
  registry write, **nothing to Partner Center, the demo or production**, no money, no external comms, no mail to any human. **No `az` at all.** No docker
  (Q-P10 is pure-node). **Your package builds are evidence in your own directory, never a publishable package (C-173: any rebuild or publish is Kam's).**
- **Never write into** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.1` or the builder's
  `session-tools/s84m/pkg-build-*` — copy before unzipping; hash at start and end.
- **Symlinks, chmod, sockets, held ports and scratch git repos live ONLY under your own mktemp dirs.**
- **Findings-only:** do not commit (outside your clone), move any branch, file a ticket, or write anything inside the NexusAI project (`2_Project_Files`,
  `session-tools/`, `worktrees/`, `1_Project_Definition/`, `qa-reports/`). **NEVER `rm`** — quarantine, per the template §5.

## 13. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch5b/report.md` — ONE report covering every
member; evidence in `./evidence/` beside it.

**Questions:** your routing name is **`QA/NexusAI-batch5b`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by) and **PROCEED ON THE SAFEST READING without waiting**;
Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning `[Tuesday -> QA/NexusAI-batch5b] ANSWER`. Approval-class items (anything
touching the demo, the registry beyond the anonymous reads above, Azure, Partner Center, money, or a human) are NOT RUN and named. Record every question,
reading and answer.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 5b: C-170 package (RD-460) · RD-696 · RD-594`
Lead the body with ONE line per ticket in this form — `C-170/RD-460: <GO|GO WITH FINDINGS|NO GO> @ be0fe37` · `RD-696: … @ 2c221fa` · `RD-594: … @
c7fbf33` — then one line naming M0, the merge order you recommend, the merged counts you measured, K2's population on the merged tree, and **whether the merge push would start
`deploy-demo.yml` and whether its build/deploy jobs would run (§7)**. Never `wednesday-agent@`. AgentMail key: `AGENTMAIL_API_KEY` in
`/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute: the QA project has none). Never put the key, a token or any secret in a mail or the
report.

Verdict format:
- **C-170 / RD-460** naming `be0fe3704023d8f092da0be27f79b82fbc029085`: the frame and the copy (Q-P0-Q-P3); the package reproduced per entry vs the SHIPPED
  2.2.1 zips, the MANIFEST diff, C-165's acceptance line (Q-P4); the control at main and its reason (Q-P5); V1-V3/BW (Q-P6); the re-anchor proofs (Q-P7);
  arm-ttk locally with both controls (Q-P8); gitleaks with its canary (Q-P9); the image question (Q-P10); prior work (Q-P11); **the `.github` facts of §0
  (a)-(d)**.
- **RD-696** naming `2c221fa2ed01a837b5390502619689e5527fc951`: the positive control, the three relayed mutants re-derived, M-C4 (L-B1) measured and
  carried, M-B1..M-B4, rows t1-t10, the leak census.
- **RD-594** naming `c7fbf338e9ffeb64790208b2391c6c1b81b419fa`: the positive control at `1904765` and the head; **M1 reddening K1 and K2 with K2's
  exact leak line quoted**; K2's population (78 at the head AND on the merged tree) and both its controls fired; M-K3 (a planted route caught by name),
  M-K5, M-K6, M-K10, M-K11; rows k1-k12 (k7: the param/router routes driven, L-C2); the RD-518 r3 prior work; the merge-trees vs the lane-1 heads it names.
- **The merged tree (§9):** M0; both orders; counts regenerated once (measured vs 4290/256); the id-superset table with every missing id and its C-133
  test; C-112's condition; the C-68 sets by name; one mutant per ticket; C-89; the object-count accounting; **your recommended merge order.**
- **The deploy/CI trigger (§7):** the workflow table, the `CI_DEPLOY_ENABLED` reading (or UNMEASURED), the last `deploy-demo` runs on main.
- **The §3b sweep:** per ticket, population / negative cells / still reaching / disarmed.
- Each of **L-P1..L-P4, L-B1, L-B2 and L-C1..L-C3** answered: discharged with a measurement, or left standing and named (C-112).
- All refs as **three timestamped readings (start / mid / end)**, each with its branch name.
- **§3a H-1..H-19:** for each, that it was followed, with the self-test outputs (H-1), landing controls (H-3, H-10), max HB gap per hold (H-4), byte checks
  (H-9).
- Every action recommendation carries its evidence class: **MEASURED AT RUNTIME / PROBED / READ ONLY**. Severity is yours; priority is Tuesday's.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, arm-ttk in GitHub Actions, any deploy, what-if or validation against real Azure, Partner Center, Azure Container Apps, a real Key Vault success path, production mode, and Windows.

## WRONG OR UNVERIFIED IN THE COMMISSION AND THE READYS — carried so the gate inherits the corrections
1. **"Kam's 2026-09-26 07:18 ruling (a) 'package files into main' recorded as C-170" (the commission) — WRONG at source.** The 07:18:54 AEST ruling,
   option **(a)** "Yes, bring only the package files into main", is **C-165** (:1688-1689). **C-170** (:1740-1741) is a LATER ruling, option **(b)**
   "Package plus what main needs to build and check it", card `nexusai-package-files-scope`, **2026-09-26 21:05:47 AEST**, and it SUPERSEDES C-165's
   "NOT release-policy or test re-anchors" line. **The drafter's reading (§0) is that C-138 + C-170 (not C-165) are what could cover the workflow copy;
   C-165 alone (option a, "only the package files") would NOT.** C-138 (:1458-1462) SAYS what the commission claims (Kam approved arm-ttk in CI from one
   new workflow; Tuesday's conditions include "does not merge without that gate and a Tuesday GO"). **Neither C-138 nor C-170 names the act of COPYING
   `.github/workflows/arm-ttk.yml` onto main in words;** C-142 (:1503) records "Kam owns .github changes" and asks such a change be "mailed before pushing".
   Coverage = Tuesday's ruling at stamp.
2. **"re-affirmed 2026-09-27 ~08:2x"** (the merge grant) — the drafter found no re-affirmation in `0_Brain/daily_tuesday/2026-09-27.md` or
   `0_Brain/dashboard/data/chat_tuesday.json` (grep "merge once tested" / "work your way"; positive control: the 2026-09-25 :84 original found). The
   2026-09-25 22:04 grant itself is verified. **UNVERIFIED, RELAYED.**
3. **"C-170 … copies 32 paths … incl. .github/workflows/arm-ttk.yml"** — correct (MEASURED 32/32 blob-equal to `3f79e9c`), but note the delta is **34
   files**: 32 copies + the DELETION of `scripts/build-plan-packages.sh` + the counts file. The READY's "32 checks" (MANIFEST) and "32 paths" (copies) are
   DIFFERENT 32s — coincidence; do not read one as proof of the other.
4. **The gate's id-superset control will NOT show "missing 0"** — A renames at least five cell titles and one `describe` in files main has (§9.6). Plain
   C-57 STOPS on a missing id; C-133 excludes short-lived branches; its ADDENDUM accounts an authorised rename. **Whether C-170's re-anchor clause
   authorises these renames is Tuesday's ruling — the merge author (S86M) will hit this at merge time too.**
5. **`deploy-demo.yml` WILL be started by the merge push** (READ: `on.push.branches [main]`, `paths-ignore` covers only `**.md`, `docs/**`, `tests/**`
   — `__tests__/` is not `tests/`). Whether it builds/deploys depends on `vars.CI_DEPLOY_ENABLED` and the `demo` environment reviewer — **UNVERIFIED by the
   drafter (no `gh`)**; §7 measures it. This is true of EVERY merge to main that touches non-md paths, not only A. **`arm-ttk.yml` will also start** (a
   NEW Actions workflow on main — C-138's spend decision).
6. **"arm-ttk in CI is UNMEASURED unless a PR exists" (commission)** — correct; the author ran NO arm-ttk locally either (READY :29). The gate runs it
   locally (Q-P8); the CI result stays UNMEASURED.
7. **RD-696 READY: "Verify … 4138/4138 … After verify, a header comment changed"** — the committed blob is not the verified blob (tests-only, comment-only
   by the author's account — C-76, a claim). Row t10.
8. **RD-696 READY has no "NOT TESTED" section;** its "NOT closed: M-C4 itself…" paragraph is carried verbatim as the declared limit (L-B1). Linux/CI and a
   non-Mac file transport (L-B2) are the drafter's additions.
9. **RD-594 had no READY and no branch at origin at 09:27:41 AEST;** at 09:41:43 its branch was at `c7fbf33` (= Tuesday's message) and the READY on
   disk. The commit (09:37:33 +1000) and the CLARIFICATIONS DELIVERED note (file mtime 09:37; the note names `c7fbf33`) were written together. VERIFIED.
10. **Merge-trees (A×B, A×C, B×C) NOT measured by the drafter** (hard rule); predicted counts-only from `comm -12`; C's author RELAYS counts-only against
    eight lane-1 heads (READY :31). The launcher's guard 80 measures the three member pairs.
11. **The pkg221 gate's CI note** — the release-line CI for `3f79e9c`/`e3d9301` was "NOT RUN (no PR)"; nothing here changes that.
12. **Lane 1's RD-705** (`rd-705-no-store-authenticated-pages-s86m` @ `e164d1a`, READY on disk `2026-09-27_nexusai-rd705-READY-mail.txt`) is a lane-1
    PRODUCT change and is NOT in this batch — the drafter assumes it is batch 5a's; Tuesday confirms.
13. **Tuesday's claude pid changed** (`47349` in batch #3/#4 → `23230` now); **Vision_Sales_Portal's `67576` is gone.** §11 carries the 09:29 set.
14. **RD-594's TIER: Tuesday's message says "Tier 2 (tests only; guards a tier-1 security property)"; Kam's card text quoted in C-178 (:1831) says
    "RD-594 subset, lane 1, tier 1 gate", and the build bullet (:1832) says "tier 1".** Tuesday's acceptance of the guard-cells shape (:1838) does not
    say it changes the tier. **The brief uses TIER 2 as commissioned and requires the k-rows at full depth; Tuesday rules the label at stamp.**
15. **C-178's DELIVERED note says it supersedes "this entry's 'with a red cell at main'"** — the entry's build bullet (:1832) actually reads "There is a
    red cell at main". Same meaning; the quoted phrase is not verbatim. Cosmetic.
16. **RD-594 READY :15 "a source scan of backend/server.js for every `app.get('/api/...')` literal with no `:param` or `*`, giving 78 routes"** — VERIFIED
    (python reproduction of the cell's own regex, 78 at `1904765`/`c7fbf33`/`be0fe37`). **The regex is column-0, single-quote, one-line only** (READ): 0
    routes in today's source escape it, but a future route written otherwise would be INVISIBLE to K2 (row k4). **86** GET `/api` literals exist in all
    (8 with params) plus **12 router mounts** — L-C2 is sizeable, not marginal.
17. **RD-594 READY :32's C-68 note is the author's rule, not yet a recorded one:** "K2 re-runs on the merged population" after rd-413/rd-681/rd-682 merge
    is in the READY and the cell header, not in CLARIFICATIONS (drafter `grep -n -i 'merged population'` on CLARIFICATIONS → 0; control `C-68` found).
    The merge author will need it at each of those merges; Tuesday decides whether it becomes a C-number.

## PROVENANCE (drafter, 2026-09-27 09:25–10:05 AEST, read-only)
- origin heads: main `1904765…`, `rd-460-pkg-into-main-s84m` `be0fe37…`, `rd-696-listen-remedy-cells-s84m` `2c221fa…`, `rd-705-…-s86m` `e164d1a…`; no
  `rd-594*` | `git ls-remote origin <refs>` | 09:27:41 — RE-READ with `rd-594-kv-identity-open-window-s86m` `c7fbf33…`, main/A/B unchanged | 09:41:43
- RD-594: READY read whole (41 lines, 3842 bytes); chain, parent, delta (2 files +147/−3), counts 4138/248, lock blob, server-source blob `bc099b2` at
  `1904765`/`c7fbf33`; A∩C = B∩C = counts; the cell file whole (144 lines); the route population 78 / 86 / 8 / 12 by python over the server source at
  three shas; C-178 :1830-1838 incl. the DELIVERED note; `session-tools/s86m/{rd594-hold.log, rd594-hold.sh, mt-objects-rd594/}` present; the RD-518 r3
  report's head lines | `cat`, `git log|diff|show|rev-parse`, `comm -12`, python (READ), `sed -n`, `ls` | 09:41-09:50
- every pinned sha a commit | `git cat-file -t` | 09:27
- chains, parents, dates, messages; merge-bases; name-status; shortstats | `git log --format='%H %P %ci %an %s' 1904765..<head>`, `git merge-base`,
  `git diff --name-status|--shortstat` | 09:28 (a zsh `:s` modifier slip on the first counts read, re-run under `/bin/bash`)
- counts at `1904765`, `be0fe37`, `2c221fa`, `3f79e9c`, `e3d9301`; `package-lock.json` blob `9064763` at the first three | `git show "${s}:…"`,
  `git rev-parse` | 09:28
- copy identity 32/32, the deletion, `azure-marketplace/` empty diff, 29/62 residuals, template/wizard/policy/build-script blobs at five shas;
  `merge-base(3f79e9c,1904765)=0677388`; `d14a975` not an ancestor of main | `git rev-parse`, `git diff --name-only`, `git merge-base [--is-ancestor]` |
  09:29-09:36
- `.github/workflows/*` listing at `1904765`/`be0fe37`; `arm-ttk.yml`, `deploy-demo.yml`, `deploy.yml`, `build.yml` `on:`/job `if:` lines; `deploy-demo.yml`
  blob `953b2a2` at both | `git ls-tree`, `git show` | 09:30
- `rd630-armttk-ci-workflow.test.js :14` reads the workflow; `arm-ttk.yml`'s release-line commit `1e217fc`; `be0fe37`'s commit message | `git show`,
  `git log -- <file>` | 09:34
- the five modified cell files' renamed `test`/`describe` lines | `git diff 1904765 be0fe37 -- <file>` (named files only) | 09:36
- `__tests__` file counts 289 / 297 | `git ls-tree -r --name-only` | 09:38
- RD-696 cell file (header, harness, env, cells) | `git show 2c221fa:__tests__/rd696-listen-failure-remedies.test.js` | 09:33
- rd385 file :4 at `1904765`, `8823458`, `8e27dc2`; `.dockerignore` at `1904765` | `git show` (named files only) | 09:37
- batch #4 heads and expected files | `launch_qa_nexusai_gate_batch4.sh` (READ) + `git ls-remote` | 09:36
- CLARIFICATIONS: size 313,569, mtime 09:09; C-02 :30 … C-179 :1839; C-138 :1458-1462; C-165 :1688-1698; C-170 :1740-1745; C-142 :1503 (".github");
  C-133 :1426 + ADDENDUM; C-141 ADDENDA :1488-1494; C-173 :1765; C-178 :1830; RD-696 0 hits (control C-141: 10) | `grep -n`, `sed -n` on that one file |
  09:31-09:35
- the three READYs read whole; the pkg221 brief and report (verdict, Q0-Q11, floor, self-corrections, NOT TESTED); the batch #1 report's RD-533 section
  and C-F1; the batch #3 brief and launcher (the pattern) whole; BRIEF_TEMPLATE | `cat`, `sed -n`, `grep -n` | 09:20-09:32
- the SHIPPED 2.2.1 zips and manifest sha256 (= C-160 / pkg221); the builder's be0fe37 zips and manifest; per-entry sha256 of all four zips (3 + 7 entries
  equal) | `shasum -a 256`; python `zipfile` in memory, nothing written | 09:35
- builder evidence present: `session-tools/s84m/{pkg-copy-set.txt (33), pkg-diff-inventory.txt, pkg-prior-work.txt, pkg-verify.log, pkg-verify2.log,
  pkg-build-final-be0fe37/, pkg-build-control-main-1904765/, rd696-hold.log, rd696-hold.sh}`; `session-tools/{nexusai-lock.sh, c57-id-superset.sh,
  s78g/armttk.sh}`; the pkg221 and batch #1 instruments | `ls` | 09:30-09:32
- the merge grant: `0_Brain/daily_tuesday/2026-09-25.md:84` found; no 2026-09-27 re-affirmation found | `grep -n -i`, python over `chat_tuesday.json` |
  09:33
- seats: `%19` 62649 (M), `%21` 9959 (N), `%22` 20317 (P), `%0` → bash 22288 → claude 23230 (Tuesday), `%23` 36118, `%24` 40285, `%25` 16516; no `%20` |
  `tmux list-panes -a -F …`, `pgrep -P`, `ps` | 09:29:23
- NexusAI `count-objects -v` `count: 436` | 09:38
- routing: **no `QA/NexusAI-batch5b` line in `fleet/inbox_routing.conf`** (batch3 :122, batch4 :123 exist) — Tuesday adds it; the launcher's guard 40
  refuses until then | `grep -n -i batch` | 09:30

## FILL AT STAMP — Tuesday, before launch (the launcher refuses until the starred items are done)
- ★ both STAMP placeholders (the SELF-CHECK line and the Self-check note) — LAST, by hand, no placeholder token in the note.
- ★ the routing line `QA/NexusAI-batch5b|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf`.
- TUESDAY'S RULINGS AT STAMP: the `.github` coverage (WRONG 1), the renamed-id treatment (WRONG 4), RD-594's tier (WRONG 14), the seats.
- If RD-594's head MOVES before launch: the launcher's guard 18 refuses — re-pin `C_HEAD` in the launcher and every `c7fbf33` in this brief, re-read the
  READY, never `sed` a sha blindly.
- The negative-control seats in §11 and the launcher's `NEG_SEATS` if any pid has exited.
