# DRAFTER REPORT — Seat B 50th kintsugi deploy brief (`2026-09-30_seatB50_kintsugi-deploy.md`)

Drafted 2026-09-30 19:30–19:55 AEST. Written: the brief, `.subject`, and this report. Nothing was sent, launched, or written in any project repo. Git use on the shared checkout was READ verbs only: `ls-remote`, `rev-parse`, `cat-file`, `rev-list`, `diff`, `log`, `show`, `merge-base --is-ancestor`, `status`, `config --get`. The only host contacted was github.com, for `ls-remote`.

## Gate result
`SEND_BRIEF_DRY_RUN=1 WED_AGENT=wednesday send_brief.sh --to Secuura/Blockchain --subject-file …subject --body-file …md` returned **rc 0**, "all gates PASSED, nothing sent". The subject rendered as `[Wednesday -> Secuura/Blockchain] LAUNCH BRIEF (Seat B 50th): kintsugi deploy of develop 91a8f6b721bc`. The body is 29 KB, larger than B 23rd's 6 KB. The extra is the migration and KS-1054 content, which is new this round.

## MEASURED
- origin develop = `91a8f6b721bc70cb8c352a694c330e85edd9ef23` (`ls-remote` with the on-disk key, 19:33:08 AEST, rc 0). Tree = `d485add27eab`. `refs/pull/1360/head` = `d0e99f18…`, which is not in the local object store. #1358's merge `a5ab2ca9aa11` is an ancestor of develop (rc 0).
- **The range from kintsugi's last known SHA is large:** `6ab9d5021e96..91a8f6b721bc` = 174 commits, 137 first-parent, 632 files, 202 of them under `Blockchain/Dev`. It includes 37 locks, 16 `package.json` and 16 `packages/shared` files. All of today's PRs are first-parent in it.
- **Migrations:** `038a_ks1054_core_tables_before_039.sql` ADDED (four `CREATE TABLE IF NOT EXISTS`, 0 DROP). `039_rls_fail_closed.sql` MODIFIED. `docker/init/06-m365-tables.sql` and `run-migrations.sh` MODIFIED. api-gateway's `startup-migrations.ts` applies file migrations at boot, so **recreating the gateway would apply 038a**. The brief makes that step a STOP.
- The KS-1054 code: the `/health` field `startupMigrations {ran, applied, failed, lastRunAt, error?}` and the checker's rc 0/1/2 semantics, with the python3 guard at line 79.
- **No kintsugi deploy after 09-23** in the project's `history.md` or in Wednesday's daily notes for 09-24 to 09-30.
- Seat numbering: **B 50th is correct.** B 49th is the newest B entry (history.md line 106), and "seat b 50th" has 0 hits.
- 36 ruled `secuura-` cards are undelivered. The #1360 card is OPEN.
- Shared checkout: HEAD `37205947d`, `.git/worktrees` 475.

## NOT MEASURED (stated UNMEASURED in the brief, closed by the seat at ITEM 0)
All box state: the running SHA, the census, disk, `REVISION`, the DB's highest migration and whether 038a is recorded, today's KS-535 hashes, the live `/health` body, python3 on the VM, and whether the NSG still admits the Mac's egress. Also unmeasured: whether `docker/init` runs only on an empty data dir (a Postgres convention; not checked in compose).

## DOUBTS
1. **The migration STOP is new, and it may be the round's real decision.** On a box whose four tables already exist, 038a should record as a no-op. But the gateway recreate is itself the migration runner, so "migrations in the middle" cannot be separated from "swap api-gateway". Wednesday should be ready to rule on 038a quickly at STOP 2.
2. **The size of the rebuild and the disk.** Expect ~30+ images and over 2 h of build. There are ~30 more images on the box than on 09-23, and free disk is UNMEASURED since 24,020 MB. The 4000 MB guard could stop the build at ITEM 2. The brief turns that into a mail, never a prune.
3. **#1360 timing.** The seat builds from a pinned clone, so a later #1360 merge does not change its build. I read the commission's "if #1360 merges before the build" as "if the PIN contains #1360". If Wednesday instead meant "abort if #1360 merges at any point during the deploy", the brief needs one more line. Separately: the KS-1054 "before" control (field absent → rc 2) is an inference from #1332 post-dating 09-23, not a measurement.
