#!/bin/bash
# QA-W-DAEMON: protected sha256 / tree oids at the head vs the brief's values (section 0 item 4).
H=/private/tmp/claude-501/qwd/h
fail=0
chk() { local p="$1" want="$2"; got=$(git -C $H show HEAD:"$p" | shasum -a 256 | cut -c1-64); if [ "$got" = "$want" ]; then echo "EQUAL $p"; else echo "DIFF  $p got $got want $want"; fail=1; fi; }
T=crates/coagent-daemon/tests
chk $T/gate_r2.rs a1944e0c65afb1c356822f04240ee2cc03794b3df6f929d1b7ee3b8221939681
chk $T/gate_r3.rs 17cfcca984130c79d544269c1b74bf6e421ce666b9a57ca79d0c68bc2a3f71c3
chk $T/gate_r4.rs a2ca92a68cc5e433ebeb5c538f561f166d66b7e430031cb7270fa41ffd727ac2
chk $T/gate_r5_model.rs 022f47049bce6688760d28876de0fcf51132b003490957a54ef50c3acb5f33da
chk $T/gate_r6_model.rs 755820e3914666646b70caad03acc6e4ae0d6676010bfb5297b78de6bf598988
chk $T/gate_r6_model_wrapper.rs 2fb203a07390d43cfb8f71d1379e610c79196ecad9892031d7b2ff3d17e3d465
chk $T/gate_return.rs d2ca677d7409133bf53a9b5d6c681c29bc87dc396c3fc4bf32066f0e37fef04c
chk $T/gate/gate_attacks.rs b0f8d6b2bc2869a4f2417e987dc9726caffee9a53ba93c18ade8380b7b0f2439
chk $T/gate/gr2.rs caee212babc8072b14ddd771fb363e5d637c44c567d275c39685aaf74b42b34f
chk $T/gate/gr3.rs eddd91ae98da52dc1c043806d17a7e8f6dc10ed00bd68e9b9819ee95a00c98d8
chk $T/gate/gr4.rs bf8f2999dc657817aabd499cbdda58d5ee7dc9d1ed32d896fce76c134a212b00
chk $T/gate/gate_hostile/mod.rs fa18b0bd9501b4e9923f8425fc31a3798d9aa6b459ff68f10b7672ca7cff290b
chk $T/common/mod.rs 08ed3f585cf09a22bc0e1cc93a7e0b953cb43c37ee7107a66db6336282d0e5c9
chk $T/support/model.rs 0429231c54ab581f7079ba77d74ea6c5ecb202789aece583199c1b3ef03cb5d7
chk $T/p1p_support/mod.rs 7ff299ef6c718d77b37507d60a2c9f92066f20a2889039f088d7a3e76f587502
chk $T/p1p_ask_in_workspace.rs 9c9b3cdc0022eaa6b03df660cf441c219694856a2c73af59a92807a5b94c7b70
chk $T/p1p_configchange.rs 692a00a44bfeb3c4e7377b5367c5281ca7a5462c56d2fff34636d5573285b18c
chk $T/p1p_daemon_down_blocks.rs 7e4eb4db37557e2ef92621dfb49dc502e8c0e151a9cc4576770a3130ed65e7be
chk $T/p1p_deny_blocks.rs c2d38f2c2466abed7c02376941092427342fc5ee137fc34ad5deb1e65f02bbb5
chk $T/p1p_hook_mapping.rs 71efafc0fd8c0ec63081e51a91abe688f8c9dd488013fdbc53a884de61b0fcfc
chk $T/p1p_liveness.rs 53060f1d64f40609526f24cb0108717fe6c07025da9c425adc330b63f69b4990
chk $T/p1p_m1_unchanged.rs 74fd1d41969b90574d9063cc598bb2b297201db1aa765d0e103278da0a9b6f91
chk $T/p1p_taint_persists.rs 983de182a7ff2b68c59ec57e820414ea5e0c15add1a8e7628bbe041004860e15
chk $T/p1p_unknown_tool_strict.rs 9c6b299982898a6e8cd298b4bf462b35f5101a4786626d6e1eedf161153deabf
chk $T/ipc.rs 7ae8babc5d652f6881f891d6f93b21c65b8fd75db9f41b5887c699cdd4f58bf8
chk $T/startup.rs 67632552f2d0f1fc0bf703cfebce6f64c73e32ef3b5147ecf3125b5dbc1ff40c
chk $T/release_audit.rs 1ee5785a1412318dc71e69602f4c8842eb41d9769ec793cbf88f7a1600290ba0
S=crates/coagent-daemon/src
chk $S/store.rs 908e5708a8e802f35e410aa55a349706a95e74f124d1648ca5a0a986066d3b3c
chk $S/gate.rs 994487b32d95f8731ed658868882251f9c78a52404f31ac96efc0b45c4e67e59
chk $S/util.rs db6997e78c933c04b470862d5d80122827b6708f421714bc2de6ddf918db5141
chk $S/lib.rs 70f807250e904aa97e41955434c8a5217041fd5f077fd4c8115b54469fd2e2fa
chk crates/coagent-daemon/Cargo.toml e72bc8e6496db29c372ee8eff8a8b3fb08646847adb5698f47e27d5b34b3bfe5
chk Cargo.lock 23f0d93872c7b839029d684ec988f0cbad83c330dd8724c58d47802c48028368
chk Cargo.toml 7097708986745eef404065afae56726e69fa31bf05085729a4376355fdcfddda
# start values of the base (to confirm the builder's start claims)
for p in Cargo.lock Cargo.toml $S/relay_child.rs $S/datadir.rs $S/engine.rs $S/main.rs; do echo "BASE $p $(git -C $H show gh/main:$p | shasum -a 256 | cut -c1-64)"; done
echo "tree gate $(git -C $H rev-parse HEAD:$T/gate) want d9578cd094be5f52db7ee7d1d753010153ecf1cd"
echo "tree common $(git -C $H rev-parse HEAD:$T/common) want 6ed351ad7dde36aee5d046d2deaf57e0aed38f8f"
echo "tests listing diff base->head:"; diff <(git -C $H ls-tree -r gh/main -- $T) <(git -C $H ls-tree -r HEAD -- $T)
echo "existing test files modified/deleted/renamed (any crate):"; git -C $H diff --name-status --diff-filter=MDR gh/main...HEAD -- 'crates/*/tests/**'
echo "planted control: a wrong value must show DIFF:"; chk $T/ipc.rs 0000000000000000000000000000000000000000000000000000000000000000
exit $fail
