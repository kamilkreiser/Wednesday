# Gateset 2026-09-26_gate26T1 — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane, merged nothing and committed nothing. It wrote only under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate26/` (this kit and its
sibling), the scratch clone `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g26_sp/clone.git` (a `--no-local` bare clone, no alternates), the control workdirs `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g26_controls_*`, the live-shape
fixtures `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g26_liveshape_fixtures/` and a scratch vitest install `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g26_vitest/` (vitest 4.1.11, `npm --legacy-peer-deps`). npm also wrote its usual
debug logs under `~/.npm/_logs/` (two failed installs, npm arborist peer-set crash) — outside the scratchpad, reported, not touched. One stray copy of fill_gate26.py
made by a drafter slip sits in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate26/_quarantine/` (not deleted).

This kit is ONE of TWO. Fourteen PRs (ten relayed; #1284 added 09:5x; #1274, #1268 and #1261 round 2 added 10:2x / 10:3x / 10:5x) split by the weight of their DIFFS: **gate26T1 = the six TIER-1 PRs**; the sibling `gate26T2` (#1245, #1261, #1268, #1275-#1279) has its own README.

| PR | ticket | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | squash subject chars | why this tier (from the DIFF) |
|---|---|---|---|---|---|
| #1274 | KS-934 | `8e94f5fb3e6d8ef21ba2007fde92d3ea0b5c942d` | 2 on `4db87c3e4b98` | 83 | the m365 notify loop on the SSRF guard (row set, wall clock, per-call deadline, WHICH rows a call reaches) + the 200 body. **Round 2 of 2, at the cap.** |
| #1280 | KS-1129 | `12c197a9215e3156d48cf47fbcec09292619cb68` | 1 on `d7cdecf1d2ee` | 71 | what the verify path PERSISTS into the document blob; two heal sites. |
| #1281 | KS-1074 | `c3374e3129ccaca29a9beeafe2d0098ffc86796d` | 1 on `d7cdecf1d2ee` | 78 | five writers that replace the blockchain column wholesale (threadToken erased). |
| #1282 | KS-730 | `34a67a9e48057a0d4939527a4b721a7a5605e4ab` | 1 on `d7cdecf1d2ee` | 72 | KS-730 1/3: admin 500s returned err.message off-production. |
| #1283 | KS-730 | `f92b7c19e98d888b39674eb0b39461ed214a37d3` | 1 on `d7cdecf1d2ee` | 64 | KS-730 2/3: fifteen GDPR 500s; a new logger import. |
| #1284 | KS-730 | `dfc2468a547f0bb3d4995404942736312384539b` | 1 on `d7cdecf1d2ee` | 71 | KS-730 3/3 (Seat B 30th): forty-six admin-config 500s; four unconditional leaks remain (KS-1334). |

Routing `QA/Secuura-batch1280`. GO string `GO: merge #1274, #1280, #1281, #1282, #1283, #1284 batch` (or the subset). All go to a MERGE SEAT (no author is live for them).

## 1. BLUF
- **Kit: READY to launch** once you add the routing line (§4). `--check` rc 0 (all guards pass:).
  - Controls: **132 controls, OK 132, MISMATCH 0** normally (rc 0); **OK 0, MISMATCH 132** under `--invert` (rc 1 — by design every control must flip).
