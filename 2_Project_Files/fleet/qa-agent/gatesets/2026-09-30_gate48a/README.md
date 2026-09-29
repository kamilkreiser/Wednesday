# Gateset 2026-09-30_gate48a — README for Wednesday

Written 2026-09-29T22:48Z by the drafter (all times are from `date -u`; the kit is dated by AEST, 2026-09-30). Every figure below comes from the kit's own output files, and each is named beside the figure.

**What the drafter did and did not do.**
- The drafter launched nothing, added no routing line, sent no mail, tapped no pane, and merged, committed or pushed nothing. It posted nothing, changed no ticket or PR, and deleted nothing. Superseded outputs were renamed (`superseded_*`), not removed.
- It wrote only two places:
  - this kit directory (text files only);
  - scratch under its session scratchpad `g48a_sp/`. That covers `clone`, a `git clone --shared --no-checkout` of the `407373b1…/screen0929/base` clone, fetched from origin only there (develop and `refs/pull/1354/head`). It also covers the synthetic control commits (plumbing in that clone) and the control plants under `controls_<HHMMSS>/`.
- Nothing was written inside `/Volumes/DevMASTER/!CODING/`:
  - The Secuura checkout was touched by `ls-remote` only.
  - The seat's record folder `5_Project_History/2026-09-30_seatB-47th/` was read only (the READY copy, `ks470/`).
  - gate47's report was hashed only.
- External reads were all read-only:
  - **GitHub:** REST GET only (gh_read_1.*, the launcher's compare, the repin's PULLS reads), plus public GETs of the advisory API.
  - **npm:** public GETs of the registry metadata for js-yaml 5.2.3 / 5.4.2.
  - **AgentMail:** ONE read-only listing of wednesday-agent@ (_mail_list_1.out) and eleven GETs by id (capture_mail_gate48a.py). Nothing was sent.
- The drafter ran no install, no audit, no docker build and no regen. Its only measurements are git plumbing and JSON parses of blobs, plus the registry and advisory reads.

**gate48a = ONE PR, #1354 (KS-470, T2), authored and merged by Seat B 47th (pane %77). It is ROUND 1 of its own PR.**

| PR | ticket | tier | head (ls-remote pull/head == branch == API == fetched) | parent | ahead / behind | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1354 | KS-470 | T2 | `4370be410bbf37b839b1030f3e28f95d11c454fe` | `37205947ddd2` (= develop) | 1 / 0 | 2: audit-baseline.json +7/-0, performance/package-lock.json +3/-3 | 81 -> 89 (PR title == commit subject) |

- Pane `QA/Secuura-batch1354`. **The drafter has not routed it** (see §4).
- GO string, used as the GO mail's SUBJECT: `GO (Seat B 47th): merge 1354 on gate48a`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-30-batch1354-g48a/` (it does not exist yet).
- Verdict mail: FROM coagent@ TO wednesday-agent@. Subject: `[QA -> Wednesday] GATE48A #1354 (Seat B47 author and merger, round 48a; T2: KS-470 js-yaml 5.4.2 fixed, undici GHSA-r53p accepted to 2026-10-09)`.

## 1. BLUF
- **Kit: READY to launch once the routing line (§4) is added.** No out-of-kit PR blocks it:
  - The census read 23 other open PRs; 0 touch either path, and 0 carry KS-470, KS-1374 or KS-1054 in the title.
  - Peter's #1351/#1352/#1353 are REPORTED by name and none touches a kit path (repin_dryrun_2.out).
  - `sequenced_out_of_kit` is EMPTY by drafting, and nothing needs it.
- **Launcher `--check` rc 0** (launcher_check_1.out, and again after the controls in launcher_check_2.out):
  - 1 of 1 head at branch AND pull/head;
  - the GitHub compare == the pins;
  - 24 by-name keywords present as tokens;
  - the EXCEPTION-FIRST rule, the holds, the named exceptions, the GO and the addendum rules all present.
