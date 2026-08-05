#!/usr/bin/env python3
"""generate.py — render 0_Brain/dashboard/data/*.json into site/index.html.

Self-contained HTML (no external assets), dark-first, FULL-WIDTH tile grid.
Tiles are draggable (organise mode), per-tile text scale, both persisted to
data/layout.json via the local API. Colors: dataviz reference palette, 3
categorical slots validated for the dark surface (2026-08-05): blue=Datasec ·
orange=Secuura · aqua=Personal/Family. Identity never color-alone.
"""
import json, html, datetime, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "0_Brain" / "dashboard" / "data"
SITE = HERE / "site"
SITE.mkdir(exist_ok=True)
NOW = datetime.datetime.now().astimezone()

def load(name):
    p = DATA / name
    return json.loads(p.read_text()) if p.exists() else None

personal = load("personal_calendar.json")
secuura = load("secuura_calendar.json")
datasec = load("datasec_calendar.json")
linear = load("linear_wed.json")
brain = load("brain_state.json")
agentmail = load("agentmail.json")
tickets = load("tickets.json")
news = load("news.json")
parking = load("parkinglot.json")
chat_log = load("chat_log.json") or []
if isinstance(chat_log, dict): chat_log = chat_log.get("data", [])
if not isinstance(chat_log, list): chat_log = []
CHAT_MODE = None  # set after LAYOUT loads
_m = DATA / "muted.json"
MUTED = set(json.loads(_m.read_text())) if _m.exists() else set()
_p = DATA / "pinned.json"
PINNED = json.loads(_p.read_text()) if _p.exists() else []
_f = DATA / "focus.json"
FOCUS = json.loads(_f.read_text()) if _f.exists() else None
_arc = DATA / "archived.json"
ARCHIVED = set(json.loads(_arc.read_text())) if _arc.exists() else set()
_l = DATA / "layout.json"
LAYOUT = json.loads(_l.read_text()) if _l.exists() else {}
if not isinstance(LAYOUT, dict): LAYOUT = {}
TILE_ORDER_DEFAULT = ["stats", "calendars", "flags", "family", "board", "chat", "tickets", "email", "news", "parkinglot"]
ORDER = [t for t in LAYOUT.get("order", TILE_ORDER_DEFAULT) if t in TILE_ORDER_DEFAULT]
ORDER += [t for t in TILE_ORDER_DEFAULT if t not in ORDER]
SCALES = LAYOUT.get("scales", {})
SIZES = LAYOUT.get("sizes", {})
if "calendars" not in SIZES: SIZES["calendars"] = {"w": 2}
if "board" not in SIZES: SIZES["board"] = {"w": 2}
if "email" not in SIZES: SIZES["email"] = {"w": 1, "h": 8}
if "tickets" not in SIZES: SIZES["tickets"] = {"w": 1, "h": 8}
if "parkinglot" not in SIZES: SIZES["parkinglot"] = {"w": 1, "h": 8}
HIDDEN_TILES = set(LAYOUT.get("hidden_tiles", []))
HIDDEN_GROUPS = set(LAYOUT.get("hidden_groups", []))   # datasec/secuura/personal/family
GROUPS = {"datasec": "Datasec", "secuura": "Secuura", "personal": "Personal", "family": "Family"}
CHAT_MODE = LAYOUT.get("chat_mode", "message")
if CHAT_MODE == "full":       # legacy expanded-tile mode → the chat-with-Wed view
    CHAT_MODE = "sidebar"
_v = DATA / "views.json"
VIEWS = json.loads(_v.read_text()) if _v.exists() else {}   # {"name": layout snapshot}
if not isinstance(VIEWS, dict): VIEWS = {}
TINTS = LAYOUT.get("tints", {})                             # {"tile-id": tint key}
if not isinstance(TINTS, dict): TINTS = {}
TINT_COLORS = {  # subtle same-lightness hue shifts of --surface-2 (#232322); text unchanged
    "slate": "#20242b", "moss": "#21261f", "plum": "#262028",
    "sand": "#262319", "teal": "#1e2626"}
# grid section separators: [{"before": tile-id, "label": str}] — bound to a tile
# id, so they follow the tile when the grid is reordered
SEP_BY_TILE = {}
for _s in (LAYOUT.get("separators") or []):
    if isinstance(_s, dict) and _s.get("before") in TILE_ORDER_DEFAULT and _s["before"] not in SEP_BY_TILE:
        SEP_BY_TILE[_s["before"]] = str(_s.get("label") or "")[:40]
# ack states (WED-73). HONESTY RULE: seen/actioning/done are written ONLY by
# Wednesday's own session; the dashboard renders them and may itself write
# nothing but "action_requested" (via /api/actionnow). Never fake ticks.
_ack = DATA / "ack_state.json"
ACK = json.loads(_ack.read_text()) if _ack.exists() else {}
if not isinstance(ACK, dict): ACK = {}
_alog = DATA / "archived_log.json"
ARCHLOG = json.loads(_alog.read_text()) if _alog.exists() else []
if not isinstance(ARCHLOG, list): ARCHLOG = []
ACK_META = {  # state → (icon, colour)
    "seen":             ("&#10003;", "var(--text-muted)"),
    "actioning":        ("&#9679;",  "#3987e5"),
    "done":             ("&#10003;", "#199e70"),
    "action_requested": ("&#9889;",  "#c98500")}

def ack_get(key):
    a = ACK.get(key)
    return a if isinstance(a, dict) and a.get("state") in ACK_META else None

def ack_line(key):
    """Tiny status line under a kam chat message. Empty when no state exists."""
    a = ack_get(key)
    if not a:
        return ""
    st = a["state"]; t = (a.get("ts") or "")[11:16]
    txt = {"seen": f"seen by Wed{' ' + t if t else ''}", "actioning": "actioning",
           "done": f"done{' ' + t if t else ''}", "action_requested": "action requested"}[st]
    return f'<div class="ackline {st}">{ACK_META[st][0]} {txt}</div>'

def ack_dot(key):
    """Small status dot before a board/tickets row title. Empty when no state."""
    a = ack_get(key)
    if not a:
        return ""
    return (f'<span class="ackdot" style="background:{ACK_META[a["state"]][1]}" '
            f'title="{a["state"].replace("_", " ")}"></span>')

SRC = {  # fixed categorical assignment — never re-ordered
    "datasec":  {"label": "Datasec",  "color": "var(--series-1)"},
    "secuura":  {"label": "Secuura",  "color": "var(--series-2)"},
    "personal": {"label": "Personal", "color": "var(--series-3)"},
}

def norm_events():
    evs = []
    if personal:
        for e in personal["data"]["events"]:
            evs.append({"src": "personal", "cal": e.get("cal", ""), "title": e["title"],
                        "start": datetime.datetime.fromisoformat(e["start"].replace("Z", "+00:00")).astimezone(),
                        "allday": e.get("allday", False)})
    if secuura:
        for e in secuura["data"]["events"]:
            evs.append({"src": "secuura", "cal": "Secuura", "title": e["title"],
                        "start": datetime.datetime.fromisoformat(e["start"]),
                        "allday": e.get("allday", False)})
    if datasec:
        for e in datasec["data"]["events"]:
            dt = datetime.datetime.fromisoformat(e["start"])
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=NOW.tzinfo)
            evs.append({"src": "datasec", "cal": "Datasec", "title": e["title"],
                        "start": dt, "allday": e.get("allday", False),
                        "loc": e.get("location", "")})
    return sorted(evs, key=lambda e: e["start"])

def ev_group(e):
    return "family" if e["cal"] == "Family" else e["src"]

EVENTS = [e for e in norm_events() if ev_group(e) not in HIDDEN_GROUPS
          and f'{e["src"]}|{e["title"]}' not in ARCHIVED]
KID_PAT = re.compile(r"\b(Alice|Harriet)\b", re.I)

def day_events(offset):
    day = (NOW + datetime.timedelta(days=offset)).date()
    return [e for e in EVENTS if e["start"].date() == day]

def mute_key(e):
    return f'{e["src"]}|{e["title"]}'

def detail_attr(fields, key=None):
    payload = {"fields": fields}
    if key: payload["key"] = key
    return html.escape(json.dumps(payload, ensure_ascii=False), quote=True)

def ev_row(e, show_day=False):
    t = e["start"].strftime("%a %d") if show_day and e["allday"] else (
        e["start"].strftime("%a %d %H:%M") if show_day else
        ("all-day" if e["allday"] else e["start"].strftime("%H:%M")))
    s = SRC[e["src"]]
    key = mute_key(e)
    cls = "evrow" + (" muted" if key in MUTED else "")
    cal = f' <span class="cal">{html.escape(e["cal"])}</span>' if e["cal"] not in ("Secuura", "Datasec") else ""
    fields = [("What", e["title"]), ("When", e["start"].strftime("%A %d %B, %H:%M") if not e["allday"]
               else e["start"].strftime("%A %d %B") + " (all-day)"),
              ("Source", s["label"] + (f' · {e["cal"]}' if e["cal"] not in ("Secuura", "Datasec") else ""))]
    if e.get("loc"): fields.append(("Where", e["loc"]))
    return (f'<li class="{cls}" data-detail="{detail_attr(fields, key)}" data-key="{html.escape(key, quote=True)}" title="click for details">'
            f'<span class="dot" style="background:{s["color"]}"></span>'
            f'<span class="src">{s["label"]}</span><span class="time">{t}</span>'
            f'<span class="ev">{html.escape(e["title"])}</span>{cal}</li>')

def collapse_allday(evs):
    """Collapse multi-day all-day repeats (same title) into one row per run."""
    out, runs = [], {}
    for e in evs:
        if e["allday"]:
            runs.setdefault(e["title"], []).append(e)
        else:
            out.append(("ev", e))
    for title, group in runs.items():
        if len(group) <= 2:
            out.extend(("ev", g) for g in group)
        else:
            out.append(("run", group))
    def sortkey(item):
        return item[1]["start"] if item[0] == "ev" else item[1][0]["start"]
    return sorted(out, key=sortkey)

def run_row(group):
    e = group[0]; last = group[-1]
    s = SRC[e["src"]]
    key = mute_key(e)
    cls = "evrow" + (" muted" if key in MUTED else "")
    rng = f'{e["start"].strftime("%a %d")}–{last["start"].strftime("%a %d")}'
    fields = [("What", e["title"]), ("When", f'{rng} · all-day, {len(group)} days'), ("Source", s["label"])]
    return (f'<li class="{cls}" data-detail="{detail_attr(fields, key)}" data-key="{html.escape(key, quote=True)}" title="click for details">'
            f'<span class="dot" style="background:{s["color"]}"></span>'
            f'<span class="src">{s["label"]}</span><span class="time">{rng}</span>'
            f'<span class="ev">{html.escape(e["title"])} <span class="cal">&times;{len(group)} days</span></span></li>')

