---
date: 2026-11-23
type: session-sheet
source: Friday; Mac blocks 1 and 2 ran on loopback on 2026-11-23 (seat C2-REHEARSAL, its report section 9); block 3 is written, not run
status: live for the next session; Friday re-checks the BIN path and makes the folder on the day
---

# CoAgent: a Claude agent on each machine, talking over the link

Client: General. Project: CoAgent (Claude to Claude).

**What this proves:** a Claude agent on the PC and a Claude agent on the Mac exchange a request and a reply each way through CoAgent. The Mac side runs WITH the gate: you approve what the Mac's agent reads and sends. The PC side runs without prompts, as you ruled on 23 Nov for development.

**Your time:** about 35 minutes, at both machines. **You need:** the USB stick, plugged into the MAC at the start.

**Before you sit down, Friday has already:** made the session folder on the Mac, checked the Mac's address, and told the PC's helper.

Every step below names its machine first. Do nothing on the other machine until the step says so.

## Step 1. MAC: Terminal window 1, the relay

Paste the block. The window shows one line, "Mac address", and then stays blank. That is correct: everything goes to a log Friday reads. If macOS shows a dialog, choose Allow and tell Friday its words.

```
BIN=/private/tmp/c2reh1123/target/debug; R=/private/tmp/c2c-c2; IP=$(ipconfig getifaddr en0); echo "Mac address: [$IP]"; if [ -z "$IP" ] || [ ! -d $R ]; then echo "STOP: no address on en0, or no folder $R: tell Friday"; else "$BIN/coagent" relay --listen ${IP}:7443 --allow-non-loopback --status-secs 60 --identity-file $R/relay.id > $R/r.log 2>&1; fi
```

## Step 2. MAC: Terminal window 2 (Command-N), the gated host

Paste the block. It prints one line beginning "relay:" and then nothing. If it prints "STOP", wait ten seconds and paste it again.

```
BIN=/private/tmp/c2reh1123/target/debug; R=/private/tmp/c2c-c2; U="$(sed -n 's/^url: //p' $R/r.log 2>/dev/null | head -1)"; P="$(sed -n 's/^fingerprint: //p' $R/r.log 2>/dev/null | head -1)"; if [ -z "$U" ] || [ -z "$P" ]; then echo "STOP: no url or fingerprint in $R/r.log yet: wait for Window 1, then paste this again"; else echo "relay: $U"; "$BIN/coagentd" --data-dir $R/h --gate --workspace $R/ws-h --exclude '<ws>/secret/**' --gate-dir $R/plugin-h --idle-exit-secs 86400 --relay-url "$U" --relay-pin "$P" 2> $R/h.log; fi
```

Tell Friday "Mac ready". Wait for her word before going to the PC.

## Step 3. PC: Command Prompt, the guest program

The PC's helper shows three lines to type. Type them. The window then sits. Tell Friday "PC started".

## Step 4. MAC: nothing to type

Friday writes the invitation onto the stick and ejects it. She tells you when to pull it out. It is valid for ten minutes.

## Step 5. PC: the join

Plug the stick in. Open a second Command Prompt and type the join line the helper shows, with the stick's drive letter. You should see the word "paired". Friday confirms "connected".

## Step 6. MAC: Terminal window 3, the Mac's Claude agent

Only after Friday says "connected". Paste the block. Accept the folder-trust question. Then type `/mcp` and check that it lists `link`.

```
R=/private/tmp/c2c-c2; MODEL="$(python3 -I -c 'import json; print(json.load(open("/Volumes/Laptop-DEV/FRIDAY/0_Brain/dashboard/data/models_latest.json"))["levels"]["haiku"]["model_id"])')"; echo "model: [$MODEL]"; if [ -z "$MODEL" ]; then echo "STOP: no model id: tell Friday"; else cd $R/ws-h && claude --model "$MODEL" --plugin-dir $R/plugin-h; fi
```

Tell Friday "Mac agent up". She then starts the PC's agent through its helper; it sends the first request by itself.

## Step 7. MAC: in the Claude session of window 3, paste this

```
Check your coagent inbox with the inbox_read tool. Then use the coagent send tool, kind reply, re set to that message's id, text exactly: C2W-2 reply from the Mac agent. Then use the coagent send tool, kind request, text exactly: C2W-3 request from the Mac agent: please reply.
```

The gate asks you each time: once for the read, once for each send. Each send shows the exact text going out. Press Yes. You should see the PC's request inside a block marked as untrusted data from the peer.

## Step 8. MAC: when Friday says the PC has replied, paste this

```
Read your coagent inbox with inbox_read and show me what arrived.
```

Press Yes. You should see "C2W-4 reply from the Windows agent".

## Step 9. Close down, in this order

1. PC: in the first Command Prompt, Ctrl-C ONCE (the C key).

2. MAC: window 3, the Claude session: Ctrl-C twice.

3. MAC: window 2, the host: Ctrl-C.

4. MAC: window 1, the relay: Ctrl-C. That closes the listener.

## What Friday can and cannot do during the session

- She reads the Mac's status and the counts of unread messages. She cannot read the messages themselves on the gated Mac: only your approved session can.
- She does not send anything by hand from the Mac. A hand-typed send would bypass your Yes (found in rehearsal; it goes to the project as a fix).

## Measured and not measured

- Ran on loopback on 23 Nov: blocks 1 and 2 (with the address set to this Mac itself), a join, connected in 2 seconds, clean stops.
- Ran on the PC on 23 Nov: Claude Code loading our tool and calling it once (rehearsal, no link).
- Not yet run anywhere: block 3 as a whole; a gated Mac session reading over a separately started relay; the two agents completing the exchange.
