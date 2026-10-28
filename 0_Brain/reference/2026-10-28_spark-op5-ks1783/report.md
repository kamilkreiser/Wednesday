# Spark operator 5 report - KS-1783 (3 cells), 2026-10-28 19:00-19:26 AEDT
Routing: claude-sonnet-5-5, Spark operator, wed-spark-drafting-cost-1028 = b. Base: develop bd6697e079fce41db6b21e094a9eddb3d0e1d08e (every line re-read there). Nothing pushed, no PR, nothing to Linear or mail. Tunnel: UP before round 1. Load: control runs ran at load1 3-6; my post-round test runs waited out one load1=17 reading (<=13 before running).

## KS-1783 scope (read-only GraphQL, key never printed; no comments on the ticket)
Quoted in each brief: "each takes its hash from a chainReply helper default (txHash: REAL_TX) and none of its assertions reads that hash" and "Facts only. No fix is proposed." NARROWING: the ticket proposes no fix and lists exactly these three cells, so each brief closes 1 of 3 and refs KS-1783 (does not close it). The ticket's own open question (do the two verify-file cells stay green under a placeholder default?) is answered below by measurement.

## Measurement answering "does the reply echo the hash?"
No. At tip the three cells themselves assert the ROUTE reply carries txHash null for a simulated reply (v2 :123, verify-route :111, verify-file :106) and those asserts pass, so the hash cannot be read from the response. The "reply hash" is the mocked anchoring reply object (chainReply output), as precedent :157-:159 / :171-:173 do (const reply = chainReply(...); expect(reply.txHash).toMatch(REAL_TX_SHAPE); callV2(reply)). All three were therefore briefable, as that shape. Each brief says so.

## Pipeline used (no new pipeline)
gen/mk_testonly.py with new specs gen/specAB.py (c1), specAC.py (c2), specAD.py (c3); tier test_only, tamper in the product (verificationV2.ts:240 / verification.ts:1267 /verify / verification.ts:724 /verify-file: "simulated: chain.simulated" -> "simulated: undefined"). One tooling change: mk_testonly.py now accepts a LIST of edits (several hunks) and per-spec hunk wording; backup gen/mk_testonly.py.pre-1028-op5. Briefs: night/briefs/ks_1783_c1_v2, ks_1783_c2_verify_route, ks_1783_c3_verify_file (KS-1783.md, golden.diff, spark.pins). Each brief: lint rc 0, dry-run OK with "prompt source: WEDNESDAY BRIEF", control PASS golden BYTE-IDENTICAL before queueing.
Brief defect found and fixed BEFORE any model round (control FAIL at A4, harness): the first c1 brief declared only one red cell; under the tamper FIVE cells of that file fail (placeholder RED, the RED edited, two N3, S1), and the checker refuses undeclared reds. Declared all five. Not a round (no model call).

## Per task
| task | briefable | rounds | verdict | wall-clock (round / model) | edits |
|---|---|---|---|---|---|
| 4 v2 chain-only (ks1634-v2-chain-only-match-carries-simulated.test.ts:117-125) | yes (hash read from the mocked reply, not the response) | 1 (no rebrief) | PASS 7/7 | 112 s / 31.1 s | 1 hunk at :118 -> 4 lines |
| 5 verify-route (...verified-by-hash-verify-route.test.ts:107-112) | yes | 1 | PASS 7/7 | 205 s / 38.8 s | 2 hunks: REAL_TX_SHAPE declared directly BEFORE REAL_TX (builder refuses an insertion with no trailing context, so not after), cell :108 |
| 6 verify-file (...verified-by-hash.test.ts:102-107) | yes | 1 | PASS 7/7 | 157 s / 38.5 s | same as 5 (declaration before REAL_TX at :44, cell :103) |
Counter: original only for all three; no rebrief used.