def tile_stats():
    n_today = len(day_events(0))
    n_active = len(linear["data"]["active"]) if linear else 0
    n_flags = len(brain["data"]["flags"]) if brain else 0
    nxt = next((e for e in EVENTS if not e["allday"] and e["start"] > NOW), None)
    nxt_txt = f'{nxt["start"].strftime("%H:%M")} {nxt["title"][:40]}' if nxt else "—"
    return f"""<div class="tiles">
 <div class="tile"><div class="v">{n_today}</div><div class="k">events today</div></div>
 <div class="tile"><div class="v">{n_active}</div><div class="k">WED in progress</div></div>
 <div class="tile"><div class="v">{n_flags}</div><div class="k">flags watched</div></div>
 <div class="tile wide"><div class="v small">{html.escape(nxt_txt)}</div><div class="k">next timed event</div></div>
</div>"""

def tile_calendars():
    out = []
    for off, name in ((0, "Today"), (1, "Tomorrow")):
        evs = day_events(off)
        parts, now_done = [], off != 0
        for e in evs:
            if not now_done and not e["allday"] and e["start"] > NOW:
                parts.append(f'<li class="nowline"><span>now · {NOW.strftime("%H:%M")}</span></li>')
                now_done = True
            parts.append(ev_row(e))
        if not now_done and off == 0 and evs:
            parts.append(f'<li class="nowline"><span>now · {NOW.strftime("%H:%M")}</span></li>')
        rows = "\n".join(parts) or '<li class="empty">nothing scheduled</li>'
        out.append(f"<h3>{name} <span class='count'>{len(evs)}</span></h3><ul class='events'>{rows}</ul>")
    out.append("<h3>Week by company <span class='count'>click to expand</span></h3>")
    for src, meta in SRC.items():
        wk = [e for e in EVENTS if e["src"] == src and 0 <= (e["start"].date() - NOW.date()).days <= 7]
        items = collapse_allday(wk)
        rows = "\n".join(run_row(it[1]) if it[0] == "run" else ev_row(it[1], show_day=True)
                          for it in items) or '<li class="empty">nothing this week</li>'
        out.append(
            f"<details class='srcweek'><summary><span class='dot' style='background:{meta['color']}'></span>"
            f"{meta['label']} <span class='count'>{len(wk)}</span>"
            f"<a class='headlink' href='area_{src}.html'>full page &#10530;</a></summary>"
            f"<ul class='events'>{rows}</ul></details>")
    return "\n".join(out)

def tile_flags():
    rows = ""
    for p in PINNED:
        rows += (f'<li data-pin="{html.escape(p, quote=True)}"><span class="flagdue">&#128204; pinned</span>'
                 f'<span class="ev">{html.escape(p)}</span></li>')
    for f in (brain["data"]["flags"] if brain else []):
        rows += (f'<li><span class="flagdue">{html.escape(f["due"])}</span>'
                 f'<span class="ev">{html.escape(f["what"])}</span></li>')
    return f"<ul class='events plain'>{rows}</ul>" if rows else '<p class="empty">no flags</p>'

def tile_family():
    fam = [e for e in EVENTS if e["cal"] == "Family" and
           (KID_PAT.search(e["title"]) or "school" in e["title"].lower())][:12]
    if not fam:
        return '<p class="empty">no kid/school items in the next stretch</p>'
    rows = "\n".join(
        f'<li><span class="time">{e["start"].strftime("%a %d %H:%M") if not e["allday"] else e["start"].strftime("%a %d")}</span>'
        f'<span class="ev">{html.escape(e["title"])}</span></li>' for e in fam)
    return f"<ul class='events plain'>{rows}</ul><p class='note'>Family calendar is display-only (cowork agent's territory).</p>"

PRIO = {0: "", 1: "P1", 2: "P2", 3: "P3", 4: "P4"}

def issue_row(i, todo=False):
    due = f' <span class="flagdue">due {i["dueDate"]}</span>' if i.get("dueDate") else ""
    pr = PRIO.get(i.get("priority") or 0, "")
    badge = f'<span class="prio p{i.get("priority")}">{pr}</span>' if pr else ""
    btns = '<span class="acts">'
    if (i.get("priority") or 5) > 1:
        btns += f'<button data-act="prioritise" data-id="{i["identifier"]}" title="set Urgent">&#9650;</button>'
    if todo:
        btns += f'<button data-act="start" data-id="{i["identifier"]}" title="move to In Progress">&#9654;</button>'
    btns += "</span>"
    url = f'https://linear.app/wednesday-agent/issue/{i["identifier"]}'
    return (f'<li data-wed="{i["identifier"]}"><a class="time tlink" href="{url}" target="_blank" rel="noopener">{i["identifier"]}</a>{badge}'
            f'{ack_dot(i["identifier"])}<span class="ev">{html.escape(i["title"])}</span>{due}{btns}</li>')

def tile_board():
    if not linear:
        return '<p class="empty">Linear feed unavailable</p>'
    a = "\n".join(issue_row(i) for i in linear["data"]["active"]) or '<li class="empty">none</li>'
    t = "\n".join(issue_row(i, todo=True) for i in linear["data"]["todo"][:10]) or '<li class="empty">none</li>'
    addbox = ("<div class='addbox'>"
              "<input id='add-title' type='text' maxlength='200' placeholder='add an item…'>"
              "<select id='add-prio'><option value='1'>P1 urgent</option><option value='2'>P2 high</option>"
              "<option value='3' selected>P3 medium</option><option value='4'>P4 low</option></select>"
              "<button id='add-btn'>add</button><span id='add-msg'></span></div>")
    return (f"<h3>In progress</h3><ul class='events plain'>{a}</ul>"
            f"<h3>Up next</h3><ul class='events plain'>{t}</ul>{addbox}")

NEWS_LABELS = {"world": "War & geopolitics", "tech": "Tech", "quantum": "Quantum",
               "security": "Security", "biotech": "Biotech & medicine"}

def news_row(n):
    fields = [("Headline", n["title"]), ("Source", f'{n["source"]} · {n["date"]}'),
              ("Summary", n["summary"] or "(no summary in feed)")]
    payload = {"fields": fields, "url": n["link"]}
    d = html.escape(json.dumps(payload, ensure_ascii=False), quote=True)
    take = html.escape((n["summary"] or "")[:140])
    key = f'news|{n["title"]}'
    return (f'<li class="evrow newsrow" data-detail="{d}" data-key="{html.escape(key, quote=True)}">'
            f'<div class="nhead">{html.escape(n["title"])}</div>'
            f'<div class="ntake">{take}</div></li>')

def tile_news():
    if not news or not any(news["data"]["topics"].values()):
        return '<p class="empty">news feeds unavailable</p>'
    out = []
    for topic, label in NEWS_LABELS.items():
        items = [n for n in news["data"]["topics"].get(topic, [])
                 if f'news|{n["title"]}' not in ARCHIVED][:3]
        if not items:
            continue
        rows = "".join(news_row(n) for n in items)
        out.append(f"<details class='srcweek'><summary>{label} <span class='count'>{len(items)}</span></summary>"
                   f"<ul class='events plain newslist'>{rows}</ul></details>")
    out.append('<p class="note">takes are source summaries for now — Wednesday-curated takes arrive with the morning-generation duty · click a headline for the full summary + article link</p>')
    return "\n".join(out)

def focus_chip():
    if not FOCUS or not FOCUS.get("text"):
        return ""
    return (f'<span id="focuschip" title="set via right-click &#9654; do now">&#9654; '
            f'{html.escape(FOCUS["text"][:90])}'
            f'<button id="focus-clear" title="clear focus">&#10005;</button></span>')

def legend_html():
    parts = []
    if "datasec" not in HIDDEN_GROUPS: parts.append(("var(--series-1)", "Datasec", "datasec"))
    if "secuura" not in HIDDEN_GROUPS: parts.append(("var(--series-2)", "Secuura", "secuura"))
    for g, l in (("personal", "Personal"), ("family", "Family")):
        if g not in HIDDEN_GROUPS:
            parts.append(("var(--series-3)", l, g))
    return "&nbsp; ".join(
        f'<span class="legchip" data-group="{g}" title="click to hide {l} everywhere">'
        f'<span class="dot" style="background:{c}"></span> {l}</span>' for c, l, g in parts)

def tile_chat():
    mode_btn = ('<button id="chat-mode" class="chatmode" data-mode="sidebar" '
                'title="open the chat-with-Wed view (left column, live)">&#9634; chat with Wed</button>')
    rows = ""
    for m in chat_log[-2:]:
        extra = ""
        if m["role"] == "kam":   # ack status + action-now only make sense on Kam's messages
            extra = (ack_line(m["ts"]) +
                     f'<button class="acknow" data-key="{html.escape(m["ts"], quote=True)}" '
                     f'data-label="{html.escape(m["text"][:200], quote=True)}" '
                     f'title="ask Wednesday to action this now">&#9889; action now</button>')
        rows += (f'<div class="msg {m["role"]}"><span class="who">{"You" if m["role"] == "kam" else "Wednesday"}</span>'
                 f'<span class="mts">{m["ts"][11:16]}</span><div class="mtext">{html.escape(m["text"])}</div>{extra}</div>')
    rows = rows or '<p class="empty">say something…</p>'
    box = ('<div class="chatinput"><input id="chat-text" type="text" maxlength="2000" '
           'placeholder="message Wednesday…"><button id="chat-send">send</button></div>')
    return (f'{mode_btn}<div class="chatlog">{rows}</div>'
            f'{box}<p class="note">async channel — read at every boot & check-in</p>')

def chat_sidebar():
    """The chat-with-Wed view: fixed left column, live chat, terminal-mirror styling."""
    return f"""<aside id="chatside">
 <div class="cs-head"><span class="cs-title">chat with Wed</span>
  <span class="cs-live" id="cs-live">&#9679; live</span>
  <button id="chat-mode" data-mode="message" title="back to the compact tile">&#9642; compact</button></div>
 <div class="chatlog term" id="cs-log"></div>
 <div class="chatinput term"><span class="cs-prompt">&gt;</span>
  <input id="chat-text" type="text" maxlength="2000" placeholder="message Wednesday…" autocomplete="off">
  <button id="chat-send">send</button></div>
 <p class="note">live mirror of the message log (4s poll) — Wednesday replies from her session at boot &amp; checkpoints</p>
</aside>"""

