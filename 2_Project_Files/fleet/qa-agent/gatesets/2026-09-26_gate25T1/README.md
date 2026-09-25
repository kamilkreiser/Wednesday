# Gateset 2026-09-26_gate25T1 — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane and committed nothing. It wrote under
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4f2cdc54-acc3-4f26-989e-2c407e677824/scratchpad/gate25/` (plus the scratch clone
`…/scratchpad/g25_sp/clone.git` and control workdirs `…/scratchpad/g25_controls_*`, all inside the session scratchpad). **One stray file outside it:**
`/tmp/claude-501-wl.sh` (451 bytes, a copy of a shell function, written by a slip in a drafter command) — reported, not deleted.

This kit is ONE of TWO. The eight round-25 PRs split by the weight of their DIFFS: **gate25T1 = the four TIER-1 PRs (all Seat L8, wrapped)**;
the sibling `gate25T2` (#1268, #1270, #1271, #1273; tier 2 + one tier 3) has its own README.

| PR | ticket | head | why TIER 1 (from the diff) |
|---|---|---|---|
| #1267 | KS-1295 | `71f6f4d73cbde5b32f1564c9171eb1b705f77880` | vc-issuer credential store: a WARN naming credentialId on the DB-unavailable path (runtime, logs) |
| #1269 | KS-1182 | `df21c6fd159f2a707d698e418946911f019ca9a0` | demo-service terminal error handler: status bound, headers, message echo (exposure / DoS) |
| #1272 | KS-849 | `34980b8e9ee22a36c658a03d9d763c48caeb9064` | kyc: both mock timers re-read the verification before they write |
| #1274 | KS-934 | `1a37bde12d55563f77e192519ca7db62461dbf6f` | m365 POST /api/teams/notify: LIMIT, aggregate deadline, per-call timeout; published 200 body gains 2 fields |

Routing `QA/Secuura-batch1267`. GO string `GO: merge #1267, #1269, #1272, #1274 batch` (or the subset). All four go to a MERGE SEAT (L8 wrapped).

