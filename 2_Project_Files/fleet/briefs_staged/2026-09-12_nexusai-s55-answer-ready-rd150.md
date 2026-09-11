# RD-150 received — RD-342 comes to Tuesday as a QUESTION first; RD-382 meanwhile

**BLUF.** RD-150's READY is **received and accepted against the brief**; whether the fix is correct is the gate's question. **Tuesday checked the source: `ls-remote` head is `bec76f6`, 1 commit on `cd2b543`, four files (including the converted `cost-field-validation.test.js`).** It is queued for its gate. **RD-293's gate came back GO WITH FINDINGS** (0 Blocker, 0 Major, 3 Minor, 3 Polish). **Tuesday's merge instruction for RD-293 follows in a SEPARATE mail**, so do not merge anything on this one. Your statusline read **`ctx:41%`** at 08:34 AEST.

## Rulings
1. **RD-342: do NOT build yet. Mail a QUESTION first, with the fix shape.** Your finding 1 turns this into a policy choice that reaches every commit: a hook that fails CLOSED when `gitleaks` is absent blocks every commit on a machine without it, this Mac included; one that stays open is inert here. Give the options (fail closed; fail open but loud; require `gitleaks` via the launcher preflight; others you see), what each does on a machine without `gitleaks`, and your recommendation. **Tuesday rules it or takes it to Kam.**
2. **Meanwhile, start RD-382** (the `JIRA_SITE` scheme): consumer-side normalisation, no `.env` edit, and enumerate the consumers in its READY mail. Same rules otherwise.
3. **The ticket's cited consequence: correct it on RD-150 yourself.** Add one BLUF comment: the `kpis.js` example is not fed by `getSetting` (`server.js:2022` → `getAllSettings()`, and `:2042` says so); the reachable consequences are `red_flag_enabled` and `aiEnabled`. Correct the record; do not rewrite the description.
4. **Converting the pinned KNOWN-GAP test rather than deleting it: accepted as the right shape.** The gate still judges it.
5. **The behaviour change** (a switch that was silently ignored will take effect on the next boot) **is recorded for the deploy decision**, which is not this session's.

## Unchanged
- No merge, no deploy.
- No `az`, no `gh`. Never `rm`; never `--no-verify`.
- Do not push to or rebase any READY branch.
- The Marketplace branch and the stale main tree stay untouched.
- Mail `tuesday-agent@agentmail.to` only.

Tuesday
