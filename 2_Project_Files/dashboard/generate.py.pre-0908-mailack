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
personal_actions = load("linear_personal.json")   # WED issues labelled "personal"
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
# "Flag for Wed" store (Kam 2026-08-06). Keyed by row key; the stored payload lets a
# flagged item outlive its source feed — a flagged headline is still there tomorrow
# after the news has moved on, until Kam unflags it.
_wf = DATA / "wedflags.json"
FLAGGED = json.loads(_wf.read_text()) if _wf.exists() else {}
if not isinstance(FLAGGED, dict): FLAGGED = {}
_l = DATA / "layout.json"
LAYOUT = json.loads(_l.read_text()) if _l.exists() else {}
if not isinstance(LAYOUT, dict): LAYOUT = {}
TILE_ORDER_DEFAULT = ["stats", "calendars", "flags", "personal", "family", "board", "chat", "tickets", "email", "news", "parkinglot"]
ORDER = [t for t in LAYOUT.get("order", TILE_ORDER_DEFAULT) if t in TILE_ORDER_DEFAULT]
ORDER += [t for t in TILE_ORDER_DEFAULT if t not in ORDER]
SCALES = LAYOUT.get("scales", {})
SIZES = LAYOUT.get("sizes", {})
if "calendars" not in SIZES: SIZES["calendars"] = {"w": 2}
if "board" not in SIZES: SIZES["board"] = {"w": 2}
if "email" not in SIZES: SIZES["email"] = {"w": 1, "h": 8}
if "tickets" not in SIZES: SIZES["tickets"] = {"w": 1, "h": 8}
if "parkinglot" not in SIZES: SIZES["parkinglot"] = {"w": 1, "h": 8}
if "personal" not in SIZES: SIZES["personal"] = {"w": 1, "h": 8}
HIDDEN_TILES = set(LAYOUT.get("hidden_tiles", []))
HIDDEN_GROUPS = set(LAYOUT.get("hidden_groups", []))   # datasec/secuura/personal/family
# Per-tile source filters: {tile_id: [group,...]} — hide a client in ONE tile without
# hiding it site-wide (Kam round 8). Site-wide HIDDEN_GROUPS still wins over these.
THEME = LAYOUT.get("theme", "dark")
if THEME not in ("dark", "light"): THEME = "dark"
TILE_GROUPS = LAYOUT.get("tile_groups", {})
if not isinstance(TILE_GROUPS, dict): TILE_GROUPS = {}
def tile_hidden(tile):
    v = TILE_GROUPS.get(tile) or []
    return set(v) | HIDDEN_GROUPS if isinstance(v, list) else HIDDEN_GROUPS
GROUPS = {"datasec": "Datasec", "secuura": "Secuura", "personal": "Personal", "family": "Family"}
CHAT_MODE = LAYOUT.get("chat_mode", "message")
if CHAT_MODE == "full":       # legacy expanded-tile mode → the chat-with-Wed view
    CHAT_MODE = "sidebar"
_v = DATA / "views.json"
VIEWS = json.loads(_v.read_text()) if _v.exists() else {}   # {"name": layout snapshot}
if not isinstance(VIEWS, dict): VIEWS = {}
TINTS = LAYOUT.get("tints", {})                             # {"tile-id": tint key}
if not isinstance(TINTS, dict): TINTS = {}
# Subtle same-lightness hue shifts of --surface-2, PER THEME. Kam round 11: tints
# are written inline on the tile, so a dark tint survived the switch to light mode
# and rendered dark-on-dark text — invisible. Each tint needs a light twin.
TINT_DARK = {"slate": "#20242b", "moss": "#21261f", "plum": "#262028",
             "sand": "#262319", "teal": "#1e2626"}
TINT_LIGHT = {"slate": "#eef1f6", "moss": "#eef3ea", "plum": "#f4eef5",
              "sand": "#f6f2e6", "teal": "#e9f2f1"}
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

# ── Project colour system (Kam round 12) ───────────────────────────────────
# Method: dataviz skill. Hue = the AREA; a lightness step within that hue = the
# project. Only THREE hues are used because that is the honest ceiling — the
# validator fails 4+ flat hues on all-pairs in both modes (worst offenders
# red↔orange ΔE 7.1 normal-vision, violet↔blue 9.8; magenta↔aqua 1.6 deutan).
# Three hues PASS all-pairs in both modes: dark worst CVD ΔE 9.4 / normal 20.9;
# light worst CVD 9.2 / normal 24.0.
#
# Steps are computed in OKLab and stepped TOWARD contrast — lighter on the dark
# surface, darker on the light one — so every step clears 3:1 against its own
# surface. Colour never carries identity alone: every row also states its name
# (the relief rule for light-mode aqua, which sits at 2.82:1 on white).
PROJECT_HUES = {
    "dark": {
        "datasec": ["#3987e5", "#56a4ff", "#72c1ff"],
        "secuura": ["#d95926", "#f97645", "#ff9363"],
        "life":    ["#199e70", "#43bb8b", "#64d8a6"],
    },
    "light": {
        "datasec": ["#2a78d6", "#005cb8", "#00419a"],
        # round 13: was #eb6834. MEASURED IN THE BROWSER at 2.80:1 against the
        # tinted tile surfaces (worst: plum #f4eef5) — under the 3:1 floor this
        # palette claims. The original validation ran against the PLAIN light
        # surface; tiles carry Kam's tints, so the real surface is not the one
        # the palette was checked on. #dc6131 clears 3.17:1 on the worst tint.
        # Cost, stated rather than buried: Secuura's own step0↔step1 separation
        # falls from ΔE 10.2 to 7.2 (still perceptible, still in family with the
        # other ramps at 8.9–10.4). Cross-family all-pairs unaffected (worst 42.4).
        "secuura": ["#dc6131", "#cb4b0c", "#ac2c00"],
        "life":    ["#009360", "#007747", "#005c35"],
    },
}
# entity -> (family, step). Fixed assignment, never cycled, never re-ordered.
# Wednesday's own board is deliberately NEUTRAL: it is not a client, and leaving
# it uncoloured keeps the client hues meaningful rather than decorative.
PROJECT_SLOT = {
    "datasec":                     ("datasec", 0),   # the client itself (calendars, mail)
    "datasec/nexusai":             ("datasec", 0),
    "datasec/cypherkey":           ("datasec", 1),
    "datasec/vision_sales_portal": ("datasec", 2),
    "secuura":                     ("secuura", 0),   # the client itself
    "secuura/blockchain":          ("secuura", 0),
    "secuura/tokenomics":          ("secuura", 1),
    "secuura/extranet":            ("secuura", 2),
    "personal":                    ("life", 0),
    "family":                      ("life", 1),
}

def project_key(client, project=None):
    k = (str(client or "").strip().lower().replace(" ", "_"))
    if project:
        k += "/" + str(project).strip().lower().replace(" ", "_")
    return k

