import re,json,os
D='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57'
t=open(D+'/brief_S57_body.md').read()
body=t.split('\nPROVENANCE:')[0]
keys=sorted(set(int(k) for k in re.findall(r'KS-(\d+)',body)))
cen={i['identifier']:i for i in json.load(open(D+'/evidence/board_all_1112.json'))}
def who(e):
    if not e: return 'UNASSIGNED'
    return e.split('@')[0]
PRI={0:'p0',1:'p1',2:'p2',3:'p3',4:'p4'}
lines=[]
for k in keys:
    key=f'KS-{k}'; f=f'{D}/evidence/tickets/{key}.json'
    if os.path.exists(f):
        i=json.load(open(f)); c=i['comments']['nodes']
        st=i['state']['name']+(' ARCHIVED '+i['archivedAt'][:10] if i['archivedAt'] else '')
        lines.append(f"- {key} | Linear read-only by key (ticket_get.py): {st} {PRI[i['priority']]} {who((i['assignee'] or {}).get('email'))}, {len(c)}c, upd {i['updatedAt'][:10]} | read 2026-11-12")
    elif key in cen:
        i=cen[key]
        lines.append(f"- {key} | Linear read-only (board_census.py, 768 non-archived): {i['state']['name']} {PRI[i['priority']]} {who((i['assignee'] or {}).get('email'))}, upd {i['updatedAt'][:10]} | read 2026-11-12")
    else:
        lines.append(f"- {key} | NOT READ by the drafter (absent from the default census; archived or not a ticket: UNMEASURED) | read 2026-11-12"); print('NOT READ',key)
other="""- Board census 768 (Backlog 494, In Progress 221, Todo 39, In Review 6, Blocked 3, Done 4, Duplicate 1; started 230; open 763; Backlog p3 237, p4 154, p2 81, p0 22; Stuart 8, Peter 10 by assignee) | Linear read-only via the S 56th drafter's `board_census.py`, saved as `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/evidence/board_all_1112.json`, counted by `count.py` | read 2026-11-12 00:44
- Eight Backlog to In Progress moves and KS-1509 gone since the S 56th drafter's 16:36 snapshot | key-by-key diff `diff.py` of `board_all_1111.json` against `board_all_1112.json` | read 2026-11-12 00:44
- Board text search (titles, descriptions and comment bodies of 768 issues; 1515 comments read, first 50 per issue, so KS-485 and KS-772 are capped) | Linear read-only via `board_text.py`, searched by `search.py` and `ctx.py` in the drafter's evidence folder | read 2026-11-12 00:44
- PR states and heads (2123 2124 2136 2138 2139 2140 2142 2143 2145 2146 2169 2170 2172 2174 2175 2176 2177 2178 2179 open; 2165 2166 2167 2168 2171 2173 1840 808 813 2113 2054 1569 merged) | GitHub REST GET via `gh_get.py pr` | read 2026-11-12 00:42 to 00:49
- Develop `cb46c28eef6f6aa761111f4737e53f3de1e43d74` | `GIT_OPTIONAL_LOCKS=0 git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop` | read 2026-11-12 00:42:49 and 00:49:13
- Ancestry `b1216f1040cb` into `6c9a593df4ab` (ahead 236, reverse behind 236); `98d7a21cf207` and `bff81a0d768d` into `cb46c28eef6f` (ahead 2 and ahead 1, behind 0) | GitHub compare via `gh_get.py cmp` | read 2026-11-12 00:4x
- METERING-USAGE-API.md line 26 (full line) at `cb46c28eef6f`, `fcd178ff34fa` and `98d7a21cf207`; exportService.ts lines 140 to 185 at `cb46c28eef6f`; kyc `src/index.ts` route lines and the isPlatformRole hit at `cb46c28eef6f` | GitHub contents API via `gh_file.py`, `gh_get.py lines` and `gh_grep.py` | read 2026-11-12 00:4x
- The 17 workflow files at `cb46c28eef6f` scanned for `openapi`, `check:openapi` and `preflight`; the five newest Actions runs | GitHub REST GET via `gh_wf_grep.py` and `gh_actions.py` (a checks-API call returned 403: unmeasured) | read 2026-11-12 00:4x
- Cards `secuura-ks2055-cancel-reason-length-bound-1111` (b), `secuura-lawyer-pack-v4-paste-and-send-1109` (a), `secuura-ghsa-chp3-effect-platform-shipped-1111` (a) | `decision_queue.sh show`, output saved as `dq_show_three.txt`; the ruled lists `dq_undelivered.txt` (177 cards) and `dq_ruled_all.txt` | read 2026-11-12 00:4x
- Card `secuura-ci-billing` discharge line | `decision_queue.sh list ruled` | read 2026-11-12 00:4x
- Gate 306 verdict (whole), gate 310 verdict (finding lines 84 and 85 and the PR 2172 to 2175 headings), gate 311 verdict (finding line 40 and headings) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-10_gate306-tier2-pr2166-2169/verdict.md, /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate310-tier2-pr2172-2175/verdict.md, /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate311-tier2-pr2176-2177/verdict.md | read 2026-11-12
- The nine gate verdict directories of queue item 3 (gates 307, 282, 284, 291, 292, 294, 293, 295, 296) | copied from S 56th's brief text, UNREAD by the drafter | read 2026-11-12 (not opened)
- S 56th's brief (293 lines, whole), plan ANSWER, HANDOVER, ROUTING, wrap mail and faults, the S 56th drafter's notes.md and review.md | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-11_seatS56_board.md, /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-11_S56_answer_plan.md and the S 56th record folder | read 2026-11-12 00:4x
- B 139th brief (first 9000 bytes, queue lines and tail row line by grep; NOT read whole) and R 99th brief (lines 1 to 80) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-12_seatB139_merge.md and /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-11_seatR99_raise.md | read 2026-11-12 00:4x
- Seat D 60th HANDOVER (lines 4 and 5 only) and the newest D seat by `ls -d` | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatD-60th/HANDOVER.md | read 2026-11-12 00:5x
- History ordinals (`Seat S 57` 0, `Seat S 56` 1, `Seat S 55` 2, `Seat S 54` 1) and `ls -d` of `*seatS-57*` (none) | `/usr/bin/grep -c -i -E` on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | read 2026-11-12 00:4x
- Model line `claude-sonnet-5-5` (checked_at_local 2026-11-12 00:38:16 +1100) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/models_latest.json | read 2026-11-12 00:5x
- Seats and capacity (B and R live, Spark o145, load1 4.0, memory free 79 percent) | Wednesday's commission /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/commission.md (her facts; not re-measured) | read 2026-11-12
"""
out=t.rstrip('\n')+'\n'+'\n'.join(lines)+'\n'+other
open(D+'/brief_S57.md','w').write(out)
print(len(keys),'ticket lines')
