#!/usr/bin/env python3
"""chat_streams.py — regenerate the DERIVED chat_log.json from the per-agent streams.

WHY THIS EXISTS (Kam's 2026-09-08 11:50 commission, Phase 0 of the two-agent plan).
Two Wednesday seats appended to ONE tracked `chat_log.json` through git. It was
corrupted THREE times on 2026-09-08 alone — twice by concurrent writes, once by a
stash pop at a rotation — and each repair was by hand. The claims files, one per
seat, have never once conflicted, because only one writer touches each file. That
is structure, not discipline, and this makes the chat the same shape.

    WRITTEN (tracked, one writer each)        DERIVED (untracked)
      chat_legacy.json     FROZEN 2026-09-08
      chat_wednesday.json  Studio seat only  \
      chat_tuesday.json    Datasec seat only  >--> chat_log.json
      chat_kam.json        the panel only    /

Every existing reader (generate.py, wake_watch.sh, kam_rulings_today.sh,
attention/ingest.py, decision_queue.sh, sync_kam_rulings.sh) keeps reading
`chat_log.json` unchanged — thirteen tracked consumers, none of which had to move.

THE `agent` FIELD IS DERIVED FROM THE STREAM, NEVER TYPED. A hand-set field can be
got wrong; the filename cannot. Legacy entries pre-date the split and are marked
`agent_source: "inferred"` so the toggle never presents a guess as a fact.

Usage:  chat_streams.py [--check]
        --check   report only; write nothing (exit 1 if the derived file is stale)
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "0_Brain", "dashboard", "data")

# stream file -> the agent every entry in it belongs to. The mapping IS the
# authority: a writer that appends to the wrong file is the only way to get the
# agent wrong, and each writer knows only its own path.
STREAMS = [
    ("chat_wednesday.json", "wednesday"),
    ("chat_tuesday.json", "tuesday"),
    ("chat_kam.json", None),        # Kam's own: agent comes from the view he sent it in
]
LEGACY = "chat_legacy.json"
DERIVED = "chat_log.json"


def load(path):
    """Read a stream. A missing stream is empty, not an error — a fresh clone
    or a seat that has never spoken has no file yet. A stream that will NOT
    parse is FATAL: never silently drop a seat's conversation."""
    if not os.path.exists(path):
        return []
    raw = open(path).read()
    if not raw.strip():
        return []
    try:
        d = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.stderr.write(
            "chat_streams: %s WILL NOT PARSE (%s) — refusing to write a derived\n"
            "  log that silently omits it. Repair the stream first; nothing was written.\n"
            % (os.path.basename(path), e))
        sys.exit(3)
    if not isinstance(d, list):
        sys.stderr.write("chat_streams: %s is not a list — refusing.\n" % os.path.basename(path))
        sys.exit(3)
    return [e for e in d if isinstance(e, dict)]


def legacy_agent(entry):
    """Attribute a pre-split entry from fields it already carries. Kam's own
    messages pre-date the toggle and were addressed to nobody in particular, so
    they show in BOTH views rather than being assigned to one."""
    if entry.get("role") == "kam":
        return "both"
    proj = (entry.get("project") or "").strip()
    seat = (entry.get("seat") or "")
    if proj == "Datasec" or "MBP" in seat:
        return "tuesday"
    return "wednesday"


def build():
    entries, per_source = [], []

    legacy = load(os.path.join(DATA, LEGACY))
    for e in legacy:
        e = dict(e)
        e["agent"] = legacy_agent(e)
        e["agent_source"] = "inferred"
        entries.append(e)
    per_source.append((LEGACY, len(legacy)))

    for fname, agent in STREAMS:
        msgs = load(os.path.join(DATA, fname))
        for e in msgs:
            e = dict(e)
            # Kam's stream carries the view he was looking at; anything else is
            # named by its file. "both" is the honest default before the toggle
            # ships — never a guess at which client he meant.
            e["agent"] = agent or (e.get("view") or "both")
            e["agent_source"] = "stream"
            entries.append(e)
        per_source.append((fname, len(msgs)))

    # Union on (ts, text) — the same key safe_push.sh and union_chat_log.py use.
    # Duplicates across streams cannot happen by construction; the union is here
    # so a re-run after a manual repair is idempotent rather than doubling.
    seen, merged = set(), []
    for e in entries:
        k = (e.get("ts", ""), e.get("text", ""))
        if k in seen:
            continue
        seen.add(k)
        merged.append(e)
    merged.sort(key=lambda e: str(e.get("ts", "")))
    return merged, per_source


