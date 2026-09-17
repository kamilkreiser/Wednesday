#!/usr/bin/env python3
"""a3b_proxy.py <input.json> <clone> <sections.json> <product repo path> <repo subdir>

A3b ASCII_PROXY (2026-09-17, Kam 15:37 "keep the local agent constantly churning through the backlog"). The model will
not reproduce a '-' line that carries non-ASCII: KS-839 r1 AND its retry (14:17/14:18) kept the em-dash line :353 as
CONTEXT and deleted its ASCII neighbour :354 instead; KS-1180-P1 did the same family on emoji. A brief cannot remove
the character from the tip. So a LINE-KEYED site may declare `ascii_proxy U+XXXX=<ascii>`: the model writes that '-'
line with each declared character replaced by its ASCII stand-in (the builder stores the exact line as
`sites[].ascii_proxy.text`), and this helper puts the tip's real bytes back BEFORE A2 applies anything.

A '-' line is substituted ONLY when BOTH hold:
  1. its text (everything after the '-') is BYTE-EQUAL to the site's ascii_proxy.text (the tip line after the declared
     substitution; indentation and trailing text included), and
  2. the hunk's OWN old-side lines place it at the site's line number: with the hunk laid over the tip so that this
     line sits at N, every other old-side line (context ' ' and '-') equals the tip line under it, whitespace-stripped
     (the evidence `git apply --ignore-whitespace` uses), and at least one of them is non-blank. The hunk header is
     NOT used (headers drift; A2's lenient mode ignores them too). Another declared proxy line in the same hunk
     counts as matching when it is byte-equal to ITS site's proxy text at its own number.
Nothing else is ever rewritten: context and '+' lines are untouched, and a3b_line.py still measures which tip line the
applied section REALLY removes, so a substituted line that lands anywhere but N is MISSED there.

Refusals (rc 1, the checker prints them as an A3b PARTIAL FIX naming the site, before A2):
  MISPLACED :N `<proxy text>` <why>     a '-' line byte-equal to N's proxy text that its hunk does not place at N
  TEXTMISMATCH :N `<proxy text>` <why>  a '-' line its hunk places at N whose text is neither the tip's line nor the
                                        declared proxy text (one character off, a hyphen for `--`, a \\u escape, an
                                        indent change: "any other difference")
Not a refusal: a '-' line at N that already equals the tip line (the model reproduced the character: nothing to do),
or no '-' line for the site at all (a3b_line.py grades that as MISSED after A2, exactly as before).
Output on rc 0: `SUBSTITUTED :N section=<file> line=<k>` per substitution, or `NOPROXYLINE ...`; the model's section is
kept beside it as `<section>.model.diff` whenever a substitution is written. `PROXY none` when no site declares one.
rc 0 ok · 1 MISPLACED/TEXTMISMATCH · 2 measure error. Arms: local-model/tests/a3b_ascii_proxy_arms.sh.
"""
import json, re, shutil, subprocess, sys


def cp_map(m):
    out = {}
    for k, v in (m or {}).items():
        mm = re.match(r"^U\+([0-9A-Fa-f]{4,6})$", k)
        if not mm or not v or any(ord(ch) > 127 or ch.isspace() for ch in v):
            raise ValueError(f"bad ascii_proxy map entry {k!r}={v!r}")
        out[chr(int(mm.group(1), 16))] = v
    return out


def proxied(text, m):
    for ch, sub in m.items():
        text = text.replace(ch, sub)
    return text


