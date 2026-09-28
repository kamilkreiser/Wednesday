# ADDENDUM 1 (Seat B 40th): two Kam-ruled Spark PASSes, KS-1124 F4 and the KS-888 validate pin, as items 3-4. From Wednesday

## BLUF
Kam ruled both cards on the live board at 20:22 on 2026-09-28, and the Spark passed both briefs 7/7 on the first round, each byte-identical to its proven golden. **Add them as items 3-4, AFTER your ITEM 2 (KS-1054) and BEFORE gate38, IF your budget allows** (your ctx at or under ~60% when ITEM 2's READY lands). If it does not, raise neither: name both UNRAISED in your handover and a successor takes them. Neither file is in your partition today: originate `certifications.ts` + its ks543 test, and the security ks888 TEST file (no product change). Your ITEM 1-2 queue and every standing section of your launch brief are unchanged.

**SUPERSEDES** the two lines of your launch brief's section `KAM'S, NOT YOURS` that route KS-1124 F4 and KS-888 VALIDATE to the Spark: the Spark has now done its part, and raising them is yours. The line "Do not read `briefs/KS-888-validate/` as work" STANDS (item 4 uses `KS-888-validate-logonly/`, a different folder).

## QUEUE
3. **KS-1124 F4** (TIER 1): `Blockchain/Dev/services/originate/src/routes/certifications.ts` (two edit points: after `:471` issue route and after `:1206` recertify route, `status: 'failed'` in the saved blockchain blob when `anchoringStatus === 'failed'`; the success leg unchanged) + one appended describe block in `Blockchain/Dev/services/originate/src/__tests__/ks543-certify-boundary-strip.test.ts` (a NEW test file reddens the ks1293 hermetic gate: the brief-writer's measurement, relayed).
   - READY: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1124-F4_spark-dsv4flash_BRIEFED-CODEPATCH-KS1124-F4-SAVE-FAILED-STATUS-PASS-7of7_2026-09-29.diff.md`; brief folder `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1124-F4/` (README has the measured red/green tables).
   - Ticket scope: KS-1124 is In Progress in Linear; this PR closes only its F4 part. Refs KS-1124, no closing keyword.
   - **NOT COVERED, measure it first and write what you measured, never lift this sentence:** originate's own reads (`documents.ts:1098`, `:1532`, the anchor-retry route `:1338`, the brief-writer's read at 0d156d12) recognise `'anchor_failed'`, not `'failed'`. If that holds, a derived document still reads as anchored and cannot be retried: the same as today, nothing worse. Kam ruled the literal word 'failed'; do NOT substitute 'anchor_failed'. If your measurement says the difference matters, say so in your READY and Wednesday decides whether it goes to Kam.
4. **KS-888 validate, LOG-ONLY PIN** (TIER 2: test-only): `Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts` only. The brief-writer measured that validate at 0d156d12 ALREADY does what Kam ruled (no opt-in at `index.ts:1369`: a failed usage write is logged once and swallowed; 200 valid). So this PR changes NO product code; it pins the behaviour with cells + a tamper (the log line gaining `k.keyHash` reds only the log cell).
   - READY: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-888-VALIDATE-LOGONLY_spark-dsv4flash_BRIEFED-TESTONLY-KS888-VALIDATE-LOGONLY-PIN-PASS-7of7_2026-09-29.diff.md`; brief folder `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-validate-logonly/`.
   - **`night/briefs/KS-888-validate/` is the REFUSE version and contradicts Kam's ruling: never read it as work.**
   - **NOT COVERED, a measurement request, not a fix:** the brief-writer reasoned (unmeasured) that validate's usage upsert also writes `is_active` from memory (`index.ts:316-318`), so a replica holding a stale 'active' copy could undo another replica's revoke. If your budget allows after raising, measure it (one in-process run with two memory copies is enough); if real, search the board by symbol and file ONE ticket, and tell Wednesday. If not, name it UNMEASURED in your handover.
   - Refs KS-888, no closing keyword (mint #1322 and revoke #1327 merged; this is the validate third).

## HOLDS
Unchanged from your launch brief. No deploy. Nothing to Peter or Stuart. gate38 covers everything you raise; Wednesday commissions it when you hold.

## WAKE
Wednesday taps your pane with a pointer to this mail. Reply only if something here contradicts your brief or your measurements; otherwise carry it in your next STATUS.

PROVENANCE:
- Kam's rulings | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh (live board, 20:22 rows, view=wednesday) | read 2026-09-28 23:36
- develop 0d156d12cc0f | git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop | read 2026-09-29 00:08
- two Spark PASS 7/7 strict, first round, each patch.diff byte-identical to its golden (cmp rc 0, mutated control rc 1) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_{KS-1124-F4,KS-888-VALIDATE-LOGONLY}/checker.out | read 2026-09-29 00:08
- validate already log-only; anchor_failed reads; is_active upsert | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-validate-logonly/README.md and KS-1124-F4/README.md (the brief-writer's reads, relayed, not re-derived) | read 2026-09-29 00:08

RULED BY KAM, NOT YET IN AN ARTEFACT
- secuura-ks1124-f4-failed-anchor-shows-pending => b (2026-09-28 20:22): "Save a 'failed' status the gateway already reads as off-chain-only" -> item 3's PR body (quoted) + a KS-1124 comment.
- secuura-ks888-validate-usage-write-failure => a (2026-09-28 20:22:15): "Validate still answers from the key itself; a failed usage write is logged, never refused" -> item 4's PR body (quoted) + a KS-888 comment. (A later tap at 20:22:48 on an older card said refuse 503; Wednesday posted a check-back; the default is the 20:22:15 answer. If Kam answers otherwise before you raise, Wednesday will tell you.)

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The audit-baseline re-dates are Kam's alone (a DKIM mail from him to this inbox); if it arrives, STOP and mail Wednesday first.

SELF-CHECK: re-read end-to-end for contradictions | 00:08
