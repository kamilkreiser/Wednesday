STARTABLE: YES (after the stamp; one prerequisite the seat handles itself: the shared clone does not hold main `1e3ea8a9`, so Step 1 fetches it under lock.sh)

# B759 drafter report (SEAT-H38, HPSM-POC, two-line logo and low-risk polish)
Drafted 2026-10-26 from 20:55 AEDT by the read-only kit drafter. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B759_SEAT-H38_hpsmpoc-two-line-logo-and-polish.md` (139 lines). Shape copied from B723 and B735; the B738 gate's notes N-A to N-F are the polish source.

## BLUF
- The kit builds ONE new asset, a PNG made from the product owner's own pixels: line 1 the HP mark copied 1:1 (x 52..264, y 6..217 of the supplied file, no resampling), line 2 the two supplied text runs resampled by one factor `s` in [0.45, 0.65], so it is visibly smaller. The supplied `hp-logo.png` stays byte for byte as the pinned source; `HpLogo.tsx` imports the new file.
- **Second-line text found in the asset:** `Cyber Security Services` (bold) over `Reseller Playbook` (regular), right of the blue "hp" circle. The component's alt constant is exactly `HP Cyber Security Services Reseller Playbook`; it stays unchanged (no new words).
- **PNG, not SVG:** the brand font is a system stack (`brand.css:23`, "no web-font download"), so live SVG text is not font-guaranteed; outlining would redraw glyphs. A PNG from supplied pixels is font-independent and one request.
- **HP's digital guidelines are NOT applied**: the attachment was the project's own user guide. The kit says so (D-1) and applies none.
- **Polish is thin on purpose:** P1 no EXIF/XMP in the new file (keeps the `iCCP` so the blue is unchanged), P2 opaque `#ffffff` canvas (= `--ds-surface`), P3 logon and header height classes from a closed list chosen by measured predicates. Everything else on the N-list is left out and named.
- **Performance rule:** JS raw and gzip delta <= 0, CSS <= 0, no new font, requests per page equal, logo bytes below 238,005, else STOP. To keep the JS from growing the asset stem is at most 7 characters.
- Clock: target READY 23:30 AEDT, hard stop 01:30 AEDT 27 Oct, a 23:00 smaller-change question. No deploy (a later seat does it after a gate).

## Facts re-measured (instrument, control)
- Main `1e3ea8a9c192146627eb4dd378bda05369070764`: `git ls-remote` (control: a 5-pattern call printed 9 rows). `refs/heads/b759*` none. It carries #226 (the logo, `68ebdbf7`) and API-only commits after it. `1e3ea8a9` is NOT in the shared clone (`git cat-file` failed): I read origin through `gh api -X GET` raw into scratch.
- Logo file at main: sha256 `64518bb2...6b71` (equals the earlier kits), 238,005 bytes, 950 x 221 RGBA (`shasum`, `file`; control: other files hash differently).
- Pixel layout (`python3 -I` zlib reader): mark x 55..261, y 9..214; bold run y 74..139, x 295..930; regular run y 149..194, x 298..666. Chunks: iCCP (3,360 bytes, `mntr RGB`), eXIf 86, iTXt/XMP 470. Control: the file dimensions and a non-zero blue count.
- Open PRs: #222 only (one `api/` test file; `gh api pulls?state=open`, control `state=closed` printed 227, 226, 225). Shared `web/` paths 0 (counter control: `b723` branch reads 17). Live branches b739, b753, b725: web paths 0.
- CI: main's last push run `completed success`, 18 check-runs success + 1 skipped. The earlier kits' "CI paused" note no longer matches the repo.
- Ports 9360-9369: `lsof` rc 1 (nothing listening; positive control not run, left to the seat). Word-boundary scan of the 10-25/10-26 non-`.pre-` SEAT kits: 0 hits (control: `974x` scan of B735 found 4). Live panes: tuesday, fleet-monitor, MPS-M35, HPSM-POC-R49, Security-Composer-G154, MPS-M34, MPS-G153. No H38 pane.
- Model: row C2, line 92, Sonnet first; `claude-sonnet-5-5` (`models_latest.json:23`). Launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Kit hygiene: stamp-slot lines 8 (7 slots + last line), at-sign pattern 0, non-ASCII bytes 0.
- Landing rule quoted from `CLARIFICATIONS.md` line 138: squash, head-pinned.

