#!/usr/bin/env python3
"""build_payload.py — TRMNL "Kam view" webhook payload, built from the dashboard's own JSON.

READ-ONLY against every input. NO network. Prints {"merge_variables": {...}} to stdout;
push.sh is the only thing that sends it anywhere.

Inputs (all under 0_Brain/dashboard/data/, written by other tools — never by this one):
  personal_calendar.json  collect.py:38-44  (EventKit probe, calendar_probe.swift:25-26: today 00:00
                          + 8 days, despite the legacy key name events_next_48h; start is UTC "Z")
  datasec_calendar.json   collect.py:223-239 (Graph calendarView, 8 days; start is naive Sydney)
  secuura_calendar.json   collect.py:197-200 (Google secret ICS, 8 days; start has an offset)
  layout.json             hidden_groups — the dashboard drops these (generate.py:66, :332)
  archived.json           "src|title" keys the dashboard drops (generate.py:332-333)
  muted.json              "src|title" keys Kam quietened (generate.py:37-38, :524); dropped here
                          by default because 1-bit e-ink has no dimmed state (--keep-muted)
  usage_<seat>.json       statusline_publish.sh:82 — rate_limits.seven_day.used_percentage
  decisions.json          decision_queue.sh — the cards; status open|ruled|withdrawn

Predicates (each mirrors a named line, so the e-ink view cannot disagree with the board):
  needs-Kam   = card.status == "open"                       (cockpit.html:1078)
  seat        = "friday" if card.seat == "friday"
                else "tuesday" if Datasec (client or id prefix) else "wednesday"
                                                            (reconcile_rulings.py:91-125)
  usage stale = age >= 900 s                                 (cockpit.html:421)

Usage:
  build_payload.py [--days 7] [--max-rows 11] [--max-actions 3]
                   [--redact datasec,secuura,personal,family] [--limit 5120] [--keep-muted]
                   [--data-dir DIR] [--now ISO8601]
  build_payload.py --selftest
Exit: 0 ok · 2 bad input/unreadable required file · 3 payload over --limit (nothing printed).
"""
import argparse, datetime, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
DATA_DEFAULT = HERE.parent.parent / "0_Brain" / "dashboard" / "data"

SEATS = ("wednesday", "tuesday", "friday")
SEAT_TITLE = {"wednesday": "Wednesday", "tuesday": "Tuesday", "friday": "Friday"}
USE_STALE_S = 900                       # cockpit.html:421
FEED_STALE_S = 3 * 3600                 # collect loop is 300 s (serve.sh:26-30); 3 h = clearly dead
DATASEC_CLIENTS = {"datasec"}           # reconcile_rulings.py:91
DATASEC_PREFIXES = ("nexusai-", "datasec-", "vision-", "mypki-", "cypherkey-", "leadbot-")  # :92
TITLE_CHARS = 30                        # one line in the left column at OG width (measured render)
MAX_ROWS_DEFAULT = 11                   # measured: OG 800x480 render, see README "Render check"
MAX_ACTIONS_DEFAULT = 3
SRC_LETTER = {"datasec": "D", "secuura": "S", "personal": "P", "family": "F"}
SRC_LABEL = {"datasec": "Datasec", "secuura": "Secuura", "personal": "Personal", "family": "Family"}


def die(msg, code=2):
    print(f"build_payload: {msg}", file=sys.stderr)
    sys.exit(code)


def load(data_dir, name, required=False):
    p = data_dir / name
    if not p.exists():
        if required:
            die(f"required input missing: {p}")
        return None
    try:
        return json.loads(p.read_text())
    except Exception as e:                      # loud, never silent
        if required:
            die(f"unreadable {p}: {e}")
        print(f"build_payload: WARN unreadable {p}: {e}", file=sys.stderr)
        return None


def clip(s, n):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def first_sentence(s):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    s = re.sub(r"^if you do not rule:\s*", "", s, flags=re.I)
    m = re.match(r"(.+?[.;])(\s|$)", s)
    return m.group(1) if m else s


def parse_ts(s, now):
    dt = datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    if dt.tzinfo is None:                       # Datasec: naive Sydney (collect.py:233-234)
        dt = dt.replace(tzinfo=now.tzinfo)      # same assumption as generate.py:322-323
    return dt.astimezone(now.tzinfo)


def age_s(collected_at, now):
    try:
        return (now - parse_ts(collected_at, now)).total_seconds()
    except Exception:
        return None


