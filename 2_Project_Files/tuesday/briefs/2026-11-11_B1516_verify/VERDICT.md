GATE B1516: GO @ 9853954 on main 879facd

Why: the white is the same #ffffff everywhere (defined once, 20 sites read it), PCOMP-81 sets only font-family to the exact .pc-mono stack on the one scoped selector, every new row goes red for its stated reason when its change is removed, and the whole workspace comparison is lost 0 / changed 0 / added 30 with lint, format:check, typecheck, build and the secret scan clean.

Tier G2. Gate run 2026-11-11 about 19:58 to 20:20 AEDT. Own clone: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s269/gate1516/clone` (push URL `invalid://no-push-gate`). Evidence: `.../gate1516/runs/`, scripts `.../gate1516/scripts/`, mutants `.../gate1516/mut/`.

## Findings

| Sev | Ticket | Finding | Evidence |
|---|---|---|---|
| (none) | | No Blocker, no Major, no Minor. | |

Observations (not findings):
- O1. The new test file's header comment names "backlog rows 75, 123 and 154" and the 2026-11-11 ruling. These are row numbers, not a B-number, ticket key, seat or card id, so inside the kit's rules. (`b1516-style-leftovers.test.ts:5-6`)
- O2. The stack e2e token-conformance specs (`b49-guided-home.spec.ts:28-70`) build their allowed colour set from EVERY `--pc-*` token in `:root` (loop `name.startsWith("--pc-")`), so the new token only adds an allowed value equal to the existing white. Read, not run.

## Refs
- Branch at source: `gh api -X GET .../git/ref/heads/b1516/composer-w3b-css-ruled` = `9853954af73e7ab585980464185f88ea93fb61a4` (equals the pinned sha). Main at source = `879facda441e4f7abccec51583916804f7770789` (not moved). Merge-base of head and main = main. 3 commits, `git log` author = committer = `88359143+kamilDatasec@users.noreply.github.com` on all 3.
- Changed paths, 6 of 6 in the partition: `tokens.css` (+1), `app.css` (11 lines), `screens-w1.css` (3), `screens-w2.css` (4), `screens-w3.css` (2 lines + 1 rule + 1 comment sentence), new `b1516-style-leftovers.test.ts` (+127). `git diff --name-only` holds no `.tsx`, no `b56-withdrawn`, no `b120-radii` (count 0; control: `.css` count 5). Because main did not move, no merge-tree needed (branch is a straight descendant).
- Open PRs #91, #86, #85: 2 / 2 / 57 files, 0 style or .css paths each (control: #85 holds 46 `.ts`/`.tsx`). No PR exists for the b1516 ref.

## (1) The white
- `git diff -U0 main..head` over the five sheets, read by me line by line: every `app.css` (11), `screens-w1.css` (3), `screens-w2.css` (4), `screens-w3.css` (2) change is exactly `#ffffff` -> `var(--pc-on-primary)` on the same line with the same property; `tokens.css` gains exactly `--pc-on-primary: #ffffff;` plus a one-line comment at line 16. No radius, `50%`, `999px` or other colour line appears in the diff.
- `grep -c -i '#ffffff'`: tokens 2 (`--pc-nav-fg` line 15, unchanged; `--pc-on-primary` line 16), app 0, w1 0, w2 0, w3 0 (positive control: the same grep at main counts 11/3/4/2 per the builder and my base-sheet mutant M0 shows the literals). `--pc-nav-fg: #ffffff; /* white on the rail 12.78:1 */` is byte-identical to main.
- Computed, my own `file://` render of the real concatenated sheets (tokens, app, w1, w2, w3), base from `git show main:`, head from the clone, headless Chromium, no network: the builder's 20-probe census markup (data only) gives 31 element rows with identical color, background, radius, `::after` colours, font family and size at base and head; 20 of 20 probes show `rgb(255, 255, 255)` at both. Control: head copy with the token set to `#fefefe` reports "all equal false". (`runs/census.json`, `scripts/census.cjs`, `scripts/census-ctl.cjs`)

## (2) PCOMP-81
- The added rule is `.w3-withdrawn-list .w3-register-key { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }` (`screens-w3.css:657-659`), the exact `.pc-mono` string (`app.css:57`). Nothing else in the rule: no `word-break`, no `font-size`, no width. Plus the one comment sentence at `screens-w3.css:660-662` ("The setting's key is in the register's code-style font."). No TSX in the diff.
- `b56-withdrawn.test.tsx` 9/9 and `b120-radii.test.ts` 3/3 pass at head and base; neither is in the diff.

