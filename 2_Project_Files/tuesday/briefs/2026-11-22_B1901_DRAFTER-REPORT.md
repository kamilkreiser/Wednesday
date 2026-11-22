STARTABLE: M-V YES, M-P YES (M-P only after Tuesday's S5 answer to the STOP-class Q1; the kit refuses to launch without it)

# B1901 DRAFTER REPORT (Sonnet, in-session, read-only), 2026-11-22 17:22 to 17:56 AEDT

Commission: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1901_MPS-LANES-MV-MP_DRAFTER_COMMISSION.md`. Routing row C8 (`model-routing.md:98`), `model: sonnet`. Scratch and prototypes: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s309/d1901/` (a tarball extraction of main `ec281cfb`, not a `git clone`: `gh api -X GET .../tarball/<sha>`, the form B1895 used; so no push URL exists to set).

## BLUF
- Two stampable kits, both `stamp_check.py <kit>` exit 0 (M-V 123 claims, M-P 160 claims, each with a sidecar line; 44 and 47 of those lines are measured by a real count or command, the rest read "UNMEASURED by design: a command, word, name or format the seat writes or runs", the B1895 precedent):
  - **M-V** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1901_SEAT-M174_mps-autosave-gap-cells.md` (seat `Datasec/MPS-M174`, MPSCALC-429): two cells, G15 and G16, in `QuoteScreen.autosave.test.tsx`. Prototype: 30 cells to 32, whole vitest 149 files / 1736 tests green, eslint and `tsc -b` rc 0, six red-table labels MATCH.
  - **M-P** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1901_SEAT-M175_mps-proposal-part-codes.md` (seat `Datasec/MPS-M175`, MPSCALC-427 and 428): one CSS rule, one new Chrome-print spec, one config name, and the no-price check's three gaps. Prototype: whole vitest 149 / 1740 green, `eslint .` and `tsc -b` rc 0, the whole api-off Playwright step 162 passed (2.5 min), red tables 6 + 5 labels MATCH.
- Main moved since the sweep: `9c9a7219` to `ec281cfb` (PR 226, the infra tests and the validate.sh comment, 2 files under `infra/`). All four web blobs the sweep printed are unchanged at `ec281cfb`.
- **Four findings Tuesday should read before stamping** (each is in the kit and in the Questions below):
  1. **427's "Chrome scales the whole PDF down" is NOT reproduced by `page.pdf`.** What is reproduced: with a 60-character unbroken code the first row of stream cards goes from 297 px + 297 px to 469 px + 125 px and the page count from 12 to 13; median word height stays 9.493 pt in both (no scale). The review's `window.print` path is unmeasured here.
  2. **The ticket's example rule `overflow-wrap: break-word` does not fix it** (still 469 + 125, 13 pages). `overflow-wrap: anywhere` does (297 + 297, 12 pages). The kit's red table has a `break-word` label that stays red.
  3. **The PDF check cannot live under `web/src/proposal/**`.** It needs one new file `web/e2e/proposal-long-code.spec.ts` and one name in `web/playwright.config.ts` `STUB_OFF_ONLY` (otherwise CI's stub-off step never matches it). It must not call `pdftotext`: `web/src/test/pdftotextTimeout.test.ts` pins a census of exactly four spec files with a `pdftotext` call.
  4. **429:** the existing cell G5 already goes red under the "do not clear the running timer" change at base (1 failed), so the ticket's "only a cell that counts timers" is true but G5 is such a cell; and both new cells are red under the "explicit save arms no gap" change. Both overlaps are named in the kit (Q2), not hidden.

## 427 and the product owner (the commission's ask)
The rule is a byte of the stylesheet of the document a customer receives, so it is a product byte a customer's page can show, but it changes layout only when a code cannot fit its card: no word, no figure. Measured by program, before and after the rule: priced S4 document 13 pages, `pdftotext -layout` text equal, `pdftoppm -r 40` pictures equal; unpriced seven-package document with a short code 12 pages, text equal, pictures equal. No clarification names a style rule as the owner's (`CLARIFICATIONS.md` counts: `overflow-wrap` 0, `long code` 0, read at 17:2x while the records seat was writing it); the one layout-only precedent, C-27 (home tiles, 2026-10-13), was put to him as a choice among options. The ticket itself says "This ticket changes no word and no priced document; it is a style change with its own independent review". So it is **STOP-class Q1 in the M-P kit with Tuesday's default** (build, gate G1, rendered before/after pages for Tuesday); the kit REFUSES if S5 does not carry the answer.

## PRIOR WORK (what existed and why)
- Instruments: `/usr/bin/grep -c -F` over the root records and the pickup, `gh api -X GET --paginate` over all 226 pull requests (title, head ref, body; saved as `scratch/allprs.jsonl`), `matching-refs`, `ls` of the briefs folder and the project `.tools`.
- MPSCALC-427, 428, 429 (Jira GET, whole, 2026-11-22 17:22:52): each Backlog, 0 comments, 0 links, last updated 2026-11-20 (17:53, 17:54, 20:18). Filed by records passes from the independent reviews of MPS #222 (427, 428) and MPS #223 (429). Root records: `CLARIFICATIONS.md` names 427 and 428 twice each and 429 once ("stay as they are", "filed"); `BACKLOG.md` rows `[B1781-OWED-1]` and `[B1800-OWED-1]`; `JIRA.md` 2 each; `history.md` 1 each. All say filed, owed. Pickup: the sweep's own check (427 two hits, 429 one, 428 none; all "filed").
- Pull requests naming any of the three keys: 0 of 226 (control: `MPSCALC-418` finds PR 224). Branches `b1901*`: 0 (control: `heads/b1790` 1). No B-number kit builds them: B1875 (held; MPSCALC-422/423, read NO LONGER TRUE at `28d8d31b`) is the sibling follow-up on the same oracle and is not this lane's; B1895 built 430 to 433 (PR 226 landed); B1897 is the live-then-gone records seat.
- Does main already do it: no. `G15`, `G16`, `saveDraftNow` 0 in the autosave test; `overflow-wrap` 0 in `proposal.css`; `proposal-long-code` 0 in the config and no such spec; `noMark`, `MPSCALC-428`, `split across` 0 in `unpriced.test.tsx` (controls: `G14` 1, `pd-card` 5, `oracle P` 3).

## FACTS RE-MEASURED (instrument; control)
| fact | instrument | control |
|---|---|---|
| main `ec281cfb35a1356d59e23e1c69e8eab1e1852f2e` (17:22 and 17:42); open PRs 0; `compare 9c9a7219...ec281cfb` 2 files, both `infra/` | `gh api -X GET` under the project `GH_CONFIG_DIR` (`gh auth status` Datasec account) | the same call returned `9c9a7219` as the sweep's base in the kit text |
| blobs at `ec281cfb`: autosave test `940d8cdf`, `QuoteScreen.tsx` `5c95b667`, `unpriced.test.tsx` `eb3f7e7b`, `proposal.css` `7e326056`, `ProposalDocument.tsx` `df4b6bb9`, `playwright.config.ts` `a7ba5b0a` | `git hash-object` over the tarball extraction | the first five equal the sweep's and the tickets' blobs |
| line pointers (`armGap` 240, call 268, `scanText` 112, `stripCodes` 185, `Cards` 112, `.pd-card` rules 67 to 71, `STUB_OFF_ONLY` 17 ...) | `grep -n` / `awk NR==n` over the raw files at `ec281cfb` | each printed its own text |
| test counts: autosave test 30 cells (indented `^[[:space:]]+it\(`; column-1 0); `unpriced.test.tsx` 88 vitest tests, 79 `it(` lines | `grep -c -E`, `vitest run` | column-1 pattern 0 in both |
| whole vitest at head: M-V 1736, M-P 1740; base DERIVED 1734 | `vitest run` in the prototype copies (`npm ci --prefer-offline`, node 24.22.2) | first run failed 1 test for lack of `docs/` in my copy (a missing fixture of the copy, not of the change); fixed by copying `docs/`, rerun green |
| api-off Playwright step 162 passed at head; `--list` stub 277 tests / 19 files, 0 lines naming the new spec; api-off 162 / 9 files, 1 line | `npx playwright test` with `MPSCALC_E2E_MODE=api-off`, `--list` | stub list has the same total with the spec ignored |
| Chrome 157.0.8103.39; poppler 26.11.0; gitleaks 8.30.1; node `v24.22.2`, npm `11.19.1` | `--version` | |
| red tables: `red429.py` 6 labels, `red428.py` 6, `red427.py` 5, all MATCH | the scripts as embedded in the kits (byte equality of every embedded block against the tested file checked by program: 3 of 3 and 8 of 8 EQUAL) | each table holds a label that must be red (`base-m2`, `cells-only`, `no-rule`) and fired |
| `lengths.py` prints lengths only | run on a SYNTHETIC file: `count 4 | min 2 | max 18 | length:count 2:1 3:1 10:1 18:1`, `object keys holding a digit: count 1`; 0 of 7 planted strings in its output | the planted price and codes are absent from the output |
| ports `9980-9989` free (0 listeners); no 2026-11-21 or 2026-11-22 SEAT kit names a port of that block (word-boundary scan of the non-`.pre-` kits) | `lsof -nP -iTCP:9980-9989 -sTCP:LISTEN`, scan | the scan found `5000` in two OXPd kits (control fired) |
| panes: no `Datasec/MPS-` pane at 17:43 (R295 was live at 17:22) | `tmux list-panes -a -F` | one pane named `tuesday` |
| git identity: repo email 29 bytes with newline, name 12; `core.sshCommand` names `/Volumes/Laptop-DEV` once; deploy key present (2 files) | `git config --local --get`, `ls` (values never printed) | |

## CHAIN INPUTS (rule 4: each input comes from an earlier step or exists at BASE)
| kit, step | inputs | from |
|---|---|---|
| M-V 2 baseline | clone, `node_modules` | Step 1 (`npm ci --prefer-offline`, itself in Step 2) |
| M-V 5 edit, red table | `apply_edits.py`, `red429.py`, base tree | the kit; Step 1 `git archive` |
| M-V 6 checks | `scans1901.py`, canary file | the kit; scratch |
| M-P 2 lengths | `lengths.py`, the project's `.local/pricebooks/catalogue-map.json` | the kit; exists at the project (gitignored, not in the clone) |
| M-P 3 baseline | clone, node_modules, S7 port | Step 1; Stamp S7 |
| M-P 6 edits and red428 | two apply scripts, `red428.py`, `EDITS_PY`, base tree | the kit; Step 1 |
| M-P 7 Chrome print | `red427.py` (reads the clone, which holds the spec after Step 6), `compare427.py`, `pdfbox.py`, Chrome, poppler | Step 6; the kit; the machine (REFUSE checks them) |
| M-P 8 evidence | the PDFs of Step 7's label folders | Step 7 |
| M-P 9 checks | `scans1901.py`, all of the above | the kit |
| M-P 10 commit | the three figures of Step 2 and Step 7 | Steps 2 and 7 |

## QUESTIONS WITH DEFAULTS
M-P (the kit's own list is the authority; Tuesday's answers go in S5):
- **Q1 STOP-CLASS: is the stylesheet rule a product byte a customer sees, and the product owner's?** Default: build, gate G1 (Opus) with the rendered before/after pages of Step 8, as the commission's default. Without the answer the seat refuses.
- Q2 breadth of the rule: default `overflow-wrap: anywhere` on `.pd-card .pd-bullets li` only; alternatives `min-width: 0` on `.pd-card` (UNMEASURED) or scoped to the unpriced option.
- Q3 where the PDF check lives: default new spec + one config name (the lane grows by two paths, disjoint from every other lane); alternative method and figures in the commit body only.
- Q4 text size / print path: default pin cause and page count, print text size as evidence only; `window.print` UNMEASURED.
- Q5 page-count equality is fixture-dependent: default the frozen seven three-line packages (12 = 12). With the four-line package the long code adds a page (14 against 15, measured once, rule present). Hosted fonts differ; the first hosted run is the unmeasured one.
- Q6 header sentence of `unpriced.test.tsx` (default: one added sentence); Q7 six cells N1 to N5 + control (default); Q8 one commit; Q9 gate G1; Q10 level sonnet (row C2); Q11 seat prints counts.
M-V: Q1 two cells at the end of the gap describe; Q2 keep both cells as run (G15 behaviour, G16 timer count; shared red under the first change, overlap with G5 under the second); Q3 the title of G15 names `GAP`; Q4 one commit; Q5 gate G2; Q6 level sonnet (C2); Q7 counts.
Both: weekend grant `WED_USAGE_STOP=100` is written in the launch line with the note that it lapses at the end of Sunday 2026-11-22. Gate tiers: M-V G2 (`model-routing.md:109`), M-P G1 (`:108`). Heavy rule: B1790's two-slot lock and load1 under 24, carried (I did NOT take the project's lock: writing it is a write in the project tree, outside my fences).

## UNMEASURED
- The real catalogue part-code lengths (the pricebook store was never opened by me; the program ran on a synthetic file only).
- The review's `window.print` shrink (14 to 13 to 12 pages), the one-pager's detail cell with a long code, hosted CI (a different font set; the new spec's page-count equality on the hosted runner), the whole stub step, `npm audit` and the production build at head (not run by me; the kit asks the seat to run them), `gitleaks git` (the kit forbids the whole-history run, B1895 measured 9449 old findings).
- Heavy lock and load gate: the seat's locks `.tools/.heavy-lock-1/-2` are the carried rule, not re-checked; load limit 24 carried, not re-checked (my own runs saw load1 3.3 to 9.4).
- The base figures `1734` (whole vitest), `161 passed / 8 files` (api-off) and `Total: 161 tests in 8 files` are DERIVED from head minus the new tests, marked so; the stub step's `260 passed / 17 skipped` is RELAYED from B1790's gate and marked so.
- 44 of 123 (M-V) and 47 of 160 (M-P) sidecar lines are measured by a real count or command; the others are the "by design" form. The sidecar was written by a helper of mine (`scratch/fill_sidecar.py`); Tuesday's five-line spot check should include at least one `awk NR==` pointer and one `Tests` line.

## BYTES AND READ LOAD (counted by program)
| kit | kit bytes | read load of the seat (kit + CLAUDE.md + named ranges) |
|---|---|---|
| M-V | 54032 | 89536 bytes (kit 54032; project `CLAUDE.md` 8103; autosave test 21756; `QuoteScreen.tsx` three ranges 4502; `autosave.ts` 1 to 21, 1143) |
| M-P | 95777 | 130818 bytes (kit 95777; `CLAUDE.md` 8103; `proposal.css` 66 to 72, 615; `ProposalDocument.tsx` three ranges 1714; `unpriced.test.tsx` four ranges 13927; `playwright.config.ts` 3041; `proposal-purchase.spec.ts` 4609; `pdftotextTimeout.test.ts` 3032) |
Sidecars: `.measured` beside each kit (M-V 18054 bytes, M-P about 22000). The M-P kit is long because it carries eight code blocks (two apply scripts, two red tables, `lengths.py`, two evidence scripts, `scans1901.py`); the seat copies them, never retypes them.

## OUTSIDE-THE-FENCES DISCLOSURE
- Wrote only: the two kits and sidecars, this report, and scratch under `fleet/state/s309/d1901/` (tarball, prototypes `proto_v`, `proto_p`, `proto_check`, `base_p`, scripts, logs, PDFs, red-table outputs, a `build/` folder of kit templates). No git write anywhere (none run), no Jira or GitHub write, no message, nothing deleted (one `rm -f` of my own PDFs was refused by the no-delete hook and not retried; the files were simply overwritten by later runs).
- Read in the project: `git --no-optional-locks status`, `config --get` (values never printed), `ls` of `.tools` and `3_Access_Keys`, `CLAUDE.md`, `SETUP_RUNBOOK.md`, counted searches of `CLARIFICATIONS.md`, `BACKLOG.md`, `JIRA.md`, `history.md` (the records seat R295 was modifying these files at the time; I touched none). `2_Project_Files/.local/` and `Source_Documents/` were never opened. The project tree shows `history.md`, `BACKLOG.md`, `JIRA.md` modified: those are R295's, not mine (`git status` of `2_Project_Files` printed 0 lines).
- Network: `gh api -X GET` (account, refs, PR list, compare, tarball), Jira GET through my own helper `scratch/jget.py` (credentials read in-process, never printed), and `npm ci --prefer-offline` inside two scratch copies (273 packages from the machine cache in 1 s). Loopback only otherwise: Vite on ports 5997 and 9981 started by Playwright for my runs, Chrome driven by Playwright; both ports were checked at 0 listeners afterwards and no vite, playwright or vitest process remains.
- One slip: I typed `cd` once, inside a subshell, in the `npm ci` command (`(cd "$D/proto_v/web" ...; true)`), with no effect on the shell or any file; every other command used `env -C`. A second slip, mine: an unquoted-heredoc python snippet ran backticks through the shell (`command not found: 1250.50` printed twice) and its edit did not apply; I redid it with the Edit tool.
- Not run: dotnet, `az`, docker, ssh, any hosted call; no heavy-lock taken (see above); `gitleaks`, `npm audit`, the production build and the whole stub step were not run by me (the kits ask the seats).
- Other agents' files (B1898, B1899, B1900, the live R295) were not read or touched; the only other briefs I read were B1895 (the form), B1790 and B1875 (toolchain and heavy rules, a sibling follow-up), the sweep and `DRAFTER_RULES.md`.
