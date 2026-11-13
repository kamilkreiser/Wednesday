import ast,re
P="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-13_seatB-173rd/tools/b173_match.py"
src=open(P,encoding="utf-8").read()
tree=ast.parse(src)
L=None
for node in ast.walk(tree):
    if isinstance(node,ast.Assign) and any(getattr(t,"id","")=="OTHER_SEATS" for t in node.targets):
        L=ast.literal_eval(node.value)
print("entries",len(L),"distinct",len(set(L)),"head",L[0],"tail",L[-6:])
for s in ["B 173rd","B 172nd","B 174th","B 175th","B 274th","B 1074th","B 1174th","B 1474th","B 1574th","B 273rd","B 1073rd","B 1173rd","B 1473rd","B 1573rd","B 272nd","B 1072nd","B 1172nd","B 1472nd","B 1572nd","B 171st"]:
    print(s,"present" if s in L else "ABSENT")
m=re.search(r'MINE\s*=\s*re\.compile\((.*)\)',src); print("MINE line:",m.group(0) if m else None)
for tok in ['"B 1572nd"','"B 1573rd"','"B 173rd"','"B 172nd"','B 173rd','173rd','"B 1571st"']:
    print("occurrences",tok,src.count(tok))
# self-test cases count
print("assignments of cases:",len(re.findall(r"cases\s*=\s*\[",src)))
print("tail anchor present for 174:",'"B 1572nd"' in src, "'B 1573rd' present:", '"B 1573rd"' in src)
idx=L.index("B 173rd") if "B 173rd" in L else None
print("index of B 173rd in list:",idx,"; tail before it:",L[idx-1:idx+2] if idx else None)
