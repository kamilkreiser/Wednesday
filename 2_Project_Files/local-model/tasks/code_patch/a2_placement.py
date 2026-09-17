#!/usr/bin/env python3
"""a2_placement.py — code_patch A2 placement: the CONTEXT-WS reanchor and the FUZZY offset guard (2026-09-18, KS-1229).

WHY: KS-1229 r1 + retry (runs/2026-09-18_ks1229-ornith35b-night) — the model's 43 '+' lines were byte-exact, but it
re-indented ONE trailing context line (`});` at column 0 written `  });`). Strict and --recount --ignore-whitespace both
fail (git's whitespace tolerance never matches "no leading space" against "some"), so the checker fell to FUZZY (-C1),
and `-C1` matched the FIRST `  });` of nine: "apply fragment at 174" for a hunk whose header says `@@ -204`. The cells
landed in a scope with no `issue` (a load error). Into a scope that compiles it would have been a false green.

Two subcommands:

  ctxws <section.diff> <file-at-tip> <out.diff>
      For every hunk: its OLD side (context + '-' lines) must equal the tip's lines at the header's old-start after
      stripping leading/trailing whitespace from both — searched at offsets 0, ±1, ±2, ±3 only (the same bound as the
      fuzzy guard), nearest first; a tie at the nearest distance is ambiguous and refused. The hunk is rebuilt with the
      TIP's exact text for every context and '-' line and honest counts; the '+' lines are copied byte for byte (never
      altered). Refused (rc 1, section left alone): a new-file section, a body line with no diff marker, an old side
      with no non-blank line, a match outside the window, a tie, overlapping hunks. rc 0 = wrote <out.diff>; the caller
      then applies it STRICTLY and records "A2 CONTEXT-WS REANCHORED at <line>".
      stdout: `hunk <k>: CONTEXT-WS at <line> (header old-start <S>, offset <d>): <n> context/'-' line(s) differ from the
      tip only in whitespace: :<line> written=<indent> tip=<indent> ...` · last line `ctxws <n>/<n> hunk(s)`.

  fuzzy <section.diff> <git-apply-check-v-output>
      Reads `git apply --check -v --recount --ignore-whitespace -C1` output for the section. For every hunk git had to
      REDUCE the context of ("Context reduced to (l/t) to apply fragment at N"): B = old-start + (net line delta of the
      hunks before it) is the header's line in the image git patches, and D = the leading context lines git dropped.
      N is PLACED when B - 3 <= N <= B + D + 3, else MISPLACED. The window is the header line itself (the literal rule:
      N within 3 of the old-start) widened upward by D, because N is where the REDUCED fragment starts: when the D dropped
      lines are real file lines N sits D lines below the header, and when the model invented or drifted them it sits
      nearer the header — census 2026-09-18: KS-1074 (header 5 lines late, 6 dropped, the right code) and KS-1087
      (header 13 late, 15 dropped, the right code) both land inside; KS-1229 (174 for 204, 1 dropped) does not.
      (git searches from the header's NEW start in the partly-patched image, so N is in that image's coordinates; B is
      computed in the same coordinates from the hunks' measured -/+ counts, so a model that miscounts its later
      new-starts does not skew the measure. A hunk applied with its FULL context is not judged here — that is ordinary
      strict/lenient placement.)
      stdout: `PLACED hunk <k> at <N> (header old-start <S>, expected <B>..<B+D>, off by <d>, context reduced to <l>/<t>, …)`
      or `MISPLACED hunk <k> at <N> (…the same…)` · `UNMEASURED …`. <d> is the distance outside [B, B+D] (0 inside).
      rc 0 every reduced hunk inside its window · 1 >= 1 MISPLACED · 2 a reduced fragment could not be tied to a hunk (fail closed).
"""
import re
import sys

BOUND = 3
HDR = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")


