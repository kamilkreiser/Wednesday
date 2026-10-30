## QA GATE - TIER 1, round 1: GO WITH NOTES

**PR:** Secuura/Distributed_Secuura #1820, "KS-1823 api-gateway Dockerfile" (Seat R 65th)
**Head:** `b562a7e459a7c0b8e70f63fe76ee1011e54af470`. ls-remote of refs/pull/1820/head showed this SHA at the start and again at the end (2026-10-29T22:04:41Z). It matches the author's claim.
**Develop:** `e3d8456ec81d0b02172dd5a3060404815e797bde`, the same at both reads. The merge-base with the head is `593cd90c3131`.
**Gate:** QA gate 24. I report findings only. I fixed nothing, commented nowhere, pushed nothing and pushed no image. No box or registry was touched.

**COUNTS:**
- **Diff:** 4 files, +104 / -0. Exactly the declared 4. The instrument was `git diff --stat`, three-dot against both 593cd90c and e3d8456e, and both gave the same set.
- **Dockerfile + lines:** byte-equal to the mail. I checked with `cat -vet`: no CR and no trailing whitespace.
  - the comment `# KS-1823: the host directory can also hold rollback copies of the spec; the gateway reads secuura-api.yaml only.`
  - `RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*`
- **Red-first:**
  - spark_gate: 3 failed / 5 passed on BASE product code (R1 to R3 red, C1 to C5 green), and 8/8 on HEAD.
  - My own run: 8/8 at head. With only the rm line removed: 3 failed / 5 passed, the same R1 to R3. Restore was asserted by sha256 `a3dac7cc…`.
- **Whole api-gateway vitest suite, `--maxWorkers=3`, vitest 4.1.10, node v26.8.1:**
  - Head: 130 files, 1303/1321 passed, 18 failed.
  - Develop e3d8456e control: 129 files, 1297/1313 passed, 16 failed.
  - **16 of the failures are pre-existing on both sides,** in the same files and cells: ks1090 1, ks1195 7, ks1215 5, ks480 3. They are instrument failures, not PR failures (see I1).
  - **The other 2 failed at head only:** the ks1543 C7 and C2 eslint cells, both `Test timed out in 60000ms`. Re-run alone at head they pass 16/16. That is the load flake the author disclosed, not this change.
- **Image property** (local Docker 29.7.2, linux/arm64): decoys are present with develop's Dockerfile and absent with the head's (details under the image tests below).
- **Image-layer scan:** I extracted every layer blob of the final image with `docker save` and listed it with `tar -t`.
  - Develop image: 4 entries for the removed shapes (the positive control).
  - Head image: **0**. No layer of the final image carries the removed files.
- **My mutants of the Dockerfile against the PR test:** 7 run, 5 killed and 2 survived (F4). The script is `mutants.py`.
- **Merge-tree of the head onto e3d8456e:** CONFLICT. The tree is `b502447c1d5e5e3469556eae886176cc3cdf3db5`, with conflict markers in **both** Projects Documents files. Everything under `Blockchain/` merges clean: the merged tree differs from the head only by develop's 4 nft-certificate files.

---

### Findings, ranked (none blocks the merge)

**F1 (Low, completeness). The glob removes two name shapes. Six other backup shapes still reach the image.**
- **Where:** `services/api-gateway/Dockerfile:35`.
- **What:** I planted these in `docs/openapi` in my clone and built with the head's Dockerfile.

  | Shape | Result |
  |---|---|
  | `x.pre-test` | REMOVED |
  | `x.rollback-test` | REMOVED |
  | `secuura-api.yaml.pre-ks508` (the real host shape) | REMOVED |
  | `secuura-api.yaml.rollback-2026-08-27-ks661` (the real host shape) | REMOVED |
  | `.z.pre-test` (a dotfile; busybox `*` does not match a leading dot) | **STILL IN IMAGE** |
  | `secuura-api.yaml.PRE-upper` (the glob is case-sensitive) | **STILL IN IMAGE** |
  | `sub/y.pre-test` (the glob covers the top level only) | **STILL IN IMAGE** |
  | `x.bak` | **STILL IN IMAGE** |
  | `x.orig` | **STILL IN IMAGE** |
  | `x~` | **STILL IN IMAGE** |