def project_color(key):
    """Hex for an entity, or None for 'no colour' (Wednesday's own work).

    Round 13 — GRACEFUL FALLBACK. Only three lightness steps per hue survive the
    all-pairs validator, so a family cannot hold more than three projects. Datasec
    already has more than three real projects (Lead_Bot, myPKI, Task_Dispatcher…),
    so an unlisted project must NOT fall through to neutral — neutral means
    "Wednesday's own work" and would say something false. It inherits its CLIENT's
    base hue instead: the client is always right, the step is a bonus where one
    was assigned. This also makes Kam's open question on WED-82 (steps vs
    client-level only) a config change, not a rebuild."""
    if not key:
        return None                     # no entity = neutral, and callers may pass None
    slot = PROJECT_SLOT.get(key)
    if not slot and "/" in key:
        slot = PROJECT_SLOT.get(key.split("/", 1)[0])   # unlisted project → its client
    if not slot:
        return None
    fam, step = slot
    return PROJECT_HUES["light" if THEME == "light" else "dark"][fam][step]

# Calendar/mail sources are CLIENT-level entities; Family is its own life step.
AREA_OF = {"datasec": "datasec", "secuura": "secuura", "personal": "personal"}

# Distinctive tokens only — a false colour is worse than no colour, so anything
# ambiguous ("vision", "portal") is matched on its full multi-word form.
ENTITY_ALIASES = (
    ("vision sales portal", "datasec/vision_sales_portal"),
    ("cypherkey",           "datasec/cypherkey"),
    ("onetimepad",          "datasec/cypherkey"),
    ("nexusai",             "datasec/nexusai"),
    ("lead_bot",            "datasec/lead_bot"),
    ("lead bot",            "datasec/lead_bot"),
    ("mypki",               "datasec/mypki"),
    ("tokenomics",          "secuura/tokenomics"),
    ("extranet",            "secuura/extranet"),
    ("blockchain",          "secuura/blockchain"),
    ("platform k",          "secuura/blockchain"),
    ("datasec",             "datasec"),
    ("secuura",             "secuura"),
)

# Ticket prefixes are unambiguous identity — a KS- number can only be Secuura's
# board — so they are checked BEFORE the word aliases. WED- is deliberately
# absent: Wednesday's own work is neutral.
TICKET_PREFIX = (
    (re.compile(r"\bKS-\d+", re.I),    "secuura/blockchain"),
    (re.compile(r"\bRD-\d+", re.I),    "datasec/nexusai"),
    (re.compile(r"\bCPKEY-\d+", re.I), "datasec/cypherkey"),
)

def entity_from_text(text):
    """Best-effort entity for free text (flag lines). Ticket prefixes first, then
    the most distinctive alias — the list is ordered project-before-client.
    Returns None when nothing matches: neutral is the honest answer, not a guess."""
    t = (text or "").lower()
    for pat, key in TICKET_PREFIX:
        if pat.search(text or ""):
            return key
    for alias, key in ENTITY_ALIASES:
        if alias in t:
            return key
    return None

MAIL_PREFIX = re.compile(r"^\s*\[([^\]]+)\]")

def entity_from_subject(subject):
    """Fleet mail subjects ARE routing: '[Client/Project -> Wednesday] topic'.
    Parse the prefix rather than scanning the whole subject — the topic text
    often names other projects, and the sender is what the row is about."""
    m = MAIL_PREFIX.match(subject or "")
    if not m:
        return None
    for side in [p.strip() for p in re.split(r"->|→", m.group(1))]:
        low = side.lower()
        if low.startswith("wednesday") or low in ("all agents", "coagent"):
            continue                      # my own end of the conversation
        if "/" in side:
            client, _, project = side.partition("/")
            return project_key(client, project)
        return entity_from_text(side)
    return None

def src_color(src, cal=None):
    """Identity colour for a calendar/mail row. The Family calendar is its own
    entity (life step 1) regardless of which account carries it."""
    if cal == "Family":
        return project_color("family")
    return project_color(AREA_OF.get(src, src))

def project_rail(key):
    """Inline style for a left identity rail — the monday.com pattern: the same
    colour repeats on the group and on its items, so identity reads at a glance
    without tinting text."""
    c = project_color(key)
    return f' style="border-left:3px solid {c}"' if c else ' style="border-left:3px solid var(--line)"'

def project_chip(key, label):
    c = project_color(key)
    dot = (f'<span class="pdot" style="background:{c}"></span>' if c
           else '<span class="pdot neutral"></span>')
    return f'{dot}<span class="plabel">{html.escape(label)}</span>'

def flag_btn(key, label="", kind="item", payload=None):
    """The ⚑ toggle. Filled = flagged for Wednesday; nothing upstream changes."""
    on = key in FLAGGED
    pl = html.escape(json.dumps(payload, ensure_ascii=False), quote=True) if payload else ""
    return (f'<button class="flagbtn{" on" if on else ""}" data-flag="{html.escape(key, quote=True)}" '
            f'data-flabel="{html.escape(label[:200], quote=True)}" data-fkind="{kind}"'
            f'{f" data-fpayload=\"{pl}\"" if pl else ""} '
            f'title="{"flagged for Wednesday — click to clear" if on else "flag for Wed"}">&#9873;</button>')

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
            f'<span class="dot" style="background:{src_color(e["src"], e["cal"])}"></span>'
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
            f'<span class="dot" style="background:{src_color(e["src"], e["cal"])}"></span>'
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

def group_chips(tile):
    """Per-tile source toggles (Kam round 8 item 4): hide a client just here."""
    hid = set(TILE_GROUPS.get(tile) or [])
    bits = []
    for g, label in GROUPS.items():
        if g in HIDDEN_GROUPS:
            continue                     # already gone site-wide; nothing to toggle
        off = g in hid
        bits.append(f'<button class="tgchip{" off" if off else ""}" data-tile="{tile}" data-group="{g}" '
                    f'title="{"show" if off else "hide"} {label} in this tile only">{label}</button>')
    return f'<div class="tgbar">{"".join(bits)}</div>' if bits else ""

def tile_calendars():
    hid = tile_hidden("calendars")
    out = [group_chips("calendars")]
    for off, name in ((0, "Today"), (1, "Tomorrow")):
        evs = [e for e in day_events(off) if ev_group(e) not in hid]
        if not evs:
            continue                     # Kam item 1: no rows, no heading
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
    week_srcs = [(src, meta) for src, meta in SRC.items() if src not in hid]
    if week_srcs:
        out.append("<h3>Week by company <span class='count'>click to expand</span></h3>")
    for src, meta in week_srcs:
        wk = [e for e in EVENTS if e["src"] == src and ev_group(e) not in hid
              and 0 <= (e["start"].date() - NOW.date()).days <= 7]
        items = collapse_allday(wk)
        rows = "\n".join(run_row(it[1]) if it[0] == "run" else ev_row(it[1], show_day=True)
                          for it in items) or '<li class="empty">nothing this week</li>'
        # round 13: the group carries the same rail+dot its rows carry
        out.append(
            f"<details class='srcweek proj'{project_rail(AREA_OF.get(src, src))}>"
            f"<summary>{project_chip(AREA_OF.get(src, src), meta['label'])}"
            f" <span class='count'>{len(wk)}</span>"
            f"<a class='headlink' href='area_{src}.html'>full page &#10530;</a></summary>"
            f"<ul class='events'>{rows}</ul></details>")
    return "\n".join(out)

