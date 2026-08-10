#!/usr/bin/env python3
"""queue_cli.py — list/mark/count for Wednesday's unified attention queue.

Marking read is ALWAYS explicit (this tool, `mark`) — never a side effect
of ingest or list (learning 2026-08-04: blanket mark-seen swallowed a live
QUESTION; acknowledgment covers exactly what was explicitly marked).
"""
import json
import os
import sys
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
QUEUE_FILE = os.path.join(PROJECT_DIR, "0_Brain", "attention", "queue.json")
STATE_DIR = os.path.join(SCRIPT_DIR, "state")
LAST_LISTED = os.path.join(STATE_DIR, "last_listed.txt")


def parse_ts(s):
    try:
        dt = datetime.datetime.fromisoformat((s or "").replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt
    except ValueError:
        return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


def load():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save(items):
    tmp = QUEUE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(items, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, QUEUE_FILE)


def line(it):
    return "%s  [%s] %s | %s" % (
        it["id"], it["channel"], it["client_project"], it["summary"])


def cmd_list():
    items = load()
    unread = sorted([i for i in items if not i["read"]],
                    key=lambda i: parse_ts(i["ts"]), reverse=True)
    read = sorted([i for i in items if i["read"]],
                  key=lambda i: parse_ts(i["ts"]), reverse=True)
    print("UNREAD (%d):" % len(unread))
    for it in unread:
        print("  " + line(it))
    if read:
        print("READ (%d):" % len(read))
        for it in read[:10]:
            print("  " + line(it))
        if len(read) > 10:
            print("  … %d more read (in queue.json)" % (len(read) - 10))
    # record what was listed as unread, for `mark all-listed`
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(LAST_LISTED, "w") as f:
        for it in unread:
            f.write(it["id"] + "\n")


def cmd_mark(target):
    items = load()
    if target == "all-listed":
        if not os.path.exists(LAST_LISTED):
            sys.stderr.write("mark all-listed: nothing listed yet (run list first)\n")
            sys.exit(1)
        with open(LAST_LISTED) as f:
            ids = set(l.strip() for l in f if l.strip())
    else:
        ids = {target}
    hit = 0
    for it in items:
        if it["id"] in ids and not it["read"]:
            it["read"] = True
            hit += 1
    if target != "all-listed" and hit == 0:
        known = any(it["id"] == target for it in items)
        if not known:
            sys.stderr.write("mark: no item with id %s\n" % target)
            sys.exit(1)
        print("marked 0 (already read)")
        return
    save(items)
    print("marked %d read" % hit)


def cmd_count():
    items = load()
    unread = sum(1 for i in items if not i["read"])
    print("%d unread / %d total" % (unread, len(items)))


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: queue_cli.py list|mark <id|all-listed>|count\n")
        sys.exit(2)
    cmd = sys.argv[1]
    if cmd == "list":
        cmd_list()
    elif cmd == "mark":
        if len(sys.argv) != 3:
            sys.stderr.write("usage: queue_cli.py mark <id|all-listed>\n")
            sys.exit(2)
        cmd_mark(sys.argv[2])
    elif cmd == "count":
        cmd_count()
    else:
        sys.stderr.write("unknown command: %s\n" % cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()