- **Control:** all 10 shapes are present in the develop-Dockerfile image (`ls_develop_decoys.txt`).
- **The .dockerignore does not cover any of them.** `Blockchain/Dev/.dockerignore` has `docs` then `!docs/openapi`, which re-includes the whole directory. Its `*.md` is root-only, which is why WORKFLOWS.md and TRACK2_OPENAPI_MIGRATION.md also ship. No `.dockerignore` sits beside the api-gateway Dockerfile.
- **Scope:** the author's mail already states "the line removes two name shapes only". The two shapes that actually sit on the demo host are covered, so this is not a regression.
- **Possible follow-up:** an allow-list (`COPY docs/openapi/secuura-api.yaml ./docs/openapi/`), or `.dockerignore` lines for these shapes. That would also keep them out of the build context and the builder layer (F2).
- **Reproduce:** plant the files above, then run `docker build -f services/api-gateway/Dockerfile Blockchain/Dev`, then `docker run --rm --entrypoint ls <img> -la /app/docs/openapi`.

**F2 (Info, by design). The backups still enter the build context and the builder-stage layer.**
- The rm runs in the `builder` stage. The final stage copies the post-rm directory (`COPY --from=builder /app/docs/openapi`, Dockerfile:71), so the final image is clean; the layer scan above shows 0 entries.
- The files are still uploaded as build context, which matters for a remote `az acr build`. They also stay in the builder's `COPY docs/openapi/` cache layer on the build host, and in any `--target builder` image.
- The .dockerignore route from F1 would close this too.

**F3 (Low, robustness). A directory with a matching name breaks the build.**
- **What:** I planted `docs/openapi/old.rollback-dir/` and built with the head's Dockerfile.
- **Result:** `rm: './docs/openapi/old.rollback-dir' is a directory`, then `exit code: 1`. The build failed.
- **Why it is Low:** it fails closed, and no such directory exists today.
- **What does not fail:** a clean tree with no match. busybox `rm -f` on an unmatched literal glob gives rc 0, and the clean build passed.
- **Possible fix:** `rm -rf`, or `find … -type f`.

**F4 (Info, test strength). The text test pins the line, not the image.**
- **Mutants that survive the 8 cells:**
  - M4: a second `COPY docs/openapi/ ./docs/openapi/` after the rm, which re-imports the backups.
  - M5: the runtime stage also copying `docs/openapi` from the build context.
- **Mutants that are killed:**
  - M1 (rm commented out), M6 (rm without `-f`, the build-breaking form) and M7 (`|| true` appended).
  - M2 and M3, which are functionally equivalent placements (after `npm run build`; in the runtime stage). The test over-constrains here.
