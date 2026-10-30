## QA GATE - TIER 1, round 1: GO WITH NOTES
(Filed by the Wednesday seat from gate 35's returned text, 16:5x. Probes moved from the session scratchpad to `probes/` beside this file; every `scratchpad/g35/...` path in the gate's text now reads `0_Brain/reference/2026-10-30_gate35-1832/probes/...`.)

**Subject:** PR #1832 (Secuura/Distributed_Secuura), KS-1857, author Seat E 22nd — check-no-sql-injection.sh skips node_modules and reports a real hit.
**Head:** `2db15a998cfbd5023ab601ae12326457ed39544a`, ls-remote equal at 16:34:10 and 16:51:33 AEDT. Merge-base 85cd24d81cb9; develop a8c554659cb3; range adds no RawUnsafe line; guard script byte-identical base vs develop. merge-tree conflicts ONLY in the two Projects Documents html (docs-only, not a finding).
**Gate:** 35, tier 1 (raised by Wednesday: narrows a security guard's scan). Clone `repo/` here, push URL `no_push_qa_gate`. Nothing pushed/commented/merged; nothing written under !CODING.

### Verdict
The exclusion cannot hide product code develop's guard saw: BSD `--exclude-dir=node_modules` is an exact case-sensitive basename match, and every path under such a dir already contained the substring the old `grep -v` dropped. Proven by behaviour: 47 planted cases, exit codes identical develop vs head; M1 (exclusion removed) identical to head. The `$` escape fix is correct (develop printed only "queryRawUnsafe: unbound variable"). Red-first 3/4 + 2/4 at develop, 4/4 + 4/4 at head. Real worktree with 27 node_modules trees: head 0.6-28 s vs develop 86-348 s, all rc 0.

### Findings
- **F1 Minor — FIX BEFORE MERGE (one real-grep cell).** Both suites stub grep; M7 (`--exclude-dir=src`) and M8 (`--exclude-dir='*'`, guard BLIND: rc 0 "OK" with three planted violations) survive all 8 cells. Fix: one cell running the real grep on a throwaway tree (violations in services/a/src/x.ts, services/a/src/node_modules_shim/x.ts, services/a/node_modules/p/i.js); assert rc 1, first path reported, node_modules/ one not. The PR's "Real-grep arms 6 of 6" are uncommitted. Evidence: probes/mut/M7-*.sh, M8-*.sh, realprobe.sh.
- **F2 Major, PRE-EXISTING — FOLLOW-UP (= KS-1865).** Line-34 post-filter `grep -v 'node_modules\|/dist/\|src/db.ts:.*\\\$queryRaw\|originate/src/db.ts'` substring-matches the whole line: hidden (rc 0) at develop and head: src/node_modules_shim/, foo.node_modules.ts, my_node_modules/, SQL text with `/* node_modules */`, src/dist/, services/not-originate/src/db.ts, content with `/dist/`. Fix: filter the path field only, segment-anchored `(^|/)node_modules/`, `(^|/)dist/`, exact `services/originate/src/db.ts`. Exposure today none (census `git ls-tree -r` at 2db15a9: 4,806 paths; 1 contains node_modules = the new test, outside roots; 0 /dist/ under roots). Not covered: untracked trees on disks.
- **F3 Major, PRE-EXISTING — FOLLOW-UP.** Independent multi-line scanner (probes/indep.py, 1,250 files) finds 3 interpolated *RawUnsafe templates the guard reports 0 of (develop and head): `packages/shared/src/db/optimization.ts:105` ($queryRawUnsafe<T[]>( with `${model}` / `${relatedField}`; exported at packages/shared/src/index.ts:18; no in-repo caller found); `services/originate/src/routes/signatories.ts:346` and `services/originate/src/routes/webhooks.ts:310` ($executeRawUnsafe( newline then `UPDATE ... SET ${...join(', ')}`). Exploitability NOT judged (column names look whitelisted, not traced). Also not scanned: .mjs/.cjs/.mts/.jsx (0 RawUnsafe files in those today).
- **F4 Minor, PRE-EXISTING — FOLLOW-UP.** `2>/dev/null ... || true` with pipefail: a grep error reads as clean (unreadable file with a violation -> rc 0 OK; both roots missing -> rc 0 OK). Fix: grep status 1 = no match, >= 2 = fail.
- **F5 Info.** Timing above confirms the motivation.

### Mutants
Gate's reconstruction M1-M6 (author's exact six not in repo; PR body unread, no gh auth): all killed. M7, M8 SURVIVE (F1). M9 equivalent (F2 already hides). M10 (`--exclude='*.ts'`) equivalent on BSD grep, untested on GNU grep.

### NOT TESTED
GNU grep semantics (guard runs only in pre-push; no .github workflow references it); the author's exact six mutants; the whole 101-suite shell runner; full pre-push timing / cache control; untracked node_modules/dist on seats' disks; exploitability of the F3 update sites.

### Instrument faults
Interactive `grep` is a ugrep wrapper: censuses used /usr/bin/grep, guard ran under PATH=/usr/bin:/bin. Hook refused `git -C $R` with a variable path (re-run literal). A Python f-string error in indep.py fixed before any result was read.
