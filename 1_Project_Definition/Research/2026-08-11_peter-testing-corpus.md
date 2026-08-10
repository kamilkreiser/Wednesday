# Peter — Testing Corpus & Methodology Study

**Purpose:** build a complete picture of how Peter (client-side tester on Secuura Blockchain / Platform K, `peter@obeden.com`) tests, thinks, and challenges the platform — so Wednesday can scope a cross-project QA/testing agent modelled on his methodology.
**Author:** Wednesday research agent · **Date:** 2026-08-11
**Scope note:** the "methodology, distilled client-neutrally" section is deliberately scrubbed of all Secuura/Peter/client specifics and is safe to seed into any client's QA-agent session.

---

## BLUF

Peter is a **client-side / external QA and security tester** who works almost entirely from *evidence and code*, not from the platform's own claims. What makes him effective is a small set of disciplines applied relentlessly: he **reproduces every finding at the wire level** (raw `curl`, replayable case IDs, VCR cassettes) and cites `file:line`; he **distrusts green** and treats a passing check as a hypothesis until he has proven the check actually executed against a real precondition; he **hunts the class, not the instance** ("these two routes were found by accident, not by a check — audit every mount"); and he reasons about **blast radius and honesty** rather than mechanism — his sharpest findings are all variants of "the system claims something true that isn't" (fabricated anchors flagged confirmed, forged signatures labelled real, a revoked credential that still verifies). He self-corrects in public, retracts his own wrong findings with evidence, and stays rigorously **in his lane** (he tests and reports; he never writes backend fixes — he writes the regression test that flips green when someone else fixes it). Recommended QA-agent scope: an **advisory-only, evidence-first testing agent** that a calling project points at a running target + spec, which fuzzes/probes, reproduces findings deterministically with replayable artefacts, classifies honestly (executed vs skipped vs not-applicable), files findings as tickets with `file:line` + repro + blast-radius + suggested-fix-shape — and **never writes to the client's systems, never mutates state it can't clean up, and never rounds a green up to "fixed."**

---

## Provenance — sources read

**Linear (Secuura-PK team, key `KS`; some Secuura-PS `PS`) — READ-ONLY GraphQL queries, `includeArchived: true`:**
- Peter's Linear identity confirmed: user `peter@obeden.com`, displayName `peter`, active.
- **225 issues created by Peter** enumerated (KS + PS). Most are `Done` and **archived** (hidden by default in Linear — surfaced only via `includeArchived`).
- **93 comments authored by Peter** pulled in full and read (not just titles). Full comment threads read on: KS-480, KS-532, KS-570, KS-587 (the four seed tickets), plus KS-486, KS-487, KS-489, KS-490, KS-485, KS-492, KS-472, KS-519, KS-589, KS-539, KS-509, KS-508, KS-256, KS-384, KS-575, KS-525, KS-577, KS-586, KS-188, PS-19, KS-169, and three archived tickets (Akto 2.9.9 redesign ×2, ticket-consolidation 2026-08-06).
- Peter is a **creator/commenter**, rarely an assignee — he files, verifies, and hands remediation to Kamil (platform/dev side) or Stuart (Platform-S side). His own assigned work is test harnesses (KS-492 Review-G children, KS-357 Akto coverage, KS-510).

**Testing Harness folder** (`/Volumes/DevMASTER/!CODING/Secuura/Testing Harness and Agent/`): README read in full; the full tree (agent-brief, `harness/runner.js` all 14 phases, coverage audit, `test-stack/` specs + 17 tool wrappers, reports) characterised in depth by a sub-agent — folded into "His testing harnesses" below.

**Vault** (`/Volumes/DevMASTER/Notes (MASTER)/`): mined by a sub-agent. Key finding: **within `Secuura/` itself only two files mention Peter** (`platform-s-k-strategy-and-roadmap.md`, `Extranet.md`); the substantive record lives in `daily/` notes (2026-05-09 → 2026-08-10), plus `intelligence/` and `skills/Current/extranet.md`. There is **no Peter persona entry** (the "Platform Stakeholders and Personas" file is platform *roles*, no named humans), and `peter@obeden.com` does not appear in the vault. The `Testing/` run reports credit the tester as "Kamil Kreiser (via Cowork/Claude Agent)" — i.e. those are agent runs, not Peter's. Files with credentials present were not reproduced.

