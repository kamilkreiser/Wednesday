# Spark operator 67 report (2026-11-02): KS-1868 originate routes/signatories.ts + routes/thirdPartyVerifiers.ts

## BLUF
HELD, 4 of 4: O67-P1, O67-P2 (signatories.ts, 3 hunks each), O67-P3 (thirdPartyVerifiers.ts, 3 hunks), O67-P4 (thirdPartyVerifiers.ts, 2 hunks). All four: CONTROL-PASS, model round PASS 7/7 on the ORIGINAL brief, golden BYTE-IDENTICAL, strict=True. Inline guard from originate certifications.ts; no helper added.
SKIPPED (not briefed): signatories.ts :132 (POST nominate; `error.code === '23505'` check precedes the String(error)); thirdPartyVerifiers.ts :109 (POST /register, same code check); thirdPartyVerifiers.ts :193 (POST /:id/approve, issues an API key; out of scope per assignment). The remaining sites of both files (11) are all covered.
Tip: start 03977e89a343ad7362760e4fb0270602fb6da5ce (tip_start.out). The harness ran at cde2dee4dffb (develop moved when PR 1910 merged: diff 03977e89..cde2dee4 touches only mcp-server, tip_move_diffstat.out; both my product files byte-identical, checked with cmp). End: c8d77dce07dc502164de3325b1430e1f68016eb2 (tip_end.out); I did not re-diff my two files against c8d77dce (UNMEASURED; the harness A2a anchors passed at cde2dee4). Open-PR scan start and end: 22 PRs / 125 files, no PR lists signatories.ts, thirdPartyVerifiers.ts or any signator/third-party test; planted control services/originate = 6 entries both times (prscan_start.out, prscan_end.out; end scan shows new KS-1868 PRs 1912, 1913, none on originate).

## Control failures (my defects, not the model's) - answer to the coordinator note
The first four controls (09:15 to 09:22) all CONTROL-FAIL with golden byte-identical. Read the checker output (ctl_p*_checker.out) before assuming the shared-mock cause: it was NOT the @secuura/shared mock (these routes do not import shared). Two causes, both in my generated test:
1. P1 and P2: `const ORG` declared but unused, TS6133 (noUnusedLocals) = load error, A4/A5/A6 FAIL.
2. P3 and P4 (ORG already fixed): A4 "red but NOT for the right reason": my brief lacked the `## Red cells` list lines (`- RED ks1868 R1` / `- RED ks1868 R2`) that operator 66's brief has, so the checker treated the R cells as control cells. Added the two lines.
Fixed the generator (gen/mk67.py), regenerated all four, re-linted, re-queued controls; all four CONTROL-PASS. These were golden/brief defects found by controls, not model rebriefs: no model round was queued before a CONTROL-PASS; no pass needed a rebrief.
Also fixed before the re-run: P1 had no row with a `payload`, which gave TS2339 on `c.payload`; every row now carries `payload: undefined` or a body.
I built a scratch jest rig (scratchpad w2, copy of originate with the Dev node_modules and a ts-jest tsconfig that sees @types) and ran each golden: after the product patch all cells green (12/12, 12/12, 12/12, 8/8); with the product reverted only the R cells fail (6, 6, 6, 4): local_p*_green.out / local_p*_red.out. This is not the harness clone; the harness numbers below are what count.

## Per site: today vs after (all sites: `logger.error(ctx, { error: String(error) })` then a constant 500, no other catch work)
For a revoked Proxy or an Error whose `message` getter throws, `String(error)` throws INSIDE the catch. Today: nothing logged, the async handler rejects, the client gets no answer (gateway timeout). After: logged `unreadable thrown value`, constant 500. Ordinary Error today: logged `Error: <msg>`, constant 500 (unchanged after). The after-state for an unreadable value equals the ordinary-Error state. Persisted state: none of these catches write; the DB statement had already rejected, so created/updated/revoked/approved state is decided by the DB call alone and is identical before and after in every case. Nothing changes what is returned to a client other than turning a hang into the same constant 500.
Signatories (P1) :181 list, :236 check (the 500 body carries no `authorised`; same for any value after), :284 get-by-id. (P2) :357 PATCH update, :415 revoke, :464 reinstate.
Verifiers (P3) :143 list, :240 suspend, :279 reinstate. (P4) :365 POST /verify (the stand-in rejects the API-key SELECT, so the INSERT of a verification record is never reached), :397 records.
Trust-record test applied: none of the 11 fixed sites differs from the ordinary-Error path in whether a signatory/verifier is created, approved, revoked, suspended, reinstated or returned. SKIPs above are for the reasons stated (code check first; key issuance).

