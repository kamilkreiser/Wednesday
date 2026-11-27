#!/bin/bash
# probe (not a fix): a FILE-level symlink at the one fixed file name this tool writes in its destination, README.txt.
. "$1/lib3.sh"; date
say "== a dangling symlink planted at <NAS>/General/Wednesday/nightly-backup/README.txt, pointing outside"
fixture rd; B="$T/nas/General/Wednesday/nightly-backup"; mkdir -p "$B" "$T/nas/outside5"; ln -s "$T/nas/outside5/planted.txt" "$B/README.txt"
say "  rc=$(run "$(at 0 1 0)" r) GOOD=$(good r) ; files now in the outside folder: $(ls "$T/nas/outside5" | tr '\n' ' ') ; README.txt is still: $(stat -f '%HT' "$B/README.txt")"
say "== control: the same with the link pointing at an EXISTING outside file"
fixture rd2; B="$T/nas/General/Wednesday/nightly-backup"; mkdir -p "$B" "$T/nas/outside5"; echo theirs > "$T/nas/outside5/planted.txt"; ln -s "$T/nas/outside5/planted.txt" "$B/README.txt"
say "  rc=$(run "$(at 0 1 0)" r) GOOD=$(good r) ; the outside file holds: $(cat "$T/nas/outside5/planted.txt")"
