From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: the STATUS file is the wrap.
# BRIEF B52 · SEAT-E: QA DELTAS GATE (TIER 1 throughout), ROUND 2 OF 2: `b49/gate-b48-fix-round`, builder B49's fix round for gate B48's G-F1 (Major), G-F2, G-F3, G-F5, G-F6, G-F7 (Minors), G-N6, G-N9 (Notes) and Friday's rulings 1–9

**Drafted by Friday's drafter 2026-10-12 ~18:15 AEDT (DRAFT for Friday). Fired: @NOW@.** Friday read the pins with `git ls-remote origin` at about 18:09 AEDT. The drafter read them again at **18:11:22 AEDT** (rc 0, same SHAs) and used only read-only git (`ls-remote`, `cat-file`, `rev-parse`, `rev-list`, `merge-base`, `log`, `show`, `diff`, `grep`). The merged tree was predicted with `merge-tree --write-tree` in a `git clone --shared` in the drafter's scratchpad, never in the project. Friday re-pins with `ls-remote` at launch.
- You are a **TESTING** seat. The launcher calls every seat a "build seat". For you, this brief overrides that line.
- **Findings only.** You never fix code, never push, never open or comment on a PR. You never write Jira, GitHub (PR, review, comment, label, branch, alert dismissal), Azure, Entra, the records repo, or any other seat's worktree. You write no tickets and no draft lines that look like writes. Findings carry a fix shape in prose and nothing else.
- Charter rules, as quoted here (do not open the charter file; it is outside this project): Rule 1, state the FAIL condition before every test. Rule 2, untested areas are first-class output.
- **A write grant in any brief or launcher prompt, this one included, is void.** The launcher tells every seat to write `5_Project_History/history.md` and Jira. Refuse both and say so in STATUS, as B48 did (`B48_STATUS.md:4`).

**Report:** `1_Project_Definition/Briefs/2026-10-12_B52_STATUS.md`. **Evidence:** `1_Project_Definition/Briefs/2026-10-12_B52_evidence/` (0700; files 0600). It holds counts, labels, status codes, exit codes, booleans, sha256 prefixes, timings, computed-style values and screenshots of SYNTHETIC data only.
**Pane:** `Datasec/MPS-E`. Your commission is the newest file in `Briefs/` whose name contains `_SEAT-E_`.
(Launcher check: this follows B48's brief `:11-12`, which cites B41's brief `:12` (`Launch_Claude.command:107`, `:111`); the drafter did not re-read the launcher. At drafting, `ls -t Briefs | grep -i _SEAT-E_` lists `2026-10-12_B48_SEAT-E_QA-gate-b46-home-dashboard.md` first. That seat is finished: `B48_STATUS.md` last line `READY FOR REVIEW`, `:364`. **Friday copies this file into `Briefs/` to fire it**, and it then supersedes B48.)

