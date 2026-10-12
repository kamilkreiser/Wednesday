From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: the STATUS file is the wrap.
# BRIEF B63 · SEAT-G: QA GATE (TIER 1), round 1 of 2: `b60/feedback-pill-on-d711b42` (B47's Feedback pill, store, Administrator list and Jira tickets OFF by default, carried onto main `d711b42c` by B60)

**Fired: 2026-10-13 04:42 AEDT.** Ports corrected by Friday before launch: **6640–6649** (6690–6699 sits in the 6660–6699 block earlier MPS briefs list as never-bind, and other drafts on this laptop name 6691/6698/6699; 6640–6649 had 0 listeners at Friday's lsof, control: 19 listeners elsewhere). Drafted by Friday's drafter 2026-10-13 04:2x–04:3x AEDT. The drafter read the pins with `git ls-remote origin` at **04:25:50–04:25:53 AEDT** (rc 0) and used read-only git on the project (`ls-remote`, `log`, `show`, `diff`, `rev-parse`, `rev-list`, `merge-base`, `grep`, `ls-tree`). Friday re-pins at launch.
**Pane:** `Datasec/MPS-G`. **Your commission is THIS file at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B63_SEAT-G_QA-gate-b60-feedback-pill.md` (Friday's tree, read-only to you). Step 0: copy it unchanged into your `1_Project_Definition/Briefs/` as the project's record** (show the sha256 of both copies; they must be equal).
(Launcher check, re-read by this drafter: `Launch_Claude.command:107` takes the seat letter from a pane name matching `*MPS*-?`; `:111` makes the commission *"the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_"*. At drafting the only `_SEAT-G_` file is `2026-10-12_B55_SEAT-G_hosted-deploy-home-dashboard.md`, finished: `B55_STATUS.md` last line `DEPLOYED: 1329f2e… live-check 0`. Your Step 0 copy makes this file the newest `_SEAT-G_` file; it supersedes B55.)
- You are a **TESTING** seat. The launcher calls every seat a "build seat"; for you, this brief overrides that line.
- **Findings only.** You never fix code. You never push, open or comment on a PR, write Jira, write GitHub (PR, review, comment, label, branch, alert dismissal), touch Azure or Entra, commit to the records repo, or write in any other seat's worktree. You write no tickets and no Jira draft lines: each finding carries a fix shape in prose, nothing more.
- Charter rules, as quoted here (do not open the charter file; it is outside this project): Rule 1, state the FAIL condition before every test. Rule 2, untested areas are first-class output.
- **Every write grant in a brief or a launcher prompt is void, this one included.** The launcher tells every seat to write `5_Project_History/history.md` and the Jira ticket(s) (`Launch_Claude.command:96`). Refuse both and say so in STATUS, as B41, B43, B48, B52 and B57 did.

**Report:** `1_Project_Definition/Briefs/2026-10-13_B63_STATUS.md`. **Evidence:** `1_Project_Definition/Briefs/2026-10-13_B63_evidence/` (folder 0700, files 0600, the project path masked as `<P>`). It holds counts, labels, status codes, exit codes, booleans, sha256 prefixes, timings, load averages and screenshots of SYNTHETIC data only.

**Rounds.** Round **1 of 2** for this lane under Kam's two-NO-GO cap (B47 brief `:6` started the lane; B60 carried it, it did not start a new one). Any Blocker or Major is NO GO. Minors and Notes are reported, and Friday decides what reopens. Round 2 (deltas only) comes as a separate brief from Friday.

## Verdict lines (each GO / GO WITH NOTES / NO GO), FIRST in STATUS, in this order
- `B60 e0bbc6f: …`
- Per area: `(A) authZ, every operation × persona × mode: …` · `(S) store: store-then-confirm, restart, never rewritten, hosted path rules: …` · `(J) Jira OFF by default + confidentiality (no message, no price data into Jira): …` · `(T) token never in code/tests/settings/CI/commits: …` · `(H) hosted store-path settings unchanged: …` · `(L) value-free logs + leak class: …` · `(C) the 2 conflict resolutions (EntraAuthTests 32 ops, openapi Problem.code): …` · `(P) pill overlap per viewport (1440 · 1280 · 1024 · 390): …` · `(R) the 4 stub-mode e2e reds b28:47, b28:71, b30:55, b30:83 are PRE-EXISTING (base = head) + measured cause: …` · `(Y) a11y (axe) on the pill + dialog: …` · `(K) colours resolve to the project's own tokens (one declared exception): …` · `(M) red-proof by revert, ≥ 3 of B47's security tests: …` · `(U) suites base vs head: …` · `(W) NEW WORDS: …`
- `FAST-FORWARD d711b42c → e0bbc6f: …` (main unmoved at both reads ⇒ the squash tree = head tree)
- `overall: …`

Then one closure row per item: **CLOSED / CLOSED-WITH-NOTES / NOT CLOSED / UNMEASURED / NOT IN SCOPE**, each with the ratio that decides it. Rows: B47 Items 1–8 (brief `:72-94`; Item 9 records is NOT IN SCOPE: B47 did it on `b28c95eb`, B60 wrote no records), `[B47-D6]` (390 overlap, Kam's call), `[B60-1]` (1440 Home "Continue" overlap, proposed by B60), `[B60-2]` (the 4 stub-mode reds, proposed by B60), the `ApiProcess.cs` one-line edit outside B47's write set (B47 STATUS `:24`, `:48-52`).
The last line is exactly **`READY FOR REVIEW: b60/feedback-pill-on-d711b42 e0bbc6f80829aa4ed4bba954861a73dff8303f64 <overall verdict>`**. If you are stopped, the last line is **`STOPPED: NEEDS FRIDAY`** plus ONE blocking question.

## Authority (what the lane had to build)
- **The pass conditions are the build briefs, read whole:**
  - **Spec:** `Briefs/2026-10-12_B47_SEAT-B_feedback-pill.md` (118 lines): ORANGE token decision `:41-45`, Write set and Frozen `:61-65`, ITEMS 1–8 `:72-94` (store `:72`, item shape `:73`, API `:74-79`, pill `:80`, form `:81`, tickets + confidentiality + credential + hosted holds `:82-86`, tests `:87-93`, NEW WORDS `:94`), UNMEASURED `:100-104`, HOLDS `:106-113`.
  - **Carry brief:** `Briefs/2026-10-13_B60_SEAT-B_b47-feedback-onto-main.md` (21 lines): Do `:9-15` (both sides survive a conflict `:12`; re-prove everything `:13`; main's tests never edited), HOLDS `:17-21`.
- **Builders' claims (claims, not facts):** `Briefs/2026-10-12_B47_STATUS.md` (276 lines) and `Briefs/2026-10-13_B60_STATUS.md` (174 lines), whole. Their evidence folders, `.tools/qa-B47/`, `.tools/qa-B60/`, `.tools/wt-B47*`, `.tools/wt-B60*` may be **read**, and their tools **copied**. Nothing in them is proof for you. **Test the headline claims independently.**
- **Friday's two items from B60 (B60 STATUS `:15-17`), which you rule on with measurements:**
  1. **The pill covers the Work queue "Continue" row actions at 1440 on main's new Home** (B60 STATUS `:54`: *"control `a.button.row-action "Continue"` ×2"*; screenshot `B60_evidence/b47-pill-closed-1440-seller.png`, sha256 `a4fd3a8d2eea…`, re-hashed by this drafter: equal). B47 measured 0 hits at 1440 on the old dashboard (B47 STATUS `:137`). The anchor is `web/src/screens/Dashboard.tsx:284` (`<a className="button primary row-action" …>`) inside the `Work queue` region `:328` at `d711b42c`.
  2. **4 stub-mode e2e reds**, `b28.spec.ts:47` (G-2), `:71` (G-6), `b30.spec.ts:55` (G-13), `:83` (G-3 stub), claimed identical on base and head (B60 STATUS `:46`, `:69-73`) with cause *"`POST /api/v1/quotes` → 502 with no API on the origin"*.
- **Friday's rulings carried, grade them as built, not as open questions:** the pill colour `--feedback-bg: #b84a00` on the pill only (B47 brief `:43-44`; it is outside the palette **by design**); `IncludeMessage` default false; any signed-in caller may submit, Administrator only lists and retries (B47 STATUS `:213`); the label search on `GET /rest/api/3/search/jql` (B47 STATUS `:113`, UNMEASURED against Atlassian, stays so).
- **Not yours to rule on:** `[B47-D6]` and `[B60-1]` acceptance (Kam's call, Composer C-58 precedent, B47 brief `:22`); the hosted `MpsCalc__Feedback__Path`, the Jira credential and `IncludeMessage` (Friday/Kam after merge, B47 brief `:85-86`); the SITE HOLD (records `BACKLOG.md:17-23` at records main `ae9d895`).

**Headline claims under test (claims):**
- **B60** (STATUS BLUF `:7-17`): cherry-pick of all 6 commits; 2 conflict files, both resolved keeping both sides; diff = B47's 31 files, +3787 −4; .NET 1,216 → 1,312 (API 909 → 1,005), 0 failed, Release 0 warnings; Vitest 381/52 → 426/58; Playwright `b47-feedback.spec.ts` 20/20 head, 0/20 base; `b46-home.spec.ts` 13/13 both; live probe line for line as B47.
- **B47** (STATUS `:5-26`): RED → GREEN API 110/112, web 41/45, e2e 20/20; value-free logs; message never sent to Jira by default; tickets OFF → 0 requests.

**Tier-1 Blocker classes (whatever the path):**
- **AuthZ:** any non-Administrator persona (incl. Administrator acting as Seller) that gets 2xx on `GET /api/v1/feedback` or `POST /api/v1/feedback/{id}/ticket`; any unauthenticated 2xx; a stored `submittedBy`/`submittedAt`/`roles` taken from the client; an Entra-stored item holding an e-mail address.
- **Jira / confidentiality:** any outbound request when `MpsCalc:Feedback:Jira:Enabled` is absent or false; the message text, or a planted price-shaped value, in any Jira request body when `IncludeMessage` is not `true`; any request to a non-fake host; a feedback refused or lost because a ticket failed.
- **Token:** any token-shaped value other than the literal `test-token-not-real` in code, tests, `appsettings*.json`, `infra/**`, `scripts/**`, `.github/**`, or any commit message of the range; the token, the Jira e-mail or `Basic ` in any log line, response or start-refusal message.
- **Hosted holds:** any of `MpsCalc__QuoteStore__Path`, `MpsCalc__QuoteStore__HostedRoot`, `MpsCalc__CatalogueOverlay__Path`, `MpsCalc__ReferenceStorePath` changed by the range (records `BACKLOG.md:17-21`); a hosted start that opens a feedback store outside HostedRoot, in `wwwroot`, through a link, or overlapping the quote/overlay/reference stores.
- **Store:** a 201 before the item file is in place; an item file rewritten; a restart that loses or changes an item; any delete of a stray.
- **Leak:** the planted message, page, user, display name, token, e-mail, exception text (`Exception`, `--->`, `   at `, `.cs:line`) or an absolute build or worktree path in any HTTP response, problem `detail`, log line or start-refusal message you can provoke, in DevStub **or** Entra-fake.
- **Scope:** a frozen path in the diff (B47 brief `:65`); any of main's tests edited; the Entra bundle carrying a stub string. A real price book opened by anything you start; a real-client datum anywhere you write; anything deployed.

## Targets (re-pin at start and again before the verdict)
| What | Ref | Pin (instrument) |
|---|---|---|
| Base | `refs/heads/main` | **`d711b42cfcb53da3a2043a2d672511f8ea6ea296`** (`ls-remote`, 04:25:50 AEDT); tree **`ef5cd1566b0804614418bcb533a0057126d87fd3`** (`rev-parse d711b42c^{tree}`); `log -1`: parent `1329f2e`, *"Source version store hardening (B53; gate B57 GO WITH NOTES) (#29)"*. |
| Subject | `refs/heads/b60/feedback-pill-on-d711b42` | **`e0bbc6f80829aa4ed4bba954861a73dff8303f64`** (same call); tree **`fe04a7f0b98fc0e2c28bfaa77635a8d5035ee389`** |
| Spec head (record) | `refs/heads/b47/feedback-pill` | `81b0135d13a20b770df0664857d3043cf03653ec` (same call), on `b28c95eb` |
| Not yours | `refs/heads/b58/gate-b57-overlay-fix-round` | `727c7c89…` (same call): B59's subject. Read-only, never checked out by you. |

**First action:**
1. `git -C 2_Project_Files fetch origin`.
2. `git ls-remote origin refs/heads/main refs/heads/b60/feedback-pill-on-d711b42 refs/heads/b47/feedback-pill`. All three must equal the pins. **If any differs, STOP: NEEDS FRIDAY.**
3. Run the same `ls-remote` again before the verdict. A moved head voids the verdict; a moved main voids the FAST-FORWARD line.

**Measured by Friday's drafter (re-measure; do not trust):**
- `rev-list --left-right --count d711b42c...e0bbc6f8` = **`0 6`**; `merge-base` = `d711b42c…` (so a squash PR lands tree `fe04a7f0…` exactly, if main does not move). GitHub compare (Friday, 04:2x): ahead 6, behind 0, 31 files.
- The 6 commits (`log --format='%h %p %s' d711b42c..e0bbc6f8`): `a5f8e55` Test (red) API · `f3ebadf` API · `199c2e6` Test (red) web · `d1f57b4` Web · `716a57c` Web e2e · `e0bbc6f` Docs.
- `diff --shortstat d711b42c e0bbc6f8` = **31 files, +3787 −4**. `diff --name-only` of `b28c95eb..81b0135d` vs `d711b42c..e0bbc6f8`: **identical lists** (`diff` rc 0).
- **Blob equality, B60 head vs B47 head, over the 31 paths: 28/31 equal; differ = `docs/API.md`, `docs/api/openapi.json`, `tests/MpsCalc.Api.Tests/EntraAuthTests.cs`** (per-path `rev-parse <sha>:<path>`), as B60 STATUS `:12` says.
- **Conflict resolution (C), read at head:** `EntraAuthTests.cs:65` `Assert.Equal(32, contract.Count)` and `:113` `Assert.Equal(32, checkedOps)` (base `:62` / `:110` = 29; B47 had 30). `ApiOperations()` gains 3 rows after the inventory PATCH row (`diff` hunk `@@ -52,6 +52,9 @@`). **Contract `/api/v1` operations by script over `openapi.json`: base 29 · head 32 · B47 30; path keys 30 · 32 · 30; `Problem.code` enum 38 · 42 · 37**; the head enum line = main's line with B47's four codes appended (diff lines `:72-73`). *(B60 STATUS `:31` says "32 path keys (base 28, main 30, B47 30)": its "base" is `b28c95eb`; not re-measured here.)*
- **Jira OFF by default, by reading:** `FeedbackTickets.cs:27` `if (!Flag(configuration, "Enabled"))` returns the disabled settings; `IncludeMessage` read only on the enabled path `:50`; the description puts `Page: {item.PagePath}` at `:400` and `Submitted by: {item.SubmittedByName}` at `:402`. `appsettings.Development.json:7` names `"Feedback": { "Path": "../../.local/feedback/" }` only. `git grep -n -i -E 'feedback|jira' e0bbc6f8 -- 'src/MpsCalc.Api/appsettings*.json' infra scripts .github` → that one settings line plus 3 pre-existing script lines (`scripts/tests/test_scripts.py:425`, `:472` `JIRA_SYNTHETIC=1`; `scripts/upload-pricebooks.sh:3`). `test-token-not-real` occurs in **1** file (`FeedbackTicketTests.cs`) over `tests src web`.
- **Auth, by reading:** `FeedbackEndpoints.cs:89` submit `Authorized(ctx, …)` with no role; `:175` list and `:211` retry `Authorized(…, Roles.Administrator)`; routes mapped `:80-82`.
- **Page path reaches Jira (gate it, see item 4):** `ReducePage` (`FeedbackEndpoints.cs:254-285`) keeps any client text after `#/` up to `?`, ≤ 2000 characters, and that text goes into the issue description (`FeedbackTickets.cs:400`) even with `IncludeMessage` false.
- **Colours, by reading:** `feedback.css` at head: `--feedback-bg: #b84a00` (`:5`, the declared exception); every other colour is `var(--brand-ink|accent|line|surface|text|ok-ink|ok-bg|bad-ink|bad-bg)` (tokens at `styles.css:3-15` at `d711b42c`), plus `rgba(0, 0, 0, 0.15)` (`:22`; exists at `styles.css:124` on main) and `rgba(15, 25, 40, 0.35)` (`:39`; exists at `styles.css:123`, the drawer backdrop). `styles.css` has **0** `prefers-color-scheme` lines at main (no dark theme to test). Drawer backdrop `z-index: 30` at `styles.css:123`; banner `z-index: 20` at `:40`.
- **e2e at main:** `web/e2e/` holds 10 specs (`ls-tree`): `b28`, `b30`, `b46-home`, `bom`, `inventory`, `print`, `proposal-content`, `proposal-purchase`, `proposal-stub-mode`, `smoke`. **B60 ran 5 of them** (b47, b46-home, b28, b30, inventory: STATUS `:44-46`); `smoke`, `bom`, `print` and the three `proposal-*` were not run. B49 recorded `smoke.spec.ts:13` failing at base and head (`B49_STATUS.md:60`, `:63`).
- **`b47-feedback.spec.ts` sizes:** `:12` `1440×900 edge 24`, `:13` `390×844 edge 16`; no 1280 or 1024.
- **axe:** `web/package.json` at `d711b42c` has `@playwright/test` `1.63.0` and **no** axe package; `wt-B60/web/node_modules/` has neither `axe-core` nor `@axe-core`.
- **The 4 reds' test lines at `d711b42c`:** `b28.spec.ts:47` G-2 and `:71` G-6 sit in `test.describe('stub mode')` (`:40`), whose `beforeEach` skips without the stub banner; `b30.spec.ts:55` G-13, `:83` G-3 stub. B49's stub run with a DevStub API behind the proxy (its ports `:62`) passed b30's two stub tests at its head (`B49_STATUS.md:60`).
- **Ports:** `lsof -nP -iTCP:6640-6649 -sTCP:LISTEN` at **04:29:53 AEDT → 0 lines (rc 1)**; the same range in any state → 0 lines (rc 1). **Note:** 6660–6649 is on the never-bind lists of B46 (`:59`), B48 (`:83`) and B57 (`:130`), because other projects' drafts of 2026-10-11 in Friday's tree name 6641, 6648 and 6649. Friday assigns 6640–6649 to you now; **`lsof` before every bind, and on any listener that is not yours, STOP: NEEDS FRIDAY.**
- **Load:** `uptime` at 04:29:53 AEDT → **load averages 112.85 142.67 136.46** (B59's load test running, below).
- `.tools/wt-B63*` and `.tools/qa-B63` do not exist (drafter's glob: no match).

## The other live gate: B59 (pane `Datasec/MPS-E`) — never touch it
- B59 gates `b58/gate-b57-overlay-fix-round` in this same repo, on ports **6650–6659** (its brief `:104-116`), with worktrees `.tools/wt-B59-{clean,comb,e6,e6-clean,head,main,mut,red}` and tools/logs under `.tools/qa-B59/`. At 04:29 the drafter saw its processes: `qa-B59/tools/underload59.sh`, `loop59b.sh`, a looping `dotnet test … OverlayGateFindingsTests.G1…`, and a `python3 -I` listener on 6659 (cwd `.tools/qa-B59/tools`). Its CPU burners run under `.tools/qa-B59`.
- **Never** signal, renice, read-lock or edit any B59 process, worktree, file or port. Never bind 6650–6659. Never run a broad `pkill`/`killall`.
- **Load rule:** state `uptime` with every timing. **If the 1-minute load is above ~40 when a timing-sensitive step runs** (Playwright geometry/overlap runs, the ticket backoff probe, any timeout test), **wait for it to fall, or run it and say so** in STATUS with the load, and mark the result "under load L". A timing failure under a load you state is a Minor, not a Blocker; a functional failure is graded on its merits.

## Your setup (own worktrees, own ports, own state)
- **Worktrees** (0700, never removed), from `2_Project_Files` with `worktree add --detach` only:
  - `wt-B63-base` @ `d711b42c`;
  - `wt-B63-head` @ `e0bbc6f8`;
  - `wt-B63-mut` @ `e0bbc6f8` (reverts only, restored by sha256);
  - `wt-B63-clean` @ `e0bbc6f8` and `wt-B63-base-clean` @ `d711b42c`, for `scripts/package.sh` (Entra-fake packages) and nothing else.
- **Your own clone** for any git write verb (e.g. `git revert` of a hunk to build a red-proof tree): `git clone --shared '<P>/2_Project_Files' '<P>/.tools/qa-B63/clone'` (0700), `remote set-url --push origin NO-PUSH`, show a dry push fails. Local identity `qa-b63@invalid`, never pushed.
- **Tool output:** `<P>/.tools/qa-B63/` (0700). Every cache, log, TRX and Playwright output there.
- **Copied instruments** (copy into `qa-B63/tools/`; never edit or run them in place): B60's/B47's probe scripts from `.tools/qa-B60/` and `.tools/qa-B47/` (the fake Jira, the live-probe driver), and B57's `oidc_stub*.py`, `jwt*.py`, `pkg.sh`, `leakscan.py` from `.tools/qa-B57/tools/`. Name every copied script in STATUS, and show that each control fired **in this run**. New gate keys in `qa-B63/keys/` (0600).
- **axe:** install pinned `axe-core@4.10.2` with `npm install --prefix '<P>/.tools/qa-B63/axe' axe-core@4.10.2` (and `@axe-core/playwright@4.10.2` if you use it), and inject it from there (`page.addScriptTag({ path })` or the package). **Never edit `package.json`, `package-lock.json` or any spec in a worktree you run main's tests from**; put your own specs in `qa-B63/e2e/` and point Playwright at them with your own config file in `qa-B63/`.
- **Synthetic data only:** messages `SYN-B63-…`, a planted price-shaped value (e.g. `PLANTED-B63-PRICE 9876.54`), a planted user, page and token. For any API you start with a reference store, build the store from the importer's synthetic books (`tests/MpsCalc.Import.Tests/Synthetic/`) into `qa-B63/syn/`, as B57 did. **Never `.local/pricebooks/`; never the shipped Development reference path.** Every process sets `MpsCalc__ReferenceStorePath` to your synthetic file (or a non-existent scratch path, as B60's probe did), and `MpsCalc__QuoteStore__Path`, `MpsCalc__CatalogueOverlay__Path`, `MpsCalc__Feedback__Path` to roots under `qa-B63/roots/` or the worktree's git-ignored `.local/b63-*`.
- **Ports (yours only): 6640–6649. Run `lsof -nP -iTCP:<port> -sTCP:LISTEN` before every bind.** On any listener that is not yours, **STOP: NEEDS FRIDAY**; do not move ranges.

  | Port | Process |
  |---|---|
  | 6640 | head API, DevStub (live probe; behind the head stub web for the reds' control) |
  | 6641 | base API, DevStub (behind the base stub web for the reds' control) |
  | 6642 | head API, Entra-fake, real package from `wt-B63-clean` |
  | 6643 | head web, Vite `VITE_MPSCALC_API_STUB=1`, origin 6640 (**nothing listening** for the as-shipped runs) |
  | 6644 | base web, Vite stub, origin 6641 (nothing listening for the as-shipped runs) |
  | 6645 | base API, Entra-fake, real package from `wt-B63-base-clean` |
  | 6646 | fake Jira (`python3 -I`, scratch copy) |
  | 6647 | spare |
  | 6648 | spare |
  | 6649 | OIDC/JWKS stub (your copy) |

  **Never bind** 6630–6639 (B60's), 6650–6659 (B59, live), 6680–6689 (B58's), 6870 and 6891 (container listeners, `lsof` 04:29), 5000, 7000, 7768, or anything else on B57's list (`B57_SEAT-E…md:130`) except 6640–6649.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`. Build with `-nodeReuse:false -p:UseSharedCompilation=false`. After every revert restore, `touch` the file and build `--no-incremental`.
- **Processes:** stop them by port + cwd, or by a pid you recorded; never by name. Everything you started is stopped before READY. `caffeinate`, the shared `VBCSCompiler`, `@playwright/mcp`, containers and **all of B59's** are not yours. **A Playwright MCP browser check writes `.playwright-mcp/` into the project root** (B60 STATUS `:74`): do not use the MCP browser; use your own Playwright runs with output under `qa-B63/`.
- **Instruments:** `cmd > out 2>&1; rc=$?`; never take an exit status through a pipe; **never `cat` a file into itself** (B57's 43 GB incident). The shell is zsh: run loops via `bash -c '…'`; no bare `===`. Every verdict is a ratio with its denominator. Every scanner zero and every revert needs a control that fired.
- **Personas** (every authZ arm): Seller, Seller+Pricing analyst, Approver, Administrator, Pricing analyst, all four, no role, a second Administrator, Administrator acting as Seller, Seller acting as Administrator, unauthenticated. Say how you make each in DevStub (stub headers) and in Entra-fake (real package, gate-random GUIDs, `AzureAd__MetadataAddress` → your stub on 6649, tokens minted locally and never printed).

## Items (round 1). State each FAIL condition before you run it.
0. **Pins, scope, partition, conflicts (C).**
   - Re-pin; confirm both trees; Step 0 sha256.
   - `git diff --name-status` per commit for the 6 commits; map each to B47's items. Check every path against B47's write set (`:61-64`) plus the declared `csv.ts`/`words.ts` (B47 STATUS `:45`) and `ApiProcess.cs` (`:48`). **A path outside is a finding.**
   - **Frozen numstat = 0 lines** over B47 brief `:65` (`src/MpsCalc.Engine/**`, `src/MpsCalc.Import/**`, `src/MpsCalc.Api/{Quotes,Inventory,Sources}/**`, `web/src/{proposal,screens,api,auth}/**`, `web/playwright.config.ts`, `infra/**`, `scripts/**`, `.github/**`, root build files) and over main's files B46 owned (`Shell.tsx`, `router.ts`, `styles.css`, `client.ts`, `types.ts`, `stubApi.ts`, `generated/**`, `Dtos.cs`, `QuoteEndpoints.cs`). **And: 0 lines in any of main's test files except the 3 added `EntraAuthTests` rows and the two count lines.**
   - **The two resolutions, hunk by hunk** (B60 STATUS `:25-32`): (a) `EntraAuthTests.cs` `:65` and `:113` = 32 = main's 29 + B47's 3, `ApiOperations()` 32 rows = contract 32 operations (by script, set-equal); (b) `openapi.json` `Problem.code`: every base code kept in order, B47's 4 appended, JSON parses, `Every_contract_operation_is_mapped` and `The_operation_list_covers…` pass at head. Show the 3 auto-merged files (`docs/API.md`, `openapi.json` paths/schemas) carry every main line (diff vs `d711b42c` is pure `+`, 4 `−` total in the range: name each). **FAIL: a dropped main line, a count that is not the set's size, or a test passing because its expectation was loosened.**
   - `range-diff b28c95eb..81b0135d d711b42c..e0bbc6f8`: commits 2–6 `=`, commit 1 `!` only in the two conflict files (B60 STATUS `:9`).
1. **Suites (U): base `wt-B63-base` vs head `wt-B63-head`.**
   - .NET Release `--no-incremental`, 0 warnings; `dotnet list package --vulnerable --include-transitive` 0. Full `dotnet test MpsCalc.slnx`. Claimed 1,216 → 1,312 (API 909 → 1,005). Reconcile by name (`--list-tests`, `comm`): 0 names lost; every added name is a `Feedback*` test or one of the `EntraAuthTests` theory rows.
   - Web: `npm ci`, `lint`, `typecheck`, `npm test` (claimed 381/52 → 426/58), `npm run build` (dev) and `VITE_MPSCALC_AUTH=entra npm run build`: the Entra bundle holds **0** of `SYNTHETIC FEEDBACK STUB`, `synthetic stub`, `createStubFeedback`, `stubFeedback`, `(stub)` (control: the dev bundle holds the stub chunk). `npm audit --omit=dev` 0.
   - **Playwright, ALL 10 of main's specs + `b47-feedback.spec.ts`, stub mode, base and head**, with nothing on the API origin (as shipped): per spec passed/failed/skipped, base vs head, failures by name. **FAIL: any red at head that base does not show; any spec whose counts differ base vs head beyond the b47 spec's 20.**
   - State `uptime` per run.
2. **(A) AuthZ, every operation × persona × mode (TIER 1).** DevStub head 6640 and Entra-fake head 6642 (feedback path set to a private dir under your HostedRoot).
   - The 3 operations × 11 personas × 2 modes: expected submit 201 for every signed-in persona (no role included, B47 STATUS `:87`), list/retry 2xx **only** for Administrator (not Administrator-acting-as-Seller, `FeedbackApiTests.cs:205`), 401 unauthenticated with `WWW-Authenticate: Bearer` in Entra, 403 `FORBIDDEN` otherwise. Bad tokens in Entra-fake (expired, wrong audience, wrong issuer, unsigned, wrong key): 401, nothing stored.
   - Body naming `submittedBy`/`submittedAt`/`feedbackId`/`roles`/`submittedByName`: 400, nothing stored (B47 STATUS `:94`).
   - Entra: the stored `submittedByName` is the `name` claim; the stored file holds **0** `@` (control: a token whose `name` is absent and `preferred_username` is an e-mail: state what is stored).
   - Web: the All feedback tab renders only for an Administrator persona (Vitest + your e2e), and a Seller who forces the tab (devtools-style `click` on a hidden control, or a direct `listFeedback` call) gets 403.
   - FAIL: any Blocker class.
3. **(S) Store and (H) hosted holds (TIER 1).**
   - Restart byte-equal (≥ 3 items, 3 personas), dir 0700, files 0600, item file byte-unchanged after its ticket, `.tmp` stray named and never deleted, a bad file named and left. 503 `FEEDBACK_STORE_UNAVAILABLE` with the path empty (submit, list, retry; 401 first in Entra).
   - Hosted path refusals (Entra-fake 6642 starts): outside HostedRoot, relative, in `wwwroot`, a symbolic link, a file, equal to/inside/containing the quote store, the overlay, the reference store's directory; plus a control that opens. Record exit code, listener, the refusal message verbatim (scratch paths only), files created (expected 0).
   - **(H)** `git diff d711b42c e0bbc6f8 -- 'src/MpsCalc.Api/appsettings*.json' infra scripts .github` and a `git grep` for the four held keys over the range's added lines: expected only the `Feedback` key in `appsettings.Development.json`. State that `MpsCalc:Feedback:Path` is a NEW key under the existing HostedRoot and is not placed hosted by this branch.
   - FAIL: any Blocker class.
4. **(J) Jira OFF by default and the confidentiality rule; (T) the token (TIER 1).** Head API 6640 + fake Jira 6646 (copied from B60/B47; `test-token-not-real`, `syn-bot@example.invalid`; never Atlassian).
   - **OFF:** settings absent; `Enabled=false`; `Enabled=""`. Submit ≥ 5 items, retry each as Administrator: 409 `FEEDBACK_TICKET_NOT_RETRYABLE`; the fake records **0** requests; **0** sidecars; and **0 outbound connections from the API process** (`lsof -a -p <pid> -i` sampled during and after; control: with Jira enabled the same sampling shows the connection to 6646).
   - **Enabled refusals:** each missing/invalid setting refuses the start naming the key, never the value (B47 STATUS `:110-112`; 14 arms). Scan each message for the token, e-mail and URL userinfo: 0.
   - **No price data into Jira:** with `IncludeMessage` unset and `false`, plant `PLANTED-B63-PRICE 9876.54` in (a) the message, (b) the category (expected 400), (c) the **page path** (`#/quotes/PLANTED-B63-PRICE-9876.54`, and the same after `?`), (d) the display name (Entra-fake `name` claim). Count the planted value in every fake-Jira request body: expected 0 for (a), (b), the `?` form of (c); **measure (c) and (d)**: `ReducePage` keeps client text after `#/` and `FeedbackTickets.cs:400` sends it. If it reaches Jira, rate it against B47 brief `:84` (spec §40: price-book data never goes into Jira) and say whether a route-shaped page check (known hash routes and ids only) would close it. Control: with `IncludeMessage=true` the message's planted value IS present.
   - **(T)** Token scan over the range: `git log -p d711b42c..e0bbc6f8` and `git log --format=%B` (counts only) for `ApiToken` values, `ATATT`, `Basic [A-Za-z0-9+/=]{16,}`, `Authorization:`, and any string assigned to `ApiToken` other than `test-token-not-real`; `gitleaks git --redact` over the range with a fresh planted control. Settings files: 0 `Jira` keys. Never open `4_Credentials/.env` or `JIRA.md`'s token value.
   - The live probe phases B47/B60 ran (201 path, 500→201 after the real 1-minute backoff, SIGKILL mid-attempt → restart → search finds → 0 creates): reproduce, counts only. **The backoff step is timing-sensitive: apply the load rule.**
   - FAIL: any Blocker class.
5. **(L) Value-free logs and the leak class (TIER 1).** Capture the API log of every process you start. Count the planted message, user, display name, page, token, e-mail, `Basic `, exception text and absolute paths: expected 0 (instrument control: the feedback id IS in the log; value control: the planted values ARE in the stored files). Every problem `detail` you provoke: 0 of the same. Both modes.
6. **(P) Pill overlap per viewport — Friday's item 1 (TIER 1 for "a control unreachable at every scroll position"; otherwise recorded).** Head web 6643 (stub), base web 6644 for the without-pill comparison.
   - **Viewports:** **1440×900** and **390×844** (B47's), **1280×800**, **1024×768**. Personas Seller and Administrator. Routes: B47's 4 (`#/` = main's new Home, `#/inventory` as Administrator, `#/quotes/<stub id>`, its proposal) **plus `#/quotes`** (B46's list route, B60 STATUS `:64` UNMEASURED).
   - Use B47's own method (B47 brief `:90` (b); every visible `button, a, input, select, textarea, [role=button]` and every text node's client rects; control: a planted fixed element under the pill fires), at **top**, **bottom**, and **every scroll step of one viewport height**.
   - For every hit, record: element (role + accessible name, synthetic), the pill box and the element box, and **reachable = whether some scroll position leaves it fully clear** (with `scroll-padding-bottom: 92px` and keyboard focus: Tab to it and test `elementFromPoint` at its centre). Also whether a pointer click at the element's centre lands on the pill.
   - **Specifically the Work queue "Continue" (`Dashboard.tsx:284`) at 1440, 1280, 1024 and 390**, Seller and Administrator, with the stub's default rows and with enough rows to fill the panel: hit / not hit, reachable / not.
   - **Verdict per viewport** in a table: viewport · route · persona · hits at top · hits at bottom · any hit unreachable at every scroll position (yes/no) · verdict. **An unreachable control is a Major (INTRODUCED). A covered-at-top but reachable control is a Note for Kam with `[B47-D6]` / `[B60-1]`.** Screenshots (synthetic only) per viewport at top for Home, Seller: path + sha256.
   - Also: geometry (right edge = viewport − 24 at > 900 px, − 16 at ≤ 900; bottom − 24), the drawer covers the pill (`elementFromPoint`), print hides it, no new horizontal scroll at 390 (with vs without the pill, B47 STATUS `:143`, `[B32-J6]`).
7. **(R) The 4 stub-mode reds — Friday's item 2.** `b28.spec.ts:47`, `:71`, `b30.spec.ts:55`, `:83`.
   - **(i) As shipped** (stub web, nothing on the origin): run the 4 by line on base 6644 and head 6643, ≥ 3 times each. Expected: the same 4 fail on both, with the same assertion (B60 STATUS `:70-72`). Record ratio base n/3, head n/3.
   - **(ii) Measured cause:** capture every network response (Playwright `page.on('response')` or a HAR, synthetic) during each failing test on base and head: the request, its status and the dialog text. Expected per B60: `POST /api/v1/quotes` → **502** through the Vite proxy. Name the first failing request per test and show it is not a `/api/v1/feedback` call (count feedback calls: state it).
   - **(iii) Control that proves the cause:** start a DevStub API on your **synthetic** store (base 6641 behind 6644, head 6640 behind 6643; `MPSCALC_API_ORIGIN` set) and re-run the 4: expected green (or failing for a different, named reason) on both. If they go green with an API and red without, the cause is measured. Compare with B49's run (`B49_STATUS.md:60-62`).
   - **(iv) Pill independence:** run the 4 at head with the pill hidden by an injected stylesheet (your spec only): the result must not change.
   - FAIL (against B60): any of the 4 green at base and red at head, or a cause that involves the feedback module. Otherwise CLOSED as PRE-EXISTING, `[B60-2]` stands for Friday.
8. **(Y) a11y (axe) on the pill and the dialog.** axe from `qa-B63/axe` (setup), WCAG 2.1 A+AA rules, at 1440 and 390, Seller and Administrator: (a) the page with the pill closed, scoped to `.feedback-pill`; (b) the dialog open (Send feedback tab), scoped to `dialog.feedback-dialog`; (c) the All feedback tab (Administrator) with ≥ 3 synthetic rows; (d) the success and error states. Report violations by rule id, impact and count; a control (an injected unlabelled button) must fire. Also by hand: `aria-haspopup="dialog"` on the pill, focus into the dialog, Tab stays inside, Esc closes, focus returns to the pill, every control labelled, the counter announced or not (state it). **FAIL: any `serious`/`critical` violation on the pill or dialog is a Major; `moderate`/`minor` are Minors.** Violations on main's page outside the pill and dialog are PRE-EXISTING Notes (show base parity).
9. **(K) Brand and style.** Every colour in the range's added lines (`git diff d711b42c e0bbc6f8 -- web | grep '^+'`) resolves to a `styles.css` token or an existing `styles.css` value, **except the one declared token `--feedback-bg: #b84a00`** (B47 brief `:43-44`). Script it with a planted off-palette control that fires. In Chromium, read computed styles: pill `rgb(184, 74, 0)` / `rgb(255, 255, 255)`, contrast ≥ 4.5 computed (B47 measured 5.23); dialog surface/text/line/ok/bad colours equal the token values on `:root`; focus ring `var(--accent)`. `styles.css` has 0 `feedback` lines at head (unchanged by the range). No dark theme exists at main (0 `prefers-color-scheme`): state it, no test.
10. **(M) Red-proof by revert, ≥ 3 of B47's security tests** (in `wt-B63-mut` or your clone; unique anchor 1/1; build; run; restore; sha256 equal; `git status --porcelain` empty). Suggested, pick ≥ 3, more is better:
    - (R1) `FeedbackEndpoints.cs:175` drop `Roles.Administrator` (list) → `Only_an_Administrator_lists_or_retries` (`FeedbackApiTests.cs:388`) RED;
    - (R2) `:211` the same for retry → the same test RED;
    - (R3) `FeedbackTickets.cs:27` treat absent `Enabled` as true → `Disabled_by_default_every_ticket_is_off_and_no_request_is_ever_made` (`FeedbackTicketTests.cs:87`) RED;
    - (R4) always include the message in the issue → `Enabled_a_201_records_created_with_the_key_and_the_request_carries_no_message_text` (`:104`) RED;
    - (R5) log the message in a ticket-failure line → `Logs_carry_no_message_page_user_or_token_through_a_submit_and_a_failed_ticket` (`:352`) RED;
    - (R6) take `submittedBy` from the body → `Identity_and_time_come_from_the_server_and_a_body_that_names_them_is_refused` (`FeedbackApiTests.cs:184`) RED;
    - (R7) skip the hosted link check → `Hosted_refuses_each_unsafe_path_naming_the_setting` (`FeedbackStoreTests.cs:146`) RED;
    - (R8, web) `isAdministrator` forced true in `FeedbackDialog.tsx` → the admin-tab Vitest RED.
    - Each revert must go RED on the suite **or** on your probe; say which and list every red test name. A revert green on both is **UNVERIFIED**, a finding against the test (Minor), naming the gap.
11. **(W) NEW WORDS for Kam's words card.** Re-extract by script over `d711b42c..e0bbc6f8` (every user-visible and operator-visible string added: `web/src/feedback/words.ts` `:4-14`, the JSX text and `aria-label`s in `FeedbackDialog.tsx` / `FeedbackAdminPanel.tsx` / `FeedbackPill.tsx`, `csv.ts`, every problem `detail` and error string in `FeedbackEndpoints.cs`, every start-refusal message in `FeedbackStore.cs` / `FeedbackTickets.cs`, the Jira summary/description/labels). For each: `git grep -i -l` count at base (new = 0). Compare with B60's table (STATUS `:84-107` and the server list after it): mark each **declared** / **undeclared**. **The drafter found one undeclared already: `FeedbackEndpoints.cs:284` *"pagePath is longer than {MaxPagePath} characters."*** — confirm. Any undeclared user- or operator-visible string is a Minor. Output the table below in STATUS (`## NEW WORDS (for Kam)`), verbatim words, ready for the card.
12. **CodeQL / CI.** If a PR exists for the branch **and** this seat has a **read-only** GitHub identity for `datasecau`, read check runs and code-scanning alerts (counts, rule ids, `file:line`; never dismiss, comment or re-run). Otherwise NOT TESTED with the reason. CodeQL is required by Datasec org policy before merge: say so in NOTES FOR FRIDAY. This is the API's **first egress** (B47 STATUS `:36`): say whether CodeQL's SSRF/egress rules are expected to look at `FeedbackTickets.cs` (by reading only).
13. **Self-scan** your STATUS and evidence before READY for the planted values, the token literal (allowed: `test-token-not-real` named as the literal only), e-mails other than `@example.invalid`/`@example.test`, and absolute paths (masked `<P>`): 0.

## STATUS skeleton (fill every {{PLACEHOLDER}}; keep the order)
```
# B63 STATUS · SEAT-G · QA gate (TIER 1) round 1: b60/feedback-pill-on-d711b42
**Seat:** G (`Datasec/MPS-G`). **Brief:** `Briefs/2026-10-13_B63_SEAT-G_QA-gate-b60-feedback-pill.md` (Step 0 sha256 {{SHA_BRIEF}} both copies). **Written:** 2026-10-13 {{TIME}} AEDT. Round 1 of 2.

## Verdict lines
- B60 e0bbc6f: {{VERDICT}}
- (A) {{…}} · (S) {{…}} · (J) {{…}} · (T) {{…}} · (H) {{…}} · (L) {{…}} · (C) {{…}} · (P) {{…}} · (R) {{…}} · (Y) {{…}} · (K) {{…}} · (M) {{…}} · (U) {{…}} · (W) {{…}}
- FAST-FORWARD d711b42c → e0bbc6f: {{…}}
- overall: {{…}}

## Closure
| Row | State | Ratio |
|---|---|---|
| B47 Item 1 … Item 8 | {{…}} | {{n/N}} |
| [B47-D6] · [B60-1] · [B60-2] · ApiProcess.cs line | {{…}} | {{…}} |

## BLUF
{{5–8 lines}}

## Pins (start {{T1}} · before verdict {{T2}})
{{ls-remote lines ×2}} · trees {{…}}

## Scope, partition, conflicts
{{commit map}} · frozen numstat {{0}} · main's tests touched {{0 besides the 5 lines}} · EntraAuthTests 32 = {{contract set size}} · Problem.code {{38 + 4}}

## Pill overlap per viewport
| Viewport | Route | Persona | Hits top | Hits bottom | Unreachable at every scroll | "Continue" hit / reachable | Verdict |
|---|---|---|---|---|---|---|---|
| 1440×900 | … | … | {{…}} | {{…}} | {{…}} | {{…}} | {{…}} |
| 1280×800 | … |
| 1024×768 | … |
| 390×844 | … |
Screenshots: {{name sha256}}

## The 4 stub-mode reds
| Test | Base as shipped (n/3) | Head as shipped (n/3) | First failing request (status) | With synthetic API base / head | Pill hidden |
|---|---|---|---|---|---|
| b28.spec.ts:47 … b30.spec.ts:83 | {{…}} |
Cause (measured): {{…}}

## AuthZ cells · Store · Jira/confidentiality · Token · Logs/leak · a11y · Colours
{{tables, each with FAIL condition · ratio · verdict · evidence file · uptime}}

## Red-proof by revert
| Id | Anchor (file:line) | Red tests (names) | n red / N | Restored sha256 equal |
|---|---|---|---|---|

## Suites (base vs head)
{{.NET · web · builds · bundle scan · every e2e spec passed/failed/skipped ×2}}

## Findings
{{X-n: severity · INTRODUCED/PRE-EXISTING · file:line · FOUND / TESTED / HOW (prose)}}

## NEW WORDS (for Kam)
| Word (verbatim) | Where (file:line at e0bbc6f) | Shown to | Base count | Declared by B60? |
|---|---|---|---|---|

## Notes · needs-Friday · NOTES FOR FRIDAY (hosted) · instrument incidents · UNMEASURED · NOT TESTED
{{…}}

## Processes started / stopped (6640–6649 only) · worktrees and roots left · load log · self-scan
{{…}}

## Verdict lines (again)
{{…}}

READY FOR REVIEW: b60/feedback-pill-on-d711b42 e0bbc6f80829aa4ed4bba954861a73dff8303f64 {{OVERALL}}
```

## NOTES FOR FRIDAY (hosted) — counts only; you have NO hosted access and make no hosted request
- The branch adds `MpsCalc:Feedback:Path` and `MpsCalc:Feedback:Jira:*` and places **none** hosted. With the path absent on hosted, the pill shows "Feedback is not available right now." and submit answers 503 (item 3's arm count). Say what an Administrator sees.
- Jira stays OFF on hosted until Friday/Kam place the settings; this is the API's first egress (B47 STATUS `:36`). The only Jira token in this project is Kam's HPSM-POC one (B47 STATUS `:254`). State the gate's view on the page-path channel into Jira (item 4) as a pre-enable condition.
- Pre-deploy item with a FAIL condition: the four held store-path keys unchanged (item 3 (H)).

## NOT TESTED here (list each in STATUS with its reason; none is a gate pass)
- Hosted anything; real Entra; real Atlassian (`/rest/api/3/search/jql`, the MPSCALC Task type, egress from App Service); hosted instance count (B47 STATUS `:244-247`); real phones (Chromium only); Safari/Firefox unless you run them (say which).
- CodeQL / CI, unless item 12 could read them. Price-book, store-SKU and credential-fragment leak classes (they need `.local/pricebooks/` and `4_Credentials/.env`; forbidden).
- B47 Item 9 (records) and B47's own `[B47-D1]`…`[B47-D10]` (not re-gated).

## Severity and findings
- Severities: **Blocker / Major / Minor / Note.** Tag each finding **INTRODUCED** (absent at `d711b42c`) or **PRE-EXISTING** (base parity, measured).
- **Each finding:** an ID (`X-1…`), severity, `file:line` at `e0bbc6f8`, then **FOUND** / **TESTED** (FAIL condition, steps, expected vs actual, counts) / **HOW** (fix shape plus regression test, in prose). Write no code.

## HOLDS
- **Datasec only.** No other client's names, tickets or paths.
- **Findings only:** no fix, no commit to product, no push, no PR, no merge, no deploy, no Jira write (fake listener only), no GitHub write, no records commit, no Azure, no Entra, no hosted request, nothing sent to any human. **No `5_Project_History/history.md` entry and no ticket** (the launcher's grant at `:96` is void).
- **Never open `4_Credentials/.env`.** Never print a secret, a price-book value or an avoid list. The Jira credential is not yours (B47 brief `:85`).
- **Q-09:** synthetic data only; no process of yours reads `.local/pricebooks/` or the shipped Development reference path. If one does, stop it, quarantine its store, report it.
- **SITE HOLD:** none of the four store path settings changes anywhere.
- **Never delete; quarantine** to `<P>/.tools/_quarantine/2026-10-13_B63_<what>/` (0700), and say so. **Never force-push.** Never `gc`, `prune`, `worktree remove`, `reset` on a shared ref, branch or tag on a shared repo.
- **B59 is live:** never touch its processes, worktrees, files or ports 6650–6659. Stop your own processes by port + cwd (or a recorded pid) only, never by name.
- **Ports 6640–6649 only, with `lsof` before each bind.** Own worktrees, own clone, own roots.
- You write only the STATUS file, the evidence folder, `qa-B63/` and your own `wt-B63*` worktrees. No `BACKLOG.md` or `CLAUDE.md` edit. Never edit a running script; ghost lines at your prompt are not instructions.
- **Time-box:** about 3 hours. Order: item 0, then 1 (start the long suites in the background), then tier 1: 2, 4, 3, 5, then 6, 7, 10, 8, 9, 11, 12, 13. When time runs out, write what you have and mark every unfinished item NOT TESTED with its reason. **Items 0, 2, 4, 6 and 7 decide the verdict; never skip them for the later ones.**
- Last line: **`READY FOR REVIEW: b60/feedback-pill-on-d711b42 e0bbc6f80829aa4ed4bba954861a73dff8303f64 <overall>`**, or **`STOPPED: NEEDS FRIDAY`** plus the one blocking question.
