# Spark operator 3 report, 2026-10-28 15:5x-16:4x AEDT (Sonnet operator for Wednesday)

Nothing pushed, raised, merged, commented, mailed or written under `!CODING/`. gh and Linear: gh read only (open-PR list, with the Secuura project's own GH_TOKEN in a scratch GH_CONFIG_DIR; the token was never printed); Linear read only (the review script's ticket fetch). One stray READY (`...-X-PASS...`, made by a test invocation of hold_ready.py on ks_1670_p1) was moved, not deleted, to `local-model/night/_quarantine_2026-10-28/`.
Clones (both at NON-EXISTENT paths, `rev-parse --show-toplevel` asserted equal to the dir before any fetch or write): `local-model/spark/cache/work/op3-hold-1028` (source reads, apply checks, open-PR heads) and `.../op3-review-1028` (the review harness). Develop read by `git ls-remote` at start and used throughout: `bd6697e079fce41db6b21e094a9eddb3d0e1d08e` (the passes were built at `65bc28234507ffcf242381f8020d80b3efe83e85`; 2 commits ahead; none of the 55 files the 23 passes touch changed between the two).

## Open-PR overlap check (re-run against CURRENT open PRs, before holding)
`gh pr list -R Secuura/Distributed_Secuura --state open --json number,title,baseRefName,files` -> **14 open PRs, 93 file entries** (#1726 #1383 #1360 #1129 #949 #948 #947 #946 #945 #887 #649 #639 #635 #575: dependabot bumps, lockfiles, old docs/migration PRs). Against the golden `+++ b/` file sets of all 23 held and new passes (55 distinct files): **0 overlaps**. Pass-versus-pass: the only shared file is `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (ks_1779_p1 and ks_1780_p2_admin, already flagged "raise in sequence"). `git diff --name-only 65bc2823 bd6697e0` intersected with the 55 files: empty ("DRIFT" lines: none). Method note: gh as the global/launcher config said "not logged into any GitHub hosts" (hosts.yml is empty); the earlier operator's way (project GH_TOKEN, scratch config dir) worked.

## JOB 1 - the seven batch-4 passes HELD (READY files in `local-model/night/`, decision notes appended inside each)
Hold command per pass: `python3 night/hold_ready.py --model-tag spark-dsv4flash --brief <brief> <run dir> <control run dir> <ROWID> <TITLE>` (output "HELD", golden BYTE-IDENTICAL for all seven). Each pass's golden.diff was read line by line against its brief and against the product file at the base commit (`git show 65bc2823:<path>`, develop for the apply checks).
| pass | verdict | apply mode (checker, per section) | whole-patch `git apply --check` at bd6697e0, strict / lenient | decision or note |
|---|---|---|---|---|
| ks_1701_p1 (originate documents.ts, certifications.ts, shared test helper) | HOLD-WITH-DECISION | sections 1-2 LENIENT (`--recount --ignore-whitespace -C1`), 3-4 strict; STRICT NOT CLAIMED | fail / pass | access WIDENS: `SUPER_ADMIN` and mixed-case spellings become platform admin at four sites (isPlatformRole upper-cases). Ticket is facts-only; the fix shape is the drafter's. Also interplays with ks_1591_p1 (changes isPlatformRole), files disjoint |
| ks_1536_p1 (auth issuerCerts.ts, hasAdminRole) | HOLD | STRICT (apply_mode=strict) | pass / pass | none; behaviour-preserving, Refs KS-1536 only (builder needed an open ticket) |
| ks_1240_p4_social (github, google, linkedin; 7 fetch sites) | HOLD-WITH-DECISION | sections 1-3 REANCHORED by the checker (model hunk headers did not match), test strict; STRICT NOT CLAIMED | fail / fail | 10 000 ms is the drafter's; a timeout is a 400 `OAuth authentication failed: <abort text>` on the login callback (auth.ts:1074, state already consumed) and an unclassified rejection on `POST /social/link` (auth.ts:1360, no local try) |
| ks_1240_p5_social2 (apple, facebook, microsoft-personal; 5 sites) | HOLD-WITH-DECISION | sections 1-3 REANCHORED, test strict; STRICT NOT CLAIMED | fail / fail | same 10 s and same timeout behaviour; facebook's two fetches gain a second argument `{ signal: ..., }` (trailing comma style) |
| ks_1240_p6_tokenisation (api-gateway tokenisation.ts) | HOLD-WITH-DECISION | section 1 FUZZY (`-C1`), test strict; STRICT NOT CLAIMED | fail / pass | 10 s is the drafter's; **found at source: `tokeniseFields` and `detokeniseValues` have no callers at the tip** (git grep over the whole tree) so the patch bounds unused code |
| ks_1240_p7_ipfs (nft-certificate ipfs.service.ts, 8 sites, 3 bounds) | HOLD-WITH-DECISION | STRICT | pass / pass | bounds 60/15/30 s are the drafter's; scope extension beyond the gateway ticket; **found at source: the gateway read's `await response.arrayBuffer()` (:487) is outside the try**, so a body stall is the raw abort error, not the 503 the constants comment promises, and a >30 s download fails |
| ks_1240_p8_provisioning (tenant-provisioning meteringKey.ts, index.ts) | HOLD-WITH-DECISION | section 1 LENIENT (`-C1`), 2-3 strict; STRICT NOT CLAIMED | fail / pass | 10 s x2 are the drafter's; scope extension; **found at source: a key-generation timeout does NOT fail tenant creation** (index.ts:262-269 catch only logs): the tenant is inserted with `vault_key_hash` NULL and the handler answers 201 `success: true` with `keyFile: null` |
Held 7: HOLD 1, HOLD-WITH-DECISION 6, REJECT 0. Strict apply is claimed for ks_1536_p1 and ks_1240_p7_ipfs only. Sequence: no shared file with any other held pass; Refs, never a close-word, on all (KS-1240 has five more PRs after the earlier three).
Command output, the whole-patch matrix at bd6697e0 for all 23 passes (`git apply --check <patch.diff>` then the same with `--recount --ignore-whitespace -C1`):
```
ks_1701_p1 strict@bd6697e=1 lenient=0
ks_1536_p1 strict@bd6697e=0 lenient=0
ks_1240_p4_social strict@bd6697e=1 lenient=1
ks_1240_p5_social2 strict@bd6697e=1 lenient=1
ks_1240_p6_tokenisation strict@bd6697e=1 lenient=0
ks_1240_p7_ipfs strict@bd6697e=0 lenient=0
ks_1240_p8_provisioning strict@bd6697e=1 lenient=0
ks_1197_p1 strict@bd6697e=0 lenient=0
ks_1219_p1 strict@bd6697e=0 lenient=0
ks_1240_p1 strict@bd6697e=0 lenient=0
ks_1240_p2_proxy_admin strict@bd6697e=1 lenient=0
ks_1240_p3_batch_audit strict@bd6697e=0 lenient=0
ks_1250_p1 strict@bd6697e=0 lenient=1
ks_1467_p1 strict@bd6697e=0 lenient=0
ks_1467_p2_shared strict@bd6697e=0 lenient=0
ks_1591_p1 strict@bd6697e=0 lenient=0
ks_1591_p2_security strict@bd6697e=0 lenient=0
ks_1776_p1 strict@bd6697e=0 lenient=0
ks_1779_p1 strict@bd6697e=1 lenient=0
ks_1780_p1 strict@bd6697e=0 lenient=0
ks_1780_p2_admin strict@bd6697e=0 lenient=0
ks_1780_p3_webhooks strict@bd6697e=0 lenient=0
ks_1670_p1 strict@bd6697e=0 lenient=0
```
Also recorded: an ADDENDUM appended to the earlier operator's `READY_KS-1250-...` (see Job 2: a real finding the Spark's review made and I confirmed at source). Nothing else in earlier READY files was edited.

