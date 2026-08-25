#!/usr/bin/env python3
"""collect.py — Wednesday Life-OS dashboard, Phase 0 data collectors.

Pulls every live feed into 0_Brain/dashboard/data/*.json. Read-only against
every source. Secrets come from 4_Credentials/.env; nothing secret is written
into the data files (event/ticket content only).

Feeds: personal calendar (EventKit probe) · Secuura Google (secret ICS) ·
Datasec M365 (Graph, with token refresh) · Linear WED board · brain files
(decision queue, scoreboard, flags).
"""
import json, os, re, subprocess, sys, urllib.request, urllib.parse, datetime, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent                      # WEDNESDAY project root
DATA = ROOT / "0_Brain" / "dashboard" / "data"
CRED = ROOT / "4_Credentials"
DATA.mkdir(parents=True, exist_ok=True)

def env():
    e = {}
    for line in (CRED / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            e[k.strip()] = v.strip()
    return e

ENV = env()
NOW = datetime.datetime.now().astimezone()

def write(name, payload):
    (DATA / name).write_text(json.dumps(
        {"collected_at": NOW.isoformat(), "data": payload}, indent=1, ensure_ascii=False))
    print(f"  {name}: ok")

# ── personal calendar (EventKit probe, zero credentials) ─────────────────
def personal_calendar():
    probe = ROOT / "2_Project_Files" / "tools" / "calendar_probe"
    out = subprocess.run([str(probe)], capture_output=True, text=True, timeout=30)
    payload = json.loads(out.stdout)
    wanted = [c.strip() for c in ENV.get("ICAL_CALENDAR_NAMES", "").split(",") if c.strip()]
    evs = [e for e in payload.get("events_next_48h", []) if not wanted or e["cal"] in wanted]
    write("personal_calendar.json", {"calendars": payload.get("calendars", []), "events": evs})

# ── Secuura Google (secret ICS) ──────────────────────────────────────────
def _unfold(text):
    return re.sub(r"\r?\n[ \t]", "", text)

# ── minimal-but-correct ICS engine (stdlib only; dateutil not on machines) ──
from zoneinfo import ZoneInfo

def _ics_dt(prop_line):
    """Parse 'DTSTART;TZID=Asia/Singapore:20260806T100000' → (aware dt|date, allday)."""
    m = re.match(r"[A-Z-]+(?:;[^:]*)?:(\d{8})(?:T(\d{6})(Z?))?$", prop_line.strip())
    if not m:
        return None, False
    tzid = re.search(r"TZID=([^;:]+)", prop_line)
    if m.group(2) is None:                       # VALUE=DATE → all-day
        return datetime.date(int(m.group(1)[:4]), int(m.group(1)[4:6]), int(m.group(1)[6:8])), True
    dt = datetime.datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")
    if m.group(3):                               # UTC
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    elif tzid:
        try:
            dt = dt.replace(tzinfo=ZoneInfo(tzid.group(1)))
        except Exception:
            dt = dt.astimezone()
    else:                                        # floating → local
        dt = dt.astimezone()
    return dt.astimezone(), False                # normalize to system tz (Sydney)

_WD = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}

