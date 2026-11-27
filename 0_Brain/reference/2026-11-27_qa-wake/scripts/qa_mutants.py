import os, shutil, subprocess, sys
sys.dont_write_bytecode = True
LANE = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/wake"
REAL = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files"
SCR = sys.argv[1]
M = [
 ("Q01 rename order swapped: state first, archive second", [("handover_core.py",
   "        if new_arch is not None:\n            os.replace(tmps[0], arch_path)\n        os.replace(t2, state_path)\n",
   "        os.replace(t2, state_path)\n        if new_arch is not None:\n            os.replace(tmps[0], arch_path)\n")], "HS"),
 ("Q02 changed-on-disk-during-write check removed", [("handover_core.py",
   "        if read_bytes(state_path) != cur or read_bytes(arch_path) != prev_arch:", "        if False:")], "HS"),
 ("Q03 temp-file read-back checks removed", [("handover_core.py", "            if read_bytes(t) != new_arch:", "            if False:"),
   ("handover_core.py", "        if read_bytes(t2) != new_state:", "        if False:")], "HS"),
 ("Q04 cap off by one: a block of exactly cap bytes refused", [("handover_core.py", "    if len(block) > cap:", "    if len(block) >= cap:")], "HS"),
 ("Q05 trailing newline no longer ensured on the block", [("handover_core.py",
   "    if block.strip() and not block.endswith(b\"\\n\"):\n        block += b\"\\n\"\n", "")], "HS"),
 ("Q06 seat guard blinded to WED_AGENT (unset before the guard)", [("handover.sh",
   "seat_note_dir \"$TREE\" handover || exit 2", "unset WED_AGENT; seat_note_dir \"$TREE\" handover || exit 2")], "HS"),
 ("Q07 dead marker without word boundary (DEADLINE..., CLOSEDOWN... dropped)", [("wake_pack.py",
   "        if re.match(re.escape(w) + r\"\\b\", l1):", "        if l1.startswith(w):")], "W"),
 ("Q08 other-seat match needs no separator (TUESDAY 2026-.. kick-off: dropped)", [("wake_pack.py",
   "r\"(%s)\\b\\s*(?::|\\(|—|–|-|,)\"", "r\"(%s)\\b\"")], "W"),
 ("Q09 budget counts characters, not bytes", [("wake_pack.py",
   "            rows.append((title.split(\".\")[0], s[\"label\"], s[\"src_bytes\"], len(s[\"text\"].encode(\"utf-8\"))))",
   "            rows.append((title.split(\".\")[0], s[\"label\"], s[\"src_bytes\"], len(s[\"text\"])))"),
   ("wake_pack.py", "    body_b = len(body.encode(\"utf-8\"))", "    body_b = len(body)"),
   ("wake_pack.py", "        new_total = len(head.encode(\"utf-8\")) + body_b", "        new_total = len(head) + body_b")], "W"),
 ("Q10 ledger Rule sentence cut at 70 characters instead of 700", [("wake_pack.py", "RULE_MAX = 700", "RULE_MAX = 70")], "W"),
 ("Q11 --check ignores a sidecar whose content differs", [("wake_pack.py",
   "            elif strip_volatile(open(side, encoding=\"utf-8\", errors=\"replace\").read()) != strip_volatile(side_text):", "            elif False:")], "W"),
 ("Q12 past date found anywhere in the EXPIRES cell, not at its start", [("wake_pack.py",
   "        dm = END_DATE.match(lead(exp))", "        dm = END_DATE.search(lead(exp))")], "W"),
 ("Q13 launcher hunk B ignores WAKE_PACK_OK (pack prompt even when the build failed)", [("proposed/launcher_hunk_B.sh",
   "if [ \"$AGENT\" = \"wednesday\" ] && [ \"${WAKE_PACK_OK:-0}\" = \"1\" ]; then", "if [ \"$AGENT\" = \"wednesday\" ]; then")], "P"),
 ("Q14 launcher hunk A ignores the build's exit code", [("proposed/launcher_hunk_A.sh",
   "    if [ \"$WAKE_RC\" -eq 0 ]; then", "    if true; then")], "P"),
 ("Q15 handover check ignores a header naming another seat", [("handover_core.py",
   "        if fields.get(\"seat\") != a.seat:", "        if False:")], "HSD"),
 ("Q16 a missing grants file is silently an empty part (already the behaviour: control mutant, drops ALL grant rows)", [("wake_pack.py",
   "        verdict, why = classify_grant(line, b.seat, b.today)", "        verdict, why = (\"dead\", \"qa\")")], "W"),
 ("Q17 unreadable state file treated as absent (read_bytes swallows errors)", [("handover_core.py",
   "    with open(path, \"rb\") as f:\n        return f.read()\n\n\ndef split_header",
   "    try:\n        with open(path, \"rb\") as f:\n            return f.read()\n    except OSError:\n        return None\n\n\ndef split_header")], "HS"),
 ("Q18 struck-through first cell no longer unwrapped (MARKUP loses ~)", [("wake_pack.py",
   "MARKUP = \" \\t*~_`", "MARKUP = \" \\t*_`")], "W"),
]
for n,(name,edits,groups) in enumerate(M,1):
    mroot=os.path.join(SCR,"q%02d"%n,"2_Project_Files"); mlane=os.path.join(mroot,"wake"); os.makedirs(mlane)
    shutil.copytree(os.path.join(LANE,"proposed"),os.path.join(mlane,"proposed"))
    for f in ("handover.sh","handover_core.py","wake_pack.py","wake_census.sh"): shutil.copy(os.path.join(LANE,f),os.path.join(mlane,f))
    for rel in ("tools/seat_note.sh","fleet/cockpit/seat_resolve.sh"):
        os.makedirs(os.path.dirname(os.path.join(mroot,rel)),exist_ok=True); shutil.copy(os.path.join(REAL,rel),os.path.join(mroot,rel))
    ok=True
    for rel,needle,repl in edits:
        p=os.path.join(mlane,rel); s=open(p,encoding="utf-8").read()
        if s.count(needle)!=1:
            print("MUTANT-ERROR %s :: needle found %d times in %s"%(name,s.count(needle),rel)); ok=False; break
        open(p,"w",encoding="utf-8").write(s.replace(needle,repl))
    if not ok: continue
    if rel.startswith("proposed/launcher_hunk"):
        r=subprocess.run([sys.executable,os.path.join(mlane,"proposed","build_launcher_diff.py"),"--launcher","/Volumes/DevMASTER/WEDNESDAY/Launch_Wednesday.command","--write"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print("   (diff rebuilt in the mutant copy: rc %d %s)"%(r.returncode,r.stdout.decode()[-80:].strip()))
    ms=os.path.join(SCR,"q%02d_scratch"%n); os.makedirs(ms)
    e=dict(os.environ); e.update({"WAKE_UNDER_TEST":mlane,"WAKE_TEST_SCRATCH":ms,"PYTHONDONTWRITEBYTECODE":"1"})
    r=subprocess.run([sys.executable,os.path.join(LANE,"tests","run_tests.py"),"--groups",groups],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=e)
    out=r.stdout.decode("utf-8","replace")
    red=[l.split()[1] for l in out.split("\n") if l.startswith("FAIL ")]
    tail=[l for l in out.split("\n") if l.startswith("checks:")]
    print("%s %s :: red: %s :: %s"%("CAUGHT" if red else "MISSED",name," ".join(red) or "-",tail[-1] if tail else "no count line"))
