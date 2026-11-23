import re,sys
d=open('/Volumes/Laptop-DEV/FRIDAY/0_Brain/daily_friday/2026-11-23.md',encoding='utf-8').read()
line=[l for l in d.split('\n') if l.startswith('- 10:25')][0]
m=re.search(r'note: (This is an acceptable risk.*?monitor)"',line)
daily=m.group(1)
c=open('/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/1_Project_Definition/CLARIFICATIONS.md',encoding='utf-8').read()
quote=[l for l in c.split('\n') if l.startswith('> ')]
print('quote lines:',len(quote))
q=quote[0][2:]
print('daily  repr:',repr(daily))
print('file   repr:',repr(q))
print('IDENTICAL:',daily==q,'len',len(daily),len(q),'two spaces after development.:','development.  Naturally' in q and 'development.  Naturally' in daily)
print('occurrences of daily in file:',c.count(daily))
print('card id in daily:', 'general-c2c-windows-agent-permission-mode-1123' in line, ' in file:','general-c2c-windows-agent-permission-mode-1123' in c)
print('choice text in daily:', 'c — Skip all prompts' in line)
print('non-ascii in file:',sorted(set(ch for ch in c if ord(ch)>127)))
print('trailing bytes of file:',repr(c[-80:]))
