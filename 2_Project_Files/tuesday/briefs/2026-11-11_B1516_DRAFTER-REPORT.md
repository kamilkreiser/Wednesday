STARTABLE: YES (after Tuesday's stamp; nothing is blocked at source; no Composer pane is live)

# B1516 drafter report (SEAT-C97, Datasec / Security Composer, lane W3-B)
Drafted 2026-11-11, reads 19:11:42 to 19:22:26 AEDT (`date` printed 19:11:42, 19:12:07, 19:12:18, 19:13:35, 19:14:53, 19:19:03, 19:19:47, 19:22:26). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1516_SEAT-C97_composer-w3b-css-ruled.md` (123 lines) and an identical `.pre-stamp`. Scratch: `/private/tmp/b1516-drafter/` (raw copies at main 879facda, `jira.txt`, `cmp.out`, `ahead_dates.txt`).

## BLUF
One Sonnet kit, three parts in order: **74** (new `--pc-on-primary: #ffffff` in `tokens.css`; the 11 `#ffffff` literals of `app.css` use it), **80** (the 3 + 4 literals of `screens-w1.css` and `screens-w2.css`, and by Q-1 the 2 of `screens-w3.css`), **81** (one `font-family` rule for the withdrawn list's setting key in `screens-w3.css` plus one stale comment sentence). All three are BUILD: the product owner's 14:15 ruling (`CLARIFICATIONS.md` C-139, `:2644-2656`) settles each, approves the token the backlog row #75 names (`--pc-on-primary`), keeps the round shapes, supplies no new word. No open PR (#85, #86, #91) and no pushed branch dated after 2026-10-16 touches a style sheet (196 branches compared). The white keeps its value, so 74/80 must measure 0 differing pixels; 81 is the only visible change, and its HOLD condition (monospace overflowing the key cell, no font-size or width ruled) is written in.

## Per-ticket BUILD / HOLD
| Ticket | Verdict | Why |
|---|---|---|
| PCOMP-74 (white literals, app.css) | BUILD | C-139 `:2649` approves `#ffffff` becoming a token, by name `--pc-on-primary`; value unchanged, no palette change; 11 literals at main (`grep -c -i` 11, control by `awk` with selectors). Radius half already live; 50 %/999px kept (`:2649`, `:2653`). |
| PCOMP-80 (Expert sheets) | BUILD (w1, w2: 7 literals). w3's 2 literals: BUILD by Q-1 default YES, else listed | Ticket text names w1 and w2; the ruling sentence in its comment reads "the white literals in the Expert screen styles", and S9's sheet is an Expert sheet. Not named in the ticket text, so it is a question with a default, not an assumption. Held shapes pinned by `b120-radii.test.ts` (10 entries), untouched. |
| PCOMP-81 (withdrawn key font) | BUILD, conditional HOLD on measurement | The file is `screens-w3.css` (the sweep said "builder locates"). Ruling `:2649`: keys of both lists use the monospace font; the register's key already has `pc-mono` (`register.tsx:302,307`), the withdrawn key lacks it (`withdrawn.tsx:113`). CSS-only route: one scoped `font-family` rule with the same stack as `.pc-mono`, not `word-break` (it would defeat the `<wbr>` joints) and not a new font token (unapproved). If a joint-run stops fitting on one line or anything scrolls sideways, there is no ruling for a size/width/break change: HOLD 81, push 74 and 80. |

Nothing needed a new word, a palette change, or non-CSS code. Adding `pc-mono` to the span (the shortest fix) is TSX and `b56-withdrawn.test.tsx:140` pins the class list, so it is deliberately not offered.

## Facts re-measured, with instrument
- Main `879facda441e4f7abccec51583916804f7770789`, committed 2026-11-11T06:36:13Z (`gh api -X GET .../commits/main`; `git ls-remote origin refs/heads/main` through the deploy key printed the same sha). Note the sweep and B1506 kit carried older shas; this is the current one.
- **Dead ssh path confirmed:** the local `2_Project_Files` has repo-local `core.sshCommand` pointing at `/Volumes/Laptop-DEV/.../composer_github_deploy_rw` (`git config --local --get`). `ls-remote` with `-c core.sshCommand=` plus `GIT_SSH_COMMAND` (the Datasec_DEV key) worked. The kit tells the seat the same (REFUSE 9); I edited no config. A fresh `--no-checkout` clone does not copy that config (kit says to check it prints nothing).
- Sheets at main (raw `contents`): `#ffffff` counts by `grep -c -i`: app.css 11, screens-w1 3, screens-w2 4, screens-w3 2, tokens.css 1 (`--pc-nav-fg`, left alone), others 0 incl. feedback.css; no `#fff`/`rgb(255..)`/`white` value anywhere (0, with 20 `#ffffff` lines as control). Each site printed by `awk` with its selector (all in the kit).
- Rulings: C-139 read whole (`:2644-2656`), C-143 `:2709`, C-144, C-145 headings; the 14:15 ruling is the one that rules each ticket. Sweep rows 68-70 and lane line 79 read.
- Jira GET (python `-I`, in-process credentials, 19:12): PCOMP-74/80/81 each Backlog, Task, 1 comment (40998/40999/41000), all 2026-11-11 14:39.
- Open PRs: #91 (2 files), #86 (2), #85 (57, draft). Style-sheet paths in each: 0, 0, 0 (control: #85 holds 46 `.ts/.tsx` lines). 196 branches compared (`compare/main...`): 127 ahead, 36 touch a `.css`/`styles/` path, the newest of the 36 dated 2026-10-16 (`b152/approved-words-and-looks`); 0 touching branches dated 2026-10-25 or later. Last commit per sheet: 2026-09-24 to 2026-10-16. So no overlap on a file the seat commits.
- Tests (426 `apps/web` and `scripts` files fetched at main): 13 unit tests read the sheets at run time; none pins a `#ffffff` literal (2 grep hits, both computed `rgb(255, 255, 255)` of the Feedback pill, unaffected); none pins the withdrawn key's font; the phrase "page's one font" is only in the CSS comment itself. `b120-radii.test.ts` HELD list (10) stays untouched. Control for the greps: `pc-radius` 4 in `b120-radii.test.ts`.
- Ports: `lsof -nP -iTCP:9660-9669 -sTCP:LISTEN` 0 rows (rc 1). Scan of 84 non-`.pre-` SEAT kits of 11-10/11-11 for `966[0-9]`: 2 hits, both prose saying the block was re-assigned away (B1502, B1504, both finished); control `967[0-9]` fires. Pane list: no Composer pane.
- Routing: row C2 `model-routing.md:92` (Sonnet first), gate row G2 `:109`; `claude-sonnet-5-5` at `models_latest.json:23`.
- Project style rules cited from the project itself only: `tokens.css` header, `2026-09-10_screens-MEASURED.md`, the e2e token-conformance checks, backlog row #75 (via C-139). No other project's guide read.

## D-decisions (mine, in the kit)
- D1. Token name `--pc-on-primary`: taken from C-139 `:2649`, which quotes row #75's wording as approved. It is slightly odd for white surfaces (secondary button, textarea, cards), but the ruling says one value for all.
- D2. `--pc-nav-fg` (the rail's own white, pinned by `wiring.test.ts`) is not re-pointed.
- D3. 81 uses the identical stack string, no `word-break`, no `font-size`, no new font token.
- D4. One NEW test file `apps/web/src/styles/b1516-style-leftovers.test.ts` (appended across commits) with red-first and plants; no existing test edited (the comparison must read lost 0, changed 0). CSS comment at `screens-w3.css:657-659` is edited because it would become false.
- D5. Measurement is a local `file://` headless-Chromium route (computed census per site, base vs head, contrast, real `withdrawn.tsx` markup, pixel diff with a planted control, both 1280 and 390). The project's driver is forbidden (it signs in to the demo).
- D6. READY = Step 0 + 150 min, not later than 22:45; HARD STOP 23:30 (as commissioned).

## Q-questions for Tuesday (each with a default)
- Q-1. Include the two `#ffffff` literals in `screens-w3.css` (`.w3-check-mark`) under PCOMP-80? Default YES (same sheet the seat edits for 81; ruling says "Expert screen styles"). If you read C-139's "forbids reading the ruling as covering any ticket outside its row" strictly, answer NO and they go to FOR TUESDAY.
- Q-2. Token name: default AS RULED (`--pc-on-primary`).
- Q-3. Allow a compose-stack e2e measurement of the real screens? Default NO. The kit then states plainly that the shell, Guided pages and Expert screens are not rendered and four e2e specs stay unrun for the gate.
- Q-4. New test file: default YES.

## UNMEASURED
Whether host Chromium and the project's Playwright run from `.tools/pw`/`.tools/ms-playwright`; the longest real setting key; whether the monospace key fits its 32 % cell at 1280 and the 390 cards (this is the real risk of 81, and `b126-details-polish.spec.ts` pins "each joint-run on one line"); prettier's output; the Docker cache; whether the token-conformance e2e allowed set stays a superset (reasoned, not run); the deployed look. I ran no test, build, browser or docker.

## Outside-the-fences disclosure
Read-only. `gh api -X GET` only, under the project `GH_CONFIG_DIR` (contents ×~430, tree, pulls, pulls/files, compare ×196, commits, matching-refs, branches). One `git ls-remote` on the project checkout with `-c core.sshCommand=` and the project's deploy key via `GIT_SSH_COMMAND` (no config edit). Jira GET through my own `jira_read.py` in scratch (python `-I`, `.env` read in-process, never printed). Read the project's `CLAUDE.md`, `JIRA.md`, `CLARIFICATIONS.md` (C-139 and landing lines), `.tools` listings, `.tools/pw/run.sh` and the head of `driver.mjs` (not run; I saw that it signs in to the demo and forbade it in the kit), the precedent kits and report, the sweep, DRAFTER_RULES, `model-routing.md` rows, `models_latest.json`, and listed the briefs folder for the port scan. No `decision_queue.sh` call. Did not read `briefs_staged/`, the scoreboard, the main ledger, or anything of another client. Wrote only the kit, its `.pre-stamp` copy and this report, plus scratch.