## Held files (ls night | grep O67; held_files.txt)
- READY_KS-1868-KS-1868-O67-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-O67-p1-PASS-7of7_2026-11-02.diff.md
- READY_KS-1868-KS-1868-O67-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-O67-p2-PASS-7of7_2026-11-02.diff.md
- READY_KS-1868-KS-1868-O67-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-O67-p3-PASS-7of7_2026-11-02.diff.md
- READY_KS-1868-KS-1868-O67-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-O67-p4-PASS-7of7_2026-11-02.diff.md

## Per pass
hold_ready lines (hold_p*.log), verbatim:
- P1: `golden: BYTE-IDENTICAL; touched=2 product_plus=21 product_minus=3 red=6/12 green=12/12 suite=1999->2011 strict=True`
- P2: identical numbers (red=6/12 green=12/12 suite=1999->2011 strict=True)
- P3: identical numbers (red=6/12 green=12/12 suite=1999->2011 strict=True)
- P4: `golden: BYTE-IDENTICAL; touched=2 product_plus=14 product_minus=2 red=4/8 green=8/8 suite=1999->2007 strict=True`
Callers: all are Express routes mounted under originate (`/api/signatories`, `/api/third-party-verifiers`), reached via the api-gateway; `git grep` of callers was not run separately (UNMEASURED beyond the mount names in the briefs' own text).
BEHAVIOUR CHANGE text for the PR (all four): "For an unreadable thrown value from the database only, today the catch throws, nothing is logged and the request gets no answer (the handler rejects; the gateway times out); after, the constant reason `unreadable thrown value` is logged and the constant 500 is answered, exactly what an ordinary Error already gets. No response, status or log for an ordinary Error or a string changes. Persisted state: unchanged." P3 and P4 add: "The /:id/approve (API key issuance) and /register catches are not touched." Refs KS-1868 only.
Recommended tier: P1 read-only routes lowest risk; P2, P3 admin writes (log + constant 500 only) and P4 medium by file class, but the diff is catch-only and the response is unchanged: suggest the same tier as operator 63/66 originate passes (small, QA-gated).

## Raise-seat notes
strict=True for all four. Test names start `RED ks1868 R1/R2 <route>` and `control ks1868 C1/C2 <route>`. Test files: ks1868-signatories-read-routes-p1-..., ks1868-signatories-write-routes-p2-..., ks1868-third-party-verifiers-admin-routes-p3-..., ks1868-third-party-verifiers-verify-routes-p4-... (all `-unreadable-throw.test.ts`). Hunk distances: signatories P1 hunks 181/236/284 and P2 hunks 357/415/464; P1 and P2 are in the same file and disjoint (nearest pair 284 and 357, 73 lines apart), so one PR or two both apply. Likewise P3 (143/240/279) and P4 (365/397) in thirdPartyVerifiers.ts; nearest pair 279 and 365. Within a pass the closest pair is 32 lines (P4). The old `ks593-signatories-refuses-a-non-uuid-id` test sits beside these and is unaffected (whole suite green in the harness).
Trap (from operator 63): jest run directly in the spark cache clone is red from a stale @secuura/shared build; use the harness numbers.

## Round log (done.md rows)
Controls (first set, failed): 09:15:35 P1, 09:17:26 P2, 09:18:58 P3, 09:22:00 P4 all CONTROL-FAIL.
Controls queued again 09:17:56 (P1), 09:22:17 (P2,P3,P4); CONTROL-PASS 09:32:16 P1, 09:35:06 P2, 09:37:45 P3, 09:39:51 P4.
Model rounds queued 09:32:27 (P1), 09:35:21 (P2), 09:37:55 (P3), 09:40:00 (P4). PASS (7/7): 09:48:26 P1 (182 s, 56.11 s model), 09:52:05 P2 (218 s, 56.193 s), 09:55:23 P3 (197 s, 54.871 s), 09:58:24 P4 (181 s, 50.646 s). All BYTE-IDENTICAL. done_rows.txt.

## UNMEASURED
Whether a real path throws such a value; real Postgres (stand-in only); other callers; my two files against c8d77dce (end tip); tsc/eslint outside the checker (checker tsc rc 0 per round); the orphaned p2 control rounds that ran on the stale brief were not otherwise analysed.
