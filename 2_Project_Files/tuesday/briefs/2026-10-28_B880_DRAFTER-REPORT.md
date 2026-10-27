STARTABLE: YES (after your stamp: thirteen slots, five of them decisions: DONE-MOVES, ITEM-6, ITEM-7, ITEM-8, ITEM-9; each decision slot names its default)

# B880 drafter report (kit: `2026-10-28_B880_SEAT-R80_hpsmpoc-records-deploy-c00e2828.md`)

## BLUF
Kit written for Datasec/HPSM-POC-R80, Sonnet, records. It records the B874 deploy of `c00e2828` (UAT then demo, web + API, no rollback) as C-223, and supersedes C-222's "NOT deployed" bullet in the form of C-124 and C-128 (`CLARIFICATIONS.md:1902`, `:2002`). It posts the two deploy comments on HPSMPOC-359 and -360 and moves only the keys `DONE-MOVES` names. Each of FOR TUESDAY items 6 to 9 gets its own slot. R80 is the next free seat (R79 = B875; no R80+ kit and no B878/B879 in `tuesday/briefs/`). Every fact was re-read at source (GET only) between 08:29 and 08:45 AEDT.

Defaults by slot:
- **DONE-MOVES:** both keys.
- **ITEM-6 (Tailwind):** CREATE. No ticket exists.
- **ITEM-7 (start-up warnings):** COMMENT-207. HPSMPOC-207 is this exact item, so CREATE is not offered.
- **ITEM-8 (runtime, HPSMPOC-268):** NONE. This is the commission's "no write" default.
- **ITEM-9 (UAT SecretNotFound):** SKIP. The template documents it as harmless.

## Facts re-measured (instrument; control)
**B874 STATUS** (Read, whole):
- 282 lines, sha256 `f82d29af...6f9c`, mtime 08:28.
- Line 1: `DEPLOY B874: DONE, UAT + demo @ c00e2828 (WEB + API), no rollback`. Line 282 begins `DEPLOYED: UAT + demo @ c00e2828 (WEB + API)`.
- Deployment ids in full at `:133` (UAT web `7e4d57b2-e741-...`, API `d2f3506e-7dd9-...`) and `:192` (demo web `9467aa26-e60e-...`, API `c25beeb2-36b1-...`). FOR TUESDAY 5 prints only their prefixes.
- Times: UAT 07:45:28-07:47:38, demo 08:07:27-08:14:21 (`:6`).
- Build `ksAkGKt35N5zXMin2YoW8` on both. Packages and run 40558538369 at `:42`.
- W3 at `:150` and `:209`. NOT TESTED at `:230`.
- No newer deploy STATUS was seen. The kit makes the seat check this with a `grep -l` (expected: B874).

**B871 STATUS** (89 lines, sha256 `6f1da98f...ff7f`):
- PR #149 was merged by the seat itself as merge commit `e2f46d0a` (`:61`). This is the landing precedent for Step 8.
- `grep -c -i 'HP Restricted'` gives 4 hits at lines 35, 47, 54 and 58. All four are the name of that check in scan reports, so the kit pre-clears them for the catch-up copy.

