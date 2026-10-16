# Feedback sweep 1: Datasec projects (2026-10-16)

Asked by Kam on the live board at 12:54:43 AEDT: *"as part of your startup process, and every time you renew your seat, check whether any of the projects have feedback items that have been added and categorize these as tickets and start actioning them."*

This is the first sweep. It was read-only: no Jira writes, no git writes, no `az`, no mail. I ran 5 research sub-agents in parallel and spot-checked their key numbers myself. Where a number comes from an earlier seat's record and was not measured again today, I say so.

## 1. BLUF

| Project | Where feedback lands | How it was read today | Unticketed or new since 10-09 |
|---|---|---|---|
| **MPS Calculator** | One JSON file per item on App Service `/home/data/feedback/` | B99 local copy (`.tools/qa-B99/feedback-items.json`) plus Jira JQL | **0 unticketed.** 4 items, all sent after 10-09, all ticketed or done. **UNMEASURED after 10-16 ~12:08 AEDT**: reading the hosted store needs `az` (a Kudu token) |
| **Security Composer** | Demo Postgres `pc.feedback_item`; the tracker is BACKLOG.md, not Jira | Records only (deploy-time DB counts plus BACKLOG grep) | **2 with no BACKLOG row by id** (`1061d219`, `d477d020`). **Live list UNMEASURED**: the GET writes audit rows, and the SELECT path needs `az`. Last count: 18 items (B147, 10-13) |
| **HPSM-POC** | Azure SQL `poc.feedback_item`, sent by Jira Automation webhook as `hp-feedback` issues | Jira JQL `labels = hp-feedback` | **0 in-app items unticketed** (5 issues, all Done). **1 off-app gap:** HPSMPOC-242, Paul's 7 Oct showcase feedback, still a placeholder. **1 BACKLOG-only words fix**, no Jira. Hosted store UNMEASURED (needs TOTP sign-in or `az`) |
| **HPSM** | No in-app channel (SOW-01 built no app); Jira project `HPSM` | Jira JQL | **0.** 41 issues; 0 created or updated since 10-09. Project dormant |
| **NexusAI** | Azure Files `settings.json['feedbackItems']` (share `nexusai-data`) | 2026-10-13 backup copy plus Jira JQL (`Feedback #N`) | **0 unticketed.** 9 items, newest 10-02. #6 is praise, no ticket needed. **UNMEASURED after 10-13 23:07**: `feedback-sweep.sh` needs `az` |
| **Vision Portal** | Prod Postgres `feedback` table plus email (Kam, CC Tuesday) | Live public GET `/api/feedback/report` | **1 open, unticketed:** #6 (2026-04-15), a "Social Media Engagement" tile request. Portal is paused |
| **Vision QuickQuote** | Azure Table `feedback` (`hpasqqstore`) plus email (Kam, CC Tuesday) | Records only (Tuesday's mailbox search 10-12, C-13) | **0 unticketed** (2 items, both done). **UNMEASURED since 10-12**: no mail read today; the table key has write rights |

**Two findings that go beyond feedback (for Kam):**
1. **Vision Portal `/api/feedback/report` answers with no sign-in on production.** It returns descriptions, admin notes and usernames. The sign-in fix is on branch `fix/feedback-report-auth-2026-09-22` (`8df198a`) and was never merged.
2. **Disclosure:** today's read of that endpoint ran the route's `CREATE TABLE IF NOT EXISTS` against the production database. The table exists, so it changed nothing, but it is not a pure read. Future sweeps should use the mailbox CC (or the endpoint once the sign-in fix lands), not this route.

## 2. Feedback store map

| Project | Store | Read command / endpoint (no secrets) | How to tell an item is already ticketed | Suggested watermark |
|---|---|---|---|---|
| MPS Calculator | App Service `app-mpscalc-showcase-u6agl3edszqvs` (`mpscalc-showcase-rg`), `/home/data/feedback/<id>.json` plus `attachments/<id>/` | Kudu `GET https://<scm>/api/vfs/data/feedback/` then `…/<id>.json` with an az bearer token (method in `Briefs/2026-10-13_B81_SEAT-R_read-kam-feedback-items-hosted.md:13-21`); app `GET /api/v1/feedback` (Administrator only) | Mapping in `Registers/2026-10-16_paul-review-items.md` §3 (FB-01..05 → MPSCALC-nnn). The app's `<id>.ticket.json` marker is never written (MPS-9: no hosted Jira) | `submittedAt` (UTC) plus `feedbackId`. Last seen: `2026-10-14T17:29:06Z` / `4a906c0d` |
| Security Composer | Demo Postgres `pc.feedback_item`, `pc.feedback_attachment` (`apps/api/src/routes/feedback.ts`) | `GET /api/feedback?tenant_id=<t>` per tenant (platform-admin bearer; **writes `feedback.listed` audit rows**). Clean read: SELECT through `az vm run-command` (needs az) | A BACKLOG.md row quoting the 8-character `feedback_id`, or a CLARIFICATIONS C-number. There is no Jira. The app's `status` field is not reliable | `created_at` plus `feedback_id`. Last known: `1061d219` @ 2026-10-06T22:52:19Z |
| HPSM-POC | Azure SQL `poc.feedback_item` → Jira Automation webhook → `hp-feedback` issue plus mail | Jira `project = HPSMPOC AND labels = hp-feedback`; app `GET /api/v1/feedback?limit=100` (Admin, TOTP sign-in) | A matching `hp-feedback` issue exists. In-app `delivery.state=sent` does **not** prove delivery (HPSMPOC-109) | Jira `created` on `hp-feedback`. Last: HPSMPOC-230 @ 2026-10-07T08:46 |
| HPSM | None in-app; Jira `HPSM` (board 539; credential variable is `JIRA_SITE`, not `JIRA_BASE_URL`) | Jira `project = HPSM` | Not applicable | Jira `updated`. Last: HPSM-41 @ 2026-09-30 |
| NexusAI | Azure Files `stnexusaidmjy25ipoih5eo/nexusai-data/settings.json` → `feedbackItems` | `2_Project_Files/scripts/feedback-sweep.sh`: read-only on the store and Jira, but uses `az storage file download --auth-mode key`. Call it by absolute path; CLAUDE.md's `cd` form is refused by the cd hook | Jira `project = RD AND text ~ "\"Feedback #<id>\""`; newer tickets also carry the `feedback` label | Top-level `feedbackItems_updated_at` (2026-10-02T05:24:24Z) plus max `id` (10) |
| Vision Portal | Prod Postgres `feedback`; emails to Kam plus CC tuesday-agent@; hourly digest inside the container | `GET https://datasec-sales-portal.azurewebsites.net/api/feedback/report` (open and in-progress only; see the warning above). `coordinator-state` needs a secret that is not in 4_Credentials | A `VSP-` key in `admin_notes` / `triage_notes`, or a Jira title match | `feedback.id` (max open id seen: 6) plus `created_at` |
| Vision QuickQuote | Azure Table `feedback` in `hpasqqstore`; emails to Kam plus CC tuesday-agent@ (since 2026-09-22) | **Tuesday's own mailbox:** subject contains `QuickQuote feedback (`. `GET /api/feedback` needs sign-in plus advanced mode, which writes session rows | Entry in `Quoting Tool/hpas-quoting-tool/BACKLOG.md`, a branch, or a C-number (not Jira) | Mail received time / message id. Table: `createdAt` (RowKey is reverse-time) |

## 3. Items per project

### MPS Calculator
Instrument: `python3 -I` `len(items)` on `.tools/qa-B99/feedback-items.json` gives **4**; Tuesday re-ran it and also got 4. The store holds 4 item files and 0 ticket markers (B99's Kudu read, `Briefs/2026-10-16_B99_STATUS.md:45-48`, not repeated today). The Jira JQL `key in (MPSCALC-113,138,161)` returns 3, all in Backlog.

| Ref | id / sent (AEDT) | Summary | Category | Ticket |
|---|---|---|---|---|
| FB-01 | `fee1b329` 10-13 11:57 (Kam) | Add a 7th home tile to fill the row | UX | Done (C-27); related MPSCALC-113 |
| FB-02 | `fee1b329` (same item) | Let the feedback button take file uploads | feature | Done (C-28, B83, #39, deployed) |
| FB-03 | `22091419` 10-14 17:52 (Paul) | Delete a quote from the list | feature | MPSCALC-161 (archive, not delete; K-16 open for Kam) |
| FB-04 | `8c6039d8` 10-15 04:26 (Paul) | Duplicate home tiles, with a screenshot | bug | MPSCALC-138 |
| FB-05 | `4a906c0d` 10-15 04:29 (Paul) | New home tile order, with a screenshot | UX | MPSCALC-138 |

Note: the 27 tickets labelled `feedback-sweep` (MPSCALC-162..188, JQL `labels = feedback-sweep` → 27) came from BACKLOG rows, not from in-app feedback.

### Security Composer
Instrument: the count of **18** comes from deploy-time DB counts in `vm-state_*.txt` (B97 10-07 through B147 10-13). It is a record, not re-measured today. I re-ran the BACKLOG check with `grep -c <id> BACKLOG.md`.

| id / date (UTC) | Summary | Category | Ticket |
|---|---|---|---|
| FB-1..FB-5 (`2893c2d1` `879266d7` `c37b782c` `5eb2cdce` `479c0193`), 09-26 / 10-03 | Guided start, engagement visibility, first-screen guide, Expert button placement, Discovery key box | feature / UX / bug | BACKLOG #88–#92 |
| K1–K7 (`12e7c6b5` `6648b421` `22757244` `4d167897` `eacce3d6` `fddd0f50` `e2270d88`), 10-06 | Remove the Guided view, main page, burger menu, approver membership, target/policy dropdown, empty prior-engagements list | feature / UX / bug | #213–#218, #224 |
| `2fb13337` 10-06 22:43 | Home page at 100% width | UX | #274 (deployed) |
| `356b5c65` 10-06 22:45 | Screens don't explain the HPSM / policy mapping | words | Quoted in gate note #284 only; no row of its own |
| `8b0dc2da` 10-06 22:46 | "HPSM" wording, check every screen | words | Quoted in row #272 (B102 FOUND §6) |
| **`1061d219`** 10-06 22:52 | Rename to "Policy Designer" | words | **No BACKLOG row** (grep → 0). Ruled in C-62 |
| **`d477d020`** ~10-06 | Editions lookup | feature | **No BACKLOG row** (grep → 0). B104's brief says it waits for Kam |
| (unrecorded id) 09-14 | Test item | n/a | Not real feedback |

**To ticket:** `1061d219` (words, has a ruling, needs a row to track it) and `d477d020` (feature, needs Kam). Nothing dated after 10-09 is known, and nothing after 10-13 has been measured.

### HPSM-POC
Instrument: Jira JQL `project = HPSMPOC AND labels = hp-feedback` → **5** (isLast true). `created >= "2026-10-09"` → 16, with none labelled `hp-feedback`. Hosted admin shows 3 items, all Sent (`Briefs/2026-10-16_B249_STATUS.md:144-146`, a record).

| Ref | Date | Summary | Category | Ticket |
|---|---|---|---|---|
| HPSMPOC-102, -103 | 09-29 | Synthetic route tests | n/a | Done |
| HPSMPOC-190 | 10-03 | Layout idea | UX | Done |
| HPSMPOC-221 | 10-06 | Narrative report error | bug | Done |
| HPSMPOC-230 | 10-07 | Deploy test | n/a | Done |
| **HPSMPOC-242** | 10-08 | Paul's 7 Oct showcase feedback: placeholder, nothing written down | question | Exists but empty, `needs-kam` |
| **Reset demo words** | B221 | Hosted "Reset demo" success message says "offline demo" | words | **BACKLOG.md:49 only, no Jira** |
| Steve DBS notes | 10-16 | 24 + 8 points in `Registers/2026-10-16_steve-dbs-notes.md` (branch `records/b250`, not yet on main); tone-rule question for Kam | words / question | No ticket (by design, B250) |

The match of the 3 hosted items to -190, -221 and -230 is inferred, not matched by id. I quote nothing from the HP mail.

### HPSM
Instrument: Jira JQL `project = HPSM` → 41; `… AND (labels ~ feedback OR summary ~ feedback)` → 0; `created >= "2026-10-09"` → 0; `updated >= "2026-10-09"` → 0.

Possible gap: Kam's 10-16 instruction to review Steve's DBS notes "for the HPSM - POC and HPSM project". It was filed for HPSM-POC only. Category: question. No HPSM ticket.

### NexusAI
Instrument: a Python read of `feedbackItems` in `4_Credentials/demo-share-backup-2026-10-13-s96o-pre-3907c57/settings.json` → **9 items, 0 dated on or after 10-09**. Read-only Jira JQL per id (controls: `project = RD` returns 50; a made-up phrase returns 0). `labels in (feedback,user-feedback)` → 5.

| id | Date | Summary | Category | Ticket |
|---|---|---|---|---|
| #2 | 05-07 | Job History filters | bug | RD-126, Done |
| #3 | 05-07 | Risks severity filter | UX | RD-127, Done |
| #4 | 09-01 | SCIM / business units | feature | RD-135, Testing |
| #5 | 09-04 | Prints per department | feature | RD-400, To Do |
| #6 | 09-04 | Praise for the new UI | n/a | Mentioned on RD-125 only (no action needed) |
| #7 | 09-04 | Colour % cost report | feature | RD-401, To Do |
| #8 | 10-02 | Sustainability tab: right-align | UX | RD-840, Release Ready |
| #9 | 10-02 | Eye icon → circled i | UX | RD-841, Release Ready |
| #10 | 10-02 | Fax/scan data | feature / data | RD-842, To Do |

### Vision Portal and QuickQuote
Instrument: live `GET /api/feedback/report` (HTTP 200, `generated_at` 2026-10-16T01:58:34Z) → **1 open item**. Jira VSP JQL `created >= -7d` → 0; `updated >= -7d` → 0. QuickQuote count of **2** is from Tuesday's 10-12 mailbox search (C-13; history lines 2171–2172), a record.

| id / date | Summary | Category | Ticket |
|---|---|---|---|
| **Portal #6** 2026-04-15 | Add a 4th dashboard tile, "Social Media Engagement" (needs info: 4 questions to Kam) | feature | **None** (no VSP key in notes; JQL "social media" / "tile" → 0) |
| QQ 2026-10-09 (John Spears) | Add CAD currency | feature | Done (C-14, v2.34 live 10-12) |
| QQ (earlier) | MFPs/SFPs label | words | Done (v2.31, C-04) |

Follow-ons that are not feedback items themselves: the stale AUD rate is on branch `backlog/qq-aud-seed-2026-10-12` (not merged), and three USD labels stay on screen for other currencies (QuickQuote BACKLOG:94).

## 4. Not measured

- **MPS hosted store after 10-16 ~12:08 AEDT.** Needs `az` (Kudu token). The app's admin GET needs an Administrator login, and none is in 4_Credentials.
- **Composer live feedback list.** The GET writes audit rows, and the read-only SELECT needs `az vm run-command`. Friday's 9 Oct census file was not found (it is only quoted in the B102 and B104 briefs). No count exists after B147 (10-13).
- **HPSM-POC hosted store.** Needs a TOTP demo sign-in or Azure SQL via `az`. The local checkout is 152 commits behind `origin/main`, so the code was read through `git grep origin/main`.
- **NexusAI live share after 10-13 23:07.** `feedback-sweep.sh` uses `az storage`. Item #1 is missing from the store; I did not look into why.
- **Vision Portal** closed or dismissed items, and coordinator-state (the secret is not in 4_Credentials). No DB access and no `az`.
- **Vision QuickQuote after 10-12.** No mail read today. The table key carries write and delete rights. Items from before 2026-09-22 are visible to Kam only.

**For a standing boot sweep:** every live store except the Vision report sits behind `az` or an app sign-in that writes. The cheapest truly read-only signal for MPS, NexusAI, QuickQuote and Portal is the tuesday-agent@ CC mail (where it is wired), plus each project's own Jira JQL with `created >= <watermark>`. Wiring the CC for MPS, Composer and HPSM-POC would close the gap; that is a decision for Kam.
