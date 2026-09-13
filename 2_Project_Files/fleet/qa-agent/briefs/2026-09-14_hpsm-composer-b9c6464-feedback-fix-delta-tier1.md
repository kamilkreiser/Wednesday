# QA GATE, TIER 1: Datasec/HPSM Policy Composer - the FEEDBACK credential-scan fix, DELTA d0466da..b9c6464 (feature-scoped delta, round 1) — LOCAL ONLY

**Why TIER 1.** This delta is a security surface: credential storage through feedback submission. It is headed for a live deploy.
- `b9c6464` is the ACCEPTED live target of the feedback upgrade.
- The live GO needs this gate's verdict with no Blocker or Major (`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-14_hpsm-s45-answer-b9c6464-received-delta-gate.md` L1-6).
- Rate severity honestly. Never rate it to fit that bar.

**The ruling this gate measures against (the oracle).** Tuesday, 14:34:04Z, ruling (a), `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-14_hpsm-s45-answer-g45-defect-retarget.md`:
- **L14:** *"credential-shaped free text fails closed with 422"*. Measured as all of:
  - 422 `SECRET_VALUE_ENTERED_IN_CLOUD`;
  - the value is not echoed;
  - nothing is stored: no row, no audit event, no object.
- **L15:** the fix's accepted SHAPE. Scan the decoded path as `page_url` as well as the stored one, and leave the stored value unchanged.
- **L16, verbatim:** *"Whether `decodedPagePath()` catches every encoded form, on every feedback field and every path (JSON, multipart, file name), is the delta gate's question, not Tuesday's."* Tuesday has not read the diff.
- **Its origin:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/2026-09-10_policy-composer_ARCHITECTURE.md` §2.5 L614-617.
  - L616 said "redacted + warning". The product refuses with 422 instead. That deviation is declared at BACKLOG.md L1007 (a), and L14 above rules it in force.
  - L617 is the oracle for logs: *"No secret in DB, logs, analytics or outputs."*
- **No over-refusal.** A fix that refuses ordinary feedback is a finding (§2a).

**Gate commission.** Tuesday, 14:54:25Z, the delta-gate answer above:
- L1: the target is accepted.
- L11: the backslash side note "goes to the delta gate to size".
- L15: ports **21610-21729** for this gate.
- HANDOVER-S45 L54 and the retarget answer L23 name other ports for this gate. L15 of the 14:54:25Z answer supersedes both.

**Head:** `b9c6464f73e8d7199152a1f9b0d04b9cd8894b0a`, local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer`. NOT pushed, and NOT live on any stack.
- **Delta base:** `d0466daaa7f2ae30b2da8f8fd537e95250da0aa8`, the head's first parent. `d0466da` must never go live (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/5_Project_History/HANDOVER-S45_seat-hpsm-3562.md` L23).
- **Delta `d0466da..b9c6464`: 6 commits.**
  - `c41de72` RED: the guard enumerates route configs;
  - `9686371` RED: page_url;
  - `1575749` GREEN: the decoded path is scanned;
  - `85aba32` RED: the browser-encoded file name;
  - `7ea62d7` GREEN: the decoded file name is scanned;
  - `b9c6464` the merge (parents `d0466da` + `7ea62d7`).
- **`git --no-optional-locks diff --stat d0466da b9c6464`, as read by the drafter at 2026-09-13 14:54Z:**
  ```
   apps/api/src/feedback.ts                       |  26 +++++
   apps/api/src/routes/feedback.ts                |  12 ++
   apps/api/test/api-credential-shapes.db.test.ts | 149 +++++++++++++++++++++++++
   3 files changed, 187 insertions(+)
  ```
  - This matches the builder's claim of exactly 3 files. There are no deletions.
  - `diff --name-status d0466da b9c6464 -- packages/db/migrations packages/db/src/migrate.ts` is EMPTY.
  - **Re-read both yourself** (§3.1 rows 10-11). A drafter's reading is a claim too.
- `afc10e9..b9c6464` is 348 commits. HPSM-light `origin/main` = `afc10e98c51505be1f1943335370cf2de3b47d44`.
- **The launcher refuses unless all of these hold:**
  - the head is reachable from `refs/heads/main`;
  - its first parent is the delta base;
  - the delta touches exactly those 3 files and no migration.
- **Your verdicts are about b9c6464 only. A later head needs a new brief, not a re-pointed launcher.**
- **TWO verdicts, each GO / GO WITH FINDINGS / NO GO:**
  - `DELIVERABLES`: the fix does what it claims and what ruling (a) requires, without over-refusal;
  - `SECURITY`: what the fix still lets through, on every feedback field and path.

## Prior state (context only; round 1 of this delta class, no carry-forward)
- **No gate has tested this delta.** The builder's READY FOR QA delta note is `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-s45/feedback-fix-delta/README.md`. Read it whole.
  - L8-13: what changed. L15-19: the two defects.
  - L21-31: its results table. It is a CLAIM, not evidence.
  - L33-41: what the seat did NOT settle. L43-44: not claimed.