## (3) Red first (mutants of the sheets in `gate1516/mut/`, test run in the CI-stage image, `--network none`; `runs/mut-summary.txt`, `runs/mut-*.log`)
| Mutant | Result | Reason line |
|---|---|---|
| M0 all five sheets = main | 28 red of 30 new rows (the two green are the `--pc-nav-fg` control and the ".pc-mono has one stack" control) | `Target cannot be null or undefined` (token absent), `expected [ '#ffffff' ] to include 'var(--pc-on-primary)'`, `expected [] to deeply equal [ 'font-family' ]`, stale sentence present |
| M1 `#ffffff` back at `.pc-avatar` | 2 red: that site and "app.css holds no #ffffff" | `expected [ '#ffffff' ] to deeply equal []` |
| M5 / M6 / M7 one literal back in w1 / w2 / w3 | 2 red each: that site and that sheet's "holds no" row | same |
| M2 token line removed | 1 red: "defined as #ffffff exactly once" | `Target cannot be null or undefined` |
| M3 token defined twice | 1 red, same row | `to have a length of 1 but got 2` |
| M4 token value #fefefe | 1 red, same row | `to match /--pc-on-primary:\s*#ffffff;/` |
| M13 `--pc-nav-fg` changed to #fefefe | 1 red: rail token row | `to match /--pc-nav-fg:\s*#ffffff;/` |
| M8 withdrawn key rule removed | 2 red (stack row, "sets nothing else") | `expected [] to deeply equal [ 'font-family' ]` |
| M9 stack string one character short | 1 red: stack row | `expected [ Array(1) ] to deeply equal [ Array(1) ]` |
| M10 `word-break: break-all` added | 1 red: "sets nothing else" | `[ 'font-family', 'word-break' ] to deeply equal [ 'font-family' ]` |
| M11 `font-size: 13px` added | 1 red: same row | `[ 'font-family', 'font-size' ]` |
| M12 stale sentence put back | 1 red: sentence row | `not to contain 'not the register's monospace'` |
Every mutant reddens ONLY the new file's rows (the vitest run was styles + w3 + feedback folders, 474 rows). The existing token-conformance logic (the e2e `--pc-*` loop above) allows the new token; the unit rows that read `tokens.css` (`b120-row-hover`, `wiring.test`) stay green at head.

## (4) Checks (CI-stage image built from my clone at head, `--network none`, one job at a time under `.tools/composer-heavy.lock`, taken by mkdir with a holder file and released by moving it into my own folder; load1 8 to 19 at every take, under 24; the two reads 4 s apart are not independent)
- Whole `workspace` vitest project after `npm run build`: base (main's `apps/web/src` overlaid, new test moved aside) 2880 rows, 2878 passed, 2 red; head 2910 rows, 2908 passed, 2 red. The 2 red are the same two `packages/content/src/citations.test.ts` SOW-citation rows at both (the SOW text is not mounted). `compare.py` (mine): **lost 0, status changed 0, added 30**, all 30 in `b1516-style-leftovers.test.ts`, all passed. Controls on the comparison: one row flipped -> `status changed 1`; one dropped -> `lost 1`. (`runs/compare.txt`)
- `npm run lint` rc 0, `npm run format:check` rc 0 (prettier covers the CSS and the new test), `npm run typecheck` rc 0, `npm run build` rc 0 (`runs/chk-rc.txt`).
- `scripts/secret-scan.sh --tree` on the clone: ~12.04 MB, "no leaks found"; `--self-test` 7 of 7 PASS including the planted key flagged (`runs/secret-scan.txt`, `runs/secret-selftest.txt`).
- Message and added-line scans: ticket key / B-number / `Tuesday|Wednesday|Friday` in the 3 messages 0 and in 153 added lines 0 (control: a planted `PCOMP-1` counts 1); the workspace owner's names (underscore-aware) 0 (control `_by_kam_` fires); non-ASCII 0; trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` count 3 over 3 messages. Added lines of the five sheets that are not a declaration, selector or comment: none (program: grep -v of the allowed shapes printed nothing). Only new words: `--pc-on-primary` and CSS comments.

## (5) Computed-style claim for 81 (`runs/page-diff.json`, `scripts/page.cjs`)
I re-rendered the real `WithdrawnExceptions` and `RegisterSetting` components to markup myself (the builder's fixture test, run in my container; 5 rows incl. the builder's longest key), put the markup in `file://` pages with my own base and head CSS, and compared getComputedStyle of every element (137) over 18 properties (colour, background, border colour/width, radius, font family/size/weight, shadow, word-break, overflow-wrap, text-align, display, padding, line-height, letter-spacing, width) at 1280 and 390. Result at both widths: the ONLY differing property is `fontFamily`, on 47 elements (5 key spans + 42 `<wbr>`); at head the key's family equals the register key's `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`; no sideways scroll (scrollWidth = clientWidth at 390 and 1280). Page height: 1280 unchanged (1313 both), 390 2306 -> 2341 (+35 px, the accepted reflow: extra key lines, two cards +18 px). No width, font-size or break-rule change exists in the diff, so the accepted reflow is the only layout effect. Host `ui-monospace` is this machine's, not the deployed machine's.

## NOT RUN
- CodeQL (hosted only; Tuesday reads it on the PR).
- The stack e2e specs (`b120-expert-screen-polish`, `b126-details-polish`, `b49-guided-home`, `mobile-b49-guided-home`): they need the compose stack and the demo sign-in; not run. The token-conformance e2e reasoning is by reading only (O2).
- `scripts/ci.sh` whole (starts the stack, copies the SOW text); the SOW text was never mounted.
- The branch-by-branch census of REFUSE 6 (127 old branches ahead of main); I read the three open PRs only. A newer branch touching a style sheet would show as a merge conflict, and main has not moved.
- Re-measurement of the builder's pixel-diff programs and contrast ratios (I used computed-style equality, which is stronger for 74/80, instead). The "longest real setting key" was taken from the builder's fixture, not re-derived.
- Hosted HTTP: none contacted by me beyond `gh api` ref and PR-file GETs through the project's gh config.

## Corrections
- None to the builder's claims; every number I re-ran matched (2880 -> 2910 rows, 2 red unchanged, 47 elements, 20 of 20 sites, +35 px at 390).
- Harness note: my first attempt to copy the builder's `compare.py` was refused by the path guard (write into the project tree); I wrote my own, same logic. Nothing was written in the project folder except the lock directory taken and released per job (moved into my own folder).

## Resources
Image `pc-g1516-node:head` and containers `pc-g1516-*` removed (census: 0 each; controls 28 containers, 8 images). No port published. Lock absent at the end.
