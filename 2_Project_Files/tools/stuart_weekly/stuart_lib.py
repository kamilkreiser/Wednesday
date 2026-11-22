#!/usr/bin/env python3
"""stuart_lib.py - deterministic helpers for stuart_weekly.sh (no network, no board access, no key).

  split  <claude_out.txt> <items.md> <layout.md> <date>   split the model's output on its markers and VALIDATE both documents
  card   <layout.md> <card_id> <file_id> <drawer_url> <items_rel_path> <pdf_rel_path>   print the decision-card JSON on stdout
  cards  <decisions.json> <stage_dir> <days> [extra_card_ids_file]   write decisions_index.tsv + cards/<id>.json-as-text for Stuart/Peter cards

Exit: 0 ok - 2 refused (stderr says exactly what failed validation). Run with python3 -I.
"""
import datetime, json, os, re, sys


def die(msg):
    sys.stderr.write("stuart_lib: REFUSED: %s\n" % msg)
    sys.exit(2)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def split(out_path, items_path, layout_path, date):
    t = read(out_path)
    m = re.search(r"<<<ITEMS_MD>>>\n(.*?)\n<<<LAYOUT_MD>>>\n(.*?)\n<<<END>>>", t, re.S)
    if not m:
        die("model output lacks the three marker lines <<<ITEMS_MD>>> / <<<LAYOUT_MD>>> / <<<END>>> (%d bytes read)" % len(t))
    items, layout = m.group(1).strip() + "\n", m.group(2).strip() + "\n"
    errs = []
    # items.md shape
    for need in (r"^# Items for Kam's meeting with Stuart", r"\*\*BLUF:\*\*", r"\*\*How measured\.\*\*", r"^## A\. ", r"^## B\. ", r"^## C\. ", r"^## D\. ", r"^## Not verified / limits"):
        if not re.search(need, items, re.M):
            errs.append("items.md lacks %s" % need)
    # layout shape
    if not re.search(r"^# Secuura: items for the meeting with Stuart, ", layout, re.M):
        errs.append("layout lacks its '# Secuura: items for the meeting with Stuart, ...' title")
    if not re.search(r"^## BLUF\s*$", layout, re.M):
        errs.append("layout lacks '## BLUF'")
    secs = re.findall(r"^## (.+)$", layout, re.M)
    if not secs or not secs[-1].lower().startswith("sources and limits"):
        errs.append("layout's LAST '## ' section is not 'Sources and limits' (got %r)" % (secs[-1] if secs else None))
    n_layout = [int(x) for x in re.findall(r"^### (\d+)\. ", layout, re.M)]
    n_items = [int(x) for x in re.findall(r"^(\d+)\. \*\*", items, re.M)]
    if not n_layout:
        errs.append("layout has no '### N. ' items")
    elif n_layout != list(range(1, len(n_layout) + 1)):
        errs.append("layout item numbers are not 1..N in order: %r" % n_layout)
    if n_items and n_layout and len(n_items) != len(n_layout):
        errs.append("items.md has %d numbered items but layout has %d" % (len(n_items), len(n_layout)))
    bluf = re.search(r"^## BLUF\s*\n(.*?)(?=^## )", layout, re.M | re.S)
    top3 = re.findall(r"^([123])\. (.+)$", bluf.group(1) if bluf else "", re.M)
    if [a for a, _ in top3] != ["1", "2", "3"]:
        errs.append("layout BLUF must carry exactly three numbered lines 1. 2. 3. (found %r)" % [a for a, _ in top3])
    if not re.search(r"Not verified|not checked|limits", layout, re.I):
        errs.append("layout states no limits")
    # nothing the model must not have: a key-shaped token or a Linear key
    for name, doc in (("items.md", items), ("layout", layout)):
        if re.search(r"lin_api_[A-Za-z0-9]{10,}|sk-ant-[A-Za-z0-9_-]{10,}", doc):
            errs.append("%s contains a key-shaped token" % name)
    if errs:
        die("; ".join(errs))
    with open(items_path, "w", encoding="utf-8") as f:
        f.write(items)
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout)
    print("split ok: %d items, %d bytes items.md, %d bytes layout" % (len(n_layout), len(items), len(layout)))


