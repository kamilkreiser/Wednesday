---
date: 2026-11-22
type: session-sheet
source: Friday; every command below was run on this Mac on loopback on 2026-11-22 at merged main 3337192
status: live for the session of 2026-11-23; re-check the BIN path that morning
---

# CoAgent: the first link between the Mac and the Windows PC

Client: General. Project: CoAgent (Claude to Claude).

**What this proves:** the two machines link through CoAgent over the home network and pass a message each way. No Claude Code session and no gate on either side in this first run.

**Your time:** about 30 minutes, at both machines. **You need:** the USB stick.

**Your ruling this rests on:** card `general-c2c-win-mac-relay-home-network-1120`, "Yes, for each Windows test session". The Mac's relay listens on the home network only while this session runs. You start it and you stop it.

## At the Mac: three Terminal windows

Paste each block whole. Wait for Friday's word on the board between blocks.

**Window 1, the relay.** It prints "HOSTING A RELAY" and then a reminder line every minute. Leave it running.

```
BIN=/private/tmp/claude-501/mcwd1/target/debug; R=/private/tmp/c2c-c1; mkdir -m 700 $R; IP=$(ipconfig getifaddr en0); echo "Mac address: $IP"; "$BIN/coagent" relay --listen ${IP}:7443 --allow-non-loopback --status-secs 60 --identity-file $R/relay.id 2>&1 | tee $R/r.log
```

If macOS shows a dialog asking whether `coagent` may accept incoming connections, or about the local network: choose **Allow**. Tell Friday the dialog's words.

**Window 2, the host program.** It prints nothing and keeps running.

```
BIN=/private/tmp/claude-501/mcwd1/target/debug; R=/private/tmp/c2c-c1; "$BIN/coagentd" --data-dir $R/h --relay-url "$(sed -n 's/^url: //p' $R/r.log | head -1)" --relay-pin "$(sed -n 's/^fingerprint: //p' $R/r.log | head -1)" --idle-exit-secs 86400 2> $R/h.log
```

**Window 3, the invitation, only when Friday says "make the invitation".** Put the USB stick in the Mac first. It prints "line written to the stick".

```
BIN=/private/tmp/claude-501/mcwd1/target/debug; R=/private/tmp/c2c-c1; "$BIN/coagentd" ctl --data-dir $R/h '{"v":1,"id":1,"cmd":"invite"}' | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["line"])' > /Volumes/Untitled/c2c-line.txt && echo "line written to the stick"
```

Eject the stick and carry it to the PC. The invitation works once and for 10 minutes. If it runs out, paste the Window 3 block again.

## At the PC

The PC's helper shows each step on its screen. In short:

1. Open a Command Prompt and type the three lines it shows (make a folder, set one variable, start the program).

2. When it asks, put the stick in, open a second Command Prompt, and type the one `join.cmd` line it shows with the stick's drive letter.

3. Wait for "paired", then for Friday to say "connected".

## At the end

1. PC: press **Ctrl-C once** in the first Command Prompt (the C key, not Break).

2. Mac: press **Ctrl-C** in Window 2, then in Window 1. The relay is then closed.

3. The file on the stick is spent after the join. Delete it when you like.

## What was measured on 2026-11-22 (Mac only, loopback)

- The three blocks above ran under zsh with the address set to 127.0.0.1: relay up, host started, invitation written to a file (360 bytes, one line), a guest joined from that file, `connected: true`, all stopped cleanly, no listener left.
- A full run with a request and a reply each way: both read on the far side; the message texts appeared in none of the three logs (count 0, with a control of 1).

## Not yet measured

- The relay listening on the home-network address (it is opened only for the session).
- Whether macOS shows a dialog for it. The Mac's firewall read "disabled" at 21:38 on 2026-11-22.
- The PC's route to the Mac. The PC reports it in part 1 of its work order.
- Anything on Windows beyond the PC's earlier test runs.
