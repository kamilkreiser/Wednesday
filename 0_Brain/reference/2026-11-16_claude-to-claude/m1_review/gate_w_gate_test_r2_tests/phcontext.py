"""Each new placeholder's context in the committed raw copies (body lines): which key/field it stands in."""
import re, sys, subprocess, collections
repo, commit = sys.argv[1:3]
files = subprocess.run(["git","-C",repo,"ls-tree","--name-only",commit,"spikes/W1-windows-exec-hook/raw/"],capture_output=True,check=True,text=True).stdout.split()
ctx = collections.Counter()
for f in files:
    lines = subprocess.run(["git","-C",repo,"show","%s:%s"%(commit,f)],capture_output=True,check=True,text=True).stdout.split("\n")
    for l in lines:
        if l.startswith("# "): continue
        for m in re.finditer(r"<(session-id|prompt-id|tool-use-id|event-uuid)>", l):
            pre = l[max(0,m.start()-40):m.start()]
            if re.search(r'"session_id"\s*:\s*"$', pre): k = "session_id field"
            elif re.search(r'projects\\\\[^"]*\\\\$', pre) and l[m.end():m.end()+6] == ".jsonl": k = "transcript_path ...\\<id>.jsonl"
            elif re.search(r'"prompt_id"\s*:\s*"$', pre): k = "prompt_id field"
            elif re.search(r'"(id|tool_use_id)"\s*:\s*"$', pre): k = re.search(r'"(id|tool_use_id)"\s*:\s*"$', pre).group(1) + " field"
            elif re.search(r'"uuid"\s*:\s*"$', pre): k = "uuid field"
            else: k = "OTHER: " + repr(pre[-30:])
            ctx[(m.group(0), k)] += 1
for k, v in sorted(ctx.items()): print("%-16s in %-34s x%d" % (k[0], k[1], v))