**Unreachable / not done:** No source was unreachable — DevMASTER drive mounted, Linear key valid, API reachable. Secrets were sourced transiently for queries only and are **not** reproduced here. I did not exhaustively read the platform's own `Blockchain/2_Project_Files/systemTest/` tree (characterised via the harness sub-agent instead). One caveat surfaced by the harness sub-agent and worth carrying: **the Testing Harness folder is a May–June 2026 snapshot and has drifted behind the live repo** — several wrappers/aggregator that read as "stub / not deployed" there are now implemented in-repo, so date-stamp any harness claim.

---

## Peter's defect archaeology — the CLASSES he finds, with ticket evidence

Peter's findings cluster into a handful of recurring **classes**. Ordered by how much they reveal his method.

### Class 1 — "Claims something true that isn't" (integrity / honesty defects)
His signature class, and the one he treats as most serious on an authenticity platform.
- **Fabricated anchors presented as genuine** — KS-587: *"84 anchors on the demo are fake but presented as real"* — `mock_tx_`/`tx_sim_` hashes carrying `simulated=false, status=confirmed`, so every doc in that window "claims a confirmed on-chain anchor that does not exist." He measured it read-only on the demo VM, tied it to a documented config incident (a blanked wallet mnemonic rsynced over demo), and noted *"the failure mode is a confident claim that cannot be checked, which is worse than an honest 'not anchored'."*
- **Forged signatures labelled real** — KS-489: prism issuance stamps `crypto.randomBytes(64)` as `type:'Ed25519Signature2020'` and verify returns `passed:true // Mock verification`; vc-issuer holder-binding "not cryptographically verified." He named the shared failure mode: *"claims-verified-but-isn't"* and grouped every instance into a "Wave 2 (integrity criticals)."
- **A revoked credential still verifies** — KS-521 (his), and KS-570's `unrevoke`: *"restoring a deliberately revoked credential to valid is an integrity operation, not an information leak."*
- **Honest-labelling as a required signal** — KS-522/523: a simulated anchor must carry an honest `simulated:true` flag or the verify path "has no way to know these are fabrications."

His test design follows from this: on KS-589 he built a **hash↔flag honesty invariant** ("a `mock_tx_`/`tx_sim_` hash must carry `simulated=true`; `simulated=true` must never present as confirmed or carry a block number; `simulated=false` must carry a real 64-hex hash") — and deliberately did **not** build it on the platform's own `blockchain_blob_is_simulated` helper because "it ORs the flag with the fabricated-hash test, so it answers True for Kamil's exact KS-587 shape and would score the defect honest. Proven red→green against that naive delegation."

### Class 2 — Authentication / authorization / tenancy / IDOR / BOLA / BFLA
His largest volume class (Review A, KS-486).
- **Missing-middleware auth bypass** — KS-570/KS-509: two gateway mounts (`/api/status`, `/api/leaderboard`) missing `authenticateToken`, so a *revoked-session* JWT (valid signature) still returns 200 while an anonymous request 401s. He root-caused it to `proxy.ts:697/:781`, proved the *systemic* exposure ("15 services import the shared `authenticate()`… each is one missing mount-line away from this same defect"), and separated the two stacked defects: missing *authentication* (revoked sessions) vs missing *authorization* (`/api/status` has no role check at all — "every holder of any valid token can already do all of it").
- **Cross-tenant key minting / BOLA cluster** — KS-486 pass-2: `POST /api/keys` takes `tenantId` from the request body with no role check → "any authed user mints a live key for any tenant"; `GET/DELETE /api/keys` BOLA; governance execute-proposal "no role check exists" despite the OpenAPI documenting Admin/403; staking/transfer/nft BOLA where mutating endpoints operate on a body `address` "with no binding to the JWT user."
- **`isDev`-gated fail-open auth** — routes using `...(isDev ? [] : [authenticate()])` where `isDev = NODE_ENV !== 'production'`, so any non-prod env exposes the DSR queue / erasure log unauthenticated. His instruction: *"Verify the demo VM's NODE_ENV."*
- **Unauthenticated file-read oracle** — mcp-server `/hash` takes `filePath` → `readFile(filePath)` with zero validation over `.env`/secrets.
- **Cross-tenant privilege escalation via seed path** — any single tenant's ORG_ADMIN could reset hardcoded accounts platform-wide to a known password.

