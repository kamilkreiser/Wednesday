import re, sys
CLASSES = {
 "account name": r"kamil|kreis|\bkam\b",
 "home path": r"/Users/|C:\\\\?Users\\\\?|/home/",
 "machine name": r"smashhome|DESKTOP-[A-Z0-9]+|LAPTOP-[A-Z0-9]+",
 "token": r"sk-ant-[A-Za-z0-9_-]+|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|Bearer [A-Za-z0-9._-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY",
 "session id (uuid)": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
 "mail address": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
 "network address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b|\b[0-9a-f]{1,4}(?::[0-9a-f]{1,4}){7}\b",
 "helper work folder": r"C:\\\\?c2c|C:/c2c|C--c2c|\bc2c\\\\",
 "volume / laptop path": r"/Volumes/|Laptop-DEV",
}
lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
for name, rx in CLASSES.items():
    hits = [l for l in lines if re.search(rx, l, re.I if name not in ("session id (uuid)",) else 0)]
    print("%-20s %5d" % (name, len(hits)))
    for h in hits[:4]:
        m = re.search(rx, h, re.I if name != "session id (uuid)" else 0)
        print("      ", repr(h[max(0, m.start()-60):m.end()+40]))
