#!/bin/bash
# QA-WIN-FOLLOWUP item 10: the builder brief's section 0 item 4 values against the HEAD (and the base).
C=/private/tmp/claude-501/qwf/clone; REV=${1:-cf41a77e984b7e8e274ff4cc97136cf9d1987892}
F="crates/coagent-daemon/src/engine.rs b2656f8b8e8e6506a7a4ef334c8e885e61d1667c28010a0af51546fda3c116c4
crates/coagent-daemon/src/main.rs 26e0b79f113b7c20da0dd3e484162bcda09db492299031efda38c4ac7c6dd674
crates/coagent-daemon/tests/win_datadir.rs 117dd6185c89218fb4d510cf21c5a8453715705e0cffd980ce3fc6762a8a7efa
crates/coagent-daemon/tests/win_guest.rs a132b312921039caca31630027278df2f756e25c836464baa615f4bef83b1ec9
crates/coagent-daemon/tests/win_support/mod.rs 09261764085942896ad417f22ccbbc95c00b3baebe9c4110acd89960a92d019d
crates/coagent-relay/tests/hygiene.rs bc552b8579638e3236bf8c697542d056e44fe38ec840da791dd8e2f3e7a6ea40
crates/coagent-cli/tests/support/mod.rs 2e543fb574ac752d229b1e7df7cf32a6359e2e6b4a075a5b3897c3ea1973d04f
crates/coagent-relay/red-controls/run.py 1a04fcb14882f10d1319a57e80ba690561e378f365f9b740d42a0b2735d6dabc
crates/coagent-relay/red-controls/OUTPUT.txt 08a15f8549f9ff376ad25a9f6bfe19d5620447efaef08dbbb5a88fd30d5cbe05
Cargo.toml 7097708986745eef404065afae56726e69fa31bf05085729a4376355fdcfddda
Cargo.lock 23f0d93872c7b839029d684ec988f0cbad83c330dd8724c58d47802c48028368
crates/coagent-daemon/Cargo.toml e72bc8e6496db29c372ee8eff8a8b3fb08646847adb5698f47e27d5b34b3bfe5
crates/coagent-relay/Cargo.toml d01f951d73aa1c0d8871dca06c4914c813747ab41db44f1ee8381cdf95d695da
crates/coagent-cli/Cargo.toml 2e8c616ffc61865f3c0948fc227cb6d7ab9518b61a7a48a7434bae7c8b6c31c6
scripts/check.sh 5e4349e029542fc8a4d98b266e74c6a1241542faaaaa6d02fbb8a11314c03ce1
scripts/env.sh 27f8f5ed470d473af5072b33e654591d96481ddfee472d0c323ddf8b14e8114c
scripts/test-daemon.sh 577551de91e3808ddb7afc9dd4efa6f37c92bab996e1edb4c397036c3a7c8cca
scripts/test-p1p.sh fef1f3287448186844eca694cbe5d0ed5e73a1845671624ce37be4a8f97ed15c
scripts/windows/build.sh 691d4bb086f7d1b41396a57b2fcd2e642947976cb18e154b14b555fec728df7a
scripts/windows/README.md 00900735dafc55b7bb2762dcca9e09b1feb8bd2f58fc659abc2845c5c9e13038
rust-toolchain.toml 6b1cf8341d9a08d76c6deb1e9df90a0b208d0ef0d00ee05e0173e9cd4f0f425d
deny.toml 4ce016092ac1764c4adba291d8d044f26d90debf1b1331088e248590d2c58b44
.gitignore 2757b26c8f08bedda9a8bba3856c292f0fae06ac68dd897e1760223bfe016e00"
TR="crates/coagent-daemon/tests/gate d9578cd094be5f52db7ee7d1d753010153ecf1cd
crates/coagent-daemon/tests/common 6ed351ad7dde36aee5d046d2deaf57e0aed38f8f
crates/coagent-audit c90e44c23d8b6677dc2b46e06cae997b04849258
crates/coagent-audit-host 549bb5176d2a3152e55587d3ccc3fbc47be89578
crates/coagent-relay/src 92e210fc5240fc335fdb6b29e8cc6d84475a353e
crates/coagent-cli/src 0f55246dcc8a35ef61489b72d91737597fe7539e
crates/coagent-ipc 4f72ab6774c943cc1980b701a53cc16fa4b0284e
crates/coagent-policy 289b4406e97ee712763703d3dc33ff35d1697c7d
crates/coagent-proto b391f9e873415aa1e8479a57ec87a60b835f2094
crates/coagent-crypto 71a06b593ca95e23c47f74b039333f2b0d8a276b
crates/coagent-roster 2761baf4ea04f165af447ca4af544270932476cf
crates/coagent-hook 2af2a6002bb8b6345e8e227e4543b5bf9c47f2c1
crates/coagent-mcp 80a59dc294086f25d0f96fa2cb47f50213dfcf38
scripts/windows 42812004872ef39e34f57b5a215bb000d450840e
crates/coagent-daemon/src 8c57f887dc9c0e091f62ac3c91736e52b5add71a"
eq=0; ne=0
while read p v; do got=$(git -C $C show "$REV:$p" | shasum -a 256 | cut -d' ' -f1); if [ "$got" = "$v" ]; then eq=$((eq+1)); else ne=$((ne+1)); echo "DIFF file $p"; fi; done <<< "$F"
while read p v; do got=$(git -C $C rev-parse "$REV:$p"); if [ "$got" = "$v" ]; then eq=$((eq+1)); else ne=$((ne+1)); echo "DIFF tree $p ($got)"; fi; done <<< "$TR"
echo "$REV: $eq equal, $ne different"
L=$(git -C $C ls-tree -r $REV -- crates/coagent-daemon/tests | grep -v 'tests/win_'); echo "daemon test listing without win_: $(echo "$L" | wc -l | tr -d ' ') lines, sha256 $(echo "$L" | shasum -a 256 | cut -c1-64)"
echo "positive control (a planted wrong value):"; got=$(git -C $C show "$REV:Cargo.toml" | shasum -a 256 | cut -d' ' -f1); [ "$got" = "0000" ] && echo EQUAL || echo DIFF
