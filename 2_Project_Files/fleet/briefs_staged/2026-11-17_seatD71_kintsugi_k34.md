# BRIEF: Seat D 71st, Secuura/Blockchain-D. Kintsugi deploy round k34: develop AT THE GO (Wednesday's reading fab4edcdcd07, PR 2187's squash) to KINTSUGI ONLY. Demo is NOT this seat's. No production. Written by Wednesday herself as a LEAN DELTA on Seat D 70th's stamped brief and record (round k33 -> k34); the usage gauge is 95%, so no drafter. Every fact names its source; Wednesday's reads are starting facts, not your verification. Wednesday touched no box.

## STAMP (Wednesday). Wins over every line below.
STAMPED by: Wednesday (the 14:52 rotation successor), 2026-11-17 15:12 AEDT (generated clock). Author's read; you are the second pair of eyes: say so if a line is wrong.
DEVELOP at the stamp: fab4edcdcd07 (gh api 15:1x). Kintsugi's REVISION head per D 70th's FINAL: caace2ef3d61 (k33).
FLOOR at the stamp: W 35th (-W, Sonnet, BUILD on the gateway's Redis log mask; never merges, so develop moves only if a merge seat launches: none planned today). No other D seat live.
USAGE: weekly gauge 95% (usage_gate --check, ADVISORY; hard stop 100%). Kam cannot switch accounts until Friday 2026-11-20. **Be frugal: carry D 70th's kit and evidence rather than re-deriving what has not moved; one build; no optional probes.** If `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check` reads 98%+ BEFORE the build starts, STOP and mail; once building, finish the round safely (never stop mid-swap).

## WHAT THIS BRIEF IS (read this first)
Seat D 70th's round, again, smaller. Read WHOLE: (1) D 70th's stamped brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-17_seatD70_kintsugi_k33.md` and its GO `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-17_D70_go_kintsugi.md`; this brief CARRIES them for everything it does not name (GO and pin rules, ITEM 0 shape, migration STOPs, rollback recipe, build order, the +15 min watch, census discipline, probe discipline, mail discipline, HOLDS, WRAP); (2) D 70th's record `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-17_seatD-70th/` (HANDOVER FINAL + FOR A SUCCESSOR, `tools/`, `evidence/`). Re-key the kit `_d70` -> `_d71` with its own `rekey_i0_d70.py` / `rekey_b_d70.py` method (counted, refuse on mismatch); dry until FAILURES=0; the box runner refuses every box but Kintsugi. **THIS brief wins where they differ.**
**Kit trap:** the kit carries k33's content. Before the GO, grep every tool case-insensitively for `k33`, `caace2ef3d61` used as the TARGET pin (it is now the PRIOR head), `49ebce7c227a5e3d` as the new idfp, `pre-20261117k33` as the tag to WRITE (it is now a prior to READ), the seven-service swap list, `REBUILT 7`, `k33v`; rewrite the census spec and swapset for this round's set. D 70th's traps (a)-(g) apply.
**Standing line:** your FIRST Bash call carries NO `cd`, and no later call does either. Absolute paths; `bash /abs/path/tool.sh`.
**Pushes nothing.**

## model: claude-opus-5-5
Deploy seat with box rights, routing row C6 (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md` line 96).

## NEW SEAT: you are Seat D 71st (lane Secuura/Blockchain-D, DEPLOY); trust `$TMUX_PANE`.
Ordinal (Wednesday, 15:0x): D lane maximum in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` headings = D 70 (control: S lane max S 88, W lane max W 34 before W 35th's wrap). Re-check at boot. `REC` = `.../5_Project_History/<machine date>_seatD-71st/`; `REC70` = D 70th's folder (read-only).
**Mail discipline:** act ONLY on Wednesday's mails carrying `(Seat D 71st)`. Mail to `wednesday-agent@agentmail.to` ONLY, prefix `[Secuura/Blockchain-D -> Wednesday]`, body line 1 exactly `Seat D 71st`, no secrets, no cc; read each mail back by id. You send NO message to any human; you comment on no ticket. Arm an inbox watcher as a TRACKED background task, name its pid. Plan confirmation = `QUESTION: plan confirmation (Seat D 71st)` with launcher preflight warnings VERBATIM.

## AUTHORITY (verbatim)
- **Kam 2026-11-17 15:09:07 (live board, view=wednesday), verbatim: "archive and deploy what you can"** (the archive half is a board seat's, not yours).
- **Kam 2026-11-17 15:11:24 (live board, view=wednesday), verbatim: "you have my permission to deploy anything that has been tested and is ready".**
- Kam 2026-11-16 16:55:27 (live board), verbatim: "thank you.  Deploy everything so all systems are up to date and continue with all the Secuura tickets you can" (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md`, the row "WEDNESDAY: deploy EVERYTHING", line 11; event-bound: ends when Kintsugi and demo both run develop as measured by a D seat).
- The October deploy grant, Kam 2026-10-05 16:21:39, EXTENDED 2026-10-19 18:22:57 "keep the grant alive until further notice" (same file, line 41); 2026-09-18 "deploy to kintsugi. this is the dev server so it should be the first to update".
- KS-535: Kintsugi NEVER shares demo's `PLATFORM_WALLET_MNEMONIC`. Phase 0 re-tag (`pre-20261117k34`) before building.
This seat acts on nothing until Wednesday's separate `GO KINTSUGI` mail naming Seat D 71st and the pin.

