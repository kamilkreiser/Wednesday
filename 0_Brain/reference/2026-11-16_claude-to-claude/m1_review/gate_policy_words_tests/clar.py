# QA-POLICY-WORDS (n): C-20..C-22 against the lane brief's A11 quotes, lengths, and the before-copy as byte prefix
import re
CL = "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/1_Project_Definition/CLARIFICATIONS.md"
BEF = "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools/tmp/pwo/4c6725/h/CLARIFICATIONS.before.md"
BR = "/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-11-26_coagent_POLICY-WORDS_brief.md"
cl, bef, br = open(CL, "rb").read(), open(BEF, "rb").read(), open(BR, encoding="utf-8").read()
print("before is byte prefix of now:", cl.startswith(bef), "| lines before/now:", bef.count(b"\n"), cl.count(b"\n"))
a11 = br[br.index("## A11."):]
quotes = re.findall(r'verbatim: "(Decision [^"]+)"', a11)
counts = [int(x) for x in re.findall(r"(\d+) characters by the board's count", a11)]
txt = cl.decode("utf-8")
for n, q, want in zip((20, 21, 22), quotes, counts):
    sec = txt[txt.index(f"## C-{n} —"):]
    nxt = sec.find("\n## ", 5); sec = sec if nxt < 0 else sec[:nxt]
    m = re.search(r"\n> (.*)\n?", sec)
    got = m.group(1)
    print(f"C-{n}: exists; equal to A11 text: {got == q}; length {len(got)} (board {want}, A11 text {len(q)})")
