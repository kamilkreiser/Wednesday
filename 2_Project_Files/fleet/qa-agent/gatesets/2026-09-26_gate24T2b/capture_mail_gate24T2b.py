#!/usr/bin/env python3
"""capture_mail_gate24T2b.py — capture the SEVEN READY mails of gate24T2b (#1249, #1250, #1251, #1252, #1253, #1254, #1255; Seats L6, L5, B 28th) and
Seat L5's DECLARED COUNTS mail VERBATIM, by message id. The ONLY inbox verb used is `inbox_digest.sh full wednesday-agent@agentmail.to '<id>'` (the
form Wednesday permitted; other forms mark mail seen). This script CANNOT locate a mail it was not given the id of — so the Seat L5 widen items
(KS-1201, KS-1296, KS-906, KS-1139) are NOT captured: their READY mails were never read by the drafter (README §6/§9). Writes
mail_ready_<n>.md per PR, mail_l5_declared_counts.md, and the combined capture mail_gate24T2b_ready.md beside this script, each with the
TEXT_SHA256 of the digest output, plus the sha256 + byte count of the prior reports the gate must read (READ). Refuses (rc 1) if a digest read
fails, is empty, or does not name its head (in full or as its 12-hex prefix). Writes nothing else."""
import hashlib, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
DIGEST = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh'
R = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/'
PRIOR = [R + '2026-09-13-ks828-900-981-04807ea0e-tier2-r1/report.md', R + '2026-09-25-batch1234-t1-r1/report.md',
         R + '2026-09-13-ks924-901-980-103c235b4-tier2-r2/report.md', R + '2026-09-16-ks1123-1002-a376756ab-ks1165-1003-c5488a689-tier2-r1/report.md',
         R + '2026-09-25-batch1218-t2c/report.md', R + '2026-09-25-batch1239-t1-r2/report.md', R + '2026-09-25-batch1241-t2d/report.md']
