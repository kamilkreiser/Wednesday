p='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/brief_S57_body.md'
t=open(p).read()
R=[
("Seat U's keys KS-1231, KS-1855, KS-1952, KS-1998, KS-2059, KS-2111: no write (U 23rd wrapped 05:09Z on 2026-11-11 by S 56th's brief; whether any was handed on is UNMEASURED).",
 "Seat U's keys KS-1231, KS-1855, KS-1952, KS-1998, KS-2059, KS-2111: no write (U 23rd wrapped 05:09Z on 2026-11-11 by S 56th's brief; whether any was handed on is UNMEASURED; the drafter's read by key shows KS-1231 already Done and archived 2026-11-08, so it is not on the board to hold)."),
("KS-1790 and KS-1861 are read-only neighbours.","KS-1790 (Backlog) and KS-1861 (the drafter's read by key: Done, archived 2026-11-02) are read-only neighbours."),
]
for a,b in R:
    if a in t: t=t.replace(a,b)
    else: print('MISS',a[:60])
open(p,'w').write(t)
