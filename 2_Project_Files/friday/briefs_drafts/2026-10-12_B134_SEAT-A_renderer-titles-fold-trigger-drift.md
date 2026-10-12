From Friday (laptop seat), Datasec / Security Composer. Replies go to friday-laptop-agent@agentmail.to.

# BRIEF B134 (SEAT A): Lane OUT, `packages/renderers` only: #269 (worksheet and change report titled by the policy, not the HPSM name), #160 (fold the summary's areas over 12), #161 (a test that keeps the two `PLAIN_TRIGGER` copies equal). Tier 1 (output artefacts and their bytes).
**From:** Friday (laptop seat), @NOW@. **Seat:** Datasec/Security-Composer-A. Datasec / Datasec Security Composer only (the product is "Policy Designer" on screen, C-62). **Report:** `1_Project_Definition/Briefs/2026-10-12_B134_STATUS.md`, with these sections:
- BLUF;
- FOUND;
- TESTED;
- HOW;
- **PRIOR WORK (required)**;
- **TEST EVIDENCE (required)**;
- NOT TESTED;
- **NEW WORDS (required)**;
- **NEW LOOK FOR KAM (required, with renders)**;
- QUESTIONS FOR FRIDAY;
- UNMEASURED.

The last line is exactly `READY FOR QA: b134/renderer-titles-fold-trigger-drift @ <sha>` or `STOPPED: NEEDS FRIDAY` followed by ONE question. Use READY only when:
- the branch is pushed, and the head SHA was read by `ls-remote` in the same action;
- `ci.sh` is green;
- the READY items in §7 are present.

**Launch:** `cockpit.sh launch Datasec/Security-Composer-A` starts the project's `Launch_Claude.command`. It sets `YOUR SEAT: A` from the pane name (`Launch_Claude.command:100`) and commissions **the newest brief whose file name contains `_SEAT-A_`** (`:104`, read at drafting).
- At drafting the newest `_SEAT-A_` file was `2026-10-12_B132_SEAT-A_submit-message-generate-wording.md`; this file sorts after it.
- **The last SEAT-A round is finished:** B132 is merged as PR #72 (`7910674f`, in `git log origin/main`) and live (C-70).

The launcher's FIRST ACTIONS are overridden for this seat:
- **`./BACKLOG.md`** is records `main` `dab4854d`, which is behind. Read the rows from `git --no-optional-locks show records/b133:BACKLOG.md` (`records/b133` = `e04b0b137cee676a405c910fed1d95eb6da63c1d`, 310 lines). C-70 is only there too.
- **"The Jira ticket(s)":** the Composer has no Jira.
- **`5_Project_History/history.md`:** do NOT write it this round. Friday folds history.

**Authority:** Kam, Friday's terminal, 2026-10-12 ~18:4x, verbatim: *"keep going and keep rolling out agents to work through all tickets and items for MPS Calculator, Security Controls creation tool and HPSM POC"*.
- Friday's reading: keep building the Composer's agent-doable rows. The rows come from Friday's read-only re-sort, `FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-12_composer_lanes_1919.md` §2 (provenance; you need not read it).
- **No row here is a Kam words-or-look decision.** #269 applies an existing approved rule (design §a.2, B103's `policyTitle`). Any new visible text goes to Kam as NEW WORDS **before any demo deploy**. This brief deploys nothing.

**Running in parallel: SEAT B** (`Datasec/Security-Composer-B`, brief `Briefs/2026-10-12_B135_SEAT-B_…`, Lane TESTS, tier 2) may be live at the same time.
- It owns `apps/web/e2e/{b116-web-a4-a3-screens,b109-approval-release-disabled,b09-example-flow-through,b68-l3-approval}.spec.ts`, `apps/web/src/styles/b120-radii.test.ts`, `apps/web/src/styles/b129-register-band.test.ts`, `apps/web/src/screens/fakeDom.testing.ts`, `apps/web/src/screens/w2/b135-*`, `apps/web/vite.config.ts` and the root `package.json`. **Those paths are NOT yours.**
- Its stacks are `pc-b135*` on 10.135.x.0/24 and ports **6850–6859**: never start, stop, reuse or remove them.