- **The feature this delta patches** is described in `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-s45/feedback-ready/README.md`. Use it as context for the surface only.
- **Independence.** A separate feature-scoped gate on the delta base ran earlier in another pane, on other ports and other compose projects. It has FINISHED and its stacks are down with volumes kept (Tuesday, 01:09 AEST).
  - This gate is independent of it. There are no results from it to relay, and this brief carries none.
  - Do not read its report directory and do not touch its kept volumes. §1's leave-alone list covers them.
  - The docker lock is still shared with other seats' lanes, so a docker step may queue on it.
- **This codebase has repeatedly shipped tests that could not fail.** The delta's own guard resolves route registrations with a regex over source (test L579-620). Treat it as an instrument that must be proved.

## Charter (read first, in full)
- **Charter:** `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. Rule 1 (FAIL condition first) and Rule 2 (NOT TESTED is output) govern every row.
- **Deliverables:**
  - reproduce both defects RED at the base, and show both closed at the head;
  - show that stored values are unchanged and ordinary input is not refused;
  - prove the delta's own tests can fail.
- **Security:** attack the scan two ways. First as a careless user pasting a credential through a real browser. Then as a hostile client that controls every byte of the request: every encoded form, every field, every path.

## 1. Target — LOCAL ONLY
- **LOCAL ONLY.** Your own clones and your own compose stacks on 127.0.0.1.
  - Out of scope: the live Azure demo, every other stack, and every other seat's worktree.
  - No request, no ssh, no `az`, no `gh`.
- **Clones:**
  - `D="$(mktemp -d)"; git clone --no-hardlinks '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer' "$D/pc"`, then check out the head DETACHED. Run `scripts/install-hooks.sh` in YOUR clone.
  - A second clone, or a worktree inside YOUR clone, detached at `d0466da`, for the RED reproductions.
  - **Never write into the original repository or its `.git`:** no `git worktree add` there, no fetch into it, no lock files. Read it only with `git --no-optional-locks`.
- **Your stacks,** 127.0.0.1 only, free at briefing. **Ports 21610-21729 are the gate's; nothing outside that range is yours.**
  - `policy-composer-qa-fbfix-up`, edge **21610**, the BASE-THEN-HEAD stack:
    - Bring it up at `d0466da` (16 migrations).
    - Create ordinary data: a second customer tenant, and a benign item with an attachment.
    - Reproduce both defects RED through the edge (§3.1 rows 1-2). Keep the id of every item the base stored.
    - Then redeploy the SAME project and volumes at `b9c6464`. The delta has no migration, so compose `migrate` must apply nothing. Record its log line verbatim; do not assume its wording.
    - Re-run the same probes (row 3), and read back every base-era row (row 4).
  - `policy-composer-qa-fbfix-fresh`, edge **21710**: `b9c6464` on empty volumes.
    - It is the schema-comparison control.
    - It is also the stack for superuser reads, object-store counts and any tamper.
  - Both use compose defaults (demo switch OFF) unless a probe needs ON; say which.
  - Generate stack passwords per run (pattern `scripts/ci.sh` L13-17). `PC_EDGE_PORT` sets the edge (`compose.yaml` L130).
  - **Optional, last:** clean-clone CI with `PC_CI_EDGE_PORT=21625` and `PC_E8_SOW_TEXT=/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md`.
    - `scripts/ci.sh` L9 names its own throwaway project `pc-ci-<run_id>`. It is the ONE project not named `policy-composer-qa-fbfix-*`.
    - Record its name in the docker ledger, and let `ci.sh` tear it down.
- **Browser:** the local image `mcr.microsoft.com/playwright:v1.63.0-noble` (present at briefing).
  - Drive it through `apps/web/e2e/run.sh <your project>`, or with a Playwright script run in that image against YOUR edge.
  - It is the instrument for the browser-encoded file name. Record the exact browser versions it carries.
- **Environment:** local compose, idp-mock synthetic identities, synthetic tenants, non-prod.
- **LEAVE ALONE:** never stop, recreate, exec into, send traffic to, or remove the volumes of anything you did not start. That includes:
  - lane A's stack `pc-lane-a`;
  - S45's seat and lane stacks `pc-s45-*` (among them 24080-24780 and 25080-25699), and `integ-s44`;
  - any `pc-ci-*` you did not start;
  - **any `policy-composer-qa-*` project or volume other than your two (an earlier gate's volumes are kept on purpose);**
  - any SSH tunnel or local port the S45 seat opens for its live run.
  - **Any port outside 21610-21729 belongs to someone else.**
- **Shared daemon, THE DOCKER LOCK.**
  - Run EVERY docker step as `lockf -k /private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/dc13ed6b-f206-4b51-b117-ff3f2723cf9b/scratchpad/docker.lock <cmd>`. That covers build, up, down, run, exec, and every suite that calls docker.
  - **The lock is shared with other seats' lanes.** Concurrent docker steps queue on it, and a wait on the lock is not a timeout.
  - Gates have first claim over lanes (answer L15). Hold the lock one step at a time, never across a pause.
  - Run test runners with `--maxWorkers=2`.
  - **A timeout gets at most 2 re-runs; after that the row is LOAD-BLOCKED** (NOT TESTED, with the reason). Never raise a timeout.
  - Count volumes at START and at END. There were 145 at briefing (2026-09-13 14:55Z); other seats may create volumes too, so attribute yours by compose project label, not by the difference in the count.
- **END:** `docker compose -p <each of your projects> down` with VOLUMES KEPT (no `-v`). Never `docker system|volume|image prune`, and never remove anything you did not create.

## 2. Spec / DoD - REFERENCE DOCUMENTS (read-only; every row cites document + line)
- **AUTHORITATIVE:** ruling (a) as quoted above (retarget answer L14-16). Its origin is ARCHITECTURE §2.5 L614-617, as amended by BACKLOG.md L1007 (a).
- **The builder's declaration:** the delta README above.
- **BACKLOG.md L52-69, the G45 entry.** It stays OPEN until this gate and the live upgrade.
  - L54: defect 1. L57-58: defect 2.
  - L61: the backslash side note.
  - L68: `apps/api/test` is in no tsconfig.
- **BACKLOG.md L45:** the guard gap, claimed CLOSED by this merge (README L41).
- **The seat's measurements of the other operations** (README L35-38). They are claims to verify:
  - `updateFeedback` scans its patch;
  - `triageFeedback` has NO request body;
  - query strings are not probed.
- **The HPSM implementation at `b9c6464`**, read in YOUR clone. Routes lines differ at `d0466da` below routes L399.
  - `apps/api/src/feedback.ts`:
    - `PAGE_URL_BASE` L42;
    - `pagePathOf` L55-73: drops the origin, query and fragment; `http`/`https` only; the 2,000 limit;
    - `decodedPagePath` L80-86: every `%XX` becomes a byte, then UTF-8; invalid bytes become U+FFFD;
    - `decodedFileName` L95-99: decodes runs of `%XX` only.
  - `apps/api/src/routes/feedback.ts`:
    - imports L12-13;
    - `checkUploads` L190-220: sanitised `filename` L194; `rawFilename` L203; the 400 naming refused files L197, L211;
    - `uploadRouteSchema` L223-257, querystring L246;
    - `readForm` L324-364: an empty `page_url` is dropped at L347-349;
    - `createFeedback` L366:
      - JSON body L382-384;
      - first scan L396-401;
      - decoded path scan L404-406;
      - decoded names scan L409-411;
      - request hash over the RAW page_url L413-415;
      - INSERT L446; `printableDisplayName` L459; `feedback.created` L491;
    - the upload route, registered outside `operation()`, L532-545;
    - `updateFeedback` L680, with its scan at L689;
    - `triageFeedback` L732-746, which recomputes at L735;
    - `deleteFeedback` L748.
  - `apps/api/src/feedback-multipart.ts`, `parseDisposition` L81-104:
    - parameter pattern L93;
    - quoted-string unescape L96-97;
    - a duplicate parameter returns null, L98;
    - only `filename` is used, L103.
  - `apps/api/src/feedback-attachments.ts`: `sanitiseDisplayName` L80-96 (basename L83); `attachmentDisposition` L193-197.
  - `apps/api/src/secrets.ts`: `MAX_JSON_DEPTH` L13; `refuseCredentialText` L84-98.
  - `apps/api/src/app.ts` L49-53: ajv `removeAdditional: false`, `coerceTypes: false`. `apps/api/src/server.ts` L100: `logger: true`.
  - `packages/api-contract/src/openapi.json` (L5 `0.14.0`):
    - `/feedback` L4719: POST takes `tenant_id` and `Idempotency-Key`, with JSON and multipart bodies;
    - `/feedback/{feedbackId}/triage` L5315: POST with NO requestBody;
    - `FeedbackCreate` L8565: `additionalProperties: false`;
    - `FeedbackPatch` L8839: `admin_notes` is the only free text, max 4,000.
  - `packages/db/migrations/0016_feedback.sql`: `page_path` check L24-26; `idempotency_key` L53-54; attachment `filename` check L79-81.
  - Web client:
    - `apps/web/src/feedback/page.ts` L9: the widget sends `location.pathname` only;
    - `submit.ts` L58, L77;
    - `FeedbackAdmin.tsx` L210 (`page_path`) and L253 (file name), both rendered as text.
  - `apps/api/test/api-credential-shapes.db.test.ts`:
    - `SHAPES` L52-130 (11 shapes);
    - `PROBES` L174-457. The `createFeedback` probes are L401-456, **multipart only: the JSON submit path has no repo probe;**
    - per-shape assertions L512; the control L540-577; the guard L579-620.
    - `apps/api/test/feedback-fixtures.ts` is present at both SHAs.
  - **No unit test names `decodedPagePath` or `decodedFileName`** (`git grep` over `apps` and `packages` at the head).
- **Suites.** Each runs in YOUR clone or against YOUR stack, and nowhere else.
  - Through `scripts/test-db.sh` (its own internal-only postgres, no published port, L1-3): `apps/api/test/api-credential-shapes.db.test.ts`, `apps/api/test/api-feedback.db.test.ts` and `apps/api/test/api-feedback-attachments.db.test.ts`.
    - Run them in YOUR head clone.
    - For the RED run, put the head's test file in YOUR base clone.
  - With the repo's vitest in YOUR clone: `apps/api/src/feedback.test.ts`, `apps/api/src/feedback-multipart.test.ts` and `apps/api/src/secrets.test.ts`.
  - `apps/web/e2e/run.sh <your project>` with `feedback-widget.spec.ts`, against YOUR head stack.
  - `scripts/secret-scan.sh` over YOUR clone.
  - **A repo test is evidence only after you watch it FAIL on a defect you planted in YOUR clone.** The minimum plants:
    - remove the decoded path scan (routes L404-406);
    - remove the decoded file-name scan (L409-411);
    - make `decodedPagePath` return its input;
    - make `decodedFileName` decode upper-case hex only. If the suite stays GREEN, it does not cover case;
    - add a route config the guard cannot resolve.
    - Assert that each plant landed (grep the marker, diff the file) before you read its result (charter §6).
- **Builder evidence** under `qa-s45/` and in the S45 scratchpad is a claim, not evidence.

## 2a. LEGITIMATE SHAPES
This is not a checker; it is a product feature. But the fix is a guard on ordinary input, so this table is required.
- Run each row at the base AND the head.
- **A 201 at the base that becomes 422 at the head is an over-refusal this delta introduced.**

| ordinary shape | expected |
|---|---|
| a page path with ordinary encoding (a space, an accent, CJK: `/engagements/Q3 review/controls`, `/search/café`), sent as the widget sends it (`location.pathname`) | 201 at both; `page_path` stored as the URL parser writes it (encoded), identical at both |
| a literal percent in the path: `/reports/100%25-complete`, a lone `%`, and `%FF%FE` (not UTF-8) | 201, stored as sent, no 500 (the test control at L560-577 claims this) |
| file names users really attach, sent by the image's browser: `Q3 report "final".pdf`, `café notes.docx`, a CJK screenshot name ending `.png`, `résumé (1).xlsx`, `50% done.log`, a name holding a literal `%20` | 201; the stored name is the sanitised name as sent, NOT decoded; identical at both |
| a non-browser client sending a Windows path as the file name, `C:\Users\x\Desktop\shot.png` | 201; record the stored name (§3.2 S7) |
| words, not values, in every free-text field: "password policy", "rotate the API key", "token lifetime"; a path `/settings/passphrase-policy`; a file `wpa_passphrase-howto.pdf` | 201: the scan refuses VALUES, not words |
| near-misses of the 11 shapes: an `Authorization` header NAME with no value; prose such as "set bindpw in the LDAP form"; a JSON object with an empty passphrase, percent-encoded into a path; a 40-hex git commit SHA in a path and in a file name; a UUID path | 201 expected. Before rating a 422, compare base vs head (§3.1 row 5) and check it against A-p2 (BACKLOG.md L888) |
| admin notes in ordinary prose; triage of an ordinary item | 200 |
| the same `Idempotency-Key` retried with the same body | one item, the same answer |

## 3. Scope
### 3.1 DELIVERABLES - traceability matrix
- **Row:** `ID | requirement | source + line | status | evidence path | evidence class`.
- **Status:**
  - MET / PARTIAL / NOT MET;
  - **RULED**: cite the ruling's path + line;
  - **NOT TESTABLE LOCALLY**: say why.

**Minimum rows:**
1. **Defect 1 is RED at the base** (README L16; BACKLOG.md L54).
   - Where: `policy-composer-qa-fbfix-up` at `d0466da`, through the edge.
   - Probe: each of the 11 shapes (test L52-130) in the page path, on JSON AND on multipart.
   - Record which answer 201, and which are stored in `page_path`.
   - The builder claims 6, on both paths: PGP private key block, `Authorization: Basic`, `snmp-server community`, `bindpw`, `wpa_passphrase`, and JSON passphrase.
   - **A different set is itself a finding against the claim.** Report the measured set.
2. **Defect 2 is RED at the base** (README L17; BACKLOG.md L57).
   - Send each shape as an attachment file name, the way a browser writes it.
   - First from the Playwright image's real Chromium: `FormData` through the product's own widget, or a `fetch` from a page on YOUR edge.
   - Then as raw multipart with `%22` / `%0A` / `%0D`.
   - The builder claims 1: the JSON passphrase. Record which browser version produced which bytes.
3. **Both are closed at the head.** Run the same probes on the same stack after the redeploy, and on `policy-composer-qa-fbfix-fresh`. Each must give:
   - 422 `SECRET_VALUE_ENTERED_IN_CLOUD`;
   - no echo of the value;
   - nothing stored (the checks of §3.2 S9).
4. **Stored values are unchanged** (retarget answer L15; README L12).
   - (a) Every §2a row stores byte-identical `page_path` and `filename` values at the base and the head. Its response bodies are also byte-identical, apart from ids and times.
   - (b) Every item the base stored on `policy-composer-qa-fbfix-up`, the defect rows included, reads back byte-identical after the redeploy. The fix must neither rewrite nor hide old rows.
   - (c) A download's `Content-Disposition` is unchanged.
5. **No over-refusal introduced by the delta.** Run every §2a row at the base AND the head.
   - **A 201 at the base that is 422 at the head is a finding** attributable to this delta.
   - A 422 at both is not new. Check it against A-p2 (BACKLOG.md L888).
6. **Fail closed, with no residue:** §3.2 S9.
7. **triageFeedback takes no body** (README L37).
   - READ ONLY: contract L5315 has no `requestBody`; routes L732-746 read no body.
   - RUNTIME: §3.2 S6.
8. **updateFeedback's `admin_notes` was already scanned** (README L36). RUNTIME: §3.2 S6.
9. **The delta's own tests can fail.** Re-derive README L21-31 in YOUR clones:
   - the guard at the head (the claim: 255/255);
   - the head's test file run against the base's source (the claims: 6 RED for page_url, 1 RED for the browser file name);
   - each §2 plant.
   - A test that stays GREEN under a plant is a finding.
10. **Diff review** (README L8-13).
    - Re-read `git --no-optional-locks diff --stat` and `--name-status` for `d0466da b9c6464`. FAIL if they differ from the drafter's reading above.
    - Review every hunk:
      - the scans run before any write (routes L396-411, before the INSERT at L446 and any object write);
      - the first scan still covers the raw and the sanitised names (L400);
      - `decodedPagePath` and `decodedFileName` cannot throw (feedback.ts L80-99);
      - the 422 detail names paths and shape labels only (secrets.ts L84-98).
    - **Anything changed outside the 3 files is a finding.**
11. **No migration change** (§3.3).
12. **The guard-gap closure claim** (BACKLOG.md L45; README L41): the guard now sees `createFeedback`.
    - Plant a route registration the guard's regex cannot resolve (test L579-620).
    - Plant a feedback operation that calls the scan with no probe.
    - The guard must FAIL on each.

**MET needs runtime evidence.** READ ONLY cannot carry MET alone.

### 3.2 SECURITY - attack plan (encoded forms, every field, every path)
**Every probe states FAIL first and has a POSITIVE CONTROL proving the instrument fires.**
- **Two classes. Keep them apart.**
  - (A) **In scope:** an ENCODING LAYER between the wire and the detector that hides a shape the detector catches in raw text.
  - (B) **KNOWN:** a raw-text syntax the detector misses (A-m1, BACKLOG.md L888). Do not re-report it.
- The control for every (A) probe is the same shape, raw, in a scanned field: it must be refused.
- To attribute a result to the delta, run the probe at the base too.

| # | Attack | FAIL if | Control |
|---|---|---|---|
| S1 | **page_url, every encoded form, on JSON AND multipart.** Each of the 11 shapes in the page path, encoded as: a single `%XX` of every separator and quote; lower and mixed case hex (`%2a`, `%2A`); double and triple encoding (`%2522`, `%252522`); `+` for a space; `%u0022`; overlong UTF-8 for a quote, a space and a colon (`%C0%A2`, `%E0%80%A2`, `%C0%A0`); invalid bytes inside the shape; other separators (`%09`, `%0B`, `%0C`, `%C2%A0`, `%E3%80%80`); fullwidth quote and colon; dot segments that splice two halves (`/<half>/../<half>`, `%2e%2e`); `\` as `/`; `;` path parameters. Also the shape in the page_url's userinfo, query and fragment, which `pagePathOf` drops. Also non-URL forms: a bare relative path, `//host/p`, `http:p`, an upper-case scheme, leading and trailing spaces | 201 with the shape stored in a form that a consumer decoding the stored value ONCE would read as the credential; a shape from userinfo, query or fragment stored anywhere; any 500. **A shape readable only after 2 or more decodes:** record it, find out whether any consumer decodes twice (FeedbackAdmin.tsx L210 renders `page_path` as text; confirm in the browser), and rate it on that evidence | the same shape, raw, in `title` is 422; an ordinary encoded path (§2a) is 201 |
| S2 | **Attachment file name, every encoded form.** First, a real browser submitting `FormData`: the image's Chromium, and Firefox and WebKit if the image carries them. Use names containing `"`, CR, LF, `\`, `%`, `;` and non-ASCII, and record the exact bytes each browser writes in `filename="…"`. The builder's Chromium 153 claim is a claim. Then raw multipart from a hostile client: quoted-string escapes (`\"`, `\\`); `%22`/`%0A`/`%0D` in lower and mixed case; double encoding; an unquoted token `filename=` value. Then `filename*=UTF-8''<percent-encoded shape>`, alone and beside a `filename` that differs (multipart L93-103 parses `filename*` but uses only `filename`). Then a duplicate `filename` (L98). Then a shape that a character strip would join: `sanitiseDisplayName` (L80-96) strips control characters and maps `"'`<>\|*?:` to `_`, and the DECODED-then-sanitised name is not scanned (routes L396-411). Last, a shape before or after a `/` or `\` (basename, L83) | 201 with the shape stored in `pc.feedback_attachment.filename`, in any item column, audit event or object key; a `filename*` value stored or served (Content-Disposition, attachments L193-197) without a scan; a part with only `filename*` stored as a field or a file; any 500 | the same shape as a plain `filename="…"` with backslash-escaped quotes (the form at test L432-434) is 422; an ordinary browser-sent name (§2a) is 201 and stored as the sanitised name as sent |
| S3 | **Every other feedback free-text field, JSON vs multipart.** `title` and `description` with percent-encoded, `\u`-escaped (JSON) and raw shapes. Multipart field parts with `Content-Transfer-Encoding: base64` or `quoted-printable`, or a `charset=` other than UTF-8. Field parts not in `FeedbackCreate` (additionalProperties false, openapi L8565), and unknown JSON properties, each carrying a shape. The same field sent twice in one multipart body | a raw or `\u`-escaped shape stored; an unknown field stored; a transfer-encoded field stored decoded without a scan of its decoded text; any 500. A LITERALLY percent-encoded shape in a title, stored as typed: record it, and rate it on whether any consumer decodes it (none is known; READ ONLY until shown) | the raw shape in the same field is 422; an ordinary title is 201 |
| S4 | **Query strings.** `POST /feedback?tenant_id=<id>&note=<shape>`; a shape as the `tenant_id` value; `GET /feedback?status=<shape>`; the shape in the page_url's own query (S1). Then grep the api container's log (`server.ts` L100 `logger: true`) and the edge container's log for the marker | the shape is stored in any `pc` table or audit event; any 500. **Logs:** a shape that reaches a log breaks ARCHITECTURE §2.5 L617. The drafter's grep of BACKLOG.md for `query string`, `access log`, `request log` and `logger` found no entry at 14:55Z; recheck it. If the shape reaches a log, the class is product-wide (every route logs its URL). Report it ONCE as a class, with the feedback instance as evidence, and rate its likelihood honestly: the widget sends only `location.pathname` (`page.ts` L9) | a marker in an ordinary query string appears in the log (proves the grep sees the log); the same request with no query does not carry it |
| S5 | **Stored headers.** `Idempotency-Key` carrying a shape (stored, 0016 L53-54; read the contract's schema for the header). A multipart part header other than `Content-Disposition` carrying a shape. The part's `name` parameter | the shape is stored; any 500 | an ordinary 8-200 character key is 201 and stored |
| S6 | **updateFeedback and triageFeedback.** `admin_notes` × 11 shapes, raw and `\u`-escaped (routes L689), and a patch nested deeper than 64 (secrets.ts L13). `POST /feedback/{id}/triage?tenant_id=` with a JSON body carrying a shape, an unknown field and a 65-deep body; then with `text/plain` and multipart bodies. Then triage a BASE-ERA item that stored a shape (§3.1 row 4), and read `triage_notes` and the `feedback.triaged` audit event | an admin-note shape stored; anything from a triage body stored or echoed, or a 500; a body that changes the triage result (the contract has no requestBody, openapi L5315). If the base-era triage copies the stored shape into `triage_notes` or the audit event, record it as a consequence of base-era rows (`d0466da` never ran live, HANDOVER-S45 L23) and rate it on that | an ordinary admin note is 200; a triage with no body is 200 |
| S7 | **The backslash side note, SIZED** (BACKLOG.md L61; answer L11). Measure what each available browser sends for a name holding `\`, and what is stored. Walk the interaction READ ONLY first, then probe it: the reader's unescape (multipart L96-97) runs before the basename split (attachments L83), so `a\b.txt` is stored as `ab.txt`, not `b.txt`. Hunt for consequences: a `\"` or a trailing `\` that ends the quoted-string early or late and smuggles a second parameter; a name whose stored form differs from every scanned form, so a shape appears only in storage; a basename or extension change that flips `classify` (routes L195) | a demonstrated shape, header injection, parameter smuggle, or extension/type flip; any 500. **Rating:** a cosmetic name change alone is Polish or Minor. Rate it higher only on a demonstrated consequence, and say which | an ordinary name with no `\` is stored unchanged |
| S8 | **Echo before the scan.** `checkUploads` (routes L190-220) is called in `readForm`, before the scan at L396, and answers 400 naming each refused file's sanitised name (L197, L211). Send a credential-shaped name on a file with an unsupported type or bad magic bytes. Repeat on a 413 and on a multipart refusal | the shape, as sent or as sanitised, is echoed in any response body or header; any 500 | a bad file with no shape in its name gets its 400 naming the file |
| S9 | **Fail closed, with no residue.** For every refused probe, check: no `pc.feedback_item` or `pc.feedback_attachment` row; no audit event; no object added to the object store (count objects before and after on `policy-composer-qa-fbfix-fresh`); the value absent from the response. Then retry the same `Idempotency-Key` with a clean body. Decoder robustness: a lone `%`, `%G0`, a truncated `%4`, a 2,000-character path of `%FF`, and a 120-character file name of `%FF` | a refused request leaves any row, event or object; the retry answers anything other than one clean 201 (record exactly what it does, and whether a refused request burns the key); a decoder input answers 500 or hangs | a clean submission adds exactly one row set, plus one object per attachment |
| S10 | **JSON vs multipart parity.** Every S1 and S3 shape on BOTH submit paths | the two paths answer the same shape differently | the same benign body gives 201 on both |

