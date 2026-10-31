STARTABLE: YES (after Tuesday fills 7 slots + the READ-WHOLE line; no question blocks launch)

# B1035 drafter report: SEAT-AT2, the one FOLLOWUP_DIGEST_TO write on datasec-attio-bridge

**BLUF.** Kit `2026-11-01_B1035_SEAT-AT2_attio-digest-recipient-setting-write.md` (91 lines, sha256 `aba35d15…d2b1b7`, byte-equal `.pre-stamp` by `cmp`). Opus seat, Vision's `AZURE_CONFIG_DIR` set per command line. Five fixed `az` lines (C1 account show, C2 role-assignment list at the RG scope, C3 webapp show, C4 appsettings list, C5 the one set), run only through a checker with four controls that must fail. Steps: identity 4x True/False, then the grant, then BEFORE (KV-ref / absent / already-equal flags and health), then C5 once, then read-back (equality, names + count, one digest over all other settings), then `/healthz` poll (10 min) for armed + restart proof. Every STOP stops the run; no undo, no restart, no vault.

## Facts (instrument + control)
- B1035 unused: `find` over `!CODING/Datasec` + `tuesday/` for `*B1035*` = 0 (control `*B1031*` = 2); today's daily note line 121 reserves B1035 for this kit. Suffix AT2: word grep `ATTIO-AT2|SEAT-AT2` over briefs = 0 files (control AT1 = 3).
- Vision profile (`python3 -I -B`, fields only): ONE subscription `0c57ab37…`, tenant `d500ebad…`, `servicePrincipal`, name prefix `bc1e3581`, default true. Full appId from the B1032 report :11 (RELAYED).
- Health payload fields: `src/index.js:64-97,161`, `src/followup/schedule.js:56-66,113-117` (a start arms the timer and does not run the job). `git log 7510401..HEAD` over index.js, config.js, schedule.js is empty, so main has the same code as the last proven deploy (commit 7510401, RELAYED from B1028).
- Fire time 21:00Z (`config.js:72-73`) = 2026-11-02 08:00 AEDT.
- Panes 10:3x: no Vision pane, no other ATTIO-AT pane. ATTIO-G255 is live: a code-only gate.
- Model: model-routing.md lines 96, 108, 145 and 47; models_latest.json line 17 `claude-opus-5-5`.
- The five lines checked against the checker's forbidden list by a scratch program: 0 hits; C3-C5 carry -g/-n; C1/C2 exempt by name.

## D-decisions (defaults if silent): D-1 fixed lines + checker; D-2 True/False only; D-3 one sha256 over the other settings, stored outside evidence; D-4 a KV reference = STOP; D-5 already equal = NOTHING TO DO; D-6 absent = STOP; D-7 one attempt, no undo; D-8 restart proof via `lastRunAt` / `runs`, else UNPROVEN and continue.

## Q (defaults)
- Q-1 Hard stop: default 20:00 AEDT today; the kit's floor is no write after 20:30Z.
- Q-2 D-3 digest of the other settings: default ACCEPT.
- Q-3 `az` writes logs and token refreshes into Vision's `.azure` (coupled pair): default ACCEPT.
- Q-4 Restart UNPROVEN ends DONE, and tomorrow's digest is the proof: default ACCEPT.

## UNMEASURED
Whether the grant still exists. Whether the setting is plain or a KV reference. The app's state. The live health payload. Whether the SP secret is still valid. Whether the deployed code has drifted since 08-24 (only the three files were checked).

## Outside the fences
Subject tag still `-> Wednesday` until a code deploy (B1028). The three missed digests are not re-sent. The webhook ledger resets on the restart.
