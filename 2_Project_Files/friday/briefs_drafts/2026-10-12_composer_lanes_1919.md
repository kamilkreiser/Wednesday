# Composer: next BUILD lanes, every open row re-classed at source (2026-10-12 19:19 AEDT)

**Project:** Datasec / Security Composer. **Drafter:** a read-only Friday subagent. Nothing was written in the project tree (read verbs only: `ls-remote`, `log`, `show`, `diff`, `cat-file`, `ls-tree`, `rev-parse`, `merge-base`, `grep`, `for-each-ref`).
**Ticket source:** `BACKLOG.md` in the project's records repo (the project root is its own local git repo with no remote; the project `CLAUDE.md` names no board, and the Composer has no Jira, `BACKLOG.md` #4). The freshest records are **`records/b133` = `e04b0b137cee676a405c910fed1d95eb6da63c1d`** (B133's C-70 deploy fold; `records/b132` is its ancestor). Records `main` is `dab4854d` and is **behind** it: the working-copy `BACKLOG.md` does not show C-70's 13 DEPLOYED rows. Rows below are from `git show records/b133:BACKLOG.md` (310 lines).
**Code read at:** Composer `main` = **`7910674f506a812a65f65e5ba643e8f2e0ac34b5`** (tree `1af67a56…`). `ls-remote origin refs/heads/main` gave this at 19:2x AEDT; the commit is in the local clone (`cat-file -t` = commit). Since the 10-11 sort's `4e00d573`: 4 commits, 34 files (B126 PR #69, B125 #70, B129 #71, B132 #72), live on the demo as C-70. Every file:line below is `git show/grep 7910674f`.
**Starting point:** `2026-10-11_composer_open_backlog_sort.md`. Every row was re-read at `records/b133`, and every code cite was re-checked at `7910674f`.