def _expand_rrule(dtstart, rrule, win_start, win_end, exdates, overridden):
    """Expand FREQ=DAILY/WEEKLY (full) and MONTHLY/YEARLY (simple) within window.
    Returns aware datetimes. Ordinal BYDAY (e.g. 1SU) unsupported → master only."""
    parts = dict(seg.split("=", 1) for seg in rrule.strip().split(";") if "=" in seg)
    freq = parts.get("FREQ"); interval = int(parts.get("INTERVAL", 1) or 1)
    count = int(parts["COUNT"]) if "COUNT" in parts else None
    until = None
    if "UNTIL" in parts:
        u, _ = _ics_dt("X:" + parts["UNTIL"])
        until = (datetime.datetime.combine(u, datetime.time(23, 59), tzinfo=NOW.tzinfo)
                 if isinstance(u, datetime.date) and not isinstance(u, datetime.datetime) else u)
    bydays = None
    if "BYDAY" in parts:
        if re.search(r"\d", parts["BYDAY"]):
            return []                            # ordinal BYDAY — out of scope
        bydays = {_WD[d] for d in parts["BYDAY"].split(",") if d in _WD}
    out, n, cur = [], 0, 0
    local = dtstart                              # aware, already system tz? keep ORIGINAL zone for DST-correct stepping
    step_zone = dtstart.tzinfo
    day = dtstart.date(); tod = dtstart.timetz().replace(tzinfo=None)
    for i in range(0, 800):
        if freq == "DAILY":
            d = day + datetime.timedelta(days=i * interval)
        elif freq == "WEEKLY":
            d = day + datetime.timedelta(days=i)
            week_idx = ((d - day).days + dtstart.weekday()) // 7 if False else (d - day).days // 7
            if (bydays and d.weekday() not in bydays) or (not bydays and d.weekday() != dtstart.weekday()):
                continue
            if interval > 1 and ((d - day).days // 7) % interval != 0:
                continue
        elif freq == "MONTHLY":
            mth = (day.month - 1 + i * interval); yr = day.year + mth // 12
            try:
                d = day.replace(year=yr, month=mth % 12 + 1)
            except ValueError:
                continue
        elif freq == "YEARLY":
            try:
                d = day.replace(year=day.year + i * interval)
            except ValueError:
                continue
        else:
            return []
        occ = datetime.datetime.combine(d, tod, tzinfo=step_zone)
        if occ < dtstart:
            continue
        n += 1
        if count and n > count:
            break
        if until and occ > until:
            break
        occ_local = occ.astimezone()
        if occ_local > win_end:
            break
        key = occ.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S")
        if occ_local >= win_start and key not in exdates and key not in overridden:
            out.append(occ_local)
        if freq == "WEEKLY" and i > 700:
            break
    return out

def _parse_ics(text, horizon_days=8):
    win_start = NOW - datetime.timedelta(hours=12)
    win_end = NOW + datetime.timedelta(days=horizon_days)
    vevents = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", _unfold(text), re.S):
        def prop(name):
            m = re.search(rf"^{name}(?:;[^:\n]*)?:.*$", block, re.M)
            return m.group(0) if m else None
        uid = (re.search(r"^UID:(.*)$", block, re.M) or [None, ""])[1] if re.search(r"^UID:", block, re.M) else ""
        m = re.search(r"^UID:(.*)$", block, re.M); uid = m.group(1).strip() if m else ""
        t = re.search(r"^SUMMARY:(.*)$", block, re.M)
        ds = prop("DTSTART")
        if not ds:
            continue
        start, allday = _ics_dt(ds)
        if start is None:
            continue
        de = prop("DTEND")
        end = _ics_dt(de)[0] if de else None
        rr = re.search(r"^RRULE:(.*)$", block, re.M)
        recid = prop("RECURRENCE-ID")
        exdates = set()
        for ex in re.findall(r"^EXDATE[^:\n]*:(.*)$", block, re.M):
            for one in ex.split(","):
                v, _a = _ics_dt("X:" + one.strip())
                if isinstance(v, datetime.datetime):
                    exdates.add(v.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S"))
        vevents.append({"uid": uid, "title": (t.group(1).strip() if t else "?"),
                        "start": start, "end": end, "allday": allday,
                        "rrule": rr.group(1).strip() if rr else None,
                        "recid": _ics_dt(recid)[0] if recid else None, "exdates": exdates})
    overridden = {}                              # uid → set of overridden occurrence keys
    for v in vevents:
        if v["recid"] is not None and isinstance(v["recid"], datetime.datetime):
            overridden.setdefault(v["uid"], set()).add(
                v["recid"].astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S"))
    events = []
    def emit(dt, v):
        events.append({"start": dt.isoformat() if isinstance(dt, datetime.datetime) else
                       datetime.datetime.combine(dt, datetime.time(0), tzinfo=NOW.tzinfo).isoformat(),
                       "title": v["title"], "allday": v["allday"]})
    for v in vevents:
        if v["allday"]:
            s0 = v["start"]
            e0 = v["end"] if isinstance(v["end"], datetime.date) else s0 + datetime.timedelta(days=1)
            d = s0
            while d < e0:                        # DTEND exclusive
                dd = datetime.datetime.combine(d, datetime.time(0), tzinfo=NOW.tzinfo)
                if win_start <= dd <= win_end:
                    emit(d, v)
                d += datetime.timedelta(days=1)
            continue
        if v["rrule"]:
            for occ in _expand_rrule(v["start"], v["rrule"], win_start, win_end,
                                     v["exdates"], overridden.get(v["uid"], set())):
                emit(occ, v)
            continue
        if win_start <= v["start"] <= win_end:
            emit(v["start"], v)
    return sorted(events, key=lambda e: e["start"])

def secuura_calendar():
    url = ENV["SECUURA_GCAL_ICS_URL"]
    text = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "replace")
    write("secuura_calendar.json", {"events": _parse_ics(text)})

# ── Datasec M365 (Graph delegated, refresh-token plumbing) ───────────────
def _graph_token():
    tok_path = CRED / "msgraph_token.json"
    tok = json.loads(tok_path.read_text())
    age = NOW.timestamp() - tok.get("obtained_at", 0)
    if age > tok.get("expires_in", 3600) - 300:          # refresh 5 min early
        body = urllib.parse.urlencode({
            "grant_type": "refresh_token",
            "client_id": ENV["MSGRAPH_CLIENT_ID"],
            "refresh_token": tok["refresh_token"],
            "scope": "https://graph.microsoft.com/Calendars.Read offline_access openid profile",
        }).encode()
        url = f"https://login.microsoftonline.com/{ENV['MSGRAPH_TENANT_ID']}/oauth2/v2.0/token"
        new = json.load(urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=30))
        new.setdefault("refresh_token", tok["refresh_token"])   # MS may omit on refresh
        new["obtained_at"] = int(NOW.timestamp())
        tok_path.write_text(json.dumps(new))
        os.chmod(tok_path, 0o600)
        tok = new
    return tok["access_token"]

def datasec_calendar():
    token = _graph_token()
    start = NOW.astimezone(datetime.timezone.utc)
    end = start + datetime.timedelta(days=8)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    url = ("https://graph.microsoft.com/v1.0/me/calendarView?"
           f"startDateTime={start.strftime(fmt)}&endDateTime={end.strftime(fmt)}"
           "&$select=subject,start,end,isAllDay,location&$orderby=start/dateTime&$top=50")
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + token,
        "Prefer": 'outlook.timezone="Australia/Sydney"'})
    r = json.load(urllib.request.urlopen(req, timeout=30))
    events = [{"start": e["start"]["dateTime"], "title": e["subject"],
               "allday": e["isAllDay"],
               "location": (e.get("location") or {}).get("displayName", "")}
              for e in r.get("value", [])]
    write("datasec_calendar.json", {"events": events})