def main():
    if len(sys.argv) != 6:
        print("MEASURE ERROR: usage: a3b_proxy.py <input.json> <clone> <sections.json> <product> <subdir>"); return 2
    inp, clone, secj, product, subdir = sys.argv[1:6]
    d = json.load(open(inp, encoding="utf-8"))
    sites = [s for s in (d.get("defect_line") or {}).get("sites", [])
             if s.get("ascii_proxy") and s.get("key") == "line+text" and s.get("must_change")]
    if not sites:
        print("PROXY none"); return 0
    r = subprocess.run(["git", "-C", clone, "show", f"{d['tip']}:{product}"], capture_output=True)
    if r.returncode != 0:
        print(f"MEASURE ERROR: git show {d['tip'][:9]}:{product} rc={r.returncode}: {r.stderr.decode(errors='replace')[:200]}"); return 2
    tip = r.stdout.decode("utf-8").split("\n")
    proxy = {}  # line number -> (proxy text, tip text)
    for s in sites:
        n = int(s["line"])
        try:
            m = cp_map(s["ascii_proxy"].get("map"))
        except ValueError as e:
            print(f"MEASURE ERROR: site :{n}: {e}"); return 2
        if not (1 <= n <= len(tip)):
            print(f"MEASURE ERROR: site :{n} is outside {product} ({len(tip)} lines)"); return 2
        t = tip[n - 1]; p = s["ascii_proxy"].get("text") or ""
        if proxied(t, m) != p or p == t or any(ord(ch) > 127 for ch in p):
            print(f"MEASURE ERROR: site :{n}: ascii_proxy.text is not the tip line under its declared map (a stale input; rebuild)"); return 2
        proxy[n] = (p, t)
    sections = json.load(open(secj, encoding="utf-8"))
    sec = next((o for o in sections if o.get("path") == product or f"{subdir}/{o.get('path')}" == product), None)
    if sec is None:
        print("NOPROXYLINE no product section in the diff (A3 will name it)"); return 0
    L = open(sec["file"], encoding="utf-8").read().split("\n")
    trailing_nl = bool(L) and L[-1] == ""
    if trailing_nl:
        L.pop()
    fails, subs = [], []
    i = 0
    while i < len(L):
        if not re.match(r"^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@", L[i]):
            i += 1; continue
        j = i + 1; old = []  # (section index, kind, text)
        while j < len(L) and not L[j].startswith("@@ ") and not L[j].startswith("--- ") and not L[j].startswith("diff --git "):
            c = L[j][:1]
            if c in (" ", "-") or L[j] == "":
                old.append((j, "-" if c == "-" else " ", L[j][1:] if L[j] else ""))
            j += 1
        def placed(k, n):
            """True when laying the hunk's old side over the tip with old[k] at line n matches every other line."""
            o = n - 1 - k
            nonblank = 0
            for q, (_, kind, txt) in enumerate(old):
                if q == k:
                    continue
                ln = o + q + 1
                if ln < 1 or ln > len(tip):
                    return False
                if kind == "-" and ln in proxy and txt == proxy[ln][0]:
                    nonblank += 1; continue
                if txt.strip() != tip[ln - 1].strip():
                    return False
                if txt.strip():
                    nonblank += 1
            return nonblank >= 1
        for k, (idx, kind, txt) in enumerate(old):
            if kind != "-":
                continue
            hit = [n for n in proxy if txt == proxy[n][0]]
            for n in hit:
                if placed(k, n):
                    subs.append((idx, n))
                else:
                    fails.append(f"MISPLACED :{n} `{proxy[n][0].strip()[:90]}` (ascii_proxy '-' line at section line {idx + 1}: the hunk's own lines do not place it at :{n} - the wrong line)")
            if hit:
                continue
            for n in proxy:
                if placed(k, n) and txt.strip() != proxy[n][1].strip():
                    fails.append(f"TEXTMISMATCH :{n} `{proxy[n][0].strip()[:90]}` (the '-' line its hunk places at :{n} is `{txt.strip()[:90]}` - neither the tip line nor its declared ascii_proxy text)")
        i = j
    if fails:
        print("\n".join(fails)); return 1
    if not subs:
        print(f"NOPROXYLINE no '-' line equals a declared ascii_proxy text (sites {sorted(proxy)}); nothing substituted"); return 0
    shutil.copyfile(sec["file"], sec["file"] + ".model.diff")
    for idx, n in subs:
        L[idx] = "-" + proxy[n][1]
    open(sec["file"], "w", encoding="utf-8").write("\n".join(L) + ("\n" if trailing_nl else ""))
    for idx, n in subs:
        print(f"SUBSTITUTED :{n} section={sec['file']} line={idx + 1} (the model's ascii_proxy text -> the tip's bytes; the model's section kept as {sec['file']}.model.diff)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
