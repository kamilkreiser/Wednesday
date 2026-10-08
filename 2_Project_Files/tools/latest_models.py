#!/usr/bin/env python3
"""latest_models.py -- newest Claude model ID per level from a LIVE source.

Sources, in order: (a) Anthropic Models API if ANTHROPIC_API_KEY is set (env or
4_Credentials/.env, value never printed); (b) the public docs models-overview page
(markdown rendition, 'Claude API ID' row of the comparison table).
Exit: 0 ok | 3 no live source readable / required level missing (previous JSON kept)
      4 sanity guard refused the data (malformed id), previous JSON kept.
Env overrides (tests): LM_MODELS_URL, LM_API_URL, LM_OUT, LM_PIN_GLOBS (colon list),
LM_NO_API=1 (skip path a).
"""
import glob, json, os, re, subprocess, sys, tempfile, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.environ.get("LM_OUT") or os.path.join(PROJECT, "0_Brain/dashboard/data/models_latest.json")
PAGE_URL = os.environ.get("LM_MODELS_URL") or "https://platform.claude.com/docs/en/models/overview.md"
API_URL = os.environ.get("LM_API_URL") or "https://api.anthropic.com/v1/models"
ID_RE = re.compile(r"^claude-(opus|sonnet|haiku|fable)-")
LEVELS = ("opus", "sonnet", "haiku", "fable")
REQUIRED = ("opus", "sonnet")
DEFAULT_GLOBS = ["/Volumes/DevMASTER/!CODING/*/*/Launch_Claude.command",
                 "/Volumes/DevMASTER/WEDNESDAY/Launch_*.command"]


class Fail(Exception):
    def __init__(self, rc, msg):
        Exception.__init__(self, msg)
        self.rc, self.msg = rc, msg


def version(mid):
    """claude-opus-5-5 -> (5,5); claude-opus-4-8 -> (4,8); dated suffix (8 digits) ignored."""
    m = re.match(r"^claude-[a-z]+-((?:\d+-?)+)", mid)
    nums = [int(x) for x in m.group(1).strip("-").split("-") if len(x) < 8] if m else []
    return tuple(nums)


def level_of(mid):
    m = ID_RE.match(mid)
    return m.group(1) if m else None


