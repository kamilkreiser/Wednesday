# QA-AUDIT-HOST-NOTES-R2 item 10: runs bytescan.py with the words of a words file (kept out of the
# verdict), over the inputs, then over two planted controls. Usage: python3 -B -I scanrun.py <scan dir>
import subprocess, sys
S = sys.argv[1]; B = "/private/tmp/claude-501/qahn2/bin/bytescan.py"
words = [w for w in open(S + "/words.txt").read().split("\n") if w]
src = open(S + "/notes_docs.rs.head").read()
open(S + "/plant_line.rs", "w").write(src + "\n// planted: /Volumes/Laptop-DEV/!CODING/x by Kreiser\n")
open(S + "/plant.bin", "wb").write(b"\x00\xff\xfeKAMIL\x00\x01laptop-dev\xff\x00")
ins = [S + "/added_lines.txt", S + "/BACKLOG.md.head", S + "/AUDIT-HOST.md.head", S + "/notes_docs.rs.head"]
r = subprocess.run(["python3", "-B", "-I", B] + ins + ["--"] + words, capture_output=True, text=True)
print("INPUTS:", r.stdout.strip().replace(S, "<scan>"), "rc", r.returncode)
r = subprocess.run(["python3", "-B", "-I", B, S + "/plant_line.rs", S + "/plant.bin", "--"] + words, capture_output=True, text=True)
print("CONTROLS:", r.stdout.strip().replace(S, "<scan>").count("HIT"), "hit lines;", r.stdout.strip().splitlines()[-1], "rc", r.returncode)
for f in ins:
    n = sum(1 for l in open(f, errors="replace") if __import__("re").search(r"(?i)\bkam\b", l))
    print("short name whole word in", f.replace(S, "<scan>"), n)
print("short name control:", sum(1 for l in ["planted kam here"] if __import__("re").search(r"(?i)\bkam\b", l)))
