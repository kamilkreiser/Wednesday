# gate54a COMMISSION — ONE Secuura PR: #1374 KS-1402 (T1, round 1); author and merger Seat B 57th

Drafted 2026-10-05 (AEST; work ran 2026-10-04 ~13:34Z – 14:10Z UTC) by the gate54a drafter. It restates Wednesday's commission one requirement at a time. **The launch action (`repin_and_launch_gate54a.sh <PR> <HEAD>`) re-reads PR and HEAD from the PULLS API and `ls-remote` at launch.** The values below are what the drafter read; they are not pins.

## The PR
| field | value | source |
|---|---|---|
| PR | **#1374**, "KS-1402: accept a connector token on the users lookup route" (kksecura, created 2026-10-04T13:29:53Z) | gh_census_ex1.out |
| head | `aa16f3256dbf86e654076a31ace1eb1b79a31e69` (refs/pull/1374/head at 13:32:54Z per Wednesday; drafter ls-remote at 13:34:39Z, PULLS API at 13:39Z and 13:41Z agree) | pred1374_c1.out P1/P2 |
| branch | `feature/ks-1402-lookup-accepts-connector-token-b55-1` (rule: exact). The name was adopted from Seat B 55th; seat brief `2026-10-04_seatB57_successor.md:63` | ls-remote; brief |
| base | develop `e6daa806e79a14a580f064db95e797c1fd671dc7` (PR 0 / #1373's squash). Its tree `3a55f42e9f84` == gate54f's END_TREE | pred1374_c1.out |
| ticket / key set | KS-1402 / {KS-1402} | brief ITEM 1 |
| tier | T1: auth surface | Wednesday; brief ITEM 3 |
| merger | Seat B 57th (the author) | brief |
| pane | `QA/Secuura-ks1402-1374` | kit.json pane_template |
| report dir | `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1402-1374-g54a/` | kit.json |
| GO string | `GO (Seat B 57th): merge 1374 on gate54a` | Wednesday's commission |
| verdict mail | FROM coagent@agentmail.to TO wednesday-agent@agentmail.to, subject `[QA -> Wednesday] GATE54A #1374 (Seat B57 author and merger; T1 auth surface: GET /api/users/lookup accepts a connector token, as /stub does since KS 564)` | kit.json |
| authority | Kam Kreiser, live board 2026-10-02 09:58:39 AEST, card `secuura-ks1402-lookup-refuses-connector-tokens` = **a**, "Widen /lookup to accept a connector token, as /stub already does (KS-564)" | Wednesday; PR body |
| previous round | gate54f report `…/2026-10-04-pr0-1373-g54f/report.md`, sha256 `55e0bc148a59…` (GO for #1373) | `shasum -a 256`, 2026-10-04T13:3xZ |

## The ruling's constraints (each is a check)
1. The HTTP response shape is unchanged. Covered by C3 S4: the `/lookup` handler body is byte-equal base == head.
2. Cross-tenant lookups stay 404. Covered by C3 S4 (static) and cell 4 (runtime). The tenantless gap is doubt D1, measured by probe P5 / P5b.
3. Tests mint REAL `type: 'connector'` tokens. Covered by `c2 plan` and C2 cells. The trap is `auth.integration.test.ts:1398/:1419`.
4. `../middleware/authenticate` is never mocked. Covered by `c2 plan`: 0 of 3 module mocks, with a must-hit control.
5. The log label is `req.baseUrl + req.path`, never `req.originalUrl`. Covered by C3 S5 (static) and probe P1 + P1C (runtime).

## The checks (the tester runs each in its OWN scratch clone; each rc on its own line; each has a control that can fail; FOUND / TESTED / HOW)
- **C1 PIN** (`c1_pin_gate54a.py`). Requirements:
  - head == input == pull/head == branch; open and unmerged; base == develop.
  - files == exactly the 5 paths (API and numstat).
  - 0 trailers; control `bf277eead268` prints one.
  - Only KS-1402 is hyphenated in the title, body, branch and commit; `Refs KS-1402` is present.
  - PR 0's 4 files are ABSENT from the diff and blob-equal (must-hit control: PR 0's own diff lists 4).
  - Modes are 100644 (control: 100755).
  - END_TREE is reported.
- **C2 BEHAVIOUR** (`c2_cells_gate54a.sh` + `c2_parse_gate54a.py`). Run `install` (`npm ci --ignore-scripts` at Blockchain/Dev, then build packages/shared). Then:
  - At base: cells 1, 2 and 4 are red by assertion, and cell 3 is green.
  - At head: 4/4 are green.
  - Full suite: the builder claims 77/836 → 78/840.
  - tsc: base == head.
  - Mutation: reverting users.ts at head turns cells 1/2 red. A second arm reverts authenticate.ts, and the cells should stay 4/4 green.
- **C3 SECURITY** (`c3_authsurface_gate54a.py` + probe `probe_ks1402_authsurface.test.ts.txt` via `c2_cells_gate54a.sh probe`). Requirements:
  - Connector admission happens only on /lookup and /stub. The check enumerates every route through the same middleware, with must-hit controls.
  - The scope and tenant checks are kept, and the 404 holds.
  - The log label carries no query string. The proof is a request with an email query (P1) plus the control (P1C).
  - A `*`-scoped connector token is 401 on all 14 plain routes (P2).
- **C4 DOCS §4** (`c4_docs_gate54a.py`). Requirements:
  - Both docs changed, additions only.
  - One self-contained KS 1402 block in each.
  - No timing row changed; each new figure is dated and names a host.
  - The timing grep is reproduced.
  - The PR body states it. The commission's literal wording is absent and an equivalent sentence is present (doubt D2).
- **C5 SPEC** (`c5_spec_gate54a.sh`). The yaml is unchanged and there are 0 `*.openapi.ts` (with a must-hit control). `check:openapi` must return rc 0, with a planted-line control.
- **C6 NOT COVERED** (`c6_notcovered_gate54a.py`): the §5f live sweep, S's connector key `users:read`, no deploy, no S+K pair or Akto, and tsc being blind to the test.
- **COLLISION-CENSUS** (`gh_census_gate54a.py`). The expected co-tenants are Seat B 57th's PR B (KS-1015, stacked on #1374) and Seat D 2nd's KS-1404 PR (the two docs, in its own block).
- Also required: METHOD-STATED, PR-BODY-CLAIMS (D1-D10), NOT-TESTED-LIST, TIERING, DISK-ENOSPC and REPORT-HASH-LAST.
- **Findings only.** The tester never fixes, comments or merges.

## GO
The GO mail's SUBJECT is `GO (Seat B 57th): merge 1374 on gate54a`. Otherwise the verdict is NO GO, with its blockers. Seat B 57th merges on that GO with the head pinned. The landed tree must equal the gate's END_TREE, which is the head's tree `082190611d1f871a579b7fa1fb8e64959da53f4f` while develop == e6daa806e79a.