## Checker clauses 1-6 (checker.out + my own check)
1. Applies at known commit: PASS A2, strict git apply, tip bd6697e079fc (all three; also my own strict apply in scratch clones).
2. Added lines byte-identical to the brief: A3i/A3c PASS; plus my diff of +/- lines of patch.diff vs golden.diff identical for all three (golden verdict TREE-IDENTICAL: only hunk-header context differs, per done.md / hold_ready "bytes differ; applied result IDENTICAL").
3. Touched-file set exact: A3 test-only, exactly one test file each, product untouched (hold_ready product_unchanged=True; sha256 verificationV2 b426d2cb26566eaa, verification 8131c10bac13b44a).
4. New assertion RED on a deliberate break, GREEN restored: SEE THE CAVEAT. The checker's A4 PASS (5/10 red in c1, 2/6 in c2 and c3) proves the EDITED CELL still goes red under the product tamper; it cannot prove the new assertion, whose subject is test-local data (no product line can change chainReply's default). So I measured it by hand in scratch clones (script in session scratchpad, verify.sh): set chainReply's default txHash to a mock_tx_ placeholder.
   - c1: patched file: edited cell RED (and the 6 others that depend on the default); restored: 10/10 GREEN; UNPATCHED file under the same break: the edited cell stays GREEN (the ticket's gap, reproduced) while the N3 cells (already guarded) fail.
   - c2: patched under break: "RED KS-1628 L6 verify: simulated true with a real hash" fails; restored 6/6 GREEN; unpatched under break: that cell stays GREEN.
   - c3: same as c2 for the verify-file cell (patched fails, restored 6/6, unpatched stays green).
   This also answers the ticket's "Not established" for both verify files: yes, both cells stay green under a placeholder-shaped default without the fix.
5. Rest of the file's cells no worse: A5 GREEN-AFTER (10/10, 6/6, 6/6), A6 whole services/originate suite no new red (1698 -> 1698), A7 tsc rc 0.
6. Outputs kept: runs/spark_secuura_2026-10-28_ks_1783_c{1_v2,2_verify_route,3_verify_file} (plus -control dirs; c1 has -control FAIL and -control-r2 PASS, the FAIL is the red-cell declaration defect above).

## Held (READY, via night/hold_ready.py --model-tag spark-dsv4flash, golden = the control run)
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1783-KS-1783-ks_1783_c1_v2_spark-dsv4flash_BRIEFED-TESTONLY-VERIFICATIONV2-PASS-7of7_2026-10-28.diff.md
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1783-KS-1783-ks_1783_c2_verify_route_spark-dsv4flash_BRIEFED-TESTONLY-VERIFICATION-PASS-7of7_2026-10-28.diff.md
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1783-KS-1783-ks_1783_c3_verify_file_spark-dsv4flash_BRIEFED-TESTONLY-VERIFICATION-PASS-7of7_2026-10-28.diff.md
Canonical patches: runs/<run>/out.md.checker/patch.diff. Scratch clones (patched, for QA to look at): spark/cache/work/sparkop5-1028/c1, c2, c3 (plus scratch, unpatched). All three should be raised as ONE PR (three test files, same ticket, same shape), Refs KS-1783 only. The READY files do not mention the A4 caveat; the raise seat should read clause 4 above. One reading for QA: the PR is test-only, no product bytes.

## NOT tested
- No mutation beyond the placeholder default (e.g. a "tx_"-prefixed or short hash; the regex /^[0-9a-f]{64}$/ is the file's own).
- The three test files were not run on any branch other than the bd6697e079fc clone; open-PR file overlap (gen/overlap.py) was not run. Other lanes (lanes.md lane 26 item 1) may touch the same files: check before raising.
- jest ran only the single file in my scratch runs (whole suite only inside the checker's A6).
- Nothing run on a real stack or Postgres; the cells are in-process, mocked db/auth.
- The keepdraining.sh drainer (pid 97411) was already running from an earlier operator; I did not start or stop it.
