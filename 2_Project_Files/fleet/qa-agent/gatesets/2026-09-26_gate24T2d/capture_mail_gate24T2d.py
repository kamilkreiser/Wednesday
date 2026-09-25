#!/usr/bin/env python3
"""capture_mail_gate24T2d.py — capture the gate24T2d claims VERBATIM: the FOUR READY mails Wednesday handed the drafter by message id (#1250 round 2,
Seat L5; #1262, Seat B 28th; #1263, Seat L7, and #1264, Seat L8 — the round-25 widens, handed by Wednesday's two WIDEN messages), WEDNESDAY'S RULING (a) on #1250's signal arms (her own staged outbound file, which the gate grades against), and — because
NO READY message id for #1253 round 2 was handed to the drafter — #1253's PR BODY as read by gh_read_gate24T2d.py (REST GET; gh_body_1253.md). The ONLY
inbox verb used is `inbox_digest.sh full wednesday-agent@agentmail.to '<id>'` (the form Wednesday permitted; other forms mark mail seen). This script
CANNOT locate a mail it was not given the id of — so #1253's round-2 READY and every OTHER round-25 READY (Seats B 29th / L7 / L8) are NOT captured
(README §1, §6, §9). Writes mail_ready_<n>.md per item and the combined capture mail_gate24T2d_ready.md beside this script, each with the TEXT_SHA256
of what was read, plus the sha256 + byte count of the reports the gate must read (READ). Refuses (rc 1) if a digest read fails, is empty, or does not
name its head (in full or as its 12-hex prefix). Writes nothing else."""
import hashlib, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
DIGEST = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh'
R = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/'
RULING = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_answer_seatL5_1250-signal-arms.md'
FIXR = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_FIX_seatL5_batch1249.md'
PRIOR = [R + '2026-09-26-batch1249-t2b/report.md', R + '2026-09-25-batch1234-t1-r1/report.md', R + '2026-09-25-batch1218-t2c/report.md',
         R + '2026-09-25-batch1239-t1-r2/report.md', R + '2026-09-26-batch1243-t2a/report.md']
