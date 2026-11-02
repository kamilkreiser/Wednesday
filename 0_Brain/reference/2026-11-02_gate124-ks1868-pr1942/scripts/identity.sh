#!/bin/bash
# gate 124: held-patch identity (sha, containment, sections) + strict apply at base in two orders, compared blob by blob to PR head
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942; R=$W/repo
N=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night; RU=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
declare -A SHA=([a1]=6e2c8b6ad3ff1b01c8dabdf3e54fc6dbdfeeebbd6e98717244355d7a6a026a1c [a2]=a66f10897fdab28663a2adb644932fb7a06f223a5e3484132721a628083e6aa3 [a3]=0a4ecc94416937e9401c42c84e2401c02dc3fab3656bb2225da2e55cd7cc058a [a4]=df0f48219de0088d5b080594eedc3cdecd5c000828914d560614ca50ac721e4e [a5]=ac3a5ed70e1e5e83d91d3b622adb9c00ba98ea54a328ce384a4c04268a549870)
declare -A HELD=([a1]=O79-A1 [a2]=O79-A2 [a3]=O79-A3 [a4]=O79-A4 [a5]=O79-A5)
for k in a1 a2 a3 a4 a5; do
  D=$(ls -d $RU/spark_secuura_2026-11-02_ks_1868_o79_${k}_* | /usr/bin/grep -v control); C=$D/out.md.checker
  H=$(ls $N/READY_KS-1868-KS-1868-${HELD[$k]}_*)
  S=$(shasum -a 256 $C/patch.diff | awk '{print $1}')
  python3 -I -c "
import glob
p=open('$C/patch.diff','rb').read(); h=open('$H','rb').read()
secs=sorted(glob.glob('$C/section_[0-9].diff'))
cat=b''.join(open(s,'rb').read() for s in secs)
print('$k', 'sha', '$S'[:12], 'sha_eq_brief', '$S'=='${SHA[$k]}', 'contained_in_held', p in h, 'sections', len(secs), 'concat_eq_patch', cat==p)
"
  for c in control control-r2; do [ -d $D-$c ] && echo "  $c patch eq unsuffixed: $(cmp -s $D-$c/out.md.checker/patch.diff $C/patch.diff && echo yes || echo NO)"; done
done
apply_order(){
  name=$1; shift; T=$W/apply_$name
  git -C $R worktree add -q --detach $T $MB
  for k in "$@"; do D=$(ls -d $RU/spark_secuura_2026-11-02_ks_1868_o79_${k}_* | /usr/bin/grep -v control); C=$D/out.md.checker
    for s in $(ls $C/section_[0-9].diff | sort); do o=$(git -C $T apply --check -v $s 2>&1); rc=$?
      echo "$name $k $(basename $s) check rc=$rc offset/fuzz lines: $(echo "$o" | /usr/bin/grep -i -c 'fuzz\|offset')"; echo "$o" | /usr/bin/grep -i 'offset\|fuzz'
      git -C $T apply $s || echo APPLY_FAIL; done; done
  git -C $T add -A; echo "$name tree $(git -C $T write-tree)"
  for f in $(git -C $R diff --name-only $MB pr1942); do a=$(git -C $T rev-parse ":$f" 2>/dev/null); b=$(git -C $R rev-parse "pr1942:$f"); [ "$a" = "$b" ] && echo "  SAME $f" || echo "  DIFFERS $f"; done
}
apply_order fwd a1 a2 a3 a4 a5
apply_order rev a5 a4 a3 a2 a1
echo "pr1942 tree $(git -C $R rev-parse 'pr1942^{tree}')"
git -C $R worktree remove --force $W/apply_fwd; git -C $R worktree remove --force $W/apply_rev
git -C $R worktree list
