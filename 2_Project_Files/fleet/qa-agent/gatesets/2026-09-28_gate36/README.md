# Gateset 2026-09-28_gate36 — README for Wednesday

Written 2026-09-28T08:44:00Z by the drafter (make_readme_gate36.py; every figure below is read from the kit's own output files at that moment, each named beside it).
The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-28_gate36/` and scratch under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad` (the scratch clone `g36_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, objects borrowed READ-ONLY via alternates, then fetches FROM ORIGIN into it with the checkout's repo-local key; the emit-probe workdirs `g36_emitprobe_*`; the control workdirs `g36_controls_*`; assembly parts and trial outputs under `g36/`). It did NOT write the routing line (§4).
The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its typescript). GitHub: REST GET only (GH_TOKEN read by name, never printed). Linear: queries only. decisions.json and inbox_routing.conf: read only.

**gate36 = FOUR PRs (T1 x2, T2 x2), one kit, no sibling, NO stack, ONE base.** Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree (predict_1.out (a)).

| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | why this tier (tiers lesson 2026-09-05) |
|---|---|---|---|---|---|
| #1323 | KS-1129 | T1 | `1a509947caf936bcc9b05f7817af6fcbcc974289` | 1 on `d9ce1403d158` | T1 verify-claim: changes what the gateway TELLS a verifier (`verified`, `verificationConfidence`, the demo's on-chain badge) |
| #1324 | KS-1124 | T1 | `47c4579b0199df1168220fa226805718c26fbbb3` | 1 on `d9ce1403d158` | T1 blob-write: the defect it narrows ERASED persisted anchor fields (data-destruction class); "token" = the Cardano thread-token NFT cache, not an auth token |
| #1325 | KS-1227 | T2 | `39f4922d391dabc7f3f99c9c0c8ea2ddde1b596f` | 1 on `d9ce1403d158` | T2 test-only: one cell file, no product byte (MEASURED: predict (e)) |
| #1326 | KS-1351 | T2 | `3f569dfc701c757253aa71ed8b91b81ce9c84c93` | 1 on `d9ce1403d158` | T2 types-only, CONDITIONAL on no runtime change (MEASURED by the drafter's emit probe; the gate re-measures) — it types a revocation field, and key revocation is a T1 surface |

### Squash subjects and bodies

| PR | declared subject (WITHOUT `(#n)`, the PR title as the PULLS API returned it) | declared | lands at (+8, ` (#n)`) | <= 92 | ends in `(#n)`? | squash-body keys: own | FOREIGN hyphenated keys seen (title / body / commit msg) |
|---|---|---|---|---|---|---|---|
| #1323 | KS-1129: the live chain-scan reply is shape-checked before it can claim on-chain | 80 | 88 | yes | no | KS-1129 | none (keyscan_1.out) |
| #1324 | KS-1124: the thread-token cache write merges into the blob as persisted now | 75 | 83 | yes | no | KS-1124 | none (keyscan_1.out) |
| #1325 | KS-1227: keep the count-every-stub-request rule, and say so beside the witness | 78 | 86 | yes | no | KS-1227 | none (keyscan_1.out) |
| #1326 | KS-1351 item 1: declare the revocation fields on a Secuura status extension | 75 | 83 | yes | no | KS-1351 | none (keyscan_1.out) |

Measured by fill_1.out: `subject scan: every declared subject WITHOUT a (#n) suffix, landed length <= 92: #1323 80->88, #1324 75->83, #1325 78->86, #1326 75->83`; `key scan: 4 mandated squash text block(s), each carries only its own key: #1323 ['KS-1129'], #1324 ['KS-1124'], #1325 ['KS-1227'], #1326 ['KS-1351']`. keyscan_1.out: no foreign hyphenated key and no closing word before a key in any title, body or commit message.
**Commit messages that must not be pasted:** on MG-3 grounds, NONE — no commit message carries a foreign hyphenated key (MEASURED). By the standing rule (compose, never paste) ALL FOUR are not to be pasted as squash bodies: each ends in a `Co-Authored-By` trailer; #1323's names "KS 1069" / "KS 522" space-separated (harmless as written, but not squash text); and #1325's TEST FILE carries a hyphenated `KS-1180` as content — a squash body quoting the new assertion string verbatim would attach KS-1180 (the seat's own keyscan refused exactly that on its first #1325 body).

Routing `QA/Secuura-batch1323` (**NOT added by the drafter** — §4). GO string `GO: merge #1323, #1324, #1325, #1326 batch` (or the subset); **the GO mail's SUBJECT must name Seat B 38th, with NO `#` before the numbers**: `GO (Seat B 38th): merge 1323 1324 1325 1326 on gate36` (the prompt carries this as kit rule exit 51). MERGE ORDER #1323 -> #1324 -> #1325 -> #1326 (END_TREE is order-independent, measured in all 24 orders). The GO goes to **Seat B 38th**, which raised all four and merges its own, one at a time.

**Kam's cards (READ from `0_Brain/dashboard/data/decisions.json`):** NONE rules any of the four PRs. `secuura-ks1124-f4-failed-anchor-shows-pending` is OPEN (F4 — out of #1324's scope); `secuura-ks1352-revoked-credentials-still-verify` is OPEN (a revoked credential still verifies — NOT fixed by #1326). #1325's and #1326's design choices were Wednesday's, under the 2026-08-07 autonomy grant (the PR bodies say so).

## 1. BLUF
- **Kit: READY to launch once the routing line is added** — launcher `--check` rc 0 (`all guards pass:`, launcher_check_1.out); repin `--dry-run` rc 0 (repin_dryrun_1.out: DRY RUN COMPLETE 2026-09-28T08:21:14Z — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add). The real launch refuses rc 1 at step 0 until `QA/Secuura-batch1323|coagent@agentmail.to|yes` is in inbox_routing.conf (§4).
- **Pinned over develop `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`** (tree `a87715ebff3ec63e7513fe9a7d5314150fdd08f1`, == gate35's END_TREE) — ls-remote AND fetched AND the API compare agree; gate35's #1321 / #1322 squashes in (MERGED). ONE merge-base `d9ce1403d158` for all four; develop has not moved since, so the move ∩ every own path is EMPTY.
  - **END_TREE `36d6a2425ecf27c0e898b61e17e1a6280971387b`** (7 files changed, 162 insertions(+), 8 deletions(-)), identical in ALL 24 orders (32 memoised merge-tree calls); diff(develop, END) == the union of the seven own paths and every END blob == its PR's head blob (MG-1).
  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): 2026-09-28T08:44:00Z | d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817	refs/heads/develop | 1a509947caf936bcc9b05f7817af6fcbcc974289	refs/pull/1323/head | 47c4579b0199df1168220fa226805718c26fbbb3	refs/pull/1324/head | 39f4922d391dabc7f3f99c9c0c8ea2ddde1b596f	refs/pull/1325/head | 3f569dfc701c757253aa71ed8b91b81ce9c84c93	refs/pull/1326/head — every pin still current: **True**.
- **Controls, both ways (controls_gate36.sh):**
  - normal (controls_1.out, rc 0): `SUMMARY gate36: 170 controls, OK 170, MISMATCH 0`
  - `--invert` (controls_2.out, rc 1): `SUMMARY gate36: 170 controls, OK 0, MISMATCH 170 (inverted: every control must MISMATCH-then-flip to OK; a MISMATCH here is a control that could not fail)` — every one of the 170 controls reported MISMATCH (rc 1 by design): each control can fail
- **OVERLAPS:** NONE. No stack, no shared file (#1323 and #1325 share the api-gateway SERVICE only); every kit path is disjoint from ALL 20 other open PRs. `merged_blob_paths` NONE and `noop_paths` NONE (predict (c)).
- **#1323 / #1324 == their READY and golden (MEASURED, predict_1.out (e)):** each READY block is byte-identical to its brief's golden and to the Spark checker's patch.diff; both goldens apply strict with `git apply --cached --check` at d9ce1403d158 and every blob == the head's. The +/- lines are **SLIDE-EQUAL, not IDENTICAL**: the same lines per file, but in each TEST file the inserted block's blank line sits at the other end in the brief than in `git diff -U0` — a representation difference; the blob equality is the discriminating instrument. #1325 / #1326 have NO READY (seat-written).
- **#1326 no-runtime-change (MEASURED by the drafter, emitprobe_gate36.py -> emitprobe_1.out):** types.ts emitted JS merge-base -> head: IDENTICAL; credentialRepo.ts emitted JS merge-base -> head: ["-            let result = await (0, db_1.query)('SELECT credential FROM vc_credentials_store WHERE id = $1', [id]);", "+            const result = await (0, db_1.query)('SELECT credential FROM vc_credentials_store WHERE id = $1', [id]);"] (ONLY let -> const on one line); END_TREE deltas equal the head's: True. Controls: C1 a planted runtime edit makes the emit DIFFER: True; C2 a planted type-only edit leaves the emit IDENTICAL: True; C3 head vs itself IDENTICAL: True; C4 types.ts emit non-empty at every revision: True.

### 1a. #1323 KS-1129 livescan — READ predictions (the gate measures THROUGH THE REAL ROUTE)
- The guards only NARROW: every live reply the head accepts, the merge-base accepted (READ). ONE live `anchors/verify/` fetch in api-gateway src — the guards cover every gateway live reader (READ, predict).
- **MIXED-ECHO:** `liveConfirmedAt` (:612) is set inside the verified branch whatever the hash / height guards decide; `txHash = liveTxHash || persistedTxHash`, `blockHeight = liveBlockHeight || persistedBlockHeight` (:666/:667); `source` is `cardano-live` whenever the live hash passed (:776). So a reply whose hash passes but height is refused answers `source: cardano-live` with the live hash beside the PERSISTED (or null) height, and a refused hash still echoes the reply's `confirmedAt`. The CLAIM is guarded; the echo is presentation — the prompt makes the gate measure it and say whether it misleads.
- **GUARD-PARITY:** the same placeholder regex as the persisted read (:646); neither demands 64-hex. **STRICT-HEIGHT:** a string `blockNumber` does not fall back to a numeric `blockHeight` (`??` stops at a non-null string). The body calls L5 "a behaviour choice, not a bug fix" (from the E7 ruling).
- **HELD-SURFACE (open question):** the 09-25 KS-1129 comment calls the gateway chain-scan readers "a held surface"; the body says "no recorded hold was found" and that Wednesday reads the hold as lapsed. Carried to the gate as a question, not a defect (§6 Q3).

### 1b. #1324 KS-1124 mintmerge — WHAT REMAINS of the race (READ; the gate measures each through the real create route)
- **R1 WINDOW:** still read-then-write — an anchor write landing between the read-back (:799) and the cache write is lost (the PR says so).
- **R2 MIRROR (not in the PR's scope, not disclosed in its body):** the create-path anchor-accept write (`blockchain: initial`, :913) and the anchor_failed write (:928) REPLACE the column wholesale and do not carry `threadToken` — a thread-token write that lands FIRST is erased by them. KS-1074's `carriedForward` covers the anchorStateSync writers only. The same O1 bug in the other direction.
- **R3 READ FAILURE:** `getDocument(...).catch(() => null)` falls back to the create-time copy — the pre-PR overwrite — when the read-back rejects.
- Flag-gated (STATE_THREAD_NFT_ENABLED=true AND SIMULATE_ANCHORING !== 'true'); the atomic fix (a JSONB merge in documentRepo) is unruled. The brief's arm and the seat's arm differ (the seat's first arm was a TS6133 load failure) — the gate re-runs both.

### 1c. #1325 KS-1227 and #1326 KS-1351
- #1325: TEST-ONLY (predict (e): no product file); 8 cells at base and head; R1's expected substring is a shorter prefix of the new message (READ: any change after "ASKED once" no longer reds R1). The try/finally detach and R2 were already at develop — the PR may discharge KS-1227's DoD while saying `Refs`.
- #1326: TS2339 4 -> 0 is the SEAT's figure (the drafter did not run tsc); the trap it recorded — vc-issuer resolves @secuura/shared to `dist/`, so shared must be REBUILT before any consumer tsc — is in the prompt. The credentialRepo.ts :95 anchor is NOT byte-unique alone (also :118, getByHash): the kit and the prompt use a two-line anchor. 38 source lines in 7 files name `SecuuraCredential` (predict (e), READ). KS-1352 (revoked credentials still verify) is NOT fixed by it.

### 1d. Other
- **Fleet STOP (READ, bounded region, NOT-FOUND control):** #1323 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60) (PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.); #1324 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60) (PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.); #1325 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60) (PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.); #1326 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60) (PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.). After this merge: 28/0 · 6/0 · 49/0 · 60 of 60.
- **Linear: all four PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1129, KS-1124, KS-1227, KS-1351 In Progress (the seat read KS-1124 and KS-1351 as Backlog at its boot; the board bot walked them).
- **Re-key / namespace (rekey_1.out):** rekey_check_gate36 | dir /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-28_gate36 | 18 file(s), 2250 line(s) | 61 forbidden spelling(s), 5 lineage-only | 61 lineage hit(s) ALLOWED by marker | RESULT CLEAN: 0 hit(s)
- **Drafting slips caught (disclosed):** (1) the first READY comparison read DIFFER — an insertion slide, not a code difference; the comparator now reports SLIDE-EQUAL beside the strict golden apply, with its own control; (2) the first consumer grep used `\b`, which this git's ERE does not support — a false 0; now POSIX with a >0 control; (3) a quoting slip in the assembled predict (an unescaped apostrophe) failed the first sims with a SyntaxError — fixed, every sim re-run.
- **Sizes / sha256:** `2026-09-28_secuura-batch1323.prompt.txt` 47520 bytes sha256 `d58a2993bef33794037a4f4e5bb191c570782fb1634367c4a9c2fc016a76b727`; `launch_qa_secuura_batch1323.sh` 19888 bytes sha256 `30dc68a00d9f42d2803f349a4f65c9ef378fefec331d7ca0975a8586ba5c4161`; `mail_gate36_ready.md` 58901 bytes sha256 `649aed32f936faac13c1f3d24ebb53016b04869c6877675cef78fd6cf0bb2bd5`.

## 2. Pins — predict_1.out (rc 0)
- #1323: 1 commit `1a509947caf9` over merge-base `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`; 0 behind develop; merged tree `b54d762d1a90551b198780e49622d86f52580158`; every merged blob == its head blob; numstat ['49\t0\tBlockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts', '5\t3\tBlockchain/Dev/services/api-gateway/src/routes/verification.ts']; no mode change; move ∩ own paths EMPTY.
- #1324: 1 commit `47c4579b0199` over merge-base `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`; 0 behind develop; merged tree `0e79b1fe4f8ca866cb914f74a01984258cac66d3`; every merged blob == its head blob; numstat ['5\t2\tBlockchain/Dev/services/originate/src/routes/documents.ts', '63\t0\tBlockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts']; no mode change; move ∩ own paths EMPTY.
- #1325: 1 commit `39f4922d391d` over merge-base `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`; 0 behind develop; merged tree `c63531167ea4110e1fd852a2d806e8e5fb4d7ac7`; every merged blob == its head blob; numstat ['14\t2\tBlockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts']; no mode change; move ∩ own paths EMPTY.
- #1326: 1 commit `3f569dfc701c` over merge-base `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`; 0 behind develop; merged tree `40d79e5d6caa7b0f4279cff479393c1e7de012cb`; every merged blob == its head blob; numstat ['1\t1\tBlockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts', '25\t0\tBlockchain/Dev/packages/shared/src/vc/types.ts']; no mode change; move ∩ own paths EMPTY.
- Simulations: foreign1323 -> REFUSED: FAIL=13; foreign1324 -> REFUSED: FAIL=13; foreign1325 -> REFUSED: FAIL=4; foreign1326 -> REFUSED: FAIL=4; moved -> PASS: FAIL=0. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR's first own file (must REFUSE). `predev` (`6bf794da4731`, develop^ = gate35's #1321 squash) is the moved-develop pin in controls D / RC / RD / RE / RN / RO.

## 3. What the gate owes
- Prompt `2026-09-28_secuura-batch1323.prompt.txt` — #1323 through the REAL route (simulated / mock / string-height / strict-verified replies at merge-base, head and END_TREE, a real-reply control, the mixed echo, the held-surface question); #1324 the race table through the real create route (the fixed order, the window, the mirror, the read failure; the brief's and the seat's arms); #1325 the coupling arms and the same-service END_TREE run; #1326 TS2339 4 -> 0 with shared REBUILT, a consumer sweep, the emit re-measured, prefer-const 1 -> 0; every seat red proof re-run; suites at develop / head / END_TREE; tsc with `exclude: []`; lint; the MANDATED SQUASH TEXT blocks; `## MERGE ADDENDUM` last.
- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-28-batch1323-g36/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.

## 4. Routing line — NOT added
Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch lines — the previous kit's pane line sits at line 136, READ) — backup first:
```
QA/Secuura-batch1323|coagent@agentmail.to|yes
```
Until it is present the launch action's step 0 refuses rc 1 (repin_dryrun_1.out: "line present: 0").

## 5. The ONE launch command
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-28_gate36/repin_and_launch_gate36.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-28_gate36/launch_qa_secuura_batch1323.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad
```
- Dry run (`--dry-run` appended): repin_dryrun_1.out -> DRY RUN COMPLETE 2026-09-28T08:21:14Z — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add (rc 0).
- Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`); if `g36_sp/clone.git` is absent there, predict rebuilds it on a re-pin (the emit probe is NOT re-run by a re-pin). A develop move re-pins in the same action (step 3b); an own-path move, a stack, an overlap or an END-tree disagreement refuses rc 10. A new PR on KS-1129 / KS-1124 / KS-1227 / KS-1351 or on a `-b38-<n>` branch outside the kit refuses rc 15. A moved head or a base not develop refuses rc 11.

## 6. Questions for Wednesday (each with the drafter's recommendation)
1. **The routing line** (§4). *Recommend:* add it, then launch.
2. **The coagent@ inbox.** Seat B 38th's plan confirmation (item 13, READ) says `coagent@agentmail.to` "now returns HTTP 404" and names `secuura-blockchain@agentmail.to` as the live inbox. The gate mails FROM coagent@ and the routing line routes to coagent@, as commissioned. The drafter did NOT probe AgentMail. *Recommend:* confirm coagent@ answers before launch; if it does not, the gate's verdict mail cannot be sent.
3. **HELD-SURFACE (#1323).** The 09-25 KS-1129 comment calls the gateway chain-scan readers "a held surface"; no hold is recorded that the seat or the brief found. *Recommend:* confirm the hold has lapsed (or ask Kam) before signing a GO on #1323; the gate carries it as a question.
4. **The tiers.** #1323 T1 (verifier claim), #1324 T1 (data-destruction class; the thread token is an NFT cache, not an auth token), #1325 T2, #1326 T2 conditional on no runtime change. *Recommend:* as drafted; the prompt tells the gate to re-tier #1326 to T1 if it finds any runtime byte beyond let -> const.
5. **The MIRROR race (#1324, R2).** The create-path anchor-accept / anchor_failed writes erase a threadToken that landed first — not in the PR, not in its body. *Recommend:* launch; if the gate measures it, ticket it (KS-1074 extension or new) — not a NO GO on #1324. The atomic JSONB merge that would close R1 and R2 is a design question for Kam.
6. **§5f:** #1323 and #1324 are runtime changes — neither moves to Done on offline evidence (the canonical `live sweep owed` comment). #1325 / #1326 change no runtime.
7. **KS-1352.** #1326 declares `revoked` but verify still does not read it (card OPEN, default a at Tue 29 Sep 09:00 AEST). *Recommend:* no action in this gate; the #1326 verdict line says so.

## 7. Controls: `controls_gate36.sh <scratchpad> [--invert]`
- **controls_1.out:** `SUMMARY gate36: 170 controls, OK 170, MISMATCH 0` (rc 0).
- **controls_2.out (`--invert`):** `SUMMARY gate36: 170 controls, OK 0, MISMATCH 170 (inverted: every control must MISMATCH-then-flip to OK; a MISMATCH here is a control that could not fail)` (rc 1, by design).
- Same arms as gate35's kit, re-keyed: wrong heads (one hex digit), a moved develop (predev), per-PR path renames (all four PRs), capture / prompt doctoring, every kit rule 35 / 40-44 / 46-51 SPLIT, the GO string and merge authority, the addendum, the verdict subject, a wrong END_TREE, a moved launcher, the non-TTY launch path, repin argv / routing / WIDEN by title and by branch / a false STACK / the REAL re-pin across a move in a copy / RE-RN-RO declaration plants, predict `--simulate foreign1324` and `moved`, fill from SIM / failed pins, SJ1-SJ3 subject plants, and NS[<spelling>] over gate35's and gate34's namespaces.
- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, the emit probe's verdicts beyond its four built-in controls.

## 8. Could not measure (the drafter's NOT-MEASURED list)
- No suite, tsc, lint, prettier or red-proof run by the drafter; every seat figure (20/20, 781, 6/6, 1055, 8/8, 773, TS2339 4 -> 0, 15 files / 140, the arms) is a claim in its PR bodies and records. Its raise/ holds tamper diffs for KS-1129 / KS-1124 (READ, not run) and no red / green output files.
- #1323 through the real route: NOTHING — no simulated / mock / string-height reply was driven; the MIXED-ECHO is a READ prediction.
- #1324 races: NOTHING at runtime — R1 / R2 / R3 are READ from documents.ts / anchorStateSync.ts / documentRepo.ts. Whether any deployed environment sets STATE_THREAD_NFT_ENABLED — not read.
- #1326: TS2339 and the consumer sweep not run (the emit probe measures emitted JS only; `.d.ts` output not compared).
- `check:openapi`, the served spec, Schemathesis, legs 3 / 4 / 8 — need a stack or were left to the gate. Whether the KS-1129 "held surface" was ever recorded anywhere outside WEDNESDAY/0_Brain — not searched. AgentMail (coagent@) reachability — not probed.

## 9. Files
- Kit: kit.json · COMMISSION.md (make_commission_gate36.py) · README.md (make_readme_gate36.py) · rekey_check_gate36.py -> rekey_1.out
- Pins: predict_gate36.py -> predict_1.out, predict_sim_*.out, pins_gate36.json (+ .SIM-*.json) · keyscan_gate36.py -> keyscan_1.out · final_lsremote_1.out
- Measurements: emitprobe_gate36.py -> emitprobe_1.out, emitprobe_gate36.json (#1326 no runtime change)
- Reads: gh_read_gate36.py -> gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate36.py -> linear_reads_1.out, linear_KS-*.md · capture_mail_gate36.py -> capture_1.out, mail_gate36_ready.md, stopcounts_gate36.json · _api_peek_gate36.py -> _api_peek_1.out
- Prompt/launcher: prompt_gate36.TEMPLATE.txt, launcher_gate36.TEMPLATE.sh.txt, fill_gate36.py -> 2026-09-28_secuura-batch1323.prompt.txt + launch_qa_secuura_batch1323.sh (fill_1.out), launcher_check_1.out · repin_and_launch_gate36.sh -> repin_dryrun_1.out · controls_gate36.sh -> controls_1.out / controls_2.out
