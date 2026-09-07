#!/bin/bash
# decision_queue.sh — Wednesday's decision queue CLI (WED-113 round 3).
# Maintains 0_Brain/dashboard/data/decisions.json — the "requires action from
# Kam" source the cockpit's NEEDS-YOU section renders. Wednesday writes here;
# Kam's cockpit buttons only ever send chat messages (his click is a message
# to Wednesday, never a state write — Wednesday rules the file on processing).
#
# Usage:
#   decision_queue.sh add --id ID --client-project "Client/Project" \
#       --title "..." --bluf "..." \
#       --option key:label[:detail]   (repeat, >=2) \
#       --recommended KEY --default-action "..."
#   decision_queue.sh add --json      # one JSON object on stdin (same fields:
#                                     # id, client_project, title, bluf,
#                                     # options[{key,label,detail?}],
#                                     # recommended, default_action)
#   decision_queue.sh rule ID CHOICE_KEY
#   decision_queue.sh --delivered ID ARTEFACT   # mark a RULED card delivered: the
#                                     # ruling now sits in ARTEFACT (ticket comment,
#                                     # PR, row). Refuses unless the card is ruled.
#   decision_queue.sh list [open|ruled|all]
#   decision_queue.sh list ruled --undelivered [ID-PREFIX]
#                                     # ruled cards with no delivered mark, optionally
#                                     # only ids starting with e.g. nexusai- / secuura-
#   decision_queue.sh show ID         # ONE card whole: every option with its KEY,
#                                     # label and detail, the ruling (choice + note +
#                                     # ts), delivered_artefact/ts. Copy a letter
#                                     # FROM HERE, never from the question's wording
#                                     # (2026-09-06 ledger w=107). Unknown id: exit 2.
#
# DELIVERED (2026-09-06, ledger w=3 promotion of learnings/2026-09-05_a-relayed-
# ruling-is-delivered-only-when-it-is-in-the-artefact.md rule 4): a RULED card is
# not closed until the ruling sits in the artefact the next reader lands on. The
# mysql2 EXTEND ruling of 09-04 was relayed, absorbed into a queue, pre-empted,
# and re-raised as "unanswered" by s133 — nobody owned DELIVERY as a field. Now it
# is one: `delivered_artefact` + `delivered_ts` on the card, and fleet/send_brief.sh
# refuses a --kind brief while `list ruled --undelivered <prefix>` is non-empty for
# that project and the body lacks the RULED BY KAM, NOT YET IN AN ARTEFACT section.
#
# Guarantees: the file stays valid JSON (atomic tmp+rename write); malformed
# input or an unreadable existing file FAILS LOUDLY (exit 2) and never
# clobbers what is on disk.
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export DQ_FILE="${DQ_FILE:-$DIR/../../0_Brain/dashboard/data/decisions.json}"
export DQ_CHAT="${DQ_CHAT:-$DIR/../../0_Brain/dashboard/data/chat_log.json}"
# The python below is delivered on stdin (heredoc), so a `--json` payload
# cannot also ride stdin — capture it into DQ_JSON first.
DQ_JSON=""
for a in "$@"; do
  if [ "$a" = "--json" ]; then DQ_JSON="$(cat)"; break; fi
done
export DQ_JSON
exec python3 - "$@" <<'PYEOF'
import datetime, json, os, sys, tempfile

FILE = os.environ["DQ_FILE"]

