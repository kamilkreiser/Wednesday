# print-only probes (round-4 gate). Only printf/print/read/pwd/eval-of-print run; nothing is written but h.txt.
P=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy_r4/probes
printf '/tmp/fakehome/.cl%s\n' aude > $P/h.txt
echo "--- zsh printf -v HOME"; zsh -fc 'printf -v HOME %s%s /tmp/fakehome/.cl aude ; print -rl -- ~/settings.json'
echo "--- bash printf -v HOME"; bash --noprofile --norc -c 'printf -v HOME %s%s /tmp/fakehome/.cl aude ; printf "%s\n" ~/settings.json'
echo "--- zsh read HOME"; zsh -fc "read -r HOME < $P/h.txt ; print -rl -- ~/settings.json"
echo "--- bash read HOME"; bash --noprofile --norc -c "read -r HOME < $P/h.txt ; printf '%s\n' ~/settings.json"
echo "--- zsh print -v HOME"; zsh -fc 'print -v HOME -n -- /tmp/fakehome/x ; print -rl -- ~/y'
echo "--- zsh printf -v HOME then bare cd; pwd"; zsh -fc 'printf -v HOME %s /tmp ; cd ; pwd'
echo "--- bash printf -v OLDPWD then cd -"; bash --noprofile --norc -c 'printf -v OLDPWD %s /tmp ; cd - ; pwd'
echo "--- zsh quoted eval"; zsh -fc "'eval' 'print' '=ls'"
echo "--- zsh eval after then"; zsh -fc "if true ; then eval print '=ls' ; fi"
echo "--- zsh command eval"; zsh -fc "command eval print x" 2>&1
echo "--- bash command eval"; bash --noprofile --norc -c "command eval printf '%s\\\\n' x"
echo "--- zsh magicequalsubst a==ls"; zsh -fc 'setopt magicequalsubst ; print -rl -- a==ls --opt==cat x=a:=ls'
echo "--- zsh default a==ls"; zsh -fc 'print -rl -- a==ls --opt==cat'
echo "--- zsh same-line alias"; zsh -fc 'alias foo=print ; foo hello' 2>&1
