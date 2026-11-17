STARTABLE: YES - the ruling is verified at source (decision card `nexusai-audit-details-size-cap-1116` ruled choice 'b'; record C-289 at CLARIFICATIONS.md:2971); the build can run on the drafter's defaults for the marker form, limits and wrong-type rule, but those three are NOT in the ruling (C-289 says "none is decided"), so the LANDING waits for the product owner's word on Q-1 to Q-3 (kit HOLD 23). Launch only after NX-T3 (`7bc1c5d2`) is on main (kit REFUSE 4(b)).

# B1682 DRAFTER REPORT - SEAT-N147, NexusAI lane NX-A (RD-994, audit entry field checks)

Drafted Wed 18 Nov 2026, first `date` 02:04:02 AEDT, last `date` 02:18:14 AEDT. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1682_SEAT-N147_nexusai-lane-nx-a-audit-entry-checks.md` (172 lines), sidecar `.measured` (129 lines). `stamp_check.py <kit>`: 129 claims, 129 measured, 0 not measured, rc 0. Four-underscore pattern in the kit: 5 lines (four slots and the last line). Non-ASCII characters in the kit: 0. Card id in the kit: 0. Name scan (scanlib1114.py:20 pattern, underscore-aware): 0, control `_by_<name>_` fires. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s287/d1682/`.

## BLUF
- The authority holds. RD-994 asks for a per-entry-kind field check; the kit puts ONE check inside `auditLog` (so every one of the 42 direct call sites and the entries of the other modules pass through it, and no call site changes), driven by ONE table of twelve kinds, with ONE marker form for every kind. Product change in `backend/server.js` only, one new test file, the counts file. Opus, C3, gate G1.
- Found at source and not in the ticket: `AUDIT_ACTIONS.SETTINGS_CHANGE` is used twice and never defined (both rows are written with action `undefined`); five more kinds carry request text (`entra_config_updated` keys list, `DOMAIN_CONFIG` domains list, `user_added` role, AI endpoint/deployment/host fields, `LOG_ANALYTICS_CONFIG` authMode); the ticket's `AI_ENABLED_CHANGED` "any JSON value" is stale (the route refuses a non-boolean first); a wrong-type email can make the login route 500 before its audit row (reported, not fixed).
- The census: `auditLog(` matches 48 lines (1 definition, 2 comments, 3 forwarding lambdas, 42 direct calls). The sweep's "49" does not reproduce at this blob.

## THE RULING RECORD (printed at source)
1. Decision store, read-only single-card read (`bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh show nexusai-audit-details-size-cap-1116` into `card_show.txt`, filtered on the id: 1 hit):
   `ruling:  choice='b'  ruled_ts=2026-11-16T14:29:36.991428+11:00`; options `[a] Cap each entry at 8 KB and mark cut entries`, `[b] Check each entry type's fields instead` (detail "more work; exact per type"), `[c] Leave it as it is`; `delivered_artefact: NexusAI CLARIFICATIONS section 92 C-289 (records pass B1614); the per-entry-kind field check filed as RD-994; RD-806 commented and kept open`.
2. Project record `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md:2971` (`grep -n -i 'RD-994'` -> 2967, 2971): "**C-289. WHAT DID THE PRODUCT OWNER RULE ON 2026-11-16 ABOUT THE SIZE OF AN AUDIT LOG ENTRY'S DETAILS (RD-806): OPTION (b) "Check each entry type's fields instead"; THE WORK IS A LATER LANE, FILED AS RD-994.**" ... "**Not covered:** how an over-long value is shown (cut and marked, or refused), any size number, alerts 235 and 236 of RD-806, and whether a cap is added later; none is decided."
3. RD-994 itself (0 comments) restates choice b in its description. No other record narrows it.

