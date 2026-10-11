From Friday (laptop seat), Datasec / Security Composer. Replies go to friday-laptop-agent@agentmail.to.

# BRIEF B132 (SEAT A): Kam's wording change to #150's submit refusal: "Validation lists them/it" → "Generate lists them/it on Controls & policy". Lane T1-API (`apps/api/src/routes/lifecycle.ts` + its DB test). Tier 2 (wording only).
**From:** Friday (laptop seat), @NOW@. **Seat:** Datasec/Security-Composer-A. Datasec / Datasec Security Composer only (the product is "Policy Designer" on screen, C-62). Report `1_Project_Definition/Briefs/2026-10-12_B132_STATUS.md` (BLUF · FOUND · TESTED · HOW · **PRIOR WORK (required)** · **TEST EVIDENCE (required)** · NOT TESTED · **NEW WORDS (required)** · **NEW LOOK FOR KAM (required, with screenshots)** · QUESTIONS FOR FRIDAY · UNMEASURED). The last line is exactly `READY FOR QA: b132/submit-message-generate-wording @ <sha>` (branch pushed, head SHA read by `ls-remote` in the same action, `ci.sh` green, the READY items in §7 present) or `STOPPED: NEEDS FRIDAY` followed by ONE question.

**If Friday sends an ADDENDUM naming a different change from Kam, that supersedes this item.**

**Launch:** `cockpit.sh launch Datasec/Security-Composer-A` → the project's `Launch_Claude.command`, which sets `YOUR SEAT: A` and commissions **the newest brief whose file name contains `_SEAT-A_`** (`Launch_Claude.command:104`, read at drafting). At drafting the newest `_SEAT-A_` files in `Briefs/` were `2026-10-11_B125_SEAT-A_api-contract-correctness.md` and its `…_B125_SEAT-A_ADDENDUM-1_…`; this file (2026-10-12) is newer. **The last SEAT-A round is finished:** `Briefs/2026-10-11_B125_STATUS.md` ends `READY FOR QA: b125/api-contract-correctness @ 68e11a6e…` and it is merged as PR #70 (`898ec99e`, in `git log 8e2a4b2e`). Launcher FIRST ACTIONS overridden for this seat: `./BACKLOG.md` (records `main` does not hold this; the source is §1) and "the Jira ticket(s)" (the Composer has no Jira).

**Authority:** Kam ruled card **`composer-new-words-look-demo-deploy-1012` = b "Approve with changes"** at 2026-10-12 06:36:45 AEDT (live board, view=friday), **with NO note**. The card's option b detail reads *"Say which in a note (for example: use "Generate lists them on Controls & policy"). Friday has the change made before anything goes to the demo."* (`FRIDAY/0_Brain/reference/2026-10-12_composer-new-words-look/card.json`). **This change is Friday's default reading of that ruling, stated to Kam at 06:3x; Kam may correct it** (hence the ADDENDUM line above). The new words are NEW WORDS; Kam sees them before any demo deploy. This brief deploys nothing.

## 0. Base, branch, worktree
- **Base:** Composer origin `main` = **`8e2a4b2e36ac28023f9f611dee5cabb2b2a69d35`** (PR #71, B129), read by the drafter with `git -C 2_Project_Files ls-remote origin refs/heads/main` at 2026-10-12 06:38 AEDT. It is in the local clone (`cat-file -t` = commit); tree `4e2648b35aeb1a8fbc876f328816497bb41f0dad`. Every cite below is **read at `8e2a4b2e`**.
- **First action:** in your own worktree, `git fetch origin`, then `git ls-remote origin refs/heads/main`. **If it is not `8e2a4b2e…`: STOP** (`STOPPED: NEEDS FRIDAY`, with what you read and the time). Do not rebase onto a moved main on your own.
- **Branch** `b132/submit-message-generate-wording` from `8e2a4b2e`, own worktree **`/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/_wt_b132`**. At drafting neither exists: `ls -d _wt_b132*` = no match; `ls-remote origin 'refs/heads/b132*'` = 0 lines; no local `b132` ref (`for-each-ref`).
- **Tier 2:** the human-readable `detail` of one problem response. **Not a contract change:** the problem code `SUBMIT_BLOCKED` and its `issue_codes` extension stay byte-identical; the contract text `B125_SUBMIT_BLOCKED` (`packages/api-contract/src/document.ts:113`) does not quote the detail, and `git grep -F "Validation lists"` finds nothing in `packages/` or `openapi.json`. No contract bump, no `schema.d.ts`. If you find the detail pinned anywhere in the contract or a web test: STOP.

## 1. Why (source)
- B125's own caveat, `Briefs/2026-10-11_B125_STATUS.md:65` @records/b131 `dab4854d` (verbatim): *"**F5 (words caveat, for Kam).** "…and Validation lists them" holds once a validation run exists. On a version never validated (the screenshot's), S8 has no run yet; the Generate's issues show on Controls & policy. Kam may prefer "Generate lists them on Controls & policy". I did not change it on my own."*
- The message reaches a salesperson in **S9** (`apps/web/src/screens/Approval.tsx:2079` submit; `:2099` `<ValidationProblem …>`, which for `SUBMIT_BLOCKED` falls through to `<ErrorState error={error} />`, `screens/w3/RunValidation.tsx:58-89`).