- **What this means:** the image property is proven only by the Docker builds (the author's and mine), not by CI. This is acceptable for a +2 line change.

**F5 (Info, merge-prep). Both docs conflict textually, not only the flow doc's section number.**
- **Flow doc** (lines 5787 to 5836 of the merged blob): two `<h2>118.` sections. The renumber to 119 is as the author said.
- **QA cheat sheet** (lines 5877 to 5916): KS-1823 and KS-1836 entries appended at the same point.
- **Resolution:** keep both in each file. The conflicts are docs-only, and no code path conflicts.

**Runtime check (item 5): there is no reader of the backups.**
- I grepped `services/api-gateway/src` (tests excluded) for `.pre-`, `rollback`, `docs/openapi`, `express.static` and `readdir`.
- The only spec reader is `index.ts:590-605`. It reads the fixed path `docs/openapi/secuura-api.yaml`, and the dev-only `fsWatch(specPath)` watches that same file.
- No static mount serves `docs/openapi`. The only `readdirSync` is startup-migrations.ts on `migrations/`.
- **Control:** the same grep found the real reader at index.ts:590.
- secuura-api.yaml is byte-identical in the develop image, the head image and the clone (sha256 `e5c450a6…`).

---

### TESTED / NOT TESTED / HOW

**TESTED**
- **Diff scope.** The 4 files, and the + lines byte-checked.
- **Multi-stage layout.**
  - The COPY at :32 and the RUN at :35 are both in `builder`.
  - The final stage copies the directory from builder after the rm.
- **Red-first** (spark_gate, then my own swap).
- **The whole suite**, at head and with develop as the control.
- **4 Docker builds, run on the local daemon only:**
  - develop's Dockerfile with decoys: built;
  - the head's Dockerfile with decoys: built;
  - the head on a clean tree: built, rc 0;
  - the head with a directory decoy: failed (F3).
- **Container listings** of `/app/docs/openapi`, and the layer scan of both images.
- **Runtime grep,** and the merge-tree.

**NOT TESTED**
- **A running gateway container.** I did not boot `node dist/index.js` or hit `/api/docs/openapi.yaml`.
- **The cloud path.** No `az acr build`, and no amd64 build; mine were arm64 only.
- **The demo host.** The two real backups stay on the host by design; I did not look at it.
- **The doc content.** I did not run html_docs_check and did not proof-read the doc sections beyond locating the conflict.
- **The rest of the author's checks:** tsc, eslint and the test-types ratchet on the new file; audit:gate and audit:locks.
- **Other suites:** the four platform suites, Node 24, and the develop control with a directory decoy.

**HOW**
- **The clone.** I made a `git clone --shared` of the Secuura checkout into the then-non-existent path `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e5f54089-c0c9-4cb7-8aa3-cf2e956a3e73/scratchpad/gate24/clone`.
  - Its toplevel was asserted equal to that path before any write.
  - Its origin was set to `git@github.com:Secuura/Distributed_Secuura.git`, with `core.sshCommand` copied from the checkout (a read).
  - It fetched `refs/pull/1820/head` and develop only.
- **node_modules.** The root and api-gateway node_modules were symlinked from the checkout; they were untracked and never added. TMPDIR was `/tmp/g24`.
- **Decoys.** The decoys were planted in my clone only and removed after the builds. `git status` shows only the 2 symlinks.
- **Images.** I created `gate24-develop-decoys` `7fa82dbb`, `gate24-head-decoys` `3e312f00` and `gate24-head-clean` `e1a92b5d`. Each carried only my tag, and each was removed by ID (rc 0). The dir-decoy build produced no image. Containers ran with `--rm`; 0 containers from my images remain.
  - The author's three `r65-ks1823-*` tags remain, untouched by me.
  - My builds left BuildKit cache entries, which I did not prune.
- **spark_gate.sh**
  - **Invocation:** `<clone> 1820 b562a7e4… develop <test> --node-modules <checkout>/Blockchain/Dev/node_modules --work …/spark_work --out …/spark`.
  - **Result:** rc 0. It asserted the head as the tip, with merge-base 593cd90c and base tip e3d8456e, and reported a diff of 4 files, +104 / -0.
  - **Counts:** targeted HEAD 8 passed / 0 failed; BASE 5 passed / 3 failed.
  - **Why it worked this time:** passing the **root** node_modules avoided gate 23's "vitest not found".
- **Artefacts in this folder:**
  - `mutants.py` and `mutants_run.log`;
  - `spark_facts.json`;
  - `ls_develop_decoys.txt` and `ls_head_decoys.txt`;
  - `develop_layers_openapi.txt` and `head_layers_openapi.txt`.

### Instrument errors / caveats of my own
- **I1. The 16 shared suite failures come from my resolution, not the PR.** `@secuura/shared` resolved through the symlinked node_modules to the checkout's prebuilt `packages/shared/dist`, which lacks `isProvisioningCapable` (`TypeError: isProvisioningCapable is not a function`, ks480, ks1195 and ks1215). ks1090 (the tsc baseline) is also red on both sides.
  - These failures are identical at head and develop, so they are not attributable to the PR.
  - The author's warm run reported 1321/1321 with a fresher shared build. I did not rebuild shared.
- **I2. Two attempts were refused by hooks and re-issued.** A `merge-tree` written with a `$VAR` clone path was refused, and so was an `rm` of my own decoy folder written as a `$VAR`. Both were re-issued with literal scratchpad paths. Nothing ran against the Secuura checkout.
- **I3. Part of the clean build came from cache.** In `gate24-head-clean`, the final-stage `COPY --from=builder /app/docs/openapi` layer was CACHED, a content-identical layer from an earlier build on this daemon. Its mtimes are older than my clone's files. The rm step itself executed (`DONE 0.1s`, not cached).

### FIX-BEFORE-MERGE
(none)

Optional follow-ups:
- F1/F2: an allow-list COPY or `.dockerignore` patterns for the other backup shapes.
- F3: `rm -rf`, or a `find -type f`.
- F5: resolve both doc conflicts at merge-prep. Renumbering the flow doc to 119 is not the whole job: the cheat-sheet conflict needs resolving too.