### 3.3 Migrations - none in this delta
- **READ ONLY:** `git --no-optional-locks diff --name-status d0466da b9c6464 -- packages/db/migrations/ packages/db/src/migrate.ts` must be EMPTY (the drafter read it empty). A non-empty result is a finding against the builder's 3-file claim.
- **Runtime:**
  - on `policy-composer-qa-fbfix-up`, the redeploy at `b9c6464` applies nothing; record the migrate log line;
  - `pg_dump --schema-only` of `policy-composer-qa-fbfix-up` after the redeploy vs `policy-composer-qa-fbfix-fresh`. **FAIL if they differ.** That is a finding; do not reconcile.
- **Never attempt the reverse SQL of 0016 (`reverse-0016.sql`): that is Kam's word only.**

## 4. Credentials (pointer only)
- **No live credential is needed for a LOCAL gate, and none is in scope.**
  - Read NOTHING under `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials/`. The launcher exports its identity dirs only for isolation.
  - Run no `az`, no `gh`.
- **Personas:** the idp-mock's synthetic users, `apps/idp-mock/src/app.ts`:
  - the seven roles at L10-18;
  - users at L48-73: `platform-admin`, `consultant`, `consultant-2`, `customer-approver-a`, `customer-approver-b` and the rest;
  - tokens from YOUR stack's `POST /idp/token` (L121), e.g. `http://127.0.0.1:21610/idp/token`.
