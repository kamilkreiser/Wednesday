# HPSMPOC build queue: open tickets after the reconcile

**Generated:** 2026-09-27 08:47:08 AEST. Base: HPSM-POC main `33abe1a`.

**52 open tickets:** 10 A · 14 B · 8 C · 20 D.

**Routing:** **no class-A item qualifies for Spark as it stands.**
- The only single-file candidate is 32. Its product change is one line (`ReportModelBuilder.cs:310`) with a runnable test beside it (`ReportModelTests.cs`). But the PDF outline goldens (`Reporting.Tests/Golden/*.outline.json`) may move, so a Claude seat should confirm first.
- Every other A item touches auth, security, Azure, several screens, or documents.

## A: ours to build now, easy → hard
| # | Key | Summary | Size | Route | Why / the exact ask |
|---|---|---|---|---|---|
| 1 | HPSMPOC-32 | Ruleset version shown in the report | S | Claude (Spark after the golden check) | The version is stored (`Entities.cs:75`) but not printed. Add a plain-words "Rules version 0.1.0" row beside "Scoring rules" (`ReportModelBuilder.cs:309-310`). Keep B14 F-07's ban on `id@version`/hash. |
| 2 | HPSMPOC-17 | Acceptance matrix → real tests | S | Claude | 13/13 rows mapped, but all still DESIGNED against planned ids. Re-point each row to the named tests at 33abe1a (the CLOSE_LIST tests are a head start). Then Kam confirms the bars. Analysis repo, no code. |
| 3 | HPSMPOC-15 | POC AI acceptance criteria | S | Claude | The boundary is written (05) and built. Draft the adapted AC-AI-02/03/04/05/07 list against what is on main, then Kam approves it (it becomes B at approval). |
| 4 | HPSMPOC-9 | Stage-gate evidence pack + CR log | M | Claude | Agent-owned, and nothing exists yet. Templates M1–M8 mapped to §9.2 evidence; a CR form with value/effort/schedule/displaced scope. Docs only. |
| 5 | HPSMPOC-59 | Security scans + OWASP review | M | Claude | Add `dependency-review-action` and `npm audit` to CI. Run the ASVS/OWASP review against the BUILT code (the drafts assume a BFF/CSRF that does not exist). Secret scanning is a repo setting: flag it to Kam, not a build item. |
| 6 | HPSMPOC-22 | Event-ready states on the showcase screens | M | Claude | Prototype and B04 screens are proven (`e2e/states.spec.ts`). B09/B11/B17 customer and partner screens have no loading/empty/error proofs. The fallback-customer path also needs writing into the demo pack. |
| 7 | HPSMPOC-26 | Web profile form for the ruleset `profileFields` | M | Claude | The API is done and tested. The web saves only industry plus 3 facts (`ApiSteps.tsx:50`) and never calls `putCustomerProfile`. Field wording stays placeholder until HP's data dictionary arrives. |
| 8 | HPSMPOC-53 | Metrics summary + cross-run dashboard | M | Claude | `getMetricsSummary` is NotYetImplemented (`ContractTests.cs:47`). Build the summary and a per-run view. The baseline column stays blank ("not supplied") until 51. |
| 9 | HPSMPOC-43 | Blob report store | M | Claude | Only `FileReportStore` exists (`ReportingIntegration.cs:28`). Add an `IReportStore` for Azure Blob (managed identity, write-once, sha256 kept), testable on Azurite. The live deploy waits on 57. |
| 10 | HPSMPOC-36 | Consultant override with audit note | L | Claude | Prototype-only today. Needs `putFindingDisposition` (contract op, NotYetImplemented), note required, audit event, rule outcome kept visible, and web wiring for API customers. SOW §3.1: narrative and disposition only, never severity (X-13). It also unblocks 28 and 52. |

