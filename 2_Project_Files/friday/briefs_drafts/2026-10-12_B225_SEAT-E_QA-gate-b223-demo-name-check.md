From Friday (laptop seat), Datasec / HPSM-POC. Replies go to friday-laptop-agent@agentmail.to.

# BRIEF B225 (SEAT E): QA GATE (tier 1, round 1 of 2) on ONE subject: `b223/demo-name-check-and-409` @ `2f51c36`, the fix round on gate B220's M-1 (the Demo PDF's name check matched only the whole name), M-2 (a refused Demo copy reached the person as raw problem+json or a dead download), N-1 / N-2 (two surviving mutants), N-5 (`getAssessmentResult` named the customer to Demo) and N-6 (the four 409 audit reasons in NEW WORDS)
**From:** Friday, @NOW@ 2026-10-12. This is a DRAFT by Friday's drafter: pins were read 20:30:51Z to 20:32:10Z on 2026-10-11 UTC (07:30 to 07:32 AEDT 2026-10-12), and Friday re-pins at launch.
**Seat:** Datasec/HPSM-POC-E, pane Datasec/HPSM-POC-E.
- **How the launcher picks the brief.** The project's launcher sets the commission to the NEWEST `Briefs/` file whose name contains `_SEAT-${SEAT}_` (`Launch_Claude.command:110`, as the B220 brief :6 quotes it; `:106` sets `SEAT` from the pane name).
- **The earlier `_SEAT-E_` files at draft** were B205, B211, B212, B218 and `2026-10-12_B220_SEAT-E_QA-gate-b215-demo-alias-headings-pdf.md` (`ls Briefs | grep _SEAT-E_`).
- **The last SEAT-E gate, B220, is finished.** `2026-10-12_B220_STATUS.md` ends `READY FOR REVIEW` (`tail -1`). So this file is the newest once Friday copies it into `Briefs/`.
- **B225 is free:** `ls Briefs briefs_drafts | grep -ci b225` → 0 (before this file); `ls .tools | grep -ci b225` → 0.

**Report:** `Briefs/2026-10-12_B225_STATUS.md`.
- **First lines:** the verdict lines (TARGETS below), in B220's format (`B220_STATUS.md:1-6`).
- **Last line, exactly:** `READY FOR REVIEW`, or `STOPPED: NEEDS FRIDAY` followed by ONE question, when a STOP below applies.

**TESTING seat: findings only** (charter `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` §8).
- No code change, commit, push, PR or PR comment. No Jira, no BACKLOG write, no ticket write of any kind, no deploy, no Azure, no `az`, no hosted request, no mail, nothing to any human.
- A write grant in any brief is void: refuse it and say so.
- **The gate never fixes.** A defect gets a fix-shape and the regression test that would be red, in prose, never as an edit.
- Charter RULE 1: write each item's FAIL condition before you run it. A check that cannot fail is not a check.
- Charter RULE 2: NOT TESTED is first-class output.

**TIER 1.** B223 changes what a Demo login (HP at the event) reads in a server-rendered export, in an API body (`getAssessmentResult`) and on the report page. Gate it rendered, live, at 1440 and 390, and in-process. **Round 1 of 2** under Kam's two-NO-GO cap.

