"""operator 26: spelled product edit. usage: apply_fix.py <in> <out> <key>"""
import sys
FIX = {
 'p1': ("check-akto-container-names.sh",
  [("""PATTERN="(docker[[:space:]]+(exec|logs|inspect|cp|kill|stop|rm|restart)[[:space:]]+[\\"'\\`]?akto-[a-z0-9-]+)"\n""",
    """PATTERN="(docker[[:space:]]+(exec|logs|inspect|cp|kill|stop|rm|restart)([[:space:]]+-[^[:space:]]+)*[[:space:]]+[\\"'\\`]?akto-[a-z0-9-]+)"\n""")]),
}
if __name__ == '__main__':
    src, dst, key = sys.argv[1:4]
    t = open(src, encoding='utf-8').read()
    for o, n in FIX[key][1]:
        assert t.count(o) == 1, (key, o[:50], t.count(o))
        t = t.replace(o, n)
    open(dst, 'w', encoding='utf-8').write(t)
