"""Hash every tool in a lane's record raise/ folder and parse its matcher's MINE / OTHER_SEATS (by ast)."""
import ast, glob, hashlib, os, sys
for d in sys.argv[1:]:
    print("==", d)
    for f in sorted(glob.glob(d + "/*")):
        b = os.path.basename(f)
        if not (b.endswith(".py") or b.endswith(".sh")) or ".pre-" in b:
            continue
        data = open(f, "rb").read()
        print(f"  {hashlib.sha256(data).hexdigest()[:16]} {data.count(b'\n')} {b}")
    for f in glob.glob(d + "/inbox_match*.py"):
        if ".pre-" in f:
            continue
        t = ast.parse(open(f).read())
        for n in ast.walk(t):
            if isinstance(n, ast.Assign):
                names = [getattr(x, "id", "") for x in n.targets]
                if "MINE" in names:
                    print("  MINE", repr(ast.literal_eval(n.value)), "line", n.lineno)
                if "OTHER_SEATS" in names:
                    v = ast.literal_eval(n.value)
                    probe = ["r 18th", "r 17th", "e 11th", "e 10th", "g 4th", "g 3rd", "f 5th", "f 4th", "f 6th", "g 5th", "e 12th", "r 19th"]
                    print("  OTHER_SEATS", len(v), "line", n.lineno, {p: (p in v) for p in probe})
