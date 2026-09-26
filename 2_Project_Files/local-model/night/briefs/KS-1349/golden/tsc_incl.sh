#!/bin/bash
# tsc_incl.sh <out file> : test-inclusive tsc on originate in the scratch clone (a temp config extending the
# package's tsconfig.json with exclude: [] so src/__tests__ is compiled under the package's strict options).
# Writes the SORTED error lines (file(line,col): error TSxxxx: msg) to <out>; prints the count and rc.
C=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/sparkfeed
O=$C/Blockchain/Dev/services/originate
OUT=$1
cat > $O/tsconfig.ks-incl.json <<'EOF'
{ "extends": "./tsconfig.json", "compilerOptions": { "noEmit": true, "declaration": false, "sourceMap": false }, "exclude": [] }
EOF
(cd $O && node ../../node_modules/typescript/bin/tsc -p tsconfig.ks-incl.json > $OUT.raw 2>&1; echo $? > $OUT.rc)
rm -f $O/tsconfig.ks-incl.json
grep -E 'error TS[0-9]+' $OUT.raw | sort -u > $OUT
echo "test-inclusive tsc rc=$(cat $OUT.rc) errors=$(wc -l < $OUT | tr -d ' ')"