## D-decisions (in the kit)
D-1 no HP guideline applied. D-2 PNG from supplied pixels, mark 1:1, text by one factor. D-3 line 2 is one line holding both runs; the stacked two-row block is the fallback and an evidence alternative. D-4 supplied file kept untouched and pinned; stem <= 7 chars. D-5 polish limited to P1-P3. D-6 alt unchanged. D-7 performance bar above. D-8 logon heights `h-20 sm:h-24` up to `h-24 sm:h-32` (largest that keeps all predicates and no first sign-in control newly below a fold); header `h-7 sm:h-10` unless a larger class keeps every header measurement. D-9 one commit, new ref, no PR by the seat.

## Q-questions for Tuesday (default in brackets)
- **Q-1 HP guidelines:** ask the product owner for the real guidelines file; a later round applies them. [Default: none applied, say so in the message that sends the screenshots.]
- **Q-2 What is "the second line"?** One smaller line holding both text runs [default], or the supplied two-row text block scaled down (fallback saved in evidence, one-step switch).
- **Q-3 JS delta waiver:** the dispatch said a JS delta above zero is a STOP. The URL string, a possible `blurDataURL` string and the literals could add a few bytes. [Default: STOP and ask; suggested waiver only if the diff explains every byte and it is under about 128 raw bytes.]
- **Q-4 Header size:** a two-line logo makes the mark about 20 px (phone) and 30 px (sm+) across at the current heights, and line 2 is unreadable there. [Default: keep `h-7 sm:h-10` unless a larger class keeps every header measurement; report with screenshots.]
- **Q-5 Deploy scope:** main `1e3ea8a9` has two API-only commits the deployed UAT (`68ebdbf7`) lacks. [Default: the deploy seat builds the web package from this branch and leaves the API as deployed; Tuesday decides.]
- **Q-6 Stem and mark rectangle:** confirm the 3 px margin around the circle and the stem `hp-2ln`. [Default: as written.]

## UNMEASURED
New PNG size; whether `next build` 16.4.2 prints route sizes; whether a static PNG import emits `blurDataURL`; all base page weights and JS bytes; legibility at 28/40 px and at the logon classes; whether first sign-in controls stay in view at the larger logon heights (the mock button was already below the fold at 390x844, 360x740, 1366x768); whether a narrower logo returns the 390 px header to one row; positive port control; the `two-line`/`lockup` grep over `web/`; `sips` availability beyond `/usr/bin/sips` existing; CI acceptance of a `node:zlib` PNG reader in a test.

## Disclosure (outside the fences)
- Wrote only the kit and this report. Read-only: `gh api -X GET` (pulls, compare, contents raw, commits, check-runs, actions runs) under the project's own `GH_CONFIG_DIR`; `git ls-remote` only against the shared clone; `lsof`, `tmux list-panes`, `/usr/bin/grep`, `python3 -I`. No fetch, no cd (one `cd` was typed in a draft call and the hook refused it; nothing ran).
- Downloaded raw copies of repo files into my scratch folder (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f046a545-da98-413d-a9b6-01d3656a14dd/scratchpad/b759/`), read as untrusted data. The image was opened once with the Read tool (the repo copy, not an `inbound/` file).
- Read the B738 STATUS (notes, verdict), B749 STATUS last line and addendum 2, B756 STATUS tail, other seats' kit names. Opened no decision card, no `briefs_staged`, no ledger, no scoreboard, no WEDNESDAY or FRIDAY tree; no Artifact, Docs, mail or chat tool.