- **Pinned over develop `00de57baeb405d0081fe8b6f192bd40d35acef61`** (tree `fb4d9f1691451db2cdfab3cae22db2fd675f0f80`) — read by ls-remote AND fetched AND agreed; it is the `00de57baeb40` Wednesday expected (#1270's squash).
  - END_TREE **`76e2be58f4e0ffe46ba10246c467421780ba64fc`** (13 files changed, 1517 insertions(+), 79 deletions(-)), identical in all 720 orders (214 distinct merge-tree calls, memoised).
  - END_TREE_WITH_SIBLING **`5807048824a8e15dce62d8a7a6b0d62e2160a4c1`**: develop + both kits, the same tree whichever kit lands first (measured from both kits).
- **OVERLAPS: NONE.** Measured pairwise: every kit PR vs every other, vs the sibling kit, vs the develop move since its own merge-base, and vs Seat B 30th's in-flight PRs at the pin (none left in flight at the final pin: #1274, #1268 and #1261 were, and each joined a kit at its round 2).
  - NOT STACKED: no head is another's ancestor; every pair's merge-base is on develop (hard check in predict).
  - KS-730 PR3's unpushed worktree `s-b29-ks730c` (adminConfig.ts + the ks730c test) was censused disjoint at the first pin, before it became #1284; #1274, #1268 and #1261 were in flight at the first pin and joined T1 / T2 / T2 at their round 2 (Wednesday 10:2x / 10:3x / 10:5x). Nothing of Seat B 30th is in flight at the final pin.
- **The decisive items the gate owes (predictions, not evidence):**
  - **#1274 at the cap:** the gate must re-run gate25T1's LIMIT-TRUNC case with a stub that HONOURS the new ORDER BY and the `last_sent_at` write-back (an insertion-order stub cannot see the rotation). `last_sent_at` verified by READ at 06-m365-tables.sql:63 and startup-migrations.ts:361/526/527, exactly as the seat says; no migrations/ file. R3 pins the KS-1335 starvation as a known limit (declared; not a NO GO).
  - **STALE-BODY-1274 (READ):** #1274's PR body was NOT updated for round 2 — it still says the remainder is "reported as such … call again" (round 1's refuted claim) and names neither `truncated`, R3 nor KS1335. The squash body must come from the round-2 message + the mandated block, never the PR body.
  - **ENV-ROUND2 (READ, arithmetic):** `MAX_ROWS="0"` now makes `truncated` TRUE while notifying nothing; `"abc"` makes `truncated` impossible. F-1274-2 is still unfixed (non-blocking at round 1).
  - **STALE-COMMENT-532 (#1283, READ):** the head commit message says the "no logger import" comment "is corrected in place"; the head file still says "Deliberately no logger import in this file" at line 532 while importing the logger at line 21.
  - **UNCONDITIONAL-LEAK-KS1334 (#1284, READ):** 4 response sites carry err.message with no NODE_ENV guard (lines 1859, 2031, 2152, 2158 at head) — matches the seat's 4 and KS-1334 (Backlog). Declared scope; the gate measures one under production.
  - **TOBLOCKHEIGHT-EDGES (#1280, drafter LIVE on the extracted function):** `'0x10'`→16, `'-1'`→-1, `'4242.5'`→4242.5, `'9007199254740993'`→9007199254740992 (lossy). None is reachable from pg's decimal BIGINT text (READ) — a reach ruling, not a blocker by default.
  - **RAW-HEIGHT-KS1333:** #1281's writers still persist `anchor.blockNumber || 0` uncoerced — already ticketed as KS-1333 (Backlog); declared scope for #1280/#1281.
  - **KS-730 as a set:** each of #1282/#1283/#1284 leaves the other two files' ternaries in place; only all three clear originate's share. KS-730 stays In Progress after all three (api-gateway remainder).
- **Fleet STOP (READ, bounded region, NOT-FOUND control):** #1274 28/0 · 6/0 · 49/0 · 60 of 60; #1280 28/0 · 6/0 · 49/0 · 60 of 60; #1281 28/0 · 6/0 · 49/0 · 60 of 60; #1282 28/0 · 6/0 · 49/0 · 60 of 60; #1283 28/0 · 6/0 · 49/0 · 60 of 60; #1284 28/0 · 6/0 · 49/0 · 60 of 60. After the merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no shell-suite path in either kit).
- **Fleet at the launch develop:** Wednesday relayed (11:0x) Seat B 30th's measurement at `00de57baeb40` = 28/0 · 6/0 · 49/0 · 60 of 60; the drafter could not find its file (UNMEASURED by the drafter) — the prompt tells the gate to find and quote it.
- **Linear: every PR links `contributes`; NONE `closes`** (measured, both kits). The "closes a ticket it only contributes to" class you saw twice today is NOT present in this batch.
- **MG-3 key scan:** key scan: 6 mandated squash text block(s), each carries only its own key: #1274 ['KS-934'], #1280 ['KS-1129'], #1281 ['KS-1074'], #1282 ['KS-730'], #1283 ['KS-730'], #1284 ['KS-730']

## 2. Pins — predict_2.out (rc 0; predict_1.out is the identical earlier pinned run)
- #1274: 2 commit(s) `1a37bde12d55`, `8e94f5fb3e6d` over `4db87c3e4b98b8e366c3dd60d5f399917bad5086`; 16 behind develop; merged tree `ad7a9d1ff1d771ac2359aef238c593be844ac98a`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1280: 1 commit(s) `12c197a9215e` over `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`; 11 behind develop; merged tree `cfc857c5d1c0d5c641ceb7f807b9493ec5bcbe1f`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1281: 1 commit(s) `c3374e3129cc` over `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`; 11 behind develop; merged tree `a0fad12a32b7481fc191ca8af71fc7ab7efcd4b1`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1282: 1 commit(s) `34a67a9e4805` over `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`; 11 behind develop; merged tree `c5518a3af34ba5cb453efa8e3843345bb21b7d27`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1283: 1 commit(s) `f92b7c19e98d` over `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`; 11 behind develop; merged tree `c6f86d8b739bd2ca2216218b40dd38dde00a5ee2`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1284: 1 commit(s) `dfc2468a547f` over `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`; 11 behind develop; merged tree `3f2e1e8732486dc748d36e7f75c5bdd211812ac6`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- Simulations: develop + a FOREIGN edit of a kit PR's own file → REFUSED (predict_sim_foreign*.out, rc 1); develop BEFORE gate25's six squashes `df5e9f5da6d23411e7b38a79a58aa20c04b6afe2` → PASS (predict_sim_predev.out).
- Superseded runs are kept, never deleted: `*_pre1284*`, `*_pre1274*`, `*_superseded_*` (each names why).

## 3. What the gate owes
- Prompt `2026-09-26_secuura-batch1280-t1.prompt.txt` (47793 bytes) — the per-PR sections, the rules, the MANDATED SQUASH TEXT blocks (key-scanned) and the MG-3 key-set table.
- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1280-t1/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.

## 4. Routing line to add (the drafter did NOT write it)
`QA/Secuura-batch1280|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (absent at drafting, measured: the exact line is absent; `QA/Secuura-batch1245r2` exists for round 2). Also in PROPOSED_inbox_routing_line.txt.

## 5. The ONE launch command
```
/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate26/gate26T1/repin_and_launch_gate26T1.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate26/gate26T1/launch_qa_secuura_batch1280-t1.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad
```
- Dry run (`--dry-run` appended): repin_dryrun_1.out → DRY RUN COMPLETE 2026-09-26T01:06:18Z — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add
- If develop moves (the sibling kit or any GO lands first), step 3b re-pins in the same action; a move onto an own path, a stack or a pairwise overlap refuses rc 10 (controls RD / RE).
- If you copy the kit into `gatesets/2026-09-26_gate26T1/`, pass the copied paths: step 0b re-measures and re-fills there.

## 6. Decisions for Wednesday (each with the drafter's recommendation)
1. **#1274 at the cap — the stub.** gate25T1's runtime stub modelled `ORDER BY created_at` as insertion order; round 2's fix is only visible to a stub that sorts on `last_sent_at` and applies the write-back. *Recommend:* keep the prompt's requirement; a gate that re-uses the old stub cannot grade round 2.
2. **STALE-BODY-1274.** *Recommend:* name it in the GO — the merger composes #1274's squash body from the round-2 commit message + the mandated block (Refs KS-934), never the PR body. Optionally ask Seat B 30th to refresh the PR body (a body edit does not move the head).
3. **KS-1335 / KS-1334 / KS-1333 as declared scope.** The prompt forbids a NO GO for a limit a Backlog ticket carries. *Recommend:* keep; the gate still measures each so the tickets get numbers.
4. **Merge order.** The two kits are disjoint and END_TREE_WITH_SIBLING is order-independent (measured). The three KS-730 PRs only clear the class together. *Recommend:* if the gate NO GOs one KS-730 PR, still merge the GO'd others — each is a strict improvement on its own file.
5. **#1284 authored by a LIVE seat (B 30th).** *Recommend:* the merge seat squashes it like the rest; B 30th's other fix rounds (#1261, #1268, #1274) are all in this batch now.
6. **READY mails NOT read.** Wednesday relayed heads "per mail" without message ids; a listing marks mail seen. The capture uses PR bodies, commit messages and the push logs, each with a sha256. *Recommend:* accept, or pass the ids and the capture is redone.
7. **#1285 KS-766 is NOT in gate26** (see gate26T2 §6.7): the next kit.

## 7. Controls: `controls_gate26T1.sh <scratchpad> [--invert]`
- **controls_1.out:** 132 controls, **OK 132, MISMATCH 0** (rc 0).
- **controls_2.out (`--invert`):** **OK 0, MISMATCH 132** (rc 1 by design). Every control can fail.
- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed (same length, never a superset — the H20 lesson); the launcher's head guard is whole-field.
- Doctored arms are pinned to the launcher's own develop, so a develop move mid-run cannot mask them as exit 17. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev `df5e9f5da6d2` in a MOVED copy; RE makes a kit PR also a sibling-kit PR (a pairwise overlap) and must refuse rc 10.
- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal.

## 8. Files
- Kit: kit.json · COMMISSION.md (the LEGITIMATE SHAPES table) · PROPOSED_inbox_routing_line.txt
- Pins: predict_gate26.py → predict_1/2.out, predict_sim_*.out, pins_gate26T1.json (+ .SIM-*.json)
- Reads: gh_read_gate26.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate26.py → linear_reads_1.out, linear_KS-*.md · capture_mail_gate26.py → capture_1.out, mail_gate26T1_ready.md, stopcounts_gate26T1.json
- Prompt/launcher: prompt_gate26T1.TEMPLATE.txt, launcher_gate26T1.TEMPLATE.sh.txt, fill_gate26.py → 2026-09-26_secuura-batch1280-t1.prompt.txt + launch_qa_secuura_batch1280-t1.sh (fill_1.out; `.pre-*` = earlier fills), launcher_check_1.out
- Repin/controls: repin_and_launch_gate26T1.sh (repin_dryrun_1.out), controls_gate26T1.sh (controls_1/2.out + .rc)
- Drafter probe (PREDICTION): drafter_nodeprobe_g26t1.sh → nodeprobe_1.out (toBlockHeight extracted from the head blob)
- Shared drafting helpers one level up: make_commission.py, make_readme.py, derive_repin_controls.py, repin_header.txt

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, merge, commit, push, routing write, container or port bind. No inbox read. The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --no-local` as a source); Seat B 30th's worktree only by rev-parse / merge-base / diff / `--no-optional-locks status`.
- **UNMEASURED:** every suite count and every red proof (READ from seat logs and messages); every runtime behaviour through the real modules (the drafter ran only extracted pure functions under node); tsc, lint, prettier; the usage gate and launch steps 4-6; the post-pin moves of Seat B 30th's in-flight PRs (re-read at every re-pin).
- **UNMEASURED:** the deployed svc_teams_webhooks schema (no DB read — whether a pre-CREATE table lacks last_sent_at/created_at); the 11 GDPR routes no cell drives; where logger.error lands in a deployed environment.
