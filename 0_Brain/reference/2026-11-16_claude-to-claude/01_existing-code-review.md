# CoAgent / Claude Bridge v0.4.4 — existing code review

**Date:** 2026-11-16
**Reviewed (read-only):** `/Volumes/Laptop-DEV/!CODING/Claude to Claude/claude-bridge`
**Purpose:** an accurate picture of what exists and how far it is from the new goal (link any two agents; CONTROLLED and APPROVED-TRUST modes; observe and gate the remote agent's actions). This is not a design for the new system.

**Method and limits**

- Every source file under `src/`, `worker/`, `bin/`, `electron/main.js`, `electron/preload.js`, `.claude/`, `CLAUDE.md`, `README.md`, `scripts/check-bridge.sh`, `scripts/pack.js` and `site/downloads/install.sh` was read in full. `electron/split-view.html` was read for its script block and security-relevant markup, not its CSS. `src/ui/style.css`, `install.ps1` and `_setup_template.ps1` were only searched, not read.
- **Nothing was executed.** Every behaviour described below is from reading the code. Findings that describe an attack chain are marked "by reading" — they are what the code does on paper and have not been reproduced.
- The folder is **not a git repository** on this disk (no `.git`), so there is no history to check and I could not verify what has been pushed to `kamilkreiser/claude-to-claude`.
- Paths below are relative to the project root. Line numbers are from the files as they are on disk today.

---

## 0. Verdict in one paragraph

CoAgent is a working **encrypted chat bridge with a Claude Code side-car**, not an agent-collaboration control plane. Its transport idea (local daemon per user, dumb relay, session code, X25519 + AES-GCM) is sound and reusable as a concept. Everything the new goal depends on — peer identity, authenticated pairing, visibility of the agent's actions, enforced approvals, trust grants and revocation, audit history — is absent, and the one feature that looks like approval ("Instruction Approval") is a browser-side decoration that the same build bypasses in three other ways. More urgently, the current build takes remote text and types it into a local terminal, and by reading the code a session peer can reach shell command execution on the other side without any approval. **The realistic path is a rewrite of the core (daemon, protocol, UI, Claude integration) that keeps the crypto primitives, the tunnel manager and the relay concept.** The current build should not be used with an untrusted counterpart.

---

## 1. What exists and works

### 1.1 Component map

| Component | File | Lines | Role |
|---|---|---|---|
| Bridge agent (local daemon) | `src/bridge-agent/index.js` | 801 | HTTP + WebSocket server for the UI on port 3847, TCP IPC server for the MCP server on 3849, WebSocket client to the relay, in-memory message store, key exchange |
| MCP server | `src/mcp-server/index.js` | 305 | stdio MCP server spawned by Claude Code; 5 tools; talks to the bridge agent over TCP 3849 |
| Relay | `src/relay/embedded.js` (+ 4-line `src/relay/index.js`) | 289 | In-memory WebSocket fan-out keyed by session code |
| Shared | `src/shared/protocol.js`, `crypto.js`, `constants.js`, `logger.js` | 59 / 100 / 29 / 74 | Envelope + message shape, session-code generator, X25519/HKDF/AES-GCM, ports, file logger |
| Tunnel | `src/tunnel/manager.js` | 450 | Finds or downloads `cloudflared`, opens a Cloudflare quick tunnel to the local relay |
| Web UI | `src/ui/app.js`, `index.html`, `style.css` | 673 / 133 / 523 | Connect / waiting / two-tab chat screens; instruction-approval popup |
| Cloudflare worker | `worker/api.js` | 205 | Session registry (code → tunnel URL) **and** paid-download token logic. `worker/wrangler.toml:2` sets `main = "api.js"`, so `worker/session-registry.js` (60 lines) is a superseded duplicate |
| Electron shell | `electron/main.js`, `preload.js`, `split-view.html` | 337 / 22 / 532 | Split window: xterm.js terminal on a `node-pty` shell on the left, the web UI in an iframe on the right |
| CLI entry | `bin/claude-bridge.js` | 124 | Mode switch (`--mcp`, `--relay`, default bridge), update check, registers the MCP server with Claude Code |
| Claude instructions | `CLAUDE.md`, `.claude/skills/coagent-collaborate/SKILL.md`, `.claude/settings.json`, `scripts/check-bridge.sh` | 65 / 45 / 15 / 34 | Tell Claude to poll and obey the bridge; Stop hook that feeds unread messages back to Claude |
| Packaging | `scripts/pack.js`, `site/downloads/install.sh`, `install.ps1` | 185 / 356 / — | Tarball/zip of source + installer scripts |

Present but out of scope for this review: `site/` (marketing site, demo pages, 36 release archives under `site/downloads/`), `dist/` (36 archives), `promo/`, `MARKETING-PLAN.md`, `MARKETING-PLAYBOOK.md`, `assets/media/`, `scripts/capture-media.js` + `voiceover*.js`, and `agents/` — a Docker stack for an Agent Zero "social media manager" (`agents/docker-compose.yml:2`), unrelated to the bridge product.

### 1.2 Data flow

```
Claude Code ──stdio MCP──> mcp-server ──TCP 3849 (JSON lines)──┐
Browser/Electron UI ──WS ws://localhost:3847/ws────────────────┤
                                                               v
                                                        bridge-agent  (in-memory store)
                                                               │ WS (ws://localhost:3848 or wss://<x>.trycloudflare.com)
                                                               v
                                                     relay (runs on the CREATOR's machine)
                                                               │
                                                               v
                                                    the other side's bridge-agent
```

- The **session creator hosts the relay**. `_createSessionWithRelay` starts the embedded relay on 3848 (`src/bridge-agent/index.js:376`), opens a Cloudflare quick tunnel to it (`:389-404`), then connects to its own relay on localhost (`:417-420`).
- On `session_created` the creator posts `{code, tunnelUrl}` to `https://coagent.live/api/sessions/register` (`src/bridge-agent/index.js:23`, `:565-578`).
- The joiner looks the code up at `/api/sessions/lookup/<code>` (`:475-490`) and connects to the returned `wss://` URL (`:440-443`). If the lookup fails it falls back to `ws://localhost:3848` (`:448`, `:456`).
- A message from the UI or from Claude goes through `_sendChannelMessage` (`:300-340`): store locally, encrypt if a shared secret exists, send to the relay, echo to all local UI sockets and all IPC sockets (`:350-358`).
- An incoming message is decrypted (`:646-669`) or accepted as plaintext (`:670-674`), stored, and echoed to local clients.

### 1.3 Wire protocol

Envelope: `{ type, payload, ts }` (`src/shared/protocol.js:17-19`). No protocol version field, no sequence number, no message authentication outside the optional AES-GCM payload.

Chat message body: `{ id, channel, sender: {peerId, name, type}, content, timestamp, metadata }` (`src/shared/protocol.js:29-42`). `sender.type` is `human`, `claude` or `system`. A "file" is the same message with `metadata: {type:'file', fileName, language}` and the file text in `content` (`:44-57`). Two channels only: `human` and `claude-team` (`src/shared/constants.js:19-20`).

| Hop | Types |
|---|---|
| Bridge → relay | `create_session`, `join_session`, `channel_message`, `key_exchange`, `ping` (`src/relay/embedded.js:103-119`) |
| Relay → bridge | `session_created`, `session_joined`, `session_peer_joined`, `peer_list`, `channel_message`, `key_exchange`, `peer_disconnected`, `session_error`, `error`, `pong` (`src/relay/embedded.js:34, 92, 117, 154, 177, 195, 206, 224, 239, 264`). The bridge has no case for `error`, so "Rate limit exceeded" and "Message too large" are silently dropped (`src/bridge-agent/index.js:559-705`) |
| UI → bridge | `set_name`, `create_session`, `join_session`, `send_message`, `leave_session` (`src/bridge-agent/index.js:193-212`) |
| Bridge → UI | `state`, `session_created`, `session_joined`, `session_peer_joined`, `peer_list`, `channel_message`, `peer_disconnected`, `relay_disconnected`, `relay_reconnecting`, `encryption_status`, `tunnel_status`, `session_error` |
| MCP ↔ bridge (IPC) | requests `get_messages`, `send_message`, `get_status`, `share_file`, `get_shared_files`; replies `messages`, `message_sent`, `status`, `file_shared`, `shared_files`, matched by `_ipcId` (`src/bridge-agent/index.js:215-298`); plus every local broadcast pushed unsolicited (`:355-357`) |

Relay limits: 60 messages per minute per connection (`src/relay/embedded.js:59-70`), 1 MB per message (`:96`), heartbeat every 45 s with 3 missed pongs tolerated (`src/shared/constants.js:23-24`).

### 1.4 Pairing and session codes

- Code: 8 characters from a 32-symbol alphabet, from `crypto.randomBytes` (`src/shared/protocol.js:7-15`). 256 is divisible by 32, so there is no modulo bias; that is **40 bits**. The relay header comment still says "6-digit codes" (`src/relay/embedded.js:4`) — stale.
- The code is the only credential. Knowing it lets you look up the relay URL and join.
- A waiting session (creator only) expires after 30 minutes (`src/shared/constants.js:12`, `src/relay/embedded.js:27-40`). **Once one peer has joined, the code never expires and stays joinable** for the life of the session, with no cap on the number of peers (`src/relay/embedded.js:158-174`).
- The registry entry lives 24 hours (`worker/api.js:50`).
- Peer IDs are letters assigned by position (`src/relay/embedded.js:128-130`). After a leave, the next joiner can receive an ID that is already in use (A, B, C; B leaves; the next joiner gets index 2 = "C" again).
- There is no notion of a persistent identity, a contact, a device key, or a previously-paired peer. Display names are free text (`src/ui/app.js:194-198`).

### 1.5 End-to-end encryption

- Each side generates an ephemeral X25519 key pair when the session pairs and sends the public key as a `key_exchange` message through the relay (`src/bridge-agent/index.js:748-760`).
- On receipt it derives `HKDF-SHA256(ECDH, salt = empty, info = "claude-bridge-e2e", 32 bytes)` (`src/shared/crypto.js:22-38`).
- Messages are AES-256-GCM with a random 96-bit IV; the whole message JSON is the plaintext (`src/shared/crypto.js:44-57`, `src/bridge-agent/index.js:316-325`).
- One key is used for both directions. No associated data, no counters.
- For two peers this works as described. For three or more it does not: see finding S9.

### 1.6 Claude Code integration

Four separate mechanisms deliver bridge content to Claude:

1. **MCP tools** — `bridge_read_messages`, `bridge_send_message`, `bridge_status`, `bridge_share_file`, `bridge_get_shared_files` (`src/mcp-server/index.js:171-219`). Registered at **user scope** on every start of the bridge: `claude mcp add --scope user … claude-bridge` (`bin/claude-bridge.js:112`), so every Claude Code session on the machine gets the tools.
2. **Unread alert on every tool result** — remote message text is appended to each tool response under the heading "UNREAD BRIDGE MESSAGES — You MUST read and respond to these NOW" (`src/mcp-server/index.js:60-73`, `:153-160`).
3. **Stop hook** — `.claude/settings.json:3-12` runs `scripts/check-bridge.sh`, which fetches `http://localhost:3847/api/unread` and returns `decision: block` with the remote messages as the reason (`scripts/check-bridge.sh:6`, `:23-26`), so Claude is prevented from stopping until it deals with them.
4. **PTY keystroke injection (Electron only)** — the Electron main process listens on the local UI WebSocket and writes every `claude-team` message into the terminal followed by Enter (`electron/main.js:82-98`).

`CLAUDE.md` and the skill tell Claude to treat bridge messages as work: "If it's a task/instruction — execute it and report results back" (`CLAUDE.md:46`, `SKILL.md:27`) and "Messages from the other Claude agent deserve the same attention as human messages" (`SKILL.md:43`).

`share_file` shares text that Claude chooses to paste; there is no file transfer, no diff, and no link to an actual file on disk (`src/bridge-agent/index.js:250-290`).

### 1.7 Relay, worker and tunnel roles

- **Relay**: stateless forwarder; never inspects payloads; forwards `channel_message` and `key_exchange` to all other peers in the session (`src/relay/embedded.js:214-242`). Can also run standalone (`bin/claude-bridge.js:17-19`, `Dockerfile.relay`), selected with `CLAUDE_BRIDGE_RELAY`.
- **Worker**: unauthenticated key-value registry for code → tunnel URL (`worker/api.js:44-63`), mixed in the same file with the download paywall (`:65-201`).
- **Tunnel**: `cloudflared tunnel --url http://localhost:3848 --no-autoupdate` (`src/tunnel/manager.js:327-331`), URL parsed from stderr (`:371`). Looks for the binary on `PATH`, then `~/.coagent/bin`, then runs `brew install cloudflared`, then downloads from GitHub "latest" (`:127-178`).

### 1.8 Electron packaging

- `electron/package.json:13-35` carries an `electron-builder` config, but the shipped installers do not use a built app. `scripts/pack.js:33-46` tars the source; `install.sh` copies it to `~/coagent`, runs `npm install`, rebuilds `node-pty`, and writes a shell-script `.app` wrapper that runs `electron .` from the source tree (`site/downloads/install.sh:209-255`). Nothing is code-signed or notarised.
- The window loads a local HTML file (`electron/main.js:41`) which pulls xterm.js from a CDN (`electron/split-view.html:274-275`) and embeds `http://localhost:3847` in an iframe (`:270`).
- The terminal is a general login shell (`electron/main.js:122`, `:143-149`); "Launch Claude" types `claude` into it, optionally with `--dangerously-skip-permissions` chosen by a toggle on the launch screen (`electron/main.js:180-184`, `electron/split-view.html:244-249`).
- Version drift: `electron/package.json:3` says 0.3.0; the root package is 0.4.4.

---

## 2. Security review

Threat model used: the new goal connects agents "belonging to anyone in the world", so **the session peer is treated as potentially hostile**, as are web pages open on the user's machine, other devices on the same network, and the relay/registry operator.

### Critical

**S1. Remote text is typed into the local terminal, unsanitised, before and regardless of approval** *(by reading)*
`electron/main.js:82-98` writes `"[CoAgent - AI Interactive Chat] <sender> (<type>): <content>" + "\r"` to the PTY for every `claude-team` message. Consequences:
- The content is delivered to Claude as a **user prompt**, the highest-trust input Claude has.
- Content is written raw. Embedded carriage returns and control characters are not stripped, so one message can submit several lines, and (not tested) could interrupt Claude and reach the underlying shell, which is the same PTY (`electron/main.js:143`).
- The comment says "only inject messages from remote peers (not our own)" (`:84`) but the code only excludes `system`. Locally-originated messages are injected too, including the local Claude's own outgoing messages, which the bridge echoes to all local sockets (`src/bridge-agent/index.js:339`).
- The "📋 Instruction from…" message that the approval popup is about is itself a `claude-team` message (`src/ui/app.js:245-251`), so it is injected the moment it arrives, before anyone clicks Approve.

**S2. A session peer can run script in the other side's UI, and from there type into their terminal** *(by reading)*
- `src/ui/app.js:514` assigns `peer.innerHTML = peerText…`, where `peerText` contains the remote peer's display name unescaped (`:497-498`). The name comes from the joiner via the relay's `peer_list`. No click is needed.
- `src/ui/app.js:437`, `:442`, `:457` interpolate the remote-supplied message `id` into HTML attributes and inline `onclick` handlers without escaping. Message bodies and sender names in the list are escaped (`:467`, `:471`); the `id` and the header peer name are not.
- In the Electron app the UI runs in an iframe whose parent accepts `postMessage({type:'instruct-claude', text})` from any origin and writes the text plus Enter to the PTY (`electron/split-view.html:513-518` → `electron/preload.js:6` → `electron/main.js:162-164`).
- Chain: hostile display name or message id → script in the local UI → keystrokes into a shell. If Claude is not running in that terminal, the text is a shell command.
- There is no Content-Security-Policy on either page (0 occurrences in `electron/split-view.html` and `src/ui/index.html`).

**S3. Any web page the user visits can drive the bridge and prompt the local Claude** *(by reading)*
- The local WebSocket server accepts every connection with no Origin check and no token (`src/bridge-agent/index.js:141-164`). Browsers do not apply same-origin policy to WebSocket connections.
- On connect it sends the full state: session code and all messages on both channels (`:146-155`).
- The page can then send `send_message` on `claude-team`; `_sendChannelMessage` stores and broadcasts locally even with no session (`:300-340`), and S1 types it into Claude's terminal. No session and no peer are required.
- It can also `join_session` with an attacker-created code, or `leave_session`.

**S4. The key exchange is unauthenticated, and encryption silently downgrades**
- Public keys travel through the relay with nothing binding them to the session code or to a person (`src/bridge-agent/index.js:748-792`). There is no fingerprint, safety number or short-authentication-string for the humans to compare. Whoever controls the path — the relay host, Cloudflare (which terminates TLS for the tunnel), or anyone who can change the registry entry (S6) — can substitute keys and read and alter everything.
- Plaintext is always accepted: an incoming `channel_message` without `encrypted` is stored and displayed as normal (`:670-674`).
- If key exchange fails the session "continues to work" unencrypted (`:756-759`, `:786-791`). Anything sent between pairing and key completion goes out in clear (`:333-335`).
- The only indication is the absence of a small lock icon (`src/ui/app.js:570-580`). A relay that drops the two `key_exchange` messages gets a plaintext session.

**S5. Approval is cosmetic**
- Approval state is an object in the browser page: `state.instructionApprovals` (`src/ui/app.js:19`, `:287`, `:315`). The bridge agent, the MCP server and the relay know nothing about it. It is lost on page reload (the `state` message does not carry it, `src/bridge-agent/index.js:146-155`).
- "Approve" just posts the text to the terminal and sends a chat line "✅ X approved" (`src/ui/app.js:282-311`). "Reject" only sends a chat line (`:314-326`).
- An instruction is recognised by its text starting with `📋 Instruction from` (`:101-104`, `:447`). Any message that does not start that way gets no prompt at all.
- Independently of the popup, the same text reaches Claude via PTY injection (S1), via `bridge_read_messages` and the unread alert (`src/mcp-server/index.js:60-73`), and via the Stop hook (`scripts/check-bridge.sh:23-26`).
- README line 33 ("requires approval from all participants") and `src/ui/index.html:120` ("Both humans must approve before their Claude acts on this") describe behaviour the code does not enforce.

### High

**S6. Registry: anyone can register or overwrite any code**
`POST /api/sessions/register` takes `{code, tunnelUrl}` with no authentication, no proof of ownership and no check on the URL (`worker/api.js:44-55`). Anyone who learns a code can re-point it at their own relay for the next joiner or the next reconnect; combined with S4 that is a full man-in-the-middle. No rate limiting is visible in the worker code for register or lookup (whether Cloudflare-level rules exist was not verified). CORS is `*` (`:22-26`).

**S7. Local services listen on all network interfaces with no authentication**
- UI/API server: `server.listen(this.port)` with no host (`src/bridge-agent/index.js:166`).
- MCP IPC: `server.listen(IPC_PORT)` with no host (`:190`). README line 92 calls this port "local only"; the code does not bind it to loopback. Anyone who can reach port 3849 can read all messages and send messages as "Claude" (`:219-235`).
- Relay: `new WebSocketServer({ port })` (`src/relay/embedded.js:22`).
- `GET /api/logs` serves the tail of the log file to anyone who can reach port 3847 (`src/bridge-agent/index.js:73-84`). The log contains session codes and the tunnel URL (`:433`, `:403`, `:573`).
- `GET /api/unread` changes state on a GET (advances the read cursor, `:131-133`), so any page can silently swallow messages that the Stop hook would otherwise have delivered.
- No Host-header check, so DNS-rebinding is not defended.

**S8. Remote content is framed to Claude as mandatory, by design**
Leaving aside the bugs above, the intended behaviour is prompt injection as a feature: `CLAUDE.md:29-35` and `SKILL.md:13-16` make monitoring the bridge "highest priority", `CLAUDE.md:46` says to execute instructions, and the MCP alert says "You MUST read and respond to these NOW" (`src/mcp-server/index.js:60`). The remote peer's text is never marked as untrusted. The only real control between a remote instruction and an action on the local machine is Claude Code's own permission prompt — and the launch screen offers a switch to turn that off (`electron/main.js:180`).
Related: the README says Claudes cannot see the Human Chat channel (`README.md:26`, `:51`). They can: the tool accepts `channel: "human"` (`src/mcp-server/index.js:178`), the unread alert includes it (`:63`), and so does `/api/unread` (`src/bridge-agent/index.js:115`).

**S9. Sender identity is self-asserted, and sessions with three or more peers break encryption** *(by reading)*
- `sender.peerId`, `sender.name` and `sender.type` are fields inside the message that the sender fills in (`src/shared/protocol.js:29-42`). The receiver trusts them (`src/bridge-agent/index.js:656-658`). A peer can label a message as `system`, as a human, or as another participant.
- With a third peer: the newcomer broadcasts its public key; each existing peer overwrites its single `sharedSecret` with one derived against the newcomer (`:781`) and does not reply because it already has a key pair (`:772`). The two original peers can then no longer decrypt each other, and the newcomer has no key and sends plaintext, which is accepted (S4). The UI shows a warning that E2E "only works between 2 peers" (`:612-623`) but the session carries on. An undecryptable message that reaches a peer with no secret falls into the plaintext branch with `channel` undefined (`:670-674`).
- A third party who obtains the code can join at any time (section 1.4); the only signal is a "joined" toast.

**S10. No replay, ordering or delivery guarantees**
No sequence numbers, no acknowledgement, no de-duplication on the message `id`. A relay can replay, reorder or drop ciphertexts undetected. Messages sent while the relay socket is down are stored locally and never sent (`src/bridge-agent/index.js:315`). For chat this is tolerable; for approvals and action records it is not.

### Medium

**S11. Code is fetched and run without verification**
- `cloudflared` is downloaded from GitHub "latest" with no checksum or signature check and made executable (`src/tunnel/manager.js:20`, `:153-170`); before that, `brew install cloudflared` is run without asking (`:144`).
- Updates run `curl … install.sh | bash` (`bin/claude-bridge.js:63-65`); the installer does the same for Node and Homebrew (`site/downloads/install.sh:45`, `:56`).
- The Electron renderer that holds the terminal-input API loads two scripts from a CDN with no integrity attribute (`electron/split-view.html:274-275`; 0 `integrity=` attributes for 2 remote scripts).
- The bridge edits the user's global Claude Code configuration on every start without asking (`bin/claude-bridge.js:112`).

**S12. Secrets and credentials on disk in the project**
Reported by location only:
- `agents/.env:17` — a non-empty API key. `.gitignore:1-3` does not exclude `.env` files.
- `MARKETING-PLAYBOOK.md:203` — an account username and password in clear text.
- `MARKETING-PLAYBOOK.md:420` — an API key literal inside a command example.
- `3_Access_Keys/github_deploy_rw` — a private deploy key inside the project folder; `.gitignore` does not exclude `3_Access_Keys/` (contents not opened).
- `worker/api.js:10-12` — the free-download discount code is hard-coded (also repeated in `agents/prompts/system.md`).
The folder has no `.git`, so whether any of these reached GitHub is **not verified**. `scripts/pack.js:33-40` does not copy `agents/`, `3_Access_Keys/` or the marketing files into release archives (the archives themselves were not opened to confirm).

**S13. Join rate limit is weak and misplaced**
Five join attempts per IP per minute (`src/relay/embedded.js:72-83`), counted for successful joins and reconnects as well (`:160`). Behind the tunnel every client arrives from the local `cloudflared` process, so the limit is effectively global: a handful of bad attempts locks legitimate joiners and reconnects out for a minute (inferred from how quick tunnels connect; not tested). At 40 bits the code is not practically guessable online, so brute force is not the real exposure — S6 and code leakage are.

### Low / adjacent

- **S14.** The download paywall in `worker/api.js` is bypassable: `update_from=<any other version>` returns the file with no token (`:132-143`), and PayPal transaction IDs are accepted without verification (`:79-90`). Error responses include a stack trace (`:182`). Not part of the collaboration product, but it lives in the same worker as the registry.
- **S15.** Messages are never written to the log (good), but nothing is persisted either — there is no audit trail of any kind.
- **S16.** Electron: `nodeIntegration: false`, `contextIsolation: true` are set (`electron/main.js:34-35`), which is correct; the problem is what the exposed `sendTerminalInput` API allows (S2).

---

## 3. Gap analysis against the goal

| Goal item | Exists | Partial | Missing |
|---|---|---|---|
| **Link two agents anywhere in the world** | NAT traversal works in principle: creator-hosted relay + Cloudflare quick tunnel + code registry (1.2). 40-bit one-time-ish code. | Pairing is "whoever has the code". Depends on a third-party free tunnel service and one unauthenticated worker. | Any identity (person, device or agent). Authenticated key exchange / peer verification. Persistent pairing ("connect to Sam again"). Discovery. Code expiry after use. Peer cap. A hosted relay option for when tunnels are blocked. |
| **Phase 1: two Claude Code agents** | MCP tools, skill, Stop hook, PTY injection (1.6). Two Claudes can exchange text and pasted snippets. | Delivery of incoming messages relies on Claude choosing to poll, or on keystroke injection. | Any structured notion of a task, request, result or action. |
| **Phase 2: agent-agnostic** | The relay and the crypto are agent-neutral. MCP is a cross-vendor standard. | — | Everything Claude-facing is Claude-specific: `sender.type: 'claude'`, channel name `claude-team`, `claude mcp add`, the Stop hook format, the PTY that launches `claude`, `CLAUDE.md`. No adapter boundary exists. |
| **CONTROLLED mode — see and approve every file, folder, service the remote agent touches** | Nothing. | An approve/reject popup for one specially-prefixed chat message (S5). | Visibility of actions. An enforcement point. Per-resource scoping. Any record of decisions. |
| **APPROVED TRUST mode — follow live, pause, ask, revoke** | Nothing. | The local user can watch their own terminal pane. "Leave session" ends everything. | Trust grants with scope and expiry. Live action stream to the watching side. Pause. Revoke. Kill switch that stops an in-flight action. |
| **UI: chat bottom, main pane of changing code/elements, approvals + history right** | A chat UI; an Electron split with terminal left and chat right. | — | The main activity pane, the approvals pane, history. The current UI is one hand-templated page with two tabs. |
| **Use cases: troubleshoot, security audit, remote configuration, collaboration on someone else's machine** | General chat collaboration. | A remote party can already cause work on the local machine — by instructing the local Claude — but uncontrolled. | Controlled remote operation: scoped access, read-only vs write, command gating, evidence/audit output, session recording. |

### The hard gap: chat versus actions

**What the bridge sees today.** Only strings that a human typed or that Claude chose to pass to `bridge_send_message` / `bridge_share_file`. The agent's real actions — file reads and writes, shell commands, network calls, other MCP tools — happen inside Claude Code and never pass through any CoAgent code. The bridge cannot list them, show them, delay them or stop them. The terminal bytes are rendered only in the local window (`electron/main.js:151-155`) and are not sent to the peer.

**Which direction the gate must face.** In the goal, the remote side drives and the local user approves what happens on the local machine. In the current build the path is: remote text → local Claude → local Claude's own tools. So the actions to observe and gate are the **local** Claude's tool calls made on behalf of the remote party. The only gate on that path today is Claude Code's built-in permission prompt in the terminal pane. It is per tool call rather than per remote request, carries no attribution to who asked, leaves no history, is invisible to the remote side, and can be switched off at launch.

**Where a hook would have to go in this code.**

1. *The interception point is in the agent host, not in the bridge.* The existing `.claude/settings.json` registers only a `Stop` hook (`:3`). `scripts/check-bridge.sh` is nonetheless the one pattern in the codebase that points the right way: a Claude Code hook that calls the bridge agent over local HTTP and returns a blocking decision. Gating actions means the same shape on the tool-call path — a hook that fires before each tool runs, sends the tool name and arguments to the bridge agent, and waits for allow/deny — plus an after-the-fact event for the live view. (Claude Code's hook and permission mechanisms were not re-checked against current documentation as part of this review; the design step should confirm what they can block and what they can see.)
2. *The decision must live in the bridge agent process.* `src/bridge-agent/index.js` is the right place architecturally — it is the one long-lived local component — but today it holds only `messages`, `peers` and a key (`:31-58`). It would need pending-request state, a policy/trust store, an append-only decision log and timeouts, none of which exist.
3. *The protocol needs typed messages.* The body shape is chat (`channel` + `content` string, `src/shared/protocol.js:29-42`). Action requests, decisions, action events, trust grants/revocations and pause signals would have to be new message kinds with versioning, sequence numbers and acknowledgement.
4. *The UI would only display and collect decisions.* Today the UI is the sole holder of approval state (S5); that has to be inverted.

**Can the current architecture carry it?**

- *Topology — yes.* A local daemon per side, a relay that only forwards, and an encrypted envelope are a workable base. The relay already forwards unknown payloads untouched, so new encrypted message kinds pass without relay changes.
- *As built — no, for five concrete reasons:*
  1. **The local trust boundary is open.** An approval would arrive on the same unauthenticated `/ws` that any web page or LAN device can use (S3, S7). An approval that any tab can forge is not an approval. This must be fixed before anything is built on top.
  2. **The peer is unauthenticated** (S4, S9). "Trust granted to Sam" has no meaning when nothing identifies Sam's key.
  3. **Transport limits.** 60 messages a minute per connection and silent drops over it (`src/relay/embedded.js:59-70`, `:92`), no ordering, no acks, no replay protection (S10). A live action stream would exceed the rate limit almost immediately.
  4. **No persistence.** 500 messages per channel in memory, wiped on leave (`src/shared/constants.js:13`, `src/bridge-agent/index.js:518`). There is nowhere for approval history to live.
  5. **Claude-specific interception.** Hooks solve Phase 1 only. For Phase 2 the interception point must be something every agent can be made to go through; the code has no abstraction for that today. This is the central design question for the next step (see section 5).
- *The PTY-injection path cannot be evolved into a gate.* It is the opposite of one — it converts remote text into trusted local input — and should not be carried forward.

---

## 4. Keep / refactor / rewrite

| Component | Verdict | Reason |
|---|---|---|
| `src/shared/crypto.js` | **Keep the primitives, rewrite the handshake around them** | X25519, HKDF and AES-256-GCM via Node's built-in crypto are used correctly as primitives. What is missing is authentication of the peer key, binding to the session, separate keys per direction, counters and a refusal to fall back to plaintext. |
| `src/shared/protocol.js` | **Rewrite** | 59 lines; chat-shaped; no version, sequence or schema validation. `makeSessionCode` can be kept. |
| `src/relay/embedded.js` | **Refactor** | The forward-only design is right and small. Fix peer-ID reuse, the misplaced join limit, the rate limit that would throttle an action stream, the missing peer cap and code expiry, and add an error handler (a port clash currently has none — by reading, an unhandled `error` event). |
| `src/tunnel/manager.js` | **Keep, harden** | The most carefully written file: pre-flight checks, timeouts, clean shutdown, clear errors. Needs a pinned and verified binary instead of "latest", no silent `brew install`, and a restart path when the tunnel drops (today it is only logged, `src/bridge-agent/index.js:391-394`). Keep only if creator-hosted relay remains the model. |
| `worker/api.js` (registry part) | **Rewrite** | Unauthenticated overwrite (S6), 24-hour entries, no validation. Should also be separated from the download paywall. Delete the dead `worker/session-registry.js`. |
| `src/bridge-agent/index.js` | **Rewrite** | It is the right component in the wrong shape: one 800-line class mixing HTTP, WebSocket, IPC, relay client, crypto and session state; no authentication on any local surface; no persistence; the encrypt-and-send block is duplicated (`:264-285` and `:315-336`). The new core (policy, approvals, audit) belongs here and changes most of it. |
| `src/mcp-server/index.js` | **Refactor** | Sound use of the MCP SDK and a reasonable IPC client. Reusable as the Claude adapter. Remove the "MUST respond NOW" framing, fix the own-message filter that can never match (`:40` compares `peerId` to the literal `'self'`), and authenticate the IPC link. |
| `src/ui/` | **Rewrite** | String-templated `innerHTML` with unescaped remote values (S2); holds security state it should not own (S5); layout unrelated to the target UI. |
| `electron/` | **Rewrite** | The PTY-injection model (S1), the unchecked `postMessage` path (S2), CDN scripts, and the skip-permissions toggle all have to go. Not actually packaged as an app (1.8). Whether a desktop shell is needed at all is an open question. |
| `CLAUDE.md`, `SKILL.md`, Stop hook | **Rewrite** | They instruct Claude to obey remote text (S8). The new instructions must say the opposite: remote content is untrusted data. The hook-calls-the-daemon pattern in `check-bridge.sh` is worth keeping as an idea. |
| `bin/claude-bridge.js` | **Refactor** | Fine as a mode switch. Remove the silent global `claude mcp add` and the `curl | bash` updater. |
| Installers, `scripts/pack.js` | **Refactor later** | Work as scripts; unsigned; pipe-to-shell; not relevant until there is something new to ship. |
| `agents/`, `promo/`, marketing files, media scripts | **Separate from the product** | Unrelated to the bridge. They hold the credentials listed in S12. `playwright` is a production dependency of the bridge (`package.json:21`) apparently only for media capture. |

### Code quality notes

- **Tests:** none. No test files, no test script in `package.json:9-14`, no lint config, no CI config found.
- **Version control:** no `.git` in the folder; `CLAUDE.md:6-8` names a GitHub repo and says the on-disk layout differs from the expected one (`CLAUDE.md:21`).
- **Error handling:** many empty `catch {}` blocks (for example `src/mcp-server/index.js:52`, `:114`; `src/bridge-agent/index.js:356`; `electron/main.js:101`). No `error` handlers on the HTTP server, the IPC server or the relay server, so a busy port is likely to crash the process (by reading); the installer works around this by force-killing whatever holds the three ports (`site/downloads/install.sh:228`).
- **Reconnection:** the bridge retries the relay once, 3 seconds after a drop, by re-sending `join_session` with the saved code (`src/bridge-agent/index.js:719-733`). There is no backoff and no second attempt if that fails. The rejoin arrives as a brand-new peer with a new ID and consumes the join limit. If the creator was alone when the socket dropped, the relay has already deleted the session (`src/relay/embedded.js:256-259`) and the rejoin fails. The UI and the MCP server each retry their local connection every 2 seconds indefinitely (`src/ui/app.js:44`, `src/mcp-server/index.js:126`).
- **State persistence:** none. Everything is in memory. The UI's Cancel button closes only its own socket and does not tell the bridge to leave, so the relay, tunnel and code stay live (`src/ui/app.js:660`).
- **Self-echo:** the local Claude's own outgoing messages are pushed back to it as unread via IPC (`src/bridge-agent/index.js:355-357`, `src/mcp-server/index.js:40`) and, in Electron, typed back into its terminal (S1). Whether this causes loops in practice was not tested.
- **Documentation drift:** the README quick start describes a manual two-terminal relay setup (`README.md:7-21`) that the default flow no longer needs; "6-digit" comment in the relay; several README claims do not match the code (S5, S7, S8).
- **Style:** plain CommonJS, no types, no schema validation of any inbound message from the relay, the UI socket or the IPC socket.

---

## 5. Open questions for the owner

1. **Which machine does the work, and whose agent?** The use cases describe one side operating on the other side's system. Is the model (a) the remote agent instructs the *local* agent, which acts with local tools under local approval, or (b) the remote agent itself is given tools that execute on the local machine through the bridge? The two lead to different enforcement points, and (b) is the one that is naturally agent-agnostic.
2. **How strong must the gate be?** Is it acceptable for control to depend on the local agent host cooperating (hooks, permission callbacks), or must it hold even if the agent is misled — which implies OS-level isolation (container, sandbox, separate user) around whatever executes?
3. **What is a peer's identity?** A person, a device, an agent instance, an organisation? Should pairing be remembered, and should humans verify each other (short code read aloud, QR) on first contact?
4. **Who runs the relay and registry?** Stay with creator-hosted relay plus free Cloudflare quick tunnels (no uptime commitment, blocked on some corporate networks), or operate a hosted relay? This also decides what the service operator can see and is liable for.
5. **How fine is "every file, folder or service"?** Per individual action, per path/command pattern, per task? And in trust mode, what scopes and expiries does a grant have, and are some actions (credentials, deletion, outbound network) never coverable by trust?
6. **Is an audit record a product requirement?** For security-audit and remote-configuration use, should the session produce a durable, exportable, tamper-evident log, and on which side(s) is it stored?
7. **Two parties only, or groups?** The current multi-peer support is broken at the encryption layer (S9). Dropping it for the new version would simplify identity, keys and approvals considerably.
8. **Is a desktop app required for Phase 1?** Or is a local daemon plus browser UI plus the user's own terminal enough, deferring signed desktop packaging?
9. **What happens to the current release?** v0.4.4 is downloadable from the live site and carries S1–S3. Should it be withdrawn or carry a warning while the new version is built?
10. **Housekeeping to confirm:** were the credentials in S12 ever pushed to GitHub (and should they be rotated regardless), and where is the canonical git history for this code?