## B: needs Kam's decision
| Key | Summary | The decision |
|---|---|---|
| HPSMPOC-3 | Executed SOW + Tech Lead | Sign the SOW; name the Tech Lead (team ruled: C-02). |
| HPSMPOC-4 | IP clause | The §11.3 clause, in the SOW Kam is writing (position ruled: C-04). |
| HPSMPOC-5 | Event window + audience | Window and audience for 1 Dec (date ruled: C-03). This is Datasec's to answer under C-09. |
| HPSMPOC-6 | Security SME + deputy PO | Name the SME (or confirm it is Kam) and a deputy PO. |
| HPSMPOC-7 | SME funding §9.1 vs §9.3 | A written choice. |
| HPSMPOC-11 | Kick-off / SME cadence | Record a kick-off and office hours, or waive them as N/A under C-02. |
| HPSMPOC-12 | Demo script v0 review | Review the script. It predates C-12 (deck + 16 questions) and the showcase, and U1–U11 are open. |
| HPSMPOC-13 | Design pack approval (M2) | Written PO approval. |
| HPSMPOC-14 | Rules schema approval | Rule RS-03…RS-10 (the scoring math). |
| HPSMPOC-16 | Stack decision record sign-off | Sign off 10_ADRs.md, with the deviations listed (no Figma; PdfPig). |
| HPSMPOC-19 | Figma vs the coded prototype | Does the coded prototype replace Figma? |
| HPSMPOC-20 | Prototype approval (M2) | Written PO approval against a named version. |
| HPSMPOC-21 | Branding | HP, Datasec or co-brand (with HP's logo approval). The swap is one file. |
| HPSMPOC-51 | Manual baseline + metric definitions | Baseline hours with their source; approve M1–M7; T_idle/T_last (QA-129). |

## C: waits on SME/HP content
| Key | Summary | Content owed |
|---|---|---|
| HPSMPOC-31 | SME authors the representative content | Customer Security Maturity questions (requested, C-19 addendum), mappings, weights, remediation. |
| HPSMPOC-35 | Remediation buckets | Approved remediation text per finding (the machinery is done). |
| HPSMPOC-37 | Golden scenarios reconcile to SME | The SME's scenarios and expected results (the harness is ready). |
| HPSMPOC-44 | Report language + disclaimers | Approved methodology, disclaimer and terminology text. |
| HPSMPOC-46 | Approved HP/HPSM examples | The recommendation library (replaces `hpsm-guidance.synthetic.json`). |
| HPSMPOC-47 | Finding → HPSM mapping config | Approved mapping content from 46 (no code left). |
| HPSMPOC-48 | Recommendation view + report section | "Implementation-ready" needs 46's approved guidance (the view and section are built). |
| HPSMPOC-55 | Trial runs + metrics output | SME trial runs; the baseline from 51. |

## D: blocked on something else
| Key | Summary | Blocked on |
|---|---|---|
| HPSMPOC-57 | Dev/UAT/Demo via IaC | Kam registering the 6 remaining providers (C-13 azure-providers: a). Then deploy (about US$108/month, design-pack 18). |
| HPSMPOC-24 | Entra web sign-in | A web host and web app registration (57; C-13 entra-app: a). Auth work, so Claude/L when unblocked. |
| HPSMPOC-58 | CI/CD auto-deploy | 57 (branch protection is done as ruled). |
| HPSMPOC-29 | M3 demo in UAT | 57, plus 24. |
| HPSMPOC-60 | Playwright in UAT/Demo | 57, plus the final script (12). The journey spec exists. |
| HPSMPOC-61 | UAT + triage | 57, plus SME time. |
| HPSMPOC-62 | Demo freeze, fallback, rehearsal | 57 and 12. |
| HPSMPOC-63 | Event-day, handover, Phase 2 backlog | M8 / the event on 1 Dec. |
| HPSMPOC-64 | 30-day hypercare | The event. |
| HPSMPOC-28 | Audit of override actions | 36 (everything else is audited). |
| HPSMPOC-52 | Override metric | 36 (the other metrics are captured). |
| HPSMPOC-1, -10, -18, -23, -30, -38, -45, -50, -56 | The 9 epics | Their children. Each epic closes when its last child does. |