def parse(text):
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    head, hunks, cur = [], [], None
    for ln in lines:
        m = HDR.match(ln)
        if m:
            cur = {"header": ln, "S": int(m.group(1)), "N": int(m.group(3)), "tail": m.group(5), "body": []}
            hunks.append(cur)
        elif cur is None:
            head.append(ln)
        else:
            cur["body"].append(ln)
    for h in hunks:
        while h["body"] and h["body"][-1] == "":
            h["body"].pop()
    return head, hunks


def counts(body):
    old = sum(1 for b in body if b == "" or b[:1] in (" ", "-"))
    new = sum(1 for b in body if b == "" or b[:1] in (" ", "+"))
    return old, new


def lead(body):
    n = 0
    for b in body:
        if b == "" or b[:1] == " ":
            n += 1
        elif b[:1] in ("+", "-"):
            break
    return n


def ctxws(section, tipfile, out):
    head, hunks = parse(open(section, encoding="utf-8").read())
    if not hunks:
        print("ctxws refused: no hunk in the section"); return 1
    if any(l.startswith("--- /dev/null") for l in head):
        print("ctxws refused: a new-file section has no tip lines to match"); return 1
    raw = open(tipfile, encoding="utf-8", errors="surrogateescape").read().split("\n")
    n_file = len(raw) - (1 if raw and raw[-1] == "" else 0)
    tip = raw[:n_file]
    res = list(head); notes = []; delta = 0; prev_end = 0
    for k, h in enumerate(hunks, 1):
        body = h["body"]
        bad = [b for b in body if b and b[:1] not in (" ", "-", "+", "\\")]
        if bad:
            print(f"ctxws refused: hunk {k} has a body line with no diff marker ({bad[0][:60]!r})"); return 1
        old = [(i, ("" if b == "" else b[1:])) for i, b in enumerate(body) if b == "" or b[:1] in (" ", "-")]
        if not any(t.strip() for _, t in old):
            print(f"ctxws refused: hunk {k} has no non-blank context or '-' line to anchor on"); return 1
        S = h["S"]
        if S < 1:
            print(f"ctxws refused: hunk {k} old-start {S}"); return 1
        hits = []
        for d in range(-BOUND, BOUND + 1):
            s0 = S - 1 + d
            if s0 < 0 or s0 + len(old) > n_file:
                continue
            if all(tip[s0 + j].strip() == t.strip() for j, (_, t) in enumerate(old)):
                hits.append(d)
        if not hits:
            print(f"ctxws refused: hunk {k} (header old-start {S}) — its {len(old)} context/'-' line(s) do not equal the tip's, whitespace-stripped, at any line within {BOUND} of {S}")
            return 1
        best = min(abs(d) for d in hits)
        near = [d for d in hits if abs(d) == best]
        if len(near) > 1:
            print(f"ctxws refused: hunk {k} (header old-start {S}) matches whitespace-stripped at BOTH offsets {near} — ambiguous")
            return 1
        d = near[0]; s0 = S - 1 + d
        if s0 < prev_end:
            print(f"ctxws refused: hunk {k} placed at {s0 + 1} overlaps the previous hunk (ends {prev_end})"); return 1
        ws = []
        rebuilt = []; j = 0
        for b in body:
            if b[:1] == "+" or b[:1] == "\\":
                rebuilt.append(b); continue
            t = "" if b == "" else b[1:]
            tl = tip[s0 + j]
            if t != tl:
                wi = len(t) - len(t.lstrip()); ti = len(tl) - len(tl.lstrip())
                ws.append(f":{s0 + j + 1} written indent {wi} tip indent {ti}" + ("" if t.rstrip() == t and tl.rstrip() == tl else " (trailing ws)"))
            rebuilt.append(("-" if b[:1] == "-" else " ") + tl)
            j += 1
        o, n = counts(rebuilt)
        res.append(f"@@ -{s0 + 1},{o} +{s0 + 1 + delta},{n} @@{h['tail']}")
        res += rebuilt
        delta += n - o; prev_end = s0 + o
        notes.append(f"hunk {k}: CONTEXT-WS at {s0 + 1} (header old-start {S}, offset {d:+d}): {len(ws)} context/'-' line(s) differ from the tip only in whitespace" + (": " + " · ".join(ws[:4]) + (" …" if len(ws) > 4 else "") if ws else ""))
    open(out, "w", encoding="utf-8", errors="surrogateescape").write("\n".join(res) + "\n")
    for n_ in notes:
        print(n_)
    print(f"ctxws {len(hunks)}/{len(hunks)} hunk(s)")
    return 0