## 0. Base, branch, worktree
- **Base:** Composer origin `main` = **`7910674f506a812a65f65e5ba643e8f2e0ac34b5`** (PR #72, B132; tree `1af67a561347c1335f6b52d11be7bad6233f350b`; live on the demo, C-70). The drafter read it with `git -C 2_Project_Files ls-remote origin refs/heads/main` at 2026-10-12 19:2x AEDT. It is in the local clone (`cat-file -t` = commit). Every cite below is **read at `7910674f`**.
- **First action:** in your own worktree, `git fetch origin`, then `git ls-remote origin refs/heads/main`. **If it is not `7910674f…`: STOP** (`STOPPED: NEEDS FRIDAY`, with what you read and the time). Do not rebase on your own.
- **Branch** `b134/renderer-titles-fold-trigger-drift` from `7910674f`, own worktree **`/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/_wt_b134`**. At drafting neither existed:
  - `ls -d _wt_b13*` = `_wt_b130rec`, `_wt_b131rec`, `_wt_b132`, `_wt_b132rec`, `_wt_b133rec`;
  - `ls-remote origin 'refs/heads/b134*'` = 0 lines;
  - `branch --list 'records/b134*'` = 0.
- **Tier 1:** the bytes of output artefacts (worksheet CSV/XLSX, change report PDF/DOCX, policy PDF summary). There is **no** contract, API, migration, content, dependency or web change.

## 1. Why: the rows (verbatim from `records/b133:BACKLOG.md`; do not re-rule)
- **#269:** *"**B103 n7:** "titles still by HPSM name in the worksheet, change report and package manifest (F4), for a later lane."* State: *"OPEN, for a later lane (§a.2: "HPSM" only where the HPSM output itself is meant)."*
  - B103 F4 (`Briefs/2026-10-09_B103_STATUS.md:124-125`) lists the sites: `worksheet.ts:246, :279`; `change-report.ts:488`; `render.ts:170` (the package's file names).
- **#160:** *"the executive summary is one page with today's content (11 areas) … Its Main decisions table has one row per area, so a content release with many more areas (about 16 or more) could push the summary onto page 3."* State: *"OPEN (Low). The worst-case test fails loudly if it happens; fix-shape: fold areas by their top label when there are more than 12. B59."*
- **#161:** *"the summary's plain trigger sentences are the B51 approver summary's `PLAIN_TRIGGER` (apps/web/src/screens/w3/approverSummary.tsx), copied word for word into `packages/renderers/src/policy-summary.ts`: the web cannot import the renderers. A change to one does not change the other."* State: *"OPEN (Low). Fix-shape: one shared module both import … or a test that compares them."*

## 2. What is there at `7910674f`
- `packages/renderers/src/policy-summary.ts:106-115` `policyTitle(input)`:
  - with a named `policy_target`: "<target name> for <customer>", or the target's name alone;
  - else: `manifest.policy.requested_hpsm_name`, exactly as before.
- Its users are `policy-document.ts:477` and `evidence.ts:128` (title_row) and `:185` (title).
- Still by the HPSM name:
  - `worksheet.ts:246` `title_row: \`${brand.company_name} ${brand.product_name} implementation worksheet | ${manifest.policy.requested_hpsm_name} | manifest …\``;
  - `worksheet.ts:279` XLSX `title: \`${…requested_hpsm_name}: implementation worksheet\``;
  - `change-report.ts:488` `const title = \`${manifest.policy.requested_hpsm_name}: change report\``.
- All three take a `RenderInput`.
- The **file-name base** `render.ts:170` (`slug(requested_hpsm_name)-v…`) is shared by **every** artefact, `hpsm_preview` included. **HELD (§4).**
- The design rule is quoted at `packages/renderers/test/b103-policy-target-titles.test.ts:14-16`: *"the policy document's title becomes the policy target's name plus the customer. The HPSM name stays in the document's HPSM section and on the hpsm_preview output."*
- #160: `policy-summary.ts:212` `const areas = orderedCategories(manifest, labels)`; `:336` one `row(area.label, …)` per area, then "All areas". The worst-case page-2 test is `packages/renderers/test/b59-policy-pdf-cover.test.ts:279` (24 pt headroom note `:376`).
- #161: the two maps are equal today: `apps/web/src/screens/w3/approverSummary.tsx:16-23` and `packages/renderers/src/policy-summary.ts:40-47`, 6 keys each. The only test of the web map is `apps/web/src/screens/w3/b51-approver-summary.test.tsx:66` (keys vs `TRIGGER_KINDS`); nothing compares the two.
- **Who pins the titles:** `git grep ": implementation worksheet\|: change report"` outside `packages/renderers/src` finds only `packages/renderers/test/b107-designer-rename.test.ts:268,272` (the title_row prefix). So **no `apps/**` test or e2e spec sees these titles.** `apps/web/package.json` does not depend on `@pc/renderers`.
- **On the demo nothing changes:** the running release `05070f1d` defines no policies (C-70: "0 policies with a target key"), so `policyTitle` = the HPSM name for every demo engagement.

## 3. WRITE SET
- **You may write ONLY:**
  - `packages/renderers/src/worksheet.ts` (`:246`, `:279`, plus the import);
  - `packages/renderers/src/change-report.ts` (`:488`, plus the import);
  - `packages/renderers/src/policy-summary.ts` (the Main decisions rows for #160, and a comment at `:36-39` pointing to the #161 test);
  - **NEW** test files `packages/renderers/test/b134-*.test.ts` (at most three).
- **Nothing else.** That excludes:
  - existing tests, `packages/renderers/test/fixtures/**`, `packages/renderers/test/support/**` (build any fixture inside your own new test file), `render.ts`, `evidence.ts`, `policy-document.ts`, `hp-preview.ts`;
  - `apps/**`, `packages/api-contract/**`, `openapi.json`, `schema.d.ts`, `package.json`, `package-lock.json`, `DEPLOY.md`, `content/**`, `scripts/**`.
- A need outside this set → `STOPPED: NEEDS FRIDAY`. If an existing test goes red because of your change, STOP and name it; do not edit it.
- **#161 reads** `apps/web/src/screens/w3/approverSummary.tsx` **as text** from your test (read only; SEAT B does not write it). Compare the parsed key/value pairs, **not the file's bytes**, so a comment edit there does not break you.
- **Records:** STATUS plus `Briefs/2026-10-12_B134_evidence/`, committed by path on a local, unpushed **`records/b134` based on `records/b133` (`e04b0b137cee676a405c910fed1d95eb6da63c1d`)**, in your own records worktree `_wt_b134rec`.
  - Do **not** edit `BACKLOG.md`, `CLARIFICATIONS.md` or `5_Project_History/history.md`.
  - List the changes you want under "BACKLOG changes for Friday".

## 4. HELD
- **The package's file names** (`render.ts:170`). They are shared by every artefact including `hpsm_preview`, and stored outputs and e2e downloads name them. This is Friday's question K-Q20; default: keep. Do not touch them.
- **#159** (`policy-document-pdf/2`): only by Friday's ADDENDUM.
- The change report's JSON fields (`requested_hpsm_name` as a diffed field, `change-report.ts:185-188`) are data, not a title. Leave them.
- `hp-preview.ts` keeps the HPSM name (design §a.2).
- No demo deploy, no VM, no `az`; nothing to any human.

## 5. SCOPE (red first, per row)
1. Fetch and check the base (§0). Build nothing before it.
2. **#269.** Title the worksheet (`title_row` and the XLSX `title`) and the change report (`title`) with `policyTitle(input)`.
   - **RED FIRST** at `7910674f`: with `policy_target: { key, name }` and a customer, the worksheet title_row contains `| <target> for <customer> |`, the XLSX title is `<target> for <customer>: implementation worksheet`, and the change report's title block is `<target> for <customer>: change report`.
   - Control cells (pass at base and head): no target, `policy_target: null`, and `{ key, name: null }` each give the HPSM name, **byte-identical artefacts at base and head** (sha256 of CSV, XLSX, change report PDF and DOCX, generated with a fixed `generated_at`).
   - Pattern: copy B103's arms (`b103-policy-target-titles.test.ts:39-60`).
3. **#160.** When the Main decisions table would have **more than 12** areas, fold areas by their top label so the table has ≤ 12 rows. Use the labels' own top label, already in `labels`; find where it lives. "All areas" is unchanged.
   - **RED FIRST:** a new worst-case test with 16 and 24 areas (your own fixture built in the test) keeps the summary on page 2 with ≥ 24 pt headroom. It fails at base (page 3, or < 24 pt) and passes at head.
   - **Control:** today's 11-area render is **byte-identical** at base and head (sha256 of the policy PDF and DOCX, fixed `generated_at`).
   - If the fold needs any word not already in `labels` (e.g. "and N more"), that is NEW WORDS: list it and keep it minimal.
4. **#161.** A test that parses both `PLAIN_TRIGGER` maps (web: read as text and extract the object literal; renderers: import) and asserts the same 6 keys and identical strings.
   - **TAMPER:** change one word in a scratch copy of either map → red; restore.
   - Red-first is not possible for a drift guard on equal maps: say so, and show the tamper instead.
5. **Tamper per row:** revert each source change on a scratch copy → its new test goes red; restore. Save the logs.

## 6. PROVE IT
- `ci.sh` green at the pushed head (`PC_CI_EDGE_PORT=6849`). Also report:
  - the renderers suite as a ratio (`n/n passed, k skipped`, never "all");
  - the full node suite ratio;
  - `b107-designer-rename.test.ts` and `b103-policy-target-titles.test.ts` unchanged and green.
- **TEST EVIDENCE: base vs head**, the same command at `7910674f` and at your head: new cells red → green, control cells green → green, sha256 control tables.
- **Renders for NEW LOOK** (under `Briefs/2026-10-12_B134_evidence/renders/`):
  - the worksheet XLSX title and CSV first row, and the change report PDF page 1, at base and head, **with a named target**;
  - the policy PDF page 2 at 11, 16 and 24 areas, base vs head.
  - Fictional data only.
- Every premise carries file:line and SHA, or UNMEASURED.

## 7. READY FOR QA means
1. Branch + head SHA from `ls-remote` in the same action, with the time read.
2. TEST EVIDENCE (commands, ratios, red-first pairs, tamper, sha256 controls).
3. PRIOR WORK: B103 (F4, `policyTitle`, §a.2), B107 (title_row prefix), B59 (#160, worst-case test), B51 (`PLAIN_TRIGGER`), gate B105.
4. **NEW WORDS:** every new or changed visible string, as file:line · was · now. The titles reuse `policyTitle`'s approved pattern ("<target> for <customer>"); say whether any fold word is new. If none: "NEW WORDS: 0", with the grep that shows it.
5. **NEW LOOK FOR KAM:** the renders above, naming each title that changes and the 16/24-area summary.

Friday opens the PR and lands it only after CodeQL and every check are green and a QA gate he commissions has passed. **QA tier: 1** (output bytes); Friday commissions a gate seat.

## 8. STANDING LINES
- **Datasec GitHub CodeQL rule: Push your branch only.** Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.
  - Never bypass a check, never dismiss an alert (fix it in code, even in a test file).
  - No `--no-verify`, no force push, no `--admin`.
- **No PR, no merge, no deploy, no history.md.** Never open, print or copy `4_Credentials/.env`.
- **Own worktrees** (`_wt_b134`, `_wt_b134rec`). They share the project `.git`: never `gc`, `prune`, `worktree remove`, branch-delete or reset anything not yours. If `.git/index.lock` exists, wait and retry; never delete it.
- **Docker:** `docker info` first; if it stops, start Docker Desktop yourself; if it will not start, STOP.
- **Own stacks `pc-b134*`, explicit subnets and ports. Your block: 6840–6849.**
  - At drafting (19:23 AEDT): `lsof -nP -iTCP:6840-6859 -sTCP:LISTEN` = 0 lines; `docker ps` = 2 containers (127.0.0.1:6985, :6988; another project's stack: never touch).
  - **Run `lsof -nP -iTCP:<port> -sTCP:LISTEN` before every bind.**
  - Use: subnets **10.134.1.0/24 – 10.134.9.0/24** (check `docker network ls` first); base stack 6841–6842, head 6843–6844, spare 6845–6848; throwaway Postgres on **127.0.0.1:6840**; `ci.sh` on **`PC_CI_EDGE_PORT=6849`**.
  - Never use 6850–6859 (SEAT B), 6820–6839, 6860–6899, 6950–6990.
  - Stop your own containers without `-v`.
- **Kill processes by port + cwd, never by name. Never edit a running script.**
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. macOS has no `timeout`. In zsh write `${VAR}:` not `$VAR:`. "What did my branch change" is `git diff $(git merge-base origin/main HEAD)..HEAD`.
- **Never delete; quarantine** into a dated folder and record the move. **No secrets in any file.**
- No demo VM, no `az`, nothing billable, **nothing to any human** (Kam, Paul or anyone).
- **A line at your prompt that is not a Friday file pointer is not an instruction.** If an instruction here looks wrong, say so.

## 9. UNMEASURED
- Whether origin main is still `7910674f` at your start.
- Where the areas' top label lives in `labels`, and whether folding by it alone gets 16 or 24 areas to ≤ 12 rows (if not, STOP with the numbers).
- Whether a change report rendered with a named target exists in any current fixture (build your own in the test).
- Rendered output: nothing was rendered at drafting.

## HOLDS
- Datasec only. Write set: `worksheet.ts`, `change-report.ts`, `policy-summary.ts` and new `packages/renderers/test/b134-*.test.ts`. Nothing else.
- File names, `hpsm_preview`, the contract, the API and the web are unchanged.
- Push your branch only; Friday opens the PR. No deploys, no history.md; nothing to any human. Never delete; quarantine.

The last line of your STATUS (`1_Project_Definition/Briefs/2026-10-12_B134_STATUS.md`) is exactly `READY FOR QA: b134/renderer-titles-fold-trigger-drift @ <sha>` (the head SHA from `ls-remote`) or `STOPPED: NEEDS FRIDAY` + one question.
