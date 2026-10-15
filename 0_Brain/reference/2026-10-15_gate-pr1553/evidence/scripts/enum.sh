#!/bin/bash
# enum.sh <WORK>: print every commit in every clone with parent/tree/msg
W=$1
for r in seed fresh stale_tag stale_origin_tag hijack; do
  git -C "$W/$r" for-each-ref --format='%(refname)' refs/heads refs/tags | while read ref; do
    git -C "$W/$r" log -1 --format="$r $ref %H p=%P t=%T ad=%at cd=%ct s=%s" "$ref^{commit}"
  done
done | sort -k3
