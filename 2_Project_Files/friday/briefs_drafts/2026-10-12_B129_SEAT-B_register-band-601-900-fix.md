From Friday (laptop seat), Datasec / Security Composer. Replies go to friday-laptop-agent@agentmail.to.

# BRIEF B129 (SEAT B): FIX ROUND for gate B127's Minor **B127-F1**: S9's exception register across the whole 601–900 px band (#305's share set is tuned to 820 only). Lane T2-DETAILS, `apps/web/src/styles` + one new e2e spec. Tier 2.
**From:** Friday (laptop seat), @NOW@. **Seat:** Datasec/Security-Composer-B. Datasec / Datasec Security Composer only (the product is "Policy Designer" on screen, C-62). Report `1_Project_Definition/Briefs/2026-10-12_B129_STATUS.md` (BLUF · FOUND · TESTED · HOW · **PRIOR WORK (required)** · **TEST EVIDENCE (required)** · NOT TESTED · **NEW WORDS (required)** · **NEW LOOK FOR KAM (required, with screenshots)** · MEASURED, NOT FIXED · QUESTIONS FOR FRIDAY · UNMEASURED). The last line is exactly `READY FOR QA: b129/register-band-601-900 @ <sha>` (branch pushed, head SHA read by `ls-remote` in the same action, `ci.sh` green, the READY items in §7 present) or `STOPPED: NEEDS FRIDAY` followed by ONE question.

**Round cap (say it in your BLUF):** this is **round 2 of 2** for this class under the two-NO-GO cap. Round 1 was B126 (build) / B127 (gate: GO WITH NOTES, F1 Minor). **If the gate on this round says NO GO, Friday ships what is closed and tickets the rest**; there is no round 3 for #305/F1.

**Launch (how Friday starts this seat):** `cockpit.sh launch Datasec/Security-Composer-B` → the project's `Launch_Claude.command`, which reads the pane name, sets `YOUR SEAT: B` and commissions **the newest brief whose file name contains `_SEAT-B_`** (`Launch_Claude.command:104`, read at drafting). At drafting the newest `_SEAT-B_` files in `Briefs/` were `2026-10-11_B126_SEAT-B_details-screens-polish.md` and its `…_B126_SEAT-B_ADDENDUM-1_…`; this file (dated 2026-10-12) is newer than both. **The last SEAT-B round is finished:** `Briefs/2026-10-11_B126_STATUS.md` ends `READY FOR QA: b126/details-screens-polish @ 57f6f6ec6e52cc2ca5d6936b62cdc809691b3c21`, and Friday merged it as PR #69 (`refs/pull/69/head` = `57f6f6ec…` by `ls-remote` at drafting). Two launcher FIRST ACTIONS do not fit this round and are overridden for this seat:
- `./BACKLOG.md`: the working copy is records `main` (`441fa893`), which does not hold #305 or B127-F1. Read F1 from `Briefs/2026-10-11_B127_STATUS.md` (§2 below); #305's row text is in `git show records/b124:BACKLOG.md` (`:301`).
- "the Jira ticket(s) the brief names": this brief names none (the Composer has no Jira).

**Authority:** Kam, Friday's terminal, 2026-10-11 ~11:58 (verbatim at `FRIDAY/0_Brain/daily_friday/2026-10-11.md:64`): *"…please continue on the work with HPSM poc, security composer and the MPS calculator"*. Friday's reading: keep building the Composer's agent-doable rows; B127-F1 is the open Minor on the merged #305. **Nothing here is a Kam words-or-look decision**; every changed share is a **NEW LOOK** row and **Kam sees it before any demo deploy** (#251 precedent). This brief deploys nothing.

