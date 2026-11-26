# QA-POLICY-WORDS (k): search every test fn of crates/coagent-policy/tests/** at the head for a pin of
#   A: `Monitor` + `cat .env` with an exclusion state (a deny as on the exclusion list)
#   B: `grep -r key .` with the fixture HOME as working folder (the credential-folder refusal)
#   control C: `npm test` with the fixture HOME as working folder (the builder cites t25:1419)
# Method: split each file into top-level fn bodies; a fn is a candidate when its body holds all the needles of a
# query; each candidate is printed with the matching lines, then judged by reading.
import os, re, sys
ROOT = "/private/tmp/claude-501/qpw/head/crates/coagent-policy/tests"
Q = {
 "A Monitor cat .env + exclusion": [["\"Monitor\""], ["cat .env"], [".env*", "default_exclusions", "excl"]],
 "B grep -r key . from home": [["grep -r key ."], ["fx.home", ".home", "\"home\""]],
 "C npm test from home (control)": [["npm test"], ["fx.home", ".home", "\"home\""]],
}
files = []
for d, _, fs in os.walk(ROOT):
    files += [os.path.join(d, f) for f in fs if f.endswith(".rs")]
print("files searched:", len(files))
for name, groups in Q.items():
    print("==", name)
    for p in sorted(files):
        src = open(p).read()
        starts = [m.start() for m in re.finditer(r"(?m)^(?:pub )?fn \w+", src)] + [len(src)]
        for a, b in zip(starts, starts[1:]):
            body = src[a:b]
            if all(any(n in body for n in g) for g in groups):
                fn = re.match(r"(?:pub )?fn (\w+)", body).group(1)
                ln0 = src[:a].count("\n") + 1
                hits = [f"{ln0+i}: {l.strip()[:110]}" for i, l in enumerate(body.splitlines())
                        if any(n in l for g in groups[:2] for n in g)]
                print(f"  {os.path.relpath(p, ROOT)}::{fn} (line {ln0})")
                for h in hits[:12]: print("     ", h)
