# TRMNL "Kam view": design (2026-10-09)

**Status:** designed and drafted, not published. No TRMNL write endpoint was called and nothing was installed outside `2_Project_Files/trmnl/`.
**Drafts:** `2_Project_Files/trmnl/` (markup.liquid, build_payload.py, push.sh, README.md, trmnl-push.plist.template, _preview/).

## BLUF
- **Shape.** Build one private plugin with the **Webhook** strategy. Its **full**-layout markup draws the two halves itself as a 2-column grid. It is not a mashup of two plugins.
- **Data path.** Every 15 minutes a launchd job runs `build_payload.py`, which reads the dashboard's existing JSON. `push.sh` then POSTs about 1.3 KB to the plugin's webhook. The webhook limit is 5 KB, and our worst case is 1.8 KB at the default caps.
- **Display limits.** The device redraws on TRMNL's schedule, every 15 minutes by default, so the list is near-live but not real-time.
- **Measured now.** Only **two of the three calendars are live**: the Secuura feed has returned HTTP 404 since 2026-08-28. Open actions per seat are **Wednesday 0 · Tuesday 1 · Friday 0**.
- **Kam's call.** This sends Datasec/Secuura meeting titles to TRMNL's cloud. That is his decision. Per-calendar redaction is built in.

## 1. TRMNL facts (primary sources)
| Fact | Source |
|---|---|
| You need the Developer add-on. Path: device picker → gear → "Developer perks" (one-time). Then Plugins → search "Private Plugin" → Name, Strategy → **Save**, then **Edit Markup**. | https://help.trmnl.com/en/articles/9510536-private-plugins |
| Strategies are **Webhook**, **Polling** (TRMNL fetches URLs you list) and **Plugin Merge**. That article does not name a "Static" strategy. | same |
| Webhook URL is `https://trmnl.com/api/custom_plugins/<Plugin Settings UUID>`. You POST JSON `{"merge_variables":{…}}`. Without Developer edition the API returns 403. | https://docs.trmnl.com/go/private-plugins/webhooks |
| Size limit: **5 KB** (TRMNL+: 10 KB). An oversized payload returns 422. | same |
| Rate limit: **12 posts/hour** (TRMNL+: 30). Faster posts return 429. | same |
| Default merge **replaces** the stored variables. `deep_merge` and `stream` are optional. | same |
| If the plugin hasn't refreshed in 15 minutes, new data renders right away. Otherwise it waits for the next scheduled refresh. | same |
| Accounts have a **15-minute minimum refresh** by default (5 minutes with TRMNL+). With one plugin on a 5-minute playlist, a new screen is generated only every third time. | https://help.trmnl.com/en/articles/10113695-how-refresh-rates-work |
| Mashup layouts (`1Lx1R` and others) combine **separate plugins**, each as a `view--half_vertical` and so on. A single plugin uses `view--full`. | https://trmnl.com/framework/docs/3.4/mashup |
| The platform wraps your markup in the `view`. You supply `layout` (exactly one) and an optional `title_bar` sibling. | https://trmnl.com/framework/docs/3.4/view , /layout |
| OG screen is **800×480, 1-bit** (a 2-bit OG variant exists). TRMNL X is 1040×780 at 4-bit (16 greys). | https://trmnl.com/framework/docs/3.4/screen , /devices |
| Classes used: `grid grid--cols-2`, `flex flex--col`, `table table--small`, `item`, `progress-bar` (`track`/`fill` with inline width), `label--inverted`, `title_bar`. | /grid /flex /table /item /progress /label /title_bar (all under trmnl.com/framework/docs/3.4/) |
| Overflow engine: `data-overflow`, `data-overflow-counter`, `data-table-limit`. | /overflow, /table |
| `trmnlp` local preview: `trmnlp init` / `serve` on :4567, no login for serve. It needs **Ruby ≥ 4.0** (gem) or Docker. The shell template loads `https://trmnl.com/css/<v>/plugins.css` and `/js/<v>/plugins.js`. Latest framework is 3.4.0. | https://github.com/usetrmnl/trmnlp (README, `lib/trmnlp/framework_version.rb`, `web/views/render_html.erb`), trmnl-framework `db/data/framework_versions.yml` |

