# B437 drafter report (read-only; two files written)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B437_SEAT-D25_hpsmpoc-uat-redeploy-badge.md` (about 70 lines). Slots: `@STAMP@` x4 (stamp time, launch authority, hard stop, final READ-WHOLE line). Fill them all before launch.

## Read whole
B410 brief, B410 STATUS (all 636 lines), ADDENDUM-3, ADDENDUM-R2, B418 brief (head), B418 STATUS tail, B434 brief and STATUS (390 px table), B435 verdict, `deploy-from-ci.sh` and `infra/README.md` diff at `35b2b73e`, model routing row C6, `models_latest.json` (`opus` = `claude-opus-5-5`).

## Facts MEASURED by me (read-only)
- `01dd9e4b` via `gh api`: 1 parent, "B434 ... (#179)". The object is NOT in the local checkout (`git show 01dd9e4b:...` fails), so the brief has the seat fetch first and read the script at `35b2b73e` (the parent).
- `ls-remote`-equivalent (`gh api branches/main`): main = `01dd9e4b`.
- **CI at the sha: the `ci` push run `39679167450` was still `in_progress`** when I looked (only the dynamic "Push on main" run `39679167700` was success). `deploy-from-ci.sh fetch` needs a `success` run, so Tuesday should check it before launch. The brief makes the seat wait and STOP (no hand-fetch) if `ci` ends non-success. B410 needed an addendum for a cancelled SQL shard; if that shard times out again, you will need to write that addendum.
- Ports 8070-8099: nothing listening (no positive control run); brief uses 8080-8089 and tells the seat to re-check with a control.
- `ae7a2c86..35b2b73e` touches `api/.../UatOpenAuthentication.cs`, its test, `infra/*`: so the redeploy also moves the UAT API to B418's code, not just the web badge. The brief has the seat list the live-to-target path diff and expect no migration/SQL change.

## Judgement calls to check
1. **Rollback package.** `fetch ae7a2c86` will refuse (its run rolls up red). B410's own package folder sits in a tree the seat may not open. So the brief makes the seat download each live `wwwroot` read-only (the script's own Kudu method) as the rollback kit, record sha256, and prove the rollback command runnable without running it. Wording in BUILD step 2 is slightly clumsy; it may need a tidy read.
2. **Stale-LastError wrinkle (B410 attempt 1).** The README now says to restart only for a site that has never run code. This site has run code, so the brief does NOT restart first. If the failure recurs, the seat records three facts and STOPS with one question (no hand-run API step without an addendum).
3. **Schema check.** Brief STOPs if `assessment.sql`/`feedback.sql` differ from the live ones (a schema step needs a firewall rule: a new brief). Not expected.
4. **Refusal matrix.** Taken from B410's table: Admin reset and customer delete 403 `uat.action-off`; Partner metrics and feedback list 403; Consultant and Demo feedback list 403 (they see metrics, 200). One probe per level, as asked.
5. **Widths.** Only 390 and 1280 are asserted. B434 measured wraps at 375 and 360 (the product owner's call); the brief says record, do not fix. B434's 4 px slack at 390 is Chrome-specific: Consultant wrap at 390 = STOP.
6. **Demo read-only list.** I allowed a read-only `az resource list` of the demo group before/after, copied from B410. Remove it if you want the seat to touch the demo group not at all.
7. Settings drift: the brief checks setting NAMES equal before/after and that B418's two settings (banner off, outbound addresses) survive; a code-only deploy should change none.

## Not done / fenced
No `az`, no HTTP to any host, no `.tools/b4*` tree opened, no decision queue, no other store written.

Paths:
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B437_SEAT-D25_hpsmpoc-uat-redeploy-badge.md
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B437_DRAFTER-REPORT.md
