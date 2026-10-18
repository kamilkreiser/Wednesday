# KS screen for the Spark, 2026-10-18 evening: 8 rounds run (the cap), 7 PASS, 1 ticket spent its counter

Written 2026-10-18 20:3x AEDT (shell `date` for every timestamp in the briefs) by a screening and brief-writing sub-agent for Wednesday. Commission: Kam 2026-10-18 ~19:0x, *"new account so please work on the tickets, backlog and definition of which agent to use for what. Spark connected so give it as many tickets as it can handle"*. Mid-task, Wednesday added KS-1619 (three parts) at ~19:5x. Secuura only. Method: `0_Brain/reference/2026-10-10_spark-screen/SCREEN_0040.md` / `SCREEN_0600.md`; rules: the four Spark lessons named in the commission.

**What I wrote to:** `local-model/night/briefs/<7 new dirs>/`, `spark/queue.md` (one comment line and one queue line per round, plus a closing WHY line; queue.sh dropped each queue line itself), `spark/done.md` (rows written by queue.sh), `local-model/runs/` and `spark/state/dry/` (round.sh's own), `local-model/IMPROVEMENTS.md` (5 rows appended), this file. **Read-only everywhere else:** Linear GraphQL queries only, GitHub REST GET only (keys sourced transiently from the Blockchain `.env`, never printed or written); the Secuura checkout got `ls-remote` / `config --get` / `remote get-url` only; all other git verbs ran in a `clone --shared` of the Spark cache under the session scratchpad, with develop fetched by SHA. No push, no PR, no Linear write, no Docker, no box other than the Spark endpoint through the tunnel, nothing deleted, no running script edited. Every round was run by `spark/queue.sh --max 1` (which calls `round.sh`, writes the `done.md` row and drops the line), one at a time, after `tunnel.sh check` (UP every time) and after waiting out the round lock (another seat was running test_only arm dry-runs and controls on the same lock from 19:35 to about 20:03).

## BLUF

1. **8 rounds, 7 PASS, 1 FAIL (twice: the original and its one rebrief).** Every PASS is left where round.sh put it, NOT held and NOT raised.

   | # | ticket · part | tier · rung | verdict | golden | model s · tokens | run dir (`local-model/runs/`) |
   |---|---|---|---|---|---|---|
   | 1 | KS-1509 p1: failed-anchor writer `anchorStateSync.ts:192` `?? 0` -> `?? null` | code_patch · 2 | **PASS 7/7** | TREE-IDENTICAL | 39.0 · 19784+1054 | `spark_secuura_2026-10-18_ks_1509_p1` (tip d0c5d2e0ef8b) |
   | 2 | KS-1490 p1: whatsapp-bot `verify.ts:4` strips trailing slashes (KS-812 gate note) | bash_patch2 · 2 | **PASS 10/10** | TREE-IDENTICAL | 19.4 · 8737+584 | `spark_secuura_2026-10-18_ks_1490_p1` (tip 36c77dc92b22) |
   | 3 | KS-1613 items 1+2: preflight `step()` abort quotes the header's text after the slash; 4 controls kill gate mutants N7/N5/N4 (measured) | bash_patch · 2 | **PASS 7/7** | TREE-IDENTICAL | 38.8 · 22707+905 | `spark_secuura_2026-10-18_ks_1613_p1` |
   | 4 | KS-1619 p3: `verification.ts:1579` document-types log uses fail500's describer | code_patch · 2 | **PASS 7/7** | TREE-IDENTICAL | 49.6 · 32798+980 | `spark_secuura_2026-10-18_ks_1619_p3` |
   | 5 | KS-1619 p2: 3-tenant migrate-tenant-data cell, kills M4e (tamper `adminConfig.ts:2237` + `break;`) | **test_only** · 1 | **PASS 7/7** | TREE-IDENTICAL | 61.7 · 48827+890 | `spark_secuura_2026-10-18_ks_1619_p2` |
   | 6 | KS-1619 p1: multi-chunk approve-forward reply cell, kills M1c (tamper `verification.ts:1068` -> `proxyRes.pause()`) | **test_only** · 1 | **PASS 7/7** | TREE-IDENTICAL | 41.9 · 36236+538 | `spark_secuura_2026-10-18_ks_1619_p1` |
   | 7 | KS-1545 step 1: platform audit-log logs one warn (cause + windowsRead) when it drops the platform half | code_patch · **4 loose** (3 sites) | **FAIL** (checker 7/7, A2a FAIL) | DIFFERS | 71.6 · 25997+2654 | `spark_secuura_2026-10-18_ks_1545_p1` |
   | 8 | KS-1545 step 1, the ONE rebrief | code_patch · 4 loose | **FAIL** (checker 7/7, A2a FAIL) | DIFFERS | 70.3 · 26516+2532 | `spark_secuura_2026-10-18_ks_1545_p1-r2` |

   Rounds 5 and 6 are the **first real (model) test_only rounds** since Wednesday wired the tier at 20:03 (the IMPROVEMENTS row of that wiring lists "a real (model) test_only round" as NOT exercised).

2. **KS-1545 is reallocated by the counter (original + one rebrief, then Opus 5.5).** Classification: **MODEL**, diff arithmetic, not code. Both rounds wrote correct code (red-first, green, whole api-gateway suite, tsc all PASS) but numbered their own hunk headers wrong: r1 `-421` for line 422 and a hunk of 13 old lines counted as 6; r2, after a ROUND 2 section naming that miss and listing every tip line number, hunks 1 and 3 off by -1. Ladder reading: rung 4 held for one site (KS-1410, 10-09), it fails at three nearby sites on header arithmetic. Both patches are correct code a Claude seat can re-anchor. IMPROVEMENTS row 2026-10-18 20:34.
3. **Audit surface:** KS-1545 is the platform audit-log route; Wednesday reads that at source (the 10-05 rule). KS-1619 p1 / p3 touch `verification.ts` (the approve forward and the document-types log), neither an auth line.
4. **Briefs written but not run: none.** Two more tickets are briefable and were NOT briefed because the 8-round cap was reached: **KS-1482** (pre-push `--no-renames` at `.githooks/pre-push:129/:143/:252` at d2ec786e, plus a rename-out cell in the ks998 hook suite; bash_patch, 3 edit points) and **KS-1497 items 2+4** (`scripts/prisma-generate.cjs:67-68`: refuse a symlinked or non-directory `.generate`; the product is outside `services/*`, so code_patch's builder refuses it; bash_patch2 with a new node-driving bash suite).
5. **develop moved twice under me** (d0c5d2e0 -> 36c77dc9 (#1560) -> d2ec786e (#1561), between rounds 1 and 2). round.sh's stale-brief check passed each time (the briefs' files were untouched); briefs 3-8 were written at d2ec786e6130.

## FRAME: tickets read, states, filters, counts, controls

- **Enumerated:** Linear GraphQL, team KS, state type in backlog/unstarted/started, `first:50`, paginated to `hasNextPage=false`: **13 pages, 601 tickets** (Backlog 340, In Progress 203, In Review 28, Todo 27, Blocked 3), read 19:2x. Control: Backlog+Todo **367** equals the 10-14 screen's whole-board count (367 = 339 + 28, which matched `board_count`), so the reader sees the board. KS-1619 was filed 08:48Z (19:48 AEDT), after my read; Wednesday's message supplied it and I read it alone with the same reader.
- **Waterfall (Backlog + Todo only, as commissioned):**

  | step | removed | left |
  |---|---|---|
  | open KS Backlog + Todo | | 367 |
  | named live lanes (KS-1114 1385 1612 1543 1462 1541 1614 724): 4 were in Backlog/Todo (724, 1541, 1612, 1614) | 4 | 363 |
  | assigned to Peter or Stuart | 19 | 344 |
  | title keyword for an auth/token/credential/security/session/policy/permission/login surface or a decision card | 115 | 229 |
  | prior art by ticket number (a `night/briefs/` dir, `night/READY_*` (200 ticket numbers), `night/_quarantine_*`, `spark/briefs_*`, `spark/done.md`, `night/done.md`) | 8 | **221** |

- **Titles screened: all 221.** **Descriptions read** (2-6K characters, comments' last two): KS-1526, 1576, 1505, 1539, 1530, 1465, 1613, 1610, 1509, 1524, 1563, 1583, 1551, 1548, 1546, 1497, 1482, 1483, 1389, 1585, 1587, 1579, 1513, 1527, 1523, 1507, 1494, 1491, 1490 (whole), 1545 (whole), 1559, 1590, 1338, 1251, 1184, 1560, 1537, 1466, 1516, plus KS-1619 (whole). **Read at source at the tip:** api-gateway `utils/logger.ts`, originate `utils/logger.ts` + the ks1348 test, `anchorStateSync.ts` + ks1333 + the seven `markDocumentAnchorFailed` sibling tests (grepped for `blockHeight`), whatsapp-bot `verify.ts`/`index.ts` + the ks812 suite, `prisma-generate.cjs` + the ks1305 test, `typecheck-tests/check.cjs` (part), `preflight.sh:185,216-235` + the ks1547 suite, `.githooks/pre-push` (diff lines), `platform.ts` (document-lookup and audit-log handlers) + ks1510 + ks1512, `batch.ts` fail500, `verification.ts:1035-1100,1540-1585` + ks1087 + the ks1543 document-types test, `adminConfig.ts:2150-2245` + ks730c, and the gate C verdict.
- **Open-PR census** (GitHub REST GET 19:24): **25 open PRs, 127 file entries.** Positive control: `services/api-gateway/src/routes/verification.ts` on #1560 (then open; it merged at ~19:4x and develop moved). Hits on my candidates: none for anchorStateSync, whatsapp-bot src, preflight.sh, platform.ts, adminConfig.ts after #1561 merged. **Staged-lane check:** `fleet/briefs_staged/2026-10-18_seatJ12…` (its scope: originate `routes/verification.ts`, `originate.openapi.ts`, the yaml, `services/anchoring/`, originate `saveDocument`) and `…seatR47…` (mcp `info.ts`, `credentialLiveness.ts`, raising KS-1541/1614/724): neither names a file I briefed.
- **READY check before each brief:** `night/READY_KS-<n>*` for 1509, 1490, 1613, 1545, 1482, 1497, 1619: 0 each.

## FOUND / TESTED / HOW

Every brief: written by a generator from a golden cut in the scratch clone (fences copied from the golden, asserted byte-equal; never retyped), `brief_lint.py` rc 0, then `round.sh --dry-run` rc 0 and `round.sh --control` CONTROL-PASS with the golden BYTE-IDENTICAL, then ONE queue line, then the round. Where I could run the test without node_modules (the bash suites), I ran it in scratch against the tip product (red) and the edited one (green) first.

| brief dir (`night/briefs/`) | what it carries | controls before the real round | sha256/16 brief · golden · pins |
|---|---|---|---|
| `ks_1509_p1` | 1 product hunk (the line + its now-false comment) + import hunk + appended 4 cells (2 RED, 2 CONTROL) in ks1333 | control 7/7 (A4 2 failed / 14 run) | `1f9033025f9be1e3` · `fd794640e1e6f0e8` · `02a55ad477910aa9` |
| `ks_1490_p1` | 1 product hunk + 2 RED cells in the ks812 suite; scratch: tip 5/2 rc 1, edited 7/0 rc 0 | control r1 (bash_patch) FAIL B5a (bash -n on a .ts product: brief defect), r2 (bash_patch2) PASS | `b7a258cab2a3f26f` · `871ee48b06749743` · `c1d7838b4ac65d33` |
| `ks_1613_p1` | 2 product lines + 2 RED and 4 CONTROL cells in the ks1547 suite; scratch: tip 10/2, edited 12/0; mutants N7 (4 red), N5 (1), N4 (1) all killed | control PASS | `e94278572b22e9c3` · `4b0211ba9e8b8934` · `4a44359948e63e6a` |
| `ks_1619_p3` | 1 product hunk + 3 RED and 1 CONTROL cells appended to the #1560 test | control 7/7 (A4 3 failed / 9 run) | `5d76b11f1de4b400` · `6332e786f6847dd4` · `fd742f2a78d24c28` |
| `ks_1619_p2` | test_only: tamper `:2237` + `break;`, one 3-tenant cell in ks730c | r1, r2 REFUSED by the builder (EOF append; blank context), r3 PASS (A4 1 failed / 31 under the tamper) | `1148d7b5127a9197` · `7d9c011ace6ab189` · `006f5cd943525e61` |
| `ks_1619_p1` | test_only: tamper `:1068` (M1c), one multi-chunk cell in ks1087 | r1 FAIL A3c (a `—` escape line), r2 PASS (A4 1 failed / 12) | `b944c8d75ac2a6be` · `877dcc9d4a977e1c` · `3b6e35dfe89d7c0a` |
| `ks_1545_p1` | rung 4: shape for 3 sites, no product fence; NEW 130-line test (3 RED, 1 CONTROL); ROUND 2 section added for the rebrief (r1 brief kept as `KS-1545.md.pre-r2`) | r1 FAIL A6 (checker decl_splice; harness) + a real tuple-type error, r2/r3/r4 PASS | `f6d91e2668c65d36` · `225bc3d1cecc790c` · `d356e39794249d84` |

**IMPROVEMENTS rows appended (2026-10-18):** 19:37 bash_patch B5a parses a non-.sh product (OWED guard); 20:06 test_only edit-block shape (OWED README line); 20:14 A3c drops a `\uXXXX` literal line (cause NOT measured, OWED); 20:22 decl_splice treats an object key `rows:` as an identifier and splices the ref's helper (OWED); 20:34 KS-1545 rung-4 A2a model fail x2 (counter spent; a re-anchor option for loose rungs proposed, not built).

## Rejects (why the rest did not become briefs)

- **Fix shape is a decision / facts only:** KS-1576 ("facts only; no fix"), 1530 ("a decision first"), 1590 (facts only), 1509's other six sites (documents.ts is a live lane's file; the two verification heal paths are a verification surface), 1389 (asks for a view), 1559 ("decide per item"), 1184 (design call), 1516 (policy decision first), 1546/1523 parts (decide whether), 1548 m3 (ruling interpretation), 1545 step 2 (contract change, needs Kam).
- **Security / secrets surface on reading:** **KS-1526** (gateway file logs): the ticket prescribes `combine(json())`, which is exactly the KS-1348 round-2 shape gate33 held for writing secrets and PII to the files; Kam ruled an allow-list for originate (card `secuura-ks1348-r2-files-still-leak-allowlist`), so porting a format to the gateway is a decision, not a brief. KS-1539 (connector allow-list catch; also collided with #1560 when read), 1585 (security service + RLS script), 1579 (connector API-key fallback principal), 1515/1516 (timestamp trust), 1466 (authorization-shaped), 1484/1494 (auth userRepo), 1587 (referral wallet read gate).
- **Reachability (the 09-18 rule):** **KS-1524 (a)** platform.ts:1060: at the tip the red is a HUNG request plus an unhandled rejection under express 4, not an assertion; A4 would read it as a non-assertion red. Not briefed.
- **Test-only, now briefable since 20:03 but not reached:** KS-1563, 1566, 1568, 1578, 1588, 1589, 1593, 1491, 1500, 1468, 1560 M1, 1527, 1513 (several are bash suites, whose test_only builder, `tasks/test_only/`, is still unwired per Wednesday's 20:03 row).
- **Other:** KS-1505 (index.ts not importable for a cell; part 1 is comment-only), 1465 (the fix is in the test itself plus a header comment; no product red), 1551 (a), 1497 (bash_patch2 route, owed), 1482 (owed), 1610 (Peter's instruction: "update the app only, log issues"), 1338 (open capped PR, owner's disposition), plus the long tail of roll-ups, CI, lockfiles, launchers and docs as in SCREEN_0600.

## NOT tested

- No raise, no hold, no REVIEW.md: every PASS awaits Wednesday's source read (and the review agent's first read per the 10-05 rule). TREE-IDENTICAL means the model's patch builds the same tree as my golden; I did not read the seven patches line by line myself.
- No real Postgres, Redis, tenant-provisioning, originate or WhatsApp: every cell runs on stubs, as the checker requires. The KS-1509 claim that every reader handles a null height is the KS-1333 measurement, not re-measured.
- vitest and jest were never run by hand (no node_modules in the scratch clone): those red-first/green figures are the controls'. The bash suites (KS-1490, KS-1613 and its mutants) were run by hand in scratch.
- The suspected escape-decoding step behind the KS-1619 p1 A3c failure was not located.
- KS-1482 and KS-1497 were screened at source, not briefed or proven.
- Live seats' unpushed work was not checked; only open PRs and the two staged lane briefs.
- 182 of the 221 survivors were screened by title only.

## Measured WHY the pool is still thin (and what widened it today)

Of 367 Backlog+Todo, 221 survive the mechanical filters, ~40 were worth a description read, and ~10 survived a source read. What widened the pool today, against the 10-16 "no other one-file candidate" finding: (a) **gate follow-up tickets filed since 10-12** carry exact sites and mutants (KS-1613, KS-1619), (b) **carving**: one site of a seven-site ticket (KS-1509) and a one-line note inside a hundred-file ticket (KS-1490), (c) **test_only wired at 20:03**, which turned two "test gap" items into rounds, and (d) one harder rung (KS-1545, which found the Spark's current limit). What still blocks the rest: decisions written into the tickets, security surfaces, cells whose red is a hang rather than an assertion, and the bash test_only builder still being unwired. The cheapest next widening is the bash test_only tier (KS-1563, KS-1527, KS-1513, KS-1560 are bash-suite test gaps with named mutants).

## Scratch (session scratchpad, not durable)

`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/59f676bc-e3a9-4b9a-8b25-64e572c78937/scratchpad/`: `q/` (ks.json: the 601 tickets; rows.tsv: the 221; prs.tsv / prfiles.tsv), `clone/` (the scratch clone), `logs/` (dry/control/queue output per round), `tpl_*.md` (brief templates), and the scripts `fetch.sh`, `one.sh`, `filt.py`, `show.py`, `prs.sh`, `mkclone.sh`, `prep.sh`, `mkdiff.sh`, `mkbrief.py`, `craftblank.py`, `craft1619p2.py`, `prove.sh`, `waitlock.sh`, `qadd.py`, `runq.sh`, `chk1490.sh`, `chk1613.sh`, `mut1613.sh`.