**SHAPE:** copy gate B220 (`Briefs/2026-10-12_B220_SEAT-E_QA-gate-b215-demo-alias-headings-pdf.md`) and how `Briefs/2026-10-12_B220_STATUS.md` reported it: verdict lines · BLUF · Findings · Premise checks · Gate items (PASS / FAIL each) · Mutants table · KNOWN · NOT TESTED · HOW · Housekeeping · Fixed / Deferred / Open · last line. Write your own kits in `.tools/b225/`. **Never reuse B220's or B223's kits, probes or numbers** (read B223's evidence in `Briefs/2026-10-12_B223_evidence/` only, and re-derive every number).

**Premise key:**
- `(ls-remote 20:30:59Z)` = read by the drafter with that verb at that time (UTC, 2026-10-11).
- `(git <verb>)` = a read verb on `2_Project_Files`' object store, with `--no-optional-locks`.
- `(scratch)` = run in the drafter's own `git clone --shared` in its session scratchpad (no write in `2_Project_Files`).
- `(read: file:line)` = quoted from that file at `2f51c36` unless the line says otherwise.
- **UNMEASURED** = the drafter did not establish it; the line says what closes it.

Re-check every premise. A wrong one is a finding. A moved pin is a STOP unless a rule below covers it.

## AUTHORITY (verbatim, as the B223 brief relays them; re-read there)
- **Standing ruling** `hpsmpoc-customer-names-alias-1011` → **(a) "Keep names; alias wherever data leaves the partner"**: *"ORG-nnnnn on anything HP or an export sees."* (B223 brief :12, relaying B215 brief :16).
- **Kam's B215 card** `hpsmpoc-demo-names-beyond-the-frame-1011`, ruled (b): *"Alias the headings AND the executive PDF for Demo (recommended)"*, detail *"… the PDF a Demo user downloads names the customer only by alias, in its pages and its file name."* (B223 brief :12; B220 brief :41-44).
- **The Demo rule (B208, unchanged):** the SERVER's caller holds Demo (Demo, Partner+Demo, Admin+Demo) → the alias; no Demo (Partner, Admin, Consultant) → the name.
- **The PDF's shape** is Friday's ADDENDUM-1 to B215 (a), "render on demand, then verify" (`Briefs/2026-10-11_B215_SEAT-A_ADDENDUM-1_q-b215-1-pdf-shape.md:6`): no migration, no write to the report store, no-Demo callers get the stored bytes.
- **Friday's order for B223** (B223 brief :11, :14): a fix round on B220's "Open, for Friday" (`B220_STATUS.md:209`): M-1, M-2, N-1, N-2, N-5, N-6. **Not in the round:** N-3, N-4, S-N1, S-N2, the readiness PDF, rows 9 / 10. **M-1 is built Demo-side only (widened gate 2, fail closed); the narrative-edit rule is OUT, Kam's to rule** (B220 :44-45; B223 STATUS :44 carries the flag line).
- **The oracle per item** is B220's verbatim finding text and fix-shape (`B220_STATUS.md:40-59`) plus B223 brief THE WORK 2-7 (:72-92).

## TARGETS (re-read with `git ls-remote origin` in `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/2_Project_Files` at the start, mid-gate and before the verdict; name the instrument and time on each)
| What | Value | Instrument |
|---|---|---|
| **Subject head:** `b223/demo-name-check-and-409` | `2f51c365796bb593a00dab6e7261f864eb7883ca`, tree `338e6a93735164ebbe25bf185556781bda291755` | ls-remote 20:30:59Z (= B223 STATUS :345, its last line; = the pin Friday read 07:3x AEDT); git rev-parse `^{tree}` |
| **Base = main** | `598a91ae035f28100e04fca6d19bcd19bdedcc8d`, tree `bf26f63bb191233d09766941b9148d3797837869` (= B220's tested three-way tree, `B220_STATUS.md:5`) | ls-remote 20:30:51Z and 20:30:59Z; git rev-parse; `merge-base 598a91a 2f51c36` = `598a91a` |
| Subject commits (3, linear) | `2a476ad` (API: M-1, N-5, N-1, N-2; tree `58cf3b81…`) · `8ba1add` (web: M-2; tree `b71f4d84…`) · `2f51c36` (`Result`'s doc comment) | git log --format='%H %P %s' `598a91a..2f51c36` |
| Subject files (9, +1,107 / −12) | `AssessmentEndpoints.cs` +18/−2 · `ReportingEndpoints.cs` +147/−6 · `B223DemoNameCheckTests.cs` +198 · `B223NameFormsTests.cs` +109 · `B223ResultAliasTests.cs` +130 · `B223SeededCustomersOpenByAliasTests.cs` +101 · `web/e2e/report-demo-refused-live-api.spec.ts` +108 · `ServiceReport.demo.test.tsx` +215 · `ServiceReport.tsx` +81/−4 | git diff --numstat `598a91a 2f51c36` |
| Objects present | `2f51c36`, `598a91a` → `commit` | git cat-file -t |
| PRs | none for `2f51c36`. The highest is `refs/pull/142/head` = `98158df` (B219) | ls-remote `refs/pull/14*` 20:30:59Z |
| `.tools/.git-lock` | absent (free; only `.git-lock-last-owner-*` markers) | `ls -a .tools` 20:32Z |

**NOT the gate's subject: B224** (Seat D, live in parallel). `refs/heads/b224/slow-first-login-deterministic` = `23eb29e8edbc98d60110ba6714b6223bd7297206` (ls-remote 20:30:59Z; 1 commit on `598a91a`, "B224 Row 1: …"), and **no `Briefs/2026-10-12_B224_STATUS.md` exists** (`ls`, 20:32Z), so it is not READY FOR GATE. Its files, `api/tests/HpsmPoc.Api.Tests/Assessment/HostedDemoRobustnessTests.cs` (class `HostedDemoSlowFirstLoginTests`) and `api/tests/HpsmPoc.Api.Tests/Support/StallingTcpProxy.cs` (git diff --name-only `598a91a 23eb29e`), are not graded here; B223 touches neither (0 overlap). Its ports (6970–6979; `b224-mssql` is up on 6970), worktrees `.tools/wt-b224*`, kit `.tools/b224/` and containers `b224-*` are never touched. **If B224 writes `READY FOR GATE` before this gate launches, Friday may add it as Subject 2 by ADDENDUM** (tier 2, through code plus targeted runs, B220's Subject 2 pattern); without that addendum it is out of scope. If a flake in `HostedDemoSlowFirstLoginTests` turns up in your API run, record it as KNOWN (B221 / B224's class), re-run it alone, never skip it.

**The drafter's merge trees (scratch; re-derive in YOUR scratch clone against main as it is at verdict time):**
- `merge-tree --write-tree 598a91a 2f51c36` → `338e6a93735164ebbe25bf185556781bda291755`, rc 0, which equals the head's own tree (main is the base: a fast-forward).
- For an ADDENDUM only: `merge-tree --write-tree 2f51c36 23eb29e` → `9d94cdf2fbb59d5e608c954cf5a63404828c0b33`, rc 0; `598a91a + 23eb29e` → `014f4bf4caeb92d620c7f78cbf59c6f49aa8e110`, rc 0. B224's head may move; these are not pins.

**Rules:**
- **The head moved** → STOP, and say to what.
- **Main moved** → read `git diff --name-only 598a91a <new>`. If any path overlaps B223's 9, or falls under `api/src/HpsmPoc.Modules.Assessment/Endpoints/**`, `api/src/HpsmPoc.Modules.Reporting/**`, `web/src/components/{customer,shell,screens}/**`, `web/src/server/**`, `web/e2e/**`, `api/tests/HpsmPoc.Api.Tests/Assessment/B2*` or the contract copies: STOP and say which. Otherwise re-derive the merge tree against the new main, build and test it once (vitest full, typecheck, lint, build, contract-drift, the API suite), and name it in the MERGE line. (A B224 merge to main touches only test files outside these paths: re-derive, do not stop.)
- **A conflict** → STOP, and say where.

**Verdict lines (the first lines of STATUS):**
```
B223 2f51c36: GO | GO WITH NOTES | NO GO
MERGE <main>+2f51c36: GO | GO WITH NOTES | NO GO | STOP   (tree, rc)
Round 1 of 2.
```

## GIT DISCIPLINE
- **In `2_Project_Files` itself, READ verbs only:** `ls-remote`, `log`, `show`, `diff`, `cat-file`, `ls-tree`, `rev-parse`, `rev-list`, `merge-base`, `grep`, and `git --no-optional-locks status`, always with `--no-optional-locks`. No fetch, checkout, switch, branch, merge-tree, commit-tree, worktree add/prune or gc there.
- **Everything else goes in a `git clone --shared`** or an alternates bare repo under `.tools/b225/`.
- **Your detached trees** are made under a copy of `.tools/b220/lock.sh` → `.tools/b225/lock.sh` (sha256 of the copy = the original's), on the shared `.tools/.git-lock`. Never remove another seat's lock.
  - `.tools/wt-B225-head` (`2f51c36`) · `.tools/wt-B225-base` (`598a91a`) · `.tools/wt-B225-mut` (`2f51c36`, mutants).
- **Do not use or touch** `.tools/wt-b223*`, `.tools/b223/`, `.tools/wt-B220-*`, `.tools/b220/` (beyond copying `lock.sh`), `.tools/wt-b224*`, `.tools/b224/`, or any other seat's tree, kit or container (`b223-azurite` and `b220-azurite` stay stopped; do not start or reuse them).
- Every SHA you write is one you read, with its instrument inline.

## PARTITION / PORTS: 6981–6990, yours only
- **The drafter's port check, 20:32Z:**
  - `lsof -nP -iTCP -sTCP:LISTEN` → listeners on 5000, 6970, 7000, 7768 and ephemeral ports (42050, 49152–49228, 57621, 59869) only; **none in 6980–6999**.
  - `lsof -nP -iTCP:6980-6999` → 0 lines.
  - `docker ps -a` port bindings in 69xx: only `b224-mssql` 127.0.0.1:6970 (B224, live).
  - `grep -ohE '\b69[89][0-9]\b'` over every HPSM-POC `Briefs/*.md` and Friday's `briefs_drafts/*.md` → **6980 ×2** (B221 STATUS :155, a `--rm` SQL Server dry-run container, stopped after), **6998 ×5, 6999 ×36**; nothing in 6981–6997. So 6980, 6998 and 6999 are avoided.
- **Never yours:** 6970–6979 (B224, live), 6960–6969 (B223), 6950–6959 (B220), 6860–6949, 6980, 6998, 6999, 6540–6549, 6730–6739, 6750–6799.
- **Plan:**

  | Port | Use |
  |---|---|
  | 6981 | head web, proxy mode (showcase shape) → 6983 |
  | 6982 | base web, proxy mode → 6984 |
  | 6983 | API at `2f51c36`, Development sign-in, one role set per arm, restarted per arm (B220 method), `Showcase__Enabled=true` as `scripts/showcase.sh` sets it |
  | 6984 | API at `598a91a`, the same |
  | 6985 | head web, mock build (offline demo: confirms B223 F-5, no `/reports` route) |
  | 6986 / 6987 | hosted standalone + Entra stub (`E2E_HOSTED_PORT` / `E2E_STUB_PORT`) |
  | 6988 | Azurite `b225-azurite`: new, CI digest `mcr.microsoft.com/azure-storage/azurite:3.37.0@sha256:830430c1da1a2d537e08f3e6764dd1f5ae00cf0346bcaf625b968ec3f0971fd5` (read: `.github/workflows/ci.yml:43` at `2f51c36`); key in `4_Credentials/b225-azurite.env`, mode 600, read by name only; stopped, not removed, at the end |
  | 6989 | mutant web / Playwright's own web |
  | 6990 | spare (a second API arm if one is needed) |

- **Re-check with `lsof` before every bind**, log the checks in `.tools/b225/run/lsof-checks.txt` and in STATUS.

## BUILDER'S CLAIMS (read whole first; trust no count in them)
- Brief `Briefs/2026-10-12_B223_SEAT-A_b215-followups-demo-name-check.md` (THE ITEMS table :16-30, THE WORK 1-10, the partition :94-97).
- STATUS `Briefs/2026-10-12_B223_STATUS.md`: BLUF 1-10, FOUND (M-1 table c1-c14, the false-refusal baseline, F-1 to F-6), TESTED (red-first, 49 mutants), HOW 1-6, NOT TESTED, NEW WORDS, NEW LOOK, Records. Evidence `Briefs/2026-10-12_B223_evidence/` (`found/`, `redfirst/`, `suites/`, `shots/newlook-{before,after}/`, `mutants-tip.txt`, `n5-before-after-live.tsv`, `demo-copy-timing.txt`, `lsof-checks.txt`, `push-*.txt`, `WHERE.txt`).
- The gate it answers: `Briefs/2026-10-12_B220_STATUS.md` (M-1 :40-46, M-2 :47-53, N-1 :54, N-2 :55, N-5 :58, N-6 :59; mutant table :128-154).

### The drafter's reading of B223's STATUS (each is for the gate to confirm or refute; none is a finding until measured)
1. **A count attributed to the wrong file.** BLUF 3 (:25) says "`ServiceReport.demo.test.tsx`: 10 red / 4 green at base (green: the 3 withheld tests and the no-Demo DOM pin), 14/14 green". The 3 withheld tests are in `ServiceReport.withheld.test.tsx`: `demo.test.tsx` holds 11 `it(`/`test(` and `withheld.test.tsx` 3 (git show `2f51c36:<file> | grep -cE '^\s*(it|test)\('`). TESTED (:107) states it correctly as the two files together. Confirm; a Note if it holds.
2. **"Words the report prints by itself" includes person-typed text other than narratives.** HOW 2 (:211-214) and BLUF 2 (:17) present the exclusion list as the report's own words. In code it is every string of `Model(shown, withEditedText: false)` (read: `ReportingEndpoints.cs:454-460`, `:466-468`), which drops only narratives whose `Status == "edited"`. It still holds partner-typed answers (`ReportModelBuilder.cs:206` prints `AnswerText`), profile values, and any other free text the model carries. **Hypothesis (UNMEASURED):** a partner who types "Bettong Hollow" into a printed free-text answer makes both words "own", so the token rule and the bracket-less needle (added only `if (words.Length > 1 && words.Any(Telling))`, `:562`) both fall away, and the PDF prints "Bettong Hollow" to Demo with 200. That is M-1's class through a door B223 did not close. Item 1 (b) tests it.
3. **An approved, unedited AI narrative also counts as "own".** `withEditedText: false` keeps `Status == "approved"` narratives (`NarrativeReview.cs:32`, `:37`, `:72`). ADR-R05 says AI text keeps "the organisation" (B223 F-2 cites `Reporting/README.md:68`), but nothing enforces it at approve time. UNMEASURED: whether approved AI text can hold a name word. Item 1 (b) reads it.
4. **"No-Demo callers keep the same links" holds only once the shell knows the caller.** `asksFirst = shownAs.kind !== "name"` (`ServiceReport.tsx`, diff `598a91a..2f51c36`), so a Partner clicking while the shell's answer is `"pending"` takes the fetch-and-blob path, not the plain link. B223 BLUF 3 (:23) says so ("or one the shell does not know yet"); the gate measures whether that pending window is reachable by a person and what a Partner then gets (bytes = stored? file name?). Item 3.
5. **Red-first for the e2e is half.** BLUF 3 (:26) / TESTED (:108): at base 1 failed and 1 did not run (serial), so the 390 case was never red at base. Confirm and record.
6. **Disclosed by B223, re-measure, do not re-grade:** the one console line per refusal (BLUF 3 :28); middle-click / context-menu bypass (HOW 3 :231); Safari / Firefox blob behaviour (NOT TESTED :256); F-3 (the typed name through `listNarratives`, the Narrative screen and `/result`'s narrative text); F-4 (the result's scoring-time name). The drafter found **no contradiction** between B223's line anchors and the tip: `NoAliasWords` `:425`, the four reasons `:449`, `:463`, `:468`, `:472`, the 409 `:480`, `GenericNameWords` `:524`, `DemoCopyNamesCustomerInAnyForm` `:544`, `ReportWords` `:569` (git grep `2f51c36`); the N-5 byte deltas match the name lengths (18,609 − 18,591 = 18 = len("Kookaburra Council (sample)") − len("ORG-00005"); 15,709 − 15,688 = 21 for "Banksia Manufacturing (sample)").

## THE GATE MUST, INDEPENDENTLY, AT `2f51c36`

### 1. M-1: no form of the name reaches ANY Demo surface (PDF bytes and text, rendered page, `getAssessmentResult`, ETag / caching)
Through code first: `DemoCopyNamesCustomerInAnyForm` `:544-565`, `Folded`, `Without`, `DrawnFormFound`, `BracketSuffix`, `ReportWords` from `:569`, `Folded` from `:592`, `Without` from `:615`, `GenericNameWords` from `:524` (read at `2f51c36`), against B220 :45's fix-shape. Then, with your OWN in-process probe (one fresh API per case: customer, edit, issue, download as Demo and as Partner) and a PDF extractor of your own (`pdftotext` or PdfPig) plus a raw string scan of the file (Info dict, outlines, inflated streams, UTF-16BE, as B220 item 3):
- **(a) B220's variants, re-made:** "Bettong Hollow runs 40 printers…", "Bettong Hollow(SYNTHETIC) runs…", "東京 Printing (SYNTHETIC)" typed, the exact name and upper case (controls: 409 at base already), and B223's c6-c14. **Base control:** each of the first three is 200 with the name in the copy at base; if base does not leak it, the case is blind: say so.
- **(b) The gate's own adversarial variants** (each with its FAIL condition written first: "Demo gets 200 and the copy, by your extractor or raw scan, holds a readable form of the name"):
  - **Unicode lookalikes:** Cyrillic / Greek homoglyphs ("Веttong Ноllow", "Bettοng" with Greek omicron), full-width Latin, mathematical alphanumerics (NFKC folds these; homoglyphs it does not).
  - **Whitespace and invisibles:** NBSP, U+2009, U+3000 between words; ZWSP U+200B, ZWNJ, ZWJ, U+2060, soft hyphen U+00AD **inside** a word ("Bett<U+200B>ong"). `Folded` turns any non-letter into a blank (read: `Folded` from `:592`), so "Bett<U+200B>ong" becomes "bett ong": test whether the renderer prints it as "Bettong" (a person reads the name) while the check sees two short words.
  - **Split across lines and hyphenation:** a long edit that makes the renderer wrap inside the name; an explicit "Bet-\ntong"; a name at a page break.
  - **Possessives and inflections:** "Bettong's", "Bettongs'", "Bettongs", "Hollow-based", "Bettong-Hollow".
  - **Diacritics dropped / added:** customer "Ōtautahi Café (SYNTHETIC)" typed "Otautahi Cafe"; customer "Cafe Zurich" typed "Café Zürich".
  - **Dense scripts:** a CJK name inside a CJK run with no blanks ("東京の印刷"), and a name the font CAN draw (Latin) beside CJK.
  - **Short names:** words under 4 letters ("Ace IT (sample)" typed "Ace IT"), a single-word name, a name that is all generic words ("Health Services Group (sample)"), a name made only of words the report prints (B223's own residual: "Security Assessment (sample)").
  - **Item 2 of the drafter's reading:** the name typed into a printed free-text answer / profile value / risk-acceptance or override reason (whatever the model prints; find each by reading `ReportModelBuilder.cs`), alone and together with a narrative edit.
  - **Item 3:** an approved AI narrative carrying a name word (if reachable through the API's test seams only; no live AI call).
  - **The title and other metadata:** every variant also checked in Title, Subject, Keywords, outlines.
- **(c) The other Demo surfaces, same customers:** `getAssessmentResult` body for each variant (B223 leaves narrative text unrewritten by design, F-3: record, KNOWN), `listNarratives` (F-3, KNOWN), the rendered report page and Narrative screen at 1440 and 390 for Demo, `Content-Disposition` (`filename` and `filename*`).
- **(d) ETag / caching (B223 brief :82 raised it):** the ETag is `assessment.ConcurrencyStamp` for both bodies (`Preconditions.SetETag`, read: `AssessmentEndpoints.cs:508` at `2f51c36`; `:507` at base). In ONE browser context: Partner (no Demo) reads `/result` through the BFF, then the role becomes Demo (showcase arm restart; mock sign-out / sign-in), then the same URL by fetch, by navigation and by back / forward, with and without `If-None-Match`. Also a direct `If-None-Match` to the API and through the BFF (`bff.ts` forwards `if-none-match`, B220 :99). **FAIL:** any Demo-holding read that receives the named body or a 304 that lets a cached named body stand. Confirm `Cache-Control: no-store` on every answer at both hops.
- **Severity guide:** a variant a person would plausibly type that serves a readable name to Demo is a finding against M-1 (Minor at least; Major if it needs no special character, e.g. item 2's free-text answer). An exotic one (homoglyphs) is a Note for Friday under the ruled design.

### 2. No false refusal (the N-3 family)
- Every seeded showcase customer (each listed customer and the partner-self record) and the hosted seed's names (same `ShowcaseSeeder`, read the source): the seeded report and a fresh report each open by alias for Demo (200), 0 pages naming the customer. **FAIL:** any 409.
- **The "telling word" rule must not refuse ordinary report words.** Build a list of the words the seeded report prints (your extractor) and synthesise customers whose names use them in their distinctive position ("Fleet Printing Co", "Managed Print Partners", "Council Security Services", "Toner Logistics"), plus names whose words appear in ordinary narrative text a partner may write ("Wattle Health (sample)" with an edit about "wattle trees", B223 HOW 2 :216). Record each as 200 / 409 and whether the 409 is a leak prevented or a false refusal. **N-3 itself is not in this round:** record its family as KNOWN with counts, base → head.
- Confirm the exclusion of generic words does not let a name through that is distinctive only because of a generic word (e.g. "Partners Group (sample)").

### 3. No-Demo callers are byte-identical to base
- PDF: Partner, Admin, Consultant → stored bytes, sha256 = the row's, same file name and `Digest`, as base (6983 vs 6984, same seed copy).
- `getAssessmentResult`, `getCustomer`, `listCustomers`, `listNarratives`: sha256 base = head for the three no-Demo arms (B223 BLUF 6 :38-41).
- Report-step DOM: the two anchors' `outerHTML` equal base vs head once the shell knows the caller; a click is not prevented and makes no fetch. **And the pending window** (drafter's reading item 4): hold `getMe` / the summary (B220 item 2's holds) and click as Partner; record what happens and whether a person can reach it. **FAIL:** a no-Demo caller, once known, gets anything other than base's link and bytes.
- `ServiceReport.withheld.test.tsx` green unchanged (`git diff --quiet 598a91a 2f51c36 -- <it>`).

### 4. M-2's UI in a real browser, 1440 and 390
- Showcase shape, service Partner+Demo, Demo sign-in, the seeded customer renamed after issue: "Open the PDF" and "Download PDF" each → the Alert "This report changed after it was issued" with the service's detail verbatim (`ReportingEndpoints.cs:480-482`), "Make a new copy" beside (1440) / below (390) it, the links gone, no raw JSON tab left open, no cancelled download. Then "Make a new copy" → a NEW report → Demo opens it by alias (blob tab or saved file named `executive-report-org-nnnnn-<date>.pdf`).
- A 200 path: "Open the PDF" opens the alias copy in the tab opened in the click (pop-up rule); "Download PDF" saves with the service's file name.
- A 500 / 504 / network failure (route the BFF): "The PDF could not be opened" + `describeFailure` words, never raw JSON.
- Keyboard (Enter on the link), screen reader role (`live="alert"`), and the "Preparing the PDF…" status while the copy is drawn.
- Middle-click and "open in new tab" (B223 HOW 3 :231): measure, record as NOT COVERED by B223, KNOWN.
- Console errors per page base vs head (B223's disclosed 409 resource line is the only new one: confirm and count); the timed journey's "no console errors" must stay green.
- Screenshots in evidence, captioned with the caller as the SERVICE saw it. The offline demo has no `/reports` route (B223 F-5): confirm with `git grep -n reports web/src/server/mock/api.ts` at `2f51c36`.

### 5. N-1, N-2 and mutants
- **Re-run at least 6 of B223's mutants** (`evidence/mutants-tip.txt`; STATUS :115-164), including g2, ord, wn, tk, dr, ow, ed and r3; give red counts against B223's.
- **Add at least 8 of your own**, for example:
  - `Folded` keeping zero-width / format characters as letters (or dropping them silently);
  - the bracket-less needle added only when every word is telling;
  - the dense-script rule removed (CJK 2-letter tokens);
  - `Without` removing the alias before folding instead of after;
  - `ReportWords` built WITH the edited narratives;
  - `ReportWords` reflection stopped at depth 1;
  - `ResultForDemo` replacing `customer.name` only when it differs from the alias, or keyed on a client header;
  - the Demo ETag differing from the no-Demo ETag (and its effect on the override's If-Match, B223 HOW 4 :237);
  - M-2: `asksFirst` from a client flag; the 409 detail rendered as raw text; the tab not closed on refusal; `fileNameOf` reading `filename*` wrongly.
- **Runner** as B220 (exact anchors, count 1, restore by a fresh write, sha256 = the head blob AND `git diff --quiet`, a new mtime; controls green). Any SURVIVOR is a finding with a fix-shape and the test that would be red.
- Confirm N-1 and N-2's tests are red under g2 and ord respectively and green at base (they pin existing behaviour).

### 6. N-5 through code and live
- `Result` decides Demo only by `CallerAccess.Get(http).Is(Roles.Demo)` (read: `AssessmentEndpoints.cs:500-518`, the Demo test `:515`); `ResultForDemo` from `:522` changes `customer.name` only; keys, types and every other value equal (JSON-diff Demo body vs no-Demo body: exactly one path differs). Pre-key → `NoAliasWords`. A client-sent Demo claim for a Partner changes nothing (proxy and in-process). A Demo caller who cannot see the assessment is refused and learns no name.
- Every other path in the result body that could name the customer (`customer.id` is `CUST-<guid>`, `ShowcaseSeeder.cs:494`: confirm; profile values; evidence descriptions; narratives): list each with base and head for Demo.
- The web's consumers of `/result` (B223 F-1: `client.ts:127`, `customer/api.ts:109`): Demo's results page renders the same as base apart from nothing; the override (Partner+Demo, If-Match) still succeeds.

### 7. NEW WORDS complete (N-6)
- `git grep` every string literal added in `598a91a..2f51c36` (web and API) and compare with B223's NEW WORDS table (:294-308). Any user-visible string missing is a Note.
- The four reasons verbatim at their tip lines (`:449`, `:463`, `:472`, `:468`), marked internal audit (Partner / Admin via `getAssessmentAudit`, Demo 403: measure the 403).
- Where each NEW word is seen by a person, with a screenshot: "The PDF could not be opened", "Preparing the PDF…", the `executive-report.pdf` fallback (say whether it is reachable), and the 409 title + detail now on screen.

### 8. Suites (head, once)
- vitest full (`--maxWorkers=4`; B223: 1,661 / 1,661, 172 files), typecheck, lint, build (warnings line-identical to base), contract-drift (B223: 7 / 7).
- Playwright desktop + tablet: customer-headings-alias, customer-frame-alias, metrics-dashboard, attribution-preview, a11y, responsive, nav-dead-ends, plus `report-demo-refused-live-api.spec.ts` with `E2E_LIVE_API` (B223: 48 + 2); the timed journey `E2E_TIMED=only`; the hosted project (6986 / 6987).
- The API suite once on SQLite with `b225-azurite` (all 5 projects, 0 skipped; B223: 2,670).
- gitleaks `--log-opts=598a91a..2f51c36`; a raw scan of the added lines with Python (B223: 1,107 lines, 0 invisible; □ ×2, — ×13, … ×3, · ×1, full-width brackets in the suffix regex): re-derive.
- Timing: the Demo copy cold and warm at base and head (B223: warm 130–170 ms base, 180–320 ms tip under load ≈20). It now builds an extra model; estimate the hosted effect against the BFF's 30 s `/content` budget (`bff.ts:171-175`) from B220 item 3's method. Hosted UNMEASURED by HOLD.

## KNOWN (Kam's or Friday's to rule; confirm and record, do not grade)
- M-1's other shape (the narrative-edit rule) and F-3 (the typed name through `listNarratives`, the Narrative screen and `/result` narrative text): Kam's.
- B223's PROPOSED contract sentence for `getAssessmentResult` (HOW 4 :240), the PROPOSED `content-status` route (HOW 3 :230) and `InternalsVisibleTo` (HOW 2 :205).
- N-3's family (fail-closed refusals), N-4, S-N1, S-N2, the readiness PDF, rows 9 / 10: not in this round.
- The Dependabot high on main (B223 Records :320): pre-existing.
- Known flakes: HPSMPOC-247 `ImportRobustnessTests.R2_2`; `HostedDemoSlowFirstLoginTests` (B224's subject). Re-run alone, never skip.

## FINDINGS FORMAT
- Each finding: severity (Blocker / Major / Minor / Note), `file:line` at `2f51c36`, the instrument, the FAIL condition it met, a prose fix-shape, the regression test that would be red. Severity yes, priority no (charter §8). One defect per finding (charter §9).
- **A route that serves a readable form of the customer's name to a Demo-holding caller, where B223 claims it is closed, is at least Major.**

## HOLDS
- No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool — Claude seats, subagents, the product's model, Ornith or the Spark — without HP's written approval (signed SOW §4.1.4(c)). Every PDF here is the product's own synthetic report. Do not open `HP Reporting and Docs/` or the SOW file in the project root.
- Datasec only; no other client's names, tickets or paths.
- Findings only: no code, commit, push, PR, ticket, BACKLOG or Jira write. Never delete: quarantine. Never print a secret.
- No deploy, no Azure, no setting change, no hosted request; nothing to HP or any human. No real customer export is used or requested; fixtures are synthetic. No live AI call.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY.
- No force-push, no branch delete, no history rewrite, no ref write in `2_Project_Files`.
- B223's (Seat A) and B224's (Seat D) worktrees, kits, ports and containers are never touched.
- Kam's two-NO-GO cap: this is round 1 of 2.
- *(Time-box)* about 3 h of gate time. Anything not reached is NOT TESTED with the reason, never a silent PASS.

## UNMEASURED at draft (each closes as stated)
- **Whether the Datasec/HPSM-POC-E pane is free to launch, and whether B224 is READY FOR GATE by then:** Friday, at launch.
- **Whether main or the head moves before your verdict:** your `ls-remote` at start, mid-gate and end, then the TARGETS rules.
- **Whether person-typed non-narrative text (answers, profile, reasons) whitelists a name word** (drafter's reading item 2): item 1 (b).
- **Whether the renderer wraps or hyphenates inside a name, and how PdfPig joins it:** item 1 (b).
- **Whether a pending-shell click by a no-Demo caller is reachable by a person:** item 3.
- **The hosted Demo copy's time with the extra model build:** not measurable here (HOLD); item 8 estimate.
- **Whether ports 6981–6990 stay free:** your `lsof` at each bind.