- **Repin `--dry-run` rc 0** (repin_dryrun_2.out, 22:46:57Z): `DRY RUN COMPLETE`. The only report is the missing routing line (`line present: 0`).
- **Pins** (pin_1.out rc 0, measured 21:56:28Z):
  - develop `37205947ddd2775a72a417beb5b7ac8e3240fbf3` is #1350's squash, and its tree `6930599560c9` equals gate47's END_TREE.
  - #1354 is clean alone. **END_TREE `bcac9e18943fa6aa97b394a7c8b4424124af6ea9`** (`2 files changed, 10 insertions(+), 3 deletions(-)`), which equals the head's own tree.
  - Modes: both paths are 100644. `.githooks/pre-push` is read at 100755 as the control that the instrument can read another value.
  - `baseline-contract.mjs` blob `2504d9a28dc0` is byte-equal at develop, head and END.
  - pre-push, preflight.sh and lockfile-cleanroom.sh are identical at all three trees.
- **Controls, both ways.** One unedited script (`controls_gate48a.sh`, sha256 `e5cb66571869…`), hashed before run 1 and after run 2 (controls_sha.txt):
  - normal (controls_1.out) **rc 0**: `123 controls, OK 123, MISMATCH 0 | ssh-denied retries 0`;
  - `--invert` (controls_2.out) **rc 1**: `123 controls, OK 0, MISMATCH 123`.
- **Drafter predictions.** The gate re-derives every one of them:
  - lockdiff_1.out `LOCKDIFF PASS`: 274 -> 274, MOVED=1 (js-yaml 5.2.3 -> 5.4.2), ADDED=0, REMOVED=0, OTHER=0. lockfileVersion 3 on both sides. The observability link entry is byte-equal. integrity/resolved == the registry's for 5.4.2 (and the base's for 5.2.3). The GHSA-r3ph range READ from the advisory is `>= 5.0.0, <= 5.4.0`: 5.4.2 is OUT of it, and 5.2.3 is IN it.
  - baseline_1.out `BASELINE PASS`: 25 -> 26 rows, a pure insert (7 0). The new row has fields {package undici, reason, ticket KS-470, decidedAt 2026-09-30, expires 2026-10-09}. GRANDFATHERED (17) == the no-expiry rows (17).
  - keyscan_1.out `KEYSCAN PASS`: 6 checks, 0 FLAG. The only key is KS-470, the subject lands at 89, there is 1 `Refs KS-470` and no closing keyword.
  - capture_1.out `CAPTURE OK`: 11 mails, and the READY is byte-equal to the seat's `mail/READY-gate48a.txt`. Wednesday's 3 clause-4 chat entries are included.
  - drafts_1.out `DRAFTS OK`: 2 tickets.
