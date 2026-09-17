SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation (Seat A 7th successor)
TS: 2026-09-17T11:43:21.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
Seat A 7th successor booted 11:37:04Z (PID 91353, pane `Secuura/Blockchain`). Every ref in your brief matches origin (ls-remote 11:38:59Z): develop `75ad0e55c`, #1028 `e39521cfb`, #1029 `cd3580e1f`, #1031 `be8596a29`, #922 `e60a24c50` (open), #1030 `e43af4934`. KS-1194 local = `c82f5edd5` (parents `29d9f90fa` + `75ad0e55c`); `raise-0916-a` is on that branch, porcelain 0. The v1.3 grant is re-verified at source. No write has been made except my own records folder and my daily-note block. I will run the queue as briefed, with one build default below for your veto.

## Recommendation
Confirm the queue and the item-3 default:
1. **#1028 / #1029 / #1031:** merge each ONLY on your signed GO naming its head, one at a time. Copy `merge_1026.py`, re-pin from the GO, and dry-run it first. Verify at origin, post ONE BLUF facts comment per ticket (it stays In Progress), and mail a MERGED receipt.
2. **KS-1194 into the first freed slot:** merge develop in again if it moved, then merge-tree, content re-read, and the auth suite at default AND 60 s ceilings. Then push, open the PR (`Refs KS-1194`, Test Evidence), run the POST-PUSH CHECKS and send READY tier 1. Merge only on the GO that relays Kam's tap.
3. **KS-1215 O3, local, now.** DEFAULT (veto): Linear's branch name `feature/ks-1215-api-gateway-a-revoked-session-jwt-plus-a-valid-key-whose` off develop `75ad0e55c`, built in my own `raise-0916-a` by branch switching (your 09:47:42Z acceptance). Porcelain is 0 at each switch, and WIP is committed locally, never stashed, before switching to KS-1194's push. Order:
   (a) run O1 against an unreachable exchange at runtime and record whether O1 == O3 on that row, before writing the cell;
   (b) cells on `/api/credentials` + `/api/documents`, each red at develop by assertion: N-1, split principal, the unreachable-exchange runtime cell (both shapes pass it), and controls;
   (c) tampers: a labelled STRUCTURAL tamper (module mock makes `getConnectorBearer` reject; the O1 variant reds, O3 does not), delete-removed (must red N-1), TI;
   (d) one production-mode row on `/api/v1`; `/api/batch/*` under NOT covered.
   Push only when a slot frees, after merging develop in again once #1028 lands.
4. **KS-805 + the KS-839 contract sentence:** wait for #922.
5. **Not touched:** KS-1217, KS-1219, KS-1220, KS-1204, KS-1101, KS-1212.

## Detail
- **Launcher preflight, verbatim.** The stamp is my own launch (`ps lstart` of my session = 21:37:04 AEST = 11:37:04Z):
----
# launch 2026-09-17T11:37:04Z
[F-02] No SSH identity available for git (keychain not seeded, on-disk fallback off).
       Run: ssh-add --apple-use-keychain ~/.ssh/secuura_blockchain_deploy_rw
       Or temporarily: export SECUURA_ALLOW_ONDISK_KEY=1 before launching.
       (git will use whatever core.sshCommand is already in the repo config.)
[KS-907] 2 other live session(s) on this project: PID 74217 (up since Thu 17 Sep 20:18:20 2026), PID 57090 (live claude session on this project).
         The boot git-sync is READ-ONLY this launch — it will NOT pull in 2_Project_Files.
----
  - The KS-907 line's PID 57090 is the #1028 QA gate (its argv: "fleet QA agent running ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1028 (KS-744, Seat A)"), not a seat. That is KS-1085 finding 2 again.
  - PID 74217 is Seat B 1st successor (pane `Secuura/Blockchain-B`). The repo key fetched rc 0 despite F-02.
- **Grant:** `<096604C5-237F-4467-9ECF-B79F975FCB11@me.com>` "Team collaboration", reached on page 15 of the inbox.
  - The raw Authentication-Results header reads spf=pass, envelope-from=kreiser.org@me.com, dkim=pass header.i=@me.com, dmarc=pass header.from=me.com. Each was checked as its own token.
  - The structured field is null (known).
  - Five controls (spf-fail, other envelope-from, dkim-fail, other dmarc domain, empty) each fail.
- **Brief:** structured spf/dkim/dmarc pass.
- **Shared checkout:** `feature/ks-597-b-caller-scoped-externalref` @ `355d82c8b`, porcelain 0, 0/0 against its origin branch, 173 behind origin/develop. Fetch only (rc 0): no pull, no checkout.
- **GitHub:** 22 open PRs.
  - Reviews endpoint (commit_id == head): 0 at-head approved + 0 changes-requested + 22 none/stale = 22.
  - Search index: approved [927] (Peter's approval sits at a stale head), changes_requested [887] (the reviews endpoint shows none; not my lane), none 20 (includes #1028, #1029, #1031).
  - The three lane PRs read mergeable=true, mergeable_state=unstable. That is noted, and it carries no testing claim.
- **Linear:**
  - attachmentsForURL: pull/1028 → KS-744 contributes; pull/1029 → KS-1180 contributes; pull/1031 → KS-1213 contributes; control pull/99999 → 0.
  - Lane states = the brief: KS-744 In Progress (0 comments); KS-1180 In Progress (last `da07a4c1`); KS-1213 In Progress (0); KS-1194 Backlog (last `05e914f9`); KS-1215 Backlog (0); KS-805 Backlog (0); KS-839 In Progress (last `ac3cf66c`); KS-1050 In Progress (last `d856751d`); KS-1208/1217/1219/1220/1204/1101 Backlog (0 each). None archived.
- **Board:** 82 active on the board account (In Progress 45, Todo 23, In Review 12, Blocked 2); backlog 302 (U1 H74 M155 L64 N8); completed <24h: KS-1130, KS-810, KS-793; 0 overdue.
  - All 93 KS comments in the last 24 h came from the shared account.
  - Non-shared-account updates <24h: KS-1167 (Done, Peter) and KS-588 (Backlog, Peter).
- **Audit fuses at develop:** lock-discovery `expires '2026-10-19'`. The baseline has 15 dated rows; the earliest is 2026-09-24 (×4, Seat B's lane). None falls on or before tomorrow.
- **Load and usage:** 1-min load 21.52 at 21:39 AEST; USAGE_STOP reads 90.
- **Extranet:** 6 tasks / 0 replies / 1 doc, all pre-existing. `/api/seen` NOT called: the SessionStart hook still instructs it, and I refused.
- **Vault:** `daily/2026-09-17.md` holds Seat B's uncommitted blocks. I appended mine and will stage only my own hunk at wrap.
- **Watcher:** since = 11:36:58Z (the last mail I read, your brief).

