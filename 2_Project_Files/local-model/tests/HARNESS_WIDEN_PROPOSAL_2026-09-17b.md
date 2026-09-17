# Harness widening proposal: which ONE widening unlocks the most tickets (2026-09-17b)

Measured 19:24:50–19:37:37 AEST by a read-and-measure agent. Nothing built, queued or edited except this file.

## BLUF

**Build a `comment_patch` tier.** It covers comment and docblock edits in `.ts` files. No test cell can go red for these, so every search refused them ("comment-only: no cell can red it"). The new checker grades them with a TypeScript **token-equivalence** gate instead of a red cell: the file's code tokens before and after must be identical.

- **Tickets it unlocks now: 5** (about 8 model rounds, one file per input):
  - KS-979
  - KS-1118 F-3
  - KS-1120 F-3
  - KS-1156 A.2 + A.3
  - KS-1179 F-4 (plus the docblock half of F-5)
- **One more once two READYs merge:** KS-1180 P-1005-3. Its file, api-gateway `routes/verification.ts`, is carried by READY_KS-1073 and READY_KS-1185-F1.
- **Two tickets finish:** once their held READYs are raised, the comment row is the last open item on KS-1118 and KS-1120.
- **One ticket closes outright:** KS-979.
- **First 3 to brief:**
  1. **KS-979** — `services/originate/src/__tests__/ks597-issuer-org-bind.test.ts:171-174`
  2. **KS-1118 F-3** — `services/originate/src/routes/verification.ts:739-741`, plus `__tests__/ks1103-verify-hash-field.test.ts:15-17` and `:203`
  3. **KS-1156 A.2 + A.3** — `services/api-gateway/src/middleware/scopes.ts:125-126`, plus `__tests__/ks835-oauth-token-scope-gate.test.ts:59`

  Each input changes 1–4 comment lines. All three are Backlog, and their files have 0 open-PR paths, 0 READY hunks and 0 live seat-head changes at `efaaa6034`.
- **Effort: 1 agent-session.** That covers the builder, the checker with a new C4 gate, task.md and the arms. Add **+0.5 session** for the optional C2p ASCII stand-in restore (see the spec).
- **The margin is thin.** The runner-up is `suite_patch`, for tickets where a test suite or guard is itself what gets fixed. It unlocks **5** measured tickets: 3 from recorded refusals and 2 found by today's screen only. It could reach about 11 if Wednesday rules the "gate's proposal" fix shapes. It costs about 2.5–3 sessions. `comment_patch` wins on certainty, cost and at-source cleanliness:
  - All 5 of its tickets are recorded refusals whose only standing reason is the missing grader.
  - All 5 are clean at the source.
  - One of the suite-class five (KS-897) is soft-partitioned by READY_KS-910.
