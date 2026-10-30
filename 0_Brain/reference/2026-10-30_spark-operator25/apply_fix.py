"""operator 25: the spelled product edits, one dict used by the brief generator and the hand check.
usage: apply_fix.py <in> <out> <key>"""
import sys
FIX = {
 'p1': ("check-dockerfile-non-root.sh",
  [("""  last_user=$(grep -E '^\\s*USER\\s+' "$f" | tail -1 | sed -E 's/^\\s*USER\\s+//; s/[#].*$//' | tr -d '[:space:]')\n""",
    """  last_user=$(grep -E '^[[:space:]]*USER[[:space:]]+' "$f" | tail -1 | sed -E 's/^[[:space:]]*USER[[:space:]]+//; s/[#].*$//' | tr -d '[:space:]' || true)\n""")]),
 'p2': ("check-no-strictness-patches.sh",
  [("""  hits=$(grep -rEn --include='Dockerfile*' --include='*.sh' --include='*.yml' \\\n""",
    """  hits=$(grep -rEn --exclude-dir=node_modules --include='Dockerfile*' --include='*.sh' --include='*.yml' \\\n""")]),
 'p3': ("check-connector-xss.sh",
  [("""HITS=$(grep -rEn "(^|[[:space:]<])on[a-z]+=['\\"]" connectors/ \\\n""",
    """HITS=$(grep -rEn --exclude-dir=node_modules "(^|[[:space:]<])on[a-z]+=['\\"]" connectors/ \\\n""")]),
 'p4': ("check-no-pii-store.sh",
  [("""UNTRACKED=$(git ls-files --others --exclude-standard=false \\\n""",
    """UNTRACKED=$(git ls-files --others --exclude-standard \\\n"""),
   ("""  { [ -n "$UNTRACKED" ] && echo "$UNTRACKED"; [ -n "$FOUND" ] && echo "$FOUND"; } | sed 's/^/  /' >&2\n""",
    """  { [ -n "$UNTRACKED" ] && echo "$UNTRACKED"; [ -n "$FOUND" ] && echo "$FOUND"; true; } | sed 's/^/  /' >&2\n""")]),
}
if __name__ == '__main__':
    src, dst, key = sys.argv[1:4]
    t = open(src, encoding='utf-8').read()
    for o, n in FIX[key][1]:
        assert t.count(o) == 1, (key, o[:50], t.count(o))
        t = t.replace(o, n)
    open(dst, 'w', encoding='utf-8').write(t)