**Records repo** (`gh api -X GET`):
- Main `e2f46d0a7369fb724c61787401255625749815f1`. 0 open PRs (control: `state=all` lists #149 first). `records/b88*` 0 refs; `records/b87*` = `b871` only.
- CLARIFICATIONS: 4651 lines, 222 `### C-` headings, highest C-222 at `:4626`, and its "NOT deployed" bullet at `:4648`.
- **R-R10-1 is at `:1904` verbatim** (re-read). The same text repeats at :2004, :2087, :2121 and :3709.
- `B874|ksAkGKt3|7e4d57b2|9467aa26` over the three files: 0 (control `C-222`: 4).
- BACKLOG: 2169 lines, B871 section at `:2119`. History: 2530 lines.
- The records tree holds B858 to B868 STATUS files and lacks B871 and B874. It holds no `B804_evidence/` or `B836_evidence/` path, so no evidence folder is copied.

**Code repo:**
- Main `c00e28284e9a...`, 0 open PRs.
- `web/src/app/globals.css:1` is `@import "tailwindcss";`. `@source` count 0 (positive control: `@import` 3). `postcss.config.mjs` uses `@tailwindcss/postcss` only.
- 199 `*.test.ts(x)` files, all under `web/src` (the two patterns give 199 and 199).
- `infra/modules/appservice.bicep` (255 lines): `:125` "Where the route is off, RouteSettings never reads them, so a vault without the two secrets is harmless."; `:128` route automation on the demo only; `:129-130` the two references in every environment.

**Jira** (GET via `.tools/b871/jira.py` imported by a scratch driver; no author names copied):
- HPSMPOC-359 and -360: Backlog, 1 comment each (40236, 40237).
- HPSMPOC-207: Backlog, 9 comments. It is about the 3213/3211 pair; its last three comments are sightings of it.
- HPSMPOC-268: Backlog, `needs-kam`, 6 comments. 40218 already records the demo API at 10.0.14; 40225 says the UAT runtime was not re-read.
- Searches: Tailwind 0, stylesheet 0, CSS 6 (none the item); SecretNotFound 0, WebhookToken 0, `Feedback__Automation` 5 (none the item); READ_COMMITTED_SNAPSHOT 11 and "seed lock" 17 (only HPSMPOC-207 is the item); `c00e2828` 4 (363-366); B874 0, B880 0.
- Controls: `qxv9k2zzprobe` 0, `kwpf8rrzzmarker` 0, `UatOpenTests` 23, `key = HPSMPOC-268` 1.
- `created >= 2026-10-28 00:00` lists 363-366 only. Newest key: HPSMPOC-366.

**Environment:**
- Ports: none needed, none assigned, `lsof` not run.
- Panes at 08:32: `%0 tuesday`, `%1 fleet-monitor`. Load1 1.74.
- `.tools/b880` is absent.

**Model:**
- Sonnet `claude-sonnet-5-5` (`models_latest.json:23`). `brief_seat.sh:24` defaults to opus, so `BRIEF_SEAT_LEVEL=sonnet` is inside the quotes.
- Routing cites C8 `:98` and C7 `:97`, as B871 did. Row C8's text is "Brief drafting, board screens, gate kits, tooling with arms" and does not say "records". I kept the template's citation and say so here (as B871's report did).

**Launch line:** `WED_USAGE_STOP=100` appears before `bash .../launch_when_cool.sh` (outside the quotes) and again inside them.

**Banned-term scan** (program, over all 22 fixed text parts):
- 13 classes, 0 hits each, and every class's plant fired. Classes: day words and abbreviations, banned words, backtick, non-ASCII, e-mail, `\bB[0-9]{2,4}\b`, seat / `Datasec/` / R80 / D40, lower-case card-id shape, person names, `\bHP\b`, HP Restricted, FOR-heading quote, kebab card-id shape.
- Summaries are 182 and 205 characters. The whole kit has 0 non-ASCII lines.
- Slot lines with four underscores: 14 (13 slots plus the last line).

**Every file:line in a fixed Jira text was re-read and is MEASURED:**
- `CLARIFICATIONS.md line 1904`
- `globals.css line 1`
- `appservice.bicep lines 125, 128, 129, 130`

No STATUS file:line appears in Jira text, because the STATUS file names carry B-numbers.

## D-decisions
- **D-1. No B-numbers anywhere in Jira text,** following your commission, which is stricter than the B871 template:
  - The marker is `[REC-DEPLOY-28OCT]`, not `[B880]`.
  - Summaries are prefixed `[Deploy finding, 2026-10-28]`.
  - Labels are `deploy-found`, `rec-2026-10-28` and `web` / `hosted-uat`, instead of the project's usual `b874-found` / `b880-2026-10-28`.
  - Evidence is cited as "entry {C-DEPLOY} in the analysis repository" instead of the STATUS path. See Q-3.
- **D-2. The C-number is reserved at Step 3,** before the Jira writes, because the comments cite it. A taken number at Step 6 means STOP.
- **D-3. Item 7 offers no CREATE option,** because HPSMPOC-207 already covers it.
- **D-4. Item 9 defaults to SKIP,** because the template's own comment at `:125` calls the missing secrets harmless while the route is off. The ticket text is carried in case you choose CREATE.
- **D-5. Catch-up copies are the B871 and B874 STATUS files only,** with no evidence folder.
- **D-6. The coordinator's 08:28 reads and the board report are RELAYED** in the C-entry with no board receipt id. Your receipt `bf-b3e07a3aa107` is named here only; it is not in the kit.

## Q-questions for Tuesday (each with a default)
- **Q-1 (before launch): DONE-MOVES.**
  - Default: `HPSMPOC-359, HPSMPOC-360`. Both Done-whens were met at merge by gate B863 (C-222), and this deploy completes R-R10-1. HPSMPOC-363 (the README sentence) is a separate ticket and is not a hold.
  - Alternative: move HPSMPOC-359 only, because 360's change is README-only and is not deployed by itself. The deploy still makes its commit live.
- **Q-2: Item slots.**
  - ITEM-6: CREATE.
  - ITEM-7: COMMENT-207.
  - ITEM-8: NONE. Alternatively COMMENT-268 adds the UAT 10.0.14 reading; the ticket's title names the demo API, and the demo reading is already recorded in 40218.
  - ITEM-9: SKIP.
- **Q-3: Labels and marker without B-numbers (D-1).** Default: keep them as written. If you rule that labels are metadata rather than "sent text", change the K6/K9 label lists to `b874-found`, `b880-2026-10-28` before stamping. The fixed texts themselves are unaffected.
- **Q-4: Landing.** Default: Step 8 as in B871 (the seat opens and merge-commits its own records PR). B871 proved this route at `:61`.
- **Q-5: Routing row cite** (C8 `:98` does not name records). Default: keep it, as the templates do.

## UNMEASURED
- The hosted sites: every deploy fact is the deploy seat's own claim, and your 08:28 reads are RELAYED.
- Records, code and Jira after about 08:45.
- The B874 evidence folder's contents.
- Whether the seat's PR and merge are allowed on the records repo (B871 did both).
- The project's total issue count.
- Who verified what on the board beyond your commission's wording.

## Outside-the-fences disclosure
- Read-only throughout. I wrote only the kit and this report.
- Scratch files under the session scratchpad (`b880/j.py`, `scan.py`, raw copies of the records files, `appservice.bicep`, `globals.css`, the trees) are scratch, not project files.
- I did not run `decision_queue.sh`, and did not read staged briefs, the ledger, or any WEDNESDAY or FRIDAY tree.
- Jira was read through the project's helper; no token was printed. Three hook events occurred:
  - A `cd` refusal: the command was re-issued without it, and nothing ran.
  - An unquoted `===` refusal: fixed.
  - Case-sensitive-grep advisories on index greps: not counts that decided anything.