## 0. Base, branch, worktree
- **Friday at placement: origin main has since moved to `898ec99e3bd936ebb0c255918b231919fba4442e` (PR #70 merged B125: API, contract, schema.d.ts and 4 e2e set-ups; NO styles file). Base on 898ec99; its styles are byte-equal to 72c038d (check `git diff --stat 72c038d 898ec99 -- apps/web/src/styles` = empty, else STOP).** Earlier base line: **Base:** Composer origin `main` = **`72c038d8daf619e91f9830f63babd9c12871625d`** (PR #69 squash-merged B126; Friday reports its tree as `13da9aedb23a0287f89ff7a13eff25d6cfeda61d` = `57f6f6ec^{tree}`, the tree gate B127 measured). Read by the drafter with `git -C 2_Project_Files ls-remote origin refs/heads/main` at 2026-10-12 ~00:27 AEDT = `72c038d8…`. **The local clone does not hold `72c038d8`** (`git cat-file -t` = "could not get object info"), so the tree equality is **UNMEASURED by the drafter**; `57f6f6ec` is local and its tree is `13da9aed…` (read). Every code cite below is **read at `57f6f6ec`** and holds at `72c038d8` only if the trees are equal.
- **First action:** in your own worktree, `git fetch origin`, then `git ls-remote origin refs/heads/main` and `git rev-parse 72c038d8^{tree}`. **If main is not `72c038d8…`, or its tree is not `13da9aed…`: STOP** (`STOPPED: NEEDS FRIDAY`, with what you read and the time). Do not rebase onto a moved main on your own.
- **The comparison base for broken words is `4e00d573cc4c1ae215e2aad70e92a08e3218281b`** (main before B126; the build live on the demo, C-68). "New broken word" always means: broken at your head and **whole at `4e00d573`**, at the same size, role, browser and Guided state. `72c038d8` (= B126) is the second column of every table, so the gate can see what this round changes against B126 too.
- **Branch** `b129/register-band-601-900` from `72c038d8`, own worktree **`/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/_wt_b129`** (absolute, outside `2_Project_Files`). At drafting neither exists: `ls -d _wt_b129*` = no match; `git branch -a --list '*b129*'` = 0 lines; `ls-remote origin 'refs/heads/b129*'` = 0 lines.
- **Tier 2:** CSS shares only. No auth, authz, contract, migration, content or dependency change.

**Running in parallel: SEAT F** (`Datasec/Security-Composer-F`, gate **B128** on B125, Lane T1-API, **read-only**; its ports **6540–6549**). Its records branch `records/b128` exists. Never start, stop, reuse or remove its stacks, networks or worktrees (`pc-b128*`, `_wt_b128rec`). Other Datasec seats may share the machine (Docker, CPU) but no files.

## 1. Why: B127-F1 (quoted from `Briefs/2026-10-11_B127_STATUS.md:80` @records/b127 `1ffc1989`; re-read it in full, do not re-rule)
- **Oracle violated (verbatim):** *Item 7: "the nested rule applies exactly 601–900 any pointer … 0 new broken words"; item 14: "a control that becomes unreachable or overlaps is a finding"; C-03 (tablet is a real target).*
- **What (verbatim headline):** *"#305's shares are right at 820 and wrong elsewhere in the band they apply to. The nested `@media (max-width: 900px)` (`screens-w3.css:481-515` @57f6f6ec) applies at 601–900 at any pointer, but B126 tuned and measured it at 820 only."*
- **F1's measured NEW breaks (head `57f6f6ec` vs base `4e00d573`, by word, key spans excluded; B127's `static/g305-break-lists-off.txt` and `…-off-rerun.txt`; OFF = ON record by record):**

  | Size | Mac Chrome 155 | Pinned image |
  |---|---|---|
  | 601 (touch = non-touch) | auditor "Prevention", "level"; consultant "by:", "level" | auditor "Commands", "Downgrade", "Whitelisting"; consultant "by:" |
  | 700 touch | auditor "Configuration" | auditor "@remediation", "Forgery(CSRF)", "Owner" |
  | 768 touch | auditor "Forgery(CSRF)", "Owner" | consultant "Actions" (header) |
  | 820, 820 touch | **0 new** (B126's fix) | **0 new** |
  | 900 (touch = non-touch) | consultant "Business", "Decided" | auditor "Synthetic"; consultant "Business" |
  | 901, 1180 touch, 1280, 390 | 0 new; shares equal base | 0 new; shares equal base |

- **Still broken at base AND head (not new; report, and keep if you can):** the date "2027-09-12" and "Authentication" at 601 and 700 (both browsers) and at 768 touch (Mac); "Required" (B68's #145 word) at 601–901 at base and head.
- **Actions column (consultant, rendered px, base → head):** 601 = 40 → 24; 700 = 47 → 37; **768 = 53 → 45**; 820 = 56 → 52; 900 = 62 → 62; 1180 touch 76 = 76; 1280 100 = 100.
- **"Raise exception" (44 × 61, two lines) leaves its cell at 768 touch in all 22 rows at head, both browsers** (button x 690–734 vs cell 684–729; at base 688–732 inside 682–734). At 601 and 700 it was **already outside at base** and is further outside at head (601: button 523–567, cell base 517–557 → head 517–541; 700: 616–663 vs cell …–653 at head). At 900 it fits at both. It stays on screen and clickable (the last column overhangs).
- **Evidence (B127's):** `static/g305-break-lists-{off,on,off-rerun}.txt`, `static/g305-shares-{off,on}.txt`, `data/gate_*` kinds G305 / G305BAND, shots `shots/band_{base,head}_{mac,img}_off/*_g305band_s9_{register,raise}_consultant_{601,700touch,768touch,900}_guided-off.png`.
- **F1's suggested shape (verbatim):** *"Either scope the nested rule to the width it was tuned for (e.g. 769–900), or tune the shares for the whole band with Actions ≥ its widest control (44 px + cell padding). Better still, the cards layout below ~900 px (held, Kam's). **Test:** extend `b126-details-polish.spec.ts`'s #305 test to 601, 700 touch, 768 touch and 900 for both roles: no word broken at head that base kept whole, the date and "Authentication" whole where the band claims them, and every Actions control inside its cell."* (This brief puts that test in a **new** spec; `b126-details-polish.spec.ts` is not edited, §3.)
- B127's ROUND 2 list (`B127_STATUS.md:277-285`) is what the gate on this round will check. Build to it.

## 2. What exists (read at `57f6f6ec`; re-read each at `72c038d8`)
- `apps/web/src/styles/screens-w3.css` (613 lines):
  - register cells `:320-324` (`padding: 10px 6px; overflow-wrap: anywhere`), `.pc-btn` in the register `:332-337` (wraps);
  - shares without Choose `:346-375` (Category 11 %, Setting 15 %, …), with Choose `:381-415` (Choose 4 %, Category 11 %, Setting 14 %, …, Expiry 6 %);
  - the B04 44 px block `:442` (`@media (max-width: 900px), (pointer: coarse)`: `.w3-choose` 44 × 44, register `.pc-btn` min-height 44);
  - the #188 touch block **`:464`** `@media (min-width: 601px) and (max-width: 900px), (min-width: 601px) and (pointer: coarse)` (Choose `max(44px, 6%)`, Setting 12 %, Choose padding-inline 0) and, nested in it, **B126's band rule `:475-515`** (`@media (max-width: 900px)`: no-Choose Category 14 %, Setting 14 %, Owner 7 %, Risk 7 %; Choose 44px, Category 13.5 %, Setting 13.75 %, Requested 7 %, Business justification 7 %, Expiry 7 %, Risk 7 %).
- `apps/web/src/styles/b126-register-820.test.ts`: regex-reads the `:464` block and the nested `@media (max-width: 900px)` and pins each share (4 tests; "the shares outside the band are B120's, untouched").
- `apps/web/e2e/b126-details-polish.spec.ts` (B126's; **not yours**): its #305 test at `:365-420` measures 820 touch / 1180 touch / 1280 / 390 only.
- Style guide `apps/web/src/styles/tokens.css`: not your path. No dark theme exists: "both modes" = Guided switch ON and OFF.

## 3. WRITE SET and PARTITION
- **You may write ONLY:**
  1. `apps/web/src/styles/screens-w3.css`: **the #305 block only** (the nested band rule at `:475-515` and, if your chosen shape needs it, its sibling selectors inside the `:464` block). Every other rule in the file byte-identical.
  2. `apps/web/src/styles/b126-register-820.test.ts`: extend it, or rename it (`git mv`, e.g. `b129-register-band.test.ts`) and extend it. Its "outside the band untouched" test stays and still passes.
  3. **ONE new e2e spec** `apps/web/e2e/b129-register-band.spec.ts` (the band measurement, §5).
  - **Nothing else.** Not `tokens.css`, not any other style or screen file, not `b126-details-polish.spec.ts` or any existing e2e spec, not `e2e/run.sh`, not `components/**`, `packages/**`, `apps/api/**`, `content/**`, `scripts/**`, `DEPLOY.md`, any `package.json` or the lockfile. A need outside this set → `STOPPED: NEEDS FRIDAY`.
- **Evidence-only instruments** (not committed to the repo) live in `Briefs/2026-10-12_B129_evidence/`.
- **Records:** your STATUS, `Briefs/2026-10-12_B129_evidence/` and one history entry, committed **by path** on a local, unpushed records branch **`records/b129` based on `records/b127` (`1ffc19899411df59e785f7ef01e2320e1f18ca39`, which contains `records/b126`)**, in your own records worktree `_wt_b129rec`. **Do not edit `BACKLOG.md` or `CLARIFICATIONS.md`**; list wanted changes under "BACKLOG changes for Friday".

## 4. HELD (do not build)
- **The cards layout below ~900 px** (#305's third shape; Kam's).
- Any change to computed shares at **1280, 1180 (touch), 901 (touch and not) or 390**.
- Any change to words, colours, tokens, radii, type or the 44 px rules (`:442`). No new token, no literal hex, no `!important`.
- `overflow-wrap` on the register's cells stays `anywhere` (`:323`) unless your measured shape needs a narrower override inside the band block; say so and measure it.
- B127-F2…F9 (other rows; not this round). No demo deploy, no VM, no `az`; nothing to any human.

## 5. SCOPE
**THE BAR (all of it, across the WHOLE 601–900 band):**
- **Sample sizes (minimum):** **601, 640, 700, 768, 820, 850, 900**, each **touch and non-touch** (hasTouch true/false; the band rule applies at any pointer), **both browsers** (pinned image AND host Mac Chrome; B100/B101/B110 rule, #258), **Guided ON and OFF**, **consultant (Choose column) and auditor (no Choose)**. That is 7 × 2 × 2 × 2 × 2 = 112 measured states. Add any width where your sweep shows a cliff.
- **0 new broken words** at every sampled state, against `4e00d573` (§0), key spans excluded as B123/B127 did.
- **(Friday at placement: the bar is NO NEW overflow vs base `4e00d573` at each state; overflows already present at base, e.g. "Raise exception" at 601/700, are measured and listed, and fixing them is a bonus, not the bar.)** **No cell text overflowing its cell**: for every register `td`/`th`, every child's (text Range and control) bounding box inside the cell's box (± 0.5 px), including "Raise exception", "Decide…" and the Setting link. **Note:** at 601 and 700 "Raise exception" already overflows at base (§1), so this is stricter than base there; that is the bar Friday sets. If it is the one item that cannot be met, it is the STOP case below, with numbers.
- **Keep everything B126 fixed at 820** (touch and non-touch, both browsers, both roles): the date "2027-09-12" whole (never broken inside a number) and "Authentication" whole; B126's "gone" words (Mac consultant "@remediation", "Configuration", "Forgery(CSRF)", "Expiry") stay whole.
- **Computed shares at 1280, 1180 touch, 390, 901 and 901 touch EQUAL to base** (`4e00d573`), both roles, both browsers (`getComputedStyle(th).width` per column, and rendered px).
- **Every Choose box 44 × 44** (#188) at every touch size in the band and at 1180 touch / 390 (`boundingBox` of every `.w3-choose` label, 22 rows).
- **Palette/tokens unchanged:** brand OFF-GUIDE **0** (B47/B110 instrument, or B127's GBRAND/L4 table on the register at 820 / 700 / 601), static literals: hex 0, `rgb(`/`hsl(` 0, non-token radius 0.
- **Also report (not a bar item):** where the date and "Authentication" are whole across the band at head vs base (they break at 601–768 at base; making them whole is welcome, not required), and "Required" (B68).

**Steps, in this order:**
1. **Fetch and check the base** (§0). Build nothing before it.
2. **Measure first, re-run not copied:** base `4e00d573`, B126 `72c038d8`, at every sample state: the break list by word, each column's width and its longest word's need, and the overflow list. Instruments:
   - **B126's evidence-only sweep** `Briefs/2026-10-11_B126_evidence/specs/b126-sweep-305.spec.ts` with `stack/sweep.sh` (host Mac) and `stack/sweep-img.sh` (image): it injects candidate CSS with `addStyleTag` (`bypassCSP: true`, evidence only) and prints `B126-SWEEP <json>` per candidate (column width, needs, broken words). **Copy it into your own scratchpad/evidence first** (its scripts point at B126's scratchpad and stacks `pc-b126head` / port 6762; never run them as they are, never edit the originals). It is hard-wired to `hasTouch: true` and height 1180: parameterise width, touch and height in your copy.
   - **B127's band instrument:** `Briefs/2026-10-11_B127_evidence/specs/b127-gate.spec.ts` (sizes at `:22-32`, the G305 loop `:606`, the `matchMedia` check `:640`, G305BAND shots `:976-998`) and `stack/g305-breaks.py` (by-word base vs head, key-span filter). Copy, do not edit.
3. **Pick shares with the sweep** (candidate CSS injected, nothing written to the product while sweeping). In this order of preference:
   - (a) one share set for the whole nested band rule;
   - (b) if no single set meets the bar: **more than one nested media range inside 601–900** (e.g. 601–767 / 768–900; each range inside the existing `:464` block);
   - (c) or a **`minmax()` / `clamp()`** shape on the columns that cliff (e.g. Actions `max(56px, …)`: the 44 px control + 2 × 6 px padding).
   - **State the choice and why in STATUS**, with the sweep table that ruled out the simpler shape. F1's "scope the nested rule to 769–900" is allowed only if 601–768 at head then meets the bar too (base's breaks there are not "new", but the overflow item still applies).
4. **Build it** in the #305 block only; then the static test (§3.2) and the e2e spec (§3.3).
   - Static test: pins every new share and media range; keeps "outside the band = B120's" green; **RED at `72c038d8`** for the new pins.
   - E2E spec `b129-register-band.spec.ts`: every bar item at every sample size, both roles, run in both browsers and both Guided states; for "new broken word" it carries **base's whole-word list per size/role** as a fixed expectation (from your step-2 measurement at `4e00d573`, cited to its evidence file) and fails on any word broken at head that is whole there; plus the overflow check, the 820 date/"Authentication" check, Choose 44 × 44, and the 1280/1180/390/901 shares. **Red at `72c038d8`** (F1's states) and green at head; save both logs.
5. **TAMPER:** restore B126's block (scratch copy) → your e2e goes red at 601/700/768/900 and your static test red; restore sha256-equal. Also the CSSOM tamper (delete your rule in the page) → red.
6. **STOP case.** If the bar cannot be met at all: `STOPPED: NEEDS FRIDAY` with the **measured best** candidate per shape (a)/(b)/(c), the remaining failures by size/role/browser (words and overflowing controls, with px), and the trade-off in one line each. Nothing pushed in that case unless Friday says so. (A card for Kam's eye is then Friday's call.)

## 6. PROVE IT
- **Red first:** every new test fails at `72c038d8` and passes at your head; save both logs. No assertion removed, loosened or skipped; show the before and after of any re-pinned one in the static test.
- **Measured, not eyeballed** (`boundingBox`, Range `getClientRects()`, `getComputedStyle`, `scrollWidth`), at every sample state (§5) plus **1280×800, 1180 (touch), 901, 390×844**.
- **No sideways scroll** at 390 and at every band size; **nothing new under the sticky footer bar** at load in the band (B126 footer instrument `B126_evidence/specs/b126-footer.spec.ts`).
- **B68's register words (#145)** still whole at 1280 and 1180; B120's #210/#219/#108 (d) and **B126's own spec** (`b126-details-polish.spec.ts`, #305 at 820) green at head in both browsers, both modes.
- **`a11y.spec.ts` (axe) green** on S9.
- **Case-collision guard (gate B111-F1):** `git ls-files apps/web | tr '[:upper:]' '[:lower:]' | sort | uniq -d` empty; in a worktree of your head under `/private/tmp`: `vitest run apps/web` green, `tsc -p apps/web/tsconfig.json` RC 0, `vite build` RC 0.
- **`ci.sh` green** at the pushed head (`PC_CI_EDGE_PORT=6829`, `PC_E8_SOW_TEXT` set as B105/B126 did). Name any #115/#237 timing red, B37 "precondition did not hold" or purity-lint timeout as that, and re-run once; do not fix them here.
- **Full e2e at `72c038d8` and head** (each project, Guided ON and OFF), failing lists diffed (B110's instrument).
- **Every sentence explaining WHY a share works** gets a measurement, or is marked UNVERIFIED.

## 7. READY FOR QA means
Friday opens the PR, so READY carries no PR number. It carries:
1. the branch and its **head SHA read from origin by `ls-remote` in the same action** as the READY line, with the time read;
2. **TEST EVIDENCE**, paste-ready for the PR body: each suite's command and counts as a **ratio** (`n/n passed, k skipped`, never "all"), the red-first pair, the tampers;
3. **PRIOR WORK** (required): B68 (#145 shares) and #188 (the touch set, `max(44px, 6%)`); B120 (#210) and gate B123 (F1 → #305); **B126** (#305 at 820, the nested rule, Q-1 "Choose = 44px: KEEP", ADDENDUM-1) and **gate B127** (F1 → this round; ROUND 2 list); B04 (C-03, 44 px targets);
4. **The band table:** for every sample state, base / B126 / head: broken-word count and NEW list, date and "Authentication" whole?, Actions px, overflowing controls (count, worst px), Choose box size; plus the 1280/1180/390/901 share-equality table;
5. **The shape chosen** ((a), (b) or (c)) and the sweep rows that ruled out the simpler ones;
6. **MEASURED, NOT FIXED:** base's own breaks that remain in the band (with numbers); anything the bar does not cover that you saw;
7. **NEW WORDS:** expect **none**; say so with the check you ran;
8. **NEW LOOK FOR KAM (required, with screenshots):** the S9 register **before (`72c038d8`, and `4e00d573` where it differs) and after** at **601, 700, 768 touch, 820 touch and 900**, consultant and auditor, **in the pinned image AND Mac Chrome**, Guided OFF (and ON where the screen differs), plus a "Raise exception" close-up at 768 touch; saved in `Briefs/2026-10-12_B129_evidence/shots/` with an index file naming each shot's state, tree and browser. Each row marked with the reading it rests on (#305 step 2 shares, F1's shape).
   - **Friday shows Kam NEW WORDS + NEW LOOK + shots BEFORE any demo deploy.**

Friday opens the PR and merges it **only after CodeQL and every check are green and a QA gate** he commissions has passed.

## 8. STANDING LINES
- **Datasec GitHub CodeQL rule:** **push your branch only. Friday opens the PR and merges once CodeQL and checks are green.** Never push main, never bypass a check, never dismiss an alert (fix it in code, even in a test file). No `--no-verify`, no force push, no `--admin`.
- **Own worktree** (`_wt_b129`, and `_wt_b129rec` for records) on its own branch. The worktrees share the project `.git`: never `gc`, `prune`, `worktree remove`, branch-delete or reset anything that is not yours. If `.git/index.lock` exists, wait and retry; never delete it.
- **Docker:** check `docker info` first. If it stops, start Docker Desktop yourself; if it will not start, STOP.
- **Own stacks `pc-b129*`, explicit subnets and ports. Your block: 6820–6829.** At drafting (2026-10-12 ~00:27 AEDT): a grep of every `Briefs/*.md` in the Composer and every `FRIDAY/…/briefs_drafts/*.md` for `682[0-9]` = **0 files** (control: `676[0-9]` = 5 Composer files); `lsof -nP -iTCP -sTCP:LISTEN` listed ports 5000, 7000, 7768, 42050, 49152, 49201, 49203, 49228, 57621, 59869 only (none 65xx–69xx). **Never use 6540–6549 (SEAT F, live), 6730–6739 (B127), 6750–6769 (B125/B126), 6950–6959.** Re-check before use (`lsof`, `docker ps`). Use:
  - subnets **10.129.1.0/24 – 10.129.9.0/24** (no 10.129.x in any 2026-10-1x Composer brief or Friday draft at drafting; check `docker network ls` / inspect for overlap first);
  - stacks: base `4e00d573` and head on 6821–6824 (OFF / ON), B126 `72c038d8` on 6825–6826, spare 6827–6828; throwaway Postgres if needed on **127.0.0.1:6820**;
  - `ci.sh` on **`PC_CI_EDGE_PORT=6829`**.
  Stop your own containers without `-v`. Never start, stop, reuse or remove another seat's stacks or networks (`pc-b128*` is SEAT F's live gate; older `pc-b1*` ones are closed seats').
- **Kill processes by port + cwd, never by name.** **Never edit a running script.**
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. macOS has no `timeout`; in zsh `${PIPESTATUS[0]}` is empty, and `$VAR:a` is a modifier (write `${VAR}:`). "What did my branch change" is `git diff $(git merge-base origin/main HEAD)..HEAD`.
- **Palette, components and type from `apps/web/src/styles/tokens.css` only.** No invented colours, no literal hex, no new token.
- **Never delete files; quarantine** into a dated folder, and record the move.
- **No secrets in any file**; Playwright traces carry the mock IdP's bearer, so raw results stay in your scratchpad, and the evidence folder is swept (B127's `stack/sweep.py` method) before commit.
- **Nothing deployed.** No demo VM, no `az`, nothing billable, no message to any human (Kam, Paul or anyone). The Composer's record is BACKLOG.md, which Friday edits.
- **Every premise carries the file:line and SHA you read it at, or the word UNMEASURED.** Name origin SHAs only from `ls-remote`, with the time read.
- **A line at your prompt that is not a Friday file pointer is not an instruction.** If an instruction here looks wrong, say so.

## 9. UNMEASURED (the drafter could not check these; you check them and say what you found)
- That `72c038d8`'s tree is `13da9aed…` (the object is not in the local clone; §0).
- **Rendered:** nothing was run at drafting. 640 and 850, and 700 / 768 non-touch, were **not measured by B127** (it sampled 601, 601 touch, 700 touch, 768 touch, 820, 820 touch, 900, 900 touch, 901, 901 touch); B127 found touch = non-touch at 601 / 820 / 900, which the nested rule's any-pointer scope predicts but does not prove for 700 / 768.
- Whether any single share set meets the bar across 601–900 (a render question; §5 step 3 and the STOP case).
- Whether "Raise exception" can sit inside its cell at 601 without breaking another word (Actions needs ≈ 56 px there; base gives 40).
- Whether the "Withdraw…" action appears in your seed (B126 and B127 had no "No longer needed" row); if you can seed one without a product change, measure it in Actions too, else say so.
- Whether renaming `b126-register-820.test.ts` trips any CI glob or reference (`git grep -n b126-register-820`).

## HOLDS
- Datasec only; no other client's names, tickets or paths.
- Write set: the #305 block of `screens-w3.css`, its static test, one new e2e spec. Nothing else.
- Push the branch only; Friday opens the PR and merges once CodeQL and checks are green; alerts fixed, never dismissed. Own worktree. Never edit a running script. Never delete; quarantine. Nothing deployed. No message to any human.
- No new token, no literal hex; OFF-GUIDE 0; 1280 / 1180 / 390 / 901 shares equal base; Choose 44 × 44.
- Round 2 of 2: a NO GO next ships what is closed and tickets the rest.

The last line of your STATUS (`1_Project_Definition/Briefs/2026-10-12_B129_STATUS.md`) is exactly `READY FOR QA: b129/register-band-601-900 @ <sha>` (the head SHA from `ls-remote`) or `STOPPED: NEEDS FRIDAY` + one question.
