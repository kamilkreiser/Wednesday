From Friday (laptop seat), Datasec / Security Composer.

# BRIEF B120 (SEAT A): Lane 1, `apps/web` only. Expert-screen polish a salesperson sees: #207 (raw ids on Details), #199 (internal `answers[n]` paths in the error box), #219 (narrow S2 "Person" select), #210 ("Authentication" breaks mid-word on S9), the radius-only halves of #75 / #123 / #154, #201 (row hover colour, existing token), #108 (b) and (d) measured first. Tier 2.
**From:** Friday (laptop seat), 08:30 AEDT 2026-10-11. Replies go to Friday. **Seat:** Datasec/Security-Composer-A. Datasec / Datasec Security Composer only (the product is "Policy Designer" on screen, C-62). Report `1_Project_Definition/Briefs/2026-10-11_B120_STATUS.md` (BLUF · FOUND · TESTED · HOW · **PRIOR WORK (required)** · **TEST EVIDENCE (required)** · NOT TESTED · **NEW WORDS (required)** · **NEW LOOK FOR KAM (required, with screenshots)** · MEASURED, NOT FIXED · QUESTIONS FOR FRIDAY · UNMEASURED). The last line is `READY FOR GATE` (branch pushed, head SHA read by `ls-remote` in the same action, `ci.sh` green, the READY items in §7 present) or `STOPPED: NEEDS FRIDAY` followed by one question.