## JOB 2 - Spark second-opinion review over every held READY diff (calibration for the 10-26 gate pilot; NOT a merge verdict)
Instrument: `local-model/gate/spark_review.py` (REVIEW_CHECKLIST.md as the system prompt, strict JSON back, streamed, repetition guard, SPARK_THINK=0, temperature 0), one request at a time. The deterministic half (`spark_gate.sh`) needs a PR number, so for these held diffs (no PR exists) the operator built `facts.json` from the Spark round's OWN checker artefacts (touched files, numstat, red-first and green-after counts, suite delta, checker SUMMARY; lint "not run") and a local head commit made by applying the canonical patch per section in the checker's apply mode at the pass's tip `65bc2823` in `op3-review-1028`. Ticket text came from Linear via the script's own read; ticket comments excluded (its default). No PR body and no draft comment were provided, so the "overstated sentence" leg is empty by construction. Harness scripts are in the session scratchpad (review_one.py, review_one_bash.py for the bash pass, drive.sh); per-diff inputs and outputs are in `0_Brain/reference/2026-10-28_spark-operator3/reviews/<tag>/` (`prompt_user.txt`, `facts.json`, `diff.patch`, `raw_attempt*.txt`, `review.json`, `stdout.txt`). Before each run: `fleet/spark_status.py` and `tunnel.sh check` (the driver's log is `scratchpad/drive.log`; tunnel UP every time, never re-opened).
Columns: findings (severity mix) | Spark verdict | my classification of its findings: R real observation, S real but by design (already disclosed in the READY note, a sibling pass, or the drafter's scoped extension; the Spark usually calls these Major), F false or misread, N noise (not a defect), U not verified by me at source | `evidence_quote_found_in_input` (the script's own deterministic check that every backticked quote appears in the material) | minutes | prompt+completion tokens | what I checked.
| diff | findings | verdict | classification | quote-found | minutes | tokens | basis |
|---|---|---|---|---|---|---|---|
| ks_1670_p1 | 4 (Major0/Minor0/Note4) | GO WITH NOTES | R2 S2 F0 N0 U0 | 2/4 | 0.7 (44 s) | 28619+561 | claims read against the ticket text and the READY note; all four are true observations, two already disclosed (Refs, source-text pin) |
| ks_1701_p1 | 4 (Major2/Minor2/Note0) | NO GO | R4 S0 F0 N0 U0 | 2/4 | 1.8 (108 s) | 83259+736 | [0],[1] real but Major is overstated (source-text pin and unestablished reachability are both in the brief/ticket as disclosed); NO GO is not warranted for a decision-class item |
| ks_1536_p1 | 4 (Major0/Minor0/Note4) | GO WITH NOTES | R2 S2 F0 N0 U0 | 1/4 | 0.5 (32 s) | 18051+573 | R3 source-text pin and the permissive mocked authenticate are true; ticket-scope notes are disclosed groundwork |
| ks_1240_p4_social | 4 (Major0/Minor0/Note4) | GO WITH NOTES | R1 S1 F1 N1 U0 | 2/4 | 0.5 (29 s) | 10676+645 | [1] verified at source: R5-R7 spy AbortSignal.timeout to an already-aborted signal; [2] the stub rejects on abort like a real fetch, so 'more permissive' is wrong; [3] is not a finding |
| ks_1240_p5_social2 | 6 (Major3/Minor2/Note1) | NO GO | R2 S2 F1 N1 U0 | 3/6 | 0.6 (38 s) | 9989+976 | [0],[1] real (ticket is the gateway connector-token ticket; 503 not built) but disclosed scope/decision, not Major; [2] real (mocked abort); [4] verified: R4 only asserts 0<ms<=30000, 10_000 not pinned; [3] same wrong stub claim as p4 |
| ks_1240_p6_tokenisation | 4 (Major0/Minor0/Note4) | GO WITH NOTES | R2 S1 F0 N1 U0 | 1/4 | 0.5 (29 s) | 8905+814 | [1],[2] verified in the test (mocked abort; <=30000 only). MISSED by the Spark: tokeniseFields/detokeniseValues have no callers at the tip (found at source by the operator) |
| ks_1240_p7_ipfs | 7 (Major0/Minor0/Note7) | GO WITH NOTES | R2 S2 F0 N1 U2 | 5/7 | 0.7 (42 s) | 14153+997 | [3] verified (R5 asserts <=120000, not 60/15/30); [1] contradicts itself ('the comment is consistent'). MISSED by the Spark: the gateway-read body (await response.arrayBuffer()) sits outside the try, so a stall is not the promised 503 |
| ks_1240_p8_provisioning | 6 (Major0/Minor1/Note5) | GO WITH NOTES | R4 S1 F0 N1 U0 | 2/6 | 0.8 (50 s) | 15025+1223 | [3] source-text pin of index.ts is disclosed in the brief; MISSED by the Spark: a key-generation timeout yields a 201 key-less tenant (index.ts:262-269) |
| ks_1197_p1 | 5 (Major2/Minor2/Note1) | NO GO | R1 S2 F2 N0 U0 | 1/5 | 0.6 (37 s) | 9525+918 | [1] FALSE at source: the patch coerces `userLevel` to a string at enforcement.ts:154 before the later toUpperCase; [3] FALSE: facts test_on_head is the green-after run, 'red at the tip' is the red-first leg; [4] real nuance (non-string level now meets a 'none'-required type; before it was a 500) |
| ks_1219_p1 | 8 (Major0/Minor0/Note8) | GO WITH NOTES | R2 S0 F2 N1 U3 | 3/8 | 2.0 (119 s; 2 attempts) | 63882+3057 | [1] FALSE-ish: auth mounts express.json globally (index.ts); [3] restates; [4] describes ordering, not a defect; one repetition abort then a valid retry (119 s) |
| ks_1240_p1 | 3 (Major0/Minor0/Note3) | GO WITH NOTES | R2 S1 F0 N0 U0 | 2/3 | 0.4 (24 s) | 13169+437 | magic number 5000 and mock-only signal check are true; 503 note disclosed in the READY decision note |
| ks_1240_p2_proxy_admin | 7 (Major4/Minor2/Note1) | NO GO | R1 S3 F0 N1 U2 | 3/7 | 1.5 (88 s) | 47365+1342 | [0],[1] sibling/scoped (the key-exchange half is pass p1, held separately; 502 is the existing catch) and not Major; [2] absence-red is normal for a new-symbol test, disclosed as source-text; [3] true (source-text only, disclosed) |
| ks_1240_p3_batch_audit | 5 (Major2/Minor2/Note1) | NO GO | R3 S1 F0 N1 U0 | 3/5 | 0.6 (37 s) | 12675+822 | [0] 503 not built: disclosed; [1] true (source-text tests, disclosed); [3] hard-coded 30 s is the disclosed decision |
| ks_1250_p1 | 5 (Major2/Minor2/Note1) | NO GO | R1 S0 F1 N0 U3 | 5/5 | 0.8 (47 s) | 12456+1288 | [0] VERIFIED REAL AT SOURCE and new information: smoke-test.sh full run (section 7 on) still calls hard-coded localhost:60xx ports (lines 257-327 at bd6697e0); the HOLD did not mention it, an ADDENDUM was appended to the READY file. [4] FALSE: 'STUB should be STUB' is the same string |
| ks_1467_p1 | 8 (Major3/Minor3/Note2) | NO GO | R3 S2 F1 N0 U2 | 5/8 | 1.7 (101 s; 2 attempts) | 32870+2705 | [0] sibling pass (shared half is ks_1467_p2); [1] real and exactly the decision flagged in the READY note; [2] partly false: the operator measured the three ValidationError sites at source; [3] true (S1/S2 source-text); [7] true (lint not run by this harness) |
| ks_1467_p2_shared | 6 (Major3/Minor1/Note2) | NO GO | R3 S0 F2 N0 U1 | 5/6 | 0.7 (42 s) | 8044+1197 | [1] FALSE for this half: the `details` change is the AUTH half (auth errorHandler.ts:296 is the only `instanceof <ValidationError>` site in services/*/src at bd6697e0); [2] confuses the two halves; [0] general concern, no other instanceof site found |
| ks_1591_p1 | 6 (Major2/Minor2/Note2) | NO GO | R3 S2 F1 N0 U0 | 2/6 | 0.9 (51 s) | 11487+1241 | [0] sibling pass (requireKeyAdmin is ks_1591_p2) and Major is overstated; [1] reachability is stated unestablished in the ticket/READY note; [3] misreads: the fold touches a-z only, as the comment says |
| ks_1591_p2_security | 4 (Major2/Minor1/Note1) | NO GO | R1 S2 F1 N0 U0 | 3/4 | 1.1 (66 s) | 40147+846 | [0] sibling pass; [1] real and already in the READY note (R3 accepts 401 or 403) but Minor, not Major; [2] says 'this is fine' |
| ks_1776_p1 | 6 (Major3/Minor2/Note1) | NO GO | R1 S2 F0 N2 U1 | 0/6 | 1.0 (60 s) | 26435+1117 | [0],[2] design alternatives already listed in the READY decision note (test-mock fix, move seed out of module scope); not Major; [1] weak |
| ks_1779_p1 | 12 (Major0/Minor1/Note11) | GO | R4 S0 F0 N8 U0 | 6/12 | 1.3 (79 s) | 39055+1365 | verdict GO is right; 8 of 12 are non-findings (observations that nothing is wrong, 'PR description not provided') |
| ks_1780_p1 | 5 (Major2/Minor2/Note1) | NO GO | R1 S1 F0 N0 U3 | 2/5 | 0.7 (39 s) | 10291+981 | [0] sibling passes (adminConfig is p2, webhooks is p3) so 'unfixed sites' is by design but Major is overstated |
| ks_1780_p2_admin | 7 (Major2/Minor3/Note2) | NO GO | R0 S1 F1 N1 U4 | 2/7 | 1.5 (88 s) | 44151+1531 | [0] sibling passes; [1] FALSE: falling through to fail500 instead of hanging IS the fix |
| ks_1780_p3_webhooks | 5 (Major2/Minor2/Note1) | NO GO | R1 S2 F1 N0 U1 | 2/5 | 0.6 (33 s) | 8986+938 | [0],[1] sibling passes (systemErrors is p1, adminConfig is p2); [3] FALSE: 'Threw' vs 'Threw' is the same string |

### Totals (first pass, 23 diffs: the 16 held earlier + my 7, ks_1250_p1 via the bash variant)
- Requests: 23 diffs, 25 model calls (2 diffs needed a second attempt after a repetition abort); **wall-clock 21.4 min of model time (1283 s), 569215 prompt tokens, 26310 completion tokens**; per diff 24-119 s (median 44 s); prompt size 8-83 k tokens. 0 schema failures; the repetition guard fired on ks_1219_p1 and ks_1467_p1 (retried and valid).
- Findings: 131 in total ({'Note': 67, 'Major': 34, 'Minor': 30}); verdicts {'GO WITH NOTES': 8, 'NO GO': 14, 'GO': 1}. Quote check passed for 62/131 findings.
- My reading of the 131 findings: R 46, S 30, F 14, N 19, U 22. This is the operator's reading: the items I could settle from the READY notes, the golden tests and `git show`/`git grep` at the pin I marked; the rest are U (not checked), not counted as real or false.
- **New information the review produced (1 real):** ks_1250_p1 [0], confirmed at source: smoke-test.sh's full run (section 7 on) still hits hard-coded `localhost:60xx` ports, so SMOKE_BASE_URL makes only the gateway-based checks remote (lines 257-327 at bd6697e0). An ADDENDUM was appended to that READY file and to the raise brief.
- **What the Spark missed that a source read found (3):** ks_1240_p6 (the two tokenisation functions have no callers), ks_1240_p7 (`arrayBuffer()` outside the try, so a body stall is not the promised 503), ks_1240_p8 (a key-generation timeout yields a 201 key-less tenant). All three are things a diff-plus-full-file prompt can show; the Spark described the tests instead.
- **Failure patterns:** (1) when a ticket is split across sibling passes it calls the other half "unfixed" and labels it Major, contributing to NO GO on 14 of 23 diffs where I would put GO WITH NOTES or a decision; (2) it restates scope disclosures in the brief as defects ("the ticket asks for a 503"); (3) it pads with non-findings ("PR description not provided", "the comment is consistent", "the test count adds up") especially on a clean diff (ks_1779_p1: 8 of 12); (4) two invented typos ("Threw"/"Threw", "STUB"/"STUB") and two misreads of facts.json (ks_1197_p1 [3]); (5) it never once ran into the unreproducible part: it cannot see runtime, so every "tests are source-text only" is true but already disclosed. The strengths: it reads test code closely (mocked-abort tests, bound pinned only as <=30000/<=120000, 401-or-403 acceptance, brittle source-text pins were all true), and found one genuine miss in a HOLD.
- **Determinism (temperature 0 is not enough):** second runs of the same prompt gave different findings every time. Table (first run | second run):
| diff | run 1: findings / verdict / seconds | run 2: findings / verdict / seconds | identical claims | verdict |
|---|---|---|---|---|
| ks_1670_p1 | 4 / GO WITH NOTES / 44 s | 4 / GO WITH NOTES / 26 s | 0 | SAME |
| ks_1701_p1 | 4 / NO GO / 108 s | 7 / GO WITH NOTES / 33 s | 0 | FLIPPED |
| ks_1536_p1 | 4 / GO WITH NOTES / 32 s | 4 / NO GO / 35 s | 0 | FLIPPED |
| ks_1240_p4_social | 4 / GO WITH NOTES / 29 s | 8 / GO WITH NOTES / 38 s | 0 | SAME |
| ks_1240_p5_social2 | 6 / NO GO / 38 s | 6 / GO WITH NOTES / 30 s | 0 | FLIPPED |
| ks_1240_p6_tokenisation | 4 / GO WITH NOTES / 29 s | 4 / GO WITH NOTES / 22 s | 0 | SAME |
| ks_1240_p7_ipfs | 7 / GO WITH NOTES / 42 s | 5 / GO WITH NOTES / 32 s | 0 | SAME |
| ks_1240_p8_provisioning | 6 / GO WITH NOTES / 50 s | 4 / GO WITH NOTES / 22 s | 0 | SAME |
| ks_1197_p1 | 5 / NO GO / 37 s | 5 / NO GO / 30 s | 0 | SAME |
| ks_1219_p1 | 8 / GO WITH NOTES / 119 s | 3 / GO WITH NOTES / 21 s | 0 | SAME |
| ks_1240_p1 | 3 / GO WITH NOTES / 24 s | 4 / GO WITH NOTES / 18 s | 0 | SAME |
| ks_1240_p2_proxy_admin | 7 / NO GO / 88 s | 6 / NO GO / 35 s | 0 | SAME |
| ks_1240_p3_batch_audit | 5 / NO GO / 37 s | 6 / NO GO / 41 s | 0 | SAME |
| ks_1467_p1 | 8 / NO GO / 101 s | 5 / NO GO / 34 s | 0 | SAME |
| ks_1467_p2_shared | 6 / NO GO / 42 s | 5 / NO GO / 34 s | 0 | SAME |
| ks_1591_p1 | 6 / NO GO / 51 s | 5 / NO GO / 35 s | 0 | SAME |
| ks_1591_p2_security | 4 / NO GO / 66 s | 7 / NO GO / 46 s | 0 | SAME |
| ks_1776_p1 | 6 / NO GO / 60 s | 6 / NO GO / 36 s | 0 | SAME |
| ks_1779_p1 | 12 / GO / 79 s | 6 / GO WITH NOTES / 34 s | 0 | FLIPPED |
| ks_1780_p1 | 5 / NO GO / 39 s | 6 / GO WITH NOTES / 33 s | 0 | FLIPPED |
| ks_1780_p2_admin | 7 / NO GO / 88 s | 5 / NO GO / 36 s | 0 | SAME |
| ks_1780_p3_webhooks | 5 / NO GO / 33 s | 6 / NO GO / 41 s | 0 | SAME |
  Verdict flips: 5 of 22. Run 2 is faster (prefix cache: the 28-83 k-token prompt is the same), so wall-clock minutes above are cold-cache for run 1. Conclusion for the pilot: one Spark review is a sample, not a verdict; a gate that acted on its NO GO would have rejected 14 of 23 diffs that source reads held.

### Spark running, and the rebrief (the one allowed)
- Spark used continuously: first review began about 15 min into the job (16:05), reviews ran back to back 16:05-16:28 (driver pid 95727, exited), the rebrief round ran 16:29-16:32 (drainer pid 23151, exited), a determinism second pass followed (pids 26740 and 29315). Gaps: 16:28:11-16:28:50 (my launcher step), 16:32-16:34 (between the rebrief and the second pass); everything else was a request or a round in flight. Note: `spark_status.py` printed IDLE ("IDLE since last round N min ago") throughout the review runs, because a review is not a round and writes no round.lock until the Spark's own queue is used; it cannot see review traffic. Suggest it count a live `spark_review.py` process.
- **ks_1240_p9b_internal_loose (the one rebrief of ks_1240_p9_internal_loose; original + 1):** the brief now DICTATES the old-side hunk headers (`@@ -21,1` and `@@ -44,6`, with the context lines named). Queued, dry-run rc 0, CONTROL-PASS BYTE-IDENTICAL at bd6697e0, then the round: **PASS (7/7) 16:32:03, 164 s round, 50.2 s model, 12654+2026 tokens, golden DIFFERS (loose, expected), A2a ANCHOR OK: both old-side headers at their real lines (`-21,1`, `-44,6`)**. The original failed the same A2a leg three times (hunk 2 written at `-43`, real 44). The dictation fixed it. One residue: `apply_mode=reanchored`, i.e. the model's NEW-side start of hunk 2 (`+45`; it should be 44 + the 2 lines hunk 1 adds = `+46`) is still off by one, so a strict `git apply --check` of its patch would still fail and the checker rebuilt the hunk; dictating the new-side start as well would remove that. The patch is correct and minimal (constant `SECURITY_SERVICE_FETCH_TIMEOUT_MS = 10_000` below `SECURITY_SERVICE_URL`, one `signal:` line as the last property). NOT held (not asked for): Wednesday reads it; run dir `local-model/runs/spark_secuura_2026-10-28_ks_1240_p9b_internal_loose`. The result row is in `local-model/spark/done.md` (written by the drainer). The Spark's review of both p9 patches: GO WITH NOTES (3 and 4 Notes, all about the 10 s value and the mocked abort).

## JOB 3 - raise-seat brief (DRAFT, not sent, not launched)
Path: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-28_seatRaise_spark_held_passes.md`
Shape taken from `2026-10-23_seatG15_raise_1709_1622_and_ks1707.md` (BLUF / QUEUE / HOLDS / PARTITION / PROVENANCE / SELF-CHECK) and the WORK CLONE / per-PR proof sections of `2026-10-20_seatD26_raise_spark_screen21.md`. Per-PR file lists, READY names, canonical patch paths and the apply matrix were generated by script from the goldens and the checker artefacts, not typed.
- 18 PRs over the 23 passes in three waves; the only non-disjoint pair is **PR G (KS-1779, adminConfig.ts) then PR H2 (KS-1780 p2, adminConfig.ts)**, sequenced (H2 opens after G merges). Wave 1 (HOLD, no ruling): B (KS-1467 shared), A (KS-1591 both passes), D (KS-1670), F (KS-1536), E (KS-1250), H1 (KS-1780 p1+p3), G (KS-1779). Wave 2 (HOLD-WITH-DECISION): I, C, J, K, L, M, N, O, P, Q. Wave 3: H2.
- Every PR ends at READY FOR GATE, `Refs` never `Closes`; no merge without Wednesday's GO naming the head sha.
- Included as asked: the shared-inbox warning (Seat D 38th, pane %53, live on `secuura-blockchain@` deploying `bd6697e079fc` to the boxes, touches no code); the push-window `mkdir` lock (with the first-come `push_queue.sh` join, own-mkdir flag, the anchored pgrep, holder-then-rmdir release); the per-command ssh keepalive standing line (`GIT_SSH_COMMAND="$(git config --get core.sshCommand) -o ServerAliveInterval=15 -o ServerAliveCountMax=120" git push`, never in `.git/config`, `ls-remote` in the same action); and the rule that every Secuura test change updates BOTH `Projects Documents/*.html` docs in the same commit (repo skill `secuura-test-discipline` section 4, space in the path, docs-only conflicts resolved at the merge step).
- Path checks: every file granted or excluded was checked with `git cat-file -e bd6697e079fce41db6b21e094a9eddb3d0e1d08e:<path>` in the `op3-hold-1028` clone: 55 granted paths (32 exist at the pin, 23 are NEW test files and are listed as "absent at pin" on purpose), the 2 Projects Documents docs (exist), and 7 excluded/read-only paths (all exist). The first run of the check caught a wrong path I had typed for the hook (`Blockchain/Dev/.githooks/pre-push` does not exist; it is `.githooks/pre-push` at the repo root); fixed and rerun.
- **Open decisions (HOLD-WITH-DECISION), Wednesday rules before the PR opens; the brief decides none of them (13 passes in 10 PRs):**
  1. KS-1219 / PR I: JSON `null`/`0`/`false` scope now answers 400 (was: read as absent).
  2. KS-1467 auth / PR C: three weak-password 422s start carrying `error.details = { feedback }`; can feedback echo the candidate password?
  3. KS-1776 / PR J: product try/catch (drafter's shape) vs fix the offending test mock vs move the seed out of module scope.
  4. KS-1197 / PR K: consumer-side fix (enforcement.ts) vs validate the claim at the source; partial fix (verify-handler half not included).
  5. KS-1701 / PR L: access WIDENS (`SUPER_ADMIN` and mixed-case spellings become platform admin at four originate sites).
  6. KS-1240 gateway / PR M (3 passes): 5 s / 30 s / 120 s / 30 s timeout values; auth.ts answers 401 on timeout, not the ticket's 503; slow admin create or audit export now ends in 502.
  7. KS-1240 tokenisation / PR N: 10 s; the two functions have no callers at the pin (is a PR for unused code wanted?).
  8. KS-1240 social providers / PR O (2 passes): 10 s; 400 on the login callback, unclassified rejection on `POST /social/link`.
  9. KS-1240 ipfs / PR P: 60/15/30 s; scope extension; body stall not mapped to 503; large downloads fail after 30 s.
  10. KS-1240 provisioning / PR Q: a key-generation timeout creates an active key-less tenant (201, `keyFile: null`); 10 s; scope extension.
  Decision-free HOLDs that still need a sentence in the PR body (listed in the brief): PR D (Refs, source-text pin), PR F (groundwork, Refs KS-1536), PR A (R3 accepts 401 or 403), PR E (the localhost residue above), PR H2 (sequenced).
- UNMEASURED, said in the brief's provenance: Linear ticket states for the 14 tickets (the Spark builder required an open ticket at drafting time), and whether any seat is live on these files now beyond the 14 open PRs.
- Routing: you asked for row C2; the row that literally names "raise a held local PASS as a PR" is C1 (`fleet/specs/model-routing.md:91`), and the G 15th precedent cited C1 + C2. The receipt in the brief names C2 as commissioned and notes C1; Wednesday confirms.

## What I could not do, and why
- `spark_gate.sh` (the deterministic half of the gate) needs a PR number and refs/pull heads; no PR exists for a held pass, so the review facts were built from the checker's own artefacts. Lint is "not run" in every facts.json (a few Spark findings turn on that).
- I did not source-check every one of the 131 Spark findings; those marked U in the table were not checked (reasons: sibling-pass scope claims I settled from the READY notes, not file by file; style claims about test helpers I did not open).
- ks_1240_p9b was not held (not asked); no READY file was written for it.
- Linear states of the 14 tickets not read; the brief says so.
- The 15-minute Job 1 target: the seven holds were written 16:10-16:15 by the clock (reading and the overlap/apply checks ran in parallel with the first reviews); the first Spark review ran about 16:04.
- Cost: I cannot see a token counter from inside the session; the Spark side is exact (569 k prompt tokens, 26 k completion for the first pass).

## Files this operator wrote
`local-model/night/READY_KS-{1536,1701}-...`, `READY_KS-1240-...ks_1240_p{4_social,5_social2,6_tokenisation,7_ipfs,8_provisioning}...` (7 READY files, 2026-10-28); `READY_KS-1250-...` (ADDENDUM appended); `local-model/night/_quarantine_2026-10-28/` (1 stray READY, moved); `local-model/night/briefs/ks_1240_p9b_internal_loose/` (rebrief); `local-model/spark/queue.md` (1 comment + 1 line), `done.md` (the drainer's p9b row); `0_Brain/reference/2026-10-28_spark-operator3/` (this report and `reviews/<tag>/` and `reviews/<tag>_rerun/`); `fleet/briefs_staged/2026-10-28_seatRaise_spark_held_passes.md`. Clones: `local-model/spark/cache/work/op3-hold-1028`, `.../op3-review-1028` (kept; quarantine or remove at the next sweep). Nothing under `!CODING/`.

## Coordinator switch received at about 16:45 (Kam card wed-spark-drafting-cost-1028 = b, relayed by Wednesday)
Reviews completed BEFORE the switch: all 23 first-pass reviews (16 earlier-held + my 7; ks_1250_p1 via the bash variant), the 4 early determinism re-runs (ks_1701_p1, ks_1467_p1, ks_1219_p1, ks_1240_p4_social), the two p9/p9b reviews, and a second pass over the other 18 (see the determinism table; ks_1250_p1 has no re-run). The second pass was the only review work still in flight and has finished or is at its last diff.
NOT done: the new-brief batch ("6-10 briefs, at least 3 harder rungs, overlap check, dry-run, control, drainer"). Why: the generator the earlier operators used (scratchpad gen/mk.py, mk2.py, specM..T of session 154365ac) no longer exists on disk (only gen.py remains in that scratchpad), so a batch means rebuilding it first, and I would not start a half batch. The Spark is therefore idle from the end of the second review pass. Ready for the next operator: develop pin bd6697e0, the overlap script (scratchpad overlap.py logic: golden `+++ b/` headers vs `gh pr list --json files` vs the 55 held files), the open-PR list command, and the one-rebrief lesson (dictate BOTH old- and new-side hunk start lines for loose briefs).

## Spark state at the end (spark_status.py and tunnel.sh check, pasted)
```
SPARK: tunnel UP · queue 0 · drainer not running · round none · last ks_1240_p9b_internal_loose PASS 10-28 16:32
SPARK: ⚠ IDLE since last round 14 min ago — queue EMPTY — allocate a task NOW (rule 2026-10-28: never keep the Spark idle)
UP — http://127.0.0.1:47788/v1/models 200 (listener: ssh pid 52462 )
```
