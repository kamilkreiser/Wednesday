# Live dashboard shows times one hour behind: diagnosis (read-only)

Written 2026-10-16 13:16 AEDT by a Tuesday subagent. Nothing was changed or deployed. Kam reported it on the live board at 13:03:13 AEDT.

## BLUF

**Root cause found and confirmed.** The live cockpit page formats decision-card times in **`Australia/Brisbane`**. Queensland has no daylight saving, so it stays on UTC+10 all year. Sydney moved to AEDT (UTC+11) on 2026-10-04, so every decision-card time on the board has read one hour behind since that date. The page also adds a hard-coded `" AEST"` label to those times.

- `2_Project_Files/dashboard-cloud/app/static/index.html:674`: `const AEST = "Australia/Brisbane";`
- `:675` `aest()`: `Intl.DateTimeFormat("en-AU", { timeZone: AEST, … })`. This is the card time.
- `:677` `aestDay()`: same zone, used for the "today" bucketing.
- `:728`: `aest(dec.t) + " AEST"`. This is the open card's posted time.
- `:789`: `aest(dec.ruledT) + " AEST"`. This is the ruled card's time.
- `:706` / `:715`: `aestDay(Date.now())` and `aestDay(dec.ruledT) === today`. Because of the offset, the day boundary for "ruled today" falls at 01:00 Sydney time, not midnight. Between 00:00 and 00:59 AEDT, cards ruled that day are left out and cards ruled the previous day still show.

The same bug exists in the **local** cockpit at `2_Project_Files/dashboard/cockpit.html:871` (`const AEST = "Australia/Brisbane"`), which feeds `aest`, `aestFull` and `aestDay` at :872–:886. The labels are at :995, :1018, :1033, :1097 and :1251, and the today-bucketing at :916, :922, :1057 and :1079. The cloud page copied this code from there.

The hypothesis is therefore confirmed in its "`Australia/Brisbane`" form. I found no hard-coded +10 offset and no `getTime()+10h` arithmetic anywhere.

## Every place a time is formatted for display

| Where | Function | Zone used | Correct after 2026-10-04? |
|---|---|---|---|
| cloud `static/index.html:675/728/789` | `aest()`, decision-card times | **Australia/Brisbane** (fixed +10) | **No, 1 h behind** |
| cloud `static/index.html:677/706/715` | `aestDay()`, "ruled today" filter | **Australia/Brisbane** | **No, day boundary is 1 h late** |
| cloud `static/index.html:538` and `static/chat.html:336` | message time = `m.ts.slice(11,16)` | `m.ts` comes from `common.js:281–283` `localTs()`, which uses `getHours()` | Yes. This is the **viewing device's local zone**, so it is correct on a Sydney-set device. It would be wrong on a device set to another zone. |
| cloud `static/index.html:676/678` | fallback when Intl throws | UTC with a "Z" suffix | Not reached in normal use |
| cloud `app/main.py` (lines 234, 252, 416, 459, 500, 567) | server timestamps | All UTC, `...Z` | Yes, nothing there is displayed in a local zone |
| cloud `seat/seat_common.py:72–77` `to_utc_z` | converts local ISO to UTC | Respects the offset in the string. A naive string gets `.astimezone()`, the machine zone, which is AEDT. | Yes |
| cloud `seat/get_kam_messages.py:23` | UTC to the machine's local zone | System zone (AEDT) | Yes |
| local `dashboard/cockpit.html:871–886` | `aest`/`aestFull`/`aestDay` | **Australia/Brisbane** | **No, the same bug** |
| local `dashboard/collect.py:30,71,233` / `generate.py:17` / `server.py` | `datetime.now().astimezone()`; Graph uses `Prefer: outlook.timezone="Australia/Sydney"` | System zone or Sydney | Yes. The machine is on AEDT: `date` gives `Fri 16 Oct 2026 13:15:08 AEDT`. |
| `2_Project_Files/tools/*.py,*.sh` (current files, not `.pre-*`) | searched for `brisbane`, `aest`, `timedelta(hours=10/11)`, `+10:00` and `TZ=` | No hits | n/a |

Excluded from the conclusions: the `*.pre-*` and `*.bak-*` backups (for example the earlier `index.html.pre-*` and `server.py.bak-20260817*` files). Some old REPORT_*.md files and `dashboard/site/index.html:353` contain static "AEST" text. These are historical prose or generated output, not live formatting.

## Does the live site serve the same code as the local tree?

**I could not confirm this byte-for-byte.** Plain GET requests to `/`, `/index.html` and `/static/index.html` on `wednesday-dashboard-e42e.azurewebsites.net` all return **401 with an empty body**: Easy Auth sits in front of everything. Per the brief, I did not log in.

Indirect evidence that live matches local:
- `main.py:826` serves `static/index.html` directly through `FileResponse` with no-store headers, so there is no build step that could change the JS.
- The Brisbane constant has been in the cloud page since it was copied from `cockpit.html` (it also appears in the `.pre-*` backups going back to 09-07).
- The symptom matches the code exactly: a 1 h lag, on a page where every card time is labelled "AEST".

Caveat: the most recent commit touching this file is `255ba6830`, described as "dashboard header edit (deploy pending verification)". The live copy may be one header edit behind. That edit does not touch the time code.

## Smallest fix (proposal only, not applied)

Cloud page. These are display-only changes: the zone name and the label. No data, API or server change is involved.

```diff
--- a/2_Project_Files/dashboard-cloud/app/static/index.html
+++ b/2_Project_Files/dashboard-cloud/app/static/index.html
@@ -674 +674 @@
-const AEST = "Australia/Brisbane";
+const AEST = "Australia/Sydney";   // follows DST (AEST UTC+10 / AEDT UTC+11); Brisbane never shifts — 2026-10-16 1 h-behind bug
@@ -728 +728 @@
-  ... when.textContent = dec.t ? aest(dec.t) + " AEST" : ""; ...
+  ... when.textContent = dec.t ? aest(dec.t) : ""; ...
@@ -789 +789 @@
-  ... when.textContent = aest(dec.ruledT) + " AEST";
+  ... when.textContent = aest(dec.ruledT);
```

For the label, there are two options:
- Drop the label, as in the diff above.
- Have the formatter print the correct one by adding `timeZoneName: "short"` to the `aest()` options. In en-AU this renders as "AEDT" or "AEST" automatically.

Leaving `" AEST"` hard-coded would show a wrong label for half the year.

Apply the same one-line zone change to the local `2_Project_Files/dashboard/cockpit.html:871`, plus the label lines at :995, :1018, :1033, :1097 and :1251.

Optional hardening: the message times (`common.js:281` `localTs`) follow whatever zone the viewing device is set to. If Kam ever views from a device set to another zone, those times would shift too. Pinning them to Sydney would mean formatting with `Intl.DateTimeFormat(..., {timeZone: "Australia/Sydney"})` instead of `getHours()`. That is not needed for today's bug.

Verifying the fix after deploy: open the board signed in. A card posted now should show the current Sydney wall-clock time (for example 13:xx). An entry in "ruled today" made after 00:00 AEDT should appear immediately.