def curl(args):
    p = subprocess.run(["curl", "-sSL", "-m", "30", "--fail"] + args,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise Fail(3, "fetch failed (curl rc=%d): %s" % (p.returncode, p.stderr.strip()))
    return p.stdout


def api_key():
    k = os.environ.get("ANTHROPIC_API_KEY")
    if k:
        return k
    envf = os.path.join(PROJECT, "4_Credentials/.env")
    try:
        for line in open(envf):
            m = re.match(r"^\s*(?:export\s+)?ANTHROPIC_API_KEY\s*=\s*(.*)$", line.rstrip("\n"))
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
    except OSError:
        pass
    return None


def from_api(key):
    items, after = [], None
    for _ in range(50):
        url = API_URL + "?limit=1000" + ("&after_id=" + after if after else "")
        d = json.loads(curl(["-H", "x-api-key: " + key, "-H", "anthropic-version: 2023-06-01", url]))
        items += d.get("data", [])
        if not d.get("has_more"):
            break
        after = d.get("last_id")
    return [{"id": i.get("id", ""), "display_name": i.get("display_name"), "released": i.get("created_at"),
             "retirement": None} for i in items], {"kind": "anthropic-models-api", "url": API_URL,
                                                  "how": "GET /v1/models paginated (limit=1000, after_id), header x-api-key from env/.env (value not logged), anthropic-version 2023-06-01"}


def from_page():
    text = curl([PAGE_URL])
    lines = text.splitlines()
    hdr = idr = ret = None
    for ln in lines:
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if cells[0] == "Feature":
            hdr = cells
        elif cells[0].startswith("Claude API ID") and hdr and idr is None:
            idr = cells
        elif cells[0].startswith("[Retirement]") or cells[0] == "Retirement":
            ret = cells
    if not hdr or not idr or len(idr) != len(hdr):
        raise Fail(3, "docs page readable but no 'Claude API ID' comparison table found (page format changed?) at " + PAGE_URL)
    out = []
    for n, (name, cell) in enumerate(zip(hdr, idr)):
        if n == 0:
            continue
        m = re.search(r"`([^`]+)`", cell)
        out.append({"id": m.group(1) if m else cell, "display_name": name,
                    "released": None, "retirement": (ret[n] if ret and len(ret) == len(hdr) else None)})
    return out, {"kind": "docs-models-overview-page", "url": PAGE_URL,
                 "how": "curl the markdown rendition; parse the 'Claude API ID' row of the 'Compare models' table (no API key needed; release date not on page, retirement floor recorded instead)"}


def pick(entries):
    best = {}
    for e in entries:
        mid = e["id"]
        if not ID_RE.match(mid):
            raise Fail(4, "REFUSED malformed model id %r (must match ^claude-(opus|sonnet|haiku|fable)-)" % mid)
        lv = level_of(mid)
        if not version(mid):
            raise Fail(4, "REFUSED model id %r has no parseable version" % mid)
        cur = best.get(lv)
        key = (version(mid), e.get("released") or "")
        if cur is None or key > (version(cur["id"]), cur.get("released") or ""):
            best[lv] = e
    for lv in REQUIRED:
        if lv not in best:
            raise Fail(3, "required level '%s' not found in source data -- refusing to publish" % lv)
    return best


def scan_pins(latest):
    globs = os.environ.get("LM_PIN_GLOBS")
    globs = globs.split(":") if globs else DEFAULT_GLOBS
    files = sorted(set(f for g in globs for f in glob.glob(g)))
    pins, stale = [], []
    for f in files:
        found = []
        for ln in open(f, errors="replace"):
            if ln.lstrip().startswith("#"):
                continue
            for m in re.finditer(r"--model[ =]+[\"']?([^\s\"']+)", ln):
                found.append(("--model", m.group(1)))
            for m in re.finditer(r"ANTHROPIC_DEFAULT_(?:OPUS|SONNET|HAIKU|FABLE)_MODEL=[\"']?([^\s\"']+)", ln):
                found.append(("env-default", m.group(1)))
        rel = f.replace("/Volumes/DevMASTER/", "")
        if not found:
            pins.append({"launcher": rel, "kind": "none", "pin": None, "status": "inherits (no pin)"})
        for kind, raw in found:
            pin = re.sub(r"\[[^\]]*\]$", "", raw)
            lv = level_of(pin)
            if lv is None and pin in LEVELS:
                pins.append({"launcher": rel, "kind": kind, "pin": raw, "level": pin,
                             "status": "alias (tracks newest GA; can lag a new release)"})
            elif lv is None:
                pins.append({"launcher": rel, "kind": kind, "pin": raw, "level": None, "status": "unrecognised"})
            else:
                nl = latest.get(lv, {}).get("model_id")
                if nl and version(pin) < version(nl):
                    rec = {"launcher": rel, "kind": kind, "pin": raw, "level": lv, "newest": nl, "status": "STALE"}
                    pins.append(rec)
                    stale.append(rec)
                else:
                    pins.append({"launcher": rel, "kind": kind, "pin": raw, "level": lv, "status": "current"})
    return pins, stale


def previous():
    try:
        return json.load(open(OUT)), os.path.getmtime(OUT)
    except (OSError, ValueError):
        return None, None


def main():
    prev, pmtime = previous()
    try:
        src = None
        key = None if os.environ.get("LM_NO_API") else api_key()
        entries = meta = None
        if key:
            try:
                entries, meta = from_api(key)
            except Fail as e:
                print("latest_models: API path failed (%s) -- trying docs page" % e.msg, file=sys.stderr)
        if entries is None:
            entries, meta = from_page()
        best = pick(entries)
    except Fail as e:
        age = ""
        if pmtime:
            age = " Previous %s KEPT (age %.1f h)." % (os.path.relpath(OUT, PROJECT), (datetime.datetime.now().timestamp() - pmtime) / 3600)
        else:
            age = " No previous JSON exists."
        print("latest_models: FAIL rc=%d: %s.%s" % (e.rc, e.msg, age), file=sys.stderr)
        return e.rc
    levels = {lv: {"model_id": e["id"], "display_name": e.get("display_name"),
                   "released": e.get("released"), "retirement_not_before": e.get("retirement")}
              for lv, e in best.items()}
    warns = []
    for lv, d in levels.items():
        p = ((prev or {}).get("levels") or {}).get(lv, {}).get("model_id")
        if p and version(d["model_id"]) < version(p):
            warns.append("REGRESSION %s: source now says %s, older than previous %s (source problem, not a downgrade)" % (lv, d["model_id"], p))
    pins, stale = scan_pins(levels)
    now = datetime.datetime.now().astimezone()
    doc = {"checked_at_local": now.strftime("%Y-%m-%d %H:%M:%S %z"),
           "checked_at_utc": now.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "source": meta, "levels": levels,
           "previous": {lv: v.get("model_id") for lv, v in ((prev or {}).get("levels") or {}).items()},
           "warnings": warns, "pins": pins, "stale_pins": stale}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(OUT), prefix=".models_latest.")
    with os.fdopen(fd, "w") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, OUT)
    parts = " ".join("%s=%s" % (lv, levels[lv]["model_id"]) for lv in LEVELS if lv in levels)
    seen, names = set(), []
    for s_ in stale:
        nm = s_["launcher"].split("/")[-2] if "!CODING" in s_["launcher"] else os.path.basename(s_["launcher"])
        if (nm, s_["pin"]) not in seen:
            seen.add((nm, s_["pin"]))
            names.append("%s=%s" % (nm, s_["pin"]))
    sp = ", ".join(names)
    print("latest_models: %s via %s | stale pins: %d%s" % (parts, meta["kind"], len(stale), (" (" + sp + ")") if sp else ""))
    for w in warns:
        print("latest_models: WARN " + w, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
