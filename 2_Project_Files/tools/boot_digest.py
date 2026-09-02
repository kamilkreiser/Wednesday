#!/usr/bin/env python3
"""boot_digest.py — generate (and check) the boot-time DIGEST of Wednesday's lessons.

WHY (Kam, 2026-09-02 20:44, panel): "the boot script is the main culprit. How can we take the
learnings, bottle them up, make sure we don't lose anything, but cut down the actual context?"
Measured that night: the brain load cost 34% of the window (lessons 336 KB + live ledger).

WHAT: a two-tier load. The lesson FILES stay the source of truth, untouched. This script writes
`0_Brain/learnings/_boot_digest.md` FROM them — per lesson: the H1 headline (the retrieval handle,
per the 2026-08-13 rule), frontmatter (date/type/status/supersedes), the operative paragraph, an
index of the file's section headings (so a seat knows what to open), and every RULES section
verbatim (headings/bold leads matching the shapes below). Files with no rules-shaped section are
included WHOLE (grants, contemplations). Nothing is hand-edited here — regenerate at every wrap
and consolidation; `--check` proves every headline and every rule line is present in the digest.

Losing nothing: what leaves the boot is case EVIDENCE (the incidents behind a rule), read on demand
when a lesson fires or a diagnosis needs it — the same pattern as _ledger_archive.md.

Usage:
  boot_digest.py            write the digest, print sizes
  boot_digest.py --check    verify the digest against the files (exit 1 on any miss / staleness)
Never discards stderr. Never deletes anything. Paths derive from this file's location.
"""
import os, re, sys, glob, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
LEARN = os.path.join(PROJECT, "0_Brain", "learnings")
OUT = os.path.join(LEARN, "_boot_digest.md")

# Section leads that carry RULES (kept verbatim). Matched at line start, case-insensitive.
RULE_LEADS = re.compile(
    r"^(#{2,4}\s+.*(how to apply|how to handle|the rule\b|rules? for my hands|how to read|when to read|"
    r"escalation triggers|what i will now decide|what still stops|the scope, exactly|"
    r"the operating pattern|the escalation ladder|what has held|the concrete remedy).*"
    r"|\*\*(how to apply|how to handle|the rule\b|the rules?\b|rules? for my hands|the grant\b|"
    r"the two hard requirements|escalation triggers|the class, stated|the rule, [^*]*|"
    r"the rule as he actually set it|distilled)[^\n]*\*\*.*)$",
    re.I,
)
# Status-bearing headings (amendments, enforcement, supersession) are kept as ONE LINE each plus
# their first paragraph — a seat must know a rule was amended without carrying the whole section.
STATUS_HEADS = re.compile(r"^#{2,4}\s+(AMENDED|ENFORCED|REFINED|CORRECTED|SUPERSEDED|Extension|EXTENSION|Widened|Sharpened)", re.I)
STOP_AT = re.compile(r"^(#{1,4}\s+|\*\*(related|context|why|what triggered|what happened|meta-note|the honest|the case|the failure|the catch|why this)[^\n]*\*\*)", re.I)
BOLD_LEAD = re.compile(r"^\*\*[^*]+\*\*")


def parse(path):
    text = open(path, encoding="utf-8").read()
    fm = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"')
            body = text[end + 4:]
    lines = body.split("\n")
    h1 = next((l for l in lines if l.startswith("# ")), None)
    headings = [l.strip() for l in lines if re.match(r"^#{2,4}\s+", l)]
    # operative paragraph: first non-empty paragraph after the H1
    op = ""
    if h1:
        i = lines.index(h1) + 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        para = []
        while i < len(lines) and lines[i].strip():
            para.append(lines[i]); i += 1
        op = "\n".join(para)
    # rules sections: from a RULE_LEAD line to the next heading / non-rule bold lead
    rules = []
    i = 0
    while i < len(lines):
        if RULE_LEADS.match(lines[i]):
            j = i + 1
            while j < len(lines):
                l = lines[j]
                if re.match(r"^#{1,4}\s+", l) or (BOLD_LEAD.match(l) and STOP_AT.match(l)):
                    break
                j += 1
            blk = "\n".join(lines[i:j]).rstrip()
            if blk and blk != op and blk not in rules:
                rules.append(blk)
            i = j
        elif STATUS_HEADS.match(lines[i]):
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            k = j
            while k < len(lines) and lines[k].strip() and not re.match(r"^#{1,4}\s+", lines[k]):
                k += 1
            blk = "\n".join([lines[i]] + lines[j:k]).rstrip()
            if blk not in rules:
                rules.append(blk)
            i = k
        else:
            i += 1
    return fm, h1, op, headings, rules, text