def orphans(merged, out):
    """Entries in the CURRENT derived file that no stream accounts for.

    MEASURED, not theorised: within three minutes of the cutover the still-running
    old server appended one of Kam's messages straight to chat_log.json, and the
    next rebuild would have erased it without a word. A rebuild that silently drops
    the principal's own sentence is worse than no rebuild at all, so it REFUSES and
    names them. `--harvest` routes each one into the stream its own fields name."""
    if not os.path.exists(out):
        return []
    try:
        cur = json.loads(open(out).read())
    except Exception:
        return []          # unparseable derived file is regenerated, not mourned
    if not isinstance(cur, list):
        return []
    have = {(e.get("ts", ""), e.get("text", "")) for e in merged}
    return [e for e in cur if isinstance(e, dict)
            and (e.get("ts", ""), e.get("text", "")) not in have]


def harvest(found):
    """Route orphans to the stream their own fields name. Anything unattributable
    is REFUSED rather than filed under a guess — a message in the wrong agent's
    stream is a cross-client leak, which is the one failure this phase exists to
    prevent."""
    routed, refused = {}, []
    for e in found:
        e = {k: v for k, v in e.items() if k not in ("agent", "agent_source")}
        if e.get("role") == "kam":
            tgt = "chat_kam.json"
        elif "MBP" in (e.get("seat") or "") or e.get("project") == "Datasec":
            tgt = "chat_tuesday.json"
        elif e.get("seat"):
            tgt = "chat_wednesday.json"
        else:
            refused.append(e)
            continue
        routed.setdefault(tgt, []).append(e)
    for fname, entries in routed.items():
        p = os.path.join(DATA, fname)
        cur = load(p)
        cur.extend(entries)
        cur.sort(key=lambda e: str(e.get("ts", "")))
        with open(p, "w") as f:
            f.write(json.dumps(cur, ensure_ascii=False, indent=1))
        print("chat_streams: harvested %d into %s" % (len(entries), fname))
    return refused


def main():
    check = "--check" in sys.argv[1:]
    do_harvest = "--harvest" in sys.argv[1:]
    merged, per_source = build()
    out = os.path.join(DATA, DERIVED)

    found = orphans(merged, out)
    if found and do_harvest:
        refused = harvest(found)
        for e in refused:
            sys.stderr.write("chat_streams: CANNOT ROUTE %s %r — file it by hand.\n"
                             % (e.get("ts"), (e.get("text") or "")[:70]))
        if refused:
            sys.exit(4)
        merged, per_source = build()
        found = orphans(merged, out)
    if found:
        sys.stderr.write(
            "chat_streams: 🔴 %d entr%s in chat_log.json that NO stream holds — a writer\n"
            "  bypassed the streams. Rebuilding would DELETE them. Nothing was written.\n"
            "  Re-run with --harvest to route them, or file them by hand:\n"
            % (len(found), "y" if len(found) == 1 else "ies"))
        for e in found[:10]:
            sys.stderr.write("    %s %s %r\n" % (e.get("role"), e.get("ts"),
                                                 (e.get("text") or "")[:70]))
        sys.exit(4)

    body = json.dumps(merged, ensure_ascii=False, indent=1)
    if check:
        cur = open(out).read() if os.path.exists(out) else None
        stale = cur != body
        sys.stderr.write("chat_streams --check: %s (%d entries from %s)\n" % (
            "STALE" if stale else "current", len(merged),
            " + ".join("%s %d" % (n, c) for n, c in per_source)))
        sys.exit(1 if stale else 0)

    # A derived file is still Kam's reading surface: never leave it half-written.
    fd, tmp = tempfile.mkstemp(dir=DATA, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        f.write(body)
    os.replace(tmp, out)

    # Conservation, printed rather than assumed: the derived file must hold at
    # least as many entries as the largest source, and exactly the union size.
    print("chat_streams: %s <- %s = %d entries" % (
        DERIVED, " + ".join("%s %d" % (n, c) for n, c in per_source), len(merged)))


if __name__ == "__main__":
    main()