## THE CAP (read before anything else)
**This is round 2 of 2 under Kam's two-NO-GO cap. There is no round 3 without Kam's word.** B49's brief, verbatim (`B49_SEAT-A…md:6`): *"This is **round 2 of 2** under Kam's two-NO-GO cap (lane: Home dashboard; B48 was round 1 …). The next gate is a **deltas gate** over `0c74086...<your head>`. **If it says NO GO, Friday ships what is closed and tickets the rest; there is no round 3.**"* B48 was round 1 (`B48_SEAT-E…md:14`).
- **If this gate says NO GO:** the rows it closes ship. Friday merges once CodeQL is green and deploys, per Kam's *"please deploy as soon as its ready"* (B48 brief `:17`). Every residue (each NOT CLOSED row, each new finding) is ticketed. B49 is not reopened for another fix round.
- So judge **each row on its own**: CLOSED / NOT CLOSED / UNMEASURED, never "the round". Tag **every finding** with its origin: **INTRODUCED BY B49** (a regression this branch causes), **RESIDUE of G-Fn / G-Nn** (the row's fix is incomplete), or **PRE-EXISTING** (also true at base `0c74086`, measured there). A finding whose origin you did not measure at base is incomplete.
- **Write each finding so it can be shipped past:** give its severity, what a user sees on the hosted site, and whether shipping the closed rows without it is safe. Friday uses this to split "ship" from "ticket".
- A Blocker or Major is NO GO. Minors and Notes are reported. Friday decides.

## WHY SPEED AND HOSTED MATTER (as in B48)
A GO or GO WITH NOTES here, or a NO GO whose closed rows can ship, is followed by a merge and a hosted deploy by a separate seat. You never deploy or touch hosted. **Name, as a `NOTE FOR FRIDAY (hosted)`, everything that would behave differently on the hosted site**, and carry B48's still-open hosted notes (section below). **Write provisional verdict lines (marked so) as soon as items 0–3 are done**, then keep going. The final lines replace them.

Verdict lines (each GO / GO WITH NOTES / NO GO), **first in STATUS**:
- `B49 c8eda15: …`
- per area: `(a) row closure: …` · `(b) rulings 8 and 2, nothing wider: …` · `(c) role scope on the changed figures: …` · `(d) NEW WORDS (deltas): …` · `(e) non-regression: …` · `(f) mutants: …`
- `MERGE b28c95e+c8eda15: …` (when main is unmoved, the merged tree is the head tree; say so)
- `overall: …`

Then a **closure table**, one row per item: `G-F1 (Major)`, `G-F2`, `G-F3`, `G-F5`, `G-F6`, `G-F7`, `G-N6`, `G-N9`, `ruling 8`, `ruling 2 (H-13 departure)`. Each row is **CLOSED / NOT CLOSED / UNMEASURED**, with the ratio that decides it and the B48 FAIL condition it was judged against.
The last line is exactly **`READY FOR REVIEW`**. If you are stopped, the last line is **`STOPPED: NEEDS FRIDAY`** plus ONE blocking question.

## AUTHORITY
- **The original findings and their FAIL conditions:** `Briefs/2026-10-12_B48_STATUS.md` (364 lines, last line `READY FOR REVIEW`). Read it whole. Verdict lines `:6-16`; closure `:18-26`; per-area FAIL conditions `:52-61`; authZ cells `:63-84`; hand-count table `:86-107`; H/G table `:109-151`; mutant table `:170-203`; Findings G-F1…G-F7 `:205-244`; Notes G-N1…G-N12 `:246-258`; NOTES FOR FRIDAY (hosted) `:299-311`; check items `:313-319`. B48's brief `Briefs/2026-10-12_B48_SEAT-E_QA-gate-b46-home-dashboard.md` (183 lines) holds the **Tier-1 Blocker classes (`:37-44`), which stand unchanged**, the personas (`:87`) and the mock properties (`:89-103`).
- **What B49 had to do:** `Briefs/2026-10-12_B49_SEAT-A_gate-b48-fix-round.md` (242 lines). It has Rows 1–8 (`:82-138`), the write set and frozen list (`:48-59`), Tier 1 (`:61-66`), NOT YOURS (`:140-154`) and NEW WORDS (`:156-158`). **Its appended `## FRIDAY'S RULINGS ON THE DRAFTER'S DOUBTS` (`:233-242`, rulings 1–9) SUPERSEDES the rows where they differ.** Judge each row against the ruling, not the superseded row text:
  1. Row 4: open the form from `#/`, expect "Home" at `b30.spec.ts:66`, plus ONE step opening `#/quotes` that expects "Quotes".
  2. Row 2: tile 6's Seller link keeps `scope=mine` in BOTH scopes. This is a one-tile H-13 departure, with no new words.
  3. Row 8: `ceil` against the figures' `asOf`. The cell is empty when the figures failed. No `asOf` on the list body.
  4. Rows 1 and 2: the docs stay true, the contract sync is its own commit, and the changed API sentences go under NEW WORDS.
  5. `QuoteApiTests.Home.cs:587-592` is part of Row 2, changed red-first.
  6. G17 is re-anchored to the same MEANING.
  7. The stub gets the same Row 1 and Row 2 changes.
  8. **ADDED to Row 1:** the analyst's Home work queue opens on Awaiting approval while scoped to My quotes. *"Awaiting approval is an Approver list: it lists every quote the caller may approve, whatever the scope."* Red-first.
  9. A `## For the records seat` section; no records commit.
- **The builder's claims (claims, not facts):** `Briefs/2026-10-12_B49_STATUS.md` (316 lines; last line `READY FOR GATE: b49/gate-b48-fix-round c8eda15df5c88a2e343d0c0b67948c7aa25671f2`). Read it whole:
  - BLUF `:7-16`; PRIOR-WORK CHECK `:18-24`; commits `:36-49`; Test Evidence `:51-65`;
  - red-proof `:67-131`; Tier-1 `:133-139`; FOUND/TESTED/HOW per row `:141-190`; fix shapes `:192-200`;
  - modified pre-existing tests `:202-207`; NEW WORDS `:209-243`; UNMEASURED `:245-248`; NOT DONE `:250-252`;
  - for the records seat `:254-269` (new: **B49-1**, **B49-2**); merge check with b47 `:275-278`; leak scan `:280-286`; push `:301-314`.
  - B49's evidence folder, `.tools/qa-B49/` and `.tools/wt-B49*` may be **read**. Nothing in them is proof for you. **Re-measure every headline with your own instrument and your own controls; never quote B49's number as yours.**
- C-04, C-07, C-12 (ownership, no self-approval, GST), the I-2 matrix (C-13), FR-DB-010 (no GP/margin/cost on the dashboard), Kam's D-1…D-7, the approved NEW WORDS §A, the SITE HOLD, the P-1 HOLD and Q-09 (synthetic sets only) stand unchanged. You do not rule on any of them.
- **G-F4 (server `detail` texts + 3 `aria-label`s) is NOT this round.** It is on Kam's NEW WORDS card (B49 brief `:143`). Do not grade it; only confirm B49 left those strings byte-equal. The other NOT YOURS rows (G-N1, G-N2, G-N3, G-N4, G-N5, G-N7, G-N8, G-N10, G-N11, G-N12) are likewise not graded. Report any that B49 *changed*.

**Tier-1 Blocker classes:** every B48 class (B48 brief `:37-44`), whatever the path. Also these, for this round:
- any figure that a **Seller-only caller** (or an act-as-narrowed caller without Approver) gets at head that **counts another person's quote where B48's measured base did not**. Row 1's handler now builds facts over **every** quote for `scope=mine` (`QuoteEndpoints.cs:660-662` at head), so this is the new widening risk;
- `awaitingMyApproval` present for any caller without Approver **after act-as**; `awaitingMyApproval` counting the caller's own quote (C-12);
- any row datum (quote id, ref, customer, owner) in the figures body;
- any new list read from Home that returns a member or a value a persona could not read at base, or that an **Administrator-only** caller issues (H-35: 0 list calls).

## Targets (re-pin at start and before the verdict)
| What | Ref | Pin (instrument) |
|---|---|---|
| Target (head) | `refs/heads/b49/gate-b48-fix-round` | **`c8eda15df5c88a2e343d0c0b67948c7aa25671f2`** (Friday's `ls-remote` ~18:09; drafter's 18:11:22 AEDT, rc 0; `cat-file -t` = commit); tree **`045b95fe0044eb3c728f8aa8e06785dcdb6506c8`** |
| Base (B46 head = B48's target) | `refs/heads/b46/home-dashboard` | **`0c74086a9c23e485f71dc0c7e0f80d33a4c1b317`** (same calls); tree **`5efdeca4e2c25af550a4cd0d94971b7c736324b7`** = the tree B48 gated (`B48_STATUS.md:33`) |
| MPS code main | `refs/heads/main` | **`b28c95eb0f73ed0ce7ae410791feefc8b1a059ea`** (same calls); tree `2826f02744a28e7ffd5689bd1885e2b03cad68b6` |
| Merge-bases | – | `merge-base b28c95eb c8eda15` = `b28c95eb`; `0c74086` is an ancestor of `c8eda15` |
| Also on origin (not a target) | `refs/heads/b47/feedback-pill` | `81b0135d13a20b770df0669857d3043cf03653ec` (another lane; see item 7) |

**First action:**
1. `git -C 2_Project_Files fetch origin`.
2. `git -C 2_Project_Files ls-remote origin refs/heads/main refs/heads/b46/home-dashboard refs/heads/b49/gate-b48-fix-round`. All three must equal the pins. **If the head or `b46/…` differs, STOP: NEEDS FRIDAY.** If main differs, carry on with the rows and handle it in item 7 (MERGE).
3. Run the same `ls-remote` again immediately before the verdict lines. A head that has moved voids the verdict.

**Measured by the draft writer (re-measure; do not trust):**
- `rev-list --left-right --count 0c74086...c8eda15` = `0 10`; `b28c95eb...c8eda15` = `0 18`. This is a fast-forward of main. **Predicted merged tree = `045b95fe…` = the head tree** (`merge-tree --write-tree b28c95eb c8eda15` → `045b95fe…`, rc 0, in a scratch `clone --shared`).
- `git diff --shortstat 0c74086 c8eda15`: **14 files, +474 / −60**. Per file:

  | File | Lines changed |
  |---|---|
  | `docs/API.md` | 13 |
  | `docs/api/openapi.json` | 6 |
  | `QuoteEndpoints.cs` | 7 (one hunk, in `Figures`) |
  | `QuoteFigures.cs` | 17 |
  | `QuoteApiTests.Home.cs` | 8 |
  | `QuoteApiTests.HomeB49.cs` | +152 (new) |
  | `web/e2e/b30.spec.ts` | 5 |
  | `web/e2e/b46-home.spec.ts` | +38 |
  | `web/src/api/generated/SOURCE.txt` | 4 |
  | `web/src/api/generated/openapi.snapshot.json` | 6 |
  | `web/src/api/generated/schema.ts` | 10 |
  | `stubApi.ts` | 6 |
  | `Dashboard.tsx` | 87 |
  | `Home.test.tsx` | 175 |

  Frozen numstat over a subset of B49's frozen list = **0 lines**: `Dtos.cs`, `web/src/auth`, `QuoteList.tsx`, `router.ts`, `styles.css`, `playwright.config.ts`, Engine, Import, `.github`, `infra`, `scripts`. Control: `src/MpsCalc.Api/Quotes` gives 2 lines. **Run the full frozen list yourself** (B49 brief `:53-57`).
- **Commits** (oldest first; author = committer time):
  - `5596d47` Row 1 (16:58:06)
  - `478b9f7` Row 2 (16:59:53)
  - `5c8fd0c` contract (17:00:09)
  - `1d22818` Row 7 (17:00:35)
  - `ec00f68` Row 3 (17:01:43)
  - `f24c129` Row 8 (17:02:59)
  - `5632a02` Row 6 (17:03:42)
  - `fc0f4b5` Row 5, `72e375a` Row 4 and `c8eda15` e2e tile 6 — **all three at 17:09:30**

  **All 10 commits were made in 11 min 24 s**, inside a run that B49 dates 16:51–18:07 (`B49_STATUS.md:2`). The pushed branch was then measured for an hour. Treat B49's per-row "RED at base / at the previous row's code" claims (`:71-82`, e.g. `:76` *"on the Row 1 code"*) as **unmeasured per commit** until you re-run them (item 0).
- **New code at head (anchors; re-derive each, count 1/1):**
  - **Server.**
    - `QuoteEndpoints.cs` `Figures` `:636-666`: the scope check is unchanged (`:648-655`). The loop now adds **every** quote's facts (`:658-662`, comment *"Every quote: the Seller figures narrow to scope inside Figures; awaitingMyApproval never does (B49 Row 1)"*).
    - `QuoteFigures.Figures` `:143-171`: `every` = all facts in quoteId order (`:147`); `facts = scope == "mine" ? every.Where(IsMine) : every` (`:148`). The closed figures, `approved`, `outOpen` and `followUpDue` run over `facts`.
    - `AwaitingApproval = caller.Is(Seller) ? Of(every.Where(IsMine && Submitted))` (`:168`); `AwaitingMyApproval = caller.Is(Approver) ? Of(every.Where(CallerCan.Approve))` (`:169`).
  - **Stub** `stubApi.ts:237-240`: the same two lines over `rows` (with `r.isMine`), not `inScope`.
  - **Web** `Dashboard.tsx` (head line numbers):
    - `quotes(n)` `:19`; `APPROVABLE = { status: 'submitted', canApprove: 'true' }` `:23`.
    - **`queueRows` `:29-32`**: for an Approver it **replaces** the queue's whole `submitted` group with the approvable rows. It applies to *every* Approver (pure Approver too), in **both** scopes, and on the search/owner path (`:420-424`). So the analyst's **own** Submitted quotes leave its Home queue in either scope.
    - `periodDay` guarded reads `:72-73` (B49's extra Row 3 fix, `B49_STATUS.md:155`).
    - Tile 6 Seller href `{ scope: 'mine', status: 'submitted' }` `:113` (ruling 2); `alone &&` sentence `:172`; tile 2 `:193`.
    - `daysSince` `:220-223`; hint `:242`.
    - `approver = persona.roles.includes('Approver')` `:355`; whether `persona.roles` is the **effective** role set after act-as in Entra mode decides whether a Seller+Approver acting as Seller issues the approvable read. **Measure it.**
    - The approvable read effect `:405-415` (on error: `setApprovable([])` + `setError(e)`); the loading gate `rows === null || (approver && approvable === null)` `:506`; `alone=` `:495`; `FollowUp asOf={figures?.asOf}` `:510`; `WorkQueue rows={queueRows(…)}` `:512`.
  - Tests: `QuoteApiTests.HomeB49.cs` has 5 methods = 6 cases: `B49_1` ×2 Facts, `B49_2` ×1, `B49_7` July Theory ×2 InlineData, `B49_7` boundary ×1. × DevStub/Entra = **+12** (B49 `:57`). `b46-home.spec.ts` `beforeEach` live-skip + 4 "B49 tile 6 = its list" tests; `b30.spec.ts:66` → "Home", plus `goto('/#/quotes')` → "Quotes" at the end of G-13.
- **Merge with the other lane (B49 `:275-278`):** `b47/feedback-pill` × `c8eda15` conflicts in `docs/api/openapi.json` (1 hunk) and `EntraAuthTests.cs` (2). B49 says the same conflicts occur at `0c74086` (pre-existing B46 × B47). Re-measure it in your clone. It is a merge-order fact for Friday, not a B49 finding unless B49 adds a hunk.
- Ports at drafting: `lsof -nP -iTCP:6650-6659 -sTCP:LISTEN` → rc 1, **0 lines** (18:12:17 AEDT); `6640-6649` → rc 1, 0 lines (B49 closed, `B49_STATUS.md:291`).
- `.tools/wt-B52*` and `.tools/qa-B52` do not exist. `.tools/wt-B48{,-base,-clean,-mut}`, `qa-B48/`, `wt-B49{,-base,-clean,-mut}`, `qa-B49/` and `wt-B50-design` exist: **never use any of them in place.**

## Your setup (own worktrees, own ports, own state)
- **Worktrees** (`chmod 700`; never removed). Create each with `git -C '<project>/2_Project_Files' worktree add --detach '<project>/.tools/<name>' <sha>`:
  - `.tools/wt-B52-base` at `0c74086…` (the round-1 tree);
  - `.tools/wt-B52` at `c8eda15…` (= head);
  - `.tools/wt-B52-mut` at `c8eda15…`: mutants and the per-commit red-first re-runs (item 0) only. Restore by sha256 after each.
  - `.tools/wt-B52-clean` at `c8eda15` (`scripts/package.sh`, Entra-fake package only);
  - `.tools/wt-B52-base-clean` at `0c74086`, for the base Entra-fake;
  - `.tools/wt-B52-main` at `b28c95eb`, for the list-vs-`/proposal` widening oracle (B48 brief `:39`).
- **Tool output:** `…/.tools/qa-B52/` (0700). Point Playwright `--output`, `MPSCALC_E2E_EVIDENCE_DIR`, `MPSCALC_E2E_SHOTS`, vitest caches and browser profiles there. **Always set `MPSCALC_E2E_BASE_URL`, `MPSCALC_WEB_PORT` and `MPSCALC_API_ORIGIN`.**
- **Copied instruments: the GATE's, from `.tools/qa-B48/tools/`** (rename `*52*`). Candidates: `env48.sh`, `apictl48.sh`, `build48.py`, `age48.py`, `model48.py`, `probe48.py`, `compare48.py`, `outcome48.py`, `tzread48.py`, `mut48.py`, `mutprobe48.py`, `webmut48.py`, `click48.mjs`, `fail48.mjs`, `stale48.mjs`, `ui48.mjs`, `render48.mjs`, `screens48.mjs`, `b48lib.mjs`, `probe16.mjs`, `words48.py`, `newwords48.py`, `checkwords48.py`, `words48cs.py`, `leak48.py`, `leakscan.py`, `qalib.py`, `lib48.py`, `jwt.py`, `oidc_stub48.py`, `dotnet_suite48.sh`, `web_suite48.sh`, `e2e48.sh`, `e2eall48.sh`, `Gate48DstTests.cs` (and the quarantined `.tools/_quarantine/2026-10-12_B48_gate-dst-test-file/`, **copied**, never moved).
  - **Copy, never run in place, never edit a running script.** You may **read** `qa-B49/tools/`. **Do not copy B49's `model49.py`, `probe49.py`, `click49.mjs`, `fail49.mjs`, `mut49.py`, `webmut49.py`, `e2emut49.sh`, `e2esel49.sh` or `mutall49.sh`.** The builder's instruments are what you are checking. B49 also **edited the gate's oracle** (`model49.py` `figures()`, `B49_STATUS.md:200`) and graded itself against it.
  - **Update your own `model52.py` from Friday's rulings (rows 1, 2 and ruling 8), not from B49's diff.** Print your model's diff against `model48.py` in STATUS, and show that it reproduces B48's hand count at base `0c74086` (13/13) before you use it at head.
  - Name every copied script in STATUS and show each control fired **in this run**. New gate keys in `qa-B52/keys/` (0600). Never reuse another gate's keys or GUIDs. User ids `gate52-*`.
- **Synthetic data only.** Reference store: a copy of `qa-B48/syn/v1.json` (sha256 `02078bb6…`, B48 `:351`) into `qa-B52/syn/`, with its sha256 stated. Quotes: rebuild **B48's 30-quote aged store** through the API with your copy of `build48.py` + `age48.py`. It has two Sellers, Seller+Approver, Seller+PA, one pre-owner quote, one legacy repeated-`lineNumber` quote, Q-7, every status, and the boundary instants of B48 `:87`.
  - **Add at least: one Submitted quote owned by the Seller+Approver (the analyst), one pre-owner Submitted quote, and one Submitted quote by an identity holding Approver only, if one is creatable (else say why).** Rows 1, 2 and ruling 8 turn on exactly these.
  - DevStub roots go under `<work tree>/.local/b52-*` (DevStub refuses a store elsewhere, B48 `:322`). Entra-fake roots go under `qa-B52/roots/`.
  - Every process sets `MpsCalc__ReferenceStorePath` to **your synthetic** `v1` and `MpsCalc__QuoteStore__Path` / `MpsCalc__CatalogueOverlay__Path` to your roots. The version store stays **off**. **Never start a process on the shipped Development reference path** (`appsettings.Development.json` → `../../.local/pricebooks/reference.json`).
  - Your probes write outcomes (B48 incident 4: the trailing-slash arm records one). So **build a fresh store per run and per side**, and never re-read a store a previous run wrote to (B49 had to set two runs aside, `:298`).
- **CONFIDENTIAL inputs:** `1_Project_Definition/Source_Documents/2026-10-10_example-client-quote/**` and the price books. Use them for the avoid list only (copied list loaders; never print the lists).
- **Allowed git verbs:** `fetch`, `ls-remote`, `worktree add --detach`.
  - Inside your own `wt-B52*` only: `checkout --detach` (the per-commit red-first runs, in `wt-B52-mut`), `restore`, `status`, `diff`, `show`, `log`, `rev-parse`, `archive`.
  - For the MERGE line and the NEW WORDS planted control: a `git clone --shared` into `qa-B52/merge/`, and `merge-tree --write-tree` / `merge` / local commits **there only, never pushed**.
  - Read-only on the records repo (project root): `--no-optional-locks` `log`, `show`, `rev-parse`, `ls-tree`.
  - **Forbidden:** any branch or tag in `2_Project_Files`, `push`, `merge` to any shared ref, `gc`, `prune`, `worktree remove/prune`, `reset` on a shared ref, deleting any lock, and any git verb in `2_Project_Files` other than `fetch`, `ls-remote` and `worktree add`.
- **Ports: 6650–6659 (B48's range). B48's seat is closed** (`B48_STATUS.md` last line `READY FOR REVIEW`; its read-back `:347` gives 0 listeners). **Friday reassigns 6650–6659 to B52.** This overrides the standing "never use a port named in an earlier brief" line for this range only.
  - Layout:

    | Port | Use |
    |---|---|
    | 6650 | head API, DevStub |
    | 6651 | base API (`0c74086`), DevStub |
    | 6652 | head Entra-fake (real package from `wt-B52-clean`, same-origin SPA) |
    | 6653 | base Entra-fake (from `wt-B52-base-clean`) |
    | 6654 | head web, stub |
    | 6655 | head web, live (→ 6650) |
    | 6656 | base web, live (→ 6651) |
    | 6657 | mutant API / web |
    | 6658 | spare: main API for the widening oracle, TZ arms, figures-500 API |
    | 6659 | OIDC/JWKS stub |

  - **Run `lsof -nP -iTCP:<port> -sTCP:LISTEN` before every bind. On any listener you did not start, STOP: NEEDS FRIDAY** (do not move ranges on your own).
  - **Never bind** 6640–6649 (B49), 6620–6629 (B50's range), 6590–6639, 6660–6699, 696x, 6750–6919, 5000, 5080, 5173, 5183, 5580, 5780–5783, 588x, 5960–5969, 5990–5999, 6280, 6283, 6470–6479, 6968, 6970, 7000, 7768, 10022–10082, or any other port named in the B22–B50 briefs and STATUS files. Never touch a listener that is not yours.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`. Build with `-nodeReuse:false -p:UseSharedCompilation=false`. Run `dotnet build --no-incremental` then `dotnet test --no-build`. **After every tamper restore, `touch` the file and build `--no-incremental`.**
- **Processes:** stop by port + cwd (or a pid you recorded), never by name. Everything you started is stopped before READY. `caffeinate`, the shared `VBCSCompiler` and `@playwright/mcp` belong to Friday.
- **Instruments:** `cmd > out 2>&1; rc=$?`; never take an exit status through a pipe. Every verdict is a ratio with its denominator. Every scanner zero and every tamper has a control that fired. The shell is zsh: run loops via `bash -c '…'`, and use `nullglob`. Each tamper uses a unique anchor. Prove each restore by sha256 and by `git -C wt-B52-mut status --porcelain` being empty.
- **Personas** (B48 brief `:87`, unchanged):
  - Seller A, Seller B, Seller+Pricing analyst, Approver, Seller+Approver (the analyst, `devPersonas.ts:14-16`), Administrator only, Pricing analyst only, all four, no role, no identity;
  - Administrator acting as Seller; Seller+Approver acting as Seller; all four acting as Seller; Seller acting as Approver / Administrator.
  - Use **three modes, as B48 did (`:8`): DevStub headers, Entra-fake tokens, and the UI store.** Entra-fake means the real package, gate-random GUIDs, `AzureAd__MetadataAddress` → your stub on 6659, and tokens minted locally with a NEW key, never printed and never written to an output file. Mint at least one token with a `name` claim and one without.

## Items. State each FAIL condition before you run it.
For **every row**, the per-row table in STATUS has four columns:
- **(i)** B48's **original FAIL condition**, quoted with its `B48_STATUS.md` line, re-run with your copy of B48's instrument at base (it must reproduce B48's failure there, or your instrument is blind; say so) and at head;
- **(ii)** an independent re-measure of B49's headline claim, with its own positive and negative control;
- **(iii)** mutants (item 6);
- **(iv)** the row's own question below.

0. **Pins, scope, commit map, partition.**
   - Re-pin. Confirm head tree `045b95fe…` and base tree `5efdeca4…`.
   - Run `git diff --name-status` per commit and map each to its row. Check every path against B49's write set (brief `:48-50`): out of set = a finding; a frozen path (`:53-57`) = Blocker. Name each cross-row hunk: Row 3's `periodDay` guard is inside `ec00f68`, and `c8eda15` carries Rows 1–2 e2e.
   - **`QuoteEndpoints.cs`: the only hunk is inside `Figures`.** Prove the list, outcome and proposal handlers are byte-equal, with a function-scoped diff.
   - `5c8fd0c` touches only `web/src/api/generated/**`. Re-run `sync-contract.mjs 478b9f7` in a scratch `git archive` copy: byte-equal except the header ref, and the snapshot = `docs/api/openapi.json` at head.
   - Blob ids base vs head: `pricePolicy.ts`, `PricingPolicy.cs`, `Proposal.cs`, `Dtos.cs`.
   - **G-F4 strings byte-equal:** the 8 server texts and 3 `aria-label`s of B48 `:287-294` at head (`git grep -c`, 11/11).
   - **Per-commit red-first (the commit-cadence doubt above):** in `wt-B52-mut`, `checkout --detach` each row's commit and its parent. Run that row's new tests on the parent (expected RED, with count) and on the commit (GREEN). Do it at least for Rows 1, 2 (`5596d47`, `478b9f7`), 3, 6 and 8 (`ec00f68`, `5632a02`, `f24c129`). Reconcile with B49 `:71-82`.
   - FAIL: as stated.
1. **(a) Row closure: each row against its ORIGINAL FAIL condition.**
   - **G-F1 (Major).** B48 `:209`: *"tile count ≠ the rows of the list it opens; figure ≠ the brief's rule."*
     - Instruments: copies of `probe48.py` + `model52.py` (hand count, every persona × scope, **× 3 modes DevStub / Entra-fake / UI store**) and `click48.mjs` (all **60 click arms**, label + corner, live).
     - Expected: Seller+Approver `mine` `awaitingMyApproval` = the approvable list's rows. B48 measured 4 there; recompute it on your store. All four `mine` = 5 on B48's store. Tile = list on 60/60, **count and value** (B49's 60/60 counts; B49 itself re-measured 16/60 money mismatches, all Q-7 (G-N5), `:261`: reconcile every money miss by name).
     - Entra-fake: Seller+Approver+PA acting as analyst (B48 `:212`).
   - **G-F2.** B48 `:219-220`: Seller A `scope=all` `awaitingApproval` = their own Submitted (B48's store: 3, not 5), **and** = the rows of the list tile 6 opens (B48 brief click-through FAIL `:56`). Both scopes, 3 modes, plus a pre-owner Submitted quote (nobody's: counted by no Seller).
   - **G-F3.** B48 `:229`: *"figures 500 gives no tile carrying that sentence."*
     - Copy of `fail48.mjs`, live, with a route-level 500 on `/quotes/figures` only (a mutant API on 6657/6658): Seller 0/6, Approver 0/6, Admin 0/5. Each tile still has "—", "Could not load this figure." and Retry; follow-up and queue render; the page is not blank.
     - Stub seam (`mpscalc.stub.figuresOmit`): one omitted figure → that tile only, **with** the sentence, for **every** figure key (8: the six tiles, plus the closed pair B49 newly guards). B48 did only 2.
     - The seam key is still absent from the Entra build: `check-bundle` with its control, plus a `dist/` grep with a positive control.
   - **G-F5.** B48 `:236`: `b30.spec.ts:55` RED at head stub.
     - Expected: GREEN at head stub, RED at base stub.
     - The diff touches **only** G-13 (`:55-81`): `:66` → "Home", plus the `#/quotes` step at the end, matching ruling 1. No other assertion is removed or weakened.
   - **G-F6.** B48 `:240`: 9/9 b46 red in live mode.
     - Expected at head live: every `b46-home` test **skipped, not failed** (13/13); at head stub: 13/13 passed.
     - Tamper: skip removed → live RED.
     - Measure that the `beforeEach` skip (`goto('/#/')` → detect "API STUB ON" → `about:blank`) does not mask a stub-mode failure. Plant a deliberate stub-mode failure in a copy of the spec: it must still fail.
   - **G-F7.** B48 `:244`: "1 quotes need follow-up".
     - Rendered, live and stub: tile 2 and the hint for n = 0, 1, 2. Expected: "0 quotes · AUD ex GST" / "0 quotes need follow-up"; "1 quote · AUD ex GST" / "1 quote needs follow-up"; "2 quotes…" / "2 quotes need follow-up".
     - `git grep` over B46's and B49's web diff for every other built "n quotes" string. The count nouns ruled out (B49 brief `:121`) are only listed.
   - **G-N6.** B48 `:252`: a due row at 14 d + 1 min reads "14 days".
     - FAIL: any due row reading ≤ 14 days; a days cell that moves with the browser clock (run the page with the browser clock ±2 days via `page.clock` or an init-script `Date` offset); a number shown when the figures read failed.
     - Measure on the **aged store, live**, every due row, cell by cell, against `asOf`. B49 did not (`:190`).
     - **Time the gap** between the list and figures reads over 20 loads, p50/p95/max (B49 calls the skew "ms apart" but left it UNMEASURED, `:189`, `:247`). Plant a row at 14 × 24 h − Δ, with Δ inside your measured gap if achievable, and say whether "14 days" can show.
   - **G-N9.** B48 `:255`: G8, G9 and G17 green on B46's suite.
     - Expected: each RED on the **full API suite** at head (B49 claims 4/846, 2/846, 6/846). Apply each from **your** copy of `mut48.py`; **G17 re-anchored by you** to the meaning *"count every Submitted in place of `callerCan.approve`"*, independently of B49's re-anchor (`:181`).
     - List the failing test names. B49 `:130` says G17 kills `B49_1` "×2 tests" + `B46_2_red_a_pricing…` ×2. That implies `B49_1_red_awaiting_my_approval_exists_only_for_an_approver_after_act_as`, described as a presence test (`:74`, `:135`), fails too. Settle which tests die.
     - Also run the **gate's DST test** (copied from the quarantine, never committed; B49 did not run it, `:182`) at head: 8/8. G7 and G8 each go RED on it.
2. **(b) Ruling 8 and ruling 2: what was ruled, and nothing wider.**
   - **Ruling 8** (B49 brief `:241`). Request-count and DOM probe, live + stub, every persona × scope:
     - Who issues `GET /quotes?status=submitted&canApprove=true`, with which params. Expected: only callers holding Approver **after act-as**; **0 for Administrator-only** (H-35: 0 list calls in total); 0 for Seller-only; 0 for Seller+Approver acting as Seller. That last one decides whether `persona.roles` (`Dashboard.tsx:355`) is the effective set in DevStub and in Entra-fake.
     - The Awaiting approval tab count and rows = tile 6 = the approvable list, for the analyst in **both** scopes and for the pure Approver.
     - The other tabs (Drafts, Rejected, Recently approved) keep the scope's rows (count vs base).
     - **What leaves the queue.** `queueRows` (`:29-32`) replaces the whole `submitted` group, so the analyst's **own** Submitted quotes no longer appear in its Home queue in **either** scope. Count them, base vs head.
     - **The pure Approver.** Its queue changed too (B49 `:193`: *"equals what it showed before unless a Submitted quote is one it may not approve"*). Count the rows that differ from base.
     - **The search/owner path** (`:420-424`) now merges two reads. Check the merged rows for duplicates and for a quote shown that matches neither filter.
     - **An approvable read that fails.** Inject a 500 on that read only: what shows (ErrorBox + empty tab? "Loading…" forever?).
     - **Rate each as "what was ruled" or "wider than ruled".** Ruling 8 names the analyst "while scoped to My quotes" and states the rule generally ("whatever the scope"). Quote it, and give the gate's reading with counts. Do not rule for Kam.
     - Also rate B49's new item **B49-1** (`:268`): a Seller-only's tab under All quotes lists everyone's Submitted while tile 6 counts their own. Measure it, and confirm the click-through still agrees.
   - **Ruling 2** (`:235`). Every tile href for every persona × scope at head vs base (H-13). Expected exactly **one** difference: the Seller-**without**-Approver tile 6 under All quotes, `#/quotes?status=submitted` → `#/quotes?scope=mine&status=submitted` (`Dashboard.tsx:113`). The Seller+Approver tile 6 and every other href are byte-equal. Its words are unchanged.
   - FAIL: a wider change not stated by B49 as a deviation; any Administrator list call; any approvable read by a caller without Approver after act-as.
3. **(c) Role scope on the CHANGED figures (TIER 1).**
   - **The `/figures` cell matrix**, full, from your copy of `probe48.py`: every persona × {no query, `scope=all`, `scope=mine`, `MINE`, empty, repeated, unknown} × **3 modes**. Compare it with B48's table (`:63-84`) cell by cell.
   - **`awaitingMyApproval` presence after act-as:** present iff the effective roles hold Approver. Expected absent for: Seller+Approver acting as Seller (both scopes), all four acting as Seller, Seller alone, Administrator alone. Present for: Approver, Seller+Approver, all four.
   - **Widening vs base (the new risk).** For each persona × scope × figure, give base `0c74086` vs head on the **same** store:
     - the only increases allowed are `awaitingMyApproval` for Approver-holders under `scope=mine` (Row 1);
     - the only decreases allowed are `awaitingApproval` for Sellers under `scope=all` (Row 2);
     - **any other change, and any Seller-only figure that counts another person's quote, is a Blocker class.** Prove the Seller-only `scope=mine` figures (`provided`, `outOpen`, `followUpDue`, `closedMonth`, `closedYtd`, `awaitingApproval`) count only quotes whose `IsMine` is true. Use a planted other-owner quote in every status as the control.
   - **Figures body aggregates only:** member set = `QuoteFiguresDto`, plus a scanner for quote ids / refs / customers / owners / cost keys (planted control).
   - **List-vs-`/proposal` widening** (B48 brief `:39`, B48 `0/208`): B49 **did not re-run it** (`:252`). Re-run your copy of `compare48.py` at head against main `b28c95eb` `/proposal` (6658), including the rows of the **new** approvable read Home now issues. Expected 0.
   - **Host TZ on the changed figures code:** `TZ=UTC`, `Australia/Sydney`, `America/Los_Angeles` → figure bodies byte-equal (`asOf` dropped), 3/3.
   - FAIL: any Tier-1 class.
4. **(d) NEW WORDS for the deltas.**
   - **Source level:** copies of `newwords48.py` / `checkwords48.py` / `words48.py` over `0c74086...c8eda15`, with your own planted control (in the `--shared` clone: an undeclared string in `Dashboard.tsx` and a changed `API.md` sentence at a local commit, never pushed; both flagged). Give your counts per class vs B49's (29 = 15 added + 14 removed, `:243`).
   - **Reconcile B49's own contradiction:** `:243` gives *"UNDECLARED 1 = the "n days" template"* and also *"declared 29, missing 0"*, under a heading claiming *"0 new words"* (`:209`). Settle whether the template is a new word.
   - **Rendered:** your extractor over the deltas' states only, stub and live. List text nodes and `aria-label` / `data-label` / `placeholder` apart. The states:
     - tile 2 and the hint at n = 0, 1, 2;
     - the whole-figures-fail state and the single-figure-fail state (each key);
     - the closed-figure-missing-alone state (B49's extra Row 3 fix);
     - ruling 8's queue: the analyst in both scopes, the pure Approver, and the approvable-read-failed state;
     - the days cell with and without `asOf`.
     Every string must be §A, a declared B49 change, or **undeclared** (a Minor each).
   - **API doc sentences:** re-derive each changed `docs/API.md` line and `openapi.json` description (B49 `:218-241`) **against the code**. Check each claim:
     - "`awaitingApproval` and `awaitingMyApproval` ignore `scope`";
     - "the caller's own Submitted quotes, in both scopes";
     - "over every quote: it ignores scope";
     - "scope=all, or no scope, counts every quote", which stays true for the Seller figures only.
     Measure each against an API read. `docs/API.md` and `openapi.json` must say the same thing.
   - Scan against the example-document lists (copy of `leak48.py`, counts only, controls fired).
   - **G-F4 is not this round:** confirm its 11 strings are unchanged (item 0) and nothing more.
   - FAIL: an undeclared user- or API-visible string (Minor each); a doc sentence false against the code (Minor); any example-document word (Blocker).
5. **(e) Non-regression over the full suites.** Base in `wt-B52-base`, head in `wt-B52`.
   - **.NET.** Release `build --no-incremental`, 0 warnings. `test --no-build` per project: Engine 235/235, Import 72/72 both sides; API **834 → 846** (B49 `:55`). Reconcile the +12 by name (`--list-tests`, `comm`): 6 cases × 2 modes, 0 removed. `dotnet list package --vulnerable --include-transitive` 0.
   - **Web.** `npm ci` / `lint` / `typecheck` / `build` rc 0; Entra build + `check-bundle` with control. vitest **358 → 376** (52 files both). Reconcile the +18 by name. B49 says *"10 names added … expanded: Row 1 4, Row 2 2, Row 3 5, Row 6 3, Row 8 4"* (`:59`): explain the 10 vs 18. `contract.test.ts` green.
   - **Modified pre-existing tests** (B49 `:202-207`): give each before → after and say whether it weakens a guard.
     - `QuoteApiTests.Home.cs:523` (2 → 1);
     - `:587-592` (fixture `FiguresSet` → `FiguresSetWithAnalystSubmitted`; `awaitingApproval` 2 → 1);
     - `Home.test.tsx` `due()` re-dated to a fixed `FIGURES_AS_OF`: does any B46 follow-up assertion now pass for a reason other than before?
     - `b30.spec.ts:66`;
     - the `b46-home.spec.ts` `beforeEach`.
   - **Full Playwright `web/e2e/`, stub AND live (synthetic store), base AND head**, counts per spec, every failure named. B49's figures (`:60-61`): base stub 23 passed / 9 skipped / 2 failed (`smoke:13`, `b30:55`); head stub 28/9/1 (`smoke:13`); base live 18/6/10; head live 18/19/1. Expected at head: only `smoke:13` fails (B36 N-7, pre-existing). Prove it is the same line, step and locator at base in both modes. Any other change vs base is a finding at its own severity.
   - **Re-sample B48's GO areas only where the deltas touch them:**
     - **H/G properties:** copy of `ui48.mjs`, stub + live + Entra-fake, 1440 and 390, Seller mine/all, Approver, Seller+Approver mine/all, Admin. Properties: **H-10** (tile 2 count line; your regex must accept "1 quote", and B49's probe regex did not, `:131`), **H-13** (the ruled departure only), **H-16**, **H-17…H-22** (hint and days), **H-23…H-28** (queue tabs and counts under ruling 8), **H-29** (with the planted control) and **H-35**. **Your untampered head control must pass every property, or you name each rule-backed exception with its ruling.** A dirty control voids the W8 and G15 verdicts (B49 `:125-131`).
     - **Outcome write** (B48 area 4): the handler is untouched (item 0). Sample 2 writes (owner + Approver; DevStub + Entra-fake) byte-clean with exactly one event, and the Record outcome control from the follow-up row after `FollowUp`'s prop change (`loadedAt` → `asOf`): choose → confirm → the row leaves, tiles refresh.
     - **No query = base:** `GET /quotes` with no query string at base vs head, Seller / Approver / Seller+PA, 0 diffs.
   - FAIL: an unreconciled count, a warning, a red not at base, a weakened guard, a re-sampled property that fails without a ruling.
6. **(f) Mutants.**
   - **The gate's own 17 (B48 `:185-203`)**, re-applied from your copy of `mut48.py` at head: at least G8, G9, G17 (item 1) plus G1, G3, G4, G7, G11, G12 and G13. **G12 and G13 must be re-anchored by you** (Row 1 moved `QuoteEndpoints.cs:662` into `Figures`; B49 `:94-95`). Each RED on the full suite or your probe; say which.
   - **B46's sample (B48 `:171-183`):** at least A3, A5, A6, A16 and W5. Run W5 **on the probe too** (B49 ran vitest only, `:124`).
   - **B49's own tampers:** re-create at least R1, R1b, R2b, WR1q, WR3 and WR8e from their descriptions (`:87-123`), unique anchors, and confirm RED.
   - **Yours on the deltas, at least 8, independent of B49's.** Suggested:
     - (H1) `queueRows` applied for a Seller without Approver;
     - (H2) the approvable read sent with the scope's `scope=mine`;
     - (H3) the approvable read issued when `reads` is false (Administrator-only; H-35's request count must catch it);
     - (H4) `facts` = `every` for `scope=mine` (the Seller figures over everyone: the widening guard; must go RED);
     - (H5) `AwaitingApproval` without `IsMine` only under `scope=mine`;
     - (H6) `daysSince` with `Math.round`;
     - (H7) `quotes()` singular at 0;
     - (H8) `alone` true on a whole failure for the closed pair only;
     - (H9) the stub `awaitingMyApproval` over `inScope` (stub only: does any e2e or vitest catch a stub/server split?);
     - (H10) `queueRows` keeps the analyst's own Submitted rows beside the approvable ones (a model of the "nothing wider" alternative: does any test pin today's choice?).
   - A tamper green on suite and probe is **UNVERIFIED**, with the term named.
   - Restore each by sha256, with `git status --porcelain` empty. The restored tree builds and runs 846/846 and 376/376.
   - FAIL: a mutant green without UNVERIFIED stated; a restore not proven.
7. **(g) The MERGE line.** Re-read main with `ls-remote` at verdict time.
   - **Main = `b28c95eb`:** in `qa-B52/merge/` (`git clone --shared`), `merge-tree --write-tree b28c95eb c8eda15` must print the head tree `045b95fe…`, and `rev-list --left-right --count` must give `0 18`. So **MERGE = the head's verdict**; say so.
   - **Main has moved:** run the merge there and record conflicts and the merged tree. Re-run the .NET and web suites on the merged tree in a worktree of your own clone, and give MERGE its own verdict. A conflict in B46's or B49's write set → STOP: NEEDS FRIDAY. An untested merged tree is `MERGE: UNMEASURED`, never GO.
   - **Other lane, for Friday's merge order (not a verdict input):** `merge-tree` of `81b0135` × `c8eda15` and `81b0135` × `0c74086`: conflict paths and hunk counts. Expected (B49 `:277-278`): `openapi.json` 1 hunk and `EntraAuthTests.cs` 2 hunks on both, so B49 adds 0.
8. **Leak and secret scan.** Copies of `leak48.py` / `leakscan.py` / `qalib.py` (avoid lists in `qa-B52/`, 0600).
   - Scan the added lines of `0c74086...c8eda15` and `git log --format=%B 0c74086..c8eda15`, with a planted control per class, **counts only**.
   - `gitleaks git --log-opts=0c74086..c8eda15 --redact`, with a fresh control repo.
   - Re-adjudicate B49's hits (`:282-283`: e-mails 4 `@example.test`; example-number collisions 21 = 2026 / 500 / 900).
   - **Classify the author line from commit metadata alone; do not open `4_Credentials/.env`.**
   - Self-scan your STATUS and evidence before READY: 0 after adjudication, 0 `eyJ…`, 0 planted markers.
9. **CodeQL / CI.** If a PR from `b49/gate-b48-fix-round` exists and this seat has a **read-only** GitHub identity for `datasecau`, read its check runs and code-scanning alerts for `c8eda15` (counts, rule ids, `file:line`; never dismiss, comment or re-run). Otherwise mark CodeQL/CI **NOT TESTED** with the reason (launcher WARN: no `gh` login in `4_Credentials/.gh-config`, B49 `:3`). Never borrow another project's identity. CI does not run Playwright (B48 `:236`).

## NOTES FOR FRIDAY (hosted): carried from B48. Repeat each one still open, with what this round changed.
- **P-1 / `[B38-L2]` first** (B48 `:300`, PRE-1 `:314`): the hosted repeated-`lineNumber` count comes before deploy. This round adds no write path. It does add a **second list read** on every Approver's Home (ruling 8), so each Approver Home load now reads every quote's snapshots twice plus once for the figures. Time it on 500 and 2,000 synthetic quotes, p50/p95, base vs head (B48's table `:305-310`).
- **Entra display-name collapse G-N2** (B48 `:248`, `:301`, PRE-2): unchanged rule (`CallerResolver.cs:122`, frozen). Re-measure only that Row 2's `IsMine` is identity-keyed (two "Signed-in user" Sellers do not see each other's Submitted in tile 6).
- **Pre-owner quotes** (B48 `:302`): after Row 2, a pre-owner **Submitted** quote is counted by no Seller's tile 6 in either scope (before: counted under All quotes). Friday's hosted count of `Owner == null` should now split out Submitted.
- **Sydney time-zone lookup on Linux** (B48 `:303`, POST-1): `QuoteFigures.cs:33` static field, unchanged. POST-1 stands: `GET /api/v1/quotes/figures` 200 after deploy.
- **Rollback drops outcome** (B48 `:304`, PRE-3): unchanged by this round; PRE-3 stands.
- **e2e not in CI:** G-F5 and G-F6 are now fixed in the specs, but CI still does not run Playwright, so a regression in them would not show on the PR.
Put them in a `## Post-deploy and pre-deploy check items` section, each with its FAIL condition (B48's PRE-1…PRE-3, POST-1…POST-3 carried, updated).

## NOT TESTED here (list each in STATUS with its reason; none is a gate pass)
- **Hosted:** nothing deploys; no hosted read. That covers real Entra tokens, hosted counts, the hosted clock and zone database, and hosted rollback (the check items above).
- **G-F4** (Kam's card) and the other NOT YOURS rows: not graded; changes to them are reported.
- CodeQL / CI unless item 9 could read them. Real price books (Q-09). Windows file semantics. Browsers other than Playwright's Chromium.

## Severity, findings, STATUS shape
- Severities: **Blocker / Major / Minor / Note.** The Tier-1 Blocker classes are at the top. Use new finding ids **D-F1…** and notes **D-N1…** (G-Fn / G-Nn are B48's).
- **Each finding:** id, severity, **origin tag** (INTRODUCED BY B49 / RESIDUE of G-Fn|G-Nn / PRE-EXISTING, with the base measurement), `file:line` at `c8eda15`, then **FOUND** / **TESTED** (FAIL condition, steps, expected vs actual, counts) / **HOW** (fix shape plus the regression test the owner should add, in prose) / **SHIP-PAST** (what a hosted user sees; safe to ship the closed rows without it: yes/no, why). Write no code.
- **Order of the STATUS:**
  1. verdict lines and the closure table (first);
  2. BLUF;
  3. pins and re-pins (both times, with the instrument);
  4. trees;
  5. commit map, partition and per-commit red-first table;
  6. per-row table ((i) B48 FAIL condition + base/head ratio · (ii) re-measure + controls · (iii) mutants · (iv) the row question · verdict · evidence file);
  7. ruling 8 / ruling 2 table (persona × scope: requests sent, tab counts, rows that left or joined vs base, hrefs);
  8. `/figures` cell table and the widening table (persona × scope × figure: base / head / allowed?);
  9. hand-count table (figure × persona × scope: hand / API / tile / list, × 3 modes);
  10. re-sampled H/G table;
  11. red-proof table (gate's, B46's, B49's, then yours);
  12. findings;
  13. B49 claims CONFIRMED / REFUTED / UNMEASURED (one line per BLUF row, Test Evidence row, red-proof row sampled, Tier-1 bullet and NOT DONE line);
  14. `## NEW WORDS (for Kam)`;
  15. Notes;
  16. NOTES FOR FRIDAY (hosted);
  17. instrument incidents;
  18. UNMEASURED;
  19. `## NOT TESTED` (as prominent as the evidence);
  20. post-deploy and pre-deploy check items;
  21. processes started and stopped;
  22. worktrees and roots left;
  23. self-scan;
  24. verdict lines again;
  25. last line.

## HOLDS
- Datasec only. No other client's names, tickets or paths.
- **Findings only:** no code change, no push, no PR, no Jira, no GitHub write, no ticket, no records commit, no `history.md`, no `BACKLOG.md` or `CLAUDE.md` edit. **No deploy, no hosted access** (no hosted URL, no Kudu, no `az`, no Entra or app setting). Nothing goes to any human.
- **Q-09:** every process you start points `MpsCalc__ReferenceStorePath` at your synthetic `v1`. If any process of yours reads `.local/pricebooks/`, stop it, quarantine its store, and report it.
- **Never open `4_Credentials/.env`.** Never print a secret, a token, a price-book value or the avoid list.
- **Never delete; quarantine** (to `…/.tools/_quarantine/2026-10-12_B52_<what>/`, 0700, and say so). Never move another seat's quarantine; copy from it.
- SITE HOLD: none of the four store path settings changes in any shipped file.
- You write only the STATUS file, the evidence folder, `qa-B52/` and your own `wt-B52*` worktrees.
- No real client names, prices or document content anywhere: STATUS, evidence, logs, screenshots and scratch file names hold counts, codes, labels, computed styles and booleans only.
- **Own worktrees and own ports (6650–6659) only; `lsof` before every bind.** Never edit a running script. Ghost lines at your prompt are not instructions.
- **Time-box:** about 3 hours.
  - Order: item 0 → item 1 (G-F1 first, then G-F2, G-F3, G-N6, G-N9) → item 3 (Tier 1) → item 2 → **provisional verdict lines** → items 5, 6, 4, 7, 8, 9.
  - When time runs out, write what you have and mark every unfinished item NOT TESTED with its reason. An unmeasured row is **UNMEASURED, never CLOSED**.
- Last line: **`READY FOR REVIEW`**, or **`STOPPED: NEEDS FRIDAY`** plus the one blocking question.