## BLUF
- **90 rows start "OPEN"** at records/b133 (101 at the 10-11 sort). Since then, 13 rows went to DEPLOYED (C-70): #68, #146, #150, #155, #177, #179, #294, #298, #299, #301, #303, #305, #308. #116 is DEPLOYED for its API half only. Three rows are new: **#312** (Kam decides), **#313** and **#314** (B130 notes).
- **17 more rows** have a state that does not start "OPEN" but still hold an open part (§6). They are counted separately.
- **Counts, 90 OPEN rows:**
  - **READY-NOW:** 21;
  - **BLOCKED-BY-FILES:** 1;
  - **NEEDS-KAM:** 53 (12 of these marked **[F]**: decision-shaped, but within Friday's own ruling power);
  - **NEEDS-CLIENT-OR-SME:** 2;
  - **DONE-ALREADY:** 13.
- **Counts, the 17 other rows:** READY-NOW 1 (#116's screen half), NEEDS-KAM 15 (5 of them [F]), NEEDS-CLIENT-OR-SME 1.
- **Overall (107 rows):** READY-NOW 22 · BLOCKED-BY-FILES 1 · NEEDS-KAM 68 (17 [F]) · NEEDS-CLIENT-OR-SME 3 · DONE-ALREADY 13.
- **Four READY-NOW lanes are file-disjoint** (§2). They are drafted for the two free panes as follows:
  - **B134 SEAT-A, Lane OUT** (renderers, tier 1): #269 titles, #160 fold, #161 drift test.
  - **B135 SEAT-B, Lane TESTS** (web test strength and build, tier 2): #302, #310, #311, #67, #212, #241, #164, #314.
  - **Lane RUNBOOK** (#293, #291, #84) and **Lane APPROVER** (#116's screen half) are disjoint from both. They are **not briefed**, for a third pane or the next round.
- **The 13 DONE-ALREADY rows are open on paper only:** #120, #202, #267, #262, #266, #268, #270, #283, #180, plus #79, #151, #222 and #235, which are closed by a ruling. Records should close them (§5).

## 1. The lane overlap check (B134 vs B135)
| | B134 SEAT-A (Lane OUT) | B135 SEAT-B (Lane TESTS) |
|---|---|---|
| **Writes** | `packages/renderers/src/worksheet.ts`, `packages/renderers/src/change-report.ts`, `packages/renderers/src/policy-summary.ts`; NEW files `packages/renderers/test/b134-*.test.ts` only | `apps/web/e2e/b116-web-a4-a3-screens.spec.ts`, `apps/web/e2e/b109-approval-release-disabled.spec.ts`, `apps/web/e2e/b09-example-flow-through.spec.ts`, `apps/web/e2e/b68-l3-approval.spec.ts`, `apps/web/src/styles/b120-radii.test.ts`, `apps/web/src/styles/b129-register-band.test.ts`, `apps/web/src/screens/fakeDom.testing.ts`, NEW `apps/web/src/screens/w2/b135-fake-dom-radio.test.tsx`, `apps/web/vite.config.ts`, root `package.json` (`typecheck` script only) |
| **Size** | 3 modified + ≤3 new = **≤6 files** | 9 modified + 1 new = **10 files** |
| **Reads only** | `apps/web/src/screens/w3/approverSummary.tsx` (#161 compares its `PLAIN_TRIGGER`) | nothing of A's |

- **Path intersection = ∅.** A is wholly under `packages/renderers/`. B is under `apps/web/` plus the root `package.json`. No path is in both columns.
- **Shared generated files:** neither lane writes `packages/api-contract/**`, `openapi.json`, `apps/web/src/api/schema.d.ts`, `package-lock.json`, `packages/renderers/test/fixtures/**` or `apps/web/e2e/support/**`. Both briefs forbid them by name. There is no contract bump, no migration and no dependency change.
- **Build coupling:** `apps/web/package.json` has no `@pc/renderers` dependency (`git show 7910674f:apps/web/package.json` names only `@pc/web`). The new titles from #269 are pinned only inside `packages/renderers/test` (`git grep ": implementation worksheet\|: change report"` outside `packages/renderers/src` = 2 hits, both `packages/renderers/test/b107-designer-rename.test.ts:268,272`, the title_row prefix only). So no `apps/**` test sees A's change.
- **A's one cross-read:** A reads `approverSummary.tsx`, which **B does not write**, and no other lane is in flight. No unmerged Composer branch exists: `ls-remote 'refs/heads/b13*'` = only `b132/…`, which is merged.
- **Ports:** A 6840–6849, B 6850–6859. `lsof -nP -iTCP:6840-6859 -sTCP:LISTEN` = 0 lines at 19:23. `docker ps` = 2 containers (6985, 6988; another project's QA stack).
- **Subnets:** A 10.134.x, B 10.135.x.

## 2. READY-NOW (22): agent-doable today
| # | Item | Evidence at 7910674f | Lane |
|---|---|---|---|
| 269 | Worksheet, change report titled by the HPSM name | `packages/renderers/src/worksheet.ts:246,279`, `change-report.ts:488` use `requested_hpsm_name`; the sibling `evidence.ts:128,185` already uses `policyTitle()` (`policy-summary.ts:106`, B103 design §a.2) | **B134 A** (titles only; the package file name `render.ts:170` is held, see K-Q20) |
| 160 | Summary may spill with 16+ areas | `policy-summary.ts:212,336`: one row per area, no fold; worst-case test `b59-policy-pdf-cover.test.ts:279` | **B134 A** |
| 161 | `PLAIN_TRIGGER` copied word for word | `apps/web/src/screens/w3/approverSummary.tsx:16-23` = `packages/renderers/src/policy-summary.ts:40-47` today; no comparison test (`git grep PLAIN_TRIGGER` finds 0 tests spanning both) | **B134 A** |
| 302 | b116 `input ≤ picker` check cannot fail | `apps/web/e2e/b116-web-a4-a3-screens.spec.ts:494` "no wider than the picker" | **B135 B** |
| 310 | b120 radii test misses the 3 app.css held shapes | `apps/web/src/styles/b120-radii.test.ts` `SHEETS` = w1/w2/w3 only; held shapes `app.css:233-236` `.pc-avatar`, `:410-413` `.pc-kpi-disc`, `:748-751` `.pc-step-disc` (50%) | **B135 B** |
| 311 | `tsc` on e2e: 2 errors, silent in CI | `apps/web/e2e/b109-approval-release-disabled.spec.ts:63` `const [hi, lo] = …sort(…)`; root `package.json:18` `typecheck` does not include `apps/web/e2e/tsconfig.json` | **B135 B** |
| 67 | b09 spec skips silently with the switch OFF | `apps/web/e2e/b09-example-flow-through.spec.ts:27` `test.skip(!seed.syntheticContent…)`; the project convention since B18/B51/B120/B126/B129 is `expect(seed.syntheticContent, "…switch ON").toBe(true)` (e.g. `b129-register-band.spec.ts:251`). So the default is clear | **B135 B** |
| 212 | b68 S9 width cell flakes one frame after a resize | `apps/web/e2e/b68-l3-approval.spec.ts:634-668` | **B135 B** |
| 241 | Fake DOM cannot choose a radio | `apps/web/src/screens/fakeDom.testing.ts`: `querySelectorAll` 0 hits | **B135 B** |
| 164 | Vite > 500 kB chunk warning | `apps/web/vite.config.ts:12` `build: { outDir: "dist", sourcemap: false }`: no `manualChunks` / `chunkSizeWarningLimit` | **B135 B** |
| 314 | b129 static test title claims tiling it does not check | `apps/web/src/styles/b129-register-band.test.ts:85` | **B135 B** |
| 293 | Two-step restore cut at a statement boundary exits 0 | `DEPLOY.md:202,206` check only `echo $?`; no "dump complete" check | Lane RUNBOOK (not briefed) |
| 291 | Route B never run on 0020 | Row's fix shape; `DEPLOY.md` "Proven on `pc-b18`" for 0019 only | Lane RUNBOOK |
| 84 | `up.sh` HEALTH RED on a fresh project | `scripts/health-check.sh:8` already has a 90 s deadline with `wait` retries (`:44-56`). The row's fix shape is stale: measure first | Lane RUNBOOK |
| 57 | Expert typed editor writes group sub-answers at engagement level (latent) | still `draftKey(answerKey, null)` `apps/web/src/screens/Discovery.tsx:200,269,712,974` | not laned (Discovery.tsx; disjoint from A/B) |
| 43 | "Asked under" pointer for multi-mapped questions | contract bump + B19 transcription, size L; NEW WORDS | not laned (the only contract lane next round) |
| 169 | `listControls` rebuilds the snapshot per load | measure first; no code change unless it shows | not laned |
| 140 | Off-guide token checker misreads `//` | records tooling `1_Project_Definition/Briefs/2026-10-03_B47_evidence/b47-check-off-guide.cjs` (exists) | Friday records lane |
| 297 | C-65 AMENDMENT overstates Route A | records wording; a dated correction | Friday records lane |
| 27 | VM deploy scripts / container names unconfirmed | read-only on the VM | next deploy seat |
| 247 | Unexplained `/opt/hpsm/524337` | read, then quarantine at the next deploy; never delete. C-70 / B133 did not touch it | next deploy seat |
| 116 (§6) | Approver summary shows no exception reason: **screen half** | API half live (`listExceptions`, C-70); 0 web callers (`git grep listExceptions 7910674f -- apps/web/src` = schema.d.ts only) | Lane APPROVER (not briefed): `apps/web/src/screens/w3/approverSummary.tsx` + its tests + a new e2e; NEW WORDS. Disjoint from A (A only reads that file; if both run, A's #161 test must pin the map, not the file's bytes) and from B |

**Why these two lanes were picked, of the four:**
- OUT and TESTS close 11 rows with no migration, no contract change and no deploy-shape change.
- RUNBOOK's #291 needs a seat stack restore cycle. It is best paired with a migration-bearing round (see K-Q8).
- APPROVER carries NEW WORDS for Kam. It is the obvious third pane if one frees.

## 3. BLOCKED-BY-FILES (1)
| # | Item | Blocked by |
|---|---|---|
| 72 | 7 comments still say `HPSM-light` | Hits at 7910674f: `apps/api/test/b20-rate-limit.db.test.ts`, `apps/web/src/markupText.test.ts`, `apps/web/src/markupText.testing.ts`, `apps/web/src/screens/w2/b20-draft-key-label.test.ts`, `packages/api-contract/src/openapi.test.ts`, `packages/content/src/b20-codeql-redos.test.ts`, **`packages/renderers/test/b20-slug.test.ts` (Lane OUT's directory)**. Also deferred by the row's own reason (the GitHub redirect). Run it as a one-commit chore after B134 merges, if K-Q12 says yes |

## 4. NEEDS-KAM (53 OPEN + 15 from §6): the question and the drafter's default
[F] = within Friday's own ruling power. The row itself names Friday as a decider, or the row is a test or design choice with no words or look in it.

| Q | Rows | Question | Default |
|---|---|---|---|
| K-Q1 | 312 | Which side is the auditor on for `generated_by.user_id`: Datasec (show it) or customer (mask it, as built in B125)? | Keep it as built (masked). It is the safer disclosure; record it as a C-entry |
| K-Q2 | 99, 182 | After release: build "Start the next draft" (API `createDraft` exists, `document.ts:1670`; 0 web callers; `Validation.tsx:121` points nowhere), or reword both places? | Build it: a consultant-only button on Details, tier 2, NEW WORDS |
| K-Q3 | 95 | No mail is ever sent, but the create form says approvers "are invited to sign in" (`CreateEngagement.tsx:640`): build notification mail, or reword? | Reword now (drop "they are invited to sign in"). Mail is a later product decision |
| K-Q4 | 129 | Ready sheet footer "Reply to the email this came with" (`ReadySheet.tsx:134`) on a sheet that no email carries: keep or reword? | Reword to "Questions before the session? Ask your Datasec contact." (NEW WORDS) |
| K-Q5 | 260, 285 | `completeExpertSetup` accepts neither key nor name (200): add the `anyOf`, which would refuse today's only UI path while the list is `[]`, or record it as accepted? | Accept as built; revisit when a release defines policies |
| K-Q6 | 172, 173 | Two clients of one name per source tenant: widen the check and lock the source tenant (contract text), or leave as specified? | Leave as specified (no demo persona has two roles) |
| K-Q7 | 131 | Past or far-future due dates: warn, refuse, or as is? | Warn on the form, no API change (NEW WORDS) |
| K-Q8 [F] | 152, 178 | Spend a migration (0022: an `audit_event` index plus a hex CHECK) on two Low rows now, or hold them for the next migration-bearing round? | Hold. Fold them into the first round that needs a migration anyway, with Lane RUNBOOK |
| K-Q9 | 35, 55, 30, 223, 226, 228, 231, 240 | Guided is OFF on the demo (C-50/C-52). Do any Guided-only rows get built while it is off? | No. Hold them all until Kam switches Guided back on |
| K-Q10 | 271 (+273), 277, 280, 281, 284, 304, 309 | Kam's words, next round per C-64/C-66/C-68 (POLICY_ALREADY_EXISTS words with the engine; the tenantless Feedback refusal; "created without one"; the `name: null` key run-on; S2's two HPSM lines; the two VERSION_NOT_EDITABLE phrasings; "A clone" / "An answer" / "answer_key") | Friday drafts one NEW WORDS card with a proposal per row. Kam rules them on one card, then one words lane builds them |
| K-Q11 | 257, 259, 286, 287, 288, 306, 307 | Kam's look, next round (pill over G01 notes; long-name breadcrumb; the step-3 tick; the 390 layout notes; "Not chosen" with no reason; approver input widths; the 5 px radio shift) | One NEW LOOK card with the gate shots. #257: accept as C-58 did. #307: the Frameworks 13 px half is agent-doable once proposed |
| K-Q12 [F] | 72 | Rename the 7 `HPSM-light` comments now (the redirect still works), or wait until the redirect is retired? | Now, as a one-commit chore after B134 merges |
| K-Q13 | 278 | Does view-source count as "users see" (77 unread "Composer" strings in the bundle, C-62)? | No; close the row |
| K-Q14 | 272, 252 | A content release that drops HPSM wording (#272) and deploys 3b+3c (#252) makes 4 demo engagements read-only: when? | After Paul's current review round (§f.2 option ii) |
| K-Q15 | 282 | A clone silently resets the E8 level to the target's: wanted? | Keep it, and add one sentence on S2 (NEW WORDS) |
| K-Q16 | 300 | A refused secret-shaped value stays in the input (and in the DOM `value`): clear it on 422? | Clear the input on `SECRET_VALUE_ENTERED_IN_CLOUD` (security; tier 2; no new words) |
| K-Q17 | 42 | Controls "Customer said" vs the generated snapshot: hint, stale marker, or as is? | The hint: "Answers changed after the documents were generated: Generate again" (NEW WORDS) |
| K-Q18 | 104 | Drop the written justification for "supplied locally" secret values (8 forms for 7 controls)? | Yes for local values only, plus one "mark all secret fields local" action |
| K-Q19 | 106 | A release signing key on Kam's demo (Evidence ZIP, JWS, manifest)? | Yes. Ops on Kam's word, at the next deploy |
| K-Q20 [F] | 269 (file-name half) | The package's download file names start with the HPSM-name slug (`render.ts:170`), shared by every artefact, the HPSM preview included. Rename them by `policyTitle`? | No. Keep file names (stored outputs and e2e downloads pin them). B134 changes titles only |
| K-Q21 [F] | 159 | A PDF-only template version `policy-document-pdf/2`? | Yes. It can join B134 by ADDENDUM (renderers only) |
| K-Q22 | 158 | The PDF cover date in UTC: add a time zone to the brand profile or the tenant? | A brand-profile time zone (en-AU, Australia/Sydney), cover only |
| K-Q23 [F] | 66, 70, 71 | Overall in-flight cap; a per-address sign-in limit; mutant B37-M2 | Leave all three as built (not measured to matter at demo scale). Close #71 as "keep" |
| K-Q24 [F] | 69 | 429 instead of 401 for an expired token under a flood | The web ends the session on that 429 when its own token clock says expired (no new words) |
| K-Q25 [F] | 157, 176 | Required properties on closed schemas (strict consumers) | No change until an external consumer exists; close as noted |
| K-Q26 [F] | 197 | The problem-code line is monospace against the one-font rule | Allow monospace for codes in the token rule (no visible change) |
| K-Q27 [F] | 246 | `draftKeyLabel` is unused | Leave it (never delete) |
| K-Q28 [F] | 313 | 0.011 px media overlap at x.99 in Chrome (no zoom reaches it) | Accept; no CSS change. B135 renames or strengthens #314's test only |
| K-Q29 | 227, 236 | Demo data for the Guided persona; the note on Paul's guide sign-in | Kam's word (demo data and the guide note are his) |
| K-Q30 | 171 | Docker address pools on Kam's laptop | Kam: raise `default-address-pools` in Docker Desktop settings, or keep per-seat explicit subnets (what the briefs do) |
| K-Q31 | 4, 41, 54, 73 (change 5), 101, 108 (a, c) | §6 rows: Jira key; PDF fonts +18 MB; C1 characters; Expert button rules; "not available" features; the product name and Guided q71 | As each row states; no seat until Kam rules |
| K-Q32 [F] | 26, 34, 154 (font half), 209 (b), 296 | §6 rows: migrate tolerates unknown migrations; prove "past B22" rollback; the withdrawn key font; combining-mark-only names; Q-2 (a)/(b) | #296 (a), the one guard arm. #209 (b): refuse names made only of combining marks. The rest: hold |

## 5. DONE-ALREADY (13): close in records
| # | Evidence at 7910674f |
|---|---|
| 120 | `apps/web/src/feedback/FeedbackWidget.tsx:341-347` returns before measuring when `querySelectorAll` / `getBoundingClientRect` are missing (#114's guard = #120's fix) |
| 202, 267 | `packages/engine/test/purity-lint.test.ts:21,26` and `w3r2-minor4-purity-lint.test.ts:24,53`: `ESLINT_TEST_TIMEOUT_MS = 660_000` |
| 266 | `DEPLOY.md:153` "## Rolling back a deploy that applied 0021" |
| 268 | `apps/web/src/feedback/types.test.ts:297` "is read from contract 0.32.0" (B125 moved it on) |
| 262 | = #266 + #268, both done |
| 270 | `apps/web/src/screens/w1/policyTarget.ts:31` `sectionTitle: "Policy"` used at `CreateEngagement.tsx:566`; `b110-create-policy-dom.test.tsx:302` asserts "HPSM Policy Details" absent |
| 283 | `apps/api/test/b103-policy-target.db.test.ts:362-367` "B113 #283: a clone … gets the running content's highest (5.9.0)" |
| 180 | `FRIDAY/2_Project_Files/friday/composer_demo_deploy.md:28` holds the #180 exception; C-70 / B133 used it ("ssh … Permission denied (publickey), exit 255 (the #180 exception)") |
| 79, 222 | Left by ruling (Kam B42 ADDENDUM-2; Friday B87 ADDENDUM-1 within C-22): nothing to build |
| 151 | "accepted by design unless Friday rules otherwise"; no ruling since |
| 235 | Friday's ruling (a), B92 ADDENDUM-2: a KNOWN LIMIT, live with the switch OFF (C-50) |

## 6. The 17 rows whose state does not start "OPEN" but hold an open part
| # | State (short) | Class |
|---|---|---|
| 4 | FOUND: Jira key PCOMP on HOLD, "Kam's call" | NEEDS-KAM (K-Q31) |
| 26 | DEFERRED (design): migrate refuses unknown recorded migrations | NEEDS-KAM [F] (K-Q32) |
| 30 | DEFERRED: Guided mid-question draft lost at sign-out | NEEDS-KAM (K-Q9) |
| 34 | DOCUMENTED, NOT PROVEN: rollback past B22 | NEEDS-KAM [F] (K-Q32) |
| 41 | MEASURED, NOT FIXED: CJK/Arabic/emoji fonts | NEEDS-KAM (K-Q31) |
| 54 | KAM'S CALL: C1 characters | NEEDS-KAM (K-Q31) |
| 55 | KAM'S CALL: Guided emptied box deletes an answer | NEEDS-KAM (K-Q9) |
| 73 | KAM'S CALL: change 5, the Expert button rules | NEEDS-KAM (K-Q31) |
| 101 | KAM'S CALL: hide unbuilt features or build two | NEEDS-KAM (K-Q31) |
| 108 | (a) name: KAM'S CALL; (c) Guided q71 | NEEDS-KAM (K-Q31 / K-Q9) |
| 116 | DEPLOYED in part; **screen half OPEN** | **READY-NOW** (Lane APPROVER) |
| 154 | Frame half closed; **font half OPEN** | NEEDS-KAM [F] (K-Q32) |
| 209 | (a) DEPLOYED; **(b) combining-mark names** | NEEDS-KAM [F] (K-Q32) |
| 249 | BLOCKED: lane 3a content needs Kam + Paul's check (C-57) | NEEDS-CLIENT-OR-SME |
| 252 | KAM'S CALL: content release deploy | NEEDS-KAM (K-Q14) |
| 273 | DEFERRED, next rounds per C-64 (= #271's build) | NEEDS-KAM (K-Q10) |
| 296 | NEEDS FRIDAY'S RULING (B113 Q-2) | NEEDS-KAM [F] (K-Q32) |

## 7. NEEDS-CLIENT-OR-SME (3)
- **#15:** Q-13 ratification of the B09 typed answers and 28 mappings (Kam + Paul, C-57).
- **#265:** `online_service_in_use` links always count (SME check, C-57).
- **#249:** lane 3a content (policy targets and E8 mappings) waits on Kam + Paul Waite's check.

## 8. Doubts and unmeasured
- **Records `main` vs `records/b133`.** The launcher tells each seat to read `./BACKLOG.md` (`Launch_Claude.command:87`), which is records `main` `dab4854d` and lacks C-70. Both briefs override this and point to `records/b133`.
- **The launcher also says to record progress in `5_Project_History/history.md`** (`Launch_Claude.command:89`). Both briefs override that: no history.md this round, per Friday's instruction. B132 and B133 did write history entries on their records branches, so this is a change of practice. Friday folds the history himself.
- **#269 scope is a reading:** "§a.2: HPSM only where the HPSM output itself is meant".
  - The drafter reads the worksheet and change report as policy artefacts, not the HPSM import file. The sibling evidence matrix already moved to `policyTitle` in B103 (`evidence.ts:128,185`).
  - `hpsm_preview` keeps the HPSM name (`b103-policy-target-titles.test.ts:14-16`).
  - If Friday reads the worksheet as the HPSM output itself, drop `worksheet.ts` from B134.
- **On the demo, #269 changes nothing visible.** The running release `05070f1d` defines no policies (C-70: "0 policies with a target key"), so `policyTitle` = `requested_hpsm_name` for every demo engagement.
- **#160's fold** only fires with more than 12 areas; today's content has 11 (`BACKLOG` #160). If the fold needs a label for a group, that label is NEW WORDS.
- **#311's CI half** adds `tsc -p apps/web/e2e/tsconfig.json` to the root `typecheck` script.
  - Whether the CI image (`docker/Dockerfile --target ci`, `--network none`) has `@playwright/test` types for `apps/web/e2e` is UNMEASURED.
  - The brief says STOP rather than add a dependency.
- **#164:** the B135 default is a vendor `manualChunks` split, no lazy routes. The bundle file names and count change, so this is a NEW LOOK for deploy checks, not for users. Whether the vendor split alone gets under 500 kB is UNMEASURED.
- Nothing was rendered, run or built. All layout and test claims are code reads.
