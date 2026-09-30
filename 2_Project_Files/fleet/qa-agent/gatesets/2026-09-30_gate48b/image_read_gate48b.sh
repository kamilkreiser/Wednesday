#!/bin/bash
# image_read_gate48b.sh — the drafter's READ-ONLY look at the issuer probe images ALREADY on this Docker host (no build, no run, no pull, no
# remove): `docker image inspect` of each named image — its ID, created time, the sha256 of its RootFS.Layers list (the content), and its
# compose project label. The point it measures: an image ID carries the compose `-p` project label, so two builds of byte-identical content under
# different `-p` names have DIFFERENT ids; "same digest" is only meaningful between builds under the SAME `-p`. The content equality instrument is
# the RootFS.Layers list. CONTROL: a non-issuer image (dev-vc-issuer) must read a DIFFERENT layer-list hash (the comparison can fail).
# Writes nothing outside this output. Usage: image_read_gate48b.sh
set -u
echo "image_read_gate48b $(date -u +%Y-%m-%dT%H:%M:%SZ) | docker $(docker version --format '{{.Server.Version}}' 2>&1)"
REF=""; N=0; SAME=0
for i in b47probe-issuer-frontend g48aprobe-issuer-frontend b48probe-issuer-before b48probe-issuer-frontend dev-vc-issuer; do
  id="$(docker image inspect --format '{{.Id}}' "$i" 2>/dev/null)"; rc=$?
  if [ "$rc" -ne 0 ]; then echo "  $i: ABSENT (inspect rc $rc)"; continue; fi
  ls="$(docker image inspect --format '{{json .RootFS.Layers}}' "$i" | shasum -a 256 | cut -c1-16)"
  nl="$(docker image inspect --format '{{len .RootFS.Layers}}' "$i")"
  cr="$(docker image inspect --format '{{.Created}}' "$i")"
  pj="$(docker image inspect --format '{{index .Config.Labels "com.docker.compose.project"}}' "$i")"
  [ -z "$REF" ] && REF="$ls"
  [ "$i" != dev-vc-issuer ] && { N=$((N + 1)); [ "$ls" = "$REF" ] && SAME=$((SAME + 1)); }
  echo "  $i: id ${id:7:12} | created $cr | RootFS.Layers $nl, list sha256 $ls | compose project '$pj'"
done
CTL="$(docker image inspect --format '{{json .RootFS.Layers}}' dev-vc-issuer 2>/dev/null | shasum -a 256 | cut -c1-16)"
echo "  issuer probe images with the SAME layer list as the first: $SAME of $N | CONTROL dev-vc-issuer layer list $CTL differs: $([ "$CTL" != "$REF" ] && echo True || echo False)"
[ "$N" -ge 2 ] && [ "$SAME" = "$N" ] && [ "$CTL" != "$REF" ] && echo "IMAGE READ OK: $SAME issuer probe images share one content (layer list $REF); their ids differ only where the compose project label differs" && exit 0
echo "IMAGE READ: the issuer probe images do NOT share one layer list, or the control failed"; exit 1
