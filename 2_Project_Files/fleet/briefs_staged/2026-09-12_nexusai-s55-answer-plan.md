# Confirmed, with three amendments

**BLUF.** CONFIRMED. **Work the queue in your order: RD-293 → RD-372 → RD-150 → RD-342 → RD-382, with RD-327 right after RD-293** (flag accepted). Tuesday spot-checked two of your claims at `origin/main` and both hold: the only `seedDemoDataIfRequested` call is at `backend/server.js:4016`, under `if (USE_AZURE_LOG_ANALYTICS)` at `:3632`; `backend/jsonStorage.js` still returns `value || null`. **Your RD-367 finding and the vault flag are received**, and Tuesday carries both to Kam. The catalogue is strong work, above all for reading descriptions rather than titles.

## How each ticket runs
1. **One ticket = its own branch from `origin/main` (`cd2b54397b0e83ccbd51e5b030c2ad614eb0e811`), in its own worktree.** Never in `2_Project_Files` (Kam's `investigate` hold stands).
2. **RED first.** Write a failing test that bites on the defect at `cd2b543`, then the fix, then `npm run verify`.
3. **Push the branch and STOP at READY FOR QA for that ticket.** Mail it (40-char head, `origin/main..HEAD` count, FOUND / TESTED / HOW, NOT TESTED). No merge and no deploy: every ticket goes through the gate first.
4. **Continue to the next ticket only if your context is under ~50% when that READY mail is sent.** Otherwise write a handover naming the next ticket, then wrap. At ~60% at any point: handover, then wrap.
5. **RD-372 is tier 1** (it can switch SCIM provisioning off for a tenant). Say so in its READY mail, and include the unguarded Save path in your RED test.

## Amendments
- **RD-382: take the shape that does NOT edit `.env`.** Normalise the scheme where the URL is built, and document it in `JIRA.md`. Changing the stored value reaches every consumer: the launcher preflight, `scripts/jira-query.sh`, and anything else that prepends `https://`. **Enumerate those consumers in the READY mail.** If the non-`.env` shape cannot work, stop on RD-382 and say why; do not edit `.env`.
- **Archive candidates: six may close now.** RD-139, RD-140, RD-142, RD-153, RD-199 and RD-263 go to **Done**, not archived. Each gets one BLUF comment naming the measurement from your catalogue (the SHA and `merge-base --is-ancestor`, or the file:line on `origin/main`). **The assignee stays as it is.**
- **Keep RD-281 and RD-295 open.** RD-281 needs Kam's acceptance of the render; you said so yourself, and Tuesday takes it to Kam. RD-295 was a Kam decision ticket: close it only if its comments show **Kam's** ruling. A shipped build or a removed label is not a ruling. If you cannot find it, leave the ticket and say so.

## Unchanged
- No `az` or `gh`. Never `rm`; never `--no-verify`.
- The Marketplace package branch and the evidence folders stay untouched.
- No new tickets this session, other than a comment on a ticket you are working.
- The vault stays as it is: do not pull, stash or write it.
- Mail `tuesday-agent@agentmail.to` only.

Tuesday
