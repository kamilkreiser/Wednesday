# B259 DRAFTER REPORT · HPSM-POC · QA gate (tier 1, one verdict per ticket, round 1 of 2 each) on b258/bff-imports-zstd-census @ 7fa59c5
Drafter, 2026-10-18 08:01-08:1x AEDT. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B259_SEAT-G4_hpsmpoc-gate-b258.md` (156 lines; template B252 134). B259 was free in both briefs folders (`ls | grep -c B259` = 0 before writing). Nothing was written under `!CODING/`. Git: read verbs only (`--no-optional-locks`), against `2_Project_Files` and B258's clone `.tools/b258/repo` (the branch object is only there). `gh api` GETs ran under HPSM-POC's `GH_CONFIG_DIR` (`kamilDatasec`). No Jira GET, no az, no HTTP to any app host. One scratch download: records CLARIFICATIONS at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/9e887f90-2566-4766-abd8-efc53c455a0b/scratchpad/clar.md`.

## Measured
- **`ls-remote` 08:02:41:** `b258/bff-imports-zstd-census` = `7fa59c5f65c93fef1d8587b918f6837df8864072` and main = `787d159089d8a774801b03e959f269c8a12e4ce1`. Both equal the commission. `7fa59c5` is NOT in `2_Project_Files`' object store; it is in `.tools/b258/repo`.
- **The range `787d159..7fa59c5`:** 6 commits, one per ticket, in queue order. 10 paths, +411 −27. Head tree `a083966f7157`. Merge-base `787d159`. Each commit touches only its ticket's paths (`diff-tree`), and -261 and -266 touch tests only.
- **GitHub, 08:03:** 0 open PRs, 0 check runs on `7fa59c5`, 0 open code-scanning alerts. Records main is `2e284455` (#118, 1,342 lines, highest heading C-111).
- **Decision queue, 08:03:38:**
  - 42 ruled HPSM-POC cards have no delivered mark, the same set as B258's brief.
  - `require-sqlserver-ci-check-1006` and `steve-dbs-pdfs-cleared-for-ai-1016` each have 0 matches in records CLARIFICATIONS.
  - `hpsmpoc-hosted-runtime-10013-1017` is OPEN.
- **Machine:**
  - Load 3.12 at 08:04 and 5.00 at 08:07. 8 cores.
  - `lsof 6900-7399 LISTEN` shows only `ControlCe *:7000`.
  - `b258-mssql` and `b258-azurite` are Exited and hold no ports.
  - `.tools/.git-lock` is absent.
  - Cockpit shows `tuesday`, `Datasec/NexusAI-O` and `fleet-monitor`, and no HPSM-POC pane.
  - `.env` has 28 names: 0 `AGENTMAIL_API_KEY`, and the 3 `JIRA_*` present.
- **Toolchain:**
  - node 24.21.0, SDK 10.0.401, Python 3.14.7, zstd 1.5.7, gitleaks 8.30.1, Docker 29.7.2.
  - Images: mssql `2b5b58162112`, azurite `830430c1da1a`.
- **Lineage sha256:**
  - `b250/lock.sh` `d9df031b…`, byte-equal to the b252 and b258 copies.
  - B252 fixtures a, a2, c and h match `check7_255/fixtures-sha256.txt`.
  - B252's probe, wire rig, `lostnames.py` and `addedscan.py`: the hashes are in the brief.
- **Code reads at `7fa59c5` (each `file:line` in the brief re-read):**
  - `isFilePart` `formGate.ts:125-133`, `headerParams` `:74-105`.
  - `guard.ts:19-22`, `:25`, `:38-43`.
  - Phase-3 catch `ImportEndpoints.cs:191-197`, `SaveIfStillPendingAsync` `:219-238`, `FailAsync` `:245-265`, the import-off gate `:422`.
  - `deploy-package.py` skip loop `:458-465`, refusal `:466-468`, drain `:478`.
  - `"empty"` was already in the refusal at `787d159:…:459`.
  - The F-6 literal is `Reporting/Report/ReportModelBuilder.cs:457`; its call is on `:456`.

## Corrections to the commission and to the claims
1. **No port conflict from B258.** "If b258 containers still hold 6982/6983": they hold no port (Exited). I still put the gate on **7140-7149**, off every lane used on 15-18 Oct (0 brief files name a `714x` port).
2. **The B252 row table is a, a2, b…i,** not a…i. Gate B252 added a2 (the 1 MiB-blocked tar), and its M1 claim rests on it.
3. **B258 F-7 cites the import-off gate at `ImportEndpoints.cs:411`, `:419`.** At `7fa59c5` those lines are a log declaration and a brace; the check is at `:422`. The brief asks the gate to record this drift.
4. **The ticket line numbers are off by one at tip:** BracketSuffix is `:941` (ticket `:940`), Anaphora `:308` (ticket `:307`).
5. **F-3 is reachable only at tip.** At base the exhaustion never reaches `FailAsync`. So F-3 is new reach, not a regression of -262, and the brief grades it as a ticket candidate unless the ticket's own shape regresses.
6. **QA/Vision-gate23 is no longer a live pane** (cockpit, 08:04), although B258's stamp named it. The only other live seat is NexusAI-O, as the commission says.

## Traps put in the brief (beyond the template)
- **T-a (-260):** "fail toward counting" counts ANY unparseable first disposition, including a `name="feedback"; filename="x\"` part and a `name="files\"` part. Exactly 20 MiB of files plus such a part could be a BFF 413 that the API accepts. That is the commission's "finding" class, and the brief has the gate say whether a browser can send it.
- **T-c (-265):** a type that is no longer a form drops to the JSON path. A body over 64 KiB gets 413 "over 64 KiB" before any 415, and its 403s do not close the connection. "Same verdict" therefore needs a status AND title comparison, row by row.
- **T-d (-265):** joined Content-Type headers (`…; boundary=b, text/plain`), tab, bare `;` and quoted types, measured on the real API.
- **T-g (-264):** truncated size, size past EOF, size 0, two skippable frames, the range's top (`0x184D2A5F`) and just outside it (`0x184D2A60`), skippable + gzip, + not-tar, + trailing bytes. Each must be refused with the existing words, byte-equal.
- **Shared lineage:** the builder ran B252's own mutant texts, fixtures and row harness. So every ticket gets the gate's OWN mutants (3-4 per ticket, named in the brief). B252's M1 and M251-3 are used only for the F-5 claim and as controls.

## Decisions left for Tuesday
1. **Verdict-token form.** The commission asked for GO / GO WITH FINDINGS / NO GO per ticket. I wrote the last line as `VERDICT: B259 b258 on main <sha7>: HPSMPOC-260 <token> · … · HPSMPOC-266 <token>`, which is not the template's single-token form. Change it if the records seat parses a different shape.
2. **The -265 wire leg.** `npm run build` plus the standalone server is heavy under the load-below-8 rule. I made it conditional (NOT TESTED if the load forbids) rather than mandatory. Rule it mandatory if a GO on -265 should require it.
3. **SQL Server shard 1** is "if load allows", as the commission says. If it is skipped, the gate reports NOT TESTED, and CI on the PR decides.
4. **How T-a over-refusals are graded.** I wrote Minor if a browser's FormData can send it, and Note if it is crafted only. B257's bar (B252-1 = Minor) is quoted beside it.
5. **-266 "no action".** B258's brief allowed Tuesday to close -266 as "no action". The gate grades it anyway. Close it on the gate's word if you prefer.

## Launch
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-G4 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B259_SEAT-G4_hpsmpoc-gate-b258.md'"
```
Before launch, Tuesday:
1. Reads the brief WHOLE.
2. Re-stamps its SELF-CHECK line, which is unstamped.
3. Re-reads `ls-remote`, cockpit `status`, `lsof 7140-7149`, `.tools/.git-lock` and the load.
