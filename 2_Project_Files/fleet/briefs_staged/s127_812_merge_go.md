## BLUF

**RE-GATE (4) PASSED (04:30:58Z) — GO: MERGE #812 @ `a5542df5a` TO DEVELOP NOW, as gated.** Wednesday's completion check against the commission (door 1: MFA + lockout on authorize; the pass-3 dispositions; Kam's REVERT ruling; KS-799/800/801 filed) is COMPLETE. Peter's review is not required by Kam's authorize-fix-now ruling. **Merge THE GATED SHA — no "small fixes" first: a gate is a claim about a SHA, and the follow-ups below go on the next branch.** Score for the #812 fix round: **0.90** (detail at the end). QA pass: 1.0.

## MERGE — conditions
1. Head re-read at the PUT: `a5542df5a` must still be `refs/pull/812/head` and the branch tip at origin (sha-asserted merge, the #807 pattern). Squash, subject names KS-781 door 1. Read `develop`'s new head back from `ls-remote` and report it.
2. **KS-781 stays In Progress** (door 1 of 3 — closes only on all three); comment: merge SHA, the four gates by report path, "door 1 of 3 merged; doors 2 (KS-795) and 3 (KS-796) follow". **KS-790 stays blocked** until KS-781 closes AND KS-797 (the open redirect carrying a code) merges — say so on KS-790 in one line.
3. **Then the rebases, in this order, each pushed and said on its ticket:** `ks-797` (your proven scratch rebase — now real; push the branch, open its PR, Peter requested with a one-line reason) → `ks-795` → `ks-796` (#812's suites must stay green under the split — you proved 32/381 for 797; prove the same shape for 795/796 and state the numbers). Mail Wednesday the three heads → Wednesday commissions the three gates, KS-797's first.

## THE GATE'S FINDINGS — dispositions (board writes now, code on the next branch)
- **Q4-1 (MAJOR, pre-existing, KS-801's mechanism):** the revert's 415 is walked around by `/API/oauth/authorize`. Do the two lines the tester asks for NOW: one line on KS-801 ("the #812 revert's benefit is contingent on this ticket"), and — on the NEXT branch, not #812 — the `FORM_ALLOWED_PATHS` comment naming KS-801 as the precondition.
- **Q4-2 (MAJOR, pre-existing):** WIDEN KS-800's text NOW to the measured corpus — `api-gateway/src/routes/admin.ts:535` handler-passed parser on 19 routes, 17 on proxyPaths where the gateway's parsers are skipped, NUL reaching the handler (D1/D1b) with the control D2; plus `mcp-server/src/http-server.ts:29` (a second unguarded service, outside the guard's `{index,app,server}.ts` corpus) and `routes/proxy.ts:836` (latent). KS-800 stays High and is next after the three rebases unless the category-1 read says otherwise.
- **Q4-3 / Q4-4 / Q4-5 / Q4-7 (Minor/Polish, all in #812's own tests):** ONE follow-up ticket, filed now, Medium, child of KS-781: restore the allow-set BOUND test (3 lines); make the revert-pinning test assert the 415 on a real `req.path`, not allow-set membership (it is load-bearing for a security decision); retitle/re-scope `ks781-n1-consent-form-round-trip.test.ts` to what it now proves (the auth service, not the page) and fix its line citation; widen the class guard's parser regex to `express.raw|text` and `bodyParser.*`. Small, one branch, gated once.
- **Q4-8 (originate 2 reds, IDENTICAL at the parent — not #812's):** own ticket now (Bug), naming the two `ks444-webhooks-create-description-guard` cases and the by-SHA isolation; check whether CI is green on develop for it and say.
- **Q4-6 (count 530 vs 532):** not a ticket — a rule for your wrap ritual: every count in a mail is copied from the runner's output line in the same action, never carried. Second time in four passes; the third gets a ledger row.

## SCORE — #812 fix round (s127): 0.90
Earned: both fixes real at the product path with the minter never called on a NUL scope; the class guard whose exact set reddens on a fourth site; the corpus self-correction 20→22 (reproduced by the tester by a different route); the reorder proven to move NOTHING else; three platform suites run green by the tester on your judgement, which held by diff; the revert pinned. Deductions: the allow-set bound test deleted without replacement; the pinning test on a fabricated path made load-bearing; a stated count not reconciled against the runner (second time).

PROVENANCE:
- PASS verdict, closure table, Q4-1…Q4-8, head a5542df5a unchanged at end of pass, tampers restored by md5 | `[QA -> Wednesday] KS-781 RE-GATE (4) @ a5542df5a (PR #812)` 2026-09-05T04:30:58Z; report `projects/secuura/reports/2026-09-05-s127-ks781-regate4-a5542df5a/report.md` — the tester's reads | read 2026-09-05 14:33
- Kam's authorize-fix-now ruling (2026-09-04 pickup) and REVERT ruling (13:12) | NEXT-PICKUP.md + the ruled card — Wednesday's project | read 2026-09-05 14:33
- KS-797 rebase proven clean 32/381 | your mail 2026-09-05T04:28:04Z | read 2026-09-05 14:33

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 14:33
(checked: "merge the gated SHA, follow-ups on the next branch" against the Minor findings in #812's own tests — consistent, they are filed not folded; "KS-790 stays blocked" against "door 1 merged" — the block names KS-781 whole and KS-797, stated; "Peter not required" against the HOLDS — Kam's ruling, spent.)
