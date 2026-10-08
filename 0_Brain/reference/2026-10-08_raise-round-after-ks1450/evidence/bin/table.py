import json, sys
m = json.load(open(sys.argv[1]))
for k, r in m.items():
    fs = ", ".join(f.replace("Blockchain/Dev/services/", "svc/").replace("Blockchain/Dev/", "Dev/") for f in r.get("files", []))
    secs = " ".join(("F" if x["fwd"] == 0 else "f") + ("R" if x["rev"] == 0 else "r") for x in r.get("sections", []))
    print(f'{k}|{r.get("bytes")}|{r.get("sha16")}|{r.get("tree")}|{secs}|{fs}')
