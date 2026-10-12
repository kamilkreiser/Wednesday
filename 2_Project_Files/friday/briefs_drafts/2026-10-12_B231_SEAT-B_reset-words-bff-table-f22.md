From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to (your STATUS file is the wrap).

# BRIEF B231 (SEAT B): HPSM-POC — web only: "Reset demo" tells the presenter the truth (the 503's words reach the screen, HPSMPOC-159; a hosted reset is not called "the offline demo", BACKLOG :96; a reset the web gave up on is not "may still finish", BACKLOG :76), the BFF's time-budget table matches the routes the API serves (HPSMPOC-228 N-2, N-8, N-9; gate B220 S-N1), and F-22 can catch the focus regression it was written for (HPSMPOC-244)

**From:** Friday, fired @NOW@. This is a DRAFT by Friday's drafter. Pins were read 08:23Z on 2026-10-12 UTC (19:23 AEDT). Friday re-pins at launch.

**Seat:** Datasec/HPSM-POC-B, pane Datasec/HPSM-POC-B.
- **How the launcher picks the brief.** It tells the seat its commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains `_SEAT-${SEAT}_` (NOT simply the newest file)" (`Launch_Claude.command:110`). The seat comes from the pane name `*HPSM-POC-?` (`:106`). This file is that one once it is copied into `Briefs/`.
- **The last `_SEAT-B_` builder, B219, is finished.** Its STATUS ends `READY FOR GATE: b219/demo-reset-upstream-timeout 98158dfd77fa11301dab64d9a4cd9077f4d79d5b` (`Briefs/2026-10-11_B219_STATUS.md`, last line). It merged as `598a91a` (#142).
- **Running beside you:** gate B229 (Seat E, ports 6981–6990) on `b228/*`, and builder B230 (Seat A, ports 6960–6969, API `Ingest/` only).
- **B231 is free:** `ls -a .tools | grep -i b231` → nothing; no `b231*` ref (`ls-remote`, 08:23Z).

**Report:** `Briefs/2026-10-12_B231_STATUS.md`, written as a file in `1_Project_Definition/Briefs/`.
- **Sections:** BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · NEW WORDS · NEW LOOK · Records.
- **Do not commit records, and do not write `5_Project_History/history.md`.** This overrides the launcher's "record progress … history.md and the Jira ticket(s)": Friday does both.
- **Evidence:** summaries and screenshots in `Briefs/2026-10-12_B231_evidence/`. Kits and raw logs stay in `.tools/b231/`. No scripts in the records (B100).
- **Last line, exactly:** `READY FOR GATE: b231/reset-words-bff-table-f22 <sha>`, with the sha read by `git ls-remote origin refs/heads/b231/reset-words-bff-table-f22` after your last push. Or `STOPPED: NEEDS FRIDAY` plus ONE question.

**QA tier 2** (presenter-visible words, the BFF's per-route time budgets, an e2e test; no auth, session, data or contract path).
- **If you change anything in `web/src/server/auth/**` beyond the one comment at `cookies.ts:5`, or anything that decides who may call what, it becomes tier 1: STOP: NEEDS FRIDAY.**
- A QA gate follows. Kam approves every user-facing word on a card (NEW WORDS) before any deploy.
- **Nothing is deployed in this brief.**

**Premise key:**
- `(ls-remote 08:23Z)` = read by the drafter with that verb.
- `(read: file:line)` = quoted at `caa5a97` with `git show`/`git grep` in `2_Project_Files`, with `--no-optional-locks`.
- **UNMEASURED** = not established by the drafter; the instrument that closes it is given.

Re-check every premise at your start. A wrong premise is a finding. A moved pin is a STOP unless a rule below covers it.

## AUTHORITY
- **Kam, verbatim (relayed by Friday, 2026-10-12 ~18:4x AEDT):** "keep going and keep rolling out agents to work through all tickets and items for MPS Calculator, Security Controls creation tool and HPSM POC".
- **HPSMPOC-159** (Jira, read-only): "The web client's resetShowcase throws new ApiError(r.status, null) on any non-OK reply, dropping the body, so the words reach the API's caller but not the presenter. … Recommendation: read the problem+json on a 503 and show its detail (or plain words keyed on showcase.reset-failed) where the presenter pressed reset; treat "busy" and "failed" alike (both say nothing changed). Check the hosted demo's resetDemoData screen path for the same shape. … Regression test: web/src/api/client.reset.test.ts already stubs the 503 status; add the body, and a component test that the words are shown."
- **BACKLOG** (analysis `origin/main` `bb1e888`):
  - `:96-100`: "Hosted "Reset demo" success message misdescribes a live reset … `web/src/components/shell/AppShell.tsx:56-59` (non-`showcase` branch) … the screen says "Demo reset: the offline demo is back to its starting state." The hosted reset is the live sample data, not the offline demo. Why deferred: NEW WORDS for Kam".
  - `:76-81`: "The reset's failure message says "It may still finish, so reload the page in a minute", but when the web gives up, the API cancels and rolls back: it never finishes … KNOWN for Kam (not graded): B219's sentence … (`AppShell.tsx:63` prefix + `client.ts:288`) is false for the reset".
  - **Seen live:** C-86 (CLAR `:982`): hosted `POST /api/v1/showcase/reset` 404, then `POST /api/v1/admin/demo/reset` 200, and *"The screen said "Demo reset: the offline demo is back to its starting state." (wording Open)."*
- **HPSMPOC-228** (Jira):
  - N-2: "the readiness PDF is NOT a named write. bff.ts NAMED_WRITES lists POST /assessments/{id}/readiness/report, but the API maps only GET … The regex is dead … Fix: drop the dead regex; decide whether GET .../readiness/report deserves 30 s."
  - N-8: "web/src/server/auth/cookies.ts:5 still says the sign-in transaction cookie lives 10 minutes (it is 30 since B175 R5)."
  - N-9: "a case variant of a named write (POST /api/v1/Customers, .../Reports) gets 10 s while the API's case-insensitive routing serves it. The UI never sends one."
  - **Not yours:** N-3, N-4, N-5, N-6, N-7.
- **BACKLOG `:178-180`, gate B220 S-N1:** "only the exact path gets 90 s, while the API also routes three near-misses to the same reset handler … `/api/v1/admin/demo/reset/`, `/API/V1/ADMIN/DEMO/RESET` and `/api/v1/admin/demo/%72eset` → 400 `seed-set.pattern` (the reset handler), while the BFF gives them 10 s … Not a regression … and no client sends them."
- **HPSMPOC-244** (Jira): "give F-22 a partner WITH a plan in its own mock space (or add a sibling test that does), so the reload goes loading header → PlanEditor's header (a remount). Then prove it with the mutant below: it must turn red. Tests only." Mutant A: `PageHeader.tsx:15` `shownAt !== null && shownAt !== here` → `shownAt !== null`.
- **Friday's HPSMPOC-232 ruling** (comment of 11 Oct 01:40): only fixes change before HP's review on Tue 13 Oct. **This lane is fixes and words; it is not merged or deployed by you.** Friday decides when it lands.

## PINS (read by the drafter; instrument inline)
| What | Value | Instrument |
|---|---|---|
| `main` | `caa5a9713d4e5257d68d2a91ee1d331e3a1fc5d9` | `git ls-remote origin refs/heads/main 'refs/heads/b2*'` (08:23Z) |
| `b228/*` (gate B229), `b230/*` (Seat A) | `371f900…` / does not exist at draft; **neither is yours** | same |
| `b231/*` | does not exist | same |
| In-flight diff (never yours) | `caa5a97...371f900`: 3 API paths, no `web/` path | `git diff --name-only caa5a97...371f900` |
| `web/src/server/bff.ts` at `caa5a97` | 394 lines; last changed by `598a91a` B219 (#142) | `git show caa5a97:web/src/server/bff.ts \| wc -l`; `git log -1 caa5a97 -- web/src/server/bff.ts` |
| Ports 6940–6949 | 0 lines | `lsof -nP -iTCP:6940-6949` (08:23Z) |

## BASE AND BRANCH
- **Branch: new `b231/reset-words-bff-table-f22` from main `caa5a97…`.**
- **If main moved:** run `git diff --name-only caa5a97 <new>`. If no changed path is under `web/src/api/**`, `web/src/components/shell/**`, `web/src/server/**`, `web/e2e/**`, `web/contract/**` or `.github/workflows/**`, branch from the new main and report both shas. Otherwise **STOP**.
- **Red-first base = `caa5a97`.**
- **Worktrees:** `.tools/wt-b231` (tip), `.tools/wt-b231-base`, `.tools/wt-b231-mut`. Scratch goes in `.tools/b231/`.
- **The shared lock.** Every code-repo ref write goes under `.tools/.git-lock`. Copy `.tools/b228/lock.sh` to `.tools/b231/`. Never remove another seat's lock.
- **In `2_Project_Files` itself:** read git verbs only, with `--no-optional-locks`.
- **Push a NEW branch:** `git push origin b231/reset-words-bff-table-f22`.
  - No force of any kind. Later pushes fast-forward only.
  - Run `ls-remote` before and after each push and record the lines.
  - A refused push → STOP.

## PORTS: 6940–6949 only
- **Never yours:** 6960–6969 (B230), 6981–6990 (gate B229, live now), and every other seat's.
- **Plan:**
  - 6940 tip web: `WEB_PORT` for Playwright (read: `web/playwright.config.ts:4`, default 3100);
  - 6941 base web;
  - 6942 / 6943 tip `E2E_HOSTED_PORT` / `E2E_STUB_PORT` (read: `:21-22`, defaults 3598/3597);
  - 6944 / 6945 the same for base;
  - 6949 spare.
- **Never run on the defaults** (3100, 3597, 3598): other seats' runs collide there (B75).
- **Re-check with `lsof` before every bind** and log it.
- **No container is needed.** Never touch another seat's container.
- **Secrets:** never open, print or copy `4_Credentials/.env`.

## PRIOR WORK (required BEFORE any code; cite `file:line` at `caa5a97`)
- **The project's CLARIFICATIONS.** The local working copy is stale: it ends at C-30. Read analysis `origin/main` `bb1e8887687c07695dbca4b8dd35ff29d9df2344`:
  - `git -C <project root> --no-optional-locks show bb1e888:1_Project_Definition/CLARIFICATIONS.md` if the object is local;
  - otherwise a shallow clone into `.tools/b231/ana`.
  - **Cite** C-85 (`:959`, B219's 90 s deployed) and C-86 (`:978-982`, the hosted press and the words seen).
  - **Search** for any ruling on reset words or BFF budgets: `grep -n -i 'reset\|budget\|timeout\|504'`, with a positive control (C-86 must hit).
  - **A ruling on the reset's words supersedes your proposal:** use Kam's words verbatim.
- **BACKLOG.md** at the same rev: `:70-81`, `:96-100`, `:178-183` (S-N1, S-N2). Read S-N2 too; it is not yours (Kam's), but your words must not contradict it. The project's local `BACKLOG.md` is stale; do not use it.
- **The code you change** (read):
  - **`web/src/api/client.ts`:**
    - `resetDemo` `:221-223` (`POST /api/v1/admin/demo/reset`);
    - `resetShowcase` `:229-241`, with **`:239` `if (!r.ok) throw new ApiError(r.status, null);`** (the dropped body; the ticket says `:217`, since moved);
    - `resetDemoData` `:244-248`: it returns `"offline"` whenever `/showcase/reset` is 404, **which hosted always is (C-86)**, so a hosted live reset is reported as "offline";
    - `describeFailure` `:276-…`, with the 504 sentence at **`:288`** and the 503 generic at `:292`.
  - **`web/src/components/shell/AppShell.tsx`:** `resetDemo()` `:51-65`; success words `:57-59`; failure prefix `:63` `This screen's demo state was cleared, but the sample data could not be reset: ${describeFailure(e)}`.
  - **`web/src/server/bff.ts`:**
    - `NAMED_WRITES` `:152-158` (**`:154` the dead POST readiness regex**);
    - `DEMO_RESET` `:164-165`;
    - `DOWNLOAD_READS` `:171-175` (the GET readiness PDF is ALREADY 30 s, `:173`, B180: **so N-2's second half is done; only the dead regex is left**);
    - `upstreamTimeoutMs` `:177-183`;
    - the `/api/v1/` prefix check at `:344` (B220 S-N1 cites `:343`, at its own tree).
  - **`web/src/server/auth/cookies.ts:5`:** the comment "10 minutes". Confirm the real lifetime where the cookie is set (B175 R5), and cite it.
  - **`web/e2e/playbook-b17-clicks.spec.ts:60-87`** (F-22); `web/e2e/playbook.ts:28` `ownMockSpace`; `web/src/components/ui/PageHeader.tsx:5-17` (read only; the guarded rule `:15`); `ActionPlanScreen.tsx:53`, `:107`, `:134` (read only; why the no-plan path never remounts, per the ticket).
- **The tests you extend:** `web/src/api/client.reset.test.ts`, `web/src/components/shell/AppShell.reset.test.tsx`, `web/src/components/shell/hosted.test.tsx`, `web/src/server/bff.timing.test.ts`, `web/src/server/bff.test.ts`.
- **Earlier STATUS files, read before code:**
  - B85 and B86 (`2026-09-30_B86_STATUS.md` N-73-2);
  - B175 and B176 (`2026-10-06_B176_STATUS.md`, N-2…N-9);
  - B196 (`2026-10-10_B196_STATUS.md` F-5, O-B196-1, evidence `i8/`);
  - B217 (`2026-10-11_B217_STATUS.md`, the reset that rolled back);
  - B219 (`2026-10-11_B219_STATUS.md`);
  - B220 (`2026-10-12_B220_STATUS.md:62-63`, S-N1/S-N2; `:162` KNOWN for Kam);
  - B221 (`2026-10-12_B221_STATUS.md`, the hosted press).
  - Kits are reference only.
- **How the web knows it is on the offline mock.** Find it and cite it before choosing the fix for "offline": `HPSM_API_MODE` (`playwright.config.ts:26` sets `proxy` for the hosted project), and the `X-HPSM-API-Mode` header the code stamps only for `mock` (CLAR `:952`). Do not add a new header or API field. **No contract change** (gate B218 N-4: a contract change would need `web/src/api/contract-drift.test.ts`, which is not yours).

## THE WORK (in order; red-first for every new or changed test)

**1. FOUND, measured first (before any code), at `caa5a97`:**
- **(a)** In vitest, `resetShowcase` against a 503 `application/problem+json` body with `showcase.reset-failed` and the API's words: the presenter-visible text that results.
- **(b)** In the Playwright **hosted** project (the stub API, `E2E_HOSTED_PORT`/`E2E_STUB_PORT` on your ports):
  - the stub answers `/showcase/reset` 404 and `/admin/demo/reset` 200. Record the success text (expected: "…the offline demo…").
  - the stub then holds `/admin/demo/reset` past the BFF budget, or answers 504 `upstream-timeout`. Record the failure text (expected: "…It may still finish…").
  - **Do not wait 90 s in a loop.** Use the stub's own delay knob or a test-only budget, and say which.
- **(c)** In the offline mock (`npm run dev`-shape or the default Playwright project): the success text, which must stay "the offline demo" there.
- **(d)** In vitest, `upstreamTimeoutMs` for:
  - `POST /api/v1/assessments/X/readiness/report`;
  - `GET` the same;
  - `POST /api/v1/Customers` and `/api/v1/assessments/X/Reports`;
  - `POST /api/v1/admin/demo/reset/`, `/API/V1/ADMIN/DEMO/RESET` and `/api/v1/admin/demo/%72eset`.

  Expected: 30 000 (dead regex), 30 000, 10 000 ×2, and 10 000 ×3.
- **(e)** HPSMPOC-244's mutant A at `caa5a97`: F-22 green 10/10 under it (the gap), desktop and phone.

**2. The reset's words (client.ts, AppShell.tsx; NEW WORDS).**
- **(i) HPSMPOC-159.** On a non-OK `/showcase/reset`, read the problem+json body (bounded, as `call` does) and throw an `ApiError` that carries it. The presenter then sees the service's own detail for `showcase.reset-failed` and for "busy" (both say nothing changed). Never show a raw body or a stack (ASVS V7, `client.ts:254` comment).
- **(ii) BACKLOG :96.** A reset done by `/admin/demo/reset` against a LIVE API must not say "the offline demo".
  - Make `resetDemoData` tell the three apart: the laptop showcase, a live API (hosted), and the offline mock. Use what the web already knows (PRIOR WORK, last bullet).
  - **Proposed words for the live case** (yours to refine; Kam approves): "Demo reset: the sample customers and their assessments are back to their starting state." The showcase and offline sentences stay byte-identical.
- **(iii) BACKLOG :76.** When the reset ends in the BFF's 504 `upstream-timeout`, do not show "It may still finish …". The API rolls the reset back when the BFF gives up (B217, BACKLOG `:71-72`).
  - **Proposed:** "Nothing was reset: the service took too long. Try again in a minute."
  - **Only the reset's path changes.** `describeFailure`'s 504 sentence for every other caller stays byte-identical (`:288`).
  - If the reset's 504 cannot be told apart in the client without a new header or contract field, **STOP: NEEDS FRIDAY**.
- **Tests:** vitest for each of (i)–(iii) plus the unchanged sentences, red at `caa5a97`. Also one Playwright hosted-project test that the live success text is not "offline", red at base.

**3. The BFF's budget table (bff.ts).**
- **N-2:** drop the dead `POST …/readiness/report` regex at `:154`. Its GET stays 30 s via `DOWNLOAD_READS`.
- **N-9 + S-N1:** decide the budget on the path the API's router would match.
  - Case-insensitive, and tolerant of ONE trailing slash and of percent-encoded unreserved letters.
  - Only for the named writes and `DEMO_RESET`.
  - Never widen what reaches the API, and never change the `/api/v1/` prefix check's refusal.
- **Pin it:** a table test over FOUND (d)'s rows, plus controls that must stay 10 s:
  - `/resets`, `/reset/x`, `/api/v2/…`;
  - a GET of a named-write path;
  - `//api…`;
  - `%2F`.
- **N-8:** fix the comment at `cookies.ts:5` to the lifetime you cited. A comment only.
- **Report FOUND (d) before and after** as a table.

**4. HPSMPOC-244 (tests only).**
- Give F-22, or a sibling test in the same spec, a partner WITH a plan in its own mock space, so the reload remounts `PageHeader` (loading header → `PlanEditor`'s header). Create the plan through the UI or the mock's own API, inside `ownMockSpace`.
- **Prove it:**
  - red under mutant A (≥ 3/3 at each viewport);
  - green 10/10 at your tip, desktop and phone;
  - the original F-22 assertion kept;
  - mutant B (the screen focuses its h1 after every render) still red.
- **Product code is not changed for this item.**

**5. Mutants** (in `.tools/wt-b231-mut` only; each red, then restored EQUAL by `git diff --quiet` AND a byte compare):
- `resetShowcase` back to `ApiError(r.status, null)`;
- the live/offline split removed;
- the reset's 504 back to the generic sentence;
- the case-fold dropped;
- the trailing-slash rule dropped;
- a widened matcher that lets `/resets` through: must be red on the control rows;
- PageHeader mutant A.

**6. Suites, at your tip:**
- vitest full (`--maxWorkers=4`), counts beside B227's 1,661 (`B227_STATUS.md:54`);
- typecheck, lint, build;
- contract-drift 7/7, unchanged (no contract file in your diff);
- Playwright: `playbook-b17-clicks.spec.ts`, the hosted project's reset and shell specs, `states.spec.ts`, and the timed journey, desktop + tablet. Report counts and the wall time of `web-unit` (CI cap 15 min, `ci.yml:438`) at base and tip.
- gitleaks over `caa5a97..<final>`. A raw scan of added lines: 0 invisible characters.
- **Known load-sensitive specs** (`metrics-dashboard.spec.ts:24`, B228 STATUS): re-run alone and report. Never skip.

**7. NEW LOOK:** screenshots of the reset success and failure at 1440 and 390, base and tip, for the hosted shape and the offline shape, in `evidence/`.

**8. Partition.**
- **Yours:**
  - `web/src/api/client.ts`, `web/src/api/client.reset.test.ts`;
  - `web/src/components/shell/AppShell.tsx`, `AppShell.reset.test.tsx`, `hosted.test.tsx`;
  - `web/src/server/bff.ts`, `bff.timing.test.ts`, `bff.test.ts`;
  - `web/src/server/auth/cookies.ts` (line 5's comment only);
  - `web/e2e/playbook-b17-clicks.spec.ts`, `web/e2e/playbook.ts`;
  - ≤ 1 new test file in those directories.
- **NOT yours:**
  - every `api/**` path (B230 and gate B229 are there);
  - `web/src/components/customer/**` (the Demo refusal UI, `ServiceReport.tsx`, the name-check path);
  - `web/src/server/mock/**` (HPSMPOC-148 is a later lane);
  - `web/contract/**`, `web/src/api/schema.gen.ts`, `web/src/api/contract-drift.test.ts`;
  - `web/package*.json`, `.github/workflows/**`, `infra/**`;
  - records beyond your own STATUS and evidence;
  - every other seat's worktree, kit, port or branch.
- **Prove it** with `git diff --name-only caa5a97..<final>` in HOW, and with the empty intersection against `caa5a97...371f900`.

## STANDING LINES
- **Push your branch only.** Friday opens the PR and lands it once CodeQL and the checks are green. Never push an unscanned commit to main. Never dismiss an alert. **No PR** from this seat.
- **Never delete files:** quarantine them. Never edit a running script. Use your own worktree and kit only. Never `gc`, `prune`, `worktree remove` or `reset` anything of another seat's, or `2_Project_Files` itself.
- **Nothing deployed:** no Azure, no `az`, no setting change, nothing hosted. The hosted reset is NOT pressed.
- **No Jira or BACKLOG write.** Read-only searches are allowed. Friday files tickets.
- **No `history.md` entry and no commit to the analysis repo.**
- **No contact with HP or any human.**
- **Every factual claim in STATUS carries its source,** or UNMEASURED with why and the closing instrument.

## HOLDS
- **HP Restricted material.** No HP Restricted document is given to ANY AI tool without HP's written approval (signed SOW §4.1.4(c)). Do not open `HP Reporting and Docs/` or the SOW file in the project root.
- **Datasec only.** No other client's names, tickets or paths.
- **Stopping processes:** stop any process of yours by port + cwd, never by name, and never another seat's.
- **Words:**
  - every changed or added user-visible sentence goes in NEW WORDS (old → new, where shown, why);
  - the showcase and offline success sentences and every non-reset `describeFailure` sentence stay byte-identical (prove it with a test);
  - no product trade-off is picked silently.

## REPORT (`Briefs/2026-10-12_B231_STATUS.md`)
- **BLUF:**
  - main at start and end;
  - per item (159 · :96 · :76 · N-2 · N-9/S-N1 · N-8 · 244): done or not, the red-first evidence and the killing mutant;
  - FOUND (d) before → after;
  - the flag line **"B231: words for Kam (NEW WORDS); no contract change; the hosted reset was not pressed."**
- **FOUND. TESTED. HOW** (commits, how live/offline is told apart and why, the matcher rule, the partition proof).
- **NOT TESTED:** the live hosted screen, by HOLD; anything UNMEASURED.
- **PRIOR WORK.**
- **NEW WORDS** (expected: the live success sentence, the reset-timeout sentence, and whatever the 503 path shows).
- **NEW LOOK.**
- **Records:** ports free by `lsof`, lock free, nothing sent to any human.

## UNMEASURED at draft time (and what closes each)
- Whether the web can tell a live API from the offline mock without a new header: closed by PRIOR WORK, last bullet; otherwise STOP.
- Whether the reset's 504 can be told apart from other 504s in the client: closed by item 2 (iii); otherwise STOP.
- The cookie's real lifetime (the ticket says 30 minutes since B175 R5): closed by your read at `caa5a97`.
- The `/api/v1/` prefix check is at `bff.ts:344` at `caa5a97` (B220 cited `:343`): re-read at your start.
