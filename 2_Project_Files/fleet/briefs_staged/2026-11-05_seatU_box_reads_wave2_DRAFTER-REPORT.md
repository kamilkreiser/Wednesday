# DRAFTER REPORT: Seat U 14th, box reads wave 2

**BLUF.** Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatU_box_reads_wave2.md`. Seat U, ordinal **14th** (measured: `Seat U 13th` heading at line 54 of the Secuura history file, `^## .*Seat U 14` count 0, positive control U 12th at line 940). Sonnet 5.5; model-routing.md has NO read-only-box-read row, so the brief cites C7 and C4 as nearest and U 13th as the precedent (stated plainly). Read-only on kintsugi; demo reads only for items 2 and 4. Nothing sent, launched or written to Linear or the repo.

## Items, in order (scope sentences quoted)
1. **KS-962** (Kam's account, In Progress). Open condition, ticket's own words: "closes when a deploy seat verifies `secuuraadmin`'s `rolbypassrls` on a deployed box". E 37th's ask: (a) `resynced` on the newest "Per-client user tenant re-sync complete (main DB)" line; (b) user part only of `MIGRATION_DATABASE_URL` or "unset" (parser control on `DATABASE_URL` = `secuura_app`; plus `pg_roles` booleans for the named role); (c) optional E 37th SQL as `secuura`, only if its sha256 equals the one Wednesday relays in the GO. Facts comment + mail.
2. **KS-1087 reach** (Kam's card = b, ruled 2026-11-02T12:44:48+11:00: "Wait: measure read-only whether workflow-gated document types exist; no build"). Store found at source (develop 5fc5569ed96a): **Redis**, `secuura:gateway:doctype:*` (gated = `requiresApproval === true` AND `approvalWorkflowId` truthy) and `secuura:gateway:wf:*` (approver roles in `steps[]`); both keys have TTL 3600 s. Not `admin_settings`, not `svc_gateway_settings`. Method adapted from U 13th's `gwttl_u13.sh` (SCAN/TTL/GET on two patterns, counts and roles only). Both boxes, read-only. Facts comment on KS-1087.
3. **KS-1188** (Kam's, In Review): compiled marker of the reworded 503 (`passwordLoginGate.ts:70`, "your backup code may already have been spent"), kintsugi only, positive and nonce controls. Facts comment; no close.
4. **KS-1384** (created by Stuart, assigned to Kam): mail only, no comment. The 17 fix strings measured read-only on demo; the record (D 52nd `E3_fixes4_post.txt`) shows the one MISMATCH is F33 `WriteAheadUnavailable` (0/0/0, predicted 0->0). The brief gives that as a record only and tells the seat to measure all 17 and say "not live" vs "not discriminating".
5. **Census sweep** of `inreview.tsv` (24 rows): exactly one row is marked `LIVE-CHECK-OWED (read-only box read)` = KS-1188. Two more carry a read-only half and are included: **KS-968** (read-only per-box state check; SQL goes to Wednesday for written OK BEFORE running, since it touches the credential-bearing users table) and **KS-1018** (compiled markers of three rethrows). All other rows listed as write-type/skip.

## Excluded, and why
- KS-1384 comment (Stuart-created). KS-1380, KS-1355 (Peter-created); KS-693, KS-577 (Peter/Stuart decide). Write-type rows: KS-1717, 1633, 1370, 1232, 1186, 1512, 1510, 1477. Board/scope/decision rows (no box read): KS-1594, 1553, 1545, 1533, 1508, 1194, 961, 946, 657. No Done/archive anywhere (this seat closes nothing).
- The seat is told NOT to use D 52nd's `fixes_live4_d52.sh` as is: it uses `docker run --network none` (a container create); a `docker exec`-only variant is required.

## UNMEASURED (each is written conditional in the brief)
- Sha256 of the E 37th SQL that E 37th will mail (I read the file as `838b8cc5...f4eb` at drafting, marked informational only; Wednesday must relay the real one in the GO).
- This seat's pane id; S 22nd's key list (board partition rests on a 30-minute re-read before each write); whether a D seat is live on either box.
- Exact subject of E 37th's QUESTION mail; exact text of Wednesday's ANSWER 02:57:12Z to U 13th (the brief extends the gwttl class from exists/type/ttl/pttl to scan/ttl/get and asks the seat to say if that is outside the approval).
- Whether a Postgres table also holds document types; whether any `wf:` workflow seed exists outside `admin.ts` (I found none; so seeded types may name `wf-1/2/4` with no key).
- Compiled spellings of the KS-1188 and KS-1018 markers; container names (assumed `secuura-api-gateway`, `secuura-postgres`; seat reads `docker ps`).
- Live state: nothing was contacted on either box.

## Looked wrong or stale in the lane plan / census
- The census and U 13th brief say develop tip `5fc5569ed96a` is not in the checkout; it IS now (`git cat-file -t` = commit).
- Kintsugi REVISION head is `5fc5569ed96a` but only `originate` was swapped (D 54th), so the head is not a per-container fact; the brief makes the seat name image id and StartedAt per container.
- Item 2 consequence worth Wednesday's eye: Redis keys expire in 1 hour, and the three seeded gated types only appear when `enableDemoSeed` is on AND an admin lists the catalogue. A zero on either box may be a time-of-read artefact; the brief makes the seat report key counts and TTLs beside the gated count.
- `inreview.tsv` header column 5 is the PR ancestry column, class is column NF-1; I used the last two columns for class and next step.

/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatU_box_reads_wave2.md
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatU_box_reads_wave2_DRAFTER-REPORT.md
