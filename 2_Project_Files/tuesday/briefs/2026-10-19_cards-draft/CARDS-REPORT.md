# Cards report 2026-10-19 (drafter; nothing posted)

Kept 4 cards, dropped 5 candidates. Process note: the four JSON files were written with a short python script, not the Write tool (same content, same path). Read-only throughout: `decision_queue.sh list/show` only; Jira GET with the HPSM-POC `.env` in-process; `gh api` GET of the analysis repo with that project's `GH_CONFIG_DIR`; no demo or hosted host contacted.

## HPSM-POC

| Candidate | Result | Why | Sources |
|---|---|---|---|
| HPSMPOC-6 SME + deputy PO | KEPT: `hpsmpoc-sme-deputy-1019` | Still open. PO half ruled (C-05), SME read as Kam, no deputy named. Word "deputy" has 0 hits in the analysis-repo CLARIFICATIONS.md (1745 lines, positive control: "Security SME" hits 2). Naming people is Kam's. | Jira HPSMPOC-6 (desc + comments 2026-09-23, 2026-09-27); analysis CLARIFICATIONS.md:21; local BACKLOG.md:12; decision queue ruled/open lists (no card on it) |
| HPSMPOC-237 money (larger plan) | DROPPED | Not a spend ask. The ticket itself recommends no spend and states the default "no change (B180 Q-B180-4)". No priced option exists (costs "unmeasured today"), no Jira comments. A card only becomes Kam-class when a priced option exists. Server-Timing now exists (C-81 onwards), and recent stage readings put the time in the API's caller/write stage, not plan CPU (CLARIFICATIONS.md:927, :971), so a plan upgrade is not indicated. Tuesday can hold at B1. | Jira HPSMPOC-237 (desc); analysis CLARIFICATIONS.md:884-971 |
| HPSMPOC-224 telemetry | DROPPED, already ruled | Kam accepted POC-2 default (a) "Yes, after 13 Oct, personal data scrubbed", card `hpsmpoc-decisions-pack-1012` ruled a 2026-10-12, recorded C-99 (CLARIFICATIONS.md:1116). Remaining step is a deploy card when the build exists, which Tuesday raises then. Premise flag: POC-2 says "new Azure resource", but HPSMPOC-224 says App Insights `appi-hpsmpoc-demo` is already provisioned and only the app sends nothing, so the deploy card may need no new resource. Check when building. | decision_queue.sh show hpsmpoc-decisions-pack-1012; CLARIFICATIONS.md:1116; Jira HPSMPOC-224 |
| HPSMPOC-267 import words | KEPT: `hpsmpoc-import-words-1019` | Open, Kam-owned (C-105 customer words; C-108 "Kam's word owed before ImportsEnabled is ever true"). Not on any earlier card (C-108 says the sweep sentence "was NOT on the card"; the 10-13 words card `hpsmpoc-words-b230-b231-1013` is not about it). Low urgency, so default is hold. Also unblocks -275 and -263 (C-113). | Jira HPSMPOC-267; CLARIFICATIONS.md:1270-1279 (C-108), :1424-1436 (C-113); queue ruled list |
| HPSMPOC-268 hosted .NET 10.0.13 | DROPPED, already ruled | Cards `hpsmpoc-hosted-runtime-10013-1017` (a, 2026-10-18 18:59) and `hpsmpoc-runtime-10013-route-1018` (a: wait for Azure, read at next deploy; ruled 20:56, delivered 23:12). Recorded C-116 (CLARIFICATIONS.md:1514-1535). B273 read still 10.0.12; ticket stays open per ruling a; next read is the next deploy's platform log. Re-raise only if that read is still old. | decision_queue.sh show both cards; CLARIFICATIONS.md C-116; Jira HPSMPOC-268 |

## Security Composer

| Candidate | Result | Why | Sources |
|---|---|---|---|
| #106 release signing key | DROPPED, already ruled | COMP-7 (a) "Yes, at the next deploy", accepted via C-71 (card `composer-decisions-pack-1012` ruled a 2026-10-12). The key setup is an operations step on the next deploy card, not a new decision. | BACKLOG.md:110; CLARIFICATIONS.md:1303 |
| #43 contract change | DROPPED | Not Kam-class: a read-only pointer feature ("Asked under E04") needing an internal API-contract bump, no money, no external party, no production effect. Row says OPEN, "not small", plan written. Not in the C-71 pack. It is a build-priority matter for Tuesday to queue or leave parked. | BACKLOG.md:47; grep of CLARIFICATIONS.md shows no ruling on it |
| Chainguard free-tier terms/retention | KEPT: `composer-minio-image-terms-1019` | Vendor terms and a possible registry cost are legal/money, flagged to Kam in B280 FOR TUESDAY 1. Terms and retention are unmeasured. No earlier card on MinIO/Chainguard (queue grep: 0 hits). Context: the pinned quay.io image now 401s (B277:21), so local/CI are blocked. Note PR #80 got NO GO from the B281 gate on a flaky test on main, not on the image; that triage is Tuesday's, not on this card. | B277 STATUS:21; B278 STATUS:34-36, :168-185; B280 STATUS:19-33, :122-131; B281 STATUS:1-3; queue lists |
| Demo overlay `quay.io/minio/minio:latest` | KEPT: `composer-demo-minio-overlay-1019` | Demo VM is Kam's; reading it needs his word (BACKLOG #27, #247). Overlay is not in the repo, last seen running 2026-10-16. Whether a rebuild can pull the tag: UNMEASURED (not contacted). | B280 STATUS F-1, F-2, FOR TUESDAY 3; B155 evidence step2_read_r2.txt:10 (cited via B280); BACKLOG.md:31, :243 |

## Other notes
- Local HPSM-POC CLARIFICATIONS.md ends at C-30 and is stale; the real log is `datasecau/HPSM-POC-analysis` (read via gh GET, saved only in the session scratchpad).
- Facts are as of 2026-10-19 early afternoon; the HPSM-POC Jira rows were read live today (-6 updated 09-27, -237 10-08, -224 10-06, -267 10-17).
- Unmeasured: demo VM state, whether quay.io `:latest` pulls, Chainguard retention, any price for a registry or plan.
