# COMMISSION — DRAFT the round-24 tier-2 QA batch gate kit "gate24T2b" over SEVEN PRs (Seats L6, L5, B 28th), FROZEN at seven. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-26 (~00:5x AEST) as five PRs + a Seat L5 widen, then WIDENED twice mid-draft by Wednesday's messages
("ADD #1254 KS-1155", "ADD #1255 KS-1301 … Cap stays 8"), then told the gate24T2a verdict had landed (#1243, #1244, #1248 GO and merging; #1245 NO GO).
Recorded here as the gate's commission; the QA agent reads it. Shape copied from `gatesets/2026-09-26_gate24T2a/` (and 2026-09-25_gate21T2e): JSON
pins, routing-file override, controls both ways with `--invert`; re-keyed to SEVEN rows plus a STACK base, with BRIEF_TEMPLATE.md and QA_AGENT_CHARTER.md.

## The batch — all TIER 2 per the seats; every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API)
- **#1249** KS-1144 (Seat L6), head `6eb283d058184f1f0fabdc3c3184a817db4fb94b` — STACKED: ONE commit on #1248's head `2b4960172644`, same file
  (`packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`), +81/-14 over #1248. #1248 is gate24T2a's (GO WITH FINDINGS, being merged):
  NOT graded here. #1249 merges only AFTER #1248; its equality target is the MERGED blob (== its head blob `e96215365a6d…`).
- **#1250** KS-1302 + KS-1303 (Seat L5), head `c78f4093fb531bceb94a8e9defb59350d8c60b73` — `scripts/run-shell-suites.sh` + its suite; run_shell_suites 49 -> 55.
- **#1251** KS-1147 (Seat L6), head `8020adae99129f4b7194fef32f1ea5b762819d90` — the ks860 loopback guard's host regex + two cells.
- **#1252** KS-1275 + KS-1299 (Seat B 28th), head `ca7337fa04e04e5438bc79a5abe215424fcb33ef` — two published descriptions + the regenerated yaml + cells;
  ONE commit on develop `77c6426b96d9` (not BASE). Legs 3/4/8 owed or recorded NOT run.
- **#1253** KS-1297 (Seat L5), head `6b88e4f03e82e3da0672efb1bb757ba5da912d6a` — the pre-push fixture guard; fixture_guard 6 -> 10.
- **#1254** KS-1155 (Seat L6, ADDED by Wednesday), head `da0c94968a7423c340b3a3b76244bda536d1f6d2` — packages/shared `vitest.config.ts` + a setup file + cells.
- **#1255** KS-1301 (Seat B 28th, ADDED by Wednesday), head `59245ff0b11c6b760ba5e2a9daedc5927e915e10` — test-only, ONE commit on develop `77c6426b96d9`.
- **FREEZE at seven.** The cap was 8; Seat L5's widen items had NO PR on origin at pin (branches ks-1201 `d1db0d41ac52` and ks-1296 `ff90fbf9d7e3` pushed,
  no PR; ks-906 and ks-1139 not pushed) and their READY mails were never read by the drafter (the capture script reads by message id only) — all four
  go to the NEXT batch: KS-1201 (item 5), KS-1296 (item 2), KS-906 (item 7), KS-1139 (item 6), with the counts L5 declared (5->7, 16->18, 15->16, unchanged).

## The gate MUST (Wednesday's list + the drafter's reads, carried into the prompt)
1. #1249 over develop + #1248 (or over develop once #1248 is squashed — BOTH states legal); HOLD if #1248 is not GO.
2. Base-invariant + PAIRWISE checks per PR over its grading base; the ONE declared overlap is #1248 ∩ #1249.
3. Red proofs per PR in the tester's own clone; restore by bytes.
4. THE READER RULE (the "wrong reading on any real shape = NO GO" rule, generalised to every PR that parses text or output), and #1250's
   TRAP-SWALLOWS-TERM (the INT/TERM arms nobody ran).
5. No Docker / no DB. Legs 3/4/8 NOT run; #1252's LEG-8-PORT owed in their place.
6. Fleet STOP: claimable for all seven BY READ; the NEW counts after merge: pre_push_hook_base 28/0, fixture_guard 10/0, run_shell_suites 55/0, 60 of 60.
7. Foreign keys un-hyphenated in squash bodies (#1250's commit names KS-1127 and KS-1135), subjects <= 92 (#1249 99, #1251 93, #1254 94 fail).
8. GO string `GO: merge #1249, #1250, #1251, #1252, #1253, #1254, #1255 batch` (or the subset) — #1249 after #1248.
9. Routing `QA/Secuura-batch1249` — PROPOSED line `QA/Secuura-batch1249|coagent@agentmail.to|yes`, NOT written by the drafter.

## LEGITIMATE SHAPES (BRIEF_TEMPLATE §2a) — the PRs that change a CHECKER
Predicted-by = drafter. "port" = a Python copy of the reader (a READ instrument, never evidence); "live" = the drafter's own run (drafter_trapprobe_g24b.sh).
The gate MEASURES every row.

### #1253 cell 9 — `grep -cE '(\(|\$\(|\|)[[:space:]]*build_fixture '` over the subject (a checker of source text)
| call-site shape | defeats the abort? | cell 9 flags? (port) |
|---|---|---|
| bare / `\|\| true` / `if …; then` | no (measured by the seat) | no — correct |
| `( bf )` / `x=$(bf)` | YES | yes — correct |
| **`bf \| cat` (the commit NAMES it)** | YES | **no — WRONG** |
| `bf &` / `` x=`bf` `` / `(` on its own line / `{ bf; } \| cat` | YES | **no — WRONG** |
| `false \|\| bf` | no | **yes — WRONG (safe direction)** |

### #1250 the runner under a signal (live, drafter_trapprobe_g24b.sh -> trapprobe_1.out)
| runner | SIGTERM to the runner's pid mid-suite | rc | next suite ran | verdict line | /tmp/rss.* dir |
|---|---|---|---|---|---|
| develop | killed | 143 | no | none | LEFT (KS-1302 reproduced) |
| **#1250** | **handler runs, runner CONTINUES** | **0** | **yes** | **`shell suites: 2 passed, 0 failed`** | removed; the running suite's log gone (`cat: … No such file`) |

### #1252 preflight legs 3/4/8 (port of leg 8's `summarise()` + each operation's `security`)
| field leg 3/4/8 reads | develop | head |
|---|---|---|
| openapi / info.version / path set / operation count | — | IDENTICAL |
| every operation's `security` | — | IDENTICAL |
| the spec with every `description` removed | — | EQUAL (description-only change) |

### #1254 derivedTreeWalkers() (port) — the list == the derived set at head AND over the END_TREE (7 names); nested walkers / non-marker APIs: none today.
### #1251 host regex (port) — escaped pair, `\"127.0.0.1"` (mismatched) and `\'127.0.0.1\'` accepted at head; `\"0.0.0.0\"`, `\"127.0.0.10\"` still violations.
