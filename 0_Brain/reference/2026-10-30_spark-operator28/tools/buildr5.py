# usage: python3 -I buildr5.py spec.py : LOOSE rung-5 brief; dictation + a PER-HUNK skeleton for replace-one-line hunks
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import loosegen22 as lg, mk22
def perhunk(S):
    t = ["\n**PER-HUNK SKELETON (read each one before you write that hunk; a past failure was showing the end state instead of the change).** In EVERY hunk the old SQL line is DELETED and a new one is ADDED; the two differ only in the tie-break words. Written top to bottom, the lines of each hunk are:\n"]
    k = 0
    for path, hunks in lg.product_hunks(S):
        for h, lines in hunks:
            k += 1
            t.append("- **Hunk %d** (`%s`, header `%s`), %d body lines:" % (k, path.split('/')[-1], h, len(lines)))
            seen_minus = False
            for n, l in enumerate(lines, 1):
                if l[0] == ' ': d = "context, starts with ONE SPACE: `%s`" % l[1:]
                elif l[0] == '-': d = "REMOVED, starts with `-` (NOT a space): `%s`" % l[1:]; seen_minus = True
                else: d = "ADDED, starts with `+`: YOUR new SQL line (the removed line above with the tie-break column added to its ORDER BY)"
                t.append("  %d. %s" % (n, d))
            t.append("  The old SQL line appears ONLY as the `-` line, never as a context line, and your new SQL line appears ONLY as a `+` line, never as a context line.")
    t.append("")
    return "\n".join(t)
m = lg.load(sys.argv[1]); S = dict(m.S)
S['rung_raw'] = '**' + S['rung'] + '**'
S['loose'] = "The product edits are described by behaviour in `## What is wrong` and `## Where`; no diff and no `+` line is given for them. Write them yourself: minimal, only what those two sections require.\n\n" + lg.dictation(m.S) + "\n" + perhunk(m.S)
if os.environ.get('REBRIEF'):
    S['dir'] = S['dir'] + '_rebrief'
    S['loose'] += chr(10)*2 + os.environ['REBRIEF']
mk22.build(S)