**Why one full plugin and not a mashup.** In a mashup, each half is its own plugin with its own data. We would need two private plugins, two webhooks and two pushes against two 12-per-hour budgets, plus a mashup playlist item. One full view gives us one payload and one push. The two-column layout is just a grid inside the `layout`.
**Why Webhook.** Polling needs a public HTTPS endpoint that TRMNL can reach. The dashboard is 127.0.0.1-only by policy (`2_Project_Files/dashboard/serve.sh:3`, PORTS.md). Plugin Merge only exposes other TRMNL plugins' data. A webhook needs only outbound HTTPS from the Mac, and 4 posts/hour sits well inside the 12/hour limit.

## 2. Data map (measured in this tree)
| Panel | Source file | Generator · cadence | Fields used | Transform |
|---|---|---|---|---|
| Meetings: **Datasec** | `data/datasec_calendar.json` | `collect.py:223-239` (Graph `calendarView`, 8 days, `Prefer: outlook.timezone="Australia/Sydney"`) | `start` (naive Sydney), `title`, `allday` (`location` is available but unused) | Naive time is treated as local, as in `generate.py:322-323` |
| Meetings: **Secuura** | `data/secuura_calendar.json` | `collect.py:197-200` (Google secret ICS, 8 days, RRULE expansion) | `start` (with offset), `title`, `allday` | **Currently DEAD**: data `collected_at` is 2026-08-28. `secuura_error.json` says `HTTP Error 404` at 2026-10-09 12:56 |
| Meetings: **Personal** (iCloud: Family, KREISER.org, Amelia, Eventbrite… filtered by `ICAL_CALENDAR_NAMES`, `collect.py:42`) | `data/personal_calendar.json` | `collect.py:38-44` via `tools/calendar_probe.swift:25-26`, which covers today 00:00 plus **8 days** even though the key is named `events_next_48h` | `cal`, `title`, `start` (UTC Z), `allday` | Family is shown as group `F`, as in `generate.py:329-330` |
| (all calendars) | `layout.json` `hidden_groups`, `archived.json`, `muted.json` | dashboard UI | keys `src\|title` | Hidden and archived items are dropped, as in `generate.py:332-333`. Muted items are dropped by default (`--keep-muted` keeps them) |
| Agent gauges | `data/usage_{wednesday,tuesday,friday}.json` | each seat's `tools/statusline_publish.sh:82`, `.rate_limits.seven_day.used_percentage`, written on statusline ticks | `pct`, `resets_in`, `ts` | Marked stale when age ≥ 900 s (`cockpit.html:421`); the age is shown |
| Needs you | `data/decisions.json` (653 cards) | `tools/decision_queue.sh` (add/rule/withdraw) | `status`, `seat`, `client_project`, `id`, `title`, `ts`, `default_action` | See predicate below |

All three calendar feeds are refreshed by the loop in `dashboard/serve.sh:26-30`, which runs collect + generate every **300 s** but only while the dashboard server is running. That loop discards collect's stderr (`>/dev/null 2>&1`). No feed carries an **end time**: `collect.py` drops `DTEND`/`end` and the probe never emits it.

**"As on the chat cockpit"** means the **7-day plan usage %**, not context %. The cockpit chip renders `" — " + pct + "%"` (`cockpit.html:429-446`) from `/api/usage` (`server.py:221-250`).

