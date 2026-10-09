# TRMNL "Kam view" (draft, 2026-10-09)

One full-screen TRMNL private plugin. The left half shows meetings from the three dashboard calendars. The right half shows each agent's weekly-plan usage, with the open decision cards that need Kam underneath.
Design and sources: `1_Project_Definition/Architecture/2026-10-09_trmnl-view-design.md`.

**Status:** draft only. Nothing has been published and nothing has been sent to TRMNL. No job is installed.

| File | What it is |
|---|---|
| `markup.liquid` | Paste this into the plugin's **Edit Markup → Full** tab. It uses Framework 3.4 classes and plain Liquid. |
| `build_payload.py` | Reads `0_Brain/dashboard/data/*.json` read-only and prints `{"merge_variables":…}`. It makes no network calls. Its exit codes are 0 for ok, 2 for bad input, and 3 when the payload is over `--limit`. |
| `build_payload.py --selftest` | Runs 10 planted cases. Each case also runs against a deliberately broken variant, and that variant must fail. |
| `push.sh` | Builds the payload and POSTs it to `TRMNL_WEBHOOK_URL` from `4_Credentials/.env`. It refuses if the URL is unset or is not a trmnl.com URL, never prints the URL, and won't post more often than every 300 s. `--dry-run` builds the payload without any network call. |
| `trmnl-push.plist.template` | Draft launchd job that runs every 900 s, in the same style as `scheduler/jobs/`. **Not installed.** |
| `_preview/render.js` | Approximate local render (see below). Uses liquidjs 10.16.1, installed under `_preview/node_modules` (2.1 MB, gitignored). |

## Kam's steps (once)
1. Log in at trmnl.com. Hover the device picker, click the gear, and scroll to **Developer perks**. Confirm that Developer is active (you've paid for it, so it should be).
2. Open **Plugins**, search for **Private Plugin**, and add it. Name it `Kam view`, set **Strategy** to **Webhook**, then click **Save**.
3. Click **Edit Markup**. On the **Full** tab, paste all of `markup.liquid` and save.
4. Copy the **Webhook URL** from the plugin settings. It looks like `https://trmnl.com/api/custom_plugins/<uuid>`.
5. Put this line in `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env`: `TRMNL_WEBHOOK_URL=<that URL>`. Don't paste the URL into chat.
6. Add the plugin to the device's playlist as a full-screen item, with no mashup.
7. Optional: to hide work titles, also add `TRMNL_REDACT=datasec,secuura` to the same `.env`.

After that, Wednesday runs `push.sh` once by hand and checks the screen. Only then is the job armed.

## Render check (approximate, NOT the official renderer)
The official `trmnlp` tool could not be used without a global install. It needs Ruby ≥ 4.0 and this Mac has 2.6.10. Its Docker route would pull an image into Docker's global store.
`_preview/render.js` copies trmnlp's own page shell (`web/views/render_html.erb`) and loads the official `https://trmnl.com/css/3.4.0/plugins.css` and `js/3.4.0/plugins.js`. It renders the Liquid with liquidjs. The page was then screenshotted at 800×480 with the existing Playwright install.
Results are in `_preview/render_real.png` (today's data) and `_preview/render_worst.png` (planted maximum-length data).
The defaults `--max-rows 11`, `--max-actions 3` and the title clip lengths come from those renders. If the real device clips anything, lower them.

## Kam's ruling on titles (2026-10-09 13:25:12, card `wed-trmnl-setup-and-titles-1009` = b)
**Show all titles.** No `--redact` flag is passed; the builder's default sends every calendar title and card title as-is. Do not add redaction without a new ruling.