- **The 11 shapes are synthetic** (test L52-130). Build every probe from them, or from your own synthetic variants, each carrying a random marker. Never use a real credential.
  - In the report and the mail, name a shape by its `SHAPES` label and give the encoding recipe.
  - Do not paste full shape values: downstream secret scanners cannot tell them from real ones.
- **Tokens are credentials:** never in the report, the evidence or the mail. Write "credentials present".

## 5. State-mutation & cleanup
- **Sanctioned:**
  - your own clones;
  - your two compose projects and their volumes, plus the CI's own throwaway project;
  - the synthetic tenants, sign-ins and feedback items you create on YOUR stacks;
  - superuser reads on both of your stacks. Tamper only on `policy-composer-qa-fbfix-fresh`.
- **Reachable:**
  - base-era items that stored a shape (on `policy-composer-qa-fbfix-up`);
  - refused submissions; triaged and updated items;
  - the base-to-head redeploy.
- **Gaps (documented, not failures):**
  - any live or Azure behaviour (out of scope);
  - browsers the image does not carry. Name them under NOT TESTED; never infer their encoding.
- **Never `rm`:** a new `mktemp -d` per attempt; quarantine, never removal; `${X:?}` on every expansion.
- **END:** stacks down with volumes KEPT. List volumes before and after, and every project, volume and image you created.

