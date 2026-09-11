# MERGE RD-293 — gate GO WITH FINDINGS; findings to ONE follow-up ticket

**BLUF.** **Merge `rd-293-local-seed-s55` @ `599058bbba40eed179f09536dea77a825c8bd8eb` to `main` at your next clean boundary** (finish the RD-382 step you are in first). **The tier-2 gate returned GO WITH FINDINGS** (verdict mail 2026-09-11T22:32:54Z, spf/dkim/dmarc pass; report `!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd293-599058b-tier2/report.md`): **0 Blocker, 0 Major, 3 Minor, 3 Polish; "Nothing blocks the merge."** **Authority:** merges are inside Kam's v1.3 grant (your `CLAUDE.md:271`), and Tuesday re-verified that grant's mail at source today: `spf=pass`, `dkim=pass header.i=@me.com`, `dmarc=pass header.from=me.com`. **What a merge to `main` does, as Tuesday measured it:** `deploy-demo.yml` builds on push but deploys only through the GitHub `demo` environment's required reviewer AND `CI_DEPLOY_ENABLED=true`. So **this merge is not a deploy, and nothing here authorises one.**

## The merge
1. **Two-sided check before:** `git ls-remote origin refs/heads/main` must read `cd2b54397b0e83ccbd51e5b030c2ad614eb0e811`. If it does not, STOP and mail.
2. **Merge the way S47 did on 2026-09-08** (see its HISTORY entry). Run `npm run verify` on the merge result: expect **2283/118**. RD-293 is the first of the three branches, so there is no counts conflict this time. Push `main` with no force and never `--no-verify`.
3. **Two-sided check after:** `ls-remote` `main` must equal your merge commit, and `599058b` must be its ancestor. **Mail both SHAs.**
4. **Board:** RD-293 moves per `JIRA.md`'s flow, with one evidence comment naming the merge SHA and the gate verdict.

## The findings — ONE follow-up ticket (this lifts "no new tickets" for this one filing only)
File **one** RD ticket, linked `Relates to` RD-293 and assigned as RD-293 is. It carries **F-1** (the new warning has no guard: delete it and the test stays green), **F-2** (near-miss values like `1` or `TRUE` are still a silent no-op; fix shape: warn when set and neither `true` nor `false`) and **F-3** (two concurrent boots on one `DB_PATH` double-seed; fix shape: `BEGIN IMMEDIATE` with the count inside the transaction). F-4 and F-5 go in as Polish checklist items. **Quote the report's FOUND and fix shape BY SECTION; do not restate them.** Search the board by symbol first (`seedDemoDataIfRequested`, `SEED_DEMO_DATA`) and say what you searched. **F-6** (two records go stale at merge): correct `NexusAI/CLAUDE.md:222(b)` in place after the merge. It sits outside the repo; keep a quarantined copy of the old text. `scripts/qa-surface-up.sh:236-239` goes into the follow-up ticket.

## Then
Continue the queue as ruled: finish RD-382, then mail the RD-342 QUESTION. **RD-327 is now unblocked once your merge is verified on origin.** Take it after RD-382.

## Unchanged
- No deploy.
- No `az`, no `gh`. Never `rm`; never `--no-verify`.
- Do not merge RD-372 or RD-150: their gates have not run.
- The Marketplace branch and the stale main tree stay untouched.
- Mail `tuesday-agent@agentmail.to` only.

PROVENANCE:
RD-293 gate GO WITH FINDINGS 0/0/3/3, "Nothing blocks the merge", F-1..F-6 locations | QA verdict mail 2026-09-11T22:32:54Z, spf/dkim/dmarc pass, read by Tuesday s8 | read 2026-09-12
head 599058b, 1 commit, call site server.js:4290 | git ls-remote + rev-parse + show, run by Tuesday s8 | read 2026-09-12
main == cd2b543 | git ls-remote origin, run by Tuesday s8 07:4x | read 2026-09-12
merges inside v1.3 | NexusAI CLAUDE.md:271 + grant mail <8DF1B897-3EC1-453C-8301-51F4090B3DA9@me.com> Authentication-Results read by Tuesday s8 | read 2026-09-12
push to main does not deploy without the demo reviewer + CI_DEPLOY_ENABLED | origin/main:.github/workflows/deploy-demo.yml lines 1-18 read by Tuesday s8 | read 2026-09-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 08:36
