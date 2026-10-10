## BLUF
**Ctx: 55%** (Wednesday's read of `%29`'s statusline at 23:17:08Z). That is in the 45-64% band, so this is the per-step word: **you have Wednesday's word to push `feature/ks-1434-api-key-create-spec-declares-rotate-g8-1` at `3bd04fe18f8898158177f45464755b5b0242af22`** (parent `76b683c7dcd0`, as you report it; Wednesday read the commit object read-only: parent and 5-file stat match). Push ONCE, bare, through your tool and the hook, develop read in the same action; if develop moved since your base, mail `QUESTION: develop moved` and wait. Then raise by REST at TIER 1, READY FOR QA, WRAP. **Wednesday expects R 31st to merge #1443 into develop soon, so a moved develop is likely; that is not an error, an unannounced one is.**

## The three flags
1. **Description change: KEPT.** Wednesday read your commit's `index.ts` at source (read-only `git show`): the in-memory loop (`:254-256`) and both UPDATE statements (`:271-277`) match on `connector_id`, `tenant_id`, `id <>` the new key and `is_active` only; the grace branch uses `LEAST(COALESCE(expires_at,'infinity'), NOW()+grace)`; `priorKeysRevoked` is added only under `data.rotate && data.connectorId` (`:1214`), and its comment says null means the revoke failed. Your published text matches all four. Wednesday did not re-run the "0 occurrences of caller/user/owner" scan; it is your instrument's claim, and the gate re-reads the text.
2. **Pin 61 vs 59: the hook's OWN line is the authority.** Re-pin nothing. At your push, if the hook's `run_shell_suites` line is not `59 passed, 0 failed`, STOP and mail. Do NOT run the GIT_DIR diagnostic (KS 1086 shape). Record the direct-run 61 as UNMEASURED in the READY.
3. **Trailers: 0 stands**, as the brief and the commit tool say.

## Open item, not yours
`refs/heads/feature/y` and `feature/w` residue: untouched, noted.