## WHY NOW
Kam's Done rule (card `secuura-done-rule-unit-pinned-deployed-no-live-check` = a) closes a fix only once it runs on Kintsugi. Since k33's pin caace2ef3d61, develop gained 5 squashes (gh api compare caace2ef3d61...develop: ahead 5, 14 files):
- 3e6146c3d2f8 PR 2136 KS-2151 (docs) · 49d8a7a981fd PR 2135 KS-1807 (docs) · 64cb8b88649f PR 2170 KS-1954 (**services/transfer**, 2 files; gate 307) · e36b3af9da59 PR 2075 KS-2083 (**services/auth**, 2 files; gate 254) · fab4edcdcd07 PR 2187 KS-1163 (scripts/Start_Up: start-secuura.sh waits for five more services; D 70th's successor note: reaches no image).
File groups: docs 5, Projects Documents 2, scripts 2, Start_Up 1, services/transfer 2, services/auth 2. **0 under packages/, 0 migrations** (re-measure).

## THE SERVICE SET (Wednesday's reading; YOU derive at the GO's pin)
- **Predicted REBUILT 2: auth and transfer.** BUT their running bases are OLDER than k33's (D 70th FOR A SUCCESSOR item 2: auth 61a3953e6d66, transfer 6185f0f1ace8), so derive each from ITS OWN base to the pin, not from caace2ef3d61: everything their images take in that range (packages/shared included, e.g. PR 2066's keyRevokePolicy.ts) arrives with them. Name every PR in each range in STATUS A.
- **The 12 held class-C services** (shared-only change, keyRevokePolicy.ts): HOLD again under Wednesday's option (i) unless their OWN code changed in range; re-run `census_reach_d70.py` (re-keyed) for them at the pin.
- start-secuura.sh (PR 2187): confirm it is in no image (Dockerfile COPY census) and whether the box's running start-up uses it; you do NOT re-run start-up. If it is in an image, STOP and QUESTION.
- STOP and QUESTION on: any service other than auth and transfer entering REBUILT by its own code; any migration in range; PR 2099 (migration 059) or 2195 content in the pin; vc-issuer or admin-frontend (auth's base-mates) pulled in by a shared change you cannot class.

## THE ROUND MECHANICS (carried from D 70th; named changes only)
Phase 0 tag `pre-20261117k34` + idfp computed and stated (predict it with the re-keyed idfp tool). ONE build batch (auth, transfer). Swap order: **transfer, then auth LAST** (auth ends sessions on role change: the edge for sign-in). Rollback in reverse. REVISION gains the k34 entry; `REVISION.pre-caace2ef3d61` kept. +15 min watch: error-level, restarts, OOM on the 2 plus 4 controls (api-gateway, originate, anchoring, billing). KS-535 at every step; anchoring StartedAt EQUAL.

## CONSEQUENCES TO NAME (for Wednesday's panel receipt; measured from the code at the pin)
- auth (KS-2083): a person's role change ends their existing sessions (say which sessions, measured from the diff, in one plain sentence).
- transfer (KS-1954): the escalation sweep leaves a step pending when its workflow cannot be read (one plain sentence: what a user would see differently, or "nothing visible").
- Anything else the derived ranges bring (name it).

## WEDNESDAY MUST RULE (default in brackets; none blocks STATUS A)
- W1 probes: [NONE run]. The auth change needs logins and role edits to show live (HOLDS forbid both). Report "not run" plainly.
- W2 pin policy: [the GO names develop's sha at its writing; later merges ignored].

## HOLDS (carried; named changes)
- **Kintsugi ONLY.** No tag, rsync, build, swap, probe, login or read on demo. Say so in STATUS A, STATUS B and the HANDOVER.
- No write on Kintsugi beyond the deploy itself (plus the card-1006 build-cache clear only if the DISK PLAN needs it). No database stopped; no credential created, rotated, revealed or printed — **this includes the Redis password: its rotation is a LATER seat's, after W 35th's mask fix is merged and deployed (Kam 14:45:06 card secuura-gateway-redis-password-in-log-1117 = a); do not read or print the gateway's Redis URL.** No login, no minted token, no role change.
- Stop-and-mail on: a REVISION head other than `caace2ef3d61`; a Phase 0 prior or idfp mismatch; a build failure (root cause, re-verify, never skip); a gate NOT EQUAL; free disk under 60,000 MB before the build (after the one card-1006 clear) or under 45,000 MB at any point; a migration or tracker mismatch (tracker 59, max 058 per D 70th); a KS-535 value other than `695d09df873ff42b` on anchoring or nft-certificate, a DEMO value present, or anchoring's StartedAt changed; a REBUILT set other than STATUS A's; a pin that is not the GO's.
- Wrap at your context limit (finish the item at ~70%, HANDOVER, wrap at ~75%).

## WRAP (carried, re-keyed)
History entry `## <machine date> - Seat D 71st` (newest first; duplicate guard with a control). `REC/HANDOVER.md` FINAL first, FOR A SUCCESSOR with per-service bases after this round and next stamp **k35**. Clone and scratch moved into `_quarantine_YYYY-MM-DD/` (nothing removed). Vault commit per the end-of-session skill. Wrap mail `Session wrap <date> (Seat D 71st)`, naming the next row: DEMO measured (the services and migrations between demo's d15 pin eb27110fc6e4 and develop), read-only, for Wednesday to post to Kam before any demo swap.

RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-11-17 15:09:07 (live board, view=wednesday), verbatim: "archive and deploy what you can" (kam_rulings_today.sh FRESHNESS 15:10:38).
- 2026-11-17 15:11:24 (live board, view=wednesday), verbatim: "you have my permission to deploy anything that has been tested and is ready". Wednesday's reading: tested and ready = merged on a QA gate GO and verified at source (both PRs here: gates 254 and 307). It does not lift the HOLDS (production, money, humans, irreversible, KS-535) and does not reach demo for this seat.
- 2026-11-17 14:45:06, verbatim: "Decision secuura-gateway-redis-password-in-log-1117: a — Rotate after the fix ships" (NOT this seat's to act on; named so you do not).
- 2026-11-16 16:55:27, verbatim: "thank you.  Deploy everything so all systems are up to date and continue with all the Secuura tickets you can".
- Notify-on-deploy (Peter/Stuart): HELD FOR KAM; this seat sends nothing to any human.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- D 62nd to D 70th's procedure, kit, census and fix-string rules; option (i) for shared-only class-C holds; D68-W4 (`docker exec` GET of a service's own `/health`, no POST); build seats never merge; migration 059 only on Wednesday's word; the 2026-11-17 STANDING LINE (no `cd`).

## UNMEASURED
The box today (REVISION, priors, running ids, free disk, KS-535 values, tracker) since D 70th's FINAL ~02:13Z; the auth and transfer ranges from their own bases; whether start-secuura.sh reaches any image; the exact consequence sentences; Linear state of KS-2083 and KS-1954.

PROVENANCE:
- develop fab4edcdcd07; compare caace2ef3d61...develop ahead 5, 14 files, commit list above | gh api repos/Secuura/Distributed_Secuura/compare (Wednesday, the Blockchain project's GH_CONFIG_DIR) | read 2026-11-17
- Kintsugi k33 state, per-service bases, priors, kit, traps | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-17_seatD-70th/HANDOVER.md lines 1-60 | read 2026-11-17
- PR numbers and gates for 2170 (307) and 2075 (254), 2187 reaches no image | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md checkpoint blocks 13:35-14:34 | read 2026-11-17
- grant rows (line 11 deploy EVERYTHING; line 41 October grant extended) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md | read 2026-11-17
- Kam's words 15:09:07, 14:45:06 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh FRESHNESS 15:10:38 | read 2026-11-17
- D lane max D 70 | /usr/bin/grep -a -o -i over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md headings | read 2026-11-17
- routing C6 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md line 96 | read 2026-11-17
- usage 95% | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check | read 2026-11-17

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-17 15:12
