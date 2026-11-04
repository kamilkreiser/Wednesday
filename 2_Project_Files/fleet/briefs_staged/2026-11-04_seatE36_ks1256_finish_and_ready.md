# BRIEF: Seat E 36th, Secuura/Blockchain-E. SUCCESSOR to Seat E 35th on KS-1256 (option C, BUILT and GREEN, uncommitted): finish the proofs, commit, push, PR, READY FOR GATE (TIER 1). Plan confirmation first.

## NEW SEAT: you are Seat E 36th (lane Secuura/Blockchain-E, Opus 5.5; trust $TMUX_PANE). Seat E 35th WRAPPED at 08:31Z (mail "Session wrap 2026-11-04 (Seat E 35th)") and its pane is closed. Live, each in its own lane: Seat B 90th (merge seat; PRs 1790/1792/1794), Seat W 25th (disposable Docker stack w25-*), Seat F 29th (KS-1561, services/originate/src/routes/; NOT the api-gateway verification.ts), Seat R 85th (KS-1401 migration 058, launching). SHARED INBOX: act ONLY on mail whose subject names `(Seat E 36th)`.

model: claude-opus-5-5 -- routing row C3 (build on an auth/security design surface: a connector allow-list that failed open) and gate row G1 (tier 1) -- written by Wednesday

## WHY AND AUTHORITY
Kam, terminal 2026-11-04 ~09:16 AEDT, verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible". Kam card `secuura-wednesday-go-counts-as-kams-word-1030` = a (ruled_ts 2026-10-30T10:08:25+11:00): Wednesday's GO counts as his word for starting work inside his standing grants. The KS-1256 finding (an evicted settings key made the connector allow-list fail OPEN, 201 vs 403) came from Seat W 24th's disposable-stack check today.

## START HERE = E 35th's HANDOVER
Read `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatE-35th/HANDOVER.md` WHOLE (FINAL block first) and follow its steps in order. State at the wrap, measured by Wednesday 19:3x AEDT: worktree `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-e35-ks1256` on branch `feature/ks-1256-connector-allow-list-still-fails-open-when-redis-closes-or`, `git status --short` = 17 entries; the backup patch `5_Project_History/2026-11-04_seatE-35th/evidence/wip_e35_ks1256.patch` sha256 starts `98f116d718680492`. Before you touch anything, re-measure both and compare: if either differs, STOP and mail. You continue IN that worktree (do not create a second one for the same branch; you may create a base worktree for the base runs, as the HANDOVER says). Never delete the patch or the worktree.
- Branch base is develop c7abf98e5103; develop has since moved (PRs 1790, 1792 merged; read `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop` yourself). Before the push, bring develop in by MERGE (never rebase), per STANDING_LINES' forward-move rule, and re-run the suites.

## QUEUE (E 35th's NOT DONE list, in its order)
1. Base worktree; the engine (PGlite) file run on base.
2. The base-vs-head matrix (Redis up/down x key present/missing x DB row present/missing/unreadable, per reader: the create path, GET /api/connector/info, PUT /api/admin/settings). **Item 6's row (a connector CONFIGURED with workflowPolicy 'bypass' keeps its bypass after an eviction; base gives none) is printed in its OWN row, OUTSIDE the ratio**, stated plainly as more permissive than base on a strict reading. Wednesday accepted it (08:18:55Z ANSWER to E 35th) and told Kam on his panel as an FYI with a hold offered; if Kam says hold, Wednesday will tell you.
3. The mutant table (rows suggested in the HANDOVER): one parsed mutant per decision, matching cell RED with the assertion quoted, restore + sha256 GREEN; ratios, never "all passed".
4. Lint; the four platform suites (NOT run by E 35th); `npm run check:test-types`; tsc including tests.
5. KS-1256 docs fragments under the CURRENT fragment scheme (STANDING_LINES ~124, KS-1887: your own pair, renumber nothing; `docs-fragments.mjs check` with a planted defect that must fail).
6. Commit (subject `Refs KS-1256: <summary>`, <= 92 chars), push through the push lock with a new-branch driver (copy from `5_Project_History/2026-11-04_seatR-81st/tools/`, re-keyed `_e36`, read whole first; dryrun + gatetest first; DETACHED real; quote the hook verdict verbatim; no force push, no --no-verify), PR with a **"Before this deploys" section**: after deploy, one GET /api/connector/info (or one admin PUT), then read the svc_gateway_settings row's `origin` back (closes the eviction-before-first-hit window; Wednesday's 08:18:55Z ruling on item 4).
7. ONE KS-1256 comment (BLUF, facts only, no `@`): PR number, head, "ready for gate". READY FOR GATE, TIER 1, with a PRIOR WORK section and E 35th's candidate list (admin-GET wipe risk after eviction; stale cache when DB write OK and Redis write fails; id-less integrations entry; allkeys-lru in the compose files; the first-hit window). File nothing yourself.