## 6. Output boundary / 6a. Evidence class
- **Findings, reports and recommendations ONLY** (Kam, 2026-08-11). Describe the fix-shape and the regression test in prose.
- **Evidence class on every finding and every row:** MEASURED AT RUNTIME (LOCAL) / PROBED / READ ONLY.
- **Build the schema the product deploys** (compose `migrate`). If a suite builds a different one, that is a finding; do not reconcile.

## 7. Known-fragile / known-changed
**RULINGS IN FORCE** (§2). A mismatch with any of these is a finding.
- 14:34:04Z ruling (a), retarget answer L14-16.
- The §2.5 deviation declared at BACKLOG.md L1007 (a).
- 14:54:25Z: ports, and the backslash note to size.

**KNOWN AND DECLARED at b9c6464.** A mismatch with a declaration is a finding; the declared item itself is not new.
- BACKLOG.md L52-69: this delta's own entry, still open. **Its two defects are the claims under test** (§3.1 rows 1-3), not KNOWN findings to skip.
- BACKLOG.md L61: the backslash side note. §3.2 S7 sizes and rates it; do not re-report it as new.
- BACKLOG.md L68: `apps/api/test` is in no tsconfig (TS2349 at `apps/api/test/contract.ts:23`). If the delta's test code carries a type error a typecheck would catch, report that instance citing L68.
- The feature's declared items (README L40). Their BACKLOG lines have moved since they were declared, so cite them by title:
  - orphan objects on a failed upload or an `Idempotency-Key` race;
  - about 51 MiB held in memory per upload;
  - no purge (ruled);
  - the sweep's Jira half is UNAVAILABLE;
  - e2e tenants are not torn down.
