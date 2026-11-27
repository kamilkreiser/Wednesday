import re
G="/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md"; SD="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/wake/out/WAKE-wednesday.dropped.txt"
lines=open(G,encoding="utf-8").read().split("\n")
why={}
for n in (10,18,19,29,30,33,35,55,57): why[n]=("right","marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's")
for n in (39,41,48,53,54,61,62,64,68,69): why[n]=("right","marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant)")
why[24]=("right","the struck-through grant under the marker was TUESDAY's; the permanent rule is a live lesson indexed for the tuesday seat (see finding N1), not a rule for this seat")
why[65]=("doubtful","the marker says the premise ended, not that the row is dead; the row is a RESTRICTION on this seat and its own text says to re-read it with Kam before relying on it; dropped under ruling 4 (see finding N2)")
why[72]=("right","marker leads the cell (after the warning sign); the row says the grant is spent and must be re-asked; it was given at another seat's board view")
for n in (11,13,14,15,16,17,21,22,23,25,27,28,31,32,37,42,43,50,56,63,97,98,104): why[n]=("right","one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work")
why[26]=("right","one other seat leads the cell; a HOLD on a project of the client this seat is forbidden to touch; right for wednesday, NOT safe for a friday pack (see finding N3)")
for n in (17,23,31): why[n]=("right","one other seat leads the cell; a permission to that seat on a general project; it gives this seat nothing and binds it to nothing")
why[49]=("right","EXPIRES cell is a true end date (a 14-day acceptance window ending 2026-11-09); the first cell records both halves retired")
for n in (59,67): why[n]=("right","EXPIRES cell is the row's true end date, weeks past; no later date and no extension in the row")
for n in (125,126,134): why[n]=("right","EXPIRES cell is the true end date (end of Sunday 2026-09-20); the row already sits under the file's Expired heading")
for n in (141,142): why[n]=("right","EXPIRES cell is the true end date (end of Sunday 2026-09-13); ten weeks past")
out=["| line | class (tool) | first words of the first cell | judgement | reason |","|---|---|---|---|---|"]
cnt={"right":0,"wrong":0,"doubtful":0}
for l in open(SD,encoding="utf-8"):
    m=re.match(r"(dead marker|other seat|past date) \| line (\d+) \| (.*?) \| (.*)$",l.rstrip("\n"))
    if not m: continue
    n=int(m.group(2)); c1=lines[n-1].split("|")[1].strip().lstrip(" *~_`⚠✅️")
    words=" ".join(c1.split()[:3]).rstrip(":,(") 
    if m.group(1)=="other seat": words=c1.split(":")[0].split()[0].rstrip(":")+": ..."
    j,r=why[n]; cnt[j]+=1
    out.append("| %d | %s | %s | %s | %s |"%(n,m.group(1),words.replace("|","/"),j,r))
print("\n".join(out)); print(); print("COUNTS: right %d, wrong %d, doubtful %d, total %d"%(cnt["right"],cnt["wrong"],cnt["doubtful"],sum(cnt.values())))
