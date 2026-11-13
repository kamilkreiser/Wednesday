import ast
P="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-13_seatB-171st/tools/b171_match.py"
src=open(P,encoding="utf-8").read()
tree=ast.parse(src)
L=None
for node in tree.body:
    if isinstance(node,ast.Assign) and any(getattr(t,"id","")=="OTHER_SEATS" for t in node.targets):
        L=ast.literal_eval(node.value)
print("entries",len(L),"distinct",len(set(L)),"head",L[0],"tail",L[-3:])
for x in ["B 170th","B 171st","B 172nd","B 173rd","B 272nd","B 1072nd","B 1172nd","B 1472nd","B 1572nd","B 271st","B 1071st","B 1171st","B 1471st","B 1571st","B 1070th","B 1170th","B 1470th","B 270th","B 1570th"]:
    print(x,"present" if x in L else "ABSENT")
n=len(L)
print("172: remove own B 172nd (present=%s): %d; add predecessor B 171st (present=%s); add six controls 173rd 272nd 1072nd 1172nd 1472nd 1572nd (all absent=%s)"%("B 172nd" in L,1 if "B 172nd" in L else 0,"B 171st" in L,all(x not in L for x in ["B 173rd","B 272nd","B 1072nd","B 1172nd","B 1472nd","B 1572nd"])))
n172=n-(1 if "B 172nd" in L else 0)+(0 if "B 171st" in L else 1)+6
print("n172 =",n172)
# self-test cases count
import re
m=re.search(r"^cases\s*=\s*\[(.*?)^\]",src,re.S|re.M)
print("cases literal found:",bool(m))
cl=[l for l in src.split("\n") if re.match(r"\s*cases\b",l)]
print(cl[:5])
