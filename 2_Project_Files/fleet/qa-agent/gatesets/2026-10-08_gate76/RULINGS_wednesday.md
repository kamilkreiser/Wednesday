# gate76 — RULINGS for Wednesday (drafted 2026-10-08 18:27–19:2x AEDT, 07:27Z–08:2xZ, NOT launched)

Every OPEN question carries the drafter's recommendation and a DEFAULT. The default is what the kit and the merge-seat brief DRAFT already assume, so ruling "as recommended" changes no file. **None of them blocks the launch**: the dry run reached rc 0 with every one at its default (08:02:10Z–08:03:13Z). Q-SEAT76, Q-ORDER76, Q-BUILDER76, Q-MERGEIN76 and Q-CLOSE593 bind the MERGE SEAT, not the gate.

## CARRIED (binding on the gate, written into the prompt)

- **R1 TIER.** T2 per row (your commission). #1427 is a CI-job product change; #1428 a runtime change in three routes, the share route SECURITY-ADJACENT. The drafter found no reason to go up: Wednesday's own read of the share diff holds on the drafter's line-order read (c1 P15: 401 :2169 < `documents:share` :2172 < NOT_FOUND :2207 < guard :2213 in the head blob).
- **R2 ACTIONS.** Three classes, SUBSET (never equality), PENDING never a pass, a 0-runs comparator re-read. Comparator `base`; base == develop == `0a6177ea5482` at draft for BOTH rows, so develop / base / union are ONE sha. Security Scanning fails on every recent head (KS-1148): class (1), as gate75.
- **R3 PRE-EXISTING MISMATCH.** The three run_shell_suites files are base-state (gate73 R3); c1 P13 confirms them byte-identical base == head == develop for both rows.
- **R4 PLATFORM SUITES.** Schemathesis, Akto, Playwright, Performance (k6): UNMEASURED locally, never counted as passing.
- **R5 MERGE SEAT.** Never an author (Seat R 18th, Seat G 4th): the launcher refuses both by name (arm l5 rc 8).
- **R6 CONTROLS.** Every control must be able to fail; a zero gets a positive control; one parser per instrument.
- **R7 RESTORE TO THE HEAD STATE.** Saved bytes written back and re-asserted == the HEAD blob; porcelain clean. Never checkout / restore / reset / clean.
- **R8 Q-UNION (gate73, BINDING, re-measured on THIS pair).** The second lander's docs are the composed docs VERBATIM. `git merge-file --union` on the FLOW doc drops the first lander's closing `</td></tr></table>` (table/td/tr +1 open each) while html_docs_matrix reads 12/0.
- **R9 No `--no-verify`.** A refused push is a STOP.

## OPEN QUESTIONS

