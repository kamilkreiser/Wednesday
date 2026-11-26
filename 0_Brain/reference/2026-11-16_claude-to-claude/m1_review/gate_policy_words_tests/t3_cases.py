# QA-POLICY-WORDS (f): T-3's spellings by cargo itself, and the head's depends_on_policy on the same texts.
# usage: python3 -B -I t3_cases.py <work folder> <function binary>
import json, os, subprocess, sys
WORK, FN = sys.argv[1], sys.argv[2]
P = 'path = "../coagent-policy"'
CASES = [
 ("lane1-top-deps", 'dependencies = { coagent-policy = { ' + P + ' } }'),
 ("lane2-top-dev", 'dev-dependencies = { coagent-policy = { ' + P + ' } }'),
 ("lane3-top-build", 'build-dependencies = { coagent-policy = { ' + P + ' } }'),
 ("lane4-target-inline", "[target.'cfg(unix)']\ndependencies = { coagent-policy = { " + P + " } }"),
 ("control-no-line", ""),
 ("neg1-nested-key", 'dependencies = { x = { coagent-policy = 1 } }'),
 ("neg2-value-string", 'dependencies = { x = "coagent-policy" }'),
 ("neg3-workspace", '[workspace]\ndependencies = { coagent-policy = { ' + P + ' } }'),
 ("neg4-package", '[package]\ndependencies = { coagent-policy = { ' + P + ' } }'),
 ("neg5-target-other", "[target.'cfg(unix)']\nother = { coagent-policy = 1 }"),
 ("my1-target-dev-inline", "[target.'cfg(unix)']\ndev-dependencies = { coagent-policy = { " + P + " } }"),
 ("my2-quoted-key", 'dependencies = { "coagent-policy" = { ' + P + ' } }'),
 ("my3-second-key", 'dependencies = { serde = { version = "1", optional = true }, coagent-policy = { ' + P + ' } }'),
 ("my4-renamed-inline", 'dependencies = { p = { package = "coagent-policy", ' + P + ' } }'),
 ("my5-dotted-in-inline", 'dependencies = { coagent-policy.path = "../coagent-policy" }'),
 ("my6-tight", 'dependencies={coagent-policy={path="../coagent-policy"}}'),
 ("my7-top-dotted-target-inline", "target.'cfg(unix)'.dependencies = { coagent-policy = { " + P + " } }"),
 ("my8-underscore-dev", 'dev_dependencies = { coagent-policy = { ' + P + ' } }'),
 ("my9-trailing-comment", 'dependencies = { coagent-policy = { ' + P + ' } } # c'),
 ("my10-single-quoted-key", "dependencies = { 'coagent-policy' = { " + P + " } }"),
 ("my11-target-triple-build", "[target.x86_64-unknown-linux-gnu]\nbuild-dependencies = { coagent-policy = { " + P + " } }"),
 ("my12-multiline-inline", 'dependencies = {\n  serde = "1",\n  coagent-policy = { ' + P + ' },\n}'),
 ("my13-key-in-string-value", 'dependencies = { x = { path = "../x", features = ["coagent-policy = 1"] } }'),
 ("my14-target-renamed-inline", "[target.'cfg(unix)']\ndependencies = { p = { package = \"coagent-policy\", " + P + " } }"),
 ("my15-workspace-true", 'dependencies = { coagent-policy = { workspace = true } }'),
]
def manifest(text):
    pkg = '[package]\nname = "x"\nversion = "0.0.0"\nedition = "2021"\n'
    if text.startswith("[package]"):
        return pkg + text[len("[package]\n"):] + "\n[lib]\npath = \"lib.rs\"\n"
    lines = text.split("\n") if text else []
    first = next((i for i, l in enumerate(lines) if l.lstrip().startswith("[")), len(lines))
    top, rest = lines[:first], lines[first:]
    return "\n".join(top + [pkg.rstrip("\n"), '[lib]', 'path = "lib.rs"'] + rest) + "\n"
res = []
for name, text in CASES:
    d = os.path.join(WORK, name); os.makedirs(d + "/x", exist_ok=True); os.makedirs(d + "/coagent-policy/src", exist_ok=True)
    open(d + "/coagent-policy/Cargo.toml", "w").write('[package]\nname = "coagent-policy"\nversion = "0.0.1"\nedition = "2021"\n')
    open(d + "/coagent-policy/src/lib.rs", "w").write("")
    for extra in ("x",):  # renamed / nested cases may reference ../x
        pass
    m = manifest(text); open(d + "/x/Cargo.toml", "w").write(m); open(d + "/x/lib.rs", "w").write("")
    p = subprocess.run(["cargo", "metadata", "--offline", "--no-deps", "--format-version", "1", "--manifest-path", d + "/x/Cargo.toml"],
                       capture_output=True, text=True)
    if p.returncode != 0:
        cargo = "error: " + " ".join(l.strip() for l in p.stderr.strip().splitlines() if l.strip().startswith(("error", "Caused", "caused", "|")) )[:160]
        dep = None
    else:
        meta = json.loads(p.stdout)
        x = [q for q in meta["packages"] if q["name"] == "x"][0]
        ds = [q for q in x["dependencies"] if q["name"] == "coagent-policy"]
        dep = bool(ds)
        cargo = ("dependent " + ", ".join(f"kind={q['kind'] or 'normal'} target={q['target']} rename={q.get('rename')}" for q in ds)) if ds else "not a dependent"
        warns = [l.strip() for l in p.stderr.splitlines() if "warning" in l]
        if warns: cargo += " | " + "; ".join(warns)[:140]
    f_bare = subprocess.run([FN], input=text, capture_output=True, text=True).stdout.strip()
    f_full = subprocess.run([FN], input=m, capture_output=True, text=True).stdout.strip()
    verdict = ("MISS" if dep and "false" in (f_bare, f_full) else "FALSE POSITIVE" if (dep is not True) and "true" in (f_bare, f_full) else "agree")
    res.append((name, text, f_bare, f_full, cargo, verdict))
    print(f"{name}\t{json.dumps(text)}\tfn(bare)={f_bare}\tfn(manifest)={f_full}\tcargo: {cargo}\t=> {verdict}")