def fuzzy(section, vout):
    _, hunks = parse(open(section, encoding="utf-8").read())
    info = []; acc = 0
    for h in hunks:
        o, n = counts(h["body"])
        info.append({"S": h["S"], "N": h["N"], "lead": lead(h["body"]), "base": h["S"] + acc})
        acc += n - o
    ev = []
    for ln in open(vout, encoding="utf-8", errors="replace").read().split("\n"):
        m = re.match(r"^Hunk #(\d+) succeeded at (\d+) \(offset (-?\d+) lines?\)\.", ln)
        if m:
            ev.append(("hunk", int(m.group(1)), int(m.group(2)))); continue
        m = re.match(r"^Context reduced to \((\d+)/(\d+)\) to apply fragment at (\d+)", ln)
        if m:
            ev.append(("red", int(m.group(1)), int(m.group(2)), int(m.group(3))))
    reduced = {}; rc = 0; out = []
    for i, e in enumerate(ev):
        if e[0] != "red":
            continue
        l, t, at = e[1], e[2], e[3]
        k = None
        if i > 0 and ev[i - 1][0] == "hunk" and ev[i - 1][2] == at and ev[i - 1][1] not in reduced:
            k = ev[i - 1][1]
        else:
            lo = max([x[1] for x in ev[:i] if x[0] == "hunk"] + [max(reduced) if reduced else 0])
            hi = min([x[1] for x in ev[i + 1:] if x[0] == "hunk"] + [len(hunks) + 1])
            # no "Hunk #k succeeded" line = git placed it at its own search origin: new-start - (dropped leading lines)
            cands = [c for c in range(lo + 1, hi) if c not in reduced and info[c - 1]["lead"] >= l and at == info[c - 1]["N"] - (info[c - 1]["lead"] - l)]
            if len(cands) == 1:
                k = cands[0]
        if k is None or not (1 <= k <= len(hunks)):
            out.append(f"UNMEASURED a fragment reduced to ({l}/{t}) applied at {at} could not be tied to one hunk of {len(hunks)}")
            rc = max(rc, 2); continue
        reduced[k] = (l, t, at)
    for k in sorted(reduced):
        l, t, at = reduced[k]; h = info[k - 1]
        dropped = max(0, h["lead"] - l)
        lo, hi = h["base"], h["base"] + dropped
        off = at - hi if at > hi else (at - lo if at < lo else 0)
        word = "PLACED" if abs(off) <= BOUND else "MISPLACED"
        out.append(f"{word} hunk {k} at {at} (header old-start {h['S']}, expected {lo}..{hi}, off by {off:+d}, context reduced to {l}/{t}, {dropped} leading line(s) dropped)")
    if not reduced and rc == 0:
        out.append("PLACED no hunk needed reduced context (nothing to guard)")
    print("\n".join(out))
    if rc == 2:
        return 2          # an unmeasurable fragment fails closed
    return 1 if any(o.startswith("MISPLACED") for o in out) else 0


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "ctxws" and len(sys.argv) == 5:
        return ctxws(*sys.argv[2:5])
    if len(sys.argv) >= 2 and sys.argv[1] == "fuzzy" and len(sys.argv) == 4:
        return fuzzy(*sys.argv[2:4])
    print(__doc__.split("\n")[0]); print("usage: a2_placement.py ctxws <section.diff> <file-at-tip> <out.diff> | fuzzy <section.diff> <apply -v output>")
    return 3


if __name__ == "__main__":
    sys.exit(main())
