STARTABLE: YES (after your stamp; a filler lane, no dependency open; load1 was 6.86 at 10:41, so launch_when_cool will wait)

# B936 drafter report (2026-10-30 about 10:36 to 11:05 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B936_SEAT-H67_hpsmpoc-365-366-367-tailwind-sources-logo-tests.md` (145 lines; 9 four-underscore lines = 8 slots + the last line, by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0, control `@FOO@` reads 1; non-ASCII lines 0, control: a planted ellipsis line reads 1). Read-only everywhere else: gh `-X GET` under the project `.gh-config`, a tarball of `e21d8044` in my scratchpad, three Jira issue GETs and four JQL searches, the records repo's CLARIFICATIONS.md by `contents?ref=`, no `cd`, no hosted HTTP, no ref written, no message. Nothing was written to the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H67` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes) makes two commits on `b936/hpsmpoc-367-tailwind-sources-logo-pins` off `e21d8044`, ports 9680-9689: (1) three `@source not` lines in `globals.css` after the last `@import`; (2) `HpLogo.test.tsx` gains a frame check (ring, shadow, border, outline, inline box-shadow/border/outline) in the role-selection arm, and the three raw `PAINT.test` image lines become `paintOn`, with DOM-plant rows per image. No product byte. The proof that no product rule is lost is a rule-sequence program over the BASE, commit-1 and HEAD builds (B874's method), plus HEAD css byte-equal to commit-1 css, plus a mutant build with the exclusion removed that DOES ship the plants.

## How the gate proves no product rule was lost
`playbook-print.spec.ts` reads the BUILT css (it routes `**/*.css` and checks the print block), but it only covers the print rules. The kit's step 5 covers everything: only `equal`/`delete` opcodes BASE -> C1 (plus property/theme blocks shrinking only by variables no kept rule uses); every removed rule's class token appears as a whole token in 0 non-test scanned files (controls: `bg-white` vs `bg-white/10` in `SignInScreen.tsx` must read 0; `rounded-lg` must read 40+; a planted product file must make it fail); HEAD css sha256 = C1 css; a MUT build without the exclusion ships the plants. The gate re-runs that program from the evidence CSS copies. No e2e uses screenshot baselines (grep 0), so sibling screenshots cannot fail; a lost product rule would show in the program first.

## Sweep and lane-block pointers found WRONG or incomplete
1. **"after line 1"** (sweep seed): lines 2-3 are also `@import`s, and an `@import` after another statement is invalid CSS. The kit puts the lines after line 3 (D-1).
2. **History pointer:** the PR #240 kits and gates (B885, B900, B903, B908) do not hold the -365/-366/-367 findings (grep: none). The sources are gate B868 (PR #238) STATUS lines 92-95 and 156-157, and deploy seat B874 STATUS line 67 with `B874_evidence/css_additive_proof.txt`; C-223 is item 6 at records CLARIFICATIONS line 4653 ff.
3. **C-223's 34 rules** were measured at `c00e2828`; `e21d8044` has 210 test files (C-223: 199), so the test-only rule count now is UNMEASURED and may be higher.
4. **Hidden readers of `globals.css` source:** five unit tests (print-rules, AppShell.sidebar, ClientFollowUpScreen, contrast, UatStartScreen.layout). None counts lines or reads line 1; all must pass unchanged.

## Q-questions for Tuesday (each with my default)
- Q-1 (D-1): `@source not` lines after line 3, in `globals.css` only? Default **YES**.
- Q-2 (D-2): exclude only `*.test.ts(x)` and `web/e2e` (test-data modules stay scanned)? Default **YES** (the ticket's words; can only keep rules).
- Q-3 (D-3): make both inline-style patterns case-insensitive? Default **YES**.
- Q-4 (D-4): meet -365 with red unit rows rather than a comment naming the browser spec? Default **YES**.
- Q-5 (D-5): no new file (no committed source guard for the `@source` lines)? Default **YES**.
- Q-6: gate round. Default round 1 of 2 on class "Tailwind source exclusion and logo-test pins, config and tests only".
- Q-7 (D-7): target READY 150, hard stop 225 minutes? Default YES (four production builds under load).

## Stamp slots (my defaults)
STAMP: D-1 to D-7 accepted, Q-1 to Q-7 as defaults. KEYS: HPSMPOC-367, HPSMPOC-365, HPSMPOC-366. LAUNCH WINDOW: from stamp until 18:00 AEDT 2026-10-30 through launch_when_cool below load1 7, with the live HPSM-POC panes named. Stamped by: the Tuesday seat that read kit and report. Launch authority: the 2026-10-30 10:07:23 instruction, 2026-10-29 10:05:10 commission, 2026-10-16 grant, 2026-09-13 as-many-agents rule, 2026-10-24 standing order, 2026-10-22 Sonnet-first grant. Hard stop / target: 225 / 150 minutes after Step 0. Head and main: `e21d8044` with no `b936/*` ref, or what moved (the kit's main-moved list names the files that would stop it). Model receipt: the line in the guidance plus load1.

## Reasons not to launch now
None blocking. Load1 6.86 at 10:41 with four HPSM-POC seats live: the seat will wait on its heavy lock. After this lands, every sibling's build drops its test-only rules; a sibling class written only in a test file stops shipping (the ticket's intent; the kit puts this under FOR TUESDAY).

## UNMEASURED
Unit and e2e counts at main; the test-only rule list at `e21d8044`; whether Tailwind 4.3.3 resolves these `@source not` globs as written (the build decides); the CSS chunk names; Chromium; build times under load.