- **Two product files is NOT the winner.** It has the largest raw count (27 tickets name it), but only **1** is blocked by it alone (KS-1197), and that one still needs a coerce-vs-validate pick and 2 live heads to clear.
- **The develop move changes no class count.** `81ee4b729 → efaaa6034` (#1021, #1024, #1022, #1023).
  - Gateway `middleware/auth.ts` still differs on 2 live heads (ks-744 `fb503741a`, ks-1195 `a067d4e3e`), so KS-744, KS-1208 and KS-1197 stay partitioned.

## 1. Classification

### Frame
- **Recorded refusal rows in `night/candidates.md`** (read whole, 574 lines), hand-classified from each row's own reason text:
  - SET ASIDE: 27 rows
  - SEARCH 17e: 17 rows, not counting its "held / recorded" roll-call line
  - ROUTED 12:07: 1
  - 17f: 4 ticket rows (KS-1156's four sub-rows counted as one ticket)
  - 17g: 48
  - 17h: 1
  - BRIEFS 17k: 2 refusals
  - 17l: 18
  - 17m: 9
  - 17n: 2
  - 17j: 19 (the 7-id "survey / not chosen" row expanded)
  - 17i: 0 new (its rows update 17g reasons; the update is applied)
- **Totals:** 148 row entries, **144 distinct tickets**.
- **Not classified by shape:**
  - 17l's 47 "21:0x title-level" ids (screened by instrument, never shape-read).
  - 17m's WIDER SCREENS.
  - The 5 tickets later briefed as FITs (KS-1009, KS-944, KS-938, KS-928, KS-1186); they are excluded from the unlock counts.
- **EXCLUDED-by-predicate block (156 rows), by predicate, not shape:** 86 "names no product file", 44 auth-shaped title (LAST), 18 Peter/Stuart, 8 PR attached.
- **Columns in the table below:**
  - **any** = distinct tickets whose recorded reasons include the class.
  - **sole** = distinct tickets whose ONLY recorded class it is.
  - **unlock** = the item-level count the widening would clear after a re-check at the source today (partition cleared or not, as measured).

| class (shape reason) | any | sole | unlock (item-level, measured) | harness-shaped? | ids (sole / unlock) |
|---|---|---|---|---|---|
| design / owner decision / either-or / unpicked fix shape | 79 | 34 | — | no (a ruling) | KS-725 KS-748 KS-758 KS-768 KS-782 KS-785 KS-829 KS-834 KS-837 KS-839 KS-840 KS-846 KS-855 KS-872 KS-903 KS-915 KS-980 KS-986 KS-1063 KS-1088 KS-1102 KS-1111 KS-1114 KS-1146 KS-1149 KS-1154 KS-1155 KS-1177 KS-1188 KS-1189 KS-1191 KS-1193 KS-1200 KS-1210 |
| two or more product files (incl. a spec co-move) | 27 | 3 | **1** (KS-1197, still needs a pick + partition) | yes | sole: KS-944 (FIT), KS-1032 (9 reads across services), KS-1157 (feature, next auth lane) |
| file held by a live lane (open PR / seat head / READY) | 27 | 4 | — | no (time) | KS-928 (FIT), KS-1194, KS-1202, KS-1204 |
| diagnosis / reproduce / measure first | 12 | 9 | — | no | KS-755 KS-757 KS-825 KS-954 KS-964 KS-1053 KS-1076 KS-1135 KS-1190 |
| test suite or guard IS the subject (no product tamper) | 11 | 3 | **5** (KS-897*, KS-906, KS-1159 + screened KS-1134, KS-1137) | yes | +6 with decision/quote blockers: KS-1131 KS-1140 KS-1142 KS-1143 KS-1144 KS-1147 (KS-960, KS-948 also) |
| owner (Peter/Stuart/Seat B lane/reallocated) | 10 | 5 | — | no | KS-530 KS-565 KS-588 KS-593 KS-1015 |
| config / yaml / json / package.json / tsconfig / nginx / compose / workflows | 10 | 2 | 2 (KS-918 needs `npm` lock regen = network; KS-1090 R2-2 is a gate leg) | partly | KS-918, KS-1090 |
| needs a real DB / live stack / live tool | 9 | 1 | — | no | KS-1091 |
| **comment / docblock only — "no cell can red it"** | **5** | **1** | **5 now + 1 after READYs** (KS-979, KS-1118 F-3, KS-1120 F-3, KS-1156 A.2/A.3, KS-1179 F-4; KS-1180 P-1005-3 screened) | **yes** | ticket-level "sole" hides 4 of them: each is a residue row beside decision/held rows on the same ticket |
| already fixed / no residue / board close | 4 | 4 | — | no | KS-777 KS-793 KS-810 KS-1192 |
| security-surface hold (no shape stated) | 4 | 1 | — | no | KS-590 |
| OpenAPI spec + regenerated yaml co-move | 4 | 0 | 1 (KS-805 item 1; yaml in open #922) | yes | — |
| non-ASCII / backslash quoting hazard | 4 | 0 | — | yes (ascii_proxy class) | always alongside a decision |
| frontend / React | 3 | 1 | — | no tier | KS-1105 |
| node script `.mjs` or non-vitest harness | 3 | 1 | 1 (KS-1040 reset half) | yes | KS-1040 |
| not a patch (checklist / tracker / feature PR) | 3 | 3 | — | no | KS-304 KS-770 KS-889 |
| over the size limit (>600-line test / 17 edits) | 3 | 0 | — | partly | — |
| service listens on import / no in-process driver | 3 | 0 | 1 (KS-730 tokenisation, partitioned) | yes | — |
| tamper is a MOVE or does not compile | 2 | 0 | — | no | — |
| outside the repo (launcher / vault / notes) | 2 | 1 | — | no | KS-925 |
| Playwright / tests/e2e | 2 | 2 | — | yes (no checker) | KS-1038 KS-1113 |
| unmockable `require('pg')` / real pg | 2 | 1 | 1 (KS-1125) | yes | KS-1125 |
| builder slug collision | 1 | 0 | — | yes (READY_KS-1179-F1 merge clears it) | — |
| In Progress / lane took it | 1 | 1 | — | no | KS-1187 |
| model failed twice (rebrief owed) | 1 | 1 | — | no | KS-789 |
| harness since fixed | 1 | 1 | — | done | KS-1186 (a3b_line) |
| frozen branch only | 1 | 1 | — | no | KS-981 |

`*` KS-897's file carries READY_KS-910's hunk `@@ -46,9`. That is 20 lines above `build_fixture` (`:74-:123`), and a READY-held file blocks a product edit under today's rule.

**Two corrections to the ticket-level count:**
1. **Per-ticket merging undercounts the comment class.** KS-1156 is recorded as A.1 decision, A.2/A.3 comment-only and R-C1 a MOVE. KS-1179 is recorded as F-4 comment-only, F-5 a pick and F-6 a slug collision. The comment rows are standalone items, so the item-level column is the one that counts.
2. **KS-1118 and KS-1120 look partitioned at ticket level, but their comment rows are not.** Their F-2 / F-1,F-2 rows are held READYs. The comment rows (F-3) sit in files those READYs do not hunk (measured: 0 READY hunks in either file).

**Pool-wide instrument (outside the recorded frame, for sizing the 86 "names no product file" rows):**
- 328 KS Backlog/Todo at 19:25:57: 19 Peter/Stuart, 73 carry a READY file.
- Existing paths cited in descriptions and comments, by type:
  - 113 service `src/*.ts`
  - 25 test files
  - 14 `.md`
  - 14 bash
  - 9 config
  - 9 `.mjs`/`.js`
  - 8 migration SQL
  - 8 OpenAPI yaml
  - 7 docker/compose
  - 6 frontend
  - 6 `*.openapi.ts`
- Non-owner, non-READY tickets by count of cited non-test, non-md files: 0 files 137, 1 file 48, 2 files 26, 3 files 12, 4 or more 13.
- The 26 two-file tickets are mostly the T5 security/feature rows that 3e68f4132 skipped at title level (KS-621, KS-625, KS-870, KS-1174 …). None has a measured shape, so none is counted as an unlock.

## 2. Re-check at the source (top 3 harness-shaped classes, 3 tickets each)

- **Linear:** GraphQL, first:25, 14 pages, hasNextPage false, 328 tickets at 19:25:57.
- **Open PRs:** GitHub REST GET, 21 PRs / 65 distinct paths at 19:26:01. Positive control: `ks839-a-wildcard-allow-list-grants-nothing.test.ts` is found in #1026.
- **READY hunks:** 120 READY diffs, 160 distinct `+++` paths.
- **Seat heads:** `for-each-ref` since 09-16 12:00 (34 refs) + `merge-base --is-ancestor` + a three-dot `diff --name-only` + a blob compare, 19:34:38.
- **Tip:** ls-remote `efaaa6034` at 19:25:45 and 19:36:43, local object present. Source porcelain 0.

| class | ticket | Linear | cited file(s) at `efaaa6034` | open PR | READY hunk | live head | stands? |
|---|---|---|---|---|---|---|---|
| comment-only | KS-979 | Backlog, 0 comments | ks597 test `:171-174` both wrong claims still present (`provenance.ts:109 … *different* org`, `for admin-issued keys`) | 0 | 0 | 0 | **unlocks** |
| comment-only | KS-1118 F-3 | Backlog | originate `verification.ts:739-741` and ks1103 test `:15-17`, `:203`: "every body that worked before keeps its answer" still present | 0 | 0 | 0 | **unlocks** (2 inputs) |
| comment-only | KS-1156 A.2/A.3 | Backlog | `scopes.ts:125-126` "KS-835 records that OAuth-minted tokens carry the `email` label too"; ks835 test `:59` "mounts eight times" | 0 | 0 | 0 | **unlocks** (2 inputs) |
| suite-as-subject | KS-897 | Backlog | `pre_push_hook_base.test.sh:74` build_fixture, `:123` `) >/dev/null 2>&1` | 0 | READY_KS-910 `@@ -46,9` | 0 | soft-blocked (READY file) |
| suite-as-subject | KS-906 | Backlog | `no_tracked_credentials_root.test.sh:212` `res=$(cd /tmp && run_check)` | 0 | 0 | 0 | unlocks |
| suite-as-subject | KS-1159 | Backlog | ks1061 guard (73 lines), `:29` non-recursive `readdirSync` | 0 | 0 | 0 | unlocks |
| two product files | KS-1197 | Backlog | gateway `middleware/auth.ts` + `routes/verification.ts` | 0 | verification.ts: READY_KS-1073 `@@ -682`, READY_KS-1185-F1 `@@ -429` | auth.ts: ks-744, ks-1195; verification.ts: 7 branches | blocked (partition + a pick) |
| two product files | KS-805 item 1 | Backlog | auth `routes/oauth.ts` + `auth.openapi.ts` + `docs/openapi/secuura-api.yaml` | **yaml in #922** | 0 | 0 | blocked (#922) |
| two product files | KS-1112 | Backlog | originate `routes/gdpr.ts:371` + spec description | 0 | 0 | 0 | blocked ("One decision, then one small change: either …") |

**Also screened for the comment class** (read, not partition-sampled beyond the file checks above):
- **KS-1120 F-3:** Backlog. vc-issuer ks1020 test header `:29-31` and `pgModel` docblock `:190-193` still overclaim. 0 PR, 0 READY hunks. Pick: reword, not "translate faithfully".
- **KS-1179 F-4 / F-5 docblock:** `ssrf-guard.ts:421-425` and `:460` "DNS-free connect" still present. 0 PR, 0 READY hunks, 0 head changes.
- **KS-1180 P-1005-3:** reword the gateway `verification.ts:353` marker comment. Blocked today by the two READYs and the branches above; its line was not re-located at `efaaa6034`.

## 3. SPEC — `tasks/comment_patch/` (do not build from this file without Wednesday's go)

**Routing.** `night_run.sh` already picks `prepare_clone.sh` and `checker.sh` from a pinned `task=`'s own directory (`night_run.sh:432-435`). A new task directory plugs in with no runner edit.

**Retry-once (optional).** Add `FAIL C[2-7].*` to the verdict regex. Until then a C-gate FAIL is a held FAIL.

### Files (all new; nothing in `doc_patch/` or `code_patch/` is edited)
- `task.md` — the model contract below.
- `build_comment_input.sh <KS-id> <out> <brief.md> product=<path> [ctx=N]`.
- `checker.sh <input.json> <out.md> <clone>`.
- `token_equiv.cjs` — runs under the clone's own `node_modules/typescript`, the package A7's `tsc` already uses.
- Copies (not imports) of `doc_patch/d6_ranges.py`, `anchor_restore.py` and the D1/D2/D7/D8 blocks, so the doc tier stays byte-identical.

### Brief format (Wednesday writes)
- `## Lines` — one bullet per range, `- :171-174`. These are the only tip lines the diff may change.
- `## The exact change` — a fenced diff. Its `-` lines are line-keyed (`:N` quoted) and its `+` lines are copied verbatim by the model.
- Optional `ascii_map U+2014=-- U+2192=->`. It applies only to lines inside `## Lines`.

### Builder refusals (rc 2, each naming why)
- **R1** `product=` is not a `.ts` / `.tsx` / `.js` / `.mjs` / `.cjs` under `services/*/src`, `packages/shared/src` or `scripts/`. Markdown goes to doc_patch and shell to bash_patch.
- **R2** The tip object is not local and there is no verified override (the sibling builders' G6).
- **R3** No `## Lines`, or a range falls outside the file.
- **R4 (the class predicate)** A line in a `## Lines` range carries a non-trivia token at the tip. A line that is part code, part comment is refused, so the brief cannot hide a code edit.
- **R5** A brief `-` line is not at the tip at its quoted number (the doc_patch missing-line check, line-keyed).
- **R6** A brief `+` line carries non-ASCII (rule of 2026-09-17 11:00).
- **R7** A `+` line is byte-identical to a `-` line in its hunk (the existing context-as-addition refusal).
- **R8 (golden self-check)** The builder applies the brief's own diff to a temp copy of the tip and runs C4, C4b and C5. A brief that fails its own gates is refused.
- **R9** A READY diff hunks the product file within 10 lines of a range. Product-edit rule; open PRs and heads stay with the search, as today.

### Model contract (task.md, verbatim intent)
1. Output ONE ```diff block for ONE file, `product_file`. Nothing else.
2. Change ONLY comment text on the lines `## Lines` names. Never change code, a string or template literal, a test title, an identifier or an import. A changed test title is a code change and is refused.
3. Every `-` line is the tip line at its number. Every `+` line is the brief's line copied byte for byte, indentation included.
4. Context lines are the file's real neighbours, byte for byte. Where a tip line inside `## Lines` carries a character listed in `ascii_map`, you may write its ASCII stand-in instead; the checker restores it.
5. Do not add or remove directive comments (`@ts-…`, `eslint-…`, `/// <reference`, `istanbul`, `*-environment`, `prettier-ignore`).

### Checker gates (each with the red arm that proves it can fail)

| gate | holds | red arm (must FAIL) |
|---|---|---|
| C0 subject | the clone is at the input's tip and the file is present (D0) | clone at the wrong SHA → FAIL C0 |
| C1 one block | exactly one fenced diff; a repetition loop is named (D1) | two blocks, or prose after → FAIL C1 |
| C2 applies | strict, then `--recount` (named), then the reanchor chain (D2) | a hunk with fabricated context → FAIL C2 |
| C2p ASCII restore (+0.5 session, optional) | a context or `-` line that is byte-equal to the tip line with `ascii_map` applied, AND that the hunk's own old-side lines place at that number, AND whose tip tokens are all trivia, gets the tip's bytes; the verdict names it | a stand-in placed one line off (MISPLACED) → FAIL C2; a stand-in one character off → FAIL C2; a stand-in on a CODE line → not restored → FAIL C2 |
| C3 touched set | == { product_file } | the diff also touches the ks597 test's product → FAIL C3 |
| **C4 token equivalence (new)** | `ts.createScanner(Latest, skipTrivia=true)` over BEFORE and AFTER yields the identical sequence of (SyntaxKind, token text), including literal text; the first difference is named as file:line | (a) golden + `ORG_B`→`ORG_A` at `:177` → FAIL C4; (b) golden + the `it('does NOT 403 …')` title reworded → FAIL C4 (a literal); (c) golden + a semicolon deleted → FAIL C4 |
| **C4b directives (new)** | the multiset of directive comments is identical | golden + `// @ts-expect-error` inserted inside a range → FAIL C4b |
| C5 region | every changed line (difflib on tip positions) lies inside a `## Lines` range | a correct edit plus a reworded `:18` header outside the range → FAIL C5 |
| C6 must-remove | every brief `-` line is present before and absent after (D7) | old sentence kept and new sentence added (the KS-1097 D r2 false green) → FAIL C6 |
| C7 exact adds | every brief `+` line is present after, byte-exact including leading whitespace (D8 + A3i) | backticks dropped → FAIL C7; `+` line shifted by 2 spaces → FAIL C7 |

- **No A4, A6 or A7 gate.** C4 proves the token stream is unchanged, so the program, its suite results and its `tsc` result cannot change. Running suites would cost minutes and prove nothing C4 has not.
- **Stated limits:**
  - C4 is lexical. A comment inside a template literal's text is literal text, so C4 catches that edit.
  - JSX text nodes are tokens, and editing them FAILs C4 (the conservative direction).

### Arms list (`tests/comment_patch_arms.sh`, real checker in a scratch clone at a pinned tip, `sandbox-exec` no-net)
- **ARM0 golden.** KS-979's brief diff → RESULT PASS, all gates, `apply_mode=strict`.
- **ARM1 old harness, the negative control.**
  - (a) `doc_patch/checker.sh` on the same golden and a doc-shaped input → FAIL. There is no `## ` section in a `.ts` file, so D4/D6 cannot hold.
  - (b) `code_patch/checker.sh` → FAIL A3 (no test file) or A4 (nothing red).
  - (c) `build_doc_input.sh` on the brief → REFUSED, no `## Required`.
- **ARM2a–c** C4 code, literal and punctuation mutants → FAIL C4.
- **ARM3** C4b directive → FAIL C4b.
- **ARM4** C5 out-of-range comment edit → FAIL C5.
- **ARM5** C6 kept-old-sentence → FAIL C6.
- **ARM6a/b** C7 paraphrase and indent shift → FAIL C7.
- **ARM7** C3 extra file → FAIL C3.
- **ARM8a/b/c** C2p MISPLACED, one-character-off and code-line stand-ins → FAIL C2 (only if C2p is built). **ARM8d** a correct stand-in on KS-1118 `:740` (em dash) → PASS with the restore named.
- **ARM9 mutation kill.** A checker copy with C4 short-circuited PASSes ARM2a, so the gate is proven load-bearing. Same for C4b with ARM3 and C5 with ARM4.
- **ARM10 builder refusals.**
  - R4: a range that includes `:175` (the `it(` line) → REFUSED.
  - R6: a non-ASCII `+` → REFUSED.
  - R8: a brief whose own diff edits a literal → REFUSED.
  - R9: a range within 10 lines of a READY hunk (READY_KS-910 on `pre_push_hook_base.test.sh` is a real fixture, but that file is `.sh`, so R1 refuses it first). Use a synthetic READY fixture.
- **ARM11 JS parity.** The same C4 mutant on a `.mjs` file (`scripts/audit/lock-discovery.mjs`) → FAIL C4.
- **Regression.** `doc_d9_blank_arms.sh` 10/10, `doc_anchor_restore_arms.sh` 10/10 and `newfile_header_arms.sh` 6/6 re-run unchanged. They should be byte-identical, since no shared file is edited.

### First 3 tickets it unlocks (brief-writer's notes, measured at `efaaa6034`)
1. **KS-979** (P-, Low, unassigned)
   - **File:** `Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-org-bind.test.ts`. 200 lines, a jest test file, but C4 means no suite runs.
   - **Range:** `:171-174`, a 4-line `//` comment above an `it(`.
   - **Fix:** the ticket spells both corrections. Cite `:109` for its own reason ("has no Organisation to validate against … would attribute to ANY matching tenant user"), keep the "different org" phrasing for `:136`, and say NOT NULL is dropped on the column, with the admin endpoint as the migration's reason.
   - **Why small:** 4 lines, no decision ("a two-line comment sweep with no decision in it"), and it closes the ticket.
   - **Watch:** `:172` carries an em dash. Either keep `:172` as context or use C2p.
2. **KS-1118 F-3** (two inputs: `KS-1118-F3a` product, `KS-1118-F3b` test)
   - **F3a:** `services/originate/src/routes/verification.ts:739-741` (1316 lines), the why-comment above `:742`'s alias chain.
   - **F3b:** `__tests__/ks1103-verify-hash-field.test.ts:15-17` header bullet and `:203` section banner.
   - **Fix:** the replacement sentence is given verbatim in the ticket's Recommendation 2.
   - **Why small:** 3 lines + 3 lines + 1 line, and the wording is ruled by the ticket. With READY_KS-1118-F2 held (a new test file, 0 hunks in either of these files), this is the ticket's last open item.
   - **Watch:** non-ASCII in range at `:740`, `:16` and `:203` (em dashes), so C2p is likely needed. The `+` text must be ASCII (`--`).
3. **KS-1156 A.2 + A.3** (two inputs)
   - **A.2:** `services/api-gateway/src/middleware/scopes.ts:125-126` (194 lines). The docblock says OAuth-minted tokens carry the `email` label; that stopped being true at #984. Wednesday's brief spells the replacement clause (for example "…before KS-835 (#984), OAuth-minted tokens also carried `email` …").
   - **A.3:** `__tests__/ks835-oauth-token-scope-gate.test.ts:59`, "mounts eight times" → "seven". The ticket measured `requireScope(` x6 + `requireScopeOrRole(` x1.
   - **Why small:** 2 lines and 1 word. A.1, R-C1 and R-C3 stay open, so this is a partial: "Refs KS-1156".
   - **Watch:** `:127` (em dash) and `:59` (arrows) are context or in range.
4. **Queue after those:**
   - **KS-1120 F-3:** ks1020 header `:29-31` + `pgModel` docblock `:190-193`, one file. Wednesday picks "reword".
   - **KS-1179 F-4 + the F-5 docblock half:** `ssrf-guard.ts:421-425`, `:519-523`, `:460-461`. The runtime deadline string stays out.
   - **KS-1180 P-1005-3:** after READY_KS-1073 / READY_KS-1185-F1 merge.

### Effort
- **1 agent-session:**
  - builder: about 150 lines, mostly a copy of `build_doc_input.sh`
  - checker: D0–D2/D7/D8 copied, plus C4/C4b/C5
  - `token_equiv.cjs`: about 60 lines
  - `task.md`
  - arms ARM0–7 and 9–11, with the ARM1 old-harness controls
- **+0.5 session** for C2p. That is `a3b_proxy.py` generalised from must-change `-` sites to context lines, gated on all-trivia tip lines, with ARM8.
- **Estimate basis:** comparable single-gate widenings today took one session each:
  - a3b_line: 19 arms
  - a3i: 11 arms
  - the doc D9 blank-anchor gate: 10 arms

### Runner-up, for the next dry pool: `suite_patch` (not specified in full here)
- **Gates:**
  - S4: the patched suite is green at the tip, and no existing cell name is lost unless the brief renames it.
  - S5: under a brief-declared MUTATION (a one-line product tamper, a planted fixture file, or an environment fault such as an unwritable path or a PATH shim), the PATCHED suite goes red by assertion on the declared cells.
  - S6: the ORIGINAL suite stays green under the same mutation. This is the discriminating pair, and it proves the defect.
- **Unlocks:** KS-906, KS-1159, KS-897 (after READY_KS-910) and the screened KS-1134 and KS-1137. With a Wednesday ruling on "the gate's proposal, the builder's call", it adds KS-1142, KS-1143, KS-1144, KS-1147, KS-1140 and KS-1131, though the last three also carry backslash or non-ASCII hazards.
- **Effort:** 2.5–3 sessions (bash and vitest/jest runners, three mutation kinds).

## FOUND
- **The widening that unlocks the most with the least doubt is `comment_patch`:** 5 tickets now, 1 after READYs, about 8 rounds, 1 session.
  - **Why it was refused before:** the recorded reason, "comment-only: no cell can red it" (KS-979, SET ASIDE; KS-1156 A.2/A.3, 17f; KS-1179 F-4, 17j/17m; KS-1118/KS-1120 F-3, 17m), is a grader gap, not a ticket defect.
  - **Why doc_patch cannot take it:** it measures sections by markdown `## ` headings (`doc_patch/checker.sh:10`), and it has no gate that stops a code change inside a changed line.
- **Suite-as-subject is a close second:** 5 measured, about 11 with rulings, 2.5–3 sessions.
- **Two product files looks large and unlocks 1.** 27 recorded tickets name it, but 24 of them also carry a decision, a diagnosis, an owner or a partition.
- **The "no cell can red it" class runs through the held gate follow-ups.** KS-1180 P-1005-3, reword the `:353` marker, is not covered by READY_KS-1180-P1P2P4. A search that treats a ticket with a held READY as fully held will keep missing these residues.
- **Non-ASCII is endemic in this repo's comments.** Every one of the first 3 tickets has an em dash or arrow inside or beside its range.
  - The doc_patch READY diffs, which carry the model's hunks with some normalised, show the model reproducing non-ASCII in context lines in 10 of 13 and in `-` lines in 6 of 13.
  - KS-839 and KS-1180-P1 show it failing on code and test-title lines.
  - Hence C2p is optional, with the all-trivia restriction.
- **Side finding:** gateway `middleware/auth.ts` still differs on live heads ks-744 `fb503741a` and ks-1195 `a067d4e3e` after #1023 merged, so KS-744, KS-1208 and KS-1197 stay partitioned.

## TESTED
- **Tip:** ls-remote `efaaa6034f036dd9538ee35b189217b1d08b90a9` at 19:25:45 and 19:36:43. `cat-file -t` = commit. Source porcelain 0 at both reads and at 19:34:29.
- **Linear pool:** 328 Backlog/Todo, 14 pages, hasNextPage false, no truncated comment pages, 19:25:57. All 9 sampled tickets plus KS-1120, KS-1179 and KS-1180 are Backlog.
- **Open PRs:** 21 / 65 distinct paths, 19:26:01 (control hit #1026). 0 of the 3 comment-class sample files and 0 of the 3 suite-class files are in any open PR. The OpenAPI yaml is in #922.
- **READY hunks:** measured per file over all 120 READY diffs: 0 in the comment-class files; READY_KS-910 `@@ -46,9` in `pre_push_hook_base.test.sh`; READY_KS-1073 and READY_KS-1185-F1 in gateway `verification.ts`.
- **Seat heads:** 34 refs since 09-16 12:00. The three-dot + blob compare finds changes only to gateway `auth.ts` (2 branches) and gateway `verification.ts` (7 branches) among the 14 files checked.
  - A first pass without the three-dot filter flagged stale-base branches (for example ks-1211-bump-colord on `auth.ts`). It was discarded as a false positive and re-run.
- **Tip line reads:** `git show` / `git grep` at `efaaa6034` for every cited range above, with non-ASCII counted per range.
- **Classification:** `scratchpad/hw/classify.py`, 148 rows → 144 tickets, any/sole tallies as tabled.
- **Pool-wide type census:** `screen.py`, path regex resolved against `ls-tree` at `efaaa6034`, 3836 paths. Positive control: KS-979 is found by the comment-wording screen.

## HOW
- **Scripts** (scratchpad `…/scratchpad/hw/`):
  - `pool.py` and `gh_prs.py`: copies of 17n's `poolfull.py` / `gh_prs.py`, with the output path and UA changed. Credentials are read by NAME from the Secuura `.env` inside Python and never printed. Linear is called with no Bearer prefix.
  - `tip.sh`, `tipread.sh`, `lines.sh`, `heads3.sh`: read verbs only (`ls-remote`, `cat-file`, `show`, `grep`, `for-each-ref`, `merge-base`, `rev-parse`, `diff --name-only`).
  - `screen.py`, `classify.py`.
- **Older reasons for T5 rows:** from `git show 3e68f4132:…/candidates.md` in the WEDNESDAY repo (read).
- **No `cd`**, except one call the hook refused and that was re-issued without it. No fetch, checkout or worktree on the Secuura checkout. No write outside this file.

## NOT TESTED
- **No part of `comment_patch` was built or run.** C4's scanner behaviour on JSX, decorators and template literals is reasoned from the TypeScript scanner API, not measured.
- **No model round.** The model's success on comment-only hunks with em-dash context is inferred from 13 doc_patch READY diffs, not from a `.ts` round.
- **KS-1134 and KS-1137 (suite class) and KS-1180 (comment class) were screened from their descriptions only.** Their partition was measured, but their fix shapes were not read in full. KS-1180's `:353` line was not re-located at `efaaa6034`.
- **17l's 47 title-level rows and the 86 EXCLUDED "names no product file" rows were not shape-classified.** The pool-wide type census sizes them only by cited path type.
- **The two-file T5 security rows** (KS-621, KS-625, KS-870, KS-1174, …) were never shape-read in any record, so a two-file tier's true upside there is unmeasured.
- **Live seat heads were compared only for the 14 files named above**, not for every path.
- **The effort estimates** are by analogy to today's a3b_line / a3i / D9 builds, not timed.
