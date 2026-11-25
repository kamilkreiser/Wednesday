# QA-POLICY-NOTES: positional line comparison of two differential outputs (same structure). Prints the number of
# differing line pairs, how many hold the plant string on the new side, and the kind of line (decide / mode column).
import sys
a, b, plant = sys.argv[1], sys.argv[2], sys.argv[3].encode()
n = d = hold = dec = col = other = 0
with open(a, "rb") as fa, open(b, "rb") as fb:
    for la, lb in zip(fa, fb):
        n += 1
        if la != lb:
            d += 1
            hold += plant in lb
            if lb.startswith(b" s"): dec += 1
            elif lb.startswith(b"  "): col += 1
            else: other += 1
print(f"lines {n} differing {d} holding-plant {hold} decide-lines {dec} column-lines {col} other {other}")
