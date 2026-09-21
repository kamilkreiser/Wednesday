# External dashboard — requirements and options study

**Date:** 2026-09-21 (AEST) · **Author:** Wednesday (research drafter, sub-agent) · **Status:** COMPLETE draft for Kam's ruling (written 09:54–10:09 AEST; no build, no `az`)
**Asked by Kam, 2026-09-21 09:52, verbatim:**
> "Been thinking, and I would like to build this dashboard in a way that is externally accessible to me, and both you and Tuesday interact with it through APIs. This will be hosted in the Chrysler.org Azure tenant and secured by MFA, so it's an external website. Depending on the overhead and speed, one approach will be to tokenize all data and to have de-tokenization based on certificates that live on my machine or multiple machines. Please look what would be required to do this."

("Chrysler.org" = dictation for **kreiser.org** — Kam's own identity/tenant, controller `kreiser.org@me.com`. Tenant id: **to be confirmed by Kam**; this document does not assert one.)

**Nothing in this document has been built, provisioned, or changed. No `az` command and no cloud call was run. It is a requirements + options study for Kam to rule on.**

---

## 0. BLUF

**What Kam asked for requires four things:** (1) an Entra ID single-tenant app in the kreiser.org tenant with Kam as its only user and MFA enforced by tenant policy (Security Defaults free; Conditional Access needs Entra P1 at USD 7/user/month); (2) an authenticated API with six seat routes where **Wednesday and Tuesday each hold their own certificate-backed app registration** and the server partitions every row by `client` (Secuura / Datasec / WED) from the token's role, never from the body — R0 enforced server-side; (3) a store in Azure replacing today's ~4.2 MB of JSON files (5 chat/decision streams, ~5,000 records) with delta (`since=`) reads, because today's page re-downloads the whole 3.3 MB log every 3 s and that cannot cross mobile data; (4) for "tokenised data de-tokenised by certificates on my machines" — **that is field-level encryption under keys held on Kam's devices, not tokenisation**; it is buildable (WebCrypto non-extractable keys or passkey-PRF), costs ≈ 5–10 extra seat-days and a permanent key-management duty, adds milliseconds of crypto per record, and must leave `client`, `view`, timestamps and option letters in the clear so routing and rulings keep working.
**Recommended shape:** Option A (existing Python server → App Service B1 Linux behind Easy Auth, Table storage or Cosmos serverless, Key Vault CMK, free access restrictions instead of a USD 35–381/month WAF) **with the encryption envelope designed in from the first record**, so Option B becomes a scheme flag in Phase 2 rather than a rebuild. Option C (relay/tunnel to the Studio) is cheapest but is not an API-driven external site and is down when the Studio is.
**Effort:** A ≈ 2 seat-days; B ≈ 7–12; 1-day pilot with synthetic rows first. **Running cost:** ≈ USD 15–20/month (australiaeast, Retail Prices API 2026-09-21); ≈ 55 with Front Door Standard; + 7 for P1. AUD unmeasured.
**Only Kam can decide:** (Q1) which tenant "kreiser.org" is — if it is Datasec environment #5 (controller `kreiser.org@me.com`, holds Vision Sales Portal production), Secuura content lands in a Datasec environment and hard rules 2/4 need his explicit override; (Q2) one partitioned store for both clients or two deployments; (Q6) whether the Azure operator / a compromised app is in the threat model — yes makes encryption mandatory before any real row; (Q3) phone, laptop or both as the key-holding device.
**Nothing is built. No `az` was run. The same prose already sits in plaintext in the GitHub repo the two seats sync through today** — that fact should weigh on Q6.

---

## 1. What exists today (measured from the repo, 2026-09-21 09:5x AEST)

### 1.1 The server
| Item | Measured value | Source |
|---|---|---|
| Server | `2_Project_Files/dashboard/server.py` (51,326 B), Python stdlib `ThreadingHTTPServer`, started by `serve.sh` (1,663 B) which also runs `collect.py` + `generate.py` every 300 s | `serve.sh:28-39`, `server.py:875` |
| Bind | `127.0.0.1:47787` only — PORTS.md rule 3: "Never bind 0.0.0.0 — remote access is Phase 4 (Tailscale) with auth" | `PORTS.md`, `server.py:875` |
| Auth | **None.** The loopback bind IS the auth. Docstring: "NOTE before any remote exposure (Phase 4/Tailscale): add auth to this API." | `server.py:28` |
| Secrets the server holds | reads `4_Credentials/.env` at start: `LINEAR_API_KEY`, `LINEAR_TEAM_ID`, plus (collector) `AGENTMAIL_API_KEY`, `MSGRAPH_*`, `SECUURA_GCAL_ICS_URL` — 11 keys total, names only | `server.py:41-49`, `collect.py:22-30` |
| Pages | `/` (generated `site/index.html`), `/chat` (`chat.html`, 27,754 B), `/cockpit` (`cockpit.html`, 72,193 B — conversation + fleet feed + NEEDS-YOU decision cards) | `server.py:6-11` |
| Read API | `GET /api/health`, `/api/chatlog` (whole derived log + ack join), `/api/usage` (per-seat %, with `age_seconds` — staleness returned, never hidden), `/api/agentmail` (subjects only, bodies never collected), `/api/decisions` (whole `decisions.json`), `/uploads/*` | `server.py:196-300` |
| Write API (browser → server) | `POST /api/chat` (Kam's message, ≤100,000 chars, `view` = the tab he typed in, optional attachments), `/api/upload`, `/api/speak` + `/api/speak/stop`, `/api/mute`, `/api/layout`, `/api/views`, `/api/pin`, `/api/focus`, `/api/actionnow`, `/api/archive`, `/api/park*` (4), `/api/flag`, `/api/personal_*` (3), `/api/add`, `/api/prioritise`, `/api/start` — 24 POST routes; the Linear ones write to Kam's WED board via `LINEAR_API_KEY` | `server.py:415-870` |
| Polling load | `cockpit.html` polls `/api/chatlog` **every 3 s** (`:1367`), `/api/agentmail` + `/api/decisions` every 20 s, `/api/usage` every 60 s. `/api/chatlog` returns the WHOLE `chat_log.json` (3,338,506 B today) on every poll — ~1.1 MB/s sustained per open tab. Harmless on loopback; **not shippable over mobile data** — an external API needs `since=`/delta paging before anything else. | `cockpit.html:661,1367`; file size below |
| Voice | Autoplay is **server-side**: the page POSTs `/api/speak {ts}`; the server looks the message up and runs `voice/speak.sh` → macOS `say` (Matilda/Moira) **on the Studio's speakers**. The browser never synthesises speech. Autoplay voices only messages whose `seat` == this machine's hostname (`server.py:520-528`). | `server.py:150,500-555`, `voice/speak.sh` |

### 1.2 The data store — `0_Brain/dashboard/data/` (14 MB on disk incl. 20 `(conflict_on_…)` copies; 70 files)
Shapes measured with a key-count script; **no message bodies were read into this document.**

| File | Shape | n | Bytes | Writer (single-writer rule, Phase 0 2026-09-08) | Reader |
|---|---|---|---|---|---|
| `chat_kam.json` | list of `{role:"kam", text, ts, view, attachments?}` — `view` present on 457/458 | 458 | 124,044 | **the panel only** (`server._kam_append`) | `chat_streams.py`, `kam_msgs.sh`, `reconcile_rulings.py`, both seats' wake_watch |
| `chat_wednesday.json` | list of `{role:"wednesday", seat, project, ts, text, spoken?}`; `project`: Secuura 707 / WED 96; avg text 1,113 chars, max 4,074 | 803 | 1,020,621 | **Wednesday seat only** (`tools/chat_reply.sh`, Studio) | `chat_streams.py` |
| `chat_tuesday.json` | same shape; `project`: Datasec 358 / WED 10; avg 1,054 chars | 368 | 446,995 | **Tuesday seat only** (`chat_reply.sh` on the mini) | `chat_streams.py` |
| `chat_legacy.json` | frozen 2026-09-08; mixed roles; 1,676/1,778 have no `project` field | 1,778 | 1,569,832 | nobody (frozen) | `chat_streams.py` |
| `chat_log.json` | **DERIVED, gitignored** — union of the four above + `agent`, `agent_source` fields; served by `/api/chatlog` | 3,407 | 3,338,506 | `tools/chat_streams.py` (rebuilt after every write) | `generate.py`, `/api/chatlog`, wake_watch, `decision_queue.sh`, ~13 consumers |
| `decisions.json` | list of cards `{id, client_project, title, bluf, options[{key,label,detail}], recommended, default_action, status, ruled_choice, ruled_ts, delivered_artefact?, amendments?…}`; `client_project` first segment: **Secuura 185 / Datasec 113 / WED 21 / Fleet 8**; status ruled 313 / withdrawn 12 / open 2 | 327 | 1,003,456 | **`tools/decision_queue.sh`** (both seats, one shared tracked file guarded by `_store_guard.sh`; `reconcile_rulings.py` folds Kam's taps into it, seat-scoped by client) | `/api/decisions` → cockpit NEEDS-YOU; `generate.py` |
| `usage_wednesday.json` / `usage_tuesday.json` | `{agent, pct, resets_in, ts}` | 1 | 79 / 78 | each seat's `statusline.sh` (one writer per file) | `/api/usage` |
| `agentmail.json` / `agentmail_error.json` | `{collected_at, data}` subjects snapshot / `{collected_at, error}` | – | 6,830 / 116 | `collect.py` | `/api/agentmail` |
| `ack_state.json`, `muted.json`, `layout.json`, `views.json`, `pinned.json`, `wedflags.json` | Kam's per-panel UI state | – | ≤2,452 each | the panel | the panel |
| calendars, `linear_*`, `tickets.json`, `brain_state.json`, `news.json`, `parkinglot.json` | `{collected_at, data}` collector feeds (personal EventKit, Secuura ICS, Datasec Graph, Linear WED) | – | 0.5–9 KB each | `collect.py` every 300 s | `generate.py` → `site/index.html` |

**Store size that would actually be hosted:** the four tracked chat streams + decisions ≈ 4.2 MB (5,000 records); everything else < 60 KB. Text per agent message averages ~1.1 KB; Kam's average 158 chars.

### 1.3 The two-seat write pattern (what the "APIs" are today)
- **Transport between the seats is git over GitHub** (`git@github.com:kamilkreiser/Wednesday.git`, per the 2026-09-16 structure note §1b). `tools/panel_sync.sh loop` (60 s, Studio) and `com.tuesday.chatsync` → `tools/chat_sync.sh` (60 s, mini) commit and pull the tracked streams; no `--autostash` (it corrupted `decisions.json` twice on 2026-09-09); `advance_other_streams()` fast-forwards ONLY the other seat's stream and never its own. **Consequence for this study: the streams already leave the machines** — GitHub holds every message today. "Local machines are the record" is true of authorship, not of custody.
- **Tuesday does not run a server** (structure note §9, Kam's "one website" ruling); her presence on Kam's page depends entirely on chatsync + the Studio being up. Kam reads the Studio's page.
- **Seat identity is derived, never typed:** the stream FILENAME names the agent (`chat_streams.py` STREAMS map); `chat_reply.sh` refuses to write if it cannot tell which seat it is (`WED_AGENT` or the folder name). The per-seat client default (`SEAT_PROJECT`, Studio→Secuura, mini→Datasec) is the ONE place the machine→client mapping lives, and Kam called it temporary.
- **Kam's rulings** arrive as chat messages (`Decision <id>: <key> — <label>`) posted by the cockpit's card buttons; the button never writes `decisions.json`. `reconcile_rulings.py --apply` rules only THIS seat's client's cards; another client's taps are reported, not applied (hard rule 2 applied to bookkeeping).
- **What the seats need from an external API, therefore:** (1) append to *my* chat stream; (2) read Kam's stream (`chat_kam`) filtered to my `view`; (3) add / rule / deliver / amend / withdraw decision cards for *my* client; (4) publish my usage %; (5) read acks; (6) optionally publish collector feeds. Nothing else in the 24 POST routes is a seat operation — they are Kam-in-browser operations.

### 1.4 What the panel IS to Kam (the lessons that constrain any rebuild)
- **2026-08-17 — the conversation needs a stable panel.** The chat tile is the ONE stable reading surface; fleet mechanics never go there; "separate the SURFACES, never throttle the WORK." An external site must stay a *reading* surface at least as stable as today's — latency and outages are regressions against a lesson, not features to trade.
- **2026-09-10 — a panel message is a RECORD, not a string.** `text` + `view` + `attachments` travel together; any API that drops `view` or attachments recreates a lesson that has already cost two retractions. Tokenisation that hides `view` from the server would break routing (see §4).
- **2026-09-09 — confirm receipt on the board.** "A working-but-silent channel and a broken one look identical" to Kam. Acks are records the seats write within seconds; an external API must not add a minute of queueing between his message and the seat's ack, or the channel reads as broken.
- **2026-09-08 note §2(a) — the content is two clients in one artefact.** Measured then: 1,129 "Secuura" hits, 279 "Datasec", 1,163 mentions of named client humans, 321 credential words, 144 unfixed-vulnerability words in the chat log alone. Today the split is stronger in the data (`project` on 1,273/3,407 records; 2,134 legacy records untagged) but `decisions.json` is still ONE file with Secuura 185 / Datasec 113 cards. **"One SURFACE must not become one CONTEXT"** — the merge exists in Kam's browser, never in a seat's context.

### 1.5 Tenant facts that bound the design (from `/Volumes/DevMASTER/CLAUDE.md` hard rule 4)
- Kam names "the kreiser.org tenant". The workspace rules record `kreiser.org@me.com` as the **controller of Datasec environment #5** (tenant `d500ebad-…`, two subscriptions, "separate *because it can be controlled by agents*") — but that tenant holds Datasec production (Vision Sales Portal) and Datasec dev/staging. **Whether Kam means that tenant or a separate personal kreiser.org tenant is the first open question (§7 Q1).** This document does not assume either; a Wednesday+Tuesday dashboard that carries Secuura content **must not** land in a Datasec environment (hard rules 2 and 4), so if #5 is what he means, the Secuura rows need a different home or a different answer.
- Agent identities are scoped per project via service principals confined to their own resource groups; an authorization failure is the boundary working — report it, never widen it. The same pattern (one SP / one cert per seat, scoped to one API role) is what §2(b) proposes.
- Every `az` command needs the tenant confirmed first; the seat's `AZURE_CONFIG_DIR` is per project. **No `az` was run for this study.**

## 2. Requirements (split as Kam's sentence splits them)

Each requirement names what would satisfy it and the measured fact it rests on. "MUST" = Kam's words or a hard rule; "SHOULD" = derived from a lesson; "DEFAULT" = this document's proposal where Kam has not spoken.

### 2(a) Kam's access from anywhere, behind MFA
| # | Requirement | Level | Basis |
|---|---|---|---|
| a1 | Kam signs in with ONE identity (his own account in the kreiser.org tenant), never a shared passcode. | MUST | Kam: "secured by MFA"; 2026-09-08 note §2(d): a passcode is one shared secret, not an identity |
| a2 | MFA enforced on every sign-in, phishing-resistant where the device allows (passkey / Authenticator number-match), via Conditional Access if the licence permits, Security Defaults otherwise (see §3 for the licence fact). | MUST | Kam's sentence; §8 sources |
| a3 | Session lifetime bounded (re-auth ≤ 24 h on phone, ≤ 8 h on a new device); sign-in frequency set by policy, not by the app. | SHOULD | phone loss is the realistic threat (§4 threat column) |
| a4 | The site is reachable with **no VPN and no third-party mesh client** on the phone — Kam said "external website". A mesh (option C) satisfies "reachable from anywhere" but not "external website"; it is listed as the cheapest fallback, not the answer to his sentence. | MUST (as asked) | Kam's words |
| a5 | Kam is the only human viewer. There is no second user, no role matrix, no sharing. Any design that adds a user directory is over-built. | DEFAULT | measured: one `role:"kam"` writer, 458 messages |

### 2(b) Two seats writing and reading through APIs with their OWN identities
| # | Requirement | Level | Basis |
|---|---|---|---|
| b1 | Wednesday (Studio) and Tuesday (mini) each hold **one non-shared credential**: an app registration with a **certificate** (private key generated on that machine, never exported) or an equivalent per-seat identity. No client secret strings in `.env`. | MUST | hard rule 3; workspace rule 4 per-project SP pattern; today `.env` already holds 11 secret names — the new design adds zero |
| b2 | Each seat's token carries a **`client` claim / app role** naming its client scope: Wednesday → `{Secuura, WED}`, Tuesday → `{Datasec, WED}`. The API enforces it server-side on every read and write; the seat cannot widen it by asking. | MUST | R0 (structurally unable to leak); `reconcile_rulings.py` already refuses another client's cards — the API makes that refusal impossible to route around |
| b3 | **Partition key = `client`** (`Secuura` / `Datasec` / `WED`), taken from the seat's claim on write, never from the request body. Secondary key `stream` (`kam` / `wednesday` / `tuesday` / `decision`). A record's `client` is what the store partitions on, what the API filters on, and what the browser filter chip reads. `WED` is the shared partition both seats may read (fleet/tooling cards, Kam's untargeted messages). | DEFAULT | today's `project` field maps 1:1 (Secuura 707 / WED 96 on Wednesday's stream; Datasec 358 / WED 10 on Tuesday's) |
| b4 | The seat operations are exactly the §1.3 list: `POST /streams/{me}` (append), `GET /streams/kam?view=me&since=`, `POST/PATCH /decisions/{id}` (add / rule / deliver / amend / withdraw within my client), `PUT /usage/{me}`, `GET /acks?since=`. Six routes. Everything else stays browser-only. | DEFAULT | §1.3 |
| b5 | **Delta reads.** Every list route takes `since=<ts>` and returns only newer records; a seat or browser never re-downloads 3.3 MB. | MUST | `/api/chatlog` today returns the whole store per 3-s poll (§1.1) — fine on loopback, a regression on mobile |
| b6 | The seats **keep writing their local streams too** (dual-write) during any pilot; the local files remain the fallback and the git transport remains armed until Kam rules the site is the record (§7 Q5). | DEFAULT | go-slow rule; 2026-09-09 two corruptions from an unattended sync change |
| b7 | A seat that cannot reach the API **fails loud, never silent**: the write is queued locally and the panel's own liveness line shows the backlog. | SHOULD | `panel_sync.sh`: "a sync failing silently every minute is worse than no sync at all" |

### 2(c) Client isolation — Secuura vs Datasec rows never rendered together without the right claim
| # | Requirement | Level | Basis |
|---|---|---|---|
| c1 | Kam's browser session carries the union claim `{Secuura, Datasec, WED}` because he is the only human and the only party entitled to both. **A seat's token never does.** | MUST | R0; 2026-09-08 note §3: "the merged view is for KAM's eyes only" |
| c2 | The server filters by claim **before** serialising; the client filter chip is a display convenience, never the security boundary (today the chip is the only filter — `chat.html`/`cockpit.html` — and it is per-browser localStorage). | MUST | R0 |
| c3 | `decisions.json` — today one file with 185 Secuura + 113 Datasec cards — splits into per-client partitions in the store; the `WED`/`Fleet` cards (29) sit in the shared partition. `reconcile_rulings.py`'s seat scope becomes an API-enforced scope. | MUST | measured §1.2 |
| c4 | Whether the two clients may share ONE deployment (one store, partitioned) or need TWO deployments (two apps, two stores, one sign-in) is **Kam's ruling** (§7 Q2). Default here: one deployment, partitioned, because the alternative doubles cost and Kam's own browser is where the merge already happens. The 2026-09-08 note leaned the other way ("generated per-client into two separate sites") — this document records the disagreement rather than hiding it. | Kam | §7 Q2 |
| c5 | Logs, metrics and error payloads are also partitioned or redacted: a stack trace that prints a Secuura card title into a Datasec-scoped log is a leak by the same rule. | SHOULD | 2026-08-13 shared-bus lesson: the leak was ~400 chars of another client's body in a scratchpad |

### 2(d) Availability and latency
| # | Requirement | Level | Basis |
|---|---|---|---|
| d1 | Kam reads on a phone: first paint of the last 50 messages < 2 s on mobile data; new-message poll or push ≤ 5 s behind the seat's write (today: 3-s poll on loopback; seat→Kam via git is 60–120 s). | SHOULD | `cockpit.html:1367`; `panel_sync.sh` 60 s loop |
| d2 | The site is up when the Studio is down (that is the point of "external"); if the design ties availability to the Studio (option C) that is stated as a cost, not hidden. | MUST (as asked) | Kam's words; 2026-09-16 note §9: Tuesday's presence today depends "entirely" on the Studio being up |
| d3 | **Autoplay voice:** today the Studio's speakers speak; a phone in another city needs the **browser** to speak (Web Speech API) or nothing speaks. Under tokenisation the browser must de-tokenise BEFORE it can speak, so the key must be on the phone (§4). | fact | `server.py:500-555`, `speak.sh` |
| d4 | Acks (2026-09-09 lesson) land on the board within the seat's normal reaction time; the API adds < 1 s to a write. | SHOULD | lesson |

### 2(e) Auditability
| # | Requirement | Level | Basis |
|---|---|---|---|
| e1 | Every record carries `written_by` (the token's identity: Kam / Wednesday-cert / Tuesday-cert), `written_at` (server clock), and the record is **append-only**; rulings are new records that reference the card, never in-place edits (today `decision_queue.sh rule` mutates the card; `amend`/`withdraw` keep history in arrays). | MUST | Kam's rulings are load-bearing (ledger w=107 on copying the letter from the card) |
| e2 | Sign-in and API auth logs retained ≥ 90 days; a failed-auth alert reaches Kam (mail). | SHOULD | §5 |
| e3 | An export of the whole store (per client) is one authenticated call, so the local machines can re-ingest and the site is never the ONLY copy. | MUST | 2(f) |

### 2(f) The local machines stay the record — or do they?
**Position taken by this document:** the site is a *surface plus a transport*, and the seats' brains (`0_Brain/`, the streams, `decisions.json`) remain the record **for now** — but the honest measurement is that **the streams already leave the machines today** (GitHub holds every tracked stream; §1.3). The argument for keeping the machines as the record is not custody, it is *authority*: `chat_streams.py`'s single-writer-per-file rule, `decision_queue.sh`'s guards, `reconcile_rulings.py`'s seat scope are all local code that the fleet has debugged for two weeks. Moving authority to an Azure store means re-implementing those guards server-side and re-earning the trust. **Default: dual-write during the pilot (b6); the site becomes authoritative for the chat transport only when Kam rules it (§7 Q5), and `decisions.json` moves last.** The counter-argument, stated fairly: two writers to two stores is the exact shape that corrupted files on 09-08/09-09; the shortest safe path is to make the API the ONLY writer and have the seats `GET` their own streams back into local files as a mirror. This document recommends that shape as the END state, not the pilot.

## 3. Architecture options

All prices: **USD, region australiaeast, Consumption/pay-as-you-go, from Microsoft's Retail Prices API on 2026-09-21** (the azure.microsoft.com pricing pages rendered "$-" placeholders to the fetcher; see §8). "×730" = hourly rate × 730 h, this document's arithmetic, not a quoted monthly price. **No AUD figures were obtained** — unmeasured. Effort bands are this document's estimate in seat-days, unmeasured until the pilot.

### Cost building blocks (shared by the options)
| Component | Price as read | Monthly (×730 or as stated) | Source |
|---|---|---|---|
| App Service Linux F1 | USD 0.00/h | 0 — but **no custom TLS, no client certs** | S-2a |
| App Service Linux **B1** | USD 0.019/h | **≈ 13.87** | S-2a |
| App Service Linux P0v3 / P1v3 | USD 0.092/h / 0.184/h | ≈ 67.16 / 134.32 | S-2a |
| Container Apps Consumption | vCPU USD 0.000034/s, mem USD 0.000004/GiB-s, USD 0.40/1M req; **free grant 180k vCPU-s + 360k GiB-s + 2M req/month** | ≈ 0 for a polling dashboard within grant; scale-to-zero | S-2b |
| Static Web Apps Free / Standard | Free USD 0 (no custom auth, no SLA); Standard **unmeasured** | 0 / unmeasured | S-2c |
| Functions Consumption | free grant 1M executions + 400k GB-s/month | ≈ 0 | S-2d |
| Front Door Standard / Premium | base USD 35 / 330 per month; WAF managed rules Premium only | 35 / 330 | S-3a |
| Application Gateway WAF_v2 | USD 0.522/h fixed + 0.0144/CU-h | ≈ 381 + CUs | S-3b |
| App Service access restrictions (IP allow-list) | no charge stated | 0 | S-3c |
| Cosmos DB serverless | USD 0.285/1M RU; USD 0.2875/GB-month; free tier is provisioned-only | ≈ 1–3 at this volume | S-4a |
| PostgreSQL Flexible B1ms | USD 0.026/h compute | ≈ 18.98 + storage | S-4b |
| Table storage LRS / Blob Hot LRS | USD 0.0495 / 0.02 per GB-month | < 0.01 for 5 MB | S-4c |
| Key Vault Standard ops / Premium HSM key / Managed HSM | USD 0.03/10k ops / 1.00 per key-month / 3.20/h pool | < 1 / 1 / ≈ 2,336 | S-4d |
| Azure Relay Hybrid Connections | listener USD 0.0134/h; first 5 GB free then 1.00/GB | ≈ 9.78 + data | S-5a |
| Web PubSub Free | 1 unit, 20 connections, 20k msg/day | 0 | S-5b |
| Entra ID P1 (Conditional Access) | USD 7.00/user/month (yearly) | 7 for Kam alone | S-1b |

### Option A — Lift-and-shift: today's server behind App Service + Easy Auth (RECOMMENDED for the pilot)
| Aspect | Design |
|---|---|
| Components | Resource group → App Service **B1 Linux** (or Container Apps Consumption at ≈ 0 within the free grant, with the same built-in auth [S-2b]) running `server.py` refactored: data layer swapped from JSON files to a store; the 24 browser POST routes kept behind Easy Auth; the 6 seat routes (b4) added. Store: **Table storage** (rows keyed `PartitionKey=client`, `RowKey=stream|ts`) at ≈ 0, or Cosmos serverless if `since=` queries across streams need indexing. Key Vault Standard for the CMK and the seats' public certs. Custom domain + managed cert. |
| Identity / MFA (Kam) | Easy Auth, provider Entra ID, single-tenant, `WEBSITE_AUTH_AAD_ALLOWED_TENANTS` = the kreiser.org tenant [S-1a]; Kam is the only assigned user. MFA via Security Defaults (Free) or a Conditional Access policy (P1) [S-1b]. |
| API auth (seats) | Two app registrations (`wednesday-seat`, `tuesday-seat`), **certificate credential** each, client-credentials flow → token with app roles `seat.secuura+seat.wed` / `seat.datasec+seat.wed`; Easy Auth validates the token, the app enforces role→`client`. Alternative: App Service mTLS (`X-ARR-ClientCert`, exclusion paths, TLS 1.3/HTTP2 incompatible when required [S-2a mTLS]) — more moving parts than tokens; not recommended. |
| Data protection | TLS in transit; SSE at rest (default, free) + CMK in Key Vault [S-4e]. **No tokenisation**: the server, and therefore an Azure operator with data-plane access or a compromised app, can read prose. |
| Effort band | **≈ 2 seat-days** (1 for the API + store swap + `since=`; 1 for auth, roles, domain, R0 test, deploy). |
| Monthly cost band | **≈ USD 15–20** (B1 13.87 + storage/KV < 2) with free access restrictions instead of WAF; **≈ USD 50–55** with Front Door Standard; **+ USD 7** if P1 for Conditional Access. Container Apps variant: **≈ USD 1–10** (within grant + storage) but cold-start latency after scale-to-zero (unmeasured). |
| Does NOT solve | prose visible to the platform and to anyone who compromises the app (Q6); the whole 24-route browser surface must be re-audited for auth (today none of it has any); Kam's ISP/carrier IP allow-listing may be impractical on mobile (measure). |

### Option B — Tokenised store: field-level encryption under Kam's certificate, seats encrypt at write (§4 in full)
| Aspect | Design |
|---|---|
| Components | Everything in A, plus: an envelope format on every record (`ciphertext`, `wrapped_keys[{kid, wrapped}]`, `scheme`); a key registry in the store (Kam's device public keys, the seats' public keys); a device-enrolment page (WebCrypto `generateKey(extractable:false)` → CryptoKey stored in IndexedDB, public half uploaded [S-6a]) — or WebAuthn PRF so a passkey synced by iCloud Keychain [S-6c] derives the key on every Apple device (Safari 18/iOS 18 supports PRF for platform passkeys per third-party sources; the authoritative browser table is **unmeasured** [S-6b]); seat-side encryption in the `chat_reply.sh` / `decision_queue.sh` equivalents; browser-side decrypt + Web Speech for autoplay. |
| Identity / MFA (Kam) | as A. The MFA gate protects the ENVELOPES; the private key protects the PROSE — two independent factors, which is the point. |
| API auth (seats) | as A. Note: a stolen seat cert exposes that seat's metadata and lets an attacker WRITE forged envelopes; it does not expose the other seat's prose (R0 preserved even under credential theft — an improvement over A). |
| Data protection | prose unreadable to the server, the operator and a compromised app; metadata (`client`, `ts`, `view`, card ids, option letters, sizes) in the clear by necessity (§4.4 items 2–3); phone-with-key is the boundary. Cosmos DB "Always Encrypted" (client-side, SDK-level, .NET/Java/JS [S-4f]) is the platform's version of the same idea but keys would live in Key Vault, reachable from Azure — it does **not** satisfy "certificates on my machine". |
| Effort band | **≈ 7–12 seat-days** (A's 2 + 5–10 for envelopes, key registry, enrolment, multi-device wrap, rotation, encrypted attachments, autoplay path, recovery drill, seat-side encrypt + verify-by-decrypt). |
| Monthly cost band | **same as A** (crypto runs on the seats and the phone; no HSM needed — the private keys are on Kam's devices by design). |
| Does NOT solve | search by content; new-device access to history without re-wrap; the metadata leak (who is busy with which client, when); a stolen unlocked phone; key loss (mitigated only by keeping the local plaintext streams — b6). It also does not remove the plaintext already in GitHub today. |

### Option C — Zero-knowledge relay / tunnel: the panel stays on the Studio
| Aspect | Design |
|---|---|
| Components | **C1 (Azure-native):** Azure Relay **Hybrid Connections** — a listener process on the Studio opens an outbound 443 WebSocket to the Relay; no inbound ports [S-5a]; an Azure Function or small App Service in front does Easy Auth + forwards HTTP to the relay → `server.py` unchanged on 127.0.0.1:47787. **C2 (third-party):** Tailscale (mesh) or Tailscale Funnel / Cloudflare Tunnel [S-5c] — **conflicts with "hosted in the kreiser.org Azure tenant"**: the auth and edge live at a third party. |
| Identity / MFA (Kam) | C1: Easy Auth on the fronting app as A. C2: the mesh vendor's SSO/MFA. |
| API auth (seats) | unchanged — the seats keep writing local files and syncing through git; Tuesday still needs the Studio up. Nothing becomes an API. **This does not meet Kam's "both you and Tuesday interact with it through APIs."** |
| Data protection | cheapest data exposure: nothing is stored in Azure; the relay carries TLS-wrapped bytes transiently. |
| Effort band | **≈ 0.5–1 seat-day** (C1), ≈ 1 h (C2). |
| Monthly cost band | C1 ≈ **USD 10–25** (Relay listener 9.78 + fronting App Service B1 13.87 or Functions ≈ 0); C2 ≈ 0 on personal plans (Tailscale Funnel "available for all plans" [S-5c]; Cloudflare free plan **unmeasured**). |
| Does NOT solve | availability — the site is down whenever the Studio is (2(d) d2); the Tuesday-depends-on-the-Studio problem (2026-09-16 §9) stays exactly as it is; the 3.3 MB whole-log poll still crosses the WAN; the 24 unauthenticated routes are now internet-reachable behind one login (every one of them must still be audited). It is a **remote-access** answer, not the API-driven external site Kam described. |

### Option D — Static site + serverless API (Static Web Apps + Functions + Cosmos serverless)
| Aspect | Design |
|---|---|
| Components | SWA hosts `cockpit.html`; a Functions app (Consumption, within the 1M-execution free grant [S-2d]) exposes the 6 seat routes + Kam's browser routes; Cosmos serverless (≈ USD 1–3) or Table storage for the store; Key Vault for CMK/certs. |
| Identity / MFA (Kam) | SWA **Free tier has no custom authentication** — the Entra provider on Free is the pre-configured multi-tenant one; single-tenant/custom Entra needs **Standard**, whose price the fetcher could not read (**unmeasured**) [S-2c]. |
| API auth (seats) | Functions with Easy Auth / token validation as A. |
| Data protection | as A (TLS + SSE/CMK); B's envelope format can sit on top identically. |
| Effort band | **≈ 3 seat-days** — the Python server does not port; the API is rewritten as functions (Python Functions are fine, but the process model and cold starts differ; polling every 3 s from a phone is ~28,800 executions/day per open tab — within the 1M grant, but cold-start latency on Consumption is a first-paint cost, unmeasured). |
| Monthly cost band | **≈ USD 1–5 + SWA Standard (unmeasured)**. Likely the cheapest running cost with proper auth once Standard is priced; not the cheapest build. |
| Does NOT solve | anything A does not; adds a rewrite and a cold-start question. It changes the cost picture only if SWA Standard is priced well under B1 — check before choosing. |

### Comparison at a glance
| | A lift-and-shift | B field-level encryption | C relay/tunnel | D static + serverless |
|---|---|---|---|---|
| Meets "external website" | yes | yes | C1 yes / C2 no (third-party) | yes |
| Meets "seats via APIs" | yes | yes | **no** | yes |
| Meets "MFA in the tenant" | yes | yes | C1 yes / C2 no | Standard tier only |
| Meets "tokenised, certs on my machines" | no | **yes (as encryption)** | n/a (nothing stored) | no (B on top) |
| Up when the Studio is off | yes | yes | **no** | yes |
| R0 partition enforced server-side | yes | yes + survives credential theft | no (whole panel behind one login) | yes |
| Effort (seat-days, unmeasured) | ≈ 2 | ≈ 7–12 | ≈ 0.5–1 | ≈ 3 |
| Running cost (USD/month, australiaeast) | ≈ 15–20 (55 with Front Door) | same as A | ≈ 10–25 | ≈ 1–5 + unmeasured SWA Standard |
| What it leaves exposed | prose to platform/app | metadata; phone as boundary | Studio availability; all 24 routes | as A |

**Recommended shape:** **A now, with B's envelope format designed in from the first record** so that switching prose to ciphertext in Phase 2/3 is a scheme flag, not a migration. C is the fallback if Kam wants phone access this week with zero build; D only if SWA Standard turns out materially cheaper than B1 once priced.

## 4. The tokenisation question, answered directly

Kam: *"depending on the overhead and speed, one approach will be to tokenize all data and to have de-tokenization based on certificates that live on my machine or multiple machines."*

### 4.1 What "tokenise" means here — said plainly
Tokenisation in the payments sense replaces a value with a surrogate and keeps the real value in a **vault**; whoever holds the vault can de-tokenise. Kam's sentence puts the de-tokenising capability on **his machines, keyed by certificates**. Two readings:

1. **Vault-on-the-seats.** Each seat replaces message text with an opaque token, keeps the plaintext in a local vault (its own stream file — which it already has), and the site stores tokens. Kam's browser then needs to reach the vault to render — i.e. it needs a path back to the Studio/mini. That is **option C wearing a different hat**: availability tied to the machines, and the site shows nothing when they are down.
2. **Certificate-based de-tokenisation with no callback.** The token must be *self-contained*: the browser turns token → text using only a key on the device. A surrogate that can be reversed with a key and no vault lookup **is ciphertext**. So this reading is **field-level (client-side) encryption under a key Kam holds**, and the word "certificate" means the key pair whose public half the seats encrypt to and whose private half sits on Kam's devices. This is the reading that gives Kam what he asked for (external site, works when the Studio is off), and it is the one analysed below. **It is encryption, not tokenisation; calling it what it is matters because the failure modes (key loss = total loss; key on phone = phone is the boundary) are encryption's, not a vault's.**

### 4.2 How reading 2 would work end to end
| Step | Who | What |
|---|---|---|
| Key generation | Kam, once per device (or once, then distributed) | An asymmetric key pair (e.g. ECDH P-256 or RSA-OAEP) or a passkey-derived symmetric key. Public key published to the API as "Kam's current envelope key(s)". |
| Write | the seat | Generates a fresh per-message content key (AES-256-GCM), encrypts `text` (and `bluf`, `title`, option `label`/`detail`, attachment bytes), wraps the content key to **each** of Kam's public keys (one wrap per device), and POSTs `{client, stream, ts, view, kid[], wrapped_keys[], ciphertext}`. **`client`, `ts`, `view`, `role`, card `id`, option `key`s and `status` stay in the clear** — the server needs them to partition, route and reconcile (§4.4). |
| Store | the site | Stores the envelope. It can see: who wrote, when, which client, which card was ruled with which letter; it cannot see any prose. |
| Read | Kam's browser | Fetches envelopes since `ts`, unwraps the content key with the device's private key (WebCrypto `unwrapKey`), decrypts, renders, and — for autoplay — speaks via the Web Speech API. |
| Kam writes | Kam's browser | Encrypts his message to **the seats' public keys** (each seat has one — it already has a certificate for API auth; the same key pair or a second one) plus his own devices' keys, so the seats can read it and he can see his own history. |
| Rulings | Kam's browser | The button posts `{card_id, choice_key}` **in the clear** (the key is a letter; that is what `reconcile_rulings.py` already parses and what the seat needs without a decrypt step) plus an encrypted `note` if he types one. |

### 4.3 What the server can and cannot see under each protection level
| Protection | Server sees | Defends against | Does NOT defend against | Latency added per record | Dev effort | Ops complexity |
|---|---|---|---|---|---|---|
| **TLS only** (option A baseline) | everything | network eavesdropping | Azure operator with data-plane access; a compromised app; a leaked seat credential (reads whole partition); a stolen signed-in phone | 0 | 0 | 0 |
| **Server-side encryption at rest** (platform SSE, Microsoft-managed or customer-managed keys in Key Vault) | everything at request time; disks are encrypted | stolen disks / backups; with CMK, revoking the key makes the store unreadable to the platform going forward | anything that goes through the app (operator with app access, compromised app, leaked credential, stolen phone) — the app decrypts transparently | ~0 (platform) | 0–0.5 day (CMK wiring) | low; key rotation is a Key Vault setting |
| **Field-level encryption under Kam's keys** (reading 2) | metadata only: `client`, `ts`, `view`, `role`, card ids, option letters, sizes, who-wrote-when | Azure operator; compromised app **for prose**; a leaked seat credential exposes only that seat's own plaintext (which it already holds locally) and metadata | a stolen **unlocked** phone with the key on it (the key IS the boundary); metadata leakage (Secuura vs Datasec volume and timing are visible); key loss = everything written to that key is gone unless the local streams are kept (b6 keeps them) | write: 1 AES-GCM + N wraps (N devices) ≈ **single-digit ms**; read: 1 unwrap + 1 decrypt per record ≈ ms; **50-record first paint ≈ tens of ms of crypto** — bandwidth, not crypto, dominates on a phone (figures are order-of-magnitude reasoning, **unmeasured** on Kam's devices) | **the dominant cost: ~5–10 days** — key management UI, multi-device wrapping, rotation/re-wrap, encrypted attachments, Web Speech autoplay path, seat-side encrypt in `chat_reply.sh` / `decision_queue.sh` equivalents, a recovery drill | **high**: adding a device = re-wrap or forward-publish; losing a device = rotate; every renderer and every consumer that reads text (search, `kam_msgs.sh`, `reconcile_rulings.py` `note:` taps) must run where a key is |
| **Tokenisation with a local vault** (reading 1) | opaque tokens + metadata | same as above for prose at rest in Azure | the site shows nothing when the vault (Studio/mini) is unreachable — which is the availability Kam is buying; the vault callback re-introduces an inbound path to the machines | one round trip **to the Studio** per render batch (tens–hundreds of ms over WAN) | ~5 days + a tunnel | high; two systems (site + vault) to keep alive |

### 4.4 What breaks, or has to move, under field-level encryption
1. **Search and filtering by content** — impossible server-side; the browser can search only what it has decrypted (fine for "last 500 messages", not for "everything Kam ever said about mysql2").
2. **The `view` field must stay plaintext** — it is routing (2026-09-10 lesson); so must `client`, or the partition and R0 enforcement fail. This is metadata the server *must* see; state it so nobody later "hardens" it into the ciphertext and breaks Tuesday's delivery.
3. **Decision cards' option keys and `ruled_choice` stay plaintext** — the letter is what rules the card (ledger w=107) and what the seat parses without a key. The card's `title`, `bluf`, option `label`/`detail`, `ruling_note` are prose → encrypted. A card the server can partly see is the honest shape.
4. **Autoplay** — the Studio cannot speak what it cannot read; if the seats' streams are encrypted to Kam's keys only, the seat's own `spoken`/`/api/speak` path dies unless the seat also keeps plaintext locally (it does — b6) or messages are also wrapped to the seat's key. On the phone the browser speaks after decrypting; iOS Safari requires a user gesture before `speechSynthesis` will start (behaviour stated from general knowledge — **unmeasured**, verify in the pilot).
5. **Multiple machines** — "certificates that live on my machine or multiple machines" means N public keys; every write wraps to N keys (cheap) OR one key is synced across devices (a passkey-derived key via WebAuthn PRF syncs through iCloud Keychain on Apple devices — see §8 for the support status the fact-finder returned). Adding a new phone later means the seats must re-wrap history to it or Kam accepts that the new device sees only messages written after it was enrolled. The second is the cheap, honest default.
6. **The seats read each other's prose today through git** (`advance_other_streams()` pulls the other stream, though only `generate.py` and Kam's browser render it). Under encryption-to-Kam, a seat cannot render the other seat's text — which is **exactly R0** and an improvement, not a loss.
7. **Recovery** — losing every enrolled device loses every message written only to those keys. Mitigation: the local streams (b6) remain plaintext on the seats; a recovery key printed and kept offline; or a Key Vault-held escrow key (which re-introduces an Azure-side decrypt path and defeats the threat model — say no unless Kam wants it).
8. **Debugging** — a seat that mis-encrypts produces a card Kam cannot read and the server cannot inspect. Every write must be verified by decrypting it back with the seat's own key before the HTTP call returns (the fleet's always-verify rule, applied per record).

### 4.5 Verdict on overhead and speed
- **Speed:** crypto is not the bottleneck; bandwidth and the delta API are. A phone rendering 50 encrypted records costs milliseconds of WebCrypto; a phone downloading today's 3.3 MB whole-log poll costs seconds and data — fix b5 first, in any option.
- **Overhead:** the cost is **engineering and operational**, roughly 5–10 days against ~1–2 for option A, plus a permanent key-management duty that today does not exist. It defends against the Azure operator and a compromised app — threats Kam gets to decide he cares about, given the same prose already sits in a GitHub repo in plaintext today (§1.3).
- **Recommendation for the pilot:** option A with SSE/CMK and the R0 partition **first**, with the envelope format (§4.2) designed in from day one (`ciphertext` + `wrapped_keys[]` fields present, initially carrying plaintext under a "null" scheme), so field-level encryption is a switch-on in phase 2 rather than a rebuild. If Kam's threat model includes the Azure operator, phase 2 becomes mandatory and the doc's effort band moves to the higher figure.

## 5. Security must-haves regardless of option

| # | Control | Applies to | Why (basis) |
|---|---|---|---|
| S1 | **MFA on Kam's sign-in**, enforced by tenant policy. Conditional Access requires **Entra ID P1 (USD 7.00/user/month)**; on a Free tenant, **Security Defaults** enforce MFA registration + MFA "when necessary" + MFA for portal/CLI at no cost [§8 S-1b, S-1c]. Passkey / Authenticator number-match preferred over SMS. One licensed user (Kam) is enough for CA on his own sign-ins. | A, B, C, D | Kam's sentence |
| S2 | **Conditional Access extras if P1 is present:** named locations (Australia + travel), sign-in frequency, block legacy auth. **Device compliance additionally needs Intune** — not justified for one user [§8 S-1e]. Without P1 these are unavailable — a licensing fact, not a design choice. | A, B, D | §8 |
| S3 | **Single-tenant app registration** ("Accounts in this organizational directory only"), Easy Auth `WEBSITE_AUTH_AAD_ALLOWED_TENANTS` = this tenant, Kam's account the only assigned user (app-role assignment required) [§8 S-1a]. **No B2C / External ID** — B2C is closed to new customers since 1 May 2025 [§8 S-1d] and there are no external users: one human viewer (a5). | A, B, D | a5 |
| S4 | **Per-seat identity = app registration + certificate** (private key generated on the seat, stored in the login keychain or `3_Access_Keys/`, gitignored). **No client-secret strings** in `.env`. Two app roles: `seat.secuura`, `seat.datasec`; Wednesday's registration holds only the first, Tuesday's only the second; both hold `seat.wed`. The API maps role → allowed `client` values and rejects any body whose `client` is outside them (**R0 enforced server-side**, never by the caller's good behaviour). | A, B, C, D | hard rule 3; workspace rule 4's per-project SP scoping; R0 |
| S5 | **Kam's browser token carries the union claim**; nothing else does. Logs and error payloads never print another partition's prose. | all | c1, c5 |
| S6 | **Edge control.** Full WAF is expensive at this scale (Front Door Standard USD 35/month base with custom rules only; Premium USD 330/month for managed rules; App Gateway WAF_v2 ≈ USD 381/month fixed [§8 S-3a, S-3b]). **App Service access restrictions are free** [§8 S-3c]: allow-list Kam's ISP ranges + the seats' egress IP for `/api/seats/*`, deny-all default, and rely on Easy Auth as the real gate. Front Door Standard becomes justified only if Kam wants a global edge or the phone's carrier IPs make allow-listing impractical (likely — carrier NAT ranges are wide; measure in the pilot). | A, B, D | §8 |
| S7 | **TLS 1.2+ only, HSTS, custom domain** under kreiser.org so the phone never sees a `*.azurewebsites.net` name it might confuse with a phishing page. Custom TLS needs Basic tier or above [§8 S-2a]. | all | – |
| S8 | **Logging + alerting:** Entra sign-in logs, API access logs → Log Analytics, an alert to Kam's mail on (i) any sign-in from a new country, (ii) ≥ 5 failed API auths in 10 min, (iii) any 5xx burst. Retention ≥ 90 days. | all | e2 |
| S9 | **Append-only store semantics** with `written_by` from the token, never from the body. Rulings are new records. | A, B, D | e1 |
| S10 | **Encryption at rest with a customer-managed key in Key Vault** (SSE-CMK) even in option A — SSE itself is on by default and free; CMK adds Key Vault Standard operations at USD 0.03/10k [§8 S-4d, S-4e] and makes "revoke the site" a one-key operation. **Managed HSM (≈ USD 2,336/month) is not justified** at this scale; a Premium HSM-protected key is USD 1.00/key/month if Kam wants HSM-backed CMK. | A, B, D | §4.3 |
| S11 | **No secrets committed; tenant confirmed before any `az`**; the deploying identity is a NEW service principal scoped to ONE new resource group (`wednesday-dashboard-rg` or Kam's name), following the `*-claude-deploy` pattern; an authorization error is reported, never widened. Never-touch-prod: this resource group must not share a subscription with `datasec-sales-portal-rg` unless Kam says so. | all | hard rules 3, 4, 6, 7 |
| S12 | **Content export + delete path**: one authenticated call exports a client's partition; one deletes it. The 2026-09-08 note's §2(b)–(e) risks (unremediated findings, named third parties) do not go away because the site is private — the export/delete path is how Kam unwinds it if he changes his mind. | all | 2026-09-08 note |
| S13 | **The pilot carries NO client prose** (§6) until the R0 partition is verified by test: a Datasec-scoped token asking for Secuura rows must get 403 and an empty body, and that test runs before every deploy. | all | R0; always-verify |


## 6. Phased plan (pilot → metrics → review — the project's go-slow rule)

**Phase 0 — decisions (Kam, ≤ 1 day of his attention, no build).** Rule on §7 Q1–Q8. Confirm the tenant and its Entra licence tier (P1 or Free) by looking in the portal, not recalling. Pick the domain name.

**Phase 1 — 1-day pilot (option A shape, no client prose).**
- What is built: one resource group; one App Service Basic B1 Linux (≈ USD 13.87/month) running the existing `server.py` refactored into (i) an authenticated seat API with the six routes of b4 and the `client` partition, and (ii) the cockpit page served behind Easy Auth; one small store (Table storage at USD 0.0495/GB-month for ~5 MB is the cheapest; Cosmos serverless if query needs grow — §3); one Key Vault (CMK); two app registrations with certificates; app roles as S4.
- What is loaded: **synthetic records only** (`client: WED`, generated text) plus the real `usage_*.json` numbers, which carry no client content.
- What is measured (each written to the pilot note with the command that produced it): (m1) phone first-paint time for 50 records on mobile data; (m2) seat write latency p50/p95 from the `chat_reply.sh`-equivalent to HTTP 200; (m3) poll-to-visible latency with `since=`; (m4) the R0 test — Tuesday-role token requesting `client=Secuura` → 403, zero bytes of body; Kam's token → both; (m5) MFA prompt on a fresh browser — proven by a screenshot of the prompt; (m6) sign-in from a non-named location blocked (if P1) — proven; (m7) cost meter after 24 h from the portal's cost page; (m8) Web Speech autoplay on iOS Safari after a user gesture — works / does not.
- What is NOT done: no client rows, no DNS on the real domain until m4/m5 pass, no change to `panel_sync`/`chat_sync`, no `az` outside the new resource group.

**Phase 2 — review (Kam).** Read m1–m8. Decide: (i) stop (delete the resource group — one command, nothing else touched); (ii) go to real rows with dual-write (b6) for one client first — default Secuura, because Wednesday owns the Studio where the panel already lives; (iii) whether field-level encryption (§4) is required before real rows land, based on whether the Azure operator is in Kam's threat model (Q6).

**Phase 3 — real rows, dual-write, one client.** Seats write local file + API; Kam reads the site on the phone and the local page at the Studio; m1–m3 re-measured with real volumes for 7 days.

**Phase 4 — second client + rulings.** Tuesday's registration goes live; the decisions partition moves with the append-only ruling model; the ruling reconciler reads Kam's taps (with their `view`) from the API instead of the local file. R0 test re-run with real partitions before the first Datasec row lands.

**Phase 5 — authority.** Only if Kam rules Q5 = site: the API becomes the sole writer; seats mirror back to local files; git transport for the streams retired; panel_sync/chat_sync reduced to code sync.

Effort per phase is in the BLUF; each phase ends with a written measurement, and no phase starts without the previous phase's review recorded.


## 7. Open questions for Kam (numbered, each with the default this document will assume if he says nothing)

| # | Question | Default if silent |
|---|---|---|
| Q1 | **Which tenant is "the kreiser.org tenant"?** (a) Datasec environment #5 (`d500ebad-…`, controller `kreiser.org@me.com`, which holds Datasec dev/staging AND Vision Sales Portal production), or (b) a separate personal tenant of Kam's. If (a), Secuura content lands in a Datasec-controlled environment and hard rules 2/4 need an explicit override from Kam. | **(b)** — a personal tenant, id to be supplied; nothing is provisioned until it is. |
| Q2 | May Tuesday's Datasec rows live in the **same store** as Secuura's, partitioned by `client` with server-side claim enforcement — or must they be **separate deployments**? | **Same store, partitioned** (c4) — half the cost, and the merge already happens in Kam's browser. The 2026-09-08 note preferred separate sites; Kam decides. |
| Q3 | Which device de-tokenises/decrypts: **phone**, **laptop**, or **both** ("multiple machines")? Each enrolled device is a key the seats wrap to; the phone as key-holder makes the phone the security boundary. | **Both, enrolled explicitly**; new devices see only messages written after enrolment; local streams remain the plaintext fallback. |
| Q4 | **Budget band** for running cost (monthly, USD) and for build effort (days of seat time). | Running: **≈ USD 15–20/month** (B1 + storage + Key Vault, no WAF — §3 option A low band); build: option A ≈ 2 days; field-level encryption a separate ≈ 5–10-day decision. |
| Q5 | Do the **local machines remain the record**, or does the site become authoritative for the chat transport (and later the decisions store)? | **Local machines remain the record** through Phase 4; Phase 5 only on Kam's ruling. |
| Q6 | Is the **Azure operator / a compromised app** inside the threat model? (Yes → field-level encryption is mandatory before real rows; No → option A + SSE-CMK.) Note the same prose is in a GitHub repo in plaintext today. | **No** for the pilot; revisit at Phase 2 review with the measured overhead in hand. |
| Q7 | Domain: `dash.kreiser.org` (or his choice); DNS is in his hands. | `dash.kreiser.org`, DNS added only after m4/m5 pass. |
| Q8 | Is a **mesh** (option C — Tailscale-style) acceptable as the *interim* while the site is built, given it is a third-party service rather than "hosted in the Azure tenant"? | **No** — Kam asked for an external website; C stays a documented fallback. |
| Q9 | Does the tenant have **Entra ID P1** (Conditional Access) or is it Free (Security Defaults only)? Decides S1/S2 and whether "named locations" is available at all. | Free assumed; Security Defaults MFA; P1 for one user (USD 7/month) proposed if Kam wants named locations. |

## 8. Sources

All web sources were opened on **2026-09-21** by a research sub-agent (desk research only; no `az`, no cloud call). Money figures come from Microsoft's public Retail Prices API (`https://prices.azure.com/api/retail/prices`, unauthenticated, `armRegionName eq 'australiaeast'`, USD, Consumption) because the azure.microsoft.com pricing pages rendered "$-" placeholders to the fetcher. Repo sources are cited inline by path and line in §1.

### Identity
- **S-1a** App Service auth with Entra ID — single-tenant option, `WEBSITE_AUTH_AAD_ALLOWED_TENANTS`: https://learn.microsoft.com/en-us/azure/app-service/configure-authentication-provider-aad — quote: "WEBSITE_AUTH_AAD_ALLOWED_TENANTS application setting with a comma-separated list of up to 10 tenant IDs". Read 2026-09-21.
- **S-1b** Conditional Access requires P1: https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview — "Using this feature requires Microsoft Entra ID P1 licenses." Prices P1 USD 7.00, P2 USD 10.00, Entra Suite USD 12.00 user/month (paid yearly): https://www.microsoft.com/en-us/security/business/microsoft-entra-pricing. Security Defaults (free): https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults. Read 2026-09-21.
- **S-1c** Entra Free limits (50,000 objects; 250 per non-admin user; MFA via Authenticator at no cost): https://learn.microsoft.com/en-us/entra/identity/users/directory-service-limits-restrictions and the Security Defaults page above. Read 2026-09-21.
- **S-1d** Azure AD B2C closed to new customers 1 May 2025, supported to at least May 2030: https://learn.microsoft.com/en-us/azure/active-directory-b2c/faq. External ID first 50,000 MAU free: Entra pricing page above. Read 2026-09-21.
- **S-1e** Named locations = CA (P1); device compliance needs Intune: https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-assignment-network and the CA overview. Read 2026-09-21.

### Compute
- **S-2a** App Service Linux prices (F1 0.00; B1 0.019; P0v3 0.092; P1v3 0.184 USD/h, australiaeast): Retail Prices API filter `serviceName eq 'Azure App Service'`. Pricing page (rendered "$-"): https://azure.microsoft.com/en-us/pricing/details/app-service/linux/. mTLS / client certificates (Basic tier or above; `X-ARR-ClientCert`; `clientCertExclusionPaths`; TLS 1.3/HTTP2 incompatibility when required): https://learn.microsoft.com/en-us/azure/app-service/app-service-web-configure-tls-mutual-auth. Read 2026-09-21.
- **S-2b** Container Apps consumption prices and free grant: https://azure.microsoft.com/en-us/pricing/details/container-apps/ (+ Retail API); built-in auth: https://learn.microsoft.com/en-us/azure/container-apps/authentication — "uses the same authentication and authorization system as Azure App Service". Read 2026-09-21.
- **S-2c** Static Web Apps Free vs Standard (Free: no custom auth, no SLA; Standard price rendered "$-" → **unmeasured**): https://azure.microsoft.com/en-us/pricing/details/app-service/static/. Read 2026-09-21.
- **S-2d** Functions free grants (Consumption 1M executions + 400,000 GB-s; Flex 250,000 + 100,000 GB-s): https://azure.microsoft.com/en-us/pricing/details/functions/. Read 2026-09-21.

### Edge
- **S-3a** Front Door Standard USD 35 / Premium USD 330 base per month; managed WAF rules Premium only: https://learn.microsoft.com/en-us/azure/frontdoor/understanding-pricing. Read 2026-09-21.
- **S-3b** Application Gateway WAF_v2 USD 0.522/h fixed + 0.0144/CU-h (australiaeast): Retail Prices API filter `serviceName eq 'Application Gateway'`. Read 2026-09-21.
- **S-3c** App Service access restrictions (no charge or tier gate stated): https://learn.microsoft.com/en-us/azure/app-service/overview-access-restrictions. Read 2026-09-21.

### Data and keys
- **S-4a** Cosmos DB serverless USD 0.285/1M RU, USD 0.2875/GB-month (Retail API); free tier not available for serverless: https://learn.microsoft.com/en-us/azure/cosmos-db/free-tier and https://learn.microsoft.com/en-us/azure/cosmos-db/serverless. Read 2026-09-21.
- **S-4b** PostgreSQL Flexible B1ms USD 0.026/h (australiaeast): Retail Prices API filter `serviceName eq 'Azure Database for PostgreSQL'`. Read 2026-09-21.
- **S-4c** Blob Hot LRS USD 0.02/GB-month; Table LRS USD 0.0495/GB-month (australiaeast): Retail Prices API filter `serviceName eq 'Storage'`. Read 2026-09-21.
- **S-4d** Key Vault Standard ops USD 0.03/10k; Premium HSM RSA-2048 key USD 1.00/key-month; Managed HSM B1 pool USD 3.20/h (australiaeast): Retail Prices API filter `serviceName eq 'Key Vault'`. Read 2026-09-21.
- **S-4e** Storage SSE on by default, cannot be disabled, no cost; CMK in Key Vault / Managed HSM: https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption. Read 2026-09-21.
- **S-4f** Cosmos DB Always Encrypted (client-side; .NET/Java/JS SDKs; 1.0 packages): https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-always-encrypted. Postgres equivalent **not researched**. Read 2026-09-21.

### Relay / tunnel
- **S-5a** Azure Relay Hybrid Connections — outbound-only listener on 443, no inbound firewall ports: https://learn.microsoft.com/en-us/azure/azure-relay/relay-what-is-it and https://learn.microsoft.com/en-us/azure/azure-relay/relay-hybrid-connections-protocol; listener USD 0.0134/h, first 5 GB free then USD 1.00/GB (Retail API). Read 2026-09-21.
- **S-5b** Web PubSub Free tier (1 unit, 20 connections, 20k msg/unit/day, USD 0): https://azure.microsoft.com/en-us/pricing/details/web-pubsub/. Read 2026-09-21.
- **S-5c** (third-party) Tailscale Funnel — "available for all plans": https://tailscale.com/kb/1223/funnel. Cloudflare Tunnel — outbound-only `cloudflared`; free-plan existence **unmeasured** on the page read: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/. Read 2026-09-21.
- **S-5d** (context) VPN Gateway Basic USD 0.036/h; Bastion Basic USD 0.19/h, Developer SKU free: https://learn.microsoft.com/en-us/azure/bastion/bastion-overview + Retail API. Read 2026-09-21.

### Client-side cryptography
- **S-6a** WebCrypto `generateKey` `extractable:false` blocks `exportKey`/`wrapKey`; CryptoKey storable in IndexedDB: https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/generateKey and https://www.w3.org/TR/WebCryptoAPI/. iOS Safari-specific compat row **unmeasured** (MDN compat table did not render; Baseline "available since January 2020"). Read 2026-09-21.
- **S-6b** WebAuthn PRF extension: https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API/WebAuthn_extensions; https://developers.yubico.com/WebAuthn/Concepts/PRF_Extension/index.html; Safari/iOS 18 PRF for platform passkeys and Chrome shipping — **third-party/forum sources only** (https://developer.apple.com/forums/thread/782466; https://groups.google.com/a/chromium.org/g/blink-dev/c/iTNOgLwD2bI); authoritative browser-version table **unmeasured**. Read 2026-09-21.
- **S-6c** Passkeys sync via iCloud Keychain across Apple devices: https://developer.apple.com/passkeys/. Read 2026-09-21.
- **S-6d** No Microsoft document found stating an App Service client-certificate limitation on mobile Safari (**unmeasured**); Apple forum (third-party) notes iOS apps cannot use profile-installed certs: https://developer.apple.com/forums/thread/673140. Read 2026-09-21.

### Not sourced / stated from general knowledge (marked unmeasured in the text)
- iOS Safari requiring a user gesture before `speechSynthesis` starts (§4.4 item 4).
- Per-record WebCrypto latency figures ("single-digit ms", "tens of ms for 50 records") — order-of-magnitude reasoning, to be measured in the pilot (m1).
- Container Apps / Functions cold-start latency after scale-to-zero.
- All effort bands (seat-days).
- All AUD conversions (none made).

### Repo sources (read 2026-09-21, paths absolute under `/Volumes/DevMASTER/WEDNESDAY/`)
`2_Project_Files/dashboard/{server.py,serve.sh,collect.py,generate.py,chat.html,cockpit.html}` · `2_Project_Files/PORTS.md` · `2_Project_Files/tools/{chat_streams.py,chat_reply.sh,chat_push.sh,chat_sync.sh,panel_sync.sh,decision_queue.sh,kam_msgs.sh,reconcile_rulings.py}` · `2_Project_Files/voice/speak.sh` · `0_Brain/dashboard/data/*` (shapes and sizes only) · `1_Project_Definition/Architecture/2026-09-08_two-machine-fleet-and-one-shared-panel.md` · `1_Project_Definition/Architecture/2026-09-16_tuesday-vs-wednesday-structure.md` · `0_Brain/learnings/{2026-08-17_conversation-needs-a-stable-panel,2026-09-10_a-panel-message-is-a-record-not-a-string,2026-09-09_confirm-receipt-on-the-chat-board,2026-08-04_delegation-v2-observability,2026-08-13_shared-bus-tag-filter-or-leak}.md` · `/Volumes/DevMASTER/CLAUDE.md` (hard rule 4) · `/Volumes/DevMASTER/WEDNESDAY/CLAUDE.md`.