def tile_tickets():
    out = []
    if linear:
        act = linear["data"]["active"]
        rows = "".join(f'<li data-wed="{i["identifier"]}"><span class="time">{i["identifier"]}</span>{ack_dot(i["identifier"])}'
                       f'<span class="ev">{html.escape(i["title"])}</span></li>' for i in act[:6])
        out.append(f"<details class='srcweek' open><summary>Wednesday <span class='count'>live · "
                   f"{len(act)} in progress</span></summary><ul class='events plain'>{rows}</ul></details>")
    for p in (tickets["data"]["projects"] if tickets else []):
        rows = ""
        for it in p["items"]:
            k = "ticket|" + p["client"] + "/" + p["project"] + "|" + it[:80]
            if k in ARCHIVED:   # same row-hide filter events + news apply
                continue
            rows += (f'<li data-key="{html.escape(k, quote=True)}">{ack_dot(k)}'
                     f'<span class="ev">{html.escape(it)}</span></li>')
        rows = rows or '<li class="empty">nothing carried</li>'
        out.append(f"<details class='srcweek'><summary>{html.escape(p['client'])} / "
                   f"{html.escape(p['project'])} <span class='count'>as of {p['updated']}</span></summary>"
                   f"<ul class='events plain'>{rows}</ul></details>")
    out.append('<p class="note">Client boards are cached entry-card snapshots; live client feeds arrive with the Studio/fleet session.</p>')
    return "\n".join(out)

def park_row(it):
    fields = [("What", it["title"]), ("One-liner", it["one_liner"] or "—"),
              ("Mode", "Wednesday researches it" if it["mode"] == "research" else "just parked"),
              ("Status", it["status"] + (f' → {it["promoted_to"]}' if it["promoted_to"] else "")),
              ("Added", f'{it["date"]}' + (f' · {it["source"]}' if it["source"] else ""))]
    fields.append(("Full note", it["body"]))
    payload = {"fields": fields,
               "park": {"file": it["file"], "title": it["title"], "status": it["status"]}}
    d = html.escape(json.dumps(payload, ensure_ascii=False), quote=True)
    badge = f'<span class="pmode {it["mode"]}">{html.escape(it["mode"])}</span>'
    enr = ('<span class="penr" title="research notes attached">&#9670;</span>'
           if it["research"] else "")
    status = f'<span class="cal">{html.escape(it["status"])}</span>' if it["status"] != "open" else ""
    return (f'<li class="evrow parkrow" data-detail="{d}" title="click for details">'
            f'{badge}<span class="ev">{html.escape(it["title"])}</span>{enr}{status}</li>')

def tile_parking():
    items = [i for i in (parking["data"]["items"] if parking else [])
             if i.get("status") != "dropped"]
    rows = "".join(park_row(i) for i in items) or '<li class="empty">nothing parked</li>'
    addbox = ("<div class='addbox parkadd'>"
              "<input id='park-text' type='text' maxlength='500' placeholder='park an idea&#8230; (one-liner)'>"
              "<input id='park-src' type='text' maxlength='200' placeholder='source (optional)'>"
              "</div><div class='addbox parkchoice'>"
              "<button id='park-add-p' title='save it for later, no action'>just park it</button>"
              "<button id='park-add-r' title='Wednesday researches it next session'>Wednesday researches it</button>"
              "<span id='park-msg'></span></div>")
    return (f"<ul class='events plain'>{rows}</ul>{addbox}"
            "<p class='note'>brain files in 0_Brain/parkinglot — &#9670; = research notes attached · "
            "click a row to read / promote / drop</p>")

def tile_email():
    if not agentmail:
        return '<p class="empty">Agent Mail feed unavailable</p>'
    rows = ""
    for m in agentmail["data"]["messages"]:
        ts = m["ts"][5:16].replace("T", " ")
        attn = '<span class="attn">&#9873;</span>' if m["attn"] else ""
        inboxes = "+".join(m.get("inboxes", [m.get("inbox", "?")]))
        fields = [("Subject", m["subject"]), ("From", m["from"]), ("Inboxes", inboxes),
                  ("Received", m["ts"][:16].replace("T", " "))]
        if m["attn"]: fields.append(("Attention", "QUESTION — check whether an ANSWER went out"))
        rows += (f'<li class="evrow{" needsack" if m["attn"] else ""}" data-detail="{detail_attr(fields)}">{attn}'
                 f'<span class="time">{ts}</span><span class="src">{html.escape(inboxes[:16])}</span>'
                 f'<span class="ev">{html.escape(m["subject"][:80])}</span></li>')
    return (f"<ul class='events plain'>{rows}</ul>"
            "<p class='note'>fleet inboxes (wednesday-agent + coagent), read-only — acks stay session-scoped; "
            "your personal mailboxes join in Phase 2.</p>")

TILES = {
    "stats":     ("Overview",           tile_stats),
    "calendars": ("Calendars",          tile_calendars),
    "flags":     ("Today's flags",      tile_flags),
    "family":    ("Family",             tile_family),
    "board":     ("Coding — WED board", tile_board),
    "chat":      ("Chat with Wednesday", tile_chat),
    "tickets":   ("Tickets by client",   tile_tickets),
    "email":     ("Email flags",         tile_email),
    "news":      ("News",               tile_news),
    "parkinglot": ("Parking lot",        tile_parking),
}

def feed_health():
    bits = []
    for name, obj in (("personal", personal), ("secuura", secuura), ("datasec", datasec),
                      ("linear", linear), ("brain", brain)):
        ok = obj is not None and "error" not in obj
        ts = obj.get("collected_at", "")[11:16] if obj else "—"
        bits.append(f'<span class="{"ok" if ok else "bad"}">{name} {ts}</span>')
    return " · ".join(bits)

TILE_PAGES = {
    "family": '<a class="headlink" href="area_family.html">full page &#10530;</a>',
    "board": '<a class="headlink" href="area_board.html">full page &#10530;</a>',
    "news": '<a class="headlink" href="area_news.html">full page &#10530;</a>',
}

def render_tiles():
    out = []
    for tid in ORDER:
        if tid in HIDDEN_TILES:
            continue
        if tid == "chat" and CHAT_MODE == "sidebar":
            continue  # chat lives in the fixed left column in this view
        if tid in SEP_BY_TILE:   # zone boundary: close the grid, rule + label, open a new grid
            out.append(f'</div><div class="gridsep" data-before="{tid}">'
                       f'<span>{html.escape(SEP_BY_TILE[tid])}</span></div><div class="grid">')
        title, fn = TILES[tid]
        scale = float(SCALES.get(tid, 1.0))
        sz = SIZES.get(tid, {})
        w = int(sz.get("w", 1)); h = int(sz.get("h", 0))
        tint = TINT_COLORS.get(TINTS.get(tid, ""))
        style = f"font-size:{scale}em" + (f";background:{tint}" if tint else "")
        out.append(
            f'<section class="tilebox" data-tile="{tid}" data-w="{w}" data-h="{h}" style="{style}">'
            f'<div class="tilehead"><span class="grip" title="drag to move">&#8942;&#8942;</span>'
            f'<h2>{title}</h2>'
            f'{TILE_PAGES.get(tid, "")}'
            f'<span class="sizer">'
            f'<button data-size="-" title="smaller text">A&#8722;</button>'
            f'<button data-size="+" title="bigger text">A+</button>'
            f'<button data-dim="w-" title="narrower">&#8676;</button>'
            f'<button data-dim="w+" title="wider">&#8677;</button>'
            f'<button data-dim="h-" title="shorter (0 = full height)">&#8593;</button>'
            f'<button data-dim="h+" title="taller / adds scroller">&#8595;</button>'
            f'</span></div>'
            f'<div class="tilebody">{fn()}</div></section>')
    return "\n".join(out)

SUBCSS = """
:root { color-scheme: dark;
  --surface-1:#1a1a19; --surface-2:#232322; --line:#33332f;
  --text-primary:#ffffff; --text-secondary:#c3c2b7; --text-muted:#8a897f;
  --series-1:#3987e5; --series-2:#d95926; --series-3:#199e70; }
* { box-sizing:border-box; margin:0; }
body { background:var(--surface-1); color:var(--text-primary);
  font:15px/1.5 -apple-system, "SF Pro Text", Helvetica, Arial, sans-serif;
  padding:18px 22px; max-width:900px; margin:0 auto; }
a.back { color:var(--text-muted); text-decoration:none; font-size:13px; }
a.back:hover { color:var(--text-primary); }
h1 { font-size:20px; font-weight:650; margin:6px 0 14px; }
h3 { font-size:12.5px; font-weight:600; color:var(--text-secondary);
  text-transform:uppercase; letter-spacing:.04em; margin:16px 0 4px; }
section { background:var(--surface-2); border:1px solid var(--line); border-radius:10px;
  padding:14px 16px; margin-bottom:14px; }
ul { list-style:none; }
li { display:flex; gap:8px; align-items:baseline; padding:4px 0; border-bottom:1px solid var(--line); }
li:last-child { border-bottom:none; }
.dot { width:8px; height:8px; border-radius:50%; display:inline-block; flex:none; align-self:center; }
.time { color:var(--text-secondary); font-variant-numeric:tabular-nums; font-size:.88em; width:7em; flex:none; }
.ev { color:var(--text-primary); }
.cal, .note, .empty { color:var(--text-muted); font-size:.85em; }
.muted { font-size:60%; opacity:.6; }
.nhead { color:var(--text-primary); font-weight:600; }
.ntake { color:var(--text-secondary); font-size:.9em; margin:2px 0 4px; }
.nsrc { color:var(--text-muted); font-size:.78em; }
.newsitem { display:block; }
a.art { color:var(--series-1); font-size:.85em; text-decoration:none; }
a.art:hover { text-decoration:underline; }
.tlink { color:var(--text-secondary); text-decoration:none; }
.tlink:hover { color:var(--text-primary); text-decoration:underline; }
"""

def sub_ev_row(e):
    key = mute_key(e)
    cls = "muted" if key in MUTED else ""
    t = e["start"].strftime("%a %d") if e["allday"] else e["start"].strftime("%a %d %H:%M")
    s = SRC[e["src"]]
    cal = f' <span class="cal">{html.escape(e["cal"])}</span>' if e["cal"] not in ("Secuura", "Datasec") else ""
    loc = f' <span class="cal">{html.escape(e.get("loc", ""))}</span>' if e.get("loc") else ""
    return (f'<li class="{cls}"><span class="dot" style="background:{s["color"]}"></span>'
            f'<span class="time">{t}</span><span class="ev">{html.escape(e["title"])}</span>{cal}{loc}</li>')

def render_subpage(fname, title, body):
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{html.escape(title)} — Wednesday</title><style>{SUBCSS}</style></head><body>'
            f'<a class="back" href="index.html">&larr; dashboard</a><h1>{html.escape(title)}</h1>'
            f'{body}<p class="note">generated {NOW.strftime("%H:%M")} · read-only</p></body></html>')
    (SITE / fname).write_text(page)

def area_week_html(pred):
    evs = [e for e in EVENTS if pred(e)]
    if not evs:
        return '<p class="empty">nothing in the window</p>'
    out, cur = [], None
    for e in evs:
        d = e["start"].strftime("%A %d %B")
        if d != cur:
            if cur is not None: out.append("</ul>")
            out.append(f"<h3>{d}</h3><ul>")
            cur = d
        out.append(sub_ev_row(e))
    out.append("</ul>")
    return "".join(out)

