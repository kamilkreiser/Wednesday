# plant.py <src dir copy> <file> <after line number> <python-literal text>: insert text after that line.
import sys, ast
d, f, n, t = sys.argv[1], sys.argv[2], int(sys.argv[3]), ast.literal_eval(sys.argv[4])
p = d + "/" + f; L = open(p, encoding="utf-8").read().split("\n")
L.insert(n, t); open(p, "w", encoding="utf-8").write("\n".join(L)); print("planted", repr(t), "in", f, "after line", n)
