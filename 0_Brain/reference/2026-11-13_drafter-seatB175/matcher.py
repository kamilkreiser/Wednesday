import ast,re
P="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-13_seatB-174th/tools/b174_match.py"
src=open(P,encoding="utf-8").read()
tree=ast.parse(src)
L=None
for node in ast.walk(tree):
    if isinstance(node,ast.Assign) and any(getattr(t,"id","")=="OTHER_SEATS" for t in node.targets):
        L=ast.literal_eval(node.value)
print("entries",len(L),"distinct",len(set(L)),"head",L[0],"tail",L[-7:])
for s in ["B 173rd","B 174th","B 175th","B 176th","B 275th","B 1075th","B 1175th","B 1475th","B 1575th","B 274th","B 1074th","B 1174th","B 1474th","B 1574th","B 273rd","B 1573rd","B 172nd","B 171st"]:
    print(s,"present" if s in L else "ABSENT")
m=re.search(r'MINE\s*=\s*re\.compile\((.*)\)',src); print("MINE line:",m.group(0) if m else None)
for tok in ['"B 1573rd"','"B 1574th"','"B 174th"','"B 173rd"','B 174th','174th','"B 175th"']:
    print("occurrences",tok,src.count(tok))
print("cases=[ count:",len(re.findall(r"cases\s*=\s*\[",src)))
m2=re.search(r'cases\s*=\s*\[(.*?)\n\]',src,re.S)
if m2:
    try: print("cases literal len:",len(ast.literal_eval("["+m2.group(1)+"]")))
    except Exception as e: print("cases parse fail",e)
