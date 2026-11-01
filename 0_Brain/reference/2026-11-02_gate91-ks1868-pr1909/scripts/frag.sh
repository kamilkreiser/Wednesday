#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate91-ks1868-pr1909
R=$G/repo; F="$R/Projects Documents/fragments"
N=KS-1868-nft-certificate-minting-fetch-and-wallet-reads-unreadable-thrown-value.html
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
chk(){ nice -n 10 node $R/Blockchain/Dev/scripts/docs-fragments.mjs check --root $R > "$1" 2>&1; echo "rc=$?" >> "$1"; }
chk $G/logs/frag_check_clean.log
for k in flow cheat; do
  f="$F/$k/$N"; h=$(sha "$f"); cp "$f" $G/logs/frag_orig_$k.html
  printf '\n<div>planted unclosed</div><div>\n' >> "$f"
  chk $G/logs/frag_check_planted_${k}_div.log
  cp $G/logs/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k div restore OK" || echo "$k div RESTORE FAIL"
  printf '\n<p>planted prose outside a table</p>\n' >> "$f"
  chk $G/logs/frag_check_planted_${k}_prose.log
  cp $G/logs/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k prose restore OK" || echo "$k prose RESTORE FAIL"
done
chk $G/logs/frag_check_after_restore.log
for l in clean planted_flow_div planted_flow_prose planted_cheat_div planted_cheat_prose after_restore; do echo "== $l"; tail -4 $G/logs/frag_check_$l.log; done
git -C $R status --short