### Class 3 — Input validation / injection / boundary bytes
- **Control-byte acceptance** — KS-472: C0 control bytes (0x01–0x1F, 0x7F) accepted **and persisted** on 14→30 write paths including GDPR, KYC, timestamps, wallets, the public verifier. He distinguished the already-fixed NUL (U+0000) case from "the broader C0 class still accepted — the open half of this ticket," listed all 30 operations, and gave copy-paste `curl` reproductions embedding the byte via `python3 -c 'chr(1)'`.
- **500-instead-of-4xx** — KS-514 (`"Invalid time value"` on unparseable date), KS-594 (governance cap returns `500 INTERNAL_ERROR` instead of `409` — a *business refusal mis-mapped to a server error*), KS-367/KS-508 undocumented HTML 400s. He flags these because a fuzzer scoring 400 as "correctly rejected bad input" would score a *server-supplied* unstorable value as healthy: *"A sweep scoring 400 as 'correctly rejected bad input' would score that as healthy."*
- **Contract/schema drift at scale** — KS-591 (`positive_data_acceptance` 734 failures/64 ops), KS-592 (`negative_data_rejection` 176/10), KS-593 (raw 5xx 17/8) — and crucially he tracks these as **recurrences/regressions**: "KS-430 → KS-515 → KS-591; KS-266 → KS-518 → KS-592… every intermediate ticket also Done and archived."

### Class 4 — Supply chain / secrets / dependency currency / CI hygiene
- **Committed real mnemonic + credential-reuse pattern** — KS-490: a real 24-word BIP-39 mnemonic + `SecuuraTest2026!` spending password tracked in git. He rates it Medium not High (preprod testnet, zero-value) but names the *practice* risk: "a committed real mnemonic normalises the practice… a credential-reuse pattern."
- **Unpinned actions on moving tags** — `@master` third-party GitHub actions (supply-chain risk).
- **Validated dependency audit** — KS-493/KS-384: he insists on *"pinned-version ground truth, not npm-audit range re-resolution,"* and **refuted his own pass-1 finding** ("axios is the only live drift") with the deeper audit (nested undici 5.29.0, 2 crit + 15 high in mobile).
- **CI blind spots** — KS-384: manifest-only dependency bumps slipping past a lockfile gate; he reproduced the *exact real drift that shipped* rather than a synthetic one, and caught that his first synthetic attempt was "a false test — it desyncs the ROOT lock too, so both paths fail and the blind spot is masked."

### Class 5 — DR / recoverability / silent-failure detection
- **The unrecoverable asset is not the obvious one** — KS-532/KS-480: he built a likelihood-rated data-loss register; the key insight, credited to Stuart and endorsed by him, is *"A lost key is recoverable by rotation; a lost GUID mapping is not"* — the anchor **index** (document↔tx linkage), not the on-chain proof, is the irreplaceable artefact.
- **Rotate-without-revoke** — KS-480/KS-577: he caught that `rotate:true` "mints a new key and never revokes the old one," and framed it in blast-radius/human terms: *"if someone left a company with a grudge and used the key maliciously, the company affected would not look kindly on our solution."* Kam reached the same conclusion independently and quoted Peter's line on the fix ticket.
- **Detection before cutover** — KS-577: *"All three cutover shapes are undetectable without PS-463"* (the oldest-unanchored-age alert). His reasoning about *silent* failure is a throughline: "the failures it causes are silent by construction. You'd learn about them from a customer, not a dashboard."

### Class 6 — The harness lying about itself (meta / test-infrastructure defects)
He audits his own tooling as harshly as the platform.
- **A check that never ran but reported green** — KS-589: the anchoring report⇄JUnit reconciliation "had **never once executed**" because it read a `junit.xml` constant while the file was written as `pytest-anchoring-output.xml`; `find -name junit.xml` returned nothing across every run, "each reporting *reconciled*." He found six sibling defects of the same class and coined the rule: *"a check whose input is MISSING must go RED, and a documented emitter must actually be called."*
- **Self-inflicted state** — KS-519: preconditions skips diagnosed as "a 401" were actually `500 "Maximum of 20 active proposals reached"` — *the cap filled by the sweep's own uncleaned fuzz proposals* (22 active, all titled `0000000000`, the fuzzer's min-length string). "Not a provisioning gap, and not a 401 — self-inflicted state."
- **The sweep locking itself out** — KS-575: the sweep fuzzes `POST /change-password` on the very account it authenticates with, then 401s for the rest of the run — "likely the true root of the recurring 'sweep auth 401/403' class, which has repeatedly been diagnosed as something else."
- **Stale ownership refs** — KS-589: a class rendering "a bare ref to its original ticket… all Done and archived. A bare ref reads as 'someone owns this'. Nobody did." He made the report render `KS-255 (closed — recurrence untracked)`.

