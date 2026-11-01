# QA GATE 87 (tier 2) - Secuura/Distributed_Secuura PR 1903 (KS-1867 + KS-1865, check-no-sql-injection.sh)

## BLUF: GO WITH NOTES. Nothing is fix-before-merge.
The guard does what the PR claims. The in-scope cases (multi-line call, generic, .mjs/.cjs/.mts/.jsx, a changed allowed site, a removed entry, a new site) all behave correctly, and it is green on the head tree with the two counts printed separately.
The detector has holes for shapes that are out of KS-1867's stated scope, plus two shapes that are arguably in scope (comment between `(` and the template; `?.(`). They are notes, not blockers, because the PR's own cheat-sheet fragment says "Not measured here: a query built in a variable or by concatenation first".
No new push-blocking behaviour on the current tree: run-code-guards.sh rc=0, 13 guards green.

## Heads
- Start (ls-remote, logs/lsremote_start.log): PR head 12bafc96c91262f7a6ee218f1d5cd8eda84bf858, develop 8afcf256ed5fb38d05f7273e08e1b912446bac5c. Both match EXPECTED. Parent ca36945e974081be6abbc15e548f4f8d02767e14, one commit.
- End: spark_gate asserted head == tip of refs/pull/1903/head at ~+20 min (logs/step0_spark_gate.log). I did not re-run ls-remote at the end, so the end-head claim rests on that assertion only.
- merge-tree of pr1903 onto 8afcf256: clean, rc=0, tree 17b6f336b1fed651e1648ea1fabcb215633117a3 (logs/q6_mergetree.log).

## FINDINGS
- G87-F1 (Low/Note, in-scope-adjacent): a comment between `(` and the template hides the site. `db.$queryRawUnsafe(/* c */ \`SELECT ${t}\`)` and `( // c\n \`..${t}\`)` are both MISSED (rc=0). The awk skips whitespace only. A comment before the template is the "call split across a comment" shape you asked about. Trivial to fix (skip `/*..*/` and `//..` in the whitespace skip).
- G87-F2 (Low/Note): other trivially-shaped misses. Parenthesised template `((\`..${t}\`))`, optional call `$queryRawUnsafe?.(`, bracket access `["$queryRawUnsafe"](`, `.call(db, ...)`, `.bind(db)` alias, and a generic containing `(` such as `<(a:number)=>void>` (regex `<[^(]*>` cannot span a paren) are all MISSED. Rare in this codebase; the header does not claim them.
- G87-F3 (Note, out of KS-1867 scope, disclosed): a template built in a variable then passed (`const q = \`..${t}\`; $queryRawUnsafe(q)`), `String.raw\`...\``, `'..' + x` / `".." + x` concatenation, and `buildSql(t)` are MISSED. The header says "first argument is a template literal", and the fragment discloses variable/concatenation as unmeasured. Concatenation is named in the guard's own title ("string-concatenated SQL") so it is a documented limitation, not new. Recommend a follow-up ticket.
- G87-F4 (Low): under a UTF-8 locale, BSD awk 20200816 dies with `towc: multibyte conversion failure` on a source file containing invalid UTF-8 (probed with a lone 0xFF byte). The guard fails closed with exit 2 and shows the message; under `LC_ALL=C` the same file is scanned and reported (rc=1). No tracked file triggers it today (the head tree is green), so nothing is newly blocked. It could surprise a future push that adds such a file. It would be worth a line in the header.
- G87-F5 (Note, design): the allow key pins the sink (path + opener text + interpolated expression text) but not the producers. If someone later pushes unvalidated input into `updates` or `setClauses` elsewhere in the same function, the allowed site still matches. This is inherent in the approach; the two reasons record the trace at develop ad78fa106785, and the entry should be re-traced if the function changes.
- G87-F6 (Spark calibration, not a PR finding): spark_gate reported merge_base empty and diff 0 files when given a sha as the base ref. Its "targeted on BASE product code" then read 71/71 pass, where the real result against the base script is 21 pass / 50 fail. Spark review then said "PR is test-only, no product code" and "tracing not addressed". Both statements are false. See the calibration section.

