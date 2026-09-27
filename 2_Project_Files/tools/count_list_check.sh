#!/bin/bash
# count_list_check.sh — ADVISORY. Reads a message on stdin and flags a COUNT typed beside the LIST it counts
# when the two disagree ("Five tickets depend on this answer (HPSM-12/19/25/32/35/41)" — six ids, not five).
#
# WHY (Friday ledger w=3, 2026-09-27, the laptop coordinator seat): three times in ONE day I wrote a number next
# to the list it was counting, and they disagreed. A card to Kam said "Five tickets depend on this answer" and then
# listed six (HPSM-12/19/25/32/35/41); another said "Four High findings" over a list of three. The count is typed
# from memory and the list is pasted from the measurement, so they drift the moment the list is edited and the
# number is not. Kam reads both on the one surface he rules from, and a mismatch there makes him distrust the list.
# Re-reading by willpower did not catch it three times running, so this puts the comparison in the path.
#
# WHAT IT MATCHES: a count (one…twenty, or a bare digit 1–99 that is not part of an id, time, version or #ref)
# followed IN THE SAME SENTENCE, within six words, by a list: a parenthesised group or a colon-introduced group
# (colon + space), with items split on ",", "/", " · ", ";", " and ", " or ". A slash-run of ids like
# HPSM-12/19/25 is three items. A group with fewer than two items, or with any item longer than six words, is
# treated as prose, not a list (that is the main false-positive guard).
#
# ADVISORY BY DESIGN: English uses numbers loosely ("two of the five", "one decision: A or B"), so this NEVER
# blocks and ALWAYS exits 0. It prints to stderr only. Its job is to make me look, not to decide for me.
# Usage: printf '%s' "$MSG" | count_list_check.sh      Arms: tests/count_list_check_arms.sh
set -u
CLC_TEXT="$(cat)"
export CLC_TEXT
python3 - <<'PYEOF' || true
import os, re, sys
text = os.environ.get("CLC_TEXT", "")
WORDS = {w: i for i, w in enumerate(
    "one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty".split(), 1)}
# A count: a spelled number, or a 1-2 digit number NOT glued to an id / time / version / ref / unit / 1,374.
COUNT = re.compile(r"(?<![\w#$:./,-])(?:(?P<w>" + "|".join(WORDS) + r")|(?P<d>[1-9][0-9]?))(?![\w:./%'’-]|,\d)", re.I)
OPENER = re.compile(r"\(|:\s")
# The word right after a count that says it is NOT counting a following list ("one of them", "two are overdue",
# "one at a time", "19 Aug", "three after reading them").
NOT_A_COUNT_NEXT = set("""of at after before as are is was were in on to from per more less or and the a an times
    by for with than into over under since until ago jan feb mar apr may jun jul aug sep sept oct nov dec
    january february march april june july august september october november december""".split())
PRIMARY = re.compile(r"\s*(?:,|;|\s·\s)\s*")                 # the separators a list is built from
LAST_CONJ = re.compile(r"^(?:and|or)\s+|\s+(?:and|or)\s+", re.I)
# An item opening with one of these is an ASIDE ("4 commands (from the handover doc, section 5.1)"), not a list.
ASIDE_FIRST = set("from on in under after before at per see via e.g. i.e. incl including as by with not was were is are".split())
MAX_ITEM_WORDS = 4
MAX_BETWEEN_WORDS = 5

def sentences(t):
    for para in re.split(r"\n+", t):
        for s in re.split(r"(?<=[.!?;])\s+", para):
            if s.strip():
                yield s

def group_after(s, pos):
    """The list group opening at s[pos] ('(' or ': '). Returns its raw text."""
    if s[pos] == "(":
        depth, i = 0, pos
        while i < len(s):
            if s[i] == "(":
                depth += 1
            elif s[i] == ")":
                depth -= 1
                if depth == 0:
                    return s[pos + 1:i]
            i += 1
        return s[pos + 1:]
    return s[pos + 1:].strip().rstrip(".!?;").strip()

def items_of(g):
    """Split a group into items. Commas / ';' / ' · ' are the list's own separators, and a final
    ' and ' / ' or ' joins its last item (Oxford comma or not). '/' separates items ONLY when the group
    has none of those — so HPSM-12/19/25 is three items, but '#730/KS-570, #726/KS-667' is two pairs."""
    flat = re.sub(r"\([^()]*\)", "", g).strip()          # drop nested asides: "A (merged), B" -> "A , B"
    parts = [p for p in PRIMARY.split(flat) if p.strip()]
    if len(parts) > 1:
        last = [x for x in LAST_CONJ.split(parts[-1], maxsplit=1) if x.strip()]
        parts = parts[:-1] + last
    else:
        parts = [x for x in LAST_CONJ.split(flat, maxsplit=1) if x.strip()]
        if len(parts) == 1:
            parts = flat.split("/")
    return [p.strip(" .\t'\"") for p in parts if p.strip(" .\t'\"")]

for s in sentences(text):
    for m in COUNT.finditer(s):
        n = WORDS[m.group("w").lower()] if m.group("w") else int(m.group("d"))
        if n == 1:
            continue          # "one thing / one at a time / one of them" — measured as mostly noise on 2026-09-27
        nxt = re.match(r"\s*([\w']+)", s[m.end():])
        if not nxt or nxt.group(1).lower() in NOT_A_COUNT_NEXT:
            continue
        o = OPENER.search(s, m.end())
        if not o:
            continue
        between = s[m.end():o.start()]
        # Too far away, or another count sits between (the nearer count owns the list).
        if len(between.split()) > MAX_BETWEEN_WORDS or COUNT.search(between) or re.search(r"[()]", between):
            continue
        raw = group_after(s, o.start())
        if re.search(r"\bvs\.?\b|\bversus\b", raw, re.I) or re.search(r"(\.\.\.|…|\betc\.?)\s*$", raw.strip(), re.I):
            continue          # a comparison, or an open-ended list ("x4, x3 ...") that is not meant to be complete
        items = items_of(raw)
        if items and (items[0].split()[0].lower().rstrip(":") in ASIDE_FIRST or any(":" in i for i in items)):
            continue          # an aside or a labelled note, not an enumeration
        if len(items) < 2 or any(len(i.split()) > MAX_ITEM_WORDS for i in items):
            continue          # prose, not a list
        # A breakdown ("62 tickets: 10 done, 40 partly…") or nested counts ("backend/, five build trees") sums,
        # it does not enumerate — skip rather than guess.
        if any(re.match(r"\d+\s+\w", i) or COUNT.search(i) and not re.fullmatch(r"[\w#./-]+", i) for i in items):
            continue
        if len(items) != n:
            phrase = (m.group(0) + between).strip().rstrip(":").strip()
            print(f'count_list_check: ADVISORY — "{phrase}" but the list has {len(items)} items: {raw.strip()}',
                  file=sys.stderr)
PYEOF
exit 0
