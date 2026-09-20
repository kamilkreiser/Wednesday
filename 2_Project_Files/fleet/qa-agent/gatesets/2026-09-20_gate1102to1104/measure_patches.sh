#!/bin/bash
# measure_patches.sh — canonical-patch identity: develop blobs written as plain files into a scratch dir (not a repo); each canonical patch applied
# (PR1 strict, PR2 --recount after the strict rc is recorded, PR3 strict); results hashed with git hash-object (no -w); reverse controls.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
R=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs
DEV=dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa
W="$(mktemp -d "$1/patches.XXXXXX")"
date -u +%Y-%m-%dT%H:%M:%SZ
P1="$R/2026-09-20_ks1275-ornith35b-night4/out.md.checker/patch.diff"
P2="$R/2026-09-20_ks1203-ornith35b-night/out.md.checker/patch.diff"
P3="$R/2026-09-20_ks1272-ornith35b-night/out.md.checker/patch.diff"
for p in "$P1" "$P2" "$P3"; do echo "$(shasum -a 256 "$p" | cut -c1-64) lines=$(wc -l < "$p") $p"; done
F1=Blockchain/Dev/services/originate/src/__tests__/lifecycleEventRepo.test.ts
F2=Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts
F3a=Blockchain/Dev/services/api-gateway/src/startup-migrations.ts
F3b=Blockchain/Dev/services/api-gateway/src/__tests__/ks1272-platform-dedup-uuid-tenant-id.test.ts
for f in "$F1" "$F2" "$F3a"; do mkdir -p "$W/$(dirname "$f")"; git -C "$REPO" cat-file -p "$DEV:$f" > "$W/$f"; done
echo "develop blobs (hash-object, no -w): $(git hash-object "$W/$F1") $(git hash-object "$W/$F2") $(git hash-object "$W/$F3a")"
echo "--- PR1 strict"; (cd "$W" && git apply --check "$P1"); echo "check rc=$?"; (cd "$W" && git apply "$P1"); echo "apply rc=$?"; echo "PR1 blob after: $(git hash-object "$W/$F1") (head c4aad21223cc59bf5b8c70dc9e8fa65a875d92a3)"
(cd "$W" && git apply --check "$P1"); echo "PR1 re-apply control rc=$? (want 1)"
echo "--- PR2 strict then --recount"; (cd "$W" && git apply --check "$P2"); echo "strict check rc=$? (seat: 128)"; (cd "$W" && git apply --recount --check "$P2"); echo "recount check rc=$?"; (cd "$W" && git apply --recount "$P2"); echo "recount apply rc=$?"; echo "PR2 blob after: $(git hash-object "$W/$F2") (head e05c6bd21f64ad766083c72d0fc070ebeb478b7f)"
(cd "$W" && git apply --recount -R --check "$P2"); echo "PR2 reverse-on-applied control rc=$? (want 0: it is applied)"
echo "--- PR3 strict"; (cd "$W" && git apply --check "$P3"); echo "check rc=$?"; (cd "$W" && git apply --numstat "$P3"); (cd "$W" && git apply "$P3"); echo "apply rc=$?"; echo "PR3 product blob after: $(git hash-object "$W/$F3a") (head cf371028fb564ca0e55d9d9501c3efa1211b5bd0)"; echo "PR3 test blob after: $(git hash-object "$W/$F3b") (head 2b91446416f826b69dbd5a0ab6f4123c96d06349) lines=$(wc -l < "$W/$F3b")"
echo "--- PR3 86-line variant vs canonical 85-line section_2"; diff "$R/2026-09-20_ks1272-ornith35b-night/out.md.checker/section_2.diff" "$R/2026-09-20_ks1272-ornith35b-night/out.md.checker/section_2.decl.diff"; echo "diff rc=$?"; cat "$R/2026-09-20_ks1272-ornith35b-night/out.md.checker/section_2.opts"; echo; cat "$R/2026-09-20_ks1272-ornith35b-night/out.md.checker/decl_splice.out"; echo
echo "canonical == section_1 + section_2 bytewise:"; cat "$R/2026-09-20_ks1272-ornith35b-night/out.md.checker/section_1.diff" "$R/2026-09-20_ks1272-ornith35b-night/out.md.checker/section_2.diff" | cmp - "$P3"; echo "cmp rc=$?"
echo "scratch at $W (never deleted)"