**Needs-Kam predicate** (one row per card):
`status == "open"`. This is the cockpit's own NEEDS-YOU test (`cockpit.html:1078`). Ruled and withdrawn cards are excluded.
**Seat:** `seat == "friday"` gives Friday. Otherwise a Datasec client or a Datasec id-prefix gives Tuesday, and everything else gives Wednesday (`reconcile_rulings.py:91-125`).
**Row contents:** seat · title (clipped to 60) · since (`ts`) · "If ignored:" plus the first sentence of `default_action` (clipped to 40).
The cockpit also promotes unanswered agent QUESTIONs into "Needs you" (`cockpit.html:1284-1287`). Those are badged "needs Wednesday" (`cockpit.html:1011`), so they are deliberately **excluded** here: they are Wednesday's to answer, not Kam's.

**Measurement, 2026-10-09 ~13:10 AEDT:**
- Status counts: 1 open, 627 ruled, 25 withdrawn, 653 in total.
- Open per seat: Wednesday 0 · Tuesday 1 (`nexusai-rd774-free-form-sql-1008`, since 8 Oct 08:53) · Friday 0.
- Control: applying the same seat function to all cards gives every seat a non-zero count (Wednesday 297 · Tuesday 150 · Friday 206 = 653), so a 0 is not a dead predicate.
- Cross-check: `/Volumes/DevMASTER/TUESDAY/…/decisions.json` also has 0 open, but that file is stale (last written 2026-09-25).

## 3. Payload
```json
{"merge_variables":{
  "updated":"Fri 9 Oct 13:12",
  "days":[{"label":"Today · Fri 9 Oct","events":[{"time":"18:30","src":"F","title":"Dads dinner","now":false}]}],
  "cal_more":8, "cal_total":15, "cal_warn":["Secuura feed stale since 2026-08-28"],
  "agents":[{"name":"Wednesday","pct":17,"resets":"6d 19h","stale":false,"age":"1m"}],
  "actions":[{"seat":"Tuesday","title":"RD-774: NexusAI runs SQL text sent by the browser — choose…","since":"8 Oct 08:53","dflt":"nothing in the product changes, #70 stays…"}],
  "actions_more":0, "action_counts":{"Wednesday":0,"Tuesday":1,"Friday":0}, "actions_total":1}}
```
- `src` is D (Datasec), S (Secuura), P (Personal) or F (Family).
- `now` means a timed event that started within the last 60 minutes. That is an approximation, because no feed has end times.
- Feeds whose `collected_at` is older than 3 h are **not shown** and produce a `cal_warn` line instead.

**Sizes (compact JSON, measured with `build_payload.py --measure`):**
| Case | Size |
|---|---|
| Today, defaults | **1,258 B** |
| `--keep-muted` with caps at 40 | 2,016 B |
| `--redact datasec,secuura` | 1,258 B (today no Datasec event lands inside the row budget, and Secuura is stale, so nothing changes) |
| Planted worst case at the defaults (11 rows, 3 actions, maximum-length titles) | **1,756 B** |

The limit is 5,120 B. `build_payload.py` refuses with exit 3, sending nothing, if `--limit` would be exceeded.

## 4. Layout (render-checked, approximately)
The left column is a `table--small` with a fixed column layout: a day heading row, then `time · src · title` rows. The **row budget** is enforced in the payload (`--max-rows 11`, counting headings), so the overflow engine never cuts the table and leaves a heading orphaned. The first render showed exactly that, which is why the budget lives in the payload.

The right column has three `progress-bar--small` gauges (marked "(20h old)" when stale), then the "Needs you (n) · W · T · F" block with up to 3 `item`s and a "+N more on the cockpit" line. The title bar reads `Kam` and `updated <push time>`.

**Render method.** This is not `trmnlp`. The page uses trmnlp's own `render_html.erb` shell with the official 3.4.0 CSS/JS. The Liquid is rendered by liquidjs 10.16.1, installed drive-locally in `_preview/` (2.1 MB). The screenshot is 800×480 headless Chrome via the existing Playwright install. Output files: `_preview/render_real.png` and `_preview/render_worst.png`.
- In this render, `data-clamp` did **not** truncate. Clipping is therefore also done in the payload: event titles to 30 characters, action titles to 60, defaults to 40.
- With today's data the left column fits 7 events plus 4 headings, then "+8 more" and the Secuura warning. **Tuesday's two Datasec meetings fall into "+8 more"**: the list is chronological and Family events fill the earlier days. See open question 2.

