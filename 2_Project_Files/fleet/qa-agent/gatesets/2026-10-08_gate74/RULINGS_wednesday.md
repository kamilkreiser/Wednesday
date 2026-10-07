# gate74 — RULINGS for Wednesday (drafted 2026-10-08 ~03:29–04:40 AEDT, NOT launched)

## CARRIED (from the commission and the standing rulings; binding on the gate, written into the prompt)

- **R1 TIER.** #1423 is T2: a through-code read plus the PR's own suites, re-run by the gate in its own pinned worktrees.
  - **The PREFLIGHT WEIGHT is added.** The push ran NO preflight: `.githooks/pre-push` (KS-380) selects the preflight only for `^Blockchain/Dev/`.
  - So the gate runs the preflight's legs by hand, as the hook would, at the head, the base and the SIM squash tree, after S-1.
  - It runs the package's suites through `npm run test:unit` (`vitest.unit.config.ts`), never a bare `vitest run`.
- **R2 ACTIONS.** The three classes, the SUBSET predicate (never equality), and the gate73 wording are carried. The comparator for classes (2) and (3) is **Q-SCHEMA74**, below.
- **R3 PRE-EXISTING MISMATCH.** The three files are base-state (gate73 R3). c1 P13 confirms they are byte-identical at base, head and develop.
- **R4 PLATFORM SUITES.** The four platform suites are UNMEASURED (the local stack is down) and are never counted as passing.
- **R5 MERGE SEAT.** Per gate73 Q-SEAT, the merge seat is the next R seat, `kit.json merge_seat = Secuura/Blockchain-R`, ordinal `Seat R 15th`. It is never the author (Seat R 13th); the launcher refuses the author by name.
- **R6 CONTROLS.** Every control must be able to fail. A zero gets a positive control. Before and after are read by one parser.
- **R7 LEG 14 (KS-1450).** `--no-verify` is forbidden. A landing that needs a merge-in push is a STOP: re-draft, and wait for KS-1450. It is never a bypass.

## OPEN QUESTIONS (each has the drafter's recommendation under it)

**Q-SCHEMA74 — BLOCKS LAUNCH. Which comparator judges Actions classes (2) and (3)?**
- **Status in the kit:** `kit.json actions_comparator` is `null`.
  - The launcher refuses rc 8 "RULING NEEDED".
  - A real repin refuses rc 8. A dry run reports it instead (measured: `dry1.out`, launcher rc 8 → repin rc 13).
- **Drafter's measurement** (`gh_gate74.py actions`, 2026-10-07 ~16:35Z and again at 17:0xZ). At #1423's head, `pr` fails {Akto suite (PR), Performance suite (k6 smoke), Playwright suite, Schemathesis suite}:
  - **Against develop eae08a3f:** develop fails the first three. Schemathesis PASSES on develop, so the subset FAILS by Schemathesis alone (rc 1).
  - **Against base b280b74f:** the base fails all four, so the subset HOLDS (rc 0).
  - **Union of the two:** HOLDS (rc 0).
- **Schemathesis flips with no Schemathesis path in any diff:**
  - #1422, on the SAME base, PASSES it.
  - At gate73, #1407 and #1408 passed it, while #1409, #1410 and develop 147ae442 failed it.
  - #1423 touches no Schemathesis, gateway or spec path (c1 P14; P10 asserts head == base on the schemathesis baseline).
- ***Rec:* `base`.** #1423's tree is its base plus 3 paths, and none of them reaches the Schemathesis job. The PR's own base is therefore the like-for-like comparator for a head that sits behind develop.
  - The tool still prints the verdict against all three comparators, and the gate NAMES the develop-only difference without claiming a cause.
  - If you prefer the stricter reading, rule `develop`. The gate then reports class (3) as not holding, and you rule whether the Schemathesis flip blocks.
  - **After ruling:** write the value into kit.json (it is not a pinned file) and re-run the repin. The repin re-renders `{{COMPARATOR}}` into the prompt and head file.

**Q-SEAT74 — confirm the ordinal.**
- `merge_seat_ordinal` is `Seat R 15th`. The GO string the prompt renders is `GO (Seat R 15th): merge 1423 on gate74`.
- *Rec:* confirm. If R 15th is not the seat that boots, change `merge_seat_ordinal` and re-run the repin. It re-renders the GO string, and the launcher checks it.

**Q-SUBJ — the squash subject for #1423.**
- The PR title is 80 chars, `test: … (KS 1164)`. The R-lane builder asserts `SUBJECT.startswith("KS-1164:")`, at `build_addendumra12_gate73.py`, the `assert SUBJECT.startswith(OWN_KEY + ":")` line. So the title cannot be the squash subject.
- *Rec:* declare `KS-1164: assert the k6 status-code breakdown prints locale-grouped counts`.
  - It is 73 chars, ASCII and carries no `(#`.
  - It is true of the diff: the PR adds a test and fixes nothing.
  - It is the subject the drafter's `mergera1 --dry` used (rc 0).
