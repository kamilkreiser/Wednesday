#!/usr/bin/env python3
"""stamp_paths_check.py <brief.md> <owner/repo> <ref> --gh-config <dir> [--root <prefix>] [--show N]

Re-derives every repository PATH and path:LINE pointer a brief cites, at the pinned ref, BEFORE Tuesday stamps it.
GET only (GitHub git/trees + raw contents through `gh api`); nothing is cloned, fetched or written anywhere.

WHY (ledger _ledger_laptop_datasec.md, w=3 in two days, promoted 2026-10-29): approved text whose POINTERS were
wrong — a line number (B875 csp-helpers.js 93 vs 97, 10-28 07:08), a figure (B880, 10-28 08:40) and a PATH
(B884 T04: `components/shell/AppShellFeedback.test.tsx`, the tree has it only under `components/feedback/`,
10-29 10:26). The stamping step re-derived the four LINES it chose and none of ~120 PATHS. This checks them all.

What counts as a pointer: a backticked or bare token ending in a source/doc extension, optional `:N` / `:N-M`
(cite lines with a colon; "lines N-M" after a path is not parsed). Verdicts — only the first four FAIL (rc 1):
  WRONG-DIR      the file exists in the tree but not where the brief puts it (the T04 shape). A bare name is
                 held to the directory of the list it sits in: the path before it in a ';' run of pure list
                 items, or an explicit "(all under X/)". A full path with a name found <=2 times elsewhere.
  LINE-PAST-EOF  a cited line beyond the file's length.
  AMBIGUOUS      a short path that ends several tree paths, not all named in the brief.
  MISSING-LOCAL  an absolute local path whose parent directory is missing too.
  OK             resolves (exact, under --root, or a unique suffix).
  NEW-OR-OUT-OF-REPO  printed as one list for a HUMAN read, never a failure: a file the work CREATES, an absence
                 pin, a project-folder path (Briefs/, CLARIFICATIONS, .tools/), or a generic name (page.tsx).
A pointer that resolves to the RIGHT file at the WRONG line (B875: 93 vs 97) is not detectable by existence:
--show N prints the first N cited lines so the stamping read compares the text. Run it with --show at least
for every line the approved Jira/PR text cites.
Usage at stamp time (before stamp_brief.py; the ref is the sha the kit pins, never a branch name):
  python3 -I tuesday/tools/stamp_paths_check.py <kit> datasecau/<repo> <sha> --gh-config '<project>/4_Credentials/.gh-config' [--root ""] --show 20
Arms: tests/stamp_paths_check_arms.sh (red on the B884 pre-stamp T04 text, green on its corrected path).
"""
import argparse, base64, json, os, re, subprocess, sys

EXT = re.compile(r"\.(ts|tsx|js|jsx|mjs|cjs|py|sh|md|json|ya?ml|css|scss|html|sql|txt|toml|cs|go|bicep|tf|ps1|env)$", re.I)
TOKEN = re.compile(r"`([^`\n]{3,200})`|(?<![\w/.`'\-])((?:[\w.@-]+/)*[\w.@-]+\.[A-Za-z]{1,5})(?::(\d+)(?:-(\d+))?)?(?![\w/])")
DIRTOK = re.compile(r"(?<![\w.])((?:[\w.@-]+/)+)(?=[\s;,)]|$)")
UNDER = re.compile(r"\b(?:all|each|every one|both)(?: of them| files)? (?:live |are |sit )?under `?((?:[\w.@-]+/)*[\w.@-]+/)`?", re.I)
PURE = re.compile(r"\s*(?:- )?(?:`[^`]*`\s*=\s*)?(?:[\w ]{0,12}:\s*)?`?(?:[\w.@-]+/)*[\w.@-]+\.[A-Za-z]{1,5}`?(?::\d+(?:-\d+)?)?\s*(?:\([^)]*\))?\s*[.,]?\s*")
LINEPART = re.compile(r"^(.*?):(\d+)(?:-(\d+))?$")


