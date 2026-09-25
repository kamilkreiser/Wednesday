# COMMISSION — DRAFT the round-24 tier-2 QA batch gate kit "gate24T2c" over SEVEN PRs (Seats L6, L5, B 28th), FROZEN at seven. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-26 (~02:2x AEST) while gate24T2b was RUNNING (launched 16:18:43Z over fa25c9b1). Recorded here as the
gate's commission; the QA agent reads it. Shape copied from `gatesets/2026-09-26_gate24T2b/` (JSON pins, routing-file override, controls both ways with
`--invert`, moved-kit re-fill) and `gatesets/2026-09-26_gate24T2a/` (the #1245 LIVE-SHAPE machinery), re-keyed to SEVEN rows with no stack base.

## The batch — all TIER 2; every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API)
- **#1245** KS-1313 ROUND 2 OF 2 — THE CAP ROUND (Seat L6), head `65eb964271b0d6895e90fe8f5ffcbbbb9a484050` — TWO commits on BASE (round 1
  `1700b5ae7dd5`, NO GO in gate24T2a on B-1245-1 LAST-MATCH-STDERR; round 2 on it). 2 files: `unitSuiteSlotIndependence.test.ts` + NEW
  `tests/unit/support/capturedChildOutput.ts`. A NO GO at the cap ships nothing; the residue is ticketed by Wednesday.
- **#1256** KS-1159 (Seat B 28th), `5a41ed7fea96ab77ed1dc263ae0c7d25c9846440` — test-only; the ks1061 guard's three blind spots. ONE commit on develop `77c6426b9`.
- **#1257** KS-1201 (Seat L5), `d1db0d41ac52359c231cd22abf11124204645d97` — systemTest-only; the hook's early return (0 of 15 legs); hand-run 18/0.
- **#1258** KS-1296 (Seat L5), `ff90fbf9d7e351104404e3eaad505a673e656c1e` — run_migrations_failure_exit_code 5 -> 7; exit 4 documented.
- **#1259** KS-906 (Seat L5), `8a2a28f50eb3453db7284da0f098f6a819d40145` — no_tracked_credentials_root 15 -> 16 (CASE 6b).
- **#1260** KS-1139 (Seat L5), `62e69d23b2507780316f1930123c7d57ebba3ae2` — 8 counter sites in sync-secrets.sh; NEVER executed, NEVER `az`.
- **#1261** KS-1293 (Seat B 28th), `eab8d7031b1b19071a66715ca0aabd9c5cb29c6d` — test-only; CONFIGPINNED + NODNS. ONE commit on develop `fa25c9b1`.
- **FREEZE at seven.** Wednesday's commission reads "frozen at these EIGHT" and lists seven; the kit is frozen at the seven listed (README §6).

## The gate MUST (Wednesday's list + the drafter's reads, carried into the prompt)
1. #1245: the FULL LIVE-SHAPE — S1-S18 real captures, streams SEPARATE, through the REAL function; L3 E0-E5 through childSuiteCounts (+ E6, the
   drafter's H1 inside the real child); the round-1 MUST-CHANGE list (stdout-only or JSON; S17/S18/E5 cells through the same pure function; a
   BEHAVIOURAL call-site pin — T-CALL (iii) must now RED; the {3,2} row); HUNT new real shapes. THE RULE: a wrong reading on ANY real shape = NO GO.
2. Base-invariant + PAIRWISE checks per PR over develop; NO declared overlap; disjoint from the running gate24T2b batch (its squashes re-derive, never STOP).
3. Red proofs per PR in the tester's own clone; restore by bytes; an inert tamper is a FAIL of the arm.
4. THE READER RULE for #1256 and #1261 (and #1257 / #1259's readers).
5. No Docker / no DB. Legs 3/4/8 NOT run, owed by none. #1260: never execute sync-secrets.sh, never `az` (a logging shim; log EMPTY).
6. Fleet STOP: claimable BY READ for #1258/#1259/#1260/#1261 (and #1256 only through gate24T2b's drafter's surviving reads); none for #1245 (format
   gate) or #1257 (early return). The count after merge is READ FROM THE DEVELOP IT LANDS ON (49/6 now; 55/10 once gate24T2b's #1250/#1253 land).
7. Foreign keys un-hyphenated in squash bodies (MG-3: #1259 KS-1034 KS-853 KS-859 KS-916; #1261 KS-1266); subjects <= 92 (MG-11; #1245's head commit is 94,
   its PR title 90).
