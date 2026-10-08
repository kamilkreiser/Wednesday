import re, sys
flow = open(sys.argv[1], encoding="utf-8").read()
cheat = open(sys.argv[2], encoding="utf-8").read()
FR = re.compile(r"<h2[^>]*>\s*(\d+)\.", re.S)
nums = [int(m) for m in FR.findall(flow)]
# document-shaped control: copy the LAST real <h2 ...>N. record, renumber 99, split by newline
last = list(re.finditer(r"<h2[^>]*>\s*\d+\.[^<]*", flow, re.S))[-1].group(0)
ctrl = re.sub(r"(\d+)\.", "\n 99.", last, count=1)
cn = [int(m) for m in FR.findall(flow + ctrl)]
print("FLOW numbers:", len(nums), "dups:", sorted({n for n in nums if nums.count(n) > 1}), "tail:", nums[-8:])
print("FLOW control (planted 99 copied from last record):", 99 in cn, "count", len(cn))
print("FLOW absent 32..45:", [n for n in range(32, 46) if n not in nums])
H2 = re.compile(r"<h2[^>]*>(.*?)</h2>", re.S)
keys = []
for h in H2.findall(cheat):
    ks = re.findall(r"KS-\d+", h)
    keys.append(ks[-1] if ks else None)
keys2 = [k for k in keys if k]
print("CHEAT h2:", len(keys), "with key:", len(keys2), "dups:", sorted({k for k in keys2 if keys2.count(k) > 1}), "tail:", keys2[-10:])
lastc = [h for h in re.finditer(r"<h2[^>]*>.*?</h2>", cheat, re.S) if "KS-591" in h.group(0)]
ctrlc = lastc[-1].group(0).replace("KS-591", "KS-9999") if lastc else ""
k3 = [re.findall(r"KS-\d+", h)[-1] for h in H2.findall(cheat + ctrlc) if re.findall(r"KS-\d+", h)]
print("CHEAT control KS-9999 found:", "KS-9999" in k3, "present-key KS-591:", "KS-591" in keys2)
for k in ["KS-1274", "KS-1410", "KS-1139", "KS-1364", "KS-1171", "KS-593", "KS-808", "KS-1328", "KS-1355", "KS-1164", "KS-1450"]:
    print(" ", k, "sections:", keys2.count(k))
