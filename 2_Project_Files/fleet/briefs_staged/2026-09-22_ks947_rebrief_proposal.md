# PROPOSAL — KS-947 rebrief 1 of 1 (Kam's 2026-09-16 counter): `KS-947-R16-F3F4b.md`, input built + golden-prechecked PASS 8/8 (rebrief drafter, 2026-09-22 02:3x)

## Queue line (Wednesday copies the input into night/inputs/ and queues it — the drafter touched neither)
```
KS-947 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/test_only_947F3F4b-R16.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/test_only/task.md ctx=65536
```

## build
```
# build: bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/test_only/build_test_only_input.sh KS-947 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/test_only_947F3F4b-R16.json /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-947-R16-F3F4b.md tip=64ab105132eada0621622acf4d6053bc59926780 ctx=65536
```
Built by the drafter with the SAME command into the scratchpad (rc 0): `'+' 66 '-' 0 in 1 hunk(s); tampers 3 (F3SKIP->1, F4AUTH->2, F4USERS->2); controls 4; RUNNER PINNED vitest`.

## Where things sit
- Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-947-R16-F3F4b.md` (15702 B, sha256[:16] `f950b91dde2150ba`). The original `KS-947-R16-F3F4.md` is untouched.
- Built input (drafter scratchpad — copy to `night/inputs/test_only_947F3F4b-R16.json`): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/b24cb7de-7a4a-4dad-80d5-bd3b1a9cc168/scratchpad/rebrief947/inputs/test_only_947F3F4b-R16.json` (29886 B, sha256[:16] `7e7410fb0affff8c`). Key set vs `night/inputs/test_only_947F3F4-R16.json`: set(good)-set(mine) = [] and set(mine)-set(good) = []; only `ticket.title` differs (the new header). `expected_plus` 66 lines, 0 with a backslash, 0 with a double quote.
- Golden run: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/b24cb7de-7a4a-4dad-80d5-bd3b1a9cc168/scratchpad/rebrief947/golden/` (`out.md`, `checker.log`, `out.md.checker/`, `prepare.log`), script `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/b24cb7de-7a4a-4dad-80d5-bd3b1a9cc168/scratchpad/rebrief947/golden_947b.sh`, log `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/b24cb7de-7a4a-4dad-80d5-bd3b1a9cc168/scratchpad/rebrief947/golden_947b.log`; clone `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/b24cb7de-7a4a-4dad-80d5-bd3b1a9cc168/scratchpad/rebrief947/clones/bc` (`git clone --shared --no-checkout` + `checkout --detach 64ab10513`).

## Golden verdict
`RESULT: PASS (8/8)` — T1 · T2 · T3 strict · T4 66/66 byte-exact · T5 10/10 cells green at the tip · T6/T7/T8 for F3SKIP (1 red), F4AUTH (2 reds incl. PARITY), F4USERS (2 reds incl. PARITY) — red sets == declared exactly, every control green, index.ts restored by bytes ×3. Source checkout tracked-modified 0 before / 0 after.

## Grep controls (`/usr/bin/grep -c -E "\\\\['\"]"` over the `+` lines)
| file | backslash-quote `+` lines | double-quote `+` lines | `+` lines |
|---|---|---|---|
| NEW `KS-947-R16-F3F4b.md` | **0** | **0** | 66 |
| ORIGINAL `KS-947-R16-F3F4.md` | **0** (see the finding) | 2 | 62 |
| positive control: the model's `runs/2026-09-22_ks947-ornith35b-night/out.md` (whole file) | **1** (`\"''\"`) | — | — |
| positive control: the NEW brief whole file (its rebrief note quotes the escaped forms) | 1 | — | — |

## FINDING — the commission's premise is off by one layer (no action needed beyond reading this)
The original brief's `+` lines carry NO backslash: the `MISSING '+' 'const blanked = call.replace(/\'[^\']*\'/g, ...'` text in `checker.out` is Python `repr()` quoting a string that holds both quote kinds. What Ornith actually emitted (`out.md.raw.json`, decoded once) is `call.replace(/'[^']*'/g, \"''\")` — it ESCAPED the two double quotes on the one `+` line that mixed a quote-laden regex literal with a `"''"` string; the other 61 lines were byte-exact, including line 38's `indexOf("app.use('/api/users/me/mfa'")`, which also mixes quote kinds. So the class is "the model inserts backslashes on a mixed-quote line", not "the brief carried them". The standing rule in IMPROVEMENTS (grep the brief's `+` lines for `\'`/`\"`) would have passed this brief unchanged; the rule that would have caught it is the one applied here: **no double-quote character in any `+` line** (single-quote-only; a quote character the code needs comes from `String.fromCharCode(39)`, and a quote-pair regex becomes `new RegExp(...)` from it). Wednesday may want the IMPROVEMENTS KS-947 row's cause column corrected to that.

## What changed in the brief (intent, six cells, three tampers, reds, controls: IDENTICAL)
- `+ const QUOTE = String.fromCharCode(39);` and `+ const STRING_LITERAL = new RegExp(QUOTE + '.*?' + QUOTE, 'g');` (+1 doc-comment line) replace the inline `/'[^']*'/g, "''"`; `blanked` becomes `call.replace(STRING_LITERAL, QUOTE + QUOTE)...` — same blanking semantics (a literal becomes `''`).
- Order control: `usersCall = mountCall('/api/users/me/mfa')` + a not-null expect, then `GATEWAY_SRC.indexOf(usersCall as string)` — replaces the mixed-quote needle `"app.use('/api/users/me/mfa'"` (the index of the extracted call text is the mount's position: `mountCall` slices it out of `GATEWAY_SRC`).
- Hunk header `@@ -96,4 +96,70 @@` (was `+96,66`); THE MODE and Output sections now say single quotes only, never escape or change a quote kind.
- Header carries: "REBRIEF 1 of 1 (Kam's 2026-09-16 counter) - brief defect: backslash-escaped quotes", plus a Rebrief note stating the finding above precisely.

## Not done / bounds
- No model run (the drafter's bound); the golden proves gradeability at the tip, not that Ornith reproduces 66 `+` lines.
- `night/queue.md`, `night/inputs/`, the original brief, and the Secuura checkout: untouched (read verbs only; the `--shared` clone is in the scratchpad).