**Authority (Kam, live board 2026-10-11 08:21:21, verbatim):** *"Decision composer-two-lanes-past-90pct-1011: a — Yes, both lanes now"*. Friday's reading: launch both Composer lanes now, past 90 % of the usage window, under the widened EXPIRING-GRANTS row. The rows themselves are commissioned from Friday's read-only screen of 2026-10-11 (`FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-11_composer_screen_actionable.md` §2 Lane 1). **Nothing here is a Kam words-or-look decision.** His look at the NEW WORDS and the NEW LOOK comes BEFORE any demo deploy (#251 precedent). This brief deploys nothing.

**Base.** Composer origin main = **`a3502002df54a44ae5063458862796076115766c`** (Friday read it from the GitHub API; it is the build LIVE on the demo, C-67, `Briefs/2026-10-10_B119_STATUS.md:1,12`). **The local `main` checkout is stale (`0b2fca43`)**: every cite below is **(read at `a3502002`)** with `git show a3502002:<path>`, re-verified by the drafter at 2026-10-11 ~08:25 AEDT.
- **First action:** in your own worktree, `git fetch origin`, then `git -C 2_Project_Files ls-remote origin refs/heads/main`. **If it is not `a3502002…`: STOP** (`STOPPED: NEEDS FRIDAY`, with the new SHA and the time read). Do not rebase onto a moved main on your own.
- Records cites are read from the root records repo's working copy at drafting (`BACKLOG.md`, 293 lines).

**Branch** `b120/expert-screen-polish` from `a3502002`, own worktree **`/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/_wt_b120`** (absolute, outside `2_Project_Files`). At drafting neither exists: `ls -d _wt_b12*` gives no match, and `git branch -a --list '*b120*' '*b121*'` is empty.
**Tier 2:** no auth, authz, contract, migration, content or dependency change. Friday decides the gate after you.

**Running in parallel: SEAT B is LIVE** (`Datasec/Security-Composer-B`, brief `Briefs/2026-10-11_B121_SEAT-B_api-dependency-hardening.md`, Lane 2, tier 1). It owns `apps/api/**`, `package-lock.json`, every `package.json` outside `apps/web`, and, only if a bump requires, `apps/worker`, `apps/idp-mock`, `packages/service-kit`. **Those paths are NOT yours.** Its stacks are `pc-b121*` on 10.121.x.0/24 and ports 6620–6629: never start, stop, reuse or remove them. Its dependency bump will rebuild the web bundle from your same sources; that is expected and does not touch your files. MPS seats may also share the machine (Docker, CPU) but no files.

---

## 1. Why: the rows (quoted verbatim from `BACKLOG.md`; do not re-rule)
- **#207** (`BACKLOG.md:203`): *"**B79 (found, Low, pre-existing):** Details still shows raw ids in two rows (C-37): "Cloned from" prints `cloned_from_policy_version_id`, and "Current release" falls back to `current_released_version_id` while the versions list is loading, refused, or not readable by the role (`EngagementDetails.tsx`, the HPSM policy card)."* State: *"OPEN (Low). Fix-shape: "Cloned from": the source engagement's name needs it served (API change) or say "A clone"; "Current release": "Released" (or the label once read), never the id. Why deferred: #187 named only the Customer row; the first needs an API field. Discovered 2026-10-05 by B79."*
- **#199** (`BACKLOG.md:193`): *"**B75 (found, Low):** two other API detail shapes still lead with the request's internal path in the Expert error box: `answers[<n>] repeats an answer_key for the same device group.` (`apps/api/src/routes/inputs.ts:536`, no colon, so B75's strip leaves it) and the control-character / lone-surrogate refusal `answers[<n>].value contains a control character (U+007F)…` (`apps/api/src/control-characters.ts:113`; the path is the JSON path). The second is reachable from the Expert Discovery box by pasting a DEL (the web checks control characters only on sign-in)."* State: *"OPEN. Where: `components/ui.tsx` `ErrorState` (B75's strip, `/^answers\[\d+\]:\s*/`) or the API's words. Fix-shape: name the answer instead ("The answer to D-001 contains …"), which is new wording. Why deferred: B75's brief named `answers[i]:` only. Discovered 2026-10-05, B75."*
- **#219** (`BACKLOG.md:215`): *"**B86 (found, Low):** on the live S2 at 1280 the "Person (required)" select is narrow ("Choose a p…"; `live_before` and Kam's K4 context); the person's name is cut in the closed select."* State: *"OPEN. Where: `screens/w1/ApproversTable.tsx` column widths (`styles/screens-w1.css`). Why deferred: not in Kam's words; a column-share change wants its own screenshots at 1280/1180/390. Discovered 2026-10-06 during B86."*
- **#210** (`BACKLOG.md:206`): *"**B84 (found, Low, pre-existing):** S9's register breaks "Authentication" mid-word in the Category column ("Authentica\|tion" at 1280 in the register without the Choose column, 8 %; "Authenti\|cation" at 1180 on a touch tablet, 7 %). The column shares are B68's (#145 measured headers and pills only, not Category cell text); B84 did not change the Category share."* State: *"OPEN (Low). Where: `apps/web/src/styles/screens-w3.css` register column shares. … Why deferred: not in B84's rows; the shares are a measured layout (B68). Discovered 2026-10-05, B84."*
- **#75** (`BACKLOG.md:79`), the radius half only: *"…**Still OPEN:** `#ffffff` → a token (needs Kam's token approval); the `screens-w*.css` radii B104 listed (`Briefs/2026-10-09_B104_STATUS.md`)…"*
- **#123** (`BACKLOG.md:124`), the radius half only: *"**B52 token check:** the Expert screens carry off-guide styles from before B52 (static, at base `d22dc8e`): radii 6px / 50% / 999px and `#ffffff` literals in `screens-w1.css` (`.w1-disc`, `.w1-icon-disc`, `.w1-readonly`, `.w1-switch`, `.w1-stat`) and `screens-w2.css` (`.w2-tab`), and 6px buttons, selects and pills from `app.css`."* State: *"OPEN (Minor; design)…"*
- **#154** (`BACKLOG.md:148`): *"**B57-N2 (Low, design):** S9's withdrawn section has an 8 px frame and the page font for the setting key; the register above it has the shared 6 px frame and a monospace key. The off-guide side is the register's (#75 / #123)."* State: *"OPEN (Low). Goes with #75 / #123. B57."*
- **#201** (`BACKLOG.md:197`): *"**B74 (found, Low, design, pre-existing):** a table row under the pointer takes `#f7fafd`, a raw colour outside the token palette (`apps/web/src/styles/app.css:563-564`, `.pc-table tbody tr:hover`). …"* State: *"OPEN (Low). Fix-shape: a `--pc-` token for the row hover (or an existing surface token). Where: `app.css` …"* **This brief takes the second option only: an existing token.**
- **#108** (`BACKLOG.md:112`), halves (b) and (d) only: *"**B48 minor set (both):** … (b) the sign-in's radio dots render about 5 px; … (d) at 390 the breadcrumb wraps into four lines with lone "›"."* State: *"OPEN (Minor). (a) **KAM'S CALL** on the name. …"* **(a) and (c) are NOT yours** (§4).

**Row cites that have moved since the row was written (drafter's read at `a3502002`):** #199's `inputs.ts:536` is now **`:567`**; #201's `app.css:563-564` is now **`:579-580`**. List both under "BACKLOG changes for Friday".

## 2. What exists at a3502002 (your starting point; re-read each)
- **#207**, `apps/web/src/screens/EngagementDetails.tsx`:
  - `:607-612` "Current release": `current_released_version_id === null ? "Not released yet" : (currentRelease?.release_label ?? engagement.policy.current_released_version_id)`. The id fallback is **`:612`**. `currentRelease` is `versionList.find(…)` at `:241`.
  - `:615-616` "Cloned from": `engagement.cloned_from_policy_version_id ?? "Not a clone"`. The raw id is **`:616`**.
- **#199**, `apps/web/src/components/ui.tsx`: `ErrorState` at `:356`; the strip is **`:358`** `described.detail?.replace(/^answers\[\d+\]:\s*/, "")`. The two API shapes it misses:
  - `apps/api/src/routes/inputs.ts:567` `` `answers[${index}] repeats an answer_key for the same device group.` `` (no colon);
  - `apps/api/src/control-characters.ts:112-116`: `` `${where} contains ${found.what} (${found.character}), which cannot be stored. …` `` where `where = shown(found.path)` (`:102`), so the detail leads with `answers[<n>].value`.
  - **Both are API strings and the API is SEAT B's.** Your fix is in the web's rendering only.
- **#219**, `apps/web/src/screens/w1/ApproversTable.tsx:59` `<table className="pc-table">`, header "Person (required)" `:63`, the `<select className="w1-table-input">` at `:111-113`. `screens-w1.css:133` `.w1-table-input`. **No column width** is set for this table (the screen's grep found none; re-check).
- **#210**, `apps/web/src/styles/screens-w3.css:343-345` `.w3-register .pc-table th:nth-child(1) { width: 8%; /* Category */ }`. B68's measured shares and their rationale are the comment at `:338-342` (Status 9 %, Risk 8 %, Actions 9 %).
- **Radii (#75 / #123 / #154).** The style guide has **one** radius token: `apps/web/src/styles/tokens.css:59` `--pc-radius: 8px` (B47's token check accepts radius 0 or the guide's 8 px, `screens-w3.css:555`). Off-token radii at a3502002:
  - `screens-w1.css`: `:22` `.w1-disc` 50 %; `:34` `.w1-icon-disc` 50 %; `:60` `.w1-readonly` 6px; `:157` `.w1-switch input` 999px; `:172` (the switch knob, `::before`/`::after` block from `:166`) 50 %.
  - `screens-w2.css`: `:19` `.w2-tab` 6px; `:57` `.w2-tree-button` 4px; `:68` `.w2-count` 999px; `:206` `.w2-section-link` 6px; `:228` `.w2-section-disc` 50 %.
  - `screens-w3.css`: `:35` `.w3-check-mark` 50 %.
  - **#154:** `screens-w3.css:555-562` already brings the withdrawn list's frame to `var(--pc-radius)` above 600 px; the register's frame is the shared `.pc-table-wrap`, which B104 moved to `var(--pc-radius)` (#75's app.css half, C-65). So #154's frame half **may already be closed**: UNMEASURED.
- **#201**, `apps/web/src/styles/app.css:579-580` `.pc-table tbody tr:hover { background: #f7fafd; }`. Existing surface tokens in `tokens.css` include `--pc-page-bg` `:18`, `--pc-card-bg` `:19`, `--pc-table-header-bg` `:22`, `--pc-pill-neutral-bg` `:39`.
- **#108 (b):** the sign-in's radios are `apps/web/src/screens/SignIn.tsx:119-126` (`<input type="radio">` inside a `.pc-choice-card` label). `app.css:1255-1261` sizes radios to 20 px, but only inside `@media (max-width: 900px), (pointer: coarse)` (`:1215`; comment `:1212-1214`, "A desktop with a mouse keeps the 40 px control line"): a desktop pointer above 900 px gets the browser default. **(d):** `app.css:290-304` `.pc-breadcrumb ol { display: flex; flex-wrap: wrap; gap: 8px }` and `.pc-breadcrumb-sep`; the chevron is an aria-hidden element from `ui.tsx` `PageHeader` (`:300-301` comment).
- **`#ffffff` literals** remain in all four CSS files (e.g. `screens-w1.css:24,173,230`, `app.css:46,488`). **Not yours** (§4).
- **Style guide:** `apps/web/src/styles/tokens.css`. The app has no dark theme (B116 §2: `prefers-color-scheme|data-theme` = 0 lines); "both modes" means Guided switch ON and OFF, light only. If you find a dark theme, shoot both.

## 3. PARTITION (stated from both sides)
- **You (SEAT A, Lane 1) may edit:** `apps/web/**` only: screens, components, `w1/*`, `w2/*`, `w3/*`, styles, unit/DOM tests, e2e specs, `e2e/support/*`.
- **You must NOT edit (SEAT B's, live):** `apps/api/**`; `package-lock.json`; any `package.json` (including `apps/web/package.json`); `apps/worker/**`; `apps/idp-mock/**`; `packages/**` (including `packages/service-kit`).
- **You must NOT edit (nobody's this round):** `apps/web/src/api/schema.d.ts` (regenerated, never hand-edited); `apps/web/src/styles/tokens.css` (a token change needs Kam); `content/**`; `DEPLOY.md`; `scripts/**`; the e2e image pin in `apps/web/e2e/run.sh`.
- **SEAT B owns the API's words.** If #199 can only be fixed by changing the API's detail text, **do not**: render it better in the web, and list the API-side wish under QUESTIONS FOR FRIDAY.
- **Records:** your STATUS, `Briefs/2026-10-11_B120_evidence/` and a history entry, committed **by path** to the root records repo's local `main`. **Do not edit `BACKLOG.md` or `CLARIFICATIONS.md`.** List the changes you want under "BACKLOG changes for Friday".

## 4. HELD and EXCLUDED (do not build)
- **Every `#ffffff` literal** (#75, #123): needs Kam's token approval. **No new colour token, no `#ffffff`, no literal hex anywhere you touch.**
- **#108 (a)** (naming: KAM'S CALL) and **(c)** (Guided q71; Guided is OFF, C-50).
- **#154's font half** (monospace key vs page font) is a design choice, not a radius: measure and report, do not change.
- **Kam's words/look rows #280–#288**, **#73** (B41 change 5, KAM'S CALL), **#164** (chunk warning), **#222/#223** (left by Friday's ruling). If a change here would alter one of those strings or layouts, leave it byte-identical and say so.
- **#260/#285 HELD:** the Expert set-up card (`ExpertSetupCard.tsx`, `guidedStart.ts`) stays byte-identical.
- **No demo deploy, no VM, no `az`**; nothing to Paul or any human.

## 5. SCOPE, in this order (one commit per row, so Friday can drop one)
For every row: **WHAT** · **WHERE** · **RED FIRST** (a test that fails at `a3502002` and passes at your head; save both logs) · **TAMPER** (revert only the fix line(s) on a scratch copy, show the test goes red again, restore).

1. **Fetch and check the base** (header). Build nothing before the `ls-remote` check.
2. **#207 Details raw ids.**
   - WHAT: "Cloned from" shows "A clone" when `cloned_from_policy_version_id` is non-null (the row's own no-API option); "Current release" falls back to "Released" (the row's words) instead of the id while the versions list is loading, refused or unreadable. Never an id in either row.
   - WHERE: `EngagementDetails.tsx:612`, `:616`.
   - RED FIRST: a DOM test per state (list loading, list refused 403, list loaded with label, not released, clone, not a clone) asserting **by text** that no `policy_version_id`-shaped value appears.
   - TAMPER: restore `:612`'s id fallback → the loading/refused cells go red.
   - NEW WORDS: "A clone", "Released" (row's fix shape: source "BACKLOG #207").
3. **#199 error box paths.**
   - WHAT: `ErrorState` stops leading with `answers[<n>]` for both missed shapes (no colon; `.value` JSON path), as B75 did for the colon shape. Prefer naming the answer only if the web can do so from what it holds; otherwise drop the path and lead with a plain subject (seat's own words). The rest of the detail and the code line are unchanged. Never echo the offending character's text beyond what the API already shows.
   - WHERE: `ui.tsx:358` (or a helper beside it, unit-tested).
   - RED FIRST: unit cells for `answers[3] repeats an answer_key for the same device group.`, `answers[0].value contains a control character (U+007F), which cannot be stored. …`, B75's existing `answers[1]: …` cell (still passes), and a detail without a path (unchanged).
   - TAMPER: restore the single regex → the two new cells go red.
   - NEW WORDS: every changed rendered sentence (was → now).
4. **#219 S2 Person select.**
   - MEASURE FIRST: the closed select's `boundingBox().width` and whether the chosen person's name is clipped (`scrollWidth > clientWidth` on the select, or the rendered text), at 1280, 1180 and 390, Guided ON and OFF.
   - WHAT (only if reproduced): a column share for the approvers table that lets the closed select show a typical synthetic person's full name, scoped to that table (a className on the `<table>` in `ApproversTable.tsx` is fine), with no sideways scroll at 390 beyond what `TableScroll` already allows.
   - WHERE: `ApproversTable.tsx:59`, `screens-w1.css` (near `:133`).
   - RED FIRST: an e2e measurement asserting no clipping at 1280 and 1180; fails at base if reproduced.
   - TAMPER: remove the share → red.
5. **#210 "Authentication" on S9.**
   - MEASURE FIRST at 1280 (register without the Choose column) and 1180 touch, as B84 did: does the Category cell break inside a word? Instrument: a Range over the cell's text node, `getClientRects()` line count vs word count, or B84's own spec if it measures it.
   - WHAT (only if reproduced): a Category share (or a `hyphens`/`overflow-wrap` rule that keeps words whole) that keeps "Authentication" whole, **without** breaking B68's measured words: Status "Required", Risk "medium", Actions "Withdraw…" (#145, `:338-342`). Take the share from another column only with a measurement showing its longest word still fits.
   - WHERE: `screens-w3.css:343-345` (and siblings).
   - RED FIRST: the measurement as an e2e acceptance; plus B68's own words re-measured green.
   - TAMPER: restore 8 % → red at 1280.
6. **Radii (#75 / #123 / #154), radius half only.**
   - **FRIDAY'S NARROWING (overrides anything below that conflicts):** move ONLY the fixed off-token corner radii (`6px`, `4px`) to `var(--pc-radius)`. **Leave every `50%` disc/knob and every `999px` pill/switch/count exactly as it is.** Those are shapes, not corner sizes; turning them into rounded squares is a brand/look decision that is Kam's (his palette/brand rule), so list each one under NEW LOOK as "left as is — needs Kam's ruling on circle/pill shapes" with its selector and a screenshot, and do not change it.
   - WHAT: every off-token radius listed in §2 resolves to `var(--pc-radius)` or `0` (the guide's two accepted values). **A disc, knob or pill that becomes a rounded square is a visible shape change: it goes in NEW LOOK with before/after shots, one row per selector**, and Kam sees it before deploy. Do not invent a "round" value that is not a token.
   - #154: MEASURE FIRST the computed `border-radius` of `.w3-register .pc-table-wrap` and `.w3-withdrawn-list .pc-table-wrap` at 1280 and 390. If both are 8 px (and 0 at ≤600 px), the frame half is closed: report it under MEASURED, NOT FIXED, and fix nothing. Report the font half either way.
   - WHERE: the 11 lines in §2.
   - RED FIRST: the off-guide instrument B116 named (`…_mock/check-off-guide.cjs` / `render-mock.cjs`, B47/B110) over S2, S5 and S9 at base and head: base counts > 0 for these selectors, head 0. Plus a static test that greps the three `screens-w*.css` for `border-radius:` values outside `var(--pc-radius)`/`0`/`inherit`.
   - TAMPER: restore one selector's 6px → the static test and the instrument both flag it.
7. **#201 row hover.**
   - WHAT: `.pc-table tbody tr:hover` takes an **existing** surface token (seat's choice, with the measured contrast of `--pc-text` on it and the reason, e.g. it is distinct from the header's `--pc-table-header-bg`). NEW LOOK: a hovered-row shot before and after.
   - WHERE: `app.css:580`.
   - RED FIRST: the B74/B47 computed token check with the pointer over a row: base flags `#f7fafd`, head 0.
   - TAMPER: restore the hex → flagged.
8. **#108 (b) and (d), measure first.**
   - (b): the sign-in radio's rendered box at 1280 on a desktop pointer and at 390/1180 touch, in the pinned image AND host Mac Chrome. Fix only if a radio renders under the size its own CSS sets (or under 16 px on a desktop pointer), using sizes already in the stylesheet.
   - (d): the breadcrumb at 390 on the Expert screens B48 shot (Discovery, `63_expert_discovery_390.png`): number of lines, and whether any line holds only "›". Fix only if reproduced (e.g. keep each separator with its following item), with no sideways scroll.
   - Report each, fixed or not, under MEASURED, NOT FIXED or FOUND.

## 6. PROVE IT
- **Red first:** every behaviour test fails at `a3502002` and passes at your head; save both logs. None weakened: no assertion removed, loosened or skipped. Show before and after of every re-pinned one (`git grep` the old literal first: at least `Not a clone` and B75's strip test).
- **Layout acceptances, measured, not eyeballed** (`boundingBox` / `getComputedStyle`), at 1280×800, 1180 (touch) and 390×844, **Guided switch ON and OFF**, in the pinned image AND host Mac Chrome (B100/B101/B110 rule, #258):
  - no sideways scroll at 390;
  - nothing new under the sticky footer bar at load;
  - B68's register words (#145) still whole; S2's approvers table, S5's tree and tabs, S9's register re-shot.
- **Off-guide check:** 0 off-guide **radius** values on S2, S5, S9 and Details at head, every state you touched. Report the remaining `#ffffff` hits separately as "held, needs Kam's token approval".
- **`a11y.spec.ts` (axe) green** on every screen you touched.
- **Case-collision guard (gate B111-F1):** `git ls-files apps/web | tr '[:upper:]' '[:lower:]' | sort | uniq -d` empty at your head; a worktree of your head under `/private/tmp` (case-insensitive APFS) gives `vitest run apps/web` green, `tsc -p apps/web/tsconfig.json` RC 0 and `vite build` RC 0.
- **Rename guard:** `git grep -n -I -E "Policy Composer|\bthe Composer\b"` over files you touch: 0 new user-visible lines; no new "HPSM" meaning the policy.
- **`ci.sh` green** at the pushed head (`PC_CI_EDGE_PORT=6619`). Name any #115/#237 timing red, B37 "precondition did not hold" or purity-lint timeout as that, re-run once; do not fix them here. Set `PC_E8_SOW_TEXT` as B105 did.
- **Full e2e at base and head** (each project, switch ON and OFF), failing lists diffed (B110's instrument).
- **Every sentence explaining WHY a change works** gets a red proof, or is marked UNVERIFIED.

## 7. READY FOR GATE means
This brief is **commissioned to stop at a branch: Friday opens the PR**, so READY carries no PR number. It carries:
1. the branch name and its **head SHA read from origin by `ls-remote` in the same action** as the READY line, with the time read;
2. **TEST EVIDENCE**, ready to paste into the PR body: each suite's command, its counts as a **ratio** (`n/n passed, k skipped`, never "all"), the red-first pairs and the tamper runs;
3. **PRIOR WORK**;
4. **MEASURED, NOT FIXED**: every UNMEASURED row (#210, #219, #154, #108 b/d) with its numbers, whether fixed or not;
5. **NEW WORDS:** one table, every new or changed user-visible string: file:line · was → now · screen · source (row fix shape, or "seat's own"). Expect at least #207's two cells and #199's rendered details;
6. **NEW LOOK FOR KAM:** every changed shape or colour (each radius selector, the row hover, any column share), with **before and after screenshots** at 1280 and 390, Guided ON and OFF where the screen differs, in the image and Mac Chrome, in `Briefs/2026-10-11_B120_evidence/shots/`, plus an index file naming each shot's state.
   - **Friday shows Kam NEW WORDS + NEW LOOK + shots BEFORE any demo deploy.**

Friday opens the PR and merges it **only after CodeQL and every check are green and a QA gate** he commissions has passed.

## 8. STANDING LINES
- **Datasec GitHub CodeQL rule:** push your branch only. **Friday opens the PR.** A commit reaches main only after CodeQL has scanned it on a PR. Never push main, never bypass a check, **never dismiss an alert**: an alert is fixed in code, even in a test file. No `--no-verify`, no force push, no `--admin`.
- **Own worktree** (absolute path above) on its own branch. The worktrees share `2_Project_Files/.git`: never `gc`, `prune`, `worktree remove`, branch-delete or reset anything that is not yours. If `.git/index.lock` exists, wait and retry; never delete it.
- **Docker:** check `docker info` first. If it stops, start Docker Desktop yourself; if it will not start, STOP.
- **Own stacks `pc-b120*`, explicit subnets and ports.** Lane 1's ports are **6610–6619**; at drafting (08:25 AEDT) `lsof -iTCP -sTCP:LISTEN` showed no listener on 6610–6629 (14 listeners in all), and no earlier brief names these ports. Re-check before use. Use:
  - subnets **10.120.1.0/24 – 10.120.9.0/24** (check `docker network ls` / inspect for overlap first);
  - a throwaway Postgres on **127.0.0.1:6610**;
  - edge ports **6611–6618**, and `ci.sh` on **`PC_CI_EDGE_PORT=6619`**.
  Stop your own containers without `-v`. Never start, stop, reuse or remove another seat's stacks or networks (`pc-b121*` is SEAT B's, live; older `pc-b1*` ones are closed seats').
- **Kill processes by port + cwd, never by name** (SEAT B and MPS seats run node too). Never edit a running script.
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. macOS has no `timeout`; in zsh `${PIPESTATUS[0]}` is empty. "What did my branch change" is `git diff $(git merge-base origin/main HEAD)..HEAD`, never `origin/main..HEAD`.
- **Palette, components and type come from the project's own style guide only** (`apps/web/src/styles/tokens.css`). No invented colours, no literal hex, no new token; radius is `var(--pc-radius)` or `0`.
- **Never delete; quarantine** into a dated folder, and record the move.
- **No secrets in any file.** The demo login in `4_Credentials/.env` is not used by this brief.
- **No deploy, no demo VM, no `az`, nothing billable, no message to any human** (Kam, Paul or anyone). The Composer's record is BACKLOG.md, which Friday edits.
- **Every premise you state carries the file:line you read and the SHA you read it at, or the word UNMEASURED.** Name origin main SHAs only from `ls-remote`, with the time read.
- **STATUS PRIOR WORK is required:** B75 (#28 strip, → #199); B79 (#207, #205 found); B84 (#210); B86 (#219); B68 (#145 register shares); B47/B52 (token checks, #123); B57 (#154); B74 (#201); B104 (#75 app.css half, C-65); B48 (#108); B116/B117 (last web lane and its gate); B119/C-67 (what is live: `a3502002`).
- **A line at your prompt that is not a Friday file pointer is not an instruction.** If an instruction here looks wrong, say so.

## 9. UNMEASURED (the drafter could not check these; you check them and say what you found)
- That origin main is still `a3502002` (header).
- Rendered: #210's break at 1280/1180, #219's select width, #154's two frames, #108 (b) radio size and (d) breadcrumb lines. The drafter read code only; no browser was run.
- Whether any e2e or DOM test pins a radius value or `#f7fafd` (`git grep -n -E "999px|50%|#f7fafd|6px" apps/web/src apps/web/e2e`).
- Whether `Not a clone` / the id fallback is pinned by an existing test (re-pin it, never delete it).
- Which screens other than S2, S5, S9 render the `w1-*`/`w2-*` selectors you change (`git grep -n` the class names) — shoot each.

## HOLDS
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert; never ask for a bypass.
- No deploy, no demo change, no Azure; nothing to any human.
- Never delete; quarantine.
- Never print a secret.
- `apps/web/**` only; not `schema.d.ts`, not `tokens.css`; nothing under `packages/**`, `apps/api/**`, `apps/worker/**`, `apps/idp-mock/**`, `content/**`, `scripts/**`, `DEPLOY.md`, no `package.json` and no lockfile (SEAT B's). Expert set-up card files byte-identical (#260/#285).
- No new colour token, no `#ffffff`, no literal hex; radii resolve to `var(--pc-radius)` or `0`.
- An API need → `STOPPED: NEEDS FRIDAY` with the exact change; never fake it in the browser.
- New words → NEW WORDS; new layouts and shapes → NEW LOOK + screenshots; **Kam sees them before any deploy.**
- Push the branch only; Friday opens the PR; CodeQL alerts are fixed, never dismissed. No deploy. Never delete. No message to any human.

The last line of your STATUS is `READY FOR GATE` (with the head SHA from `ls-remote`) or `STOPPED: NEEDS FRIDAY` + one question.
