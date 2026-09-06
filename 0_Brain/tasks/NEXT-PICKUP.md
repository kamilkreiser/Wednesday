---
date: 2026-09-07
type: pickup
source: replaced wholesale by the 00:1x post-rotation seat (updated ~00:5x)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 00:5x, both seats productive, F5 CONFIRMED (ripe for Kam), gate queue HELD; Kam asleep

**Time:** just past midnight AEST (mail timestamps are UTC ≈ AEST−10). Overnight coordinator seat.
**NO VOICE 23:00–06:00** (now enforced by `speak.sh` quiet-hours guard; `WEDNESDAY_SPEAK_URGENT=1`
overrides). Kam's standing words: "keep pushing the secuura agent to a ready state"; Opus-5 boot pin
"for the rest of the week" (credits; doctor WARNs after 2026-09-13).

## SEATS — both working (verify from objects; don't trust these SHAs)
- **Seat A (s141b, %130)** — was ~55% ctx. Shipped **KS-945 (PR #879 @ `79f1fcb48`, stacked on
  #876), READY FOR QA**; filed **KS-948** (its test names executed npm, broke the install — self-caught).
  Now on **KS-577 → KS-762** (bounded only; review streams + OAuth cluster held off it). Will rotate
  at its 80–85% band with a handover.
- **Seat B (s142, %134)** — ~28% ctx, Opus 4.8. **F5 fully resolved** (items 1+2 + six mounts) and
  **KS-486 swept**. Now on the **OAuth consent cluster: KS-798 → KS-799 → KS-841**, one at a time to
  READY, rotate at its band if mid-cluster.

## 🔴 F5 — CONFIRMED, and RIPE for Kam's morning ruling
Seat B confirmed on a locally booted REAL gateway (never demo): **`//` (double/multi-slash) skips the
path-scoped rate limiter on ALL 8 auth mounts and is normalised back to canonical in transit → handler
reached UNAUTHENTICATED and UNLIMITED** (12×200, counter never increments; canonical spelling correctly
429s). All 6 newly-driven mounts under public /api/auth. **KS-858 class.** The other 3 spellings
(%XX, ;matrix, %2F) skip the limiter but express 4.22.2 404s them — **curios, not exploitable.**
- **Two coupled decisions for Kam** (his existing card `secuura-f5-login-limiter-bypass` is the surface;
  a new card was NOT added — the card gate flagged Kam's prior Peter/Stuart writes, and I respected it,
  carrying this here + in the chat mirror):
  1. **Remedy:** A edge-normalise //-only at the gateway (as KS-858), raise KS-858→P1 [seat B's lean,
     my rec] · B fail-closed reject 400 · C per-predicate (NOT rec) · D fold into KS-858→P1.
  2. **Disclosure:** tell Peter/Stuart now WITH the fix option, or keep waiting. **Rec: morning, with
     the option.** External comms = Kam's signature class.
- **HELD pending Kam:** the ready-to-post KS-946 evidence comment (seat B wrote it, HELD — posting vuln
  detail to a board they may read is itself disclosure); KS-946 re-price to Blocker; **KS-733 must NOT
  close as "MFA throttled"** (its remedy is //-bypassable — keep open-with-a-bound or gate behind the
  KS-858 fix); KS-858→P1.

## 🟡 GATE QUEUE — HELD by choice, GROWING; batch it (fresh focused seat or the morning)
No tester running (go-slow + credits; not launching a stacked tier-1 gate late at night). PRs wait
harmlessly — nothing merges without a gate + Kam's GO. Run serially, tier-1 first:
1. **#876 (KS-930) tier-1 re-gate** — head moved twice before; re-read `ls-remote` before briefing.
2. **#879 (KS-945) — stacked on #876**; gate #876 first, then #879 rebased. Verify KS-948's fix is isolated.
3. **#874 (KS-926) tier-2 R2** (Kam's cap; findings as a class).
4. **#875 (KS-936)**, **#878 (KS-942)** tier-2.
Wrappers: copy `state/launch_qa_*`, python `str.replace` not `sed`, red-proof rc 6/7 both branches.
**Scoring is HELD until each gate runs** (09-01 rule: score after QA). Seat A's KS-945 + seat B's F5
deliveries are strong but unscored pending gate.

## KAM'S DESK — cards, all HOLD, none urgent
1. `secuura-demo-kam-admin-default-password` — demo admin password. Demo identity frozen.
2. `secuura-f5-login-limiter-bypass` — now RIPE (see F5 above): remedy + disclosure.
3. **KS-577 (#880, READY) — Stuart cutover + grace-window Option (escalation candidate, not a block).** Seat A built it; condition 1 is Stuart's cutover agreement + which `API_KEY_ROTATION_GRACE_SECONDS` (Opt 1 instant [Kam's default ruling] / 2 bounded / 3 S-side ack, not built). Merging as-is defaults Platform S to Opt 1. External contract = Kam opens it with Stuart. Held behind the gate.
4. **KS-762 — credential rotation date LAPSED 2026-09-05 (2 days), + the app-db-password switch decision.** Seat A correctly BLOCKED it (no PR): the switch is ruled HELD in-code (KS-165 + the guard header), all 3 conditions Kam's (switch / rotation / tell Stuart+Peter); atomic, cannot be incremental. Surface NOT unguarded today (guard passes reporting HELD). Lapsed rotation is the most actionable piece.

## KS-486 register — Kam disposition (from seat B's sweep, HELD)
Register is NOT uniformly stale (contradicts the earlier "2 of 2 stale"): KS-619/621/623 accurate
(valid low-pri hardening/trackers, KEEP); KS-652 premise moot (Actions retired → reframe as a
manual-gate-coverage question); the other 3 are Peter-owned/parked/tracker.

## 🟡 FIVE STALE RULED CARDS — Kam disposition at the real morning
Carried in seat B's successor brief. `secuura-ci-billing` (wait), `secuura-agent-github-identity`
(Kam org action), `secuura-dependabot-triage` (Peter's repo), `secuura-ks229-disclosure-mailbox`
(later/no-action), `secuura-ps-759-760-merge-owner` (Kam merges 2 Platform-S PRs). Mark `--delivered`
or re-rule; they've sat 1–2 weeks.

## THIS SESSION'S LEDGER (self-caught)
🔴 Quiet-hours voice violation at 00:16 (misread clock as morning) — `speak.sh` guard shipped +
exercised; framing errors corrected.

## STANDING NOTES
INDEX.md STALE (last real refresh 2026-08-11). Env does NOT persist across Bash calls — `set -a; . .env`
in the SAME command for any raw curl. Wednesday's key gets 403 on project inboxes (isolation) — send
success is the delivery signal; a tap ≤200 chars. Gate subject = SHA. New work = new branch. Never
delete — quarantine.