def age_label(sec):
    if sec is None:
        return "?"
    if sec < 3600:
        return f"{max(1, round(sec / 60))}m"
    if sec < 86400:
        return f"{round(sec / 3600)}h"
    return f"{round(sec / 86400)}d"


# ── calendars ─────────────────────────────────────────────────────────────
def norm_events(data_dir, now, warns):
    """Mirror of generate.py:307-327, plus a freshness gate the dashboard does not have."""
    evs = []
    feeds = (("personal", "personal_calendar.json"), ("secuura", "secuura_calendar.json"),
             ("datasec", "datasec_calendar.json"))
    for src, fname in feeds:
        doc = load(data_dir, fname)
        if not doc:
            warns.append(f"{SRC_LABEL[src]} feed missing")
            continue
        a = age_s(doc.get("collected_at"), now)
        if a is None or a > FEED_STALE_S:
            when = str(doc.get("collected_at", "?"))[:10]
            warns.append(f"{SRC_LABEL[src]} feed stale since {when}")
            continue                            # never show a dead feed's events as current
        for e in (doc.get("data") or {}).get("events", []):
            try:
                start = parse_ts(e["start"], now)
            except Exception:
                warns.append(f"{SRC_LABEL[src]}: 1 unparseable event skipped")
                continue
            cal = e.get("cal", "") if src == "personal" else SRC_LABEL[src]
            evs.append({"src": src, "cal": cal, "title": str(e.get("title", "?")),
                        "start": start, "allday": bool(e.get("allday", False))})
    return sorted(evs, key=lambda e: e["start"])


def group_of(e):
    return "family" if e["cal"] == "Family" else e["src"]       # generate.py:329-330


def build_calendar(data_dir, now, days, max_rows, redact, warns, keep_muted=False):
    layout = load(data_dir, "layout.json") or {}
    hidden = set(layout.get("hidden_groups", []))
    archived = set(load(data_dir, "archived.json") or [])
    if not keep_muted:
        archived |= set(load(data_dir, "muted.json") or [])
    horizon = (now + datetime.timedelta(days=days)).date()
    picked = []
    for e in norm_events(data_dir, now, warns):
        if group_of(e) in hidden or f'{e["src"]}|{e["title"]}' in archived:
            continue
        d = e["start"].date()
        if d < now.date() or d > horizon:
            continue
        # No source carries an END time (collect.py emits start only), so "running" is
        # approximated: a timed event stays listed for 60 min after it starts, then drops.
        if not e["allday"] and e["start"] < now - datetime.timedelta(minutes=60):
            continue
        picked.append(e)
    picked.sort(key=lambda e: (e["start"].date(), not e["allday"], e["start"]))
    # ROW BUDGET (max_rows) counts day headings as rows: the screen has a fixed height and a
    # heading costs a line, so an event is taken only if it AND (when new) its heading fit.
    # Never a heading without an event under it.
    out_days, cur, used, shown_n = [], None, 0, 0
    for e in picked:
        d = e["start"].date()
        cost = 1 + (1 if d != cur else 0)
        if used + cost > max_rows:
            break
        used += cost
        shown_n += 1
        if d != cur:
            delta = (d - now.date()).days
            stamp = e["start"].strftime("%a %-d %b")
            label = ("Today · " if delta == 0 else "Tomorrow · " if delta == 1 else "") + stamp
            out_days.append({"label": label, "events": []})
            cur = d
        g = group_of(e)
        title = f"{SRC_LABEL[g]} event" if g in redact else clip(e["title"], TITLE_CHARS)
        is_now = (not e["allday"]) and e["start"] <= now
        out_days[-1]["events"].append({
            "time": "all day" if e["allday"] else e["start"].strftime("%H:%M"),
            "src": SRC_LETTER[g], "title": title, "now": is_now})
    return out_days, len(picked) - shown_n, len(picked)


# ── agents ────────────────────────────────────────────────────────────────
def build_agents(data_dir, now):
    out = []
    for s in SEATS:
        d = load(data_dir, f"usage_{s}.json")
        if not d or not isinstance(d.get("pct"), (int, float)):
            out.append({"name": SEAT_TITLE[s], "pct": None, "resets": "", "stale": True, "age": "none"})
            continue
        try:
            a = (now - datetime.datetime.strptime(d["ts"], "%Y-%m-%dT%H:%M:%SZ")
                 .replace(tzinfo=datetime.timezone.utc)).total_seconds()
        except Exception:
            a = None
        out.append({"name": SEAT_TITLE[s], "pct": int(round(d["pct"])),
                    "resets": str(d.get("resets_in", "")),
                    "stale": a is None or a >= USE_STALE_S, "age": age_label(a)})
    return out


