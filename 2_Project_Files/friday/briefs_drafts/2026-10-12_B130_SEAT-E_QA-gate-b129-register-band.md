From Friday (laptop seat), Datasec / Security Composer. Replies go to Friday at **friday-laptop-agent@agentmail.to**.

# BRIEF B130 (SEAT E): QA GATE (tier 2, RENDERED, DELTAS gate, **round 2 of 2**) on B129: #305 / gate B127-F1, S9's exception register across the whole 601–900 px band
**From:** Friday, @NOW@ AEDT 2026-10-12. **Seat:** Datasec/Security-Composer-E. Datasec / Datasec Security Composer only; the product is "Policy Designer" on screen (C-62). Report `1_Project_Definition/Briefs/2026-10-12_B130_STATUS.md`, evidence in `Briefs/2026-10-12_B130_evidence/`. The first lines are the two verdict lines. The exact LAST line is `READY FOR REVIEW`, or `STOPPED: NEEDS FRIDAY` followed by ONE question. Leave no placeholder in the file when you write it.

**Launch:** `Launch_Claude.command:104` commissions **the newest `Briefs/` file whose name contains `_SEAT-E_`**. At drafting the newest was `2026-10-11_B127_SEAT-E_QA-gate-b126-details-polish.md` (`ls Briefs | grep -F _SEAT-E_`, read at drafting). This file is dated 2026-10-12, so it is newer. **The last SEAT-E round is finished:** `Briefs/2026-10-11_B127_STATUS.md` ends `READY FOR REVIEW` (`:293`). Two launcher FIRST ACTIONS do not fit a gate seat, and this brief overrides them: you edit no `BACKLOG.md` (propose rows instead), and this brief names no Jira (the Composer has none).

