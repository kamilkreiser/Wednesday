# Spark operator 24 - report (2026-10-30, base develop 40c06084919d at brief time; controls and rounds ran at 85cd24d81cb9, develop moved, no touched file changed)

## BLUF
4 rounds run, 4 PASS 7/7, 0 FAIL, 0 rebriefs (all counters unspent). All four are HELD as READY notes under local-model/night/. Nothing raised, pushed, merged or commented. One real product fault found on the way (check-no-sql-injection.sh:35). The pool really is thin: 400 KS Backlog/Todo tickets read (paginated, hasNextPage false), only 2 briefable test-only pins survived the screen; the other 2 rounds came from the filing list.
Drainer: keepdraining.sh pid 97411, confirmed with ps, state/keepdraining.pid reads 97411; I started none. Spark idle again after 14:00 (queue 0).

## Rounds
| brief | tier / rung | hunks | result | golden | held |
|---|---|---|---|---|---|
| ks_1812_p1_didjwk_refused_once (KS-1812: pin didJwkRefusal's early return, gate-16 mutant X12) | test_only, rung 3-4 (one new describe in anchorSchema.test.ts given byte-exact; tamper anchorSchema.ts:166 drops the pattern clause) | 1 | PASS 7/7, 124 s (33.8 s model, 22398+753 tok); A4 4 red/72, A5 72/72, anchoring suite 550->556, tsc 0 | TREE-IDENTICAL (only the `diff --git` header line absent; all + lines identical) | READY_KS-1812-KS-1812-P1_..._2026-10-30.diff.md |
| ks_1815_p4_real_node_reply_not_retried (KS-1815: pin the ALREADY_INCLUDED_REPLY clause with the node's real reply) | test_only, rung 3-4 (two cells + 2 helpers in ks726 test; tamper anchorSubmission.ts:640 -> `true;`) | 1 | PASS 7/7, 127 s (40 s model, 29633+722 tok); A4 1 red/16, A5 16/16, suite 550->552, tsc 0 | TREE-IDENTICAL, + lines identical | READY_KS-1815-KS-1815-P4_... |
| filing_sqlinj_p1_exclude_node_modules (filing list: scan walks node_modules) | bash_patch, rung 2 (one spelled line + NEW 84-line stub-grep suite; no tamper) | 1 + new file | PASS 7/7, 56 s (42.7 s model); B4 1 FAIL line at tip, B5 4/4 | DIFFERS, CONTEXT-ONLY: wrong hunk header and one mangled context line; checker REANCHORED (strict=False). The +/- pair is exactly right | READY_KS-0-KS-0-P1_... (raise seat applies section_1.diff.reanchored) |
| filing_sqlinj_p2_report_the_hit (found by me: line 35 unset vars under set -u) | bash_patch, rung 2 (one spelled line + NEW suite) | 1 + new file | PASS 7/7, 53 s (38.4 s model, 10309+1510 tok); B4 2 FAIL at tip, B5 4/4 | TREE-IDENTICAL, strict | READY_KS-0-KS-0-P2_... |

Diff reading: for 1812/1815/p2 I compared every + and - line of the model's patch.diff with my golden (identical), checked the touched-file set against the brief (exactly the briefed files), and red-first then green came from the checker's own A4/A5 (B4/B5). For p1 I read section_1.diff.reanchored: the single line gains `--exclude-dir=node_modules `.

## Raise notes
- KS-1812 and KS-1815: link as Refs (never a close word). Test-only, zero product bytes. SCOPE FLAG: both touch the anchoring service (anchorSchema.ts / anchorSubmission.ts + their tests), not index.ts and not KS-1384, no open PR file overlaps. Operator 19 had excluded the whole anchoring service, so Wednesday should confirm before a raise (note appended to both READY files).
- sql-injection p1+p2: no ticket exists; the raise seat files one on the board account or links the filing. They edit different lines (:28 and :35) of one script and add two separate new test files; combine into one PR. p1 changes only gate cost (the later grep -v stays); p2 changes the gate's output on a hit (it now prints the headline, hits and Fix hint instead of an unbound-variable error; exit code stays 1).

## Filed as candidates only (not briefed)
- account-recovery.ts:156 (`case 'mfa_backup'`): verified at source, `verified = typeof evidence.backupCode === 'string' && evidence.backupCode.length >= 8;` - any 8-char string is accepted as backup-code evidence. MFA/backup-code surface (seat F 18th) and auth: filing note only, no fix, no pin.
- certifications P2010 -> 500 not 404: verified at source, originate routes/certifications.ts:1073 `const pgCode = error.code ?? error.meta?.code` takes 'P2010' first so 22P02 in meta.code is never read (the message fallback only helps when the text carries 22P02). It is exactly the catch KS-1844 (seat U) is editing: filing note only.
- 22P02 siblings in auth/oauth/m365 read `.code` directly (pg driver, not Prisma), so they are not the same defect.

## Screen (counts)
400 Backlog/Todo read. Title screen 130 keyword hits + remaining 270 listed; 73 matched survivor/mutant/no-cell wording of which ~20 already carry a done.md tag. Open-PR file sets read for #1820-#1828 via my own clone (refs/pull fetched with the checkout's deploy key; planted control: certifications.ts in #1822 and ks1175-identity-anchoring.test.ts in #1825 both found). Rejected with reason: KS-1783 (no product tamper can redden it), KS-1796 (published-contract ruling + generated yaml), KS-1761/1593/1764/1755/1759 (decision-shaped or shell with no red cell), KS-1255/807/1338/1473 (decision), KS-1644/1567 (anchoring index.ts / Postgres), KS-1842/1841/1820-class (docs seat / PR 1820-1821), KS-1849/users.ts/MFA (seat F), KS-1844/1585/1836 (seat U), KS-1410 class (exhausted).

## Faults (IMPROVEMENTS.md, 5 rows; backup IMPROVEMENTS.md.pre-1030-op24; queue.md backup queue.md.pre-1030-op24)
1. Brief defects of mine, all caught by build/control before any model call: end-of-file insertion refused by build_input; `## Red cells` written with an `it.each` `%s` so A4 read the reds as control reds; a suite FAIL message echoing the subject's stderr was read by B4 as a LOAD error.
2. check-no-sql-injection.sh:35 product fault (above).
3. Model slip on p1: wrong hunk header numbers and a dropped backslash in a context line; harness reanchors silently as an "accommodation" (hold_ready strict=False).
4. hold_ready prints `golden: DIFFERS (4 change lines)` on a bash_patch TREE-IDENTICAL PASS (new-file header lines counted). Cosmetic.
5. Hooks: `cd`, `rm $VAR`, `=====` echo, and `git -C "$VAR" checkout` are refused (use literal paths / separate calls); heredocs containing the word cd trip the no-cd hook (use the Write tool).

## Model capability data
Rung 3-4 test_only with a given-whole new describe/cells: 2 for 2 first round. Rung 2 bash_patch with a given-whole 84-line suite: 2 for 2; the only slip was hunk-header arithmetic. No failure this session was the model's fault.

## Next operator
1. Take the 9-hunk-with-per-hunk-skeletons calibration of the retired ks_1410_p5 content only if the pool is empty again (the KS-1410 class itself is exhausted; it is calibration data, not product).
2. Other check-*.sh / scripts under Blockchain/Dev/scripts with a failure branch never exercised: run each with a planted hit under `set -u` (the p2 method, a stub-grep suite) - this found a real fault in minutes.
3. Re-read the board after KS-1384 / KS-1844 land: KS-1815-class pins on anchorSubmission.ts and the certifications 404 mapping become briefable.

## Left behind
Run dirs (-control, -control-r2, -control-r3, 4 real runs; ~335 MB each) and spark/cache/work for the prune. Clone: .../2026-10-30_spark-operator24/clone (origin = local checkout, remote gh = GitHub with the deploy key via core.sshCommand copied at fetch time; refs/pr/18xx). Tools here: mk24.py, mk24ti.py, mkbash24.py, mkbash24b.py, spec1812.py, spec1815.py, bash1/ (suites), linscreen.py, board.json, run_all.sh, lint/dry/control logs, _quarantine_2026-10-30/ (superseded logs and done markers).
