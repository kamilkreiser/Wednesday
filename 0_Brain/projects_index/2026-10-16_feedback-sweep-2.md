# Feedback sweep 2: Datasec projects (2026-10-16)

Second sweep of the day, run by a read-only sub-agent for Tuesday at **16:18 AEDT (05:18Z)**. Watermark: **2026-10-16 12:58 AEDT (01:58Z)**, the end of sweep 1 ([[2026-10-16_feedback-sweep-1]]). Window covered: 01:58Z to 05:18Z.

Read only: no Jira writes, no comments, no git writes, no mail sends, no `az`, no Kudu, no database access, and **no HTTP to any production or hosted app host**. The only network reads were the AgentMail list call for tuesday-agent@ and each project's own Jira REST search (`/rest/api/3/search/jql`, paginated until `isLast`).

## 1. BLUF

**0 new feedback items found since 12:58 AEDT. 0 unticketed.** Every live in-app store is still unmeasured (they all need `az` or a sign-in that writes), so "0" means "0 reached the read-only signals", not "0 in the stores".

| Project | New items since 12:58 | Unticketed | Instrument |
|---|---|---|---|
| MPS Calculator | 0 in Jira; store **UNMEASURED** | 0 known | Jira JQL (below) + mailbox. Hosted store needs `az` (Kudu token) |
| Security Composer | **UNMEASURED** | 0 new known (sweep 1's `1061d219`, `d477d020` still unrowed, not re-checked) | No Jira; store needs `az vm run-command`, and the GET writes audit rows |
| HPSM-POC | 0 | 0 | Jira `labels = hp-feedback` (total 5, unchanged); hosted store UNMEASURED (TOTP or `az`) |
| HPSM | 0 | 0 | Jira (no in-app channel) |
| NexusAI | 0 in Jira; store **UNMEASURED** | 0 known | Jira `Feedback #` search; share needs `az storage` |
| Vision Portal | 0 in mailbox; store **UNMEASURED** | 0 new (sweep 1's Portal #6 still stands) | Mailbox CC only. The report GET is production and was not called |
| Vision QuickQuote | 0 | 0 | Mailbox CC (`QuickQuote feedback (`): no such subject after 01:58Z |

## 2. Instruments

### AgentMail (tuesday-agent@agentmail.to)
`GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, one page. It fetched 100 messages; the oldest was 2026-10-13T01:21Z, so the whole window is covered without a second page. **39 messages after 01:58Z** (newest 05:14:29Z). Every one is fleet mail: `[Datasec/... -> Tuesday]`, `[QA/... -> Tuesday]`, `[Wednesday -> ...]` (sent by Tuesday) or Wednesday's reply. **None has a feedback-notification subject** (no `QuickQuote feedback (`, `Portal feedback`, MPS or Composer feedback notification).

Fleet mail that touches feedback but is not a feedback item (listed so the next sweep does not re-check it):
- 02:00:02Z MPS `QUESTION: feedback rate limit number (MPSCALC-174)`: build work on the feedback feature.
- 03:09:40Z and 03:42:19Z MPS B106 lane H: MPSCALC-174 and -177 ready.

### Jira (project timezone Australia/Melbourne = AEDT for every profile used; JQL uses `"2026-10-16 12:58"` local)

| Project (creds) | JQL | Total (paginated to `isLast`) |
|---|---|---|
| HPSMPOC (HPSM-POC `.env`) | `project = HPSMPOC AND labels = hp-feedback` | 5 (same as sweep 1; newest HPSMPOC-230, 10-07) |
| HPSMPOC | `… labels = hp-feedback AND (created >= W OR updated >= W)` | 0 |
| HPSMPOC | `project = HPSMPOC AND created >= W` | 0 |
| HPSMPOC | `… (summary ~ feedback OR labels in (feedback, hp-feedback, user-feedback)) AND updated >= W` | 0 |
| MPSCALC (MPS `.env`) | `project = MPSCALC AND created >= W` | 0 |
| MPSCALC | `… (summary ~ feedback OR labels in (feedback, user-feedback, in-app-feedback)) AND updated >= W` | 2: MPSCALC-174, -177 (see below) |
| RD (NexusAI `.env`) | `project = RD AND summary ~ "\"Feedback #\"" AND (created >= W OR updated >= W)` | 0 (control without the date clause: 21) |
| RD | `project = RD AND created >= W` | 1: RD-848, a Dockerfile CI item, not feedback |
| RD | `… labels in (feedback, user-feedback) AND (created >= W OR updated >= W)` | 0 |
| HPSM (HPSM `.env`) | `project = HPSM AND (created >= W OR updated >= W)` | 0 |

MPSCALC-174 (feedback hardening: rate limit, 401 handling) and MPSCALC-177 (feedback pill covers content at 390 px) were **created 12:29 AEDT, before the watermark**, and carry the `feedback-sweep` label: they come from BACKLOG rows about the feedback feature, not from in-app feedback. They only matched because they were updated (14:08, 15:03) by the B106 lane H work. Not new feedback items.

## 3. New items

None. No id, time or ticket to report.

## 4. Not measured (unchanged from sweep 1)

- **MPS hosted store** `/home/data/feedback/`: needs `az` (Kudu token). Last seen item `4a906c0d` (2026-10-14T17:29Z).
- **Composer** `pc.feedback_item`: needs `az vm run-command`; the API GET writes `feedback.listed` audit rows. No count since B147 (10-13). Not re-checked this sweep: whether `1061d219` and `d477d020` now have BACKLOG rows.
- **HPSM-POC** `poc.feedback_item`: needs TOTP sign-in or `az`. Jira only shows items whose webhook fired (HPSMPOC-109: `sent` is not proof).
- **NexusAI** share `settings.json`: needs `az storage`. Last known 10-13 23:07.
- **Vision Portal** prod Postgres: no DB, and the report route is production (out of bounds). Mailbox CC is the only signal.
- **Vision QuickQuote** Azure Table: the key has write rights; mailbox CC is the only signal. Note QuickQuote v2.36 went live 04:23Z today; it does not change the feedback path as far as the mail says (not verified in code).

**Watermarks:** advance the mailbox watermark to **05:14:29Z** (newest message read) and the Jira watermarks to **16:18 AEDT**. The store watermarks do not move: nothing was read from the stores.
