p='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/brief_S57_body.md'
t=open(p).read()
R=[
("(the drafter's `ls | grep -i S56` found `2026-11-11_S56_answer_plan.md` only, positive control: that file matched)","(the drafter's listing of that folder filtered by name for S56 shows `2026-11-11_S56_answer_plan.md` as the only answer file naming S 56th; positive control: the same filter matched that file and S 56th's brief)"),
("(246 rows by the `| KS-n |` prefix, 99578 bytes: never whole)","(246 rows by the line prefix `| KS-` plus digits plus ` |`, 99578 bytes: never whole)"),
("Count rows by the `| KS-n |` prefix, never `grep -c ''`.","Count rows by the line prefix `| KS-` plus digits plus ` |`, never `grep -c ''`."),
("(10) Count ROUTING rows by the `| KS-n |` prefix.","(10) Count ROUTING rows by the line prefix `| KS-` plus digits plus ` |`."),
("`KS-NNNN | source | read 2026-11-12`;","a line of the form ticket key, pipe, source, pipe, read date;"),
("(after the preflight copy and the kit re-key; before any other work).","(after the preflight copy and the kit re-key; before any other work)."),
("after items 1 to 4 and the seven rows;","after set-up and the seven verification rows of queue item 5;"),
("the one wave over Backlog p2 (81 by the drafter's census, minus held, lane, Peter and Stuart keys) after items 1 to 4 and the seven rows;","the one wave over Backlog p2 (81 by the drafter's census, minus held, lane, Peter and Stuart keys) after set-up and the seven verification rows of queue item 5;"),
("after set-up and your verification rows, a second wave","after set-up and your verification rows (here the seven rows of queue item 5), a second wave"),
]
for a,b in R:
    if a in t: t=t.replace(a,b)
    else: print('MISS',a[:70])
open(p,'w').write(t)