# ── Linear WED board ─────────────────────────────────────────────────────
def linear_board():
    q = {"query": """query{ issues(filter:{team:{key:{eq:"WED"}},
          state:{type:{in:["started","unstarted"]}}}, first:60, orderBy: updatedAt){
          nodes{ identifier title priority dueDate state{name} } } }"""}
    req = urllib.request.Request("https://api.linear.app/graphql",
        data=json.dumps(q).encode(),
        headers={"Authorization": ENV["LINEAR_API_KEY"], "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=30))
    issues = r["data"]["issues"]["nodes"]
    write("linear_wed.json", {"active": [i for i in issues if i["state"]["name"] == "In Progress"],
                              "todo": [i for i in issues if i["state"]["name"] == "Todo"]})

# ── Linear WED personal actions (issues labelled "personal") ─────────────
def linear_personal():
    q = {"query": """query{ issues(filter:{team:{key:{eq:"WED"}},
          labels:{name:{eq:"personal"}},
          state:{type:{nin:["completed","canceled"]}}}, first:60, orderBy: updatedAt){
          nodes{ identifier title priority dueDate updatedAt state{name type} } } }"""}
    req = urllib.request.Request("https://api.linear.app/graphql",
        data=json.dumps(q).encode(),
        headers={"Authorization": ENV["LINEAR_API_KEY"], "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=30))
    nodes = r["data"]["issues"]["nodes"]
    # priority first (urgent=1 … low=4, no-priority last), then most recently updated
    items = sorted(sorted(nodes, key=lambda i: i.get("updatedAt") or "", reverse=True),
                   key=lambda i: i.get("priority") or 5)
    write("linear_personal.json", {"items": items})

# ── brain files (paths only read; content summarized) ────────────────────
def brain_state():
    b = ROOT / "0_Brain"
    scoreboard = (b / "projects_index" / "scoreboard.md").read_text()[:4000]
    dq = (b / "projects_index" / "decision_queue.md").read_text()[:2000]
    write("brain_state.json", {
        "scoreboard_excerpt": scoreboard,
        "decision_queue_excerpt": dq,
        "flags": [
            # KS-480 consent-by-silence flag removed 2026-08-25 on Kam's ask —
            # resolved 2026-08-06 (Peter answered explicitly 08-05 11:36; consent
            # recorded properly, never by silence; verified against the live board).
            {"due": "2026-09-04", "what": "CypherKey Twilio token rotation (CPKEY-165 / WED-48)"},
            # admin-consent watch flag removed 2026-08-25: the Datasec calendar feed
            # IS live (real events in datasec_calendar.json, fresh collect cycles) —
            # the arrival it watched for happened.
        ]})

# ── Agent Mail (fleet inboxes; read-only, NO acks — at-least-once lesson) ──
def agentmail_feed():
    key = ENV.get("AGENTMAIL_API_KEY")
    if not key:
        raise RuntimeError("AGENTMAIL_API_KEY unset")
    msgs = []
    for inbox in ("wednesday-agent@agentmail.to", "coagent@agentmail.to"):
        req = urllib.request.Request(
            f"https://api.agentmail.to/v0/inboxes/{inbox}/messages?limit=8",
            headers={"Authorization": "Bearer " + key})
        r = json.load(urllib.request.urlopen(req, timeout=30))
        for m in r.get("messages", []):
            subj = m.get("subject") or "(no subject)"
            msgs.append({"inbox": inbox.split("@")[0], "from": (m.get("from") or "?"),
                         "subject": subj, "ts": m.get("timestamp", ""),
                         "attn": "QUESTION" in subj.upper(),
                         # WED-113 round 2 (additive): the API's own preview
                         # snippet (~200 chars, BLUF line) for the cockpit's
                         # expand-row view — no extra requests, no body fetch.
                         "excerpt": (m.get("preview") or "").strip()[:300]})
    by_subj = {}
    for m in sorted(msgs, key=lambda x: x["ts"], reverse=True):
        k = re.sub(r"\s+", " ", m["subject"].strip().lower())
        if k in by_subj:
            if m["inbox"] not in by_subj[k]["inboxes"]:
                by_subj[k]["inboxes"].append(m["inbox"])
        else:
            m["inboxes"] = [m["inbox"]]
            by_subj[k] = m
    write("agentmail.json", {"messages": list(by_subj.values())[:12]})

# ── Tickets: per-client cards from projects_index entries (cached; freshness shown) ──
def tickets_feed():
    entries = []
    edir = ROOT / "0_Brain" / "projects_index" / "entries"
    for f in sorted(edir.glob("*.md")):
        text = f.read_text()
        fm = {}
        if text.startswith("---"):
            fm = dict(re.findall(r"^(\w+):\s*(.+)$", text.split("---")[1], re.M))
        # Heading may carry an annotation — "**Open / next (refreshed 2026-08-25 …):**".
        # The strict form silently rendered annotated cards as EMPTY (found 2026-08-25:
        # the two most-active projects showed no items the same day they were refreshed).
        m = re.search(r"\*\*Open / next[^\n]*:\*\*\n(.*?)(?:\n\*\*|\Z)", text, re.S)
        items = [re.sub(r"^[-\s\[\]x]+", "", l).strip()
                 for l in (m.group(1).splitlines() if m else []) if l.strip().startswith("-")]
        entries.append({"client": fm.get("client", "?"), "project": fm.get("project", "?"),
                        "updated": fm.get("updated", "?"), "items": items[:8]})
    write("tickets.json", {"projects": entries})

# ── Parking lot: one .md per item in 0_Brain/parkinglot (WED-71 v1) ──────
def parkinglot_feed():
    pdir = ROOT / "0_Brain" / "parkinglot"
    items = []
    for f in sorted(pdir.glob("*.md")):
        text = f.read_text()
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        fm = {}
        for line in parts[1].splitlines():
            m = re.match(r"^(\w+):\s*(.*)$", line)
            if m:
                fm[m.group(1)] = m.group(2).split("#", 1)[0].strip().strip('"').strip()
        if "mode" not in fm:
            continue   # companions (research reports, templates) carry no mode key
        body = parts[2].strip()
        tm = re.search(r"^#\s+(.+)$", body, re.M)
        om = re.search(r"^One-liner:\s*(.*?)(?:\n\s*\n|\Z)", body, re.M | re.S)
        items.append({
            "file": f.name,
            "title": tm.group(1).strip() if tm else f.stem,
            "one_liner": re.sub(r"\s+", " ", om.group(1)).strip() if om else "",
            "mode": fm.get("mode", "parked"),
            "status": fm.get("status", "open"),
            "date": fm.get("date", ""),
            "source": fm.get("source", ""),
            "promoted_to": fm.get("promoted_to", ""),
            "research": bool(re.search(r"^(?:#+\s*)?Research\b", body, re.M)),
            "body": body,
        })
    write("parkinglot.json", {"items": items})

# ── News (public RSS, no auth; per-feed failures tolerated) ──────────────
NEWS_SOURCES = [
    ("world",    "BBC World",        "http://feeds.bbci.co.uk/news/world/rss.xml"),
    ("tech",     "Ars Technica",     "https://feeds.arstechnica.com/arstechnica/index"),
    ("quantum",  "arXiv quant-ph",   "https://rss.arxiv.org/rss/quant-ph"),
    ("security", "The Hacker News",  "https://feeds.feedburner.com/TheHackersNews"),
    ("biotech",  "Fierce Biotech",   "https://www.fiercebiotech.com/rss/xml"),
]

def _strip_html(t):
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = re.sub(r"&[a-z]+;", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def news_feed():
    import xml.etree.ElementTree as ET
    topics = {}
    errors = []
    for topic, srcname, url in NEWS_SOURCES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (WednesdayDash/0.1)"})
            raw = urllib.request.urlopen(req, timeout=20).read()
            root = ET.fromstring(raw)
            items = root.findall(".//item")[:6]
            out = []
            for it in items:
                g = lambda tag: (it.findtext(tag) or "").strip()
                out.append({"title": _strip_html(g("title"))[:160], "link": g("link"),
                            "summary": _strip_html(g("description"))[:400],
                            "date": g("pubDate")[:22], "source": srcname})
            topics[topic] = [o for o in out if o["title"]]
        except Exception as e:
            errors.append(f"{topic}: {e}")
            topics[topic] = []
    write("news.json", {"topics": topics, "errors": errors})

FEEDS = {"personal": personal_calendar, "secuura": secuura_calendar,
         "datasec": datasec_calendar, "linear": linear_board, "brain": brain_state,
         "agentmail": agentmail_feed, "tickets": tickets_feed, "news": news_feed,
         "parkinglot": parkinglot_feed, "linear_personal": linear_personal}

if __name__ == "__main__":
    failures = 0
    only = sys.argv[1:] or FEEDS.keys()
    print("collect:", NOW.isoformat())
    for name in only:
        try:
            FEEDS[name]()
        except Exception as e:
            failures += 1
            print(f"  {name}: FAILED — {e}", file=sys.stderr)
            (DATA / f"{name}_error.json").write_text(json.dumps(
                {"collected_at": NOW.isoformat(), "error": str(e)}))
    sys.exit(1 if failures else 0)