READY = [
    ('1249', 'KS-1144', '6eb283d058184f1f0fabdc3c3184a817db4fb94b', '<010001a0d8f25099-86861d1a-705b-4d79-9b56-6911dba50d23-000000@email.amazonses.com>',
     'Seat L6 READY FOR QA — #1249 KS-1144, STACKED on #1248 (14:22:34Z)'),
    ('1250', 'KS-1302 + KS-1303', 'c78f4093fb531bceb94a8e9defb59350d8c60b73', '<010001a0d8fa01cc-8afa79ce-7b25-448c-a500-a2d6c75f30d8-000000@email.amazonses.com>',
     'Seat L5 READY FOR QA — #1250 KS-1302 + KS-1303 (14:30:58Z)'),
    ('1251', 'KS-1147', '8020adae99129f4b7194fef32f1ea5b762819d90', '<010001a0d8fe8c77-18c17d2b-62a7-43b7-aa2b-4d3150eb398f-000000@email.amazonses.com>',
     'Seat L6 READY FOR QA — #1251 KS-1147 (14:35:55Z)'),
    ('1252', 'KS-1275 + KS-1299', 'ca7337fa04e04e5438bc79a5abe215424fcb33ef', '<010001a0d905ead3-23523114-c544-4596-97ee-a17b191f02d6-000000@email.amazonses.com>',
     'Seat B 28th READY FOR QA — #1252 KS-1275 + KS-1299 (14:43:58Z)'),
    ('1253', 'KS-1297', '6b88e4f03e82e3da0672efb1bb757ba5da912d6a', '<010001a0d90c6d1b-1e17e28b-da49-4329-bfd4-d797404c9b82-000000@email.amazonses.com>',
     'Seat L5 READY FOR QA — #1253 KS-1297 (14:51:05Z)'),
    ('1254', 'KS-1155', 'da0c94968a7423c340b3a3b76244bda536d1f6d2', '<010001a0d912f347-003f074b-3a44-4a73-a111-6df887f37c32-000000@email.amazonses.com>',
     'Seat L6 READY FOR QA — #1254 KS-1155, LANE COMPLETE (14:58:12Z)'),
    ('1255', 'KS-1301', '59245ff0b11c6b760ba5e2a9daedc5927e915e10', '<010001a0d91b2915-eb1ec62a-d8a8-4e8c-8728-927b0216b971-000000@email.amazonses.com>',
     'Seat B 28th READY FOR QA — #1255 KS-1301 (15:07:10Z)'),
]
DECL = ('<010001a0d908983b-1d9957c7-1c7d-497d-a4ec-ed29a0401559-000000@email.amazonses.com>', 'Seat L5 DECLARED COUNTS for items 2, 5, 6, 7 (14:46:54Z) — NOT in this batch; context for the next')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def read(mid):
    p = subprocess.run(['bash', DIGEST, 'full', 'wednesday-agent@agentmail.to', mid], capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip(): print('REFUSING: digest read of %s rc %d: %s' % (mid, p.returncode, p.stderr.strip()[:300])); sys.exit(1)
    return p.stdout
parts = []
for n, key, head, mid, label in READY:
    txt = read(mid)
    if head not in txt and head[:12] not in txt: print('REFUSING: the #%s READY does not name the head %s' % (n, head)); sys.exit(1)
    sha = hashlib.sha256(txt.encode()).hexdigest()
    named = 'in full' if head in txt else 'as its 12-hex prefix `%s` only' % head[:12]
    body = '## %s\nMESSAGE_ID %s\nTEXT_SHA256 %s\n#%s %s head %s (the READY names it %s; origin read by predict_gate24T2b.py)\n\n%s\n' % (label, mid, sha, n, key, head, named, txt.rstrip('\n'))
    open(os.path.join(G, 'mail_ready_%s.md' % n), 'w', encoding='utf-8').write(body)
    parts.append(body); print('captured #%s %s TEXT_SHA256 %s (%d B)' % (n, mid, sha, len(txt.encode())))
txt = read(DECL[0]); sha = hashlib.sha256(txt.encode()).hexdigest()
body = '## %s\nMESSAGE_ID %s\nTEXT_SHA256 %s\n\n%s\n' % (DECL[1], DECL[0], sha, txt.rstrip('\n'))
open(os.path.join(G, 'mail_l5_declared_counts.md'), 'w', encoding='utf-8').write(body); parts.append(body)
print('captured L5 DECLARED COUNTS %s TEXT_SHA256 %s' % (DECL[0], sha))
pr = []
for f in PRIOR:
    b = open(f, 'rb').read(); pr.append('PRIOR REPORT (READ): %s sha256 %s (%d bytes)' % (f, hashlib.sha256(b).hexdigest(), len(b)))
hdr = ('# CAPTURE — gate24T2b READY mails, VERBATIM by message id (captured %s by capture_mail_gate24T2b.py; instrument: `inbox_digest.sh full '
       'wednesday-agent@agentmail.to <id>`)\n\nSEVEN READYs from THREE seats. PR #1249 is KS-1144, head 6eb283d058184f1f0fabdc3c3184a817db4fb94b (STACKED on '
       '#1248 2b4960172644b5ef0414b94d46d11974012c2007, which is in the RUNNING gate24T2a batch); PR #1250 is KS-1302 + KS-1303, head '
       'c78f4093fb531bceb94a8e9defb59350d8c60b73; PR #1251 is KS-1147, head 8020adae99129f4b7194fef32f1ea5b762819d90; PR #1252 is KS-1275 + KS-1299, head '
       'ca7337fa04e04e5438bc79a5abe215424fcb33ef; PR #1253 is KS-1297, head 6b88e4f03e82e3da0672efb1bb757ba5da912d6a; PR #1254 is KS-1155, head '
       'da0c94968a7423c340b3a3b76244bda536d1f6d2; PR #1255 is KS-1301, head 59245ff0b11c6b760ba5e2a9daedc5927e915e10. The batch is FROZEN at seven '
       '(#1254 and #1255 added by Wednesday mid-draft). NOT in it: #1248 (gate24T2a), and Seat L5\'s widen items KS-1201 / KS-1296 / KS-906 / KS-1139 '
       '(no PR on origin at pin; READY mails not read by the drafter). Seat L5\'s DECLARED COUNTS mail is captured last, as context.\n%s\n' % (now, '\n'.join(pr)))
open(os.path.join(G, 'mail_gate24T2b_ready.md'), 'w', encoding='utf-8').write(hdr + '\n' + '\n'.join(parts))
for l in pr: print(l)
print('wrote', os.path.join(G, 'mail_gate24T2b_ready.md'))
