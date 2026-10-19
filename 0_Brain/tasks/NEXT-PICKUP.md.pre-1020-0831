---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the morning Wednesday seat (booted 06:0x 2026-10-20) at its ~65% checkpoint, 07:18 AEDT. Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1020-0720 + git.
---

# NEXT PICKUP (Tue 20 Oct, written 07:18 AEDT)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into the cache clone at the LITERAL path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (a `$VAR` path makes the no-cd hook refuse the whole call). **`refs/pull/N/head` can LAG the branch by 12+ min: when a seat reports a new head, ls-remote/fetch the BRANCH ref.** Re-hash verdicts with `sed '1d;$d' verdict.md | shasum -a 256` and name the method.
3. `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`.
4. **ZOOM BEFORE ANY RAW KEYPRESS** (`tmux resize-pane -Z -t %N`, read ~12 lines, unzoom). Busy line ("Brewing…", "Leavening…") = no keypress. `/model claude-opus-5-5` only at a zoomed idle prompt, then Enter on the "Switch model?" dialog, read the statusline.
5. Receipt guard: a note line quoting a send must be its OWN call after the send. A mail citing a card id needs the card to EXIST first.
6. In force: Kam 10-18 new-account grant (tickets, backlog, Spark max), routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant. Gauge 62% at 07:0x.

## 1. LIVE FLOOR (07:18) — develop = 937c7d10b7f83d2fa7e5e662ce46a9e8877186e3 (#1646)
**Merged by this seat today (verified by Wednesday's own fetch):** #1645 KS-1668 docs 5ac66264b9ee (tree 37244a4a698e = BF0 r2, Wednesday's own through-code check) · #1646 KS-1679 937c7d10b7f8 (tree f16006646d53 = gate BF1). Also on develop since the evening: Peter's own #1642 (KS-1607 Schemathesis, merged by him 05:50) and #1625 (merged by him 10-19). **Kintsugi runs a4187f0f6622** (D 22nd); **demo runs d75bfe2deb80 with the KS-1032 vouch secret ARMED** (D 23rd, 200 -> 401, real callers byte-identical).
- **R 57th (%14, Opus 5.5 by Wednesday's switch):** building **KS-1677** (m365 OAuth callback: nonce state + browser-binding cookie + PKCE, retire `POST /api/connections/complete`, DB state table **migration 053**, five schema copies, one PR, tier 1). Cookie pass-through PROVEN live (Docker stack `secuura_r57probe` on this Studio, slot 4; R tears it down after). Its READY -> a **tier-1 Opus gate** (cells R1-R10, C1-C3, seven mutants). Then **KS-1682** (High: m365 refresh-token taken from a process-wide MSAL cache, filed today) is a SEPARATE later PR; **KS-1679 N1** (a falsy-value log cell) is a later test-only follow-up.
- **C 30th (%15, Opus 5.5 by Wednesday's switch):** building **KS-1116** (presentations + credentials owned by the creating principal; bound at the ROUTE layer on the record incl. the in-memory fallback; widen to `GET /api/credentials` list + `by-hash` ONLY if a read-only Platform S consumer search finds no caller, else STOP; **migration 054**; NULL-owner arm = interim option C (nobody) pending Kam's card). Its READY -> a **tier-1 Opus gate**. fleet_ack for its 20:12Z plan QUESTION was not yet collected at 07:1x: re-run `fleet_ack.sh answered 'KS-1116' '...'`.
- **D lane EMPTY** (D 23rd wrapped 0.95). **Demo deploy of a4187f0f6622 is NOT GO** (KS-695 part ii: Stuart's rule "demo-pk only after uat-ps", no uat-ps note) — waits on Kam's card. D 23rd's handover `5_Project_History/2026-10-20_seatD-23rd/HANDOVER.md` (project tree) lets the next D seat run it cold: Phase 0 from RUNNING image ids (5 containers not on their own :latest), `--profile phase2 build`, originate's `:latest` pinned to running `e0efefd0b7e0` (probe preserved as `dev-originate:probe-20261007`), migrations 049-052 censused.
- **Next kintsugi round** (when worth it): develop since a4187f0f6622 = #1640-#1646 + Peter's #1642; only #1641 (display-only) and #1646 (KS-1679, one originate file) are product; then a live read of a derived document's stored certificationId/certifiedAt.

## 2. KAM'S CARDS (all Secuura, all with defaults)
- `secuura-demo-deploy-ks695-uatps-precondition-1020` — rec a (a seat asks Stuart one line on KS-695 whether uat-ps carries aeae5ca); default c (defer).
- `secuura-demo-smoke-provisioning-key-unbounded-1020` — rec/default a (measure key_66e82ef0's last use read-only, then re-raise; nothing revoked).
- `secuura-ks1116-null-owner-who-reads-1020` — rec a (tenant admins: ORG_ADMIN/SYSTEM_ADMIN with a tenant); default c (nobody). The ambiguous phrase was WEDNESDAY's own 09-13 option text (ledger row). **When he rules, tell C 30th (or its successor) by mail; it is one predicate.**
- Datasec `composer-l05-setup-card-too-1014` is Tuesday's.

## 3. OWED BY WEDNESDAY (in order)
1. R 57th's KS-1677 READY -> tier-1 gate brief + Agent gate (Opus, row G1) -> GO -> verify merge.
2. C 30th's KS-1116 READY -> tier-1 gate (Opus) -> GO -> verify merge. Sequence the two migrations (053 R, 054 C) if both land before a deploy.
3. On any Kam tap: rule the card in the same step, receipt first, deliver to the seat.
4. Spark: queue is empty with a WHY line; new tickets today (KS-1681 dangling DEPLOY-BLOCKERS citations, KS-1682) are not Spark-shaped. Re-screen when the board moves.
5. Fable 5.1 coordinator trial (routing decision 7, second half) still OWED.
6. Regenerate BOTH boot digests at the wrap if any lesson FILE is edited (only the ledger was edited today so far).
7. Ledger 3c archive at the 05:30 shift-change wrap.
8. KS-1665 (deploy.sh admin fallback on a failed key-vault read) deserves more than Low before any production deploy; KS-982 archive is Kam's call. Neither carded yet.
