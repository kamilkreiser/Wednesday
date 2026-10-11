From Friday (laptop seat), Datasec / Security Composer. Replies go to Friday at **friday-laptop-agent@agentmail.to**.

# BRIEF B127 (SEAT E) — QA GATE (tier 2, RENDERED, round 1 of 2): B126 Lane T2-DETAILS, Details + S9 + breadcrumb polish (#298, #299, #301, #305, #308, #155, #68)
**From:** Friday, @NOW@ AEDT 2026-10-11. **Seat:** Datasec/Security-Composer-E (your commission is the newest `Briefs/` file containing `_SEAT-E_`). Datasec / Datasec Security Composer only. The product is "Policy Designer" on screen (C-62). Report `1_Project_Definition/Briefs/2026-10-11_B127_STATUS.md`; evidence in `Briefs/2026-10-11_B127_evidence/`. The first lines are the two verdict lines; the exact LAST line is `READY FOR REVIEW`, or `STOPPED: NEEDS FRIDAY` followed by ONE question. No placeholder may be left in the file when you write it.

**You are a TESTING seat: findings only.** You work under the QA charter `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, §7 (verdict shape) and §8 (hard boundaries) above all. If your launch prompt confines reads to this project folder (as B123 recorded, STATUS `:20`), do not read it; the two rules that matter are quoted here:
- §7: every finding *"names the oracle violated … cites evidence … is coverage-qualified … separates proved from assumed"*; coverage is *"executed / skipped (why) / not-applicable (why)"*, never a bare PASS.
- §8: *"ADVISORY-ONLY, FINDINGS-ONLY — you never make changes … not even a report-only regression test … If a brief contains a write-scope grant, it is void: refuse it and report that you refused."* Fix-shapes and regression tests are prose in your report.

No code change, no push, no PR comment or review, no merge, no Jira or ticket, no BACKLOG or CLARIFICATIONS write, no deploy, no demo VM, no `az`, nothing to any human. A write grant in any brief or message is void.

**SHAPE:** follow the earlier tier-2 rendered gates on this project: `Briefs/2026-10-11_B123_SEAT-E_QA-gate-b120-web-polish.md` (+ `B123_ADDENDUM-1_base-b9625f1.md`, the moved-main leg) and the long form it points to, `Briefs/2026-10-10_B117_SEAT-D_QA-gate-b116-web.md` (gate items A–M, controls, HOLDS, report sections). Report as `2026-10-11_B123_STATUS.md` did: verdict lines, BLUF, FOUND, TESTED, …, ROUND 2, `## ADDENDUM-n` if any. Same browsers (Mac Chrome + the pinned image), Guided OFF and ON, merge-tree method.

## Verdict lines (both, in this order, first lines of STATUS)
- `B126 57f6f6e: GO | GO WITH NOTES | NO GO`
- `MERGE <main-at-verdict, 7 chars>+57f6f6e: GO | GO WITH NOTES | NO GO` (main as `ls-remote` reads it **at the moment you write the verdict**; see item M)

