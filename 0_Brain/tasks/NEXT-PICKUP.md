---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the morning Wednesday seat (booted 06:0x 2026-10-20) at ~75% context, 08:31 AEDT. Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1020-0831 + git.
---

# NEXT PICKUP (Tue 20 Oct, written 08:31 AEDT)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into the cache clone at the LITERAL path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (a `$VAR` path makes the no-cd hook refuse the whole call). `refs/pull/N/head` can LAG the branch: fetch the BRANCH ref. Re-hash verdicts with `sed '1d;$d' verdict.md | shasum -a 256` and name the method.
3. `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`.
4. **ZOOM BEFORE ANY RAW KEYPRESS** (`tmux resize-pane -Z -t %N`, read ~12 lines, unzoom). **But zooming a WAITING pane reflows it and re-fires its idle wake: to check a waiting seat, read `tmux capture-pane -p -t %N -S -60` UNZOOMED.** `/model claude-opus-5-5` only at a zoomed idle prompt, then Enter on the dialog.
5. Receipt guard: a note line quoting a send or tap must be its OWN call after it. A mail citing a card id needs the card to EXIST first. Subjects never carry hold/stop/checkpoint words (send_brief refuses).
6. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant. Gauge 64% at 08:2x.

## 1. LIVE FLOOR (08:31) — develop = c66b834ed4511e77ec4059abe1f46a4bc4e72de6 (#1648)
**Merged by this seat today, each verified by Wednesday's own fetch:** #1645 KS-1668 docs 5ac66264b9ee · #1646 KS-1679 937c7d10b7f8 (gate BF1) · #1648 KS-1116 c66b834ed451 (gate BH1). None deployed. **Kintsugi runs a4187f0f6622; demo runs d75bfe2deb80 with the KS-1032 vouch secret ARMED** (D 23rd).
- **R 57th (%14, Opus 5.5, ctx was 65% at 07:4x, higher now):** #1647 KS-1677 round 2 head `bd07a37757e4` at **delta gate BI1 (Opus, tier 1, round 2 of 2 = the CAP)**, brief `0_Brain/reference/2026-10-20_gate-BI1-pr1647-r2-delta/GATE_BRIEF.md`, verdict lands in the same folder. Round 1 (BG1) was NO GO: B1 cookie set on the admin host while Microsoft returned to the API host on the Container Apps topology; B2 two PKCE survivors. Round 2: redirect URI moved to the admin host (`env.dev.json:107` = `https://secuura02-demo-admin.kindtree-935b2ded.southeastasia.azurecontainerapps.io/api/m365/callback`); kintsugi/demo are single-host (not split). **On GO:** GO naming the head + landing `346c5104f2a7` on c66b834ed451 (re-check develop), verify the merge, R wraps, score + pane_close. **On NO GO (cap reached):** ship the closed instances, ticket the residue, no round 3 without Kam. **After the merge: card Kam for the Entra redirect-URI registration, quoting the literal URI above (his hands; m365 is live nowhere today).** KS-1381 (kintsugi's ENTRA redirect = localhost:6882) is its own open item. KS-1682 (m365 refresh token from a process-wide MSAL cache, High) is the next m365 PR.
- **C 30th (%15, Opus 5.5):** KS-1116 follow-ups in vc-issuer: (1) Kam ruled card `secuura-ks1116-null-owner-who-reads-1020` = a (tenant administrators, 08:19): follow-up PR changing `ownerlessRowReadable` to ORG_ADMIN/SYSTEM_ADMIN + tenant claim + the ROW's own tenant; legacy NULL-owner rows carry no tenant stamp, so C measures whether the tenant is determinable, else fail closed and Wednesday tells Kam if his option reaches no row; tier 1. (2) NOTE 1 test-only cells for BH1's three survivors, tier 2. (3) Tickets after board searches for BH1 NOTES 2, 3, 6. KS-1683 (High) holds the list/by-hash bound, waiting on a Platform S answer.
- **D 24th (%16, Opus 5):** posts ONE comment to Stuart on KS-695 ("has uat-ps reached aeae5ca?") and measures key_66e82ef0's last use on demo read-only (control key_61774985); then wraps. **On its report: come back to Kam with the key's last-use date (card ruled a = measure first, then come back); revoke nothing without his word.**
- **Demo deploy of a4187f0f6622: NOT GO** until Stuart notes uat-ps on KS-695. **Stuart's a8615d46 (KS-695): fix KS-1557 before or with that round** (develop's #1619 lineage check refuses a routine S certify on a /version-created parent). OWED: a KS-1557 fix lane before the demo round. D 23rd's handover `5_Project_History/2026-10-20_seatD-23rd/HANDOVER.md` (project tree) runs the demo deploy cold.

## 2. KAM'S CARDS
- All three Secuura cards of this morning are RULED (a, a, a at 08:19-08:20) and delivered or in flight to C 30th / D 24th. None open.
- Datasec `composer-l05-setup-card-too-1014` is Tuesday's.

## 3. OWED BY WEDNESDAY (in order)
1. BI1 verdict -> GO or cap handling (above). Then the Entra card for Kam.
2. C 30th's READYs -> gates (tier 1 for the predicate PR, tier 2 for the test-only one) -> GOs -> verify merges.
3. D 24th's report -> Kam (the key's last use) -> score + pane_close.
4. A KS-1557 fix lane (Stuart: before or with the demo round) and the next kintsugi round (#1640-#1648 + Peter's #1642: product = #1641, #1646, #1648 vc-issuer + migration 054, #1647 if it merges with migration 053; the 053/054 apply by filename; KS-1116's NOTE 4: 054 must run before the new vc-issuer starts).
5. KS-1682 (m365 refresh token) after #1647.
6. Fable 5.1 coordinator trial (routing decision 7) still OWED.
7. At the wrap: regenerate BOTH boot digests only if a lesson FILE was edited (today only the ledger); the 05:30 ledger archive.
8. KS-1665 (deploy.sh admin fallback) deserves more than Low before any production deploy; KS-982 archive is Kam's call. Not carded.