READY = [
    ('1250', 'KS-1302 + KS-1303', '2b8dcb824dd2c5cd4b92757934d7de9d28813a22', '<010001a0d9c39635-ec2ab9d6-d1ad-4b71-ab9f-fbe66a5d542c-000000@email.amazonses.com>',
     'Seat L5 READY FOR QA — #1250 KS-1302 + KS-1303 ROUND 2 OF 2 (18:11:08Z)'),
    ('1262', 'KS-1310 + KS-1311', '3b319485d1e3a58f30e4190a7898d7562cb80c3b', '<010001a0d97f1618-7d0f5150-543b-4e8b-9258-2cf0521c60c5-000000@email.amazonses.com>',
     'Seat B 28th READY FOR QA — #1262 KS-1310 + KS-1311 (16:56:19Z)'),
    ('1263', 'KS-1140', '3c33f936fe3985ab40b72b78bda15a6959448e18', '<010001a0d9dcdfdc-123bc7b0-e9f0-4854-92b2-8006589a668e-000000@email.amazonses.com>',
     'Seat L7 READY FOR QA — #1263 KS-1140, tier 3 comment-only, the round-25 WIDEN (18:38:46Z)'),
    ('1264', 'KS-1281', '2e95121dfc475a09c81d61d61f9a81148b6bb0b9', '<010001a0d9e3c948-2788f49d-79b7-450e-83dd-e89fd9e3c9cf-000000@email.amazonses.com>',
     'Seat L8 READY FOR QA — #1264 KS-1281, tier 3 comment-only, the second round-25 WIDEN (18:46:19Z)'),
]
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def read(mid):
    p = subprocess.run(['bash', DIGEST, 'full', 'wednesday-agent@agentmail.to', mid], capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip() or '(no body)' in p.stdout[:400]:
        print('REFUSING: digest read of %s rc %d: %s' % (mid, p.returncode, p.stderr.strip()[:300])); sys.exit(1)
    return p.stdout
parts = []
for n, key, head, mid, label in READY:
    txt = read(mid)
    if head not in txt and head[:12] not in txt: print('REFUSING: the #%s READY does not name the head %s' % (n, head)); sys.exit(1)
    sha = hashlib.sha256(txt.encode()).hexdigest()
    named = 'in full' if head in txt else 'as its 12-hex prefix `%s` only' % head[:12]
    body = '## %s\nMESSAGE_ID %s\nTEXT_SHA256 %s\n#%s %s head %s (the READY names it %s; origin read by predict_gate24T2d.py)\n\n%s\n' % (label, mid, sha, n, key, head, named, txt.rstrip('\n'))
    open(os.path.join(G, 'mail_ready_%s.md' % n), 'w', encoding='utf-8').write(body)
    parts.append(body); print('captured #%s %s TEXT_SHA256 %s (%d B)' % (n, mid, sha, len(txt.encode())))
b53 = open(os.path.join(G, 'gh_body_1253.md'), encoding='utf-8').read()
if '91e066264004fdb22c67efb0c25fc44375ec6eac' not in b53: print('REFUSING: gh_body_1253.md does not name #1253\'s round-2 head — run gh_read_gate24T2d.py first'); sys.exit(1)
sha = hashlib.sha256(b53.encode()).hexdigest()
body = ('## #1253 KS-1297 ROUND 2 OF 2 — NO READY MESSAGE ID WAS HANDED TO THE DRAFTER: the PR BODY instead (REST GET by gh_read_gate24T2d.py, gh_body_1253.md)\n'
        'SOURCE gh_body_1253.md\nTEXT_SHA256 %s\n#1253 KS-1297 head 91e066264004fdb22c67efb0c25fc44375ec6eac (Wednesday\'s daily note 04:02 records the round-2 READY as received; '
        'its id was not in the commission, and this script reads by id only)\n\n%s\n' % (sha, b53.rstrip('\n')))
open(os.path.join(G, 'mail_ready_1253.md'), 'w', encoding='utf-8').write(body); parts.append(body); print('captured #1253 PR body TEXT_SHA256 %s (%d B)' % (sha, len(b53.encode())))
b65 = open(os.path.join(G, 'gh_body_1265.md'), encoding='utf-8').read()
if '87ef6a1b088754ab773f541ddb273acce8dfab4f' not in b65: print('REFUSING: gh_body_1265.md does not name #1265\'s head — run gh_read_gate24T2d.py first'); sys.exit(1)
sha = hashlib.sha256(b65.encode()).hexdigest()
body = ('## #1265 KS-1315 (Seat L7, round 25, tier 2) — NO READY MESSAGE ID WAS HANDED TO THE DRAFTER (Wednesday named it as "the newest READY FOR QA (Seat L7): #1265 mail"; '
        'locating it would need a listing, which marks mail seen): the PR BODY instead (REST GET, gh_body_1265.md)\n'
        'SOURCE gh_body_1265.md\nTEXT_SHA256 %s\n#1265 KS-1315 head 87ef6a1b088754ab773f541ddb273acce8dfab4f\n\n%s\n' % (sha, b65.rstrip('\n')))
open(os.path.join(G, 'mail_ready_1265.md'), 'w', encoding='utf-8').write(body); parts.append(body); print('captured #1265 PR body TEXT_SHA256 %s (%d B)' % (sha, len(b65.encode())))
b66 = open(os.path.join(G, 'gh_body_1266.md'), encoding='utf-8').read()
if '952f4329de97cd7f94ab6363e670248c456d0a54' not in b66: print('REFUSING: gh_body_1266.md does not name #1266\'s head — run gh_read_gate24T2d.py first'); sys.exit(1)
sha = hashlib.sha256(b66.encode()).hexdigest()
body = ('## #1266 KS-1120 (Seat L8, round 25, tier 2) — NO READY MESSAGE ID WAS HANDED TO THE DRAFTER (Wednesday named it as "the newest READY FOR QA (Seat L8): #1266 mail"): '
        'the PR BODY instead (REST GET, gh_body_1266.md)\nSOURCE gh_body_1266.md\nTEXT_SHA256 %s\n#1266 KS-1120 head 952f4329de97cd7f94ab6363e670248c456d0a54\n\n%s\n' % (sha, b66.rstrip('\n')))
open(os.path.join(G, 'mail_ready_1266.md'), 'w', encoding='utf-8').write(body); parts.append(body); print('captured #1266 PR body TEXT_SHA256 %s (%d B)' % (sha, len(b66.encode())))
for lab, path in (('WEDNESDAY\'S RULING (a) on #1250\'s signal arms — the standard this gate grades #1250 against (Wednesday\'s staged outbound, READ as a file)', RULING),
                  ('the FIX ROUNDS mail it partly supersedes (the round-1 HOLD lines verbatim; Wednesday\'s staged outbound, READ as a file)', FIXR)):
    t = open(path, encoding='utf-8').read(); sha = hashlib.sha256(t.encode()).hexdigest()
    parts.append('## %s\nSOURCE %s\nTEXT_SHA256 %s\n\n%s\n' % (lab, path, sha, t.rstrip('\n'))); print('captured %s TEXT_SHA256 %s' % (os.path.basename(path), sha))
pr = []
for f in PRIOR:
    try:
        b = open(f, 'rb').read(); pr.append('PRIOR REPORT (READ): %s sha256 %s (%d bytes)' % (f, hashlib.sha256(b).hexdigest(), len(b)))
    except OSError as e:
        pr.append('PRIOR REPORT UNREAD: %s (%s)' % (f, e))
hdr = ('# CAPTURE — gate24T2d claims, VERBATIM (captured %s by capture_mail_gate24T2d.py; instrument for mail: `inbox_digest.sh full '
       'wednesday-agent@agentmail.to <id>`)\n\nSEVEN PRs, FROZEN: two at the cap round, one from a wrapped author, four round-25 widens. PR #1250 is KS-1302 + KS-1303, ROUND 2 OF 2, head 2b8dcb824dd2c5cd4b92757934d7de9d28813a22 '
       '(round 1 c78f4093fb531bceb94a8e9defb59350d8c60b73, NO GO in gate24T2b: TRAP SWALLOWS); PR #1253 is KS-1297, ROUND 2 OF 2, head '
       '91e066264004fdb22c67efb0c25fc44375ec6eac (round 1 6b88e4f03e82e3da0672efb1bb757ba5da912d6a, NO GO in gate24T2b: READER WRONG); PR #1262 is KS-1310 + KS-1311, head '
       '3b319485d1e3a58f30e4190a7898d7562cb80c3b (Seat B 28th, wrapped); PR #1263 is KS-1140, head 3c33f936fe3985ab40b72b78bda15a6959448e18 (Seat L7, round 25, tier 3 comment-only; '
       'added by Wednesday\'s WIDEN message); PR #1264 is KS-1281, head 2e95121dfc475a09c81d61d61f9a81148b6bb0b9 (Seat L8, round 25, tier 3 comment-only; '
       'added by Wednesday\'s second WIDEN message); PR #1265 is KS-1315, head 87ef6a1b088754ab773f541ddb273acce8dfab4f (Seat L7, round 25, tier 2 test-only; '
       'added by Wednesday\'s third WIDEN message; no READY id: its PR body is captured). PR #1266 is KS-1120, head 952f4329de97cd7f94ab6363e670248c456d0a54 (Seat L8, round 25, tier 2 test-only; the fourth WIDEN; no READY id: its PR body is captured). NOT in it: any other round-25 PR. '
       'Wednesday\'s RULING (a) is captured after the READYs: it SUPERSEDES the round-1 signal-cell clause of the FIX ROUNDS mail, which is captured last.\n%s\n' % (now, '\n'.join(pr)))
open(os.path.join(G, 'mail_gate24T2d_ready.md'), 'w', encoding='utf-8').write(hdr + '\n' + '\n'.join(parts))
for l in pr: print(l)
print('wrote', os.path.join(G, 'mail_gate24T2d_ready.md'))
