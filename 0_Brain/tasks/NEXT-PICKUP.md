---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the overnight Wednesday seat (booted 2026-10-20 02:45) at its 70% checkpoint, 2026-10-20 04:1x. Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1020-0415 + git.
---

# NEXT PICKUP (Tue 20 Oct, written 04:13 AEDT; quiet hours until 06:00)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open` (it lives in tools/, NOT fleet/), fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into the cache clone at the LITERAL path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src`. Re-hash every verdict with `sed '1d;$d' verdict.md | shasum -a 256` AND name that method in any brief that quotes a hash (ledger 10-20).
3. `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`.
4. **ZOOM BEFORE ANY RAW KEYPRESS** into a seat pane (`tmux resize-pane -Z -t %N`, read, unzoom): the 44-column panes hide the busy line; this seat typed `/model` into C 28th's running turn at 03:3x (ledger 10-20). `/model` only at a ZOOMED idle prompt.
5. Seat context when the statusline is unreadable: zoom the pane and read `ctx:NN%`; your OWN: the last usage row of your transcript jsonl (input + cache_read + cache_creation).
6. In force: Kam 10-18 new-account grant (tickets, backlog, Spark max), routing v1.0, the October deploy grant EXTENDED "until further notice" (Kam 10-19 18:22:57), the TESTED merge grant. Gauge 57% at 04:0x.

## 1. LIVE FLOOR (04:13) — develop = 2b205beada00a2f0fb3144e38198e471848132b6 (#1640). Kintsugi DEPLOY IN FLIGHT (pin a4187f0f6622).
**Merged since this seat booted (02:45), each verified by Wednesday's own fetch (6):** #1635 KS-1262 17ab917aa6f4 (=AW1) · #1639 KS-1634 N2/N3 c129c63cf777 (=AZ1) · #1637 **KS-1673 B Teams** f7d35d628cdc (=AX1, Fable) · #1638 KS-1653 comments a4187f0f6622 (=AY0, Wednesday's through-code check) · #1641 KS-1660 c9ab6b36ff92 (=BB1) · #1640 KS-1673 real-engine cells 2b205beada00 (=BC1 round 2). Secuura merges since the 10-19 evening: **28**. All `Refs`; Done = deployed + live check.
- **D 22nd (%11, Opus 5, launcher pin; NOT switched by decision): KINTSUGI DEPLOY of a4187f0f6622** (161 commits, migrations 049-052) on Wednesday's GO 16:4xZ. Brief `2_Project_Files/fleet/briefs_staged/2026-10-20_seatD22_kintsugi_census_then_deploy.md`. State at 16:58Z: vouch secret ARMED on the pin images (proved: boot DISABLED->ACTIVE, forged headers 200->401; .env + compose interpolation; D self-caught an .env newline fault and restored byte-identical); Phase 0 33/33 re-tagged `:pre-20261020`; source rsynced (.env/.env.local unchanged); BUILD RUNNING since 16:54:58Z (~2 h). D asserts migrations per file + schema (run-migrations.sh continues past a refusal). **On its DEPLOYED mail:** read whole; check the boot line ACTIVE + image ids (ACTIVE alone cannot prove new code); KS-535 re-verified; REVISION; the Stuart/Peter notice is DRAFTED in the mail, NOT posted — Wednesday decides (rule: client-facing comms are ticket comments; Kam is the escalation channel). The drafted KS-1557 comment likewise. Then score + pane_close. **Demo is a separate later round** (the same KS-1032 vouch precondition must be measured on demo).
- **C 28th (%10, Opus 5; the Sonnet switch was CANCELLED at 03:3x after Wednesday typed into its running turn — it finishes the round on Opus 5):** queue item 3 = KS-1500 + KS-1468 ONE test-only PR (auth ks963, two commits), item 4 = KS-1676 ONE test-only PR from FOUR held Spark passes (`local-model/night/READY_KS-1676-{V2SETTLEDFAILED,V1SETTLEDFAILED,V2STOREDGUARDS,V1STOREDGUARDS}-1_*`; report `0_Brain/reference/2026-10-18_spark-screen/SCREEN_17.md`). Each READY -> a tier-2 Sonnet gate.
- **R lane: EMPTY.** R 56th wrapped 17:12Z (scored 0.95, pane closed). Its handover: `5_Project_History/2026-10-20_seatR-56th/HANDOVER.md` in the project.
- **Spark:** SCREEN_17 produced 4 PASS (all held, above). Pool: re-screen when new tickets land (new tonight: KS-1677, 1678, 1679).

## 2. OWED BY WEDNESDAY (in order)
1. **D 22nd's DEPLOYED mail** (above). Then: kintsugi live-checked tickets become Done-eligible (D lists them; moving them is a separate instruction to a seat). Then plan the DEMO round.
2. **R 57th (if worth a seat):** KS-1677 (Medium: m365 OAuth callback `state` = bare connection id, any status) needs a WEDNESDAY RULING on fix shape: an unguessable single-use `state` nonce bound to the connection + expiry is the standard; PKCE additionally if the client is public. Read the callback code first (services/m365-integration/src/index.ts) and KS-1677's comments (AS1 measured the rebind). Then KS-1679 (Medium, caller spread overwrites certificationId/certifiedAt on derived cert rows: a SPARK candidate, KS-1660 shape) and the #1639 NOTE 1 / #1640 header nits on the next touch.
3. **Kam's morning receipt (06:00+), lead with value:** 28 Secuura merges overnight, all gated, each verified at source; KS-1673 (HIGH, m365/Teams cross-org) code-complete and deploying to kintsugi (state on D's mail); the kintsugi deploy is under his October grant (flag it); KS-1032 vouch secret generated on kintsugi; KS-1557 regression ACCEPTED on dev-ps per Stuart's own comment (fix queued); one open card `secuura-m365-admin-setup-for-customer-org-1020` (default b); KS-1665 (deploy.sh admin fallback on a failed key-vault read) deserves more than Low before any production deploy; KS-982 (Peter set it Done; two seats declined to archive it because archiving hides relations): his call.
4. Fable 5.1 coordinator trial (routing decision 7, second half) still OWED; two Fable tier-1 gate data points recorded in `fleet/specs/model-routing.md`.
5. The Secuura launcher pins `--model claude-opus-5` (Launch_Claude.command:664): every Secuura seat needs `/model` at a ZOOMED idle prompt per routing (raise seats Sonnet, deploy/security Opus 5.5). A durable fix is a project-launcher change (the project's agent, on a brief, or Kam).
6. Regenerate BOTH boot digests at the wrap (`python3 2_Project_Files/tools/boot_digest.py --by-tier` and the bare form): the ledger was edited tonight.
7. Ledger archive at the 05:30 shift-change wrap (rows older than ~3 days -> `_ledger_archive.md`, conservation asserted).

## 3. KAM'S CARDS
- `secuura-m365-admin-setup-for-customer-org-1020` (open, rec/default b). Tuesday's Datasec cards stay Tuesday's.

## 4. TOOLING CHANGED TONIGHT
- `local-model/night/hold_ready.py`: accepts NEW-file test-only passes (no A3c when the patch is byte-identical to the control golden; a `File:` line equal to the brief's own `Test file:` tolerated; a test absent from input files accepted only when the patch creates it and `git cat-file -e <tip>:<test>` fails). Arms run; backup `.pre-1020-testonlygolden`; IMPROVEMENTS row.
- `0_Brain/tasks/DEPLOY-BLOCKERS.md`: dated 10-20 paragraph for the D 22nd round (backup `.pre-1020-d22`).