No HIGH finding. G87-F1..F5 do not block merge.

## Q1 - fixed guard on the head tree, plus mutations
- run-code-guards.sh on the head tree: rc=0, 13 guards passed, prints `ALLOWED (2)` and `ALLOWED-OPEN (1)` as separate lines, `OK ... (40 files naming *RawUnsafe examined)` (logs/q1_guards.log, 6.6 s).
- Scratch copy of services/packages/scripts (evidence/scratch), mutations in logs/q1_mutations.log:
  - 4th multi-line site (`db.$queryRawUnsafe(\n \`SELECT 1 FROM ${t}\n ...\`)`): rc=1, reported at zz_new.ts:2 with the expression `t`.
  - Remove the webhooks entry: rc=1, webhooks.ts:310 reported, ALLOWED (1).
  - Change the allowed expression (`updates.join(", ").concat(" , evil")`): rc=1, reports the site with the new expression and also reports the stale entry (allow list line 12). Both fire. The key does not cover a changed line.
  - Pristine after reset: rc=0, back to ALLOWED (2) / ALLOWED-OPEN (1).

## Q2 - can the allow list be abused?
- The path is compared as an exact string with the paths grep prints. A copy of the webhooks site as `webhooks.tsx` (M5) and as `routes/sub/webhooks.ts` (M5b) is each reported (rc=1). Same opener text in another file does not match.
- A second identical call in the same file (M4, appended at :593) is reported. The entry is consumed once, and the first site found (:310) takes the entry.
- Not abusable by the shapes tried. Residual: F5, and a reason string that starts with "OPEN:" is the only thing that moves an entry to ALLOWED-OPEN. That is by design and is counted apart.

## Q3 - the two ALLOWED sites read at the head
- webhooks.ts PATCH /:id (:255-:330): `updates` receives only the literals `url = $N`, `events = $N`, `description = $N`, `is_active = $N` and `'updated_at = NOW()'`, where N is the counter `idx`. Every value goes into `values` and is passed as a bound parameter after the SQL (`...values`). The final `WHERE id = $${idx}::uuid` is the counter. The body is also zod-validated first (KS-445). SAFE as ruled.
- signatories.ts PATCH /:id (:295-:365): `setClauses` receives only the literals `updated_at = NOW()`, `display_name = $N`, `title = $N`, `document_types = $N::jsonb`, `can_delegate = $N`, with N taken from `params.length`. `idIdx` and `tenantIdx` are `params.length` (numbers). Values are bound via `...params`. SAFE as ruled.
- No HIGH finding. The optimization.ts:105 ALLOWED-OPEN entry is as Wednesday ruled (KS-1929, 0 in-repo callers per the entry). I did not re-measure callers.

## Q4 - false negatives (logs/q4q5_probes.log, logs/q4b_probes.log)
| Shape | Result | In KS-1867 scope? |
|---|---|---|
| multi-line template, single-line template, `.mjs`, `<T[]>` generic | CAUGHT | yes |
| backtick nested inside a `${}` | CAUGHT | yes |
| template in a variable, then passed | MISSED | no (disclosed) |
| `String.raw` tag | MISSED | no |
| `'..' + x`, `".." + x` | MISSED | no (title names it, header limits to templates) |
| `buildSql(t)` | MISSED | no |
| comment between `(` and the template (block or line) | MISSED | arguably yes (G87-F1) |
| `((template))`, `?.(`, `["$queryRawUnsafe"](`, `.call`, `.bind` alias | MISSED | edge (G87-F2) |
| generic containing a paren | MISSED | edge (G87-F2) |

