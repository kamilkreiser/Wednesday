# usage: st.sh "<log line>" "<last line>"
S="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/5_Project_History/STATUS_QA_SCANNER_CORE_R2.md"
python3 -B - "$S" "$1" "$2" <<'PY'
import sys
p, log, last = sys.argv[1:4]
L = open(p).read().rstrip('\n').split('\n')
L = L[:-1]
while L and L[-1] == '': L.pop()
if log: L.append(log)
L += ['', last]
open(p, 'w').write('\n'.join(L) + '\n')
PY
