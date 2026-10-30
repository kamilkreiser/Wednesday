# Spark operator 29 - report (2026-10-30, base develop 85cd24d81cb9, clone .../2026-10-30_spark-operator29/clone)

## BLUF
Census EMPTY. No KS-1544-class site (paged list, ORDER BY without a unique last key) remains in Platform K outside (a) op 28's held originate files and (b) the live-seat exclusion list. No brief written, no Spark round run (0 rounds), nothing held. Drainer 97411 alive, I started none. Spark idle.

## Census (clone at new path, rev-parse --show-toplevel asserted equal; ls-remote develop 85cd24d81cb9, same as ops 27/28)
Method: case-insensitive grep for SQL `OFFSET` (and `skip:`/`.skip(`/`(page-1)*`) over services/, packages/, shared/ (no node_modules/dist/tests/.d.ts), plus every `ORDER BY` (126 lines, 48 files) read for paged use.
14 SQL OFFSET sites in total:
| site | state | disposition |
|---|---|---|
| tenant-provisioning index.ts:589 | `created_at DESC, id DESC` FIXED | CONTROL (KS-1544's own named site): shows fixed |
| vc-issuer credentialRepo.ts:365 | `created_at DESC, id DESC` FIXED | CONTROL 2 (KS-1731) |
| originate errorTrackingService.ts:91,100,108,116,123 | open | op 28 held (O28-P1) |
| originate adminConfig.ts:1235,1241,1405,1410 | open | op 28 held (O28-P1) |
| staking rewards.ts:315,362; stake.ts:458 | open (`ORDER BY claimed_at/distributed_at/stake_date`, no key) | EXCLUDED: live seat owns staking. Hand to raise seat |
| auth userRepo.ts:1044; issuerCertRepo.ts:294 | userRepo open (`created_at DESC`); issuerCertRepo ordering not shown on the OFFSET line | EXCLUDED: services/auth live seat |
Everything else is not DB paging: security/index.ts (:872,:1049), api-gateway admin.ts (:1108,:1129), analytics (:506) slice in memory; originate documentRepo.ts:275-288 reads `ORDER BY created_at DESC LIMIT 200` then pages in memory (borderline, see below). packages/shared db/optimization.ts getPaginatedList and applyPagination (Prisma skip/take, default orderBy createdAt only) have ZERO callers (grep over the tree) - dead helpers, not a live site.
Positive control: the same grep finds all 14 OFFSET lines incl. the two fixed ones, so it is not blind.

## KS-1544 ticket (read-only, key sourced transiently, not echoed)
Status In Progress. Names ONE site only: tenant-provisioning index.ts (then :558, now :589) `ORDER BY created_at DESC` -> `, id DESC`; P4; test = >200 rows sharing one created_at read in two windows. That site is ALREADY fixed on develop 85cd24d (control above). The ticket names no other site and does not mention originate; so ALL 9 originate sites (O28-P1), the 3 staking sites and userRepo.ts are unnamed there. Raise seat: the ticket's own site needs only a status check; the class sites are unticketed.

## Borderline (not briefed)
originate documentRepo.ts listDocuments (:271-288): SQL `ORDER BY created_at DESC LIMIT 200` has no tie-break, so which rows fall in the 200 cap is undefined on ties, then JS re-sorts and slices. One file, one hunk: same class but a single-file rung-4 job, and it is the repository behind documents.ts (a live seat's file); I did not take it. Also unmeasured: whether any caller exceeds 200 rows per tenant.

## Rounds
None. (Rung 6 not attempted: no census to support 4+ files; inventing sites would not be real work.)

## Faults
1. Hooks: one `cd` refused two calls; zsh glob `--include=*.ts` unquoted cost one call. 2. Wrote the grep scratch to /tmp/x (should have been the scratchpad); 126 lines of grep output only, no secrets.

## Next
1. Raise seat / Wednesday: staking (3 sites) and auth userRepo.ts:1044 are the remaining class sites; both need their live seat or a hand-off before Spark can brief them. Spark brief for them is cheap once cleared (staking: 3 hunks, 1 file + test).
2. Rung 6 still unmeasured; needs a different, real 4+ file task.
3. Prune clone (this dir).

## Left behind
clone/, lsremote.txt, this report. done.md and IMPROVEMENTS.md untouched (no rounds).