def tile_flags():
    # round 13: today's flags carry the rail of whichever project they belong to,
    # inferred from the flag text (entity_from_text is deliberately conservative —
    # no match means no rail, never a guessed one).
    rows = ""
    for p in PINNED:
        rows += (f'<li data-pin="{html.escape(p, quote=True)}"'
                 f'{project_rail(entity_from_text(p)) if entity_from_text(p) else ""}>'
                 f'<span class="flagdue">&#128204; pinned</span>'
                 f'<span class="ev">{html.escape(p)}</span></li>')
    for f in (brain["data"]["flags"] if brain else []):
        ek = entity_from_text(f["what"])
        rows += (f'<li{project_rail(ek) if ek else ""}>'
                 f'<span class="flagdue">{html.escape(f["due"])}</span>'
                 f'<span class="ev">{html.escape(f["what"])}</span></li>')
    return f"<ul class='events plain'>{rows}</ul>" if rows else '<p class="empty">no flags</p>'

def day_label(e):
    """Day heading for the family tile. Kam round 10: Today/Tomorrow now carry the
    DATE too, so a gap in the run of days is obvious rather than puzzling — the
    tile shows the next days that actually HAVE items, not consecutive days."""
    d = e["start"].date()
    delta = (d - NOW.date()).days
    stamp = e["start"].strftime("%a %-d %b")
    if delta == 0:  return f"Today · {stamp}"
    if delta == 1:  return f"Tomorrow · {stamp}"
    return stamp

def who_label(e):
    """Under a day heading the date is already stated, so the category column
    carries whose item it is (Alice / Harriet) — falling back to the calendar."""
    m = KID_PAT.search(e["title"])
    if m:
        return m.group(0).title()
    return "School" if "school" in e["title"].lower() else "Home"

def tile_family():
    if "family" in tile_hidden("family"):
        return '<p class="empty">Family is hidden — use the reset arrow beside the menu to restore</p>'
    # Kam round 11 — I had this wrong. The tile filtered to titles containing a
    # child's name or "school", so genuinely family items were dropped: "Maths
    # tutor" (Mon) and "Berry" (Sat) both vanished, which is what made the day
    # sequence jump Fri → Wed and look like a bug. It was my filter, not the data.
    # The Family calendar is already curated by the family; everything on it
    # belongs here, and the bell exists to quieten anything Kam doesn't want.
    fam = [e for e in EVENTS if e["cal"] == "Family"
           and e["start"].date() >= NOW.date()][:16]
    if not fam:
        return '<p class="empty">no kid/school items in the next stretch</p>'
    # Kam round 9: calendar-style DAY HEADINGS, and strictly time-ordered within a day.
    fam = sorted(fam, key=lambda e: (e["start"].date(), e["allday"] is False, e["start"]))
    out, current_day = [], None
    rows = []
    for e in fam:
        d = e["start"].date()
        if d != current_day:
            if rows:
                out.append("<ul class='events plain'>" + "\n".join(rows) + "</ul>")
                rows = []
            same_day = [x for x in fam if x["start"].date() == d]
            out.append(f"<h3>{day_label(e)} <span class='count'>{len(same_day)}</span></h3>")
            current_day = d
        key = mute_key(e)
        muted = key in MUTED
        t = "all-day" if e["allday"] else e["start"].strftime("%H:%M")
        s = SRC[e["src"]]
        fields = [("What", e["title"]),
                  ("When", e["start"].strftime("%A %d %B") + ("" if e["allday"] else e["start"].strftime(", %H:%M"))),
                  ("Calendar", e["cal"])]
        if e.get("loc"): fields.append(("Where", e["loc"]))
        # bell = quieten this item to the same muted treatment the calendar uses;
        # crossed bell = already quiet, click to restore. Persisted via /api/mute.
        bell = (f'<button class="bell{" off" if muted else ""}" data-mute="{html.escape(key, quote=True)}" '
                f'title="{"muted — click to restore" if muted else "quieten this item"}">'
                f'{"&#128277;" if muted else "&#128276;"}</button>')
        rows.append(
            f'<li class="evrow{" muted" if muted else ""}" data-detail="{detail_attr(fields, key)}" '
            f'data-key="{html.escape(key, quote=True)}" title="click for details">'
            f'<span class="dot" style="background:{src_color(e["src"], e["cal"])}"></span>'
            f'<span class="src">{who_label(e)}</span><span class="time">{t}</span>'
            f'<span class="ev">{html.escape(e["title"])}</span>{bell}</li>')
    if rows:
        out.append("<ul class='events plain'>" + "\n".join(rows) + "</ul>")
    return (group_chips("family") + "\n".join(out) +
            "<p class='note'>NB. Family calendar is display-only (cowork agent's territory).</p>")

PRIO = {0: "", 1: "P1", 2: "P2", 3: "P3", 4: "P4"}