def gh(args, cfg):
    env = dict(os.environ, GH_CONFIG_DIR=cfg)
    r = subprocess.run(["gh", "api"] + args, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        sys.exit(f"stamp_paths_check: gh api {' '.join(args)} failed rc {r.returncode}: {r.stderr.strip()[:300]}")
    return r.stdout


def tree(repo, ref, cfg):
    d = json.loads(gh([f"repos/{repo}/git/trees/{ref}?recursive=1"], cfg))
    if d.get("truncated"):
        sys.exit("stamp_paths_check: REFUSED — the tree listing is TRUNCATED, so a MISSING would be a false absence")
    return [e["path"] for e in d["tree"] if e["type"] == "blob"]


def lines_of(repo, ref, path, cfg, cache):
    if path not in cache:
        d = json.loads(gh([f"repos/{repo}/contents/{path}?ref={ref}"], cfg))
        if d.get("encoding") == "base64" and d.get("content") is not None:
            raw = base64.b64decode(d["content"])
        else:  # large files: the blob API
            b = json.loads(gh([f"repos/{repo}/git/blobs/{d['sha']}"], cfg))
            raw = base64.b64decode(b["content"])
        cache[path] = raw.decode("utf-8", "replace").split("\n")
    return cache[path]


def candidates(text):
    """{(token, a, b): (brief line, the dirs named on that line)} for every path-shaped token."""
    seen = {}
    lines = text.split("\n")
    for i, ln in enumerate(lines, 1):
        under = [d if d.endswith("/") else d + "/" for d in UNDER.findall(ln)]
        ctx = None  # the parent dir of the previous ';' item, carried through a chain of bare names
        for seg in ln.split(";"):
            pure = bool(PURE.fullmatch(seg))
            if not pure:
                ctx = None  # prose breaks the chain: only a run of bare list items inherits a directory
            seg_ctx = ctx
            for m in TOKEN.finditer(seg):
                if m.group(1) is not None:
                    tok, a, b = m.group(1).strip(), None, None
                    lm = LINEPART.match(tok)
                    if lm:
                        tok, a, b = lm.group(1), lm.group(2), lm.group(3)
                else:
                    tok, a, b = m.group(2), m.group(3), m.group(4)
                tok = tok.strip().strip("'\"").rstrip(".,;)")
                if " " in tok or tok.startswith(("http", "-", "$", "~")) or any(c in tok for c in "*<{='"):
                    continue
                if not EXT.search(tok):
                    continue
                if "/" in tok:
                    seg_ctx = tok.rsplit("/", 1)[0] + "/"
                    scope = []
                else:
                    scope = under + ([ctx] if ctx else [])
                seen.setdefault((tok, a, b), (i, scope))
            ctx = seg_ctx if pure else None
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief"); ap.add_argument("repo"); ap.add_argument("ref")
    ap.add_argument("--gh-config", required=True)
    ap.add_argument("--root", default="web/src/", help="prefix the brief's short paths are written from (default web/src/)")
    ap.add_argument("--show", type=int, default=0)
    ap.add_argument("--project-dir", default="", help="the project folder: relative paths outside the repo (session-tools/, "
                    "1_Project_Definition/Briefs/) are checked for existence there, read-only")
    o = ap.parse_args()
    text = open(o.brief, encoding="utf-8").read()
    paths = tree(o.repo, o.ref, o.gh_config)
    pset = set(paths)
    by_base = {}
    for p in paths:
        by_base.setdefault(p.rsplit("/", 1)[-1], []).append(p)
    cache, bad, shown, counts, info = {}, 0, 0, {}, []

    def tally(k):
        counts[k] = counts.get(k, 0) + 1

    for (tok, a, b), (at, dirs) in sorted(candidates(text).items(), key=lambda kv: kv[1][0]):
        if tok.startswith("/"):
            if not tok.startswith(("/Volumes/", "/Users/", "/private/", "/tmp/", "/opt/")):
                tally("NEW-OR-OUT-OF-REPO"); info.append(f"brief:{at} {tok} (absolute, not a local root: a container path?)")
                continue
            if not os.path.exists(tok):
                if os.path.isdir(os.path.dirname(tok.rstrip("/"))):
                    tally("NEW-OR-OUT-OF-REPO"); info.append(f"brief:{at} {tok} (parent dir exists)")
                else:
                    bad += 1; tally("MISSING-LOCAL"); print(f"MISSING-LOCAL brief:{at}  {tok}  (parent dir missing too)")
            else:
                tally("OK")
            continue
        rel = tok[2:] if tok.startswith("./") else tok
        if rel.startswith("2_Project_Files/"):  # this workspace's layout: the repo IS <project>/2_Project_Files
            rel = rel[len("2_Project_Files/"):]
        if o.project_dir and rel not in pset and o.root + rel not in pset:
            for base in ("", "1_Project_Definition/"):
                if os.path.exists(os.path.join(o.project_dir, base, rel)):
                    rel = None; break
            if rel is None:
                tally("OK-LOCAL"); continue
        full, verdict = None, "OK"
        for c in [rel, o.root + rel]:
            if c in pset:
                full = c; break
        if not full and "/" in rel:
            hits = [p for p in paths if p.endswith("/" + rel)]
            if len(hits) == 1:
                full = hits[0]
            elif len(hits) > 1:
                if sum(1 for h in hits if h in text) != 1 and not all(h in text for h in hits):
                    bad += 1; tally("AMBIGUOUS"); print(f"AMBIGUOUS brief:{at}  {tok}  -> {', '.join(hits[:5])}")
                else:
                    tally("OK")
                continue
        if not full and "/" not in rel:
            where = by_base.get(rel, [])
            if not where:
                tally("NEW-OR-OUT-OF-REPO"); info.append(f"brief:{at} {tok}"); continue
            # a bare name inside a scoped list ("a/b/x.ts; y.ts" or "(all under a/b/)") must live there (the T04 shape)
            scoped = [w for w in where if any(("/" + d.strip("/") + "/") in ("/" + w) for d in dirs)]
            if dirs and not scoped:
                bad += 1; tally("WRONG-DIR")
                print(f"WRONG-DIR brief:{at}  {tok}  — the line names {sorted(set(dirs))}; the tree has it at: {', '.join(where[:4])}")
                continue
            full = (scoped or where)[0]
            named = [w for w in (scoped or where) if w in text]
            if len(named) == 1:
                full = named[0]
            elif len(scoped or where) > 1 and a:
                bad += 1; tally("AMBIGUOUS"); print(f"AMBIGUOUS brief:{at}  {tok}:{a}  -> {', '.join((scoped or where)[:5])}")
                continue
        if not full:
            bn = rel.rsplit("/", 1)[-1]
            where = by_base.get(bn, [])
            if where and len(where) <= 2:
                bad += 1; tally("WRONG-DIR"); print(f"WRONG-DIR brief:{at}  {tok}  — the tree has {bn} at: {', '.join(where[:4])}")
            elif where:  # a generic name (page.tsx, index.ts) lives everywhere: an absence pin or a new file, read it
                tally("NEW-OR-OUT-OF-REPO"); info.append(f"brief:{at} {tok} (generic name, {len(where)} elsewhere)")
            else:
                tally("NEW-OR-OUT-OF-REPO"); info.append(f"brief:{at} {tok}")
            continue
        if a:
            L = lines_of(o.repo, o.ref, full, o.gh_config, cache)
            n = len(L) - (1 if L and L[-1] == "" else 0)
            if int(b or a) > n:
                bad += 1; tally("LINE-PAST-EOF")
                print(f"LINE-PAST-EOF brief:{at}  {full}:{a}{'-' + b if b else ''}  (file has {n} lines)")
                continue
            if shown < o.show:
                shown += 1; print(f"SHOW     brief:{at}  {full}:{a}  | {L[int(a) - 1].strip()[:160]}")
        tally(verdict)
    if info:
        print("NEW-OR-OUT-OF-REPO (not in the tree, basename nowhere: a file the work CREATES, or a project-folder path; read each): "
              + "; ".join(info[:40]) + (" ..." if len(info) > 40 else ""))
    summary = " ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    print(f"stamp_paths_check: {o.repo}@{o.ref[:8]} tree {len(paths)} files · {summary} · rc {1 if bad else 0}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
