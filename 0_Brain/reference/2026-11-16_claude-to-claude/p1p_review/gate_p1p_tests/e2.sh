. /private/tmp/claude-501/qp1/p/lib.sh
mkdir -p $W/p/w4/secret $W/p/w5/private $W/p/w6
startd $W/p/x4 --gate --workspace $W/p/w4 --exclude '<ws>/secret/**' || echo startfail
startd $W/p/x5 --gate --workspace $W/p/w5 --exclude '<ws>/nothere/**' || echo startfail
startd $W/p/x6 --gate --workspace $W/p/w6 --exclude 'private/**' || echo startfail
echo "== x4 (<ws>/secret/**) Bash ls"; ev s1 $W/p/w4 default Bash '{"command":"ls"}' | hk $W/p/x4 | san
echo "== x5 (<ws>/nothere/**) Bash ls"; ev s1 $W/p/w5 default Bash '{"command":"ls"}' | hk $W/p/x5 | san
echo "== x6 (private/**) Write hello"; ev s1 $W/p/w6 default Write "{\"file_path\":\"$W/p/w6/hello.txt\",\"content\":\"x\"}" | hk $W/p/x6 | san
echo "== x6 (private/**) Read hello"; ev s1 $W/p/w6 default Read "{\"file_path\":\"$W/p/w6/hello.txt\"}" | hk $W/p/x6 | san
for d in x4 x5 x6; do stopd $W/p/$d; done