def parse_layout(layout):
    n = len(re.findall(r"^### \d+\. ", layout, re.M))
    bluf = re.search(r"^## BLUF\s*\n(.*?)(?=^## )", layout, re.M | re.S).group(1)
    top3 = [re.sub(r"\*\*", "", l).strip() for l in re.findall(r"^[123]\. .+$", bluf, re.M)]
    settled = [re.sub(r"\*\*", "", l).strip() for l in re.findall(r"^Settled.*$", bluf, re.M)]
    return n, top3, settled


def card(layout_path, card_id, file_id, drawer, items_rel, pdf_rel):
    n, top3, settled = parse_layout(read(layout_path))
    if len(top3) != 3:
        die("cannot build the card: BLUF top three not found")
    bluf = ("Raise these with Stuart in your Monday meeting. Download: file %s in the live board file drawer (%s), also in the repo at %s. "
            "THE THREE THAT MOST NEED HIM: %s %s %s "
            "%sFull list with every source: %s. Not checked: anything already raised by WhatsApp, email or in person; items marked 'not checked' in the PDF."
            % (file_id, drawer, pdf_rel, top3[0], top3[1], top3[2], (settled[0] + " ") if settled else "", items_rel))
    c = {
        "id": card_id,
        "client_project": "Secuura/Blockchain",
        "title": "For this week's meeting with Stuart: %d items, three that most need him" % n,
        "bluf": bluf,
        "options": [
            {"key": "a", "label": "Raise as listed", "detail": "Use the list (and the file) as this week's agenda; tell Wednesday his answers afterwards and she routes them to tickets and seats."},
            {"key": "b", "label": "Change the list", "detail": "Add a note with what to add, drop or reword; Wednesday updates the file before the meeting."},
        ],
        "recommended": "a",
        "default_action": "If no answer: option a; the list stays as written and Wednesday routes whatever Stuart answers once you tell her.",
    }
    print(json.dumps(c, ensure_ascii=False))


def cards(decisions, stage, days, extra_file):
    d = json.load(open(decisions, encoding="utf-8"))
    cut = (datetime.datetime.now().astimezone() - datetime.timedelta(days=int(days))).isoformat()
    extra = set()
    if extra_file and os.path.isfile(extra_file):
        extra = set(l.strip() for l in open(extra_file, encoding="utf-8") if l.strip())
    os.makedirs(os.path.join(stage, "cards"), exist_ok=True)
    rows, n = [], 0
    for c in d:
        if not str(c.get("client_project", "")).lower().startswith("secuura"):
            continue
        blob = json.dumps(c, ensure_ascii=False).lower()
        if "stuart" not in blob and "peter" not in blob and c.get("id") not in extra:
            continue
        rows.append("\t".join([c.get("id", ""), c.get("status", ""), str(c.get("ts", ""))[:16], str(c.get("ruled_ts") or "")[:16], c.get("ruled_choice") or "", (c.get("title") or "").replace("\t", " ")]))
        if str(c.get("ts", "")) >= cut or c.get("id") in extra:
            opts = "\n".join("  [%s] %s: %s" % (o.get("key"), o.get("label"), o.get("detail", "")) for o in c.get("options", []))
            txt = "id: %s\nstatus: %s (%s)\ncreated: %s\nruled: choice=%s at %s\ntitle: %s\nbluf: %s\noptions:\n%s\ndefault: %s\n" % (
                c.get("id"), c.get("status"), c.get("client_project"), c.get("ts"), c.get("ruled_choice"), c.get("ruled_ts"), c.get("title"), c.get("bluf"), opts, c.get("default_action"))
            with open(os.path.join(stage, "cards", c["id"] + ".txt"), "w", encoding="utf-8") as f:
                f.write(txt)
            n += 1
    with open(os.path.join(stage, "decisions_index.tsv"), "w", encoding="utf-8") as f:
        f.write("id\tstatus\tcreated\truled\tchoice\ttitle\n" + "\n".join(rows) + "\n")
    print("cards: %d Secuura cards mention Stuart or Peter, %d staged in full (last %s days + cited)" % (len(rows), n, days))


if __name__ == "__main__":
    a = sys.argv[1:]
    try:
        if a and a[0] == "split" and len(a) == 5:
            split(a[1], a[2], a[3], a[4])
        elif a and a[0] == "card" and len(a) == 7:
            card(*a[1:])
        elif a and a[0] == "cards" and len(a) in (4, 5):
            cards(a[1], a[2], a[3], a[4] if len(a) == 5 else None)
        else:
            sys.exit(__doc__)
    except (OSError, ValueError, KeyError) as e:
        die("%s: %s" % (type(e).__name__, e))
