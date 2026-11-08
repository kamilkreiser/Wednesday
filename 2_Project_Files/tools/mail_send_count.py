#!/usr/bin/env python3
"""mail_send_count.py: how many mails the WHOLE fleet has sent today, against Agent Mail's daily plan limit.

WHY (Kam, live board 2026-11-08 20:46-20:49: no $200 tier, "make the change"; ledger 2026-11-06: the
fleet hit the 1000-a-day plan limit at 23:14 and nobody knew the limit existed). The limit is per
organisation and counts every inbox's sends; send_brief's own sent_log sees only this seat's share.

WHAT IT READS: for every inbox the key can list, the TIMESTAMPS of messages labelled 'sent' since
00:00 UTC (the plan day: the 11-06 reset came at 11:00 AEDT = 00:00 UTC). It never reads a subject,
a sender or a body, so another client's inbox contributes a number and nothing else (hard rule 2).

OUTPUT: one line, 'MAILCOUNT: <n> sent today (UTC) across <k> inboxes · <ok|WARN 700|HOLD 900>', plus
an action line at WARN or HOLD. A cache (60 s) keeps send_brief from hammering the API.
Exit 0 always; an unreadable count prints 'MAILCOUNT: unreadable (<why>)' so a caller never mistakes
an error for a zero.
Env: AGENTMAIL_API_KEY (required) · MAILCOUNT_WARN (700) · MAILCOUNT_HOLD (900) ·
     MAILCOUNT_CACHE (path; default 2_Project_Files/fleet/state/mail_send_count.json) · MAILCOUNT_NOCACHE=1
"""
import datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("MAILCOUNT_CACHE", os.path.join(HERE, "..", "fleet", "state", "mail_send_count.json"))
WARN = int(os.environ.get("MAILCOUNT_WARN", "700"))
HOLD = int(os.environ.get("MAILCOUNT_HOLD", "900"))
BASE = "https://api.agentmail.to/v0"


def get(url, key):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + key})
    return json.load(urllib.request.urlopen(req, timeout=20))


def count(key):
    day0 = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
    inboxes = [i.get("inbox_id") or i.get("email") for i in get(BASE + "/inboxes?limit=100", key).get("inboxes", [])]
    if not inboxes:
        raise RuntimeError("the key lists no inboxes")
    total = 0
    for ib in inboxes:
        token = None
        for _ in range(50):  # 50 pages x 100 = 5000 per inbox, far past the plan limit
            q = {"limit": "100", "labels": "sent", "after": day0}
            if token:
                q["page_token"] = token
            d = get(f"{BASE}/inboxes/{urllib.parse.quote(ib)}/messages?" + urllib.parse.urlencode(q), key)
            total += len(d.get("messages", []))
            token = d.get("next_page_token")
            if not token:
                break
        else:
            raise RuntimeError(f"pagination did not end for one inbox")
    return total, len(inboxes), day0


def main():
    key = os.environ.get("AGENTMAIL_API_KEY", "")
    if not key:
        print("MAILCOUNT: unreadable (AGENTMAIL_API_KEY unset)")
        return 0
    now = time.time()
    if os.environ.get("MAILCOUNT_NOCACHE") != "1":
        try:
            c = json.load(open(CACHE))
            if now - c["at"] < 60 and c["day0"] == datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT00:00:00Z"):
                return report(c["n"], c["k"], cached=True)
        except Exception:
            pass
    try:
        n, k, day0 = count(key)
    except urllib.error.HTTPError as e:
        print(f"MAILCOUNT: unreadable (HTTP {e.code} {e.read(200).decode('utf-8', 'replace')})")
        return 0
    except Exception as e:
        print(f"MAILCOUNT: unreadable ({e})")
        return 0
    try:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump({"at": now, "n": n, "k": k, "day0": day0}, open(CACHE, "w"))
    except Exception as e:
        print(f"mail_send_count: cache not written ({e})", file=sys.stderr)
    return report(n, k)


def report(n, k, cached=False):
    state = "HOLD 900" if n >= HOLD else ("WARN 700" if n >= WARN else "ok")
    print(f"MAILCOUNT: {n} sent today (UTC) across {k} inboxes · limit 1000 · {state}{' (cached <60 s)' if cached else ''}")
    if n >= HOLD:
        print("MAILCOUNT: ⚠ HOLD: mail every live seat (one ADDENDUM each) to send ONLY QUESTION and MERGED until 11:00 AEDT; everything else goes to a file in its record folder.")
    elif n >= WARN:
        print("MAILCOUNT: ⚠ WARN: tell every live seat to cut to READY, QUESTION, MERGED and wraps, long bodies as files with a one-line pointer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
