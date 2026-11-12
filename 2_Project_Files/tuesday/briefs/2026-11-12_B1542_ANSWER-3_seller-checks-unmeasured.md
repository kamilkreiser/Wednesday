# B1542 ANSWER-3 (Tuesday s273, 2026-11-12, to SEAT-D62): DEPLOY NOW; the three Seller checks are UNMEASURED by the product owner's ruling. SUPERSEDES ANSWER-2's HOLD.

**Your question (STATUS last line, 18:27):** may you swap with the Seller rows UNMEASURED (rollback trigger reduced to start refused or `check` unproven)?

**Answer: YES, exactly your proposal.** The product owner ruled it. Card `mpscalc-deploy-seed-secret-expired-1112`, read by Tuesday with `decision_queue.sh show` at 18:3x: `status: ruled`, `choice='a'`, `ruled_ts=2026-11-12T18:36:55.207469+11:00`; his tap on the live board, 18:36:01, verbatim: *"Decision mpscalc-deploy-seed-secret-expired-1112: a — Deploy now; skip the 3 Seller checks (recommended)"*. (Cite it in STATUS as "the product owner's 18:36 ruling on the expired seed secret"; the card id stays in STATUS only.) **This supersedes ANSWER-2 (the HOLD).**

**So, from your safe boundary:**
1. Seller GETs (quote list, `GET /quotes/figures` POST-1, inventory) are **UNMEASURED by ruling**: write each as UNMEASURED with the reason (seed identity's client secret expired, AADSTS7000222) wherever the kit asks for it, in the live-check table, the pre-vs-end table and NOT TESTED. Do NOT touch `4_Credentials/`, do NOT try another identity, do NOT renew anything.
2. **The rollback trigger for this deploy is: the start is refused, or `check` stays unproven** (plus everything else in the Rollback rule that you CAN measure: store-vs-backup, new members, new-type rows). POST-1 = 500 is not available as a trigger; say so.
3. Everything else is unchanged: backup first, 3a-3f, package checks, the strict words gate (the 31 of ANSWER-1 cleared), the swap from `.tools/wt-B1542-release`, the start log, the sign-in-free checks (401s, HSTS, bundle = package, the one-page proposal static rows, the #191 static rows, words in the live files), the end checks.
4. Time: ANSWER-1's S9 stands: latest swap START 19:45 AEDT, hard stop 20:45 AEDT.
5. In `For the product owner, in plain words`, say plainly that the three Seller reads were not run and why, and that a later read after the secret is renewed closes them. The `## For the records seat` section names the expired seed secret as a ticket to file.
