From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to.

# BRIEF B208 (SEAT A): HPSM-POC — the customer page FRAME (breadcrumb + journey rail) shows the alias to Demo callers on every customer page; partners without Demo keep names
**From:** Friday, ~17:10 2026-10-11. **Seat:** Datasec/HPSM-POC-A, pane Datasec/HPSM-POC-A. The project's own launcher picks the newest `Briefs/` file containing `_SEAT-A_` (`Launch_Claude.command:110`); this brief is that file. Report `Briefs/2026-10-11_B208_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · NEW WORDS · Records). Last line `READY FOR GATE — b208/customer-frame-alias @ <sha>` (the sha read by `ls-remote` after your last push) or `STOPPED: NEEDS FRIDAY` + one question.
**Tier 1** (data leaving the partner: what a Demo caller, i.e. HP at the event, sees of a customer). A QA gate follows; then Kam sees screenshots; then Friday deploys. **Deploy is NOT in this brief.**

**Premise key:** every pin below was read by Friday with the instrument named inline. If any premise does not hold at your start, say which in BLUF and follow the rule given for it; where no rule is given, STOP.

## AUTHORITY (Kam's ruling, verbatim)
- Live board, 2026-10-11 16:30:41, view=friday: **"Decision hpsmpoc-page-frame-names-for-demo-1011: b — Alias the page frame for Demo logins before Tuesday (recommended)"**. The card's option text: *"The breadcrumb and rail show ORG-nnnnn to Demo; partners still see their own names."*
- Standing, unchanged: `hpsmpoc-customer-names-alias-1011` → **(a) "Keep names; alias wherever data leaves the partner"**: *"ORG-nnnnn on anything HP or an export sees."* (Ruled 2026-10-11T12:50:18+11:00; relayed in B207's brief :10.) Friday's Q-B207-1 ruling (a) (B207 STATUS :233-236): the linked page's customer line shows the alias when the caller holds Demo, the name for a Partner without Demo.
- **Kam's words are "the page frame".** Read them as: what `CustomerShell.tsx` renders around every customer page, outside `<main id="main">` (the breadcrumb and the journey rail, plus anything else the shell itself prints), and the document title. The screens inside `<main>` are NOT the frame (see item 3).

## WHERE THIS COMES FROM (read these whole, first)
- `Briefs/2026-10-11_B207_STATUS.md`, especially ADDENDUM-1 **FOUND A1-F1** (:253-256): on `/customers/{id}/metrics` the eyebrow reads `ORG-00004`, but the shell shows "Customers › **Banksia Manufacturing (sample)** › Metrics" (breadcrumb) and "**Banksia Manufacturing (sample)** · Manufacturing" (journey rail), for Demo and Partner, at both widths; and A1-F3 (:258: in the laptop showcase a Partner sign-in is Partner+Demo at the service, so it sees the alias too).
- `Briefs/2026-10-11_B204_R2_STATUS.md` **A1-F1** (:69: the breadcrumb names the customer in all 56 linked-page runs, every caller, Demo included) and **R2-N1** (:70-74: `getCustomer` answers a Demo caller with the name). **R2-N1 stays a note: `getCustomer`'s API body is OUT of scope.**
- `Briefs/2026-10-11_B209_STATUS.md` (the server-said mode: `ApiModeProvider` / `useApiModeHint`, `components/shell/ApiMode.tsx`; `useCustomerShownAs` skips `getMe` when the hint is `"mock"`, so the offline demo logs no 404; the timed journey counts console errors, `journey.spec.ts:35`).

## PINS (Friday read each one, 2026-10-11 06:06–06:10Z; instrument inline)
| What | Value | Instrument |
|---|---|---|
| `main` | `ef69c4cf8611d0739c3cc43ef237c052e77bdf9c` (PR #137 squash: "B202/B207: attribution keys + 'Preview: next phase' page, aliases on metrics …") | `friday_as.sh datasec gh api repos/datasecau/HPSM-POC/commits/main --jq .sha` (06:06Z); `git -C 2_Project_Files --no-optional-locks ls-remote origin refs/heads/main` (06:06:40Z) |
| PR #137 | closed, merged 2026-10-11T06:05:17Z, `merge_commit_sha` `ef69c4c…`, head `c6c0c925a4df4d6c4bbfb382b0331ea92d3117fa` (B209's tip) | `friday_as.sh datasec gh api repos/datasecau/HPSM-POC/pulls/137` (06:10Z) |
| main's parent / tree | parent `76acd696a1c99aa449cc040ac11e852648d95efe` (B203, #136); tree `c57c071d3536846313c4e034a95e41e986cf1055`, the prefix B209 STATUS :28 gives for `merge-tree 76acd69 c6c0c92` | `git rev-parse 'ef69c4c^{tree}' 'ef69c4c^'` in Friday's scratch `clone --shared` after a fetch of main |
| Open PRs | none | `friday_as.sh … gh api repos/datasecau/HPSM-POC/pulls` (06:10Z) → empty |
| `b208/customer-frame-alias` | **does not exist** | `ls-remote origin 'refs/heads/b2*'` (06:06:40Z): no `b208/` line |
| `ef69c4c` in `2_Project_Files`' object store | **NOT present** | `git --no-optional-locks cat-file -t ef69c4c…` → "could not get object info" (06:06Z). **So you need one fetch of `main`; take the lock for it.** |
| `.tools/wt-b208`, `.tools/b208/` | do not exist | `ls .tools` (06:08Z) |

**At your start, re-read main** (`ls-remote`): `ef69c4c` → proceed. Moved → read the new commit's files (`git diff --name-only ef69c4c <new>`); if none is under `web/src/components/shell/**`, `web/src/components/customer/**`, `web/src/lib/attribution-preview.ts` or `web/e2e/**`, base on `ef69c4c` anyway and report a read-only `git merge-tree --write-tree <new main> <your tip>` in BLUF; otherwise **STOP**.

## BASE
- Branch **`b208/customer-frame-alias`** from **`ef69c4cf8611d0739c3cc43ef237c052e77bdf9c`**. Worktree `.tools/wt-b208`; scratch `.tools/b208/`. Every code-repo ref write (fetch, worktree add, branch create, commit, push) under the shared lock `.tools/.git-lock` (copy `.tools/b209/lock.sh` to `.tools/b208/`; never remove another seat's lock). In `2_Project_Files` itself, read git verbs only, with `--no-optional-locks`.
- Push a NEW branch: `git push origin b208/customer-frame-alias` (no `--force`, no `--force-with-lease`, no `+refspec`); every later push a fast-forward. `ls-remote` before and after each push; record the lines. A refused push → STOP.

## PORTS: 6770–6779 only
Friday checked, 2026-10-11T06:08Z: `lsof -nP -iTCP -sTCP:LISTEN` → in 6500–6999 only 6750, 6751, 6752, 6761, 6762 are listening (another project's live seats; also live elsewhere: 6620–6629, 6640–6649, 6750–6769); `lsof -nP -iTCP:6770-6789` → 0 lines; `docker inspect` of every container's `HostConfig.PortBindings` (running and stopped) → none binds 6770–6789 (HPSM-POC's stopped containers hold 6663, 6670–6674, 6681–6683, 6691, 6720–6721, 6740–6741: never start, reuse or remove them); a grep of every `Briefs/*.md` for 677x–68xx → no brief allocates them. Seat D (B206) has 6780–6789. Plan: 6770 / 6771 web head / mutant, 6772 API (proxy-mode probe, if needed), 6773 OIDC stub if needed, 6774–6777 Playwright, 6778–6779 spare. **Re-check with `lsof` before every bind** and state the checks in STATUS.

## THE WORK (in order; red-first for every new test: its log red, then green)
1. **Measure first (FOUND, before any code), at `ef69c4c`:**
   - Every place the frame prints the customer: `CustomerShell.tsx:56-57` (`crumbs`: the customer crumb `c.name`, alone on the overview, a link on every other page), `:178` (the rail's `<CustomerName name={customer.name} industry={customer.industry} />`, lg and up). Confirm nothing else the shell renders names the customer: the phone `<select>` (`:139-158`), the tabs (`:159-174`), the draft-rules note (`:131-136`), the loading / not-found / load-failed states (`:98-111`).
   - The document title: Friday read each `customers/[customerId]/**/page.tsx` `metadata.title` (static strings, e.g. "Automation metrics"; template `"%s · Security Services Playbook (POC)"` at `web/src/app/layout.tsx:8`) and found no `document.title` write in `web/src` (`git grep` at `ef69c4c`). Confirm it rendered, on every customer page, for a Demo caller.
   - Then **list every OTHER visible element on customer pages that names the customer to a Demo caller** (item 3). Friday's read-only `git grep` at `ef69c4c` already finds, for you to confirm and complete: the eyebrows built from `CustomerName` (`AssessmentScreen.tsx:57, :82`, `ConversationCoach.tsx:154`, `DocumentGeneration.tsx:100`, `FindingDetail.tsx:50, :105`, `FirmwareTask.tsx:87`, `NarrativeScreen.tsx:42, :60`, `NextEngagementScreen.tsx:21`, `ProfileScreen.tsx:20, :25`, `RecommendationScreen.tsx:42`, `ReportScreen.tsx:168, :180`, `ResultsScreen.tsx:27`, `RoadmapScreen.tsx:62`); the overview's h1 and "Customer name" row (`EngagementOverview.tsx:116, :136`); `ReportScreen.tsx:65, :78`; `DocumentGeneration.tsx:170`; `FirmwareTask.tsx:119`; `ApiSteps.tsx:100`; the coach and narrative texts that take `customer.name` (`ConversationCoach.tsx:151, :158`, `NarrativeScreen.tsx:47, :62`); the `/customers` list itself; and **the executive report PDF a Demo user can download**: `downloadReport` is on the `read` group (`AssessmentModule.cs:252`; `Roles.ReadRoles` includes Demo, `Caller.cs:42`) and its file name is `executive-report-{Slug(customer)}-{date}.pdf` (`ReportingEndpoints.cs:414-415`). Whether the PDF's own pages name the customer is UNMEASURED: closed by your generating one in the mock or showcase and reading its text (do not open any HP document).
2. **Build: the frame, every customer page, Demo only.**
   - The shell takes the SAME answer the metrics page takes: `useCustomerShownAs(customer.apiId ?? customer.id)` (`components/customer/useCustomerShownAs.ts:22-35`), which already reads the service's roles through `getMe` and skips `getMe` when `useApiModeHint()` is `"mock"` (B209). **Reuse it; do not add a role source, setting, env name or flag.** If the shell's use needs a change to the hook, keep the metrics page's behaviour byte-for-byte (B207's `MetricsScreen.alias.test.tsx`, all 16 cases, unchanged and green).
   - **Demo** (`kind: "alias"`): the customer crumb and the rail's customer line read the alias (`aliasLabel`, `web/src/lib/attribution-preview.ts:77`; null → `NO_ALIAS_LABEL` "No alias (made before the keys)", :72). **No run** (`kind: "no-run"`): `NO_RUN_ALIAS_LABEL` "Alias not available yet (no scored run)" (:75). Reuse B207's words; add new words only if a crumb needs a shorter form, and list them as PROPOSED.
   - The rail's industry beside the alias: decide whether it shows (B200's industry is display data, not a name) and say why under NEW WORDS; Kam's option text names only the name.
   - **No name while pending, and none on failure:** while `pending`, and when `getMe` or `getMetricsSummary` fails (the hook then stays `pending`), the customer crumb and the rail line show neither the name nor an alias (a neutral placeholder, or nothing; keep the crumb's link target and the breadcrumb's layout stable). Test it with each call held and each failing (500 and network).
   - **Partners without Demo, Admin, Consultant** (`kind: "name"`): exactly as today. In the offline demo the session role decides (B209), so Demo there reads the alias and Partner the name.
   - **Every customer page**, not only `/metrics`: overview, profile, assessment, results, findings and one finding, narrative, report, recommendation, next-engagement, roadmap, documents, coach, metrics, tasks/firmware-risk (the routes under `web/src/app/(app)/customers/[customerId]/`).
   - **Do NOT change `customer.name` in `CustomerProvider`'s value** (`CustomerShell.tsx:127`): every screen reads it, and aliasing it would change screens beyond the frame and the partner's own names. The alias is applied only where the shell itself renders.
   - The extra call per customer page: show it does not add a console error or a 4xx in the offline demo (the timed journey, B209's check), and measure whether it moves any span of the timed journey (`E2E_TIMED=only`, desktop + tablet).
3. **Beyond the frame: FINDINGS for Friday, NOT built.** Each element from item 1 that is not in the frame goes in a FOUND table: element · page(s) · `file:line` · Demo sees the name (measured yes / no) · fix-shape in one line. Alias nothing outside the frame. If you believe the ruling cannot be met without changing something outside the frame, STOP and ask.
4. **Tests (red-first):**
   - **vitest** (`CustomerShell.*.test.tsx`, a new `CustomerShell.alias.test.tsx`): under `ApiModeProvider` "api" and "mock", for Partner+Demo, Demo, Admin+Demo → alias in crumb AND rail, no name anywhere in the shell; Partner, Admin, Consultant → the name, and `getMetricsSummary` not called; pre-key → its words; no run → its words; pending, then `getMe` failing, then the summary failing → no name and no alias. RED against `ef69c4c`'s shell, green after. Every existing shell test you change is listed in HOW with why.
   - **e2e** (a new spec or `metrics-dashboard.spec.ts`): Demo opens at least three customer pages (the overview, one journey step, `/metrics`) directly and by navigation; asserts the breadcrumb and rail show the alias and the page's frame holds no customer name, no `/api/v1/me` request in the offline demo, and no console error. Partner: the name. At 1440 and 390. RED at `ef69c4c`, green after.
   - **Mutants** (each red, then restored EQUAL by `git diff --quiet` AND a byte compare with a new mtime, B207 FOUND 1): the shell ignores the hook (name always); the shell shows the name while pending; the shell shows the name on a failed `getMe`; the Demo check reads Partner; the rail aliased but the crumb not; the crumb aliased on `/metrics` only.
   - **Rendered-lines probe** (as B207 item 3): every rendered line of the frame for Demo on every customer page, 1440 and 390: 0 customer names; and the NEW WORDS table covers every frame line.
5. **Screenshots:** before (`ef69c4c`) and after, at **1440 and 390**, **Demo and Partner**, at least the overview and `/metrics`: offline demo (mock build) AND the live-showcase shape (API default user Partner+Demo, web in proxy mode, as B207's `item5/shots/`). Say for each which caller the SERVICE saw (A1-F3: in the showcase a Partner sign-in is Partner+Demo and so sees the alias).
6. **Partition.**
   - **Yours:** `web/src/components/shell/CustomerShell.tsx` and its tests; `web/src/components/customer/useCustomerShownAs.ts` (only if needed, see item 2); `web/src/components/customer/parts.tsx` (`Breadcrumbs`, only if needed); `web/src/lib/attribution-preview.ts` (words only, if needed); new or changed tests under `web/src/**` and `web/e2e/**` for these.
   - **NOT yours — Seat D (B206, running in parallel):** everything under `api/`; `web/contract/**`; `web/src/api/schema.gen.ts`; `web/src/api/contract-drift.test.ts`; `.tools/wt-b206`, `.tools/b206/`, ports 6780–6789. You change no API, contract, migration or Persistence file; prove it with `git diff --name-only ef69c4c..<final>` (0 under `api/`, `web/contract/`, `web/src/api/`).
   - **Not yours either:** the screens under `web/src/components/screens/**` and `web/src/components/customer/*.tsx` other than the two named above (item 3 is report-only), `ApiMode.tsx` and `bff.ts` (reuse, do not change; if you must, STOP and ask), and every other seat's worktree, kit, container or port.
7. **Suites and report.** vitest (full, `--maxWorkers=4`), typecheck, lint, build; Playwright: your new spec plus metrics-dashboard, journey (`E2E_TIMED=only`, desktop + tablet), a11y, responsive, nav-dead-ends at 1440 and 390; the hosted project (standalone server, proxy to the Entra stub) as B209 ran it; gitleaks over `ef69c4c..<final>`; a raw scan of the added lines with Python (not BSD grep, B205 N-4). Known flakes (HPSMPOC-247 `ImportRobustnessTests.R2_2`; the timing windows) are re-run alone and reported, never skipped.

## PRIOR WORK (cite file:line at `ef69c4c` in your PRIOR WORK; Friday read these)
`CustomerShell.tsx:52-65` (`crumbs`), `:82-94` (the `getCustomer` load and the API-only name), `:98-111` (load states), `:127` (`CustomerProvider`), `:130` (Breadcrumbs), `:178` (rail customer line), `:219` (`<main id="main">`); `useCustomerShownAs.ts:16-35`; `ApiMode.tsx:9-17`; `(app)/layout.tsx:12` (`ApiModeProvider` around `AppShell`); `customers/[customerId]/layout.tsx:9`; `CustomerName.tsx:5-8`; `MetricsScreen.tsx:21-26, :40, :49`; `attribution-preview.ts:72, :75, :77`; `parts.tsx:50` (`Breadcrumbs`); `web/src/app/layout.tsx:8`; `ReportingEndpoints.cs:414-415`; `AssessmentModule.cs:201, :252`; `Caller.cs:42`. The tests that render the shell today: `CustomerShell.b24/.b45/.b59.test.tsx` and the screen tests that wrap it (`git grep -c CustomerShell` at `ef69c4c`: ApiProfile, ConversationCoach, DocumentGeneration, EngagementOverview, FindingDetail, FindingOverride, FirmwareTask, LoadFailed.states, industries, ClientPacks).

## HOLDS (verbatim from B207, then the lines for this round)
- No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool — Claude seats, subagents, the product's model, Ornith or the Spark — without HP's written approval (signed SOW §4.1.4(c)).
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert. **Friday opens the PR.**
- No deploy, no Azure, no setting change; nothing to HP or any human.
- Never delete; quarantine.
- Never print a secret.
- Scoring/priorities unchanged (industry ruling a). No real revenue, no HP data feed, no HP partner id. No AI narrative touches the preview.
- *(B207)* Stop any process of yours by port + cwd (check its working directory first); never by name; never another seat's.
- *(B207)* No force-push of any kind, no branch delete, no history rewrite.
- *(Added)* `getCustomer`'s API body is out of scope (B204 R2-N1 stays a note). No screen inside `<main>` is aliased (item 3).

## REPORT
`Briefs/2026-10-11_B208_STATUS.md`, evidence `Briefs/2026-10-11_B208_evidence/` (summaries; kits and raw logs stay in `.tools/b208/`, no scripts in records, B100):
- **BLUF:** main at start and end; what "the page frame" covered (the measured list); the hook reuse; the no-flash proof; the beyond-the-frame count.
- **FOUND** (item 1 measurement; the item 3 table; the PDF measurement).
- **TESTED** (red-first log for every new test; each mutant red, then restored EQUAL; suites as item 7; the journey span comparison).
- **HOW** (commits, each with its files; every existing test you changed).
- **NOT TESTED** (honestly; anything UNMEASURED says what would close it).
- **PRIOR WORK** (file:line).
- **NEW WORDS** (string · where `file:line` at your final tip · why · status; reused B207 words marked "reused").
- **Records** (containers, worktree, ports free at the end by `lsof`).
- Last line: `READY FOR GATE — b208/customer-frame-alias @ <sha>` (sha from `ls-remote` after your last push), or `STOPPED: NEEDS FRIDAY` + one question.

## UNMEASURED at draft time (and what closes each)
- Whether main moves during the round: closed by your start and end `ls-remote` (rule under PINS).
- Whether the executive report PDF's pages name the customer to Demo: closed by item 1 (generate one in the mock or showcase; read its text).
- Whether the shell's extra summary call moves any timed-journey span: closed by item 2's `E2E_TIMED=only` comparison base vs head.
- Whether any existing shell or screen test asserts the name in the frame for a Demo session: closed by your red-first run (list each in HOW).
- Ports 6770–6779 free at your start: closed by your `lsof` re-check.
