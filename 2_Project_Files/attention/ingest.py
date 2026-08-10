#!/usr/bin/env python3
"""ingest.py — pull NEW attention items into Wednesday's unified queue.

Called by ingest.sh (which sources 4_Credentials/.env). Reads keys from the
environment only — never prints them, never writes them anywhere.

Sources (all read-only):
  mail    — AgentMail inboxes wednesday-agent@ + coagent@ (inbound only;
            messages FROM wednesday-agent@ skipped — those are Wednesday's own)
  chat    — 0_Brain/dashboard/data/chat_log.json, role == "kam" only
  linear  — Linear WED-team issues updated since last run

Queue: 0_Brain/attention/queue.json — summary + source_ref pointer ONLY,
never full bodies. Wednesday's and Kam's eyes only.

Dedupe: by source_ref against the whole queue. Cursors (per-source
last-seen timestamp) live in state/ (gitignored) and only bound the scan;
correctness comes from the dedupe.

NEVER sets read=true on anything — marking is queue.sh's explicit act only
(learning 2026-08-04: acknowledgment covers exactly what was explicitly
marked, nothing else).
"""
import json
import os
import re
import sys
import hashlib
import datetime
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
QUEUE_DIR = os.path.join(PROJECT_DIR, "0_Brain", "attention")
QUEUE_FILE = os.path.join(QUEUE_DIR, "queue.json")
STATE_DIR = os.path.join(SCRIPT_DIR, "state")
CHAT_LOG = os.path.join(PROJECT_DIR, "0_Brain", "dashboard", "data", "chat_log.json")

MAIL_INBOXES = ["wednesday-agent@agentmail.to", "coagent@agentmail.to"]
OWN_ADDR = "wednesday-agent@agentmail.to"


def parse_ts(s):
    """ISO timestamp -> aware datetime (naive assumed UTC). None on failure."""
    if not s:
        return None
    try:
        dt = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt
    except ValueError:
        return None


def read_cursor(name):
    p = os.path.join(STATE_DIR, "cursor_%s.txt" % name)
    if os.path.exists(p):
        with open(p) as f:
            return f.read().strip()
    return ""


PENDING_CURSORS = {}


def write_cursor(name, value):
    """Record a cursor advance; applied by main() only AFTER the queue is
    safely persisted (else a failed save would strand items behind the
    cursor and they would never re-ingest)."""
    if value:
        PENDING_CURSORS[name] = value


def flush_cursors():
    for name, value in PENDING_CURSORS.items():
        p = os.path.join(STATE_DIR, "cursor_%s.txt" % name)
        with open(p, "w") as f:
            f.write(value + "\n")


def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE) as f:
            return json.load(f)
    return []


def save_queue(items):
    os.makedirs(QUEUE_DIR, exist_ok=True)
    tmp = QUEUE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(items, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, QUEUE_FILE)


def clean_summary(text):
    return " ".join((text or "").split())[:200]


def make_item(channel, ts, client_project, kind, summary, source_ref):
    return {
        "id": hashlib.sha1(source_ref.encode("utf-8")).hexdigest()[:10],
        "ts": ts,
        "channel": channel,
        "client_project": client_project,
        "kind": kind,
        "summary": clean_summary(summary),
        "source_ref": source_ref,
        "read": False,
        "actioned": False,
    }


def http_json(url, headers, data=None, timeout=30):
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


# ── mail ─────────────────────────────────────────────────────────────────
def ingest_mail(add):
    key = os.environ.get("AGENTMAIL_API_KEY", "")
    if not key:
        raise RuntimeError("AGENTMAIL_API_KEY not set")
    for inbox in MAIL_INBOXES:
        cursor_name = "mail_" + inbox.split("@")[0]
        cursor = parse_ts(read_cursor(cursor_name))
        d = http_json(
            "https://api.agentmail.to/v0/inboxes/%s/messages?limit=50" % inbox,
            {"Authorization": "Bearer " + key},
        )
        newest = cursor
        newest_raw = None
        for m in d.get("messages", []):
            ts_raw = m.get("timestamp", "")
            ts = parse_ts(ts_raw)
            if ts and (newest is None or ts > newest):
                newest, newest_raw = ts, ts_raw
            # inbound only: skip Wednesday's own sent mail
            if "sent" in (m.get("labels") or []):
                continue
            if OWN_ADDR in (m.get("from") or ""):
                continue
            if cursor and ts and ts <= cursor:
                continue
            subj = m.get("subject") or "(no subject)"
            mm = re.match(r"\[([^\]]+?)\s*->", subj)
            client_project = mm.group(1) if mm else "-"
            if "QUESTION" in subj:
                kind = "question"
            elif "Session wrap" in subj:
                kind = "wrap"
            else:
                kind = "mail"
            summary = subj
            preview = (m.get("preview") or "").strip()
            if preview:
                summary = subj + " — " + preview
            add(make_item(
                "mail", ts_raw, client_project, kind, summary,
                "mail:%s:%s" % (inbox, m.get("message_id", "")),
            ))
        if newest_raw:
            write_cursor(cursor_name, newest_raw)


