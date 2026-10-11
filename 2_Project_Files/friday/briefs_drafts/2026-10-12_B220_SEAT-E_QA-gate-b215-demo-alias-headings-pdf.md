From Friday (laptop seat), Datasec / HPSM-POC. Replies go to friday-laptop-agent@agentmail.to.

# BRIEF B220 (SEAT E): QA GATE (tier 1, round 1 of 2) on TWO file-disjoint subjects. **Subject 1:** `b215/demo-alias-headings-and-pdf`, where a Demo login sees the alias, never the customer's name, in the customer page HEADINGS (eyebrow, overview h1, report preview) and in the executive report PDF (pages, document Title, file name), and partners without Demo keep names. **Subject 2:** `b219/demo-reset-upstream-timeout`, where the BFF waits 90 s for `POST /api/v1/admin/demo/reset` and only for that call.
**From:** Friday, @NOW@ 2026-10-12. This is a DRAFT by Friday's drafter: pins were read 13:14:37Z to 13:17:52Z and Friday re-pins at launch.
**Seat:** Datasec/HPSM-POC-E, pane Datasec/HPSM-POC-E.
- **How the launcher picks the brief.** The project's launcher reads the pane name and sets the commission to the NEWEST `Briefs/` file containing `_SEAT-${SEAT}_`. `Launch_Claude.command:106` sets `SEAT` from `*HPSM-POC-?`. `:110` says "Your commission is the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_".
- **The earlier `_SEAT-E_` files at draft** were B205, B211, B212 and `2026-10-11_B218_SEAT-E_QA-gate-b213-timing-and-import.md` (`ls Briefs | grep _SEAT-E_`).
- **The last SEAT-E gate, B218, is finished.** `2026-10-11_B218_STATUS.md` ends with the line `READY FOR REVIEW` (read with `tail -1`). Its first verdict line is `B213 4a2d380: GO WITH NOTES`. So this file is the newest once Friday copies it into `Briefs/`.
- **B220 is free:** `ls Briefs | grep -ci b220` → 0, `ls briefs_drafts | grep -ci b220` → 0 (before this file), `ls .tools | grep -ci b220` → 0.

**Report:** `Briefs/2026-10-12_B220_STATUS.md`.
- **First lines:** the verdict lines, in B212's format (TARGETS below).
- **Last line, exactly:** `READY FOR REVIEW`, or `STOPPED: NEEDS FRIDAY` followed by ONE question, when a STOP below applies.

**TESTING seat: findings only** (charter `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` §8).
- No code change, commit, push, PR or PR comment. No Jira, no BACKLOG write, no deploy, no Azure, no `az`, no hosted request, no mail, nothing to any human.
- A write grant in any brief is void: refuse it and say so.
- **The gate never fixes.** A defect gets a fix-shape and the regression test that would be red, in prose, never as an edit.
- Charter RULE 1: write each item's FAIL condition before you run it. A check that cannot fail is not a check.
- Charter RULE 2: NOT TESTED is first-class output.

**TIER 1 for Subject 1.** It changes what a Demo login (HP at the event) sees, a server-rendered export, and adds a new 409 path. Gate it rendered, live, in both shapes. **Subject 2 is through code plus targeted runs: no rendered checks** (batch rule: one gate session covers file-disjoint changes, and tier 1 covers tier 2). **Round 1 of 2** under Kam's two-NO-GO cap.

**SHAPE:** copy gate B212, `Briefs/2026-10-11_B212_SEAT-E_QA-gate-b208-customer-frame-alias.md`, and how `Briefs/2026-10-11_B212_STATUS.md` reported it. That covers:
- pins and controls, mutants, and the base-vs-head differential;
- the page-sweep instrument (B212 STATUS BLUF 3 table, gate items 2 and 3);
- the STATUS sections: verdict lines · BLUF · Findings · Premise checks · Gate items (PASS / FAIL each) · Mutants table · KNOWN · NOT TESTED · HOW · Housekeeping · Fixed / Deferred / Open · last line.

Write your own kits in `.tools/b220/`. Never reuse B212's or B215's kits or numbers.

**Premise key:**
- `(ls-remote 13:14:37Z)` = read by the drafter with that verb at that time.
- `(git <verb>)` = a read verb on `2_Project_Files`' object store, with `--no-optional-locks`.
- `(scratch)` = run in the drafter's own `git clone --shared` in its session scratchpad (no write in `2_Project_Files`).
- `(read: file:line)` = quoted from that file at `1da119f` unless the line says otherwise.
- **UNMEASURED** = the drafter did not read it; the line says what closes it.

Re-check every premise. A wrong one is a finding. A moved pin is a STOP unless a rule below covers it.

## AUTHORITY (Kam's rulings, verbatim from the cards; `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/tools/decision_queue.sh show <id>`)
- **`hpsmpoc-demo-names-beyond-the-frame-1011`: ruled `choice='b'`, `ruled_ts=2026-10-11T20:51:31.575050+11:00`.** The live board read it at 20:50:28, view=friday, as B215 brief :7 records. The two times are the board click and the card's stored stamp, and both refer to one ruling.
  - **bluf:** *"The page-frame alias you approved is built and goes to its test now: the breadcrumb and journey rail show ORG-nnnnn to Demo on all 15 customer pages (measured: 0 of 240 page loads name the customer there). But the builder measured 11 other places that still name the customer to Demo. The most visible is the heading line directly under the breadcrumb, on 13 of the 14 other customer pages, plus the overview page's title. So a Demo user reads the alias and, an inch below, the name. The executive report PDF names the customer on all 17 pages and in its file name. All showcase names are synthetic and labelled sample."*
  - **(a):** *"One more small build plus a test round: the heading and overview title show ORG-nnnnn to Demo; partners keep names."*
  - **(b), RULED:** *"Alias the headings AND the executive PDF for Demo (recommended)"*. Detail: *"As (a), plus the PDF a Demo user downloads names the customer only by alias, in its pages and its file name. The PDF is the clearest case of data leaving the partner; it is a bigger round."*