## 5. Refresh plan
- **Job.** `2_Project_Files/trmnl/trmnl-push.plist.template` (draft, not installed) runs `push.sh` every **900 s**. It follows the `scheduler/jobs/*.plist.template` style, with `@PROJECT_DIR@`/`@SEAT@` placeholders and logs in `~/Library/Logs` because of the EX_CONFIG-78 lesson noted in `chatsync.plist.template`. It would be armed for the **wednesday** seat only, since the collect loop runs on Wednesday's Mac, by adding it to `scheduler/jobs/` and `install_all_jobs.sh`. That is a later change and needs Kam's go-ahead.
- **Why 900 s.** It is 4 posts/hour against a limit of 12/hour, and it matches TRMNL's 15-minute default account refresh, so pushing faster shows nothing new. `push.sh` also refuses a second push within 300 s.
- **End-to-end lag.** An event change reaches the screen in at most about 5 min (collect) + 15 min (push) + 15 min (device refresh), roughly 35 minutes worst case. The screen shows "updated HH:MM" so its age is always visible.

## 6. Privacy (Kam's call)
A push sends **meeting titles from all three calendars** to TRMNL's cloud. That includes Datasec customer meetings (e.g. "HP-Datasec | Playbook Platform Touchpoint") and Family items naming the children. It also sends decision-card titles and their default actions (e.g. "RD-774: NexusAI runs SQL text sent by the browser…"). TRMNL stores the last payload and returns it on GET (webhooks doc).
- **Options.** `TRMNL_REDACT=datasec,secuura,personal,family` (any subset) replaces each matching title with "Datasec event" and similar. The selftest proves a redacted title appears nowhere in the payload. There is no option to redact action titles; one could be added.
- **Recommendation.** Leave it to Kam. If he wants a default, redact `datasec` (customer names) and keep the rest.

## 7. Contradictions with the brief
1. **The three calendars** are Datasec (M365), Secuura (Google) and Personal (iCloud, which includes Family) (`generate.py:135-139`). They are not "personal, family, Datasec". **Secuura has been dead since 28 Aug (HTTP 404)**, so only two are live. Fixing it means a new secret ICS URL in `.env`. That is a separate task, and probably Kam's to supply.
2. **The cockpit shows only Wednesday and Tuesday chips** (`cockpit.html:430`, the `["wednesday","tuesday"]` loop). Friday is published by `server.py:236` but never rendered on the cockpit. The TRMNL view shows all three.
3. The figure is **weekly plan usage**, not context %. Wednesday and Friday currently read the same 16–17% with the same "6d 20h" reset. That is consistent with one shared plan, but **unmeasured**. Tuesday reads 100%, published 20 h ago, so it shows as stale.

## 8. Unmeasured
- Kam's device model (OG 800×480 1-bit vs X 1040×780 4-bit). The layout was rendered for the OG only.
- Whether he has TRMNL+, which would allow a 10 KB payload, 30 posts/hour and 5-minute refresh.
- How the real device renders: the official renderer was not run, and data-clamp did not work in the approximate render.
- A live webhook round-trip (forbidden in this task). It includes whether `curl -K <(…)` behaves as expected on the first real push.
- Whether TRMNL's Liquid treats `== nil` on a missing `pct` the same way liquidjs does.

## Open questions (recommended default in **bold**)
1. Redact work titles? **No redaction, but Kam decides before the first push.**
2. Should the left list be purely chronological (today: Family fills it and pushes Datasec Tuesday into "+8 more"), or should it prioritise work calendars? **Chronological, but shorten the horizon to 3 days when rows overflow.** This is a one-flag change (`--days`).
3. Show muted items? **No (`--keep-muted` is available).**
4. Include agents' unanswered QUESTIONs in "Needs you"? **No: they need Wednesday, not Kam.**
