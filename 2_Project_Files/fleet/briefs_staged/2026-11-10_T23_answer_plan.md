Seat T 23rd

ANSWER: plan CONFIRMED, and O-1 RULED AS YOU PROPOSE (Seat T 23rd). Part 1 is released.

O-1 (Wednesday's ruling, inside Kam's card secuura-ks1991-verify-presents-later-copy-fix-1110 = a, under his 2026-10-27 grant "I am happy for you to make the call"): registration is AWAITED and never swallowed. registerInPlatformRegistry REJECTS on failure, and the caller catches it. On a failure the create still answers 201 with the body unchanged, and logs at ERROR with the stable code 'KS-1991 REGISTRY_WRITE_FAILED' (document id and tenant id only). The idempotent re-POST path (respondForExisting) runs the same awaited registration before its 200, so every retry heals. The backfill covers anything left. Why this is inside the card and not wider than it: the card's words are 'stops being fire-and-forget', and an awaited call whose failure is surfaced and healed by retry is exactly not fire-and-forget. Your measurement (an autocommit INSERT committed before registration, the registry in another database, a rollback being a DELETE, and an error answer leaving a saved document never anchored) shows a failing create would be worse and would itself need Kam's card. The PR body states this reasoning in two sentences, with the stable code, and says the backfill is the repair for rows already missing.

RULINGS ON YOUR NOTES:
1. O-6 LEAST on the live path: CONFIRMED. It moves an existing row's created_at only EARLIER, only when the same (hash, tenant) registers again, and blanks or drops nothing; row C4 does not apply. O-7 (the backfill never UPDATEs an existing row) still binds the BACKFILL. Keep that line in the PR body so the two are not confused.
2. The Part 3 mutants: your replacements (a) to (d) plus one sensitivity mutant per rank site (verification.ts:611, :788, verificationV2.ts:330), each scored by a named cell, are ACCEPTED in place of the brief's three. Say so in the READY.
3. O-2 to O-5, as you read them: CONFIRMED. The script is Blockchain/Dev/scripts/backfill-platform-registry.js (dry run by default, --apply to write, functions exported for the cells). O-3: the stored value verbatim, with 'already registered' matching both forms. O-4: erased (metadata anonymized), deleted and empty-hash excluded; revoked IN. O-5: no; the certification path is a follow-up candidate, named in the READY.
4. 74 open PRs: noted; the census at your push decides.
5. Preflight [F-02] and [KS-907]: no action. Reads work through the repo-local core.sshCommand; never seed the keychain or set SECUURA_ALLOW_ONDISK_KEY; a refused fetch or push in your own clone is a STOP of git and a QUESTION.
6. HOLDS unchanged: the backfill runs on no box; demo FROZEN; the PR body's 'The backfill is not run by this PR' section is mandatory.

Wednesday
