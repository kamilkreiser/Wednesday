STARTABLE: YES (with D-1 and Q-1 below; the ruling is "read once, change nothing" and the list read has one unavoidable sign-in footprint)

Drafted at `date` Tue 3 Nov 2026 10:59 AEDT (last `date` read before writing). Kit: `2026-11-03_B1202_SEAT-R154_hpsmpoc-uat-feedback-read.md`.

## BLUF
- We do NOT need a key we lack. UAT sign-in is a level picker: `POST /api/auth/uat` form `level=admin` sets a cookie; the web BFF mints the signed assertion itself from its own `HPSM_UAT_OPEN_KEY` (key vault reference on the site). The list is `GET /api/v1/feedback?limit=200` on the WEB host (Admin only).
- Credential held? NO key held, NONE needed. Locations checked (names only): `HPSM-POC/4_Credentials/.env` has no `HPSM_UAT_OPEN_KEY` / `Auth__UatOpen__Key` name (grep of names: 0; control: `JIRA_BASE_URL` found). The key lives only in the UAT key vault (`uat-open-key`, RELAYED `B415_STATUS.md:84`, `B1048_STATUS.md:95`); I ran no az.
- Hosts: `.tools/b1048/hosts.txt` lines 1-2 are the UAT web and API hostnames (read by `cat`; no HTTP made by me).

## Facts (command + control)
- Origin main `f464376b1f7b62e4a5bf0c73af6c14a8c29993ea` (`git ls-remote origin main`). Raw files by `gh api -X GET contents/...?ref=main` (Accept raw); pointers printed by `grep -n`.
- Route map: `FeedbackModule.cs:165` GET list, `:166` GET attachment, `:62` AdminPolicy, `:102` `RequireRole(Roles.Admin)`. Control: `:164` is the POST (found by the same grep).
- List handler `FeedbackEndpoints.cs:204`, `MaxLimit = 200` at `:51`, no SaveChanges inside it (read `:204-226`). Download `:185` does `db.Audit.Add` + SaveChanges (WRITES an audit row).
- Web: `AdminFeedback.tsx:73` `client.GET("/api/v1/feedback", limit 100)`; BFF UAT branch `bff.ts:430-439`; sign-in `uatOpen.ts:104-120`; same-origin check `:67-80`.
- Caller lookup `Caller.cs:89-135`: first call inserts `app_user` + audit `user.first-seen`; later calls update `LastSeenAt`. Applies to every signed-in call.
- Feedback route off: `slotflags-api.txt:19` `Feedback__Route False` (also `:17-18` webhook names). `IFeedbackSink.cs:110` comment confirms "shipped default off".
- Ports: `lsof -nP -iTCP:9660-9669 -sTCP:LISTEN | wc -l` = 5 (G313's; the kit uses none). Panes: `tmux list-panes -a` shows `HPSM-POC focus-ring round3 gate` only.
- Model: `model-routing.md:98` C8 -> Sonnet; id `claude-sonnet-5-5` (`models_latest.json`).

## D-decisions
- D-1: the attachment download (`getFeedbackAttachment`) writes an audit row, so the kit does NOT call it by default; a Stamp slot `ATTACHMENTS (ALLOWED or NO)` lets Tuesday flip it. Items' attachment facts come from the list (name, size, type, sha256).
- D-2: no API-host call and no search for the UAT key (hold no key; the BFF signs). Sign-in uses the same level picker a reviewer uses.
- D-3: no page cursor exists; limit 200 newest-first. If exactly 200 return, the seat reports it rather than guessing.
- D-4: no commit/push by default (`LAND` slot); evidence stays local unless Tuesday stamps YES.

## Q-questions for Tuesday
- Q-1: Is the ordinary sign-in footprint (an `app_user` row / last-seen update and a `user.first-seen` audit event for "Admin (review copy)" on UAT, created by any signed-in call) acceptable under "nothing changed on the site"? Default: yes, it is the same footprint every reviewer leaves and is not a change to feedback; the seat discloses it in STATUS.
- Q-2: Do you want the attachments downloaded (each one writes one audit row `feedback.attachment-read`)? Default: NO (list facts only); say ALLOWED in the slot if the product owner wants the files.
- Q-3: Is `HPSM_UAT_OPEN_SIGNIN` still `on` on the live UAT web since the 2026-11-01 deploy (B1048 reported `Auth__UatOpen__Enabled` true)? Default: assume yes; the seat's step 2 stops cleanly on a 404 at the picker and names it.

## UNMEASURED
- Whether the UAT hosts are up now and the picker answers 303 (I made no HTTP call by rule). Whether any item is signed beyond the product owner's, or how many exist. Whether `app_user` for the review-copy admin already exists (decides if a first-seen row is new). Reverse proxy/Cloudflare-style blocks of curl user agents: none seen in B1031/B1048 pollers (`curl -m 8 --noproxy '*'`).

## Outside the fences
None. Read: DRAFTER_RULES, HPSM-POC git origin raw files, `Briefs/` records, `.tools/b1048/hosts.txt`, `4_Credentials/.env` variable NAMES only (sed stripped values), model-routing and models_latest. Scratch under the session scratchpad. Wrote only these two files. No HTTP to any hosted host, no Jira, no az, no `decision_queue.sh`.
