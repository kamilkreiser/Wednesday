# Spark operator 22 shared spec helpers: the KS-1410 class (thrown text in a 500 body), LOOSE rung-4 code_patch2 + one NEW source-text vitest file
CONST = 'An unexpected error occurred'
def edit_sites(sites, mode='plain'):
    """sites: list of (k, logline_text, special) - k = index in the file-order list of lines containing `.status(500).json(`.
    returns a callable edit: for each chosen 500 statement, insert a console.error line before it and make the body constant."""
    def f(src):
        lines = src.split('\n')
        idx = [i for i, l in enumerate(lines) if '.status(500).json(' in l]
        for k, logtxt, kind in sorted(sites, reverse=True):
            i = idx[k]; stmt = lines[i]; ind = stmt[:len(stmt) - len(stmt.lstrip())]
            if kind == 'verified':
                assert stmt.strip() == "res.status(500).json({ verified: false, error: message });", stmt
                new = ind + "res.status(500).json({ verified: false, error: '%s' });" % CONST
            else:
                old = "message: message } });"
                assert stmt.rstrip().endswith(old), stmt
                new = stmt.replace(old, "message: '%s' } });" % CONST)
            log = ind + "console.error(%s, message);" % logtxt
            if kind == 'headers':   # statement sits inside `if (!res.headersSent) {`: log before the `if`, one indent level out
                assert lines[i-1].strip() == 'if (!res.headersSent) {', lines[i-1]
                lines[i] = new
                ind2 = ind[:-2]
                lines.insert(i-1, ind2 + "console.error(%s, message);" % logtxt)
            else:
                assert lines[i-1].strip().startswith('const message = err instanceof Error'), lines[i-1]
                lines[i] = new
                lines.insert(i, log)
        return '\n'.join(lines)
    return f

TEST_HEAD = '''import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const SRC = readFileSync(resolve(__dirname, '..', '%(file)s'), 'utf8');
const CONSTANT = '%(const)s';

type Five = { line: number; stmt: string; handler: string; context: string };

/** Every statement that answers 500 through `.status(500).json(...)`, with the route it sits in and the 4 lines (plus the same line's prefix) before it. */
function fiveHundreds(source: string): Five[] {
  const lines = source.split('\\n');
  const out: Five[] = [];
  lines.forEach((text, i) => {
    const at = text.indexOf('.status(500).json(');
    if (at < 0) return;
    let handler = '';
    for (let j = i; j >= 0; j--) {
      const m = /^\\s*(?:app|router)\\.(get|post|put|patch|delete)\\(\\s*'([^']+)'/.exec(lines[j]);
      if (m) {
        handler = m[1].toUpperCase() + ' ' + m[2];
        break;
      }
    }
    out.push({ line: i + 1, stmt: text.slice(at), handler, context: lines.slice(Math.max(0, i - 4), i).join('\\n') + '\\n' + text.slice(0, at) });
  });
  return out;
}

/** True when the response argument names a caught value: an identifier left once string literals and the envelope keys are removed. */
function leaks(stmt: string): boolean {
  const bare = stmt.replace(/'[^']*'/g, "''").replace(/\\b(success|error|code|message|verified)\\s*:/g, '');
  return /\\b(err|error|msg|message|detail|details|stack)\\b/.test(bare);
}

const FIVE = fiveHundreds(SRC);
'''