### Class 7 — Coverage honesty (Akto/Schemathesis classification)
- **"An untested endpoint is not vulnerability-free"** — KS-325: he demands a *coverage-qualified verdict*, not "0 vulns."
- **Run-everything-classify-honestly** — the Akto redesign (archived, 2026-06-29): he replaced pre-excluding inapplicable templates with running *everything* and reclassifying post-run into `notApplicableStack` / `knownFalsePositive`, excluded from the coverage *denominator*, each with a plain-English reason, plus a drift guard that "fails loudly if a fingerprinted stack becomes a gateway upstream." Reported "93% honest coverage" rather than a bare PASS.
- **Don't gate on a flaky verdict** — KS-509/KS-570: he proved an Akto verdict is non-deterministic ("two pre-merge runs on an unchanged stack minutes apart returned vulnerable=1 then vulnerable=0 — identical input, opposite answers") and that "a run whose templates failed to load passed with '0 vulnerable' having executed nothing." His acceptance gate is therefore a **deterministic probe**, not the scanner verdict.

---

### Class 8 — Process & governance defects (he tests the workflow, not just the code)
The vault record shows Peter also imposes *process* controls, treating a weak gate as a defect:
- **Block-all CI gate** (his position, adopted): "any finding ≥ threshold blocks, new or pre-existing; escape only via a ticketed `gate-exceptions.json`. Reason: a known issue must be tracked, not silently merged."
- **Branch naming = ticket↔branch** (his ask): branches use Linear's auto `gitBranchName` so traceability is mechanical.
- **Pre-push githooks auto-activate** (his recommended enforcement point) so checks can't be skipped locally.
- **Detection-first, fix-handed-off** as a workflow: he owns "In Test → Deploy to UAT," merges the *detection* half and hands the *fix* (e.g. KS-425 weekend handover; his #588 regression suite "auto-flips to pass when these fail closed").
- **He disputes numbers and reopens closed tickets** rather than trusting a green: settled a "0 findings" dispute by proving his run was limiter-on ("limiter-off is the only trustworthy signal"), and reopened KS-199 to ask if the spec still needed updating.
- **He argues architecture** — the develop-vs-main branching model, rejecting template-keyed FP suppression as "= global test disable," and winning the Accept-Encoding DECODE-not-strip argument on failure-mode grounds.

### How the team works with him (context for the agent's persona/scope)
The Secuura fleet has built *conventions around Peter's reading* that are themselves instructive for a QA-agent design:
- **BLUF discipline is fleet-wide because of him:** every ticket comment / status / sign-off uses `## BLUF / ## Recommendation / ## Detail`, justified verbatim as *"Peter reads every ticket personally and that reading is the scarcest resource in the loop."* A QA agent's output should be optimised for a scarce human reader the same way.
- **He is ~4 days/week, tests local-first with test data, runs full sweeps off-hours/weekends**, and re-reproduces findings with fresh seeds before trusting a close.
- **He is outside the agent's authority:** the fleet's delegation protocol lists "external communication to a human outside the team — … Peter, Stuart" as requiring a signed mail from Kam. Peter is a *human reviewer the agent reports to*, not a delegatee.
- **Silence-consent windows** are the team's device for his sign-offs — but the record is emphatic that on the KS-480 contract the consent was **taken by explicit confirmation, not silence** ("the phrase 'consent by silence' must not appear — the mechanism was never triggered"). Relevant caution for any agent automating approval flows: engaged human review must never be misrepresented as consent-by-default.
- **The team actively protects him from their own defects** ("ensure Peter doesn't pick up our mistakes" → the KS-380 preflight harness + required PR gates), and notifies him on a three-channel protocol (extranet to-do + team-doc post + Linear @-mention) for anything he must act on.

---

## His testing harnesses

### The Testing Harness & Agent folder
`/Volumes/DevMASTER/!CODING/Secuura/Testing Harness and Agent/` — canonical home (2026-06-09 onward) for the testing agent's kit. Layout:
- `agent-brief/SECUURA-AGENT-BRIEF.md` — single ground-truth platform brief (creds, API rules, gotchas, runbook); "read end-to-end before doing anything."
- `harness/runner.js` — **test-kit-2026-05-24**, a browser-injected JS module. Injected into an admin-SPA devtools console on Local/Dev/Demo, then `await window._SX.runAll()`. It derives the API base URL from `location.hostname` (path-independent) and executes **14 phases**: health → auth → tenants → rights-holders → documents → certifications → verification → revocation → RBAC → M365 → API keys → verifier UI → portals → tool-stack readiness, returning a structured summary. Latest pass rates: Local 91%, Dev 78%, Demo 76%.
- `audit/HARNESS-COVERAGE-AUDIT-2026-06-09.md` — gap analysis vs OWASP/SOC2/ISO/GDPR/APP; proposes 8 new phases (headers/cookies depth, JWT structure, BOLA/BFLA, security.txt + DSAR, rate-limit, anchor integrity, inventory drift, evidence emission) plus an out-of-band CI hardening track (Schemathesis, Nuclei, trivy, syft, gitleaks).
- `test-stack/` — the KS-49 CI scaffold: `ci/orchestrate.sh` + per-tool wrappers (`run-schemathesis`, `run-nuclei`, `run-trivy`, etc.) and specs for parallelization / tiered-blocking / dedupe.
- `reports/` — dated e2e reports (templates for new runs); `references/` — dev-agent Q&A, environment notes, QA-tool cheat sheets, dashboards.
- **Continuity model:** a Cowork-side memory (`MEMORY.md` index) keeps a chronological log of findings, dev-agent corrections, platform-state snapshots, and run results — "read the index before starting a new run."

**The runner in detail (`harness/runner.js`, test-kit-2026-05-24).** A single browser-injected IIFE (~16KB, one shot into an admin-SPA devtools console via Chrome MCP), registering `window._SX` and returning a sentinel `_SX_LOADED_<env>_<version>`. It detects env from `location.hostname` and derives the API base by host-swap (path-independent, no config file), and carries **env-aware transport rules** that are themselves a tested insight: CSRF header name and cookie mode differ Local vs Cloud, and because a cross-subdomain cookie cannot flow, **Cloud writes 403 by design — reported as a coverage gap, not a bug** (KS-107). Helpers re-read the CSRF cookie before *every* write (cookies rotate), skip Content-Type on bodyless GETs (avoids preflight failure), and poll for SPA hydration before screenshotting (the fix for a pre-hydration false-positive). `runAll()` runs 14 phases sequentially, each try/caught, and returns a structured `summary()` with pass/fail/warn/skip/info counts, `passRate`, and per-phase breakdown. Statuses PASS/FAIL/WARN/SKIP/INFO; ~40 tests on a healthy Dev, up to 55 on Local. The 14 phases: 01 Health · 02 Auth (valid/bad-password/malformed/no-token) · 03 Tenants · 04 RightsHolders (with full request/response stashed on failure) · 05 Documents (with a **documented caveat that three negative cases pass for the wrong reason** — they 400 on missing title, not hash validation) · 06 Certifications · 07 Verification (includes an **`F-DEMO-VERIFY-01` sentinel**: `verified:true` with no anchor evidence → FAIL as regression) · 08 Revocation · 09 RBAC (**`BUG-ROLE-001`**: a bogus `superadmin_hacker` role that is actually granted → FAIL) · 10 M365 (Dev; 503 = PASS-by-design) · 11 APIKeys · 12 VerifierUI · 13 Portals · 14 ToolStack (**readiness, never execution** — Akto/APIFuzzer hard-coded FAIL when not deployed, a 5-security-header probe, etc.).

**The agent-brief (`SECUURA-AGENT-BRIEF.md`, ~766 lines).** The institutional-knowledge document that makes an LLM agent productive in one turn: platform/personas/tenancy, per-env credentials + tenant IDs, the two API rules (response envelope + CSRF on every mutation), **22 explicit "gotchas"** (e.g. a CSRF-reject looks like a CORS TypeError; JWT-shaped strings must be redacted; the `/api/api/…` base-URL trap; login lockout 5/15min), a runbook (read brief → **confirm scope with a human before guessing which envs to test** → inject → parallel run → collect failures → visual spot-check → report → memory update), reporting expectations, and a "recent platform changes — don't flag as new" list. Note a `.STALE_DO_NOT_USE.txt` near-duplicate copy sits alongside it as a trap for greppers.

**The coverage audit (`HARNESS-COVERAGE-AUDIT-2026-06-09.md`, ~471 lines).** Frames the runner honestly as a *functional surface smoke* (~40 probes over ~15 of ~268 endpoints; "Phase 14 is a readiness probe, not an assurance probe"), maps each phase to standards (OWASP API Top 10 2023, ASVS, SOC 2 CC-numbers, ISO 27001, GDPR/APP articles), and proposes **8 new phases (15–22, each <150 LoC, no new deps)**: HeadersCookies, JWT structure, AuthZ (persona cross-role 403s), Compliance (`security.txt`/DSAR/erasure), RateLimit, AnchorIntegrity, InventoryBuild (spec-drift), and Evidence (assemble one SOC 2 artefact) — plus a 16-row **CI hardening track** (npm-audit+grype, syft SBOM, trivy, semgrep, gitleaks, testssl, ZAP, Nuclei, Schemathesis, Akto, APIFuzzer, k6, `aiken check`, SLSA provenance, signed commits) whose result counts feed back into Phase 14/22 to convert readiness into assurance.

**The CI test-stack design (`test-stack/specs/`).** Three written specs the in-repo CI later implements: **(01) parallelization map** — Stage 1 static tools in parallel → "API up" gate → Stage 2 DAST/perf/E2E each on its own KS instance, with per-tool P50/P99 budgets and timeouts and an explicit "if PR creeps past 9 min, drop X" fallback; **(02) tiered blocking** — resolves a real Kamil-vs-Peter disagreement (fast PR gate vs "everything blocks") into three tiers (PR-blocking ~9 min / pre-merge ~15 min / nightly ~30 min) with **computed, not chosen, promotion rules** (CRITICAL/HIGH + first-party → always blocking; third-party/runtime → nightly-blocking only; MED/LOW/INFO → informational-but-tracked); **(03) dedupe matrix** — a normalized finding shape and per-category dedupe-key tuples, a scenario×tool PRIMARY/Supplement grid, and conflict resolution (severity = max, first-party ownership wins, `sources[]` retained). `test-stack/ci/tools/` holds 17 wrappers (the Schemathesis one at 235 lines is the most developed: 6 modes contract/fuzz/negative/auth/stateful/idempotency, each with its own v4 flag set and tier); the Akto wrapper carries an explicit "do NOT mirror production traffic" PII warning.

**Report conventions.** Findings named `F-<AREA>-<NN>` (or `BUG-…`) each with severity/env/status/root-cause-to-`file:line`/proposed-action; a Δ-vs-prior-run column; a "closures CONFIRMED this run" table; raw HTTP/JSON evidence blocks; a **separate "harness corrections (not platform bugs)" section** (runner defects vs platform defects); a mandatory **"Uncovered (known gaps; not regressions)"** section naming the missing tool + KS ticket ("if a report doesn't include these, the agent has overclaimed coverage"); and a scrub rule (return `{status, len}`, never raw JWT-shaped bodies). The machine-readable finding shape (id = sha256 of dedupe key, tool, severity, category, endpoint, cve/package, ownership, evidence ≤1KB, first_seen commit, raw_pointer) is the aggregator's contract.

### The systemTest suites he actually lives in (in the Blockchain repo)
Beyond the browser runner, Peter's day-to-day work is the repo's `systemTest/` tree — the tools he wraps, gates, and audits:
- **Schemathesis** (property-based API contract fuzzing) — his primary instrument. Run via `python3 scripts/run.py full` (full local sweep on `:6882`) vs a fast PR gate. He built: authenticated-coverage gating (a run that loses its session and never reaches a handler must **fail**, not read as "nothing failed" — KS-517), report⇄console reconciliation, per-check→Linear-ticket columns, `xfail`/`skip` report-only regressions that auto-flip when the platform fix lands, and honesty invariants. Artefacts per run: VCR cassette (`schemathesis-output.yaml`), replayable crash files (`schemathesis-crashes/*.json`), `st replay <CASE_ID>`, metrics JSONL, console txt — every finding is reproducible from disk.
- **Akto** (OWASP API security scanning) — coverage-honest classification (above); he drives `authzPrecondition` skips toward zero (KS-357) and treats the scanner as *discovery*, never an acceptance gate.
- **k6** (performance: smoke/load/stress/spike/soak/capacity — KS-193–198) — soak runs to detect memory leaks and connection exhaustion.
- **Playwright** (end-to-end UI journeys — KS-525) — 23 flows across the published API; he flags flows where the product state can't be reached deterministically (e.g. an already-expired certification, a synthetic system-error) rather than faking coverage.
- **CI tiering** — PR / pre-merge / nightly tiers; he is deliberate that durable route-table-wide regressions go in the **nightly** tier "so PR/pre-merge gates stay untouched," and that a **mount-level assertion** (every `/api/*` proxy mount carries `authenticateToken`) "would have caught this class at review time."

---

## The methodology, distilled CLIENT-NEUTRALLY

*(No client/product/person specifics below — safe to seed into any QA-agent session.)*

**A. Evidence over claims.**
1. Never trust the system's own report of itself. A passing check, a green scan, a "confirmed" flag, a boot log — each is a *hypothesis* until independently verified. Verify the check actually executed against a real precondition before believing its verdict.
2. Reproduce every finding at the lowest honest level — a raw request, a replayable case ID, a stored request/response pair. A finding without a deterministic reproduction "proves nothing either way."
3. Cite location precisely (`file:line`, exact field, exact endpoint). Trace a defect through the code path, not just the symptom, so the root cause and the fix site are both named.
4. Re-derive every figure from source and record corrections in public rather than quietly fixing them ("Corrections made today, recorded rather than quietly fixed").

**B. Distrust green — the ways a pass lies.**
5. A check whose *input is missing* must go RED, not silently pass. A documented emitter must actually be called. (A reconciliation that reads a file that is never written will report "reconciled" forever.)
6. A green that measured nothing is worse than a red. Prove the test executed (rows produced, a verdict reached with a real message) before believing "0 findings."
7. A 4xx can be a *mis-mapping*, not a healthy rejection: a business refusal or a server-side unstorable value dressed as a client-input error. Don't score a status code as "correct rejection" without knowing *why* it was returned.
8. Prove the preconditions were real. A 401 proves nothing if the subject was never in the state you think — an expired token 401s "for the wrong reason and looks exactly like a fix." Assert the precondition (state, session count, token expiry) alongside the result.
9. A non-deterministic verdict is not an acceptance gate. If identical input yields opposite answers across runs, use the tool for *discovery* and gate on a deterministic probe instead.

**C. Hunt the class, not the instance.**
10. When a defect is found "by accident rather than by a check," assume siblings exist and audit the whole surface (every mount, every route, every service sharing the code path). Name the systemic exposure even when only two instances are proven.
11. Prefer a structural guard over a per-instance convention: "a per-endpoint 'remember not to include it' convention will eventually fail." Push the check to the single code path (one layer, one assertion) that covers the class.
12. Track recurrence explicitly. A class that has been "fixed" two or three times and returned is a **regression pattern**, not a fresh bug — and a bare reference to a closed ticket "reads as 'someone owns this'. Nobody does." Make ownership of recurring classes visible.

**D. Reason about honesty, blast radius, and silence.**
13. The most serious defect class on any trust system is "claims something true that isn't" — fabricated proof presented as genuine, unverified signatures labelled verified, revoked things still validating. A confident false claim is worse than an honest "unknown."
14. Rate findings by *likelihood of occurring in operation* and *blast radius*, separately from severity and from implementation difficulty. Decide contested calls on blast radius, not mechanism.
15. The dangerous failures are the **silent** ones — the ones surfaced by a customer, not a dashboard. "The cautious-looking option whose failure mode is invisible" is not actually the safe one. Insist that detection/alerting is in place and *verified firing* before an irreversible operation is exercised.
16. Identify the genuinely unrecoverable asset (often not the obvious one) and protect that first.

**E. Audit your own tooling as harshly as the target.**
17. A test harness can lie about itself: report a check as run that never ran, accumulate its own state until legitimate operations fail ("self-inflicted state"), or lock itself out by fuzzing the account it authenticates with. Treat harness defects as first-class findings.
18. A capture/observation layer must not perturb what it observes: "a pass through it must predict a pass without it." Fail *loudly and locally*, never *silently and systemically*.
19. When fuzzing mutates shared state, either scope the run to a disposable identity or clean up after — never leave residue that degrades the next run or the shared environment.

**F. Coverage honesty.**
20. "An untested endpoint is not vulnerability-free." Report a *coverage-qualified* verdict: what ran, what was skipped and why, what is not-applicable and why (excluded from the denominator, each with a plain-English reason) — never a bare PASS.
21. Prefer "run everything and classify honestly" over pre-excluding what looks inapplicable; add a drift guard that fails loudly if an excluded assumption ever becomes false.
22. Label a read-only surface as a read surface rather than implying journey coverage you don't have. If a required product state can't be reached deterministically within a run, record it as a documented coverage gap, not a silent omission.

**G. Discipline, lane, and communication.**
23. Stay in your lane: test and report; write the *regression test* that flips green when the owner fixes the defect — do not write the fix yourself. Hand remediation to the owner with a suggested fix-*shape*, not a patch.
24. Self-correct in public. Retract your own wrong findings with evidence and name the reasoning error ("I confirmed a mechanism and then assumed it was the cause"; "I reasoned from the harness's model of the platform rather than the platform itself").
25. Separate what you proved from what you assume; flag loose ends you didn't chase rather than smoothing them over ("flagging rather than smoothing over").
26. Ask the owner to record the *why* behind a decision, not just the what — those rationale notes stop findings being wrongly re-derived weeks later ("more of them makes the next round faster and less wrong").
27. Frame a review request so that "if the platform is right, the test is wrong" — invite the owner to correct the test, because some test calls are really platform questions "wearing a test costume."
28. One consolidated status per period; supersede stale notes explicitly ("a stale one is how someone acts on the wrong thing").

---

## Recommended role scope for the QA agent

### What it should do
- **Advisory, evidence-first testing.** Point it at a running target + its API spec (and, read-only, its source tree). It probes/fuzzes/scans, reproduces every finding deterministically with a replayable artefact, root-causes to `file:line`, and reports.
- **Distrust-green gating.** For any pass it relies on, it verifies the check executed against a real, asserted precondition — and refuses to report "clean" for a run that measured nothing.
- **Class-hunting.** On any finding "found by accident," it enumerates the surface and reports the systemic exposure, and recommends the structural/single-path guard over per-instance conventions.
- **Honesty & blast-radius framing.** It flags "claims-true-that-isn't" defects as the top class; rates by likelihood-in-operation and blast radius; and insists detection is verified-firing before irreversible operations.
- **Coverage-honest verdicts.** Every report is coverage-qualified (ran / skipped-why / N/A-why), never a bare PASS.
- **Regression authoring.** It writes report-only regression tests (skip/xfail) that document a live defect without red-ing a gate and auto-flip when the fix lands.
- **Self-auditing.** It treats its own harness defects (never-ran checks, self-inflicted state, self-lockout, observer-perturbation) as first-class findings.

### Inputs it needs from a calling project
- A running target (base URL) and the environment identity (which env, what `NODE_ENV`/mode) — *confirmed with a human, never guessed*.
- The API spec (OpenAPI) and read-only access to the source tree for root-causing.
- Test credentials/personas for the roles it must exercise (attacker-role + normal-role), ideally a **disposable** account for state-mutating fuzz.
- A findings sink (a ticket tracker) and the naming/label conventions to file into.
- A statement of which product states are reachable on-demand (so it can label unreachable ones as documented coverage gaps).

### What it must NEVER do (hard advisory-only guardrails)
- **Never write to, patch, deploy to, or reconfigure the client's systems.** It reports findings and writes tests; it never authors the fix.
- **Never mutate state it cannot clean up**, and never fuzz destructive/credential-mutating operations against the identity it authenticates with (use a disposable account or exclude+record).
- **Never run against production**, and never operate on an environment whose identity/mode it hasn't confirmed.
- **Never round a green up to "fixed"** — no "0 vulns / all green" claim without proof the checks executed against real preconditions.
- **Never copy secrets** (JWTs, keys, mnemonics, PII) into a report, a ticket, or an artefact — scrub before emitting; refer to them as "credentials present."
- **Never present an assumption as a verified fact** — separate proved from inferred; flag unchased loose ends.

### Open design questions for Wednesday / Kam
1. **Cross-client isolation.** Peter's methodology is client-neutral but his *artefacts* are Secuura-specific. How does the agent carry transferable heuristics between clients while keeping each client's findings/creds/spec strictly siloed (per the workspace hard rules)? A shared "methodology core" + per-client evidence store?
2. **Write boundary vs. useful automation.** Peter never writes fixes but *does* write regression tests into the repo. Is the QA agent allowed to write *tests* into a calling project's test tree (a bounded write), or is it purely read-and-report with the calling agent applying its test PRs? (This is the "manage, don't do" tension.)
3. **State mutation & cleanup.** Fuzzing inherently mutates state. What's the sanctioned pattern — disposable accounts the agent provisions, a scoped teardown, or exclude-and-report-only? Peter's own harness got this wrong (KS-519/KS-575) and it's a recurring trap.
4. **Tool ownership.** Does the agent run its own tool stack (Schemathesis/Akto/k6/Playwright/nuclei/trivy) drive-locally per the portability rule, or invoke the calling project's existing suites? Peter mostly *hardened the project's own suites* rather than running a parallel stack.
5. **Verdict authority.** Given his proof that scanner verdicts are non-deterministic, should the agent be *barred* from gating on any single tool verdict and *required* to produce a deterministic probe for every acceptance claim?
6. **Persona / voice.** Peter's public self-correction and "record corrections rather than quietly fix them" is a cultural behaviour worth encoding as an agent norm — how strongly should Wednesday bake that in vs. leave it to the calling project's conventions?
