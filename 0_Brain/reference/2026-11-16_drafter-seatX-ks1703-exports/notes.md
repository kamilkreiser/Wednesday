# Drafter notes, Seat X KS-1703 analytics exports (2026-11-16 01:1x AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatX1_ks1703_exports.md (34,988 bytes, under 35 KB). Scratch and copies: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-16_drafter-seatX-ks1703-exports/_work/.

## What I found that the commission did not say
1. **The ordinal is wrong.** History has Seat X 1st (2026-10-27) through X 9th (2026-11-09); `Seat X 1st` count = 1, not 0; `Seat X 10th` = 0. The brief names X 10th and tells the seat to re-measure.
2. **Exports are platform aggregates, not company rows.** The payload comes from `analyticsService.get*Metrics({period,startDate,endDate})`, which takes no tenant. The leak is a real missing check (no creator, no company on the record; ids enumerable through the list route) but the bytes exposed are platform-wide numbers. Who may CREATE a users/revenue export is KS-1856 (Backlog, priority 3), not this PR.
3. **There is no download route and no delete route.** The "file" is the `data:` `downloadUrl` inside the GET answers. Measured: 0 hits for delete/download in the routes file.
4. **The list route is the door that makes the by-id read decorative** (it returns every export with its inline file). Brief puts it in scope (W2), same reasoning as the C 38th brief's W3.
5. **AC6 trap:** the systemTest module's actors are two OWNERS of the SAME company and `test_analytics_export_by_id` is `xfail(strict=True)` ruling-pending. A cross-company-only fix leaves it failing, so the marker MUST STAY. The brief forbids touching that file (PR 2241 also edits it).
6. **Overlap with open PR 2188** (KS-2167, edits `exportService.ts`, the processExport catch). Design avoids it: the route records the owner in a new module's side Map, so `exportService.ts` is not edited. Alternative (owner on the service) is W4. PR 2241 touches no analytics file. Dependabot PRs 948/649/575 touch analytics `package.json` only.
7. **Positional INSERT parameters are pinned by tests** (ks1922 reads `p[1]`, `p[8]`; ks2167 filters `p[1]`), so adding a column or reordering parameters is forbidden by the design anyway.
8. **DB persistence looks broken by the repo's own DDL:** `svc_analytics_exports` (three DDL copies) has no `type`, `download_url`, `expires_at`, `error` columns that the INSERT writes. KS-1856 claims rows reload at boot; unconfirmed against a live DB. Design is fail-closed on an unknown owner (admin only), no column.

## Rule chosen (D1)
Platform role (`isPlatformRole`) reads all; else caller `tenantId` equals creator `tenantId` (both non-empty, `===`, as `decideTenantAccess`); else, for a tenant-less creator, same `userId`; no owner record = admin only; refusal = the route's own 404 bytes. Same-company reads unchanged (Kam's open card, default build nothing inside-company).

## Stack measured
TypeScript, express 4, zod 4, vitest 4.1 (script `vitest` is watch: use `npx vitest run`), eslint 10 (`eslint src`), tsc strict with `noUnused*`, tsconfig includes tests. Same shape as the transfer service.

## Calls made
develop e659170439406810d368bdebf19dd39c08abeace (committed 2026-11-15T13:41:56Z = 00:41:56 AEDT; the commission's 00:55:59 was its read time). 72 open PRs, 370 file rows. KS-1703 In Progress, priority 0, 7 comments. load1 about 3-4. No secret printed; Linear key read in-process only.

UNMEASURED
whole services/analytics suite at develop (not run); live DB columns of svc_analytics_exports and the boot reload; gateway role gating for /api/analytics; external API clients; analytics.openapi.ts 404 text for the by-id path; the open state of Kam's card secuura-ks1703-ac4-same-company-reads-1115 (from the commission); push hook refusal branches; whether a platform-admin token carries a tenantId; whether PR 2240 touches analytics (not checked; 2241 checked).
