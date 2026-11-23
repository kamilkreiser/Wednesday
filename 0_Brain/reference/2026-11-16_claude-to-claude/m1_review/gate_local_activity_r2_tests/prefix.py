"""Merge check: main's file must be a byte-for-byte prefix of the head's, and the lane's own appended
part (the r1 head's addition over the old base) must be what follows, possibly with later lane lines.
usage: python3 -B prefix.py <clone> <main sha> <head sha> <old base sha> <r1 head sha> <path>..."""
import subprocess, sys
clone, M, H, B, O = sys.argv[1:6]
def blob(sha, p):
    return subprocess.run(["git", "-C", clone, "show", f"{sha}:{p}"], capture_output=True, check=True).stdout
bad = 0
for p in sys.argv[6:]:
    m, h, b, o = blob(M, p), blob(H, p), blob(B, p), blob(O, p)
    pre = h.startswith(m)
    ctl = bytearray(m); ctl[len(ctl)//2] ^= 1
    ctl_pre = h.startswith(bytes(ctl))
    mine_r1 = o[len(b):] if o.startswith(b) else None
    rest = h[len(m):]
    print(f"{p}: main {len(m)} B, head {len(h)} B, main is a byte prefix of head: {pre}; control (one byte flipped in main): {ctl_pre}")
    print(f"   base {len(b)} B is prefix of main: {m.startswith(b)}; of r1 head: {o.startswith(b)}; r1 lane part {len(mine_r1) if mine_r1 is not None else 'n/a'} B; head's part after main {len(rest)} B")
    for tag in (b"<<<<<<<", b">>>>>>>", b"\n=======\n"):
        if tag in h: print("   CONFLICT MARKER", tag); bad += 1
    if not pre or ctl_pre: bad += 1
    # lines of either side dropped?
    hl = set(h.split(b"\n"))
    for side, data in (("main", m), ("r1-lane", mine_r1 or b"")):
        miss = [l for l in data.split(b"\n") if l not in hl]
        print(f"   {side} lines absent from head: {len(miss)}", [x[:80] for x in miss[:5]])
    sys.stdout.flush()
    print("   head's appended part (first 200 bytes):", rest[:200])
sys.exit(1 if bad else 0)
