# QA-POLICY-B item 3, the sliding real corpus: every 1 200-character window (step 600) of every tracked text file of
# the repository at the head, and of `git log -p` of its last 200 commits, as a web fetch's prompt and as a search.
# Row ids carry the file and offset only. python3 -B mk_sliding.py <repo> <out.jsonl>
import json, subprocess, sys
R, OUT = sys.argv[1], sys.argv[2]
H = "cd7b6fdd1a4b2de5937795b052a68d793146eb6d"
files = subprocess.run(["git", "-C", R, "ls-tree", "-r", "--name-only", H], capture_output=True, text=True).stdout.split("\n")
n_files = n_text = n_win = 0
with open(OUT, "w") as f:
    def windows(name, text):
        global n_win
        k = 0
        while True:
            w = text[k:k + 1200]
            if not w.strip(): break
            for tool in ("WebFetch", "WebSearch"):
                inp = {"url": "https://example.com/", "prompt": w} if tool == "WebFetch" else {"query": w}
                f.write(json.dumps({"id": f"{name}@{k}:{tool}", "tool": tool, "input": inp}, ensure_ascii=False) + "\n")
            n_win += 1
            if k + 1200 >= len(text): break
            k += 600
    for p in files:
        if not p: continue
        n_files += 1
        b = subprocess.run(["git", "-C", R, "show", f"{H}:{p}"], capture_output=True).stdout
        if b"\0" in b[:8000]: continue
        try: t = b.decode("utf-8")
        except UnicodeDecodeError: continue
        n_text += 1
        windows(p, t)
    log = subprocess.run(["git", "-C", R, "log", "-p", "-200", H], capture_output=True).stdout.decode("utf-8", "replace")
    windows("<git log -p -200>", log)
print(f"files {n_files}, text files {n_text}, windows {n_win} (each through two tools)")
