---
date: 2026-11-03
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE ~07:48 AEDT 2026-11-03 by the morning seat (respawned 05:34; ctx 64%). Previous kept as NEXT-PICKUP.md.pre-1103-0748. Replace wholesale; never stack.
---

# NEXT PICKUP — Tue 3 Nov 2026, ~07:48 AEDT (morning seat)

## OWED FIRST (in order)
1. **Gate notes -> QUEUE -> GO chain** (every merge: QUEUE at NOTES PATCHED, then B 80th's READY, pre-GO checks, GO `GO: merge PR <n> at <head12> on develop <pin12> (Seat B 80th)`):
   - **PR 1964** (originate documents routes, T1, head 25c437f4): gate 149 GO WITH NOTES; R 77th asked to FILE one High ticket (G149-F1/F2 sign retry duplicates; F7 = existing KS-1831, not re-filed) + PATCH notes. QUEUE at its NOTES PATCHED.
   - **PR 1966** (W 20th item 1, prism/timestamping/security db.ts, T2, head 86986a55): gate 150 GO WITH NOTES; W 20th asked to PATCH notes. QUEUE at NOTES PATCHED.
2. **KAM CARDS OWED BEFORE MERGE** (each AFTER its Opus gate measures; same shape as card secuura-pr1961-erasure-skip-not-shredded-1103, which Kam ruled a in ~1 min):
   - **R 77th's PR 7** (api-gateway middleware: brute-force guard + limiter header-write move fail-CLOSED -> fail-OPEN for a hostile value; ordinary Error already fail-open; precedent KS-1256 = fail closed). Gate 148 at its READY (driver 73868 still queued).
   - **W 20th's PR item 4** (referral, T1 by its own raise: hostile value joins the ordinary path that RE-AWARDS qualifying milestones on a failed progress read and boots fraud detection empty). Opus gate at READY.
   - **R 77th's PR 10** (auth password.ts: isPasswordBreached -> false = fail OPEN). Opus gate at READY.
3. **Gates to commission at READY:** W 20th items 2 (demo-service), 3 (vc-issuer), 5 (m365 oauthState) = Sonnet T2; item 6 originate = T2; items 7 governance + 8 billing = Opus T1; item 9 transfer delegation. R 77th PR 8 (anchoring, T1 Opus; amend + test-only `vi` commit RULED), PR 9 (auth session, T1), PR 11 (security rotate, T1; R 77th tells me before building).
4. **Spark operator 91 RUNNING** (Sonnet subagent; workdir 0_Brain/reference/2026-11-03_spark-operator91/). If it dies at a rotation: check spark/done.md + night/ READY_*O91*, re-commission. Feed it: G149-F4 (documentRepo.ts unguarded reads), W 20th's generateCode unguarded reads (referralService.ts:257/:68), G150-F3 probeDb in prism/timestamping, G146-F2/G145-F3 test gaps are NOT Spark work.
5. wed_claim release for the Spark deps fix (operator 90's loops ended? check ps 13450/71347, commit their logs, then release).

## STATE (07:48)
- develop **7ad0dcc14e5c** (PR 1963). Merged by this seat's GOs today: 1957, 1958, 1959, 1960, 1961, 1962, 1963 (7); 1953 just before.
- **Live seats (all Sonnet 5.5):** B 80th %96 (merge, queue empty, ctx ~72%: B 81st brief from its HANDOVER when it wraps), W 20th %97 (raise, ctx 70%; items 1-5 built, 6-9 to go; W 21st from its HANDOVER when it wraps), R 77th %98 (raise; plan CONFIRMED; PR 7 READY at driver 73868 VERIFY, PR 1964 notes + ticket, PR 8 amend, PRs 9-11).
- Wrapped + scored + closed this seat: W 19th 0.94, B 79th 0.95, R 76th 0.93.
- **High tickets filed today from gate findings (all pre-existing, read back):** KS-1952 (gateway doc-type fail-open on Redis loss), KS-1953 (erasure lifecycle row under platform keyring), KS-1954 (transfer escalations silently timed out), KS-1955 (failed kyc/wallet-connector erasure unreported). Kam told once (combined FYI ~07:06): recommended KS-1953 + KS-1955 next for a fix seat.
- Spark harness FIXED 06:03 (deps store + LOCK KEY check; spark/build_deps.sh when develop's package files move).
- Kam ruled today: wed-morning-plan-1103 = a; secuura-pr1961-erasure-skip-not-shredded-1103 = a. Gauge 7d ~60%.

## RULES IN FORCE
- Before any GO: no un-MERGED GO outstanding; push_queue.sh list; gate_stray_check.sh rc 0; ls-remote pin + head.
- Launch seats with SEAT_MODEL_ENV=claude-sonnet-5-5 (id from models_latest.json). Read every drafted brief WHOLE; dry run; send gate format rules: PROVENANCE ends `| read YYYY-MM-DD`; no unsourced scope words; git ref names are not paths.
- New pre-existing High finding from a gate: board search first; file via the PR's own seat on Wednesday's word; read back.

## OWED (not first-work)
- WED-155 (credentials on curl argv, 9 scripts). gate_common.md cwd/logs note (G144-F7/G145-F6). msal half of the 11-09 baseline row: UNMEASURED, check before Mon 9 Nov. INDEX.md refresh. Ticket candidates for a board seat: the G139-F1 test-gap family (G141/142/143/144/150-F1), G145-F3, G146-F2, G149-F5, flow-fragment follow-ups (1961, 1963), earlier pickup list.