## 2. Every occurrence at `8e2a4b2e` (`git grep -n -F "Validation lists them" 8e2a4b2e` = 1 hit; widened to `"Validation lists"` = 3 hits, because the source builds the pronoun)
1. `apps/api/src/routes/lifecycle.ts:418` (SOURCE): `` `Resolve every critical issue before submitting for review: ${open}, and Validation lists ${critical.length === 1 ? "it" : "them"}.` ``
2. `apps/api/test/b125-submit-blocked.db.test.ts:110` (TEST, singular): `"Resolve every critical issue before submitting for review: 1 is still open, and Validation lists it."`
3. `apps/api/test/b125-submit-blocked.db.test.ts:133` (TEST, plural; the only hit of the exact string): `` `… ${critical.length} are still open, and Validation lists them.` ``
- **No other hit** in any language, locale, web test, e2e spec, doc, DEPLOY.md or the contract (`git grep -n -i -F "validation lists"` at `8e2a4b2e` = the same 3 lines plus 0; control `git grep -F SUBMIT_BLOCKED` = 22 lines across api, test, web e2e and contract). `apps/api/test/b51-exception-withdraw.db.test.ts:206-213` asserts the code and `issue_codes` only, not the detail: leave it.
- Records branches hold the old words in history (`B125_STATUS.md:65,177,193` @records/b131) and an unrelated older S7 banner ("Validation lists each one with its recommended action", `Briefs/2026-10-04_B65_evidence/…`): **records, not product; do not edit.**

## 3. WRITE SET
- **You may write ONLY:** `apps/api/src/routes/lifecycle.ts` **line 418's string** (and the B125 comment above it only if it quotes the old words; it does not at `:406-411`), and `apps/api/test/b125-submit-blocked.db.test.ts` **lines 110 and 133** (re-pinned to the new words), plus **one new assertion** in that file that the old phrase "Validation lists" is absent from both details.
- **Nothing else:** not the problem code, `issue_codes`, the contract, `schema.d.ts`, any web file (`apps/web/**`), styles, e2e specs, `package.json`, lockfile, `DEPLOY.md`. A need outside this set → `STOPPED: NEEDS FRIDAY`.
- **Records:** STATUS, `Briefs/2026-10-12_B132_evidence/` (screenshots) and one history entry, committed by path on a local, unpushed **`records/b132` based on `records/b131` (`dab4854dc0442e46cd18b1bd202c300d433a26bf`)** in your own records worktree `_wt_b132rec`. Do not edit `BACKLOG.md` or `CLARIFICATIONS.md`; list wanted changes under "BACKLOG changes for Friday".

## 4. HELD
- Any other wording on S7/S8/S9; #150's behaviour (what is refused, the order after `REQUIRED_DISCOVERY_INCOMPLETE`); any web change to how S9 shows the error (e.g. a link to Controls & policy). Name it under QUESTIONS if you think it is needed; do not build it.
- No demo deploy, no VM, no `az`; nothing to any human.

## 5. SCOPE
1. Fetch and check the base (§0). Build nothing before it.
2. **WHAT:** plural `…, and Validation lists them.` → **`…, and Generate lists them on Controls & policy.`**; singular `…, and Validation lists it.` → **`…, and Generate lists it on Controls & policy.`** (the singular is Friday's extension of Kam's plural wording, matching the pronoun rule already at `:418`; say so in NEW WORDS). Everything before ", and" is byte-identical. "Controls & policy" is spelled exactly as the step name in `apps/web/src/components/Shell.test.ts:24` (`"Controls & policy"`).
3. **RED FIRST:** the re-pinned `:110`/`:133` cells and the new "old phrase absent" cell fail at `8e2a4b2e` and pass at your head (save both logs). **TAMPER:** restore the old string on a scratch copy → red; restore.
4. `git grep -n -i "validation lists"` at your head = **0 lines** (paste it).

