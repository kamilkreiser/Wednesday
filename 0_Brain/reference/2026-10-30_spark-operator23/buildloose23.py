# usage: python3 -I buildloose23.py spec.py : LOOSE candidate; dictation + a PER-HUNK instruction (Wednesday 2026-10-30)
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import loosegen22 as lg, mk22
def perhunk(S):
    t = ["\n**PER-HUNK INSTRUCTION (read each one before you write that hunk; a previous attempt failed by showing the end state instead of the change).** In EVERY hunk the old `res.status(500).json(...)` line is DELETED and a new one is ADDED. Written top to bottom, the lines of each hunk are:\n"]
    k = 0
    for path, hunks in lg.product_hunks(S):
        for h, lines in hunks:
            k += 1
            t.append("- **Hunk %d** (header `%s`), %d body lines:" % (k, h, len(lines)))
            for n, l in enumerate(lines, 1):
                if l[0] == ' ': d = "context, starts with ONE SPACE: `%s`" % l[1:]
                elif l[0] == '-': d = "REMOVED, starts with `-` (NOT a space): `%s`" % l[1:]
                elif l[1:].lstrip().startswith('console.error'): d = "ADDED, starts with `+`: YOUR `console.error('[mcp-http] ...', message);` line"
                else: d = "ADDED, starts with `+`: YOUR new `res.status(500).json(...)` line with the constant message"
                t.append("  %d. %s" % (n, d))
            t.append("  The old `res.status(500)` line above appears ONLY as the `-` line, never as a context line, and your new `res.status(500)` line appears ONLY as a `+` line, never as a context line.")
    t.append("")
    return "\n".join(t)
m = lg.load(sys.argv[1]); S = dict(m.S)
S['rung_raw'] = '**' + S['rung'] + '**'
S['loose'] = S['loose'] + lg.dictation(m.S) + "\n" + perhunk(m.S)
mk22.build(S)