- BACKLOG.md L888: the credential detector's syntax gaps and false positives (A-m1, A-p2, A-m2).
  - A shape the detector misses in RAW text is KNOWN.
  - **NEW here:** an encoding layer that hides a shape the detector catches raw, or an over-refusal the delta introduced.
- BACKLOG.md L728: a credential-shaped display name answers 500 on storeOutput. Feedback uses the same `printableDisplayName` (routes L24, L459). **The same 500 on a feedback path is a NEW instance of a KNOWN class:** report it, citing L728.

**CLAIMED CLOSED in this delta (the claims under test, NOT KNOWN):** BACKLOG.md L45 (the guard gap), and both defects of BACKLOG.md L52.

**Outside this delta:** tenant isolation, the role matrix, RLS, attachment types and sizes, the edge body limit, retention, accessibility, and NexusAI parity. Do not redo them. A defect you trip over there is still a finding: record it, mark it outside the delta, and rate it.

**Still owed:** a KNOWN item that silently gives a WRONG RESULT on the delta's surface IS a finding. Mark it "KNOWN, re-rated", with its BACKLOG line.

## 8. Logistics
- **One session, LOCAL ONLY.** Order:
  1. clones, docker ledger START, the first head reading;
  2. diff review and the no-migration read (§3.1 rows 10-11, READ ONLY);
  3. `policy-composer-qa-fbfix-up` at `d0466da`: data, the RED reproductions (rows 1-2), §2a at the base;
  4. the redeploy at `b9c6464`: rows 3-4, and §2a at the head (row 5);
  5. `policy-composer-qa-fbfix-fresh`;
  6. SECURITY S1-S10;
  7. suites and plants (rows 9 and 12);
  8. CI (optional);
  9. the rest.
  - Anything unfinished is NOT TESTED, with the reason.