# ── actions (decision cards awaiting Kam) ──────────────────────────────────
def is_datasec(card):
    cp = str(card.get("client_project", "")).strip()
    client = cp.split("/", 1)[0].strip().lower() if cp else ""
    return client in DATASEC_CLIENTS or str(card.get("id", "")).lower().startswith(DATASEC_PREFIXES)


def seat_of(card):
    if card.get("seat") == "friday":
        return "friday"
    return "tuesday" if is_datasec(card) else "wednesday"


def needs_kam(card):
    return isinstance(card, dict) and card.get("status") == "open"


def build_actions(data_dir, now, max_actions, predicate=needs_kam):
    cards = load(data_dir, "decisions.json", required=True)
    if not isinstance(cards, list):
        die("decisions.json is not a list")
    open_cards = [c for c in cards if predicate(c)]
    open_cards.sort(key=lambda c: str(c.get("ts", "")))         # oldest first: longest-waiting on top
    counts = {SEAT_TITLE[s]: 0 for s in SEATS}
    rows = []
    for c in open_cards:
        seat = seat_of(c)
        counts[SEAT_TITLE[seat]] += 1
        try:
            since = parse_ts(c.get("ts", ""), now).strftime("%-d %b %H:%M")
        except Exception:
            since = "?"
        rows.append({"seat": SEAT_TITLE[seat], "title": clip(c.get("title", "?"), 60),
                     "since": since, "dflt": clip(first_sentence(c.get("default_action", "")), 40)})
    return rows[:max_actions], max(0, len(rows) - max_actions), counts, len(cards)


# ── assemble ──────────────────────────────────────────────────────────────
def build(data_dir, now, days=7, max_rows=MAX_ROWS_DEFAULT, max_actions=MAX_ACTIONS_DEFAULT, redact=frozenset(), keep_muted=False):
    warns = []
    cal_days, cal_more, cal_total = build_calendar(data_dir, now, days, max_rows, redact, warns, keep_muted)
    actions, act_more, counts, _ = build_actions(data_dir, now, max_actions)
    mv = {
        "updated": now.strftime("%a %-d %b %H:%M"),
        "days": cal_days, "cal_more": cal_more, "cal_total": cal_total,
        "cal_warn": warns,
        "agents": build_agents(data_dir, now),
        "actions": actions, "actions_more": act_more,
        "action_counts": counts, "actions_total": sum(counts.values()),
    }
    return {"merge_variables": mv}


def measure(payload):
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
    mv = json.dumps(payload["merge_variables"], ensure_ascii=False, separators=(",", ":")).encode()
    return len(body), len(mv)


