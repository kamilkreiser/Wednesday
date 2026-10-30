# Spark operator 21: NEW-file test_only brief builder (KS-1836 F1 / Mf). Reads the product at TIP via git show in GEN_SRC clone.
import sys, os, subprocess, difflib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/3595961a-a258-453d-996e-1aad78887d58/scratchpad/op21/clone'
BR = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
TIP = os.environ.get('GEN_TIP', '530f091120d5da749edf972e8e0089e44cfc5589')
def rd(p): return subprocess.run(['git', '-C', SRC, 'show', TIP + ':' + p], check=True, capture_output=True).stdout.decode('utf-8')
def newfile_diff(path, content):
    b = content.splitlines(keepends=True)
    out = [f'diff --git a/{path} b/{path}\n', 'new file mode 100644\n', '--- /dev/null\n', f'+++ b/{path}\n', '@@ -0,0 +1,%d @@\n' % len(b)]
    out += ['+' + l for l in b]
    return ''.join(out)
def build(T):
    prod = rd(T['product']).split('\n')
    assert prod[T['tamper_line'] - 1] == T['tamper_from'], (prod[T['tamper_line'] - 1], T['tamper_from'])
    k = T['ticket']; test = T['test']; content = T['content']
    nl = len(content.splitlines())
    diff = newfile_diff(test, content)
    d = BR + T['dir']
    if os.path.exists(d + '/golden.diff') and not os.environ.get('GEN_OVERWRITE'): sys.exit('REFUSED: exists ' + d)
    os.makedirs(d, exist_ok=True)
    open(d + '/golden.diff', 'w', encoding='utf-8').write(diff)
    open(d + '/spark.pins', 'w').write(f"# test_only, a NEW test file (the tamper is in {os.path.basename(T['product'])}, the product is NOT modified); ref = a source-text test of the same shape (shape only); line = the tamper line at the tip.\ntier=test_only\nref={T['ref']}\nline={T['tamper_line']}\n")
    s = f"# {k} {T['title']}\n\n{T['intro']}\n\nFile: `{T['product']}`  (product, NOT modified: it is the tamper target only)\nTest file: `{test}`  (NEW file, {nl} lines, given in full below; {T['ncells']})\n"
    s += f"Tip: `{TIP}` (origin/develop by `git ls-remote` on 2026-10-30; every line number and quote below was read from a shared clone at exactly this sha)\nRunner: `{T['runner']}`\nTier: `test_only` (the `## Tamper` block below)\nRung: **3 (test-only mode, a NEW test file given byte-exact; a planted tamper must redden the declared cells)**\n\n"
    s += "## Scope\n\n" + T['scope'] + "\n\n"
    s += "## The mode - read this twice\n\nTEST-ONLY, NEW FILE. Your diff contains EXACTLY ONE file: the NEW test file above, as a new-file diff (`--- /dev/null`, NEVER `--- a/`), ONE hunk. **No hunk for `" + os.path.basename(T['product']) + "`.** Do NOT modify any existing test file (the ks1232 info-reader test least of all). The checker reddens your new cells by planting the tamper named below into a clone of the product file, then expects the file GREEN at the untouched tip. A diff that touches the product file is refused at A3.\n\n"
    s += "## What is wrong (one paragraph)\n\n" + T['wrong'] + "\n\n## Where\n\n" + T['where'] + "\n\n"
    s += "## The exact change\n\nNONE to the product: `" + T['product'] + "` is right at the tip and is not edited. The only change is the NEW vitest test file (new-file diff, `--- /dev/null`), the whole file, one hunk:\n\nFile: `" + test + "`\n\n```diff\n" + diff + " BRIEF-MARKER: the line you are reading ends the fence; it is NOT file content and NOT part of your diff\n```\n\nThe `+` lines are byte-exact: copy them; do not paraphrase a comment, do not re-indent. Indentation is spaces only. The one fence line that begins with a single space and reads `BRIEF-MARKER ...` is a marker for the brief's tooling (the builder refuses a fence with no line after the last `+`): never copy it. Your diff ends with the file's last `+` line; its hunk header counts only the `+` lines.\n\n"
    s += "## The test\n\nThe new test file is the one given under `## The exact change`: `" + test + "`.\n\n"
    s += f"## Tamper (test-only mode - the checker plants this in a clone of {os.path.basename(T['product'])} to prove your cells can go red)\nline: {T['tamper_line']}\nfrom: `{T['tamper_from']}`\nto: `{T['tamper_to']}`\nstatement_ok: {T['statement_ok']}\n\n"
    s += "## Red cells\n" + ''.join(f"- {c}\n" for c in T['red']) + "\n## Cells and controls\n\n" + T['cells'] + "\n\n"
    s += "## UNMEASURED - stated rather than glossed\n\n" + T['unmeasured'] + "\n\n"
    s += "## Output\n\nExactly ONE fenced ```diff block, nothing outside it: `diff --git a/" + test + " b/" + test + "`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/" + test + "`, then the hunk header `@@ -0,0 +1,%d @@` and every body line starting `+`. Every `+` line on its own physical line.\n" % nl
    open(d + f'/{k}.md', 'w', encoding='utf-8').write(s)
    print('wrote', d, nl, 'lines')
if __name__ == '__main__':
    sp = importlib.util.spec_from_file_location('s', sys.argv[1]); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); build(m.T)