def die(msg, code=2):
    print(f"decision_queue: ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def now():
    return datetime.datetime.now().astimezone().isoformat()

def load():
    if not os.path.exists(FILE):
        return []
    try:
        data = json.loads(open(FILE).read())
    except Exception as e:
        die(f"{FILE} is not valid JSON ({e}) — refusing to touch it. Fix it by hand.")
    if not isinstance(data, list):
        die(f"{FILE} is not a JSON list — refusing to touch it.")
    return data

def save(data):
    # atomic: write a sibling tmp file, validate by re-parsing, then rename
    d = os.path.dirname(os.path.abspath(FILE))
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".decisions-", suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
        json.loads(open(tmp).read())          # paranoia: never install unparseable bytes
        os.replace(tmp, FILE)
    except BaseException:
        try: os.unlink(tmp)
        except OSError: pass
        raise

def validate(d, existing_ids):
    if not isinstance(d, dict):
        die("decision must be a JSON object")
    dec = {}
    for k in ("id", "client_project", "title", "bluf", "default_action"):
        v = d.get(k)
        if not isinstance(v, str) or not v.strip():
            die(f"missing/empty required field: {k}")
        dec[k] = v.strip()
    if dec["id"] in existing_ids:
        die(f"id already exists: {dec['id']}")
    opts = d.get("options")
    if not isinstance(opts, list) or len(opts) < 2:
        die("options must be a list of at least 2 {key,label[,detail]} objects")
    seen, out = set(), []
    for o in opts:
        if not isinstance(o, dict) or not str(o.get("key", "")).strip() \
           or not str(o.get("label", "")).strip():
            die("every option needs a non-empty key and label")
        k = str(o["key"]).strip()
        if k in seen:
            die(f"duplicate option key: {k}")
        seen.add(k)
        out.append({"key": k, "label": str(o["label"]).strip(),
                    "detail": str(o.get("detail", "")).strip()})
    dec["options"] = out
    rec = str(d.get("recommended", "")).strip()
    if rec not in seen:
        die(f"recommended must be one of the option keys ({', '.join(sorted(seen))})")
    dec["recommended"] = rec
    dec["ts"] = str(d.get("ts", "")).strip() or now()
    dec["status"] = "open"
    dec["ruled_choice"] = None
    dec["ruled_ts"] = None
    return dec

STOPWORDS = {"about","after","again","before","between","could","should","would","their","there","these","those","which","while","wednesday","secuura","datasec","nexusai","blockchain","kam","agent","ticket","tickets","decision","recommended","default","nothing","moves","today","tomorrow","reported","expires","money","only"}

def prior_rulings(d):
    """Kam's panel messages whose text shares >=2 subject words with the card's id+title."""
    import re
    chat = os.environ.get("DQ_CHAT", "")
    if not chat or not os.path.exists(chat):
        return []
    try:
        c = json.load(open(chat))
    except Exception as e:
        die(f"chat log unreadable ({e}) — refusing to add a card without the prior-ruling check")
    msgs = c if isinstance(c, list) else c.get("messages", c)
    subject = f"{d.get('id','')} {d.get('title','')}".lower().replace("-", " ")
    words = {w for w in re.findall(r"[a-z]{5,}", subject) if w not in STOPWORDS}
    if not words:
        return []
    hits = []
    for m in msgs:
        if m.get("role") != "kam":
            continue
        text = str(m.get("text", ""))
        low = text.lower()
        shared = {w for w in words if w in low}
        if len(shared) >= 2:
            hits.append((str(m.get("ts", ""))[:16].replace("T", " "), " ".join(text.split())))
    return hits

def cmd_add(args):
    if args == ["--json"]:
        try:
            d = json.loads(os.environ.get("DQ_JSON", ""))
        except Exception as e:
            die(f"stdin is not valid JSON ({e})")
    else:
        d = {"options": []}
        flag_map = {"--id": "id", "--client-project": "client_project",
                    "--title": "title", "--bluf": "bluf",
                    "--recommended": "recommended", "--default-action": "default_action"}
        i = 0
        while i < len(args):
            a = args[i]
            if a == "--option":
                if i + 1 >= len(args): die("--option needs key:label[:detail]")
                parts = args[i + 1].split(":", 2)
                if len(parts) < 2: die(f"--option must be key:label[:detail], got {args[i+1]!r}")
                d["options"].append({"key": parts[0], "label": parts[1],
                                     "detail": parts[2] if len(parts) > 2 else ""})
                i += 2
            elif a == "--override-prior-rulings":
                d["_override_prior"] = True
                i += 1
            elif a in flag_map:
                if i + 1 >= len(args): die(f"{a} needs a value")
                d[flag_map[a]] = args[i + 1]
                i += 2
            else:
                die(f"unknown flag: {a}")
    # PRIOR-RULING GATE (2026-09-05 16:4x, ledger w=2 — the Founders Hub credit was carded a FOURTH
    # time at 16:32 after Kam's 10:51 panel note "no need to raise this again. this is in hand";
    # the seat had read the panel only for messages after its predecessor's last action). A card
    # is Wednesday's artefact; the panel holds Kam's rulings. Before any card is written, every
    # Kam message on the panel is searched for the card's subject words; a hit REFUSES the add and
    # prints his words, unless --override-prior-rulings is passed (and then the override is stated
    # in the receipt). In the path, not in memory.
    override = bool(d.pop("_override_prior", False))
    prior = prior_rulings(d)
    if prior and not override:
        print("decision_queue: REFUSED — Kam has already written on this subject on the panel "
              f"({len(prior)} message(s)). Read them; if the card is still warranted, re-run with "
              "--override-prior-rulings and say why in the BLUF:", file=sys.stderr)
        for ts, text in prior:
            print(f"  {ts} | {text[:220]}", file=sys.stderr)
        sys.exit(3)
    data = load()
    dec = validate(d, {x.get("id") for x in data if isinstance(x, dict)})
    if prior and override:
        dec["prior_rulings_overridden"] = [ts for ts, _ in prior]
    data.append(dec)
    save(data)
    print(f"added: {dec['id']} ({dec['client_project']}) — {dec['title']} [rec: {dec['recommended']}]")

def cmd_rule(args):
    if len(args) != 2:
        die("usage: rule ID CHOICE_KEY")
    did, choice = args
    data = load()
    for dec in data:
        if isinstance(dec, dict) and dec.get("id") == did:
            if dec.get("status") == "ruled":
                die(f"{did} is already ruled ({dec.get('ruled_choice')} @ {dec.get('ruled_ts')})")
            keys = {o.get("key") for o in dec.get("options", []) if isinstance(o, dict)}
            if choice not in keys:
                die(f"choice {choice!r} is not an option of {did} ({', '.join(sorted(k for k in keys if k))})")
            dec["status"] = "ruled"
            dec["ruled_choice"] = choice
            dec["ruled_ts"] = now()
            save(data)
            print(f"ruled: {did} -> {choice}")
            return
    die(f"no decision with id {did!r}")

def is_delivered(dec):
    return bool(str(dec.get("delivered_artefact") or "").strip())

def cmd_delivered(args):
    # Marks a RULED card as delivered into ARTEFACT. The timestamp is generated
    # here (now()), never typed. A card that is open/withdrawn/absent REFUSES —
    # delivery is a property of a ruling, and there is none to deliver.
    if len(args) != 2 or not args[0].strip() or not args[1].strip():
        die("usage: --delivered ID ARTEFACT   (ARTEFACT = the ticket comment / PR / row the ruling now sits in)")
    did, artefact = args[0].strip(), " ".join(args[1].split())
    data = load()
    for dec in data:
        if isinstance(dec, dict) and dec.get("id") == did:
            st = dec.get("status")
            if st != "ruled":
                die(f"{did} is not ruled (status={st!r}) — only a ruled card can be delivered")
            if is_delivered(dec):
                die(f"{did} is already delivered: {dec['delivered_artefact']} @ {dec.get('delivered_ts')}")
            dec["delivered_artefact"] = artefact
            dec["delivered_ts"] = now()
            save(data)
            print(f"delivered: {did} -> {artefact} @ {dec['delivered_ts'][:16]}")
            return
    die(f"no decision with id {did!r}")

def cmd_show(args):
    # SHOW (2026-09-06, ledger w=107): a letter was glossed from the question's word
    # order instead of the store. Print the card whole, key beside label.
    if len(args) != 1 or not args[0].strip():
        die("usage: show ID")
    did = args[0].strip()
    dec = next((d for d in load() if isinstance(d, dict) and d.get("id") == did), None)
    if dec is None:
        die(f"no decision with id {did!r}")
    print(f"id:      {dec.get('id')}")
    print(f"status:  {dec.get('status')}   ({dec.get('client_project', '?')})")
    print(f"title:   {dec.get('title', '')}")
    print(f"bluf:    {dec.get('bluf', '')}")
    print(f"options (recommended: {dec.get('recommended')}):")
    for o in dec.get("options", []):
        if isinstance(o, dict):
            print(f"  [{o.get('key')}] {o.get('label', '')}")
            if str(o.get("detail") or "").strip():
                print(f"        detail: {o['detail']}")
    print(f"default: {dec.get('default_action', '')}")
    print(f"ruling:  choice={dec.get('ruled_choice')!r}"
          + (f"  ruling={dec['ruling']!r}" if dec.get("ruling") else "")
          + f"  ruled_ts={dec.get('ruled_ts')}")
    for k in ("ruling_note", "withdrawn_at", "withdrawn_reason", "delivered_artefact", "delivered_ts"):
        if dec.get(k):
            print(f"{k}: {dec[k]}")

def cmd_list(args):
    which = args[0] if args else "all"
    if which not in ("open", "ruled", "all"):
        die("usage: list [open|ruled|all] | list ruled --undelivered [ID-PREFIX]")
    undelivered, prefix = False, ""
    rest = args[1:]
    if rest:
        if which != "ruled" or rest[0] != "--undelivered" or len(rest) > 2:
            die("usage: list [open|ruled|all] | list ruled --undelivered [ID-PREFIX]")
        undelivered = True
        prefix = rest[1] if len(rest) == 2 else ""
    data = load()
    shown = 0
    for dec in data:
        if not isinstance(dec, dict):
            print("  (skipping one malformed entry)", file=sys.stderr)
            continue
        st = dec.get("status", "?")
        if which != "all" and st != which:
            continue
        if undelivered:
            if is_delivered(dec):
                continue
            if prefix and not str(dec.get("id", "")).startswith(prefix):
                continue
        shown += 1
        line = f"[{st:5}] {dec.get('id','?')}  {dec.get('client_project','?')} — {dec.get('title','?')}"
        if st == "ruled":
            line += f"  => {dec.get('ruled_choice')} @ {str(dec.get('ruled_ts') or '')[:16]}"
            if is_delivered(dec):
                line += f"  delivered: {dec['delivered_artefact']} @ {str(dec.get('delivered_ts') or '')[:16]}"
        else:
            line += f"  (rec: {dec.get('recommended','?')}; default: {dec.get('default_action','?')})"
        print(line)
    tag = which
    if undelivered:
        tag += ", undelivered" + (f", prefix={prefix}" if prefix else "")
    print(f"{shown} decision(s) [{tag}]")

if len(sys.argv) < 2:
    die("usage: decision_queue.sh add|rule|--delivered|list|show ...", 1)
cmd, rest = sys.argv[1], sys.argv[2:]
if cmd == "add":   cmd_add(rest)
elif cmd == "rule": cmd_rule(rest)
elif cmd == "show": cmd_show(rest)
elif cmd in ("--delivered", "delivered"): cmd_delivered(rest)
elif cmd == "list": cmd_list(rest)
else: die(f"unknown command: {cmd}", 1)
PYEOF
