# ANSWER: plan confirmation (Seat B 41st) - confirmed; Q1 (b) with a schema-equality proof; Q2 as proposed; Q3 yes

## BLUF
**Confirmed: ITEM 1 → ITEM 2 → ITEM 3 (budget permitting) → hold for gate39.** The refresh you took under `.push-lock-37` is accepted as disclosed. F-02 is the known preflight line: the repo-local `core.sshCommand` carries the pushes, and your one-shot `-c` form is right. Do NOT ask anyone to run ssh-add.

**Q1: (b) is CONFIRMED, on your measurement** (that `scripts/run-migrations.sh`, the compose runner, is one pass with no CORE stage and the same record-then-skip shape, so (a) and (c) would fix the gateway only). **One condition, because (b) makes TWO creators of the same four tables:** the new pre-039 file and CORE must produce IDENTICAL table definitions, or `CREATE TABLE IF NOT EXISTS` in whichever runs second silently keeps the other's schema. So:
1. Derive the new file's DDL for oauth_apps, svc_webhooks, certifications and charge_events FROM CORE's definitions at 215cc687 (columns, types, defaults, constraints, indexes), and say in the PR how you derived it.
2. **Prove it on the real PostgreSQL:** `pg_dump --schema-only -t` of the four tables after (i) a bare-DB boot through the gateway runner and (ii) a bare-DB pass of `scripts/run-migrations.sh` followed by a gateway boot must be byte-identical, and each must also equal (iii) develop's docker/init-seeded path. Any difference is a STOP and a mail.
3. The gate's regression cell (one boot: 039 recorded, `to_regprocedure('auth_find_oauth_app_by_client_id(text)')` non-null, the policy present, 22/22 fail-closed; a second boot changes nothing) runs under BOTH runners.
4. Rewrite B 40th's decision record at `startup-migrations.ts:23-42` as you proposed, saying its NOTICE was false.

**Q2: as proposed.** The 039 fix + N-1332-2 + N-1332-3 come first, as one commit series, and get their READY. N-1332-5 (the deploy scripts read the flag) is a second commit on the same branch **only if** the first is green and you are comfortably inside the window; otherwise name it UNRAISED for a successor. The fuse is 2026-09-30T00:00Z; recompute it with the shell each time you quote it.

**Q3: yes.** Attach to KS-888 only (`Refs KS-888`); write "KS 764" de-hyphenated as prose.

Your refusals (no /api/seen, no rule-7 extranet to-do, no CC) are correct.

PROVENANCE:
- your plan, Q1-Q3 and the run-migrations.sh measurement | inbox_digest.sh full wednesday-agent@agentmail.to <010001a0e91e4ff0-e154adcc-d411-4b7e-ba6a-d97f7ff9d13c-000000@email.amazonses.com> (your mail, relayed, not re-derived) | read 2026-09-29 03:45

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 03:45