def issue_row(i, todo=False):
    due = f' <span class="flagdue">due {i["dueDate"]}</span>' if i.get("dueDate") else ""
    pr = PRIO.get(i.get("priority") or 0, "")
    badge = f'<span class="prio p{i.get("priority")}">{pr}</span>' if pr else ""
    # Kam 2026-08-06: every row gets BOTH — "flag for Wed" (no ticket change at all,
    # it just tells Wednesday to look) and prioritise. The status change is hers to
    # make once she has actually seen it, which is the whole point of the label.
    btns = '<span class="acts">'
    btns += flag_btn(i["identifier"], i.get("title", ""), "wed")
    if (i.get("priority") or 5) > 1:
        btns += f'<button data-act="prioritise" data-id="{i["identifier"]}" title="prioritise — set Urgent">&#9650;</button>'
    if todo:
        btns += f'<button data-act="start" data-id="{i["identifier"]}" title="move to In Progress">&#9654;</button>'
    btns += "</span>"
    url = f'https://linear.app/wednesday-agent/issue/{i["identifier"]}'
    # round 13: WED items stay NEUTRAL by design — Wednesday is not a client, and
    # colouring her own board would make the client hues decorative. The rail is
    # still drawn in --line so this column aligns with the coloured tiles beside
    # it, EXCEPT where a WED item is plainly about one client's work.
    ek = entity_from_text(i.get("title", ""))
    return (f'<li data-wed="{i["identifier"]}"{project_rail(ek)}>'
            f'<a class="time tlink" href="{url}" target="_blank" rel="noopener">{i["identifier"]}</a>{badge}'
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

PRIO_NAMES = {0: "none", 1: "urgent", 2: "high", 3: "medium", 4: "low"}

def personal_row(i):
    due = f' <span class="flagdue">due {i["dueDate"]}</span>' if i.get("dueDate") else ""
    p = i.get("priority") or 0
    pr = PRIO.get(p, "")
    badge = f'<span class="prio p{p}">{pr}</span>' if pr else ""
    # ▲ cycles urgent→high→medium→low→urgent (no-priority starts at urgent);
    # ✓ moves the issue to the team's completed state. Both ride the shared
    # .acts button handler: POST /api/<data-act> {"id": <data-id>}.
    nxt = PRIO_NAMES[{0: 1, 1: 2, 2: 3, 3: 4, 4: 1}[p if p in PRIO_NAMES else 0]]
    btns = ('<span class="acts">'
            f'<button data-act="personal_prio" data-id="{i["identifier"]}" '
            f'title="priority: {PRIO_NAMES.get(p, "none")} — click to set {nxt}">&#9650;</button>'
            f'<button data-act="personal_done" data-id="{i["identifier"]}" '
            f'title="done — move to the completed state">&#10003;</button></span>')
    url = f'https://linear.app/wednesday-agent/issue/{i["identifier"]}'
    return (f'<li data-wed="{i["identifier"]}">'
            f'<a class="time tlink" href="{url}" target="_blank" rel="noopener">{i["identifier"]}</a>{badge}'
            f'<span class="ev">{html.escape(i["title"])}</span>{due}{btns}</li>')

def tile_personal():
    addbox = ("<div class='addbox'>"
              "<input id='padd-title' type='text' maxlength='200' placeholder='add a personal action&#8230;'>"
              "<button id='padd-btn'>add</button><span id='padd-msg'></span></div>")
    if not personal_actions:
        return ("<p class='empty'>personal feed not collected yet — run collect.py linear_personal</p>"
                + addbox)
    rows = "\n".join(personal_row(i) for i in personal_actions["data"]["items"]) or \
        '<li class="empty">nothing personal on the list — add one below</li>'
    return (f"<ul class='events plain'>{rows}</ul>{addbox}"
            "<p class='note'>NB. WED issues labelled <i>personal</i> — &#9650; cycles priority · "
            "&#10003; completes the ticket</p>")

NEWS_LABELS = {"world": "War & geopolitics", "tech": "Tech", "quantum": "Quantum",
               "security": "Security", "biotech": "Biotech & medicine"}

def news_row(n, kept=False):
    fields = [("Headline", n["title"]), ("Source", f'{n["source"]} · {n["date"]}'),
              ("Summary", n["summary"] or "(no summary in feed)")]
    payload = {"fields": fields, "url": n["link"]}
    d = html.escape(json.dumps(payload, ensure_ascii=False), quote=True)
    take = html.escape((n["summary"] or "")[:140])
    key = f'news|{n["title"]}'
    # the flag stores the whole item, so it survives tomorrow's feed refresh
    fp = {"title": n["title"], "summary": n["summary"], "link": n["link"],
          "source": n["source"], "date": n["date"]}
    keep = '<span class="keptmark" title="kept by your flag — the feed has moved on">kept</span>' if kept else ""
    return (f'<li class="evrow newsrow{" kept" if kept else ""}" data-detail="{d}" data-key="{html.escape(key, quote=True)}">'
            f'{flag_btn(key, n["title"], "news", fp)}'
            f'<div class="nbody"><div class="nhead">{html.escape(n["title"])}{keep}</div>'
            f'<div class="ntake">{take}</div></div></li>')

def tile_news():
    if not news or not any(news["data"]["topics"].values()):
        return '<p class="empty">news feeds unavailable</p>'
    out = []
    live_titles = set()
    for topic, label in NEWS_LABELS.items():
        items = [n for n in news["data"]["topics"].get(topic, [])
                 if f'news|{n["title"]}' not in ARCHIVED][:3]
        if not items:
            continue
        live_titles.update(n["title"] for n in items)
        rows = "".join(news_row(n) for n in items)
        # open by default (Kam): all categories visible without clicking
        out.append(f"<details class='srcweek' open><summary>{label} <span class='count'>{len(items)}</span></summary>"
                   f"<ul class='events plain newslist'>{rows}</ul></details>")
    # Flagged headlines the feed has since dropped — Kam's ask: a flagged item stays
    # until HE unflags it, so tomorrow's refresh cannot quietly take it away.
    kept = [v["payload"] for k, v in FLAGGED.items()
            if v.get("kind") == "news" and v.get("payload")
            and v["payload"].get("title") not in live_titles]
    if kept:
        rows = "".join(news_row(n, kept=True) for n in kept)
        out.insert(0, f"<details class='srcweek kept' open><summary>&#9873; Flagged — kept for you "
                      f"<span class='count'>{len(kept)}</span></summary>"
                      f"<ul class='events plain newslist'>{rows}</ul></details>")
    out.append('<p class="note">NB. takes are source summaries for now — Wednesday-curated takes arrive with the morning-generation duty · click a headline for the full summary + article link · &#9873; keeps an item across tomorrow\'s refresh until you clear it</p>')
    return "\n".join(out)

def focus_chip():
    if not FOCUS or not FOCUS.get("text"):
        return ""
    return (f'<span id="focuschip" title="set via right-click &#9654; do now">&#9654; '
            f'{html.escape(FOCUS["text"][:90])}'
            f'<button id="focus-clear" title="clear focus">&#10005;</button></span>')

def legend_html():
    # round 13: the legend is now driven by the same palette the rows use, so it
    # is a key rather than a decoration. Personal and Family previously shared
    # var(--series-3) — identical dots for two different groups; they are now the
    # two life steps and actually distinguishable.
    parts = []
    for g, l in (("datasec", "Datasec"), ("secuura", "Secuura"),
                 ("personal", "Personal"), ("family", "Family")):
        if g not in HIDDEN_GROUPS:
            parts.append((project_color(g) or "var(--line)", l, g))
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
    return (f'<div class="scrollpart">{mode_btn}<div class="chatlog">{rows}</div></div>'
            f'{box}<p class="note">NB. async channel — read at every boot &amp; check-in</p>')

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
 <p class="note">NB. live mirror of the message log (4s poll) — Wednesday replies from her session at boot &amp; checkpoints</p>
</aside>"""

CLIENT_GROUP = {"datasec": "datasec", "secuura": "secuura"}

def tile_tickets():
    # WED items deliberately NOT shown here (Kam 2026-08-06): Wednesday's own work
    # has its own board tile, and duplicating it just made this tile longer.
    hid = tile_hidden("tickets")
    out = [group_chips("tickets")]
    for p in (tickets["data"]["projects"] if tickets else []):
        # a client section belongs to the group of the same name (Kam item 2:
        # hiding Datasec anywhere hides its projects here too)
        if CLIENT_GROUP.get(str(p.get("client", "")).lower()) in hid:
            continue
        rows = ""
        for it in p["items"]:
            k = "ticket|" + p["client"] + "/" + p["project"] + "|" + it[:80]
            if k in ARCHIVED:   # same row-hide filter events + news apply
                continue
            rows += (f'<li data-key="{html.escape(k, quote=True)}">{ack_dot(k)}'
                     f'<span class="ev">{html.escape(it)}</span>'
                     f'<span class="acts">{flag_btn(k, it, "ticket")}</span></li>')
        rows = rows or '<li class="empty">nothing carried</li>'
        # open by default (Kam): every client's items visible without a click.
        # Round 12: identity rail + dot in the same hue — the group and its items
        # carry the same colour, which is the pattern that makes monday.com scan.
        pk = project_key(p["client"], p["project"])
        out.append(f"<details class='srcweek proj' open{project_rail(pk)}>"
                   f"<summary>{project_chip(pk, p['client'] + ' / ' + p['project'])}"
                   f" <span class='count'>as of {p['updated']}</span></summary>"
                   f"<ul class='events plain'>{rows}</ul></details>")
    if not out:
        out.append('<p class="empty">no client boards cached</p>')
    out.append('<p class="note">NB. Project boards are cached entry-card snapshots; live client feeds arrive with the Studio/fleet session. Wednesday\'s own items live in the WED board tile.</p>')
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
            "<p class='note'>NB. brain files in 0_Brain/parkinglot — &#9670; = research notes attached · "
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
        # same column order as calendars/family (dot · category · time · text) so
        # tiles stacked in a column line up — Kam round 10 item (b)
        # round 13: the sending project's colour on the rail, so a glance down the
        # column says WHICH project is talking. Wednesday's own broadcasts stay
        # neutral — the same rule as her board.
        ek = entity_from_subject(m["subject"])
        rows += (f'<li class="evrow{" needsack" if m["attn"] else ""}"'
                 f'{project_rail(ek) if ek else ""} data-detail="{detail_attr(fields)}">'
                 f'<span class="dot flagslot">{attn}</span>'
                 f'<span class="src">{html.escape(inboxes[:16])}</span><span class="time">{ts}</span>'
                 f'<span class="ev">{html.escape(m["subject"][:80])}</span></li>')
    return (f"<ul class='events plain'>{rows}</ul>"
            "<p class='note'>NB. fleet inboxes (wednesday-agent + coagent), read-only — acks stay session-scoped; "
            "your personal mailboxes join in Phase 2.</p>")

TILES = {
    "stats":     ("Overview",           tile_stats),
    "calendars": ("Calendars",          tile_calendars),
    "flags":     ("Today's flags",      tile_flags),
    "family":    ("Family",             tile_family),
    "board":     ("Coding — WED board", tile_board),
    "personal":  ("Personal Actions",   tile_personal),
    "chat":      ("Chat with Wednesday", tile_chat),
    "tickets":   ("Tickets by Project",  tile_tickets),
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
        tint = (TINT_LIGHT if THEME == "light" else TINT_DARK).get(TINTS.get(tid, ""))
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
    # round 13: subpages render rows through THIS function, not ev_row — they were
    # missed in the first pass of the rollout and kept the legacy series colours.
    return (f'<li class="{cls}"><span class="dot" style="background:{src_color(e["src"], e["cal"])}"></span>'
            f'<span class="time">{t}</span><span class="ev">{html.escape(e["title"])}</span>{cal}{loc}</li>')

def render_subpage(fname, title, body):
    page = (f'<!doctype html><html data-theme="{THEME}" lang="en"><head><meta charset="utf-8">'
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
        # same identity mark the tile uses, so a project reads the same on both surfaces
        pk = project_key(pr["client"], pr["project"])
        c = project_color(pk)
        dot = f'<span class="dot" style="background:{c}"></span> ' if c else ""
        rail = f' style="border-left:3px solid {c}; padding-left:8px"' if c else ""
        out.append(f'<h3{rail}>{dot}{html.escape(pr["project"])} '
                   f'<span class="cal">as of {pr["updated"]}</span></h3><ul>{rows}</ul>')
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
                '<p class="note">NB. Family calendar is display-only (cowork agent&#39;s territory).</p>')
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
    # Kam round 7: saving must offer UPDATE-an-existing as well as save-as-new,
    # so re-saving a tweak to "Cal Pref Default" doesn't silently make a duplicate.
    opts = "".join(f'<option value="{html.escape(n, quote=True)}">{html.escape(n)}</option>' for n in VIEWS)
    upd = (f'<div class="vsave"><select id="view-update">'
           f'<option value="">— update an existing layout —</option>{opts}</select>'
           f'<button id="view-update-btn">update</button></div>') if VIEWS else ""
    return (f'<div id="views-panel" hidden><h4>Favourite views</h4>{rows}'
            f'{upd}'
            f'<div class="vsave"><input id="view-name" type="text" maxlength="40" '
            f'placeholder="save as a NEW layout&#8230;"><button id="view-save">save new</button></div>'
            f'<span id="views-msg" class="verr"></span>'
            f'<p class="cpnote" style="margin-top:6px">a view snapshots the whole layout '
            f'(order, sizes, tints, separators, hidden tiles &amp; sources, chat mode) &middot; max 12 &middot; '
            f'NB. browser page zoom is a Chrome per-site setting, not part of a view</p></div>')

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
    # Flagged-for-Wednesday panel — Kam flags, nothing upstream moves until Wednesday
    # has actually looked. This panel is her queue and his receipt that it landed.
    flag_rows = []
    for k, v in sorted(FLAGGED.items(), key=lambda kv: kv[1].get("ts", ""), reverse=True):
        lbl = str(v.get("label") or k)
        ts = str(v.get("ts") or "")[5:16].replace("T", " ")
        kind = str(v.get("kind") or "item")
        flag_rows.append(f'<div class="strow"><span style="color:#e0a33e" title="flagged for Wednesday">&#9873;</span>'
                         f'<span class="stlabel">{html.escape(lbl[:90])}</span>'
                         f'<span class="sts">{kind} · {ts}</span></div>')
    n_flag = len(flag_rows)
    flagged = "".join(flag_rows) or '<p class="vempty">nothing flagged for Wednesday</p>'
    panels = (f'<div id="acting-panel" hidden><h4>Being actioned</h4>{acting}'
              f'<p class="cpnote" style="margin-top:6px">&#9889; action requested &middot; '
              f'&#9679; Wednesday actioning &mdash; states are written by Wednesday&#39;s own '
              f'session, never faked by the dashboard</p></div>'
              f'<div id="flagged-panel" hidden><h4>Flagged for Wednesday</h4>{flagged}'
              f'<p class="cpnote" style="margin-top:6px">NB. flagging changes nothing upstream &mdash; '
              f'no ticket moves and no status changes until Wednesday has seen it. '
              f'Clear a flag by clicking the &#9873; on the row again.</p></div>'
              f'<div id="archived-panel" hidden><h4>Archived</h4>{arch}</div>')
    return n_act, n_arch, n_flag, panels

N_ACTING, N_ARCHIVED, N_FLAGGED, STATUS_PANELS = status_panels_html()
ACTING_BTN = "&#9679; actioning" + (f" ({N_ACTING})" if N_ACTING else "")
ARCHIVED_BTN = "&#9634; archived" + (f" ({N_ARCHIVED})" if N_ARCHIVED else "")
FLAG_CT = f" ({N_FLAGGED})" if N_FLAGGED else ""
DARK_TICK = " &#10003;" if THEME == "dark" else ""
LIGHT_TICK = " &#10003;" if THEME == "light" else ""
# Every source hidden renders a dashboard with no events at all — which reads as
# "broken" rather than "filtered". Say so loudly, with a one-click way back.
# Kam round 8 item 3: once a source is hidden there was NO way back without the
# customise panel. This sits beside the burger and lights up whenever anything is
# filtered — site-wide or per-tile — and clears the lot in one click.
_ANY_HIDDEN = bool(HIDDEN_GROUPS) or any(TILE_GROUPS.get(t) for t in TILE_GROUPS)
RESET_BTN = ('<button id="reset-filters" class="resetbtn" title="restore all hidden clients '
             '(site-wide and per-tile)">&#8635;</button>' if _ANY_HIDDEN else "")
TILE_GROUPS_JSON = json.dumps(TILE_GROUPS)
ALLHIDDEN_BANNER = ('<div class="allhidden">All sources are hidden, so every calendar tile is empty. '
                    '<button id="showall-btn">show all sources</button></div>'
                    if set(GROUPS) and set(GROUPS) <= HIDDEN_GROUPS else "")

def customise_tile_rows():
    out = []
    for tid in TILE_ORDER_DEFAULT:
        cur = TINTS.get(tid, "none")
        opts = f'<option value="none"{" selected" if cur == "none" else ""}>no tint</option>' + "".join(
            f'<option value="{k}" style="background:{c}"{" selected" if k == cur else ""}>{k}</option>'
            for k, c in (TINT_LIGHT if THEME == "light" else TINT_DARK).items())
        _tp = TINT_LIGHT if THEME == "light" else TINT_DARK
        selstyle = f' style="background:{_tp[cur]}"' if cur in _tp else ""
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

PAGE = f"""<!doctype html><html data-theme="{THEME}" lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wednesday — Day Dashboard</title>
<style>
:root {{ color-scheme: dark;
  --surface-1:#1a1a19; --surface-2:#232322; --line:#33332f;
  --text-primary:#ffffff; --text-secondary:#c3c2b7; --text-muted:#8a897f;
  --series-1:#3987e5; --series-2:#d95926; --series-3:#199e70; }}
:root[data-theme="light"] {{ color-scheme: light;
  --surface-1:#f7f7f4; --surface-2:#ffffff; --line:#dcdcd4;
  --text-primary:#1b1b19; --text-secondary:#4a4a44; --text-muted:#78776e;
  --series-1:#1f63b8; --series-2:#b8431a; --series-3:#127956; }}
:root[data-theme="light"] .tilebox {{ box-shadow:0 1px 2px rgba(0,0,0,.05); }}
:root[data-theme="light"] li.nowline span {{ color:#b8431a; }}
:root[data-theme="light"] .resetbtn {{ background:#fdf3e0; border-color:#d8b878; color:#7a5a1a; }}
:root[data-theme="light"] .allhidden {{ background:#fdf3e0; border-color:#d8b878; color:#7a5a1a; }}
:root[data-theme="light"] .flagbtn.on {{ color:#b8860b; }}
:root[data-theme="light"] .keptmark, :root[data-theme="light"] details.srcweek.kept > summary {{ color:#b8860b; }}
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
.menu a.menubtn {{ display:inline-block; background:var(--surface-2); color:var(--text-secondary);
  border:1px solid var(--line); border-radius:7px; font-size:13px; padding:5px 12px;
  text-decoration:none; }}
.menu a.menubtn:hover {{ color:var(--text-primary); border-color:var(--text-muted); }}
.topbar .menu {{ position:relative; }}
#burger-drop {{ position:absolute; right:0; top:calc(100% + 6px); z-index:60; display:flex;
  flex-direction:column; gap:6px; background:var(--surface-2); border:1px solid var(--line);
  border-radius:8px; padding:8px; min-width:190px; box-shadow:0 6px 24px rgba(0,0,0,.45); }}
#burger-drop button {{ text-align:left; }}
#burger-drop[hidden] {{ display:none; }}
/* cascading submenus (Kam 2026-08-06): top level = intent, second level = action */
#burger-drop {{ gap:2px; padding:6px; min-width:210px; }}
.mgroup {{ position:relative; display:block; }}
.mgroup > .mparent {{ display:flex; width:100%; align-items:center; justify-content:space-between;
  background:none; border:none; color:var(--text-secondary); cursor:pointer;
  padding:7px 10px; border-radius:6px; font-size:13px; }}
.mgroup > .mparent:hover, .mgroup.open > .mparent {{ background:var(--surface-1); color:var(--text-primary); }}
.mgroup > .mparent .carat {{ color:var(--text-muted); font-size:10px; }}
.mgroup.open > .mparent .carat {{ transform:rotate(90deg); display:inline-block; }}
.msub {{ display:none; flex-direction:column; gap:1px; padding:2px 0 4px 10px;
  margin-left:6px; border-left:1px solid var(--line); }}
.mgroup.open > .msub {{ display:flex; }}
.msub button, .msub a {{ display:block; width:100%; text-align:left; background:none; border:none;
  color:var(--text-secondary); cursor:pointer; padding:6px 10px; border-radius:6px;
  font-size:12.5px; text-decoration:none; }}
.msub button:hover, .msub a:hover {{ background:var(--surface-1); color:var(--text-primary); }}
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
.src {{ color:var(--text-muted); font-size:.78em; width:3.6rem; flex:none; }}
.time {{ color:var(--text-secondary); font-variant-numeric:tabular-nums; font-size:.88em; width:4.2rem; flex:none; }}
ul.plain .time {{ width:4.2rem; }}
.ev {{ color:var(--text-primary); }}
.cal {{ color:var(--text-muted); font-size:.8em; }}
.flagdue {{ color:var(--text-secondary); font-size:.85em; width:6em; flex:none; font-variant-numeric:tabular-nums; }}
.empty {{ color:var(--text-muted); }}
.note {{ color:var(--text-muted); font-size:.8em; margin-top:6px; }}
/* Kam 2026-08-06: a tile's trailing note / input sits at the BOTTOM of the tile,
   not immediately under the content — so every tile in a row ends on the same line. */
.tilebody {{ display:flex; flex-direction:column; }}

/* Scrolling tiles pin their trailing note/input too: the CONTENT scrolls, the
   input stays put. Kam's ask was explicitly "chat with wednesday input". */
.tilebox.scroll .tilebody {{ display:flex; flex-direction:column; }}
.tilebox.scroll .tilebody > .scrollpart {{ flex:1 1 auto; overflow-y:auto; min-height:0; scrollbar-width:thin; }}
.tilebox.scroll .tilebody > .note, .tilebox.scroll .tilebody > .chatinput,
.tilebox.scroll .tilebody > .addbox, .tilebox.scroll .tilebody > .parkadd {{ flex:none; }}
/* EVERY tile gets a .scrollpart wrapper at load (see JS): content scrolls inside it,
   trailing notes/inputs pin to the tile floor. Kam 2026-08-06 round 7 — the earlier
   rule only reached tiles that already had one, which was almost none of them. */
.tilebody > .scrollpart {{ flex:1 1 auto; min-height:0; }}
.tilebox.scroll .tilebody > .scrollpart {{ overflow-y:auto; scrollbar-width:thin; }}
.tilebody > .note, .tilebody > .chatinput, .tilebody > .addbox, .tilebody > .parkadd {{ flex:none; }}
.tilebody > .note:last-child {{ margin-top:6px; padding-top:4px; }}
/* ⚑ flag-for-Wed toggle */
.flagbtn {{ background:none; border:none; color:var(--text-muted); cursor:pointer; padding:0 4px;
  font-size:1.05em; line-height:1; flex:none; opacity:.45; }}
.flagbtn:hover {{ opacity:1; color:var(--text-primary); }}
.flagbtn.on {{ opacity:1; color:#e0a33e; }}
li:hover .flagbtn {{ opacity:.85; }}
li:hover .flagbtn.on {{ opacity:1; }}
.newsrow {{ align-items:flex-start; }}
.newsrow .nbody {{ flex:1; }}
/* project identity marks (round 12) — colour sits on a MARK, never on text */
.pdot {{ width:9px; height:9px; border-radius:2.5px; display:inline-block; flex:none;
  margin-right:7px; vertical-align:middle; }}
.pdot.neutral {{ background:var(--text-muted); opacity:.45; }}
.plabel {{ vertical-align:middle; }}
details.srcweek.proj {{ padding-left:10px; border-radius:3px; }}
details.srcweek.proj > summary {{ margin-left:0; }}
.legchip .pdot {{ margin-right:5px; }}
.resetbtn {{ background:#3a2a1a; border:1px solid #7a5a2a; color:#f0c98a; border-radius:6px;
  cursor:pointer; padding:2px 8px; font-size:14px; line-height:1.3; margin-right:6px; }}
.resetbtn:hover {{ background:#4a3520; color:#fff; }}
.tgbar {{ display:flex; gap:5px; flex-wrap:wrap; margin:0 0 8px; }}
.tgchip {{ background:var(--surface-1); border:1px solid var(--line); color:var(--text-secondary);
  border-radius:999px; padding:1px 9px; font-size:.72em; cursor:pointer; }}
.tgchip:hover {{ color:var(--text-primary); }}
.tgchip.off {{ opacity:.4; text-decoration:line-through; }}
.allhidden {{ background:#3a2a1a; border:1px solid #7a5a2a; color:#f0c98a; border-radius:8px;
  padding:10px 14px; margin-top:12px; font-size:13px; display:flex; gap:12px; align-items:center; }}
.allhidden button {{ background:var(--surface-2); color:var(--text-primary); border:1px solid var(--line);
  border-radius:6px; padding:4px 10px; cursor:pointer; font-size:12.5px; }}
.dot.flagslot {{ background:none; border-radius:0; display:inline-flex; align-items:center;
  justify-content:center; overflow:visible; }}
.dot.flagslot .attn {{ font-size:.8em; }}
.bell {{ background:none; border:none; cursor:pointer; padding:0 2px; font-size:.85em;
  line-height:1; margin-left:auto; flex:none; opacity:.35; filter:grayscale(1); }}
li:hover .bell {{ opacity:.9; }}
.bell.off {{ opacity:.55; }}

.keptmark {{ color:#e0a33e; font-size:.7em; margin-left:6px; text-transform:uppercase;
  letter-spacing:.04em; vertical-align:middle; }}
details.srcweek.kept > summary {{ color:#e0a33e; }}
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
li.muted {{ font-size:60%; opacity:.55; }}   /* Kam round 9: +20% on the previous 50% */
/* Kam round 10: a muted row keeps the SAME column geometry as its full-size
   neighbours — only the TEXT shrinks. Widths are already in rem (root-relative),
   so they do not scale with the row's 60% font-size; the dot and the row gap
   must be pinned too or the columns still drift. */
li.muted {{ gap:8px; }}
li.muted .dot {{ width:8px; height:8px; }}
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
 <span class="menu"><a class="menubtn" href="/cockpit" title="open the cockpit: conversation with Wednesday + fleet activity (plain chat stays at /chat)">&#128172; Chat</a> {RESET_BTN}<button id="burger-btn" title="menu">&#9776;</button>
 <span id="burger-drop" hidden>
   <span class="mgroup">
     <button class="mparent">&#9881; Customise <span class="carat">&#9656;</span></button>
     <span class="msub">
       <button id="preset-save-btn">&#128190; Save layout&#8230;</button>
       <button id="views-btn">&#9734; Load layout</button>
       <button id="organise-btn">&#9998; Organise (drag tiles)</button>
       <button id="customise-btn">&#9636; Tile setup</button>
     </span>
   </span>
   <span class="mgroup">
     <button class="mparent">&#9873; Review <span class="carat">&#9656;</span></button>
     <span class="msub">
       <button id="flagged-btn">&#9873; Flagged for Wednesday{FLAG_CT}</button>
       <button id="acting-btn">{ACTING_BTN}</button>
       <button id="archived-btn">{ARCHIVED_BTN}</button>
     </span>
   </span>
   <span class="mgroup">
     <button class="mparent">&#10530; Full pages <span class="carat">&#9656;</span></button>
     <span class="msub">
       <a href="area_board.html">WED board</a>
       <a href="area_news.html">News</a>
       <a href="area_family.html">Family</a>
       <a href="area_datasec.html">Datasec week</a>
       <a href="area_secuura.html">Secuura week</a>
     </span>
   </span>
   <span class="mgroup">
     <button class="mparent">&#8635; Data <span class="carat">&#9656;</span></button>
     <span class="msub">
       <button id="refresh-btn">&#8635; Refresh now</button>
       <button id="clearfocus-btn">&#10005; Clear focus</button>
     </span>
   </span>
   <span class="mgroup">
     <button class="mparent">&#9681; Appearance <span class="carat">&#9656;</span></button>
     <span class="msub">
       <button class="themebtn" data-theme-set="dark">&#9789; Dark{DARK_TICK}</button>
       <button class="themebtn" data-theme-set="light">&#9788; Light{LIGHT_TICK}</button>
     </span>
   </span>
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
{ALLHIDDEN_BANNER}<div id="grid"><div class="grid">
{render_tiles()}
</div></div>
<script type="application/json" id="tile-groups-state">{TILE_GROUPS_JSON}</script>
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
// Bottom-align every tile's trailing note / input (Kam round 7): wrap the CONTENT
// in .scrollpart so the note or input box sits on the tile floor whatever the
// content height, and never overlaps it.
document.querySelectorAll(".tilebody").forEach(body => {{
  if (body.querySelector(":scope > .scrollpart")) return;      // chat already has one
  const kids = [...body.children];
  const isTail = el => el.matches(".note, .addbox, .chatinput, .parkadd");
  let cut = kids.length;
  while (cut > 0 && isTail(kids[cut - 1])) cut--;
  if (cut === kids.length || cut === 0) return;                // nothing to pin / nothing above
  const wrap = document.createElement("div");
  wrap.className = "scrollpart";
  kids.slice(0, cut).forEach(k => wrap.appendChild(k));
  body.insertBefore(wrap, body.firstChild);
}});
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
document.querySelectorAll(".acts button:not(.flagbtn)").forEach(b => b.addEventListener("click", async () => {{
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
// ── Personal Actions add flow (WED issue, personal label, Todo state) ──
const paddBtn = document.getElementById("padd-btn");
if (paddBtn) paddBtn.addEventListener("click", async () => {{
  const t = document.getElementById("padd-title"), m = document.getElementById("padd-msg");
  if (!t.value.trim()) {{ m.textContent = "type something first"; return; }}
  paddBtn.disabled = true; m.textContent = "adding…";
  const r = await api("/api/personal_add", {{title: t.value}});
  if (r.ok) {{ m.textContent = r.created + " added"; setTimeout(() => location.reload(), 700); }}
  else {{ m.textContent = r.error || "failed"; paddBtn.disabled = false; }}
}});
document.getElementById("padd-title")?.addEventListener("keydown", e => {{ if (e.key === "Enter") paddBtn.click(); }});
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
                          ["flagged-btn", "flagged-panel"], ["views-btn", "views-panel"]]) {{
  const bt = document.getElementById(bid), pn = document.getElementById(pid);
  if (!bt || !pn) continue;
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
// UPDATE an existing layout in place (same save action, existing name = overwrite)
const viewUpdBtn = document.getElementById("view-update-btn");
if (viewUpdBtn) viewUpdBtn.addEventListener("click", async () => {{
  const sel = document.getElementById("view-update");
  const name = sel.value;
  if (!name) {{ vmsg.textContent = "pick a layout to update"; sel.focus(); return; }}
  viewUpdBtn.disabled = true;
  const r = await api("/api/views", {{action: "save", name}});
  if (r.ok) location.reload();
  else {{ vmsg.textContent = r.error || "failed"; viewUpdBtn.disabled = false; }}
}});
const burger = document.getElementById("burger-btn"), bdrop = document.getElementById("burger-drop");
burger.addEventListener("click", e => {{ e.stopPropagation(); bdrop.hidden = !bdrop.hidden; burger.classList.toggle("on", !bdrop.hidden); }});
document.addEventListener("click", e => {{
  if (!bdrop.hidden && !e.target.closest("#burger-drop") && e.target !== burger) {{ bdrop.hidden = true; burger.classList.remove("on"); }}
}});
// submenu parents toggle their own group and must NOT close the menu
bdrop.querySelectorAll(".mparent").forEach(p => p.addEventListener("click", e => {{
  e.stopPropagation();
  const g = p.parentElement, wasOpen = g.classList.contains("open");
  bdrop.querySelectorAll(".mgroup").forEach(x => x.classList.remove("open"));
  if (!wasOpen) g.classList.add("open");
}}));
// leaf actions close the whole menu
bdrop.querySelectorAll(".msub button, .msub a").forEach(b => b.addEventListener("click", () => {{
  bdrop.hidden = true; burger.classList.remove("on");
  bdrop.querySelectorAll(".mgroup").forEach(x => x.classList.remove("open"));
}}));
// reset EVERYTHING that is filtered — site-wide groups and every per-tile filter
// light/dark switch — stored in the layout so it travels with the dashboard
// rather than living in one browser (Kam round 11)
document.querySelectorAll(".themebtn").forEach(b => b.addEventListener("click", async () => {{
  const want = b.dataset.themeSet;
  document.documentElement.setAttribute("data-theme", want);   // instant, before the round trip
  const r = await api("/api/layout", {{theme: want}});
  if (r.ok) location.reload();
}}));
const resetBtn = document.getElementById("reset-filters");
if (resetBtn) resetBtn.addEventListener("click", async () => {{
  resetBtn.disabled = true;
  const r = await api("/api/layout", {{hidden_groups: [], tile_groups: {{}}}});
  if (r.ok) location.reload(); else resetBtn.disabled = false;
}});
// per-tile source chips: hide/show a client in THIS tile only
document.querySelectorAll(".tgchip").forEach(c => c.addEventListener("click", async () => {{
  const tile = c.dataset.tile, grp = c.dataset.group;
  const cur = JSON.parse(document.getElementById("tile-groups-state").textContent || "{{}}");
  const list = new Set(cur[tile] || []);
  if (list.has(grp)) list.delete(grp); else list.add(grp);
  cur[tile] = [...list];
  const r = await api("/api/layout", {{tile_groups: cur}});
  if (r.ok) location.reload();
}}));
const showAllBtn = document.getElementById("showall-btn");
if (showAllBtn) showAllBtn.addEventListener("click", async () => {{
  const r = await api("/api/layout", {{hidden_groups: []}});
  if (r.ok) location.reload();
}});
// 🔔 bell on family rows — quieten/restore an item using the SAME persisted mute
// the calendar already uses, so a quietened item stays quiet across refreshes.
document.addEventListener("click", async e => {{
  const b = e.target.closest(".bell");
  if (!b) return;
  e.preventDefault(); e.stopPropagation();
  try {{
    const r = await fetch("/api/mute", {{ method:"POST", headers:{{"Content-Type":"application/json"}},
      body: JSON.stringify({{ key: b.dataset.mute }}) }});
    if (!r.ok) throw new Error(await r.text());
    setTimeout(() => location.reload(), 250);
  }} catch (err) {{ console.error("mute failed", err); }}
}});
// ⚑ flag for Wed — flags the item for Wednesday and changes NOTHING upstream
document.addEventListener("click", async e => {{
  const b = e.target.closest(".flagbtn");
  if (!b) return;
  e.preventDefault(); e.stopPropagation();
  const on = !b.classList.contains("on");
  b.classList.toggle("on", on);            // optimistic; reverted if the call fails
  let payload = null;
  try {{ payload = b.dataset.fpayload ? JSON.parse(b.dataset.fpayload) : null; }} catch (_) {{}}
  try {{
    const r = await fetch("/api/flag", {{ method:"POST", headers:{{"Content-Type":"application/json"}},
      body: JSON.stringify({{ key:b.dataset.flag, label:b.dataset.flabel || "",
                              kind:b.dataset.fkind || "item", on, payload }}) }});
    if (!r.ok) throw new Error(await r.text());
    setTimeout(() => location.reload(), 250);
  }} catch (err) {{ b.classList.toggle("on", !on); console.error("flag failed", err); }}
}});
const refreshBtn = document.getElementById("refresh-btn");
if (refreshBtn) refreshBtn.addEventListener("click", () => location.reload());
const clearFocusBtn = document.getElementById("clearfocus-btn");
if (clearFocusBtn) clearFocusBtn.addEventListener("click", async () => {{
  try {{ await fetch("/api/focus", {{ method:"POST", headers:{{"Content-Type":"application/json"}},
        body: JSON.stringify({{ clear:true }}) }}); }} catch (_) {{}}
  location.reload();
}});
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
