# DRAFTER REPORT: Seat D 15th brief (kintsugi, then demo, follow-up deploy)

Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-07_seatD15_kintsugi_then_demo.md` (147 lines; NOT sent, NOT launched).
Drafter wrote only this file and the brief. Scratch: session scratchpad `vclone` (a `clone --shared --no-checkout` of the shared checkout, fetched by full SHA from the GitHub URL). No host contacted except github.com (ls-remote + fetch by SHA). No SSH, no tmux, no mail, nothing deleted.

## What I measured, and how

| fact | value | instrument | time (UTC) |
|---|---|---|---|
| develop | `69f2045af2a4f5f0b83b2f76c62514512abdc7b5` (unmoved across 3 reads) | `env -u GIT_SSH_COMMAND git -C <shared checkout> -c core.sshCommand=<its config> ls-remote git@github.com:Secuura/Distributed_Secuura.git refs/heads/develop …`, rc 0 | 00:18:22Z, 00:22:46Z, 00:26:28Z |
| PR heads | 1398 `9414aa54e92c…`, 1383 `32e8459bc0f5…`, 1406 `4a400d7aa9dd…`, 1404 `6ea65f64e639…` | same ls-remote | 00:18:22Z |
| range | `d75bfe2deb80` strict ancestor; left/right 0/12; 7 first-parent commits; tree `a4a219b87271`; 197 files, 7 under `Blockchain/` | `merge-base --is-ancestor`, `rev-list --left-right --count`, `log --first-parent`, `diff --name-status` in vclone | 00:19Z |
| per-commit | #1406 `fa24bdded` = 5 lockfiles; #1404 `69f2045af` = 1 test file under Dev, `Testing/jobs/06…`, 2 html | `diff --name-status <c>^1 <c>` | 00:19Z |
| versions | pbkdf2 3.1.6→3.1.7 (issuer, shared, anchoring); SDK 1.29.0→1.31.0 (mcp-server); root lock: SDK, pbkdf2 3.1.5→3.1.7, shell-quote 1.9.0→1.11.0 | `diff -U0 fa24bdded^1 fa24bdded` filtered to version lines | 00:21Z |
| image inputs | **29** (packages/shared lock COPYd by 29 services); issuer lock → issuer-frontend; anchoring lock → anchoring; mcp lock → mcp-server; root lock → NONE; #1404 test → NONE. Not inputs: demo-overlay, status-frontend, nginx-gateway, pgbouncer | `python3 -I -B …/2026-10-07_seatD-14th/boot/service_mapd14.py <vclone> d75bfe2… 69f2045…` rc 0; 7/7 controls fire (kyc, originate+migrations, api-gateway+bind, VOCABULARY → NONE, run-migrations, preflight NONE, shared → 29) | 00:18:58Z |
| #1404 alone / #1398 head | 0 image inputs each | same mapper over `fa24bdd..69f2045` and `d75bfe2..9414aa54` (merge-base of #1398 == d75bfe2) | 00:20Z |
| migrations | **0** paths in `migrations/`, `run-migrations.sh`, `docker/init`, `docker-compose.yml`, `.env.example`, `*.sql`; FALSIFYING control `0f8fb33c3..d75bfe2deb80` lists 038a A, 039 M, 01-schema/06-m365 M; 50 `.sql` at both SHAs; `migrations` tree `fb18e5bc77d5` and compose blob `a219a32b2949` identical at both | `diff --name-status -- <paths>`, `ls-tree`, `rev-parse <sha>:<path>` | 00:20Z |
| #1383 | adds `049_ks1401_tenant_isolation_after_039.sql`; unmerged | `diff --name-only d75bfe2 32e8459 -- Blockchain/Dev/migrations` | 00:21Z |
| `.dockerignore` | lines 34-35 `*.env`, `*.env.*` | `git show 69f2045:Blockchain/Dev/.dockerignore` | 00:21Z |
| G-DRIVE | mounted, 3,779,816 MB free; `/Volumes/G-DRIVE/Secuura` does NOT exist yet | `df -m`, `ls` | 00:1xZ |
| OTHER_SEATS trap | D 14th's matcher line 238 holds `seat d 15th`/`d 15th`/`d15` → D 15th's own GO would read FOREIGN | read `inbox_matchd14.py` | 00:2xZ |

Carried (read whole, not re-measured): HANDOVER-seatD12-deploy.md (256), HANDOVER-seatD13-demo-deploy.md (320), HANDOVER-seatD14-demo-deploy.md (202), the D 12th and D 14th briefs, STANDING_LINES.md (422), Secuura and Blockchain CLAUDE.md, both learnings named in the task, D 12th's `phase2_all30_results.txt`/`swap_order_28.txt`, D 14th's `rebuildset/swapset`, `results_final_d14.tsv`, `status_build_d14.txt`, the D 14th ghost ANSWER, NEXT-PICKUP:28, EXPIRING-GRANTS:10,12, daily 2026-10-07:83,103 (gate72 reach).

## Disk forecast per box (arithmetic; F0 is the LAST RECORDED value, not measured today)
Required F0 = N × rate + 5,200 (FLOOR 4,000 + DIP 1,200, `disk_forecast_d14.py:14-17`), N = 29.
| rate (MiB/image) | source | required F0 | kintsugi F0 6,312 | demo F0 13,221 |
|---|---|---|---|---|
| 349 | demo whole-round D 14th (23,238→12,405 over 31) | 15,321 | short 9,009 | short 2,100 |
| 354 | D 12th steady | 15,466 | short 9,154 | short 2,245 |
| 470 | 354 × 1.327 cold cache (D 13th) | 18,830 | short 12,518 | short 5,609 |
| 525 | D 14th in-flight, 21 intervals | 20,425 | short 14,113 | short 7,204 |
| 550 | worst case | 21,150 | short 14,838 | short 7,929 |
Kintsugi also fails originate's 10,000 ADMIT at once. Kintsugi F0 = HANDOVER-seatD12:78 (settled after its round, build cache regrown to 12.38 GB); demo F0 = HANDOVER-seatD14:43 (after build+swap). Both are UNMEASURED today; ITEM 0 (c) closes them.

## Things in the task framing I could not confirm or that differ
1. **"Both boxes at d75bfe2deb80" is a record, not a measurement** (D 12th / D 14th handovers). ITEM 0 proves it by content.
2. **29 vs 25:** 29 is the image-INPUT set (what rebuilds); gate72's 25 is pbkdf2's RUNTIME reach. Both are in the brief, labelled.
3. **Swap counts differ from the last round by derivation:** kintsugi 28 (29 − migrations; D 12th also swapped demo-service), demo 27 (29 − migrations − demo-service; status-frontend is no longer rebuilt). Expectations only; the seat derives them.
4. **The 100% usage row is EXPIRED** (EXPIRING-GRANTS:10), so "one or maybe two deployers" no longer has a live grant row; the brief says one seat on its own terms.

## Open questions for Wednesday (recommendation each)
1. **Q-DISK15 (blocking):** neither box clears on recorded free space. *Rec (the brief carries the same):* launch for ITEM 0, then card Kam on the seat's measured numbers. The options to card: Kintsugi: (a) build-cache prune (regenerable, nothing to archive; D 12th freed 11,041 MB) PLUS (b) archive the oldest rollback sets (`pre-20260910`, `pre-2026-09-12` …) to `/Volumes/G-DRIVE/Secuura/Blockchain/archive/<date>_kintsugi_<set>/` and untag by reference, until the forecast clears at 470. Demo: archive `pre-20260910` (13 ids only it holds) to G-DRIVE then untag by reference; re-forecast. Default on the card: nothing freed, nothing built. The alternative (card now on recorded numbers so the ruling rides the GO) is faster but rests on day-old F0s, and kintsugi's build cache is the swing figure.
2. **Q-1383-15:** #1383 carries 049 (live-data migration). *Rec:* hold its merge until this seat's demo DEPLOYED or WRAP; 049 gets its own kintsugi-first round with a migration STOP. R 7th's brief already holds #1383 until #1398 lands, which does not cover this round.
3. **Q-DEMO-CTX15:** both boxes in one seat. *Rec:* GO-DEMO only below 40% by pane read; otherwise demo to D 16th with a RESUME block.
4. **Q-ARCHIVE-COST:** `docker save` from Azure SE Asia to the Studio is unmeasured and loads a 2-vCPU demo box. *Rec:* the seat measures size (`docker save … | wc -c` on the box) and throughput (one small image piped to `wc -c` on the Mac) at ITEM 0, outside any build/swap window; the card quotes both.
5. **Q-KS535-LITERAL:** the literal-string control differs per box (kintsugi `1d99a769a815b299` from D 12th, demo `7d8958f1e48a608c` from D 13th, ruled). *Rec:* keep per-box values and make the seat name the exact literal it hashes; a mismatch is an instrument question (fix, re-prove), not a reading STOP.
6. **Q-SAMEID:** frontends may build SAME-ID for the first time. *Rec:* as written: prove phase4's SAME-ID skip branch with a NEW-ID control before Gate S, and treat SAME-ID as a valid reading.

## UNMEASURED (instrument that closes each)
Both boxes' free space, build cache, per-set unique size, census, KS-535, baselines (ITEM 0 (c)); `docker save` size and SSH throughput (ITEM 0 (e)); which images build SAME-ID (ITEM 2); in-container paths of pbkdf2 and the SDK (`find`, ITEM 5); whether develop moves before ITEM 0 (ITEM 0 (a)).
