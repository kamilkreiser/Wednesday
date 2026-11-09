Seat G 32nd

ANSWER: gate 292 returned 'PR 2138: GO WITH NOTES'. Read the verdict whole: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate292-tier1-pr2138-ks590/verdict.md. The code holds on every v1 and v2 verify path. Same-tenant callers lose no field that comes from a database row. 16 of 23 cells were red on develop as declared, the 10 mutants are exact, the whole suite is green, and the KS 1114 T9 golden passes 17 of 17 on a local PostgreSQL 15 with a planted control. Good work.

FIX ROUND 1 of 2, on this security surface, as a NEW commit on the PR's branch (never force, never rebase):
1. G292-2 (test gap): add a cell that kills the gate's gap-1 mutant. The mutant keeps certifierOrganizationId when no certifier NAME is present. Real chain metadata carries the org id without a name, and every fixture carries a name. The new cell must be red under that mutant and green at the fix.
2. G292-3 (test gaps): add cells pinning (a) verify-file's chain-first answer for a caller WITH a tenant (the gate's probe mutant survives today) and (b) v2's cross-tenant organisation id (the gate's probe fails on develop and passes at the head). Each cell is red on develop or under its named mutant, declared before running.
3. G292-1 (wording): the PR body, the code comment at verification.ts:458-461, the flow fragment and your ticket comment 845cb0df credit migration 039's RLS. The real guarantee is migration 011 (documents.tenant_id NOT NULL; the gate measured it with a null insert refused and a control accepted). Correct all four to name 011. Edit the ticket comment in place and say it was edited; do not stack a new one.
4. G292-5 (Info): if the openapi fieldsWithheld description sits in a file you already touch, reword it so it also covers chain-only matches (no registration). If it is in a file outside your scope, leave it, and say so in the READY.
HOLD on G292-4: the chain-first and v2 chain-only answers withhold the issuer, certifier, org id and on-chain metadata from EVERY caller, logged-in ones included. Kam's card says 'from an anonymous verify'. Do NOT change that behaviour in this round. It goes to Kam as a card now. If he narrows it, that is round 2 of 2; otherwise it ships as built.
Census before the push; the per-push grant shape is as before. Red-first predictions are declared before running. READY FOR GATE names round 1 of 2 and the delta from d769c05d0a9b.

Wednesday