- **FUSE-COUNT (the drafter's read, baseline_1.out): 5 rows expire 2026-10-09 at END, against 4 at develop.**
  - The five: GHSA-337j and GHSA-wrjc (react-router, KS-528), GHSA-frvp (@hono/node-server, KS-530), GHSA-mwp4 (ip-address, KS-729; one of leg 6's two "no longer reported" rows), and **GHSA-r53p (undici, KS-470, new)**.
  - That is **217.8 h** to 2026-10-09T00:00:00Z, computed at 2026-09-29T22:12:57Z.
- **Final re-read of the heads** (final_lsremote_1.out, 22:46:57Z): develop `37205947ddd2`, #1354 `4370be410bbf` (branch and pull/head), #1351 `eac2dae2afb7`. Every pin is still current.

## 2. What the gate must rule (READ or MEASURED as stated; each one is a by-name item in the prompt)
1. **EXCEPTION-CHECKED (READ, lockcensus_1.out). This is the ruling that decides the verdict.** Three undici entries are vulnerable to GHSA-r53p, and all three are PRODUCTION entries (no `dev` flag):
   - `frontend/issuer/package-lock.json` 5.29.0. That directory has its own Dockerfile, whose builder stage does `COPY frontend/issuer/package*.json ./` and then `npm ci`.
   - the workspace root `Blockchain/Dev/package-lock.json` 5.29.0.
   - `mobile/secuura-app` 6.28.0, a shipped APP that is out of scope (KS 769).

   Read literally, Wednesday's own question ("any lock whose directory builds a shipped tree") answers **YES** for the issuer. The seat's NO rests on the artefact read of the final stage. That read is clause 2, and the grant says the exception exists so that clause 2 does not carry the whole decision alone. The 12 grandfathered undici siblings were accepted on the same reasoning before the grant existed. If the gate says the exception fires: **NO GO, and it stops for Kam.**
2. **GRANT-CLAUSES:**
   - Clause 3 says "the SHARED re-triage date", but the seat itself measured that the file has none (2026-10-09 ×4, 10-15 ×3, 10-31 ×1).
   - The grant says "Baselining ONLY. No pin bumped", yet the js-yaml fix is a pin bump, ruled separately.
   - Clause 4's flag to Kam (07:31:59) called undici "a build tool used only when building the issuer frontend" and "in no backend service". The census reads it as a production entry that is also pinned in the root lock. The flag never gave Kam the number of rows on the fuse date (5).
3. **REASON-TEXT-TRUE (READ, row_reason_gate48a.md, 10 sentences, reason sha256 `e75b662a69b9…`).** The row's reason is a published record:
   - It says undici is "reached ONLY via frontend/issuer", and three sentences later names "the root lock's own undici entry".
   - It says "would close it and all 12 sibling rows" as a fact; that is unmeasured unless the gate reads the 12 advisory ranges.
   - It says "the single shared re-triage date this file already carries", which contradicts the seat's own measurement.
4. **DRAFTED-TICKETS-CHECKED (READ).**
   - The cleanroom ticket's title says the script "cannot regenerate one of the 43 locks it polices". The cleanroom script's corpus is `find services packages frontend scripts -maxdepth 2` under `Blockchain/Dev`: 35 locks at END, **0 under `systemTest/`**. The 43 locks are leg 7's corpus (`audit-locks.mjs`). Its refusal text at `:352` points readers to lockfile-cleanroom.sh.
   - The PR body repeats that claim.
   - The `:120` citation itself is correct.
5. **LOCK-DIFF, item (c) (READ).** For the same reason, **no preflight leg runs `npm ci --dry-run` on `systemTest/performance`'s lock**, so the new lock's installability is unmeasured by the hook. The prompt makes the gate run it.
6. **PR-BODY-CLAIMS.** The PR body's "before this PR" column says `audit:contract` **rc 1**, but the READY's table says rc 0 at the base.
7. **The READY does not carry the two ticket texts.** Wednesday's ruling said "Put the ticket text in your READY". The READY only names the files, so the kit reads them from `ks470/`.
8. **Context, not a finding of #1354.** The seat's handover (21:56Z) discloses that one of Wednesday's ANSWER mails arrived with no pane tap and went unread for about 50 minutes. **A GO sent by tap alone could sit unread.** The seat says its watcher is now armed.
9. Also carried: `mergeable_state` `unstable` (CI retired); the leg-6 feed lag; the regen's reproducibility if the registry has moved.

## 3. Pins and what the gate owes
- The prompt `2026-09-30_secuura-batch1354.prompt.txt` (40479 bytes, sha256 `282ffbe888f5…`) carries the requirements under 24 keywords (fill_gate48a.py `KW`), each checked as a TOKEN.
- The launcher `launch_qa_secuura_batch1354.sh` (12715 bytes, `5e9c19252501…`) refuses on any of these:
  - a missing keyword (33);
  - the ticket line (32);
  - the tier, FROZEN or round lines (7);
  - the **EXCEPTION-FIRST rule (34)**;
  - the HOLDS: gate47's, **plus four named exceptions** (39). The four are: X1 registry reads; X2 the scratch-copy regen containers with network; X3 the ONE `docker compose -p g48aprobe build issuer-frontend`, build only; X4 advisory and registry GETs;
  - the GO (26);
  - the addendum rules: MG-1 2 over 2, CONTRACT == base blob, FUSE rows, drafted tickets, REPORT-HASH-LAST, TRUE-OF-THE-DIFF (25);
  - the verdict subject or report dir (23);
  - develop or END_TREE not given in full (31);
  - any kit file missing or not named (8).
- **Differences from gate47's HOLDS, stated because the brief asked for them verbatim:**
  - "#1350 is driven with STUBS only" became "#1354 deploys nothing and nothing is deployed on it".
  - "its working tree is far BEHIND origin develop" became "its working tree is the seat's, never your evidence".
  - Peter's parenthetical now names his #1351-#1353.
  - Every phrase the launcher checks is unchanged.
- The prompt's 8 requirements cover the brief's nine items by name: LOCK-DIFF-ONE-ENTRY, JSYAML-OUT-OF-RANGE, BASELINE-ROW-FIELDS, CONTRACT-BYTE-EQUAL, FUSE-COUNT, AUDIT-GATES-HEAD-END, CLAUSE2-REMEASURE, EXCEPTION-CHECKED, GRANT-CLAUSES, REASON-TEXT-TRUE, DRAFTED-TICKETS-CHECKED, CLEAN-MERGE, END-TREE, MODES, OUT-OF-KIT-CENSUS, SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS, TIERING, DISK-ENOSPC, REPORT-HASH-LAST.
- Capture `mail_gate48a_ready.md` (69308 bytes, `65afff55acf4…`). Drafted texts `drafted_texts_gate48a.md`:
  - override: 2308 chars, `c8404eafca27…`;
  - cleanroom: 2126 chars, `9441b243a027…`.
- gate47's report sha256 `e0eb8ba1eb26…` equals the hash in Wednesday's gate47 GO. The fill refuses if it does not.

## 4. Routing line — NOT added
Back up the file first. Then add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`, after line 156 (`QA/Secuura-batch1349|coagent@agentmail.to|yes`, currently the last line):
```
QA/Secuura-batch1354|coagent@agentmail.to|yes
```
- Until that line is present, step 0 of the launch action refuses with rc 1. Control R1 measures that refusal on an empty routing file.
- Control R8 shows the same run, with the line present, passing step 0 and stopping at 3b.

## 5. Controls: `controls_gate48a.sh <scratchpad> [--invert]` — 123 controls
- **PN0-PN5, PNZ, pin_gate48a.py:**
  - PN0 is the real subject run as a simulation: END_TREE, END == the head tree, 3 modes OK, contract byte-equal, the hook.
  - PN1 is a wrong head; PN1d shows `--develop` is refused without `--simulate`.
  - PN2 is a contract-edit plant, refused by (K).
  - PN3 is a develop move ON the row next to the insertion: `(C) the develop move touches its own path`.
  - PN4 is audit-baseline.json recorded 100755: MODE MISMATCH.
  - PN5 is a develop move on an unrelated path: clean, with the END == head-tree line reading **False**. This proves the equality line can print False.
  - PNZ: the real pins are sha256-unchanged.
- **LD0-LD5, lockdiff:**
  - LD1 is a second entry moved (MOVED=2);
  - LD2 is a changed integrity (fails L5);
  - LD3 is the observability link entry edited (fails L4);
  - LD4 is lockfileVersion 2 (fails L1);
  - LD5 is js-yaml 5.3.0, which is in range (fails L6).
- **BL0-BL4, BLCT, baseline:**
  - BL1 is expires 2026-10-10 (B4 fails, and the fuse count drops to 4);
  - BL2 is another row touched (B2 fails; numstat 8 1);
  - BL3 is the row with no expires (B5 fails: 17 vs 18);
  - BL4 is ticket KS-471;
  - BLCT is the contract plant (B5 fails).
- **LC0-LC2, LCZ, lockcensus:**
  - at END, 3 entries are vulnerable;
  - at develop, 4 are vulnerable, including js-yaml 5.2.3 in systemTest/performance (the control);
  - the offline fallback is labelled as such;
  - the real census JSON is sha256-unchanged.
- **KS0-KS9, keyscan:**
  - `(#n)`; a foreign key; lands at 93; `KS-4700` is not KS-470; a missing `Refs`; `Closes`; a foreign key in the body; a FLAG on a planted PR body;
  - **KS8: a FALSE subject that still PASSES the scan.** Truth is the gate's to rule.
- **L0-L20 + LK1-LK24, the launcher** (refusal code in brackets):
  - wrong head (6), moved develop (17), wrong compare (10);
  - foreign GO / seat (26 ×2), unfilled token (8);
  - each of the 24 keywords broken (33 ×24);
  - capture without the head (20);
  - nine dropped HOLDs, including the named exceptions (39 ×9);
  - non-TTY launch (21), develop not in full (31);
  - tier and round lines (7 ×2), ticket line (32);
  - five addendum rules (25 ×5), verdict subject (23);
  - MOVED KIT (2);
  - four kit files not named (8 ×4);
  - EXCEPTION-FIRST (34).
- **R0-R8, the launch action:**
  - R0: the live dry run completes; R0c: the census line; R0h: Peter's #1351 reported;
  - R1: no routing line (1);
  - R2: overlap via Blockchain/Dev/package-lock.json (15);
  - R3: title key KS-1386 hits #1351 (15);
  - **R3s: a controls-only stand-in for Wednesday sequencing #1351 at its current head** is reported, not refused; **R3w: the stand-in at a WRONG head refuses rc 15**;
  - R4: DISJOINT dependabot (0);
  - R5: stale head pin (11);
  - R6: moved develop (10);
  - R7: bad scratchpad (9);
  - R8: a routed temp file stops at 3b (0).
- **Not controlled:**
  - on a real launch: the usage gate (5), `cockpit.sh add` (7) and the override refusal (4);
  - a `mergeable=False` refusal;
  - a REAL re-pin across a develop move (only the dry run's rc 10 is controlled).
- **Side effects, kept:**
  - R1 and R8 wrote `launch_<HHMMSS>.*` step outputs into this kit (6 routing files now, across the superseded and formal runs);
  - the PN simulations wrote `pins_gate48a.SIM-*.json`;
  - LC1 wrote `lockcensus_gate48a.37205947ddd2.json`.
- **The drafter's own instrument errors, each caught and kept as `superseded_*`:**
  - the first mode control named preflight.sh, which is recorded 100644;
  - lockdiff L7's predicate was wrong;
  - lockcensus had a COPY substring false-positive (vc-issuer);
  - **lockdiff L6 judged the constant 5.4.2 instead of the head's recorded pin. Control LD5 caught it in the first controls run (122 of 123), and the formal pair ran after the fix.**
- The R-series depends on live GitHub state: #1351 open at `eac2dae2afb7`, and dependabot PRs touching Blockchain/Dev/package-lock.json.

## 6. Could not measure (the drafter)
- No audit leg, install, regen, image build or served-file grep was run. Every one of these figures is the seat's claim:
  - 24/25 -> 24/26, 20/18 -> 19/19, contract rc 0;
  - the regen's bytes, EMISSINGTARGET, and the inert `npm install`;
  - 58 files, 0 node_modules, react 27 / secuura 8;
  - 723 -> 721.
- The vulnerable-lock census and the Dockerfile COPY lines are git READS, not builds.
- Whether the mobile bundle ships undici; whether 7.30.0 falls outside all 12 sibling ranges.

## 7. Files
- **Config:** kit.json (`sequenced_out_of_kit` EMPTY) · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md.
- **Pins:** pin_gate48a.py -> pin_1.out (+ .rc) and pins_gate48a.json (+ .SIM-*.json from the controls) · final_lsremote_1.out.
- **Reads:**
  - gh_read_gate48a.py -> gh_read_1.out, gh_read_1.json, gh_body_1354.md;
  - _mail_list_gate48a.py -> _mail_list_1.out;
  - capture_mail_gate48a.py -> capture_1.out (+ .rc), mail_gate48a_ready.md;
  - drafts_gate48a.py -> drafts_1.out (+ .rc), drafted_texts_gate48a.md.
- **Instruments:**
  - lockdiff_gate48a.py -> lockdiff_1.out;
  - baseline_gate48a.py -> baseline_1.out, row_reason_gate48a.md;
  - lockcensus_gate48a.py -> lockcensus_1.out, lockcensus_gate48a.json;
  - keyscan_gate48a.py -> keyscan_1.out (each with its .rc).
- **Prompt and launcher:** prompt_gate48a.TEMPLATE.txt and launcher_gate48a.TEMPLATE.sh.txt. fill_gate48a.py fills them into the prompt, the launcher and COMMISSION.md (fill_1.out). Then launcher_check_1.out and launcher_check_2.out (+ .rc).
- **Launch:** repin_and_launch_gate48a.sh -> repin_dryrun_1.out and repin_dryrun_2.out (rc 0 each).
- **Controls:** controls_gate48a.sh -> controls_1.out and controls_2.out (+ .rc), controls_sha.txt · superseded_* (the earlier outputs and the L6-bug run).

## 8. The ONE launch command (run it after the routing line in §4 is added)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-30_gate48a/repin_and_launch_gate48a.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-30_gate48a/launch_qa_secuura_batch1354.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ffc4a192-4894-4f1e-abfb-22149b1bd26c/scratchpad
```
- For a dry run, append `--dry-run`. Today it gives rc 0 (repin_dryrun_2.out).
- Argument 2 may be ANY existing Claude session scratchpad. If `g48a_sp/clone` is absent there, pin_gate48a.py rebuilds it on a re-pin.
- If develop moves, the launch re-pins in the same action (step 3b runs pin, lockdiff, baseline, lockcensus, then fill):
  - it refuses rc 10 if the move reaches either path or the merge is unclean;
  - a moved head refuses rc 11;
  - another open PR touching a kit path, or titled KS-470 / KS-1374 / KS-1054, refuses rc 15 unless Wednesday sequenced it at its current head.
