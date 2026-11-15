import ast,re
P="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-15_seatB-177th/tools/b177_match.py"
src=open(P,encoding="utf-8").read()
L=None
for node in ast.walk(ast.parse(src)):
    if isinstance(node,ast.Assign) and any(getattr(t,"id","")=="OTHER_SEATS" for t in node.targets): L=ast.literal_eval(node.value)
new=["B 179th","B 278th","B 1078th","B 1178th","B 1478th","B 1578th"]
print("entries",len(L),"distinct",len(set(L)))
print("B 177th present:", "B 177th" in L, "| B 178th present:", "B 178th" in L)
print("new controls ABSENT each:",[(s,s not in L) for s in new])
print("old controls present:",[(s,s in L) for s in ["B 278th" if False else "B 277th","B 1077th","B 1177th","B 1477th","B 1577th","B 1576th","B 1575th"]])
n=len(L)-1+1+len(new)
print("n =",len(L),"-1 (own B 178th out) +1 (B 177th in) +",len(new),"=",n,"; self-test 9+n =",9+n)
print("self-test arithmetic check B177's: 9+722 =",9+722)
for tok in ['"B 1577th"','"B 1576th"','"B 177th"','B 177th','177th','"B 178th"','B 178th','178th']: print("occurrences",tok,src.count(tok))
print("tail:",L[-8:])