# ── selftest: planted cases; each assertion is also run against a BROKEN variant
#    of the code under test and must FAIL there, or the test itself is void. ──
def selftest():
    import tempfile
    tz = datetime.timezone(datetime.timedelta(hours=11))
    now = datetime.datetime(2026, 10, 9, 13, 0, tzinfo=tz)
    fresh = now.isoformat()
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="trmnl_selftest_"))

    def w(name, obj):
        (tmp / name).write_text(json.dumps(obj))

    w("personal_calendar.json", {"collected_at": fresh, "data": {"events": [
        {"cal": "Family", "title": "Netball", "start": "2026-10-09T05:00:00Z", "allday": False},   # 16:00 today
        {"cal": "KREISER.org", "title": "Long gone", "start": "2026-10-08T22:00:00Z", "allday": False},  # 09:00 -> past >60m
        {"cal": "KREISER.org", "title": "Archived thing", "start": "2026-10-09T06:00:00Z", "allday": False},
        {"cal": "Family", "title": "Muted thing", "start": "2026-10-09T07:00:00Z", "allday": False}]}})
    w("datasec_calendar.json", {"collected_at": fresh, "data": {"events": [
        {"start": "2026-10-09T12:30:00.0000000", "title": "SECRET-CLIENT standup", "allday": False}]}})  # naive local: started 30m ago -> now
    w("secuura_calendar.json", {"collected_at": "2026-08-28T20:23:51+10:00", "data": {"events": [
        {"start": "2026-10-09T15:00:00+11:00", "title": "STALE-SECUURA", "allday": False}]}})
    w("layout.json", {"hidden_groups": []})
    w("archived.json", ["personal|Archived thing"])
    w("muted.json", ["personal|Muted thing"])
    w("usage_wednesday.json", {"agent": "wednesday", "pct": 16, "resets_in": "6d", "ts": "2026-10-09T01:55:00Z"})  # 5 min old
    w("usage_tuesday.json", {"agent": "tuesday", "pct": 100, "resets_in": "2d", "ts": "2026-10-08T05:48:05Z"})     # stale
    # friday file deliberately absent
    w("decisions.json", [
        {"id": "nexusai-x", "client_project": "Datasec/NexusAI", "title": "T-open-datasec", "status": "open",
         "ts": "2026-10-08T08:00:00+11:00", "default_action": "If you do not rule: nothing changes. More."},
        {"id": "secuura-y", "client_project": "Secuura/Blockchain", "title": "T-open-secuura", "status": "open",
         "ts": "2026-10-09T08:00:00+11:00", "default_action": "x"},
        {"id": "nexusai-f", "client_project": "Datasec/NexusAI", "title": "T-open-friday", "status": "open",
         "seat": "friday", "ts": "2026-10-09T09:00:00+11:00", "default_action": "y"},
        {"id": "z1", "client_project": "WED", "title": "T-ruled", "status": "ruled", "ts": "2026-10-01T00:00:00+11:00"},
        {"id": "z2", "client_project": "WED", "title": "T-withdrawn", "status": "withdrawn", "ts": "2026-10-01T00:00:00+11:00"},
    ])

    checks = []

    def check(name, good, broken):
        ok_good, ok_broken = bool(good()), bool(broken())
        checks.append((name, ok_good, not ok_broken))
        return ok_good and not ok_broken

    def titles(p):
        return [e["title"] for d in p["merge_variables"]["days"] for e in d["events"]]

    p = build(tmp, now)
    mv = p["merge_variables"]
    act_titles = [a["title"] for a in mv["actions"]]

    check("only OPEN cards are actions",
          lambda: act_titles and not {"T-ruled", "T-withdrawn"} & set(act_titles),
          lambda: {"T-ruled", "T-withdrawn"} & set(a["title"] for a in
                  build_actions(tmp, now, 6, predicate=lambda c: c.get("status") != "x")[0]) == set())
    check("seat attribution W/T/F = 1/1/1",
          lambda: mv["action_counts"] == {"Wednesday": 1, "Tuesday": 1, "Friday": 1},
          lambda: _counts_without_friday_rule(tmp, now) == {"Wednesday": 1, "Tuesday": 1, "Friday": 1})
    check("default_action loses its 'If you do not rule' preamble and stops at sentence 1",
          lambda: any(a["dflt"] == "nothing changes." for a in mv["actions"]),
          lambda: any(clip(c.get("default_action", ""), 80) == "nothing changes."
                      for c in json.loads((tmp / "decisions.json").read_text())))
    check("stale Secuura feed is NOT shown and IS warned",
          lambda: "STALE-SECUURA" not in titles(p) and any("Secuura" in x for x in mv["cal_warn"]),
          lambda: "STALE-SECUURA" not in _titles_without_staleness_gate(tmp, now))
    check("archived and >60-min-old events dropped; started-30m-ago kept as now",
          lambda: "Archived thing" not in titles(p) and "Long gone" not in titles(p)
          and any(e["now"] and e["title"].startswith("SECRET") for d in mv["days"] for e in d["events"]),
          lambda: "Long gone" not in [e["title"] for e in norm_events(tmp, now, [])])
    check("muted dropped by default, shown with keep_muted",
          lambda: "Muted thing" not in titles(p) and "Muted thing" in titles(build(tmp, now, keep_muted=True)),
          lambda: "Muted thing" not in titles(build(tmp, now, keep_muted=True)))
    def rows(pp):
        days_ = pp["merge_variables"]["days"]
        return len(days_) + sum(len(d["events"]) for d in days_), all(d["events"] for d in days_)
    check("row budget counts headings; no orphan heading; overflow counted",
          lambda: rows(build(tmp, now, max_rows=2))[0] <= 2 and rows(build(tmp, now, max_rows=2))[1]
          and build(tmp, now, max_rows=2)["merge_variables"]["cal_more"] >= 1,
          lambda: (len(sorted({e["start"].date() for e in norm_events(tmp, now, [])}))
                   + min(2, len(norm_events(tmp, now, [])))) <= 2)   # broken: budget = events only
    pr = build(tmp, now, redact=frozenset({"datasec"}))
    check("redaction removes the Datasec title from the WHOLE payload",
          lambda: "SECRET-CLIENT" not in json.dumps(pr) and "Datasec event" in titles(pr),
          lambda: "SECRET-CLIENT" not in json.dumps(p))
    ag = {a["name"]: a for a in mv["agents"]}
    check("usage: fresh not stale, 20h-old stale, missing file shown as none",
          lambda: (not ag["Wednesday"]["stale"]) and ag["Tuesday"]["stale"]
          and ag["Friday"]["pct"] is None and ag["Friday"]["age"] == "none",
          lambda: {a["name"]: a for a in _agents_with_gate(tmp, now, 10 ** 9)}["Tuesday"]["stale"])
    big, _ = measure(p)
    check("over-limit payload is refused (exit 3)",
          lambda: _run_main_exit(["--data-dir", str(tmp), "--now", now.isoformat(), "--limit", str(big - 1)]) == 3,
          lambda: _run_main_exit(["--data-dir", str(tmp), "--now", now.isoformat(), "--limit", str(big + 10)]) == 3)

    bad = 0
    for name, g, b in checks:
        verdict = "PASS" if (g and b) else "FAIL"
        bad += verdict == "FAIL"
        print(f"  {verdict}  {name}   [good={g} broken-variant-caught={b}]")
    print(f"selftest: {len(checks) - bad}/{len(checks)} pass (temp data {tmp})")
    return 1 if bad else 0