def area_tickets_html(client):
    out = []
    for pr in (tickets["data"]["projects"] if tickets else []):
        if pr["client"].lower() != client.lower():
            continue
        rows = "".join(f'<li><span class="ev">{html.escape(it)}</span></li>' for it in pr["items"]) or                '<li class="empty">nothing carried</li>'
        out.append(f'<h3>{html.escape(pr["project"])} <span class="cal">as of {pr["updated"]}</span></h3><ul>{rows}</ul>')
    return "".join(out) or '<p class="empty">no cached project cards</p>'

def area_mail_html(needle):
    if not agentmail:
        return '<p class="empty">no mail feed</p>'
    rows = ""
    for m in agentmail["data"]["messages"]:
        if needle.lower() in m["subject"].lower():
            rows += (f'<li><span class="time">{m["ts"][5:16].replace("T", " ")}</span>'
                     f'<span class="ev">{html.escape(m["subject"][:110])}</span></li>')
    return f"<ul>{rows}</ul>" if rows else '<p class="empty">no recent fleet mail mentioning this area</p>'

def write_subpages():
    for g, title, needle in (("datasec", "Datasec", "Datasec"), ("secuura", "Secuura", "Secuura")):
        body = (f'<section><h3 style="margin-top:0">Week ahead</h3>'
                f'{area_week_html(lambda e, g=g: e["src"] == g)}</section>'
                f'<section><h3 style="margin-top:0">Projects & carried items</h3>{area_tickets_html(title)}</section>'
                f'<section><h3 style="margin-top:0">Recent fleet mail</h3>{area_mail_html(needle)}</section>')
        render_subpage(f"area_{g}.html", title, body)
    render_subpage("area_personal.html", "Personal",
        f'<section>{area_week_html(lambda e: e["src"] == "personal" and e["cal"] != "Family")}</section>')
    fam_body = (f'<section>{area_week_html(lambda e: e["cal"] == "Family")}</section>'
                '<p class="note">Family calendar is display-only (cowork agent&#39;s territory).</p>')
    render_subpage("area_family.html", "Family", fam_body)
    if linear:
        rows_a = "".join(f'<li><a class="tlink time" href="https://linear.app/wednesday-agent/issue/{i["identifier"]}" target="_blank" rel="noopener">{i["identifier"]}</a>'
                         f'<span class="ev">{html.escape(i["title"])}</span></li>' for i in linear["data"]["active"])
        rows_t = "".join(f'<li><a class="tlink time" href="https://linear.app/wednesday-agent/issue/{i["identifier"]}" target="_blank" rel="noopener">{i["identifier"]}</a>'
                         f'<span class="ev">{html.escape(i["title"])}</span></li>' for i in linear["data"]["todo"])
        render_subpage("area_board.html", "WED board",
            f'<section><h3 style="margin-top:0">In progress</h3><ul>{rows_a}</ul>'
            f'<h3>Up next</h3><ul>{rows_t}</ul></section>')
    if news:
        parts = []
        for topic, label in NEWS_LABELS.items():
            items = news["data"]["topics"].get(topic, [])
            if not items:
                continue
            rows = "".join(
                f'<li class="newsitem"><div class="nhead">{html.escape(n["title"])}</div>'
                f'<div class="ntake">{html.escape(n["summary"])}</div>'
                f'<span class="nsrc">{html.escape(n["source"])} · {html.escape(n["date"])}</span> '
                f'<a class="art" href="{html.escape(n["link"], quote=True)}" target="_blank" rel="noopener">open article &#8599;</a></li>'
                for n in items)
            parts.append(f'<section><h3 style="margin-top:0">{label}</h3><ul>{rows}</ul></section>')
        render_subpage("area_news.html", "News", "".join(parts))

def views_panel_html():
    """Favourite-views dropdown panel: list saved views (apply / delete) + save-as box."""
    rows = "".join(
        f'<div class="vrow"><button class="vapply" data-name="{html.escape(n, quote=True)}" '
        f'title="apply this view">{html.escape(n)}</button>'
        f'<button class="vdel" data-name="{html.escape(n, quote=True)}" title="delete this view">&#10005;</button></div>'
        for n in VIEWS)
    if not rows:
        rows = '<p class="vempty">no saved views yet — arrange the board, then save it here</p>'
    return (f'<div id="views-panel" hidden><h4>Favourite views</h4>{rows}'
            f'<div class="vsave"><input id="view-name" type="text" maxlength="40" '
            f'placeholder="save current as&#8230;"><button id="view-save">save</button></div>'
            f'<span id="views-msg" class="verr"></span>'
            f'<p class="cpnote" style="margin-top:6px">a view snapshots the whole layout '
            f'(order, sizes, tints, separators, hidden tiles &amp; sources, chat mode) &middot; max 12</p></div>')

def status_panels_html():
    """Topbar "actioning" / "archived" panels. Lifecycle rule: ack state "done"
    renders under ARCHIVED, not actioning (Wednesday sets done out-of-band)."""
    acting_rows = []
    for k in ACK:
        a = ack_get(k)
        if a and a["state"] in ("actioning", "action_requested"):
            icon, col = ACK_META[a["state"]]
            lbl = str(a.get("label") or k)   # entries without labels show the raw key
            ts = (a.get("ts") or "")[5:16].replace("T", " ")
            acting_rows.append(
                f'<div class="strow"><span style="color:{col}" title="{a["state"].replace("_", " ")}">{icon}</span>'
                f'<span class="stlabel">{html.escape(lbl[:90])}</span><span class="sts">{ts}</span></div>')
    arch_rows, logged = [], set()
    for e in reversed(ARCHLOG):   # newest first
        if not isinstance(e, dict):
            continue
        logged.add(e.get("key_or_id"))
        lbl = str(e.get("label") or e.get("key_or_id") or "?")
        ts = str(e.get("ts") or "")[5:16].replace("T", " ")
        arch_rows.append(f'<div class="strow"><span class="sticon">&#9634;</span>'
                         f'<span class="stlabel">{html.escape(lbl[:90])}</span><span class="sts">{ts}</span></div>')
    for k in ACK:
        a = ack_get(k)
        if a and a["state"] == "done":
            lbl = str(a.get("label") or k)
            ts = (a.get("ts") or "")[5:16].replace("T", " ")
            arch_rows.append(f'<div class="strow"><span style="color:#199e70" title="done">&#10003;</span>'
                             f'<span class="stlabel">{html.escape(lbl[:90])}</span><span class="sts">{ts}</span></div>')
    for k in sorted(ARCHIVED):   # legacy row-hide archives with no log entry / label
        if k not in logged:
            arch_rows.append(f'<div class="strow"><span class="sticon">&#9634;</span>'
                             f'<span class="stlabel">{html.escape(str(k)[:90])}</span></div>')
    n_act, n_arch = len(acting_rows), len(arch_rows)
    acting = "".join(acting_rows) or '<p class="vempty">nothing being actioned right now</p>'
    arch = "".join(arch_rows) or '<p class="vempty">nothing archived yet</p>'
    panels = (f'<div id="acting-panel" hidden><h4>Being actioned</h4>{acting}'
              f'<p class="cpnote" style="margin-top:6px">&#9889; action requested &middot; '
              f'&#9679; Wednesday actioning &mdash; states are written by Wednesday&#39;s own '
              f'session, never faked by the dashboard</p></div>'
              f'<div id="archived-panel" hidden><h4>Archived</h4>{arch}</div>')
    return n_act, n_arch, panels

N_ACTING, N_ARCHIVED, STATUS_PANELS = status_panels_html()
ACTING_BTN = "&#9679; actioning" + (f" ({N_ACTING})" if N_ACTING else "")
ARCHIVED_BTN = "&#9634; archived" + (f" ({N_ARCHIVED})" if N_ARCHIVED else "")

def customise_tile_rows():
    out = []
    for tid in TILE_ORDER_DEFAULT:
        cur = TINTS.get(tid, "none")
        opts = f'<option value="none"{" selected" if cur == "none" else ""}>no tint</option>' + "".join(
            f'<option value="{k}" style="background:{c}"{" selected" if k == cur else ""}>{k}</option>'
            for k, c in TINT_COLORS.items())
        selstyle = f' style="background:{TINT_COLORS[cur]}"' if cur in TINT_COLORS else ""
        sep = SEP_BY_TILE.get(tid)
        out.append(
            f'<div class="cprow"><label><input type="checkbox" data-kind="tile" value="{tid}"'
            f'{" checked" if tid not in HIDDEN_TILES else ""}> {TILES[tid][0]}</label>'
            f'<select class="tintsel" data-tile="{tid}" title="tile background tint"{selstyle}>{opts}</select>'
            f'<input type="checkbox" class="sepchk" data-tile="{tid}" title="separator above this tile"'
            f'{" checked" if sep is not None else ""}>'
            f'<input type="text" class="seplab" data-tile="{tid}" maxlength="40" '
            f'placeholder="section label" value="{html.escape(sep or "", quote=True)}"></div>')
    return "".join(out)

PAGE = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wednesday — Day Dashboard</title>
<style>
:root {{ color-scheme: dark;
  --surface-1:#1a1a19; --surface-2:#232322; --line:#33332f;
  --text-primary:#ffffff; --text-secondary:#c3c2b7; --text-muted:#8a897f;
  --series-1:#3987e5; --series-2:#d95926; --series-3:#199e70; }}
* {{ box-sizing:border-box; margin:0; }}
body {{ background:var(--surface-1); color:var(--text-primary);
  font:15px/1.5 -apple-system, "SF Pro Text", Helvetica, Arial, sans-serif; padding:18px 22px; }}
.topbar {{ display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;
  position:sticky; top:0; z-index:40; background:var(--surface-1); padding:6px 0 8px;
  border-bottom:1px solid var(--line); }}
.topbar h1 {{ font-size:21px; font-weight:650; }}
.topbar .sub {{ color:var(--text-secondary); }}
.topbar .legend {{ color:var(--text-secondary); font-size:13px; }}
.topbar .menu {{ margin-left:auto; }}
.menu button {{ background:var(--surface-2); color:var(--text-secondary); border:1px solid var(--line);
  border-radius:7px; font:inherit; font-size:13px; padding:5px 12px; cursor:pointer; }}
.menu button.on, .menu button:hover {{ color:var(--text-primary); border-color:var(--text-muted); }}
.topbar .menu {{ position:relative; }}
#burger-drop {{ position:absolute; right:0; top:calc(100% + 6px); z-index:60; display:flex;
  flex-direction:column; gap:6px; background:var(--surface-2); border:1px solid var(--line);
  border-radius:8px; padding:8px; min-width:190px; box-shadow:0 6px 24px rgba(0,0,0,.45); }}
#burger-drop button {{ text-align:left; }}
#burger-drop[hidden] {{ display:none; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:14px; margin-top:14px;
  grid-auto-rows:8px; grid-auto-flow:dense; }}