8. GO string `GO: merge #1245, #1256, #1257, #1258, #1259, #1260, #1261 batch` (or the subset).
9. Routing `QA/Secuura-batch1245r2` — PROPOSED line `QA/Secuura-batch1245r2|coagent@agentmail.to|yes`, NOT written by the drafter.

## LEGITIMATE SHAPES (BRIEF_TEMPLATE §2a) — the PRs that change a CHECKER
Predicted-by = drafter. "live" = the drafter's own real vitest 4.1.11 runs through spawnSync (drafter_liveshape_g24c.py, liveshape_2.out), read by a
BYTE-LIFTED copy of the head's reader block; "port" = a Python copy of a reader (a READ instrument, never evidence). The gate MEASURES every row.

### #1245 `readChildOutput` (a checker of vitest's own output) — live, 29 shapes
| shape | vitest's own summary | correct | stdout-only (THE PRODUCT INPUT) | JOINED (the seat's named claim) | develop |
|---|---|---|---|---|---|
| S1-S16 (the gate24T2a set) | printed | its Tests line | correct x16 (S15 NULL = correct refusal) | correct x16 | NULL on S1-S5, S7-S9, S11-S13; {5,0} on S16 |
| S17 console.error lookalike | `1 failed \| 1 passed (2)` | {1,1} | {1,1} | {1,1} | {1,1} |
| S18 diff context lookalike | `1 failed \| 1 passed (2)` | {1,1} | {1,1} | {1,1} | {1,1} |
| S19 (the seat's) Test Files + Tests logged to stdout | `1 failed \| 1 passed (2)` | {1,1} | {1,1} | **NULL — WRONG** (the stderr code frame carries ` Test Files `) | {7,0} |
| **H1 KILLED-AFTER-LOOKALIKE** (spawnSync timeout after S19's log) | **NONE** (ETIMEDOUT, rc 143) | NULL | **{7,0} — WRONG, silent** | **{7,0} — WRONG** | {7,0} |
| H1b killed after a Tests-only lookalike / H1c killed, none | NONE | NULL | NULL / NULL | NULL / NULL | {5,0} / NULL |
| H2 late console.log / H3 late stdout.write / H4 exit-hook write | printed | {2,1} / {1,1} / {1,1} | correct x3 | correct / NULL / NULL | correct |
| H5 FORCE_COLOR=1 / H7a CI=true / H7b --silent=true | printed (stdout) | {1,1} | correct x3 | correct / correct / NULL | correct |
| H6 unhandled error after passes (Errors line, rc 1) | `2 passed (2)` | {2,0} (the line) | {2,0} | {2,0} | {2,0} |
| H8 console.error of both lines / **H8b diff context of both lines** | `1 failed \| 1 passed (2)` | {1,1} | {1,1} / {1,1} | NULL / **{9,0} — WRONG, silent** | {1,1} |
| H9 a failing test NAMED with ` Test Files ` | `1 failed \| 1 passed (2)` | {1,1} | {1,1} | NULL | {1,1} |

### #1245 the call-site pin (READ)
| arm | the "behavioural" cell (`readChildOutput(S17_STDOUT)`) | the text pin | predicted |
|---|---|---|---|
| T-CALL (ii) joined streams again (the seat's E2) | GREEN | RED (`readChildOutput(result.stdout)` absent) | RED |
| **T-CALL (iii)** inline reading + comment `// readChildOutput(result.stdout)` | GREEN (never enters childSuiteCounts) | GREEN (comment satisfies toContain) | **GREEN — the must-change item NOT met** |
| **T-CALL (iv)** calls readChildOutput, returns `{245,0}` | GREEN | GREEN | **GREEN** |

### #1261 CONFIGPINNED (port) — 9 subject files, 11 bases, floor 8; a file that no longer MENTIONS the key is SKIPPED
| env line deleted in | still mentions the key | pinned after | CONFIGPINNED |
|---|---|---|---|
| ks1213 (the ticket's named file), ks1293, ks444 x2, ks445, ks520, ks543 | yes | 8-10 | RED — correct |
| **ks1228-a-refused-request-writes-no-provenance-row (:26)** | **no** | 10 | **GREEN — WRONG on the named shape** |
| **ks1264-revoke-records-its-action-provenance-row (:16)** | **no** | 10 | **GREEN — WRONG on the named shape** |

### #1256 the ks1061 guard (port) — develop / head / END_TREE: 21 factories, 0 offenders under BOTH guards; BACKTICK and NAMED-FACTORY unread by any cell.
### #1260 the census (port) — CELL 4 regex over every tracked *.sh: BASE {sync-secrets.sh 8, validate-env.sh 3}; END {validate-env.sh 3} (the ticket's "NOT defects").
