import sys
f, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(f).read()
n = s.count(old)
assert n == 1, f"{n} matches for {old!r}"
open(f, 'w').write(s.replace(old, new))
print("mutated", f)
