# Gateset 2026-09-29_gate42b — README for Wednesday

Written 2026-09-29T06:50Z by the drafter (times from `date -u`). Every figure below is read from the kit's own output files, each named beside it.
The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory (text files only) and scratch under its session scratchpad `g42b_sp/` (`clone` — `git clone --shared --no-checkout` of Wednesday's `screen0929/base` clone, fetched from origin ONLY there with the Secuura deploy key; the extracted blobs under `fuse/`; the control plants under `controls_*`). It did NOT write the routing line (§4).
The Secuura checkout was touched by read verbs only (`ls-remote` in the launcher, the repin and final_lsremote_1.out). GitHub: REST GET only (gh_read_1.json; the launcher's compare; the repin's PULLS reads). AgentMail: ONE read-only listing of wednesday-agent@ and secuura-blockchain@ (_mail_list_1.out) and four by-id GETs (capture_mail_gate42b.py); no seen-state touched, nothing sent. No npm advisory call was made: legs 6 and 7 were NOT run by the drafter (the gate owes them).

**gate42b = ONE PR, Tier 2, round 1 of 2. #1340 KS-530 + KS-729 + KS-528, the audit-baseline re-date Kam signed. It MUST MERGE before 2026-09-30T00:00Z (the fuse). Merge order: #1340 ALONE.**

| PR | tickets | tier | head (ls-remote pull/head == branch == API == fetched) | base | files | subject declared -> lands |
|---|---|---|---|---|---|---|
| #1340 | KS-530 + KS-729 + KS-528 (all `Refs`) | T2 | `9199a2f9f7394cdd2c78b5134e68ff7ba3e91fae` | develop `2cb858335472` (== merge-base; 1 commit ahead, 0 behind) | 1 (`Blockchain/Dev/scripts/audit/audit-baseline.json`, +8/-8) | 68 -> 76 |

Pane `QA/Secuura-batch1340` (**NOT routed by the drafter** — §4). GO string, as the GO mail's SUBJECT: `GO (Seat B 44th): merge 1340 on gate42b`. Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-29-batch1340-g42b/`. Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE42b batch #1340 (Seat B44, round 42b; T2: KS-530 the audit-baseline re-date, round 1 of 2)`.

## 1. BLUF
- **Kit: READY to launch once the routing line is added (§4).** Launcher `--check` rc 0 (launcher_check_1.out: `all guards pass:`); repin `--dry-run` rc 0 (repin_dryrun_1.out: `DRY RUN COMPLETE 2026-09-29T06:42:49Z`; routing line reported absent, the only thing the real run would refuse on; 1037 minutes to the fuse at that moment).
- **Pins** (pin_1.out, rc 0, 2026-09-29T06:37:35Z): head `9199a2f9f7394cdd2c78b5134e68ff7ba3e91fae` == the commission's; develop `2cb858335472fafcce535ca4ad328c897ed87bfb` == the commission's (tree `438bc1254bbf…`, which is gate42's END_TREE, so #1339 landed as predicted). The head's one commit's parent is develop. `git merge-tree --write-tree`: CLEAN, **END_TREE `09c593f29fd4ecf1691d99e961bfa060812932c8`** (== the head's own tree); diff(develop, END) == the one path; baseline blob `2230ad84181b` -> `5aca4edb6128` (END blob == head blob).
- **Heads re-read at the end** (final_lsremote_1.out, 2026-09-29T06:49:51Z): develop `2cb858335472…`, pull/1340/head and branch `9199a2f9f739…`. Every pin is still current.
- **Controls, both ways** (controls_gate42b.sh, one unedited script, sha256 `69082d78cbd8…` before the first run and after the second, controls_sha.txt):
  - normal (controls_1.out, rc 0): `SUMMARY gate42b: 51 controls, OK 51, MISMATCH 0`
  - `--invert` (controls_2.out, rc 1): `SUMMARY gate42b: 51 controls, OK 0, MISMATCH 51` (every control can fail).
- **Requirement 1 + 2, field level vs Kam's mail** (fieldcheck_1.out, rc 0): `FIELDCHECK PASS: 24 checks, 0 FAIL, 4 row(s) checked field by field`. The four ids are PARSED from Kam's text (never hard-coded): exactly those four rows differ; on each only `expires` and `reason`; `ticket` equals the ticket Kam named each under (frvp KS-530, mwp4 KS-729, wrjc + 337j KS-528); each `reason` is the old reason plus an appended tail quoting the instruction verbatim with the Message-ID; 25 rows before and after, the same ids in the same order; `$comment` and the top-level keys unchanged; one file. No head row expires on or before 2026-09-30.
- **The authority** (capture_1.out, rc 0): Kam's mail read by id from secuura-blockchain@, from `kreiser.org@me.com`, 2026-09-29T04:14:47Z, `<EB856837-268F-4CC7-B167-BE74B4824634@me.com>`; the instruction is present verbatim (whitespace-normalised). DKIM and DMARC were NOT re-read (the API exposes no raw headers to this drafter). The PR relies on the seat's reading of them.
- **Requirement 4, the drafter's offline fuse predicate** (fuseproof_1.out, rc 0: the repo's own `baseline-contract.mjs` at the head, under the kit's preload; NOT legs 6/7). The rows that CAN lapse: develop @ 2026-09-30T00:01Z -> frvp + mwp4; head @ 09-30T00:01Z -> none; head @ 10-08T23:59Z -> none; head @ 10-09T00:01Z and 10-10T00:01Z -> the four. The preload's positive arm (CK0, CK4) and its refusals (CK1 unset, CK2 garbage, rc 97) are in the controls.
- **Requirement 5** (keyscan_1.out, rc 0): subject keys {KS-530}, no `(#n)`, declared 68, lands 76 (≤ 92). The mandated body carries exactly `Refs KS-530` / `Refs KS-729` / `Refs KS-528`, no closing keyword, and no foreign key.
- **Requirement 6:** END_TREE above. **Overlap census** (repin step 2b): none of the other 20 open PRs touches the baseline file.

## 2. Doubts the drafter found (each READ or MEASURED)
1. **The head COMMIT MESSAGE is stale against its base (READ).** It was written on the pre-#1339 develop `8af6ab82` and says "2 LAPSED" at base and "ALL SIX ARMS EXIT 1… five advisories un-baselined at develop". The PR body and the READY carry the post-rebase table (base 1 lapsed, rc 1 -> head rc 0; real-clock legs 0/0). The seat reports the commit message as byte-identical across the rebase (by `cmp`). So the squash body must be COMPOSED, and the prompt forbids pasting the commit message. kit.json `mandated_body` is a clean minimum.
2. **mwp4 is inert (READ, the seat's own correction).** After #1339 the ip-address advisory is no longer reported, so its row cannot lapse whatever its date. It is re-dated because Kam named it. The gate measures which re-dated rows actually lapse at 10-10: the READY says 3 for leg 6 and 2 for leg 7.
3. **`isLapsed` is `expires <= today` (READ).** The new fuse is **2026-10-09T00:00Z (10:00 AEST, 09 Oct)**, not the end of 09 Oct (arm head-1009: all four can lapse at 00:01Z). This is a new deadline Wednesday should track. It is not a defect of this PR.
4. **Leg 6 spawns `npm audit` as a child (READ).** Passing the preload through NODE_OPTIONS would also freeze that child, so the prompt tells the gate to pass it on the node command line and say which way it used. `audit-gate.mjs` / `audit-locks.mjs` honour `AUDIT_BASELINE_PATH` (READ). The gate may use it as a cross-check, but its base/head arms run on real worktrees.
5. **The CLEANUP rows** (GHSA-v2v4-37r5-5v8g, GHSA-mwp4-54f8-5fhr) that leg 6 advises removing are left alone, which is out of scope. The seat lists their removal as owed. The prompt asks the gate to rule whether it blocks (prediction: no).
6. **The real legs read the live npm advisory database.** A new advisory published today would red base and head alike. The prompt makes the gate name it and rule on it.
7. **GitHub `mergeable_state: unstable`** (gh_read_1.json; mergeable True): CI does not start on this account, the same as gate42.

## 3. Pins and what the gate owes
- The prompt `2026-09-29_secuura-batch1340.prompt.txt` (17284 bytes, sha256 `63e8e5c7980a…`) names Wednesday's six requirements by 23 keywords. The launcher refuses a prompt that is missing any of them (exit 33), is missing Kam's instruction verbatim or the Message-ID or the fuse (34), the HOLDS (39), the GO (26) or the addendum rules (25). `## MERGE ADDENDUM` must be ONE LINE at the end of the report.
- Launcher `launch_qa_secuura_batch1340.sh` (10119 bytes, sha256 `38dc243f65a7…`); capture `mail_gate42b_ready.md` (13846 bytes, sha256 `99d84efb6451…`); COMMISSION.md (filled).

## 4. Routing line — NOT added
Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (after line 148, `QA/Secuura-batch1339r2…`). Back up the file first:
```
QA/Secuura-batch1340|coagent@agentmail.to|yes
```
Until the line is present, the launch action's step 0 refuses with rc 1 (control R1 measures that refusal on an empty routing file). The dry run found no other refusal.

## 5. Controls: `controls_gate42b.sh <scratchpad> [--invert]`
- FC0–FC11 fieldcheck on the real subject and on plants: a fifth row re-dated, a `ticket` changed, a wrong date, a row deleted, a top-level key added, a second file, one named row NOT re-dated, Kam's text with an id swapped, a reason edited rather than appended, `$comment` touched, frvp left at 09-30. Each refusal must name its own defect (`/why`).
- KS0–KS6 keyscan: `(#n)` suffix, foreign key in the subject, over-length, a missing `Refs`, `Closes`, a quoted leg-6 CLEANUP line (KS-470).
- CK0–CK4 preload: the positive arm through the repo's own `utcToday()`, refusal when unset or garbage, the real clock without the preload, `Date.now()`/`new Date()` frozen.
- FU0–FU6 fuse predicate arms (and two wrong expectations that must NOT match).
- L0–L11 launcher: wrong head (6), moved develop (17), wrong compare paths (10), a foreign GO (26), an unfilled token (8), a dropped keyword (33), an altered Kam text (34), a capture without the head (20), a dropped HOLD (39), the real launch path non-TTY (21), develop not in full (31).
- R0–R5 launch action: dry run (0), real run without the routing line (1), a baseline overlap via the census path override against the real open PRs (15), a stale head pin (11), a moved develop (10), a bad scratchpad (9).
- PN0–PN1: the pin script refuses a head it was not given and leaves pins_gate42b.json unchanged.
- Not controlled: the usage gate (5), `cockpit.sh add` (7), the override refusal (4) on a real launch, a `mergeable=False` refusal, the real re-pin across a develop move (the pin script's P6 path).

## 6. Could not measure
Legs 6 and 7 (real clock or frozen) and `npm run audit:contract`: no advisory call was made. The DKIM/DMARC headers of Kam's mail: not re-read. The seat's `cmp` of the pre/post-rebase diffs: not re-derived. Every leg figure in the READY and the PR body is the seat's claim.

## 7. Files
- Config: kit.json · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md
- Pins: pin_gate42b.py -> pin_1.out (+ .rc), pins_gate42b.json · final_lsremote_1.out · gh_read_1.json
- Checks: fieldcheck_gate42b.py -> fieldcheck_1.out · keyscan_gate42b.py -> keyscan_1.out · clockfreeze_gate42b.mjs + fuseproof_gate42b.mjs + run_fuseproof_gate42b.sh -> fuseproof_1.out
- Capture: capture_mail_gate42b.py -> capture_1.out, mail_gate42b_ready.md · _mail_list_1.out
- Prompt and launcher: prompt_gate42b.TEMPLATE.txt, launcher_gate42b.TEMPLATE.sh.txt, fill_gate42b.py -> 2026-09-29_secuura-batch1340.prompt.txt + launch_qa_secuura_batch1340.sh (fill_1.out), launcher_check_1.out
- Launch: repin_and_launch_gate42b.sh -> repin_dryrun_1.out (+ .rc) · launch_064513.routing.out / launch_064802.routing.out (written by control R1's real run, one per controls pass)
- Controls: controls_gate42b.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt

## 8. The ONE launch command (after the routing line, §4)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate42b/repin_and_launch_gate42b.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate42b/launch_qa_secuura_batch1340.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/35f90900-da39-4310-a097-bf496fc89a5b/scratchpad
```
- For a dry run, append `--dry-run` (repin_dryrun_1.out is one, rc 0). Argument 2 may be ANY existing Claude session scratchpad (`/private/tmp/claude-501/*/scratchpad*`). If `g42b_sp/clone` is absent there, pin_gate42b.py rebuilds it on a re-pin.
- If develop moves, the launch re-pins in the same action (step 3b: pin, then fill). It refuses rc 10 if the move touched the baseline or the merge is unclean. A moved #1340 head refuses rc 11. Another open PR touching the baseline refuses rc 15. Launching after the fuse is allowed with a WARNING: the base legs are red by design at that point, and the gate time-stamps every leg.