- The gate re-declares it, and its wording wins.

**Q-BUILDER74 — the seat's builder cannot express either landing. The tool wins; this needs your spec.**

`build_addendumra12_gate73.py` (sha256/16 `ab0ec003b23c30b2`, R 14th's copy) has two shapes:
- **`NO_MERGE_IN=1`:** PARENTS == [GO develop], HEAD == gated head, tree == T'.
- **`NO_MERGE_IN=0`:** a merge-in M with parents [gated head, develop].

#1423 fits neither:
- Its parent is b280b74f, and develop is eae08a3f. With D = develop, `PARENTS == [D]` fails. With D = base, m7's and mergera1's develop checks STOP.
- tree(head) is END_TREE `39c96de3`, but the squash tree is `a6227cb3`.
- The squash lands MERGED doc blobs, but the builder hardcodes `merged_blob_paths: []`.

#1422 also fails it:
- It touches no doc. `one(flow …)` / `one(cheat …)` and `targets[FLOW]` raise.
- It has three own keys, but `RA12_OWN_KEY` must be a single `KS-n` and `keys == {OWN_KEY}`.
- Its subject cannot start with one key.

**mergera1.py itself handles both, unchanged (sha256/16 `aaf230e7d1975213`, MEASURED).** A scratch copy was run with `--repo <drafter clone> --dry` on hand-written addenda:
- **#1423:** rc 0. The two docs were declared `merged_blob_paths`, with their targets set to the MERGED blobs `3f8f3c0c…` / `e4c8ee75…`. Predicted tree `a6227cb3` == the addendum's.
- **#1422:** rc 0 once the PR body carries Refs lines (see Q-1422-REFS).
- Evidence: `drafter_evidence_2026-10-08/mergera1_dry*/`.

*Rec:* R 15th writes a NEW COPY, `build_addendumra15_gate74.py`, and never edits the predecessor's. It keeps every inherited assert and adds three REQUIRED knobs, none with a default:
- **`RA15_LANDING=behind`:** parse `- PR base B: <40hex>` and `- END_TREE: <40hex>`, then:
  - assert PARENTS(head) == [B];
  - assert HEAD == the gated head;
  - assert tree(HEAD) == END_TREE;
  - count paths as diff(B, HEAD) == `RA15_EXPECT_PATHS`;
  - the addendum's `merged_tree` = the GO's T'. mergera1 then predicts it over the develop it reads, and asserts it while develop == D.
- **`RA15_DOCS=merged|none`:**
  - `merged`: the GO's `flow`/`cheat` lines are the MERGED blobs. Declare both docs in `merged_blob_paths`, and assert each head blob != the merged blob (otherwise the overlap is false).
  - `none`: assert the GO has 0 `flow`/`cheat` lines and the PR touches neither doc.
- **`RA15_OWN_KEYS`:** a sorted comma list. The key-set assert becomes `keys == set(RA15_OWN_KEYS)`, and the subject must open with the keys in that order, followed by `: `.

Further changes to the copy:
- Re-key the GO-clause literal to a required `RA15_GO_CLAUSE`. Its exact value is the GO subject: `GO (Seat R 15th): merge 1423 on gate74` / `GO (Seat R 15th): merge 1422 on tier3`.
- Add `"Seat R 12th"` to the predecessor tuple. R 12th merged #1410, so its claim sits in develop's history.
- Prove it with arms, each of which must REFUSE:
  - a wrong B;
  - a wrong END_TREE;
  - docs declared `merged` on #1422;
  - head blob == merged blob;
  - a key-set mismatch;
  - a GO clause naming R 14th.
- Then run the builder → `mergera1.py --dry` chain on both PRs before any squash.

**Q-1422-REFS — mergera1 STOPs on #1422.**
- Measured: `STOP: the PR body carries no Refs KS-#### line`. The live body has 0 `Refs` lines. Its keys appear only in three Linear URLs.
- **(a)** R 15th PATCHes #1422's PR body (a GitHub write, on our own lane's PR) and adds `Refs KS-998` / `Refs KS-1435` / `Refs KS-591` after the "None of them closes here" line.
  - The DRAFT is `merge_inputs/1422.pr_body_with_refs.DRAFT.txt` (4,375 B, sha256 `0a7b4775…`).
  - Then R 15th reads the body back by sha256 and uses it VERBATIM as the squash body.
  - Simulated: mergera1 with that body is rc 0, own_keys == Refs == MG-3 set {KS-1435, KS-591, KS-998}.
- **(b)** Rule an exception in the tool. *Rec:* **(a)**, authorised by name in the tier-3 GO. Never loosen the instrument.

**Q-1422-SUBJ — the squash subject for #1422.**
- *Rec:* `KS-998, KS-1435, KS-591: add the 5d WHY comments to the three gate73 lines` (74 chars, ASCII, no `(#`, true: comment-only).
- It hyphenates the three OWN keys, so the squash attaches to all three tickets. That is intended (the comments are theirs), it has no closing word, and no ticket state moves.
- KS-1435 stays In Progress (live sweep owed, gate73 Q-SWEEP).
- The alternative is the 81-char PR title with de-hyphenated keys. It fails the subject-opens-with-keys assert, so it would need its own ruling.

**Q-ORDER74 — which lands first?**
- The final develop tree is ORDER-INDEPENDENT (merge-tree, drafter clone): `d6ee60d91e2f…` either way.
  - #1422 onto develop is `2c8b0984…`. #1423 onto develop is `a6227cb3…`. Either onto the other gives `d6ee60d9…`.
- #1422 needs no gate.
- *Rec:* **#1422 FIRST**, on your tier-3 GO, while the gate runs. Then #1423 after the gate's GO, onto the develop that holds #1422.
  - The gate's SIM legs stay valid by the "what moved" discriminator: #1422 is 9 comment lines in 3 files, and `c4 merged` / `mergera1 --dry` re-predict on the real develop anyway.
  - If the gate has not launched when #1422 lands, the repin refuses rc 10 and prints `--repin-develop` (and c4 re-predicts).
- The default order in the brief is 1422 → 1423. Reverse it by ruling.

**Q-UNKEYED — develop's cheat heading `Observability images + native k6 guard — KS-1445 (with KS-1367)`.**
- The heading does not END in its key, so the pinned cheat reader (composee5:82) cannot key it. 19 `<h2` openings vs 18 keyed at develop.
- It is BASE-STATE: it is present byte-identically in develop and the SIM squash (c4 M5).
- *Rec:* polish, not this PR's. It is a residue for the KS-1445 author: an h2 should end `— KS-n`.

**Q-ENGINES (polish, §6e).** `systemTest/performance/package.json` declares `engines.node >=24.11.0`. The author and the drafter both ran node v24.7.0, and npm warned without refusing. *Rec:* the gate names what it ran on; this is not a blocker.

**Q-LOCALE (polish).** The RED cell can only tell `1,234` from `1234` under a locale that groups thousands. CONTROL F-3c asserts that the runner's locale does group. *Rec:* fine as built. The gate names its locale.

**Q-OTHER-SITES (polish).** report.ts has three more `toLocaleString()` sites (:133, :135, :140). No cell pins them. *Rec:* a named gap; a follow-up cell if wanted.

**Q-BRIEF-WORDING (no ruling; a correction).**
- The commission described #1423 as carrying "the writeGateReport overwrite fix". MEASURED: it is test-only. report.ts is blob `ac59af37cbc6` at base, head and develop, and the writeGateReport fix landed earlier as `f3bf8698d628` (#1271), which is an ancestor of the base (c1 P14).
- The commission also named #1422's TS file as `api-gateway index.ts`. It is `Blockchain/Dev/services/transfer/src/index.ts`.

**Q-PREFLIGHT-BUDGET.** The gate runs the full preflight 3× (head, base, SIM): about 6 min each, plus about 1.6 GB of installs per worktree. *Rec:* accept. If the budget runs short, keep head + SIM; the base run is the comparator, and the head's run alone is already green, 71/0 of 71.

## WEDNESDAY'S RULINGS — 2026-10-08 04:31 AEDT
- **Q-SCHEMA74 = base.** #1423 is test-only (3 paths; c1 P14 none reach Schemathesis; P10 baseline head == base); develop passes Schemathesis only after Peter's later baseline triage (#1424/#1425). Written into kit.json. The gate still prints all three verdicts and names the develop-only flip without claiming a cause.
- **Q-SEAT74 = Seat R 15th** (`Secuura/Blockchain-R`). Confirmed.
- **Q-SUBJ / Q-1422-SUBJ:** as recommended (73 and 74 chars, no `(#n)` suffix).
- **Q-ORDER74:** #1422 first (tier 3, no gate), then #1423 on the gate's GO.
- **Q-1422-REFS:** yes. R 15th adds the three `Refs` lines to #1422's PR body on Wednesday's word (an edit to OUR PR's body; foreign keys per STANDING_LINES :278 where they would attach).
- **Q-BUILDER74:** R 15th writes a new builder copy to the drafter's spec, red-proofed (genuine record + tampered body, and one arm per legitimate landing shape: API-only squash with no merge-in, multi-key body, no docs) BEFORE any GO is parsed. The tool wins over this ruling.
- **Q-UNKEYED, Q-ENGINES, Q-LOCALE, Q-OTHER-SITES:** named gaps, as recommended; the gate reports them, it does not fix them.
- **Q-PREFLIGHT-BUDGET:** accepted.
- Standing: a merge-in is NEVER pushed while develop is red on leg 14 (KS-1450); if either landing turns out to need one, STOP and mail. Never `--no-verify`.