## Q5 - exit codes and the grep-error path (logs/q4q5_probes.log)
- Missing packages/: rc=2, message "the scan root packages/ does not exist". The headline says "(grep exit 0)", which is slightly misleading but harmless.
- Unreadable file (chmod 000): rc=2, "grep: services/originate/src/zz_unread.ts: Permission denied", with and without LC_ALL=C.
- Malformed allow-list line: rc=2 with the line number.
- Clean tree: rc=0, same under LC_ALL=C. Violations: rc=1.
- Invalid UTF-8 in a source file: default locale rc=2 (awk towc failure), LC_ALL=C rc=1 and reported. See G87-F4.
- Not run: GNU/mawk awk (only BSD awk on this host), and Linux grep.

## Q6 - suites, base red, syntax, runner, docs, merge
- 5 suites on the head (logs/q6_head_*.log): allow_list 15/15, multiline 22/22, path_filter_and_scan_errors 25/25, reports_the_hit 4/4, skips_node_modules 5/5 = 71/71.
- Same suites against a byte copy of the base script (CHECK_NO_SQL_INJECTION_SH=evidence/base_check.sh, from `git show pr1903~1:`; logs/q6_base_*.log): 0/15 pass, 9/22, 6/25, 4/4, 2/5. That is 50 RED and 21 pass, which matches the claim. reports_the_hit is all controls and passes on base.
- `bash -n` is clean on all 5 suites and on the guard.
- run-shell-suites.sh `--list`: rc=0, the 5 sql-injection suites are listed. `--check-unreached`: rc=0, "all 110 tracked shell suite(s) are reached".
- SKIP lines: none of the 5 suites prints a SKIP line (the grep hits are the words "skipped"/"skips" in case names). There is nothing to check against the runner regex (cf. G83-F1).
- docs-fragments `check --root repo`: rc=0, "lint clean, render passes" (two ADVISORY lines on committed-page drift are pre-existing). With a planted unclosed `<table>` in the new cheat fragment: rc=1, "tags are not balanced ... FAIL" (logs/q6_docs_planted.log).
- Not re-run: the claimed mutants 42/42 and hook 13/16 with leg 15 passed (not asked as a re-run in the question list; no evidence from me either way).

## Spark calibration (Step 0, evidence/spark_shadow/, logs/step0_*.log)
- spark_gate.sh rc=0, 22 s. HEAD: 5/5 files, 71 passed, 0 failed. Correct.
- BASE run: also reported 71 passed, 0 failed. WRONG as a red-against-base signal. The tool printed `merge_base` empty and `diff {'files': 0}`, and diff.patch is 0 bytes. I passed the base as a SHA (8afcf256) in a blobless clone. The probable cause is the merge-base lookup failing, so the "base product code" worktree was the head's. I did not debug it. A vacuous base run reads as "tests do not discriminate", which is the opposite of the truth (50 red).
- spark_review.py rc=0, verdict "GO WITH NOTES", 4 Notes. Three are false: "the PR is test-only, no product code", "the tracing in criterion (b) is not addressed". Both come from the empty diff. One is fair: the facts do not include a run of the real guard on the three real sites; I measured that in Q1.
- Takeaway: with an empty diff, Spark was confidently wrong rather than silent. A tier-1 rule would be: refuse to review (or flag) when diff.patch is 0 bytes or merge_base is empty. Its verdict agreed with mine by luck, not by evidence.

## Notes for the PR body
- State that the detector is limited to a template literal written directly as the first argument; list the variable, concatenation, String.raw and comment-split shapes as not covered. Optionally add a follow-up ticket.
- Consider fixing G87-F1 (comment skip) in this PR since it is a few lines and is the shape asked about.
- Add one header line: awk is read under the caller's locale, and a source file with invalid UTF-8 fails the scan (exit 2) under UTF-8 locales.
- Note that the allow key pins the sink and the opener, not the producers (G87-F5). Re-trace on change.
- The 50 RED / 71 figure reproduced exactly. The mutants 42/42 and hook 13/16 figures were not reproduced by this gate.
