# Dashboard snapshot — 2026-08-06 19:46, before the project-colour redesign

**Why this exists:** Kam, 2026-08-06: *"please take a snapshot of the layout,
code, etc for the dashboard as we might role back to this point if the next item
is not a keeper."* The next item is a project-colour system across the whole
dashboard, in both themes — a broad visual change that may not survive review.

## What this is a snapshot OF

The dashboard as it stood after rounds 6–11 today: cascading menu, flag-for-Wed,
news flagging that survives the feed, whole-site source filtering with reset,
bottom-aligned notes, family day headings + bell, and light/dark themes with
theme-aware tints. Everything verified in-browser.

## Two ways back

**1. Git (preferred — the whole repo at this point):**
```
git tag                     # find: dashboard-pre-colour-2026-08-06
git checkout dashboard-pre-colour-2026-08-06 -- 2_Project_Files/dashboard
git checkout dashboard-pre-colour-2026-08-06 -- 0_Brain/dashboard/data/layout.json
cd 2_Project_Files/dashboard && python3 generate.py
```

**2. These files (works even without git):**
```
cp generate.py server.py collect.py serve.sh  ../../../2_Project_Files/dashboard/
cp layout.json views.json                      ../../../0_Brain/dashboard/data/
cd ../../../2_Project_Files/dashboard && python3 generate.py
```
Then restart: `pkill -f dashboard/server.py; nohup ./serve.sh >> logs/serve.log 2>&1 &`

`index.html.rendered` is the exact page as served at snapshot time — useful for
diffing "what did it look like before" without regenerating.

## NOT captured here (deliberately)

Live feed data (`*_calendar.json`, `linear_wed.json`, `agentmail.json`,
`news.json`) — those refresh every 5 minutes and are not part of the design.
Nor are `muted.json` / `archived.json` / `wedflags.json` / `chat_log.json`,
which are Kam's own state and should NOT be rolled back with a design change.

## Verify a restore worked

```
curl -s http://127.0.0.1:47787/api/health          # {"app":"wednesday-dashboard","ok":true}
grep -c 'tgchip' site/index.html                    # per-tile source chips present
grep -o 'data-theme="[a-z]*"' site/index.html | head -1
```
