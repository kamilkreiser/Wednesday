#!/usr/bin/env python3
"""QA-MEASURE-2-R2 task 5 (T-d): my own count over the quarantined transcripts and the committed headless streams.
COUNTS ONLY, never content. Walks EVERY file at ANY depth under each root (not only top-level .jsonl).
usage: python3 -I -B qm2r_modelcount.py <root>... [--control]
Per file and in total: entries per top-level `type`; assistant messages per message.model; content-block types (all of
them, any type the seat did not count included); server_tool_use blocks per name; tool_use blocks per name CLASS (mcp__*,
built-in name, other); every "model" value found at ANY depth of an entry; keys at any depth containing "advisor";
occurrences of the byte string "advisor" (case-insensitive) in the raw file; `modelUsage` keys.
--control: the same counter over an in-memory planted transcript with one other-model message, one server_tool_use block
named oddly (no "advisor" in the name), one block of a made-up type and a nested model field."""
import collections, json, os, sys
sys.dont_write_bytecode = True
def walk_models(o, acc, keys):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "model" and isinstance(v, str): acc[v] += 1
            if "advisor" in k.lower(): keys[k] += 1
            walk_models(v, acc, keys)
    elif isinstance(o, list):
        for v in o: walk_models(v, acc, keys)
def count_lines(lines, raw):
    c = {k: collections.Counter() for k in ("entry", "asst_model", "block", "stu", "tool_class", "any_model", "adv_keys", "usage")}
    bad = 0
    for l in lines:
        try: e = json.loads(l)
        except ValueError: bad += 1; continue
        if not isinstance(e, dict): continue
        c["entry"][e.get("type")] += 1
        walk_models(e, c["any_model"], c["adv_keys"])
        for k in (e.get("modelUsage") or {}): c["usage"][k] += 1
        m = e.get("message")
        if isinstance(m, dict):
            if e.get("type") == "assistant": c["asst_model"][m.get("model")] += 1
            cont = m.get("content")
            if isinstance(cont, list):
                for b in cont:
                    if not isinstance(b, dict): continue
                    c["block"][b.get("type")] += 1
                    if b.get("type") == "server_tool_use": c["stu"][b.get("name")] += 1
                    if b.get("type") == "tool_use":
                        n = str(b.get("name", "")); c["tool_class"]["mcp__*" if n.startswith("mcp__") else n] += 1
    c["adv_bytes"] = raw.lower().count(b"advisor"); c["unparsed"] = bad
    return c
def show(label, c):
    print("%s | entries %s | assistant per model %s | block types %s | server_tool_use %s | tool_use %s | model values at any depth %s | advisor keys %s | 'advisor' bytes %d | modelUsage %s | unparsed %d" % (
        label, dict(c["entry"]), dict(c["asst_model"]), dict(c["block"]), dict(c["stu"]), dict(c["tool_class"]), dict(c["any_model"]), dict(c["adv_keys"]), c["adv_bytes"], dict(c["usage"]), c["unparsed"]))
if "--control" in sys.argv:
    planted = [json.dumps({"type": "assistant", "message": {"model": "claude-madeup-9", "content": [{"type": "server_tool_use", "name": "zz_helper"}, {"type": "made_up_block"}]}}),
               json.dumps({"type": "system", "meta": {"inner": {"model": "claude-madeup-9"}}})]
    show("CONTROL planted", count_lines(planted, "\n".join(planted).encode())); sys.exit(0)
tot = collections.Counter(); nfiles = 0; asst_total = collections.Counter(); blocks_total = collections.Counter(); stu_total = 0; anym = collections.Counter(); advb = 0
for root in [a for a in sys.argv[1:] if not a.startswith("--")]:
    for dp, ds, fs in sorted(os.walk(root)):
        for f in sorted(fs):
            p = os.path.join(dp, f); raw = open(p, "rb").read(); nfiles += 1
            c = count_lines(raw.decode("utf-8", "replace").split("\n"), raw)
            label = os.path.basename(dp).replace("-cwd", "").split("-")[-1] if "transcripts" in dp else os.path.relpath(p, root)
            label = os.path.basename(dp)[len("-private-tmp-m2-") + 7:] if os.path.basename(dp).startswith("-private-tmp-m2-") else label
            show("%-14s depth %d" % (label, os.path.relpath(p, root).count(os.sep)), c)
            asst_total.update(c["asst_model"]); blocks_total.update(c["block"]); stu_total += sum(c["stu"].values()); anym.update(c["any_model"]); advb += c["adv_bytes"]
print("TOTAL files %d | assistant messages per model %s | block types %s | server_tool_use %d | model values at any depth %s | 'advisor' bytes %d" % (
    nfiles, dict(asst_total), dict(blocks_total), stu_total, dict(anym), advb))