.tilebox {{ background:var(--surface-2); border:1px solid var(--line); border-radius:10px; padding:14px 16px;
  overflow:hidden; }}
.tilebox.scroll .tilebody {{ overflow-y:auto; height:calc(100% - 34px); scrollbar-width:thin; }}
.tilehead {{ display:flex; align-items:center; gap:8px; margin-bottom:8px; }}
.tilehead h2 {{ font-size:1.0em; font-weight:650; }}
.grip {{ color:var(--text-muted); cursor:grab; display:none; letter-spacing:-3px; }}
.sizer {{ margin-left:auto; display:none; gap:4px; }}
.sizer button {{ background:var(--surface-1); color:var(--text-secondary); border:1px solid var(--line);
  border-radius:5px; font-size:11px; padding:1px 7px; cursor:pointer; }}
body.organise .grip, body.organise .sizer {{ display:inline-flex; }}
body.organise .tilebox {{ outline:1px dashed var(--text-muted); }}
.tilebox.dragging {{ opacity:.4; }}
.tiles {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:10px; }}
.tile {{ background:var(--surface-1); border:1px solid var(--line); border-radius:8px; padding:10px 12px; }}
.tile .v {{ font-size:24px; font-weight:700; font-variant-numeric:tabular-nums; }}
.tile .v.small {{ font-size:14px; font-weight:600; padding-top:5px; }}
.tile .k {{ color:var(--text-muted); font-size:11.5px; margin-top:2px; }}
section h3 {{ font-size:.83em; font-weight:600; color:var(--text-secondary);
  text-transform:uppercase; letter-spacing:.04em; margin:10px 0 4px; }}
.count {{ color:var(--text-muted); font-weight:400; text-transform:none; letter-spacing:0; }}
ul.events {{ list-style:none; }}
ul.events li {{ display:flex; gap:8px; align-items:baseline; padding:3px 0; border-bottom:1px solid var(--line); }}
ul.events li:last-child {{ border-bottom:none; }}
.dot {{ width:8px; height:8px; border-radius:50%; display:inline-block; flex:none; align-self:center; }}
.src {{ color:var(--text-muted); font-size:.78em; width:56px; flex:none; }}
.time {{ color:var(--text-secondary); font-variant-numeric:tabular-nums; font-size:.88em; width:4.6em; flex:none; }}
ul.plain .time {{ width:6.2em; }}
.ev {{ color:var(--text-primary); }}
.cal {{ color:var(--text-muted); font-size:.8em; }}
.flagdue {{ color:var(--text-secondary); font-size:.85em; width:6em; flex:none; font-variant-numeric:tabular-nums; }}
.empty {{ color:var(--text-muted); }}
.note {{ color:var(--text-muted); font-size:.8em; margin-top:6px; }}
.stub {{ color:var(--text-muted); font-style:italic; }}
.prio {{ font-size:.74em; font-weight:700; border-radius:4px; padding:0 5px; flex:none; align-self:center; }}
.prio.p1 {{ color:#e66767; border:1px solid #e66767; }} .prio.p2 {{ color:#c98500; border:1px solid #c98500; }}
.prio.p3, .prio.p4 {{ color:var(--text-muted); border:1px solid var(--line); }}
.acts {{ margin-left:auto; flex:none; display:flex; gap:4px; opacity:.35; }}
li:hover .acts {{ opacity:1; }}
.acts button {{ background:var(--surface-1); color:var(--text-secondary); border:1px solid var(--line);
  border-radius:5px; font-size:.74em; padding:1px 7px; cursor:pointer; }}
.acts button:hover {{ color:var(--text-primary); border-color:var(--text-muted); }}
.addbox {{ display:flex; gap:6px; margin-top:12px; }}
.addbox input[type=text] {{ flex:1; background:var(--surface-1); border:1px solid var(--line);
  color:var(--text-primary); border-radius:6px; padding:6px 9px; font:inherit; font-size:.9em; }}
.addbox select, .addbox button {{ background:var(--surface-1); color:var(--text-secondary);
  border:1px solid var(--line); border-radius:6px; font:inherit; font-size:.87em; padding:5px 8px; }}
.addbox button {{ cursor:pointer; }} .addbox button:hover {{ color:var(--text-primary); }}
#add-msg {{ align-self:center; font-size:.8em; color:var(--text-muted); }}
.pmode {{ font-size:.74em; font-weight:600; border-radius:4px; padding:0 5px; flex:none; align-self:center; }}
.pmode.parked {{ color:var(--text-muted); border:1px solid var(--line); }}
.pmode.research {{ color:var(--series-1); border:1px solid var(--series-1); }}
.penr {{ color:var(--series-3); font-size:.8em; flex:none; align-self:center; }}
.parkadd #park-src {{ flex:0 0 34%; }}
.parkchoice {{ margin-top:6px; }}
#park-msg {{ align-self:center; font-size:.8em; color:var(--text-muted); }}
#modal-park {{ margin-top:12px; display:flex; gap:6px; flex-wrap:wrap; align-items:center; }}
#modal-park[hidden] {{ display:none; }}
#modal-park button {{ background:var(--surface-1); color:var(--text-secondary); border:1px solid var(--line);
  border-radius:6px; font:inherit; font-size:13px; padding:5px 12px; cursor:pointer; }}
#modal-park button:hover {{ color:var(--text-primary); }}
#modal-park-msg {{ font-size:12px; color:var(--text-muted); }}
#modal-body {{ max-height:62vh; overflow-y:auto; scrollbar-width:thin; }}
li.mutable {{ cursor:pointer; }}
li.muted {{ font-size:50%; opacity:.55; }}
li.muted .ev, li.muted .src, li.muted .time, li.muted .cal {{ color:var(--text-muted); }}
li.muted .dot {{ opacity:.4; }}
details.srcweek {{ border-bottom:1px solid var(--line); padding:4px 0; }}
details.srcweek summary {{ cursor:pointer; color:var(--text-secondary); font-size:.9em;
  list-style:none; display:flex; gap:8px; align-items:center; padding:3px 0; }}
details.srcweek summary::before {{ content:"▸"; color:var(--text-muted); font-size:.75em; }}
details.srcweek[open] summary::before {{ content:"▾"; }}
details.srcweek .events {{ margin:2px 0 6px 18px; }}
#customise-panel {{ display:flex; gap:26px; background:var(--surface-2); border:1px solid var(--line);
  border-radius:10px; padding:14px 18px; margin-top:12px; }}
#customise-panel[hidden] {{ display:none; }}
#views-panel {{ background:var(--surface-2); border:1px solid var(--line); border-radius:10px;
  padding:12px 16px; margin-top:12px; max-width:420px; }}
#views-panel[hidden] {{ display:none; }}
#views-panel h4 {{ font-size:12px; text-transform:uppercase; letter-spacing:.05em;
  color:var(--text-secondary); margin-bottom:6px; }}
.vrow {{ display:flex; gap:6px; align-items:center; padding:2px 0; }}
.vrow .vapply {{ flex:1; text-align:left; background:var(--surface-1); color:var(--text-primary);
  border:1px solid var(--line); border-radius:6px; font:inherit; font-size:13px; padding:4px 10px; cursor:pointer; }}
