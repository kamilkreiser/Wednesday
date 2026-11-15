import ast,re,glob
P=glob.glob("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-15_seatB-176th/**/b176_match.py",recursive=True)
print("b176_match.py paths:",P)
src=open(P[0],encoding="utf-8").read()
L=None
for node in ast.walk(ast.parse(src)):
    if isinstance(node,ast.Assign) and any(getattr(t,"id","")=="OTHER_SEATS" for t in node.targets): L=ast.literal_eval(node.value)
print("entries",len(L),"distinct",len(set(L)),"head",L[0],"tail",L[-8:])
for s in ["B 176th","B 177th","B 175th","B 178th","B 277th","B 1077th","B 1177th","B 1477th","B 1577th","B 276th","B 1076th","B 1176th","B 1476th","B 1576th","B 1575th"]:
    print(s,"present" if s in L else "ABSENT")
m=re.search(r'MINE\s*=\s*re\.compile\((.*)\)',src); print("MINE line:",m.group(0) if m else None)
for tok in ['"B 1575th"','"B 1576th"','"B 176th"','B 176th','176th','"B 177th"']: print("occurrences",tok,src.count(tok))
print("cases at lines:",[i+1 for i,l in enumerate(src.splitlines()) if "cases" in l][:6])