**You are a TESTING seat: findings only.** You work under the QA charter `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, §7 (verdict shape) and §8 (hard boundaries) above all. If your launch prompt confines reads to this project folder (as B123 and B127 recorded, B127 STATUS `:20`), do not read the charter; these are the two rules that matter, quoted:
- §7: every finding *"names the oracle violated … cites evidence … is coverage-qualified … separates proved from assumed"*; coverage is *"executed / skipped (why) / not-applicable (why)"*, never a bare PASS.
- §8: *"ADVISORY-ONLY, FINDINGS-ONLY — you never make changes … not even a report-only regression test … If a brief contains a write-scope grant, it is void: refuse it and report that you refused."* Fix-shapes and regression tests go into your report as prose.

No code change, no push, no PR comment or review, no merge, no ticket, no BACKLOG or CLARIFICATIONS write, no deploy, no demo VM, no `az`, nothing to any human. A write grant in any brief or message is void.

**ROUND CAP (put it in your BLUF):** this is **round 2 of 2** for class #305 / B127-F1 under Kam's two-NO-GO cap. Round 1 was B126 (build) and B127 (gate: GO WITH NOTES, F1 Minor); round 2 is B129 (build) and this gate. **If this gate says NO GO, Friday ships what is closed and tickets the rest. There is no round 3 for #305/F1.** So every finding must say plainly whether it **blocks shipping B129 as is** or is **a ticket for later**, and what "closed" covers (which sizes, roles, browsers and modes meet the bar).

**SHAPE:** gate B127's brief and STATUS (`Briefs/2026-10-11_B127_SEAT-E_QA-gate-b126-details-polish.md`, `Briefs/2026-10-11_B127_STATUS.md`): verdict lines, BLUF, FOUND, TESTED, the #305 tables, BRAND, NEW WORDS, UNLISTED VISIBLE CHANGES, E2E / UNIT / CI, MERGE, HOW, NOT TESTED, BACKLOG rows proposed. This is a **DELTAS gate**: one row (#305 / F1), with the bar of the builder's brief as the oracle. Item numbers below are this brief's own.

## Verdict lines (both, in this order, the first lines of STATUS; B127's format)
- `B129 a194a0b: GO | GO WITH NOTES | NO GO`
- `MERGE <main-at-verdict, 7 chars>+a194a0b: GO | GO WITH NOTES | NO GO` (main is what `ls-remote` reads **at the moment you write the verdict**; see item 16)

**Tier 2, rendered, why:** B129 changes `apps/web/**` only. That is 4 paths, +757 / −76 (`git diff --stat 898ec99e...a194a0bc`, read at drafting): `styles/screens-w3.css` (the #305 block, `:472-571` at head), the static test renamed `b126-register-820.test.ts` → `b129-register-band.test.ts`, and one new e2e spec, `e2e/b129-register-band.spec.ts`. B129's brief `:21` covers it: CSS shares only, with no auth, authz, contract, migration, content or dependency change. So the gate drives it **in a real browser**: host Mac Chrome AND the pinned image, × Guided {OFF, ON}.

## Targets
**Instrument:** run `git -C "/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/2_Project_Files" ls-remote origin` (read-only; filter `refs/heads/main` and `refs/heads/b129/register-band-601-900`). The drafter read it at **2026-10-12 ~02:45 AEDT**. Re-read it yourself before you start, and record the time. **If the B129 head moved: STOP.** If main moved, do not stop; see item 16.

| Ref | SHA |
|---|---|
| `refs/heads/b129/register-band-601-900` (head) | **`a194a0bc1b8cb1773bb0d44dd7c42dad4abe072c`**, tree `4e2648b35aeb1a8fbc876f328816497bb41f0dad` (`rev-parse a194a0bc^{tree}`, drafting). 4 commits on `898ec99e`: `2ef840f2` the shares + static test + spec · `19965bf7` static test typed strings (tsc) · `d28aa426` spec browser detection by `navigator.platform` · `a194a0bc` the CSS comment only (`git diff --stat d28aa426 a194a0bc` = `screens-w3.css` 2+/2−, drafting). |
| `refs/heads/main` (merge base) | **`898ec99e3bd936ebb0c255918b231919fba4442e`** (PR #70, B125: API, contract, `schema.d.ts`, 4 e2e set-ups; no styles). `git merge-base 898ec99e a194a0bc` = `898ec99e` (drafting). Its styles are byte-equal to B126's `72c038d8` (`git diff --stat 72c038d8 898ec99e -- apps/web/src/styles` = empty, drafting). Tree `d1cd5818…`. |
| **Break-count base** | **`4e00d573cc4c1ae215e2aad70e92a08e3218281b`** (main before B126; the build live on the demo, C-68). As B127 did, "NEW broken word" and "NEW overflow" always mean: present at head and absent at `4e00d573`, at the same width, pointer, role, register, browser and Guided state. |
| B126 column | `72c038d8` (styles = `898ec99e`'s). It is the second column of every table, so Friday can see what round 2 changed against round 1. A `898ec99e` stack serves as this column: say so, and show the styles diff = empty. |
| PR | None at drafting (Friday opens it). CodeQL / PR checks: one line, NOT TESTED, Friday's. |

All four commits are in the local objects of `2_Project_Files` (`git cat-file -t` = commit, drafting).

## Read first, whole
- **The oracle:** B129's brief `Briefs/2026-10-12_B129_SEAT-B_register-band-601-900-fix.md`. **Its §5 BAR (`:71-79`) is this gate's bar**, with Friday's placement line (`:74`):
  - **0 NEW broken words** vs `4e00d573` across 601–900 (key spans excluded, as B123/B127 did);
  - **NO NEW overflow** vs `4e00d573` (every register `td`/`th` child's box, text Range and control, inside its cell ± 0.5 px; base's own overflows are listed, not counted);
  - **B126's 820 wins kept** (`:75`): the date "2027-09-12" and "Authentication" whole at 820 / 820 touch, plus Mac consultant "@remediation", "Configuration", "Forgery(CSRF)" and "Expiry";
  - **computed shares at 1280, 1180 touch, 901, 901 touch and 390 EQUAL to base** (`:76`);
  - **every Choose box 44 × 44** (`:77`);
  - **brand OFF-GUIDE 0** and static literals 0 (`:78`).
  - Also: §1 F1 verbatim (`:23-41`), §3 write set (`:54-61`), §4 HELD (`:63-68`), §6 PROVE IT (`:97-106`), §9 UNMEASURED (`:140-146`).
- **The claims:** `Briefs/2026-10-12_B129_STATUS.md` (ends `READY FOR QA: b129/register-band-601-900 @ a194a0bc…`, `:241`):
  - BLUF `:5-27`, FOUND F-1…F-3 `:29-34`, TESTED `:36-54`;
  - **HOW** `:56-96`: the four-range table `:59-65`, "why each share works" `:69-74`, the static test `:76-84`, the e2e spec `:86-96`;
  - TEST EVIDENCE `:105-121` (red-first, tampers `:117-118`, `ci.sh` `:119`, full e2e `:120-121`);
  - **THE BAND TABLE** `:124-160`, B127's ROUND 2 list item by item `:162-175`;
  - NOT TESTED `:177-180` (**"Fractional viewport widths … covered by the `.98` bounds (no gap)"**: a claim you test, item 6);
  - NEW WORDS `:182-183`, **NEW LOOK L1–L9** `:185-200`, MEASURED, NOT FIXED `:202-211`, BACKLOG `:216-219`, UNMEASURED `:221-228`.
  - Evidence: `Briefs/2026-10-12_B129_evidence/` (`specs/b129-measure.spec.ts`, `specs/b129-extras.spec.ts`, `stack/*`, `static/*`, `shots/INDEX.md`). The records are on local `records/b129` @ `fb80a57e` (in `_wt_b129rec`; B129's, never yours).
- **The round-1 gate:** B127 STATUS: F1 `:80`, the #305 BREAK LISTS `:166-168`, SHARES `:170-181`, Q-1 CHOOSE BOXES `:183-195`, BRAND `:197-202`, HOW `:231-262`, **ROUND 2 list `:277-285`** (this gate checks every item of it that F1 touches). B127's band instrument: `Briefs/2026-10-11_B127_evidence/specs/b127-gate.spec.ts` (sizes `:16-32`, `census` `:164`, `underFooterBar` `:243`, the G305 loop `:604-668`, GSWEEP `:783-833`, G305BAND shots `:976-998`) and `…/stack/g305-breaks.py` (by-word base vs head, key-span filter).
- **Re-derive everything yourself.** B129's tables, logs, shots, specs and tests are claims, not evidence. Re-measure every headline number with **your own instrument**: a copy of B127's band instrument in **your** scratchpad, renamed and parameterised by you. **Copy instruments, never run another seat's in place, never edit the originals.** B127's and B129's scripts are pinned to their own stack names and ports, so they refuse yours. B129's `b129-register-band.spec.ts` and `b129-measure.spec.ts` run only as a **second instrument**, labelled so. A number that only B129's instrument produces is UNVERIFIED.

## RULINGS CARRIED (quote them; do not re-rule)
- **B126 Q-1: "Choose = 44px: KEEP"** (`Briefs/2026-10-11_B126_SEAT-B_ADDENDUM-1_q1-q2-answers-records.md:8`). B129 keeps it for the whole band (`screens-w3.css:483-487` @a194a0bc).
- **Friday's placement line on the bar** (B129 brief `:74`): *NO NEW overflow vs base*. Fixing base's own overflows ("Raise exception" at 601/700) is a bonus, not the bar.
- **Shape (b) is allowed** (B129 brief `:88`, "more than one nested media range inside 601–900"). You judge whether the four ranges meet the bar and are maintainable (item 9). You do not re-rule the shape choice.
- **The cards layout below ~900 px is HELD** (Kam's). B127-F2…F9 are not this round.
- **NEW WORDS (expected none) and NEW LOOK L1–L9 are Kam's, not this gate's.** You check that each renders exactly as and where listed, and that it breaks nothing. **Friday shows Kam NEW WORDS + NEW LOOK + shots before any demo deploy.**
- **HELD byte-identical** (B129 brief §3/§4): `apps/web/src/styles/tokens.css`, every rule of `screens-w3.css` outside the #305 block (`:472-571` at head), `apps/web/e2e/b126-details-polish.spec.ts` and every other pre-existing e2e spec, `e2e/run.sh` (image pin `:15`), `components/**`, `packages/**`, `apps/api/**`, `content/**`, `scripts/**`, every `package.json` and the lockfile.

## Stacks, trees, ports (the PARTITION)
- **Other seats:** other Datasec seats may be live on this machine (Docker, CPU, Chrome). **Never start, stop, reuse, inspect-and-change or remove** `pc-b128*` (SEAT F), `pc-b129*` (B129, closed; its volumes kept) or `pc-b12[0-7]*`, nor any `_wt_b12*` / `_wt_b129rec` worktree or B129's scratch `wt/*`. Whether any of them is up now is **UNMEASURED** (Docker was not queried at drafting).
- **Your block: ports 6830–6839**, subnets **10.130.1.0/24 – 10.130.9.0/24**, stacks **`pc-b130*`** only.
  - **What the drafter checked (2026-10-12 02:48 AEDT):**
    - a grep for `\b683[0-9]\b` over every `2026-*.md` in each Datasec project's `1_Project_Definition/Briefs/` (4 projects) and in Friday's `briefs_drafts/` (1,138 files) found **0 files**. The control `\b682[0-9]\b` found **3** (B129's block);
    - `10.130.` and `pc-b130` appear in 0 files (control `10.129.`: 3);
    - `lsof -nP -iTCP:6830-6839 -sTCP:LISTEN` found no listener (rc 1).
    - Avoided explicitly: **6540–6549, 6730–6739, 6750–6769, 6820–6829, 6950–6959**.
  - Use a throwaway Postgres on **127.0.0.1:6830**, edge ports **6831–6838**, and `ci.sh` on **`PC_CI_EDGE_PORT=6839`**. Before each `up`, re-check `lsof` and `docker network ls` / `inspect` (subnet overlap), and list what you found in HOW. If 6830–6839 or 10.130.x is taken: STOP (one question: which block).
  - **At most two of your stacks up at once.** Suggested: `pc-b130base` / `pc-b130baseon` (`4e00d573`, OFF / ON); `pc-b130main` / `pc-b130mainon` (`898ec99e` = the B126 column and the full-e2e base); `pc-b130head` / `pc-b130headon` (`a194a0bc`); `pc-b130m` (the merged tree, only if main moved, item 16).
- **Trees:** your own detached worktrees (`git worktree add --detach`) or `git clone --shared` copies, **in YOUR scratchpad only**. Read-only git verbs in the project repo (below), with `--no-optional-locks`.
- **Mac Chrome** = the installed Google Chrome, headless, a fresh profile, 127.0.0.1 only; state its version (B127/B129: 155). **The pinned image** = `mcr.microsoft.com/playwright:v1.63.0-noble@sha256:eff16c30e6f3f4af0a03fa4b706120d5e9b0891c344a27d64559aff5900a4a27` (`apps/web/e2e/run.sh:15` @a194a0bc, read at drafting). It renders in WenQuanYi Zen Hei (#258), so a layout number from the image alone is not a Mac number: report both.
- **Seed data** through the API and the screens only, fictional ("E2E synthetic b130 …"), on synthetic tenants of your own. **Both registers:** r1 (B126's shape; the consultant's has Choose) and r2 (B51's "No longer needed" shape, whose consultant Actions hold "Withdraw…"; B129 HOW `:87`, recipe D-023). Answers served with `page.route` are labelled "API answer served by the test" in every table and shot.
- **Time-box (charter §10):** about 6 hours of wall clock. If you reach it before the verdict, write what is executed and end `STOPPED: NEEDS FRIDAY` with one question.

## Gate items (each with its instrument and a control that could fail)

**A. Frame.**
1. **Diff frame.** `git diff --name-only 898ec99e...a194a0bc` should give the 4 paths. `git diff 898ec99e...a194a0bc -- apps/web/src/styles/screens-w3.css` should touch only the #305 block (every hunk inside `:464`'s outer block). The HELD list should be byte-identical (`git rev-parse <sha>:<path>` equal at both, for each path). **Control:** the same instrument on `screens-w3.css` must report a difference.
2. **`d28aa426` vs `a194a0bc`:** B129's NEW LOOK shots are of `d28aa426` (STATUS `:186`). Confirm that the difference is the CSS comment only, and that `vite build` emits the same CSS at both (B129: `index-DvaqW66Q.css`, STATUS `:110`). If they differ, the shots do not show the head, and that is a finding.
3. **Case-collision + `/private/tmp` guard** (B111-F1). At head, `git ls-files apps/web` lower-cased and passed through `uniq -d` must be empty. In a `/private/tmp` worktree of `a194a0bc`, run `vitest run apps/web`, `tsc -p apps/web/tsconfig.json` and `vite build`: each exits 0, with counts as ratios (B129: 1394/1394, 165 files).

**B. The bar, re-measured (#305 / F1).** Use your own copy of B127's G305 walker: Range `getClientRects` per word, key spans excluded; every cell child's box inside its cell; `getComputedStyle(th).width` + rendered px per column; `.w3-choose` `boundingBox`; `scrollWidth`; `matchMedia` for each of the five nested queries and the outer `:464` one, recorded per state. Run it on base `4e00d573`, B126 column `898ec99e` and head, **both roles** (consultant, auditor), **both registers** (r1, r2; Choose and no Choose), **both browsers**, **Guided OFF and ON**.

4. **B127's sample states, re-run:** 601, 601 touch, 700 touch, 768 touch, 820, 820 touch, 900, 900 touch, 901, 901 touch, 1180 touch, 1280×800, 390×844. Add B129's 640 and 850 (touch and non-touch). For each state, check **0 NEW broken words; 0 NEW overflow**, with base's overflows listed by count and worst px. At 820 / 820 touch, B126's wins are kept. Your counts sit beside B129's band table (`:128-157`) and B127-F1's (`B127_STATUS.md:80`): agree, or say by how much and why.
5. **The four range boundaries B129 chose** (`screens-w3.css:488 / :499 / :516 / :551` @a194a0bc: ≤ 699.98 / 700–767.98 / 768–820.98 / 821–900). Test **699, 700, 767, 768, 820, 821, 900, 901** (touch and non-touch). Also test a fractional width inside each range near its end: **699.5, 767.5, 820.5**. Expected: each falls in the range below its boundary (`matchMedia` per query shows which range applied).
6. **The gaps between ranges.** The ranges end at `.98` and the next starts at the integer, so a viewport of **699.99, 767.99 or 820.99** CSS px matches **no** range. Only the outer block and the Choose 44 px rule apply there. This contradicts B129's "no gap" (STATUS `:178`), which is UNMEASURED by B129: its dense proof is integers only. Measure the bar at those three widths too.
   - **How to reach a fractional width (your choice; name it):** e.g. a same-origin `<iframe>` of the app sized `width: 699.5px` (media queries then evaluate against the frame's viewport), or a CDP device-metrics override. **Control:** at 699.5 inside the frame, `matchMedia('(max-width: 699.98px)')` is true; at 699.99 it is false, and so is `matchMedia('(min-width: 700px)')`.
   - Grade the outcome: a NEW break or NEW overflow in a gap is a finding. Weigh its severity by how a real viewport reaches that width (desktop browser zoom yields fractional CSS widths; an emulated or real tablet at an integer width does not), and **say whether it blocks shipping or is a ticket**.
7. **Shares outside the band equal base:** computed + rendered px per column at 1280, 1180 touch, 901, 901 touch and 390, both roles, both registers, both browsers, OFF and ON. B129 claims 25/25 per browser and mode (STATUS `:12`, `:160`).
8. **Choose 44 × 44** at every touch state in the band and at 1180 touch / 390, for every `.w3-choose` label and every row. Report the Actions column px at each band state, base / B126 / head. Check B129's floor claims yourself: **Actions ≥ 50.5 px** everywhere in the band (measured minimum 50.7), and **0.2 px under base only at 768–770, consultant** (STATUS `:71`, `:197`). A control that becomes unreachable or overlaps is a finding (B127 item 14).
9. **Is the four-range shape maintainable?** Read `screens-w3.css:472-571` @a194a0bc as text and as the built CSS:
   - Tabulate every declaration: range × selector × column (nth-child) × value. Mark any value that is **duplicated** (the same selector declared twice in one range, or a range re-declaring the value it already inherits from B120 / #188, `:346-415` / `:464-475`). Mark any value that is **contradictory** (two rules for one column that both apply at one width).
   - Check that every `/* column */` comment names the column the `nth-child` actually is, in that register. Read it from the rendered header text per register; the no-Choose and Choose registers are offset by one.
   - From the declared shares, compute the leftover for Actions at each range's narrowest **and** widest width, and compare it with what you measured.
   - Check that the static test (`b129-register-band.test.ts`) pins exactly what the CSS declares, with nothing unpinned and no stale pin.
   - State the result in one line: maintainable / maintainable with notes / not. **Cite each line.** A duplicate or contradiction is a Note unless it changes a rendered share.
   - Also check B129 F-2 ("`max(44px, 6%)` is laid out as auto in Chrome's fixed table", STATUS `:33`). It sits outside the bar, so one measurement at 1180 touch is enough: report it.
10. **Tamper arms** (scratch copy, sha256-equal restore, logged as `runs/tamper_*.log` + `.diff`):
    - **Delete one range at a time** (four arms) from a scratch copy of `screens-w3.css`, then rebuild and re-measure. **Expected:** that range's widths get back the breaks / overflows that B126's or the outer shares give there, and the other three ranges are unchanged. A deleted range that changes nothing is a finding (a dead range).
    - **Delete the Choose 44 px rule** (`:483-487`). **Expected:** the Choose width goes back to `max(44px, 6%)` / auto, and you report what changes.
    - **The CSSOM arm:** delete each range in the page on the head stack (no rebuild); the same expectations apply.
    - **Restore:** sha256 of `screens-w3.css` equal to `a194a0bc`'s blob; the tree is clean.
    - **Also:** show that B129's static test goes red for each deleted range, and that its band spec goes red for at least one deleted range in each browser (second instrument).

**C. Brand and visible things.**
11. **Brand, against the style source `apps/web/src/styles/tokens.css`** (unchanged: item 1).
    - **OFF-GUIDE census of the changed values:** on the head register at one width per range (e.g. 650, 730, 800, 860) plus 820 touch, both roles and both browsers, build a painted part · computed value · token-or-**OFF-GUIDE** table, ending `OFF-GUIDE: <n>`. The bar is **0 new**. **Control:** the instrument must find base's known off-guide Feedback pill `#c05000` (C-22; B129: 1 → 1).
    - **Static, on the added lines of the branch diff:** hex 0, `rgb(` / `hsl(` 0, radius that is not a token 0, `!important` 0, `content:` 0, and only `width:` declarations with % or px. **Control:** the matcher finds base's `#ffffff`.
