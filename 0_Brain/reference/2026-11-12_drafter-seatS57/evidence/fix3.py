import re
p='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/brief_S57_body.md'
t=open(p).read()
def ex(m):
    nums=re.findall(r'(?:KS-)?(\d+)',m.group(0))
    if len(nums)<4: return m.group(0)
    return ', '.join('KS-'+n for n in nums)
t2=re.sub(r'KS-\d+(?:, (?:KS-)?\d+)+',ex,t)
open(p,'w').write(t2); print(len(t),len(t2))