.vrow .vapply:hover {{ border-color:var(--text-muted); }}
.vrow .vdel {{ background:none; border:none; color:var(--text-muted); cursor:pointer; font-size:12px; padding:2px 4px; }}
.vrow .vdel:hover {{ color:#e66767; }}
.vempty {{ color:var(--text-muted); font-size:12.5px; }}
.vsave {{ display:flex; gap:6px; margin-top:8px; }}
.vsave input {{ flex:1; background:var(--surface-1); border:1px solid var(--line); color:var(--text-primary);
  border-radius:6px; padding:5px 9px; font:inherit; font-size:13px; }}
.vsave button {{ background:var(--surface-1); color:var(--text-secondary); border:1px solid var(--line);
  border-radius:6px; font:inherit; font-size:13px; padding:4px 12px; cursor:pointer; }}
.vsave button:hover {{ color:var(--text-primary); }}
.tintsel {{ margin-left:8px; background:var(--surface-1); color:var(--text-secondary); border:1px solid var(--line);
  border-radius:5px; font:inherit; font-size:11.5px; padding:1px 4px; }}
.verr {{ color:#e66767; font-size:12px; }}
.cprow {{ display:flex; align-items:center; gap:6px; padding:2px 0; }}
.cprow label {{ min-width:150px; }}
.seplab {{ width:110px; background:var(--surface-1); border:1px solid var(--line); color:var(--text-primary);
  border-radius:5px; font:inherit; font-size:11.5px; padding:2px 6px; }}
.gridsep {{ margin:18px 0 4px; display:flex; align-items:center; gap:10px; min-height:0; }}
.gridsep::before {{ content:""; width:18px; border-top:1px solid var(--line); }}
.gridsep::after {{ content:""; flex:1; border-top:1px solid var(--line); }}
.gridsep span {{ color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:.06em;
  white-space:nowrap; }}
.gridsep span:empty {{ display:none; }}
.ackline {{ font-size:.74em; margin-top:2px; }}
.ackline.seen {{ color:var(--text-muted); }} .ackline.actioning {{ color:#3987e5; }}
.ackline.action_requested {{ color:#c98500; }} .ackline.done {{ color:#199e70; }}
.ackdot {{ width:7px; height:7px; border-radius:50%; display:inline-block; flex:none; align-self:center; }}
.msg {{ position:relative; }}
.msg .acknow {{ display:none; position:absolute; top:5px; right:0; background:var(--surface-1); color:#c98500;
  border:1px solid var(--line); border-radius:5px; font-size:10.5px; padding:1px 7px; cursor:pointer; }}
.msg:hover .acknow {{ display:inline-block; }}
.msg .acknow:hover {{ border-color:#c98500; }}
#acting-panel, #archived-panel {{ background:var(--surface-2); border:1px solid var(--line); border-radius:10px;
  padding:12px 16px; margin-top:12px; max-width:520px; }}
#acting-panel[hidden], #archived-panel[hidden] {{ display:none; }}
#acting-panel h4, #archived-panel h4 {{ font-size:12px; text-transform:uppercase; letter-spacing:.05em;
  color:var(--text-secondary); margin-bottom:6px; }}
.strow {{ display:flex; gap:8px; align-items:baseline; padding:3px 0; border-bottom:1px solid var(--line);
  font-size:13px; }}
.strow:last-child {{ border-bottom:none; }}
.stlabel {{ flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.sts {{ color:var(--text-muted); font-size:11px; white-space:nowrap; font-variant-numeric:tabular-nums; }}
.sticon {{ color:var(--text-muted); }}
.cpcol h4 {{ font-size:12px; text-transform:uppercase; letter-spacing:.05em; color:var(--text-secondary); margin-bottom:6px; }}
.cpcol label {{ display:block; font-size:13.5px; color:var(--text-primary); padding:2px 0; cursor:pointer; }}
.cpcol input {{ accent-color:var(--series-1); margin-right:6px; }}
.cpnote {{ color:var(--text-muted); font-size:12px; max-width:260px; }}
#customise-save {{ margin-top:8px; background:var(--surface-1); color:var(--text-secondary);
  border:1px solid var(--line); border-radius:6px; font:inherit; font-size:13px; padding:4px 14px; cursor:pointer; }}
#customise-save:hover {{ color:var(--text-primary); }}
.chatmode {{ position:absolute; top:12px; right:14px; background:var(--surface-1); color:var(--text-muted);
  border:1px solid var(--line); border-radius:5px; font-size:11px; padding:1px 8px; cursor:pointer; }}
.chatmode:hover {{ color:var(--text-primary); }}
.tilebox[data-tile="chat"] {{ position:relative; }}
.chatlog {{ margin:4px 0 8px; }}
.chatlog.chatfull {{ height:340px; overflow-y:auto; scrollbar-width:thin; }}
.msg {{ padding:6px 0; border-bottom:1px solid var(--line); }}
.msg .who {{ font-size:.78em; font-weight:650; color:var(--text-secondary); margin-right:8px; }}
.msg.kam .who {{ color:var(--series-1); }}
.msg .mts {{ font-size:.75em; color:var(--text-muted); }}
.msg .mtext {{ margin-top:2px; white-space:pre-wrap; }}
.chatinput {{ display:flex; gap:6px; }}
.chatinput input {{ flex:1; background:var(--surface-1); border:1px solid var(--line);
  color:var(--text-primary); border-radius:6px; padding:6px 9px; font:inherit; font-size:.9em; }}
.chatinput button {{ background:var(--surface-1); color:var(--text-secondary); border:1px solid var(--line);
  border-radius:6px; font:inherit; font-size:.87em; padding:5px 12px; cursor:pointer; }}
.chatinput button:hover {{ color:var(--text-primary); }}
.attn {{ color:#c98500; margin-right:2px; }}
.tilebox[data-tile="email"] .ev {{ white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
li.needsack .ev {{ font-weight:600; }}
.newslist li {{ display:block; }}
.nhead {{ color:var(--text-primary); font-weight:600; }}
.ntake {{ color:var(--text-muted); font-size:.85em; margin-top:1px;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }}
#modal-link {{ display:inline-block; margin:12px 12px 0 0; color:var(--series-1); font-size:13.5px; }}
.headlink {{ margin-left:auto; color:var(--text-muted); font-size:12px; text-decoration:none; }}
.headlink:hover {{ color:var(--text-primary); }}
.legchip {{ cursor:pointer; }} .legchip:hover {{ color:var(--text-primary); }}
li.nowline {{ border-bottom:none !important; padding:0 !important; }}
li.nowline span {{ display:block; width:100%; text-align:left; color:#e66767; font-size:.72em;
  border-top:1px solid #e66767; line-height:1; padding-top:1px; opacity:.8; }}
.tlink {{ text-decoration:none; }} .tlink:hover {{ text-decoration:underline; color:var(--text-primary); }}
#modal-backdrop {{ position:fixed; inset:0; background:rgba(0,0,0,.55); z-index:100;
  display:flex; align-items:center; justify-content:center; }}
#modal-backdrop[hidden] {{ display:none; }}
#modal {{ background:var(--surface-2); border:1px solid var(--line); border-radius:12px;
  padding:20px 22px; max-width:480px; width:92%; position:relative; }}
#modal-close {{ position:absolute; top:10px; right:12px; background:none; border:none;
  color:var(--text-muted); font-size:15px; cursor:pointer; }}
#modal-close:hover {{ color:var(--text-primary); }}
#modal-body .mrow {{ padding:5px 0; border-bottom:1px solid var(--line); }}
#modal-body .mrow:last-child {{ border-bottom:none; }}
#modal-body .mk {{ font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--text-muted); }}
#modal-body .mv {{ color:var(--text-primary); margin-top:1px; white-space:pre-wrap; }}
#modal-mute {{ margin-top:12px; background:var(--surface-1); color:var(--text-secondary);
  border:1px solid var(--line); border-radius:6px; font:inherit; font-size:13px; padding:5px 12px; cursor:pointer; }}
#modal-mute:hover {{ color:var(--text-primary); }}
#focuschip {{ background:var(--surface-2); border:1px solid #c98500; color:var(--text-primary);
  border-radius:7px; padding:2px 10px; font-size:13px; display:inline-flex; gap:7px; align-items:center;
  max-width:420px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
#focuschip button {{ background:none; border:none; color:var(--text-muted); cursor:pointer; font-size:11px; padding:0; }}
#focuschip button:hover {{ color:var(--text-primary); }}
#ctxmenu {{ position:fixed; z-index:200; background:var(--surface-2); border:1px solid var(--line);
  border-radius:9px; padding:4px; min-width:180px; max-width:280px; box-shadow:0 8px 24px rgba(0,0,0,.5); }}
#ctxmenu[hidden] {{ display:none; }}
#ctxmenu .cmk {{ color:var(--text-muted); font-size:11px; padding:3px 10px 5px; border-bottom:1px solid var(--line);
  margin-bottom:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
#ctxmenu button {{ display:block; width:100%; text-align:left; background:none; border:none;
  color:var(--text-primary); font:inherit; font-size:13.5px; padding:6px 10px; border-radius:6px; cursor:pointer; }}
#ctxmenu button:hover {{ background:var(--surface-1); }}
/* ── chat-with-Wed view: fixed 30% left column, terminal mirror ── */
body.chatview {{ padding-left:calc(30vw + 20px); }}
#chatside {{ position:fixed; left:0; top:0; bottom:0; width:30vw; min-width:320px; z-index:60;
  background:#141413; border-right:1px solid var(--line); display:flex; flex-direction:column;
  padding:12px 14px; }}
