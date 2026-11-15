#!/bin/bash
# dl_repo.sh <repo> <revision> <dest_dir> [path_prefix] — 2026-11-12 five-model A/B (Wednesday operator).
# Downloads every file of an official HF repo at a PINNED revision (optionally only files under path_prefix),
# 4 in parallel with curl resume, then verifies each file's size and (for LFS files) sha256 against the HF API.
# Writes <dest_dir>/dl.status (start/done/verify lines). Never deletes anything. No cd.
set -uo pipefail
REPO=$1; REV=$2; DEST=$3; PFX=${4:-}
mkdir -p "$DEST"
ST="$DEST/dl.status"
date -u +"start %FT%TZ repo=$REPO rev=$REV prefix=$PFX" >> "$ST"
curl -sS -m 60 "https://huggingface.co/api/models/$REPO/revision/$REV?blobs=true" > "$DEST/.api.json" || { echo "api fail" >> "$ST"; exit 2; }
python3 - "$DEST/.api.json" "$PFX" > "$DEST/.files.tsv" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); pfx=sys.argv[2]
for s in d["siblings"]:
    n=s["rfilename"]
    if pfx and not n.startswith(pfx): continue
    if n.endswith(".gitattributes") or n.startswith("."): continue
    lfs=s.get("lfs") or {}
    print("\t".join([n, str(s.get("size") or lfs.get("size") or ""), lfs.get("sha256","")]))
PY
echo "files $(wc -l < "$DEST/.files.tsv") bytes $(awk -F'\t' '{s+=$2} END{print s}' "$DEST/.files.tsv")" >> "$ST"
cut -f1 "$DEST/.files.tsv" | xargs -P 4 -I{} bash -c '
  f="$1"; mkdir -p "$(dirname "$2/$f")"
  curl -sSL --retry 8 --retry-delay 10 -C - -o "$2/$f" "https://huggingface.co/$3/resolve/$4/$f"; echo "$f curl_rc=$?" >> "$2/dl.status"' _ {} "$DEST" "$REPO" "$REV"
date -u +"downloaded %FT%TZ" >> "$ST"
ok=0; bad=0
while IFS=$'\t' read -r n sz sha; do
  have=$(stat -c %s "$DEST/$n" 2>/dev/null || echo -1)
  if [ "$have" != "$sz" ]; then echo "VERIFY BAD size $n have=$have want=$sz" >> "$ST"; bad=$((bad+1)); continue; fi
  if [ -n "$sha" ]; then
    got=$(sha256sum "$DEST/$n" | cut -d' ' -f1)
    if [ "$got" != "$sha" ]; then echo "VERIFY BAD sha $n" >> "$ST"; bad=$((bad+1)); continue; fi
  fi
  ok=$((ok+1))
done < "$DEST/.files.tsv"
date -u +"verified %FT%TZ ok=$ok bad=$bad" >> "$ST"
