#!/usr/bin/env python3
"""linear_fetch.py - READ-ONLY snapshot of the Secuura Linear board (team KS) for the weekly Stuart list.

Why a script and not the model: the project's own LINEAR_API_KEY is read HERE, in-process, from
Secuura/Blockchain/4_Credentials/.env, and is never printed, written or handed to the headless model. The model reads
the snapshot files this script writes. Only GraphQL *queries* are sent (asserted below): no write to the board.

Board rules honoured (count rules): OPEN = state.type not in (completed, canceled); pages followed until hasNextPage is
false (unbounded); comments(first:50) per issue sorted CLIENT-SIDE by updatedAt (never last:N); an issue returning 50
comments is marked comments_capped (its newest comment is UNMEASURED against the full thread).

Usage: linear_fetch.py <out_dir>      writes board_summary.json (aggregates + predicate) and board_open.jsonl (one issue per line)
Exit: 0 ok - 2 cannot read key/board (stderr says why).
"""
import json, os, sys, time, urllib.request, urllib.error

ENVFILE = os.environ.get("STUART_LINEAR_ENV", "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env")
URL = "https://api.linear.app/graphql"
PAGE = 20  # 20 issues x 50 comments keeps each query under Linear's complexity limit
STUART = ("stuart", "jamieson")
PETER = ("peter", "obeden")


def read_key():
    try:
        for l in open(ENVFILE, encoding="utf-8"):
            if l.startswith("LINEAR_API_KEY="):
                k = l.split("=", 1)[1].strip().strip('"').strip("'")
                if k:
                    return k
    except OSError as e:
        sys.exit("linear_fetch: cannot read %s: %s" % (ENVFILE, e))
    sys.exit("linear_fetch: LINEAR_API_KEY not found in %s" % ENVFILE)


def gql(key, query, variables=None):
    assert query.lstrip().startswith(("query", "{")), "queries only"
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json", "Authorization": key})
            d = json.load(urllib.request.urlopen(req, timeout=120))
            if d.get("errors"):
                raise RuntimeError("GraphQL errors: " + json.dumps(d["errors"])[:300])
            return d["data"]
        except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
            last = e
            time.sleep(3 * (attempt + 1))
    sys.exit("linear_fetch: Linear query failed after retries: %s" % (str(last).replace(key, "<key>")[:300]))


def who(u):
    u = u or {}
    return {"name": u.get("name"), "email": u.get("email"), "id": u.get("id")}


def has(u, needles):
    s = ((u or {}).get("name") or "") + " " + ((u or {}).get("email") or "")
    s = s.lower()
    return any(n in s for n in needles)


def slim(r):
    """Row with the newest comment cut to who/when/first 160 chars (the full body lives in board_open.jsonl)."""
    r = dict(r)
    nc = r.get("newest_comment")
    if nc:
        r["newest_comment"] = {"by": nc["by"], "is_board_account": nc["is_board_account"], "at": nc["at"], "body": nc["body"][:160]}
    return r


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    key = read_key()
    viewer = gql(key, "query{viewer{id name email}}")["viewer"]
    q = ("query($after:String){issues(first:%d, after:$after, filter:{team:{key:{eq:\"KS\"}}, state:{type:{nin:[\"completed\",\"canceled\"]}}}){"
         "nodes{identifier title priority priorityLabel createdAt updatedAt state{name type} assignee{id name email} "
         "comments(first:50){nodes{id body createdAt updatedAt user{id name email}}}} pageInfo{hasNextPage endCursor}}}" % PAGE)
    issues, after, pages = [], None, 0
    while True:
        d = gql(key, q, {"after": after})["issues"]
        issues += d["nodes"]
        pages += 1
        if not d["pageInfo"]["hasNextPage"]:
            break
        after = d["pageInfo"]["endCursor"]
    rows, by_assignee, human_newest = [], {}, []
    for i in issues:
        cs = sorted(i["comments"]["nodes"], key=lambda c: c.get("updatedAt") or c.get("createdAt") or "")
        capped = len(cs) >= 50
        newest = cs[-1] if cs else None
        a = i.get("assignee")
        an = (a or {}).get("name") or "UNASSIGNED"
        if a and a.get("id") == viewer["id"]:
            an = "BOARD-ACCOUNT(%s)" % viewer.get("name")
        by_assignee[an] = by_assignee.get(an, 0) + 1
        nc = None
        if newest:
            nu = newest.get("user") or {}
            nc = {"by": nu.get("name") or "?", "email": nu.get("email"), "is_board_account": nu.get("id") == viewer["id"],
                  "at": newest.get("updatedAt") or newest.get("createdAt"), "body": (newest.get("body") or "")[:900]}
        row = {"id": i["identifier"], "title": i["title"], "state": i["state"]["name"], "priority": i["priorityLabel"],
               "assignee": an, "created": i["createdAt"], "updated": i["updatedAt"], "n_comments": len(cs),
               "comments_capped": capped, "newest_comment": nc}
        if nc and not nc["is_board_account"]:
            human_newest.append(row)
        rows.append(row)
    with open(os.path.join(out, "board_open.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    stuart = [r for r, i in zip(rows, issues) if has(i.get("assignee"), STUART)]
    peter = [r for r, i in zip(rows, issues) if has(i.get("assignee"), PETER)]
    summary = {
        "read_at": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "predicate": "team KS, state.type not in (completed, canceled); pages of %d followed until hasNextPage=false (%d pages); "
                     "comments(first:50) per issue sorted client-side by updatedAt; newest comment = last of that sort" % (PAGE, pages),
        "key_identity": "the board account is the Linear user the project key belongs to: %s" % viewer.get("name"),
        "open_issues": len(rows),
        "assignee_counts": dict(sorted(by_assignee.items(), key=lambda kv: -kv[1])),
        "stuart_assigned_count": len(stuart),
        "peter_assigned_count": len(peter),
        "positive_control": "the stuart filter matches by name/email substring and returns %d; a Peter zero is a real zero only if this is non-zero and Peter is known to be assigned nothing" % len(stuart),
        "open_with_newest_comment_by_a_human_not_the_board_account": len(human_newest),
        "newest_comment_human_by_person": {},
        "capped_issues_newest_comment_unmeasured": [r["id"] for r in rows if r["comments_capped"]],
        "stuart_assigned": stuart,
        "newest_comment_human": human_newest,
        "decision_tickets_open": [slim(r) for r in rows if "[decision]" in r["title"].lower()],
        "urgent_or_high_open_count": sum(1 for r in rows if r["priority"] in ("Urgent", "High")),
        "files": {"all_open_issues_one_per_line": "board_open.jsonl"},
    }
    for r in human_newest:
        k = r["newest_comment"]["by"]
        summary["newest_comment_human_by_person"][k] = summary["newest_comment_human_by_person"].get(k, 0) + 1
    with open(os.path.join(out, "board_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)
    print("linear_fetch: %d open issues, %d pages, %d with a human newest comment, %d capped -> %s" % (len(rows), pages, len(human_newest), len(summary["capped_issues_newest_comment_unmeasured"]), out))


if __name__ == "__main__":
    main()
