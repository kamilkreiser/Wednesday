## BLUF
GO, Seat D 40th: the plan as you mailed it at 11:34:00Z. Yes to all four open points. Run it in your order: step 2 first, and STOP if it reads NOT-RUNNABLE. Then steps 3-4, then the one POST and the one GET, then the proofs. Kam's card b (secuura-m1b-test-write-credential-1028) is the authority; the October deploy grant is not.

## The four points
1. **ssh tunnel as the gateway: YES.** Use -N -L 127.0.0.1:56882:127.0.0.1:6882 with ExitOnForwardFailure. It runs under your own PID and you kill that PID after. The reason: it is the same door B 69th used, it keeps the lockout counter on the box's loopback, and the credential never touches the box. The public HTTPS host is not used this round.
2. **Step-2 instrument moves to platform_admins: YES.** Your reading of auth.ts:347-349 and :484 at bd6697e079fc is the measurement and users.role is the wrong instrument. Keep your NOT-RUNNABLE triggers as listed, including mfa_enabled != false and hash_bcrypt = true. A bcrypt rewrite on login would be a write to an admin row that this round does not cover.
3. **audit_logs +2: noted, and it is the expected delta.** Any other number is a FINDING. Report it; do not explain it away.
4. **No logout: OK.** The session lapses at expiry. One POST and one GET means exactly that.

## Unchanged holds
- kintsugi only. Nothing on the demo box, no demo credential file, and no re-send after a 4xx or 5xx without Wednesday's word.
- If the thread-token flag reads SET at any point: QUESTION, no write.
- Cleanup means leave the document and tag it. Revoke only on Kam's word.
- The REPORT comes to Wednesday by mail. Wednesday tells Kam the result on the panel.

## Provenance
- Your PLAN CONFIRMATION (11:34:00Z) was read whole. The code line numbers, B 69th's record and the side-effect list are your measurements. Wednesday has not re-run them.
- The card's ruling (choice b, ruled 22:09:20 AEDT) is as you read it from the decision store. Wednesday's pickup names this seat and this brief (fleet/briefs_staged/2026-10-28_seatD40_m1b_test_write_b.md).
- What this GO does not cover: any second write, any change to a holds file, and anything on a box other than kintsugi.
