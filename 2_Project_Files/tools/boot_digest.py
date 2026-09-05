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

BY TIER (WED-145 Phase 0, 2026-09-05): each lesson carries `tier:` in its frontmatter — W (Wednesday:
Kam, the coordination method, the boundaries, her own failure modes), M (fleet method, client-neutral),
P-<Client>/<Project> (that project's cases), MIXED (a W/M lesson whose body carries project CASE
sections, each marked in the file by `<!-- tier: P-<Client>/<Project> -->` on the line above its
heading). `--by-tier` writes a SECOND digest beside the first: W as today; M without the section index;
every P file and every P section inside a MIXED file reduced to ONE line — the heading plus the path to
read it at. A file with no `tier:` falls back to today's behaviour and is named UNTAGGED at the top.
The default output is unchanged by any of this, byte for byte.

Usage:
  boot_digest.py            write the digest, print sizes
  boot_digest.py --check    verify the digest against the files (exit 1 on any miss / staleness)
  boot_digest.py --by-tier  write _boot_digest_by_tier.md as well, print both sizes
Never discards stderr. Never deletes anything. Paths derive from this file's location.
"""
import os, re, sys, glob, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
LEARN = os.path.join(PROJECT, "0_Brain", "learnings")
OUT = os.path.join(LEARN, "_boot_digest.md")
OUT_BY_TIER = os.path.join(LEARN, "_boot_digest_by_tier.md")
# a project CASE section inside a W/M lesson: this comment sits on the line ABOVE its heading
P_MARK = re.compile(r"^<!--\s*tier:\s*(P-\S+)\s*-->\s*$")

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
    return parse_text(open(path, encoding="utf-8").read())


def parse_text(text):
    # the `<!-- tier: P-… -->` markers are metadata about a section, never content: they are stripped
    # here so no digest — default or by-tier — ever carries one.
    if "<!-- tier: P-" in text:
        text = "\n".join(l for l in text.split("\n") if not P_MARK.match(l))
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


def split_p_sections(text):
    """Lift every marked project CASE section out of a lesson.

    Returns (remainder_text, [(project, heading, bytes)]). A section runs from its marked heading to
    the next heading of any level, so a marked sub-section ends its parent. Nothing is edited: the
    remainder is the file with those spans removed, and the file itself is never written to."""
    lines = text.split("\n")
    heads = [i for i, l in enumerate(lines) if re.match(r"^#{1,6}\s", l)]
    drop, found = set(), []
    for n, i in enumerate(heads):
        if i == 0:
            continue
        m = P_MARK.match(lines[i - 1])
        if not m:
            continue
        end = heads[n + 1] if n + 1 < len(heads) else len(lines)
        found.append((m.group(1), lines[i].lstrip("#").strip(),
                      len("\n".join(lines[i:end]).encode())))
        drop.update(range(i - 1, end))
    if not drop:
        return text, []
    return "\n".join(l for k, l in enumerate(lines) if k not in drop), found


def tier_block(f, rel):
    """One lesson, rendered for its tier. Returns (tier, block, p_lines)."""
    text = open(f, encoding="utf-8").read()
    name = os.path.basename(f)
    body, psecs = split_p_sections(text)
    fm, h1, op, headings, rules, _ = parse_text(body)
    tier = fm.get("tier", "").strip() or None
    head = (h1 or "# " + name).replace("# ", "## ", 1)
    meta = f"`{name}` · {fm.get('type','?')} · {fm.get('date','?')} · status: {fm.get('status','?')} · tier: {tier or 'UNTAGGED'}"
    if fm.get("supersedes"):
        meta += f" · supersedes: {fm['supersedes']}"
    p_lines = [f"- **{proj}** · {h} — cases in the file: `{rel}`" for proj, h, _ in psecs]

    # a P file is a handle and nothing else
    if tier and tier.startswith("P-"):
        return tier, f"- **{tier}** · {(h1 or name)[2:] if h1 else name} — cases in the file: `{rel}`", []

    block = [head, meta, ""]
    if rules:
        if op:
            block += [op, ""]
        # the section index is a W affordance ("open the file for these"); M is rules-only
        if headings and tier != "M":
            block += ["sections (open the file for these): " + " · ".join(h.lstrip('#').strip() for h in headings), ""]
        block += ["\n\n".join(rules), ""]
    else:
        block += ["(no rules-shaped section — file included WHOLE)", "",
                  body.split("\n---", 2)[-1].strip() if body.startswith("---") else body.strip(), ""]
    if p_lines:
        block += [f"project CASE sections lifted to their own tier ({len(p_lines)}, read them in the file):", ""] + p_lines + [""]
    return tier, "\n".join(block), p_lines


def build_by_tier():
    files = sorted(glob.glob(os.path.join(LEARN, "2026-*.md")))
    parts, untagged, counts, psec = [], [], {}, []
    src_bytes = 0
    for f in files:
        rel = os.path.relpath(f, PROJECT)
        src_bytes += os.path.getsize(f)
        tier, block, p_lines = tier_block(f, rel)
        counts[tier or "UNTAGGED"] = counts.get(tier or "UNTAGGED", 0) + 1
        psec += p_lines
        if not tier:
            untagged.append(os.path.basename(f))
        parts.append(block)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tally = " · ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    header = (
        "---\n"
        f"date: {now[:10]}\n"
        "type: digest\n"
        "source: GENERATED by 2_Project_Files/tools/boot_digest.py --by-tier — never hand-edit; the lesson files are the source of truth\n"
        "status: live\n"
        "---\n\n"
        "# Boot digest BY TIER — W whole, M rules-only, every project case a handle\n\n"
        f"Generated {now} from {len(files)} lesson files ({src_bytes:,} B). {tally}. "
        f"{len(psec)} project CASE sections inside MIXED files are reduced to one line each: the heading and "
        "the path to read it at. W blocks are exactly what the default digest carries; M blocks drop the "
        "section index and keep the rules; a P file is a single handle. The CASES behind every rule live only "
        "in the lesson files — open one the moment its rule fires.\n\n"
        + (f"**UNTAGGED ({len(untagged)}) — no `tier:` in the frontmatter, so these fall back to the default "
           f"shape:** {' · '.join(untagged)}\n\n" if untagged else "")
    )
    out = header + "\n\n".join(parts) + "\n"
    tmp = OUT_BY_TIER + ".tmp"
    open(tmp, "w", encoding="utf-8").write(out)
    os.replace(tmp, OUT_BY_TIER)
    dig = len(out.encode())
    print(f"by-tier digest written: {OUT_BY_TIER}")
    print(f"  {len(files)} files, source {src_bytes:,} B -> by-tier {dig:,} B ({100*dig//src_bytes}%); "
          f"{tally}; {len(psec)} P case sections reduced to a handle")
    return 0


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
    if "--check" in sys.argv:
        sys.exit(check())
    if "--by-tier" in sys.argv:
        sys.exit(build_by_tier())
    sys.exit(build())