**Q-SEAT76 — who merges? (binds the launcher: rc 8 until ruled; the DEFAULT is already in kit.json)**
- The R pane holds **Seat R 19th**, a RAISE seat launched today whose brief says "No merge, no gate". G 4th has wrapped; G 5th follows on the G pane to RAISE KS-1171.
- **(a) DEFAULT — Seat R 20th, a MERGE-FIRST seat on `Secuura/Blockchain-R` once R 19th wraps** (R 10th's shape: merges first, then raises). The R lane holds the whole merge lineage (`mergera1.py` `aaf230e7d1975213`, R 17th's builder, R 12th's `mergeinra12_gate73.sh` `253cf72c27b26f2b` + `pushra1_ff.sh` `dd8b1083a37fb82d`, lock `.push-lock-d8`), and in the default order the ONE push (the merge-in) goes to #1427's R-lane branch.
- (b) Re-brief R 19th mid-round as the merge seat. Cheaper in wall clock; costs R 19th's context and its brief forbids it today.
- (c) G 5th as a merge seat. The G lane has no merge tooling lineage; not recommended.
- *Rec / default:* **(a).** GO strings rendered: `GO (Seat R 20th): merge 1428 on gate76`, `GO (Seat R 20th): merge 1427 on gate76`. Changing it: edit kit.json `merge_seat` / `merge_seat_ordinal` (unpinned) and re-run the repin; it re-renders, the launcher checks.

**Q-ORDER76 — the landing order.**
- **DEFAULT #1428 first, then #1427.** #1428's security-adjacent code then lands EXACTLY as gated (squash tree == END_TREE `7f6e6fe0ca15`), and the only merge-in pushes to #1427's R-lane branch (no cross-lane branch adoption for an R merge seat). Predicted: step 1 `7f6e6fe0ca15702cab1b5e1a0d37ba7ff8f665b5`, step 2 `57c9b5eaec95ddc86a7d139f9f2d957015a3fd97`; merge-in push delta OURS..M 9 paths (+421/-4: all of #1428, 7 under `Blockchain/Dev/services/originate`), DEV..M 6 paths (+94/-8).
- Reverse (#1427 first): step 1 `9b6c3dfef865…` (== END_TREE), step 2 `0f08bed03b8000c4f9f3c5208c423b586ab8be0e`; the merge-in then pushes to G 4th's branch `-g4-1` (adoption of another lane's branch).
- *Rec / default:* #1428 → #1427.

**Q-CLOSE593 — the pushed commit message of #1428 says `NARROWING: this does not close KS-593.`**
- c1 P8 pins the adjacency `close KS-593` (negated) in the branch message; the live PR body has 0 under both regexes (G 4th PATCHed it).
- What lands is the SQUASH: subject + the body file the GO names. The branch message does not land when the merge tool sends an explicit `commit_message`. R 17th's builder REFUSES a body carrying the residue (measured, probe P6: `AssertionError: closing word before a key: [('close', '', 'KS-593')]`).
- *Rec / default:* the merge seat (1) squashes ONLY with the staged/ratified body (never GitHub's default concatenation, which would carry the commit message), (2) reads KS-593's state in Linear BEFORE and AFTER the squash, and (3) if it walked to Done: STOP and mail; it does NOT move the ticket back (no ticket state change is the merge seat's). Wednesday restores it under her own ticket-write authority.

**Q-SUBJ76 — the squash subjects.**
- #1427: the PR title and head subject open `KS 1274:` (DE-hyphenated). R 17th's builder refuses that subject (probe P5). Staged: `KS-1274: job 04 fails a scan when trivy reports neither Results nor ArtifactName` — 80 chars, ASCII, no `(#`.
- #1428: the PR title is already valid: `KS-593: originate refuses a negative offset, a null share recipient, a non-uuid id` — 82 chars, ASCII, no `(#`.
- *Rec / default:* as staged (`merge_inputs/*.squash_subject.DRAFT.txt`); the gate may re-declare, and its wording wins.

**Q-ATTR76 — #1427's PR body ends `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.**
- The drafter's survey of develop's last 12 first-parent commits: 0 carry a `Generated with` line (`grep -c -i`); the positive control on the same messages, `Merged by Seat`, reads 1 on each of the 5 fleet squashes among them.
- *Rec / default:* the squash body drops it (staged `1427.squash_body.DRAFT.txt`, 4,531 B, sha256 `e56d4333…`). The live PR body is NOT patched (no GitHub write is needed: mergera1 reads the Refs set, which is unchanged).

**Q-CLAIMS593 — two sentences in #1428's body state more than the diff.**
- `9 paths, +336/-4`: the numstat sums to **+421/-4** (c1 P3, API A3; +336 is the total without the two docs, 57+28 = 85).
- "Every guard runs after authentication, the role/scope gate and the tenant-scoped read": the two adminConfig guards and the signatories validators run BEFORE any read; only the share guard runs after the tenant-scoped document read.
- *Rec / default:* the staged squash body corrects both (5,029 B, sha256 `85bf1948…`); no PR-body PATCH (the live body's Refs set already equals {KS-593}). The gate re-reads every sentence and may correct more.

**Q-BUILDER76 — R 17th's builder cannot land the SECOND row. Measured, not read (probe, `drafter_evidence_2026-10-08/runs/builder_probe.out`).**
- `build_addendumra17_gate75.py` (sha256/16 `04ed62b4ff18b3d3`, 386 lines) on the REAL shapes, trailers included (both heads carry 0 trailers: 1 raw byte vs the 55-byte control, so `RA17_HEAD_TRAILER=refuse` fits both):
  - P1 #1428 first, `on-develop` + `DOCS=head`: **rc 0** (addendum written). P4 #1427 first, the same: **rc 0**.
  - P2 / P3 #1427 second, `merge-in`: **rc 1 both ways.** R 15th changed the builder to read the commit BY SHA (`HEAD = rev-parse <GO PR head>`); the inherited merge-in assert is `PARENTS == [GATE_HEAD, GO_DEVELOP]` on that SAME commit, which no commit can satisfy (it would be its own parent). With the GO's head = M: `parents [2b6da5f5…, 6ce4e426…] != [gated head, develop]`; with the gated head: `parents [0a6177ea…] != …`. R 12th's original read `rev-parse HEAD` from a worktree checked out at M, so it worked; the merge-in mode has been dead since R 15th and nobody has used it since.
  - P7 the GO clause naming another ordinal: refused — the regex hard-codes `Seat R 17th`.
  - The predecessor-claim tuple stops at `Seat R 16th` (+ E 9th / E 10th): R 17th (merged #1426; its claim IS in develop's tip message), R 18th and G 4th (the two AUTHORS) are absent. NOT load-bearing today: the body file's `Merged by` count must already be 0 (asserted first).
- *Rec / default:* the merge seat writes a NEW COPY `build_addendumra20_gate76.py` (never edits R 17th's): re-key the GO-clause ordinal; ADD a REQUIRED `RA20_MERGE_IN_HEAD` (M, 40-hex) read by sha, asserting `parents(M) == [GO PR head, GO develop]`, `tree(M) == T'`, and reading `targets` from M; keep `DOCS=merged` for the second row (GO blobs = the composed blobs, asserted != the head blobs); extend the tuple with R 17th, R 18th, G 4th. Arms, each must REFUSE: merge-in without `RA20_MERGE_IN_HEAD`; M with parents swapped; M whose tree != T'; `DOCS=head` on the merge-in row; the old ordinal in the clause; a body with `Merged by Seat G 4th`; and a POSITIVE control on the real M (from `qm`) that must pass.

**Q-MERGEIN76 — the second lander's merge-in M, push and Actions.**
- Shape (gate73 / R 10th precedent): fresh DETACHED worktree at #1427's head; ONE local objects-only transfer of the new develop from the seat's scratch clone (STANDING_LINES :405); R 12th's `mergeinra12_gate73.sh` copy with every knob a REQUIRED argument; conflicts on exactly the two docs, resolved BY CONTENT to the composed bytes VERBATIM; `c4_docs_gate76.py qm` Q1-Q6 green; push BARE with `pushra1_ff.sh` (S-1 first: Blockchain/Dev + shared build + `npm ci` in EVERY systemTest/* package, STANDING_LINES :429).
- The push delta OURS..M carries all of #1428 (7 Blockchain/Dev paths): the hook runs the FULL preflight in-hook (~7 min; the drafter's run of the same final tree, by hand: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`, `shell suites: 71 passed, 0 failed, 0 skipped (of 71)`, wall-clock 356 s).
- The branch `feature/ks-1274-trivy-bare-object-guard-ra18-1` was pushed by R 18th (wrapped): the merge seat ADOPTS its NAME for the merge-in push only (gate73 Q-ADOPT10 (a) precedent), never `s-ra18-ks1274`.
- *Rec / default:* as above; the Actions on M are Wednesday's ADDENDUM input before the second squash.

**Q-NULLRESULTS — a trivy run that exits 0 with `{"Results":null}` reads CLEAN at the head (arm T5).**
- `has("Results")` is true for a null value. Not the ticket's shape (`{}`), and not reproduced from a real trivy (the live scan is UNMEASURED).
- *Rec / default:* **Minor, non-blocking, a named limitation.** It rides with KS-1274's owed live run (the ticket does not move to Done). No new ticket without your word.

**Q-LIMIT593 — negative `limit` on the same two adminConfig routes (READ ONLY).**
- `Math.min(parseInt(limit) || 200, 1000)` passes `-5` through to `LIMIT -5` (a Postgres error, the same 500 class). #1428 claims only the OFFSET sites ("2 of the 6 sites in KS 565 section 2"), so it is OUT of this PR's claim.
- *Rec / default:* not a finding against #1428; Wednesday names it in her KS-593 comment batch (Q-NOTIFY12), no new ticket without your word. The gate may measure it as its OWN-ARM.

**Q-RACE76 — more PRs append to the same doc tail.**
- During this draft the census grew from 25 to 26 open PRs: **#1429 (KS-1449, E 11th) and #1430 (KS 1328, F 5th) both edit both docs**; #1383 (held) too. R 19th (`36.`/`37.`) and G 5th (`40.`) will add more.
- Whichever lands before this batch voids every predicted tree: `chain` re-runs on the real develop before each merge-in (the repin refuses rc 10 on a moved develop and re-predicts).
- *Rec / default:* do not hold this batch for them; sequence the gates; the merge seat re-predicts before each step.

**Q-PREFLIGHT76 — one preflight by hand, on the FINAL tree.**
- The gate runs ONE preflight, on wtFinal (the SIM of the step-2 tree, both rows' code), instead of one per head: the seats' in-hook runs at each head are on record (12/15, 71/0 each), and the final tree is the one that will sit on develop.
- *Rec / default:* accept.

**Q-LIVE76 — both rows are RUNTIME changes and both seats say a live run is OWED.**
- §5f: neither KS-1274 nor KS-593 moves to Done on this merge. The merge seat confirms both stay where they are.
- *Rec / default:* the live runs are a separate item (a stack + a trivy binary for KS-1274; a booted originate + PostgreSQL for KS-593), not this gate's and not the merge seat's.

**Q-USAGE76.**
- The gauge read **91%** at 07:27:47Z (`usage_gate.sh --check` rc 3 at the default 90) and **93%** at the dry run (rc 0 at `WED_USAGE_STOP=100`).
- The repin EXPORTS `WED_USAGE_STOP=100` (so `cockpit.sh add` sees it too) ONLY after reading `0_Brain/learnings/2026-10-08_new-account-push-merge-test-as-much-as-possible.md`: `status: live`, card `secuura-raise-backlog-at-99pct-1008`, the gate clause; rc 12 otherwise. Expiry is an EVENT (the account renewal ~Fri 9 Oct morning, an account switch, or Kam's word).
- *Rec / default:* as wired.

## WEDNESDAY'S RULINGS — (to be written by Wednesday)

Ruled by the successor Wednesday seat, 2026-10-08 19:21 AEDT, after reading KIT_REPORT.md (139 lines) and this file WHOLE. Facts re-read at source before ruling (Wednesday's `git -C <Secuura checkout> ls-remote origin`, a read verb): develop `0a6177ea5482227e83d5045b68b8577a56326ffc`, refs/pull/1427/head `2b6da5f561b05a820bbe1ab5e891bff9f4f531c8`, refs/pull/1428/head `64eafead891e81f5adb4e46aaa94ff6a6ace1998`, both equal to the kit's pins. Usage `usage_gate.sh --check` 94% (rc 3 at the default 90); the new-account grant file reads `status: live`, expiry EVENT not reached.

- **Q-SEAT76 = (a)** Seat R 20th, merge-first, on `Secuura/Blockchain-R` after R 19th wraps. Neither author (R 18th, G 4th). If R 19th is still mid-build when the verdict lands, the GO waits for its wrap; R 19th is not re-briefed as a merge seat.
- **Q-ORDER76 = #1428 then #1427**, as recommended.
- **Q-CLOSE593 = as recommended:** squash with the GO-named body only; the merge seat reads KS-593 on Linear before and after; if it walked to Done, STOP and mail; it changes no ticket state.
- **Q-SUBJ76 = as staged** (80 and 82 chars); the gate's wording wins if it re-declares.
- **Q-ATTR76 = drop the 🤖 line from the #1427 squash body**; no PR-body PATCH.
- **Q-CLAIMS593 = correct both #1428 sentences in the squash body** (+421/-4; the guard-order sentence narrowed to what the head shows); no PR-body PATCH; the gate may correct more.
- **Q-BUILDER76 = a NEW COPY** `build_addendumra20_gate76.py` with the required `RA20_MERGE_IN_HEAD`, the ordinal re-keyed, the tuple extended (R 17th, R 18th, G 4th), the 9 refusal arms and the positive control on the real M. R 17th's builder is never edited.
- **Q-MERGEIN76 = as recommended** (R 12th's mergein + pushra1_ff copies, every knob a required argument; adopt `feature/ks-1274-trivy-bare-object-guard-ra18-1`'s NAME for the one push; full preflight in-hook; no `--no-verify`).
- **Q-NULLRESULTS = Minor, a named limitation**, rides with KS-1274's owed live run; no new ticket.
- **Q-LIMIT593 = not a finding against #1428**; named in the KS-593 comment batch (Q-NOTIFY12); no new ticket.
- **Q-RACE76 = do not hold the batch**; re-predict before each step; #1429 and #1430 go to gate77.
- **Q-PREFLIGHT76 = accept** (one preflight on wtFinal).
- **Q-LIVE76 = neither KS-1274 nor KS-593 moves to Done** on this merge.
- **Q-USAGE76 = as wired** (the repin exports `WED_USAGE_STOP=100` only after reading the live grant file).

## AFTER THE VERDICT — Wednesday, 19:51 AEDT
Verdict mail `[QA -> Wednesday] GATE76 …` 08:49:45Z read WHOLE (281 lines); report sha256 58c3b8d1e5b720c2… re-hashed EQUAL (671 lines); squash bodies 91e3ee3a… (4,998 B) and 06737833… (6,064 B) re-hashed EQUAL; develop / #1427 / #1428 re-read unmoved.
- **#1428 is NOT held for a doc re-draft.** N-1428-1 (the cheat authz-order sentence), N-1428-2 ("non-object" in the docs and the `documents.ts:2212` comment) and N-1428-6 (the b8ff928e2b63 tree) are Minor; the gate measured that no runtime decision moves. Both merge as gated, in the ruled order, with the GATE76 squash bodies.
- **OWED, queued for Seat R 20th AFTER both merges:** ONE docs-and-comment-only follow-up PR correcting N-1428-1, N-1428-2 (docs + the code comment) and N-1428-6 on both platform docs, keyed `Refs KS-593`, tier 2 through-code. No product line changes.
