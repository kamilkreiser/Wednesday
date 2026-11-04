# gate 194: sha12 (first 8 hex of sha256) of every "unreadable thrown value" guard block in credentialRepo.ts, at base and head
# (blobs from git), plus a planted one-character control. Window (gate 191's, as the seat states it): from the nearest preceding
# line matching `} catch (err` through the line AFTER the 'unreadable thrown value' line.
import hashlib, re, subprocess
R = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959/repo"
P = "Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts"
def blocks(text):
    L = text.split("\n"); out = []
    for i, l in enumerate(L):
        if "'unreadable thrown value'" in l:
            j = i
            while j >= 0 and not re.match(r"^\s*\} catch \(err", L[j]): j -= 1
            out.append((j + 1, i + 2, hashlib.sha256("\n".join(L[j:i + 2]).encode()).hexdigest()[:8]))
    return out
for rev in ("e899463d2a0b1b30f2cff46b23d001622620029a", "a968818a0038727399663775722017c130d4cb08"):
    t = subprocess.run(["git", "-C", R, "show", f"{rev}:{P}"], capture_output=True, text=True, check=True).stdout
    print(rev[:12], len(blocks(t)), [f"{a}-{b}:{h}" for a, b, h in blocks(t)])
    if rev.startswith("a968"):
        head = t
L = head.split("\n")
k = next(i for i, l in enumerate(L) if "'unreadable thrown value'" in l)
L[k] = L[k].replace("reason", "reasom", 1)
print("planted (1 char: reason->reasom on the first guard's marker line)", [f"{a}-{b}:{h}" for a, b, h in blocks("\n".join(L))])