def build():
    files = sorted(glob.glob(os.path.join(LEARN, "2026-*.md")))
    parts = []
    stats = {"files": 0, "whole": 0, "src_bytes": 0, "whole_names": []}
    for f in files:
        fm, h1, op, headings, rules, text = parse(f)
        name = os.path.basename(f)
        stats["files"] += 1; stats["src_bytes"] += len(text.encode())
        head = (h1 or "# " + name).replace("# ", "## ", 1)
        meta = f"`{name}` · {fm.get('type','?')} · {fm.get('date','?')} · status: {fm.get('status','?')}"
        if fm.get("supersedes"):
            meta += f" · supersedes: {fm['supersedes']}"
        block = [head, meta, ""]
        if rules:
            if op:
                block += [op, ""]
            if headings:
                block += ["sections (open the file for these): " + " · ".join(h.lstrip('#').strip() for h in headings), ""]
            block += ["\n\n".join(rules), ""]
        else:
            stats["whole"] += 1; stats["whole_names"].append(name)
            block += ["(no rules-shaped section — file included WHOLE)", "", text.split("\n---", 2)[-1].strip() if text.startswith("---") else text.strip(), ""]
        parts.append("\n".join(block))
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    header = (
        "---\n"
        f"date: {now[:10]}\n"
        "type: digest\n"
        "source: GENERATED by 2_Project_Files/tools/boot_digest.py — never hand-edit; the lesson files are the source of truth\n"
        "status: live\n"
        "---\n\n"
        "# Boot digest — headline + rules of every lesson (open the file when it fires)\n\n"
        f"Generated {now} from {stats['files']} lesson files ({stats['src_bytes']:,} B). Each block = the lesson's retrieval "
        "handle (H1), its frontmatter, the operative paragraph, its section index, and every RULES section verbatim. "
        f"{stats['whole']} files carry no rules-shaped section and are included whole. The CASES behind a rule live only "
        "in the file: open it the moment the rule fires, or when a diagnosis needs the evidence. `_ledger.md` is read whole "
        "beside this digest; `_ledger_archive.md` on demand.\n\n"
    )
    out = header + "\n\n".join(parts) + "\n"
    tmp = OUT + ".tmp"
    open(tmp, "w", encoding="utf-8").write(out)
    os.replace(tmp, OUT)
    dig = len(out.encode())
    print(f"digest written: {OUT}")
    print(f"  {stats['files']} files, source {stats['src_bytes']:,} B -> digest {dig:,} B ({100*dig//stats['src_bytes']}%); {stats['whole']} included whole: {' '.join(stats['whole_names'])}")
    return 0


def check():
    if not os.path.exists(OUT):
        print("CHECK FAIL: no digest at", OUT, file=sys.stderr); return 1
    digest = open(OUT, encoding="utf-8").read()
    dmtime = os.path.getmtime(OUT)
    files = sorted(glob.glob(os.path.join(LEARN, "2026-*.md")))
    misses = 0; stale = []
    for f in files:
        fm, h1, op, headings, rules, text = parse(f)
        name = os.path.basename(f)
        if os.path.getmtime(f) > dmtime:
            stale.append(name)
        if h1 and h1[2:].strip() not in digest:
            print(f"MISS headline: {name}: {h1}", file=sys.stderr); misses += 1
        if f"`{name}`" not in digest:
            print(f"MISS file ref: {name}", file=sys.stderr); misses += 1
        for r in rules:
            for line in r.split("\n"):
                if line.strip() and line not in digest:
                    print(f"MISS rule line: {name}: {line[:80]}", file=sys.stderr); misses += 1
                    break
    if stale:
        print(f"CHECK FAIL: digest older than {len(stale)} lesson file(s): {' '.join(stale)} — regenerate", file=sys.stderr)
    print(f"check: {len(files)} files, {misses} misses, {len(stale)} stale")
    return 1 if (misses or stale) else 0


if __name__ == "__main__":
    sys.exit(check() if "--check" in sys.argv else build())