- **The earlier frame ruling, `hpsmpoc-page-frame-names-for-demo-1011`: ruled `choice='b'`, `ruled_ts=2026-10-11T16:31:01.710494+11:00`:** *"Alias the page frame for Demo logins before Tuesday (recommended)"*. Detail: *"One small build plus a test round, a few hours. The breadcrumb and rail show ORG-nnnnn to Demo; partners still see their own names."* The gate must find B208's frame still intact at the head.
- **Standing:** `hpsmpoc-customer-names-alias-1011` → (a) *"Keep names; alias wherever data leaves the partner"*: *"ORG-nnnnn on anything HP or an export sees."* (read: B215 brief :12).
  - **The Demo rule (B208's):** a caller who holds Demo (Demo, Partner+Demo or Admin+Demo) gets the alias. A caller without Demo (Partner, Admin or Consultant) gets the name.
- **Friday's technical ruling on the PDF shape:** `Briefs/2026-10-11_B215_SEAT-A_ADDENDUM-1_q-b215-1-pdf-shape.md`, Q-B215-1 → **(a) "render on demand, then verify"**:
  1. Serve the Demo copy only when its extracted text equals the stored PDF's extracted text with every occurrence of the name replaced by the alias (whitespace-normalised). Otherwise answer Demo with a 409.
  2. The 409 never names the customer.
  3. A non-Demo caller gets the stored bytes, byte-identical.
  4. The file name carries the alias.
  5. The post-deploy re-issue step is recorded for the deploy seat.
- **The oracle for Subject 1 is the IN/OUT table** of 11 elements in `Briefs/2026-10-11_B215_SEAT-A_demo-alias-headings-and-pdf.md` :14-32.
  - **IN:** 1 (eyebrow, 13 pages), 2a (overview h1), 3 (report preview h2 and "Organisation" row), 11 (executive PDF: pages and file name), and 8 *inside the PDF only* (the summary opening).
  - **OUT, must equal base:** 2b, 4, 5, 6, 7, 8 on screen, 9 and 10.
- **The oracle for Subject 2** is Friday's ruling in ADDENDUM-1 to B217, as `Briefs/2026-10-11_B219_SEAT-B_demo-reset-upstream-timeout.md` relays it: only the hosted reset changes; the laptop showcase's reset keeps 30 s. Re-read it there.

## TARGETS (re-read with `git ls-remote origin` in `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/2_Project_Files` at the start, mid-gate and before the verdict; name the instrument and time on each)
| What | Value | Instrument |
|---|---|---|
| **Subject 1 head:** `b215/demo-alias-headings-and-pdf` | `1da119f6bafcdfad460f739875593f05246b1ecb`, tree `85a4fad9ba1966a53276555f0083b099a721b919` | ls-remote 13:14:37Z and 13:17:52Z (= B215 STATUS last line); git rev-parse `^{tree}` |
| **Subject 1 base** (= B215's base) | `4229be358760b9e2af9ed6ccc68a60332d9b97ec`, tree `a815337cb36dc429b664243fe4c7f00e0c657127` | git rev-parse; `merge-base 4229be3 1da119f` = `4229be3` |
| Subject 1 commits (6, linear) | `0799920` the PDF · `73e905e` the headings · `f62a387` tests · `99c1a64` the name check's word characters · `bb0cfed`, `1da119f` tests | git log --format='%H %P %s' `4229be3..1da119f` |
| **Subject 2 head:** `b219/demo-reset-upstream-timeout` | `98158dfd77fa11301dab64d9a4cd9077f4d79d5b`, 1 commit, parent `4229be3` | ls-remote 13:14:37Z and 13:17:52Z (= B219 STATUS last line); git log |
| **main** | `da58da962837fe947a32421edc2b3c5258ab0da9` (B213, PR #140; parent `4229be3`), tree `9e77e5ff9e6f60b2bd39f5bbc72daa35c14db2cf` | ls-remote 13:14:37Z and 13:17:52Z; git rev-parse. That tree equals B218's MERGE tree (B218 STATUS :3) |
| Objects present | `1da119f`, `98158df`, `4229be3`, `da58da9` → `commit` | git cat-file -t |
| PRs | none for `1da119f` or `98158df`. The highest is `refs/pull/140/head` = `4a2d380` (B213) | ls-remote `refs/pull/*/head` 13:14:37Z |
| `.tools/.git-lock` | absent (free) | `ls` |

**What main moved by (`4229be3` → `da58da9`, 13 files, git diff --name-only):**
- Ingest `ImportReader.cs` and `Assessment/README.md`;
- the API contract copy `openapi.yaml`, `PROVENANCE.md`, and `ImportFileStoredHashMigrationTests.cs`;
- `RequestTimingLogTests.cs`, `ImportStoredCopyTests.cs` and `NarrativePipelineTests.cs`;
- `web/contract/{SOURCES.md, design-pack/api/openapi.merged.json, design-pack/api/openapi.yaml}`, `web/src/api/contract-drift.test.ts` and `web/src/api/schema.gen.ts`.

**Disjointness, as the drafter measured it (prove it again yourself):**
- `comm -12` of main's 13 and B215's 22 → **0**.
- main's 13 and B219's 2 → **0**.
- B215's 22 and B219's 2 → **0**.
- B219 = `web/src/server/bff.ts` (+8/−1) and `web/src/server/bff.timing.test.ts` (+75/−2) (git diff --numstat `4229be3 98158df`).

**The drafter's merge trees (scratch; re-derive each in YOUR scratch clone against main as it is at verdict time):**
- `merge-tree --write-tree da58da9 1da119f` → `32ba7393ba127252997e8ab0622a038827d9ba73`, rc 0. This equals B215's reported `32ba7393…` (B215 STATUS :23).
- `merge-tree --write-tree da58da9 98158df` → `30321f49e0d63586eceaccc5e4fcd051c3b0fadf`, rc 0.
- **B215 + B219 together:** first make a probe commit of tree `32ba7393…` on parent `da58da9` with `commit-tree`, in scratch. Its sha depends on the time, so it is not a pin. Then `merge-tree --write-tree <probe> 98158df` → `bf26f63bb191233d09766941b9148d3797837869`, rc 0.

**Rules:**
- **A head moved** → STOP, and say to what.
- **Main moved again** → read `git diff --name-only da58da9 <new>`. If any path overlaps either subject's files, or falls under `web/src/components/{shell,customer,screens}/**`, `web/src/server/**`, `api/src/HpsmPoc.Modules.Assessment/Endpoints/ReportingEndpoints.cs` or `api/src/HpsmPoc.Modules.Reporting/Report/**`: STOP and say which. Otherwise re-derive the three trees against the new main.
- **A conflict** → STOP, and say where.
- **Build and test the THREE-WAY merged tree (`bf26f63…` or its re-derivation) once** in `.tools/wt-B220-merged`: vitest full, typecheck, lint, build, `contract-drift`, `bff.timing.test.ts`, `customer-headings-alias.spec.ts` + `customer-frame-alias.spec.ts`, and the API suite once if time allows (else UNMEASURED, said).
  - **Why `contract-drift` matters here:** main's B213 changed the contract copies and `schema.gen.ts`, and B215 changes an API response (a 409 on `downloadReport`) without touching the contract. B215 PROPOSED the contract text (STATUS :241).

**Verdict lines (the first lines of STATUS):**
```
B215 1da119f: GO | GO WITH NOTES | NO GO
B219 98158df: GO | GO WITH NOTES | NO GO
MERGE <main>+1da119f: GO | GO WITH NOTES | NO GO | STOP   (tree, rc)
MERGE <main>+98158df: GO | GO WITH NOTES | NO GO | STOP   (tree, rc)
MERGE <main>+1da119f+98158df: GO | GO WITH NOTES | NO GO | STOP   (tree, rc; disjoint files proved)
Round 1 of 2.
```

## GIT DISCIPLINE
- **In `2_Project_Files` itself, READ verbs only:** `ls-remote`, `log`, `show`, `diff`, `cat-file`, `ls-tree`, `rev-parse`, `rev-list`, `merge-base`, `grep`, and `git --no-optional-locks status`, always with `--no-optional-locks`. No fetch, checkout, switch, branch, merge-tree, commit-tree, worktree add/prune or gc there.
- **Everything else goes in a `git clone --shared`** or an alternates bare repo under `.tools/b220/`: merge-tree, the probe commit, any fetch of a moved main.
- **Your detached trees** are made under a copy of `.tools/b218/lock.sh` → `.tools/b220/lock.sh` (the sha256 of the copy equals the original's), on the shared `.tools/.git-lock`. Never remove another seat's lock.
  - `.tools/wt-B220-head` (`1da119f`)
  - `.tools/wt-B220-base` (`4229be3`)
  - `.tools/wt-B220-mut` (`1da119f`, mutants)
  - `.tools/wt-B220-b219` (`98158df`; its base is `wt-B220-base`)
  - `.tools/wt-B220-merged` (the three-way tree)
  - `.tools/wt-B220-prekey`, only if you seed pre-key data with an API from before the keys (B212 used `76acd69`).
- **Do not use or touch** `.tools/wt-b215*` or `.tools/b215/` (read the builder's evidence in `Briefs/2026-10-11_B215_evidence/` only, and re-derive every number), `.tools/wt-B219`, `.tools/b219/`, `.tools/wt-B212-*`, `.tools/b212/`, `.tools/b218/` (beyond copying `lock.sh`), or any other seat's tree, kit or container.
- Every SHA you write is one you read, with its instrument inline.

## PARTITION / PORTS: 6950–6959, yours only
- **Seat B / B219:** the brief that drafted this gate called B219 a live seat. **That no longer holds.** B219's builder pane is closed (Friday, 2026-10-12), and its STATUS ends `READY FOR GATE: b219/demo-reset-upstream-timeout 98158dfd…`. B219 is now this gate's Subject 2, so it has no live writer. Its builder's ports, 6930–6939, are still not yours.
- **Live elsewhere:** the hosted lane (no hosted request from this seat). Never start, stop, reuse or remove any `b2xx-*` or `pc-*` container other than your new `b220-*` one.
- **The drafter's port check, 13:1xZ:**
  - `lsof -nP -iTCP -sTCP:LISTEN` in 6000–7999 → 6540, 7000 and 7768 only.
  - `lsof -nP -iTCP:6940-6959` → 0 lines.
  - `docker ps -a` port bindings: only `pc-b128-pg` 127.0.0.1:6540; none in 6900–6999.
  - `grep -ohE '\b69[4-9][0-9]\b'` over every HPSM-POC `Briefs/*.md` and Friday's `briefs_drafts/*.md` → 6941 (B214's SQL Server), 6998 and 6999 only. **0 in 6950–6959.**
- **Never yours:** 6860–6939 (B212, B213, B216, B215's 6890–6899, 6900–6919, B218's 6920–6929, B219's 6930–6939), 6941, 6540–6549, 6730–6739, 6750–6799.
- **Plan:**

  | Port | Use |
  |---|---|
  | 6950 | head web, mock build (offline demo) |
  | 6951 | base web, mock build |
  | 6952 | head web, proxy mode (showcase shape) → 6954 |
  | 6953 | base web, proxy mode → 6955 |
  | 6954 | API at `1da119f`, Development sign-in, one role set per arm, restarted per arm (B204 R2 / B212 method), `Showcase__Enabled=true` as `scripts/showcase.sh` sets it (B215 FOUND 1) |
  | 6955 | API at `4229be3`, the same (B215 changes the API, so the base arm needs the base API) |
  | 6956 / 6957 | hosted standalone + Entra stub (`E2E_HOSTED_PORT` / `E2E_STUB_PORT`) |
  | 6958 | Azurite `b220-azurite`: new, CI digest `mcr.microsoft.com/azure-storage/azurite:3.37.0@sha256:830430c1…` (read: `.github/workflows/ci.yml:43` at `1da119f`); key in `4_Credentials/b220-azurite.env`, mode 600, read by name only; stopped, not removed, at the end |
  | 6959 | mutant web, then the merged-tree web (one at a time) |

- **Re-check with `lsof` before every bind**, and log the checks in `.tools/b220/run/lsof-checks.txt` and in STATUS.

## BUILDER'S CLAIMS (read whole first; trust no count in them)
- **Subject 1.** Brief `Briefs/2026-10-11_B215_SEAT-A_demo-alias-headings-and-pdf.md`, which has the SCOPE table, THE WORK 1–7 and the partition. Its ADDENDUM-1. STATUS `Briefs/2026-10-11_B215_STATUS.md`: BLUF 1–7, FOUND 1–7, TESTED, the 16 mutants, HOW, NOT TESTED, NEW WORDS, NEW LOOK. Evidence `Briefs/2026-10-11_B215_evidence/`: `sweep/`, `flash/`, `mutants/`, `shots/`, `logs/`, `fidelity-measure.txt`, `partition.txt`, `merge-tree.txt`, `setup.txt`.
- **Subject 2.** Brief `Briefs/2026-10-11_B219_SEAT-B_demo-reset-upstream-timeout.md` and STATUS `Briefs/2026-10-11_B219_STATUS.md`: the limits table "Every limit on the path", red-first, and the mutant. Evidence `Briefs/2026-10-11_B219_evidence/`.

## SUBJECT 1: THE GATE MUST, INDEPENDENTLY, AT `1da119f`

### 1. Through code: the diff against the brief, plus the partition
Read `4229be3..1da119f` (22 files, +971/−45; git diff --stat) item by item against B215 THE WORK 2–3, with `file:line` at `1da119f`. The drafter's anchors:
- **`api/src/HpsmPoc.Modules.Assessment/Endpoints/ReportingEndpoints.cs`:**
  - `DownloadReport` `:383-421`. The gate, the withheld 403 and the stored sha check come first, `:390-410`. The Demo branch is `:413` `if (CallerAccess.Get(http).Is(Roles.Demo))`.
  - `NoAliasWords` `:424` and `ChangedSinceIssueCode` `:427`.
  - `DemoRenditionAsync` `:441-486`:
    - **gate 1**, `:462`: `Sha256Hex(Draw(customer.Name)) != row.Sha256`;
    - **gate 2**, `:463`: `DemoCopyNamesCustomer(pdf = Draw(shown), customer.Name)`;
    - the 409 `:475-477`; audit `:473`, `:481-482`; the usage event only on a 200, `:480`; the copy's own `Digest` `:484`; the file name `:485`.
  - `DemoCopyNamesCustomer` `:491-500`.
  - `InlinePdf` `:557-561`, `Slug` `:564`.
- **Web:**
  - `web/src/components/customer/CustomerHeading.tsx`: the context `:16-18`, `useCustomerEyebrow` `:25-31`, `useCustomerHeading` `:34-36`.
  - `CustomerShell.tsx`: `shownAsState` and `CustomerShownAsProvider`.
  - `useCustomerShownAs.ts`: the `who` guard (+7/−4). **This file is outside B215's named paths** (B215 HOW :173). It is the N-2 fix.
  - The 12 screens and components that take the eyebrow; `EngagementOverview.tsx` h1 = `heading`; `ReportScreen.tsx` passes `shownAs` only from `PrototypeReport`.
- **Confirm:**
  - `CustomerProvider`'s value still carries the real name, so the OUT rows are unchanged.
  - **No new role source, setting, env name or flag.** Look for 0 added `process.env` / `NEXT_PUBLIC` / config lines in the diff.
  - No screen calls `useCustomerShownAs` itself (`git grep -n useCustomerShownAs 1da119f -- web/src`). The only callers should be the shell and `MetricsScreen.tsx`.
  - `MetricsScreen.tsx` and `MetricsScreen.alias.test.tsx` are unchanged (`git diff --quiet 4229be3 1da119f -- <both>`).
  - `Caller.cs`, `Program.cs`, `**/Migrations/**`, `web/contract/**`, `web/src/api/schema.gen.ts`, `ApiMode.tsx` and `bff.ts` are unchanged (0 in the name list).
  - `api/src/HpsmPoc.Modules.Reporting/Report/**` is unchanged (B215 HOW :168).
- **Partition:** compare `git diff --name-only 4229be3 1da119f` (22) with B215's "Yours" list (brief :87) and its NOT-yours lists (:88). Expect 0 in the NOT-yours lists. The one path beyond the named ones is `useCustomerShownAs.ts`: judge whether it was needed. The measure is item 7's mutant: the N-2 test red without the guard.

### 2. The page sweep: every route, 1440 and 390, mock and showcase, Demo-holding arms against no-Demo arms (B212 items 2 and 3, extended to `#main`)
- **Routes:** every `page.tsx` under `web/src/app/(app)/customers/[customerId]/` (git ls-tree; B212 counted 16, with `tasks/page.tsx` a redirect, so 15 routes plus `/tasks`), plus `/customers` and `/workspace` (row 9). Every listed customer: the prototype ids and the API-only mock customers.
- **Shapes and arms:**
  - **Offline demo** (6950 head / 6951 base; the session role decides, B209): Demo, Partner, Admin and Consultant sign-ins.
  - **Showcase / proxy** (6952 → 6954 head, 6953 → 6955 base): one arm per SERVICE role set through the Development sign-in. The arms are Demo · Partner+Demo (the showcase default) · Admin+Demo · Partner · Admin · Consultant, plus **pre-key data** (a customer with no `CustomerKeys` row, made as B212 made it). Read `getMe` per arm and record what the SERVICE gave.
- **Instrument:** your own rendered-lines probe, **case-insensitive** (B208 FOUND 7: `innerText` applies `text-transform`).
  - It reads `#main` per element: the eyebrow, the h1, the report preview h2 and "Organisation" row, and each OUT row's own locator. It also reads everything outside `#main` (B208's frame), and `document.title`.
  - **A `MutationObserver` installed by `addInitScript` before navigation** records EVERY text an IN element or the title ever held, from navigation start to settle.
  - Match against EVERY customer name in that build's data, not only the page's own.
- **Base control (the instrument is not blind):** the same probe at base must FIND the name in every IN element for Demo. If base finds none for an element, that element's row is UNMEASURED: STOP that row, say so, and do not record it as a pass.
- **FAIL conditions (write them before the runs):**
  - any Demo-holding page load whose IN element, title or frame holds a customer name, at any moment;
  - any OUT row whose count differs from base for any arm;
  - any no-Demo arm where an IN element differs from base;
  - B208's frame naming the customer to Demo.
- **Report per SCOPE row** in a table like B215 BLUF 2's: Demo-holding loads naming base → head; no-Demo loads (= base); and the distinct label strings Demo read.
- **Row 3:** reach the report preview's issued view for Demo yourself. B215 did it by putting the journey's issued state in the session (FOUND 3). Say how you reached it, and whether that is a state a real Demo user can reach. Then measure the h2 and the "Organisation" row (B215 says that row shows only without a description list: confirm in code).
- **No flash, no stale (B212 item 3's holds, re-made):**
  - `getMe` and the summary, each held 3 s then answered, held then 500, 500, and aborted, on the overview, `/profile`, `/report` and `/documents`, in both shapes.
  - A customer switch by the firmware picker and by `router.push`, with the next answer held.
  - In the mock, Partner → sign out → Demo, then return to the same customer.
  - **FAIL:** a name, or a previous customer's alias, in any IN element at any moment.
- **The industry beside the alias in the overview header** (B215 FOUND 4: "Government · 450 staff · Customer since 2026") and **row 2b under the aliased h1:** record both, KNOWN for Kam, not graded.

### 3. The executive PDF, for each caller (row 11; the product's own synthetic report only, never an HP document)
- **Data:** the showcase's seeded report, plus one report you issue yourself through the API under a Partner caller (`POST /assessments/{id}/reports`).
- **Download as:** Demo-only (`X-Dev-User b220-demo`), Partner+Demo, Admin+Demo, Partner, Admin and Consultant, against the head API (6954) and the base API (6955).
- **Read for each:** status, `Content-Disposition` (both `filename` and any `filename*`), `Digest`, and sha256 against the report row. Then:
  - with `pdftotext` (or PdfPig): pages naming the customer, occurrences, `ORG-` count;
  - with `pdfinfo` **and a raw metadata dump**: the Info dictionary's Title, Author, Subject, Keywords, Creator and Producer, any XMP packet, outlines and bookmarks, annotations, and embedded file names. Gate 2 only checks words and Title (`:498-499`); every other place a name could sit is yours to read.
- **Expect, Demo-holding:** 200; 0 pages and 0 metadata fields naming the customer; the alias on the cover, the running header, the summary opening (when an approved summary exists) and the "Organisation" row; Title with the alias; file name `executive-report-org-nnnnn-<GeneratedAt date>.pdf`; `Digest` = the copy's own sha256, which is ≠ the row's; the printed date = `GeneratedAt`, not today.
- **Expect, no Demo:** the stored bytes, **sha256 = the row's**, today's file name and `Digest`, exactly as base.
- **Base control:** the base API serves the stored, named PDF to Demo, and your extractor finds the name there. If it finds none, the extractor is blind: STOP the item.
- **Fidelity, by YOUR instrument:** stored text with every occurrence of the name replaced by the alias, blanks collapsed, compared with the Demo copy's text. They must be equal. Report page counts too.
- **Judge B215's deviation from Friday's text check.** B215 gates on BYTES with the name (gate 1), not on the text comparison ADDENDUM-1 item 1 named (B215 BLUF 3, :63-64). It argues that bytes are stricter and imply the text check, and that a text replacement would refuse faithful copies (the header ellipsis, swapped glyphs).
  - Say whether the claim holds.
  - Say whether gate 1 + gate 2 together refuse every case the text check would refuse.
  - Say whether any case passes gate 1 + gate 2 yet serves a copy that differs from "stored with name → alias" in some way other than the name. For example: a long name whose truncated prefix stays in the header, or a glyph-swapped name that the regex cannot match.
  - This is a finding only if you can make such a case. Otherwise it is a Note for Friday, who ruled the text check.
- **Timing:** time the Demo copy cold and warm (B215: 1,171 ms / 619 ms).
  - The BFF's limit for `GET /reports/{id}/content` is **30 s**, not the 10 s B215's brief cited. B180 moved the downloads to the named 30 s (read: `web/src/server/bff.ts` `DOWNLOAD_READS` and `upstreamTimeoutMs`, `:166-182` at `98158df`; `bff.timing.test.ts:47-54` at `1da119f`). Re-read it.
  - The Demo copy draws the PDF **twice** (gate 1 and the copy). B217 measured the hosted sample PDF at 12.6 s (relayed: `bff.ts` B219 comment at `98158df`).
  - Estimate the hosted Demo download as about 2 × the hosted draw time, against 30 s, and say whether a cold hosted Demo download can be cut. That is UNMEASURED on hosted (no hosted request); state the estimate and how it was made.

### 4. The verify gate: it can fail, and it fails closed
- **Plant post-issue changes, each on a freshly issued report:** an override, a profile edit and a customer rename (B215's three). Add at least one B215 did not plant: a narrative approved after issue, or a ruleset or content change if one is reachable through the API.
- **Expect for Demo:** 409 with `report.changed-since-issue`, and a body naming neither the customer nor the alias (check the title, detail, field error and every header). No `report.downloaded` usage event is written. One `report.demo-rendition` "refused: …" audit row is written: read the audit and usage tables before and after.
- **Expect for no-Demo callers:** still the stored bytes.
- **After issuing a NEW report** following the change, Demo gets 200 by alias.
- **Can the comparison not fail?** Read and test:
  - **(a)** `DemoCopyNamesCustomer` returns `false` when the collapsed name is empty (`:494`). Can a customer name be empty or blank at this point? `WithCurrentName` throws on whitespace (`CustomerNameAtRender.cs` `ThrowIfNullOrWhiteSpace`) and the catch at `:465` turns that into a refusal. Try a name of only punctuation or only blanks through `createCustomer` / the profile, then download as Demo.
  - **(b)** Gate 1 is not trivially true: show one case where `Draw(customer.Name)` ≠ stored, which is your planted changes.
  - **(c)** Gate 1 is not trivially false: a renderer that is not deterministic (a PDF `/ID`, a creation date, font subset tags) would refuse every Demo download. Show that two draws of the same input are byte-equal.
  - **(d)** Gate 2's regex and word join: a name containing regex characters, a hyphenated name, a name with a double blank, a non-ASCII name, a name that is a word inside other text ("Org", B215 `99c1a64`), and a name split across lines by the renderer.
- **Mutants:** remove gate 1; remove gate 2; make gate 2 always `false`; make the 409 body carry the name; write the usage event before the gate. Each must turn the gate's own tests red (`B215DemoAliasPdfTests.cs`). A SURVIVOR is a finding with a fix-shape and the test that would be red.

### 5. Demo is decided on the SERVER, by role
- **Code:** the only Demo decision in the PDF path is `CallerAccess.Get(http).Is(Roles.Demo)` (`:413`). In the web, the decision is the hook's `holdsDemo` from `getMe` / the session role.
- **Try to obtain the real name AS DEMO, for each route or header the builder did not list.** Record each attempt with its FAIL condition.
  - The API JSON bodies: `listReports` (`AssessmentModule.cs:250`), `getAssessment`, `listNarratives`, `getHpRecommendations`, `getAssessmentMetrics`, `getMetricsSummary`, `getMe`, the audit and usage reads if Demo can reach them, any problem+json body.
  - `getCustomer` (row 10, OUT): it names the customer. That is KNOWN: confirm it is byte-identical to base.
  - The file-name headers (`Content-Disposition` `filename*`, through the BFF's `FORWARD_RESPONSE`, `bff.ts:139`).
  - PDF metadata (item 3).
  - The readiness PDF (`getReadinessReport`; KNOWN, B215 FOUND 5: try it on a named customer as Demo, and record it, not graded).
  - Cached responses: `Cache-Control: no-store` on every API response (`Program.cs:119-124`) and on the BFF (`bff.ts:303`). In ONE browser context, Partner (no Demo) downloads the PDF, then the role changes to Demo (mock sign-out/sign-in; showcase arm restart), and the same URL is opened again, including by back/forward. Expect the alias copy, never the cached named bytes.
- **Client claims must change nothing:** a query string, cookies, `X-Dev-Roles: Demo` sent through the BFF in proxy mode, and `X-Dev-Roles` against the **hosted** project (Entra stub, 6956/6957), where the Development sign-in must be off. Read where `DevelopmentAuthentication` is registered (`api/src/HpsmPoc.Api/Auth/DevelopmentAuthentication.cs:23-24`, `Program.cs`) and confirm it is not registered outside Development.
- **Grading:**
  - **A route that serves the NAMED executive PDF or its name-bearing file name to a Demo-holding caller is a Blocker.**
  - Any other unlisted place that names the customer to Demo is a finding (Minor or Note), reported for Friday to put to Kam under the standing ruling ("anything HP or an export sees"). It is not graded against the B215 table.

### 6. Words for customers without an alias, and every NEW WORD for Kam
- **Pre-key** (no `CustomerKeys` row), Demo:
  - The web: eyebrow, h1 and report preview read "No alias (made before the keys)" (`attribution-preview.ts:72`).
  - The PDF: cover, header, Title, summary opening, "Organisation" row and file name read `NoAliasWords` (`ReportingEndpoints.cs:424`), with file name `executive-report-no-alias-made-before-the-keys-<date>.pdf`.
  - **FAIL:** any fallback to the name.
- **No scored run:** "Alias not available yet (no scored run)" in each IN element.
- **NEW WORDS completeness** (for Kam; B215 STATUS :198-207).
  - `git grep` every string literal added in `4229be3..1da119f` (web and API) and compare the list with B215's NEW WORDS table. Any user-visible string missing from it is a finding (Note).
  - Quote verbatim: the 409 title (`:475`), the detail (`:476`), and the field error with its code (`:477`, `:427`); the pre-key PDF words; the "Customer" word now used in the h1 and the report preview.
  - Say where each is seen by a person. For example, does the 409 detail reach the screen, and in what words does the report page show a 409 to Demo?
  - Screenshot the report page as Demo when the download answers 409.

### 7. B212 N-2 (the hook was touched: `useCustomerShownAs.ts` +7/−4)
- **Re-make B212's mutant (h)** (drop `customerId` from the hook key) and **remove the `who` guard** (return `state.data.shownAs` whenever `ready`). Each must turn the N-2 same-instance re-render test red (`CustomerHeading.alias.test.tsx`).
- **Confirm the guard does not add a flicker** between one customer's own steps: navigate overview → profile → results with the MutationObserver on. "Customer" should never flash in the crumb when the same customer and role are kept.
- **Confirm the metrics page's key string is byte-identical** to base for `refresh === undefined` (B212 item 4 method), and that `MetricsScreen.alias.test.tsx` passes 16/16, unchanged.
- **N-1:** the title assertion exists in `customer-frame-alias.spec.ts` (+1 line). Re-make B212's mutant (e) (`document.title = customer.name`): red.

### 8. The post-deploy step (B215 BLUF 6): necessary and sufficient?
B215 wrote *"after the 2nd hosted deploy, issue a new report on the seeded customer, then open it as Demo"*. Through code and the laptop showcase only (no hosted request):
- **Necessary?** Does the hosted demo reset (`resetDemoData`; B219: the reset itself draws "the sample PDF") already issue a new seeded report on the deployed build? If so, is "reset the demo after deploy" sufficient on its own?
- **The draw mode.** Seeder `approverRoleOnly` (`ShowcaseSeeder.cs:272`, `ScoredAsync` `:84`; B215 FOUND 1). Is the hosted seed drawn in the same mode as the hosted Demo copy? Reproduce on the laptop, in one mode: seed (issue) → restart the API → download as Demo → 200. Then the mode switch → 409.
- **Sufficient?** Does any per-host or per-machine input to the renderer (fonts, culture, time zone `ReportTimeZone`, the build) differ between the instance that issued and one that redraws? Consider App Service scale-out, and a slot swap after issue. Name each input the renderer reads that is not stored with the report.
- **Expected answer shape:** "necessary: yes/no because …; sufficient: yes/no, missing …". Give the step in words a deploy seat can follow.

### 9. NEW LOOK (your own screenshots, before = base, after = head)
- **Pages:** overview (h1, plus the 2b row under it), `/profile` (eyebrow; B215 FOUND 2's `ApiSteps` row), `/report` (eyebrow, plus the preview h2 and row), `/documents`.
- **Callers:** Demo and Partner, at 1440 and 390, in the offline demo AND the showcase. Caption each with the caller as the SERVICE saw it (a showcase Partner sign-in is Partner+Demo, B208 FOUND 2).
- **The PDF:** the Demo copy's cover and one inner page beside the stored PDF's, as PNGs, captioned with both file names. Also the Demo 409 on the report page.
- Put summaries and PNGs in evidence; raw data stays in `.tools/b220/`.

### 10. Suites and the gate's own mutants
- **Head:**
  - vitest full (`--maxWorkers=4`; B215: 1,640 / 1,640, 171 files), typecheck, lint, build (B215: the 8 Edge-runtime warnings, line-identical to base: compare).
  - Playwright desktop + tablet: customer-headings-alias, customer-frame-alias, metrics-dashboard, attribution-preview, a11y, responsive, nav-dead-ends (B215: 48 / 48).
  - The timed journey (`E2E_TIMED=only`, desktop + tablet). **The console-error assertion is graded:** `journey.spec.ts` "no console errors (incl. CSP violations)". A timing-budget miss under load is recorded and re-run once alone.
  - The hosted project, standalone + Entra stub (B215: 6 / 6).
  - The full API suite once on SQLite with `b220-azurite` (all 5 projects, 0 skipped; B215: 2,627).
  - gitleaks `--log-opts=4229be3..1da119f`.
  - A raw scan of the added lines **with Python**, not BSD grep (B205 N-4). B215 found U+00B7 ×18, U+2014 ×6, U+2013 ×3, U+2026 ×2, U+203A ×1, and 0 invisible: re-derive.
- **Console errors and 4xx/5xx per page, base vs head:** a new one at head is a finding. B208 FOUND 5's profile 404s and unscored 409s are KNOWN if base = head. **The Demo 409 on `/content` IS new by design.** Confirm it never fires on the seeded report in the showcase mode, and say what the report page shows when it does.
- **Mutants:**
  - **Runner** as B212 (exact replacement, anchor count 1, restore by copy, blob sha256 EQUAL to the head blob AND `git diff --quiet` after each, a new mtime; control M00 green).
  - **Re-make at least 4 of B215's 16** (STATUS :134-151), including a2 (stored bytes served to Demo), a3 (the Demo check reads Partner), a4 (the Demo check reads a client header) and m1 (one eyebrow left on `CustomerName`, API branch). Give red counts against B215's.
  - **Plus your own, at least:**
    - one IN screen reading `useCustomer().name` instead of the context;
    - `heading` falling back to `customer.name` instead of "Customer";
    - the copy's file name using `Slug(customer.Name)` only when the alias is null (pre-key);
    - the Demo check placed after the integrity check fails (order);
    - item 4's mutants;
    - item 7's guard removal.
  - Any SURVIVOR is a finding with a fix-shape and the regression test that would be red.

## SUBJECT 2: B219 AT `98158df` (through code + targeted runs; no rendered checks)
- **S2-1. Only the one route's limit changes.**
  - Read `upstreamTimeoutMs` (`bff.ts:177-183` at `98158df`) and the constants `:141` 10 s, `:145` 75 s, `:151` 30 s, `:164-165` 90 s + `DEMO_RESET`, plus `NAMED_WRITES` `:152-158` and `DOWNLOAD_READS` `:171-175`.
  - With your own table-driven test in `.tools/b220/` (run against both trees, never committed), assert that `upstreamTimeoutMs` gives base = head for **a control per route class**: a GET read (10 s), each `DOWNLOAD_READS` GET (30 s), the narrative POST (75 s), each remaining `NAMED_WRITES` POST including `/api/v1/showcase/reset` (30 s, the laptop's), another POST (10 s), and PUT / DELETE (10 s).
  - **Only** `POST /api/v1/admin/demo/reset` differs: 30 s → 90 s.
  - **FAIL:** any other path or method differs.
- **S2-2. The regex cannot match anything else.** Feed `upstreamTimeoutMs` near-misses: `/api/v1/admin/demo/reset/`, `/api/v1/admin/demo/resets`, `/api/v1/admin/demo/reset/x`, `/api/v1/admin/demo`, `/API/V1/ADMIN/DEMO/RESET`, `//api/v1/admin/demo/reset`, `/api/v1/admin/demo/reset%2F`, `/api/v2/admin/demo/reset`, and a GET or lowercase `post` on the right path.
  - Then read what `src.pathname` is at the call site (`bff.ts:274`): is the query string already stripped, and is the path normalised before the test? Show it by a request through the BFF handler in a vitest (as `bff.timing.test.ts` drives it) with `?x=1`, a trailing slash and an encoded slash.
  - Expect 90 s only for the exact path, and say what the API does with each near-miss (404 or the same handler).
- **S2-3. Red at base, green at head.** Run `bff.timing.test.ts` from `98158df` against base `bff.ts`: B219 reports 3 failed / 36 passed, red. At head expect 39 / 39. Read the fake-clock cases to confirm they use a fake clock (no real 90 s wait) and that the "not before 89 999 ms" case can fail.
- **S2-4. A mutant reverting to 30 s is caught.** Try `DEMO_RESET_TIMEOUT_MS = 30_000`, the `DEMO_RESET` line deleted, and the reset back in `NAMED_WRITES` with the line deleted: each must be red. Try B219's own mutant (every named write at 90 s): red, B219 says 8.
- **S2-5. B219's limits table, re-checked at source** (B219 STATUS "Every limit on the path"). For each hop re-cite `file:line` at `98158df`:
  - `client.ts` with no signal;
  - `route.ts` with no `maxDuration`;
  - the Node `requestTimeout` / `headersTimeout` (a request-receive bound, not a response bound: confirm against Node's docs for the version `node --version` gives);
  - `bearerFor` before `forward()`;
  - undici's defaults;
  - `infra/**` with no Front Door or App Gateway (`git grep -i`);
  - the App Service 230 s (outside the repo: say so);
  - the API with no request timeout;
  - `ShowcaseSeedLock.cs:62` `ResetWait` = 15 s and `:225` CommandTimeout = wait + 30.
  - A limit B219 missed that is under 90 s is a finding.
- **S2-6. Is 90 s enough?**
  - The ingredients: B217's measured 34 s (34,090 ms then 499, relayed in B219 STATUS), the 15 s seed-lock wait (`ShowcaseSeedLock.cs:62`), the 45 s lock statement timeout (`:225`) and SqlClient's 30 s per-statement default, and the hosted cold token step (`entra.ts:35`, `:40`, before the upstream timer).
  - Give the worst plausible sum and its margin to 90 s. **Include B215's effect:** B215 changes no reset code, so the reset's seeded report is drawn exactly as before. Confirm by `git diff --quiet 4229be3 1da119f -- api/src/HpsmPoc.Modules.Assessment/Showcase`.
  - Record B219's NEW WORDS candidate ("It may still finish", false for the reset) as KNOWN for Kam, not graded.
- **S2-7. Suites at `98158df`** (targeted): `bff.timing.test.ts`, vitest full once, typecheck, lint, build, gitleaks `--log-opts=4229be3..98158df`, and a Python raw scan of the added lines.

## KNOWN (Kam's or Friday's to rule; confirm and record, do not grade)
- **B215 FOUND 4 (row 2b):** the overview h1 reads ORG-nnnnn and the "Customer details" panel directly below reads the name. The industry and lead sit beside the alias in the overview header.
- **B215 FOUND 2 (row 6):** `ApiSteps` "Customer" row on `/profile` names the customer to Demo (OUT, = base).
- **B215 FOUND 3:** the report preview reads "Alias not available yet (no scored run)" in the offline demo.
- **B215 FOUND 5:** the readiness PDF on a named customer.
- **B215 FOUND 1 / BLUF 6:** a change of approver mode after issue refuses old reports to Demo, and the post-deploy re-issue step (graded only as item 8 asks).
- **B215's PROPOSED contract text** for `downloadReport` (`openapi.yaml:1632-1640` not edited).
- **Rows 4, 5, 7, 8 (screen), 9, 10** name the customer to Demo by design (OUT).
- **B219's 504 sentence** "It may still finish" is false for the reset.
- **Known flakes, recorded not chased:** HPSMPOC-247 `ImportRobustnessTests.R2_2`; a vitest worker-start timeout under load (`customer-text.test.ts`, B215). Re-run each alone, never skip it.

## FINDINGS FORMAT
- Give each finding a severity (Blocker / Major / Minor / Note) with `file:line` at the subject's head, the instrument, the FAIL condition it met, a prose fix-shape, and the regression test that would be red.
- Severity yes, priority no (charter §8).
- One defect per finding (charter §9).

## HOLDS
- No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool without HP's written approval (signed SOW §4.1.4(c)). Every PDF here is the product's own synthetic report.
- Datasec only; no other client's names, tickets or paths.
- Findings only. Never delete: quarantine. Never print a secret.
- Kam's two-NO-GO cap: this is round 1 of 2.
- No deploy, no Azure, no setting change, no hosted request; nothing to HP or any human. No real customer export is used or requested.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY.
- No force-push, no branch delete, no history rewrite, no ref write in `2_Project_Files`.
- B215's (Seat A) and B219's (Seat B) worktrees, kits, ports and containers are never touched.
- *(Time-box)* about 3 h of gate time. Anything not reached is NOT TESTED with the reason, never a silent PASS.

## UNMEASURED at draft (each closes as stated)
- **Whether the Datasec/HPSM-POC-E pane is free to launch:** Friday, at launch.
- **Whether main moves before your verdict:** your `ls-remote` at start, mid-gate and end, then the TARGETS rules.
- **The hosted Demo download time against the BFF's 30 s:** not measurable here (no hosted request). Item 3 gives an estimate from the hosted draw time.
- **Whether a Demo copy can pass both gates and still differ from "stored with name → alias":** item 3's judgement and item 4 (d).
- **Whether the hosted demo reset makes B215's post-deploy step redundant:** item 8, through code.
- **Whether `src.pathname` at `bff.ts:274` is normalised before the 90 s test:** S2-2.
- **Whether a pre-key customer can be made for the live showcase arm:** item 2. If not, vitest only, and say so.
- **Whether ports 6950–6959 stay free:** your `lsof` at each bind.