12. **axe** (WCAG 2.2 AA, B127's `TAGS`) on S9 with both registers at 1280, 1180 touch, 820 touch, 390 and one width per range, both roles, both browsers, OFF and ON. Count violations base vs head; a new one is a finding.
13. **Visible things the builder did not list:** at **1280×800, 1180 touch, 820×1180 touch and 390×844**, both browsers, OFF and ON, base vs head, over S9 (both registers, the withdrawn list) and every screen that loads `screens-w3.css` rules:
    - the text-line diff (`innerText` lines, and per element the line count via `getClientRects`), each difference classified against L1–L9 or reported as a finding;
    - **mid-word breaks** at head that base did not have;
    - no sideways scroll (against the set viewport);
    - nothing new under the sticky footer bar at load (B127 `underFooterBar`).
    - At 1280 / 1180 / 390 the CSS predicts **no** difference at all (item 7). Any difference there is a finding.
14. **NEW LOOK screenshots, before and after, for Kam's card.** Your own shots of the S9 register at **601, 700, 768 touch, 820 touch, 900**, plus one width inside each range (e.g. 650, 730, 800, 860), consultant (r1 + r2) and auditor, Mac Chrome AND the pinned image, Guided OFF (ON where it differs).
    - Take three: before = base `4e00d573` and B126 `898ec99e`, after = head.
    - Add a "Raise exception" / "Withdraw…" close-up at 601, 700 and 768 touch, and the shots for any finding (including the gap widths, item 6).
    - Save them to `Briefs/2026-10-12_B130_evidence/shots/` with an `INDEX.md` naming each shot's state, tree, browser and the L-row it shows.
    - Compare at least 10 with B129's `shots/INDEX.md`. A B129 shot that does not match what you render is a finding.
    - Shots carry no `eyJ`, no password and no connection string.
    - **NEW WORDS:** confirm there are none. The diff adds no `.tsx`, content or `content:`, and the head's rendered S9 states show no line absent at base other than through wrapping. **Control:** a planted served title "Policy Composer test plant" MUST be reported.

**D. Suites.**
15. Run these:
    - **Your own gate spec** (in your evidence folder, not the repo) covering items 4–14, run in all four of {Mac Chrome, pinned image} × {Guided OFF, ON}, at base, the B126 column and head, with counts as ratios.
    - Then the **second instrument**: B129's `b129-register-band.spec.ts` + `b126-details-polish.spec.ts` + `b120-expert-screen-polish` + `s47-s9-register-layout` + `a11y` + `b68-l3-approval` (B129: image 32/32 OFF and ON; Mac 30 passed / 1 failed / 1 did not run, the failure being `b68` #143 at 390, which B129 calls pre-existing at base, F-1). **Re-measure F-1 at `4e00d573` yourself.**
    - **Red-first:** the head's static test on `72c038d8` / `898ec99e` source (B129: 1/8 → 8/8), and the band spec at the B126 column (B129: 1 failed / 1 passed → 2/2). Name the failing assertions.
    - **Web unit suite** at `898ec99e` and head (B129: 1390 → 1394).
    - **`scripts/ci.sh` at `a194a0bc`** with `PC_CI_EDGE_PORT=6839` and `PC_E8_SOW_TEXT` set as B105/B126/B129 did. Give the run id, GREEN/RED and counts as ratios (B129: node 2949 + 1 skip; db 281/281; API 1304/1304). Name a #115/#237 timing red, a B37 "precondition did not hold" or a purity-lint timeout (#267) as such, and re-run once.
    - **Full e2e** (`apps/web/e2e/run.sh`, every project), OFF and ON, `898ec99e` vs head. Diff the failing lists **by test name** (B129: OFF identical by name, 49 Guided-only names; ON 709/709). ON must have 0 failed at head.

**M. The merge (evaluated against main at the moment of the verdict).**
16. Immediately before writing the verdict lines, re-read `ls-remote origin` and record the time.
    - **If main is still `898ec99e`:** the squash is a content fast-forward, and the merged tree = `a194a0bc^{tree}` = `4e2648b3…`. Say so; the head legs are the merge legs. Line: `MERGE 898ec99+a194a0b`.
    - **If main moved:** name the new SHA and what landed (`git diff --stat 898ec99e <new>`).
      - In a `git clone --shared` in your scratchpad (never the project repo; never `merge-tree --write-tree` there), build `<new> + a194a0bc` and report `git write-tree`. A textual conflict means STOP and say where.
      - If the new main touches `apps/web/src/styles/**` or S9, re-run items 4, 5, 7 and 8 on the merged tree in both browsers. Otherwise run `tsc`, `vite build`, the web unit suite and a 1280 / 820 touch / 390 smoke of S9.
      - Any difference from the head is a finding. Line: `MERGE <new 7>+a194a0b`.
    - **If main moves after you have written the lines:** add `## ADDENDUM-1` with the re-read, and do not re-run legs the change cannot affect (B123 ADDENDUM-1 precedent).

**Out of scope:** the demo VM; the cards layout (held); B127-F2…F9; whether NEW LOOK L1–L9 is right (Kam's); real tablets (state it as UNMEASURED, emulated only, as every gate so far); other seats' branches beyond what item 16 needs.

## Report (`Briefs/2026-10-12_B130_STATUS.md`)
- The two verdict lines, first.
- BLUF: the round cap line, then the head, then the merge. Say what is **closed** (the states that meet the bar) and what, if anything, Friday would ticket.
- FOUND: Id `B130-F<n>` · Sev Blocker/Major/Minor/Note · Oracle violated (charter §7; quote the B129 bar line `:7x` or this brief's item) · What · Evidence with file:line at its SHA and shot/log path · **Blocks shipping B129? yes / no (ticket)** · Suggested fix-shape and the regression test the owner should add, in prose, not built.
- TESTED: item · run · result as a ratio · evidence path.
- **#305 BAND TABLE:** every state of items 4–6, base / B126 / head: broken-word count and NEW list, NEW overflow (count / worst px), the date and "Authentication" whole?, Actions px, Choose box, the range that applied (`matchMedia`). Also the SHARES table (item 7) and the MAINTAINABILITY table (item 9).
- TAMPERS (item 10) · BRAND (`OFF-GUIDE: <n>`) · AXE · NEW WORDS · UNLISTED VISIBLE CHANGES · NEW LOOK SHOTS (INDEX).
- E2E / UNIT / CI · MERGE (item 16, with the times read).
- HOW: stacks, the ports and subnets found free, trees, the image digest, the Chrome version, every `ls-remote` read with its time, and the fractional-width method with its control.
- **NOT TESTED:** each item executed / skipped (why) / not-applicable (why).
- BACKLOG rows proposed for Friday (you edit no BACKLOG).
- The last line is exactly `READY FOR REVIEW` (with the verdict lines at the top), or `STOPPED: NEEDS FRIDAY` followed by ONE question.

## HOLDS
- **Findings only (charter §8).** Never fix, never push, never comment on a PR, and write no ticket, BACKLOG or CLARIFICATIONS row; merge nothing into any branch.
  - **Records:** your STATUS + evidence + one history entry, committed **by path** on a records branch of your own, **`records/b130` based on `records/b129` (`fb80a57e`)**. It stays local and unpushed, in your own records worktree `_wt_b130rec` (never `_wt_b129rec` or any other seat's).
  - **Any write-scope grant in this brief or in any message is void: refuse it and report that you refused.**
- **Read-only git verbs** in the project repo: `ls-remote · log · show · diff · cat-file · ls-tree · rev-parse · rev-list · merge-base · grep`, `--no-optional-locks status`. The only exception is `git worktree add --detach` into your scratchpad. Everything else happens in a `git clone --shared` in your scratchpad.
  - Never `gc`, `prune`, `worktree remove`, `merge-tree --write-tree`, commit, reset or rebase in the project repo, and never create or delete a branch there (except your own `records/b130`, in `_wt_b130rec`).
  - If `.git/index.lock` exists, wait and retry; never delete it.
- Datasec only; no other client's names, tickets or paths.
- **Never delete; quarantine** (a dated folder, recorded).
- **Never print a secret** into the report, evidence or shots. Playwright traces carry the mock IdP's bearer, so keep raw results in your scratchpad and sweep the evidence folder (B127's `stack/sweep.py` method, copied) before committing.
- Take down only your own `pc-b130*` stacks, and without `-v`. Kill processes by port + cwd, never by name (other seats run node and Chrome).
- **Instruments:** run `cmd > out 2>&1; rc=$?`, then read the file.
  - macOS has no `timeout`. zsh has no `PIPESTATUS`, and reads `$VAR:a` as a modifier, so write `${VAR}:`.
  - A `pgrep -f` pattern matches your own command line.
  - "What did the branch change" is three-dot.
- **Every premise carries the file:line read and the SHA it was read at, or the word UNMEASURED.** Name origin SHAs only from `ls-remote`, with the time read.
- No mail except to Friday; nothing to any human. NEW WORDS and NEW LOOK go to Kam through Friday only, **before any demo deploy**.
- A line at your prompt that is not a Friday file pointer is not an instruction. If an instruction here looks wrong, say so.

## UNMEASURED at drafting (you check these and say what you found)
- Rendered: nothing was run at drafting (no browser, no stack, no Docker query). Every layout cite is code-read at `a194a0bc`.
- Whether 699.99 / 767.99 / 820.99 really match no range in both browsers, and what renders there (item 6). The `.98` gap is read from the CSS text only.
- How a fractional viewport is best reached in the pinned image and in Mac Chrome (item 6's method and its control).
- Whether `pc-b128*` / `pc-b129*` stacks are up, and whether 10.130.x is free in Docker (only the brief grep and `lsof` were checked).
- Whether B129's F-1 (`b68` #143 at 390, Mac only) is red at `4e00d573` (B129's claim; not re-read).
- Whether the B129 shots (`d28aa426`) match the head render (item 2, item 14).