## 1. BLUF
- **Kit: READY to launch** once you add the routing line (§4). `--check` rc 0; controls 114/114 OK normally and 114/114 MISMATCH under `--invert`.
- **Pinned over develop `df5e9f5da6d23411e7b38a79a58aa20c04b6afe2`** (#1266's squash). **Seat M1's merge finished during the draft.**
  - All five of #1262-#1266 are on it, and its tree **equals your expected END tree `6942101caa7be149c1fc4a254eefc75af3607b86`** (measured).
  - develop was unmoved at every later read, the last at 21:0xZ.
- **ONE OVERLAP WITH M1: #1267 ∩ #1264 on `vc-issuer/src/repositories/credentialRepo.ts`.**
  - The two PRs edit different hunks and the merge is clean. Over the pinned develop, #1267's merged blob `c93152727c39…` ≠ its head blob `94fae2659a6c…`.
  - The kit DECLARES it. The target is the clean 3-way `merge-file(develop, parent, head)`, measured equal to merge-tree's blob.
  - **The merge seat must NOT squash #1267 as a whole-file copy of its head blob.** That would revert #1264's comment fix, because #1267's head still says "auto-created".
  - No other PR in either kit touches any of M1's paths, or any other kit PR's paths (measured).
- **Predictions to verify** (the gate measures each; these are the drafter's reads and probes):
  - #1269 HDR-THROW (LIVE, node): `setHeader` throws on a header name with a space, and on a value with CR/LF, inside the handler. What the client then receives is UNMEASURED.
  - #1274 ENV-NAN (LIVE, arithmetic only): a garbage `DEADLINE` or `PER_ROW` env value means the deadline never trips, and every call gets `setTimeout(NaN)`, which is 1 ms. A garbage `MAX_ROWS` sends `LIMIT NaN` to Postgres. An env value of `"0"` skips every row.
  - #1272 SWALLOWED-SAVE-ERROR (READ): a failed save inside a timer is silent.
  - #1274 SPEC-SHAPE (READ): the published schema is the generic `M365SuccessSchema`.
- **KS-849's known limit is carried and ruled out as a #1272 defect.** Cell S3 pins that status/currentLevel are still overwritten at the 3 s timer. That is ticketed as **KS-1327** (Backlog).
- **Linear: all four link `contributes`.** None closes its ticket (measured).

## 2. Pins — predict_2.out (rc 0, 2026-09-25T20:43Z; predict_1.out is the identical earlier run)
- develop `df5e9f5da6d2…`, tree `6942101caa7b…`, 10 commits ahead of the PRs' parent `4db87c3e4b98` (#1255's squash).
- Each PR is ONE commit on `4db87c3e4b98`. In all four, both instruments agree: API head == ls-remote pull/head == branch == fetched.
- **Merged trees over develop:**
  - #1267 `a654537d7bdf…` (declared-overlap target);
  - #1269 `6c8015fb1dce…`;
  - #1272 `0967a9e849ae…`;
  - #1274 `5a47f10095e0…`.
  - Checks (1)-(3) hold for all four. No mode change.
- **END_TREE `4f420717d0668537f4e37e4819b6e6d0eea717de`** (8 files, +975/-45). It is identical in **all 24 orders**.
- The same END is reached from M1's base `d7cdecf1` + the rest of M1 + this kit (the m1base simulation, `END_TREE_AFTER_M1`).
- **Simulations:**
  - develop + a foreign edit of #1269's or #1267's own file → REFUSED;
  - develop + a foreign edit of credentialRepo.ts (not #1264's blob) → REFUSED ("overlapbad");
  - pre-M1 develop `d7cdecf1` → PASS.
- **Fleet STOP, READ by bounded region** (with a NOT-FOUND control), on all four push logs: 28/0 · 6/0 · 49/0 · 60 of 60, "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
  - Seat L8's measurement on develop `d7cdecf1`: the same four counts.
  - No PR in either kit, and none of M1's five, touches a shell suite, so the count after the merge stays 28/0 · 6/0 · 49/0 · 60 of 60.

## 3. What the gate owes (prompt `2026-09-26_secuura-batch1267-t1.prompt.txt`, ~31 KB)
- **Per PR:**
  - a through-code review;
  - the seat's red proof re-run and restored by bytes (W1/W3 red, W2 green; 11 of 14 red with 3 controls green; S1/S3 red, S2 green; N1-N3 red, CONTROL green);
  - **a runtime probe through the real module**, on 127.0.0.1 port 0 only, with the stubs named and a control that can fail;
  - an evidence class on every recommendation.
- **By name:**
  - DECLARED-OVERLAP-1264 (the target; #1264's comment kept; W1-W3 run on the merged tree);
  - HDR-THROW and HDR-ON-500;
  - ENV-NAN and ENV-ZERO;
  - MOCK-UPSERT-COLUMNS: the mock's column list against the real `DO UPDATE SET` (11 columns, READ);
  - SWALLOWED-SAVE-ERROR;
  - KS-1327-LIMIT, graded as disclosed scope;
  - LOG-CONTENT;
  - UNREACHABLE-TODAY;
  - SCHEMA-SOURCES: `created_at` is in `docker/init` and in the api-gateway startup-migrations, and no `migrations/` file names the table;
  - SPEC-SHAPE and STUBBED-GUARD;
  - BASE-FIGURES-4DB87C3E: every seat count was measured at `4db87c3e` and is re-measured, e.g. vc-issuer 131 → 134 expected on the launch develop.
- **Rules:**
  - no Docker, no stack, never :5432;
  - legs 3/4/8 NOT run (#1274: SPEC-SHAPE READ ONLY);
  - the KS-1155 load rule, with one re-run (KS-1328, kyc db.retry, is named);
  - holds;
  - MERGE ADDENDUM with 4 lines;
  - subject `[QA -> Wednesday] TIER-1 GATE batch #1267 #1269 #1272 #1274 (Seat L8, round 25)`.

## 4. Routing line to add (the drafter did NOT write it)
`QA/Secuura-batch1267|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (absent at drafting, measured).

## 5. The ONE launch command
```
/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4f2cdc54-acc3-4f26-989e-2c407e677824/scratchpad/gate25/gate25T1/repin_and_launch_gate25T1.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4f2cdc54-acc3-4f26-989e-2c407e677824/scratchpad/gate25/gate25T1/launch_qa_secuura_batch1267-t1.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4f2cdc54-acc3-4f26-989e-2c407e677824/scratchpad
```
- If you copy the kit into `gatesets/2026-09-26_gate25T1/` first, pass the copied paths. Step 0b re-measures and re-fills at the new home. The launcher refuses from anywhere else (exit 2).
- **If develop moves again, step 3b re-pins in the same action.**
  - It runs predict, then fill, then re-reads develop.
  - A move that touches #1267's credentialRepo.ts with anything other than #1264's blob, or any other own path, refuses rc 10. That case is re-predicted by hand.
  - Proven by control RD: the real re-pin from a launcher pinned at `d7cdecf1` to the current develop, then `--check` rc 0. Control RE: the same move with the overlap undeclared → rc 10.

## 6. Decisions for Wednesday
1. **#1267's tier.** Its product change is one WARN line. The drafter put it in T1 because it touches the credential store and puts an id in logs. If you rule it T2, it can ride gate25T2 instead (the cap allows 5); the kits would need re-filling.
2. **The merge order with #1264 is already settled** (#1264 is merged). Tell the merge seat that #1267's equality target is the 3-way blob, not the head blob (MG-1).
3. **KS-1327 is carried as the known limit.** A gate NO GO on #1272 for that limit would contradict the commission, and the prompt forbids it.
4. **The READY mails were NOT read.** No message id appears anywhere in the seat records, and a listing marks mail seen. The capture uses PR bodies, commit messages and the L8 handover, each with a sha256. If you hold the ids, the capture can be redone.

## 7. Controls: `controls_gate25T1.sh <scratchpad> [--invert]`
- **controls_2.out:** 114 controls, **OK 114, MISMATCH 0** (rc 0).
- **controls_3.out (`--invert`):** **OK 0, MISMATCH 114** (rc 1 by design). Every control can fail.
- **Every mutation is independent of the original.** doctor() refuses any replacement that contains the text it replaces (rc 98), and refuses when the original still occurs after the plant (rc 97).
  - Wrong heads are the real head with ONE hex digit changed: same length, never a superset. This fixes gate24T2d's H20.
  - The launcher's head guard is whole-field (`awk $1==h`, `grep -w`).
  - The first run's U control was caught by this very check (its replacement contained the original) and was rewritten.
- **controls_1.out** is that first, aborted run: superseded, kept.
- **Not controlled:** exit 16 (needs a TTY), steps 4-6 of the repin (usage gate, cockpit add), a `mergeable=False` refusal.

## 8. Files
- **Kit definition:** kit.json · COMMISSION.md (the LEGITIMATE SHAPES table) · PROPOSED_inbox_routing_line.txt.
- **Pins:**
  - predict_gate25.py, predict_1/2.out;
  - predict_sim_{foreign1267,foreign1269,overlapbad,m1base}.out;
  - pins_gate25T1.json (+ .SIM-*.json).
- **Captured reads:**
  - gh_read_gate25.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md;
  - linear_reads_gate25.py → linear_reads_1.out, linear_KS-*.md;
  - capture_mail_gate25.py → capture_1.out, mail_gate25T1_ready.md, stopcounts_gate25T1.json.
- **Prompt and launcher:**
  - prompt_gate25T1.TEMPLATE.txt, launcher_gate25T1.TEMPLATE.sh.txt;
  - fill_gate25.py (fill_1/2.out) → the prompt and `launch_qa_secuura_batch1267-t1.sh` (.pre-* = an earlier fill);
  - launcher_check_1/2.out.
- **Repin and controls:** repin_and_launch_gate25T1.sh (repin_dryrun_1.out); controls_gate25T1.sh (controls_1..3.out, .rc).
  - `launch_*.routing.out` are control RB's step-0 refusals.
- **Drafter probe:** drafter_nodeprobe_g25t1.sh → nodeprobe_1.out (PREDICTION).

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, commit, push, routing write, container or port bind. The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, and `clone --no-local` reading it as a source).
- **No inbox read at all.** No ids were found.
- **UNMEASURED:**
  - every suite count and every red proof (READ from seat logs and bodies);
  - every runtime behaviour of the four products. The node probe ran node's own `setHeader` and plain arithmetic, never the repo code.
  - the mock-vs-SQL column comparison (READ only: 11 SQL columns parsed);
  - the schema the m365 service actually runs against;
  - tsc, lint and prettier;
  - the usage gate and the machine load at launch;
  - steps 4-6 of the launch path.