## FACTS RE-MEASURED (instrument -> result)
- Origin main: `gh api -X GET .../branches/main` -> `f8a6232aaee87ffee903d6bdbfd0f55fdde4d1f0` (#217, records); open PRs 0. `compare/751285aa...f8a6232a` -> ahead 2, `HISTORY.md` only. `compare/f8a6232a...7bc1c5d2` -> diverged 5/2, the four NX-T3 test files + counts. `git/matching-refs/heads/b168` -> `b1680/nexusai-lane-nx-t3-test-tail 7bc1c5d2`.
- Counts: `0ee27c40ed9a` at f8a6232a (contents API = `git rev-parse 751285aa:...`) -> 5868/377; at 7bc1c5d2 -> 5870/377.
- `backend/server.js` blob `bf648e298429` at f8a6232a (contents API), 751285aa and 7bc1c5d2 (`git rev-parse` in the read-only `.tools/b1680/clone`); extracted to scratch, `git hash-object` equal; 22645 lines.
- Census (`census_sites.txt`, a python program printing each call's whole argument text): 48 `auditLog(` lines = 1 def (:305) + 2 comments (:514, :1619) + 3 forwarding (:22211, :22223, :22251) + 42 direct. `auditLog` 52 lines (+ :474, :1755, :4706 hand-offs, :535 comment). Other modules' kinds by `git grep` at 751285aa: scimProvisioning.js 5, entraProvisioning.js 5, sustainability.js 1, retentionPolicy.js:168, services/aiEnabled.js:299.
- `SETTINGS_CHANGE`: `grep -n -F` -> :17201, :17445 only; `sed -n 431,458p | grep -c -F` -> 0 (control ROLE_CHANGED -> 1); whole tree at 751285aa -> those two lines only.
- `details: details,` -> 1 (:309); `AUDIT-FIELDS`, `fieldCheck`, `shapeAuditDetails` -> 0 each in server.js (control AUDIT_BUFFER_MAX -> 6); at 7bc1c5d2 `git grep` over backend/__tests__/static rc 1 (control denialDetails -> 2).
- New test path absent: `ls-tree ... | grep -c -i rd994` -> 0 at 751285aa and 7bc1c5d2 (control rd932 -> 3).
- Code scanning: 22 open on main, 13 on server.js, #237 `js/http-to-file-access` server.js:390 (RD-806); `state=fixed` first page 100 rows (control).
- Model: model-routing.md:93 C3, :108 G1; models_latest.json:17 `claude-opus-5-5`.
- Slot 3 (band 21920-22559): `names1682.py` controls old51 16, old8 16, old22 17, old13 12, b1680 old34 2, b1670 old10 1; 24 SEAT kits of 17-18 Nov name slots 0,1,2,5,13,15,16,17; no gate commission names slot 3 (rc 1); `lsof` band 0 rows at 02:08 (machine-wide 20). Trees old7, probe32, new65, mut22, v30, chk18, chk22 all slot 3, all absent.
- Jest lock: `nexusai-jest.lock` PRESENT at 02:10 (a gate running), `queue-jest` 0 entries; load 4.45 5.35 5.42 (02:08), 5.19 5.51 5.44 (02:18).
- Tools in `.tools/b1680/`: all 18 named present (`[ -e ]`).
- Landing rule: CLARIFICATIONS.md:2067 (`awk NR==2067`): "Merge path: open a PR from the gated branch, wait for CodeQL (a background wait that EXITS), then land the SAME commit. Never squash, never rebase".
- Prior work: RD-994 named only in records/sweep STATUS files (B1614, B1618, B1633, B1638, B1651) and the B1667 kit's left-for-others; no branch names RD-994 (478 heads; 7 old audit-named heads, none of this ticket); `b1682*` 0.

## D-DECISIONS (the drafter's; Tuesday may overrule)
- D-1 One central check inside `auditLog`, no call-site edits (covers all 42 sites and the hand-off modules; guarantees "the same for every kind").
- D-2 Kinds not in the table and non-object details pass unchanged (same reference); a field not named in its kind's map is kept (C2 cell proves no request field is unnamed).
- D-3 In-limit entries are returned as the same object (the acceptance "export and existing audit tests unchanged").
- D-4 Test seam: marker comments + `vm` extraction (precedent rd477:177-178), so every kind gets U cells even where HTTP cannot reach the bad value; HTTP H cells are candidates kept by a measured red-first rule.
- D-5 T is generated and committed INSIDE the chain (step 2b) from the measured kept-list, keeping ONE lock acquisition (the B1680 D-in-chain form).

## Q-QUESTIONS (each with a default; whether the build can proceed on it)
- **Q-1 (needs KAM: what a user sees)** How is an over-long value shown? Default: cut to the limit and marked; the entry gains one `fieldCheck` key naming the field and `{ cutFrom: <original length> }`; the request is never refused and the entry never dropped. Alternative: refuse (drop the field or the entry). Build proceeds on the default; landing waits.
- **Q-2 (needs KAM: size numbers)** The limits: email 254, name 256, role 32, error 1024, description 1024, workspaceId 64, id 128, host/requestedHost/primaryDomain 253, authMode 64, endpoint/apiEndpoint 2048, deployment 256, lists 50 items (keys x64, domains x253). Build proceeds; a different answer is a table edit + rerun.
- **Q-3 (needs KAM: what is stored)** A wrong-type value becomes `null` with `{ wrongType: '<type>' }`. Alternative: keep a cut JSON text of it. Build proceeds; landing waits.
- Q-4 (Tuesday) Scope: the twelve server.js kinds only; SCIM `userName`, Entra provisioning, sustainability, retention, `AI_REQUEST_REFUSED`, request `path` and top-level `userAgent` left (reported). Default: as drafted.
- Q-5 (Tuesday; Kam if Tuesday wants) Define `SETTINGS_CHANGE` in this lane (the export's action column for the two data-source rows changes from empty to `SETTINGS_CHANGE`). Default: yes (the check needs the kind; it is a defect fix).
- Q-6 (Tuesday) Keep everything in server.js with `vm` extraction for the U cells (commission: product changes in server.js only), versus a new `backend/services/auditFields.js` module unit-tested directly. Default: server.js.
- Q-7 (Tuesday) Gate G1 (Opus) for the whole branch. Default: G1.

## CHAIN INPUTS (each produced earlier or present at BASE)
| step | inputs | produced by |
|---|---|---|
| 0 browser | old7 tree | Step 1 (worktree at BASE) |
| 1 readers-base | old7, 18 reader files | BASE |
| 2 red-first | probe32 at BASE, probe variant | `mkT.py --probe` written and proved before the lock |
| 2b tstep | probe-obs.json, `kept.py`, `mkT.py --kept` | step 2; pre-lock |
| 3 a-alone | new65 at A | commit A (before the lock) |
| 4 new-cells | new65 at T | step 2b |
| 5 scanners | Step 1b(iii) list, new65 | Step 1b; step 4 |
| 6 mut | mut22 at T, plant specs | step 2b; pre-lock |
| 8-9 verifies | chk18, v30 at T | step 2b |
| 10 kstep | v30's counts file | step 9 |
| 11 p-plain-K | chk22 at K | step 10 |

## UNMEASURED (said so in the kit)
Which H candidates reach their audit row (H2 list-valued query under express 5, H8 entra-config, the login wrong-type 500); the real cell counts and pair (no jest run: the commission forbade it and the lock was held); the predicted lock hold; the census source class of each call (the seat's own reading at Step 1b); the heads census over server.js beyond names (compare API cap); the Deploy demo skip on a landing.

## OUTSIDE-THE-FENCES DISCLOSURE
- Read-only reads of ANOTHER seat's clone (`/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1680/clone`): `git --no-optional-locks` cat-file, show, rev-parse, grep, log, ls-tree only (the records working copy lacks the objects; fetch is forbidden). Nothing written there.
- `decision_queue.sh show <exact id>` once (allowed form; never `list`). Jira GET only via my scratch helper `jget.py` (reads the project `.env` in-process; no token printed); `gh api -X GET` only under the project's GH_CONFIG_DIR. No jest, no server, no push, no write in the NexusAI folder.
- `DRAFTER_RULES.md` names `/Volumes/Laptop-DEV/...` paths; this machine's tree is `/Volumes/Datasec_DEV/...`; the kit uses the latter throughout.
- One Bash call was refused by the no-rm hook (I tried to remove my own first `.measured` before re-init); nothing was deleted; the sidecar was rewritten in place.
- Scratch files written: `jget.py`, `rd994.txt`, `rd_ctx.txt`, `card_show.txt`, `server.js` (extracted), `census_sites.txt`, `names1682.py`, `alerts_open.txt`, `heads_all.txt`, `readers_serverjs.txt`, `claims.txt`.
