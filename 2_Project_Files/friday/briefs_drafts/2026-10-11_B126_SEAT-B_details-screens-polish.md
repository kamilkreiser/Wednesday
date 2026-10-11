From Friday (laptop seat), Datasec / Security Composer.

# BRIEF B126 (SEAT B): Lane T2-DETAILS, `apps/web/src/screens` and `apps/web/src/styles` only. Expert screens a salesperson sees: #298 (a failed re-read still says "the page now shows it"), #299 (no "Choose a policy" on a stale pin), #301 (two absence tests that do not bite), #305 (the 820 px band on S9), #308 (a long name with no spaces scrolls 390 sideways), #155 (withdrawn Setting keys break mid-word), #68 (in-scope group columns only, latent). Tier 2.
**From:** Friday (laptop seat), 16:51 AEDT 2026-10-11. Replies go to Friday. **Seat:** Datasec/Security-Composer-B. Datasec / Datasec Security Composer only (the product is "Policy Designer" on screen, C-62). Report `1_Project_Definition/Briefs/2026-10-11_B126_STATUS.md` (BLUF · FOUND · TESTED · HOW · **PRIOR WORK (required)** · **TEST EVIDENCE (required)** · NOT TESTED · **NEW WORDS (required)** · **NEW LOOK FOR KAM (required, with screenshots)** · MEASURED, NOT FIXED · QUESTIONS FOR FRIDAY · UNMEASURED). The last line is `READY FOR QA: <branch> @ <sha>` (branch pushed, head SHA read by `ls-remote` in the same action, `ci.sh` green, the READY items in §7 present) or `STOPPED: NEEDS FRIDAY` followed by one question.