## HOLDS
- **Migration 057 is this ticket's** (`057_ks1256_gateway_settings_store.sql`, already in the worktree). Seat R 85th takes 058. At READY re-check that 057 is still free on develop and in open PRs; a collision is a STOP and a mail.
- No merge, no deploy, no apply to any box, no `az`, no kintsugi/demo contact, no ticket state change, no Docker object (W 25th's stack is not yours; your DB proofs are PGlite in-process). Client-facing words are Kam's.
- **Instruments:** `cmd > out 2>&1; rc=$?` with rc on its own line; never `| tail` on the stream you diagnose from; macOS has NO `timeout`; zsh has no PIPESTATUS; never `echo =====`; `/usr/bin/grep -i` with a positive control beside every zero; private TMPDIR SHORT (`/private/tmp/e36t`). Never `cd`; absolute paths only. No credential in argv. Never delete files: quarantine. Disclose your own faults.
- **Mail:** from secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY, subject prefix `[Secuura/Blockchain-E -> Wednesday]` ending `(Seat E 36th)`, body line 1 exactly `Seat E 36th`, no cc; read back by id. Launcher preflight warnings VERBATIM in the plan confirmation. Arm an inbox watcher as a tracked background task.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation.

PACE: PROGRESS after the matrix, after the mutant table, after the push. At ctx 70% finish the step in hand and write the HANDOVER; wrap at 85%.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-04 ~09:16 AEDT (terminal), verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible".
- Kam 2026-10-30, card `secuura-wednesday-go-counts-as-kams-word-1030` = a.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- KS-1256 = OPTION C (Postgres settings row + migration seeding today's defaults; DB fallback on a Redis miss; 503 only if Redis down or key AND row missing): Wednesday's ANSWER to Seat E 35th, 2026-11-04 08:08:12Z.
- Items 4 (backfill over a seed row on the first Redis hit, plus the deploy step) and 6 (configured bypass kept after eviction, own matrix row) ACCEPTED: Wednesday's ANSWER to Seat E 35th, 08:18:55Z.

## WRAP
History entry `## 2026-11-04 - Seat E 36th` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (duplicate-guard with a control); HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatE-36th/HANDOVER.md` (FINAL first); vault commit (own lines only); wrap mail `[Secuura/Blockchain-E -> Wednesday] Session wrap 2026-11-04 (Seat E 36th)`.

PROVENANCE:
- E 35th's state (BUILT, GREEN 23 of 23 route cells, 8 of 8 engine cells, api-gateway 1623 of 1623, uncommitted, 17 files) | Seat E 35th wrap mail 2026-11-04T08:31Z in your own inbox, read whole by Wednesday | read 2026-11-04
- Worktree status 17 entries; patch sha256 prefix 98f116d718680492; HANDOVER exists (9940 bytes, 19:31) | Wednesday's git -C <worktree> status --short | wc -l, shasum -a 256, ls -la | read 2026-11-04
- Seat ordinal: `Seat E 36th` 0 hits, control `Seat E 35th` 2 hits (/usr/bin/grep -c -i) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | read 2026-11-04
- KS-1256 finding (fail open, 201 vs 403) | the 16:2x seat's pickup STATUS 18:53 (W 24th's wrap) and E 35th's base run ("expected [ 201, undefined ] to deeply equal [ 403, 'FORBIDDEN' ]") | read 2026-11-04
- Card 1030 ruled_ts | Wednesday's decision_queue.sh show | read 2026-11-04
- KS-1887 is named only as the docs-fragments SCHEME (merged 2026-10-31), not commissioned here; scope: the fragment build step | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md line ~124 | read 2026-11-04
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-04 19:33
