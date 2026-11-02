H=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/suites_head/summary.txt; B=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/suites_base/summary.txt
echo head lines: $(grep -c ' rc=' $H) base: $(grep -c ' rc=' $B)
echo "head nonzero rc:"; grep -v 'rc=0' $H | grep ' rc='
echo "base nonzero rc:"; grep -v 'rc=0' $B | grep ' rc='
echo "diff base vs head:"; diff $B $H
