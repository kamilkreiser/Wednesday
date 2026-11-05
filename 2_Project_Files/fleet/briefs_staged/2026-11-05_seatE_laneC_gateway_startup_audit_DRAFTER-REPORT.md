# DRAFTER REPORT: Seat E 37th, lane C (2026-11-05 ~16:55 AEDT)

**BLUF.** Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatE_laneC_gateway_startup_audit.md`. Seat E, measured ordinal **37th** (max E in history.md is 36th, line 478; derivation in the brief's PROVENANCE). Model claude-sonnet-5-5, routing row **C2** (C3 flagged as a stop-line for KS-962). Six tickets included, but **only part of each is buildable without an answer from you**: KS-962, KS-1645, KS-864 and KS-1128's remaining halves all hinge on a design or partition choice the tickets leave open, and the brief turns each into a QUESTION mail, not a pre-made answer. KS-736, KS-1494 and KS-1548 are excluded. The develop tip read was `5fc5569ed96a` (16:22).

## Tickets included, in order, with remaining scope quoted
1. **KS-962** (High). Title still says "remove its INSERT"; that is DONE (PR 973). Remaining, ticket's own words: "This ticket stays OPEN: F-973-3 (silent no-op under a NOBYPASSRLS migration role) and F4 ... stand by ruling; closes when a deploy seat verifies `secuuraadmin`'s `rolbypassrls` on a deployed box", plus the 11-04 box read: no `secuuraadmin` on kintsugi, gateway runs as `secuura_app`, "Not measured: whether the boot statement updates 0 rows". The brief commissions "measure and ask" only (narrowing declared). Fix shape = QUESTION to you; an RLS-bypass fix is a C3 surface, so Sonnet must stop and hand to Opus.
2. **KS-1645** (High). "Left open: items 1, 2 and 4, and the rest of item 3." Confirmed still true at the tip in `audit-export.ts` (no `limit`, `to` day truncated) and `api-gateway.openapi.ts:610-647`. Item 1 (page vs declare cap), item 2 (`to` inclusive vs documented exclusive) and item 3b (security filters vs gateway stops claiming) are choices the ticket itself leaves open: three QUESTIONs.
3. **KS-864** (Medium). Remaining per the ticket: the unused third `getServiceUrl` args, the `secuura-staging` az hint (now `system-status.ts:541`), portals probed on `:80` vs nginx `:8080`, headline ignores red panels, and two Polish test items (F-1009-1/2).
4. **KS-1504** (Medium). Items 3 and 4 only (two test cells), tests only, no deploy surface (addendum). Item 2 (optional) not commissioned.
5. **KS-1128** (Low), after KS-962 (same file). SEED-REALPG real-PostgreSQL cell and a cell pinning the 200-char cut; SEED-INNER not commissioned.
6. **KS-1841** (Low). F2 only (build context / builder layer). Gate tier 1 proposed.

## Excluded
- **KS-736**: Opus, `proxy.ts` posture change. **Lane-plan error:** lanes.md says it depends on "unmerged PR 1701". PR 1701 is MERGED (`409ad6c36cdb`, ancestor of develop, `merge-base --is-ancestor` rc 0; KS-1713 Done).
- **KS-1494** (Kam a, 16:09): remaining build is in `services/auth/.../userRepo.ts` (lane A, seat J), not `startup-migrations.ts` (0 hits for the seed). The "otherwise unchanged" doc location is UNMEASURED. Route to seat J or you.
- **KS-1548** (Kam a, 16:09): the code is in `routes/platform.ts` (platform audit-log), NOT `audit-export.ts`; `platform.ts` is in no live lane's family (only lane X's KS-1536). Partition question for you.
- Seen, not taken: KS-1493 (ruled 16:10) concerns a limiter; which lane holds it is UNMEASURED.

## UNMEASURED lines (all conditional in the brief)
Box facts for KS-962 (the `resynced` count / drift; seat has no box access, so QUESTION); security service `/api/audit` limit clamp and date handling; what KS-1102 ruled for the status hint; whether seat T edits `api-gateway.openapi.ts` this wave; which build path (compose / acr / BuildKit) the image uses; Docker daemon state; today's ks949 suite totals; KS-1494's doc location; the seat's pane id.

## Things that looked wrong in the lane plan
- KS-864's lane line ("items 2,3: drop ... 16 of 18 getServiceUrl calls") conflates the dead third-arg cleanup with the ticket's items 2 and 3 (port, headline). Drafter counted **17** call lines carrying the arg (plus the hint = 18 `secuura-staging` hits); the ticket says "16 of the 18". Seat told to re-measure and use its own.
- Lane C's family lists miss files the tickets need: `api-gateway.openapi.ts` and `docs/openapi/secuura-api.yaml` (KS-1645 item 4), `frontend/status/index.html` and `docker/nginx-gateway/` (KS-864), root `.dockerignore` shared by every image (KS-1841), `services/security` (KS-1645 item 3b). All are OUTSIDE the family; the brief makes each a stop-and-ask.
- Repo paths carry a `Blockchain/Dev/` prefix inside the checkout; lanes.md paths omit it (the brief says so).
- KS-962 is not "build the fix": its title is stale; its remaining condition is a box read.

Brief gate literals present at line start (RULED BY KAM, PROVENANCE, SELF-CHECK); no SCOPE-HIT words (grep rc 1); `self_check_view.sh` run, two defects found and fixed. Nothing was sent, launched or written to Linear or any repo.

/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatE_laneC_gateway_startup_audit.md
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatE_laneC_gateway_startup_audit_DRAFTER-REPORT.md