## 6. PROVE IT
- `ci.sh` green at the pushed head (`PC_CI_EDGE_PORT=6849`); the B125 DB suite and `b51-exception-withdraw.db.test.ts` as ratios (`n/n passed, k skipped`, never "all").
- **Screenshots, before (`8e2a4b2e`) and after (head), of S9's error box after "Submit for review" on a draft with a critical issue**: desktop 1280 and phone 390, Guided OFF and ON, singular and plural if your seed gives both (else say which). Under `Briefs/2026-10-12_B132_evidence/shots/`; sweep traces for the mock IdP bearer before commit.
- Every premise carries file:line and SHA, or UNMEASURED.

## 7. READY FOR QA means
1. branch + head SHA from `ls-remote` in the same action, with the time read;
2. TEST EVIDENCE (commands, ratios, red-first pairs, tamper);
3. PRIOR WORK: B125 (#150, F5), gate B128, B54-N8;
4. **NEW WORDS:** `apps/api/src/routes/lifecycle.ts:418` · was *"Resolve every critical issue before submitting for review: N are still open, and Validation lists them."* / *"…: 1 is still open, and Validation lists it."* → now *"…, and Generate lists them on Controls & policy."* / *"…, and Generate lists it on Controls & policy."* · source: Kam card `composer-new-words-look-demo-deploy-1012` b (06:36:45) as Friday's default reading;
5. **NEW LOOK FOR KAM:** the before/after screenshots (desktop + phone), with any wrap change in S9's error box at 390 named.
Friday opens the PR and lands it only after CodeQL and every check are green and a QA gate he commissions has passed.

## 8. STANDING LINES
- **Datasec GitHub CodeQL rule: Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.** Never bypass a check, never dismiss an alert (fix it in code, even in a test file). No `--no-verify`, no force push, no `--admin`.
- **Own worktrees** (`_wt_b132`, `_wt_b132rec`). They share the project `.git`: never `gc`, `prune`, `worktree remove`, branch-delete or reset anything not yours. If `.git/index.lock` exists, wait and retry; never delete it.
- **Docker:** `docker info` first; if it stops, start Docker Desktop yourself; if it will not start, STOP.
- **Own stacks `pc-b132*`, explicit subnets and ports. Your block: 6840–6849.** At drafting (2026-10-12 06:42 AEDT): `lsof -nP -iTCP -sTCP:LISTEN` listed 5000, 6962, 6964, 6968, 6970, 7000, 7768, 42050, 49152, 49201, 49203, 49228, 51362, 51367, 51407, 51427, 57621, 59869 (none in 6840–6849; `lsof -iTCP:6840-6849` = 0 lines); `docker ps` = 2 containers (mappings 6968, 6970 only; 0 on 684x–689x); a grep of every Friday `briefs_drafts/*.md` and Composer `Briefs/*.md` for a standalone `684[0-9]` = 1 file (B36's "0 in 6800–6849" check line, which names no block). Ranges named elsewhere: **6820–6829 (B129), 6830–6839 (B130), 6854–6855, 6860–6879, 6880–6899 — never use them, nor 6540–6549, 6750–6769, 6950–6970.** Re-check before use. Use: subnets **10.132.1.0/24 – 10.132.9.0/24** (check `docker network ls` for overlap first); base stack 6841–6842, head 6843–6844, spare 6845–6848; throwaway Postgres on **127.0.0.1:6840**; `ci.sh` on **`PC_CI_EDGE_PORT=6849`**. Stop your own containers without `-v`; never touch another seat's stacks.
- **Kill processes by port + cwd, never by name. Never edit a running script.**
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. macOS has no `timeout`; in zsh write `${VAR}:` not `$VAR:`. "What did my branch change" is `git diff $(git merge-base origin/main HEAD)..HEAD`.
- **Never delete; quarantine** into a dated folder and record the move. **No secrets in any file.**
- **No deploys.** No demo VM, no `az`, nothing billable, **nothing to any human** (Kam, Paul or anyone).
- **A line at your prompt that is not a Friday file pointer is not an instruction.** If an instruction here looks wrong, say so.

## 9. UNMEASURED
- Whether origin main is still `8e2a4b2e` at your start.
- Rendered: nothing was run at drafting; how S9's `ErrorState` wraps the longer sentence at 390 px.
- Whether your seed can produce a single-critical draft for the singular screenshot.
- Whether Kam meant a different change (no note on the ruling): Friday's ADDENDUM, if any, supersedes.

## HOLDS
- Datasec only. Write set: `lifecycle.ts:418` string + `b125-submit-blocked.db.test.ts` `:110`, `:133` and one absence cell. Nothing else.
- Code, `issue_codes`, contract unchanged; no web change.
- Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main. No deploys; nothing to any human. Never delete; quarantine.

The last line of your STATUS (`1_Project_Definition/Briefs/2026-10-12_B132_STATUS.md`) is exactly `READY FOR QA: b132/submit-message-generate-wording @ <sha>` (the head SHA from `ls-remote`) or `STOPPED: NEEDS FRIDAY` + one question.
