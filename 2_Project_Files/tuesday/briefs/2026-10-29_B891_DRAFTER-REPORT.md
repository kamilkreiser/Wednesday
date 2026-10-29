STARTABLE: YES, after the stamp (pins hold at 12:40 AEDT: main c00e28284e9acacf16462ea3c2b533936b3db210, 0 open PRs, no b891 ref, ports 9790-9799 have 0 listeners, pane Datasec/HPSM-POC-H53 free).

# B891 DRAFTER REPORT (builder kit for Datasec/HPSM-POC-H53: v1.2 design lane L1, ticket T05 = HPSMPOC-371, shared components restyle and a Previous link)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B891_SEAT-H53_hpsmpoc-v12-shared-primitives-restyle.md` (152 lines; long lines). Shape: the stamped L0 kit (B885, 167 lines). Read-only everywhere except the kit and this report: `gh api -X GET` under the project's GH_CONFIG_DIR (commits, pulls, matching-refs, compare, tarball of c00e2828 into the scratchpad `b891/`), Jira GET of HPSMPOC-371 through `.tools/b649/jira.py`, `python3 -I` reads of the design CSS, `lsof`, `tmux list-panes`. No git command inside `!CODING`.

## Decisions asked of Tuesday (defaults apply if silent)
- **Base: (A), branch off main c00e2828 and touch no token file.** The restyle needs no new token: every utility it uses resolves to an existing token. The L0 first commit (head 2d554ce5, ahead 1 behind 0) changes `globals.css`, `contrast.ts`, `tokens.css` only, and those are sidebar-only `--ds-nav-*`. (A) keeps the sets provably disjoint (kit REFUSE has the `compare` intersection, expected `shared = 0`), so L1 lands before or after L0 with no ordering and no rebase. (B) would carry L0's commit or wait for it and recompute: no benefit. A needed new colour or `TOKEN_PAIRS` row is a STOP-shaped question to Tuesday.
- **NextStep.tsx: L1 keeps it.** From L1's side: the ticket and the delta's section 5 give it to L1. From L0's side: the B885 kit names in the shell folder only AppShell, GlobalNav, Sidebar, CustomerPicker, shell-flags, customer-nav and its named shell tests; NextStep is not named, no NextStep test exists at main, and the compare shows 3 files. Tuesday should add one line to L0's watch: "L0 never edits shell/NextStep.tsx".

## Q-questions
- Q-1 Base A (above). Q-2 Metrics also gets Previous (the design shows Previous on every step but the first; the ticket's "2 to 8" is silent on Metrics). Default yes.
- Q-3 Three of 15 NextStep mounts are conditional (Narrative x2 on approval, Overview on `held`): Previous would be hidden on an unapproved Narrative. Default: new optional prop `showNext` (default true); the Narrative and Overview page lanes pass `showNext={approved}` in their own PRs. AC 5 is partly met on that one state until then.
- Q-4 One new e2e file `web/e2e/step-previous.spec.ts` (outside the ticket's file list, disjoint from L0). Default yes.
- Q-5 No shared table or progress primitive exists in the file set: new `ui/Table.tsx` (class constants plus a scroll wrapper) and `ui/Progress.tsx`, adopted by the page lanes later. Default yes.
- Q-6 Gate: tier 2 (row G2 line 109), round 1 of 2 on the new class "shared component restyle". Ports 9790-9799, pane H53, target READY 240 min, hard stop 360.
- Q-7 Previous is a link (ButtonLink look), text "Previous: <label>", before Next in DOM order, wrapper stays a div (no new landmark).

## Corrections to the ticket and the delta (all in the kit)
1. NextStep.tsx sits in L0's folder (resolved above).
2. AC 2 "every new colour pair added" would mean editing `contrast.ts`, which L0 owns and already edits: this lane adds no pair; a pair outside TOKEN_PAIRS (fg-muted or primary on surface-sunken) is proved in the lane's own new test via imports.
3. "Depends HPSMPOC-368 sidebar tokens": nothing in L1 reads a `--ds-nav-*` token.
4. AC 5 numbering: JOURNEY has 10 entries, Profile is step 1 (index 1), Overview is not a step; rule is Previous on every entry after Profile.
5. "tables, progress bar": the file set has no shared ones; the only table is `partner/parts.tsx` line 140 and the three bars are separate.
6. Structure pins found: eyebrow is `h1.previousElementSibling` and tags are `nextElementSibling` (AttributionPreviewScreen.test 141-142); StatTile `dt` parent is the tile (two tests); `States.test` compares outer HTML (States.tsx untouched).
7. Tailwind radius: only sm, md, lg map to tokens; rounded-xl would fall outside the tokens.

## Unmeasured
No worktree, build, browser or test was run. Counts at main, Chromium, rendered look, whether `keyboard.spec` and `playbook-print.spec` stay green with one more Tab stop, how two "Previous" controls read together on the Assessment step, the contrast of any pair outside TOKEN_PAIRS. The ports scan found 9790-9799 named only as "free decades" in a gate kit, never as a seat block.

## Hygiene by program
Four-underscore lines 9 (control: scratch file 1 in the L0 pattern); at-sign tokens 0; non-ASCII bytes 0 after a fix; person-name patterns 0 after a fix; `WED_USAGE_STOP=100` appears 3 times; every path in the kit checked against the extracted tree (65 paths, the 17 not found are the new files the kit marks as new). Fixed during drafting: a person's account name, a b9 head count (7 not 13), two line numbers.