- **Head readings** of the original repo at start, mid and end: SHA + branch + time, via `git --no-optional-locks`. S45's seat is live, so main may move.
- **Launch:** Tuesday runs the launcher in one tmux pane (`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/HPSM-fbfix' "bash '<launcher>'"`), never nohup.
  - The launcher sets `CLAUDE_CONFIG_DIR=/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.claude`.
  - It sets HPSM's own `AZURE_CONFIG_DIR` / `GH_CONFIG_DIR` for isolation only.
- **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-14-composer-b9c6464-feedback-fix-delta-tier1/report.md`. It is a NEW path; the launcher refuses if it exists. In this order:
  - **BLUF:** both verdicts, plus Blocker / Major / Minor / Polish counts on the delta's surface;
  - **findings:** FOUND / TESTED / HOW, oracle, evidence class, and Blocker / Major / Minor / Polish with justification (priority is the humans' call);
  - the matrix;
  - the security table, with each control's result;
  - the no-migration check;
  - **NOT TESTED**, with the reason for each, including the encodings, fields and browsers you could not reach;
  - the docker ledger; the head readings.
- **Findings-only:** never fix, commit or file tickets. Run long commands in the FOREGROUND; never end a turn waiting on a background notice.
- **No inbox:**
  - where the brief is silent, take the safest reading and record it;
  - approval-class work is not done: anything on the live demo, the reverse SQL, money, external comms, anything irreversible. List it under NOT TESTED.
- **Before any mail:** grep the evidence folder and the report, with a positive control, for bearer tokens (`eyJ`), stack passwords, your planted markers, and full synthetic shape values. Record that the grep ran.
- **INTERIM mail AT ONCE for any Blocker** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-HPSM -> Tuesday] INTERIM BLOCKER — Policy Composer FEEDBACK fix delta @ b9c6464 (tier 1)`. Then keep testing.
- **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`:
  - subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer FEEDBACK fix delta @ b9c6464 (tier 1)`;
  - first line `DELIVERABLES: <GO | GO WITH FINDINGS | NO GO> · SECURITY: <GO | GO WITH FINDINGS | NO GO>`;
  - then `Blocker <n> · Major <n> · Minor <n> · Polish <n>` on the delta's surface, the NOT TESTED headline, and the report path.
  - **Datasec's coordinator is TUESDAY; never `wednesday-agent@`.**

