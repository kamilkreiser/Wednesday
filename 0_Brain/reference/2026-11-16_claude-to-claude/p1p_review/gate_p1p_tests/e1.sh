. /private/tmp/claude-501/qp1/p/lib.sh
mkdir -p $W/p/w1/private $W/p/w2/private $W/p/w3
startd $W/p/x1 --gate --workspace $W/p/w1 --exclude '<ws>/private/**' || echo startfail
startd $W/p/x2 --gate --workspace $REAL/p/w2 --exclude '<ws>/private/**' || echo startfail
startd $W/p/x3 --gate --workspace $W/p/w3 || echo startfail
for c in "x1 $W/p/w1" "x1 $REAL/p/w1" "x2 $REAL/p/w2" "x2 $W/p/w2" "x3 $W/p/w3"; do set -- $c
 echo "== daemon $1 cwd $2 :: Bash ls"; ev s1 $2 default Bash '{"command":"ls"}' | hk $W/p/$1 | san
 echo "== daemon $1 cwd $2 :: Read hello"; ev s1 $2 default Read "{\"file_path\":\"$2/hello.txt\"}" | hk $W/p/$1 | san
done
for d in x1 x2 x3; do stopd $W/p/$d; done
