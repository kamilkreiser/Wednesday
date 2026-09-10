#!/usr/bin/env python3
"""Page breaks before numbered top-level sections only.

Kam, 2026-09-10: "only create page breaks before level 1 headings. So section 1,
section 2, section 3, etc. Subsections and subpoints only need three enters."

Top-level numbered sections are the markdown '## ' headings (they render as the
document's outermost headings; the '# ' title is stripped into metadata by the
build). A standalone page-break block before '### ' or '#### ' is replaced by
three empty Word paragraphs -- three presses of Enter. The Contents block at the
head of the file bundles its break with other OpenXML and is never touched.
"""
import sys, re

FENCE = '```{=openxml}'
BRK   = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
ENTERS = [FENCE, '<w:p/><w:p/><w:p/>', '```']

def transform(path):
    lines = open(path).read().split('\n')
    out, i = [], 0
    kept = replaced = embedded = 0
    while i < len(lines):
        if lines[i].strip() == FENCE:
            j = i + 1
            while j < len(lines) and lines[j].strip() != '```':
                j += 1
            block = lines[i+1:j]
            if block == [BRK]:
                k = j + 1
                while k < len(lines) and not lines[k].strip():
                    k += 1
                nxt = lines[k] if k < len(lines) else ''
                m = re.match(r'^(#{1,6}) ', nxt)
                assert m, f"{path}: break at line {i+1} is not followed by a heading: {nxt[:80]!r}"
                if len(m.group(1)) == 2:
                    out.extend(lines[i:j+1]); kept += 1
                else:
                    out.extend(ENTERS);       replaced += 1
            else:
                if any('w:type="page"' in b for b in block):
                    embedded += 1
                out.extend(lines[i:j+1])
            i = j + 1
        else:
            out.append(lines[i]); i += 1
    open(path, 'w').write('\n'.join(out))
    return kept, replaced, embedded

for p in sys.argv[1:]:
    k, r, e = transform(p)
    print(f"{p.split('/')[-1]}: kept {k} page breaks (## sections) | "
          f"replaced {r} with three enters (###/####) | left {e} embedded block(s) alone")
