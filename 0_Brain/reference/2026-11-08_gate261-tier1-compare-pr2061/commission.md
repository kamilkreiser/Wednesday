# Gate 261, tier 1 COMPARE: PR 2061 (KS-1536 3b) after its develop merge-in, against gate 244's re-merge conditions. Launched 2026-11-08 by the 22:4x Wednesday seat

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. Pins, by Wednesday's `git ls-remote origin` at 23:23:19 AEDT: PR 2061 head 29a732c8e9367e6758663188580f08123a149196, develop abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82. Re-read both at start and end; if either moved, say so first. QA no-rm (clone at /private/tmp/g261, name its size); one clone; stop under 12 GiB free on DevMASTER; load1 under 8; never cd; /Volumes/DevMASTER/!CODING/ is read-only including its .git.

This is NOT a re-gate. Gate 244 gave GO WITH NOTES on PR 2060 and PR 2061 (old 2061 head edcb42e7ae99): /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate244-tier1-ks1536/verdict.md. Read it whole, especially section "The re-merge: compare, not re-gate, on conditions" (line ~108): it set FOUR conditions under which 3b's re-merge onto develop (now carrying PR 2060, merged as cfb6c1573ba9) is a compare only. The builder's READY (Seat Y 9th; its claims, not Wednesday's): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatY-9th/mail/out_03_ready_ks1536_3b.md, evidence under that folder's evidence/.

Questions:
1. Each of gate 244's four conditions: does it hold at the new head? Measure each yourself; for each, a control that would fail if the condition did not hold.
2. The merge-in commit itself (parents edcb42e7ae99 and cfb6c1573ba9): is the conflict on docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md resolved keeping BOTH 3a's and 3b's rows, with no other content change? Diff the head against a mechanical merge of its two parents and name every line that differs.
3. Develop has moved again to abd044f63a9d (PR 2058, 7 files): merge-tree of the head on the current develop, rc and tree; confirm PR 2058 shares no path with PR 2061.
4. The KS-1536 3b cells (users.ts, oauth.ts routes asking the shared isPlatformRole predicate) on the merged tree: run them, plus the 3a guard cells G1-G7 in packages/shared, with a planted defect per suite.
5. Open PRs 2075 (users.ts) and 2066 (the inventory doc, keyRevokePolicy.ts): merge-tree each against the new 2061 head; would landing 2061 first break either? (Wednesday holds both until 2061 lands.)

Verdict line 1: GO, GO WITH NOTES or NO GO. Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_gate261-tier1-compare-pr2061/verdict.md, with a NOT TESTED list. Findings only; post nothing.