.cs-head {{ display:flex; align-items:center; gap:10px; padding-bottom:8px; border-bottom:1px solid var(--line); }}
.cs-title {{ font-family:"SF Mono", Menlo, monospace; font-size:14px; font-weight:700; }}
.cs-live {{ color:#199e70; font-size:11px; }}
.cs-head button {{ margin-left:auto; background:var(--surface-2); color:var(--text-muted); border:1px solid var(--line);
  border-radius:5px; font-size:11px; padding:1px 8px; cursor:pointer; }}
.cs-head button:hover {{ color:var(--text-primary); }}
.chatlog.term {{ flex:1; overflow-y:auto; scrollbar-width:thin; font-family:"SF Mono", Menlo, monospace;
  font-size:12.5px; line-height:1.5; padding:10px 2px; }}
.chatlog.term .msg {{ border:none; padding:3px 0; }}
.chatlog.term .who {{ color:var(--series-3); }}
.chatlog.term .msg.kam .who {{ color:var(--series-1); }}
.chatlog.term .mts {{ color:var(--text-muted); font-size:.85em; }}
.chatlog.term .mtext {{ white-space:pre-wrap; word-break:break-word; color:var(--text-primary); }}
.chatinput.term {{ align-items:center; border-top:1px solid var(--line); padding-top:8px; }}
.cs-prompt {{ font-family:"SF Mono", Menlo, monospace; color:var(--series-3); font-weight:700; }}
.chatinput.term input {{ font-family:"SF Mono", Menlo, monospace; font-size:12.5px; background:#1a1a19; }}
@media (max-width:900px) {{
  body.chatview {{ padding-left:12px; }}
  #chatside {{ position:static; width:auto; min-width:0; height:50vh; margin-bottom:14px;
    border:1px solid var(--line); border-radius:10px; }}
}}
@media (max-width:700px) {{
  .tilebox {{ grid-column:1 / -1 !important; }}
  .topbar h1 {{ font-size:17px; }}
  body {{ padding:10px 12px; }}
}}
footer {{ margin-top:16px; color:var(--text-muted); font-size:12px; }}
footer .ok {{ color:var(--text-secondary); }} footer .bad {{ color:#e66767; font-weight:600; }}
</style></head><body class="{"chatview" if CHAT_MODE == "sidebar" else ""}">
{chat_sidebar() if CHAT_MODE == "sidebar" else ""}
<div class="topbar">
 <h1>Wednesday — Day Dashboard</h1>
 <span class="sub">{NOW.strftime("%A %-d %B %Y · %H:%M %Z")}</span>
 <span class="legend">{legend_html()}</span>
 {focus_chip()}
 <span class="menu"><button id="burger-btn" title="menu">&#9776;</button>
 <span id="burger-drop" hidden>
 <button id="acting-btn">{ACTING_BTN}</button>
 <button id="archived-btn">{ARCHIVED_BTN}</button>
 <button id="views-btn">&#9734; view presets</button>
 <button id="preset-save-btn">&#128190; save this setup&#8230;</button>
 <button id="customise-btn">&#9881; customise</button>
 <button id="organise-btn">&#9998; organise</button>
 </span></span>
</div>
{STATUS_PANELS}
{views_panel_html()}
<div id="customise-panel" hidden>
 <div class="cpcol"><h4>Tiles</h4>{customise_tile_rows()}</div>
 <div class="cpcol"><h4>Sources</h4>{"".join(
   f'<label><input type="checkbox" data-kind="group" value="{g}"'
   f'{" checked" if g not in HIDDEN_GROUPS else ""}> {label}</label>' for g, label in GROUPS.items())}</div>
 <div class="cpcol cpnote">Source toggles filter every tile at once (calendars, counts, family, next-event). Tints give a tile a subtle background shade. Changes apply on save.<br><button id="customise-save">save</button></div>
</div>
<div id="grid"><div class="grid">
{render_tiles()}
</div></div>
<div id="ctxmenu" hidden></div>
<div id="modal-backdrop" hidden><div id="modal">
 <button id="modal-close" title="close">&#10005;</button>
 <div id="modal-body"></div>
 <button id="modal-mute" hidden>de-prioritise / restore</button>
 <div id="modal-park" hidden>
  <button id="park-promote">&#8599; promote to WED ticket</button>
  <button id="park-drop">drop</button>
  <button id="park-discuss">discuss with Wed</button>
  <span id="modal-park-msg"></span>
 </div>
</div></div>
<footer>feeds: {feed_health()} · regenerated {NOW.strftime("%H:%M:%S")} · auto-refresh 5 min (paused while organising) · right-click any row for actions · read-only everywhere</footer>
<script>
async function api(path, payload) {{
  const r = await fetch(path, {{method:"POST", headers:{{"Content-Type":"application/json"}},
    body: JSON.stringify(payload)}});
  return r.json();
}}
let organise = false;
setInterval(() => {{
  const ct = document.getElementById("chat-text");
  if (!organise && document.getElementById("customise-panel").hidden
      && document.getElementById("views-panel").hidden
      && document.getElementById("acting-panel").hidden
      && document.getElementById("archived-panel").hidden
      && !(ct && (ct.value.trim() || document.activeElement === ct))) location.reload();
}}, 300000);
// ── drill-down modal (mute lives inside it now) ──
const mb = document.getElementById("modal-backdrop"), mbody = document.getElementById("modal-body"),
      mmute = document.getElementById("modal-mute");
let modalKey = null, parkCur = null;
function openDetail(li) {{
  const d = JSON.parse(li.dataset.detail);
  mbody.innerHTML = d.fields.map(f =>
    `<div class="mrow"><div class="mk">${{f[0]}}</div><div class="mv"></div></div>`).join("");
  [...mbody.querySelectorAll(".mv")].forEach((el, i) => el.textContent = d.fields[i][1]);
  modalKey = d.key || null;
  mmute.hidden = !modalKey;
  parkCur = d.park || null;
  document.getElementById("modal-park").hidden = !parkCur;
  if (parkCur) {{
    for (const id of ["park-promote", "park-drop", "park-discuss"]) {{
      const b = document.getElementById(id); b.disabled = false;
    }}
    document.getElementById("park-promote").hidden = parkCur.status !== "open";
    document.getElementById("modal-park-msg").textContent = "";
  }}
  const oldLink = document.getElementById("modal-link");
  if (oldLink) oldLink.remove();
  if (d.url) {{
    const a = document.createElement("a");
    a.id = "modal-link"; a.href = d.url; a.target = "_blank"; a.rel = "noopener";
    a.textContent = "open article \u2197";
    document.getElementById("modal").appendChild(a);
  }}
  mb.hidden = false;
}}
document.querySelectorAll("li.evrow").forEach(li => li.addEventListener("click", (ev) => {{
  if (organise || ev.target.closest("button") || ev.target.closest("a")) return;
  openDetail(li);
}}));
// ── right-click context menu (WED-70): expand · prioritise/pin · do now · discuss · archive ──
const PINNED_JS = {json.dumps(PINNED)};
const cm = document.getElementById("ctxmenu");
function cmHide() {{ cm.hidden = true; }}
document.addEventListener("click", cmHide);
document.addEventListener("contextmenu", e => {{
  const li = e.target.closest("li[data-key], li[data-wed], li[data-pin], li.evrow");
  if (!li || organise) return;               // everywhere else keeps the native menu
  e.preventDefault();
  const wed = li.dataset.wed || null, key = li.dataset.key || null, pin = li.dataset.pin || null;
  const text = ((li.querySelector(".nhead") || li.querySelector(".ev") || li).textContent || "").trim().slice(0, 200);
  const label = wed ? wed + " — " + text : text;
  const items = [];
  if (li.dataset.detail) items.push(["expand", () => openDetail(li)]);
  else if (wed) items.push(["expand in Linear ↗",
    () => window.open("https://linear.app/wednesday-agent/issue/" + wed, "_blank")]);
  if (wed) items.push(["prioritise — set P1",
    async () => {{ await api("/api/prioritise", {{id: wed}}); location.reload(); }}]);
  else if (pin || PINNED_JS.includes(text)) items.push(["unpin from flags",
    async () => {{ await api("/api/pin", {{text: pin || text}}); location.reload(); }}]);
  else items.push(["pin to flags",
    async () => {{ await api("/api/pin", {{text}}); location.reload(); }}]);
  items.push(["do now — set focus", async () => {{
    if (wed) await api("/api/start", {{id: wed}});
    await api("/api/focus", {{text: label}});
    location.reload();
  }}]);
  const srcTile = li.closest(".tilebox");
  if ((wed || key) && srcTile && (srcTile.dataset.tile === "board" || srcTile.dataset.tile === "tickets"))
    items.push(["action now ⚡", async () => {{
      await api("/api/actionnow", {{key: wed || key, label}});
      location.reload();
    }}]);
  items.push(["discuss with Wednesday",
    async () => {{ await api("/api/chat", {{text: "Discuss: " + label}}); location.reload(); }}]);
  if (wed) items.push(["archive ticket",
    async () => {{ await api("/api/archive", {{id: wed, label}}); location.reload(); }}]);
  else if (key) items.push(["archive — hide row",
    async () => {{ await api("/api/archive", {{key, label}}); location.reload(); }}]);
  cm.innerHTML = "";
  const hd = document.createElement("div"); hd.className = "cmk"; hd.textContent = label; cm.appendChild(hd);
  for (const [lab, fn] of items) {{
    const b = document.createElement("button"); b.textContent = lab;
    b.addEventListener("click", ev => {{ ev.stopPropagation(); cmHide(); fn(); }});
    cm.appendChild(b);
  }}
  cm.hidden = false;
  cm.style.left = Math.min(e.clientX, innerWidth - cm.offsetWidth - 8) + "px";
  cm.style.top = Math.min(e.clientY, innerHeight - cm.offsetHeight - 8) + "px";
}});
document.getElementById("focus-clear")?.addEventListener("click", async () => {{
  await api("/api/focus", {{text: ""}}); location.reload();
}});
document.getElementById("modal-close").addEventListener("click", () => mb.hidden = true);
mb.addEventListener("click", e => {{ if (e.target === mb) mb.hidden = true; }});
document.addEventListener("keydown", e => {{ if (e.key === "Escape") {{ mb.hidden = true; cmHide(); }} }});
mmute.addEventListener("click", async () => {{
  if (!modalKey) return;
  const r = await api("/api/mute", {{key: modalKey}});
  if (r.ok) location.reload();
}});
// ── parking-lot modal actions (inline messages only — no browser dialogs) ──
const pmsg = document.getElementById("modal-park-msg");
document.getElementById("park-promote").addEventListener("click", async e => {{
  if (!parkCur) return;
  e.target.disabled = true; pmsg.textContent = "creating WED ticket…";
  const r = await api("/api/parkpromote", {{file: parkCur.file}});
  if (r.ok) {{ pmsg.textContent = "promoted → " + r.created; setTimeout(() => location.reload(), 800); }}
  else {{ pmsg.textContent = r.error || "failed"; e.target.disabled = false; }}
}});
document.getElementById("park-drop").addEventListener("click", async e => {{
  if (!parkCur) return;
  e.target.disabled = true; pmsg.textContent = "dropping…";
  const r = await api("/api/parkdrop", {{file: parkCur.file}});
  if (r.ok) location.reload();
  else {{ pmsg.textContent = r.error || "failed"; e.target.disabled = false; }}
}});
document.getElementById("park-discuss").addEventListener("click", async e => {{
  if (!parkCur) return;
  e.target.disabled = true; pmsg.textContent = "sending to chat…";
  const r = await api("/api/parkdiscuss", {{file: parkCur.file}});
  if (r.ok) location.reload();
  else {{ pmsg.textContent = r.error || "failed"; e.target.disabled = false; }}
}});
// ── parking-lot add flow: the two buttons ARE the mode choice (no default) ──
const parkAdd = async mode => {{
  const t = document.getElementById("park-text"), s = document.getElementById("park-src"),
        m = document.getElementById("park-msg"),
        bp = document.getElementById("park-add-p"), br = document.getElementById("park-add-r");
  if (!t.value.trim()) {{ m.textContent = "type the one-liner first"; t.focus(); return; }}
  bp.disabled = true; br.disabled = true;
  m.textContent = mode === "research" ? "parking for research…" : "parking…";
  const r = await api("/api/parkadd", {{text: t.value, mode, source: s.value}});
  if (r.ok) {{ m.textContent = "parked: " + r.file; setTimeout(() => location.reload(), 700); }}
  else {{ m.textContent = r.error || "failed"; bp.disabled = false; br.disabled = false; }}
}};
document.getElementById("park-add-p")?.addEventListener("click", () => parkAdd("parked"));
document.getElementById("park-add-r")?.addEventListener("click", () => parkAdd("research"));
document.getElementById("park-text")?.addEventListener("keydown", e => {{
  if (e.key === "Enter") document.getElementById("park-msg").textContent =
    "choose: just park it, or Wednesday researches it";
}});
// ── clickable legend: hide a source everywhere (re-enable in customise) ──
const HIDDEN_GROUPS_JS = {json.dumps(sorted(HIDDEN_GROUPS))};
document.querySelectorAll(".legchip").forEach(c => c.addEventListener("click", async () => {{
  const hg = HIDDEN_GROUPS_JS.concat([c.dataset.group]);
  const r = await api("/api/layout", {{hidden_groups: hg}});
  if (r.ok) location.reload();
}}));
document.querySelectorAll(".acts button").forEach(b => b.addEventListener("click", async () => {{
  b.disabled = true; b.textContent = "…";
  const r = await api("/api/" + b.dataset.act, {{id: b.dataset.id}});
  if (r.ok) location.reload(); else {{ b.textContent = "!"; b.title = r.error || "failed"; }}
}}));
const addBtn = document.getElementById("add-btn");
if (addBtn) addBtn.addEventListener("click", async () => {{
  const t = document.getElementById("add-title"), m = document.getElementById("add-msg");
  if (!t.value.trim()) {{ m.textContent = "type something first"; return; }}
  addBtn.disabled = true; m.textContent = "adding…";
  const r = await api("/api/add", {{title: t.value, priority: +document.getElementById("add-prio").value}});
  if (r.ok) {{ m.textContent = r.created + " added"; setTimeout(() => location.reload(), 700); }}
  else {{ m.textContent = r.error || "failed"; addBtn.disabled = false; }}
}});
document.getElementById("add-title")?.addEventListener("keydown", e => {{ if (e.key === "Enter") addBtn.click(); }});
const IS_CHATVIEW = document.body.classList.contains("chatview");
const chatSend = document.getElementById("chat-send");
if (chatSend) {{
  const doSend = async () => {{
    const t = document.getElementById("chat-text");
    if (!t.value.trim()) return;
    chatSend.disabled = true;
    const r = await api("/api/chat", {{text: t.value}});
    if (IS_CHATVIEW) {{ if (r.ok) t.value = ""; chatSend.disabled = false; await csPoll(true); t.focus(); }}
    else if (r.ok) location.reload(); else chatSend.disabled = false;
  }};
  chatSend.addEventListener("click", doSend);
  document.getElementById("chat-text").addEventListener("keydown", e => {{ if (e.key === "Enter") doSend(); }});
}}
// ── action-now buttons on kam chat messages (compact tile: server-rendered) ──
document.querySelectorAll(".acknow[data-key]").forEach(b => b.addEventListener("click", async () => {{
  b.disabled = true;
  const r = await api("/api/actionnow", {{key: b.dataset.key, label: b.dataset.label || ""}});
  if (r.ok) location.reload(); else {{ b.disabled = false; b.textContent = r.error || "failed"; }}
}}));
const chatMode = document.getElementById("chat-mode");
if (chatMode) chatMode.addEventListener("click", async () => {{
  const r = await api("/api/layout", {{chat_mode: chatMode.dataset.mode}});
  if (r.ok) location.reload();
}});
// ── chat-with-Wed live mirror: poll the log every 4s, no page reloads ──
let csCount = -1;
async function csPoll(force) {{
  const log = document.getElementById("cs-log");
  if (!log) return;
  try {{
    const d = await (await fetch("/api/chatlog")).json();
    const msgs = d.messages || [];
    const live = document.getElementById("cs-live");
    if (live) live.textContent = "● live";
    if (!force && msgs.length === csCount) return;
    csCount = msgs.length;
    const nearBottom = log.scrollHeight - log.scrollTop - log.clientHeight < 80;
    log.innerHTML = "";
    for (const m of msgs) {{
      const div = document.createElement("div"); div.className = "msg " + m.role;
      const who = document.createElement("span"); who.className = "who";
      who.textContent = (m.role === "kam" ? "kam" : "wednesday") + " › ";
      const ts = document.createElement("span"); ts.className = "mts"; ts.textContent = (m.ts || "").slice(11, 16);
      const tx = document.createElement("div"); tx.className = "mtext"; tx.textContent = m.text;
      div.append(who, ts, tx);
      if (m.role === "kam") {{
        if (m.ack && m.ack.state) {{   // rendered from Wednesday-written state, never faked
          const al = document.createElement("div"); al.className = "ackline " + m.ack.state;
          const at = (m.ack.ts || "").slice(11, 16);
          al.textContent = m.ack.state === "seen" ? "✓ seen by Wed" + (at ? " " + at : "")
            : m.ack.state === "actioning" ? "● actioning"
            : m.ack.state === "done" ? "✓ done" + (at ? " " + at : "")
            : "⚡ action requested";
          div.appendChild(al);
        }}
        const ab = document.createElement("button"); ab.className = "acknow";
        ab.textContent = "⚡ action now"; ab.title = "ask Wednesday to action this now";
        ab.addEventListener("click", async () => {{
          ab.disabled = true;
          const r = await api("/api/actionnow", {{key: m.ts, label: (m.text || "").slice(0, 200)}});
          if (r.ok) await csPoll(true); else ab.disabled = false;
        }});
        div.appendChild(ab);
      }}
      log.appendChild(div);
    }}
    if (nearBottom || force) log.scrollTop = log.scrollHeight;
  }} catch (e) {{
    const live = document.getElementById("cs-live");
    if (live) live.textContent = "○ reconnecting…";
  }}
}}
if (IS_CHATVIEW) {{ csPoll(true); setInterval(csPoll, 4000); }}
const cpanel = document.getElementById("customise-panel");
const cbtn = document.getElementById("customise-btn");
cbtn.addEventListener("click", () => {{
  cpanel.hidden = !cpanel.hidden;
  cbtn.classList.toggle("on", !cpanel.hidden);
  organise = !cpanel.hidden ? organise : organise;  // no-op; refresh pause handled below
}});
document.getElementById("customise-save").addEventListener("click", async () => {{
  const hidden_tiles = [...cpanel.querySelectorAll('input[data-kind="tile"]:not(:checked)')].map(i => i.value);
  const hidden_groups = [...cpanel.querySelectorAll('input[data-kind="group"]:not(:checked)')].map(i => i.value);
  const tints = {{}};
  cpanel.querySelectorAll("select.tintsel").forEach(s => {{
    if (s.value !== "none") tints[s.dataset.tile] = s.value;
  }});
  const separators = [];
  cpanel.querySelectorAll("input.sepchk:checked").forEach(c => {{
    const lab = cpanel.querySelector('input.seplab[data-tile="' + c.dataset.tile + '"]');
    separators.push({{before: c.dataset.tile, label: lab ? lab.value.slice(0, 40) : ""}});
  }});
  const r = await api("/api/layout", {{hidden_tiles, hidden_groups, tints, separators}});
  if (r.ok) location.reload();
}});
// ── topbar panels: actioning / archived / favourite views ──
for (const [bid, pid] of [["acting-btn", "acting-panel"], ["archived-btn", "archived-panel"],
                          ["views-btn", "views-panel"]]) {{
  const bt = document.getElementById(bid), pn = document.getElementById(pid);
  bt.addEventListener("click", () => {{
    pn.hidden = !pn.hidden;
    bt.classList.toggle("on", !pn.hidden);
  }});
}}
// favourite views: save / apply / delete named layout snapshots
// (no browser dialogs — errors go to the inline #views-msg line)
const vpanel = document.getElementById("views-panel");
const vmsg = document.getElementById("views-msg");
vpanel.querySelectorAll(".vapply").forEach(b => b.addEventListener("click", async () => {{
  const r = await api("/api/views", {{action: "apply", name: b.dataset.name}});
  if (r.ok) location.reload(); else vmsg.textContent = r.error || "failed";
}}));
vpanel.querySelectorAll(".vdel").forEach(b => b.addEventListener("click", async () => {{
  const r = await api("/api/views", {{action: "delete", name: b.dataset.name}});
  if (r.ok) location.reload(); else vmsg.textContent = r.error || "failed";
}}));
const viewSave = document.getElementById("view-save");
viewSave.addEventListener("click", async () => {{
  const inp = document.getElementById("view-name");
  if (!inp.value.trim()) {{ vmsg.textContent = "type a name first"; inp.focus(); return; }}
  viewSave.disabled = true;
  const r = await api("/api/views", {{action: "save", name: inp.value.trim()}});
  if (r.ok) location.reload();
  else {{ vmsg.textContent = r.error || "failed"; viewSave.disabled = false; }}
}});
document.getElementById("view-name").addEventListener("keydown", e => {{
  if (e.key === "Enter") viewSave.click();
}});
const burger = document.getElementById("burger-btn"), bdrop = document.getElementById("burger-drop");
burger.addEventListener("click", e => {{ e.stopPropagation(); bdrop.hidden = !bdrop.hidden; burger.classList.toggle("on", !bdrop.hidden); }});
document.addEventListener("click", e => {{
  if (!bdrop.hidden && !e.target.closest("#burger-drop") && e.target !== burger) {{ bdrop.hidden = true; burger.classList.remove("on"); }}
}});
bdrop.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {{ bdrop.hidden = true; burger.classList.remove("on"); }}));
document.getElementById("preset-save-btn").addEventListener("click", () => {{
  const vp = document.getElementById("views-panel");
  if (vp && vp.hidden) document.getElementById("views-btn").click();
  const inp = document.getElementById("view-name");
  if (inp) setTimeout(() => inp.focus(), 50);
}});
const grid = document.getElementById("grid");
const obtn = document.getElementById("organise-btn");
obtn.addEventListener("click", () => {{
  organise = !organise;
  document.body.classList.toggle("organise", organise);
  obtn.classList.toggle("on", organise);
  obtn.innerHTML = organise ? "&#10003; done" : "&#9998; organise";
  document.querySelectorAll(".tilebox").forEach(t => t.draggable = organise);
  if (!organise) saveLayout();
}});
function layoutState() {{
  const order = [...grid.querySelectorAll(".tilebox")].map(t => t.dataset.tile);
  const scales = {{}}, sizes = {{}};
  grid.querySelectorAll(".tilebox").forEach(t => {{
    const s = parseFloat(t.style.fontSize) || 1;
    if (Math.abs(s - 1) > 0.01) scales[t.dataset.tile] = Math.round(s * 100) / 100;
    const w = parseInt(t.dataset.w || 1), h = parseInt(t.dataset.h || 0);
    if (w !== 1 || h !== 0) sizes[t.dataset.tile] = {{w, h}};
  }});
  return {{order, scales, sizes}};
}}
async function saveLayout() {{ await api("/api/layout", layoutState()); }}
let dragEl = null;
grid.addEventListener("dragstart", e => {{
  dragEl = e.target.closest(".tilebox"); if (dragEl) dragEl.classList.add("dragging");
}});
grid.addEventListener("dragend", () => {{ if (dragEl) dragEl.classList.remove("dragging"); dragEl = null; }});
grid.addEventListener("dragover", e => {{
  if (!dragEl) return; e.preventDefault();
  const over = e.target.closest(".tilebox");
  if (over && over !== dragEl) {{
    const r = over.getBoundingClientRect();
    const before = (e.clientY - r.top) < r.height / 2;
    over.parentNode.insertBefore(dragEl, before ? over : over.nextSibling);
  }}
}});
grid.addEventListener("drop", e => e.preventDefault());
document.querySelectorAll('.sizer button[data-size]').forEach(b => b.addEventListener("click", () => {{
  const tile = b.closest(".tilebox");
  let s = parseFloat(tile.style.fontSize) || 1;
  s = Math.min(1.8, Math.max(0.7, s + (b.dataset.size === "+" ? 0.1 : -0.1)));
  tile.style.fontSize = s.toFixed(2) + "em";
  sizeAll(); saveLayout();
}}));
// ── masonry sizing: width span 1-3, height 0=auto(full) or fixed units w/ scroller ──
const ROWU = 8, GAPU = 14, HUNIT = 44;
function sizeAll() {{
  document.querySelectorAll(".tilebox").forEach(t => {{
    const w = Math.min(4, Math.max(1, parseInt(t.dataset.w || 1)));
    const h = Math.max(0, parseInt(t.dataset.h || 0));
    t.style.gridColumn = w >= 4 ? "1 / -1" : "span " + w;
    if (h > 0) {{ t.style.height = (h * HUNIT) + "px"; t.classList.add("scroll"); }}
    else {{ t.style.height = ""; t.classList.remove("scroll"); }}
    t.style.gridRowEnd = "";
    const px = h > 0 ? h * HUNIT : t.scrollHeight + 2;   // scrollHeight = real content, immune to grid clipping
    t.style.gridRowEnd = "span " + Math.max(3, Math.ceil((px + GAPU) / (ROWU + GAPU)));
  }});
}}
sizeAll();
window.addEventListener("resize", () => sizeAll());
document.querySelectorAll("details").forEach(d => d.addEventListener("toggle", () => sizeAll()));
document.querySelectorAll('.sizer button[data-dim]').forEach(b => b.addEventListener("click", () => {{
  const t = b.closest(".tilebox"), d = b.dataset.dim;
  let w = parseInt(t.dataset.w || 1), h = parseInt(t.dataset.h || 0);
  if (d === "w+") w = Math.min(4, w + 1);  // 4 = full row (footer)
  if (d === "w-") w = Math.max(1, w - 1);
  if (d === "h+") h = Math.min(20, (h || Math.round(t.getBoundingClientRect().height / HUNIT)) + 1);
  if (d === "h-") h = Math.max(0, (h || Math.round(t.getBoundingClientRect().height / HUNIT)) - 1);
  t.dataset.w = w; t.dataset.h = h;
  sizeAll(); saveLayout();
}}));
</script>
</body></html>"""

(SITE / "index.html").write_text(PAGE)
write_subpages()
print(f"site/index.html written ({len(PAGE)} bytes, {len(EVENTS)} events, order={ORDER})")
