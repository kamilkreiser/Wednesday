import re
p='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/brief_S57_body.md'
t=open(p).read()
m=re.search(r'- \*\*Spent or archived:\*\*.*?\n',t)
print(m.group(0)[:600])
new="- **Spent or archived:** the archived and closed tickets of S 53rd to S 56th (S 56th's HELD list, first bullet, in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-11_seatS56_board.md`: the 17 closed by S 53rd to S 55th, Peter's 17 archived and eight other archived keys; archived tickets are absent from a default census, so a key that does not appear in your read is one of them), KS-1509 (closed Done and archived by S 56th 2026-11-11T07:19:13.556Z) and KS-1488 (type `duplicate`, keep it in every census predicate).\n"
t=t.replace(m.group(0),new); open(p,'w').write(t)