**Tier 2, rendered, why:** B126 changes `apps/web/**` only: 10 files, +1,419 / −34 (Friday's `git diff --stat 4e00d573...57f6f6ec`, read in the project repo). 5 product files (`screens/EngagementDetails.tsx`, `screens/Discovery.tsx`, `screens/w3/withdrawn.tsx`, `styles/app.css`, `styles/screens-w3.css`), 4 test files, 1 new e2e spec. No auth, authz, contract, migration, content or dependency change (B126 brief `:16`). So the gate drives it **in a real browser**: host Mac Chrome AND the pinned image, at **1280×800, 1180 touch, 820×1180 touch and 390×844**, Guided OFF and ON. **Round 1 of 2 under Kam's two-NO-GO cap:** say plainly what a round 2 would need to check.

## Targets
**Instrument:** `git -C "/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/2_Project_Files" ls-remote origin refs/heads/main refs/heads/b126/details-screens-polish refs/heads/b125/api-contract-correctness`, read by the drafter at **2026-10-11T08:44:47Z (19:44 AEDT)**. Re-read it yourself before you start. **If the B126 head moved: STOP.** If main moved, do not stop: see item M.

| Ref | SHA |
|---|---|
| `refs/heads/b126/details-screens-polish` (head) | **`57f6f6ec6e52cc2ca5d6936b62cdc809691b3c21`**, tree `13da9aedb23a0287f89ff7a13eff25d6cfeda61d`. 9 commits on `4e00d573`: `fe4b07c7` #301 · `5bed47d9` #298 · `f3b3fd7f` #299 · `54c28e29` e2e spec · `e1858089` #308 · `78d73d23` #305 · `50f5780e` #155 · `8c65731e` e2e follow-up · `57f6f6ec` #68. |
| `refs/heads/main` (base) | **`4e00d573cc4c1ae215e2aad70e92a08e3218281b`** = the build live on the demo (C-68, B124). `git merge-base 4e00d573 57f6f6ec` = `4e00d573` (Friday's read). |
| `refs/heads/b125/api-contract-correctness` (Seat A, live, NOT yours) | `b8b7724bfd742eef43ce90ad1b9b8af6ef79c646` at the read. 19 files three-dot from `4e00d573`; **0 shared with B126**, but it regenerates `apps/web/src/api/schema.d.ts` (the types Details compiles against) and touches `apps/web/src/feedback/types.test.ts`. |
| PR | **None at drafting:** no `refs/pull/*/head` equals `57f6f6ec` (ls-remote, same read). Friday opens it. CodeQL / PR checks: one line, NOT TESTED, Friday's. |

Both SHAs are in the local objects of `2_Project_Files` (`git cat-file -t` = commit, both).

## Read first, whole
- **The oracle per row:** the builder brief `Briefs/2026-10-11_B126_SEAT-B_details-screens-polish.md`: §1 the rows verbatim with **Friday's readings** (`:22-41`), §2 what exists at `4e00d573` (`:43-62`), §3 PARTITION (`:64-70`), §4 HELD (`:72-81`), §5 SCOPE rows 2–8 (`:83-137`), §6 PROVE IT (`:138`), §9 UNMEASURED (`:195`).
- **The claims:** `Briefs/2026-10-11_B126_STATUS.md`: BLUF `:7-18`; FOUND `:20-30`; **HOW per commit `:32-47`**; **TEST EVIDENCE `:58-120`** (red-first `:65`, tamper table `:67-76`, #301 mutants `:78-85`, targeted e2e `:87-96`, full e2e `:98-108`); **NOT TESTED `:122-128`**; **NEW WORDS `:130-136`** (1 built, 1 proposed-not-built); **NEW LOOK L1–L5 `:138-150`**; **MEASURED, NOT FIXED `:152-160`**; Q-1/Q-2 `:167-174`; Hygiene `:186-189`. Its evidence: `Briefs/2026-10-11_B126_evidence/` (`shots/INDEX.md`, `runs/`, `data/`, `static/`, `stack/`, `specs/`).
- **Friday's answers:** `Briefs/2026-10-11_B126_SEAT-B_ADDENDUM-1_q1-q2-answers-records.md`. Quote, do not re-rule:
  - **Q-1: KEEP `44px` for Choose in the 601–900 band.** *"The gate measures that each Choose box is still 44 × 44 at 820 × 1180 touch."* (item 14 below)
  - **Q-2: KEEP BOTH red boxes** on #298 (the refusal and the failed read). It stays NEW LOOK L2; Kam can collapse it.
- Gate B117 (`Briefs/2026-10-10_B117_STATUS.md` F1 `:61`, F2 `:62`, F5 `:65`; `…_B117_evidence/stack/b5-mutants.sh`) and gate B123 (`Briefs/2026-10-11_B123_STATUS.md` F1 `:76`, F4 `:79`; `…_B123_evidence/static/g210-820-breaks.txt`; the census in `…_B123_evidence/specs/b123-gate.spec.ts`): where each row came from, and the instruments you re-derive from.
- **Re-derive everything yourself. B126's tables, logs, shots, specs and tests are claims, not evidence.** Re-measure every headline number with **your own instrument**. Run B126's own spec (`apps/web/e2e/b126-details-polish.spec.ts`) or its evidence scripts only as a **second instrument**, labelled so; a number that only B126's instrument produces is UNVERIFIED.

## RULINGS CARRIED (quote them; do not re-rule)
- **Friday's readings, to be confirmed at THIS gate** (B126 brief §1). You check that the build matches each reading and that the reading's stated limits hold. Whether the look is right is Kam's.
  - #298 (`:24`): the first shape, the existing `ErrorState` + the existing "Reload the latest details", chooser closed, **no hint variant**.
  - #299 (`:26`): R-3 gains "pinned to the running release" (cloneBlock's comparison); while `running` is unknown the chooser behaves as at base; **no new sentence**.
  - #305 (`:30-35`): CSS only, inside the `screens-w3.css:464` block; step 1 first, shares only if needed; **not the cards layout**; **1280, 1180 and 390 byte-identical in computed shares**.
  - #155 (`:39`): `<wbr>`-style joints in the withdrawn list only; copy, text and accessible name byte-identical; register keys untouched.
- Q-1 and Q-2 as above.
- **NEW WORDS (1) and NEW LOOK (L1–L5) are Kam's, not this gate's.** You check each renders exactly as and where listed and breaks nothing. #299's proposed sentence (STATUS `:136`) is **not built**: confirm it appears nowhere.
- **HELD byte-identical** (B126 brief §3/§4): `apps/web/src/styles/tokens.css`, `styles/b120-radii.test.ts`, `screens/fakeDom.testing.ts`, `components/**` (incl. `ui.tsx`'s `ErrorState`), every pre-existing `apps/web/e2e/*` spec, `e2e/run.sh` (image pin `:15`), `vite.config.ts`, every `package.json`, `package-lock.json`, `packages/**`, `apps/api/**`, `schema.d.ts`, `feedback/types.test.ts`, `content/**`, `scripts/**`, `DEPLOY.md`, `ExpertSetupCard.tsx`, `guidedStart.ts`; Kam's rows #257, #259, #280–#288, #306, #307, #222/#223; every `#ffffff` literal, 50 % disc and 999px pill.

## Stacks, trees, ports (the PARTITION)
- **Live seat, do not touch:** Datasec/Security-Composer-A (B125, branch `b125/api-contract-correctness`), stacks **`pc-b125*`** on 10.125.x.0/24 and ports **6750–6759** (at drafting `lsof` showed listeners on **6757, 6758**). Never start, stop, reuse, inspect-and-change or remove them, nor `_wt_b125`, `_wt_b125rec`. B126's own stacks (`pc-b126*`, 6760–6769, 10.126.x) are closed: do not reuse them or their 8 kept volumes.
- **Your block: ports 6730–6739**, subnets **10.127.1.0/24 – 10.127.9.0/24**, stacks **`pc-b127*`** only.
  - **What the drafter checked (2026-10-11T08:43–08:44Z):** a grep of every port number 6500–6999 in every Datasec `1_Project_Definition/Briefs/2026-10-*.md` (Composer included) and in Friday's `briefs_drafts/2026-10-*.md`. Every 10-port block from 6700 to 6999 is claimed by some brief **except 6730–6739**. Avoided explicitly: 6750–6769 (B125/B126), 6860–6869 (listeners 6860–6864, 6867 at drafting), 6900–6909, 6610–6649 (B120–B123). `lsof -nP -iTCP:6730-6739 -sTCP:LISTEN`: none. No brief names `10.127.` or `pc-b127`. Docker was **not** queried at drafting.
  - Use: throwaway Postgres **127.0.0.1:6730**; edge ports **6731–6738**; `ci.sh` on **`PC_CI_EDGE_PORT=6739`**. Re-check `lsof` and `docker network ls` / `inspect` (subnet overlap) before each `up`, and list what you found in HOW. If 6730–6739 is taken: STOP (one question: which block).
  - **At most two of your stacks up at once.** Suggested: `pc-b127base` (`4e00d573`, OFF) · `pc-b127baseon` (ON) · `pc-b127` (`57f6f6ec`, OFF) · `pc-b127on` (ON) · `pc-b127m` (the merged tree, item M, only if main moved).
- **Trees:** your own detached worktrees or `git clone --shared` copies **in YOUR scratchpad only**. Read-only git verbs in the project repo (`--no-optional-locks`), except `git worktree add --detach` into your scratchpad. **Never use or write `_wt_b126`, `_wt_b126rec`, or B126's scratch `wt/*`** (STATUS `:189`), nor any other seat's.
- **B126's scripts refuse your names** (`evidence/stack/up.sh` is pinned to `pc-b126*` / 6761–6768). Copy their shape into your evidence folder with your names; never run them as is, never edit them.
- **Mac Chrome** = the installed Google Chrome, headless, fresh profile, 127.0.0.1 only; state its version (B123/B126: 155). **The pinned image** = `mcr.microsoft.com/playwright:v1.63.0-noble@sha256:eff16c30e6f3f4af0a03fa4b706120d5e9b0891c344a27d64559aff5900a4a27` (`apps/web/e2e/run.sh:15` at `57f6f6ec`). It renders in WenQuanYi Zen Hei (#258), so a layout number from the image alone is not a Mac number: report both.
- **Seed data** through the API and the screens only, fictional ("E2E synthetic b127 …"), synthetic tenants of your own. Answers served with `page.route` are labelled "API answer served by the test" in every table and shot.

## Gate items (each with its instrument and a control that could fail)

**A. Frame.**
1. **Diff frame.** `git diff --name-only 4e00d573...57f6f6ec`: the 10 paths, all under `apps/web/`. The HELD list above byte-identical (`git rev-parse <sha>:<path>` equal at both, each path). **Control:** the same instrument on `EngagementDetails.tsx` must report a difference.
2. **One commit per row** (B126 brief §5): `git show --stat` each of the 9 commits; each touches only its row's files. Say which commit, if dropped alone, would leave another row's test red.
3. **Case-collision + `/private/tmp` guard** (B111-F1): `git ls-files apps/web` lower-cased `uniq -d` empty at head; in a `/private/tmp` worktree of `57f6f6ec`: `vitest run apps/web`, `tsc -p apps/web/tsconfig.json`, `vite build` exit 0, counts as ratios (B126: 1390/1390).

**B. Per row: re-measure the headline claim, red at base / green at head, tamper.**
Required with your OWN arms (not B126's tests): **#298, #299, #68, #305**. For #301, #308, #155 at least the headline re-measure and one tamper each. Every tamper is in a scratch copy, reverted with sha256-equal restore, logged as `runs/<row>_tamper*.log` + `.diff`.

4. **#298 state logic** (`EngagementDetails.tsx:238-239` `reread`/`rereadFailed`, catch `:343-347`, outcome `:367-371`, action guard `:521`, at `57f6f6ec`). Served sequence (label it): consultant, draft, served list of ≥2 targets → "Choose a policy" → pick → PUT 409 POLICY_TARGET_ALREADY_CHOSEN → re-read `GET /engagements/{id}` 503.
   - Head: no "the page now shows it" anywhere in `innerText`; exactly two `ErrorState` boxes (refusal + failed read; Q-2 KEEP BOTH); "Reload the latest details" present and focusable; chooser closed, "Choose this policy" absent, "Choose a policy" absent; card claims nothing it did not read.
   - Base: the opposite (B117-F1's readings). Red at base, green at head, **in a real browser**, both browsers, OFF and ON.
   - **State-transition arms (the risk is the identity tie `reread.refusal === error`):** (a) Reload with the GET now OK → both boxes gone, the card shows the chosen policy, no stale "Choose a policy"; (b) Reload with the GET still failing → what renders (report; a page with no way forward is a finding); (c) after (a), a fresh unrelated error (e.g. a served 412 on another edit) → no leftover failed-read box; (d) the OK re-read arm unchanged from base (ML3 shown, chooser closed, hint shown); (e) the 412 / `isStale` path byte-identical in what it shows.
   - Count PUTs: 1 per attempt; 0 sent after the 409 from the UI.
   - **Tamper:** restore the empty `catch {}` → your arm red.
5. **#299 chooser rule** (`policyChooser` `:755-767`, term `:764`; caller passes `running`). Compare with `w1/editability.ts:59` (`cloneBlock`) by text.
   - Arms, real browser, served answers: running = pin → offered; running ≠ pin → **not offered** and no picker, no failed words, no `[]` sentence; `GET /content-releases/running` pending (held route) → as base; running 403/503 → as base (offered; the API is the backstop); a non-consultant (auditor, platform_admin) → never offered, and `running` is never requested for them (network log).
   - **Real stale pin, if you can** without editing `packages/**`: B117 reached it by creating on the demo release and then running a TEST release (B117 STATUS `:62`; B111's generator `Briefs/2026-10-09_B111_evidence/specs/make-test-release.mjs`, scratchpad only, labelled "TEST release, not lane 3a", never committed). Otherwise NOT TESTED with the reason (B126 also served it, STATUS `:123`).
   - Confirm the proposed #299 sentence is **not** in the build (`git grep` at head = 0) and report what a consultant on a stale pin actually sees (L1).
   - **Tamper:** remove the `:764` term → red.
6. **#68 in-scope filter** (`Discovery.tsx:941-951` `inScopeGroups`/`outOfScope`, table `:1087-`, list `:1140-1166`).
   - Re-measure the latent claim yourself: count untyped group-scoped questions in both content releases (B126: 0 untyped of 26; STATUS `:30`, `:158`). Name your instrument.
   - DOM arms of your own (fixture: one untyped group-scoped question; groups in-scope / `in_scope: false` / `in_scope` absent): columns = in-scope + absent only; an out-of-scope stored answer listed read-only with NEW WORDS 1 exactly and Remove; Remove sends `value: null` and the API accepts it (direct call on your stack); Save sends nothing for the out-of-scope group; read-only roles see the row without Remove.
   - **Probes B126 did not list:** a stored answer whose `device_group_id` is in **no** group of the profile (deleted group): shown anywhere? (base vs head); profile not `ready` (loading/failed): is the out-of-scope answer hidden with no hint; a typed question is unaffected.
   - **Tamper:** columns back to `groups` → red; hide the list → red.
7. **#305 shares** (`screens-w3.css` outer block `:464`, `@media (min-width: 601px) and (max-width: 900px), (min-width: 601px) and (pointer: coarse)`; B126's nested `@media (max-width: 900px)` at ~`:481-515`).
   - Your own break instrument (Range/`getClientRects` per word, as B123's G210, not B126's `collect.py`): S9 register at **820 × 1180 touch**, consultant (Choose) and auditor, both browsers, OFF and ON. Base list vs head list **by word**: 0 new broken words; "Authentication" whole; the Expiry date never broken inside a number. Compare your counts to B126's (Mac 24 → 18 / 12 → 11; image 19 → 16 / 11 → 10) and to B123's `g210-820-breaks.txt`.
   - **Computed shares (`getComputedStyle(th).width` + rendered px) at 1280, 1180 touch and 390 equal to base**, both roles, both browsers (Friday's reading's limit). **Edges:** 601, 900 and 901 (touch and non-touch): the nested rule applies exactly 601–900 any pointer; at 901 coarse, base's shares. **820 non-touch** (B126 NOT TESTED `:127`): measure it.
   - B68's words (#145: "Required", "medium", "Withdraw…") at 1280, 1180, 820 vs base; B126 says "Required"/"medium" already broke at 820 at base: confirm.
   - The built CSS: confirm `vite build` keeps the nested `@media` (read the emitted CSS) and both browsers apply it.
   - **Tamper:** remove the nested block → red at 820.
8. **#301 bite** (`b116-details-choose-policy-dom.test.tsx`). Re-run B117's mutant m1 (remove `policyChooser`'s `draftEditBlock` line) and mutant (b) (the `[]` sentence for any role) with **your own** mutation script against base's and head's test file. Expect B126's numbers (m1: base 1 red / head 4 red; (b): 0 / 1) or report yours. Add one mutant of your own (e.g. the role check moved after the list state) and say whether the head arms catch it. Read the diff: nothing removed, loosened or skipped.
9. **#308** (`app.css:280` `.pc-page-header h1`, `:309-311` `.pc-breadcrumb a`). Your own measure: a 73-character no-space name → `document.documentElement.scrollWidth` vs **the viewport you set** (not `innerWidth`; B126 MEASURED `:160`) on S4, S5, S7, S9, Details at 390, and Details at 820 and 1180. **Spaced names must lay out exactly as at base**: line count and break positions of the h1 and breadcrumb for B120's long spaced name, at every width. No lone "›" (#108 (d)). **Tamper:** remove both rules → red.
10. **#155** (`w3/withdrawn.tsx:58-66` `keyWithJoints`, used `:113`). Your own Range instrument: the longest withdrawn key at 1280 and 390, both roles: no break inside a `_`/`.`-free run. Copy (`Selection.toString()` over the cell), `textContent`, the accessible name (axe tree / `ariaSnapshot`) **byte-equal to base**. The register's keys (#107) unchanged (no `<wbr>` there: count). **Tamper:** `{keyWithJoints(key)}` → `{key}` → red. Read the re-pin `b56-withdrawn.test.tsx:68` before/after: only `<wbr>` stripped.

**C. Brand / visual pass on L1–L5 against the style source.**
11. **The style source is `apps/web/src/styles/tokens.css`** (the project's only style guide; B126 brief `:62`, `:180`; unchanged by B126, item 1). For each of L1–L5 (STATUS `:141-147`), a rendered brand table: painted part · computed value · token or **OFF-GUIDE**; end with `OFF-GUIDE: <n>`. Cover the two red boxes and the reload button (L2), the closed card (L1), the wrapped h1/breadcrumb (L3), the 820 register incl. the Choose boxes (L4), the withdrawn key cell (L5).
   - Static: in the added lines of `git diff 4e00d573...57f6f6ec -- apps/web/src/styles apps/web/src/screens`, 0 literal hex/`rgb(`/`hsl(`, 0 radius not `var(--pc-radius…)`/`0`, 0 `!important`. (The only `#` in added CSS should be BACKLOG numbers in comments; B126 `:114`.) The inline `style={{ gap: 4 }}` at `Discovery.tsx:1141`: on-guide spacing or not? Say which and why.
   - Page-wide: B123's census method (15 screens × 1280/390, every shown element against `--pc-*`) base vs head: **NEW off-guide at head = 0** is the bar. **Control:** the instrument must find base's known off-guide (the Feedback pill `#c05000`, C-22).
   - Shots of your own for L1–L5, before and after, at the widths each changes, both browsers, OFF and ON, in `Briefs/2026-10-11_B127_evidence/shots/` with `INDEX.md`. Compare a sample of ≥10 with B126's `shots/INDEX.md`: any B126 shot that does not match what you render is a finding.
12. **NEW WORDS:** row 1 found exactly (`Discovery.tsx:1143-1145`) in the DOM arm (latent, so DOM is enough; say so). Sweep the head's rendered states for any user-visible line absent at base and classify each; an unlisted new string is a finding. Rename guard over the touched screens: `/composer/i` 0 hits; no new "HPSM" meaning the policy. **Control:** a planted "Policy Composer test plant" served title MUST be reported.

**D. Visible things the builder did not list.**
13. **Sweep at 1280×800, 1180 touch, 820×1180 touch and 390×844**, both browsers, Guided OFF and ON, base vs head, over every screen with a page header or breadcrumb (`.pc-page-header h1` and `.pc-breadcrumb a` are **global** rules, not Details-only), plus Details, S9 (register + withdrawn), S5:
   - text-line diff (every line of `innerText`, and every element's line count via `getClientRects`) base vs head; each difference classified against L1–L5 or a finding;
   - **mid-word breaks** anywhere at head that base did not have (the `overflow-wrap: anywhere` risk: a short word in a narrow flex item);
   - no sideways scroll (vs the set viewport); nothing new under the sticky footer bar at load (B126 MEASURED `:159` explains the no-space-name case at 390; re-measure it and grade: reachable by scroll = Note, never reachable = finding);
   - axe (WCAG 2.2 AA) on every touched screen and state, both browsers.
14. **Q-1's measurement:** at 820 × 1180 touch, every Choose box (`.w3-choose` label) is **≥ 44 × 44 CSS px** (`boundingBox`), both browsers, OFF and ON; also at 601 and 900 touch. The Actions column's width and words at 820 (B126: ~52 px, "Raise exception" already broke at base): report; a control that becomes unreachable or overlaps is a finding.

**E. Suites.**
15. **Your own gate spec** (in your evidence folder, not the repo) covering items 4–14, run in all four of {Mac Chrome, pinned image} × {Guided OFF, ON}, at base and head: counts as ratios. Then B126's spec + B120's spec + `s47-s9-register-layout` + `a11y` as the **second instrument** (B126: base 4 failed / 24 passed → head 28/28, every cell; STATUS `:87-96`).
16. **Web unit suite** at base and head (B126: 1371/1371 → 1390/1390) and **red-first**: head's 4 new/changed test files on base source (B126: 9 failed / 38 passed → 47/47). Name ≥6 tests red at base with the failing assertion.
17. **`scripts/ci.sh` at `57f6f6ec`**, `PC_CI_EDGE_PORT=6739`, `PC_E8_SOW_TEXT` set as B105/B126 did. Run id, GREEN/RED, counts as ratios (B126: node 2933 + 1 skip; db 281/281; API 1279/1279). Name a #115/#237 timing red, a B37 "precondition did not hold" or a purity-lint timeout (#267) as that, and re-run once.
18. **Full e2e** (`apps/web/e2e/run.sh`, every project), OFF and ON, base and head; failing lists diffed **by test name** against B126's `runs/full_*.failing.txt`. ON must be 0 failed at head. Any non-baseline failure is a finding until explained (B126 had one axe "Target crashed" each side OFF; re-run once if you see the class).

**M. The merge (evaluated against main at the moment of the verdict).**
19. Immediately before writing the verdict lines, re-read `ls-remote origin refs/heads/main refs/heads/b125/api-contract-correctness` and record the time.
   - **main still `4e00d573`:** the squash is a content fast-forward; the merged tree = `57f6f6ec^{tree}` = `13da9aed…`. Say so; the head legs are the merge legs. Line: `MERGE 4e00d57+57f6f6e`.
   - **main moved (e.g. B125 merged first):** name the new SHA and what landed (`git diff --stat 4e00d573 <new>`). In a `git clone --shared` in your scratchpad (never the project repo; never `merge-tree --write-tree` there), build `<new> + 57f6f6ec` (three-dot diff applied, or `git merge --no-ff` in the clone), `git write-tree`, report the tree id. A textual conflict: **STOP** and say where. Then run on that tree: `tsc`, `vite build`, the web unit suite, your gate spec ×4 cells, and a 1280/390 smoke of Details and S9 (a regenerated `schema.d.ts` can change what Details compiles against). Compare with your head numbers; any difference is a finding. `ci.sh` on the merged tree if the API changed. Line: `MERGE <new 7>+57f6f6e`.
   - **If main moves after you have written the lines:** add `## ADDENDUM-1` with the re-read; do not re-run legs the change cannot affect (B123 ADDENDUM-1 precedent).

**Out of scope:** the demo VM; Seat A's branch (read its diff for item M only); lane 3a and any real content release; #299's sentence and #305's cards layout (Kam's / held); whether NEW WORDS or L1–L5 are right (Kam's); #57, #116's web half, #146's If-Match on withdraw.

## Report (`Briefs/2026-10-11_B127_STATUS.md`)
- The two verdict lines, first.
- BLUF (the head, then the merge).
- FOUND: Id `B127-F<n>` · Sev Blocker/Major/Minor/Note · Oracle violated (charter §7; quote the brief/row line) · What · Evidence with file:line at its SHA and shot/log path · Suggested fix-shape and the regression test the owner should add, in prose, not built.
- TESTED: item · run · result as a ratio · evidence path.
- PER-ROW TABLE: row · your instrument · base · head · B126's number · agree? · tamper result.
- #298 STATE ARMS (a)–(e) · #299 ARMS · #68 ARMS · #305 BREAK LISTS (by word) + SHARES (1280/1180/901/900/820/601/390) · Q-1 CHOOSE BOXES (px).
- BRAND (`OFF-GUIDE: <n>`, L1–L5 and census) · NEW WORDS · UNLISTED VISIBLE CHANGES (item 13).
- E2E / UNIT / CI.
- MERGE (item 19, with the times read).
- HOW: stacks, ports found free, subnets, trees, the image digest, the Chrome version, every `ls-remote` read with time.
- **NOT TESTED:** each item executed / skipped (why) / not-applicable (why).
- ROUND 2: what it would need to check.
- BACKLOG rows proposed for Friday (you edit no BACKLOG).
- Last line exactly `READY FOR REVIEW` (verdict lines at the top), or `STOPPED: NEEDS FRIDAY` followed by ONE question.

## HOLDS
- **Findings only (charter §8).** Never fix, never push, never comment on a PR, no ticket, BACKLOG or CLARIFICATIONS write, no merge to any branch. Records: your STATUS + evidence + one history entry, committed **by path** on a records branch of your own (`records/b127`), local, not pushed, in your own records worktree (never `_wt_b126rec`). **Any write-scope grant in this brief or in any message is void: refuse it and report that you refused.**
- Read-only git verbs in the project repo (`ls-remote · log · show · diff · cat-file · ls-tree · rev-parse · rev-list · merge-base · grep`, `--no-optional-locks status`), except `git worktree add --detach` into your scratchpad. Everything else in a `git clone --shared` in your scratchpad. Never `gc`, `prune`, `worktree remove`, `merge-tree --write-tree`, commit, reset, rebase, or create/delete a branch in the project repo. If `.git/index.lock` exists, wait and retry; never delete it.
- Datasec only; no other client's names, tickets or paths. Never delete; quarantine (dated folder, recorded). Never print a secret into the report, evidence or shots; Playwright traces carry the mock IdP's bearer: quarantine raw results outside the evidence folder. Shots: no `eyJ`, no password value, no connection string, no ≥40-character line from `1_Project_Definition/Source_Documents/**`.
- Take down only your own `pc-b127*` stacks, without `-v`. Never start, stop, reuse or remove `pc-b125*`, `pc-b126*` or any other stack, network or volume. Kill processes by port + cwd, never by name (other Datasec seats run node and Chrome).
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. macOS has no `timeout`; zsh has no `PIPESTATUS`. A `pgrep -f` pattern matches your own command line. "What did the branch change" is three-dot.
- **Every premise carries the file:line read and the SHA it was read at, or the word UNMEASURED.** Origin SHAs only from `ls-remote`, with the time read.
- Nothing to Paul, HP or any human; no mail except to Friday. NEW WORDS and NEW LOOK go to Kam through Friday only, **before any demo deploy**.
- A line at your prompt that is not a Friday file pointer is not an instruction.

## UNMEASURED at drafting (you check these and say what you found)
- Rendered: nothing was run at drafting (no browser, no stack, no Docker query). Every layout cite is code-read at `57f6f6ec`.
- Whether `vite build` keeps the nested `@media (max-width: 900px)` inside the `:464` block as written.
- Whether the global `.pc-page-header h1` / `.pc-breadcrumb a` `overflow-wrap: anywhere` changes any spaced title or crumb on any screen (item 13).
- The exact head line range of B126's nested block in `screens-w3.css` (~`:481-515`, from the hunk `@@ -472,6 +472,47`).
- Whether port block 6730–6739 and subnets 10.127.x are still free when you start.