# ── dashboard chat (Kam's messages only) ─────────────────────────────────
def ingest_chat(add):
    if not os.path.exists(CHAT_LOG):
        raise RuntimeError("chat log not found: %s" % CHAT_LOG)
    with open(CHAT_LOG) as f:
        msgs = json.load(f)
    cursor = parse_ts(read_cursor("chat"))
    newest = cursor
    newest_raw = None
    for m in msgs:
        if m.get("role") != "kam":
            continue
        ts_raw = m.get("ts", "")
        ts = parse_ts(ts_raw)
        if ts and (newest is None or ts > newest):
            newest, newest_raw = ts, ts_raw
        if cursor and ts and ts <= cursor:
            continue
        add(make_item(
            "chat", ts_raw, "Wednesday", "chat",
            m.get("text", ""), "chat:%s" % ts_raw,
        ))
    if newest_raw:
        write_cursor("chat", newest_raw)


# ── Linear WED issues updated since last run ─────────────────────────────
def ingest_linear(add):
    key = os.environ.get("LINEAR_API_KEY", "")
    if not key:
        raise RuntimeError("LINEAR_API_KEY not set")
    cursor_raw = read_cursor("linear")
    date_filter = ""
    if cursor_raw:
        date_filter = ', updatedAt:{gt:"%s"}' % cursor_raw
    q = {"query": """query{ issues(filter:{team:{key:{eq:"WED"}}%s},
          first:50, orderBy: updatedAt){
          nodes{ identifier title updatedAt priority state{name} } } }""" % date_filter}
    r = http_json(
        "https://api.linear.app/graphql",
        {"Authorization": key, "Content-Type": "application/json"},
        data=json.dumps(q).encode(),
    )
    if "errors" in r:
        raise RuntimeError("Linear GraphQL errors: %s" % r["errors"])
    cursor = parse_ts(cursor_raw)
    newest = cursor
    newest_raw = None
    for n in r["data"]["issues"]["nodes"]:
        ts_raw = n.get("updatedAt", "")
        ts = parse_ts(ts_raw)
        if ts and (newest is None or ts > newest):
            newest, newest_raw = ts, ts_raw
        if cursor and ts and ts <= cursor:
            continue
        state = (n.get("state") or {}).get("name", "?")
        add(make_item(
            "linear", ts_raw, "Wednesday/WED", "issue",
            "%s %s [%s]" % (n.get("identifier"), n.get("title"), state),
            "linear:%s" % n.get("identifier"),
        ))
    if newest_raw:
        write_cursor("linear", newest_raw)


def main():
    os.makedirs(STATE_DIR, exist_ok=True)
    queue = load_queue()
    known = set(it["source_ref"] for it in queue)
    added = {"mail": 0, "chat": 0, "linear": 0}
    current = [None]

    def add(item):
        if item["source_ref"] in known:
            return
        known.add(item["source_ref"])
        queue.append(item)
        added[current[0]] += 1

    failed = []
    for name, fn in (("mail", ingest_mail), ("chat", ingest_chat),
                     ("linear", ingest_linear)):
        current[0] = name
        try:
            fn(add)
        except Exception as e:
            failed.append(name)
            sys.stderr.write("ATTENTION INGEST ERROR (%s): %s\n" % (name, e))

    save_queue(queue)
    flush_cursors()
    total_new = sum(added.values())
    print("ingest: %d new (mail %d, chat %d, linear %d) — queue total %d"
          % (total_new, added["mail"], added["chat"], added["linear"], len(queue)))
    if failed:
        sys.stderr.write("ingest: FAILED sources: %s (their cursors not advanced)\n"
                         % ", ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
