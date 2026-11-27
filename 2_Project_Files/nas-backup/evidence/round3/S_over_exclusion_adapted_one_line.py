#!/usr/bin/env python3
# S_over_exclusion.py — what does the secret-SHAPE rule leave out of the real scope today? NAMES ONLY, read-only.
# It walks the real source sets with os.scandir exactly as the tool's walker does (same rule object, imported from
# a scratch COPY of nb_core.py), and RECORDS every entry the rule excludes as secret-shaped: its shape, whether it
# is a folder, its lower-cased name. It never descends into an excluded entry and never opens any file.
#   S_over_exclusion.py <scratch copy of the lane> <real conf (read)> <out detail file>
import os, sys, collections, re
lane, conf_path, detail = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, lane); sys.dont_write_bytecode = True
import nb_core
class Ctx(object): pass
ctx = Ctx(); ctx.info = nb_core.SEATS["wednesday"]; ctx.tree = "/Volumes/DevMASTER/WEDNESDAY"; ctx.state_dir = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup/state"  # R3-SEAT: round 3 Rules reads this
c = {"sets": [], "exclude_name": [], "exclude_name_in": [], "exclude_path": []}
for ln in open(conf_path, encoding="utf-8").read().split("\n"):
    ln = ln.strip()
    if not ln or ln.startswith("#") or ln.startswith("END ") or "=" not in ln: continue
    k, v = [x.strip() for x in ln.split("=", 1)]
    if k == "set":
        p = v.split("|"); c["sets"].append({"client": p[0], "dest": p[1], "src": p[2]})
    elif k == "exclude_name": c["exclude_name"].append(v)
    elif k == "exclude_name_in":
        p = v.split("|"); c["exclude_name_in"].append((p[0], p[1]))
    elif k == "exclude_path":
        p = v.split("|"); c["exclude_path"].append((p[0], p[1].strip("/")))
ctx.conf = c
print("sets: %d ; exclude_path: %d ; exclude_name_in: %d" % (len(c["sets"]), len(c["exclude_path"]), len(c["exclude_name_in"])))
by_shape = collections.Counter(); names = collections.defaultdict(collections.Counter); dirs = collections.Counter(); in_scope = 0
other = collections.Counter(); rows = []
for s in c["sets"]:
    rules = nb_core.Rules(ctx, s)
    stack = [("", s["src"])]
    while stack:
        rel, path = stack.pop()
        try:
            it = os.scandir(path)
        except OSError as e:
            other["scandir-error"] += 1; continue
        with it:
            for e in it:
                r = e.name if not rel else rel + "/" + e.name
                try:
                    is_link = e.is_symlink(); is_dir = (not is_link) and e.is_dir(follow_symlinks=False)
                except OSError:
                    other["stat-error"] += 1; continue
                m = rules.match(e.name, r, is_dir)
                if m:
                    if m[0] == "secret":
                        by_shape[m[1]] += 1; names[m[1]][e.name.lower()] += 1
                        if is_dir: dirs[m[1]] += 1
                        rows.append("%s\t%s\t%s\t%s" % (m[1], "DIR" if is_dir else "file", s["dest"], r))
                    else:
                        other[m[0]] += 1
                    continue
                if is_dir: stack.append((r, e.path))
                elif not is_link: in_scope += 1
with open(detail, "w", encoding="utf-8", errors="surrogateescape") as fh:
    fh.write("\n".join(sorted(rows)) + "\n")
print("in-scope files seen by this walk (before the hard-link rule): %d" % in_scope)
print("other exclusions (control that the walk applies the same rules): %s" % dict(other))
print("EXCLUDED AS SECRET-SHAPED: %d entries in total" % sum(by_shape.values()))
def klass(shape, n):
    if shape == "env-file":
        if re.search(r"\.(example|sample|template|tmpl|dist|defaults?|schema|test|ci)(\.|$)", n) or n.endswith(".example"): return "template/example env (not a secret by convention)"
        if n == ".envrc": return ".envrc"
        if n in (".env",) or re.match(r"^\.env\.[a-z0-9_-]+$", n): return "real env file (.env, .env.<stage>)"
        if n.startswith(".env"): return "other name starting .env"
        return "other (*.env, *.env.*)"
    if shape == "key-or-certificate":
        m = re.search(r"\.(pem|key|p12|pfx|ppk|jks|keystore|kdbx|skey)", n); return "extension ." + (m.group(1) if m else "?")
    if shape == "ssh-key": return "public half (.pub)" if n.endswith(".pub") else "private-shaped"
    return n if shape in ("credential-file", "credential-store", "credentials-folder-name", "terraform-state") and names[shape][n] >= 3 else "(other names)"
for shape in sorted(by_shape, key=lambda k: -by_shape[k]):
    print("  %-26s %6d entries (%d of them folders, whose whole content is left out)" % (shape, by_shape[shape], dirs[shape]))
    k = collections.Counter()
    for n, v in names[shape].items(): k[klass(shape, n)] += v
    for kk, v in k.most_common(14): print("        %6d  %s" % (v, kk))
    print("        most common names: %s" % "; ".join("%s x%d" % kv for kv in names[shape].most_common(10)))
print("detail (shape, kind, set, path): %s" % detail)
