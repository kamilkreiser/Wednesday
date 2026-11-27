# summarise each mutant log: failing tests and the first panic message of each (python3 -I -B mut_sum.py names...)
import sys, re
Q = '/private/tmp/claude-501/qae3'
for n in sys.argv[1:]:
    t = open(f'{Q}/logs/mut_{n}.log', errors='replace').read()
    failed = re.findall(r'^test (\S+) \.\.\. FAILED$', t, re.M)
    comp = len(re.findall(r'Compiling coagent-audit ', t)); cerr = 'error[E' in t or 'could not compile' in t
    print(f'{n}: compiling {comp}; compile error {cerr}; failed {failed or "none"}')
    for m in re.finditer(r"---- (\S+) stdout ----\n(?:.*\n)*?thread '[^']*' (?:\(\d+\) )?panicked at [^\n]*:\n([^\n]*)", t):
        print(f'    {m.group(1)}: {m.group(2)[:300]}')
