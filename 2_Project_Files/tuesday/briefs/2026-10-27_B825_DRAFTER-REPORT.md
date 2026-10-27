STARTABLE: YES (after Tuesday stamps the 8 slots; Q-1 to Q-4 each have a default, none blocks)

# B825 DRAFTER REPORT: HPSM-POC chooser logo keyline (SEAT-H46)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B825_SEAT-H46_hpsmpoc-chooser-logo-keyline.md` (112 lines; 8 lines match four underscores, control: 7 slots + last line). Drafted 13:3x-13:4x AEDT, 27 Oct, Sonnet 5.5, template B797 read whole.

## BLUF
The chooser's logo is `HpMark` (asset `hp-mark.png`, opaque near-white background) wrapped in `<div className="rounded-lg bg-surface p-3">` at `UatStartScreen.tsx` line 72 (main `271f6932`). That is the white tile on the grey page. `HpMark` and the tile are SHARED with `SignInScreen.tsx` (lines 54, 124), so the kit adds a NEW asset (`hp-mark-keyline.png`) and a NEW export for the chooser only, and removes the tile on the chooser only. Headers (`HpLogo`) and sign-in pages untouched. The supplied file really is transparent outside the circle, so no tile is needed.

## Facts re-measured (instrument, control)
- Attached PNG: sha256 `d24bc18cab6cb8ac9ecad042d1950c4e42f6f19581420f53d35c2cd8ad579c2b` (`shasum`), 172,789 bytes (`ls`), 3000 x 3000 8-bit RGBA colour type 6 (`sips` AND a raw IHDR read agree), chunks IHDR/tEXt/IDAT/IEND. Full decode with my own `python3 -I` zlib un-filter (no PIL/numpy here): row filters 2336 Up + 631 Sub + 33 Paeth = 3000 rows (control: the sum is 3000). Census over 9,000,000 px: alpha 0 = 21.37 %, alpha 255 = 78.53 %, partial 0.10 % (pi/4 = 78.54 %, as a radius-1500 circle predicts). Corners (0,0,0,0): outside the circle is transparent. White keyline ring 110 px wide on row 1500 (3.7 % of the diameter), touching the canvas edge at the compass points; fill blue (2,74,216). The ring will show as a thin white ring on the grey page: by design, the kit says so.
- Main at origin: `271f69328c8506c38243066a2853d9eee2ed9e0f` (`git ls-remote`), not the B797 `d415a3fe`. No open PRs (`gh api -X GET pulls?state=open`), no `refs/heads/b825*`.
- `hp-mark.png` 215 x 214 RGBA sha `ac74d709...dad1`. Pin traps found by reading `HpLogo.test.tsx` (R2 helper pins `rounded-lg bg-surface p-3` for the chooser and both sign-in renders), `HpLogo.proxy.test.tsx` (src mapping, 215x214), `web/e2e/logon-logo-top.ts` (`MARK_WIDTH = 215`, four viewport cells, "only image", top <= 200, block <= 40 from main, centred 2 px), `LogonLogoTop.test.tsx` (stays green). The kit names each and says how to change it.
- Dark mode: `gh api` code search for `prefers-color-scheme` in `web/src` returned nothing; tree has no `dark` path; control: a search for `UatStartScreen` returned 5 files. Kit says re-measure and shoot dark only if it exists.
- Model: `model-routing.md` row C2 line 92 (Sonnet 1st); id `claude-sonnet-5-5` at `models_latest.json` line 23; launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Landing rule: `CLARIFICATIONS.md` line 138 precedent ("PR #27 (B23) squash-merged head-pinned ..."), copied from B797 which quoted it; I grep-read the line in the project file: the only squash/head-pinned line there. Project `CLAUDE.md` has no squash line (RELAYED from B797, not re-read).
- Ports: `lsof -nP -iTCP:7650-7659 -sTCP:LISTEN | wc -l` = 0 (read twice). Word-boundary scan of non-`.pre-` SEAT kits of 26/27 Oct for `765N`: ONE hit, B823 (NexusAI M22), whose text only says it scanned "also 7630-7659" (it owns 7640-7649): not an assignment. The scan's own positive control (my first regex matched that file) fired. Live panes 13:39: tuesday, Security-Composer-J26, MPS-M47, MPS-M44, MPS-M40, NexusAI-M21, fleet-monitor.
- Seat name: highest HPSM-POC builder kit is H45 (B814); `H46` appears in no kit (grep count 0) and no pane. Chose H46.

## D-decisions (in the kit)
D-1 chooser only. D-2 use the supplied file byte for byte, no downscale. D-3 Sonnet, tier-2 gate. D-4 keep the outer wrapper and heights so position pins hold.

## Q-questions for Tuesday (each with a default)
- Q-1: Should the two sign-in pages (mock picker, Entra) get the same keyline circle? Default NO: he said "the initial screen (selection of roles)"; they keep the tile. If yes, a follow-up kit (the E2E MARK_WIDTH pin and the R2 rows change again).
- Q-2: A 3000 x 3000, 172 KB PNG for a 96-128 px display. Default: ship the exact file (project convention, one asset to approve). Alternative: a derived downscale (needs his OK as a second asset).
- Q-3: Times. Default READY-by 14:30 AEDT, hard stop 15:30 AEDT (builder lanes ran about 1.5 h).
- Q-4: Dark theme: default light only if the seat's grep confirms none (my search says none).

## UNMEASURED
No npm, build, test, browser or screenshot run. Web suite counts at main; how a loopback server serves the chooser (UAT/open sign-in env on the seat's own process; kit tells the seat to find it in `config.ts`/e2e config and STOP-ask if it cannot); Playwright availability; which e2e spec calls `expectLogoAtTop` for the chooser; how the 110 px white ring looks at 96 px; I did not view the sign-in tile code beyond grep lines. PR #232 content was not read directly; I used B810's STATUS and the file at main.

## Outside-the-fences disclosure
Read-only only: files read under `0_Brain/reference/2026-10-27_hpsmpoc-chooser-logo/`, the project's `1_Project_Definition/Briefs/` (B810 STATUS, evidence screenshot), `CLARIFICATIONS.md` grep, `.tools/b198`/`b267` directory listings. `gh` only `-X GET` with the project `GH_CONFIG_DIR` (code search, contents, commits, pulls). Wrote scratch files (decoder, fetched sources, a copy of `hp-mark.png`) ONLY in the session scratchpad. First Bash call attempted a `cd`, which the hook refused; no effect. No decision-queue, no Jira, no ledger or WEDNESDAY/FRIDAY tree, no fleet/briefs_staged, no hosted HTTP, no az/ssh/docker, no Artifact/Docs/mail tool. The kit text carries no person's name and no card id.
