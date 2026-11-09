#!/usr/bin/env python3
"""template_siblings.py — A4 (2026-11-09). For any file the PR's touched (non-test) code sources or reads by path, find the
SHIPPED template/example sibling of that file in the repo (env.example, *.example, *.sample, *.template, ...) and name it in facts.json
under "template_siblings", so spark_review.py can put it in front of the reviewer. Deterministic, no LLM.
usage: template_siblings.py REPO HEAD_SHA OUT      (reads OUT/facts.json, rewrites it with the new key)
Bounds: at most 3 sibling files, each shown at most 400 lines (the facts record the true line count and truncation).
Why: PR 2127 sourced a .env at runtime; the committed env.example (the file the code would meet on a fresh clone) was in the repo
but not in the diff, the Spark never saw it, and the Blocker it carried was missed."""
import sys, os, re, json, subprocess

MAX_FILES, MAX_LINES = 3, 400
CFG_EXT = r"(?:env|json|ya?ml|conf|cfg|ini|toml|tpl|template|cnf|properties|txt)"
# a path-ish literal naming a config-like file, or an .env variant
LIT = re.compile(r"""(?<![\w.])((?:[\w./${}\-]*/)?\.?[\w\-]*\.""" + CFG_EXT + r""")(?![\w])""")
SRCCMD = re.compile(r"""(?m)^\s*(?:source|\.)\s+["']?([^\s"';|&)]+)""")
READERS = re.compile(r"readFileSync|readFile\(|open\(|dotenv|load_dotenv|json\.load|yaml\.safe_load|toml|source\s|\bcat\s|\bgrep\s|<\s*[\"$\w]")
SUFFIX = (".example", ".sample", ".template", ".tpl", ".dist", ".default", ".defaults")


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout


def is_test(p):
    return bool(re.search(r"(__tests__/|\.test\.|\.spec\.|/tests?/|(^|/)test_[^/]*$)", p))


def candidate_names(text):
    """basenames of files the code reads/sources (only when the file also shows a reader construct)."""
    out = {}
    if not READERS.search(text):
        return out
    for m in SRCCMD.finditer(text):
        b = os.path.basename(m.group(1).rstrip("/"))
        if b and "$" not in b and re.search(r"\.", b):
            out.setdefault(b, "source")
    for m in LIT.finditer(text):
        b = os.path.basename(m.group(1))
        if b and "$" not in b and "{" not in b and not b.endswith((".example", ".sample", ".template")):
            out.setdefault(b, "path literal")
    return out


def example_forms(b):
    low = b.lower(); stem = low.lstrip(".")
    forms = {low + s for s in SUFFIX} | {stem + s for s in SUFFIX}
    if "." in stem:
        n, e = stem.rsplit(".", 1)
        forms |= {f"{n}{s}.{e}" for s in SUFFIX} | {f"{n}.example.{e}", f"example.{stem}", f"{stem}.example"}
    if stem == "env" or stem.startswith("env."):
        forms |= {"env.example", ".env.example", "env.sample", ".env.sample", "env.template", ".env.template", ".env.dist", "env.dist"}
    return forms


def main():
    repo, head, out = sys.argv[1:4]
    fp = os.path.join(out, "facts.json")
    facts = json.load(open(fp))
    touched = [t["path"] for t in facts.get("touched_files", []) if not t["status"].startswith("D") and not is_test(t["path"])]
    tree = git(repo, "ls-tree", "-r", "--name-only", head).splitlines()
    byname = {}
    for p in tree:
        byname.setdefault(os.path.basename(p).lower(), []).append(p)
    found = []  # (rank, path, token, read_by)
    for t in touched:
        text = git(repo, "show", f"{head}:{t}")
        for tok, how in candidate_names(text).items():
            for form in example_forms(tok):
                for p in byname.get(form, []):
                    # nearer to the reading file = more likely the right sibling
                    pa, ta = os.path.dirname(p).split("/"), os.path.dirname(t).split("/")
                    common = 0
                    for x, y in zip(pa, ta):
                        if x != y: break
                        common += 1
                    found.append(((-common, len(pa) - common), p, tok, t, how))
    found.sort(key=lambda x: (x[0], x[1]))
    seen, chosen = set(), []
    for _, p, tok, t, how in found:
        if p in seen or p in touched:
            continue
        seen.add(p); chosen.append((p, tok, t, how))
    skipped = [c[0] for c in chosen[MAX_FILES:]]
    items = []
    for p, tok, t, how in chosen[:MAX_FILES]:
        n = len(git(repo, "show", f"{head}:{p}").splitlines())
        items.append({"path": p, "template_of": tok, "read_by": t, "found_via": how, "lines": n, "shown_lines": min(n, MAX_LINES), "truncated": n > MAX_LINES})
    facts["template_siblings"] = {"bounds": f"at most {MAX_FILES} files, {MAX_LINES} lines each", "included": items, "over_bound_not_included": skipped,
                                  "note": "shipped template/example siblings of files the touched non-test code reads or sources; empty list = none found"}
    json.dump(facts, open(fp, "w"), indent=1)
    print("template_siblings:", [i["path"] for i in items] or "none", ("(+%d over bound)" % len(skipped)) if skipped else "")


if __name__ == "__main__":
    main()