PROVENANCE:
- Ruling (a), 14:34:04Z: credential-shaped free text fails closed with 422; the fix shape; the decoding question is the gate's; do not contact the running gate | retarget answer L14-16, L24, read whole | read 2026-09-14 00:59 AEST
- Gate commission: target accepted, GO needs three, backslash note to size, ports 21610-21729, no contact with either gate | 14:54:25Z answer L1-6, L11, L15, L20, read whole | read 2026-09-14 00:56 AEST
- ARCHITECTURE §2.5 L614-617; BACKLOG.md L1007 (a) | sed -n / grep -n | read 2026-09-14 01:00 AEST
- READY FOR QA delta: what changed, both defects, the results claims, the open items | the delta README, read whole | read 2026-09-14 00:54 AEST
- Head `b9c6464` = `refs/heads/main`; `d0466da` an ancestor and the first parent; 6 commits in the delta; 348 in `afc10e9..b9c6464`; `origin/main` `afc10e9`; diff --stat 3 files, 187 insertions, 0 deletions; the migrations name-status empty | `git --no-optional-locks` rev-parse / merge-base --is-ancestor / rev-list --count / log / diff --stat / diff --name-status | read 2026-09-13 14:54Z
- BACKLOG.md L45, L52-69, L728, L888, L1007; no entry for query strings or request logs | grep -n / sed -n on `HPSM/BACKLOG.md` (2,299 lines) | read 2026-09-13 14:55-14:58Z
- HANDOVER-S45 L23, L52-56, L106 | grep -n / sed -n | read 2026-09-14 00:57 AEST
- Implementation lines | `git show b9c6464:<path>` of feedback.ts, routes/feedback.ts, feedback-multipart.ts, feedback-attachments.ts, secrets.ts, app.ts, server.ts, openapi.json (parsed), 0016_feedback.sql, idp-mock app.ts, the web feedback files, api-credential-shapes.db.test.ts; `git show d0466da:apps/api/src/routes/feedback.ts` for the base anchors; `git cat-file -e d0466da:apps/api/test/feedback-fixtures.ts` | read 2026-09-14 00:55-01:02 AEST
- Ports 21610-21729 free: `lsof -nP -iTCP:21610-21729 -sTCP:LISTEN` returned nothing (rc 1). Control: the same command over the concurrently running gate's block listed its two edge listeners (rc 0), so an empty result is a real reading | read 2026-09-13 14:54Z and 14:59Z
- 145 volumes; the Playwright image present; docker answers within 30 s; the lock file exists; the report dir absent | docker volume ls, docker image inspect, docker info, ls | read 2026-09-13 14:55Z

AMENDED by Tuesday s15 at review (01:1x AEST): the concurrent gate FINISHED before launch; the four 'running now' lines are now past tense; nothing else changed.

SELF-CHECK: re-read end-to-end for contradictions. LOCAL ONLY throughout. No live host is named. No port, compose project or report path of the running gate is named; the S45 lane ranges appear only in §1's leave-alone list. No result from any other gate is carried. The report path and verdict subject agree with the launcher | 2026-09-14 01:05 AEST
