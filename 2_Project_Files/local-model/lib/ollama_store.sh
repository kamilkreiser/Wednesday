# ollama_store.sh — ONE resolver for "which Ollama models dir does the fleet use". Source it, then:
#
#   store="$(ollama_store_resolve "<override-or-empty>")" || <refuse>
#
# Written 2026-10-05 (Kam: "clear up the dev drive"; policy
# 1_Project_Definition/Policies/2026-10-05_drive-hygiene-policy.md). Until today night_run.sh, doctor.sh and
# set_ollama_pointers.sh PINNED the in-tree copy 2_Project_Files/local-model/models, while start_ollama.sh
# (the thing that actually starts the server) already preferred the SYSTEM store. Two answers to one
# question is how a 128 GB duplicate stays on the drive: the pin made the copy look load-bearing.
#
# ORDER (same preference as start_ollama.sh:31-33, plus the ornith requirement):
#   1. the deliberate override (arg 1: night_run passes NIGHT_OLLAMA_MODELS) — used ONLY if it holds the
#      required manifest; an override WITHOUT it is REFUSED (rc 3), never silently replaced: whoever set it
#      meant something, and a wrong deliberate pointer should be loud.
#   2. the SYSTEM store /Volumes/DevMASTER/SYSTEM/ollama/models (launchd's OLLAMA_MODELS, Kam's live store)
#   3. the in-tree fallback 2_Project_Files/local-model/models (moved to G-DRIVE Scratch 2026-10-05; kept
#      in the chain so a machine that still has an in-tree store keeps working — the portability rule)
#   none holds it -> rc 2, nothing printed on stdout.
#
# THE 09-16 PROTECTION IS KEPT: a stray global OLLAMA_MODELS is NEVER consulted (it is not an input here),
# and every candidate must hold manifests/registry.ollama.ai/library/<OLLAMA_STORE_REQUIRE> (default
# ornith/35b) — so no env var can point the fleet at a store without ornith.
#
# Arg 2 / arg 3 replace the SYSTEM and in-tree candidates — FOR TESTS ONLY (they are positional, not env,
# so nothing in a launchd environment can set them by accident).
ollama_store_resolve() {
  local override="${1:-}"
  local system="${2:-/Volumes/DevMASTER/SYSTEM/ollama/models}"
  local intree="${3:-$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/models}"
  local rel="manifests/registry.ollama.ai/library/${OLLAMA_STORE_REQUIRE:-ornith/35b}"
  if [ -n "$override" ]; then
    if [ -f "$override/$rel" ]; then echo "$override"; return 0; fi
    echo "ollama_store_resolve: REFUSED — override $override lacks $rel" >&2; return 3
  fi
  local s
  for s in "$system" "$intree"; do
    if [ -f "$s/$rel" ]; then echo "$s"; return 0; fi
  done
  echo "ollama_store_resolve: no store holds $rel (checked $system, $intree)" >&2; return 2
}