**Launch (how Friday starts this seat, as B120/B121 were started):** `cockpit.sh launch Datasec/Security-Composer-B` (`FRIDAY/2_Project_Files/fleet/cockpit/launchers.conf:35` → the project's own `Launch_Claude.command`). That launcher reads the pane name, sets `YOUR SEAT: B`, and commissions **the newest brief whose file name contains `_SEAT-B_`** (`Launch_Claude.command:92-105`): this file. Two things in the launcher's FIRST ACTIONS do not fit this round, and this brief overrides them for this seat only:
- It says to read `./BACKLOG.md`. **The working copy is records `main` (`441fa893`, 293 lines), which does not hold #298–#308**: `grep -c` of the six row numbers #298, #299, #301, #303, #305 and #308 there = 0, control #146/#150/#155 = 3. Read the rows from `git --no-optional-locks show records/b124:BACKLOG.md` (records/b124 = `ce70da67db8cee3785409960fae1852dc2b113b4`, 307 lines; `git merge-base --is-ancestor records/b124 main` = false). C-67 and C-68 are likewise only on `records/b124`.
- It says to record progress in "the Jira ticket(s) the brief names". **This brief names none** (the Composer has no Jira; `BACKLOG.md:4` @records/b124). Its scope rule 1 (this folder only) stands: the FRIDAY paths cited here are provenance, not reading.

**Authority (Kam, Friday's terminal, 2026-10-11 ~11:58, verbatim, recorded at `FRIDAY/0_Brain/daily_friday/2026-10-11.md:64`):** *"I have logged you in using a freash account. please continue on the work with HPSM poc, security composer and the MPS calculator"*. Friday's reading: keep building the Composer's agent-doable rows. The rows are commissioned from Friday's read-only sort of every open BACKLOG row (`FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-11_composer_open_backlog_sort.md` §6 "T2-DETAILS"). **Nothing here is a Kam words-or-look decision.** Four rows (#298, #299, #305, #155) carry **Friday's reading, to be confirmed at the gate**, stated at each row. Every changed look (#299, #305, #308, #155) and any new sentence goes to Kam as NEW LOOK / NEW WORDS, and **his look comes BEFORE any demo deploy** (#251 precedent). This brief deploys nothing.

**Base.** Composer origin main = **`4e00d573cc4c1ae215e2aad70e92a08e3218281b`**: the build LIVE on the demo since B124 (C-68, `Briefs/2026-10-11_B124_STATUS.md`, records/b124 `ce70da67`). The drafter read it at 2026-10-11 16:37 AEDT two ways: `friday_as.sh datasec gh api repos/datasecau/Datasec-Security-Composer/commits/main --jq .sha` and `git ls-remote origin refs/heads/main`. Both gave `4e00d573…`. **The local clone does not hold that commit** (`git cat-file -t 4e00d573…` in `2_Project_Files` = "could not get object info"). Every code cite below is **(read at `4e00d573`)**, read with `git show 4e00d573:<path>` / `git grep … 4e00d573` in a `git clone --shared` of `2_Project_Files` after a fetch.
- **First action:** in your own worktree, `git fetch origin`, then `git -C 2_Project_Files ls-remote origin refs/heads/main`. **If it is not `4e00d573…`: STOP** (`STOPPED: NEEDS FRIDAY`, with the new SHA and the time read). Do not rebase onto a moved main on your own.

**Branch** `b126/details-screens-polish` from `4e00d573`, own worktree **`/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/_wt_b126`** (absolute, outside `2_Project_Files`). At drafting neither exists: `ls -d _wt_b12*` gives `_wt_b120`, `_wt_b121`, `_wt_b124rec` only; `git branch -a --list '*b125*' '*b126*'` is empty (0 lines); `ls-remote origin 'refs/heads/b12*'` lists only `b120/…` and `b121/…`.
**Tier 2:** no auth, authz, contract, migration, content or dependency change. Friday decides the gate after you.

**Running in parallel: SEAT A** (`Datasec/Security-Composer-A`, brief `Briefs/2026-10-11_B125_SEAT-A_api-contract-correctness.md`, Lane T1-API, tier 1) may be LIVE at the same time. It owns **`packages/api-contract/src/**`**, **`apps/api/src/routes/**`** and **`apps/api/test/**`**. Friday may also confirm three more files for it: `apps/web/src/api/schema.d.ts` (regenerated), `apps/web/src/feedback/types.test.ts:297-298` and one `apps/api/src/authz.ts` entry. **Those paths are NOT yours.** Its stacks are `pc-b125*` on 10.125.x.0/24 and ports **6750–6759**: never start, stop, reuse or remove them. Its contract bump (0.32.0) changes the generated types your screens compile against. Your branch is built on 0.31.0, and the gate checks the merge; do not read or depend on SEAT A's branch. Other Datasec seats may share the machine (Docker, CPU) but no files.

---

## 1. Why: the rows (quoted verbatim from `git show records/b124:BACKLOG.md`, records/b124 `ce70da67`; do not re-rule)
- **#298** (`BACKLOG.md:294` @records/b124): *"**Gate B117-F1 (Minor; PR #65, B116).** Oracle, verbatim: "It also proves that the screens claim nothing the API did not answer" (brief :10); item 15's probe What, verbatim: *"The sequence is: setPolicyTarget refused 409 POLICY_TARGET_ALREADY_CHOSEN, then the re-read `GET /engagements/{id}` fails (served 503). What renders: the hint "This engagement's policy was chosen in the meantime, and **the page now shows it**. …". The Policy card still says **"Not chosen No policy was chosen."**, the chooser **stays open with ML2 selected**, and **"Reload the latest details" is not offered**. A second "Choose this policy" would only be refused again. The catch swallows the failure (`EngagementDetails.tsx:340` @f64f9aa; its comment says the card "keeps what it read"). The hint is fixed (`w1/problems.ts:37-38`). Nothing is written (real policy, revision and audits equal before and after). With an OK re-read, the card shows the other choice (ML3) and the chooser closes, as B116 says."* Evidence, verbatim (gate B117's, under `Briefs/2026-10-10_B117_evidence/`): `data/g_mac_head_off.jsonl` and `g_img_head_off.jsonl` kind D15, case "PROBE: re-read GET fails (503)": `card_first_row "Not chosen No policy was chosen."`, `form_still_open 1`, `select_value "e8-2023-11-ml2"`, `reload_button 0`, `hint409 true`. The same in ON (`g_*_head_on.jsonl`). Shots: `shots/g_*_head_*/b117_*_details_refused_POLICY_TARGET_ALREADY_CHOSEN_reget_fails_1280.png` ("API answer served by the test"). Suggested shape, verbatim: *"When the re-read fails, do not claim the page shows it. Show the failed read (ErrorState) with "Reload the latest details", as the 412 path already does, and close or disable the chooser. Or use a hint variant that says to reload to see the chosen policy. **Test:** DOM test: 409 ALREADY_CHOSEN, then a failing GET. Assert the text has no "the page now shows it", the reload button is present, and the "Choose this policy" submit is gone or disabled."* Source: `Briefs/2026-10-10_B117_STATUS.md:61` FOUND (round 1). Discovered 2026-10-10 by gate B117. Row added 2026-10-10, B119."* State: *"OPEN, **next round** (gate B117 round 1 GO WITH NOTES; Kam approved B116's words and the deploy, card `composer-b116-words-look-1010` a; now live on the demo, C-67)."*
  - **Slice (Friday's reading, to be confirmed at the gate):** the first shape. When the re-read fails, show the failed read (the existing `ErrorState`) with the existing **"Reload the latest details"** button, and close the chooser. **No hint variant**: that would be a new sentence. Why: it reuses words Kam has already seen and is reversible.
- **#299** (`BACKLOG.md:295` @records/b124): *"**Gate B117-F2 (Minor; PR #65, B116).** Oracle, verbatim: "The UI must never offer" a control whose only outcome is a refusal (the brief's R-3 aim and item 30's spirit: "No visible control appears for a role whose API call would 403"); item 13's probe What, verbatim: *"**"Choose a policy" is offered on an engagement pinned to a content release the service no longer runs.** `policyChooser` (`EngagementDetails.tsx:738-748` @f64f9aa) does not compare pins. setPolicyTarget then always answers **409 CONTENT_VERSION_CHANGED** (`refuseStalePin`, `engagements.ts:914`, which runs first). The page shows the API's words: "This cannot be done in the engagement's current state. This version is pinned to a content or device-capability release the service does not run. Moving it to the new release is an explicit action that is not available yet." The web adds **no next step**: `w1/problems.ts` has 0 CONTENT_VERSION_CHANGED lines (`grep -c`). The words are readable. Nothing is written (target null, revision 1 → 1). Reached on my TEST stack by creating the engagement on the demo release `05070f1d…` and then running the TEST release `7030ac3f…`. Both browsers, Guided OFF and ON."* Evidence, verbatim (gate B117's, under `Briefs/2026-10-10_B117_evidence/`): `data/t_{img,mac}_{off,on}.jsonl` kind probe-stale-pin: `offered_choose 1`, `put … 409`, `target_after null`, `revision_before_after [1,1]`. Shots `shots/t_*/b117_*_probe_stale_pin_details_1280.png`, `…_probe_stale_pin_refused_1280.png` ("TEST release, not lane 3a") Suggested shape, verbatim: *"R-3 needs one more term, "pinned to the running release". The pattern exists: `cloneBlock` (`w1/editability.ts:50` @f64f9aa) compares `running.id` with `engagement.content_release.id` and refuses up front in the API's own words. Friday rules whether to add it, because it changes R-3. **Test:** a DOM arm with the running release ≠ the engagement's pin → no "Choose a policy" (plus that state's sentence, if one is ruled)."* Source: `Briefs/2026-10-10_B117_STATUS.md:62` FOUND (round 1). Discovered 2026-10-10 by gate B117. Row added 2026-10-10, B119."* State: *"OPEN, **next round** (gate B117 round 1 GO WITH NOTES; Kam approved B116's words and the deploy, card `composer-b116-words-look-1010` a; now live on the demo, C-67)."*
  - **Slice (Friday's reading, to be confirmed at the gate):** **add the term** to R-3. "Choose a policy" is offered only when the running release is known and equals the engagement's pin (cloneBlock's comparison). While `running` is unknown (not read yet, refused or failed), the chooser behaves as today and the API stays the backstop, as cloneBlock does. **No new sentence** for that state. Why: the oracle already forbids a control whose only outcome is a refusal; hiding the control is reversible; a sentence would be new words Kam has not seen. The missing control is a **NEW LOOK** row.
- **#301** (`BACKLOG.md:297` @records/b124): *"**Gate B117-F5 (Note (test strength); PR #65, B116).** Oracle, verbatim: Item 5: "say whether it really asserts an absence that base also satisfies, or is a weak test" What, verbatim: *"Two of B116's "pass by design" DOM tests **do not bite**. I mutated a scratch copy of head, restoring it sha256-equal after each mutant. (a) Removing R-3's role term (`draftEditBlock` line in `policyChooser`) leaves **both role arms green** (auditor, security reviewer). Only the "in review" arm goes red. (b) Showing the `[]` sentence to any role leaves "**[]: no sentence for a role that cannot choose**" green (21/21). The cause in both: those roles cannot read the list (`POLICY_TARGET_READERS` = consultant, content_manager, platform_admin, `PolicyTargetParts.tsx:43`), so the screen never reaches the state the term guards. In mutant (a), an auditor would see the list's **failed words + Try again**, and the arm does not look for them. **The product is right live:** platform_admin and content_manager, who can read the list, get no action (D13, both browsers). Every other absence arm bites: target, set-up, error-as-ready and null-as-0 each go red under their mutant."* Evidence, verbatim (gate B117's, under `Briefs/2026-10-10_B117_evidence/`): `runs/b5_mutants.txt` (m1–m6); `stack/b5-mutants.sh` Suggested shape, verbatim: *"Use a list-reading non-consultant (platform_admin) for the role arm and for the `[]`-sentence negative, and also assert no picker / no failed words. **Test:** mutant m1 must turn the role arm red."* Source: `Briefs/2026-10-10_B117_STATUS.md:65` FOUND (round 1). Discovered 2026-10-10 by gate B117. Row added 2026-10-10, B119."* State: *"OPEN, **next round** (gate B117 round 1 GO WITH NOTES; Kam approved B116's words and the deploy, card `composer-b116-words-look-1010` a; now live on the demo, C-67)."*
  - **Slice:** the row's test change, unchanged. No product change.
- **#305** (`BACKLOG.md:301` @records/b124): *"**Gate B123-F1 (Minor; PR #68, B120).** Oracle, verbatim: "each row's before/after at 1280, 1180 and 390 … and anything visible the builder did not list"; C-03 "Phone and tablet are REAL targets" What, verbatim: *"**#210 in the 601–900 band (820 × 1180, touch):** "Authentication" still breaks inside the word at head, for the auditor and the consultant, in both browsers. With the Choose column (consultant), B120's shares (`screens-w3.css` Category 11 %, Setting 14 %, Expiry 6 %; the #188 touch set's Setting 12 %, `e7aed51`) make Category's words whole but **add new mid-word breaks**: **"2027-09-12"** (the expiry date, broken inside a number, not at a hyphen; Expiry 53 → 45 px) and **"Forgery(CSRF)"** in both browsers, plus **"Configuration"**, **"@remediation"** (Setting 113 → 90 px) and the **"Expiry"** header in Mac Chrome. Net break count: Mac 25 → 24, image 21 → 19, so the band is no better and different. For the auditor (no Choose), head is strictly better (Mac 16 → 12; image 11 = 11). B120 measured only 1280, 1180 and 390 (its NOT TESTED). The band was already badly broken at base ("Devic\|e Contr\|ol")."* Evidence, verbatim (gate B123's, under `Briefs/2026-10-11_B123_evidence/`): `static/g210-820-breaks.txt`; `data/gate_{base,head}_{mac,img}_{off,on}.jsonl` kind G210; shots `shots/gate_{base,head}_mac_off/mac_g210_s9_register_consultant_820touch_guided-off.png` Suggested shape, verbatim: *"A share set for 601–900 px (the register is a table there), or let the Expiry date wrap only at its hyphens (`overflow-wrap: normal` / a non-breaking date format) and keep Setting ≥ its longest word, or show the register as cards below ~900 px as at ≤ 600. **Test:** extend B120's #210 e2e to 820 × 1180 touch, both roles: no new broken word against base's list, the Expiry date never broken inside a number, and "Authentication" whole."* Source: `Briefs/2026-10-11_B123_STATUS.md:76` FOUND (round 1). Discovered 2026-10-11 by gate B123. Row added 2026-10-11, B124."* State: *"OPEN, **next round** (gate B123 round 1 GO WITH NOTES ×2; Kam approved the deploy, card `composer-4e00d57-words-look-demo-deploy-1011` a; now live on the demo, C-68)."*
  - **Slice (Friday's reading, to be confirmed at the gate):** CSS only, **inside the existing 601–900 / touch media block** (`screens-w3.css:464`), in this order:
    1. the second shape first: the Expiry date never breaks inside a number (it wraps at its hyphens or not at all), and Setting is kept at or above its longest word;
    2. shares inside that block, **only if** step 1 alone does not meet the row's test.
    - **Not the cards layout below ~900 px**: it is the largest change and a layout Kam has not seen.
    - 1280, 1180 and 390 stay byte-identical in computed shares; prove it.
    - Every changed share or wrap is a **NEW LOOK** row.
- **#308** (`BACKLOG.md:304` @records/b124): *"**Gate B123-F4 (Note (pre-existing; head slightly wider); PR #68, B120).** Oracle, verbatim: "no sideways scroll at 390" (B120 brief §6) What, verbatim: *"**An engagement name with no spaces** ("E2E_synthetic_b123_…", 73 characters) makes S4, S5, S7 and S9 scroll sideways at 390, at base (511 px) and at head (**525 px**, +14: the flex `li` and its 8 px chevron margin). Details overflows to 965 px at both (beyond the breadcrumb). B120's long name had spaces, so it was not covered."* Evidence, verbatim (gate B123's, under `Briefs/2026-10-11_B123_evidence/`): `data/*` kind G108d (`unbroken`); shots `mac_g108d_breadcrumb_{details,s5}_unbroken_390_guided-off.png` Suggested shape, verbatim: *"`overflow-wrap: anywhere` on the breadcrumb link and the h1 (title). **Test:** a 73-character name without spaces → scrollWidth = 390 on every engagement screen. Proposed BACKLOG row (below)."* Source: `Briefs/2026-10-11_B123_STATUS.md:79` FOUND (round 1). Discovered 2026-10-11 by gate B123. Row added 2026-10-11, B124."* State: *"OPEN, **next round** (gate B123 round 1 GO WITH NOTES ×2; Kam approved the deploy, card `composer-4e00d57-words-look-demo-deploy-1011` a; now live on the demo, C-68)."*
  - **Slice:** the row's shape. Details' own 965 px overflow ("beyond the breadcrumb") is measured, and fixed only where it is the same no-space name in a heading or cell, in the same way. Otherwise report it under MEASURED, NOT FIXED.
- **#155** (`BACKLOG.md:149` @records/b124): *"**B57-N3 (Low, pre-existing in kind):** long setting keys break mid-word in the withdrawn section's Setting column (`overflow-wrap: anywhere`, e.g. "admin_ews_passwo|rd_and_account_policy" at 1280), as the register's #107. Readable; the label above is whole."* State: *"OPEN (Low). With #107. B57."*
  - **Slice (Friday's reading, to be confirmed at the gate):** the row states no fix shape, so this is the reading that changes the least and is reversible. In the withdrawn section only, the key gets break opportunities at its own joints (after `_` and `.`, e.g. `<wbr>` in the rendered key). `overflow-wrap: anywhere` stays as the last resort for a single joint-free run, and the column shares are unchanged. The register's keys (#107 (c), #210 class) are not touched. **NEW LOOK** row.
- **#68** (`BACKLOG.md:72` @records/b124): *"B35 (from #56): on the Expert Discovery screen, an UNTYPED group-scoped question's table offers a column for every device group, out-of-scope ones included; a value typed there is refused 400 since B30"* State: *"OPEN (latent: both content releases have 0 untyped questions; the fixture has none group-scoped). Where: `apps/web/src/screens/Discovery.tsx` (the `groupScoped` table uses `groups` from the device profile, all of them). Fix-shape: columns for in-scope groups only, and an out-of-scope group's stored row read-only with Remove, as F1 does. Discovered 2026-10-01, B35."*
  - **Slice:** the row's shape, proved on a DOM fixture (it is latent on both content releases, so nothing changes on the demo). Take the in-scope rule from the same source F1 uses; name it.

## 2. What exists at 4e00d573 (your starting point; re-read each)
- **#298**, `apps/web/src/screens/EngagementDetails.tsx`:
  - the choose handler's catch: `setError(err)`, then for `POLICY_TARGET_ALREADY_CHOSEN` a re-read `api.GET("/engagements/{engagementId}")` inside `try`; the empty `catch {}` comment is at **`:340`** ("…so the card keeps what it read");
  - the outcome block `:355-375`: `ErrorState` `:359`, `problemHint(error, …)` `:360`, and **`isStale(error) &&`** `:361` guarding **"Reload the latest details"** `:370`;
  - the hint is `apps/web/src/screens/w1/problems.ts:37-38` (`POLICY_TARGET_ALREADY_CHOSEN: "This engagement's policy was chosen in the meantime, and the page now shows it. …"`).
  - `ErrorState` lives in `apps/web/src/components/ui.tsx` (**not your path**): reuse it, do not edit it.
- **#299:** `EngagementDetails.tsx:741-751` `policyChooser(engagement, isConsultant, choice)`, called at `:292`. Details already reads the running release, for the consultant only (`:125`, `GET /content-releases/running`), and passes it to `cloneBlock` at `:245`. `apps/web/src/screens/w1/editability.ts:50` `cloneBlock`; its comparison is `:59` `running !== null && running.id !== engagement.content_release.id`. `w1/problems.ts` has 0 `CONTENT_VERSION_CHANGED` lines (`grep -c` = 0 at 4e00d573).
- **#301:** `apps/web/src/screens/b116-details-choose-policy-dom.test.tsx` holds `describe("B116 A3 (#263) R-3 (a)…` (`:379`) and the arm `it("[]: no sentence for a role that cannot choose"` (**`:438`**). `POLICY_TARGET_READERS = ["consultant", "content_manager", "platform_admin"]` (`apps/web/src/screens/w1/PolicyTargetParts.tsx:43`).
- **#305**, `apps/web/src/styles/screens-w3.css`:
  - the register's cells `:320-324` (`overflow-wrap: anywhere`);
  - the shares `:346-375` (no Choose) and `:381-415` (`.w3-register--choose`);
  - the 601–900 / touch block **`:464-475`** (Choose `max(44px, 6%)`, Setting `12%`).
  - B120's #210 e2e is `apps/web/e2e/b120-expert-screen-polish.spec.ts` (662 lines; TOUCH = 1180 × 820 at `:22`). **That spec is not yours** (§3).
- **#308**, `apps/web/src/styles/app.css`:
  - `:290-299` `.pc-breadcrumb ol` (flex, wrap, gap 8px), `:302-304` `.pc-breadcrumb-sep`;
  - the ≤900 / touch breadcrumb rules `:1242-1270` (B120 #108 (d));
  - `h1` has only a colour rule (`:25-29`).
- **#155:** `screens-w3.css:547-551` `.w3-withdrawn-list .pc-table th, td { … overflow-wrap: anywhere; }`, shares `:552-560` (Setting 32 %). Rendered by `apps/web/src/screens/w3/withdrawn.tsx` (`:71` `w3-withdrawn-list`).
- **#68:** `apps/web/src/screens/Discovery.tsx:931` `const groupScoped = !typed && GROUP_SCOPED.has(questionId);`, the table at **`:1055`** (`{groupScoped && (`).
- **Style guide:** `apps/web/src/styles/tokens.css`, not your path to change. The app has no dark theme (B116 §2, B120 §2), so "both modes" means Guided switch ON and OFF, light only.

## 3. PARTITION (stated from both sides)
- **You (SEAT B, Lane T2-DETAILS) may edit:** `apps/web/src/screens/**` (screens, `w1/*`, `w2/*`, `w3/*`, their DOM/unit tests) and `apps/web/src/styles/**`. **But not** `apps/web/src/styles/tokens.css` (a token change needs Kam), and **not** `apps/web/src/styles/b120-radii.test.ts` or `apps/web/src/screens/fakeDom.testing.ts` (the next T2-TESTS round's #310 / #241). If a DOM test needs `fakeDom.testing.ts` changed: STOP.
- **Write-set addition, Friday confirms at placement:** **one NEW file** `apps/web/e2e/b126-details-polish.spec.ts` (no existing spec is edited). If Friday strikes it, the rendered measurements run from `Briefs/2026-10-11_B126_evidence/specs/` against your worktree, as B117/B123 ran theirs, and are not committed to the repo.
- **You must NOT edit (SEAT A's):** `packages/api-contract/**`, `apps/api/**` (routes, tests, `authz.ts` and everything else), `apps/web/src/api/schema.d.ts`, `apps/web/src/feedback/types.test.ts`.
- **You must NOT edit (nobody's this round):** `apps/web/src/components/**` (`ui.tsx`'s `ErrorState` is reused, not changed); every existing `apps/web/e2e/*` spec and `e2e/run.sh`'s image pin; `apps/web/vite.config.ts`; any `package.json`; `package-lock.json`; `packages/**`; `content/**`; `DEPLOY.md`; `scripts/**`.
- **An API need → STOP.** If a row can only be fixed with an API or contract change, do not fake it in the browser. Name the change under QUESTIONS FOR FRIDAY.
- **Records:** your STATUS (at the path above, where Friday reads it), `Briefs/2026-10-11_B126_evidence/` and a history entry. Commit them **by path** on a records branch **`records/b126` based on `records/b124` (`ce70da67`)**, in your own records worktree `_wt_b126rec`: a local commit, read back, not pushed. Do not base it on `main`, because records `main` (`441fa893`) does not contain records/b124 (B124's precedent). **Do not edit `BACKLOG.md` or `CLARIFICATIONS.md`.** List what you want changed under "BACKLOG changes for Friday".

## 4. HELD and EXCLUDED (do not build)
- **#299's state sentence:** none this round. If you find the hidden control leaves a consultant with no way to tell why, propose a sentence under NEW WORDS, marked "proposed, not built".
- **#305's cards layout below ~900 px**; and any share change at 1280, 1180 or 390.
- **#298's hint variant** (a new sentence).
- **#57** (device-group sub-answers at engagement level, `Discovery.tsx:200,269`): not this brief, even though it is in the same file.
- **#116's web half** (the approver summary showing the reason) and **sending If-Match on withdraw** (#146): they wait for SEAT A's contract; not this round.
- **Every `#ffffff` literal, every 50 % disc and 999px pill** (B120's narrowing; Kam's rows). **No new colour token, no literal hex** anywhere you touch; radius is `var(--pc-radius)` or `0`.
- **Kam's words/look rows #257, #259, #280–#288, #306, #307**, and **#222/#223** (left by Friday's ruling). If a change here would alter one of those strings or layouts, leave it byte-identical and say so. #259 (the S5 breadcrumb wrapping long names *with* spaces) is Kam's: #308 covers the no-space case only.
- **#260/#285 HELD:** the Expert set-up card (`ExpertSetupCard.tsx`, `guidedStart.ts`) stays byte-identical.
- **No demo deploy, no VM, no `az`**; nothing to Paul or any human.

## 5. SCOPE, in this order (one commit per row, so Friday can drop one)
For every row: **WHAT** · **WHERE** · **RED FIRST** (a test that fails at `4e00d573` and passes at your head; save both logs) · **TAMPER** (revert only the fix line(s) on a scratch copy, show the test goes red again, restore).

1. **Fetch and check the base** (header). Build nothing before the `ls-remote` check.
2. **#301 make the two absence arms bite** (first, because #299 changes `policyChooser` and these arms guard it).
   - WHAT: the role arm and the `[]`-sentence negative use **platform_admin** (a list-reading non-consultant) and also assert no picker and no failed words, as the row says.
   - WHERE: `b116-details-choose-policy-dom.test.tsx` (`:379-` arms, `:438`).
   - PROOF (instead of red-first: the product is right, the test was weak): B117's **mutant m1** (remove `policyChooser`'s `draftEditBlock` line, `EngagementDetails.tsx:746`) turns the role arm **red** under your test and stayed green under base's. Mutant (b) (the `[]` sentence shown to any role) turns the negative red. Restore sha256-equal after each mutant.
3. **#298 failed re-read** (Friday's reading, §1).
   - WHAT: when the re-read after `POLICY_TARGET_ALREADY_CHOSEN` fails:
     - the hint "…the page now shows it…" is not shown;
     - the failed read shows through `ErrorState`;
     - **"Reload the latest details"** is offered (the existing button and words);
     - the chooser closes (or its submit is gone).
     An OK re-read behaves exactly as at base.
   - WHERE: `EngagementDetails.tsx:325-347` (the catch), `:355-375` (the outcome block), and `w1/problems.ts` only if the hint lookup needs a flag (its words byte-identical).
   - RED FIRST: the row's DOM test (409 ALREADY_CHOSEN, then a failing GET): no "the page now shows it", the reload button present, "Choose this policy" gone or disabled. Plus the OK re-read arm (the other choice shown, chooser closed) still green.
   - TAMPER: restore the empty catch → red.
   - NEW WORDS: none expected. If any string changes, list it.
4. **#299 no chooser on a stale pin** (Friday's reading, §1).
   - WHAT: `policyChooser` returns `"none"` when the running release is known and its id ≠ `engagement.content_release.id`. Pass the `running` Details already holds (`:125`, `:245`), as `cloneBlock` reads it. While `running` is null the behaviour is unchanged.
   - WHERE: `EngagementDetails.tsx:741-751`, `:292`.
   - RED FIRST: the row's DOM arm: running ≠ pin → no "Choose a policy" (offered at base). Running = pin → offered (unchanged). Running unknown → as base.
   - TAMPER: remove the term → red.
   - NEW LOOK: the stale-pinned Details card at 1280 and 390, before and after.
5. **#308 no-space names at 390.**
   - WHAT: `overflow-wrap: anywhere` on the breadcrumb link and on the page `h1` (title), as the row says. Names with spaces render as at base.
   - WHERE: `app.css` (`.pc-breadcrumb` block `:290-304`, or the ≤900 block `:1242-1270` if that is where the link rule lives; say which); `h1` scoped to the page header, not every `h1` if a narrower selector exists.
   - RED FIRST: a 73-character name without spaces → `document.documentElement.scrollWidth` = 390 on S4, S5, S7, S9 and Details at 390 (511/525 px at base). Plus B120's spaced long name still free of a lone "›" (#108 (d)).
   - TAMPER: remove the rule → red.
   - Measure Details' 965 px (§1 slice) and report it.
6. **#305 the 820 band** (Friday's reading, §1).
   - MEASURE FIRST at 820 × 1180 touch, consultant (Choose) and auditor, both browsers: base's list of broken words (B123's instrument, `Briefs/2026-10-11_B123_evidence/static/g210-820-breaks.txt`, re-run, not copied).
   - WHAT: step 1 (the date unbroken inside a number, and Setting ≥ its longest word), then shares in the `:464` block only if needed.
   - WHERE: `screens-w3.css:464-475` only.
   - RED FIRST: the row's test, extended to 820 × 1180 touch, both roles:
     - no broken word that base's list does not have;
     - the Expiry date never broken inside a number;
     - "Authentication" whole.
     Plus B68's register words (#145: Status "Required", Risk "medium", Actions "Withdraw…") still whole at 1280, 1180 and 820. Plus computed shares at 1280, 1180 and 390 equal to base.
   - TAMPER: restore the block → red at 820.
   - NEW LOOK: S9 register at 820, consultant and auditor, before and after.
7. **#155 withdrawn keys** (Friday's reading, §1).
   - WHAT: break opportunities after `_` and `.` in the withdrawn section's rendered setting key. The text content is unchanged: copy and paste of the key, and its accessible name, are byte-identical. Prove it.
   - WHERE: `w3/withdrawn.tsx` (near `:71`); CSS unchanged unless needed.
   - RED FIRST: at 1280, `admin_ews_password_and_account_policy` (or the longest key in your fixture) has no line break inside a `_`-free run (B84's Range / `getClientRects()` instrument). Plus a DOM cell that the cell's `textContent` equals the key.
   - TAMPER: remove the break points → red.
   - NEW LOOK: the withdrawn section at 1280 and 390, before and after.
8. **#68 in-scope group columns (latent).**
   - WHAT: the untyped group-scoped table shows columns for in-scope groups only. An out-of-scope group's stored row is read-only with Remove, as F1 does.
   - WHERE: `Discovery.tsx:931`, `:1055-`.
   - RED FIRST: a DOM fixture with one untyped group-scoped question and an out-of-scope group (none exists in either content release; say so). Base offers its column; head does not; the stored row is read-only with Remove.
   - TAMPER: restore `groups` → red.
   - Say what this does on the demo (expected: nothing, 0 untyped questions; re-measure).

## 6. PROVE IT
- **Red first:** every behaviour test fails at `4e00d573` and passes at your head; save both logs. None weakened: no assertion removed, loosened or skipped. Show the before and after of every re-pinned one.
- **Layout acceptances, measured, not eyeballed** (`boundingBox` / `getComputedStyle` / `scrollWidth`), at **1280×800, 1180 (touch), 820×1180 (touch) and 390×844**, **Guided switch ON and OFF**, in the pinned image AND host Mac Chrome (B100/B101/B110 rule, #258):
  - no sideways scroll at 390, including the no-space name (#308);
  - nothing new under the sticky footer bar at load;
  - B68's register words (#145) still whole; B120's #210, #219 and #108 (d) acceptances still green.
- **Off-guide check:** 0 new off-guide values (radius, colour) on S9, Details, Discovery and the breadcrumb screens at head (B47/B110 instrument).
- **`a11y.spec.ts` (axe) green** on every screen you touched.
- **Case-collision guard (gate B111-F1):** `git ls-files apps/web | tr '[:upper:]' '[:lower:]' | sort | uniq -d` is empty at your head. In a worktree of your head under `/private/tmp` (case-insensitive APFS): `vitest run apps/web` green, `tsc -p apps/web/tsconfig.json` RC 0, `vite build` RC 0.
- **Rename guard:** `git grep -n -I -E "Policy Composer|\bthe Composer\b"` over the files you touch gives 0 new user-visible lines, and no new "HPSM" meaning the policy.
- **`ci.sh` green** at the pushed head (`PC_CI_EDGE_PORT=6769`). Name any #115/#237 timing red, B37 "precondition did not hold" or purity-lint timeout as that, and re-run once; do not fix them here. Set `PC_E8_SOW_TEXT` as B105 did.
- **Full e2e at base and head** (each project, switch ON and OFF), with the failing lists diffed (B110's instrument).
- **Every sentence explaining WHY a change works** gets a red proof, or is marked UNVERIFIED.

## 7. READY FOR QA means
This brief is **commissioned to stop at a branch: Friday opens the PR**, so READY carries no PR number. It carries:
1. the branch name and its **head SHA read from origin by `ls-remote` in the same action** as the READY line, with the time read;
2. **TEST EVIDENCE**, ready to paste into the PR body: each suite's command and its counts as a **ratio** (`n/n passed, k skipped`, never "all"), the red-first pairs, the tamper runs and #301's mutants;
3. **PRIOR WORK**;
4. **MEASURED, NOT FIXED:** #305's base break list, Details' 965 px (#308), #68 on the demo, each with its numbers;
5. **NEW WORDS:** one table, every new or changed user-visible string: file:line · was → now · screen · source (row fix shape, or "seat's own"). Expect none. #299's sentence, if you propose one, is marked "proposed, not built";
6. **NEW LOOK FOR KAM:** every changed look: #299's missing control, #305's 820 band, #308's wrapped names, #155's key breaks. Each one gets **before and after screenshots** at the widths it changes, Guided ON and OFF where the screen differs, in the image and Mac Chrome, saved in `Briefs/2026-10-11_B126_evidence/shots/` with an index file naming each shot's state. Each one is also marked with the **Friday's reading** it rests on.
   - **Friday shows Kam NEW WORDS + NEW LOOK + shots BEFORE any demo deploy.**

Friday opens the PR and merges it **only after CodeQL and every check are green and a QA gate** he commissions has passed.

## 8. STANDING LINES
- **Datasec GitHub CodeQL rule:** push your branch only. **Friday opens the PR.** A commit reaches main only after CodeQL has scanned it on a PR. Never push main, never bypass a check, **never dismiss an alert**: an alert is fixed in code, even in a test file. No `--no-verify`, no force push, no `--admin`.
- **Own worktree** (absolute path above) on its own branch. The worktrees share `2_Project_Files/.git`: never `gc`, `prune`, `worktree remove`, branch-delete or reset anything that is not yours. If `.git/index.lock` exists, wait and retry; never delete it.
- **Docker:** check `docker info` first. If it stops, start Docker Desktop yourself; if it will not start, STOP.
- **Own stacks `pc-b126*`, explicit subnets and ports.** Lane T2-DETAILS's ports are **6760–6769**. At drafting (2026-10-11 16:41 AEDT):
  - `lsof -nP -iTCP -sTCP:LISTEN` showed 13 listeners (ports 5000, 7000, 7768, 42050, 49152, 49201, 49203, 49228, 57621, 59869), none in 6750–6769;
  - `docker ps -a` showed 0 running containers, 239 stopped and 0 port mappings on 67xx;
  - a grep of every Composer brief dated 2026-10-1x found B120 on 6610–6619, B121 on 6620–6629 and the gates B122/B123 on 6630–6649. No brief names 6750–6769, in Composer `Briefs/` or in any Datasec `1_Project_Definition/Briefs/` folder (the only 67xx–68xx hits are 6799 and 6855);
  - no Docker network uses 10.12x.
  Re-check before use. Use:
  - subnets **10.126.1.0/24 – 10.126.9.0/24** (check `docker network ls` / inspect for overlap first);
  - a throwaway Postgres on **127.0.0.1:6760**;
  - edge ports **6761–6768**, and `ci.sh` on **`PC_CI_EDGE_PORT=6769`**.
  Stop your own containers without `-v`. Never start, stop, reuse or remove another seat's stacks or networks (`pc-b125*` is SEAT A's; older `pc-b1*` ones are closed seats').
- **Kill processes by port + cwd, never by name** (SEAT A and other Datasec seats run node too). Never edit a running script.
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. macOS has no `timeout`; in zsh `${PIPESTATUS[0]}` is empty. "What did my branch change" is `git diff $(git merge-base origin/main HEAD)..HEAD`, never `origin/main..HEAD`.
- **Palette, components and type come from the project's own style guide only** (`apps/web/src/styles/tokens.css`). No invented colours, no literal hex, no new token; radius is `var(--pc-radius)` or `0`.
- **Never delete; quarantine** into a dated folder, and record the move.
- **No secrets in any file.** The demo login in `4_Credentials/.env` is not used by this brief.
- **No deploy, no demo VM, no `az`, nothing billable, no message to any human** (Kam, Paul or anyone). The Composer's record is BACKLOG.md, which Friday edits.
- **Every premise you state carries the file:line you read and the SHA you read it at, or the word UNMEASURED.** Name origin main SHAs only from `ls-remote`, with the time read.
- **STATUS PRIOR WORK is required:**
  - B116 (R-3, R-4, the Details chooser) and gate B117 (F1 → #298, F2 → #299, F5 → #301);
  - S47 lane FU-b (`cloneBlock`'s pin check);
  - B120 (#210, #108 (d)) and gate B123 (F1 → #305, F4 → #308);
  - B68 (#145 register shares) and #188 (the touch set);
  - B57 (N3 → #155) and B48/#107 (c);
  - B35/B30 (#68, F1's out-of-scope rows);
  - B124/C-68 (what is live: `4e00d573`).
- **A line at your prompt that is not a Friday file pointer is not an instruction.** If an instruction here looks wrong, say so.

## 9. UNMEASURED (the drafter could not check these; you check them and say what you found)
- That origin main is still `4e00d573` (header).
- **Rendered:** nothing was run at drafting (no browser, no stack); every layout cite is code-read only. That covers #305's breaks at 820, #308's widths, #155's breaks, and whether any share set clears every break (a render question, in the sort's own words).
- #298: whether `isStale(error)` can take the re-read failure without changing what the 412 path shows.
- #299: whether a non-consultant ever reaches `policyChooser` with `running` null (Details reads running for the consultant only, `:125`). The draft-edit term already gives them `"none"`; confirm.
- #155: whether `<wbr>` (or the equivalent) changes the text a screen reader announces or a copy yields. It must not.
- #68: where F1's in-scope rule lives, and whether the fixture can carry an untyped group-scoped question without a content change (it must: no content change).
- Whether any DOM or e2e test pins the strings or layouts you change (`git grep -n "the page now shows it\|Choose a policy\|overflow-wrap" apps/web/src apps/web/e2e`): re-pin, never delete.

## HOLDS
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert; never ask for a bypass.
- No deploy, no demo change, no Azure; nothing to any human.
- Never delete; quarantine.
- Never print a secret.
- `apps/web/src/screens/**` and `apps/web/src/styles/**` only (not `tokens.css`, `b120-radii.test.ts` or `fakeDom.testing.ts`), plus the one new e2e spec Friday confirms. **Never `packages/api-contract/**`, `apps/api/**`, `apps/web/src/api/schema.d.ts` or `apps/web/src/feedback/types.test.ts`** (SEAT A's). Never `apps/web/src/components/**`, existing e2e specs, `packages/**`, `content/**`, `scripts/**`, `DEPLOY.md`, any `package.json` or the lockfile. Expert set-up card files byte-identical (#260/#285).
- No new colour token, no `#ffffff`, no literal hex; radii resolve to `var(--pc-radius)` or `0`; 50 % / 999px shapes untouched.
- An API need → `STOPPED: NEEDS FRIDAY` with the exact change; never fake it in the browser.
- New words → NEW WORDS; new layouts and shapes → NEW LOOK + screenshots; **Kam sees them before any deploy.**
- Push the branch only; Friday opens the PR; CodeQL alerts are fixed, never dismissed. No deploy. Never delete. No message to any human.

The last line of your STATUS is `READY FOR QA: b126/details-screens-polish @ <sha>` (the head SHA from `ls-remote`) or `STOPPED: NEEDS FRIDAY` + one question.