def _counts_without_friday_rule(tmp, now):
    cards = json.loads((tmp / "decisions.json").read_text())
    c = {"Wednesday": 0, "Tuesday": 0, "Friday": 0}
    for k in cards:
        if needs_kam(k):
            c["Tuesday" if is_datasec(k) else "Wednesday"] += 1       # broken: ignores seat=friday
    return c


def _titles_without_staleness_gate(tmp, now):
    global FEED_STALE_S
    saved, FEED_STALE_S = FEED_STALE_S, 10 ** 12                     # broken: gate disabled
    try:
        return [e["title"] for e in norm_events(tmp, now, [])]
    finally:
        FEED_STALE_S = saved


def _agents_with_gate(tmp, now, gate):
    global USE_STALE_S
    saved, USE_STALE_S = USE_STALE_S, gate                           # broken: gate effectively off
    try:
        return build_agents(tmp, now)
    finally:
        USE_STALE_S = saved


def _run_main_exit(argv):
    import contextlib, io
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            main(argv)
    except SystemExit as e:
        return e.code
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--max-rows", type=int, default=MAX_ROWS_DEFAULT, help="left-column rows incl. day headings")
    ap.add_argument("--max-actions", type=int, default=MAX_ACTIONS_DEFAULT)
    ap.add_argument("--redact", default="", help="comma list of datasec,secuura,personal,family")
    ap.add_argument("--limit", type=int, default=5120, help="bytes; 5 KB standard, 10240 with TRMNL+")
    ap.add_argument("--data-dir", default=str(DATA_DEFAULT))
    ap.add_argument("--now", default="", help="ISO time, for tests")
    ap.add_argument("--keep-muted", action="store_true", help="show events Kam muted on the dashboard")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--measure", action="store_true", help="print sizes to stderr")
    a = ap.parse_args(argv)
    if a.selftest:
        sys.exit(selftest())
    redact = frozenset(x.strip().lower() for x in a.redact.split(",") if x.strip())
    unknown = redact - set(SRC_LABEL)
    if unknown:
        die(f"--redact: unknown group(s) {sorted(unknown)}; use {sorted(SRC_LABEL)}")
    now = (datetime.datetime.fromisoformat(a.now) if a.now else datetime.datetime.now()).astimezone()
    payload = build(pathlib.Path(a.data_dir), now, a.days, a.max_rows, a.max_actions, redact, a.keep_muted)
    body_b, mv_b = measure(payload)
    if a.measure:
        print(f"build_payload: body {body_b} B, merge_variables {mv_b} B, limit {a.limit} B", file=sys.stderr)
    if max(body_b, mv_b) > a.limit:
        die(f"payload {body_b} B exceeds --limit {a.limit} B; lower --max-rows/--max-actions", code=3)
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
